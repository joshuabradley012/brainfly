"""Exploratory check, not pre-registered: what keeps weak receptor input from reaching the projection neurons?

odor_probe41.py and odor_probe44.py: the model's transform (one glomerulus's receptor neurons driven alone, the PNs'
mean rise over 0.5 s; Olsen et al. 2010) is shifted to stronger input than flies': DL5's PNs rise 41 spikes/s for 10
spikes/s of receptor input where Olsen et al.'s fit gives 73, and 75 for 20 where it gives 115, meeting it only near 80;
the transform's sigma is 21-34 (flies 12-16). In flies broad tuning and weak-input gain come mainly from the receptor
synapse itself (research_notes/Rung 9 learning data/lateral_excitation.md: Olsen & Wilson 2008, Wilson 2013), whose
depression and presynaptic inhibition the model both carries.
Model: odor_probe44.py's (its cache).
Measured: for each of Olsen et al.'s four glomeruli and 5, 10, 20 and 40 spikes/s of receptor input above the
spontaneous rate, odor_probe24.drive_response (the PNs' rise over the first 100 ms and over 0.5 s, 8 flies, 2 seeds)
under four conditions: intact; the presynaptic inhibition off; the receptor synapses' depression off (fast and slow,
every receptor neuron's synapses at their rested strength throughout); both off. Seeds 460000 + 100 x condition + 10 x
glomerulus + rate index (+ 5 for the second seed); settled starts (warm.tracking) throughout.

    python experiments/odor_weak_input_check.py      (writes experiments/odor_weak_input_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe16 as p16
import odor_probe24 as p24
import odor_probe44 as p44
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 460000
RATES = (5, 10, 20, 40)
SEEDS = 2
CONDITIONS = ("intact", "no presynaptic inhibition", "no depression", "neither")


def olsen(x, rmax, sigma):
    return rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    b, types, m = o.brain, o.types, o.m
    pres = dict(b._presynaptic) if b._presynaptic is not None else None
    orn = b.params[b.cls[np.flatnonzero(m["orn"])[0]]]
    plain = {k: orn[k] for k in ("depression", "slow_depression")}
    out = {"question": __doc__, "orn_depression": plain, "conditions": {}}
    for c, cond in enumerate(CONDITIONS):
        if cond in ("no presynaptic inhibition", "neither"):
            b._presynaptic = None
        else:
            b._presynaptic = dict(pres) if pres is not None else None
        b.set_type("ORN", **({"depression": 1.0, "slow_depression": 0.0} if cond in ("no depression", "neither") else plain))
        row = {}
        with warm.tracking(o, rec):
            for gi, g in enumerate(p16.GLOMERULI):
                pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
                row[g] = {}
                for k, hz in enumerate(RATES):
                    runs = [p24.drive_response(o, rec, {g: hz}, pns, SEED + 100 * c + 10 * gi + k + 5 * s) for s in range(SEEDS)]
                    row[g][f"{hz:g}"] = {x: round(float(np.mean([r[x] for r in runs])), 2) for x in ("whole", "first_100ms", "rest")}
                row[g]["olsen_fit"] = {f"{hz:g}": round(olsen(hz, *p16.OLSEN[g]), 1) for hz in RATES}
        out["conditions"][cond] = row
        print(cond, json.dumps({g: [row[g][f"{hz:g}"]["whole"] for hz in RATES] for g in p16.GLOMERULI}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b._presynaptic = pres
    b.set_type("ORN", **plain)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
