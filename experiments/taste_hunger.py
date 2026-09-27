"""Exploratory, not pre-registered: does hunger's gain on sugar neurons' output bring taste back to the
resting brain?

Sugar no longer moves MN9 in the resting brain (taste_at_rest.py; escape_at_rest.py's model, +1.9 Hz),
and none of the depression rules tried brings it back (depression_rules.py, depression_classes.py).
Real flies are tested for proboscis extension starved, and research_notes/Rung 4 resting state
data/short_term_plasticity.md (section 4.3, from the taste sub-agent's summary, unchecked) reports
hunger acting mainly as a gain on sugar GRNs' output: presynaptic calcium 1.3-3 times higher with
starvation, through dNPF, dopamine and DopEcR on the GRNs (Inagaki et al. 2012), with spike rates
unchanged. Shiu et al. 2024 also chose their one weight so that sugar at 100 Hz gives MN9 about 80%
of its maximum, which puts rung 1's route at the edge of its amplification by construction.
Here every synapse from a sugar GRN (shiu_baseline.py's SETS, both sides) is multiplied by a gain g
in escape_at_rest.py's model, with escape_at_rest.py's calibrated biases unchanged (GRNs are silent
at rest, so the resting brain is the same). Measured as escape_at_rest.py measures taste (MN9 L's
rise over its rest under 1 s of sugar at 100 Hz, at 10 Hz, and sugar with bitter; 8 flies), for
g = 1, 1.5, 2, 3, and 5 and 10 beyond what hunger does, to see how far the route is from working.

    python experiments/taste_hunger.py            (writes experiments/taste_hunger.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import escape_at_rest as escape
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
from shiu_baseline import SETS

OUT = Path(__file__).with_suffix(".json")
FULL_NETWORK = attempt1.network
GAINS = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0]


def with_gain(g: float):
    def network():
        M, scale, labels, types, superclass = FULL_NETWORK()
        sugar = np.isin(labels["cell_type"], SETS["sugar"]) | np.isin(types, SETS["sugar"])
        return (M.tocsr() @ sparse.diags(np.where(sugar, g, 1.0))).tocsr(), scale, labels, types, superclass
    return network


def main() -> None:
    t0 = time.perf_counter()
    attempt2.model = escape.model
    bias = np.load(escape.HERE / "intact.npz")["bias"]
    out = {"question": __doc__, "gains": []}
    for g in GAINS:
        attempt1.network = with_gain(g)
        s = eyes.Setup(None, seed=5)
        s.bias = bias.copy()
        s.brain.set_bias(s.bias[s.gid])
        out["gains"].append(r := {"gain": g, **escape.taste(s)})
        print(json.dumps(r), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
