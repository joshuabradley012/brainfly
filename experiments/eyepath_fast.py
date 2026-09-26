"""Is LC4 held back by the slow loom? A fast loom, at 2 ms steps.

eyepath_flyvis.py showed a slowly approaching dark disk (r/v 0.4 s) to flyvis's optic lobe on
MaleCNS wiring. At the strongest coupling tried (gain 3) the same side's LPLC2 rose 3.4-5.1 Hz, but
LC4 only 0.7 Hz and the giant fiber (DNp01) 1.4-1.7 Hz. In real flies LPLC2 signals how big a
looming object is and LC4 how fast it expands, and the giant fiber's fast escape follows fast looms
(von Reyn et al. 2017; Ache et al. 2019). A disk ten times faster (r/v 0.04 s) grows through most of
its size in the last 100 ms before contact, which 20 ms steps can't resolve, so everything here runs
at 2 ms: FlyBrain(dt=0.002, refractory=0.004), the README's setting that matches the 20 ms brain's
resting descending-neuron rate, and the flyvis optic lobe stepped at 2 ms (flyvis trains at 20 ms
and evaluates its own stimuli at 5 ms). Graded release is expressed per 20 ms, so a gain means the
same coupling as in eyepath_flyvis.py. Otherwise the setup is eyepath_flyvis.py's: retina filled,
flyvis on its 54 types, the rest of the optic lobe graded at 0.15 / 0.3, everything else spiking.

Scenes, 2 s each, same noise in every scene (paired by fly):
  blank
  fastL    a dark disk (90% darker) 70 deg to the left at the horizon, approaching with r/v 0.04 s,
           contact at 1.8 s, angular radius capped at 45 deg: 7.6 deg at 1.5 s, 45 deg from 1.76 s
  fastR    its mirror image
  slowL/R  eyepath_flyvis.py's looms (r/v 0.4 s, contact 2.2 s, capped at 45 deg: 30 deg at 1.5 s,
           45 deg from 1.8 s)
Windows: FULL 0.5-2.0 s (eyepath_flyvis.py's); LATE 1.5-2.0 s (the fast disk's expansion, then 0.24 s
at full size).
Knob: flyvis's coupling to its MaleCNS targets, gain in {1, 3, 10}.
Pass criteria, fixed before the first run (all must hold at one gain):
  REST   blank, FULL window: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; <= 5% of
         FlyBrain's own graded neurons at their release limits; neurons outside the optic lobe and
         retina at no more than 1.2 x their rate in the all-spiking FlyBrain at the same dt and
         refractory period
  RELAY  in LATE, fastL raises left LC4 and left LPLC2 by >= 3 Hz each over blank (t >= 4 over
         flies); fastR likewise on the right
  SIDE   in LATE, fastL raises left LC4 and LPLC2 more than their right copies, by >= 2 Hz (t >= 4);
         fastR mirrored
  SPEED  in LATE, the same side's LC4 rises >= 2 Hz more for the fast loom than for the slow one
         (t >= 4), on both sides
Secondary: ESCAPE (in LATE, the same side's DNp01 up >= 3 Hz and >= 2 Hz above the other side, t >= 4).
Descriptive: the slow looms in the FULL window, against eyepath_flyvis.py's 20 ms result (does the
step change the answer?); T4/T5 direction selectivity at 2 ms; LC4, LPLC2 and DNp01 time courses.
Sweep on seed 1 with 6 flies; the passing gain with the lowest value is re-run on seed 2 with 8 flies,
and only that confirmation counts.

    python experiments/eyepath_fast.py            (writes experiments/eyepath_fast.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.eye2d import CompoundEye, looming
from brainfly.optic import GRADED as OPTIC, FlyvisOpticLobe
from eyepath import GRADED, SCENES as SCENES_1D, STATIONS, stat
from eyepath_2d import scenes as slow_scenes
from eyepath_filled import N0, measure as measure_1d, verdict
from eyepath_flyvis import direction_selectivity

OUT = Path(__file__).with_name("eyepath_fast.json")
DT, REFRACTORY = 0.002, 0.004
SECONDS = 2.0
WINDOWS = {"full": (0.5, 2.0), "late": (1.5, 2.0)}
FAST = dict(r_over_v=0.04, contact=1.8)
GAINS = [1.0, 3.0, 10.0]
TRACE = ["LC4", "LPLC2", "DNp01"]   # time courses, in 20 ms bins
BIN = 0.020


def scenes() -> dict:
    slow = slow_scenes()
    return {"blank": slow["blank"], "fastL": looming(70.0, 0.0, **FAST), "fastR": looming(-70.0, 0.0, **FAST),
            "slowL": slow["loomL"], "slowR": slow["loomR"]}


def measure(brain, ol, eye, scene, seed, rest_pop, own_graded) -> dict:
    """Per window: station rates (spiking stations in Hz; graded ones as release per second, in
    spike units), the REST population's rate and the share of FlyBrain's graded neurons at their
    limits. Also the TRACE stations' time courses."""
    brain.reset(seed)
    ol.reset()
    steps = int(round(SECONDS / brain.dt))
    per = brain.dt / 0.020                       # release values are per 20 ms
    B = brain.batch
    spans = {w: (int(round(t0 / brain.dt)), int(round(t1 / brain.dt))) for w, (t0, t1) in WINDOWS.items()}
    acc = {w: {"spikes": np.zeros((brain.n, B), np.float32), "fv": np.zeros(len(ol.neurons)),
               "own": np.zeros((len(own_graded), B)), "bounds": 0.0} for w in WINDOWS}
    traced = [(f"{name} {side}", brain.cells([name], side)) for name in TRACE for side in "LR"]
    label = np.full(brain.n, -1)
    for k, (_, idx) in enumerate(traced):
        label[idx] = k
    trace = np.zeros((steps, len(traced), B))
    for s in range(steps):
        rel = ol.step(eye.contrast(scene(s * brain.dt)))
        brain.set_graded(ol.neurons, rel)
        fired = brain.step()
        for b, f in enumerate(fired):
            lab = label[f]
            trace[s, :, b] = np.bincount(lab[lab >= 0], minlength=len(traced))
        live = [w for w, (s0, s1) in spans.items() if s0 <= s < s1]
        if not live:
            continue
        out = brain.graded_out[own_graded]
        at_bounds = float(np.mean((out <= -brain.graded_release + 1e-6) | (out >= 1 - brain.graded_release - 1e-6)))
        for w in live:
            a = acc[w]
            for b, f in enumerate(fired):
                a["spikes"][f, b] += 1
            a["fv"] += rel * per
            a["own"] += out * per
            a["bounds"] += at_bounds
    fv_pos = {int(i): k for k, i in enumerate(ol.neurons)}
    graded_pos = {int(i): k for k, i in enumerate(brain.graded)}
    own_pos = {int(r): k for k, r in enumerate(own_graded)}
    result = {}
    for w, (s0, s1) in spans.items():
        a, window = acc[w], (s1 - s0) * brain.dt
        rates = {}
        for name, types in STATIONS.items():
            for side in "LR":
                idx = brain.cells(types, side)
                idx = idx[idx < N0]
                fv_rows = [fv_pos[int(i)] for i in idx if int(i) in fv_pos]
                if len(fv_rows) > len(idx) // 2:   # a flyvis station: its release change, the same in every fly
                    rates[f"{name} {side}"] = [float(a["fv"][fv_rows].mean() / window)] * B
                elif int(idx[0]) in graded_pos:
                    rates[f"{name} {side}"] = (a["own"][[own_pos[graded_pos[int(i)]] for i in idx]].mean(0) / window).tolist()
                else:
                    rates[f"{name} {side}"] = (a["spikes"][idx].mean(0) / window).tolist()
        result[w] = {"rates": rates, "rest_pop_hz": float(a["spikes"][rest_pop].mean() / window),
                     "graded_at_bounds": a["bounds"] / (s1 - s0)}
    k = int(round(BIN / brain.dt))
    binned = trace[: steps // k * k].reshape(steps // k, k, len(traced), B).sum(1).mean(2)   # spikes per bin, fly mean
    result["trace_hz"] = {name: np.round(binned[:, j] / (len(idx) * BIN), 2).tolist() for j, (name, idx) in enumerate(traced)}
    return result


def judge(m: dict, rest_ref_hz: float) -> dict:
    """The criteria: REST and the slow looms from the FULL window, RELAY/SIDE/ESCAPE from the fast
    looms in LATE, SPEED from fast against slow in LATE."""
    slow = verdict({"blank": m["blank"]["full"], "loomL": m["slowL"]["full"], "loomR": m["slowR"]["full"]}, rest_ref_hz)
    fast = verdict({"blank": m["blank"]["late"], "loomL": m["fastL"]["late"], "loomR": m["fastR"]["late"]}, rest_ref_hz)
    speed = {}
    for side in "LR":
        f = np.array(m[f"fast{side}"]["late"]["rates"][f"LC4 {side}"])
        s = np.array(m[f"slow{side}"]["late"]["rates"][f"LC4 {side}"])
        speed[f"LC4 {side} fast-slow"] = stat(f - s)
    ok_speed = all(x["delta"] >= 2 and x["t"] >= 4 for x in speed.values())
    ok = slow["REST"] and fast["RELAY"] and fast["SIDE"] and ok_speed
    return {"pass": bool(ok), "REST": slow["REST"], "RELAY": fast["RELAY"], "SIDE": fast["SIDE"], "SPEED": bool(ok_speed),
            "ESCAPE": fast["ESCAPE"], "rest_hz": slow["rest_hz"], "rest_pop_hz": slow["rest_pop_hz"],
            "rest_ref_hz": slow["rest_ref_hz"], "graded_at_bounds": slow["graded_at_bounds"],
            "relay": fast["relay"], "side": fast["side"], "escape": fast["escape"], "speed": speed,
            "slow_full": {"relay": slow["relay"], "side": slow["side"], "escape": slow["escape"]}}


def run_config(brain, ol, eye, seed, rest_pop, rest_ref_hz, own_graded, sc) -> dict:
    m = {name: measure(brain, ol, eye, fn, seed, rest_pop, own_graded) for name, fn in sc.items()}
    v = judge(m, rest_ref_hz)
    v["stations"] = {w: {k: {name: round(float(np.mean(m[name][w]["rates"][k])), 3) for name in sc}
                         for k in m["blank"][w]["rates"]} for w in WINDOWS}
    v["trace_hz"] = {name: m[name]["trace_hz"] for name in sc}
    return v


def build(batch: int):
    brain = FlyBrain(batch=batch, graded=OPTIC, fill_retina=True, dt=DT, refractory=REFRACTORY)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisOpticLobe(brain)
    eye = CompoundEye(brain)
    own = np.flatnonzero(~np.isin(brain.graded, ol.neurons))     # rows of brain.graded that FlyBrain itself runs
    return brain, ol, eye, own


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

    brain, ol, eye, own = build(6)
    results["flyvis_neurons"] = int(len(ol.neurons))
    results["direction_selectivity"] = ds = direction_selectivity(brain, ol, eye)
    print("direction selectivity:", {k: (v["preferred"], v["dsi"], "OK" if v["correct"] else "x") for k, v in ds.items()}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    sc = scenes()
    fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t']:.0f})" for k, x in d.items())
    for gain in GAINS:
        t1 = time.perf_counter()
        ol.gain = gain
        v = run_config(brain, ol, eye, 1, rest_pop, rest_ref_hz, own, sc)
        results["sweep"].append({"gain": gain, **v})
        print(f"gain {gain}: {'PASS' if v['pass'] else 'fail'}  REST {v['REST']} {v['rest_hz']} pop {v['rest_pop_hz']} "
              f"bounds {v['graded_at_bounds']} | RELAY {v['RELAY']} {fmt(v['relay'])} | SIDE {v['SIDE']} | "
              f"SPEED {v['SPEED']} {fmt(v['speed'])} | ESCAPE {v['ESCAPE']} {fmt(v['escape'])} | "
              f"slow FULL {fmt(v['slow_full']['relay'])} ({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [r for r in results["sweep"] if r["pass"]]
    if passing:
        pick = min(passing, key=lambda r: r["gain"])
        brain, ol, eye, own = build(8)
        ol.gain = pick["gain"]
        v = run_config(brain, ol, eye, 2, rest_pop, rest_ref_hz, own, sc)
        results["confirm"] = {"gain": pick["gain"], **v}
        print(f"CONFIRM gain {pick['gain']}: {'PASS' if v['pass'] else 'FAIL'} REST {v['REST']} RELAY {v['RELAY']} "
              f"SIDE {v['SIDE']} SPEED {v['SPEED']} ESCAPE {v['ESCAPE']}", flush=True)
    else:
        print("no gain passed the sweep; nothing to confirm", flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
