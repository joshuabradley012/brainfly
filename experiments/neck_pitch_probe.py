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

Ran (2026-10-12, 102 s): vertical motion drives the VS cells and DNp20 hard, and the pitch MN CvN7 a little, the right
way round. CvN4-6 barely move. The yaw MNs and DNp15 answer upward motion, mostly on the left.
- The brain's own neurons average 1.65 Hz at grey, 4.4 with the static stripes, 5.2 with the stripes moving down and 6.2
  moving up (0.1-0.5% over 100 Hz).
- VS cells (9 per side): 85 and 88 Hz to downward motion, 7 and 8 to upward (vertical signal +158 Hz, t 1166), and 0 to
  the static stripes. HS cells are silent (0 Hz) in every stripe scene, against 1.9-2.1 at grey.
- DNp20: 48 and 40 Hz down, 0.1-0.3 up (+88, t 86). DNp22: 3.0 and 6.8 down, 0 up (+9.8, t 18).
- Pitch MNs, left and right under down, then under up (Hz):
  - CvN7: 4.2 and 2.8, then 1.5 and 1.4 (+4.0, t 8.5);
  - CvN4: 2.0 and 3.7, then 2.4 and 2.1 (+1.2, t 2.3);
  - CvN5: +0.8 (t 0.9);
  - CvN6: 6.4 and 5.5, then 3.5 and 7.5 (+0.9, t 1.3).
- Yaw MNs: negative signals, from the left side's response to upward motion.
  - GNG276: -9.3 (t -12.7; left 3.7 Hz down, 11.8 up);
  - GNG647: -6.7 (t -11.0);
  - GNG283: -5.5 (t -9.4);
  - GNG653: -3.8 (t -12.7);
  - GNG314: +0.2.
  DNp15 also answers upward motion (5.8 and 7.2 Hz, against 0.9 and 1.9; -10.2, t -11.4), with HS silent.
So the VS cells and DNp20 follow downward motion strongly, as flies' VS cells and DNOVS1 prefer downward motion. CvN7
follows it the right way round, as Gorko et al. recorded, but weakly: 85 Hz of VS input raises it from about 2 to 3.5 Hz.
Its VS input is 1.2-1.4% of its chemical input (the note's summary, item 3), and in blowflies the VS-to-CNMN link is
electrical (Wertz et al. 2012), which the chemical connectome can't show. The yaw MNs' and DNp15's response to upward
motion comes through some other route, since HS is silent, and more on the left than the right. It wasn't predicted
and isn't explained here.

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
