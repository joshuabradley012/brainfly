"""Exploratory check, not pre-registered: odor_apl_kinetics_check.py again, with the APL conductance's reversal measured
from each Kenyon cell's own resting potential (mb_calibration4.py), as flies' would be. Can APL with flies' time course
answer each odor in proportion and hold the Kenyon cells back 2-3-fold, and with which reading of its strength?

odor_apl_kinetics_check.py's Inada et al. Fig. 5B test found that APL at its ceiling held a quiet Kenyon cell 3.8 mV down
at a reversal of -20, where the design said 11: HybridBrain measures slow_reversal from the model's zero, and the Kenyon
cells rest at 0 (alpha'/beta'), -5.5 (alpha/beta) and -16.5 mV (gamma), so the reversal lay 20, 14.5 and 3.5 mV below them
and APL barely inhibited the gamma cells. mb_calibration4.py puts each type's reversal `reversal` mV below its rest and
scales its APL synapses so that at rest it takes the designed current. Everything else as odor_apl_kinetics_check.py:
the conductance decaying with tau 0.3 s (research_notes/Rung 9 learning data/apl_kinetics.md), and two readings of the
strength, as APL's conductance at its ceiling (a multiple of the Kenyon cell's leak, the same whatever the reversal): 1,
holding a quiet Kenyon cell 11 mV below rest at the reversal (synapses at physiological chloride; 1.22 at -20, 2.75 at
-15); 2, 11 mV at -50 mV, the pipette's chloride (0.28; 4.4 mV at -20). (odor_apl_kinetics_check.py held the current at
rest fixed instead when it changed the reversal, so its "strength 2" and its pipette test had other conductances.)
Conditions:
    strength 1, reversal -20 mV (conductance 1.22): drive 0.5, 1, 1.5 and 2.5 times MaleCNS's
    strength 1, reversal -15 mV (2.75): drive 0.5, 1 and 1.5
    strength 2, reversal -20 mV (0.28): drive 1.5, 2.5, 4, 6 and 10
Measured as odor_apl_kinetics_check.py measures, Inada et al.'s Fig. 5B test also by class (alpha/beta, alpha'/beta',
gamma), for the chosen condition, with its reversal and with the pipette's (-50 mV from rest), the conductance the same.
Chosen, as stated before running: among the conditions whose silencing raises both odors' Kenyon cell spikes 2-3-fold,
the one whose APL peak ratio is nearest 0.49 (by |log|); if none does, the one nearest both (the summed squared log ratios
to 2.5 and 0.49), reported as missing. mb_calibration4.py then takes its constants.

    python experiments/odor_apl_conductance2_check.py      (writes experiments/odor_apl_conductance2_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_apl_conductance_check as cc
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe7 as p7
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 870000, 2
TAU = 0.3
PIPETTE_MV = -50.0
ODORS = cc.ODORS
FLIES = {**cc.FLIES, "inada_5b": {"rise_10_50_90_s": [0.14, 0.27, 0.56], "half_gone_after_s": 0.32, "left_1s": 0.22,
                                  "left_2s": 0.13, "plateau_mv_pipette": [-12.0, -10.0]}}


def conductance_for(ceiling: float, reversal: float) -> float:
    """APL's conductance at its ceiling, as a multiple of a Kenyon cell's leak, that holds a quiet cell |ceiling| mV below
    rest with this reversal: |reversal| g / (1 + g) = |ceiling|."""
    return abs(ceiling) / (abs(reversal) - abs(ceiling))


def effect_of(g: float, reversal: float) -> float:
    """mb_calibration4's effect for conductance g at this reversal: its current at rest, g |reversal| mV, over
    mb_calibration.py's 11 mV ceiling."""
    import mb_calibration
    return g * abs(reversal) / abs(mb_calibration.KC_SATURATION_MV)


def apl_drive(o, rec, seed: int, apl: np.ndarray, extra_mv: float = 30.0) -> dict:
    """Inada et al. Fig. 5B on the model: at rest, APL's bias raised extra_mv for 1 s after 0.5 s; the quiet Kenyon cells'
    mean free potential every 10 ms, driven less undriven (same seed), and its landmarks."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    plan = rec.plan(None, 0.0, p10.PEAK_HZ)                  # no odor: the receptor neurons fire spontaneously
    piece = int(round(p10.PIECE / b.dt))
    own = o.own_bias().copy()

    def run(driven: bool):
        b.reset(seed)
        b.set_release(o.s.ol.neurons, o.s.silent)
        t, course, spikes = -4.0, [], 0
        for k in range(350):
            if driven and k == 50:
                raised = own.copy()
                raised[apl] += extra_mv
                b.set_bias(raised)
            if driven and k == 150:
                b.set_bias(own)
            spikes = spikes + b.advance(piece, drive=rec.at(plan, t))[:, kc]
            course.append(cc.free_potential(b, b.x, b.s)[:, kc])
            t += p10.PIECE
        return np.array(course), np.asarray(spikes)

    on, s_on = run(True)
    off, s_off = run(False)
    quiet = (s_on == 0) & (s_off == 0)                         # (flies, Kenyon cells)
    d = np.array([(a - z)[quiet].mean() for a, z in zip(on, off)])
    types = o.types[kc]
    by_class = {}
    for cl, prefix in p7.CLASSES.items():
        m = quiet & np.char.startswith(types, prefix)[None, :]
        by_class[cl] = round(float(np.mean([(a - z)[m].mean() for a, z in zip(on[80:100], off[80:100])])), 2)
    ts = (np.arange(350) + 1) * p10.PIECE - 0.5               # from the drive's start
    plateau = float(d[(ts > 0.8) & (ts <= 1.0)].mean())
    def first(mask):
        idx = np.flatnonzero(mask)
        return round(float(ts[idx[0]]), 3) if len(idx) else None
    during, after = (ts > 0) & (ts <= 1.0), ts > 1.0
    rise = [first(during & (d <= f * plateau)) for f in (0.1, 0.5, 0.9)]
    half_gone = first(after & (d >= 0.5 * plateau))
    at = lambda s_: float(d[np.argmin(np.abs(ts - (1.0 + s_)))])
    return {"plateau_mv": round(plateau, 2), "rise_10_50_90_s": rise,
            "half_gone_after_s": round(half_gone - 1.0, 3) if half_gone is not None else None,
            "left_1s": round(at(1.0) / plateau, 3), "left_2s": round(at(1.95) / plateau, 3),
            "plateau_mv_by_class": by_class, "quiet_share": round(float(quiet.mean()), 4), "course_mv": np.round(d, 2).tolist()}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import mb_calibration3
    import mb_calibration4
    b = o.brain
    out = {"question": __doc__, "flies": FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}, "inada_5b": {}}
    apl = b.cells(["APL"])
    calibrated = b.weights.copy()
    held = []                                          # every weight array installed, so that no new one reuses an old id
    g1, g15, g2 = conductance_for(cc.CEILING_MV, -20.0), conductance_for(cc.CEILING_MV, -15.0), conductance_for(cc.CEILING_MV, PIPETTE_MV)
    conditions = ([(f"strength 1, reversal -20, drive {d:g}", d, g1, -20.0, TAU, "1") for d in (0.5, 1.0, 1.5, 2.5)]
                  + [(f"strength 1, reversal -15, drive {d:g}", d, g15, -15.0, TAU, "1") for d in (0.5, 1.0, 1.5)]
                  + [(f"strength 2, reversal -20, drive {d:g}", d, g2, -20.0, TAU, "2") for d in (1.5, 2.5, 4.0, 6.0, 10.0)])
    own_bias = o.own_bias().copy()
    with warm.tracking(o, rec):
        for name, drive, g, reversal, tau, strength in conditions:
            effect = effect_of(g, reversal)
            held += [b.weights, b.slow_weights]
            reversals = mb_calibration4.install(o, drive, effect, reversal, calibrated, tau)
            b.set_bias(own_bias)
            kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            off = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            row = cc.condition(on, off)
            course = row["3-octanol"]["inhibition_course_mv_50ms"]
            row.update({"kc_rest": kc_rest, "reversal_mv_by_type": reversals, "drive": drive, "effect": round(effect, 3), "reversal_mv": reversal, "tau_s": tau,
                        "strength": strength, "conductance_x_leak": round(g, 3),
                        "ceiling_mv": round(-abs(reversal) * g / (1 + g), 2),
                        "ceiling_mv_pipette": round(-abs(PIPETTE_MV) * g / (1 + g), 2),
                        "largest_inhibition_at_s": round((int(np.argmin(course)) + 2.5) * p10.PIECE, 3)})
            out["conditions"][name] = row
            a, c = row["3-octanol"], row["4-methylcyclohexanol"]
            print(f"{name}: APL peak {a['apl_release_peak_hz']}/{c['apl_release_peak_hz']} (ratio {row['apl_peak_mch_over_oct']})"
                  f" | block {a['block_ratio']}/{c['block_ratio']} | KCs {a['kcs_answering']}/{c['kcs_answering']}"
                  f" | largest {a['largest_inhibition_mv_50ms']} mV at {row['largest_inhibition_at_s']} s, silent"
                  f" {a['inhibition_mv_silent_cells']}, rest {a['inhibition_mv_at_rest']} | equalization"
                  f" {row['answering_mch_over_oct']['equalization']} | both {row['share_answering_both']}", flush=True)
            OUT.write_text(json.dumps(out, indent=1, default=float))
        candidates = {k: v for k, v in out["conditions"].items() if v["tau_s"] == TAU}
        chosen = min(candidates, key=lambda k: cc.score(candidates[k]))
        out["chosen"] = {"condition": chosen, "meets_block_ratio": not cc.score(candidates[chosen])[0]}
        print("chosen:", json.dumps(out["chosen"]), flush=True)
        for name in (chosen,):
            _, drive, g, reversal, tau, _ = next(c for c in conditions if c[0] == name)
            for label, rev in (("reversal", reversal), ("pipette", PIPETTE_MV)):
                held += [b.weights, b.slow_weights]
                mb_calibration4.install(o, drive, effect_of(g, rev), rev, calibrated, tau)     # the same conductance
                b.set_bias(own_bias)
                p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
                res = apl_drive(o, rec, SEED + 5000, apl)
                out["inada_5b"][f"{name} | {label} {rev:g} mV"] = res
                print(f"Inada 5B, {name} | {label} {rev:g} mV:", json.dumps({k: v for k, v in res.items() if k != "course_mv"}), flush=True)
                OUT.write_text(json.dumps(out, indent=1, default=float))
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
