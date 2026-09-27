"""Exploratory, not pre-registered: depression by synapse class in the resting brain, and taste.

depression_rules.py found no uniform depression rule that keeps the resting brain calm and lets
sugar reach MN9. research_notes/Rung 4 resting state data/short_term_plasticity.md assigns depression by
presynaptic class instead (escape_at_rest.py's model), with unmeasured central cholinergic neurons as
the knob: 0.9 of the strength left per spike, recovering in 0.2 s first, 0.5 s if loops persist. And
if the subesophageal interneurons still block taste, it suggests exempting the neurons that take most
of their input from gustatory receptor neurons. Measured as in depression_rules.py (eyes_at_rest.py's
setup and eyes-open biases, 12 fresh-start rounds, 8 flies): rest, taste and looming at gain 1, for
  class rule, central recovery 0.2 s
  class rule, central recovery 0.5 s                (escape_at_rest.py's model)
  the same, plus neurons taking at least 20% of their input synapses from GRNs left undepressed
  the same as escape_at_rest.py's model, but visual projection neurons depressed mildly and fast
      (0.95 / 0.3 s, the notes' "if any"), since escape_at_rest.py found the left LPLC2, LC4 and giant
      fiber running at rest (28, 8 and 28 Hz) with them undepressed
Also reported: each fly's resting LPLC2 L, LC4 L and giant fiber L rates (blank scene, gain 1).

    python experiments/depression_classes.py            (writes experiments/depression_classes.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import depression_rules as rules
import escape_at_rest as escape
import eyes_at_rest as eyes
import rest_calibration as attempt1

OUT = Path(__file__).with_suffix(".json")
GRN_PREFIXES = ("LB", "PhG", "claw_tpGRN", "dorsal_tpGRN", "LgLG", "WG", "SNch")


def class_model(recovery: float, grn_share: float, vpn: dict | None = None):
    def model(types, superclass):
        spec, sets = escape.model(types, superclass)
        spec["cholinergic"] = {"depression": 0.9, "recovery": recovery}
        if vpn is not None:
            spec["vpn"] = vpn
            sets["vpn"] = np.intersect1d(sets["cholinergic"], np.flatnonzero(superclass == "visual_projection"))
        if grn_share > 0:
            C = abs(attempt1.network()[0].tocsr())
            grn = np.zeros(len(types), bool)
            for p in GRN_PREFIXES:
                grn |= np.char.startswith(types, p)
            share = np.asarray(C[:, np.flatnonzero(grn)].sum(1)).ravel() / np.maximum(np.asarray(C.sum(1)).ravel(), 1)
            sets["undepressed"] = np.union1d(sets["undepressed"], np.intersect1d(sets["cholinergic"], np.flatnonzero(share >= grn_share)))
        return spec, sets
    return model


def main() -> None:
    t0 = time.perf_counter()
    eyes.ROUNDS = [1.0] * 8 + [0.5] * 4
    out = {"question": __doc__, "rules": []}
    for label, recovery, share, vpn in (("class rule, central recovery 0.2 s", 0.2, 0.0, None),
                                        ("class rule, central recovery 0.5 s", 0.5, 0.0, None),
                                        ("class rule, 0.5 s, GRN-input neurons undepressed", 0.5, 0.2, None),
                                        ("class rule, 0.5 s, VPNs 0.95 / 0.3 s", 0.5, 0.0, {"depression": 0.95, "recovery": 0.3})):
        rules.rule_model = lambda rule, m=class_model(recovery, share, vpn): m
        out["rules"].append(r := rules.measure(label))
        print(json.dumps(r), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
