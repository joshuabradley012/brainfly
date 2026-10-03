"""Exploratory, not pre-registered: is the whole-brain bump's lean set by the 2 Hz the calibration gives the unmeasured
neurons that inhibit the EPGs?

ring_attribution.py found that the head-direction ring's input from outside it makes the bump lean, that the EPGs'
share alone is enough, and that the inhibitory part alone gives the whole lean. The neurons outside the ring that
inhibit the EPGs (fan-shaped body and LAL types among them) have no measured resting rate, so the calibration holds them
at its 2 Hz default, and each inhibits only a few wedges.
Model and setup: ring_attribution.py's "all" condition. That is ring_insitu.py's brain (brain seed 9) with
rung4_anneal.py's calibrated group biases, every ring neuron's offset from ring_homeostasis.py --slow --fit ring_fit3
lowered by the mean of its real input from outside the ring, and that input kept.
  epg-inhibition: the synapses from inhibitory neurons outside the ring onto the EPGs removed, and the EPGs' offsets
    lowered only by the mean of the input that remains. Is it the EPGs' inhibitory input, rather than other ring
    neurons'?
  quiet: every cell type outside the ring with an inhibitory synapse onto an EPG gets a resting target of 0.5 Hz in
    place of 2 Hz (types with measured targets keep theirs). The rest of the brain is recalibrated (4 rounds at k = 1 mV
    and 4 at 0.5, calibration round r from seed 7900 + r, the ring held out). The ring's offsets are lowered by the mean
    of its outside input at the new rates (each outside input's rate in a 2-s resting run, seed 33, times its weight,
    its depression's steady efficacy and the synaptic time constant, as ring_insitu.tune).
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9970, as ring_attribution.py):
the BUMP measures, ring_landscape.py's per-wedge occupancy and EPG rates, the ring groups' rates, the brain's mean
rate, and the quieted types' rates. ring_attribution.py's all: position entropy 0.85, resultants 0.72 and 0.78.
Ran: neither. Without the EPGs' inhibitory input from outside the ring, the lean stays (position entropy 0.85,
resultants 0.97 and 0.94). With the 76 types that inhibit the EPGs quieted (they settled at 1.07 Hz rather than 0.5
after 8 rounds), it barely eases (0.89; 0.70 and 0.72). So the 2 Hz default isn't what sets the lean, and the EPGs'
inhibitory input isn't needed for it. Across ring_attribution.py and these runs, the ring is even with no outside
input and leans with any substantial share of it, its mean cancelled or not.

    python experiments/ring_quiet.py epg-inhibition     (writes experiments/ring_quiet/epg-inhibition.json)
    python experiments/ring_quiet.py quiet              (writes experiments/ring_quiet/quiet.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import eyes_at_rest as eyes
import rest_calibration as attempt1
import ring_insitu
import ring_landscape
import ring_whole
import rung4_anneal as r4a
import taste_escape as te
from brainfly import imaging
from brainfly.hybrid import TAU
from shiu_rewiring import W_SYN

HERE = Path(__file__).with_suffix("")
SEED, REST_SEED, CAL_SEED, QUIET_HZ = 9970, 33, 7900, 0.5
_subnetwork = ring_whole.subnetwork


def epg_mask(types: np.ndarray) -> np.ndarray:
    m = np.zeros(len(types), bool)
    m[attempt1.epgs(np.asarray(types).astype(str))[0]] = True
    return m


def inhibitors(M, types: np.ndarray) -> np.ndarray:
    """Neurons outside the ring with an inhibitory synapse onto an EPG (M rows postsynaptic)."""
    ring, _ = ring_whole.ring_members(np.asarray(types).astype(str))
    sub = M.tocsr()[epg_mask(types)].tocoo()
    pre = np.zeros(len(types), bool)
    pre[sub.col[(sub.data < 0) & ~ring[sub.col]]] = True
    return pre


def without_epg_inhibition(p):
    """ring_whole.subnetwork(p), then every synapse from an inhibitory neuron outside the ring onto an EPG removed."""
    inner = _subnetwork(p)

    def apply(M, types, superclass):
        M, slow, tau_slow = inner(M, types, superclass)
        coo = M.tocoo()
        cut = epg_mask(types)[coo.row] & inhibitors(M, types)[coo.col] & (coo.data < 0)
        print(f"removed {int(cut.sum())} inhibitory entries onto the EPGs", flush=True)
        return sparse.csr_matrix((coo.data[~cut], (coo.row[~cut], coo.col[~cut])), shape=coo.shape), slow, tau_slow
    return apply


def main(mode: str) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    p = json.loads(Path(__file__).with_name(f"{ring_insitu.FIT}.json").read_text())["best"]["params"]
    if mode == "epg-inhibition":
        ring_whole.subnetwork = without_epg_inhibition
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    b, ring, types = s.brain, st["ring"], s.types
    s.bias = np.load(r4a.HERE / "intact_state.npz")["group_bias"].copy()
    full = _subnetwork(p)(te.network_for(None)[0], types, np.asarray(b.superclass))[0].tocsr()
    quieted = np.zeros(b.n, bool)
    if mode == "quiet":
        named = np.unique(types[inhibitors(full, types)])
        named = [t for t in named if t and abs(s.target[types == t].mean() - 2.0) < 1e-9]       # only default targets
        quieted = np.isin(types, named)
        s.target = np.where(quieted, QUIET_HZ, s.target)
        print(f"quieting {len(named)} types, {int(quieted.sum())} neurons, to {QUIET_HZ} Hz", flush=True)
        st["extra"][:] = np.where(ring, st["homeo"], 0.0)                                # during the calibration
        eyes.CAL_SEED, eyes.ROUNDS = CAL_SEED, [1.0] * 4 + [0.5] * 4
        log = s.calibrate()
    b.reset(REST_SEED)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
    if mode != "quiet":                                    # the saved resting rates, as ring_attribution.py
        rate = np.load(Path(__file__).with_name("ring_insitu") / "measure.npz")["rates"].mean(0)
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    drive = np.where(ring, 0.0, rate / (1.0 + (1.0 - f) * rate * tau))
    mean_in = (full @ drive) * b.scale * W_SYN * TAU
    if mode == "epg-inhibition":                           # the EPGs no longer get their inhibitory outside input
        inh = inhibitors(full, types)
        mean_in = np.where(epg_mask(types), mean_in - (full.minimum(0) @ np.where(inh, drive, 0.0)) * b.scale * W_SYN * TAU, mean_in)
    st["extra"][:] = np.where(ring, st["homeo"] - mean_in, 0.0)
    b.set_bias(s.bias[s.gid])
    epg, side, glom = attempt1.epgs(types)
    _, r_runs, windows = attempt1.run(b, imaging.region_weights(), epg, seed=SEED)
    r = r_runs.mean(0)
    spiking = np.ones(b.n, bool)
    spiking[b.graded] = False
    spiking &= ~b.external
    out = {"mode": mode, "seed": SEED, **ring_landscape.landscape(windows, r_runs[:, epg], side, glom),
           "mean_hz": round(float(r[spiking].mean()), 3), "over_100hz": round(float((r[spiking] > 100).mean()), 5),
           "ring_group_hz": {g: round(float(r[m].mean()), 2) for g, m in st["groups"].items()},
           "seconds": round(time.perf_counter() - t0)}
    if mode == "quiet":
        out.update({"quieted_types": sorted(set(types[quieted])), "quieted_hz": round(float(r[quieted].mean()), 3),
                    "calibration": log[-1]})
    bump = out["bump"]
    out["BUMP"] = bool(all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                           and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR") and out["bump_motion"]["MOVES_LIKE_A_FLY"])
    print(mode, json.dumps({k: out[k] for k in ("BUMP", "wedge_rate_cv", "mean_hz", "ring_group_hz")}),
          json.dumps({x: (bump[x]["strength"], bump[x]["shuffle_p99"], bump[x]["resultant"]) for x in "LR"}),
          json.dumps({k: v for k, v in out["bump_motion"].items() if k != "position_histogram"}),
          json.dumps({k: out[k] for k in ("quieted_hz",) if k in out}), flush=True)
    (HERE / f"{mode}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
