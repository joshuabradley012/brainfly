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

Ran: no; the fills move 4-methylcyclohexanol further from 3-octanol. Its summed receptor response rises from 0.39 of
3-octanol's to 0.41 (the first 0.5 s), but its PNs' falls from 0.53 to 0.47 (0.51 to 0.42 over the second) and its
Kenyon cells' from 0.28 to 0.20 (3-octanol 8.9% to 10.7% of Kenyon cells, 4-methylcyclohexanol 2.5% to 2.2%; flies
0.85-0.98 and 0.73-0.92). 3-octanol's one fill is strong (VM2 0.69): VM2's PNs answer at 89 spikes/s and the odor reaches
15 glomeruli over 10 spikes/s (14). 4-methylcyclohexanol's four are weak (0.12-0.175): their PNs answer at 28 (VC1), 26
(VM2), 9.5 (VA7l) and 0 (VC3) spikes/s, while the extra input recruits more lateral inhibition and every glomerulus the
odor already drove answers less (D 98 to 91, VA3 74 to 67, DL1 53 to 45, VM5d 27 to 20), so its PNs' summed response
falls (2175 to 1958 spikes/s) and it still reaches 9 glomeruli over 10 spikes/s (flies 18). In this model adding weak
input to a broad odor costs the other glomeruli more than it brings, where flies' antennal lobe makes 4-methylcyclohexanol's
weak, broad input nearly as effective as 3-octanol's strong one. MBON11 gains 17.6 and 6.2 spikes (odor_probe49.py 17.1
and 6.1); 53% of 4-methylcyclohexanol's responders also answer 3-octanol (flies 30-33%).

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
