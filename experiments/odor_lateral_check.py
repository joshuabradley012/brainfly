"""Exploratory check, not pre-registered: can electrical coupling between the antennal lobe's cholinergic local neurons
and its projection neurons, which the model lacks, make weak input reach the PNs as it does in flies?

odor_probe41.py: with the receptor synapse's slow component at Kazama & Wilson's unitary size and the PNs keeping their
current, the antennal lobe opens and accommodates roughly as flies' does, but weak input reaches the PNs at about half
flies' strength (the transform's sigma 23-34 against Olsen et al.'s 12-16), only 29-43% of PNs respond to an odor
(flies 59 +- 14%), and 4-methylcyclohexanol reaches a quarter as many Kenyon cells as 3-octanol (flies 0.73-0.92);
odor_probe43.py: the PNs' resting rate isn't the cause. In flies, PNs whose own receptor neurons are gone still answer
odors through excitatory local neurons, largely by electrical synapses (Olsen et al. 2007; Yaksi & Wilson 2010). The
model's cholinergic LN-to-PN synapses were removed as chemical synapses (odor_probe14.py), and it has no electrical ones.
Model: odor_probe41.py's kw08_kept (its cache), as built (rest not polished again, inhibition not refitted, so this
shows only the direction), with an electrical synapse each way for every pair of a cholinergic antennal lobe LN and a
uniglomerular PN that MaleCNS connects by chemical synapses (the edges odor_probe14.py removed): each spike raises the
partner's membrane by k x the pair's synapse count / the median pair's count, k = 0.1, 0.3 and 1 mV (the kernel's
electrical synapses carry spikes only, not subthreshold voltage). No measured coupling strength is used yet.
Measured for each k: everything odor_probe36.py measures, on odor_probe41.py's seeds for kw08_kept (391000), so k = 0 is
odor_probe41.py's own result.

Ran (k = 0.1 only; stopped there): the coupling makes weak input reach the PNs worse, not better, because the PNs'
spikes excite the LNs. At k = 0.1 the GABAergic LNs rest at 4.8 spikes/s (4.4) and answer 2-heptanone with 33, 23, 17
and 11 spikes/s in Nagel et al.'s bins (24, 16, 11 and 8; flies 22, 13, 8 and 6); with the inhibition as fitted without
them, the PNs rest at 0.1 spikes/s (0.4), 3-octanol's peak at 87 (103) and its strongly driven ones at 149 (186); the
transform's sigma rises to 29-43 (23-34) and Rmax falls to 76-177 (84-198); 4-methylcyclohexanol reaches 0.16 as many
Kenyon cells as 3-octanol (0.23); PN breadth is mixed (25-38% by Turner's criterion, 29-43%). Meanwhile the measurements
arrived (research_notes/Rung 9 learning data/lateral_excitation.md): one eLN spike moves a PN by about 0.4 mV (Huang et
al. 2010), but the PN-to-eLN link is about 85% chemical (which the model already has), the net effect of lateral input on
PNs in intact flies is usually inhibitory (removing the antennae raised 18 of 20 VM7 odor responses; Olsen & Wilson
2008), and PNs stay broadly tuned without it (Wilson 2013). So this symmetric coupling overstates the PN-to-LN direction,
and electrical coupling isn't what the model's weak input lacks; the larger strengths weren't run.

    python experiments/odor_lateral_check.py      (writes experiments/odor_lateral_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import brain_cache
import odor_probe14 as p14
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe41 as p41
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
BASE = 391000
KICKS_MV = (0.1, 0.3, 1.0)


def pairs(o) -> tuple:
    """(cholinergic LN, uPN, synapse count) for every LN-to-PN pair MaleCNS connects."""
    b = o.brain
    nt = np.asarray(consensus_transmitters())
    cho = np.array([bool(p14.LN.match(t)) for t in o.types]) & (nt == "acetylcholine")
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(cho[pre] & o.m["upn"][b.idx])
    return pre[e], b.idx[e], np.asarray(b._counts[e], np.float64)


def set_gap(b, ln, pn, counts, kick: float) -> None:
    """Electrical synapses both ways, kick x count / median count mV per spike (csc: rows postsynaptic)."""
    mv = kick * counts / np.median(counts)
    rows, cols = np.concatenate([pn, ln]), np.concatenate([ln, pn])
    G = sparse.csc_matrix((np.concatenate([mv, mv]).astype(np.float32), (rows, cols)), shape=(b.n, b.n))
    G.sum_duplicates()
    b.gptr, b.gidx, b.gap_mv = G.indptr, G.indices, G.data.astype(np.float32)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe41_kw08_kept", p41.builder(p36.KW08_CHARGE, True), p40.prepare)
    b = o.brain
    ln, pn, counts = pairs(o)
    out = {"question": __doc__, "pairs": int(len(counts)), "lns": int(len(np.unique(ln))), "pns": int(len(np.unique(pn))),
           "median_count": float(np.median(counts)), "count_quartiles": [float(x) for x in np.percentile(counts, [25, 75])],
           "conditions": {}}
    print(json.dumps({k: out[k] for k in ("pairs", "lns", "pns", "median_count", "count_quartiles")}), flush=True)
    for kick in KICKS_MV:
        set_gap(b, ln, pn, counts, kick)
        entry = {"kick_mv": kick, "ln_response": p40.ln_measure(o, rec, BASE)}
        lr = entry["ln_response"]
        print(f"k {kick} LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
              "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]), flush=True)
        entry.update(p36.measure(o, rec, built, BASE))
        out["conditions"][f"{kick:g}"] = entry
        t = entry["transform"]
        print(f"k {kick} done ({time.perf_counter() - t0:.0f} s): sigma", json.dumps({g: t[g]["fit"]["sigma"] if t[g]["fit"] else None for g in t}),
              "Turner", json.dumps({od[:6]: r["pn_share_turner"] for od, r in entry["odors"].items()}),
              "KC", json.dumps({od[:6]: r["kc_share"] for od, r in entry["odors"].items()}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
