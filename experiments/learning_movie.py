"""Recording, not a test: learning_pilot11.py's protocol with the weighed input, keeping MBON11's spikes over time, for
the README's animation of rung 9's learning test (assets/learning_movie.py).

learning_pilot11.py ran Hige et al.'s pairing on the current model (odor_probe60.py's antennal lobe, mb_calibration4.py's
mushroom body) and reported MBON11's evoked spikes before and after pairing. This repeats its weighed-input condition
with the same seeds (learning_pilot4.variant, 640000), so its numbers should repeat, and keeps, for every trial,
MBON11's spikes in 10 ms bins (mean over flies) from 0.5 s before the odor to 1.5 s after its onset. learning_pilot3.trial
is wrapped for that and is otherwise unchanged.

Ran (2026-10-11, 14 minutes): learning pilot 11's numbers repeat to the hundredth (MBON11's evoked spikes before pairing
38.57 to 3-octanol and 8.48 to 4-methylcyclohexanol; 3-octanol paired, 88.7% and 38.5% fewer; 4-methylcyclohexanol
paired, 98% and 10.2%). The time courses show what the totals hid. Smoothed as Hige et al. smoothed theirs (a Gaussian,
SD 50 ms; assets/learning_movie.py), MBON11's response to 3-octanol peaks at 144 spikes/s 85 ms after the odor's onset
(358 in 10 ms bins), about as high as flies' (135-140 at about 0.3 s; Hige et al. 2015, Fig. 1E), but 79% of its evoked
spikes come in the first 0.3 s, and from 0.5 to 1 s it fires 12.4 spikes/s (5.7 at rest) where flies' holds 95-100. To
4-methylcyclohexanol it peaks at 57 and is back at rest by 0.3 s (flies 135, then about 100). So the model's MBON11 gains
a third of flies' spikes to 3-octanol (38.6 against 118) for want of a sustained response, not a peak.

    python experiments/learning_movie.py      (writes experiments/learning_movie.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import learning_pilot as lp
import learning_pilot3 as lp3
import learning_pilot4 as lp4
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 640000
CHARGE_PC = 0.030 * 34.5 / 19.0
CALLS = []


def wrap(trial):
    """learning_pilot3.trial, recording MBON11's spikes per bin from -0.5 to 1.5 s around the odor's onset."""
    def recorded(o, rec, odor, seed, mbon, kc, f, recover_s):
        b = o.brain
        plain = b.advance
        bins = []

        def advance(*args, **kwargs):
            c = plain(*args, **kwargs)
            bins.append(float(c[:, mbon].mean()))
            return c
        b.advance = advance
        try:
            out = trial(o, rec, odor, seed, mbon, kc, f, recover_s)
        finally:
            del b.advance                                  # back to the class's method
        n_pre = int(round(lp.PRE / lp.BIN))
        series = np.array(bins[1:])                        # the first advance is the 0.5 s settle
        CALLS.append({"odor": odor, "seed": int(seed), "mbon11_hz": np.round(series[n_pre - 50:n_pre + 150] / lp.BIN, 2).tolist(),
                      "evoked_spikes": float(np.mean(out["mbon"]))})
        return out
    return recorded


def main() -> None:
    t0 = time.perf_counter()
    lp3.CHARGE_PC = CHARGE_PC
    lp4.SEED, lp4.OUT = SEED, OUT.with_name(OUT.stem + "_variant.json")
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    lp3.trial = wrap(lp3.trial)
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "bin_s": lp.BIN, "t0": -0.5}
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        out["result"] = lp4.variant(o, rec, True, {"variants": {}})
    out["calls"] = CALLS
    lp4.OUT.unlink(missing_ok=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print(f"done ({out['seconds']} s), {len(CALLS)} trials recorded", flush=True)


if __name__ == "__main__":
    main()
