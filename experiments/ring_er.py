"""Exploratory, not pre-registered: does the head-direction ring hold a bump once its ring neurons are in?

ring_alone.py found no bump in the 152 neurons of the ring's own types at any uniform gains.
research_notes/Rung 4 resting state data/head_direction_models.md explains why. Ring neurons (ER) and
extrinsic ring neurons (ExR) supply 75% of the EPGs' input, as inhibition that is flat around the ring
and partly driven by the EPGs themselves, and no published model got a bump from synapse counts times
one weight. Its toy (a research agent's, run from the session scratchpad) held a bump with the ring
neurons added and three changes. This repeats that toy in the repo and scores it with rung 4's bump
measures. Network: the 460 neurons of the ring's types (EPG, EPGt, PEN_a, PEN_b, PEG, Delta7) plus
every ER and ExR type, with their MaleCNS wiring (rung 1's network: synapses over target size, w_syn
1.5556 mV), Poisson background (1 mV kicks at 200 Hz) and bias 0. The recipe:
  - SLOW       the excitatory edges from EPG, EPGt, PEN_a, PEN_b and PEG onto the ring's six types act
               through a 100 ms current, weighted by 5/100 so each spike delivers the same charge as
               through the usual 5 ms one
  - DEPRESSION short-term depression on those five types' outputs (0.9 of the strength left per spike,
               recovering in 0.3 s)
  - GAINS      every excitatory synapse in the sub-network times 3, every inhibitory one times 1.5
Conditions: the recipe; the recipe with each change taken away in turn; the ring's six types alone with
all three changes.
Measured, 8 runs each:
  spontaneous  30 s after 1 s to settle, no cue: rung 4's BUMP measures (strength per bridge side in
               1-s windows, the 99th percentile of 1,000 glomerulus-label shuffles, the resultant of the
               runs' mean positions; BUMP holds if strength >= 0.3 and above the shuffles on both sides
               and the resultant is under 0.6); in 1-s windows, the busiest wedge's rate and the bump's
               full width at half maximum over the 16 ellipsoid-body wedges, peak-aligned; each type's
               mean rate
  seeded       a 10 mV bias on the EPGs of 3 adjacent wedges for 0.3 s, at 8 positions 45 deg apart,
               then 10 s free: the bump's distance from the seed over the last second (held if under
               45 deg)
An EPG's wedge comes from its bridge glomerulus (the notes' map from EPG-to-EPG contacts): R_k to wedge
2k mod 16, L_k to (19 - 2k) mod 16.

    python experiments/ring_er.py            (writes experiments/ring_er.json)
"""
from __future__ import annotations

import json
import re
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy import sparse

import rest_calibration as attempt1
from brainfly.hybrid import TAU, HybridBrain
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
RING = ["EPG", "EPGt", "PEN_a(PEN1)", "PEN_b(PEN2)", "PEG", "Delta7"]
EXC = ["EPG", "EPGt", "PEN_a(PEN1)", "PEN_b(PEN2)", "PEG"]
RUNS, SPONTANEOUS, FREE, SEEDS = 8, 30, 10, range(0, 16, 2)
RECIPE = {"ring neurons": True, "slow": 0.1, "depression": {"depression": 0.9, "recovery": 0.3}, "gains": (3.0, 1.5)}


@lru_cache(maxsize=1)
def whole():
    M, scale, labels, types, superclass = attempt1.network()
    ring_neurons = sorted({t for t in types if re.match(r"^ER\d", t) or t.startswith("ExR")})
    return M.tocsr(), scale, labels, types, attempt1.epgs(types), ring_neurons


class Ring:
    def __init__(self, recipe: dict, trials: int, seed: int):
        M, scale, labels, types, (epg, side, glom), ring_neurons = whole()
        names = RING + (ring_neurons if recipe["ring neurons"] else [])
        sel = np.flatnonzero(np.isin(types, names))
        Ms = M[sel][:, sel].tocoo()
        pre, post = types[sel][Ms.col], types[sel][Ms.row]
        gE, gI = recipe["gains"]
        data = np.where(Ms.data > 0, Ms.data * gE, Ms.data * gI)
        slow = None
        if recipe["slow"]:
            m = np.isin(pre, EXC) & np.isin(post, RING) & (data > 0)
            slow = sparse.csr_matrix((data[m] * TAU / recipe["slow"], (Ms.row[m], Ms.col[m])), shape=(len(sel),) * 2)
            data = np.where(m, 0.0, data)
        W = sparse.csr_matrix((data, (Ms.row, Ms.col)), shape=(len(sel),) * 2)
        W.eliminate_zeros()
        spec = {"all": attempt1.BACKGROUND | {"bias": 0.0}}
        if recipe["depression"]:
            spec |= {t: dict(recipe["depression"]) for t in EXC}
        self.brain = HybridBrain(trials=trials, w_syn=W_SYN, matrix=W, slow=slow, tau_slow=recipe["slow"] or 0.1,
                                 scale=scale[sel], labels={k: v[sel] for k, v in labels.items()}, seed=seed, types=spec)
        at = {g: k for k, g in enumerate(sel)}
        self.epg, self.side, self.glom = np.array([at[i] for i in epg]), side, glom
        self.wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
        self.types = types[sel]

    def windows(self, seconds: int) -> tuple[np.ndarray, np.ndarray]:
        """EPG spike counts in 1-s windows (runs x windows x EPGs), and every neuron's mean rate."""
        b = self.brain
        w, total = [], np.zeros((b.trials, b.n))
        for _ in range(seconds):
            c = b.advance(int(round(1.0 / b.dt)))
            w.append(c[:, self.epg])
            total += c
        return np.stack(w, 1), total / seconds

    def profile(self, w: np.ndarray) -> np.ndarray:
        """Mean rate per ellipsoid-body wedge in each window (runs x windows x 16)."""
        return np.stack([w[..., self.wedge == k].mean(-1) for k in range(16)], -1)


def width_and_peak(p: np.ndarray) -> tuple[float | None, float]:
    """Peak-aligned full width at half maximum (deg) and the busiest wedge's rate (Hz), over windows."""
    flat = p.reshape(-1, 16)
    flat = flat[flat.max(1) > 0]
    if not len(flat):
        return None, 0.0
    aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in flat]).mean(0)
    return 22.5 * float((aligned >= aligned.max() / 2).sum()), float(flat.max(1).mean())


def spontaneous(recipe: dict) -> dict:
    r = Ring(recipe, RUNS, seed=1)
    b = r.brain
    b.advance(int(round(1.0 / b.dt)))
    w, rate = r.windows(SPONTANEOUS)
    bump = attempt1.bump(w, r.side, r.glom, np.random.default_rng(7))
    fwhm, peak = width_and_peak(r.profile(w))
    ok = all(bump[s]["strength"] >= 0.3 and bump[s]["strength"] > bump[s]["shuffle_p99"] and bump[s]["resultant"] < 0.6 for s in "LR")
    groups = {"EPG": ["EPG"], "PEN_a": ["PEN_a(PEN1)"], "PEN_b": ["PEN_b(PEN2)"], "PEG": ["PEG"], "Delta7": ["Delta7"],
              "ER": [t for t in set(r.types) if t.startswith("ER")], "ExR": [t for t in set(r.types) if t.startswith("ExR")]}
    return {"bump": bump, "BUMP": bool(ok), "fwhm_deg": fwhm, "busiest_wedge_hz": round(peak, 1),
            "rate_hz": {k: round(float(rate[:, np.isin(r.types, v)].mean()), 2) for k, v in groups.items() if np.isin(r.types, v).any()}}


def seeded(recipe: dict) -> dict:
    out = []
    for k, start in enumerate(SEEDS):
        r = Ring(recipe, 2, seed=10 + k)
        b = r.brain
        b.advance(int(round(1.0 / b.dt)))
        kick = np.zeros(b.n)
        kick[r.epg[np.isin(r.wedge, [(start + d) % 16 for d in (-1, 0, 1)])]] = 10.0
        b.set_bias(kick)
        b.advance(int(round(0.3 / b.dt)))
        b.set_bias(np.zeros(b.n))
        b.advance(int(round((FREE - 1) / b.dt)))
        w, _ = r.windows(1)
        z = r.profile(w)[:, 0] @ np.exp(2j * np.pi * np.arange(16) / 16)
        out += np.round(np.degrees(np.abs(np.angle(z * np.exp(-2j * np.pi * start / 16)))), 1).tolist()
    return {"distance_from_seed_deg": out, "held": int((np.asarray(out) < 45).sum()), "runs": len(out)}


def main() -> None:
    t0 = time.perf_counter()
    conditions = {"recipe": RECIPE, "no slow current": RECIPE | {"slow": None}, "no depression": RECIPE | {"depression": None},
                  "unit gains": RECIPE | {"gains": (1.0, 1.0)}, "ring's six types alone": RECIPE | {"ring neurons": False}}
    out = {"question": __doc__, "conditions": {}}
    for name, recipe in conditions.items():
        out["conditions"][name] = r = {"spontaneous": spontaneous(recipe), "seeded": seeded(recipe)}
        s = r["spontaneous"]
        print(name, "| BUMP", s["BUMP"], {x: (v["strength"], v["shuffle_p99"], v["resultant"]) for x, v in s["bump"].items()},
              "| fwhm", s["fwhm_deg"], "peak", s["busiest_wedge_hz"], s["rate_hz"], "| held", r["seeded"]["held"], "/", r["seeded"]["runs"], flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
