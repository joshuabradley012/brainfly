"""Exploratory, not pre-registered: the antennal lobe rebuilt with its local neurons as MaleCNS classes them and with
every run starting from a settled state: how does it answer odors?

odor_probe41.py's kw08_kept is the closest model yet (the receptor synapse's slow component at Kazama & Wilson's unitary
size, the uniglomerular PNs keeping their synaptic current, every synapse onto the LNs at 0.17 of its strength, the
GABAergic LNs resting at flies' 4 spikes/s, the inhibition fitted after the resting polishes). Two corrections remain:
- al_cells.py: the LNs were picked by a pattern on type names, which misses 101 of the 420 neurons MaleCNS classes
  ALLN and takes in 2 it doesn't; 25 of the 115 GABAergic LNs were missing from the presynaptic inhibition's
  inhibitors (and from the LNs' scaling and resting target), and 17 cholinergic LNs kept their chemical synapses onto
  PNs.
- odor_warm_check.py: every run starts in a transient after the reset (the LNs above their steady rate, the PNs below
  theirs). From a settled state the LNs match Nagel et al.'s PSTH almost exactly and the PNs rest at 1.6-2.0 spikes/s
  instead of 0.4-0.6, the odor responses barely changing; the build's polishes were measured in that transient too.
Model: odor_probe41.py's kw08_kept with every LN role (the inhibitors, the cholinergic LN-to-PN synapses removed, the
synapses scaled by 0.17, the GABAergic LNs' resting target) given to MaleCNS's ALLNs (al_cells.py), and every run from
the resting recalibration on, in the build and in the measures, starting from a settled state (warm.tracking: 6 s of
spontaneous activity, settled again whenever biases, weights, types or the inhibition have changed). Cached as
odor_probe44.
Measured as odor_probe42.py measures (the LN measures over the GABAergic ALLNs). Seeds 240000 for the build (as
odor_probe42.py offsets them; 440000 for the settled states); 450000 for the measures (odor_probe40.py's offsets).

    python experiments/odor_probe44.py         (writes experiments/odor_probe44.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import al_cells
import brain_cache
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe42 as p42
import odor_probe7 as p7
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 450000
SCALE = 0.17
PLAIN_LN_EDGES, PLAIN_LN_MASK = p14.cholinergic_ln_edges, p40.ln_mask


def prepare() -> None:
    """odor_probe40.prepare with the LN roles given to MaleCNS's ALLNs."""
    p40.prepare()
    p21.masks = functools.partial(al_cells.masks, plain=p29.pn_only_masks)
    p14.cholinergic_ln_edges = al_cells.cholinergic_ln_edges


def build() -> tuple:
    """odor_probe42.built_inhibition_last's steps with odor_probe41.py's kw08_kept settings, the ALLNs as the LNs, and
    settled starts from the resting recalibration on."""
    prepare()
    plain, charge, ratio = p21.build, p17.SLOW_CHARGE, p21.combined_peak_ratio

    def configured(o):
        out = plain(o)
        b = o.brain
        b.set_type("uPN", keep_current=1.0)
        ln = al_cells.alln(o)
        onto = ln[b.idx]
        w = b.weights.copy()
        w[onto] *= SCALE
        b.weights, b._external_matrix = w, None
        gaba = p21.masks(o)["inhibitors"]
        o.s.target = o.s.target.copy()
        o.s.target[gaba] = p40.GABA_LN_REST_HZ
        out["ln_inputs"] = {"scale": SCALE, "lns": int(ln.sum()), "gaba_lns": int(len(gaba)), "edges": int(onto.sum()),
                            "gaba_ln_rest_target_hz": p40.GABA_LN_REST_HZ, "upn_keep_current": True,
                            "slow_over_fast_charge": round(p36.KW08_CHARGE, 4)}
        return out
    p21.build = configured
    p17.SLOW_CHARGE = p36.KW08_CHARGE
    p21.combined_peak_ratio = functools.partial(ratio, charge=p36.KW08_CHARGE)
    try:
        o = p7.Olfaction()
        b = o.brain
        out = {"build": p21.build(o)}
    finally:
        p21.build, p17.SLOW_CHARGE, p21.combined_peak_ratio = plain, charge, ratio
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], p30.SEED + 930)
    p28.apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)
    with warm.tracking(o, rec) as held:
        p10.POLISH, schedule = p27.FIRST_POLISH, p10.POLISH
        try:
            out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0, p30.SEED + 600)
        finally:
            p10.POLISH = schedule
        out["pn_rest"] = p27.pn_polish(o, rec, p30.SEED + 700)
        out["second_polish"] = p24.polish(o, rec, p30.SEED + 640, p27.SECOND_POLISH)
        out["pn_rest_after"] = p27.pn_polish(o, rec, p30.SEED + 800, rounds=6)
        rec.kinetics = "fast"
        out["presynaptic"] = p30.calibrate(o, rec, mk, base_w, base_sw)
        out["rest_check"] = p42.rest_check(o, rec, out, p30.SEED + 1100)
        out["settles"] = held["settles"]
    return o, rec, out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"]}
    o, rec, built = brain_cache.load("odor_probe44", build, prepare)
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
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
