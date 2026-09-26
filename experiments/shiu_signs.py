"""Does fast transmission from only the neurons with a known fast transmitter end the MaleCNS runaway?
(rung 1, fourth attempt)

On the corrected kernel, the second attempt's density recipe came closest (shiu_scaled.py: every
synapse onto a neuron divided by its size). Only 20 undriven neurons passed 100 Hz, and MN9 followed
the sugar rate: 0 Hz at 10 and 25 Hz sugar, 68 Hz at 100 Hz. It failed because activity outlasted the
drive, at 23% of its level where the limit is 1%, and because 11 of 20 weight shuffles drove MN9
too. A diagnostic that wasn't pre-registered traced the lasting activity to a cluster of pars
intercerebralis and prow neurons: insulin-producing cells, DH44, DMS, PI3 and DNES1 cells, and PRW
and SMP interneurons. Most of them have no transmitter MaleCNS could call (consensus "unclear"), and
brainfly's sign rule counts that as fast excitation by default, as doomfly's does. Such cells are
largely neurosecretory and peptidergic. They signal through G-protein receptors over hundreds of
milliseconds or longer, and the research report puts that kind of signalling, like the monoamines',
in slow modulatory state rather than fast excitation (rung 2).

So this keeps in the fast network only synapses from neurons with a known fast transmitter. It
removes every synapse from:
  (a) the 541 neurons whose consensus transmitter is dopamine, octopamine or serotonin;
  (b) the neurons with no consensus transmitter (unclear or missing), except sensory neurons.
      Insect sensory neurons are overwhelmingly cholinergic, so an unclear call there reflects the
      classifier, not the cell; photoreceptors, which are histaminergic, are called so. 6 of the 38
      bitter taste neurons are among the exempted.
  (c) Kenyon cells onto other Kenyon cells, which act through inhibitory muscarinic receptors rather
      than fast excitation (Bielopolski et al. 2019).
Transmitters come from MaleCNS's consensus only. Its machine prediction calls 4,058 of the 4,064
Kenyon cells dopaminergic, which made shiu_mb.py remove nearly all Kenyon-cell output.

Model: brainfly.hybrid.HybridBrain with nothing else changed (Shiu's neuron model and parameters,
0.1 ms steps, Brian2-exact), on the MaleCNS signed counts minus (a)-(c). Every synapse onto neuron i
is divided by s_i, as in shiu_scaled.py's density recipe (s_i = neuron i's total synapses in the whole
connectome / the median).
Calibration: Shiu's rule, as before (the w_syn whose MN9 L rate at 100 Hz sugar is closest to 80% of
its maximum over 10-200 Hz), over w_syn = 0.55 x 2^(k/4) mV, k = 0..8 (0.55-2.2 mV; the density
recipe calibrated at the top of the earlier grid, 1.1 mV), 10 trials per point.
Tests at the calibrated w_syn: exactly shiu_baseline.py's (30 trials, 100 Hz, same neuron sets and
seeds). Nulls: 20 weight shuffles and 20 degree-preserving rewirings of this modified count matrix,
with the size scaling applied after shuffling, as in shiu_scaled.py, 10 trials each.
Pass, fixed before the first run: STABLE and SUGAR and NULL, as shiu_scaled.py defines them, and
RESPONSE: at the calibrated w_syn, MN9 L's rate at 10 Hz sugar is at most 25% of its rate at 100 Hz
in the calibration grid. RESPONSE is new. shiu_mb.py showed the taste tests passing while MN9 fired
as fast at 10 Hz sugar as at 100 Hz.
Confirmation: a pass counts only if STABLE, SUGAR and RESPONSE hold again on fresh seeds (the tests
rerun with every seed + 1000, and MN9 L at 10 and 100 Hz sugar, 30 trials each).
Reported, not part of the pass: WATER, BITTER, IR94E, what still fires after the drive (by type),
and each null network's MN9 rate and count of neurons above 100 Hz.

    python experiments/shiu_signs.py            (writes experiments/shiu_signs.json)
"""
from __future__ import annotations

import collections
import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from shiu_baseline import RATES, SETS, SHUFFLES, tests
from shiu_scaled import sizes

OUT = Path(__file__).with_name("shiu_signs.json")
GRID = [round(0.55 * 2 ** (k / 4), 4) for k in range(9)]
FAST = ("acetylcholine", "gaba", "glutamate", "histamine")
MONOAMINES = ("dopamine", "octopamine", "serotonin")


def fast_network(C: sparse.spmatrix, transmitter: np.ndarray, superclass: np.ndarray, kc: np.ndarray):
    """The counts without (a)-(c), and what was removed."""
    amine = np.isin(transmitter, MONOAMINES)
    sensory = np.char.find(superclass.astype(str), "sensory") >= 0
    unknown = ~np.isin(transmitter, FAST) & ~amine & ~sensory
    coo = C.tocoo()
    kc_kc = kc[coo.row] & kc[coo.col]
    drop = amine[coo.col] | unknown[coo.col] | kc_kc
    M = sparse.csr_matrix((coo.data[~drop], (coo.row[~drop], coo.col[~drop])), shape=C.shape)
    syn = np.abs(coo.data)
    removed = {"monoaminergic_neurons": int(amine.sum()), "no_fast_transmitter_neurons": int(unknown.sum()),
               "exempted_sensory_neurons": int((~np.isin(transmitter, FAST) & ~amine & sensory).sum()),
               "synapses_from_monoaminergic": int(syn[amine[coo.col]].sum()),
               "synapses_from_no_fast_transmitter": int(syn[unknown[coo.col]].sum()),
               "synapses_kenyon_to_kenyon": int(syn[kc_kc].sum()), "synapses_kept": int(np.abs(M.data).sum()),
               "synapses_before": int(syn.sum())}
    return M, removed


def calibrate(brain: HybridBrain, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    grid = []
    for w in GRID:
        brain.w_syn = w
        mn = [float(brain.run(1.0, drive=[(sugar, r)], seed=100 + r).rates[mn9[0]]) for r in RATES]
        ratio = mn[RATES.index(100)] / max(mn) if max(mn) > 0 else None
        grid.append({"w_syn": w, "mn9_L_hz": [round(m, 2) for m in mn], "ratio_100": None if ratio is None else round(ratio, 3)})
        print(f"    w_syn {w:.4f}: MN9 L {[round(m, 1) for m in mn]} Hz, 100 Hz / max = {grid[-1]['ratio_100']}", flush=True)
    usable = [g for g in grid if g["ratio_100"] is not None]
    pick = min(usable, key=lambda g: abs(g["ratio_100"] - 0.8)) if usable else None
    return {"grid": grid, "w_syn": None if pick is None else pick["w_syn"]}


def response(mn9_10: float, mn9_100: float) -> bool:
    return bool(mn9_100 > 0 and mn9_10 <= 0.25 * mn9_100)


def nulls(M: sparse.csc_matrix, w: float, scale: np.ndarray, labels: dict, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    rng = np.random.default_rng(7)
    result = {}
    for name in ("weight_shuffle", "degree_preserving"):
        hits, hot = [], []
        for k in range(SHUFFLES):
            if name == "weight_shuffle":
                S = sparse.csc_matrix((rng.permutation(M.data), M.indices, M.indptr), shape=M.shape)
            else:
                S = sparse.csc_matrix((M.data, rng.permutation(M.indices), M.indptr), shape=M.shape)
            b = HybridBrain(trials=10, w_syn=w, matrix=S, scale=scale, labels=labels)
            r = b.run(1.0, drive=[(sugar, 100.0)], seed=200 + k)
            over = r.rates > 100
            over[sugar] = False
            hits.append(float(r.rates[mn9[0]]))
            hot.append(int(over.sum()))
        result[name] = {"mn9_L_hz": [round(h, 2) for h in hits], "undriven_over_100hz": hot,
                        "activated": int(sum(h > 0 for h in hits))}
        print(f"    {name}: MN9 L activated in {result[name]['activated']}/{SHUFFLES}; neurons > 100 Hz {hot}", flush=True)
    result["NULL"] = all(result[k]["activated"] <= 2 for k in ("weight_shuffle", "degree_preserving"))
    return result


class Reseeded:
    """The same brain with every run's seed moved by `offset`, for the confirmation."""

    def __init__(self, brain: HybridBrain, offset: int):
        self.brain, self.offset, self.n = brain, offset, brain.n

    def run(self, *args, seed: int = 0, **kw):
        return self.brain.run(*args, seed=seed + self.offset, **kw)


def lasting(brain: HybridBrain, sugar: np.ndarray, types: np.ndarray, superclass: np.ndarray) -> dict:
    """What still fires in the 0.5 s after 1 s of 100 Hz sugar."""
    r = brain.run(1.0, drive=[(sugar, 100.0)], seed=1, tail=0.5)
    after = r.after_rates.mean(0)
    firing = after > 1
    by_type = collections.Counter()
    for i in np.flatnonzero(firing):
        by_type[types[i] or "(untyped)"] += float(after[i])
    return {"neurons_over_1hz": int(firing.sum()), "spikes_per_s": round(float(after.sum()), 1),
            "by_superclass": dict(collections.Counter(superclass[firing]).most_common(8)),
            "top_types_spikes_per_s": {k: round(v, 1) for k, v in by_type.most_common(12)}}


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    kc = np.char.startswith(types.astype(str), "KC")
    M, removed = fast_network(C, consensus_transmitters(), meta["superclass"], kc)
    scale = 1.0 / sizes(C)
    results = {"criteria": __doc__, "removed": removed}
    print("removed:", removed, flush=True)
    brain = HybridBrain(trials=10, matrix=M, scale=scale, labels=labels)
    cells = {k: brain.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([brain.cells(["MN9"], side="L"), brain.cells(["MN9"], side="R")])
    print("calibration (10 trials per point)", flush=True)
    results["calibration"] = cal = calibrate(brain, cells["sugar"], mn9)
    OUT.write_text(json.dumps(results, indent=1))
    w = cal["w_syn"]
    if w is None:
        results["pass"] = False
        print("sugar never reached MN9; FAIL", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
        return
    point = next(g for g in cal["grid"] if g["w_syn"] == w)["mn9_L_hz"]
    results["RESPONSE"] = response(point[RATES.index(10)], point[RATES.index(100)])
    print(f"calibrated w_syn = {w} mV; RESPONSE {results['RESPONSE']}; tests (30 trials)", flush=True)
    test_brain = HybridBrain(trials=30, w_syn=w, matrix=M, scale=scale, labels=labels)
    results["tests"] = t = tests(test_brain, cells, mn9)
    print(f"    {json.dumps(t)}", flush=True)
    results["lasting_activity"] = lasting(test_brain, cells["sugar"], types.astype(str), meta["superclass"].astype(str))
    print(f"    after the drive: {json.dumps(results['lasting_activity'])}", flush=True)
    OUT.write_text(json.dumps(results, indent=1))
    print("nulls (10 trials each)", flush=True)
    results["nulls"] = nulls(M.tocsc(), w, scale, labels, cells["sugar"], mn9)
    results["pass"] = bool(t["STABLE"] and t["SUGAR"] and results["nulls"]["NULL"] and results["RESPONSE"])
    OUT.write_text(json.dumps(results, indent=1))
    if results["pass"]:
        print("confirmation on fresh seeds (30 trials)", flush=True)
        c = tests(Reseeded(test_brain, 1000), cells, mn9)
        low = float(test_brain.run(1.0, drive=[(cells["sugar"], 10.0)], seed=1010).rates[mn9[0]])
        high = float(test_brain.run(1.0, drive=[(cells["sugar"], 100.0)], seed=1100).rates[mn9[0]])
        results["confirmation"] = {"tests": c, "mn9_L_hz_10": round(low, 2), "mn9_L_hz_100": round(high, 2),
                                   "confirmed": bool(c["STABLE"] and c["SUGAR"] and response(low, high))}
        print(f"    {json.dumps(results['confirmation'])}", flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: STABLE {t['STABLE']} SUGAR {t['SUGAR']} NULL {results['nulls']['NULL']} "
          f"RESPONSE {results['RESPONSE']} | WATER {t['WATER']} BITTER {t['BITTER']} IR94E {t['IR94E']} "
          f"({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
