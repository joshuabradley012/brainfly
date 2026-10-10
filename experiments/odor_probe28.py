"""Exploratory, not pre-registered: if the presynaptic inhibition builds after the local neurons fire, as flies' does,
rather than following their onset burst at once, do the projection neurons keep their odor onsets while the Kenyon
cells stay odor-specific?

odor_probe27.py: inhibition evoked above the LNs' resting rate, fitted to Olsen & Wilson 2008's EPSCs, decorrelates the
PNs' odor patterns (r = 0.22) and makes the Kenyon cells as sparse and specific as flies' (1.0-4.5%, mean Jaccard 0.15),
but its traces, first-order low-passes of the LNs' rate, take in the LNs' onset burst at once, so the synapses fall to
0.06-0.08 of their resting strength within 50 ms and the PNs are suppressed at onset (32-73 Hz in the first 100 ms,
flies 100-200) and too narrowly tuned (16-26% by Turner's criterion, flies 59 +- 14%). In flies "LN firing rates peak
rapidly after odor onset, but the functional effects of inhibition peak ~100 ms later", the inhibition's time course
fits "an alpha function with a time constant of about 25 ms" (Nagel, Hong & Wilson 2015), and its measured step response
reaches 90% at about 150 ms (research_notes/Rung 9 learning data/pn_ln_dynamics.md).
Model: odor_probe27.py's with each trace replaced by two first-order stages in series (HybridBrain.set_presynaptic's
source): GABA-A as two 25 ms stages, which is Nagel et al.'s alpha function; GABA-B as a 50 ms stage feeding its 1 s
decay, so that its response to a brief burst peaks about 160 ms later. Each acts only above the LNs' resting rate, as in
odor_probe27.py, and k_A and k_B are fitted to Olsen & Wilson's EPSCs in the same way.
Measured as odor_probe27.py measures. Seeds 220000 (otherwise as odor_probe27.py's, with its offsets).

Ran: the delayed onset changes almost nothing, because the LNs' burst is too large next to their later activity. The
fit gives k_A = 0.0064 and k_B = 0.0096 per spike/s above rest (EPSCs at 0.23-0.41 of baseline, flies 0.27-0.37; GABA-B
blocked 0.47-0.88, flies 0.52-0.81). The GABAergic LNs fire 46 spikes/s each over an odor's first 50 ms but only about
1 above their resting 0.56 later (flies: 22 over the first 50 ms, 6-8 later, over a rest of about 4), so strengths
fitted at 0.25 s and later amount to a divisor of about 20 during the burst, which two 25 ms stages delay by only tens of
ms: the synapses are at 0.05 of their resting strength by 50 ms and the PNs still fall at onset and then climb
(3-octanol: 48 Hz in the first 50 ms, 19 at 50-150 ms, 89 by 500 ms). Everything else matches odor_probe27.py: Rmax 176,
271, 323 and 290, sigma 36, 30, 39 and 33, lateral input abolishing responses (to 0-0.28); PNs at 40-79 Hz in the first
100 ms and 105-159 over 1 s, 17-28% responding by Turner's criterion; PN patterns correlating 0.23 between odors; 1.0-4.5%
of Kenyon cells responding, mean Jaccard 0.15, 48% of 4-methylcyclohexanol's responders also answering 3-octanol;
alpha'/beta' cells 0.1-1.4%; MBON11 1.7-7.5 spikes, MBON-alpha2sc 1.1-18. PNs rest at 1.2 Hz after the polish.

    python experiments/odor_probe28.py         (writes experiments/odor_probe28.json)
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
import odor_probe7 as p7
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED = 220000
TAUS = (0.025, 0.025, 0.05, 1.0)                  # GABA-A stage 1, stage 2; GABA-B stage 1, stage 2
SOURCE = (-1, 0, -1, 2)


def apply(o: p7.Olfaction, mk: dict, base_w, base_sw, k_a: float, k_b: float, a_rest: float) -> None:
    """odor_probe27.apply with two stages per component; only the second stages act, above the LNs' resting rate."""
    b = o.brain
    b.weights, b._external_matrix = base_w.copy(), None
    b.slow_weights = base_sw.copy()
    b.set_presynaptic(fast=mk["fast"], slow=mk["slow"], inhibitors=mk["inhibitors"], tau=TAUS, k=(0.0, k_a, 0.0, k_b),
                      start=a_rest, offset=a_rest, source=SOURCE, depleting=np.flatnonzero(o.m["orn"]))


def lateral_traces(o: p7.Olfaction, rec: p10.Receptors, seed: int) -> np.ndarray:
    """The two components' acting traces at Olsen & Wilson's sample times: (odors, times, 2)."""
    b = o.brain
    base = p24.spontaneous(rec)
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
            row.append((a[1], a[3]))
        out.append(row)
    return np.array(out)


def calibrate(o, rec, mk, base_w, base_sw) -> dict:
    a_rest = p24.resting_inhibitors(o, rec, mk["inhibitors"], SEED + 940)
    k_a, k_b, rounds = 0.0, 0.0, []
    for r in range(4):
        apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
        k_a, k_b, model = p27.fit(lateral_traces(o, rec, SEED + 960 + 10 * r), a_rest)
        rounds.append({"k_a": round(k_a, 6), "k_b": round(k_b, 6), **model})
        print("calibration round", r + 1, json.dumps(rounds[-1]), flush=True)
    apply(o, mk, base_w, base_sw, k_a, k_b, a_rest)
    return {"k": [0.0, k_a, 0.0, k_b], "offset_hz": round(a_rest, 1), "tau_s": list(TAUS), "source": list(SOURCE),
            "inhibitors_rest_hz": round(a_rest, 1), "resting_divisor": 1.0, "calibration": rounds,
            "flies": {"times_s": p21.OLSEN_T, "control_fraction": p21.OLSEN_CONTROL, "cgp_fraction": p21.OLSEN_CGP}}


def main() -> None:
    t0 = time.perf_counter()
    p21.SEED = p22.SEED = p24.SEED = p27.SEED = SEED
    o = p7.Olfaction()
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]} & {t.split("_")[0] for t in types[m["upn"]]})
    pn_of = {g: np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_")) for g in gloms}
    out = {"question": __doc__, "flies": p7.FLIES, "build": p21.build(o)}
    mk = p21.masks(o)
    rec = p10.Receptors(o)
    rec.spontaneous, rec.kinetics = True, False
    out["spontaneous_hz"] = rec.spont
    base_w, base_sw = b.weights.copy(), b.slow_weights.copy()
    a0 = p21.resting_inhibitors(o, mk["inhibitors"], SEED + 930)
    apply(o, mk, base_w, base_sw, 0.0, 0.0, a0)
    p10.POLISH, schedule = p27.FIRST_POLISH, p10.POLISH
    try:
        out["resting_recalibration"] = p24.recalibrate_rest(o, rec, mk, base_w, base_sw, 1.0, SEED + 600)
    finally:
        p10.POLISH = schedule
    out["pn_rest"] = p27.pn_polish(o, rec, SEED + 700)
    entry = {"presynaptic": calibrate(o, rec, mk, base_w, base_sw)}
    out["second_polish"] = p24.polish(o, rec, SEED + 640, p27.SECOND_POLISH)
    out["pn_rest_after"] = p27.pn_polish(o, rec, SEED + 800, rounds=6)
    k, offset = np.asarray(entry["presynaptic"]["k"]), entry["presynaptic"]["offset_hz"]
    base = SEED + 1000
    entry["course"] = {}
    for j, odor in enumerate(p21.COURSE_ODORS):
        pns = np.concatenate([pn_of[g] for g in odors.glomeruli(odor) if g in pn_of])
        entry["course"][odor] = p27.course(o, rec, odor, base + 700 + j, pns, mk["inhibitors"], k, offset)
        print(odor, json.dumps({x: entry["course"][odor][x][:10] for x in ("pn_hz", "inhibitors_hz", "gain")}), flush=True)
    entry["transform"] = p24.transform(o, rec, base)
    entry.update(p24.odor_measures(o, rec, base, gloms, pn_of))
    out["condition"] = entry
    pair = entry["pairs"]["3-octanol | 4-methylcyclohexanol"]
    print(json.dumps({"rest": entry["rest"], "mean_jaccard": entry["mean_jaccard"], "mean_pn_early_corr": entry["mean_pn_early_corr"],
                      "oct_mch": pair, "odors_per_cell": entry["odors_per_cell"]["model"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
