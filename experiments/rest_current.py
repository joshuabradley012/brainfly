"""Reported, not a test: the current resting brain's resting-state measures, as rung 4 reports them.

Rung 4's criteria changed on 27 September 2026: resting FC moved to the ladder's final hurdle and is reported
at every attempt, and the bump gained position entropy and drift. This measures them for the current brain,
taste_escape.py's (which passed): escape_at_rest2.py's model (depression by synapse class, no synapses between
visual projection neurons of the same type, flyvis's eyes silent at grey) with rung 1's sugar route keeping
rung 1's settings, and its calibrated biases (experiments/taste_escape/intact.npz). Protocol as
rest_calibration.py's run: 8 fresh runs of 300 s at grey after 2 s to settle, imaged as the flies were
(brainfly.imaging). Reported: the measured types' rates against their targets; the resting FC's r with the
flies' mean FC, against the same neurons firing independently at their own rates through shared neurites
(imaging.measurement_only) and attempts 1 and 2; rung 4's bump measures, with bump_motion's position entropy
and drift; the brain's mean rate and neurons over 100 Hz. The head-direction ring here is the resting brain's,
not ring_fit3.py's (which isn't in this brain yet).

    python experiments/rest_current.py            (writes experiments/rest_current.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_at_rest2 as escape2
import rest_calibration as attempt1
import taste_escape as te
from brainfly import imaging
from rest_fc import pairs

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    t0 = time.perf_counter()
    attempt1.network = escape2.network
    s, _ = te.build(None, seed=5)
    s.bias = np.load(te.HERE / "intact.npz")["bias"]
    b = s.brain
    b.set_bias(s.bias[s.gid])
    b.set_release(s.ol.neurons, s.silent)             # external from now on; reset() keeps them silent
    weights = imaging.region_weights()
    epg, side, glom = attempt1.epgs(s.types)
    fc, rates, windows = attempt1.run(b, weights, epg, seed=1100)
    np.savez_compressed(Path(__file__).with_suffix(".npz"), fc=fc, rates=rates, windows=windows)   # before anything can fail
    own = ~s.fixed
    rate = rates.mean(0)
    data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target = pairs(data_fc)
    r = lambda m: round(float(np.corrcoef(target, pairs(m))[0, 1]), 3)
    bump = attempt1.bump(windows, side, glom, np.random.default_rng(7))
    motion = attempt1.bump_motion(windows, side, glom)
    earlier = {}
    for name, path in (("attempt 1", "rest_calibration/intact.json"), ("attempt 2", "rest_calibration2/intact.json")):
        p = Path(__file__).parent / path
        if p.exists():
            earlier[name] = json.loads(p.read_text())["r"]
    out = {"question": __doc__,
           "measured_types": {k: {"target_hz": v, "hz": round(float(rate[s.types == k].mean()), 2)} for k, v in attempt1.MEASURED.items()},
           "mean_hz_own": round(float(rate[own].mean()), 3), "over_100hz_own": round(float((rate[own] > 100).mean()), 5),
           "r": r(fc), "r_independent": r(imaging.measurement_only(weights, variance=rate)), "r_earlier": earlier,
           "bump": bump, "bump_motion": motion,
           "BUMP_as_before": bool(all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                                      and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR")),
           "fc": np.round(fc, 3).tolist(), "seconds": round(time.perf_counter() - t0)}
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "fc")}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
