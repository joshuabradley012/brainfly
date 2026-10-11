"""Exploratory, not pre-registered: learning_pilot8.py on odor_probe60.py's model (presynaptic inhibition scaling with an
odor's total input as flies' normalization does) with a graded APL (mb_calibration2.py). Does pairing
4-methylcyclohexanol now depress MBON11's response to 3-octanol as flies' does (rung 9's reciprocal)?

learning_pilot8.py and rung9_learning.py (odor_probe56.py's model, mb_calibration.py): with the weighed input, pairing
3-octanol cuts its own MBON11 spikes 88-89% and 4-methylcyclohexanol's 31-35% (flies 80% and 27%), but pairing
4-methylcyclohexanol cuts 3-octanol's only 4-5% (flies 38%; band 15-50%): its 60 responding Kenyon cells carry 3-4% of
3-octanol's input to MBON11. Since then: odor_probe60.py's antennal lobe divides weak odors less (4-methylcyclohexanol
0.30 of 3-octanol at the PNs with the weighed input, from 0.21; 0.73 with DoOR's, from 0.54), and odor_apl_two_knob_check.py
makes APL answer each odor in proportion (4-methylcyclohexanol 0.47 of 3-octanol's peak, flies 0.49), equalizing the
Kenyon cells 1.29-fold (flies 1.25).
Model: odor_probe60.py's (its cache) with mb_calibration2.py's mushroom body; otherwise as learning_pilot8.py (MBON11 held
near 6 Hz, its Kenyon cell synapses at 0.054 pC and depressing as measured). Inputs, each a condition: DoOR alone; and
the receptor input the evidence supports at Hige et al.'s concentration (receptor_fills.RECOMMENDED). Protocol, rule,
fit and measures as learning_pilot5.py. Seeds learning_pilot8.py's (640000), so that only the model differs.

Ran (22 minutes): with the weighed input every one of rung9_learning.py's four marks passes, two of them narrowly; with
DoOR's input the reciprocal passes and the unpaired odor falls too far. Weighed input: 4-methylcyclohexanol reaches 138
Kenyon cells against 3-octanol's 612 (learning_pilot8.py 61 and 388) and MBON11 answers with 12.8 and 58.7 spikes (5.3
and 31.1; flies 110 and 118). Pairing 3-octanol cuts its own spikes 96% and 4-methylcyclohexanol's 42.5% (band 10-45%;
its charge 39%; flies 27%); pairing 4-methylcyclohexanol cuts its own 102% and 3-octanol's 17.2% (band 15-50%; flies
38%; learning_pilot8.py 4.2%); backward pairing changes the charge 0.1% and 1.7%. The two margins, 2.5 and 2.2 points,
are about the size of a standard error (the spikes' SEMs give about 5 and 3 points), so fresh seeds could fail either.
DoOR's input: 326 against 517 Kenyon cells (129 and 438), 29.3 and 41.7 spikes (12.8 and 27.6); pairing 3-octanol cuts
95% and 50% (band 10-45%), pairing 4-methylcyclohexanol 99% and 30.5% (learning_pilot8.py 12.5%). The depressions follow
the Kenyon cells' overlap as flies' do (Hige et al. 2015, Fig. 7I: about 0.71 x overlap + 0.15): with DoOR's input half
of 4-methylcyclohexanol's answering cells answer 3-octanol (0.50; flies 0.33) and a third of 3-octanol's answer
4-methylcyclohexanol (0.32; flies 0.30), predicting 0.51 and 0.38 against the model's 0.50 and 0.305; with the weighed
input 0.55 and 0.12. What still separates the model from flies is the size of 4-methylcyclohexanol's Kenyon cell set,
not the rule: flies answer the two odors with about as many cells (49 and 53 in Hige et al.'s data). The graded APL
behind this holds the Kenyon cells up to 27.5 mV down at its ceiling, where flies' saturates at 10-12 mV
(odor_apl_inhibition_check.py measures what it does during odors).

    python experiments/learning_pilot9.py        (writes experiments/learning_pilot9.json)
"""
from __future__ import annotations

import contextlib
import json
import time
from pathlib import Path

import brain_cache
import learning_pilot3 as lp3
import learning_pilot4 as lp4
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SCRATCH = OUT.with_name(OUT.stem + "_variant.json")
SEED = 640000
CHARGE_PC = 0.030 * 34.5 / 19.0
CONDITIONS = ("DoOR", "weighed input")


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    lp4.SEED, lp4.OUT = SEED, SCRATCH
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration2                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration2.apply(o),
           "conditions": {}}
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        for name in CONDITIONS:
            print("condition:", name, flush=True)
            inputs = contextlib.nullcontext() if name == "DoOR" else receptor_fills.applied(recommended=True)
            with inputs:
                row = lp4.variant(o, rec, True, {"variants": {}})
            out["conditions"][name] = row
            OUT.write_text(json.dumps(out, indent=1))
    SCRATCH.unlink(missing_ok=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
