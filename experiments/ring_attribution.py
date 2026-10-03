"""Exploratory, not pre-registered: which ring cell type's input from outside the ring makes the whole-brain bump lean?

Alone, the head-direction ring's bump visits every heading evenly (ring_homeostasis.py --slow --fit ring_fit3).
Inside the whole brain it leans toward part of the ring, before homeostasis in place (ring_whole.py --homeostasis) and
after it (rung4_rest.py, rung4_anneal.py). Neither its loops through the brain (ring_loops.py) nor its outside input's
mean or variance by wedge (ring_inputs.py) explain that. The ring in the whole brain differs from the ring alone in one
way: each ring neuron also gets its real input from neurons outside the ring, whose mean ring_insitu.tune corrects
neuron by neuron. This gives that input back to one cell type at a time.
Model: ring_insitu.py's brain (brain seed 9) with rung4_anneal.py's calibrated group biases for the rest of the brain.
Every ring neuron gets its offset from ring_homeostasis.py --slow --fit ring_fit3, as in the ring alone. For the
condition's cell types, the ring neurons keep their synapses from outside the ring, and their offsets are lowered by
that input's mean: each outside input's resting rate in ring_insitu.py's measurement (ring_insitu/measure.npz), times
its weight, its depression's steady efficacy and the synaptic time constant, as ring_insitu.tune. For the other types,
every synapse from outside the ring onto them is removed. Conditions: none (the ring alone in the whole brain, its
loops cut at the ring's input), all, and each of EPG, PEN_a, PEN_b, PEG, Delta7, ER and ExR alone.
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9970, the same for every
condition): the BUMP measures, ring_landscape.py's per-wedge occupancy and EPG rates, and the ring groups' rates.
A condition allbut:<types> (comma-separated) keeps every ring neuron's real outside input except from neurons of those
types, which is removed, and lowers the offsets only by the mean of the input that remains (allbut:LPsP,LAL184: the
four neurons that give the EPGs 80% of their outside input).
A condition ending in -fit (none-fit, all-fit) gives the ring's neurons the parameters ring_fit.py fitted them with
(ring_insitu.build's fit_params): in the whole brain they reset 5 mV below rest, as rest_calibration2.py set for
every neuron, but the ring was fitted resetting to rest, and three ExR types depress by the brain's class rule.
Ran: the ring's outside input makes the bump lean, and the EPGs' share does nearly all of it. With no real outside
input the ring inside the whole brain passes BUMP: position entropy 0.92, resultants 0.41 and 0.43. With all of it,
it fails (0.85; 0.72 and 0.78), and with only the EPGs' it fails as badly (0.83; 0.93 and 0.82). Each other type's
outside input alone leaves the bump fly-like or near it: PEN_b, PEG, ER and ExR pass, and PEN_a and Delta7 miss only
on the resultants (0.65 and 0.62; 0.77 and 0.68). Four neurons give the EPGs 80% of that input: two LPsP and two
LAL184, excitatory, at the 2 Hz default target. Removing them changes nothing (0.86; 0.82 and 0.86), so the lean comes
from the remaining fifth, which includes inhibitory inputs from FB and LAL types spread very unevenly over the wedges
(wedge CV 0.9-2.6). With the ring's fitted parameters, the ring alone does even better (0.94; 0.10 and 0.02), but
with all outside input the lean is worse (0.69; 0.99 and 0.98), so that mismatch isn't the cause. One measurement per
condition.

    python experiments/ring_attribution.py <condition>   (writes experiments/ring_attribution/<condition>.json)
    python experiments/ring_attribution.py summary       (writes experiments/ring_attribution.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import rest_calibration as attempt1
import ring_insitu
import ring_landscape
import ring_whole
import rung4_anneal as r4a
import taste_escape as te
from brainfly import imaging
from brainfly.hybrid import TAU
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
GROUPS = ("EPG", "PEN_a", "PEN_b", "PEG", "Delta7", "ER", "ExR")
CONDITIONS = ("none", "all") + GROUPS + ("none-fit", "all-fit")
SEED = 9970
_subnetwork = ring_whole.subnetwork


def real_mask(types: np.ndarray, condition: str) -> np.ndarray:
    """The ring neurons that keep their real input from outside the ring."""
    groups = ring_whole.group_of(types)
    keep = np.zeros(len(types), bool)
    for g in (GROUPS if condition in ("all",) or condition.startswith("allbut:") else () if condition == "none" else (condition,)):
        keep[groups[g]] = True
    return keep


def removed_inputs(types: np.ndarray, condition: str) -> np.ndarray:
    """For allbut:<types>, the presynaptic neurons whose synapses onto the ring are removed; else none."""
    named = condition.split(":", 1)[1].split(",") if condition.startswith("allbut:") else []
    return np.isin(np.asarray(types).astype(str), named)


def partly_cut(condition: str):
    """ring_whole.subnetwork(p), then every synapse from outside the ring onto a ring neuron outside the condition's
    types removed (for allbut:<types>, every synapse onto the ring from those types)."""
    def make(p):
        inner = _subnetwork(p)

        def apply(M, types, superclass):
            M, slow, tau_slow = inner(M, types, superclass)
            ring, _ = ring_whole.ring_members(types)
            coo = M.tocoo()
            if condition.startswith("allbut:"):
                cut_rows = ring
                keep = ~(ring[coo.row] & removed_inputs(types, condition)[coo.col])
            else:
                cut_rows = ring & ~real_mask(types, condition)
                keep = ~(cut_rows[coo.row] & ~ring[coo.col])       # rows postsynaptic, columns presynaptic
            print(f"{condition}: removed {int((~keep).sum())} entries onto {int(cut_rows.sum())} ring neurons", flush=True)
            return sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=coo.shape), slow, tau_slow
        return apply
    return make


def run(name: str) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    condition, fit = name.removesuffix("-fit"), name.endswith("-fit")
    p = json.loads(Path(__file__).with_name(f"{ring_insitu.FIT}.json").read_text())["best"]["params"]
    ring_whole.subnetwork = partly_cut(condition)
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"], fit_params=fit)
    b, ring = s.brain, st["ring"]
    s.bias = np.load(r4a.HERE / "intact_state.npz")["group_bias"].copy()
    rates = np.load(Path(__file__).with_name("ring_insitu") / "measure.npz")["rates"].mean(0)
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    full = _subnetwork(p)(te.network_for(None)[0], s.types, np.asarray(b.superclass))[0].tocsr()
    kept = ~ring & ~removed_inputs(s.types, condition)
    mean_in = (full @ np.where(kept, rates / (1.0 + (1.0 - f) * rates * tau), 0.0)) * b.scale * W_SYN * TAU
    real = real_mask(s.types, condition)
    st["extra"][:] = np.where(ring, st["homeo"] - np.where(real, mean_in, 0.0), 0.0)
    b.set_bias(s.bias[s.gid])
    epg, side, glom = attempt1.epgs(s.types)
    _, r_runs, windows = attempt1.run(b, imaging.region_weights(), epg, seed=SEED)
    r = r_runs.mean(0)
    out = {"condition": name, "seed": SEED, **ring_landscape.landscape(windows, r_runs[:, epg], side, glom),
           "ring_group_hz": {g: round(float(r[m].mean()), 2) for g, m in st["groups"].items()},
           "real_input_neurons": int(real.sum()), "seconds": round(time.perf_counter() - t0)}
    bump = out["bump"]
    out["BUMP"] = bool(all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                           and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR") and out["bump_motion"]["MOVES_LIKE_A_FLY"])
    print(name, json.dumps({k: out[k] for k in ("BUMP", "wedge_rate_cv", "ring_group_hz")}),
          json.dumps({x: (bump[x]["strength"], bump[x]["shuffle_p99"], bump[x]["resultant"]) for x in "LR"}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}), flush=True)
    (HERE / f"{name.replace(':', '_').replace(',', '_')}.json").write_text(json.dumps(out, indent=1))


def summary() -> None:
    rows = {c: json.loads((HERE / f"{c}.json").read_text()) for c in CONDITIONS if (HERE / f"{c}.json").exists()}
    table = {c: {"entropy": d["bump_motion"]["position_entropy"], "D": d["bump_motion"]["drift_D_rad2_per_s"],
                 "resultants": [d["bump"][x]["resultant"] for x in "LR"], "strength": [d["bump"][x]["strength"] for x in "LR"],
                 "wedge_rate_cv": d["wedge_rate_cv"], "epg_hz": d["ring_group_hz"]["EPG"], "BUMP": d["BUMP"]} for c, d in rows.items()}
    OUT.write_text(json.dumps({"question": __doc__, "table": table, "conditions": rows}, indent=1))
    for c, t in table.items():
        print(f"{c:7s} entropy {t['entropy']:.3f} resultants {t['resultants'][0]:.2f} {t['resultants'][1]:.2f} "
              f"D {t['D']:.4f} wedge CV {t['wedge_rate_cv']:.2f} EPG {t['epg_hz']:.2f} Hz BUMP {t['BUMP']}")


if __name__ == "__main__":
    summary() if sys.argv[1] == "summary" else run(sys.argv[1])
