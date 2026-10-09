"""Exploratory, not pre-registered: Kenyon cells built from Turner et al. 2008's measurements. Do odors then drive the
sparse responses flies show, and does MBON11 hear them?

odor_probe4.py gave Kenyon cells a 150 ms membrane time constant (somatic measurements) and found them sparse but too
quiet. Turner, Bazhenov & Laurent 2008 (J Neurophysiol 99:734) measured the rest of the input stage in vivo:
  - EPSPs are fast although the soma's time constant is over 200 ms: 10-90% rise 2.1 +- 0.5 ms, decay 11.5 +- 5.3 ms,
    "determined mostly by synaptic (and possibly, voltage-gated) conductances in the dendrites". In this model a
    neuron's membrane time constant is what sets its EPSP's decay, so the Kenyon cells get 11.5 ms.
  - unitary EPSPs of 1.4 mV (mean; median 1.2), from the distribution of spontaneous EPSPs; here 3.3 mV for the mean
    PN-to-KC connection (with a 20 ms membrane).
  - resting 21.5 +- 5.6 mV below threshold (odor_probe3.py's calibration), and about 10 PNs per Kenyon cell.
  - a passive model built from these numbers, driven by recorded PN odor responses with no synaptic depression,
    responded in 6% of model Kenyon cells, as the real ones did.
Measured in flies, as predictions here: a given odor evoked spikes in 6 +- 5% of Kenyon cells (71 cells, 10 odors
each; a response is a rate 3.5 SD over baseline within 2 s); responses "closely followed the stimulus time course";
alpha/beta Kenyon cells fired 2.2 +- 1.2 spikes per response and alpha'/beta' ones 4.9 +- 3.0. And MBON11 (Hige et al.
2015): high rates "that persisted throughout the duration of the 1-s odor pulse", rising from about 37 Hz to about 57.
Model: odor_probe3.py's ORN + KC brain (ORN-to-PN at 6.19 mV per connection; Kenyon cells 21.5 mV below threshold),
and every Kenyon cell's membrane time constant 11.5 ms, the PN-to-KC weights times one factor so that the mean
connection's peak PSP is 1.4 mV, then the Kenyon cells' rest set again to 21.5 mV below threshold. Conditions:
  Turner     PN-to-KC synapses undepressed, as in Turner's model (no fly data; none in locusts, Jortner et al. 2007);
  depressed  PN-to-KC synapses keeping the PNs' depression (0.85 left per spike, 0.8 s), as in rung 4's brain.
Odors, trials and measures as odor_probe4.py (seeds 9700 + 10 x condition + odor); a responding Kenyon cell is one
firing at least one spike more in the odor's second than in the second of rest before it, in at least half the flies.
Also reported: spikes per response by Kenyon cell class (the mean extra spikes of the responding cells).

Ran: close on the input stage, wrong on the output. The mean PN-to-KC connection went from 3.41 to 1.4 mV (times
0.28). Turner: 13-33% of Kenyon cells fire at least one extra spike per odor (MCH 13%, OCT 23%, ethyl acetate 33%;
flies: 6 +- 5%), and 2-12% rise by more than 5 Hz. The cells rising by 5 Hz differ partly between odors (Jaccard 0.44
on average; OCT and MCH 0.34). Spikes per response come out the wrong way round: alpha/beta 3.6-7.1 (flies: 2.2 +- 1.2),
alpha'/beta' 1.3-1.6 (flies: 4.9 +- 3.0), gamma 2.6-5.2. APL releases 12-42 Hz in the first 100 ms. MBON11 rises
2.5-4.3 Hz and MBON18 1-8 Hz (Hige et al. 2015's flies: 118 +- 8.3 spikes above the spontaneous rate in the 1.4 s
from 3-octanol's onset, about 84 a second; "about 20 Hz", used here at first, wasn't that experiment's measure). With the PNs' depression (depressed), 1.7-2.6% of Kenyon cells
respond, with under one extra spike, and the MBONs don't move. The resting brain stays at 0.97 Hz either way.

    python experiments/odor_probe5.py          (writes experiments/odor_probe5.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe4 as p4
import rung4_scaling as r4s

OUT = Path(__file__).with_suffix(".json")
KC_TAU, KC_UNITARY_MV = 0.0115, 1.4


def peak(tau_m: float, tau_s: float = 0.005) -> float:
    """Peak PSP per unit weight: a current decaying with tau_s into a membrane with tau_m."""
    t = np.linspace(0, 0.1, 100001)
    return float((tau_s / (tau_s - tau_m) * (np.exp(-t / tau_s) - np.exp(-t / tau_m))).max())


def main() -> None:
    t0 = time.perf_counter()
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    m = p3.masks(types)
    p4.APL_POS = np.searchsorted(b.graded, np.flatnonzero(types == "APL"))
    orn_pn, pn_kc = p3.edges(b, m["orn"], m["upn"]), p3.edges(b, m["upn"], m["kc"])
    w = b.weights.copy()
    w[orn_pn] *= p3.UNITARY_MV / (p3.PEAK * float(w[orn_pn].mean()))
    before = peak(0.02) * float(w[pn_kc].mean())
    factor = KC_UNITARY_MV / (peak(KC_TAU) * float(w[pn_kc].mean()))
    w[pn_kc] *= factor
    b.weights, b._external_matrix = w.astype(np.float32), None
    p4.set_kc_tau(b, m["kc"], KC_TAU)
    bias0 = s.bias[s.gid].astype(np.float64)
    out = {"question": __doc__, "pn_kc": {"connections": int(pn_kc.sum()), "peak_mv_before": round(before, 2),
                                          "factor": round(factor, 3), "peak_per_weight_11.5ms": round(peak(KC_TAU), 4)},
           "conditions": {}, "kc_rest_calibration": {}}
    print(json.dumps(out["pn_kc"]), flush=True)
    for c, (name, undepressed) in enumerate((("Turner", True), ("depressed", False))):
        b.full_strength[:] = pn_kc if undepressed else False
        bias = bias0.copy()
        b.set_bias(bias)
        out["kc_rest_calibration"][name] = p3.set_kc_rest(s, m["kc"], types, bias, 9780 + 10 * c)[-1]
        out["conditions"][name] = p4.condition(s, name, types, m, c + 10)     # odor seeds 9700 + 10 c + odor
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
