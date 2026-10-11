"""Exploratory, not pre-registered: learning pilot 12 with the Kenyon cells of kc_integration.md's set C. Does rung 9's
reciprocal mark move?

kc_setc_check.py: of the Kenyon cell sets that keep Gruntman & Turner's plateau, set C (a 50 ms membrane, the projection
neuron-to-Kenyon cell synapses keeping 0.85 of their strength per spike and recovering over 0.1 s, scaled so that a resting
synapse's EPSP peaks as now) keeps flies' density (10.7% of the cells answering 3-octanol; flies about 12%) and APL's effect
(silencing it raises the spikes 2.8 and 2.7-fold; flies 2-3), and moves 4-methylcyclohexanol toward 3-octanol (0.28 as
many cells answering, against 0.18) and the share of 3-octanol's cells that 4-methylcyclohexanol reaches toward flies' (0.17
against 0.10; flies 0.30), on which the reciprocal mark turns (learning_pilot11.py: pairing 4-methylcyclohexanol cuts
3-octanol's response by about the share of its charge 4-methylcyclohexanol's cells carry). Its input to MBON11 is smaller
(126 pC to 3-octanol through the slow current, against 202; flies 245-275).
Model: learning pilot 12's (mb_calibration5.py's slow Kenyon cell current included), with set C's Kenyon cells installed
before their rest is set (as kc_setc_check.py installs them). Protocol, rule, fit, seeds and measures as learning pilot 12,
without the flash.
Rung 9's marks reported as rung9_learning.py states them. If all four pass with this input, rung 9's standing rule allows a
second attempt (the input the evidence supports, set C chosen from Gruntman & Turner's measurements before any learning
result, fresh seeds); if not, set C stays a candidate.

Ran (2026-10-11, 15 minutes): set C moves the reciprocal into flies' band and spoils the other marks, so there is no second
attempt. Before pairing, 479 Kenyon cells answer 3-octanol and 129 4-methylcyclohexanol (0.27 as many), and MBON11 gains
45.8 and 9.5 spikes (learning pilot 12 70.8 and 11.4; flies 118 and 110), peaking at 76 spikes/s to 3-octanol and firing
36 from 0.5 to 1 s; its slow current peaks at 191 pA, 108 pC (flies about 400 and 245-275).
  PAIRED      fails: 3-octanol's spikes fall 92.4%, but only 25.5 points more than 4-methylcyclohexanol's (30 required).
  UNPAIRED    fails: 4-methylcyclohexanol's spikes fall 66.9% and its charge 62.7% (band 10-45%; flies 27%).
  RECIPROCAL  passes: 4-methylcyclohexanol paired cuts its own 97.6% and 3-octanol's 36.4% (band 15-50%; flies 38%).
  BACKWARD    fails, narrowly: the paired odor's charge changes 1.9% and 16.0% (at most 15%; the second at eta 11.6, the
              rule driving 4-methylcyclohexanol's small charge down 90%).
Learning pilot 12 failed only the reciprocal (9.4%). Here 4-methylcyclohexanol's Kenyon cells reach more of 3-octanol's,
so pairing it cuts 3-octanol as flies' does, but they also sit mostly inside 3-octanol's set (kc_setc_check.py: 0.62 of
them answer 3-octanol; flies 0.33), so pairing 3-octanol cuts 4-methylcyclohexanol two and a half times as much as flies'.
Flies' two odors reach separate sets of about the same size, sharing about a third each way; the model's
4-methylcyclohexanol reaches a small set nested in 3-octanol's, with either Kenyon cell set, which points again at its
projection neurons: too few of its glomeruli answer, and its strongest after VA3 (D) is one of 3-octanol's
(odor_mch_input_sensitivity.py: with the glomeruli flies' projection neuron imaging adds, a fly-like 0.28 of its cells
answered 3-octanol).

Correction (2026-10-11, after an independent review):
- The Kenyon cells' rest wasn't set back to their distances below threshold after set C was installed.
  odor_probe33.set_rest's first pass measured them with the old 20 ms time constant's share of the bias, and its second
  pass didn't undo the overshoot (kc_rest.py). The JSON's kc_rest records them resting nearer threshold than the
  targets: alpha/beta by 3.1 mV, alpha'/beta' by 4.3-4.5, gamma by up to 3.1. The alpha'/beta' cells fired 0.12
  spikes/s at rest, 30 times learning pilot 12's rate. These aren't kc_setc_check.py's set C cells either, whose rest
  was off differently (alpha'/beta' 14.5 mV from threshold there, 11.7 here). So the run above tests set C with cells
  nearer threshold than meant. learning_pilot15.py runs it again with the rest held.
- "Nested" overstates it. 0.62 of 4-methylcyclohexanol's answering cells answer 3-octanol in kc_setc_check.py's set C,
  so 38% lie outside 3-octanol's set: mostly inside.
- "Too few of its glomeruli answer" is an inference (odor_mch_input_sensitivity.py's own note says so), not a finding.
  As tested, 13 glomeruli answer 4-methylcyclohexanol and 16 answer 3-octanol (more than 20 spikes/s above rest;
  pn_accommodation_check.py). The bigger difference is strength: the answering glomeruli peak at 64 spikes/s against 133.
- Flies' 3-octanol charge is about 245-250 pC (Hige et al.'s 248 and 244). 245-275 pools both odors;
  4-methylcyclohexanol's is 230-273 (Hige's Figs. 4H and 3D; amended after a second review).
- "Moves the reciprocal into flies' band": the band, 15-50%, is rung 9's, set around flies' 38%.

Correction (2026-10-11, kc_input_audit.py): set C's synapses were scaled from the model's own EPSP, 1.90 mV per
connection (kc_setc_check.py's correction), so they carried about 5.5 mV per connection at 115 spikes/s, not
kc_integration.md's 3.9 (flies about 4.4).

    python experiments/learning_pilot13.py      (writes experiments/learning_pilot13.json)
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
import kc_membrane_check as km
import kc_setc_check as ksc
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
SD_S = 0.05


def set_c(o) -> dict:
    """kc_setc_check.py's set C: the Kenyon cells' membrane time constant 50 ms; the projection neuron-to-Kenyon cell
    synapses depressing on their own (0.85, 0.1 s) and scaled so that a resting synapse's EPSP peaks as now."""
    b, m = o.brain, o.m
    tau_m, f, recovery = ksc.SETS["C"]
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    pn_kc = m["upn"][pre] & m["kc"][b.idx]
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    if m["upn"][spre].any():
        raise RuntimeError("projection neurons have slow synapses, which their slow_depression would change")
    scale = km.peak_per_w(0.020) / km.peak_per_w(tau_m) / ksc.resting_strength(f, recovery)
    w = b.weights.copy()
    w[pn_kc] *= np.float32(scale)
    b.weights, b._external_matrix = w, None
    full = b.full_strength.copy()
    full[pn_kc] = False
    b.full_strength = full
    b.own_depression = pn_kc.copy()
    b.set_type("uPN", slow_depression=f, slow_recovery=recovery)
    b.set_type("kenyon_cells", tau_m=tau_m)
    return {"tau_m_s": tau_m, "depression": f, "recovery_s": recovery, "pn_kc_scale": round(float(scale), 3), "synapses": int(pn_kc.sum())}


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
        out["set_c"] = set_c(o)
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
