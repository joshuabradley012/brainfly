"""Exploratory probe, written before it runs, not pre-registered: in rung 6's whole brain with its eyes, does a rotating
drum reach the brain's neck motor neurons, with the signs the wiring predicts?

research_notes/Rung 8 flight data/neck_head_control.md:
- About half of the fly's 49 neck motor neurons (MNs) sit in the brain, in the labial neuromere of the GNG.
- The yaw MNs among them take synapses straight from the lobula plate tangential cells: soma-side HS and opposite-side
  H2. These are VCvN1-3 (MaleCNS GNG647 and GNG314), CvN1/2 (GNG653) and the unmatched GNG283 and GNG276. The pitch MNs
  CvN4-7 take frontal VS cells.
- In blowflies VCNM depolarizes to front-to-back motion on its own side (Haag et al. 2010). In Drosophila only CvN7, a
  pitch MN, has been recorded (Gorko et al. 2024).
- DNp15 (DNHS1), which carries HS signals to the nerve cord's neck MNs, prefers yaw (Suver et al. 2016).
- The nerve cord relay doesn't pass descending signals yet (rung 5), so the brain MNs are this probe's targets.
Model: rung6_relay.build("intact") with its eyes (flyvis flow/0000/001 at gain 1, as rung 6's looms), 8 flies.
Scenes: eyes_at_rest.Setup.run, 1 s of grey then 2 s of the scene, with rates from 0.5 to 2 s; seed 7700, the same
noise in every scene.
- grey;
- a static vertical sine grating, period 30 deg;
- the grating rotating counterclockwise at 40 deg/s (1.33 Hz) and clockwise (optomotor.py's drum).
Read-out, per side:
- the brain neck MNs (GNG647, GNG314, GNG653, GNG283, GNG276, GNG648, CvN4-7, GNG641, GNG650; the note's section 2.2);
- HS (HSN, HSE, HSS), H2 and the VS cells;
- DNp15, DNp20 and DNp22;
- DNa02, the optomotor steering signal, as a check that the drum gets through.
For each: its rate in every scene, and its direction signal, (left - right under counterclockwise) - (left - right under
clockwise), with t over flies.
Expected from the wiring (the note's sections 3.6 and 7.3):
- A counterclockwise drum sweeps front-to-back across the left eye, so left HS rises. The left yaw MNs (VCvN, CvN1/2,
  GNG283/GNG276), the left DNp15 and the left DNa02 should then rise, with clockwise the reverse: positive direction
  signals.
- The pitch MNs CvN4-7 should move little.
These are expectations to describe, not criteria. A pre-registered test comes after, with these signs and the
selectivity as criteria and rewiring as the null.

    python experiments/neck_drive_probe.py      (writes experiments/neck_drive_probe.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung6_relay as r6
from brainfly.eye2d import Grating

OUT = Path(__file__).with_suffix(".json")
SEED, GAIN = 7700, 1.0
WINDOW = (0.5, 2.0)
NECK = ["GNG647", "GNG314", "GNG653", "GNG283", "GNG276", "GNG648", "CvN4", "CvN5", "CvN6", "CvN7", "GNG641", "GNG650"]
GROUPS = {**{t: [t] for t in NECK}, "HS": ["HSN", "HSE", "HSS"], "H2": ["H2"],
          "VS": [f"VS{k}" for k in range(1, 9)], "DNp15": ["DNp15"], "DNp20": ["DNp20"], "DNp22": ["DNp22"], "DNa02": ["DNa02"]}
SCENES = {"grey": lambda t: [], "static": lambda t: [Grating(30.0, 0.0)],
          "ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)]}


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
        if not all(x in per_fly["ccw"][g] for x in "LR"):
            continue
        d = (per_fly["ccw"][g]["L"] - per_fly["ccw"][g]["R"]) - (per_fly["cw"][g]["L"] - per_fly["cw"][g]["R"])
        sd = float(d.std(ddof=1))
        t = float(d.mean() / (sd / np.sqrt(len(d)))) if sd > 0 else (float("inf") * np.sign(d.mean()) if d.mean() else 0.0)
        signal[g] = {"direction_signal_hz": round(float(d.mean()), 3), "t": round(t, 2) if np.isfinite(t) else str(t),
                     "cw_minus_ccw_hz": {x: round(float((per_fly["cw"][g][x] - per_fly["ccw"][g][x]).mean()), 3) for x in "LR"}}
    out["direction"] = signal
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("direction", json.dumps(signal), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
