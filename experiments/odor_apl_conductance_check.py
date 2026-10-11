"""Exploratory check, not pre-registered: with APL's synapses onto the Kenyon cells acting as a conductance, held to
flies' 10-12 mV saturation, can APL answer 4-methylcyclohexanol with about half its response to 3-octanol (flies 0.49)
and raise the Kenyon cells' spikes 2-3-fold when silenced, without holding them more than 15 mV down during an odor?

odor_apl_inhibition_check.py: mb_calibration2.py's graded APL meets the first two of flies' numbers with synapses onto the
Kenyon cells 2.5 times mb_calibration.py's, but as a current they hold the Kenyon cells up to 20 mV down as 3-octanol
begins, and could hold them 27.5 mV down at APL's ceiling, where flies' APL saturates at 10-12 mV however hard it is
driven (Inada et al. 2017) and Kenyon cells inhibit one another through it by 15 mV at most (Vrontou et al. 2021). A
synapse's effect ends at its reversal potential: APL's GABA-A (about 40% of its effect on Kenyon cells) and GABA-B (35%)
receptors reverse below a Kenyon cell's rest (Inada et al.), and a conductance divides a cell's other input as well as
pulling it toward that potential, most when the cell is depolarized.
Model: odor_probe60.py's (its cache) with mb_calibration.py's mushroom body and the Kenyon cells' rest as the learning
pilots set it, then mb_calibration3.install: APL's synapses onto the Kenyon cells in the slow current, which in the
Kenyon cells decays with the fast current's 5 ms and reverses `reversal` mV from rest, at `effect` times mb_calibration.py's
weights; the Kenyon cells' synapses onto APL at `drive` times MaleCNS's. For each reversal (-15, -20 and -30 mV, the span
a GABA-A and GABA-B mixture below a resting potential of about -50 to -60 mV allows), effect is set so that APL's ceiling
holds a quiet Kenyon cell 11 mV down (the middle of Inada et al.'s 10-12; mb_calibration3.ceiling_mv): 3.75, 2.22 and
1.58. Then drive at 1, 1.5, 2.5, 4, 6 and 10 times MaleCNS's. Also, as controls at reversal -20: the same synapses as a
current in the slow channel (reversal infinite, effect 2.22 and mb_calibration2.py's 2.5 at drive 1.5), separating the
conductance from the move out of the fast current (whose input a Kenyon cell's spike erases); and, first, mb_calibration.py's
and mb_calibration2.py's APL as they were (fast current; drive 10 and effect 1, drive 1.5 and effect 2.5), measured the same
way for comparison.
Each condition sets the Kenyon cells' rest anew with its APL working (odor_probe33.set_rest, as the learning pilots do
after installing the mushroom body), so that they start at their measured distances below threshold, and silencing APL
then removes its tonic inhibition too, as it would in flies.
Measured as odor_apl_inhibition_check.py measures (odor_apl_check.trial's protocol: DoOR's input, a 1 s odor after 1.5 s,
2 seeds of 8 flies, APL working and silenced, the same seeds for every condition): APL's
release (peak of 50 ms means, mean over the odor) and its 4-methylcyclohexanol/3-octanol ratio; the Kenyon cells
answering each odor (more than half a spike over the odor's first second) and their spikes, with APL working and
silenced, and the rise silencing gives; the odors' shared answering cells; the Kenyon cells' free membrane potential with
APL working less silenced (its course in 50 ms means from the odor's onset, the largest of them, the mean over the odor's
first second of the cells firing in neither condition, and at rest).
Chosen, as stated before running: among the conductance conditions whose silencing raises both odors' Kenyon cell spikes
2-3-fold, the one whose APL peak ratio is nearest 0.49 (by |log|); if none does, the one nearest both (the summed squared
log ratios to 2.5 and 0.49), reported as missing. Then reported against flies: its largest inhibition during 3-octanol
(15 mV at most), how it equalizes the odors (the answering ratio with APL working over silenced; flies' claws 1.25-fold,
Prisco et al. 2021), and the share of each odor's answering cells answering both (flies 0.30 and 0.33).

Ran (33 minutes): yes, at a reversal of -20 mV. Chosen by the rule: APL's synapses onto the Kenyon cells a conductance
reversing 20 mV below rest, 2.22 times mb_calibration.py's (so that APL's ceiling holds a quiet Kenyon cell 11 mV down),
and the Kenyon cells' drive onto APL 1.5 times MaleCNS's. APL then answers 4-methylcyclohexanol with 0.45 of its peak
for 3-octanol (27.7 and 12.5 Hz; flies 0.49), silencing it raises the Kenyon cells' spikes 2.92 and 2.21-fold (flies
2-3), and as 3-octanol begins it holds them at most 7.1 mV down (mb_calibration2.py's APL, measured here the same way,
20.8; flies 15 at most), 1.6 mV over the odor for the cells that never fire (4.7) and 0.7 mV at rest (2.2). 345 and 230
Kenyon cells answer the two odors (426 and 287), 0.30 of 3-octanol's and 0.45 of 4-methylcyclohexanol's answering both
(flies 0.30 and 0.33), and APL raises 4-methylcyclohexanol's share of answering cells 1.45-fold (flies' claws 1.25; 1.41
for mb_calibration2.py's). One other condition met the silencing rule: reversal -30 at drive 2.5 (APL's ratio 0.54,
silencing 2.72 and 2.19, at most 8.3 mV). At -15 silencing raises 3-octanol's spikes more than 3-fold at every drive
(3.5-11), and at -30 the drives below 2.5 leave 4-methylcyclohexanol's rise under 2. The driving force is what does it:
the same synapses as a current in the slow channel (2.22, drive 1.5) hold the Kenyon cells 19.2 mV down while silencing
raises their spikes only 2.40 and 1.96-fold; moving them out of the fast current alone changes nothing (mb_calibration2.py's
synapses there: 2.54 and 1.97, 20.8 mV; as they were, 2.51 and 1.98, 20.8). A conductance divides a depolarized Kenyon
cell's input more than it pulls a quiet one down, which is how flies' APL can hold responding Kenyon cells back 2-3-fold
while taking none of them more than 10-12 mV below rest. Still unlike flies': the inhibition is largest 80-110 ms into
the odor (flies' lags by several hundred ms), and 4-methylcyclohexanol's answering cells are 0.67 of 3-octanol's (flies
about 0.9). Rechecked, mb_calibration.py's APL as calibrated: 0.995, 2.43 and 2.41, at most 10.6 mV. (In the result
file a conductance row's ceiling_mv is the distance below rest, a current row's is signed.) mb_calibration3.py installs
the chosen APL.

    python experiments/odor_apl_conductance_check.py      (writes experiments/odor_apl_conductance_check.json)
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
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 850000, 2
ODORS = ("3-octanol", "4-methylcyclohexanol")
REVERSALS = (-15.0, -20.0, -30.0)
DRIVES = (1.0, 1.5, 2.5, 4.0, 6.0, 10.0)
CEILING_MV = -11.0
FLIES = {"apl_mch_over_oct": 0.49, "block_ratio": [2.0, 3.0], "largest_inhibition_mv": -15.0, "equalization": 1.25,
         "share_answering_both": {"3-octanol": 0.30, "4-methylcyclohexanol": 0.33}}


def effect_for(reversal: float, ceiling: float = CEILING_MV) -> float:
    """The effect (times mb_calibration.py's synapses) whose conductance holds a quiet Kenyon cell `ceiling` mV from rest
    at APL's ceiling: 11 e / (1 + 11 e / |reversal|) = |ceiling|."""
    import mb_calibration
    c, r = abs(ceiling), abs(reversal)
    return c * r / (abs(mb_calibration.KC_SATURATION_MV) * (r - c))


def free_potential(b, x: np.ndarray, sl: np.ndarray) -> np.ndarray:
    """odor_gaba_block_check.free_potential with the slow current's driving force where it has a reversal potential: the
    fixed point of u = a_vv u + a_vx x + a_bias + tonic + a_vs s (1 - u r_inv)."""
    k, c = b._kernel_tables(), b.cls
    tonic = b._tonic if len(b._tonic) else 0.0
    slow = np.where(b.slow_in, k["a_vs"][c] * sl, 0.0) if len(b.slow_weights) else 0.0
    return (k["a_vx"][c] * x + k["a_bias"][c] + tonic + slow) / (1.0 - k["a_vv"][c] + slow * k["r_inv"][c])


def trial(o, rec, odor: str, seed: int, apl: np.ndarray, silence) -> dict:
    """odor_apl_inhibition_check.trial with the free potential above."""
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
    rest_x = rest_s = 0.0
    for _ in range(100):
        b.advance(piece, drive=rec.at(plan, t), silence=silence)
        rest_x, rest_s = rest_x + b.x / 100, rest_s + b.s / 100
        t += p10.PIECE
    spikes, odor_x, odor_s, course, release = 0, 0.0, 0.0, [], []
    for k in range(140):
        fired = b.advance(piece, drive=rec.at(plan, t), silence=silence)
        release.append(float(b.release[:, q].mean()))
        course.append(float(free_potential(b, b.x, b.s)[:, kc].mean()))
        if k < 100:
            spikes = spikes + fired[:, kc]
            odor_x, odor_s = odor_x + b.x / 100, odor_s + b.s / 100
        t += p10.PIECE
    return {"rest": free_potential(b, rest_x, rest_s)[:, kc], "odor": free_potential(b, odor_x, odor_s)[:, kc],
            "spikes": np.asarray(spikes), "course": np.array(course), "release": np.array(release)}


def condition(on: dict, off: dict) -> dict:
    """APL working (on) against silenced (off), each {odor: [trials]}, the same seeds."""
    out = {}
    answering = {"APL working": {}, "APL silenced": {}}
    for odor in ODORS:
        a, z = on[odor], off[odor]
        d_odor = np.concatenate([x["odor"] - y["odor"] for x, y in zip(a, z)])
        d_rest = np.concatenate([x["rest"] - y["rest"] for x, y in zip(a, z)])
        quiet = np.concatenate([(x["spikes"] == 0) & (y["spikes"] == 0) for x, y in zip(a, z)])
        smooth = np.convolve(np.mean([x["course"] - y["course"] for x, y in zip(a, z)], 0), np.ones(5) / 5, mode="valid")
        release = np.mean([x["release"] for x in a], 0)
        spikes_on = np.concatenate([x["spikes"] for x in a]).mean(0)
        spikes_off = np.concatenate([y["spikes"] for y in z]).mean(0)
        answering["APL working"][odor], answering["APL silenced"][odor] = spikes_on > 0.5, spikes_off > 0.5
        out[odor] = {"apl_release_peak_hz": round(float(np.convolve(release, np.ones(5) / 5, mode="valid").max()), 2),
                     "apl_release_mean_hz": round(float(release[:100].mean()), 2),
                     "kcs_answering": int((spikes_on > 0.5).sum()), "kcs_answering_silenced": int((spikes_off > 0.5).sum()),
                     "kc_spikes": round(float(spikes_on.sum()), 1), "kc_spikes_silenced": round(float(spikes_off.sum()), 1),
                     "block_ratio": round(float(spikes_off.sum() / max(spikes_on.sum(), 1e-9)), 2),
                     "largest_inhibition_mv_50ms": round(float(smooth.min()), 2),
                     "inhibition_mv_silent_cells": round(float(d_odor[quiet].mean()), 2),
                     "inhibition_mv_at_rest": round(float(d_rest.mean()), 2),
                     "inhibition_course_mv_50ms": np.round(smooth, 2).tolist(),
                     "apl_release_course_hz": np.round(release, 2).tolist()}
    a, c = out["3-octanol"], out["4-methylcyclohexanol"]
    out["apl_peak_mch_over_oct"] = round(c["apl_release_peak_hz"] / max(a["apl_release_peak_hz"], 1e-9), 3)
    out["apl_mean_mch_over_oct"] = round(c["apl_release_mean_hz"] / max(a["apl_release_mean_hz"], 1e-9), 3)
    ratio_on = c["kcs_answering"] / max(a["kcs_answering"], 1)
    ratio_off = c["kcs_answering_silenced"] / max(a["kcs_answering_silenced"], 1)
    out["answering_mch_over_oct"] = {"APL working": round(ratio_on, 3), "APL silenced": round(ratio_off, 3),
                                     "equalization": round(ratio_on / max(ratio_off, 1e-9), 3)}
    both = answering["APL working"]["3-octanol"] & answering["APL working"]["4-methylcyclohexanol"]
    out["share_answering_both"] = {od: round(int(both.sum()) / max(int(answering["APL working"][od].sum()), 1), 3) for od in ODORS}
    return out


def score(row: dict) -> tuple:
    """The choice rule: (misses the 2-3-fold silencing rise for either odor, then the distance)."""
    blocks = [row[od]["block_ratio"] for od in ODORS]
    meets = all(2.0 <= x <= 3.0 for x in blocks)
    apl = abs(np.log(max(row["apl_peak_mch_over_oct"], 1e-9) / 0.49))
    far = apl if meets else apl ** 2 + sum(np.log(max(x, 1e-9) / 2.5) ** 2 for x in blocks)
    return (not meets, far)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import mb_calibration3
    b = o.brain
    out = {"question": __doc__, "flies": FLIES, "mb_calibration": mb_calibration.apply(o), "conditions": {}}
    apl = b.cells(["APL"])
    calibrated = b.weights.copy()
    held = []                                          # every weight array installed, so that no new one reuses an old id
    conditions = [(f"reversal {r:g}, effect {effect_for(r):.2f}, drive {d:g}", d, effect_for(r), r) for r in REVERSALS for d in DRIVES]
    conditions += [("current (slow), effect 2.22, drive 1.5", 1.5, effect_for(-20.0), np.inf),
                   ("current (slow), effect 2.5, drive 1.5", 1.5, 2.5, np.inf)]
    own_bias = o.own_bias().copy()
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    kc_apl = o.m["kc"][pre] & np.isin(b.idx, apl)
    apl_kc = np.isin(pre, apl) & o.m["kc"][b.idx]
    fast = [("mb_calibration.py (fast current), drive 10, effect 1", 10.0, 1.0),
            ("mb_calibration2.py (fast current), drive 1.5, effect 2.5", 1.5, 2.5)]
    with warm.tracking(o, rec):
        for name, drive, effect, reversal in [(n, d, e, None) for n, d, e in fast] + conditions:
            held += [b.weights, b.slow_weights]
            if reversal is None:                       # as the earlier calibrations had it, before anything moves
                w = calibrated.copy()
                w[kc_apl] *= drive / mb_calibration.KC_APL_SCALE
                w[apl_kc] *= effect
                b.weights, b._external_matrix = w, None
                reversal = np.inf
                moved = False
            else:
                mb_calibration3.install(o, drive, effect, reversal, calibrated)
                moved = True
            b.set_bias(own_bias)
            kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
            on = {odor: [trial(o, rec, odor, SEED + 10 * j + k, apl, ()) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            off = {odor: [trial(o, rec, odor, SEED + 10 * j + k, apl, apl) for k in range(SEEDS)] for j, odor in enumerate(ODORS)}
            row = condition(on, off)
            row["kc_rest"] = kc_rest
            row.update({"drive": drive, "effect": round(effect, 3), "channel": "slow" if moved else "fast",
                        "reversal_mv": None if not np.isfinite(reversal) else reversal,
                        "ceiling_mv": round(mb_calibration3.ceiling_mv(effect, reversal), 2) if np.isfinite(reversal)
                        else round(mb_calibration.KC_SATURATION_MV * effect, 2)})
            out["conditions"][name] = row
            a, c = row["3-octanol"], row["4-methylcyclohexanol"]
            print(f"{name}: APL peak {a['apl_release_peak_hz']}/{c['apl_release_peak_hz']} (ratio {row['apl_peak_mch_over_oct']})"
                  f" | block {a['block_ratio']}/{c['block_ratio']} | KCs {a['kcs_answering']}/{c['kcs_answering']}"
                  f" | largest {a['largest_inhibition_mv_50ms']} mV, silent {a['inhibition_mv_silent_cells']}, rest"
                  f" {a['inhibition_mv_at_rest']} | equalization {row['answering_mch_over_oct']['equalization']}"
                  f" | both {row['share_answering_both']}", flush=True)
            OUT.write_text(json.dumps(out, indent=1, default=float))
    candidates = {k: v for k, v in out["conditions"].items() if v["reversal_mv"] is not None}
    chosen = min(candidates, key=lambda k: score(candidates[k]))
    out["chosen"] = {"condition": chosen, "meets_block_ratio": not score(candidates[chosen])[0]}
    b.weights, b._external_matrix = calibrated, None
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print("chosen:", json.dumps(out["chosen"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
