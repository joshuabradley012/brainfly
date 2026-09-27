"""Exploratory, not pre-registered: how much of the flies' resting FC does the measurement explain
before any dynamics, and what does that say about rung 4's tests?

rest_calibration2.py's resting brain matched the flies' FC (Turner et al. 2021) at r = 0.38, below
its own neurons firing independently (0.40) and below calibrated rewirings (0.50). Every FC in rung 4
goes through one forward model (brainfly.imaging): a region's signal is its neurons' activity, each
weighted by its synapses in the region. This asks how much that choice matters, with no dynamics at
all: the FC that independently firing neurons (equal variance) give under other weightings of the
same synapse table, from a neuron's raw synapse count to a mere presence in the region (5 or more
synapses). A weighting closer to a mere presence is closer to how much of a neuron a voxel sees.
Also reported: how much of each model's FC its measurement-only FC explains, and each FC's mean
(the flies' regions co-fluctuate far more strongly than any model's).

    python experiments/rest_measurement.py            (writes experiments/rest_measurement.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly import imaging
from rest_fc import pairs

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target = pairs(data_fc)
    r = lambda m: round(float(np.corrcoef(target, pairs(m))[0, 1]), 3)
    W = imaging.region_weights().tocsr().astype(np.float64)
    weightings = {
        "synapses (brainfly.imaging)": W,
        "sqrt(synapses)": W.sqrt(),
        "log(1 + synapses)": W.log1p(),
        "present (5 or more synapses)": (W >= 5).astype(np.float64),
        "share of the neuron's own synapses": sparse.diags(1 / np.maximum(np.asarray(W.sum(1)).ravel(), 1)) @ W,
    }
    independent = {name: r(imaging.measurement_only(Wv)) for name, Wv in weightings.items()}
    ind = imaging.measurement_only(W)
    models = {}
    here = Path(__file__).parent
    for label, path in (("uncalibrated (rest_fc.py)", here / "rest_fc.json"),
                        ("attempt 1", here / "rest_calibration" / "intact.json"),
                        ("attempt 2", here / "rest_calibration2" / "intact.json"),
                        ("attempt 2, rewired 1", here / "rest_calibration2" / "rewired-1.json"),
                        ("attempt 2, rewired 2", here / "rest_calibration2" / "rewired-2.json")):
        d = json.loads(path.read_text())
        fc = np.array(d["model_fc"] if "model_fc" in d else d["fc"], float)
        models[label] = {"r": r(fc), "r_with_its_measurement_only_fc": round(float(np.corrcoef(pairs(fc), pairs(ind))[0, 1]), 3),
                         "mean_z": round(float(np.nanmean(pairs(fc))), 3)}
    out = {"question": __doc__, "independent_firing_r_by_weighting": independent, "models": models,
           "mean_z": {"flies": round(float(np.nanmean(target)), 3), "independent firing": round(float(np.nanmean(pairs(ind))), 3)}}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "question"}, indent=1))


if __name__ == "__main__":
    main()
