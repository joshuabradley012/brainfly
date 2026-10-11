"""Exploratory check, not pre-registered and not a change to the model: kc_membrane_check.py's longer membranes and
kc_setc_check.py's Kenyon cell sets again, with the cells' rest held at the same distances below threshold, as both
meant to hold it.

kc_membrane_check.py and kc_setc_check.py set the cells' rest with odor_probe33.set_rest after changing their membrane
time constant and the projection neuron synapses' strength. They left the cells resting closer to threshold than the
targets (alpha/beta 21.5, alpha'/beta' 16 and gamma 32.5 mV): by 1.5-5.1 mV at 50 ms, 1.0-4.3 at 100 ms, 1.5-4.9 in set
C and 6.3-22.8 in set D, where the cells fired at 1-2 spikes/s at rest. Every 20 ms run was within 0.3 mV (kc_rest.py
gives the cause). So part of what those checks credited to integration may come from cells resting nearer threshold.
Model: as kc_setc_check.py's (learning pilot 12's Kenyon cells: odor_probe60.py's cache, mb_calibration4.py's mushroom
body, receptor_fills.RECOMMENDED), in five conditions: A, 20 ms and undepressed (the model now); kc_membrane_check.py's
50 and 100 ms, undepressed, the projection neuron-to-Kenyon cell synapses x 2.03 and 3.69 so that one spike's EPSP peaks
as now; and kc_setc_check.py's C (50 ms, the synapses depressing on their own to 0.85 per spike, recovering over 0.1 s)
and D (189 ms, 0.5 and 0.15 s), scaled as it scaled them. In each, the cells' rest is set with kc_rest.fit (every class
within 0.3 mV of its distance), and the realized distances are recorded.
Measured as kc_setc_check.py measures (2 seeds of 8 flies, the learning pilots' seeds).
Read as (written before the run), the two checks' own readings:
- kc_membrane_check.py: a longer time constant is worth recalibrating the mushroom body around if, with the distances
  to threshold held, 4-methylcyclohexanol's answering cells come nearer 3-octanol's than at 20 ms, and the cells keep
  more of their early firing.
- kc_setc_check.py: a set is worth recalibrating the mushroom body around if 4-methylcyclohexanol's answering cells come
  nearer 3-octanol's than in A while the share of all Kenyon cells answering 3-octanol stays within 6-25% (flies about
  12%) and the cells keep more of their early firing.
And what follows: whichever way set C comes out, learning_pilot15.py runs learning pilot 13 again with the rest held,
since pilot 13's result is in the README; the README's crux entry is corrected by what this check finds.

Ran (2026-10-11, 12 minutes): with the rest held, the longer membranes still make far too many cells answer, set C
half meets kc_setc_check.py's reading, and set D is sparse, not the set that answered everything. Every condition's
rest came to within 0.3 mV of its targets in each class in three passes (every type within 0.9 mV, measured with the
cells firing).
- A (as now) repeats kc_setc_check.py's. 623 and 109 Kenyon cells answer 3-octanol and 4-methylcyclohexanol, 0.18 as
  many and 15.3% of the cells for 3-octanol. 0.52 of 4-methylcyclohexanol's answering cells answer 3-octanol.
- 50 and 100 ms, undepressed (kc_membrane_check.py's):
  - 1,294 and 1,861 cells answer 3-octanol, 32 and 46% of them (with the rest unheld 37 and 51%).
  - 407 and 808 answer 4-methylcyclohexanol, 0.315 and 0.43 as many (unheld 0.37 and 0.49).
  - The cells keep 0.445, 0.535 and 0.29 of their early firing at 50 ms and 0.57, 0.61 and 0.47 at 100 ms
    (alpha/beta, alpha'/beta', gamma; A 0.19, 0.29 and 0.05).
  So kc_membrane_check.py's reading holds with the distances held, and so does its caveat: far too many cells answer.
- C (the synapses x 2.08):
  - 311 and 77 cells answer, 7.7% for 3-octanol (unheld 436 and 121, 10.7%), 0.25 as many (unheld 0.28).
  - Silencing APL raises both odors' spikes 2.4-fold (flies 2-3).
  - 0.61 of 4-methylcyclohexanol's answering cells answer 3-octanol (A 0.52; flies 0.33), and 0.15 of 3-octanol's
    answer 4-methylcyclohexanol (A 0.09; flies 0.30).
  - The alpha/beta and alpha'/beta' cells keep a little more of their early firing (0.22 and 0.31; A 0.19 and 0.29).
    The gamma cells keep less (0.024; A 0.052), and their early rate falls to a sixth of A's (0.10 spikes/s per cell
    against 0.60).
  - Through the slow current MBON11's input would peak at 152 pA, 76 pC (A 419 and 202; flies about 400 and 245-250).
- D (the synapses x 7.75):
  - 187 and 103 cells answer, 4.6% for 3-octanol, under the reading's 6% (unheld 2,905 and 3,109). That is 0.55 as
    many, the nearest of any condition.
  - The cells keep 0.68, 0.58 and 0.39 of their early firing.
  - 0.69 of 4-methylcyclohexanol's answering cells answer 3-octanol, and 0.38 of 3-octanol's answer
    4-methylcyclohexanol (flies 0.30).
  - APL's 4-methylcyclohexanol/3-octanol peak ratio is 0.99 (flies 0.49).
  - The gamma cells barely answer (0.012 spikes/s per cell early), so MBON11's input would be 34 pA, 32 pC.
By kc_setc_check.py's reading neither set qualifies. C brings 4-methylcyclohexanol nearer 3-octanol at flies' density,
but its gamma cells hold less of their firing. D holds the firing and brings the odors nearest, but answers in too few
cells. In every condition 0.52-0.78 of 4-methylcyclohexanol's answering cells answer 3-octanol (flies 0.33): longer
integration enlarges its set mostly by recruiting 3-octanol's cells. Whether pilot 13's reciprocal pass survives the
held rest is learning_pilot15.py's question.

Correction (2026-10-11, after a second independent review):
- The verdict on set C applied "the cells keep more of their early firing" class by class, to 3-octanol only, where
  only the gamma cells keep less (0.024 against 0.052, on a few dozen spikes). The reading names neither a class nor
  an odor. For the cells as a whole (the classes' rates weighted by their cells), set C keeps more: 0.236 of the early
  rate against A's 0.202 for 3-octanol, and 0.226 against 0.129 for 4-methylcyclohexanol, where every class keeps
  more. So set C meets the reading, and by it is worth recalibrating the mushroom body around. Against that, on
  measures it wasn't chosen from: its odor input to MBON11 through the slow current is 76 pC (A 202; flies about
  245-250), and in learning_pilot15.py MBON11 answers at a quarter of flies' strength or less. Set D fails the reading
  on density.
- "At flies' density": set C's 7.7% is inside the reading's band (6-25%), about two thirds of flies' 12%.
- A nearly repeats kc_setc_check.py's (623 and 109 cells against 624 and 111), its rest fitted afresh.
- Longer integration enlarges 4-methylcyclohexanol's set mostly by recruiting 3-octanol's cells at 50 and 100 ms
  undepressed (214 of the 298 cells added, and 572 of 699, answer 3-octanol). In sets C and D its set shrinks (77 and
  103 cells against A's 109), while the share inside 3-octanol's set rises.

    python experiments/kc_setc_check2.py      (writes experiments/kc_setc_check2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import kc_membrane_check as km
import kc_rest
import kc_setc_check as ks
import mb_calibration
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = km.SEED, km.SEEDS
SETS = {"A": (0.020, None, None), "50 ms": (0.050, None, None), "100 ms": (0.100, None, None),
        "C": (0.050, 0.85, 0.10), "D": (0.189, 0.50, 0.15)}           # tau_m, depression, recovery


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    b, m = o.brain, o.m
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "conditions": {}}
    kc = np.flatnonzero(m["kc"])
    cls = {name: mask[kc] for name, mask in mb_calibration.classes(o).items() if name != "other"}
    apl = b.cells(["APL"])
    mbon = np.flatnonzero(o.types == "MBON11")
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    pn_kc = m["upn"][pre] & m["kc"][b.idx]
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    if m["upn"][spre].any():
        raise RuntimeError("projection neurons have slow synapses, which their slow_depression would change")
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mbon))
    syn = np.bincount(np.searchsorted(kc, pre[onto]), weights=b._counts[onto], minlength=len(kc))
    base_w, base_full = b.weights.copy(), b.full_strength.copy()
    held = [base_w]
    ts = -0.5 + (np.arange(190) + 0.5) * p10.PIECE
    tt = (np.arange(300) + 0.5) * p10.PIECE
    kern = np.exp(-tt / km.SLOW[1]) - np.exp(-tt / km.SLOW[0])
    kern /= kern.sum() * p10.PIECE
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        for name, (tau_m, f, recovery) in SETS.items():
            x_rest = ks.resting_strength(f, recovery)
            scale = km.peak_per_w(0.020) / km.peak_per_w(tau_m) / x_rest
            w = base_w.copy()
            w[pn_kc] *= np.float32(scale)
            b.weights, b._external_matrix = w, None
            held.append(w)
            full = base_full.copy()
            if f is None:
                b.own_depression = np.zeros(0, np.bool_)
            else:
                full[pn_kc] = False
                b.own_depression = pn_kc.copy()
                b.set_type("uPN", slow_depression=f, slow_recovery=recovery)
            b.full_strength = full
            b.set_type("kenyon_cells", tau_m=tau_m)
            kc_rest_ = kc_rest.fit(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            off = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            row = cc.condition(on, off)
            row.update({"tau_m_s": tau_m, "depression": f, "recovery_s": recovery, "resting_strength": round(x_rest, 3),
                        "pn_kc_scale": round(float(scale), 3), "kc_rest": kc_rest_, "by_odor": {}})
            for j, od in enumerate(km.ODORS):
                rs = [km.timed(o, rec, od, SEED + 10 * j + k, cls, syn) for k in range(SEEDS)]
                byc = {}
                for c in cls:
                    r = np.mean([x["rates"][c] for x in rs], 0)
                    early, late = r[(ts > 0) & (ts < 0.3)].mean(), r[(ts > 0.5) & (ts < 1.0)].mean()
                    byc[c] = {"hz_per_cell_0_to_0.3s": round(float(early), 3), "hz_per_cell_0.5_to_1s": round(float(late), 3),
                              "late_over_early": round(float(late / max(early, 1e-9)), 3)}
                d = np.mean([x["drive"] for x in rs], 0) / p10.PIECE
                d -= d[ts < 0].mean()
                cur = np.convolve(d, kern)[:len(ts)] * p10.PIECE * km.Q_PC / len(mbon)
                late = float(cur[(ts > 0.6) & (ts < 1.0)].mean())
                row["by_odor"][od] = {"classes": byc, "mbon11_slow_current": {"peak_pa": round(float(cur.max()), 1), "pa_0.6_to_1s": round(late, 1),
                                      "late_over_peak": round(late / max(float(cur.max()), 1e-9), 3), "charge_pc_0_to_1.4s": round(float(cur[(ts > 0) & (ts < 1.4)].sum() * p10.PIECE), 1)}}
            row["share_answering_3_octanol"] = round(row["3-octanol"]["kcs_answering"] / len(kc), 4)
            out["conditions"][name] = row
            a, c_ = row["3-octanol"], row["4-methylcyclohexanol"]
            print(f"{name} (tau_m {tau_m}, {f}/{recovery}; x {scale:.2f}): KCs {a['kcs_answering']}/{c_['kcs_answering']} | block {a['block_ratio']}/{c_['block_ratio']} | "
                  f"APL ratio {row['apl_peak_mch_over_oct']} | both {row['share_answering_both']} | equalization {row['answering_mch_over_oct']} | sustain "
                  f"{json.dumps({od: {k: v['late_over_early'] for k, v in row['by_odor'][od]['classes'].items()} for od in km.ODORS})} | MBON11 "
                  f"{json.dumps({od: row['by_odor'][od]['mbon11_slow_current'] for od in km.ODORS})} ({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
        b.set_type("kenyon_cells", tau_m=0.020)
        b.own_depression = np.zeros(0, np.bool_)
        b.weights, b._external_matrix, b.full_strength = base_w, None, base_full
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
