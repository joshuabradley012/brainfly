"""Exploratory, not pre-registered: which neurons does rest_calibration.py's per-type calibration leave
over 100 Hz, and why?

With a condition's final biases (default: intact), 8 trials run 5 s after 2 s to settle. For each group
(type, or superclass when untyped) with hot neurons: its size, how many are hot, its target, its bias
(and whether that sits at the -30 mV floor), its mean rate and its hot members' mean, and how much
of the hot members' excitatory drive (synapses x presynaptic rate) comes from other hot neurons.
A group that is hot on average with its bias at the floor is beyond per-type calibration; a few
hot neurons in a group near its target are beyond per-type parameters; hot neurons fed mostly by
hot neurons are a loop.

    python experiments/rest_hot.py [condition]            (writes experiments/rest_hot.json)
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import numpy as np

from brainfly.hybrid import HybridBrain
from rest_calibration import BACKGROUND, HERE, LOW, SETTLE, TRIALS, network, targets
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "intact"
    M, scale, labels, types, superclass = network()
    key = np.where(types != "", types, np.char.add("superclass:", superclass))
    names, gid = np.unique(key, return_inverse=True)
    saved = np.load(HERE / f"{name}.npz")
    assert np.array_equal(saved["groups"], names), "groups differ from the calibration's"
    bias = saved["bias"]
    target = targets(types, superclass, 2.0 if not name.startswith("default-") else float(name[8:-2]))
    brain = HybridBrain(trials=TRIALS, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=77,
                        types={"all": BACKGROUND, "APL": {"unit": "graded"}}, bias=bias[gid])
    brain.advance(int(round(SETTLE / brain.dt)))
    rate = brain.advance(int(round(5.0 / brain.dt))).mean(0) / 5.0
    hot = rate > 100
    W = M.tocsr().multiply(scale[:, None]).tocsr()                      # rows postsynaptic, as HybridBrain scales them
    exc = W.maximum(0).tocsr()
    drive_all = exc @ rate
    drive_hot = exc @ np.where(hot, rate, 0.0)
    size = np.bincount(gid)
    group_rate = np.bincount(gid, weights=rate) / size
    rows = []
    for g, n_hot in collections.Counter(gid[hot]).most_common():
        members = gid == g
        mh = members & hot
        rows.append({"group": str(names[g]), "size": int(size[g]), "hot": int(n_hot),
                     "target_hz": round(float(target[members].mean()), 2), "bias_mv": round(float(bias[g]), 2),
                     "at_floor": bool(bias[g] <= LOW), "group_hz": round(float(group_rate[g]), 1),
                     "hot_members_hz": round(float(rate[mh].mean()), 1),
                     "superclass": collections.Counter(superclass[mh]).most_common(1)[0][0],
                     "drive_from_hot": round(float(drive_hot[mh].sum() / max(drive_all[mh].sum(), 1e-9)), 3)})
    out = {"question": __doc__, "condition": name, "mean_hz": round(float(rate.mean()), 3), "hot": int(hot.sum()),
           "hot_by_superclass": dict(collections.Counter(superclass[hot]).most_common()),
           "groups_with_hot_neurons": len(rows), "groups_hot_on_average": int(sum(r["group_hz"] > 100 for r in rows)),
           "hot_in_groups_at_floor": int(sum(r["hot"] for r in rows if r["at_floor"])),
           "hot_drive_from_hot": round(float(drive_hot[hot].sum() / max(drive_all[hot].sum(), 1e-9)), 3),
           "groups": rows}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "groups")}))
    for r in rows[:25]:
        print(r)


if __name__ == "__main__":
    main()
