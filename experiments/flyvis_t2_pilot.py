"""Exploratory, not pre-registered: how strongly must a T2 constraint be weighted to fine-tune flyvis's best model,
and how fast does it train here?

flyvis_screen.py found no pretrained flyvis model with a T2 that answers light decrements (as a real T2 does;
Keles et al. 2020) that also gets 30 of the 32 known contrast polarities right. Its best model, flow/0000/000,
gets 30 but its T2 answers only increments. The plan is to fine-tune 000 on its own training task (Sintel flow,
brainfly.vistrain on Apple's GPU) plus a penalty on T2's flash responses, and then test the result on rung 3's
criteria, which the penalty doesn't touch: T2 is not among flyvis's 32 known polarities. This pilot only
chooses the penalty's weight and the learning rate. It records T2's flash peaks, the flow loss, flyvis's
validation error and the time per iteration. It measures none of rung 3's tests, so they stay held out.
Penalty: w * [relu(0.5 * max(on, off) - min(on, off)) + relu(0.1 - on) + relu(0.1 - off)], with on and off the
central T2's peak change in the 0.5 s after a full-field (radius 6) flash to light or dark from grey (dt 0.01).
The screen's T2 criterion, both above 0.02 and the smaller at least a third of the larger, measured at dt 0.005
over 1 s, holds with a margin once the penalty is 0. Each setting runs 300 iterations from 000 (seed 0).
Ran: weights 100 and 1000 at learning rate 5e-6 (the end of flyvis's schedule). Both lowered T2's ON peak
(2.90 to 2.46 and 2.25) while its OFF peak stayed at or below 0, and flyvis's validation error rose (5.13 to
5.34 and 5.64). The two remaining settings were cancelled: while T2's OFF response is negative throughout,
its peak is at the flash's onset, before the network responds, so the penalty's OFF term carries no gradient
and only lowering ON reduces it. flyvis_t2_pilot2.py penalizes the mean OFF response instead.

    python experiments/flyvis_t2_pilot.py            (writes experiments/flyvis_t2_pilot.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt

OUT = Path(__file__).with_suffix(".json")
SETTINGS = [{"weight": 100.0, "lr": 5e-6}, {"weight": 1000.0, "lr": 5e-6}]
ITERS = 300


def t2_penalty(net, weight: float) -> torch.Tensor:
    on, off = vt.flash_peaks(net, "T2")
    return weight * (torch.relu(0.5 * torch.maximum(on, off) - torch.minimum(on, off)) + torch.relu(0.1 - on) + torch.relu(0.1 - off))


def screen_t2(net) -> dict:
    with torch.no_grad():
        on, off = vt.flash_peaks(net, "T2", dt=0.005, t_pre=1.0, t_flash=1.0).tolist()
    return {"t2_on": round(on, 3), "t2_off": round(off, 3),
            "T2": bool(on > 0.02 and off > 0.02 and min(on, off) / max(on, off) >= 1 / 3)}


def main() -> None:
    view, net, dec = vt.load("flow/0000/000")
    task = vt.sintel(view)
    out = {"question": __doc__, "start": {**screen_t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}, "runs": []}
    print(json.dumps(out["start"]), flush=True)
    for s in SETTINGS:
        view, net, dec = vt.load("flow/0000/000")
        trace = []

        def log(row):
            trace.append({**row, **screen_t2(net)})
            print(json.dumps({**s, **trace[-1]}), flush=True)

        t0 = time.perf_counter()
        vt.fine_tune(net, dec, task, lambda n: t2_penalty(n, s["weight"]), ITERS, lr=s["lr"], every=50, log=log)
        seconds = time.perf_counter() - t0
        out["runs"].append({**s, "trace": trace, "end": {**screen_t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
                            "seconds_per_iteration": round(seconds / ITERS, 3)})
        print(json.dumps({**s, **out["runs"][-1]["end"], "s_per_iter": out["runs"][-1]["seconds_per_iteration"]}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
