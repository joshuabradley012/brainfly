"""Exploratory, not pre-registered: with every Kenyon cell class's PN synapses and APL inhibition at the measured,
class-independent strengths, do the classes respond in flies' order?

odor_probe46.py: with the PN-to-Kenyon cell synapses doubled to Turner et al.'s 1.4 mV unitary EPSP on average and APL
fitted to flies' block effect, the Kenyon cells respond in flies' range, but the classes in the wrong order: to
3-octanol alpha/beta 17.2%, gamma 9.8%, alpha'/beta' 6.8%, where flies' alpha'/beta' respond most (9-14%), alpha/beta 3-8%
and gamma about 2%. The scale was one for all classes, and rung 4's size rule makes each class's synapses different:
the median alpha'/beta' cell gets 44 (alpha/beta 75, gamma 69) of summed PN weight and -70 (-51, -60) of APL weight, so
APL would saturate them at -13 mV against alpha/beta's -10, where Inada et al. 2017 found APL's saturation the same for
alpha/beta, alpha'/beta' and gamma cells. The unitary claw EPSP is measured only for unclassified cells (Turner: 1.4 mV)
and alpha/beta-c (Groschner et al. 2018: about 1.25 mV), alike (research_notes/Rung 9 learning data/kc_integration.md);
the classes' thresholds differ (Inada's offsets, already in the model).
Model: odor_probe44.py's (its cache), settled starts, with each class's (alpha/beta, alpha'/beta', gamma) uniglomerular
PN-to-Kenyon cell synapses scaled so that its mean unitary EPSP at the PNs' resting depression is 1.4 mV, each class's
APL-to-Kenyon cell synapses scaled so that its mean summed APL weight is the population's (so that APL saturates every
class at -11 mV, at 38.3 Hz), APL releasing from 3.5 mV, and its Kenyon cell synapses times s, the fit (stated before
running) s from 10, 20 and 40 whose mean block ratio is nearest 2.5 (odor_probe45.py's measure).
Measured at the chosen s: everything odor_probe36.py measures, and the Kenyon cells' mean membrane potential over the
odor with APL working against silenced. Seeds 500000 (odor_probe45.py's offsets).

Ran: the alpha'/beta' cells now respond most, as in flies, but the gamma cells nearly as much, where flies' respond
least. At the PNs' resting depression the classes' unitary claw EPSPs were 0.85 (alpha/beta), 0.56 (alpha'/beta') and
0.61 mV (gamma), so their PN synapses are scaled x 1.66, 2.52 and 2.29 (2 cells MaleCNS types only as KC, x 0.30); APL's
synapses x 1.13, 0.83 and 0.96 to give every class APL's mean summed weight (-57.5 mV per Hz, saturating at 38.3 Hz).
The block ratio is 2.44 with s = 10 (chosen), 2.69 with 20 and 2.87 with 40. To 3-octanol alpha/beta cells respond at
9.0%, alpha'/beta' at 17.7% and gamma at 15.5% (flies, at Hige et al.'s stimulus, about 6, 20 and 3.5%: research_notes/Rung
9 learning data/mbon11_kc_activity.md; Turner et al. 2008: alpha'/beta' 9-14%, alpha/beta 3-8%, gamma about 2%), and
across six odors alpha'/beta' 4.6-21.3%, alpha/beta 2.4-13.8%, gamma 5.4-15.7%; all Kenyon cells 3.9-14.7% (flies
6 +- 5%), mean Jaccard 0.18. The responding cells fire 1.7-3.2 spikes per response (alpha/beta; flies 2.2), 2.6-4.4
(alpha'/beta'; flies 4.9) and 1.5-2.2 (gamma). APL releases 20-23 Hz over an odor's first 100 ms. MBON11 gains 40 spikes
to 3-octanol from 205 pC per cell (flies 118 from about 250) and 18 to 4-methylcyclohexanol from 64 pC (flies 110 from
about 265); 4-methylcyclohexanol reaches 0.30 as many Kenyon cells as 3-octanol (flies 0.73-0.92). Inada et al.'s gamma
offset (+2.5 mV) is the low end of the measured range: Chen et al. 2026 found gamma cells' threshold 11 mV above alpha/beta
cells', Turner's gamma cells almost never spiked to odors (1 of 15), and Inada's fired least above threshold.

    python experiments/odor_probe47.py         (writes experiments/odor_probe47.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import mb_calibration as mbc
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe45 as p45
import odor_probe46 as p46
import odor_probe7 as p7
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 500000
SCALES = (10.0, 20.0, 40.0)
CLASSES = {"alpha/beta": "KCab", "alpha'/beta'": "KCa'b'", "gamma": "KCg"}


def classes(o) -> dict:
    """The three classes, and the Kenyon cells MaleCNS types as none of them ("other"), equalized alike."""
    types = o.types
    out = {name: o.m["kc"] & np.char.startswith(types, prefix) for name, prefix in CLASSES.items()}
    out["other"] = o.m["kc"] & ~np.logical_or.reduce(list(out.values()))
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    runner = p10.make_runner(rec)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, apl))
    kc0, pn0 = np.flatnonzero(m["kc"])[0], np.flatnonzero(m["upn"])[0]
    kp, pp = b.params[b.cls[kc0]], b.params[b.cls[pn0]]
    t = np.arange(0, 0.1, 1e-5)
    tau_m, tau_s = kp["tau_m"], p21.TAU
    peak = float((tau_s / (tau_s - tau_m) * (np.exp(-t / tau_s) - np.exp(-t / tau_m))).max())
    left = 1.0 / (1.0 + p46.PN_REST_HZ * pp["recovery"] * (1.0 - pp["depression"])) if pp["depression"] < 1 else 1.0
    w0 = b.weights.copy()
    apl_all = np.flatnonzero(np.isin(pre, apl) & m["kc"][b.idx])
    kc = np.flatnonzero(m["kc"])
    target_apl = float(np.bincount(b.idx[apl_all], weights=b.weights[apl_all], minlength=b.n)[kc].mean())
    per = {}
    for name, sel in classes(o).items():
        pn_e = np.flatnonzero(m["upn"][pre] & sel[b.idx])
        epsp = float(b.weights[pn_e].mean()) * peak * left
        k = p46.EPSP_MV / epsp
        w0[pn_e] *= k
        ap_e = np.flatnonzero(np.isin(pre, apl) & sel[b.idx])
        cells = np.flatnonzero(sel)
        summed = float(np.bincount(b.idx[ap_e], weights=b.weights[ap_e], minlength=b.n)[cells].mean())
        a = target_apl / summed
        w0[ap_e] *= a
        per[name] = {"cells": int(len(cells)), "unitary_epsp_mv_before": round(epsp, 3), "pn_scale": round(k, 3),
                     "apl_summed_mv_before": round(summed, 2), "apl_scale": round(a, 3)}
    max_hz = p45.KC_SATURATION_MV / (target_apl * p21.TAU)
    out = {"question": __doc__, "per_class": per, "apl": {"release_at_mv": mbc.APL_RELEASE_AT_MV, "max_release_hz": round(max_hz, 2),
                                                          "summed_mv": round(target_apl, 2)}, "sweep": {}}
    print("per class", json.dumps(per), f"APL max {max_hz:.1f} Hz", flush=True)
    with warm.tracking(o, rec):
        b.set_type("APL", release_at=mbc.APL_RELEASE_AT_MV, max_release=max_hz)
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
        print("by class", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
