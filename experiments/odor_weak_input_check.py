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

Ran: presynaptic inhibition isn't it, and the receptor synapse's depression can't be taken out on its own. Intact,
DL5's PNs rise 19, 42, 78 and 111 spikes/s over the 0.5 s for 5, 10, 20 and 40 spikes/s of receptor input (Olsen et
al.'s fit 36, 73, 115 and 144), VM7d's 13, 34, 70 and 108 (33, 68, 110 and 139), DM4's 9, 19, 31 and 46 (25, 55, 98 and
135), and DM1's 24, 50, 82 and 114, above its fit (5, 14, 33 and 66): DM1 is flies' least sensitive glomerulus (sigma
45) and the model's most sensitive. Without the presynaptic inhibition they barely change (DL5 22, 45, 79 and 111): one
glomerulus recruits too few LNs for it to matter. Without the receptor synapses' depression the spontaneous input,
undepressed, drives the LNs so hard that the inhibition silences the PNs at rest (0 spikes/s) and nearly abolishes weak
responses (DL5 0, 4, 42 and 123); with both off the PNs rest at 39-89 spikes/s and rise far above flies' (DL5 84, 146,
222 and 286). The model's resting state is built around the depressed synapse, so these manipulations don't isolate its
gain. odor_transform_check.py asks whether the step the transform is measured with understates weak input.

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
