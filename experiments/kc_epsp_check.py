"""Exploratory check, written before it runs: the Kenyon cells with their projection neuron input at its measured size.

kc_input_audit.py: as the rung 9 experiments run the model, one projection neuron spike gives a Kenyon cell a 1.90 mV
EPSP at every spike, where Turner et al. 2008 measured 1.4 mV and Gruntman & Turner 2013 1.24-1.48. mb_calibration.py
scaled the synapses to 1.4 mV "at the PNs' resting depression", but the synapses are exempt from depression, so they
carry 1/0.735 of it. The steady drive per connection is about 7 mV at 115 spikes/s, against flies' 4.4. The model's
density, APL fit and learning results all came with that input.
Model: kc_setc_check2.py's set A (learning pilot 12's Kenyon cells: odor_probe60.py's cache, mb_calibration4.py's
mushroom body, receptor_fills.RECOMMENDED, a 20 ms membrane), in three conditions: the projection neuron-to-Kenyon cell
synapses as now (1.90 mV), and scaled so that one spike's EPSP at full strength is Turner's 1.4 mV (x 0.735), or 1.24
mV (Gruntman & Turner's lower end, x 0.65; sensitivity only). In each, the cells' rest is set with kc_rest.fit and
recorded.
Measured as kc_setc_check2.py measures (2 seeds of 8 flies, the learning pilots' seeds): the cells answering each odor,
the share answering both, the rise silencing APL gives each odor's spikes, APL's peak ratio, the classes' early and late
firing, and the current their synapses would give MBON11 through mb_calibration5.py's slow current.
Read as (written before the run):
- If, at 1.4 mV, the share of all Kenyon cells answering 3-octanol stays within 6-25% (flies about 12%) and silencing
  APL raises both odors' spikes 2-3-fold (flies 2-3), mb_calibration6.py adopts the corrected input (1.4 mV at full
  strength, everything else as now), and learning_pilot16.py runs rung 9's test on it.
- If not, APL's fitted drive is fitted again around the corrected input before anything is adopted (a separate,
  pre-registered step).
The 1.24 mV condition only shows how sensitive the cells are; it decides nothing.

    python experiments/kc_epsp_check.py      (writes experiments/kc_epsp_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import kc_input_audit as audit
import kc_membrane_check as km
import kc_rest
import mb_calibration
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = km.SEED, km.SEEDS
TARGETS = {"as now": None, "1.4 mV": 1.4, "1.24 mV": 1.24}       # one spike's EPSP at full strength, mV


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
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mbon))
    syn = np.bincount(np.searchsorted(kc, pre[onto]), weights=b._counts[onto], minlength=len(kc))
    base_w = b.weights.copy()
    held = [base_w]
    epsp_now = {}
    for name, sel in mb_calibration.classes(o).items():
        e = np.flatnonzero(m["upn"][pre] & sel[b.idx])
        if len(e):
            c = int(b.cls[np.flatnonzero(sel)[0]])
            epsp_now[name] = (e, float(audit.response(b, c, float(base_w[e].mean())).max()))
    out["epsp_now_mv"] = {name: round(v, 3) for name, (_, v) in epsp_now.items()}
    ts = -0.5 + (np.arange(190) + 0.5) * p10.PIECE
    tt = (np.arange(300) + 0.5) * p10.PIECE
    kern = np.exp(-tt / km.SLOW[1]) - np.exp(-tt / km.SLOW[0])
    kern /= kern.sum() * p10.PIECE
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        for name, target in TARGETS.items():
            w = base_w.copy()
            scales = {}
            for cl, (e, now) in epsp_now.items():
                scales[cl] = 1.0 if target is None else target / now
                w[e] *= np.float32(scales[cl])
            b.weights, b._external_matrix = w, None
            held.append(w)
            kc_rest_ = kc_rest.fit(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            off = {od: [cc.trial(o, rec, od, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, od in enumerate(km.ODORS)}
            row = cc.condition(on, off)
            row.update({"epsp_target_mv": target, "pn_kc_scale": {k: round(v, 4) for k, v in scales.items()}, "kc_rest": kc_rest_,
                        "by_odor": {}})
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
            print(f"{name}: KCs {a['kcs_answering']}/{c_['kcs_answering']} ({row['share_answering_3_octanol']}) | block {a['block_ratio']}/{c_['block_ratio']} | "
                  f"APL ratio {row['apl_peak_mch_over_oct']} | both {row['share_answering_both']} | equalization {row['answering_mch_over_oct']} | sustain "
                  f"{json.dumps({od: {k: v['late_over_early'] for k, v in row['by_odor'][od]['classes'].items()} for od in km.ODORS})} | MBON11 "
                  f"{json.dumps({od: row['by_odor'][od]['mbon11_slow_current'] for od in km.ODORS})} ({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
        b.weights, b._external_matrix = base_w, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
