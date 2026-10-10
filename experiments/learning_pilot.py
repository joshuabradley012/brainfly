"""Exploratory, not pre-registered: dopamine-gated depression at Kenyon cell to MBON11 synapses, in Hige et al. 2015's
protocol, on odor_probe7.py's current model. With the rule's rate fitted to the paired odor's depression, how much does
the unpaired odor's response change?

Hige et al. 2015 (research_notes/Rung 9 learning data/mushroom_body_plasticity.md): a 1 s odor with PPL1-gamma1pedc
driven by four 1 ms light pulses at 2 Hz from 0.2 s after the odor's onset depressed MBON-gamma1pedc's response to that
odor: its odor-evoked spikes (0 to 1.4 s from onset, spontaneous rate subtracted) fell from 118 +- 8.3 to 24 +- 7.4
(80%), its EPSC charge in the same window by 90 +- 3.7%. To the other odor, spikes fell from 110 +- 11 to 83 +- 14
(about 25%). Backward pairing (the odor 0.5 s after the last pulse) changed nothing. The paired odor's depression is
what the rule's rate is fitted to; the unpaired odor's depends on how many Kenyon cells the two odors share through
the real PN-to-KC wiring, so it is a prediction. The backward pairing checks the rule's timing, not the connectome.
Model: odor_probe7.py's current model ("+ undepressed outputs"; Kenyon cells' rest set from seed 11090).
Rule: each Kenyon cell carries an eligibility trace of its spikes that decays with tau_e; at each dopamine pulse every
synapse from it onto MBON11 (MBON-gamma1pedc>a/b, both cells; MBON11's dendrites lie in gamma1 and the peduncle,
which PPL1-gamma1pedc innervates) loses a share of its weight: ln w -> ln w - eta x (the trace at the pulse). The pulses
are the protocol's, at fixed times, not PPL101's simulated spikes. The model's 8 flies share one set of weights, so the
traces are means over flies and seeds: the pilot treats them as one fly.
Trials: 0.5 s to settle, 2.5 s before the odor, the odor for 1 s, 1 s after, Kenyon cells' spikes in 10 ms bins.
MBON11's response is its spikes from 0 to 1.4 s after onset less 1.4 times its rate in the second before, mean over
flies, seeds and both cells; its charge is the sum over its Kenyon cell synapses of each one's weight times its Kenyon
cell's evoked spikes in the same window (mean over flies and seeds), the current a Kenyon cell's spikes deliver here.
Procedure, for 3-octanol paired and 4-methylcyclohexanol unpaired, then the reverse:
  1. pre: both odors (and the four others of odor_probe7.py) at 4 seeds each (32 flies);
  2. pairing: the paired odor with pulses at 0.2, 0.7, 1.2 and 1.7 s (4 seeds), and for the backward check pulses at
     -2.0, -1.5, -1.0 and -0.5 s (4 more);
  3. for tau_e of 0.2, 0.5 and 1 s: eta set so the paired odor's charge falls 90% (computed from the pre trials' Kenyon
     cell spikes; no simulation), the unpaired odor's and the other odors' charge changes read off the same way, and
     the backward pairing's change with the same eta;
  4. post: with tau_e 0.5 s's weights, both odors again at the same 4 seeds: the spike depression.
Seeds: 11000 + 10 x odor + seed (pre and post), 11200 + 10 x pairing + seed (forward), 11300 + ... (backward).

Ran (after the second review: DoOR's spontaneous level subtracted; the first run is in git history): the depression
isn't odor-specific: the two odors' Kenyon cells overlap too much. Before pairing, MBON11 gains 3.6 +- 0.3 spikes to
OCT and 1.8 +- 0.3 to MCH (32 flies; Hige's flies 118 and 110). The rate that cuts OCT's charge by 90% cuts MCH's by
79%, and the other four odors' by 60-80%; paired with MCH instead, MCH's 90% comes with OCT's 51% (the others 30-46%).
In flies the unpaired odor's charge didn't change significantly (Hige et al. Fig. 3, n = 5 cells). tau_e makes no
difference (0.2 to 1 s change these by under a percentage point). In spikes (tau_e 0.5 s), pairing with OCT takes OCT's
response from 3.6 to -1.4 and MCH's from 1.8 to 0.5, drops of 140% and 73% (flies: 80% and about 25%); pairing with
MCH, MCH's goes from 1.8 to 0.3 and OCT's from 3.6 to 1.0 (83% and 73%). Responses below zero mean MBON11 fires less
than at rest during the odor once its Kenyon cell input is gone. Backward pairing changes the paired odor's charge by
1% (OCT) or 7-8% (MCH), where flies' responses don't change; that checks only the rule's timing. 665 of the 4,064 Kenyon
cells gain more than half a spike to OCT and 284 to MCH; 3,623 of them reach MBON11, through 4,184 connections
(41,460 synapses). The responses are small and noisy enough that the spike drops carry about 10-20 percentage points
of uncertainty (SEMs of 0.3 spikes on responses of 2-4).

Checked afterwards (2026-10-10): "didn't change significantly" holds only for Hige et al.'s Fig. 3. Hige et al. 2015
read in full (research_notes/Rung 9 learning data/hige2015_specificity.md): with 3-octanol paired,
4-methylcyclohexanol's charge fell 20% in Fig. 3 (n = 5, not significant, the figure cited above) and 35% in Fig. 4 (n =
6, every cell), and its spikes 27% (Fig. 1F, itself significant) and 38% (Fig. 4E); with 4-methylcyclohexanol paired
(Fig. S3D, n = 6), its spikes fell 76% and 3-octanol's 38%; no charge was measured that way round. On this model the
unpaired odor's charge still fell more than flies' (51-79%) and its spikes too (73%).

    python experiments/learning_pilot.py         (writes experiments/learning_pilot.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
FORWARD, BACKWARD = (0.2, 0.7, 1.2, 1.7), (-2.0, -1.5, -1.0, -0.5)
BIN, SEEDS, TARGET = 0.01, 4, 0.9
TAUS = (0.2, 0.5, 1.0)
PRE = 2.5
PAIRS = (("3-octanol", "4-methylcyclohexanol"), ("4-methylcyclohexanol", "3-octanol"))


def trial(o, odor: str, seed: int, mbon: np.ndarray) -> dict:
    """MBON11's evoked spikes (per fly, mean over its cells), each Kenyon cell's evoked spikes over 0-1.4 s (mean over
    flies), and the Kenyon cells' spikes per 10 ms bin from 2.5 s before the odor to 2 s after onset (mean over flies)."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)))
    drive = odors.orn_drive(b, odor, p3.MAX_HZ)
    piece = int(round(BIN / b.dt))
    n_pre, n_odor = int(round(PRE / BIN)), int(round(1.0 / BIN))
    bins, rest, window = [], 0, 0
    for k in range(n_pre + 2 * n_odor):
        c = b.advance(piece, drive=drive if n_pre <= k < n_pre + n_odor else ())
        bins.append(c[:, kc].mean(0))
        if n_pre - 100 <= k < n_pre:
            rest = rest + c
        elif n_pre <= k < n_pre + 140:
            window = window + c
    evoked = window - 1.4 * rest
    return {"mbon": evoked[:, mbon].mean(1), "kc_evoked": evoked[:, kc].mean(0), "kc_bins": np.array(bins)}


def eligibility(kc_bins: np.ndarray, pulses, tau: float) -> np.ndarray:
    """Each Kenyon cell's trace summed over the pulses (times from the odor's onset): its spikes in the bins ending by
    a pulse, each weighted by exp(-(pulse - bin end) / tau)."""
    ends = (np.arange(len(kc_bins)) + 1) * BIN - PRE
    total = np.zeros(kc_bins.shape[1])
    for p in pulses:
        before = ends <= p + 1e-9
        total += (np.exp(-(p - ends[before]) / tau)[:, None] * kc_bins[before]).sum(0)
    return total


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    calibration = o.set(p7.CURRENT, 11090)
    b, types, m = o.brain, o.types, o.m
    kc = np.flatnonzero(m["kc"])
    mbon = np.flatnonzero(types == "MBON11")
    pre_n = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre_n] & np.isin(b.idx, mbon))          # KC -> MBON11 synapses
    kc_of = np.searchsorted(kc, pre_n[onto])
    w0 = b.weights.copy()
    per_kc = np.bincount(kc_of, weights=w0[onto], minlength=len(kc))      # each KC's total weight onto MBON11
    out = {"question": __doc__, "kc_rest_calibration": calibration, "kc_mbon11_connections": int(len(onto)),
           "kc_mbon11_synapses": int(np.abs(b._counts[onto]).sum()), "kcs_onto_mbon11": int((per_kc > 0).sum()),
           "pre": {}, "pairings": []}

    def tests(odor: str, k: int) -> dict:
        r = [trial(o, odor, 11000 + 10 * k + j, mbon) for j in range(SEEDS)]
        spikes = np.concatenate([x["mbon"] for x in r])
        return {"spikes": float(spikes.mean()), "sem": float(spikes.std(ddof=1) / np.sqrt(len(spikes))),
                "kc_evoked": np.mean([x["kc_evoked"] for x in r], 0)}
    pre = {odor: tests(odor, k) for k, odor in enumerate(p7.ODORS)}
    for odor, r in pre.items():
        out["pre"][odor] = {"mbon11_evoked_spikes": round(r["spikes"], 2), "sem": round(r["sem"], 2),
                            "charge": round(float((per_kc * np.clip(r["kc_evoked"], 0, None)).sum()), 1),
                            "kcs_with_evoked_spikes_over_0.5": int((r["kc_evoked"] > 0.5).sum())}
        print("pre", odor, json.dumps(out["pre"][odor]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))

    def charge(log_scale: np.ndarray, odor: str) -> float:
        return float((per_kc * np.exp(log_scale) * np.clip(pre[odor]["kc_evoked"], 0, None)).sum())

    for i, (paired, unpaired) in enumerate(PAIRS):
        fw = [trial(o, paired, 11200 + 10 * i + j, mbon)["kc_bins"] for j in range(SEEDS)]
        bw = [trial(o, paired, 11300 + 10 * i + j, mbon)["kc_bins"] for j in range(SEEDS)]
        row = {"paired": paired, "unpaired": unpaired, "by_tau": {}}
        for tau in TAUS:
            E = np.mean([eligibility(x, FORWARD, tau) for x in fw], 0)
            Eb = np.mean([eligibility(x, BACKWARD, tau) for x in bw], 0)
            base = charge(np.zeros(len(kc)), paired)
            lo, hi = 0.0, 1.0
            while 1 - charge(-hi * E, paired) / base < TARGET and hi < 1e6:
                lo, hi = hi, hi * 4
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if 1 - charge(-mid * E, paired) / base < TARGET else (lo, mid)
            eta = 0.5 * (lo + hi)
            drop = {od: round(1 - charge(-eta * E, od) / charge(np.zeros(len(kc)), od), 3) for od in p7.ODORS}
            row["by_tau"][str(tau)] = {"eta": round(eta, 4), "reachable": bool(hi < 1e6),
                                       "charge_drop": drop, "backward_charge_drop": round(1 - charge(-eta * Eb, paired) / base, 3),
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
