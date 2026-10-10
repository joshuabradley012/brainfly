"""Exploratory, not pre-registered: with the slow component of flies' receptor synapses depressing as measured, does
the antennal lobe transform receptor input as flies' does?

odor_probe17.py: adding Nagel, Hong & Wilson 2015's slow receptor-synapse component (0.774 times the fast component's
charge, tau 80 ms) gives the PNs Olsen et al. 2010's transform shape (sigma 10-19 against 12-16) but twice their gain
(Rmax 223-352 against 144-170), and taken as undepressed it drives PNs to 330-350 Hz through an odor. Nagel et al.'s
slow component does deplete: by r = 0.0073 per spike, recovering over tau_A = 33.2 s, against the fast component's 0.23
and 1.0 s. That is small per spike, but at 100-200 Hz it halves the component within half a second.
Condition: odor_probe17.py's, except that the slow receptor synapses depress on their own (HybridBrain's per-type
slow_depression 0.9927 and slow_recovery 33.2 s for the receptor neurons) instead of not at all. Measured as
odor_probe17.py measures (Olsen's transform in DM4, DL5, VM7d and DM1; the odors' PN, Kenyon cell and MBON11 responses).
Seeds 110000 (+ 10 x glomerulus + rate for the transform; + odor for Turner's protocol, + 50 + odor for Hige's, + 900
for each type's rest, + 997 for the PNs' resting rates, + 995 for the resting brain).

Ran: depression barely matters over half a second. The fitted Rmax is 214, 335, 348 and 329 spikes/s for DM4, DL5,
VM7d and DM1 (undepressed, 223-352; Olsen 144-170) and sigma 17.9, 11.5, 10.3 and 11.4 (Olsen 16.3, 11.8, 12.4, 44.8),
the PNs already near their highest rates where the slow component would deplete most. In odors the Kenyon cells stay
flooded (mean Jaccard 0.62, 740 cells answering all six odors). The gain is the problem (odor_probe19.py).         (writes experiments/odor_probe18.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe14 as p14
import odor_probe17 as p17
import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 110000
SLOW_DEPRESSION, SLOW_RECOVERY = 1 - 0.0073, 33.247      # Nagel et al. 2015's slow component: r per spike, tau_A


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    entry = {"kc_rest_calibration": o.set(p7.CURRENT, SEED + 900)}
    entry["removed"] = p14.remove(o, p14.cholinergic_ln_edges(o), SEED + 997)
    entry["slow"] = p17.add_slow_receptor_synapses(o)
    b.slow_full[:] = False                                # depressing on their own instead
    b.sets["ORN"] = np.flatnonzero(m["orn"])
    b.set_type("ORN", slow_depression=SLOW_DEPRESSION, slow_recovery=SLOW_RECOVERY)
    entry["slow"].update(slow_depression=SLOW_DEPRESSION, slow_recovery_s=SLOW_RECOVERY)
    entry["kc_rest_recalibration"] = p3.set_kc_rest(o.s, m["kc"], types, o.own_bias(), SEED + 900)[-1]
    print(json.dumps({k: entry[k] for k in ("removed", "slow")}), flush=True)
    entry["transform"] = p17.transform(o, SEED)
    entry.update(p17.odor_measures(o, SEED, gloms, pn_of))
    out = {"question": __doc__, "flies": p7.FLIES, "condition": entry}
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_kc_drive_corr": entry["mean_kc_drive_corr"],
                      "mean_pn_early_corr": entry["mean_pn_early_corr"], "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}),
          f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
