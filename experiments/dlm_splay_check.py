"""Exploratory check, not pre-registered and not a change to the model: can brainfly's neurons, coupled as flies' flight
motor neurons are, fire in flies' splay state?

Flies' five DLM motor neurons (MN1-5) fire in flight at one rate per fly, 4.5-8 Hz (ISI CV 0.22). They avoid firing
together (Hürkey et al. 2023; research_notes/Rung 8 flight data/dlm_splay_state.md):
- Splayness over the five is 0.76 (0.73-0.79, n = 8); independent phases give 0.59.
- MN1-4 fire in the order 1423 or 1324 in 48-70% of 4-spike windows; the strongly coupled pairs sit opposite.
- MN2 fires at 0.42-0.61 of MN1's cycle.
- MN5 avoids MN4's spikes: sync index r 0.56 and dip10 0.06, against 0.637 and 0.20 for independent phases.
With the electrical synapses knocked down (shakB RNAi), rates are unchanged and the phases are about random: r 0.61,
dip10 0.24, no preferred order. The coupling is weak and measured: coupling coefficient (CC) 0.023 between MN1-2 and
MN3-4, 0.011 between the other MN1-4 pairs; MN5's was never measured. In Hürkey et al.'s model, weak coupling
desynchronizes neurons whose phase-response curve falls through mid-cycle. Flies' curve was never measured.
brainfly's neurons are leaky integrators, and its electrical synapses were spikelets only, which theory predicts
synchronize. HybridBrain.set_coupling now gives them as conductances, which also carry a partner's subthreshold voltage
and its reset after a spike. A toy in the scratchpad suggested this desynchronizes neurons that share input.
Model: five neurons with brainfly's spiking unit as the whole-brain model sets it: 20 ms membrane, threshold 7 mV above
rest, reset 5 mV below rest (rest_calibration2.py), refractory 2.2 ms. They are alone, with no network. Each gets the
same steady drive (bias) and independent Poisson kicks of 0.1 mV, Hürkey et al.'s drive: one shared steady input,
independent noise. The drive is set so the uncoupled neurons fire at 6.6 Hz (Hürkey's model; flies 4.5-8), and the
kicks' rate so their ISI CV is flies' 0.22. Both are found by bisection on the uncoupled neurons, before any coupled
run. Conditions:
  uncoupled         (shakB)
  measured          conductances at the measured CCs: 0.023 for MN1-2 and MN3-4, 0.011 for the other MN1-4 pairs, and
                    MN5 to each of MN1-4 at half the others' mean (0.0075), as Hürkey's model takes it
  model's           at Hürkey et al.'s model's CCs (0.0099, 0.0044, 0.0031)
  measured x 3      the measured CCs three times over
  + spikelet        measured, plus each spike's own depolarization as a spikelet. Flies' overshoot passes at CC 0.01,
                    about 0.75 mV for about 1 ms. Here it is the jump with the same area over the 20 ms membrane,
                    0.0375 mV, for every coupled pair alike.
Measured as Hürkey et al.'s code measures, from 300 s per run after 3 s, 8 runs (seeds 4400 + condition):
- splayness over the five;
- r and dip10 for MN4-MN5;
- MN2's phase in MN1's cycle (circular mean and vector strength), and MN4's in MN3's;
- the share of 4-spike windows of MN1-4 in each cyclic order;
- rates and ISI CV;
- the share of each neuron's spikes within 3 ms of another's, against chance.

    python experiments/dlm_splay_check.py      (writes experiments/dlm_splay_check.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly.hybrid import HybridBrain

OUT = Path(__file__).with_suffix(".json")
DT = 1e-4
N = 5
SECONDS, BURN, RUNS, SEED = 300.0, 3.0, 8, 4400
CHUNK = 100_000                                     # steps recorded at a time (10 s)
UNIT = {"tau_m": 0.02, "threshold": 7.0, "reset": -5.0, "refractory": 0.0022}
KICK_MV = 0.1
TARGET_HZ, TARGET_CV = 6.6, 0.22
FLIES = {"rate_hz": [4.5, 8.0], "isi_cv": 0.22, "splayness": [0.73, 0.79], "splayness_random": 0.59,
         "r_mn4_mn5": [0.49, 0.63], "dip10": [0.02, 0.10], "r_random": 0.637, "dip10_random": 0.20,
         "mn2_phase_in_mn1": [0.42, 0.61], "preferred_order_share": [0.48, 0.70],
         "shakb": {"r_mn4_mn5": [0.56, 0.72], "dip10": [0.18, 0.41], "splayness": [0.52, 0.69]}}
STRONG = {(0, 1), (2, 3)}                           # MN1-2 and MN3-4 (indices 0-3); MN5 is index 4
SPIKELET_MV = 0.75 * 1e-3 / 0.02                    # 0.75 mV for 1 ms, as the same area over the 20 ms membrane


def ratios(strong: float, weak: float, mn5: float) -> sparse.csr_matrix:
    """The conductance matrix (g_c / g_L, both ways) for coupling coefficients strong, weak and MN5's."""
    rows, cols, vals = [], [], []
    for i, j in combinations(range(N), 2):
        cc = mn5 if 4 in (i, j) else strong if (i, j) in STRONG else weak
        if cc > 0:
            r = cc / (1 - cc)
            rows += [i, j]
            cols += [j, i]
            vals += [r, r]
    return sparse.csr_matrix((np.array(vals, np.float32), (rows, cols)), shape=(N, N))


def brain(bias: float, kick_hz: float, coupling=None, spikelet: float = 0.0) -> HybridBrain:
    labels = {"cell_type": np.array([f"MN{k + 1}" for k in range(N)]), "side": np.array(["R"] * N),
              "superclass": np.array(["motor"] * N)}
    gap = None
    if spikelet and coupling is not None:
        c = coupling.tocoo()
        gap = sparse.csr_matrix((np.full(len(c.data), spikelet, np.float32), (c.row, c.col)), shape=(N, N))
    return HybridBrain(matrix=sparse.csr_matrix((N, N), dtype=np.float32), labels=labels, trials=RUNS, dt=DT, w_syn=1.0,
                       types={"all": {**UNIT, "bias": bias, "noise_rate": kick_hz, "noise_kick": KICK_MV}},
                       coupling=coupling, gap=gap)


def spike_times(b: HybridBrain, seconds: float, seed: int) -> list[list[np.ndarray]]:
    """Each run's spike times (s) for each neuron, from `seconds` of activity after BURN s."""
    b.reset(seed)
    b.advance(int(round(BURN / DT)))
    times = [[[] for _ in range(N)] for _ in range(RUNS)]
    done = 0
    total = int(round(seconds / DT))
    while done < total:
        k = min(CHUNK, total - done)
        _, sp = b.advance(k, record=np.arange(N))
        for r, step, i in zip(*np.nonzero(sp)):
            times[r][i].append((done + step) * DT)
        done += k
    return [[np.array(t) for t in run] for run in times]


def phases(times: list[np.ndarray], step: float = 1e-3) -> np.ndarray:
    """Each neuron's phase, (t - t_n) / (t_n+1 - t_n), every `step` s, from the last neuron's first spike to the first
    neuron's last spike (Hürkey et al.'s window)."""
    t0, t1 = max(t[0] for t in times), min(t[-1] for t in times)
    grid = np.arange(t0, t1, step)
    out = np.empty((len(times), len(grid)))
    for i, t in enumerate(times):
        k = np.clip(np.searchsorted(t, grid, side="right") - 1, 0, len(t) - 2)
        out[i] = (grid - t[k]) / (t[k + 1] - t[k])
    return out


def splayness(ph: np.ndarray) -> float:
    """1 - sqrt(mean over time of N/(N-1) x sum of (gap - 1/N)^2), the gaps between the sorted phases (Hürkey's eq. 7)."""
    n = ph.shape[0]
    s = np.sort(ph, axis=0)
    gaps = np.diff(np.vstack([s, s[:1] + 1.0]), axis=0)
    r = n / (n - 1) * ((gaps - 1.0 / n) ** 2).sum(0)
    return float(1.0 - np.sqrt(r.mean()))


def sync_index(ph: np.ndarray, i: int, j: int) -> float:
    return float(np.mean(np.abs(np.cos(np.pi * (ph[i] - ph[j])))))


def phase_of(times: list[np.ndarray], i: int, j: int) -> np.ndarray:
    """The phase of each of j's spikes within i's interspike interval."""
    ti, tj = times[i], times[j]
    k = np.searchsorted(ti, tj, side="right") - 1
    ok = (k >= 0) & (k < len(ti) - 1)
    return (tj[ok] - ti[k[ok]]) / (ti[k[ok] + 1] - ti[k[ok]])


def orders(times: list[np.ndarray]) -> dict:
    """The share of 4-spike windows of MN1-4's merged train in each cyclic order (starting at MN1), and the rest."""
    lab = np.concatenate([np.full(len(times[i]), i + 1) for i in range(4)])
    lab = lab[np.argsort(np.concatenate(times[:4]), kind="stable")]
    count, total = {}, 0
    for k in range(len(lab) - 3):
        w = lab[k:k + 4]
        total += 1
        if len(set(w)) < 4:
            count["rest"] = count.get("rest", 0) + 1
            continue
        start = int(np.flatnonzero(w == 1)[0])
        key = "".join(str(x) for x in np.roll(w, -start))
        count[key] = count.get(key, 0) + 1
    return {k: round(v / total, 4) for k, v in sorted(count.items())}


def coincidences(times: list[np.ndarray], window: float = 0.003) -> float:
    """Spikes within `window` of another neuron's spike, as a multiple of what independent trains at the same rates give."""
    t_all = np.concatenate(times)
    span = max(t[-1] for t in times) - min(t[0] for t in times)
    seen, expected = 0, 0.0
    for i, t in enumerate(times):
        others = np.sort(np.concatenate([times[j] for j in range(len(times)) if j != i]))
        k = np.searchsorted(others, t)
        near = np.minimum(np.abs(t - others[np.clip(k - 1, 0, len(others) - 1)]),
                          np.abs(others[np.clip(k, 0, len(others) - 1)] - t))
        seen += int((near <= window).sum())
        expected += len(t) * (1 - np.exp(-len(others) / span * 2 * window))
    del t_all
    return round(seen / max(expected, 1e-9), 3)


def measure(runs: list[list[np.ndarray]]) -> dict:
    rows = []
    for times in runs:
        ph = phases(times)
        p12, p34 = phase_of(times, 0, 1), phase_of(times, 2, 3)
        circ = lambda p: (round(float(np.angle(np.mean(np.exp(2j * np.pi * p))) / (2 * np.pi) % 1.0), 3),
                          round(float(np.abs(np.mean(np.exp(2j * np.pi * p)))), 3))
        isi = [np.diff(t) for t in times]
        o = orders(times)
        rows.append({"rate_hz": [round(len(t) / SECONDS, 2) for t in times],
                     "isi_cv": [round(float(d.std() / d.mean()), 3) for d in isi],
                     "splayness": round(splayness(ph), 4),
                     "r_mn4_mn5": round(sync_index(ph, 3, 4), 4),
                     "dip10": round(float(np.mean((lambda p: (p < 0.1) | (p >= 0.9))(phase_of(times, 3, 4)))), 4),
                     "mn2_in_mn1": circ(p12), "mn4_in_mn3": circ(p34),
                     "orders": o, "preferred_order_share": round(o.get("1423", 0) + o.get("1324", 0), 4),
                     "coincidence_vs_chance_3ms": coincidences(times)})
    keys = ("splayness", "r_mn4_mn5", "dip10", "preferred_order_share", "coincidence_vs_chance_3ms")
    summary = {k: [round(float(np.median([r[k] for r in rows])), 4), round(float(min(r[k] for r in rows)), 4),
                   round(float(max(r[k] for r in rows)), 4)] for k in keys}
    summary["rate_hz"] = round(float(np.mean([np.mean(r["rate_hz"]) for r in rows])), 2)
    summary["isi_cv"] = round(float(np.mean([np.mean(r["isi_cv"]) for r in rows])), 3)
    summary["mn2_in_mn1"] = [round(float(np.median([r["mn2_in_mn1"][0] for r in rows])), 3),
                             round(float(np.median([r["mn2_in_mn1"][1] for r in rows])), 3)]
    return {"summary": summary, "runs": rows}


def calibrate() -> dict:
    """The bias for 6.6 Hz and the kicks' rate for an ISI CV of 0.22, on the uncoupled neurons (60 s, the first 4
    runs' seeds): for each kick rate on a bisection, the bias that gives 6.6 Hz, also by bisection."""
    def stats(bias, hz):
        t = spike_times(brain(bias, hz), 60.0, SEED - 1)
        rates = np.mean([[len(x) / 60.0 for x in run] for run in t])
        cvs = [np.diff(x).std() / np.diff(x).mean() for run in t for x in run if len(x) > 2]
        cv = np.mean(cvs) if cvs else 0.0
        return float(rates), float(cv)

    def bias_for(hz):
        mean_kick = hz * KICK_MV * UNIT["tau_m"]           # the kicks' mean depolarization, mV
        lo, hi = 7.0 - mean_kick - 3.0, 7.0 - mean_kick + 3.0
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            rate, cv = stats(mid, hz)
            lo, hi = (mid, hi) if rate < TARGET_HZ else (lo, mid)
        return 0.5 * (lo + hi), rate, cv

    trail = []
    lo, hi = 50.0, 20000.0                                  # kick rates, Hz: more kicks, more noise, higher CV
    for _ in range(12):
        mid = float(np.sqrt(lo * hi))
        bias, rate, cv = bias_for(mid)
        trail.append({"kick_hz": round(mid, 1), "bias_mv": round(bias, 4), "rate_hz": round(rate, 2), "isi_cv": round(cv, 3)})
        print("calibrate", json.dumps(trail[-1]), flush=True)
        lo, hi = (mid, hi) if cv < TARGET_CV else (lo, mid)
    best = min(trail, key=lambda x: abs(x["isi_cv"] - TARGET_CV) + abs(x["rate_hz"] - TARGET_HZ) / TARGET_HZ)
    return {"chosen": best, "trail": trail}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": FLIES, "unit": UNIT, "kick_mv": KICK_MV}
    out["calibration"] = cal = calibrate()
    bias, hz = cal["chosen"]["bias_mv"], cal["chosen"]["kick_hz"]
    measured = ratios(0.023, 0.011, 0.0075)
    conditions = [("uncoupled", None, 0.0), ("measured", measured, 0.0), ("model's", ratios(0.0099, 0.0044, 0.0031), 0.0),
                  ("measured x 3", ratios(0.069, 0.033, 0.0225), 0.0), ("+ spikelet", measured, SPIKELET_MV)]
    out["conditions"] = {}
    for c, (name, coupling, spikelet) in enumerate(conditions):
        runs = spike_times(brain(bias, hz, coupling, spikelet), SECONDS, SEED + c)
        out["conditions"][name] = measure(runs)
        print(name, json.dumps(out["conditions"][name]["summary"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
