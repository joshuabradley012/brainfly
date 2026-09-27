"""Exploratory, not pre-registered: do the looming loop's ignitions come from a point neuron counting
axo-axonic contacts as input?

ignition.py found the resting brain's left LPLC2 either quiet (0.2-0.9 Hz) or running at about 93 Hz,
driving the giant fiber to about 100 Hz, and each fly falls one way or the other at random. The
calibration pushes the loop to that edge, because its quiet state sits below the 2 Hz target. The
right side never ignites. In the model's wiring, 16% of a left LPLC2's input comes from other left
LPLC2s, against 11% on the right (LC4: 7% and 5%). MaleCNS (roi_elements.feather) puts nearly all of
LPLC2's output synapses in the brain in its optic glomerulus in the PVLP (about 25,000 per side,
against about 5,000 in the optic lobe), along with 33,554 of the left LPLC2s' input synapses (29,485
on the right), so most of those contacts are between axon terminals. The left LPLC2s' share is
larger because they have fewer optic-lobe inputs (131,404 against 168,369), and rung 1 divides each
synapse by its target's input count. A neuron's own axon terminals are electrically far from
where it starts its spikes, but a point neuron takes every synapse as input to the cell. Here every
synapse between two visual projection neurons of the same type is removed, a rule for every such
type rather than a patch for this loop, and every other synapse keeps its weight (the division by
input count is unchanged). Otherwise as ignition.py (eyes_at_rest.py's setup, 12 fresh-start rounds
from its eyes-open biases, 32 flies on seeds 1, 11, 12 and 13), for escape_at_rest.py's model and for
the same with the visual projection neurons depressed mildly and fast (0.95 / 0.3 s). Also, eyes_at_rest.py's
looming tests at gain 1 on seed 1 (seed 2, which confirms, isn't used).

    python experiments/vpn_axoaxonic.py            (writes experiments/vpn_axoaxonic.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import depression_classes as classes
import eyes_at_rest as eyes
import ignition
import rest_calibration as attempt1
import rest_calibration2 as attempt2

OUT = Path(__file__).with_suffix(".json")
FULL_NETWORK = attempt1.network


def without_same_type_vpn():
    M, scale, labels, types, superclass = FULL_NETWORK()
    M = M.tocoo()
    vpn = superclass == "visual_projection"
    drop = vpn[M.row] & vpn[M.col] & (types[M.row] == types[M.col]) & (types[M.row] != "")
    return sparse.csr_matrix((M.data[~drop], (M.row[~drop], M.col[~drop])), shape=M.shape), scale, labels, types, superclass


def removed_share() -> dict:
    M, scale, labels, types, superclass = FULL_NETWORK()
    W = abs(M.tocsr().multiply(scale[:, None])).tocsr()
    kept = abs(without_same_type_vpn()[0].tocsr().multiply(scale[:, None])).tocsr()
    side, vpn = labels["side"], superclass == "visual_projection"
    out = {"visual projection neurons' input": round(float(1 - kept[vpn].sum() / W[vpn].sum()), 4)}
    for t in ("LPLC2", "LC4"):
        for s in "LR":
            rows = np.flatnonzero((types == t) & (side == s))
            out[f"{t} {s}"] = round(float(1 - kept[rows].sum() / W[rows].sum()), 4)
    return out


def measure(label: str, model) -> dict:
    attempt2.model, eyes.ROUNDS = model, ignition.ROUNDS["12 rounds"]
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(eyes.HERE / "intact.npz")["bias"]
    log = s.calibrate()
    fly = {k: [] for k in s.cells if k.split()[0] in ignition.LIMIT}
    for seed in ignition.SEEDS:
        rates = s.run(lambda t: [], 1.0, seed, window=(eyes.SCENE - eyes.LATE, eyes.SCENE))["rates"]
        for k in fly:
            fly[k] += np.round(rates[:, s.cells[k]].mean(1), 1).tolist()
    hot = np.zeros(len(ignition.SEEDS) * eyes.TRIALS, bool)
    for k, v in fly.items():
        hot |= np.asarray(v) > ignition.LIMIT[k.split()[0]]
    v = eyes.loom_tests(s, 1.0, seed=1)
    return {"model": label, "last_round": log[-1], "ignited_flies": int(hot.sum()), "flies": len(hot), "per_fly_hz": fly,
            "looming": {k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")},
            "giant_fiber_rise_hz": {k: x["delta"] for k, x in v["escape"].items() if "near" not in k},
            "relay_rise_hz": {k: x["delta"] for k, x in v["relay"].items()}}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "removed_share_of_input": removed_share(), "runs": []}
    print(out["removed_share_of_input"], flush=True)
    attempt1.network = without_same_type_vpn
    for label, model in (("escape_at_rest.py's model", classes.class_model(0.5, 0.0)),
                         ("the same, VPNs 0.95 / 0.3 s", classes.class_model(0.5, 0.0, {"depression": 0.95, "recovery": 0.3}))):
        out["runs"].append(r := measure(label, model))
        print(json.dumps({k: v for k, v in r.items() if k != "per_fly_hz"}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
