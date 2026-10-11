"""Exploratory check, not pre-registered and not a change to the model: Kenyon cells integrating over longer times with
their projection neuron synapses depressing, so that they keep flies' plateau (research_notes/Rung 9 learning
data/kc_integration.md's candidate sets). Do they answer 4-methylcyclohexanol more as flies' do, and hold their firing?

kc_membrane_check.py: with the unitary EPSP held, Kenyon cells integrating over 50 or 100 ms answer 4-methylcyclohexanol
0.37 and 0.49 as often as 3-octanol (0.18 now; flies about as often) and hold their firing, but far too many answer,
because undepressed a longer membrane takes in about twice the sustained drive flies' Kenyon cells keep (Gruntman &
Turner 2013: a plateau of about 4.4 mV per connection at 115 spikes/s, unitary EPSPs of 1.2-1.5 mV). kc_integration.md
fitted sets that meet both: A, 20 ms and no depression (4.5 mV; the model now, its projection neuron-to-Kenyon cell
synapses exempt from their neurons' depression); C, 50 ms with the synapses keeping 0.85 of their strength per spike and
recovering over 0.1 s (3.9 mV; it also gives Gruntman & Turner's brief-input decay of 35-60 ms, which A's 20 ms doesn't);
D, Groschner et al. 2018's 189 ms with 0.5 and 0.15 s (3.2 mV; it gives Groschner's summation of EPSPs 50-100 ms apart,
and not Turner et al.'s 11.5 ms decay). Depressing synapses compress the projection neurons' rate range at the Kenyon
cells: weak input counts for more against strong (at 40 spikes/s about 1.6 mV per connection in A, 2.1 in C, 3.2 in D;
at 115 spikes/s 4.5, 3.4 and 3.7), which is what 4-methylcyclohexanol, two strong glomeruli and many weak, would need.
Model: kc_membrane_check.py's (learning pilot 12's Kenyon cells: odor_probe60.py's cache, mb_calibration4.py's mushroom
body, receptor_fills.RECOMMENDED) in sets A, C and D: the Kenyon cells' membrane time constant; the projection neuron-to-
Kenyon cell synapses depressing on their own (HybridBrain's own_depression, the projection neurons' slow_depression and
slow_recovery; their other synapses as they are), scaled so that one spike's EPSP at the synapses' resting strength (their
projection neurons resting at about 5 spikes/s) peaks as it does now; the cells' rest set again to the same distances
below threshold; APL and everything else as they are.
Measured as kc_membrane_check.py measures (2 seeds of 8 flies, the learning pilots' seeds).
Read as (written before the run): a set is worth recalibrating the mushroom body around if 4-methylcyclohexanol's answering
cells come nearer 3-octanol's than in A while the share of all Kenyon cells answering 3-octanol stays within 6-25%
(flies about 12%; Hige et al. 2015, Honegger et al. 2011) and the cells keep more of their early firing.

Ran (2026-10-11, 7 minutes): set C meets the reading, modestly; set D answers everything. Set A repeats
kc_membrane_check.py's 20 ms condition exactly (624 and 111 Kenyon cells answering 3-octanol and 4-methylcyclohexanol, 0.18
as many; silencing APL raises their spikes 2.73 and 2.16-fold). Set C (the synapses x 2.08, at 0.977 of their strength at
rest): 436 and 121 answer, 0.28 as many, 10.7% of the Kenyon cells for 3-octanol (flies about 12%); silencing APL raises
the spikes 2.77 and 2.72-fold (flies 2-3); from 0.5 to 1 s the alpha/beta, alpha'/beta' and gamma cells fire at 0.29, 0.39
and 0.085 of their early rate to 3-octanol (A 0.20, 0.29 and 0.05); 0.17 of 3-octanol's answering cells answer
4-methylcyclohexanol (A 0.10; flies 0.30), and 0.62 of 4-methylcyclohexanol's answer 3-octanol (A 0.53; flies 0.33).
The ratio rises more because fewer cells answer 3-octanol, and with fewer spikes each (1,162 against 2,766), than because
more answer 4-methylcyclohexanol: the depressing synapses compress 3-octanol's strong drive. Through the slow current
their input to MBON11 would peak at 242 pA for 3-octanol with 0.26 of it held (A 416 and 0.21; flies about 400 and 0.43),
126 pC (A 202; flies 245-275): MBON11 would answer more weakly. Set D (x 7.75): 2,905 and 3,109 answer, 71 and 76% of the
Kenyon cells, equal but nothing like flies' sparseness (APL's silencing still 2.6-2.8-fold); it fails the reading.
So of the sets that keep Gruntman & Turner's plateau, C keeps flies' density and APL's effect and moves
4-methylcyclohexanol and the cells' sustained firing toward flies', a little; whether that moves rung 9's reciprocal is
learning_pilot13.py's question.

Correction (2026-10-11, after an independent review):
- In sets C and D the cells' rest wasn't set back to the same distances below threshold, though the model above says it
  was. odor_probe33.set_rest's first pass measured the cells with the previous condition's time constant's share of the
  bias (20 ms before set C, set C's 50 ms before set D; amended after a second review), and its second pass didn't undo
  the overshoot (kc_rest.py). The JSON records the realized distances. Set A's are within
  0.3 mV of the targets (alpha/beta 21.5, alpha'/beta' 16, gamma 32.5 mV). Set C's cells rest 1.5-4.9 mV nearer
  threshold. Set D's rest 6.3-22.8 mV nearer and fire 0.9-2.2 spikes/s at rest. So set C's numbers above were
  measured with the cells nearer threshold than meant. Set D's answering shares mostly reflect cells resting near
  threshold, so "it fails the reading" doesn't test set D. kc_setc_check2.py runs the sets again with the rest held.
- The per-connection plateaus in the first paragraph disagree. kc_integration.md's table F gives 4.5, 3.9 and 3.2 mV
  at 115 spikes/s (A, C, D) and 1.57, 2.37 and 2.77 at 40. The second set here (1.6, 2.1 and 3.2 at 40; 4.5, 3.4 and
  3.7 at 115) comes from one unitary EPSP of about 1.24 mV held at the resting strength, as this check scales the
  synapses. The note gives each set its own unitary EPSP (C 1.4, D 1.25 mV). The ratio of 40 to 115 spikes/s is the
  same either way (about 0.35, 0.6 and 0.86), so the compression argument stands.
- resting_strength assumes regular firing at 5 spikes/s. For Poisson firing (warm.rest_depression's mean,
  1/(1 + r tau (1 - f))) a resting synapse keeps 0.930 of its strength in C and 0.727 in D, not 0.977 and 0.848. Its
  EPSP is then about 5% (C) and 14% (D) below "as now".
- "1,162 against 2,766" are the Kenyon cells' total spikes per fly (odor_apl_conductance_check.condition's kc_spikes).
  Per answering cell they are 2.7 against 4.4.
- Set D's shares are 71.5 and 76.5% of the Kenyon cells, not 71 and 76%.
- "About twice the sustained drive" (from kc_membrane_check.py) holds at 50 ms. At 100 ms it is nearly four times.
- Flies' 3-octanol charge is about 245-250 pC (Hige et al.'s 248 and 244). 245-275 pools both odors.

    python experiments/kc_setc_check.py      (writes experiments/kc_setc_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import kc_membrane_check as km
import mb_calibration
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = km.SEED, km.SEEDS
PN_REST_HZ = 5.0
SETS = {"A": (0.020, None, None), "C": (0.050, 0.85, 0.10), "D": (0.189, 0.50, 0.15)}   # tau_m, depression, recovery


def resting_strength(f: float | None, recovery: float | None, hz: float = PN_REST_HZ) -> float:
    """A depressing synapse's strength at each spike of regular firing at hz (1 when it doesn't depress)."""
    if f is None:
        return 1.0
    e = np.exp(-1.0 / (hz * recovery))
    return float((1.0 - e) / (1.0 - f * e))


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
            x_rest = resting_strength(f, recovery)
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
            kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            off = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            row = cc.condition(on, off)
            row.update({"tau_m_s": tau_m, "depression": f, "recovery_s": recovery, "resting_strength": round(x_rest, 3),
                        "pn_kc_scale": round(float(scale), 3), "kc_rest": kc_rest, "by_odor": {}})
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
            print(f"set {name} (tau_m {tau_m}, {f}/{recovery}; x {scale:.2f}): KCs {a['kcs_answering']}/{c_['kcs_answering']} | block {a['block_ratio']}/{c_['block_ratio']} | "
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
