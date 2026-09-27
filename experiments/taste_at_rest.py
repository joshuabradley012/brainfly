"""Does rung 1's taste pathway survive in rung 4's resting brain? (pre-registered)

Rung 1 passed (shiu_rewiring.py) in a brain that is silent at rest: sugar taste neurons drive the
proboscis motor neuron MN9, bitter and Ir94e neurons suppress it, and scrambled wiring abolishes it.
Rung 4's resting brain (rest_calibration2.py) adds per-type properties, short-term depression at
cholinergic synapses and a calibrated resting activity in every neuron. Each rung has to keep the
ones below it passing, so this repeats rung 1's tests there, measured against MN9's resting rate.
Model: rest_calibration2.py's, with its intact biases, unchanged (no recalibration). Protocol, 30
trials per condition: a fresh start, 1 s to settle, then 1 s with the taste neurons driven by
Poisson input at 100 Hz (rung 1's drive: w_poi = 250 x w_syn, SETS of shiu_baseline.py), then 0.5 s
without. MN9's rate at rest is taken over the 0.5 s before the drive.
Tests (MN9 L, as rung 1's):
  SUGAR     sugar raises MN9 by at least 10 Hz over its resting rate (t >= 4 over trials)
  RESPONSE  at 10 Hz of sugar, MN9's rise is at most 25% of its rise at 100 Hz
  BITTER    adding bitter neurons cuts sugar's rise by at least 25% (Welch t >= 4)
  IR94E     adding Ir94e neurons cuts sugar's rise by at least 25% (Welch t >= 4)
  STABLE    during sugar at most 0.1% of the undriven neurons pass 100 Hz, and in the last 0.25 s
            after it the brain's mean rate is within 20% of its rate at rest
  NULL      in rest_calibration2.py's 2 degree-preserving rewirings, with their own biases, sugar
            raises MN9 by less than 10 Hz
Pass: all six. Reported: WATER (MN9's rise under water neurons) and MN9 R.

    python experiments/taste_at_rest.py            (writes experiments/taste_at_rest.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import rest_calibration2 as attempt2
from brainfly import nulls
from brainfly.hybrid import HybridBrain
from shiu_baseline import SETS, welch
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
TRIALS, SETTLE, DRIVE, TAIL, REST_WINDOW = 30, 1.0, 1.0, 0.5, 0.5


def build(rewiring: int | None) -> tuple[HybridBrain, dict, np.ndarray, np.ndarray]:
    M, scale, labels, types, superclass = attempt1.network()
    if rewiring is not None:
        M = nulls.degree_preserving(M, np.random.default_rng(100 + rewiring))
    key = np.where(types != "", types, np.char.add("superclass:", superclass))
    names, gid = np.unique(key, return_inverse=True)
    saved = np.load(attempt2.HERE / ("intact.npz" if rewiring is None else f"rewired-{rewiring}.npz"))
    assert np.array_equal(saved["groups"], names)
    spec, sets = attempt2.model(types, superclass)
    brain = HybridBrain(trials=TRIALS, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=0, types=spec, sets=sets,
                        bias=saved["bias"][gid])
    cells = {k: brain.cells(v, "L") for k, v in SETS.items()}
    return brain, cells, brain.cells(["MN9"], "L"), brain.cells(["MN9"], "R")


def trial(brain: HybridBrain, drive: list, seed: int) -> dict:
    """One condition, all trials: MN9 L/R rates at rest and under the drive, the brain's mean rate
    at rest and late in the tail, and the undriven neurons over 100 Hz under the drive."""
    brain.reset(seed)
    brain.advance(int(round((SETTLE - REST_WINDOW) / brain.dt)))
    rest = brain.advance(int(round(REST_WINDOW / brain.dt))) / REST_WINDOW
    driven = brain.advance(int(round(DRIVE / brain.dt)), drive=drive) / DRIVE
    brain.advance(int(round((TAIL - 0.25) / brain.dt)))
    late = brain.advance(int(round(0.25 / brain.dt))) / 0.25
    return {"rest": rest, "driven": driven, "late": late}


def main() -> None:
    t0 = time.perf_counter()
    brain, cells, mn9L, mn9R = build(None)
    undriven = np.ones(brain.n, bool)
    undriven[np.concatenate(list(cells.values()))] = False
    run = lambda names, rate=100.0, seed=1: trial(brain, [(cells[k], rate) for k in names], seed)
    conds = {"sugar": run(["sugar"], seed=1), "sugar 10 Hz": run(["sugar"], 10.0, seed=5), "water": run(["water"], seed=2),
             "sugar+bitter": run(["sugar", "bitter"], seed=3), "sugar+ir94e": run(["sugar", "ir94e"], seed=4)}
    rise = {k: v["driven"][:, mn9L].mean(1) - v["rest"][:, mn9L].mean(1) for k, v in conds.items()}   # per trial
    t_sugar = rise["sugar"].mean() / (rise["sugar"].std(ddof=1) / np.sqrt(TRIALS))
    cut = lambda k: 1 - rise[k].mean() / rise["sugar"].mean() if rise["sugar"].mean() > 0 else 0.0
    s = conds["sugar"]
    hot = float((s["driven"][:, undriven].mean(0) > 100).mean())
    rest_mean, late_mean = float(s["rest"].mean()), float(s["late"].mean())
    results = {
        "criteria": __doc__,
        "mn9_L_hz": {k: {"rest": round(float(v["rest"][:, mn9L].mean()), 2), "driven": round(float(v["driven"][:, mn9L].mean()), 2)}
                     for k, v in conds.items()},
        "mn9_R_hz": {k: {"rest": round(float(v["rest"][:, mn9R].mean()), 2), "driven": round(float(v["driven"][:, mn9R].mean()), 2)}
                     for k, v in conds.items()},
        "rise_hz": {k: round(float(v.mean()), 2) for k, v in rise.items()},
        "t_sugar": round(float(t_sugar), 1), "bitter_cut": round(float(cut("sugar+bitter")), 3),
        "t_bitter": round(welch(rise["sugar"], rise["sugar+bitter"]), 1), "ir94e_cut": round(float(cut("sugar+ir94e")), 3),
        "t_ir94e": round(welch(rise["sugar"], rise["sugar+ir94e"]), 1),
        "undriven_over_100hz": round(hot, 5), "brain_rest_hz": round(rest_mean, 3), "brain_late_hz": round(late_mean, 3),
    }
    results["SUGAR"] = bool(rise["sugar"].mean() >= 10 and t_sugar >= 4)
    results["RESPONSE"] = bool(rise["sugar 10 Hz"].mean() <= 0.25 * rise["sugar"].mean())
    results["BITTER"] = bool(cut("sugar+bitter") >= 0.25 and results["t_bitter"] >= 4)
    results["IR94E"] = bool(cut("sugar+ir94e") >= 0.25 and results["t_ir94e"] >= 4)
    results["STABLE"] = bool(hot <= 0.001 and abs(late_mean - rest_mean) <= 0.2 * rest_mean)
    results["WATER_rise_hz"] = results["rise_hz"]["water"]
    print(json.dumps({k: v for k, v in results.items() if k != "criteria"}), flush=True)
    results["nulls"] = []
    for k in (1, 2):
        b, c, m, _ = build(k)
        r = trial(b, [(c["sugar"], 100.0)], seed=10 + k)
        rise_k = float((r["driven"][:, m].mean(1) - r["rest"][:, m].mean(1)).mean())
        results["nulls"].append({"rewiring": k, "rise_hz": round(rise_k, 2), "rest_hz": round(float(r["rest"][:, m].mean()), 2)})
        print(results["nulls"][-1], flush=True)
    results["NULL"] = all(n["rise_hz"] < 10 for n in results["nulls"])
    results["pass"] = all(results[k] for k in ("SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE", "NULL"))
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: " + " ".join(f"{k} {results[k]}" for k in ("SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE", "NULL"))
          + f" ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
