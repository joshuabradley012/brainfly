"""Exploratory, not pre-registered: learning_pilot6.py on the model whose receptor synapse's slow component depresses
as measured: does the reciprocal pairing reach flies'?

learning_pilot6.py (odor_probe52.py's model): pairing 3-octanol cut its MBON11 spikes 81-84% and 4-methylcyclohexanol's
42-47% (flies 80% and 27%), but pairing 4-methylcyclohexanol cut 3-octanol's only 8-13% (flies 38%; band 15-50%),
4-methylcyclohexanol reaching a quarter as many Kenyon cells as 3-octanol with every input. odor_slow_depression_check.py:
with the slow component depressing as Nagel et al. measured it the PNs' transform saturates nearly as flies' does
(odor_probe54.py rebuilds the model with it), which is part of how flies' antennal lobe equalizes a weak, broad odor with
a strong one.
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body; otherwise as learning_pilot6.py (MBON11
held near 6 Hz, its Kenyon cell synapses at 0.054 pC and depressing as measured).
Inputs, each a condition, as learning_pilot6.py: DoOR alone; with receptor_fills.FILLS; with receptor_fills.PN_INFERRED
as well. Protocol, rule, fit and measures as learning_pilot5.py. Seeds learning_pilot6.py's (640000), so that only the
model differs.

    python experiments/learning_pilot7.py        (writes experiments/learning_pilot7.json)
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
import odor_probe54 as p54
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
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
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
