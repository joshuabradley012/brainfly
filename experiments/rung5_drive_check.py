"""Exploratory, not pre-registered: how much do rung 5's two attempts depend on the descending neurons' drive?

A review (2026-10-09) found two things in rung5_vnc.py and rung5_vnc2.py that the drive decides:
  - DNb08's drive comes from Pugliese et al.'s DN screen rule (halve it if more than 1,500 neurons are active or more
    than 100 fire over 100 Hz, double it if fewer than 5 are active), started at 128. Pugliese et al. give no starting
    value (their DNb08 drives were 65 in MANC and 180 in FANC), and in both attempts the rule kept 128 for every
    replicate, so 128 decided DNb08's result.
  - DNg100's scrambled-wiring null drives the rewired network at 400, the drive suited to the real network, and every
    null run had about 100 of 130 motor neurons active, where the real network has 4-9. A network that saturated
    can't oscillate, so the null may be abolishing the rhythm by running away rather than by losing the wiring.
Here, on each attempt's own network and seeds:
  - DNg100's nulls (the same rewirings, seeds and 32 replicates) with the drive tuned by the same rule, started at 400,
    as attempt 2 tuned DNb08's nulls;
  - every DNb08 neuron at 256, which the review found the rule also keeps for the left VES082 neuron, 16 replicates on
    its attempt's seeds, with the rule's verdict on 256 from the run's first second (identical to the rule's 1 s run).
Reported as the attempts' criteria read them: rhythmic replicates (score over 0.5) and their median frequency.

Ran: both attempts' verdicts turn on the drive, on both sides of the test.
  - DNb08 at 256, which the rule keeps for every replicate of the left VES082 neuron: that neuron is rhythmic in 16 of
    16 replicates at 13.6 Hz in attempt 1 and 15 of 16 at 13.3 Hz in attempt 2, against 10 of 16 at 18.2 Hz and 4 of
    16 at 17.0 Hz at 128. Either would pass both attempts' DNB08 test, and attempt 1 as a whole. The other three stay
    weak: the left VES083 in 6 and 3 of 16 (17.0 and 16.9 Hz), the right two in 0-1 (for the right VES083 the rule
    would halve 256 in 6 of 16 replicates). DNb08 itself fires 52-64 Hz at 256.
  - DNg100's nulls with their drive tuned by the rule: it settles at 137.5-250 (from 400), where the rewired networks
    barely reach the motor neurons (a median of 0-1 active, at most 15). Seven of the eight conditions are never
    rhythmic, but in attempt 2's first rewiring the right DNg100 is rhythmic in 13 of 32 replicates, slowly (5.8 Hz,
    5.2-6.8), more than the null's limit of 3. At 400 the same rewired networks ran away (98-110 of 130 motor neurons
    active) and were never rhythmic.
So at the drive the rule kept, DNb08 failed both attempts; at another the rule accepts, it would have passed; and had
DNg100's nulls been tuned as attempt 2 tuned DNb08's, attempt 2's null would have failed. Neither was pre-registered,
so the recorded verdicts stand. A third attempt needs one drive policy, for the real and rewired networks alike, fixed
in advance.

    python experiments/rung5_drive_check.py        (writes experiments/rung5_drive_check.json)
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
ATTEMPTS = {"attempt 1": 5000, "attempt 2": 7000}
DNB08_DRIVE = 256.0


def tuned(W, table, j: int, reps: int, seed: int, start: float) -> np.ndarray:
    """rung5_vnc.tuned_drive, started at `start` instead of its 128."""
    saved, a1.START_DRIVE = a1.START_DRIVE, start
    try:
        return a1.tuned_drive(W, table, j, reps, seed)
    finally:
        a1.START_DRIVE = saved


def summary(r: dict) -> dict:
    return {x: r[x] for x in ("rhythmic", "of", "score_mean", "freq_hz_median", "freq_hz")}


def rule_on(table, rates: np.ndarray) -> dict:
    """The screen rule's verdict on each replicate's first second (rates: time x neurons x replicates)."""
    first = rates[: int(round(1.0 / v.SAVE))]
    active = (first.sum(0) > 0).sum(0)
    high = (first.max(0) > a1.HIGH_HZ).sum(0)
    keep = (active >= a1.ACTIVE[0]) & (active <= a1.ACTIVE[1]) & (high <= a1.HIGH)
    return {"keeps": int(keep.sum()), "active": [int(active.min()), int(active.max())], "over_100hz": [int(high.min()), int(high.max())]}


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    dng100, dnb08 = np.flatnonzero(types == "DNg100"), np.flatnonzero(types == "DNb08")
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    out = {"question": __doc__, "dng100_null_tuned": {}, "dnb08_at_256": {}}
    for name, seed0 in ATTEMPTS.items():
        for rw in (1, 2):
            Wr = nulls.degree_preserving(W, np.random.default_rng(seed0 + 1000 + rw))
            for k, j in enumerate(dng100):
                seed = seed0 + 200 + 10 * rw + k
                drive = tuned(Wr, table, j, a1.NULL_REPS, seed, v.STIM)
                r = a1.condition(Wr, table, j, drive, a1.NULL_REPS, seed)
                active = [x["active_mn"] for x in r["replicates"]]
                row = {**summary(r), "drive": [float(drive.min()), float(drive.max())],
                       "active_motor_neurons": [int(min(active)), int(np.median(active)), int(max(active))]}
                out["dng100_null_tuned"][f"{name}, rewiring {rw}, {inst[j]}"] = row
                print(name, "rewiring", rw, inst[j], json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
                OUT.write_text(json.dumps(out, indent=1))
        for k, j in enumerate(dnb08):
            seed = seed0 + 100 + k
            p = v.params(table, np.random.default_rng(seed), a1.DNB08_REPS)
            stim = np.zeros((len(table), a1.DNB08_REPS))
            stim[j] = DNB08_DRIVE
            rates = a1.simulate(W, p, stim, v.T)
            per = [v.rhythm(rates[:, :, x], mn) for x in range(a1.DNB08_REPS)]
            freqs = [x["freq_hz"] for x in per if x["score"] > 0.5 and x["freq_hz"] is not None]
            row = {"rhythmic": int(sum(x["score"] > 0.5 for x in per)), "of": a1.DNB08_REPS,
                   "freq_hz_median": round(float(np.median(freqs)), 1) if freqs else None,
                   "freq_hz": [round(f, 1) for f in freqs], "rule": rule_on(table, rates),
                   "active_motor_neurons": [int(min(x["active_mn"] for x in per)), int(np.median([x["active_mn"] for x in per])),
                                            int(max(x["active_mn"] for x in per))],
                   "dn_hz": round(float(rates[int(0.5 / v.SAVE):, j].mean()), 1)}
            out["dnb08_at_256"][f"{name}, {inst[j]}"] = row
            print(name, inst[j], json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
