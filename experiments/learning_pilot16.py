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
