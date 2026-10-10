"""Exploratory, not pre-registered: with presynaptic inhibition of the receptor terminals set from flies' measurements,
does the antennal lobe transform receptor input as flies' does?

odor_probe20.py: inhibition low-passed over 1 s alone barely acts within half a second, and was set without a measured
magnitude. research_notes/Rung 9 learning data/presynaptic_inhibition.md now has one: during a lateral odor an ORN-evoked
EPSC in a PN falls to 27% of its baseline at 0.32 s and 32-37% later (Olsen & Wilson 2008, Fig. 3c, n = 12), and with
GABA-B blocked to 52% and then 68-81% (n = 5); GABA-B's part decays over about 1 s, GABA-A's within 0.25 s, and the
inhibition's onset follows LN spikes as an alpha function of about 25 ms (Nagel, Hong & Wilson 2015). Flies' LNs, like
the model's, fire a burst at odor onset (about 43 spikes/s) and then 6-8.
Model, both conditions: odor_probe18.py's antennal lobe (no cholinergic LN-to-PN synapses; Nagel et al.'s two-component
receptor synapse, its slow part depressing as measured) with two corrections: the receptor synapses' rested unitary
EPSP brought back to Kazama & Wilson's 6.19 mV (odor_probe17.py added the slow part on top of a fast weight already set
to the whole EPSP, 1.11 times too strong), and the removal's lost input averaged over 4 rest windows (the resting
antennal lobe has brief LN population bursts, so one window's mean varied 0.43-1.55 mV between probes).
  base          no presynaptic inhibition
  presynaptic   every receptor-neuron output (fast; its terminals' release sites contact PNs and LNs alike) and their
                slow synapses onto uniglomerular PNs divided by 1 + k_A A_A + k_B A_B, where A_A and A_B are the 90
                GABAergic antennal lobe LNs' summed rate filtered as GABA-A (a difference of 40 and 15 ms exponentials,
                peaking at 23.5 ms like Nagel's alpha function) and as GABA-B (decaying over 1 s), each starting at its
                resting value. k_A is fitted to Olsen & Wilson's GABA-B-blocked EPSCs and then k_B to their control
                EPSCs (least squares on the log divisor relative to rest, at their four sample times less the valve's
                75 ms delay), with five broad training odors (none of the six test odors) as the lateral odor, iterated
                four times since the inhibition also acts on the LNs' own input. The inhibited synapses are multiplied
                by the resulting resting divisor, so that at rest they carry the strength they were calibrated to
                (Kazama & Wilson measured in vivo, under tonic inhibition).
Measured as odor_probe17.py measures (Olsen's transform, the odors' PN, Kenyon cell and MBON responses, the resting
brain), plus the driven PNs' and the LNs' rates in 50 ms bins over 1 s of 3-octanol and 4-methylcyclohexanol, and the
synapses' strength relative to rest. Seeds 140000: + 900 the Kenyon cells' rest, + 997-1000 the removal's rest windows,
+ 940-943 the LNs' resting rate, + 960-994 the calibration's odors; per condition c, + 1000 c (+ 10 x glomerulus + rate
for the transform; + odor for Turner's protocol, + 50 + odor for Hige's, + 700 + odor for the time courses, + 995 for
the resting brain).

Ran: the measured inhibition divides each glomerulus by the others, as flies' does, and halves the Kenyon cells'
density, but leaves one glomerulus alone saturating at twice flies' rate, and the PNs still don't accommodate.
  base          as odor_probe18.py: Rmax 208, 332, 343 and 326 spikes/s for DM4, DL5, VM7d and DM1 (Olsen 170, 167, 163,
                144), sigma 18, 12, 11 and 12 (16, 12, 12, 45); lateral input at 20 Hz in every other glomerulus leaves
                0.96-1.01 of the response (DM4 1.13-1.30). The driven PNs climb through an odor (3-octanol: 173 Hz in
                its first 50 ms, 264 from 400 ms on); 242-263 Hz in the first 100 ms and 305-330 over a whole 1 s odor
                (flies 100-200 at onset, then about half by 500 ms). 25-61% of Kenyon cells respond (flies 6 +- 5%),
                mean Jaccard 0.60; MBON11 gains 41-98 spikes and MBON-alpha2sc 56-132 (flies 110-118 and about 71-85).
  presynaptic   The 90 GABAergic LNs fire 201 spikes/s between them at rest. The fit gives k_A = 0.00086 and
                k_B = 0.0164 per spike/s, a resting divisor of 4.46 (Nagel et al.'s model, by its own construction, has
                4-5), and EPSCs during the lateral odors at 0.31-0.33 of baseline (flies 0.27-0.37), 0.57-0.76 with
                GABA-B blocked (0.52-0.81), and 0.32-0.33 with GABA-A blocked, as in flies (the same as control).
                Lateral input now divides every glomerulus's response, to 0.36-0.60, more for weaker direct input, as
                Olsen et al.'s input-gain model has it (their fits imply roughly 0.3-0.9 at a similar lateral load,
                derived). But alone the glomeruli barely change: Rmax 200, 300, 331 and 304, sigma 19, 11, 11 and 12. In
                odors the driven PNs fire 195-214 Hz in the first 100 ms and 208-242 over 1 s, about a quarter less, and
                still climb (3-octanol: 143 Hz in the first 50 ms, 181 from 400 ms on): the synapses fall to about a third
                of their resting strength within 100 ms (0.31-0.34), as the LNs' onset burst (5,300-6,200 spikes/s in
                the first 50 ms) fills the GABA-B trace at once, and stay near it (0.33-0.44 to the end). 10-36% of Kenyon cells respond (alpha/beta 11-47%,
                alpha'/beta' 2-13%, gamma 12-35%; flies about 3-8, 9-14 and 2), still with 5-9 spikes per response
                (flies 2.2-4.9); mean Jaccard 0.40, and 131 cells answer all six odors (654 in base). MBON11 gains 13-46
                spikes and MBON-alpha2sc 19-72. PNs stay about as broad as flies' (37-59% by Turner's criterion, 59 +-
                14%) and rest at 3.6 Hz; the resting brain is unchanged (0.98 Hz).
The two gaps have different causes. One glomerulus recruits few LNs, so inhibition can't set its saturation
(odor_presynaptic_sweep.py: inhibition strong enough to cut an odor's synapses to 5-24% lowers DL5's Rmax only from 351
to 275); Olsen et al. attribute it to the synapses' depression and the PNs' relative refractory period, which the model's
PNs lack (an absolute 2.2 ms only). The accommodation needs the inhibition to lag the LNs' burst, as flies' does by about
100 ms (odor_probe22.py); measured receptor kinetics alone don't do it (odor_receptor_course.py).

    python experiments/odor_probe21.py [condition ...]    (writes experiments/odor_probe21.json; all conditions if none named)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import odor_probe14 as p14
import odor_probe17 as p17
import odor_probe18 as p18
import odor_probe3 as p3
import odor_probe7 as p7
from brainfly import odors
from brainfly.hybrid import consensus_transmitters
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED = 140000
REST_SEEDS = 4                                   # rest windows averaged for the removal's lost input (al_rest_noise)
CONDITIONS = ("base", "presynaptic")
# Presynaptic inhibition's traces (s): GABA-A's onset as Nagel et al. 2015's alpha function (tau ~25 ms), drawn as a
# difference of exponentials (40 and 15 ms, peaking at 23.5 ms; Olsen & Wilson 2008: gone within 0.25 s of the odor's
# end); GABA-B decaying over 1 s (Olsen & Wilson 2008's tail after the odor, 0.8-1.4 s)
TAU_A, TAU_A_RISE, TAU_B = 0.040, 0.015, 1.0
# Olsen & Wilson 2008 Fig. 3c: an ORN-evoked EPSC during a lateral odor, as a fraction of its baseline (control n = 12;
# CGP54626, GABA-B blocked, n = 5), at 0.32, 0.57, 0.82 and 1.07 s after odor onset (read off the figure)
OLSEN_T = (0.32, 0.57, 0.82, 1.07)
OLSEN_CONTROL = (0.27, 0.32, 0.33, 0.37)
OLSEN_CGP = (0.52, 0.68, 0.77, 0.81)
VALVE_DELAY = 0.075                              # s from odor onset at the valve to the ORNs' response (Bhandawat 2007)
LATERAL = ("1-hexanol", "pentyl acetate", "propyl acetate", "2,3-butanedione", "e2-hexenal")   # training odors only
COURSE_ODORS = ("3-octanol", "4-methylcyclohexanol")
BIN = 0.05                                       # s, the PNs' time course


def combined_peak_ratio(tau_m: float, tau_fast: float = TAU, tau_slow: float = p17.SLOW_TAU,
                        charge: float = p17.SLOW_CHARGE) -> float:
    """The rested unitary PSP's peak with the slow component (charge x the fast one's, decaying with tau_slow) over its
    peak with the fast component alone: what odor_probe17.py's slow synapses added on top of a fast weight already set
    to Kazama & Wilson's whole 6.19 mV."""
    t = np.arange(0.0, 0.3, 1e-5)
    psp = lambda tau_i: tau_i / (tau_i - tau_m) * (np.exp(-t / tau_i) - np.exp(-t / tau_m))
    fast = psp(tau_fast)
    slow = charge * tau_fast / tau_slow * psp(tau_slow)
    return float((fast + slow).max() / fast.max())


def remove_averaged(o: p7.Olfaction, edges: np.ndarray, seed: int) -> dict:
    """odor_probe14.remove with the resting rates averaged over REST_SEEDS rest windows: the resting antennal lobe has
    brief local-neuron population bursts in about one trial-second in five, so one window's mean varies by a factor of two."""
    b = o.brain
    rate = np.mean([p3.rest_state(o.s, seed + r, False)["counts"].mean(0) for r in range(REST_SEEDS)], axis=0)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    lost = np.bincount(b.idx[edges], weights=rate[pre[edges]] * b.weights[edges] * TAU, minlength=b.n)
    w = b.weights.copy()
    w[edges] = 0.0
    b.weights, b._external_matrix = w, None
    b.set_bias(o.own_bias() + lost)
    upn = o.m["upn"]
    return {"edges": int(edges.sum()), "rest_windows": REST_SEEDS,
            "lost_mean_input_mv": {"upn_mean": round(float(lost[upn].mean()), 3), "upn_max": round(float(lost[upn].max()), 3)}}


def build(o: p7.Olfaction) -> dict:
    """odor_probe18.py's antennal lobe (no cholinergic LN-to-PN synapses; Nagel et al.'s two-component receptor synapse,
    the slow component depressing as measured), with the receptor synapses' rested unitary EPSP brought back to 6.19 mV
    and the removal's lost input averaged over several rest windows. Returns what was set, and the masks used later."""
    types, m, b = o.types, o.m, o.brain
    out = {"kc_rest_calibration": o.set(p7.CURRENT, SEED + 900)}
    out["removed"] = remove_averaged(o, p14.cholinergic_ln_edges(o), SEED + 997)
    out["slow"] = p17.add_slow_receptor_synapses(o)
    b.slow_full[:] = False
    b.sets["ORN"] = np.flatnonzero(m["orn"])
    b.set_type("ORN", slow_depression=p18.SLOW_DEPRESSION, slow_recovery=p18.SLOW_RECOVERY)
    upn_tau = float(b.params[b.cls[np.flatnonzero(m["upn"])[0]]]["tau_m"])
    ratio = combined_peak_ratio(upn_tau)
    fast = o.orn_pn & (b.weights > 0)
    w = b.weights.copy()
    w[fast] /= ratio
    b.weights, b._external_matrix = w, None
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    slow = m["orn"][spre] & m["upn"][b.sidx]
    b.slow_weights = b.slow_weights.copy()
    b.slow_weights[slow] /= ratio
    out["unitary"] = {"combined_over_fast_peak": round(ratio, 4), "pn_tau_m_s": upn_tau, "fast_edges": int(fast.sum()),
                      "slow_edges": int(slow.sum())}
    out["kc_rest_recalibration"] = p3.set_kc_rest(o.s, m["kc"], types, o.own_bias(), SEED + 900)[-1]
    return out


def masks(o: p7.Olfaction) -> dict:
    """The inhibitors (GABAergic antennal lobe LNs) and the inhibited synapses: every output of the receptor neurons,
    fast, and their slow synapses onto uniglomerular PNs. Presynaptic inhibition acts on the receptor terminals, whose
    release sites each contact several partners (PNs and LNs alike), so it can't spare some targets."""
    b, m = o.brain, o.m
    nt = np.asarray(consensus_transmitters())
    gaba_ln = np.flatnonzero(np.array([bool(p14.LN.match(t)) for t in o.types]) & (nt == "gaba"))
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    spre = np.repeat(np.arange(b.n), np.diff(b.sptr))
    return {"inhibitors": gaba_ln, "fast": m["orn"][pre] & (b.weights != 0), "slow": m["orn"][spre] & m["upn"][b.sidx]}


def course(o: p7.Olfaction, odor: str, seed: int, pns_of_odor: np.ndarray, inhibitors: np.ndarray, k: np.ndarray,
           d_rest: float = 1.0) -> dict:
    """1 s to settle, 1 s of rest, the odor for 1 s: the driven PNs' rate and the inhibitors' summed rate per BIN, and
    the inhibited synapses' strength relative to rest, d_rest / (1 + sum k A), at each bin's end (1 if it's off)."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))
    drive = odors.orn_drive(b, odor)
    pn, inh, gain = [], [], []
    for _ in range(int(round(1.0 / BIN))):
        c = b.advance(int(round(BIN / b.dt)), drive=drive)
        pn.append(float(c[:, pns_of_odor].mean() / BIN))
        inh.append(float(c[:, inhibitors].sum(1).mean() / BIN))
        a = b.presynaptic_state
        gain.append(float((d_rest / (1.0 + (a * k).sum(1))).mean()) if a.shape[1] else 1.0)
    return {"bin_s": BIN, "rest_pn_hz": round(float(rest[:, pns_of_odor].mean()), 2),
            "rest_inhibitors_hz": round(float(rest[:, inhibitors].sum(1).mean()), 1),
            "pn_hz": [round(x, 1) for x in pn], "inhibitors_hz": [round(x, 1) for x in inh], "gain": [round(x, 4) for x in gain]}


def resting_inhibitors(o: p7.Olfaction, inhibitors: np.ndarray, seed: int) -> float:
    """The inhibitors' summed resting rate (spikes/s), over REST_SEEDS rest windows of 8 flies. Presynaptic inhibition
    can't change it: the receptor neurons are silent at rest."""
    return float(np.mean([p3.rest_state(o.s, seed + r, False)["counts"][:, inhibitors].sum(1).mean() for r in range(REST_SEEDS)]))


def apply(o: p7.Olfaction, mk: dict, base_w: np.ndarray, base_sw: np.ndarray, k_a: float, k_b: float, a_rest: float) -> float:
    """Presynaptic inhibition with strengths k_a (GABA-A) and k_b (GABA-B) per spike/s of the inhibitors' summed rate,
    each trace starting at the resting rate, and the inhibited synapses' weights times the resting divisor, so that at
    rest they carry the strength they were calibrated to (Kazama & Wilson's 6.19 mV was measured in vivo, under the
    tonic inhibition). Returns the resting divisor."""
    b = o.brain
    d_rest = 1.0 + (k_a + k_b) * a_rest
    w = base_w.copy()
    w[mk["fast"]] *= d_rest
    b.weights, b._external_matrix = w, None
    b.slow_weights = base_sw.copy()
    b.slow_weights[mk["slow"]] *= d_rest
    c = TAU_A / (TAU_A - TAU_A_RISE)                 # the difference of exponentials' steady state = k_a x the rate
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=(TAU_A, TAU_A_RISE, TAU_B),
                      k=(c * k_a, -(c - 1.0) * k_a, k_b), start=a_rest)
    return d_rest


def lateral_traces(o: p7.Olfaction, seed: int) -> np.ndarray:
    """Each LATERAL odor (all its glomeruli, at the model's usual strength): the GABA-A and GABA-B traces (flies' mean)
    at Olsen & Wilson's sample times, shifted by the valve's delay. Shape (odors, times, 2)."""
    b = o.brain
    c = TAU_A / (TAU_A - TAU_A_RISE)
    out = []
    for j, odor in enumerate(LATERAL):
        b.reset(seed + j)
        b.set_release(o.s.ol.neurons, o.s.silent)
        b.advance(int(round(2.0 / b.dt)))
        drive, t, row = odors.orn_drive(b, odor), 0.0, []
        for ts in OLSEN_T:
            b.advance(int(round((ts - VALVE_DELAY - t) / b.dt)), drive=drive)
            t = ts - VALVE_DELAY
            a = b.presynaptic_state.mean(0)
            row.append((c * a[0] - (c - 1.0) * a[1], a[2]))
        out.append(row)
    return np.array(out)


def fit(e: np.ndarray, a_rest: float) -> tuple[float, float, dict]:
    """k_a from the GABA-B-blocked EPSCs, then k_b from the control ones with k_a fixed, each by least squares on the
    log divisor relative to rest (Olsen & Wilson normalized each condition to its own baseline)."""
    from scipy.optimize import minimize_scalar
    ea, eb = e[..., 0].mean(0), e[..., 1].mean(0)
    cgp, ctl = -np.log(np.array(OLSEN_CGP)), -np.log(np.array(OLSEN_CONTROL))
    rel_a = lambda ka: np.log((1 + ka * ea) / (1 + ka * a_rest))
    k_a = minimize_scalar(lambda x: ((rel_a(x) - cgp) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    rel = lambda kb: np.log((1 + k_a * ea + kb * eb) / (1 + (k_a + kb) * a_rest))
    k_b = minimize_scalar(lambda x: ((rel(x) - ctl) ** 2).sum(), bounds=(0.0, 1.0), method="bounded").x
    model = {"cgp_fraction": np.round(np.exp(-rel_a(k_a)), 3).tolist(), "control_fraction": np.round(np.exp(-rel(k_b)), 3).tolist(),
             "gaba_b_only_fraction": np.round((1 + k_b * a_rest) / (1 + k_b * eb), 3).tolist(),
             "trace_a_over_rest": np.round(ea / a_rest, 2).tolist(), "trace_b_over_rest": np.round(eb / a_rest, 2).tolist()}
    return float(k_a), float(k_b), model


def set_condition(o: p7.Olfaction, name: str, mk: dict) -> dict:
    b = o.brain
    if name == "base":
        b.set_presynaptic()
        return {"presynaptic": None}
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a_rest = resting_inhibitors(o, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):                               # the traces depend on k through the inhibited ORN-to-LN synapses
        apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        e = lateral_traces(o, SEED + 960 + 10 * r)
        k_a, k_b, model = fit(e, a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    d_rest = apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    c = TAU_A / (TAU_A - TAU_A_RISE)
    return {"presynaptic": {"k": [c * k_a, -(c - 1.0) * k_a, k_b], "k_a": k_a, "k_b": k_b, "tau_s": [TAU_A, TAU_A_RISE, TAU_B],
                            "inhibitors_rest_hz": round(a_rest, 1), "resting_divisor": round(d_rest, 3), "calibration": rounds,
                            "flies": {"times_s": OLSEN_T, "control_fraction": OLSEN_CONTROL, "cgp_fraction": OLSEN_CGP}}}


def main(names: list[str]) -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    types, m = o.types, o.m
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = json.loads(OUT.read_text()) if OUT.exists() else {"question": __doc__, "flies": p7.FLIES, "conditions": {}}
    out["question"] = __doc__
    out["build"] = build(o)
    mk = masks(o)
    print(json.dumps(out["build"]["removed"]), json.dumps(out["build"]["unitary"]), flush=True)
    for c, name in enumerate(CONDITIONS):
        if name not in names:
            continue
        base = SEED + 1000 * c
        entry = set_condition(o, name, mk)
        k = np.asarray(entry["presynaptic"]["k"]) if entry["presynaptic"] else np.zeros(0)
        d_rest = entry["presynaptic"]["resting_divisor"] if entry["presynaptic"] else 1.0
        entry["course"] = {}
        for j, odor in enumerate(COURSE_ODORS):
            pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
            entry["course"][odor] = course(o, odor, base + 700 + j, pns, mk["inhibitors"], k, d_rest)
            print(name, odor, json.dumps({x: entry["course"][odor][x][::4] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
        entry["transform"] = p17.transform(o, base)
        entry.update(p17.odor_measures(o, base, gloms, pn_of))
        out["conditions"][name] = entry
        pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
        print(name, json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                                "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or list(CONDITIONS))
