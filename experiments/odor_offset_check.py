"""Exploratory check, not pre-registered: does the built antennal lobe's presynaptic inhibition act at rest?

odor_probe27.py made the presynaptic inhibition act only on the GABAergic LNs' summed rate above their resting rate (the
trace's offset), because flies have little tonic presynaptic inhibition, and odor_probe28.py's alpha-shaped traces keep
that offset. The build (odor_probe31.build, odor_probe30.py's sequence) measures that rate when it fits the inhibition,
after the first resting polish and the PN polish, and then polishes the rest again. In odor_probe36.py's odor runs on
odor_probe30.py's model the inhibitors' summed resting rate was 282 spikes/s, against an offset of 48.6 (odor_probe40.py
at s = 0.17: about 385 against 266), which would leave the receptor-to-PN synapses at about 0.6 (0.5) of their
calibrated strength at rest; the slow GABA-B trace (1 s) also starts each run at the offset and climbs through it.
Model: odor_probe30.py's (brain_cache.py's copy), and odor_probe40.py's at s = 0.17 (its cache).
Measured for each: over 1 s of rest after 4 s to settle (2 seeds of 8 flies), the inhibitors' summed rate, the acting
traces' means (GABA-A's and GABA-B's second stages) and the inhibited synapses' mean strength, 1 / (1 + sum k max(A -
offset, 0)), at the end of each 10 ms piece, with the offset as built; then the same with the offset (and the traces'
start) raised to the GABA-A trace's resting mean, k unchanged; and with each offset, 3-octanol's PN course
(odor_probe30.course) and the transform (odor_probe24.transform) on the same seeds. Seeds 400000 + 1000 x model (+ seed
for the rest, + 700 for the course).

Ran: yes, in both models, and raising the offset alone undoes little of it. In odor_probe30.py's model the inhibitors
rest at 200 spikes/s summed (the GABA-A trace at 203, the GABA-B trace at 233) against an offset of 48.6, so the
receptor-to-PN synapses rest at 0.67 of their strength, and the PNs at 2.0 spikes/s. With the offset at 203 the PNs rest
at 3.1 spikes/s, which drives the inhibitors to 310, and the synapses rest at 0.73. 3-octanol's PNs then fire 74
spikes/s at 50-100 ms instead of 68 and peak at 115 instead of 105, and accommodate no more (0.97 of the peak at 0.5 s,
0.95 before). The transform barely moves (Rmax 194-344 and sigma 27-38, against 189-339 and 30-37). In odor_probe40.py's
model at s = 0.17 the inhibitors rest at 361 against 266 and the synapses at 0.54, the PNs at 1.1 spikes/s; with the
offset at 361 the PNs rest at 4.65 spikes/s, the inhibitors at 401 and the synapses at 0.71. Its 3-octanol PNs fire 85 at
50-100 ms instead of 73 and peak at 113 instead of 94 (0.94 of the peak at 0.5 s, 0.90 before). Its transform's sigma
falls to 27-34 (37-48 before) as weak input works better (5 spikes/s of receptor input: 19-41 spikes/s in the PNs,
against 4-20), its Rmax unchanged (187-346). The build sets the offset before its second polishes raise the LNs to their
targets, so the offset has to come after them; odor_probe42.py builds that way. Also, in the window where every run
measures rest and starts its odor (1-2 s after the reset), the inhibitors fire about a quarter above their steady rate
(odor_probe30.py's model: 252 spikes/s summed, against 200 after 4 s) and the PNs at half theirs (1.0 against 2.0): the
runs start in a transient, which the build's polish, measured in the same window, calibrates.

    python experiments/odor_offset_check.py      (writes experiments/odor_offset_check.json)
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
import odor_probe28 as p28
import odor_probe30 as p30
import odor_probe40 as p40
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 400000
SETTLE_S, REST_S, SEEDS = 4.0, 1.0, 2


def resting(o, rec, seed: int, inhibitors: np.ndarray, k: np.ndarray, offset: float) -> dict:
    b = o.brain
    plan = rec.plan(None, 0.0, 0.0)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    for _ in range(int(round(SETTLE_S / p10.PIECE))):
        b.advance(piece, drive=rec.at(plan, -1.0))
    counts, traces, gains = 0, [], []
    for _ in range(int(round(REST_S / p10.PIECE))):
        counts = counts + b.advance(piece, drive=rec.at(plan, -1.0))
        a = np.asarray(b.presynaptic_state, np.float64)
        traces.append(a.mean(0))
        gains.append(float((1.0 / (1.0 + (np.maximum(a - offset, 0.0) * k).sum(1))).mean()))
    hz = counts.mean(0) / REST_S
    return {"inhibitors_summed_hz": float(hz[inhibitors].sum()), "traces": np.mean(traces, 0), "gain": float(np.mean(gains)),
            "upn_hz": float(hz[o.m["upn"]].mean())}


def rest_summary(o, rec, base: int, inhibitors, k, offset) -> dict:
    rows = [resting(o, rec, base + s, inhibitors, k, offset) for s in range(SEEDS)]
    t = np.mean([r["traces"] for r in rows], 0)
    return {"offset_hz": round(offset, 1), "inhibitors_summed_hz": round(float(np.mean([r["inhibitors_summed_hz"] for r in rows])), 1),
            "gaba_a_trace_hz": round(float(t[1]), 1), "gaba_b_trace_hz": round(float(t[3]), 1),
            "synapse_strength_at_rest": round(float(np.mean([r["gain"] for r in rows])), 3),
            "upn_rest_hz": round(float(np.mean([r["upn_hz"] for r in rows])), 2)}


def measure(o, rec, built: dict, base: int) -> dict:
    b, types, m = o.brain, o.types, o.m
    mk = p21.masks(o)
    inhibitors = mk["inhibitors"]
    pres = built["presynaptic"]
    k, offset = np.asarray(pres["k"], np.float64), float(pres["offset_hz"])
    k_a, k_b = float(k[1]), float(k[3])
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    pns = np.concatenate([pn_of[g] for g in odors.glomeruli("3-octanol") if g in pn_of])
    out = {"k": [round(x, 6) for x in k]}
    raised = None
    for name in ("as built", "offset at rest"):
        if name == "offset at rest":
            raised = out["as built"]["rest"]["gaba_a_trace_hz"]
            p28.apply(o, mk, base_w, base_sw, k_a, k_b, raised)
            offset = raised
        row = {"rest": rest_summary(o, rec, base, inhibitors, k, offset)}
        print(" ", name, "rest", json.dumps(row["rest"]), flush=True)
        c = p30.course(o, rec, "3-octanol", base + 700, pns, inhibitors, k, offset)
        row["course_3_octanol"] = {x: c[x] for x in ("rest_pn_hz", "rest_inhibitors_hz", "pn_hz", "gain")}
        print(" ", name, "3-octanol PNs", json.dumps(c["pn_hz"][:12]), "gain", json.dumps(c["gain"][:6]), flush=True)
        t = p24.transform(o, rec, base)
        row["transform"] = {g: t[g]["fit"] for g in t}
        row["transform_alone"] = {g: {h: v["whole"] for h, v in t[g]["alone"].items()} for g in t}
        out[name] = row
    p28.apply(o, mk, base_w, base_sw, k_a, k_b, float(pres["offset_hz"]))     # leave the model as built
    return out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "settle_s": SETTLE_S, "models": {}}
    loads = {"odor_probe30": lambda: brain_cache.probe30(),
             "odor_probe40_s0.17": lambda: brain_cache.load("odor_probe40_s0.17", p40.builder(0.17), p40.prepare)}
    for i, (name, load) in enumerate(loads.items()):
        o, rec, built = load()
        print(name, flush=True)
        out["models"][name] = measure(o, rec, built, SEED + 1000 * i)
        OUT.write_text(json.dumps(out, indent=1))
        del o, rec
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
