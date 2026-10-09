"""Exploratory, not pre-registered: why do the current model's responding Kenyon cells overlap so much across odors, and
does making the Kenyon cells' excitability more even, as flies' is, make their responses odor-specific?

odor_probe7.py's current model: 3-octanol's and 4-methylcyclohexanol's responding Kenyon cells have a Jaccard index of
0.32. 16.7% and 7.3% of the cells respond, so 80% of 4-methylcyclohexanol's responders also respond to 3-octanol, and
pairing either odor with dopamine depresses the other's response (learning_pilot.py). In flies the two odors "activate
very different populations of KCs" (Honegger et al. 2011), dissimilar odors share about a fifth of their responders
(Campbell et al. 2013: 21.8%), each Kenyon cell responds to 6 +- 12% of odors, and each rests 21.5 +- 5.6 mV below
its spike threshold (Turner et al. 2008, n = 17; research_notes/Rung 9 learning data/).
A static check (each Kenyon cell's input from the projection neurons, PNs, weighted by DoOR's glomerular responses;
odor_probe12.py saves it) finds each odor's input correlating with a cell's total PN input (r = 0.35-0.62). So the
simulated overlap may come from uneven excitability: cells with more PN input, or resting nearer threshold, answering
every odor. The model sets each Kenyon cell type's mean distance below threshold (odor_probe3.set_kc_rest), not each
cell's.
Diagnosis, in the current model, per Kenyon cell: its responses to the six odors (Turner's protocol and criterion, as
odor_probe7.py); its distance below threshold from its mean membrane potential over 1 s of rest; its excitatory PN
input (summed weight, connections, glomeruli); and each odor's drive on it, the summed weight of its PN inputs times
their rise in rate over the 0.5 s odor. Reported: how many odors each cell responds to against independent responses
at the same shares; the response probability by quintile of rest distance, of PN input and of glomeruli; the rest
distance's spread against Turner's 5.6 mV; the share of each odor's responders that respond to another (Campbell's
measure); how much the odors' drives correlate across cells.
Conditions, each from a measurement (all else the current model):
  current                         each type's mean 21.5 mV below threshold
  per-cell rest                   every Kenyon cell 21.5 mV below threshold (Turner's mean), by its own bias
  per-cell rest, Turner's spread  every Kenyon cell at its own distance, drawn from Turner's 21.5 +- 5.6 mV (clipped
                                  to 8.5-34.5, the 1st to 99th percentiles) independently of its input
  equal PN input                  each Kenyon cell's PN synapses scaled so its summed PN weight is its type's median,
                                  then each type's mean recalibrated to 21.5 mV: the compensation Abdelrahman et al.
                                  2021 found in part in the hemibrain (more claws, fewer synapses per claw), carried
                                  through
  equal PN input, per-cell rest   both
Measured for each, as odor_probe7.py: the shares and classes responding, spikes per response, MBON11's evoked spikes
(Hige et al.'s protocol), the overlaps, and the resting brain. Seeds 40000 + 100 x condition + odor (Turner's
protocol), + 50 + odor (Hige's), + 90 (each type's rest), + 80 (each cell's), + 70 (the spread's draw), + 95 (the
resting brain), + 97 (the rest sample).

Ran: the overlap isn't the Kenyon cells' rest, and only partly their input. Each type's calibration already leaves
every Kenyon cell within 0.1-0.2 mV of 21.5 mV (SD), so setting each cell's rest changes nothing (mean Jaccard over the
15 odor pairs 0.42 against 0.43). Responses follow each cell's summed PN input instead: the fifth of cells with the
least respond to 0.9% of the odors, the fifth with the most to 43%, and the 113 cells that respond to all six have 1.9
times the PN weight of those that respond to none. Summed PN weight varies with a CV of 0.46; alpha'/beta' cells get
about 60% of the others' (a median of 22 against 35-38) and respond least; two untyped Kenyon cells get 7 times the
typical weight and answer every odor. Independent responses at the same shares would leave no cell answering all six
odors and 2 answering five; here 113 and 206 do, and each cell answers 12 +- 28% of the odors (flies: 6 +- 12%).
Turner's 5.6 mV spread of rest, drawn independently of input, makes it worse (mean Jaccard 0.52; 218 cells answer every
odor): flies have that spread yet sparse, odor-specific responses, so their excitability must offset their input, as
Abdelrahman et al. argue. Equal PN input within each type helps only a little (mean Jaccard 0.37; 3-octanol and
4-methylcyclohexanol at 0.28, with 76% of the latter's responders also answering the former; 86 cells answer all six),
because the odors' drives stay correlated across cells (r = 0.71 for that pair): odor_probe12.py traces this to the
projection neurons' broad, fly-like responses. MBON11 gains 1-6 spikes as before (with Turner's spread, 4-15). The
resting brain stays at 0.96-0.98 Hz with nothing over 100 Hz.

    python experiments/odor_probe11.py         (writes experiments/odor_probe11.json, and the current model's per-cell
                                                data in experiments/odor_probe11.npz)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 40000
TURNER_GAP, TURNER_SD = 21.5, 5.6
CONDITIONS = {"current": {}, "per-cell rest": {"rest": "each"}, "per-cell rest, Turner's spread": {"rest": "spread"},
              "equal PN input": {"equal_input": True}, "equal PN input, per-cell rest": {"equal_input": True, "rest": "each"}}


def quintiles(x: np.ndarray, y: np.ndarray) -> list:
    """y's mean in each quintile of x (ties broken by rank)."""
    q = np.argsort(np.argsort(x, kind="stable"), kind="stable") * 5 // len(x)
    return [{"x": [round(float(x[q == k].min()), 3), round(float(x[q == k].max()), 3)], "mean": round(float(y[q == k].mean()), 4)}
            for k in range(5)]


def independent(shares: np.ndarray) -> np.ndarray:
    """The distribution of the number of odors a cell responds to if each responded independently at these shares."""
    p = np.array([1.0])
    for s in shares:
        p = np.convolve(p, [1 - s, s])
    return p


def pn_input(o: p7.Olfaction) -> tuple:
    """Each Kenyon cell's PN input edges (and their Kenyon cell's slot), summed weight, connections and glomeruli."""
    b, kc = o.brain, np.flatnonzero(o.m["kc"])
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(o.pn_kc)
    slot = np.searchsorted(kc, b.idx[e])
    weight = np.bincount(slot, b.weights[e].astype(np.float64), len(kc))
    glom = np.unique(np.array([t.split("_")[0] for t in o.types[pre[e]]]), return_inverse=True)[1]
    pairs = np.unique(np.stack([slot, glom]), axis=1)
    return e, slot, pre, weight, np.bincount(slot, minlength=len(kc)), np.bincount(pairs[0], minlength=len(kc))


def equalize_input(o: p7.Olfaction) -> dict:
    """Scale each Kenyon cell's PN synapses so its summed PN weight is its type's median."""
    b, kc = o.brain, np.flatnonzero(o.m["kc"])
    e, slot, _, weight, _, _ = pn_input(o)
    target = np.zeros(len(kc))
    for t in np.unique(o.types[kc]):
        m = o.types[kc] == t
        target[m] = np.median(weight[m])
    factor = np.where(weight > 0, target / np.maximum(weight, 1e-12), 1.0)
    w = b.weights.copy()
    w[e] = (w[e] * factor[slot]).astype(w.dtype)
    b.weights, b._external_matrix = w, None
    return {"factor_percentiles": [round(float(x), 3) for x in np.percentile(factor[weight > 0], (5, 25, 50, 75, 95))]}


def set_each_rest(o: p7.Olfaction, gaps: np.ndarray, seed: int, rounds: int = 4) -> list:
    """Each Kenyon cell's bias set so it rests `gaps` mV below threshold (its own value), in `rounds` corrections."""
    b, kc = o.brain, np.flatnonzero(o.m["kc"])
    threshold = b.params[b.cls[kc[0]]]["threshold"]
    bias = o.own_bias()                                   # set_bias adds the ring's offsets back
    log = []
    for r in range(rounds + 1):
        gap = threshold - p3.rest_state(o.s, seed + r, True)["u"][kc]
        log.append({"mean": round(float(gap.mean()), 2), "sd": round(float(gap.std()), 2),
                    "mean_abs_error": round(float(np.abs(gap - gaps).mean()), 2)})
        if r < rounds:
            bias[kc] += gap - gaps
            b.set_bias(bias)
    print("Kenyon cells' rest, by round:", json.dumps(log), flush=True)
    return log


def prepare(o: p7.Olfaction, spec: dict, base: int) -> dict:
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    kc = np.flatnonzero(o.m["kc"])
    if spec.get("equal_input"):
        out["equal_input"] = equalize_input(o)
        out["kc_rest_recalibration"] = p3.set_kc_rest(o.s, o.m["kc"], o.types, o.own_bias(), base + 90)[-1]
    if spec.get("rest") == "each":
        out["kc_rest_each"] = set_each_rest(o, np.full(len(kc), TURNER_GAP), base + 80)
    elif spec.get("rest") == "spread":
        lo, hi = TURNER_GAP - 2.33 * TURNER_SD, TURNER_GAP + 2.33 * TURNER_SD
        gaps = np.clip(np.random.default_rng(base + 70).normal(TURNER_GAP, TURNER_SD, len(kc)), lo, hi)
        out["kc_rest_each"] = set_each_rest(o, gaps, base + 80)
    return out


def condition(o: p7.Olfaction, name: str, c: int) -> tuple[dict, dict]:
    base = SEED + 100 * c
    out = prepare(o, CONDITIONS[name], base)
    b, kc = o.brain, np.flatnonzero(o.m["kc"])
    threshold = b.params[b.cls[kc[0]]]["threshold"]
    out["rest"] = p7.rest_measures(o, base + 95)
    gap = threshold - p3.rest_state(o.s, base + 97, True)["u"][kc]
    e, slot, pre, pn_weight, pn_connections, n_glom = pn_input(o)
    cls = np.full(len(kc), "other", dtype=object)
    for cname, prefix in p7.CLASSES.items():
        cls[np.char.startswith(o.types[kc], prefix)] = cname
    out["odors"], responses, drive = {}, [], []
    for k, odor in enumerate(p7.ODORS):
        captured = {}

        def runner(o, odor, seed, seconds, after, silence=(), max_hz=p3.MAX_HZ):
            r = p7.run(o, odor, seed, seconds, after, silence, max_hz)
            captured.setdefault("turner", r)                      # measure_odor runs Turner's protocol first
            return r
        row, resp = p7.measure_odor(o, odor, base + k, base + 50 + k, runner=runner)
        out["odors"][odor] = row
        r = captured["turner"]
        rise = (r["odor"] / 0.5 - r["rest"]).mean(0)                # each neuron's rise in Hz over the odor
        responses.append(resp)
        drive.append(np.bincount(slot, b.weights[e] * rise[pre[e]], len(kc)))
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "evoked_spikes_0_1.4s")}), flush=True)
    R, D = np.array(responses), np.array(drive)
    shares, count = R.mean(1), R.sum(0)
    out["odors_per_cell"] = {"model": np.bincount(count, minlength=7).tolist(),
                             "independent": [round(float(x) * len(kc), 1) for x in independent(shares)],
                             "mean_share_of_odors": round(float(count.mean() / len(p7.ODORS)), 4),
                             "sd_share_of_odors": round(float((count / len(p7.ODORS)).std()), 4), "flies_turner": "6 +- 12%"}
    out["rest_gap_mv"] = {"all": [round(float(gap.mean()), 2), round(float(gap.std()), 2)],
                          **{cn: [round(float(gap[cls == cn].mean()), 2), round(float(gap[cls == cn].std()), 2)] for cn in p7.CLASSES},
                          "flies_turner": "21.5 +- 5.6"}
    out["response_probability_by_quintile"] = {"rest_gap_mv": quintiles(gap, R.mean(0)), "pn_weight": quintiles(pn_weight, R.mean(0)),
                                               "pn_glomeruli": quintiles(n_glom.astype(float), R.mean(0))}
    out["pn_input"] = {"weight": [round(float(pn_weight.mean()), 3), round(float(pn_weight.std()), 3)],
                       "connections": [round(float(pn_connections.mean()), 2), round(float(pn_connections.std()), 2)],
                       "glomeruli": [round(float(n_glom.mean()), 2), round(float(n_glom.std()), 2)],
                       "corr_weight_gap": round(float(np.corrcoef(pn_weight, gap)[0, 1]), 3)}
    out["pairs"] = {}
    for i, j in combinations(range(len(p7.ODORS)), 2):
        both = (R[i] & R[j]).sum()
        out["pairs"][f"{p7.ODORS[i]} | {p7.ODORS[j]}"] = {
            "jaccard": round(float(both / max((R[i] | R[j]).sum(), 1)), 3),
            "share_of_first_in_second": round(float(both / max(R[i].sum(), 1)), 3),
            "share_of_second_in_first": round(float(both / max(R[j].sum(), 1)), 3),
            "drive_correlation": round(float(np.corrcoef(D[i], D[j])[0, 1]), 3)}
    out["mean_jaccard"] = round(float(np.mean([p["jaccard"] for p in out["pairs"].values()])), 3)
    out["by_odors_responded"] = {int(n): {"cells": int((count == n).sum()), "gap_mv": round(float(gap[count == n].mean()), 2),
                                          "pn_weight": round(float(pn_weight[count == n].mean()), 3),
                                          "glomeruli": round(float(n_glom[count == n].mean()), 2),
                                          "classes": {cn: int(((count == n) & (cls == cn)).sum()) for cn in p7.CLASSES}}
                                 for n in np.unique(count)}
    cells = {"responses": R, "drive": D, "gap": gap, "pn_weight": pn_weight, "pn_connections": pn_connections,
             "glomeruli": n_glom, "cls": cls.astype(str)}
    return out, cells


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    out = {"question": __doc__, "flies": p7.FLIES, "kc": int(o.m["kc"].sum()), "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name], cells = condition(o, name, c)
        if name == "current":
            np.savez_compressed(OUT.with_suffix(".npz"), **cells)
        e = out["conditions"][name]
        pair = e["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": e["rest"], "mean_jaccard": e["mean_jaccard"], "oct_mch": pair,
                                "odors_per_cell": e["odors_per_cell"]["model"], "rest_gap_mv": e["rest_gap_mv"]["all"]}),
              f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
