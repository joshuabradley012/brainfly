"""Exploratory, not pre-registered: if the receptor terminals' GABA-B inhibition rises over tens of ms after the local
neurons fire, as flies' does, do the projection neurons accommodate?

odor_probe21.py: presynaptic inhibition fitted to Olsen & Wilson 2008's EPSC time courses divides each glomerulus's
response by the others' input (to 0.36-0.60) and halves the Kenyon cells' density, but the PNs still don't accommodate:
the LNs fire a burst at odor onset (as flies' do) and the model's GABA-B trace, a 1 s low-pass with no rise, takes that
burst in at once, so the synapses are at about a third of their resting strength within 50 ms and stay there. In flies
"the functional effects of inhibition peak ~100 ms later" than the LNs' spikes and "the main effect of blocking
inhibition on the PN odor response begins ~100 ms after the peak in LN spiking" (Nagel, Hong & Wilson 2015), and GABA-B's
inhibition rises within about 0.3 s (Olsen & Wilson 2008; research_notes/Rung 9 learning data/presynaptic_inhibition.md),
while PN responses peak about 150 ms after the valve opens and fall to about half by 500 ms (Bhandawat et al. 2007).
Model: odor_probe21.py's presynaptic condition with GABA-B's trace a difference of exponentials, decaying over 1 s and
rising with a 40 ms time constant, so that its response to a brief burst peaks 134 ms later; k_A and k_B fitted again to
Olsen & Wilson's EPSCs as in odor_probe21.py, and the inhibited synapses again multiplied by the resting divisor.
Measured as odor_probe21.py measures. Seeds 160000 (otherwise as odor_probe21.py's, with its offsets).

Ran: the rise changes almost nothing. The fit gives k_A = 0.00085 and k_B = 0.0092 per spike/s (a resting divisor of 2.7)
and fits Olsen & Wilson's EPSCs as well (control 0.31-0.33, GABA-B blocked 0.56-0.74). The PNs still climb (3-octanol:
151 Hz in the first 50 ms, 180 from 350 ms on; 4-methylcyclohexanol 108 to 131), since the synapses still fall to about a
third of their resting strength within 100 ms (0.31-0.34): the fast, GABA-A part, fitted where the LNs fire about 1,000
spikes/s between them, is several times stronger during their onset burst (5,300-6,500 spikes/s). Everything else
matches odor_probe21.py: Rmax 201, 307, 331 and 307, sigma 18, 12, 10 and 12, lateral input dividing to 0.41-0.64; PNs at
201-221 Hz in the first 100 ms and 211-244 over 1 s; 10-37% of Kenyon cells responding, mean Jaccard 0.40; MBON11 14-45
spikes, MBON-alpha2sc 19-73.

    python experiments/odor_probe22.py         (writes experiments/odor_probe22.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 160000
TAU_B_RISE = 0.040


def pairs() -> tuple[tuple, tuple]:
    """The traces' time constants, and each component's weights on them so that its steady state is k x the rate and
    its response to a spike starts from zero: ((tau...), (GABA-A weights, GABA-B weights))."""
    ca = p21.TAU_A / (p21.TAU_A - p21.TAU_A_RISE)
    cb = p21.TAU_B / (p21.TAU_B - TAU_B_RISE)
    taus = (p21.TAU_A, p21.TAU_A_RISE, p21.TAU_B, TAU_B_RISE)
    return taus, ((ca, -(ca - 1.0), 0.0, 0.0), (0.0, 0.0, cb, -(cb - 1.0)))


def apply(o: p7.Olfaction, mk: dict, base_w: np.ndarray, base_sw: np.ndarray, k_a: float, k_b: float, a_rest: float) -> tuple:
    """odor_probe21.apply with GABA-B's rising trace. Returns the resting divisor and the per-trace k."""
    b = o.brain
    d_rest = 1.0 + (k_a + k_b) * a_rest
    w = base_w.copy()
    w[mk["fast"]] *= d_rest
    b.weights, b._external_matrix = w, None
    b.slow_weights = base_sw.copy()
    b.slow_weights[mk["slow"]] *= d_rest
    taus, (wa, wb) = pairs()
    k = k_a * np.array(wa) + k_b * np.array(wb)
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=taus, k=k, start=a_rest)
    return d_rest, k


def lateral_traces(o: p7.Olfaction, seed: int) -> np.ndarray:
    """odor_probe21.lateral_traces with the GABA-B pair: (odors, times, 2) effective GABA-A and GABA-B rates."""
    b = o.brain
    _, (wa, wb) = pairs()
    out = []
    for j, odor in enumerate(p21.LATERAL):
        b.reset(seed + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        b.advance(int(round(2.0 / b.dt)))
        drive, t, row = odors.orn_drive(b, odor), 0.0, []
        for ts in p21.OLSEN_T:
            b.advance(int(round((ts - p21.VALVE_DELAY - t) / b.dt)), drive=drive)
            t = ts - p21.VALVE_DELAY
            a = b.presynaptic_state.mean(0)
            row.append((float(np.dot(wa, a)), float(np.dot(wb, a))))
        out.append(row)
    return np.array(out)


def calibrate(o: p7.Olfaction, mk: dict) -> dict:
    b = o.brain
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a_rest = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):
        apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = p21.fit(lateral_traces(o, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    d_rest, k = apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    taus, _ = pairs()
    return {"k": k.tolist(), "k_a": k_a, "k_b": k_b, "tau_s": list(taus), "inhibitors_rest_hz": round(a_rest, 1),
            "resting_divisor": round(d_rest, 3), "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = SEED                                  # build's and the measures' seeds follow this probe's
    o = p7.Olfaction()
    types, m = o.types, o.m
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    entry = {"presynaptic": calibrate(o, mk)}
    k, d_rest = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["resting_divisor"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = p21.course(o, odor, base + 700 + j, pns, mk["inhibitors"], k, d_rest)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = p17.transform(o, base)
    entry.update(p17.odor_measures(o, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
