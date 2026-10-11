"""Exploratory check, not pre-registered and not a change to the model: why does the model's MBON11 answer odors in a
burst, where flies' holds?

learning_movie.py: smoothed as Hige et al. smoothed theirs (a Gaussian, SD 50 ms), MBON11's response to 3-octanol peaks at
144 spikes/s 85 ms after the odor's onset, about as high as flies' (135-140 at about 0.3 s; Hige et al. 2015, Fig. 1E),
but 79% of its evoked spikes come in the first 0.3 s, and from 0.5 to 1 s it fires 12 spikes/s where flies' holds 95-100.
Flies' odor EPSC in MBON11 holds too: about 400 pA at its peak, 170 pA from 0.6 to 1.0 s (0.43 of the peak; Fig. 3C;
research_notes/Rung 9 learning data/mbon11_input.md). Three things could end the model's response: its Kenyon cells stop
firing (APL's inhibition, which now builds over 0.1-0.5 s, or their own adaptation), their synapses onto MBON11 depress (0.5
of the strength left per spike, recovering over 1.5 s; learning_pilot3.py's reading of Yamada et al. 2024), or MBON11
adapts. For comparison, flies: Murthy et al. 2008's alpha/beta-c Kenyon cells keep a median 0.40 of their peak
depolarization at 0.95 s of a 1 s odor; Turner et al. 2008's fire 2.2 (alpha/beta) and 4.9 (alpha'/beta') spikes per
response to 0.5 s odors; Yamada et al.'s flash-evoked EPSC peaks about 100 ms after the flash and keeps about 0.3 of its
peak at 400 ms (mbon11_kc_activity.md).
Model: learning_movie.py's (learning pilot 11's weighed-input condition: odor_probe60.py's cache, mb_calibration4.py's
mushroom body, receptor_fills.RECOMMENDED, MBON11 keeping its current and held near 6 Hz), before any pairing.
Conditions: as in the learning test; the Kenyon cell-to-MBON11 synapses not depressing; APL silenced; both. 3-octanol and
4-methylcyclohexanol, each with the learning test's seeds (640000 + 10 x odor + seed, 4 seeds of 8 flies) in every
condition, learning_pilot3.trial's protocol (the first condition should repeat learning_movie.py's recording).
Measured, per condition and odor, in 10 ms bins from 0.5 s before the odor to 1.5 s after its onset: MBON11's rate and
membrane potential; the Kenyon cells' spikes by class; the Kenyon cells answering in four windows (0-0.1, 0.1-0.3, 0.3-0.6,
0.6-1.0 s; at least one spike); the drive the Kenyon cells deliver onto MBON11 (each synapse's weight times its Kenyon
cell's spikes times the strength its depression has left, read at the start of each bin), by class; and APL's release.
Summaries: MBON11's peak (smoothed as Hige's), the share of its evoked spikes (0-1.4 s, above the rest) in the first 0.3 s
and its rate from 0.5 to 1 s; the delivered drive from 0.6 to 1.0 s over its peak (smoothed alike; flies' EPSC 0.43); and
by class the Kenyon cells' rate from 0.5 to 1 s over their rate in the first 0.3 s.

Ran (2026-10-11, 9 minutes): the depression ends it. The first condition repeats learning_movie.py's recording to the
hundredth (3-octanol: MBON11's peak 143.6 spikes/s at 85 ms, 38.6 evoked spikes, 79% of them in the first 0.3 s, 12.4
spikes/s from 0.5 to 1 s). With the Kenyon cell-to-MBON11 synapses not depressing, MBON11 holds as flies' does: 94
spikes/s from 0.5 to 1 s (flies 95-100), 41% of its evoked spikes in the first 0.3 s and 132 evoked spikes (flies 118),
though it peaks too high (224 spikes/s at 0.245 s; flies 135-140). With APL silenced the Kenyon cells fire about twice
as much, but MBON11's response stays brief (208 spikes/s at its peak, 69% of 73.9 evoked spikes in the first 0.3 s, 28
spikes/s from 0.5 to 1 s); with both, 323 spikes/s, 194 spikes and 135 spikes/s from 0.5 to 1 s. As tested, the Kenyon
cells keep firing, from 0.5 to 1 s at 0.18 (alpha/beta), 0.25 (alpha'/beta') and 0.05 (gamma) of their rate in the first
0.3 s, with 55, 53 and 6 cells of each class per fly still firing from 0.6 to 1.0 s (236, 168 and 107 in the first 0.1 s);
but their synapses, depressed by the early spikes, deliver from 0.6 to 1.0 s only 1.3% of the drive's peak (undepressed
0.20; flies' EPSC 0.43). Two thirds of MBON11's Kenyon cell synapses, by weight, are gamma cells', the least sustained
class. To 4-methylcyclohexanol MBON11 stays weak in every condition (7.8-33 evoked spikes; flies 110), since too few
Kenyon cells answer it.
So the depression rule, each spike leaving 0.5 of the strength and recovering over 1.5 s, is what turns the response into
a burst. The rule reads Yamada et al. 2024's paired flashes (a second flash 400 ms after the first evokes 0.38-0.68 of the
first EPSC) as one spike per flash; if a flash drives two or three spikes per Kenyon cell, as mbon11_kc_activity.md
estimates (1-3, up to 5), the same 0.62 leaves each spike 0.71 to 0.79 of the strength. And Yamada et al.'s flash EPSC
peaks about 100 ms after the flash and decays with a time constant of 256-333 ms (mbon11_kc_activity.md 2.1), where the
model's Kenyon cell-to-MBON11 current decays in 5 ms: either Kenyon cells fire for hundreds of milliseconds after a flash
or their transmission is slow, and either would carry MBON11's response through an odor. The next check is Yamada et
al.'s flash in the model.

    python experiments/mbon11_burst_check.py      (writes experiments/mbon11_burst_check.json)
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
import odor_probe24 as p24
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 640000                                          # learning_movie.py's, so the first condition repeats it
CHARGE_PC = 0.030 * 34.5 / 19.0
ODORS = {"3-octanol": 0, "4-methylcyclohexanol": 1}   # learning_pilot4.variant's odor index, for the seeds
CONDITIONS = {"as tested": (True, False), "not depressing": (False, False), "APL silenced": (True, True),
              "both": (False, True)}                   # (depressing, APL silenced)
WINDOWS = ((0.0, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.0))
SD_S = 0.05


def hold(o, rec, depressing: bool) -> dict:
    """learning_pilot4.variant's setup: the Kenyon cell-to-MBON11 synapses at CHARGE_PC per synapse, depressing or not, and
    MBON11 held near 6 Hz."""
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
    set_depressing(o, depressing)                      # where learning_pilot4.variant sets it, after the gain
    p = b.params[b.cls[kc[0]]]
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
    return {"kc": kc, "mbon": mbon, "per_kc": np.bincount(kc_of, weights=w0[onto], minlength=len(kc)),
            "f": float(p["depression"]), "recover_s": float(p["recovery"]), "gain": gain, "bias_step_mv": step}


def set_depressing(o, depressing: bool) -> None:
    full = o.brain.full_strength.copy()
    full[o.kc_mbon] = not depressing
    o.brain.full_strength = full


def trial(o, rec, odor: str, seed: int, h: dict, cls: dict, depressing: bool, silence) -> dict:
    """learning_pilot3.trial's protocol, recording per bin from -0.5 to 1.5 s."""
    b = o.brain
    kc, mbon, per_kc, f = h["kc"], h["mbon"], h["per_kc"], h["f"]
    apl = b.cells(["APL"])
    q = [int(np.flatnonzero(b.graded == i)[0]) for i in apl]
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=p24.spontaneous(rec), silence=silence)
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece = int(round(lp.BIN / b.dt))
    recover = h["recover_s"] / b.dt
    n_pre, n_odor = int(round(lp.PRE / lp.BIN)), int(round(1.0 / lp.BIN))
    keep = range(n_pre - 50, n_pre + 150)
    out = {"mbon_hz": [], "mbon_u": [], "apl_release": [], "kc_hz": {c: [] for c in cls}, "drive": {c: [] for c in cls}}
    first = np.zeros((b.u.shape[0], len(kc), len(WINDOWS)))
    for k in range(n_pre + 2 * n_odor):
        t = (k - n_pre) * lp.BIN
        if depressing:
            left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
        c = b.advance(piece, drive=rec.at(plan, t), silence=silence)
        if k not in keep:
            continue
        n = c[:, kc].astype(np.float64)
        d = left * (1.0 - f ** n) / (1.0 - f) if depressing else n
        out["mbon_hz"].append(float(c[:, mbon].mean()) / lp.BIN)
        out["mbon_u"].append(float(b.u[:, mbon].mean()))
        out["apl_release"].append(float(b.release[:, q].mean()))
        for name, mask in cls.items():
            out["kc_hz"][name].append(float(n[:, mask].mean()) / lp.BIN)
            out["drive"][name].append(float((d[:, mask] * per_kc[mask]).sum(1).mean()) / lp.BIN)
        for w, (a, z) in enumerate(WINDOWS):
            if a <= t + 1e-9 < z:
                first[:, :, w] += n
    out["answering"] = {name: [float(((first[:, mask, w] > 0).sum(1)).mean()) for w in range(len(WINDOWS))] for name, mask in cls.items()}
    return out


def smooth(v: np.ndarray, dt: float) -> np.ndarray:
    half = int(round(3 * SD_S / dt))
    k = np.exp(-0.5 * (np.arange(-half, half + 1) * dt / SD_S) ** 2)
    return np.convolve(np.pad(v, half, mode="edge"), k / k.sum(), mode="valid")


def summary(rs: list, cls: dict) -> dict:
    ts = -0.5 + (np.arange(200) + 0.5) * lp.BIN
    mean = lambda key: np.mean([r[key] for r in rs], 0)
    hz, sm = mean("mbon_hz"), smooth(mean("mbon_hz"), lp.BIN)
    rest = hz[ts < 0].mean()
    window = (ts > 0) & (ts < 1.4)
    evoked = hz[window] - rest
    drive = np.sum([np.mean([r["drive"][c] for r in rs], 0) for c in cls], 0)
    dsm = smooth(drive, lp.BIN)
    out = {"mbon11": {"rest_hz": round(float(rest), 2), "peak_hz": round(float(sm.max()), 1), "t_peak_s": round(float(ts[np.argmax(sm)]), 3),
                      "evoked_spikes": round(float(evoked.sum() * lp.BIN), 2),
                      "share_in_first_0.3s": round(float(evoked[ts[window] < 0.3].sum() / max(evoked.sum(), 1e-9)), 3),
                      "hz_0.5_to_1s": round(float(hz[(ts > 0.5) & (ts < 1.0)].mean()), 2),
                      "u_mv_rest": round(float(mean("mbon_u")[ts < 0].mean()), 2), "u_mv_0.5_to_1s": round(float(mean("mbon_u")[(ts > 0.5) & (ts < 1.0)].mean()), 2)},
           "drive": {"peak": round(float(dsm.max()), 2), "t_peak_s": round(float(ts[np.argmax(dsm)]), 3),
                     "rest": round(float(drive[ts < 0].mean()), 3),
                     "late_over_peak": round(float((drive[(ts > 0.6) & (ts < 1.0)].mean() - drive[ts < 0].mean()) / max(dsm.max() - drive[ts < 0].mean(), 1e-9)), 3),
                     "share_by_class": {c: round(float(np.mean([r["drive"][c] for r in rs], 0)[window].sum() / max(drive[window].sum(), 1e-12)), 3) for c in cls}},
           "kcs": {}, "apl_release": {"peak": round(float(mean("apl_release").max()), 2), "t_peak_s": round(float(ts[np.argmax(mean("apl_release"))]), 3),
                                      "0.5_to_1s": round(float(mean("apl_release")[(ts > 0.5) & (ts < 1.0)].mean()), 2)}}
    for c in cls:
        k = np.mean([r["kc_hz"][c] for r in rs], 0)
        early, late = k[(ts > 0) & (ts < 0.3)].mean(), k[(ts > 0.5) & (ts < 1.0)].mean()
        out["kcs"][c] = {"hz_per_cell_0_to_0.3s": round(float(early), 3), "hz_per_cell_0.5_to_1s": round(float(late), 3),
                         "late_over_early": round(float(late / max(early, 1e-9)), 3),
                         "answering_by_window": [round(float(x), 1) for x in np.mean([r["answering"][c] for r in rs], 0)]}
    return out


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "windows_s": WINDOWS, "bin_s": lp.BIN, "t0": -0.5,
           "conditions": {}}
    cls = {name: mask[np.flatnonzero(o.m["kc"])] for name, mask in mb_calibration.classes(o).items() if name != "other"}
    apl = o.brain.cells(["APL"])
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        h = hold(o, rec, True)
        out["held"] = {"bias_step_mv": round(h["bias_step_mv"], 2), "gain": h["gain"], "depression": h["f"], "recovery_s": h["recover_s"],
                       "mbon11_synapses_by_class": {c: round(float(h["per_kc"][m].sum() / h["per_kc"].sum()), 3) for c, m in cls.items()}}
        print("held", json.dumps(out["held"]), flush=True)
        for name, (depressing, silenced) in CONDITIONS.items():
            set_depressing(o, depressing)
            out["conditions"][name] = {}
            for odor, k in ODORS.items():
                rs = [trial(o, rec, odor, SEED + 10 * k + j, h, cls, depressing, apl if silenced else ()) for j in range(lp.SEEDS)]
                row = summary(rs, cls)
                row["series"] = {"mbon_hz": np.round(np.mean([r["mbon_hz"] for r in rs], 0), 2).tolist(),
                                 "mbon_u": np.round(np.mean([r["mbon_u"] for r in rs], 0), 3).tolist(),
                                 "apl_release": np.round(np.mean([r["apl_release"] for r in rs], 0), 3).tolist(),
                                 "kc_hz": {c: np.round(np.mean([r["kc_hz"][c] for r in rs], 0), 4).tolist() for c in cls},
                                 "drive": {c: np.round(np.mean([r["drive"][c] for r in rs], 0), 3).tolist() for c in cls}}
                out["conditions"][name][odor] = row
                print(name, odor, json.dumps({x: row[x] for x in ("mbon11", "drive", "kcs", "apl_release")}),
                      f"({time.perf_counter() - t0:.0f} s)", flush=True)
                OUT.write_text(json.dumps(out))
        set_depressing(o, True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
