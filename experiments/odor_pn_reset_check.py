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

Correction, found while it ran: the model's PNs don't reset to rest. Every neuron resets 5 mV below rest (the type key
"all", rest_calibration2.py, rung 4: fly central neurons' spikes leave 1.5-8 mV afterhyperpolarizations) and the PNs fire
from 10 mV above rest, not 7. So "0 (as built)" above is wrong: the as-built reset is -5 mV, every condition here raises
it (by 5, 8, 10 and 11 mV), and the 0 mV condition skipped the polish (its PNs rest at 2.4-2.9 spikes/s before the valve,
as built 2.2-2.8). The as-built numbers come from odor_probe51.py's measure on the same seeds (mb_calibration.py's
mushroom body doesn't change the PNs' responses: 83.8 spikes/s in DL5 at 40 with it and without).

Ran: raising the reset scales the PNs' responses up from 10 spikes/s of input on, but barely the weakest, and moves
neither sigma much nor 4-methylcyclohexanol. Over the cholinergic PNs, Olsen et al.'s protocol, Rmax for DM4, DL5, VM7d
and DM1 is 83, 121, 126 and 118 as built (-5 mV), 105, 150, 155 and 145 at rest, 128, 176, 182 and 172 at 3 mV, 151, 200,
207 and 197 at 5, and 166, 217, 223 and 213 at 6 (flies 170, 167, 163, 144); sigma 23.5, 19.5, 24.3 and 17.3 as built,
24.0, 19.0, 24.5 and 16.5 at rest, 21.7, 17.1, 22.1 and 13.5 at 6 (flies 16.3, 11.8, 12.4, 44.8). DL5's PNs rise 19, 36,
84 and 123 spikes/s at 5, 10, 40 and 160 as built, 20, 49, 107 and 151 at rest, 26, 74, 165 and 215 at 6 (flies: 44 at
5.1, 85 at 13.4, 149 at 41.5, 158 at 98.7): flies' curve rises steeply and saturates by about 50, the model's keeps
rising at any reset. 4-methylcyclohexanol's summed PN response stays at 0.52 of 3-octanol's. A reset at rest, as in
Jeanne & Wilson's fitted PN, brings Rmax within about 10% of flies' in DL5, VM7d and DM1; higher resets overshoot them.

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
