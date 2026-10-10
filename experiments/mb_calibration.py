"""The mushroom body's measured calibration, applied to a built antennal lobe model (odor_probe44.py's cache).

odor_probe46.py: the uniglomerular PN-to-Kenyon cell synapses doubled (x 1.995), so that one PN spike at one claw gives
Turner et al. 2008's 1.4 mV at the PNs' resting depression; APL releasing from 3.5 mV above rest (the middle of
non-spiking insect interneurons' 2-5 mV), saturating at 38.3 Hz per APL (where the Kenyon cells sit 11 mV down, Inada et
al. 2017), its Kenyon cell synapses times 20 (fitted: silencing APL then raises the Kenyon cells' evoked spikes 2.48-fold,
flies' 2-3, Lin et al. 2014 and Bergmann et al. 2026). Neither changes the resting state (the Kenyon cells are silent at
rest), so the antennal lobe's build stands; odor_probe36.measure sets the Kenyon cells' rest again.

    o, rec, built = brain_cache.load("odor_probe44", odor_probe44.build, odor_probe44.prepare)
    mb_calibration.apply(o)
"""
from __future__ import annotations

import numpy as np

PN_KC_SCALE = 1.995
APL_RELEASE_AT_MV, APL_MAX_HZ, KC_APL_SCALE = 3.5, 38.29, 20.0


def apply(o) -> dict:
    """The calibration on o's brain (weights replaced, APL's type changed); returns what was set."""
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    pn_kc = m["upn"][pre] & m["kc"][b.idx]
    kc_apl = m["kc"][pre] & np.isin(b.idx, apl)
    w = b.weights.copy()
    w[pn_kc] *= PN_KC_SCALE
    w[kc_apl] *= KC_APL_SCALE
    b.weights, b._external_matrix = w, None
    b.set_type("APL", release_at=APL_RELEASE_AT_MV, max_release=APL_MAX_HZ)
    return {"pn_kc_scale": PN_KC_SCALE, "kc_apl_scale": KC_APL_SCALE, "apl_release_at_mv": APL_RELEASE_AT_MV,
            "apl_max_hz": APL_MAX_HZ, "pn_kc_edges": int(pn_kc.sum()), "kc_apl_edges": int(kc_apl.sum())}
