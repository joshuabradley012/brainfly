"""Exploratory, not pre-registered: which neurons' fast transmitters conflict with their hemilineage's?

The report's rung 2 adds an audit of transmitter conflicts by hemilineage. Neurons born from one hemilineage
use one fast transmitter (acetylcholine, GABA or glutamate), a rule found across the nerve cord's
hemilineages (Lacin et al. 2019, eLife 8:e43701) and used to check transmitter predictions (Eckstein et al.
2024). MaleCNS gives each neuron a consensus transmitter (brainfly's sign rule reads it) and many a
hemilineage (itoleeHl in the brain, trumanHl in the nerve cord). Here, for every hemilineage with at least 10
neurons whose consensus is a fast transmitter: its majority transmitter and the share holding it. Then the neurons
that disagree with a clear majority (at least 90%). A disagreement flips the sign when it pits acetylcholine
against GABA or glutamate, and changes nothing in brainfly's model between GABA and glutamate, which are both
inhibitory there. Counted by kind, by superclass, and among rung 1's taste route (the neurons sugar at 100 Hz
raises by more than 5 Hz in its silent brain).

    python experiments/hemilineage_audit.py            (writes experiments/hemilineage_audit.json)
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
import pyarrow.feather as feather

from brainfly.data import DATA
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
FAST = ("acetylcholine", "gaba", "glutamate")
MIN_NEURONS, CLEAR = 10, 0.9


def hemilineages() -> np.ndarray:
    """Each neuron's hemilineage in brain.npz order: itoleeHl, else trumanHl, else ""."""
    ids = np.load(DATA / "brain.npz")["ids"]
    ann = feather.read_table(DATA / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "itoleeHl", "trumanHl"]).to_pandas().drop_duplicates("bodyId").set_index("bodyId")
    ann = ann.reindex(ids)
    hl = ann["itoleeHl"].fillna("").astype(str).where(ann["itoleeHl"].notna(), ann["trumanHl"].fillna("").astype(str))
    return hl.to_numpy().astype(str)


def audit() -> dict:
    nt = consensus_transmitters()
    hl = hemilineages()
    meta = np.load(DATA / "brain.npz")
    superclass = meta["superclass"].astype(str)
    fast = np.isin(nt, FAST) & (hl != "")
    table, conflicts = {}, np.zeros(len(nt), bool)
    majority_of = np.full(len(nt), "", dtype=object)
    for h in np.unique(hl[fast]):
        members = fast & (hl == h)
        if members.sum() < MIN_NEURONS:
            continue
        c = Counter(nt[members])
        top, n_top = c.most_common(1)[0]
        share = n_top / members.sum()
        table[h] = {"neurons": int(members.sum()), "majority": top, "share": round(share, 3), "counts": dict(c)}
        if share >= CLEAR:
            bad = members & (nt != top)
            conflicts |= bad
            majority_of[bad] = top
    kinds = Counter(f"{nt[i]} in a {majority_of[i]} hemilineage" for i in np.flatnonzero(conflicts))
    sign_flip = conflicts & ((nt == "acetylcholine") != (majority_of == "acetylcholine"))
    return {"nt": nt, "hl": hl, "conflicts": conflicts, "sign_flip": sign_flip, "majority_of": majority_of,
            "table": table, "kinds": kinds, "superclass": superclass}


def main() -> None:
    a = audit()
    fast = np.isin(a["nt"], FAST)
    out = {"question": __doc__,
           "neurons_with_fast_consensus": int(fast.sum()),
           "with_hemilineage": int((fast & (a["hl"] != "")).sum()),
           "hemilineages_scored": len(a["table"]),
           "clear_hemilineages": int(sum(v["share"] >= CLEAR for v in a["table"].values())),
           "mixed_hemilineages": {h: v for h, v in a["table"].items() if v["share"] < 0.75},
           "conflicts": int(a["conflicts"].sum()), "sign_flips": int(a["sign_flip"].sum()),
           "conflict_kinds": dict(a["kinds"].most_common()),
           "sign_flips_by_superclass": dict(Counter(a["superclass"][a["sign_flip"]]).most_common())}
    try:
        from brainfly.hybrid import HybridBrain
        import rest_calibration as attempt1
        from shiu_baseline import SETS
        from shiu_rewiring import W_SYN
        M, scale, labels, types, superclass = attempt1.network()
        b = HybridBrain(trials=8, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=1)
        route = b.run(1.0, drive=[(b.cells(SETS["sugar"], "L"), 100.0)], seed=3).rates > 5
        out["on_rung1_sugar_route"] = {"route_neurons": int(route.sum()), "conflicts": int((a["conflicts"] & route).sum()),
                                       "sign_flips": int((a["sign_flip"] & route).sum()),
                                       "sign_flip_types": sorted(set(types[a["sign_flip"] & route]))}
    except Exception as e:                                   # the audit stands without the route
        out["on_rung1_sugar_route"] = f"not computed: {e}"
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "mixed_hemilineages")}, indent=1), flush=True)
    OUT.write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
