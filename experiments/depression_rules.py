"""Exploratory, not pre-registered: which short-term depression rule keeps the resting brain calm and
still lets sensory signals through?

eyes_at_rest.py and taste_at_rest.py found rung 4's resting brain (rest_calibration2.py: the ORN-to-PN
depression, 0.78 of the strength left per spike and 0.89 s to recover, at every cholinergic synapse)
calm, but unable to pass looming on to the giant fiber or sugar to MN9. Each rule below starts from
eyes_at_rest.py's setup (flyvis's eyes, model 001, the eyes-open biases), is recalibrated from fresh
starts (10 rounds), and is then measured, 8 flies each:
  rest     10 s at grey: the brain's own mean rate, neurons over 100 Hz, neurons whose 1-s Fano
           factor passes 10 (bursting), and the median Fano factor of the central-complex types that
           burst in attempt 1
  taste    MN9 L's rise over rest under 1 s of sugar at 100 Hz, at 10 Hz, and with bitter
  looming  eyes_at_rest.py's tests at gain 1 (REST, RELAY, SIDE, ESCAPE) and the giant fiber's rise
Rules: as in rest_calibration2.py; without depression on LC4's and LPLC2's outputs; depression only
at central-brain intrinsic neurons' synapses; recovering in 0.1 s instead of 0.89; leaving 0.9 of the
strength instead of 0.78.

    python experiments/depression_rules.py            (writes experiments/depression_rules.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rest_calibration2 as attempt2
from shiu_baseline import SETS

OUT = Path(__file__).with_suffix(".json")
RULES = ["as attempt 2", "LC4 and LPLC2 undepressed", "central-brain intrinsic only", "fast recovery (0.1 s)", "milder (0.9)"]
ORIGINAL = attempt2.model                  # each rule changes this, never the rule before it


def rule_model(rule: str):
    def model(types, superclass):
        spec, sets = ORIGINAL(types, superclass)
        if rule == "LC4 and LPLC2 undepressed":
            for t in ("LC4", "LPLC2"):
                spec[t] = {**spec.get(t, {}), "depression": 1.0}
        elif rule == "central-brain intrinsic only":
            sets["cholinergic"] = np.intersect1d(sets["cholinergic"], np.flatnonzero(superclass == "cb_intrinsic"))
        elif rule == "fast recovery (0.1 s)":
            spec["cholinergic"] = {"depression": 0.78, "recovery": 0.1}
        elif rule == "milder (0.9)":
            spec["cholinergic"] = {"depression": 0.9, "recovery": 0.89}
        return spec, sets
    return model


def measure(rule: str) -> dict:
    attempt2.model = rule_model(rule)
    eyes.ROUNDS = [1.0] * 6 + [0.5] * 4
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(eyes.HERE / "intact.npz")["bias"]
    log = s.calibrate()
    b, own = s.brain, ~s.fixed
    b.reset(77)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    c = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(10)])
    mean, var = c.mean((0, 1)), c.var(0).mean(0)
    fano = np.where(mean > 0.5, var / np.maximum(mean, 1e-9), np.nan)
    rest = {"mean_hz_own": round(float(mean[own].mean()), 3), "over_100hz": int((mean[own] > 100).sum()),
            "bursting_fano_over_10": int(np.nansum(fano[own] > 10)),
            "cx_median_fano": {t: round(float(np.nanmedian(fano[s.types == t])), 1) for t in ("FR1", "LNO1", "PFNv")}}
    mn9, sugar, bitter = b.cells(["MN9"], "L"), b.cells(SETS["sugar"], "L"), b.cells(SETS["bitter"], "L")

    def taste(drive, seed):
        b.reset(seed)
        b.set_release(s.ol.neurons, s.silent)
        b.advance(int(round(0.5 / b.dt)))
        before = b.advance(int(round(0.5 / b.dt)))[:, mn9].mean() / 0.5
        return float(b.advance(int(round(1.0 / b.dt)), drive=drive)[:, mn9].mean() - before)
    tastes = {"sugar": taste([(sugar, 100.0)], 1), "sugar 10 Hz": taste([(sugar, 10.0)], 5),
              "sugar+bitter": taste([(sugar, 100.0), (bitter, 100.0)], 3)}
    v = eyes.loom_tests(s, 1.0, seed=1)
    return {"rule": rule, "calibration": log[-1], "rest": rest, "taste_rise_hz": {k: round(x, 2) for k, x in tastes.items()},
            "looming": {k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")},
            "giant_fiber_rise_hz": {k: x["delta"] for k, x in v["escape"].items() if "near" not in k},
            "lc4_rise_hz": {k: x["delta"] for k, x in v["relay"].items() if "LC4" in k}}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "rules": []}
    for rule in RULES:
        out["rules"].append(r := measure(rule))
        print(json.dumps(r), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
