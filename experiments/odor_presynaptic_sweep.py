"""Exploratory sensitivity check, not a calibration and not pre-registered: in odor_probe21.py's base antennal lobe, how
much does GABA-A-like presynaptic inhibition of the receptor terminals change one glomerulus's transform, its division by
the others, and an odor's time course, as its strength grows?

Inhibition as odor_probe21.py's (every receptor-neuron output, and their slow synapses onto uniglomerular PNs, divided by
1 + k A, A the 90 GABAergic antennal lobe LNs' summed rate through a difference of 40 and 15 ms exponentials), but
starting from zero and without the resting divisor, at k = 0, 0.00036, 0.00095, 0.0021 and 0.0057 per spike/s (about
0.8, 0.6, 0.4 and 0.2 of the synapses left at the LNs' sustained odor rate). Measured: DL5's PNs driven alone at 5-160 Hz
and at 20 Hz with every other glomerulus at 20 Hz (odor_probe16.py's protocol), and 3-octanol's driven PNs, the LNs and
the synapses' strength in 50 ms bins. Seeds 150000-150020.

Ran: inhibition this strong divides one glomerulus's response by the others' input (DL5 at 20 Hz with lateral input:
1.02, 0.73, 0.56, 0.39 and 0.22 of its response alone), but barely changes the glomerulus alone (at 160 Hz: 351, 339,
325, 306 and 275 spikes/s), since one glomerulus recruits few LNs. In 3-octanol the synapses are weakest at onset
(0.42-0.05 of full strength at 50 ms, after the LNs' burst) and recover over 0.5 s (0.80-0.24), so the PNs rise through
the odor at every strength (to 0.95-1.0 of their peak by 0.5 s, against flies' about 0.5).

    python experiments/odor_presynaptic_sweep.py       (writes experiments/odor_presynaptic_sweep.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe16 as p16
import odor_probe21 as p21
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
STRENGTHS = (0.0, 0.00036, 0.00095, 0.0021, 0.0057)


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    b, m, types = o.brain, o.m, o.types
    out = {"question": __doc__, "build": p21.build(o), "strengths": {}}
    mk = p21.masks(o)
    gloms = sorted({t[4:] for t in types[m["orn"]]})
    orns = {g: b.cells([f"ORN_{g}"]) for g in gloms}
    pns = np.flatnonzero(m["upn"] & np.char.startswith(types, "DL5_"))
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    oct_pns = np.concatenate([pn_of[g] for g in odors.glomeruli("3-octanol") if g in pn_of and len(pn_of[g])])
    background = [(orns[h], p16.BACKGROUND_HZ) for h in gloms if h != "DL5" and len(orns[h])]
    c = p21.TAU_A / (p21.TAU_A - p21.TAU_A_RISE)
    for ka in STRENGTHS:
        k = np.array([c * ka, -(c - 1.0) * ka])
        if ka:
            b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=(p21.TAU_A, p21.TAU_A_RISE), k=k)
        else:
            b.set_presynaptic()
        alone = {f"{hz:g}": p16.drive_response(o, [(orns["DL5"], hz)], pns, 150000 + i)["whole"] for i, hz in enumerate(p16.RATES)}
        lateral = p16.drive_response(o, [(orns["DL5"], 20.0)] + background, pns, 150010)["whole"]
        course = p21.course(o, "3-octanol", 150020, oct_pns, mk["inhibitors"], k if ka else np.zeros(0))
        late, peak = float(np.mean(course["pn_hz"][8:10])), max(course["pn_hz"])
        out["strengths"][f"{ka:g}"] = {"dl5_alone": alone, "dl5_lateral_20hz_over_alone": round(lateral / alone["20"], 3),
                                      "octanol": course, "octanol_pn_at_0.5s_over_peak": round(late / peak, 3)}
        print(ka, json.dumps({"alone": alone, "lateral": out["strengths"][f"{ka:g}"]["dl5_lateral_20hz_over_alone"],
                              "pn": course["pn_hz"][:10], "gain": course["gain"][:10]}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
