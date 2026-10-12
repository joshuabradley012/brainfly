"""Exploratory check, written before it runs, not pre-registered and not a change to the model: Hürkey et al.'s own
conductance model of the flight motor neurons, measured as dlm_splay_check6.py measures.

dlm_splay_check6.py and dlm_splay_check7.py: leaky-integrator units at flies' coupling, firing at one rate, give flies'
splayness (0.73-0.75), firing orders and sub-chance coincidences, and the strongly coupled pairs (and MN5's, with MN5 at
1.26 times the others' rate) come out about as flies'. But the weakly coupled MN1-4 pairs come within 10 ms of each
other 1.6-3 times as often as flies' (0.50-0.59 against 0.16-0.31 times chance; dip10 0.09-0.10 against 0.03-0.06),
and 24-30% of 4-spike windows hold a repeat (flies 5-20%). Hürkey et al. 2023 explained the splay state with a
three-variable conductance model (Berger & Crook 2015's Na and Shab-like K currents) near the small saddle-node-loop
point. Its phase response falls through phase 0.5, so weak electrical synapses push pairs apart; a leaky integrator's
phase response doesn't fall. Their model used conductances 2.3 times weaker than flies' measured coupling (taking it as
steady-state coefficients), and independent noise set so that splayness came out at flies' 0.76
(research_notes/Rung 8 flight data/dlm_splay_state.md, sections 1.8 and 3).
Model: five identical units with the published equations and parameters (section 1.8: C 0.13 nF, g_Na 0.4312 uS, g_L
8.624 nS, g_shab 0.13768216 uS, E_L -60, E_K -72, E_Na 55 mV, the gates of their Supplementary Table 3), joined by linear,
symmetric electrical synapses, each unit with its own constant drive and independent white-noise current. Integrated by
Heun's method at 10 us (checked against 3 us below); spikes counted at upward crossings of -10 mV with a 10 ms dead time,
as theirs were. Four conditions:
- A, as published: the published conductances (86.59 pS between MN1-2 and between MN3-4, 38.27 pS between the other
  MN1-4 pairs, 27.19 pS for MN5's), 108.75 pA for every unit, noise 0.949 pA ms^0.5.
- B, flies' coupling: conductances fitted so that a 20 ms step of -20 pA into one resting unit gives its partner flies'
  peak ratio (0.023, 0.011, and MN5's assumed 0.0075, as dlm_splay_check5.py fitted the leaky integrator's), noise as
  A, and each unit's drive found by bisection so that all five fire at 6.6 Hz (dlm_splay_check6.py's rate).
- C, flies' coupling and irregularity: as B, with the noise set so that an uncoupled unit at 6.6 Hz has flies' ISI CV
  of 0.22 (as dlm_splay_check2.py set the leaky integrator's kicks), and the drives found again.
- D, published coupling, flies' irregularity: A's conductances with C's noise, the drives found as in B.
The drives are bisected all at once, in dlm_splay_check7.py's two passes (the second re-brackets each unit at its first
drive plus or minus 0.2 pA), on 8 runs of 60 s; each unit's calibration rate must end within 2% of 6.6 Hz, or the
condition is reported as failing calibration.
Before the runs, the implementation is checked against the paper's own numbers: without noise or coupling, a unit at
108.75 pA fires at 6.59 Hz, swinging between about -49 and +3 mV; the SNIC parameters (g_shab 0.2156 uS, 175 pA) give
6.56 Hz; at no drive the unit rests near -61.5 mV. And condition A on 2 runs of 60 s at 10 against 3 us steps: if their rates or
CVs differ by more than 2%, everything after runs at 3 us.
Measured as dlm_splay_check6.py measures (8 runs of 300 s after 3 s, seeds 4900 + 10 x condition), with each unit's rate
and CV, and the ten pairs against flies'. For A, Hürkey et al.'s Fig. 3j gives 1423 about 0.42, 1324 about 0.35, the
other four orders 0.04-0.05 and repeats about 0.03, and their ED Fig. 6a splayness about 0.76.
Read: if B or C puts the weakly coupled MN1-4 pairs inside flies' ranges (dip10 0.030-0.056, within 10 ms 0.16-0.31
times chance), where the leaky integrators at the same coupling didn't, their shortfall comes from the units' type (the
leaky integrator's phase response), and brainfly's flight motor neurons would need units whose phase response falls, a
question for the kernel. If neither does, the weak pairs need something neither model has.

Ran (2026-10-11, 6.5 minutes): neither B nor C puts the weakly coupled pairs inside flies' ranges, and neither holds a
fly-like rate. So by the reading, the weak pairs need something neither model has. Hürkey et al.'s model, as published,
falls short on those pairs just as the leaky integrators do.
- The implementation matches the paper: 6.593 Hz at 108.75 pA, swinging from -49.25 to +2.82 mV; SNIC 6.561 Hz; rest
  -61.23 mV. 10 us and 3 us steps agree within 0.4% (8.47 against 8.50 Hz, CV 0.066 against 0.066).
- The published conductances give 20 ms peak ratios of 0.0055, 0.0024 and 0.0017, 0.55 of their steady-state
  coefficients. Flies' peak ratios need 0.367, 0.174 and 0.118 nS (steady-state 0.041, 0.020, 0.013), 4.2 times the
  published ones. Flies' ISI CV of 0.22 needs noise of 2.30 pA ms^0.5, 2.4 times the published 0.949 (an uncoupled unit
  at 108.8 pA then fires at 6.57 Hz).
- A, as published: MN1-4 fire at 8.68 Hz and MN5 at 7.81 (same drive, weaker coupling), with ISI CV 0.064-0.071 (flies
  0.22).
  - Splayness 0.713 (the paper's ED Fig. 6a about 0.76). Preferred orders 0.81 (1423 0.42, 1324 0.40; the paper's Fig.
    3j 0.42 and 0.35), with repeats 0.023 (about 0.03).
  - Strong pairs: r 0.25, dip10 0.000, within 10 ms 0.00 times chance, locked more tightly than flies' (0.34-0.39,
    0.006-0.025, 0.05-0.20).
  - Weak MN1-4 pairs: r 0.65-0.66, dip10 0.10-0.11, within 10 ms 0.55-0.59 times chance (flies 0.60-0.67, 0.030-0.056,
    0.16-0.31). These are the leaky integrators' numbers at flies' coupling (dlm_splay_check6.py: dip10 0.09-0.10,
    0.50-0.59).
  - MN5's pairs: dip10 0.19-0.20, within 10 ms 1.03-1.06 (flies 0.063-0.141, 0.34-0.58). Slower than the others, MN5
    drifts through them.
- B and C, flies' coupling: both fail calibration. The 60 s calibration runs end at 5.86 and 7.71 Hz (MN5 4.77 and
  6.22); the 300 s runs give 8.8-14.6 and 10.1-13.9 Hz, with MN5's ISI CV 2.1-2.4.
  - B, in those runs: a rigid four-cycle, with 1324 in 99.7% of one run's windows and splayness 0.774. The weak pairs
    come within 10 ms at 0.073-0.079 times chance, below flies'.
  - C: organized as A (splayness 0.713, preferred orders 0.85, repeats 0.023), with the weak pairs at 0.72-0.83 times
    chance and dip10 0.09-0.10, above flies'.
- D, published coupling at flies' irregularity: calibrated (6.58-6.62 Hz, CV 0.21-0.22), and barely organized.
  Splayness 0.642 (independent phases 0.59), preferred orders 0.31, repeats 0.21. Within 10 ms: strong pairs 0.61
  times chance, weak 0.90-0.95, MN5's 0.94-0.99.
So a falling phase response alone doesn't give flies' weak pairs. Hürkey et al.'s model, as published, leaves them where
the leaky integrators at flies' coupling do, while firing three times more regularly than flies'. At
flies' irregularity, its published coupling barely organizes the five. At flies' measured coupling it doesn't fire at a
fly-like rate (below).

Checked afterwards (2026-10-11, the same code, not part of the plan above):
- B's and C's own drives, rates in 30 s bins over 300 s, on the calibration and main seeds: the coupled units start
  nearly silent (MN1's median 0.0-1.8 Hz over the first 30 s). Within 30-60 s they switch to a self-sustained cycle at
  about 14-15 Hz, which lasts to the end (one of C's 16 runs fell back to 4 Hz in its last 30 s). The 60 s calibration
  averaged the two states.
- With all five at one drive, flies' coupling, 8 runs of 180 s (seed 77), at either noise: from 96 to 108 pA the units
  stay silent throughout. From 108.25 pA they fire from the start, in every run: 15.3-15.6 Hz at 108.25, rising to
  21.2-21.3 at 109.75, and 22, 27, 34, 40 and 50 Hz at 110, 112, 116, 120 and 130 pA (MN5 18-47). None of these drives
  gives flies' 4.5-8 Hz. Between 108 and 108.25 pA, B's and C's drives switch from silence to about 14-15 Hz.

Correction (2026-10-12, review 12):
- The reading's test didn't run as planned. B and C failed calibration, so their runs aren't at 6.6 Hz, and "by the
  reading" above draws on conditions the reading wasn't written for.
- A isn't like for like with the leaky integrators at flies' coupling (dlm_splay_check6.py). It differs in three ways:
  - about a quarter of flies' 20 ms coupling (peak ratios 0.24, 0.22 and 0.23 of flies');
  - a third of their irregularity (CV 0.064 against 0.22);
  - MN1-4 at 8.68 Hz, with MN5 at 0.90 times them.
  So its weak pairs landing near the leaky integrators' compares nothing about phase responses. dlm_splay_check11.py ran
  the leaky integrators at A's and D's coupling, irregularity and rates. They hold the weak pairs apart better than
  Hürkey et al.'s model: 0.33-0.38 against 0.55-0.59 times chance as A, 0.60-0.67 against 0.90-0.95 as D. So the
  conclusion's direction holds for this model, and more strongly, but not on the basis the Ran gave. As corrected:
  Hürkey et al.'s falling phase response holds the weak pairs apart no better than the leaky integrator at the same
  coupling and irregularity, and at flies' coupling it can't be run at a fly-like rate.
- B's result, weak pairs over-separated, comes from its low noise. At flies' coupling and A's noise, review 12 found the
  leaky integrators over-separating them too.
- "Silent, or 14 Hz and faster" misses a bistable branch. Once firing, the network keeps firing down to 107.45-107.6 pA
  at 9-11 Hz (MN5 5-7 Hz) before it stops (dlm_splay_check11.py, part 3). No drive tried gives all five 4.5-8 Hz.
- The first "Checked afterwards" bullet has two errors:
  - The switch from silence comes at 0-115 s in B's main runs and 0-77 s in C's (dlm_splay_check11.py, part 4), not
    "within 30-60 s".
  - The run said to have "fell back to 4 Hz in its last 30 s" (C, calibration seed, run 1) was silent until 291 s and
    then fired at 14 Hz (review 12).
- The implementation also reproduces the paper's network values with its homogeneous coupling: splayness 0.761 and
  0.679, MN4-MN5 0.564 (dlm_splay_check11.py, part 1). A's 0.713 against "about 0.76" compares the heterogeneous
  coupling, which slows MN5 to 0.90 times MN1-4, with a figure made with homogeneous coupling. The published coupling
  raises the units from 6.56 to 8.4-8.7 Hz.
- Numbers:
  - The fitted conductances are 4.24, 4.53 and 4.34 times the published ones: 4.2-4.5 times, not "4.2 times".
  - "(dlm_splay_check6.py: dip10 0.09-0.10, 0.50-0.59)" are dlm_splay_check7.py's ranges. Check 6's weak pairs are at
    dip10 0.086-0.094 and within 10 ms 0.50-0.52.
  - In B every run locks into one order, not one run: 1324 in five runs, 1423 in three, 99.2-100% of windows.
  - "The 300 s runs give 8.8-14.6 and 10.1-13.9 Hz" are MN1-4's, averaging a silent start with the firing state. After
    the switch they fire at 14.3-14.6 and 13.5-13.9 Hz.
  - On the firing part alone, C's weak pairs are at 0.68-0.74 times chance and B's at 0.062-0.071 (review 12).
  - In C's main runs MN1-4's CV is 0.10-0.11, half flies'. Only the noise was set for flies' CV, on an uncoupled unit
    at 6.6 Hz.
  - "The paper's own numbers" (6.59 Hz, -61.5 mV) are the notes' derivations from the authors' code and saved run.

Correction (2026-10-12, review 13):
- The background above says "the strongly coupled pairs (and MN5's, with MN5 at 1.26 times the others' rate) come out
  about as flies'". Neither holds:
  - dlm_splay_check7.py's MN5 fit came with MN5 far more regular than the others (dlm_splay_check10.py).
  - The strong pairs fall outside flies' ranges on all three measures: r 0.31 against 0.336-0.394, dip10 0.029-0.031
    against 0.006-0.025, within 10 ms 0.23 against 0.05-0.20.
- The review-12 correction gives B's and C's switch at 0-115 and 0-77 s, and their rates after it as 14.3-14.6 and
  13.5-13.9 Hz. Those come from dlm_splay_check11.py's part 4, which reports window starts. The onsets are 4-121 s in B
  and 0-83 s in C, then 14.8 and 13.9 Hz (review 13; review 12 had 4-121 and 0-83 s).
- "Silent, or 14 Hz and faster", quoted in that correction, was the README's phrase, not this check's.
- "The published coupling raises the units from 6.56 to 8.4-8.7 Hz" is MN1-4 (8.42-8.43 Hz homogeneous, 8.68
  heterogeneous). MN5 fires at 7.81 Hz under the heterogeneous coupling.

    python experiments/dlm_splay_check8.py      (writes experiments/dlm_splay_check8.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numba
import numpy as np

import dlm_splay_check as c1
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6

OUT = Path(__file__).with_suffix(".json")
SEED = 4900
CAL_SECONDS = 60.0
Q = 0.0392                                          # /mV
C_PF, G_NA, G_L = 130.0, 431.2, 8.624               # pF, nS, nS: currents in pA, time in ms, voltages in mV
E_L, E_K, E_NA = -60.0, -72.0, 55.0
M_Z, M_V = 3.0, -33.0
H_Z, H_V, H_R, H_G = 5.2, -39.14, 0.2, 0.38
B_Z, B_V, B_R, B_G = 1.1056, -42.14, 0.2, 0.38
G_SHAB = {"SNL": 137.68216, "SNIC": 215.6}          # nS
PUBLISHED = {"drive_pa": 108.75, "sigma_pa_ms05": 0.949, "g_ns": {"strong": 0.08659, "weak": 0.03827, "mn5": 0.02719}}
DT_MS = 0.01
SPIKE_MV, DEAD_MS = -10.0, 10.0
STATE = {"dt_ms": DT_MS}                           # 0.003 if the time-step check fails
STEP_PA, STEP_MS = -20.0, 20.0


@numba.njit(inline="always", cache=True)
def _derivs(v, h, b, drive, g, g_shab, dv, dh, db):
    n = len(v)
    for i in range(n):
        x = v[i]
        m = 1.0 / (1.0 + np.exp(-Q * M_Z * (x - M_V)))
        eh = np.exp(-Q * H_Z * (x - H_V))
        eb = np.exp(-Q * B_Z * (x - B_V))
        gap = 0.0
        for j in range(n):
            gap += g[i, j] * (v[j] - x)
        b2 = b[i] * b[i]
        cur = drive[i] - G_L * (x - E_L) - g_shab * b2 * b2 * (x - E_K) - G_NA * m * m * m * (1.0 - h[i]) * (x - E_NA) + gap
        dv[i] = cur / C_PF
        dh[i] = (1.0 / (1.0 + eh) - h[i]) * H_R * (1.0 + eh) / np.exp(-Q * H_Z * H_G * (x - H_V))
        db[i] = (1.0 / (1.0 + eb) - b[i]) * B_R * (1.0 + eb) / np.exp(-Q * B_Z * B_G * (x - B_V))


@numba.njit(inline="always", cache=True)
def _steady(v, h, b):
    for i in range(len(v)):
        h[i] = 1.0 / (1.0 + np.exp(-Q * H_Z * (v[i] - H_V)))
        b[i] = 1.0 / (1.0 + np.exp(-Q * B_Z * (v[i] - B_V)))


@numba.njit(parallel=True, cache=True)
def _simulate(drives, sigma, g, g_shab, dt, burn_steps, steps, seeds, v0, cap):
    """Spike times (s, from the end of the burn-in) per trial and unit; drives (trials, n) pA; sigma pA ms^0.5."""
    trials, n = drives.shape
    times = np.full((trials, n, cap), -1.0)
    counts = np.zeros((trials, n), np.int64)
    for r in numba.prange(trials):
        np.random.seed(seeds[r])
        v = v0[r].copy()
        h, b = np.empty(n), np.empty(n)
        _steady(v, h, b)
        k1v, k1h, k1b = np.empty(n), np.empty(n), np.empty(n)
        k2v, k2h, k2b = np.empty(n), np.empty(n), np.empty(n)
        vs, hs, bs, noise = np.empty(n), np.empty(n), np.empty(n), np.empty(n)
        last = np.full(n, -10 ** 12)
        above = np.zeros(n, np.bool_)
        dead = int(round(DEAD_MS / dt))
        amp = sigma * np.sqrt(dt) / C_PF
        d = drives[r]
        for s in range(burn_steps + steps):
            for i in range(n):
                noise[i] = amp * np.random.normal(0.0, 1.0)
            _derivs(v, h, b, d, g, g_shab, k1v, k1h, k1b)
            for i in range(n):
                vs[i] = v[i] + k1v[i] * dt + noise[i]
                hs[i] = h[i] + k1h[i] * dt
                bs[i] = b[i] + k1b[i] * dt
            _derivs(vs, hs, bs, d, g, g_shab, k2v, k2h, k2b)
            for i in range(n):
                v[i] += 0.5 * (k1v[i] + k2v[i]) * dt + noise[i]
                h[i] += 0.5 * (k1h[i] + k2h[i]) * dt
                b[i] += 0.5 * (k1b[i] + k2b[i]) * dt
                up = v[i] > SPIKE_MV
                if up and not above[i] and s - last[i] >= dead:
                    last[i] = s
                    if s >= burn_steps and counts[r, i] < cap:
                        times[r, i, counts[r, i]] = (s - burn_steps + 1) * dt * 1e-3
                        counts[r, i] += 1
                above[i] = up
    return times, counts


@numba.njit(cache=True)
def _trace(drive, g, g_shab, dt, burn_steps, steps, step_on, step_off, step_pa):
    """Without noise: two-unit (or one-unit) voltages after a burn-in, with step_pa added to unit 0 from step_on to
    step_off (steps after the burn-in); returns the voltages (steps, n)."""
    n = len(drive)
    v = np.full(n, -61.0)
    h, b = np.empty(n), np.empty(n)
    _steady(v, h, b)
    k1v, k1h, k1b = np.empty(n), np.empty(n), np.empty(n)
    k2v, k2h, k2b = np.empty(n), np.empty(n), np.empty(n)
    vs, hs, bs = np.empty(n), np.empty(n), np.empty(n)
    out = np.empty((steps, n))
    d = drive.copy()
    for s in range(burn_steps + steps):
        k = s - burn_steps
        d[0] = drive[0] + (step_pa if step_on <= k < step_off else 0.0)
        _derivs(v, h, b, d, g, g_shab, k1v, k1h, k1b)
        for i in range(n):
            vs[i] = v[i] + k1v[i] * dt
            hs[i] = h[i] + k1h[i] * dt
            bs[i] = b[i] + k1b[i] * dt
        _derivs(vs, hs, bs, d, g, g_shab, k2v, k2h, k2b)
        for i in range(n):
            v[i] += 0.5 * (k1v[i] + k2v[i]) * dt
            h[i] += 0.5 * (k1h[i] + k2h[i]) * dt
            b[i] += 0.5 * (k1b[i] + k2b[i]) * dt
        if k >= 0:
            out[k] = v
    return out


def matrix(g_ns: dict) -> np.ndarray:
    g = np.zeros((c1.N, c1.N))
    for i, j in combinations(range(c1.N), 2):
        g[i, j] = g[j, i] = g_ns[c5.pair_class(i, j)]
    return g


def runs(drives: np.ndarray, sigma: float, g: np.ndarray, seconds: float, seed: int, trials: int = c1.RUNS,
         dt: float | None = None, regime: str = "SNL") -> list[list[np.ndarray]]:
    dt = STATE["dt_ms"] if dt is None else dt
    rng = np.random.default_rng(seed)
    seeds = seed * 1000 + np.arange(trials)
    v0 = rng.uniform(-62.0, -48.0, (trials, len(drives)))
    d = np.broadcast_to(np.asarray(drives, np.float64), (trials, len(drives))).copy()
    times, counts = _simulate(d, sigma, g, G_SHAB[regime], dt, int(round(c1.BURN * 1e3 / dt)), int(round(seconds * 1e3 / dt)),
                              seeds, v0, int(seconds * 40))
    assert (counts < int(seconds * 40)).all(), "spike buffer full"
    return [[times[r, i, :counts[r, i]].copy() for i in range(len(drives))] for r in range(trials)]


def rates(drives: np.ndarray, sigma: float, g: np.ndarray, seed: int = SEED - 1) -> np.ndarray:
    rs = runs(drives, sigma, g, CAL_SECONDS, seed)
    return np.array([np.mean([len(r[i]) / CAL_SECONDS for r in rs]) for i in range(len(drives))])


def bisect_drives(sigma: float, g: np.ndarray, start: np.ndarray, half_range: float, iterations: int) -> np.ndarray:
    lo, hi = start - half_range, start + half_range
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        r = rates(mid, sigma, g)
        lo, hi = np.where(r < c1.TARGET_HZ, mid, lo), np.where(r < c1.TARGET_HZ, hi, mid)
    return 0.5 * (lo + hi)


def calibrated_drives(sigma: float, g: np.ndarray) -> dict:
    first = bisect_drives(sigma, g, np.full(c1.N, PUBLISHED["drive_pa"]), 30.0, 18)
    drives = bisect_drives(sigma, g, first, 0.2, 12)
    cal = rates(drives, sigma, g)
    return {"drives_pa": drives, "calibration_rates_hz": [round(float(x), 3) for x in cal],
            "calibrated_within_2pct": bool(np.all(np.abs(cal / c1.TARGET_HZ - 1) <= 0.02))}


def uncoupled_cv(sigma: float) -> tuple[float, float, float]:
    """An uncoupled unit's drive for 6.6 Hz at this noise (5 units x 8 runs of 60 s), its rate and its ISI CV."""
    g = np.zeros((c1.N, c1.N))
    lo, hi = 20.0, 200.0
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if rates(np.full(c1.N, mid), sigma, g).mean() < c1.TARGET_HZ else (lo, mid)
    drive = 0.5 * (lo + hi)
    rs = runs(np.full(c1.N, drive), sigma, g, CAL_SECONDS, SEED - 1)
    isi = [np.diff(r[i]) for r in rs for i in range(c1.N)]
    return drive, float(np.mean([len(r[i]) for r in rs for i in range(c1.N)]) / CAL_SECONDS), float(np.mean([d.std() / d.mean() for d in isi]))


def sigma_for_cv() -> dict:
    lo, hi, trail = np.log(0.2), np.log(40.0), []
    for _ in range(12):
        mid = 0.5 * (lo + hi)
        drive, rate, cv = uncoupled_cv(float(np.exp(mid)))
        trail.append({"sigma": round(float(np.exp(mid)), 4), "drive_pa": round(drive, 3), "rate_hz": round(rate, 3), "isi_cv": round(cv, 4)})
        lo, hi = (mid, hi) if cv < c1.TARGET_CV else (lo, mid)
    best = min(trail, key=lambda x: abs(x["isi_cv"] - c1.TARGET_CV))
    return {"sigma_pa_ms05": best["sigma"], "chosen": best, "trail": trail}


def peak_ratio(g_ns: float, step_pa: float = STEP_PA) -> float:
    """Two resting units joined by g_ns: a 20 ms step into the first; the second's peak change over the first's."""
    steps = int(round(80.0 / DT_MS))
    on, off = int(round(10.0 / DT_MS)), int(round((10.0 + STEP_MS) / DT_MS))
    g = np.array([[0.0, g_ns], [g_ns, 0.0]])
    v = _trace(np.zeros(2), g, G_SHAB["SNL"], DT_MS, int(round(500.0 / DT_MS)), steps, on, off, step_pa)
    dv = v - v[:on].mean(0)
    k = np.argmax(np.abs(dv[:, 0]))
    return float(np.abs(dv[:, 1]).max() / abs(dv[k, 0]))


def fitted_g(cc: float) -> float:
    lo, hi = 0.0, 2.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if peak_ratio(mid) < cc else (lo, mid)
    return 0.5 * (lo + hi)


def deterministic(regime: str, drive: float) -> dict:
    v = _trace(np.array([drive]), np.zeros((1, 1)), G_SHAB[regime], DT_MS, int(round(2000.0 / DT_MS)), int(round(10000.0 / DT_MS)),
               0, 0, 0.0)[:, 0]
    up = np.flatnonzero((v[1:] > SPIKE_MV) & (v[:-1] <= SPIKE_MV))
    return {"rate_hz": round(1e3 / (np.diff(up).mean() * DT_MS), 3), "v_min_mv": round(float(v.min()), 2), "v_max_mv": round(float(v.max()), 2)}


def implementation() -> dict:
    out = {"snl_108.75pA": deterministic("SNL", 108.75), "snic_175pA": deterministic("SNIC", 175.0),
           "rest_mv": round(float(_trace(np.zeros(1), np.zeros((1, 1)), G_SHAB["SNL"], DT_MS, int(round(2000.0 / DT_MS)), 10, 0, 0, 0.0)[-1, 0]), 2),
           "published_cc_steady": {k: round(v / (v + G_L), 5) for k, v in PUBLISHED["g_ns"].items()},
           "published_peak_ratio_20ms": {k: round(peak_ratio(v), 5) for k, v in PUBLISHED["g_ns"].items()}}
    g = matrix(PUBLISHED["g_ns"])
    d = np.full(c1.N, PUBLISHED["drive_pa"])
    step = {}
    for dt in (DT_MS, 0.003):
        rs = runs(d, PUBLISHED["sigma_pa_ms05"], g, 60.0, SEED - 2, trials=2, dt=dt)
        step[f"{dt * 1000:g}us"] = {"rate_hz": round(float(np.mean([len(t) / 60.0 for r in rs for t in r])), 3),
                                    "isi_cv": round(float(np.mean([np.diff(t).std() / np.diff(t).mean() for r in rs for t in r])), 4)}
    a, b = step["10us"], step["3us"]
    step["within_2pct"] = bool(abs(a["rate_hz"] / b["rate_hz"] - 1) <= 0.02 and abs(a["isi_cv"] / b["isi_cv"] - 1) <= 0.02)
    out["time_step"] = step
    if not step["within_2pct"]:
        STATE["dt_ms"] = 0.003
    out["dt_ms_used"] = STATE["dt_ms"]
    return out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies_pairs": c6.FLIES_PAIRS, "published": PUBLISHED, "conditions": {}}
    out["implementation"] = implementation()
    print("implementation", json.dumps(out["implementation"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["fitted_g_ns"] = {k: round(fitted_g(cc), 5) for k, cc in c5.CC.items()}
    out["fitted_steady_cc"] = {k: round(v / (v + G_L), 5) for k, v in out["fitted_g_ns"].items()}
    print("fitted", json.dumps({k: out[k] for k in ("fitted_g_ns", "fitted_steady_cc")}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["noise_for_cv"] = sigma_for_cv()
    print("noise", json.dumps(out["noise_for_cv"]["chosen"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    sig_cv = out["noise_for_cv"]["sigma_pa_ms05"]
    conditions = [("A, as published", PUBLISHED["g_ns"], PUBLISHED["sigma_pa_ms05"], False),
                  ("B, flies' coupling", out["fitted_g_ns"], PUBLISHED["sigma_pa_ms05"], True),
                  ("C, flies' coupling and irregularity", out["fitted_g_ns"], sig_cv, True),
                  ("D, published coupling, flies' irregularity", PUBLISHED["g_ns"], sig_cv, True)]
    for c, (name, g_ns, sigma, calibrate) in enumerate(conditions):
        g = matrix(g_ns)
        res = {"g_ns": g_ns, "sigma_pa_ms05": sigma}
        if calibrate:
            cal = calibrated_drives(sigma, g)
            drives = cal.pop("drives_pa")
            res.update(cal)
        else:
            drives = np.full(c1.N, PUBLISHED["drive_pa"])
        res["drives_pa"] = [round(float(x), 4) for x in drives]
        res.update(c6.summarize(runs(drives, sigma, g, c1.SECONDS, SEED + 10 * c)))
        out["conditions"][name] = res
        s = res["summary"]
        print(name, json.dumps({k: res.get(k) for k in ("calibrated_within_2pct", "calibration_rates_hz", "drives_pa", "unit_rates_hz", "unit_isi_cv")}),
              json.dumps({"splayness": s["splayness"][0], "preferred": s["preferred_order_share"][0], "repeats": s["repeat_share"],
                          "coincidence": s["coincidence_vs_chance_3ms"][0], "pairs": res["pairs"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
