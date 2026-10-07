"""Does the optomotor signal need the connectome's wiring? optomotor.py's test on scrambled wiring.

optomotor.py found that a rotating drum reaches the HS cells and the steering neuron DNa02 with the
biological signs (confirmed on seed 2, 8 flies, gain 1). A result earns its place in brainfly only if
it also stops working when the wiring is scrambled. Here FlyBrain's wiring is rewired
(FlyBrain(rewire=k)): every connection keeps its presynaptic neuron, sign and weight but gets a random
target, and each neuron's inputs are rescaled to their original total, so every neuron still gets as
much input as before, from the wrong partners. The optic lobe model (FlyvisNative) is unchanged: the
question is whether MaleCNS's wiring downstream of it carries the signal.
Setup, scenes, windows and measures exactly as optomotor.py's confirmation (gain 1, seed 2, 8 flies),
for three independent rewirings, k = 1, 2, 3.
Pass criterion (the effect depends on the wiring), fixed before the first run: under every rewiring,
both of optomotor.py's direction signals miss their bars: HS (left minus right, ccw minus cw) is
below 3 Hz or has t < 4, and STEER (DNa02, likewise) is below 2 Hz or has t < 4.
Descriptive: REST under each rewiring; the number of descending neuron types that still carry a
direction signal.

    python experiments/optomotor_null.py            (writes experiments/optomotor_null.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.optic import GRADED as OPTIC, MODEL, FlyvisNative
from eyepath import GRADED, SCENES as SCENES_1D
from eyepath_fast import DT, REFRACTORY
from eyepath_filled import N0, measure as measure_1d
from eyepath_native import rises
from optomotor import HS, run_config

OUT = Path(__file__).with_name("optomotor_null.json")
REWIRINGS = [1, 2, 3]
GAIN, SEED, FLIES = 1.0, 2, 8


def build(rewire: int):
    brain = FlyBrain(batch=FLIES, graded=OPTIC, dt=DT, refractory=REFRACTORY, rewire=rewire)
    brain.graded_gain, brain.graded_release = 0.15, 0.3
    ol = FlyvisNative(brain, model=MODEL, gain=GAIN)
    own = np.flatnonzero(~np.isin(brain.graded, ol.neurons))
    ct, sc = brain.cell_type.astype(str), brain.superclass.astype(str)
    dn_types = sorted({t for t in ct[sc == "descending_neuron"] if all(len(brain.cells([t], s)) for s in "LR")})
    groups = {"HS": {s: brain.cells(HS, s) for s in "LR"}, "H2": {s: brain.cells(["H2"], s) for s in "LR"}}
    groups.update({t: {s: brain.cells([t], s) for s in "LR"} for t in dn_types})
    return brain, ol, own, groups, dn_types


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "rewirings": {}}
    ref = FlyBrain(batch=6, dt=DT, refractory=REFRACTORY)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic)
    rest_ref_hz = measure_1d(ref, SCENES_1D["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    del ref
    missed = []
    tfmt = lambda x: x["t"] if isinstance(x["t"], str) else round(x["t"])
    for k in REWIRINGS:
        t1 = time.perf_counter()
        brain, ol, own, groups, dn_types = build(k)
        v = run_config(brain, ol, SEED, rest_pop, rest_ref_hz, own, groups, dn_types)
        abolished = not rises(v["hs"], 3) and not rises(v["steer"], 2)
        missed.append(abolished)
        results["rewirings"][k] = {"abolished": abolished, **v}
        print(f"rewiring {k}: {'abolished' if abolished else 'SURVIVES'} | REST {v['REST']} pop {v['rest_pop_hz']} | "
              f"HS {v['hs']['delta']:+.1f}(t{tfmt(v['hs'])}) | STEER {v['steer']['delta']:+.1f}(t{tfmt(v['steer'])}) | "
              f"DN types with a direction signal {v['descending_significant']}/{v['descending_tested']} "
              f"({time.perf_counter() - t1:.0f} s)", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        del brain, ol
    results["pass"] = bool(all(missed))
    results["seconds"] = round(time.perf_counter() - t0)
    print("PASS: the signal needs the wiring" if results["pass"] else "FAIL: the signal survives scrambled wiring", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
