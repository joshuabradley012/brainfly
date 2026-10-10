"""Exploratory, not pre-registered: with the presynaptic inhibition building as fast as flies' does, rather than as Nagel et
al.'s alpha fit has it, do the projection neurons open strongly and then accommodate, and with the slow receptor
component sized to Olsen et al.'s transform, do the Kenyon cells respond as flies' do?

odor_probe36.py: the receptor synapse's slow component carries the PNs' sustained drive. At Nagel et al.'s odor-fitted
size (0.774 of the fast charge) 3-octanol's PNs climb to 105 spikes/s at 0.3-0.35 s and hold 0.78 of that at 0.95 s, and
the transform's Rmax is 184-355 (flies 144-170); at Kazama & Wilson's unitary size (0.086) they peak at 51 spikes/s at
50-100 ms and fall to 0.48 by 0.95 s, as flies' do, but the transform's Rmax falls to 62-124 and the Kenyon cells fall
silent. In both, the inhibition takes hold within 50-100 ms of the LNs' onset burst. In flies, under a step of
ChR2-driven LN firing, a PN's inhibition reaches half its size at about 50-70 ms and 90% at about 150-160 ms (Nagel et
al. 2015; research_notes/Rung 9 learning data/pn_ln_dynamics.md); the model's GABA-A part, two 25 ms stages (Nagel et
al.'s "alpha function with a time constant of about 25 ms"), reaches half at 42 ms and 90% at 97 ms. Two 38 ms stages
reach half at 64 ms and 90% at 148 ms.
Model: odor_probe36.py's (Inada's Kenyon cell classes, MBON11 keeping its synaptic current, its Kenyon cell synapses at
0.030 pC), the antennal lobe rebuilt and refitted for each condition exactly as odor_probe30.py builds it, Olsen &
Wilson 2008's EPSCs fitted again. Conditions:
  step              GABA-A as two 38 ms stages (the step response's half and 90% times); the slow component Nagel's
  step + slow 0.30  the same, with the slow component at 0.30 of the fast charge: a one-parameter fit, between the two
                    measurements, to Olsen et al.'s transform (Rmax 144-170, mean 161), interpolated linearly from
                    odor_probe36.py's two sizes (mean Rmax 288 at 0.774 and 104 at 0.086; 161 at 0.30)
Measured as odor_probe36.py measures. Seeds 240000 for the builds (odor_probe30.py's); 340000 + 1000 x condition for the
measures (with odor_probe36.py's offsets).

Ran: the inhibition's measured onset helps the projection neurons' onset only a little, and the intermediate slow
component gives neither flies' strong onset nor their accommodation. With GABA-A as two 38 ms stages (refitted: k_A
0.00042, k_B 0.0023 per spike/s above rest; Olsen & Wilson's EPSCs met as before), 3-octanol's PNs fire 76 spikes/s at
50-100 ms (71 before) and still climb to 107 at 0.3-0.35 s, 0.97 of that at 0.5 s and 0.78 at 0.95 s; the transform
(Rmax 193-336, sigma 31-41), the Kenyon cells (2.2-11.1% respond, 11 spikes per responding cell to 3-octanol) and MBON11
(123 and 35 spikes) are as before. With the slow component also at 0.30 (refitted: k_A 0.00038, k_B 0.0021), the PNs
peak at 67 spikes/s at 0.2-0.25 s and hold 0.93 of that at 0.5 s and 0.69 at 0.95 s; the transform's Rmax comes to
116-260 (mean 203, not the 161 the linear interpolation aimed at; sigma 33-50); only 0.3-2.1% of Kenyon cells respond
(37 responding cells per fly to 3-octanol, 8 spikes each) and MBON11 gains 10 and 2 spikes. The Kenyon cells need PNs
near 100 spikes/s, and flies' odor-driven PNs open at 100-200 and then fall; what the model's PNs lack is that strong
onset. The presynaptic inhibition still takes hold early because the LNs' onset burst is about three times flies' (57
spikes/s per LN at 50-100 ms, then 12-13 over 0.2-0.5 s, where flies' LNs fire about 22 over the first 50 ms, 13 at
50-100 ms and 6-8 later; Nagel et al. 2015, Fig. 5b).

    python experiments/odor_probe37.py         (writes experiments/odor_probe37.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe31 as p31
import odor_probe36 as p36

OUT = Path(__file__).with_suffix(".json")
SEED = 340000
STEP_TAU = 0.038                                   # s, each of GABA-A's two stages
CONDITIONS = {"step": None, "step + slow 0.30": 0.30}


def build(slow_charge) -> tuple:
    """odor_probe31.build with GABA-A's stages at STEP_TAU and, if given, the slow component at slow_charge."""
    taus, charge, ratio = p28.TAUS, p17.SLOW_CHARGE, p21.combined_peak_ratio
    p28.TAUS = (STEP_TAU, STEP_TAU) + tuple(taus[2:])
    if slow_charge is not None:
        p17.SLOW_CHARGE = slow_charge
        p21.combined_peak_ratio = functools.partial(ratio, charge=slow_charge)
    try:
        p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
        p21.masks = p29.pn_only_masks
        o, rec, built = p31.build()
    finally:
        p17.SLOW_CHARGE, p21.combined_peak_ratio = charge, ratio
    return o, rec, built, taus                       # p28.TAUS stays set while this model is measured


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "step_tau_s": STEP_TAU, "conditions": {}}
    for c, (name, slow) in enumerate(CONDITIONS.items()):
        o, rec, built, nagel_taus = build(slow)
        try:
            out["conditions"][name] = {"slow_over_fast_charge": slow if slow is not None else round(p17.SLOW_CHARGE, 3),
                                       "presynaptic": {k: built["presynaptic"][k] for k in ("k", "tau_s", "offset_hz")},
                                       **p36.measure(o, rec, built, SEED + 1000 * c)}
        finally:
            p28.TAUS = nagel_taus
        OUT.write_text(json.dumps(out, indent=1))
        print(name, "done", f"({time.perf_counter() - t0:.0f} s)", flush=True)
        del o, rec
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
