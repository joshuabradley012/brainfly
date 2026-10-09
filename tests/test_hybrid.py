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
    for name in ("u", "x", "s", "until", "graded_input", "slow_graded_input", "release", "rng"):
        np.testing.assert_array_equal(getattr(whole, name), getattr(pieces, name), err_msg=name)


def test_only_the_slow_synapses_targets_carry_a_slow_current():
    """Delivering slow input to the slow synapses' targets alone gives the same spikes and state as scanning every
    neuron for it, as the kernel once did."""
    edges, slow, types, n = random_circuit()
    slow = [(i, j, w) for i, j, w in slow if j % 3]            # leave every third neuron without slow input
    drive = [(np.arange(4), 120.0)]
    listed = small(edges, n, slow, types=types, trials=3, w_poi=30.0)
    scanned = small(edges, n, slow, types=types, trials=3, w_poi=30.0)
    scanned.stargets, scanned.slow_in = np.arange(n, dtype=np.int64), np.ones(n, np.bool_)
    a, b = listed.advance(2000, drive), scanned.advance(2000, drive)
    assert len(listed.stargets) < n and a.sum() > 100
    np.testing.assert_array_equal(a, b)
    for name in ("u", "x", "s"):
        np.testing.assert_array_equal(getattr(listed, name), getattr(scanned, name), err_msg=name)
    assert not listed.s[:, ~listed.slow_in].any()


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


def test_graded_release_along_a_slow_synapse_settles_like_spikes():
    """A graded neuron's release along a slow synapse acts like that many spikes a second into its target's slow
    current, which settles where release x weight x dt balances the slow current's decay."""
    brain = small([], 2, slow_edges=[(0, 1, 1.5)], tau_slow=0.05, types={"c0": {"unit": "graded", "bias": 20.0, "gain": 5.0}})
    brain.advance(20000)                                # 2 s, 40 slow time constants
    r = 5.0 * (20.0 - 7.0)
    s_ss = 1.5 * r * DT / (1 - np.exp(-DT / 0.05))      # about r x weight x tau_slow
    assert brain.s[0, 1] == pytest.approx(s_ss, rel=1e-3)
    assert brain.u[0, 1] == pytest.approx(_approach(0.05, T_MBR, DT) * s_ss / (1 - np.exp(-DT / T_MBR)), rel=1e-3)
    assert brain.x[0, 1] == 0                           # nothing reaches the fast current
    brain.set_slow(sparse.csr_matrix(([1.5], ([1], [0])), shape=(2, 2)))     # the same edge, set again mid-run:
    brain.advance(20000)                                # the release carries on, so the slow current rebuilds
    assert brain.s[0, 1] == pytest.approx(s_ss, rel=1e-3)
    brain.set_slow(None)                                # without the slow synapse the target gets nothing
    brain.reset()
    brain.advance(2000)
    assert brain.u[0, 1] == 0


def test_full_strength_exempts_single_synapses_from_depression():
    """A depressing neuron's second spike reaches a target flagged in full_strength at full strength, and its other
    target depressed, exactly as a neuron without depression and one with it would."""
    def two_spikes(depression):
        brain = small([(0, 1, 1.0), (0, 2, 1.0)], 3, types={"c0": {"depression": depression, "recovery": 1.0}},
                      w_poi=100.0)
        pre = np.repeat(np.arange(brain.n), np.diff(brain.ptr))
        brain.full_strength[(pre == 0) & (brain.idx == 2)] = True
        for _ in range(2):                              # two spikes 2 ms apart
            brain.advance(1, drive=[([0], 1 / DT)])
            brain.advance(19)
        brain.advance(20)                               # both have arrived
        return brain.x[0, 1], brain.x[0, 2]
    depressed, full = two_spikes(0.5)
    plain_1, plain_2 = two_spikes(1.0)
    assert full == pytest.approx(plain_2, rel=1e-6)
    assert depressed < plain_1 - 0.1


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


def test_external_release_reaches_targets_and_the_neuron_never_fires():
    """A neuron whose release is set from outside never fires, however hard it is driven. Its
    target settles where release x weight x dt per step puts it, a negative release takes input
    away, and reset() clears the release."""
    brain = small([(0, 1, 10.0), (2, 0, 500.0)], 3, w_poi=100.0)
    brain.set_release([0], 65.0)
    counts = brain.advance(8000, drive=[([2], 1 / DT)])     # neuron 2 hammers neuron 0
    assert counts[0, 0] == 0 and counts[0, 2] > 1000
    x = 10.0 * 65.0 * DT / (1 - np.exp(-DT / TAU))
    assert brain.x[0, 1] == pytest.approx(x, rel=1e-3)
    brain.set_release([0], -65.0)
    brain.advance(8000)
    assert brain.x[0, 1] == pytest.approx(-x, rel=1e-3)
    brain.reset()
    brain.advance(100)
    assert brain.x[0, 1] == 0 and brain.external[0]


def test_input_to_external_neurons_changes_nothing():
    """External release skips targets that are external themselves, since their input can't
    matter: with or without a synapse between two external neurons, every spike is the same."""
    base = [(1, 2, 40.0), (2, 3, 60.0), (3, 2, -20.0), (4, 3, 50.0)]
    for edges in (base, base + [(1, 4, 300.0), (0, 4, 80.0)]):
        brain = small(edges, 5, w_poi=30.0)
        for k in range(30):
            brain.set_release([1, 4], [20.0 + 5 * k, 90.0 - 3 * k])
            spikes = brain.advance(100, drive=[([0], 200.0)])
            if k == 0:
                total = spikes
            else:
                total = total + spikes
        if edges is base:
            expected = total
    assert total[0, 2:4].sum() > 0
    np.testing.assert_array_equal(total[:, [0, 2, 3]], expected[:, [0, 2, 3]])


def test_background_kicks_are_independent_poisson_events():
    """2,000 unconnected neurons, each kick large enough to make a spike: over 2 s at 20 Hz, spikes
    match a Poisson count in total and in each neuron's variance."""
    brain = small([], 2000, types={"all": {"noise_rate": 20.0, "noise_kick": 50.0, "refractory": 0.0}}, trials=2)
    spikes = brain.advance(20000)
    expected = 2000 * 20 * 2.0
    for trial in spikes:
        assert abs(trial.sum() - expected) < 0.012 * expected    # a kick landing as its neuron fires is lost (~0.2%)
        assert 0.85 < trial.var() / trial.mean() < 1.15
    assert not np.array_equal(spikes[0], spikes[1])


def test_background_is_the_same_in_pieces():
    edges, slow, types, n = random_circuit()
    types = dict(types, all={"noise_rate": 30.0, "noise_kick": 4.0})
    types = {"all": types.pop("all"), **types}                  # broad first, so the others still apply
    whole = small(edges, n, slow, types=types, trials=2)
    pieces = small(edges, n, slow, types=types, trials=2)
    once = whole.advance(3000)
    parts = sum(pieces.advance(k) for k in (13, 987, 2000))
    assert once.sum() > 20
    np.testing.assert_array_equal(once, parts)


def test_a_per_neuron_bias_adds_to_the_type_bias():
    """Each neuron settles at its type's bias plus its own."""
    extra = np.array([0.0, 1.5, -2.0])
    brain = small([], 3, types={"c0": {"bias": 3.0}}, bias=extra)
    brain.advance(6000)
    np.testing.assert_allclose(brain.u[0], [3.0, 1.5, -2.0], atol=1e-3)


def test_a_bias_given_per_neuron_acts_as_the_same_type_bias():
    """On an active circuit with background, the same bias per neuron or per type: identical spikes.
    And set_bias between advances moves a neuron where it would have gone from the start."""
    edges, slow, types, n = random_circuit()
    noisy = {"all": {"noise_rate": 30.0, "noise_kick": 4.0}}
    by_type = small(edges, n, slow, types={"all": {**noisy["all"], "bias": 5.0}}, trials=2)
    by_neuron = small(edges, n, slow, types=noisy, trials=2, bias=np.full(n, 5.0))
    expected = by_type.advance(3000)
    assert expected.sum() > 20
    np.testing.assert_array_equal(by_neuron.advance(3000), expected)
    later = small([], 2)
    later.advance(100)
    later.set_bias(np.array([4.0, -1.0]))
    later.advance(6000)
    np.testing.assert_allclose(later.u[0], [4.0, -1.0], atol=1e-3)


def test_adaptation_current_decays_and_holds_the_neuron_down():
    """An adaptation current of 5 mV on a silent neuron decays with adaptation_tau and, being slow,
    holds v at -a tau_a / (tau_a - tau_m)."""
    brain = small([], 1, types={"c0": {"adaptation": 1.0, "adaptation_tau": 0.2}})
    brain.ad[0, 0] = 5.0
    brain.advance(2000)
    a = 5.0 * np.exp(-2000 * DT / 0.2)
    assert brain.ad[0, 0] == pytest.approx(a, rel=1e-4)
    assert brain.u[0, 0] == pytest.approx(-a * 0.2 / (0.2 - T_MBR), rel=1e-3)


def test_adaptation_slows_a_tonic_neuron_and_survives_pieces():
    """A neuron held above threshold fires fast at first and slower once adapted, at a steady rate
    whose adaptation current is about rate x step x tau; and pieces give the same spikes."""
    types = {"c0": {"bias": 20.0, "adaptation": 1.0, "adaptation_tau": 0.2}}
    brain = small([], 1, types=types)
    onset = brain.advance(500)[0, 0] / 0.05
    brain.advance(19500)
    late = brain.advance(10000)[0, 0] / 1.0
    assert onset > 1.5 * late > 0
    assert brain.ad[0, 0] == pytest.approx(late * 1.0 * 0.2, rel=0.2)
    edges, slow, circuit, n = random_circuit()
    circuit = dict(circuit, c1={"adaptation": 2.0, "adaptation_tau": 0.05}, c6={"adaptation": 0.5})
    whole = small(edges, n, slow, types=circuit, trials=2, w_poi=30.0)
    pieces = small(edges, n, slow, types=circuit, trials=2, w_poi=30.0)
    drive = [(np.arange(4), 120.0)]
    once = whole.advance(2000, drive)
    parts = sum(pieces.advance(k, drive) for k in (3, 997, 1000))
    assert once.sum() > 100
    np.testing.assert_array_equal(once, parts)
    np.testing.assert_array_equal(whole.ad, pieces.ad)


def test_a_named_set_takes_parameters_like_a_type():
    """Parameters given to a named set reach exactly its neurons, and combine with their types'."""
    brain = small([], 4, types={"c1": {"threshold": 10.0}, "picked": {"bias": 3.0}}, sets={"picked": [1, 3]})
    params = [brain.params[c] for c in brain.cls]
    assert [p["bias"] for p in params] == [0.0, 3.0, 0.0, 3.0]
    assert [p["threshold"] for p in params] == [7.0, 10.0, 7.0, 7.0]


def two_cells(gap) -> HybridBrain:
    labels = {"cell_type": np.array(["c0", "c1"]), "side": np.array(["L", "L"]), "superclass": np.array(["test", "test"])}
    return HybridBrain(matrix=sparse.csr_matrix((2, 2), dtype=np.float32), labels=labels, w_syn=1.0, gap=gap, w_poi=20.0)


KICKS = {10, 60, 110, 160}                  # steps at which c0 gets a sure 20 mV kick, far apart


def kicked(brain: HybridBrain, steps: int = 200) -> np.ndarray:
    return np.array([brain.advance(1, drive=[([0], 1 / DT)] if t in KICKS else ())[0] for t in range(steps)])


def test_an_electrical_synapse_fires_its_partner_on_the_next_step():
    """A spikelet over threshold makes the partner fire one step after each presynaptic spike, and
    only in the junction's direction; without the junction the partner stays silent."""
    gap = sparse.csr_matrix((np.array([10.0], np.float32), ([1], [0])), shape=(2, 2))     # c0 -> c1, 10 mV
    run = kicked(two_cells(gap))
    pre, post = np.flatnonzero(run[:, 0]), np.flatnonzero(run[:, 1])
    assert len(pre) == len(KICKS)
    np.testing.assert_array_equal(post, pre + 1)
    assert kicked(two_cells(None))[:, 1].sum() == 0
    assert kicked(two_cells(gap.T.tocsr()))[:, 1].sum() == 0


def test_a_subthreshold_spikelet_only_adds_to_other_input():
    """A 3 mV spikelet can't fire a resting partner (threshold 7 mV above rest): it raises its
    membrane by 3 mV at once, which then decays."""
    gap = sparse.csr_matrix((np.array([3.0], np.float32), ([1], [0])), shape=(2, 2))
    brain = two_cells(gap)
    before, fired = None, 0
    for t in range(40):
        c = brain.advance(1, drive=[([0], 1 / DT)] if t == 10 else ())[0]
        fired += int(c[1])
        if c[0]:
            before = float(brain.u[0, 1])
    assert before is not None and abs(before - 3.0) < 1e-5
    assert float(brain.u[0, 1]) < before and fired == 0



def fast_pair(size: float, types: dict | None = None) -> HybridBrain:
    labels = {"cell_type": np.array(["c0", "c1"]), "side": np.array(["L", "L"]), "superclass": np.array(["test", "test"])}
    fast = sparse.csr_matrix((np.array([size], np.float32), ([1], [0])), shape=(2, 2))          # c0 -> c1
    return HybridBrain(matrix=sparse.csr_matrix((2, 2), dtype=np.float32), labels=labels, w_syn=1.0, w_poi=20.0,
                       fast=fast, fast_delay=3e-4, types=types)


def test_a_fast_synapse_fires_its_target_after_its_delay():
    """A fast synapse over threshold makes its target fire 3 steps (0.3 ms) after each presynaptic spike, plus the
    step the target takes to fire, and only in the synapse's direction."""
    run = kicked(fast_pair(10.0))
    pre, post = np.flatnonzero(run[:, 0]), np.flatnonzero(run[:, 1])
    assert len(pre) == len(KICKS)
    np.testing.assert_array_equal(post, pre + 4)


def test_a_fast_synapse_depresses_with_its_neuron():
    """With c0 depressing (half its strength left after a spike, recovering with 20 ms), the second of two spikes
    10 ms apart raises c1 by 1 - 0.5 exp(-10/20) of the first's 5 mV, and the first by exactly 5 mV."""
    brain = fast_pair(5.0, types={"c0": {"depression": 0.5, "recovery": 0.02}})
    u = []
    for t in range(140):
        brain.advance(1, drive=[([0], 1 / DT)] if t in (10, 110) else ())
        u.append(float(brain.u[0, 1]))
    u = np.array(u)
    assert abs(u[14] - 5.0) < 1e-5 and u[13] == 0.0                   # c0 fires at step 11 (kicked at 10); 3 steps on
    decay = u[113] / u[112]                                         # c1's own decay per step, with nothing arriving
    second = u[114] - u[113] * decay
    assert second == pytest.approx(5.0 * (1 - 0.5 * np.exp(-100 / 200)), rel=1e-4)


def test_recorded_spikes_match_the_counts_step_by_step():
    """advance(record=...) returns the listed neurons' spikes step by step, summing to their counts, and the
    same run as without recording."""
    gap = sparse.csr_matrix((np.array([10.0], np.float32), ([1], [0])), shape=(2, 2))
    a, b = two_cells(gap), two_cells(gap)
    drive = [([0], 200.0)]
    plain = a.advance(500, drive=drive)
    counts, spikes = b.advance(500, drive=drive, record=[1, 0])
    np.testing.assert_array_equal(plain, counts)
    np.testing.assert_array_equal(spikes.sum(1), counts[:, [1, 0]])
    pre, post = np.flatnonzero(spikes[0, :, 1]), np.flatnonzero(spikes[0, :, 0])
    assert len(post) > 3 and post[0] == pre[0] + 1
    assert set(post) <= set(pre + 1)                # c1 fires one step after c0, unless still refractory
