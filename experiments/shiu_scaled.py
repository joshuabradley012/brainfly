"""Does scaling each synapse by its target's size stop the MaleCNS runaway? (rung 1, second attempt)

shiu_baseline.py failed. With Shiu's uniform w_syn, weights of 0.20 mV and above run away, and weights
of 0.18 mV and below are stable but sugar barely reaches MN9 (shiu_runaway.py). Two findings point at
the uniform weight: synapse count predicts EPSP size best when divided by the target's size (Liu et
al. 2022), and Pugliese et al. found size-scaled excitability "crucial" in their MaleCNS nerve-cord
model. A synapse onto a big, leaky neuron should move it less.

Recipes (both reported). s_i = neuron i's total synapses (input + output) / the median over neurons,
a stand-in for size (MaleCNS's flat files carry no volumes):
  density   every synapse onto neuron i weighs w_syn * count / s_i
  sqrt      every synapse onto neuron i weighs w_syn * count / sqrt(s_i)
Calibration per recipe, Shiu's rule as in shiu_baseline.py (w_syn whose MN9 L rate at 100 Hz sugar
is closest to 80% of its maximum over 10-200 Hz), over w_syn = 0.275 x {0.35, 0.5, 0.7, 1, 1.4, 2,
2.8, 4} mV. The grid now runs both ways.

Tests per recipe at its calibrated w_syn: exactly shiu_baseline.py's (30 trials, 100 Hz, same neuron
sets and seeds). Pass, fixed before the first run: STABLE and SUGAR and NULL (the runaway gone, sugar
still reaching MN9, and that route still depending on the real wiring). WATER, BITTER and IR94E are
reported but are not part of the pass. Water never reached MN9 in any earlier variant, which points
at the provisional LB3a = water label, and bitter and Ir94e were only ever measured inside a runaway
network.

Re-run 2026-09-26 on brainfly.shiu's corrected kernel, which now matches Brian2 spike for spike
(tests/test_shiu_brian2.py). The first run used a kernel that kept input arriving during
refractoriness, where Brian2 drops it, and ran its steps in a different order; that run is in git
history.

    python experiments/shiu_scaled.py            (writes experiments/shiu_scaled.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly.shiu import W_SYN, ShiuBrain, counts
from shiu_baseline import RATES, SETS, SHUFFLES, tests

SCALES = [0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0]
OUT = Path(__file__).with_name("shiu_scaled.json")


def sizes(C: sparse.spmatrix) -> np.ndarray:
    A = abs(C)
    total = np.asarray(A.sum(0)).ravel() + np.asarray(A.sum(1)).ravel()
    s = total / np.median(total[total > 0])
    return np.where(total > 0, s, 1.0)


def calibrate(brain: ShiuBrain, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    grid = []
    for scale in SCALES:
        brain.w_syn = W_SYN * scale
        mn = [float(brain.run(1.0, drive=[(sugar, r)], seed=100 + r).rates[mn9[0]]) for r in RATES]
        ratio = mn[RATES.index(100)] / max(mn) if max(mn) > 0 else None
        grid.append({"w_syn": round(brain.w_syn, 4), "mn9_L_hz": [round(m, 2) for m in mn],
                     "ratio_100": None if ratio is None else round(ratio, 3)})
        print(f"    w_syn {brain.w_syn:.4f}: MN9 L {[round(m, 1) for m in mn]} Hz, 100 Hz / max = {grid[-1]['ratio_100']}", flush=True)
    usable = [g for g in grid if g["ratio_100"] is not None]
    pick = min(usable, key=lambda g: abs(g["ratio_100"] - 0.8)) if usable else None
    return {"grid": grid, "w_syn": None if pick is None else pick["w_syn"]}


def nulls(C: sparse.csc_matrix, w_syn: float, scale: np.ndarray, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    rng = np.random.default_rng(7)
    result = {}
    for name in ("weight_shuffle", "degree_preserving"):
        hits = []
        for k in range(SHUFFLES):
            if name == "weight_shuffle":
                M = sparse.csc_matrix((rng.permutation(C.data), C.indices, C.indptr), shape=C.shape)
            else:
                M = sparse.csc_matrix((C.data, rng.permutation(C.indices), C.indptr), shape=C.shape)
            b = ShiuBrain(w_syn=w_syn, trials=10, matrix=M, scale=scale)
            hits.append(float(b.run(1.0, drive=[(sugar, 100.0)], seed=200 + k).rates[mn9[0]]))
        result[name] = {"mn9_L_hz": [round(h, 2) for h in hits], "activated": int(sum(h > 0 for h in hits))}
        print(f"    {name}: MN9 L activated in {result[name]['activated']}/{SHUFFLES}", flush=True)
    result["NULL"] = all(result[k]["activated"] <= 2 for k in ("weight_shuffle", "degree_preserving"))
    return result


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsc()
    s = sizes(C)
    recipes = {"density": 1 / s, "sqrt": 1 / np.sqrt(s)}
    results = {"criteria": __doc__, "recipes": {}}
    for name, scale in recipes.items():
        print(f"{name}: calibration (10 trials per point)", flush=True)
        brain = ShiuBrain(trials=10, scale=scale)
        cells = {k: brain.cells(v, side="L") for k, v in SETS.items()}
        mn9 = np.concatenate([brain.cells(["MN9"], side="L"), brain.cells(["MN9"], side="R")])
        rec = results["recipes"][name] = {"calibration": calibrate(brain, cells["sugar"], mn9)}
        w = rec["calibration"]["w_syn"]
        OUT.write_text(json.dumps(results, indent=1))
        if w is None:
            print(f"{name}: sugar never reached MN9; nothing to test", flush=True)
            rec["pass"] = False
            continue
        print(f"{name}: calibrated w_syn = {w} mV; tests (30 trials)", flush=True)
        rec["tests"] = t = tests(ShiuBrain(w_syn=w, trials=30, scale=scale), cells, mn9)
        print(f"    {json.dumps(t)}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        print(f"{name}: nulls (10 trials each)", flush=True)
        rec["nulls"] = nulls(C, w, scale, cells["sugar"], mn9)
        rec["pass"] = bool(t["STABLE"] and t["SUGAR"] and rec["nulls"]["NULL"])
        print(f"{name}: PASS {rec['pass']}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
