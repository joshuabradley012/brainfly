"""Exploratory check, not pre-registered: measured as Olsen et al. measured flies, how steep is the model's transform?

The model's transform (odor_transform_check.py: Rmax 78-186, sigma 20-31; flies 144-170 and 12-16, DM1 45) has been
measured with windows starting with the receptor input. Olsen et al. 2010 averaged both the receptor neurons' and the
PNs' rates over the 500 ms from the valve's opening, less the 500 ms before; responses start about 100-125 ms after the
valve opens and outlast it, weak receptor responses rising slowly and staying tonic, strong ones peaking at about
190-260 ms and adapting toward about 0.65 (their Fig. S2). In a one-PN model with brainfly's synapse, measuring that way
lowers sigma about 1.3-fold and Rmax about 0.88-fold (research_notes/Rung 9 learning data/weak_input_gain.md, which
predicts sigma about 18 for DL5, 24 for VM7d and 22 for DM4 in the model).
Model: odor_probe49.py's (its cache), with its settled starts.
Measured: for Olsen et al.'s four glomeruli and receptor rates x of 5-160 spikes/s (odor_probe16.RATES), the PNs' mean
rate over the 500 ms from the valve's opening less the 500 ms before, and their PSTH (25 ms bins, -0.5 to 1 s), over the
glomerulus's cholinergic uniglomerular PNs, the ones flies' recordings are of (orn_pn_glomeruli_check.py: DM4's two
GABAergic vPNs get almost no receptor input), and over all its uniglomerular PNs as before; with the
glomerulus's receptor neurons following Olsen et al.'s time course (weak_input_gain.md's: 100 ms latency, then a
first-order rise over 40 ms for x under 20 spikes/s, or over 25 ms with adaptation toward 0.65 of the peak over 0.25 s
for x of 20 and more; from 520 ms a decay over 60 ms), scaled so that its mean over the 500 ms is x; and as a step for
comparison (odor_transform_check.py's protocol). Olsen et al.'s function fitted to each. Two seeds per point: 570000 +
1000 x protocol + 100 x glomerulus + 10 x rate index + seed. Flies: sigma 11.7, 12.7 and 16.3 and Rmax 166, 163 and 170
(DL5, VM7, DM4; DM1 45 and 152); VM7 PNs peak at 176 spikes/s at 175 ms for x = 11.6, 0.42 of the peak at 500 ms; peak
over mean 2.3-2.5 for weak and intermediate input, 1.9 for strong (Olsen et al. Fig. 8).

    python experiments/odor_olsen_protocol_check.py      (writes experiments/odor_olsen_protocol_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

import brain_cache
import odor_probe10 as p10
import odor_probe16 as p16
import odor_probe24 as p24
import odor_probe44 as p44
import odor_probe49 as p49
import warm
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 570000, 2
LATENCY_S, OFFSET_S, OFF_TAU_S, WINDOW_S = 0.1, 0.52, 0.06, 0.5
PRE_S, POST_S, BIN_S = 0.5, 1.0, 0.025


def olsen_shape(t: np.ndarray, x: float) -> np.ndarray:
    """The receptor neurons' extra rate (unscaled) t s after the valve opens, for a response whose window mean is x."""
    t = np.asarray(t, float)
    tau_r = 0.04 if x < 20 else 0.025
    c = np.clip(t - LATENCY_S, 0.0, None)
    adapt = 1.0 if x < 20 else 0.65 + 0.35 * np.exp(-c / 0.25)
    on = (1.0 - np.exp(-c / tau_r)) * adapt
    c_off = OFFSET_S - LATENCY_S
    at_off = (1.0 - np.exp(-c_off / tau_r)) * (1.0 if x < 20 else 0.65 + 0.35 * np.exp(-c_off / 0.25))
    return np.where(t < LATENCY_S, 0.0, np.where(t < OFFSET_S, on, at_off * np.exp(-(t - OFFSET_S) / OFF_TAU_S)))


def run(o, rec, g: str, x: float, sets: dict, seed: int, protocol: str) -> dict:
    """Each set of PNs' mean rate in BIN_S bins from -PRE_S to POST_S around the valve's opening."""
    b = o.brain
    base = p24.spontaneous(rec)
    grid = np.arange(0, POST_S, p10.PIECE) + p10.PIECE / 2
    if protocol == "olsen":
        window = grid < WINDOW_S
        extra = olsen_shape(grid, x)
        extra *= x / float(extra[window].mean())
    else:                                                   # the step, from the valve's opening, for 0.5 s
        extra = np.where(grid < WINDOW_S, x, 0.0)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=base)
    piece = int(round(p10.PIECE / b.dt))
    counts = {k: [] for k in sets}
    for k in range(int(round(PRE_S / p10.PIECE))):
        c = b.advance(piece, drive=base)
        for name, pns in sets.items():
            counts[name].append(float(c[:, pns].mean()))
    for e in extra:
        drive = [(rec.cells[h], rec.spont[h] + (e if h == g else 0.0)) for h in rec.glomeruli if len(rec.cells[h])]
        c = b.advance(piece, drive=drive)
        for name, pns in sets.items():
            counts[name].append(float(c[:, pns].mean()))
    per = int(round(BIN_S / p10.PIECE))
    return {name: np.array(v).reshape(-1, per).mean(1) / p10.PIECE for name, v in counts.items()}


def summarize(psth: np.ndarray) -> dict:
    """Olsen et al.'s measure (the 500 ms from the valve's opening less the 500 ms before) and the time course."""
    n_pre, n_win = int(round(PRE_S / BIN_S)), int(round(WINDOW_S / BIN_S))
    rest = float(psth[:n_pre].mean())
    win = psth[n_pre:n_pre + n_win] - rest
    # Olsen et al.'s PSTHs: 50 ms bins overlapping by 25 ms, i.e. two 25 ms bins averaged
    smooth = (psth[n_pre:-1] + psth[n_pre + 1:]) / 2 - rest
    k = int(np.argmax(smooth))
    at_500 = float(smooth[int(round(WINDOW_S / BIN_S)) - 1])
    return {"window_mean": round(float(win.mean()), 2), "peak": round(float(smooth[k]), 1),
            "peak_ms": round((k + 1) * BIN_S * 1000), "at_500ms_over_peak": round(at_500 / float(smooth[k]), 3) if smooth[k] > 0 else None,
            "peak_over_window_mean": round(float(smooth[k]) / float(win.mean()), 2) if win.mean() > 0 else None,
            "rest": round(rest, 2)}


def fit(xs, ys) -> dict | None:
    try:
        (rmax, sigma), _ = curve_fit(p16.olsen, np.array(xs, float), np.array(ys, float), p0=(160.0, 15.0), maxfev=20000)
        return {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
    except RuntimeError:
        return None


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe49", p49.build, p44.prepare)
    types, m = o.types, o.m
    cholinergic = np.asarray(consensus_transmitters()) == "acetylcholine"
    out = {"question": __doc__, "rates": list(p16.RATES), "settling": getattr(o, "settling", None), "protocols": {}}
    with warm.tracking(o, rec):
        for p, protocol in enumerate(("olsen", "step")):
            rows = {}
            for gi, g in enumerate(p16.GLOMERULI):
                pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
                sets = {"cholinergic": pns[cholinergic[pns]], "all": pns}
                pts = {name: {} for name in sets}
                for k, x in enumerate(p16.RATES):
                    rs = [run(o, rec, g, x, sets, SEED + 1000 * p + 100 * gi + 10 * k + s, protocol) for s in range(SEEDS)]
                    for name in sets:
                        psth = np.mean([r[name] for r in rs], 0)
                        pts[name][f"{x:g}"] = dict(summarize(psth), psth=psth.round(1).tolist())
                rows[g] = {"pns": {name: int(len(v)) for name, v in sets.items()},
                           "olsen": {"rmax": p16.OLSEN[g][0], "sigma": p16.OLSEN[g][1]}}
                for name in sets:
                    rows[g][name] = {"points": pts[name],
                                     "fit": fit(p16.RATES, [pts[name][f"{x:g}"]["window_mean"] for x in p16.RATES])}
            out["protocols"][protocol] = rows
            for name in ("cholinergic", "all"):
                print(protocol, name, json.dumps({g: rows[g][name]["fit"] for g in rows}),
                      json.dumps({g: [rows[g][name]["points"][f"{x:g}"]["window_mean"] for x in p16.RATES] for g in rows}), flush=True)
            for g in rows:
                print(" ", g, json.dumps({x: {k: v for k, v in rows[g]["cholinergic"]["points"][x].items() if k != "psth"}
                                          for x in ("5", "10", "20", "40")}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
