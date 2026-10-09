"""Exploratory, not pre-registered: with ORN-to-PN synapses at their measured strength and Kenyon cells at their
measured distance below threshold (odor_probe3.py), two more measured properties: do odors then drive sparse Kenyon
cell responses?

odor_probe3.py: projection neurons now fire like a fly's (about 190 Hz in an odor's first 100 ms, 100 Hz over the
second), but no Kenyon cell rises by 5 Hz. Traced (not saved): at the odor's onset about a fifth of the Kenyon cells
cross 10 mV within 20 ms and fire together, APL's release then clamps them (to 22 mV below rest), and without APL the
response still dies within about 100 ms, because the PNs' synapses depress (0.85 of the strength left per spike, 0.8 s
to recover) to about 8% at 100 Hz. Two properties behind that differ from measurements:
  tau   Kenyon cells' membrane time constant is 20 ms here (Shiu's, for every neuron). Measured: about 185 ms in
        alpha/beta, 118-130 ms in alpha'/beta' and 125 ms in gamma (Groschner et al. 2018; Chen et al. 2026), over
        200 ms (Turner et al. 2008). Here: 150 ms for every Kenyon cell.
  PNKC  the PNs' depression is DM1-to-LHN1's (Kim et al. 2025), applied to all their synapses. No fly data exist for
        PN to KC, and in locusts that synapse shows neither depression nor facilitation (Jortner et al. 2007), while
        the same fly PN's synapses onto another LH neuron facilitate. Here: PN-to-KC synapses undepressed.
Conditions: odor_probe3.py's "ORN + KC" brain; plus tau; plus PNKC; plus both. In each, the Kenyon cells' rest is
set again to 21.5 mV below threshold, as in odor_probe3.py.
Odors, trials and measures as odor_probe3.py (seeds 9600 + 10 x condition + odor), plus APL's release (Hz) in the
odor's first 100 ms and over the second, which odor_probe3.py missed (APL is graded and never spikes).

Ran: the measured time constant alone makes the Kenyon cells sparse and odor-specific, but too quiet for the output
neurons to notice. Shares of Kenyon cells firing at least one extra spike, by odor (OCT, MCH, ethyl acetate,
isopentyl acetate, benzaldehyde, 2-heptanone), and MBON11's rate over the second (rest about 37 Hz):
  ORN + KC        35-52%, the same cells for every odor (Jaccard 1.0); APL 48-76 Hz in the first 100 ms; MBON11 38
  + tau           2.4-7.6% (4.4% OCT, 2.4% MCH); at most 1 cell rises by 5 Hz; APL 1-7 Hz; MBON11 38
  + PNKC          68-87% (56-82% rise by 5 Hz, at 28-41 Hz); APL 102-167 Hz; MBON11 51-54
  + tau + PNKC    72-88% (33-68% by 5 Hz, at 8-11 Hz); MBON11 51-56
The resting brain stays at 0.96-0.98 Hz with no neuron over 100 Hz in all four. With the time constant, the
onset burst is gone: a claw then gives about 4.5 mV at an odor's onset (190 Hz, depressing; estimated by hand, not
simulated), so about 5 coactive claws reach the 21.5 mV threshold, as Gruntman & Turner 2013 found (about 4 of 5-7). Undepressed PN synapses make
almost every Kenyon cell respond, and APL can't stop it. MBON11's synapses from Kenyon cells are near the one
measured value (alpha/beta KC to MBON-alpha2sc: 0.15 mV here, about 0.2 measured).
Checked afterwards (odor_probe7.py): the saved overlaps ("overlap_jaccard") are over the cells rising by 5 Hz, and with
the time constant there are almost none, so the overlap of 0.2 first reported for "+ tau" meant nothing; that run
can't say whether its responding cells were odor-specific. "About 37 to 57 Hz" isn't the flies' MBON11 response in the
pairing experiment: Hige et al. 2015 counted 118 +- 8.3 spikes above the spontaneous rate in the 1.4 s from 3-octanol's
onset.

    python experiments/odor_probe4.py          (writes experiments/odor_probe4.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import rung4_scaling as r4s
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
KC_TAU = 0.15


def set_kc_tau(b, kc: np.ndarray, tau: float) -> None:
    classes = np.unique(b.cls[kc])
    assert not np.isin(b.cls[~kc], classes).any(), "Kenyon cells share a parameter class with other neurons"
    for c in classes:
        b.params[c]["tau_m"] = tau
    b._tables_cache = None


def odor_trial(s, odor: str, seed: int, apl_pos: np.ndarray) -> dict:
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))
    drive = odors.orn_drive(b, odor, p3.MAX_HZ)
    counts, apl = np.zeros_like(rest), []
    onset = None
    for k in range(100):                                   # the odor's second in 10 ms pieces, sampling APL's release
        counts = counts + b.advance(int(round(0.01 / b.dt)), drive=drive)
        apl.append(float(b.release[:, apl_pos].mean()))
        if k == 9:
            onset = counts.copy()
    b.advance(int(round(1.0 / b.dt)))
    return {"rest": rest, "onset": onset, "odor": counts, "apl": [round(float(np.mean(apl[:10])), 1), round(float(np.mean(apl)), 1)]}


def condition(s, name: str, types: np.ndarray, m: dict, c: int) -> dict:
    p3.odor_trial = lambda s_, odor, seed: odor_trial(s_, odor, seed, APL_POS)
    out = p3.condition(s, name, types, m, c + 10)          # odor seeds 9500 + 10 x (c + 10) = 9600 + 10 c + odor
    return out


def main() -> None:
    global APL_POS
    t0 = time.perf_counter()
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    m = p3.masks(types)
    APL_POS = np.searchsorted(b.graded, np.flatnonzero(types == "APL"))
    orn_pn, pn_kc = p3.edges(b, m["orn"], m["upn"]), p3.edges(b, m["upn"], m["kc"])
    w = b.weights.copy()
    w[orn_pn] *= p3.UNITARY_MV / (p3.PEAK * float(w[orn_pn].mean()))
    b.weights, b._external_matrix = w.astype(np.float32), None
    bias0 = s.bias[s.gid].astype(np.float64)
    tau0 = b.params[b.cls[np.flatnonzero(m["kc"])[0]]]["tau_m"]
    out = {"question": __doc__, "conditions": {}, "kc_rest_calibration": {}}
    for c, (name, tau, pnkc) in enumerate((("ORN + KC", False, False), ("+ tau", True, False),
                                           ("+ PNKC", False, True), ("+ tau + PNKC", True, True))):
        set_kc_tau(b, m["kc"], KC_TAU if tau else tau0)
        b.full_strength[:] = pn_kc if pnkc else False
        bias = bias0.copy()
        b.set_bias(bias)
        out["kc_rest_calibration"][name] = p3.set_kc_rest(s, m["kc"], types, bias, 9680 + 10 * c)[-1]
        res = condition(s, name, types, m, c)
        out["conditions"][name] = res
        print(name, json.dumps(res["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
