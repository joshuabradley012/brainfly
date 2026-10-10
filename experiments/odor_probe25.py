"""Exploratory, not pre-registered: odor_probe24.py's control. With the receptor synapses at their rested, uninhibited
strength divided by the presynaptic inhibition in vivo, but the receptor neurons still silent at rest, how much of
odor_probe24.py's change comes from the weights alone?

Model: odor_probe22.py's antennal lobe with the weights left as calibrated instead of multiplied by the resting divisor
(odor_probe24.apply: at rest the inhibited synapses carry 1 / (resting divisor) of their calibrated strength), the
receptor neurons' depletion following the gain, and k_A and k_B fitted again to Olsen & Wilson 2008's EPSCs; no
spontaneous receptor firing, so no resting recalibration beyond odor_probe21.py's build. Measured as odor_probe21.py
measures. Seeds 190000 (otherwise as odor_probe21.py's, with its offsets).

Ran: too weak in odors, but it brackets flies' transform from the other side. With the synapses no longer multiplied by
the resting divisor, the LNs respond less (their traces 2.9-5.7 times their resting rate, against 3.6-7.3 in
odor_probe22.py), so the fit needs far more inhibition: k_A = 0.00098, k_B = 0.063 per spike/s, a resting divisor of 14.5
(fits: control 0.32-0.33, GABA-B blocked 0.56-0.75). At rest the synapses then carry 1/14.5 of their calibrated
strength. Driven alone, DL5, VM7d and DM1 saturate near flies' rate (Rmax 160, 177 and 157 spikes/s; Olsen 167, 163,
144; DM4 86, against 170), and DM1's sigma matches (43, against 44.8, which Olsen et al. attribute to tonic GABA), but
the others' sigma is three times flies' (DL5 42, VM7d 37, DM4 49; Olsen 12, 12, 16): weak input is suppressed. Lateral
input nearly abolishes responses (to 0-0.48). In odors the driven PNs fire only 67-85 Hz, flat (flies 100-200 at
onset), and only 25-42% of PNs respond by Turner's criterion (59 +- 14%); 0.1-0.4% of Kenyon cells respond (flies 6 +-
5%) and the MBONs don't move. So odor_probe21.py to odor_probe23.py (synapses times the resting divisor) give flies'
sigma with twice their Rmax, and this gives their Rmax with three times their sigma: the tonic inhibition between the
two would match both, but inhibition linear in LN rate can't give flies' threefold relative suppression with a smaller
tonic divisor (odor_probe24.py). Flies also differ by glomerulus here (Olsen et al.: GABA antagonists raise DM1's gain but
not VM7's; Hong & Wilson 2015: sensitivity to LN activation varies about 25-fold across glomeruli), which one global
strength can't give.

    python experiments/odor_probe25.py         (writes experiments/odor_probe25.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 190000


def calibrate(o: p7.Olfaction, mk: dict, base_w, base_sw) -> dict:
    a_rest = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):
        p24.apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = p21.fit(p22.lateral_traces(o, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    d_rest, k = p24.apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    taus, _ = p22.pairs()
    return {"k": k.tolist(), "k_a": k_a, "k_b": k_b, "tau_s": list(taus), "inhibitors_rest_hz": round(a_rest, 1),
            "resting_divisor": round(d_rest, 3), "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = SEED
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    entry = {"presynaptic": calibrate(o, mk, b.weights.copy(), b.slow_weights.copy())}
    k = np.asarray(entry["presynaptic"]["k"])                   # course's gain here: relative to the uninhibited synapse
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = p21.course(o, odor, base + 700 + j, pns, mk["inhibitors"], k, 1.0)
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
