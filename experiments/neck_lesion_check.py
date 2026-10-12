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
