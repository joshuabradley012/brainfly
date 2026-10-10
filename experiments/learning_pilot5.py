"""Exploratory, not pre-registered: learning_pilot4.py with MBON11's Kenyon cell synapses at the charge Yamada et al.'s
population EPSCs give with their slow tail: does MBON11 answer as strongly as flies', and does the specificity hold?

learning_pilot4.py: on the rebuilt antennal lobe with the calibrated mushroom body, the depression is about as specific
as flies' both ways with the Kenyon cell-to-MBON synapses undepressed (and the reciprocal falls short with them
depressing), but MBON11 gains only 14-26 spikes to 3-octanol held near 6 Hz (flies 118). Its synapses' 0.030 pC came from
odor_probe31.py's reading of Yamada et al. 2024's population EPSCs, about 19 pC per flash; with the EPSC's slow tail
(decaying over 256-333 ms, 15-26 pA left after 1.5 s) the charge per flash is 26-43 pC (research_notes/Rung 9 learning
data/mbon11_kc_activity.md), so the same derivation gives 0.030 x 34.5 / 19 = 0.054 pC per synapse (the range's middle).
Model, protocol, rule, fit and measures as learning_pilot4.py, with 0.054 pC per synapse. Seeds 530000 (learning_pilot3's
offsets), the same for both variants.

Ran: with 0.054 pC MBON11 answers half again as strongly, still about a third as strongly as flies', and the specificity
is as before, the reciprocal pairing at or below the band's edge. Held near 6 Hz (5.6 and 5.9 Hz), MBON11 gains 38.4 spikes
to 3-octanol and 15.5 to 4-methylcyclohexanol undepressed, 19.7 and 9.9 depressing (flies 118 and 110). Undepressed:
pairing 3-octanol cuts its spikes 86% and 4-methylcyclohexanol's 35% (charge 40%); pairing 4-methylcyclohexanol cuts its
own 87% and 3-octanol's 14.5% (charge 16%; flies 38%), just below the band's 15%; backward 0-2%. Depressing: 81% and 40%
(charge 44%); 87% and 8.7% (charge 13%). What holds the reciprocal back is the responders' numbers: 4-methylcyclohexanol
recruits 99 Kenyon cells against 3-octanol's 383, so its responders carry 15% of 3-octanol's input (3-octanol's carry 41%
of 4-methylcyclohexanol's), where flies' two odors recruit about as many (49 and 53) and share 30-33% of their responders
(Hige et al. 2015). The reciprocal pairing waits on the antennal lobe equalizing 4-methylcyclohexanol with 3-octanol, as
flies' does (research_notes/Rung 9 learning data/oct_mch_input.md).

    python experiments/learning_pilot5.py        (writes experiments/learning_pilot5.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import learning_pilot3 as lp3
import learning_pilot4 as lp4
import mb_calibration
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 530000
CHARGE_PC = 0.030 * 34.5 / 19.0


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    lp4.SEED, lp4.OUT = SEED, OUT
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration.apply(o),
           "variants": {}}
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        for depressing in lp4.VARIANTS:
            lp4.variant(o, rec, depressing, out)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
