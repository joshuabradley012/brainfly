"""Rung 5 (pre-registered): does brainfly's nerve cord, built by Pugliese et al.'s recipe from MaleCNS, turn DNg100
and DNb08 into leg rhythms at walking frequencies, and does scrambled wiring abolish them?

Rung 5 (README; the report's plan): the recipe is Pugliese et al.'s ("raw counts, excitability scaled by size, graded
premotor neurons, strong descending drive"), and the test is "DNg100 and DNb08 produce 7-15 Hz leg rhythms". Driving
DNg100 (BDN2) makes decapitated flies walk, stepping at about 7-15 Hz, and DNb08 makes them move their front and
middle legs rhythmically (Pugliese et al. 2025/2026, bioRxiv; Sapkal et al. 2024). vnc_rhythm.py (exploratory)
reran Pugliese et al.'s model on their own male CNS files and reproduced their DNg100 rhythm. vnc_own.py found the
same rhythm on brainfly's own copy of the network (16 of 16 replicates on each side, 12-13 Hz), and none when sizes
come from brainfly's synapse-count proxy instead of neuron volumes.
Model: the front legs' neuromere network Pugliese et al. selected (4,310 neurons; 4,309 in brainfly's MaleCNS), with
brainfly's synapse counts among them (brainfly.shiu.counts, signed by brainfly's consensus transmitters:
acetylcholine excitatory, GABA and glutamate inhibitory; connections under 5 synapses dropped;
vnc_own.own_network), their neuron volumes, and their rate model and parameter distributions (vnc_rhythm.py), drawn
afresh for each replicate from seeds no earlier run used.
Drives: DNg100, each side alone, at 400 (their male CNS value), 32 replicates. DNb08, each of the four alone, by their
DN screen's rule, 16 replicates: each replicate's drive starts at 128; in 1-s runs it halves (or bisects down) while
more than 1,500 neurons are active or more than 100 pass 100 Hz, and doubles (or bisects up) while fewer than 5 are
active, at most 10 times; then the test run at that drive.
Score (theirs, vnc_rhythm.py): the rhythmicity of the active leg motor neurons' rates after 0.23 s of a 2-s drive; a
replicate is rhythmic above 0.5; its frequency is that of the autocorrelation's most prominent peak.
Tests:
  DNG100  each DNg100 is rhythmic in at least 24 of its 32 replicates, and those replicates' median frequency is
          7-15 Hz
  DNB08   at least one DNb08 neuron is rhythmic in at least 8 of its 16 replicates, at a median frequency of 7-15 Hz
          (a single DNb08 drove rhythms in their male CNS network)
  NULL    in each of 2 degree-preserving rewirings of the network (brainfly.nulls), each DNg100 is rhythmic in at
          most 3 of 32 replicates
Pass: all three.
Reported: each condition's scores and frequencies, the DNb08 drives the rule settles on, and the motor modules (their
table's annotation: coxa swing, tibia flexion...) that the rhythmic replicates' active motor neurons belong to.

    python experiments/rung5_vnc.py            (writes experiments/rung5_vnc.json)
"""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

import numpy as np

import vnc_rhythm as v
from brainfly import nulls
from vnc_own import own_network

OUT = Path(__file__).with_suffix(".json")
SEED = 5000
DNG100_REPS, DNB08_REPS, NULL_REPS = 32, 16, 32
FREQ = (7.0, 15.0)
START_DRIVE, MAX_ADJUST, ACTIVE, HIGH, HIGH_HZ = 128.0, 10, (5, 1500), 100, 100.0


def modules(table, rates: np.ndarray, mn: np.ndarray) -> list[str]:
    active = mn[rates[:, mn].max(0) > 0.01]
    return [str(m) for m in table["motor module"].to_numpy()[active] if isinstance(m, str)]


def condition(W, table, j: int, drive, reps: int, seed: int) -> dict:
    """reps replicates with neuron j driven at `drive` (a number, or one per replicate)."""
    rng = np.random.default_rng(seed)
    p = v.params(table, rng, reps)
    stim = np.zeros((len(table), reps))
    stim[j] = drive
    rates = simulate(W, p, stim, v.T)
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    per = [v.rhythm(rates[:, :, k], mn) for k in range(reps)]
    rhythmic = [k for k in range(reps) if per[k]["score"] > 0.5]
    freqs = [per[k]["freq_hz"] for k in rhythmic if per[k]["freq_hz"] is not None]
    mods = Counter(m for k in rhythmic for m in modules(table, rates[:, :, k], mn))
    return {"rhythmic": len(rhythmic), "of": reps, "score_mean": round(float(np.mean([x["score"] for x in per])), 3),
            "freq_hz_median": round(float(np.median(freqs)), 1) if freqs else None,
            "freq_hz": [round(f, 1) for f in freqs], "motor_modules": dict(mods.most_common()),
            "drive": np.round(np.broadcast_to(drive, (reps,)), 2).tolist(), "replicates": per}


def simulate(W, p: dict, stim: np.ndarray, seconds: float) -> np.ndarray:
    """vnc_rhythm.simulate with a drive per replicate (stim: n x reps) and a given duration."""
    saved_T, saved_pulse = v.T, v.PULSE
    v.T, v.PULSE = seconds, (0.02, seconds - 0.001)
    try:
        n, k = p["tau"].shape
        Wb = (v.B * W).tocsr()
        r = np.zeros((n, k))
        steps, every = int(round(v.T / v.DT)), int(round(v.SAVE / v.DT))
        out = np.zeros((steps // every + 1, n, k), np.float32)

        def f(r, t):
            drive = stim * (v.PULSE[0] <= t <= v.PULSE[1])
            act = np.maximum(p["rmax"] * np.tanh((p["a"] / p["rmax"]) * (drive + Wb @ r - p["theta"])), 0.0)
            return (act - r) / p["tau"]
        for s in range(steps):
            t = s * v.DT
            if s % every == 0:
                out[s // every] = r
            k1 = f(r, t)
            k2 = f(r + 0.5 * v.DT * k1, t + 0.5 * v.DT)
            k3 = f(r + 0.5 * v.DT * k2, t + 0.5 * v.DT)
            k4 = f(r + v.DT * k3, t + v.DT)
            r = r + v.DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[-1] = r
        return out
    finally:
        v.T, v.PULSE = saved_T, saved_pulse


def tuned_drive(W, table, j: int, reps: int, seed: int) -> np.ndarray:
    """Their DN screen's rule, replicate by replicate, with the replicates' own parameters (same seed as the test)."""
    rng = np.random.default_rng(seed)
    p = v.params(table, rng, reps)
    drive = np.full(reps, START_DRIVE)
    too_high, too_low = np.full(reps, np.nan), np.full(reps, np.nan)
    for _ in range(MAX_ADJUST):
        stim = np.zeros((len(table), reps))
        stim[j] = drive
        rates = simulate(W, p, stim, 1.0)
        active = (rates.sum(0) > 0).sum(0)
        high = (rates.max(0) > HIGH_HZ).sum(0)
        down = (active > ACTIVE[1]) | (high > HIGH)
        up = ~down & (active < ACTIVE[0])
        if not (down | up).any():
            break
        new = drive.copy()
        new[down] = np.where(np.isnan(too_low[down]), drive[down] / 2, (drive[down] + too_low[down]) / 2)
        new[up] = np.where(np.isnan(too_high[up]), drive[up] * 2, (drive[up] + too_high[up]) / 2)
        too_high[down], too_low[up] = drive[down], drive[up]
        drive = new
    return drive


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    results = {"criteria": __doc__, "dng100": {}, "dnb08": {}, "nulls": []}
    dng100, dnb08 = np.flatnonzero(types == "DNg100"), np.flatnonzero(types == "DNb08")
    for k, j in enumerate(dng100):
        results["dng100"][inst[j]] = r = condition(W, table, j, v.STIM, DNG100_REPS, SEED + k)
        print(inst[j], json.dumps({x: r[x] for x in r if x not in ("replicates", "drive")}), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    for k, j in enumerate(dnb08):
        seed = SEED + 100 + k
        drive = tuned_drive(W, table, j, DNB08_REPS, seed)
        results["dnb08"][inst[j]] = r = condition(W, table, j, drive, DNB08_REPS, seed)
        print(inst[j], json.dumps({x: r[x] for x in r if x not in ("replicates",)}), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    for rw in (1, 2):
        Wr = nulls.degree_preserving(W, np.random.default_rng(SEED + 1000 + rw))
        entry = {"rewiring": rw}
        for k, j in enumerate(dng100):
            entry[inst[j]] = r = condition(Wr, table, j, v.STIM, NULL_REPS, SEED + 200 + 10 * rw + k)
            print("rewired", rw, inst[j], json.dumps({x: r[x] for x in r if x not in ("replicates", "drive")}), flush=True)
        results["nulls"].append(entry)
        OUT.write_text(json.dumps(results, indent=1))

    band = lambda r: r["freq_hz_median"] is not None and FREQ[0] <= r["freq_hz_median"] <= FREQ[1]
    results["DNG100"] = bool(all(r["rhythmic"] >= 24 and band(r) for r in results["dng100"].values()))
    results["DNB08"] = bool(any(r["rhythmic"] >= 8 and band(r) for r in results["dnb08"].values()))
    results["NULL"] = bool(all(e[inst[j]]["rhythmic"] <= 3 for e in results["nulls"] for j in dng100))
    results["pass"] = bool(results["DNG100"] and results["DNB08"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print({x: results[x] for x in ("DNG100", "DNB08", "NULL", "pass")}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
