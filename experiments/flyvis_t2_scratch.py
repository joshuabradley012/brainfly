"""Exploratory, not pre-registered: train a flyvis model from scratch with T2's response to darkening as a constraint
from the start.

Fine-tuning a trained flyvis model to give T2 its OFF response failed three ways: all parameters (rung3_t2.py) broke
motion direction; T2 alone (rung3_t2_local.py) flipped two polarities and cost LPLC2 its looming response, as T2's new
activity spread into the OFF-motion pathway; freeing T2's outputs too (flyvis_t2_pilot7.py) didn't converge. A
network trained with the constraint from the start can adapt everything else around it, as in the 8 of flyvis's 50
models whose T2 came out answering both flashes by chance. flyvis's own training here, on Apple's GPU: its network
and task configuration (model 000's), a fresh initialisation (resting potentials drawn with seed 9100, flyvis's
others fixed by its config), 250,000 iterations of its flow task at batch 4, Adam with its learning rate stepping from
5e-5 to 5e-6 in ten steps, its activity penalty (toward 5, weight 0.1, until iteration 150,000), plus
flyvis_t2_pilot5.py's capped T2 penalty at weight 100, every other iteration at twice that. Checkpoints every
2,500 iterations, every 500 from iteration 10,000 (so that a stop loses little); the run resumes from the last one. The model goes to flyvis's results as flow/9100/000. Logged:
the flow loss, T2's flash responses and flyvis's validation error; no test of rung 3.
With `control`, the same network from the same initialisation trains without the T2 penalty (flow/9101/000,
flyvis_t2_scratch_control.json, validation error every 2,500 iterations): at 20,000 iterations the constrained run
still predicted flow no better than zero, and this asks whether the constraint is what holds it back.

    python experiments/flyvis_t2_scratch.py            (writes experiments/flyvis_t2_scratch.json; resumable)
    python experiments/flyvis_t2_scratch.py control    (writes experiments/flyvis_t2_scratch_control.json; resumable)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

from brainfly import vistrain as vt
from flyvis_t2_pilot2 import t2 as t2_measures
from flyvis_t2_pilot5 import penalty as capped_t2_penalty

OUT = Path(__file__).with_suffix(".json")
NAME, SEED, ITERS = "flow/9100/000", 9100, 250_000
T2_WEIGHT, T2_EVERY, CHECKPOINT, EVAL_EVERY = 100.0, 2, 500, 10_000
if sys.argv[1:] == ["control"]:                     # the same training without the T2 penalty
    NAME, T2_WEIGHT, EVAL_EVERY, OUT = "flow/9101/000", 0.0, 2_500, OUT.with_name("flyvis_t2_scratch_control.json")


def build():
    """A fresh network by model 000's configuration, its decoder, flyvis's optimizer, penalty and scheduler."""
    import flyvis
    from datamate import Namespace
    from flyvis import NetworkView
    from flyvis.network import Network
    from flyvis.solver import HyperParamScheduler, Penalty
    from flyvis.task.tasks import init_decoder
    view = NetworkView(flyvis.results_dir / "flow/0000/000")
    config = view.dir.config.network.deepcopy()
    config.node_config.bias.seed = SEED
    with vt.on(vt.DEVICE):
        net = Network(**config.to_dict())
    task = vt.sintel(view)
    dec = init_decoder(view.dir.config.task.decoder, net.connectome)
    for d in dec.values():
        d.to(vt.DEVICE)
        for m in d.modules():
            if hasattr(m, "mask"):
                m.mask = m.mask.float().to(vt.DEVICE)
    with vt.on(vt.DEVICE):
        opt = torch.optim.Adam([{"params": net.parameters(), "lr": 5e-5}] +
                               [{"params": d.parameters(), "lr": 5e-5} for d in dec.values()])
        pen = Penalty(Namespace(activity_penalty=Namespace(activity_baseline=5.0, activity_penalty=0.1, stop_iter=150_000,
                                                           below_baseline_penalty_weight=1.0, above_baseline_penalty_weight=0.1),
                                optim="SGD"), net)
    step = lambda: Namespace(function="stepwise", start=5e-5, stop=5e-6, steps=10)
    sched = HyperParamScheduler(Namespace(lr_net=step(), lr_dec=step(), lr_pen=step(),
                                          dt=Namespace(function="stepwise", start=0.02, stop=0.02, steps=10)),
                                net, task, opt, pen)
    return view, net, dec, task, opt, pen, sched


def main() -> None:
    import flyvis
    view, net, dec, task, opt, pen, sched = build()
    folder = flyvis.results_dir / NAME
    chkpt = folder / "chkpts" / "scratch_last.pt"
    log = json.loads(OUT.read_text()) if OUT.exists() else {"question": __doc__, "trace": [], "evals": []}
    k = 0
    if chkpt.exists():
        state = torch.load(chkpt, map_location=vt.DEVICE, weights_only=False)
        net.load_state_dict(state["network"])
        for t, d in dec.items():
            d.load_state_dict(state["decoder"][t])
        opt.load_state_dict(state["optim"])
        for key, o in pen.optimizers.items():
            o.load_state_dict(state["penalty"][key])
        k = state["iteration"]
        print("resumed at", k, flush=True)
    torch.manual_seed(SEED + k)
    np.random.seed((SEED + k) % 2**32)
    sched(k)
    dt, t0, flow, t2p = task.dataset.dt, time.perf_counter(), [], []
    net.train()
    for d in dec.values():
        d.train()
    with task.dataset.augmentation(True):
        while k < ITERS:
            with vt.on(vt.DEVICE), torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=dt, batch_size=task.batch_size, value=0.5)
            for data in task.train_data:
                if k >= ITERS:
                    break
                with vt.on(vt.DEVICE):
                    opt.zero_grad()
                    net.stimulus.zero(*data["lum"].shape[:2])
                    net.stimulus.add_input(data["lum"].to(vt.DEVICE))
                    act = net(net.stimulus(), dt, state=state)
                    loss = task.loss(dec["flow"](act), data["flow"].to(vt.DEVICE), "flow")
                    extra = (T2_EVERY * T2_WEIGHT / 1000.0) * capped_t2_penalty(net) if k % T2_EVERY == 0 and T2_WEIGHT else torch.zeros((), device=vt.DEVICE)
                    (loss + extra).backward(retain_graph=True)
                    opt.step()
                    pen(activity=act, iteration=k)
                flow.append(float(loss))
                t2p.append(float(extra))
                k += 1
                if not np.isfinite(float(loss)):
                    raise FloatingPointError(f"flow loss {float(loss)} at iteration {k}")
                if k % CHECKPOINT == 0 or k == ITERS:
                    with torch.no_grad():
                        m = t2_measures(net)
                    log["trace"].append({"iteration": k, "flow_loss": round(float(np.mean(flow)), 2), "t2_penalty": round(float(np.mean(t2p)), 3),
                                         **m, "seconds": round(time.perf_counter() - t0)})
                    flow, t2p = [], []
                    if k % EVAL_EVERY == 0 or k == ITERS:
                        log["evals"].append({"iteration": k, "val_epe": round(vt.validation_epe(net, dec, task), 4)})
                        net.train()
                        for d in dec.values():
                            d.train()
                    folder.joinpath("chkpts").mkdir(parents=True, exist_ok=True)
                    torch.save({"network": net.state_dict(), "decoder": {t: d.state_dict() for t, d in dec.items()},
                                "optim": opt.state_dict(), "penalty": {key: o.state_dict() for key, o in pen.optimizers.items()},
                                "iteration": k}, chkpt)
                    OUT.write_text(json.dumps(log, indent=1))
                    print(json.dumps(log["trace"][-1]), json.dumps(log["evals"][-1]) if log["evals"] else "", flush=True)
            sched(k)                                      # flyvis steps its schedule between epochs
    epe = vt.validation_epe(net, dec, task)
    vt.save(net, dec, NAME, note={"experiment": "experiments/flyvis_t2_scratch.py", "iterations": ITERS, "seed": SEED}, val_epe=epe)
    log["end"] = {**t2_measures(net), "val_epe": round(epe, 4)}
    OUT.write_text(json.dumps(log, indent=1))
    print("end:", json.dumps(log["end"]), flush=True)


if __name__ == "__main__":
    main()
