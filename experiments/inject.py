"""Past the eye: do the fly's own feature detectors drive the right command neurons?

Instead of showing the fly a scene, this drives two sets of visual projection neurons on the fly's
left directly, with brainfly's default settings (tonic 0.14, gain 3.0), and records descending
neurons on both sides:
  loom   LC4 and LPLC2, the looming detectors, whose strongest target is the giant fiber (DNp01)
  chase  LC10a, which males use to track a female during courtship, feeding the steering neuron DNa02
Each detector gets 0.3 or 0.8 extra volts per 20 ms step for 2 s; rates are counted over the last
1.5 s, 8 flies, the same noise with and without the drive, a bright blank field on the eye (drive
0.45). Measure: each descending neuron's rate change on each side (t over flies).
Question, stated before the run: does each drive raise its known target on the same side (loom:
DNp01; chase: DNa02) by >= 3 Hz with t >= 4, and more than on the other side?

    python experiments/inject.py            (writes experiments/inject.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import FlyBrain

OUT = Path(__file__).with_name("inject.json")
SECONDS, SKIP, FLIES, SEED = 2.0, 0.5, 8, 11
DRIVES = {"loom": ["LC4", "LPLC2"], "chase": ["LC10a"]}
TARGET = {"loom": "DNp01", "chase": "DNa02"}
WATCH = ["DNp01", "DNp10", "DNa02", "DNg13", "MDN", "DNg100"]


def rates(brain: FlyBrain, cells, volts: float, watch: dict) -> dict[str, np.ndarray]:
    brain.reset(SEED)
    lit = np.full(len(brain.visual), 0.45, np.float32)
    counts = {k: np.zeros(brain.batch) for k in watch}
    steps = int(round(SECONDS / brain.dt))
    for s in range(steps):
        fired = brain.step(lit, inject=[(cells, volts)] if cells is not None else ())
        if s * brain.dt < SKIP:
            continue
        for b, idx in enumerate(fired):
            hit = np.zeros(brain.n, bool)
            hit[idx] = True
            for k, rows in watch.items():
                counts[k][b] += hit[rows].sum()
    window = SECONDS - SKIP
    return {k: counts[k] / (len(watch[k]) * window) for k in watch}


def main() -> None:
    brain = FlyBrain(batch=FLIES)
    watch = {f"{t} {s}": brain.cells([t], s) for t in WATCH for s in "LR"}
    watch = {k: v for k, v in watch.items() if len(v)}
    rest = rates(brain, None, 0.0, watch)
    out = {"question": __doc__, "rest_hz": {k: round(float(v.mean()), 2) for k, v in rest.items()}, "drives": {}}
    for name, types in DRIVES.items():
        cells = brain.cells(types, "L")
        for volts in (0.3, 0.8):
            r = rates(brain, cells, volts, watch)
            change = {}
            for k in watch:
                d = r[k] - rest[k]
                sd = d.std(ddof=1)
                change[k] = {"delta": round(float(d.mean()), 2), "t": round(float(d.mean() / (sd / np.sqrt(len(d)))), 1) if sd > 0 else 0.0}
            target = TARGET[name]
            near, far = change[f"{target} L"], change[f"{target} R"]
            answer = near["delta"] >= 3 and near["t"] >= 4 and near["delta"] > far["delta"]
            out["drives"][f"{name} x{volts}"] = {"cells": int(len(cells)), "change": change, "target_same_side": bool(answer)}
            print(f"{name} ({len(cells)} neurons, left) x{volts}: {target} left {near['delta']:+.1f} (t {near['t']}), "
                  f"right {far['delta']:+.1f} | " + " ".join(f"{k} {v['delta']:+.1f}" for k, v in change.items()), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
