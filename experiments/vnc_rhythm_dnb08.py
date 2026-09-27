"""Exploratory, not pre-registered: does DNb08 drive leg rhythms in Pugliese et al.'s male CNS nerve cord model at
the drive they used for it?

vnc_rhythm.py drove each descending neuron with 400, Pugliese et al.'s male CNS value for DNg100. DNg100 then gave
12-13 Hz rhythms, but the DNb08 neurons, which are a fifth of DNg100's volume, gave weak scores (0.19-0.26). Since
threshold and gain scale with size, a drive of 400 pushes a DNb08 far past threshold. Pugliese et al. drove one
DNb08 with 65 in MANC, where their DNg100 drive was 250 (400 in the male CNS). This sweeps 65, 104 (65 x 400 / 250)
and 160 for each DNb08 alone, 8 replicates each, with vnc_rhythm.py's model and score.
Ran: little rhythm at 65 and 104 (at most 2 of 8 replicates); at 160 one neuron, DNb08(VES082)_L, is rhythmic in 6 of 8
but at 16.4 Hz. Their paper gives no male CNS drive for DNb08 (their DN screen set drives by a recruitment rule, which
rung5_vnc.py uses) and no DNb08 frequency.

    python experiments/vnc_rhythm_dnb08.py            (writes experiments/vnc_rhythm_dnb08.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import vnc_rhythm as v

OUT = Path(__file__).with_suffix(".json")
DRIVES = [65.0, 104.0, 160.0]


def main() -> None:
    table, W = v.network()
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    v.REPLICATES = 8
    out = {"question": __doc__, "conditions": {}}
    for k, drive in enumerate(DRIVES):
        v.STIM = drive
        for j in np.flatnonzero(types == "DNb08"):
            name = f"{inst[j]} at {drive:g}"
            out["conditions"][name] = r = v.run(W, table, [j], np.random.default_rng(300 + 10 * k + j % 10))
            print(name, json.dumps({x: r[x] for x in r if x != "replicates"}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
