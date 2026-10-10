"""Exploratory, not pre-registered: if the projection neurons can't fire faster than flies' do for long, does the
antennal lobe saturate at flies' rate?

odor_probe21.py and odor_probe22.py: with measured presynaptic inhibition, one glomerulus driven alone still saturates
at 300-331 spikes/s over 0.5 s in DL5, VM7d and DM1 (Olsen et al. 2010: Rmax 144-170), and one glomerulus recruits too
few local neurons for inhibition to matter (odor_presynaptic_sweep.py). Olsen et al. attribute the saturation to the
synapses' depression and "the relative refractory period of PNs" (Kazama & Wilson 2008), and the receptor synapse's slow
component, fitted by Nagel et al. 2015 to disinhibited PN odor responses, barely depresses. The model's PNs have only a
2.2 ms absolute refractory period, so they can fire about 450 spikes/s. Flies' PNs "can fire constantly over a 500-ms
period of somatic current injection" at about 164 spikes/s at most (Kazama & Wilson 2008 Fig. 9A, n = 8, read off the
figure; research_notes/Rung 9 learning data/pn_ln_dynamics.md), nearly Olsen et al.'s Rmax; no refractory period,
afterhyperpolarization or f-I curve beyond that has been published for them.
Model: odor_probe22.py's (presynaptic inhibition with GABA-B rising over 40 ms, k_A and k_B fitted again to Olsen & Wilson
2008's EPSCs) with every uniglomerular PN's absolute refractory period set to 1/164 s (6.1 ms), so that no PN can fire
faster than 164 spikes/s. This also caps brief rates: flies' strongest odor responses reach about 300 spikes/s in a 50 ms
bin (Bhandawat et al. 2007: 12 of 126 odor-glomerulus pairs at 250 or more, median peak about 108), which the cap clips;
the alternative, a use-dependent ceiling acting over tens of ms, has no measurement to set it.
Measured as odor_probe21.py measures. Seeds 170000 (otherwise as odor_probe21.py's, with its offsets).

Ran: the cap overcorrects and bends the transform, but it shows what the Kenyon cells need. A 6.1 ms refractory period
stretches every interspike interval, not only the fastest, so it lowers the whole curve: Rmax 88, 127, 133 and 127 for
DM4, DL5, VM7d and DM1 (Olsen 170, 167, 163, 144) and sigma 8, 5, 5 and 6 (16, 12, 12, 45), weak input still twice too
effective (DL5 at 5 Hz: 67 spikes/s, Olsen's fit about 36), lateral input dividing to 0.58-0.79. The fit gives k_A =
0.00077 and k_B = 0.0119 (resting divisor 3.4). In odors the driven PNs fire 107-112 Hz in the first 100 ms and 110-120
over 1 s, still without accommodating (3-octanol: 89 Hz in the first 50 ms, 97 by 450 ms), and stay as broad as flies'
(37-59% by Turner's criterion). With PNs at that rate the Kenyon cells come into flies' range: 0.9-7.5% respond (flies
6 +- 5%), mean Jaccard 0.24 (flies' dissimilar odors share about 0.22), 12 cells answer all six odors, and responding
alpha/beta cells fire about 4 spikes (flies 2.2). But the classes are wrong the other way now: alpha'/beta' cells
almost never respond (0-0.4%; flies about 9-14%), alpha/beta 0.8-12% and gamma 1.3-6% (flies about 3-8 and 2), and
4-methylcyclohexanol's few responders (0.9%) are still mostly 3-octanol's (78%). MBON11 gains 0.3-6.4 spikes and
MBON-alpha2sc 0.1-12 (flies 110-118 and about 71-85). The resting brain is unchanged (0.95 Hz). Weak input's excess,
which a cap can't touch, points at the synapses' resting state: the model's receptor neurons are silent at rest, so
every odor meets fully rested synapses (odor_probe24.py).

    python experiments/odor_probe23.py         (writes experiments/odor_probe23.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 170000
PN_MAX_HZ = 164.0                                # Kazama & Wilson 2008, Fig. 9A


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = SEED                       # build's, calibration's and the measures' seeds follow this probe's
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    b.set_type("uPN", refractory=1.0 / PN_MAX_HZ)
    out["pn_refractory_s"] = round(1.0 / PN_MAX_HZ, 5)
    mk = p21.masks(o)
    entry = {"presynaptic": p22.calibrate(o, mk)}
    k, d_rest = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["resting_divisor"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = p21.course(o, odor, base + 700 + j, pns, mk["inhibitors"], k, d_rest)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = p17.transform(o, base)
    entry.update(p17.odor_measures(o, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
