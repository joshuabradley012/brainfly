"""Exploratory check, not pre-registered and not a change to the model: would Kenyon cells that integrate their input
over longer times answer weak odors more as flies' do, and hold their firing through an odor?

Two of rung 9's gaps sit at the Kenyon cells. 4-methylcyclohexanol reaches 85-87 of them against 3-octanol's 560 or so,
where flies answer the two odors with about as many (learning_pilot11.py, learning_pilot12.py); and the cells' firing
falls to 0.05-0.25 of its early rate by 0.5-1 s although their projection neurons keep about half of theirs, as flies' do
(mbon11_burst_check.py, pn_accommodation_check.py), which holds MBON11's plateau below flies'. The model's Kenyon cells
have Shiu et al.'s 20 ms membrane time constant; Groschner et al. 2018 measured 118 ms (alpha'/beta') and 189 ms
(alpha/beta-c), with spontaneous EPSPs decaying over 263 ms, and found that "even EPSPs spaced 50 or even 100 ms apart
could add up sufficiently to drive spiking", against Turner et al. 2008's 11.5 ms EPSP decay; research_notes/Rung 9
learning data/kc_integration.md recommends 20-50 ms. 4-methylcyclohexanol drives two glomeruli strongly and many weakly:
a Kenyon cell that sums its claws' input over longer times would let weak, sustained input count for more.
Model: learning pilot 12's Kenyon cells (odor_probe60.py's cache, mb_calibration4.py's mushroom body, receptor_fills
.RECOMMENDED), at membrane time constants of 20 (as now), 50 and 100 ms, with the projection neuron-to-Kenyon cell
synapses scaled so that one spike's EPSP peaks as it does now (x 2.03 and 3.69: the measured 1.25-1.4 mV unitary EPSPs
hold; the charge each carries, and so the depolarization a steady input gives, grows with the time constant) and the
cells' rest set again to the same distances below threshold (odor_probe33.set_rest); APL, its synapses and everything
else as they are.
Measured for 3-octanol and 4-methylcyclohexanol, 2 seeds of 8 flies (the learning pilots' seeds), APL working and silenced,
as odor_apl_conductance_check.py measures (odor_apl_conductance_check.condition: the answering cells and those answering
both, the rise silencing APL gives each odor's spikes, APL's peak release and the two odors' ratio); and, APL working,
the Kenyon cells' firing per 10 ms by class (the rate from 0.5 to 1 s over the first 0.3 s's), and the current their
synapses would give MBON11 through the slow current mb_calibration5.py adopted (its peak and its mean from 0.6 to 1 s).
Read as (written before the run): a time constant is worth recalibrating the mushroom body around if, with the distances
to threshold held, 4-methylcyclohexanol's answering cells come nearer 3-octanol's than now (flies about as many), and the
cells keep more of their early firing.

Ran (2026-10-11, 7 minutes): by the reading, worth it, but the check left out what keeps flies' Kenyon cells from firing
so much. Longer integration makes them far more excitable. At 20, 50 and 100 ms (the synapses x 1, 2.03 and 3.69) 624, 1,495
and 2,065 Kenyon cells answer 3-octanol (15, 37 and 51%; flies about 12%) and 111, 545 and 1,020 answer
4-methylcyclohexanol, 0.18, 0.37 and 0.49 as many (flies about as many). They hold their firing: from 0.5 to 1 s the
alpha/beta, alpha'/beta' and gamma cells fire at 0.20, 0.29 and 0.05 of their first 0.3 s's rate to 3-octanol at 20 ms,
0.49, 0.56 and 0.35 at 50 and 0.60, 0.64 and 0.50 at 100. Through mb_calibration5.py's slow current their input to MBON11
would peak at 416, 1,237 and 1,834 pA with 0.21, 0.33 and 0.40 of the peak held from 0.6 to 1 s (flies about 400 pA and
0.43), carrying 202, 749 and 1,190 pC (flies 245-275). Silencing APL raises the spikes 2.7, 2.0 and 1.6-fold (3-octanol;
flies 2-3); APL's 4-methylcyclohexanol/3-octanol peak ratio is 0.28, 0.67 and 0.84 (flies 0.49); the share of
4-methylcyclohexanol's answering cells that answer 3-octanol rises from 0.53 to 0.71 and 0.81 (flies 0.33), and of
3-octanol's that answer 4-methylcyclohexanol from 0.10 to 0.26 and 0.40 (flies 0.30).
What's missing: flies' Kenyon cells keep a plateau of about 4.4 mV per connection at 115 spikes/s with unitary EPSPs of
1.2-1.5 mV (Gruntman & Turner 2013; kc_integration.md), which a 20 ms membrane meets undepressed (4.5) and a longer one
only with the projection neuron-to-Kenyon cell synapses depressing (kc_integration.md's set C: 50 ms, 0.85 of the
strength left per spike, recovering over 0.1 s, 3.9 mV); here at 50 ms undepressed it is about 9. So these cells take in
twice flies' sustained drive, and the densities above overstate what a longer time constant does. The test that keeps
flies' plateau is set C, which needs those synapses to depress on their own (the model's projection neurons depress all
their outputs alike, 0.85 and 0.8 s, and exempt their Kenyon cell synapses).

Correction (2026-10-11, after an independent review):
- At 50 and 100 ms the cells' rest wasn't set back to the same distances below threshold, though the reading needs it
  and the model above says it was. odor_probe33.set_rest's first pass measured the cells with the previous
  condition's time constant's share of the bias (20 ms before 50, 50 ms before 100; amended after a second review), and
  its second pass didn't undo the overshoot (kc_rest.py). The JSON records the
  realized distances. At 20 ms they are within 0.3 mV of the targets (alpha/beta 21.5, alpha'/beta' 16, gamma 32.5
  mV). At 50 ms the cells rest 1.5-5.1 mV nearer threshold, and at 100 ms 1.0-4.3 mV nearer, where the alpha'/beta'
  cells fire 0.25 spikes/s at rest. Part of the densities and of 4-methylcyclohexanol's rise to 0.37 and 0.49 may
  therefore come from the rest, not the integration. kc_setc_check2.py runs these conditions again with the rest held.
- "Twice flies' sustained drive" holds at 50 ms (about 9.2 mV per connection at 115 spikes/s, 2.1 times flies' 4.4).
  At 100 ms it is about 16.7 mV, 3.8 times.
- Flies' 3-octanol charge is about 245-250 pC (Hige et al.'s 248 and 244). 245-275 pools both odors.

Correction (2026-10-11, kc_input_audit.py): the EPSP held across the time constants is the model's own, 1.90 mV per
connection at every spike, not "the measured 1.25-1.4 mV unitary EPSPs" (mb_calibration.py scaled the synapses to 1.4
mV at the PNs' resting depression although they don't depress). So the steady drive per connection at 115 spikes/s
is about 7.0 mV at 20 ms, 14 at 50 ms and 26 at 100 ms (flies about 4.4), not "about 9" at 50 ms. Even at 20 ms the
cells take in 1.6 times flies' sustained drive.

    python experiments/kc_membrane_check.py      (writes experiments/kc_membrane_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import mb_calibration
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 640000, 2
TAU_M = (0.020, 0.050, 0.100)
TAU_S, Q_PC = 0.005, 0.030 * 34.5 / 19.0                # the fast current; the Kenyon cell-to-MBON11 charge per synapse
SLOW = (0.040, 0.280)                                   # mb_calibration5.py's current
ODORS = ("3-octanol", "4-methylcyclohexanol")


def peak_per_w(tau_m: float) -> float:
    """One spike's EPSP peak per unit weight, the current decaying with TAU_S and the membrane with tau_m."""
    t = np.log(tau_m / TAU_S) * tau_m * TAU_S / (tau_m - TAU_S)
    return TAU_S / (tau_m - TAU_S) * (np.exp(-t / tau_m) - np.exp(-t / TAU_S))


def timed(o, rec, odor: str, seed: int, cls: dict, syn: np.ndarray) -> dict:
    """odor_apl_conductance_check.trial's protocol (APL working), recording per 10 ms the Kenyon cells' spikes by class and
    the synapse-spikes they deliver to MBON11 (at the strength their depression has left)."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    p = b.params[b.cls[kc[0]]]
    f, recover = float(p["depression"]), float(p["recovery"]) / b.dt
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t, rates, drive = -1.5, {c: [] for c in cls}, []
    for k in range(290):
        left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
        n = b.advance(piece, drive=rec.at(plan, t))[:, kc].astype(np.float64)
        if k >= 100:                                    # from 0.5 s before the odor to 1.4 s after its onset
            for c, mask in cls.items():
                rates[c].append(float(n[:, mask].mean()) / p10.PIECE)
            drive.append(float((left * (1.0 - f ** n) / (1.0 - f) * syn).sum(1).mean()))
        t += p10.PIECE
    return {"rates": {c: np.array(v) for c, v in rates.items()}, "drive": np.array(drive)}


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
    pn_kc = np.flatnonzero(m["upn"][pre] & m["kc"][b.idx])
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mbon))
    syn = np.bincount(np.searchsorted(kc, pre[onto]), weights=b._counts[onto], minlength=len(kc))
    base_w = b.weights.copy()
    held = [base_w]
    tt = (np.arange(300) + 0.5) * p10.PIECE
    kern = np.exp(-tt / SLOW[1]) - np.exp(-tt / SLOW[0])
    kern /= kern.sum() * p10.PIECE
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        for tau_m in TAU_M:
            scale = peak_per_w(0.020) / peak_per_w(tau_m)
            w = base_w.copy()
            w[pn_kc] *= np.float32(scale)
            b.weights, b._external_matrix = w, None
            held.append(w)
            b.set_type("kenyon_cells", tau_m=tau_m)
            kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, od in enumerate(ODORS)}
            off = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, od in enumerate(ODORS)}
            row = cc.condition(on, off)
            row.update({"pn_kc_scale": round(float(scale), 3), "kc_rest": kc_rest, "by_odor": {}})
            ts = -0.5 + (np.arange(190) + 0.5) * p10.PIECE
            for j, od in enumerate(ODORS):
                rs = [timed(o, rec, od, SEED + 10 * j + k, cls, syn) for k in range(SEEDS)]
                byc = {}
                for c in cls:
                    r = np.mean([x["rates"][c] for x in rs], 0)
                    early, late = r[(ts > 0) & (ts < 0.3)].mean(), r[(ts > 0.5) & (ts < 1.0)].mean()
                    byc[c] = {"hz_per_cell_0_to_0.3s": round(float(early), 3), "hz_per_cell_0.5_to_1s": round(float(late), 3),
                              "late_over_early": round(float(late / max(early, 1e-9)), 3)}
                d = np.mean([x["drive"] for x in rs], 0) / p10.PIECE
                d -= d[ts < 0].mean()
                cur = np.convolve(d, kern)[:len(ts)] * p10.PIECE * Q_PC / len(mbon)
                late = float(cur[(ts > 0.6) & (ts < 1.0)].mean())
                row["by_odor"][od] = {"classes": byc, "mbon11_slow_current": {"peak_pa": round(float(cur.max()), 1), "pa_0.6_to_1s": round(late, 1),
                                      "late_over_peak": round(late / max(float(cur.max()), 1e-9), 3), "charge_pc_0_to_1.4s": round(float(cur[(ts > 0) & (ts < 1.4)].sum() * p10.PIECE), 1)}}
            out["conditions"][str(tau_m)] = row
            a, c_ = row["3-octanol"], row["4-methylcyclohexanol"]
            print(f"tau_m {tau_m}: KCs {a['kcs_answering']}/{c_['kcs_answering']} | block {a['block_ratio']}/{c_['block_ratio']} | APL ratio {row['apl_peak_mch_over_oct']} | "
                  f"both {row['share_answering_both']} | equalization {row['answering_mch_over_oct']} | sustain "
                  f"{json.dumps({od: {k: v['late_over_early'] for k, v in row['by_odor'][od]['classes'].items()} for od in ODORS})} | MBON11 "
                  f"{json.dumps({od: row['by_odor'][od]['mbon11_slow_current'] for od in ODORS})} ({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
        b.set_type("kenyon_cells", tau_m=0.020)
        b.weights, b._external_matrix = base_w, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
