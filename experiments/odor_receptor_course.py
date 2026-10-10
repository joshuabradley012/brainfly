"""Exploratory check, not pre-registered: in odor_probe21.py's base antennal lobe, does odor_probe10.py's measured
receptor time course (latency 4-50 ms falling with drive, a 30 ms rise, adaptation toward half over 0.4 s; no spontaneous
firing) remove the LNs' onset burst or make the PNs accommodate?

Each of 3-octanol and 4-methylcyclohexanol for 1 s, with the receptor neurons stepping on (as in every other probe) and
with odor_probe10.py's time course: the driven PNs', the 90 GABAergic LNs' (summed) and the receptor neurons' (summed)
rates in 50 ms bins. Seed 151000.

Ran: no. The time course delays the LNs' burst by about 50 ms (summed peak 7,000 and 6,200 spikes/s for 3-octanol, in
the first and second bins) but leaves its size. The PNs then start slower and peak a little earlier (at 300-450 ms
rather than 500-600) and decline after, following the receptor neurons' adaptation (3-octanol: 255 Hz at the peak, 230
at 1 s), but at 0.5 s they are still at 0.99-1.0 of their peak, against flies' about 0.5 (Bhandawat et al. 2007).

    python experiments/odor_receptor_course.py       (writes experiments/odor_receptor_course.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 151000


def run(o, rec, mk, pn_of, odor: str, kinetics: bool) -> dict:
    b, m = o.brain, o.m
    rec.kinetics = "fast" if kinetics else False
    plan = rec.plan(odor, 1.0, 200.0)
    pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of and len(pn_of[g])])
    b.reset(SEED)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -2.0
    for _ in range(200):
        b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
    pn, ln, orn = [], [], []
    t = 0.0
    for _ in range(20):
        c = 0
        for _ in range(5):
            c = c + b.advance(piece, drive=rec.at(plan, t))
            t += p10.PIECE
        pn.append(round(float(c[:, pns].mean() / 0.05), 1))
        ln.append(round(float(c[:, mk["inhibitors"]].sum(1).mean() / 0.05), 1))
        orn.append(round(float(c[:, m["orn"]].sum(1).mean() / 0.05), 1))
    return {"pn_hz": pn, "gaba_ln_summed_hz": ln, "orn_summed_hz": orn, "pn_at_0.5s_over_peak": round(float(np.mean(pn[8:10]) / max(pn)), 3),
            "pn_peak_bin": int(np.argmax(pn))}


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m = o.types, o.m
    out = {"question": __doc__, "build": p21.build(o), "runs": {}}
    mk = p21.masks(o)
    gloms = sorted({t[4:] for t in types[m["orn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    rec = p10.Receptors(o)
    for odor in ("3-octanol", "4-methylcyclohexanol"):
        for kin in (False, True):
            r = run(o, rec, mk, pn_of, odor, kin)
            out["runs"][f"{odor} | {'measured time course' if kin else 'step'}"] = r
            print(odor, kin, json.dumps(r), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
