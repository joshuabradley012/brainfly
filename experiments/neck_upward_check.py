"""Exploratory check, written before it runs, not pre-registered and not a change to the model: which inputs make the
brain's yaw neck motor neurons answer upward motion in rung 6's brain?

neck_pitch_probe.py:
- Stripes moving up drive the left yaw neck MNs: GNG276 rises from 3.7 to 11.8 Hz, and GNG647 and GNG283 rise too. HS is
  silent.
- DNp15 answers upward motion on both sides (5.8 and 7.2 Hz, against 0.9 and 1.9 for downward).
- H2, which feeds both, wasn't read.
Flies' yaw neck MNs take HS and H2 input, both tuned to horizontal motion, so a response to vertical motion needs some
other route, or is an artifact.
Model and scenes: neck_pitch_probe.py's (rung 6's brain with its eyes at gain 1, 8 flies, seed 7710). Grey, then
horizontal stripes (period 30 deg) moving up and moving down at 40 deg/s; rates from 0.5 to 2 s.
Measured, for each of the left and right GNG276, GNG647, GNG283 and DNp15:
- its rate in each scene;
- its 15 strongest presynaptic types by summed signed weight, each with its rate in each scene and its drive onto the
  target, weight x rate x 5 ms;
- the inputs ranked by their drive's change, up minus down.
Also each scene's rates for H2, HS, VS, LPLC1, LPLC2, LLPC1-3 and the brain's own mean.
Read:
- If a few input types carry most of the upward change, they are the route. Whether flies' versions of them answer
  vertical motion decides whether it's an artifact.
- If the change is spread thinly over many inputs, it is the brain's general rise with upward motion (own mean 6.2 Hz,
  against 5.2 for down), not a specific route.

    python experiments/neck_upward_check.py      (writes experiments/neck_upward_check.json)
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
SCENES = {"grey": lambda t: [], "up": lambda t: [ElevationGrating(30.0, 40.0 * t)], "down": lambda t: [ElevationGrating(30.0, -40.0 * t)]}
TARGETS = ["GNG276", "GNG647", "GNG283", "DNp15"]
CONTEXT = {"H2": ["H2"], "HS": ["HSN", "HSE", "HSS"], "VS": ["VS"], "LPLC1": ["LPLC1"], "LPLC2": ["LPLC2"],
           "LLPC1": ["LLPC1"], "LLPC2": ["LLPC2"], "LLPC3": ["LLPC3"]}
TOP, TAU_SYN = 15, 0.005


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    rates, own = {}, {}
    for name, scene in SCENES.items():
        r = s.run(scene, GAIN, SEED, WINDOW)
        rates[name], own[name] = r["rates"].mean(0), round(r["own_mean_hz"], 3)       # fly means per neuron
        print(name, own[name], f"({time.perf_counter() - t0:.0f} s)", flush=True)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    ct = np.asarray(b.cell_type).astype(str)
    types = np.where(ct != "", ct, np.asarray(b.mcns_type).astype(str))
    out = {"question": __doc__, "own_mean_hz": own, "context_hz": {}, "targets": {}}
    for g, tt in CONTEXT.items():
        out["context_hz"][g] = {x: {sc: round(float(rates[sc][b.cells(tt, x)].mean()), 2) if len(b.cells(tt, x)) else None for sc in SCENES}
                                for x in "LR"}
    for target in TARGETS:
        for x in "LR":
            cells = b.cells([target], x)
            e = np.flatnonzero(np.isin(b.idx, cells))
            w = np.asarray(b.weights[e], np.float64)
            src = pre[e]
            by_type = {}
            for c, wt in zip(src, w):
                d = by_type.setdefault(types[c], {})
                d[int(c)] = d.get(int(c), 0.0) + float(wt)
            rows = []
            for t, per_cell in by_type.items():
                cs = np.array(list(per_cell))
                ws = np.array([per_cell[c] for c in cs])
                drive = {sc: float((ws * rates[sc][cs]).sum() * TAU_SYN) for sc in SCENES}
                rows.append({"type": t, "cells": int(len(cs)), "weight_mv": round(float(ws.sum()), 2),
                             "rate_hz": {sc: round(float(rates[sc][cs].mean()), 2) for sc in SCENES},
                             "drive_mv": {sc: round(v, 3) for sc, v in drive.items()},
                             "up_minus_down_mv": round(drive["up"] - drive["down"], 3)})
            strongest = sorted(rows, key=lambda r: -abs(r["weight_mv"]))[:TOP]
            changing = sorted(rows, key=lambda r: -abs(r["up_minus_down_mv"]))[:TOP]
            total = sum(r["up_minus_down_mv"] for r in rows)
            out["targets"][f"{target} {x}"] = {
                "rate_hz": {sc: round(float(rates[sc][cells].mean()), 2) for sc in SCENES},
                "summed_up_minus_down_mv": round(total, 3),
                "top5_share_of_change": round(sum(r["up_minus_down_mv"] for r in changing[:5]) / total, 3) if abs(total) > 1e-9 else None,
                "strongest_inputs": strongest, "most_changing_inputs": changing}
            print(f"{target} {x}", json.dumps(out["targets"][f"{target} {x}"]["rate_hz"]), "change", round(total, 3),
                  json.dumps([(r["type"], r["up_minus_down_mv"]) for r in changing[:6]]), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("context", json.dumps(out["context_hz"]), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
