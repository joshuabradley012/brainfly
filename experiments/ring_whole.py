"""Exploratory, not pre-registered: does the fitted head-direction ring keep its bump inside the whole resting
brain?

ring_fit.py (and ring_fit2.py, which also penalizes preferred places) fitted the ring's class gains,
slow current, depression and group biases in its 460-neuron sub-network, where ring neurons get only the
background. Here those settings go into escape_at_rest2.py's resting brain (which passed): the class
gains on every synapse between two of the 460 neurons, the excitatory ring edges through the slow
current, the depression on the ring's excitatory outputs. The ring can't be calibrated the way the rest
of the brain is (ring_calibrated.py: it's bistable), so its groups keep the fitted biases, each less
the mean input its neurons get from outside the ring at rest (each input's resting rate times its
weight, its depression's steady efficacy at that rate and the 5 ms synaptic time constant), and are
left out of the calibration. Procedure: the eyes-open start (escape_at_rest2.py's biases), the ring's
biases uncorrected, 8 fresh-start rounds of the usual calibration (k = 1 mV, then 0.5) for everything
else; then the correction from a 2-s resting run, and 4 more rounds (k = 0.5). Measured: rung 4's BUMP
over 8 runs of 60 s at grey (strength per bridge side, 1,000 shuffles, the resultant), the bump's
position entropy over the 16 wedges (as ring_fit2.py), width, the busiest wedge, the ring's group
rates, and the brain's own mean rate and neurons over 100 Hz.

    python experiments/ring_whole.py --fit ring_fit      (or ring_fit2; writes experiments/ring_whole/<fit>.json)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import escape_at_rest as escape
import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
import ring_er
from brainfly.hybrid import TAU
from shiu_rewiring import W_SYN

HERE = Path(__file__).with_suffix("")
PEN = ["PEN_a(PEN1)", "PEN_b(PEN2)"]
SECONDS = 60


def ring_members(types: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    er = np.char.startswith(types, "ER") & np.array([t[2:3].isdigit() for t in types]) | np.char.startswith(types, "ExR")
    return np.isin(types, ring_er.RING) | er, er


def subnetwork(p: dict):
    """eyes_at_rest.SUBNETWORK for the fitted ring: class gains inside the ring, its slow edges split off."""
    def apply(M, types, superclass):
        ring, er = ring_members(types)
        M = M.tocoo()
        pre, post = M.col, M.row
        inside = ring[pre] & ring[post]
        tp, tq = types[pre], types[post]
        ring_exc = np.isin(types, ring_er.EXC)
        g = np.where(M.data > 0, p["gE"], p["gI"])
        g = g * np.where(((tp == "EPG") & np.isin(tq, PEN)) | (np.isin(tp, PEN) & (tq == "EPG")), p["loop"], 1.0)
        g = g * np.where((tp == "EPG") & (tq == "EPG"), p["epg_epg"], 1.0)
        g = g * np.where(tp == "Delta7", p["delta7"], 1.0)
        g = g * np.where(ring_exc[pre] & er[post], p["to_er"], 1.0)
        g = g * np.where(er[pre] & ~er[post], p["from_er"], 1.0)
        g = g * np.where(er[pre] & er[post], p["er_er"], 1.0)
        if p.get("wedge_norm", 0.0):
            epg, side, glom = attempt1.epgs(types)
            wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
            n_w = np.bincount(wedge, minlength=16)
            f = np.ones(len(types))
            f[epg] = (n_w.mean() / n_w[wedge]) ** p["wedge_norm"]
            g = g * f[pre]
        data = np.where(inside, M.data * g, M.data)
        slow_edge = inside & ring_exc[pre] & np.isin(tq, ring_er.RING) & (data > 0)
        slow = sparse.csr_matrix((data[slow_edge] * TAU / p["slow_tau"], (post[slow_edge], pre[slow_edge])), shape=M.shape)
        fast = sparse.csr_matrix((np.where(slow_edge, 0.0, data), (post, pre)), shape=M.shape)
        fast.eliminate_zeros()
        return fast, slow, p["slow_tau"]
    return apply


def model_with_ring(p: dict):
    def model(types, superclass):
        spec, sets = escape.model(types, superclass)
        for t in ring_er.EXC:
            spec[t] = {"depression": p["dep_f"], "recovery": p["dep_tau"]}
        return spec, sets
    return model


def group_of(types: np.ndarray) -> dict:
    ring, er = ring_members(types)
    return {"EPG": np.isin(types, ["EPG", "EPGt"]), "PEN_a": types == "PEN_a(PEN1)", "PEN_b": types == "PEN_b(PEN2)",
            "PEG": types == "PEG", "Delta7": types == "Delta7", "ER": er & ~np.char.startswith(types, "ExR"),
            "ExR": np.char.startswith(types, "ExR")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", default="ring_fit")
    fit_name = ap.parse_args().fit
    t0 = time.perf_counter()
    p = json.loads((Path(__file__).with_name(f"{fit_name}.json")).read_text())["best"]["params"]
    attempt2.model, attempt1.network = model_with_ring(p), escape2.network
    eyes.SUBNETWORK = subnetwork(p)
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(escape2.HERE / "intact.npz")["bias"]
    b, types = s.brain, s.types
    ring, _ = ring_members(types)
    groups = group_of(types)
    ring_groups = np.unique(s.gid[ring])
    fitted = np.zeros(b.n)
    for g, m in groups.items():
        fitted[m] = p[f"b_{g}"]
    for k in ring_groups:
        s.bias[k] = fitted[s.gid == k].mean()
    s.fixed |= ring
    eyes.ROUNDS = [1.0] * 4 + [0.5] * 4
    log = s.calibrate()

    # the ring's correction: mean input from outside the ring at rest
    b.reset(3)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    efficacy = 1.0 / (1.0 + (1.0 - f) * rate * tau)
    M = eyes.SUBNETWORK(escape2.network()[0], types, np.asarray(b.superclass))[0].tocsr()
    outside = np.where(ring, 0.0, rate * efficacy)
    ext = (M @ outside) * b.scale * W_SYN * TAU                       # mV of mean depolarization per neuron
    for k in ring_groups:
        s.bias[k] = fitted[s.gid == k].mean() - ext[s.gid == k].mean()
    eyes.ROUNDS = [0.5] * 4
    log += s.calibrate()

    # measure
    b.reset(11)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(2.0 / b.dt)))
    epg, side, glom = attempt1.epgs(types)
    w, total = [], np.zeros((eyes.TRIALS, b.n))
    for _ in range(SECONDS):
        c = b.advance(int(round(1.0 / b.dt)))
        w.append(c[:, epg])
        total += c
    w = np.stack(w, 1)
    rate = total / SECONDS
    bump = attempt1.bump(w, side, glom, np.random.default_rng(7))
    wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
    prof = np.stack([w[..., wedge == k].mean(-1) for k in range(16)], -1)
    z = prof @ np.exp(2j * np.pi * np.arange(16) / 16)
    seen = prof.sum(-1) > 0
    hist = np.bincount(np.round(np.angle(z[seen]) / (2 * np.pi / 16)).astype(int) % 16, minlength=16) / max(int(seen.sum()), 1)
    entropy = float(-(hist[hist > 0] * np.log(hist[hist > 0])).sum() / np.log(16))
    flat = prof.reshape(-1, 16)
    flat = flat[flat.max(1) > 0]
    aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in flat]).mean(0) if len(flat) else np.zeros(16)
    ok = all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
             and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR")
    out = {"question": __doc__, "fit": fit_name, "params": p, "calibration": log[-1], "BUMP": bool(ok), "bump": bump,
           "position_entropy": round(entropy, 3), "position_histogram": np.round(hist, 3).tolist(),
           "fwhm_deg": 22.5 * float((aligned >= aligned.max() / 2).sum()) if len(flat) else None,
           "busiest_wedge_hz": round(float(flat.max(1).mean()), 1) if len(flat) else 0.0, "epg_hz": round(float(rate[:, epg].mean()), 2),
           "ring_group_hz": {g: round(float(rate[:, m].mean()), 2) for g, m in groups.items()},
           "outside_input_mv": {g: round(float(ext[m].mean()), 2) for g, m in groups.items()},
           "own_mean_hz": round(float(rate[:, ~s.fixed].mean()), 3), "own_over_100hz": int((rate[:, ~s.fixed].mean(0) > 100).sum()),
           "seconds": round(time.perf_counter() - t0)}
    HERE.mkdir(exist_ok=True)
    (HERE / f"{fit_name}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "params")}), flush=True)


if __name__ == "__main__":
    main()
