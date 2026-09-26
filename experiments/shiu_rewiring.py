"""Does the fifth attempt's network pass when its null scrambles the wiring? (rung 1, sixth attempt)

The fifth attempt (shiu_sensory.py) was the first network on MaleCNS to pass STABLE. MN9 followed the
sugar rate, and degree-preserving rewiring abolished the route in 20 of 20 networks, but it failed
its pre-registered null. Shuffling synaptic strengths among each neuron's inputs of one sign left
sugar driving MN9 in 15 of 20 quiet networks. The global weight shuffle, Shiu's null, can't be used
here: it runs these networks away (61,000-79,000 neurons above 100 Hz), and a network that runs away
drives MN9 whatever its routing. A within-neuron shuffle keeps each neuron's partners, so a route set
by which neurons connect survives it; it tests weight specificity, not routing. The report's rule is
that a rung passes only if the effect degrades under scrambled wiring, and its null ladder climbs
from weight shuffles to degree-preserving rewiring, degree- and weight-matched ensembles, and
cell-class-preserving rewiring. So, as decided after the fifth attempt, this gates rung 1 on
scrambled wiring and reports the weight shuffles without gating on them.

Model: shiu_sensory.py's, unchanged, at its calibrated w_syn = 1.5556 mV (not recalibrated).
Tests, all on seeds none of the earlier runs used (every seed + 2000):
  shiu_baseline.py's tests (30 trials); MN9 L at 10 and 100 Hz sugar (30 trials each).
Nulls, 20 networks each, 10 trials, new random networks and seeds:
  degree-preserving rewiring  every synapse keeps its source and count and gets a random target from
                              all synapses' targets (each neuron keeps its in- and out-degree), as before
  class-preserving rewiring   the same, with targets drawn only from synapses whose targets are in the
                              same superclass, so each source keeps its number of synapses into each
                              superclass (27 of them). The stricter null: it keeps the coarse
                              sensory-to-central-to-motor structure and scrambles which neurons connect.
Pass, fixed before the first run: STABLE and SUGAR (as shiu_baseline.py defines them), RESPONSE (MN9 L
at 10 Hz sugar at most 25% of its rate at 100 Hz), and NULL: the degree-preserving and the
class-preserving rewirings each activate MN9 in at most 2 of 20.
Reported, not part of the pass: WATER, BITTER, IR94E; what still fires after the drive; each null
network's MN9 rate and count of neurons above 100 Hz; and 20 within-neuron and 20 global weight
shuffles, as in shiu_sensory.py.

    python experiments/shiu_rewiring.py            (writes experiments/shiu_rewiring.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from shiu_baseline import SETS, SHUFFLES, tests
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input, within_neuron_shuffle
from shiu_signs import Reseeded, fast_network, lasting, response

OUT = Path(__file__).with_name("shiu_rewiring.json")
W_SYN = 1.5556          # shiu_sensory.py's calibration
OFFSET = 2000           # seeds none of the earlier runs used


def class_preserving_rewiring(C: sparse.csc_matrix, klass: np.ndarray, rng: np.random.Generator) -> sparse.csc_matrix:
    """Every synapse keeps its source and count and takes the target of a random synapse whose target
    is in the same class (columns = presynaptic, so targets are C.indices)."""
    group = klass[C.indices]
    random_order = np.lexsort((rng.random(C.nnz), group))      # each class's targets, in random order
    in_place = np.argsort(group, kind="stable")                 # each class's synapses, where they sit
    targets = C.indices.copy()
    targets[in_place] = C.indices[random_order]
    return sparse.csc_matrix((C.data, targets, C.indptr), shape=C.shape)


def nulls(M: sparse.csr_matrix, scale: np.ndarray, labels: dict, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    rng = np.random.default_rng(2026)
    C = M.tocsc()
    klass = np.unique(labels["superclass"].astype(str), return_inverse=True)[1]
    make = {
        "degree_preserving": lambda: sparse.csc_matrix((C.data, rng.permutation(C.indices), C.indptr), shape=C.shape),
        "class_preserving": lambda: class_preserving_rewiring(C, klass, rng),
        "within_neuron_shuffle": lambda: within_neuron_shuffle(M, rng),
        "global_weight_shuffle": lambda: sparse.csc_matrix((rng.permutation(C.data), C.indices, C.indptr), shape=C.shape),
    }
    result = {}
    for name, shuffled in make.items():
        hits, hot = [], []
        for k in range(SHUFFLES):
            b = HybridBrain(trials=10, w_syn=W_SYN, matrix=shuffled(), scale=scale, labels=labels)
            r = b.run(1.0, drive=[(sugar, 100.0)], seed=OFFSET + 200 + k)
            over = r.rates > 100
            over[sugar] = False
            hits.append(float(r.rates[mn9[0]]))
            hot.append(int(over.sum()))
        result[name] = {"mn9_L_hz": [round(h, 2) for h in hits], "undriven_over_100hz": hot,
                        "activated": int(sum(h > 0 for h in hits))}
        print(f"    {name}: MN9 L activated in {result[name]['activated']}/{SHUFFLES}; neurons > 100 Hz {hot}", flush=True)
    result["NULL"] = all(result[k]["activated"] <= 2 for k in ("degree_preserving", "class_preserving"))
    return result


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    kc = np.char.startswith(types.astype(str), "KC")
    M, removed = fast_network(C, consensus_transmitters(), meta["superclass"], kc)
    M, sensory = no_sensory_input(M, meta["superclass"])
    removed.update(sensory, synapses_kept=int(np.abs(M.data).sum()))
    scale = 1.0 / sizes(C)
    results = {"criteria": __doc__, "w_syn": W_SYN, "removed": removed}
    brain = HybridBrain(trials=30, w_syn=W_SYN, matrix=M, scale=scale, labels=labels)
    cells = {k: brain.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([brain.cells(["MN9"], side="L"), brain.cells(["MN9"], side="R")])
    fresh = Reseeded(brain, OFFSET)
    print(f"tests at w_syn = {W_SYN} mV on fresh seeds (30 trials)", flush=True)
    results["tests"] = t = tests(fresh, cells, mn9)
    print(f"    {json.dumps(t)}", flush=True)
    low = float(fresh.run(1.0, drive=[(cells["sugar"], 10.0)], seed=10).rates[mn9[0]])
    high = float(fresh.run(1.0, drive=[(cells["sugar"], 100.0)], seed=100).rates[mn9[0]])
    results["mn9_L_hz_10"], results["mn9_L_hz_100"] = round(low, 2), round(high, 2)
    results["RESPONSE"] = response(low, high)
    print(f"    MN9 L {low:.1f} Hz at 10 Hz sugar, {high:.1f} Hz at 100 Hz: RESPONSE {results['RESPONSE']}", flush=True)
    results["lasting_activity"] = lasting(fresh, cells["sugar"], types.astype(str), meta["superclass"].astype(str))
    print(f"    after the drive: {json.dumps(results['lasting_activity'])}", flush=True)
    OUT.write_text(json.dumps(results, indent=1))
    print("nulls (10 trials each)", flush=True)
    results["nulls"] = nulls(M, scale, labels, cells["sugar"], mn9)
    results["pass"] = bool(t["STABLE"] and t["SUGAR"] and results["RESPONSE"] and results["nulls"]["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: STABLE {t['STABLE']} SUGAR {t['SUGAR']} RESPONSE {results['RESPONSE']} "
          f"NULL {results['nulls']['NULL']} | WATER {t['WATER']} BITTER {t['BITTER']} IR94E {t['IR94E']} "
          f"({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
