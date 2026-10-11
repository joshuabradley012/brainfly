"""Exploratory, not pre-registered: learning pilot 12 with the alpha/beta Kenyon cells' synapses onto MBON11 carrying
the charge Yamada et al.'s alpha/beta flashes give. Does MBON11 then answer odors as strongly as flies', and how does rung
9's learning test come out?

learning_pilot12.py adopted a slow Kenyon cell-to-MBON current (mb_calibration5.py); MBON11 then gains 70.8 evoked spikes
to 3-octanol (flies 118) and fires 51 spikes/s from 0.5 to 1 s (flies 95-100), short of flies' because the Kenyon cells'
firing falls away through the odor, the gamma cells' most (pn_accommodation_check.py: their projection neurons don't).
Every Kenyon cell synapse onto MBON11 carries 0.054 pC, set from Yamada et al. 2024's gamma flashes. Their alpha/beta
flashes (Fig. 8, three example cells) carry 58-87 pC against the gamma examples' 28-36, from cells making a third as many
synapses on MBON11 (6.5-9.3 per cell against 21.4): at the same labelled share and one spike per flash, each alpha/beta
synapse carries about 0.1-0.5 pC, 4-6 times the gamma value (research_notes/Rung 9 learning data/mbon11_kc_activity.md
2.4; possible other causes: more spikes per flash in the more excitable alpha/beta cells, different labelling, better
clamp). In the model the alpha/beta cells hold their firing better than the gamma ones (mbon11_burst_check.py: 0.18 of
their early rate from 0.5 to 1 s, against 0.05).
Model: learning pilot 12's, with the alpha/beta Kenyon cells' synapses onto MBON11 at 4 times the charge (0.22 pC, the low
end of the range above) before they move into the slow current. Protocol, rule, fit, seeds and measures as learning pilot
12, without the flash.

Ran (2026-10-11, 15 minutes): MBON11 now answers more strongly than flies', and the marks come out as before. To
3-octanol it gains 152 evoked spikes (learning pilot 12 70.8; flies 118), peaks at 211 spikes/s (122; flies 135-140) and
fires 114 from 0.5 to 1 s (51; flies 95-100); its slow current peaks at 841 pA and holds 266, 504 pC over 0-1.4 s (flies
about 400, 170 and 245-275). To 4-methylcyclohexanol 25.3 spikes (11.4; flies 110). Learning: PAIRED passes (87.5%, 45
points more than 4-methylcyclohexanol's), UNPAIRED passes (42.1%; charge 43.4%), RECIPROCAL fails (3-octanol's spikes fall
8.0%; band 15-50%), BACKWARD passes (0.0% and 0.3%). So the alpha/beta synapses' strength sets MBON11's amplitude and not
the learning marks, which follow the Kenyon cell sets. At 4 times the charge MBON11's input is about twice flies'; with
the alpha/beta cells carrying about half of the drive (mbon11_burst_check.py), flies' 245-275 pC would come at about 1.6-1.9
times, inside what Yamada et al.'s alpha/beta flashes allow if those cells fire more than once per flash. Not taken
further: choosing the factor from flies' odor EPSC would fit the measure the slow current was tested on.

    python experiments/learning_pilot14.py      (writes experiments/learning_pilot14.json)
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
import mb_calibration3 as mb3
import mbon11_burst_check as burst
import odor_probe24 as p24
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe7 as p7
import odor_probe8 as p8
import odor_probe10 as p10
import warm
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED = 640000
TAU_SLOW, RISE = 0.280, 0.040
AB_SCALE = 4.0                                          # the alpha/beta synapses' charge over the gamma-derived 0.054 pC
SD_S = 0.05


def install(o) -> dict:
    """Every Kenyon cell-to-MBON synapse moved into its target's slow current (its weight x TAU / TAU_SLOW), the MBONs'
    slow current rising with RISE, decaying with TAU_SLOW and kept through spikes."""
    b = o.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    moved = np.flatnonzero(o.kc_mbon & (b.weights != 0))
    mbons = np.unique(b.idx[moved])
    if np.isin(mbons, b.stargets).any():
        raise RuntimeError("an MBON already has slow input, whose time constant this would change")
    w = b.weights.copy()
    weights = w[moved] * np.float32(TAU / TAU_SLOW)
    w[moved] = 0.0
    b.weights, b._external_matrix = w, None
    mb3.add_slow_edges(b, pre[moved], b.idx[moved], b._counts[moved], weights)
    b.sets = {**b.sets, "mbons_from_kcs": mbons}
    b.set_type("mbons_from_kcs", tau_slow=TAU_SLOW, slow_rise=RISE, slow_keep=1.0)
    return {"synapses_moved": int(len(moved)), "mbons": int(len(mbons))}


def recorded(o, rec, odor: str, seed: int, mbon: np.ndarray, kc: np.ndarray, f: float, recover_s: float) -> dict:
    """learning_pilot3.trial, with MBON11's spikes and slow current per 10 ms bin from -0.5 to 1.5 s."""
    b = o.brain
    plain = b.advance
    hz, s = [], []

    def advance(*args, **kwargs):
        c = plain(*args, **kwargs)
        hz.append(float(c[:, mbon].mean()) / lp.BIN)
        s.append(float(b.s[:, mbon].mean()))
        return c
    b.advance = advance
    try:
        out = lp3.trial(o, rec, odor, seed, mbon, kc, f, recover_s)
    finally:
        del b.advance
    n_pre, n_odor = int(round(lp.PRE / lp.BIN)), int(round(1.0 / lp.BIN))
    keep = slice(len(hz) - (n_pre + 2 * n_odor) + n_pre - 50, len(hz) - (n_pre + 2 * n_odor) + n_pre + 150)
    out["mbon11_hz"], out["mbon11_s"] = np.array(hz[keep]), np.array(s[keep])
    return out


def smooth(v: np.ndarray, dt: float) -> np.ndarray:
    half = int(round(3 * SD_S / dt))
    k = np.exp(-0.5 * (np.arange(-half, half + 1) * dt / SD_S) ** 2)
    return np.convolve(np.pad(v, half, mode="edge"), k / k.sum(), mode="valid")


def shape(hz: np.ndarray, s_pa: np.ndarray) -> dict:
    """MBON11's rate and slow current over -0.5 to 1.5 s: the peak smoothed as Hige's and when, the share of the evoked
    spikes in the first 0.3 s, the rate from 0.5 to 1 s; the current's peak, its mean from 0.6 to 1 s and its charge."""
    t = -0.5 + (np.arange(len(hz)) + 0.5) * lp.BIN
    rest = hz[t < 0].mean()
    window = (t > 0) & (t < 1.4)
    evoked = hz[window] - rest
    sm = smooth(hz, lp.BIN)
    i = s_pa - s_pa[t < 0].mean()
    j = int(np.argmax(i))
    return {"peak_hz": round(float(sm.max()), 1), "t_peak_s": round(float(t[np.argmax(sm)]), 3),
            "share_in_first_0.3s": round(float(evoked[t[window] < 0.3].sum() / max(evoked.sum(), 1e-9)), 3),
            "hz_0.5_to_1s": round(float(hz[(t > 0.5) & (t < 1.0)].mean()), 2), "rest_hz": round(float(rest), 2),
            "current_peak_pa": round(float(i[j]), 1), "current_t_peak_s": round(float(t[j]), 3),
            "current_pa_0.6_to_1s": round(float(i[(t > 0.6) & (t < 1.0)].mean()), 1),
            "current_charge_pc_0_to_1.4s": round(float(i[window].sum() * lp.BIN), 1)}


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = burst.CHARGE_PC
    lp3.DEPRESSING = True
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    b = o.brain
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "bin_s": lp.BIN, "t0": -0.5}
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        b.set_type("MBON11", keep_current=1.0)
        h = burst.hold(o, rec, True)                    # the fast weights, the depression and the hold, as the pilots set them
        kc, mbon, f, recover_s = h["kc"], h["mbon"], h["f"], h["recover_s"]
        alpha_beta = mb_calibration.classes(o)["alpha/beta"]
        pre_f = np.repeat(np.arange(b.n), np.diff(b.ptr))
        ab_onto = np.flatnonzero(alpha_beta[pre_f] & np.isin(b.idx, mbon))
        w_ab = b.weights.copy()
        w_ab[ab_onto] *= np.float32(AB_SCALE)
        b.weights, b._external_matrix = w_ab, None
        per_kc = h["per_kc"] * np.where(alpha_beta[kc], AB_SCALE, 1.0)
        out["alpha_beta"] = {"scale": AB_SCALE, "synapses_onto_mbon11": int(b._counts[ab_onto].sum()), "edges": int(len(ab_onto))}
        out["installed"] = install(o)
        to_pa = h["gain"]["slope_hz_per_mv"] / p31.GAIN_HZ_PER_PA
        spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
        onto = np.flatnonzero(o.m["kc"][spre] & np.isin(b.sidx, mbon))
        kc_of = np.searchsorted(kc, spre[onto])
        sw0 = b.slow_weights.copy()
        out["held"] = {"bias_step_mv": round(h["bias_step_mv"], 2), "gain": h["gain"], "pa_per_mv": round(to_pa, 3),
                       "rest_hz_with_slow_synapses": round(float(p10.resting(o, rec, SEED + 949)["hz"][mbon].mean()), 2)}
        print("installed", json.dumps(out["installed"]), "held", json.dumps(out["held"]), flush=True)

        def tests(odor: str, k: int) -> dict:
            r = [recorded(o, rec, odor, SEED + 10 * k + j, mbon, kc, f, recover_s) for j in range(lp.SEEDS)]
            spikes = np.concatenate([x["mbon"] for x in r])
            hz, s = np.mean([x["mbon11_hz"] for x in r], 0), np.mean([x["mbon11_s"] for x in r], 0)
            return {"spikes": float(spikes.mean()), "sem": float(spikes.std(ddof=1) / np.sqrt(len(spikes))),
                    "kc_evoked": np.mean([x["kc_evoked"] for x in r], 0), "kc_delivered": np.mean([x["kc_delivered"] for x in r], 0),
                    "shape": shape(hz, s * to_pa), "hz": hz, "s_pa": s * to_pa}
        pre = {odor: tests(odor, k) for k, odor in enumerate(p7.ODORS)}
        out["pre"] = {}
        for odor, r in pre.items():
            out["pre"][odor] = {"mbon11_evoked_spikes": round(r["spikes"], 2), "sem": round(r["sem"], 2),
                                "charge": round(float((per_kc * np.clip(r["kc_delivered"], 0, None)).sum()), 1),
                                "kcs_with_evoked_spikes_over_0.5": int((r["kc_evoked"] > 0.5).sum()), **r["shape"]}
            print("  pre", odor, json.dumps(out["pre"][odor]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        out["series"] = {f"pre {od}": {"hz": np.round(pre[od]["hz"], 2).tolist(), "s_pa": np.round(pre[od]["s_pa"], 2).tolist()}
                         for od in lp.PAIRS[0]}

        def charge(log_scale: np.ndarray, odor: str) -> float:
            return float((per_kc * np.exp(log_scale) * np.clip(pre[odor]["kc_delivered"], 0, None)).sum())

        out["pairings"] = []
        for i, (paired, unpaired) in enumerate(lp.PAIRS):
            fw = [lp3.trial(o, rec, paired, SEED + 200 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
            bw = [lp3.trial(o, rec, paired, SEED + 300 + 10 * i + j, mbon, kc, f, recover_s)["kc_bins"] for j in range(lp.SEEDS)]
            pr = {"paired": paired, "unpaired": unpaired}
            E = np.mean([lp.eligibility(x, lp.FORWARD, 0.5) for x in fw], 0)
            Eb = np.mean([lp.eligibility(x, lp.BACKWARD, 0.5) for x in bw], 0)
            base = charge(np.zeros(len(kc)), paired)
            lo, hi = 0.0, 1.0
            while 1 - charge(-hi * E, paired) / base < lp.TARGET and hi < 1e6:
                lo, hi = hi, hi * 4
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if 1 - charge(-mid * E, paired) / base < lp.TARGET else (lo, mid)
            eta = 0.5 * (lo + hi)
            log_scale = -eta * E
            pr["fit"] = {"eta": round(eta, 4), "charge_drop": {od: round(1 - charge(log_scale, od) / charge(np.zeros(len(kc)), od), 3) for od in p7.ODORS},
                         "backward_charge_drop": round(1 - charge(-eta * Eb, paired) / base, 3)}
            sw = sw0.copy()
            sw[onto] = sw0[onto] * np.exp(log_scale[kc_of]).astype(np.float32)
            b.slow_weights = sw
            post = {od: tests(od, p7.ODORS.index(od)) for od in (paired, unpaired)}
            b.slow_weights = sw0.copy()
            pr["spikes"] = {od: {"pre": round(pre[od]["spikes"], 2), "post": round(post[od]["spikes"], 2),
                                 "sem": [round(pre[od]["sem"], 2), round(post[od]["sem"], 2)],
                                 "drop": round(1 - post[od]["spikes"] / pre[od]["spikes"], 3) if pre[od]["spikes"] > 0 else None,
                                 "post_shape": post[od]["shape"]} for od in (paired, unpaired)}
            for od in (paired, unpaired):
                out["series"][f"{paired} paired, {od}"] = {"hz": np.round(post[od]["hz"], 2).tolist(), "s_pa": np.round(post[od]["s_pa"], 2).tolist()}
            print("  ", paired, json.dumps({"fit": pr["fit"], "spikes": {od: {k: v for k, v in x.items() if k != "post_shape"} for od, x in pr["spikes"].items()}}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            out["pairings"].append(pr)
            OUT.write_text(json.dumps(out))
    s_ = {p["paired"]: p for p in out["pairings"]}
    oct_, mch = lp.PAIRS[0]
    sd = lambda paired, od: s_[paired]["spikes"][od]["drop"]
    cd = lambda paired, od: s_[paired]["fit"]["charge_drop"][od]
    out["marks"] = {"PAIRED": {"oct_spikes_drop": sd(oct_, oct_), "gap": round(sd(oct_, oct_) - sd(oct_, mch), 3)},
                    "UNPAIRED": {"mch_spikes_drop": sd(oct_, mch), "mch_charge_drop": cd(oct_, mch)},
                    "RECIPROCAL": {"mch_spikes_drop": sd(mch, mch), "gap": round(sd(mch, mch) - sd(mch, oct_), 3), "oct_spikes_drop": sd(mch, oct_)},
                    "BACKWARD": {"oct_paired_charge_change": s_[oct_]["fit"]["backward_charge_drop"],
                                 "mch_paired_charge_change": s_[mch]["fit"]["backward_charge_drop"]}}
    m = out["marks"]
    m["PAIRED"]["pass"] = m["PAIRED"]["oct_spikes_drop"] >= 0.65 and m["PAIRED"]["gap"] >= 0.30
    m["UNPAIRED"]["pass"] = all(0.10 <= x <= 0.45 for x in (m["UNPAIRED"]["mch_spikes_drop"], m["UNPAIRED"]["mch_charge_drop"]))
    m["RECIPROCAL"]["pass"] = m["RECIPROCAL"]["mch_spikes_drop"] >= 0.65 and m["RECIPROCAL"]["gap"] >= 0.30 and 0.15 <= m["RECIPROCAL"]["oct_spikes_drop"] <= 0.50
    m["BACKWARD"]["pass"] = all(abs(x) <= 0.15 for x in (m["BACKWARD"]["oct_paired_charge_change"], m["BACKWARD"]["mch_paired_charge_change"]))
    oct_pre = out["pre"][oct_]
    out["marks"]["pass"] = all(m[k]["pass"] for k in ("PAIRED", "UNPAIRED", "RECIPROCAL", "BACKWARD"))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print("marks", json.dumps(out["marks"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
