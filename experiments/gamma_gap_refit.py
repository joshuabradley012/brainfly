"""Exploratory, written before it runs: odor_probe48.py's choice of the gamma Kenyon cells' resting distance below
threshold, made again on the corrected input (mb_calibration6.py).

odor_probe48.py chose the gamma cells' gap as alpha/beta's 21.5 mV plus 11 mV (Chen et al. 2026), from the measured
2.5-11 mV, by the rule "the one whose gamma cells respond to 3-octanol nearest 3.5%" (flies at Hige et al.'s stimulus;
Turner et al. 2008 about 2%). It made the choice with the projection neuron input a third stronger than flies'
(kc_input_audit.py): gamma cells answered 15.5, 11.0 and 6.2% at +2.5, +6.5 and +11 mV. At the measured input
(kc_epsp_check.py, learning_pilot16.py) all the Kenyon cells answer less, and MBON11, which takes two thirds of its
Kenyon cell synapses from gamma cells, gets under a third of flies' charge. The rule stays; only the input has changed.
Model: the corrected model (odor_probe60.py's cache, mb_calibration6.apply, receptor_fills.RECOMMENDED), with the
classes' gaps alpha/beta 21.5 mV, alpha'/beta' 16 and gamma 21.5 plus 2.5, 6.5 or 11 mV (as odor_probe48.py set them),
each rest set with kc_rest.fit.
Measured for 3-octanol and 4-methylcyclohexanol as odor_probe7.measure_odor measures (odor_probe48.py's measure: the
share of each class responding by Turner et al.'s criterion, odor_probe10's runner), seeds 510000 + 1000 x condition
(odor_probe48.py's).
Read as (written before the run): odor_probe48.py's rule. The offset whose gamma cells respond to 3-octanol nearest
3.5% is chosen. If it isn't 11 mV, mb_calibration7.py adopts it and learning_pilot17.py runs rung 9's test on it.

Ran (2026-10-11, 5 minutes): 11 mV again, so mb_calibration6.py stands. By Turner et al.'s criterion the gamma cells
answer 3-octanol at 9.8, 5.9 and 2.5% at +2.5, +6.5 and +11 mV (flies about 3.5%), and +11 is nearest. At +11 the
corrected input gives the classes flies' densities:
- 3-octanol: alpha/beta 7.2% (flies about 6), alpha'/beta' 17.8% (about 20) and gamma 2.5% (about 3.5), 7.2% of all
  Kenyon cells (flies 6 +- 5%). With the input a third too strong, odor_probe48.py had alpha/beta at 9.1% and gamma at
  6.2%.
- 4-methylcyclohexanol: alpha/beta 0.8%, alpha'/beta' 3.5% and gamma 0.3%, 1.0% of all, a seventh of 3-octanol's.
So the corrected model's Kenyon cells answer 3-octanol as densely as flies' do, class by class, and the gaps that remain
are 4-methylcyclohexanol's few cells and MBON11's small charge.

    python experiments/gamma_gap_refit.py      (writes experiments/gamma_gap_refit.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import kc_rest
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe7 as p7
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 510000
GAMMA_OFFSETS_MV = (2.5, 6.5, 11.0)
ALPHA_BETA_MV, ALPHA_PRIME_MV = 21.5, 16.0
ODORS = ("3-octanol", "4-methylcyclohexanol")
FLIES_GAMMA = 0.035


def gaps(o, gamma_offset: float) -> dict:
    """odor_probe48.gaps_for's distances: alpha/beta 21.5, alpha'/beta' 16, gamma 21.5 + offset, other Kenyon cells 21.5."""
    out = {}
    for t in np.unique(o.types[o.m["kc"]]):
        out[t] = (ALPHA_PRIME_MV if t.startswith("KCa'b'") else ALPHA_BETA_MV + gamma_offset if t.startswith("KCg")
                  else ALPHA_BETA_MV)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration6                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration6.apply(o), "conditions": {}}
    runner = p10.make_runner(rec)
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        for c, g in enumerate(GAMMA_OFFSETS_MV):
            base = SEED + 1000 * c
            entry = {"gamma_offset_mv": g, "kc_rest": kc_rest.fit(o, rec, gaps(o, g), base + 900), "odors": {}}
            for k, odor in enumerate(ODORS):
                row, _ = p7.measure_odor(o, odor, base + k, base + 50 + k, (), p10.PEAK_HZ, runner)
                entry["odors"][odor] = {key: row[key] for key in ("kc_share", "kc_share_by_class", "spikes_per_response",
                                                                  "kc_share_1spike_1s", "evoked_spikes_0_1.4s")}
            out["conditions"][f"{g:g}"] = entry
            print(f"gamma +{g:g} mV:", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
    share = {g: out["conditions"][f"{g:g}"]["odors"]["3-octanol"]["kc_share_by_class"]["gamma"] for g in GAMMA_OFFSETS_MV}
    chosen = min(GAMMA_OFFSETS_MV, key=lambda g: abs(share[g] - FLIES_GAMMA))
    out["choice"] = {"gamma_share_3_octanol": {f"{g:g}": share[g] for g in GAMMA_OFFSETS_MV}, "flies": FLIES_GAMMA,
                     "chosen_offset_mv": chosen}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print("choice:", json.dumps(out["choice"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
