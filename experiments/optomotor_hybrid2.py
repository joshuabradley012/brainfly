"""Is there a gain at which vision reaches DNa02 in the rung-1 brain without igniting it? (second attempt)

optomotor_hybrid.py failed at every gain from 1 to 100. The drum's signal reached HS and, at gains 3
and 10, DNa02 with the right sign, but the network ran away. Two checks afterwards (not
pre-registered, both on its gain 1) shaped this attempt, and are disclosed here:
  - flyvis's own output takes about a second to settle after the drum stops (8% of its drum-time
    level in the 0.25-0.5 s window the first attempt measured), so stability is now measured
    1.0-1.25 s after the drum, when flyvis's output is below 0.1% of that level;
  - at gain 1 the brain's own neurons still fired at 75% of their drum-time level then, in the
    central complex, the anterior visual pathway and the nerve cord, so the gains here are lower.
A full-field drum drives much of the optic lobe, and visual neurons can fire above 100 Hz, so the
count of neurons over 100 Hz now leaves out the visual system (superclasses ol_intrinsic,
visual_projection, visual_centrifugal, ol_sensory).

Setup, scenes, HS, STEER, the held-out drum and NULL: exactly optomotor_hybrid.py's, with the grey after
the moving drums lasting 1.25 s.
Knob: G in {0.03, 0.1, 0.3}.
Pass, fixed before the first run, all at one G:
  STABLE  under ccw and under cw: at most 20 neurons outside the visual system pass 100 Hz, and
          1.0-1.25 s after the drum the neurons flyvis doesn't drive fire under 1% as much as
          during it
  HS, STEER as in optomotor_hybrid.py
then, at the lowest passing G, HS and STEER on the held-out drum, and NULL.

    python experiments/optomotor_hybrid2.py            (writes experiments/optomotor_hybrid2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import nulls
from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.optic import FlyvisNative
from brainfly.shiu import counts, mcns_types
from optomotor_hybrid import HS, OPTIC_DT, measure, scenes, signals, verdict
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

OUT = Path(__file__).with_name("optomotor_hybrid2.json")
GAINS = [0.03, 0.1, 0.3]
TAIL = 1.25
VISUAL = ["ol_intrinsic", "visual_projection", "visual_centrifugal", "ol_sensory"]


def run_gain(brain, ol, gain, drum, outside, tail=True) -> tuple[dict, dict]:
    ol.gain = gain
    rates, stable = {}, {"STABLE": True}
    for name, scene in drum.items():
        moving = name in ("ccw", "cw")
        r, during, late = measure(brain, ol, scene, TAIL if (moving and tail) else 0.0)
        rates[name] = r
        if moving and tail:
            hot = int((r[outside] > 100).sum())
            fraction = float(late.mean() / during.mean()) if during.mean() > 0 else 0.0
            stable[f"{name}_over_100hz_outside_vision"] = hot
            stable[f"{name}_over_100hz_all"] = int((r[~brain.external] > 100).sum())
            stable[f"{name}_tail_fraction"] = round(fraction, 5)
            stable["STABLE"] &= bool(hot <= 20 and fraction < 0.01)
    return rates, stable


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    scale = 1.0 / sizes(C)
    brain = HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels)
    ol = FlyvisNative(brain, dt=OPTIC_DT)
    outside = ~np.isin(meta["superclass"].astype(str), VISUAL)
    cells = {f"HS {s}": brain.cells(HS, s) for s in "LR"}
    cells.update({f"{t} {s}": brain.cells([t], s) for t in ("DNa02", "DNa01") for s in "LR"})
    results = {"criteria": __doc__, "gains": {}}
    drum = scenes(30.0, 40.0)
    passing = None
    for gain in GAINS:
        rates, stable = run_gain(brain, ol, gain, drum, outside)
        v = verdict(signals(rates, cells), stable)
        results["gains"][str(gain)] = {"signals": signals(rates, cells), "verdict": v}
        print(f"G {gain:5.2f}: HS signal {v['HS_signal_hz']:+.1f} Hz, STEER {v['STEER_signal_hz']:+.1f} Hz, "
              f"DNa01 {v['DNa01_signal_hz']:+.1f} Hz | STABLE {v['STABLE']} (outside vision over 100 Hz "
              f"{v['ccw_over_100hz_outside_vision']}/{v['cw_over_100hz_outside_vision']}, all {v['ccw_over_100hz_all']}, "
              f"tail {v['ccw_tail_fraction']}/{v['cw_tail_fraction']})", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        if passing is None and v["STABLE"] and v["HS"] and v["STEER"]:
            passing = gain
    results["passing_gain"] = passing
    if passing is None:
        results["pass"] = False
        results["seconds"] = round(time.perf_counter() - t0)
        print("FAIL: no gain passes STABLE, HS and STEER", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        return
    print(f"lowest passing gain {passing}; held-out drum (20 deg, 60 deg/s)", flush=True)
    rates, stable = run_gain(brain, ol, passing, scenes(20.0, 60.0), outside)
    held = verdict(signals(rates, cells), stable)
    results["held_out"] = held
    print(f"    HS {held['HS_signal_hz']:+.1f} Hz, STEER {held['STEER_signal_hz']:+.1f} Hz, STABLE {held['STABLE']}", flush=True)
    rng = np.random.default_rng(31)
    null = []
    for k in range(10):
        rewired = HybridBrain(trials=1, w_syn=W_SYN, matrix=nulls.degree_preserving(M, rng), scale=scale, labels=labels)
        rates, _ = run_gain(rewired, ol, passing, {k2: drum[k2] for k2 in ("ccw", "cw")}, outside, tail=False)
        v = verdict(signals(rates, cells), None)
        null.append({"HS_signal_hz": v["HS_signal_hz"], "STEER_signal_hz": v["STEER_signal_hz"], "STEER": v["STEER"]})
        print(f"    rewiring {k}: HS {v['HS_signal_hz']:+.1f} Hz, STEER {v['STEER_signal_hz']:+.1f} Hz", flush=True)
    results["nulls"] = null
    results["NULL"] = sum(x["STEER"] for x in null) <= 1
    results["pass"] = bool(held["HS"] and held["STEER"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: G {passing}; held-out HS {held['HS']} STEER {held['STEER']}; "
          f"NULL {results['NULL']} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
