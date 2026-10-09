"""FlyvisNative's fast matrix-vector product gives exactly scipy's numbers, so the optic lobe's output,
and every experiment that used it, is unchanged. Needs flyvis and the network files; skipped without."""
from __future__ import annotations

import numpy as np
import pytest

from brainfly.data import has_data

pytest.importorskip("brainfly.vistrain")         # before flyvis: it points flyvis at brainfly's data
pytestmark = pytest.mark.skipif(not has_data(), reason="needs the network files: python -m brainfly download")


@pytest.fixture(scope="module")
def optic():
    from brainfly import FlyBrain
    from brainfly.optic import GRADED, MODEL, FlyvisNative

    brain = FlyBrain(batch=1, graded=GRADED, dt=0.002, refractory=0.004)
    return FlyvisNative(brain, model=MODEL)


def test_matvec_matches_scipy_bit_for_bit(optic):
    from brainfly.optic import matvec

    rng = np.random.default_rng(0)
    for x in (np.maximum(optic.V, 0), rng.random(optic.W.shape[1]), rng.normal(0, 3, optic.W.shape[1])):
        assert np.array_equal(matvec(optic.W, x), optic.W @ x)


def test_optic_lobe_output_is_unchanged(optic, monkeypatch):
    import brainfly.optic as module
    from brainfly.eye2d import Disk, direction

    def run():                                  # a dark disk sweeping across the left eye
        optic.reset()
        return np.array([optic.step(optic.contrast([Disk(direction(-40 + 4 * k, 0), np.radians(12))])) for k in range(25)])

    fast = run()
    monkeypatch.setattr(module, "matvec", lambda W, x: W @ x)
    np.testing.assert_array_equal(fast, run())


def test_the_shipped_eye_is_the_checkpoint_brainfly_ships():
    """The default eye's folder holds the shipped checkpoint's parameters, and the check tells models apart."""
    from pathlib import Path

    from brainfly import optic

    shipped = Path(optic.__file__).with_name("models") / optic.EYE.replace("/", "_") / "best_chkpt"
    folder = optic.ensure_model(optic.EYE)
    assert optic._same_parameters(folder / "chkpts" / "chkpt_00000", shipped)
    assert not optic._same_parameters(optic.ensure_model("flow/0000/001") / "best_chkpt", shipped)
