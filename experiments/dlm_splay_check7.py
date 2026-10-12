"""Exploratory check, written after review 11 and before it runs, not pre-registered and not a change to the model: the
leaky-integrator units of dlm_splay_check6.py with MN5 running at flies' median and maximum rate ratio.

dlm_splay_check6.py set all five units to one rate. There MN5's pairs came within 10 ms of their partners more often than
flies' (0.59-0.64 against 0.34-0.58 times chance), and MN4-MN5's dip10 was 0.110 (flies 0.016-0.097). In flies MN5 fires
at 0.98-1.26 times MN1-4's rate (median 1.10; Hürkey et al.'s Fig. 1b, 8 flies), and review 11's exploratory reruns found
MN5's pairs inside flies' ranges with MN5 at about 1.2 times.
Model: dlm_splay_check6.py's "LIF, MN5 assumed" (flies' 20 ms coupling, MN5's junctions at the assumed CC 0.0075, private
kicks calibrated for CV 0.22), each unit with its own drive, with MN1-4 targeted at 6.3 Hz and MN5 at 1.10 or 1.26 times
that (6.93 and 7.94 Hz; flies' per-fly means are 4.5-8 Hz). The drives are found by bisection, all five at once, in two
passes: the second re-brackets each unit at its first-pass drive plus or minus 0.05 mV. Each unit's calibration rate
must end within 2% of its target, or the condition is reported as failing calibration.
Measured as dlm_splay_check6.py measures (8 runs of 300 s after 3 s, seeds 4800 + 10 x condition), with each unit's
rate and CV, and the ten pairs against flies'.

Ran (2026-10-11, 42 s): MN5's pairs come inside flies' ranges at flies' maximum rate ratio, not at the median. Both
conditions calibrated within 2% (MN1-4 at 6.29-6.32 Hz, MN5 at 6.93 and 7.93).
- MN5 at 1.10 times (main runs 6.24-6.35 and 7.00 Hz):
  - splayness 0.735, preferred orders 54%, 30% of windows with a repeat;
  - MN5's pairs: r 0.59, dip10 0.10-0.11 (MN4-MN5 0.108; flies 0.016-0.097), within 10 ms 0.60-0.64 times chance
    (flies 0.34-0.58). Still outside.
- MN5 at 1.26 times (6.27-6.33 and 7.95 Hz):
  - splayness 0.732, preferred orders 54%, 30% with a repeat;
  - MN5's pairs: r 0.59-0.60, dip10 0.088-0.093 (MN4-MN5 0.088), within 10 ms 0.44-0.48 times chance. Inside flies'
    ranges.
- In both, the weakly coupled MN1-4 pairs are as in dlm_splay_check6.py (dip10 0.09-0.10, within 10 ms 0.50-0.59 times
  chance; flies 0.03-0.06 and 0.16-0.31). The strong pairs keep flies' r (0.33-0.35) but come within 10 ms of each
  other more often than in check 6 (0.35-0.40 times chance; check 6 0.23 at 6.6 Hz; flies 0.05 and 0.20).
So with MN5 at the top of flies' rate range its pairs fit flies'. At flies' median ratio they don't, so it is a
boundary result. The weakly coupled pairs' shortfall doesn't depend on MN5's rate.

    python experiments/dlm_splay_check7.py      (writes experiments/dlm_splay_check7.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6

OUT = Path(__file__).with_suffix(".json")
SEED = 4800
BASE_HZ = 6.3
RATIOS = (1.10, 1.26)


def biases_for(targets: np.ndarray, rates_for, start: np.ndarray, half_range: float, iterations: int = 22) -> np.ndarray:
    lo, hi = start - half_range, start + half_range
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        r = rates_for(mid)
        lo, hi = np.where(r < targets, mid, lo), np.where(r < targets, hi, mid)
    return 0.5 * (lo + hi)


def main() -> None:
    t0 = time.perf_counter()
    d2 = json.loads(Path(c1.OUT).with_name("dlm_splay_check2.json").read_text())
    d6 = json.loads(Path(c6.OUT).read_text())
    lif_hz = d2["calibration"]["chosen"]["kick_hz"]
    coupling, gap = c6.junctions(d6["ratios"]["assumed_mn5"], c5.CC, False)
    start = np.array(d6["conditions"]["LIF, MN5 assumed"]["unit_biases_mv"])
    rates_for = lambda bb: np.array([np.mean([len(r[i]) / 60.0 for r in c6.lif_runs(bb, lif_hz, coupling, gap, 60.0, c1.SEED - 1)])
                                     for i in range(c1.N)])
    out = {"question": __doc__, "flies_pairs": c6.FLIES_PAIRS, "conditions": {}}
    for c, ratio in enumerate(RATIOS):
        targets = np.array([BASE_HZ] * 4 + [BASE_HZ * ratio])
        first = biases_for(targets, rates_for, start, 3.0)
        biases = biases_for(targets, rates_for, first, 0.05)
        cal = rates_for(biases)
        calibrated = bool(np.all(np.abs(cal / targets - 1) <= 0.02))
        runs = c6.lif_runs(biases, lif_hz, coupling, gap, c1.SECONDS, SEED + 10 * c)
        res = c6.summarize(runs)
        res.update({"targets_hz": [round(float(x), 3) for x in targets], "calibration_rates_hz": [round(float(x), 3) for x in cal],
                    "calibrated_within_2pct": calibrated, "unit_biases_mv": [round(float(x), 5) for x in biases]})
        name = f"LIF, MN5 at {ratio:.2f} x MN1-4"
        out["conditions"][name] = res
        s = res["summary"]
        print(name, json.dumps({"calibrated": calibrated, "cal": res["calibration_rates_hz"], "rates": res["unit_rates_hz"],
                                "splayness": s["splayness"][0], "preferred": s["preferred_order_share"][0],
                                "repeats": s["repeat_share"], "pairs": res["pairs"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
