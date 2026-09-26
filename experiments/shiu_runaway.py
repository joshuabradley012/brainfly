"""Post hoc, not pre-registered: where does the Shiu-recipe runaway on MaleCNS live, and what stops it?

shiu_baseline.py failed STABLE: at w_syn = 0.275 mV a 1 s sugar drive ignites ~7,400 undriven neurons
above 100 Hz, and the activity outlasts the drive. This asks, after the fact:
  where    which superclasses and cell types are hot during the drive and still firing after it
  onset    the network's spike rate in 10 ms bins (how fast it ignites)
  variants the shiu_baseline.py tests (10 trials) with one change each:
           no synapses onto sensory neurons (the research report's rung-1 recipe);
           brain only (nerve cord removed); both;
           monoamine synapses removed (dopamine, octopamine, serotonin as fast excitation: rung 2);
           Kenyon-cell-to-Kenyon-cell synapses removed
  window   for each w_syn, does 100 Hz sugar reach MN9 L, and does the network stay stable? (5 trials)

    python experiments/shiu_runaway.py            (writes experiments/shiu_runaway.json)
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import numpy as np
import pyarrow.feather as feather
from scipy import sparse

from brainfly.data import DATA
from brainfly.shiu import ShiuBrain, counts
from shiu_baseline import SETS, tests

W = 0.275
OUT = Path(__file__).with_name("shiu_runaway.json")
KEEP = ("SUGAR", "WATER", "BITTER", "IR94E", "STABLE", "mn9_L_hz", "bitter_drop", "t_bitter", "ir94e_drop", "t_ir94e",
        "t_water", "tail_fraction", "undriven_over_100hz", "network_hz_during_sugar", "activated_by_sugar")


def main() -> None:
    C = counts().tocsr()
    base = ShiuBrain(w_syn=W, trials=5)
    sc = base.superclass.astype(str)
    cells = {k: base.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([base.cells(["MN9"], side="L"), base.cells(["MN9"], side="R")])

    r = base.run(1.0, drive=[(cells["sugar"], 100.0)], tail=0.5, seed=1)
    hot = r.rates > 100
    alive = r.after_rates.mean(0) > 1
    results = {"criteria": __doc__, "where": {
        "hot_by_superclass": {k: int(v) for k, v in collections.Counter(sc[hot]).most_common(10)},
        "hot_top_types": {k: int(v) for k, v in collections.Counter(base.mcns_type[hot]).most_common(12)},
        "firing_after_drive": int(alive.sum()),
        "after_by_superclass": {k: int(v) for k, v in collections.Counter(sc[alive]).most_common(10)},
        "network_hz_10ms_bins": np.round(r.timeline.mean(0)[:30]).astype(int).tolist()}}
    print(json.dumps(results["where"]), flush=True)

    ids = np.load(DATA / "brain.npz")["ids"]
    nt = feather.read_table(DATA / "raw" / "body-neurotransmitters-male-cns-v1.0.feather",
                            columns=["body", "consensus_nt", "predicted_nt"]).to_pandas().drop_duplicates("body").set_index("body").reindex(ids)
    monoamines = ["dopamine", "octopamine", "serotonin"]
    amine = (nt.consensus_nt.fillna("").isin(monoamines) | nt.predicted_nt.fillna("").isin(monoamines)).to_numpy()
    kc = np.char.startswith(base.mcns_type.astype(str), "KC")
    sensory = np.char.find(sc, "sensory") >= 0
    vnc = np.char.startswith(sc, "vnc_")
    keep = lambda mask: sparse.diags((~mask).astype(np.float32))
    coo = C.tocoo()
    kckc = kc[coo.row] & kc[coo.col]
    variants = {
        "no input to sensory neurons": keep(sensory) @ C,
        "brain only (no nerve cord)": keep(vnc) @ C @ keep(vnc),
        "both": keep(sensory) @ keep(vnc) @ C @ keep(vnc),
        "monoamine synapses removed": C @ keep(amine),
        "KC-to-KC synapses removed": sparse.csr_matrix((np.where(kckc, 0, coo.data), (coo.row, coo.col)), shape=C.shape),
    }
    results["counts"] = {"monoaminergic_neurons": int(amine.sum()), "kenyon_cells": int(kc.sum())}
    results["variants"] = {}
    for name, M in variants.items():
        t = tests(ShiuBrain(w_syn=W, trials=10, matrix=M), cells, mn9)
        results["variants"][name] = {k: t[k] for k in KEEP}
        print(f"{name}: {json.dumps(results['variants'][name])}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))

    results["window"] = []
    driven = np.zeros(base.n, bool)
    driven[cells["sugar"]] = True
    for w in (0.275, 0.25, 0.22, 0.2, 0.18, 0.15):
        base.w_syn = w
        r = base.run(1.0, drive=[(cells["sugar"], 100.0)], tail=0.5, seed=1)
        during = r.timeline[:, : int(round(1.0 / r.bin))].mean()
        last = r.timeline[:, -int(round(0.25 / r.bin)):].mean()
        row = {"w_syn": w, "mn9_L_hz": round(float(r.rates[mn9[0]]), 2),
               "undriven_over_100hz": int((r.rates[~driven] > 100).sum()), "active_neurons": int((r.rates > 0).sum()),
               "tail_fraction": round(float(last / during), 4) if during > 0 else 0.0}
        results["window"].append(row)
        print(f"window: {json.dumps(row)}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
