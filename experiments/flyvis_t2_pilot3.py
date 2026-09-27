"""Exploratory, not pre-registered: does fine-tuning flyvis's model 006 give it a T2 that answers light decrements,
and at what cost to its flow task?

flyvis_t2_pilot.py and flyvis_t2_pilot2.py fine-tuned flow/0000/000, whose T2 falls when the field darkens. In
both, T2's ON response shrank and its OFF response didn't rise: in 000 the dark flash removes T2's drive from
ON cells (Mi1, Tm3) and its OFF input (Tm2) rests below threshold, so no small change turns the fall into a
rise. flyvis_screen.py lists model 006 (seventh of 50 by validation loss) as the only one of flyvis's 50 with all
32 known contrast polarities right, and its T2 already rises to the dark flash, by 0.95 against 4.94 to the
light one. The screen's T2 criterion needs the smaller at least a third of the larger. So 006 is the natural
start: the fix is smaller, and T2's OFF peak comes while the network is responding, where it has a gradient.
Two penalties, each for 500 iterations from 006 at weight 1000 and learning rate 5e-6 (seed 0):
  symmetric   relu(0.5 * max(on, off) - min(on, off)) + relu(0.1 - on) + relu(0.1 - off)   (flyvis_t2_pilot.py's)
  raise only  relu(0.5 * [on] - off) + relu(0.5 * [off] - on) + relu(0.1 - on) + relu(0.1 - off), [x] held
              fixed in the gradient, so each response can only be pushed up towards half the other, not down
with on and off the central T2's peaks in the 0.5 s after a full-field (radius 6) flash from grey (dt 0.01).
Recorded, as in the earlier pilots: T2's flash peaks (as the screen measures them), the flow loss, flyvis's
validation error and the time per iteration, and none of rung 3's tests, which stay held out for the model
this chooses.
Ran: with the symmetric penalty T2 met the screen's criterion by iteration 50 and the penalty was 0 from
iteration 150. After 500 iterations T2 rose by 4.64 to light and 3.98 to dark (from 5.18 and 1.19 by this
measure), and flyvis's validation error was 5.50 (from 5.27). With "raise only", T2's responses grew to 25.9 and
37.5 and the validation error to 5.81, so the symmetric penalty is the one rung3_t2.py uses.

    python experiments/flyvis_t2_pilot3.py            (writes experiments/flyvis_t2_pilot3.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch

from brainfly import vistrain as vt

OUT = Path(__file__).with_suffix(".json")
START = "flow/0000/006"
SETTINGS = [{"penalty": "symmetric", "weight": 1000.0, "lr": 5e-6, "iters": 500},
            {"penalty": "raise only", "weight": 1000.0, "lr": 5e-6, "iters": 500}]


def t2_penalty(net, kind: str, weight: float) -> torch.Tensor:
    on, off = vt.flash_peaks(net, "T2")
    floors = torch.relu(0.1 - on) + torch.relu(0.1 - off)
    if kind == "symmetric":
        return weight * (torch.relu(0.5 * torch.maximum(on, off) - torch.minimum(on, off)) + floors)
    return weight * (torch.relu(0.5 * on.detach() - off) + torch.relu(0.5 * off.detach() - on) + floors)


def t2(net) -> dict:
    with torch.no_grad():
        on, off = vt.flash_peaks(net, "T2", dt=0.005, t_pre=1.0, t_flash=1.0).tolist()
    return {"t2_on": round(on, 3), "t2_off": round(off, 3),
            "T2": bool(on > 0.02 and off > 0.02 and min(on, off) / max(on, off) >= 1 / 3)}


def main() -> None:
    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    out = {"question": __doc__, "start": {**t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}, "runs": []}
    print(json.dumps(out["start"]), flush=True)
    for s in SETTINGS:
        view, net, dec = vt.load(START)
        trace = []

        def log(row):
            trace.append({**row, **t2(net)})
            print(json.dumps({**s, **trace[-1]}), flush=True)

        t0 = time.perf_counter()
        vt.fine_tune(net, dec, task, lambda n: t2_penalty(n, s["penalty"], s["weight"]), s["iters"], lr=s["lr"], every=50, log=log)
        seconds = time.perf_counter() - t0
        out["runs"].append({**s, "trace": trace, "end": {**t2(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)},
                            "seconds_per_iteration": round(seconds / s["iters"], 3)})
        print(json.dumps({**s, **out["runs"][-1]["end"], "s_per_iter": out["runs"][-1]["seconds_per_iteration"]}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
