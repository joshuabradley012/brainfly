"""Does the brain that passed rung 1 carry the optomotor signal? flyvis driving HybridBrain, open loop.

optomotor.py showed a rotating drum reaching the steering neuron DNa02 through FlyvisNative and
FlyBrain, the inherited model, and closed_loop.py turned the body with it. FlyBrain isn't validated.
This asks whether the same signal survives in HybridBrain as it passed rung 1 (shiu_rewiring.py),
with no change made for vision.

Setup: HybridBrain with shiu_sensory.py's network exactly, at w_syn = 1.5556 mV. FlyvisNative (model
0000/000) is stepped every 2 ms and sets the release of its 69,917 MaleCNS neurons through
set_release, in Hz: 50 x its output per 20 ms, times the gain G. Every other neuron, including the
optic lobe types flyvis doesn't model, the HS cells and the descending neurons, is a spiking Shiu
neuron. The network has no noise and no Poisson drive, so one run per scene says everything (there
are no flies to average over). The fly doesn't move.
Scenes as in optomotor.py, 2 s each, rates from 0.5 to 2 s:
  blank   grey
  static  a vertical sine grating, period 30 deg, contrast 1
  ccw     the grating rotating counterclockwise at 40 deg/s, then 0.5 s of grey
  cw      clockwise at 40 deg/s, then 0.5 s of grey
Knob: G in {1, 3, 10, 30, 100}.
Pass criteria, fixed before the first run, all at one G:
  STABLE  under ccw and under cw: at most 20 neurons that flyvis doesn't drive pass 100 Hz, and in
          the last 0.25 s of the grey after the drum, those neurons fire under 1% as much as
          during it
  HS      (HS left - HS right) is at least 3 Hz higher under ccw than under cw, HS being the mean
          rate of HSN, HSE and HSS on that side
  STEER   (DNa02 left - DNa02 right) is at least 2 Hz higher under ccw than under cw
The lowest passing G is the result. It must then pass HS and STEER on a held-out drum (period 20 deg,
60 deg/s), and NULL: in 10 degree-preserving rewirings of the network (brainfly.nulls; flyvis
unchanged, and the rewiring moves flyvis's outputs too), STEER holds in at most 1.
Reported: every rate above for each G; DNa01's signal; H2's and each descending type's direction
signal ((left - right) under ccw minus under cw), ranked, at the passing G.

    python experiments/optomotor_hybrid.py            (writes experiments/optomotor_hybrid.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import nulls
from brainfly.data import DATA
from brainfly.eye2d import Grating
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.optic import MODEL, FlyvisNative
from brainfly.shiu import counts, mcns_types
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

OUT = Path(__file__).with_name("optomotor_hybrid.json")
GAINS = [1.0, 3.0, 10.0, 30.0, 100.0]
SECONDS, WARM, TAIL = 2.0, 0.5, 0.5
OPTIC_DT = 0.002
HS = ["HSN", "HSE", "HSS"]


def scenes(period: float, speed: float) -> dict:
    return {"blank": lambda t: [], "static": lambda t: [Grating(period, 0.0)],
            "ccw": lambda t: [Grating(period, speed * t)], "cw": lambda t: [Grating(period, -speed * t)]}


def measure(brain: HybridBrain, ol: FlyvisNative, scene, tail: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rates per neuron over WARM..SECONDS, the undriven network's spikes per 2 ms over the stimulus
    window, and over the last 0.25 s of `tail` seconds of grey that follow."""
    brain.reset()
    ol.reset()
    per = int(round(OPTIC_DT / brain.dt))
    n_on, n_tail = int(round(SECONDS / OPTIC_DT)), int(round(tail / OPTIC_DT))
    spikes = np.zeros(brain.n)
    during, late = [], []
    own = ~brain.external
    for k in range(n_on + n_tail):
        t = k * OPTIC_DT
        release = ol.step(ol.contrast(scene(t) if k < n_on else []))
        brain.set_release(ol.neurons, 50.0 * release)
        c = brain.advance(per)[0]
        if WARM <= t < SECONDS:
            spikes += c
            during.append(int(c[own].sum()))
        if k >= n_on + n_tail - int(round(0.25 / OPTIC_DT)):
            late.append(int(c[own].sum()))
    return spikes / (SECONDS - WARM), np.array(during), np.array(late)


def signals(rates: dict, cells: dict) -> dict:
    """Per scene: HS and DNa02/DNa01 rates per side."""
    out = {}
    for name, r in rates.items():
        out[name] = {"HS": {s: float(np.mean(r[cells[f"HS {s}"]])) for s in "LR"},
                     "DNa02": {s: float(r[cells[f"DNa02 {s}"]].mean()) for s in "LR"},
                     "DNa01": {s: float(r[cells[f"DNa01 {s}"]].mean()) for s in "LR"}}
    return out


def verdict(sig: dict, stable: dict | None) -> dict:
    lr = lambda scene, group: sig[scene][group]["L"] - sig[scene][group]["R"]
    hs = lr("ccw", "HS") - lr("cw", "HS")
    steer = lr("ccw", "DNa02") - lr("cw", "DNa02")
    out = {"HS_signal_hz": round(hs, 2), "STEER_signal_hz": round(steer, 2),
           "DNa01_signal_hz": round(lr("ccw", "DNa01") - lr("cw", "DNa01"), 2),
           "HS": bool(hs >= 3), "STEER": bool(steer >= 2)}
    if stable is not None:
        out.update(stable)
    return out


def run_gain(brain, ol, gain, cells, drum, tail=True) -> tuple[dict, dict]:
    ol.gain = gain
    rates, stable = {}, {"STABLE": True}
    for name, scene in drum.items():
        moving = name in ("ccw", "cw")
        r, during, late = measure(brain, ol, scene, TAIL if (moving and tail) else 0.0)
        rates[name] = r
        if moving and tail:
            hot = int((r[~brain.external] > 100).sum())
            fraction = float(late.mean() / during.mean()) if during.mean() > 0 else 0.0
            stable[f"{name}_over_100hz"] = hot
            stable[f"{name}_tail_fraction"] = round(fraction, 5)
            stable["STABLE"] &= bool(hot <= 20 and fraction < 0.01)
    return rates, stable


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    scale = 1.0 / sizes(C)
    brain = HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels)
    ol = FlyvisNative(brain, model=MODEL, dt=OPTIC_DT)
    cells = {f"HS {s}": brain.cells(HS, s) for s in "LR"}
    cells.update({f"{t} {s}": brain.cells([t], s) for t in ("DNa02", "DNa01") for s in "LR"})
    results = {"criteria": __doc__, "cells": {k: v.tolist() for k, v in cells.items()}, "gains": {}}
    drum = scenes(30.0, 40.0)
    passing = None
    for gain in GAINS:
        rates, stable = run_gain(brain, ol, gain, cells, drum)
        sig = signals(rates, cells)
        v = verdict(sig, stable)
        results["gains"][str(gain)] = {"signals": sig, "verdict": v}
        print(f"G {gain:5.1f}: HS signal {v['HS_signal_hz']:+.1f} Hz, STEER {v['STEER_signal_hz']:+.1f} Hz, "
              f"DNa01 {v['DNa01_signal_hz']:+.1f} Hz | STABLE {v['STABLE']} "
              f"({v['ccw_over_100hz']}/{v['cw_over_100hz']} over 100 Hz, tail {v['ccw_tail_fraction']}/{v['cw_tail_fraction']})",
              flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        if passing is None and v["STABLE"] and v["HS"] and v["STEER"]:
            passing = gain
            descending = np.flatnonzero(meta["superclass"].astype(str) == "descending_neuron")
            dn_types = sorted(set(types[descending].astype(str)) - {""})
            ranked = []
            for t in dn_types:
                L, R = brain.cells([t], "L"), brain.cells([t], "R")
                if len(L) and len(R):
                    d = (rates["ccw"][L].mean() - rates["ccw"][R].mean()) - (rates["cw"][L].mean() - rates["cw"][R].mean())
                    ranked.append((t, round(float(d), 2)))
            ranked.sort(key=lambda kv: -abs(kv[1]))
            results["descending_direction_signals"] = ranked[:15]
    results["passing_gain"] = passing
    if passing is None:
        results["pass"] = False
        results["seconds"] = round(time.perf_counter() - t0)
        print("FAIL: no gain passes STABLE, HS and STEER", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        return
    print(f"lowest passing gain {passing}; held-out drum (20 deg, 60 deg/s)", flush=True)
    rates, stable = run_gain(brain, ol, passing, cells, scenes(20.0, 60.0))
    held = verdict(signals(rates, cells), stable)
    results["held_out"] = held
    print(f"    HS {held['HS_signal_hz']:+.1f} Hz, STEER {held['STEER_signal_hz']:+.1f} Hz", flush=True)
    print("nulls: 10 degree-preserving rewirings", flush=True)
    rng = np.random.default_rng(31)
    null = []
    for k in range(10):
        rewired = HybridBrain(trials=1, w_syn=W_SYN, matrix=nulls.degree_preserving(M, rng), scale=scale, labels=labels)
        rates, _ = run_gain(rewired, ol, passing, cells, {k2: drum[k2] for k2 in ("ccw", "cw")}, tail=False)
        v = verdict(signals(rates, cells), None)
        null.append({"HS_signal_hz": v["HS_signal_hz"], "STEER_signal_hz": v["STEER_signal_hz"], "STEER": v["STEER"]})
        print(f"    rewiring {k}: HS {v['HS_signal_hz']:+.1f} Hz, STEER {v['STEER_signal_hz']:+.1f} Hz", flush=True)
    results["nulls"] = null
    results["NULL"] = sum(x["STEER"] for x in null) <= 1
    results["pass"] = bool(held["HS"] and held["STEER"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: G {passing}; held-out HS {held['HS']} STEER {held['STEER']}; "
          f"NULL {results['NULL']} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
