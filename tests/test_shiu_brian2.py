"""brainfly.shiu's kernel against Brian2 running Shiu et al.'s equations with their schedule.

Shiu's results come from Brian2 (github.com/philshiu/Drosophila_brain_model, model.py), so Brian2's
schedule is the reference. Within each 0.1 ms step Brian2 integrates, applies the threshold, delivers
synaptic and Poisson input, then resets. A spike's input arrives 1.8 ms later. A neuron is refractory
while timestep(t - lastspike) < timestep(2.2 ms), and input that reaches it then is dropped: Brian2
gives variables marked "unless refractory" a conditional write. Neurons with Poisson input have no
refractory period. Skipped if brian2 isn't installed (pip install brian2).
"""
from __future__ import annotations

import logging

import numpy as np
import pytest
from scipy import sparse

b2 = pytest.importorskip("brian2")

from brainfly.shiu import F_POI, T_DLY, T_MBR, T_RFC, TAU, V0, V_RST, V_TH, W_SYN, _simulate  # noqa: E402

logging.getLogger("brian2").setLevel(logging.ERROR)
DT = 1e-4


def brian2_run(n, edges, driven, w_poi, rate, seconds, tail, trials=1, seed=0):
    """Shiu's model.py network in Brian2: spike (step, neuron) pairs, `trials` independent copies
    (copy c's neuron i is c * n + i). Driven neurons get one PoissonInput each onto v, and no
    refractory period."""
    b2.start_scope()
    b2.prefs.codegen.target = "numpy"
    b2.defaultclock.dt = DT * b2.second
    b2.seed(seed)
    ns = dict(v_0=V0 * b2.mV, v_th=V_TH * b2.mV, v_rst=V_RST * b2.mV, t_mbr=T_MBR * b2.second, tau=TAU * b2.second)
    eqs = """dv/dt = (x - (v - v_0)) / t_mbr : volt (unless refractory)
             dx/dt = -x / tau : volt (unless refractory)
             rfc : second"""
    # the driven neurons of every copy come first, so one PoissonInput covers them all
    order = list(driven) + [i for i in range(n) if i not in driven]
    slot = np.empty(n, int)
    slot[order] = np.arange(n)
    nd = len(driven)

    def index(copy, i):
        return copy * nd + slot[i] if slot[i] < nd else trials * nd + copy * (n - nd) + slot[i] - nd

    G = b2.NeuronGroup(trials * n, eqs, threshold="v > v_th", reset="v = v_rst; x = 0*mV", refractory="rfc",
                       method="linear", namespace=ns)
    G.v, G.x, G.rfc = ns["v_0"], 0 * b2.mV, T_RFC * b2.second
    G.rfc[:trials * nd] = 0 * b2.ms
    pre, post, w = zip(*edges)
    S = b2.Synapses(G, G, "w : volt", on_pre="x += w", delay=T_DLY * b2.second)
    S.connect(i=np.array([index(c, i) for c in range(trials) for i in pre]),
              j=np.array([index(c, j) for c in range(trials) for j in post]))
    S.w = np.tile(np.array(w, float), trials) * b2.mV
    P = b2.PoissonInput(G[:trials * nd], "v", N=1, rate=rate * b2.Hz, weight=w_poi * b2.mV)
    M = b2.SpikeMonitor(G)
    net = b2.Network(G, S, P, M)
    net.run(seconds * b2.second)
    P.active = False
    if tail > 0:
        net.run(tail * b2.second)
    back = np.empty(trials * n, int)                 # Brian2 index -> copy * n + neuron
    for c in range(trials):
        for i in range(n):
            back[index(c, i)] = c * n + i
    steps = np.round(np.asarray(M.t / b2.second) / DT).astype(int)
    return steps, back[np.asarray(M.i)]


def kernel_run(n, edges, driven, w_poi, p, steps, drive_steps, trials=1, bin_steps=1, seed=0):
    pre, post, w = zip(*edges)
    C = sparse.csc_matrix((np.array(w, np.float32), (post, pre)), shape=(n, n))   # columns = presynaptic
    e_m, e_s = np.exp(-DT / T_MBR), np.exp(-DT / TAU)
    a_vx = TAU / (TAU - T_MBR) * (e_s - e_m)
    return _simulate(C.indptr, C.indices, C.data.astype(np.float32), n, trials, steps, drive_steps,
                     int(round(T_DLY / DT)), int(round(T_RFC / DT)), np.float32(e_m), np.float32(a_vx),
                     np.float32(e_s), np.array(driven, np.int64), np.full(len(driven), p), np.float32(w_poi),
                     np.zeros(n, np.bool_), bin_steps, seed)


# Every neuron fires. Weights in mV: chains, excitatory and inhibitory convergence, inhibition onto
# both driven neurons, autapses that arrive inside the refractory period (1 and 5, dropped) and one
# onto a driven neuron, which has none (0, kept).
EDGES = [(0, 0, 3), (0, 1, 50), (0, 2, 30), (4, 2, 30), (1, 1, 40), (1, 3, 70), (2, 3, -20), (2, 1, -25),
         (3, 5, 55), (3, 4, -30), (5, 0, -20), (5, 5, 70), (4, 5, 20)]
N, DRIVEN, KICK = 6, [0, 4], 0.08          # 0.08 mV onto neurons 0 and 4 every step, so they integrate
STEPS, DRIVE_STEPS = 3000, 2000            # 200 ms driven, then 100 ms without


def test_spike_trains_match_brian2_step_for_step():
    steps, neuron = brian2_run(N, EDGES, DRIVEN, KICK, 1 / DT, DRIVE_STEPS * DT, (STEPS - DRIVE_STEPS) * DT)
    expected = np.zeros((STEPS, N), int)
    np.add.at(expected, (steps, neuron), 1)
    assert (expected.sum(0) > 0).all(), "every neuron should fire in the reference run"
    # the kernel returns counts, so run it for 1..STEPS steps and difference the totals
    totals = np.array([kernel_run(N, EDGES, DRIVEN, KICK, 1.0, s, min(s, DRIVE_STEPS))[0][0] for s in range(1, STEPS + 1)])
    actual = np.diff(np.vstack([np.zeros(N, int), totals]), axis=0)
    for i in range(N):
        np.testing.assert_array_equal(np.flatnonzero(actual[:, i]), np.flatnonzero(expected[:, i]), err_msg=f"neuron {i}")
    total, after, timeline = kernel_run(N, EDGES, DRIVEN, KICK, 1.0, STEPS, DRIVE_STEPS, bin_steps=10)
    np.testing.assert_array_equal(after[0], expected[DRIVE_STEPS:].sum(0))
    np.testing.assert_array_equal(timeline[0], expected.sum(1).reshape(-1, 10).sum(1))


def test_poisson_rates_match_brian2():
    """Shiu's actual drive, where every Poisson event pushes a neuron over threshold (250 x w_syn),
    at 150 Hz into a random network; mean rates over 300 trials agree within sampling error."""
    rng = np.random.default_rng(3)
    n, driven = 24, [0, 1, 2, 3]
    pairs = [(i, j) for i in range(n) for j in range(n) if rng.random() < 0.25]
    edges = [(i, j, float(rng.normal(8, 14))) for i, j in pairs]
    trials, seconds = 300, 0.5
    steps, neuron = brian2_run(n, edges, driven, F_POI * W_SYN, 150.0, seconds, 0.0, trials=trials, seed=1)
    brian = np.bincount(neuron, minlength=trials * n).reshape(trials, n) / seconds
    total, _, _ = kernel_run(n, edges, driven, F_POI * W_SYN, 150.0 * DT, int(round(seconds / DT)),
                             int(round(seconds / DT)), trials=trials, seed=1)
    ours = total / seconds
    assert brian[:, n // 2:].mean() > 1.0, "the network downstream of the drive should be active"
    se = np.sqrt(ours.var(0, ddof=1) / trials + brian.var(0, ddof=1) / trials)
    diff = np.abs(ours.mean(0) - brian.mean(0))
    assert (diff <= 4 * se + 0.5).all(), f"rates differ: ours {ours.mean(0).round(1)}, Brian2 {brian.mean(0).round(1)}"
