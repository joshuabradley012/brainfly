"""Settled starts: runs that begin from a state the brain has already settled into, instead of from the reset.

Every run in the olfaction experiments resets the brain and lets it settle for 1-2 s before it measures, and that window
isn't settled: the antennal lobe's local neurons still fire about a quarter above their steady rate and its projection
neurons at half theirs (odor_offset_check.py), which inflates the local neurons' odor response (odor_warm_check.py).
Flies meet an odor from a settled state. Here the state of every trial is taken once after a long settle and put back
at each reset, with fresh random streams from the reset's own seed, so runs keep their own noise.

    with warm.settled(o, rec):                # every HybridBrain.reset inside starts from the settled state
        ...                                   # the experiments' measures, unchanged

    with warm.tracking(o, rec):               # the same, settling again whenever the model has changed since
        ...                                   # (biases, weights, types, presynaptic inhibition), as in a build

It lives outside brainfly/hybrid.py so that the cached models (brain_cache.py, keyed on every loaded module's code)
stay valid.
"""
from __future__ import annotations

import contextlib
import hashlib

import numpy as np

import odor_probe24 as p24
from brainfly.hybrid import HybridBrain

STATE = ("u", "x", "s", "until", "ad", "pending", "fpending", "pending_slow", "touched", "n_touched", "graded_input",
         "slow_graded_input", "_external_release", "external_input", "release", "driven", "left", "last", "left_s",
         "last_s", "presynaptic_state", "t")
SEED, SETTLE_S = 440000, 6.0


def snapshot(b: HybridBrain) -> dict:
    """Every trial's state as it stands (copies)."""
    return {k: (getattr(b, k).copy() if isinstance(getattr(b, k), np.ndarray) else getattr(b, k)) for k in STATE}


def restore(b: HybridBrain, state: dict, seed: int) -> None:
    """Put a snapshot back (into the arrays in place where their shapes match, as reset clears _external_release in
    place) and give every trial a fresh random stream from seed, as HybridBrain.reset does."""
    for k, v in state.items():
        now = getattr(b, k)
        if isinstance(v, np.ndarray) and isinstance(now, np.ndarray) and now.shape == v.shape:
            now[...] = v
        else:
            setattr(b, k, v.copy() if isinstance(v, np.ndarray) else v)
    b.rng = np.random.SeedSequence(seed).generate_state(b.trials, dtype=np.uint64)


def settle(o, rec, seed: int = SEED, seconds: float = SETTLE_S) -> dict:
    """The state after `seconds` of spontaneous activity from a reset with `seed`."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(seconds / b.dt)), drive=p24.spontaneous(rec))
    return snapshot(b)


@contextlib.contextmanager
def settled(o, rec, seed: int = SEED, seconds: float = SETTLE_S):
    """Within the block, HybridBrain.reset(seed') restores the settled state with fresh streams from seed'."""
    state = settle(o, rec, seed, seconds)
    cold = HybridBrain.reset

    def warm_reset(self, seed: int = 0) -> None:
        cold(self, seed)
        restore(self, state, seed)
    HybridBrain.reset = warm_reset
    try:
        yield state
    finally:
        HybridBrain.reset = cold


def fingerprint(b: HybridBrain) -> tuple:
    """What a settled state depends on: the biases (hashed), the weight arrays (by identity; they're replaced, not edited,
    when changed), the types' parameters and the presynaptic inhibition's settings."""
    bias = hashlib.md5(np.ascontiguousarray(b.bias).tobytes()).hexdigest() if b.bias is not None else None
    pres = None if b._presynaptic is None else repr({k: np.asarray(v).tolist() for k, v in b._presynaptic.items()
                                                    if k in ("k", "offset", "decay", "start", "power", "source")})
    return bias, id(b.weights), id(b.slow_weights), id(b.gap_mv), repr(b.types), pres


@contextlib.contextmanager
def tracking(o, rec, seed: int = SEED, seconds: float = SETTLE_S):
    """Within the block, HybridBrain.reset(seed') restores a settled state with fresh streams from seed', settling
    again (from a cold reset with `seed`) whenever the model's fingerprint has changed since the last settle."""
    cold = HybridBrain.reset
    held = {"key": None, "state": None, "settles": 0}

    def warm_reset(self, seed_: int = 0) -> None:
        key = fingerprint(self)
        if key != held["key"]:
            cold(self, seed)
            self.set_release(o.s.ol.neurons, o.s.silent)
            self.advance(int(round(seconds / self.dt)), drive=p24.spontaneous(rec))
            held["key"], held["state"] = key, snapshot(self)
            held["settles"] += 1
        cold(self, seed_)
        restore(self, held["state"], seed_)
    HybridBrain.reset = warm_reset
    try:
        yield held
    finally:
        HybridBrain.reset = cold
