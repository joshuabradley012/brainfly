"""Exploratory check, not pre-registered and not a rung 5 attempt: between the drive at which rung 5's third attempt
found DNg100 rhythmic (400) and the one at which the network ran away (800), where is the front legs' rhythm, and at
what rates does DNg100 fire there?

rung5_vnc3.py drove DNg100 at 50, 100, 200, 400 and 800 only: at 400 (DNg100 at about 16 spikes/s) the right one was
rhythmic in 32 of 32 replicates and the left in 23; at 800 about half the network was active. research_notes/Embodied fly
connectome simulation/descending_neuron_rates.md: walking descending neurons recorded whole-cell fire about 20-60
spikes/s, which would put DNg100 at drives of about 460-800 (no one has recorded DNg100 itself). vnc_codrive_check.py: the
model's rhythm speeds up only a little with DNg97 and falls apart as more of the network joins.
Model and measures: vnc_codrive_check.py's, DNg100 alone at 300, 400, 450, 500, 550, 600 and 700, 16 replicates per side
(seeds 18100 + side, the same parameters at every drive).

Ran (12 minutes): the rhythm lives in a narrow window, below the rates walking descending neurons reach. Right DNg100:
rhythmic in 15, 16 and 14 of 16 replicates at drives 300, 400 and 450 (9.3, 11.6 and 11.8 Hz), with DNg100 at 11.0, 17.5
and 20.2 spikes/s; at 500, 7 of 16, with 1,498 of the network's neurons active; from 550 the network runs away (2,000+
active, about 800 above 100 Hz) and no replicate is rhythmic from 600. Left: 1, 14 and 7 of 16 at 300, 400 and 450 (6.5,
13.0 and 13.7 Hz; DNg100 at 10.4, 16.6 and 19.3 spikes/s), 3 at 500 (with 53 motor neurons active and a slow 1.4 Hz
rhythm), then runaway. As the network runs away it silences DNg100 itself (7.4, 0.9 and 0 spikes/s on the left at 550,
600 and 700). So the model's front-leg rhythm needs DNg100 at about 10-20 spikes/s, the low end of what walking
descending neurons recorded in flies fire (about 20-60), and the network can't take DNg100 any faster.

    python experiments/vnc_drive_sweep.py      (writes experiments/vnc_drive_sweep.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung5_vnc as a1
import rung5_vnc3 as r3
import vnc_rhythm as v
from vnc_own import own_network

OUT = Path(__file__).with_suffix(".json")
SEED, REPS = 18100, 16
CONDITIONS = [(f"DNg100 {d:g}", d, 0.0) for d in (300.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0)]


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    out = {"question": __doc__, "conditions": {}}
    for k, side in enumerate(("L", "R")):
        g100 = int(np.flatnonzero(inst == f"DNg100_{side}")[0])
        g97 = int(np.flatnonzero(inst == f"DNg97_{side}")[0])
        p = v.params(table, np.random.default_rng(SEED + k), REPS)
        p = {x: np.tile(y, (1, len(CONDITIONS))) for x, y in p.items()}
        stim = np.zeros((len(table), REPS * len(CONDITIONS)))
        for c, (_, d100, d97) in enumerate(CONDITIONS):
            stim[g100, c * REPS:(c + 1) * REPS] = d100
            stim[g97, c * REPS:(c + 1) * REPS] = d97
        sim = r3.simulate(W, p, stim, np.concatenate([mn, [g97]]), g100)      # the motor neurons, and DNg97 last
        late = np.arange(sim["rates"].shape[0]) * v.SAVE >= 0.5
        sim97 = sim["rates"][late, len(mn), :].mean(0)
        out["conditions"][side] = {}
        for c, (name, d100, d97) in enumerate(CONDITIONS):
            cols = list(range(c * REPS, (c + 1) * REPS))
            per = [v.rhythm(sim["rates"][:, :len(mn), i], np.arange(len(mn))) for i in cols]
            rhythmic = [x for x in per if x["score"] > 0.5]
            freqs = [x["freq_hz"] for x in rhythmic if x["freq_hz"] is not None]
            active, high = sim["active"][cols], sim["high"][cols]
            row = {"rhythmic": len(rhythmic), "of": REPS, "freq_hz_median": round(float(np.median(freqs)), 1) if freqs else None,
                   "freq_hz": [round(f, 1) for f in freqs], "active_motor_neurons_median": int(np.median([x["active_mn"] for x in per])),
                   "active_median": int(np.median(active)), "over_100hz_median": int(np.median(high)),
                   "rule_keeps": int(((active >= a1.ACTIVE[0]) & (active <= a1.ACTIVE[1]) & (high <= a1.HIGH)).sum()),
                   "dng100_hz": round(float(np.mean(sim["dn_hz"][cols])), 1), "dng97_hz": round(float(np.mean(sim97[cols])), 1)}
            out["conditions"][side][name] = row
            print(side, name, json.dumps({x: row[x] for x in ("rhythmic", "freq_hz_median", "active_motor_neurons_median",
                                                             "active_median", "over_100hz_median", "dng100_hz", "dng97_hz")}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
