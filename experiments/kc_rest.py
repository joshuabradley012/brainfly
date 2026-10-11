"""The Kenyon cells' rest set to each type's distance below threshold so that it holds whatever their membrane time
constant and input: odor_probe33.set_rest made to converge.

odor_probe33.set_rest moves each Kenyon cell type's bias by its mean resting potential's distance from the target, in
two passes, and then measures the result. After a change to the cells' membrane time constant and the projection neuron
synapses' strength it left them resting 1.5-23 mV closer to threshold than the targets (kc_membrane_check.py's 50 and
100 ms, kc_setc_check.py's sets C and D, learning_pilot13.py; found by review, 2026-10-11), for two reasons:
- HybridBrain.set_bias bakes each type's time constant into the share of the bias added each step, and set_type doesn't
  update it, so the first pass measured the cells with the old 20 ms share. At 50 ms that share holds the cells at about
  2.5 times their bias, and at 189 ms about 9.5 times. The pass's correction then overshot, and one more pass was left
  to undo it.
- Cells pushed into firing hold their mean potential near threshold whatever their bias, so the step creeps (set D:
  still 8 spikes/s and 15 mV off after seven more passes).
Here the share follows the current time constant before the first pass. The passes then set the cells' free membrane
potential (their threshold out of reach), which moves one for one with the bias, until each class's mean is within
TOL_MV of its target (at most PASSES passes). The rest is then measured with the cells firing, as odor_probe33.set_rest
measures it, and returned in its format with the passes' log added.
"""
from __future__ import annotations

import json

import numpy as np

import odor_probe10 as p10
import odor_probe7 as p7

PASSES, TOL_MV = 4, 0.3
OUT_OF_REACH_MV = 1.0e4


def _types_back(b, types: dict) -> None:
    """The type table exactly as it was (HybridBrain.set_type's own steps, with the synapse scales kept)."""
    scale = b.scale.copy()
    b.types = types
    b._tables()
    b.scale = scale
    b._tables_cache = None


def fit(o, rec, gaps: dict, seed: int) -> dict:
    """Each Kenyon cell type's mean resting potential at threshold minus gaps[type] (mV), with spontaneous receptor
    firing (odor_probe10.resting); returns the realized distances, the classes' resting rates and the passes."""
    b, kc, types = o.brain, o.m["kc"], o.types
    threshold = b.params[b.cls[np.flatnonzero(kc)[0]]]["threshold"]
    if np.any(np.array([p["threshold"] for p in b.params])[b.cls[kc]] != threshold):
        raise RuntimeError("the Kenyon cell types' thresholds differ")
    by_class = {name: np.char.startswith(types, prefix) & kc for name, prefix in p7.CLASSES.items()}
    target = np.full(b.n, np.nan)
    for t, gap in gaps.items():
        target[types == t] = threshold - gap
    bias = o.own_bias()
    b.set_bias(bias)                                      # the share of the bias each step follows the time constants now
    held = b.types
    b.set_type("kenyon_cells", threshold=OUT_OF_REACH_MV)
    log = []
    try:
        for r in range(PASSES):
            u = p10.resting(o, rec, seed + r, sample=True)["u"]
            off = {name: round(float((target[mask] - u[mask]).mean()), 3) for name, mask in by_class.items()}
            worst = max(abs(float(target[types == t].mean() - u[types == t].mean())) for t in gaps)
            log.append({"pass": r, "class_off_mv": off, "worst_type_off_mv": round(worst, 3)})
            if all(abs(v) <= TOL_MV for v in off.values()):
                break
            for t in gaps:
                mask = types == t
                bias[mask] += float((target[mask] - u[mask]).mean())
            b.set_bias(bias)
    finally:
        _types_back(b, held)
    rest = p10.resting(o, rec, seed + PASSES, sample=True)
    out = {"gap_mv": {t: round(float(threshold - rest["u"][types == t].mean()), 2) for t in gaps},
           "rest_hz_by_class": {name: round(float(rest["hz"][mask].mean()), 4) for name, mask in by_class.items()},
           "passes": log, "converged": bool(all(abs(v) <= TOL_MV for v in log[-1]["class_off_mv"].values()))}
    print("Kenyon cells' distance below threshold:", json.dumps(out), flush=True)
    return out
