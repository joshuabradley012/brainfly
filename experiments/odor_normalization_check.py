"""Exploratory check, not pre-registered: does the model's presynaptic inhibition grow with an odor's total receptor input
as flies' normalization does?

Olsen, Bhandawat & Wilson 2010 describe a projection neuron's response to its receptor neurons' rate r as Rmax r^1.5 /
(sigma^1.5 + r^1.5 + (m s)^1.5), where s is the summed receptor input to the other glomeruli: the suppression grows as
the 1.5 power of the odor's total input, so a weak odor is suppressed much less than a strong one (Luo, Axel & Abbott 2010
use m = 0.05 with s summed over 20 receptors; Olsen et al.'s own population model 10.63 / 190, about 0.056, over 24
glomeruli). Written as a divisor of r (Rmax (r / D)^1.5 / (sigma^1.5 + (r / D)^1.5)) that is D = (1 + (m s / sigma)^1.5)^(2/3),
whose excess D - 1 grows with s at a log-log slope between 1 and 1.5. The model's presynaptic inhibition is fitted to
Olsen & Wilson 2008's EPSCs during five strong odors (odor_probe28.py), so how it scales with s comes from its LNs.
research_notes/Rung 9 learning data/weak_input_gain.md, section 8: through Olsen et al.'s equation the receptor input
the evidence supports would nearly equalize 4-methylcyclohexanol with 3-octanol, where the model doesn't.
Model: odor_probe56.py's (its cache), or another's through measure(). Measured for sixteen odors (DoOR's input): the summed
evoked receptor rate over the first 0.5 s after the model's odor onset (each glomerulus's rate over its spontaneous rate,
summed over glomeruli), and the presynaptic divisor over the same 0.5 s (2 seeds of 8 flies, from a settled start); the
log-log slope of D - 1 against s, the model's and the equation's (m 0.05, sigma 12; the model sums over about 50
glomeruli, so the equation's D is high in absolute terms but its slope isn't).

Ran (odor_probe56.py's model): no; the model's inhibition grows about half as steeply as flies' normalization. D - 1
rises with the summed input at a log-log slope of 0.64, the equation's at 1.20. The strong odors (summed input 970-1,200
spikes/s, among them the five the inhibition was fitted to and 3-octanol) are divided by 2.3-2.7, the weaker ones
(360-580: 4-methylcyclohexanol, methyl salicylate, geranyl acetate, acetophenone) by 1.8-2.0; the equation, scaled to
the strong odors' 2.6, would divide the weaker ones by about 1.4-1.7. So a flatter inhibition takes more from weak
odors relative to strong ones than flies' does, which is one reason 4-methylcyclohexanol falls behind 3-octanol
(odor_probe59.py tests a steeper one).

    python experiments/odor_normalization_check.py      (writes experiments/odor_normalization_check.json)

Note (2026-10-11): this file's name first held a different check, Olsen et al.'s pentyl acetate suppression (commit
b654576), which writing this one overwrote; that check is restored unchanged as odor_pentyl_suppression_check.py.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe44 as p44
import odor_probe56 as p56
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 810000
ODORS = ("1-hexanol", "pentyl acetate", "propyl acetate", "2,3-butanedione", "e2-hexenal", "3-octanol", "4-methylcyclohexanol",
         "ethyl acetate", "isopentyl acetate", "benzaldehyde", "2-heptanone", "methyl salicylate", "ethyl butyrate",
         "geranyl acetate", "1-octen-3-ol", "acetophenone")
M, SIGMA = 0.05, 12.0


def olsen_divisor(s: float) -> float:
    return float((1 + (M * s / SIGMA) ** 1.5) ** (2 / 3))


def gain(b) -> np.ndarray:
    """The presynaptic gain of each trial now, from the installed inhibition (its k, offsets and powers)."""
    pres = b._presynaptic
    k, n = np.asarray(pres["k"], float), len(pres["k"])
    off, power = np.broadcast_to(np.asarray(pres["offset"], float), n), np.broadcast_to(np.asarray(pres["power"], float), n)
    a = np.maximum(np.asarray(b.presynaptic_state, float) - off, 0.0)
    return 1.0 / (1.0 + (k * a ** power).sum(1))


def measure(o, rec, seed: int = SEED) -> dict:
    b = o.brain
    piece = int(round(p10.PIECE / b.dt))
    ts = np.arange(0.0, 0.5, p10.PIECE)
    first = {g: rec.cells[g][0] for g in rec.glomeruli if len(rec.cells[g])}
    of_cell = {c: g for g, c in first.items()}
    rows = {}
    with warm.settled(o, rec):
        for j, odor in enumerate(ODORS):
            plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
            s = sum(max(hz - rec.spont[of_cell[cells[0]]], 0.0) for t in ts for cells, hz in rec.at(plan, t)
                    if cells[0] in of_cell) / len(ts)
            gains = []
            for k in range(2):
                b.reset(seed + 10 * j + k)
                b.set_release(o.s.ol.neurons, o.s.silent)
                for t in ts:
                    b.advance(piece, drive=rec.at(plan, t))
                    gains.append(float(gain(b).mean()))
            rows[odor] = {"summed_evoked_hz": round(float(s), 1), "divisor": round(1.0 / float(np.mean(gains)), 3),
                          "olsen_divisor": round(olsen_divisor(s), 3)}
            print(f"{odor:22s}", json.dumps(rows[odor]), flush=True)
    s = np.array([r["summed_evoked_hz"] for r in rows.values()])
    d, do = np.array([r["divisor"] for r in rows.values()]), np.array([r["olsen_divisor"] for r in rows.values()])
    out = {"odors": rows, "slope_model": round(float(np.polyfit(np.log(s), np.log(d - 1), 1)[0]), 3),
           "slope_olsen": round(float(np.polyfit(np.log(s), np.log(do - 1), 1)[0]), 3)}
    print("log-log slope of D - 1 against the summed input: model", out["slope_model"], "Olsen et al.'s", out["slope_olsen"], flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe56", p56.build, p44.prepare)
    out = {"question": __doc__, "m": M, "sigma": SIGMA, **measure(o, rec)}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
