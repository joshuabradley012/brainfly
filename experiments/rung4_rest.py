"""Rung 4, attempt 3, pre-registered: with its head-direction ring fitted and each ring neuron's slow homeostasis run in
place, does the brain that tastes and escapes rest like a fly's?

Attempts 1 and 2 (rest_calibration.py, rest_calibration2.py) rested at the measured rates, but their head-direction
bump sat in one place. taste_escape.py (pre-registered, passed) then gave the resting brain rung 1's taste alongside
the looming escape. ring_fit3.py fitted the ring's class gains in its 460-neuron sub-network. ring_insitu.py
(exploratory) found that 80 rounds of the ring neurons' slow homeostasis, run inside the whole brain, give it a bump
that moves like a fly's: BUMP and RATE held on its one measurement. This test runs ring_insitu.py's procedure again
from the start, on seeds no earlier run used, and asks all of rung 4 of the result: resting rates, the bump, and the
rungs below still passing at rest. FC is reported, not tested (it moved to the ladder's final hurdle on 27 September
2026).

Model: ring_insitu.py's. That is taste_escape.py's brain (escape_at_rest2.py's model, rung 1's sugar route keeping rung
1's settings), with ring_fit3.py's ring as ring_whole.py puts it in: the class gains on every synapse between two of
the 460 ring neurons, their excitatory edges through the 500 ms slow current, depression on the ring's excitatory
outputs, and the fitted group biases. Each ring neuron adds its offset from ring_homeostasis.py --slow --fit
ring_fit3, less its mean input from outside the ring at rest. The ring stays out of the rate calibration.

Procedure (each condition from the start, as ring_insitu.py ran it, on fresh seeds):
  1. Build the brain (seed 7 intact; 57 and 58 for the rewirings).
  2. Calibrate the rest of the brain: 4 rounds at k = 1 mV and 4 at 0.5, from taste_escape/intact.npz's biases
     (calibration round r from seed 4900 + r). A rewired network starts from rest_calibration2.py's rewired biases, as
     taste_escape.py's nulls did, so it first gets taste_escape.py's 20 rounds (8 at 2 mV, 8 at 1, 4 at 0.5).
  3. Correct each ring neuron's offset for its mean input from outside the ring (from a 2-s resting run, seed 13),
     then 4 more rounds at 0.5 mV.
  4. 80 rounds of slow homeostasis in place (ring_insitu.homeostasis; round k's batches from seeds 6000 + 10k and
     6001 + 10k, 7000 and 8000 in place of 6000 for the rewirings), then set the final offsets.
Tests:
  RATE   rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s at grey after 2 s, seed 4200): the brain's own
         spiking neurons, the ring's included, average at most 4 Hz, and at most 0.1% of them fire over 100 Hz.
  BUMP   the same runs, as rung 4 now scores it (rest_calibration.bump and bump_motion). On each side of the bridge,
         the bump's strength is at least 0.3 and above the 99th percentile of 1,000 glomerulus-label shuffles. The 8
         runs' mean positions have a resultant under 0.6. The bump's position entropy over the 16 wedges is at
         least 0.9, and its drift D is 0.003-0.04 rad^2/s.
  REST, RELAY, SIDE, ESCAPE  eyes_at_rest.py's looming tests at gain 1 (8 flies, seed 13), as taste_escape.py ran them.
  QUIET, SUGAR, RESPONSE, BITTER, IR94E, STABLE  taste_escape.py's tests (taste_escape.taste_tests), with 30 flies of
         the same brain (seed 8), biases and offsets. QUIET runs from seed 89, the taste conditions from seeds 31-36.
  NULL   in 2 degree-preserving rewirings (eyes_at_rest.py's rewirings 1 and 2 of this network, the sugar route found
         again in each; the same procedure), BUMP fails (rung 4's protocol, seeds 4201 and 4202).
Pass: all thirteen hold.
Reported: resting FC against the flies' (r), against the same neurons firing independently; the ring's group rates
and the measured types' rates; RATE without the ring (as ring_insitu.py reported it); each homeostasis round's bump
motion; the rewired networks' RATE and bump measures.

    python experiments/rung4_rest.py intact           (also rewired-1 and rewired-2: each writes rung4_rest/<condition>.json)
    python experiments/rung4_rest.py verdict          (writes experiments/rung4_rest.json)
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
import taste_escape as te
from brainfly import imaging
from rest_fc import pairs

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
CONDITIONS = {"intact": dict(rewiring=None, brain=7, homeostasis=6000, measure=4200),        # seeds
              "rewired-1": dict(rewiring=1, brain=57, homeostasis=7000, measure=4201),
              "rewired-2": dict(rewiring=2, brain=58, homeostasis=8000, measure=4202)}
CAL_SEED, OUTSIDE_SEED, LOOM_SEED, TASTE_BRAIN, QUIET_SEED, TASTE_SEEDS = 4900, 13, 13, 8, 89, (31, 32, 33, 34, 35, 36)
FIRST_ROUNDS = [1.0] * 4 + [0.5] * 4
LOWER = ("REST", "RELAY", "SIDE", "ESCAPE", "QUIET", "SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE")


def prepare(name: str) -> tuple[eyes.Setup, dict, list, list]:
    """Steps 1-4 of the procedure for one condition: the setup, the ring's state, the calibration log and the
    homeostasis trace. The offsets are saved to rung4_rest/<condition>_offsets.npz."""
    c = CONDITIONS[name]
    eyes.CAL_SEED = CAL_SEED
    s, st = ring_insitu.build(c["rewiring"], seed=c["brain"])
    rounds = FIRST_ROUNDS if c["rewiring"] is None else te.ROUNDS + FIRST_ROUNDS
    log = ring_insitu.tune(s, st, rounds, seed=OUTSIDE_SEED)
    trace = ring_insitu.homeostasis(s, st, c["homeostasis"], save=HERE / f"{name}_offsets.npz")
    s.brain.set_bias(s.bias[s.gid])                       # the final round's offsets
    return s, st, log, trace


def rest(s: eyes.Setup, st: dict, seed: int) -> dict:
    """RATE and BUMP from rung 4's protocol, with FC and the rates reported."""
    b, types, groups = s.brain, s.types, st["groups"]
    epg, side, glom = attempt1.epgs(types)
    weights = imaging.region_weights()
    fc, rates, windows = attempt1.run(b, weights, epg, seed=seed)
    rate = rates.mean(0)
    spiking = np.ones(b.n, bool)
    spiking[b.graded] = False
    spiking &= ~b.external
    ringless = ~s.fixed
    bump = attempt1.bump(windows, side, glom, np.random.default_rng(7))
    motion = attempt1.bump_motion(windows, side, glom)
    classic = all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                  and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR")
    data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target_pairs = pairs(data_fc)
    r = lambda mat: round(float(np.corrcoef(target_pairs, pairs(mat))[0, 1]), 3)
    return {"RATE": bool(rate[spiking].mean() <= attempt1.MAX_MEAN and (rate[spiking] > 100).mean() <= attempt1.MAX_HOT),
            "BUMP": bool(classic and motion["MOVES_LIKE_A_FLY"]),
            "mean_hz": round(float(rate[spiking].mean()), 3), "over_100hz": round(float((rate[spiking] > 100).mean()), 5),
            "without_ring": {"mean_hz": round(float(rate[ringless].mean()), 3), "over_100hz": round(float((rate[ringless] > 100).mean()), 5)},
            "bump": bump, "bump_motion": motion,
            "ring_group_hz": {g: round(float(rate[m].mean()), 2) for g, m in groups.items()},
            "measured_types": {t: {"target_hz": v, "hz": round(float(rate[types == t].mean()), 2)} for t, v in attempt1.MEASURED.items()},
            "fc_r": r(fc), "fc_r_independent": r(imaging.measurement_only(weights, variance=rate))}


def lower_rungs(s: eyes.Setup, st: dict) -> dict:
    """The rungs below at rest: taste_escape.py's looming tests, then its taste tests with 30 flies of the same brain."""
    v = eyes.loom_tests(s, 1.0, seed=LOOM_SEED)
    eyes.show("escape, gain 1", v)
    out = {"looming": {k: v[k] for k in ("rest_hz", "own_mean_hz", "own_over_100hz", "relay", "side", "escape", "trace_hz")}}
    out.update({k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")})
    eyes.TRIALS = te.TASTE_TRIALS
    t, tst = ring_insitu.build(None, start_bias=s.bias, seed=TASTE_BRAIN)
    eyes.TRIALS = 8
    tst["extra"][:] = st["extra"]
    t.brain.set_bias(t.bias[t.gid])
    out.update(te.taste_tests(t, quiet_seed=QUIET_SEED, seeds=TASTE_SEEDS))
    return out


def condition(name: str) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    path = HERE / f"{name}.json"
    s, st, log, trace = prepare(name)
    out = {"condition": name, "seeds": CONDITIONS[name], "calibration": log[-1], "homeostasis": trace}
    out.update(rest(s, st, CONDITIONS[name]["measure"]))
    print(json.dumps({k: out[k] for k in ("RATE", "BUMP", "mean_hz", "over_100hz", "bump", "fc_r", "fc_r_independent")}), flush=True)
    path.write_text(json.dumps(out, indent=1))
    if name == "intact":
        out.update(lower_rungs(s, st))
        path.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    path.write_text(json.dumps(out, indent=1))
    print(name, "done", out["seconds"], "s", flush=True)


def verdict() -> None:
    r = {name: json.loads((HERE / f"{name}.json").read_text()) for name in CONDITIONS}
    intact = r["intact"]
    tests = {"RATE": intact["RATE"], "BUMP": intact["BUMP"], **{k: intact[k] for k in LOWER},
             "NULL": all(not r[k]["BUMP"] for k in ("rewired-1", "rewired-2"))}
    out = {"criteria": __doc__, **tests, "pass": all(tests.values()), "conditions": r}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"{'PASS' if out['pass'] else 'FAIL'}: " + " ".join(f"{k} {v}" for k, v in tests.items()), flush=True)


if __name__ == "__main__":
    verdict() if sys.argv[1] == "verdict" else condition(sys.argv[1])
