"""Rung 4, attempt 2 (pre-registered): attempt 1 with the per-type properties fly neurons are measured
to have that stop recurrent loops from running away, and a calibration that fits the state the tests
see. Does the brain now rest like a fly?

Attempt 1 (rest_calibration.py) failed on FC (r 0.20, below its independent-firing null's 0.41) and the
bump, for two reasons. Its calibration ran without restarting and settled in a different state from
the one a fresh start reaches, so the fitted rates didn't carry over. And a few central-complex
neurons switched between silence and bursts (1-s Fano factors of 24-128), dominating their regions'
slow signals. research_notes/Rung 4 resting state data/adaptation.md surveyed the intrinsic
properties behind this. Fly central neurons barely adapt, but spikes leave afterhyperpolarisations
of 1.5-8 mV, and projection and lateral-horn neurons sit about 10 mV below threshold. Cholinergic
synapses depress: ORN to PN, each spike leaves 0.78 of the synapse's strength, which recovers with
a 0.89 s time constant (Nagel, Hong & Wilson 2015).
An exploratory pilot, judged on rates and bursting only (FC and the bump were never computed),
calibrated from a fresh start every round, adding these properties one at a time. Fresh starts alone,
or with the reset and thresholds, left bursting central-complex neurons and hot neurons, and 57-72%
of groups within a factor of 2. With depression added, every group was within a factor of 2, with no
neuron over 100 Hz and none with a 1-s Fano factor over 10.

Model: attempt 1's (rung 1's network, APL graded, the same background, one bias per group), plus
  reset       5 mV below rest for every neuron (Shiu: at rest)
  threshold   10 mV above rest for uniglomerular projection neurons and lateral-horn types (LH*),
              16 mV for Kenyon cells (Gu & O'Dowd 2006); 7 elsewhere, as in Shiu's model
  depression  every cholinergic neuron's output (MaleCNS consensus transmitter): 0.78 per spike,
              recovering with 0.89 s (ORN to PN values, assumed for every cholinergic synapse)
Calibration: attempt 1's targets and update rule, but each round starts fresh (a reset with a new
seed, 1 s to settle, 2 s measured), 30 rounds, k = 2 mV for rounds 1-15, 1 for 16-25, 0.5 for 26-30.
Tests, conditions and pass rule: exactly attempt 1's (FC against Turner et al.'s 20 flies, beating the
independent-firing null and 2 calibrated degree-preserving rewirings by 0.05 in r; RATE; BUMP), and
the same sensitivity conditions. Attempt 1's FC errors were seen, so FC is held out from the fit
but not from the whole project's history. This attempt's changes come from the literature and a
rate pilot, not from FC.

    python experiments/rest_calibration2.py --condition intact      (also rewired-1, rewired-2,
                                                                      default-1hz, default-4hz)
    python experiments/rest_calibration2.py --report               (writes experiments/rest_calibration2.json)
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
from brainfly.hybrid import consensus_transmitters

HERE = Path(__file__).with_suffix("")
OUT = Path(__file__).with_suffix(".json")
RESET, THRESHOLD_PN_LH, THRESHOLD_KC = -5.0, 10.0, 16.0
DEPRESSION, RECOVERY = 0.78, 0.89
ROUNDS = [2.0] * 15 + [1.0] * 10 + [0.5] * 5          # k, mV per e-fold of rate error
SETTLE_ROUND, MEASURE_ROUND = 1.0, 2.0


def model(types: np.ndarray, superclass: np.ndarray) -> tuple[dict, dict]:
    spec = {"all": {**attempt1.BACKGROUND, "reset": RESET}, "APL": {"unit": "graded"}}
    for t in sorted({t for t in types if t}):
        if re.search(r"_[a-z]*PN$", t) or t.startswith("LH"):
            spec[t] = {"threshold": THRESHOLD_PN_LH}
        elif t.startswith("KC"):
            spec[t] = {"threshold": THRESHOLD_KC}
    spec["cholinergic"] = {"depression": DEPRESSION, "recovery": RECOVERY}
    return spec, {"cholinergic": np.flatnonzero(consensus_transmitters() == "acetylcholine")}


def calibrate(brain, gid: np.ndarray, target: np.ndarray, graded: np.ndarray) -> tuple[np.ndarray, list]:
    G = gid.max() + 1
    size = np.bincount(gid, minlength=G)
    goal = np.bincount(gid, weights=target, minlength=G) / size
    free = np.bincount(gid, weights=~graded, minlength=G) > 0
    bias, log = np.zeros(G), []
    for r, k in enumerate(ROUNDS):
        brain.reset(seed=500 + r)
        brain.set_bias(bias[gid])
        brain.advance(int(round(SETTLE_ROUND / brain.dt)))
        rate = brain.advance(int(round(MEASURE_ROUND / brain.dt))).mean(0) / MEASURE_ROUND
        got = np.bincount(gid, weights=rate, minlength=G) / size
        step = np.where(free, np.clip(k * np.log((goal + attempt1.SOFT) / (got + attempt1.SOFT)), -k, k), 0.0)
        bias = np.clip(bias + step, attempt1.LOW, attempt1.HIGH)
        log.append({"round": r + 1, "mean_hz": round(float(rate.mean()), 3), "over_100hz": int((rate > 100).sum()),
                    "groups_within_2x": round(float(attempt1.within_factor_2(got, goal)[free].mean()), 4),
                    "mean_abs_step_mv": round(float(np.abs(step[free]).mean()), 3)})
        print(json.dumps(log[-1]), flush=True)
    return bias, log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=list(attempt1.CONDITIONS))
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.report:
        attempt1.report(here=HERE, out=OUT, criteria=__doc__)
    elif a.condition:
        attempt1.condition(a.condition, model=model, fit=calibrate, here=HERE)
    else:
        ap.error("give --condition or --report")


if __name__ == "__main__":
    main()
