"""Exploratory, not pre-registered: does letting each ring neuron set its own excitability free the bump
from preferred wedges?

ring_er.py's sub-network (the head-direction ring with its ring neurons, a slow current on the ring's
excitation, depression on its excitatory outputs, gains of 3 and 1.5) holds a bump. But it fails rung
4's BUMP test because runs settle on the same few wedges, and it's 45 deg wide against flies' 80-120.
MaleCNS wedges hold 2 to 4 EPGs each, so some wedges excite themselves twice as strongly as others.
Renart, Song & Wang (2003, Neuron 38:473) found that homeostasis in each neuron evens out such
differences in a bump attractor: a neuron that fires too much at a spot lowers its own excitability
and the spot loses its pull. Here each condition's biases are fitted as rung 4 fits them (fresh starts,
8 runs of 1 s to settle and 5 s measured, 20 rounds, the bias moving by k ln((target + 0.5) /
(rate + 0.5)) mV, at most k, k = 2 for rounds 1-10 and 1 after, kept within -30 and +20 mV; targets
rung 4's: PEN_a 3.9 Hz, every other type 2) either
  per type     one bias per cell type (rung 4's calibration)
  per neuron   one bias per neuron, each neuron to its type's target
and then scored as ring_er.py scores it (8 spontaneous runs of 30 s with rung 4's BUMP measures,
width and peak; 16 seeded runs of 10 s). Conditions: the recipe, and the recipe with the EPG-PEN loop
(EPG to PEN_a and PEN_b, and back) 1.5 and 2 times stronger, which the notes found widens the bump but
drives it hot.

    python experiments/ring_calibrated.py            (writes experiments/ring_calibrated.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_er

OUT = Path(__file__).with_suffix(".json")
ROUNDS = [2.0] * 10 + [1.0] * 10
SETTLE, MEASURE = 1.0, 5


def calibrate(recipe: dict, per_neuron: bool) -> tuple[np.ndarray, list]:
    r = ring_er.Ring(recipe, ring_er.RUNS, seed=900)
    b = r.brain
    target = np.where(r.types == "PEN_a(PEN1)", 3.9, 2.0)
    gid = np.arange(b.n) if per_neuron else np.unique(r.types, return_inverse=True)[1]
    count = np.bincount(gid)
    goal = np.bincount(gid, target) / count
    bias, log = np.zeros(b.n), []
    for k, step_k in enumerate(ROUNDS):
        b.reset(seed=900 + k)
        b.set_bias(bias)
        b.advance(int(round(SETTLE / b.dt)))
        rate = b.advance(int(round(MEASURE / b.dt))).mean(0) / MEASURE
        got = np.bincount(gid, rate) / count
        bias = np.clip(bias + np.clip(step_k * np.log((goal + attempt1.SOFT) / (got + attempt1.SOFT)), -step_k, step_k)[gid],
                       attempt1.LOW, attempt1.HIGH)
        log.append({"round": k + 1, "within_2x": round(float(attempt1.within_factor_2(got, goal).mean()), 3),
                    "epg_hz": round(float(rate[r.epg].mean()), 2), "epg_max_hz": round(float(rate[r.epg].max()), 1)})
    return bias, log


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "conditions": []}
    for loop in (1.0, 1.5, 2.0):
        recipe = ring_er.RECIPE | {"loop": loop}
        for per_neuron in (False, True):
            bias, log = calibrate(recipe, per_neuron)
            s, sd = ring_er.spontaneous(recipe, bias), ring_er.seeded(recipe, bias)
            out["conditions"].append(c := {"loop": loop, "calibration": "per neuron" if per_neuron else "per type",
                                           "last_round": log[-1], "spontaneous": s, "seeded": sd})
            print(f"loop x{loop} {c['calibration']}: BUMP {s['BUMP']}",
                  {x: (v["strength"], v["shuffle_p99"], v["resultant"]) for x, v in s["bump"].items()},
                  f"| fwhm {s['fwhm_deg']} peak {s['busiest_wedge_hz']}", s["rate_hz"], f"| held {sd['held']}/{sd['runs']} |", log[-1], flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
