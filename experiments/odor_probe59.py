"""Exploratory probe, not pre-registered: odor_probe56.py's model with presynaptic inhibition that grows with an odor's
total receptor input as flies' normalization does. Does 4-methylcyclohexanol then come closer to 3-octanol, at the
projection neurons and the Kenyon cells, with the transform and Olsen & Wilson's EPSCs kept?

odor_normalization_check.py: across sixteen odors the model's presynaptic divisor grows with the summed receptor input at
a log-log slope (of D - 1) of 0.64, where Olsen et al. 2010's normalization, written as a divisor, grows at 1.20: its
suppression rises as the 1.5 power of the odor's total input. Anchored at the strong odors where Olsen & Wilson 2008
measured the EPSCs (the model's fit), a flatter divisor over-suppresses weaker odors, and with the receptor input the
evidence supports, the model's projection neurons give 4-methylcyclohexanol's glomeruli 0.6-0.8 of what Olsen et al.'s
equation predicts and 3-octanol's strongest 0.8-1.3 (summed over glomeruli 0.39 against the equation's 0.66; scratch
analysis, 2026-10-11). The model's divisor is 1 + k_A max(A_A - A_rest, 0) + k_B max(A_B - A_rest, 0), A the LNs'
low-passed summed rate, which rises sublinearly with an odor's total input.
Model: odor_probe56.py's build with the inhibitors' rate above rest raised to the power 2 in both components (chosen
before the run from that slope gap: 1.3 / 0.64), the fit to Olsen & Wilson's EPSC fractions unchanged in form (k_A from
the CGP54626 fractions, then k_B from the control ones; four rounds), so the strong odors stay where the EPSCs put them
and weaker ones are divided less. The rest check raises the offset as before.
Measured as odor_probe57.py measures (odor_gaba_block_check.measure included), and odor_normalization_check.measure.
Seeds 790000.
Adopted as the base, by a rule set before the run, if the divisor's slope rises to 1.0 or more with Olsen & Wilson's
control fractions still fitted (each of the four within 0.05 of 0.27, 0.32, 0.33, 0.37) and the CGP54626 ones within 0.08;
each glomerulus's sigma within 2 of odor_probe56.py's or nearer flies', Rmax no lower than 0.85 of it, and 0.35-0.55 of the
peak left at 500 ms; the PNs resting at 4-6 spikes/s and the GABAergic LNs within 2x of their targets; blocking GABA at
rest raising the PNs' free potential within flies' 5-8 mV or within 1.5 mV of odor_probe56.py's 5.2; and the weighed
input's 4-methylcyclohexanol summed response over the Badel set larger against 3-octanol's than odor_probe56.py's 0.558.

Ran: not adopted, though the inhibition now scales like flies'. The divisor's slope against the summed input is 1.25
(Olsen et al.'s equation 1.20; odor_probe56.py 0.64): the strong odors are still divided by 2.0-2.6 and the weaker ones
now by 1.36-1.52 (1.8-2.0). The transform keeps its shape or steepens (sigma DM4 13.2, DL5 11.9, VM7d 14.7, DM1 10.3;
odor_probe56.py 13.5, 12.6, 15.4, 11.2; Rmax 86, 129, 131, 127), the PNs rest at 4.93 spikes/s and the GABAergic LNs at
3.67, and 4-methylcyclohexanol comes closer at the PNs: with DoOR's input 0.72 of 3-octanol (0.54), 1.03 over the Badel set
(0.85), 0.39 at the Kenyon cells (0.28); with the weighed input 0.33 (0.21), 0.635 over the Badel set (0.558), but still
0.17 at the Kenyon cells (0.16; responders 46 against 283 per fly). The rule fails three ways: Olsen & Wilson's control
fractions sit up to 0.08 off (0.35, 0.36, 0.33, 0.30 against 0.27, 0.32, 0.33, 0.37) and the CGP54626 ones up to 0.12, and
DM4 keeps 0.32 of its peak at 500 ms, though odor_probe56.py's own fit missed those thresholds too (0.075 and 0.10 off;
0.35); and blocking GABA at rest raises the PNs' free potential only 0.9 mV (flies 5-8). That last failure is the
informative one: odor_gaba_block_check.py (its parts, added afterwards) shows that half of odor_probe56.py's 5.2 mV came
from presynaptic inhibition at rest, the LNs' fluctuations above the offset dividing the receptor synapses by about 1.18
(their resting strength 0.85), which the power of 2 all but removes (0.99). odor_probe60.py keeps this scaling and makes
that resting division explicit.

    python experiments/odor_probe59.py      (writes experiments/odor_probe59.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

import brain_cache
import odor_normalization_check as nc
import odor_offset_check as oc
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe30 as p30
import odor_probe44 as p44
import odor_probe56 as p56
import odor_probe57 as p57

OUT = Path(__file__).with_suffix(".json")
SEED = 790000
POWER = 2.0
SCALE = {"a_rest": None}                         # the resting rate the fit's traces were normalized by


def apply(o, mk: dict, base_w, base_sw, k_a: float, k_b: float, a_rest: float) -> None:
    """odor_probe28.apply with the components acting on the inhibitors' rate above rest raised to POWER."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=p28.TAUS, k=(0.0, k_a, 0.0, k_b),
                      start=a_rest, offset=a_rest, power=POWER, source=p28.SOURCE, depleting=np.flatnonzero(o.m["orn"]))


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, dict]:
    """odor_probe27.fit with the traces' rise above rest, as a fraction of the resting rate, raised to POWER (k fitted in
    those units, then returned per (spikes/s)^POWER)."""
    da = (np.maximum(e[..., 0].mean(0) - a_rest, 0.0) / a_rest) ** POWER
    db = (np.maximum(e[..., 1].mean(0) - a_rest, 0.0) / a_rest) ** POWER
    cgp, ctl = -np.log(np.array(p21.OLSEN_CGP)), -np.log(np.array(p21.OLSEN_CONTROL))
    ka = minimize_scalar(lambda x: ((np.log(1 + x * da) - cgp) ** 2).sum(), bounds=(0.0, 1e4), method="bounded",
                         options={"xatol": 1e-6}).x
    kb = minimize_scalar(lambda x: ((np.log(1 + ka * da + x * db) - ctl) ** 2).sum(), bounds=(0.0, 1e4), method="bounded",
                         options={"xatol": 1e-6}).x
    model = {"cgp_fraction": np.round(1 / (1 + ka * da), 3).tolist(), "control_fraction": np.round(1 / (1 + ka * da + kb * db), 3).tolist(),
             "gaba_b_only_fraction": np.round(1 / (1 + kb * db), 3).tolist(), "k_per_rest_fraction": [round(float(ka), 4), round(float(kb), 4)],
             "trace_a_over_rest": np.round(e[..., 0].mean(0) / a_rest, 2).tolist(), "trace_b_over_rest": np.round(e[..., 1].mean(0) / a_rest, 2).tolist()}
    return float(ka / a_rest ** POWER), float(kb / a_rest ** POWER), model


def resting(o, rec, seed: int, inhibitors: np.ndarray, k, offset) -> dict:
    """odor_offset_check.resting with the gain from the installed inhibition (its powers included)."""
    b = o.brain
    plan = rec.plan(None, 0.0, 0.0)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    for _ in range(int(round(oc.SETTLE_S / p10.PIECE))):
        b.advance(piece, drive=rec.at(plan, -1.0))
    counts, traces, gains = 0, [], []
    for _ in range(int(round(oc.REST_S / p10.PIECE))):
        counts = counts + b.advance(piece, drive=rec.at(plan, -1.0))
        traces.append(np.asarray(b.presynaptic_state, np.float64).mean(0))
        gains.append(float(nc.gain(b).mean()))
    hz = counts.mean(0) / oc.REST_S
    return {"inhibitors_summed_hz": float(hz[inhibitors].sum()), "traces": np.mean(traces, 0), "gain": float(np.mean(gains)),
            "upn_hz": float(hz[o.m["upn"]].mean())}


def course(o, rec, odor: str, seed: int, pns: np.ndarray, inhibitors: np.ndarray, k, offset) -> dict:
    """odor_probe30.course with the gain from the installed inhibition (its powers included)."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    rest = b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    pn, inh, gain, orn = [], [], [], []
    t = 0.0
    piece = int(round(p10.PIECE / b.dt))
    for _ in range(int(round(1.0 / p21.BIN))):
        c = 0
        for _ in range(int(round(p21.BIN / p10.PIECE))):
            c = c + b.advance(piece, drive=rec.at(plan, t))
            t += p10.PIECE
        pn.append(float(c[:, pns].mean() / p21.BIN))
        inh.append(float(c[:, inhibitors].sum(1).mean() / p21.BIN))
        orn.append(float(c[:, o.m["orn"]].sum(1).mean() / p21.BIN))
        gain.append(float(nc.gain(b).mean()))
    return {"bin_s": p21.BIN, "rest_pn_hz": round(float(rest[:, pns].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain],
            "orn_summed_hz": [round(x, 1) for x in orn]}


def build():
    """odor_probe56.build with every installation of the presynaptic inhibition acting on the rate above rest to POWER."""
    saved = p28.apply, p27.fit, oc.resting
    p28.apply, p27.fit, oc.resting = apply, fit, resting
    try:
        o, rec, out = p56.build()
    finally:
        p28.apply, p27.fit, oc.resting = saved
    out["presynaptic"]["power"] = POWER
    return o, rec, out


def main() -> None:
    t0 = time.perf_counter()
    p57.OUT, p57.SEED = OUT, SEED
    p57.EQUALIZATION_SEED, p57.WEIGHED_SEED, p57.WEIGHED_EQUALIZATION_SEED = SEED + 1000, SEED + 2000, SEED + 3000
    loaded = brain_cache.load("odor_probe59", build, p44.prepare)
    load, plain_course = brain_cache.load, p30.course
    brain_cache.load, p30.course = (lambda *a, **k: loaded), course      # odor_probe57.main measures this model
    try:
        p57.main()
    finally:
        brain_cache.load, p30.course = load, plain_course
    out = json.loads(OUT.read_text())
    out.pop("resting_divisor", None)                                     # odor_probe57.py's, not this model's
    out["question"], out["power"] = __doc__, POWER
    out["normalization"] = nc.measure(loaded[0], loaded[1], SEED + 4000)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
