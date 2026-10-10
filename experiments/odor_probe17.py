"""Exploratory, not pre-registered: with the slow component of flies' receptor synapses added, does the antennal lobe
transform receptor input as flies' does, and do the Kenyon cells' responses become more odor-specific?

odor_probe16.py: one glomerulus's receptor neurons (ORNs) driven alone, its projection neurons (PNs) saturate early
(fitted Rmax 56-115 spikes/s, against Olsen et al. 2010's 144-170) and answer weak input too strongly (sigma 3.7-4.1,
against 11.8-44.8), so PN patterns approach on and off and different odors' patterns correlate. The model's ORN-to-PN
synapse has the fast, depressing component of Nagel, Hong & Wilson 2015's fit (each spike leaves 78% of its strength,
recovering over 0.89 s; their r = 0.23 per spike, tau_A = 1006 ms). It lacks their slow component: k = 1.8 nS per spike
with tau_g = 80 ms, 0.774 times the fast component's charge (20 nS, 9.3 ms), depleting by r = 0.0073 per spike and
recovering over 33 s (research_notes/Rung 9 learning data/orn_dynamics.md). Over a 0.5 s odor it barely depletes, so at
high ORN rates, where the fast component is depressed to a tenth, the slow one would carry most of the drive.
Conditions, both with odor_probe14.py's correction (the cholinergic local neurons' synapses onto PNs removed, each PN's
bias raised by the resting input it lost) and the Kenyon cells' rest recalibrated:
  no cholinergic LN->PN       as odor_probe14.py, on new seeds
  + slow receptor synapses    each ORN-to-uniglomerular-PN synapse also acting through the PN's slow current, with
                              0.774 times its rested fast charge, an 80 ms time constant (the PNs' tau_slow) and no
                              depression (HybridBrain.slow_full; their depletion over a 0.5 s pulse is a few percent)
Measured for each: Olsen's transform as odor_probe16.py measures it (DM4, DL5, VM7d and DM1 alone at 5-160 Hz, the
fitted Rmax and sigma; lateral input at 20 Hz in every other glomerulus); and the odors as odor_probe14.py measures them
(PNs by Turner's criterion, flies 59 +- 14%; the Kenyon cells' shares, classes, overlaps and how many odors each
answers; MBON11's evoked spikes; the resting brain). Seeds 100000 + 1000 x condition (+ 10 x glomerulus + rate for the
transform; + odor for Turner's protocol, + 50 + odor for Hige's, + 900 for each type's rest, + 997 for the PNs' resting
rates, + 995 for the resting brain).

    python experiments/odor_probe17.py         (writes experiments/odor_probe17.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.optimize import curve_fit

import odor_probe14 as p14
import odor_probe16 as p16
import odor_probe3 as p3
import odor_probe7 as p7
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED = 100000
SLOW_CHARGE, SLOW_TAU = (1.8 * 80.0) / (20.0 * 9.3), 0.08      # Nagel et al. 2015's slow over fast charge; tau_g, s
CONDITIONS = ("no cholinergic LN->PN", "+ slow receptor synapses")


def add_slow_receptor_synapses(o: p7.Olfaction) -> dict:
    """Give every ORN-to-uPN synapse a slow, undepressed component, 0.774 x its rested fast charge, tau 80 ms."""
    b, m = o.brain, o.m
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(o.orn_pn & (b.weights > 0))
    # slow counts: HybridBrain weighs them by w_syn x the target's scale, as the fast counts; the fast weights carry
    # odor_probe7's receptor factor on top, so the slow ones need it too, and TAU / SLOW_TAU for the slower current
    factor = float(np.median(b.weights[e] / (b._counts[e] * b.w_syn * b.scale[b.idx[e]])))
    counts = b._counts[e] * factor * SLOW_CHARGE * TAU / SLOW_TAU
    old = sparse.csc_matrix((b._slow_counts, b.sidx, b.sptr), shape=(b.n, b.n))
    add = sparse.csc_matrix((counts, (b.idx[e], pre[e])), shape=(b.n, b.n))
    b.set_slow((old + add).tocsc())
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    b.slow_full[:] = m["orn"][spre] & m["upn"][b.sidx]
    b.sets["uPN"] = np.flatnonzero(m["upn"])
    b.set_type("uPN", tau_slow=SLOW_TAU)
    return {"edges": int(len(e)), "receptor_factor": round(factor, 3), "slow_edges": int(b.slow_full.sum()),
            "pn_tau_slow_s": SLOW_TAU, "slow_over_fast_charge": round(SLOW_CHARGE, 3)}


def transform(o: p7.Olfaction, base: int) -> dict:
    """odor_probe16's measurement of Olsen et al.'s transform in the brain as it stands."""
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]})
    orns = {g: b.cells([f"ORN_{g}"]) for g in gloms}
    out = {}
    for gi, g in enumerate(p16.GLOMERULI):
        pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
        row = {"alone": {}, "lateral": {}}
        for k, hz in enumerate(p16.RATES):
            row["alone"][f"{hz:g}"] = p16.drive_response(o, [(orns[g], hz)], pns, base + 10 * gi + k)
        y = np.array([row["alone"][f"{hz:g}"]["whole"] for hz in p16.RATES])
        try:
            (rmax, sigma), _ = curve_fit(p16.olsen, np.array(p16.RATES), y, p0=(160.0, 15.0), maxfev=20000)
            row["fit"] = {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
        except RuntimeError:
            row["fit"] = None
        background = [(orns[h], p16.BACKGROUND_HZ) for h in gloms if h != g and len(orns[h])]
        for k, hz in enumerate(p16.LATERAL_RATES):
            r = p16.drive_response(o, [(orns[g], hz)] + background, pns, base + 10 * gi + 7 + k)
            alone = row["alone"][f"{hz:g}"]["whole"]
            row["lateral"][f"{hz:g}"] = {**r, "suppressed_to": round(r["whole"] / alone, 3) if alone > 0 else None}
        row["olsen"] = {"rmax": p16.OLSEN[g][0], "sigma": p16.OLSEN[g][1]}
        out[g] = row
        print("  ", g, json.dumps({"fit": row["fit"], "olsen": row["olsen"], "alone": {h: v["whole"] for h, v in row["alone"].items()},
                                   "lateral": {h: v["suppressed_to"] for h, v in row["lateral"].items()}}), flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m = o.types, o.m
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        base = SEED + 1000 * c
        entry = {"kc_rest_calibration": o.set(p7.CURRENT, base + 900)}
        entry["removed"] = p14.remove(o, p14.cholinergic_ln_edges(o), base + 997)
        if name != "no cholinergic LN->PN":
            entry["slow"] = add_slow_receptor_synapses(o)
        entry["kc_rest_recalibration"] = p3.set_kc_rest(o.s, m["kc"], types, o.own_bias(), base + 900)[-1]
        print(name, json.dumps({k: entry.get(k) for k in ("removed", "slow")}), flush=True)
        entry["transform"] = transform(o, base)
        measured = odor_measures(o, base, gloms, pn_of)
        entry.update(measured)
        out["conditions"][name] = entry
        pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_kc_drive_corr": entry["mean_kc_drive_corr"],
                                "mean_pn_early_corr": entry["mean_pn_early_corr"], "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}),
              f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


def odor_measures(o: p7.Olfaction, base: int, gloms: list, pn_of: dict) -> dict:
    """odor_probe14.condition's measurements, in the brain as it stands (no new setup)."""
    from itertools import combinations

    import odor_probe11 as p11
    from brainfly import odors
    out = {"rest": p7.rest_measures(o, base + 995)}
    e, slot, pre, pn_weight, _, _ = p11.pn_input(o)
    kc = np.flatnonzero(o.m["kc"])
    w = o.brain.weights[e].astype(np.float64)
    out["odors"], responses, drive, pn_early = {}, [], [], []
    for k, odor in enumerate(p7.ODORS):
        rp = p14.run_binning_pns(o, odor, base + k)
        row, resp = p7.measure_odor(o, odor, base + k, base + 50 + k)
        pm = p14.pn_measures(o, rp, odors.glomeruli(odor), gloms, pn_of)
        whole = (rp["odor"] / 0.5 - rp["rest"]).mean(0)
        row.update(pn_share_turner=round(float(p7.turner_responders(rp).mean()), 3), pn_onset=pm["summary"])
        out["odors"][odor] = row
        responses.append(resp)
        drive.append(np.bincount(slot, w * whole[pre[e]], len(kc)))
        pn_early.append(pm["early"])
        print("  ", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "evoked_spikes_0_1.4s", "pn_share_turner")}), flush=True)
    R, D, P = np.array(responses), np.array(drive), np.array(pn_early)
    count = R.sum(0)
    out["odors_per_cell"] = {"model": np.bincount(count, minlength=7).tolist(),
                             "independent": [round(float(x) * len(kc), 1) for x in p11.independent(R.mean(1))]}
    out["pairs"] = {}
    for i, j in combinations(range(len(p7.ODORS)), 2):
        both = (R[i] & R[j]).sum()
        out["pairs"][f"{p7.ODORS[i]} | {p7.ODORS[j]}"] = {
            "jaccard": round(float(both / max((R[i] | R[j]).sum(), 1)), 3),
            "share_of_first_in_second": round(float(both / max(R[i].sum(), 1)), 3),
            "share_of_second_in_first": round(float(both / max(R[j].sum(), 1)), 3),
            "kc_drive_corr": round(float(np.corrcoef(D[i], D[j])[0, 1]), 3),
            "pn_early_corr": round(float(np.corrcoef(P[i], P[j])[0, 1]), 3)}
    for key in ("jaccard", "kc_drive_corr", "pn_early_corr"):
        out[f"mean_{key}"] = round(float(np.mean([p[key] for p in out["pairs"].values()])), 3)
    return out


if __name__ == "__main__":
    main()
