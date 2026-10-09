"""Rung 2 (pre-registered): does rung 1 still pass with transmitter signs audited by hemilineage, and do its
false positives stay near Shiu's 1%?

Rung 2 adds MaleCNS's consensus transmitters, takes dopamine, octopamine and serotonin out of fast excitation
(both already in rung 1's pass), and audits transmitter conflicts by hemilineage. Its criteria (README; the
report's plan): rung 1 still passes, and false positives stay near Shiu et al.'s 1%. That 1% is Shiu et al.
2024's null: with the weights shuffled, sugar activated MN9 in 1 of 100 networks. brainfly's rung 1 gates
instead on scrambled wiring, since the global weight shuffle runs MaleCNS networks away (shiu_sensory.py). It
found 0 of 20 degree-preserving and 0 of 20 class-preserving rewirings activating MN9, too few to tell 1% from 0.
hemilineage_audit.py (exploratory) found 348 neurons whose consensus fast transmitter disagrees with a clear
majority (at least 90%) of their hemilineage (at least 10 neurons with a fast consensus). One hemilineage uses one
fast transmitter (Lacin et al. 2019). 260 of them differ in sign (acetylcholine against GABA or glutamate), 4 of
them on rung 1's sugar route.
Model: rung 1's (shiu_rewiring.py's network at w_syn = 1.5556 mV, silent at rest), with each of the audit's 260
sign conflicts given its hemilineage's majority sign (its outgoing synapses' signs flipped).
Tests, on seeds no earlier run used (every seed + 3000):
  RUNG1  rung 1's pass criteria: STABLE and SUGAR as shiu_baseline.py defines them (30 trials), and RESPONSE
         (MN9 L at 10 Hz sugar at most 25% of its rate at 100 Hz)
  FALSE  false positives: in 100 degree-preserving and 100 class-preserving rewirings of this network (built as
         shiu_rewiring.py builds them, new random networks), sugar at 100 Hz activates MN9 L (any spike, 10
         trials) in at most 3 of each 100. With a true rate of 1%, 3 or fewer of 100 happens 98% of the time.
Pass: RUNG1 and FALSE.
Reported, not part of the pass: WATER, BITTER, IR94E. Also rung 1's tests on the same seeds three more ways:
  - without the audit (the difference it makes);
  - with every glutamatergic synapse excitatory instead of inhibitory (glutamate's sign sensitivity);
  - with the monoamines back as fast excitation (rung 2's other change undone).

Checked afterwards (2026-10-09 review; the code is left as it ran): 6 of the 260 flipped neurons have MaleCNS ground
truth agreeing with their consensus and should have been exempt (hemilineage_audit.py). And the glutamate variant
flips the consensus-glutamatergic neurons of the already-audited matrix, so 128 that the audit had made cholinergic
are flipped back to inhibitory and 41 that it had made glutamatergic stay inhibitory: 169 neurons with 1.9% of the
glutamatergic synapses that the variant meant to be excitatory. It ran away regardless (94,950 undriven neurons over
100 Hz).

    python experiments/rung2_signs.py            (writes experiments/rung2_signs.json)
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
from shiu_baseline import SETS, tests
from shiu_rewiring import W_SYN, class_preserving_rewiring
from shiu_scaled import sizes
from shiu_sensory import no_sensory_input
from shiu_signs import Reseeded, fast_network, response

OUT = Path(__file__).with_suffix(".json")
OFFSET, NULLS, MAX_HITS = 3000, 100, 3


def flip(M: sparse.spmatrix, which: np.ndarray) -> sparse.csr_matrix:
    """M with the outgoing synapses (columns) of `which` neurons changed in sign."""
    return (M.tocsr() @ sparse.diags(np.where(which, -1.0, 1.0).astype(np.float32))).tocsr()


def rung1_tests(M, scale, labels, cells, mn9) -> dict:
    fresh = Reseeded(HybridBrain(trials=30, w_syn=W_SYN, matrix=M, scale=scale, labels=labels), OFFSET)
    t = tests(fresh, cells, mn9)
    low = float(fresh.run(1.0, drive=[(cells["sugar"], 10.0)], seed=10).rates[mn9[0]])
    high = float(fresh.run(1.0, drive=[(cells["sugar"], 100.0)], seed=100).rates[mn9[0]])
    t.update(mn9_L_hz_10=round(low, 2), mn9_L_hz_100=round(high, 2), RESPONSE=response(low, high))
    return t


def false_positives(M, scale, labels, sugar, mn9) -> dict:
    rng = np.random.default_rng(2027)
    C = M.tocsc()
    klass = np.unique(labels["superclass"].astype(str), return_inverse=True)[1]
    make = {"degree_preserving": lambda: sparse.csc_matrix((C.data, rng.permutation(C.indices), C.indptr), shape=C.shape),
            "class_preserving": lambda: class_preserving_rewiring(C, klass, rng)}
    out = {}
    for name, rewired in make.items():
        hz, hot = [], []
        for k in range(NULLS):
            r = HybridBrain(trials=10, w_syn=W_SYN, matrix=rewired(), scale=scale, labels=labels).run(
                1.0, drive=[(sugar, 100.0)], seed=OFFSET + 200 + k)
            over = r.rates > 100
            over[sugar] = False
            hz.append(round(float(r.rates[mn9[0]]), 2))
            hot.append(int(over.sum()))
        out[name] = {"activated": int(sum(h > 0 for h in hz)), "mn9_L_hz": hz, "undriven_over_100hz": hot}
        print(f"  {name}: MN9 L activated in {out[name]['activated']}/{NULLS}", flush=True)
    out["FALSE"] = all(out[k]["activated"] <= MAX_HITS for k in make)
    return out


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types().astype(str)
    superclass = meta["superclass"].astype(str)
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    nt = consensus_transmitters()
    kc = np.char.startswith(types, "KC")
    M1, _ = fast_network(C, nt, meta["superclass"], kc)
    M1, _ = no_sensory_input(M1, meta["superclass"])
    scale = 1.0 / sizes(C)
    audit = hemilineage_audit.audit()
    M = flip(M1, audit["sign_flip"])
    probe = HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels)
    cells = {k: probe.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([probe.cells(["MN9"], side="L"), probe.cells(["MN9"], side="R")])
    results = {"criteria": __doc__, "audited_sign_flips": int(audit["sign_flip"].sum())}
    results["tests"] = t = rung1_tests(M, scale, labels, cells, mn9)
    results["RUNG1"] = bool(t["STABLE"] and t["SUGAR"] and t["RESPONSE"])
    print("audited:", json.dumps(t), flush=True)
    OUT.write_text(json.dumps(results, indent=1))
    results["false_positives"] = fp = false_positives(M, scale, labels, cells["sugar"], mn9)
    results["FALSE"] = fp["FALSE"]
    OUT.write_text(json.dumps(results, indent=1))

    # reported: the same tests without the audit, with glutamate excitatory, and with the monoamines back
    amine = np.isin(nt, ["dopamine", "octopamine", "serotonin"])
    coo = C.tocoo()
    keep = ~(~np.isin(nt, ["acetylcholine", "gaba", "glutamate"]) & ~amine & (np.char.find(superclass, "sensory") < 0))[coo.col] & ~(kc[coo.row] & kc[coo.col])
    with_amines, _ = no_sensory_input(sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=C.shape), meta["superclass"])
    variants = {"without the audit": M1, "glutamate excitatory": flip(M, nt == "glutamate"),
                "monoamines as fast excitation": flip(with_amines, audit["sign_flip"])}
    results["reported"] = {}
    for name, Mv in variants.items():
        results["reported"][name] = rv = rung1_tests(Mv, scale, labels, cells, mn9)
        print(f"{name}:", json.dumps(rv), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    results["pass"] = bool(results["RUNG1"] and results["FALSE"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: RUNG1 {results['RUNG1']} (STABLE {t['STABLE']} SUGAR {t['SUGAR']} RESPONSE {t['RESPONSE']}) "
          f"FALSE {results['FALSE']} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
