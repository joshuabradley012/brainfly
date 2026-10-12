"""Exploratory check, written after dlm_splay_check.py's result and before it runs, not pre-registered and not a change
to the model: dlm_splay_check.py again, at flies' irregularity if the unit can reach it, and at one rate in every
condition.

dlm_splay_check.py: conductance coupling at flies' measured strengths moved five of brainfly's units a third of the way
to flies' splay state. Splayness went from 0.59 to 0.64 (flies 0.76), MN4-MN5's dip10 from 0.20 to 0.16 (flies 0.06),
and the strong pairs fired in antiphase. But two things confounded it:
- Its calibration's search stopped at 55 Hz of kicks with an ISI CV of 0.34 (flies 0.22).
- The coupling's load slowed the units, from 6.6 to 4.95 Hz, and made them more irregular (CV 0.50). Flies' rates
  don't change with shakB RNAi.
Model and measures: dlm_splay_check.py's, with two changes:
- The kicks' rate is searched from 0.2 Hz (16 halvings on a log scale).
- In every condition the shared drive (bias) is found again, by the same bisection, so that the units fire at 6.6 Hz
  with that condition's coupling. The kicks stay as calibrated on the uncoupled units.
The order of MN1-4 is also reported among complete 4-spike windows (all four neurons once), besides over all windows.
Runs, seeds (4400 + condition) and durations are dlm_splay_check.py's.

Ran (2026-10-11, 35 s): at flies' irregularity and one rate, the measured coupling gives most of flies' splay state.
- The calibration found 10.8 Hz of kicks (bias 7.001 mV). Uncoupled, the units fire at 6.58 Hz with CV 0.22.
- Uncoupled: independent, as the nulls give. Splayness 0.592, MN4-MN5 r 0.643, dip10 0.20, coincidences 1.01 times
  chance. MN1-4's preferred orders take 22% of windows (34% of complete ones, about a third by chance).
- Measured CCs (bias 7.055 for 6.6 Hz; CV 0.26):
  - splayness 0.713 (flies 0.73-0.79; null 0.59);
  - r 0.595 and dip10 0.101 (flies 0.49-0.63 and 0.02-0.10);
  - spikes within 3 ms of another's at 0.69 times chance (flies' controls fall below chance);
  - MN2 at 0.51 of MN1's cycle and MN4 at 0.50 of MN3's, vector strength 0.40 (flies 0.42-0.61, about 0.7);
  - the preferred orders, 1324 and 1423, at 19-20% of windows each, the other four at 6.5-7%. That is 39% of all
    windows (flies 48-70%) and 59% of complete ones (flies' complete cycles 51-79%). 35% of the windows hold a repeat,
    as uncoupled (flies 9%).
- The model's CCs: a little weaker. Splayness 0.704, r 0.589, dip10 0.109; preferred orders 31% of windows, 47% of
  complete ones.
- Measured x 3: splayness 0.712, r 0.612, dip10 0.075. The strong pairs lock tighter (vector strength 0.68), and the
  preferred orders take 56% of windows (86% of complete ones).
- With spikelets: synchrony. Splayness 0.297, r 0.80, dip10 0.66, coincidences 5.0 times chance, and MN4 in phase with
  MN3 (0.00).
So brainfly's leaky integrators, joined by conductances at flies' measured strengths, give the splay state's main
signatures:
- splayness just under flies' range, and r and dip10 inside theirs;
- coincidences below chance;
- the strong pairs in antiphase, with the orders that put them opposite preferred.
The pairs' tightness and the orders' share fall short. 35% of 4-spike windows hold a repeat, where flies' hold 9%,
which suggests flies' irregularity is shared (all five rates rising and falling together) more than private. And the
spikes' own depolarization, passed at flies' measured share, synchronizes the units outright. In flies the long AHP
(more than 100 ms, passed at CC 0.04) outweighs it. The model's unit has no such AHP, only a reset that recovers over
its 20 ms membrane.

Correction (2026-10-11, review 8):
- As in dlm_splay_check.py's correction, "the measured CCs" ran at about half flies' effective coupling (the
  steady-state conversion of 20 ms peak ratios). "Measured x 3" is nearer flies' strength (1.8 times) than "measured".
- dip10's median, 0.101 (runs 0.087-0.105), is just above flies' maximum, 0.097, so "inside theirs" is borderline.
- "Most of the splay state" overstates. From uncoupled to flies' controls, splayness and dip10 go about 70% of the way,
  r and the strong pairs' locking about half, the preferred orders 45%, and the windows with a repeat none of it.
- The preferred orders' 59% of complete windows compares with flies' sliding windows, 52-77% (preferred over
  complete), not with flies' complete MN1 cycles (51-79%).
- MN5's coupling (0.0075) is Hürkey et al.'s model's convention, not a measurement. dip10, an MN4-MN5 measure, depends
  on it.
- The spikelets were dlm_splay_check.py's unsourced 0.0375 mV on every pair. dlm_splay_check3.py's sizes (0.035 mV on
  the strong pairs, smaller on the others) synchronize this unit too (review 8's rerun: splayness 0.41, coincidences
  4.7 times chance).

    python experiments/dlm_splay_check2.py      (writes experiments/dlm_splay_check2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1

OUT = Path(__file__).with_suffix(".json")


def stats(bias: float, hz: float, coupling=None, spikelet: float = 0.0) -> tuple:
    t = c1.spike_times(c1.brain(bias, hz, coupling, spikelet), 60.0, c1.SEED - 1)
    rate = float(np.mean([[len(x) / 60.0 for x in run] for run in t]))
    cvs = [np.diff(x).std() / np.diff(x).mean() for run in t for x in run if len(x) > 2]
    return rate, float(np.mean(cvs)) if cvs else 0.0


def bias_for(hz: float, coupling=None, spikelet: float = 0.0) -> tuple:
    """The bias (mV) at which the units fire at 6.6 Hz with these kicks and this coupling, by bisection."""
    mean_kick = hz * c1.KICK_MV * c1.UNIT["tau_m"]
    lo, hi = 7.0 - mean_kick - 3.0, 7.0 - mean_kick + 3.0
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        rate, cv = stats(mid, hz, coupling, spikelet)
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi), rate, cv


def calibrate() -> dict:
    trail = []
    lo, hi = 0.2, 20000.0
    for _ in range(16):
        mid = float(np.sqrt(lo * hi))
        bias, rate, cv = bias_for(mid)
        trail.append({"kick_hz": round(mid, 3), "bias_mv": round(bias, 5), "rate_hz": round(rate, 2), "isi_cv": round(cv, 3)})
        print("calibrate", json.dumps(trail[-1]), flush=True)
        lo, hi = (mid, hi) if cv < c1.TARGET_CV else (lo, mid)
    best = min(trail, key=lambda x: abs(x["isi_cv"] - c1.TARGET_CV) + abs(x["rate_hz"] - c1.TARGET_HZ) / c1.TARGET_HZ)
    return {"chosen": best, "trail": trail}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": c1.FLIES, "unit": c1.UNIT, "kick_mv": c1.KICK_MV}
    out["calibration"] = cal = calibrate()
    hz = cal["chosen"]["kick_hz"]
    measured = c1.ratios(0.023, 0.011, 0.0075)
    conditions = [("uncoupled", None, 0.0), ("measured", measured, 0.0), ("model's", c1.ratios(0.0099, 0.0044, 0.0031), 0.0),
                  ("measured x 3", c1.ratios(0.069, 0.033, 0.0225), 0.0), ("+ spikelet", measured, c1.SPIKELET_MV)]
    out["conditions"] = {}
    for c, (name, coupling, spikelet) in enumerate(conditions):
        bias, rate, cv = bias_for(hz, coupling, spikelet)
        res = c1.measure(c1.spike_times(c1.brain(bias, hz, coupling, spikelet), c1.SECONDS, c1.SEED + c))
        for r in res["runs"]:
            complete = 1.0 - r["orders"].get("rest", 0.0)
            r["preferred_share_of_complete"] = round(r["preferred_order_share"] / complete, 4) if complete > 0 else None
        vals = [r["preferred_share_of_complete"] for r in res["runs"] if r["preferred_share_of_complete"] is not None]
        res["summary"]["preferred_share_of_complete"] = [round(float(np.median(vals)), 4), round(min(vals), 4), round(max(vals), 4)]
        res["summary"]["rest_share"] = round(float(np.median([r["orders"].get("rest", 0.0) for r in res["runs"]])), 4)
        res["bias_mv"] = round(bias, 5)
        out["conditions"][name] = res
        print(name, f"bias {bias:.4f}", json.dumps(res["summary"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
