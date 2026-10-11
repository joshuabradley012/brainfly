"""Exploratory check, not pre-registered and not a change to the model: Yamada et al. 2024's optogenetic flash in the
model. Does a brief activation of a few gamma Kenyon cells give MBON11 an EPSC with flies' time course, and with what
Kenyon cell membrane time constant would it?

mbon11_burst_check.py: the depression of the Kenyon cell-to-MBON11 synapses ends MBON11's odor response within 0.3 s,
where flies' holds; the depression comes from Yamada et al.'s paired flashes read as one Kenyon cell spike per flash.
Their flash EPSC (research_notes/Rung 9 learning data/mbon11_kc_activity.md 2.1 and mbon11_input.md 3.1: ex vivo, 1-ms
625-nm flashes 400 ms apart onto a random ~3-7% of gamma Kenyon cells expressing CsChrimson, MBON11 clamped at -60 mV
with Cs+ and QX-314) peaks 102-118 ms after the flash, is 235-260 ms wide at half its peak, keeps 0.32-0.39 of its peak at
400 ms and decays with a time constant of 256-333 ms over the 160 ms before the second flash; the second flash evokes
0.38-0.68 of the first (PPR, at 1.5 mM calcium). A 1 ms flash through CsChrimson, which closes with a time constant of
about 21 ms (Klapoetke et al. 2014), can't make so long an EPSC through fast synapses unless the Kenyon cells keep firing
for hundreds of milliseconds afterwards (the note's reading: "a compound response to prolonged KC activity after the
flash"). The model's Kenyon cells have Shiu et al.'s membrane time constant, 20 ms; Groschner et al. 2018 measured 118 ms
in alpha'/beta' and 189 ms in alpha/beta-c Kenyon cells (kc_integration.md), against Turner et al. 2008's 11.5 ms EPSP
decay.
Model: mbon11_burst_check.py's as tested (learning pilot 11's: odor_probe60.py's cache, mb_calibration4.py's mushroom
body, receptor_fills.RECOMMENDED, the Kenyon cells' rest set as the pilots set it, the Kenyon cell-to-MBON11 synapses at
0.054 pC each and depressing, 0.5 of the strength left per spike and 1.5 s to recover), at rest with the receptor neurons
firing spontaneously (not ex vivo), MBON11 silenced as if clamped.
The flash: in a random 5% of the gamma Kenyon cells (78 of 1,557; a different set for each seed), a current that falls
from the flash with CsChrimson's 21 ms (their bias raised by A e^(-t/21 ms), stepped every 2 ms for 150 ms), at 0 and 0.4
s. Conditions: the gamma Kenyon cells' membrane time constant at 20 ms (the model), 50, 100 and 150 ms (the rest of the
brain unchanged), and for each, the flash strength A that gives the flashed cells on average 1, 2, 3 and 5 spikes over the
0.4 s after the first flash (read off a grid of 10 strengths on one seed, interpolated in log A); 4 seeds of 8 flies.
Measured in 2 ms bins from 0.1 s before the first flash to 1.5 s after it: the flashed cells' spikes; the Kenyon cell
input to MBON11 as a current per MBON11 cell (each synapse's 0.054 pC times the strength its depression has left, through
the model's 5 ms synaptic current); and APL's release. Summaries: the flashed cells' spikes after each flash and when they
come; the current's peak, time to peak, width at half the peak, the share left at 400 ms, the time constant of its decay
over 240-400 ms (as Yamada et al.'s tail was fitted) and the PPR (the second flash's peak above the current left at 400
ms, over the first's peak; also without that subtraction). The same Kenyon cell input through a slow synaptic current
(rising with 40 ms, decaying with 280 ms) is reported alongside, as the other reading of Yamada et al.'s EPSC.
Read as (written before the run): a combination matches Yamada et al.'s time course if its current peaks 80-140 ms after
the flash, is 180-320 ms wide at half its peak and keeps 0.25-0.45 of its peak at 400 ms (their ranges widened by about a
quarter, being read off figures); and their PPR if it is 0.38-0.68.

    python experiments/kc_flash_check.py      (writes experiments/kc_flash_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import learning_pilot3 as lp3
import mb_calibration
import mbon11_burst_check as burst
import odor_probe24 as p24
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 990000, 4
SHARE, TAU_OFF, FLASH2 = 0.05, 0.021, 0.4
TAU_M = (0.020, 0.050, 0.100, 0.150)
TARGETS = (1, 2, 3, 5)
GRID = np.geomspace(30.0, 6000.0, 10)                  # flash strengths A (mV of bias at the flash) for the calibration
BIN, PRE, POST = 0.002, 0.1, 1.5
STEP_S, FLASH_S = 0.002, 0.15                           # the flash current's steps, and how long it is stepped
SLOW = (0.040, 0.280)                                   # the slow current's rise and decay, the other reading


def kernel(rise: float, decay: float, n: int) -> np.ndarray:
    """A synaptic current's time course per unit charge, in BIN steps (rise 0: a single exponential)."""
    t = (np.arange(n) + 0.5) * BIN
    k = np.exp(-t / decay) if rise == 0 else np.exp(-t / decay) - np.exp(-t / rise)
    return k / (k.sum() * BIN)


def run(o, rec, seed: int, flashed: np.ndarray, amp: float, h: dict, base: np.ndarray, syn: np.ndarray, record: bool) -> dict:
    """One trial of 8 flies: the 0.5 s settle as learning_pilot3.trial's, then PRE s of rest, a flash at 0 and at FLASH2.
    record: keep the per-bin series (else only the flashed cells' spikes after the first flash)."""
    b = o.brain
    kc, mbon, f = h["kc"], h["mbon"], h["f"]
    apl = b.cells(["APL"])
    q = [int(np.flatnonzero(b.graded == i)[0]) for i in apl]
    flashed_kc = np.searchsorted(kc, flashed)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    drive = p24.spontaneous(rec)
    piece = int(round(BIN / b.dt))
    recover = h["recover_s"] / b.dt
    b.advance(int(round(0.5 / b.dt)), drive=drive, silence=mbon)
    n_bins = int(round((PRE + (POST if record else FLASH2)) / BIN))
    spikes, delivered, release = np.zeros(n_bins), np.zeros(n_bins), np.zeros(n_bins)
    stepped = False
    try:
        for k in range(n_bins):
            t = -PRE + k * BIN                              # the bin's start, from the first flash
            on = [t0 for t0 in (0.0, FLASH2) if t0 - 1e-9 <= t < t0 + FLASH_S]
            if on:                                          # CsChrimson's current, stepped every 2 ms
                bias = base.copy()
                bias[flashed] += amp * np.exp(-(t - on[-1] + STEP_S / 2) / TAU_OFF)
                b.set_bias(bias)
                stepped = True
            elif stepped:
                b.set_bias(base)
                stepped = False
            left = 1.0 - (1.0 - b.left[:, kc]) * np.exp(-(b.t - b.last[:, kc]) / recover)
            c = b.advance(piece, drive=drive, silence=mbon)
            n = c[:, kc].astype(np.float64)
            spikes[k] = n[:, flashed_kc].sum(1).mean()
            if record:
                d = left * (1.0 - f ** n) / (1.0 - f)
                delivered[k] = float((d * syn).sum(1).mean())
                release[k] = float(b.release[:, q].mean())
    finally:
        b.set_bias(base)                                   # exactly the held bias again, so warm starts stay valid
    t = -PRE + (np.arange(n_bins) + 0.5) * BIN
    first = spikes[(t > 0) & (t < FLASH2)].sum() / len(flashed)
    out = {"spikes_per_cell_first": float(first)}
    if record:
        out.update({"spikes": spikes, "delivered": delivered, "release": release})
    return out


def shape(current: np.ndarray, t: np.ndarray) -> dict:
    """The first flash's current: peak, time to peak, width at half the peak, the share left at 400 ms, the decay's time
    constant over 240-400 ms, and the PPR with and without the current left at 400 ms subtracted."""
    rest = current[t < 0].mean()
    i = current - rest
    w1 = (t > 0) & (t < FLASH2)
    j = int(np.argmax(np.where(w1, i, -np.inf)))
    peak = i[j]
    above = np.flatnonzero(w1 & (i >= peak / 2))
    tail = (t > 0.24) & (t < FLASH2)
    pos = tail & (i > 0)
    tau = float(-1.0 / np.polyfit(t[pos], np.log(i[pos]), 1)[0]) if pos.sum() > 10 and np.polyfit(t[pos], np.log(i[pos]), 1)[0] < 0 else None
    left400 = float(i[(t > FLASH2 - 0.01) & (t < FLASH2)].mean())
    w2 = (t > FLASH2) & (t < 2 * FLASH2)
    peak2 = float(i[w2].max())
    return {"peak": float(peak), "t_peak_s": float(t[j]), "half_width_s": float((above[-1] - above[0] + 1) * BIN) if len(above) else 0.0,
            "left_at_400ms": left400 / peak if peak > 0 else None, "tail_tau_s": tau,
            "ppr": (peak2 - left400) / peak if peak > 0 else None, "ppr_unsubtracted": peak2 / peak if peak > 0 else None,
            "left_at_1.5s": float(i[t > POST - 0.02].mean()) / peak if peak > 0 else None}


def matches(s: dict) -> dict:
    return {"time_course": bool(s["peak"] > 0 and 0.08 <= s["t_peak_s"] <= 0.14 and 0.18 <= s["half_width_s"] <= 0.32
                                and s["left_at_400ms"] is not None and 0.25 <= s["left_at_400ms"] <= 0.45),
            "ppr": bool(s["ppr"] is not None and 0.38 <= s["ppr"] <= 0.68)}


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = burst.CHARGE_PC
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    b = o.brain
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "bin_s": BIN, "t0": -PRE, "conditions": {}}
    gamma = np.flatnonzero(mb_calibration.classes(o)["gamma"])
    gamma_types = sorted(set(o.types[gamma]))
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), burst.SEED + 900)   # as the learning test set it
        b.set_type("MBON11", keep_current=1.0)
        h = burst.hold(o, rec, True)
        kc, mbon = h["kc"], h["mbon"]
        pre_n = np.repeat(np.arange(b.n), np.diff(b.ptr))
        onto = np.flatnonzero(o.m["kc"][pre_n] & np.isin(b.idx, mbon))
        syn = np.bincount(np.searchsorted(kc, pre_n[onto]), weights=b._counts[onto], minlength=len(kc))
        to_pa = burst.CHARGE_PC / BIN / len(mbon)          # synapse-spikes per bin -> pA per MBON11 cell
        base = b.bias.copy()
        sets = [np.sort(np.random.default_rng(SEED + j).choice(gamma, int(round(SHARE * len(gamma))), replace=False)) for j in range(SEEDS)]
        out["held"] = {"bias_step_mv": round(h["bias_step_mv"], 2), "flashed_cells": len(sets[0]), "gamma_types": gamma_types,
                       "mbon11_synapses_from_flashed_cells": [int(syn[np.searchsorted(kc, s_)].sum()) for s_ in sets]}
        print("held", json.dumps(out["held"]), flush=True)
        fast, slow = kernel(0.0, 0.005, 200), kernel(*SLOW, 1500)
        for tau_m in TAU_M:
            for g in gamma_types:
                b.set_type(g, tau_m=tau_m)
            b.set_bias(base)                                # the tonic share of the bias follows the new time constant
            grid = [run(o, rec, SEED + 500, sets[0], a, h, base, syn, False)["spikes_per_cell_first"] for a in GRID]
            print(f"tau_m {tau_m}: spikes per flashed cell over A", json.dumps({f"{a:.0f}": round(x, 2) for a, x in zip(GRID, grid)}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            row = {"grid": {"A_mv": GRID.round(1).tolist(), "spikes_per_cell": [round(x, 3) for x in grid]}, "targets": {}}
            g_ = np.maximum.accumulate(np.asarray(grid))
            for n_target in TARGETS:
                if g_[-1] < n_target:
                    row["targets"][str(n_target)] = None
                    continue
                k = int(np.searchsorted(g_, n_target))
                if k == 0:
                    amp = float(GRID[0])
                else:
                    lo, hi = g_[k - 1], g_[k]
                    frac = (n_target - lo) / max(hi - lo, 1e-9)
                    amp = float(np.exp(np.log(GRID[k - 1]) + frac * (np.log(GRID[k]) - np.log(GRID[k - 1]))))
                rs = [run(o, rec, SEED + j, sets[j], amp, h, base, syn, True) for j in range(SEEDS)]
                t = -PRE + (np.arange(len(rs[0]["spikes"])) + 0.5) * BIN
                delivered = np.mean([r["delivered"] for r in rs], 0)
                cur_fast = np.convolve(delivered, fast)[:len(t)] * BIN * to_pa
                cur_slow = np.convolve(delivered, slow)[:len(t)] * BIN * to_pa
                spk = np.mean([r["spikes"] for r in rs], 0) / len(sets[0])
                first = spk[(t > 0) & (t < FLASH2)]
                cum = np.cumsum(first) / max(first.sum(), 1e-12)
                tt = t[(t > 0) & (t < FLASH2)]
                s_fast, s_slow = shape(cur_fast, t), shape(cur_slow, t)
                res = {"A_mv": round(amp, 1),
                       "spikes_per_cell": {"first_flash": round(float(first.sum()), 3),
                                           "second_flash": round(float(spk[(t > FLASH2) & (t < 2 * FLASH2)].sum()), 3),
                                           "half_by_s": round(float(tt[np.searchsorted(cum, 0.5)]), 4) if first.sum() > 0 else None,
                                           "ninety_percent_by_s": round(float(tt[min(np.searchsorted(cum, 0.9), len(tt) - 1)]), 4) if first.sum() > 0 else None},
                       "current_fast": {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in s_fast.items()},
                       "current_slow": {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in s_slow.items()},
                       "matches_fast": matches(s_fast), "matches_slow": matches(s_slow),
                       "apl_release_peak": round(float(np.mean([r["release"] for r in rs], 0).max()), 2),
                       "series": {"spikes_per_cell": np.round(spk, 4).tolist(), "current_fast_pa": np.round(cur_fast, 2).tolist(),
                                  "current_slow_pa": np.round(cur_slow, 2).tolist()}}
                row["targets"][str(n_target)] = res
                print(f"tau_m {tau_m} target {n_target}:", json.dumps({k_: v for k_, v in res.items() if k_ != "series"}),
                      f"({time.perf_counter() - t0:.0f} s)", flush=True)
                out["conditions"][str(tau_m)] = row
                OUT.write_text(json.dumps(out))
            out["conditions"][str(tau_m)] = row
        for g in gamma_types:                               # the model's own time constant back
            b.set_type(g, tau_m=0.020)
        b.set_bias(base)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
