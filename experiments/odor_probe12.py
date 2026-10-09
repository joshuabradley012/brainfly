"""Exploratory, not pre-registered: do the model's projection neurons make odors more alike than its receptor neurons
do, where flies' make them more separable?

odor_probe11.py: the current model's Kenyon cells answer different odors with overlapping populations, and evening out
their input helps only a little, because the odors' drives on them stay correlated (3-octanol against
4-methylcyclohexanol: r = 0.71 across Kenyon cells). In flies, projection neurons (PNs) are more broadly tuned than
their receptor neurons (ORNs), but odors lie farther apart in PN space than in ORN space: Bhandawat et al. 2007
(7 glomeruli, 18 odors) found the distances between odors "significantly larger in PN space as compared to ORN space
(p<0.0001, paired t-test, n=153)" early in the response, because the ORN-to-PN transformation has high gain for weak
inputs and flattens for strong ones, so PNs use their whole range more evenly.
Measured in odor_probe7.py's current model, each of its six odors with Turner's protocol (0.5 s, as odor_probe7.py):
  - each glomerulus's receptor neurons' rise in rate over the odor (their drive is DoOR's response above spontaneous
    times 200 Hz), and its uniglomerular PNs' rise, over the first 100 ms (the early epoch) and over the 0.5 s;
  - between each pair of odors, the correlation of the glomerular patterns and their Euclidean distance (Hz), in ORN
    space and PN space, over the glomeruli with both;
  - each odor's breadth: glomeruli whose ORNs or PNs rise by at least 10 Hz, and the PN rise in glomeruli whose ORNs
    aren't driven (spillover through the antennal lobe); and the share of uniglomerular PNs responding by Turner et
    al. 2008's criterion, the one odor_probe7.py applies to Kenyon cells (flies: 59 +- 14% of PNs, n = 37);
  - the Kenyon cells' drive (each cell's PN weights times the PNs' rises over the 0.5 s, as odor_probe11.py) against
    a static drive, the same weights times DoOR's responses of the PNs' glomeruli: the drives' correlations between
    odors across Kenyon cells, and each odor drive's correlation with the cells' summed PN weight.
Seeds 50000 + odor.

Ran: the projection neurons look fly-like on both measures available, so the overlap arises in the Kenyon cells. By
Turner's criterion 49-71% of uniglomerular PNs respond to each odor (flies: 59 +- 14%), and early in the response odors
lie farther apart in PN space than in ORN space in all 15 pairs (a mean distance of 420 against 281 Hz over the first
100 ms; over the whole 0.5 s 287 against 282, farther in 6), as Bhandawat et al. found. As in flies the PNs are more
broadly tuned than their ORNs: 22-36 of the 50 glomeruli with both rise by at least 10 Hz (ORNs: 12-25), 38-47 in the
first 100 ms, and the glomerular patterns correlate more between odors (r = 0.54-0.59 against 0.32), with little
spillover into undriven glomeruli over the 0.5 s (1.6-6.5 Hz on average; 0-4 glomeruli above 10 Hz). Through the
PN-to-KC wiring the odors' drives correlate still more (r = 0.80 on average, against 0.50 for DoOR's responses through
the same weights), and each odor's drive follows the cells' summed PN weight (r = 0.60-0.80; static 0.35-0.62): broad
PN input reaches most of each cell's claws, so the cells with the most PN weight answer nearly every odor. Flies' Kenyon
cells stay odor-specific with input this broad.

    python experiments/odor_probe12.py         (writes experiments/odor_probe12.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 50000
RISE_HZ = 10.0


def corr(a: np.ndarray, b: np.ndarray) -> float:
    return round(float(np.corrcoef(a, b)[0, 1]), 3) if a.std() > 0 and b.std() > 0 else None


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    o.set(p7.CURRENT, SEED + 90)
    b, types, m = o.brain, o.types, o.m
    kc = np.flatnonzero(m["kc"])
    orn_glom = {t[4:] for t in types[m["orn"]]}
    pn_glom = {t.split("_")[0] for t in types[m["upn"]]}
    gloms = sorted(orn_glom & pn_glom)
    orn_of = {g: np.flatnonzero(types == f"ORN_{g}") for g in gloms}
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(o.pn_kc)
    slot = np.searchsorted(kc, b.idx[e])
    w = b.weights[e].astype(np.float64)
    summed = np.bincount(slot, w, len(kc))
    pre_glom = np.array([t.split("_")[0] for t in types[pre[e]]])
    out = {"question": __doc__, "glomeruli": gloms, "odors": {}}
    space = {k: {} for k in ("door", "orn_early", "orn", "pn_early", "pn")}
    drive, static = {}, {}
    for k, odor in enumerate(p7.ODORS):
        kc_mask, o.m["kc"] = o.m["kc"], o.m["upn"]               # run bins o.m["kc"]'s cells: bin the PNs instead
        try:
            r = p7.run(o, odor, SEED + k, 0.5, 1.5)
        finally:
            o.m["kc"] = kc_mask
        pn_turner = p7.turner_responders(r)
        early = (r["first"] / 0.1 - r["rest"]).mean(0)                          # Hz rise, first 100 ms
        whole = (r["odor"] / 0.5 - r["rest"]).mean(0)                           # Hz rise, 0.5 s
        door = odors.glomeruli(odor)
        space["door"][odor] = np.array([door.get(g, 0.0) for g in gloms])
        for name, x in (("orn_early", early), ("orn", whole)):
            space[name][odor] = np.array([x[orn_of[g]].mean() for g in gloms])
        for name, x in (("pn_early", early), ("pn", whole)):
            space[name][odor] = np.array([x[pn_of[g]].mean() if len(pn_of[g]) else 0.0 for g in gloms])
        drive[odor] = np.bincount(slot, w * whole[pre[e]], len(kc))
        static[odor] = np.bincount(slot, w * np.array([door.get(g, 0.0) for g in pre_glom]), len(kc))
        driven = space["door"][odor] > 0
        out["odors"][odor] = {
            "pn_share_turner": round(float(pn_turner.mean()), 3),
            "glomeruli_door_responding": int(driven.sum()),
            "glomeruli_orn_rise_10hz": int((space["orn"][odor] >= RISE_HZ).sum()),
            "glomeruli_pn_rise_10hz": int((space["pn"][odor] >= RISE_HZ).sum()),
            "glomeruli_pn_rise_10hz_early": int((space["pn_early"][odor] >= RISE_HZ).sum()),
            "pn_rise_hz_driven": round(float(space["pn"][odor][driven].mean()), 1) if driven.any() else None,
            "pn_rise_hz_undriven": round(float(space["pn"][odor][~driven].mean()), 1),
            "pn_undriven_rising_10hz": int(((space["pn"][odor] >= RISE_HZ) & ~driven).sum()),
            "kc_drive_vs_summed_weight": corr(drive[odor], summed),
            "kc_static_vs_summed_weight": corr(static[odor], summed),
            "patterns": {name: [round(float(x), 2) for x in space[name][odor]] for name in space}}
        print(odor, json.dumps({x: y for x, y in out["odors"][odor].items() if x != "patterns"}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["pairs"] = {}
    for a, z in combinations(p7.ODORS, 2):
        row = {}
        for name, s in space.items():
            row[f"{name}_corr"] = corr(s[a], s[z])
            if name != "door":
                row[f"{name}_distance_hz"] = round(float(np.linalg.norm(s[a] - s[z])), 1)
        row["kc_drive_corr"], row["kc_static_corr"] = corr(drive[a], drive[z]), corr(static[a], static[z])
        out["pairs"][f"{a} | {z}"] = row
    mean = lambda key: round(float(np.mean([p[key] for p in out["pairs"].values() if p[key] is not None])), 3)
    out["means"] = {key: mean(key) for key in next(iter(out["pairs"].values()))}
    out["pn_farther_than_orn"] = {"early": int(sum(p["pn_early_distance_hz"] > p["orn_early_distance_hz"] for p in out["pairs"].values())),
                                  "whole": int(sum(p["pn_distance_hz"] > p["orn_distance_hz"] for p in out["pairs"].values())),
                                  "of": len(out["pairs"])}
    out["seconds"] = round(time.perf_counter() - t0)
    print(json.dumps({"means": out["means"], "pn_farther_than_orn": out["pn_farther_than_orn"]}, indent=1), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
