"""vnc_rhythm.py's rate model of the nerve cord, integrated in numba: the same fourth-order Runge-Kutta steps, in the same
order of operations, as rung5_vnc.simulate, without numpy's per-call overhead.

    tau_i dr_i/dt = max(rmax_i tanh((a_i / rmax_i) (I_i + B sum_j w_ij r_j - theta_i)), 0) - r_i

The weighted sums run row by row in CSR order, as scipy's sparse products do, so the rates match rung5_vnc.simulate's
(`python experiments/vnc_fast.py` checks). simulate() keeps only the saved rates of the neurons asked for, each
neuron's activity and peak over the first second (what Pugliese et al.'s screen rule looks at), and one neuron's mean
rate after 0.5 s.

    out = simulate(W, params, stim, seconds=2.0, record=motor_neurons, watch=j)

Speed with 4 threads, against rung5_vnc.simulate (0.5 s of the model, DNg100 driven, 9 Oct 2026, two other jobs
running): 32 replicates 12.1 against 32.8 s, 160 replicates 47.6 against 180.3 s, the rates identical to the bit.
"""
from __future__ import annotations

import numba
import numpy as np

import vnc_rhythm as v


@numba.njit(cache=True, parallel=True)
def _derivative(indptr, indices, data, tau, a_over, theta, rmax, stim, on, r, out):
    """out = (max(rmax tanh(a_over (stim * on + W r - theta)), 0) - r) / tau, W in CSR (rows = targets). Rows run in
    parallel; each row's sum keeps its order, so the result doesn't depend on the threads."""
    n, k = r.shape
    for i in numba.prange(n):
        for c in range(k):
            out[i, c] = 0.0
        for jj in range(indptr[i], indptr[i + 1]):
            w, col = data[jj], indices[jj]
            for c in range(k):
                out[i, c] += w * r[col, c]
        for c in range(k):
            x = (stim[i, c] * on + out[i, c]) - theta[i, c]
            act = rmax[i, c] * np.tanh(a_over[i, c] * x)
            if act < 0.0:
                act = 0.0
            out[i, c] = (act - r[i, c]) / tau[i, c]


@numba.njit(cache=True, parallel=True)
def _axpy(r, h, kk, out):
    """out = r + h * kk."""
    n, k = r.shape
    for m in numba.prange(n):
        for c in range(k):
            out[m, c] = r[m, c] + h * kk[m, c]


@numba.njit(cache=True, parallel=True)
def _step(r, sixth, k1, k2, k3, k4):
    """r = r + sixth * (((k1 + 2 k2) + 2 k3) + k4), in rung5_vnc.simulate's order."""
    n, k = r.shape
    for m in numba.prange(n):
        for c in range(k):
            r[m, c] = r[m, c] + sixth * (((k1[m, c] + 2 * k2[m, c]) + 2 * k3[m, c]) + k4[m, c])


@numba.njit(cache=True)
def _integrate(indptr, indices, data, tau, a_over, theta, rmax, stim, t_on, t_off, dt, steps, every, record, first, watch,
               rec, active, peak, watched):
    n, k = tau.shape
    r = np.zeros((n, k))
    k1, k2, k3, k4, tmp = np.empty((n, k)), np.empty((n, k)), np.empty((n, k)), np.empty((n, k)), np.empty((n, k))
    count = 0
    half, sixth = 0.5 * dt, dt / 6
    for s in range(steps):
        t = s * dt
        if s % every == 0:
            i = s // every
            for q in range(len(record)):
                for c in range(k):
                    rec[i, q, c] = r[record[q], c]
            if i < first:
                for m in range(n):
                    for c in range(k):
                        if r[m, c] > 0.0:
                            active[m, c] = True
                        if r[m, c] > peak[m, c]:
                            peak[m, c] = r[m, c]
            if t >= 0.5:
                for c in range(k):
                    watched[c] += r[watch, c]
                count += 1
        th = t + half
        _derivative(indptr, indices, data, tau, a_over, theta, rmax, stim, 1.0 if t_on <= t <= t_off else 0.0, r, k1)
        _axpy(r, half, k1, tmp)
        _derivative(indptr, indices, data, tau, a_over, theta, rmax, stim, 1.0 if t_on <= th <= t_off else 0.0, tmp, k2)
        _axpy(r, half, k2, tmp)
        _derivative(indptr, indices, data, tau, a_over, theta, rmax, stim, 1.0 if t_on <= th <= t_off else 0.0, tmp, k3)
        _axpy(r, dt, k3, tmp)
        _derivative(indptr, indices, data, tau, a_over, theta, rmax, stim, 1.0 if t_on <= t + dt <= t_off else 0.0, tmp, k4)
        _step(r, sixth, k1, k2, k3, k4)
    for q in range(len(record)):
        for c in range(k):
            rec[rec.shape[0] - 1, q, c] = r[record[q], c]
    for c in range(k):
        watched[c] /= max(count, 1)


def simulate(W, p: dict, stim: np.ndarray, seconds: float = v.T, record=None, watch: int = 0) -> dict:
    """The model for `seconds` with a step drive (stim: neurons x replicates) from 0.02 s to `seconds` - 0.001 s."""
    n, k = p["tau"].shape
    Wb = (v.B * W).tocsr()                                  # unsorted as in rung5_vnc.simulate: the same summing order
    record = np.arange(n) if record is None else np.asarray(record, np.int64)
    steps, every = int(round(seconds / v.DT)), int(round(v.SAVE / v.DT))
    rec = np.zeros((steps // every + 1, len(record), k), np.float32)
    active, peak, watched = np.zeros((n, k), np.bool_), np.zeros((n, k)), np.zeros(k)
    _integrate(Wb.indptr.astype(np.int64), Wb.indices.astype(np.int64), Wb.data.astype(np.float64), p["tau"], p["a"] / p["rmax"],
               p["theta"], p["rmax"], np.asarray(stim, np.float64), 0.02, seconds - 0.001, v.DT, steps, every, record,
               int(round(1.0 / v.SAVE)), int(watch), rec, active, peak, watched)
    return {"rates": rec, "active": active.sum(0), "peak": peak, "watched_hz": watched}


if __name__ == "__main__":
    import time

    import rung5_vnc as a1
    from vnc_own import own_network
    table, _ = v.network()
    W, _ = own_network(table)
    inst = table["instance"].astype(str).to_numpy()
    j = int(np.flatnonzero(inst == "DNb08(VES082)_L")[0])
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    p = v.params(table, np.random.default_rng(5103), 4)
    stim = np.zeros((len(table), 4))
    stim[j] = 256.0
    simulate(W, p, stim, 0.01, mn, j)                       # compile
    t0 = time.perf_counter()
    fast = simulate(W, p, stim, v.T, mn, j)
    t1 = time.perf_counter()
    slow = a1.simulate(W, p, stim, v.T)
    t2 = time.perf_counter()
    print(f"numba {t1 - t0:.1f} s, numpy {t2 - t1:.1f} s; largest difference in the motor neurons' rates:",
          float(np.abs(fast["rates"] - slow[:, mn, :]).max()))
