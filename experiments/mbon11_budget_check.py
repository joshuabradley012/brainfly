"""Exploratory measurement, not a test and not a change to the model: MBON11's Kenyon cell input budget, class by class,
in the corrected model (mb_calibration7.py) against flies' (research_notes/Rung 9 learning data/mbon11_kc_activity.md
section 3.7).

With the Kenyon cells' input at its measured size and APL refitted around it, the classes answer 3-octanol at flies'
densities by Turner et al.'s criterion (gamma_gap_refit.py: alpha/beta 7.2%, alpha'/beta' 17.8%, gamma 2.5%). Yet
MBON11's Kenyon cell input carries 71 pC to 3-octanol, about a quarter of flies' 245-250 (learning_pilot17.py).
mbon11_kc_activity.md's budget for flies at Hige et al.'s stimulus puts MBON11_R's input at about 3,200 synapse-spikes
in 0-1.4 s (1,300-7,500): each class's synapses onto MBON11_R times the share of its cells responding times their spikes.
- gamma-main and gamma-s: 3.5% x 3.5 spikes.
- alpha/beta s, m and c: 6% x 2.5.
- alpha'/beta': 20% x 5.
- gamma-d and alpha/beta-p: inhibited.
At an effective 0.08 pC per synapse-spike that is 250 pC.
Model: the corrected model (odor_probe60.py's cache, mb_calibration7.apply, receptor_fills.RECOMMENDED), the Kenyon
cells' rest set with kc_rest.fit. Measured for 3-octanol and 4-methylcyclohexanol, 2 seeds of 8 flies (the learning
pilots' seeds), with odor_probe10's runner:
- each class's synapses onto MBON11_R (MaleCNS counts);
- the share of its cells responding by Turner et al.'s criterion (0.5 s odor);
- their evoked spikes in Hige et al.'s window (1 s odor, 0-1.4 s, rest subtracted);
- the synapse-spikes onto MBON11_R, from the responders and from every above-rest spike, and what they would carry at
  the model's 0.054 pC per synapse with no depression;
- from the same spikes at 10 ms (odor_apl_conductance_check.trial's protocol, as kc_membrane_check.timed records them),
  the synapse-spikes MBON11_R gets at the strength each Kenyon cell's depression has left (0.5 per spike, recovering
  over 1.5 s) and with none, 0-1.4 s, rest subtracted.

Ran (2026-10-11, 3 minutes): to 3-octanol the corrected model's Kenyon cells give MBON11_R about as many synapse-spikes
as flies' budget, and the synapses' depression halves what they carry.
- Synapse-spikes onto MBON11_R in 0-1.4 s: 4,401 from every above-rest spike, 4,187 from the responders. Flies'
  budget on the same synapse counts is 3,206 (1,300-7,500).
  - gamma-main and gamma-s: 3.5% respond (flies 3.5%) with 1.65 spikes each (flies about 3.5).
  - alpha/beta s, m and c: 9.5% with 2.9 (flies 6% with 2.5).
  - alpha'/beta': 19.6% with 3.25 (flies 20% with 5).
  - gamma-d and alpha/beta-p: none, as in flies.
- At 0.054 pC per synapse with no depression that carries 238 pC (flies 245-250).
- From the same spikes at 10 ms, the depression (0.5 per spike, recovering over 1.5 s) leaves 0.50 of them, about 133 pC
  onto MBON11_R.
- 4-methylcyclohexanol: 456 synapse-spikes, a seventh of flies' budget: 0.4% of the gamma cells respond with 0.8 spikes
  each, 0.8% of alpha/beta and 3.6% of alpha'/beta'. The depression leaves 0.71 of them, 17.5 pC (flies 230-273).
So with the corrected input the model's shortfall to 3-octanol isn't Kenyon cell activity onto MBON11, which meets flies'
estimate. It is the depression rule, read from Yamada et al.'s paired flashes at one spike per flash (mbon11_burst_check.py),
which their data also allow at two spikes per flash with a milder depression (kc_flash_check.py's correction). To
4-methylcyclohexanol the activity itself is a seventh of flies'. The learning pilots report less: learning_pilot17.py's 71
pC is the mean over both MBON11 cells (the left has 31% fewer Kenyon cell synapses, the same classes; about 0.85 of the
right's input), through the slow current within 0-1.4 s, in the learning test's protocol. That is about 1.6 times below this
measure's equivalent, and the two aren't reconciled here.

Checked afterwards (2026-10-11): "it is the depression rule" is too simple, because the rule and the charge per
synapse come from the same flash. kc_flash_check.py's 5% of the gamma cells, one spike each, gives flies' flash EPSC at
0.054 pC per synapse. So the charge per spike scales as 1 / (share flashed x spikes per flash, depression included).
- Read as two or three spikes per flash at the same paired-flash ratio, the depression eases (each spike leaving 0.71 or
  0.79 of the strength), but each spike carries 1/1.71 or 1/2.42 of the charge.
- By the same spikes that is roughly 100 and 80 pC onto MBON11_R (derived, with the depression's share estimated at
  about 0.65 and 0.73), against 133 at one spike per flash. So the one-spike reading already gives the most.
- What would close the gap is fewer cells flashed. Yamada et al.'s 3-7% is borrowed from SPARC2-S labelling in other
  cell types (mbon11_kc_activity.md section 2.2). At 3% the charge per spike would be 0.09 pC, about 220 pC onto MBON11_R;
  at 2.5%, about 265 pC (flies 245-250).

Correction (2026-10-11, after a review): the densities quoted at the top are gamma_gap_refit.py's, measured with APL at
mb_calibration6.py's drive, before apl_refit.py halved it. Flies' values for them are mbon11_kc_activity.md's derived
estimates for Hige et al.'s stimulus (alpha/beta 4-8%, alpha'/beta' 11-30%, gamma 2-6%; together about 7.4%, below
imaging's 12%), not single-cell measurements. On this check's own model (mb_calibration7.py), by the same criterion,
the classes that reach MBON11 respond more: alpha/beta s, m and c 9.5%, above the derived 4-8%, alpha'/beta' 19.6%
and gamma-main and gamma-s 3.5%.

    python experiments/mbon11_budget_check.py      (writes experiments/mbon11_budget_check.json)
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
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 640000, 2
ODORS = ("3-octanol", "4-methylcyclohexanol")
Q_PC = 0.054
CLASSES = {"gamma-main and gamma-s": lambda t: t.startswith("KCg") and t != "KCg-d",
           "alpha/beta s, m, c": lambda t: t in ("KCab-s", "KCab-m", "KCab-c"),
           "alpha'/beta'": lambda t: t.startswith("KCa'b'"),
           "gamma-d": lambda t: t == "KCg-d", "alpha/beta-p": lambda t: t == "KCab-p"}
FLIES = {"gamma-main and gamma-s": (0.035, 3.5), "alpha/beta s, m, c": (0.06, 2.5), "alpha'/beta'": (0.20, 5.0),
         "gamma-d": (0.0, 0.0), "alpha/beta-p": (0.0, 0.0)}     # mbon11_kc_activity.md 3.7: responders, spikes


def delivered(o, rec, odor: str, seed: int, syn: np.ndarray) -> tuple:
    """kc_membrane_check.timed's protocol: MBON11_R's synapse-spikes per 10 ms, at the strength the Kenyon cells'
    depression has left and with none, from 0.5 s before the odor to 1.4 s after its onset."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    p = b.params[b.cls[kc[0]]]
    f, recover = float(p["depression"]), float(p["recovery"]) / b.dt
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t, dep, raw = -1.5, [], []
    for k in range(290):
        left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
        n = b.advance(piece, drive=rec.at(plan, t))[:, kc].astype(np.float64)
        if k >= 100:
            dep.append(float((left * (1.0 - f ** n) / (1.0 - f) * syn).sum(1).mean()))
            raw.append(float((n * syn).sum(1).mean()))
        t += p10.PIECE
    return np.array(dep), np.array(raw), {"depression": f, "recovery_s": float(p["recovery"])}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration7                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    b, m = o.brain, o.m
    out = {"question": __doc__, "mb_calibration": mb_calibration7.apply(o), "flies": FLIES, "odors": {}}
    kc = np.flatnonzero(m["kc"])
    types = o.types[kc]
    mb = np.flatnonzero(o.types == "MBON11")
    right = mb[np.asarray(b.side)[mb] == "R"]
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, right))
    syn = np.bincount(np.searchsorted(kc, pre[onto]), weights=b._counts[onto], minlength=len(kc))
    masks = {name: np.array([f(t) for t in types]) for name, f in CLASSES.items()}
    out["classes"] = {name: {"cells": int(mk.sum()), "synapses_onto_mbon11_r": int(syn[mk].sum())} for name, mk in masks.items()}
    out["synapses_onto_mbon11_r"] = int(syn.sum())
    runner = p10.make_runner(rec)
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = kc_rest.fit(o, rec, p8.class_gaps(o, None), SEED + 900)
        for j, odor in enumerate(ODORS):
            resp, evoked = [], []
            for k in range(SEEDS):
                t = runner(o, odor, SEED + 10 * j + k, 0.5, 1.5)                        # Turner's protocol
                resp.append(p7.turner_responders(t))
                h = runner(o, odor, SEED + 100 + 10 * j + k, 1.0, 0.4)                  # Hige's protocol
                evoked.append((h["window"][:, kc] - 1.4 * h["rest"][:, kc]).mean(0))
            r, e = np.mean(resp, 0), np.mean(evoked, 0)
            responders = r >= 0.5                       # responding on both seeds' tests, or on one of them at the edge
            row = {}
            for name, mk in masks.items():
                sel = mk & responders
                row[name] = {"responding": round(float(r[mk].mean()), 4),
                             "spikes_per_responder": round(float(e[sel].mean()), 2) if sel.any() else None,
                             "synapse_spikes_responders": round(float((np.clip(e, 0, None) * syn)[sel].sum()), 1),
                             "synapse_spikes_all": round(float((np.clip(e, 0, None) * syn)[mk].sum()), 1)}
            tot_r = sum(v["synapse_spikes_responders"] for v in row.values())
            tot_a = float((np.clip(e, 0, None) * syn).sum())
            out["odors"][odor] = {"classes": row, "synapse_spikes_responders": round(tot_r, 1), "synapse_spikes_all": round(tot_a, 1),
                                  "charge_pc_at_q_undepressed": round(tot_a * Q_PC, 1)}
            ts = -0.5 + (np.arange(190) + 0.5) * p10.PIECE
            runs = [delivered(o, rec, odor, SEED + 10 * j + k, syn) for k in range(SEEDS)]
            dep, raw = np.mean([x[0] for x in runs], 0), np.mean([x[1] for x in runs], 0)
            w = (ts > 0) & (ts < 1.4)
            d_ev, r_ev = float((dep[w] - dep[ts < 0].mean()).sum()), float((raw[w] - raw[ts < 0].mean()).sum())
            out["odors"][odor]["timed"] = {"synapse_spikes_depressed": round(d_ev, 1), "synapse_spikes_undepressed": round(r_ev, 1),
                                           "share_left_by_depression": round(d_ev / max(r_ev, 1e-9), 3),
                                           "charge_pc_depressed": round(d_ev * Q_PC, 1), "rule": runs[0][2]}
            print(odor, json.dumps(out["odors"][odor]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
    flies_total = sum(out["classes"][c]["synapses_onto_mbon11_r"] * a * s for c, (a, s) in FLIES.items())
    out["flies_synapse_spikes_from_this_connectome"] = round(flies_total, 0)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print("flies' budget on these synapse counts:", round(flies_total), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
