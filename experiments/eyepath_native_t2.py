"""Does LC4 respond to looming when flyvis's T2 responds to light decrements, as a real T2 does?

eyepath_native.py ran FlyvisNative with flyvis's best model (flow/0000/000). Looming drove LPLC2 and
the giant fiber, but LC4, the other looming detector, didn't move (at most +0.16 Hz at any gain).
LC4's largest input is T2. In model 000, T2 depolarises to a full-field light increment (+2.9) and
not at all to a decrement (0.00), while a real T2 is excited by both (Keles et al. 2020), and a
looming dark disk is a decrement. Of flyvis's 50 flow models, 8 have a T2 that depolarises to both
flashes: each peak over 0.02, the smaller at least a third of the larger (flyvis's Flashes, radius
6, the central T2's peak change in the second after onset). They are 001, 003, 016, 026, 032, 040,
041 and 046. This test uses 001, the best of them by validation loss (second of all 50), whose T2
gives +1.3 to the increment and +2.8 to the decrement.
Everything else, the pass criteria included, is eyepath_native.py's: the same brain and scenes, the
gain sweep {0.3, 1, 3, 10} on seed 1 with 6 flies, and the lowest passing gain confirmed on seed 2
with 8 flies. Pass: REST, RELAY and SIDE at one gain, confirmed.

    python experiments/eyepath_native_t2.py            (writes experiments/eyepath_native_t2.json)
"""
from __future__ import annotations

from pathlib import Path

import eyepath_native

MODEL = "flow/0000/001"

if __name__ == "__main__":
    eyepath_native.main(model=MODEL, out=Path(__file__).with_suffix(".json"), criteria=__doc__)
