"""Exploratory, not pre-registered: rung 9's learning test with the Kenyon cells' projection neuron input at its measured
size (mb_calibration6.py).

kc_input_audit.py: one projection neuron spike gave a Kenyon cell 1.90 mV, a third more than the 1.4 mV mb_calibration.py
meant (Turner et al. 2008; Gruntman & Turner 2013 1.24-1.48), because the synapses don't depress. kc_epsp_check.py: at
1.4 mV the cells answer 3-octanol at 7.4% (flies about 12%) and 4-methylcyclohexanol with 0.14 as many cells, and
MBON11's input would carry 76 pC (flies 245-250). Its rule adopted the corrected input.
Model: learning pilot 12's (mb_calibration5.py's slow Kenyon cell current included), with mb_calibration6.correct after
mb_calibration4.apply. That sets the Kenyon cells' 20 ms membrane in their type, and their projection neuron synapses at
1.4 mV per spike at full strength. The rest is set with kc_rest.fit. It is run by learning_pilot13.py's own code, with
its set_c replaced by mb_calibration6.correct, so the JSON's "set_c" entry holds the correction. Protocol, rule, fit,
seeds and measures are learning pilot 12's, without the flash.
Rung 9's marks reported as rung9_learning.py states them. If all four pass with this input, rung 9's standing rule
allows a second attempt (the input the evidence supports, its size fixed from measurements before any learning result,
fresh seeds). If not, the failing marks say where the corrected model stands.

Ran (2026-10-11, 15 minutes): the marks come out as learning pilot 12's did, the reciprocal further off, and MBON11
answers more weakly. The cells' rest held (within 0.3 mV in each class).
Before pairing:
- 259 Kenyon cells answer 3-octanol and 38 4-methylcyclohexanol, 0.15 as many (learning pilot 12: 567 and 85).
- MBON11 gains 27.0 and 3.3 spikes (learning pilot 12 70.8 and 11.4; flies 118 and 110). It peaks at 57 spikes/s to
  3-octanol and fires 21.5 from 0.5 to 1 s.
- Its slow current peaks at 131 pA and carries 63 pC (flies about 400 and 245-250).
  PAIRED      passes: 3-octanol's spikes fall 93.7%, 56 points more than 4-methylcyclohexanol's.
  UNPAIRED    passes: 4-methylcyclohexanol's spikes fall 37.7% and its charge 31.6% (band 10-45%; flies 27%).
  RECIPROCAL  fails: 4-methylcyclohexanol paired removes its own response (104%, to just below rest) but cuts
              3-octanol's only 4.2% (band 15-50%; flies 38%).
  BACKWARD    passes: the paired odor's charge changes 0.0% and 0.4%.
4-methylcyclohexanol's 38 cells carry 5% of 3-octanol's charge (learning pilot 12: 11.5%), so pairing it barely
touches 3-octanol. By the rule there is no second attempt. With its input at the measured size, the model's
4-methylcyclohexanol is weaker still. Its MBON11 answers 3-octanol at a quarter of flies' strength and
4-methylcyclohexanol at a thirtieth. Rung 9's crux, 4-methylcyclohexanol's small Kenyon cell set, stands, and the
corrected input adds a second gap: too little Kenyon cell drive overall.

Correction (2026-10-11, after a review):
- "4-methylcyclohexanol's 38 cells carry 5% of 3-octanol's charge (learning pilot 12: 11.5%)": 5% and 11.5% are the
  drops in 3-octanol's charge that the fitted rule gives when 4-methylcyclohexanol is paired, not the shares of
  3-octanol's charge its cells carry (rung9_learning.py keeps the two apart).
- "Too little Kenyon cell drive overall" rests on fits made with the input a third too strong: the gamma cells' +11
  mV gap (gamma_gap_refit.py has since kept it on the corrected input), the Kenyon cells' drive onto APL (MaleCNS's
  weight; mb_calibration.py's x 10 is replaced by mb_calibration4.py), and APL's conductance design. apl_refit.py and
  apl_refit2.py have since fitted APL's drive again.

Correction (2026-10-11, review 7):
- The earlier correction's last sentence was amended in place on 2026-10-11 (commit 425d6bd). Before, it read "...the
  Kenyon cell-to-APL x 10, and APL's conductance design. The last two haven't been refitted."
- Every fit it lists has now been made again and kept. On this pilot's own model, mbon11_budget_check2.py finds the
  Kenyon cells giving MBON11_R 1.1 times flies' budget of synapse-spikes to 3-octanol. So the Ran's "too little Kenyon
  cell drive overall" is a shortfall in the charge each spike carries, not in the cells' activity.

Correction (2026-10-11, review 8):
"A shortfall in the charge each spike carries, not in the cells' activity" is a little strong: the pilot's own
charge, 63 pC, is 0.66-0.73 of the budget measure's equivalent (87-96 pC), and the gamma cells, 59% of MBON11_R's
Kenyon cell synapses, give 0.79 of flies' gamma budget. It is mostly a shortfall in charge per spike.

    python experiments/learning_pilot16.py      (writes experiments/learning_pilot16.json)
"""
from __future__ import annotations

import types
from pathlib import Path

import kc_rest
import learning_pilot13 as lp13
import mb_calibration6

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    lp13.OUT = OUT
    lp13.set_c = mb_calibration6.correct                    # in place of set C's Kenyon cells
    lp13.p33 = types.SimpleNamespace(set_rest=kc_rest.fit)   # learning_pilot13.main's only use of odor_probe33
    lp13.__doc__ = __doc__                                  # its JSON's question
    lp13.main()


if __name__ == "__main__":
    main()
