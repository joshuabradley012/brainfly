"""Does removing the network's input to sensory neurons end the lasting activity? (rung 1, fifth attempt)

The fourth attempt (shiu_signs.py) got closest yet. MN9 followed the sugar rate (0 Hz at 10 Hz sugar,
62 Hz at 100 Hz), and only 8 undriven neurons passed 100 Hz. Two things failed.

First, activity outlasted the drive at 14% of its level. The largest single source was the Ir94e
taste neurons: nothing drove them, yet they fired at about 36 Hz after the sugar stopped. Synapses
from the network onto their axon terminals kept them going. In the fly a sensory neuron's firing is
set by transduction, and synapses onto its terminals modulate its release (presynaptic inhibition;
Olsen & Wilson 2008). A point neuron gets this wrong by letting them make it fire. The research
report's rung-1 recipe specifies "no synapses onto sensory neurons". Attempts 1-4 omitted this, and
shiu_runaway.py tried it only as a variant of the runaway network.

Second, 18 of 20 weight shuffles drove MN9. A check afterwards (not pre-registered) showed that
shuffling the counts runs these networks away (50,000-83,000 neurons above 100 Hz [corrected afterwards: no saved
result holds that range; shiu_signs.py's 20 count shuffles put 77,135-84,782 neurons above 100 Hz]), and that even
shuffling the final synaptic strengths leaves 9,000-27,000 there. A network that runs away drives MN9
whatever its routing, so that null can't ask whether the route depends on the wiring. The null here
shuffles strengths only among the inputs of one sign onto one neuron. Each neuron keeps its total
excitatory and inhibitory input, and its partners, and the null asks whether it matters which partner
carries which strength. Degree-preserving rewiring stays as before. The global shuffle is still run
and reported, but it isn't part of the pass.

Model: exactly shiu_signs.py's (HybridBrain with Shiu's neuron model; fast transmission only from
neurons with a consensus fast transmitter, sensory neurons exempted; no Kenyon-to-Kenyon synapses;
the density recipe), with every synapse onto a sensory neuron also removed (superclasses containing
"sensory"). Sensory neurons keep their Poisson drive and their output.
Calibration, tests and RESPONSE: exactly shiu_signs.py's.
Nulls: 20 within-neuron shuffles (each neuron's excitatory input counts permuted among its excitatory
inputs, and inhibitory among inhibitory; as all of a neuron's inputs share its size scaling, this is
also a shuffle of its final strengths), and 20 degree-preserving rewirings, as before, 10 trials each.
Reported only: 20 global weight shuffles, as in shiu_signs.py.
Pass, fixed before the first run: STABLE and SUGAR and RESPONSE, as in shiu_signs.py, and NULL: the
within-neuron shuffles and the degree-preserving rewirings each activate MN9 in at most 2 of 20.
Confirmation: as in shiu_signs.py (STABLE, SUGAR and RESPONSE again on fresh seeds).
Reported, not part of the pass: WATER, BITTER, IR94E, what still fires after the drive (by type),
each null network's MN9 rate and count of neurons above 100 Hz, and the global weight shuffles.

    python experiments/shiu_sensory.py            (writes experiments/shiu_sensory.json)
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
from shiu_signs import RATES, Reseeded, calibrate, fast_network, lasting, response

OUT = Path(__file__).with_name("shiu_sensory.json")


def no_sensory_input(M: sparse.spmatrix, superclass: np.ndarray):
    """M without the synapses onto sensory neurons (rows = postsynaptic)."""
    sensory = np.char.find(superclass.astype(str), "sensory") >= 0
    coo = M.tocoo()
    onto = sensory[coo.row]
    kept = sparse.csr_matrix((coo.data[~onto], (coo.row[~onto], coo.col[~onto])), shape=M.shape)
    return kept, {"sensory_neurons": int(sensory.sum()), "synapses_onto_sensory_removed": int(np.abs(coo.data[onto]).sum())}


def within_neuron_shuffle(M: sparse.csr_matrix, rng: np.random.Generator) -> sparse.csr_matrix:
    """Each neuron's excitatory input counts permuted among its excitatory inputs, and inhibitory among
    inhibitory (rows = postsynaptic)."""
    M = M.tocsr()
    rows = np.repeat(np.arange(M.shape[0]), np.diff(M.indptr))
    group = rows * 2 + (M.data < 0)
    random_order = np.lexsort((rng.random(M.nnz), group))      # each group's entries, in random order
    in_place = np.argsort(group, kind="stable")                 # each group's entries, where they sit
    data = M.data.copy()
    data[in_place] = M.data[random_order]
    return sparse.csr_matrix((data, M.indices.copy(), M.indptr.copy()), shape=M.shape)


def nulls(M: sparse.csr_matrix, w: float, scale: np.ndarray, labels: dict, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    rng = np.random.default_rng(7)
    C = M.tocsc()
    make = {
        "within_neuron_shuffle": lambda: within_neuron_shuffle(M, rng),
        "degree_preserving": lambda: sparse.csc_matrix((C.data, rng.permutation(C.indices), C.indptr), shape=C.shape),
        "global_weight_shuffle": lambda: sparse.csc_matrix((rng.permutation(C.data), C.indices, C.indptr), shape=C.shape),
    }
    result = {}
    for name, shuffled in make.items():
        hits, hot = [], []
        for k in range(SHUFFLES):
            b = HybridBrain(trials=10, w_syn=w, matrix=shuffled(), scale=scale, labels=labels)
            r = b.run(1.0, drive=[(sugar, 100.0)], seed=200 + k)
            over = r.rates > 100
            over[sugar] = False
            hits.append(float(r.rates[mn9[0]]))
            hot.append(int(over.sum()))
        result[name] = {"mn9_L_hz": [round(h, 2) for h in hits], "undriven_over_100hz": hot,
                        "activated": int(sum(h > 0 for h in hits))}
        print(f"    {name}: MN9 L activated in {result[name]['activated']}/{SHUFFLES}; neurons > 100 Hz {hot}", flush=True)
    result["NULL"] = all(result[k]["activated"] <= 2 for k in ("within_neuron_shuffle", "degree_preserving"))
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
    results["nulls"] = nulls(M, w, scale, labels, cells["sugar"], mn9)
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
