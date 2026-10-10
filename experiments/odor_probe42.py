"""Exploratory, not pre-registered: with the presynaptic inhibition fitted last, so that it acts only above the finished
model's resting rate as odor_probe27.py meant, how does the antennal lobe answer odors, with its local neurons as
built and scaled to flies' onset?

odor_offset_check.py: the build (odor_probe31.build, odor_probe30.py's sequence) measures the GABAergic LNs' resting
rate for the inhibition's offset right after the PN polish, which has just lowered the PNs from about 43 to 13
spikes/s and with them the LNs (to about 0.5 spikes/s each in odor_probe30.py's build), and then polishes the rest
again, which brings the LNs back to their targets. So the inhibition acts at rest: in odor_probe30.py's model the
inhibitors' summed resting rate is 200 spikes/s against an offset of 48.6 and the receptor-to-PN synapses rest at 0.67
of their strength; in odor_probe40.py's at s = 0.17, 361 against 266 and 0.54. Raising the offset alone doesn't undo
it, because the freed PNs drive the LNs harder (odor_probe30.py's model with the offset at 203: the PNs resting at 3.1
spikes/s instead of 2.0, the inhibitors at 310, the synapses at 0.73).
Model: odor_probe40.py's build (odor_probe30.py's sequence, Inada et al.'s Kenyon cell classes and MBON11 as in
odor_probe36.py's measures) with the second resting polish and PN polish moved before the inhibition is fitted, so
that its offset is the resting rate of LNs already at their targets, and nothing moved after it; then the inhibitors'
resting traces (4 s to settle) checked against the offset, which is raised to them if they're above it (k unchanged),
before the model is cached.
Conditions: every synapse onto the antennal lobe's LNs at s = 1 with rung 4's resting targets (the current model,
corrected), and at s = 0.17 with the GABAergic LNs resting at flies' 4 spikes/s (odor_probe40.py's best). Each built
model is cached (odor_probe42_s1, odor_probe42_s0.17).
Measured for each: everything odor_probe40.py measures. Seeds 240000 for the builds (odor_probe30.py's, + 1100 + seed for
the resting check); 420000 + 1000 x condition for the measures (odor_probe40.py's offsets).

    python experiments/odor_probe42.py         (writes experiments/odor_probe42.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_offset_check as oc
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe30 as p30
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 420000
SCALES = (1.0, 0.17)


def built_inhibition_last(scale: float):
    """A no-argument build for brain_cache: odor_probe31.build's steps with the second polishes before the inhibition's
    fit, the LNs' inputs and resting target set as odor_probe40.builder sets them when scale < 1."""
    def build() -> tuple:
        plain = p21.build

        def scaled(o):
            out = plain(o)
            if scale < 1.0:
                b = o.brain
                onto = p40.ln_mask(o.types)[b.idx]
                w = b.weights.copy()
                w[onto] *= scale
                b.weights, b._external_matrix = w, None
                gaba = p21.masks(o)["inhibitors"]
                o.s.target = o.s.target.copy()
                o.s.target[gaba] = p40.GABA_LN_REST_HZ
                out["ln_inputs"] = {"scale": scale, "edges": int(onto.sum()), "gaba_ln_rest_target_hz": p40.GABA_LN_REST_HZ}
            return out
        p40.prepare()
        p21.build = scaled
        try:
            o = p7.Olfaction()
            b = o.brain
            out = {"build": p21.build(o)}
        finally:
            p21.build = plain
        mk = p21.masks(o)
        rec = p10.Receptors(o)
        rec.spontaneous, rec.kinetics = True, False
        base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
        a0 = p21.resting_inhibitors(o, mk["inhibitors"], p30.SEED + 930)
        p28.apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)
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
        out["rest_check"] = rest_check(o, rec, out, p30.SEED + 1100)
        return o, rec, out
    return build


def rest_check(o, rec, built: dict, base: int) -> dict:
    """odor_offset_check.py's resting measure; if the GABA-A trace rests above the offset, the offset (and the traces'
    start) is raised to it, k unchanged, and measured again."""
    b = o.brain
    mk = p21.masks(o)
    pres = built["presynaptic"]
    k, offset = np.asarray(pres["k"], np.float64), float(pres["offset_hz"])
    out = {"as fitted": oc.rest_summary(o, rec, base, mk["inhibitors"], k, offset)}
    print("  rest as fitted", json.dumps(out["as fitted"]), flush=True)
    raised = out["as fitted"]["gaba_a_trace_hz"]
    if raised > offset:
        p28.apply(o, mk, b.weights.copy(), b.slow_weights.copy(), float(k[1]), float(k[3]), raised)
        pres["offset_hz"] = round(raised, 1)
        out["raised to"] = oc.rest_summary(o, rec, base, mk["inhibitors"], k, raised)
        print("  rest, offset raised", json.dumps(out["raised to"]), flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "conditions": {}}
    for c, s in enumerate(SCALES):
        o, rec, built = brain_cache.load(f"odor_probe42_s{s:g}", built_inhibition_last(s), p40.prepare)
        base = SEED + 1000 * c
        entry = {"scale": s, "build": {x: built[x] for x in ("build", "presynaptic", "rest_check") if x in built}}
        entry["ln_response"] = p40.ln_measure(o, rec, base)
        lr = entry["ln_response"]
        print(f"s {s} LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
              json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]),
              flush=True)
        out["conditions"][f"{s:g}"] = entry
        OUT.write_text(json.dumps(out, indent=1))
        entry.update(p36.measure(o, rec, built, base))
        OUT.write_text(json.dumps(out, indent=1))
        print(f"s {s} done ({time.perf_counter() - t0:.0f} s)", flush=True)
        del o, rec
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
