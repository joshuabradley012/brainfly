"""Exploratory, not pre-registered: why didn't flyvis_t2_scratch.py's `fast` run learn through model 000's fixed decoder?

`fast` trained a fresh flyvis network with T2's response to darkening as a constraint, read by model 000's trained
decoder held fixed. Its validation error stayed at the level of predicting no flow (5.777 at 2,500, 5,000 and 7,500
iterations), constant to the fourth decimal while the network's parameters kept changing. These checks ask whether the
network is alive and whether the decoder passes it a gradient.
  activity  on flyvis's first 4 validation clips (no augmentation, 0.25 s of grey first): each network's mean
            activity, the share of its nodes above zero at any time and for at least half the time, the median over
            nodes of each node's standard deviation over time, the readout's size and the clips' endpoint error, for
            the fresh network (seed 9100), fast's last checkpoint, main's last checkpoint (each read by its own
            decoder; the fresh network by model 000's) and flyvis's trained model 000
  gradient  on the first validation clip, for the fresh network and fast's checkpoint read by model 000's decoder:
            the decoder's batch-norm outputs (its softplus inputs), the share of them below -4 (where the softplus is
            flat) and the flow loss's gradient norm on the network's parameters, with the batch norm on model 000's
            running statistics (as `fast` trained) and on the clip's own statistics
Ran: the networks are alive; the decoder starves them. Training made the fresh network answer the stimulus (median
temporal standard deviation 0.0004 fresh, 0.18 in fast, 0.19 in main, 0.29 in model 000), and nearly all of its nodes
are active. But model 000's decoder, normalizing by model 000's statistics, reads fast's network as almost nothing
(readout 0.009, against 2.2 for model 000): 81% of its softplus inputs sit below -4 (mean -128; -11 for the fresh
network). Normalized by the clip's own statistics, none do, and the gradient on the network is 9 times larger (1,499
against 161). Main's trainable decoder reads its network a little (readout 0.29; error 16.79 on these clips, against
16.89 for predicting no flow and 15.07 for model 000).

    python experiments/flyvis_readout.py      (writes experiments/flyvis_readout.json; on the CPU)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

os.environ["BRAINFLY_DEVICE"] = "cpu"               # beside a training run on the GPU
sys.argv = [sys.argv[0], "fast"]                     # flyvis_t2_scratch's fast configuration: model 000's decoder

import numpy as np  # noqa: E402
import torch  # noqa: E402

import flyvis_t2_scratch as fs  # noqa: E402
from brainfly import vistrain as vt  # noqa: E402

OUT = Path(__file__).with_suffix(".json")
CLIPS = 4
DEV = torch.device("cpu")


def checkpoint(name: str) -> dict:
    """A training run's last checkpoint, copied first since a running job may be rewriting it."""
    import flyvis
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(flyvis.results_dir / name / "chkpts" / "scratch_last.pt", Path(tmp) / "ck.pt")
        return torch.load(Path(tmp) / "ck.pt", map_location="cpu", weights_only=False)


def run(net, dec, data, dt):
    with vt.on(DEV):
        state = net.steady_state(t_pre=0.25, dt=dt, batch_size=1, value=0.5)
        net.stimulus.zero(1, data["lum"].shape[1])
        net.stimulus.add_input(data["lum"])
        act = net(net.stimulus(), dt, state=state)
        return act, dec["flow"](act)


def main() -> None:
    from flyvis.task.objectives import epe
    view, net, dec, task, opt, pen, sched = fs.build()
    dt = task.dataset.dt
    model000 = {t: {k: v.clone() for k, v in d.state_dict().items()} for t, d in dec.items()}
    fresh = {k: v.clone() for k, v in net.state_dict().items()}
    fast, main_run = checkpoint("flow/9104/000"), checkpoint("flow/9100/000")
    _, net000, _ = vt.load("flow/0000/000", DEV)
    with task.dataset.augmentation(False):
        clips = [data for _, data in zip(range(CLIPS), task.val_data)]
    zero = float(np.mean([float(epe(torch.zeros_like(c["flow"]), c["flow"])) for c in clips]))
    out = {"question": __doc__, "zero_prediction_epe": round(zero, 4), "activity": {}, "gradient": []}
    for name, net_state, dec_state in (("fresh", fresh, model000), (f"fast at {fast['iteration']:,}", fast["network"], fast["decoder"]),
                                       (f"main at {main_run['iteration']:,}", main_run["network"], main_run["decoder"]),
                                       ("model 000", net000.state_dict(), model000)):
        net.load_state_dict(net_state)
        for t, d in dec.items():
            d.load_state_dict(dec_state[t])
            d.eval()
        net.eval()
        acts, ys, errors = [], [], []
        with torch.no_grad():
            for c in clips:
                a, y = run(net, dec, c, dt)
                acts.append(a[0].numpy())
                ys.append(y[0].numpy())
                errors.append(float(epe(y, c["flow"])))
        A, Y = np.concatenate(acts), np.concatenate(ys)
        on = (A > 1e-6).mean(0)
        out["activity"][name] = {"epe": round(float(np.mean(errors)), 4), "mean_activity": round(float(A.mean()), 4),
                                 "nodes_ever_active": round(float((on > 0).mean()), 4), "nodes_active_half_the_time": round(float((on > 0.5).mean()), 4),
                                 "median_temporal_std": round(float(np.median(A.std(0))), 5), "readout_abs_mean": round(float(np.abs(Y).mean()), 4)}
        print(name, json.dumps(out["activity"][name]), flush=True)

    bn = dec["flow"].base[1]
    seen = {}
    bn.register_forward_hook(lambda m, i, o: seen.__setitem__("x", o.detach()))
    for name, net_state in (("fresh", fresh), (f"fast at {fast['iteration']:,}", fast["network"])):
        net.load_state_dict(net_state)
        for own in (False, True):
            dec["flow"].load_state_dict(model000["flow"])
            dec["flow"].eval()
            bn.train(own)                                # the clip's own statistics, the weights still fixed
            net.eval()
            net.zero_grad()
            a, y = run(net, dec, clips[0], dt)
            task.loss(y, clips[0]["flow"], "flow").backward()
            g = torch.sqrt(sum((p.grad ** 2).sum() for p in net.parameters() if p.grad is not None)).item()
            x = seen["x"]
            row = {"network": name, "batch_norm": "the clip's own statistics" if own else "model 000's statistics",
                   "softplus_input_mean": round(float(x.mean()), 2), "share_below_minus_4": round(float((x < -4).float().mean()), 3),
                   "readout_abs_mean": round(float(y.abs().mean()), 4), "gradient_norm": round(g, 1)}
            out["gradient"].append(row)
            print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
