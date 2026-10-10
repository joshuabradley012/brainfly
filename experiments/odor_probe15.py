"""Exploratory, not pre-registered: with the antennal lobe's cholinergic local neurons no longer exciting projection
neurons chemically, does matching each Kenyon cell's excitability to its own input make its odor responses specific?

Each change alone helps partway. odor_probe14.py: removing the cholinergic local neurons' synapses onto projection
neurons (PNs), which in flies excite PNs only electrically and weakly (Yaksi & Wilson 2010), ends the onset spillover
into undriven glomeruli; 3.7-16.2% of Kenyon cells respond (flies 6 +- 5%) and the mean Jaccard over odor pairs falls
from 0.43 to 0.35, but 82% of 4-methylcyclohexanol's responders still answer 3-octanol. odor_probe13.py: setting each
Kenyon cell's distance below threshold from its own drive over 30 training odors brings the mean Jaccard to 0.35 and
puts alpha'/beta' cells 9 mV nearer threshold than alpha/beta, as measured (5.5-13 mV).
Conditions, each with odor_probe14.py's removal (each PN's bias raised by the resting input it lost) and the Kenyon
cells' rest recalibrated:
  no cholinergic LN->PN            odor_probe14.py's condition, on new seeds
  + matched                        odor_probe13.py's matching across all Kenyon cells, from the training panel's drives
                                   in this antennal lobe
  + matched within types           the same within each type
Measured as odor_probe13.py measures. Seeds 80000 + 100 x condition + odor (Turner's protocol), + 50 + odor (Hige's),
+ 90 (each type's rest), + 80 (each cell's), + 95 (the resting brain), + 97 (the PNs' resting rates); the training
panel 80500 + odor.

Ran: the two help together, a little more than either alone. With matching across all cells, 4.9-10.3% of Kenyon cells
respond to each odor, inside flies' 6 +- 5% for all six; alpha/beta cells respond at 2.6-6.7% and alpha'/beta' at
6.5-8.6% (flies: about 3-8 and 9-14%), alpha'/beta' again landing 9 mV nearer threshold than alpha/beta (16.2 against
25.2 mV). gamma cells still respond too often (6.8-15.2%; flies about 2%). The overlap falls only somewhat: the mean
Jaccard over odor pairs is 0.31 (0.34 with the correction alone, 0.30 matched within types), 58% of 4-methylcyclohexanol's
responders also answer 3-octanol (71% within types), and 40-44 cells answer all six odors. MBON11 gains -0.2-2.2 spikes,
less than before, and Kenyon cells rest at 0.07 Hz. A static check (each Kenyon cell's input, normalized by its total,
with the top share for each odor responding) shows why the overlap can't go much lower here: with odor_probe12.py's PN
patterns even that ideal layer has 70-77% of 4-methylcyclohexanol's responders answering 3-octanol, against 33% with
DoOR's receptor patterns. The PNs, not the Kenyon cells, now set most of the overlap.

    python experiments/odor_probe15.py         (writes experiments/odor_probe15.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe11 as p11
import odor_probe13 as p13
import odor_probe14 as p14
import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 80000
CONDITIONS = ("no cholinergic LN->PN", "+ matched", "+ matched within types")


def prepare(o: p7.Olfaction, base: int) -> dict:
    """odor_probe7's current model, odor_probe14's removal, each Kenyon cell type's rest at 21.5 mV."""
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    out["removed"] = p14.remove(o, p14.cholinergic_ln_edges(o), base + 97)
    out["kc_rest_recalibration"] = p3.set_kc_rest(o.s, o.m["kc"], o.types, o.own_bias(), base + 90)[-1]
    return out


def training_drives(o: p7.Olfaction) -> np.ndarray:
    """odor_probe13.training_drives on this probe's seeds."""
    e, slot, pre, _, _, _ = p11.pn_input(o)
    kc = np.flatnonzero(o.m["kc"])
    w = o.brain.weights[e].astype(np.float64)
    out = []
    for k, odor in enumerate(p13.TRAINING):
        r = p7.run(o, odor, SEED + 500 + k, 0.5, 1.5)
        early = (r["first"] / 0.1 - r["rest"]).mean(0)
        out.append(np.bincount(slot, w * early[pre[e]], len(kc)))
        print("training", odor, f"PN rise {early[o.m['upn']].mean():.1f} Hz", flush=True)
    return np.array(out)


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    out = {"question": __doc__, "flies": p7.FLIES, "training": list(p13.TRAINING), "conditions": {}}
    prepare(o, SEED + 90)
    drives = training_drives(o)
    for c, name in enumerate(CONDITIONS):
        base = SEED + 100 * c
        entry = prepare(o, base)
        if name != "no cholinergic LN->PN":
            target = p13.gaps(o, drives, name == "+ matched within types")
            entry["target_gap_mv"] = {"mean": round(float(target.mean()), 2), "sd": round(float(target.std()), 2),
                                      "clipped_low": int((target <= p13.LOW).sum()), "clipped_high": int((target >= p13.HIGH).sum()),
                                      **{cn: round(float(target[np.char.startswith(o.types[o.m["kc"]], p)].mean()), 2)
                                         for cn, p in p7.CLASSES.items()}}
            entry["kc_rest_each"] = p11.set_each_rest(o, target, base + 80)
        entry.update(p13.measure(o, name, base))
        out["conditions"][name] = entry
        pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "shares_in_other": entry["mean_share_in_other"],
                                "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
