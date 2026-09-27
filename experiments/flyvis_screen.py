"""Exploratory, not pre-registered: which of flyvis's 50 flow models match what is known of the fly's
optic lobe, before any of them drives the brain?

rung3_verdict.py found that flow/0000/001 gets T2 right (it depolarises to light increments and
decrements, as a real T2 does; Keles et al. 2020) but 29 of 32 known contrast polarities and T5a's
direction wrong. This screens every model on three properties that involve flyvis alone:
  T2        the central T2's peak change in the second after a full-field ON and OFF flash (flyvis's
            Flashes, radius 6): both over 0.02, the smaller at least a third of the larger
  POLARITY  the flash response index has the known polarity's sign for how many of flyvis's 32 known
            types (rung 3 asks for 30)
  DIRECTION for the models passing both, flyvis_native.py's direction check on the male eye: how many
            of the 16 T4/T5 subtypes prefer their expected direction (rung 3 asks for all)
A model passing all three is the one to test on looming through the brain, a test it wasn't chosen on.

    python experiments/flyvis_screen.py            (writes experiments/flyvis_screen.json)
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.data import DATA
from brainfly.optic import GRADED as OPTIC, FlyvisNative
from flyvis_native import direction_selectivity

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    os.environ.setdefault("FLYVIS_ROOT_DIR", str(DATA / "flyvis"))
    import flyvis
    from flyvis.analysis.flash_responses import flash_response_index
    from flyvis.analysis.stimulus_responses import flash_responses
    from flyvis.network import EnsembleView
    from flyvis.utils.groundtruth_utils import polarity as known

    known = {k: v for k, v in known.items() if v != 0}
    ens = EnsembleView(flyvis.results_dir / "flow/0000")
    resp = flash_responses(ens, radius=(6,), dt=0.005, batch_size=4)
    fri = flash_response_index(resp, radius=6)
    fri = fri.squeeze("sample") if "sample" in fri.dims else fri
    names = list(fri["network_name"].values)
    cells = list(resp["cell_type"].values)
    t = resp["time"].values
    R = resp["responses"].values                                   # (network, sample, frame, neuron)
    on_sample, off_sample = list(resp["intensity"].values).index(1), list(resp["intensity"].values).index(0)
    j = cells.index("T2")

    def peak(m, sample):
        x = R[m, sample, :, j]
        return float((x[(t >= 0) & (t < 1)] - x[t < 0].mean()).max())

    models = []
    for m, name in enumerate(names):
        on, off = peak(m, on_sample), peak(m, off_sample)
        v = fri.isel(network_id=m).values
        wrong = [ct for ct, pol in known.items() if np.sign(v[cells.index(ct)]) != pol]
        models.append({"model": name, "rank": m, "t2_on": round(on, 3), "t2_off": round(off, 3),
                       "T2": bool(on > 0.02 and off > 0.02 and min(on, off) / max(on, off) >= 1 / 3),
                       "polarity": len(known) - len(wrong), "polarity_wrong": wrong})
    for row in models:
        if row["T2"] and row["polarity"] >= 30:
            ol = FlyvisNative(FlyBrain(batch=1, graded=OPTIC, dt=0.002, refractory=0.004), model=row["model"])
            ds = direction_selectivity(ol)
            row["direction"] = int(sum(v["correct"] for v in ds.values()))
            row["direction_wrong"] = [k for k, v in ds.items() if not v["correct"]]
        print(json.dumps({k: row[k] for k in row if k != "polarity_wrong"}), flush=True)
    passing = [r["model"] for r in models if r["T2"] and r["polarity"] >= 30 and r.get("direction") == 16]
    OUT.write_text(json.dumps({"question": __doc__, "models": models, "passing": passing}, indent=1))
    print("passing all three:", passing, flush=True)


if __name__ == "__main__":
    main()
