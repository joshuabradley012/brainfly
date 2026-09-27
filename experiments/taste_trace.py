"""Exploratory, not pre-registered: where does sugar's signal die in the resting brain?

In rung 1's silent brain, 100 Hz of sugar drives MN9 to about 40 Hz through 343 active neurons
(taste_depression.py). In the resting brain (escape_at_rest.py's model and calibrated biases) it moves
MN9 by 2 Hz, and taste_hunger.py found that multiplying the sugar neurons' output by up to 10 only
lowers that. This drives the left sugar neurons (shiu_baseline.py's SETS) at 100 Hz for 1 s, 8 flies, in
both brains (the silent one as taste_depression.py runs it; the resting one as escape_at_rest.py
measures taste, rises over the 0.5 s before), and compares every neuron's rise:
  layers   rung 1's active neurons (over 5 Hz) by their fewest excitatory steps from the sugar neurons
           in the model's wiring, with how many rise at least 5 Hz in each brain and their median rises
  MN9      MN9 L's 15 strongest inputs, signed, with their rises in each brain, and MN9's summed
           excitatory and inhibitory input change (each input's rise times its weight, mV per ms of
           current at the soma, before the membrane)

    python experiments/taste_trace.py            (writes experiments/taste_trace.json)
"""
from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path

import numpy as np

import escape_at_rest as escape
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
from brainfly.hybrid import HybridBrain
from shiu_baseline import SETS
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")


def silent_rise(M, scale, labels, sugar) -> np.ndarray:
    b = HybridBrain(trials=8, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=1)
    return b.run(1.0, drive=[(sugar, 100.0)], seed=3).rates          # at rest it's silent, so rate = rise


def resting_rise(sugar_types) -> tuple[np.ndarray, eyes.Setup]:
    attempt2.model = escape.model
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(escape.HERE / "intact.npz")["bias"]
    b = s.brain
    b.set_bias(s.bias[s.gid])
    sugar = b.cells(sugar_types, "L")
    b.reset(1)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(0.5 / b.dt)))
    before = b.advance(int(round(0.5 / b.dt))).mean(0) / 0.5
    during = b.advance(int(round(1.0 / b.dt)), drive=[(sugar, 100.0)]).mean(0) / 1.0
    return during - before, s


def hops(M, start: np.ndarray, allowed: np.ndarray) -> np.ndarray:
    """Fewest excitatory steps from `start` to each neuron, moving only through `allowed` ones."""
    E = (M.tocsc() > 0).astype(np.int8).T.tocsr()          # row: presynaptic, columns: its targets
    d = np.full(M.shape[0], -1)
    d[start] = 0
    q = deque(start.tolist())
    while q:
        i = q.popleft()
        for j in E.indices[E.indptr[i]:E.indptr[i + 1]]:
            if d[j] < 0 and allowed[j]:
                d[j] = d[i] + 1
                q.append(j)
    return d


def main() -> None:
    t0 = time.perf_counter()
    M, scale, labels, types, superclass = attempt1.network()
    M = M.tocsr()
    rest, s = resting_rise(SETS["sugar"])
    b = s.brain
    sugar = b.cells(SETS["sugar"], "L")
    silent = silent_rise(M, scale, labels, sugar)
    active = silent > 5
    d = hops(M, sugar, active)
    layers = []
    for k in range(0, d.max() + 1):
        m = d == k
        layers.append({"steps": k, "neurons": int(m.sum()), "rise_5hz_silent": int((silent[m] >= 5).sum()), "rise_5hz_resting": int((rest[m] >= 5).sum()),
                       "median_rise_silent_hz": round(float(np.median(silent[m])), 1), "median_rise_resting_hz": round(float(np.median(rest[m])), 1)})
    mn9 = b.cells(["MN9"], "L")[0]
    w = np.asarray(M[mn9].todense()).ravel() * scale[mn9] * W_SYN      # mV per presynaptic spike
    top = np.argsort(-np.abs(w))[:15]
    name = lambda i: f"{types[i] or superclass[i]} {labels['side'][i]}"
    inputs = [{"input": name(i), "mv_per_spike": round(float(w[i]), 3), "rise_silent_hz": round(float(silent[i]), 1),
               "rise_resting_hz": round(float(rest[i]), 1), "steps": int(d[i])} for i in top]
    drive = {f"{brain} {sign}": round(float(np.sum(np.where(w > 0 if sign == "excitation" else w < 0, w * r, 0.0))), 2)
             for brain, r in (("silent", silent), ("resting", rest)) for sign in ("excitation", "inhibition")}
    out = {"question": __doc__, "mn9_rise_hz": {"silent": round(float(silent[mn9]), 1), "resting": round(float(rest[mn9]), 1)},
           "active_in_silent": int(active.sum()), "layers": layers, "mn9_inputs": inputs, "mn9_input_change_mv_per_s": drive,
           "seconds": round(time.perf_counter() - t0)}
    print(json.dumps({k: v for k, v in out.items() if k != "question"}, indent=1), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
