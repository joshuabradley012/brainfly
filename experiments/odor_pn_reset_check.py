"""Exploratory check, not pre-registered: with the PNs' membrane reset only part of the way to rest after a spike, are
their responses as large as flies'?

odor_probe51.py (the base model) with odor_olsen_protocol_check.py's protocol: the PNs answer with roughly flies'
steepness and time course but at half to two thirds of flies' size at every input (cholinergic PNs: Rmax 83-126, flies
163-170; DL5 at 5 and 10 spikes/s of receptor input 19 and 36 spikes/s, flies about 44 at 5 and 85 at 13). The PNs follow
Shiu et al.'s rule of resetting the membrane to rest after each spike (keeping their synaptic current, odor_probe41.py).
In flies a PN's spikes start in its axon while its soma and dendrites stay depolarized through firing ("large sustained
membrane depolarizations capped by small fast spikelets", Iniguez et al. 2013; Gouwens & Wilson 2009); in a point neuron
that is a reset part of the way to threshold. Nothing measures how far. In a one-PN model with brainfly's synapse a reset
at 5.5 mV (threshold 7) raised Rmax and lowered sigma (research_notes/Rung 9 learning data/weak_input_gain.md, section 9).
Model: odor_probe51.py's (its cache), the uniglomerular PNs' reset at 0 (as built), 3, 5 and 6 mV above rest (threshold
7), each PN's bias polished again to rung 4's 3 spikes/s (odor_probe27.pn_polish, 8 rounds), the rest of the build as it
was (the inhibition not refitted).
Measured: the transform as odor_olsen_protocol_check.py measures it (Olsen et al.'s protocol, cholinergic PNs), and
odor_equalization_check.py's summed responses. Seeds: the polish 610000 + 1000 x condition; the measures odor_probe51.py's
(570000 and 560000), the same for every condition.

    python experiments/odor_pn_reset_check.py      (writes experiments/odor_pn_reset_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_probe27 as p27
import odor_probe44 as p44
import odor_probe51 as p51
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 610000
RESETS_MV = (0.0, 3.0, 5.0, 6.0)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe51", p51.build, p44.prepare)
    import odor_equalization_check as eq                   # after the cache, so that their edits don't invalidate it
    import odor_olsen_protocol_check as olsen
    b = o.brain
    own = o.own_bias().copy()
    out = {"question": __doc__, "conditions": {}}
    with warm.tracking(o, rec):
        for c, reset in enumerate(RESETS_MV):
            b.set_bias(own.copy())
            b.set_type("uPN", reset=reset)
            entry = {"reset_mv": reset}
            if reset:
                entry["polish"] = p27.pn_polish(o, rec, SEED + 1000 * c, rounds=8)["pn_polish"][-1]
            transform = olsen.measure(o, rec, protocols=("olsen",), show=False)["olsen"]
            entry["olsen_protocol"] = transform
            entry["fits"] = {g: transform[g]["cholinergic"]["fit"] for g in transform}
            entry["equalization"] = eq.measure(o, rec, p51.EQUALIZATION_SEED)
            out["conditions"][f"{reset:g}"] = entry
            print(f"reset {reset:g} mV:", json.dumps(entry["fits"]),
                  json.dumps({g: [transform[g]["cholinergic"]["points"][x]["window_mean"] for x in ("5", "10", "40", "160")]
                              for g in transform}), "MCH/OCT", json.dumps(entry["equalization"]["mch_over_oct"]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    b.set_type("uPN", reset=0.0)
    b.set_bias(own)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
