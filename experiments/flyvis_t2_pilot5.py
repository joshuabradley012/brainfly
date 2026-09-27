"""Exploratory, not pre-registered: can a fine-tune of T2's own parameters and its inputs, but not its synapse onto
itself, give flyvis model 000's T2 a response to light decrements without T2 running away?

flyvis_t2_pilot4.py freed T2's resting potential and time constant and the strengths of every synapse onto T2
(brainfly.vistrain.local) in model 000, with the flow decoder frozen. T2's mean OFF response rose from -2.16 to
-0.64 in 150 iterations, and then T2 ran away (flash peaks in the hundreds): among its inputs is its own synapse
onto itself, which the fit strengthened until the loop amplified everything. Here that synapse stays as flyvis
fitted it, and the penalty also caps T2's responses:
    w * [relu(1 - off_mean) + relu(0.5 * max(on, off) - min(on, off)) + relu(0.1 - on) + relu(on - 5) + relu(off - 5)]
with on and off the central T2's peaks in the 0.5 s after a full-field (radius 6) flash from grey and off_mean its
mean change over the dark flash's first 0.25 s (dt 0.01). 000's T2 peaks at 2.9 to the light flash, and model
001's, which answers darkening, at 2.8 to the dark one, so 5 bounds a T2 of the right size. Weight 1000, learning
rate 1e-4, 500 iterations, seed 0. As in the other pilots this records T2's flash responses, the flow loss,
flyvis's validation error and the time per iteration, and none of rung 3's tests.
Ran: T2 met the screen's criterion from iteration 250 and never ran away: after 500 iterations it rises by 1.90
to the light flash and 0.92 to the dark one (peaks at most 2.2 on the way). Its mean OFF response rose from -2.16
to -0.19, short of the penalty's 1. But flyvis's validation error rose to 6.34, worse than predicting no motion
(5.77). T2 is one of the frozen decoder's 34 input types, so its new response corrupts the flow readout, and the
flow loss then pulls T2 back against the penalty. flyvis_t2_pilot6.py trains the decoder too.

    python experiments/flyvis_t2_pilot5.py            (writes experiments/flyvis_t2_pilot5.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt
from flyvis_t2_pilot2 import DT, WINDOW, t2 as t2_measures

OUT = Path(__file__).with_suffix(".json")
START, WEIGHT, LR, ITERS, CAP = "flow/0000/000", 1000.0, 1e-4, 500, 5.0


def penalty(net) -> torch.Tensor:
    r = vt.flash_responses(net, "T2", dt=DT)
    on, off = r.max(1).values
    off_mean = r[1, :int(round(WINDOW / DT))].mean()
    return WEIGHT * (torch.relu(1.0 - off_mean) + torch.relu(0.5 * torch.maximum(on, off) - torch.minimum(on, off))
                     + torch.relu(0.1 - on) + torch.relu(on - CAP) + torch.relu(off - CAP))


def masks(net) -> dict:
    """T2's own parameters and the synapses onto it, but not T2's synapse onto itself."""
    m = vt.local(net, "T2")
    keys = net.edge_params["syn_strength"].keys
    m["edges_syn_strength"][keys.index(("T2", "T2"))] = False
    return m


def main() -> None:
    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    start = {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}
    trace = []

    def log(row):
        trace.append({**row, **t2_measures(net)})
        print(json.dumps(trace[-1]), flush=True)

    t0 = time.perf_counter()
    vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, every=50, log=log, masks=masks(net), train_decoder=False)
    out = {"question": __doc__, "start": START, "start_measures": start, "trace": trace,
           "end": {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
           "seconds_per_iteration": round((time.perf_counter() - t0) / ITERS, 3)}
    OUT.write_text(json.dumps(out, indent=1))
    print("end:", json.dumps(out["end"]), flush=True)


if __name__ == "__main__":
    main()
