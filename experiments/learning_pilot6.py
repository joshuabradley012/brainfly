"""Exploratory, not pre-registered: on the rebuilt base model, how specific is learning, and how much does
4-methylcyclohexanol's missing receptor input matter for the reciprocal pairing?

learning_pilot5.py (odor_probe44.py's model): with the Kenyon cell-to-MBON11 synapses at 0.054 pC and depressing as
measured, pairing 3-octanol cut 4-methylcyclohexanol's MBON11 spikes 40% (flies 27%), but pairing 4-methylcyclohexanol
cut 3-octanol's only 8.7% (flies 38%; the suggested band 15-50%), because 4-methylcyclohexanol recruits a quarter as
many Kenyon cells as 3-octanol (flies about as many). Since then the base model has been rebuilt (odor_probe49.py to
odor_probe52.py: settled starts that settle, the receptor synapse as two pools, the PNs resetting to rest): Kenyon cells
2.4-13.8%, MBON11 24 spikes to 3-octanol and 9.4 to 4-methylcyclohexanol, which still reaches 0.26 as many Kenyon cells.
DoOR has no 4-methylcyclohexanol data for 13 receptors; receptor_fills.py fills four from Barth et al.'s receptor imaging
and, as a labelled stand-in, seven more from Badel et al.'s PN responses (odor_probe53.py measures what they do to the
Kenyon cells).
Model: odor_probe52.py's (its cache) with mb_calibration.py's mushroom body, settled starts, MBON11 keeping its current
and held near 6 Hz, its Kenyon cell synapses at 0.054 pC each and depressing as measured (learning_pilot5.py's
depressing variant, the configuration the fit targets chose).
Inputs, each a condition: DoOR alone; with receptor_fills.FILLS; with receptor_fills.PN_INFERRED as well.
Protocol, rule, fit and measures as learning_pilot5.py (learning_pilot4.variant). Seeds 640000 (learning_pilot3.py's
offsets), the same for every condition.

Ran: pairing 3-octanol is as specific as flies' at the band's upper edge, the reciprocal falls short in every
condition, and filling 4-methylcyclohexanol's missing receptors moves it toward flies' but not into the band. MBON11,
held at 6.4 Hz, gains 19.7-21.4 spikes to 3-octanol and 8.7-11.4 to 4-methylcyclohexanol (flies 118 and 110), whose
Kenyon cells number a quarter of 3-octanol's (92 against 368 with DoOR alone, 89 against 410 with the receptor fills,
141 against 496 with the PN-inferred tier too; flies 49 and 53).
  DoOR alone: 3-octanol paired cuts its own spikes 84% and 4-methylcyclohexanol's 42% (charge 42%); 4-methylcyclohexanol
    paired cuts its own 98% and 3-octanol's 8.3% (charge 13%).
  receptor fills: 83% and 43% (charge 42%); 97% and 7.7% (charge 14%).
  with the PN-inferred tier: 81% and 47% (charge 52%); 93% and 12.8% (charge 19%).
Backward pairing: 0.1-0.5% of the charge. Flies: 80% and 27% with 3-octanol paired, 76% and 38% with
4-methylcyclohexanol paired (hige2015_specificity.md's bands: the unpaired odor 10-45%, the reciprocal 15-50%, the paired
at least 65% and 30 points beyond). The asymmetry follows the overlap: 49-58% of 4-methylcyclohexanol's responders also
answer 3-octanol, carrying 37-50% of its input to MBON11, but those shared cells carry only 10-15% of 3-octanol's input,
where flies' two odors share 30-33% of their responders each way. The reciprocal waits on 4-methylcyclohexanol reaching
as many Kenyon cells as 3-octanol, which none of the receptor inputs gives it on this antennal lobe (odor_probe53.py).

    python experiments/learning_pilot6.py        (writes experiments/learning_pilot6.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import learning_pilot3 as lp3
import learning_pilot4 as lp4
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe52 as p52
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SCRATCH = OUT.with_name(OUT.stem + "_variant.json")
SEED = 640000
CHARGE_PC = 0.030 * 34.5 / 19.0
CONDITIONS = (("DoOR", None), ("receptor fills", False), ("receptor and PN-inferred fills", True))


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    lp4.SEED, lp4.OUT = SEED, SCRATCH
    o, rec, built = brain_cache.load("odor_probe52", p52.build, p44.prepare)
    import contextlib
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration.apply(o),
           "conditions": {}}
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        for name, pn_inferred in CONDITIONS:
            print("condition:", name, flush=True)
            inputs = contextlib.nullcontext() if pn_inferred is None else receptor_fills.applied(pn_inferred=pn_inferred)
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
