"""Exploratory, not pre-registered: with APL's feedback set from its measured release onset, maximum and effect, do the
Kenyon cells stay as sparse as flies', and what does that leave for MBON11?

odor_probe44.py (the base model): 0.8-4.9% of Kenyon cells respond to each odor (flies 6 +- 5%), the alpha/beta cells
firing 0.95-1.7 spikes per response (flies 2.2), but APL is silent (it releases 0-0.4 Hz during odors; so since
odor_probe30.py): its graded release starts 7 mV above rest (rung 4's default, the spiking threshold) and the Kenyon
cells, firing few spikes, depolarize it by under 1 mV. In flies APL matters: blocking it raises the Kenyon cells' odor
responses two- to threefold (Lin et al. 2014: alpha lobe calcium 0.24 -> 0.72 with APL>TeTx; Bergmann et al. 2026: "two
to threefold"); driving it hyperpolarizes every Kenyon cell, saturating at -10 to -12 mV (Inada et al. 2017, ex vivo);
non-spiking insect interneurons release transmitter from 2-5 mV of depolarization (Amin et al. 2020, Vrontou et al.
2021); in vivo, alpha/beta-c Kenyon cells' lateral inhibition through APL averages -5.5 to -7.5 mV (Vrontou)
(research_notes/Rung 9 learning data/kc_classes_and_apl.md).
Model: odor_probe44.py's (its cache), settled starts (warm.tracking), with APL's release starting 3.5 mV above rest
(the middle of 2-5 mV; gain as before, 6 Hz per mV), its maximum release the rate that hyperpolarizes the Kenyon cells
by 11 mV on average below threshold (each Hz of APL release acting like a spike per second on its synapses: the mean
over Kenyon cells of the summed APL synapse weight x the synaptic time constant x the rate; computed, because holding a
graded neuron's release with set_release lets its own release run away, a kernel bug noted below), and every Kenyon
cell-to-APL synapse times s. The fit, stated before running: s from 1, 3, 10 and 30 whose mean ratio of the Kenyon
cells' evoked spikes with APL silenced to those with it working (Hige et al.'s protocol, 1 s odor and 0.4 s after; six
odors, 2 seeds of 8 flies) is nearest 2.5.
Measured at the chosen s: everything odor_probe36.py measures, and the Kenyon cells' mean membrane potential over each
odor with APL working against silenced (3-octanol and 4-methylcyclohexanol). Seeds 480000 (+ 100 x scale index + 10 x
odor + seed for the sweep, the same for APL working and silenced; + 700 + odor for the membrane potentials).

Kernel bug found on the way (to fix with the next change to brainfly/hybrid.py, which invalidates every cache): a neuron
made external with set_release still takes background noise kicks but isn't integrated, so its membrane climbs without
leak; nothing reads an ordinary external neuron's state, but a graded one's own release is still computed from it and
added to the release set_release gives it. No run so far made a graded neuron (the two APLs are the only ones) external.

Ran: APL's feedback, set from its measurements, makes the Kenyon cells sparser than flies'. APL's synapses onto a
Kenyon cell sum to -57.5 mV per Hz of release (mean), so it saturates at 38.3 Hz per APL. Releasing from 3.5 mV alone
wakes it: with s = 1 silencing it raises the Kenyon cells' evoked spikes 1.43-fold (mean of six odors), with 3 1.69, with
10 2.22 and with 30 2.83; s = 10 is the nearest 2.5. There APL releases 8-17 Hz over an odor's first 100 ms and 4-8 Hz
over the odor, and the Kenyon cells sit 1.1-1.4 mV lower over the odor than with it silenced (Vrontou et al.'s -5.5 to
-7.5 mV came from driving alpha/beta-c Kenyon cells for 50-2000 ms, not from odors, so it isn't compared). The Kenyon
cells then respond at 0.5-2.1% (flies 6 +- 5%; 0.8-4.9% with APL silent, odor_probe44.py), the alpha/beta cells firing
0.9-1.9 spikes per response (flies 2.2) and the alpha'/beta' cells responding at 0.9% to 3-octanol (flies 9-14%); mean
Jaccard 0.12; MBON11 gains 3 spikes to 3-octanol from 10 pC per cell (flies 118 from about 250). So the Kenyon cells'
match to flies' density depended on APL being silent; with it working, the drive they get from the PNs falls about
twofold short (odor_probe46.py).

    python experiments/odor_probe45.py         (writes experiments/odor_probe45.json)
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
import odor_probe7 as p7
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 480000
SCALES = (1.0, 3.0, 10.0, 30.0)
RELEASE_AT_MV, KC_SATURATION_MV, TARGET_RATIO, SEEDS = 3.5, -11.0, 2.5, 2


def evoked_kc_spikes(o, rec, runner, odor: str, seed: int, silence) -> float:
    """Hige et al.'s protocol: the Kenyon cells' spikes over the odor and 0.4 s after, less their rest, per fly."""
    h = runner(o, odor, seed, 1.0, 0.4, silence)
    kc = o.m["kc"]
    return float((h["window"][:, kc].sum(1) - 1.4 * h["rest"][:, kc].sum(1)).mean())


def kc_odor_v(o, rec, odor: str, seed: int, silence) -> float:
    """The Kenyon cells' mean membrane potential over the 1 s odor (after 2 s of rest)."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    kc = o.m["kc"]
    t = -2.0
    for _ in range(200):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        t += p10.PIECE
    u = 0.0
    for _ in range(100):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        t += p10.PIECE
        u += float(b.u[:, kc].mean()) / 100
    return u


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    runner = p10.make_runner(rec)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, apl))
    w0 = b.weights.copy()
    out = {"question": __doc__, "apl_cells": int(len(apl)), "kc_to_apl_edges": int(len(onto)), "release_at_mv": RELEASE_AT_MV,
           "flies": {"block_ratio": "2-3 (Lin 2014: 3.0; Bergmann 2026: 2-3)", "kc_saturation_mv": "-10 to -12 (Inada 2017)",
                     "lateral_inhibition_mv": "-5.5 to -7.5 (Vrontou 2021)"}, "sweep": {}}
    kc = np.flatnonzero(m["kc"])
    e = np.flatnonzero(np.isin(pre, apl) & m["kc"][b.idx])
    summed = np.bincount(b.idx[e], weights=b.weights[e], minlength=b.n)[kc]        # mV per Hz of every APL's release
    max_hz = KC_SATURATION_MV / (float(summed.mean()) * p21.TAU)
    out["apl_to_kc_summed_weight_mv"] = {"mean": round(float(summed.mean()), 2), "median": round(float(np.median(summed)), 2)}
    out["max_release_hz"] = round(max_hz, 2)
    print(f"APL's summed weight onto a Kenyon cell {summed.mean():.1f} mV: maximum release {max_hz:.1f} Hz per APL", flush=True)
    with warm.tracking(o, rec):
        b.set_type("APL", release_at=RELEASE_AT_MV, max_release=max_hz)
        for i, s in enumerate(SCALES):
            w = w0.copy()
            w[onto] *= s
            b.weights, b._external_matrix = w, None
            row = {}
            for j, odor in enumerate(p7.ODORS):
                on = np.mean([evoked_kc_spikes(o, rec, runner, odor, SEED + 100 * i + 10 * j + k, ()) for k in range(SEEDS)])
                off = np.mean([evoked_kc_spikes(o, rec, runner, odor, SEED + 100 * i + 10 * j + k, apl) for k in range(SEEDS)])
                row[odor] = {"apl_on": round(float(on), 1), "apl_silenced": round(float(off), 1), "ratio": round(float(off / max(on, 1e-9)), 2)}
            ratios = [row[od]["ratio"] for od in row]
            out["sweep"][f"{s:g}"] = {"odors": row, "mean_ratio": round(float(np.mean(ratios)), 2)}
            print(f"s {s:g}: mean ratio {np.mean(ratios):.2f}", json.dumps({od[:6]: (r['apl_on'], r['apl_silenced']) for od, r in row.items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
        best = min(out["sweep"], key=lambda k: abs(out["sweep"][k]["mean_ratio"] - TARGET_RATIO))
        out["chosen_scale"] = float(best)
        w = w0.copy()
        w[onto] *= float(best)
        b.weights, b._external_matrix = w, None
        print("chosen s", best, flush=True)
        entry = {"kc_odor_v_mv": {}}
        for j, odor in enumerate(("3-octanol", "4-methylcyclohexanol")):
            on = kc_odor_v(o, rec, odor, SEED + 700 + j, ())
            off = kc_odor_v(o, rec, odor, SEED + 700 + j, apl)
            entry["kc_odor_v_mv"][odor] = {"apl_on": round(on, 3), "apl_silenced": round(off, 3), "difference": round(on - off, 3)}
        print("Kenyon cells' mean V over the odor, APL on - silenced:", json.dumps({od[:6]: r["difference"] for od, r in entry["kc_odor_v_mv"].items()}), flush=True)
        entry.update(p36.measure(o, rec, built, SEED))
        out["at_chosen_scale"] = entry
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
