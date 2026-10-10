"""Exploratory, not pre-registered: on odor_probe30.py's antennal lobe, do the Kenyon cell classes' measured thresholds put
the right classes first, and does MBON11's input come closer to flies'?

odor_probe30.py's antennal lobe brings the Kenyon cells into flies' density (2.4-10.5% respond, mean Jaccard 0.16), but
not their classes: alpha'/beta' cells respond at 0.7-3.9% and gamma cells at 2.5-9.4%, where Turner et al. 2008's flies
show alpha'/beta' most (about 9-14%), alpha/beta 3-8% and gamma about 2%; responding alpha/beta cells fire 4.6-5.7
spikes (flies 2.2 +- 1.2) and alpha'/beta' 1.9-4.5 (4.9 +- 3.0). With MBON11's synapses set from its own measurements
(odor_probe31.py), its Kenyon cell input is 1.5-3.3 times flies' for 3-octanol and 0.3-0.7 times for
4-methylcyclohexanol, the gamma cells, which make 63% of MBON11's Kenyon cell synapses, responding at 9.4% and 2.6%.
Every lab finds alpha'/beta' cells' spike threshold lowest: 5.5 mV below alpha/beta's in Inada et al. 2017 (ex vivo;
gamma 2.5 mV above alpha/beta), about 13 mV below in Groschner et al. 2018 (in vivo) and Chen et al. 2026 (ex vivo;
gamma 11 mV above) (research_notes/Rung 9 learning data/kc_classes_and_apl.md). odor_probe8.py tried both on
odor_probe7.py's antennal lobe, where 7-20% of Kenyon cells responded: Inada's offsets moved the classes partway,
Groschner/Chen's brought gamma to about flies' 2% but sent alpha'/beta' to 59-80%.
Model: odor_probe30.py's brain (odor_probe31.build on its seeds; brain_cache.py keeps it) with the Kenyon cell-to-MBON11
synapses at odor_probe31.py's middle charge (q = 0.030 pC per synapse). Conditions, as odor_probe8.py sets them, each
Kenyon cell type's distance below threshold at rest set (two rounds, spontaneous receptor firing on) from one set of
offsets with the population's mean kept at Turner's 21.5 mV, unclassified "KC" cells at 21.5:
  equal          every class at 21.5 mV (odor_probe30.py's, measured again on this probe's seeds)
  Inada          alpha'/beta' 5.5 mV nearer threshold than alpha/beta, gamma 2.5 mV farther
  Groschner/Chen alpha'/beta' 13 mV nearer, gamma 11 mV farther
Inada's offsets, the one lab's measurement of all three classes in one preparation, are the ones to adopt if the
classes move toward flies'; Groschner/Chen's bound the range. Measured as odor_probe30.py measures (odor_probe24's
odor measures), and for each odor MBON11's Kenyon cell input per cell as odor_probe31.py measures it (its Kenyon cells'
spikes above rest x their synapses onto it x q, mean of the two MBON11s) against Hige et al. 2015's about 250-265 pC,
with MBON11's evoked spikes in the same runs. Seeds 280000 + 1000 x condition (+ odor_probe24's offsets for the odor
measures; + 900 + round for the Kenyon cells' rest; + 200 + odor for MBON11's input).

    python experiments/odor_probe33.py         (writes experiments/odor_probe33.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe31 as p31
import odor_probe7 as p7
import odor_probe8 as p8

OUT = Path(__file__).with_suffix(".json")
SEED = 280000
CHARGE_PC = 0.030
CONDITIONS = {"equal": {}, "Inada": p8.OFFSETS["Inada"], "Groschner/Chen": p8.OFFSETS["Groschner/Chen"]}


def set_rest(o: p7.Olfaction, rec: p10.Receptors, gaps: dict, seed: int) -> dict:
    """odor_probe8.set_rest with the receptor neurons firing spontaneously (odor_probe10.resting)."""
    b, kc, types = o.brain, o.m["kc"], o.types
    threshold = b.params[b.cls[np.flatnonzero(kc)[0]]]["threshold"]
    bias = o.own_bias()
    for r in range(2):
        u = p10.resting(o, rec, seed + r, sample=True)["u"]
        for t, gap in gaps.items():
            mask = types == t
            bias[mask] += (threshold - gap) - u[mask].mean()
        b.set_bias(bias)
    rest = p10.resting(o, rec, seed + 2, sample=True)
    by_class = {name: np.char.startswith(types, prefix) & kc for name, prefix in p7.CLASSES.items()}
    out = {"gap_mv": {t: round(float(threshold - rest["u"][types == t].mean()), 2) for t in gaps},
           "rest_hz_by_class": {name: round(float(rest["hz"][mask].mean()), 4) for name, mask in by_class.items()}}
    print("Kenyon cells' distance below threshold:", json.dumps(out), flush=True)
    return out


def mbon11_input(o: p7.Olfaction, rec: p10.Receptors, base: int, mb: np.ndarray, syn: np.ndarray) -> dict:
    """Per odor (Hige et al.'s window, 0-1.4 s): MBON11's evoked spikes and its Kenyon cell input per cell, pC."""
    runner = p10.make_runner(rec)
    out = {}
    for k, odor in enumerate(p7.ODORS):
        h = runner(o, odor, base + 200 + k, 1.0, 0.4)
        evoked = h["window"] - 1.4 * h["rest"]
        extra = np.maximum(evoked.mean(0), 0.0)                                  # each neuron's spikes above rest
        out[odor] = {"MBON11": round(float(evoked[:, mb].mean()), 1),
                     "kc_input_pc_per_cell": round(float((extra[:, None] * syn).sum(0).mean() * CHARGE_PC), 1)}
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    mb = np.flatnonzero(types == "MBON11")
    gain = p31.mbon_gain(o, rec, mb)
    w_syn = p31.GAIN_HZ_PER_PA * CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mb))
    w = b.weights.copy()
    w[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w, None
    syn = np.zeros((b.n, len(mb)))                                               # synapses onto each MBON11
    np.add.at(syn, (pre[onto], np.searchsorted(mb, b.idx[onto])), b._counts[onto])
    out = {"question": __doc__, "flies": {**p7.FLIES, "kc_share_by_class": {"alpha/beta": "3-8%", "alpha'/beta'": "9-14%",
                                                                            "gamma": "about 2%"},
                                          "mbon11_input_pc_per_cell": "about 250-265"},
           "mbon11_gain": gain, "weight_per_synapse_mv": round(w_syn, 4), "conditions": {}}
    bias0 = o.own_bias()
    for c, (name, offsets) in enumerate(CONDITIONS.items()):
        base = SEED + 1000 * c
        b.set_bias(bias0)
        gaps = p8.class_gaps(o, offsets)
        entry = {"gaps_mv": {t: round(g, 2) for t, g in gaps.items()}, "kc_rest": set_rest(o, rec, gaps, base + 900)}
        entry.update(p24.odor_measures(o, rec, base, gloms, pn_of))
        entry["mbon11_input"] = mbon11_input(o, rec, base, mb, syn)
        out["conditions"][name] = entry
        pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"mean_jaccard": entry["mean_jaccard"], "oct_mch": pair, "rest": entry["rest"],
                                "mbon11_input": entry["mbon11_input"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b.set_bias(bias0)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
