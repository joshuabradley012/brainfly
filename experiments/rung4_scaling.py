"""Rung 4, attempt 5, pre-registered: with the head-direction ring's outside input under homeostatic synaptic scaling,
does the brain that tastes and escapes rest like a fly's?

Attempts 3 and 4 (rung4_rest.py, rung4_anneal.py) passed every criterion but BUMP: their bumps were strong and drifted
like a fly's but leaned toward part of the ring. ring_attribution.py traced the lean to the ring's input from outside
it: the ring inside the whole brain is even without it and leans with it, even with its mean cancelled
(ring_quiet.py). An offset on each neuron (the homeostasis of attempts 3 and 4) cancels the mean of its outside input,
not its fluctuations. ring_scaling.py (exploratory) let each ring neuron scale its synapses from outside the ring
instead, excitatory down and inhibitory up when it fires too much and the reverse when too little, over 40 annealed
rounds with the factors averaged. BUMP then passed by the widest margins yet (position entropy 0.98, resultants 0.27
and 0.36). This test runs that from the start on new seeds and asks all of rung 4.

Model: ring_insitu.py's (taste_escape.py's brain with ring_fit3.py's ring as ring_whole.py puts it in, every ring
neuron with its offset from ring_homeostasis.py --slow --fit ring_fit3, the ring out of the rate calibration), plus a
factor g_i for every ring neuron that multiplies its excitatory synapses from outside the ring and divides its
inhibitory ones.
Procedure (each condition from the start, on new seeds):
  1-3. rung4_rest.py's steps 1-3 (ring_insitu.tune): build the brain (seed 11; 61 and 62 for the rewirings), calibrate
       the rest of the brain (4 rounds at k = 1 mV and 4 at 0.5 from taste_escape/intact.npz's biases, a rewired network
       first getting taste_escape.py's 20 rounds from rest_calibration2.py's rewired biases; calibration round r from
       seed 6900 + r), lower each ring neuron's offset by its mean input from outside the ring (a 2-s resting run, seed
       43), and calibrate 4 more rounds at 0.5 mV.
  4. 40 rounds of synaptic scaling, as ring_scaling.py: each round 2 batches of 8 fresh runs of 40 s after 1 s (round
     k from seeds 14000 + 10k and 14001 + 10k; 15000 and 16000 in place of 14000 for the rewirings). Every neuron of the
     ring's tuned types (all but ER and ExR) moves ln g_i by -step ln((rate + 0.5) / (target + 0.5)), at most step,
     toward its type's rate in ring_fit3.py's fit. Its rate is smoothed over rounds (each new round weighted 0.3), and
     the step falls linearly from 0.2 to 0.02. Then each g_i is set to its geometric mean over the 40 rounds. The
     offsets don't change after step 3.
Tests, rung4_rest.py's thirteen on new seeds:
  RATE, BUMP  rung 4's protocol (8 fresh runs of 300 s at grey after 2 s, seed 6200), scored as in rung4_rest.py.
  REST, RELAY, SIDE, ESCAPE  eyes_at_rest.py's looming tests at gain 1 (8 flies, seed 43).
  QUIET, SUGAR, RESPONSE, BITTER, IR94E, STABLE  taste_escape.py's tests with 30 flies of the same brain (seed 28),
         biases, offsets and factors: QUIET from seed 109, the taste conditions from seeds 51-56.
  NULL   in 2 degree-preserving rewirings (eyes_at_rest.py's rewirings 1 and 2, the sugar route found again in each;
         the same procedure), BUMP fails (rung 4's protocol, seeds 6201 and 6202).
Pass: all thirteen hold.
Order: the intact brain runs first; the rewired brains run only if it passes its twelve tests.
Reported: as rung4_rest.py, plus each round's bump motion and the factors' spread by ring group.

    python experiments/rung4_scaling.py intact        (then rewired-1 and rewired-2: each writes rung4_scaling/<condition>.json;
                                                       rerun after an interruption to resume)
    python experiments/rung4_scaling.py verdict       (writes experiments/rung4_scaling.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rest_calibration as attempt1
import ring_insitu
import rung4_rest as r4
import taste_escape as te

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
CONDITIONS = {"intact": dict(rewiring=None, brain=11, scaling=14000, measure=6200),        # seeds
              "rewired-1": dict(rewiring=1, brain=61, scaling=15000, measure=6201),
              "rewired-2": dict(rewiring=2, brain=62, scaling=16000, measure=6202)}
CAL_SEED, OUTSIDE_SEED, LOOM_SEED, TASTE_BRAIN, QUIET_SEED, TASTE_SEEDS = 6900, 43, 43, 28, 109, (51, 52, 53, 54, 55, 56)
STEPS, EMA, BATCHES, SECONDS = np.linspace(0.2, 0.02, 40), 0.3, 2, 40


class Scaling:
    """The synapses from outside the ring onto ring neurons in a brain's weights (columns presynaptic), and the factors
    that scale them: excitatory ones times g, inhibitory ones divided by g."""

    def __init__(self, brain, ring: np.ndarray):
        self.brain, self.w0 = brain, brain.weights.copy()
        pre = np.repeat(np.arange(brain.n), np.diff(brain.ptr))
        onto = ring[brain.idx] & ~ring[pre]
        self.exc, self.inh = onto & (self.w0 > 0), onto & (self.w0 < 0)

    def apply(self, log_g: np.ndarray) -> None:
        g = np.exp(log_g)
        w = self.w0.copy()
        w[self.exc] *= g[self.brain.idx[self.exc]]
        w[self.inh] /= g[self.brain.idx[self.inh]]
        self.brain.weights = w.astype(np.float32)
        self.brain._external_matrix = None


def prepare(name: str) -> tuple[eyes.Setup, dict, list, list, np.ndarray]:
    """Steps 1-4 for one condition: the setup with the averaged factors in place, the ring's state, the calibration log,
    the scaling trace and the factors (log). Everything needed to resume is kept after every round in
    rung4_scaling/<condition>_state.npz."""
    c = CONDITIONS[name]
    eyes.CAL_SEED = CAL_SEED
    s, st = ring_insitu.build(c["rewiring"], seed=c["brain"])
    b, ring, groups = s.brain, st["ring"], st["groups"]
    state = HERE / f"{name}_state.npz"
    if state.exists():
        z = np.load(state)
        s.bias, st["extra"][:] = z["group_bias"].copy(), z["extra"]
        log, trace = json.loads(str(z["log"])), json.loads(str(z["trace"]))
        log_g, total, first = z["log_g"].copy(), z["total"].copy(), int(z["rounds"])
        smooth = z["smooth"].copy() if first else None
        print("resuming after round", first, flush=True)
    else:
        rounds = r4.FIRST_ROUNDS if c["rewiring"] is None else te.ROUNDS + r4.FIRST_ROUNDS
        log = ring_insitu.tune(s, st, rounds, seed=OUTSIDE_SEED)
        log_g, total, first, trace, smooth = np.zeros(b.n), np.zeros(b.n), 0, [], None
    scaling = Scaling(b, ring)
    target = np.zeros(b.n)
    for gname, hz in st["fit"]["group_hz"].items():
        if gname in groups and gname not in ("ER", "ExR"):
            target[groups[gname]] = hz
    tuned = ring & (target > 0)
    epg, side, glom = attempt1.epgs(s.types)

    def keep(k: int) -> None:
        np.savez(state, group_bias=s.bias, extra=st["extra"], log_g=log_g, total=total, rounds=k, trace=json.dumps(trace),
                 log=json.dumps(log), smooth=np.zeros(0) if smooth is None else smooth)
    if first == 0:
        keep(0)
    for k in range(first, len(STEPS)):
        scaling.apply(log_g)
        rate_k, windows = np.zeros(b.n), []
        for batch in range(BATCHES):
            b.reset(c["scaling"] + 10 * k + batch)
            b.set_release(s.ol.neurons, s.silent)
            b.set_bias(s.bias[s.gid])
            b.advance(int(round(1.0 / b.dt)))
            w = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(SECONDS)], 1)      # trials x seconds x n
            rate_k += w.sum((0, 1)) / (SECONDS * eyes.TRIALS * BATCHES)
            windows.append(w[:, :, epg])
        smooth = rate_k if smooth is None else (1 - EMA) * smooth + EMA * rate_k
        step = STEPS[k]
        log_g = np.where(tuned, log_g - np.clip(step * np.log((smooth + 0.5) / (target + 0.5)), -step, step), log_g)
        total += log_g
        m = attempt1.bump_motion(np.concatenate(windows), side, glom)
        trace.append({"round": k + 1, "position_entropy": m["position_entropy"], "drift_D": m["drift_D_rad2_per_s"],
                      "epg_hz": round(float(rate_k[epg].mean()), 2), "epg_rate_cv": round(float(rate_k[epg].std() / max(rate_k[epg].mean(), 1e-9)), 3),
                      "g_range": [round(float(np.exp(log_g[tuned].min())), 3), round(float(np.exp(log_g[tuned].max())), 3)]})
        print(json.dumps(trace[-1]), flush=True)
        keep(k + 1)
    averaged = total / len(STEPS)                          # each factor's geometric mean over the rounds
    scaling.apply(averaged)
    b.set_bias(s.bias[s.gid])
    return s, st, log, trace, averaged


def lower_rungs(s: eyes.Setup, st: dict, log_g: np.ndarray) -> dict:
    """rung4_rest.lower_rungs with this test's seeds, its 30-fly brain getting the same offsets and factors."""
    v = eyes.loom_tests(s, 1.0, seed=LOOM_SEED)
    eyes.show("escape, gain 1", v)
    out = {"looming": {k: v[k] for k in ("rest_hz", "own_mean_hz", "own_over_100hz", "relay", "side", "escape", "trace_hz")}}
    out.update({k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")})
    eyes.TRIALS = te.TASTE_TRIALS
    t, tst = ring_insitu.build(None, start_bias=s.bias, seed=TASTE_BRAIN)
    eyes.TRIALS = 8
    tst["extra"][:] = st["extra"]
    Scaling(t.brain, tst["ring"]).apply(log_g)
    t.brain.set_bias(t.bias[t.gid])
    out.update(te.taste_tests(t, quiet_seed=QUIET_SEED, seeds=TASTE_SEEDS))
    return out


def condition(name: str) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    path = HERE / f"{name}.json"
    s, st, log, trace, log_g = prepare(name)
    groups = st["groups"]
    out = {"condition": name, "seeds": CONDITIONS[name], "calibration": log[-1], "scaling": trace,
           "factors_by_group": {g: [round(float(np.exp(log_g[m].min())), 3), round(float(np.exp(np.median(log_g[m]))), 3),
                                    round(float(np.exp(log_g[m].max())), 3)] for g, m in groups.items()}}
    out.update(r4.rest(s, st, CONDITIONS[name]["measure"]))
    print(json.dumps({k: out[k] for k in ("RATE", "BUMP", "mean_hz", "over_100hz", "bump", "fc_r", "fc_r_independent")}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}), flush=True)
    path.write_text(json.dumps(out, indent=1))
    if name == "intact":
        out.update(lower_rungs(s, st, log_g))
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
