"""Exploratory, not pre-registered: with the receptor input DoOR lacks filled from Barth et al.'s receptor imaging, how
far does 4-methylcyclohexanol come toward 3-octanol in the PNs and the Kenyon cells?

odor_equalization_check.py: the model's antennal lobe raises 4-methylcyclohexanol from 0.39 of 3-octanol's summed
receptor response to 0.52 at the PNs (flies about 0.45 to 0.85-0.98), and to 0.26 at the Kenyon cells (flies 0.73-0.92).
DoOR has no 4-methylcyclohexanol data for 13 of the receptors with 3-octanol data, and the model drives them with
nothing; Barth et al. 2014's receptor neuron imaging shows the odor weakly exciting four of them (receptor_fills.py: VC1,
VC3, VM2, VA7l), and 3-octanol strongly exciting VM2, which DoOR has no data for either. The fills keep the input
receptor-like (summed 0.48 of 3-octanol's; DoOR alone 0.445), but the antennal lobe may amplify weak, broad input more
than it does strong input (research_notes/Rung 9 learning data/weak_input_gain.md, section 8: with flies' transform the
fills lift the summed PN ratio from 0.64 to 0.75).
Model: odor_probe49.py's (its cache) with mb_calibration.py's mushroom body, settled starts as it carries them.
Measured, with the fills: odor_equalization_check.py's measures, and odor_probe36.measure's (the Kenyon cells' responses
to six odors by class, their overlap, MBON11's input and spikes). Seeds 580000 for odor_probe36.measure, 590000 for the
equalization; odor_probe49.py's measures are the same model without the fills.

    python experiments/odor_probe50.py         (writes experiments/odor_probe50.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import mb_calibration
import odor_equalization_check as eq
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe49 as p49
import receptor_fills
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 580000, 590000


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe49", p49.build, p44.prepare)
    out = {"question": __doc__, "fills": receptor_fills.FILLS, "mb_calibration": mb_calibration.apply(o)}
    with receptor_fills.applied(), warm.tracking(o, rec) as held:
        out["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
        OUT.write_text(json.dumps(out, indent=1))
        out.update(p36.measure(o, rec, built, SEED))
        print("KCs", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in out["odors"].items()}),
              "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in out["mbon11_input"].items()}), flush=True)
        out["measure_settles"] = held["settles"]
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
