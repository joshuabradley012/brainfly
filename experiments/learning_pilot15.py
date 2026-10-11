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

Ran (2026-10-11, 15 minutes): with the rest held, set C passes three marks of four and fails the unpaired. The cells
rest within 0.45 mV of their targets, the alpha'/beta' cells firing 0.010 spikes/s at rest (pilot 13 0.12).
Before pairing:
- 265 Kenyon cells answer 3-octanol and 57 4-methylcyclohexanol, 0.22 as many (pilot 13 479 and 129).
- MBON11 gains 28.1 and 4.4 spikes (pilot 13 45.8 and 9.5; learning pilot 12 70.8 and 11.4; flies 118 and 110). It
  peaks at 55 spikes/s to 3-octanol and fires 23 from 0.5 to 1 s.
- Its slow current peaks at 126 pA and carries 64 pC (flies about 400 and 245-250).
  PAIRED      passes: 3-octanol's spikes fall 93.9%, 35.6 points more than 4-methylcyclohexanol's.
  UNPAIRED    fails: 4-methylcyclohexanol's spikes fall 58.3% and its charge 55.4% (band 10-45%; flies 27%).
  RECIPROCAL  passes: 4-methylcyclohexanol paired cuts its own 97.0% and 3-octanol's 25.1% (band 15-50%; flies 38%).
  BACKWARD    passes: the paired odor's charge changes 0.4% and 6.5%.
So pilot 13's "one mark of four" came from its cells resting nearer threshold. Held, set C fails only the unpaired,
the mark the crux predicts. 4-methylcyclohexanol's cells sit mostly inside 3-octanol's (0.61 of them answer
3-octanol in kc_setc_check2.py; flies 0.33), so pairing 3-octanol takes 55% of 4-methylcyclohexanol's charge, twice
flies' 27%. Pairing 4-methylcyclohexanol now takes 25% of 3-octanol's (learning pilot 12 about 10%), enough for the
reciprocal. The unpaired drop rests on a small response (4.4 spikes before pairing, 1.8 after), but the charge, which
has no such noise, fails too.
Set C also leaves MBON11 answering weakly: a quarter of flies' spikes to 3-octanol and a twenty-fifth to
4-methylcyclohexanol, its gamma Kenyon cells answering a sixth as much as now. By the rule above there is no second
attempt. Set C stays a candidate, and the unpaired mark waits on 4-methylcyclohexanol's input.

Correction (2026-10-11, after a second independent review): "pairing 3-octanol takes 55% of 4-methylcyclohexanol's
charge, twice flies' 27%" compares the model's charge drop with flies' spike drop. Flies' charge drops are 20% and
35% (rung9_learning.py, from Hige et al.'s Figs. 3D and 4H), so the model's is 1.6-2.8 times flies'. Its spike drop,
58.3% against 27%, is 2.2 times.

Correction (2026-10-11, kc_input_audit.py): set C's synapses were scaled from the model's own EPSP, 1.90 mV per
connection (kc_setc_check.py's correction), so they carried about 5.5 mV per connection at 115 spikes/s, not
kc_integration.md's 3.9 (flies about 4.4).

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
