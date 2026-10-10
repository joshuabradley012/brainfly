"""Exploratory check, not pre-registered: how do the model's receptor-to-PN connections differ from glomerulus to
glomerulus, against flies'?

odor_probe7.py scales every receptor neuron-to-PN synapse by one factor, chosen so that the mean same-glomerulus
connection gives Kazama & Wilson 2008's 6.19 mV rested unitary EPSP. Each connection's EPSP is then proportional to its
MaleCNS synapse count, so glomeruli whose connections have more synapses get larger EPSPs. In flies the rested unitary
EPSPs are matched across glomeruli (DM6 5.5, VM2 5.4, DL5 7.0, DM4 6.9 mV) while the unitary currents differ about
3-fold (13-41 pA), the PNs' input resistance making up the difference (Kazama & Wilson 2008, "homeostatic matching"),
and every receptor neuron of a glomerulus contacts every PN of it (Kazama & Wilson 2009; Tobin et al. 2017). The
convergence sets the transform's weak-input gain (sigma falls about as 1 / sqrt(N) in a one-PN model;
research_notes/Rung 9 learning data/weak_input_gain.md), and the model's DM4 reaches only 81 spikes/s (flies 170).
Model: odor_probe7.py's connectome (no build needed: the weights are MaleCNS synapse counts times the one factor).
Measured, per glomerulus with uniglomerular PNs: receptor neurons and PNs, the share of receptor neuron-PN pairs
connected, synapses per connection, the rested unitary EPSP (fast and slow components together, 6.19 mV on average),
and the summed rested EPSP one spike in every receptor neuron of the glomerulus puts on each PN; against Grabe et al.
2016's receptor neuron counts (per antenna, female/male) and Kazama & Wilson's uEPSPs.

Ran: the model's unitary EPSPs vary far more across glomeruli than flies', and DM4's connections are among the weakest
and least complete. The one factor on synapse counts, divided by each PN's total input (the 1 / size scale), gives the
same-glomerulus connections 3.3-16.4 mV across the 50 glomeruli with uniglomerular PNs (5th-95th percentile; median
7.7), falling as the glomerulus's receptor neurons grow in number (r = -0.65; DL2d 19.4 mV with 15 receptor neurons, DA1
2.6 with 204). Where Kazama & Wilson measured them: DM4 4.5 mV (flies 6.9), DL5 6.9 (7.0), DM6 7.0 (5.5), VM2 9.0 (5.4).
Some glomeruli's convergence is incomplete: DM4's 32 receptor neurons reach 68% of their pairs with its 4 PNs (flies:
every one), DM3's 52%, VL2p's 49%. One spike in every receptor neuron of DM4 puts 97 mV on each of its PNs (the summed
rested EPSPs), where DL5 gets 291 and most glomeruli 156-394 (5th-95th percentile): DM4's PNs get a third of DL5's
drive, which accounts for its low Rmax (81 spikes/s; flies 170; DL5 166-187). The receptor neuron counts are a male's:
DM4 32, DL5 43, DM1 74, VM7d 36 over both antennae (Grabe et al. per antenna, female/male: 23/15.5, 24/21, 38.5/32,
11.5/15).

    python experiments/orn_pn_glomeruli_check.py      (writes experiments/orn_pn_glomeruli_check.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import odor_probe10 as p10
import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
KW08_UEPSP_MV = {"DM6": 5.5, "VM2": 5.4, "DL5": 7.0, "DM4": 6.9}
GRABE_PER_ANTENNA = {"DM4": (23, 15.5), "DL5": (24, 21), "DM1": (38.5, 32), "VM7d": (11.5, 15), "VM2": (18, 15),
                     "DM6": (18, 10.5), "DA1": (62.5, 62.25), "VA2": (43.5, 32), "DM2": (8, 8), "DM3": (34, 31)}


def main() -> None:
    o = p7.Olfaction()
    b, types, m = o.brain, o.types, o.m
    rec = p10.Receptors(o)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(o.orn_pn)
    glom_pre = np.array([t[4:] for t in types[pre[e]]])
    glom_post = np.array([t.split("_")[0] for t in types[b.idx[e]]])
    same = e[glom_pre == glom_post]
    counts = b._counts.astype(float)
    mean_all = float(o.w0[same].mean())
    uepsp = p3.UNITARY_MV * o.w0 / mean_all                  # rested unitary EPSP per edge, mV (6.19 on average)
    rows = {}
    for g in rec.glomeruli:
        orns = np.flatnonzero(types == f"ORN_{g}")
        pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
        if not len(orns) or not len(pns):
            continue
        sel = same[np.isin(pre[same], orns) & np.isin(b.idx[same], pns)]
        per_pn = np.bincount(b.idx[sel], weights=uepsp[sel], minlength=b.n)[pns]
        rows[g] = {"orns": int(len(orns)), "upns": int(len(pns)),
                   "connected_share": round(len(sel) / (len(orns) * len(pns)), 3),
                   "synapses_per_connection": round(float(counts[sel].mean()), 1) if len(sel) else 0.0,
                   "uepsp_mv": round(float(uepsp[sel].mean()), 2) if len(sel) else 0.0,
                   "summed_uepsp_per_pn_mv": round(float(per_pn.mean()), 1),
                   "spontaneous_hz": rec.spont[g]}
        if g in GRABE_PER_ANTENNA:
            rows[g]["grabe_per_antenna_female_male"] = GRABE_PER_ANTENNA[g]
        if g in KW08_UEPSP_MV:
            rows[g]["kw08_uepsp_mv"] = KW08_UEPSP_MV[g]
    u = np.array([r["uepsp_mv"] for r in rows.values()])
    s = np.array([r["summed_uepsp_per_pn_mv"] for r in rows.values()])
    n = np.array([r["orns"] for r in rows.values()])
    out = {"question": __doc__, "glomeruli": len(rows),
           "uepsp_mv_quantiles_5_25_50_75_95": np.percentile(u, [5, 25, 50, 75, 95]).round(2).tolist(),
           "summed_uepsp_mv_quantiles_5_25_50_75_95": np.percentile(s, [5, 25, 50, 75, 95]).round(1).tolist(),
           "orns_quantiles_5_25_50_75_95": np.percentile(n, [5, 25, 50, 75, 95]).round(1).tolist(),
           "corr_orns_vs_uepsp": round(float(np.corrcoef(n, u)[0, 1]), 3),
           "glomeruli_by_name": dict(sorted(rows.items()))}
    for g in ("DM4", "DL5", "VM7d", "DM1", "VM2", "DM6", "DA1", "VA2", "DM2", "DM3"):
        if g in rows:
            print(g, json.dumps(rows[g]), flush=True)
    for k in ("uepsp_mv_quantiles_5_25_50_75_95", "summed_uepsp_mv_quantiles_5_25_50_75_95", "orns_quantiles_5_25_50_75_95",
              "corr_orns_vs_uepsp"):
        print(k, out[k], flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
