"""Exploratory check, written before it runs, not pre-registered and not a change to the model: which inputs carry the
drum's direction signal and the stripes' vertical signal to the neck motor neurons in rung 6's brain, and how much of
neck_lesion_check.py's losses is lost signal rather than lost gain?

neck_lesion_check.py:
- Cutting only HS's and H2's synapses onto the yaw neck MNs removes 82-88% of GNG283's and GNG276's drum signal, about
  70% of VCvN1-3's and 39% of CvN1/2's (GNG653).
- Cutting only VS's synapses onto CvN4-7 turns CvN7's downward preference upward, and it removes 77% of CvN6's drum
  signal. neck_drive_probe.py had read CvN6's drum response, from the sides alone, as coming through its HSS input.
- But a cut removes a synapse's tonic drive along with its direction signal, and a neuron's rate isn't linear in its
  drive. Under either drum direction H2 fires at 68-150 Hz and VS at 12-19 Hz.
In rung 6's brain HS, H2 and VS don't depress. 519 of the neck MNs' 2,076 presynaptic cells do (each spike leaves 0.9 of
their strength). None is external or graded, and the brain has no slow synapses.
Model and scenes are neck_lesion_check.py's: the intact brain, seed 7720, 8 flies; grey, the drum each way, stripes
down and up; rates from 0.5 to 2 s. They run through eyes_at_rest.Setup.run's loop, which here also sums each spike's
strength under its neuron's depression.
Computed for each of GNG283, GNG276, GNG647, GNG653, GNG314 and CvN4-7, and for each presynaptic cell: its drive onto the
target, in mV per target cell, per fly. That is weight x strength-weighted spikes per s x 5 ms (the synaptic time
constant), as dna02_drum_check.py and neck_upward_check.py computed it without depression. Then, by presynaptic type
and summed over all inputs:
- the yaw change: the drive under the drum that excites the HS cells on the target's nerve side, minus the drive under
  the other drum, summed over the left- and right-soma cells as the direction signal sums them;
- the vertical change: down minus up, summed over both sides;
- the mean drum drive: the mean of the two drums' drives, averaged over both sides, and its rise from grey (the tonic
  part).
Reported per target type:
- these for all inputs together;
- the same for HS, HSS on its own, H2 and VS;
- the cut group's share of the summed yaw change and of the vertical change (HS and H2 for the yaw types, VS for
  CvN4-7), next to neck_lesion_check.py's loss;
- the 8 input types with the largest yaw change and the 8 with the largest vertical change;
- each VS cell presynaptic to CvN6 or CvN7, with its weights onto them and its rates.
Read:
- For each type, the cut group's linear share of the yaw (or vertical) change against the lesion's loss. If the two
  are within about 15 points, the lesion's loss is the group's signal. If the loss is much larger, the rest is lost
  gain: the group's mean drum drive is the depolarization the cut took away.
- For CvN6: if VS's yaw change outweighs HSS's, VS carries the drum's signal to CvN6. If HSS's outweighs VS's while VS
  gives tonic drive, the VS cut's loss is mainly gain, and neck_drive_probe.py's HSS reading stands.

    python experiments/neck_route_check.py      (writes experiments/neck_route_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rung6_relay as r6
from brainfly.eye2d import ElevationGrating, Grating
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
LESION = Path(__file__).with_name("neck_lesion_check.json")
SEED, GAIN = 7720, 1.0
WINDOW = (0.5, 2.0)
SCENES = {"grey": lambda t: [], "ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)],
          "down": lambda t: [ElevationGrating(30.0, -40.0 * t)], "up": lambda t: [ElevationGrating(30.0, 40.0 * t)]}
YAW = ["GNG283", "GNG276", "GNG647", "GNG653", "GNG314"]
PITCH = ["CvN4", "CvN5", "CvN6", "CvN7"]
CROSSED = {"CvN6", "CvN7"}                       # axons cross: the nerve is on the other side from the soma
NAMED = {"HS": ["HSN", "HSE", "HSS"], "HSS": ["HSS"], "H2": ["H2"], "VS": ["VS"]}
CUT = {**{t: ["HS", "H2"] for t in YAW}, **{t: ["VS"] for t in PITCH}}
TOP = 8


def run(s, scene, sources: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """eyes_at_rest.Setup.run's loop for one scene. Per fly: every neuron's rate in the window, and each source's spikes
    per s there, each weighted by its strength under its neuron's depression."""
    b, ol = s.brain, s.ol
    b.reset(SEED)
    ol.reset()
    ol.gain = GAIN
    per = int(round(eyes.OPTIC_DT / b.dt))
    for _ in range(int(round(eyes.SETTLE / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(None))
        b.advance(per)
    a, z = (int(round(w / eyes.OPTIC_DT)) for w in WINDOW)
    dep = np.array([p["depression"] for p in b.params])[b.cls][sources]
    rec = (np.array([p["recovery"] for p in b.params])[b.cls] / b.dt)[sources]
    d = dep < 1
    counts, eff = np.zeros((b.trials, b.n)), np.zeros((b.trials, len(sources)))
    for k in range(int(round(eyes.SCENE / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(scene(k * eyes.OPTIC_DT))))
        inside = a <= k < z
        if inside:
            avail = np.ones((b.trials, len(sources)))
            avail[:, d] = 1 - (1 - b.left[:, sources[d]]) * np.exp(-(b.t - b.last[:, sources[d]]) / rec[d])
        c = b.advance(per)
        if inside:
            counts += c
            n = c[:, sources]
            # several spikes in one 2 ms step: the first at the strength available, each later one at depression x the last
            eff += avail * np.where(d, (1 - dep ** n) / np.where(d, 1 - dep, 1.0), n)
    span = WINDOW[1] - WINDOW[0]
    return counts / span, eff / span


def tstat(x: np.ndarray) -> float:
    sd = float(x.std(ddof=1))
    return round(float(x.mean() / (sd / np.sqrt(len(x)))), 2) if sd > 0 else 0.0


def summary(x: np.ndarray) -> dict:
    return {"mv": round(float(x.mean()), 3), "t": tstat(x)}


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    ct = np.asarray(b.cell_type).astype(str)
    types = np.where(ct != "", ct, np.asarray(b.mcns_type).astype(str))
    cells = {t: {x: b.cells([t], x) for x in "LR"} for t in YAW + PITCH}
    every = np.concatenate([v for d in cells.values() for v in d.values()])
    edges = np.flatnonzero(np.isin(b.idx, every))
    sources = np.unique(pre[edges])
    col = np.searchsorted(sources, pre[edges])
    w = np.asarray(b.weights[edges], np.float64)
    named = {g: np.isin(pre[edges], b.cells(tt)) for g, tt in NAMED.items()}
    rates, eff = {}, {}
    for name, scene in SCENES.items():
        rates[name], eff[name] = run(s, scene, sources)
        print(name, f"({time.perf_counter() - t0:.0f} s)", flush=True)
    contrib = {sc: w[None, :] * eff[sc][:, col] * TAU for sc in SCENES}          # (flies, edges), mV
    out = {"question": __doc__, "targets": {}, "vs_cells": []}
    lesion = json.loads(LESION.read_text())["conditions"] if LESION.exists() else None
    for t in YAW + PITCH:
        per_side = {}
        for x in "LR":
            mask = np.isin(b.idx[edges], cells[t][x])
            ncell = len(cells[t][x])
            nerve = x if t not in CROSSED else {"L": "R", "R": "L"}[x]
            pref, null = ("ccw", "cw") if nerve == "L" else ("cw", "ccw")
            per_side[x] = {"mask": mask, "ncell": ncell, "pref": pref, "null": null}
        def metrics(sel: np.ndarray) -> dict:
            """sel: a boolean over the edges. Per fly: yaw and vertical changes (summed over sides), mean drum drive and
            its rise from grey (averaged over sides), in mV per target cell."""
            yaw = vert = drum = tonic = 0.0
            for x, p in per_side.items():
                m = p["mask"] & sel
                dr = {sc: contrib[sc][:, m].sum(1) / p["ncell"] for sc in SCENES}
                yaw = yaw + dr[p["pref"]] - dr[p["null"]]
                vert = vert + dr["down"] - dr["up"]
                drum = drum + (dr["ccw"] + dr["cw"]) / 4
                tonic = tonic + ((dr["ccw"] + dr["cw"]) / 2 - dr["grey"]) / 2
            return {"yaw_change": summary(yaw), "vertical_change": summary(vert), "mean_drum_drive": summary(drum),
                    "tonic": summary(tonic)}
        allin = metrics(np.ones(len(edges), bool))
        groups = {g: metrics(m) for g, m in named.items()}
        cut = np.zeros(len(edges), bool)
        for g in CUT[t]:
            cut |= named[g]
        cutm = metrics(cut)
        share = lambda k: round(cutm[k]["mv"] / allin[k]["mv"], 3) if abs(allin[k]["mv"]) > 1e-9 else None
        rows = []
        onto = per_side["L"]["mask"] | per_side["R"]["mask"]
        for ty in np.unique(types[pre[edges[onto]]]):
            m = (types[pre[edges]] == ty) & onto
            r = metrics(m)
            rows.append({"type": str(ty), "cells": int(len(np.unique(pre[edges][m]))), "weight_mv": round(float(w[m].sum()), 2),
                         **{k: r[k]["mv"] for k in r}})
        side_rates = {sc: {x: round(float(rates[sc][:, cells[t][x]].mean()), 2) for x in "LR"} for sc in SCENES}
        d = sum((rates[per_side[x]["pref"]][:, cells[t][x]].mean(1) - rates[per_side[x]["null"]][:, cells[t][x]].mean(1)) for x in "LR")
        v = sum((rates["down"][:, cells[t][x]].mean(1) - rates["up"][:, cells[t][x]].mean(1)) for x in "LR")
        entry = {"rate_hz": side_rates, "yaw_signal_hz": {"hz": round(float(d.mean()), 3), "t": tstat(d)},
                 "vertical_signal_hz": {"hz": round(float(v.mean()), 3), "t": tstat(v)},
                 "all_inputs": allin, "named": groups, "cut_group": CUT[t], "cut": cutm,
                 "cut_share_of_yaw_change": share("yaw_change"), "cut_share_of_vertical_change": share("vertical_change"),
                 "top_yaw": sorted(rows, key=lambda r: -abs(r["yaw_change"]))[:TOP],
                 "top_vertical": sorted(rows, key=lambda r: -abs(r["vertical_change"]))[:TOP]}
        if lesion is not None:
            it, after = lesion["intact"], lesion["HS/H2 cut" if t in YAW else "VS cut"]
            loss = lambda k: round(1 - after[k][t]["signal_hz"] / it[k][t]["signal_hz"], 3) if it[k][t]["signal_hz"] else None
            entry["lesion_loss"] = {"yaw": loss("yaw"), "vertical": loss("vertical") if t in PITCH else None,
                                    "intact_yaw_hz_in_lesion_run": it["yaw"][t]["signal_hz"]}
        out["targets"][t] = entry
        print(t, json.dumps({k: entry[k] for k in ("yaw_signal_hz", "vertical_signal_hz", "cut_share_of_yaw_change",
                                                    "cut_share_of_vertical_change")}),
              json.dumps(entry.get("lesion_loss")), "| all", json.dumps({k: allin[k]["mv"] for k in allin}),
              "| cut", json.dumps({k: cutm[k]["mv"] for k in cutm}), flush=True)
    vs = b.cells(["VS"])
    for c in vs:
        e = edges[(pre[edges] == c) & np.isin(b.idx[edges], np.concatenate([cells[t][x] for t in ("CvN6", "CvN7") for x in "LR"]))]
        if not len(e):
            continue
        onto = {}
        for t in ("CvN6", "CvN7"):
            for x in "LR":
                m = np.isin(b.idx[e], cells[t][x])
                if m.any():
                    onto[f"{t} {x}"] = round(float(b.weights[e][m].sum()), 2)
        out["vs_cells"].append({"cell": int(c), "side": str(b.side[c]), "onto_mv": onto,
                                "rate_hz": {sc: round(float(rates[sc][:, c].mean()), 2) for sc in SCENES}})
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("vs cells", json.dumps(out["vs_cells"]), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
