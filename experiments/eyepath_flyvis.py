"""Does looming reach the looming detectors with flyvis's fitted optic lobe on MaleCNS wiring?

eyepath_2d.py showed a realistic looming disk to a real 2-D eye: the signal reached LC4 and LPLC2 on
the right side but only at about 1 Hz, with every optic lobe neuron on one hand-set graded
parameter set. Here the 54 flyvis cell types of the retina and optic lobe run flyvis's fitted
dynamics (brainfly.optic.FlyvisOpticLobe: 734 parameters trained by Lappalainen et al., on
MaleCNS's own neurons and synapses, each neuron's input per presynaptic type scaled to flyvis's
totals). Their output drives the rest of the MaleCNS network (FlyBrain, retina filled, other optic
lobe neurons graded at eyepath's gain 0.15 / release 0.3, everything else spiking).

Validation reported alongside (descriptive, run first): with ON edges (T4) and OFF edges (T5)
moving front-to-back, back-to-front, up and down across the right eye at 40 deg/s, the preferred
direction and direction selectivity index of T4a-d and T5a-d. Biology (Maisak et al. 2013): a
front-to-back, b back-to-front, c up, d down.

Scenes: eyepath_2d.py's (a dark disk 70 deg to either side at the horizon, r/v 0.4 s, capped at
45 deg; blank). Knob swept: how strongly flyvis's output drives its MaleCNS targets, gain in
{0.1, 0.3, 1, 3} (release change per unit change of relu(V)).
Pass criteria, fixed before the first run (all must hold), eyepath_2d.py's:
  REST    blank field: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; <= 5% of FlyBrain's own
          graded neurons at their release limits; neurons outside the optic lobe and retina at no more
          than 1.2 x their rate in the original all-spiking model
  RELAY   loomL raises left LC4 and left LPLC2 by >= 3 Hz each (t >= 4 over flies); loomR likewise on the right
  SIDE    loomL raises left LC4 and left LPLC2 more than their right copies, by >= 2 Hz (t >= 4); loomR mirrored
Secondary: ESCAPE (same-side DNp01 up >= 3 Hz and >= 2 Hz above the other side, t >= 4).
Sweep on seed 1 with 6 flies; the passing gain with the lowest value is re-run on seed 2 with 8 flies,
and only that confirmation counts.

    python experiments/eyepath_flyvis.py            (writes experiments/eyepath_flyvis.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.eye2d import CompoundEye, Edge
from brainfly.optic import GRADED as OPTIC, FlyvisOpticLobe
from eyepath import GRADED, SECONDS, STATIONS, WARM
from eyepath_2d import scenes
from eyepath_filled import N0, measure as measure_1d, verdict

OUT = Path(__file__).with_name("eyepath_flyvis.json")
GAINS = [0.1, 0.3, 1.0, 3.0]


def direction_selectivity(brain: FlyBrain, ol: FlyvisOpticLobe, eye: CompoundEye, speed: float = 40.0) -> dict:
    side = brain.side.astype(str)[ol.neurons]
    moves = {"front-to-back": ("azimuth", 20, -180, +1), "back-to-front": ("azimuth", -180, 20, -1),
             "upward": ("elevation", -90, 90, -1), "downward": ("elevation", 90, -90, +1)}   # right eye
    opposite = {"front-to-back": "back-to-front", "back-to-front": "front-to-back", "upward": "downward", "downward": "upward"}
    expected = {"a": "front-to-back", "b": "back-to-front", "c": "upward", "d": "downward"}
    peak = {}
    for polarity in (+1.0, -1.0):
        for name, (axis, a, b, behind) in moves.items():
            ol.reset()
            best = np.zeros(len(ol.neurons))
            for s in range(int((abs(b - a) / speed + 0.5) / brain.dt)):
                ol.step(eye.contrast([Edge(axis, a + np.sign(b - a) * speed * s * brain.dt, behind, polarity)]))
                best = np.maximum(best, np.maximum(ol.V, 0) - ol.rest)
            peak[(polarity, name)] = best
    out = {}
    for family, polarity in (("T4", +1.0), ("T5", -1.0)):
        for sub in "abcd":
            m = (ol.types == f"{family}{sub}") & (side == "R")
            r = {k: float(peak[(polarity, k)][m].mean()) for k in moves}
            pref = max(r, key=r.get)
            out[f"{family}{sub}"] = {"responses": {k: round(v, 3) for k, v in r.items()}, "preferred": pref,
                                     "dsi": round((r[pref] - r[opposite[pref]]) / (r[pref] + r[opposite[pref]] + 1e-9), 3),
                                     "expected": expected[sub], "correct": pref == expected[sub]}
    ol.reset()
    return out


def measure(brain, ol, eye, scene, seed, rest_pop, own_graded) -> dict:
    brain.reset(seed)
    ol.reset()
    steps, warm = int(SECONDS / brain.dt), int(WARM / brain.dt)
    B = brain.batch
    spikes = np.zeros((brain.n, B), np.float32)
    fv_release = np.zeros(len(ol.neurons))
    own_release = np.zeros((len(own_graded), B), np.float32)
    bounds = 0.0
    for s in range(steps):
        rel = ol.step(eye.contrast(scene(s * brain.dt)))
        brain.set_graded(ol.neurons, rel)
        fired = brain.step()
        if s < warm:
            continue
        for b, f in enumerate(fired):
            spikes[f, b] += 1
        fv_release += rel
        out = brain.graded_out[own_graded]
        own_release += out
        bounds += float(np.mean((out <= -brain.graded_release + 1e-6) | (out >= 1 - brain.graded_release - 1e-6)))
    window = (steps - warm) * brain.dt
    fv_pos = {int(i): k for k, i in enumerate(ol.neurons)}
    graded_pos = {int(i): k for k, i in enumerate(brain.graded)}
    own_pos = {int(r): k for k, r in enumerate(own_graded)}
    rates = {}
    for name, types in STATIONS.items():
        for side in "LR":
            idx = brain.cells(types, side)
            idx = idx[idx < N0]
            fv_rows = [fv_pos[int(i)] for i in idx if int(i) in fv_pos]
            if len(fv_rows) > len(idx) // 2:   # a flyvis station: its release change, the same in every fly
                v = fv_release[fv_rows].mean() / window
                rates[f"{name} {side}"] = [float(v)] * B
            elif int(idx[0]) in graded_pos:
                rates[f"{name} {side}"] = (own_release[[own_pos[graded_pos[int(i)]] for i in idx]].mean(0) / window).tolist()
            else:
                rates[f"{name} {side}"] = (spikes[idx].mean(0) / window).tolist()
    return {"rates": rates, "rest_pop_hz": float(spikes[rest_pop].mean() / window), "graded_at_bounds": bounds / (steps - warm)}


def run_config(brain, ol, eye, seed, rest_pop, rest_ref_hz, own_graded, sc) -> dict:
    m = {name: measure(brain, ol, eye, fn, seed, rest_pop, own_graded) for name, fn in sc.items()}
    v = verdict(m, rest_ref_hz)
    v["stations"] = {k: {name: round(float(np.mean(m[name]["rates"][k])), 3) for name in sc} for k in m["blank"]["rates"]}
    return v


def build(batch: int):
    brain = FlyBrain(batch=batch, graded=OPTIC, fill_retina=True)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisOpticLobe(brain)
    eye = CompoundEye(brain)
    own = np.flatnonzero(~np.isin(brain.graded, ol.neurons))     # rows of brain.graded that FlyBrain itself runs
    return brain, ol, eye, own


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "sweep": [], "confirm": None}
    ref = FlyBrain(batch=6)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic)
    from eyepath import SCENES as SCENES_1D
    rest_ref_hz = measure_1d(ref, SCENES_1D["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    del ref

    brain, ol, eye, own = build(6)
    results["flyvis_neurons"] = int(len(ol.neurons))
    results["direction_selectivity"] = ds = direction_selectivity(brain, ol, eye)
    print("direction selectivity:", {k: (v["preferred"], v["dsi"], "OK" if v["correct"] else "x") for k, v in ds.items()}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    sc = scenes()
    for gain in GAINS:
        t1 = time.perf_counter()
        ol.gain = gain
        v = run_config(brain, ol, eye, 1, rest_pop, rest_ref_hz, own, sc)
        results["sweep"].append({"gain": gain, **v})
        fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t']:.0f})" for k, x in d.items())
        print(f"gain {gain}: {'PASS' if v['pass'] else 'fail'}  REST {v['REST']} {v['rest_hz']} pop {v['rest_pop_hz']} "
              f"bounds {v['graded_at_bounds']} | RELAY {v['RELAY']} {fmt(v['relay'])} | SIDE {v['SIDE']} | "
              f"ESCAPE {v['ESCAPE']} {fmt(v['escape'])} ({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [r for r in results["sweep"] if r["pass"]]
    if passing:
        pick = min(passing, key=lambda r: r["gain"])
        brain, ol, eye, own = build(8)
        ol.gain = pick["gain"]
        v = run_config(brain, ol, eye, 2, rest_pop, rest_ref_hz, own, sc)
        results["confirm"] = {"gain": pick["gain"], **v}
        print(f"CONFIRM gain {pick['gain']}: {'PASS' if v['pass'] else 'FAIL'} REST {v['REST']} RELAY {v['RELAY']} "
              f"SIDE {v['SIDE']} ESCAPE {v['ESCAPE']}", flush=True)
    else:
        print("no gain passed the sweep; nothing to confirm", flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
