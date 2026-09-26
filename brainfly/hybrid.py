"""HybridBrain: brainfly's own network model, in which each cell type can be the kind of unit the
biology calls for.

The research report (reports/, "Fly neurons span a hundredfold range of input resistance") found
that fly neurons differ by type. Membrane time constants run from about 2 ms to 30 ms, excitability
falls with size, and many neurons never spike: the optic lobe's columnar cells, the mushroom body's
APL, patchy antennal-lobe local neurons, some nerve-cord interneurons. Shiu et al.'s model gives
every neuron one set of parameters and every synapse one weight, and on MaleCNS it runs away
(experiments/shiu_*.py). HybridBrain keeps Shiu's machinery, the Brian2-exact 0.1 ms kernel of
brainfly.shiu, and lets each cell type differ:

    unit          "spiking", or "graded": integrates the same way but never spikes, releasing
                  transmitter continuously at clip(gain * (v - release_at), 0, max_release) Hz.
                  Each Hz acts on its targets like one spike per second, and no refractory
                  period caps it.
    tau_m         membrane time constant, s (Shiu: 0.020 for every neuron)
    threshold     mV above rest (Shiu: 7)
    reset         mV above rest (Shiu: 0)
    refractory    s (Shiu: 0.0022)
    bias          a constant drive, as the depolarisation it holds a quiet neuron at, mV (Shiu: 0,
                  so every neuron is silent until driven)
    scale         a multiplier on every synapse onto the type (Shiu: 1)
    gain, release_at, max_release    a graded unit's release: Hz per mV, mV above rest, Hz
                  (defaults 6 Hz/mV from the threshold up with no ceiling, which roughly follows
                  a Shiu neuron's firing rate between 60 and 130 Hz; nothing measured sets them)
    depression, recovery    short-term depression of the type's outgoing synapses: the fraction
                  of their strength each spike leaves, recovering toward full with time constant
                  recovery, s (default 1: none; olfactory receptor neurons onto projection neurons:
                  0.78 and 0.893, Nagel, Hong & Wilson 2015)

A spike adds w_syn x (signed synapse count) to a fast current in each target (tau 5 ms, as in
Shiu), or to a slow current (tau_slow) along the edges given as slow, t_dly later. As in Brian2,
input that reaches a refractory neuron is lost, and a spike resets the fast current but not the
slow one. With no types and no slow edges HybridBrain is Shiu's model: tests/test_hybrid.py checks it
against Brian2 spike for spike. Its state persists between calls to advance(), so it can run inside
a loop with a body, and advancing in pieces gives the same spikes as advancing in one go.

    brain = HybridBrain(types={"APL": {"unit": "graded"}})
    rates = brain.run(1.0, drive=[(brain.cells(["LB3b", "LB3c"], side="L"), 100.0)]).rates
"""
from __future__ import annotations

from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import ensure_data
from .shiu import F_POI, T_DLY, T_MBR, T_RFC, TAU, V0, V_RST, V_TH, W_SYN, Result, counts, mcns_types

UNIT = {"spiking": False, "graded": True}
DEFAULTS = {"unit": "spiking", "tau_m": T_MBR, "threshold": V_TH - V0, "reset": V_RST - V0, "refractory": T_RFC,
            "bias": 0.0, "scale": 1.0, "gain": 6.0, "release_at": V_TH - V0, "max_release": np.inf,
            "depression": 1.0, "recovery": 1.0}
MONOAMINES = ("dopamine", "octopamine", "serotonin")


def _approach(tau_in: float, tau_m: float, dt: float) -> float:
    """How much of a current decaying with tau_in reaches v (time constant tau_m) over one step, per
    unit of current at its start: the exact solution of dv/dt = (i - v)/tau_m, di/dt = -i/tau_in."""
    if abs(tau_in - tau_m) < 1e-12:
        return dt / tau_m * np.exp(-dt / tau_m)
    return tau_in / (tau_in - tau_m) * (np.exp(-dt / tau_in) - np.exp(-dt / tau_m))


@numba.njit(inline="always")
def _uniform(rng, b):
    """The next number in [0, 1) from trial b's splitmix64 stream, whose state lives in rng[b], so it
    carries over from one call to the next."""
    z = rng[b] + np.uint64(0x9E3779B97F4A7C15)
    rng[b] = z
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return np.float64(z >> np.uint64(11)) * (1.0 / 9007199254740992.0)


@numba.njit(parallel=True)
def _advance(t0, steps, delay, dt, ptr, idx, w, sptr, sidx, sw,
             cls, a_vv, a_vx, a_vs, a_bias, a_xx, a_ss, theta, reset, rfc, graded, depress, recover,
             g_list, g_gain, g_at, g_max,
             u, x, s, until, pend, spend, R, rel, rng, left, last,
             drive_idx, drive_p, w_poi, driven, silenced, counts, timeline, bin_start, bin_steps):
    """Advance every trial `steps` steps from global step t0, in Brian2's order as brainfly.shiu does:
    integrate the neurons that aren't refractory, find the spiking ones over threshold, update graded
    release, deliver the input due now (spikes from `delay` steps ago, graded release, Poisson drive)
    to neurons that aren't refractory, then reset the neurons that fired and send their spikes.
    Per-neuron parameters come from a small table indexed by cls. A depressing neuron's spike carries
    the fraction left[b, i] of its full strength, recovered toward 1 (time constant recover, in
    steps) since its last spike, and leaves depress times that. counts[b, i] gains each spike, and
    timeline[b, (bin_start + k) // bin_steps] each step's spikes, if bin_steps > 0."""
    trials, n = u.shape
    slow = len(sw) > 0
    ng = len(g_list)
    for b in numba.prange(trials):
        fired = np.empty(n, np.int64)
        for k in range(steps):
            t = t0 + k
            m = 0
            for i in range(n):
                if t < until[b, i]:
                    continue
                c = cls[i]
                ui = a_vv[c] * u[b, i] + a_vx[c] * x[b, i] + a_bias[c]
                x[b, i] = a_xx * x[b, i]
                if slow:
                    ui += a_vs[c] * s[b, i]
                    s[b, i] = a_ss * s[b, i]
                u[b, i] = ui
                if ui > theta[c] and not graded[c]:
                    fired[m] = i
                    m += 1
            for q in range(ng):
                i = g_list[q]
                r = 0.0 if silenced[i] else min(max(g_gain[q] * (u[b, i] - g_at[q]), 0.0), g_max[q])
                change = r - rel[b, q]
                if change != 0.0:
                    rel[b, q] = r
                    for e in range(ptr[i], ptr[i + 1]):
                        R[b, idx[e]] += w[e] * change
            slot = t % delay
            row = pend[b, slot]
            srow = spend[b, slot]
            for i in range(n):
                live = t >= until[b, i]
                if row[i] != 0.0:
                    if live:
                        x[b, i] += row[i]
                    row[i] = 0.0
                if ng and live and R[b, i] != 0.0:
                    x[b, i] += R[b, i] * dt
                if slow and srow[i] != 0.0:
                    if live:
                        s[b, i] += srow[i]
                    srow[i] = 0.0
            for q in range(len(drive_idx)):
                j = drive_idx[q]
                if _uniform(rng, b) < drive_p[q] and t >= until[b, j]:
                    u[b, j] += w_poi
            for f in range(m):
                i = fired[f]
                u[b, i] = reset[cls[i]]
                x[b, i] = 0.0
                until[b, i] = t if driven[i] else t + rfc[cls[i]]
                counts[b, i] += 1
                strength = np.float32(1.0)
                if depress[cls[i]] < 1.0:
                    strength = np.float32(1.0 - (1.0 - left[b, i]) * np.exp(-(t - last[b, i]) / recover[cls[i]]))
                    left[b, i] = strength * depress[cls[i]]
                    last[b, i] = t
                if not silenced[i]:
                    for e in range(ptr[i], ptr[i + 1]):
                        row[idx[e]] += w[e] * strength
                    if slow:
                        for e in range(sptr[i], sptr[i + 1]):
                            srow[sidx[e]] += sw[e] * strength
            if bin_steps > 0:
                timeline[b, (bin_start + k) // bin_steps] += m


def consensus_transmitters(data: Path | str | None = None) -> np.ndarray:
    """Each neuron's consensus transmitter in MaleCNS ("" where it has none), as brainfly's sign rule
    reads it. Use this rather than predicted_nt: the machine prediction calls 4,058 of the 4,064
    Kenyon cells dopaminergic, while their consensus, like the literature, says acetylcholine."""
    import pyarrow.feather as feather

    from .build import TRANSMITTERS, download_all

    data = ensure_data(data)
    download_all(data / "raw")
    ids = np.load(data / "brain.npz")["ids"]
    nt = feather.read_table(data / "raw" / TRANSMITTERS, columns=["body", "consensus_nt"]).to_pandas()
    return nt.drop_duplicates("body").set_index("body").reindex(ids).consensus_nt.fillna("").astype(str).to_numpy()


def monoaminergic(data: Path | str | None = None) -> np.ndarray:
    """Which neurons MaleCNS's consensus calls dopaminergic, octopaminergic or serotonergic (541)."""
    return np.isin(consensus_transmitters(data), MONOAMINES)


def split(C: sparse.spmatrix, pre: np.ndarray | None = None, post: np.ndarray | None = None):
    """Split a matrix (rows = postsynaptic) into the entries whose presynaptic neuron is in `pre` and
    postsynaptic neuron in `post` (boolean masks; None means all), and the rest: (rest, chosen)."""
    coo = C.tocoo()
    chosen = np.ones(coo.nnz, bool)
    if pre is not None:
        chosen &= pre[coo.col]
    if post is not None:
        chosen &= post[coo.row]
    part = lambda keep: sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=C.shape)
    return part(~chosen), part(chosen)


class HybridBrain:
    """MaleCNS with per-type units. data: the folder with brain.npz (as ShiuBrain). trials: independent
    copies, each with its own Poisson input, run in parallel. dt: step, s. w_syn: mV per synapse.
    types: {cell type or superclass: {parameter: value}} (see the module docstring), applied in order,
    so list broad classes first. matrix: signed synapse counts, rows = postsynaptic (default
    shiu.counts). slow: signed counts of the edges that act through the slow current instead (not
    also in matrix), with tau_slow its time constant, s. w_poi: mV per Poisson event (default
    Shiu's, 250 x w_syn, which pushes any neuron over threshold). scale: a multiplier per neuron on
    every synapse onto it (e.g. 1 / size), on top of its type's. labels: {"cell_type", "side",
    "superclass"} arrays for a network of your own, given as matrix, instead of MaleCNS."""

    def __init__(self, data: Path | str | None = None, trials: int = 1, dt: float = 1e-4, w_syn: float = W_SYN,
                 types: dict[str, dict] | None = None, matrix: sparse.spmatrix | None = None,
                 slow: sparse.spmatrix | None = None, tau_slow: float = 0.1, w_poi: float | None = None,
                 scale: np.ndarray | None = None, seed: int = 0, labels: dict[str, np.ndarray] | None = None):
        if labels is None:
            data = ensure_data(data)
            meta = np.load(data / "brain.npz")
            labels = {k: meta[k] for k in ("cell_type", "side", "superclass")} | {"mcns_type": mcns_types(data)}
        elif matrix is None:
            raise ValueError("a network given by labels needs its matrix")
        self.cell_type, self.side, self.superclass = (np.asarray(labels[k]) for k in ("cell_type", "side", "superclass"))
        self.mcns_type = np.asarray(labels.get("mcns_type", self.cell_type))
        self.n = len(self.cell_type)
        self.trials, self.dt = int(trials), float(dt)
        self._fixed_poi = None if w_poi is None else float(w_poi)
        self.types = dict(types or {})
        self._tables()
        if scale is not None:
            self.scale = (self.scale * np.asarray(scale, np.float32)).astype(np.float32)
        C = (counts(data) if matrix is None else matrix).tocsc()
        self.ptr, self.idx, self._counts = C.indptr, C.indices, C.data.astype(np.float32)
        S = sparse.csc_matrix((self.n, self.n), dtype=np.float32) if slow is None else slow.tocsc()
        self.sptr, self.sidx, self._slow_counts = S.indptr, S.indices, S.data.astype(np.float32)
        self.w_syn = w_syn
        self.tau_slow = float(tau_slow)
        self.delay = int(round(T_DLY / self.dt))
        self.reset(seed)

    @property
    def w_syn(self) -> float:
        """mV per synapse; setting it rescales every weight (and the Poisson events, unless w_poi was given)."""
        return self._w_syn

    @w_syn.setter
    def w_syn(self, value: float) -> None:
        self._w_syn = float(value)
        self.weights = (self._counts * np.float32(value) * self.scale[self.idx]).astype(np.float32)
        self.slow_weights = (self._slow_counts * np.float32(value) * self.scale[self.sidx]).astype(np.float32)
        self.w_poi = F_POI * self._w_syn if self._fixed_poi is None else self._fixed_poi

    def cells(self, types: list[str], side: str | None = None) -> np.ndarray:
        """Neurons whose cell type (FlyWire's or MaleCNS's own) or superclass is in `types`,
        optionally on one side."""
        named = np.isin(self.cell_type, types) | np.isin(self.mcns_type, types) | np.isin(self.superclass, types)
        return np.flatnonzero(named & (self.side == side) if side else named)

    def _tables(self) -> None:
        """Each neuron's parameters, stored once per distinct combination: self.params lists the
        combinations and self.cls gives each neuron's."""
        keys = [k for k in DEFAULTS if k != "scale"]
        numeric = lambda name, value: float(UNIT[value]) if name == "unit" else float(value)
        values = np.array([[numeric(k, DEFAULTS[k]) for k in keys]] * self.n)
        self.scale = np.ones(self.n, np.float32)
        for key, given in self.types.items():
            unknown = set(given) - set(DEFAULTS)
            if unknown:
                raise ValueError(f"unknown parameters for {key!r}: {sorted(unknown)}; known: {list(DEFAULTS)}")
            if "unit" in given and given["unit"] not in UNIT:
                raise ValueError(f"unit must be one of {list(UNIT)}, not {given['unit']!r}")
            rows = self.cells([key])
            if not len(rows):
                raise ValueError(f"no neurons of type or superclass {key!r}")
            for name, value in given.items():
                if name == "scale":
                    self.scale[rows] = value
                else:
                    values[rows, keys.index(name)] = numeric(name, value)
        combos, cls = np.unique(values, axis=0, return_inverse=True)
        self.cls = cls.reshape(-1).astype(np.int32)
        self.params = [{k: (("spiking", "graded")[int(v)] if k == "unit" else float(v)) for k, v in zip(keys, row)}
                       for row in combos]
        self.graded = np.flatnonzero(np.array([p["unit"] == "graded" for p in self.params])[self.cls])

    def _coefficients(self):
        dt, table = self.dt, self.params
        f32 = lambda key: np.array([key(p) for p in table], np.float32)
        return dict(
            a_vv=f32(lambda p: np.exp(-dt / p["tau_m"])),
            a_vx=f32(lambda p: _approach(TAU, p["tau_m"], dt)),
            a_vs=f32(lambda p: _approach(self.tau_slow, p["tau_m"], dt)),
            a_bias=f32(lambda p: (1 - np.exp(-dt / p["tau_m"])) * p["bias"]),
            theta=f32(lambda p: p["threshold"]), reset=f32(lambda p: p["reset"]),
            rfc=np.array([int(round(p["refractory"] / dt)) for p in table], np.int64),
            graded=np.array([UNIT[p["unit"]] for p in table], np.bool_),
            depress=f32(lambda p: p["depression"]), recover=np.array([p["recovery"] / dt for p in table]))

    def reset(self, seed: int = 0) -> None:
        """Every trial back to rest, with fresh Poisson streams from `seed`."""
        shape = (self.trials, self.n)
        self.u, self.x, self.s = np.zeros(shape, np.float32), np.zeros(shape, np.float32), np.zeros(shape, np.float32)
        self.until = np.zeros(shape, np.int64)
        self.pending = np.zeros((self.trials, self.delay, self.n), np.float32)
        slow_n = self.n if len(self.slow_weights) else 0
        self.pending_slow = np.zeros((self.trials, self.delay, slow_n), np.float32)
        self.graded_input = np.zeros(shape if len(self.graded) else (self.trials, 0), np.float32)
        self.release = np.zeros((self.trials, len(self.graded)), np.float32)
        self.rng = np.random.SeedSequence(seed).generate_state(self.trials, dtype=np.uint64)
        self.driven = np.zeros(self.n, np.bool_)
        depressing = any(p["depression"] < 1 for p in self.params)
        self.left = np.ones(shape if depressing else (self.trials, 0), np.float32)
        self.last = np.full(shape if depressing else (self.trials, 0), -(1 << 40), np.int64)
        self.t = 0

    def advance(self, steps: int, drive=(), silence=()) -> np.ndarray:
        """Run `steps` steps and return each trial's spike count per neuron, (trials, n). drive:
        (neuron indices, rate in Hz) pairs of Poisson input, each event pushing its neuron w_poi mV.
        A neuron given drive has no refractory period from then until reset(), as in Shiu's code,
        where that is a fixed property of the drive's targets. silence: neuron indices whose spikes
        and release go nowhere during these steps."""
        return self._step(steps, drive, silence)

    def _step(self, steps, drive=(), silence=(), timeline=None, bin_start=0, bin_steps=0) -> np.ndarray:
        """advance(), also adding each step's spikes to timeline[:, (bin_start + k) // bin_steps]."""
        idx = [np.asarray(i, np.int64) for i, _ in drive]
        drive_idx = np.concatenate(idx) if idx else np.empty(0, np.int64)
        drive_p = np.concatenate([np.full(len(i), r * self.dt) for i, (_, r) in zip(idx, drive)]) if idx else np.empty(0)
        self.driven[drive_idx] = True
        silenced = np.zeros(self.n, np.bool_)
        silenced[np.asarray(silence, np.int64)] = True
        k = self._coefficients()
        g = [self.params[c] for c in self.cls[self.graded]]
        counts = np.zeros((self.trials, self.n), np.int32)
        _advance(self.t, int(steps), self.delay, np.float32(self.dt), self.ptr, self.idx, self.weights,
                 self.sptr, self.sidx, self.slow_weights, self.cls, k["a_vv"], k["a_vx"], k["a_vs"], k["a_bias"],
                 np.float32(np.exp(-self.dt / TAU)), np.float32(np.exp(-self.dt / self.tau_slow)), k["theta"],
                 k["reset"], k["rfc"], k["graded"], k["depress"], k["recover"], self.graded.astype(np.int64),
                 np.array([p["gain"] for p in g], np.float32), np.array([p["release_at"] for p in g], np.float32),
                 np.array([p["max_release"] for p in g], np.float32), self.u, self.x, self.s, self.until,
                 self.pending, self.pending_slow, self.graded_input, self.release, self.rng, self.left, self.last,
                 drive_idx, drive_p, np.float32(self.w_poi), self.driven, silenced, counts,
                 np.zeros((self.trials, 0), np.int64) if timeline is None else timeline, int(bin_start), int(bin_steps))
        self.t += int(steps)
        return counts

    def run(self, seconds: float, drive=(), silence=(), tail: float = 0.0, seed: int = 0, bin: float = 0.01) -> Result:
        """From rest, drive neurons for `seconds`, then run `tail` seconds without the drive; the same
        Result as ShiuBrain.run. silence here also cuts every synapse onto the silenced neurons, as
        ShiuBrain's does."""
        self.reset(seed)
        saved = self.weights
        if len(silence):
            cut = np.zeros(self.n, bool)
            cut[np.asarray(silence, np.int64)] = True
            self.weights = np.where(cut[self.idx], np.float32(0), self.weights).astype(np.float32)
        try:
            drive_steps, tail_steps = int(round(seconds / self.dt)), int(round(tail / self.dt))
            bin_steps = max(1, int(round(bin / self.dt)))
            timeline = np.zeros((self.trials, -(-(drive_steps + tail_steps) // bin_steps)), np.int64)
            during = self._step(drive_steps, drive, silence, timeline, 0, bin_steps)
            after = self._step(tail_steps, (), silence, timeline, drive_steps, bin_steps)
        finally:
            self.weights = saved
        rates = during / seconds
        return Result(rates=rates.mean(0), trial_rates=rates,
                      after_rates=after / tail if tail > 0 else np.zeros_like(rates),
                      timeline=timeline / (bin_steps * self.dt), bin=bin_steps * self.dt)
