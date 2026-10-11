"""Exploratory, written before it runs: apl_refit.py's choice made on the receptor input rung 9 runs on
(receptor_fills.RECOMMENDED), with one more drive below the grid's edge.

apl_refit.py made odor_apl_conductance2_check.py's choice of APL's strength and drive again on the corrected Kenyon cell
input, and chose the Kenyon cells' drive onto APL at half MaleCNS's weight (mb_calibration7.py). A review found two
problems with how it was run:
- It ran that check's protocol on DoOR's input, as the check did. But rung 9's learning test runs on
  receptor_fills.RECOMMENDED, the input the evidence supports, where APL's ratio moved toward flies' with the corrected
  input (0.28 at 1.90 mV, 0.31 at 1.4 mV; kc_epsp_check.py), not away (0.53 to 0.36 on DoOR). And on RECOMMENDED,
  silencing APL at drive 1 already raised 4-methylcyclohexanol's spikes only 2.01-fold, at the edge of the rule.
- Drive 0.5, the one chosen, is the grid's lowest.
Both refits, and learning_pilot17.py, were decided after learning_pilot16.py's result. kc_epsp_check.py's own plan,
written before its run, refitted APL only if silencing left 2-3-fold, which it hadn't.
Model: apl_refit.py's (odor_probe60.py's cache, mb_calibration.apply, mb_calibration6.correct before APL is installed,
the rest set with kc_rest.fit), on receptor_fills.RECOMMENDED. Its twelve conditions plus drive 0.25 at strength 1,
reversal -20 mV:
- strength 1, reversal -20 mV: drive 0.25, 0.5, 1, 1.5 and 2.5 times MaleCNS's;
- strength 1, reversal -15 mV: drive 0.5, 1 and 1.5;
- strength 2, reversal -20 mV: drive 1.5, 2.5, 4, 6 and 10.
Measured as it measures (odor_apl_conductance_check.condition; 2 seeds of 8 flies, seeds 870000).
Read as (written before the run): the same rule (odor_apl_conductance_check.score) chooses among the thirteen. If it
chooses drive 1 (mb_calibration6.py's APL), mb_calibration7.py is withdrawn and mb_calibration6.py stays the model
(learning_pilot16.py its test). If it chooses drive 0.5, mb_calibration7.py stands (learning_pilot17.py its test).
Anything else: mb_calibration8.py takes it and learning_pilot18.py runs rung 9's test on it.

    python experiments/apl_refit2.py      (writes experiments/apl_refit2.json)
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import kc_rest
import odor_apl_conductance2_check as cc2
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS, TAU, PIPETTE_MV = cc2.SEED, cc2.SEEDS, cc2.TAU, cc2.PIPETTE_MV
ODORS = cc2.ODORS
NOW = "strength 1, reversal -20, drive 1"


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import mb_calibration4
    import mb_calibration6
    import receptor_fills
    b = o.brain
    out = {"question": __doc__, "flies": cc2.FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}, "inada_5b": {}}
    out["correction"] = mb_calibration6.correct(o)
    apl = b.cells(["APL"])
    calibrated = b.weights.copy()
    held = []                                          # every weight array installed, so that no new one reuses an old id
    conductance_for, effect_of = cc2.conductance_for, cc2.effect_of
    g1, g15, g2 = conductance_for(cc.CEILING_MV, -20.0), conductance_for(cc.CEILING_MV, -15.0), conductance_for(cc.CEILING_MV, PIPETTE_MV)
    conditions = ([(f"strength 1, reversal -20, drive {d:g}", d, g1, -20.0, TAU, "1") for d in (0.25, 0.5, 1.0, 1.5, 2.5)]
                  + [(f"strength 1, reversal -15, drive {d:g}", d, g15, -15.0, TAU, "1") for d in (0.5, 1.0, 1.5)]
                  + [(f"strength 2, reversal -20, drive {d:g}", d, g2, -20.0, TAU, "2") for d in (1.5, 2.5, 4.0, 6.0, 10.0)])
    own_bias = o.own_bias().copy()
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        for name, drive, g, reversal, tau, strength in conditions:
            effect = effect_of(g, reversal)
            held += [b.weights, b.slow_weights]
            reversals = mb_calibration4.install(o, drive, effect, reversal, calibrated, tau)
            b.set_bias(own_bias)
            kc_rest_ = kc_rest.fit(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            off = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            row = cc.condition(on, off)
            row.update({"kc_rest": kc_rest_, "reversal_mv_by_type": reversals, "drive": drive, "effect": round(effect, 3),
                        "reversal_mv": reversal, "tau_s": tau, "strength": strength, "conductance_x_leak": round(g, 3)})
            out["conditions"][name] = row
            a, c = row["3-octanol"], row["4-methylcyclohexanol"]
            print(f"{name}: APL peak {a['apl_release_peak_hz']}/{c['apl_release_peak_hz']} (ratio {row['apl_peak_mch_over_oct']})"
                  f" | block {a['block_ratio']}/{c['block_ratio']} | KCs {a['kcs_answering']}/{c['kcs_answering']}"
                  f" | equalization {row['answering_mch_over_oct']['equalization']} | both {row['share_answering_both']}"
                  f" ({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, indent=1, default=float))
        chosen = min(out["conditions"], key=lambda k: cc.score(out["conditions"][k]))
        out["chosen"] = {"condition": chosen, "meets_block_ratio": not cc.score(out["conditions"][chosen])[0],
                         "differs_from_mb_calibration4": chosen != NOW, "input": "receptor_fills.RECOMMENDED"}
        print("chosen:", json.dumps(out["chosen"]), flush=True)
        _, drive, g, reversal, tau, _ = next(c for c in conditions if c[0] == chosen)
        held += [b.weights, b.slow_weights]
        mb_calibration4.install(o, drive, effect_of(g, reversal), reversal, calibrated, tau)
        b.set_bias(own_bias)
        kc_rest.fit(o, rec, p8.class_gaps(o, None), SEED + 900)
        res = cc2.apl_drive(o, rec, SEED + 5000, apl)
        out["inada_5b"][chosen] = res
        print("Inada 5B:", json.dumps({k: v for k, v in res.items() if k != "course_mv"}), flush=True)
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
