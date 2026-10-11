"""Exploratory analysis, not pre-registered: pn_toy.py with the receptor synapse models orn_pn_recovery_fit.py fitted,
whose slow pool can recover faster with residual calcium. Does a synapse that recovers fast during bursts and slowly at
rest give a PN flies' small resting drive with flies' steep, strong transform?

pn_toy.py: with brainfly's two fixed pools, deeper depression lowers the resting drive but flattens the transform
(Kazama & Wilson's single pool: 12 mV, Rmax 82-96), and a high spontaneous rate costs DL5 both. Here each model fitted in
orn_pn_recovery_fit.py (its parameters read from orn_pn_recovery_fit.json) drives pn_toy.py's PN, everything else as there:
a DL5-like cell (43 receptor neurons at the basiconic median 6 spikes/s), DL5 at its measured 14 spikes/s, and a DM4-like
cell (32 at its measured 3.44). Measured as pn_toy.py measures: the resting drive, the synapses' resting efficacy, Olsen
et al.'s transform (sigma, Rmax) and the share of the peak left at 500 ms at 80 spikes/s.
Fly targets: resting drive 5-10 mV (DM4 about 5-7); DL5's points (5.1, 44), (13.4, 85), (41.5, 149), (98.7, 158), sigma
11.8, Rmax 167; DM4 sigma 16.3, Rmax 170; 0.44 of the peak left at 500 ms.

Ran (48 s): no; with the synapse fitted to flies' trains, deeper resting depression costs the response, whichever model.
A DL5-like cell (6 spikes/s): brainfly's pools give a 21.3 mV resting drive, Rmax 128, sigma 11.7 and 0.35 of the peak left
at 500 ms; refitted 15.2 mV, Rmax 97, sigma 10.3, 0.17; DKR 17.3 mV, Rmax 111, sigma 10.2, 0.26 (M4-DKR the same). A
DM4-like cell (3.44 spikes/s): 11.1, 8.9 and 8.8 mV (flies about 5-7), Rmax 122, 96 and 107 (flies 170). DL5 at its
measured 14 spikes/s stays the puzzle in every model: 20-32 mV of resting drive and Rmax 69-95 (flies 167). Flies' small
resting drive and strong, sustained response (0.44 left at 500 ms) can't both come from how the receptor synapse
depresses, as its trains constrain it: something else must carry their odor drive, such as the slow component, lateral
excitation or a recurrent current the toy lacks, or flies' resting drive is smaller for another reason.

    python experiments/pn_toy2.py      (writes experiments/pn_toy2.json; needs orn_pn_recovery_fit.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from numba import njit, prange
from scipy.optimize import curve_fit

OUT = Path(__file__).with_suffix(".json")
FIT = Path(__file__).with_name("orn_pn_recovery_fit.json")
DT = 1e-4
TAU_S, TAU_M, TAU_SLOW = 0.005, 0.020, 0.080
THRESHOLD, RESET, REFRACTORY = 10.0, 0.0, 0.0022
NOISE_RATE, NOISE_KICK = 200.0, 1.0
UEPSP_MV, SLOW_CHARGE = 6.19, 0.086
SLOW_F, SLOW_TAU = 0.91, 0.629
REST_HZ = 4.6
RATES = (5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
LATENCY_S, OFFSET_S, PRE_S, POST_S, WINDOW_S = 0.1, 0.52, 0.5, 1.0, 0.5
FLY_DL5 = [(5.1, 44.2), (13.4, 84.9), (41.5, 148.6), (98.7, 158.4)]


def peak_factor(tau_s: float) -> float:
    t = np.arange(0, 0.2, 1e-5)
    return float((tau_s / (tau_s - TAU_M) * (np.exp(-t / tau_s) - np.exp(-t / TAU_M))).max())


def olsen_shape(t: np.ndarray, x: float) -> np.ndarray:
    """odor_olsen_protocol_check.olsen_shape: the receptor neurons' extra rate (unscaled) t s after the valve opens."""
    t = np.asarray(t, float)
    tau_r = 0.04 if x < 20 else 0.025
    c = np.clip(t - LATENCY_S, 0.0, None)
    adapt = 1.0 if x < 20 else 0.65 + 0.35 * np.exp(-c / 0.25)
    on = (1.0 - np.exp(-c / tau_r)) * adapt
    c_off = OFFSET_S - LATENCY_S
    at_off = (1.0 - np.exp(-c_off / tau_r)) * (1.0 if x < 20 else 0.65 + 0.35 * np.exp(-c_off / 0.25))
    return np.where(t < LATENCY_S, 0.0, np.where(t < OFFSET_S, on, at_off * np.exp(-(t - OFFSET_S) / 0.06)))


@njit(parallel=True, cache=True)
def simulate(rates, n_orn, trials, bias, w, fa, ta, fb, tb, d, j_fast, j_slow, settle_steps, bin_steps, seed, silent, tmin, tc, kc):
    """Each trial: settle at rates[0] for settle_steps, then run rates (one per step); returns spike counts per bin
    (trials x bins) and the mean membrane potential over the run, and the mean strength left at the run's start."""
    n = rates.shape[0]
    nb = n // bin_steps
    counts = np.zeros((trials, nb))
    u_mean = np.zeros(trials)
    eff = np.zeros(trials)
    db, ds, dcal = np.exp(-DT / tb), np.exp(-DT / SLOW_TAU), np.exp(-DT / tc)
    dsyn, dslow, dm = np.exp(-DT / TAU_S), np.exp(-DT / TAU_SLOW), np.exp(-DT / TAU_M)
    for k in prange(trials):
        np.random.seed(seed + k)
        a = np.ones(n_orn)
        b = np.ones(n_orn)
        s = np.ones(n_orn)
        cal = np.zeros(n_orn)
        i_fast, i_slow, u, until = 0.0, 0.0, 0.0, -1
        for step in range(settle_steps + n):
            r = rates[0] if step < settle_steps else rates[step - settle_steps]
            if silent:
                r = 0.0
            p = r * DT
            for i in range(n_orn):
                rate_a = 1.0 / ta + (1.0 / tmin - 1.0 / ta) * cal[i] / (cal[i] + kc)
                a[i] = 1.0 - (1.0 - a[i]) * np.exp(-DT * rate_a)
                cal[i] *= dcal
                b[i] = 1.0 - (1.0 - b[i]) * db
                s[i] = 1.0 - (1.0 - s[i]) * ds
                if np.random.random() < p:
                    strength = (w * a[i] + (1.0 - w) * b[i]) / d
                    i_fast += j_fast * strength
                    i_slow += j_slow * s[i] / d
                    a[i] -= (1.0 - fa) * a[i] / d
                    b[i] -= (1.0 - fb) * b[i] / d
                    cal[i] += 1.0
                    s[i] -= (1.0 - SLOW_F) * s[i] / d
            i_fast *= dsyn
            i_slow *= dslow
            if step == settle_steps:
                tot = 0.0
                for i in range(n_orn):
                    tot += (w * a[i] + (1.0 - w) * b[i]) / d
                eff[k] = tot / n_orn
            if np.random.random() < NOISE_RATE * DT:
                u += NOISE_KICK
            if step < until:
                u = RESET
            else:
                u = u * dm + (1.0 - dm) * (bias + i_fast + i_slow)
                if u >= THRESHOLD:
                    u = RESET
                    until = step + int(REFRACTORY / DT)
                    if step >= settle_steps:
                        counts[k, (step - settle_steps) // bin_steps] += 1
            if step >= settle_steps:
                u_mean[k] += u / n
    return counts, u_mean, eff


class Toy:
    def __init__(self, n_orn=40, r0=6.0, w=0.5, fa=0.83, ta=7.5, fb=0.67, tb=0.3, d=1.0, uepsp=UEPSP_MV, trials=200, seed=1,
                 tmin=None, tc=0.1, kc=1.0):
        self.n_orn, self.r0, self.w, self.fa, self.ta, self.fb, self.tb, self.d = n_orn, r0, w, fa, ta, fb, tb, d
        self.tmin, self.tc, self.kc = (ta if tmin is None else tmin), tc, kc
        self.trials, self.seed = trials, seed
        self.j_fast = uepsp / peak_factor(TAU_S)
        self.j_slow = SLOW_CHARGE * self.j_fast * TAU_S / TAU_SLOW      # the slow current's charge 0.086 of the fast's
        self.bias = 0.0

    def run(self, rates: np.ndarray, settle_s: float, bin_s: float, silent: bool = False, trials=None, seed_off=0):
        return simulate(rates.astype(np.float64), self.n_orn, trials or self.trials, self.bias, self.w, self.fa, self.ta,
                        self.fb, self.tb, self.d, self.j_fast, self.j_slow, int(settle_s / DT), int(bin_s / DT),
                        self.seed + seed_off, silent, self.tmin, self.tc, self.kc)

    def rest_rate(self, trials=100) -> float:
        rates = np.full(int(1.0 / DT), self.r0)
        c, _, _ = self.run(rates, 3.0, 1.0, trials=trials, seed_off=50000)
        return float(c.mean())

    def set_rest(self, target=REST_HZ) -> float:
        lo, hi = -80.0, 20.0
        for _ in range(14):
            self.bias = 0.5 * (lo + hi)
            lo, hi = (self.bias, hi) if self.rest_rate() < target else (lo, self.bias)
        self.bias = 0.5 * (lo + hi)
        return self.rest_rate(trials=200)

    def resting(self) -> dict:
        rates = np.full(int(1.0 / DT), self.r0)
        c, u, eff = self.run(rates, 3.0, 1.0, trials=100, seed_off=60000)
        _, u0, _ = self.run(rates, 3.0, 1.0, silent=True, trials=100, seed_off=61000)
        return {"rest_hz": round(float(c.mean()), 2), "drive_mv": round(float(u.mean() - u0.mean()), 2),
                "efficacy": round(float(eff.mean()), 3)}

    def olsen(self, x: float) -> dict:
        grid = np.arange(0, POST_S, DT) + DT / 2
        extra = olsen_shape(grid, x)
        window = grid < WINDOW_S
        extra *= x / float(extra[window].mean())
        rates = np.concatenate([np.full(int(PRE_S / DT), self.r0), self.r0 + extra])
        c, _, _ = self.run(rates, 3.0, 0.01, seed_off=int(x * 100))
        psth = c.mean(0) / 0.01
        n_pre, n_win = int(PRE_S / 0.01), int(WINDOW_S / 0.01)
        rest = psth[:n_pre].mean()
        win = psth[n_pre:n_pre + n_win] - rest
        smooth = np.convolve(psth[n_pre:] - rest, np.ones(5) / 5, mode="valid")
        k = int(np.argmax(smooth))
        late = float(smooth[int(round((WINDOW_S - 0.025) / 0.01))])
        return {"window_mean": round(float(win.mean()), 1), "peak": round(float(smooth[k]), 1),
                "late_over_peak": round(late / float(smooth[k]), 3) if smooth[k] > 0 else None}


def olsen_eq(x, rmax, sigma):
    return rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)


def evaluate(name: str, **kw) -> dict:
    toy = Toy(**kw)
    rest = toy.set_rest()
    out = {"name": name, "settings": kw, "bias_mv": round(toy.bias, 2), "rest_hz": round(rest, 2)}
    out.update(toy.resting())
    pts = {f"{x:g}": toy.olsen(x) for x in RATES}
    out["points"] = pts
    try:
        (rmax, sigma), _ = curve_fit(olsen_eq, np.array(RATES), np.array([pts[f"{x:g}"]["window_mean"] for x in RATES]),
                                     p0=(160.0, 15.0), maxfev=20000)
        out["fit"] = {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
    except RuntimeError:
        out["fit"] = None
    out["late_over_peak_80"] = pts["80"]["late_over_peak"]
    print(f"{name:42s} drive {out['drive_mv']:5.1f} mV  eff {out['efficacy']:.3f}  bias {out['bias_mv']:6.1f}  "
          f"points {[pts[f'{x:g}']['window_mean'] for x in RATES]}  fit {out['fit']}  late {out['late_over_peak_80']}", flush=True)
    return out


def conditions() -> list:
    """M4 as brainfly has it and each fitted model, for a DL5-like cell at the basiconic median rate, DL5 at its measured
    rate, and a DM4-like cell at its measured rate."""
    fits = json.loads(FIT.read_text())["models"]
    kinds = {"M4 (brainfly)": dict(w=0.5, fa=0.83, ta=7.5, fb=0.67, tb=0.3)}
    m = fits["M4"]["params"]
    kinds["M4 refitted"] = dict(w=m[0], fa=m[1], ta=m[2], fb=m[3], tb=m[4])
    m = fits["DKR"]["params"]
    kinds["DKR"] = dict(w=1.0, fa=m[0], ta=m[1], tmin=m[2], tc=m[3], kc=m[4])
    m = fits["M4-DKR"]["params"]
    kinds["M4-DKR"] = dict(w=m[0], fa=m[1], ta=m[2], fb=m[3], tb=m[4], tmin=m[5], tc=m[6], kc=m[7])
    cells = {"DL5-like, N 43, r0 6": dict(n_orn=43, r0=6.0), "DL5, N 43, measured r0 14": dict(n_orn=43, r0=14.0),
             "DM4-like, N 32, r0 3.44": dict(n_orn=32, r0=3.44)}
    return [(f"{k}: {c}", {**kw, **ck}) for k, kw in kinds.items() for c, ck in cells.items()]


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": {"drive_mv": [5, 10], "dl5_points": FLY_DL5, "dl5_fit": [167, 11.8], "late_over_peak": 0.44},
           "conditions": []}
    for name, kw in conditions():
        out["conditions"].append(evaluate(name, **kw))
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
