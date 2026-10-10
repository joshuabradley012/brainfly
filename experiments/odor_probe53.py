"""Exploratory, not pre-registered: with 4-methylcyclohexanol's untested receptors given the input flies' PN responses
imply, does it come as close to 3-octanol in the model's Kenyon cells as in flies'?

odor_probe50.py: filling the four receptors Barth et al. imaged moved 4-methylcyclohexanol further from 3-octanol (PNs
0.53 to 0.47, Kenyon cells 0.28 to 0.20), its weak fills recruiting more inhibition than they add, and
odor_normalization_check.py: the model's lateral division matches flies'. Seven of the glomeruli where flies' PNs answer
4-methylcyclohexanol significantly (Badel et al. 2016: VM7v, DA3, DL4, DA4l, DL3, DA1, VM3) have receptors no study has
recorded with it, so the model drives them with nothing. receptor_fills.PN_INFERRED gives them the receptor input that
would give Badel et al.'s PN responses (0.0028 DoOR units per % PN ΔF/F, the median of 10 anchors): a stand-in for
missing receptor data, not a measurement, and the same for 3-octanol's four untested glomeruli. With it,
4-methylcyclohexanol's summed receptor drive is 0.61 of 3-octanol's (receptor data alone 0.48) and reaches 16 glomeruli
above 0.1 (3-octanol 22; flies' PNs: 18 and 13 significant).
Model: odor_probe52.py's (its cache) with mb_calibration.py's mushroom body.
Measured, with the receptor fills alone and with the PN-inferred tier too: odor_equalization_check.py's measures and
odor_probe36.measure's (Kenyon cells by class and odor, overlap, MBON11). Seeds 620000 (odor_probe36.measure) and 630000
(equalization) + 100000 x condition.

    python experiments/odor_probe53.py         (writes experiments/odor_probe53.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe52 as p52
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 620000, 630000


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe52", p52.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o), "conditions": {}}
    for c, pn_inferred in enumerate((False, True)):
        name = "receptor and PN-inferred fills" if pn_inferred else "receptor fills"
        with receptor_fills.applied(pn_inferred=pn_inferred) as fills, warm.tracking(o, rec):
            entry = {"fills": fills, "equalization": eq.measure(o, rec, EQUALIZATION_SEED + 100000 * c)}
            out["conditions"][name] = entry
            OUT.write_text(json.dumps(out, indent=1))
            entry.update(p36.measure(o, rec, built, SEED + 100000 * c))
            od = entry["odors"]
            print(name, "KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
                  "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
                  "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in entry["mbon11_input"].items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
