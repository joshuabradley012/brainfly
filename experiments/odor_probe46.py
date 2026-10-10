"""Exploratory, not pre-registered: with the PN-to-Kenyon cell synapses at their measured strength and APL's feedback
fitted again around them, do the Kenyon cells respond as flies' do?

odor_probe45.py: with APL's release starting 3.5 mV above rest, saturating where the Kenyon cells sit 11 mV down (38.3
Hz per APL), and the Kenyon cell-to-APL synapses times 10 (the scale nearest flies' 2-3-fold block effect: 2.22), APL
releases 8-17 Hz over an odor's first 100 ms and the Kenyon cells fall below flies' (0.5-2.1% respond, flies 6 +- 5%;
MBON11 gains 3 spikes). Their resting distance to threshold is measured (21.5 +- 5.6 mV; Turner et al. 2008), but the
PN-to-Kenyon cell synapse carries rung 4's size rule: one PN spike at one claw gives a median 0.89 mV EPSP (mean 0.96),
where flies' unitary claw EPSPs have a median of about 1.2 mV and a mean of about 1.5 (Gruntman & Turner 2013), and
spontaneous ones in vivo 1.4 +- 0.8 mV (Turner et al. 2008; Groschner et al. 2018: about 1.25 in alpha/beta-c)
(research_notes/Rung 9 learning data/kc_integration.md).
Model: odor_probe44.py's (its cache), settled starts (warm.tracking), every uniglomerular PN-to-Kenyon cell synapse
scaled so that the mean unitary EPSP (one PN spike through all its synapses onto one Kenyon cell, at the PN's resting
depression) is Turner et al.'s 1.4 mV; APL as odor_probe45.py sets it (release from 3.5 mV, at most 38.3 Hz), its
Kenyon cell synapses times s, the fit (stated before running) s from 5, 10 and 20 whose mean block ratio (as
odor_probe45.py measures it) is nearest 2.5.
Measured at the chosen s: everything odor_probe36.py measures, and the Kenyon cells' mean membrane potential over the
odor with APL working against silenced. Seeds 490000 (odor_probe45.py's offsets).

    python experiments/odor_probe46.py         (writes experiments/odor_probe46.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe45 as p45
import odor_probe7 as p7
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 490000
SCALES = (5.0, 10.0, 20.0)
EPSP_MV = 1.4                                      # Turner et al. 2008, spontaneous claw EPSPs in vivo
PN_REST_HZ = 3.0                                   # the PNs' resting target (odor_probe44.py rests them at 2.8-2.95)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    runner = p10.make_runner(rec)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    pn_kc = np.flatnonzero(m["upn"][pre] & m["kc"][b.idx])
    kc_apl = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, apl))
    kc0, pn0 = np.flatnonzero(m["kc"])[0], np.flatnonzero(m["upn"])[0]
    kp, pp = b.params[b.cls[kc0]], b.params[b.cls[pn0]]
    t = np.arange(0, 0.1, 1e-5)
    tau_m, tau_s = kp["tau_m"], p21.TAU
    peak = float((tau_s / (tau_s - tau_m) * (np.exp(-t / tau_s) - np.exp(-t / tau_m))).max())
    left = 1.0 / (1.0 + PN_REST_HZ * pp["recovery"] * (1.0 - pp["depression"])) if pp["depression"] < 1 else 1.0
    epsp = float(b.weights[pn_kc].mean()) * peak * left
    k = EPSP_MV / epsp
    out = {"question": __doc__, "kc_tau_m_s": tau_m, "epsp_peak_per_mv": round(peak, 4),
           "pn_depression": {"depression": pp["depression"], "recovery_s": pp["recovery"], "resting_strength": round(left, 3)},
           "unitary_epsp_mv_before": round(epsp, 3), "pn_kc_scale": round(k, 3), "apl": {"release_at_mv": p45.RELEASE_AT_MV},
           "sweep": {}}
    e = np.flatnonzero(np.isin(pre, apl) & m["kc"][b.idx])
    summed = np.bincount(b.idx[e], weights=b.weights[e], minlength=b.n)[np.flatnonzero(m["kc"])]
    max_hz = p45.KC_SATURATION_MV / (float(summed.mean()) * p21.TAU)
    out["apl"]["max_release_hz"] = round(max_hz, 2)
    print(f"unitary EPSP {epsp:.3f} mV (PN resting strength {left:.3f}) -> PN-to-KC synapses x {k:.3f}; APL max {max_hz:.1f} Hz", flush=True)
    w0 = b.weights.copy()
    w0[pn_kc] *= k
    with warm.tracking(o, rec):
        b.set_type("APL", release_at=p45.RELEASE_AT_MV, max_release=max_hz)
        for i, s in enumerate(SCALES):
            w = w0.copy()
            w[kc_apl] *= s
            b.weights, b._external_matrix = w, None
            row = {}
            for j, odor in enumerate(p7.ODORS):
                on = np.mean([p45.evoked_kc_spikes(o, rec, runner, odor, SEED + 100 * i + 10 * j + q, ()) for q in range(p45.SEEDS)])
                off = np.mean([p45.evoked_kc_spikes(o, rec, runner, odor, SEED + 100 * i + 10 * j + q, apl) for q in range(p45.SEEDS)])
                row[odor] = {"apl_on": round(float(on), 1), "apl_silenced": round(float(off), 1), "ratio": round(float(off / max(on, 1e-9)), 2)}
            ratios = [row[od]["ratio"] for od in row]
            out["sweep"][f"{s:g}"] = {"odors": row, "mean_ratio": round(float(np.mean(ratios)), 2)}
            print(f"s {s:g}: mean ratio {np.mean(ratios):.2f}", json.dumps({od[:6]: (r['apl_on'], r['apl_silenced']) for od, r in row.items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
        best = min(out["sweep"], key=lambda q: abs(out["sweep"][q]["mean_ratio"] - p45.TARGET_RATIO))
        out["chosen_scale"] = float(best)
        w = w0.copy()
        w[kc_apl] *= float(best)
        b.weights, b._external_matrix = w, None
        print("chosen s", best, flush=True)
        entry = {"kc_odor_v_mv": {}}
        for j, odor in enumerate(("3-octanol", "4-methylcyclohexanol")):
            on = p45.kc_odor_v(o, rec, odor, SEED + 700 + j, ())
            off = p45.kc_odor_v(o, rec, odor, SEED + 700 + j, apl)
            entry["kc_odor_v_mv"][odor] = {"apl_on": round(on, 3), "apl_silenced": round(off, 3), "difference": round(on - off, 3)}
        entry.update(p36.measure(o, rec, built, SEED))
        out["at_chosen_scale"] = entry
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
