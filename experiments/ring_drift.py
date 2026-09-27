"""Exploratory, not pre-registered: how fast does the fitted ring's bump drift, against flies' in darkness?

ring_homeostasis.py's slow homeostasis frees ring_fit2.py's bump from favored places (position entropy
0.96-0.97 on unseen seeds), and then rung 4's resultant passes on 2 of 4 seeds: a bump that crosses the
whole ring within a 300-s run leaves each run's mean position to chance. Whether that roaming is
fly-like depends on its speed. Flies' bumps in darkness diffuse with D of about 0.003-0.04 rad^2/s
(research_notes/Rung 4 resting state data/head_direction_models.md, derived from Seelig & Jayaraman 2015
and Noorman et al. 2024). Here, 8 runs of 120 s (seed 21, unseen by both fits), the bump's ellipsoid-body
angle in 0.5-s windows, unwrapped, and D from the mean squared displacement over lags of 0.5-20 s
(slope / 2), with and without the slow homeostasis's biases.

    python experiments/ring_drift.py                    (writes experiments/ring_drift.json)
    python experiments/ring_drift.py --fit ring_fit3    (ring_fit3.py's best and its slow homeostasis; writes
                                                         experiments/ring_drift_ring_fit3.json)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import ring_fit

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", default="ring_fit2")
    fit_name = ap.parse_args().fit
    suffix = "" if fit_name == "ring_fit2" else f"_{fit_name}"
    p = json.loads(ring_fit.OUT.with_name(f"{fit_name}.json").read_text())["best"]["params"]
    extra_by_type = json.loads(ring_fit.OUT.with_name(f"ring_homeostasis_slow{suffix}.json").read_text())["extra_bias_mv"]
    out = {"question": __doc__, "conditions": []}
    for label, homeostasis in ((f"{fit_name}.py's best", False), ("with ring_homeostasis.py --slow", True)):
        r = ring_fit.Ring(p, 8, seed=21)
        b = r.brain
        types = np.asarray(b.mcns_type)
        extra = np.zeros(b.n)
        if homeostasis:
            for t, vals in extra_by_type.items():
                extra[types == t] = vals
        b.set_bias(r.bias + extra)
        b.advance(int(round(2.0 / b.dt)))
        w = np.stack([b.advance(int(round(0.5 / b.dt)))[:, r.epg] for _ in range(240)], 1)
        pw = np.stack([w[..., r.wedge == k].mean(-1) for k in range(16)], -1)
        theta = np.unwrap(np.angle(pw @ np.exp(2j * np.pi * np.arange(16) / 16)), axis=1)
        lags = np.arange(1, 41)
        msd = np.array([np.mean((theta[:, k:] - theta[:, :-k]) ** 2) for k in lags])
        out["conditions"].append(row := {"condition": label, "D_rad2_per_s": round(float(np.polyfit(lags * 0.5, msd, 1)[0] / 2), 3),
                                         "rms_displacement_10s_deg": round(float(np.degrees(np.sqrt(msd[19]))), 1),
                                         "msd_rad2": np.round(msd, 3).tolist()})
        print(json.dumps({k: v for k, v in row.items() if k != "msd_rad2"}), flush=True)
    OUT.with_name(f"ring_drift{suffix}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
