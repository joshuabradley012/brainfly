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
