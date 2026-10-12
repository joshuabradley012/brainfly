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

Ran (2026-10-12, 76 s): DNa02 sits about 13.5 mV below threshold, and the drum moves it 2-3.5 mV, mostly by inhibiting
one side, so it never fires.
- At grey its median membrane potential is 13.5 mV (left) and 13.8 mV (right) below threshold (95th percentile 9.0 and
  8.3 below). It fires at 0 and 0.08 spikes/s.
- Counterclockwise: left 13.65 mV below (about unchanged), right 17.1 below. Clockwise: left 15.4 below, right 12.6
  below. So the side the drum would turn a fly toward ends up 2.8-3.4 mV less hyperpolarized than the other, the sign of
  flies' steering signal. That comes mainly from inhibiting the other side, and no DNa02 spike results.
- Its strongest inputs by summed weight:
  - AN03A008: +30 mV, about 1.5 spikes/s, unchanged;
  - VES051/052: -25 mV;
  - LAL028/029: +21 mV; 1.7-2.1 spikes/s at grey, falling to 0.1-0.4 under either drum;
  - PS049: -20 mV; the right PS049 rises to 21 spikes/s under counterclockwise, 2.3 mV of drive onto the right DNa02;
  - PS059: -20 mV;
  - PFL3: +15 mV; the central complex's steering cells, unchanged at 1.6-2.1 spikes/s;
  - LLPC1 (59 cells): +14 mV; onto the right DNa02, 0 spikes/s under counterclockwise and 5.7 under clockwise.
- Of the left HS cells' 50 strongest targets, 24 change by more than 5 spikes/s with the drum. 12 of those also synapse
  onto DNa02: DNp15, CB2473, DNg41, CB1693 and CB3560/CB3177 change by 24-57 spikes/s. But their weights are too small to
  rank among its 25 strongest input types.
So by the reading, DNa02 is held too far down to hear the drum: 13.5 mV below threshold, against a 2-3.5 mV signal. The
flight motor neurons were held down the same way (dlm_drive_probe.py). The signal does reach it, with flies' sign, but
mostly as inhibition of one side. In flies, DNa02's firing during walking predicts turning (Rayshubskiy et al. 2020). In
rung 6's brain at rest it is silent, so the body can't be steered through it until its resting state is fly-like.

Correction (2026-10-12, review 15):
- DNa02 isn't held down like the flight motor neurons. It sits at rest_calibration's 0.1 Hz target for every descending
  neuron ("DNa02 near 0 standing"), with a group bias of -12.4 mV, and fires 0-0.08 Hz at grey: on target.
  - That puts it 13.5 mV below threshold, not the reading's "tens of mV".
  - The flight MNs were lowered a further 40-46 mV after calibration, to about 60 mV below threshold.
  - The project's later rate notes put flies' resting DNa02 at about 3-9 spikes/s immobile (Rayshubskiy et al. 2025, the
    eLife version of the work cited above as 2020; descending_neuron_rates.md).
  So the model's DNa02 is quiet because of the 0.1 Hz rule for descending neurons. Raising its target, or modelling a
  walking state, would change that. It isn't the nerve cord's resting-state question.
- The ranking by weight misses inputs that carry about as much of the drum's effect as the 25 strongest types (review
  15's accounting over all 1,112 and 1,172 inputs): LPT22 (GABA; 2 Hz rising to 90-92 under the drum, -0.67 to -0.80
  mV), SAD013 (GABA, -0.54 to -0.61) and PLP012 (ACh, +0.7 to +1.6 undepressed). Under clockwise, the left DNa02's
  inhibition comes more from LPT22 (-0.67) than from PS049 (-0.38).
- The drive estimate assumes full weight. In rung 6's brain cholinergic synapses depress (0.78 per spike, 0.89 s
  recovery), which cuts an input at 50-100 Hz to about a tenth, while GABAergic inhibition doesn't depress. That probably
  explains why the drum reaches DNa02 mostly as inhibition (review 15's reading, not a measured split).
- "12 of those also synapse onto DNa02": 12 of the 50 targets do, and 11 of them change by more than 5 Hz (PS220 by
  0.25 Hz). "24-57 spikes/s" is 23.4-57, and "2.8-3.4 mV" is 2.74-3.43.

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
