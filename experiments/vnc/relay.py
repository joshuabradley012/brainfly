"""Do the brain's commands reach the motor neurons? The nerve cord relay, with brainfly's defaults.

Descending neurons carry the brain's commands to the nerve cord, where premotor circuits drive the
motor neurons. This drives five commands with brainfly's default settings, each at 0.8 extra volts per
20 ms step (about 25 Hz): forward walking (DNg100, both sides), steering (DNa02, left or right),
escape (DNp01, both) and backward walking (MDN, both). It records every motor neuron, pooled by side
and by body segment: the neck (superclass cb_motor), and the nerve cord's motor neurons (vnc_motor)
by the position of their cell body along the cord: front legs (T1), middle legs and wings (T2), and
hind legs and abdomen (T3 onwards). Synapses onto sensory neurons are removed (sensory_input=False),
so the olfactory receptors' runaway doesn't flood the network.
Each condition: 8 flies, 1 s to settle, 1 s baseline, 1 s with the command driven; rates per fly, and
the change from baseline with t over flies.
Question, stated before the run: does any command raise any motor pool by >= 3 Hz with t >= 4?
(Earlier tests with the inherited code found every motor group moved by under 0.6 Hz, and neither
retuning the nerve cord's gain and drive nor 2-5 ms steps got commands through without also driving
the motor neurons at rest.)

    python experiments/vnc/relay.py            (writes experiments/vnc/relay.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import FlyBrain

OUT = Path(__file__).with_name("relay.json")
FLIES, SEED, VOLTS = 8, 5, 0.8
COMMANDS = {"forward (DNg100)": (["DNg100"], None), "steer left (DNa02 L)": (["DNa02"], "L"),
            "steer right (DNa02 R)": (["DNa02"], "R"), "escape (DNp01)": (["DNp01"], None),
            "backward (MDN)": (["MDN"], None)}
BANDS = {"T1": (-np.inf, 76_000), "T2": (76_000, 100_000), "T3+": (100_000, np.inf)}   # cell body depth, EM voxels


def pools(brain: FlyBrain) -> dict[str, np.ndarray]:
    sc, side = brain.superclass.astype(str), brain.side.astype(str)
    depth = brain.positions[:, 2]
    out = {}
    for s in "LR":
        out[f"neck {s}"] = np.flatnonzero((sc == "cb_motor") & (side == s))
        for band, (lo, hi) in BANDS.items():
            out[f"{band} {s}"] = np.flatnonzero((sc == "vnc_motor") & (side == s) & (depth >= lo) & (depth < hi))
    return {k: v for k, v in out.items() if len(v)}


def window(brain: FlyBrain, steps: int, inject, pool_of: np.ndarray, n_pools: int, cmd) -> tuple[np.ndarray, np.ndarray]:
    """Spike counts per pool and fly, and the driven command neurons' spike count per fly, over `steps`."""
    counts = np.zeros((n_pools, brain.batch))
    driven = np.zeros(brain.batch)
    for _ in range(steps):
        for b, idx in enumerate(brain.step(inject=inject)):
            g = pool_of[idx]
            np.add.at(counts[:, b], g[g >= 0], 1)
            if cmd is not None:
                driven[b] += np.isin(cmd, idx).sum()
    return counts, driven


def main() -> None:
    brain = FlyBrain(batch=FLIES, sensory_input=False)
    groups = pools(brain)
    names = list(groups)
    pool_of = np.full(brain.n, -1)
    for g, name in enumerate(names):
        pool_of[groups[name]] = g
    sizes = np.array([len(groups[k]) for k in names])[:, None]
    second = int(round(1.0 / brain.dt))
    out = {"question": __doc__, "pools": {k: int(len(v)) for k, v in groups.items()}, "commands": {}}
    print("motor pools:", {k: int(len(v)) for k, v in groups.items()})
    biggest = 0.0
    for label, (types, side) in COMMANDS.items():
        cmd = brain.cells(types, side)
        brain.reset(SEED)
        window(brain, second, (), pool_of, len(names), None)                        # settle
        base, _ = window(brain, second, (), pool_of, len(names), None)
        drive, fired = window(brain, second, [(cmd, VOLTS)], pool_of, len(names), cmd)
        change = {}
        for g, name in enumerate(names):
            d = (drive[g] - base[g]) / sizes[g]
            sd = d.std(ddof=1)
            change[name] = {"delta": round(float(d.mean()), 3), "t": round(float(d.mean() / (sd / np.sqrt(len(d)))), 1) if sd > 0 else 0.0}
        top = max(change.items(), key=lambda kv: abs(kv[1]["delta"]))
        biggest = max(biggest, abs(top[1]["delta"]))
        out["commands"][label] = {"neurons": int(len(cmd)), "command_hz": round(float(fired.mean() / len(cmd)), 1),
                                  "resting_pool_hz": {k: round(float(base[g].mean() / sizes[g, 0]), 2) for g, k in enumerate(names)},
                                  "change": change}
        print(f"{label}: {len(cmd)} neurons at {fired.mean() / len(cmd):.0f} Hz; biggest motor change {top[0]} "
              f"{top[1]['delta']:+.2f} Hz (t {top[1]['t']})", flush=True)
    reached = [(c, p) for c, r in out["commands"].items() for p, x in r["change"].items() if x["delta"] >= 3 and x["t"] >= 4]
    out["reached"] = reached
    print(f"commands reaching a motor pool (>= 3 Hz, t >= 4): {reached or 'none'}; biggest change of any pool {biggest:.2f} Hz")
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
