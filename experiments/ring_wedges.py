"""Exploratory, not pre-registered: does evening out each wedge's EPG output free ring_fit2.py's bump from
its favored place?

ring_heldout.py found ring_fit2.py's bump spending about 40% of its time near wedges 1-2. MaleCNS wedges
hold 2 to 4 EPGs each (wedges 0 and 3 hold 4), and ring_fit2.py's wedge normalization (every synapse from
an EPG times (the mean number of EPGs per wedge / the number in its wedge) to the power b) ended at
b = 0.39. Here ring_fit2.py's best with b = 0.39, 0.7 and 1 (every wedge's EPGs giving the same total
output): 8 runs of 60 s on seed 2, the bump's position entropy over the 16 wedges (as ring_fit2.py) and
rung 4's bump measures.

    python experiments/ring_wedges.py            (writes experiments/ring_wedges.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_fit
from ring_homeostasis import entropy_of

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    p0 = json.loads(ring_fit.OUT.with_name("ring_fit2.json").read_text())["best"]["params"]
    out = {"question": __doc__, "conditions": []}
    for b_norm in (0.39, 0.7, 1.0):
        r = ring_fit.Ring(dict(p0, wedge_norm=b_norm), 8, seed=2)
        b = r.brain
        b.advance(int(round(2.0 / b.dt)))
        w = np.stack([b.advance(int(round(1.0 / b.dt)))[:, r.epg] for _ in range(60)], 1)
        bump = attempt1.bump(w, r.side, r.glom, np.random.default_rng(7))
        h, hist = entropy_of(w, r.wedge)
        out["conditions"].append(row := {"wedge_norm": b_norm, "position_entropy": round(h, 3), "position_histogram": np.round(hist, 3).tolist(),
                                         "strength": [bump[s]["strength"] for s in "LR"], "resultant": [bump[s]["resultant"] for s in "LR"]})
        print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
