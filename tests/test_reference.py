"""FlyBrain's spikes under ten configurations, hashed: a change to any hash is a change to the model.

The hashes were recorded with the code that produced the experiments' recorded results, before it was
rewritten, and the rewrite reproduces them bit for bit. They don't depend on the number of threads
(brainfly.brain.SHARES); they could still differ on another CPU architecture if its compiler rounds
differently. Needs the network files (python -m brainfly download); skipped without them.
"""
from __future__ import annotations

import hashlib

import numpy as np
import pytest

from brainfly import FlyBrain
from brainfly.data import has_data
from brainfly.eyes import Eyes, blob_for
from brainfly.optic import GRADED as OPTIC

pytestmark = pytest.mark.skipif(not has_data(), reason="needs the network files: python -m brainfly download")
LAMINA = ["R1-6", "R7", "R8", "L1", "L2", "L3", "L4", "L5"]


def raster(brain: FlyBrain, steps: int, eye: str | None = "drive", inject: bool = False, graded=None) -> str:
    """sha256 (16 hex digits) of every step's spikes, and of graded release when there is any: a dark
    bar sweeping across the 1-D eye, optionally LC4 on the left kicked every third step, and
    optionally random release set on `graded` neurons each step."""
    brain.reset(7)
    eyes = Eyes(brain.azimuth)
    lc4 = brain.cells(["LC4"], side="L")
    rng = np.random.default_rng(3)
    h = hashlib.sha256()
    for s in range(steps):
        blobs = [blob_for(-110 + 45 * s * brain.dt, 30, 0.9)]
        drive = None if eye is None else eyes.contrast(blobs) if eye == "contrast" else eyes.drive(blobs)
        if graded is not None:
            brain.set_graded(graded, rng.normal(0, 0.2, len(graded)).astype(np.float32))
        fired = brain.step(drive, inject=[(lc4, 0.5)] if inject and s % 3 == 0 else ())
        for f in fired if isinstance(fired, list) else [fired]:
            h.update(np.asarray(f, np.int64).tobytes())
            h.update(b"|")
        if len(brain.graded):
            h.update(np.ascontiguousarray(brain.graded_out).tobytes())
    return h.hexdigest()[:16]


def overridden() -> FlyBrain:
    brain = FlyBrain()
    brain.tonic, brain.gain = 0.12, 4.0          # changed after construction, as experiments do
    return brain


CASES = {
    "default": (lambda: FlyBrain(), dict(steps=60, inject=True), "b346fde8814d390c"),
    "batch3": (lambda: FlyBrain(batch=3), dict(steps=60, inject=True), "bb2866d6cd411936"),
    "dt2ms": (lambda: FlyBrain(dt=0.002), dict(steps=120, inject=True), "fe1c9e1d268dc335"),
    "nosensory_refr": (lambda: FlyBrain(sensory_input=False, refractory=0.004, dt=0.002), dict(steps=120, inject=True),
                       "8222ac81cf8c1c21"),
    "override": (overridden, dict(steps=60, inject=True), "4946ee57b0570023"),
    "graded_lamina": (lambda: FlyBrain(batch=2, graded=LAMINA), dict(steps=60, eye="contrast"), "c79773b059b1965f"),
    "fill_optic": (lambda: FlyBrain(graded=OPTIC, fill_retina=True), dict(steps=40, eye="contrast"), "9d93d124745c4890"),
    "cell_params": (lambda: FlyBrain(batch=2, cell_params={"visual_projection": {"tau": 0.05, "threshold": 1.1, "tonic": 0.15,
                                                                                 "gain": 2.5}, "LC4": {"gain": 4.0}}),
                    dict(steps=60), "6c06cada70da5806"),
    "rewire": (lambda: FlyBrain(rewire=1), dict(steps=60), "2a6090d71806fd61"),
    "set_graded_2ms": (lambda: FlyBrain(batch=2, graded=OPTIC, dt=0.002, refractory=0.004), dict(steps=150, eye=None),
                       "b35596f81ba67334"),
}


@pytest.mark.parametrize("name", list(CASES))
def test_spikes_unchanged(name):
    make, kw, expected = CASES[name]
    brain = make()
    if name == "set_graded_2ms":
        kw = dict(kw, graded=brain.graded[::7])
    assert raster(brain, **kw) == expected
