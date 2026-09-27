"""Exploratory, not pre-registered: can the ring's bump be fitted to hold still like a fly's?

ring_fit2.py's ring has a fly-shaped bump (112 deg, strength 0.67, EPGs 1.9 Hz), and ring_homeostasis.py's
slow homeostasis frees it from favored places. But ring_drift.py found it diffusing at D = 0.11-0.16
rad^2/s, against flies' 0.003-0.04 in darkness, and ring_fit2.py's hold test (within 45 deg after 6 s)
was too loose to see that. Drift from spontaneous runs can't be the target, because a pinned bump drifts
least. So this scores seeded stability: the bump seeded (as ring_er.py) at 8 positions 45 deg apart, 2
runs each, and its angular distance from the seed averaged over the last 5 of 10 s free, whose root mean
square must be at most 30 deg (a fly's bump at D = 0.014 rad^2/s moves about that far in 10 s). That
penalizes both diffusion and sliding to a favored place. The other terms are ring_fit2.py's, with the
pinning term's weight halved (slow homeostasis handles the rest), and the ranges widened where
ring_fit2.py ended at a bound: EPG to EPG down to 0.05, ring-type cells onto ER and ExR up to 8, the slow
current up to 0.5 s (NMDA currents in fly neurons decay over 100 ms or more), the strength left per spike
down to 0.7. Starting from ring_fit2.py's best, step 0.12, 12 candidates a generation, 80 generations.

    python experiments/ring_fit3.py            (writes experiments/ring_fit3.json)
"""
from __future__ import annotations

import json
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import ring_fit as fit
import ring_fit2 as fit2

OUT = Path(__file__).with_suffix(".json")
fit.SPACE.update({"epg_epg": (0.05, 4, True, 1.0), "to_er": (0.25, 8, True, 1.0), "slow_tau": (0.03, 0.5, True, 0.1),
                  "dep_f": (0.7, 0.98, False, 0.9), "wedge_norm": (0.0, 1.0, False, 0.25)})
fit.NAMES = list(fit.SPACE)
SEEDS, SEEDED_RUNS, FREE, MAX_RMS = tuple(range(0, 16, 2)), 2, 10, 30.0
SIGMA0, GENERATIONS = 0.12, 80


def evaluate(u: np.ndarray, detail: bool = False):
    fit.SPACE.update({"epg_epg": (0.05, 4, True, 1.0), "to_er": (0.25, 8, True, 1.0), "slow_tau": (0.03, 0.5, True, 0.1),
                      "dep_f": (0.7, 0.98, False, 0.9), "wedge_norm": (0.0, 1.0, False, 0.25)})
    fit.NAMES = list(fit.SPACE)
    base = fit2.evaluate(u, detail=True)                       # ring_fit2.py's terms (its seeded test included)
    p = fit.decode(u)
    dist = []
    for k, start in enumerate(SEEDS):
        s = fit.Ring(p, SEEDED_RUNS, seed=30 + k)
        bb = s.brain
        bb.advance(int(round(1.0 / bb.dt)))
        kick = s.bias.copy()
        kick[s.epg[np.isin(s.wedge, [(start + d) % 16 for d in (-1, 0, 1)])]] += 10.0
        bb.set_bias(kick)
        bb.advance(int(round(0.3 / bb.dt)))
        bb.set_bias(s.bias)
        bb.advance(int(round((FREE - 5) / bb.dt)))
        for _ in range(5):
            c = bb.advance(int(round(1.0 / bb.dt)))[:, s.epg]
            z = np.stack([c[:, s.wedge == q].mean(-1) for q in range(16)], -1) @ np.exp(2j * np.pi * np.arange(16) / 16)
            dist += np.degrees(np.abs(np.angle(z * np.exp(-2j * np.pi * start / 16)))).tolist()
    rms = float(np.sqrt(np.mean(np.square(dist))))
    g = base["group_hz"]
    band = fit.band
    score = (4 * max(0.0, 0.5 - min(base["weakest_run"])) + 2 * sum(max(0.0, q + 0.05 - s) for q, s in zip(base["shuffle_p99"], base["strength"]))
             + ((base["fwhm_deg"] - 100) / 45) ** 2 + 4 * max(0.0, fit2.MIN_ENTROPY - base["position_entropy"])
             + 4 * max(0.0, rms / MAX_RMS - 1) ** 2 * 4 + 4 * band(base["epg_hz"], 0.5, 2) + band(base["busiest_wedge_hz"], 1e-3, 20)
             + band(g["PEN_a"], 2, 6) + 0.5 * band(g["ER"], 2.5, 8) + 0.5 * sum(band(g[x], 0.5, 20) for x in ("PEN_b", "PEG", "Delta7"))
             + 0.25 * band(g["ExR"], 0.5, 20) + (10.0 if max(g.values()) > 100 else 0.0))
    if not detail:
        return float(score)
    return base | {"score": round(float(score), 3), "seeded_rms_deg": round(rms, 1)}


def main() -> None:
    t0 = time.perf_counter()
    start = json.loads(fit.OUT.with_name("ring_fit2.json").read_text())["best"]["params"]
    x0 = fit.encode(start)
    out = {"question": __doc__, "start": evaluate(x0, detail=True), "log": []}
    print("start:", json.dumps(out["start"]), flush=True)

    def log(row):
        out["log"].append(row)
        print(json.dumps(row), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    with Pool(fit.LAMBDA, initializer=fit._init) as pool:
        (score, x), mean = fit.cma_es(evaluate, x0, SIGMA0, fit.LAMBDA, GENERATIONS, pool, log)
    out["best"] = evaluate(x, detail=True)
    out["mean"] = evaluate(mean, detail=True)
    out["seconds"] = round(time.perf_counter() - t0)
    print("best:", json.dumps(out["best"]), "\nmean:", json.dumps(out["mean"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
