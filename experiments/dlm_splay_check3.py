"""Exploratory check, written after dlm_splay_check2.py's result and before it runs, not pre-registered and not a change
to the model: the DLM motor neurons' splay state with the unit given flies' afterhyperpolarization, so that their
spikelets can be included.

dlm_splay_check2.py: five of brainfly's units, joined by conductances at flies' measured strengths, gave most of the splay
state's signatures. Splayness was 0.71 (flies 0.73-0.79), MN4-MN5 r and dip10 fell inside flies' ranges, and the
strong pairs fired in antiphase. But spikelets at flies' measured share synchronized them outright (splayness 0.30). In
flies each partner spike passes about 0.4 mV of brief excitation and about 0.5 mV of inhibition lasting more than
100 ms: the presynaptic AHP, 14.4 mV below baseline at 11.5 ms, 10.4 at 50 ms and 8.7 at 100 ms (Hürkey et al.'s Fig.
2h source trace; research_notes/Rung 8 flight data/dlm_splay_state.md section 2.9). The model's unit resets 12 mV
below threshold and recovers over its 20 ms membrane, with no slow AHP.
Unit (AHP): dlm_splay_check.py's (20 ms membrane, threshold 7 mV, refractory 2.2 ms), with two changes fitted to flies'
AHP before this was written:
- The reset is 18 mV below threshold, flies' fast AHP trough (median of 15 traces, section 2.8).
- An adaptation current, 10.3 mV per spike decaying over 0.476 s, the least-squares fit to the three points of the
  Fig. 2h trace given that reset. It gives 14.6, 10.3 and 8.75 mV below baseline at 11.5, 50 and 100 ms; with the
  model's own reset the best fit misses by up to 1.3 mV.
Checked first, not fitted: the unit's f-I, measured as flies' was (spikes over 1 s and 0.4 s steps from rest, by step
size in mV), against flies' 62-75 Hz/nA (Fig. 1e mean; 75 per-cell median, IQR 45-82) at an input resistance of 80-100
MOhm. Then dlm_splay_check2.py's procedure: the uncoupled units calibrated to 6.6 Hz and flies' ISI CV of 0.22 by the
kicks' rate, and the bias found again in every condition for 6.6 Hz. Conditions:
  uncoupled
  measured             conductances at the measured CCs (0.023 / 0.011; MN5 0.0075)
  measured + spikelet  plus spikelets: on the strong pairs 0.035 mV, flies' measured 0.38 mV for about the 1.86 ms of a
                       spike's half-width as the jump with the same area over the 20 ms membrane, and on the other pairs
                       scaled with their coupling
  model's + spikelet   Hürkey et al.'s model's CCs (0.0099 / 0.0044 / 0.0031), with the spikelets scaled with them
  measured x 3 + spikelet
Measured as dlm_splay_check2.py measures; 300 s per run after 3 s, 8 runs (seeds 4400 + condition).

    python experiments/dlm_splay_check3.py      (writes experiments/dlm_splay_check3.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import dlm_splay_check as c1
from brainfly.hybrid import HybridBrain

OUT = Path(__file__).with_suffix(".json")
UNIT = {**c1.UNIT, "reset": 7.0 - 18.0, "adaptation": 10.3, "adaptation_tau": 0.476}
AHP_TARGET_MV = {0.0115: -14.4, 0.05: -10.4, 0.10: -8.7}
SPIKELET_MV = 0.38 * 1.86e-3 / 0.02
FLIES_HZ_PER_NA = [62.0, 75.0]
RIN_MOHM = [80.0, 100.0]


def brain(bias: float, kick_hz: float, coupling=None, spikelet: float = 0.0, trials: int = c1.RUNS) -> HybridBrain:
    labels = {"cell_type": np.array([f"MN{k + 1}" for k in range(c1.N)]), "side": np.array(["R"] * c1.N),
              "superclass": np.array(["motor"] * c1.N)}
    gap = None
    if spikelet and coupling is not None:
        c = coupling.tocoo()                      # spikelets on the coupled pairs, scaled with each pair's coupling
        gap = sparse.csr_matrix((spikelet * c.data / 0.0235, (c.row, c.col)), shape=(c1.N, c1.N))
    return HybridBrain(matrix=sparse.csr_matrix((c1.N, c1.N), dtype=np.float32), labels=labels, trials=trials, dt=c1.DT,
                       w_syn=1.0, types={"all": {**UNIT, "bias": bias, "noise_rate": kick_hz, "noise_kick": c1.KICK_MV}},
                       coupling=coupling, gap=gap, w_poi=40.0)


def ahp() -> dict:
    """The unit's voltage after one forced spike from just below threshold, against flies' AHP (mV below baseline)."""
    b = brain(6.9, 0.0, trials=1)
    b.advance(20000)                              # 2 s to settle at 6.9 mV
    base = float(b.u[0, 0])
    b.advance(1, drive=[([0], 1 / c1.DT)])         # a sure kick; it fires on the next step
    out = {}
    trace = []
    for k in range(1100):
        b.advance(1)
        trace.append(float(b.u[0, 0]) - base)
    for t_s, target in AHP_TARGET_MV.items():
        out[f"{t_s * 1000:g} ms"] = {"model_mv": round(trace[int(round(t_s / c1.DT))], 2), "flies_mv": target}
    return out


def f_i() -> dict:
    """Rates over 1 s and 0.4 s steps from rest, by step size (mV of bias), no kicks; slope over 2-30 Hz."""
    steps = np.arange(6.0, 150.01, 1.0)
    rows = []
    for mv in steps:
        b = brain(float(mv), 0.0, trials=1)
        b.reset(1)
        c04 = b.advance(4000)[0, 0]
        c10 = c04 + b.advance(6000)[0, 0]
        rows.append({"step_mv": float(mv), "hz_1s": float(c10), "hz_04s": float(c04 / 0.4)})
    out = {"rows": rows}
    for key in ("hz_1s", "hz_04s"):
        pts = [(r["step_mv"], r[key]) for r in rows if 2.0 <= r[key] <= 30.0]
        if len(pts) >= 2:
            x, y = np.array(pts).T
            slope = float(np.polyfit(x, y, 1)[0])
            out[key] = {"hz_per_mv": round(slope, 3), "hz_per_na": [round(slope * r, 1) for r in RIN_MOHM]}
    return out


def stats(bias: float, hz: float, coupling=None, spikelet: float = 0.0) -> tuple:
    t = c1.spike_times(brain(bias, hz, coupling, spikelet), 60.0, c1.SEED - 1)
    rate = float(np.mean([[len(x) / 60.0 for x in run] for run in t]))
    cvs = [np.diff(x).std() / np.diff(x).mean() for run in t for x in run if len(x) > 2]
    return rate, float(np.mean(cvs)) if cvs else 0.0


def bias_for(hz: float, coupling=None, spikelet: float = 0.0) -> tuple:
    """dlm_splay_check2.bias_for, over 0-120 mV (the adapting unit needs far more drive for 6.6 Hz)."""
    mean_kick = hz * c1.KICK_MV * UNIT["tau_m"]
    lo, hi = -mean_kick, 120.0 - mean_kick
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        rate, cv = stats(mid, hz, coupling, spikelet)
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi), rate, cv


def calibrate() -> dict:
    """dlm_splay_check2.calibrate's search (0.2-20,000 Hz of kicks, 16 halvings), with this unit."""
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
    out = {"question": __doc__, "flies": {**c1.FLIES, "hz_per_na": FLIES_HZ_PER_NA, "ahp_mv": AHP_TARGET_MV}, "unit": UNIT,
           "kick_mv": c1.KICK_MV, "spikelet_mv": SPIKELET_MV}
    out["ahp"] = ahp()
    print("AHP", json.dumps(out["ahp"]), flush=True)
    out["f_i"] = f_i()
    print("f-I", json.dumps({k: v for k, v in out["f_i"].items() if k != "rows"}), flush=True)
    out["calibration"] = cal = calibrate()
    hz = cal["chosen"]["kick_hz"]
    measured = c1.ratios(0.023, 0.011, 0.0075)
    conditions = [("uncoupled", None, 0.0), ("measured", measured, 0.0), ("measured + spikelet", measured, SPIKELET_MV),
                  ("model's + spikelet", c1.ratios(0.0099, 0.0044, 0.0031), SPIKELET_MV),
                  ("measured x 3 + spikelet", c1.ratios(0.069, 0.033, 0.0225), SPIKELET_MV)]
    out["conditions"] = {}
    for c, (name, coupling, spikelet) in enumerate(conditions):
        bias, rate, cv = bias_for(hz, coupling, spikelet)
        res = c1.measure(c1.spike_times(brain(bias, hz, coupling, spikelet), c1.SECONDS, c1.SEED + c))
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
