"""Exploratory, not pre-registered: with the Kenyon cell-to-MBON11 synapses set from MBON11's own measurements instead
of rung 4's size rule, does MBON11 answer odors as flies' does?

Every probe so far leaves MBON-gamma1pedc>alpha/beta (MBON11) gaining a few to tens of spikes in the 1.4 s after an odor's
onset where Hige et al. 2015 counted 118 +- 8.3 (3-octanol) and 110 +- 11 (4-methylcyclohexanol), and MBON-alpha2sc
short too (flies about 71-85): rung 4 divides each synapse by its target's size, and the one unitary KC-to-MBON EPSP
the model matches (onto alpha2sc) was recorded in mecamylamine, which blocks these synapses in part (research_notes/Rung 9
learning data/mbon11_input.md). Two measurements on MBON11 itself set the synapse without Hige's counts: a 1 ms flash on
about 3-7% of the gamma Kenyon cells gives an EPSC of 80-117 pA, slow (half-width about 0.23 s), about 0.4-0.9 pC per
Kenyon cell, so about 0.019-0.042 pC per synapse over a gamma cell's 21.4 (Yamada et al. 2024, ex vivo, spikes per
flash not reported); and MBON11 fires 0.35-0.47 spikes/s more per pA of injected current (Wang et al. 2026, in vivo).
Together these predict that flies' sparse Kenyon cell activity (about 300 spikes/s onto MBON11) drives it about 80 Hz
above rest, as Hige et al. found, so the data agree with each other.
Model: odor_probe30.py's antennal lobe, built on the same seeds (so the same brain). MBON11's own gain is measured
first: its rate over 1 s of rest with its bias raised 0-8 mV in 2 mV steps (spontaneous receptor firing on), the slope
s in spikes/s per mV fitted over the steps. Then every Kenyon cell-to-MBON11 synapse is given the weight
w = 0.41 Hz/pA x q / (s x 5 ms), so that its mean drive, per spike of its Kenyon cell, matches q pC through Wang et al.'s
gain (the model's synaptic current decays over 5 ms), for q = 0.019, 0.030 and 0.042 pC per synapse; the synapses stay
undepressed, as in the current model. Measured for each q, over the six odors: MBON11's and alpha2sc's evoked spikes as
Hige et al. counted them (0-1.4 s, spontaneous rate subtracted), and the charge MBON11's Kenyon cell input carries in that
window (its Kenyon cells' spikes above their resting rate x their synapses onto it x q), against Hige et al.'s odor EPSC,
about 250-265 pC (a semi-independent check: the same experiments). Seeds 240000 for the build (odor_probe30.py's), 250000
for this probe's runs (+ 10 x step for the gain; + 100 x q index + odor for the odors).

    python experiments/odor_probe31.py         (writes experiments/odor_probe31.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe22 as p22
import odor_probe24 as p24
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe29 as p29
import odor_probe30 as p30
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 250000
GAIN_HZ_PER_PA = 0.41                            # Wang et al. 2026, mean of their four conditions' per-cell slopes
CHARGES_PC = (0.019, 0.030, 0.042)               # per synapse (Yamada et al. 2024, derived)
STEPS_MV = (0.0, 2.0, 4.0, 6.0, 8.0)
HIGE = {"3-octanol": (118, 8.3), "4-methylcyclohexanol": (110, 11)}


def build() -> tuple:
    """odor_probe30.main's model, up to its measurements, on its seeds."""
    p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
    p21.masks = p29.pn_only_masks
    o = p7.Olfaction()
    b = o.brain
    out = {"build": p21.build(o)}
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], p30.SEED + 930)
    p28.apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)
    p10.POLISH, schedule = p27.FIRST_POLISH, p10.POLISH
    try:
        out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0, p30.SEED + 600)
    finally:
        p10.POLISH = schedule
    out["pn_rest"] = p27.pn_polish(o, rec, p30.SEED + 700)
    rec.kinetics = "fast"
    out["presynaptic"] = p30.calibrate(o, rec, mk, base_w, base_sw)
    out["second_polish"] = p24.polish(o, rec, p30.SEED + 640, p27.SECOND_POLISH)
    out["pn_rest_after"] = p27.pn_polish(o, rec, p30.SEED + 800, rounds=6)
    return o, rec, out


def mbon_gain(o: p7.Olfaction, rec: p10.Receptors, cells: np.ndarray) -> dict:
    """MBON11's resting rate with its bias raised by each step; the slope fitted over the steps."""
    b = o.brain
    base = o.own_bias()
    rates = []
    for k, d in enumerate(STEPS_MV):
        bias = base.copy()
        bias[cells] += d
        b.set_bias(bias)
        rates.append(float(p10.resting(o, rec, SEED + 10 * k)["hz"][cells].mean()))
    b.set_bias(base)
    slope = float(np.polyfit(STEPS_MV, rates, 1)[0])
    return {"steps_mv": list(STEPS_MV), "rate_hz": [round(r, 2) for r in rates], "slope_hz_per_mv": round(slope, 3)}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, out = build()
    out["question"] = __doc__
    b, m, types = o.brain, o.m, o.types
    mbon11 = np.flatnonzero(types == "MBON11")
    gain = mbon_gain(o, rec, mbon11)
    out["mbon11_gain"] = gain
    print("MBON11 gain", json.dumps(gain), flush=True)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    edges = m["kc"][pre] & np.isin(b.idx, mbon11)
    counts = b._counts[edges].astype(np.float64)
    w0 = b.weights.copy()
    per_kc_syn = np.bincount(pre[edges], weights=counts, minlength=b.n)          # each KC's synapses onto MBON11
    out["kc_to_mbon11"] = {"edges": int(edges.sum()), "synapses": int(counts.sum()), "kcs": int((per_kc_syn > 0).sum()),
                           "weight_per_synapse_before_mv": round(float((w0[edges] / counts).mean()), 4)}
    runner = p10.make_runner(rec)
    out["conditions"] = {}
    for qi, q in enumerate(CHARGES_PC):
        w_syn = GAIN_HZ_PER_PA * q / (gain["slope_hz_per_mv"] * p21.TAU)
        w = w0.copy()
        w[edges] = counts * w_syn
        b.weights, b._external_matrix = w, None
        row = {"charge_pc_per_synapse": q, "weight_per_synapse_mv": round(w_syn, 4),
               "unitary_psp_per_kc_mv": round(float(p21.p3.PEAK * w_syn * per_kc_syn[per_kc_syn > 0].mean()), 3), "odors": {}}
        for j, odor in enumerate(p7.ODORS):
            h = runner(o, odor, SEED + 100 * qi + j, 1.0, 0.4)
            types_ = types
            evoked = h["window"] - 1.4 * h["rest"]
            kc_extra = np.maximum((h["window"] - 1.4 * h["rest"]).mean(0), 0.0)        # spikes above rest, per KC
            charge = float((kc_extra * per_kc_syn).sum() * q)
            row["odors"][odor] = {"MBON11": round(float(evoked[:, mbon11].mean()), 1),
                                  "MBON18": round(float(evoked[:, types_ == "MBON18"].mean()), 1),
                                  "kc_input_charge_pc": round(charge, 1)}
            print(f"q {q}", odor, json.dumps(row["odors"][odor]), flush=True)
        out["conditions"][f"{q:g}"] = row
        OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = w0, None
    out["flies"] = {"hige_2015_mbon11_spikes": HIGE, "hige_2015_alpha2sc_spikes": "about 71-85", "odor_epsc_charge_pc": "about 250-265"}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
