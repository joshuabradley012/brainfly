"""Exploratory check, not pre-registered and not a change to the model: would a rise time on APL's conductance give the
Kenyon cells flies' time course in Inada et al.'s test?

odor_apl_conductance2_check.py (with the correction after it): in the model's copy of Inada et al. 2017's Fig. 5B (APL
driven to its ceiling for 1 s at rest, the quiet Kenyon cells' free potential), the current APL's inhibition reaches 10, 50
and 90% of its plateau 0.01, 0.14 and 0.42 s into the drive, where flies' does at 0.14, 0.27 and 0.56 s; it is half gone
0.36 s after the drive (flies 0.32) but leaves 0.08 of itself at 1 s and none at 2 s (flies 0.22 and 0.13;
research_notes/Rung 9 learning data/apl_kinetics.md). The model has no delay or rise before the conductance builds
(apl_kinetics.md suggested about 50 ms). HybridBrain's slow_rise (learning_pilot12.py) now gives a slow current a rise.
Model: odor_probe60.py's (its cache) with mb_calibration4.py's mushroom body, the Kenyon cells' rest set as the learning
pilots set it; the Kenyon cells' slow current (APL's conductance, decaying with 0.3 s) given a rise time of 0, 30, 60,
100 and 150 ms (its steady effect, and so the rest, unchanged). Measured: odor_apl_conductance2_check.apl_drive, one seed
of 8 flies, for each.

Ran (2026-10-11, 3 minutes): a rise time trades the rise for the fall; no single one gives flies' course. Without one the
inhibition reaches 10, 50 and 90% of its plateau (8.1 mV) 0.02, 0.12 and 0.41 s into the drive and is half gone 0.37 s
after it, 0.11 left at 1 s and none at 2 s. With 30, 60, 100 and 150 ms of rise: 0.05/0.15/0.41, 0.06/0.18/0.50,
0.08/0.23/0.52 and 0.08/0.24/0.55 s (flies 0.14/0.27/0.56), but half gone 0.42, 0.44, 0.51 and 0.53 s after (flies 0.32),
with 0.10-0.18 left at 1 s and 0.01-0.03 at 2 s (flies 0.22 and 0.13); the plateau doesn't move (7.97-8.14 mV). Flies'
course reads as a delay of about 0.12 s, a quick approach (an exponential of about 0.2 s from 0.12 gives 0.14, 0.26 and
0.58 s) and a fall with a long tail, which would take a delay and two decaying parts, not a rise; and some of the delay
may be the optogenetic drive's, not APL's synapses'. Not taken further: APL's conductance stays as mb_calibration4.py
set it.

    python experiments/odor_apl_rise_check.py      (writes experiments/odor_apl_rise_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_apl_conductance2_check as cc2
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 640000                                           # the learning pilots' rest
RISES = (0.0, 0.03, 0.06, 0.10, 0.15)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    b = o.brain
    out = {"question": __doc__, "flies": cc2.FLIES["inada_5b"], "mb_calibration": mb_calibration4.apply(o), "rises": {}}
    apl = b.cells(["APL"])
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        for rise in RISES:
            b.set_type("kenyon_cells", slow_rise=rise)
            res = cc2.apl_drive(o, rec, SEED + 5000, apl)
            out["rises"][str(rise)] = res
            print(f"rise {rise * 1000:.0f} ms:", json.dumps({k: v for k, v in res.items() if k not in ("course_mv", "plateau_mv_by_class")}),
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)
            OUT.write_text(json.dumps(out, default=float))
        b.set_type("kenyon_cells", slow_rise=0.0)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
