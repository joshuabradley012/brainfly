"""Exploratory, not pre-registered: can fine-tuning give flyvis's best model a T2 that answers light decrements,
if the penalty asks for T2's mean OFF response instead of its peak?

flyvis_t2_pilot.py penalized T2's flash peaks. While T2's OFF response is negative throughout (in flow/0000/000
it falls by about 2 in its own units), the OFF peak sits at the flash's onset, before the network responds. So that
term carried no gradient, and the fine-tune only lowered T2's ON response. Here the OFF term is the mean change
over the first 0.25 s of the dark flash, which has a gradient through every pathway that moves T2 then:
    w * [relu(1 - off_mean) + relu(0.5 * max(on, off) - min(on, off)) + relu(0.1 - on)]
with on and off the central T2's peaks in the 0.5 s after a full-field (radius 6) flash from grey (dt 0.01).
The penalty is 0 only when the dark flash raises T2 by at least 1 on average over its first 0.25 s and the
smaller peak is at least half the larger. As in the first pilot, this records T2's flash responses, the flow loss,
flyvis's validation error and the time per iteration, and none of rung 3's tests, which stay held out.
Settings, each from 000 (seed 0) at learning rate 5e-6: no penalty for 300 iterations (how much fine-tuning alone
moves the validation error), then weights 100 and 1000 for 1000 iterations.
Ran: without the penalty, 300 iterations moved flyvis's validation error from 5.135 to 5.142 and left T2 as it
was. At weight 100, T2's ON peak fell from 2.90 to 1.50 in 400 iterations while its mean OFF response stayed
near -2.0 (from -2.16), the first pilot's failure again. That run was stopped there and weight 1000 cancelled.

    python experiments/flyvis_t2_pilot2.py            (writes experiments/flyvis_t2_pilot2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt

OUT = Path(__file__).with_suffix(".json")
SETTINGS = [{"weight": 0.0, "lr": 5e-6, "iters": 300}, {"weight": 100.0, "lr": 5e-6, "iters": 1000},
            {"weight": 1000.0, "lr": 5e-6, "iters": 1000}]
DT, WINDOW = 0.01, 0.25


def t2_penalty(net, weight: float) -> torch.Tensor:
    r = vt.flash_responses(net, "T2", dt=DT)
    on, off = r.max(1).values
    off_mean = r[1, :int(round(WINDOW / DT))].mean()
    return weight * (torch.relu(1.0 - off_mean) + torch.relu(0.5 * torch.maximum(on, off) - torch.minimum(on, off))
                     + torch.relu(0.1 - on))


def t2(net) -> dict:
    with torch.no_grad():
        on, off = vt.flash_peaks(net, "T2", dt=0.005, t_pre=1.0, t_flash=1.0).tolist()
        off_mean = float(vt.flash_responses(net, "T2", dt=DT)[1, :int(round(WINDOW / DT))].mean())
    return {"t2_on": round(on, 3), "t2_off": round(off, 3), "t2_off_mean": round(off_mean, 3),
            "T2": bool(on > 0.02 and off > 0.02 and min(on, off) / max(on, off) >= 1 / 3)}


def main() -> None:
    view, net, dec = vt.load("flow/0000/000")
    task = vt.sintel(view)
    out = {"question": __doc__, "start": {**t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}, "runs": []}
    print(json.dumps(out["start"]), flush=True)
    for s in SETTINGS:
        view, net, dec = vt.load("flow/0000/000")
        trace = []

        def log(row):
            trace.append({**row, **t2(net)})
            print(json.dumps({**s, **trace[-1]}), flush=True)

        t0 = time.perf_counter()
        penalty = (lambda n: t2_penalty(n, s["weight"])) if s["weight"] else None
        vt.fine_tune(net, dec, task, penalty, s["iters"], lr=s["lr"], every=50, log=log)
        seconds = time.perf_counter() - t0
        out["runs"].append({**s, "trace": trace, "end": {**t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
                            "seconds_per_iteration": round(seconds / s["iters"], 3)})
        print(json.dumps({**s, **out["runs"][-1]["end"], "s_per_iter": out["runs"][-1]["seconds_per_iteration"]}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
