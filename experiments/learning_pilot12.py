"""Exploratory, not pre-registered: learning pilot 11's weighed-input condition with the Kenyon cell-to-MBON current as
slow as Yamada et al. 2024's flash EPSC. Does MBON11 then answer odors as flies' does, and how does rung 9's learning test
come out?

mbon11_burst_check.py: what ends the model's MBON11 response to an odor within 0.3 s (flies' holds 95-100 spikes/s to the
odor's end) is the depression of its Kenyon cell synapses. kc_flash_check.py: Yamada et al.'s flash EPSC, which the
depression rule reads as one spike per flash, peaks about 100 ms after the flash and fades over hundreds of milliseconds;
the model's flashed Kenyon cells fire within about 50 ms at any membrane time constant from 20 to 150 ms, so through the
model's 5 ms synapses the current peaks within 20 ms, 8-80 times higher than flies'; through a slow current (rising with
40 ms, decaying with 280 ms) the same input matches their time course and their paired-pulse ratio at one spike per
flash. mbon11_slow_epsc.py: that slow current turns the model's Kenyon cell activity during 3-octanol into an EPSC of 347
pA at its peak and 83 pA from 0.6 to 1 s (flies about 400 and 170), about 75 spikes through MBON11's gain (flies 118).
Model: learning_movie.py's (learning pilot 11's weighed input: odor_probe60.py's cache, mb_calibration4.py's mushroom
body, receptor_fills.RECOMMENDED, the Kenyon cells' rest set as the pilots set it, MBON11 keeping its current and held
near 6 Hz, its Kenyon cell synapses at 0.054 pC each, depressing as measured), with every Kenyon cell-to-MBON synapse moved
into the targets' slow current (HybridBrain's slow_rise 40 ms, tau_slow 280 ms, slow_keep: the current kept through
spikes), each weighted by 5 / 280 so that a spike carries the charge it did, depressing with its Kenyon cell as before.
Protocol, rule, fit and measures as learning pilot 11 (learning_pilot4.variant's, rewritten for synapses in the slow
current; the same seeds, 640000), with MBON11's spikes and slow current recorded in 10 ms bins over -0.5 to 1.5 s of every
test; and Yamada et al.'s flash as kc_flash_check.py gives it (5% of the gamma Kenyon cells, one spike each, at 0 and 0.4
s; MBON11 silenced), MBON11's slow current recorded in 2 ms bins, all before any pairing.
The slow current as pA: the model's MBON11 turns s mV into 3.46 spikes/s and Wang et al. 2026's 0.41 spikes/s per pA,
so s mV is about 8.4 pA (the calibration the synapses' weights came from; odor_probe31.py).
Adopted into the model carried forward (stated before the run) if (1) its flash EPSC passes kc_flash_check.py's reading
(peak 80-140 ms after the flash, 180-320 ms wide at half its peak, 0.25-0.45 left at 400 ms, PPR 0.38-0.68): a check that
the synapse does what it was built to; and (2) MBON11's response to 3-octanol before pairing moves toward flies' on what
the slow current wasn't chosen from: its evoked spikes nearer flies' 118 than learning pilot 11's 38.6, its rate from 0.5
to 1 s nearer flies' 95-100 than 12, and its peak (smoothed as Hige et al.'s, a Gaussian with an SD of 50 ms) within
100-180 spikes/s (flies 135-140). Rung 9's four marks are reported either way; a second attempt still needs the weighed
input to pass them all.

    python experiments/learning_pilot12.py      (writes experiments/learning_pilot12.json)
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
FLASH_A, FLASH_SHARE, TAU_OFF = 107.9, 0.05, 0.021      # kc_flash_check.py's one spike per flashed cell at 20 ms
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


def flash(o, rec, h: dict, to_pa: float) -> dict:
    """kc_flash_check.py's flash (5% of the gamma Kenyon cells, one spike each, at 0 and 0.4 s; MBON11 silenced), with
    MBON11's slow current read in 2 ms bins over -0.1 to 1.5 s; 4 seeds of 8 flies."""
    b = o.brain
    gamma = np.flatnonzero(mb_calibration.classes(o)["gamma"])
    base = b.bias.copy()
    piece, n_bins = int(round(0.002 / b.dt)), 800
    series = []
    for j in range(lp.SEEDS):
        flashed = np.sort(np.random.default_rng(990000 + j).choice(gamma, int(round(FLASH_SHARE * len(gamma))), replace=False))
        b.reset(990000 + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        drive = p24.spontaneous(rec)
        b.advance(int(round(0.5 / b.dt)), drive=drive, silence=h["mbon"])
        s, stepped = [], False
        try:
            for k in range(n_bins):
                t = -0.1 + k * 0.002
                on = [t0 for t0 in (0.0, 0.4) if t0 - 1e-9 <= t < t0 + 0.15]
                if on:
                    bias = base.copy()
                    bias[flashed] += FLASH_A * np.exp(-(t - on[-1] + 0.001) / TAU_OFF)
                    b.set_bias(bias)
                    stepped = True
                elif stepped:
                    b.set_bias(base)
                    stepped = False
                b.advance(piece, drive=drive, silence=h["mbon"])
                s.append(float(b.s[:, h["mbon"]].mean()))
        finally:
            b.set_bias(base)
        series.append(s)
    t = -0.1 + (np.arange(n_bins) + 0.5) * 0.002
    i = (np.mean(series, 0) - np.mean(series, 0)[t < 0].mean()) * to_pa
    w1 = (t > 0) & (t < 0.4)
    j = int(np.argmax(np.where(w1, i, -np.inf)))
    peak = float(i[j])
    above = np.flatnonzero(w1 & (i >= peak / 2))
    left = float(i[(t > 0.39) & (t < 0.4)].mean())
    peak2 = float(i[(t > 0.4) & (t < 0.8)].max())
    out = {"peak_pa": round(peak, 1), "t_peak_s": round(float(t[j]), 3), "half_width_s": round(float((above[-1] - above[0] + 1) * 0.002), 3),
           "left_at_400ms": round(left / peak, 3), "ppr": round((peak2 - left) / peak, 3), "series_pa": np.round(i, 2).tolist()}
    out["matches"] = bool(0.08 <= out["t_peak_s"] <= 0.14 and 0.18 <= out["half_width_s"] <= 0.32 and 0.25 <= out["left_at_400ms"] <= 0.45
                          and 0.38 <= out["ppr"] <= 0.68)
    return out


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
        kc, mbon, f, recover_s, per_kc = h["kc"], h["mbon"], h["f"], h["recover_s"], h["per_kc"]
        out["installed"] = install(o)
        to_pa = h["gain"]["slope_hz_per_mv"] / p31.GAIN_HZ_PER_PA
        spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
        onto = np.flatnonzero(o.m["kc"][spre] & np.isin(b.sidx, mbon))
        kc_of = np.searchsorted(kc, spre[onto])
        sw0 = b.slow_weights.copy()
        out["held"] = {"bias_step_mv": round(h["bias_step_mv"], 2), "gain": h["gain"], "pa_per_mv": round(to_pa, 3),
                       "rest_hz_with_slow_synapses": round(float(p10.resting(o, rec, SEED + 949)["hz"][mbon].mean()), 2)}
        print("installed", json.dumps(out["installed"]), "held", json.dumps(out["held"]), flush=True)
        out["flash"] = flash(o, rec, h, to_pa)
        print("flash", json.dumps({k: v for k, v in out["flash"].items() if k != "series_pa"}), f"({time.perf_counter() - t0:.0f} s)", flush=True)

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
    out["adoption"] = {"flash_matches": out["flash"]["matches"],
                       "spikes_nearer_flies": abs(oct_pre["mbon11_evoked_spikes"] - 118) < abs(38.6 - 118),
                       "late_rate_nearer_flies": abs(oct_pre["hz_0.5_to_1s"] - 97.5) < abs(12.4 - 97.5),
                       "peak_in_100_to_180": 100 <= oct_pre["peak_hz"] <= 180}
    out["adoption"]["adopted"] = all(out["adoption"].values())
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print("marks", json.dumps(out["marks"]), "adoption", json.dumps(out["adoption"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
