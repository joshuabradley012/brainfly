"""Exploratory check, not pre-registered: with APL answering the odors in proportion instead of saturating, does it equalize
4-methylcyclohexanol with 3-octanol in the Kenyon cells as flies' APL does?

odor_apl_check.py: the model's APL releases at its ceiling (38.3 Hz) for both odors within 100 ms (peak ratio 0.95, mean
over the odor 0.71), so it scales both odors' Kenyon cells down alike (silencing it raises their spikes 2.42 and 2.39-fold)
and 4-methylcyclohexanol's Kenyon cells stay at a quarter of 3-octanol's. Flies' APL answers 4-methylcyclohexanol with
half its calcium response to 3-octanol (43 against 88 %max; Prisco et al. 2021) and holds 3-octanol's claws back more
(claws answering 0.76 of 3-octanol's without APL, 0.95 with it). APL's graded release rises 6 Hz per mV above 3.5 mV, a
default nothing measures (mb_calibration.py fits only its ceiling, from Inada et al.'s -11 mV, and the Kenyon cell
synapses' scale, 10, to the 2-3-fold block effect).
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body and the Kenyon cells' rest as the learning
pilots set it, APL's gain (Hz per mV above its release onset) at 1, 2, 3 or 6 and its Kenyon cell synapses at 3, 10 or 30
times their rung 4 strength; its release onset (3.5 mV) and ceiling (38.3 Hz) kept.
Measured for each, as odor_apl_check.py (one seed of 8 flies, 680000 + 10 x odor, the same for every condition): APL's
release (peak and mean over the odor) and the Kenyon cells answering and their evoked spikes, for 3-octanol and
4-methylcyclohexanol, with APL working and silenced. Chosen, as stated before running: the condition nearest both flies'
block effect (2.5) and APL's ratio (0.49 of 3-octanol's mean release), by the sum of their squared log ratios; the Kenyon
cells' equalization is then the test.

    python experiments/odor_apl_range_check.py      (writes experiments/odor_apl_range_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_apl_check as ac
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe54 as p54
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 680000
GAINS = (1.0, 2.0, 3.0, 6.0)
SCALES = (3.0, 10.0, 30.0)
BLOCK, APL_RATIO = 2.5, 0.49


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import mb_calibration                              # after the cache, so that its edits don't invalidate it
    cal = mb_calibration.apply(o)
    b, m = o.brain, o.m
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, apl))
    w10 = b.weights.copy()                             # mb_calibration's: Kenyon cell synapses onto APL x 10
    out = {"question": __doc__, "mb_calibration": cal, "conditions": {}}
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for g in GAINS:
            for s in SCALES:
                w = w10.copy()
                w[kc_apl] *= s / mb_calibration.KC_APL_SCALE
                b.weights, b._external_matrix = w, None
                b.set_type("APL", gain=g)
                row = {}
                for name, silence in (("on", ()), ("off", apl)):
                    row[name] = {odor: ac.summarize([ac.trial(o, rec, odor, SEED + 10 * j, apl, silence)])
                                 for j, odor in enumerate(ac.ODORS)}
                on, off = row["on"], row["off"]
                oc, mc = "3-octanol", "4-methylcyclohexanol"
                block = {od: off[od]["kc_evoked_spikes"] / max(on[od]["kc_evoked_spikes"], 1e-9) for od in ac.ODORS}
                ratio = on[mc]["apl_release_mean_hz"] / max(on[oc]["apl_release_mean_hz"], 1e-9)
                score = float(np.log(np.mean(list(block.values())) / BLOCK) ** 2 + np.log(ratio / APL_RATIO) ** 2)
                row.update({"gain_hz_per_mv": g, "kc_apl_scale": s, "block_ratio": {k: round(v, 2) for k, v in block.items()},
                            "apl_mean_ratio": round(ratio, 3), "score": round(score, 4),
                            "kc_answering_ratio_on": round(on[mc]["kcs_answering"] / max(on[oc]["kcs_answering"], 1), 3),
                            "kc_answering_ratio_off": round(off[mc]["kcs_answering"] / max(off[oc]["kcs_answering"], 1), 3),
                            "kc_spike_ratio_on": round(on[mc]["kc_evoked_spikes"] / max(on[oc]["kc_evoked_spikes"], 1e-9), 3)})
                out["conditions"][f"gain {g:g}, scale {s:g}"] = row
                print(f"gain {g:g} scale {s:g}:", json.dumps({k: row[k] for k in ("block_ratio", "apl_mean_ratio", "score",
                      "kc_answering_ratio_on", "kc_answering_ratio_off", "kc_spike_ratio_on")}),
                      "APL peak/mean", json.dumps({od[:6]: (on[od]["apl_release_peak_hz"], on[od]["apl_release_mean_hz"]) for od in ac.ODORS}),
                      "KCs", json.dumps({od[:6]: on[od]["kcs_answering"] for od in ac.ODORS}), flush=True)
                OUT.write_text(json.dumps(out, indent=1))
    best = min(out["conditions"], key=lambda k: out["conditions"][k]["score"])
    out["chosen"] = best
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("chosen:", best, f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
