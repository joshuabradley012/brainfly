"""Exploratory, not pre-registered: why does rung 4's bump still favor one region after annealed homeostasis?

rung4_anneal.py (attempt 4, pre-registered) failed only on BUMP. After 120 rounds of the ring neurons' homeostasis,
annealed and averaged, its bump visits every heading (position entropy 0.92) but the runs still settle around one
region (resultants 0.64 and 0.71). The homeostasis moves each ring neuron toward its type's mean rate. If the bump
fires more strongly in some places than in others, it can linger longer where it is weak and still give every EPG the
same mean rate: equal rates need not mean equal time everywhere. This measures, wedge by wedge, how much time the bump
spends there, how strongly the EPGs fire while it is there, and the EPGs' mean rates.
Model: rung4_anneal.py's intact brain with its averaged offsets (rung4_anneal/intact_state.npz).
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9600), keeping each 1-s
window's EPG spikes. In each window the bump sits at the wedge nearest its population vector (as bump_motion places
it), and its strength there is the window's EPG spikes per EPG. Reported per wedge: the share of windows the bump spends
there, its mean strength there, and the wedge's EPGs' mean rate over the whole measurement; and the correlation of
occupancy with strength across wedges.
Ran: the bump is no weaker where it lingers. Its strength is 2.7-3.1 Hz wherever it sits, slightly higher at its
favored wedges (r = 0.40). Instead, the homeostasis never evened out the rates over long runs: the bump spends 2.5
times longer than average at wedges 11-13, and their EPGs fire 4.2 Hz against 2.1 elsewhere (wedge rates' CV 0.27;
occupancy against rate, r = 0.68). The homeostasis measured rates in 40-s runs from fresh starts, which this slow drift
barely shows in. On this seed the same brain scores position entropy 0.96 and resultants 0.42 and 0.61.

    python experiments/ring_landscape.py            (writes experiments/ring_landscape.json and ring_landscape.npz)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_insitu
import rung4_anneal as r4a

OUT = Path(__file__).with_suffix(".json")
SEED = 9600


def main() -> None:
    t0 = time.perf_counter()
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    z = np.load(r4a.HERE / "intact_state.npz")
    s.bias, st["extra"][:] = z["group_bias"].copy(), z["total"] / r4a.ANNEALED
    s.brain.set_bias(s.bias[s.gid])
    epg, side, glom = attempt1.epgs(s.types)
    from brainfly import imaging
    fc, rates, windows = attempt1.run(s.brain, imaging.region_weights(), epg, seed=SEED)
    np.savez_compressed(OUT.with_suffix(".npz"), windows=windows, epg_rates=rates[:, epg], side=side, glom=glom)
    wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
    prof = np.stack([windows[..., wedge == k].mean(-1) for k in range(16)], -1)          # runs x windows x 16
    z = prof @ np.exp(2j * np.pi * np.arange(16) / 16)
    seen = prof.sum(-1) > 0
    at = np.round(np.angle(z) / (2 * np.pi / 16)).astype(int) % 16
    strength = windows.sum(-1) / len(epg)                                                  # spikes per EPG per window
    occupancy = np.bincount(at[seen], minlength=16) / seen.sum()
    strength_at = np.array([strength[seen & (at == k)].mean() if (seen & (at == k)).any() else np.nan for k in range(16)])
    rate = rates[:, epg].mean(0)
    wedge_rate = np.array([rate[wedge == k].mean() for k in range(16)])
    ok = np.isfinite(strength_at)
    out = {"question": __doc__, "seed": SEED,
           "bump": attempt1.bump(windows, side, glom, np.random.default_rng(7)),
           "bump_motion": attempt1.bump_motion(windows, side, glom),
           "occupancy": np.round(occupancy, 3).tolist(), "strength_at_hz": np.round(strength_at, 2).tolist(),
           "wedge_mean_rate_hz": np.round(wedge_rate, 2).tolist(),
           "wedge_rate_cv": round(float(wedge_rate.std() / wedge_rate.mean()), 3),
           "occupancy_vs_strength_r": round(float(np.corrcoef(occupancy[ok], strength_at[ok])[0, 1]), 3),
           "occupancy_vs_rate_r": round(float(np.corrcoef(occupancy, wedge_rate)[0, 1]), 3),
           "epgs_per_wedge": np.bincount(wedge, minlength=16).tolist(),
           "seconds": round(time.perf_counter() - t0)}
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "bump")}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
