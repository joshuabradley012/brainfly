"""Exploratory check, not pre-registered: how far does the model's antennal lobe equalize 4-methylcyclohexanol with
3-octanol, at its receptor neurons and at its projection neurons?

learning_pilot5.py: 4-methylcyclohexanol recruits a quarter as many Kenyon cells as 3-octanol (99 against 383), where
flies' two odors recruit about as many (49 and 53), which holds back the reciprocal pairing. In flies MCH/OCT is about
0.45 summed over receptor neurons, 0.85-0.98 over projection neurons (Barth et al. 2014, Badel et al. 2016, MCH active in
at least as many glomeruli as OCT: 18 against 13), and 0.73-0.92 over Kenyon cells (research_notes/Rung 9 learning
data/oct_mch_input.md, which lists this as its first check).
Model: odor_probe44.py's (its cache) with mb_calibration.py's calibration, settled starts.
Measured: for 3-octanol and 4-methylcyclohexanol (Hige et al.'s protocol, 1 s; 4 seeds of 8 flies), the summed evoked
rate over the receptor neurons and over the uniglomerular PNs (the odor's first 0.5 s and its whole second, less the
rest before it), the PNs' evoked rate per glomerulus, and the number of glomeruli whose PNs rise more than 10 and 30
spikes/s; and the ratios. Seeds 540000 + 10 x odor + seed.

Ran: the model's antennal lobe equalizes the two odors a little where flies' equalizes them almost fully. Summed over
receptor neurons, 4-methylcyclohexanol's evoked rate is 0.39 of 3-octanol's over the first 0.5 s (flies about 0.45);
summed over uniglomerular PNs 0.52 (0.50 over the whole second; flies 0.85-0.98); over Kenyon cells 0.26 in
learning_pilot5.py (flies 0.73-0.92). The PNs of 14 glomeruli rise more than 10 spikes/s to 3-octanol and of 9 to
4-methylcyclohexanol (11 and 5 more than 30), where flies' PNs answer 4-methylcyclohexanol in more glomeruli than
3-octanol (18 against 13; Badel et al. 2016). 4-methylcyclohexanol's weak receptor input to many glomeruli (14 of its 18
glomeruli in DoOR are below 0.2) doesn't become PN responses as it does in flies.

    python experiments/odor_equalization_check.py      (writes experiments/odor_equalization_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import mb_calibration
import odor_probe10 as p10
import odor_probe44 as p44
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 540000
ODORS = ("3-octanol", "4-methylcyclohexanol")
SEEDS = 4


def run(o, rec, odor: str, seed: int) -> dict:
    """Counts per neuron (mean over flies): 1 s of rest, the odor's first 0.5 s and its whole 1 s."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -1.5
    for _ in range(50):
        b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
    rest = 0
    for _ in range(100):
        rest = rest + b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
    first, whole = 0, 0
    for k in range(100):
        c = b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
        whole = whole + c
        if k < 50:
            first = first + c
    return {"rest": rest.mean(0), "first": first.mean(0), "whole": whole.mean(0)}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    mb_calibration.apply(o)
    types, m = o.types, o.m
    gloms = sorted({t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    orn, upn = np.flatnonzero(m["orn"]), np.flatnonzero(m["upn"])
    out = {"question": __doc__, "odors": {}}
    with warm.tracking(o, rec):
        for j, odor in enumerate(ODORS):
            rs = [run(o, rec, odor, SEED + 10 * j + k) for k in range(SEEDS)]
            rest, first, whole = (np.mean([r[x] for r in rs], 0) for x in ("rest", "first", "whole"))
            ev_first, ev_whole = first / 0.5 - rest, whole - rest            # Hz per neuron, over the rest
            per_glom = {g: round(float(ev_first[idx].mean()), 1) for g, idx in pn_of.items() if len(idx)}
            out["odors"][odor] = {"orn_summed_evoked_hz": {"first_0.5s": round(float(ev_first[orn].sum()), 1), "1s": round(float(ev_whole[orn].sum()), 1)},
                                  "upn_summed_evoked_hz": {"first_0.5s": round(float(ev_first[upn].sum()), 1), "1s": round(float(ev_whole[upn].sum()), 1)},
                                  "glomeruli_over_10hz": int(sum(v > 10 for v in per_glom.values())),
                                  "glomeruli_over_30hz": int(sum(v > 30 for v in per_glom.values())),
                                  "pn_evoked_hz_by_glomerulus_first_0.5s": dict(sorted(per_glom.items(), key=lambda kv: -kv[1]))}
            r = out["odors"][odor]
            print(odor, json.dumps({k: r[k] for k in ("orn_summed_evoked_hz", "upn_summed_evoked_hz", "glomeruli_over_10hz", "glomeruli_over_30hz")}), flush=True)
    a, b2 = out["odors"]["4-methylcyclohexanol"], out["odors"]["3-octanol"]
    out["mch_over_oct"] = {"orn_first": round(a["orn_summed_evoked_hz"]["first_0.5s"] / b2["orn_summed_evoked_hz"]["first_0.5s"], 3),
                           "upn_first": round(a["upn_summed_evoked_hz"]["first_0.5s"] / b2["upn_summed_evoked_hz"]["first_0.5s"], 3),
                           "upn_1s": round(a["upn_summed_evoked_hz"]["1s"] / b2["upn_summed_evoked_hz"]["1s"], 3)}
    print("MCH/OCT", json.dumps(out["mch_over_oct"]), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
