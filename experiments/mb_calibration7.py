"""APL refitted on the corrected Kenyon cell input, as apl_refit.py's rule chose it (2026-10-11).

mb_calibration6.py corrected the Kenyon cells' projection neuron input to its measured size (1.4 mV per spike at full
strength; it had been 1.90). APL's strength and drive had been chosen with the strong input (odor_apl_conductance2_check
.py, mb_calibration4.py). apl_refit.py made that choice again on the corrected input, by the same rule: among the
conditions whose silencing raises both odors' Kenyon cell spikes 2-3-fold, the one whose APL peak ratio
(4-methylcyclohexanol over 3-octanol) is nearest flies' 0.49. It chose the Kenyon cells' drive onto APL at half
MaleCNS's weight: silencing APL then raises the spikes 2.37 and 2.36-fold, and APL answers 4-methylcyclohexanol with
0.43 of its peak for 3-octanol. At mb_calibration4.py's full weight it was 2.77, 2.57 and 0.36. APL's conductance stays
mb_calibration4.py's: reversal 20 mV below each class's rest, 1.22 times the leak at APL's ceiling, decaying over 0.3 s.

Withdrawn (2026-10-11): apl_refit.py made its choice on DoOR's input, as odor_apl_conductance2_check.py did, not on
receptor_fills.RECOMMENDED, the input rung 9 runs on. apl_refit2.py made it again there, with drive 0.25 added, and
its rule kept drive 1 (mb_calibration6.py's APL): at drive 0.5 silencing APL raises 4-methylcyclohexanol's spikes
only 1.95-fold. By the reading written before that run, this module is withdrawn and mb_calibration6.py stays the
model. It is kept so that learning_pilot17.py and mbon11_budget_check.py, which ran on it, can be rerun.

    import mb_calibration7
    mb_calibration7.apply(o)              # in place of mb_calibration4.apply(o) (and mb_calibration6's correction);
                                          # mb_calibration5.install(o) after the MBON11 setup, as before
"""
from __future__ import annotations

import mb_calibration
import mb_calibration4
import mb_calibration6

KC_APL_DRIVE = 0.5                            # apl_refit.py's choice (mb_calibration4.py: 1.0)


def apply(o) -> dict:
    """mb_calibration.apply, mb_calibration6.correct, then APL installed with mb_calibration4.py's conductance and
    KC_APL_DRIVE; returns what was set."""
    out = mb_calibration.apply(o)
    out["correction"] = mb_calibration6.correct(o)
    rev = mb_calibration4.install(o, KC_APL_DRIVE, mb_calibration4.APL_KC_EFFECT, mb_calibration4.REVERSAL_MV,
                                  o.brain.weights.copy(), mb_calibration4.TAU_S)
    out.update({"kc_apl_scale": KC_APL_DRIVE, "kc_apl_drive": KC_APL_DRIVE, "apl_kc_effect": mb_calibration4.APL_KC_EFFECT,
                "apl_kc_reversal_mv_from_rest": mb_calibration4.REVERSAL_MV, "apl_kc_reversal_mv_by_type": rev,
                "apl_kc_tau_s": mb_calibration4.TAU_S, "graded_apl": "mb_calibration7.py"})
    return out
