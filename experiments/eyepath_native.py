"""Does flyvis, run on its own terms, carry looming to LC4, LPLC2 and the giant fiber?

eyepath_fast.py found LC4 nearly unmoved by looms of any speed with flyvis ported onto MaleCNS wiring,
and flyvis_port.py traced that to the port's shifted operating point. brainfly.optic.FlyvisNative runs
flyvis's own network, tiled onto the male eye and validated in flyvis_native.py (it rebuilds flyvis
exactly; all 16 T4/T5 subtypes prefer their biological direction). Here it drives the rest of the
MaleCNS network (FlyBrain at 2 ms steps, refractory 4 ms; the optic lobe types flyvis doesn't model
graded at 0.15 / 0.3; everything else spiking), with eyepath_fast.py's scenes and windows:
  blank; fastL/R (a dark disk 70 deg to one side, r/v 0.04 s, contact 1.8 s, angular radius capped
  at 45 deg); slowL/R (r/v 0.4 s, contact 2.2 s). FULL window 0.5-2.0 s, LATE 1.5-2.0 s.
Knob: gain in {0.3, 1, 3, 10} (release change per unit change of relu(V), per 20 ms).
Pass criteria, fixed before the first run (all must hold at one gain), eyepath_fast.py's primary ones:
  REST   blank, FULL window: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; <= 5% of
         FlyBrain's own graded neurons at their release limits; neurons outside the optic lobe and
         retina at no more than 1.2 x their rate in the all-spiking FlyBrain at the same dt and
         refractory period
  RELAY  in LATE, fastL raises left LC4 and left LPLC2 by >= 3 Hz each over blank (t >= 4 over
         flies); fastR likewise on the right
  SIDE   in LATE, fastL raises left LC4 and LPLC2 more than their right copies, by >= 2 Hz (t >= 4);
         fastR mirrored
Secondary: ESCAPE (in LATE, the same side's DNp01 up >= 3 Hz and >= 2 Hz above the other side,
t >= 4). One change from eyepath_fast.py, fixed here in advance: a change identical in every fly
(zero variance) counts as t = +/-infinity when it isn't zero, rather than t = 0.
Descriptive: the slow looms in the FULL window; SPEED (LC4's rise, fast minus slow, in LATE); the
time courses; the same numbers from eyepath_fast.py's port for comparison.
Sweep on seed 1 with 6 flies; the passing gain with the lowest value is re-run on seed 2 with 8 flies,
and only that confirmation counts.

    python experiments/eyepath_native.py            (writes experiments/eyepath_native.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.optic import GRADED as OPTIC, FlyvisNative
from eyepath import GRADED, SCENES as SCENES_1D
from eyepath_fast import DT, REFRACTORY, WINDOWS, measure, scenes
from eyepath_filled import N0, measure as measure_1d

OUT = Path(__file__).with_name("eyepath_native.json")
GAINS = [0.3, 1.0, 3.0, 10.0]


def stat(d) -> dict:
    d = np.asarray(d, float)
    sd = d.std(ddof=1)
    if sd > 0:
        t = round(float(d.mean() / (sd / np.sqrt(len(d)))), 2)
    else:                                   # the same change in every fly
        t = "inf" if d.mean() > 0 else ("-inf" if d.mean() < 0 else 0.0)
    return {"delta": round(float(d.mean()), 3), "t": t}


def rises(x: dict, lo: float) -> bool:
    t = x["t"]
    t = np.inf if t == "inf" else (-np.inf if t == "-inf" else t)
    return x["delta"] >= lo and t >= 4


def verdict(blank_full, blank_late, m_late, rest_ref_hz) -> dict:
    """REST from the blank's FULL window; RELAY, SIDE and ESCAPE from the fast looms in LATE."""
    r = {k: np.array(v) for k, v in blank_full["rates"].items()}
    ok_rest = (all(r[f"{st} {s}"].mean() <= 10 for st in ("LC4", "LPLC2") for s in "LR")
               and all(r[f"DNp01 {s}"].mean() <= 5 for s in "LR")
               and blank_full["graded_at_bounds"] <= 0.05 and blank_full["rest_pop_hz"] <= 1.2 * rest_ref_hz)
    b = {k: np.array(v) for k, v in blank_late["rates"].items()}
    relay, side, escape = {}, {}, {}
    for scene, near, far in (("fastL", "L", "R"), ("fastR", "R", "L")):
        d = {k: np.array(v) - b[k] for k, v in m_late[scene]["rates"].items()}
        for st in ("LC4", "LPLC2", "DNp01"):
            (escape if st == "DNp01" else relay)[f"{scene} {st}"] = stat(d[f"{st} {near}"])
            (escape if st == "DNp01" else side)[f"{scene} {st} near-far"] = stat(d[f"{st} {near}"] - d[f"{st} {far}"])
    ok_relay = all(rises(x, 3) for x in relay.values())
    ok_side = all(rises(x, 2) for x in side.values())
    ok_escape = all(rises(x, 3 if "near-far" not in k else 2) for k, x in escape.items())
    return {"pass": bool(ok_rest and ok_relay and ok_side), "REST": bool(ok_rest), "RELAY": bool(ok_relay),
            "SIDE": bool(ok_side), "ESCAPE": bool(ok_escape),
            "rest_hz": {k: round(float(r[k].mean()), 2) for k in ("LC4 L", "LC4 R", "LPLC2 L", "LPLC2 R", "DNp01 L", "DNp01 R")},
            "rest_pop_hz": round(blank_full["rest_pop_hz"], 2), "rest_ref_hz": round(rest_ref_hz, 2),
            "graded_at_bounds": round(blank_full["graded_at_bounds"], 4), "relay": relay, "side": side, "escape": escape}


def run_config(brain, ol, seed, rest_pop, rest_ref_hz, own, sc) -> dict:
    m = {name: measure(brain, ol, ol, fn, seed, rest_pop, own) for name, fn in sc.items()}
    v = verdict(m["blank"]["full"], m["blank"]["late"], {k: m[k]["late"] for k in ("fastL", "fastR")}, rest_ref_hz)
    bf = {k: np.array(x) for k, x in m["blank"]["full"]["rates"].items()}
    bl = {k: np.array(x) for k, x in m["blank"]["late"]["rates"].items()}
    v["slow_full"] = {f"{sc_} {st}": stat(np.array(m[sc_]["full"]["rates"][f"{st} {sc_[-1]}"]) - bf[f"{st} {sc_[-1]}"])
                      for sc_ in ("slowL", "slowR") for st in ("LC4", "LPLC2", "DNp01")}
    v["speed"] = {f"LC4 {s} fast-slow": stat(np.array(m[f"fast{s}"]["late"]["rates"][f"LC4 {s}"])
                                             - np.array(m[f"slow{s}"]["late"]["rates"][f"LC4 {s}"])) for s in "LR"}
    v["stations"] = {w: {k: {name: round(float(np.mean(m[name][w]["rates"][k])), 3) for name in sc}
                         for k in m["blank"][w]["rates"]} for w in WINDOWS}
    v["trace_hz"] = {name: m[name]["trace_hz"] for name in sc}
    return v


def build(batch: int):
    brain = FlyBrain(batch=batch, graded=OPTIC, dt=DT, refractory=REFRACTORY)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisNative(brain)
    own = np.flatnonzero(~np.isin(brain.graded, ol.neurons))     # rows of brain.graded that FlyBrain itself runs
    return brain, ol, own


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "sweep": [], "confirm": None}
    ref = FlyBrain(batch=6, dt=DT, refractory=REFRACTORY)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic)
    rest_ref_hz = measure_1d(ref, SCENES_1D["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    print(f"REST reference (all-spiking, 2 ms, refractory 4 ms): {rest_ref_hz:.2f} Hz", flush=True)
    del ref

    brain, ol, own = build(6)
    results["flyvis_native"] = {"cells": len(ol.cell_type), "driven": len(ol.neurons)}
    sc = scenes()
    fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t'] if isinstance(x['t'], str) else round(x['t'])})" for k, x in d.items())
    for gain in GAINS:
        t1 = time.perf_counter()
        ol.gain = gain
        v = run_config(brain, ol, 1, rest_pop, rest_ref_hz, own, sc)
        results["sweep"].append({"gain": gain, **v})
        print(f"gain {gain}: {'PASS' if v['pass'] else 'fail'}  REST {v['REST']} {v['rest_hz']} pop {v['rest_pop_hz']} "
              f"bounds {v['graded_at_bounds']} | RELAY {v['RELAY']} {fmt(v['relay'])} | SIDE {v['SIDE']} | "
              f"ESCAPE {v['ESCAPE']} {fmt(v['escape'])} | SPEED {fmt(v['speed'])} | slow FULL {fmt(v['slow_full'])} "
              f"({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [r for r in results["sweep"] if r["pass"]]
    if passing:
        pick = min(passing, key=lambda r: r["gain"])
        brain, ol, own = build(8)
        ol.gain = pick["gain"]
        v = run_config(brain, ol, 2, rest_pop, rest_ref_hz, own, sc)
        results["confirm"] = {"gain": pick["gain"], **v}
        print(f"CONFIRM gain {pick['gain']}: {'PASS' if v['pass'] else 'FAIL'} REST {v['REST']} RELAY {v['RELAY']} "
              f"{fmt(v['relay'])} SIDE {v['SIDE']} ESCAPE {v['ESCAPE']} {fmt(v['escape'])}", flush=True)
    else:
        print("no gain passed the sweep; nothing to confirm", flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
