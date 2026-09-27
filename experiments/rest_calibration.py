"""Rung 4, attempt 1 (pre-registered): with each cell type's excitability calibrated to measured
resting rates, does the rung-1 brain rest like a fly, with real flies' functional connectivity and a
head-direction bump?

rest_fc.py found the uncalibrated brain's resting FC further from real flies' (Pearson r 0.248 over
the 2,145 region pairs) than what shared neurites alone give under independent firing (0.377): its
hot circuits add the wrong correlations. Rung 4 asks for per-type properties throughout. This attempt
fits resting rates only, which FC never sees, so all 20 flies of Turner et al. 2021 are held out.

Model: rung 1's network (shiu_sensory.py's, w_syn = 1.5556 mV), APL graded (Amin et al. 2020), Poisson
background of 1 mV kicks at 200 Hz for every neuron (as in rest_fc.py), and one tonic bias per group,
a group being a neuron's MaleCNS type, or its superclass when it has none.
Targets, from research_notes/Rung 4 resting state data (Hz):
  0     Kenyon cells (Gruntman & Turner 2013: most at zero) and sensory neurons (no stimulus, so no
        sensory drive at rest)
  0.1   descending neurons (Ache et al. 2019: DNp07 and DNp10 under 0.02 Hz; DNa02 near 0 standing)
  3     uniglomerular antennal-lobe projection neurons (Kazama & Wilson 2009: 1-5)
  37.2, 21.5, 16.5, 15.5, 13.4, 10.9   MBON11, 12, 13, 14, 17, 18, and 20.1 PPL101 (Huang et al. 2024)
  3.9   PEN_a (Turner-Evans et al. 2017)
  2     every other group (unmeasured; the research report's energy budget allows a mean of 4 Hz or less)
Graded neurons (APL) aren't calibrated.
Calibration: 8 trials run on, without reset, through 40 rounds. Each round runs 2 s (rounds 1-20) or
4 s (21-40), then moves each group's bias by k ln((target + 0.5) / (rate + 0.5)) mV, with k = 2 (1 from
round 21), at most k mV a round, kept within -30 and +20 mV. The biases after round 40 are final.
Tests, on 8 fresh runs of 300 s after 2 s to settle ("flies"), imaged as the data were (rest_fc.py):
  FC    the model's r with the data's mean FC beats by at least 0.05 both
        (a) the independent null: the FC its neurons would give firing independently at their own
            rates, through shared neurites alone (brainfly.imaging.measurement_only, variance = rate)
        (b) each of 2 degree-preserving rewirings of the network (brainfly.nulls), calibrated and run
            the same way
  RATE  the mean rate is 4 Hz or less, with at most 0.1% of neurons over 100 Hz
  BUMP  the head-direction bump. EPG spikes in 1-s windows, summed per protocerebral-bridge glomerulus
        (L1-L8 and R1-R8; each side's 8 span the full circle), give a population vector whose length
        over the total, the bump strength, is 0 for flat activity and about 0.7 for the ~100 deg bump
        of real flies (Seelig & Jayaraman 2015). On each side, the mean over runs and windows is at
        least 0.3 and above the 99th percentile of 1,000 shuffles of the EPGs' glomerulus labels
        within the side; and the runs' mean bump positions differ (their resultant length is under
        0.6), as an attractor's bump would and one fixed by differences between neurons wouldn't.
Pass: FC, RATE and BUMP all hold.
Reported, not gating: calibration quality (the share of groups whose (rate + 0.5) / (target + 0.5) is
within a factor of 2); r against rest_fc.py's structural predictor (0.65) and ceiling (0.921) and the
equal-variance measurement-only null (0.377); the largest FC errors; the same fit with every default
target at 1 Hz or 4 Hz instead of 2 (sensitivity).

    python experiments/rest_calibration.py --condition intact      (also rewired-1, rewired-2,
                                                                     default-1hz, default-4hz)
    python experiments/rest_calibration.py --report                (writes experiments/rest_calibration.json)
Each condition writes experiments/rest_calibration/<condition>.json (and its biases, <condition>.npz);
scripts/remote/run.sh runs them side by side.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import numpy as np

from brainfly import imaging, nulls
from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from rest_fc import pairs
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

HERE = Path(__file__).with_suffix("")
OUT = Path(__file__).with_suffix(".json")
TRIALS, SECONDS, BIN, WINDOW, SETTLE = 8, 300.0, 0.05, 1.0, 2.0
BACKGROUND = {"noise_rate": 200.0, "noise_kick": 1.0}
ROUNDS = [(2.0, 2.0)] * 20 + [(4.0, 1.0)] * 20          # (seconds run, k: mV per e-fold of rate error)
SOFT, LOW, HIGH = 0.5, -30.0, 20.0
MEASURED = {"MBON11": 37.2, "MBON12": 21.5, "MBON13": 16.5, "MBON14": 15.5, "MBON17": 13.4, "MBON18": 10.9,
            "PPL101": 20.1, "PEN_a(PEN1)": 3.9}
CONDITIONS = {"intact": (None, 2.0), "rewired-1": (1, 2.0), "rewired-2": (2, 2.0),     # (rewiring seed,
              "default-1hz": (None, 1.0), "default-4hz": (None, 4.0)}                  #  default target)
MARGIN, MAX_MEAN, MAX_HOT, MIN_BUMP, MAX_RESULTANT = 0.05, 4.0, 0.001, 0.3, 0.6


def network():
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    return M, 1.0 / sizes(C), labels, types.astype(str), meta["superclass"].astype(str)


def targets(types: np.ndarray, superclass: np.ndarray, default: float) -> np.ndarray:
    t = np.full(len(types), default)
    t[np.char.startswith(superclass, "descending_neuron")] = 0.1
    t[np.array([bool(re.search(r"_[a-z]*PN$", x)) for x in types])] = 3.0
    for name, hz in MEASURED.items():
        t[types == name] = hz
    t[np.char.startswith(types, "KC")] = 0.0
    t[np.char.find(superclass, "sensory") >= 0] = 0.0
    return t


def epgs(types: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The EPG neurons, their side of the bridge and glomerulus (1-8), from MaleCNS instance names
    such as EPG(PB08)_L3."""
    import pyarrow.feather as feather

    ann = feather.read_table(DATA / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "instance"]).to_pandas()
    ids = np.load(DATA / "brain.npz")["ids"]
    instance = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(ids)["instance"].fillna("").astype(str).to_numpy()
    found = [(i, re.search(r"_([LR])([1-8])$", instance[i])) for i in np.flatnonzero(types == "EPG")]
    found = [(i, m) for i, m in found if m]
    return (np.array([i for i, _ in found]), np.array([m.group(1) for _, m in found]),
            np.array([int(m.group(2)) for _, m in found]))


def within_factor_2(rate: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.abs(np.log((rate + SOFT) / (target + SOFT))) <= np.log(2)


def calibrate(brain: HybridBrain, gid: np.ndarray, target: np.ndarray, graded: np.ndarray) -> tuple[np.ndarray, list]:
    G = gid.max() + 1
    size = np.bincount(gid, minlength=G)
    goal = np.bincount(gid, weights=target, minlength=G) / size
    free = np.bincount(gid, weights=~graded, minlength=G) > 0
    bias, log = np.zeros(G), []
    for r, (seconds, k) in enumerate(ROUNDS):
        brain.set_bias(bias[gid])
        rate = brain.advance(int(round(seconds / brain.dt))).mean(0) / seconds
        got = np.bincount(gid, weights=rate, minlength=G) / size
        step = np.where(free, np.clip(k * np.log((goal + SOFT) / (got + SOFT)), -k, k), 0.0)
        bias = np.clip(bias + step, LOW, HIGH)
        log.append({"round": r + 1, "mean_hz": round(float(rate.mean()), 3), "over_100hz": int((rate > 100).sum()),
                    "groups_within_2x": round(float(within_factor_2(got, goal)[free].mean()), 4),
                    "mean_abs_step_mv": round(float(np.abs(step[free]).mean()), 3)})
        print(json.dumps(log[-1]), flush=True)
    return bias, log


def run(brain: HybridBrain, weights, epg: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """8 fresh runs: FC, each neuron's rate per run, and EPG spikes per 1-s window."""
    brain.reset(seed)
    brain.advance(int(round(SETTLE / brain.dt)))
    steps, bins, per = int(round(BIN / brain.dt)), int(round(SECONDS / BIN)), int(round(WINDOW / BIN))
    activity = np.empty((TRIALS, weights.shape[1], bins), np.float32)
    windows = np.zeros((TRIALS, bins // per, len(epg)), np.int32)
    total = np.zeros((TRIALS, brain.n))
    for k in range(bins):
        c = brain.advance(steps)
        activity[:, :, k] = imaging.regional(c, weights)
        windows[:, k // per] += c[:, epg]
        total += c
    fc, _ = imaging.connectivity({f"run {b}": imaging.image(activity[b], BIN) for b in range(TRIALS)}, trims={})
    return fc, total / SECONDS, windows


def bump(windows: np.ndarray, side: np.ndarray, glom: np.ndarray, rng: np.random.Generator) -> dict:
    """Per side: the mean bump strength, its 99th percentile over glomerulus-label shuffles, and each
    run's mean bump position with their resultant length."""
    out = {}
    for s in "LR":
        mine = np.flatnonzero(side == s)
        phase = np.exp(2j * np.pi * (np.arange(8)) / 8)

        def vectors(labels):
            per = np.zeros(windows.shape[:2] + (8,))
            for g in range(8):
                per[..., g] = windows[..., mine[labels == g + 1]].sum(-1)
            return per @ phase, per.sum(-1)

        z, total = vectors(glom[mine])
        with np.errstate(invalid="ignore", divide="ignore"):
            strength = float(np.nanmean(np.abs(z) / total))
            shuffled = [np.nanmean(np.abs(zz) / tt) for zz, tt in (vectors(rng.permutation(glom[mine])) for _ in range(1000))]
        position = np.angle(z.sum(1))                                         # each run's mean position
        out[s] = {"strength": round(strength, 3), "shuffle_p99": round(float(np.percentile(shuffled, 99)), 3),
                  "run_positions_deg": np.round(np.degrees(position), 1).tolist(),
                  "resultant": round(float(np.abs(np.exp(1j * position).mean())), 3)}
    return out


def condition(name: str) -> None:
    t0 = time.perf_counter()
    seed, default = CONDITIONS[name]
    index = list(CONDITIONS).index(name)
    M, scale, labels, types, superclass = network()
    if seed is not None:
        M = nulls.degree_preserving(M, np.random.default_rng(100 + seed))
    key = np.where(types != "", types, np.char.add("superclass:", superclass))
    names, gid = np.unique(key, return_inverse=True)
    target = targets(types, superclass, default)
    brain = HybridBrain(trials=TRIALS, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=10 + index,
                        types={"all": BACKGROUND, "APL": {"unit": "graded"}})
    graded = np.zeros(brain.n, bool)
    graded[brain.graded] = True
    bias, log = calibrate(brain, gid, target, graded)
    HERE.mkdir(exist_ok=True)
    np.savez_compressed(HERE / f"{name}.npz", groups=names, bias=bias)

    weights = imaging.region_weights()
    epg, side, glom = epgs(types)
    brain.set_bias(bias[gid])
    fc, rates, windows = run(brain, weights, epg, seed=1000 + index)
    rate = rates.mean(0)
    data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target_pairs = pairs(data_fc)
    r = lambda m: round(float(np.corrcoef(target_pairs, pairs(m))[0, 1]), 3)
    size = np.bincount(gid)
    got = np.bincount(gid, weights=rate) / size
    goal = np.bincount(gid, weights=target) / size
    free = np.bincount(gid, weights=~graded) > 0
    err = pairs(fc) - target_pairs
    iu = np.triu_indices(len(data_fc), 1)
    measured = {k: {"target_hz": v, "hz": round(float(rate[types == k].mean()), 2)} for k, v in MEASURED.items()}
    classes = {"Kenyon cells": np.char.startswith(types, "KC"), "sensory": np.char.find(superclass, "sensory") >= 0,
               "descending": np.char.startswith(superclass, "descending_neuron"),
               "uniglomerular PNs": np.array([bool(re.search(r"_[a-z]*PN$", x)) for x in types]),
               "EPG": types == "EPG", "Delta7": types == "Delta7"}
    result = {
        "condition": name, "rewiring_seed": seed, "default_target_hz": default, "groups": int(len(names)),
        "calibration": log,
        "bias_mv": {"min": round(float(bias[free].min()), 2), "median": round(float(np.median(bias[free])), 2),
                    "max": round(float(bias[free].max()), 2), "at_low": int((bias[free] <= LOW).sum()),
                    "at_high": int((bias[free] >= HIGH).sum())},
        "groups_within_2x": round(float(within_factor_2(got, goal)[free].mean()), 4),
        "neurons_in_groups_within_2x": round(float(within_factor_2(got, goal)[gid][~graded].mean()), 4),
        "measured_types": measured,
        "classes_hz": {k: round(float(rate[v].mean()), 3) for k, v in classes.items()},
        "superclass_hz": {s: round(float(rate[superclass == s].mean()), 3) for s in np.unique(superclass)},
        "mean_hz": round(float(rate.mean()), 3), "over_100hz": round(float((rate > 100).mean()), 5),
        "mean_hz_per_run": np.round(rates.mean(1), 3).tolist(),
        "r": r(fc), "r_independent": r(imaging.measurement_only(weights, variance=rate)),
        "fc_mean_z": round(float(np.nanmean(pairs(fc))), 3), "data_fc_mean_z": round(float(np.nanmean(target_pairs)), 3),
        "largest_errors": [(imaging.REGIONS[iu[0][k]], imaging.REGIONS[iu[1][k]], round(float(err[k]), 2))
                           for k in np.argsort(-np.abs(err))[:10]],
        "bump": bump(windows, side, glom, np.random.default_rng(7)),
        "fc": np.round(fc, 3).tolist(), "seconds": round(time.perf_counter() - t0)}
    (HERE / f"{name}.json").write_text(json.dumps(result, indent=1))
    print(f"{name}: r {result['r']} (independent {result['r_independent']}); mean {result['mean_hz']} Hz, "
          f"{result['over_100hz']:.4%} over 100 Hz; bump {json.dumps(result['bump'])}; {result['seconds']} s", flush=True)


def report() -> None:
    got = {name: json.loads((HERE / f"{name}.json").read_text()) for name in CONDITIONS if (HERE / f"{name}.json").exists()}
    missing = sorted(set(CONDITIONS) - set(got))
    if {"intact", "rewired-1", "rewired-2"} - set(got):
        raise SystemExit(f"missing conditions: {missing}")
    x = got["intact"]
    rivals = {"independent": x["r_independent"], "rewired-1": got["rewired-1"]["r"], "rewired-2": got["rewired-2"]["r"]}
    fc_ok = all(x["r"] - v >= MARGIN for v in rivals.values())
    rate_ok = x["mean_hz"] <= MAX_MEAN and x["over_100hz"] <= MAX_HOT
    bump_ok = all(b["strength"] >= MIN_BUMP and b["strength"] > b["shuffle_p99"] and b["resultant"] < MAX_RESULTANT
                  for b in x["bump"].values())
    summary = {k: {f: v[f] for f in ("r", "r_independent", "mean_hz", "over_100hz", "groups_within_2x", "bump", "seconds")}
               for k, v in got.items()}
    results = {"criteria": __doc__, "FC": fc_ok, "RATE": rate_ok, "BUMP": bump_ok, "pass": bool(fc_ok and rate_ok and bump_ok),
               "r": x["r"], "rivals": rivals, "for_scale": {"structure_r": 0.65, "ceiling_r": 0.921,
                                                              "measurement_only_equal_variance_r": 0.377,
                                                              "uncalibrated_r": 0.248},
               "conditions": summary, "missing": missing}
    OUT.write_text(json.dumps(results, indent=1))
    print(json.dumps({k: results[k] for k in ("FC", "RATE", "BUMP", "pass", "r", "rivals", "missing")}))
    for k, v in summary.items():
        print(k, json.dumps(v))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=list(CONDITIONS))
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.report:
        report()
    elif a.condition:
        condition(a.condition)
    else:
        ap.error("give --condition or --report")


if __name__ == "__main__":
    main()
