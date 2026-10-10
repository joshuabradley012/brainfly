"""Exploratory, not pre-registered: learning_pilot.py again, on odor_probe30.py's antennal lobe and Kenyon cells, with
MBON11's Kenyon cell synapses set from MBON11's own measurements (odor_probe31.py). With the rule's rate fitted to the
paired odor's depression, how much does the unpaired odor's response change?

learning_pilot.py, on odor_probe7.py's model: the depression wasn't odor-specific. The rate that cut 3-octanol's charge
by 90% cut 4-methylcyclohexanol's by 79%, where flies' didn't change significantly (Hige et al. 2015), because the two
odors' Kenyon cells overlapped (Jaccard 0.32 in odor_probe7.py); and MBON11 gained only 1.8-3.6 spikes (flies 110-118),
so the spike drops carried 10-20 percentage points of noise. odor_probe30.py's antennal lobe (the measured receptor
synapse, spontaneous and time-varying receptor firing, presynaptic inhibition fitted to Olsen & Wilson 2008) gives
Kenyon cells as sparse as flies' (2.4-10.5%, mean Jaccard 0.16, these two odors 0.12), though 56% of
4-methylcyclohexanol's responders also answer 3-octanol (flies' dissimilar odors share about 22%); odor_probe31.py
sets the Kenyon cell-to-MBON11 synapses from Yamada et al. 2024's EPSC charge and Wang et al. 2026's gain.
Model: odor_probe31.build() (odor_probe30.py's brain, rebuilt on its seeds; brain_cache.py keeps it) with odor_probe31.py's Kenyon
cell-to-MBON11 weights at q = CHARGE_PC per synapse, the middle of Yamada et al.'s range (chosen before odor_probe31.py
finished), from MBON11's gain measured as odor_probe31.py measures it.
Rule, protocol, fit and measures as learning_pilot.py (four 1 ms dopamine pulses at 2 Hz from 0.2 s into a 1 s odor;
the paired odor's charge set to fall 90%; spikes from 0 to 1.4 s less 1.4 times the second before; post-pairing tests
with tau_e 0.5 s's weights), with the receptor neurons firing spontaneously throughout and following their measured
time course during the odor (odor_probe30.py's drive). Also reported: the share of each odor's responding Kenyon cells
(over half a spike evoked) that also respond to the other, and the share of the unpaired odor's charge that the paired
odor's responders carry. Seeds 240000 for the build (odor_probe30.py's); 250000 + 10 x step for MBON11's gain
(odor_probe31.py's); 260000 + 10 x odor + seed (pre and post), 260200 + 10 x pairing + seed (forward pairing), 260300 +
10 x pairing + seed (backward).

Ran: on odor_probe30.py's sparser antennal lobe the depression is far more odor-specific than in learning_pilot.py, and
the spike drops come out like flies', though the unpaired odor's charge still falls by up to 38% where flies' didn't
change significantly. MBON11 (gain 3.68 spikes/s per mV, so 0.67 mV per synapse) gains 76.8 +- 0.6 spikes to 3-octanol
and 29.0 +- 0.4 to 4-methylcyclohexanol before pairing (32 flies; flies 118 +- 8.3 and 110 +- 11), and 25-71 to the
other four odors; 437 Kenyon cells gain more than half a spike to 3-octanol and 106 to 4-methylcyclohexanol. 55% of
4-methylcyclohexanol's responders also respond to 3-octanol (Jaccard 0.12) and carry 46% of its charge;
4-methylcyclohexanol's responders carry 15% of 3-octanol's. The rate that cuts 3-octanol's charge by 90% cuts
4-methylcyclohexanol's by 38% (learning_pilot.py: 79%) and the other four odors' by 9-67%; paired with
4-methylcyclohexanol instead, 3-octanol's falls 11% (learning_pilot.py: 51%) and the others' 1-50%. tau_e makes no
difference (0.2 to 1 s change these by under a percentage point). In spikes (tau_e 0.5 s), pairing with 3-octanol takes
its response from 76.8 to 14.4 (81%; flies 80%) and 4-methylcyclohexanol's from 29.0 to 20.4 (30%; flies about 25%);
pairing with 4-methylcyclohexanol takes its response from 29.0 to 3.7 (87%) and 3-octanol's from 76.8 to 72.6 (5.5%).
The SEMs are 0.3-0.7 spikes, so these drops are well resolved. Backward pairing leaves the paired odor's charge
unchanged in both directions, as in flies. The asymmetry follows the imbalance between the two odors (odor_probe31.py:
3-octanol drives about four times as many Kenyon cells, and gamma cells at 9.4% against flies' about 2%), which flies'
MBON11 doesn't show (118 and 110 spikes): 4-methylcyclohexanol's few responders lie half inside 3-octanol's many.

Checked afterwards (2026-10-10): flies' unpaired odor does lose input; "didn't change significantly" holds only for Hige
et al.'s Fig. 3. Hige et al. 2015 read in full (research_notes/Rung 9 learning data/hige2015_specificity.md): with
3-octanol paired, 4-methylcyclohexanol's charge fell 20% in Fig. 3 (n = 5, not significant, the figure cited above) and
35% in Fig. 4 (n = 6, every cell), and its spikes 27% (Fig. 1F, itself significant) and 38% (Fig. 4E); with
4-methylcyclohexanol paired (Fig. S3D, n = 6), its spikes fell 76% and 3-octanol's 38%; no charge was measured that way
round. So with 3-octanol paired the model's numbers fall within flies' (charge 38%, spikes 30%), while with
4-methylcyclohexanol paired the model's 3-octanol loses too little (spikes 5.5%, charge 11%; flies' spikes 38%): flies'
depression is about as specific in both directions, the model's isn't, because 3-octanol drives about four times as many
Kenyon cells as 4-methylcyclohexanol.

    python experiments/learning_pilot2.py        (writes experiments/learning_pilot2.json)
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
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe31 as p31
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 260000
CHARGE_PC = 0.030


def prepare() -> None:
    """The module globals odor_probe31.build sets, also needed when the brain comes from the cache."""
    p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
    p21.masks = p29.pn_only_masks


def trial(o, rec, odor: str, seed: int, mbon: np.ndarray) -> dict:
    """learning_pilot.trial with spontaneous receptor firing throughout and the odor following the receptor time course."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece = int(round(lp.BIN / b.dt))
    n_pre, n_odor = int(round(lp.PRE / lp.BIN)), int(round(1.0 / lp.BIN))
    bins, rest, window = [], 0, 0
    for k in range(n_pre + 2 * n_odor):
        t = (k - n_pre) * lp.BIN
        c = b.advance(piece, drive=rec.at(plan, t))
        bins.append(c[:, kc].mean(0))
        if n_pre - 100 <= k < n_pre:
            rest = rest + c
        elif n_pre <= k < n_pre + 140:
            window = window + c
    evoked = window - 1.4 * rest
    return {"mbon": evoked[:, mbon].mean(1), "kc_evoked": evoked[:, kc].mean(0), "kc_bins": np.array(bins)}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe30", p31.build, prepare)
    b, types, m = o.brain, o.types, o.m
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
    per_kc = np.bincount(kc_of, weights=w0[onto], minlength=len(kc))
    out = {"question": __doc__, "build": built, "mbon11_gain": gain, "charge_pc_per_synapse": CHARGE_PC,
           "weight_per_synapse_mv": round(w_syn, 4), "kc_mbon11_connections": int(len(onto)),
           "kcs_onto_mbon11": int((per_kc > 0).sum()), "pre": {}, "pairings": []}
    print("MBON11 gain", json.dumps(gain), "weight per synapse", round(w_syn, 4), flush=True)

    def tests(odor: str, k: int) -> dict:
        r = [trial(o, rec, odor, SEED + 10 * k + j, mbon) for j in range(lp.SEEDS)]
        spikes = np.concatenate([x["mbon"] for x in r])
        return {"spikes": float(spikes.mean()), "sem": float(spikes.std(ddof=1) / np.sqrt(len(spikes))),
                "kc_evoked": np.mean([x["kc_evoked"] for x in r], 0)}
    pre = {odor: tests(odor, k) for k, odor in enumerate(p7.ODORS)}
    for odor, r in pre.items():
        out["pre"][odor] = {"mbon11_evoked_spikes": round(r["spikes"], 2), "sem": round(r["sem"], 2),
                            "charge": round(float((per_kc * np.clip(r["kc_evoked"], 0, None)).sum()), 1),
                            "kcs_with_evoked_spikes_over_0.5": int((r["kc_evoked"] > 0.5).sum())}
        print("pre", odor, json.dumps(out["pre"][odor]), flush=True)
    out["overlap"] = {}
    for paired, unpaired in lp.PAIRS:
        a, u = pre[paired]["kc_evoked"] > 0.5, pre[unpaired]["kc_evoked"] > 0.5
        evoked = per_kc * np.clip(pre[unpaired]["kc_evoked"], 0, None)
        out["overlap"][f"{unpaired} in {paired}"] = {
            "share_of_responders": round(float((a & u).sum() / max(u.sum(), 1)), 3),
            "jaccard": round(float((a & u).sum() / max((a | u).sum(), 1)), 3),
            "share_of_charge": round(float(evoked[a].sum() / evoked.sum()), 3)}
    print("overlap", json.dumps(out["overlap"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))

    def charge(log_scale: np.ndarray, odor: str) -> float:
        return float((per_kc * np.exp(log_scale) * np.clip(pre[odor]["kc_evoked"], 0, None)).sum())

    for i, (paired, unpaired) in enumerate(lp.PAIRS):
        fw = [trial(o, rec, paired, SEED + 200 + 10 * i + j, mbon)["kc_bins"] for j in range(lp.SEEDS)]
        bw = [trial(o, rec, paired, SEED + 300 + 10 * i + j, mbon)["kc_bins"] for j in range(lp.SEEDS)]
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
