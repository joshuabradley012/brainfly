"""Exploratory, not pre-registered: with MBON11 keeping its synaptic current through its spikes, as neurons do, does
it turn its Kenyon cell input into spikes as flies' MBON11 does, and how do its responses compare with Hige et al.'s?

odor_probe32.py found MBON11 making half the spikes from its Kenyon cell input that the same mean drive gives as a
steady bias, and odor_kc_timing.py then found that input neither coincident across Kenyon cells nor bursty within them.
The loss is the model's spike rule, Shiu et al.'s: at each spike the fast synaptic current is set to zero and input
arriving during the 2.2 ms refractory period is dropped, so synaptic drive that holds a neuron at a high rate loses much
of its charge where a bias loses only the refractory time (HybridBrain's keep_current test: 40 mV of synaptic drive gives
95 spikes/s, the same as a bias 167, and 163 when the current is kept). In flies, MBON11's synaptic charge and injected
current are about equally effective: 118 spikes from about 250 pC of odor EPSC (0.47 per pC; Hige et al. 2015) against
0.41 spikes/s per pA of current (Wang et al. 2026).
Model: odor_probe30.py's brain (brain_cache.py) with Inada et al.'s Kenyon cell class offsets (odor_probe33.py), the
Kenyon cell-to-MBON11 synapses at odor_probe31.py's middle charge (q = 0.030 pC per synapse), and MBON11 keeping its
fast current through spikes (HybridBrain keep_current; only its voltage held at reset while refractory). Conditions, as
odor_probe34.py's: Kenyon cell-to-MBON synapses undepressed (the current model), or depressing as Yamada et al. 2024
measured (0.5 of the strength left per spike, recovering over 1.5 s).
Measured for each, as odor_probe34.py measures (six odors, 4 seeds of 8 flies, Hige et al.'s window; MBON11's charge
per cell counting each spike's remaining strength; 50 ms courses for 3-octanol and 4-methylcyclohexanol), and also, for
3-octanol and 4-methylcyclohexanol, MBON11's evoked spikes held at about 6 Hz as Hige et al. held their cells (its bias
lowered by the step at which its rate crosses 6 Hz, from its rate at 0, -4, -8 and -12 mV, interpolated). MBON11's gain
near rest (bias steps, unaffected by keep_current) and its resting rate are reported. Seeds 320000 + 1000 x condition +
10 x odor + seed (+ 400 + ... held; + 900 + round for the Kenyon cells' rest; + 950 + step for the hold).

    python experiments/odor_probe35.py         (writes experiments/odor_probe35.json)
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
SEED = 320000
HELD_HZ = 6.0
HOLD_STEPS_MV = (-12.0, -8.0, -4.0, 0.0)
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


def held(o, rec, depressing: bool, base: int, kc, mb, syn, f: float, recover_s: float) -> dict:
    """MBON11 held near 6 Hz as Hige et al. held their cells: its bias lowered by the interpolated step at which its
    resting rate crosses 6 Hz; then 3-octanol's and 4-methylcyclohexanol's evoked spikes (4 seeds)."""
    b = o.brain
    bias0 = o.own_bias()
    rates = []
    for k, d in enumerate(HOLD_STEPS_MV):
        bias = bias0.copy()
        bias[mb] += d
        b.set_bias(bias)
        rates.append(float(p10.resting(o, rec, base + 950 + k)["hz"][mb].mean()))
    k = next((i for i, r in enumerate(rates) if r >= HELD_HZ), 0)
    step = HOLD_STEPS_MV[k] if k == 0 else float(np.interp(HELD_HZ, rates[k - 1:k + 1], HOLD_STEPS_MV[k - 1:k + 1]))
    bias = bias0.copy()
    bias[mb] += step
    b.set_bias(bias)
    try:
        out = {"steps_mv": list(HOLD_STEPS_MV), "rest_hz_by_step": [round(r, 2) for r in rates], "bias_step_mv": round(step, 2),
               "rest_hz": round(float(p10.resting(o, rec, base + 949)["hz"][mb].mean()), 2)}
        for j, odor in enumerate(COURSE_ODORS):
            runs = [trial(o, rec, odor, base + 400 + 10 * j + s, kc, mb, syn, f, recover_s, depressing) for s in range(SEEDS)]
            out[odor] = round(float(np.mean([(r["window"] - 1.4 * r["rest"])[:, mb].mean() for r in runs])), 1)
    finally:
        b.set_bias(bias0)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, p8.OFFSETS["Inada"]), SEED + 900)
    b.set_type("MBON11", keep_current=1.0)
    kept = [bool(b.params[c]["keep_current"]) for c in b.cls[np.flatnonzero(types == "MBON11")]]
    assert all(kept) and sum(bool(p["keep_current"]) for p in b.params) == len(set(b.cls[np.flatnonzero(types == "MBON11")])), kept
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
           "mbon11_rest_hz": round(float(p10.resting(o, rec, SEED + 990)["hz"][mb].mean()), 2),
           "kc_depression": {"left_per_spike": f, "recovery_s": recover_s, "ppr_400ms": round(1 - (1 - f) * np.exp(-0.4 / recover_s), 3)},
           "kc_mbon_full_strength_before": round(float(full0[o.kc_mbon].mean()), 3), "kc_rest_inada": kc_rest, "conditions": {}}
    print(json.dumps({k: out[k] for k in ("mbon11_gain", "kc_depression", "kc_mbon_full_strength_before")}), flush=True)
    for c, name in enumerate(CONDITIONS):
        full = full0.copy()
        full[o.kc_mbon] = name == "undepressed"
        b.full_strength = full
        print(name, flush=True)
        out["conditions"][name] = condition(o, rec, name == "depressing", SEED + 1000 * c, kc, mb, syn, f, recover_s)
        out["conditions"][name]["held"] = held(o, rec, name == "depressing", SEED + 1000 * c, kc, mb, syn, f, recover_s)
        print(name, "held", json.dumps(out["conditions"][name]["held"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b.full_strength = full0
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
