"""Audit, not a test and not a change to the model: the projection neuron-to-Kenyon cell input as the rung 9
experiments run it, against what their docstrings and research_notes/Rung 9 learning data/kc_integration.md assume and
what flies show.

Found while checking HybridBrain.set_type after a review (2026-10-11). The model is meant to have Turner et al.
2008's Kenyon cells (odor_probe5.py, odor_probe7.py's "+ undepressed outputs", the build's condition): EPSPs decaying in
11.5 ms and unitary inputs of 1.4 mV, the projection neuron synapses exempt from depression. mb_calibration.py then
scales each class's projection neuron synapses so that one spike gives Turner's 1.4 mV "at the PNs' resting
depression". kc_integration.md, kc_membrane_check.py and kc_setc_check.py took the model's unitary EPSP to be 1.24-1.4
mV. Two things undo that:
- odor_probe4.set_kc_tau sets the Kenyon cells' 11.5 ms by editing the parameter table directly. Any later
  HybridBrain.set_type rebuilds the table from the types, which don't carry it, and so puts back the default 20 ms. In
  odor_probe60.py's build that happens at odor_probe17.add_slow_receptor_synapses's set_type("uPN", ...) (a traced build,
  scratch). Shown here on the model itself: set_kc_tau, then a set_type that changes nothing, and the time constant is
  20 ms again.
- mb_calibration.py's "at the PNs' resting depression" divides by the strength a depressing synapse keeps at 3
  spikes/s (0.735), but the synapses are exempt from depression (full_strength), so they carry 1/0.735 of 1.4 mV at
  every spike.
Measured, from odor_probe60.py's cache after mb_calibration4.apply (as every learning pilot sets the model), for each
Kenyon cell class:
- the membrane time constant and the share of the projection neuron synapses exempt from depression;
- the unitary EPSP of one spike through the class's mean projection neuron synapse, from the kernel's own coefficients
  step by step (without APL's resting conductance, which shunts it by several percent), with its time to peak and its
  width at half the peak;
- the steady depolarization per connection at 40 and 115 spikes/s (the response's area times the rate).
Against flies: Turner et al. 2008, 1.4 mV and an 11.5 ms decay in vivo; Gruntman & Turner 2013, unitary EPSPs of
1.24-1.48 mV and about 4.4 mV per connection at 115 spikes/s (kc_integration.md section 1).

Ran (2026-10-11, 1 minute): the model's Kenyon cell input is a third stronger than meant.
- Every class has a 20 ms membrane, and 99.1-99.9% of its projection neuron synapses are exempt from depression.
- One spike through the mean synapse gives a 1.90 mV EPSP, peaking 9.2 ms after it and 26.5 ms wide at half its peak
  (Turner et al. 2008: 1.4 mV; Gruntman & Turner 2013: 1.24-1.48 mV).
- The steady drive per connection is 2.42 mV at 40 spikes/s and 6.95 mV at 115 (flies about 4.4 at 115).
- set_kc_tau sets the cells' 11.5 ms; a set_type that changes nothing puts back 20 ms. In every experiment the model
  gets one anyway: mb_calibration.apply's set_type("APL", ...).
So since odor_probe46.py the projection neuron input has been 1.36 times what mb_calibration.py meant and 1.3-1.5 times
flies' unitary EPSPs, at the default 20 ms membrane. kc_integration.md's "current model" (6.11 mV weights at 11.5 ms,
3.5 mV per connection at 115 spikes/s) never ran. kc_epsp_check.py runs the cells at the measured size.

Correction (2026-10-11, after a review):
- kc_integration.md's "current model" did run: probes 7-16 ran Turner's 11.5 ms with 6.11 mV weights. The revert came
  with odor_probe17.py's set_type, and every model since has run at 20 ms.
- The size error is entirely the depression division. mb_calibration.py measured its EPSP at the 20 ms membrane, so
  the revert changed the EPSP's time course, not its size.
- The mean synapse includes the GABAergic projection neurons' few Kenyon cell synapses (about 1-2%).

    python experiments/kc_input_audit.py      (writes experiments/kc_input_audit.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import brain_cache
import mb_calibration
import odor_probe4 as p4
import odor_probe44 as p44
import odor_probe5 as p5
import odor_probe60 as p60

OUT = Path(__file__).with_suffix(".json")
FLIES = {"turner2008": {"unitary_epsp_mv": 1.4, "epsp_decay_ms": 11.5},
         "gruntman_turner2013": {"unitary_epsp_mv": [1.24, 1.48], "plateau_mv_per_connection_at_115_hz": 4.4}}


def response(b, c: int, w: float, steps: int = 3000) -> np.ndarray:
    """One spike's EPSP in a neuron of class c through a synapse of weight w: the kernel's step (u <- a_vv u + a_vx x,
    x <- a_xx x) from x = w, with nothing else."""
    k = b._kernel_tables()
    a_vv, a_vx, a_xx = float(k["a_vv"][c]), float(k["a_vx"][c]), float(k["a_xx"])
    u, x, out = 0.0, w, np.empty(steps)
    for t in range(steps):
        u, x = a_vv * u + a_vx * x, a_xx * x
        out[t] = u
    return out


def main() -> None:
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    b, m = o.brain, o.m
    out = {"question": __doc__, "flies": FLIES, "kc_tau_in_cache_s": sorted({round(b.params[c]["tau_m"], 4) for c in np.unique(b.cls[m["kc"]])})}
    out["mb_calibration"] = mb_calibration4.apply(o)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    pn0 = np.flatnonzero(m["upn"])[0]
    pp = b.params[b.cls[pn0]]
    out["pn_depression"] = {"depression": pp["depression"], "recovery_s": pp["recovery"],
                            "strength_left_at_3_hz": round(1.0 / (1.0 + mb_calibration.PN_REST_HZ * pp["recovery"] * (1.0 - pp["depression"])), 4),
                            "mb_calibration_epsp_mv_at_resting_depression": mb_calibration.EPSP_MV}
    out["classes"] = {}
    for name, sel in mb_calibration.classes(o).items():
        e = np.flatnonzero(m["upn"][pre] & sel[b.idx])
        if not len(e):
            continue
        cs = np.unique(b.cls[np.flatnonzero(sel)])
        c = int(cs[0])
        w = float(b.weights[e].mean())
        r = response(b, c, w)
        t = (np.arange(len(r)) + 1) * b.dt
        j = int(np.argmax(r))
        above = np.flatnonzero(r >= r[j] / 2)
        area = float(r.sum() * b.dt)
        out["classes"][name] = {"cells": int(sel.sum()), "tau_m_s": sorted({round(b.params[x]["tau_m"], 4) for x in cs}),
                                "pn_synapses": int(len(e)), "full_strength_share": round(float(b.full_strength[e].mean()), 3),
                                "mean_weight_mv": round(w, 3), "unitary_epsp_mv": round(float(r[j]), 3),
                                "t_peak_ms": round(float(t[j]) * 1000, 2),
                                "half_width_ms": round(float((above[-1] - above[0] + 1) * b.dt) * 1000, 2),
                                "plateau_mv_at_40_hz": round(area * 40.0, 2), "plateau_mv_at_115_hz": round(area * 115.0, 2)}
        print(name, json.dumps(out["classes"][name]), flush=True)
    kc = m["kc"]
    held = b.types
    p4.set_kc_tau(b, kc, p5.KC_TAU)                     # odor_probe7's '+ undepressed outputs' does this
    set_to = sorted({round(b.params[c]["tau_m"], 4) for c in np.unique(b.cls[kc])})
    upn_key = "uPN" if "uPN" in b.types else next(iter(b.types))
    b.set_type(upn_key, **{k: v for k, v in b.types[upn_key].items() if k not in ("scale", "unit")})   # changes nothing
    after = sorted({round(b.params[c]["tau_m"], 4) for c in np.unique(b.cls[kc])})
    out["set_kc_tau_then_set_type"] = {"set_kc_tau_s": p5.KC_TAU, "tau_m_after_set_kc_tau_s": set_to,
                                       "set_type_called_on": upn_key, "tau_m_after_set_type_s": after}
    print("set_kc_tau then set_type:", json.dumps(out["set_kc_tau_then_set_type"]), flush=True)
    assert b.types == held
    OUT.write_text(json.dumps(out, default=float))


if __name__ == "__main__":
    main()
