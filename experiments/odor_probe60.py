"""Exploratory probe, not pre-registered: odor_probe59.py's presynaptic inhibition, which scales with an odor's total
input as flies' normalization does, with the resting division odor_probe56.py's model had made explicit. Does the
antennal lobe then disinhibit at rest like flies' and keep 4-methylcyclohexanol's gain?

odor_probe59.py: squaring the inhibitors' rate above rest gives the divisor flies' scaling (slope 1.25 against Olsen et
al.'s 1.20), keeps the transform, and brings 4-methylcyclohexanol closer to 3-octanol at the projection neurons, but
blocking GABA at rest then raises the PNs only 0.9 mV (flies 5-8). odor_gaba_block_check.py's parts: half of
odor_probe56.py's 5.2 mV came from presynaptic inhibition at rest, the LNs' fluctuations above the offset dividing the
receptor synapses by about 1.18 (resting strength 0.849, odor_probe42.rest_check), which the square removes. Kazama &
Wilson 2008's DM4 comparison allows a resting divisor up to 1.55 at one standard error with this synapse
(research_notes/Rung 9 learning data/orn_pn_resting_state.md).
Model: odor_probe59.py's build with odor_probe57.py's tonic trace (the GABA-A trace again, acting from zero, linear,
k_t = (D - 1) / the inhibitors' summed target rate) at D = 1 / 0.849 = 1.178, installed from the first resting
calibration (which estimates resting input at the installed gain); the evoked part fitted to Olsen & Wilson's EPSCs
relative to the resting divisor, with CGP54626 leaving the tonic term (as odor_probe57.py).
Measured as odor_probe59.py measures. Seeds 800000.
Adopted as the base, by a rule set before the run, if the divisor's slope against the summed input stays 1.0 or more;
blocking GABA raises the PNs' free potential within flies' 5-8 mV or within 1.5 mV of odor_probe56.py's 5.2; Olsen &
Wilson's control and CGP54626 fractions are fitted no worse than odor_probe56.py's by more than 0.03 (its largest misses
0.075 and 0.10); each glomerulus's sigma within 2 of odor_probe56.py's or nearer flies', Rmax no lower than 0.85 of it, and
a share of the peak left at 500 ms of 0.55 or less and no more than 0.05 below odor_probe56.py's; the PNs resting at 4-6
spikes/s and the GABAergic LNs within 2x of their targets; and the weighed input's 4-methylcyclohexanol summed response
over the Badel set larger against 3-octanol's than odor_probe56.py's 0.558.

Ran: adopted; the base model from here on. Every part of the rule holds. The divisor grows with the summed input at a
slope of 1.04 (odor_probe56.py 0.64; Olsen et al.'s equation 1.20): the strong odors divided by 2.2-2.8 as before, the
weaker ones by 1.5-1.6 (1.8-2.0). Blocking GABA at rest raises the PNs' free potential 4.9 mV in DM6, VM2 and VM7 (5.2;
flies 5-8): 2.9 from turning the presynaptic inhibition off alone, as in odor_probe56.py, now from the explicit resting
division (resting strength 0.852; divisor 1.165 at the traces' start) instead of the LNs' fluctuations. Olsen & Wilson's
control fractions are 0.37, 0.36, 0.33, 0.29 (0.27, 0.32, 0.33, 0.37) and the CGP54626 ones 0.50, 0.76, 0.80, 0.76 (0.52,
0.68, 0.77, 0.81), largest misses 0.10 and 0.08 (odor_probe56.py 0.075 and 0.10). The transform barely moves: sigma DM4
14.0, DL5 12.4, VM7d 15.0, DM1 11.0 (13.5, 12.6, 15.4, 11.2), Rmax 90.5, 135, 139, 132 (90, 136, 141, 132), 0.34-0.42 of the
peak left at 500 ms; the PNs rest at 4.75 spikes/s and the GABAergic LNs at 3.64. 4-methylcyclohexanol gains at the PNs
and less after: with DoOR's input 0.73 of 3-octanol (0.54), 1.02 over the Badel set (0.85; flies 0.98), 0.35 at the Kenyon
cells (0.28), MBON11 18.8 and 44.2 spikes (13.7 and 42); with the weighed input 0.30 (0.21), 0.609 over the Badel set
(0.558), 0.19 at the Kenyon cells (0.16; responders 50 against 299 per fly). The resting drive stays where it was (by
the free potential 28.9 mV in DM6, VM2 and VM7 with every receptor neuron silenced), the synapse's problem
(odor_probe58.py). Next: the Kenyon cells, where APL saturates for both odors (odor_apl_check.py).

Correction (2026-10-11, from an independent review, checked): the weaker odors are divided by 1.52-1.70, not 1.5-1.6.

    python experiments/odor_probe60.py      (writes experiments/odor_probe60.json)
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
import odor_probe21 as p21
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe30 as p30
import odor_probe44 as p44
import odor_probe51 as p51
import odor_probe56 as p56
import odor_probe57 as p57
import odor_probe59 as p59
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 800000
RESTING_DIVISOR = 1.0 / 0.849
POWER = p59.POWER
TONIC = {"k_t": None}


def tonic_k(o, mk: dict) -> float:
    return (RESTING_DIVISOR - 1.0) / float(o.s.target[mk["inhibitors"]].sum())


def apply(o, mk: dict, base_w, base_sw, k_a: float, k_b: float, a_rest: float) -> None:
    """odor_probe59.apply with odor_probe57.py's tonic trace (linear, from zero) at RESTING_DIVISOR."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    TONIC["k_t"] = k_t = tonic_k(o, mk)
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=p57.TAUS, k=(0.0, k_a, 0.0, k_b, k_t),
                      start=a_rest, offset=(a_rest,) * 4 + (0.0,), power=(POWER,) * 4 + (1.0,), source=p57.SOURCE,
                      depleting=np.flatnonzero(o.m["orn"]))


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, dict]:
    """odor_probe59.fit relative to the resting divisor 1 + k_t a_rest, the tonic term following the GABA-A trace and left
    in place by CGP54626 (as odor_probe57.fit)."""
    k_t = TONIC["k_t"]
    tonic = k_t * e[..., 0].mean(0)
    d0 = 1.0 + k_t * a_rest
    da = (np.maximum(e[..., 0].mean(0) - a_rest, 0.0) / a_rest) ** POWER
    db = (np.maximum(e[..., 1].mean(0) - a_rest, 0.0) / a_rest) ** POWER
    cgp, ctl = -np.log(np.array(p21.OLSEN_CGP)), -np.log(np.array(p21.OLSEN_CONTROL))
    ka = minimize_scalar(lambda x: ((np.log((1 + tonic + x * da) / d0) - cgp) ** 2).sum(), bounds=(0.0, 1e4), method="bounded",
                         options={"xatol": 1e-6}).x
    kb = minimize_scalar(lambda x: ((np.log((1 + tonic + ka * da + x * db) / d0) - ctl) ** 2).sum(), bounds=(0.0, 1e4),
                         method="bounded", options={"xatol": 1e-6}).x
    model = {"cgp_fraction": np.round(d0 / (1 + tonic + ka * da), 3).tolist(),
             "control_fraction": np.round(d0 / (1 + tonic + ka * da + kb * db), 3).tolist(),
             "tonic_only_fraction": np.round(d0 / (1 + tonic), 3).tolist(), "k_per_rest_fraction": [round(float(ka), 4), round(float(kb), 4)],
             "trace_a_over_rest": np.round(e[..., 0].mean(0) / a_rest, 2).tolist(), "trace_b_over_rest": np.round(e[..., 1].mean(0) / a_rest, 2).tolist()}
    return float(ka / a_rest ** POWER), float(kb / a_rest ** POWER), model


def build():
    """odor_probe56.build with every installation carrying the squared evoked terms and the tonic trace, and the first
    resting calibration at the installed gain."""
    saved = p28.apply, p27.fit, oc.resting, p51.recalibrate_rest
    p28.apply, p27.fit, oc.resting, p51.recalibrate_rest = apply, fit, p59.resting, p57.recalibrate_rest
    try:
        o, rec, out = p56.build()
    finally:
        p28.apply, p27.fit, oc.resting, p51.recalibrate_rest = saved
    pres = o.brain._presynaptic
    out["presynaptic"]["power"] = [float(x) for x in pres["power"]]
    out["presynaptic"]["tonic"] = {"k_t": round(float(pres["k"][4]), 8), "resting_divisor_at_start": round(1.0 / warm.resting_gain(o.brain), 3),
                                   "inhibitors_target_hz": round(float(o.s.target[p21.masks(o)["inhibitors"]].sum()), 1)}
    out["presynaptic"]["k"] = [float(x) for x in pres["k"]]
    out["presynaptic"]["offset_hz"] = [float(x) for x in pres["offset"]]
    return o, rec, out


def main() -> None:
    t0 = time.perf_counter()
    p57.OUT, p57.SEED = OUT, SEED
    p57.EQUALIZATION_SEED, p57.WEIGHED_SEED, p57.WEIGHED_EQUALIZATION_SEED = SEED + 1000, SEED + 2000, SEED + 3000
    loaded = brain_cache.load("odor_probe60", build, p44.prepare)
    load, plain_course = brain_cache.load, p30.course
    brain_cache.load, p30.course = (lambda *a, **k: loaded), p59.course
    try:
        p57.main()
    finally:
        brain_cache.load, p30.course = load, plain_course
    out = json.loads(OUT.read_text())
    out.pop("resting_divisor", None)
    out["question"], out["power"], out["resting_divisor"] = __doc__, POWER, round(RESTING_DIVISOR, 4)
    out["normalization"] = nc.measure(loaded[0], loaded[1], SEED + 4000)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
