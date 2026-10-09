"""Exploratory, not pre-registered: does rung 2's sugar route need its wiring once the scrambled wiring keeps every
neuron's input and output strength?

Rung 2 passed with sugar driving MN9 L in 1 of 100 degree-preserving and 0 of 100 class-preserving rewirings
(rung2_signs.py). Degree-preserving rewiring keeps each neuron's number of partners but not its input strength: MN9 L
keeps only a quarter of its excitatory synapses (brainfly/nulls.py), so a route it abolishes may only have lost its
input. Class-preserving rewiring keeps more of it. The report's null ladder has a rung between them that brainfly
hasn't run, degree- and weight-matched ensembles.
Null here: every synapse keeps its source and count and takes the target of a random synapse of the same sign whose
count is within 10% of its own (counts grouped in log-spaced bins 10% wide, so single counts below 10). Every neuron
keeps its partners' number on both sides and its output strength exactly, and its input strength to within its
inputs' bins (MN9 L's strongest inputs, 241-464 synapses, are among the rarest counts). Rung 2's network otherwise
(rung2_signs.py: rung 1's, with the hemilineage audit's 260 sign flips), with its scale per neuron unchanged.
Measured as rung 2's FALSE test: in 100 networks, sugar at 100 Hz activates MN9 L (any spike in 10 trials of 1 s).
Read, fixed before the first run as rung 2's FALSE reads it: at most 3 of 100 means the route needs its wiring beyond
each neuron's strength. Seeds 6000 + network; rewiring from default_rng(2028).

Ran: sugar activates MN9 L in none of the 100 networks (rung 2: 1 of 100 degree-preserving, 0 of 100
class-preserving), and no undriven neuron passes 100 Hz in any. MN9 L keeps its input, 2,921-3,008 excitatory and
2,856-2,946 inhibitory synapses against 2,963 and 2,914, all from new partners, and no neuron's input changes by more
than 7.5%. So the route needs the connectome's wiring, not just each neuron's strength.

    python experiments/rung2_strength_null.py      (writes experiments/rung2_strength_null.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import hemilineage_audit
from brainfly.data import DATA
from brainfly.hybrid import HybridBrain, consensus_transmitters
from brainfly.shiu import counts, mcns_types
from rung2_signs import MAX_HITS, flip
from shiu_baseline import SETS
from shiu_rewiring import W_SYN
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import fast_network

OUT = Path(__file__).with_suffix(".json")
NETWORKS, OFFSET, WIDTH = 100, 6000, 0.1


def strength_preserving_rewiring(C: sparse.csc_matrix, rng: np.random.Generator, width: float = WIDTH) -> sparse.csc_matrix:
    """Every synapse keeps its source and count and takes the target of a random synapse of the same sign whose count
    is in the same log-spaced bin, `width` wide (columns = presynaptic, so targets are C.indices)."""
    magnitude = np.floor(np.log(np.abs(C.data)) / np.log1p(width)).astype(np.int64)
    group = 2 * magnitude + (C.data < 0)
    random_order = np.lexsort((rng.random(C.nnz), group))      # each bin's targets, in random order
    in_place = np.argsort(group, kind="stable")                 # each bin's synapses, where they sit
    targets = C.indices.copy()
    targets[in_place] = C.indices[random_order]
    return sparse.csc_matrix((C.data, targets, C.indptr), shape=C.shape)


def strengths(C: sparse.csc_matrix) -> tuple:
    """Each neuron's excitatory and inhibitory input, in synapses."""
    n = C.shape[0]
    return (np.bincount(C.indices, np.where(C.data > 0, C.data, 0), n),
            np.bincount(C.indices, np.where(C.data < 0, -C.data, 0), n))


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types().astype(str)
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    nt = consensus_transmitters()
    M1, _ = fast_network(C, nt, meta["superclass"], np.char.startswith(types, "KC"))
    M1, _ = no_sensory_input(M1, meta["superclass"])
    M = flip(M1, hemilineage_audit.audit()["sign_flip"]).tocsc()
    scale = 1.0 / sizes(C)
    probe = HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels)
    sugar = probe.cells(SETS["sugar"], side="L")
    mn9 = probe.cells(["MN9"], side="L")[0]
    exc0, inh0 = strengths(M)
    rung2 = json.loads((OUT.parent / "rung2_signs.json").read_text())["false_positives"]
    out = {"question": __doc__, "rung2_activated": {k: rung2[k]["activated"] for k in ("degree_preserving", "class_preserving")},
           "mn9_L_input_synapses": {"excitatory": int(exc0[mn9]), "inhibitory": int(inh0[mn9])}, "networks": []}
    rng = np.random.default_rng(2028)
    for k in range(NETWORKS):
        R = strength_preserving_rewiring(M, rng)
        exc, inh = strengths(R)
        moved = R.indices != M.indices
        into = M.indices == mn9
        r = HybridBrain(trials=10, w_syn=W_SYN, matrix=R, scale=scale, labels=labels).run(
            1.0, drive=[(sugar, 100.0)], seed=OFFSET + k)
        over = r.rates > 100
        over[sugar] = False
        row = {"mn9_L_hz": round(float(r.rates[mn9]), 2), "undriven_over_100hz": int(over.sum()),
               "mn9_L_input_synapses": {"excitatory": int(exc[mn9]), "inhibitory": int(inh[mn9])},
               "synapses_moved": round(float(moved.mean()), 4),
               "mn9_L_inputs_moved": round(float(moved[into].mean()), 3),
               "largest_input_change": round(float(np.max(np.abs(exc + inh - exc0 - inh0) / np.maximum(exc0 + inh0, 1))), 3)}
        out["networks"].append(row)
        print(k, json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    hz = [n["mn9_L_hz"] for n in out["networks"]]
    out["activated"] = int(sum(h > 0 for h in hz))
    out["needs_wiring"] = out["activated"] <= MAX_HITS
    out["seconds"] = round(time.perf_counter() - t0)
    print(f"sugar activates MN9 L in {out['activated']}/{NETWORKS} strength-preserving rewirings "
          f"(rung 2: degree-preserving {out['rung2_activated']['degree_preserving']}, class-preserving "
          f"{out['rung2_activated']['class_preserving']}); {out['seconds']} s", flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
