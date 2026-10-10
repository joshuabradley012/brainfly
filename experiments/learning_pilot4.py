"""Exploratory, not pre-registered: learning_pilot3.py again, on the model as it stands after odor_probe36.py to
odor_probe48.py: how specific is the depression now, with and without the Kenyon cell-to-MBON synapses' measured
depression?

learning_pilot3.py, on odor_probe30.py's model: with 3-octanol paired the model matched flies on every measure (its
spikes 85% down, flies 80%; 4-methylcyclohexanol's 29.5%, flies 27%), but with 4-methylcyclohexanol paired 3-octanol's
spikes fell only 5.6% (flies 38%), because 4-methylcyclohexanol reached too few Kenyon cells; the Kenyon cell-to-MBON
synapses' measured depression was held out until the Kenyon cells fired as few spikes as flies' (odor_probe34.py). Since
then the antennal lobe has been rebuilt (odor_probe44.py: its local neurons calibrated to flies' odor response, the
receptor synapse's slow component at its unitary size, the PNs keeping their current, the inhibition fitted after the
polishes, MaleCNS's ALLNs, settled starts) and the mushroom body calibrated (mb_calibration.py: each class's PN synapses at
Turner et al.'s 1.4 mV, APL from its measured release onset, saturation and block effect, the classes' thresholds from
Inada et al. and Chen et al.). The Kenyon cells now respond at 2.5-13.1% of cells, firing 1.7-3.3 spikes per response
(alpha/beta; flies 2.2), so the depression is no longer held out; both are run.
Model: odor_probe44.py's (its cache) with mb_calibration.py's calibration, settled starts (warm.tracking), MBON11 keeping
its current and held near 6 Hz, its Kenyon cell synapses at 0.030 pC each (learning_pilot3.py), undepressed or depressing
with their Kenyon cells as rung 4 has them (0.5 of the strength left per spike, recovering over 1.5 s; Yamada et al.'s
paired-pulse ratio).
Protocol, rule, fit and measures as learning_pilot3.py. Seeds 520000 (learning_pilot3.py's offsets), the same for both
variants.

Ran: with the synapses undepressed, the depression is now about as specific as flies' both ways; with them depressing,
the reciprocal pairing falls short again; and MBON11 now answers both odors far more weakly than flies'. Held near 6 Hz
(6.3 and 6.5 Hz; its bias 7.7 mV lower), MBON11 gains 25.8 spikes to 3-octanol and 8.5 to 4-methylcyclohexanol
undepressed, 14.2 and 5.4 depressing (flies 118 and 110; learning_pilot3.py's model 132 and 41); 380 and 91 Kenyon cells
gain more than half a spike, half of 4-methylcyclohexanol's also answering 3-octanol (Jaccard 0.11). Undepressed: pairing
3-octanol cuts its spikes 89% (flies 80%) and 4-methylcyclohexanol's 36% (flies 27%), 4-methylcyclohexanol's charge 40%
(flies 20% and 35%); pairing 4-methylcyclohexanol cuts its spikes 96% (flies 76%) and 3-octanol's 17% (flies 38%; 5.6% in
learning_pilot3.py), 3-octanol's charge 17%; backward pairing 0-2% (flies within 7%). Every one falls inside the bands
hige2015_specificity.md suggests for a pre-registered test (unpaired spikes and charge 10-45%, paired at least 65% and 30
points beyond the unpaired, reciprocal 15-50%, backward within 15%), the reciprocal only just. Depressing: 3-octanol
paired cuts its spikes 89% and 4-methylcyclohexanol's 46% (charge 45%), just beyond the band's 45%; 4-methylcyclohexanol
paired cuts its own to nothing and 3-octanol's 10% (charge 14%), below the band. tau_e changes nothing (0.2-1 s). The
reciprocal reaches the band though 4-methylcyclohexanol's responders carry about as much of 3-octanol's input as before
(15% of its charge, against 13% in learning_pilot3.py): 3-octanol's charge falls 17% (9% before), and MBON11, answering
in a lower range, now loses spikes in proportion (in learning_pilot3.py 9% of the charge took 5.6% of 132 spikes).
4-methylcyclohexanol itself still reaches a quarter as many Kenyon cells as 3-octanol (flies 0.73-0.92). MBON11's weakness comes partly from its Kenyon cell synapses' charge: 0.030 pC was derived from Yamada et
al.'s population EPSCs without their slow tail, which raises the charge per flash from about 19 pC to 26-43
(research_notes/Rung 9 learning data/mbon11_kc_activity.md).

    python experiments/learning_pilot4.py        (writes experiments/learning_pilot4.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import learning_pilot as lp
import learning_pilot3 as lp3
import mb_calibration
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe7 as p7
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 520000
VARIANTS = (False, True)                           # the Kenyon cell-to-MBON synapses undepressed, depressing


def variant(o, rec, depressing: bool, out: dict) -> dict:
    """learning_pilot3.main's measures after the model's setup, with or without the Kenyon cell-to-MBON depression."""
    b, types, m = o.brain, o.types, o.m
    lp3.DEPRESSING = depressing
    kc = np.flatnonzero(m["kc"])
    mbon = np.flatnonzero(types == "MBON11")
    gain = p31.mbon_gain(o, rec, mbon)
    pre_n = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre_n] & np.isin(b.idx, mbon))
    kc_of = np.searchsorted(kc, pre_n[onto])
    w_syn = p31.GAIN_HZ_PER_PA * lp3.CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    w0 = b.weights.copy()
    w0[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w0.copy(), None
    full = b.full_strength.copy()
    full[o.kc_mbon] = not depressing
    b.full_strength = full
    p = b.params[b.cls[kc[0]]]
    f, recover_s = float(p["depression"]), float(p["recovery"])
    per_kc = np.bincount(kc_of, weights=w0[onto], minlength=len(kc))
    bias0 = o.own_bias()
    rates = []
    for k, d in enumerate(lp3.HOLD_STEPS_MV):
        bias = bias0.copy()
        bias[mbon] += d
        b.set_bias(bias)
        rates.append(float(p10.resting(o, rec, SEED + 950 + k)["hz"][mbon].mean()))
    k = next((i for i, r in enumerate(rates) if r >= lp3.HELD_HZ), 0)
    step = lp3.HOLD_STEPS_MV[k] if k == 0 else float(np.interp(lp3.HELD_HZ, rates[k - 1:k + 1], lp3.HOLD_STEPS_MV[k - 1:k + 1]))
    bias = bias0.copy()
    bias[mbon] += step
    b.set_bias(bias)
    held = {"rest_hz_by_step": [round(r, 2) for r in rates], "bias_step_mv": round(step, 2),
            "rest_hz": round(float(p10.resting(o, rec, SEED + 949)["hz"][mbon].mean()), 2)}
    print("depressing" if depressing else "undepressed", "held", json.dumps(held), "gain", json.dumps(gain), flush=True)
    row = {"depressing": depressing, "held": held, "mbon11_gain": gain, "weight_per_synapse_mv": round(w_syn, 4), "pre": {},
           "pairings": []}

    def tests(odor: str, k: int) -> dict:
        r = [lp3.trial(o, rec, odor, SEED + 10 * k + j, mbon, kc, f, recover_s) for j in range(lp.SEEDS)]
        spikes = np.concatenate([x["mbon"] for x in r])
        return {"spikes": float(spikes.mean()), "sem": float(spikes.std(ddof=1) / np.sqrt(len(spikes))),
                "kc_evoked": np.mean([x["kc_evoked"] for x in r], 0), "kc_delivered": np.mean([x["kc_delivered"] for x in r], 0)}
    pre = {odor: tests(odor, k) for k, odor in enumerate(p7.ODORS)}
    for odor, r in pre.items():
        row["pre"][odor] = {"mbon11_evoked_spikes": round(r["spikes"], 2), "sem": round(r["sem"], 2),
                            "charge": round(float((per_kc * np.clip(r["kc_delivered"], 0, None)).sum()), 1),
                            "kcs_with_evoked_spikes_over_0.5": int((r["kc_evoked"] > 0.5).sum())}
        print("  pre", odor, json.dumps(row["pre"][odor]), flush=True)
    row["overlap"] = {}
    for paired, unpaired in lp.PAIRS:
        a, u = pre[paired]["kc_evoked"] > 0.5, pre[unpaired]["kc_evoked"] > 0.5
        evoked = per_kc * np.clip(pre[unpaired]["kc_delivered"], 0, None)
        row["overlap"][f"{unpaired} in {paired}"] = {
            "share_of_responders": round(float((a & u).sum() / max(u.sum(), 1)), 3),
            "jaccard": round(float((a & u).sum() / max((a | u).sum(), 1)), 3),
            "share_of_charge": round(float(evoked[a].sum() / max(evoked.sum(), 1e-12)), 3)}
    print("  overlap", json.dumps(row["overlap"]), flush=True)

    def charge(log_scale: np.ndarray, odor: str) -> float:
        return float((per_kc * np.exp(log_scale) * np.clip(pre[odor]["kc_delivered"], 0, None)).sum())

    for i, (paired, unpaired) in enumerate(lp.PAIRS):
        fw = [lp3.trial(o, rec, paired, SEED + 200 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
        bw = [lp3.trial(o, rec, paired, SEED + 300 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
        pr = {"paired": paired, "unpaired": unpaired, "by_tau": {}}
        log_scale = None
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
            pr["by_tau"][str(tau)] = {"eta": round(eta, 4), "reachable": bool(hi < 1e6), "charge_drop": drop,
                                      "backward_charge_drop": round(1 - charge(-eta * Eb, paired) / base, 3),
                                      "kcs_losing_half": int((np.exp(-eta * E) < 0.5).sum())}
            print("  ", paired, "tau", tau, json.dumps(pr["by_tau"][str(tau)]), flush=True)
            if tau == 0.5:
                log_scale = -eta * E
        w = w0.copy()
        w[onto] = w0[onto] * np.exp(log_scale[kc_of])
        b.weights, b._external_matrix = w.astype(np.float32), None
        post = {od: tests(od, p7.ODORS.index(od)) for od in (paired, unpaired)}
        pr["spikes"] = {od: {"pre": round(pre[od]["spikes"], 2), "post": round(post[od]["spikes"], 2),
                             "sem": [round(pre[od]["sem"], 2), round(post[od]["sem"], 2)],
                             "drop": round(1 - post[od]["spikes"] / pre[od]["spikes"], 3) if pre[od]["spikes"] > 0 else None}
                        for od in (paired, unpaired)}
        print("  ", paired, "spikes", json.dumps(pr["spikes"]), flush=True)
        b.weights, b._external_matrix = w0.copy(), None
        row["pairings"].append(pr)
        out["variants"]["depressing" if depressing else "undepressed"] = row
        OUT.write_text(json.dumps(out, indent=1))
    b.set_bias(bias0)
    return row


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o), "variants": {}}
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        for depressing in VARIANTS:
            variant(o, rec, depressing, out)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
