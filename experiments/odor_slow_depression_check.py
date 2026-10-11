"""Exploratory check, not pre-registered: with the receptor synapse's slow component depressing as its measurements
suggest instead of as Nagel et al.'s model fit, does the PNs' transform saturate as flies' does?

odor_drive_check.py (odor_probe52.py's model, DL5): over the last 300 ms of the odor the PNs' fast synaptic current is
flat from 20 spikes/s of receptor input on (39, 45, 48, 48 and 48 at 10, 20, 40, 80 and 160), but their slow current
grows almost in proportion to it (5, 8, 13, 23 and 39), and the PNs' rate with it (57 to 176 spikes/s): the slow
component depresses by only 0.73% per spike, recovering over 33 s (odor_probe18.py). Flies' transform saturates by
about 50 spikes/s of input (Olsen et al. 2010), and so does the synapse's charge, slow part included (Kazama & Wilson
2008 Fig. 9D: after 7 Hz, 107% of the 100 Hz charge at 50 spikes/s and 87% at 200). Nagel, Hong & Wilson 2015 measured the
slow (curare-resistant) component depressing to 0.91 per spike, recovering over 0.629 s; they fitted 0.0073 per spike and
33 s to disinhibited odor responses instead, judging that curare incompletely blocks the fast component so the measured
slow component "depressed too quickly" (research_notes/Rung 9 learning data/orn_pn_depression.md section 3). They read the
two components as two receptor types on the same release, which would depress together.
Model: odor_probe52.py's (its cache); the receptor neurons' slow synapses depressing as built (0.9927, 33.2 s), as Nagel et
al. measured them (0.91, 0.629 s), or with the fast synapses (the two pools); each PN's bias polished again to 3 spikes/s
(odor_probe27.pn_polish, 8 rounds), the rest of the build as it was.
Measured: the transform as odor_olsen_protocol_check.py measures it (cholinergic PNs) and odor_equalization_check.py's
summed responses. Seeds: the polish 660000 + 1000 x condition; the measures odor_probe51.py's (570000, 560000).

    python experiments/odor_slow_depression_check.py      (writes experiments/odor_slow_depression_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_probe27 as p27
import odor_probe44 as p44
import odor_probe51 as p51
import odor_probe52 as p52
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 660000
CONDITIONS = (("as built", 0.9927, 33.2), ("as measured", 0.91, 0.629), ("with the fast pools", 0.0, 0.0))


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe52", p52.build, p44.prepare)
    import odor_equalization_check as eq                   # after the cache, so that their edits don't invalidate it
    import odor_olsen_protocol_check as olsen
    b = o.brain
    own = o.own_bias().copy()
    out = {"question": __doc__, "conditions": {}}
    with warm.tracking(o, rec):
        for c, (name, dep, rec_s) in enumerate(CONDITIONS):
            b.set_bias(own.copy())
            b.set_type("ORN", slow_depression=dep, slow_recovery=rec_s)
            entry = {"slow_depression": dep, "slow_recovery_s": rec_s}
            if c:
                entry["polish"] = p27.pn_polish(o, rec, SEED + 1000 * c, rounds=8)["pn_polish"][-1]
            transform = olsen.measure(o, rec, protocols=("olsen",), show=False)["olsen"]
            entry["olsen_protocol"] = transform
            entry["fits"] = {g: transform[g]["cholinergic"]["fit"] for g in transform}
            entry["equalization"] = eq.measure(o, rec, p51.EQUALIZATION_SEED)
            out["conditions"][name] = entry
            print(name, json.dumps(entry["fits"]),
                  json.dumps({g: [transform[g]["cholinergic"]["points"][x]["window_mean"] for x in ("5", "10", "40", "160")]
                              for g in transform}),
                  json.dumps({g: [transform[g]["cholinergic"]["points"][x]["at_500ms_over_peak"] for x in ("10", "40", "160")]
                              for g in ("DL5", "VM7d")}), "MCH/OCT", json.dumps(entry["equalization"]["mch_over_oct"]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    b.set_type("ORN", slow_depression=CONDITIONS[0][1], slow_recovery=CONDITIONS[0][2])
    b.set_bias(own)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
