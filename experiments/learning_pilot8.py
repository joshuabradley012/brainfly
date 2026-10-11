"""Exploratory, not pre-registered: learning_pilot7.py on the model whose projection neurons rest at flies' rate: does the
reciprocal pairing reach flies'?

learning_pilot7.py (odor_probe54.py's model): pairing 3-octanol cut its MBON11 spikes 83-84% and 4-methylcyclohexanol's
45-49% (flies 80% and 27%), but pairing 4-methylcyclohexanol cut 3-octanol's only 9-14% (flies 38%; band 15-50%), with
4-methylcyclohexanol reaching a quarter as many Kenyon cells as 3-octanol, and MBON11 answering 3-octanol with about a
fifth of flies' spikes. odor_pn_rest_check.py: with the PNs resting nearer flies' 4.6 spikes/s their responses move
toward flies' at all but the weakest input and MBON11's response to 3-octanol nearly doubles; odor_probe56.py rebuilds
the model that way.
Model: odor_probe56.py's (its cache) with mb_calibration.py's mushroom body; otherwise as learning_pilot7.py (MBON11
held near 6 Hz, its Kenyon cell synapses at 0.054 pC and depressing as measured).
Inputs, each a condition: DoOR alone; and the receptor input the evidence supports at Hige et al.'s concentration
(receptor_fills.RECOMMENDED). Protocol, rule, fit and measures as learning_pilot5.py. Seeds learning_pilot6.py's
(640000), so that only the model (and the second input) differs.

    python experiments/learning_pilot8.py        (writes experiments/learning_pilot8.json)
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
import odor_probe56 as p56
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
    o, rec, built = brain_cache.load("odor_probe56", p56.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration.apply(o),
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
