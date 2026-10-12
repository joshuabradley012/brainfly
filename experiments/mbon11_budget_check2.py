"""Exploratory measurement, written before it runs, not a test and not a change to the model: mbon11_budget_check.py's
budget again, on the model apl_refit2.py's rule kept (mb_calibration6.py).

mbon11_budget_check.py measured MBON11_R's Kenyon cell input budget on mb_calibration7.py, whose halved drive onto APL
apl_refit.py had chosen on DoOR's input. apl_refit2.py made the same choice on receptor_fills.RECOMMENDED, the input
rung 9 and this measure run on, and its rule kept mb_calibration6.py's drive (1), so mb_calibration7.py was withdrawn.
This repeats the measurement on mb_calibration6.py, so that the README's numbers describe the model in use.
Model: mbon11_budget_check.py's, with mb_calibration6.apply in place of mb_calibration7.apply; its code, seeds
(640000) and measures unchanged. Expected from learning pilots 16 and 17 (the same two models, the learning test's
protocol): about a tenth fewer synapse-spikes to 3-octanol (259 against 285 Kenyon cells, 63 against 71 pC) and
4-methylcyclohexanol's unchanged.

    python experiments/mbon11_budget_check2.py      (writes experiments/mbon11_budget_check2.json)
"""
from __future__ import annotations

from pathlib import Path

import mbon11_budget_check as m

OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    import mb_calibration6
    import mb_calibration7
    m.OUT = OUT
    mb_calibration7.apply = mb_calibration6.apply           # mbon11_budget_check.main calls mb_calibration7.apply
    m.__doc__ = __doc__                                     # its JSON's question
    m.main()


if __name__ == "__main__":
    main()
