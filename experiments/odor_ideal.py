"""Exploratory analysis, no simulation: how much odor overlap would an ideal Kenyon cell layer show, given the
projection neurons' (PNs') responses?

Each Kenyon cell's input is its PN synapse counts (MaleCNS, excitatory) times the PN responses of their glomeruli,
divided by its summed PN synapse count (so every cell is equally excitable per unit of input), and for each odor the
cells with the most input respond, as many as odor_probe14.py's corrected model has respond (3-octanol 12.6%,
4-methylcyclohexanol 3.7%, ethyl acetate 12.9%, isopentyl acetate 13.8%, benzaldehyde 11.4%, 2-heptanone 16.2%). The
PN responses are odor_probe12.py's saved glomerular patterns: the PNs' rise over an odor's first 100 ms, over its 0.5 s,
or DoOR's receptor responses themselves (as if PNs passed their receptors' pattern through unchanged).

    python experiments/odor_ideal.py           (writes experiments/odor_ideal.json)
"""
from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path

import numpy as np

from brainfly.shiu import counts, mcns_types

OUT = Path(__file__).with_suffix(".json")
SHARES = {"3-octanol": 0.126, "4-methylcyclohexanol": 0.037, "ethyl acetate": 0.129, "isopentyl acetate": 0.138,
          "benzaldehyde": 0.114, "2-heptanone": 0.162}


def main() -> None:
    p12 = json.loads((OUT.parent / "odor_probe12.json").read_text())
    gl = {g: i for i, g in enumerate(p12["glomeruli"])}
    C = counts().tocsr()
    types = mcns_types().astype(str)
    kc = np.flatnonzero(np.char.startswith(types, "KC"))
    upn = np.flatnonzero([bool(re.search(r"_[a-z]*PN$", t)) for t in types])
    K = C[kc][:, upn].tocsr()
    K.data = np.maximum(K.data, 0)
    total = np.asarray(K.sum(1)).ravel()
    pn_glom = [t.split("_")[0] for t in types[upn]]
    out = {"question": __doc__, "sources": {}}
    for source in ("pn_early", "pn", "door"):
        responding = {}
        for odor, share in SHARES.items():
            pattern = np.array(p12["odors"][odor]["patterns"][source])
            act = np.array([max(pattern[gl[g]], 0.0) if g in gl else 0.0 for g in pn_glom])
            drive = (K @ act) / np.maximum(total, 1e-9)
            responding[odor] = drive >= np.quantile(drive, 1 - share)
        a, b = responding["3-octanol"], responding["4-methylcyclohexanol"]
        js = [float((responding[x] & responding[y]).sum() / (responding[x] | responding[y]).sum()) for x, y in combinations(SHARES, 2)]
        out["sources"][source] = {"oct_mch_jaccard": round(float((a & b).sum() / (a | b).sum()), 3),
                                  "mch_responders_answering_oct": round(float((a & b).sum() / b.sum()), 3),
                                  "mean_jaccard": round(float(np.mean(js)), 3)}
        print(source, json.dumps(out["sources"][source]))
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
