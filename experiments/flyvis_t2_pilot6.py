"""Exploratory, not pre-registered: flyvis_t2_pilot5.py's fine-tune of model 000's T2, with the flow decoder trained.

flyvis_t2_pilot5.py gave model 000's T2 a response to darkening by fine-tuning only T2's own parameters and its
inputs (not its synapse onto itself), with a capped penalty on its flash responses. With the flow decoder frozen,
flyvis's validation error rose from 5.13 to 6.34: T2 is one of the decoder's 34 input types, so the frozen readout
misreads it, and the flow loss pulls T2 back against the penalty. The decoder only reads the network (it feeds
nothing back), so training it changes no cell's response. Everything else is pilot 5's: model 000, the same
parameters free, the same penalty, weight 1000, learning rate 1e-4, 500 iterations, seed 0. Recorded: T2's flash
responses, the flow loss, flyvis's validation error and the time per iteration, and none of rung 3's tests.
Ran: T2 met the screen's criterion from iteration 250 and stayed bounded; after 500 iterations it rises by 1.87 to
the light flash and 0.90 to the dark one (by this measure). flyvis's validation error was 5.70 (5.13 for 000, 6.34
with the decoder frozen): the new T2 still costs the flow task, less. rung3_t2_local.py uses this procedure.

    python experiments/flyvis_t2_pilot6.py            (writes experiments/flyvis_t2_pilot6.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from brainfly import vistrain as vt
from flyvis_t2_pilot2 import t2 as t2_measures
from flyvis_t2_pilot5 import ITERS, LR, START, masks, penalty

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    start = {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}
    trace = []

    def log(row):
        trace.append({**row, **t2_measures(net)})
        print(json.dumps(trace[-1]), flush=True)

    t0 = time.perf_counter()
    vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, every=50, log=log, masks=masks(net), train_decoder=True)
    out = {"question": __doc__, "start": START, "start_measures": start, "trace": trace,
           "end": {**t2_measures(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
           "seconds_per_iteration": round((time.perf_counter() - t0) / ITERS, 3)}
    OUT.write_text(json.dumps(out, indent=1))
    print("end:", json.dumps(out["end"]), flush=True)


if __name__ == "__main__":
    main()
