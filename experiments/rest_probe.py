"""Exploratory, not pre-registered: can background activity alone give the rung-1 brain a resting state?

The vision probes (optomotor_hybrid.py, optomotor_hybrid2.py) found that a brain silent at rest, as
Shiu's is, has no gain at which a visual signal reaches DNa02 without igniting recurrent circuits.
FlyBrain, whose neurons idle near threshold, does. A realistic brain idles at a low mean rate (the
research report's energy budget: 4 Hz or less). This asks what uniform background does to rung 1's
network (shiu_sensory.py's, w_syn = 1.5556 mV), with no stimulus: every neuron gets Poisson kicks of
k mV at r Hz (HybridBrain's noise_rate and noise_kick), for 3 s.
  grid     k in {0.5, 1, 2} mV x r in {50, 200, 800} Hz: mean rate in the first and third second,
           the share of silent neurons, and the neurons over 100 Hz by superclass
  where    at the lowest background that wakes the network (1 mV x 200 Hz): the types over 100 Hz,
           and the rates of the circuits that ran away before (Kenyon cells, APL, MBONs, the
           central complex)

    python experiments/rest_probe.py            (writes experiments/rest_probe.json)
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import numpy as np

from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

OUT = Path(__file__).with_name("rest_probe.json")


def main() -> None:
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    scale = 1.0 / sizes(C)
    sc, ty = meta["superclass"].astype(str), types.astype(str)
    make = lambda k, r: HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels,
                                    types={"all": {"noise_rate": r, "noise_kick": k}})
    out = {"question": __doc__, "grid": []}
    for k in (0.5, 1.0, 2.0):
        for r in (50.0, 200.0, 800.0):
            brain = make(k, r)
            seconds = [brain.advance(10000)[0] for _ in range(3)]
            last = seconds[2]
            hot = last > 100
            row = {"kick_mv": k, "rate_hz": r, "mean_drive_mv": round(k * r * 0.02, 2),
                   "mean_hz_first_second": round(float(seconds[0].mean()), 2), "mean_hz_third_second": round(float(last.mean()), 2),
                   "silent": round(float((last == 0).mean()), 3), "over_100hz": int(hot.sum()),
                   "over_100hz_by_superclass": dict(collections.Counter(sc[hot]).most_common(5))}
            out["grid"].append(row)
            print(row, flush=True)
    brain = make(1.0, 200.0)
    brain.advance(10000)
    rate = brain.advance(20000)[0] / 2.0
    hot = rate > 100
    groups = {"Kenyon cells": np.char.startswith(ty, "KC"), "APL": ty == "APL", "MBONs": np.char.startswith(ty, "MBON"),
              "PAM dopamine neurons": np.char.startswith(ty, "PAM"), "PFN (central complex)": np.char.startswith(ty, "PFN"),
              "EPG": ty == "EPG", "Delta7": ty == "Delta7", "TuBu": np.char.startswith(ty, "TuBu"),
              "descending neurons": sc == "descending_neuron"}
    out["where"] = {"background": "1 mV x 200 Hz", "types_over_100hz": collections.Counter(ty[hot]).most_common(25),
                    "groups": {name: {"n": int(g.sum()), "mean_hz": round(float(rate[g].mean()), 1),
                                      "over_100hz": int((rate[g] > 100).sum()), "silent": round(float((rate[g] == 0).mean()), 3)}
                               for name, g in groups.items()},
                    "median_hz_of_active": round(float(np.median(rate[rate > 0])), 2),
                    "share_of_spikes_from_over_100hz": round(float(rate[hot].sum() / rate.sum()), 3)}
    print(json.dumps(out["where"]["groups"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
