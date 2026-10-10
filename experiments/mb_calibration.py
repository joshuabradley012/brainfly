"""The mushroom body's measured calibration, applied to a built antennal lobe model (odor_probe44.py's cache).

odor_probe47.py (superseding odor_probe46.py's single scale): each Kenyon cell class's (alpha/beta, alpha'/beta', gamma,
and the few MaleCNS types only as KC) uniglomerular PN synapses scaled so that one PN spike at one claw gives Turner et
al. 2008's 1.4 mV on average at the PNs' resting depression; each class's APL synapses scaled to APL's mean summed weight,
so that APL saturates every class alike (Inada et al. 2017); APL releasing from 3.5 mV above rest (the middle of
non-spiking insect interneurons' 2-5 mV), saturating where the Kenyon cells sit 11 mV down, its Kenyon cell synapses times
10 (fitted: silencing APL then raises the Kenyon cells' evoked spikes 2.44-fold, flies' 2-3, Lin et al. 2014 and Bergmann
et al. 2026). None of it changes the resting state (the Kenyon cells are silent at rest), so the antennal lobe's build
stands; odor_probe36.measure sets the Kenyon cells' rest again.

    o, rec, built = brain_cache.load("odor_probe44", odor_probe44.build, odor_probe44.prepare)
    mb_calibration.apply(o)
"""
from __future__ import annotations

import numpy as np

import odor_probe21 as p21

EPSP_MV, PN_REST_HZ = 1.4, 3.0                     # Turner et al. 2008; the PNs' resting target
APL_RELEASE_AT_MV, KC_SATURATION_MV, KC_APL_SCALE = 3.5, -11.0, 10.0
CLASSES = {"alpha/beta": "KCab", "alpha'/beta'": "KCa'b'", "gamma": "KCg"}


def classes(o) -> dict:
    """The three classes, and the Kenyon cells MaleCNS types as none of them ("other")."""
    out = {name: o.m["kc"] & np.char.startswith(o.types, prefix) for name, prefix in CLASSES.items()}
    out["other"] = o.m["kc"] & ~np.logical_or.reduce(list(out.values()))
    return out


def apply(o) -> dict:
    """The calibration on o's brain (weights replaced, APL's type changed); returns what was set."""
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc0, pn0 = np.flatnonzero(m["kc"])[0], np.flatnonzero(m["upn"])[0]
    kp, pp = b.params[b.cls[kc0]], b.params[b.cls[pn0]]
    t = np.arange(0, 0.1, 1e-5)
    tau_m, tau_s = kp["tau_m"], p21.TAU
    peak = float((tau_s / (tau_s - tau_m) * (np.exp(-t / tau_s) - np.exp(-t / tau_m))).max())
    left = 1.0 / (1.0 + PN_REST_HZ * pp["recovery"] * (1.0 - pp["depression"])) if pp["depression"] < 1 else 1.0
    kc = np.flatnonzero(m["kc"])
    apl_all = np.isin(pre, apl) & m["kc"][b.idx]
    target_apl = float(np.bincount(b.idx[apl_all], weights=b.weights[apl_all], minlength=b.n)[kc].mean())
    w = b.weights.copy()
    out = {"classes": {}}
    for name, sel in classes(o).items():
        pn_e = np.flatnonzero(m["upn"][pre] & sel[b.idx])
        k = EPSP_MV / (float(b.weights[pn_e].mean()) * peak * left)
        w[pn_e] *= k
        ap_e = np.flatnonzero(np.isin(pre, apl) & sel[b.idx])
        cells = np.flatnonzero(sel)
        a = target_apl / float(np.bincount(b.idx[ap_e], weights=b.weights[ap_e], minlength=b.n)[cells].mean())
        w[ap_e] *= a
        out["classes"][name] = {"pn_scale": round(k, 3), "apl_scale": round(a, 3), "cells": int(len(cells))}
    kc_apl = m["kc"][pre] & np.isin(b.idx, apl)
    w[kc_apl] *= KC_APL_SCALE
    b.weights, b._external_matrix = w, None
    max_hz = KC_SATURATION_MV / (target_apl * p21.TAU)
    b.set_type("APL", release_at=APL_RELEASE_AT_MV, max_release=max_hz)
    out.update({"kc_apl_scale": KC_APL_SCALE, "apl_release_at_mv": APL_RELEASE_AT_MV, "apl_max_hz": round(max_hz, 2)})
    return out
