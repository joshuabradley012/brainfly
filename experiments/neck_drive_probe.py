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

Ran (2026-10-12, 99 s): the drum drives the brain's yaw neck MNs strongly, on the side whose HS cells it excites, with
the signs the wiring predicts. The pitch MN CvN7 stays where it was. CvN6 answers on the opposite side through its HSS
input. DNa02, the steering check, stays silent.
- The brain's own neurons average 1.67 Hz at grey, with none over 100 Hz. They average 3.6 Hz with the static grating
  and 5.0 with either drum (0.05-0.07% over 100 Hz).
- HS: 66 Hz on the left and 0 on the right under counterclockwise, the mirror under clockwise (direction signal +134
  Hz, t 483). H2: 73 and 148 Hz, then 150 and 68 (-157). The static grating alone raises HS to 6-10 Hz and H2 to 55-66
  Hz, the pattern's onset.
- Yaw MNs, left and right under counterclockwise, then under clockwise (Hz), and their direction signals:
  - GNG283: 36 and 3, then 1 and 41 (+72, t 80);
  - GNG276: 24 and 4, then 2 and 24 (+43, t 62);
  - GNG647 (VCvN1/2): 24 and 2, then 1 and 17 (+37, t 57);
  - GNG653 (CvN1/2): 10.5 and 0.8, then 0.2 and 6.8 (+16, t 21);
  - GNG314 (VCvN3): 2.5 and 1.5, then 1.3 and 3.0 (+2.7, t 5.9).
- DNp15: 52 and 2 Hz, then 0.2 and 68 (+118, t 168), from 0.1-0.2 at grey. DNp20: 1.3 and 0.2, then 0.2 and 1.7 (+2.7,
  t 6.4). DNp22 is silent.
- Pitch and other brain MNs:
  - CvN7 stays at 1-2 Hz throughout (+0.4, t 0.4).
  - CvN4 (+7, t 8.5) and CvN5 (+5.7, t 4.9) move a little.
  - CvN6 fires on the side opposite the stimulated HS (4.9 and 18.8, then 14.8 and 3.3; -25, t -34), as its
    opposite-side HSS input predicts.
  - GNG648 (CvN3, roll): +6 (t 8.6). GNG641 and GNG650 stay within 2.3 Hz.
- DNa02 stays at 0-0.1 Hz in every scene. The optomotor steering signal doesn't reach it in this brain, though
  optomotor.py found it in FlyBrain.
- The VS cells weren't read. MaleCNS types them as one type, "VS" (18 cells), not VS1-VS8.
So in rung 6's brain a yaw drum drives the brain's yaw neck MNs on the side whose HS it excites. That fits the
connectome's routes and blowfly VCNM's preference for front-to-back motion on its own side (Haag et al. 2010). It also
leaves CvN7 alone, as its wiring and Gorko et al.'s tuning (best axis 60-90 deg, nose-up pitch with roll) predict. The
rates run above flies' at rest:
- DNp15 at 52-68 Hz, against about 3 to 12 Hz in quiescent flies (Suver et al. 2016);
- HS spiking at 66 Hz, where flies' HS cells are graded.
So a test should rest on signs and selectivity, not rates. Next: a pre-registered version with these signs and a
rewiring null, and a pitch probe (vertical motion, VS by receptive field, CvN4-7).

Correction (2026-10-12, review 14):
- Left and right are soma sides. CvN6's and CvN7's axons cross (BANC's nerve column), so the CvN6 that fires under the
  counterclockwise drum, the right-soma cell at 18.75 Hz, leaves through the left cervical nerve. By nerve side it fires
  on the stimulated side, with the yaw MNs' sign, and follows its nerve-side HSS, as Gorko et al. frame CvN6's input.
  The docstring expected the pitch MNs CvN4-7 to move little. That failed for CvN6 (-25 by soma side, t -34) and for
  CvN4 (+7, t 8.5), and the Ran didn't say so.
- "It also leaves CvN7 alone, as its wiring and Gorko et al.'s tuning ... predict" doesn't follow.
  - The probe didn't read the VS cells. MaleCNS types them as "VS", not VS1-VS8. Review 14's rerun of this probe read
    them: 19.3 and 12.7 Hz under counterclockwise, 12.1 and 14.3 under clockwise, against 2.1-2.2 at grey.
  - So CvN7's VS input is driven under the drum while CvN7 stays at 1.1-1.8 Hz.
  - Gorko et al. never tested yaw: their rotations were about horizontal axes.
  So the drum doesn't test CvN7's wiring.
- "The static grating alone raises HS to 6-10 Hz and H2 to 55-66 Hz, the pattern's onset": the window starts 0.5 s after
  the onset, and H2's response is sustained, 52-68 Hz through 0.5-2 s (review 14's time courses). The model's H2 cells
  fire at 24-29 times their grey rate to a stationary grating, so their "null-direction" rates under the drum (68-73 Hz)
  are mostly this response to the pattern.
- The quiescent DNp15 comparison: Suver et al.'s Fig. 3G gives quiescent DNHS1 at about 0.5-1 Hz (null axis) to 14 Hz
  (preferred), not "about 3 to 12" (the research note's misreading; dated note there). Their stimulus was a star field at
  22.5 deg/s, not this grating. The model's 52-68 Hz is about four to five times flies' quiescent peak.
- Smaller:
  - CvN7's range is 0.92-2.42 Hz, and DNp15 at grey is 0.08-0.25.
  - "GNG641 and GNG650 stay within 2.3 Hz" refers to their direction signals; their rates reach 3.75 Hz.
  - 0.23% of the brain's own neurons exceed 100 Hz with the static grating.
  - The t values are over 8 noise trials of one network, not across wirings.

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
