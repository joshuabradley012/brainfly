"""Exploratory, not pre-registered: does each ring neuron's own homeostasis free ring_fit2.py's bump from
its favored place?

ring_fit2.py's ring has a fly-like bump (112 deg wide, strength 0.67, EPGs at 1.9 Hz), but
ring_heldout.py found it spending about 40% of its time near wedges 1-2, so over 300-s runs each run's
mean position lands there and rung 4's resultant fails (0.58-0.93). Evening out each wedge's EPG output
made that worse, so the pull comes from the ring's wiring beyond EPG counts. Renart, Song & Wang (2003)
removed such pulls in a bump attractor by homeostasis in each neuron: a neuron that fires more than its
set point, because the bump sits on it too often, lowers its own excitability. ring_calibrated.py
couldn't do this for ring_er.py's bistable ring, but ring_fit2.py's forms a bump in every run. Here every
neuron of the ring's six types (EPG, EPGt, PEN_a, PEN_b, PEG, Delta7) gets its own bias on top of the
fitted ones, moved each round by k ln((target + 0.5) / (rate + 0.5)) mV, at most k, the target being
its type's mean rate in ring_fit2.py's run (so each type's mean stays put and only the spread
changes); ER and ExR keep theirs. 30 rounds of 16 fresh runs of 20 s (1 s settle), k = 1 mV for 15
rounds and 0.5 after, on seeds 100 onward. Then rung 4's BUMP and the position entropy on ring_heldout.py's
unseen seeds (2 to 5, 8 runs of 300 s).

    python experiments/ring_homeostasis.py            (writes experiments/ring_homeostasis.json)
    python experiments/ring_homeostasis.py --slow     (writes experiments/ring_homeostasis_slow.json)
--slow: that first run overshot (the bump moved from wedges 1-2 to 11-12), because each round's steps
were large next to how long the bump stays in one place. Renart et al.'s homeostasis is slow next to
the bump's dwell time, so --slow takes 80 rounds of 16 runs of 40 s, steps of at most 0.2 mV, and
moves each neuron by its rate averaged over rounds (each round's rate given a weight of 0.3).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_er
import ring_fit

OUT = Path(__file__).with_suffix(".json")
ROUNDS = [1.0] * 15 + [0.5] * 15
RUNS, SECONDS, HELDOUT = 16, 20, (2, 3, 4, 5)


def entropy_of(w: np.ndarray, wedge: np.ndarray) -> tuple[float, np.ndarray]:
    pw = np.stack([w[..., wedge == k].mean(-1) for k in range(16)], -1)
    seen = pw.sum(-1) > 0
    bins = np.round(np.angle((pw @ np.exp(2j * np.pi * np.arange(16) / 16))[seen]) / (2 * np.pi / 16)).astype(int) % 16
    hist = np.bincount(bins, minlength=16) / max(len(bins), 1)
    return float(-(hist[hist > 0] * np.log(hist[hist > 0])).sum() / np.log(16)), hist


def main() -> None:
    global ROUNDS, SECONDS, OUT
    slow = argparse.ArgumentParser()
    slow.add_argument("--slow", action="store_true")
    slow = slow.parse_args().slow
    ema = 1.0
    if slow:
        ROUNDS, SECONDS, ema = [0.2] * 80, 40, 0.3
        OUT = OUT.with_name("ring_homeostasis_slow.json")
    t0 = time.perf_counter()
    fit2 = json.loads(ring_fit.OUT.with_name("ring_fit2.json").read_text())["best"]
    p = fit2["params"]
    r = ring_fit.Ring(p, RUNS, seed=100)
    b = r.brain
    types = np.asarray(b.mcns_type)
    ring6 = np.isin(types, ring_er.RING)
    target_by_type = {"EPG": fit2["group_hz"]["EPG"], "EPGt": fit2["group_hz"]["EPG"], "PEN_a(PEN1)": fit2["group_hz"]["PEN_a"],
                      "PEN_b(PEN2)": fit2["group_hz"]["PEN_b"], "PEG": fit2["group_hz"]["PEG"], "Delta7": fit2["group_hz"]["Delta7"]}
    target = np.array([target_by_type.get(x, 0.0) for x in types])
    extra, log, smooth = np.zeros(b.n), [], None
    for k, step in enumerate(ROUNDS):
        b.reset(seed=100 + k)
        b.set_bias(r.bias + extra)
        b.advance(int(round(1.0 / b.dt)))
        c = [b.advance(int(round(1.0 / b.dt))) for _ in range(SECONDS)]
        rate = np.sum(c, 0).mean(0) / SECONDS
        smooth = rate if smooth is None else (1 - ema) * smooth + ema * rate
        w = np.stack([x[:, r.epg] for x in c], 1)
        extra = np.where(ring6, np.clip(extra + np.clip(step * np.log((target + 0.5) / (smooth + 0.5)), -step, step),
                                        attempt1.LOW, attempt1.HIGH), 0.0)
        h, _ = entropy_of(w, r.wedge)
        log.append({"round": k + 1, "position_entropy": round(h, 3), "epg_hz": round(float(rate[r.epg].mean()), 2),
                    "epg_rate_cv": round(float(rate[r.epg].std() / max(rate[r.epg].mean(), 1e-9)), 3),
                    "extra_bias_sd_mv": round(float(extra[ring6].std()), 2)})
        print(json.dumps(log[-1]), flush=True)
    out = {"question": __doc__, "log": log, "extra_bias_mv": {x: np.round(extra[types == x], 2).tolist() for x in target_by_type}, "heldout": []}
    for seed in HELDOUT:
        h = ring_fit.Ring(p, 8, seed=seed)
        hb = h.brain
        hb.set_bias(h.bias + extra)
        hb.advance(int(round(2.0 / hb.dt)))
        w, total = [], np.zeros((8, hb.n))
        for _ in range(300):
            c = hb.advance(int(round(1.0 / hb.dt)))
            w.append(c[:, h.epg])
            total += c
        w = np.stack(w, 1)
        bump = attempt1.bump(w, h.side, h.glom, np.random.default_rng(7))
        ok = all(bump[s]["strength"] >= attempt1.MIN_BUMP and bump[s]["strength"] > bump[s]["shuffle_p99"]
                 and bump[s]["resultant"] < attempt1.MAX_RESULTANT for s in "LR")
        ent, hist = entropy_of(w, h.wedge)
        rate = total / 300
        out["heldout"].append(row := {"seed": seed, "BUMP": bool(ok), "position_entropy": round(ent, 3), "position_histogram": np.round(hist, 3).tolist(),
                                      "bump": bump, "epg_hz": round(float(rate[:, h.epg].mean()), 2),
                                      "group_hz": {g: round(float(rate[:, m].mean()), 2) for g, m in h.groups.items()}})
        print(json.dumps({k: v for k, v in row.items() if k != "bump"}),
              {s: (v["strength"], v["shuffle_p99"], v["resultant"]) for s, v in bump.items()}, flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
