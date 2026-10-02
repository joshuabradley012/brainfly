"""Exploratory, not pre-registered: does the bump even out when the ring's outside input is replaced by its mean?

Alone, the head-direction ring's bump visits every heading evenly (ring_homeostasis.py --slow --fit ring_fit3). Inside
the whole brain it favors wedges 11-13, and neither its loops through the rest of the brain (ring_loops.py) nor the
mean or variance of its outside input by wedge (ring_inputs.py) explain that. This keeps the ring in the whole brain but
gives it its outside input only as a constant.
Model: rung4_anneal.py's intact brain with its averaged offsets (rung4_anneal/intact_state.npz), with every synapse
from a neuron outside the ring onto a ring neuron removed, and each ring neuron's offset raised by that input's mean at
rest, estimated as ring_insitu.tune does (each outside input's rate in a 2-s resting run of this brain, seed 31, times
its weight, its depression's steady efficacy and the synaptic time constant). The ring still drives the rest of the
brain, which no longer feeds back.
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9960): the BUMP measures,
ring_landscape.py's per-wedge occupancy, strength and EPG rates, and the brain's mean rate.
Ran: no. With its outside input only as a constant, the ring's bump still favors part of the ring, now wedges 0-2 and
11-12, and almost never visits wedges 3-7. Position entropy is 0.88 (resultants 0.38 and 0.53), the wedge rates' CV
0.37, EPGs 3.7 Hz. So the fluctuations of outside input aren't the whole story either. The offsets the whole-brain
homeostasis settled on are part of the landscape: they were tuned to the input the ring actually gets, and don't
carry over when it is replaced.

    python experiments/ring_isolated.py            (writes experiments/ring_isolated.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import rest_calibration as attempt1
import ring_insitu
import ring_landscape
import ring_whole
import rung4_anneal as r4a
import taste_escape as te
from brainfly import imaging
from brainfly.hybrid import TAU
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
SEED, REST_SEED = 9960, 31
_subnetwork = ring_whole.subnetwork


def isolated(p):
    """ring_whole.subnetwork(p), then every synapse from outside the ring onto a ring neuron removed."""
    inner = _subnetwork(p)

    def apply(M, types, superclass):
        M, slow, tau_slow = inner(M, types, superclass)
        ring, _ = ring_whole.ring_members(types)
        coo = M.tocoo()
        keep = ~(ring[coo.row] & ~ring[coo.col])                  # rows postsynaptic, columns presynaptic
        print(f"removed {int((~keep).sum())} entries from the rest of the brain onto the ring", flush=True)
        return sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=coo.shape), slow, tau_slow
    return apply


def main() -> None:
    t0 = time.perf_counter()
    p = json.loads((Path(__file__).with_name(f"{ring_insitu.FIT}.json")).read_text())["best"]["params"]
    ring_whole.subnetwork = isolated
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    b, ring = s.brain, st["ring"]
    z = np.load(r4a.HERE / "intact_state.npz")
    s.bias, st["extra"][:] = z["group_bias"].copy(), z["total"] / r4a.ANNEALED
    b.reset(REST_SEED)                                     # the outside inputs' resting rates
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    full = _subnetwork(p)(te.network_for(None)[0], s.types, np.asarray(b.superclass))[0].tocsr()
    mean_in = (full @ np.where(ring, 0.0, rate / (1.0 + (1.0 - f) * rate * tau))) * b.scale * W_SYN * TAU
    st["extra"][:] = np.where(ring, st["extra"] + mean_in, st["extra"])
    print(f"ring neurons' mean outside input: {mean_in[ring].mean():.2f} mV (range {mean_in[ring].min():.2f} to {mean_in[ring].max():.2f})", flush=True)
    b.set_bias(s.bias[s.gid])
    epg, side, glom = attempt1.epgs(s.types)
    _, rates, windows = attempt1.run(b, imaging.region_weights(), epg, seed=SEED)
    r = rates.mean(0)
    spiking = np.ones(b.n, bool)
    spiking[b.graded] = False
    spiking &= ~b.external
    out = {"question": __doc__, "seed": SEED, **ring_landscape.landscape(windows, rates[:, epg], side, glom),
           "mean_hz": round(float(r[spiking].mean()), 3), "over_100hz": round(float((r[spiking] > 100).mean()), 5),
           "ring_group_hz": {g: round(float(r[m].mean()), 2) for g, m in st["groups"].items()},
           "mean_outside_input_mv": round(float(mean_in[ring].mean()), 3), "seconds": round(time.perf_counter() - t0)}
    out["BUMP"] = bool(all(out["bump"][x]["strength"] >= attempt1.MIN_BUMP and out["bump"][x]["strength"] > out["bump"][x]["shuffle_p99"]
                           and out["bump"][x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR") and out["bump_motion"]["MOVES_LIKE_A_FLY"])
    print(json.dumps({k: out[k] for k in ("BUMP", "mean_hz", "bump", "wedge_rate_cv", "wedge_mean_rate_hz", "ring_group_hz")}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
