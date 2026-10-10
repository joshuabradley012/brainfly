"""Exploratory, not pre-registered: learning_pilot2.py again, on the model as it stands after odor_probe33.py to
odor_probe35.py, with MBON11's spikes counted as Hige et al. counted them (the cell held near 6 Hz): how specific is the
depression now, against flies' numbers read in full?

learning_pilot2.py, on odor_probe30.py's antennal lobe with MBON11's Kenyon cell synapses from its own measurements: the
rate that cuts the paired odor's charge by 90% cuts the unpaired odor's by 38% (3-octanol paired) or 11%
(4-methylcyclohexanol paired), and the unpaired odor's spikes fall 30% or 5.5% (flies about 25%). Since then the Kenyon
cell classes' distances below threshold come from Inada et al. 2017's offsets (odor_probe33.py: alpha'/beta' and gamma
cells responding as in flies, MBON11's input a quarter lower), MBON11 keeps its synaptic current through its spikes
(odor_probe35.py: Shiu et al.'s rule threw half its input away), and DEPRESSING says whether the Kenyon cell-to-MBON
synapses depress as Yamada et al. 2024 measured (odor_probe34.py: held out until the Kenyon cells fire as few spikes as
flies'). Flies (research_notes/Rung 9 learning data/hige2015_specificity.md): with 3-octanol paired, its spikes fell 80%
and 4-methylcyclohexanol's 27% (Fig. 1F), 4-methylcyclohexanol's charge 20% (Fig. 3, n = 5) and 35% (Fig. 4, n = 6); with
4-methylcyclohexanol paired, its spikes fell 76% and 3-octanol's 38% (Fig. S3D); backward pairing within 7%.
Model: odor_probe30.py's brain (brain_cache.py) with Inada's offsets and odor_probe31.py's Kenyon cell-to-MBON11
synapses (0.030 pC per synapse), depressing with their Kenyon cells (0.5 of the strength left per spike, recovering over
1.5 s) if DEPRESSING, and MBON11 keeping its current (keep_current) and held near 6 Hz in every test (its bias lowered by
the step at which its resting rate crosses 6 Hz, from 0, -4, -8 and -12 mV, interpolated, as odor_probe35.py holds it).
Protocol, rule, fit and measures as learning_pilot2.py, except that each Kenyon cell's spikes count,
in the charge, with the strength its depression has left (read from the brain at the start of each 10 ms piece), and
in the rule's eligibility trace as spikes (responders, for the overlap, by their spikes as before). Seeds 310000 + 10 x
odor + seed (pre and post), 310200 + 10 x pairing + seed (forward), 310300 + ... (backward); + 900 + round for the Kenyon
cells' rest; + 950 + step for the hold.

    python experiments/learning_pilot3.py        (writes experiments/learning_pilot3.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import learning_pilot as lp
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe7 as p7
import odor_probe8 as p8

OUT = Path(__file__).with_suffix(".json")
SEED = 310000
CHARGE_PC = 0.030
DEPRESSING = False                                 # odor_probe34.py: held out until the Kenyon cells fire as few spikes as flies'
HELD_HZ, HOLD_STEPS_MV = 6.0, (-12.0, -8.0, -4.0, 0.0)


def trial(o, rec, odor: str, seed: int, mbon: np.ndarray, kc: np.ndarray, f: float, recover_s: float) -> dict:
    """learning_pilot2.trial, the Kenyon cells' evoked spikes also counted with their remaining strength."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece = int(round(lp.BIN / b.dt))
    recover = recover_s / b.dt
    n_pre, n_odor = int(round(lp.PRE / lp.BIN)), int(round(1.0 / lp.BIN))
    bins, rest, window, rest_d, window_d = [], 0, 0, 0, 0
    for k in range(n_pre + 2 * n_odor):
        t = (k - n_pre) * lp.BIN
        if DEPRESSING:
            left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
        c = b.advance(piece, drive=rec.at(plan, t))
        n = c[:, kc].astype(np.float64)
        d = left * (1.0 - f ** n) / (1.0 - f) if DEPRESSING else n
        bins.append(c[:, kc].mean(0))
        if n_pre - 100 <= k < n_pre:
            rest, rest_d = rest + c, rest_d + d
        elif n_pre <= k < n_pre + 140:
            window, window_d = window + c, window_d + d
    evoked = window - 1.4 * rest
    return {"mbon": evoked[:, mbon].mean(1), "kc_evoked": evoked[:, kc].mean(0),
            "kc_delivered": (window_d - 1.4 * rest_d).mean(0), "kc_bins": np.array(bins)}


def main() -> None:
    if DEPRESSING is None:
        raise SystemExit("set DEPRESSING from odor_probe34.py's result first")
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, p8.OFFSETS["Inada"]), SEED + 900)
    b.set_type("MBON11", keep_current=1.0)
    kc = np.flatnonzero(m["kc"])
    mbon = np.flatnonzero(types == "MBON11")
    gain = p31.mbon_gain(o, rec, mbon)
    pre_n = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre_n] & np.isin(b.idx, mbon))
    kc_of = np.searchsorted(kc, pre_n[onto])
    w_syn = p31.GAIN_HZ_PER_PA * CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    w0 = b.weights.copy()
    w0[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w0.copy(), None
    full = b.full_strength.copy()
    full[o.kc_mbon] = not DEPRESSING
    b.full_strength = full
    p = b.params[b.cls[kc[0]]]
    f, recover_s = float(p["depression"]), float(p["recovery"])
    per_kc = np.bincount(kc_of, weights=w0[onto], minlength=len(kc))
    bias0 = o.own_bias()
    rates = []
    for k, d in enumerate(HOLD_STEPS_MV):
        bias = bias0.copy()
        bias[mbon] += d
        b.set_bias(bias)
        rates.append(float(p10.resting(o, rec, SEED + 950 + k)["hz"][mbon].mean()))
    k = next((i for i, r in enumerate(rates) if r >= HELD_HZ), 0)
    step = HOLD_STEPS_MV[k] if k == 0 else float(np.interp(HELD_HZ, rates[k - 1:k + 1], HOLD_STEPS_MV[k - 1:k + 1]))
    bias = bias0.copy()
    bias[mbon] += step
    b.set_bias(bias)                                   # held for the rest of the run
    held = {"steps_mv": list(HOLD_STEPS_MV), "rest_hz_by_step": [round(r, 2) for r in rates], "bias_step_mv": round(step, 2),
            "rest_hz": round(float(p10.resting(o, rec, SEED + 949)["hz"][mbon].mean()), 2)}
    print("held", json.dumps(held), flush=True)
    out = {"question": __doc__, "depressing": DEPRESSING, "held": held, "kc_rest_inada": kc_rest, "mbon11_gain": gain,
           "charge_pc_per_synapse": CHARGE_PC, "weight_per_synapse_mv": round(w_syn, 4), "pre": {}, "pairings": []}
    print("MBON11 gain", json.dumps(gain), "depressing", DEPRESSING, flush=True)

    def tests(odor: str, k: int) -> dict:
        r = [trial(o, rec, odor, SEED + 10 * k + j, mbon, kc, f, recover_s) for j in range(lp.SEEDS)]
        spikes = np.concatenate([x["mbon"] for x in r])
        return {"spikes": float(spikes.mean()), "sem": float(spikes.std(ddof=1) / np.sqrt(len(spikes))),
                "kc_evoked": np.mean([x["kc_evoked"] for x in r], 0), "kc_delivered": np.mean([x["kc_delivered"] for x in r], 0)}
    pre = {odor: tests(odor, k) for k, odor in enumerate(p7.ODORS)}
    for odor, r in pre.items():
        out["pre"][odor] = {"mbon11_evoked_spikes": round(r["spikes"], 2), "sem": round(r["sem"], 2),
                            "charge": round(float((per_kc * np.clip(r["kc_delivered"], 0, None)).sum()), 1),
                            "kcs_with_evoked_spikes_over_0.5": int((r["kc_evoked"] > 0.5).sum())}
        print("pre", odor, json.dumps(out["pre"][odor]), flush=True)
    out["overlap"] = {}
    for paired, unpaired in lp.PAIRS:
        a, u = pre[paired]["kc_evoked"] > 0.5, pre[unpaired]["kc_evoked"] > 0.5
        evoked = per_kc * np.clip(pre[unpaired]["kc_delivered"], 0, None)
        out["overlap"][f"{unpaired} in {paired}"] = {
            "share_of_responders": round(float((a & u).sum() / max(u.sum(), 1)), 3),
            "jaccard": round(float((a & u).sum() / max((a | u).sum(), 1)), 3),
            "share_of_charge": round(float(evoked[a].sum() / evoked.sum()), 3)}
    print("overlap", json.dumps(out["overlap"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))

    def charge(log_scale: np.ndarray, odor: str) -> float:
        return float((per_kc * np.exp(log_scale) * np.clip(pre[odor]["kc_delivered"], 0, None)).sum())

    for i, (paired, unpaired) in enumerate(lp.PAIRS):
        fw = [trial(o, rec, paired, SEED + 200 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
        bw = [trial(o, rec, paired, SEED + 300 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
        row = {"paired": paired, "unpaired": unpaired, "by_tau": {}}
        for tau in lp.TAUS:
            E = np.mean([lp.eligibility(x, lp.FORWARD, tau) for x in fw], 0)
            Eb = np.mean([lp.eligibility(x, lp.BACKWARD, tau) for x in bw], 0)
            base = charge(np.zeros(len(kc)), paired)
            lo, hi = 0.0, 1.0
            while 1 - charge(-hi * E, paired) / base < lp.TARGET and hi < 1e6:
                lo, hi = hi, hi * 4
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if 1 - charge(-mid * E, paired) / base < lp.TARGET else (lo, mid)
            eta = 0.5 * (lo + hi)
            drop = {od: round(1 - charge(-eta * E, od) / charge(np.zeros(len(kc)), od), 3) for od in p7.ODORS}
            row["by_tau"][str(tau)] = {"eta": round(eta, 4), "reachable": bool(hi < 1e6), "charge_drop": drop,
                                       "backward_charge_drop": round(1 - charge(-eta * Eb, paired) / base, 3),
                                       "kcs_losing_half": int((np.exp(-eta * E) < 0.5).sum())}
            print(paired, "tau", tau, json.dumps(row["by_tau"][str(tau)]), flush=True)
            if tau == 0.5:
                log_scale = -eta * E
        w = w0.copy()
        w[onto] = w0[onto] * np.exp(log_scale[kc_of])
        b.weights, b._external_matrix = w.astype(np.float32), None
        post = {od: tests(od, p7.ODORS.index(od)) for od in (paired, unpaired)}
        row["spikes"] = {od: {"pre": round(pre[od]["spikes"], 2), "post": round(post[od]["spikes"], 2),
                              "sem": [round(pre[od]["sem"], 2), round(post[od]["sem"], 2)],
                              "drop": round(1 - post[od]["spikes"] / pre[od]["spikes"], 3)} for od in (paired, unpaired)}
        print(paired, "spikes", json.dumps(row["spikes"]), flush=True)
        b.weights, b._external_matrix = w0.copy(), None
        out["pairings"].append(row)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
