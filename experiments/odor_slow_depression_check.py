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

Ran: either measured-like depression makes the transform saturate and brings sigma to flies', and neither moves
4-methylcyclohexanol. Over the cholinergic PNs, Olsen et al.'s protocol, DL5, VM7d, DM4 and DM1:
  as built (0.9927, 33.2 s): sigma 19.7, 24.5, 24.7, 16.3; Rmax 150, 156, 105, 145; DL5 rising 19, 47, 105 and 151
    spikes/s at 5, 10, 40 and 160 spikes/s of input (160 over 40: 1.43); strong responses keep 0.56 of their peak at
    500 ms; 4-methylcyclohexanol's PNs 0.53 of 3-octanol's;
  as measured (0.91, 0.629 s): sigma 14.9, 17.3, 16.8, 12.0; Rmax 136, 141, 91, 134; DL5 20, 52, 111 and 131 (1.18);
    strong 0.37; 0.52;
  with the fast pools: sigma 12.7, 15.2, 13.4, 10.7; Rmax 107, 106, 68, 107; DL5 19, 46, 92 and 103 (1.12); strong
    0.26-0.28; 0.51.
Flies: sigma 11.8, 12.4, 16.3 and 44.8, Rmax 167, 163, 170 and 144; DL5 44 at 5.1, 85 at 13.4, 149 at 41.5 and 158 at
98.7 (98.7 over 41.5: 1.06); strong responses 0.44 of their peak at 500 ms. By sigma and saturation alone (the criterion
stated before the last condition came in) the fast pools are a little closer (sigma off by 0.9, 2.8 and 2.9 against
3.1, 4.9 and 0.5; 1.12 against 1.18), but they take Rmax down to two thirds of flies' and make strong responses fall
faster than flies'; the measured depression keeps Rmax within about 15% of flies' in three glomeruli and strong responses
near flies' shape, so it is the one carried forward (odor_probe54.py). The weakest input still gets half of flies'
response, and DM1, without its GABA, is the most sensitive.

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
