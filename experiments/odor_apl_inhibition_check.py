"""Exploratory check, not pre-registered: how far does the model's APL hold the Kenyon cells down during an odor, with
mb_calibration.py's APL and with mb_calibration2.py's, against what flies' APL can do?

odor_apl_two_knob_check.py's graded APL (mb_calibration2.py) meets flies' odor-graded APL (4-methylcyclohexanol 0.47 of
3-octanol's peak, flies 0.49) and silencing ratio (2.05-2.45, flies 2-3) with APL's synapses onto the Kenyon cells 2.5
times mb_calibration.py's, so that APL's ceiling holds them 27.5 mV down. In flies, driving APL optogenetically
hyperpolarizes every Kenyon cell tested, saturating at about 10-12 mV (Inada et al. 2017, ex vivo); driving about 160
alpha/beta-c Kenyon cells inhibits others through APL by 5.5-7.5 mV on average and up to 15 (Vrontou et al. 2021, in
vivo; research_notes/Rung 9 learning data/kc_classes_and_apl.md). Neither is an odor response; together they bound
what APL can do.
Model: odor_probe60.py's (its cache) with mb_calibration.py's mushroom body, the Kenyon cells' rest as the learning
pilots set it (as odor_apl_two_knob_check.py), then APL as calibrated (Kenyon cell-to-APL synapses at 10 times MaleCNS's,
its synapses onto the Kenyon cells as calibrated) and as mb_calibration2.py sets it (1.5 times; 2.5 times).
odor_apl_check.trial's protocol (DoOR's input, a 1 s odor after 1.5 s, 2 seeds of 8 flies), APL working and silenced.
Measured, for 3-octanol and 4-methylcyclohexanol: the Kenyon cells' free membrane potential (where the membrane would sit
without its own spikes, odor_gaba_block_check.free_potential) with APL working minus with it silenced, over the odor's
first second, for all Kenyon cells and for those firing no spike in either condition; its largest value over the odor
(50 ms running means of the population mean); APL's release; and the same at rest before the odor.
Also the two odors' answering Kenyon cells (more than half a spike over the odor's first second, on average over the
flies) and the share of each odor's that answer both, with APL working and silenced; in flies 30% of 3-octanol's and 33%
of 4-methylcyclohexanol's answer both (Hige et al. 2015; research_notes/Rung 9 learning data/hige2015_specificity.md).
Comparison: the inhibition during 3-octanol against flies' 5.5-7.5 mV mean and 15 mV most (Vrontou), and APL's ceiling
against the 10-12 mV at which flies' saturates (Inada).

Ran (148 s): mb_calibration2.py's APL holds the Kenyon cells farther down than flies' can as an odor begins, and about as
far as mb_calibration.py's over the odor. During 3-octanol their mean free potential falls up to 20.0 mV below where it
sits with APL silenced (50 ms means, at 80 ms, as APL's release peaks at 32 Hz): beyond the 15 mV most Vrontou et al. saw
and the 10-12 at which Inada et al.'s APL saturates. mb_calibration.py's falls up to 10.9 mV (its ceiling 11). Over the
odor's first second the Kenyon cells firing in neither condition sit 4.5 mV lower on average (5th-95th percentiles 6.5 and
2.7; mb_calibration.py's 3.7; Vrontou et al.'s mean 5.5-7.5); for 4-methylcyclohexanol 3.4 mV and up to 9.3 (3.2 and
10.2). At rest the graded APL holds every Kenyon cell 2.3 mV down (mb_calibration.py's 1.0). The inhibition is quickest
to arrive where flies' is slowest: largest at 80-110 ms, where flies' lags the Kenyon cells' excitation by several hundred
ms and lasts about a second (Vrontou et al.). The graded APL brings the odors' answering cells near flies' overlap: 108
answer both, 0.28 of 3-octanol's 387 and 0.46 of 4-methylcyclohexanol's 234 (flies 0.30 and 0.33; Jaccard 0.21, flies
about 0.19), against mb_calibration.py's 0.22 and 0.59 of 450 and 170. The rule for what came next was written in the
weekend's plan at 03:47, before this check reported: if this APL held the Kenyon cells down by 15 mV or less at its
largest during 3-octanol, rung 9's second attempt would be registered on it; above 15 mV, the attempt waits for an APL
whose synapses onto the Kenyon cells act as a conductance, which the cells' reversal potential bounds as flies' are
bounded. (The largest is taken from all the Kenyon cells' mean, three quarters of them firing in neither condition;
over the odor the silent cells' and everyone's means differ by 0.1 mV.) So the attempt waits.

    python experiments/odor_apl_inhibition_check.py      (writes experiments/odor_apl_inhibition_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 840000, 2
ODORS = ("3-octanol", "4-methylcyclohexanol")
FLIES = {"inada_2017_saturating_mv": [-12.0, -10.0], "vrontou_2021_mean_mv": [-7.5, -5.5], "vrontou_2021_most_mv": -15.0,
         "hige_2015_share_answering_both": {"3-octanol": 0.30, "4-methylcyclohexanol": 0.33}}


def trial(o, rec, odor: str, seed: int, apl: np.ndarray, silence) -> dict:
    """odor_apl_check.trial, also keeping the Kenyon cells' mean synaptic currents (for their free potential) at rest and
    over the odor's first second, and the population's free potential every 10 ms."""
    import odor_gaba_block_check as gb
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    q = [int(np.flatnonzero(b.graded == i)[0]) for i in apl]
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -1.5
    for _ in range(50):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        t += p10.PIECE
    rest_x = rest_s = 0.0
    for _ in range(100):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        rest_x, rest_s = rest_x + b.x / 100, rest_s + b.s / 100
        t += p10.PIECE
    spikes, odor_x, odor_s, course, release = 0, 0.0, 0.0, [], []
    for k in range(140):
        fired = b.advance(piece, drive=rec.at(plan, t), silence=silence)
        release.append(float(b.release[:, q].mean()))
        course.append(float(gb.free_potential(b, b.x, b.s)[:, kc].mean()))
        if k < 100:
            spikes = spikes + fired[:, kc]
            odor_x, odor_s = odor_x + b.x / 100, odor_s + b.s / 100
        t += p10.PIECE
    return {"rest": gb.free_potential(b, rest_x, rest_s)[:, kc], "odor": gb.free_potential(b, odor_x, odor_s)[:, kc],
            "spikes": np.asarray(spikes), "course": np.array(course), "release": np.array(release)}


def compare(on: list, off: list) -> dict:
    """APL's inhibition: the free potential with APL working minus with it silenced, the same seeds."""
    d_odor = np.concatenate([a["odor"] - b["odor"] for a, b in zip(on, off)])         # (flies, Kenyon cells)
    d_rest = np.concatenate([a["rest"] - b["rest"] for a, b in zip(on, off)])
    quiet = np.concatenate([(a["spikes"] == 0) & (b["spikes"] == 0) for a, b in zip(on, off)])
    course = np.mean([a["course"] - b["course"] for a, b in zip(on, off)], 0)
    smooth = np.convolve(course, np.ones(5) / 5, mode="valid")
    release = np.mean([a["release"] for a in on], 0)
    return {"inhibition_mv_all": round(float(d_odor.mean()), 2), "inhibition_mv_silent_cells": round(float(d_odor[quiet].mean()), 2),
            "silent_cells_share": round(float(quiet.mean()), 4),
            "silent_cells_inhibition_mv_percentiles_5_50_95": np.round(np.percentile(d_odor[quiet], [5, 50, 95]), 2).tolist(),
            "largest_inhibition_mv_50ms": round(float(smooth.min()), 2), "at_s": round(float(np.argmin(smooth) * p10.PIECE + 0.02), 2),
            "inhibition_mv_at_rest": round(float(d_rest.mean()), 3),
            "apl_release_peak_hz": round(float(np.convolve(release, np.ones(5) / 5, mode="valid").max()), 2),
            "apl_release_mean_hz": round(float(release[:100].mean()), 2)}


def overlap(answering: dict) -> dict:
    """The two odors' answering Kenyon cells and the share of each odor's answering both."""
    a, c = answering["3-octanol"], answering["4-methylcyclohexanol"]
    both = int((a & c).sum())
    return {"answering": {"3-octanol": int(a.sum()), "4-methylcyclohexanol": int(c.sum())}, "answering_both": both,
            "share_answering_both": {"3-octanol": round(both / max(int(a.sum()), 1), 3),
                                     "4-methylcyclohexanol": round(both / max(int(c.sum()), 1), 3)},
            "jaccard": round(both / max(int((a | c).sum()), 1), 3)}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import mb_calibration2
    calibrations = {"mb_calibration.py": (mb_calibration.KC_APL_SCALE, 1.0),
                    "mb_calibration2.py": (mb_calibration2.KC_APL_DRIVE, mb_calibration2.APL_KC_EFFECT)}
    b = o.brain
    out = {"question": __doc__, "flies": FLIES, "mb_calibration": mb_calibration.apply(o), "calibrations": {}}
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = o.m["kc"][pre] & np.isin(b.idx, apl)
    apl_kc = np.isin(pre, apl) & o.m["kc"][b.idx]
    calibrated = b.weights.copy()
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for name, (s, g) in calibrations.items():
            w = calibrated.copy()
            w[kc_apl] *= s / mb_calibration.KC_APL_SCALE
            w[apl_kc] *= g
            b.weights, b._external_matrix = w, None
            entry = {"kc_apl_scale": s, "apl_kc_effect": g, "ceiling_inhibition_mv": round(mb_calibration.KC_SATURATION_MV * g, 1)}
            answering = {"APL working": {}, "APL silenced": {}}
            for j, odor in enumerate(ODORS):
                on = [trial(o, rec, odor, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)]
                off = [trial(o, rec, odor, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)]
                entry[odor] = compare(on, off)
                for cond, rs in (("APL working", on), ("APL silenced", off)):
                    answering[cond][odor] = np.concatenate([r["spikes"] for r in rs]).mean(0) > 0.5
                print(name, odor, json.dumps(entry[odor]), flush=True)
            entry["overlap"] = {cond: overlap(a) for cond, a in answering.items()}
            print(name, "overlap", json.dumps(entry["overlap"]), flush=True)
            out["calibrations"][name] = entry
            OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
