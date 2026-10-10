"""Exploratory, not pre-registered: with the receptor terminals inhibited presynaptically by the local neurons, as in
flies, does the antennal lobe transform receptor input as flies' does?

odor_probe19.py: dividing every receptor synapse by Root et al. 2008's GABA-B factor (blocking GABA-B doubles the PNs'
input-output slope) brings DM4 to Olsen et al. 2010's Rmax but leaves the other glomeruli 1.8 times high, and PNs rise
through an odor where flies' accommodate. In flies the inhibition depends on activity: GABAergic local neurons (LNs)
inhibit the receptor neurons' terminals presynaptically, early through GABA-A (onset with an alpha function of tau about
25 ms) and late, over seconds, through GABA-B (Olsen & Wilson 2008; research_notes/Rung 4 resting state data/
short_term_plasticity.md), so strong or widespread input divides itself.
Model: odor_probe18.py's (no cholinergic LN-to-PN synapses; Nagel et al. 2015's two-component receptor synapse, the slow
component depressing as measured) with HybridBrain.set_presynaptic on every receptor-to-uniglomerular-PN synapse, fast
and slow: their strength divided by 1 + k A, A the GABAergic antennal lobe LNs' summed spike rate low-passed over 1 s
(GABA-B's late phase). k is set from Root et al.: GABA-B halves the gain (k A = 1.05) at the LNs' mean summed rate over
the six odors' 0.5 s, measured first in the model without the inhibition. GABA-A's early part is left out here.
Measured as odor_probe17.py measures (Olsen's transform in DM4, DL5, VM7d and DM1, now also dividing laterally; the
odors' PN, Kenyon cell and MBON11 responses). Seeds 130000 (+ 300 + odor for the LNs' rate; + 10 x glomerulus + rate
for the transform; + odor for Turner's protocol, + 50 + odor for Hige's, + 900 for each type's rest, + 997 for the PNs'
resting rates, + 995 for the resting brain).

Ran: the slow inhibition barely acts within half a second. The 90 GABAergic LNs fire 167 spikes/s between them at rest
and 1,572-2,436 in odors (mean 2,092), so k = 0.000502 per spike/s. Driven alone, the four glomeruli's fitted Rmax is
211, 328, 344 and 324 spikes/s (odor_probe18.py, without the inhibition: 214-348; Olsen 144-170) and sigma 18, 12, 11
and 12. Lateral input now divides three of the four a little (to 0.79-0.91 of the response alone; DM4 not at all,
0.97-1.08), where without the inhibition it didn't (0.99-1.24). In odors the PNs fire 239-258 Hz in the first 100 ms
and 287-315 Hz over a whole 1 s odor, still rising where flies' accommodate; they stay about as broad as flies' (39-61%
by Turner's criterion, flies 59 +- 14%), but 22-56% of Kenyon cells respond (flies 6 +- 5%; mean Jaccard 0.57) and
MBON11 gains 35-86 spikes. The reason is the time constant: low-passed over 1 s, the LNs' rate climbs only part of the
way during a 0.5 s stimulus, so for a full odor the gain falls from 0.92 at rest to about 0.7 by 0.5 s, 0.78 on average
(derived from the LNs' rates without the inhibition), not the 0.49 k was set for. How to set k depends on what Root
et al. measured: over which window, and whether part of GABA-B's effect is tonic. The early, GABA-A phase is still
missing (odor_probe21.py).

    python experiments/odor_probe20.py         (writes experiments/odor_probe20.json)
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
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
SEED = 130000
TAU_B, GABA_B_SLOPE = 1.0, 2.05


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
    entry["kc_rest_recalibration"] = p3.set_kc_rest(o.s, m["kc"], types, o.own_bias(), SEED + 900)[-1]
    nt = np.asarray(consensus_transmitters())
    gaba_ln = np.flatnonzero(np.array([bool(p14.LN.match(t)) for t in types]) & (nt == "gaba"))
    rates = []
    for k, odor in enumerate(p7.ODORS):
        r = p7.run(o, odor, SEED + 300 + k, 0.5, 1.5)
        rates.append({"odor": float((r["odor"][:, gaba_ln].sum(1) / 0.5).mean()), "rest": float(r["rest"][:, gaba_ln].sum(1).mean())})
        print("GABA LNs during", odor, json.dumps({x: round(v, 1) for x, v in rates[-1].items()}), flush=True)
    a_odor = float(np.mean([x["odor"] for x in rates]))
    k_b = (GABA_B_SLOPE - 1.0) / a_odor
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    fast = o.orn_pn & (b.weights > 0)
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    slow = m["orn"][spre] & m["upn"][b.sidx]
    b.set_presynaptic(fast=fast, slow=slow, inhibitors=gaba_ln, tau=TAU_B, k=k_b)
    entry["presynaptic"] = {"gaba_lns": int(len(gaba_ln)), "ln_summed_hz": {"odor_mean": round(a_odor, 1), "rest_mean": round(float(np.mean([x["rest"] for x in rates])), 1),
                                                                         "per_odor": [round(x["odor"], 1) for x in rates]},
                            "tau_s": TAU_B, "k_per_hz": round(k_b, 6), "gain_at_odor_rate": round(1 / GABA_B_SLOPE, 3),
                            "fast_edges": int(fast.sum()), "slow_edges": int(slow.sum())}
    print(json.dumps({k: entry[k] for k in ("removed", "slow", "presynaptic")}), flush=True)
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
