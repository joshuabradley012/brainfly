"""Exploratory, not pre-registered: learning_pilot9.py with APL's synapses onto the Kenyon cells acting as a conductance
(mb_calibration3.py), held to flies' 10-12 mV saturation. Do rung 9's four marks still pass with the weighed input?

learning_pilot9.py: on odor_probe60.py's model with mb_calibration2.py's graded APL, the weighed input passes all four
marks, two by about a standard error (with 3-octanol paired 4-methylcyclohexanol's spikes fall 42.5%, band 10-45%; with
4-methylcyclohexanol paired 3-octanol's 17.2%, band 15-50%), but that APL holds the Kenyon cells up to 20 mV down as an
odor begins, beyond flies' 15 at most (odor_apl_inhibition_check.py). odor_apl_conductance_check.py: as a conductance
reversing 20 mV below rest, with its ceiling holding a quiet Kenyon cell 11 mV down and the Kenyon cells' drive at 1.5
times MaleCNS's, APL answers 4-methylcyclohexanol with 0.45 of its peak for 3-octanol (flies 0.49), silencing it raises
the Kenyon cells' spikes 2.92 and 2.21-fold (flies 2-3), and it holds them at most 7.1 mV down during an odor.
Model: odor_probe60.py's (its cache) with mb_calibration3.py's mushroom body; otherwise as learning_pilot9.py. Inputs,
each a condition: DoOR alone; and the weighed input (receptor_fills.RECOMMENDED). Protocol, rule, fit and measures as
learning_pilot5.py. Seeds learning_pilot8.py's and learning_pilot9.py's (640000), so that only the model differs.

Ran (27 minutes): as learning_pilot9.py's, a little weaker. With the weighed input all four of rung9_learning.py's marks
pass, the reciprocal by 0.4 points. 4-methylcyclohexanol reaches 111 Kenyon cells against 3-octanol's 514
(learning_pilot9.py 138 and 612), and MBON11 answers with 9.8 and 48.9 spikes (12.8 and 58.7; flies 110 and 118).
Pairing 3-octanol cuts its own spikes 97% and 4-methylcyclohexanol's 41.3% (its charge 36.8%; band 10-45%); pairing
4-methylcyclohexanol cuts its own 103% and 3-octanol's 15.4% (band 15-50%; flies 38%); backward pairing changes the
charge 0.1% and 1.1%. With DoOR's input 268 against 422 Kenyon cells, and the pairings cut 95% and 46.7% (band 10-45%;
its charge 41.9%), and 99% and 32.0%. With the weighed input 0.54 of 4-methylcyclohexanol's answering cells answer
3-octanol and 0.12 of 3-octanol's answer 4-methylcyclohexanol (flies 0.33 and 0.30). Before this pilot reported, the
weekend's plan was amended (04:55, on research_notes/Rung 9 learning data/apl_kinetics.md): rung 9's second attempt waits
for an APL with flies' time course, whatever this pilot showed, since this APL's conductance decays in 5 ms where flies'
takes about 0.3 s (odor_apl_kinetics_check.py).

Correction (2026-10-11, odor_apl_kinetics_check.py's Fig. 5B test): HybridBrain measures slow_reversal from the model's
zero, and the Kenyon cells don't rest there: each class sits its measured distance below the shared 16 mV threshold, so
alpha'/beta' cells rest at 0, alpha/beta at -5.5 and gamma at -16.5 mV. A reversal of -20 therefore lay 20, 14.5 and 3.5 mV
below them, not 20 below each, and APL could barely inhibit the gamma cells (38% of the Kenyon cells, among them MBON11's γ1
input). APL at its ceiling held the quiet Kenyon cells 3.8 mV down on average, not 11. mb_calibration4.py corrects it. This pilot ran on that APL.

    python experiments/learning_pilot10.py        (writes experiments/learning_pilot10.json)
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
    import mb_calibration3                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration3.apply(o),
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
