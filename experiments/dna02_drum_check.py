"""Exploratory check, written before it runs, not pre-registered and not a change to the model: why does the rotating
drum leave DNa02 silent in rung 6's brain?

neck_drive_probe.py:
- A drum drives the left HS cells to 66 spikes/s, DNp15 to 52-68 and the brain's yaw neck motor neurons hard.
- DNa02, which the optomotor tests used as the steering signal (optomotor.py found it in FlyBrain), stays at 0-0.1
  spikes/s in every scene.
- Rung 7's walking body is steered through DNa02. So if it can't hear the drum, closed-loop optomotor turning can't work
  in this brain.
Model: rung6_relay.build("intact") with its eyes (flyvis flow/0000/001, gain 1), 8 flies, seed 7700 as there. Scenes:
grey and the counterclockwise and clockwise drums (30 deg, 40 deg/s), 1 s of grey then 2 s of the scene, rates from 0.5
to 2 s (eyes_at_rest.Setup.run's protocol, stepped here so that voltages can be read).
Measured:
- DNa02's rate and its membrane potential below threshold (median and 95th percentile, sampled every 2 ms).
- Its 25 strongest presynaptic types by summed signed weight. Each with its weight onto DNa02, its rate in each scene
  and side, and its drive onto DNa02: weight x rate x 5 ms, the mean synaptic drive in mV if every spike delivered its
  full weight over the synaptic time constant.
- How many of the left HS cells' strongest targets, two synapses away from DNa02, change their rate with the drum.
Read: if DNa02 sits tens of mV below threshold while its inputs' drive changes by a few mV, it is held too far down to
hear the drum, as the flight motor neurons were (dlm_drive_probe.py). If its inputs don't change, the signal doesn't
reach it through the wiring.

    python experiments/dna02_drum_check.py      (writes experiments/dna02_drum_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rung6_relay as r6
from brainfly.eye2d import Grating

OUT = Path(__file__).with_suffix(".json")
SEED, GAIN = 7700, 1.0
WINDOW = (0.5, 2.0)
SCENES = {"grey": lambda t: [], "ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)]}
TOP = 25
TAU_SYN = 0.005


def run(s: eyes.Setup, scene, seed: int, watch: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Setup.run's protocol: each neuron's rate per fly in WINDOW, and `watch`'s voltages below threshold (every 2 ms)."""
    b, ol = s.brain, s.ol
    b.reset(seed)
    ol.reset()
    ol.gain = GAIN
    per = int(round(eyes.OPTIC_DT / b.dt))
    for _ in range(int(round(eyes.SETTLE / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(None))
        b.advance(per)
    a, z = int(round(WINDOW[0] / eyes.OPTIC_DT)), int(round(WINDOW[1] / eyes.OPTIC_DT))
    acc = np.zeros((b.trials, b.n))
    volts = []
    for k in range(int(round(eyes.SCENE / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(scene(k * eyes.OPTIC_DT))))
        c = b.advance(per)
        if a <= k < z:
            acc += c
            volts.append((b.u[:, watch] - theta[watch]).copy())
    return acc / (WINDOW[1] - WINDOW[0]), np.stack(volts, 1)                    # (flies, n), (flies, samples, watched)


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    theta = np.array([b.params[k]["threshold"] for k in range(len(b.params))])[b.cls]
    dna02 = {x: b.cells(["DNa02"], x) for x in "LR"}
    watch = np.concatenate([dna02["L"], dna02["R"]])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    types = np.where(np.asarray(b.cell_type).astype(str) != "", np.asarray(b.cell_type).astype(str), np.asarray(b.mcns_type).astype(str))
    out = {"question": __doc__, "dna02_cells": {x: [int(i) for i in v] for x, v in dna02.items()}, "scenes": {}}
    rates, volts = {}, {}
    for name, scene in SCENES.items():
        rates[name], volts[name] = run(s, scene, SEED, watch, theta)
        v = volts[name]
        out["scenes"][name] = {
            "dna02_hz": {x: round(float(rates[name][:, dna02[x]].mean()), 3) for x in "LR"},
            "dna02_v_below_threshold_mv": {x: {"median": round(float(np.median(v[:, :, k])), 2), "p95": round(float(np.percentile(v[:, :, k], 95)), 2)}
                                           for k, x in enumerate("LR")}}
        print(name, json.dumps(out["scenes"][name]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    inputs = {}
    for x in "LR":
        e = np.flatnonzero(np.isin(b.idx, dna02[x]))
        w = np.asarray(b.weights[e], np.float64)
        by_type = {}
        for src, wt in zip(pre[e], w):
            t = types[src]
            by_type.setdefault(t, {"cells": set(), "weight_mv": 0.0})
            by_type[t]["cells"].add(int(src))
            by_type[t]["weight_mv"] += float(wt)
        ranked = sorted(by_type.items(), key=lambda kv: -abs(kv[1]["weight_mv"]))[:TOP]
        rows = []
        for t, info in ranked:
            cells = np.array(sorted(info["cells"]))
            per_cell = {}
            for src in cells:
                per_cell[int(src)] = float(w[pre[e] == src].sum())
            drive = {sc: round(float(sum(per_cell[c] * rates[sc][:, c].mean() for c in cells) * TAU_SYN), 3) for sc in SCENES}
            rows.append({"type": t, "cells": int(len(cells)), "weight_mv": round(info["weight_mv"], 2),
                         "rate_hz": {sc: round(float(rates[sc][:, cells].mean()), 2) for sc in SCENES}, "drive_mv": drive})
        inputs[x] = rows
        print(f"inputs {x}", json.dumps(rows[:10]), flush=True)
    out["inputs"] = inputs
    hs_l = b.cells(["HSN", "HSE", "HSS"], "L")
    e = np.flatnonzero(np.isin(pre, hs_l))
    tgt = {}
    for post, wt in zip(b.idx[e], b.weights[e]):
        tgt[int(post)] = tgt.get(int(post), 0.0) + float(wt)
    top_targets = sorted(tgt, key=lambda k: -tgt[k])[:50]
    into_dna02 = set(pre[np.isin(b.idx, watch)].tolist())
    two_hop = [c for c in top_targets if c in into_dna02]
    change = lambda c: float(rates["ccw"][:, c].mean() - rates["cw"][:, c].mean())
    out["hs_left_top50_targets"] = {
        "changing_over_5hz": int(sum(abs(change(c)) > 5 for c in top_targets)),
        "also_presynaptic_to_dna02": [{"cell": int(c), "type": str(types[c]), "weight_from_hs_mv": round(tgt[c], 2),
                                       "ccw_minus_cw_hz": round(change(c), 2)} for c in two_hop]}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("hs targets", json.dumps(out["hs_left_top50_targets"]), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
