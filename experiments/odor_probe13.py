"""Exploratory, not pre-registered: if each Kenyon cell's excitability is matched to its own input, as flies' is thought
to be, do its odor responses become odor-specific?

odor_probe11.py and odor_probe12.py: the projection neurons (PNs) respond as broadly as flies', and the Kenyon cells with
the most PN input answer nearly every odor, so 80% of 4-methylcyclohexanol's responding cells also answer 3-octanol
(flies: dissimilar odors share about a fifth, Campbell et al. 2013). Evening out each cell's summed PN weight helps
only a little. Abdelrahman et al. 2021 argue that flies' Kenyon cells match excitability to input, so that each
answers a similar share of odors, by activity-dependent and activity-independent means, and find correlations in the
hemibrain consistent with it; Apostolopoulou & Lin 2020 show Kenyon cells adjusting their excitability in vivo.
Compensation here: each Kenyon cell's distance below threshold at rest set in proportion to its own strong drive.
For each cell, q is the 94th percentile of its drive over a training panel of 30 DoOR odors that excludes the six test
odors (the drive as in odor_probe11.py, its PN weights times the PNs' rise, over an odor's first 100 ms, when most
Kenyon cell spikes come), so that if a cell fired whenever its drive crossed its threshold it would answer 6% of
odors, Turner et al. 2008's mean. Each cell's distance is 21.5 mV x q / mean(q), the mean kept at Turner's 21.5 mV,
clipped to 8.5-34.5 mV (Turner's spread's 1st to 99th percentiles), the mean taken over:
  matched                 all Kenyon cells, so classes with weaker input get nearer threshold
  matched within types    each type, so each type's mean stays at 21.5 mV as in the current model
against the current model (each type's mean 21.5 mV) on the same seeds. Nothing here is fitted to the test odors'
responses. Measured for the six test odors as odor_probe7.py and odor_probe11.py measure them: the shares and classes
responding, spikes per response, MBON11's evoked spikes, the overlaps (Jaccard, and Campbell's share of one odor's
responders answering another), how many odors each cell answers, and the resting brain. Seeds 60000 + 100 x condition
+ odor (Turner's protocol), + 50 + odor (Hige's), + 90 (each type's rest), + 80 (each cell's), + 95 (the resting
brain); the training panel 60500 + odor.

Ran: matching helps, but only partway. Across all cells it brings the mean Jaccard over the 15 odor pairs from 0.43 to
0.35, and the share of 4-methylcyclohexanol's responders that also answer 3-octanol from 77% to 58% (flies' dissimilar
odors: about 22%); 69 cells answer all six odors (112 before). Within types it does about as well (0.34; 64%; 89 cells).
The classes are the striking part. Matched across all cells, alpha'/beta' cells get the smallest distances (16.0 mV on
average, against 25.0 for alpha/beta and 20.4 for gamma): 9 mV nearer threshold than alpha/beta, between Inada et al.'s
5.5 mV and Groschner's and Chen's 13, though nothing about classes went into the matching. alpha/beta cells then respond
at 3.3-8.5% and alpha'/beta' at 8.6-12.1% (flies: about 3-8 and 9-14%), but gamma at 11.7-20% (flies: about 2%; the
measured gamma thresholds lie 2.5-11 mV farther than alpha/beta's, where matching puts them 4.7 mV nearer). Each cell
answers 10 +- 23% of the odors (flies 6 +- 12%). The costs: 504 cells with little drive sit at the 8.5 mV floor, Kenyon
cells rest at 0.07 Hz (0.005 before), and MBON11 gains only 0.1-1.4 spikes. The resting brain stays at 0.96 Hz.

    python experiments/odor_probe13.py         (writes experiments/odor_probe13.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

import odor_probe11 as p11
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 60000
TRAINING = ("2,3-butanedione", "pentyl acetate", "e2-hexenal", "propanoic acid", "butyric acid", "putrescine",
            "ammonium hydroxide", "phenethyl alcohol", "geranyl acetate", "2,3-butanediol", "acetic acid", "butanal",
            "phenylacetaldehyde", "ethyl butyrate", "1-octen-3-ol", "acetone", "1-hexanol", "cyclohexanone",
            "2-methylphenol", "methyl salicylate", "2-butanone", "1-butanol", "propanal", "acetophenone",
            "6-methyl-5-hepten-2-one", "3-methyl-butanol", "cadaverine", "propyl acetate", "hexyl acetate", "4-methylphenol")
SHARE, GAP, LOW, HIGH = 0.06, 21.5, 21.5 - 2.33 * 5.6, 21.5 + 2.33 * 5.6
CONDITIONS = ("current", "matched", "matched within types")


def training_drives(o: p7.Olfaction) -> np.ndarray:
    """Each Kenyon cell's early drive for each training odor (odors x cells), in the current model."""
    e, slot, pre, _, _, _ = p11.pn_input(o)
    kc = np.flatnonzero(o.m["kc"])
    w = o.brain.weights[e].astype(np.float64)
    out = []
    for k, odor in enumerate(TRAINING):
        r = p7.run(o, odor, SEED + 500 + k, 0.5, 1.5)
        early = (r["first"] / 0.1 - r["rest"]).mean(0)
        out.append(np.bincount(slot, w * early[pre[e]], len(kc)))
        print("training", odor, f"PN rise {early[o.m['upn']].mean():.1f} Hz", flush=True)
    return np.array(out)


def gaps(o: p7.Olfaction, drives: np.ndarray, within_types: bool) -> np.ndarray:
    q = np.quantile(drives, 1 - SHARE, axis=0)
    types = o.types[o.m["kc"]]
    g = np.zeros(len(q))
    groups = [types == t for t in np.unique(types)] if within_types else [np.ones(len(q), bool)]
    for m in groups:
        g[m] = GAP * q[m] / max(q[m].mean(), 1e-12)
    return np.clip(g, LOW, HIGH)


def measure(o: p7.Olfaction, name: str, base: int) -> dict:
    kc = np.flatnonzero(o.m["kc"])
    out = {"rest": p7.rest_measures(o, base + 95), "odors": {}}
    responses = []
    for k, odor in enumerate(p7.ODORS):
        row, resp = p7.measure_odor(o, odor, base + k, base + 50 + k)
        out["odors"][odor] = row
        responses.append(resp)
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "evoked_spikes_0_1.4s")}), flush=True)
    R = np.array(responses)
    count = R.sum(0)
    out["odors_per_cell"] = {"model": np.bincount(count, minlength=7).tolist(),
                             "independent": [round(float(x) * len(kc), 1) for x in p11.independent(R.mean(1))],
                             "mean_share_of_odors": round(float(count.mean() / len(p7.ODORS)), 4),
                             "sd_share_of_odors": round(float((count / len(p7.ODORS)).std()), 4), "flies_turner": "6 +- 12%"}
    out["pairs"] = {}
    for i, j in combinations(range(len(p7.ODORS)), 2):
        both = (R[i] & R[j]).sum()
        out["pairs"][f"{p7.ODORS[i]} | {p7.ODORS[j]}"] = {
            "jaccard": round(float(both / max((R[i] | R[j]).sum(), 1)), 3),
            "share_of_first_in_second": round(float(both / max(R[i].sum(), 1)), 3),
            "share_of_second_in_first": round(float(both / max(R[j].sum(), 1)), 3)}
    out["mean_jaccard"] = round(float(np.mean([p["jaccard"] for p in out["pairs"].values()])), 3)
    weaker = [min(p["share_of_first_in_second"], p["share_of_second_in_first"]) for p in out["pairs"].values()]
    stronger = [max(p["share_of_first_in_second"], p["share_of_second_in_first"]) for p in out["pairs"].values()]
    out["mean_share_in_other"] = {"lower": round(float(np.mean(weaker)), 3), "higher": round(float(np.mean(stronger)), 3)}
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    out = {"question": __doc__, "flies": p7.FLIES, "training": list(TRAINING), "conditions": {}}
    o.set(p7.CURRENT, SEED + 90)
    drives = training_drives(o)
    out["training_drive_percentiles"] = [round(float(x), 2) for x in np.percentile(np.quantile(drives, 1 - SHARE, axis=0), (5, 25, 50, 75, 95))]
    for c, name in enumerate(CONDITIONS):
        base = SEED + 100 * c
        entry = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
        if name != "current":
            target = gaps(o, drives, name == "matched within types")
            entry["target_gap_mv"] = {"mean": round(float(target.mean()), 2), "sd": round(float(target.std()), 2),
                                      "clipped_low": int((target <= LOW).sum()), "clipped_high": int((target >= HIGH).sum()),
                                      **{cn: round(float(target[np.char.startswith(o.types[o.m["kc"]], p)].mean()), 2)
                                         for cn, p in p7.CLASSES.items()}}
            entry["kc_rest_each"] = p11.set_each_rest(o, target, base + 80)
        entry.update(measure(o, name, base))
        out["conditions"][name] = entry
        pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "shares_in_other": entry["mean_share_in_other"],
                                "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
