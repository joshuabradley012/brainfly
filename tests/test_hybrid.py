"""HybridBrain: Shiu's model when nothing is changed, graded units and the slow current as the
module describes them, and state that carries over from one call to the next."""
from __future__ import annotations

import numpy as np
import pytest
from scipy import sparse

from brainfly.data import has_data
from brainfly.hybrid import HybridBrain, _approach
from brainfly.shiu import TAU, T_MBR

DT = 1e-4


def small(edges, n, slow_edges=(), **kw) -> HybridBrain:
    """A HybridBrain on a network of n neurons named c0, c1, ..., with weights in mV (w_syn = 1)."""
    def matrix(e):
        pre, post, w = zip(*e) if e else ((), (), ())
        return sparse.csr_matrix((np.array(w, np.float32), (post, pre)), shape=(n, n))
    labels = {"cell_type": np.array([f"c{i}" for i in range(n)]), "side": np.array(["L"] * n),
              "superclass": np.array(["test"] * n)}
    return HybridBrain(matrix=matrix(edges), slow=matrix(list(slow_edges)) if slow_edges else None, labels=labels,
                       w_syn=1.0, **kw)


def test_defaults_match_brian2_step_for_step():
    """The six-neuron circuit of test_shiu_brian2.py, stepped one step at a time."""
    brian2 = pytest.importorskip("brian2")  # noqa: F841
    from test_shiu_brian2 import DRIVE_STEPS, DRIVEN, EDGES, KICK, N, STEPS, brian2_run

    steps, neuron = brian2_run(N, EDGES, DRIVEN, KICK, 1 / DT, DRIVE_STEPS * DT, (STEPS - DRIVE_STEPS) * DT)
    expected = np.zeros((STEPS, N), int)
    np.add.at(expected, (steps, neuron), 1)
    brain = small(EDGES, N, w_poi=KICK)
    actual = np.array([brain.advance(1, drive=[(DRIVEN, 1 / DT)] if t < DRIVE_STEPS else ())[0] for t in range(STEPS)])
    np.testing.assert_array_equal(actual, expected)


def random_circuit(seed=5, n=30):
    rng = np.random.default_rng(seed)
    edges = [(i, j, float(rng.normal(4, 9))) for i in range(n) for j in range(n) if rng.random() < 0.2]
    slow = [(i, j, float(rng.normal(-3, 2))) for i in range(n) for j in range(n) if rng.random() < 0.05]
    types = {"c3": {"unit": "graded", "gain": 4.0}, "c4": {"tau_m": 0.008, "bias": 3.0},
             "c5": {"threshold": 10.0, "refractory": 0.004, "scale": 0.5}}
    return edges, slow, types, n


def test_advancing_in_pieces_changes_nothing():
    edges, slow, types, n = random_circuit()
    drive = [(np.arange(4), 120.0)]
    whole = small(edges, n, slow, types=types, trials=3, w_poi=30.0)
    once = whole.advance(2000, drive)
    pieces = small(edges, n, slow, types=types, trials=3, w_poi=30.0)
    parts = sum(pieces.advance(k, drive) for k in (1, 7, 192, 800, 1000))
    assert once.sum() > 100, "the circuit should be active"
    np.testing.assert_array_equal(once, parts)
    for name in ("u", "x", "s", "until", "graded_input", "release", "rng"):
        np.testing.assert_array_equal(getattr(whole, name), getattr(pieces, name), err_msg=name)


def test_graded_release_and_its_effect_at_steady_state():
    """A graded neuron held at 20 mV releases gain x (20 - 7) Hz, and its target settles where that
    continuous input puts it."""
    brain = small([(0, 1, 10.0)], 2, types={"c0": {"unit": "graded", "bias": 20.0, "gain": 5.0}})
    brain.advance(8000)                                 # 0.8 s, 40 membrane time constants
    assert brain.release[0, 0] == pytest.approx(5.0 * (20.0 - 7.0), rel=1e-4)
    a_xx, a_vv, a_vx = np.exp(-DT / TAU), np.exp(-DT / T_MBR), _approach(TAU, T_MBR, DT)
    x = 10.0 * 65.0 * DT / (1 - a_xx)                   # x' = a_xx x + R dt at steady state
    assert brain.x[0, 1] == pytest.approx(x, rel=1e-3)
    assert brain.u[0, 1] == pytest.approx(a_vx * x / (1 - a_vv), rel=1e-3)
    assert brain.advance(1000).sum() == 0               # 3.3 mV, below threshold: nothing spikes


def test_slow_current_decays_with_its_own_time_constant_and_survives_spikes():
    brain = small([(1, 1, 0.0)], 2, slow_edges=[(0, 1, 5.0)], tau_slow=0.08, w_poi=100.0)
    brain.advance(1, drive=[([0], 1 / DT)])             # step 0: a kick past threshold
    assert brain.advance(1)[0, 0] == 1                  # step 1: neuron 0 fires
    brain.advance(18)                                   # its slow input lands at step 19
    assert brain.s[0, 1] == pytest.approx(5.0)
    brain.advance(100)
    assert brain.s[0, 1] == pytest.approx(5.0 * np.exp(-100 * DT / 0.08), rel=1e-5)
    assert brain.x[0, 1] == 0 and brain.u[0, 1] > 0
    before = float(brain.s[0, 1])
    brain.advance(1, drive=[([1], 1 / DT)])             # kick neuron 1 past threshold
    assert brain.advance(1)[0, 1] == 1                  # it fires, and its slow current only decays
    assert brain.s[0, 1] == pytest.approx(before * np.exp(-2 * DT / 0.08), rel=1e-5)


@pytest.mark.skipif(not has_data(), reason="needs the network files: python -m brainfly download")
def test_defaults_reproduce_shiubrain_on_the_connectome():
    """With a drive that fires on every step there is no randomness, so HybridBrain with nothing
    changed must give ShiuBrain's spikes exactly, on all of MaleCNS."""
    from brainfly.shiu import ShiuBrain

    shiu = ShiuBrain(trials=2)
    sugar = shiu.cells(["LB3b", "LB3c"], side="L")
    expected = shiu.run(0.05, drive=[(sugar, 1 / DT)], tail=0.02)
    actual = HybridBrain(trials=2).run(0.05, drive=[(sugar, 1 / DT)], tail=0.02)
    assert expected.trial_rates.sum() > 0
    np.testing.assert_array_equal(actual.trial_rates, expected.trial_rates)
    np.testing.assert_array_equal(actual.after_rates, expected.after_rates)
    np.testing.assert_array_equal(actual.timeline, expected.timeline)
    scale = np.random.default_rng(0).uniform(0.5, 2.0, shiu.n)     # and with a synapse scale per neuron
    expected = ShiuBrain(trials=2, scale=scale).run(0.05, drive=[(sugar, 1 / DT)], tail=0.02)
    actual = HybridBrain(trials=2, scale=scale).run(0.05, drive=[(sugar, 1 / DT)], tail=0.02)
    np.testing.assert_array_equal(actual.trial_rates, expected.trial_rates)
    np.testing.assert_array_equal(actual.after_rates, expected.after_rates)


def test_depression_follows_its_recurrence():
    """A depressing neuron fired every 10 ms: each spike carries the strength the recurrence
    s(1) = 1, s(k+1) = 1 - (1 - 0.78 s(k)) exp(-10 ms / 893 ms) predicts, and it reaches the target."""
    brain = small([(0, 1, 1.0)], 2, types={"c0": {"depression": 0.78, "recovery": 0.893}}, w_poi=100.0)
    strength, expected, landed = 1.0, [], []
    for k in range(12):
        brain.advance(1, drive=[([0], 1 / DT)])         # a kick; neuron 0 fires on the next step
        before = float(brain.x[0, 1])
        brain.advance(19)                               # its spike lands 18 steps after it
        landed.append(float(brain.x[0, 1]) - before * np.exp(-19 * DT / TAU))   # the old input decays 19 steps
        brain.advance(80)
        expected.append(strength)
        assert brain.left[0, 0] == pytest.approx(0.78 * strength, rel=1e-5)
        strength = 1 - (1 - 0.78 * strength) * np.exp(-100 * DT / 0.893)
    assert expected[-1] < 0.3, "twelve spikes at 100 Hz should depress the synapse deeply"
    np.testing.assert_allclose(landed, expected, rtol=1e-4)      # it lands on the last of those 19 steps


def test_setting_w_syn_is_the_same_as_building_with_it():
    edges, slow, types, n = random_circuit()
    built = small(edges, n, slow, types=types, trials=2)
    built.w_syn = 0.6
    fresh = HybridBrain(matrix=built_matrix(edges, n), slow=built_matrix(slow, n), types=types, trials=2, w_syn=0.6,
                        labels=built_labels(n))
    drive = [(np.arange(4), 150.0)]
    np.testing.assert_array_equal(built.advance(1500, drive), fresh.advance(1500, drive))
    assert built.w_poi == pytest.approx(250 * 0.6)


def built_matrix(edges, n):
    pre, post, w = zip(*edges)
    return sparse.csr_matrix((np.array(w, np.float32), (post, pre)), shape=(n, n))


def built_labels(n):
    return {"cell_type": np.array([f"c{i}" for i in range(n)]), "side": np.array(["L"] * n),
            "superclass": np.array(["test"] * n)}


def test_delivery_is_the_same_whether_or_not_the_target_lists_overflow():
    """Input waiting for delivery is found through a list of the targets that received some, or by
    scanning every neuron when that list overflows; both must give the same spikes."""
    edges, slow, types, n = random_circuit()
    drive = [(np.arange(4), 150.0)]
    listed = small(edges, n, types=types, trials=2, w_poi=30.0)
    scanned = small(edges, n, types=types, trials=2, w_poi=30.0)
    scanned.touched = np.zeros((2, scanned.delay, 1), np.int32)     # room for one target: nearly always overflows
    np.testing.assert_array_equal(listed.advance(3000, drive), scanned.advance(3000, drive))
    np.testing.assert_array_equal(listed.x, scanned.x)
    assert listed.advance(1000, drive).sum() > 50
