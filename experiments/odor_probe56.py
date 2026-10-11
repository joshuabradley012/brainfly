"""Exploratory, not pre-registered: odor_probe54.py rebuilt with the projection neurons resting at flies' measured rate.

odor_pn_rest_check.py: on odor_probe54.py's model, polishing the uniglomerular PNs toward flies' resting rate (4.6 +- 4.2
spikes/s, Turner et al. 2008; about 4.5 in Bhandawat et al. 2007) from settled starts brought them only to 3.7 (2.7 as
built), the GABAergic LNs' presynaptic inhibition rising with them, and even so moved their responses toward flies' at
every input but the weakest (Rmax 101-155 against 84-130, flies 144-170; strong responses keeping 0.45 of their peak at
500 ms against 0.35, flies 0.44; DL5 at 5 spikes/s of input 24 against 20, flies 44) and nearly doubled MBON11's response
to 3-octanol (57.7 spikes against 31.5, flies 118), with 4-methylcyclohexanol barely moved (0.53 against 0.51 over Badel et
al.'s glomeruli, flies 0.98). The build polishes the PNs' rest before it fits the presynaptic inhibition, which then
lowers it (polished to rung 4's 3 spikes/s, they settle at 2.4-2.7).
Model: odor_probe54.py's build with every uniglomerular PN's resting target at 4.6 spikes/s, in the group polish and in
both PN polishes (odor_probe43.py's change), and a last PN polish toward it (8 rounds) once the presynaptic inhibition is
fitted, before the rest check, so that the PNs rest at flies' rate with the inhibition in place. Rebuilt and cached as
odor_probe56. Measured with mb_calibration.py's mushroom body.
Measured as odor_probe54.py measures (the LNs' responses, Olsen et al.'s protocol, odor_probe36.measure, the equalization
with DoOR's input), on its seeds, and as odor_probe55.py measures with receptor_fills.RECOMMENDED's input (the
equalization and odor_probe36.measure), on its seeds; the PNs' settled resting rate.

    python experiments/odor_probe56.py         (writes experiments/odor_probe56.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import numpy as np

import al_cells
import brain_cache
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe27 as p27
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe42 as p42
import odor_probe44 as p44
import odor_probe54 as p54
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = p54.SEED, p54.EQUALIZATION_SEED
PN_REST_HZ, LAST_ROUNDS = 4.6, 8
WEIGHED_SEED, WEIGHED_EQUALIZATION_SEED = 690000, 695000   # odor_probe55.py's


def build() -> tuple:
    """odor_probe54.build with every uniglomerular PN's resting target at PN_REST_HZ: in the group polish, in both PN
    polishes, and in a last PN polish once the presynaptic inhibition is fitted (just before the rest check)."""
    plain, polish, check = p21.build, p27.pn_polish, p42.rest_check

    def resting_target(o):
        out = plain(o)
        o.s.target = o.s.target.copy()
        o.s.target[o.m["upn"]] = PN_REST_HZ
        out["upn_rest_target_hz"] = PN_REST_HZ
        return out

    def polished_check(o, rec, built, base):
        built["pn_rest_inhibited"] = polish(o, rec, base + 50, rounds=LAST_ROUNDS, goal=PN_REST_HZ)
        return check(o, rec, built, base)
    p21.build = resting_target
    p27.pn_polish = functools.partial(polish, goal=PN_REST_HZ)
    p42.rest_check = polished_check
    try:
        return p54.build()
    finally:
        p21.build, p27.pn_polish, p42.rest_check = plain, polish, check


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "pn_rest_target_hz": PN_REST_HZ}
    o, rec, built = brain_cache.load("odor_probe56", build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_olsen_protocol_check as olsen
    import receptor_fills
    out["settling"] = o.settling
    out["mb_calibration"] = mb_calibration.apply(o)
    p40.ln_mask = lambda types: al_cells.alln(o)
    upn = np.flatnonzero(o.m["upn"])
    try:
        with warm.tracking(o, rec) as held:
            entry = {"build": {x: built[x] for x in ("build", "resting_recalibration", "presynaptic", "rest_check", "settles",
                                                    "pn_rest_inhibited") if x in built}}
            rest = p10.resting(o, rec, SEED + 990)["hz"]
            entry["upn_rest_hz"] = {"mean": round(float(rest[upn].mean()), 2), "median": round(float(np.median(rest[upn])), 2)}
            print("PN rest", json.dumps(entry["upn_rest_hz"]), flush=True)
            entry["ln_response"] = p40.ln_measure(o, rec, SEED)
            lr = entry["ln_response"]
            print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
                  json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs",
                  json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:11]), flush=True)
            out["condition"] = entry
            OUT.write_text(json.dumps(out, indent=1))
            entry["olsen_protocol"] = olsen.measure(o, rec, protocols=("olsen",), show=False)
            t = entry["olsen_protocol"]["olsen"]
            print("fits", json.dumps({g: t[g]["cholinergic"]["fit"] for g in t}), "points", json.dumps({g: [t[g]["cholinergic"]["points"][x]["window_mean"]
                  for x in ("5", "10", "20", "40", "80", "160")] for g in t}),
                  "at 500 ms", json.dumps({g: t[g]["cholinergic"]["points"]["80"]["at_500ms_over_peak"] for g in t}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry.update(p36.measure(o, rec, built, SEED))
            print("KCs", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                  "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in entry["mbon11_input"].items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
            print("MCH/OCT (DoOR)", json.dumps(entry["equalization"]["mch_over_oct"]), flush=True)
            with receptor_fills.applied(recommended=True) as inputs:
                rec_entry = {"inputs": inputs, "equalization": eq.measure(o, rec, WEIGHED_EQUALIZATION_SEED)}
                print("MCH/OCT (weighed)", json.dumps(rec_entry["equalization"]["mch_over_oct"]), flush=True)
                OUT.write_text(json.dumps(out, indent=1))
                rec_entry.update(p36.measure(o, rec, built, WEIGHED_SEED))
                od = rec_entry["odors"]
                print("weighed: KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
                      "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
                      "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in rec_entry["mbon11_input"].items()}), flush=True)
            out["weighed_input"] = rec_entry
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = p44.PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
