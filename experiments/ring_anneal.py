"""Exploratory, not pre-registered: does annealing the ring neurons' homeostasis even out the bump that rung 4's third
attempt left favoring one side?

rung4_rest.py (pre-registered) ran ring_insitu.py's procedure from the start on fresh seeds and failed only on BUMP.
Its bump was strong and drifted like a fly's, but it favored one side of the ring (position entropy 0.79,
resultants 0.91), where ring_insitu.py's run had left it even (0.96). Each round's step moves every ring neuron's
offset by up to 0.2 mV on a rate estimate from 16 runs of 40 s, so with a constant step the offsets keep random-walking,
and the landscape the bump sees at round 80 is where that walk happened to be. Stochastic approximation settles when
its steps shrink or its iterates are averaged. This tests both, from where the failed run ended.
Model: rung4_rest.py's intact brain (ring_insitu.py's model, brain seed 7), with its calibrated biases, offsets and
smoothed rates after its 80 rounds (rung4_rest/intact_state.npz).
Procedure: 40 more rounds of ring_insitu.homeostasis (2 batches of 8 fresh runs of 40 s after 1 s, round k from
seeds 9000 + 10k and 9001 + 10k), each round's step falling linearly from 0.2 to 0.02 mV, and the mean of the offsets
after each of the 40 rounds kept alongside.
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9500), as rung4_rest.py scores
it, once with the final offsets and once with the averaged ones.
Ran: annealing evened the ring out, and with the averaged offsets BUMP passes. The bump's strength is 0.71 and 0.70
(shuffles' 99th percentiles 0.38), the resultants are 0.42 and 0.40, the position entropy is 0.93 (from 0.79), and D is
0.015 rad^2/s. With the final round's offsets the position entropy is also 0.93, but one side's resultant is 0.78, so
BUMP misses. RATE holds either way (1.66 Hz, nothing over 100 Hz). This is one measurement from one brain; eight runs
give the resultant test a few percent chance of failing even for a perfectly even ring.

    python experiments/ring_anneal.py            (writes experiments/ring_anneal.json; resumes after an interruption)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import ring_insitu
import rung4_rest as r4

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
STEPS = np.linspace(0.2, 0.02, 40)
SEED, MEASURE = 9000, 9500


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    s, st = ring_insitu.build(None, seed=r4.CONDITIONS["intact"]["brain"])
    start = np.load(r4.HERE / "intact_state.npz")
    s.bias = start["group_bias"].copy()
    state = HERE / "state.npz"
    if state.exists():                                   # resume: the offsets, smoothed rates, trace and running sum
        z = np.load(state)
        st["extra"][:] = z["extra"]
        resume = {"rounds": int(z["rounds"]), "smooth": z["smooth"], "trace": json.loads(str(z["trace"]))}
        total = z["total"].copy()
        print("resuming after round", resume["rounds"], flush=True)
    else:
        st["extra"][:] = start["extra"]
        resume = {"rounds": 0, "smooth": start["smooth"], "trace": []}
        total = np.zeros_like(st["extra"])

    def keep(k: int, smooth, trace: list) -> None:
        total[:] += st["extra"]
        np.savez(state, extra=st["extra"], smooth=smooth, rounds=k, trace=json.dumps(trace), total=total)
    trace = ring_insitu.homeostasis(s, st, SEED, resume=resume, checkpoint=keep, steps=STEPS)
    final, averaged = st["extra"].copy(), total / len(STEPS)
    out = {"question": __doc__, "homeostasis": trace, "measured": {}}
    for name, offsets in (("final", final), ("averaged", averaged)):
        st["extra"][:] = offsets
        s.brain.set_bias(s.bias[s.gid])
        m = r4.rest(s, st, MEASURE)
        out["measured"][name] = m
        print(name, json.dumps({k: m[k] for k in ("RATE", "BUMP", "mean_hz", "over_100hz", "bump")}),
              json.dumps({k: v for k, v in m["bump_motion"].items() if k != "position_histogram"}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
