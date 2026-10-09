"""Exploratory, not pre-registered: odor_probe5.py's Turner brain with Kenyon cell to MBON synapses undepressed. Does
MBON11 then answer odors as a fly's does?

odor_probe5.py: with Turner et al. 2008's input stage, 13-33% of Kenyon cells fire at least one extra spike per odor
(flies: 6 +- 5%), alpha/beta cells 3.6-7.1 spikes per response (flies: 2.2 +- 1.2), and MBON11 rises only 2.5-4 Hz
(flies: about 37 to 57 Hz, Hige et al. 2015). Kenyon cells' outputs depress here (0.5 of the strength left per spike,
1.5 s), derived from gamma KC to MBON-gamma1pedc paired-pulse ratios ex vivo with optogenetics (Yamada et al. 2024),
which the notes flag as possibly inflated by fewer KC spikes on the second pulse; in vivo, MBON-gamma1pedc's odor EPSCs
are "sustained throughout the duration of the odor pulse" (Hige et al. 2015). Here every Kenyon cell to MBON synapse is
undepressed (Kenyon cells' other outputs keep the depression); odor_probe5.py's model and measures otherwise, seeds
9900 + odor (condition index 40 in odor_probe3.condition).

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


def main() -> None:
    t0 = time.perf_counter()
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
    out = {"question": __doc__, "kc_mbon_connections": int(kc_mbon.sum()),
           "kc_rest_calibration": p3.set_kc_rest(s, m["kc"], types, bias, 9980)[-1]}
    out["condition"] = p4.condition(s, "Turner, KC-MBON undepressed", types, m, 30)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
