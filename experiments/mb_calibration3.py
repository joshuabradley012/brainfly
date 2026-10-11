"""mb_calibration.py's mushroom body with APL's synapses onto the Kenyon cells acting as a conductance: their effect scales
with the Kenyon cell's distance from the synapses' reversal potential, so that however hard APL is driven it can't hold a
Kenyon cell past it, as flies' APL can't hold one more than 10-12 mV down (Inada et al. 2017).

mb_calibration2.py's graded APL meets flies' odor-graded APL and silencing ratio, but as a current its synapses hold the
Kenyon cells up to 27.5 mV down at APL's ceiling and 20 mV as 3-octanol begins (odor_apl_inhibition_check.py). Here
APL's synapses onto the Kenyon cells move from the fast current to the slow one, which HybridBrain lets a type give a
reversal potential (slow_reversal); the Kenyon cells' slow current gets the fast one's 5 ms time constant, so that at rest
APL acts on them exactly as before, and only the driving force (and keeping its current through a Kenyon cell's own
spike, which the fast current doesn't) differs. Then:
    reversal   the synapses' reversal potential, mV from rest (REVERSAL_MV)
    effect     APL's synapses onto the Kenyon cells, times mb_calibration.py's (APL_KC_EFFECT; at the ceiling they would
               hold a Kenyon cell 11 x effect mV down as a current, and as a conductance 11 x effect / (1 + 11 x effect /
               |reversal|))
    drive      the Kenyon cells' synapses onto APL, times their MaleCNS weight (KC_APL_DRIVE)
are odor_apl_conductance_check.py's: reversal -20 mV, effect 2.22 (so that APL's ceiling holds a quiet Kenyon cell 11 mV
down), drive 1.5. Then APL answers 4-methylcyclohexanol with 0.45 of its peak for 3-octanol (flies 0.49), silencing it
raises the Kenyon cells' spikes 2.92 and 2.21-fold (flies 2-3), and it holds them at most 7.1 mV down during an odor
(flies 15 at most; mb_calibration2.py 20.8).

    o, rec, built = brain_cache.load("odor_probe60", odor_probe60.build, odor_probe44.prepare)
    mb_calibration3.apply(o)
"""
from __future__ import annotations

import numpy as np
from scipy import sparse

import mb_calibration

TAU_FAST = 0.005                                   # brainfly.shiu.TAU, the fast current's time constant
REVERSAL_MV, KC_APL_DRIVE = -20.0, 1.5             # odor_apl_conductance_check.py's choice
CEILING_MV = -11.0                                  # APL's ceiling on a quiet Kenyon cell: Inada et al. 2017's 10-12, its middle
APL_KC_EFFECT = (abs(CEILING_MV) * abs(REVERSAL_MV)
                 / (abs(mb_calibration.KC_SATURATION_MV) * (abs(REVERSAL_MV) - abs(CEILING_MV))))     # 2.22


def ceiling_mv(effect: float, reversal: float) -> float:
    """Where APL at its ceiling holds a quiet Kenyon cell, mV from rest (negative): the current's -11 x effect mV, divided
    by the conductance's 1 + (11 x effect) / |reversal|."""
    shift = -mb_calibration.KC_SATURATION_MV * effect
    return -shift / (1.0 + shift / abs(reversal))


def add_slow_edges(b, pre: np.ndarray, post: np.ndarray, counts: np.ndarray, weights: np.ndarray) -> None:
    """Add slow synapses pre -> post (signed counts, weights in mV) to the brain's, keeping every existing slow synapse's
    weight, depression exemption (slow_full) and presynaptic inhibition flag."""
    old_pre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    old = {(int(i), int(j)): e for e, (i, j) in enumerate(zip(old_pre, b.sidx))}
    if any((int(i), int(j)) in old for i, j in zip(pre, post)):
        raise ValueError("a synapse to add is already slow")
    weights_old, full_old = b.slow_weights.copy(), b.slow_full.copy()
    pres = b._presynaptic
    flags_old = pres["slow"].copy() if pres is not None else None
    rows = np.concatenate([b.sidx, post]).astype(np.int64)
    cols = np.concatenate([old_pre, pre]).astype(np.int64)
    data = np.concatenate([b._slow_counts, counts]).astype(np.float32)
    b.set_slow(sparse.csc_matrix((data, (rows, cols)), shape=(b.n, b.n)))
    new_pre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    added = {(int(i), int(j)): float(w) for i, j, w in zip(pre, post, weights)}
    w = np.empty(len(b.sidx), np.float32)
    full = np.zeros(len(b.sidx), np.bool_)
    flags = np.zeros(len(b.sidx), np.bool_)
    for e, (i, j) in enumerate(zip(new_pre, b.sidx)):
        key = (int(i), int(j))
        if key in old:
            o = old[key]
            w[e], full[e] = weights_old[o], full_old[o]
            if flags_old is not None:
                flags[e] = flags_old[o]
        else:
            w[e] = added[key]
    b.slow_weights, b.slow_full = w, full
    if pres is not None:
        pres["slow"] = flags
    b.slow_graded_input[:] = 0.0                   # graded release along the new weights (set_slow used the counts')
    for q, i in enumerate(b.graded):
        for e in range(b.sptr[i], b.sptr[i + 1]):
            b.slow_graded_input[:, b.sidx[e]] += b.slow_weights[e] * b.release[:, q]


def apply(o, drive: float | None = None, effect: float | None = None, reversal: float | None = None) -> dict:
    """mb_calibration.apply; then the Kenyon cell-to-APL synapses at `drive` times their MaleCNS weight, and APL's
    synapses onto the Kenyon cells, `effect` times mb_calibration.py's, moved into the slow current, which in the Kenyon
    cells decays as the fast one does and reverses `reversal` mV from rest. Returns what was set."""
    drive = KC_APL_DRIVE if drive is None else drive
    effect = APL_KC_EFFECT if effect is None else effect
    reversal = REVERSAL_MV if reversal is None else reversal
    out = mb_calibration.apply(o)
    install(o, drive, effect, reversal)
    out.update({"kc_apl_scale": drive, "apl_kc_effect": effect, "apl_kc_reversal_mv": reversal,
                "ceiling_mv": round(ceiling_mv(effect, reversal), 2), "graded_apl": "mb_calibration3.py"})
    return out


def install(o, drive: float, effect: float, reversal: float, base_weights: np.ndarray | None = None) -> None:
    """The part of apply after mb_calibration.apply, from mb_calibration.py's weights (base_weights, or the brain's)."""
    b = o.brain
    apl = b.cells(["APL"])
    kc = np.flatnonzero(o.m["kc"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    w = (b.weights if base_weights is None else base_weights).copy()
    w[o.m["kc"][pre] & np.isin(b.idx, apl)] *= drive / mb_calibration.KC_APL_SCALE
    apl_kc = np.flatnonzero(np.isin(pre, apl) & o.m["kc"][b.idx])
    moved = w[apl_kc] * effect
    w[apl_kc] = 0.0
    b.weights, b._external_matrix = w, None
    if not hasattr(b, "_apl_slow_installed"):
        add_slow_edges(b, pre[apl_kc], b.idx[apl_kc], b._counts[apl_kc], moved)
        b._apl_slow_installed = True
    else:                                          # already slow: only their weights change
        spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
        lookup = {(int(i), int(j)): float(x) for i, j, x in zip(pre[apl_kc], b.idx[apl_kc], moved)}
        sw = b.slow_weights.copy()
        for e in np.flatnonzero(np.isin(spre, apl) & o.m["kc"][b.sidx]):
            sw[e] = lookup[(int(spre[e]), int(b.sidx[e]))]
        b.slow_weights = sw
    b.sets = {**b.sets, "kenyon_cells": kc}
    b.set_type("kenyon_cells", tau_slow=TAU_FAST, slow_reversal=float(reversal))
