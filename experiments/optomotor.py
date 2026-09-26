"""Does a rotating drum reach the steering neurons? The optomotor pathway, open loop.

Before the brain steers the body (brainfly.body.Loop), its descending neurons have to carry a signal
to steer with. The classic test is the optomotor response: a fly turns with a drum rotating around
it. A drum rotating counterclockwise (seen from above) sweeps front-to-back across the left eye and
back-to-front across the right; the left HS cells, which prefer front-to-back motion in their own
eye (Schnell et al. 2010), depolarize, the right ones hyperpolarize, and the fly turns left, with
the drum. DNa02 on one side predicts turning to that side (Rayshubskiy et al. 2020).

Setup: eyepath_native.py's (FlyvisNative on the male eye driving FlyBrain at 2 ms steps, refractory
4 ms; the optic lobe types flyvis doesn't model graded at 0.15 / 0.3; everything else spiking,
including HS cells and descending neurons). The fly doesn't move (open loop).
Scenes, 2 s each, same noise in every scene (paired by fly), rates from 0.5 to 2 s:
  blank    grey
  static   a vertical sine grating, period 30 deg, contrast 1, not moving
  ccw      the grating rotating counterclockwise at 40 deg/s (1.3 Hz temporal frequency)
  cw       clockwise at 40 deg/s
Knob: FlyvisNative gain in {1, 3, 10}.
Pass criteria, fixed before the first run (all must hold at one gain):
  REST      blank: DNa02 <= 5 Hz on both sides; <= 5% of FlyBrain's own graded neurons at their
            release limits; neurons outside the optic lobe and retina at no more than 1.2 x their
            rate in the all-spiking FlyBrain at the same dt and refractory period
  HS        (HS left - HS right) is >= 3 Hz higher under ccw than under cw (t >= 4 over flies),
            HS being the mean rate of HSN, HSE and HSS on that side
  STEER     (DNa02 left - DNa02 right) is >= 2 Hz higher under ccw than under cw (t >= 4)
Secondary: the same STEER test for DNa01. A change identical in every fly counts as t = +/-inf when it
isn't zero. Descriptive: HS and H2 against blank and static; every descending neuron type's
direction signal ((left - right) under ccw minus under cw), ranked.
Sweep on seed 1 with 6 flies; the passing gain with the lowest value is re-run on seed 2 with 8 flies,
and only that confirmation counts.

    python experiments/optomotor.py            (writes experiments/optomotor.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.eye2d import Grating
from brainfly.optic import GRADED as OPTIC, FlyvisNative
from eyepath import GRADED, SCENES as SCENES_1D, WARM
from eyepath_fast import DT, REFRACTORY
from eyepath_filled import N0, measure as measure_1d
from eyepath_native import rises, stat

OUT = Path(__file__).with_name("optomotor.json")
SECONDS = 2.0
GAINS = [1.0, 3.0, 10.0]
PERIOD, SPEED = 30.0, 40.0
HS = ["HSN", "HSE", "HSS"]


def scenes() -> dict:
    return {"blank": lambda t: [], "static": lambda t: [Grating(PERIOD, 0.0)],
            "ccw": lambda t: [Grating(PERIOD, SPEED * t)], "cw": lambda t: [Grating(PERIOD, -SPEED * t)]}


def measure(brain, ol, scene, seed, rest_pop, own, groups) -> dict:
    """Per group of neurons, per side: mean rate (Hz) per fly over 0.5-2 s. Also the REST numbers."""
    brain.reset(seed)
    ol.reset()
    steps, warm = int(round(SECONDS / brain.dt)), int(round(WARM / brain.dt))
    B = brain.batch
    spikes = np.zeros((brain.n, B), np.float32)
    bounds = 0.0
    for s in range(steps):
        brain.set_graded(ol.neurons, ol.step(ol.contrast(scene(s * brain.dt))))
        fired = brain.step()
        if s < warm:
            continue
        for b, f in enumerate(fired):
            spikes[f, b] += 1
        out = brain.graded_out[own]
        bounds += float(np.mean((out <= -brain.graded_release + 1e-6) | (out >= 1 - brain.graded_release - 1e-6)))
    window = (steps - warm) * brain.dt
    rates = {f"{g} {s}": (spikes[idx].mean(0) / window).tolist() for g, sides in groups.items() for s, idx in sides.items()}
    return {"rates": rates, "rest_pop_hz": float(spikes[rest_pop].mean() / window), "graded_at_bounds": bounds / (steps - warm)}


def direction_signal(m, group) -> dict:
    lr = lambda sc: np.array(m[sc]["rates"][f"{group} L"]) - np.array(m[sc]["rates"][f"{group} R"])
    return stat(lr("ccw") - lr("cw"))


def run_config(brain, ol, seed, rest_pop, rest_ref_hz, own, groups, dn_types) -> dict:
    sc = scenes()
    m = {name: measure(brain, ol, fn, seed, rest_pop, own, groups) for name, fn in sc.items()}
    blank = m["blank"]
    ok_rest = (all(np.mean(blank["rates"][f"DNa02 {s}"]) <= 5 for s in "LR") and blank["graded_at_bounds"] <= 0.05
               and blank["rest_pop_hz"] <= 1.2 * rest_ref_hz)
    hs, steer, steer01 = direction_signal(m, "HS"), direction_signal(m, "DNa02"), direction_signal(m, "DNa01")
    v = {"pass": bool(ok_rest and rises(hs, 3) and rises(steer, 2)), "REST": bool(ok_rest), "HS": bool(rises(hs, 3)),
         "STEER": bool(rises(steer, 2)), "STEER_DNa01": bool(rises(steer01, 2)),
         "hs": hs, "steer": steer, "steer_DNa01": steer01,
         "rest_pop_hz": round(blank["rest_pop_hz"], 2), "rest_ref_hz": round(rest_ref_hz, 2),
         "graded_at_bounds": round(blank["graded_at_bounds"], 4),
         "groups": {k: {name: round(float(np.mean(m[name]["rates"][k])), 3) for name in sc} for k in blank["rates"]}}
    ranked = []
    for t in dn_types:
        d = direction_signal(m, t)
        ranked.append({"type": t, **d})
    tval = lambda x: np.inf if x["t"] == "inf" else (-np.inf if x["t"] == "-inf" else x["t"])
    ranked.sort(key=lambda x: -abs(x["delta"]))
    v["descending_ranked"] = ranked[:25]
    v["descending_significant"] = int(sum(abs(tval(x)) >= 4 and abs(x["delta"]) >= 2 for x in ranked))
    v["descending_tested"] = len(ranked)
    return v


def build(batch: int):
    brain = FlyBrain(batch=batch, graded=OPTIC, dt=DT, refractory=REFRACTORY)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisNative(brain)
    own = np.flatnonzero(~np.isin(brain.graded, ol.neurons))
    ct, sc = brain.cell_type.astype(str), brain.superclass.astype(str)
    dn_types = sorted({t for t in ct[sc == "descending_neuron"]
                       if all(len(brain.cells([t], s)) for s in "LR")})               # types present on both sides
    groups = {"HS": {s: brain.cells(HS, s) for s in "LR"}, "H2": {s: brain.cells(["H2"], s) for s in "LR"}}
    groups.update({t: {s: brain.cells([t], s) for s in "LR"} for t in dn_types})
    return brain, ol, own, groups, dn_types


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "sweep": [], "confirm": None}
    ref = FlyBrain(batch=6, dt=DT, refractory=REFRACTORY)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic)
    rest_ref_hz = measure_1d(ref, SCENES_1D["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    del ref
    brain, ol, own, groups, dn_types = build(6)
    results["descending_types"] = len(dn_types)
    tfmt = lambda x: x["t"] if isinstance(x["t"], str) else round(x["t"])
    for gain in GAINS:
        t1 = time.perf_counter()
        ol.gain = gain
        v = run_config(brain, ol, 1, rest_pop, rest_ref_hz, own, groups, dn_types)
        results["sweep"].append({"gain": gain, **v})
        top = ", ".join(f"{x['type']} {x['delta']:+.1f}(t{tfmt(x)})" for x in v["descending_ranked"][:5])
        print(f"gain {gain}: {'PASS' if v['pass'] else 'fail'} REST {v['REST']} pop {v['rest_pop_hz']} | "
              f"HS {v['HS']} {v['hs']['delta']:+.1f}(t{tfmt(v['hs'])}) | STEER {v['STEER']} {v['steer']['delta']:+.1f}(t{tfmt(v['steer'])}) | "
              f"DNa01 {v['steer_DNa01']['delta']:+.1f}(t{tfmt(v['steer_DNa01'])}) | significant DNs {v['descending_significant']}/"
              f"{v['descending_tested']} top: {top} ({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [r for r in results["sweep"] if r["pass"]]
    if passing:
        pick = min(passing, key=lambda r: r["gain"])
        brain, ol, own, groups, dn_types = build(8)
        ol.gain = pick["gain"]
        v = run_config(brain, ol, 2, rest_pop, rest_ref_hz, own, groups, dn_types)
        results["confirm"] = {"gain": pick["gain"], **v}
        print(f"CONFIRM gain {pick['gain']}: {'PASS' if v['pass'] else 'FAIL'} REST {v['REST']} HS {v['HS']} "
              f"STEER {v['STEER']}", flush=True)
    else:
        print("no gain passed the sweep; nothing to confirm", flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
