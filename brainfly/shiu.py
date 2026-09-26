"""Shiu et al. (2024)'s whole-brain leaky integrate-and-fire model, run on the MaleCNS connectome.

Shiu, P. K. et al. A Drosophila computational brain model reveals sensorimotor processing.
Nature 634 (2024); code github.com/philshiu/Drosophila_brain_model. It is the fly whole-brain model
with the most experimental validation: 91% of 164 predictions held on FlyWire. Its recipe differs
from FlyBrain's on every axis the research report flags: raw synapse counts times one global weight
instead of per-neuron normalisation, 0.1 ms steps instead of 20 ms, no tonic drive or noise (every
neuron is silent until driven), and synaptic delay, current and refractoriness in real units:

    dv/dt = (x - (v - v0)) / t_mbr        dx/dt = -x / tau        (both frozen while refractory)
    v > v_th -> spike: v = v_rst, x = 0, refractory for t_rfc
    each spike adds w_syn * (signed synapse count) to x of every target, t_dly later

v0 = v_rst = -52 mV, v_th = -45 mV, t_mbr = 20 ms, tau = 5 ms, t_rfc = 2.2 ms, t_dly = 1.8 ms and
w_syn = 0.275 mV are Shiu's values. w_syn was fitted on FlyWire, whose synapse counts run lower than
MaleCNS's, so it needs refitting here. As in the original, a driven neuron gets Poisson input whose
every event pushes it over threshold (and it has no refractory period), and a silenced neuron loses
all its synapses. The equations are integrated exactly over each step, and each step runs in
Brian2's order, as Shiu's did. A consequence easy to miss: Brian2 drops input that reaches a
refractory neuron, because it gives variables marked "unless refractory" a conditional write.
tests/test_shiu_brian2.py checks the kernel against Brian2 spike for spike.

    brain = ShiuBrain(w_syn=0.275)
    rates = brain.run(1.0, drive=[(brain.cells(["LB3b", "LB3c"], side="L"), 100.0)]).rates
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import DATA, ensure_data

V0, V_RST, V_TH = -52.0, -52.0, -45.0     # mV
T_MBR, TAU, T_RFC, T_DLY = 0.020, 0.005, 0.0022, 0.0018   # s
W_SYN = 0.275                             # mV per synapse (fitted on FlyWire)
F_POI = 250                               # Poisson input weight = F_POI * w_syn


def counts(data: Path | str | None = None) -> sparse.csr_matrix:
    """The connectome before FlyBrain's normalisation: synapse counts between the neurons of
    brain.npz (rows = postsynaptic), negative where the presynaptic neuron's transmitter is GABA,
    glutamate or histamine (build.py's rule). Cached as <data>/counts.npz. The first call reads the
    MaleCNS tables in <data>/raw, downloading them (~1.1 GB) if they aren't there."""
    from .build import CONNECTIONS, connections, download_all, transmitter_signs

    data = ensure_data(data)
    cache = data / "counts.npz"
    if cache.exists():
        return sparse.load_npz(cache).tocsr()
    raw = data / "raw"
    download_all(raw)
    ids = np.load(data / "brain.npz")["ids"]
    sign = transmitter_signs(raw, ids)
    pre, post, synapses = connections(raw / CONNECTIONS, ids)
    C = sparse.csr_matrix((synapses * sign[pre], (post, pre)), shape=(len(ids), len(ids)), dtype=np.float32)
    sparse.save_npz(cache, C, compressed=False)
    return C


def mcns_types(data: Path | str | None = None) -> np.ndarray:
    """MaleCNS's own cell type for each neuron of brain.npz ("" where it has none). brain.npz names
    neurons by their FlyWire type first, which lumps some MaleCNS subtypes (LB3a-d are all "LB3")."""
    import pyarrow.feather as feather

    from .build import download_all

    data = ensure_data(data)
    download_all(data / "raw")
    ann = feather.read_table(data / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "type"]).to_pandas()
    ids = np.load(data / "brain.npz")["ids"]
    return ann.drop_duplicates("bodyId").set_index("bodyId").reindex(ids)["type"].fillna("").astype(str).to_numpy()


@numba.njit(parallel=True)
def _simulate(indptr, indices, weights, n, trials, steps, drive_steps, delay, rfc_steps,
              a_vv, a_vx, a_xx, drive_idx, drive_p, w_poi, silenced, bin_steps, seed):
    """Every trial in parallel. Each step follows Brian2's schedule, which Shiu's results come from:
    integrate every neuron that isn't refractory, find those over threshold, deliver the synaptic
    input due now and the Poisson input, then reset the neurons that fired. A spike's input arrives
    `delay` steps later. A neuron that fires at step t is refractory until step t + rfc_steps
    (Brian2: while timestep(t - lastspike) < timestep(t_rfc)): frozen, and deaf, since Brian2 drops
    writes to variables marked "unless refractory". Driven neurons have no refractory period, as in
    Shiu's code. Returns spike counts (trials, n) over the whole run, spike counts (trials, n) after
    the drive stops, and the network's spike count per bin (trials, bins)."""
    total = np.zeros((trials, n), np.int32)
    after = np.zeros((trials, n), np.int32)
    timeline = np.zeros((trials, (steps + bin_steps - 1) // bin_steps), np.int32)
    driven = np.zeros(n, np.bool_)
    for k in range(len(drive_idx)):
        driven[drive_idx[k]] = True
    for b in numba.prange(trials):
        np.random.seed(seed + b)
        u = np.zeros(n, np.float32)            # v - v0
        x = np.zeros(n, np.float32)
        until = np.zeros(n, np.int64)          # first step at which the neuron is no longer refractory
        pending = np.zeros((delay, n), np.float32)   # input arriving `delay` steps after a spike
        fired = np.empty(n, np.int64)
        for t in range(steps):
            m = 0
            for i in range(n):
                if t < until[i]:
                    continue
                ui = a_vv * u[i] + a_vx * x[i]
                x[i] = a_xx * x[i]
                u[i] = ui
                if ui > V_TH - V0:
                    fired[m] = i
                    m += 1
            row = pending[t % delay]
            for i in range(n):
                if row[i] != 0.0:
                    if t >= until[i]:
                        x[i] += row[i]
                    row[i] = 0.0
            if t < drive_steps:
                for k in range(len(drive_idx)):
                    if np.random.random() < drive_p[k] and t >= until[drive_idx[k]]:
                        u[drive_idx[k]] += w_poi
            for s in range(m):                 # input that just reached these is reset away
                i = fired[s]
                u[i] = V_RST - V0
                x[i] = 0.0
                until[i] = t if driven[i] else t + rfc_steps
                total[b, i] += 1
                if t >= drive_steps:
                    after[b, i] += 1
                if not silenced[i]:
                    for e in range(indptr[i], indptr[i + 1]):
                        row[indices[e]] += weights[e]
            timeline[b, t // bin_steps] += m
    return total, after, timeline


@dataclass
class Result:
    """One run. rates: Hz per neuron over the drive, mean over trials; trial_rates: (trials, n);
    after_rates: (trials, n) Hz after the drive stopped (empty tail -> zeros); timeline: network
    spikes per second in each bin, (trials, bins); bin: bin width in seconds."""
    rates: np.ndarray
    trial_rates: np.ndarray
    after_rates: np.ndarray
    timeline: np.ndarray
    bin: float


class ShiuBrain:
    """dt: step in seconds (Shiu used Brian2's default 0.1 ms). trials: independent runs, each with
    its own Poisson input, simulated in parallel. matrix: signed synapse counts to use instead of
    the connectome (e.g. a shuffled copy), rows = postsynaptic, same neurons as brain.npz.
    scale: one multiplier per neuron on every synapse onto it (e.g. 1 / size, so a synapse onto a
    big, leaky neuron moves it less); None = Shiu's uniform weight."""

    def __init__(self, data: Path | str | None = None, w_syn: float = W_SYN, trials: int = 30,
                 dt: float = 1e-4, matrix: sparse.spmatrix | None = None, scale: np.ndarray | None = None):
        data = ensure_data(data)
        meta = np.load(data / "brain.npz")
        self.cell_type = meta["cell_type"]
        self.mcns_type = mcns_types(data)
        self.side = meta["side"]
        self.superclass = meta["superclass"]
        C = (counts(data) if matrix is None else matrix).tocsc()   # columns = presynaptic
        self.n = C.shape[0]
        self.indptr, self.indices = C.indptr, C.indices
        self.synapses = C.data.astype(np.float32)
        self.w_syn = float(w_syn)
        self.trials = int(trials)
        self.dt = float(dt)
        self.scale = None if scale is None else np.asarray(scale, np.float32)

    def cells(self, types: list[str], side: str | None = None) -> np.ndarray:
        """Neurons whose cell type (FlyWire's or MaleCNS's own) or superclass is in `types`,
        optionally on one side."""
        named = np.isin(self.cell_type, types) | np.isin(self.mcns_type, types) | np.isin(self.superclass, types)
        return np.flatnonzero(named & (self.side == side) if side else named)

    def run(self, seconds: float, drive=(), silence=(), tail: float = 0.0, seed: int = 0,
            bin: float = 0.01) -> Result:
        """Drive neurons for `seconds` with Poisson input, then keep simulating `tail` seconds with
        no drive. drive: (neuron indices, rate in Hz) pairs. silence: neuron indices whose synapses
        are removed (they receive nothing and their spikes go nowhere)."""
        dt = self.dt
        idx = [np.asarray(i, np.int64) for i, _ in drive]
        drive_idx = np.concatenate(idx) if idx else np.empty(0, np.int64)
        drive_p = (np.concatenate([np.full(len(i), r * dt) for i, (_, r) in zip(idx, drive)])
                   if idx else np.empty(0))
        silenced = np.zeros(self.n, np.bool_)
        silenced[np.asarray(silence, np.int64)] = True
        weights = self.synapses * np.float32(self.w_syn)
        if self.scale is not None:
            weights *= self.scale[self.indices]
        weights[silenced[self.indices]] = 0.0          # nothing reaches a silenced neuron
        e_m, e_s = np.exp(-dt / T_MBR), np.exp(-dt / TAU)
        a_vx = TAU / (TAU - T_MBR) * (e_s - e_m)
        drive_steps = int(round(seconds / dt))
        steps = drive_steps + int(round(tail / dt))
        bin_steps = max(1, int(round(bin / dt)))
        total, after, timeline = _simulate(
            self.indptr, self.indices, weights, self.n, self.trials, steps, drive_steps,
            int(round(T_DLY / dt)), int(round(T_RFC / dt)), np.float32(e_m), np.float32(a_vx),
            np.float32(e_s), drive_idx, drive_p, np.float32(F_POI * self.w_syn), silenced, bin_steps, seed)
        during = (total - after) / seconds
        return Result(rates=during.mean(0), trial_rates=during,
                      after_rates=after / tail if tail > 0 else np.zeros_like(during),
                      timeline=timeline / (bin_steps * dt), bin=bin_steps * dt)
