"""Exploratory analysis, not pre-registered: in one projection neuron driven by its receptor neurons through brainfly's
synapse, which settings give flies' small resting drive and flies' steep transform together?

odor_resting_drive_check.py: silencing every receptor neuron drops the model's PNs 24.8 mV (DM1 18.0), where flies' drop
about 5-10 (Gouwens & Wilson 2009); flies' DM4 synapses keep about 0.26 of their rested strength at rest (Kazama & Wilson
2008), where brainfly's two-pool synapse predicts 0.47 at DM4's 3.44 spikes/s (research_notes/Rung 9 learning
data/orn_pn_depression.md, section 7). Deeper resting depression would bring the drive down but, in a toy like this one,
flattens the transform (weak_input_gain.md, section 9: sigma 26.6 with the two pools, 40 with Kazama & Wilson's single
pool), while flies have both deep resting depression and sigma 12-16 (Olsen et al. 2010). This toy asks which
combination of the measured quantities can give both.
The toy: N receptor neurons firing independently (Poisson) at r0 spikes/s, each through its own synapse onto one leaky
integrate-and-fire PN, as brainfly's are: a 5 ms current whose rested PSP peaks at 6.19 mV (Kazama & Wilson 2008),
depressing as two pools in parallel (share w recovering over tau_a with f_a left per spike, the rest over tau_b with f_b;
orn_pn_depression.md's M4: w 0.5, 0.83/7.5 s, 0.67/0.3 s), plus the slow component (0.086 of the fast charge, a current
decaying over 80 ms, depressing 0.91 per spike and recovering over 0.629 s, as Nagel et al. measured it); optionally a
tonic presynaptic divisor d (release and depletion both divided by d, Nagel et al. 2015's form). The PN: threshold 10 mV
above rest, reset to rest, 2.2 ms refractory, tau_m 20 ms, keeping its current through spikes, 200/s Poisson kicks of 1
mV (brainfly's uPN settings), and a bias set so that it rests at 4.6 spikes/s (Turner et al. 2008). 0.1 ms steps.
Measured for each setting: the resting drive (the PN's mean membrane potential at rest less with its receptor neurons
silent, the bias unchanged), the synapses' resting efficacy (mean strength left x 1/d), and the transform measured as
Olsen et al. measured flies' (odor_olsen_protocol_check.py's receptor time course and windows: 5-160 spikes/s, the PN's
500 ms window from the valve less the 500 ms before; their Eq. 1 fitted for sigma and Rmax; the share of the peak left at
500 ms at 80 spikes/s).
Fly targets: resting drive 5-10 mV (DM1-like PNs) or about 5-7 (DM4, 35-46 receptor neurons at 3.44 spikes/s); DL5's
points (5.1, 44), (13.4, 85), (41.5, 149), (98.7, 158), sigma 11.8, Rmax 167; 0.44 of the peak left at 500 ms.

Ran: a tonic presynaptic divisor of about 2-2.5, the part of flies' resting efficacy brainfly lacks, gives flies' small
resting drive without flattening the transform. The toy matches the full model where they overlap (its brainfly-like DL5:
a 21.3 mV resting drive, 30 and 57 spikes/s at 5 and 10 spikes/s of input, sigma 11.7, Rmax 128; odor_probe56.py's DL5
19.0 mV, 28 and 59, sigma 12.6, Rmax 136). Deeper depression lowers the drive but takes the responses with it (the slow
pool's share at 0.88, or Kazama & Wilson's single pool: 12 mV, but Rmax 82-96). A tonic divisor doesn't: it lowers the
synapses' net resting efficacy as deeper depression would, but by dividing release, so the synapses also deplete less at
rest and keep more for an odor. At divisor 2 the brainfly-like DL5 has a 14.2 mV drive, 0.27 efficacy, the same weak end
(30 spikes/s at 5) and Rmax 153 (128), keeping 0.43 of its peak at 500 ms (0.35; flies 0.44). A DM4-like cell (32 receptor
neurons at DM4's measured 3.44 spikes/s) at divisor 2.5 matches flies' DM4 on four measures of five: drive 5.7 mV (flies
about 5-7), efficacy 0.29 (flies 0.26, Kazama & Wilson 2008), sigma 15.1 (16.3), 0.43 of the peak at 500 ms (0.44); Rmax
149 (170). DL5 with a female's 48 receptor neurons at divisor 2: Rmax 162 (167), 0.44 at 500 ms (0.44), sigma 13.9 (11.8),
but still 32 spikes/s at 5 (flies 44). DM1 (74 receptor neurons at its measured 9 spikes/s) keeps 25-32 mV at divisors 2-3
and would need about 6-8, in line with flies' DM1 being held down by GABA (sigma 45 in saline, 13.4 with GABA blocked;
weak_input_gain.md). DL5 at its measured 14 spikes/s still answers too little (17 at 5), the puzzle weak_input_gain.md
notes. Flies' 0.26 is the ratio of spontaneous EPSCs with the antennae intact to rested uEPSCs (Kazama & Wilson 2008), so
it includes whatever tonic presynaptic inhibition the intact antennal lobe exerts (Nagel et al. 2015's model has a
resting divisor of about 4); brainfly's presynaptic inhibition starts above the resting rate and its receptor synapses
are scaled so that at rest they carry the rested strength, so the model has the depression and not the division.

    python experiments/pn_toy.py      (writes experiments/pn_toy.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from numba import njit, prange
from scipy.optimize import curve_fit

OUT = Path(__file__).with_suffix(".json")
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
def simulate(rates, n_orn, trials, bias, w, fa, ta, fb, tb, d, j_fast, j_slow, settle_steps, bin_steps, seed, silent):
    """Each trial: settle at rates[0] for settle_steps, then run rates (one per step); returns spike counts per bin
    (trials x bins) and the mean membrane potential over the run, and the mean strength left at the run's start."""
    n = rates.shape[0]
    nb = n // bin_steps
    counts = np.zeros((trials, nb))
    u_mean = np.zeros(trials)
    eff = np.zeros(trials)
    da, db, ds = np.exp(-DT / ta), np.exp(-DT / tb), np.exp(-DT / SLOW_TAU)
    dsyn, dslow, dm = np.exp(-DT / TAU_S), np.exp(-DT / TAU_SLOW), np.exp(-DT / TAU_M)
    for k in prange(trials):
        np.random.seed(seed + k)
        a = np.ones(n_orn)
        b = np.ones(n_orn)
        s = np.ones(n_orn)
        i_fast, i_slow, u, until = 0.0, 0.0, 0.0, -1
        for step in range(settle_steps + n):
            r = rates[0] if step < settle_steps else rates[step - settle_steps]
            if silent:
                r = 0.0
            p = r * DT
            for i in range(n_orn):
                a[i] = 1.0 - (1.0 - a[i]) * da
                b[i] = 1.0 - (1.0 - b[i]) * db
                s[i] = 1.0 - (1.0 - s[i]) * ds
                if np.random.random() < p:
                    strength = (w * a[i] + (1.0 - w) * b[i]) / d
                    i_fast += j_fast * strength
                    i_slow += j_slow * s[i] / d
                    a[i] -= (1.0 - fa) * a[i] / d
                    b[i] -= (1.0 - fb) * b[i] / d
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
    def __init__(self, n_orn=40, r0=6.0, w=0.5, fa=0.83, ta=7.5, fb=0.67, tb=0.3, d=1.0, uepsp=UEPSP_MV, trials=200, seed=1):
        self.n_orn, self.r0, self.w, self.fa, self.ta, self.fb, self.tb, self.d = n_orn, r0, w, fa, ta, fb, tb, d
        self.trials, self.seed = trials, seed
        self.j_fast = uepsp / peak_factor(TAU_S)
        self.j_slow = SLOW_CHARGE * self.j_fast * TAU_S / TAU_SLOW      # the slow current's charge 0.086 of the fast's
        self.bias = 0.0

    def run(self, rates: np.ndarray, settle_s: float, bin_s: float, silent: bool = False, trials=None, seed_off=0):
        return simulate(rates.astype(np.float64), self.n_orn, trials or self.trials, self.bias, self.w, self.fa, self.ta,
                        self.fb, self.tb, self.d, self.j_fast, self.j_slow, int(settle_s / DT), int(bin_s / DT),
                        self.seed + seed_off, silent)

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


CONDITIONS = [
    ("brainfly DM1-like: N 74, r0 6, M4", dict(n_orn=74, r0=6.0)),
    ("brainfly DL5-like: N 43, r0 6, M4", dict(n_orn=43, r0=6.0)),
    ("DL5 at its measured r0 14", dict(n_orn=43, r0=14.0)),
    ("DM4-like: N 32, r0 3.44, M4", dict(n_orn=32, r0=3.44)),
    ("slow pool share 0.88 (DM4's 0.26)", dict(n_orn=43, r0=6.0, w=0.88)),
    ("KW09 single pool (0.72, 2.4 s)", dict(n_orn=43, r0=6.0, w=1.0, fa=0.72, ta=2.4)),
    ("tonic divisor 2", dict(n_orn=43, r0=6.0, d=2.0)),
    ("tonic divisor 4 (Nagel's I_rest)", dict(n_orn=43, r0=6.0, d=4.0)),
    ("N 86 (twice the convergence)", dict(n_orn=86, r0=6.0)),
    ("N 86, tonic divisor 4", dict(n_orn=86, r0=6.0, d=4.0)),
    ("uEPSP 3.1 mV (half)", dict(n_orn=43, r0=6.0, uepsp=3.1)),
    ("r0 3, N 43", dict(n_orn=43, r0=3.0)),
    ("DM4-like, tonic divisor 2", dict(n_orn=32, r0=3.44, d=2.0)),
    ("DM4-like, tonic divisor 2.5", dict(n_orn=32, r0=3.44, d=2.5)),
    ("DM1-like at its measured r0 9, divisor 2", dict(n_orn=74, r0=9.0, d=2.0)),
    ("DM1-like at r0 9, divisor 3", dict(n_orn=74, r0=9.0, d=3.0)),
    ("DL5-like, divisor 2, female N 48", dict(n_orn=48, r0=6.0, d=2.0)),
    ("DL5-like, divisor 2, female N 48, r0 14", dict(n_orn=48, r0=14.0, d=2.0)),
]


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": {"drive_mv": [5, 10], "dl5_points": FLY_DL5, "dl5_fit": [167, 11.8], "late_over_peak": 0.44},
           "conditions": []}
    for name, kw in CONDITIONS:
        out["conditions"].append(evaluate(name, **kw))
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
