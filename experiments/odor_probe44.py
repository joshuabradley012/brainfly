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

Ran: the corrections hold the model's resting state to its targets and change its odor responses only a little, mostly
weakening them. The build scales the 187,358 synapses onto all 420 ALLNs; with all 115 GABAergic ALLNs as inhibitors
the inhibition's fit gives k_A 0.0014 and k_B 0.0084 per spike/s (control 0.31-0.34 of baseline, GABA-B blocked
0.56-0.73; flies 0.27-0.37 and 0.52-0.81), and the receptor synapses rest at 0.95 of their strength. Settled 62 times in
the build and 9 in the measures, the PNs now rest at 2.8-2.95 spikes/s where the odor runs start (rung 4's target 3;
0.4-0.6 in odor_probe41.py's runs, 1.6-2.0 in odor_warm_check.py's) and the GABAergic LNs at 3.7. The LNs answer
2-heptanone with 18.7, 11.2, 8.2 and 6.5 spikes/s per cell in Nagel et al.'s bins (flies 22, 13, 8 and 6; root mean
square log ratio 0.12). 3-octanol's PNs peak at 96 spikes/s at 50-100 ms and fall to 0.31 of it at 0.40-0.45 s (flies
0.48) and 0.14 at 0.95 s; the transform's Rmax is 166-187 in DL5, VM7d and DM1 (flies 163-170) and 81 in DM4 (170), its
sigma 20-32 (12-16); 0.8-4.9% of Kenyon cells respond (flies 6 +- 5%), mean Jaccard 0.13, the alpha/beta cells firing
0.95-1.7 spikes per response (flies 2.2); 4-methylcyclohexanol reaches 0.27 as many Kenyon cells as 3-octanol (flies
0.73-0.92); 16-25% of PNs pass Turner's criterion over their higher rest (flies 59 +- 14%); MBON11 gains 8.5 spikes to
3-octanol (flies 118). Against odor_probe41.py's kw08_kept measured from settled states (odor_warm_check.py), 3-octanol's
PNs peak at 96 instead of 102 and accommodate a little more (0.31 against 0.37), and the Kenyon cells respond a little
less (3.1% to 3-octanol against 4.7%). This is the base model from here on.

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
