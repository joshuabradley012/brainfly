"""Rung 5, attempt 2 (pre-registered): does brainfly's nerve cord, by Pugliese et al.'s recipe, turn DNg100 into leg
rhythms at walking frequencies and DNb08 into leg rhythms, and does scrambled wiring abolish both?

Attempt 1 (rung5_vnc.py, pre-registered) passed DNG100 (rhythmic in 30 and 31 of 32 replicates, at 13.7 and 11.6 Hz)
and NULL, and failed DNB08 on frequency alone. One DNb08 neuron (VES082, left) was rhythmic in 10 of 16 replicates,
but at a median 18.2 Hz, against the 7-15 Hz band it asked of both DNs. That band is walking's stepping frequency.
DNg100 makes decapitated flies walk; DNb08 makes them move their front and middle legs in searching movements, whose
frequency no study gives. Pugliese et al. report none, in simulation or in flies, and they call a DNb08 replicate
rhythmic on the rhythmicity score alone. So this attempt asks DNb08 for a rhythm at any frequency. That change was
decided after seeing attempt 1's result, which is why it is a new attempt on new seeds rather than a re-reading of
the old run. With a looser DNb08 criterion it also adds a scrambled-wiring control for DNb08.
Model, drives and score: attempt 1's exactly (rung5_vnc.condition and tuned_drive; the front legs' neuromere network,
4,309 neurons, brainfly's signed synapse counts with connections under 5 dropped, their neuron volumes, rate model and
parameter distributions), drawn from seeds no earlier run used (base 7000). DNg100 each side alone at 400, 32
replicates. Each of the four DNb08 neurons alone, 16 replicates, its drive set replicate by replicate by their DN
screen's rule. A replicate is rhythmic when the active leg motor neurons' rhythmicity score passes 0.5; its frequency
is the autocorrelation's most prominent peak.
Tests:
  DNG100  each DNg100 is rhythmic in at least 24 of its 32 replicates, at a median frequency of 7-15 Hz
  DNB08   at least one DNb08 neuron is rhythmic in at least 8 of its 16 replicates (frequency reported, not tested)
  NULL    in each of 2 degree-preserving rewirings (brainfly.nulls): each DNg100 is rhythmic in at most 3 of 32
          replicates, and each DNb08 neuron, its drive set by the same rule in the rewired network, in at most 3 of 16
Pass: all three.
Reported: as attempt 1, plus the DNb08 frequencies and the motor modules of its rhythmic replicates.

    python experiments/rung5_vnc2.py            (writes experiments/rung5_vnc2.json)
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
SEED = 7000


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    results = {"criteria": __doc__, "dng100": {}, "dnb08": {}, "nulls": []}
    dng100, dnb08 = np.flatnonzero(types == "DNg100"), np.flatnonzero(types == "DNb08")
    show = lambda r, drop: json.dumps({x: r[x] for x in r if x not in drop})
    for k, j in enumerate(dng100):
        results["dng100"][inst[j]] = r = a1.condition(W, table, j, v.STIM, a1.DNG100_REPS, SEED + k)
        print(inst[j], show(r, ("replicates", "drive")), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    for k, j in enumerate(dnb08):
        seed = SEED + 100 + k
        drive = a1.tuned_drive(W, table, j, a1.DNB08_REPS, seed)
        results["dnb08"][inst[j]] = r = a1.condition(W, table, j, drive, a1.DNB08_REPS, seed)
        print(inst[j], show(r, ("replicates",)), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    for rw in (1, 2):
        Wr = nulls.degree_preserving(W, np.random.default_rng(SEED + 1000 + rw))
        entry = {"rewiring": rw}
        for k, j in enumerate(dng100):
            entry[inst[j]] = r = a1.condition(Wr, table, j, v.STIM, a1.NULL_REPS, SEED + 200 + 10 * rw + k)
            print("rewired", rw, inst[j], show(r, ("replicates", "drive")), flush=True)
        for k, j in enumerate(dnb08):
            seed = SEED + 300 + 10 * rw + k
            drive = a1.tuned_drive(Wr, table, j, a1.DNB08_REPS, seed)
            entry[inst[j]] = r = a1.condition(Wr, table, j, drive, a1.DNB08_REPS, seed)
            print("rewired", rw, inst[j], show(r, ("replicates",)), flush=True)
        results["nulls"].append(entry)
        OUT.write_text(json.dumps(results, indent=1))

    band = lambda r: r["freq_hz_median"] is not None and a1.FREQ[0] <= r["freq_hz_median"] <= a1.FREQ[1]
    results["DNG100"] = bool(all(r["rhythmic"] >= 24 and band(r) for r in results["dng100"].values()))
    results["DNB08"] = bool(any(r["rhythmic"] >= 8 for r in results["dnb08"].values()))
    results["NULL"] = bool(all(e[inst[j]]["rhythmic"] <= 3 for e in results["nulls"] for j in dng100)
                           and all(e[inst[j]]["rhythmic"] <= 3 for e in results["nulls"] for j in dnb08))
    results["pass"] = bool(results["DNG100"] and results["DNB08"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print({x: results[x] for x in ("DNG100", "DNB08", "NULL", "pass")}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
