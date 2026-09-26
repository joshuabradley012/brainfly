"""FlyBrain: the MaleCNS connectome as a network of leaky integrate-and-fire neurons.

Every step of length dt, each neuron's voltage decays with a 100 ms time constant and gains the
synaptic input from the last step's spikes, a constant tonic drive, random noise kicks and, for
photoreceptors, the light:

    v <- exp(-dt/tau) v + gain * W @ spikes + tonic + noise + eye input,  spike and reset to 0 at v >= 1

W is brainfly.build's matrix: synapse counts, negative for inhibitory transmitters, each neuron's
inputs scaled to at most one unit in total. The recipe is Fly64's (github.com/ornata/fly),
implemented independently here. The constants are set by hand, not measured: Fly64's tonic 0.18
with gain 1.5 holds every neuron at threshold (0.18 / (1 - exp(-0.2)) = 1.0), so the network
fires on its own; tonic 0.14 with gain 3.0 keeps descending neurons near 1 Hz at rest while
driving the looming detectors still reaches the giant fiber (DNp01) on the same side.

Options, all off by default (see FlyBrain):
* cell_params: a time constant, threshold, tonic drive and gain per cell type or superclass.
* graded: neurons simulated as graded, like the real retina and lamina. They integrate the same
  way but never spike; each passes on the change in its transmitter release from rest,
      out = clip(graded_gain * (v - v_rest), -graded_release, 1 - graded_release),
  in units of one spike per 20 ms, scaled to the step so it means the same at any dt. A drop
  below rest reaches the targets too, which a silent spiking neuron can't signal: that is how a
  light increment, which hyperpolarises the lamina, gets through.
* fill_retina, rewire, sensory_input, refractory, dt: see FlyBrain.

With batch > 1 the same wiring runs that many flies at once, each with its own voltages and noise;
on a GPU one sparse product serves them all.
"""
from __future__ import annotations

import os
from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import ensure_data

PARAMS = ("tau", "threshold", "tonic", "gain")   # the parameters cell_params can set per cell type


def cuda_available() -> bool:
    """Whether CuPy is installed and sees an NVIDIA GPU."""
    try:
        import cupy
    except ImportError:
        return False
    try:
        return cupy.cuda.runtime.getDeviceCount() > 0
    except Exception:
        return False


def _rewire(W, seed: int):
    """W (rows postsynaptic) with every synapse given a random target, each target's inputs then
    rescaled to their original total absolute weight (FlyBrain's rewire option)."""
    W = W.tocoo()
    before = np.bincount(W.row, weights=np.abs(W.data), minlength=W.shape[0])
    rows = np.random.default_rng(seed).permutation(W.row)
    R = sparse.csr_matrix((W.data, (rows, W.col)), shape=W.shape)
    after = np.asarray(abs(R).sum(1)).ravel()
    scale = np.where(after > 0, before / np.maximum(after, 1e-30), 0.0)
    return (sparse.diags(scale.astype(np.float32)) @ R).astype(W.dtype).tocsr()


SHARES = 14    # _scatter's split of the sources; fixed so float sums don't depend on the thread count


@numba.njit(nogil=True, parallel=True, cache=True)
def _scatter(indptr, targets, weights, sources, amounts, n):
    """Input to each of n neurons from `sources`, the columns of a CSC matrix, each column scaled
    by its amount (1 for a spike, the release change for a graded neuron). The sources are split
    into SHARES contiguous shares, each accumulated into its own row, and the rows are added in
    order, so the sum depends on neither scheduling nor the number of threads. (14 is the thread
    count of the machine the recorded results came from, which keeps them bit for bit.)"""
    rows = np.zeros((SHARES, n), np.float32)
    share = (len(sources) + SHARES - 1) // SHARES
    for w in numba.prange(SHARES):
        row = rows[w]
        for k in range(w * share, min(len(sources), (w + 1) * share)):
            col = sources[k]
            amount = amounts[k]
            for e in range(indptr[col], indptr[col + 1]):
                row[targets[e]] += weights[e] * amount
    out = np.zeros(n, np.float32)
    for i in numba.prange(n):
        total = np.float32(0.0)
        for w in range(SHARES):
            total += rows[w, i]
        out[i] = total
    return out


class FlyBrain:
    """The whole MaleCNS network, stepped dt at a time on the CPU (numba) or an NVIDIA GPU (CuPy).

    One or more flies share the wiring (batch); voltages have shape (n, batch). Inputs broadcast:
    an amount is a number for every fly or an array with one value per fly. step() returns the
    neurons that fired: an array of neuron indices with batch 1, else a list of arrays, one per fly.
    The CPU and GPU run the same model but draw different noise, so their spikes differ in detail."""

    # Hand-set constants, per 20 ms step unless noted (see the module docstring).
    dt = 0.020               # step, s
    tau = 0.100              # membrane time constant, s
    gain = 3.0               # voltage per unit of synaptic input
    tonic = 0.14             # constant drive; rescaled for other steps so rest stays put
    threshold = 1.0
    noise_hz = 1.2           # rate of random voltage kicks per neuron
    noise_amp = 0.22         # size of each kick
    eye_gain = 0.62          # voltage per unit of eye input
    graded_gain = 0.15       # graded neurons: release change per unit of voltage from rest
    graded_release = 0.3     # graded neurons: release at rest, the most a drop can remove

    def __init__(self, data: Path | str | None = None, seed: int = 64, device: str | None = None, batch: int = 1,
                 dt: float | None = None, sensory_input: bool = True, refractory: float = 0.0,
                 cell_params: dict[str, dict[str, float]] | None = None, graded: list[str] | tuple = (),
                 fill_retina: bool = False, rewire: int | None = None):
        """data: the folder with brain.npz and weights.npz (default $FLY_DATA, else ~/fly-data);
        the prebuilt files are fetched into it on first use (~260 MB).

        seed: the noise seed reset() starts from.

        device: "cpu", "cuda" or "auto" (default $FLY_DEVICE, else "cpu").

        batch: how many flies to run at once.

        dt: step length in seconds (default 0.020). tonic is rescaled so a silent neuron settles
        where it does at 20 ms, and graded release is per 20 ms, so it carries over. Eye input is
        added once per step, as in the original model.

        sensory_input: False removes every synapse onto sensory neurons (superclasses containing
        "sensory"), so they fire only from noise and injected input. With True, the original model,
        olfactory receptor neurons excite each other into a runaway and sit near their top rate at
        rest, so odours add nothing.

        refractory: seconds a neuron is held at 0 after a spike (0 = none; at 20 ms steps the step
        itself caps rates at 50 Hz).

        cell_params: {cell type or superclass: {"tau": s, "threshold": v, "tonic": v, "gain": x}},
        replacing the whole-brain value for those neurons (tonic per 20 ms step, like the default).
        Later entries win where they overlap, so list broad classes first. Without cell_params the
        model is exactly the original.

        graded: cell types or superclasses simulated as graded neurons, e.g. ["R1-6", "R7", "R8",
        "L1", "L2", "L3", "L4", "L5"] for the retina and lamina. Graded photoreceptors want a signed
        contrast (Eyes.contrast) rather than Eyes.drive, as they rest at the background they are
        adapted to.

        fill_retina: add a virtual photoreceptor bundle to each lamina column whose R1-6 input
        MaleCNS lost at the edge of its volume (about half of them), wired like the intact
        columns (brainfly.retina; needs the raw MaleCNS tables). The bundles are neurons
        n, n+1, ... of type R1-6; self.filled says what was added. Imputed, not observed.

        rewire: a seed for a null model of the wiring. Every connection keeps its presynaptic
        neuron, sign and weight but gets a random postsynaptic target, so each neuron keeps its
        number of inputs and outputs (up to the 0.3% of connections that land on an already
        connected pair and merge); then each neuron's inputs are rescaled to their original total
        absolute weight, so only the routing changes (0.6% of the original pairs stay connected)."""
        choice = device or os.environ.get("FLY_DEVICE", "cpu")
        if choice == "auto":
            choice = "cuda" if cuda_available() else "cpu"
        if choice not in ("cpu", "cuda"):
            raise ValueError(f"device must be cpu, cuda or auto, not {choice!r}")
        self.device = choice
        self.batch = int(batch)
        if dt is not None:
            self.dt = float(dt)
        self.refractory_steps = round(refractory / self.dt)
        self.sensory_input = sensory_input
        W = self._load(ensure_data(data), fill_retina)
        if not sensory_input:
            if self.superclass is None:
                raise RuntimeError("brain.npz has no superclass; rebuild it with `brainfly build`")
            deaf = np.char.find(self.superclass.astype(str), "sensory") >= 0
            W = sparse.diags((~deaf).astype(np.float32)) @ W.tocsr()     # rows are postsynaptic
        if rewire is not None:
            W = _rewire(W, rewire)
        self.xp = np
        if self.device == "cuda":
            import cupy
            from cupyx.scipy import sparse as cusparse

            self.xp = cupy
            self._W = cusparse.csr_matrix(W.tocsr().astype(np.float32))
        by_source = W.tocsc()                                               # columns are presynaptic
        self.n = by_source.shape[0]
        self.indptr, self.indices, self.weights = by_source.indptr, by_source.indices, by_source.data
        self._visual = self.xp.asarray(self.visual)
        self._set_parameters(cell_params or {}, graded)
        self.graded = self.cells(list(graded)) if graded else np.empty(0, np.int64)
        self._graded = self.xp.asarray(self.graded) if len(self.graded) else None
        self._set_rows = None                      # set_graded's last neurons and their rows in graded_out
        self._spiking = None
        if self._graded is not None:
            spiking = np.ones((self.n, 1), bool)
            spiking[self.graded] = False
            self._spiking = self.xp.asarray(spiking)
        self.reset(seed)

    def _load(self, data: Path, fill_retina: bool):
        """Read brain.npz into attributes and return weights.npz's matrix (rows postsynaptic),
        with the retina filled in if asked."""
        info = np.load(data / "brain.npz")
        W = sparse.load_npz(data / "weights.npz")
        self.visual = info["visual"]                  # photoreceptor rows
        self.azimuth = info["azimuth"]                # their 1-D eye azimuth, -1 far left ... +1 far right
        self.cell_type = info["cell_type"]
        self.side = info["side"]
        self.positions = info["positions"] if "positions" in info.files else None
        self.superclass = info["superclass"] if "superclass" in info.files else None
        self.groups = {k.removeprefix("group_"): info[k] for k in info.files if k.startswith("group_")}
        self.filled = None
        if fill_retina:
            from .retina import fill
            n0 = W.shape[0]
            W, self.filled, added = fill(W, data)
            V = W.shape[0] - n0
            self.visual = np.concatenate([self.visual, n0 + np.arange(V)])
            self.azimuth = np.concatenate([self.azimuth, self.filled.azimuth])
            self.cell_type = np.concatenate([self.cell_type.astype(str), added["cell_type"]])
            self.side = np.concatenate([self.side.astype(str), added["side"]])
            self.superclass = np.concatenate([self.superclass.astype(str), added["superclass"]])
            if self.positions is not None:
                self.positions = np.concatenate([self.positions, np.full((V, 3), np.nan, self.positions.dtype)])
        return W

    def _set_parameters(self, cell_params: dict, graded) -> None:
        """Per-cell-type overrides, the tonic drive and decay for this dt, and the release scale."""
        for key, values in cell_params.items():
            if set(values) - set(PARAMS):
                raise ValueError(f"unknown cell parameters for {key!r}: {sorted(set(values) - set(PARAMS))}; "
                                 f"known: {list(PARAMS)}")
        for key in [*cell_params, *graded]:
            if not len(self.cells([key])):
                raise ValueError(f"no neurons of cell type or superclass {key!r}")
        for name in PARAMS:
            overrides = [(key, values[name]) for key, values in cell_params.items() if name in values]
            if overrides:
                per_neuron = np.full((self.n, 1), getattr(self, name))   # (n, 1): broadcasts over the flies
                for key, value in overrides:
                    per_neuron[self.cells([key])] = value
                setattr(self, name, per_neuron)
        # the tonic drive that holds a silent neuron where it rests at 20 ms steps, and the decay per step
        self.tonic = self.tonic * (1 - np.exp(-self.dt / self.tau)) / (1 - np.exp(-0.020 / self.tau))
        self.decay = np.float32(np.exp(-self.dt / self.tau))
        # graded release is per 20 ms step (in spike units); scale it to this step
        self._release_scale = None if self.dt == 0.020 else np.float32(self.dt / 0.020)
        if np.ndim(self.gain):
            self.gain = self.gain.astype(np.float32)   # same arithmetic as the scalar, so defaults reproduce exactly
        for name in ("threshold", "tonic", "gain", "decay"):
            if np.ndim(getattr(self, name)):
                setattr(self, name, self.xp.asarray(getattr(self, name)))

    def reset(self, seed: int | None = None) -> None:
        """Start over: every voltage at 0, no spikes, the noise restarted from `seed`. Graded
        neurons start at their resting voltage, releasing at their resting level."""
        xp = self.xp
        self.rng = xp.random.default_rng(seed)
        self.v = xp.zeros((self.n, self.batch), xp.float32)
        self.fired = xp.empty(0, xp.int64)                    # flat indices into v of the last step's spikes
        self.steps = 0
        self.last_spike = None                                # the step of each neuron's last spike
        if self.refractory_steps:
            self.last_spike = xp.full((self.n, self.batch), -1_000_000, xp.int32)
        if self._graded is not None:
            self.v[self._graded] = self._graded_rest()
            # change in release from rest, per graded neuron (rows follow self.graded) and fly
            self.graded_out = xp.zeros((len(self.graded), self.batch), xp.float32)

    def rest(self):
        """Voltage a neuron settles at with no synaptic input (tonic plus the mean noise,
        against the leak): a number, or (n, 1) with per-cell-type parameters."""
        return (self.tonic + self.noise_amp * self.noise_hz * self.dt) / (1 - self.decay)

    def _graded_rest(self):
        rest = self.rest()
        return rest[self._graded] if np.ndim(rest) else rest

    def cells(self, types: list[str], side: str | None = None) -> np.ndarray:
        """Indices of the neurons whose cell type is in `types`; a superclass name there
        ("descending_neuron", "visual_projection", ...) takes the whole class. side: "L" or "R"."""
        chosen = np.isin(self.cell_type, types)
        if self.superclass is not None:
            chosen |= np.isin(self.superclass, types)
        if side:
            chosen &= self.side == side
        return np.flatnonzero(chosen)

    def _amount(self, amount):
        """An amount as float32: a scalar, or one value per fly shaped (1, batch)."""
        value = self.xp.asarray(amount, dtype=self.xp.float32)
        return value.reshape(1, -1) if value.ndim else value

    def stimulate(self, idx: np.ndarray, amount) -> None:
        """Add voltage to these neurons now, before the next step."""
        self.v[self.xp.asarray(idx)] += self._amount(amount)

    def set_graded(self, idx: np.ndarray, values) -> None:
        """Replace these graded neurons' release change for the next step, e.g. with the output of
        brainfly.optic.FlyvisNative. values: one per neuron, or (neurons, batch), per 20 ms like
        self.graded_out."""
        idx = np.asarray(idx)
        cached = self._set_rows                    # a loop sets the same neurons every step
        if cached is None or len(cached[0]) != len(idx) or not np.array_equal(cached[0], idx):
            rows = np.searchsorted(self.graded, idx)
            if len(idx) and (rows.max() >= len(self.graded) or not np.array_equal(self.graded[rows], idx)):
                raise ValueError("set_graded: not all of these neurons are graded")
            cached = self._set_rows = (idx.copy(), self.xp.asarray(rows))
        vals = self.xp.asarray(values, dtype=self.xp.float32)
        self.graded_out[cached[1]] = vals[:, None] if vals.ndim == 1 else vals

    def synaptic_input(self, fired):
        """Synaptic input (n, batch) from the last step: its spikes (flat indices into v), plus
        the graded neurons' release changes (self.graded_out)."""
        xp, B = self.xp, self.batch
        release = None
        if self._graded is not None:
            release = self.graded_out if self._release_scale is None else self.graded_out * self._release_scale
        if self.device == "cuda":
            activity = xp.zeros((self.n, B), xp.float32)
            activity.ravel()[fired] = 1.0
            if release is not None:
                activity[self._graded] = release
            return (self._W @ activity[:, 0])[:, None] if B == 1 else self._W @ activity
        neuron, fly = np.divmod(fired, B)
        per_fly = []
        for b in range(B):
            sources = neuron[fly == b]                        # spikes first, then the graded neurons
            amounts = np.ones(len(sources), np.float32)
            if release is not None:
                sources = np.concatenate([sources, self.graded])
                amounts = np.concatenate([amounts, release[:, b]])
            per_fly.append(_scatter(self.indptr, self.indices, self.weights, sources, amounts, self.n))
        return np.column_stack(per_fly)

    def step(self, eye_drive: np.ndarray | None = None, inject=()):
        """Advance one step of dt. eye_drive: input per photoreceptor (len(self.visual), or
        (len(self.visual), batch)): 0..1 from Eyes.drive, or a signed contrast for graded
        photoreceptors. inject: (neuron indices, extra voltage) pairs added this step. Returns the
        neurons that fired (see the class docstring); graded neurons' output is in
        self.graded_out."""
        xp, B = self.xp, self.batch
        current = self.synaptic_input(self.fired) * self.gain
        self.v *= self.decay
        self.v += current + self.tonic
        kicks = self.rng.random((self.n, B)) < self.noise_hz * self.dt
        self.v += kicks * np.float32(self.noise_amp)
        if eye_drive is not None:
            light = xp.asarray(eye_drive, dtype=xp.float32)
            if light.ndim == 1:
                light = light[:, None]
            self.v[self._visual] += light * self.eye_gain
        for idx, amount in inject:
            self.v[xp.asarray(idx)] += self._amount(amount)
        if self.refractory_steps:
            recovering = (self.steps - self.last_spike) <= self.refractory_steps
            self.v[recovering] = 0.0
        crossed = self.v >= self.threshold
        if self._graded is not None:
            crossed &= self._spiking
            self.graded_out = xp.clip(self.graded_gain * (self.v[self._graded] - self._graded_rest()),
                                      -self.graded_release, 1 - self.graded_release).astype(xp.float32)
        fired = xp.flatnonzero(crossed)
        self.v.ravel()[fired] = 0.0
        if self.refractory_steps:
            self.last_spike.ravel()[fired] = self.steps
        self.fired = fired
        self.steps += 1
        spikes = fired.get() if xp is not np else fired
        if B == 1:
            return spikes
        neuron, fly = np.divmod(spikes, B)
        return [neuron[fly == b] for b in range(B)]
