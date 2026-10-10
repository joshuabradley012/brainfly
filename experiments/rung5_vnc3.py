"""Rung 5, attempt 3 (pre-registered): over one grid of drives applied alike to the real and the scrambled networks, does
brainfly's nerve cord turn DNg100 into leg rhythms at walking frequencies and DNb08 into leg rhythms, while scrambled
wiring gives none at any drive?

Attempts 1 and 2 (rung5_vnc.py, rung5_vnc2.py) failed on DNb08. rung5_drive_check.py (exploratory, run after both)
found that drives chosen without data decided both: DNb08's came from Pugliese et al.'s screen rule started at 128,
a value with no source that the rule never moved; at 256, which the rule also accepts, the left VES082 DNb08 was
rhythmic in 16 and 15 of 16 replicates. And DNg100's scrambled networks, driven at the real network's 400, ran away
(about 100 of 130 motor neurons active), while tuned by the same rule one of four made a slow rhythm (13 of 32
replicates at 5.8 Hz). This attempt was designed after that check, so its design is not blind to those results. To
take the choice of drive out of the test, every descending neuron is driven, in the real network and in two fresh
scrambled ones, at each drive of one grid: 50, 100, 200, 400 and 800, Pugliese et al.'s male CNS drive for DNg100 (400)
halved and doubled as their screen's rule steps. 256 is not on it.
Model, as attempts 1 and 2: the front legs' neuromere network (4,309 neurons) with brainfly's signed synapse counts
(connections under 5 dropped; vnc_own.own_network), Pugliese et al.'s neuron volumes, rate model and parameter
distributions (vnc_rhythm.py). Each descending neuron alone: DNg100 (each side) with 32 replicates, each of the four
DNb08 neurons with 16; each replicate's parameters drawn once, from seeds no earlier run used (base 17000), and used at
all five drives. Scrambled: two degree-preserving rewirings (brainfly.nulls.degree_preserving, seeds 17501 and 17502).
A drive counts for a neuron in a network if the screen's rule would keep it in at least half the replicates: over the
run's first second (identical to the rule's 1 s run), between 5 and 1,500 neurons active and at most 100 above 100 Hz.
Score (vnc_rhythm.py): a replicate is rhythmic when its active leg motor neurons' rhythmicity score passes 0.5; its
frequency is the autocorrelation's most prominent peak.
Tests:
  DNG100  each DNg100, at some drive that counts in the real network, is rhythmic in at least 24 of its 32 replicates,
          at a median frequency of 7-15 Hz
  DNB08   at least one DNb08 neuron, at some drive that counts in the real network, is rhythmic in at least 8 of its 16
          replicates (frequency reported, not tested, as in attempt 2)
  NULL    in each rewiring, at every drive that counts there, each DNg100 is rhythmic in at most 3 of 32 replicates and
          each DNb08 neuron in at most 3 of 16, at any frequency
Pass: all three.
Reported: for every neuron, network and drive, the rhythmic replicates and their frequencies, the score, the rule's
verdict, the active neurons and motor neurons, and the descending neuron's own rate.


Ran (2026-10-09, 2.2 hours; the text above is the pre-registration as it ran): fail, on DNG100, by one replicate.
  DNG100  fails. In the real network each DNg100 counts only at 400: at 200 and below one to four neurons are active,
          at 800 about 2,000-2,300 of the 4,309 (770-1,030 above 100 Hz). At 400 the right DNg100 is rhythmic in 32 of
          32 replicates at a median of 11.6 Hz, and the left in 23 of 32 at 13.7 Hz, one short of the 24 required.
          (Attempts 1 and 2, at the same drive on other seeds: left 30 and 30 of 32, right 31 and 32.)
  DNB08   passes. The left VES082 DNb08 is rhythmic in 15 of 16 replicates at 200 (13.2 Hz), 8 at 400 (14.2 Hz) and
          3 at 100; the left VES083 in 8 of 16 at 200 (16.0 Hz) and 7 at 400 (18.2 Hz). The right two are rhythmic in
          none at the drives that count for them (100 and 200; 1 of 16 at 400, which doesn't count).
  NULL    holds, partly vacuously. No rewired replicate is rhythmic at any drive, counting or not (0 of 1,280). But a
          drive counts for only 7 of the 12 neuron-rewiring pairs, each time one at which the motor neurons barely
          respond (a median of 0-2 active), and for the other 5 no drive counts, so the test there asks nothing. At
          every drive with more response than that, the rewired networks run away (about 3,000 of the 4,309 neurons
          active, 1,600-2,000 above 100 Hz, about 100 motor neurons). On this grid they go from nearly silent motor
          neurons to runaway within one doubling of the drive, so the grid never samples them in between, where
          rung5_drive_check.py's rule-tuned drives found one slow rhythm in another rewiring.

Checked afterwards (2026-10-09, exploratory): rerun on the same seeds, the left DNg100 at 400 again gives 23 of 32. Of
  its nine misses, six oscillate at 13.0-15.4 Hz but score 0.43-0.50, at or just under the 0.5 cutoff (with four to
  seven motor neurons active, one or two arrhythmic ones pull the mean under it); two are broad and slow (31 and 78
  motor neurons active, 0.6-0.8 Hz), and in one no motor neuron is active.

    python experiments/rung5_vnc3.py            (writes experiments/rung5_vnc3.json; about 2 hours)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung5_vnc as a1
import vnc_rhythm as v
from brainfly import nulls
from vnc_own import own_network

OUT = Path(__file__).with_suffix(".json")
SEED = 17000
DRIVES = (50.0, 100.0, 200.0, 400.0, 800.0)
REPS = {"DNg100": 32, "DNb08": 16}
NETWORKS = ("real", "rewired 1", "rewired 2")


def simulate(W, p: dict, stim: np.ndarray, record: np.ndarray, j: int) -> dict:
    """vnc_rhythm's model (as rung5_vnc.simulate: RK4 at v.DT, a step drive from 0.02 s to the end, rates saved every
    v.SAVE) keeping only the `record` neurons' saved rates, each neuron's activity and peak over the first second, and
    neuron j's mean rate after 0.5 s."""
    n, k = p["tau"].shape
    Wb = (v.B * W).tocsr()
    r = np.zeros((n, k))
    steps, every = int(round(v.T / v.DT)), int(round(v.SAVE / v.DT))
    first = int(round(1.0 / v.SAVE))
    pulse = (0.02, v.T - 0.001)
    rec = np.zeros((steps // every + 1, len(record), k), np.float32)
    active, peak, dn = np.zeros((n, k), bool), np.zeros((n, k)), np.zeros(k)

    def f(r, t):
        drive = stim * (pulse[0] <= t <= pulse[1])
        act = np.maximum(p["rmax"] * np.tanh((p["a"] / p["rmax"]) * (drive + Wb @ r - p["theta"])), 0.0)
        return (act - r) / p["tau"]
    for s in range(steps):
        t = s * v.DT
        if s % every == 0:
            i = s // every
            rec[i] = r[record]
            if i < first:
                active |= r > 0
                np.maximum(peak, r, out=peak)
            if t >= 0.5:
                dn += r[j]
        k1 = f(r, t)
        k2 = f(r + 0.5 * v.DT * k1, t + 0.5 * v.DT)
        k3 = f(r + 0.5 * v.DT * k2, t + 0.5 * v.DT)
        k4 = f(r + v.DT * k3, t + v.DT)
        r = r + v.DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    rec[-1] = r[record]
    saves_after = sum(1 for s in range(0, steps, every) if s * v.DT >= 0.5)
    return {"rates": rec, "active": active.sum(0), "high": (peak > a1.HIGH_HZ).sum(0), "dn_hz": dn / max(saves_after, 1)}


def condition(W, table, j: int, reps: int, seed: int, mn: np.ndarray) -> dict:
    """Neuron j at every drive of the grid, the same replicates' parameters at each (drives as column blocks)."""
    p = v.params(table, np.random.default_rng(seed), reps)
    p = {x: np.tile(y, (1, len(DRIVES))) for x, y in p.items()}
    stim = np.zeros((len(table), reps * len(DRIVES)))
    stim[j] = np.repeat(DRIVES, reps)
    sim = simulate(W, p, stim, mn, j)
    out = {}
    for d, drive in enumerate(DRIVES):
        cols = range(d * reps, (d + 1) * reps)
        per = [v.rhythm(sim["rates"][:, :, c], np.arange(len(mn))) for c in cols]
        rhythmic = [x for x in per if x["score"] > 0.5]
        freqs = [x["freq_hz"] for x in rhythmic if x["freq_hz"] is not None]
        active, high = sim["active"][list(cols)], sim["high"][list(cols)]
        keeps = int(((active >= a1.ACTIVE[0]) & (active <= a1.ACTIVE[1]) & (high <= a1.HIGH)).sum())
        mns = [x["active_mn"] for x in per]
        out[f"{drive:g}"] = {"rhythmic": len(rhythmic), "of": reps, "freq_hz_median": round(float(np.median(freqs)), 1) if freqs else None,
                             "freq_hz": [round(f, 1) for f in freqs], "score_mean": round(float(np.mean([x["score"] for x in per])), 3),
                             "rule_keeps": keeps, "counts": keeps >= reps / 2, "active": [int(active.min()), int(np.median(active)), int(active.max())],
                             "over_100hz": [int(high.min()), int(high.max())], "active_motor_neurons": [int(min(mns)), int(np.median(mns)), int(max(mns))],
                             "dn_hz": round(float(np.mean(sim["dn_hz"][list(cols)])), 1)}
    return out


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    dns = [j for t in ("DNg100", "DNb08") for j in np.flatnonzero(types == t)]
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    nets = {"real": W, **{f"rewired {rw}": nulls.degree_preserving(W, np.random.default_rng(SEED + 500 + rw)) for rw in (1, 2)}}
    results = {"criteria": __doc__, "drives": list(DRIVES), "conditions": {}}
    for ni, (name, net) in enumerate(nets.items()):
        results["conditions"][name] = {}
        for di, j in enumerate(dns):
            r = condition(net, table, j, REPS[types[j]], SEED + 1000 * ni + di, mn)
            results["conditions"][name][inst[j]] = r
            print(name, inst[j], json.dumps({d: (x["rhythmic"], x["freq_hz_median"], x["counts"], x["active_motor_neurons"][1]) for d, x in r.items()}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(results, indent=1))
    real = results["conditions"]["real"]
    dng = [inst[j] for j in dns if types[j] == "DNg100"]
    dnb = [inst[j] for j in dns if types[j] == "DNb08"]
    band = lambda x: x["freq_hz_median"] is not None and a1.FREQ[0] <= x["freq_hz_median"] <= a1.FREQ[1]
    results["DNG100"] = bool(all(any(x["counts"] and x["rhythmic"] >= 24 and band(x) for x in real[d].values()) for d in dng))
    results["DNB08"] = bool(any(x["counts"] and x["rhythmic"] >= 8 for d in dnb for x in real[d].values()))
    results["NULL"] = bool(all(x["rhythmic"] <= 3 for net in ("rewired 1", "rewired 2") for d in dng + dnb
                               for x in results["conditions"][net][d].values() if x["counts"]))
    results["pass"] = bool(results["DNG100"] and results["DNB08"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print({x: results[x] for x in ("DNG100", "DNB08", "NULL", "pass")}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
