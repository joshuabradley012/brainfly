"""Training flyvis's optic lobe on this machine, with brainfly's added constraints (rung 3).

flyvis (Lappalainen et al. 2024) fits its connectome-constrained optic lobe (brainfly.optic) by training it to
report optic flow in Sintel movies. flyvis runs on CUDA or the CPU. On a Mac's CPU one training iteration takes
about 3 s, and flyvis trains each model for 250,000. Here the same network runs on Apple's GPU (MPS), about 7x
faster (0.46 s per iteration on an M4 Pro), after working around the places where flyvis builds float64 or CPU
tensors. The validation error matches flyvis's published values on either device.

    load(model)                   a flyvis network and its flow decoder, on the GPU when there is one
    sintel(view)                  flyvis's training task (MultiTaskSintel flow, its train/validation split)
    flash_responses(net, "T2")    the central cell's response to a full-field ON and OFF flash, differentiably
    flash_peaks(net, "T2")        their peaks, as flyvis_screen.py measures them
    central_flash_responses(net)  every type's central cell's flash responses at once
    validation_epe(net, dec, t)   flyvis's validation endpoint error
    fine_tune(...)                flyvis's training step (Adam on its flow loss) plus a penalty on the flash peaks
    local(net, "T2")              masks for fine_tune freeing only one cell type's own parameters and its inputs
    save(net, dec, name)          a model directory flyvis (and brainfly.optic) loads like a pretrained one
"""
from __future__ import annotations

import json
import os
import shutil
import time
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Callable

import numpy as np

from .data import DATA

os.environ.setdefault("FLYVIS_ROOT_DIR", str(DATA / "flyvis"))
import torch  # noqa: E402

DEVICE = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
N_OMMATIDIA = 721                   # flyvis's lattice, extent 15


@contextmanager
def on(dev: torch.device):
    """Build and run flyvis modules on `dev`: its default device, with float64 made float32 (MPS has no float64)."""
    import flyvis
    import flyvis.task.decoder as decoder
    saved = torch.tensor, torch.from_numpy, torch.Generator, flyvis.device, decoder.device, torch.get_default_device()
    tensor, from_numpy, generator = saved[:3]

    def as32(data, *a, **k):
        if "dtype" not in k:
            if isinstance(data, np.ndarray) and data.dtype == np.float64:
                data = data.astype(np.float32)
            elif isinstance(data, (float, np.floating)):
                k["dtype"] = torch.float32
        return tensor(data, *a, **k)

    if dev.type != "cpu":
        torch.tensor = as32
        torch.from_numpy = lambda x: from_numpy(x.astype(np.float32) if x.dtype == np.float64 else x)
        torch.Generator = lambda *a, **k: generator(device=dev)
    flyvis.device = decoder.device = dev
    torch.set_default_device(dev)
    try:
        yield
    finally:
        torch.tensor, torch.from_numpy, torch.Generator, flyvis.device, decoder.device = saved[:5]
        torch.set_default_device(saved[5])


def load(model: str = "flow/0000/000", dev: torch.device = DEVICE):
    """flyvis's `model` (a path under its results directory): (view, network, decoders), on `dev`."""
    import flyvis
    from flyvis import NetworkView
    view = NetworkView(flyvis.results_dir / model)
    with on(dev):
        net = view.init_network()
    dec = view.init_decoder()                         # built on the CPU (its hex mask is float64), then moved
    for d in dec.values():
        d.to(dev)
        for m in d.modules():
            if hasattr(m, "mask"):
                m.mask = m.mask.float().to(dev)
    return view, net, dec


def sintel(view):
    """flyvis's training task for `view`'s config: Sintel flow, flyvis's original train/validation split."""
    from flyvis.task.tasks import Task
    config = {k: v for k, v in view.dir.config.task.to_dict().items() if k not in ("type", "task_weight")}
    return Task(**config, task_weights=None, original_split=True)


def _cells(net) -> list[str]:
    return [c.decode() if isinstance(c, bytes) else str(c) for c in net.connectome.unique_cell_types[:]]


def central(net, cell: str) -> int:
    """The index of `cell`'s central column in flyvis's activity."""
    return int(np.asarray(net.connectome.central_cells_index[:])[_cells(net).index(cell)])


@lru_cache(maxsize=8)
def _flashes(dt: float, t_pre: float, t_flash: float, radius: int) -> np.ndarray:
    from flyvis.datasets.flashes import render_flash
    with on(torch.device("cpu")):                     # flyvis renders on the CPU
        x = [render_flash(N_OMMATIDIA, i, 0.5, t_flash, t_pre, dt, (0, 1), radius) for i in (1.0, 0.0)]
    return np.stack(x)[:, :, None].astype(np.float32)


def flash_responses(net, cell: str = "T2", dt: float = 0.01, t_pre: float = 0.1, t_flash: float = 0.5,
                    radius: int = 6, dev: torch.device = DEVICE) -> torch.Tensor:
    """The central `cell`'s change from grey through the `t_flash` s after a flash of radius `radius` hexals turns
    light (1) or dark (0) from grey (0.5), starting from grey's steady state: (2, frames), rows ON and OFF, with
    gradients."""
    x = torch.from_numpy(_flashes(dt, t_pre, t_flash, radius)).to(dev)
    j, pre = central(net, cell), int(round(t_pre / dt))
    with on(dev):
        state = net.steady_state(t_pre=0.5, dt=dt, batch_size=2, value=0.5)
        net.stimulus.zero(2, x.shape[1])
        net.stimulus.add_input(x)
        a = net(net.stimulus(), dt, state=state)[:, :, j]
    return a[:, pre:] - a[:, :pre].mean(1, keepdim=True)


def central_flash_responses(net, dt: float = 0.01, t_pre: float = 0.1, t_flash: float = 0.5, radius: int = 6,
                            dev: torch.device = DEVICE) -> torch.Tensor:
    """flash_responses for the central cell of every type at once: (2, frames, types), rows ON and OFF, types in
    flyvis's order (node_params keys), with gradients."""
    x = torch.from_numpy(_flashes(dt, t_pre, t_flash, radius)).to(dev)
    j = torch.as_tensor(np.asarray(net.connectome.central_cells_index[:]), device=dev)
    pre = int(round(t_pre / dt))
    with on(dev):
        state = net.steady_state(t_pre=0.5, dt=dt, batch_size=2, value=0.5)
        net.stimulus.zero(2, x.shape[1])
        net.stimulus.add_input(x)
        a = net(net.stimulus(), dt, state=state)[:, :, j]
    return a[:, pre:] - a[:, :pre].mean(1, keepdim=True)


def flash_peaks(net, cell: str = "T2", dt: float = 0.01, t_pre: float = 0.1, t_flash: float = 0.5,
                radius: int = 6, dev: torch.device = DEVICE) -> torch.Tensor:
    """flash_responses' peaks, as flyvis_screen.py measures them: tensor([on, off]), with gradients."""
    return flash_responses(net, cell, dt, t_pre, t_flash, radius, dev).max(1).values


def validation_epe(net, dec, task, dev: torch.device = DEVICE) -> float:
    """flyvis's validation loss: the flow's endpoint error over its validation sequences (no augmentation)."""
    from flyvis.task.objectives import epe
    net.eval()
    for d in dec.values():
        d.eval()
    out = []
    with torch.no_grad(), task.dataset.augmentation(False):
        for data in task.val_data:
            with on(dev):
                state = net.steady_state(t_pre=0.25, dt=task.dataset.dt, batch_size=1, value=0.5)
                net.stimulus.zero(1, data["lum"].shape[1])
                net.stimulus.add_input(data["lum"].to(dev))
                y = dec["flow"](net(net.stimulus(), task.dataset.dt, state=state))
            out.append(float(epe(y, data["flow"].to(dev))))
    return float(np.mean(out))


def local(net, cell: str) -> dict[str, torch.Tensor]:
    """Masks for fine_tune that free only `cell`'s own parameters (resting potential and time constant) and the
    strengths of the synapses onto it."""
    to_cell = torch.tensor([t == cell for _, t in net.edge_params["syn_strength"].keys])
    own = torch.tensor([c == cell for c in net.node_params["bias"].keys])
    assert list(net.node_params["time_const"].keys) == list(net.node_params["bias"].keys)
    return {"nodes_bias": own, "nodes_time_const": own, "edges_syn_strength": to_cell}


def fine_tune(net, dec, task, penalty: Callable | None, iters: int, lr: float = 5e-6, seed: int = 0,
              every: int = 100, log: Callable[[dict], None] = print, dev: torch.device = DEVICE,
              masks: dict[str, torch.Tensor] | None = None, train_decoder: bool = True) -> list[dict]:
    """flyvis's training step for `iters` iterations: Adam on network and decoder, flyvis's flow loss on augmented
    Sintel batches, each epoch starting from grey's steady state. `penalty(net)` (a scalar tensor) is added to
    each iteration's loss. masks: {network parameter name: boolean mask}; given, only the masked entries of those
    parameters train and every other network parameter is frozen (see local). train_decoder: False freezes the
    flow decoder. Logs the mean losses every `every` iterations."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    named = dict(net.named_parameters())
    free = {n: m.to(dev) for n, m in (masks or {}).items()}
    params = [p for n, p in named.items() if masks is None or n in free]
    if train_decoder:
        params += [p for d in dec.values() for p in d.parameters()]
    opt = torch.optim.Adam(params, lr=lr)
    net.train()
    for d in dec.values():
        d.train()
    dt, rows, flow, pen, t0 = task.dataset.dt, [], [], [], time.perf_counter()
    k = 0
    with task.dataset.augmentation(True):
        while k < iters:
            with on(dev), torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=dt, batch_size=task.batch_size, value=0.5)
            for data in task.train_data:                  # the sampler runs on the CPU
                if k >= iters:
                    break
                with on(dev):
                    opt.zero_grad()
                    net.stimulus.zero(*data["lum"].shape[:2])
                    net.stimulus.add_input(data["lum"].to(dev))
                    loss = task.loss(dec["flow"](net(net.stimulus(), dt, state=state)), data["flow"].to(dev), "flow")
                    extra = penalty(net) if penalty is not None else torch.zeros((), device=dev)
                    (loss + extra).backward()
                    for n, m in free.items():             # frozen entries get no gradient, so Adam leaves them
                        if named[n].grad is not None:
                            named[n].grad.mul_(m.to(named[n].grad.dtype))
                    opt.step()
                    net.clamp()
                flow.append(float(loss))
                pen.append(float(extra))
                k += 1
                if k % every == 0 or k == iters:
                    rows.append({"iteration": k, "flow_loss": round(float(np.mean(flow)), 2),
                                 "penalty": round(float(np.mean(pen)), 4), "seconds": round(time.perf_counter() - t0)})
                    log(rows[-1])
                    flow, pen = [], []
                if not np.isfinite(float(loss)):
                    raise FloatingPointError(f"flow loss {float(loss)} at iteration {k}")
    net.eval()
    for d in dec.values():
        d.eval()
    return rows


def save(net, dec, name: str, source: str = "flow/0000/000", note: dict | None = None, val_epe: float | None = None) -> Path:
    """A flyvis model directory `name` (under flyvis's results) holding net and dec: `source`'s directory with
    its checkpoint replaced, so flyvis's NetworkView and brainfly.optic load it like a pretrained model. Any
    parameters brainfly.optic cached for an earlier model of the same name are removed."""
    import flyvis
    src, dst = flyvis.results_dir / source, flyvis.results_dir / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__cache__"))
    chkpt = {"network": {k: v.detach().cpu() for k, v in net.state_dict().items()},
             "decoder": {t: {k: v.detach().cpu() for k, v in d.state_dict().items()} for t, d in dec.items()}}
    torch.save(chkpt, dst / "chkpts" / "chkpt_00000")
    torch.save(chkpt, dst / "best_chkpt")
    if val_epe is not None:
        import h5py
        with h5py.File(dst / "validation_loss.h5", "r+") as f:
            f["data"][()] = val_epe
    (dst / "brainfly.json").write_text(json.dumps({"source": source, **(note or {})}, indent=1))
    for cache in (f"flyvis_{name.replace('/', '_')}.npz", f"flyvis_filters_{name.replace('/', '_')}.npz"):
        (DATA / cache).unlink(missing_ok=True)       # brainfly.optic's parameters for an older model of this name
    return dst
