"""Exploratory, not pre-registered: is the model's antennal lobe gain twice flies' because it lacks the receptor
terminals' presynaptic GABA-B inhibition?

odor_probe18.py: with Nagel et al. 2015's two-component receptor synapse (the slow component depressing as measured),
the PNs' transform has Olsen et al. 2010's shape (sigma 10-18, against 12-16) but about twice their gain (Rmax 214-348
spikes/s, against 144-170). In flies, local neurons inhibit the receptor neurons' terminals presynaptically, through
GABA-A early and GABA-B over seconds (Olsen & Wilson 2008), and blocking GABA-B "increased the slope of the input-output
function by 105% with no effect on the offset" (Root et al. 2008; research_notes/Rung 4 resting state data/
short_term_plasticity.md). The model has no GABA-B anywhere, so its receptor synapses act as flies' do with GABA-B
blocked.
Condition: odor_probe18.py's, with every receptor-to-uniglomerular-PN synapse's weight, fast and slow, divided by 2.05,
standing in for GABA-B's presynaptic gain control as a fixed factor. In flies it grows with the local neurons' activity
(so it also divides one glomerulus's response by the others'); a fixed factor can't do that, and it also halves the
synapses at rest, where Kazama & Wilson's 6.19 mV unitary EPSP was measured. Measured as odor_probe17.py measures.
Seeds 120000 (+ 10 x glomerulus + rate for the transform; + odor for Turner's protocol, + 50 + odor for Hige's, + 900
for each type's rest, + 997 for the PNs' resting rates, + 995 for the resting brain).

Ran: it closes about half the gap. The fitted Rmax is 173, 293, 307 and 286 spikes/s for DM4, DL5, VM7d and DM1 (Olsen
170, 167, 163, 144) and sigma 25, 17, 15 and 18 (16.3, 11.8, 12.4, 44.8). DM4, whose two main PNs get about half the
median PN's summed receptor weight (77-99 against 160), lands on Olsen's Rmax; the others, near or above the median,
stay about 1.8 times too high, so evening out the PNs' receptor input wouldn't close the gap either. Lateral input still
barely divides (0.89-1.26). In odors the PNs fire 199-219 Hz in the first 100 ms and 252-279 Hz over a whole 1 s
odor, rising where flies' accommodate; 15-48% of Kenyon cells respond (flies 6 +- 5%) and MBON11 gains 20-68 spikes.
A fixed factor halves weak and strong input alike. In flies the presynaptic inhibition grows with the local neurons'
activity, early through GABA-A and late through GABA-B, so it cuts strong drive more, accommodates the response, and
divides one glomerulus's output by the others' input: the next step is that inhibition itself.

    python experiments/odor_probe19.py         (writes experiments/odor_probe19.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe14 as p14
import odor_probe17 as p17
import odor_probe18 as p18
import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 120000
GABA_B_SLOPE = 2.05                                       # Root et al. 2008: blocking GABA-B raises the slope 105%


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    entry = {"kc_rest_calibration": o.set(p7.CURRENT, SEED + 900)}
    entry["removed"] = p14.remove(o, p14.cholinergic_ln_edges(o), SEED + 997)
    entry["slow"] = p17.add_slow_receptor_synapses(o)
    b.slow_full[:] = False
    b.sets["ORN"] = np.flatnonzero(m["orn"])
    b.set_type("ORN", slow_depression=p18.SLOW_DEPRESSION, slow_recovery=p18.SLOW_RECOVERY)
    fast = o.orn_pn & (b.weights > 0)
    w = b.weights.copy()
    w[fast] /= GABA_B_SLOPE
    b.weights, b._external_matrix = w, None
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    slow = m["orn"][spre] & m["upn"][b.sidx]
    b.slow_weights = b.slow_weights.copy()
    b.slow_weights[slow] /= GABA_B_SLOPE
    entry["gaba_b"] = {"factor": round(1 / GABA_B_SLOPE, 4), "fast_edges": int(fast.sum()), "slow_edges": int(slow.sum())}
    entry["kc_rest_recalibration"] = p3.set_kc_rest(o.s, m["kc"], types, o.own_bias(), SEED + 900)[-1]
    print(json.dumps({k: entry[k] for k in ("removed", "slow", "gaba_b")}), flush=True)
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
