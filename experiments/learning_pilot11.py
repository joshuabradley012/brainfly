"""Exploratory, not pre-registered: learning_pilot10.py with the corrected APL conductance (mb_calibration4.py): its
reversal 20 mV below each Kenyon cell's own rest and flies' time course (decay 0.3 s). Do rung 9's four marks pass with the
weighed input?

learning_pilot10.py passed them narrowly, but on mb_calibration3.py's APL, whose reversal lay only 3.5 mV below the gamma
Kenyon cells' rest, and whose inhibition faded in 5 ms where flies' takes about 0.3 s. odor_apl_conductance2_check.py:
corrected, APL answers 4-methylcyclohexanol with 0.53 of its peak for 3-octanol (flies 0.49) and silencing it raises the
Kenyon cells' spikes 2.7-fold (flies 2-3), but more Kenyon cells answer, APL no longer equalizes the odors, and 0.63 of
4-methylcyclohexanol's answering cells answer 3-octanol (flies 0.33).
Model: odor_probe60.py's (its cache) with mb_calibration4.py's mushroom body; otherwise as learning_pilot10.py. Inputs,
each a condition: DoOR alone; and the weighed input (receptor_fills.RECOMMENDED). Protocol, rule, fit and measures as
learning_pilot5.py. Seeds learning_pilot8.py's to learning_pilot10.py's (640000), so that only the model differs.
Rule, written before it runs (and in the weekend's plan): if the weighed input passes all four of rung9_learning.py's
marks, rung 9's second attempt is registered on this model with fresh seeds; if not, it isn't.

Ran (28 minutes): no. On the corrected APL the weighed input fails the reciprocal, so by the rule rung 9's second attempt
isn't registered. With the weighed input 4-methylcyclohexanol reaches 87 Kenyon cells against 3-octanol's 562
(learning_pilot10.py 111 and 514), and MBON11 answers with 8.5 and 38.6 spikes (flies 110 and 118). Pairing 3-octanol cuts
its own spikes 89% and 4-methylcyclohexanol's 38.5% (its charge 38.8%; band 10-45%); pairing 4-methylcyclohexanol cuts its
own 98% but 3-octanol's only 10.2% (band 15-50%; flies 38%); backward pairing changes the charge 0.0% and 0.7%. With DoOR's
input 240 against 572 Kenyon cells: pairing 3-octanol cuts 84% and 56% (band 10-45%), pairing 4-methylcyclohexanol 95% and
20.9%. With the weighed input half of 4-methylcyclohexanol's answering cells answer 3-octanol (0.51; flies 0.33), but only
0.08 of 3-octanol's answer 4-methylcyclohexanol (flies 0.30), carrying 7% of its charge. With inhibition that builds over
0.3 s, the first spikes decide which Kenyon cells answer, and 3-octanol's stronger input recruits far more of them. What
separates the model from flies is the same as before: 4-methylcyclohexanol's Kenyon cell set (flies answer the two odors
with about as many cells), now without APL's equalizing (0.85-fold; flies 1.25; odor_apl_conductance2_check.py).

    python experiments/learning_pilot11.py        (writes experiments/learning_pilot11.json)
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
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration4.apply(o),
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
