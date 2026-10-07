"""flyvis's network on the male eye, as brainfly.optic.FlyvisNative tiles it, in PyTorch and differentiable in the flyvis
model's own parameters, so that a flyvis model can be trained on what the tiled eye does (rung 3's direction test).

One eye (FlyvisNative's two are independent copies). Each cell steps as FlyvisNative._advance does,
V <- V + dt / tau (-V + bias + W relu(V) + x), with x the photoreceptors' input, 0.5 (1 + contrast) in their column.
W's entries are sign x strength x count of the flyvis filter element each one comes from (optic.tile_entries);
strength, bias and time constant are the network's trainable parameters, so gradients reach them.

    eye = EyeTorch(net, side="R", dt=0.02)              # net: a flyvis Network (brainfly.vistrain.load)
    rest = eye.settle(net)                               # grey's steady state (no gradient)
    x = eye.edge_sweeps(polarity=-1.0)                    # the direction test's four sweeps, as photoreceptor input
    peak = eye.peaks(net, x, rest)                        # (4, cells): each cell's peak change of relu(V) from rest
    r = eye.type_means(peak, "T5a")                       # (4,): the subtype's mean, as the direction test takes it
"""
from __future__ import annotations

import numpy as np
import torch
from torch.utils.checkpoint import checkpoint

from .optic import BACKGROUND, MODEL, R16, flyvis_filters, plane, tile_entries
from . import vistrain as vt

SPEED = 40.0                                             # deg/s, as flyvis_native.direction_selectivity
MOVES = {"R": {"front-to-back": ("azimuth", 20, -180, +1), "back-to-front": ("azimuth", -180, 20, -1),
               "upward": ("elevation", -90, 90, -1), "downward": ("elevation", 90, -90, +1)},
         "L": {"front-to-back": ("azimuth", -20, 180, -1), "back-to-front": ("azimuth", 180, -20, +1),
               "upward": ("elevation", -90, 90, -1), "downward": ("elevation", 90, -90, +1)}}


def _name(k) -> str:
    return k.decode() if isinstance(k, bytes) else str(k)


class EyeTorch:
    def __init__(self, net, side: str = "R", dt: float = 0.02, structure: str = MODEL, data=None,
                 dev: torch.device = vt.DEVICE, chunk: int = 25):
        """net: the flyvis network whose parameters weight the eye. structure: a flyvis model whose connectome gives
        the filters' counts, signs and sparse types' positions (the same for every model of flyvis's ensemble)."""
        from .eye2d import ACCEPTANCE_DEG, column_directions
        f = flyvis_filters(structure, data)
        dirs = column_directions(data)
        ks = sorted(k for k in dirs if k[0] == side)
        C = np.array([(h1, h2) for _, h1, h2 in ks])
        xy = plane(*C.T)
        origin = C[np.argmin(((xy - xy.mean(0)) ** 2).sum(1))]              # as FlyvisNative
        cell_type, cell_col, rows, cols, element, keys = tile_entries(C, origin, f)
        self.side, self.dt, self.dev, self.chunk = side, float(dt), dev, chunk
        self.cell_type, self.cell_col = cell_type, cell_col
        self.directions = np.array([dirs[k] for k in ks])
        self.sigma = np.radians(ACCEPTANCE_DEG) / (2 * np.sqrt(2 * np.log(2)))
        self.n = len(cell_type)

        ep, npar = net.edge_params, net.node_params
        pair = {(_name(s), _name(t)): i for i, (s, t) in enumerate(ep["syn_strength"].keys)}
        sign = {(_name(s), _name(t)): float(v) for (s, t), v in zip(ep["sign"].keys, ep["sign"].semantic_values.tolist())}
        count = {(_name(s), _name(t), int(du), int(dv)): float(v)
                 for (s, t, du, dv), v in zip(ep["syn_count"].keys, ep["syn_count"].semantic_values.tolist())}
        self.pair_of_element = torch.tensor([pair[(s, t)] for s, t, du, dv in keys], device=dev)
        self.fixed_of_element = torch.tensor([sign[(s, t)] * count[(s, t, du, dv)] for s, t, du, dv in keys],
                                             dtype=torch.float32, device=dev)
        self.element = torch.as_tensor(element, device=dev)
        self.rows = torch.as_tensor(rows, device=dev)
        self.cols = torch.as_tensor(cols, device=dev)
        types = [_name(k) for k in npar["bias"].keys]
        assert types == [_name(k) for k in npar["time_const"].keys]
        self.type_of_cell = torch.tensor([types.index(t) for t in cell_type], device=dev)
        inp = np.flatnonzero(np.isin(cell_type, R16 + ["R7", "R8"]))
        self.input_cells = torch.as_tensor(inp, device=dev)
        self.input_cols = cell_col[inp]
        self._rest = None

    def weights(self, net):
        """(W values per synapse, bias per cell, time constant per cell), from the network's current parameters."""
        strength = net.edge_params["syn_strength"].semantic_values
        w = (self.fixed_of_element * strength[self.pair_of_element].float())[self.element]
        bias = net.node_params["bias"].semantic_values.float()[self.type_of_cell]
        tau = torch.clamp(net.node_params["time_const"].semantic_values.float()[self.type_of_cell], min=self.dt)
        return w, bias, tau

    def _step(self, V, x, w, bias, tau):
        """One FlyvisNative step for a batch: V (batch, cells), x (batch, input cells)."""
        r = torch.relu(V)
        drive = torch.zeros_like(V).index_add_(1, self.rows, r[:, self.cols] * w)
        inp = torch.zeros_like(V)
        inp[:, self.input_cells] = x
        return V + self.dt / tau * (-V + bias + drive + inp)

    def settle(self, net, seconds: float = 10.0) -> torch.Tensor:
        """Grey's steady state (1, cells), without gradient; later calls start from the last one."""
        with torch.no_grad():
            w, bias, tau = self.weights(net)
            V = bias[None].clone() if self._rest is None else self._rest
            x = torch.full((1, len(self.input_cells)), BACKGROUND, device=self.dev)
            for _ in range(int(round(seconds / self.dt))):
                V = self._step(V, x, w, bias, tau)
        self._rest = V
        return V

    def edge_sweeps(self, polarity: float, speed: float = SPEED) -> tuple[torch.Tensor, torch.Tensor, list[str]]:
        """flyvis_native.direction_selectivity's four edges across this eye as photoreceptor input: (4, steps, input
        cells), each sweep's length in steps, and the directions' names. Shorter sweeps repeat their last frame."""
        from .eye2d import Edge, render
        names = list(MOVES[self.side])
        seqs = []
        for name in names:
            axis, a, b, behind = MOVES[self.side][name]
            n = int((abs(b - a) / speed + 0.5) / self.dt)
            frames = [render(self.directions, np.ones(len(self.directions), bool),
                             [Edge(axis, a + np.sign(b - a) * speed * s * self.dt, behind, polarity)], self.sigma)
                      for s in range(n)]
            seqs.append(BACKGROUND * (1 + np.stack(frames)[:, self.input_cols]))
        lengths = [len(q) for q in seqs]
        m = max(lengths)
        x = np.stack([np.concatenate([q, np.repeat(q[-1:], m - len(q), 0)]) for q in seqs]).astype(np.float32)
        return torch.as_tensor(x, device=self.dev), torch.as_tensor(lengths, device=self.dev), names

    def peaks(self, net, sweeps, rest: torch.Tensor | None = None) -> torch.Tensor:
        """Each cell's peak change of relu(V) from rest over each sweep (batch, cells), with gradients (recomputed
        chunk by chunk in the backward pass, to keep the memory down)."""
        x, lengths, _ = sweeps
        rest = self.settle(net) if rest is None else rest
        w, bias, tau = self.weights(net)
        V = rest.expand(x.shape[0], -1).clone()
        r0 = torch.relu(rest)
        best = torch.zeros_like(V)

        def run(V, best, start, xs):
            for k in range(xs.shape[1]):
                V = self._step(V, xs[:, k], w, bias, tau)
                live = (start + k < lengths)[:, None]
                best = torch.where(live, torch.maximum(best, torch.relu(V) - r0), best)
            return V, best

        for start in range(0, x.shape[1], self.chunk):
            xs = x[:, start:start + self.chunk]
            if torch.is_grad_enabled():
                V, best = checkpoint(run, V, best, start, xs, use_reentrant=False)
            else:
                V, best = run(V, best, start, xs)
        return best

    def type_means(self, peak: torch.Tensor, cell_type: str) -> torch.Tensor:
        """The mean over this eye's cells of a type (batch,), as the direction test takes it."""
        m = torch.as_tensor(np.flatnonzero(self.cell_type == cell_type), device=self.dev)
        return peak[:, m].mean(1)
