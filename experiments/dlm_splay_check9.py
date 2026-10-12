"""Exploratory check, written before it runs, not pre-registered and not a change to the model: dlm_splay_check6.py's
leaky-integrator units at flies' coupling, with most of their irregularity shared, as dlm_splay_check4.py shared it.

With private noise, leaky-integrator units at flies' coupling (dlm_splay_check6.py, dlm_splay_check7.py) and Hürkey et
al.'s own conductance model as published (dlm_splay_check8.py) leave the weakly coupled MN1-4 pairs coming within 10 ms
of each other more often than flies' (0.50-0.59 times chance, against 0.16-0.31; dip10 0.09-0.11 against 0.03-0.06).
In the leaky integrators 23-30% of 4-spike windows also hold a repeat (flies 5-20%). Flies' DLM motor neurons share
88-95% of their input (MaleCNS). dlm_splay_check4.py found that sharing most of the irregularity gives flies' firing
order, but it used the AHP unit at about half flies' coupling, where the splay stayed weak. Shared irregularity moves
all five units together, so it may leave the coupling's pull on their relative phases intact where private noise
scatters them.
Model: dlm_splay_check6.py's "LIF, MN5 assumed" (the leaky integrator; flies' coupling as 20 ms peak ratios; MN5's
junctions at the assumed CC 0.0075; no spikelets), with its private kicks (0.1 mV) and a shared Ornstein-Uhlenbeck
fluctuation (0.5 s, set every 10 ms, the same for all five), as in dlm_splay_check4.py:
- For each share f of the ISI variance (0.5, 0.8, 0.95), the private kicks' rate is set so that private noise alone
  gives a CV of 0.22 x sqrt(1 - f). The shared fluctuation's size is then set so that both together give 0.22, on
  uncoupled units at 6.6 Hz (bisection, 60 s).
- At each share, two conditions:
  - uncoupled: one bias for all five, found for 6.6 Hz in that calibration;
  - coupled: flies' coupling, each unit's bias found so that all five fire at 6.6 Hz, in dlm_splay_check7.py's two
    passes on 4 runs of 60 s. Each unit must end within 2% of 6.6 Hz, or the condition is reported as failing
    calibration.
Measured as dlm_splay_check6.py measures: 8 runs of 300 s after 3 s, each with its own shared fluctuation (seeds 5000 +
10 x share's index + condition, plus 100 x run). Also each unit's rate and CV, and the ten pairs against flies'.
Read: if at some share the coupled units put the weakly coupled pairs inside flies' ranges (dip10 0.030-0.056, within
10 ms 0.16-0.31 times chance) while their splayness stays in flies' 0.73-0.79, flies' shared drive may be what lets the
weak coupling hold those pairs apart; the whole-network test would get it from the connectome's shared input. If
sharing bunches the units (splayness below 0.73) or leaves the weak pairs short, it isn't.

    python experiments/dlm_splay_check9.py      (writes experiments/dlm_splay_check9.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1
import dlm_splay_check4 as c4
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6
import dlm_splay_check7 as c7

OUT = Path(__file__).with_suffix(".json")
SEED = 5000
SHARES = (0.5, 0.8, 0.95)
CAL_RUNS = 4


def run(biases: np.ndarray, kick_hz: float, sd_mv: float, seconds: float, seed: int, coupling=None) -> list[np.ndarray]:
    """One run of the five leaky-integrator units: private kicks and the shared fluctuation (sd_mv, an OU process over
    dlm_splay_check4.TAU_SHARED) set every dlm_splay_check4.PIECE s; each unit's spike times (s)."""
    b = c5.unit("LIF", 0.0, kick_hz, c1.KICK_MV, coupling, None, 1)
    b.reset(seed)
    rng = np.random.default_rng(seed)
    a = np.exp(-c4.PIECE / c4.TAU_SHARED)
    ou = rng.standard_normal()
    steps = int(round(c4.PIECE / c1.DT))
    burn, total = int(round(c1.BURN / c4.PIECE)), int(round(seconds / c4.PIECE))
    times = [[] for _ in range(c1.N)]
    for k in range(burn + total):
        ou = a * ou + np.sqrt(1 - a * a) * rng.standard_normal()
        b.set_bias(biases + sd_mv * ou)
        if k < burn:
            b.advance(steps)
            continue
        _, sp = b.advance(steps, record=np.arange(c1.N))
        for _, step, i in zip(*np.nonzero(sp)):
            times[i].append(((k - burn) * steps + step) * c1.DT)
    return [np.array(t) for t in times]


def bias_for(kick_hz: float, sd_mv: float) -> tuple:
    """dlm_splay_check4.bias_for for the leaky integrator: one bias, uncoupled, for 6.6 Hz (one run of 60 s)."""
    mean_kick = kick_hz * c1.KICK_MV * c1.UNIT["tau_m"]
    lo, hi = -mean_kick - 20.0, 120.0 - mean_kick
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        rate, cv = c4.rate_cv(run(np.full(c1.N, mid), kick_hz, sd_mv, 60.0, SEED - 1))
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi), rate, cv


def calibrate(share: float) -> dict:
    """dlm_splay_check4.calibrate for the leaky integrator."""
    target_private = c1.TARGET_CV * np.sqrt(1 - share)
    lo, hi = 0.2, 50000.0
    for _ in range(14):                              # private kicks alone for target_private
        mid = float(np.sqrt(lo * hi))
        bias, rate, cv = bias_for(mid, 0.0)
        lo, hi = (mid, hi) if cv < target_private else (lo, mid)
    kick_hz, private_cv = mid, cv
    lo, hi = 0.0, 40.0
    for _ in range(14):                              # then the shared fluctuation's size for 0.22 in all
        sd = 0.5 * (lo + hi)
        bias, rate, cv = bias_for(kick_hz, sd)
        lo, hi = (sd, hi) if cv < c1.TARGET_CV else (lo, sd)
    return {"share": share, "kick_hz": round(kick_hz, 3), "private_cv": round(private_cv, 3),
            "target_private_cv": round(float(target_private), 3), "shared_sd_mv": round(sd, 4), "bias_mv": round(bias, 4),
            "rate_hz": round(rate, 2), "isi_cv": round(cv, 3)}


def main() -> None:
    t0 = time.perf_counter()
    d6 = json.loads(Path(c6.OUT).read_text())
    coupling, _ = c6.junctions(d6["ratios"]["assumed_mn5"], c5.CC, False)
    out = {"question": __doc__, "flies_pairs": c6.FLIES_PAIRS, "ratios": d6["ratios"]["assumed_mn5"], "shares": {}}
    for si, share in enumerate(SHARES):
        cal = calibrate(share)
        print("calibration", json.dumps(cal), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        row = {"calibration": cal, "conditions": {}}
        kick_hz, sd = cal["kick_hz"], cal["shared_sd_mv"]
        targets = np.full(c1.N, c1.TARGET_HZ)
        rates_for = lambda bb: np.array([np.mean([len(t[i]) / 60.0 for t in
                                                  [run(bb, kick_hz, sd, 60.0, SEED - 1 + 100 * r, coupling) for r in range(CAL_RUNS)]])
                                         for i in range(c1.N)])
        for ci, name in enumerate(("uncoupled", "coupled")):
            res = {}
            if name == "uncoupled":
                biases, junction = np.full(c1.N, cal["bias_mv"]), None
            else:
                first = c7.biases_for(targets, rates_for, np.full(c1.N, cal["bias_mv"]), 3.0)
                biases, junction = c7.biases_for(targets, rates_for, first, 0.05), coupling
                cal_rates = rates_for(biases)
                res.update({"calibration_rates_hz": [round(float(x), 3) for x in cal_rates],
                            "calibrated_within_2pct": bool(np.all(np.abs(cal_rates / targets - 1) <= 0.02))})
            runs = [run(biases, kick_hz, sd, c1.SECONDS, SEED + 10 * si + ci + 100 * r, junction) for r in range(c1.RUNS)]
            res.update(c6.summarize(runs))
            res["unit_biases_mv"] = [round(float(x), 5) for x in biases]
            row["conditions"][name] = res
            s = res["summary"]
            print(f"share {share} {name}", json.dumps({k: res.get(k) for k in ("calibrated_within_2pct", "calibration_rates_hz", "unit_rates_hz", "unit_isi_cv")}),
                  json.dumps({"splayness": s["splayness"][0], "preferred": s["preferred_order_share"][0], "repeats": s["repeat_share"],
                              "coincidence": s["coincidence_vs_chance_3ms"][0], "pairs": res["pairs"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
            out["shares"][str(share)] = row
            OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
