"""Rung 4, attempt 4, pre-registered: with the ring neurons' homeostasis annealed and its offsets averaged, so that the
ring can settle, does the brain that tastes and escapes rest like a fly's?

rung4_rest.py (attempt 3, pre-registered) passed every criterion but BUMP. Run from the start on fresh seeds,
ring_insitu.py's 80 rounds of the ring neurons' slow homeostasis left a bump that was strong and drifted like a fly's
but favored one side of the ring (position entropy 0.79, resultants 0.91). With a constant step, the homeostasis's
offsets keep random-walking on noisy rate estimates, so the ring a run ends with is partly luck. ring_anneal.py
(exploratory) continued that brain for 40 rounds with the step falling from 0.2 to 0.02 mV. With the offsets averaged
over those rounds, BUMP passed: position entropy 0.93, resultants 0.42 and 0.40, D = 0.015 rad^2/s. With the final
round's offsets alone, one resultant missed (0.78). This test adds those 40 rounds and the averaging to attempt 3's
procedure and runs it all from the start on new seeds.

Model: rung4_rest.py's, which is ring_insitu.py's: taste_escape.py's brain (escape_at_rest2.py's model; rung 1's
sugar route keeping rung 1's settings) with ring_fit3.py's ring as ring_whole.py puts it in. Each ring neuron adds its
offset from ring_homeostasis.py --slow --fit ring_fit3, less its mean input from outside the ring at rest, and the
ring stays out of the rate calibration.

Procedure (each condition from the start, on new seeds):
  1-3. rung4_rest.py's: build the brain (seed 9; 59 and 60 for the rewirings), calibrate the rest of the brain (4
       rounds at k = 1 mV and 4 at 0.5 from taste_escape/intact.npz's biases, a rewired network first getting
       taste_escape.py's 20 rounds from rest_calibration2.py's rewired biases; calibration round r from seed 5900 + r),
       correct the ring's offsets for its outside input (a 2-s resting run, seed 23), and calibrate 4 more rounds at
       0.5 mV.
  4. 120 rounds of ring_insitu.homeostasis (round k's two batches of 8 fresh runs of 40 s from seeds 10000 + 10k and
     10001 + 10k; 11000 and 12000 in place of 10000 for the rewirings): 80 at a step of 0.2 mV, then 40 with the step
     falling linearly from 0.2 to 0.02 mV. Each ring neuron's offset is then set to its mean after each of those last
     40 rounds.
Tests, rung4_rest.py's thirteen on new seeds:
  RATE, BUMP  rung 4's protocol (8 fresh runs of 300 s at grey after 2 s, seed 5200), scored as in rung4_rest.py.
  REST, RELAY, SIDE, ESCAPE  eyes_at_rest.py's looming tests at gain 1 (8 flies, seed 23).
  QUIET, SUGAR, RESPONSE, BITTER, IR94E, STABLE  taste_escape.py's tests with 30 flies of the same brain (seed 18),
         biases and offsets: QUIET from seed 99, the taste conditions from seeds 41-46.
  NULL   in 2 degree-preserving rewirings (eyes_at_rest.py's rewirings 1 and 2, the sugar route found again in each;
         the same procedure), BUMP fails (rung 4's protocol, seeds 5201 and 5202).
Pass: all thirteen hold.
Order: the intact brain runs first. The rewired brains run only if it passes its twelve tests, since otherwise NULL
can't change the verdict.
Reported: as rung4_rest.py (FC against the flies' and against independent firing, the ring's group rates, the
measured types' rates, RATE without the ring, each homeostasis round's bump motion, the rewired brains' measures).

    python experiments/rung4_anneal.py intact         (then rewired-1 and rewired-2: each writes rung4_anneal/<condition>.json;
                                                       rerun after an interruption to resume)
    python experiments/rung4_anneal.py verdict        (writes experiments/rung4_anneal.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import ring_insitu
import rung4_rest as r4
import taste_escape as te

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
CONDITIONS = {"intact": dict(rewiring=None, brain=9, homeostasis=10000, measure=5200),        # seeds
              "rewired-1": dict(rewiring=1, brain=59, homeostasis=11000, measure=5201),
              "rewired-2": dict(rewiring=2, brain=60, homeostasis=12000, measure=5202)}
CAL_SEED, OUTSIDE_SEED, LOOM_SEED, TASTE_BRAIN, QUIET_SEED, TASTE_SEEDS = 5900, 23, 23, 18, 99, (41, 42, 43, 44, 45, 46)
CONSTANT, ANNEALED = 80, 40
STEPS = np.concatenate([np.full(CONSTANT, ring_insitu.STEP), np.linspace(ring_insitu.STEP, 0.02, ANNEALED)])


def prepare(name: str) -> tuple[eyes.Setup, dict, list, list]:
    """Steps 1-4 for one condition: the setup with the averaged offsets in place, the ring's state, the calibration log
    and the homeostasis trace. Everything needed to resume is kept after every round in rung4_anneal/<condition>_state.npz."""
    c = CONDITIONS[name]
    eyes.CAL_SEED = CAL_SEED
    s, st = ring_insitu.build(c["rewiring"], seed=c["brain"])
    state, resume = HERE / f"{name}_state.npz", None
    if state.exists():
        z = np.load(state)
        s.bias, st["extra"][:] = z["group_bias"].copy(), z["extra"]
        log, total = json.loads(str(z["log"])), z["total"].copy()
        resume = {"rounds": int(z["rounds"]), "smooth": z["smooth"] if int(z["rounds"]) else None,
                  "trace": json.loads(str(z["trace"]))}
        print("resuming after round", resume["rounds"], flush=True)
    else:
        rounds = r4.FIRST_ROUNDS if c["rewiring"] is None else te.ROUNDS + r4.FIRST_ROUNDS
        log = ring_insitu.tune(s, st, rounds, seed=OUTSIDE_SEED)
        total = np.zeros_like(st["extra"])

    def keep(k: int, smooth, trace: list) -> None:
        if k > CONSTANT:
            total[:] += st["extra"]
        np.savez(state, group_bias=s.bias, extra=st["extra"], smooth=np.zeros(0) if smooth is None else smooth, rounds=k,
                 trace=json.dumps(trace), log=json.dumps(log), total=total)
    if resume is None:
        keep(0, None, [])
    trace = ring_insitu.homeostasis(s, st, c["homeostasis"], resume=resume, checkpoint=keep, steps=STEPS)
    st["extra"][:] = total / ANNEALED                     # each offset's mean over the annealed rounds
    s.brain.set_bias(s.bias[s.gid])
    return s, st, log, trace


def condition(name: str) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    path = HERE / f"{name}.json"
    s, st, log, trace = prepare(name)
    out = {"condition": name, "seeds": CONDITIONS[name], "calibration": log[-1], "homeostasis": trace}
    out.update(r4.rest(s, st, CONDITIONS[name]["measure"]))
    print(json.dumps({k: out[k] for k in ("RATE", "BUMP", "mean_hz", "over_100hz", "bump", "fc_r", "fc_r_independent")}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}), flush=True)
    path.write_text(json.dumps(out, indent=1))
    if name == "intact":
        out.update(r4.lower_rungs(s, st, loom_seed=LOOM_SEED, taste_brain=TASTE_BRAIN, quiet_seed=QUIET_SEED,
                                  taste_seeds=TASTE_SEEDS))
    out["seconds"] = round(time.perf_counter() - t0)
    path.write_text(json.dumps(out, indent=1))
    print(name, "done", out["seconds"], "s", flush=True)


def verdict() -> None:
    r = {name: json.loads((HERE / f"{name}.json").read_text()) for name in CONDITIONS if (HERE / f"{name}.json").exists()}
    intact = r["intact"]
    nulls = [r[k]["BUMP"] for k in ("rewired-1", "rewired-2") if k in r]
    tests = {"RATE": intact["RATE"], "BUMP": intact["BUMP"], **{k: intact[k] for k in r4.LOWER},
             "NULL": (not any(nulls)) if len(nulls) == 2 else None}
    out = {"criteria": __doc__, **tests, "pass": all(v is True for v in tests.values()), "conditions": r}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"{'PASS' if out['pass'] else 'FAIL'}: " + " ".join(f"{k} {v}" for k, v in tests.items()), flush=True)


if __name__ == "__main__":
    verdict() if sys.argv[1] == "verdict" else condition(sys.argv[1])
