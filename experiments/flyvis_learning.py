"""Exploratory, not pre-registered: why does flyvis's training from scratch never learn here?

flyvis_t2_scratch.py trained a flyvis network from scratch (with T2's response to darkening as a constraint) for
116,500 iterations, and a control without the constraint for 24,000. Neither's validation error moved from that of
predicting no flow (5.774). Without data augmentation (noaug) even the training loss stayed flat for 5,000 iterations.
flyvis's own pipeline check, training on one batch, does lower the loss. These checks ask which part learns.
Each: one fixed training batch, augmentation off, 600 iterations of Adam from flyvis_t2_scratch.py's fresh network (seed
9100), reporting the loss every 100 iterations and the loss of predicting no flow on that batch.
  a  network and decoder, learning rate 1e-5 (flyvis's tutorial)
  b  network and decoder, 5e-5 (flyvis's starting rate)
  c  as b, with flyvis's activity penalty stepping the resting potentials after every update, as the full loop does
  d  only the network, the decoder frozen at its initialisation (flyvis's: constant weights of 0.001)
  e  only the decoder, the network frozen
  f  only the network, read by flyvis's trained decoder from model 000, frozen

    python experiments/flyvis_learning.py a ... f      (each writes flyvis_learning/<variant>.json)
    python experiments/flyvis_learning.py summary      (writes experiments/flyvis_learning.json)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

from brainfly import vistrain as vt
import flyvis_t2_scratch as fs

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
VARIANTS = "abcdef"
ITERS = 600


def run(variant: str) -> None:
    HERE.mkdir(exist_ok=True)
    view, net, dec, task, opt, pen, sched = fs.build()
    if variant == "f":
        _, _, dec = vt.load("flow/0000/000", vt.DEVICE)
    if variant in "abc":
        params = [*net.parameters(), *[p for d in dec.values() for p in d.parameters()]]
    elif variant in "df":
        params = list(net.parameters())
    else:
        params = [p for d in dec.values() for p in d.parameters()]
    with vt.on(vt.DEVICE):
        adam = torch.optim.Adam(params, lr=1e-5 if variant == "a" else 5e-5)
    with task.dataset.augmentation(False):
        data = next(iter(task.train_data))
    dt = task.dataset.dt
    net.train()
    for d in dec.values():
        d.eval() if variant == "f" else d.train()
    losses = []
    with vt.on(vt.DEVICE):
        lum, flow = data["lum"].to(vt.DEVICE), data["flow"].to(vt.DEVICE)
        zero = float(task.loss(torch.zeros_like(flow), flow, "flow"))
        for k in range(ITERS):
            with torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=dt, batch_size=lum.shape[0], value=0.5)
            adam.zero_grad()
            net.stimulus.zero(*lum.shape[:2])
            net.stimulus.add_input(lum)
            act = net(net.stimulus(), dt, state=state)
            loss = task.loss(dec["flow"](act), flow, "flow")
            loss.backward(retain_graph=variant == "c")
            adam.step()
            if variant == "c":
                pen(activity=act, iteration=k)
            if k % 100 == 0 or k == ITERS - 1:
                losses.append([k, round(float(loss), 2)])
    out = {"variant": variant, "zero_prediction": round(zero, 2), "losses": losses,
           "drop": round(1 - losses[-1][1] / losses[0][1], 4), "below_zero_prediction": round(1 - losses[-1][1] / zero, 4)}
    print(variant, json.dumps(out), flush=True)
    (HERE / f"{variant}.json").write_text(json.dumps(out, indent=1))


def summary() -> None:
    rows = {v: json.loads((HERE / f"{v}.json").read_text()) for v in VARIANTS if (HERE / f"{v}.json").exists()}
    OUT.write_text(json.dumps({"question": __doc__, "variants": rows}, indent=1))
    for v, r in rows.items():
        print(v, r["drop"], r["below_zero_prediction"])


if __name__ == "__main__":
    summary() if sys.argv[1] == "summary" else run(sys.argv[1])
