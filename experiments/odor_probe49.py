"""Exploratory, not pre-registered: the base model rebuilt with settled starts that have settled: how does it answer odors?

settle_check.py: warm.py's settled starts (6 s of spontaneous activity from a reset) leave the receptor synapses' slow
component at 0.80 of its strength where it settles near 0.37 (it recovers over 33 s), so the PNs fire 3.1 spikes/s where
every run begins and 2.05 once settled. odor_probe44.py's polishes met their 3 spikes/s target in that state, and every
run on its model has begun with the slow component at twice its resting strength, draining as the run went on. Started
at their resting depression, the synapses stay there and the antennal lobe settles within about 2 s.
Model: odor_probe44.py's build with every settle starting from the receptor synapses' resting depression and lasting 3 s
(warm.py's rested settling, which the model carries, so that every run on its cache settles the same way); cached as
odor_probe49. Measured with mb_calibration.py's mushroom body.
Measured: as odor_probe44.py (odor_probe40.ln_measure and odor_probe36.measure, now with the calibrated mushroom body, as
odor_probe48.py), and odor_equalization_check.py's responses to 3-octanol and 4-methylcyclohexanol. Seeds as
odor_probe44.py for the build (240000; 440000 for the settled states); 550000 for the measures, 560000 for the
equalization.

    python experiments/odor_probe49.py         (writes experiments/odor_probe49.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import al_cells
import brain_cache
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe44 as p44
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 550000, 560000
SETTLING = {"rested": True, "seconds": warm.RESTED_SETTLE_S}


def build() -> tuple:
    """odor_probe44.build with the model carrying SETTLING from its first settle on."""
    plain = warm.tracking

    def rested(o, rec, *args, **kw):
        o.settling = dict(SETTLING)
        return plain(o, rec, *args, **kw)
    warm.tracking = rested
    try:
        return p44.build()
    finally:
        warm.tracking = plain


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"]}
    o, rec, built = brain_cache.load("odor_probe49", build, p44.prepare)
    import mb_calibration                              # after the cache, so that its edits don't invalidate it
    import odor_equalization_check as eq
    out["settling"] = o.settling
    out["mb_calibration"] = mb_calibration.apply(o)
    p40.ln_mask = lambda types: al_cells.alln(o)
    try:
        with warm.tracking(o, rec) as held:
            entry = {"build": {x: built[x] for x in ("build", "presynaptic", "rest_check", "settles") if x in built},
                     "ln_response": p40.ln_measure(o, rec, SEED)}
            lr = entry["ln_response"]
            print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
                  json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs",
                  json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]), flush=True)
            out["condition"] = entry
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
