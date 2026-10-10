"""Exploratory, not pre-registered: what one strength for all of the local neurons' synaptic inputs gives the GABAergic
LNs flies' odor response?

odor_ln_inputs.py: the GABAergic LNs' onset burst (63 spikes/s per cell at 50-100 ms to 2-heptanone; flies about 22 over
the first 50 ms and 13 at 50-100 ms, Nagel et al. 2015, Fig. 5b) comes from all their inputs at once, receptor neurons,
uniglomerular and other PNs and the LNs themselves, each from its synapses' rested strength, so scaling the receptor
neurons' synapses alone (odor_probe38.py) leaves the onset 2.7 times flies'. None of these strengths is measured; all
carry rung 4's size rule.
Model: odor_probe30.py's brain (brain_cache.py) with every synapse onto every antennal lobe LN (GABAergic and
cholinergic) multiplied by s, for s = 1, 0.6, 0.45, 0.35 and 0.25. For each s the LNs' biases are moved (six rounds,
each cell by its rate's distance from its target at 2 spikes/s per mV) so that every GABAergic LN rests at 4/2.8 times
its rate in the built model (their mean 4 spikes/s, flies' baseline) and every other LN at its rate in the built model;
the presynaptic inhibition stays as built (its offset at the built LNs' resting rate), so the PN measures here only
indicate the direction.
Measured: the GABAergic LNs' mean rate per cell in 50 ms bins over the odor's first 0.55 s, for 2-heptanone (Nagel et
al.'s odor) and 3-octanol (4 seeds of 8 flies); the fit, stated before running, is the root mean square of the log
ratio of the model's 50-100, 100-150, 150-250 and 250-550 ms to flies' 0-50, 50-100, 100-200 and 200-500 ms (22, 13, 8, 6)
for 2-heptanone, the model's bins taken 50 ms later for its receptor neurons' latency (up to 50 ms, where Nagel et
al.'s LNs peak 15-25 ms after their fast valve). Also: 3-octanol's driven uniglomerular PNs in the same bins. Seeds
370000 + 100 x scale index (+ round for the rest; + 50 + 10 x odor + seed for the odors).

    python experiments/odor_probe39.py         (writes experiments/odor_probe39.json)
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
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 370000
SCALES = (1.0, 0.6, 0.45, 0.35, 0.25)
ODORS = ("2-heptanone", "3-octanol")
NAGEL = (22.0, 13.0, 8.0, 6.0)
MODEL_BINS = ((0.05, 0.1), (0.1, 0.15), (0.15, 0.25), (0.25, 0.55))
REST_HZ, SLOPE, ROUNDS, SEEDS = 4.0, 2.0, 6, 4


def course(o, rec, odor: str, seed: int, cells: np.ndarray, pns: np.ndarray) -> tuple:
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(2.0 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece = int(round(p10.PIECE / b.dt))
    ln, pn = [], []
    for k in range(55):
        c = b.advance(piece, drive=rec.at(plan, k * p10.PIECE))
        ln.append(float(c[:, cells].mean()))
        pn.append(float(c[:, pns].mean()) if len(pns) else 0.0)
    return np.array(ln) / p10.PIECE, np.array(pn) / p10.PIECE


def binned(x: np.ndarray, bins) -> list:
    return [float(x[int(round(a / p10.PIECE)):int(round(z / p10.PIECE))].mean()) for a, z in bins]


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    inhibitors = p21.masks(o)["inhibitors"]
    ln = np.array([bool(p14.LN.match(t)) for t in types])
    lns = np.flatnonzero(ln)
    edges = np.flatnonzero(ln[b.idx])                              # every synapse onto an LN
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    oct_pns = np.concatenate([pn_of[g] for g, v in odors.glomeruli("3-octanol").items() if v > 0.2 and g in pn_of])
    w0, bias0 = b.weights.copy(), o.own_bias()
    rest0 = np.mean([p10.resting(o, rec, SEED + 90 + r)["hz"] for r in range(2)], 0)
    target = rest0.copy()
    target[inhibitors] *= REST_HZ / max(float(rest0[inhibitors].mean()), 1e-9)
    bins10 = [(round(0.05 * k, 2), round(0.05 * (k + 1), 2)) for k in range(11)]
    out = {"question": __doc__, "flies": {"nagel_2015_hz": NAGEL, "bins_s": ((0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.5)),
                                          "baseline_hz": REST_HZ},
           "model_bins_s": MODEL_BINS, "ln_edges": int(len(edges)), "lns": int(len(lns)), "gaba_lns": int(len(inhibitors)),
           "built_rest_hz_gaba_lns": round(float(rest0[inhibitors].mean()), 2), "scales": {}}
    for i, s in enumerate(SCALES):
        w = w0.copy()
        w[edges] *= s
        b.weights, b._external_matrix = w, None
        bias = bias0.copy()
        b.set_bias(bias)
        for r in range(ROUNDS):
            hz = p10.resting(o, rec, SEED + 100 * i + r)["hz"]
            bias[lns] += (target[lns] - hz[lns]) / SLOPE
            b.set_bias(bias)
        hz = p10.resting(o, rec, SEED + 100 * i + ROUNDS)["hz"]
        row = {"rest_hz_gaba_lns": round(float(hz[inhibitors].mean()), 2), "rest_hz_other_lns": round(float(hz[np.setdiff1d(lns, inhibitors)].mean()), 2),
               "odors": {}}
        for j, odor in enumerate(ODORS):
            runs = [course(o, rec, odor, SEED + 100 * i + 50 + 10 * j + k, inhibitors, oct_pns) for k in range(SEEDS)]
            lnr, pnr = np.mean([r[0] for r in runs], 0), np.mean([r[1] for r in runs], 0)
            row["odors"][odor] = {"ln_hz_50ms": [round(x, 1) for x in binned(lnr, bins10)],
                                  "ln_hz_nagel_bins": [round(x, 2) for x in binned(lnr, MODEL_BINS)]}
            if odor == "3-octanol":
                row["odors"][odor]["oct_pn_hz_50ms"] = [round(x, 1) for x in binned(pnr, bins10)]
        model = np.array(row["odors"]["2-heptanone"]["ln_hz_nagel_bins"])
        row["rms_log_error"] = round(float(np.sqrt(np.mean(np.log(np.maximum(model, 0.1) / np.array(NAGEL)) ** 2))), 3)
        out["scales"][f"{s:g}"] = row
        print(f"s {s}", json.dumps({k: row[k] for k in ("rest_hz_gaba_lns", "rms_log_error")}),
              json.dumps(row["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(row["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = w0, None
    b.set_bias(bias0)
    out["best_scale"] = float(min(out["scales"], key=lambda k: out["scales"][k]["rms_log_error"]))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("best scale", out["best_scale"], flush=True)


if __name__ == "__main__":
    main()
