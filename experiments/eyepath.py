"""Does looming reach the looming detectors through the eyes once the retina and lamina are graded?

sweep.py found that the photoreceptor signal dies at the lamina. Photoreceptors inhibit L1-L3 (histamine),
and a lamina neuron that is silent at rest can't be inhibited any further, so a spiking model loses the
image there. In a real fly the retina and lamina are graded (non-spiking) neurons that release transmitter
continuously, so a change in light moves their release up or down. This runs the looming-escape pathway
with FlyBrain(graded=...):

    photoreceptors -> lamina -> medulla -> T4/T5, lobula -> LC4 / LPLC2 (looming detectors) -> DNp01 (giant fiber)

Graded sets (nested):
  spiking  nothing graded: the original model with Eyes.drive (sweep.py's setup), for reference
  lamina   photoreceptors (R1-6, R7, R8) and lamina neurons (L1-L5, Lawf1, Lawf2, Lai)
  optic    lamina plus every optic lobe intrinsic neuron (medulla, lobula, lobula plate, incl. T4/T5);
           visual projection neurons such as LC4 and LPLC2 still spike
Graded photoreceptors get Eyes.contrast (signed contrast against the blank background).
Knobs swept for each graded set: graded_gain in {0.05, 0.15, 0.5} x graded_release in {0.1, 0.3};
everything else at the FlyBrain defaults (tonic 0.14, gain 3.0, eye_gain 0.62, 20 ms steps).

Scenes, 2 s each, rates from 0.5 to 2 s, same noise in every scene (paired by fly):
  blank, loomL (dark object approaching on the left: sweep.py's stimulus), loomR (its mirror image).

Pass criteria, fixed before the first run (all must hold):
  REST    blank field: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; mean rate of all spiking
          neurons <= 5 Hz; <= 5% of graded neurons at the floor or ceiling of their release
  RELAY   loomL raises left LC4 and left LPLC2 by >= 3 Hz each (t >= 4 over flies); loomR the same on the right
  SIDE    loomL raises left LC4 and left LPLC2 more than their right copies, by >= 2 Hz (t >= 4); loomR mirrored
Secondary, reported but not part of the pass:
  ESCAPE  loomL raises left DNp01 by >= 3 Hz (t >= 4) and by >= 2 Hz more than right DNp01 (t >= 4); loomR mirrored
Sweep on one seed with 6 flies; for each graded set, the passing config with the lowest graded_gain (then
the lowest graded_release) is re-run on a fresh seed with 8 flies, and only that confirmation counts.

    python experiments/eyepath.py            (writes experiments/eyepath.json)
"""
from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.eyes import Eyes, blob_for

SECONDS, WARM = 2.0, 0.5
PHOTORECEPTORS = ["R1-6", "R7", "R8"]
LAMINA = ["L1", "L2", "L3", "L4", "L5", "Lawf1", "Lawf2", "Lai"]
GRADED = {"spiking": [], "lamina": PHOTORECEPTORS + LAMINA, "optic": PHOTORECEPTORS + LAMINA + ["ol_intrinsic"]}
GRADED_GAIN = [0.05, 0.15, 0.5]
GRADED_RELEASE = [0.1, 0.3]
SCENES = {
    "blank": lambda t: [],
    "loomL": lambda t: [blob_for(-110 + 45 * t, 30, 0.9)],
    "loomR": lambda t: [blob_for(110 - 45 * t, 30, 0.9)],
}
# Stations along the pathway, reported per side; the criteria use LC4, LPLC2 and DNp01.
STATIONS = {"R1-6": ["R1-6"], "L1": ["L1"], "L2": ["L2"], "Mi1": ["Mi1"], "Tm1": ["Tm1"], "Tm2": ["Tm2"],
            "T4": ["T4a", "T4b", "T4c", "T4d"], "T5": ["T5a", "T5b", "T5c", "T5d"],
            "LC4": ["LC4"], "LPLC2": ["LPLC2"], "DNp01": ["DNp01"], "DNa02": ["DNa02"]}


def measure(brain: FlyBrain, scene, contrast: bool, seed: int) -> dict:
    """One scene for every fly in the batch. Per station and side: spike rate (Hz) per fly, or for a
    graded station its mean release change from rest in spikes per second (Hz-equivalent)."""
    brain.reset(seed)
    eyes = Eyes(brain.azimuth)
    steps, warm = int(SECONDS / brain.dt), int(WARM / brain.dt)
    B = brain.batch
    counts = np.zeros((brain.n, B), np.float32)
    release = np.zeros((len(brain.graded), B), np.float32)
    bounds = 0.0
    for s in range(steps):
        blobs = scene(s * brain.dt)
        fired = brain.step(eyes.contrast(blobs) if contrast else eyes.drive(blobs))
        if s < warm:
            continue
        for b, f in enumerate(fired if B > 1 else [fired]):
            counts[f, b] += 1
        if len(brain.graded):
            out = brain.graded_out
            release += out
            bounds += float(np.mean((out <= -brain.graded_release + 1e-6) | (out >= 1 - brain.graded_release - 1e-6)))
    window = (steps - warm) * brain.dt
    graded_pos = {int(i): k for k, i in enumerate(brain.graded)}
    spiking = np.ones(brain.n, bool)
    spiking[brain.graded] = False
    rates = {}
    for name, types in STATIONS.items():
        for side in "LR":
            idx = brain.cells(types, side)
            if len(brain.graded) and idx[0] in graded_pos:   # stations are all graded or all spiking
                rows = [graded_pos[int(i)] for i in idx]
                rates[f"{name} {side}"] = (release[rows].mean(0) / window).tolist()
            else:
                rates[f"{name} {side}"] = (counts[idx].mean(0) / window).tolist()
    return {"rates": rates, "spiking_mean_hz": float(counts[spiking].mean() / window),
            "graded_at_bounds": bounds / (steps - warm) if len(brain.graded) else 0.0}


def stat(d: np.ndarray) -> dict:
    sd = d.std(ddof=1)
    return {"delta": round(float(d.mean()), 3), "t": round(float(d.mean() / (sd / np.sqrt(len(d)))), 2) if sd > 0 else 0.0}


def verdict(m: dict) -> dict:
    r = {scene: {k: np.array(v) for k, v in m[scene]["rates"].items()} for scene in SCENES}
    rest = m["blank"]
    ok_rest = (all(r["blank"][f"{st} {s}"].mean() <= 10 for st in ("LC4", "LPLC2") for s in "LR")
               and all(r["blank"][f"DNp01 {s}"].mean() <= 5 for s in "LR")
               and rest["spiking_mean_hz"] <= 5 and rest["graded_at_bounds"] <= 0.05)
    relay, side, escape = {}, {}, {}
    for scene, near, far in (("loomL", "L", "R"), ("loomR", "R", "L")):
        d = {k: r[scene][k] - r["blank"][k] for k in r[scene]}
        for st in ("LC4", "LPLC2", "DNp01"):
            up = stat(d[f"{st} {near}"])
            lateral = stat(d[f"{st} {near}"] - d[f"{st} {far}"])
            (escape if st == "DNp01" else relay)[f"{scene} {st}"] = up
            (escape if st == "DNp01" else side)[f"{scene} {st} near-far"] = lateral
    rises = lambda x, lo: x["delta"] >= lo and x["t"] >= 4
    ok_relay = all(rises(x, 3) for x in relay.values())
    ok_side = all(rises(x, 2) for x in side.values())
    ok_escape = all(rises(x, 3 if "near-far" not in k else 2) for k, x in escape.items())
    return {"REST": bool(ok_rest), "RELAY": bool(ok_relay), "SIDE": bool(ok_side), "pass": bool(ok_rest and ok_relay and ok_side),
            "ESCAPE": bool(ok_escape),
            "rest_hz": {k: round(float(r["blank"][k].mean()), 2) for k in ("LC4 L", "LC4 R", "LPLC2 L", "LPLC2 R", "DNp01 L", "DNp01 R")},
            "spiking_mean_hz": round(rest["spiking_mean_hz"], 2), "graded_at_bounds": round(rest["graded_at_bounds"], 4),
            "relay": relay, "side": side, "escape": escape}


def run_config(brain: FlyBrain, contrast: bool, seed: int) -> dict:
    m = {scene: measure(brain, fn, contrast, seed) for scene, fn in SCENES.items()}
    stations = {k: {scene: round(float(np.mean(m[scene]["rates"][k])), 2) for scene in SCENES} for k in m["blank"]["rates"]}
    return {**verdict(m), "stations": stations}


def show(label: str, v: dict, seconds: float) -> None:
    fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t']:.0f})" for k, x in d.items())
    print(f"{label:34s} {'PASS' if v['pass'] else 'fail'}  REST {v['REST']} {v['rest_hz']} all {v['spiking_mean_hz']} Hz "
          f"bounds {v['graded_at_bounds']}\n{'':36s}RELAY {v['RELAY']} {fmt(v['relay'])}\n{'':36s}SIDE {v['SIDE']} {fmt(v['side'])}\n"
          f"{'':36s}ESCAPE {v['ESCAPE']} {fmt(v['escape'])}  ({seconds:.0f} s)", flush=True)


def main() -> None:
    out = Path(__file__).with_suffix(".json")
    results = {"criteria": __doc__, "sweep": [], "confirm": {}}
    for name, graded in GRADED.items():
        brain = FlyBrain(batch=6, graded=graded)
        grid = [(None, None)] if not graded else list(itertools.product(GRADED_GAIN, GRADED_RELEASE))
        for gain, release in grid:
            t0 = time.perf_counter()
            if graded:
                brain.graded_gain, brain.graded_release = gain, release
            v = run_config(brain, contrast=bool(graded), seed=1)
            results["sweep"].append({"graded": name, "graded_gain": gain, "graded_release": release, **v})
            show(f"{name} gain {gain} release {release}", v, time.perf_counter() - t0)
            out.write_text(json.dumps(results, indent=1))
        passing = [r for r in results["sweep"] if r["graded"] == name and r["pass"]]
        if not graded or not passing:
            print(f"{name}: {'reference only' if not graded else 'no config passed the sweep; nothing to confirm'}", flush=True)
            continue
        pick = min(passing, key=lambda r: (r["graded_gain"], r["graded_release"]))
        print(f"\n{name}: confirming gain {pick['graded_gain']} release {pick['graded_release']} on a fresh seed, 8 flies", flush=True)
        t0 = time.perf_counter()
        brain = FlyBrain(batch=8, graded=graded)
        brain.graded_gain, brain.graded_release = pick["graded_gain"], pick["graded_release"]
        v = run_config(brain, contrast=True, seed=2)
        results["confirm"][name] = {"graded_gain": pick["graded_gain"], "graded_release": pick["graded_release"], **v}
        show(f"CONFIRM {name}", v, time.perf_counter() - t0)
        out.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
