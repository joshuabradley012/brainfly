"""Exploratory check, not pre-registered: is warm.py's settled start settled?

warm.py starts every trial from the state 6 s of spontaneous activity leave after a reset. A reset leaves the receptor
synapses undepressed, and their slow component recovers over 33 s (odor_probe18.py: 0.9927 of it left per spike, 33.2 s
to recover), while the build sets the biases for its resting depression (odor_probe24.recalibrate_rest: 0.36 of full
strength at the receptor neurons' spontaneous rates). At 6-19 spikes/s that depression approaches rest with a time
constant of about 10-15 s (derived), so after 6 s it may still be well above it, and with it the PNs' input.
Model: odor_probe44.py's (its cache) with mb_calibration.py's calibration.
Measured: from a reset with warm.SEED, 60 s of spontaneous activity (8 flies), in 0.5 s bins: the mean rate of the
receptor neurons, the uniglomerular PNs, the GABAergic and the other ALLNs and the Kenyon cells; the receptor synapses'
mean fast and slow strength (the share of full strength the next spike would release) and the presynaptic inhibition's
traces; each one's value over 5.5-6 s against its mean over the last 10 s, and when it comes to stay within 3% of that.
Twice: from the reset as warm.py starts (synapses undepressed), and with the receptor neurons' synapses started at their
resting depression (rest_depression below: at spontaneous rate r, using (1 - f) g of what's left per spike and
recovering over tau, a synapse keeps 1 / (1 + r tau (1 - f) g) on average, g the resting presynaptic gain).

Ran: it isn't, for the receptor synapses' slow component, and the PNs' rest moves with it. From the reset the slow
component still keeps 0.80 of its strength at 6 s where it settles near 0.37 (within 3% of that only after 45 s); the
fast component keeps 0.43 (settled 0.41) and the presynaptic traces run 5-9% above their settled values. The PNs fire
3.1 spikes/s at 6 s and 2.05 once settled (1.5 times; their 2 s means within 5% of it only from 34 s), the GABAergic
ALLNs 3.75 and 3.47, the other ALLNs 2.0 and 1.8, the receptor neurons 8.46 throughout. So the build's polishes, measured
from 6 s settles, met the PNs' 3 spikes/s target in a state that drifts to 2 once settled, and every run since odor_probe44
has started with the slow component at twice its rest, draining during the run. Started at their resting depression
(fast 0.408, slow 0.361 computed; the resting presynaptic gain is 1, the traces resting below the offset), the synapses
stay there (slow 0.362-0.365 over the minute), and the PNs' and LNs' 2 s means are within 5% of their settled values from
2-2.5 s: the same settled state (PNs 2.04, GABAergic ALLNs 3.47) in about 2 s instead of a minute. A settle costs 2.2 s of
wall time per simulated second (8 flies, 8 threads).

    python experiments/settle_check.py      (writes experiments/settle_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import al_cells
import brain_cache
import mb_calibration
import odor_probe24 as p24
import odor_probe44 as p44
import warm

OUT = Path(__file__).with_suffix(".json")
SECONDS, BIN = 60.0, 0.5


def strengths(b, cells: np.ndarray) -> dict:
    """The mean share of full strength the cells' next spike would release, at their fast and slow synapses."""
    recovery = {"fast": np.array([b.params[c]["recovery"] for c in b.cls[cells]]),
                "slow": np.array([b.params[c]["slow_recovery"] or b.params[c]["recovery"] for c in b.cls[cells]])}
    out = {}
    for name, left, last in (("fast", b.left, b.last), ("slow", b.left_s, b.last_s)):
        if left.shape[1]:
            s = 1.0 - (1.0 - left[:, cells]) * np.exp(-(b.t - last[:, cells]) / (recovery[name] / b.dt))
            out[name] = float(s.mean())
    return out


def resting_gain(b) -> float:
    """The presynaptic gain with every trace at its resting start (1 without presynaptic inhibition)."""
    pres = b._presynaptic
    if pres is None:
        return 1.0
    a = np.maximum(np.asarray(pres["start"], float) - pres["offset"], 0.0)
    return float(1.0 / (1.0 + np.sum(pres["k"] * a ** pres["power"])))


def rest_depression(o, rec) -> dict:
    """The receptor neurons' fast and slow synapses set to their mean depression at their spontaneous rates."""
    b = o.brain
    rate = np.zeros(b.n)
    for g, cells in rec.cells.items():
        rate[cells] = rec.spont[g]
    gain = np.ones(b.n)
    if b._presynaptic is not None:
        gain[b._presynaptic["depleting"]] = resting_gain(b)
    cells = np.flatnonzero(rate > 0)
    out = {"resting_gain": round(resting_gain(b), 4)}
    for c in np.unique(b.cls[cells]):
        sel = cells[b.cls[cells] == c]
        p = b.params[c]
        for name, f, tau in (("fast", p["depression"], p["recovery"]),
                             ("slow", p["slow_depression"], p["slow_recovery"] or p["recovery"])):
            left, last = (b.left, b.last) if name == "fast" else (b.left_s, b.last_s)
            if left.shape[1] and 0 < f < 1:
                strength = 1.0 / (1.0 + rate[sel] * tau * (1 - f) * gain[sel])
                left[:, sel], last[:, sel] = strength, b.t
                out[name] = round(float(strength.mean()), 4)
    return out


def settles(series: list, final: float, tol: float = 0.03) -> float | None:
    """The time (s, at a bin's end) from which every bin stays within tol of final."""
    x = np.asarray(series, float)
    off = np.abs(x - final) > tol * abs(final)
    if not off.any():
        return BIN
    last = int(np.flatnonzero(off)[-1])
    return None if last == len(x) - 1 else round((last + 2) * BIN, 2)


def run(o, rec, idx: dict, rested: bool) -> tuple:
    """60 s of spontaneous activity from a reset: the series, and what rest_depression set (if rested)."""
    b = o.brain
    b.reset(warm.SEED)
    b.set_release(o.s.ol.neurons, o.s.silent)
    start = rest_depression(o, rec) if rested else None
    drive = p24.spontaneous(rec)
    steps = int(round(BIN / b.dt))
    series = {k: [] for k in idx}
    series.update({"strength_fast": [], "strength_slow": []})
    traces = []
    t1 = time.perf_counter()
    for _ in range(int(round(SECONDS / BIN))):
        c = b.advance(steps, drive=drive)
        for name, i in idx.items():
            series[name].append(round(float(c[:, i].mean() / BIN), 4))
        for name, v in strengths(b, idx["ORN"]).items():
            series[f"strength_{name}"].append(round(v, 4))
        traces.append(np.asarray(b.presynaptic_state, float).mean(0))
    wall = time.perf_counter() - t1
    traces = np.array(traces)
    for k in range(traces.shape[1]):
        series[f"presynaptic_trace_{k}"] = traces[:, k].round(4).tolist()
    return series, start, wall


def summarize(series: dict) -> dict:
    n6, last = int(round(6.0 / BIN)), int(round(10.0 / BIN))
    out = {}
    for name, x in series.items():
        if x:
            final, at6 = float(np.mean(x[-last:])), float(x[n6 - 1])
            out[name] = {"at_6s": round(at6, 4), "last_10s": round(final, 4),
                         "at_6s_over_last": round(at6 / final, 3) if final else None,
                         "within_3pct_from_s": settles(x, final)}
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe44", p44.build, p44.prepare)
    mb_calibration.apply(o)
    m = o.m
    gaba = al_cells.transmitter(o, "gaba")
    pops = {"ORN": m["orn"], "uPN": m["upn"], "GABA ALLN": gaba, "other ALLN": al_cells.alln(o) & ~gaba, "KC": m["kc"]}
    idx = {k: np.flatnonzero(v) for k, v in pops.items()}
    out = {"question": __doc__, "bin_s": BIN, "trials": int(o.brain.trials), "conditions": {}}
    for name, rested in (("from reset", False), ("resting depression", True)):
        series, start, wall = run(o, rec, idx, rested)
        summary = summarize(series)
        out["conditions"][name] = {"started_at": start, "summary": summary, "series": series,
                                   "wall_s_per_simulated_s": round(wall / SECONDS, 2)}
        print(name, json.dumps(start), flush=True)
        for k, v in summary.items():
            print(" ", k, json.dumps(v), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
