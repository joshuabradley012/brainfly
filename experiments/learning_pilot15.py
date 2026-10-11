"""Exploratory, not pre-registered: learning pilot 13 again with the Kenyon cells' rest held, as it meant to hold it.

learning_pilot13.py installed set C's Kenyon cells (a 50 ms membrane, the projection neuron-to-Kenyon cell synapses
depressing on their own to 0.85 per spike, recovering over 0.1 s) and set their rest with odor_probe33.set_rest, which
left them closer to threshold than the targets: alpha/beta by 3.1 mV, alpha'/beta' by 4.3-4.5 and gamma by up to 3.1,
the alpha'/beta' cells firing 0.12 spikes/s at rest, 30 times learning pilot 12's (kc_rest.py gives the cause). Its
result, the reciprocal mark passing and the other three failing, is in the README.
Model, protocol, rule, fit, seeds and measures: learning_pilot13.py's, run by its own code, with kc_rest.fit setting the
rest in place of odor_probe33.set_rest (same targets and seed).
Rung 9's marks reported as rung9_learning.py states them, and read as pilot 13's: if all four pass with this input,
rung 9's standing rule allows a second attempt (the input the evidence supports, set C chosen from Gruntman & Turner's
measurements before any learning result, fresh seeds); if not, set C stays a candidate. Either way pilot 13's result
is corrected by this one in the README.

    python experiments/learning_pilot15.py      (writes experiments/learning_pilot15.json)
"""
from __future__ import annotations

import types
from pathlib import Path

import kc_rest
import learning_pilot13 as lp13

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    lp13.OUT = OUT
    lp13.p33 = types.SimpleNamespace(set_rest=kc_rest.fit)   # learning_pilot13.main's only use of odor_probe33
    lp13.__doc__ = __doc__                                  # its JSON's question
    lp13.main()


if __name__ == "__main__":
    main()
