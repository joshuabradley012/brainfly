"""Exploratory check, not pre-registered: with the projection neurons resting at flies' measured rate, settled, do they
give weak input flies' gain, and 4-methylcyclohexanol flies' breadth?

odor_weak_glomeruli_check.py: 4-methylcyclohexanol falls behind because the PNs give weak input about half of flies'
gain (its glomeruli with 12-20 Hz of receptor input answer at 0.43 of Olsen et al.'s transform alone, and the odor's
presynaptic division then silences those at 8 Hz or less); with flies' transform the same input gives 0.90 of
3-octanol's summed response over Badel et al.'s 37 glomeruli, against the model's 0.51. The model's PNs rest at about 2.4
spikes/s once settled (the build polished them toward rung 4's 3 in windows that hadn't settled; settle_check.py), where
flies' rest at 4.6 +- 4.2 (Turner et al. 2008, n = 37) and about 4.5 (Bhandawat et al. 2007), nearer threshold.
odor_probe43.py polished them to 4.6 on an older model without settled starts, and they fell back to about 1 spike/s
in the windows its odor runs started from, so flies' rate was never in place during an odor.
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body, every uniglomerular PN's bias polished
toward 4.6 spikes/s at rest (odor_probe27.pn_polish, 8 rounds, each from a settled start, which also sets the Kenyon
cells' rest again), the rest of the build as it was (the inhibition not refitted). As built is odor_probe54.py's and
odor_probe55.py's measures, on the same seeds.
Measured: odor_olsen_protocol_check.py's transform (Olsen et al.'s protocol, cholinergic PNs; odor_probe54.py's seeds),
and, with receptor_fills.RECOMMENDED's input, odor_equalization_check.py's measures and odor_probe36.measure's
(odor_probe55.py's seeds, 695000 and 690000); the PNs' settled resting rate.
Adopted into a rebuilt base, as stated before running, if it brings DL5's response to 5 and 10 spikes/s of receptor input
nearer flies' (44 at 5.1, 85 at 13.4) and 4-methylcyclohexanol's PN ratio over Badel's glomeruli nearer flies' 0.98,
without taking Rmax more than 10% past flies' (163-170) or the strong responses' time course away from flies' (0.44 of
peak at 500 ms).

Ran: the polish holds the PNs at 3.1-3.3 spikes/s in its own rounds and 3.69 at the end (2.72 before), short of
flies' 4.6: raising their biases raises the GABAergic LNs' drive and with it the presynaptic inhibition at rest. Even so,
the PNs' responses move toward flies' at every input but the weakest. Over the cholinergic PNs, Olsen et al.'s protocol,
Rmax for DL5, VM7d, DM4 and DM1 is 148, 155, 101 and 143 (as built 127, 130, 84 and 126; flies 167, 163, 170 and 144), and
sigma 15.5, 18.2, 17.0 and 13.3 (13.9, 16.8, 15.9 and 11.9; flies 11.8, 12.4, 16.3 and 44.8). Strong responses keep 0.45
of their peak at 500 ms in DL5 and VM7d (0.35 and 0.34; flies 0.44). But DL5 rises only 24 and 54 spikes/s at 5 and 10
spikes/s of input (20 and 51; flies 44 at 5.1, 85 at 13.4). With the weighed input, 4-methylcyclohexanol's PNs sum 0.53
of 3-octanol's over Badel et al.'s glomeruli (0.51; flies 0.98) and its Kenyon cells 0.14 (0.15), while MBON11 gains 57.7
spikes to 3-octanol (31.5; flies 118). By the rule stated, adopted: odor_probe56.py rebuilds the model with every
uniglomerular PN's resting target at 4.6, the inhibition fitted again around it.

    python experiments/odor_pn_rest_check.py      (writes experiments/odor_pn_rest_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe27 as p27
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe54 as p54
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 740000
PN_REST_HZ = 4.6                                   # Turner et al. 2008
EQUALIZATION_SEED, MEASURE_SEED = 695000, 690000   # odor_probe55.py's


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_olsen_protocol_check as olsen
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o)}
    upn = np.flatnonzero(o.m["upn"])
    with warm.tracking(o, rec) as held:
        before = p10.resting(o, rec, SEED + 900)["hz"]
        out["rest_before_hz"] = {"upn": round(float(before[upn].mean()), 2), "upn_median": round(float(np.median(before[upn])), 2)}
        out["polish"] = p27.pn_polish(o, rec, SEED, rounds=8, goal=PN_REST_HZ)["pn_polish"]
        after = p10.resting(o, rec, SEED + 901)["hz"]
        out["rest_after_hz"] = {"upn": round(float(after[upn].mean()), 2), "upn_median": round(float(np.median(after[upn])), 2)}
        print("rest", json.dumps({k: out[k] for k in ("rest_before_hz", "rest_after_hz")}), flush=True)
        transform = olsen.measure(o, rec, protocols=("olsen",), show=False)["olsen"]
        out["olsen_protocol"] = transform
        out["fits"] = {g: transform[g]["cholinergic"]["fit"] for g in transform}
        print("fits", json.dumps(out["fits"]), "points", json.dumps({g: [transform[g]["cholinergic"]["points"][x]["window_mean"]
              for x in ("5", "10", "20", "40", "80", "160")] for g in transform}),
              "at 500 ms", json.dumps({g: transform[g]["cholinergic"]["points"]["80"]["at_500ms_over_peak"] for g in transform}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
        with receptor_fills.applied(recommended=True) as inputs:
            out["inputs"] = inputs
            out["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
            print("MCH/OCT", json.dumps(out["equalization"]["mch_over_oct"]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            out.update(p36.measure(o, rec, built, MEASURE_SEED))
            od = out["odors"]
            print("KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
                  "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
                  "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in out["mbon11_input"].items()}), flush=True)
        out["measure_settles"] = held["settles"]
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
