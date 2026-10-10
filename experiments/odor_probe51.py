"""Exploratory, not pre-registered: with the receptor synapses depressing as the two pools Kazama & Wilson's and Nagel et
al.'s trains call for, do the PNs answer strong input as lastingly as flies' do?

odor_probe49.py (the base model, settled properly): 3-octanol's PNs fall to 0.20 of their peak at 0.40-0.45 s (flies 0.48)
and the transform's Rmax is 132-134 (flies 144-170). Measured as Olsen et al. measured flies (odor_olsen_protocol_check.py,
cholinergic PNs), its sigma is near flies' (DL5 15.6, VM7d 19.9, DM4 20.3; flies 11.8, 12.4, 16.3) and weak responses
keep flies' shape (0.42-0.59 of the peak at 500 ms; flies 0.42), but strong ones fall to 0.17-0.35 of their peak (flies
0.44) and every response is about half to two thirds of flies' (Rmax 81-118; flies 163-170). The receptor synapses
depress as one pool (0.78 of the strength left per spike, recovering over 0.893 s: Nagel et al. 2015's fit to 10-Hz
trains), which sits at about 0.4 of its strength at rest and saturates at about 5 full-strength releases per second per
receptor neuron whatever its rate, so a strong odor adds little lasting drive above rest. No single pool fits the
measured trains and recoveries (research_notes/Rung 9 learning data/orn_pn_depression.md: recovery after a 7-Hz train
over 7.5 s, after 50-200 Hz trains over about 0.4 s); two pools in parallel, each half the synapse (0.67 of it left per
spike, recovering over 0.3 s; 0.83, 7.5 s), halve the best single pool's misfit, rest at 0.37 of full strength at 6
spikes/s, 0.32 at 8 and 0.19 at 19 (one pool: 0.46, 0.39, 0.21), and should add about a third more lasting drive above
rest at odor rates (derived), at the cost of a slightly smaller onset.
Model: odor_probe49.py's build with the receptor neurons' fast synapses depressing as those two pools (HybridBrain's
second pool), the resting recalibration taking their resting strength as the two pools'; the slow component as before.
Cached as odor_probe51; measured with mb_calibration.py's mushroom body.
Measured: as odor_probe49.py, on its seeds (550000 for odor_probe36.measure and odor_probe40.ln_measure, 560000 for the
equalization), and the transform as odor_olsen_protocol_check.py measures it (Olsen et al.'s protocol, its seeds 570000).

    python experiments/odor_probe51.py         (writes experiments/odor_probe51.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import al_cells
import brain_cache
import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe44 as p44
import odor_probe49 as p49
import odor_probe10 as p10
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 550000, 560000
POOLS = {"depression": 0.67, "recovery": 0.3, "depression2": 0.83, "recovery2": 7.5, "share2": 0.5}


def resting_strength(p: dict, rate: np.ndarray, gain: float) -> np.ndarray:
    """The fast synapses' mean strength at Poisson rate `rate`, one pool or two."""
    one = lambda f, tau: 1.0 / (1.0 + rate * tau * (1 - f) * gain) if f < 1 else np.ones_like(rate)
    first = one(p["depression"], p["recovery"])
    if p.get("share2", 0.0) > 0:
        return (1 - p["share2"]) * first + p["share2"] * one(p["depression2"], p["recovery2"])
    return first


def recalibrate_rest(o, rec, mk: dict, base_w: np.ndarray, base_sw: np.ndarray, gain_rest: float, seed: int) -> dict:
    """odor_probe24.recalibrate_rest with the fast component at its two pools' resting strength."""
    b, m = o.brain, o.m
    orn0 = b.cls[np.flatnonzero(m["orn"])[0]]
    p = b.params[orn0]
    fs, rec_s = p["slow_depression"], p["slow_recovery"]
    rate = np.zeros(b.n)
    for g, cells in rec.cells.items():
        rate[cells] = rec.spont[g]
    left_f = resting_strength(p, rate, gain_rest)
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
    log.update(p24.polish(o, rec, seed, p10.POLISH))
    return log


def build() -> tuple:
    """odor_probe49.build with the receptor neurons' fast synapses as two pools from odor_probe21.build on."""
    plain_build, plain_rest = p21.build, p24.recalibrate_rest

    def two_pools(o):
        out = plain_build(o)
        b = o.brain
        b.set_type("ORN", **POOLS)
        orn = np.flatnonzero(o.m["orn"])
        assert all(b.params[c]["share2"] == POOLS["share2"] for c in np.unique(b.cls[orn]))
        out["receptor_pools"] = dict(POOLS)
        return out
    p21.build, p24.recalibrate_rest = two_pools, recalibrate_rest
    try:
        return p49.build()
    finally:
        p21.build, p24.recalibrate_rest = plain_build, plain_rest


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "pools": POOLS}
    o, rec, built = brain_cache.load("odor_probe51", build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_olsen_protocol_check as olsen
    out["settling"] = o.settling
    out["mb_calibration"] = mb_calibration.apply(o)
    p40.ln_mask = lambda types: al_cells.alln(o)
    try:
        with warm.tracking(o, rec) as held:
            entry = {"build": {x: built[x] for x in ("build", "resting_recalibration", "presynaptic", "rest_check", "settles")
                               if x in built},
                     "ln_response": p40.ln_measure(o, rec, SEED)}
            lr = entry["ln_response"]
            print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
                  json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs",
                  json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:11]), flush=True)
            out["condition"] = entry
            OUT.write_text(json.dumps(out, indent=1))
            entry["olsen_protocol"] = olsen.measure(o, rec, protocols=("olsen",))
            OUT.write_text(json.dumps(out, indent=1))
            entry.update(p36.measure(o, rec, built, SEED))
            print("KCs", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                  "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in entry["mbon11_input"].items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = p44.PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
