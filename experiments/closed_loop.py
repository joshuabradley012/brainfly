"""Closing the loop: does the brain turn the body with a rotating drum?

optomotor.py found, open loop, that a rotating drum seen through FlyvisNative drives the HS cells
and the steering neuron DNa02 with the biological signs. Here the brain steers a body: NeuroMechFly
(FlyGym 2.1) walks on flat ground inside the drum under FlyGym's hybrid turning controller, and
brainfly.body.Loop sets the controller's two drives from DNa02 (drives 1 -/+ 0.05 x the left-minus-
right DNa02 rate change from baseline, in Hz, filtered with a 0.1 s time constant: fixed in advance,
not fitted). The loop is closed: as the fly turns, the drum moves across its eyes accordingly.
Brain as in optomotor.py (FlyBrain at 2 ms steps, refractory 4 ms; FlyvisNative at gain 1, the
lowest gain that passed there), one fly per run, eight flies (seeds 1-8).
Conditions per fly, each 0.5 s of baseline (static drum, walking at drive 1 on both sides; sets the
DNa02 baseline) then 3 s measured:
  ccw      the drum (sine grating, period 30 deg, contrast 1) rotating counterclockwise at 40 deg/s
  cw       clockwise at 40 deg/s
  static   not rotating
  ccw-cut, cw-cut   the same with the brain's link to the body cut (drives stay at 1)
Measure: the fly's mean yaw velocity over the 3 s (heading change / 3 s; positive counterclockwise).
Pass criterion, fixed before the first run:
  TURN   yaw velocity under ccw minus under cw >= 10 deg/s (t >= 4 over flies, paired by fly): the
         fly turns with the drum
Descriptive: the same difference with the link cut (a pipeline check: the body then ignores the
brain, so ccw and cw should give identical paths); static against the mean of ccw and cw; DNa02
rates; LC4, LPLC2 and DNp01 spikes; distance walked. A change identical in every fly counts as
t = +/-inf when it isn't zero.

    python experiments/closed_loop.py            (writes experiments/closed_loop.json)
    python experiments/closed_loop.py rung3eye   (the same with rung 3's eye, brainfly.optic.EYE: closed_loop_rung3eye.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.body import Body, Drum, Loop
from brainfly.optic import EYE, GRADED as OPTIC, MODEL, FlyvisNative
from eyepath_fast import DT, REFRACTORY
from eyepath_native import rises, stat

OUT = Path(__file__).with_name("closed_loop.json")
EYE_MODEL = MODEL                                   # flyvis's model 000, as it first ran
if sys.argv[1:] == ["rung3eye"]:                    # rung 3's eye instead
    EYE_MODEL, OUT = EYE, OUT.with_name("closed_loop_rung3eye.json")
FLIES = range(1, 9)
SECONDS, BASELINE = 3.0, 0.5
OPTIC_GAIN, STEER_GAIN = 1.0, 0.05
CONDITIONS = {"ccw": (40.0, STEER_GAIN), "cw": (-40.0, STEER_GAIN), "static": (0.0, STEER_GAIN),
              "ccw-cut": (40.0, 0.0), "cw-cut": (-40.0, 0.0)}


def run_fly(brain, ol, body, seed) -> dict:
    out = {}
    for name, (speed, gain) in CONDITIONS.items():
        body.reset(seed)
        loop = Loop(brain, ol, body, arena=[Drum(period=30.0, speed=speed)], gain=gain)
        rec = loop.run(SECONDS, baseline=BASELINE, seed=seed)
        h = np.unwrap(np.array(rec["heading"]))
        out[name] = {"yaw_deg_s": float(np.degrees(h[-1] - h[0]) / (rec["t"][-1] - rec["t"][0])),
                     "distance_mm": float(np.sum(np.hypot(np.diff(rec["x"]), np.diff(rec["y"])))),
                     "dna02_hz": {"L": float(np.mean(rec["steer_left_hz"])), "R": float(np.mean(rec["steer_right_hz"])),
                                  "rest": rec["steer_rest_hz"]},
                     "spikes": {k: int(np.sum(rec[k])) for k in loop.watch},
                     "heading_deg": np.round(np.degrees(h[::25]), 1).tolist()}
    return out


def main() -> None:
    t0 = time.perf_counter()
    brain = FlyBrain(batch=1, graded=OPTIC, dt=DT, refractory=REFRACTORY)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisNative(brain, model=EYE_MODEL, gain=OPTIC_GAIN)
    body = Body(control_dt=DT)
    flies = {}
    for seed in FLIES:
        t1 = time.perf_counter()
        flies[seed] = r = run_fly(brain, ol, body, seed)
        print(f"fly {seed}: yaw deg/s " + " ".join(f"{k} {v['yaw_deg_s']:+.1f}" for k, v in r.items())
              + f" | DNa02 ccw L/R {r['ccw']['dna02_hz']['L']:.1f}/{r['ccw']['dna02_hz']['R']:.1f} Hz ({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps({"criteria": __doc__, "eye": EYE_MODEL, "flies": flies}, indent=1))
    yaw = {k: np.array([flies[s][k]["yaw_deg_s"] for s in FLIES]) for k in CONDITIONS}
    turn = stat(yaw["ccw"] - yaw["cw"])
    cut = stat(yaw["ccw-cut"] - yaw["cw-cut"])
    result = {"TURN": bool(rises(turn, 10)), "turn": turn, "cut": cut,
              "static_vs_moving": stat(yaw["static"] - (yaw["ccw"] + yaw["cw"]) / 2),
              "mean_yaw_deg_s": {k: round(float(v.mean()), 2) for k, v in yaw.items()}}
    result["pass"] = result["TURN"]
    print(f"{'PASS' if result['pass'] else 'FAIL'}: TURN {turn} | link cut {cut} | "
          f"mean yaw {result['mean_yaw_deg_s']}", flush=True)
    OUT.write_text(json.dumps({"criteria": __doc__, "eye": EYE_MODEL, "result": result, "flies": flies,
                               "seconds": round(time.perf_counter() - t0)}, indent=1))


if __name__ == "__main__":
    main()
