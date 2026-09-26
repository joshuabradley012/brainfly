"""Leaky integrate-and-fire simulation of the MaleCNS connectome.

Dynamics follow ornata/fly (fly64/model.py) so results are comparable:
    v <- exp(-dt/tau) v + gain * W @ spikes + tonic + noise + eye input
    v >= 1 -> spike, reset to 0
tonic/gain/noise are hand-calibrated, not measured. fly64 used tonic 0.18,
gain 1.5, which parks every neuron at threshold (0.18 / (1 - 0.82) = 1.0) so
the network ticks on its own. inject.py showed tonic 0.14, gain 3.0 keeps
descending neurons quiet at rest (~1 Hz) while LC4/LPLC2 -> DNp01 and
LC10a -> DNa02 signals still get through, ipsilaterally.

Two optional departures from that model, both off by default:
* cell_params: tau, threshold, tonic and gain per cell type or superclass
  instead of one value for the whole brain.
* graded: cell types simulated as graded (non-spiking) neurons, like the
  photoreceptors and lamina neurons of a real fly. A graded neuron integrates
  the same way but never spikes; it releases transmitter continuously, and its
  synapses pass on the change in release from its resting level:
      out = clip(graded_gain * (v - v_rest), -graded_release, 1 - graded_release)
  in the units of a spike per 20 ms step (1 = as much as one spike), scaled to
  the step length so it means the same at any dt. A drop below rest reaches its
  targets too, which a silent spiking neuron can't signal: that is how a light
  increment, which hyperpolarises the lamina, gets through.

batch > 1 runs that many independent flies (same wiring, own voltages and
noise) in lock-step; on a GPU one sparse multiply serves them all, so 8 flies
cost about as much as 1-2.
"""
from __future__ import annotations

import os
from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import DATA, ensure_data


PARAMS = ("tau", "threshold", "tonic", "gain")   # settable per cell type (cell_params)


@numba.njit(nogil=True, parallel=True)
def _propagate(indptr, indices, weights, sources, amounts, n):
    """Sum the outgoing weights (CSC columns) of every source neuron, each scaled by
    its amount (1 for a spike, the release change for a graded neuron).
    Each thread scatters into its own buffer; buffers are summed at the end."""
    threads = numba.get_num_threads()
    partial = np.zeros((threads, n), np.float32)
    chunk = (len(sources) + threads - 1) // threads
    for t in numba.prange(threads):
        acc = partial[t]
        for k in range(t * chunk, min(len(sources), (t + 1) * chunk)):
            j = sources[k]
            a = amounts[k]
            for e in range(indptr[j], indptr[j + 1]):
                acc[indices[e]] += weights[e] * a
    current = np.zeros(n, np.float32)
    for i in numba.prange(n):
        s = np.float32(0.0)
        for t in range(threads):
            s += partial[t, i]
        current[i] = s
    return current


def cuda_available() -> bool:
    try:
        import cupy
        return cupy.cuda.runtime.getDeviceCount() > 0
    except Exception:
        return False


class FlyBrain:
    """device: "cpu" (numba), "cuda" (CuPy, NVIDIA GPU) or "auto"; defaults to
    $FLY_DEVICE, else "cpu". Both run the same model; the noise streams differ,
    so individual spikes differ between devices but statistics match.

    batch: number of independent flies. Voltages are (n, batch). With batch 1,
    step() returns the fired neuron indices; with batch > 1, a list of them,
    one array per fly. Inputs broadcast: an amount can be a number (same for
    every fly) or an array of length batch (one per fly)."""
    dt = 0.020
    tau = 0.100
    gain = 3.0
    tonic = 0.14            # calibrated at dt = 0.020; rescaled for other steps (see __init__)
    threshold = 1.0
    noise_hz = 1.2
    noise_amp = 0.22
    eye_gain = 0.62
    # Graded neurons, hand-set: eyepath.py's strongest setting that kept the network at rest.
    graded_gain = 0.15      # release change per unit of voltage away from rest
    graded_release = 0.3    # release at rest, so the most a drop below rest can take away

    def __init__(self, data: Path | str | None = None, seed: int = 64, device: str | None = None, batch: int = 1,
                 dt: float | None = None, sensory_input: bool = True, refractory: float = 0.0,
                 cell_params: dict[str, dict[str, float]] | None = None, graded: list[str] | tuple = (),
                 fill_retina: bool = False):
        """data: folder with brain.npz and weights.npz (default $FLY_DATA, else ~/fly-data).
        If they aren't there, the prebuilt brain is downloaded into it first (~260 MB, once).

        dt: step length in seconds (default 0.020). tonic is rescaled so a silent
        neuron settles at the same voltage as in the calibrated 20 ms model, and graded
        release is per 20 ms, so it carries over. Eye input, as in the original model, is
        added once per step.

        sensory_input: False removes every synapse onto sensory neurons (any superclass
        containing "sensory"), so they fire only from noise and what you inject. With
        True (the original model), olfactory receptor neurons excite each other into a
        runaway loop and sit near maximum rate at rest, so odours add nothing.

        refractory: seconds a neuron is held at 0 after it spikes (0 = none; at 20 ms
        steps the step itself already caps rates at 50 Hz).

        cell_params: {cell type or superclass: {"tau": s, "threshold": v, "tonic": v, "gain": x}},
        overriding the whole-brain value for those neurons (tonic is per 20 ms step, like
        the default). Later entries win where they overlap, so list broad classes first.
        Without cell_params the model is exactly the original.

        graded: cell types or superclasses simulated as graded (non-spiking) neurons, e.g.
        ["R1-6", "R7", "R8", "L1", "L2", "L3", "L4", "L5"] for the retina and lamina. Graded
        photoreceptors want a signed contrast drive (Eyes.contrast) rather than Eyes.drive,
        since they rest at the background they are adapted to.

        fill_retina: add a virtual photoreceptor bundle to each lamina column whose R1-6 input
        MaleCNS lost at the edge of its volume (about half of them), wired like the intact
        columns (brainfly.retina; needs the raw MaleCNS tables). The bundles are neurons
        n, n+1, ... of type R1-6; self.filled says what was added. Imputed, not observed."""
        device = device or os.environ.get("FLY_DEVICE", "cpu")
        if device == "auto":
            device = "cuda" if cuda_available() else "cpu"
        if device not in ("cpu", "cuda"):
            raise ValueError(f"device must be cpu, cuda or auto, not {device!r}")
        self.device = device
        self.batch = int(batch)
        if dt is not None:
            self.dt = float(dt)
        self.refractory_steps = int(round(refractory / self.dt))
        self.sensory_input = sensory_input
        data = ensure_data(data)
        meta = np.load(data / "brain.npz")
        W = sparse.load_npz(data / "weights.npz")
        self.visual = meta["visual"]
        self.azimuth = meta["azimuth"]  # -1 far left ... +1 far right
        self.cell_type = meta["cell_type"]
        self.side = meta["side"]
        self.positions = meta["positions"] if "positions" in meta.files else None
        self.superclass = meta["superclass"] if "superclass" in meta.files else None
        self.groups = {k.removeprefix("group_"): meta[k] for k in meta.files if k.startswith("group_")}
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
        if not sensory_input:
            if self.superclass is None:
                raise RuntimeError("brain.npz has no superclass; run `brainfly build`")
            sensory = np.char.find(self.superclass.astype(str), "sensory") >= 0
            W = sparse.diags((~sensory).astype(np.float32)) @ W.tocsr()   # rows = postsynaptic
        if device == "cuda":
            import cupy
            from cupyx.scipy import sparse as cusparse
            self.xp = cupy
            self._W = cusparse.csr_matrix(W.tocsr().astype(np.float32))  # rows = postsynaptic
        else:
            self.xp = np
        W = W.tocsc()
        self.n = W.shape[0]
        self.indptr, self.indices, self.weights = W.indptr, W.indices, W.data
        self._visual = self.xp.asarray(self.visual)
        cell_params = cell_params or {}
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
        self.tonic = self.tonic * (1 - np.exp(-self.dt / self.tau)) / (1 - np.exp(-0.020 / self.tau))
        self.decay = np.float32(np.exp(-self.dt / self.tau))
        # graded release is per 20 ms step (in spike units); scale it to this step
        self._release_scale = None if self.dt == 0.020 else np.float32(self.dt / 0.020)
        if np.ndim(self.gain):
            self.gain = self.gain.astype(np.float32)   # same arithmetic as the scalar, so defaults reproduce exactly
        for name in ("threshold", "tonic", "gain", "decay"):
            if np.ndim(getattr(self, name)):
                setattr(self, name, self.xp.asarray(getattr(self, name)))
        self.graded = self.cells(list(graded)) if graded else np.empty(0, np.int64)
        self._graded = self.xp.asarray(self.graded) if len(self.graded) else None
        self._spiking = None
        if self._graded is not None:
            spiking = np.ones((self.n, 1), bool)
            spiking[self.graded] = False
            self._spiking = self.xp.asarray(spiking)
        self.reset(seed)

    def reset(self, seed: int | None = None) -> None:
        """Silence the network (all voltages 0, no spikes) and restart the noise.
        Graded neurons start at their resting voltage, releasing at their resting level."""
        xp = self.xp
        self.rng = xp.random.default_rng(seed)
        self.v = xp.zeros((self.n, self.batch), xp.float32)
        self.fired = xp.empty(0, xp.int64)   # flat indices into v
        self.steps = 0
        # step of each neuron's last spike, for the refractory period
        self.last_spike = xp.full((self.n, self.batch), -10**6, xp.int32) if self.refractory_steps else None
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
        """Neurons whose cell type is in `types`. A superclass name
        ("descending_neuron", "visual_projection", ...) selects the whole class."""
        mask = np.isin(self.cell_type, types)
        if self.superclass is not None:
            mask |= np.isin(self.superclass, types)
        if side:
            mask &= self.side == side
        return np.flatnonzero(mask)

    def _amount(self, amount):
        """A number, or one value per fly, shaped to broadcast over v[idx]."""
        a = self.xp.asarray(amount, dtype=self.xp.float32)
        return a if a.ndim == 0 else a.reshape(1, -1)

    def stimulate(self, idx: np.ndarray, amount) -> None:
        """Add voltage to these neurons right now (before the next step)."""
        self.v[self.xp.asarray(idx)] += self._amount(amount)

    def set_graded(self, idx: np.ndarray, values) -> None:
        """Replace these graded neurons' release change for the next step, e.g. with the output of
        brainfly.optic.FlyvisOpticLobe. values: one per neuron, or (neurons, batch), per 20 ms
        like self.graded_out."""
        idx = np.asarray(idx)
        rows = np.searchsorted(self.graded, idx)
        if len(idx) and (rows.max() >= len(self.graded) or not np.array_equal(self.graded[rows], idx)):
            raise ValueError("set_graded: not all of these neurons are graded")
        vals = self.xp.asarray(values, dtype=self.xp.float32)
        self.graded_out[self.xp.asarray(rows)] = vals[:, None] if vals.ndim == 1 else vals

    def synaptic_input(self, fired):
        """Input current (n, batch) from the flat spike indices of the last step, plus the
        graded neurons' release changes (self.graded_out) from the same step."""
        xp, B = self.xp, self.batch
        release = None
        if self._graded is not None:
            release = self.graded_out if self._release_scale is None else self.graded_out * self._release_scale
        if self.device == "cuda":
            spikes = xp.zeros((self.n, B), xp.float32)
            spikes.ravel()[fired] = 1.0
            if self._graded is not None:
                spikes[self._graded] = release
            if B == 1:
                return (self._W @ spikes[:, 0])[:, None]
            return self._W @ spikes
        rows, cols = np.divmod(fired, B)
        columns = []
        for b in range(B):
            sources = rows[cols == b]
            amounts = np.ones(len(sources), np.float32)
            if self._graded is not None:
                sources = np.concatenate([sources, self.graded])
                amounts = np.concatenate([amounts, release[:, b]])
            columns.append(_propagate(self.indptr, self.indices, self.weights, sources, amounts, self.n))
        return np.column_stack(columns)

    def step(self, eye_drive: np.ndarray | None = None, inject=()):
        """Advance one step (dt, 20 ms by default). eye_drive: 0..1 per photoreceptor (len(self.visual)), or
        (len(self.visual), batch), signed contrast for graded photoreceptors; inject: (neuron
        indices, extra voltage) pairs added this step. Returns the indices of the neurons that
        fired (NumPy): one array with batch 1, else a list with one array per fly. Graded
        neurons never fire; their output this step is in self.graded_out."""
        xp, B = self.xp, self.batch
        current = self.synaptic_input(self.fired) * self.gain
        self.v *= self.decay
        self.v += current + self.tonic
        self.v += (self.rng.random((self.n, B)) < self.noise_hz * self.dt) * np.float32(self.noise_amp)
        if eye_drive is not None:
            drive = xp.asarray(eye_drive, dtype=xp.float32)
            self.v[self._visual] += (drive[:, None] if drive.ndim == 1 else drive) * self.eye_gain
        for idx, amount in inject:
            self.v[xp.asarray(idx)] += self._amount(amount)
        if self.refractory_steps:
            self.v[(self.steps - self.last_spike) <= self.refractory_steps] = 0.0
        above = self.v >= self.threshold
        if self._graded is not None:
            above &= self._spiking
            self.graded_out = xp.clip(self.graded_gain * (self.v[self._graded] - self._graded_rest()),
                                      -self.graded_release, 1 - self.graded_release).astype(xp.float32)
        fired = xp.flatnonzero(above)
        self.v.ravel()[fired] = 0.0
        if self.refractory_steps:
            self.last_spike.ravel()[fired] = self.steps
        self.fired = fired
        self.steps += 1
        flat = fired if xp is np else fired.get()
        if B == 1:
            return flat
        rows, cols = np.divmod(flat, B)
        order = np.argsort(cols, kind="stable")
        return np.split(rows[order], np.cumsum(np.bincount(cols, minlength=B))[:-1])
