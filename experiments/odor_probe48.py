"""Exploratory, not pre-registered: with the gamma Kenyon cells' threshold where Chen et al. measured it instead of where
Inada et al. did, do the gamma cells respond as rarely as flies'?

odor_probe47.py (the model with the mushroom body calibrated class by class, mb_calibration.py): alpha'/beta' cells
respond most, as in flies (17.7% to 3-octanol; flies about 20% at Hige et al.'s stimulus), alpha/beta 9.0% (about 6%),
but gamma 15.5%, where flies' respond least (about 3.5% at Hige's stimulus; Turner et al. 2008: about 2%, and 1 of 15
gamma cells spiked to odors). Its classes' resting distances below threshold follow Inada et al. 2017 (from a -60 mV hold:
alpha/beta 21.5 mV, alpha'/beta' 16, gamma 24), the low end of the measured range for gamma: Chen et al. 2026 found gamma
cells' threshold 11 mV above alpha/beta cells' (-22 against -33 mV), and Inada's gamma cells fire least above threshold
(research_notes/Rung 9 learning data/kc_classes_and_apl.md).
Model: odor_probe44.py's (its cache) with mb_calibration.py's calibration, settled starts, and the Kenyon cells' resting
gaps set with alpha/beta at 21.5 mV (Inada's and Turner et al.'s), alpha'/beta' at 16 (Inada's) and gamma at alpha/beta's
plus 6.5 or 11 mV (Chen's); odor_probe47.py is the same with +2.5 (Inada's). The choice between them, stated before
running: the one whose gamma cells respond to 3-octanol nearest 3.5%, the measured range being 2.5-11 mV.
Measured for each: everything odor_probe36.py measures. Seeds 510000 + 1000 x condition (odor_probe40.py's offsets).

Ran: Chen's offset is the one chosen, and with it the classes respond in flies' order. Gamma cells answer 3-octanol at
15.5% with Inada's +2.5 mV (odor_probe47.py), 11.0% with +6.5 and 6.2% with +11 (flies about 3.5%), across six odors
1.7-7.7% with +11; alpha'/beta' (17.6% to 3-octanol) and alpha/beta (9.1%) barely move. With +11 all Kenyon cells respond
at 2.5-13.1% (flies 6 +- 5%), mean Jaccard 0.16, the responding cells firing 1.7-3.3 spikes per response (alpha/beta;
flies 2.2 +- 1.2), 2.5-4.6 (alpha'/beta'; flies 4.9 +- 3.0) and 1.2-1.7 (gamma). With fewer gamma cells answering,
MBON11's input falls (3-octanol 145 pC per cell with +6.5, 102 with +11; flies about 250) and with it its spikes (30 and
23; flies 118); 4-methylcyclohexanol 26 pC and 9 spikes with +11 (flies about 265 and 110). mb_calibration.py now sets
these gaps.

    python experiments/odor_probe48.py         (writes experiments/odor_probe48.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import mb_calibration
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 510000
GAMMA_OFFSETS_MV = (6.5, 11.0)
ALPHA_BETA_MV, ALPHA_PRIME_MV = 21.5, 16.0
PLAIN_GAPS = p8.class_gaps


def gaps_for(gamma_offset: float):
    def class_gaps(o, offsets) -> dict:
        types = o.types[o.m["kc"]]
        out = {}
        for t in np.unique(types):
            if t.startswith("KCab"):
                out[t] = ALPHA_BETA_MV
            elif t.startswith("KCa'b'"):
                out[t] = ALPHA_PRIME_MV
            elif t.startswith("KCg"):
                out[t] = ALPHA_BETA_MV + gamma_offset
            else:
                out[t] = ALPHA_BETA_MV
        return out
    return class_gaps


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o), "conditions": {}}
    try:
        with warm.tracking(o, rec):
            for c, g in enumerate(GAMMA_OFFSETS_MV):
                p8.class_gaps = gaps_for(g)
                entry = {"gamma_offset_mv": g}
                entry.update(p36.measure(o, rec, built, SEED + 1000 * c))
                out["conditions"][f"{g:g}"] = entry
                print(f"gamma +{g:g} mV:", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                      "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in entry["mbon11_input"].items()}), flush=True)
                OUT.write_text(json.dumps(out, indent=1))
    finally:
        p8.class_gaps = PLAIN_GAPS
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
