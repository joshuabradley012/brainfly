"""Exploratory check, not pre-registered: what in the Kenyon cell input's timing wastes MBON11's input? Coincident volleys
across Kenyon cells, or each Kenyon cell's own burst?

odor_probe32.py: the same mean drive given as a steady current adds about twice the spikes the odor's Kenyon cell input
does (163 against 72 to 3-octanol, 50 against 27 to 4-methylcyclohexanol), and MBON11's other inputs don't matter.
Model: odor_probe30.py's brain (brain_cache.py) with odor_probe31.py's Kenyon cell-to-MBON11 synapses (0.030 pC per
synapse). For 3-octanol and 4-methylcyclohexanol (2 seeds of 8 flies), the Kenyon cells' spikes in 1 ms bins over the
odor's first 1.4 s, and:
  1. each responding Kenyon cell's spikes (cells with at least 2 spikes in a fly): how many, the share of its
     intervals under 10 and under 20 ms, its first spike's time, and the spread of its spike times;
  2. coincidence: within each 50 ms window, the variance of MBON11's Kenyon cell input across its 1 ms bins (summed over
     Kenyon cells, each weighted by its synapses onto the cell) against what independent Poisson cells with the same
     window counts would give; a ratio near 1 means independent, above 1 coincident (mean over the odor's windows with
     input, over flies and both MBON11s);
  3. bursts: the share of the input's synapse-weighted spikes that come within 20 ms of the same Kenyon cell's previous
     spike.
Seeds 300000 + 10 x odor + seed.

    python experiments/odor_kc_timing.py       (writes experiments/odor_kc_timing.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe24 as p24

OUT = Path(__file__).with_suffix(".json")
SEED = 300000
ODORS = ("3-octanol", "4-methylcyclohexanol")
SEEDS = 2
MS = 0.001
WINDOW = 50                                       # ms


def record(o, rec, odor: str, seed: int, kc: np.ndarray) -> np.ndarray:
    """Kenyon cells' spike counts per 1 ms over the odor's first 1.4 s: (ms, flies, cells), int16."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(2.0 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    per_ms = int(round(MS / b.dt))
    out = np.zeros((1400, b.trials, len(kc)), np.int16)
    for k in range(1400):
        out[k] = b.advance(per_ms, drive=rec.at(plan, (k // 10) * p10.PIECE))[:, kc]    # the drive changes every 10 ms
    return out


def measures(S: np.ndarray, syn: np.ndarray) -> dict:
    T, F, N = S.shape
    total = S.sum(0)                                                      # (flies, cells)
    cells = [[], [], [], [], []]                                          # count, <10 ms, <20 ms, first spike, spread
    burst_w, all_w = 0.0, 0.0
    weight = syn.sum(1)                                                   # each Kenyon cell's synapses onto both MBON11s
    for f in range(F):
        for i in np.flatnonzero(total[f] >= 2):
            times = np.repeat(np.arange(T), S[:, f, i]).astype(float)
            isi = np.diff(times)
            cells[0].append(len(times))
            cells[1].append(float((isi < 10).mean()))
            cells[2].append(float((isi < 20).mean()))
            cells[3].append(times[0])
            cells[4].append(float(times.std()))
        spikes = np.flatnonzero(total[f] >= 1)
        for i in spikes:                                                  # bursts, weighted by synapses
            times = np.repeat(np.arange(T), S[:, f, i]).astype(float)
            close = np.concatenate([[False], np.diff(times) < 20])
            burst_w += weight[i] * close.sum()
            all_w += weight[i] * len(times)
    ratios = []
    for f in range(F):
        I = S[:, f, :].astype(np.float64) @ syn                           # (ms, cells): synapse-weighted input per ms
        for w0 in range(0, T, WINDOW):
            block = S[w0:w0 + WINDOW, f, :].sum(0).astype(np.float64)    # each Kenyon cell's spikes in the window
            for j in range(syn.shape[1]):
                expected = (block * syn[:, j] ** 2).sum() / WINDOW        # independent Poisson: sum_i r_i w_i^2
                if expected > 0 and block[syn[:, j] > 0].sum() >= 5:
                    ratios.append(float(I[w0:w0 + WINDOW, j].var() / expected))
    c = [np.array(x) for x in cells]
    return {"responding_cells_per_fly": round(len(c[0]) / F, 1), "spikes_per_responding_cell": round(float(c[0].mean()), 2),
            "share_of_intervals_under_10ms": round(float(c[1].mean()), 3), "share_of_intervals_under_20ms": round(float(c[2].mean()), 3),
            "first_spike_ms_median": round(float(np.median(c[3])), 1), "spike_time_spread_ms_median": round(float(np.median(c[4])), 1),
            "coincidence_ratio_mean": round(float(np.mean(ratios)), 2), "coincidence_ratio_median": round(float(np.median(ratios)), 2),
            "windows": len(ratios), "input_share_from_bursts": round(burst_w / all_w, 3) if all_w else None}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types, m = o.brain, o.types, o.m
    kc, mb = np.flatnonzero(m["kc"]), np.flatnonzero(types == "MBON11")
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mb))
    syn = np.zeros((len(kc), len(mb)))
    np.add.at(syn, (np.searchsorted(kc, pre[onto]), np.searchsorted(mb, b.idx[onto])), b._counts[onto])
    out = {"question": __doc__, "flies": {"spikes_per_response": {"alpha/beta": "2.2 +- 1.2", "alpha'/beta'": "4.9 +- 3.0"}}, "odors": {}}
    for j, odor in enumerate(ODORS):
        S = np.concatenate([record(o, rec, odor, SEED + 10 * j + s, kc) for s in range(SEEDS)], axis=1)
        out["odors"][odor] = measures(S, syn)
        print(odor, json.dumps(out["odors"][odor]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
