"""Exploratory check, not pre-registered: does the model's APL answer each odor in proportion to its Kenyon cell drive,
and equalize 4-methylcyclohexanol with 3-octanol in the Kenyon cells, as flies' APL does?

learning_pilot6.py and learning_pilot7.py: 4-methylcyclohexanol reaches a quarter as many Kenyon cells as 3-octanol (flies
about as many), which leaves the reciprocal pairing short. research_notes/Rung 9 learning data/mch_oct_equalization.md: at
the projection neurons the model already equalizes about as flies' do on the glomeruli flies' imaging covers (0.82-0.86
against 0.85-0.98), and in flies APL equalizes the Kenyon cells: Prisco et al. 2021 found APL's calcium response to
4-methylcyclohexanol about half its response to 3-octanol (43 against 88 %max, 0.49), and the Kenyon cells' claw responses
at 0.89 of 3-octanol's peak (63 against 71) and 0.95 of its count (17.5 against 18.5 claws) with APL working, but 0.65
(115 against 177) and 0.76 (21 against 27.5) with APL silenced. odor_probe54.py: the model's APL releases at 23.3 Hz at
its peak for 3-octanol and 21.8 for 4-methylcyclohexanol (0.94).
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body, the Kenyon cells' rest set as the learning
pilots set it, settled starts.
Measured, for each odor with APL working and with it silenced (Hige et al.'s protocol: a 1 s odor after 1.5 s; 2 seeds of
8 flies, the same seeds for both): APL's release (peak of 50 ms running means, mean over the odor); the Kenyon cells
answering (more than half an evoked spike over 1.4 s) and their evoked spikes; the Kenyon cells' mean depolarization over
the odor (all cells, and those answering), the model's nearest measure to claw calcium; each odor's ratios
(4-methylcyclohexanol over 3-octanol). Seeds 670000 + 10 x odor + seed.

    python experiments/odor_apl_check.py      (writes experiments/odor_apl_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe54 as p54
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 670000, 2
ODORS = ("3-octanol", "4-methylcyclohexanol")
FLIES = {"apl": 0.49, "claw_peak_apl_on": 0.89, "claw_peak_apl_off": 0.65, "claws_apl_on": 0.95, "claws_apl_off": 0.76}


def trial(o, rec, odor: str, seed: int, apl: np.ndarray, silence) -> dict:
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    q = [int(np.flatnonzero(b.graded == i)[0]) for i in apl]
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -1.5
    for _ in range(50):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        t += p10.PIECE
    rest, rest_u = 0, 0.0
    for _ in range(100):
        rest = rest + b.advance(piece, drive=rec.at(plan, t), silence=silence)[:, kc]
        rest_u += b.u[:, kc] / 100
        t += p10.PIECE
    window, release, u_odor = 0, [], 0.0
    for k in range(140):
        window = window + b.advance(piece, drive=rec.at(plan, t), silence=silence)[:, kc]
        release.append(float(b.release[:, q].mean()))
        if k < 100:
            u_odor += b.u[:, kc] / 100
        t += p10.PIECE
    return {"evoked": (window - 1.4 * rest).astype(float), "depolarization": u_odor - rest_u, "release": np.array(release)}


def summarize(rs: list) -> dict:
    evoked = np.concatenate([r["evoked"] for r in rs])               # (flies, KCs)
    depol = np.concatenate([r["depolarization"] for r in rs])
    release = np.mean([r["release"] for r in rs], 0)
    answering = evoked.mean(0) > 0.5
    smooth = np.convolve(release, np.ones(5) / 5, mode="valid")
    return {"apl_release_peak_hz": round(float(smooth.max()), 2), "apl_release_mean_hz": round(float(release[:100].mean()), 2),
            "kcs_answering": int(answering.sum()), "kc_evoked_spikes": round(float(evoked.mean(0).clip(0).sum()), 1),
            "kc_depolarization_mv": round(float(depol.mean()), 3),
            "answering_kc_depolarization_mv": round(float(depol[:, answering].mean()), 3) if answering.any() else None}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import mb_calibration                              # after the cache, so that its edits don't invalidate it
    out = {"question": __doc__, "flies": FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}}
    apl = o.brain.cells(["APL"])
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for name, silence in (("APL working", ()), ("APL silenced", apl)):
            rows = {}
            for j, odor in enumerate(ODORS):
                rows[odor] = summarize([trial(o, rec, odor, SEED + 10 * j + s, apl, silence) for s in range(SEEDS)])
            a, b = rows["4-methylcyclohexanol"], rows["3-octanol"]
            rows["mch_over_oct"] = {k: round(a[k] / b[k], 3) if b.get(k) else None for k in b if isinstance(b[k], (int, float))}
            out["conditions"][name] = rows
            print(name, json.dumps(rows), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    on, off = out["conditions"]["APL working"], out["conditions"]["APL silenced"]
    out["block_ratio"] = {od: round(off[od]["kc_evoked_spikes"] / max(on[od]["kc_evoked_spikes"], 1e-9), 2) for od in ODORS}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("block ratio", json.dumps(out["block_ratio"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
