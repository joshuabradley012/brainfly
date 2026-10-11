"""Exploratory probe, not pre-registered: odor_probe56.py's model with tonic presynaptic inhibition at rest. Does it bring
the projection neurons' resting state toward flies' and keep their transform, and what does it do to
4-methylcyclohexanol's breadth and the Kenyon cells?

research_notes/Rung 9 learning data/orn_pn_resting_state.md (2026-10-10): flies' antennal lobe inhibits at rest. Blocking
GABA receptors (picrotoxin with CGP54626) depolarizes PNs by about 5-8 mV with no odor (Nagel, Hong & Wilson 2015; DM6,
VM2 and VM7), and their model, whose presynaptic inhibition divides release by the LNs' resting rate (a divisor of about
4-5, not fitted), reproduces it. Kazama & Wilson 2008's DM4 comparison, which odor_probe27.py read as "little tonic
presynaptic inhibition", allows a divisor up to about 2.6 at one standard error with DM4's own depression (2.9 at two
with brainfly's synapse). Olsen & Wilson 2008's own supplement shows CGP54626 alone leaving the pre-odor EPSCs unchanged
(one cell rose 25% only with picrotoxin added), so the tonic part would act through the fast, picrotoxin-sensitive
component. odor_gaba_block_check.py: blocking GABA raises odor_probe56.py's PNs only 3.1 mV in those glomeruli, all of it
postsynaptic, and silencing every receptor neuron drops them 24.8 mV (flies about 7-10). pn_toy.py: a tonic divisor of
2-2.5 gives a DM4-like PN flies' resting drive at DM4's measured rate and keeps or steepens the transform.
Model: odor_probe56.py's build with every installation of the presynaptic inhibition (odor_probe28.apply) carrying a fifth
trace, the fast (GABA-A) trace again, acting from zero with k_t = (2 - 1) / the inhibitors' summed target rate, the same
at every installation, so that the synapses rest divided by 2 (release and depletion, as Nagel et al.'s) once the
polishes bring the LNs to their targets; from the first resting calibration on (which estimates each neuron's resting
receptor input at that gain), so the LNs' and PNs' biases are set with it. The evoked part is fitted as before (odor_probe27.fit, four rounds) to Olsen &
Wilson's EPSCs relative to the resting divisor, with CGP54626 leaving the tonic term in place; the rest check raises the
evoked terms' offset as before. (A first build took k_t from the LNs' rate measured before the resting calibration
and again at the fit, from the polished rate; the change sent the PNs to 42 spikes/s, which the last PN polish brought
only to 12 (9.96 at rest, LNs 2.7 Hz against 4.3), and its measures stopped at the Kenyon cells on a four-trace
assumption in odor_probe30.course. Its resting state: receptor neurons silenced, -18.6 mV; GABA blocked, +2.45 mV in
DM6, VM2 and VM7.) The rested unitary EPSP stays Kazama & Wilson's 6.19 mV, which their cut-nerve
preparation (release probability 0.79) measured with little or no tonic inhibition.
Measured as odor_probe56.py measures (PN rest, LNs, Olsen's protocol, Kenyon cells and MBON11, 4-methylcyclohexanol
against 3-octanol with DoOR's and the weighed input), and odor_gaba_block_check.measure (GABA block, receptor neurons
silenced, resting efficacy). Seeds 770000.
Adopted as the base, by a rule set before the run, if the resting state moves toward flies' (the drop with every
receptor neuron silenced and the rise with GABA blocked, in DM6, VM2 and VM7, both closer to flies' 7-10 and 5-8 mV)
without the transform getting worse (each glomerulus's sigma within 2 of odor_probe56.py's or nearer flies', Rmax no
lower than 0.85 of it, 0.35-0.55 of the peak left at 500 ms), the PNs resting at 4-6 spikes/s and the GABAergic LNs
within 2x of their targets, and the weighed input's 4-methylcyclohexanol summed response on the reliable glomeruli not
smaller against 3-octanol's (odor_probe56.py: 0.64).

Ran: not adopted, and tonic presynaptic inhibition isn't what this model lacks. Built cleanly (resting divisor 1.94, PNs
at 5.32 spikes/s, GABAergic LNs at 3.84), with the fit finding the tonic term alone enough for Olsen & Wilson's
CGP54626 fractions (k_A 7e-5, k_B 0.0141). Silencing every receptor neuron drops the PNs 18.9 mV in DM6, VM2 and VM7
(odor_probe56.py 27.3), 17.4 over all (24.8), DM4 8.9 (13.2), DL5 12.5 (19.0), DM1 12.2 (18.3); blocking GABA raises them
3.8 mV in those glomeruli (3.1); both move toward flies', as the rule asked. But DL5's sigma rose 2.9, past the rule's 2:
12.6 to 15.5 (flies 11.8), though its weak end barely moved (27 and 56 spikes/s at 5 and 10 spikes/s of input, against 28
and 59) while its Rmax rose from 136 to 154 (flies 167). The others: sigma DM4 18.2, VM7d 17.1, DM1 14.3 (13.5, 15.4, 11.2;
flies 16.3, 12.4, 44.8), Rmax 106, 163, 148 (90, 141, 132; flies 170, 163, 144), 0.41-0.50 of the peak left at 500 ms
(flies 0.44). 4-methylcyclohexanol gains little: against 3-octanol 0.555 at the PNs (0.54) with DoOR's input and 0.227
(0.212) with the weighed input, 0.177 at the Kenyon cells with the weighed input (0.16; responders 45.5 against 250.8 per
fly), MBON11 57.0 and 9.8 spikes (55 and 7.6). And the PNs' free membrane potential, added to the measure after the run
began (the membrane resets at each spike, so its mean saturates as the rate rises: here 5 to 37 spikes/s with GABA
blocked), says the 3.8 mV is 13.2, twice flies' 5-8, where odor_probe56.py's PNs rise 5.2 (odor_gaba_block_check.py,
checked afterwards), already inside flies' range. So flies' resting disinhibition is the model's postsynaptic GABA
alone, and a tonic divisor overshoots it; the excess resting drive (by the free potential 28.4 mV in those glomeruli in
odor_probe56.py, 20.2 here) has to come down another way: measured spontaneous rates (odor_probe58.py), or deeper
depression at low rates.

    python experiments/odor_probe57.py      (writes experiments/odor_probe57.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

import al_cells
import brain_cache
import odor_offset_check as oc
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe27 as p27
import odor_probe28 as p28
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe44 as p44
import odor_probe51 as p51
import odor_probe56 as p56
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED, WEIGHED_SEED, WEIGHED_EQUALIZATION_SEED = 770000, 771000, 772000, 773000
RESTING_DIVISOR = 2.0
TAUS = p28.TAUS + (p28.TAUS[1],)                 # the fifth trace: the GABA-A trace again (second stage of trace 0)
SOURCE = p28.SOURCE + (0,)


TONIC = {"k_t": None}


def tonic_k(o, mk: dict) -> float:
    """(RESTING_DIVISOR - 1) / the inhibitors' summed target rate: the same at every installation, so that the divisor
    is RESTING_DIVISOR wherever the polishes bring the LNs to their targets."""
    return (RESTING_DIVISOR - 1.0) / float(o.s.target[mk["inhibitors"]].sum())


def apply(o, mk: dict, base_w, base_sw, k_a: float, k_b: float, a_rest: float) -> None:
    """odor_probe28.apply with the tonic trace, k_t from tonic_k, acting from zero."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    TONIC["k_t"] = k_t = tonic_k(o, mk)
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=TAUS, k=(0.0, k_a, 0.0, k_b, k_t),
                      start=a_rest, offset=(a_rest,) * 4 + (0.0,), source=SOURCE, depleting=np.flatnonzero(o.m["orn"]))


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, dict]:
    """odor_probe27.fit relative to the resting divisor 1 + k_t a_rest, k_t as installed, the tonic term following the
    GABA-A trace (e[..., 0]) and left in place by CGP54626."""
    k_t = TONIC["k_t"]
    tonic = k_t * e[..., 0].mean(0)
    d0 = 1.0 + k_t * a_rest
    da = np.maximum(e[..., 0].mean(0) - a_rest, 0.0)
    db = np.maximum(e[..., 1].mean(0) - a_rest, 0.0)
    cgp, ctl = -np.log(np.array(p21.OLSEN_CGP)), -np.log(np.array(p21.OLSEN_CONTROL))
    k_a = minimize_scalar(lambda x: ((np.log((1 + tonic + x * da) / d0) - cgp) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    k_b = minimize_scalar(lambda x: ((np.log((1 + tonic + k_a * da + x * db) / d0) - ctl) ** 2).sum(), bounds=(0.0, 1.0),
                          method="bounded").x
    model = {"cgp_fraction": np.round(d0 / (1 + tonic + k_a * da), 3).tolist(),
             "control_fraction": np.round(d0 / (1 + tonic + k_a * da + k_b * db), 3).tolist(),
             "tonic_only_fraction": np.round(d0 / (1 + tonic), 3).tolist(),
             "trace_a_over_rest": np.round(e[..., 0].mean(0) / a_rest, 2).tolist(),
             "trace_b_over_rest": np.round(e[..., 1].mean(0) / a_rest, 2).tolist()}
    return float(k_a), float(k_b), model


def resting(o, rec, seed: int, inhibitors, k, offset) -> dict:
    """odor_offset_check.resting with the gain from the installed inhibition (its five traces and their own offsets)."""
    pres = o.brain._presynaptic
    return RESTING(o, rec, seed, inhibitors, np.asarray(pres["k"], float), np.asarray(pres["offset"], float))


RESTING = oc.resting


def recalibrate_rest(o, rec, mk, base_w, base_sw, gain_rest, seed):
    """odor_probe51.recalibrate_rest (which odor_probe51.build installs for the build) at the installed resting
    presynaptic gain; odor_probe44.py passes 1."""
    return RECALIBRATE(o, rec, mk, base_w, base_sw, warm.resting_gain(o.brain), seed)


RECALIBRATE = p51.recalibrate_rest


def build():
    """odor_probe56.build with the tonic trace in every installation of the presynaptic inhibition, and the first
    resting calibration at its resting gain."""
    saved = p28.apply, p27.fit, oc.resting, p51.recalibrate_rest
    p28.apply, p27.fit, oc.resting, p51.recalibrate_rest = apply, fit, resting, recalibrate_rest
    try:
        o, rec, out = p56.build()
    finally:
        p28.apply, p27.fit, oc.resting, p51.recalibrate_rest = saved
    pres = o.brain._presynaptic
    out["presynaptic"]["tonic"] = {"k_t": round(float(pres["k"][4]), 7), "inhibitors_target_hz": round(float(
        o.s.target[p21.masks(o)["inhibitors"]].sum()), 1), "resting_divisor_at_start": round(1.0 / warm.resting_gain(o.brain), 3)}
    out["presynaptic"]["k"] = [float(x) for x in pres["k"]]                   # all five traces, for the measures
    out["presynaptic"]["offset_hz"] = [float(x) for x in pres["offset"]]       # (odor_probe30.course takes per-trace offsets)
    return o, rec, out


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": json.loads(p40.OUT.read_text())["flies"], "resting_divisor": RESTING_DIVISOR}
    o, rec, built = brain_cache.load("odor_probe57", build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import odor_gaba_block_check as gb
    import odor_olsen_protocol_check as olsen
    import receptor_fills
    out["settling"] = o.settling
    out["mb_calibration"] = mb_calibration.apply(o)
    p40.ln_mask = lambda types: al_cells.alln(o)
    upn = np.flatnonzero(o.m["upn"])
    try:
        entry = {"build": {x: built[x] for x in ("build", "resting_recalibration", "presynaptic", "rest_check", "settles",
                                                "pn_rest_inhibited") if x in built}}
        out["condition"] = entry
        entry["resting_state"] = gb.measure(o, rec, SEED + 500)
        OUT.write_text(json.dumps(out, indent=1))
        with warm.tracking(o, rec) as held:
            rest = p10.resting(o, rec, SEED + 990)["hz"]
            entry["upn_rest_hz"] = {"mean": round(float(rest[upn].mean()), 2), "median": round(float(np.median(rest[upn])), 2)}
            print("PN rest", json.dumps(entry["upn_rest_hz"]), flush=True)
            entry["ln_response"] = p40.ln_measure(o, rec, SEED)
            lr = entry["ln_response"]
            print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_other_lns", "rest_hz_upns", "rms_log_error")}),
                  json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs",
                  json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:11]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry["olsen_protocol"] = olsen.measure(o, rec, protocols=("olsen",), show=False)
            t = entry["olsen_protocol"]["olsen"]
            print("fits", json.dumps({g: t[g]["cholinergic"]["fit"] for g in t}), "points", json.dumps({g: [t[g]["cholinergic"]["points"][x]["window_mean"]
                  for x in ("5", "10", "20", "40", "80", "160")] for g in t}),
                  "at 500 ms", json.dumps({g: t[g]["cholinergic"]["points"]["80"]["at_500ms_over_peak"] for g in t}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry.update(p36.measure(o, rec, built, SEED))
            print("KCs", json.dumps({od[:6]: r["kc_share_by_class"] for od, r in entry["odors"].items()}),
                  "MBON11", json.dumps({od[:6]: r["MBON11"] for od, r in entry["mbon11_input"].items()}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
            entry["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
            print("MCH/OCT (DoOR)", json.dumps(entry["equalization"]["mch_over_oct"]), flush=True)
            with receptor_fills.applied(recommended=True) as inputs:
                rec_entry = {"inputs": inputs, "equalization": eq.measure(o, rec, WEIGHED_EQUALIZATION_SEED)}
                print("MCH/OCT (weighed)", json.dumps(rec_entry["equalization"]["mch_over_oct"]), flush=True)
                OUT.write_text(json.dumps(out, indent=1))
                rec_entry.update(p36.measure(o, rec, built, WEIGHED_SEED))
                od = rec_entry["odors"]
                print("weighed: KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
                      "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
                      "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in rec_entry["mbon11_input"].items()}), flush=True)
            out["weighed_input"] = rec_entry
            entry["measure_settles"] = held["settles"]
    finally:
        p40.ln_mask = p44.PLAIN_LN_MASK
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
