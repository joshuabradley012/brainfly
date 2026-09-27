"""Exploratory, not pre-registered: does the nerve cord rhythm survive when brainfly builds Pugliese et al.'s network
from its own copy of MaleCNS?

vnc_rhythm.py reran Pugliese et al.'s male CNS model on their own network files and reproduced their result:
DNg100 drives 12-13 Hz leg rhythms, and a rewired network doesn't. This builds the same 4,310 neurons' network from
brainfly's data instead (brainfly.shiu.counts, from MaleCNS v1.0 at confidence 0.5, signed by brainfly's consensus
transmitters: acetylcholine excitatory, GABA and glutamate inhibitory, others left out; connections under 5 synapses
dropped). It differs from theirs in counting every synapse between two of these neurons, brain-side ones
included, where theirs keeps the nerve cord's only; one untyped sensory neuron of theirs isn't in brainfly's
MaleCNS and gets no synapses. It reports how the two networks compare, then runs
vnc_rhythm.py's model, score and 16 replicates with DNg100 on each side driven at 400, with two sizes:
  volume    their neuron volumes, as in vnc_rhythm.py
  synapses  brainfly's size proxy (each neuron's synapses in and out, over the median; shiu_scaled.sizes), which the
            rest of brainfly uses and which needs no volumes, so it extends to neurons their table lacks
Ran: brainfly's network keeps 118,680 of their 118,920 connections (99.8%), all with the same sign, counts
correlating at 0.96; counting brain-side synapses adds 23,256 more. With their volumes DNg100 gives rhythms in 16 of
16 replicates on each side (13.4 and 11.6 Hz). With the synapse proxy (ranked like the volumes, Spearman 0.93) there
is no rhythm (0 of 16), and hardly any motor neuron is active: size scaling needs the volumes.

    python experiments/vnc_own.py            (writes experiments/vnc_own.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

import vnc_rhythm as v
from brainfly.data import DATA
from brainfly.hybrid import consensus_transmitters
from brainfly.shiu import counts
from shiu_scaled import sizes

OUT = Path(__file__).with_suffix(".json")
MIN_SYNAPSES = 5


def own_network(table: pd.DataFrame) -> tuple[sparse.csr_matrix, np.ndarray]:
    """brainfly's signed counts among the table's neurons (rows postsynaptic), and its size proxy for them."""
    ids = np.load(DATA / "brain.npz")["ids"]
    where = pd.Series(np.arange(len(ids)), index=ids)
    found = where.reindex(table["bodyId"].to_numpy()).to_numpy(float)
    have = ~np.isnan(found)                           # all but one untyped sensory neuron, which gets no synapses
    idx = found[have].astype(int)
    C = counts().tocsr()
    nt = consensus_transmitters()
    sign = np.where(nt == "acetylcholine", 1.0, np.where(np.isin(nt, ["gaba", "glutamate"]), -1.0, 0.0))
    raw = abs(C[idx][:, idx])                                         # counts() is signed; keep the counts
    raw.data[raw.data < MIN_SYNAPSES] = 0.0
    raw.eliminate_zeros()
    sub = (raw @ sparse.diags(sign[idx])).tocoo()
    pos = np.flatnonzero(have)
    W = sparse.csr_matrix((sub.data, (pos[sub.row], pos[sub.col])), shape=(len(table), len(table)))
    W.eliminate_zeros()
    size = np.ones(len(table))
    size[have] = sizes(C)[idx]
    return W, size


def main() -> None:
    table, theirs = v.network()
    ours, proxy = own_network(table)
    a, b = theirs.toarray(), ours.toarray()
    both = (a != 0) & (b != 0)
    out = {"question": __doc__, "compare": {
        "their_connections": int((a != 0).sum()), "our_connections": int((b != 0).sum()), "shared": int(both.sum()),
        "same_sign_of_shared": round(float((np.sign(a[both]) == np.sign(b[both])).mean()), 4),
        "count_correlation_of_shared": round(float(np.corrcoef(np.abs(a[both]), np.abs(b[both]))[0, 1]), 4),
        "size_proxy_vs_volume_spearman": round(float(pd.Series(proxy).rank().corr(table["size"].rank())), 3)}}
    print(json.dumps(out["compare"]), flush=True)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    volume = table["size"].to_numpy(float)
    for label, size in (("volume", volume), ("synapses", proxy * np.nanmedian(volume))):
        t = table.copy()
        t["size"] = size
        for k, j in enumerate(np.flatnonzero(types == "DNg100")):
            name = f"{inst[j]}, {label}"
            out[name] = r = v.run(ours, t, [j], np.random.default_rng(400 + 10 * k + (label == "synapses")))
            print(name, json.dumps({x: r[x] for x in r if x != "replicates"}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
