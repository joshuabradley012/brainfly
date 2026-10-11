"""Exploratory check, not pre-registered and not a rung 5 attempt: does co-driving DNg97 with DNg100 speed the nerve
cord model's front-leg rhythm, as co-activating them speeds headless flies' stepping?

research_notes/Embodied fly connectome simulation/descending_neuron_rates.md: no one has recorded DNg100's or DNg97's
spikes, so rung 5's drives still rest on no data; but in decapitated flies, activating DNg100 alone gives stepping at
about 7.6-8.3 Hz on a ball and 11-12 Hz in air, and adding DNg97 (oDN1) raises ball stepping to about 12 Hz and front-leg
air-stepping to about 21 Hz (Sapkal et al. 2026, read off figures). A model whose rhythm comes from the right circuit
should at least speed up. rung5_vnc3.py: driven at 400 (the only drive at which they count), DNg100 makes 11.6 (right)
and 13.7 Hz (left) front-leg rhythms.
Model: rung5_vnc3.py's (the front legs' neuromere network, 4,309 neurons, brainfly's signed counts, Pugliese et al.'s
volumes, rate model and parameter distributions; rung5_vnc3.simulate and vnc_rhythm.rhythm). Each side separately: that
side's DNg100 at 400 with its DNg97 at 0, 100, 200 and 400 (nothing measures DNg97's rate either), and DNg97 alone at 200
and 400; 16 replicates per condition, the same parameters across the side's conditions, from seeds no earlier run used
(18000 + side).
Measured, per condition: the rhythmic replicates (score above 0.5), their median frequency, the active motor neurons,
the network's active neurons and those above 100 Hz in the first second, and both descending neurons' rates.

Ran (10 minutes): in flies' direction, but much weaker and less robust. DNg100 alone at 400 makes front-leg rhythms in
16 of 16 replicates each side, at 13.0 Hz (left) and 11.4 Hz (right). Adding DNg97 raises the frequency: left to 13.9,
14.5 and 14.9 Hz at DNg97 drives of 100, 200 and 400, right to 11.9, 13.2 and 12.7 Hz, at most 16% (flies' ball stepping
rises about 50%, from about 8 to 12 Hz, and front-leg air-stepping from 11-12 to about 21). But the rhythm falls apart
as DNg97's drive grows: rhythmic in 14, 5 and 2 of 16 on the left and 16, 13 and 3 on the right, as more of the network
joins (median active neurons from 90-116 to 248-478, motor neurons from 4-8 to 11-30). DNg97 alone makes no rhythm at 200
and a slow one at 400 on the right only (7 of 16 at 5.6 Hz), with DNg97 at 10-24 spikes/s. So the model's walking rhythm
comes from DNg100 at one narrow drive and isn't the network flies speed up by recruiting DNg97.

    python experiments/vnc_codrive_check.py      (writes experiments/vnc_codrive_check.json)
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
SEED, REPS = 18000, 16
CONDITIONS = [("DNg100 400", 400.0, 0.0), ("DNg100 400 + DNg97 100", 400.0, 100.0), ("DNg100 400 + DNg97 200", 400.0, 200.0),
              ("DNg100 400 + DNg97 400", 400.0, 400.0), ("DNg97 200 alone", 0.0, 200.0), ("DNg97 400 alone", 0.0, 400.0)]


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
