"""Exploratory, not pre-registered: do the SEZ's own settings bring taste back to the resting brain that escapes?

research_notes/Rung 4 resting state data/taste_at_rest.md found sugar's signal intact at the second-order
taste neurons (G2N-1, Zorro, Clavicle, FMIn and Rattle rise 25-90 Hz in the resting brain, as in rung 1's
silent one) and lost one or two synapses later, in a recurrent premotor cluster (Roundup, Rounddown,
DNge059, GNG169, Sternum) that can no longer ignite. It traced that to two of the resting brain's
settings, neither measured for this circuit:
  depression   the central cholinergic default (0.9 of the strength left per spike, 0.5 s to recover)
               caps the taste interneurons, which fire 25-90 Hz under sugar. No short-term plasticity has
               been measured at any taste synapse, and the default was added to calm other loops.
  targets      the 0.1 Hz target for every descending neuron holds the cluster's descending members 12-16
               mV below threshold. That value came from walking, steering and escape descending neurons
               (DNa02, DNp07, DNp10, the giant fiber). The only gnathal ones with measured rates fire
               tonically: DSOG1 (DNg70 and DNg98, matched by the notes) at about 17 Hz in every feeding
               state (Pool et al. 2014), the octopaminergic VUMd descending neurons at about 4 Hz.
Its probes (no full recalibration) got MN9 from +2 to +27 Hz with both changed. Here, by rules rather than
by which neurons sugar recruits, in escape_at_rest2.py's model (which passed):
  rank 1   every cholinergic neuron of a GNG* or PRW* type, and Clavicle (ANXXX462a), undepressed
  rank 2   every descending neuron of a DNg* type (gnathal, including DNge*) at the 2 Hz default instead of
           0.1 Hz, and DNg70 and DNg98 at 17 Hz; other descending neurons keep 0.1 Hz
for rank 1 alone, rank 2 alone and both, each recalibrated from escape_at_rest2.py's biases in 20 fresh-start
rounds (k = 2 mV for 8, then 1 for 8, then 0.5 for 4). Measured, 8 flies unless noted:
  rest      10 s at grey: the brain's own mean rate, neurons over 100 Hz, neurons whose 1-s Fano factor
            passes 10
  ignition  the left looming loop over 32 flies, as ignition.py counts it
  taste     MN9 L's rise over its rest (the 0.5 s before) under 1 s of drive at 100 Hz: sugar; sugar at 10 Hz;
            sugar with bitter; sugar with Ir94e; water (rung 1's sets)
  premotor  MN9 L's rise when the left Roundup, Roundtree and Rounddown (GNG108, GNG120, DNge080) are driven
            at 50 Hz for 1 s (flies extend to MN9's own activation, so the path below the cluster must work)
  looming   eyes_at_rest.py's tests at gain 1 on seed 1, and the giant fiber's rise

Second round (after the first three): with both, sugar raised MN9 by 20.5 Hz, but MN9 rested at 11 Hz in
bouts of about 50 Hz lasting seconds, 262 neurons burst (gnathal descending types now at 2 Hz, such as
DNg12, and the nerve-cord neurons they drive), and water alone raised MN9 13 Hz. Awake flies rarely extend
the proboscis at rest, and MN9 fires only while the rostrum moves (Gordon & Scott 2009), so the notes'
fourth, uncertain change, a quiet proboscis motor module, is tried too, again by rule:
  route        rank 1, and only the descending neurons of rung 1's own taste route (those sugar at 100 Hz
               raises by more than 5 Hz in the silent brain: 42 neurons of 26 gnathal types) at 2 Hz; DSOG1
               at 17 Hz; other descending neurons keep 0.1 Hz
  quiet        both, and MN9 with every neuron making at least 100 synapses onto it (16 neurons: its
               excitatory and inhibitory premotor inputs) at 0.2 Hz
  route_quiet  route and the quiet module together
Also measured for these: MN9's spontaneous bouts, the share of fly-seconds at rest in which MN9 L fires
more than 20 spikes.

    python experiments/taste_route.py --condition both     (also rank1, rank2, route, quiet, route_quiet;
                                                            writes experiments/taste_route/<condition>.json)
    python experiments/taste_route.py --report             (writes experiments/taste_route.json)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

import escape_at_rest as escape
import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import ignition
import rest_calibration as attempt1
import rest_calibration2 as attempt2

FULL_NETWORK = attempt1.network
from brainfly.hybrid import consensus_transmitters
from shiu_baseline import SETS

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
CONDITIONS = {"rank1": (True, None, False), "rank2": (False, "gnathal", False), "both": (True, "gnathal", False),
              "route": (True, "route", False), "quiet": (True, "gnathal", True), "route_quiet": (True, "route", True)}
ROUNDS = [2.0] * 8 + [1.0] * 8 + [0.5] * 4
FULL_TARGETS = attempt1.targets
DSOG1 = ["DNg70", "DNg98"]
PREMOTOR = ["GNG108", "GNG120", "DNge080"]


def route_model(undepress: bool):
    def model(types, superclass):
        spec, sets = escape.model(types, superclass)
        if undepress:
            ach = consensus_transmitters() == "acetylcholine"
            sez = np.char.startswith(types, "GNG") | np.char.startswith(types, "PRW") | (types == "ANXXX462a")
            sets["sez_taste"] = np.flatnonzero(ach & sez)
            spec["sez_taste"] = {"depression": 1.0}
        return spec, sets
    return model


def gnathal_targets(types, superclass, default):
    t = FULL_TARGETS(types, superclass, default)
    t[np.char.startswith(superclass, "descending_neuron") & np.char.startswith(types, "DNg")] = default
    t[np.isin(types, DSOG1)] = 17.0
    return t


def route_descending() -> np.ndarray:
    """The descending neurons sugar at 100 Hz raises by more than 5 Hz in rung 1's silent brain."""
    from brainfly.hybrid import HybridBrain
    from shiu_rewiring import W_SYN
    M, scale, labels, types, superclass = FULL_NETWORK()
    b = HybridBrain(trials=8, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=1)
    rates = b.run(1.0, drive=[(b.cells(SETS["sugar"], "L"), 100.0)], seed=3).rates
    return np.char.startswith(superclass, "descending_neuron") & (rates > 5)


def mn9_module(types) -> np.ndarray:
    """MN9 and every neuron making at least 100 synapses onto it."""
    M = abs(FULL_NETWORK()[0].tocsr())
    mn9 = types == "MN9"
    return mn9 | (np.asarray(M[np.flatnonzero(mn9)].sum(0)).ravel() >= 100)


def targets_for(dn: str | None, quiet: bool):
    route = route_descending() if dn == "route" else None
    def targets(types, superclass, default):
        t = FULL_TARGETS(types, superclass, default)
        if dn == "gnathal":
            t[np.char.startswith(superclass, "descending_neuron") & np.char.startswith(types, "DNg")] = default
        elif dn == "route":
            t[route] = default
        if dn is not None:
            t[np.isin(types, DSOG1)] = 17.0
        if quiet:
            t[mn9_module(types)] = 0.2
        return t
    return targets


def rise(s: eyes.Setup, cells, drive, seed: int) -> np.ndarray:
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(0.5 / b.dt)))
    before = b.advance(int(round(0.5 / b.dt)))[:, cells].mean(1) / 0.5
    return b.advance(int(round(1.0 / b.dt)), drive=drive)[:, cells].mean(1) - before


def condition(name: str) -> dict:
    t0 = time.perf_counter()
    undepress, dn, quiet = CONDITIONS[name]
    retarget = dn is not None
    if name in ("rank2", "both"):                    # the first round's rule, kept as it ran
        attempt1.targets = gnathal_targets
    elif dn is not None or quiet:
        attempt1.targets = targets_for(dn, quiet)
    attempt2.model, attempt1.network = route_model(undepress), escape2.network
    eyes.ROUNDS = ROUNDS
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(escape2.HERE / "intact.npz")["bias"]
    log = s.calibrate()
    b, own = s.brain, ~s.fixed
    b.reset(77)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    c = np.stack([b.advance(int(round(1.0 / b.dt))) for _ in range(10)])
    mean, var = c.mean((0, 1)), c.var(0).mean(0)
    fano = np.where(mean > 0.5, var / np.maximum(mean, 1e-9), np.nan)
    mn9 = b.cells(["MN9"], "L")
    rest = {"mean_hz_own": round(float(mean[own].mean()), 3), "over_100hz": int((mean[own] > 100).sum()),
            "bursting_fano_over_10": int(np.nansum(fano[own] > 10)), "mn9_L_hz": round(float(mean[mn9].mean()), 2),
            "dsog1_hz": round(float(mean[b.cells(DSOG1)].mean()), 2),
            "mn9_L_bout_share": round(float((c[:, :, mn9].sum(2) > 20).mean()), 3)}
    hot = np.zeros(len(ignition.SEEDS) * eyes.TRIALS, bool)
    for k, seed in enumerate(ignition.SEEDS):
        rates = s.run(lambda t: [], 1.0, seed, window=(eyes.SCENE - eyes.LATE, eyes.SCENE))["rates"]
        for cell in s.cells:
            if cell.split()[0] in ignition.LIMIT:
                hot[k * eyes.TRIALS:(k + 1) * eyes.TRIALS] |= rates[:, s.cells[cell]].mean(1) > ignition.LIMIT[cell.split()[0]]
    sets = {k: b.cells(v, "L") for k, v in SETS.items()}
    taste = {"sugar": rise(s, mn9, [(sets["sugar"], 100.0)], 1), "sugar 10 Hz": rise(s, mn9, [(sets["sugar"], 10.0)], 5),
             "sugar+bitter": rise(s, mn9, [(sets["sugar"], 100.0), (sets["bitter"], 100.0)], 3),
             "sugar+ir94e": rise(s, mn9, [(sets["sugar"], 100.0), (sets["ir94e"], 100.0)], 4),
             "water": rise(s, mn9, [(sets["water"], 100.0)], 6),
             "premotor 50 Hz": rise(s, mn9, [(b.cells(PREMOTOR, "L"), 50.0)], 7)}
    v = eyes.loom_tests(s, 1.0, seed=1)
    stat = lambda x: {"mean": round(float(x.mean()), 2), "sem": round(float(x.std(ddof=1) / np.sqrt(len(x))), 2)}
    out = {"condition": name, "undepressed_sez_taste": undepress, "descending_targets": dn, "quiet_module": quiet,
           "calibration": log[-1], "rest": rest, "ignited_flies": int(hot.sum()), "flies": len(hot),
           "mn9_rise_hz": {k: stat(x) for k, x in taste.items()},
           "looming": {k: v[k] for k in ("REST", "RELAY", "SIDE", "ESCAPE")},
           "giant_fiber_rise_hz": {k: x["delta"] for k, x in v["escape"].items() if "near" not in k},
           "seconds": round(time.perf_counter() - t0)}
    HERE.mkdir(exist_ok=True)
    (HERE / f"{name}.json").write_text(json.dumps(out, indent=1))
    np.savez_compressed(HERE / f"{name}.npz", groups=s.names, bias=s.bias)
    print(json.dumps(out), flush=True)
    return out


def report() -> None:
    out = {"question": __doc__, "conditions": [json.loads((HERE / f"{c}.json").read_text()) for c in CONDITIONS if (HERE / f"{c}.json").exists()]}
    OUT.write_text(json.dumps(out, indent=1))
    for c in out["conditions"]:
        print(c["condition"], c["calibration"]["groups_within_2x"], c["rest"], c["ignited_flies"],
              {k: x["mean"] for k, x in c["mn9_rise_hz"].items()}, c["looming"], c["giant_fiber_rise_hz"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=list(CONDITIONS))
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    report() if a.report else condition(a.condition)


if __name__ == "__main__":
    main()
