"""Post hoc, not pre-registered: does eyepath_filled.py's closest setting replicate on fresh seeds?

eyepath_filled.py's optic set (graded_gain 0.15, graded_release 0.3, retina filled) failed RELAY only
on LC4 (+2.7 Hz against 3), and passed the secondary ESCAPE criterion: the same-side giant fiber rose
about 3 Hz from looming seen through the eyes. No config passed, so the pre-registered procedure ran no
confirmation. This re-runs that one setting on seeds 3 and 4 with 8 flies each, scored by
eyepath_filled.py's criteria.

    python experiments/eyepath_filled_replication.py      (writes experiments/eyepath_filled_replication.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from eyepath import GRADED, SCENES
from eyepath_filled import N0, measure, run_config

OUT = Path(__file__).with_name("eyepath_filled_replication.json")


def main() -> None:
    ref = FlyBrain(batch=8)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    pop = np.flatnonzero(~optic)
    rest_ref = measure(ref, SCENES["blank"], False, 3, pop)["rest_pop_hz"]
    del ref
    brain = FlyBrain(batch=8, graded=GRADED["optic"], fill_retina=True)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    out = {}
    for seed in (3, 4):
        v = run_config(brain, True, seed, pop, rest_ref)
        out[seed] = {k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE", "relay", "escape", "rest_hz", "rest_pop_hz", "graded_at_bounds")}
        print(f"seed {seed}: REST {v['REST']} RELAY {v['RELAY']} SIDE {v['SIDE']} ESCAPE {v['ESCAPE']}", flush=True)
        print("   relay ", {k: (x["delta"], x["t"]) for k, x in v["relay"].items()}, flush=True)
        print("   escape", {k: (x["delta"], x["t"]) for k, x in v["escape"].items()}, flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
