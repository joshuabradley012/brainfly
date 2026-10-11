"""Exploratory check, not pre-registered: with APL's conductance onto the Kenyon cells given flies' time course, can APL
still answer each odor in proportion and hold the Kenyon cells back 2-3-fold, and for which of the two readings of its
strength that flies' recordings allow?

odor_apl_conductance_check.py chose APL's synapses onto the Kenyon cells as a conductance reversing 20 mV below rest,
strong enough that APL's ceiling holds a quiet Kenyon cell 11 mV down, with a 5 ms decay. research_notes/Rung 9 learning
data/apl_kinetics.md: driving APL directly, flies' inhibition is half up 0.27 s after the light begins (10% at 0.14 s,
90% at 0.56 s), plateaus near -10 mV, is half gone 0.32 s after the light ends and leaves about a fifth after 1 s (Inada
et al. 2017 Fig. 5B); driven by Kenyon cells for 200 ms it peaks at about 0.31 s and decays with tau about 0.39 s (Vrontou
et al. 2021). The model's decays 50-80 times too fast. And those recordings set chloride's reversal near -121 mV with the
pipette, so the 10-12 mV ceiling reads two ways: if the synapses kept physiological chloride, it is the ceiling at a
reversal about 20 mV below rest (as now); if the pipette's chloride reached them, it is the ceiling at about 50 mV below
rest (-121 mV against a cell held near -70 once the junction potential is corrected), and APL's conductance is about half
as large.
Model: odor_probe60.py's (its cache) with mb_calibration.py's mushroom body, then mb_calibration3.install with the Kenyon
cells' slow current decaying with tau 0.3 s (apl_kinetics.md's 0.25-0.4 s), its synapses scaled by 5 ms / tau so that a
steady release gives the same conductance. Conditions:
    strength 1, reversal -20 mV: ceiling 11 mV at -20 (effect 2.22); drive 1, 1.5, 2.5 and 4 times MaleCNS's
    strength 1, reversal -15 mV: ceiling 11 mV at -15 (effect 3.75); drive 0.5, 1 and 1.5
    strength 2, reversal -20 mV: ceiling 11 mV at -50, as the recordings would have measured it with pipette chloride
               (effect 1.28; at -20 its ceiling is 8.3 mV); drive 1.5, 2.5, 4 and 6
and, for comparison, mb_calibration3.py's APL as it is (tau 5 ms, reversal -20, effect 2.22, drive 1.5).
Measured as odor_apl_conductance_check.py measures (the Kenyon cells' rest set anew in each condition; DoOR's input, 2
seeds of 8 flies, APL working and silenced): APL's release and its 4-methylcyclohexanol/3-octanol ratio, the rise
silencing gives each odor's Kenyon cell spikes, the answering cells and those shared, and the Kenyon cells' inhibition
(its course in 50 ms means and when it is largest). And for the chosen condition and the comparison, Inada et al.'s Fig.
5B on the model: the brain at rest, APL driven to its ceiling for 1 s (its bias raised 30 mV), the quiet Kenyon cells'
mean free potential against the same run undriven (one seed of 8 flies): when the inhibition reaches 10, 50 and 90% of
its plateau, the plateau, when half of it is gone after the drive, and what is left 1 and 2 s after; once with the
condition's reversal and once with -50 mV, the pipette's.
Chosen, as stated before running: among the tau 0.3 s conditions whose silencing raises both odors' Kenyon cell spikes
2-3-fold, the one whose APL peak ratio is nearest 0.49 (by |log|); if none does, the one nearest both (the summed squared
log ratios to 2.5 and 0.49), reported as missing. Then reported against flies: Inada et al.'s time course (10/50/90% at
0.14/0.27/0.56 s, half gone 0.32 s after, about 0.2 of it left at 1 s) and plateau with the pipette's reversal (10-12 mV).

Ran (22 minutes), but on a mis-specified APL, which its own Fig. 5B test exposed: driven to its ceiling, APL held the
quiet Kenyon cells 3.8 mV down at a reversal of -20 (3.8 too with the 5 ms decay), where the design said 11. HybridBrain
measures slow_reversal from the model's zero, and the Kenyon cells rest at 0 (alpha'/beta'), -5.5 (alpha/beta) and -16.5
mV (gamma), their shared threshold of 16 less their gaps, so a reversal of -20 lay 20, 14.5 and 3.5 mV below them and APL
could barely inhibit the gamma cells. mb_calibration3.py and every run on it share the error (mb_calibration4.py corrects
it; odor_apl_conductance2_check.py repeats this check). Also, where a test changed the reversal it held the conductance's
current at rest fixed, not the conductance: "strength 2" was a conductance of 0.70 times the Kenyon cell's leak, not 0.28,
and the pipette test's conductance 0.4 times its condition's. With those caveats, the time course is near flies': driven
directly, the inhibition reaches 10, 50 and 90% of its plateau at 0.02-0.03, 0.11-0.16 and 0.37-0.51 s (flies 0.14, 0.27,
0.56) and half of it is gone 0.32-0.37 s after the drive (flies 0.32), where the 5 ms decay gave 0.01-0.02 s and 0.06 s;
but only 0.05-0.06 of it is left after 1 s (flies about 0.2: the slower GABA-B part, which the model lacks). In odors it
is largest at 0.17-0.23 s, not 0.075. By the rule, strength 1 at -20 with drive 1 was chosen: APL's ratio 0.48 (flies
0.49), silencing 2.39 and 2.31-fold. But 695 Kenyon cells answered 3-octanol and 248 4-methylcyclohexanol (the 5 ms
comparison 356 and 219), APL no longer equalized the odors (0.82-fold; flies 1.25), and 0.63 of 4-methylcyclohexanol's
answering cells answered 3-octanol (flies 0.33), with the gamma cells nearly free of APL. Stronger drives took APL to its
ceiling for 3-octanol (ratios 0.62-0.93); -15 mV held the Kenyon cells back 3.4-4.6-fold.

    python experiments/odor_apl_kinetics_check.py      (writes experiments/odor_apl_kinetics_check.json)
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
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 860000, 2
TAU = 0.3
PIPETTE_MV = -50.0
ODORS = cc.ODORS
FLIES = {**cc.FLIES, "inada_5b": {"rise_10_50_90_s": [0.14, 0.27, 0.56], "half_gone_after_s": 0.32, "left_1s": 0.22,
                                  "left_2s": 0.13, "plateau_mv_pipette": [-12.0, -10.0]}}


def strength2_effect(reversal: float = -20.0, pipette: float = PIPETTE_MV, ceiling: float = cc.CEILING_MV) -> float:
    """The effect whose conductance holds a quiet Kenyon cell `ceiling` mV down at APL's ceiling with the pipette's
    reversal: the current's shift G with G / (1 + |G| / |pipette|) = |ceiling|, G = 11 x effect (the reversal used in the
    odors doesn't enter: the conductance is the same)."""
    import mb_calibration
    g = abs(ceiling) / (1.0 - abs(ceiling) / abs(pipette))
    return g / abs(mb_calibration.KC_SATURATION_MV)


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
            "quiet_share": round(float(quiet.mean()), 4), "course_mv": np.round(d, 2).tolist()}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import mb_calibration3
    b = o.brain
    out = {"question": __doc__, "flies": FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}, "inada_5b": {}}
    apl = b.cells(["APL"])
    calibrated = b.weights.copy()
    held = []                                          # every weight array installed, so that no new one reuses an old id
    e1, e15, e2 = cc.effect_for(-20.0), cc.effect_for(-15.0), strength2_effect()
    conditions = ([("comparison: tau 5 ms, reversal -20, effect 2.22, drive 1.5", 1.5, e1, -20.0, mb_calibration3.TAU_FAST, "comparison")]
                  + [(f"strength 1, reversal -20, drive {d:g}", d, e1, -20.0, TAU, "1") for d in (1.0, 1.5, 2.5, 4.0)]
                  + [(f"strength 1, reversal -15, drive {d:g}", d, e15, -15.0, TAU, "1") for d in (0.5, 1.0, 1.5)]
                  + [(f"strength 2, reversal -20, drive {d:g}", d, e2, -20.0, TAU, "2") for d in (1.5, 2.5, 4.0, 6.0)])
    own_bias = o.own_bias().copy()
    with warm.tracking(o, rec):
        for name, drive, effect, reversal, tau, strength in conditions:
            held += [b.weights, b.slow_weights]
            mb_calibration3.install(o, drive, effect, reversal, calibrated, tau=tau)
            b.set_bias(own_bias)
            kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            off = {odor: [cc.trial(o, rec, odor, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            row = cc.condition(on, off)
            course = row["3-octanol"]["inhibition_course_mv_50ms"]
            row.update({"kc_rest": kc_rest, "drive": drive, "effect": round(effect, 3), "reversal_mv": reversal, "tau_s": tau,
                        "strength": strength, "ceiling_mv": round(mb_calibration3.ceiling_mv(effect, reversal), 2),
                        "ceiling_mv_pipette": round(mb_calibration3.ceiling_mv(effect, PIPETTE_MV), 2),
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
        for name in (chosen, conditions[0][0]):
            _, drive, effect, reversal, tau, _ = next(c for c in conditions if c[0] == name)
            for label, rev in (("reversal", reversal), ("pipette", PIPETTE_MV)):
                held += [b.weights, b.slow_weights]
                mb_calibration3.install(o, drive, effect, rev, calibrated, tau=tau)
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
