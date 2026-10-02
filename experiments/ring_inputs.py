"""Exploratory analysis, not pre-registered: does the ring's input from outside explain where the bump lingers?

ring_loops.py found the bump's favored region (wedges 11-13) survives cutting the ring's loops through the rest of the
brain. What remains from outside is the ring's input. Its mean is corrected neuron by neuron (ring_insitu.tune), but
its fluctuations are not, and an EPG with more or busier outside partners gets noisier input. This computes, for each
EPG, the mean and a Poisson variance proxy (the sum of w^2 r) of its input from neurons outside the ring, with each
input's depression at its rate, from ring_insitu.py's resting rates (ring_insitu/measure.npz) and rung4_anneal.py's
brain. Averaged by wedge, each is correlated with ring_landscape.py's occupancy (where attempt 4's bump spends its time).
Ran: no. The correlations with occupancy are weak: r = 0.14 for the mean, 0.12 for the variance, 0.16 for the
excitatory part and 0.05 for the inhibitory part. The wedges differ in outside input (CV 0.16 for the mean, 0.25 for the
variance), but not in step with where the bump lingers.

    python experiments/ring_inputs.py            (writes experiments/ring_inputs.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import sparse

import rest_calibration as attempt1
import ring_insitu
import rung4_anneal as r4a

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).parent


def main() -> None:
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    b, ring = s.brain, st["ring"]
    rates = np.load(HERE / "ring_insitu" / "measure.npz")["rates"].mean(0)
    W = sparse.csc_matrix((b.weights, b.idx, b.ptr), shape=(b.n, b.n)).tocsr()       # rows postsynaptic
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    drive = np.where(ring, 0.0, rates / (1.0 + (1.0 - f) * rates * tau))              # outside neurons only
    inputs = {"mean": W @ drive, "variance": W.multiply(W) @ drive,
              "excitatory": W.maximum(0) @ drive, "inhibitory": -(W.minimum(0) @ drive)}
    epg, side, glom = attempt1.epgs(s.types)
    wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
    occupancy = np.array(json.loads((HERE / "ring_landscape.json").read_text())["occupancy"])
    out = {"question": __doc__, "occupancy": occupancy.tolist(), "by_wedge": {}}
    for name, x in inputs.items():
        v = np.array([x[epg][wedge == k].mean() for k in range(16)])
        out["by_wedge"][name] = {"values": np.round(v, 2).tolist(), "cv": round(float(v.std() / abs(v.mean())), 3),
                                 "r_with_occupancy": round(float(np.corrcoef(v, occupancy)[0, 1]), 3)}
        print(name, out["by_wedge"][name]["r_with_occupancy"], out["by_wedge"][name]["cv"], flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
