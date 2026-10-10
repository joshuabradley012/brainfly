"""Exploratory, not pre-registered: with the receptor synapse's slow component at Kazama & Wilson 2008's unitary size
instead of Nagel et al. 2015's odor-fitted one, do the projection neurons accommodate as flies' do, and do the Kenyon
cells fire fewer spikes?

odor_probe30.py's projection neurons rise through an odor instead of peaking early and falling: to 3-octanol they climb
from 71 spikes/s at 50-100 ms to 106 at 350-400 ms and hold 84 at 1 s, where flies' average PN peaks about 150 ms after
the valve opens, before its receptor neurons do, and falls to 0.48 of its peak by 500 ms (Bhandawat et al. 2007, 843
responses). In that model the receptor synapse's fast component depresses to under a tenth of its rested strength
during an odor, while its slow component, 0.774 of the fast component's rested charge and barely depressing (Nagel et
al.'s model parameters, fitted to disinhibited PN odor responses), comes to carry most of the late drive. Measured on
unitary connections, that slow component "was relatively small, on average only about 1 % as large as the fast component
at the time when the fast component peaks", which Kazama & Wilson read as lateral input (research_notes/Rung 9 learning
data/orn_pn_depression.md). With Nagel et al.'s measured decay times (80 and 9.3 ms), 1% of the amplitude is about 0.086
of the fast component's charge.
Model: odor_probe30.py's antennal lobe (odor_probe31.build on its seeds), with Inada et al.'s Kenyon cell class offsets
(odor_probe33.py), MBON11 keeping its synaptic current (odor_probe35.py) and its Kenyon cell synapses at 0.030 pC each.
Conditions:
  Nagel   the slow component at 0.774 of the fast charge (the current model; brain_cache.py's copy)
  KW08    the slow component at 0.086 of the fast charge (its depression unchanged), the unitary EPSP's correction for
          it recomputed, and the antennal lobe rebuilt and refitted exactly as odor_probe30.py builds it (resting
          calibration, PN polish, presynaptic inhibition fitted again to Olsen & Wilson 2008's EPSCs, second polish)
Measured for each, as odor_probe30.py measures (PN, LN and receptor time courses in 50 ms bins, the transform, the odor
measures), with MBON11's input and evoked spikes per odor (odor_probe33.py's measure) and, for 3-octanol and
4-methylcyclohexanol, the responding Kenyon cells' spikes over 1.4 s (odor_kc_timing.py's measure, 1 seed). Seeds
240000 for the builds (odor_probe30.py's); 330000 + 1000 x condition for the measures (+ odor_probe30.py's offsets;
+ 900 + round for the Kenyon cells' rest; + 200 + odor for MBON11; + 500 + odor for the timing).

Ran: the slow component's size sets whether the projection neurons accommodate, but neither measurement gives flies'
strong onset and accommodation together. With Nagel et al.'s (0.774), 3-octanol's PNs climb to 105 spikes/s at 0.3-0.35
s and are at 0.97 of that at 0.5 s and 0.78 at 0.95 s (43 in the first 100 ms); the transform's Rmax is 184-355 (flies
144-170), sigma 28-38; 2.1-10.1% of Kenyon cells respond, those answering 3-octanol firing 10.8 spikes over 1.4 s, and
MBON11 gains 112 spikes from 429 pC per cell. With Kazama & Wilson's (0.086; presynaptic inhibition refitted to k_A
0.00042 and k_B 0.0021 per spike/s above rest, Olsen & Wilson's EPSCs met as well: control 0.30-0.34, GABA-B blocked
0.53-0.76), the PNs peak early, at 51 spikes/s at 50-100 ms, and fall to 0.61 of that by 0.5 s and 0.48 by 0.95 s
(flies: a peak about 75 ms after their receptors start, 0.48 by 500 ms); but at half the rate the transform's Rmax falls
to 62-124 (sigma 22-34), and the Kenyon cells nearly fall silent (0.1-0.4% respond; 5 responding cells per fly to
3-octanol; MBON11 gains about 1 spike). So the slow component carries the PNs' sustained drive, and its size, between
the two measurements' 0.086 and 0.774, trades accommodation against strength. What holds the onset down in both is the
presynaptic inhibition, which here takes hold within 50-100 ms of the LNs' onset burst (the synapses at 0.25-0.28 of
their strength), where flies' builds over 50-150 ms (half at 50-70 ms and 90% at 150-160 ms of a step of LN firing;
Nagel et al. 2015; research_notes/Rung 9 learning data/pn_ln_dynamics.md).

    python experiments/odor_probe36.py         (writes experiments/odor_probe36.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_kc_timing as kt
import odor_probe10 as p10
import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe31 as p31
import odor_probe33 as p33
import odor_probe7 as p7
import odor_probe8 as p8
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 330000
CHARGE_PC = 0.030
KW08_CHARGE = 0.01 * 80.0 / 9.3                    # 1% of the fast amplitude at its peak, Nagel et al.'s decay times
TIMING_ODORS = ("3-octanol", "4-methylcyclohexanol")


def kw08_build() -> tuple:
    """odor_probe31.build with the slow component at KW08_CHARGE of the fast charge."""
    nagel_charge, nagel_ratio = p17.SLOW_CHARGE, p21.combined_peak_ratio
    p17.SLOW_CHARGE = KW08_CHARGE
    p21.combined_peak_ratio = functools.partial(nagel_ratio, charge=KW08_CHARGE)
    try:
        p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
        p21.masks = p29.pn_only_masks
        return p31.build()
    finally:
        p17.SLOW_CHARGE, p21.combined_peak_ratio = nagel_charge, nagel_ratio


def measure(o, rec, built: dict, base: int) -> dict:
    b, types, m = o.brain, o.types, o.m
    kc_rest = p33.set_rest(o, rec, p8.class_gaps(o, p8.OFFSETS["Inada"]), base + 900)
    b.set_type("MBON11", keep_current=1.0)
    mb = np.flatnonzero(types == "MBON11")
    gain = p31.mbon_gain(o, rec, mb)
    w_syn = p31.GAIN_HZ_PER_PA * CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(m["kc"][pre] & np.isin(b.idx, mb))
    w = b.weights.copy()
    w[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w, None
    syn = np.zeros((b.n, len(mb)))
    np.add.at(syn, (pre[onto], np.searchsorted(mb, b.idx[onto])), b._counts[onto])
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    pres = built["presynaptic"]
    k, offset = np.asarray(pres["k"]), pres["offset_hz"]
    inhibitors = p21.masks(o)["inhibitors"]
    entry = {"presynaptic_fit": pres["calibration"][-1], "kc_rest": kc_rest, "mbon11_gain": gain,
             "weight_per_synapse_mv": round(w_syn, 4), "course": {}}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = p30.course(o, rec, odor, base + 700 + j, pns, inhibitors, k, offset)
        print("  ", odor, json.dumps({x: entry["course"][odor][x][:12] for x in ("pn_hz", "gain")}), flush=True)
    entry["transform"] = p24.transform(o, rec, base)
    entry.update(p24.odor_measures(o, rec, base, gloms, pn_of))
    entry["mbon11_input"] = p33.mbon11_input(o, rec, base, mb, syn)
    print("   MBON11", json.dumps(entry["mbon11_input"]), flush=True)
    kc = np.flatnonzero(m["kc"])
    kc_syn = syn[kc]
    entry["kc_timing"] = {odor: kt.measures(kt.record(o, rec, odor, base + 500 + j, kc), kc_syn) for j, odor in enumerate(TIMING_ODORS)}
    print("   KC timing", json.dumps({od: {x: r[x] for x in ("responding_cells_per_fly", "spikes_per_responding_cell")}
                                     for od, r in entry["kc_timing"].items()}), flush=True)
    return entry


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": {"pn_peak_s_after_valve": "about 0.14-0.15", "pn_at_500ms_of_peak": 0.48,
                                          "orn_at_500ms_of_peak": 0.73, "kc_spikes_per_response_alpha_beta": "2.2 +- 1.2",
                                          "mbon11_spikes": {"3-octanol": 118, "4-methylcyclohexanol": 110}},
           "kw08_slow_over_fast_charge": round(KW08_CHARGE, 4), "conditions": {}}
    o, rec, built = brain_cache.probe30()
    out["conditions"]["Nagel"] = measure(o, rec, built, SEED)
    OUT.write_text(json.dumps(out, indent=1))
    print("Nagel done", f"({time.perf_counter() - t0:.0f} s)", flush=True)
    del o, rec
    o, rec, built = kw08_build()
    out["kw08_build"] = {x: built[x] for x in ("build", "presynaptic") if x in built}
    out["conditions"]["KW08"] = measure(o, rec, built, SEED + 1000)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("KW08 done", f"({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
