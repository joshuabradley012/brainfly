"""Exploratory check, not pre-registered: why do 4-methylcyclohexanol's weakly driven glomeruli answer so little in the
model, against flies' transform?

odor_probe55.py: with the receptor input the evidence supports (receptor_fills.RECOMMENDED), the model's projection
neurons answer 4-methylcyclohexanol at 0.51 of 3-octanol's over Badel et al.'s 37 glomeruli (flies 0.98). Olsen et al.
2010's transform with their normalization (165 r^1.5 / (12^1.5 + r^1.5 + (0.05 x summed input)^1.5); research_notes/
Rung 9 learning data/oct_mch_concentration.md section 5.2) gives 0.90 on the same input. Compared glomerulus by
glomerulus (from odor_probe55.json, before this was written): where the input is strong (80-300 Hz) the model matches the
equation (3-octanol: 491 against 487 spikes/s summed), but it gives 0.68 of it at 30-80 Hz, 0.36 at 10-30 Hz and nothing
below 10. 4-methylcyclohexanol leans on weak glomeruli: its seven at 10-30 Hz sum 141 against the equation's 405, its 22
below 10 Hz 36 against 245. In the odor's context the equation divides a 20 Hz glomerulus's response by 1.7 for
4-methylcyclohexanol and 7.6 for 3-octanol; the model's single-glomerulus transform is also weaker than flies' (Rmax
127-130 against 163-170, sigma 14-17 against 12-16; odor_probe54.py).
Model: odor_probe54.py's (its cache), receptor input as receptor_fills.RECOMMENDED gives it.
Measured (2 seeds of 8 flies; the cholinergic uniglomerular PNs' rate over the odor's first 0.5 s less the 0.4 s before,
as odor_probe55.py measures it; Olsen's equation for each with and without the normalization):
  alone     each of 4-methylcyclohexanol's glomeruli with at least 8 Hz of input driven alone, with that input's time
            course (the others at their spontaneous rates): the transform without the odor's other glomeruli;
  whole     the whole odor, each glomerulus's response, and with it the presynaptic inhibition's gain relative to rest
            and the GABAergic LNs' rate;
  no post   the whole odor with the GABAergic LNs' synapses onto uniglomerular PNs removed (each PN's bias lowered by the
            mean inhibition they gave it at rest, so that it rests as before): how much of the suppression is
            postsynaptic (presynaptic inhibition can't be removed the same way: the receptor synapses' resting depletion
            follows its gain);
  and the whole odor and no post for 3-octanol, for comparison.

Ran: the shortfall is the transform's weak end; postsynaptic inhibition plays almost no part, and the odor divides the
weak glomeruli about as flies' normalization does until they near threshold. Alone, 4-methylcyclohexanol's seven
glomeruli with 12-20 Hz of input answer at 46-53 spikes/s (DA4l, VC1, VC2, DL4, DM2, VM2; VC3 an outlier at 19), 0.43 of
Olsen et al.'s transform summed (309 against 721), and VA3 and D at 96 and 99 (161 and 143). In the whole odor those seven
keep 0.45 of their alone responses (137.5 spikes/s summed; the equation's normalization keeps 0.56), but the two at 8 Hz
(DM6, VM7d) keep 0.10 (the equation 0.42): the odor's presynaptic inhibition divides the receptor synapses by 1.4 (gain
0.71 of rest, 0.58 at its lowest; 3-octanol 0.52 and 0.38) and pushes PNs that weak input leaves near threshold below it.
Without the GABAergic LNs' synapses onto PNs the responses barely change (seven glomeruli 139.9 against 137.5;
3-octanol's at 30-80 Hz 488 against 472). So 4-methylcyclohexanol's missing breadth comes from the PNs' weak-input
gain, about half of flies' (Rmax 0.77 of flies' and sigma^1.5 1.3-1.6 times, which multiply at weak input), not from
missing lateral excitation or excess postsynaptic inhibition. No model reproduces flies' weak-input gain from measured
parameters (weak_input_gain.md), and raising the PNs' reset scales their responses from 10 Hz of input up but barely
the weakest (odor_pn_reset_check.py).

    python experiments/odor_weak_glomeruli_check.py      (writes experiments/odor_weak_glomeruli_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe24 as p24
import odor_probe44 as p44
import odor_probe54 as p54
import warm
from brainfly.hybrid import consensus_transmitters
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 730000, 2
ODORS = ("4-methylcyclohexanol", "3-octanol")
ALONE_HZ = 8.0
LEAD_S, PRE_S, ODOR_S = 0.3, 0.5, 0.5
RMAX, SIGMA, M, EXPONENT = 165.0, 12.0, 0.05, 1.5          # Olsen et al. 2010, Luo et al. 2010


def olsen(r: float, summed: float = 0.0) -> float:
    return RMAX * r ** EXPONENT / (SIGMA ** EXPONENT + r ** EXPONENT + (M * summed) ** EXPONENT)


def gain_of(b) -> np.ndarray:
    """Each fly's presynaptic gain now (1 / the divisor; 1 without presynaptic inhibition)."""
    p = b._presynaptic
    if p is None:
        return np.ones(b.trials)
    a = np.maximum(b.presynaptic_state - np.asarray(p["offset"]), 0.0)
    return 1.0 / (1.0 + (np.asarray(p["k"]) * a ** np.asarray(p["power"])).sum(1))


def trial(o, rec, plan, seed: int, sets: dict, gaba: np.ndarray) -> dict:
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -PRE_S - LEAD_S
    for _ in range(int(round(LEAD_S / p10.PIECE))):
        b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
    n = int(round((PRE_S + ODOR_S) / p10.PIECE))
    hz = {k: np.zeros(n) for k in sets}
    gain, gaba_hz = np.zeros(n), np.zeros(n)
    for i in range(n):
        c = b.advance(piece, drive=rec.at(plan, t))
        for k, cells in sets.items():
            hz[k][i] = float(c[:, cells].mean()) / p10.PIECE
        gain[i] = float(gain_of(b).mean())
        gaba_hz[i] = float(c[:, gaba].mean()) / p10.PIECE
        t += p10.PIECE
    return {"hz": hz, "gain": gain, "gaba_hz": gaba_hz}


def evoked(x: np.ndarray) -> float:
    n_pre = int(round(PRE_S / p10.PIECE))
    return float(x[n_pre:].mean() - x[:n_pre - 10].mean())


def run(o, rec, plan, base: int, sets: dict, gaba: np.ndarray) -> dict:
    rs = [trial(o, rec, plan, base + s, sets, gaba) for s in range(SEEDS)]
    n_pre = int(round(PRE_S / p10.PIECE))
    gain = np.mean([r["gain"] for r in rs], 0)
    gh = np.mean([r["gaba_hz"] for r in rs], 0)
    return {"pn_evoked_hz": {k: round(evoked(np.mean([r["hz"][k] for r in rs], 0)), 2) for k in sets},
            "gain_over_rest": round(float(gain[n_pre:].mean() / gain[:n_pre - 10].mean()), 3),
            "gain_min_over_rest": round(float(gain[n_pre:].min() / gain[:n_pre - 10].mean()), 3),
            "gaba_ln_hz": {"rest": round(float(gh[:n_pre - 10].mean()), 2), "odor": round(float(gh[n_pre:].mean()), 2)}}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import receptor_fills                              # after the cache, so that its edits don't invalidate it
    b = o.brain
    nt = np.asarray(consensus_transmitters())
    gloms = [g for g in rec.glomeruli if len(rec.cells[g])]
    sets = {g: np.flatnonzero(o.m["upn"] & (nt == "acetylcholine") & np.char.startswith(o.types, f"{g}_")) for g in gloms}
    sets = {g: v for g, v in sets.items() if len(v)}
    gaba = np.flatnonzero(np.array([bool(p14.LN.match(t)) for t in o.types]) & (nt == "gaba"))
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    post_e = np.isin(pre, gaba) & o.m["upn"][b.idx]
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    post_s = np.isin(spre, gaba) & o.m["upn"][b.sidx]
    w0, sw0, bias0 = b.weights.copy(), b.slow_weights.copy(), o.own_bias()
    out = {"question": __doc__, "olsen": {"rmax": RMAX, "sigma": SIGMA, "m": M, "exponent": EXPONENT},
           "gaba_ln_to_upn": {"fast_edges": int(post_e.sum()), "slow_edges": int(post_s.sum())}, "odors": {}}
    with receptor_fills.applied(recommended=True) as inputs, warm.tracking(o, rec) as held:
        out["inputs"] = inputs
        for i, odor in enumerate(ODORS):
            rows = {}
            v = {g: x for g, x in receptor_fills.RECOMMENDED[odor].items() if x > 0}
            summed = 200.0 * sum(v.values())
            base = SEED + 10000 * i
            plan = rec.plan(odor, ODOR_S, p10.PEAK_HZ)
            rows["whole"] = run(o, rec, plan, base, sets, gaba)
            if odor == ODORS[0]:
                alone = {}
                for j, g in enumerate(sorted((g for g in v if 200 * v[g] >= ALONE_HZ and g in sets), key=lambda g: -v[g])):
                    p = dict(plan, rows=[(h, x if h == g else 0.0, lat) for h, x, lat in plan["rows"]])
                    r = run(o, rec, p, base + 100 + 10 * j, {g: sets[g]}, gaba)
                    alone[g] = r["pn_evoked_hz"][g]
                    print(odor, "alone", g, alone[g], flush=True)
                rows["alone"] = alone
            # no post: the GABAergic LNs' synapses onto uniglomerular PNs removed, rest compensated
            b.reset(SEED + 9000 + i)                           # a settled rest (warm.tracking's)
            b.set_release(o.s.ol.neurons, o.s.silent)
            rest = b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec)).mean(0)
            tau_slow = np.array([b.params[c].get("tau_slow", 0.0) for c in range(len(b.params))])[b.cls]
            lost = np.bincount(b.idx[post_e], weights=rest[pre[post_e]] * w0[post_e] * TAU, minlength=b.n)
            lost += np.bincount(b.sidx[post_s], weights=rest[spre[post_s]] * sw0[post_s] * tau_slow[b.sidx[post_s]], minlength=b.n)
            w, sw = w0.copy(), sw0.copy()
            w[post_e], sw[post_s] = 0.0, 0.0
            b.weights, b.slow_weights, b._external_matrix = w.astype(np.float32), sw.astype(np.float32), None
            b.set_bias(bias0 + lost)
            rows["no post"] = run(o, rec, plan, base + 50, sets, gaba)
            rows["no post"]["bias_change_mv"] = {"upn_mean": round(float(lost[o.m["upn"]].mean()), 3)}
            b.weights, b.slow_weights, b._external_matrix = w0, sw0, None
            b.set_bias(bias0)
            table = {}
            for g in sorted(v, key=lambda g: -v[g]):
                if g not in sets:
                    continue
                r = 200.0 * v[g]
                table[g] = {"input_hz": round(r, 1), "olsen_alone": round(olsen(r), 1), "olsen_whole": round(olsen(r, summed), 1),
                            "model_alone": rows.get("alone", {}).get(g), "model_whole": rows["whole"]["pn_evoked_hz"][g],
                            "model_no_post": rows["no post"]["pn_evoked_hz"][g]}
            bins = {}
            for lo, hi in ((0, 10), (10, 30), (30, 80), (80, 400)):
                gs = [g for g, t in table.items() if lo <= t["input_hz"] < hi]
                if gs:
                    bins[f"{lo}-{hi} Hz"] = {"glomeruli": len(gs), **{k: round(sum(max(table[g][k], 0.0) for g in gs), 1)
                                                                     for k in ("olsen_whole", "model_whole", "model_no_post")}}
                    if odor == ODORS[0]:
                        al = [g for g in gs if table[g]["model_alone"] is not None]
                        if al:
                            bins[f"{lo}-{hi} Hz"].update({"with_alone": len(al), "olsen_alone": round(sum(table[g]["olsen_alone"] for g in al), 1),
                                                          "model_alone": round(sum(max(table[g]["model_alone"], 0.0) for g in al), 1),
                                                          "model_whole_same": round(sum(max(table[g]["model_whole"], 0.0) for g in al), 1),
                                                          "olsen_whole_same": round(sum(table[g]["olsen_whole"] for g in al), 1)})
            rows.update({"summed_input_hz": round(summed, 1), "table": table, "bins": bins})
            out["odors"][odor] = rows
            print(odor, json.dumps({k: rows[k] for k in ("summed_input_hz", "bins")}),
                  json.dumps({k: {x: rows[k][x] for x in ("gain_over_rest", "gain_min_over_rest", "gaba_ln_hz")} for k in ("whole", "no post")}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
        out["settles"] = held["settles"]
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
