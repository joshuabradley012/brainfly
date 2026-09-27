"""Exploratory, not pre-registered: can the head-direction ring's bump be fitted without preferred places?

ring_fit.py's best ring passes rung 4's BUMP test, but ring_heldout.py found each run's bump sitting in one
of two places about 170 deg apart: the resultant clause passes because the two cancel. Flies' bumps show
no preferred positions (Noorman et al. 2024). MaleCNS wedges hold 2 to 4 EPGs each, so some excite
themselves more than others. This refits with two changes:
  - a pinning penalty in the score: the bump's position in every 1-s window of 16 spontaneous runs of 20
    s, binned over the 16 wedges; the entropy of that histogram over its maximum (1 when every wedge is
    visited equally) must reach 0.8. It replaces the resultant term. Seeded runs are scored at 8 positions
    (one run each), held within 45 deg after 6 s.
  - one more parameter, wedge normalization b in [0, 1]: every synapse from an EPG is multiplied by (the
    mean number of EPGs per wedge / the number in its wedge) to the power b, so at b = 1 every wedge's
    EPGs give the same total output. Synaptic scaling of this kind is how Renart, Song & Wang (2003)
    evened out a bump attractor's preferred places.
Otherwise as ring_fit.py (the same parameters and ranges, the other score terms, 12 candidates a
generation, 100 generations), starting from its best with wedge normalization at 0.25 and a step of 0.15.

    python experiments/ring_fit2.py            (writes experiments/ring_fit2.json)
"""
from __future__ import annotations

import json
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import ring_fit as fit

OUT = Path(__file__).with_suffix(".json")
fit.SPACE["wedge_norm"] = (0.0, 1.0, False, 0.25)
fit.NAMES = list(fit.SPACE)
RUNS, SPONT, FREE, POSITIONS = 16, 20, 6, tuple(range(0, 16, 2))
SIGMA0, MIN_ENTROPY = 0.15, 0.8


def evaluate(u: np.ndarray, detail: bool = False):
    fit.SPACE.setdefault("wedge_norm", (0.0, 1.0, False, 0.25))
    fit.NAMES = list(fit.SPACE)
    p = fit.decode(u)
    r = fit.Ring(p, RUNS, seed=1)
    b = r.brain
    b.advance(int(round(1.0 / b.dt)))
    w, total = [], np.zeros((RUNS, b.n))
    for _ in range(SPONT):
        c = b.advance(int(round(1.0 / b.dt)))
        w.append(c[:, r.epg])
        total += c
    w = np.stack(w, 1)
    rate = total / SPONT
    group_hz = {g: float(rate[:, m].mean()) for g, m in r.groups.items()}
    epg_hz = float(rate[:, r.epg].mean())
    per_run = fit.strengths(w, r.side, r.glom)
    rng = np.random.default_rng(7)
    shuffles = []
    for _ in range(200):
        lab = r.glom.copy()
        for s in "LR":
            mine = np.flatnonzero(r.side == s)
            lab[mine] = rng.permutation(lab[mine])
        shuffles.append(fit.strengths(w, r.side, r.glom, lab).mean(0))
    p99 = np.percentile(np.array(shuffles), 99, axis=0)
    strength = per_run.mean(0)
    prof = np.stack([w[..., r.wedge == k].mean(-1) for k in range(16)], -1)          # runs x windows x 16
    z = prof @ np.exp(2j * np.pi * np.arange(16) / 16)
    seen = prof.sum(-1) > 0
    bins = np.round(np.angle(z[seen]) / (2 * np.pi / 16)).astype(int) % 16
    hist = np.bincount(bins, minlength=16) / max(len(bins), 1)
    entropy = float(-(hist[hist > 0] * np.log(hist[hist > 0])).sum() / np.log(16))
    phase8 = np.exp(2j * np.pi * np.arange(8) / 8)
    resultant = []
    for s in "LR":
        mine = np.flatnonzero(r.side == s)
        per = np.stack([w[..., mine[r.glom[mine] == g + 1]].sum(-1) for g in range(8)], -1)
        resultant.append(float(np.abs(np.exp(1j * np.angle((per @ phase8).sum(1))).mean())))
    flat = prof.reshape(-1, 16)
    flat = flat[flat.max(1) > 0]
    if len(flat):
        aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in flat]).mean(0)
        fwhm, busiest = 22.5 * float((aligned >= aligned.max() / 2).sum()), float(flat.max(1).mean())
    else:
        fwhm, busiest = 360.0, 0.0
    held = []
    for k, start in enumerate(POSITIONS):
        s = fit.Ring(p, 1, seed=10 + k)
        bb = s.brain
        bb.advance(int(round(1.0 / bb.dt)))
        kick = s.bias.copy()
        kick[s.epg[np.isin(s.wedge, [(start + d) % 16 for d in (-1, 0, 1)])]] += 10.0
        bb.set_bias(kick)
        bb.advance(int(round(0.3 / bb.dt)))
        bb.set_bias(s.bias)
        bb.advance(int(round((FREE - 1) / bb.dt)))
        c = bb.advance(int(round(1.0 / bb.dt)))[:, s.epg]
        zz = np.stack([c[:, s.wedge == q].mean(-1) for q in range(16)], -1) @ np.exp(2j * np.pi * np.arange(16) / 16)
        held += (np.degrees(np.abs(np.angle(zz * np.exp(-2j * np.pi * start / 16)))) < 45).tolist()
    band = fit.band
    score = (4 * float(np.maximum(0, 0.5 - per_run).mean()) + 2 * float(np.maximum(0, p99 + 0.05 - strength).sum())
             + ((fwhm - 100) / 45) ** 2 + 8 * max(0.0, MIN_ENTROPY - entropy) + 2 * (1 - float(np.mean(held)))
             + 4 * band(epg_hz, 0.5, 2) + band(busiest, 1e-3, 20) + band(group_hz["PEN_a"], 2, 6) + 0.5 * band(group_hz["ER"], 2.5, 8)
             + 0.5 * sum(band(group_hz[g], 0.5, 20) for g in ("PEN_b", "PEG", "Delta7")) + 0.25 * band(group_hz["ExR"], 0.5, 20)
             + (10.0 if max(group_hz.values()) > 100 else 0.0))
    if not detail:
        return float(score)
    return {"score": round(float(score), 3), "params": {k: round(v, 4) for k, v in p.items()},
            "strength": np.round(strength, 3).tolist(), "shuffle_p99": np.round(p99, 3).tolist(),
            "weakest_run": np.round(per_run.min(0), 3).tolist(), "position_entropy": round(entropy, 3),
            "position_histogram": np.round(hist, 3).tolist(), "resultant": np.round(resultant, 3).tolist(),
            "fwhm_deg": fwhm, "busiest_wedge_hz": round(busiest, 1), "epg_hz": round(epg_hz, 2),
            "group_hz": {g: round(v, 2) for g, v in group_hz.items()}, "held": f"{int(np.sum(held))}/{len(held)}"}


def main() -> None:
    t0 = time.perf_counter()
    start = json.loads(fit.OUT.read_text())["best"]["params"] | {"wedge_norm": 0.25}
    x0 = fit.encode(start)
    out = {"question": __doc__, "start": evaluate(x0, detail=True), "log": []}
    print("start:", json.dumps(out["start"]), flush=True)

    def log(row):
        out["log"].append(row)
        print(json.dumps(row), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    with Pool(fit.LAMBDA, initializer=fit._init) as pool:
        (score, x), mean = fit.cma_es(evaluate, x0, SIGMA0, fit.LAMBDA, fit.GENERATIONS, pool, log)
    out["best"] = evaluate(x, detail=True)
    out["mean"] = evaluate(mean, detail=True)
    out["seconds"] = round(time.perf_counter() - t0)
    print("best:", json.dumps(out["best"]), "\nmean:", json.dumps(out["mean"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
