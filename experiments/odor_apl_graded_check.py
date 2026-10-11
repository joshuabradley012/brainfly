"""Exploratory check, not pre-registered: with a weaker Kenyon cell-to-APL drive, does the model's APL answer
4-methylcyclohexanol with about half its response to 3-octanol, as flies' does, and hold 3-octanol's Kenyon cells back
more, while silencing it still raises the Kenyon cells' spikes 2-3-fold?

odor_apl_check.py: the model's APL saturates for both odors (its release peaking at 38.3 and 36.3 Hz, its calibrated
maximum, within 100 ms), so it divides their Kenyon cells alike; flies' APL answers 4-methylcyclohexanol with 0.49 of its
calcium response to 3-octanol and brings the odors' Kenyon cell claw responses from 0.65 (peak) and 0.76 (claws
answering) of 3-octanol's with APL silenced to 0.89 and 0.95 with it working (Prisco et al. 2021). mb_calibration.py
multiplies the Kenyon cell-to-APL synapses by 10, fitted only to the silencing ratio (2.44; flies 2-3, Lin et al. 2014,
Bergmann et al. 2026); what saturates APL is that drive.
Model: MODEL's (odor_probe56.py's cache by default) with mb_calibration.py's mushroom body, the Kenyon cell-to-APL
synapses then scaled to 10 (as calibrated), 6, 4 or 2.5 times their MaleCNS weight; nothing else changed (APL's release
from 3.5 mV, its ceiling, its synapses onto the Kenyon cells). odor_apl_check.trial's protocol and measures (a 1 s odor
after 1.5 s, DoOR's input, 2 seeds of 8 flies, the same for every scale), with APL working and silenced.
Measured for each scale: APL's release (peak and mean over the odor) for both odors and its 4-methylcyclohexanol/3-octanol
ratio, the Kenyon cells answering and their evoked spikes for both odors, with APL working and silenced, and the ratio
silencing gives.

    python experiments/odor_apl_graded_check.py [cache name]      (writes experiments/odor_apl_graded_check.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_apl_check as ac
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe56 as p56
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 820000
SCALES = (10.0, 6.0, 4.0, 2.5)
BUILDS = {"odor_probe56": p56.build}


def main() -> None:
    t0 = time.perf_counter()
    model = sys.argv[1] if len(sys.argv) > 1 else "odor_probe56"
    if model not in BUILDS:
        BUILDS[model] = __import__(model).build
    o, rec, built = brain_cache.load(model, BUILDS[model], p44.prepare)
    import mb_calibration                              # after the cache, so that its edits don't invalidate it
    b = o.brain
    out = {"question": __doc__, "model": model, "flies": ac.FLIES, "mb_calibration": mb_calibration.apply(o), "scales": {}}
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = o.m["kc"][pre] & np.isin(b.idx, apl)
    calibrated = b.weights.copy()
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for s in SCALES:
            w = calibrated.copy()
            w[kc_apl] *= s / mb_calibration.KC_APL_SCALE
            b.weights, b._external_matrix = w, None
            entry = {}
            for name, silence in (("APL working", ()), ("APL silenced", apl)):
                rows = {odor: ac.summarize([ac.trial(o, rec, odor, SEED + 10 * j + k, apl, silence) for k in range(ac.SEEDS)])
                        for j, odor in enumerate(ac.ODORS)}
                a, c = rows["4-methylcyclohexanol"], rows["3-octanol"]
                rows["mch_over_oct"] = {k: round(a[k] / c[k], 3) if c.get(k) else None for k in c if isinstance(c[k], (int, float))}
                entry[name] = rows
            on, off = entry["APL working"], entry["APL silenced"]
            entry["block_ratio"] = {od: round(off[od]["kc_evoked_spikes"] / max(on[od]["kc_evoked_spikes"], 1e-9), 2) for od in ac.ODORS}
            out["scales"][f"{s:g}"] = entry
            print(f"scale {s:g}: APL working", json.dumps(on["mch_over_oct"]), "| APL silenced", json.dumps(off["mch_over_oct"]),
                  "| APL peak/mean OCT", on["3-octanol"]["apl_release_peak_hz"], on["3-octanol"]["apl_release_mean_hz"],
                  "MCH", on["4-methylcyclohexanol"]["apl_release_peak_hz"], on["4-methylcyclohexanol"]["apl_release_mean_hz"],
                  "| block ratio", json.dumps(entry["block_ratio"]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
