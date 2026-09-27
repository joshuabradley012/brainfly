"""Exploratory, not pre-registered: can a fine-tune that changes only T2 give it a response to light decrements?

rung3_t2.py (pre-registered) fine-tuned all of flyvis model 006's parameters with a penalty on T2's flash
responses. T2 then answered both flashes and 31 of 32 polarities stayed right, but only 6 of the 16 T4/T5
subtypes kept their preferred direction: the fine-tune reached far beyond T2. Here only T2's own parameters (its
resting potential and time constant) and the strengths of the synapses onto T2 may change
(brainfly.vistrain.local), and the flow decoder is frozen. The rest of the network changes only through T2's
outputs (onto Lawf2, Mi1, T2, Tm5c, TmY15 and TmY5a in flyvis's connectome). With 26 free parameters the learning
rate can be higher than flyvis's 5e-6. The start is 000, flyvis's best model by validation error, whose T4/T5
all prefer their right direction on the male eye (flyvis_native.py) and which gets 30 of 32 polarities; its T2
falls when the field darkens. (006 was dropped: its own direction selectivity, reported by rung3_t2.py, is 12 of
16.) Penalties:
  peak   flyvis_t2_pilot3.py's symmetric penalty on the peaks
  mean   flyvis_t2_pilot2.py's, which asks for T2's mean change over the dark flash's first 0.25 s to be at
         least 1 (its peak carries no gradient while the response is negative throughout)
each at weight 1000 for 500 iterations, learning rate 1e-4, seed 0. As in the other pilots this records T2's
flash responses, the flow loss, flyvis's validation error and the time per iteration, and none of rung 3's
tests.
Ran: with the mean penalty, T2's mean OFF response rose from -2.16 to -0.64 by iteration 150 (its ON peak fell
from 2.90 to 1.67). Then T2 ran away: ON peaks of 31 at iteration 200 and 455 at 250, OFF close behind. The fit had
strengthened T2's synapse onto itself (free, as an input to T2) until the loop amplified any change. The run was
stopped at iteration 350 and the peak setting cancelled; flyvis_t2_pilot5.py freezes that synapse and caps T2's
responses.

    python experiments/flyvis_t2_pilot4.py            (writes experiments/flyvis_t2_pilot4.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt
from flyvis_t2_pilot2 import t2 as t2_measures, t2_penalty as mean_penalty
from flyvis_t2_pilot3 import t2_penalty as peak_penalty

OUT = Path(__file__).with_suffix(".json")
SETTINGS = [{"start": "flow/0000/000", "penalty": "mean"}, {"start": "flow/0000/000", "penalty": "peak"}]
WEIGHT, LR, ITERS = 1000.0, 1e-4, 500


def penalty(kind: str):
    return (lambda n: peak_penalty(n, "symmetric", WEIGHT)) if kind == "peak" else (lambda n: mean_penalty(n, WEIGHT))


def main() -> None:
    out = {"question": __doc__, "runs": []}
    task = None
    for s in SETTINGS:
        view, net, dec = vt.load(s["start"])
        task = task or vt.sintel(view)
        start = {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}
        trace = []

        def log(row):
            trace.append({**row, **t2_measures(net)})
            print(json.dumps({**s, **trace[-1]}), flush=True)

        t0 = time.perf_counter()
        vt.fine_tune(net, dec, task, penalty(s["penalty"]), ITERS, lr=LR, every=50, log=log,
                     masks=vt.local(net, "T2"), train_decoder=False)
        seconds = time.perf_counter() - t0
        out["runs"].append({**s, "weight": WEIGHT, "lr": LR, "iters": ITERS, "start_measures": start, "trace": trace,
                            "end": {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
                            "seconds_per_iteration": round(seconds / ITERS, 3)})
        print(json.dumps({**s, "start": start, "end": out["runs"][-1]["end"]}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
