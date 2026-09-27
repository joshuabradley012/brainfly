"""brainfly.jump: the TTM twitch's timing, shape and cap, and the calibrated jump leaving the ground."""
from __future__ import annotations

import numpy as np
import pytest

from brainfly import jump as J


def test_twitch_timing_shape_and_cap():
    t = np.arange(-2e-3, 40e-3, 1e-6)
    k = J.twitch(t)
    assert np.all(k[t <= 0] == 0)
    peak = J.RISE * np.log(1 + J.DECAY / J.RISE)                    # 2.7 ms after onset
    assert J.twitch(peak) == pytest.approx(1.0) and k.max() <= 1.0
    assert t[np.argmax(k)] == pytest.approx(peak, abs=2e-6)
    up = lambda f: t[np.argmax(k >= f)]
    assert 1.0e-3 < up(0.9) - up(0.1) < 1.8e-3                     # rises over about 1.3 ms
    late = t > 10e-3
    assert np.allclose(np.diff(np.log(k[late])) / 1e-6, -1 / J.DECAY, rtol=1e-2)   # then decays with DECAY
    assert J.twitch(20e-3) < 0.2                                   # mostly over by 20 ms

    a = J.activation(t, [0.0])
    assert np.all(a[t <= J.TTM_DELAY] == 0) and a[t > J.TTM_DELAY + 1e-4].min() > 0
    assert np.allclose(a, J.twitch(t - J.TTM_DELAY))
    burst = J.activation(t, [0.0, 0.5e-3, 1e-3, 1.5e-3])
    assert burst.max() == 1.0 and np.all(burst <= 1.0)             # summed, capped at 1
    assert np.all(J.activation(t, []) == 0)


@pytest.fixture(scope="module")
def jump():
    pytest.importorskip("flygym")
    return J.Jump()


def test_standing_fly_stays_put(jump):
    rec = jump.run({"L": [], "R": []}, seconds=0.01)
    assert not rec["summary"]["took_off"]
    assert np.abs(rec["com"] - rec["com"][0]).max() < 0.02          # mm
    assert rec["contact"][:, [1, 4]].all()


def test_bilateral_spike_lifts_the_fly_off(jump):
    rec = jump.run({"L": [0.0], "R": [0.0]}, seconds=0.015, tau_max=J.TAU_MAX)
    s = rec["summary"]
    assert s["took_off"] and s["takeoff_ms"] < 15.0
    assert not rec["contact"][-1].any()
    assert rec["thorax"][-1, 2] > rec["thorax"][0, 2] + 1.0         # risen more than 1 mm
    assert 0.3 < s["launch_speed_m_s"] < 0.7
