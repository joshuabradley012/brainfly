"""Exploratory, not pre-registered: does Pugliese et al.'s nerve cord model, rerun in brainfly, give leg rhythms
when DNg100 or DNb08 is driven?

Rung 5 (README): "Pugliese et al.'s recipe: raw counts, excitability scaled by size, graded premotor neurons,
strong descending drive"; its test: "DNg100 and DNb08 produce 7-15 Hz leg rhythms". Pugliese et al. (bioRxiv
2025, v2 2026; github.com/smpuglie/Pugliese_2026) simulated nerve cord connectomes as rate networks and found leg
rhythms, from a three-neuron oscillator repeated in each leg, when DNg100 (BDN2) or DNb08 is driven. Driving
DNg100 makes decapitated flies walk, and DNb08 makes them flail rhythmically. This reruns their male CNS case,
before brainfly builds its own: their network of the front legs' neuromere (4,310 neurons: 1,236 descending,
2,378 intrinsic, 328 ascending, 232 sensory, 130 leg motor neurons), with synapses in the nerve cord only and
connections under 5 synapses dropped (their W_20260210_vncRoisOnly and its table, in ~/fly-data/pugliese).
Their model, reimplemented:
    tau_i dr_i/dt = max(rmax_i tanh((a_i / rmax_i) (I_i + 0.03 sum_j w_ij r_j - theta_i)), 0) - r_i
w the synapse counts, signed by transmitter; tau ~ N(20, 2) ms, a ~ N(1, 0.1) / size, theta ~ N(7.5, 0.6) x size and
rmax ~ N(200, 10) Hz (normals truncated at 0; size = volume / median), drawn afresh for each of 16 replicates. A
step of 400 onto one descending neuron from 0.02 s to 2 s (their male CNS value for DNg100). Fourth-order
Runge-Kutta at 0.1 ms (0.05 ms gives the same rates within 0.01 Hz), rates kept every 1 ms.
Their score: for each active leg motor neuron (peak rate over 0.01 Hz), the autocorrelation of its rate after
0.23 s, scaled to [-1, 1]; its highest peak away from lag 0 with prominence at least 0.05 gives min(height,
prominence), divided by the same for a sine at that peak's frequency; averaged over active motor neurons. The
frequency is that of the most prominent peak. They count a score over 0.5 as rhythmic.
Conditions: each DNg100 and each DNb08 alone, and DNg100 in a degree-preserving rewiring of the network.
Ran: DNg100 reproduces their result. The left one gives rhythmic legs in 14 of 16 replicates (13.3 Hz) and the
right one in 16 of 16 (11.6 Hz), through 4-8 active motor neurons. At the same drive, the left DNb08s are rhythmic in
9-10 of 16 but fast (16-18 Hz), the right ones in 1-4. Rewired, DNg100 gives no rhythm (0 of 16) and 96 motor
neurons run up to about 64 Hz. vnc_rhythm_dnb08.py drives DNb08 at their gentler DNb08 value.

    python experiments/vnc_rhythm.py            (writes experiments/vnc_rhythm.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.signal import find_peaks

from brainfly import nulls
from brainfly.data import DATA

OUT = Path(__file__).with_suffix(".json")
SOURCE = DATA / "pugliese"
T, DT, SAVE, PULSE = 2.0, 1e-4, 1e-3, (0.02, 1.999)
B, REPLICATES, STIM, CLIP, PROMINENCE = 0.03, 16, 400.0, 230, 0.05


def network():
    table = pd.read_csv(SOURCE / "wTable_20260210_vncRoisOnly.csv", index_col=0)
    W = pd.read_csv(SOURCE / "W_20260210_vncRoisOnly.csv").drop(columns="bodyId_pre").to_numpy(np.float32)
    return table, sparse.csr_matrix(W.T)                   # rows postsynaptic


def params(table, rng: np.random.Generator, k: int) -> dict:
    """k replicates of Pugliese et al.'s per-neuron parameters, (n, k) each."""
    n = len(table)
    size = table["size"].to_numpy(float)
    size = np.where(np.isnan(size) | (size == 0), np.nan, size)
    size = np.where(np.isnan(size), 1.0, size / np.nanmedian(size))

    def normal(mean, sd):
        x = rng.normal(mean, sd, (n, k))
        while (bad := x <= 0).any():                        # truncated at 0
            x[bad] = rng.normal(mean, sd, bad.sum())
        return x
    return {"tau": normal(0.02, 0.002), "a": normal(1.0, 0.1) / size[:, None], "theta": normal(7.5, 0.6) * size[:, None],
            "rmax": normal(200.0, 10.0)}


def simulate(W, p: dict, stim: np.ndarray) -> np.ndarray:
    """Rates (saves, n, k) under a step of `stim` (n,) during PULSE."""
    n, k = p["tau"].shape
    Wb = (B * W).tocsr()
    r = np.zeros((n, k))
    steps, every = int(round(T / DT)), int(round(SAVE / DT))
    out = np.zeros((steps // every + 1, n, k), np.float32)

    def f(r, t):
        drive = stim[:, None] * (PULSE[0] <= t <= PULSE[1])
        act = np.maximum(p["rmax"] * np.tanh((p["a"] / p["rmax"]) * (drive + Wb @ r - p["theta"])), 0.0)
        return (act - r) / p["tau"]
    for s in range(steps):
        t = s * DT
        if s % every == 0:
            out[s // every] = r
        k1 = f(r, t)
        k2 = f(r + 0.5 * DT * k1, t + 0.5 * DT)
        k3 = f(r + 0.5 * DT * k2, t + 0.5 * DT)
        k4 = f(r + DT * k3, t + DT)
        r = r + DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    out[-1] = r
    return out


def _peak_score(x: np.ndarray) -> tuple[float, float]:
    """min(height, prominence) of the autocorrelation's best peak away from lag 0, and its frequency (Hz)."""
    lo, hi = x.min(), x.max()
    if hi - lo <= 1e-6:
        return 0.0, 0.0
    x = 2 * (x - lo) / (hi - lo) - 1
    ac = np.correlate(x, x, mode="full")
    ac = ac / max(np.abs(ac).max(), 1e-12)
    ac = ac[len(ac) // 2:]
    idx, prop = find_peaks(ac, prominence=PROMINENCE)
    keep = idx > 0
    if not keep.any():
        return 0.0, 0.0
    idx, heights, proms = idx[keep], ac[idx[keep]], prop["prominences"][keep]
    return float(min(heights.max(), proms.max())), float(1.0 / (idx[np.argmax(proms)] * SAVE))


def rhythm(rates: np.ndarray, mn: np.ndarray) -> dict:
    """Pugliese et al.'s score for one replicate's rates (saves, n): the mean over active motor neurons."""
    x = rates[CLIP:, mn]
    active = rates[:, mn].max(0) > 0.01
    scores, freqs = [], []
    t = np.arange(x.shape[0]) * SAVE
    for j in np.flatnonzero(active):
        raw, f = _peak_score(x[:, j].astype(float))
        if raw > 1e-6 and f > 0:
            ref = max(_peak_score(np.sin(2 * np.pi * f * t))[0], _peak_score(np.cos(2 * np.pi * f * t))[0])
            scores.append(min(raw / ref, 1.0) if ref > 1e-6 else 0.0)
            freqs.append(f)
        else:
            scores.append(0.0)
    return {"score": float(np.mean(scores)) if scores else 0.0, "active_mn": int(active.sum()),
            "freq_hz": float(np.median(freqs)) if freqs else None}


def run(W, table, stim_idx: list[int], rng) -> dict:
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    p = params(table, rng, REPLICATES)
    stim = np.zeros(len(table))
    stim[stim_idx] = STIM
    rates = simulate(W, p, stim)
    per = [rhythm(rates[:, :, k], mn) for k in range(REPLICATES)]
    scores = np.array([x["score"] for x in per])
    freqs = [x["freq_hz"] for x in per if x["freq_hz"] is not None]
    return {"score_mean": round(float(scores.mean()), 3), "rhythmic_replicates": int((scores > 0.5).sum()),
            "freq_hz_median": round(float(np.median(freqs)), 1) if freqs else None,
            "active_mn_median": int(np.median([x["active_mn"] for x in per])),
            "mn_peak_hz_median": round(float(np.median(rates[CLIP:, mn].max(0))), 1), "replicates": per}


def main() -> None:
    t0 = time.perf_counter()
    table, W = network()
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    out = {"question": __doc__, "conditions": {}}
    conds = [(f"{i}", [j]) for j in np.flatnonzero(types == "DNg100") for i in [inst[j]]]
    conds += [(f"{inst[j]}", [j]) for j in np.flatnonzero(types == "DNb08")]
    for k, (name, idx) in enumerate(conds):
        out["conditions"][name] = r = run(W, table, idx, np.random.default_rng(100 + k))
        print(name, json.dumps({x: r[x] for x in r if x != "replicates"}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    Wr = nulls.degree_preserving(W, np.random.default_rng(7))
    j = conds[0][1]
    out["conditions"][f"{conds[0][0]}, rewired"] = r = run(Wr, table, j, np.random.default_rng(200))
    print("rewired", json.dumps({x: r[x] for x in r if x != "replicates"}), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
