"""Exploratory check, not pre-registered: with APL's drive from the Kenyon cells weaker and its synapses onto them stronger,
can APL answer 4-methylcyclohexanol with about half its response to 3-octanol (flies 0.49) and still raise the Kenyon
cells' spikes 2-3-fold when silenced?

odor_apl_graded_check.py: weakening the Kenyon cell-to-APL drive alone (from 10 to 2.5 times) leaves 3-octanol at APL's
ceiling (38 Hz) and brings 4-methylcyclohexanol's peak only to 0.74 of it, while silencing APL then raises the Kenyon cells'
spikes only 1.7-fold (flies 2-3; Lin et al. 2014, Bergmann et al. 2026). Prisco et al. 2021: flies' APL calcium answers
4-methylcyclohexanol with 0.49 of 3-octanol's, and the Kenyon cells' claws answering go from 0.76 of 3-octanol's with APL
silenced to 0.95 with it working.
Model: odor_probe60.py's (its cache) with mb_calibration.py's mushroom body, then the Kenyon cell-to-APL synapses at s
times their MaleCNS weight (calibrated: 10) and APL's synapses onto the Kenyon cells g times their calibrated weight (so
APL's ceiling holds the Kenyon cells g x 11 mV down), for s in 2.5, 1.5, 1 and g in 1.5, 2.5. odor_apl_check.trial's
protocol and measures (DoOR's input, 2 seeds of 8 flies), APL working and silenced.
Measured for each pair: APL's release peak and mean for both odors and their ratio, the Kenyon cells answering and their
spikes (4-methylcyclohexanol against 3-octanol) with APL working and silenced, and the ratio silencing gives.

Ran: yes, with the drive at 1.5 and the synapses onto the Kenyon cells at 2.5. Then APL's release peaks at 31.1 Hz for
3-octanol and 14.5 for 4-methylcyclohexanol (0.47; flies 0.49), silencing APL raises the Kenyon cells' spikes 2.45 and
2.05-fold (flies 2-3), and the Kenyon cells answering 4-methylcyclohexanol are 0.55 of 3-octanol's with APL working and
0.43 with it silenced: APL equalizes the odors 1.29-fold, as flies' does (claws 0.95 against 0.76, 1.25-fold; Prisco et al.
2021), where the calibrated APL (10, 1) saturated for both (0.99) and equalized 0.36 against 0.44. Across the grid APL's
ratio falls with the drive (0.65 at 2.5 and 1.5 to 0.44 at 1 and 2.5) and the silencing ratio rises with the synapses
(1.6-2.2 at 1.5 times, 2.0-3.0 at 2.5); only 1.5 and 2.5 meets both of flies' numbers (2.5 and 2.5: 0.55, 2.5-3.0). The
Kenyon cells still get less of 4-methylcyclohexanol than flies' before APL acts (0.43 against 0.76 of 3-octanol's,
with APL silenced). mb_calibration2.py installs the pair.

    python experiments/odor_apl_two_knob_check.py      (writes experiments/odor_apl_two_knob_check.json)
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
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 830000
PAIRS = [(s, g) for s in (2.5, 1.5, 1.0) for g in (1.5, 2.5)]


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that its edits don't invalidate it
    b = o.brain
    out = {"question": __doc__, "flies": ac.FLIES, "mb_calibration": mb_calibration.apply(o), "pairs": {}}
    apl = b.cells(["APL"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = o.m["kc"][pre] & np.isin(b.idx, apl)
    apl_kc = np.isin(pre, apl) & o.m["kc"][b.idx]
    calibrated = b.weights.copy()
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for s, g in PAIRS:
            w = calibrated.copy()
            w[kc_apl] *= s / mb_calibration.KC_APL_SCALE
            w[apl_kc] *= g
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
            out["pairs"][f"s {s:g}, g {g:g}"] = entry
            print(f"s {s:g}, g {g:g}: APL peak OCT {on['3-octanol']['apl_release_peak_hz']} MCH {on['4-methylcyclohexanol']['apl_release_peak_hz']}"
                  f" (ratio {on['mch_over_oct']['apl_release_peak_hz']}, mean ratio {on['mch_over_oct']['apl_release_mean_hz']}) | KCs answering"
                  f" MCH/OCT {on['mch_over_oct']['kcs_answering']} (silenced {off['mch_over_oct']['kcs_answering']}), spikes"
                  f" {on['mch_over_oct']['kc_evoked_spikes']} | OCT KCs {on['3-octanol']['kcs_answering']} | block ratio {json.dumps(entry['block_ratio'])}",
                  flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
