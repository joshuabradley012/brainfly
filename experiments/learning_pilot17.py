"""Exploratory, not pre-registered: rung 9's learning test on the corrected Kenyon cell input with APL refitted around it
(mb_calibration7.py).

mb_calibration6.py corrected the Kenyon cells' projection neuron input to 1.4 mV per spike. learning_pilot16.py: the
marks came out as learning pilot 12's, the reciprocal at 4.2%, and MBON11 answered at about a quarter of flies'
strength. A review then pointed out that APL's strength and drive had been chosen with the strong input.
apl_refit.py made that choice again on the corrected input, by odor_apl_conductance2_check.py's rule, unchanged. It
halved the Kenyon cells' drive onto APL: silencing APL raises the spikes 2.37 and 2.36-fold (flies 2-3), and APL
answers 4-methylcyclohexanol with 0.43 of its peak for 3-octanol (flies 0.49). With APL driven half as hard, more
Kenyon cells answer each odor (apl_refit.py, on its own seeds and input: 330 and 97 against 305 and 91).
Model: learning pilot 16's, with mb_calibration7.apply in place of mb_calibration4.apply and mb_calibration6.correct.
It is run by learning_pilot13.py's own code: its mb_calibration4.apply replaced by mb_calibration7.apply, its set_c by
a step that changes nothing, its rest set by kc_rest.fit. Protocol, rule, fit, seeds and measures are learning pilot
12's, without the flash.
Rung 9's marks reported as rung9_learning.py states them. If all four pass with this input, rung 9's standing rule
allows a second attempt (the input the evidence supports, the model fixed by measurements and stated rules, fresh
seeds). If not, the failing marks say where the model stands.

Ran (2026-10-11, 15 minutes): the marks come out as learning pilot 16's. The rest held (within 0.3 mV in each class).
Before pairing:
- 285 Kenyon cells answer 3-octanol and 38 4-methylcyclohexanol (learning pilot 16: 259 and 38).
- MBON11 gains 30.2 and 3.3 spikes (27.0 and 3.3; flies 118 and 110).
- Its slow current peaks at 140 pA and carries 71 pC (131 and 63; flies about 400 and 245-250).
  PAIRED      passes: 3-octanol's spikes fall 93.3%, 55 points more than 4-methylcyclohexanol's.
  UNPAIRED    passes: 4-methylcyclohexanol's spikes fall 38.7% and its charge 33.2% (band 10-45%; flies 27%).
  RECIPROCAL  fails: 4-methylcyclohexanol paired cuts its own 92.2% but 3-octanol's only 4.7% (band 15-50%; flies 38%).
  BACKWARD    passes: the paired odor's charge changes 0.0% and 0.3%.
So halving APL's drive raises 3-octanol's Kenyon cells and MBON11's response by a tenth, and leaves
4-methylcyclohexanol's 38 cells as they were. By the rule there is no second attempt. With the corrected input and APL
refitted around it, rung 9 fails where it always has: pairing 4-methylcyclohexanol takes 5% of 3-octanol's charge, as
the rule fits it (flies' response falls 38%).

    python experiments/learning_pilot17.py      (writes experiments/learning_pilot17.json)
"""
from __future__ import annotations

import types
from pathlib import Path

import kc_rest
import learning_pilot13 as lp13

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    import mb_calibration4
    import mb_calibration7
    lp13.OUT = OUT
    mb_calibration4.apply = mb_calibration7.apply           # learning_pilot13.main calls mb_calibration4.apply
    lp13.set_c = lambda o: {"model": "mb_calibration7.apply"}   # in place of set C's Kenyon cells: nothing more
    lp13.p33 = types.SimpleNamespace(set_rest=kc_rest.fit)   # learning_pilot13.main's only use of odor_probe33
    lp13.__doc__ = __doc__                                  # its JSON's question
    lp13.main()


if __name__ == "__main__":
    main()
