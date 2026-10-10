"""Exploratory, not pre-registered: with the receptor neurons' measured time course added to odor_probe29.py's antennal
lobe, do the projection neurons accommodate during an odor, and do the Kenyon cells fire as few spikes as flies'?

odor_probe29.py: with presynaptic inhibition evoked above the GABAergic LNs' rest and acting on the receptor-to-PN
synapses, the PNs open at 130-156 Hz (flies 100-200) and the Kenyon cells respond at 3-16% with a mean Jaccard of 0.19,
but the PNs rise through an odor (3-octanol 83 Hz in the first 50 ms, 122 by 450 ms) where flies' peak about 150 ms after
the valve opens and fall to about half by 500 ms (Bhandawat et al. 2007), and responding Kenyon cells fire too many
spikes (alpha/beta 6.3, flies 2.2). The model's receptor neurons step on at a constant rate. Flies' rise with a latency
that falls with drive, over about 30 ms, and adapt toward half over about 0.4 s, reaching about 0.75 of their peak by
500 ms (odor_probe10.py's time course; research_notes/Rung 9 learning data/orn_dynamics.md); odor_receptor_course.py
found that alone barely makes PNs accommodate, without presynaptic inhibition.
Model: odor_probe29.py's with odor_probe10.py's receptor time course (tau_r 30 ms) in every odor, including the
calibration's lateral odors, on top of the spontaneous firing; the transform's protocol keeps its step (Olsen et al.
quantified the 500 ms mean of a private odor's response). k_A and k_B fitted again to Olsen & Wilson 2008's EPSCs.
Measured as odor_probe29.py measures. Seeds 240000 (otherwise as odor_probe29.py's, with its offsets).

Ran: the receptor time course brings the Kenyon cells into flies' range and the PNs part of the way to accommodating.
The fit to Olsen & Wilson's EPSCs is the closest yet (k_A = 0.00046, k_B = 0.0023 per spike/s above rest; control 0.30,
0.33, 0.33 and 0.33 of baseline against flies' 0.27, 0.32, 0.33 and 0.37; GABA-B blocked 0.53, 0.72, 0.75 and 0.76
against 0.52, 0.68, 0.77 and 0.81). The driven PNs now peak and decline with the receptor neurons' adaptation
(3-octanol: 71 Hz at 50-100 ms, a peak of 106 at 350-400 ms, 84 at 1 s, 0.79 of the peak, with the receptor neurons at
0.81 of theirs by 600 ms), where flies' peak about 75 ms after their receptors start and fall to about half by 500 ms:
62-84 Hz in the first 100 ms (lower than before, the receptors' latency and rise included) and 124-172 over 1 s; 21-36%
respond by Turner's criterion (flies 59 +- 14%). 2.4-10.5% of Kenyon cells respond (flies 6 +- 5%), with mean Jaccard 0.16
(flies' dissimilar odors about 0.22), PN patterns correlating 0.23, 5 cells answering all six odors, but 56% of
4-methylcyclohexanol's responders also answering 3-octanol (flies' dissimilar odors share about 22%). Responding cells
fire 4.6-5.7 spikes (alpha/beta; flies 2.2) and alpha'/beta' cells 3.4-4.5 (flies 4.9), but alpha'/beta' cells respond
at only 0.7-3.9% (flies about 9-14%) and gamma cells at 2.5-9.4% (about 2). MBON11 gains 1.7-9.5 spikes and
MBON-alpha2sc 1.9-21 (flies 110-118 and about 71-85; odor_probe31.py sets their synapses from MBON11's measurements). The
transform keeps odor_probe29.py's step and is unchanged (Rmax 185, 305, 345 and 298; sigma 36, 29, 35 and 28). PNs rest
at 1.55 Hz, the brain at 1.10 Hz.

    python experiments/odor_probe30.py         (writes experiments/odor_probe30.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 240000


def advance_odor(o: p7.Olfaction, rec: p10.Receptors, plan: dict, t: float, until: float) -> float:
    """Advance from t to `until` s after the odor's onset in odor_probe10.py's 10 ms pieces, the drive following the
    receptor time course. Returns the new time."""
    b = o.brain
    while t < until - 1e-9:
        step = min(p10.PIECE, until - t)
        b.advance(int(round(step / b.dt)), drive=rec.at(plan, t))
        t += step
    return t


def lateral_traces(o: p7.Olfaction, rec: p10.Receptors, seed: int) -> np.ndarray:
    """odor_probe28.lateral_traces with the receptor time course."""
    b = o.brain
    out = []
    for j, odor in enumerate(p21.LATERAL):
        b.reset(seed + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        b.advance(int(round(2.0 / b.dt)), drive=p24.spontaneous(rec))
        plan = rec.plan(odor, 2.0, p10.PEAK_HZ)
        t, row = 0.0, []
        for ts in p21.OLSEN_T:
            t = advance_odor(o, rec, plan, t, round(ts - p21.VALVE_DELAY, 2))
            a = b.presynaptic_state.mean(0)
            row.append((a[1], a[3]))
        out.append(row)
    return np.array(out)


def calibrate(o, rec, mk, base_w, base_sw) -> dict:
    a_rest = p24.resting_inhibitors(o, rec, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):
        p28.apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = p27.fit(lateral_traces(o, rec, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    p28.apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    return {"k": [0.0, k_a, 0.0, k_b], "offset_hz": round(a_rest, 1), "tau_s": list(p28.TAUS), "source": list(p28.SOURCE),
            "inhibitors_rest_hz": round(a_rest, 1), "resting_divisor": 1.0, "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def course(o, rec, odor: str, seed: int, pns: np.ndarray, inhibitors: np.ndarray, k: np.ndarray, offset: float) -> dict:
    """odor_probe27.course with the receptor time course (the odor's first bin starts at its onset at the valve's
    side of the receptors, before their latency)."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    rest = b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    pn, inh, gain, orn = [], [], [], []
    t = 0.0
    piece = int(round(p10.PIECE / b.dt))
    for _ in range(int(round(1.0 / p21.BIN))):
        c = 0
        for _ in range(int(round(p21.BIN / p10.PIECE))):
            c = c + b.advance(piece, drive=rec.at(plan, t))
            t += p10.PIECE
        pn.append(float(c[:, pns].mean() / p21.BIN))
        inh.append(float(c[:, inhibitors].sum(1).mean() / p21.BIN))
        orn.append(float(c[:, o.m["orn"]].sum(1).mean() / p21.BIN))
        a = np.maximum(b.presynaptic_state - offset, 0.0)
        gain.append(float((1.0 / (1.0 + (a * k).sum(1))).mean()))
    return {"bin_s": p21.BIN, "rest_pn_hz": round(float(rest[:, pns].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain],
            "orn_summed_hz": [round(x, 1) for x in orn]}


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = SEED
    p21.masks = p29.pn_only_masks
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    out["spontaneous_hz"] = rec.spont
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 930)
    p28.apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)
    p10.POLISH, schedule = p27.FIRST_POLISH, p10.POLISH
    try:
        out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0, SEED + 600)
    finally:
        p10.POLISH = schedule
    out["pn_rest"] = p27.pn_polish(o, rec, SEED + 700)
    rec.kinetics = "fast"                                # odors from here on follow the receptor time course
    entry = {"presynaptic": calibrate(o, rec, mk, base_w, base_sw)}
    out["second_polish"] = p24.polish(o, rec, SEED + 640, p27.SECOND_POLISH)
    out["pn_rest_after"] = p27.pn_polish(o, rec, SEED + 800, rounds=6)
    k, offset = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["offset_hz"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = course(o, rec, odor, base + 700 + j, pns, mk["inhibitors"], k, offset)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = p24.transform(o, rec, base)
    entry.update(p24.odor_measures(o, rec, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
