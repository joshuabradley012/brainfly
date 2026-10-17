"""Exploratory check, written after review 15 and before it runs, not pre-registered and not a change to the model: do the
neck motor neurons' visual responses in rung 6's brain come through their direct synapses from the lobula plate's cells?

rung8_neck_yaw.py passed as written, but review 15 found two gaps:
- Its null scrambled the whole network, including the HS cells' own inputs, so it couldn't test the HS- and
  H2-to-yaw-MN synapses. Deleting those synapses alone would.
- Its selectivity criterion compared CvN7 with VCvN1-3. Gorko et al.'s map compares CvN7's own horizontal and vertical
  responses; summed linearly over the authors' grid, it predicts a yaw-to-vertical ratio of 0.12-0.16. On one seed,
  review 15 found 0.28.
Model: rung6_relay.build("intact") with its eyes (flyvis flow/0000/001 at gain 1), 8 flies, seed 7720 (new). Three
conditions:
- intact;
- HS/H2 cut: every synapse from HSN, HSE, HSS and H2 onto the yaw neck MNs (GNG647, GNG314, GNG653, GNG283, GNG276)
  set to zero, both sides;
- VS cut: every synapse from VS onto the pitch neck MNs CvN4-7 set to zero.
Scenes (eyes_at_rest.Setup.run: 1 s of grey, then 2 s; rates from 0.5 to 2 s; the same seed in every scene):
- grey;
- the drum counterclockwise and clockwise (30 deg vertical grating, 40 deg/s);
- horizontal stripes (30 deg) moving down and up at 40 deg/s.
Measured: the synapses each cut removes (count and summed weight, and per target type against all its excitatory
input), then in each condition:
- the yaw MNs' and DNp15's direction signals ((left - right under counterclockwise) - (left - right under clockwise),
  by soma side, which is their nerve side);
- CvN4-7's vertical signals (down - up, both cells);
- CvN7's yaw signal by nerve side;
- each group's rate at grey.
In the intact brain, CvN7's yaw-to-vertical ratio (|yaw| / vertical) is reported against the map's 0.12-0.16.
Read:
- If cutting the HS/H2 synapses cuts the yaw MNs' direction signals by 80% or more while DNp15 (not cut) keeps its,
  the direct synapses carry the signal. If much of it survives, longer routes carry it too.
- If cutting VS cuts CvN7's vertical signal by half or more, its weak downward response comes through its direct VS
  synapses.

Ran (2026-10-12, 313 s): by the readings, the direct HS/H2 synapses carry most of the drum's signal for four of the five
yaw types and less than half of it for CvN1/2. CvN7's downward preference comes entirely through its VS synapses.
Unexpectedly, so does most of CvN6's drum signal. A cut removes a synapse's tonic drive along with its signal, so part
of each loss may be lost gain.
- The cuts:
  - HS/H2 onto the yaw MNs: 37 cell-to-cell connections, 146.7 mV summed. As a share of each type's excitatory input
    weight: GNG283 4.4%, GNG276 2.4%, GNG647 1.8%, GNG314 0.6%, GNG653 0.4%.
  - VS onto CvN4-7: 26 connections, 84.9 mV. As a share: CvN7 2.3%, CvN6 2.2%, CvN5 0.8%, CvN4 0.6%.
- Intact, seed 7720, drum direction signals:
  - GNG283 +72.6 Hz (t 68), GNG276 +42.7 (t 32), GNG647 +36.7 (t 50), GNG653 +16.3 (t 16), GNG314 +2.75 (t 3.6);
  - VCvN1-3 pooled +22.0 (t 32), DNp15 +118.9 (t 206).
- HS/H2 cut, the same signals and the share kept:
  - GNG283 +9.0 (t 7.8; 12%), GNG276 +7.5 (t 8.9; 18%), GNG647 +10.7 (t 16; 29%), GNG314 +0.83 (t 2.4; 30%), GNG653
    +10.0 (t 13; 61%), VCvN1-3 +6.4 (t 14; 29%).
  - Unchanged to the last digit: DNp15, HS, H2, VS and CvN4-7. Each condition uses the same trial noise, and nothing the
    yaw MNs drive reaches those cells within the run.
- VS cut:
  - Vertical signals (down - up), intact to cut: CvN7 +3.9 (t 9.2) to -2.1 (t -4.4); CvN6 -0.9 (t -0.9) to -4.2 (t
    -6.9); CvN5 +0.8 to -2.7 (t -5.5); CvN4 +1.1 to +0.25.
  - Drum signals by nerve side: CvN6 +24.8 (t 34) to +5.75 (t 10; 23% kept), CvN5 +5.0 to +1.4 (28%), CvN4 +5.9 to +3.8
    (65%). CvN7 stays at -1.3. The yaw MNs and DNp15 are unchanged to the last digit.
- CvN7, intact: a yaw signal of -1.33 Hz by nerve side (t -2.8) against a vertical one of +3.92 (t 9.2), a ratio of
  0.34.
  - Seed 8800 gave 0.28 (review 15). The map predicts 0.12-0.16.
  - The yaw signal is small, so each ratio is uncertain: standard errors about 0.13 and 0.11 by the delta method. The
    two pooled give 0.31 +- 0.08, 1.8 standard errors above the map's 0.16.
So:
- By the readings:
  - The direct synapses carry the drum's signal for GNG283 and GNG276 (82-88% lost).
  - For VCvN1-3 they carry about 70%, short of the 80% the reading asks.
  - For CvN1/2 (GNG653) longer routes carry most of it.
  - DNp15 keeps its signal.
  - Longer routes give four of the five types 7.5-10.7 Hz of signal (t 8-16). Gap junctions, which the connectome
    can't show, would add routes of their own.
- CvN7's downward preference comes through its direct VS synapses. Without them CvN7 prefers upward motion, as CvN5
  and CvN6 then do. Some other input drives the pitch MNs upward, and in the intact brain VS outweighs it only in CvN7.
  The yaw MNs' upward route (neck_upward_check.py) may be the same one; that wasn't tested.
- Not anticipated: cutting VS's synapses also removes 77% of CvN6's drum signal. neck_drive_probe.py had inferred from
  the sides alone that CvN6 follows the drum through its HSS input.
- Both readings need one caveat. A cut removes a synapse's direction signal and its tonic drive together, and a
  neuron's rate isn't linear in its drive. Under either drum direction H2 fires at 68-150 Hz and VS at 12-19 Hz
  (neck_drive_probe.py's Ran and its review 14 note). So part of each loss may be lost gain rather than lost signal.
  neck_route_check.py, next, splits each input's drive into its direction change and its tonic part.
- CvN7's own selectivity: on both seeds that measured its yaw and vertical responses in one run, yaw is about twice the
  share the map predicts. With so little signal that isn't decisive. And CvN7 barely answers its preferred direction
  (+4 Hz), so the ratio rests on small numbers.

    python experiments/neck_lesion_check.py      (writes experiments/neck_lesion_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung6_relay as r6
from brainfly.eye2d import ElevationGrating, Grating

OUT = Path(__file__).with_suffix(".json")
SEED, GAIN = 7720, 1.0
WINDOW = (0.5, 2.0)
YAW = ["GNG647", "GNG314", "GNG653", "GNG283", "GNG276"]
PITCH = ["CvN4", "CvN5", "CvN6", "CvN7"]
SCENES = {"grey": lambda t: [], "ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)],
          "down": lambda t: [ElevationGrating(30.0, -40.0 * t)], "up": lambda t: [ElevationGrating(30.0, 40.0 * t)]}
GROUPS = {**{t: [t] for t in YAW + PITCH}, "VCvN1-3": ["GNG647", "GNG314"], "DNp15": ["DNp15"], "HS": ["HSN", "HSE", "HSS"],
          "H2": ["H2"], "VS": ["VS"]}


def tstat(d: np.ndarray) -> float:
    sd = float(d.std(ddof=1))
    return round(float(d.mean() / (sd / np.sqrt(len(d)))), 2) if sd > 0 else 0.0


def shares(b, pre: np.ndarray, weights: np.ndarray, src: np.ndarray, targets: list[str]) -> dict:
    """Per target type: the summed weight of the synapses cut and of all its excitatory input, in mV."""
    out = {}
    for t in targets:
        e = np.flatnonzero(np.isin(b.idx, b.cells([t])))
        w = weights[e]
        out[t] = {"cut_mv": round(float(w[src[pre[e]]].sum()), 1), "excitatory_input_mv": round(float(w[w > 0].sum()), 1)}
    return out


def measure(s, cells: dict) -> dict:
    per = {}
    for name, scene in SCENES.items():
        r = s.run(scene, GAIN, SEED, WINDOW)
        per[name] = {g: {x: r["rates"][:, v].mean(1) for x, v in d.items() if len(v)} for g, d in cells.items()}
    out = {"grey_hz": {g: {x: round(float(v.mean()), 2) for x, v in d.items()} for g, d in per["grey"].items()}, "yaw": {}, "vertical": {}}
    for g in GROUPS:
        if not all(x in per["ccw"][g] for x in "LR"):
            continue
        d = (per["ccw"][g]["L"] - per["ccw"][g]["R"]) - (per["cw"][g]["L"] - per["cw"][g]["R"])
        if g in ("CvN6", "CvN7"):
            d = -d                                  # by nerve side
        out["yaw"][g] = {"signal_hz": round(float(d.mean()), 3), "t": tstat(d)}
        v = sum(per["down"][g][x] - per["up"][g][x] for x in "LR")
        out["vertical"][g] = {"signal_hz": round(float(v.mean()), 3), "t": tstat(v)}
    return out


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    cells = {g: {x: b.cells(types, x) for x in "LR"} for g, types in GROUPS.items()}
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    saved = b.weights.copy()
    src_lptc = np.isin(np.arange(b.n), b.cells(["HSN", "HSE", "HSS", "H2"]))
    tgt_yaw = np.isin(np.arange(b.n), b.cells(YAW))
    src_vs = np.isin(np.arange(b.n), b.cells(["VS"]))
    tgt_pitch = np.isin(np.arange(b.n), b.cells(PITCH))
    cuts = {"intact": np.zeros(len(saved), bool), "HS/H2 cut": src_lptc[pre] & tgt_yaw[b.idx], "VS cut": src_vs[pre] & tgt_pitch[b.idx]}
    out = {"question": __doc__, "synapses_cut": {k: {"edges": int(v.sum()), "summed_weight_mv": round(float(saved[v].sum()), 1)} for k, v in cuts.items()},
           "cut_share": {"HS/H2 cut": shares(b, pre, saved, src_lptc, YAW), "VS cut": shares(b, pre, saved, src_vs, PITCH)},
           "conditions": {}}
    print("cuts", json.dumps(out["synapses_cut"]), json.dumps(out["cut_share"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    for name, cut in cuts.items():
        b.weights = np.where(cut, np.float32(0), saved).astype(np.float32)
        out["conditions"][name] = measure(s, cells)
        c = out["conditions"][name]
        print(name, json.dumps({"yaw": c["yaw"], "vertical": {g: c["vertical"][g] for g in PITCH}}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    b.weights = saved
    it = out["conditions"]["intact"]
    yaw7, vert7 = it["yaw"]["CvN7"]["signal_hz"], it["vertical"]["CvN7"]["signal_hz"]
    out["cvn7_yaw_over_vertical_intact"] = round(abs(yaw7) / vert7, 3) if vert7 > 0 else None
    keep = lambda g, c: round(out["conditions"][c]["yaw"][g]["signal_hz"] / it["yaw"][g]["signal_hz"], 3) if it["yaw"][g]["signal_hz"] else None
    out["yaw_signal_kept_after_hs_h2_cut"] = {g: keep(g, "HS/H2 cut") for g in YAW + ["VCvN1-3", "DNp15"]}
    vkeep = lambda g: round(out["conditions"]["VS cut"]["vertical"][g]["signal_hz"] / it["vertical"][g]["signal_hz"], 3) if it["vertical"][g]["signal_hz"] else None
    out["vertical_signal_kept_after_vs_cut"] = {g: vkeep(g) for g in PITCH}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("summary", json.dumps({k: out[k] for k in ("cvn7_yaw_over_vertical_intact", "yaw_signal_kept_after_hs_h2_cut", "vertical_signal_kept_after_vs_cut")}), flush=True)
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
