"""Exploratory, not pre-registered: with the Kenyon cell-to-MBON synapses depressing as Yamada et al. 2024 measured, does
MBON11's odor response take flies' shape?

odor_probe7.py made every Kenyon cell-to-MBON synapse undepressed: "The two undepressed choices have no fly measurement
behind them and were made after seeing the depressed versions fall silent". There is one: at gamma Kenyon cell-to-MBON11
synapses a second light flash 400 ms after the first evokes 0.38-0.68 of the first EPSC, less with more calcium, so the
depression is presynaptic and release likely (Yamada et al. 2024; high release probability at these synapses, Woitkuhn
et al. 2020 via Piao & Sigrist 2021), and rung 4's Kenyon cell depression was set from it (each spike leaves 0.5 of the
strength, recovering over 1.5 s: 0.62 at 400 ms; research_notes/Rung 4 resting state data/short_term_plasticity.md). In
flies' odor responses MBON11's EPSC falls from about 400 pA at its peak to about 170 pA within 0.5 s (Hige et al. 2015,
Fig. 3C), depression and Kenyon cell adaptation together. odor_probe31.py: with undepressed synapses set from Yamada et
al.'s charge and Wang et al. 2026's gain, MBON11 gains 74 spikes to 3-octanol and 28 to 4-methylcyclohexanol at the
middle charge (flies 118 and 110), its input per cell 573 and 137 pC (flies about 250-265), 0.13-0.22 spikes per pC
(flies about 0.45).
Model: odor_probe30.py's brain (odor_probe31.build on its seeds; brain_cache.py keeps it) with the Kenyon cell classes'
distances below threshold from Inada et al. 2017's offsets (odor_probe33.py, which moved the classes toward flies':
alpha'/beta' 5.5 mV nearer threshold than alpha/beta, gamma 2.5 mV farther, the mean at 21.5 mV), and the Kenyon
cell-to-MBON11 synapses at odor_probe31.py's middle charge (q = 0.030 pC per synapse, for a rested synapse). Conditions:
  undepressed   every Kenyon cell-to-MBON synapse at full strength (the current model)
  depressing    every Kenyon cell-to-MBON synapse depressing with its Kenyon cell, as rung 4 set it (0.5, 1.5 s)
Measured for each, over the six odors (4 seeds of 8 flies; Hige et al.'s window, 0-1.4 s from onset, less 1.4 times the
second before): MBON11's and MBON-alpha2sc's evoked spikes, and the charge MBON11's Kenyon cell input delivers per cell
(each Kenyon cell spike x its synapses onto that cell x q x the strength its depression has left, read from the brain at
the start of each 10 ms piece), above its rest; and, in 50 ms bins over 2 s, MBON11's rate and its Kenyon cell input as
a current (pA), for 3-octanol and 4-methylcyclohexanol, against Hige et al.'s PSTH (from about 6 Hz, rising 0.15 s
after the valve opens to 135-140 Hz at about 0.3 s and 95-100 Hz at 0.6-1.05 s) and EPSC (about 380-430 pA at its peak,
about 170 pA from 0.6 to 1.0 s). Seeds 290000 + 1000 x condition + 10 x odor + seed (+ 900 + round for the Kenyon cells'
rest).

Ran: the measured depression gives MBON11's input flies' early peak but not their sustained plateau, so with the model's
Kenyon cell firing it leaves MBON11 far short of flies'; the depression is held out of the model carried forward until
the Kenyon cells fire as sparsely in time as flies' (MBON11's gain here 3.70 spikes/s per mV; the Kenyon cell depression
leaves 0.617 at 400 ms). Undepressed, MBON11 gains 64.5 spikes to 3-octanol from 442 pC per cell and 22.1 to
4-methylcyclohexanol from 101 pC (20-67 to the other odors; 0.15-0.24 spikes per pC); its input to 3-octanol peaks at
701 pA at 0.3-0.35 s and is still 254 pA at 0.95 s, and MBON11 peaks at 122 spikes/s and holds 83 at 0.95 s. Depressing,
that input peaks earlier and lower, 302 pA at 0.2-0.25 s, and falls to 89 pA by 0.5 s and 21 pA by 0.95 s (flies' EPSC:
about 400 pA at its peak soon after onset, about 200 pA at 0.35 s and 170 pA from 0.6 to 1.0 s); MBON11 peaks at 91
spikes/s at 0.2-0.25 s and is back near its 34 Hz rest by 1 s (40 spikes/s) where flies' holds 95-100. It gains 25.6
spikes to 3-octanol from 114 pC and 7.5 to 4-methylcyclohexanol from 25 pC (6.7-24 to the others; MBON-alpha2sc
0.1-1.9), now 0.22-0.31 spikes per pC: the depressed spikes were partly the wasted ones. Flies' synapses depress too,
yet their EPSC stays at about 40% of its peak through the odor and their MBON11 keeps firing; with each spike leaving
0.5 of the strength and 1.5 s to recover, that needs Kenyon cells whose spikes come singly and spread out over the odor,
so that most find their synapses largely recovered, where the model's responding Kenyon cells fire 4-6 spikes, mostly
early (odor_probe33.py; flies' alpha/beta 2.2).

    python experiments/odor_probe34.py         (writes experiments/odor_probe34.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe7 as p7
import odor_probe8 as p8

OUT = Path(__file__).with_suffix(".json")
SEED = 290000
CHARGE_PC = 0.030
SEEDS = 4
BIN = 0.05
COURSE_ODORS = ("3-octanol", "4-methylcyclohexanol")
CONDITIONS = ("undepressed", "depressing")


def trial(o, rec, odor: str, seed: int, kc, mb, syn, f: float, recover_s: float, depressing: bool) -> dict:
    """1 s to settle, 1 s of rest, then 2 s from the odor's onset (1 s of odor), in 10 ms pieces. Spike counts over the
    rest and over 0-1.4 s; per 50 ms bin of the 2 s, MBON11's spikes (flies, cells) and its Kenyon cells' delivered
    charge per cell (flies, cells), and the same per second at rest."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    piece, per = int(round(p10.PIECE / b.dt)), int(round(BIN / p10.PIECE))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    recover = recover_s / b.dt                                     # in steps, as the brain keeps b.t and b.last

    def piece_run(t: float):
        if depressing:
            left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
        c = b.advance(piece, drive=rec.at(plan, t))
        n = c[:, kc].astype(np.float64)
        delivered = left * (1.0 - f ** n) / (1.0 - f) if depressing else n
        return c, (delivered @ syn) * CHARGE_PC                      # (flies, n), (flies, cells) in pC

    rest, rest_q, t = 0, 0, -1.0
    for _ in range(100):
        c, q = piece_run(t)
        rest, rest_q, t = rest + c, rest_q + q, t + p10.PIECE
    window, bins_mb, bins_q, cur_mb, cur_q, t = 0, [], [], 0, 0, 0.0
    for k in range(200):
        c, q = piece_run(t)
        t += p10.PIECE
        if k < 140:
            window = window + c
        cur_mb, cur_q = cur_mb + c[:, mb], cur_q + q
        if (k + 1) % per == 0:
            bins_mb.append(cur_mb)
            bins_q.append(cur_q)
            cur_mb, cur_q = 0, 0
    return {"rest": rest, "rest_q": rest_q, "window": window, "bins_mb": np.array(bins_mb), "bins_q": np.array(bins_q)}


def condition(o, rec, depressing: bool, base: int, kc, mb, syn, f: float, recover_s: float) -> dict:
    types = o.types
    a2sc = np.flatnonzero(types == "MBON18")
    n_window = int(round(1.4 / BIN))
    out = {"odors": {}, "course": {}}
    for j, odor in enumerate(p7.ODORS):
        runs = [trial(o, rec, odor, base + 10 * j + s, kc, mb, syn, f, recover_s, depressing) for s in range(SEEDS)]
        evoked = np.concatenate([r["window"] - 1.4 * r["rest"] for r in runs])          # (flies x seeds, n)
        charge = np.concatenate([r["bins_q"][:n_window].sum(0) - 1.4 * r["rest_q"] for r in runs])
        row = {"MBON11": round(float(evoked[:, mb].mean()), 1), "MBON18": round(float(evoked[:, a2sc].mean()), 1),
               "kc_charge_pc_per_cell": round(float(charge.mean()), 1)}
        row["spikes_per_pc"] = round(row["MBON11"] / row["kc_charge_pc_per_cell"], 3) if row["kc_charge_pc_per_cell"] > 0 else None
        out["odors"][odor] = row
        print("  ", odor, json.dumps(row), flush=True)
        if odor in COURSE_ODORS:
            rate = np.mean([r["bins_mb"].mean((1, 2)) / BIN for r in runs], 0)
            current = np.mean([r["bins_q"].mean((1, 2)) / BIN for r in runs], 0)
            out["course"][odor] = {"bin_s": BIN, "start_s": 0.0,
                                   "rest_hz": round(float(np.mean([r["rest"][:, mb].mean() for r in runs])), 2),
                                   "rest_pa": round(float(np.mean([r["rest_q"].mean() for r in runs])), 1),
                                   "mbon11_hz": [round(float(x), 1) for x in rate],
                                   "kc_current_pa": [round(float(x), 1) for x in current]}
            print("   rate", out["course"][odor]["mbon11_hz"][:16], flush=True)
            print("   current", out["course"][odor]["kc_current_pa"][:16], flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, p8.OFFSETS["Inada"]), SEED + 900)
    kc, mb = np.flatnonzero(m["kc"]), np.flatnonzero(types == "MBON11")
    gain = p31.mbon_gain(o, rec, mb)
    w_syn = p31.GAIN_HZ_PER_PA * CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mb))
    w = b.weights.copy()
    w[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w, None
    syn = np.zeros((len(kc), len(mb)))                               # each Kenyon cell's synapses onto each MBON11
    np.add.at(syn, (np.searchsorted(kc, pre[onto]), np.searchsorted(mb, b.idx[onto])), b._counts[onto])
    p = b.params[b.cls[kc[0]]]
    f, recover_s = float(p["depression"]), float(p["recovery"])
    full0 = b.full_strength.copy()
    out = {"question": __doc__, "mbon11_gain": gain, "weight_per_synapse_mv": round(w_syn, 4),
           "kc_depression": {"left_per_spike": f, "recovery_s": recover_s, "ppr_400ms": round(1 - (1 - f) * np.exp(-0.4 / recover_s), 3)},
           "kc_mbon_full_strength_before": round(float(full0[o.kc_mbon].mean()), 3), "kc_rest_inada": kc_rest, "conditions": {}}
    print(json.dumps({k: out[k] for k in ("mbon11_gain", "kc_depression", "kc_mbon_full_strength_before")}), flush=True)
    for c, name in enumerate(CONDITIONS):
        full = full0.copy()
        full[o.kc_mbon] = name == "undepressed"
        b.full_strength = full
        print(name, flush=True)
        out["conditions"][name] = condition(o, rec, name == "depressing", SEED + 1000 * c, kc, mb, syn, f, recover_s)
        OUT.write_text(json.dumps(out, indent=1))
    b.full_strength = full0
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
