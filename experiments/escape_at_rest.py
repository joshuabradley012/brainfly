"""Does the resting brain escape? eyes_at_rest.py again, with short-term depression set by synapse class
from the literature instead of everywhere (pre-registered).

eyes_at_rest.py failed on the escape neuron alone: in rung 4's resting brain (rest_calibration2.py),
looming drove LC4 and LPLC2 by 17-61 Hz, but the giant fiber rose only 2-4 Hz. depression_rules.py
traced that to the ORN-to-PN depression applied to every cholinergic synapse, which caps what a fast
input passes on at about 5 spikes/s. research_notes/Rung 4 resting state data/short_term_plasticity.md
surveyed where depression is measured. It assigns it by presynaptic class. This test takes its rule,
with the fallback the notes give if loops persist (central recovery 0.5 s instead of 0.2), and does
nothing else. Exploratory pilots (rates, bursting, taste and looming at gain 1 on seed 1; FC and the
bump never computed) chose that fallback: at 0.2 s the resting brain failed REST, at 0.5 s it passed.
Model: rest_calibration2.py's per-type properties (reset 5 mV below rest; thresholds of 10 mV for
projection and lateral-horn neurons, 16 for Kenyon cells), with depression, as fraction of strength
left per spike / recovery time constant, by presynaptic class, later entries overriding earlier ones:
  every cholinergic neuron                                     0.9 / 0.5 s
  sensory neurons other than olfactory, thermo- and hygroreceptor ones; visual projection neurons;
  descending neurons                                           none
  olfactory, thermo- and hygroreceptor neurons (ORN_*, TRN_*, HRN_*)   0.78 / 0.9 s
  uniglomerular projection neurons                             0.85 / 0.8 s
  Kenyon cells                                                 0.5 / 1.5 s
flyvis's eyes (model 001) as in eyes_at_rest.py, recalibrated with the eyes open as it does (12
fresh-start rounds from its biases), and eyes_at_rest.py's scenes, tests (REST, RELAY, SIDE, ESCAPE),
gain sweep {1, 3, 10} on seed 1, confirmation of the lowest passing gain on seed 2, and NULL (in 2
degree-preserving rewirings, recalibrated the same way from rest_calibration2.py's rewired biases,
ESCAPE fails for both looms). Pass: the confirmation passes and NULL holds.
Reported, not gating: the drum's HS and DNa02 signals at each gain; rung 1's taste tests
(taste_at_rest.py's SUGAR, RESPONSE, BITTER measures, 8 trials) in this brain.

    python experiments/escape_at_rest.py            (writes experiments/escape_at_rest.json)
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rest_calibration2 as attempt2
from brainfly.hybrid import consensus_transmitters
from shiu_baseline import SETS

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
ATTEMPT2_MODEL = attempt2.model


def model(types: np.ndarray, superclass: np.ndarray) -> tuple[dict, dict]:
    spec, sets = ATTEMPT2_MODEL(types, superclass)
    ach = consensus_transmitters() == "acetylcholine"
    sensory = np.char.find(superclass, "sensory") >= 0
    orn = np.char.startswith(types, "ORN_") | np.char.startswith(types, "TRN_") | np.char.startswith(types, "HRN_")
    upn = np.array([bool(re.search(r"_[a-z]*PN$", t)) for t in types])
    undepressed = (sensory & ~orn) | (superclass == "visual_projection") | np.char.startswith(superclass, "descending_neuron")
    del spec["cholinergic"]
    spec.update({"cholinergic": {"depression": 0.9, "recovery": 0.5}, "undepressed": {"depression": 1.0},
                 "orn": {"depression": 0.78, "recovery": 0.9}, "upn": {"depression": 0.85, "recovery": 0.8},
                 "kc": {"depression": 0.5, "recovery": 1.5}})
    sets = {"cholinergic": np.flatnonzero(ach), "undepressed": np.flatnonzero(ach & undepressed),
            "orn": np.flatnonzero(ach & orn), "upn": np.flatnonzero(ach & upn),
            "kc": np.flatnonzero(ach & np.char.startswith(types, "KC"))}
    return spec, sets


def taste(s: eyes.Setup) -> dict:
    """taste_at_rest.py's measures (MN9 L's rise over its rest under 1 s of taste drive at 100 Hz)."""
    b = s.brain
    mn9 = b.cells(["MN9"], "L")
    cells = {k: b.cells(v, "L") for k, v in SETS.items()}

    def rise(drive, seed):
        b.reset(seed)
        b.set_release(s.ol.neurons, s.silent)
        b.advance(int(round(0.5 / b.dt)))
        before = b.advance(int(round(0.5 / b.dt)))[:, mn9].mean(1) / 0.5
        return b.advance(int(round(1.0 / b.dt)), drive=drive)[:, mn9].mean(1) - before       # per trial
    r = {"sugar": rise([(cells["sugar"], 100.0)], 1), "sugar 10 Hz": rise([(cells["sugar"], 10.0)], 5),
         "sugar+bitter": rise([(cells["sugar"], 100.0), (cells["bitter"], 100.0)], 3)}
    out = {k: round(float(v.mean()), 2) for k, v in r.items()}
    out["SUGAR"] = bool(r["sugar"].mean() >= 10 and r["sugar"].mean() / (r["sugar"].std(ddof=1) / np.sqrt(len(r["sugar"]))) >= 4)
    return out


def main() -> None:
    t0 = time.perf_counter()
    attempt2.model = model
    eyes.HERE = HERE
    HERE.mkdir(exist_ok=True)
    results = {"criteria": __doc__, "model": eyes.MODEL, "sweep": [], "drum": {}, "confirm": None, "nulls": []}
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(Path(__file__).with_name("eyes_at_rest") / "intact.npz")["bias"]
    results["calibration"] = s.calibrate()
    np.savez_compressed(HERE / "intact.npz", groups=s.names, bias=s.bias)
    results["taste"] = taste(s)
    print("taste:", results["taste"], flush=True)
    for gain in eyes.GAINS:
        v = eyes.loom_tests(s, gain, seed=1)
        results["sweep"].append(v)
        eyes.show(f"gain {gain}", v)
        results["drum"][str(gain)] = d = eyes.drum(s, gain, seed=1)
        print(f"  drum: HS {d['HS_signal_hz']:+.1f} Hz, DNa02 {d['DNa02_signal_hz']:+.2f} Hz", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [v["gain"] for v in results["sweep"] if v["pass"]]
    if not passing:
        results["pass"] = False
        print("FAIL: no gain passes the sweep", flush=True)
    else:
        gain = min(passing)
        results["confirm"] = v = eyes.loom_tests(s, gain, seed=2)
        eyes.show(f"CONFIRM gain {gain}", v)
        for k in (1, 2):
            null = eyes.Setup(k, seed=50 + k)
            log = null.calibrate()
            n = eyes.loom_tests(null, gain, seed=2)
            results["nulls"].append({"rewiring": k, "calibration": log[-1], **{f: n[f] for f in ("escape", "relay", "ESCAPE", "RELAY", "own_mean_hz")}})
            print(f"  rewiring {k}: ESCAPE {n['ESCAPE']}, RELAY {n['RELAY']}", flush=True)
        results["NULL"] = not any(n["ESCAPE"] for n in results["nulls"])
        results["pass"] = bool(v["pass"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
