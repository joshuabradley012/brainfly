"""Rung 9, learning, attempt 1 (pre-registered): on brainfly's olfactory pathway, does the mushroom body's dopamine
learning rule depress MBON11's response to an odor paired with dopamine as flies' does (Hige et al. 2015), sparing the
unpaired odor as much as flies' does, in both directions, and not at all when dopamine comes first?

The ladder's benchmark for rung 9's learning half is "80-90% depression after 1 s of odour paired with dopamine" (its
scrambled-wiring null belongs to the rung's other half, resting FC once arousal gives the brain its brain-wide state).
Hige et al.'s 4-pulse experiments give the paired odor's spikes 76-86% down; the rule's rate here is fitted so that the
paired odor's charge falls 90% (as Hige et al.'s Fig. 3 found), so the paired odor's depression is largely built in, and
what tests the model is how specific it is. The bands are research_notes/Rung 9 learning data/hige2015_specificity.md's
(section 8), written before any pilot used them. Learning pilots 2-8 (exploratory) ran this protocol on earlier models;
on every model since learning_pilot3.py the 3-octanol-paired direction has matched flies and the reciprocal has fallen
short (3-octanol's spikes down 5-14% with 4-methylcyclohexanol paired, flies 38%), because 4-methylcyclohexanol reaches a
quarter as many Kenyon cells as 3-octanol, where flies' two odors reach about as many. So this attempt is expected to
fail on the reciprocal; it is run to fix the rung's status on the model as it stands. Its design, the weighed input
included (chosen on accuracy), was fixed on 10 October 2026 at 21:55 PDT, before learning_pilot8.py, which runs the same
protocol on the same model with the pilots' seeds, had reported.
Model: odor_probe56.py's (its cache; the PNs resting at about flies' rate) with mb_calibration.py's mushroom body, the
Kenyon cells' rest set to its classes' distances below threshold (odor_probe33.set_rest), MBON11 keeping its synaptic
current and held near 6 Hz as Hige et al.
held their cells, its Kenyon cell synapses at 0.054 pC each (learning_pilot5.py) and depressing as measured (Yamada et
al. 2024: 0.5 of the strength left per spike, recovering over 1.5 s). Receptor input: receptor_fills.RECOMMENDED for both
odors (the receptor-level evidence at Hige et al.'s 2% of saturated vapour, with DoOR's import errors corrected), DoOR
for the others.
Protocol, rule, fit and measures as learning_pilot5.py (learning_pilot4.variant, depressing): four 1 ms dopamine pulses at
2 Hz from 0.2 s into a 1 s odor; each Kenyon cell's synapses onto MBON11 scaled by exp(-eta E), E its eligibility trace
(tau_e 0.5 s) at the pulses; eta fitted, for each pairing, so that the paired odor's charge onto MBON11 falls 90%; MBON11's
evoked spikes over 0-1.4 s from odor onset less 1.4 times the second before, before and after pairing (the ratio of the
means over all flies); backward pairing: the same pulses 2.0-0.5 s before the odor, eta as fitted forward. Seeds 910000
(learning_pilot3.py's offsets), used by no earlier run.
Tests (OCT 3-octanol, MCH 4-methylcyclohexanol):
  PAIRED      with OCT paired, OCT's spikes fall at least 65%, and at least 30 percentage points more than MCH's
              (flies 80% and 27%)
  UNPAIRED    with OCT paired, MCH's spikes and its charge each fall 10-45% (flies: spikes 27%, 95% CI 10-44%; charge
              20% and 35%)
  RECIPROCAL  with MCH paired, MCH's spikes fall at least 65% and at least 30 points more than OCT's, and OCT's fall
              15-50% (flies 76% and 38%)
  BACKWARD    with the dopamine first, the paired odor's charge changes by at most 15% either way, in both pairings
              (flies' spikes +7% and -4%; the model measures charge for this condition, which its spikes follow)
Pass: all four.
Reported: MBON11's responses before and after, their SEMs, the charges, the Kenyon cells answering each odor and their
overlap, eta, and the charge drops at tau_e 0.2 and 1 s.


Ran (2026-10-10, 14 minutes; the text above is the pre-registration as it ran): fail, on RECIPROCAL, as expected.
  PAIRED      passes. Pairing 3-octanol cuts its MBON11 spikes from 31.2 to 3.5 (89%), 58 points more than
              4-methylcyclohexanol's.
  UNPAIRED    passes. 4-methylcyclohexanol's spikes fall from 5.8 to 4.0 (31%) and its charge 30%.
  RECIPROCAL  fails. Pairing 4-methylcyclohexanol cuts its own spikes to nothing (99%) but 3-octanol's only from 31.2
              to 29.6 (4.9%; flies 38%, band 15-50%), its charge 6.9%.
  BACKWARD    passes. The paired odor's charge changes 0.1% (3-octanol) and 1.4% (4-methylcyclohexanol).
MBON11, held at 5.3 Hz (its bias 7.7 mV lower; gain 3.49 spikes/s per mV), gains 31.2 +- 0.6 spikes to 3-octanol and 5.8 +-
0.4 to 4-methylcyclohexanol before pairing (flies 118 +- 8.3 and 110 +- 11). 407 Kenyon cells gain more than half a spike
to 3-octanol and 60 to 4-methylcyclohexanol (flies about as many each). 37% of 4-methylcyclohexanol's responders also
answer 3-octanol and carry 30% of its charge, which is why pairing 3-octanol spares it as much as flies' does; but its 60
responders carry only 3.4% of 3-octanol's charge, so pairing it can barely touch 3-octanol. tau_e changes nothing (0.2-1
s, within a percentage point). The failure is the one learning pilots 3-8 found: with the receptor input the evidence
supports, 4-methylcyclohexanol reaches too few Kenyon cells, because the model's PNs give its many weakly driven
glomeruli about three quarters of flies' gain at best and its presynaptic inhibition then silences the weakest
(odor_weak_glomeruli_check.py, odor_probe56.py).

    python experiments/rung9_learning.py        (writes experiments/rung9_learning.json; about half an hour)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import learning_pilot3 as lp3
import learning_pilot4 as lp4
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe56 as p56
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SCRATCH = OUT.with_name(OUT.stem + "_variant.json")
SEED = 910000
CHARGE_PC = 0.030 * 34.5 / 19.0
OCT, MCH = "3-octanol", "4-methylcyclohexanol"


def verdicts(row: dict) -> dict:
    by = {(p["paired"], p["unpaired"]): p for p in row["pairings"]}
    oct_p, mch_p = by[(OCT, MCH)], by[(MCH, OCT)]
    s = lambda p, od: p["spikes"][od]["drop"]
    c = lambda p, od: p["by_tau"]["0.5"]["charge_drop"][od]
    b = lambda p: p["by_tau"]["0.5"]["backward_charge_drop"]
    out = {"PAIRED": {"oct_spikes_drop": s(oct_p, OCT), "gap": round(s(oct_p, OCT) - s(oct_p, MCH), 3)},
           "UNPAIRED": {"mch_spikes_drop": s(oct_p, MCH), "mch_charge_drop": c(oct_p, MCH)},
           "RECIPROCAL": {"mch_spikes_drop": s(mch_p, MCH), "gap": round(s(mch_p, MCH) - s(mch_p, OCT), 3),
                          "oct_spikes_drop": s(mch_p, OCT)},
           "BACKWARD": {"oct_paired_charge_change": b(oct_p), "mch_paired_charge_change": b(mch_p)}}
    out["PAIRED"]["pass"] = out["PAIRED"]["oct_spikes_drop"] >= 0.65 and out["PAIRED"]["gap"] >= 0.30
    out["UNPAIRED"]["pass"] = all(0.10 <= x <= 0.45 for x in (out["UNPAIRED"]["mch_spikes_drop"], out["UNPAIRED"]["mch_charge_drop"]))
    r = out["RECIPROCAL"]
    r["pass"] = r["mch_spikes_drop"] >= 0.65 and r["gap"] >= 0.30 and 0.15 <= r["oct_spikes_drop"] <= 0.50
    out["BACKWARD"]["pass"] = all(abs(x) <= 0.15 for x in (b(oct_p), b(mch_p)))
    out["pass"] = all(out[k]["pass"] for k in ("PAIRED", "UNPAIRED", "RECIPROCAL", "BACKWARD"))
    return out


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    lp4.SEED, lp4.OUT = SEED, SCRATCH
    o, rec, built = brain_cache.load("odor_probe56", p56.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "charge_pc_per_synapse": round(CHARGE_PC, 4), "mb_calibration": mb_calibration.apply(o)}
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True) as inputs:
        out["inputs"] = inputs
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        row = lp4.variant(o, rec, True, {"variants": {}})
    out["result"] = row
    out["verdicts"] = verdicts(row)
    SCRATCH.unlink(missing_ok=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("verdicts", json.dumps(out["verdicts"]), f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
