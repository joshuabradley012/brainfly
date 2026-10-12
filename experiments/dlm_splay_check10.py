"""Exploratory check, written after review 12 and before it runs, not pre-registered and not a change to the model:
dlm_splay_check7.py with each unit's irregularity set for its own rate.

dlm_splay_check7.py ran MN5 at 1.10 and 1.26 times MN1-4's 6.3 Hz, with every unit's kicks as dlm_splay_check2.py set
them for a CV of 0.22 at 6.6 Hz. Review 12 found that this changed MN5's regularity along with its rate. In the main runs
MN5's CV was 0.158 at 1.26 times and 0.225 at 1.10, against MN1-4's 0.25-0.26. So the fit at 1.26 times came with MN5
far more regular than the others, which flies don't show: their five fire "with similar variance in the ISI (CV 0.22 ±
0.07 for each MN)" (research_notes/Rung 8 flight data/dlm_splay_state.md, section 1.2).
Model: dlm_splay_check7.py's (dlm_splay_check6.py's "LIF, MN5 assumed": the leaky integrator, flies' coupling as 20 ms
peak ratios, MN5's junctions at the assumed CC 0.0075, no spikelets), MN1-4 targeted at 6.3 Hz and MN5 at 1.0, 1.10 or
1.26 times that (6.3, 6.93 and 7.938 Hz). Each unit's kicks (0.1 mV) are set as dlm_splay_check2.py set them, but for
its own rate: an uncoupled unit at its target rate gets a CV of 0.22, with the kick rate found by bisection (16 steps,
geometric) and, at each, the bias for the rate (18 steps; 8 runs of 60 s). The coupled drives are then found as in
dlm_splay_check7.py, in two passes (plus or minus 3 mV, then 0.05 mV) on 8 runs of 60 s. Each unit must end within 2% of
its target, or the condition is reported as failing calibration.
Measured as dlm_splay_check6.py measures (8 runs of 300 s after 3 s, seeds 5100 + 10 x condition), with each unit's rate
and CV, and the ten pairs against flies'.
Read: if MN5's pairs come inside flies' ranges (within 10 ms 0.34-0.58 times chance, MN4-MN5 dip10 0.016-0.097) at 1.10
or 1.26 times with MN5's CV within 0.05 of MN1-4's, the rate ratio is enough. If they don't, check 7's fit came from MN5's
regularity, and the MN5 shortfall found in review 11 stands at flies' rate ratios.

Ran (2026-10-12, 3 minutes): once MN5 is as irregular as the others, its pairs stay outside flies' ranges at every rate
ratio, and move away from flies' as MN5 speeds up. By the reading, dlm_splay_check7.py's fit at 1.26 times came from
MN5's regularity, and the MN5 shortfall stands at flies' rate ratios.
- Kicks for a CV of 0.22, uncoupled: 9.17 a second at 6.3 Hz, 13.34 at 6.93 and 23.93 at 7.938 (dlm_splay_check2.py's
  10.80 at 6.6). All three conditions calibrated within 2% (MN1-4 6.27-6.38 Hz; MN5 6.29, 6.89 and 7.94).
- In the main runs MN1-4's CVs were 0.225-0.239 and MN5's 0.259, 0.259 and 0.237, within 0.05 of MN1-4's at every
  ratio.
- MN5's pairs (flies: within 10 ms 0.34-0.58 times chance, MN4-MN5 dip10 0.016-0.097):
  - at 1.0 times, within 10 ms 0.585-0.620 and dip10 0.101-0.108 (MN4-MN5 0.104);
  - at 1.10, 0.625-0.639 and 0.107-0.112 (0.112);
  - at 1.26, 0.630-0.682 and 0.115-0.121 (0.117).
- Splayness 0.749, 0.744 and 0.736 (flies 0.73-0.79); preferred orders 61-62%; 25% of windows with a repeat (flies
  5-20%).
- Weak MN1-4 pairs: within 10 ms 0.44-0.52 times chance and dip10 0.080-0.087 (flies 0.16-0.31 and 0.030-0.056).
- Strong pairs: within 10 ms 0.24-0.34, dip10 0.029-0.040, r 0.30-0.32. Flies' two pairs: 0.05 and 0.20, 0.006 and
  0.025, 0.336 and 0.394.
So with every unit about as irregular as flies', leaky integrators at flies' coupling have flies' splayness, but none of
the three kinds of pair falls inside flies' ranges. The strong pairs come closest, and the weak pairs and MN5's fire
together more often than flies'.

    python experiments/dlm_splay_check10.py      (writes experiments/dlm_splay_check10.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6
import dlm_splay_check7 as c7

OUT = Path(__file__).with_suffix(".json")
SEED = 5100
BASE_HZ = 6.3
RATIOS = (1.0, 1.10, 1.26)


def brain(kicks: tuple[float, float], coupling, biases: np.ndarray):
    """Five leaky-integrator units, MN1-4 kicked at kicks[0] and MN5 at kicks[1] per second (0.1 mV each)."""
    b = c5.unit("LIF", 0.0, kicks[0], c1.KICK_MV, coupling, None, c1.RUNS)
    b.set_type("MN5", noise_rate=kicks[1])
    b.set_bias(np.asarray(biases, np.float64))
    return b


def rate_cv(kick_hz: float, bias: float) -> tuple[float, float]:
    t = c1.spike_times(c5.unit("LIF", bias, kick_hz, c1.KICK_MV, None, None, c1.RUNS), 60.0, c1.SEED - 1)
    rate = float(np.mean([[len(x) / 60.0 for x in run] for run in t]))
    cv = float(np.mean([np.diff(x).std() / np.diff(x).mean() for run in t for x in run if len(x) > 2]))
    return rate, cv


def bias_for(kick_hz: float, target_hz: float) -> tuple[float, float, float]:
    """dlm_splay_check5.private_bias for a target rate: an uncoupled unit's bias, its rate and CV."""
    mean_kick = kick_hz * c1.KICK_MV * c1.UNIT["tau_m"]
    lo, hi = 7.0 - mean_kick - 3.0, 7.0 - mean_kick + 3.0
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        rate, cv = rate_cv(kick_hz, mid)
        lo, hi = (mid, hi) if rate < target_hz else (lo, mid)
    bias = 0.5 * (lo + hi)
    rate, cv = rate_cv(kick_hz, bias)
    return bias, rate, cv


def kicks_for(target_hz: float, target_cv: float = c1.TARGET_CV) -> dict:
    """dlm_splay_check2.calibrate for a target rate: the kick rate giving an uncoupled unit a CV of target_cv there."""
    trail = []
    lo, hi = 0.2, 20000.0
    for _ in range(16):
        mid = float(np.sqrt(lo * hi))
        bias, rate, cv = bias_for(mid, target_hz)
        trail.append({"kick_hz": round(mid, 3), "bias_mv": round(bias, 5), "rate_hz": round(rate, 3), "isi_cv": round(cv, 4)})
        lo, hi = (mid, hi) if cv < target_cv else (lo, mid)
    best = min(trail, key=lambda x: abs(x["isi_cv"] - target_cv) + abs(x["rate_hz"] - target_hz) / target_hz)
    return {"target_hz": target_hz, "target_cv": target_cv, "chosen": best, "trail": trail}


def main() -> None:
    t0 = time.perf_counter()
    d6 = json.loads(Path(c6.OUT).read_text())
    coupling, _ = c6.junctions(d6["ratios"]["assumed_mn5"], c5.CC, False)
    start = np.array(d6["conditions"]["LIF, MN5 assumed"]["unit_biases_mv"])
    out = {"question": __doc__, "flies_pairs": c6.FLIES_PAIRS, "kicks": {}, "conditions": {}}
    for hz in sorted({round(BASE_HZ * r, 3) for r in RATIOS}):
        out["kicks"][str(hz)] = kicks_for(hz)
        print("kicks", json.dumps(out["kicks"][str(hz)]["chosen"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    for c, ratio in enumerate(RATIOS):
        targets = np.array([BASE_HZ] * 4 + [BASE_HZ * ratio])
        kicks = (out["kicks"][str(round(BASE_HZ, 3))]["chosen"]["kick_hz"], out["kicks"][str(round(BASE_HZ * ratio, 3))]["chosen"]["kick_hz"])
        rates_for = lambda bb: np.array([np.mean([len(r[i]) / 60.0 for r in c1.spike_times(brain(kicks, coupling, bb), 60.0, c1.SEED - 1)])
                                         for i in range(c1.N)])
        first = c7.biases_for(targets, rates_for, start, 3.0)
        biases = c7.biases_for(targets, rates_for, first, 0.05)
        cal = rates_for(biases)
        calibrated = bool(np.all(np.abs(cal / targets - 1) <= 0.02))
        runs = c1.spike_times(brain(kicks, coupling, biases), c1.SECONDS, SEED + 10 * c)
        res = c6.summarize(runs)
        res.update({"targets_hz": [round(float(x), 3) for x in targets], "kick_hz": {"MN1-4": kicks[0], "MN5": kicks[1]},
                    "calibration_rates_hz": [round(float(x), 3) for x in cal], "calibrated_within_2pct": calibrated,
                    "unit_biases_mv": [round(float(x), 5) for x in biases]})
        name = f"LIF, MN5 at {ratio:.2f} x MN1-4, own kicks"
        out["conditions"][name] = res
        s = res["summary"]
        print(name, json.dumps({"calibrated": calibrated, "cal": res["calibration_rates_hz"], "rates": res["unit_rates_hz"],
                                "cv": res["unit_isi_cv"], "splayness": s["splayness"][0], "preferred": s["preferred_order_share"][0],
                                "repeats": s["repeat_share"], "pairs": res["pairs"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
