"""Exploratory, not pre-registered: does a stronger synapse bring taste back to the resting brain while it
still rests and escapes?

Shiu et al. (2024) fitted their one synaptic weight so that sugar at 100 Hz drives MN9 to about 80% of its
maximum, and rung 1 refitted it for MaleCNS (1.5556 mV). The resting brain keeps that weight and adds a
bias per cell type calibrated to resting rates, so a stronger synapse can rest the same, the biases
absorbing it, while passing more of a signal on. taste_trace.py found the resting brain's gain too low
at every step of rung 1's route: sugar's rise falls about 3-fold per synapse (25 to 7.5 Hz at the
first, 17 to 1.2 at the second, 13 to 0 at the third), and MN9's premotor inputs barely move. Here
escape_at_rest2.py's model (which passed) with every synapse's weight multiplied by m, recalibrated
from escape_at_rest2.py's eyes-open biases in 20 fresh-start rounds (k = 2 mV for 8 rounds, then 1 for
8, then 0.5 for 4), then measured:
  rest      10 s at grey, 8 flies: the brain's own mean rate, neurons over 100 Hz, neurons whose 1-s
            Fano factor passes 10 (bursting, as depression_rules.py counts it)
  ignition  the left looming loop, 32 flies, as ignition.py counts it
  taste     escape_at_rest.py's measures (MN9 L's rise under sugar at 100 and 10 Hz, and with bitter)
  looming   eyes_at_rest.py's tests at gain 1 on seed 1, and the giant fiber's rise
for m = 1 (escape_at_rest2.py's weight, recalibrated the same way), 1.5, 2 and 3. flyvis's release
reaches the brain through the same weight, so at m = 3 a loom at gain 1 lands as hard as one at gain
3 did.

    python experiments/taste_wsyn.py --m 1.5        (writes experiments/taste_wsyn/1.5.json; also 1, 2, 3)
    python experiments/taste_wsyn.py --report       (writes experiments/taste_wsyn.json)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

import escape_at_rest as escape
import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import ignition
import rest_calibration as attempt1
import rest_calibration2 as attempt2
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
MULTIPLIERS = [1.0, 1.5, 2.0, 3.0]
ROUNDS = [2.0] * 8 + [1.0] * 8 + [0.5] * 4


def condition(m: float) -> dict:
    t0 = time.perf_counter()
    attempt2.model, attempt1.network = escape.model, escape2.network
    eyes.ROUNDS, eyes.W_SYN = ROUNDS, W_SYN * m
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(escape2.HERE / "intact.npz")["bias"]
    log = s.calibrate()
    b, own = s.brain, ~s.fixed
    b.reset(77)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    c = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(10)])
    mean, var = c.mean((0, 1)), c.var(0).mean(0)
    fano = np.where(mean > 0.5, var / np.maximum(mean, 1e-9), np.nan)
    rest = {"mean_hz_own": round(float(mean[own].mean()), 3), "over_100hz": int((mean[own] > 100).sum()),
            "bursting_fano_over_10": int(np.nansum(fano[own] > 10))}
    hot = np.zeros(len(ignition.SEEDS) * eyes.TRIALS, bool)
    for seed in ignition.SEEDS:
        rates = s.run(lambda t: [], 1.0, seed, window=(eyes.SCENE - eyes.LATE, eyes.SCENE))["rates"]
        block = slice(ignition.SEEDS.index(seed) * eyes.TRIALS, (ignition.SEEDS.index(seed) + 1) * eyes.TRIALS)
        for name in s.cells:
            if name.split()[0] in ignition.LIMIT:
                hot[block] |= rates[:, s.cells[name]].mean(1) > ignition.LIMIT[name.split()[0]]
    v = eyes.loom_tests(s, 1.0, seed=1)
    out = {"m": m, "w_syn_mv": round(W_SYN * m, 4), "calibration": log[-1], "rest": rest,
           "ignited_flies": int(hot.sum()), "flies": len(hot), "taste": escape.taste(s),
           "looming": {k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")},
           "giant_fiber_rise_hz": {k: x["delta"] for k, x in v["escape"].items() if "near" not in k},
           "seconds": round(time.perf_counter() - t0)}
    HERE.mkdir(exist_ok=True)
    (HERE / f"{m:g}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out), flush=True)
    return out


def report() -> None:
    out = {"question": __doc__, "conditions": [json.loads((HERE / f"{m:g}.json").read_text()) for m in MULTIPLIERS
                                               if (HERE / f"{m:g}.json").exists()]}
    OUT.write_text(json.dumps(out, indent=1))
    for c in out["conditions"]:
        print(c["m"], c["calibration"]["groups_within_2x"], c["rest"], c["ignited_flies"], c["taste"], c["looming"], c["giant_fiber_rise_hz"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=float)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    report() if a.report else condition(a.m)


if __name__ == "__main__":
    main()
