"""How faithful is brainfly.optic's port of flyvis to MaleCNS wiring? (Descriptive, not pre-registered.)

eyepath_fast.py found LC4 nearly unmoved by looms of any speed, while LPLC2 responded. This compares
the port (FlyvisOpticLobe, right side, mean over neurons) with the original flyvis network on its own
connectome (flow/0000/000, central column), both at 2 ms steps:
  rest     each type's voltage after settling on grey
  dOFF     its change 0.1 s into a full-field OFF step (grey 0.5 -> 0.1)
  missing  the resting input current the port lacks, per source type: pairs from flyvis types the
           port leaves out (CT1) or MaleCNS lacks (Mi3, Mi11, Mi12, Tm28), and pairs that some MaleCNS
           neurons of the target type don't have. Computed with the original's resting activity for
           every source, so it isolates wiring from activity.
Also T2's response to full-field ON and OFF steps in the original (LC4's largest input; a real T2 is
excited by both, Keles et al. 2020).

    python experiments/flyvis_port.py            (writes experiments/flyvis_port.json)
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.data import DATA
from brainfly.eye2d import CompoundEye
from brainfly.optic import GRADED as OPTIC, MODEL, FlyvisOpticLobe, flyvis_params

OUT = Path(__file__).with_name("flyvis_port.json")
DT = 0.002


def original() -> dict:
    """The original network: per type, resting V, dOFF, and the ON/OFF step responses of T2."""
    os.environ.setdefault("FLYVIS_ROOT_DIR", str(DATA / "flyvis"))
    import torch
    import flyvis
    from flyvis import NetworkView

    flyvis_params(MODEL)                                             # fetches the models if needed
    net = NetworkView(flyvis.results_dir / MODEL).init_network(checkpoint="best")
    c = net.connectome
    types = np.asarray(c.nodes.type[:]).astype(str)
    u, v = np.asarray(c.nodes.u[:]), np.asarray(c.nodes.v[:])
    n_hex = int((types == "R1").sum())
    steps = int(round(0.1 / DT))
    with torch.no_grad():
        state = net.steady_state(10.0, DT, 1)
        grey = net.simulate(torch.full((1, 5, 1, n_hex), 0.5), DT, initial_state=state).cpu().numpy()[0]
        step = {level: net.simulate(torch.full((1, steps, 1, n_hex), level), DT, initial_state=state).cpu().numpy()[0]
                for level in (0.1, 0.9)}
    centre = {t: int(np.flatnonzero((types == t) & (u == 0) & (v == 0))[0]) for t in np.unique(types)}
    rest = {t: float(grey[-1, k]) for t, k in centre.items()}
    rest["R1-6"] = float(np.mean([rest[f"R{i}"] for i in range(1, 7)]))
    doff = {t: float(step[0.1][-1, k] - grey[-1, k]) for t, k in centre.items()}
    doff["R1-6"] = float(np.mean([doff[f"R{i}"] for i in range(1, 7)]))
    k = centre["T2"]
    t2 = {"ON": float(step[0.9][:, k].max() - grey[-1, k]), "OFF_up": float(step[0.1][:, k].max() - grey[-1, k]),
          "OFF_down": float(step[0.1][:, k].min() - grey[-1, k])}
    return {"rest": rest, "dOFF": doff, "T2": t2}


def port() -> tuple[dict, FlyvisOpticLobe, np.ndarray]:
    brain = FlyBrain(batch=1, graded=OPTIC, fill_retina=True, dt=DT)
    ol, eye = FlyvisOpticLobe(brain, gain=1.0), CompoundEye(brain)
    right = brain.side.astype(str)[ol.neurons] == "R"
    ol.reset()
    v0 = ol.V.copy()
    off = np.where(eye.placed, -0.8, 0.0).astype(np.float32)          # grey 0.5 -> 0.1
    for _ in range(int(round(0.1 / DT))):
        ol.step(off)
    out = {"rest": {}, "dOFF": {}, "n": {}}
    for t in sorted(set(ol.types)):
        m = (ol.types == t) & right
        if m.any():
            out["rest"][t] = float(v0[m].mean())
            out["dOFF"][t] = float((ol.V[m] - v0[m]).mean())
            out["n"][t] = int(m.sum())
    return out, ol, right


def missing(ol: FlyvisOpticLobe, right: np.ndarray, orig_rest: dict) -> dict:
    p = flyvis_params(MODEL)
    W = ol.W.tocsr()
    present = set(ol.types)
    rows = {t: np.flatnonzero((ol.types == t) & right) for t in present}
    cols = {t: np.flatnonzero(ol.types == t) for t in present}
    out = {}
    for (s, t), (sign, strength, total) in p["pairs"].items():
        if t not in present:
            continue
        expected = sign * strength * total * max(orig_rest.get(s, 0.0), 0.0)
        coverage = float((np.diff(W[rows[t]][:, cols[s]].tocsr().indptr) > 0).mean()) if s in present else 0.0
        if abs(expected * (1 - coverage)) > 0.01:
            out.setdefault(t, []).append({"source": s, "current": round(expected * (1 - coverage), 3),
                                          "coverage": round(coverage, 2), "left_out": s not in present})
    return {t: sorted(v, key=lambda x: -abs(x["current"])) for t, v in out.items()}


def main() -> None:
    o = original()
    pt, ol, right = port()
    miss = missing(ol, right, o["rest"])
    table = []
    for t in pt["rest"]:
        if t not in o["rest"]:
            continue
        table.append({"type": t, "orig_rest": round(o["rest"][t], 2), "port_rest": round(pt["rest"][t], 2),
                      "orig_dOFF": round(o["dOFF"][t], 2), "port_dOFF": round(pt["dOFF"][t], 2), "n": pt["n"][t],
                      "missing_current": round(sum(x["current"] for x in miss.get(t, [])), 2)})
    table.sort(key=lambda r: -abs(r["port_rest"] - r["orig_rest"]))
    print(f"{'type':9s} {'orig rest':>9s} {'port rest':>9s} {'orig dOFF':>9s} {'port dOFF':>9s} {'missing':>8s}  largest missing inputs")
    def part(x: dict) -> str:
        return f"{x['source']} {x['current']:+.2f} " + ("(left out)" if x["left_out"] else f"cov {x['coverage']:.2f}")

    for r in table:
        parts = "; ".join(part(x) for x in miss.get(r["type"], [])[:3])
        print(f"{r['type']:9s} {r['orig_rest']:+9.2f} {r['port_rest']:+9.2f} {r['orig_dOFF']:+9.2f} {r['port_dOFF']:+9.2f} "
              f"{r['missing_current']:+8.2f}  {parts}")
    print("original T2, full-field steps:", {k: round(v, 2) for k, v in o["T2"].items()})
    OUT.write_text(json.dumps({"description": __doc__, "types": table, "missing": miss, "original_T2": o["T2"]}, indent=1))


if __name__ == "__main__":
    main()
