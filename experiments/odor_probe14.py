"""Exploratory, not pre-registered: do the antennal lobe's cholinergic local neurons, which the model lets excite
projection neurons chemically, cause the onset spillover that makes Kenyon cells answer every odor?

odor_probe12.py: in an odor's first 100 ms, projection neurons (PNs) of glomeruli whose receptors aren't driven rise
by 16-26 Hz on average (for 4-methylcyclohexanol 24 of its 32 undriven glomeruli rise by at least 10 Hz), though
hardly at all over the whole 0.5 s, and most Kenyon cell spikes come in those first 100 ms. The model takes the
connectome's synapses from cholinergic local neurons (LNs) onto PNs as chemical excitation: 36% as many synapses as
the receptor neurons give PNs. In flies "eLN-to-iLN synapses are largely cholinergic, whereas eLN-to-PN synapses are
mainly or purely electrical", with a coupling coefficient of about 0.01 (Yaksi & Wilson 2010; research_notes/Rung 4
resting state data/short_term_plasticity.md), so the connectome's cholinergic LN-to-PN synapses probably overstate
lateral excitation. (Huang et al. 2010 report cholinergic synapses as well, in an abstract.)
Conditions:
  current                odor_probe7.py's current model
  no cholinergic LN->PN  its synapses from cholinergic antennal lobe LNs onto uniglomerular PNs removed (types lLN,
                         ilNLN, vNLN, vLN, lvLN, lNLN, LN with consensus transmitter acetylcholine), the weak
                         electrical coupling left out; each PN's bias raised by the mean input it lost at rest (their
                         resting rates x weight x the 5 ms synaptic time constant), so that the resting brain stays put
Measured for each: the PNs as odor_probe12.py measures them (the share responding by Turner's criterion, flies
59 +- 14%; the rise in undriven glomeruli in the first 100 ms and over 0.5 s; the glomerular patterns' correlations
between odors), the Kenyon cells as odor_probe11.py measures them (shares, classes, the overlaps, how many odors each
answers, the drives' correlation), MBON11's evoked spikes (Hige et al.'s protocol), and the resting brain. Seeds
70000 + 100 x condition + odor (Turner's protocol), + 50 + odor (Hige's), + 90 (the Kenyon cells' rest), + 95 (the
resting brain), + 97 (the PNs' resting rates).

Ran: the cholinergic LNs cause the onset spillover. Without their 152,952 synapses onto PNs (10,750 connections), PNs of
undriven glomeruli no longer rise in an odor's first 100 ms (-3.6 to +1.4 Hz on average, against +16 to +24; 0-2
glomeruli above 10 Hz, against 7-21), while driven glomeruli still rise by 93-122 Hz and PNs answer at 159-176 Hz in
the first 100 ms (flies: 100-200). PNs stay about as broad as flies' by Turner's criterion (36-60% responding, against
43-71% before; flies 59 +- 14%) and rest at 3.8 Hz (2.9 before, with each PN's bias raised by the 0.9 mV of input it
lost; flies 4.6 +- 4.2). The Kenyon cells get sparser and somewhat more specific: 3.7-16.2% respond (6.5-19.7% before;
flies 6 +- 5%), the mean Jaccard over odor pairs falls from 0.43 to 0.35, and 43 cells answer all six odors (106 before).
But the odors' drives on the Kenyon cells stay correlated (r = 0.77 against 0.80), and 4-methylcyclohexanol, now
answered by only 3.7% of the cells, shares 82% of them with 3-octanol: the cells with the most PN input still answer
nearly everything. The classes don't change (alpha'/beta' 1-3%, gamma 5-17%), MBON11 gains 2-6 spikes as before, and
the resting brain stays at 0.98 Hz.

    python experiments/odor_probe14.py         (writes experiments/odor_probe14.json)
"""
from __future__ import annotations

import json
import re
import time
from itertools import combinations
from pathlib import Path

import numpy as np

import odor_probe11 as p11
import odor_probe3 as p3
import odor_probe7 as p7
from brainfly import odors
from brainfly.hybrid import consensus_transmitters
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED = 70000
LN = re.compile(r"^(lLN|il\dLN|v\dLN|vLN\d|lvLN|l\dLN|LN\d)")
CONDITIONS = ("current", "no cholinergic LN->PN")


def cholinergic_ln_edges(o: p7.Olfaction) -> np.ndarray:
    """The brain's edges from cholinergic antennal lobe LNs onto uniglomerular PNs."""
    b = o.brain
    nt = np.asarray(consensus_transmitters())
    assert len(nt) == b.n
    ln = np.array([bool(LN.match(t)) for t in o.types]) & (nt == "acetylcholine")
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    return ln[pre] & o.m["upn"][b.idx]


def run_binning_pns(o: p7.Olfaction, odor: str, seed: int) -> dict:
    """odor_probe7.run with Turner's protocol, its 200 ms bins taken over the uniglomerular PNs instead of the Kenyon
    cells (run bins o.m["kc"]'s cells)."""
    kc_mask, o.m["kc"] = o.m["kc"], o.m["upn"]
    try:
        return p7.run(o, odor, seed, 0.5, 1.5)
    finally:
        o.m["kc"] = kc_mask


def remove(o: p7.Olfaction, edges: np.ndarray, seed: int) -> dict:
    """Zero the edges and raise each target's bias by the mean input it lost at rest."""
    b = o.brain
    rate = p3.rest_state(o.s, seed, False)["counts"].mean(0)          # 1 s of rest: spikes = Hz
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    lost = np.bincount(b.idx[edges], weights=rate[pre[edges]] * b.weights[edges] * TAU, minlength=b.n)
    w = b.weights.copy()
    w[edges] = 0.0
    b.weights, b._external_matrix = w, None
    b.set_bias(o.own_bias() + lost)                                    # set_bias adds the ring's offsets back
    upn = o.m["upn"]
    return {"edges": int(edges.sum()), "synapses": int(b._counts[edges].sum()),
            "lost_mean_input_mv": {"upn_mean": round(float(lost[upn].mean()), 3), "upn_max": round(float(lost[upn].max()), 3)}}


def pn_measures(o: p7.Olfaction, r: dict, door: dict, gloms: list, pn_of: dict) -> dict:
    early = (r["first"] / 0.1 - r["rest"]).mean(0)
    whole = (r["odor"] / 0.5 - r["rest"]).mean(0)
    pe = np.array([early[pn_of[g]].mean() for g in gloms])
    pw = np.array([whole[pn_of[g]].mean() for g in gloms])
    driven = np.array([door.get(g, 0.0) > 0 for g in gloms])
    return {"early": pe, "whole": pw, "summary": {
        "undriven_glomeruli": int((~driven).sum()), "undriven_early_rise_hz": round(float(pe[~driven].mean()), 1),
        "undriven_early_rising_10hz": int((pe[~driven] >= 10).sum()), "undriven_whole_rise_hz": round(float(pw[~driven].mean()), 1),
        "driven_early_rise_hz": round(float(pe[driven].mean()), 1), "glomeruli_early_rising_10hz": int((pe >= 10).sum())}}


def condition(o: p7.Olfaction, name: str, c: int, gloms: list, pn_of: dict) -> dict:
    base = SEED + 100 * c
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    if name != "current":
        out["removed"] = remove(o, cholinergic_ln_edges(o), base + 97)
        out["kc_rest_recalibration"] = p3.set_kc_rest(o.s, o.m["kc"], o.types, o.own_bias(), base + 90)[-1]
    out["rest"] = p7.rest_measures(o, base + 95)
    e, slot, pre, pn_weight, _, _ = p11.pn_input(o)
    kc = np.flatnonzero(o.m["kc"])
    w = o.brain.weights[e].astype(np.float64)
    out["odors"], responses, drive, pn_early = {}, [], [], []
    for k, odor in enumerate(p7.ODORS):
        rp = run_binning_pns(o, odor, base + k)           # the same run as measure_odor's Turner protocol, PNs binned
        pn_share = float(p7.turner_responders(rp).mean())
        row, resp = p7.measure_odor(o, odor, base + k, base + 50 + k)
        pm = pn_measures(o, rp, odors.glomeruli(odor), gloms, pn_of)
        whole = (rp["odor"] / 0.5 - rp["rest"]).mean(0)
        row.update(pn_share_turner=round(pn_share, 3), pn_onset=pm["summary"])
        out["odors"][odor] = row
        responses.append(resp)
        drive.append(np.bincount(slot, w * whole[pre[e]], len(kc)))
        pn_early.append(pm["early"])
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "evoked_spikes_0_1.4s", "pn_share_turner", "pn_onset")}), flush=True)
    R, D, P = np.array(responses), np.array(drive), np.array(pn_early)
    count = R.sum(0)
    out["odors_per_cell"] = {"model": np.bincount(count, minlength=7).tolist(),
                             "independent": [round(float(x) * len(kc), 1) for x in p11.independent(R.mean(1))],
                             "sd_share_of_odors": round(float((count / len(p7.ODORS)).std()), 4)}
    out["pairs"] = {}
    for i, j in combinations(range(len(p7.ODORS)), 2):
        both = (R[i] & R[j]).sum()
        out["pairs"][f"{p7.ODORS[i]} | {p7.ODORS[j]}"] = {
            "jaccard": round(float(both / max((R[i] | R[j]).sum(), 1)), 3),
            "share_of_first_in_second": round(float(both / max(R[i].sum(), 1)), 3),
            "share_of_second_in_first": round(float(both / max(R[j].sum(), 1)), 3),
            "kc_drive_corr": round(float(np.corrcoef(D[i], D[j])[0, 1]), 3),
            "pn_early_corr": round(float(np.corrcoef(P[i], P[j])[0, 1]), 3)}
    for key in ("jaccard", "kc_drive_corr", "pn_early_corr"):
        out[f"mean_{key}"] = round(float(np.mean([p[key] for p in out["pairs"].values()])), 3)
    out["kc_responses_vs_pn_weight"] = p11.quintiles(pn_weight, R.mean(0))
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m = o.types, o.m
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "glomeruli": len(gloms), "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = e = condition(o, name, c, gloms, pn_of)
        pair = e["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": e["rest"], "removed": e.get("removed"), "mean_jaccard": e["mean_jaccard"],
                                "mean_kc_drive_corr": e["mean_kc_drive_corr"], "mean_pn_early_corr": e["mean_pn_early_corr"],
                                "oct_mch": pair, "odors_per_cell": e["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
