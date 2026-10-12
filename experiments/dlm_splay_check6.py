"""Exploratory check, written after review 10 and before it runs, not pre-registered and not a change to the model:
dlm_splay_check5.py's key conditions with all five units at one rate, and every pair reported against flies'.

Review 10 found that dlm_splay_check5.py's leaky-integrator condition gave all five units one drive, so MN5, whose
assumed junctions load it less, fired 1.41 times as fast as MN1-4 (8.6 against 6.1 Hz) and half as irregularly. In
flies all five fire at one rate (MN5 at 0.98-1.26 times MN1-4 in Hürkey et al.'s Fig. 1b) with similar ISI CVs. At a
common rate (a review's rerun) MN5's pairs left flies' ranges. Reviews 9 and 10 also left several numbers in scratch
reruns only, such as splayness with MN5 coupled like a weak pair. This check puts them on record.
Model: dlm_splay_check5.py's units, junctions (fitted to flies' 20 ms peak ratios in the unit's 20 ms membrane),
spikelets and calibrated noise, with one change: each unit gets its own drive (bias), found by bisection, all five at
once, so that every unit fires at 6.6 Hz in that condition. Conditions:
  LIF, MN5 assumed               private noise (CV 0.22 calibration), MN5's junctions at CC 0.0075 (assumed)
  LIF, MN5 as weak pairs         MN5's four junctions at the measured weak-pair CC, 0.011
  LIF + spikelets, MN5 assumed
  AHP 95% shared + spikelets, MN5 as weak pairs     dlm_splay_check4.py's share-0.95 calibration
Measured as dlm_splay_check5.py measures, plus each unit's rate and ISI CV, and for each of the ten pairs the sync index
r, dip10 (the later unit's spikes at phase < 0.1 or >= 0.9 of the earlier unit's interspike interval) and the share of
the later unit's spikes within 10 ms of the earlier unit's, over chance (1 - exp(-0.02 x the earlier unit's rate)),
against flies' (dlm_splay_state.md sections 2.3-2.4): the strong pairs r 0.336 and 0.394, dip10 0.006 and 0.025, within
10 ms 0.05 and 0.20 times chance; the weak MN1-4 pairs r 0.598-0.666, dip10 0.030-0.056, 0.16-0.31 times; MN5's pairs
r 0.570-0.621, dip10 0.063-0.141, 0.34-0.58 times. 8 runs of 300 s after 3 s (seeds 4700 + 10 x condition, plus 100 x run
in the shared condition).

    python experiments/dlm_splay_check6.py      (writes experiments/dlm_splay_check6.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import sparse

import dlm_splay_check as c1
import dlm_splay_check4 as c4
import dlm_splay_check5 as c5

OUT = Path(__file__).with_suffix(".json")
SEED = 4700
FLIES_PAIRS = {"strong": {"r": [0.336, 0.394], "dip10": [0.006, 0.025], "within_10ms_over_chance": [0.05, 0.20]},
               "weak": {"r": [0.598, 0.666], "dip10": [0.030, 0.056], "within_10ms_over_chance": [0.16, 0.31]},
               "mn5": {"r": [0.570, 0.621], "dip10": [0.063, 0.141], "within_10ms_over_chance": [0.34, 0.58]}}


def junctions(ratio: dict, cc: dict, spikelets: bool):
    """The conductance matrix (per pair class) and, if asked, spikelets scaled by each pair class's CC from the strong
    pairs' 0.035 mV (dlm_splay_check5.py's rule)."""
    rows, cols, vals, gvals = [], [], [], []
    for i, j in combinations(range(c1.N), 2):
        k = c5.pair_class(i, j)
        rows += [i, j]
        cols += [j, i]
        vals += [ratio[k]] * 2
        gvals += [c5.SPIKELET_STRONG * cc[k] / cc["strong"]] * 2
    coupling = sparse.csr_matrix((np.array(vals, np.float32), (rows, cols)), shape=(c1.N, c1.N))
    gap = sparse.csr_matrix((np.array(gvals, np.float32), (rows, cols)), shape=(c1.N, c1.N)) if spikelets else None
    return coupling, gap


def lif_runs(biases: np.ndarray, kick_hz: float, coupling, gap, seconds: float, seed: int, trials: int = c1.RUNS):
    b = c5.unit("LIF", 0.0, kick_hz, c1.KICK_MV, coupling, gap, trials)
    b.set_bias(biases)
    return c1.spike_times(b, seconds, seed)


def shared_runs(biases: np.ndarray, kick_hz: float, sd_mv: float, seconds: float, seed: int, coupling, gap):
    """dlm_splay_check5.shared_run with a drive of each unit's own on top of the shared fluctuation."""
    b = c5.unit("AHP", 0.0, kick_hz, c4.KICK_MV, coupling, gap, 1)
    b.reset(seed)
    rng = np.random.default_rng(seed)
    a = np.exp(-c4.PIECE / c4.TAU_SHARED)
    ou = rng.standard_normal()
    steps = int(round(c4.PIECE / c1.DT))
    burn, total = int(round(c1.BURN / c4.PIECE)), int(round(seconds / c4.PIECE))
    times = [[] for _ in range(c1.N)]
    for k in range(burn + total):
        ou = a * ou + np.sqrt(1 - a * a) * rng.standard_normal()
        b.set_bias(biases + sd_mv * ou)
        if k < burn:
            b.advance(steps)
            continue
        _, sp = b.advance(steps, record=np.arange(c1.N))
        for _, step, i in zip(*np.nonzero(sp)):
            times[i].append(((k - burn) * steps + step) * c1.DT)
    return [np.array(t) for t in times]


def per_unit_biases(rates_for, start: float, half_range: float, iterations: int = 22) -> np.ndarray:
    """Each unit's bias, bisected all at once so that each fires at 6.6 Hz; rates_for(biases) -> per-unit rates."""
    lo, hi = np.full(c1.N, start - half_range), np.full(c1.N, start + half_range)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        r = rates_for(mid)
        lo, hi = np.where(r < c1.TARGET_HZ, mid, lo), np.where(r < c1.TARGET_HZ, hi, mid)
    return 0.5 * (lo + hi)


def pairs(times: list[np.ndarray]) -> dict:
    ph = c1.phases(times)
    out = {}
    for i, j in combinations(range(c1.N), 2):
        kind = "mn5" if j == 4 else "strong" if (i, j) in c1.STRONG else "weak"
        p = c1.phase_of(times, i, j)
        ti, tj = times[i], times[j]
        k = np.searchsorted(ti, tj)
        near = np.minimum(np.abs(tj - ti[np.clip(k - 1, 0, len(ti) - 1)]), np.abs(ti[np.clip(k, 0, len(ti) - 1)] - tj))
        rate_i = len(ti) / c1.SECONDS
        out[f"MN{i + 1}-MN{j + 1}"] = {"kind": kind, "r": round(c1.sync_index(ph, i, j), 4),
                                       "dip10": round(float(np.mean((p < 0.1) | (p >= 0.9))), 4),
                                       "within_10ms_over_chance": round(float(np.mean(near <= 0.010)) / (1 - np.exp(-0.02 * rate_i)), 3)}
    return out


def summarize(runs) -> dict:
    res = c5.summarize(runs)
    res["unit_rates_hz"] = [round(float(np.median([len(r[i]) / c1.SECONDS for r in runs])), 3) for i in range(c1.N)]
    res["unit_isi_cv"] = [round(float(np.median([np.diff(r[i]).std() / np.diff(r[i]).mean() for r in runs])), 3) for i in range(c1.N)]
    per_run = [pairs(r) for r in runs]
    res["pairs"] = {name: {"kind": per_run[0][name]["kind"],
                           **{m: round(float(np.median([pr[name][m] for pr in per_run])), 4)
                              for m in ("r", "dip10", "within_10ms_over_chance")}} for name in per_run[0]}
    inside = {}
    for name, v in res["pairs"].items():
        f = FLIES_PAIRS[v["kind"]]
        inside[name] = {m: bool(f[m][0] <= v[m] <= f[m][1]) for m in f}
    res["pairs_inside_flies"] = inside
    return res


def main() -> None:
    t0 = time.perf_counter()
    d2 = json.loads(Path(c1.OUT).with_name("dlm_splay_check2.json").read_text())
    d4 = json.loads(Path(c4.OUT).read_text())
    d5 = json.loads(Path(c5.OUT).read_text())
    ratio = d5["ratio_fitted_20ms"]
    lif_hz = d2["calibration"]["chosen"]["kick_hz"]
    cal = d4["shares"]["0.95"]["calibration"]
    weak_mn5 = {**ratio, "mn5": ratio["weak"]}
    out = {"question": __doc__, "flies_pairs": FLIES_PAIRS, "ratios": {"assumed_mn5": ratio, "mn5_as_weak": weak_mn5},
           "conditions": {}}
    conditions = [("LIF, MN5 assumed", "LIF", ratio, False, d5["conditions"]["LIF, private"]["bias_mv"]),
                  ("LIF, MN5 as weak pairs", "LIF", weak_mn5, False, d5["conditions"]["LIF, private"]["bias_mv"]),
                  ("LIF + spikelets, MN5 assumed", "LIF", ratio, True, d5["conditions"]["LIF, private + spikelets"]["bias_mv"]),
                  ("AHP 95% shared + spikelets, MN5 as weak pairs", "AHP", weak_mn5, True,
                   d5["conditions"]["AHP, 95% shared + spikelets"]["bias_mv"])]
    for c, (name, kind, rt, spikelets, start) in enumerate(conditions):
        cc = {**c5.CC, "mn5": c5.CC["weak"]} if rt is weak_mn5 else c5.CC
        coupling, gap = junctions(rt, cc, spikelets)
        if kind == "LIF":
            rate_of = lambda bb: np.array([np.mean([len(r[i]) / 60.0 for r in lif_runs(bb, lif_hz, coupling, gap, 60.0, c1.SEED - 1)])
                                           for i in range(c1.N)])
            biases = per_unit_biases(rate_of, start, 3.0)
            runs = lif_runs(biases, lif_hz, coupling, gap, c1.SECONDS, SEED + 10 * c)
        else:
            rate_of = lambda bb: np.array([len(t) / 60.0 for t in shared_runs(bb, cal["kick_hz"], cal["shared_sd_mv"], 60.0,
                                                                              c4.SEED - 1, coupling, gap)])
            biases = per_unit_biases(rate_of, start, 10.0)
            runs = [shared_runs(biases, cal["kick_hz"], cal["shared_sd_mv"], c1.SECONDS, SEED + 10 * c + 100 * r, coupling, gap)
                    for r in range(c1.RUNS)]
        res = summarize(runs)
        res["unit_biases_mv"] = [round(float(x), 5) for x in biases]
        out["conditions"][name] = res
        s = res["summary"]
        print(name, json.dumps({"rates": res["unit_rates_hz"], "cv": res["unit_isi_cv"], "splayness": s["splayness"][0],
                                "preferred": s["preferred_order_share"][0], "repeats": s["repeat_share"],
                                "coinc": s["coincidence_vs_chance_3ms"][0], "pairs": res["pairs"]}),
              f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
