"""Exploratory, not pre-registered: why does rung 1's taste pathway fail in the resting brain?

taste_at_rest.py found that sugar no longer moves MN9 in rung 4's resting brain (rest_calibration2.py),
which has short-term depression at every cholinergic synapse. This takes rung 1's own brain, silent at
rest (shiu_rewiring.py's network and w_syn, no background, no biases), and adds only that depression,
at every cholinergic synapse or on part of them: MN9 L's rate under 1 s of sugar at 100 Hz, 8 trials,
and how many neurons pass 5 Hz. The ORN-to-PN values (Nagel, Hong & Wilson 2015: 0.78 of the strength
left per spike, recovering with 0.89 s) and a milder version (0.9). Also, instead of depression, every
inhibitory synapse (GABA, glutamate, histamine) made 1.5, 2 or 3 times stronger, the other common way
to keep a recurrent network calm.

    python experiments/taste_depression.py            (writes experiments/taste_depression.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
from brainfly.hybrid import HybridBrain, consensus_transmitters
from shiu_baseline import SETS
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    M, scale, labels, types, superclass = attempt1.network()
    ach = np.flatnonzero(consensus_transmitters() == "acetylcholine")
    sensory = np.flatnonzero(np.char.find(superclass, "sensory") >= 0)
    measured, mild = {"depression": 0.78, "recovery": 0.89}, {"depression": 0.9, "recovery": 0.89}
    cases = {"none (rung 1 as it passed)": (None, None),
             "every cholinergic synapse": (measured, ach), "every cholinergic synapse, milder": (mild, ach),
             "cholinergic sensory neurons only": (measured, np.intersect1d(ach, sensory)),
             "every cholinergic synapse but sensory neurons'": (measured, np.setdiff1d(ach, sensory))}
    for g in (1.5, 2.0, 3.0):
        cases[f"inhibition x{g:g}, no depression"] = (None, None, g)
    out = {"question": __doc__, "cases": {}}
    for label, case in cases.items():
        params, who, g = case if len(case) == 3 else (*case, 1.0)
        types_ = {} if params is None else {"depressing": params}
        sets = {} if who is None else {"depressing": who}
        Mg = M.tocsr(copy=True)
        Mg.data = np.where(Mg.data < 0, Mg.data * g, Mg.data)
        b = HybridBrain(trials=8, w_syn=W_SYN, matrix=Mg, scale=scale, labels=labels, seed=1, types=types_, sets=sets)
        r = b.run(1.0, drive=[(b.cells(SETS["sugar"], "L"), 100.0)], seed=3).rates
        out["cases"][label] = {"mn9_L_hz": round(float(r[b.cells(["MN9"], "L")].mean()), 1), "neurons_over_5hz": int((r > 5).sum())}
        print(label, out["cases"][label], flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
