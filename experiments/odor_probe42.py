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

Ran: with the inhibition fitted after the polishes the receptor synapses rest at full strength (0.99 at both scales; the
inhibitors resting at 78 and 305 spikes/s summed, below offsets of 122 and 341, so none was raised), and the LNs at 0.17
answer odors as flies' do, but the projection neurons still don't accommodate. At s = 1 the model is odor_probe30.py's
with the bug undone, and its odor responses barely change: k_A 0.00042 and k_B 0.0022 (0.00046 and 0.0023 before);
3-octanol's PNs fire 74 spikes/s at 50-100 ms, peak at 106 at 0.3 s and hold 0.95 of it at 0.5 s and 0.79 at 0.95 s
(71, 105, 0.97 and 0.78 before); the transform's Rmax is 214-361 and sigma 28-42 (184-355 and 28-38); 2.6-10.5% of
Kenyon cells respond (2.1-10.1%), mean Jaccard 0.17, alpha/beta cells firing 4.6-6.4 spikes per response; MBON11 gains
119 spikes to 3-octanol from 459 pC (112 and 429). Its GABAergic LNs rest at 1.9 spikes/s and fire 64, 43, 23 and 12 in
Nagel et al.'s bins (root mean square log ratio 1.02). At s = 0.17, with the GABAergic LNs' target at 4 spikes/s, they
rest at 3.8 and fire 23, 16, 10 and 7.5 (flies 22, 13, 8 and 6; 0.20), 3-octanol alike, a little weaker. The
inhibition's strengths triple (k_A 0.0012, k_B 0.0072), and 3-octanol's PNs open harder (90 spikes/s at 50-100 ms, the
synapses at 0.39 of their strength there against 0.32 at s = 1) but still climb, to 120 at 0.3 s, holding 0.93 of it at
0.5 s and 0.71 at 0.95 s; the strongly driven ones (glomeruli driven over 0.2) go from 156 at 50-100 ms to 202 at
0.3-0.35 s. 4-methylcyclohexanol's PNs peak at 0.61 of 3-octanol's (0.55 at s = 1; flies 0.85-0.98). The transform's
sigma falls a little (26-37; Rmax 210-358) and PN breadth rises (28-39% respond by Turner's criterion, 17-36% at s = 1;
flies 59 +- 14%), but with stronger PNs and nothing to make them accommodate the Kenyon cells respond more densely
(3.6-13.4%, mean Jaccard 0.18) with more spikes (alpha/beta 4.8-7.3 per response), and MBON11 gains 133 spikes to
3-octanol from 561 pC and 53 to 4-methylcyclohexanol from 162.

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
