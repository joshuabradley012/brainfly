"""mb_calibration.py's mushroom body with a graded APL: its drive from the Kenyon cells weaker and its synapses onto them
stronger, so that it answers each odor in proportion to its Kenyon cells instead of saturating for every odor.

mb_calibration.py multiplies the Kenyon cell-to-APL synapses by 10, fitted only to the rise in the Kenyon cells' spikes
when APL is silenced (2.44; flies 2-3), and APL then saturates for 3-octanol and 4-methylcyclohexanol alike
(odor_apl_check.py; 0.99 of 3-octanol's peak, flies' calcium 0.49, Prisco et al. 2021). odor_apl_two_knob_check.py: with
those synapses at 1.5 times their MaleCNS weight and APL's synapses onto the Kenyon cells at 2.5 times mb_calibration.py's
(its ceiling holding them 27.5 mV down), APL answers 4-methylcyclohexanol with 0.47 of its peak for 3-octanol, silencing
it raises the Kenyon cells' spikes 2.05-2.45-fold, and it equalizes the odors' Kenyon cells 1.29-fold (flies 1.25-fold).
Both numbers were fitted (a grid of six pairs on odor_probe60.py's model); the equalization is what they predict.
mb_calibration.py is unchanged, so the experiments that used it (rung9_learning.py among them) still run as they ran.

Checked afterwards (2026-10-11, odor_apl_conductance_check.py): with the Kenyon cells' rest set after installing this APL,
as the learning pilots do, silencing it raises their spikes 2.51 and 1.98-fold (3-octanol, 4-methylcyclohexanol).

    o, rec, built = brain_cache.load("odor_probe60", odor_probe60.build, odor_probe44.prepare)
    mb_calibration2.apply(o)
"""
from __future__ import annotations

import numpy as np

import mb_calibration

KC_APL_DRIVE, APL_KC_EFFECT = 1.5, 2.5          # odor_apl_two_knob_check.py


def apply(o) -> dict:
    """mb_calibration.apply, then the Kenyon cell-to-APL synapses at KC_APL_DRIVE times their MaleCNS weight (instead of
    mb_calibration.KC_APL_SCALE) and APL's synapses onto the Kenyon cells times APL_KC_EFFECT; returns what was set."""
    out = mb_calibration.apply(o)
    b = o.brain
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    w = b.weights.copy()
    w[o.m["kc"][pre] & np.isin(b.idx, apl)] *= KC_APL_DRIVE / mb_calibration.KC_APL_SCALE
    w[np.isin(pre, apl) & o.m["kc"][b.idx]] *= APL_KC_EFFECT
    b.weights, b._external_matrix = w, None
    out.update({"kc_apl_scale": KC_APL_DRIVE, "apl_kc_effect": APL_KC_EFFECT, "graded_apl": "mb_calibration2.py"})
    return out
