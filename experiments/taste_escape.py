"""Does the resting brain taste as well as escape? (pre-registered)

escape_at_rest2.py's resting brain passed its pre-registered escape test, but sugar no longer drives the
proboscis motor neuron MN9 in it (+1.5 Hz, against +40 in rung 1's silent brain). research_notes/Rung 4
resting state data/taste_at_rest.md traced the loss to two settings that no measurement supports for this
circuit. One is short-term depression on the taste interneurons; none has been measured at any taste
synapse. The other is the 0.1 Hz target for descending neurons, which came from walking and escape
descending neurons, while the premotor cluster that feeds MN9 has descending members. taste_route.py
(exploratory, 7 conditions) found three things. Changing both by type name set off spontaneous MN9 bouts at
rest, through a cluster off rung 1's taste route. Quieting MN9's inputs stopped the bouts but lost the taste.
One rule worked: rung 1's sugar route keeps rung 1's settings. With it (route_all), on the pilots' seeds,
sugar raised MN9 by 19.6 Hz, bitter and Ir94e cut that, MN9 had no spontaneous bouts, and the escape still
passed. This test takes that rule and does nothing else.
Model: escape_at_rest2.py's (rest_calibration2.py's per-type properties, depression by presynaptic class, no
synapses between visual projection neurons of the same type, flyvis's eyes, model 001), plus:
  the sugar route: the neurons that sugar at 100 Hz (rung 1's drive onto the left sugar GRNs, LB3b and LB3c)
    raises by more than 5 Hz in the silent version of the test's own network (rung 1's neuron model: no
    background, no bias, no depression; 8 trials, seed 1 for the brain and 3 for the drive)
  the route's cholinergic neurons undepressed; its descending neurons at the 2 Hz default target instead of
  0.1 Hz; DSOG1 (DNg70, DNg98) at 17 Hz (Pool et al. 2014)
Calibration: 20 fresh-start rounds from escape_at_rest2.py's eyes-open biases (k = 2 mV for 8 rounds, then 1
for 8, then 0.5 for 4; 8 trials; 1 s to settle and 2 s measured, as eyes_at_rest.py).
Tests, on seeds no pilot used:
  REST, RELAY, SIDE, ESCAPE  eyes_at_rest.py's looming tests at gain 1 (escape_at_rest2.py's confirmed gain),
                             seed 3, 8 flies
  QUIET    at rest (10 s at grey after 1 s, 30 flies, seed 79), MN9 L fires more than 20 spikes in at most 5%
           of fly-seconds. Awake flies rarely extend the proboscis at rest, and MN9 fires only while the
           rostrum moves (Gordon & Scott 2009).
  SUGAR, RESPONSE, BITTER, IR94E, STABLE  taste_at_rest.py's tests and protocol: 30 flies, 1 s to settle
           (MN9 L's rest over its last 0.5 s), 1 s of drive at 100 Hz, 0.5 s after; seeds 21-25
             SUGAR     sugar raises MN9 L by at least 10 Hz (t >= 4 over flies)
             RESPONSE  at 10 Hz of sugar, the rise is at most 25% of the rise at 100 Hz
             BITTER    adding bitter neurons cuts the rise by at least 25% (Welch t >= 4)
             IR94E     adding Ir94e neurons cuts the rise by at least 25% (Welch t >= 4)
             STABLE    during sugar at most 0.1% of the brain's own undriven neurons pass 100 Hz, and in the
                       last 0.25 s after it their mean rate is within 20% of the rate at rest
  NULL     in 2 degree-preserving rewirings (eyes_at_rest.py's, of this network; the sugar route found again
           in each rewired network by the same rule; recalibrated the same way from rest_calibration2.py's
           rewired biases), sugar raises MN9 L by less than 10 Hz (8 flies, seed 21) and ESCAPE fails (gain
           1, seed 3), in both
Pass: all eleven hold.
Reported: water's effect on MN9; MN9 R; MN9 L's rise when the left Roundup, Roundtree and Rounddown (GNG108,
GNG120, DNge080) are driven at 50 Hz; the brain's resting statistics (own mean rate, neurons over 100 Hz,
neurons whose 1-s Fano factor passes 10).

    python experiments/taste_escape.py            (writes experiments/taste_escape.json and taste_escape/intact.npz)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_at_rest as escape
import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
from brainfly import nulls
from brainfly.hybrid import HybridBrain, consensus_transmitters
from shiu_baseline import SETS, welch
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
FULL_TARGETS = attempt1.targets
ROUNDS = [2.0] * 8 + [1.0] * 8 + [0.5] * 4
DSOG1, PREMOTOR = ["DNg70", "DNg98"], ["GNG108", "GNG120", "DNge080"]
TASTE_TRIALS, SETTLE, REST_WINDOW, DRIVE, TAIL = 30, 1.0, 0.5, 1.0, 0.5


def network_for(rewiring: int | None):
    """The test's network as eyes_at_rest.Setup builds it (escape_at_rest2.py's, rewired if asked)."""
    M, scale, labels, types, superclass = escape2.network()
    if rewiring is not None:
        M = nulls.degree_preserving(M, np.random.default_rng(100 + rewiring))
    return M, scale, labels, types, superclass


def sugar_route(M, scale, labels) -> np.ndarray:
    b = HybridBrain(trials=8, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=1)
    return b.run(1.0, drive=[(b.cells(SETS["sugar"], "L"), 100.0)], seed=3).rates > 5


def use_route(route: np.ndarray) -> None:
    """Set the model and targets for eyes_at_rest.Setup: the route keeps rung 1's settings."""
    def model(types, superclass):
        spec, sets = escape.model(types, superclass)
        sets["sugar_route"] = np.flatnonzero((consensus_transmitters() == "acetylcholine") & route)
        spec["sugar_route"] = {"depression": 1.0}
        return spec, sets

    def targets(types, superclass, default):
        t = FULL_TARGETS(types, superclass, default)
        t[route & np.char.startswith(superclass, "descending_neuron")] = default
        t[np.isin(types, DSOG1)] = 17.0
        return t
    attempt2.model, attempt1.targets = model, targets


def build(rewiring: int | None, seed: int) -> tuple[eyes.Setup, int]:
    M, scale, labels, types, superclass = network_for(rewiring)
    route = sugar_route(M, scale, labels)
    use_route(route)
    return eyes.Setup(rewiring, seed=seed), int(route.sum())


def taste_trial(s: eyes.Setup, drive: list, seed: int) -> dict:
    """taste_at_rest.py's trial, with flyvis's neurons silent at grey."""
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round((SETTLE - REST_WINDOW) / b.dt)))
    rest = b.advance(int(round(REST_WINDOW / b.dt))) / REST_WINDOW
    driven = b.advance(int(round(DRIVE / b.dt)), drive=drive) / DRIVE
    b.advance(int(round((TAIL - 0.25) / b.dt)))
    late = b.advance(int(round(0.25 / b.dt))) / 0.25
    return {"rest": rest, "driven": driven, "late": late}


def taste_tests(t: eyes.Setup, quiet_seed: int = 79, seeds: tuple = (21, 22, 23, 24, 25, 26)) -> dict:
    """QUIET and the taste tests (SUGAR, RESPONSE, BITTER, IR94E, STABLE) in a 30-fly setup whose biases are set, as
    this test ran them: QUIET's rest from quiet_seed, the six taste conditions from seeds."""
    b = t.brain
    out = {}
    own = ~t.fixed
    mn9L, mn9R = b.cells(["MN9"], "L"), b.cells(["MN9"], "R")
    b.reset(quiet_seed)
    b.set_release(t.ol.neurons, t.silent)
    b.advance(int(round(1.0 / b.dt)))
    c = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(10)])        # seconds x flies x neurons
    bouts = float((c[:, :, mn9L].sum(2) > 20).mean())
    mean, var = c.mean((0, 1)), c.var(0).mean(0)
    fano = np.where(mean > 0.5, var / np.maximum(mean, 1e-9), np.nan)
    out["rest"] = {"own_mean_hz": round(float(mean[own].mean()), 3), "own_over_100hz": int((mean[own] > 100).sum()),
                   "bursting_fano_over_10": int(np.nansum(fano[own] > 10)), "mn9_L_hz": round(float(mean[mn9L].mean()), 2),
                   "mn9_L_bout_share": round(bouts, 4), "dsog1_hz": round(float(mean[b.cells(DSOG1)].mean()), 2)}
    out["QUIET"] = bool(bouts <= 0.05)
    print("rest:", out["rest"], "QUIET", out["QUIET"], flush=True)

    cells = {k: b.cells(v, "L") for k, v in SETS.items()}
    undriven = own.copy()
    undriven[np.concatenate(list(cells.values()))] = False
    run = lambda names, rate=100.0, seed=seeds[0]: taste_trial(t, [(cells[k], rate) for k in names], seed)
    conds = {"sugar": run(["sugar"], seed=seeds[0]), "sugar 10 Hz": run(["sugar"], 10.0, seed=seeds[1]), "sugar+bitter": run(["sugar", "bitter"], seed=seeds[2]),
             "sugar+ir94e": run(["sugar", "ir94e"], seed=seeds[3]), "water": run(["water"], seed=seeds[4]),
             "premotor 50 Hz": taste_trial(t, [(b.cells(PREMOTOR, "L"), 50.0)], seeds[5])}
    rise = {k: x["driven"][:, mn9L].mean(1) - x["rest"][:, mn9L].mean(1) for k, x in conds.items()}
    t_sugar = rise["sugar"].mean() / (rise["sugar"].std(ddof=1) / np.sqrt(TASTE_TRIALS))
    cut = lambda k: 1 - rise[k].mean() / rise["sugar"].mean() if rise["sugar"].mean() > 0 else 0.0
    sug = conds["sugar"]
    hot = float((sug["driven"][:, undriven].mean(0) > 100).mean())
    rest_mean, late_mean = float(sug["rest"][:, own].mean()), float(sug["late"][:, own].mean())
    out["taste"] = {
        "rise_hz": {k: round(float(x.mean()), 2) for k, x in rise.items()},
        "rise_sem_hz": {k: round(float(x.std(ddof=1) / np.sqrt(len(x))), 2) for k, x in rise.items()},
        "mn9_L_hz": {k: {"rest": round(float(x["rest"][:, mn9L].mean()), 2), "driven": round(float(x["driven"][:, mn9L].mean()), 2)} for k, x in conds.items()},
        "mn9_R_hz": {k: {"rest": round(float(x["rest"][:, mn9R].mean()), 2), "driven": round(float(x["driven"][:, mn9R].mean()), 2)} for k, x in conds.items()},
        "t_sugar": round(float(t_sugar), 1), "bitter_cut": round(float(cut("sugar+bitter")), 3), "t_bitter": round(welch(rise["sugar"], rise["sugar+bitter"]), 1),
        "ir94e_cut": round(float(cut("sugar+ir94e")), 3), "t_ir94e": round(welch(rise["sugar"], rise["sugar+ir94e"]), 1),
        "undriven_over_100hz": round(hot, 5), "brain_rest_hz": round(rest_mean, 3), "brain_late_hz": round(late_mean, 3)}
    tr = out["taste"]
    out["SUGAR"] = bool(rise["sugar"].mean() >= 10 and t_sugar >= 4)
    out["RESPONSE"] = bool(rise["sugar 10 Hz"].mean() <= 0.25 * rise["sugar"].mean())
    out["BITTER"] = bool(cut("sugar+bitter") >= 0.25 and tr["t_bitter"] >= 4)
    out["IR94E"] = bool(cut("sugar+ir94e") >= 0.25 and tr["t_ir94e"] >= 4)
    out["STABLE"] = bool(hot <= 0.001 and abs(late_mean - rest_mean) <= 0.2 * rest_mean)
    print("taste:", tr["rise_hz"], {k: out[k] for k in ("SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE")}, flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    attempt1.network = escape2.network                  # eyes_at_rest.Setup builds the test's network
    eyes.ROUNDS = ROUNDS
    HERE.mkdir(exist_ok=True)
    results = {"criteria": __doc__}
    s, n_route = build(None, seed=5)
    s.bias = np.load(escape2.HERE / "intact.npz")["bias"]
    results["route_neurons"] = n_route
    results["calibration"] = s.calibrate()
    np.savez_compressed(HERE / "intact.npz", groups=s.names, bias=s.bias)

    v = eyes.loom_tests(s, 1.0, seed=3)
    eyes.show("escape, gain 1", v)
    results["looming"] = {k: v[k] for k in ("rest_hz", "own_mean_hz", "own_over_100hz", "relay", "side", "escape",
                                            "REST", "RELAY", "SIDE", "ESCAPE", "trace_hz")}
    for k in ("REST", "RELAY", "SIDE", "ESCAPE"):
        results[k] = v[k]
    OUT.write_text(json.dumps(results, indent=1))

    # 30 flies for the taste tests and QUIET, with the calibrated biases
    eyes.TRIALS = TASTE_TRIALS
    t, _ = build(None, seed=6)
    t.bias = s.bias.copy()
    t.brain.set_bias(t.bias[t.gid])
    results.update(taste_tests(t))
    OUT.write_text(json.dumps(results, indent=1))

    eyes.TRIALS = 8
    results["nulls"] = []
    for k in (1, 2):
        n, n_route = build(k, seed=50 + k)
        log = n.calibrate()
        nb = n.brain
        m9 = nb.cells(["MN9"], "L")
        r = taste_trial(n, [(nb.cells(SETS["sugar"], "L"), 100.0)], 21)
        sugar_rise = float((r["driven"][:, m9].mean(1) - r["rest"][:, m9].mean(1)).mean())
        lv = eyes.loom_tests(n, 1.0, seed=3)
        results["nulls"].append({"rewiring": k, "route_neurons": n_route, "calibration": log[-1], "sugar_rise_hz": round(sugar_rise, 2),
                                 "ESCAPE": lv["ESCAPE"], "escape": lv["escape"], "RELAY": lv["RELAY"]})
        print(f"  rewiring {k}: route {n_route}, sugar rise {sugar_rise:+.2f} Hz, ESCAPE {lv['ESCAPE']}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    results["NULL"] = all(x["sugar_rise_hz"] < 10 and not x["ESCAPE"] for x in results["nulls"])
    tests = ("REST", "RELAY", "SIDE", "ESCAPE", "QUIET", "SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE", "NULL")
    results["pass"] = all(results[k] for k in tests)
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: " + " ".join(f"{k} {results[k]}" for k in tests) + f" ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
