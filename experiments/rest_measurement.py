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
(the flies' regions co-fluctuate far more strongly than any model's). And since that suggests a
signal shared across the brain: independent firing plus one slow signal that every neuron carries
equally, scaled so its FC's mean matches the flies' (mean z 0.29), under each weighting. No network,
no wiring beyond which regions each neuron reaches. Finally, what that best null leaves (the flies'
FC minus it, under presence weighting) against how strongly two regions are wired together (log of
the synapses between neurons, split by each neuron's share of its synapses in each region), raw and
with the number of shared neurons partialled out; and against attempt 2's network-made FC (its FC
minus its own measurement-only FC).

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
    here = Path(__file__).parent
    ind = imaging.measurement_only(W)
    models = {}
    for label, path in (("uncalibrated (rest_fc.py)", here / "rest_fc.json"),
                        ("attempt 1", here / "rest_calibration" / "intact.json"),
                        ("attempt 2", here / "rest_calibration2" / "intact.json"),
                        ("attempt 2, rewired 1", here / "rest_calibration2" / "rewired-1.json"),
                        ("attempt 2, rewired 2", here / "rest_calibration2" / "rewired-2.json")):
        d = json.loads(path.read_text())
        fc = np.array(d["model_fc"] if "model_fc" in d else d["fc"], float)
        models[label] = {"r": r(fc), "r_with_its_measurement_only_fc": round(float(np.corrcoef(pairs(fc), pairs(ind))[0, 1]), 3),
                         "mean_z": round(float(np.nanmean(pairs(fc))), 3)}
    def shared(Wv, alpha):
        Wn = sparse.csr_matrix(Wv @ sparse.diags(1 / np.maximum(np.asarray(Wv.sum(0)).ravel(), 1)))
        cov = (Wn.T @ Wn).toarray()
        g = np.asarray(Wn.sum(0)).ravel()                    # every neuron carries the shared signal equally
        cov = cov + alpha * np.outer(g, g)
        sd = np.sqrt(np.diag(cov))
        c = cov / np.outer(sd, sd)
        np.fill_diagonal(c, np.nan)
        return np.arctanh(np.clip(c, -1 + 1e-9, 1 - 1e-9))

    goal = float(np.nanmean(target))
    with_shared = {}
    for name, Wv in weightings.items():
        lo, hi = 1e-9, 1e3                                   # the shared signal's size that matches the flies' mean z
        for _ in range(60):
            mid = np.sqrt(lo * hi)
            lo, hi = (mid, hi) if np.nanmean(pairs(shared(Wv, mid))) < goal else (lo, mid)
        with_shared[name] = r(shared(Wv, np.sqrt(lo * hi)))
    from brainfly.shiu import counts

    P = weightings["present (5 or more synapses)"]
    lo, hi = 1e-9, 1e3
    for _ in range(60):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if np.nanmean(pairs(shared(P, mid))) < goal else (lo, mid)
    resid = target - pairs(shared(P, np.sqrt(lo * hi)))
    share = sparse.diags(1 / np.maximum(np.asarray(W.sum(1)).ravel(), 1)) @ W
    R = (share.T @ abs(counts()).tocsr().T @ share).toarray()
    iu = np.triu_indices(len(data_fc), 1)
    wired = np.log1p(R + R.T)[iu]
    overlap = np.log1p((P.T @ P).toarray()[iu])
    partial = lambda a, b, z: float(np.corrcoef(a - np.polyval(np.polyfit(z, a, 1), z), b - np.polyval(np.polyfit(z, b, 1), z))[0, 1])
    a2 = np.array(json.loads((here / "rest_calibration2" / "intact.json").read_text())["fc"], float)
    residual = {"r_with_wiring": round(float(np.corrcoef(resid, wired)[0, 1]), 3),
                "r_with_wiring_given_shared_neurons": round(partial(resid, wired, overlap), 3),
                "r_with_attempt2_network_made_fc": round(float(np.corrcoef(resid, pairs(a2) - pairs(ind))[0, 1]), 3)}
    out = {"question": __doc__, "independent_firing_r_by_weighting": independent, "what_the_best_null_leaves": residual,
           "independent_firing_plus_a_shared_signal_r_by_weighting": with_shared, "models": models,
           "mean_z": {"flies": round(float(np.nanmean(target)), 3), "independent firing": round(float(np.nanmean(pairs(ind))), 3)}}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "question"}, indent=1))


if __name__ == "__main__":
    main()
