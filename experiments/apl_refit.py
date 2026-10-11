"""Exploratory, written before it runs: odor_apl_conductance2_check.py's choice of APL's strength and drive, made again on
the corrected Kenyon cell input (mb_calibration6.py).

odor_apl_conductance2_check.py chose APL's conductance (strength 1 at a reversal 20 mV below rest, 1.22 times the Kenyon
cell's leak at APL's ceiling) and the Kenyon cells' drive onto it (MaleCNS's weight) by the rule: among the conditions
whose silencing raises both odors' Kenyon cell spikes 2-3-fold, the one whose APL peak ratio (4-methylcyclohexanol over
3-octanol) is nearest flies' 0.49. It made the choice with the projection neuron input a third stronger than flies'
(kc_input_audit.py). At the measured input (kc_epsp_check.py) silencing APL still raises the spikes 2.77 and 2.01-fold,
but APL's ratio is 0.31, where the choice gave 0.53. gamma_gap_refit.py has kept the other fit made with the strong
input, the gamma cells' gap. The rule stays; only the input has changed.
Model: as odor_apl_conductance2_check.py's (odor_probe60.py's cache, mb_calibration.apply), with mb_calibration6.correct
applied before APL is installed in each condition (the projection neuron synapses at 1.4 mV per spike at full strength,
the Kenyon cells' 20 ms membrane in their type), the rest set with kc_rest.fit. Its twelve conditions:
- strength 1, reversal -20 mV: drive 0.5, 1, 1.5 and 2.5 times MaleCNS's;
- strength 1, reversal -15 mV: drive 0.5, 1 and 1.5;
- strength 2 (the pipette's chloride), reversal -20 mV: drive 1.5, 2.5, 4, 6 and 10.
Measured as it measures (odor_apl_conductance_check.condition; 2 seeds of 8 flies, seeds 870000), and Inada et al.'s Fig.
5B test for the chosen condition.
Read as (written before the run): odor_apl_conductance2_check.py's rule (odor_apl_conductance_check.score) chooses. If
the choice isn't mb_calibration4.py's (strength 1, reversal -20, drive 1), mb_calibration7.py takes its constants with
the corrected input, and learning_pilot17.py runs rung 9's test on it.

Ran (2026-10-11, 27 minutes): the rule chooses a weaker drive. On the corrected input, only strength 1 at -20 mV with
drive 0.5 or 1 raises both odors' spikes 2-3-fold.
- Drive 0.5: 2.37 and 2.36-fold, APL's ratio 0.43, 330 and 97 cells answer. Chosen (flies 2-3 and 0.49).
- Drive 1 (mb_calibration4.py's): 2.77 and 2.57-fold, ratio 0.36, 305 and 91 cells.
- Drive 1.5 raises 3-octanol's spikes 3.03-fold and drive 2.5 3.28-fold (ratio 0.47). At -15 mV silencing raises them
  4.5-6.2-fold. Strength 2 (the pipette's chloride) raises them only 1.3-1.6-fold at every drive, as before.
So mb_calibration7.py takes drive 0.5 with the corrected input. With half the drive APL holds the Kenyon cells back less,
and more answer both odors. 4-methylcyclohexanol's share of answering cells stays 0.29-0.30 of 3-octanol's (flies about
0.92). APL's conductance is unchanged, and Inada et al.'s Fig. 5B test gives what it gave before: 8.1 mV at the
plateau, 10, 50 and 90% of it at 0.02, 0.14 and 0.42 s, half gone 0.37 s after the drive. This check runs
odor_apl_conductance2_check.py's protocol, its seeds and its input (DoOR's, without receptor_fills). That is why drive 1
here gives 305 and 91 cells, where kc_epsp_check.py (the learning pilots' seeds, receptor_fills.RECOMMENDED) gave 299
and 41.

Correction (2026-10-11, after a review):
- This ran odor_apl_conductance2_check.py's protocol on DoOR's input, as that check did. Rung 9's learning test runs on
  receptor_fills.RECOMMENDED, where the corrected input moved APL's ratio toward flies' (0.28 to 0.31), not away (DoOR:
  0.53 to 0.36). There, silencing APL at drive 1 already raised 4-methylcyclohexanol's spikes only 2.01-fold, so drive
  0.5 likely falls under the rule's 2. apl_refit2.py makes the choice on RECOMMENDED.
- Drive 0.5 is the grid's lowest, so it is the grid's best point, not a located optimum. apl_refit2.py adds 0.25.
- "Runs odor_apl_conductance2_check.py's protocol, its seeds and its input": kc_epsp_check.py ran the same protocol
  (odor_apl_conductance_check.trial and condition, 2 seeds of 8 flies). The seeds and the input differ, and the input
  also explains APL's ratio there (0.31 against 0.36 here).
- The first run crashed before measuring anything: mb_calibration6.correct set the Kenyon cells' membrane on a type
  set ("kenyon_cells") that only mb_calibration3.install had defined. correct() now defines it (commit 1acaf7b), and
  this is the second run.
- The account of what was decided when: kc_epsp_check.py's rule, written before its run, kept APL, since its silencing
  effect stayed within 2-3. This refit, and gamma_gap_refit.py, were decided after learning_pilot16.py's result, when a
  review listed the fits made with the strong input.

    python experiments/apl_refit.py      (writes experiments/apl_refit.json)
"""
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
    b = o.brain
    out = {"question": __doc__, "flies": cc2.FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}, "inada_5b": {}}
    out["correction"] = mb_calibration6.correct(o)
    apl = b.cells(["APL"])
    calibrated = b.weights.copy()
    held = []                                          # every weight array installed, so that no new one reuses an old id
    conductance_for, effect_of = cc2.conductance_for, cc2.effect_of
    g1, g15, g2 = conductance_for(cc.CEILING_MV, -20.0), conductance_for(cc.CEILING_MV, -15.0), conductance_for(cc.CEILING_MV, PIPETTE_MV)
    conditions = ([(f"strength 1, reversal -20, drive {d:g}", d, g1, -20.0, TAU, "1") for d in (0.5, 1.0, 1.5, 2.5)]
                  + [(f"strength 1, reversal -15, drive {d:g}", d, g15, -15.0, TAU, "1") for d in (0.5, 1.0, 1.5)]
                  + [(f"strength 2, reversal -20, drive {d:g}", d, g2, -20.0, TAU, "2") for d in (1.5, 2.5, 4.0, 6.0, 10.0)])
    own_bias = o.own_bias().copy()
    with warm.tracking(o, rec):
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
                         "differs_from_mb_calibration4": chosen != NOW}
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
