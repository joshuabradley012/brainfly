"""Exploratory, not pre-registered: with the receptor neurons firing spontaneously, as flies' do, so that their synapses
sit partly depressed at rest, does the antennal lobe transform receptor input as flies' does?

odor_probe21.py to odor_probe23.py: with measured presynaptic inhibition the PNs' transform has flies' shape and lateral
division, but its gain is two to three times flies' at every input rate (DL5 at 5 Hz: about 100 spikes/s, Olsen et
al. 2010's fit about 36; at 160 Hz about 330, against about 160), and capping the PNs' rate at Kazama & Wilson's
164 spikes/s only clips the top (odor_probe23.py). In the model the receptor neurons are silent at rest, so every odor
meets fully rested synapses. In flies they fire spontaneously (DM4 3.4 spikes/s per neuron, most types 6-19; research_
notes/Rung 9 learning data/orn_dynamics.md), and Nagel et al. 2015's slow synaptic component, which recovers over 33 s,
integrates that firing: with presynaptic inhibition lowering release, their model holds both components at about 0.68
of full strength at rest (0.33 without inhibition). Kazama & Wilson's 6.19 mV unitary EPSP was measured rested, by
minimal stimulation of the antennal nerve once every 30 s.
Model: odor_probe22.py's antennal lobe (presynaptic inhibition, GABA-B rising over 40 ms, k_A and k_B fitted to Olsen &
Wilson 2008's EPSCs; PNs' 2.2 ms refractory period as before) with:
  - spontaneous receptor firing at the median rate of each glomerulus's sensillum class (antennal basiconic 6, palp 8,
    coeloconic 19, otherwise 6 spikes/s; odor_probe10.py's Receptors), independent Poisson trains, odors adding DoOR's
    response x 200 Hz on top as before (no time course);
  - presynaptic inhibition lowering the receptor neurons' depletion with their release (HybridBrain.set_presynaptic's
    depleting): a spike under gain g uses (1 - f) g of what is left, as Nagel et al.'s model divides the receptor rate
    that drives depression by its inhibition;
  - the receptor synapses' weights left at the rested, uninhibited strength they were calibrated to, not multiplied by
    the resting divisor as in odor_probe21.py to odor_probe23.py: Kazama & Wilson stimulated the cut antennal nerve,
    whose fibres were silent and whose local neurons had lost most of their drive, so at rest in vivo the synapses
    carry 1 / (resting divisor) of it, times their resting depression;
  - the resting state recalibrated with the spontaneous input (odor_probe10.recalibrate_rest: each neuron's bias lowered
    by its mean spontaneous receptor input, rung 4's rate calibration polishing every group but the Kenyon cells and the
    ring, the Kenyon cells' rest set again), with the inhibition on, and k_A and k_B fitted again with the spontaneous
    firing running (the LNs' resting rate, and so the resting divisor, change with it).
Measured as odor_probe21.py measures, with the spontaneous firing running throughout and the transform's and lateral
input's rates added to it (Olsen et al. subtracted baselines on both axes). Seeds 180000 (otherwise as odor_probe21.py's,
with its offsets; + 600-622 and + 630-652 for the resting recalibration and its second polish).

Ran (stopped at the calibration, by design: when the fit reaches its bound the script saves what it has and stops): the
resting state comes out as flies' and the presynaptic fit then fails. The receptor neurons fire 8.4 spikes/s on average
at rest and their synapses rest at 0.66 (fast) and 0.62 (slow) of full strength (Nagel et al.'s model: about 0.68), giving
each uniglomerular PN 24 mV of mean spontaneous input (10 of it slow), about 1.5 mV per spontaneous EPSP. The polish
couldn't hold the PNs at rung 4's 3 Hz: they went from 8 to 14 and ended at 11 spikes/s (flies 1-5), since every round
that lowered the LNs toward their targets also eased the tonic inhibition of the receptor terminals (99% of groups ended
within a factor of 2 of their targets; Kenyon cells 21.4-21.8 mV below threshold). With the spontaneous input the LNs fire
178 spikes/s between them at rest, and a lateral odor raises their traces only 2.0-2.9 times above that, so inhibition
linear in their rate, 1 + k A, can divide the synapses by at most that ratio: the fit reached its bound (k_B = 1 per
spike/s) with the control EPSCs at 0.35-0.50 of baseline against flies' 0.27-0.37. Flies' LNs are modulated no more
(their sustained odor rate is about 1.5 times their resting rate; Nagel et al. 2015, Chou et al. 2010), so flies'
presynaptic inhibition must depend on LN activity more than linearly; Wilson & Laurent 2005 note that GABA-B inhibition
"is known to depend strongly on the number of presynaptic action potentials".

    python experiments/odor_probe24.py         (writes experiments/odor_probe24.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

import odor_probe10 as p10
import odor_probe11 as p11
import odor_probe14 as p14
import odor_probe16 as p16
import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 180000


def spontaneous(rec: p10.Receptors) -> list:
    return [(rec.cells[g], rec.spont[g]) for g in rec.glomeruli if len(rec.cells[g])]


def drive_response(o: p7.Olfaction, rec: p10.Receptors, extra: dict, pns: np.ndarray, seed: int) -> dict:
    """odor_probe16.drive_response with every glomerulus at its spontaneous rate and `extra` (glomerulus -> Hz) added
    during the 0.5 s."""
    b = o.brain
    base = spontaneous(rec)
    driven = [(rec.cells[g], rec.spont[g] + extra.get(g, 0.0)) for g in rec.glomeruli if len(rec.cells[g])]
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=base)
    rest = b.advance(int(round(1.0 / b.dt)), drive=base)[:, pns].mean()
    first = b.advance(int(round(0.1 / b.dt)), drive=driven)[:, pns].mean() / 0.1
    later = b.advance(int(round(0.4 / b.dt)), drive=driven)[:, pns].mean() / 0.4
    return {"whole": round(float((0.1 * first + 0.4 * later) / 0.5 - rest), 2), "first_100ms": round(float(first - rest), 2),
            "rest": round(float(rest), 2)}


def transform(o: p7.Olfaction, rec: p10.Receptors, base: int) -> dict:
    """odor_probe17.transform with the spontaneous firing running."""
    types, m = o.types, o.m
    out = {}
    for gi, g in enumerate(p16.GLOMERULI):
        pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
        row = {"alone": {}, "lateral": {}}
        for k, hz in enumerate(p16.RATES):
            row["alone"][f"{hz:g}"] = drive_response(o, rec, {g: hz}, pns, base + 10 * gi + k)
        y = np.array([row["alone"][f"{hz:g}"]["whole"] for hz in p16.RATES])
        try:
            (rmax, sigma), _ = curve_fit(p16.olsen, np.array(p16.RATES), y, p0=(160.0, 15.0), maxfev=20000)
            row["fit"] = {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
        except RuntimeError:
            row["fit"] = None
        for k, hz in enumerate(p16.LATERAL_RATES):
            extra = {h: p16.BACKGROUND_HZ for h in rec.glomeruli if h != g}
            extra[g] = hz
            r = drive_response(o, rec, extra, pns, base + 10 * gi + 7 + k)
            alone = row["alone"][f"{hz:g}"]["whole"]
            row["lateral"][f"{hz:g}"] = {**r, "suppressed_to": round(r["whole"] / alone, 3) if alone > 0 else None}
        row["olsen"] = {"rmax": p16.OLSEN[g][0], "sigma": p16.OLSEN[g][1]}
        out[g] = row
        print("  ", g, json.dumps({"fit": row["fit"], "olsen": row["olsen"], "alone": {h: v["whole"] for h, v in row["alone"].items()},
                                   "lateral": {h: v["suppressed_to"] for h, v in row["lateral"].items()}}), flush=True)
    return out


def lateral_traces(o: p7.Olfaction, rec: p10.Receptors, seed: int) -> np.ndarray:
    """odor_probe22.lateral_traces with the spontaneous firing running under and before the lateral odors."""
    b = o.brain
    _, (wa, wb) = p22.pairs()
    base = spontaneous(rec)
    out = []
    for j, odor in enumerate(p21.LATERAL):
        b.reset(seed + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        b.advance(int(round(2.0 / b.dt)), drive=base)
        plan = rec.plan(odor, 2.0, p10.PEAK_HZ)
        drive, t, row = rec.at(plan, 0.0), 0.0, []
        for ts in p21.OLSEN_T:
            b.advance(int(round((ts - p21.VALVE_DELAY - t) / b.dt)), drive=drive)
            t = ts - p21.VALVE_DELAY
            a = b.presynaptic_state.mean(0)
            row.append((float(np.dot(wa, a)), float(np.dot(wb, a))))
        out.append(row)
    return np.array(out)


def resting_inhibitors(o: p7.Olfaction, rec: p10.Receptors, inhibitors: np.ndarray, seed: int) -> float:
    return float(np.mean([p10.resting(o, rec, seed + r)["hz"][inhibitors].sum() for r in range(p21.REST_SEEDS)]))


def apply(o, mk, base_w, base_sw, k_a, k_b, a_rest) -> tuple:
    """odor_probe22.apply without multiplying the inhibited synapses by the resting divisor, and with the receptor
    neurons' depletion following the gain. Returns the resting divisor and the per-trace k."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    taus, (wa, wb) = p22.pairs()
    k = k_a * np.array(wa) + k_b * np.array(wb)
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=taus, k=k, start=a_rest,
                      depleting=np.flatnonzero(o.m["orn"]))
    return 1.0 + (k_a + k_b) * a_rest, k


def calibrate(o: p7.Olfaction, rec: p10.Receptors, mk: dict, base_w, base_sw, k_a: float, k_b: float) -> dict:
    a_rest = resting_inhibitors(o, rec, mk["inhibitors"], SEED + 940)
    rounds = []
    for r in range(4):
        apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = p21.fit(lateral_traces(o, rec, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
        if max(k_a, k_b) > 0.99:                     # the fit's bound (1 per spike/s): flies' EPSCs out of reach
            return {"failed": "the fit reached its bound", "inhibitors_rest_hz": round(a_rest, 1), "calibration": rounds,
                    "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}
    d_rest, k = apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    taus, _ = p22.pairs()
    return {"k": k.tolist(), "k_a": k_a, "k_b": k_b, "tau_s": list(taus), "inhibitors_rest_hz": round(a_rest, 1),
            "resting_divisor": round(d_rest, 3), "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def course(o, rec, odor: str, seed: int, pns: np.ndarray, inhibitors: np.ndarray, k: np.ndarray, d_rest: float) -> dict:
    """odor_probe21.course with the spontaneous firing running."""
    b = o.brain
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=spontaneous(rec))
    rest = b.advance(int(round(1.0 / b.dt)), drive=spontaneous(rec))
    drive = rec.at(plan, 0.0)
    pn, inh, gain = [], [], []
    for _ in range(int(round(1.0 / p21.BIN))):
        c = b.advance(int(round(p21.BIN / b.dt)), drive=drive)
        pn.append(float(c[:, pns].mean() / p21.BIN))
        inh.append(float(c[:, inhibitors].sum(1).mean() / p21.BIN))
        a = b.presynaptic_state
        gain.append(float((d_rest / (1.0 + (a * k).sum(1))).mean()))
    return {"bin_s": p21.BIN, "rest_pn_hz": round(float(rest[:, pns].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain]}


def odor_measures(o: p7.Olfaction, rec: p10.Receptors, base: int, gloms: list, pn_of: dict) -> dict:
    """odor_probe17.odor_measures with odor_probe10.py's runner (the spontaneous firing running)."""
    runner = p10.make_runner(rec)
    hz = p10.resting(o, rec, base + 995)["hz"]
    types, m = o.types, o.m
    out = {"rest": {"brain_hz": round(float(hz.mean()), 3), "over_100hz": int((hz > 100).sum()), "kc_hz": round(float(hz[m["kc"]].mean()), 3),
                    "upn_hz": round(float(hz[m["upn"]].mean()), 2), "orn_hz": round(float(hz[m["orn"]].mean()), 2),
                    **{f"{x}_hz": round(float(hz[types == x].mean()), 2) for x in p7.MBONS}}}
    e, slot, pre, _, _, _ = p11.pn_input(o)
    kc = np.flatnonzero(m["kc"])
    w = o.brain.weights[e].astype(np.float64)
    out["odors"], responses, drive, pn_early = {}, [], [], []
    for k, odor in enumerate(p7.ODORS):
        kc_mask, m["kc"] = m["kc"], m["upn"]           # odor_probe14.run_binning_pns with this runner
        try:
            rp = runner(o, odor, base + k, 0.5, 1.5)
        finally:
            m["kc"] = kc_mask
        row, resp = p7.measure_odor(o, odor, base + k, base + 50 + k, (), p10.PEAK_HZ, runner)
        pm = p14.pn_measures(o, rp, odors.glomeruli(odor), gloms, pn_of)
        whole = (rp["odor"] / 0.5 - rp["rest"]).mean(0)
        row.update(pn_share_turner=round(float(p7.turner_responders(rp).mean()), 3), pn_onset=pm["summary"])
        out["odors"][odor] = row
        responses.append(resp)
        drive.append(np.bincount(slot, w * whole[pre[e]], len(kc)))
        pn_early.append(pm["early"])
        print("  ", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "evoked_spikes_0_1.4s", "pn_share_turner")}), flush=True)
    R, D, P = np.array(responses), np.array(drive), np.array(pn_early)
    out["odors_per_cell"] = {"model": np.bincount(R.sum(0), minlength=7).tolist(),
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


def recalibrate_rest(o: p7.Olfaction, rec: p10.Receptors, mk: dict, base_w: np.ndarray, base_sw: np.ndarray,
                     gain_rest: float, seed: int) -> dict:
    """odor_probe10.recalibrate_rest for this synapse: each neuron's bias lowered by its mean spontaneous receptor input,
    fast and slow (rate x resting strength x weight x the current's time constant), each component at its resting
    depression with depletion lowered by the resting presynaptic gain, and the inhibited synapses at their resting
    effective weight (base weight x resting gain); then odor_probe10's polish and the Kenyon cells' rest."""
    b, m = o.brain, o.m
    orn0 = b.cls[np.flatnonzero(m["orn"])[0]]
    f, rec_f = b.params[orn0]["depression"], b.params[orn0]["recovery"]
    fs, rec_s = b.params[orn0]["slow_depression"], b.params[orn0]["slow_recovery"]
    rate = np.zeros(b.n)
    for g, cells in rec.cells.items():
        rate[cells] = rec.spont[g]
    left_f = 1.0 / (1.0 + rate * rec_f * (1 - f) * gain_rest)
    left_s = 1.0 / (1.0 + rate * rec_s * (1 - fs) * gain_rest)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = m["orn"][pre]
    fast_in = np.bincount(b.idx[e], weights=rate[pre[e]] * left_f[pre[e]] * base_w[e] * gain_rest * p21.TAU, minlength=b.n)
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    es = mk["slow"]
    slow_in = np.bincount(b.sidx[es], weights=rate[spre[es]] * left_s[spre[es]] * base_sw[es] * gain_rest * p17.SLOW_TAU,
                          minlength=b.n)
    mean_input = fast_in + slow_in
    b.set_bias(o.own_bias() - mean_input)
    log = {"mean_input_mv": {"uPN": round(float(mean_input[m["upn"]].mean()), 2), "uPN_slow": round(float(slow_in[m["upn"]].mean()), 2),
                             "max": round(float(mean_input.max()), 2), "neurons_over_1mv": int((mean_input > 1).sum())},
           "resting_strength": {"fast": round(float(left_f[m["orn"]].mean()), 3), "slow": round(float(left_s[m["orn"]].mean()), 3)}}
    print("spontaneous input", json.dumps(log), flush=True)
    log.update(polish(o, rec, seed, p10.POLISH))
    return log


def polish(o: p7.Olfaction, rec: p10.Receptors, seed: int, schedule) -> dict:
    """odor_probe10.recalibrate_rest's polish (rung 4's schedule, Kenyon cells and the ring held) and Kenyon cell rest,
    from the biases as they stand."""
    b, s, m = o.brain, o.s, o.m
    bias = o.own_bias()
    held = s.fixed | m["kc"]
    gid = s.gid
    G = gid.max() + 1
    free_n = np.bincount(gid, weights=~held, minlength=G)
    goal = np.bincount(gid, weights=s.target * ~held, minlength=G) / np.maximum(free_n, 1)
    log = {"polish": []}
    for r, k in enumerate(schedule):
        hz = p10.resting(o, rec, seed + r)["hz"]
        got = np.bincount(gid, weights=hz * ~held, minlength=G) / np.maximum(free_n, 1)
        step = np.where(free_n > 0, np.clip(k * np.log((goal + p10.attempt1.SOFT) / (got + p10.attempt1.SOFT)), -k, k), 0.0)
        bias = bias + np.where(held, 0.0, step[gid])
        b.set_bias(bias)
        log["polish"].append({"round": r + 1, "upn_hz": round(float(hz[m["upn"]].mean()), 2), "orn_hz": round(float(hz[m["orn"]].mean()), 2),
                              "groups_within_2x": round(float(p10.attempt1.within_factor_2(got, goal)[free_n > 0].mean()), 4)})
        print("polish", json.dumps(log["polish"][-1]), flush=True)
    threshold = b.params[b.cls[np.flatnonzero(m["kc"])[0]]]["threshold"]
    kc_types = o.types[m["kc"]]
    for r in range(2):
        u = p10.resting(o, rec, seed + 20 + r, sample=True)["u"]
        for t in np.unique(kc_types):
            mask = o.types == t
            bias[mask] += (threshold - p10.p3.KC_GAP_MV) - u[mask].mean()
        b.set_bias(bias)
    u = p10.resting(o, rec, seed + 22, sample=True)["u"]
    log["kc_gap_mv"] = {t: round(float(threshold - u[o.types == t].mean()), 2) for t in np.unique(kc_types)}
    print("Kenyon cells' distance below threshold:", json.dumps(log["kc_gap_mv"]), flush=True)
    return log


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = SEED
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    out["spontaneous_hz"] = rec.spont
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()      # the recalibration moves biases, not weights
    # the inhibition at odor_probe22.py's strengths, its traces starting at the LNs' resting rate without spontaneous
    # receptor input, while the resting state is recalibrated; then fitted again, and the rest polished again
    k_a0, k_b0 = 0.000851, 0.009247
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 930)
    d0, _ = apply(o, mk, base_w, base_sw, k_a0, k_b0, a0)
    out["resting_recalibration"] = recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0 / d0, SEED + 600)
    entry = {"presynaptic": calibrate(o, rec, mk, base_w, base_sw, k_a0, k_b0)}
    if "failed" in entry["presynaptic"]:
        out["condition"], out["seconds"] = entry, round(time.perf_counter() - t0)
        OUT.write_text(json.dumps(out, indent=1))
        print("stopped:", entry["presynaptic"]["failed"], flush=True)
        return
    out["second_polish"] = polish(o, rec, SEED + 630, [0.5] * 6)
    k, d_rest = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["resting_divisor"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = course(o, rec, odor, base + 700 + j, pns, mk["inhibitors"], k, d_rest)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = transform(o, rec, base)
    entry.update(odor_measures(o, rec, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
