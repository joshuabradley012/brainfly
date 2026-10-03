"""Exploratory, not pre-registered: can homeostatic synaptic scaling of the ring neurons' outside input even out the
whole-brain bump?

The head-direction ring's bump is even with no input from outside the ring and leans with any substantial share of it,
whether or not that input's mean is cancelled (ring_attribution.py, ring_quiet.py). Homeostasis on each ring neuron's
excitability (an offset, as in ring_insitu.py) can match mean rates but leaves the size of each neuron's input
fluctuations as the connectome gives it. Synaptic scaling (Turrigiano 2008) changes that too. A neuron that fires too
much scales its excitatory synapses down and its inhibitory synapses up; one that fires too little does the opposite.
Here each ring neuron scales only its synapses from outside the ring.
Model: ring_attribution.py's "all" condition. That is ring_insitu.py's brain (brain seed 9) with rung4_anneal.py's
calibrated group biases, every ring neuron's offset from ring_homeostasis.py --slow --fit ring_fit3 lowered by the
mean of its real outside input, and that input kept. Each ring neuron i then gets a factor g_i (from 1) that
multiplies its excitatory synapses from outside the ring and divides its inhibitory ones.
Procedure: 40 rounds, each 2 batches of 8 fresh runs of 40 s after 1 s (round k from seeds 13000 + 10k and
13001 + 10k). Each round, every neuron of the ring's tuned types (ring_insitu.homeostasis's: all but ER and ExR) moves
ln g_i by -step ln((rate + 0.5) / (target + 0.5)), at most step, toward its type's rate in ring_fit3.py's fit. Its rate
is smoothed over rounds (each new round weighted 0.3), and the step falls linearly from 0.2 to 0.02. The offsets don't
change. The mean of ln g over the 40 rounds is kept alongside.
Measured: rung 4's protocol (rest_calibration.run: 8 fresh runs of 300 s after 2 s, seed 9970, as ring_attribution.py)
with the final factors and with the averaged ones: the BUMP measures, ring_landscape.py's per-wedge occupancy and EPG
rates, the ring groups' rates, and the spread of the factors. ring_attribution.py's all, before any scaling: position
entropy 0.85, resultants 0.72 and 0.78.
Ran: yes, with the averaged factors, by the widest margins yet. The position entropy is 0.98, the resultants 0.27 and
0.36, the wedge rates' CV 0.09 (from 0.53), the bump's strength 0.67 and 0.65 against shuffles' 0.36, and D = 0.030
rad^2/s, inside flies' range. With the final round's factors the entropy is 0.94, but one resultant is 0.73, so BUMP
misses, as with ring_anneal.py's final offsets. The EPGs scaled their outside excitatory input by a median of 2.0
(0.46-2.7 across EPGs), and their inhibitory input by the inverse. One measurement from one brain, on the seed
ring_attribution.py used.

    python experiments/ring_scaling.py            (writes experiments/ring_scaling.json; resumes after an interruption)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

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

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
STEPS = np.linspace(0.2, 0.02, 40)
SEED, MEASURE, EMA = 13000, 9970, 0.3


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    p = json.loads(Path(__file__).with_name(f"{ring_insitu.FIT}.json").read_text())["best"]["params"]
    s, st = ring_insitu.build(None, seed=r4a.CONDITIONS["intact"]["brain"])
    b, ring, types, groups = s.brain, st["ring"], s.types, st["groups"]
    s.bias = np.load(r4a.HERE / "intact_state.npz")["group_bias"].copy()
    rates = np.load(Path(__file__).with_name("ring_insitu") / "measure.npz")["rates"].mean(0)
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    full = ring_whole.subnetwork(p)(te.network_for(None)[0], types, np.asarray(b.superclass))[0].tocsr()
    mean_in = (full @ np.where(ring, 0.0, rates / (1.0 + (1.0 - f) * rates * tau))) * b.scale * W_SYN * TAU
    st["extra"][:] = np.where(ring, st["homeo"] - mean_in, 0.0)

    # the synapses from outside the ring onto ring neurons, as entries of the brain's weights (columns presynaptic)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    w0 = b.weights.copy()
    onto = ring[b.idx] & ~ring[pre]
    exc, inh = onto & (w0 > 0), onto & (w0 < 0)

    def scale(log_g: np.ndarray) -> None:
        g = np.exp(log_g)
        w = w0.copy()
        w[exc] *= g[b.idx[exc]]
        w[inh] /= g[b.idx[inh]]
        b.weights = w.astype(np.float32)
        b._external_matrix = None

    target = np.zeros(b.n)
    for gname, hz in st["fit"]["group_hz"].items():
        if gname in groups and gname not in ("ER", "ExR"):
            target[groups[gname]] = hz
    tune = ring & (target > 0)
    epg, side, glom = attempt1.epgs(types)
    state = HERE / "state.npz"
    if state.exists():
        z = np.load(state)
        log_g, smooth, total, first, trace = z["log_g"].copy(), z["smooth"].copy(), z["total"].copy(), int(z["rounds"]), json.loads(str(z["trace"]))
        print("resuming after round", first, flush=True)
    else:
        log_g, smooth, total, first, trace = np.zeros(b.n), None, np.zeros(b.n), 0, []
    for k in range(first, len(STEPS)):
        scale(log_g)
        rate_k, windows = np.zeros(b.n), []
        for batch in range(2):
            b.reset(SEED + 10 * k + batch)
            b.set_release(s.ol.neurons, s.silent)
            b.set_bias(s.bias[s.gid])
            b.advance(int(round(1.0 / b.dt)))
            w = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(40)], 1)      # trials x seconds x n
            rate_k += w.sum((0, 1)) / (40 * eyes.TRIALS * 2)
            windows.append(w[:, :, epg])
        smooth = rate_k if smooth is None else (1 - EMA) * smooth + EMA * rate_k
        step = STEPS[k]
        log_g = np.where(tune, log_g - np.clip(step * np.log((smooth + 0.5) / (target + 0.5)), -step, step), log_g)
        total += log_g
        m = attempt1.bump_motion(np.concatenate(windows), side, glom)
        trace.append({"round": k + 1, "position_entropy": m["position_entropy"], "drift_D": m["drift_D_rad2_per_s"],
                      "epg_hz": round(float(rate_k[epg].mean()), 2), "epg_rate_cv": round(float(rate_k[epg].std() / max(rate_k[epg].mean(), 1e-9)), 3),
                      "g_range": [round(float(np.exp(log_g[tune].min())), 3), round(float(np.exp(log_g[tune].max())), 3)]})
        print(json.dumps(trace[-1]), flush=True)
        np.savez(state, log_g=log_g, smooth=smooth, total=total, rounds=k + 1, trace=json.dumps(trace))
    out = {"question": __doc__, "rounds": trace, "measured": {}}
    for name, lg in (("final", log_g), ("averaged", total / len(STEPS))):
        scale(lg)
        b.set_bias(s.bias[s.gid])
        _, r_runs, windows = attempt1.run(b, imaging.region_weights(), epg, seed=MEASURE)
        r = r_runs.mean(0)
        m = {**ring_landscape.landscape(windows, r_runs[:, epg], side, glom),
             "ring_group_hz": {gname: round(float(r[mm].mean()), 2) for gname, mm in groups.items()},
             "g_by_group": {gname: [round(float(np.exp(lg[mm].min())), 3), round(float(np.exp(np.median(lg[mm]))), 3),
                                    round(float(np.exp(lg[mm].max())), 3)] for gname, mm in groups.items()}}
        bump = m["bump"]
        m["BUMP"] = bool(all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
                             and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR") and m["bump_motion"]["MOVES_LIKE_A_FLY"])
        out["measured"][name] = m
        print(name, json.dumps({k: m[k] for k in ("BUMP", "wedge_rate_cv", "ring_group_hz")}),
              json.dumps({x: (bump[x]["strength"], bump[x]["shuffle_p99"], bump[x]["resultant"]) for x in "LR"}),
              json.dumps({k: v for k, v in m["bump_motion"].items() if k != "position_histogram"}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
