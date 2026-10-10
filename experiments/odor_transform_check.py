"""Exploratory check, not pre-registered: is the model's weak-input deficit partly the transform's protocol?

odor_weak_input_check.py: the model's PNs answer weak receptor input at a third to three quarters of Olsen et al.
2010's fitted transform (DM4, DL5, VM7d; DM1 above it), and presynaptic inhibition isn't the cause. The model measures
its transform with a step: one glomerulus's receptor neurons jump to their spontaneous rate plus x for 0.5 s
(odor_probe24.drive_response). Flies' receptor neurons answer a private odor with a transient (latency, a rise over
about 30 ms, adaptation toward about half over 0.4 s; odor_probe10.py's time course), and Olsen et al. plotted the PNs'
500-ms mean against the receptor neurons' 500-ms mean; with depressing synapses PNs answer a change in rate more than a
held rate, and flies' weak-input PN responses are strongly transient (peak over mean about 2.5-6.9 for a weak private
odor, about 2 for a strong one; Olsen et al. Fig. 8C; research_notes/Rung 9 learning data/pn_ln_dynamics.md).
Model: odor_probe44.py's (its cache), with settled starts (warm.tracking).
Measured: for each of Olsen et al.'s four glomeruli and each receptor rate x (5-160 spikes/s, odor_probe16.RATES), the
PNs' mean rise over the 0.5 s (and over its first 100 ms, and its peak in 50 ms bins) with x given as a step
(odor_probe24.drive_response), and with x given as odor_probe10.py's time course (the fast rise, 25 ms latency) scaled so
that its mean over the 0.5 s is x; Olsen et al.'s function fitted to each. Seeds 470000 + 1000 x protocol + 10 x
glomerulus + rate index.

Ran: no. With the receptor neurons' time course the transform comes out as with the step: Rmax 78-179 and sigma 21-28
(the step: 81-186 and 20-31; flies 144-170 and 12-16, DM1 45); DL5's PNs rise 18, 42 and 75 spikes/s over the 0.5 s for
5, 10 and 20 spikes/s of receptor input (the step: 19, 42 and 79; Olsen et al.'s fit 36, 73 and 115). The responses'
peaks (50 ms bins) are 1.4-2.4 times their 0.5 s means at every input, with either protocol, where flies' are about 2
for strong private odors and 2.5-6.9 for weak ones (Olsen et al. Fig. 8C): flies' PNs answer weak input with a large
onset transient the model's don't. Set against other measurements the model's weak-input gain is less far off than
Olsen et al.'s fit suggests: near threshold, flies' PNs fire about three times their receptor neurons' rate (Jeanne &
Wilson 2015; the model about 4 times at 5-10 spikes/s), and receptor input under 20 spikes/s can drive PNs over 100
(Kazama & Wilson 2008; the model's peaks at 20 spikes/s are 107-135). Receptor convergence matches too (MaleCNS: 32-74
receptor neurons per glomerulus from both antennae for these four). What stays unexplained is the weak responses'
transience and the 0.5 s means at 10-40 spikes/s (a third to a half below Olsen et al.'s fit, partly the model's PNs
accommodating more than flies').

    python experiments/odor_transform_check.py      (writes experiments/odor_transform_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

import brain_cache
import odor_probe10 as p10
import odor_probe16 as p16
import odor_probe24 as p24
import odor_probe44 as p44
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 470000
LATENCY_S, WINDOW_S, BIN_S = 0.025, 0.5, 0.05


def shape(t: np.ndarray) -> np.ndarray:
    return p10.course(np.asarray(t) - LATENCY_S, p10.TAU_RISE["fast"])


def drive_course(o, rec, g: str, x: float, pns: np.ndarray, seed: int) -> dict:
    """odor_probe24.drive_response with glomerulus g's extra rate following the receptor time course, its mean over
    the window x."""
    b = o.brain
    base = p24.spontaneous(rec)
    grid = np.arange(0, WINDOW_S, p10.PIECE) + p10.PIECE / 2
    amp = x / float(np.mean(shape(grid)))
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=base)
    rest = float(b.advance(int(round(1.0 / b.dt)), drive=base)[:, pns].mean())
    piece = int(round(p10.PIECE / b.dt))
    counts = []
    for t in grid:
        extra = amp * float(shape(t))
        drive = [(rec.cells[h], rec.spont[h] + (extra if h == g else 0.0)) for h in rec.glomeruli if len(rec.cells[h])]
        counts.append(float(b.advance(piece, drive=drive)[:, pns].mean()))
    counts = np.array(counts) / p10.PIECE
    per = int(round(BIN_S / p10.PIECE))
    bins = counts.reshape(-1, per).mean(1)
    return {"whole": round(float(counts.mean() - rest), 2), "first_100ms": round(float(counts[:10].mean() - rest), 2),
            "peak_50ms": round(float(bins.max() - rest), 2), "rest": round(rest, 2)}


def drive_step(o, rec, g: str, x: float, pns: np.ndarray, seed: int) -> dict:
    """odor_probe24.drive_response, the step, with its peak in 50 ms bins as well."""
    b = o.brain
    base = p24.spontaneous(rec)
    driven = [(rec.cells[h], rec.spont[h] + (x if h == g else 0.0)) for h in rec.glomeruli if len(rec.cells[h])]
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=base)
    rest = float(b.advance(int(round(1.0 / b.dt)), drive=base)[:, pns].mean())
    bins = np.array([float(b.advance(int(round(BIN_S / b.dt)), drive=driven)[:, pns].mean()) / BIN_S for _ in range(10)])
    return {"whole": round(float(bins.mean() - rest), 2), "first_100ms": round(float(bins[:2].mean() - rest), 2),
            "peak_50ms": round(float(bins.max() - rest), 2), "rest": round(rest, 2)}


def fit(xs, ys) -> dict | None:
    try:
        (rmax, sigma), _ = curve_fit(p16.olsen, np.array(xs, float), np.array(ys, float), p0=(160.0, 15.0), maxfev=20000)
        return {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
    except RuntimeError:
        return None


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    types, m = o.types, o.m
    out = {"question": __doc__, "rates": list(p16.RATES), "protocols": {}}
    with warm.tracking(o, rec):
        for p, (name, run) in enumerate((("step", drive_step), ("receptor time course", drive_course))):
            rows = {}
            for gi, g in enumerate(p16.GLOMERULI):
                pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
                pts = {f"{x:g}": run(o, rec, g, x, pns, SEED + 1000 * p + 10 * gi + k) for k, x in enumerate(p16.RATES)}
                rows[g] = {"points": pts, "fit": fit(p16.RATES, [pts[f"{x:g}"]["whole"] for x in p16.RATES]),
                           "olsen": {"rmax": p16.OLSEN[g][0], "sigma": p16.OLSEN[g][1]}}
            out["protocols"][name] = rows
            print(name, json.dumps({g: rows[g]["fit"] for g in rows}),
                  json.dumps({g: [rows[g]["points"][f"{x:g}"]["whole"] for x in p16.RATES] for g in rows}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
