"""Exploratory, not pre-registered: if the receptor terminals' presynaptic inhibition is evoked by the local neurons'
activity above rest, with no tonic part, do the measured synapse and inhibition give flies' transform with the receptor
neurons firing spontaneously?

odor_probe24.py to odor_probe26.py: inhibition proportional to the GABAergic LNs' rate (or a power of it) always carries
a tonic part at rest, and to divide flies' EPSCs threefold during a lateral odor (Olsen & Wilson 2008) with the LNs
modulated only 2-3 times above rest, the fit drives that tonic part so high that the synapses are crushed at rest
(odor_probe25.py: resting divisor 14.5) or the fit fails (odor_probe24.py, odor_probe26.py). In flies there is little
tonic inhibition at least in VM7: GABA receptor antagonists "increase the gain in DM1 but not VM7" (Olsen et al. 2010).
Model: odor_probe24.py's (spontaneous receptor firing at each sensillum class's median rate; the receptor synapses at
their calibrated strength; depletion lowered with release; the resting state recalibrated) with the divisor
1 + k_A max(A_A - A_rest, 0) + k_B max(A_B - A_rest, 0): A_A the GABAergic antennal lobe LNs' summed rate low-passed over
50 ms (Nagel et al. 2015's alpha function of about 25 ms has that mean delay), A_B over 1 s (GABA-B's decay after an
odor, Olsen & Wilson 2008), each acting only above the LNs' resting rate A_rest. With no tonic inhibition, Kazama &
Wilson's 6.19 mV is the synapse's strength at rest however it is read (less its resting depression, which the
spontaneous firing now sets). k_A is fitted to Olsen & Wilson's GABA-B-blocked EPSCs and k_B then to their control
EPSCs, as in odor_probe21.py, iterated four times; the resting polish runs 20 rounds before and 6 after, each
followed by a polish of the uniglomerular PNs one by one (16 and 6 rounds of up to 3 mV), since with spontaneous input
some PNs fire from its fluctuations and the group polish's 1 mV steps barely move them.
Measured as odor_probe24.py measures. Seeds 210000 (otherwise as odor_probe24.py's, with its offsets; + 700-765 and
+ 800-855 for the PN polishes).

Ran: the resting state and the fit work, and the Kenyon cells become as sparse and odor-specific as flies', but the
projection neurons are now suppressed at an odor's onset and too narrowly tuned.
  rest       With no tonic inhibition the receptor synapses rest at 0.41 (fast) and 0.36 (slow) of full strength (Nagel et
             al.'s model without inhibition: 0.33), giving the PNs 40 mV of mean spontaneous input, whose fluctuations
             made them fire 61 Hz until the PN polish brought them to 1.8 Hz (median 1.4; flies 1-5). The LNs rest at 49
             spikes/s between them (0.55 each; flies 2.3-4.6).
  fit        k_A = 0.0055 and k_B = 0.0103 per spike/s above rest; EPSCs during the lateral odors at 0.23, 0.31, 0.36 and
             0.42 of baseline (flies 0.27, 0.32, 0.33, 0.37), with GABA-B blocked 0.47-0.91 (0.52-0.81).
  transform  Rmax 189, 307, 347 and 293 spikes/s for DM4, DL5, VM7d and DM1 (Olsen 170, 167, 163, 144) and sigma 39, 34,
             40 and 30 (16, 12, 12, 45): weak input is held back by the resting depression while strong input escapes.
             Lateral input abolishes the response (to -0.07-0.28; Olsen et al.'s fits imply roughly 0.3-0.9).
  odors      The inhibition is strongest right after the LNs' onset burst (synapses at 0.06-0.08 of their resting strength
             at 50 ms), so the PNs fall at onset and then climb (3-octanol: 37 Hz in the first 50 ms, 17-20 at 50-150 ms,
             91 by 500 ms): 32-73 Hz in the first 100 ms and 108-156 over 1 s (flies 100-200 at onset, then about half),
             and only 16-26% respond by Turner's criterion (flies 59 +- 14%). But different odors' PN patterns now
             correlate only 0.22 on average (0.48-0.52 in odor_probe21.py to odor_probe23.py), and the Kenyon cells
             respond as sparsely and specifically as flies': 1.0-4.5% per odor (flies 6 +- 5%), mean Jaccard 0.15 (flies'
             dissimilar odors share about 0.22), 6 cells answering all six odors, 45% of 4-methylcyclohexanol's responders
             also answering 3-octanol (78-94% before; Campbell et al.'s dissimilar odors 22%), responding alpha/beta cells
             firing 2.9 spikes (flies 2.2). The classes stay wrong (alpha'/beta' 0-1.3%, flies about 9-14%; alpha/beta
             1.3-8.8%, gamma 0.8-3.5%), and MBON11 gains 1.4-7.4 spikes and MBON-alpha2sc 3.9-17 (flies 110-118 and
             about 71-85). The resting brain runs at 1.09 Hz, nothing over 100 Hz.
Strong global normalization of the PNs decorrelates odors, as Olsen et al. 2010 argued it does in flies, and that alone
makes the Kenyon cells odor-specific; what it costs here, the PNs' onset and breadth, comes from the inhibition peaking
with the LNs' onset burst, where flies' takes about 100 ms to build (Nagel et al. 2015).

    python experiments/odor_probe27.py         (writes experiments/odor_probe27.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 210000
TAU_A, TAU_B = 0.05, 1.0
FIRST_POLISH = [1.0] * 12 + [0.5] * 8
SECOND_POLISH = [0.5] * 6


def apply(o: p7.Olfaction, mk: dict, base_w, base_sw, k_a: float, k_b: float, a_rest: float) -> None:
    """The weights as calibrated; the inhibition acting only above the LNs' resting rate; the receptor neurons'
    depletion following the gain."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=(TAU_A, TAU_B), k=(k_a, k_b),
                      start=a_rest, offset=a_rest, depleting=np.flatnonzero(o.m["orn"]))


def lateral_traces(o: p7.Olfaction, rec: p10.Receptors, seed: int) -> np.ndarray:
    """The two traces at Olsen & Wilson's sample times during each lateral odor, spontaneous firing running:
    (odors, times, 2)."""
    b = o.brain
    base = p24.spontaneous(rec)
    out = []
    for j, odor in enumerate(p21.LATERAL):
        b.reset(seed + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        b.advance(int(round(2.0 / b.dt)), drive=base)
        plan = rec.plan(odor, 2.0, p10.PEAK_HZ)
        drive, t, row = rec.at(plan, 0.0), 0.0, []
        for ts in p21.OLSEN_T:
            b.advance(int(round((ts - p21.VALVE_DELAY - t) / b.dt)), drive=drive)
            t = ts - p21.VALVE_DELAY
            a = b.presynaptic_state.mean(0)
            row.append((a[0], a[1]))
        out.append(row)
    return np.array(out)


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, dict]:
    """k_A from the GABA-B-blocked EPSCs, then k_B from the control ones, on the log divisor (1 at rest)."""
    da = np.maximum(e[..., 0].mean(0) - a_rest, 0.0)
    db = np.maximum(e[..., 1].mean(0) - a_rest, 0.0)
    cgp, ctl = -np.log(np.array(p21.OLSEN_CGP)), -np.log(np.array(p21.OLSEN_CONTROL))
    k_a = minimize_scalar(lambda x: ((np.log(1 + x * da) - cgp) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    k_b = minimize_scalar(lambda x: ((np.log(1 + k_a * da + x * db) - ctl) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    model = {"cgp_fraction": np.round(1 / (1 + k_a * da), 3).tolist(), "control_fraction": np.round(1 / (1 + k_a * da + k_b * db), 3).tolist(),
             "gaba_b_only_fraction": np.round(1 / (1 + k_b * db), 3).tolist(),
             "trace_a_over_rest": np.round(e[..., 0].mean(0) / a_rest, 2).tolist(), "trace_b_over_rest": np.round(e[..., 1].mean(0) / a_rest, 2).tolist()}
    return float(k_a), float(k_b), model


def calibrate(o, rec, mk, base_w, base_sw) -> dict:
    a_rest = p24.resting_inhibitors(o, rec, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):
        apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = fit(lateral_traces(o, rec, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    return {"k": [k_a, k_b], "offset_hz": round(a_rest, 1), "tau_s": [TAU_A, TAU_B], "inhibitors_rest_hz": round(a_rest, 1),
            "resting_divisor": 1.0, "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def course(o, rec, odor: str, seed: int, pns: np.ndarray, inhibitors: np.ndarray, k: np.ndarray, offset: float) -> dict:
    """odor_probe24.course with the strength relative to rest 1 / (1 + sum k max(A - offset, 0))."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    rest = b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    drive = rec.at(plan, 0.0)
    pn, inh, gain = [], [], []
    for _ in range(int(round(1.0 / p21.BIN))):
        c = b.advance(int(round(p21.BIN / b.dt)), drive=drive)
        pn.append(float(c[:, pns].mean() / p21.BIN))
        inh.append(float(c[:, inhibitors].sum(1).mean() / p21.BIN))
        a = np.maximum(b.presynaptic_state - offset, 0.0)
        gain.append(float((1.0 / (1.0 + (a * k).sum(1))).mean()))
    return {"bin_s": p21.BIN, "rest_pn_hz": round(float(rest[:, pns].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain]}


def pn_polish(o: p7.Olfaction, rec: p10.Receptors, seed: int, rounds: int = 16, step: float = 3.0, goal: float = 3.0) -> dict:
    """The uniglomerular PNs one by one toward rung 4's 3 Hz: each round, each PN's bias moves by step x the log ratio of
    goal to its resting rate (clipped to +-step mV); then the Kenyon cells' rest is set again. With spontaneous receptor
    input some PNs fire from its fluctuations, which the group polish's 1 mV steps barely move."""
    b, m = o.brain, o.m
    upn = np.flatnonzero(m["upn"])
    log = []
    for r in range(rounds):
        hz = p10.resting(o, rec, seed + r)["hz"]
        bias = o.own_bias()
        bias[upn] += np.clip(step * np.log((goal + 0.5) / (hz[upn] + 0.5)), -step, step)
        b.set_bias(bias)
        log.append({"round": r + 1, "upn_hz": round(float(hz[upn].mean()), 2), "upn_hz_median": round(float(np.median(hz[upn])), 2),
                    "upn_over_10hz": int((hz[upn] > 10).sum())})
        print("PN polish", json.dumps(log[-1]), flush=True)
    out = {"pn_polish": log}
    out.update(p24.polish(o, rec, seed + 50, []))          # the Kenyon cells' rest again
    return out


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = p24.SEED = SEED
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    out["spontaneous_hz"] = rec.spont
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 930)
    apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)             # no tonic inhibition: the resting gain is 1
    p10.POLISH, schedule = FIRST_POLISH, p10.POLISH
    try:
        out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0, SEED + 600)
    finally:
        p10.POLISH = schedule
    out["pn_rest"] = pn_polish(o, rec, SEED + 700)
    entry = {"presynaptic": calibrate(o, rec, mk, base_w, base_sw)}
    out["second_polish"] = p24.polish(o, rec, SEED + 640, SECOND_POLISH)
    out["pn_rest_after"] = pn_polish(o, rec, SEED + 800, rounds=6)
    k, offset = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["offset_hz"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = course(o, rec, odor, base + 700 + j, pns, mk["inhibitors"], k, offset)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = p24.transform(o, rec, base)
    entry.update(p24.odor_measures(o, rec, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
