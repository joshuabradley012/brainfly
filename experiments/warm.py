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

A reset leaves every synapse undepressed, and the receptor synapses' slow component recovers over 33 s, so 6 s from a
reset leave it at 0.80 of its strength where it settles at 0.37, and the PNs firing 1.5 times their settled rate
(settle_check.py). A model whose `settling` attribute says {"rested": True} starts each settle with the receptor neurons'
synapses at their mean depression at their spontaneous rates (rest_depression), from which the antennal lobe settles
within about 2 s, and settles for settling["seconds"] (RESTED_SETTLE_S). A model carries the attribute in its cache, so
every run on it settles the same way; models without it (odor_probe44.py's and earlier) settle as they were built, 6 s
from the undepressed reset.
"""
from __future__ import annotations

import contextlib
import hashlib

import numpy as np

import odor_probe24 as p24
from brainfly.hybrid import HybridBrain

STATE = ("u", "x", "s", "until", "ad", "pending", "fpending", "pending_slow", "touched", "n_touched", "graded_input",
         "slow_graded_input", "_external_release", "external_input", "release", "driven", "left", "last", "left_s",
         "last_s", "left2", "last2", "presynaptic_state", "t")
SEED, SETTLE_S, RESTED_SETTLE_S = 440000, 6.0, 3.0


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


def resting_gain(b: HybridBrain) -> float:
    """The presynaptic gain with every trace at its resting start (1 without presynaptic inhibition)."""
    pres = b._presynaptic
    if pres is None:
        return 1.0
    a = np.maximum(np.asarray(pres["start"], float) - pres["offset"], 0.0)
    return float(1.0 / (1.0 + np.sum(pres["k"] * a ** pres["power"])))


def rest_depression(o, rec) -> dict:
    """The receptor neurons' fast and slow synapses (and a second pool, where their type has one) set to their mean
    depression at their spontaneous rates: at rate r, using (1 - f) g of what is left per spike (g the resting
    presynaptic gain, for the neurons whose depletion follows it) and recovering over tau, a pool keeps
    1 / (1 + r tau (1 - f) g) of its strength on average."""
    b = o.brain
    rate = np.zeros(b.n)
    for g, cells in rec.cells.items():
        rate[cells] = rec.spont[g]
    gain = np.ones(b.n)
    if b._presynaptic is not None:
        gain[b._presynaptic["depleting"]] = resting_gain(b)
    cells = np.flatnonzero(rate > 0)
    out = {}
    for c in np.unique(b.cls[cells]):
        sel = cells[b.cls[cells] == c]
        p = b.params[c]
        pools = (("fast", p["depression"], p["recovery"], b.left, b.last),
                 ("slow", p["slow_depression"], p["slow_recovery"] or p["recovery"], b.left_s, b.last_s),
                 ("second", p.get("depression2", 1.0) if p.get("share2", 0.0) > 0 else 1.0, p.get("recovery2", 1.0),
                  getattr(b, "left2", None), getattr(b, "last2", None)))
        for name, f, tau, left, last in pools:
            if left is not None and left.shape[1] and 0 < f < 1:
                strength = 1.0 / (1.0 + rate[sel] * tau * (1 - f) * gain[sel])
                left[:, sel], last[:, sel] = strength, b.t
                out[name] = round(float(strength.mean()), 4)
    return out


def settling(o, seconds=None, rested=None) -> tuple:
    """(seconds, rested): as given, else as the model's `settling` attribute says, else 6 s from the reset."""
    how = getattr(o, "settling", None) or {}
    rested = bool(how.get("rested", False)) if rested is None else rested
    seconds = how.get("seconds", RESTED_SETTLE_S if rested else SETTLE_S) if seconds is None else seconds
    return seconds, rested


def _settle(b: HybridBrain, o, rec, reset, seed: int, seconds: float, rested: bool) -> dict:
    reset(b, seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    if rested:
        rest_depression(o, rec)
    b.advance(int(round(seconds / b.dt)), drive=p24.spontaneous(rec))
    return snapshot(b)


def settle(o, rec, seed: int = SEED, seconds: float | None = None, rested: bool | None = None) -> dict:
    """The state after `seconds` of spontaneous activity from a reset with `seed` (see settling)."""
    seconds, rested = settling(o, seconds, rested)
    return _settle(o.brain, o, rec, HybridBrain.reset, seed, seconds, rested)


@contextlib.contextmanager
def settled(o, rec, seed: int = SEED, seconds: float | None = None, rested: bool | None = None):
    """Within the block, HybridBrain.reset(seed') restores the settled state with fresh streams from seed'."""
    state = settle(o, rec, seed, seconds, rested)
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
def tracking(o, rec, seed: int = SEED, seconds: float | None = None, rested: bool | None = None):
    """Within the block, HybridBrain.reset(seed') restores a settled state with fresh streams from seed', settling
    again (from a cold reset with `seed`; see settling) whenever the model's fingerprint has changed since the last
    settle."""
    seconds, rested = settling(o, seconds, rested)
    cold = HybridBrain.reset
    held = {"key": None, "state": None, "settles": 0}

    def warm_reset(self, seed_: int = 0) -> None:
        key = fingerprint(self)
        if key != held["key"]:
            held["key"], held["state"] = key, _settle(self, o, rec, cold, seed, seconds, rested)
            held["settles"] += 1
        cold(self, seed_)
        restore(self, held["state"], seed_)
    HybridBrain.reset = warm_reset
    try:
        yield held
    finally:
        HybridBrain.reset = cold
