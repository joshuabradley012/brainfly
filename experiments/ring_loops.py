"""Exploratory, not pre-registered: is the whole-brain bump's favored region carried by loops through the rest of the
brain?

Alone, the head-direction ring's bump visits every heading evenly (ring_homeostasis.py --slow --fit ring_fit3). Inside
the whole brain it keeps favoring a region even after annealed homeostasis (rung4_anneal.py; ring_landscape.py). The
ring's static input from outside is corrected neuron by neuron (ring_insitu.tune), but loops are not: the ring drives
neurons outside it, and they feed back to it, so where the bump sits can come back as input that depends on where it
sits. This removes those loops at the ring's end and measures the bump.
Model: rung4_anneal.py's intact brain with its averaged offsets (rung4_anneal/intact_state.npz), with every synapse
from a ring neuron onto a neuron outside the ring removed. The rest of the brain still drives the ring but no longer
hears it. Biases and offsets are not recalibrated.
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9950): the BUMP measures,
ring_landscape.py's per-wedge occupancy, strength and EPG rates, and the brain's mean rate. The same brain with its
loops scored position entropy 0.92 and 0.96 on two measurements (resultants 0.64 and 0.71; 0.42 and 0.61), wedge
rates' CV 0.27.
Ran: no. With the loops cut the bump still favors the same region, spending 44% of its time at wedges 11-13 (wedge
rates' CV 0.42). Its position entropy is 0.895 and its resultants 0.50 and 0.56, so BUMP fails, on entropy. Nor does the
ring's input from outside explain the region: across wedges, the mean and the variance of the EPGs' outside input
correlate weakly with where the bump lingers (r = 0.14 and 0.12; ring_inputs.py).

    python experiments/ring_loops.py            (writes experiments/ring_loops.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_insitu
import ring_whole
import ring_landscape
import rung4_anneal as r4a
from brainfly import imaging
from scipy import sparse

OUT = Path(__file__).with_suffix(".json")
SEED = 9950
_subnetwork = ring_whole.subnetwork


def without_loops(p):
    """ring_whole.subnetwork(p), then every synapse from a ring neuron onto a neuron outside the ring removed."""
    inner = _subnetwork(p)

    def apply(M, types, superclass):
        M, slow, tau_slow = inner(M, types, superclass)
        ring, _ = ring_whole.ring_members(types)
        coo = M.tocoo()
        keep = ~(~ring[coo.row] & ring[coo.col])                  # rows postsynaptic, columns presynaptic
        print(f"removed {int((~keep).sum())} entries from the ring onto the rest of the brain", flush=True)
        return sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=coo.shape), slow, tau_slow
    return apply


def main() -> None:
    t0 = time.perf_counter()
    ring_whole.subnetwork = without_loops
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    z = np.load(r4a.HERE / "intact_state.npz")
    s.bias, st["extra"][:] = z["group_bias"].copy(), z["total"] / r4a.ANNEALED
    s.brain.set_bias(s.bias[s.gid])
    epg, side, glom = attempt1.epgs(s.types)
    _, rates, windows = attempt1.run(s.brain, imaging.region_weights(), epg, seed=SEED)
    rate = rates.mean(0)
    spiking = np.ones(s.brain.n, bool)
    spiking[s.brain.graded] = False
    spiking &= ~s.brain.external
    out = {"question": __doc__, "seed": SEED, **ring_landscape.landscape(windows, rates[:, epg], side, glom),
           "mean_hz": round(float(rate[spiking].mean()), 3), "over_100hz": round(float((rate[spiking] > 100).mean()), 5),
           "ring_group_hz": {g: round(float(rate[m].mean()), 2) for g, m in st["groups"].items()},
           "seconds": round(time.perf_counter() - t0)}
    out["BUMP"] = bool(all(out["bump"][x]["strength"] >= attempt1.MIN_BUMP and out["bump"][x]["strength"] > out["bump"][x]["shuffle_p99"]
                           and out["bump"][x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR") and out["bump_motion"]["MOVES_LIKE_A_FLY"])
    print(json.dumps({k: out[k] for k in ("BUMP", "mean_hz", "bump", "wedge_rate_cv", "wedge_mean_rate_hz")}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
