"""Exploratory, not pre-registered: with 3-octanol's and 4-methylcyclohexanol's receptor input as the receptor-level
evidence puts it at Hige et al.'s concentration, how do the model's projection neurons and Kenyon cells answer them,
compared like for like with flies'?

research_notes/Rung 9 learning data/oct_mch_concentration.md: weighing every receptor-level measurement by tier and
concentration, correcting DoOR's import errors (D's unsubtracted solvent response, DA2's floor) and giving no drive where
flies' PN responses are lateral (DA1, DL3), 4-methylcyclohexanol's summed receptor drive at 2% of saturated vapour is
0.37 of 3-octanol's (receptor_fills.RECOMMENDED: 1.99 against 5.32; 2 glomeruli above 0.1 against 13), so the receptor
input can't equalize the odors, and flies' equalization has to come downstream. mch_oct_equalization.md: flies' PN ratios
(0.98 over Badel et al.'s 37 glomeruli, 0.85 over Barth et al.'s 18) leave out 3-octanol's strongest glomeruli (VM5d,
VM5v, VC3, DC1), and summed over Badel's 37 the model's odor_probe54.py already gives 0.86 (0.93 with the fills),
against 0.56 over every glomerulus; at the Kenyon cells the model gives 0.25 where flies' give 0.73-0.92, and flies' APL
holds 3-octanol back more (Prisco et al. 2021), which the model's, saturating, doesn't (odor_apl_check.py,
odor_apl_range_check.py).
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body.
Measured, with receptor_fills.RECOMMENDED's input: odor_equalization_check.py's measures (now with the ratio over
Badel et al.'s glomeruli and per glomerulus over all of them) and odor_probe36.measure's (Kenyon cells by class and
odor, overlap, MBON11). Seeds 690000 (odor_probe36.measure) and 695000 (equalization).

    python experiments/odor_probe55.py         (writes experiments/odor_probe55.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe54 as p54
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 690000, 695000


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o)}
    with receptor_fills.applied(recommended=True) as inputs, warm.tracking(o, rec) as held:
        out["inputs"] = inputs
        out["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
        OUT.write_text(json.dumps(out, indent=1))
        out.update(p36.measure(o, rec, built, SEED))
        od = out["odors"]
        print("KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
              "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
              "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in out["mbon11_input"].items()}), flush=True)
        out["measure_settles"] = held["settles"]
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
