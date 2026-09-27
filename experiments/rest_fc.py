"""Exploratory, not pre-registered: how close is the resting brain's functional connectivity to real
flies' before any fitting? Rung 4's starting point.

Data: Turner, Mann & Clandinin 2021 (brainfly.imaging): 20 flies, mean Fisher-z FC over 66 central
regions. Model: the best resting brain from rest_probe.py, which is rung 1's network (shiu_sensory.py,
w_syn = 1.5556 mV) with the mushroom body's measured properties (graded APL, Kenyon cells resting 16 mV
below threshold) and Poisson background of 1 mV kicks at 200 Hz for every neuron. 8 independent
runs ("flies") of 300 s each, imaged as the data were (brainfly.imaging.record and image: regional
activity in 50 ms bins, a GCaMP6s-like kernel, 1.2 Hz frames, then the same FC recipe, dropping the
first 100 frames). The similarity is the Pearson r between the model's and the data's mean FC over
the 2,145 region pairs.
For scale:
  ceiling     r between two halves of the 20 flies (100 random splits): how well flies agree
  structure   r of the data's FC with log(1 + the number of MaleCNS neurons that have at least 5
              synapses in both regions); Turner et al. found structure like this predicts FC well
Also reported: the model's mean rate and share of neurons over 100 Hz, and the per-region-pair
errors that dominate the mismatch.
A rewired control (the same model on a degree-preserving rewiring) was planned and dropped mid-run:
under this background the rewired network runs away (a mean of 78 Hz with 70,000 neurons over 100
Hz, in rest_calibration.py's first rounds), so its 2,400 trial-seconds would take hours, and its FC
would say nothing about wiring. rest_calibration.py's calibrated rewirings are the null that counts.

    python experiments/rest_fc.py            (writes experiments/rest_fc.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import imaging
from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

OUT = Path(__file__).with_name("rest_fc.json")
SECONDS, BIN, RUNS = 300.0, 0.05, 8


def pairs(m: np.ndarray) -> np.ndarray:
    return m[np.triu_indices(len(m), 1)]


def model_fc(matrix, scale, labels, types, weights, seed: int) -> tuple[np.ndarray, dict]:
    brain = HybridBrain(trials=RUNS, w_syn=W_SYN, matrix=matrix, scale=scale, labels=labels, types=types, seed=seed)
    brain.advance(int(round(2.0 / brain.dt)))                                    # settle
    activity = imaging.record(brain, SECONDS, weights, bin=BIN)                  # (runs, regions, bins)
    frames = {f"run {b}": imaging.image(activity[b], BIN) for b in range(RUNS)}
    fc, each = imaging.connectivity(frames, trims={})
    spikes = brain.advance(int(round(1.0 / brain.dt)))                           # one more second, for rates
    stats = {"mean_hz": round(float(spikes.mean()), 2), "over_100hz": round(float((spikes > 100).mean()), 4)}
    return fc, stats


def main() -> None:
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    scale = 1.0 / sizes(C)
    ty = types.astype(str)
    rest = {"all": {"noise_rate": 200.0, "noise_kick": 1.0}, "APL": {"unit": "graded"},
            **{t: {"threshold": 16.0} for t in sorted({t for t in ty if t.startswith("KC")})}}
    weights = imaging.region_weights()

    data_fc, data_each = imaging.connectivity(imaging.rest_signals(imaging.turner()))
    target = pairs(data_fc)
    rng = np.random.default_rng(0)
    halves = []
    for _ in range(100):
        order = rng.permutation(len(data_each))
        a = np.nanmean(data_each[order[:10]], axis=0)
        b = np.nanmean(data_each[order[10:]], axis=0)
        halves.append(np.corrcoef(pairs(a), pairs(b))[0, 1])
    B = (weights >= 5).astype(np.float32)
    shared = (B.T @ B).toarray()
    results = {"question": __doc__, "regions": imaging.REGIONS,
               "ceiling_split_half_r": round(float(np.mean(halves)), 3),
               "structure_r": round(float(np.corrcoef(target, np.log1p(pairs(shared)))[0, 1]), 3)}
    print(f"ceiling (split-half r) {results['ceiling_split_half_r']}; structure r {results['structure_r']}", flush=True)

    fc, stats = model_fc(M, scale, labels, rest, weights, seed=1)
    results["model"] = {"r": round(float(np.corrcoef(target, pairs(fc))[0, 1]), 3), **stats,
                        "fc_mean_z": round(float(np.nanmean(pairs(fc))), 3), "data_fc_mean_z": round(float(np.nanmean(target)), 3)}
    err = pairs(fc) - target
    worst = np.argsort(-np.abs(err))[:10]
    iu = np.triu_indices(len(data_fc), 1)
    results["model"]["largest_errors"] = [(imaging.REGIONS[iu[0][k]], imaging.REGIONS[iu[1][k]], round(float(err[k]), 2)) for k in worst]
    results["model_fc"] = np.round(fc, 3).tolist()
    print(f"model: r {results['model']['r']} | {json.dumps(stats)} | mean z {results['model']['fc_mean_z']} "
          f"(data {results['model']['data_fc_mean_z']})", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
