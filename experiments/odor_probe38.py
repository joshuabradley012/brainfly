"""Exploratory, not pre-registered: what strength of the receptor neurons' synapses onto the antennal lobe's local
neurons gives the LNs flies' odor response?

odor_probe37.py: the presynaptic inhibition still takes hold within 50-150 ms of an odor's onset, even building as slowly
as flies' (two 38 ms stages), because the GABAergic LNs fire about 57 spikes/s each at 50-100 ms and 12-13 over 0.2-0.5 s,
where the mean of 45 LNs in flies fires about 22 over the first 50 ms, 13 at 50-100 ms, 8 at 100-200 ms and 6 at 200-500
ms, from a baseline of about 4 (Nagel et al. 2015, Fig. 5b, 2-heptanone, a fast valve; research_notes/Rung 9 learning
data/pn_ln_dynamics.md). The receptor-to-LN synapses carry rung 4's size rule, which no measurement sets; the
presynaptic inhibition acts only on receptor-to-PN synapses (odor_probe29.py), so the LNs' own odor response can be
set on the built model before the antennal lobe is refitted around it.
Model: odor_probe30.py's brain (brain_cache.py) with every receptor neuron-to-LN synapse (every antennal lobe LN type)
multiplied by s, for s = 1, 0.7, 0.5, 0.35 and 0.25. For each s the LNs' biases are moved (three rounds, each cell by its
rate's distance from its target at 3 spikes/s per mV) so that every GABAergic LN rests at 4/2.8 times its rate in the
built model (their mean then 4 spikes/s, flies' baseline) and every other LN at its rate in the built model.
Measured: the GABAergic LNs' mean rate per cell in Nagel et al.'s bins, 0-50, 50-100, 100-200 and 200-500 ms after the
odor reaches the antenna, for 2-heptanone (Nagel et al.'s odor) and 3-octanol (4 seeds of 8 flies), and the root mean
square of the log ratio to Nagel et al.'s 22, 13, 8 and 6 over the four bins for 2-heptanone. Seeds 350000 + 100 x
scale index (+ round for the rest; + 50 + 10 x odor + seed for the odors).

    python experiments/odor_probe38.py         (writes experiments/odor_probe38.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe21 as p21
import odor_probe24 as p24

OUT = Path(__file__).with_suffix(".json")
SEED = 350000
SCALES = (1.0, 0.7, 0.5, 0.35, 0.25)
ODORS = ("2-heptanone", "3-octanol")
BINS = ((0.0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.5))
NAGEL = (22.0, 13.0, 8.0, 6.0)
REST_HZ, SLOPE = 4.0, 3.0
SEEDS = 4


def psth(o, rec, odor: str, seed: int, inhibitors: np.ndarray) -> list:
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(2.0 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece = int(round(p10.PIECE / b.dt))
    counts = [b.advance(piece, drive=rec.at(plan, k * p10.PIECE))[:, inhibitors].mean() for k in range(50)]
    return [float(np.sum(counts[int(round(a / p10.PIECE)):int(round(z / p10.PIECE))]) / (z - a)) for a, z in BINS]


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    inhibitors = p21.masks(o)["inhibitors"]
    ln = np.array([bool(p14.LN.match(t)) for t in types])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    edges = np.flatnonzero(m["orn"][pre] & ln[b.idx])
    w0, bias0 = b.weights.copy(), o.own_bias()
    rest0 = np.mean([p10.resting(o, rec, SEED + 90 + r)["hz"] for r in range(2)], 0)
    target = rest0.copy()
    target[inhibitors] *= REST_HZ / max(float(rest0[inhibitors].mean()), 1e-9)
    lns = np.flatnonzero(ln)
    out = {"question": __doc__, "flies": {"bins_s": BINS, "nagel_2015_hz": NAGEL, "baseline_hz": REST_HZ},
           "orn_ln_edges": int(len(edges)), "gaba_lns": int(len(inhibitors)), "lns": int(len(lns)),
           "built_rest_hz_gaba_lns": round(float(rest0[inhibitors].mean()), 2), "scales": {}}
    for i, s in enumerate(SCALES):
        w = w0.copy()
        w[edges] *= s
        b.weights, b._external_matrix = w, None
        bias = bias0.copy()
        b.set_bias(bias)
        for r in range(3):
            hz = p10.resting(o, rec, SEED + 100 * i + r)["hz"]
            bias[lns] += (target[lns] - hz[lns]) / SLOPE
            b.set_bias(bias)
        hz = p10.resting(o, rec, SEED + 100 * i + 3)["hz"]
        row = {"rest_hz_gaba_lns": round(float(hz[inhibitors].mean()), 2), "odors": {}}
        for j, odor in enumerate(ODORS):
            runs = [psth(o, rec, odor, SEED + 100 * i + 50 + 10 * j + k, inhibitors) for k in range(SEEDS)]
            row["odors"][odor] = [round(float(x), 2) for x in np.mean(runs, 0)]
        model = np.array(row["odors"]["2-heptanone"])
        row["rms_log_error_2_heptanone"] = round(float(np.sqrt(np.mean(np.log(np.maximum(model, 0.1) / np.array(NAGEL)) ** 2))), 3)
        out["scales"][f"{s:g}"] = row
        print(f"s {s}", json.dumps(row), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = w0, None
    b.set_bias(bias0)
    best = min(out["scales"], key=lambda k: out["scales"][k]["rms_log_error_2_heptanone"])
    out["best_scale"] = float(best)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("best scale", best, flush=True)


if __name__ == "__main__":
    main()
