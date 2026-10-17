"""Exploratory check, written before it runs, not pre-registered and not a change to the model: does OCG01f's inhibition
keep CvN7's downward response weak in rung 6's brain, and what drives OCG01f?

neck_route_check.py:
- VS gives CvN7 +15.7 mV more drive under downward stripes than upward ones. OCG01f, glutamatergic and so inhibitory in
  the model, takes 12.8 of it back, which leaves CvN7 firing only about 4 Hz more to downward motion. Onto CvN6 OCG01f's
  opposing drive (-16.8 mV) exceeds VS's (+11.7).
- OCG01f is a cell of the ocellar ganglion, which MaleCNS lacks. So in the model it keeps only its brain inputs: 54%
  from OCG01b and 18% from VS (research note §3.4). The note predicted from the wiring that this route would oppose the
  direct one at about 0.4 of its size; in the model it is 0.8 of it onto CvN7.
- CvN7's yaw signal is 0.34 of its vertical one on this seed (0.28 on seed 8800). Gorko et al.'s map, summed linearly,
  predicts 0.12-0.16.
Model and scenes are neck_route_check.py's: the intact brain, seed 7720, 8 flies; grey, the drum each way, stripes down
and up; rates from 0.5 to 2 s; its loop, with each spike weighted by its strength under its neuron's depression. Two
conditions: intact, and every synapse from OCG01f onto CvN4-7 set to zero.
Measured:
- CvN4-7's vertical signals (down - up, both cells) and drum signals by nerve side, and CvN7's yaw-to-vertical ratio,
  in each condition;
- OCG01f's and OCG01b's rates in each scene, by side;
- OCG01f's inputs, as neck_route_check.py computes drives: their vertical drive change (down - up, in mV per OCG01f
  cell), VS's and OCG01b's shares of it, and the 8 input types with the largest change;
- the T4/T5 subtypes' shares of the excitatory input of each VS cell presynaptic to CvN6 or CvN7, from the connectome.
Read:
- If the cut raises CvN7's vertical signal by half or more, OCG01f's inhibition is what keeps it weak.
- CvN7's yaw-to-vertical ratio with the cut, against the map's 0.12-0.16. If it falls there, the map's selectivity
  appears once OCG01f's inhibition is gone. Either way the model's CvN7 tuning then rests on a cell whose ocellar input
  is missing.
- If VS carries most of OCG01f's vertical drive change, OCG01f is feedforward inhibition from VS. If OCG01b does,
  whatever drives OCG01b sets it.

Ran (2026-10-17, 221 s): OCG01f's inhibition is what keeps CvN7's downward response weak, and CvN6's absent. Cutting its
synapses onto CvN4-7 makes CvN7 eight times as downward-selective and blind to yaw: its ratio falls from 0.34 to 0.02,
past the map's 0.12-0.16. VS drives all of OCG01f's vertical response, so in the model it is feedforward inhibition from
VS.
- The cut: 7 connections, -180.7 mV summed.
- Intact, it reproduces neck_route_check.py: CvN7's vertical signal is +3.92 Hz (t 9.2), its yaw signal -1.33 (t -2.8).
- With the cut, vertical signals (down - up) and drum signals by nerve side, intact to cut:
  - CvN7: vertical +3.9 to +31.8 Hz (t 25); yaw -1.33 to +0.58 (t 1.4). Its yaw-to-vertical ratio falls from 0.34 to
    0.018; the yaw signal's standard error alone is 0.013 of the vertical signal.
  - CvN6: vertical -0.9 to +32.1 (t 29); yaw +24.8 to +33.0 (t 39).
  - CvN5: vertical +0.8 to +5.8 (t 11); yaw +5.0 to +7.4 (t 11).
  - CvN4 is unchanged (vertical +1.1 to +1.25).
- OCG01f's rates, left and right:
  - grey 2.4 and 2.0 Hz;
  - downward stripes 37.4 and 45.9, upward 1.4 and 7.0;
  - drum 12.4 (left) under clockwise and 16.6 (right) under counterclockwise, which is back-to-front across each cell's
    own eye; 3.2 and 5.1 under the other.
  - OCG01b stays at 0-4.2 Hz in every scene.
- OCG01f's vertical drive change is +12.2 mV per cell (t 133). VS's five cells onto it give 109% of that (63.7 mV of
  weight), and OCG01b gives -9%.
- The VS cells onto CvN6 and CvN7, by their T4/T5 inputs:
  - cells 4 (left) and 8 (right), the two that answer the drum, take 53% and 60% of their excitatory input from T4b/T5b
    (back-to-front) and nearly all the rest from T4d/T5d (downward);
  - the other four take 83-96% from T4d/T5d.
So:
- By the readings:
  - the cut raises CvN7's vertical signal eightfold, so OCG01f's inhibition is what keeps it weak;
  - CvN7's ratio with the cut, 0.018, falls below the map's 0.12-0.16 rather than into it. The map sits between the
    intact model (0.34) and the cut (0.02);
  - VS carries all of OCG01f's vertical drive, so in the model OCG01f is feedforward inhibition from VS. Its yaw
    responses follow the frontal VS cells' back-to-front input, which is why cutting it also raises CvN6's drum signal.
- How this sits against flies:
  - Flies' CvN7 at rest answers wide-field rotation with graded, on average subthreshold, potentials: about 3.2 mV peak
    to peak (Gorko et al. 2024; note §1.3). The intact model's few extra spikes are closer to that than the cut's
    +31.8 Hz.
  - Blowfly CNMN6/7, the counterparts of CvN6/7, are tuned to downward pitch (Wertz, Haag & Borst 2012; note §6). The
    intact model's CvN6 doesn't answer vertical motion at all (-0.9 Hz) and does once OCG01f's synapses are cut.
  - In blowflies VS reaches CNMN6/7 through dye-coupled, electrical, synapses, which the connectome can't show and the
    model doesn't have. That would strengthen the direct route against OCG01f's chemical one.
  - Glutamate is taken as inhibitory, and in flies OCG01f also takes ocellar input that MaleCNS lacks.
- So the pitch MNs' tuning in rung 6's brain hangs on one unconstrained relay: VS's direct excitation against
  VS-to-OCG01f-to-MN inhibition. As the model stands it leaves CvN6 without the downward tuning its blowfly counterpart
  has. Fixing that needs a model choice (electrical VS-to-CvN6/7 coupling, or OCG01f's sign or drive), and nothing in
  the notes measures either in Drosophila. These are exploratory checks, not a change to the model.

    python experiments/neck_ocg_check.py      (writes experiments/neck_ocg_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import neck_route_check as nr
import rung6_relay as r6
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
PITCH = ["CvN4", "CvN5", "CvN6", "CvN7"]
T45 = ["T4a", "T4b", "T4c", "T4d", "T5a", "T5b", "T5c", "T5d"]
TOP = 8


def tstat(x: np.ndarray) -> float:
    sd = float(x.std(ddof=1))
    return round(float(x.mean() / (sd / np.sqrt(len(x)))), 2) if sd > 0 else 0.0


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    ct = np.asarray(b.cell_type).astype(str)
    types = np.where(ct != "", ct, np.asarray(b.mcns_type).astype(str))
    pitch = {t: {x: b.cells([t], x) for x in "LR"} for t in PITCH}
    ocg_f, ocg_b, vs = b.cells(["OCG01f"]), b.cells(["OCG01b"]), b.cells(["VS"])
    into_f = np.flatnonzero(np.isin(b.idx, ocg_f))                     # edges onto OCG01f
    sources = np.unique(pre[into_f])
    col = np.searchsorted(sources, pre[into_f])
    saved = b.weights.copy()
    cut = np.isin(pre, ocg_f) & np.isin(b.idx, np.concatenate([v for d in pitch.values() for v in d.values()]))
    out = {"question": __doc__, "cut": {"edges": int(cut.sum()), "summed_weight_mv": round(float(saved[cut].sum()), 1)},
           "conditions": {}}
    print("cut", json.dumps(out["cut"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    for name, mask in (("intact", np.zeros(len(saved), bool)), ("OCG01f cut", cut)):
        b.weights = np.where(mask, np.float32(0), saved).astype(np.float32)
        rates, eff = {}, {}
        for sc, scene in nr.SCENES.items():
            rates[sc], eff[sc] = nr.run(s, scene, sources)
        c = {"pitch": {}, "rates_hz": {}}
        for t in PITCH:
            L, R = pitch[t]["L"], pitch[t]["R"]
            m = lambda sc, v: rates[sc][:, v].mean(1)
            d = (m("ccw", L) - m("ccw", R)) - (m("cw", L) - m("cw", R))
            if t in nr.CROSSED:
                d = -d                                                  # by nerve side
            v = (m("down", L) - m("up", L)) + (m("down", R) - m("up", R))
            c["pitch"][t] = {"yaw_hz": round(float(d.mean()), 3), "yaw_t": tstat(d), "vertical_hz": round(float(v.mean()), 3),
                             "vertical_t": tstat(v)}
        y, v = c["pitch"]["CvN7"]["yaw_hz"], c["pitch"]["CvN7"]["vertical_hz"]
        c["cvn7_yaw_over_vertical"] = round(abs(y) / v, 3) if v > 0 else None
        for g, cells in (("OCG01f", ocg_f), ("OCG01b", ocg_b)):
            c["rates_hz"][g] = {sc: {x: round(float(rates[sc][:, cells[b.side[cells] == x]].mean()), 2) for x in "LR"
                                     if (b.side[cells] == x).any()} for sc in nr.SCENES}
        if name == "intact":
            w = np.asarray(saved[into_f], np.float64)
            per_cell = len(ocg_f)
            drive = {sc: (w[None, :] * eff[sc][:, col] * TAU) for sc in nr.SCENES}     # (flies, edges), mV
            change = (drive["down"] - drive["up"]).sum(1) / per_cell                   # per OCG01f cell
            src_t = types[pre[into_f]]
            rows = []
            for ty in np.unique(src_t):
                k = src_t == ty
                ch = (drive["down"][:, k] - drive["up"][:, k]).sum(1) / per_cell
                rows.append({"type": str(ty), "cells": int(len(np.unique(pre[into_f][k]))), "weight_mv": round(float(w[k].sum()), 2),
                             "vertical_change_mv": round(float(ch.mean()), 3)})
            total = float(change.mean())
            share = lambda ty: round(sum(r["vertical_change_mv"] for r in rows if r["type"] == ty) / total, 3) if abs(total) > 1e-9 else None
            vs_type = str(types[vs[0]])
            c["ocg01f_inputs"] = {"vertical_change_mv": {"mv": round(total, 3), "t": tstat(change)},
                                  "vs_share": share(vs_type), "ocg01b_share": share("OCG01b"),
                                  "top": sorted(rows, key=lambda r: -abs(r["vertical_change_mv"]))[:TOP]}
        out["conditions"][name] = c
        print(name, json.dumps(c["pitch"]), "ratio", c["cvn7_yaw_over_vertical"], json.dumps(c["rates_hz"]),
              f"({time.perf_counter() - t0:.0f} s)", flush=True)
        if "ocg01f_inputs" in c:
            print("OCG01f inputs", json.dumps(c["ocg01f_inputs"]), flush=True)
    b.weights = saved
    onto = np.concatenate([pitch[t][x] for t in ("CvN6", "CvN7") for x in "LR"])
    out["vs_cells"] = []
    for cell in vs:
        if not (np.isin(b.idx, onto) & (pre == cell)).any():
            continue
        e = np.flatnonzero(b.idx == cell)
        w = np.asarray(saved[e], np.float64)
        exc = w[w > 0].sum()
        out["vs_cells"].append({"cell": int(cell), "side": str(b.side[cell]),
                                "t4t5_share": {t: round(float(w[(types[pre[e]] == t) & (w > 0)].sum() / exc), 3) for t in T45}})
    it, cu = out["conditions"]["intact"]["pitch"], out["conditions"]["OCG01f cut"]["pitch"]
    out["vertical_gain_with_cut"] = {t: round(cu[t]["vertical_hz"] / it[t]["vertical_hz"], 3) if it[t]["vertical_hz"] else None for t in PITCH}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("vs cells", json.dumps(out["vs_cells"]), flush=True)
    print("vertical with cut / intact", json.dumps(out["vertical_gain_with_cut"]), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
