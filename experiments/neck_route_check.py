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

Ran (2026-10-17, 124 s): each cut took 20-30 points more of the drum's signal than the cut group's linear share of it
(GNG314 excepted). The cut groups also supply most of their targets' tonic drive under the drum. VS carries more of
CvN6's drum signal than HSS does. CvN7's downward drive from VS is mostly cancelled by inhibition from OCG01f.
- The loop reproduces neck_lesion_check.py's intact rates exactly: GNG283's direction signal is +72.583 Hz (t 68) and
  CvN7's vertical one +3.917 (t 9.2).
- Yaw MNs. Drives are in mV per target cell; the yaw change is summed over both sides. All inputs' yaw change, then HS
  and H2's, their share of it, and neck_lesion_check.py's loss:

  | Type | All inputs | HS | H2 | HS+H2 share | Lesion's loss |
  | --- | --- | --- | --- | --- | --- |
  | GNG283 | 35.5 | 13.5 | 9.7 | 65% | 88% |
  | GNG276 | 20.6 | 3.0 | 7.8 | 52% | 82% |
  | GNG647 | 21.2 | 7.3 | 3.1 | 49% | 71% |
  | GNG653 | 13.4 | 1.7 | 0.8 | 19% | 39% |
  | GNG314 | 4.7 | 2.9 | 0.3 | 68% | 70% |

  - HS and H2's mean drum drive, against all inputs': GNG283 10.2 mV (8.9), GNG276 6.2 (3.6), GNG647 4.0 (5.3), GNG653
    1.0 (2.9), GNG314 0.9 (1.6). H2 supplies most of it except in GNG314 (6.8, 5.5, 2.2, 0.6 and 0.2 mV), since it
    fires to the moving pattern in either direction.
  - The other inputs with the largest yaw changes: DNb03 (+7.5 onto GNG283, +2.3 onto GNG647, +1.9 onto GNG653),
    DNge006 (+7.5 onto GNG276, +2.5, +1.9 and +2.4 onto GNG283, GNG653 and GNG314) and CB3714 (+1.9 to +3.3 onto four
    types), all excitatory, and inhibitory AN_GNG_175, released (+3.4 onto GNG276, +1.6 onto GNG653). Opposing them:
    inhibitory CB0034 (-1.6 to -3.8 onto four types) and CB1042 (-3.6 onto GNG283).
- CvN6's yaw change is 11.15 mV (t 29).
  - VS gives 6.06 (54%), HSS 3.20 (29%), H2 2.26 (20%) and CB3714 3.21. OCG01f takes away 4.65.
  - VS's mean drum drive is 4.19 of CvN6's 5.60 mV.
- The VS cells onto CvN6 and CvN7:
  - Two answer the drum. Cell 4 (left) fires 108.8 Hz under the clockwise drum (back-to-front across its own eye) and
    50.1 under counterclockwise; cell 8 (right) is the mirror (114.3 and 50.3).
  - Both also fire to stripes moving either way (99-107 Hz down, 62-68 up). Their weights onto CvN6 are 8.4 and 11.8 mV.
  - By their weights onto CvN6 and CvN7 they match the note's rank-1 VS cells: the most frontal, with T4b/T5b input,
    as the note says Drosophila VS1 has (§3.2).
  - The other four VS cells fire at 0-2.7 Hz under the drum, and at 121.5-128.4 Hz to downward stripes and 0 to upward
    ones.
- Vertical changes (down - up, mV), VS's against all inputs':
  - CvN7 +15.7 against +3.4; CvN6 +11.7 against -1.1; CvN5 +5.5 against +1.7; CvN4 +1.4 against -0.7.
  - The largest opposing input is OCG01f, which is glutamatergic and so inhibitory in the model: -12.8 mV onto CvN7,
    -16.8 onto CvN6 and -4.2 onto CvN5.
  - DNg46 takes away 6.2 from CvN5, and CB0213 2.8 from CvN4 and 2.5 from CvN7. PS237 adds 2.4-5.2 to CvN4, CvN6 and
    CvN7.
So:
- By the reading, the yaw MNs' losses exceed HS and H2's linear share by 20-30 points (GNG283 88% against 65%, GNG276
  82 against 52, GNG647 71 against 49, GNG653 39 against 19). The excess is lost gain. GNG314's loss (70% against 68%)
  is its group's signal.
  - HS and H2 carry half to two-thirds of the yaw MNs' direction-selective drive directly (a fifth of CvN1/2's).
  - Mostly through H2, they also hold the cells nearer threshold under the drum, so that the rest of the signal turns
    into spikes.
  - The rest comes through descending and local cells that the drum also drives: DNb03, DNge006, CB3714 and
    AN_GNG_175, opposed by CB0034 and CB1042. Several of them (CB3714, DNge006, DNb03, CB0034) also carry the yaw MNs'
    upward response (neck_upward_check.py).
- CvN6: VS's yaw change outweighs HSS's (6.06 against 3.20 mV). So by the reading VS carries most of the drum's signal
  to CvN6, through the two frontal VS cells with back-to-front input. HSS carries about half as much.
  neck_drive_probe.py's reading of CvN6's input as HSS's was incomplete. The VS cut's 77% loss against VS's 54% linear
  share is lost gain: VS gives 4.2 of CvN6's 5.6 mV of drive under the drum.
- CvN7: its vertical drive from VS (+15.7 mV) is mostly cancelled by inhibition from OCG01f (-12.8). OCG01f is a cell
  of the ocellar ganglion, which MaleCNS lacks, so in the model OCG01f keeps only its brain inputs: 54% from OCG01b and
  18% from VS (the note's §3.4). The sign of its drive change says it fires more to downward stripes than upward ones.
  - The note predicted from the wiring that the VS-to-OCG01f route would oppose the direct one at about 0.4 of its
    size (W2 about -0.005 against W1 0.012-0.013).
  - In the model OCG01f's opposing drive is 0.8 of VS's direct drive onto CvN7 and 1.4 onto CvN6.
  - So CvN7's weak downward response here is VS's excitation minus OCG01f's inhibition. It rests on a cell that in
    flies also takes ocellar input, which the model doesn't have.
- Next, neck_ocg_check.py: cut OCG01f's synapses onto CvN4-7 and read CvN7's selectivity, OCG01f's and OCG01b's rates,
  and the VS cells' T4/T5 inputs.

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
