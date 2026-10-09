"""Exploratory, not pre-registered: three checks on odor_probe7.py's current model, each from a measurement. Is its APL
as strong as a fly's, would the Kenyon cell classes' measured thresholds put the right classes first, and how much does
the odor's strength matter?

odor_probe7.py: with the pathway's measured properties, 11-30% of Kenyon cells respond to an odor by Turner et al.
2008's criterion (flies: 6 +- 5%), alpha'/beta' cells least (2-5%) and gamma cells a lot (15-29%), where Turner's
flies show alpha'/beta' most (about 9-14%), alpha/beta 3-8% and gamma about 2%; and MBON11 gains 2-11 spikes where Hige
et al. 2015's flies gained 110-118. The measurements behind these checks are in
research_notes/Rung 9 learning data/kc_classes_and_apl.md:
  APL      blocking APL raises Kenyon cells' odor calcium two- to threefold and lowers their population sparseness from
           0.97 to 0.86-0.89 (Lin et al. 2014), roughly 3% active to 11-14% (derived): about four times as many.
           Here: APL silenced throughout, the current model otherwise. The model's APL hyperpolarizes Kenyon cells by
           about 11 mV at its peak (release about 38 Hz x the summed APL-to-KC weight x 5 ms), near the measured
           saturation of 10-12 mV (Inada et al. 2017), but for about 100 ms, where flies' inhibition lags by
           several hundred ms and lasts about a second.
  classes  every lab finds alpha'/beta' Kenyon cells' spike threshold lowest: 5.5 mV below alpha/beta's in Inada et al.
           2017 (ex vivo; gamma 2.5 mV above alpha/beta), about 13 mV below in Groschner et al. 2018 (in vivo) and Chen
           et al. 2026 (ex vivo; gamma 11 mV above). Here each class's distance below threshold at rest is set from
           one set of offsets, the population's mean kept at Turner's 21.5 mV (his 17 cells' classes are unknown):
             Inada          alpha'/beta' 5.5 mV nearer threshold than alpha/beta, gamma 2.5 mV farther
             Groschner/Chen alpha'/beta' 13 mV nearer, gamma 11 mV farther
           (unclassified "KC" cells at 21.5 mV).
  strength the current model drives each receptor neuron at its DoOR response times 200 Hz. Turner diluted odors
           1:1000; Hige et al. used 2% of saturated vapour, a stronger stimulus, and no study here relates either to
           receptor rates. Here: 100 and 50 Hz at a response of 1.
Odors, flies and measures as odor_probe7.py; seeds 20000 + 100 x condition + odor (Turner's protocol), + 50 + odor
(Hige's), + 90 (Kenyon cells' rest), + 95 (the resting brain).

    python experiments/odor_probe8.py          (writes experiments/odor_probe8.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
OFFSETS = {"Inada": {"alpha'/beta'": -5.5, "gamma": 2.5}, "Groschner/Chen": {"alpha'/beta'": -13.0, "gamma": 11.0}}
CONDITIONS = {"current": {}, "current, APL silenced": {"silence_apl": True},
              "class thresholds, Inada": {"offsets": "Inada"}, "class thresholds, Groschner/Chen": {"offsets": "Groschner/Chen"},
              "current, receptors at 100 Hz": {"max_hz": 100.0}, "current, receptors at 50 Hz": {"max_hz": 50.0}}


def class_gaps(o: p7.Olfaction, offsets: dict) -> dict:
    """Each Kenyon cell type's distance below threshold at rest: alpha/beta at g, the others offset from it, the
    population's mean 21.5 mV."""
    types = o.types[o.m["kc"]]
    cls = {name: np.char.startswith(types, prefix) for name, prefix in p7.CLASSES.items()}
    n = {name: int(mask.sum()) for name, mask in cls.items()}
    typed = sum(n.values())
    shift = sum(n[k] * offsets.get(k, 0.0) for k in n) / typed
    g = p3.KC_GAP_MV - shift
    gaps = {}
    for t in np.unique(types):
        name = next((k for k, prefix in p7.CLASSES.items() if t.startswith(prefix)), None)
        gaps[t] = p3.KC_GAP_MV if name is None else g + offsets.get(name, 0.0)
    return gaps


def set_rest(o: p7.Olfaction, gaps: dict, seed: int) -> list:
    """odor_probe3.set_kc_rest with a distance below threshold per Kenyon cell type."""
    b, kc, types = o.brain, o.m["kc"], o.types
    threshold = b.params[b.cls[np.flatnonzero(kc)[0]]]["threshold"]
    bias = b.bias.copy()
    log = []
    for r in range(3):
        u = p3.rest_state(o.s, seed + r, True)["u"]
        row = {}
        for t, gap in gaps.items():
            mask = types == t
            row[t] = round(float(threshold - u[mask].mean()), 2)
            if r < 2:
                bias[mask] += (threshold - gap) - u[mask].mean()
        log.append(row)
        b.set_bias(bias)
    print("Kenyon cells' distance below threshold:", json.dumps(log[-1]), flush=True)
    return log


def condition(o: p7.Olfaction, name: str, c: int) -> dict:
    spec = CONDITIONS[name]
    base = 20000 + 100 * c
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    if "offsets" in spec:
        gaps = class_gaps(o, OFFSETS[spec["offsets"]])
        out["gaps_mv"] = {t: round(g, 2) for t, g in gaps.items()}
        out["kc_rest_by_class"] = set_rest(o, gaps, base + 80)
    silence = o.brain.cells(["APL"]) if spec.get("silence_apl") else ()
    max_hz = spec.get("max_hz", p3.MAX_HZ)
    out["rest"] = p7.rest_measures(o, base + 95, silence)
    out["odors"], responders = {}, {}
    for k, odor in enumerate(p7.ODORS):
        row, responders[odor] = p7.measure_odor(o, odor, base + k, base + 50 + k, silence, max_hz)
        out["odors"][odor] = row
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "spikes_per_response", "evoked_spikes_0_1.4s")}), flush=True)
    out["overlap_jaccard"] = p7.overlaps(responders)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    out = {"question": __doc__, "flies": p7.FLIES, "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = condition(o, name, c)
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
