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

Ran (2026-10-11, 3 minutes): a fifth fewer synapse-spikes to 3-octanol, not the tenth expected, and
4-methylcyclohexanol's nearly unchanged.
- 3-octanol: 3,536 synapse-spikes onto MBON11_R from every above-rest spike (3,355 from the responders), against
  flies' budget of 3,206 (1,300-7,500) on the same synapse counts.
  - gamma-main and gamma-s: 3.3% respond (flies 3.5%), with 1.45 spikes each (flies about 3.5).
  - alpha/beta s, m and c: 8.6% with 2.6 (flies 6% with 2.5; the derived range is 4-8%).
  - alpha'/beta': 18.7% with 2.8 (flies 20% with 5).
- At 0.054 pC per synapse with no depression, that carries 191 pC (flies 245-250). The depression leaves 0.54 of it,
  114 pC.
- 4-methylcyclohexanol: 434 synapse-spikes, 0.14 of flies' budget. That is 23 pC undepressed and 17 after the
  depression (flies 230-273).
The share responding and the spikes each responder fires both fall with APL at full drive. Their product falls more
(0.80 of mbon11_budget_check.py's 4,401) than learning pilots 16 and 17 differed (0.91 in Kenyon cells, 0.89 in charge).
So on the model in use, the Kenyon cells give MBON11_R 1.1 times flies' budget of synapse-spikes to 3-octanol. That
would carry 0.77 of flies' charge undepressed and 0.46 after the depression. mbon11_budget_check.py's derived figures
scale with it. With 3% of cells flashed in Yamada et al.'s calibration instead of 5%, MBON11_R would get about 190 pC
(114 x 5/3). Flies' charge would need about 2.3%, below the borrowed 3-7%.

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
