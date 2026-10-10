"""Exploratory, not pre-registered: with the projection neurons' membrane reset to rest after a spike, as fly PNs' is,
instead of 5 mV below it, do they answer as strongly as flies'?

odor_probe51.py (the base model): measured as Olsen et al. measured flies, the PNs answer with flies' time course and
lateral division but at half to two thirds of flies' size (Rmax 83-126 in DM4, DL5, VM7d and DM1; flies 144-170).
Every neuron in the model resets 5 mV below rest after a spike (rest_calibration2.py, rung 4: fly central neurons' spikes
leave afterhyperpolarizations of 1.5-8 mV, chosen for the whole brain to quiet bursting neurons), and the PNs fire from
10 mV above rest. Fly PNs' spikes start in the axon while the soma and dendrites stay depolarized ("large sustained
membrane depolarizations capped by small fast spikelets", Iniguez et al. 2013), and Jeanne & Wilson 2015's integrate-
and-fire PN, fitted to PNs' first-spike latencies, resets to rest. odor_pn_reset_check.py: on odor_probe51.py's model,
the PNs' reset at rest (biases polished again, the rest of the build as it was) raises Rmax to 150 in DL5, 155 in VM7d,
145 in DM1 and 105 in DM4 (flies 167, 163, 144, 170), sigma barely moving.
Model: odor_probe51.py's build with the uniglomerular PNs' reset at rest (0 mV; their threshold stays at 10 mV), from
the build's start, so the polishes and the inhibition's fit are made with it. Cached as odor_probe52; measured with
mb_calibration.py's mushroom body.
Measured: as odor_probe51.py, on its seeds.

Ran: with the PNs resetting to rest they answer about as strongly as flies' at strong input, keeping the two pools'
time course, and the Kenyon cells and MBON11 gain with them; weak input and 4-methylcyclohexanol stay where they were.
Built with it, the inhibition's fit gives k_A 0.0017 and k_B 0.0099 (odor_probe51.py: 0.0017, 0.0103), the PNs rest at
2.79 spikes/s where runs begin, the GABAergic ALLNs at 3.58; the LNs answer 2-heptanone with 17.5, 8.9, 7.3 and 6.0
spikes/s (flies 22, 13, 8, 6). Measured with odor_probe16.py's step over all PNs, Rmax is 176, 182 and 172 in DL5, VM7d
and DM1 (odor_probe51.py 141, 145, 137; flies 167, 163, 144) and 81 in DM4 (its vPNs averaged in), sigma 24, 30, 20 and
27. Measured as Olsen et al. measured flies (cholinergic PNs): Rmax 150, 156, 145 and 105 (121, 126, 118, 83; flies 167,
163, 144, 170), sigma 19.8, 24.4, 16.3 and 24.7 (flies 11.8, 12.4, 44.8, 16.3); DL5 rises 19, 47, 105 and 150 spikes/s
at 5, 10, 40 and 160 spikes/s of input (flies 44 at 5.1, 85 at 13.4, 149 at 41.5, 158 at 98.7); strong responses peak at
300-308 spikes/s (flies' VM7 296) and keep 0.36-0.56 of it at 500 ms (flies 0.44), peak over mean 2.0-2.3. 3-octanol's
PNs peak at 89 spikes/s (78) and keep 0.38 of it at 0.40-0.45 s (0.34; flies 0.48); the strongly driven ones peak at 163
(141). 2.4-13.8% of Kenyon cells respond (1.6-8.6%; flies 6 +- 5%), 3-octanol's in flies' class order (alpha'/beta' 17.8%,
alpha/beta 8.8%, gamma 6.2%), the alpha/beta cells firing 1.6-3.6 spikes per response (flies 2.2 +- 1.2), mean Jaccard
0.16; MBON11 gains 24 spikes to 3-octanol and 9.4 to 4-methylcyclohexanol (11.8 and 3.7; flies 118 and 110).
4-methylcyclohexanol stays at 0.52 of 3-octanol at the PNs and 0.26 at the Kenyon cells (flies 0.85-0.98, 0.73-0.92).
This is the base model from here on.

    python experiments/odor_probe52.py         (writes experiments/odor_probe52.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import al_cells
import brain_cache
import odor_probe21 as p21
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe44 as p44
import odor_probe51 as p51
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = p51.SEED, p51.EQUALIZATION_SEED
PN_RESET_MV = 0.0


def build() -> tuple:
    """odor_probe51.build with the uniglomerular PNs resetting to rest from odor_probe21.build on."""
    plain = p21.build

    def at_rest(o):
        out = plain(o)
        o.brain.set_type("uPN", reset=PN_RESET_MV)
        out["upn_reset_mv"] = PN_RESET_MV
        return out
    p21.build = at_rest
    try:
        return p51.build()
    finally:
        p21.build = plain


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "pools": p51.POOLS, "upn_reset_mv": PN_RESET_MV}
    o, rec, built = brain_cache.load("odor_probe52", build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_olsen_protocol_check as olsen
    out["settling"] = o.settling
    out["mb_calibration"] = mb_calibration.apply(o)
    p40.ln_mask = lambda types: al_cells.alln(o)
    try:
        with warm.tracking(o, rec) as held:
            entry = {"build": {x: built[x] for x in ("build", "resting_recalibration", "presynaptic", "rest_check", "settles")
                               if x in built},
                     "ln_response": p40.ln_measure(o, rec, SEED)}
            lr = entry["ln_response"]
            print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
                  json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs",
                  json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:11]), flush=True)
            out["condition"] = entry
            OUT.write_text(json.dumps(out, indent=1))
            entry["olsen_protocol"] = olsen.measure(o, rec, protocols=("olsen",))
            OUT.write_text(json.dumps(out, indent=1))
            entry.update(p36.measure(o, rec, built, SEED))
            print("KCs", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                  "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in entry["mbon11_input"].items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = p44.PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
