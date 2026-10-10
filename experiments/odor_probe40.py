"""Exploratory, not pre-registered: with the antennal lobe rebuilt around local neurons that answer odors as flies' do,
do the projection neurons open strongly and then accommodate, and do the Kenyon cells respond as flies' do?

odor_probe39.py: one scale on every synapse onto the antennal lobe's LNs brings the GABAergic LNs' onset to flies'
(Nagel et al. 2015, Fig. 5b: 22, 13, 8 and 6 spikes/s per cell over 0-50, 50-100, 100-200 and 200-500 ms, from a
baseline of about 4) at 0.25 of the synapses' strength, the best of the scales swept; with the LNs resting at flies'
4 spikes/s instead of the 4.65 the sweep's rest correction left them at, the response's growth with the scale puts the
best scale at about 0.17. That sweep kept the presynaptic inhibition as built, fitted around LNs whose onset was three
times flies', so its projection neurons only showed the direction.
Model: odor_probe36.py's (odor_probe30.py's antennal lobe, Inada et al.'s Kenyon cell classes, MBON11 keeping its
synaptic current, its Kenyon cell synapses at 0.030 pC each), rebuilt exactly as odor_probe30.py builds it but with every
synapse onto every antennal lobe LN multiplied by s as soon as the antennal lobe's synapses are set (after
odor_probe21.build), and the GABAergic LN types' resting target at flies' 4 spikes/s (rung 4's default 2 for the other
LNs), so that the resting calibration, the PN polish and the presynaptic inhibition's fit to Olsen & Wilson 2008's EPSCs
are all made around those LNs. s = 0.25 and 0.17. Each built model is cached (brain_cache.py, odor_probe40_s0.25 and
odor_probe40_s0.17).
Measured for each: the GABAergic LNs' resting rate and their rate in 50 ms bins over the odor's first 0.55 s, with the
root mean square log ratio to Nagel et al.'s bins, as odor_probe39.py measures (4 seeds of 8 flies); then everything
odor_probe36.py measures (PN, LN and receptor time courses, the transform, the odor measures, MBON11's input and spikes,
the responding Kenyon cells' spikes). Seeds 240000 for the builds (odor_probe30.py's); 380000 + 1000 x condition for the
measures (odor_probe36.py's offsets; + 300 + 10 x odor + seed for the LN rates, + 990 for the LNs' rest).

    python experiments/odor_probe40.py         (writes experiments/odor_probe40.json)
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
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe31 as p31
import odor_probe36 as p36
import odor_probe39 as p39
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 380000
SCALES = (0.25, 0.17)
GABA_LN_REST_HZ = 4.0                              # flies' baseline (Nagel et al. 2015, Fig. 5b)


def ln_mask(types: np.ndarray) -> np.ndarray:
    return np.array([bool(p14.LN.match(t)) for t in types])


def builder(scale: float):
    """A no-argument build for brain_cache: odor_probe31.build with every synapse onto an antennal lobe LN times scale
    straight after odor_probe21.build, and the GABAergic LNs' resting target at GABA_LN_REST_HZ."""
    def build() -> tuple:
        plain = p21.build

        def scaled(o):
            out = plain(o)
            b = o.brain
            onto = ln_mask(o.types)[b.idx]
            w = b.weights.copy()
            w[onto] *= scale
            b.weights, b._external_matrix = w, None
            gaba = p21.masks(o)["inhibitors"]
            o.s.target = o.s.target.copy()
            o.s.target[gaba] = GABA_LN_REST_HZ
            out["ln_inputs"] = {"scale": scale, "edges": int(onto.sum()), "gaba_ln_rest_target_hz": GABA_LN_REST_HZ,
                                "gaba_lns": int(len(gaba))}
            return out
        p21.build = scaled
        try:
            return p31.build()
        finally:
            p21.build = plain
    return build


def prepare() -> None:
    p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
    p21.masks = p29.pn_only_masks


def ln_measure(o, rec, base: int) -> dict:
    """odor_probe39.py's measure on the model as built."""
    types, m = o.types, o.m
    ln = ln_mask(types)
    inhibitors = p21.masks(o)["inhibitors"]
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    oct_pns = np.concatenate([pn_of[g] for g, v in odors.glomeruli("3-octanol").items() if v > 0.2 and g in pn_of])
    hz = p10.resting(o, rec, base + 990)["hz"]
    bins10 = [(round(0.05 * k, 2), round(0.05 * (k + 1), 2)) for k in range(11)]
    out = {"rest_hz_gaba_lns": round(float(hz[inhibitors].mean()), 2),
           "rest_hz_other_lns": round(float(hz[np.setdiff1d(np.flatnonzero(ln), inhibitors)].mean()), 2),
           "rest_hz_upns": round(float(hz[m["upn"]].mean()), 2), "odors": {}}
    for j, odor in enumerate(p39.ODORS):
        runs = [p39.course(o, rec, odor, base + 300 + 10 * j + k, inhibitors, oct_pns) for k in range(p39.SEEDS)]
        lnr, pnr = np.mean([r[0] for r in runs], 0), np.mean([r[1] for r in runs], 0)
        out["odors"][odor] = {"ln_hz_50ms": [round(x, 1) for x in p39.binned(lnr, bins10)],
                              "ln_hz_nagel_bins": [round(x, 2) for x in p39.binned(lnr, p39.MODEL_BINS)]}
        if odor == "3-octanol":
            out["odors"][odor]["oct_pn_hz_50ms"] = [round(x, 1) for x in p39.binned(pnr, bins10)]
    model = np.array(out["odors"]["2-heptanone"]["ln_hz_nagel_bins"])
    out["rms_log_error"] = round(float(np.sqrt(np.mean(np.log(np.maximum(model, 0.1) / np.array(p39.NAGEL)) ** 2))), 3)
    return out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": {"nagel_2015_hz": p39.NAGEL, "bins_s": ((0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.5)),
                                          "baseline_hz": GABA_LN_REST_HZ, "pn_at_500ms_of_peak": 0.48,
                                          "kc_spikes_per_response_alpha_beta": "2.2 +- 1.2",
                                          "mbon11_spikes": {"3-octanol": 118, "4-methylcyclohexanol": 110}},
           "model_bins_s": p39.MODEL_BINS, "conditions": {}}
    for c, s in enumerate(SCALES):
        o, rec, built = brain_cache.load(f"odor_probe40_s{s:g}", builder(s), prepare)
        base = SEED + 1000 * c
        entry = {"scale": s, "build": {x: built[x] for x in ("build", "presynaptic") if x in built},
                 "ln_response": ln_measure(o, rec, base)}
        lr = entry["ln_response"]
        print(f"s {s} LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
              json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]),
              flush=True)
        out["conditions"][f"{s:g}"] = entry
        OUT.write_text(json.dumps(out, indent=1))
        entry.update(p36.measure(o, rec, built, base))
        OUT.write_text(json.dumps(out, indent=1))
        print(f"s {s} done ({time.perf_counter() - t0:.0f} s)", flush=True)
        del o, rec
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
