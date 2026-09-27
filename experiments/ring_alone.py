"""Exploratory, not pre-registered: does the connectome's head-direction ring hold a bump on its own?

rest_calibration2.py's resting brain has no head-direction bump: every EPG fires near its calibrated
2 Hz, and exempting the ring's excitatory types from depression changes nothing. This takes the 152
neurons of the ring's types (EPG, EPGt, PEN_a, PEN_b, PEG, Delta7) with their MaleCNS wiring (rung 1's
network, synapses divided by target size, w_syn 1.5556 mV), alone, with Poisson background (1 mV kicks
at 200 Hz) and a tonic bias of 0 or 5 mV, every excitatory synapse scaled by gE and every inhibitory
one by gI. 8 runs of 10 s each: the EPGs' mean and highest rates and rest_calibration.py's bump measures
(strength, the shuffle's 99th percentile, the runs' resultant; a real bump: strength about 0.7).

    python experiments/ring_alone.py            (writes experiments/ring_alone.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
from brainfly.hybrid import HybridBrain
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
RING = ["EPG", "EPGt", "PEN_a(PEN1)", "PEN_b(PEN2)", "PEG", "Delta7"]
TRIALS, SECONDS = 8, 10


def main() -> None:
    M, scale, labels, types, superclass = attempt1.network()
    ring = np.flatnonzero(np.isin(types, RING))
    Mr = M.tocsr()[ring][:, ring].tocsr()
    epg_all, side, glom = attempt1.epgs(types)
    at = {g: k for k, g in enumerate(ring)}
    epg = np.array([at[i] for i in epg_all])
    lab = {k: v[ring] for k, v in labels.items()}
    out = {"question": __doc__, "neurons": int(len(ring)), "sweep": []}
    for gE in (0.05, 0.1, 0.2, 0.35, 1.0, 2.0, 4.0, 8.0):
        for gI in (1.0, 4.0, 10.0):
            for bias in (0.0, 5.0):
                W = Mr.copy()
                W.data = np.where(W.data > 0, W.data * gE, W.data * gI)
                b = HybridBrain(trials=TRIALS, w_syn=W_SYN, matrix=W, scale=scale[ring], labels=lab, seed=1,
                                types={"all": {"noise_rate": 200.0, "noise_kick": 1.0, "bias": bias}})
                b.advance(int(round(1.0 / b.dt)))
                wins = np.stack([b.advance(int(round(1.0 / b.dt)))[:, epg] for _ in range(SECONDS)], 1)
                bump = attempt1.bump(wins, side, glom, np.random.default_rng(7))
                rate = wins.sum(1) / SECONDS
                row = {"gE": gE, "gI": gI, "bias_mv": bias, "epg_mean_hz": round(float(rate.mean()), 1),
                       "epg_max_hz": round(float(rate.max()), 1),
                       "bump": {s: {k: v[k] for k in ("strength", "shuffle_p99", "resultant")} for s, v in bump.items()}}
                out["sweep"].append(row)
                print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
