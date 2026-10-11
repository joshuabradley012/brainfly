"""Exploratory probe, not pre-registered: the receptor neurons' spontaneous rates measured where flies' have been, in place
of their sensillum class's median. Does the resting state move further toward flies', and what do DL5's and DL1's high
rates do to their transforms?

odor_probe10.py gives every receptor neuron its sensillum class's median spontaneous rate (basiconic 6, palp 8,
coeloconic 19 spikes/s; DoOR's compilation). research_notes/Rung 9 learning data/orn_pn_resting_state.md (2026-10-10)
collects measured rates for eight glomeruli: DM4 3.44 (Kazama & Wilson 2009, n = 11), DM6 2.2 (Tobin et al. 2017, from the
spontaneous EPSC rate and the ORN count), VM2 7.1 and DL1 17.2 (Olsen et al. 2007, n = 14 and 10), VM7d about 10-12.8
(Olsen & Wilson 2008; Nagel et al. 2011's pb1A), DM1 9 and about 15 (de Bruyne et al. 2001; Bhandawat et al. 2007), DL5
15.6-17 (Hallem et al. 2004; de Bruyne et al. 2001), DA1 1.5 (Jeanne & Wilson 2015). The note's arithmetic: the class
median overstates DM4's rate 1.7-fold, which alone explains much of DM4's excess resting drive, while DL5's and DL1's
measured rates would raise theirs; flies' DL5 PNs nonetheless respond steeply, which nothing measured explains
(pn_toy.py: DL5 at 14 spikes/s has sigma 19-20 against flies' 11.8).
Model: odor_probe56.py's build (odor_probe57.py's tonic presynaptic divisor wasn't adopted) with these rates from the
receptor drive's construction on, so the whole resting calibration is done with them: DM4 3.44, DM6 2.2, VM2 7.1, DL1 17.2, VM7d
11.4, DM1 12, DL5 16.3, DA1 1.5 (the midpoint where two measurements differ); every other glomerulus keeps its class's
median.
Measured as odor_probe57.py measures. Seeds 780000.
Adopted as the base, by a rule set before the run, if, by the PNs' free membrane potential (odor_gaba_block_check.py),
the fall with every receptor neuron silenced moves toward the note's estimates in DM4 and DM6 (about 6-8 mV) without the
mean over DM6, VM2 and VM7 moving away from flies' 7-10 mV and the rise with GABA blocked stays within flies' 5-8 mV or
within 1.5 mV of odor_probe56.py's 5.2; the PNs rest at 4-6 spikes/s and the GABAergic LNs within 2x of their targets;
the weighed input's 4-methylcyclohexanol summed response over the Badel set doesn't fall against 3-octanol's
(odor_probe56.py: 0.558); and every glomerulus but DL5 and DL1 (whose rates rise) keeps its sigma within 2 of
odor_probe56.py's or nearer flies'. DL5's and DL1's transforms are reported either way.

Ran: not adopted, and the measured rates show where the synapse fails rather than fixing the resting state. Where the
measured rate is low the resting drive falls toward flies' (by the free potential, every receptor neuron silenced: DM6
12.4 mV at 2.2 spikes/s, from 25.2; DM4 10.5, from 14.5; DA1 9.6 at 1.5, from 28.0); where it is high it grows (DL5 34.8 at
16.3 spikes/s, from 20.7; DL1 49.3, from 29.4; VM7d 37.9, from 31.1; DM1 28.2, from 19.6), so the mean over DM6, VM2 and VM7
barely moves (27.5, from 28.4). Blocking GABA raises the PNs 4.9 mV there (5.2), the PNs rest at 5.02 spikes/s and the
GABAergic LNs at 4.0. The high-rate glomeruli lose their transforms with their synapses' resting strength (DL5 0.21 of
rested, DL1 0.21): DL5's Rmax 101 and sigma 22.5 (odor_probe56.py 136 and 12.6; flies 167 and 11.8), VM7d 127 and 18.8 (141
and 15.4), DM1 110 and 16.0 (132 and 11.2), while DM4's steepens (Rmax 105, sigma 11.8; 90 and 13.5; flies 170 and 16.3).
The rule fails on VM7d's sigma (its rate rose too, from 8 to 11.4, though the rule exempted only DL5 and DL1) and,
narrowly, on 4-methylcyclohexanol (0.553 of 3-octanol over the Badel set with the weighed input, against 0.558; 0.143 at
the Kenyon cells, against 0.16). This is the note's DL5 problem in the full model: with two depleting pools a high
spontaneous rate costs a glomerulus both resting drive and response, where flies' DL5 and DL1 respond steeply anyway.
Flies' synapses would need deep depression at rest that caps the resting drive (Kazama & Wilson 2009's DM4) and
transmission that recovers fast during an odor (their 2008 recovery: about 0.4 s after 50-200 spikes/s, 7.5 s after 7).

    python experiments/odor_probe58.py      (writes experiments/odor_probe58.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe56 as p56
import odor_probe57 as p57

OUT = Path(__file__).with_suffix(".json")
SEED = 780000
MEASURED_HZ = {"DM4": 3.44, "DM6": 2.2, "VM2": 7.1, "DL1": 17.2, "VM7d": 11.4, "DM1": 12.0, "DL5": 16.3, "DA1": 1.5}


def build():
    """odor_probe56.build with the receptor neurons' spontaneous rates measured where flies' have been."""
    init = p10.Receptors.__init__

    def measured(self, o):
        init(self, o)
        for g, hz in MEASURED_HZ.items():
            if g in self.spont:
                self.spont[g] = hz
    p10.Receptors.__init__ = measured
    try:
        o, rec, out = p56.build()
    finally:
        p10.Receptors.__init__ = init
    out["spontaneous_hz"] = {g: rec.spont[g] for g in MEASURED_HZ if g in rec.spont}
    return o, rec, out


def main() -> None:
    t0 = time.perf_counter()
    p57.OUT, p57.SEED = OUT, SEED
    p57.EQUALIZATION_SEED, p57.WEIGHED_SEED, p57.WEIGHED_EQUALIZATION_SEED = SEED + 1000, SEED + 2000, SEED + 3000
    loaded = brain_cache.load("odor_probe58", build, p44.prepare)
    brain_cache_load, brain_cache.load = brain_cache.load, lambda *a, **k: loaded       # odor_probe57.main measures this model
    try:
        p57.main()
    finally:
        brain_cache.load = brain_cache_load
    out = json.loads(OUT.read_text())
    out.pop("resting_divisor", None)                                                   # odor_probe57.py's, not this model's
    out["question"], out["measured_spontaneous_hz"] = __doc__, MEASURED_HZ
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
