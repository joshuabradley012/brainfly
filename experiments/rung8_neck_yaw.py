"""Rung 8 groundwork test, pre-registered (written and committed before it runs): does a rotating drum reach the brain's
yaw neck motor neurons with flies' sign, spare the pitch motor neuron CvN7 as flies' receptive-field map predicts, and
depend on the wiring?

Background:
- research_notes/Rung 8 flight data/neck_head_control.md: about half of the fly's 49 neck motor neurons (MNs) sit in the
  brain. The yaw MNs among them (VCvN1-3 = MaleCNS GNG647 and GNG314; CvN1/2 = GNG653) take synapses straight from the
  HS cells on their side and H2 from the other. Their nerves leave on their soma side.
- The exploratory probes neck_drive_probe.py and neck_pitch_probe.py found the yaw MNs following a yaw drum on the side
  whose HS cells it excites, and CvN7 near rest. Review 14 corrected their readings.
- This test runs the yaw result on fresh seeds, with criteria from fly data and scrambled wiring as the null.
Model: rung6_relay.build("intact") with its eyes (flyvis flow/0000/001 at gain 1), 8 flies, seed 8800, never used
before. Scenes: eyes_at_rest.Setup.run, 1 s of grey then 2 s of a vertical sine grating (period 30 deg) on a drum
rotating counterclockwise (seen from above; front-to-back across the left eye) or clockwise at 40 deg/s; rates from 0.5
to 2 s. The same seed in both scenes.
Direction signal of a cell type: (left - right under counterclockwise) - (left - right under clockwise), per fly, with t
over the 8 flies (mean over sd/sqrt(8)). Sides are nerve sides: soma sides for VCvN, CvN1/2 and DNp15, the opposite side
for CvN7, whose axon crosses (BANC). A positive signal means the side whose HS cells the drum excites fires more.
Criteria, all of which must hold:
- YAW: VCvN1-3 (GNG647 and GNG314 together), CvN1/2 (GNG653) and DNp15 each have a positive direction signal with t >= 4.
  Flies:
  - HS cells depolarize to front-to-back motion on their own eye (Schnell et al. 2010).
  - Blowfly VCNM, the VCvN counterpart, depolarizes to front-to-back motion on its own side (Haag et al. 2010; another
    species).
  - DNHS1 (DNp15) takes HS input and answers yaw best (Suver et al. 2016).
  - Drosophila's HS-to-VCNM contact is anatomical (Pokusaeva et al. 2024).
- SELECTIVITY: CvN7's direction signal is at most a quarter of VCvN1-3's in size. Flies: CvN7's receptive field
  has a horizontal component of at most 0.8 mV, against 2.8 mV for downward motion (Gorko et al. 2024; the note's
  §1.3). Gorko et al. didn't rotate about the vertical axis.
- NULL: in each of 2 degree-preserving rewirings (rung6_relay.relay_null(1) and (2), recalibrated and quieted as rung 6's
  nulls were), VCvN1-3's direction signal is below half of the intact brain's, or its t is below 4. Same seed and scenes.
Reported, not scored: HS, H2, VS, DNa02, GNG283, GNG276, CvN4-6 (CvN6 by nerve side) and the brain's own mean rate, in
every network.
A pass shows that the drum's yaw signal reaches the brain's yaw neck MNs with flies' sign, spares CvN7 as flies' map
predicts, and depends on the wiring. It doesn't test rates (the model's run above flies' at rest), the head's movement,
or which way a fly turns its head (the note's §1.6).

    python experiments/rung8_neck_yaw.py      (writes experiments/rung8_neck_yaw.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung6_relay as r6
from brainfly.eye2d import Grating

OUT = Path(__file__).with_suffix(".json")
SEED, GAIN, REWIRINGS = 8800, 1.0, (1, 2)
WINDOW = (0.5, 2.0)
SCENES = {"ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)]}
GROUPS = {"VCvN1-3": ["GNG647", "GNG314"], "CvN1/2": ["GNG653"], "DNp15": ["DNp15"], "CvN7": ["CvN7"],
          "HS": ["HSN", "HSE", "HSS"], "H2": ["H2"], "VS": ["VS"], "DNa02": ["DNa02"], "GNG283": ["GNG283"],
          "GNG276": ["GNG276"], "CvN4": ["CvN4"], "CvN5": ["CvN5"], "CvN6": ["CvN6"]}
CROSSED = {"CvN6", "CvN7"}                          # nerve on the side opposite the soma (BANC)


def signal(per: dict, group: str) -> dict:
    d = (per["ccw"][group]["L"] - per["ccw"][group]["R"]) - (per["cw"][group]["L"] - per["cw"][group]["R"])
    if group in CROSSED:
        d = -d                                      # by nerve side
    sd = float(d.std(ddof=1))
    t = float(d.mean() / (sd / np.sqrt(len(d)))) if sd > 0 else (float("inf") * np.sign(d.mean()) if d.mean() else 0.0)
    return {"direction_signal_hz": round(float(d.mean()), 3), "t": round(t, 2) if np.isfinite(t) else t}


def measure(s, seed: int) -> dict:
    b = s.brain
    cells = {g: {x: b.cells(types, x) for x in "LR"} for g, types in GROUPS.items()}
    per, own = {}, {}
    for name, scene in SCENES.items():
        r = s.run(scene, GAIN, seed, WINDOW)
        per[name] = {g: {x: r["rates"][:, v].mean(1) for x, v in d.items()} for g, d in cells.items()}
        own[name] = round(r["own_mean_hz"], 3)
    return {"cells": {g: {x: int(len(v)) for x, v in d.items()} for g, d in cells.items()}, "own_mean_hz": own,
            "rates_hz": {sc: {g: {x: round(float(v.mean()), 2) for x, v in d.items()} for g, d in per[sc].items()} for sc in per},
            "signals": {g: signal(per, g) for g in GROUPS}}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "criteria": {}}
    s = r6.build("intact")
    out["intact"] = intact = measure(s, SEED)
    print("intact", json.dumps(intact["signals"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    del s                                           # one whole brain in memory at a time
    sig = intact["signals"]
    yaw = {g: bool(sig[g]["direction_signal_hz"] > 0 and float(sig[g]["t"]) >= 4) for g in ("VCvN1-3", "CvN1/2", "DNp15")}
    out["criteria"]["YAW"] = {"pass": all(yaw.values()), "by_group": yaw}
    ratio = abs(sig["CvN7"]["direction_signal_hz"]) / max(abs(sig["VCvN1-3"]["direction_signal_hz"]), 1e-9)
    out["criteria"]["SELECTIVITY"] = {"pass": bool(ratio <= 0.25), "cvn7_over_vcvn": round(ratio, 4)}
    out["nulls"] = []
    for rw in REWIRINGS:
        n, log = r6.relay_null(rw)
        m = measure(n, SEED)
        m["rewiring"], m["calibration_last"] = rw, log[-1] if log else None
        out["nulls"].append(m)
        del n
        print(f"null {rw}", json.dumps(m["signals"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    v = sig["VCvN1-3"]["direction_signal_hz"]
    null_ok = [bool(m["signals"]["VCvN1-3"]["direction_signal_hz"] < 0.5 * v or float(m["signals"]["VCvN1-3"]["t"]) < 4) for m in out["nulls"]]
    out["criteria"]["NULL"] = {"pass": all(null_ok), "by_rewiring": null_ok}
    out["pass"] = bool(all(c["pass"] for c in out["criteria"].values()))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("criteria", json.dumps(out["criteria"]), "pass", out["pass"], flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
