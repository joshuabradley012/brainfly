"""Exploratory probe, written before it runs, not pre-registered: in rung 6's whole brain with its eyes, does vertical
motion reach the brain's pitch neck motor neurons, as their wiring and the one recording of them predict?

neck_drive_probe.py: a yaw drum drives the brain's yaw neck MNs on the side whose HS cells it excites, and leaves CvN7, a
pitch MN, near rest. research_notes/Rung 8 flight data/neck_head_control.md:
- The pitch MNs CvN4-7 pitch the head down. They take direct synapses from frontal VS cells, about 100 per CvN7, 105-109
  per CvN6 and 64-69 per CvN5 (the note's summary, item 3).
- Gorko et al. 2024 recorded CvN7. It depolarizes and spikes to downward, not upward, local motion fronto-dorsally on
  one eye (item 5).
- Downward motion in front comes from nose-up pitch, so a pitch-down response compensates (item 11).
- VS cells depolarize to downward motion in their receptive fields (item 6).
Model: rung6_relay.build("intact") with its eyes (flyvis flow/0000/001 at gain 1), 8 flies, as neck_drive_probe.py.
Scenes: eyes_at_rest.Setup.run, 1 s of grey then 2 s of the scene, rates from 0.5 to 2 s; seed 7710, the same noise in
every scene. The scenes:
- grey;
- a static grating of horizontal stripes, period 30 deg (brainfly.eye2d.ElevationGrating), on both eyes;
- the stripes moving down at 40 deg/s (1.33 Hz) on both eyes;
- the stripes moving up at 40 deg/s.
Read-out, per side:
- the pitch MNs CvN4-7;
- the yaw MNs (GNG283, GNG276, GNG647, GNG653, GNG314), as a control;
- the VS cells (MaleCNS type "VS") and HS;
- DNp20, DNp22 and DNp15.
For each: its rate in every scene, and its vertical signal, (down - up) summed over the two sides, with t over flies.
Expected:
- CvN4-7 and the VS cells fire more to downward than to upward motion: positive signals.
- DNp20 and DNp22, which take VS input, follow them.
- The yaw MNs, HS and DNp15 move little.
These are expectations to describe, not criteria.

    python experiments/neck_pitch_probe.py      (writes experiments/neck_pitch_probe.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung6_relay as r6
from brainfly.eye2d import ElevationGrating

OUT = Path(__file__).with_suffix(".json")
SEED, GAIN = 7710, 1.0
WINDOW = (0.5, 2.0)
PITCH, YAW = ["CvN4", "CvN5", "CvN6", "CvN7"], ["GNG283", "GNG276", "GNG647", "GNG653", "GNG314"]
GROUPS = {**{t: [t] for t in PITCH + YAW}, "VS": ["VS"], "HS": ["HSN", "HSE", "HSS"],
          "DNp20": ["DNp20"], "DNp22": ["DNp22"], "DNp15": ["DNp15"]}
SCENES = {"grey": lambda t: [], "static": lambda t: [ElevationGrating(30.0, 0.0)],
          "down": lambda t: [ElevationGrating(30.0, -40.0 * t)], "up": lambda t: [ElevationGrating(30.0, 40.0 * t)]}


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    cells = {g: {x: b.cells(types, x) for x in "LR"} for g, types in GROUPS.items()}
    out = {"question": __doc__, "cells": {g: {x: int(len(v)) for x, v in d.items()} for g, d in cells.items()}, "scenes": {}}
    print("built", json.dumps(out["cells"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    per_fly = {}
    for name, scene in SCENES.items():
        r = s.run(scene, GAIN, SEED, WINDOW)
        per_fly[name] = {g: {x: r["rates"][:, v].mean(1) for x, v in d.items() if len(v)} for g, d in cells.items()}
        out["scenes"][name] = {"own_mean_hz": round(r["own_mean_hz"], 3), "own_over_100hz": round(r["own_over_100hz"], 5),
                               "rates_hz": {g: {x: round(float(v.mean()), 2) for x, v in d.items()} for g, d in per_fly[name].items()}}
        print(name, json.dumps(out["scenes"][name]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    signal = {}
    for g in GROUPS:
        sides = [x for x in "LR" if x in per_fly["down"][g]]
        if not sides:
            continue
        d = sum(per_fly["down"][g][x] - per_fly["up"][g][x] for x in sides)
        sd = float(d.std(ddof=1))
        t = float(d.mean() / (sd / np.sqrt(len(d)))) if sd > 0 else (float("inf") * np.sign(d.mean()) if d.mean() else 0.0)
        signal[g] = {"vertical_signal_hz": round(float(d.mean()), 3), "t": round(t, 2) if np.isfinite(t) else str(t),
                     "down_minus_up_hz": {x: round(float((per_fly["down"][g][x] - per_fly["up"][g][x]).mean()), 3) for x in sides}}
    out["vertical"] = signal
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("vertical", json.dumps(signal), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
