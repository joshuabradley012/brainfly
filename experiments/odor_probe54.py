"""Exploratory, not pre-registered: with the receptor synapse's slow component depressing as Nagel et al. measured it,
does the rebuilt model's transform saturate as flies' does, and does 4-methylcyclohexanol come closer to 3-octanol?

odor_drive_check.py: the PNs' slow synaptic current grows almost in proportion to the receptor input (the slow component
uses 0.73% of its strength per spike, Nagel et al. 2015's model fit), so their response keeps rising where flies'
saturates by about 50 spikes/s of input. odor_slow_depression_check.py (on odor_probe52.py's model, PN biases polished
again): with the slow component depressing as Nagel et al. measured it on curare-resistant EPSCs (0.91 of it left per
spike, recovering over 0.629 s; they judged the measurement to depress too fast, curare incompletely blocking the fast
component) sigma comes to 14.9, 17.3 and 16.8 in DL5, VM7d and DM4 (flies 11.8, 12.4, 16.3), the response to 160
spikes/s of input is 1.18 times that to 40 (as built 1.43; flies 1.06), Rmax 134-141 in DL5, VM7d and DM1 (flies
144-167); 4-methylcyclohexanol's PNs stay at 0.52 of 3-octanol's.
Model: odor_probe52.py's build with the receptor neurons' slow synapses depressing as measured (0.91, 0.629 s) from
odor_probe21.build on, so the polishes and the inhibition's fit are made with it. Cached as odor_probe54; measured with
mb_calibration.py's mushroom body.
Measured: as odor_probe52.py on its seeds, and odor_equalization_check.py's measures again with receptor_fills.py's
receptor and PN-inferred tiers (seed 570500).

    python experiments/odor_probe54.py         (writes experiments/odor_probe54.json)
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
import odor_probe52 as p52
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED, FILLED_SEED = p51.SEED, p51.EQUALIZATION_SEED, 570500
SLOW_DEPRESSION, SLOW_RECOVERY_S = 0.91, 0.629


def build() -> tuple:
    """odor_probe52.build with the receptor neurons' slow synapses depressing as measured from odor_probe21.build on."""
    plain = p21.build

    def measured_slow(o):
        out = plain(o)
        o.brain.set_type("ORN", slow_depression=SLOW_DEPRESSION, slow_recovery=SLOW_RECOVERY_S)
        out["slow_depression"] = {"per_spike": SLOW_DEPRESSION, "recovery_s": SLOW_RECOVERY_S}
        return out
    p21.build = measured_slow
    try:
        return p52.build()
    finally:
        p21.build = plain


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "pools": p51.POOLS,
           "upn_reset_mv": p52.PN_RESET_MV, "slow_depression": [SLOW_DEPRESSION, SLOW_RECOVERY_S]}
    o, rec, built = brain_cache.load("odor_probe54", build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_olsen_protocol_check as olsen
    import receptor_fills
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
            with receptor_fills.applied(pn_inferred=True):
                entry["equalization_filled"] = eq.measure(o, rec, FILLED_SEED)
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = p44.PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
