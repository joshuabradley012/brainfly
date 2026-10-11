"""mb_calibration3.py's APL conductance, corrected: its reversal measured from each Kenyon cell's own resting potential,
and its time course flies' (constants: odor_apl_conductance2_check.py).

mb_calibration3.py set the Kenyon cells' slow_reversal to one value, which HybridBrain measures from the model's zero. But
the Kenyon cells don't rest there: odor_probe33.set_rest holds each class its measured distance below the shared 16 mV
threshold, so alpha'/beta' cells rest at 0, alpha/beta at -5.5 and gamma at -16.5 mV, and a reversal of -20 lay 20, 14.5
and 3.5 mV below them: APL could barely inhibit the gamma cells. Flies' classes differ in threshold more than in resting
potential (research_notes/Rung 9 learning data/kc_classes_and_apl.md), so the reversal should lie the same distance below
each class's rest. Here each Kenyon cell type's reversal is its rest (threshold less its gap, odor_probe8.class_gaps) plus
`reversal`, and its APL synapses are scaled by (its reversal / `reversal`), so that at rest every class takes the current
mb_calibration3.py's design gave it (the conductance's current is its slow current times (E - v) / E). Then APL's ceiling
holds a quiet Kenyon cell of any class mb_calibration3.ceiling_mv(effect, reversal) mV below its rest, as designed.
`tau`: the conductance's decay (research_notes/Rung 9 learning data/apl_kinetics.md: about 0.3 s in flies).

    o, rec, built = brain_cache.load("odor_probe60", odor_probe60.build, odor_probe44.prepare)
    mb_calibration4.apply(o)
"""
from __future__ import annotations

import numpy as np

import mb_calibration
import mb_calibration3
import odor_probe8 as p8

REVERSAL_MV, APL_KC_EFFECT, KC_APL_DRIVE, TAU_S = None, None, None, None     # odor_apl_conductance2_check.py


def class_reversals(o, reversal: float) -> dict:
    """Each Kenyon cell type's reversal in the model's units: its rest (the threshold less its gap) plus `reversal`."""
    b, kc = o.brain, np.flatnonzero(o.m["kc"])
    threshold = b.params[b.cls[kc[0]]]["threshold"]
    return {str(t): threshold - gap + reversal for t, gap in p8.class_gaps(o, None).items()}


def install(o, drive: float, effect: float, reversal: float, base_weights: np.ndarray, tau: float) -> dict:
    """mb_calibration3.install, then each Kenyon cell type's reversal set from its rest and its APL synapses scaled to
    match; returns the reversals used."""
    mb_calibration3.install(o, drive, effect, reversal, base_weights, tau=tau)
    b = o.brain
    rev = class_reversals(o, reversal)
    apl = b.cells(["APL"])
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    onto = np.isin(spre, apl) & o.m["kc"][b.sidx]
    sw = b.slow_weights.copy()
    types = o.types
    sets = dict(b.sets)
    for t in rev:                                  # named sets, so that they come after mb_calibration3's in b.types
        sets[f"apl reversal {t}"] = np.flatnonzero(types == t)
    b.sets = sets
    for t, e in rev.items():
        sw[onto & (types[b.sidx] == t)] *= e / reversal
        b.set_type(f"apl reversal {t}", tau_slow=float(tau), slow_reversal=float(e))
    b.slow_weights = sw
    return {t: round(e, 2) for t, e in rev.items()}


def apply(o) -> dict:
    """mb_calibration.apply, then install with the module's constants; returns what was set."""
    out = mb_calibration.apply(o)
    rev = install(o, KC_APL_DRIVE, APL_KC_EFFECT, REVERSAL_MV, o.brain.weights.copy(), TAU_S)
    out.update({"kc_apl_scale": KC_APL_DRIVE, "apl_kc_effect": APL_KC_EFFECT, "apl_kc_reversal_mv_from_rest": REVERSAL_MV,
                "apl_kc_reversal_mv_by_type": rev, "apl_kc_tau_s": TAU_S,
                "ceiling_mv": round(mb_calibration3.ceiling_mv(APL_KC_EFFECT, REVERSAL_MV), 2), "graded_apl": "mb_calibration4.py"})
    return out
