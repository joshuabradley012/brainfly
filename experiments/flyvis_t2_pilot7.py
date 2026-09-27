"""Exploratory, not pre-registered: can T2 gain a response to darkening while every other cell of flyvis model 000
keeps its flash responses?

rung3_t2_local.py (pre-registered, failed) changed only T2's own parameters and inputs in 000. T2 answered darkening
and LC4 began to answer looms, but T5a and T5b flipped polarity and LPLC2 lost its looming response: T2's new
activity spread through its outputs (onto Lawf2, which feeds back to the lamina, Mi1, Tm5c, TmY15, TmY5a), and a
diagnostic found the loom's drive onto LPLC2 through T5 gone and through T4 reversed. Here T2's outputs within
flyvis are freed too, and the penalty adds a term keeping every other type's central cell as 000 had it:
    pilot 5's T2 penalty + d * mean over types other than T2 of ((response - 000's response) / (s + 0.1))^2
with the responses each type's central cell's change through the 0.5 s after a full-field light and dark flash from
grey (dt 0.01), and s the spread of 000's response of that type. d = 100 and 1000, weight 1000, learning rate 1e-4,
500 iterations, seed 0; free: T2's resting potential and time constant, the synapses onto T2 except its own, the
synapses from T2, and the flow decoder. Keeping other cells' flash responses keeps their polarity nearly by
construction, so a rung 3 test built on this would check polarity as preservation, not prediction. Recorded: T2's
flash responses, the other types' largest deviation, the flow loss, flyvis's validation error, and none of rung 3's
tests.
Ran: neither setting worked in 500 iterations. T2 didn't meet the screen's criterion (its OFF peak ended at -0.74
with d = 100 and 0.07 against an ON peak of 2.78 with d = 1000), the fit swung back and forth, and the other types
drifted anyway: TmY5a, which T2 drives directly, ended 9 and 6 of its own spreads from 000's responses. flyvis's
validation error was 5.80.

    python experiments/flyvis_t2_pilot7.py            (writes experiments/flyvis_t2_pilot7.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt
from flyvis_t2_pilot2 import t2 as t2_measures
from flyvis_t2_pilot5 import ITERS, LR, START
from flyvis_t2_pilot5 import penalty as t2_penalty

OUT = Path(__file__).with_suffix(".json")
DISTILL = [100.0, 1000.0]


def masks(net) -> dict:
    """T2's own parameters, the synapses onto T2 except its own, and the synapses from T2."""
    m = vt.local(net, "T2")
    keys = net.edge_params["syn_strength"].keys
    m["edges_syn_strength"] |= torch.tensor([s == "T2" for s, _ in keys])
    m["edges_syn_strength"][keys.index(("T2", "T2"))] = False
    return m


def main() -> None:
    out = {"question": __doc__, "runs": []}
    task = None
    for d in DISTILL:
        view, net, dec = vt.load(START)
        task = task or vt.sintel(view)
        types = list(net.node_params["bias"].keys)
        others = torch.tensor([t != "T2" for t in types], device=vt.DEVICE)
        with torch.no_grad():
            ref = vt.central_flash_responses(net).detach()
        scale = ref.std(dim=(0, 1)) + 0.1

        def deviation(n) -> torch.Tensor:
            return (((vt.central_flash_responses(n) - ref) / scale) ** 2).mean(dim=(0, 1))[others]

        def penalty(n) -> torch.Tensor:
            return t2_penalty(n) + d * deviation(n).mean()

        start = {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}
        trace = []

        def log(row):
            with torch.no_grad():
                dev = deviation(net)
            worst = int(dev.argmax())
            trace.append({**row, **t2_measures(net), "deviation_mean": round(float(dev.mean()), 4),
                          "deviation_max": round(float(dev.max()), 4), "worst_type": [t for t in types if t != "T2"][worst]})
            print(json.dumps({"distill": d, **trace[-1]}), flush=True)

        t0 = time.perf_counter()
        vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, every=50, log=log, masks=masks(net), train_decoder=True)
        out["runs"].append({"distill": d, "start_measures": start, "trace": trace,
                            "end": {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
                            "seconds_per_iteration": round((time.perf_counter() - t0) / ITERS, 3)})
        print("end", d, json.dumps(out["runs"][-1]["end"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
