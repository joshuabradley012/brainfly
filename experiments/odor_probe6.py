"""Exploratory, not pre-registered: odor_probe5.py's Turner brain with Kenyon cell to MBON synapses undepressed. Does
MBON11 then answer odors as a fly's does?

odor_probe5.py: with Turner et al. 2008's input stage, 13-33% of Kenyon cells fire at least one extra spike per odor
(flies: 6 +- 5%), alpha/beta cells 3.6-7.1 spikes per response (flies: 2.2 +- 1.2), and MBON11 rises only 2.5-4 Hz.
Kenyon cells' outputs depress here (0.5 of the strength left per spike,
1.5 s), derived from gamma KC to MBON-gamma1pedc paired-pulse ratios ex vivo with optogenetics (Yamada et al. 2024),
which the notes flag as possibly inflated by fewer KC spikes on the second pulse; in vivo, MBON-gamma1pedc's odor EPSCs
are "sustained throughout the duration of the odor pulse" (Hige et al. 2015). Here every Kenyon cell to MBON synapse is
undepressed (Kenyon cells' other outputs keep the depression); odor_probe5.py's model and measures otherwise, seeds
9900 + odor (condition index 40 in odor_probe3.condition).

Ran: MBON11 now moves, by much less than a fly's. Its rate over the odor's second rises 5.1-16.6 Hz above rest (MCH
5.1, OCT 7.5, ethyl acetate 16.6), MBON18's 4.1-29.8 and MBON01's 2.3-12.8. The Kenyon cells respond as in
odor_probe5.py (13-33% with at least one extra spike, 2-12% rising by 5 Hz), and the resting brain stays at 0.96 Hz
with no neuron over 100 Hz.
Checked afterwards (odor_probe7.py): the flies' figure first set beside this, "about 37 to 57 Hz", combined a resting
rate from voltage imaging with an onset rate read off a figure of 15 s odors. In the pairing experiment, Hige et al.
2015 counted 118 +- 8.3 spikes above the spontaneous rate in the 1.4 s from 3-octanol's onset (110 +- 11 for MCH):
about 84 a second, five to sixteen times MBON11's rise here. And the ORN-to-PN factor should be 7.3, not 8.8 (see
odor_probe3.py). And DoOR's responses here include each receptor's spontaneous level (DoOR's SFR row, 0-0.2 of its strongest
response), which brainfly.odors now subtracts, as DoOR's own reset_sfr does; so every glomerulus was driven harder
than its odor drives it, and receptors at or below their spontaneous rate were driven too (odor_probe7.py reruns
the current model without this).

    python experiments/odor_probe6.py          (writes experiments/odor_probe6.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe4 as p4
import odor_probe5 as p5
import rung4_scaling as r4s

OUT = Path(__file__).with_suffix(".json")


def build():
    """odor_probe6.py's brain: (setup, types, masks, the KC-to-MBON edges), Kenyon cells' rest set (seed 9980)."""
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    m = p3.masks(types)
    p4.APL_POS = np.searchsorted(b.graded, np.flatnonzero(types == "APL"))
    mbon = np.char.startswith(types, "MBON")
    orn_pn, pn_kc, kc_mbon = p3.edges(b, m["orn"], m["upn"]), p3.edges(b, m["upn"], m["kc"]), p3.edges(b, m["kc"], mbon)
    w = b.weights.copy()
    w[orn_pn] *= p3.UNITARY_MV / (p3.PEAK * float(w[orn_pn].mean()))
    w[pn_kc] *= p5.KC_UNITARY_MV / (p5.peak(p5.KC_TAU) * float(w[pn_kc].mean()))
    b.weights, b._external_matrix = w.astype(np.float32), None
    p4.set_kc_tau(b, m["kc"], p5.KC_TAU)
    b.full_strength[:] = pn_kc | kc_mbon
    bias = s.bias[s.gid].astype(np.float64)
    b.set_bias(bias)
    calibration = p3.set_kc_rest(s, m["kc"], types, bias, 9980)[-1]
    return s, types, m, kc_mbon, calibration


def main() -> None:
    t0 = time.perf_counter()
    s, types, m, kc_mbon, calibration = build()
    out = {"question": __doc__, "kc_mbon_connections": int(kc_mbon.sum()), "kc_rest_calibration": calibration}
    out["condition"] = p4.condition(s, "Turner, KC-MBON undepressed", types, m, 30)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
