"""Exploratory, not pre-registered: does homeostasis that measures rates over long runs even out the bump's long-run
landscape?

rung4_anneal.py (attempt 4, pre-registered) failed only on BUMP: its bump visits every heading, but runs still settle
around one region (resultants 0.64 and 0.71). ring_landscape.py found why. Over rung 4's 300-s runs, the bump spends
2.5 times longer than average at its favored wedges, and their EPGs fire twice as fast as elsewhere (4.2 against
2.1 Hz). So the homeostasis never equalized their rates over long runs. It measures rates in 40-s runs from fresh
starts, where where the bump starts matters more than where it slowly drifts to. Here the homeostasis measures rates
in runs as long as the test's.
Model: rung4_anneal.py's intact brain with its averaged offsets (rung4_anneal/intact_state.npz).
Procedure: 10 rounds, each 8 fresh runs of 300 s after 2 s (round k from seed 9800 + k). Every ring neuron's offset
moves by 0.2 ln((target + 0.5) / (rate + 0.5)) mV, at most 0.2 mV, toward its type's rate in ring_fit3.py's fit,
on its rate over that round (as ring_insitu.homeostasis, without the smoothing over rounds).
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9900) as rung4_rest.py scores
it, with the final offsets; and each round's bump measures and the spread of its wedges' EPG rates.
Ran: no, it pinned the bump. After the first round (position entropy 0.91, wedge rates' CV 0.34), each round's runs
settled more and more on one region. From round 5 the entropy was 0.39-0.56 and the wedge rates' CV about 1. In the
final measurement every run holds the bump within about 10 degrees of one heading (resultants 0.998), the position
entropy is 0.37, and the bump barely drifts (D = 0.002 rad^2/s, under flies' range). With rates from long runs, full
0.2 mV steps and no smoothing over rounds, wherever the bump settled, the next round's corrections deepened the pin
rather than removing it. RATE holds (1.66 Hz).

With `gentle`, the steps are a quarter the size (0.05 mV) and each neuron's rate is smoothed over rounds (each new
round weighted 0.3, as ring_insitu.homeostasis), against the windup that pinned the bump (writes ring_longruns_gentle).

    python experiments/ring_longruns.py            (writes experiments/ring_longruns.json; resumes after an interruption)
    python experiments/ring_longruns.py gentle     (writes experiments/ring_longruns_gentle.json; resumes likewise)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_insitu
import rung4_anneal as r4a
import rung4_rest as r4

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
ROUNDS, SEED, MEASURE = 10, 9800, 9900
STEP, EMA = 0.2, 1.0                                   # mV; the weight of each new round in a neuron's smoothed rate
if sys.argv[1:] == ["gentle"]:
    OUT, HERE, STEP, EMA, SEED, MEASURE = OUT.with_name("ring_longruns_gentle.json"), HERE.with_name("ring_longruns_gentle"), 0.05, 0.3, 9820, 9920


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    b, types, ring, groups = s.brain, s.types, st["ring"], st["groups"]
    start = np.load(r4a.HERE / "intact_state.npz")
    s.bias = start["group_bias"].copy()
    state = HERE / "state.npz"
    if state.exists():
        z = np.load(state)
        st["extra"][:], first, trace = z["extra"], int(z["rounds"]), json.loads(str(z["trace"]))
        print("resuming after round", first, flush=True)
    else:
        st["extra"][:], first, trace = start["total"] / r4a.ANNEALED, 0, []
    target = np.zeros(b.n)
    for g, hz in st["fit"]["group_hz"].items():
        if g in groups and g not in ("ER", "ExR"):
            target[groups[g]] = hz
    tune = ring & (target > 0)
    epg, side, glom = attempt1.epgs(types)
    wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
    from brainfly import imaging
    weights = imaging.region_weights()
    smooth = np.load(state)["smooth"] if state.exists() and "smooth" in np.load(state) else None
    for k in range(first, ROUNDS):
        b.set_bias(s.bias[s.gid])
        _, rates, windows = attempt1.run(b, weights, epg, seed=SEED + k)
        rate = rates.mean(0)
        smooth = rate if smooth is None else (1 - EMA) * smooth + EMA * rate
        st["extra"][:] = np.where(tune, st["extra"] + np.clip(STEP * np.log((target + 0.5) / (smooth + 0.5)), -STEP, STEP), st["extra"])
        m = attempt1.bump_motion(windows, side, glom)
        wedge_rate = np.array([rate[epg][wedge == w].mean() for w in range(16)])
        trace.append({"round": k + 1, "position_entropy": m["position_entropy"], "drift_D": m["drift_D_rad2_per_s"],
                      "epg_hz": round(float(rate[epg].mean()), 2), "wedge_rate_cv": round(float(wedge_rate.std() / wedge_rate.mean()), 3)})
        print(json.dumps(trace[-1]), flush=True)
        np.savez(state, extra=st["extra"], rounds=k + 1, trace=json.dumps(trace), smooth=smooth)
    b.set_bias(s.bias[s.gid])
    out = {"question": __doc__, "rounds": trace, "measured": r4.rest(s, st, MEASURE), "seconds": round(time.perf_counter() - t0)}
    m = out["measured"]
    print(json.dumps({k: m[k] for k in ("RATE", "BUMP", "mean_hz", "bump")}),
          json.dumps({k: v for k, v in m["bump_motion"].items() if k != "position_histogram"}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
