"""Exploratory, not pre-registered: if the receptor terminals' GABA-B inhibition grows faster than linearly with the local
neurons' activity, can measured presynaptic inhibition work with the receptor neurons firing spontaneously, as flies'
do, and does the antennal lobe then transform receptor input as flies' does?

odor_probe24.py: with spontaneous receptor firing the synapses rest as flies' do (0.66 and 0.62 of full strength), but a
lateral odor raises the GABAergic LNs' rate only 2-3 times above rest, so inhibition linear in that rate can't divide
the synapses threefold, as flies' EPSCs fall (Olsen & Wilson 2008); flies' LNs are modulated no more (sustained odor
rates about 1.5 times their resting rate). Wilson & Laurent 2005: GABA-B inhibition "is known to depend strongly on the
number of presynaptic action potentials" (in mammals it needs transmitter pooled from many release sites).
odor_probe25.py (the weights uninhibited, no spontaneous firing): flies' Rmax but three times their sigma.
Model: odor_probe24.py's (spontaneous receptor firing at each sensillum class's median rate; the receptor synapses at
their calibrated, uninhibited strength, divided in vivo by the presynaptic divisor; depletion lowered with release; the
resting state recalibrated) with the divisor 1 + k_A A_A + k_B A_B^n: A_A the GABAergic antennal lobe LNs' summed rate
through GABA-A's difference of 40 and 15 ms exponentials, linear; A_B the same rate low-passed over 1 s (GABA-B's decay
after an odor, Olsen & Wilson 2008), raised to a power n. k_A is fitted to Olsen & Wilson's GABA-B-blocked EPSCs as
before; then the GABA-B divisor at rest, k_B A_rest^n, and n are fitted together to their control EPSCs (least squares on
the log divisor relative to rest at their four sample times, n from 1 to 4), iterated four times. The resting polish runs
longer than odor_probe24.py's (20 rounds, then 10 more after the fit), since easing the LNs toward their targets also
eases the tonic inhibition of the receptor terminals.
Measured as odor_probe24.py measures. Seeds 200000 (otherwise as odor_probe24.py's, with its offsets).

Ran (stopped at the calibration, by design, when the fit degenerated): a power doesn't rescue the fit. At rest the
synapses carry 0.70 (fast) and 0.66 (slow) of full strength and the PNs get 21 mV of mean spontaneous input; after the
20-round polish they rest at 12.4 Hz (flies 1-5). In the first round the fit reproduces flies' control EPSCs (0.25,
0.30, 0.35 and 0.41 of baseline, against 0.27, 0.32, 0.33 and 0.37) with n = 1.4, but only through a GABA-B divisor at
rest of 48 (its bound is 50): the LNs' 1 s trace sinks from 2.8 to 1.95 times its resting value over the second while
flies' suppression holds, a power steepens that decline, and so the fit again buys the late suppression with tonic
inhibition. Applied, that divisor also cuts the receptor neurons' synapses onto the LNs, whose odor responses vanish
(their traces at 0.03-1.3 times rest), and the second round's fit degenerates (n = 4, the divisor 0.17, the EPSCs left
at 0.78-1.13). Flies have little tonic inhibition at least in VM7 (GABA antagonists don't change its gain; Olsen et al.
2010), which points to inhibition evoked above rest (odor_probe27.py).

    python experiments/odor_probe26.py         (writes experiments/odor_probe26.json)
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
SEED = 200000
FIRST_POLISH = [1.0] * 12 + [0.5] * 8
SECOND_POLISH = [1.0] * 4 + [0.5] * 6
POWERS = np.round(np.arange(1.0, 4.001, 0.05), 2)


def traces_k(k_a: float, k_b: float) -> tuple[tuple, np.ndarray]:
    c = p21.TAU_A / (p21.TAU_A - p21.TAU_A_RISE)
    return (p21.TAU_A, p21.TAU_A_RISE, p21.TAU_B), np.array([c * k_a, -(c - 1.0) * k_a, k_b])


def apply(o: p7.Olfaction, mk: dict, base_w, base_sw, k_a: float, k_b: float, n: float, a_rest: float) -> float:
    """The weights as calibrated, the inhibition with GABA-B's trace raised to n, the receptor neurons' depletion
    following the gain. Returns the resting divisor."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    taus, k = traces_k(k_a, k_b)
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=taus, k=k, start=a_rest,
                      depleting=np.flatnonzero(o.m["orn"]), power=(1.0, 1.0, n))
    return 1.0 + k_a * a_rest + k_b * a_rest ** n


def lateral_traces(o: p7.Olfaction, rec: p10.Receptors, seed: int) -> np.ndarray:
    """odor_probe24.lateral_traces for this probe's traces: (odors, times, 2) the effective GABA-A rate and GABA-B's rate."""
    b = o.brain
    c = p21.TAU_A / (p21.TAU_A - p21.TAU_A_RISE)
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
            row.append((c * a[0] - (c - 1.0) * a[1], a[2]))
        out.append(row)
    return np.array(out)


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, float, dict]:
    """k_A from the GABA-B-blocked EPSCs (linear, as odor_probe21.fit); then, for each n, the GABA-B divisor at rest
    d_B = k_B A_rest^n from the control EPSCs, keeping the n that fits best."""
    ea, eb = e[..., 0].mean(0), e[..., 1].mean(0)
    cgp, ctl = -np.log(np.array(p21.OLSEN_CGP)), -np.log(np.array(p21.OLSEN_CONTROL))
    rel_a = lambda ka: np.log((1 + ka * ea) / (1 + ka * a_rest))
    k_a = minimize_scalar(lambda x: ((rel_a(x) - cgp) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    best = None
    for n in POWERS:
        rel = lambda d: np.log((1 + k_a * ea + d * (eb / a_rest) ** n) / (1 + k_a * a_rest + d))
        r = minimize_scalar(lambda d: ((rel(d) - ctl) ** 2).sum(), bounds=(0.0, 50.0), method="bounded")
        if best is None or r.fun < best[2]:
            best = (float(n), float(r.x), float(r.fun))
    n, d_b, sse = best
    k_b = d_b / a_rest ** n
    rel = np.log((1 + k_a * ea + d_b * (eb / a_rest) ** n) / (1 + k_a * a_rest + d_b))
    model = {"n": n, "gaba_b_divisor_at_rest": round(d_b, 3), "sse": round(sse, 5),
             "cgp_fraction": np.round(np.exp(-rel_a(k_a)), 3).tolist(), "control_fraction": np.round(np.exp(-rel), 3).tolist(),
             "gaba_b_only_fraction": np.round((1 + d_b) / (1 + d_b * (eb / a_rest) ** n), 3).tolist(),
             "trace_a_over_rest": np.round(ea / a_rest, 2).tolist(), "trace_b_over_rest": np.round(eb / a_rest, 2).tolist()}
    return float(k_a), float(k_b), n, model


def calibrate(o, rec, mk, base_w, base_sw, k_a, k_b, n) -> dict:
    a_rest = p24.resting_inhibitors(o, rec, mk["inhibitors"], SEED + 940)
    rounds = []
    for r in range(4):
        apply(o, mk, base_w, base_sw, k_a, k_b, n, a_rest)
        k_a, k_b, n, model = fit(lateral_traces(o, rec, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": float(f"{k_b:.4g}"), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
        if model["sse"] > 0.5 or model["gaba_b_divisor_at_rest"] > 49.9:     # degenerate or at the fit's bound
            return {"failed": "the fit degenerated or reached its bound", "inhibitors_rest_hz": round(a_rest, 1),
                    "calibration": rounds, "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL,
                                                     "cgp_fraction": p21.OLSEN_CGP}}
    d_rest = apply(o, mk, base_w, base_sw, k_a, k_b, n, a_rest)
    taus, k = traces_k(k_a, k_b)
    return {"k": k.tolist(), "power": [1.0, 1.0, n], "k_a": k_a, "k_b": k_b, "n": n, "tau_s": list(taus),
            "inhibitors_rest_hz": round(a_rest, 1), "resting_divisor": round(d_rest, 3), "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def course(o, rec, odor: str, seed: int, pns: np.ndarray, inhibitors: np.ndarray, k: np.ndarray, power: np.ndarray, d_rest: float) -> dict:
    """odor_probe24.course with the traces' powers in the strength relative to rest."""
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
        a = np.maximum(b.presynaptic_state, 0.0)
        gain.append(float((d_rest / (1.0 + (k * a ** power).sum(1))).mean()))
    return {"bin_s": p21.BIN, "rest_pn_hz": round(float(rest[:, pns].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain]}


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
    # the resting recalibration with odor_probe22.py's linear strengths as a start, then the fit, then more polish
    k_a0, k_b0, n0 = 0.000851, 0.009247, 1.0
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 930)
    d0 = apply(o, mk, base_w, base_sw, k_a0, k_b0, n0, a0)
    p10.POLISH, schedule = FIRST_POLISH, p10.POLISH        # recalibrate_rest polishes with p10.POLISH
    try:
        out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0 / d0, SEED + 600)
    finally:
        p10.POLISH = schedule
    entry = {"presynaptic": calibrate(o, rec, mk, base_w, base_sw, k_a0, k_b0, n0)}
    if "failed" in entry["presynaptic"]:
        out["condition"], out["seconds"] = entry, round(time.perf_counter() - t0)
        OUT.write_text(json.dumps(out, indent=1))
        print("stopped:", entry["presynaptic"]["failed"], flush=True)
        return
    out["second_polish"] = p24.polish(o, rec, SEED + 640, SECOND_POLISH)
    k, power = np.asarray(entry["presynaptic"]["k"]), np.asarray(entry["presynaptic"]["power"])
    d_rest = entry["presynaptic"]["resting_divisor"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = course(o, rec, odor, base + 700 + j, pns, mk["inhibitors"], k, power, d_rest)
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
