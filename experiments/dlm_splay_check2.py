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
