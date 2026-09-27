"""Exploratory, not pre-registered: does slow homeostasis, run in place, give the whole resting brain a fly-like bump?

ring_fit3.py fitted the head-direction ring's class gains in its 460-neuron sub-network, and with
ring_homeostasis.py's slow homeostasis the ring alone behaves like a fly's compass. Inside the whole brain
(ring_whole.py) it keeps a fly-like bump but favors half the ring. 30 coarse rounds of homeostasis in place
made that worse, while the sub-network needed 80 slow rounds (ring_homeostasis.py --slow). This runs the
sub-network's slow schedule in place, in the brain that tastes and escapes (taste_escape.py's), and then
measures the bump as rung 4 now scores it.
Model: taste_escape.py's brain (escape_at_rest2.py's model, rung 1's sugar route keeping rung 1's settings;
its calibrated biases), plus ring_fit3.py's ring as ring_whole.py puts it in. That means the class gains on every
synapse between two of the 460 ring neurons, their excitatory edges through the 500 ms slow current, the depression
on the ring's excitatory outputs, and the fitted group biases. Each ring neuron also keeps its offset from
ring_homeostasis.py --slow --fit ring_fit3, less its mean input from outside the ring at rest, neuron by
neuron. The ring stays out of the rate calibration.
Procedure: calibrate the rest of the brain (4 rounds at k = 1 mV, 4 at 0.5) with the ring's biases
uncorrected. Then correct them for outside input (from a 2-s resting run) and run 4 more rounds at 0.5.
Then 80 rounds of homeostasis in place, each round 16 fresh runs (2 batches of 8) of 40 s after 1 s to settle.
Every neuron of the ring's six types moves its offset by at most 0.2 mV, by ln((target + 0.5) /
(rate + 0.5)), toward its type's rate in ring_fit3.py's fit. Its rate is averaged over rounds, each new round
weighted 0.3. The offsets are saved every 10 rounds (experiments/ring_insitu/offsets.npz).
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, imaged). That gives the
BUMP measures with bump_motion's position entropy and drift, the rates of the ring's groups and the measured
types, the brain's mean rate and hot neurons, and FC (reported).

    python experiments/ring_insitu.py            (writes experiments/ring_insitu.json and ring_insitu/offsets.npz)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
import ring_er
import ring_whole
import taste_escape as te
from brainfly import imaging
from brainfly.hybrid import TAU
from rest_fc import pairs
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
FIT = "ring_fit3"
ROUNDS, BATCHES, SECONDS, STEP, EMA = 80, 2, 40, 0.2, 0.3


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    fit = json.loads(Path(__file__).with_name(f"{FIT}.json").read_text())["best"]
    p = fit["params"]
    attempt1.network = escape2.network
    M, scale, labels, types, superclass = escape2.network()
    te.use_route(te.sugar_route(M, scale, labels))          # the taste route's model and targets
    route_model = attempt2.model

    def model(types, superclass):
        spec, sets = route_model(types, superclass)
        for t in ring_er.EXC:
            spec[t] = {"depression": p["dep_f"], "recovery": p["dep_tau"]}
        return spec, sets
    attempt2.model = model
    eyes.SUBNETWORK = ring_whole.subnetwork(p)
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(te.HERE / "intact.npz")["bias"]
    b, types = s.brain, s.types
    ring, _ = ring_whole.ring_members(types)
    groups = ring_whole.group_of(types)
    ring_groups = np.unique(s.gid[ring])
    fitted = np.zeros(b.n)
    for g, m in groups.items():
        fitted[m] = p[f"b_{g}"]
    for k in ring_groups:
        s.bias[k] = fitted[s.gid == k].mean()
    homeo = np.zeros(b.n)
    for t, vals in json.loads(Path(__file__).with_name(f"ring_homeostasis_slow_{FIT}.json").read_text())["extra_bias_mv"].items():
        homeo[types == t] = vals
    extra = homeo.copy()
    group_bias = b.set_bias
    b.set_bias = lambda bias: group_bias(None if bias is None else np.asarray(bias) + extra)
    s.fixed |= ring
    eyes.ROUNDS = [1.0] * 4 + [0.5] * 4
    log = s.calibrate()

    # the ring's correction for its mean input from outside the ring, neuron by neuron
    b.reset(3)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    fast = eyes.SUBNETWORK(escape2.network()[0], types, np.asarray(b.superclass))[0].tocsr()
    ext = (fast @ np.where(ring, 0.0, rate / (1.0 + (1.0 - f) * rate * tau))) * b.scale * W_SYN * TAU
    extra[:] = np.where(ring, homeo - ext, 0.0)
    eyes.ROUNDS = [0.5] * 4
    log += s.calibrate()

    # slow homeostasis in place
    target = np.zeros(b.n)
    for g, hz in fit["group_hz"].items():
        if g in groups and g not in ("ER", "ExR"):
            target[groups[g]] = hz
    tune = ring & (target > 0)
    epg, side, glom = attempt1.epgs(types)
    smooth, trace = None, []
    for k in range(ROUNDS):
        rate_k, windows = np.zeros(b.n), []
        for batch in range(BATCHES):
            b.reset(2000 + 10 * k + batch)
            b.set_release(s.ol.neurons, s.silent)
            b.set_bias(s.bias[s.gid])
            b.advance(int(round(1.0 / b.dt)))
            w = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(SECONDS)], 1)      # trials x seconds x n
            rate_k += w.sum((0, 1)) / (SECONDS * eyes.TRIALS * BATCHES)
            windows.append(w[:, :, epg])
        smooth = rate_k if smooth is None else (1 - EMA) * smooth + EMA * rate_k
        extra[:] = np.where(tune, extra + np.clip(STEP * np.log((target + 0.5) / (smooth + 0.5)), -STEP, STEP), extra)
        m = attempt1.bump_motion(np.concatenate(windows), side, glom)
        trace.append({"round": k + 1, "position_entropy": m["position_entropy"], "drift_D": m["drift_D_rad2_per_s"],
                      "epg_hz": round(float(rate_k[epg].mean()), 2), "epg_rate_cv": round(float(rate_k[epg].std() / max(rate_k[epg].mean(), 1e-9)), 3)})
        print(json.dumps(trace[-1]), flush=True)
        if (k + 1) % 10 == 0:
            np.savez_compressed(HERE / "offsets.npz", extra=extra, group_bias=s.bias, rounds=k + 1)
    np.savez_compressed(HERE / "offsets.npz", extra=extra, group_bias=s.bias, rounds=ROUNDS)

    # rung 4's protocol
    weights = imaging.region_weights()
    fc, rates, windows = attempt1.run(b, weights, epg, seed=1200)
    np.savez_compressed(HERE / "measure.npz", fc=fc, rates=rates, windows=windows)
    own = ~s.fixed
    rate = rates.mean(0)
    bump = attempt1.bump(windows, side, glom, np.random.default_rng(7))
    motion = attempt1.bump_motion(windows, side, glom)
    data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target_pairs = pairs(data_fc)
    r = lambda mat: round(float(np.corrcoef(target_pairs, pairs(mat))[0, 1]), 3)
    classic = all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                  and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR")
    out = {"question": __doc__, "calibration": log[-1], "homeostasis": trace,
           "BUMP": bool(classic and motion["MOVES_LIKE_A_FLY"]), "bump": bump, "bump_motion": motion,
           "RATE": bool(rate[own].mean() <= attempt1.MAX_MEAN and (rate[own] > 100).mean() <= attempt1.MAX_HOT),
           "mean_hz_own": round(float(rate[own].mean()), 3), "over_100hz_own": round(float((rate[own] > 100).mean()), 5),
           "ring_group_hz": {g: round(float(rate[m].mean()), 2) for g, m in groups.items()},
           "measured_types": {t: {"target_hz": v, "hz": round(float(rate[types == t].mean()), 2)} for t, v in attempt1.MEASURED.items()},
           "r": r(fc), "r_independent": r(imaging.measurement_only(weights, variance=rate)),
           "seconds": round(time.perf_counter() - t0)}
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "homeostasis")}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
