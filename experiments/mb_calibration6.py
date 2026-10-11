"""The Kenyon cells' projection neuron input at its measured size, as kc_epsp_check.py's rule adopted it (2026-10-11).

kc_input_audit.py found the input a third stronger than meant. mb_calibration.py scaled each class's projection neuron
synapses to Turner et al. 2008's 1.4 mV "at the PNs' resting depression", dividing by the 0.735 of its strength a
depressing synapse keeps at 3 spikes/s. But the synapses are exempt from depression, so every spike gave 1.90 mV. Here,
after mb_calibration4.apply, each class's synapses are scaled so that one spike through its mean synapse gives 1.4 mV at
full strength, as the synapses run (kc_input_audit.response: the kernel's own step).
The Kenyon cells' 20 ms membrane, which they have had since odor_probe17.py's build (odor_probe4.set_kc_tau's 11.5 ms
is undone by any set_type), is set in their type, so that it shows in the model's types and no later table can change it.
kc_epsp_check.py: the cells then answer 3-octanol at 7.4% (flies about 12%; the rule's 6-25%), and silencing APL raises
both odors' spikes 2.8 and 2.0-fold (flies 2-3), so the rule stated before that run adopted it.

    import mb_calibration6
    mb_calibration6.apply(o)              # in place of mb_calibration4.apply(o); mb_calibration5.install(o) after the
                                          # MBON11 setup, as before
"""
from __future__ import annotations

import numpy as np

import kc_input_audit
import mb_calibration
import mb_calibration4

EPSP_MV, KC_TAU_M = 1.4, 0.020                  # Turner et al. 2008, at full strength; the model's membrane


def apply(o) -> dict:
    """mb_calibration4.apply, then correct; returns what was set."""
    out = mb_calibration4.apply(o)
    out.update(correct(o))
    return out


def correct(o) -> dict:
    """The Kenyon cells' membrane at KC_TAU_M in their type, and their projection neuron synapses at EPSP_MV per spike
    at full strength, on a model mb_calibration4.apply has set; returns what was set."""
    out = {}
    b, m = o.brain, o.m
    b.set_type("kenyon_cells", tau_m=KC_TAU_M)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    w = b.weights.copy()
    out["epsp"] = {}
    for name, sel in mb_calibration.classes(o).items():
        e = np.flatnonzero(m["upn"][pre] & sel[b.idx])
        if not len(e):
            continue
        c = int(b.cls[np.flatnonzero(sel)[0]])
        now = float(kc_input_audit.response(b, c, float(w[e].mean())).max())
        w[e] *= np.float32(EPSP_MV / now)
        out["epsp"][name] = {"before_mv": round(now, 3), "scale": round(EPSP_MV / now, 4)}
    b.weights, b._external_matrix = w, None
    out.update({"kc_epsp_mv_at_full_strength": EPSP_MV, "kc_tau_m_s": KC_TAU_M, "pn_kc_input": "mb_calibration6.py"})
    return out
