"""Does taking the mushroom body's slow transmission out of fast excitation stop the MaleCNS runaway?
(rung 1, third attempt)

shiu_baseline.py and shiu_scaled.py failed: Shiu et al.'s recipe runs away on MaleCNS, and
shiu_runaway.py placed the runaway among the mushroom body's Kenyon cells. The wiring says why. An
average Kenyon cell receives about 284 synapses from other Kenyon cells and 55 from dopamine neurons,
both counted as fast excitation by the transmitter sign rule, against about 125 from olfactory
projection neurons and 48 inhibitory synapses from APL. Neither large input is fast excitation in the
fly. Acetylcholine acts on Kenyon cells partly through muscarinic receptors that inhibit them
(mAChR-B; Bielopolski et al. 2019), a slow G-protein effect, and no recording shows Kenyon cells
exciting each other. Dopamine, octopamine and serotonin act through G-protein receptors over hundreds
of milliseconds, as modulation, which is rung 2 of the ladder. shiu_runaway.py removed each on its
own, and each shrank the runaway without ending it. This removes both from the fast network at once
and leaves everything else as in shiu_baseline.py.

Model: brainfly.shiu.ShiuBrain (Shiu's parameters, raw signed synapse counts x w_syn, 0.1 ms steps) on
the MaleCNS counts with (a) every synapse from a neuron whose consensus or predicted transmitter is
dopamine, octopamine or serotonin removed (shiu_runaway.py's definition), and (b) every synapse from
one Kenyon cell onto another removed.
Calibration: Shiu's rule, as in shiu_scaled.py: the w_syn whose MN9 L rate at 100 Hz sugar is closest
to 80% of its maximum over 10-200 Hz, over w_syn = 0.275 x {0.35, 0.5, 0.7, 1, 1.4, 2, 2.8, 4} mV,
10 trials per point.
Tests at the calibrated w_syn: exactly shiu_baseline.py's (30 trials, 100 Hz, same neuron sets and
seeds).
Pass, fixed before the first run: STABLE and SUGAR and NULL, as shiu_scaled.py defines them: the
runaway gone, sugar still reaching MN9, and 20 weight shuffles and 20 degree-preserving rewirings of
this modified matrix each activating MN9 in at most 2.
Reported, not part of the pass: WATER, BITTER, IR94E, and the Kenyon cells' and APL's rates during
sugar.

Re-run 2026-09-26 on brainfly.shiu's corrected kernel, which now matches Brian2 spike for spike
(tests/test_shiu_brian2.py). The first run used a kernel that kept input arriving during
refractoriness, where Brian2 drops it, and ran its steps in a different order; that run is in git
history.

Correction, 2026-09-26: the monoamine rule, consensus or predicted transmitter, also caught 4,058
Kenyon cells, which MaleCNS's machine prediction calls dopaminergic though their consensus
transmitter is acetylcholine. So (a) removed nearly all Kenyon-cell output, not only the synapses
of the 541 neurons whose consensus is a monoamine. The run stands as a test of what it did;
shiu_signs.py reads consensus transmitters only.

    python experiments/shiu_mb.py            (writes experiments/shiu_mb.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pyarrow.feather as feather
from scipy import sparse

from brainfly.data import DATA
from brainfly.shiu import ShiuBrain, counts
from shiu_baseline import SETS, tests
from shiu_scaled import calibrate, nulls

OUT = Path(__file__).with_name("shiu_mb.json")
MONOAMINES = ["dopamine", "octopamine", "serotonin"]


def modified(C: sparse.csr_matrix, mcns_type: np.ndarray) -> tuple[sparse.csr_matrix, dict]:
    """The counts without monoamine synapses and without Kenyon-to-Kenyon synapses."""
    ids = np.load(DATA / "brain.npz")["ids"]
    nt = feather.read_table(DATA / "raw" / "body-neurotransmitters-male-cns-v1.0.feather",
                            columns=["body", "consensus_nt", "predicted_nt"]).to_pandas()
    nt = nt.drop_duplicates("body").set_index("body").reindex(ids)
    amine = (nt.consensus_nt.fillna("").isin(MONOAMINES) | nt.predicted_nt.fillna("").isin(MONOAMINES)).to_numpy()
    kc = np.char.startswith(mcns_type.astype(str), "KC")
    coo = C.tocoo()
    drop = amine[coo.col] | (kc[coo.row] & kc[coo.col])            # columns are presynaptic
    M = sparse.csr_matrix((coo.data[~drop], (coo.row[~drop], coo.col[~drop])), shape=C.shape)
    removed = {"monoaminergic_neurons": int(amine.sum()), "kenyon_cells": int(kc.sum()),
               "synapses_removed_monoamine": int(np.abs(coo.data[amine[coo.col]]).sum()),
               "synapses_removed_kc_to_kc": int(np.abs(coo.data[kc[coo.row] & kc[coo.col]]).sum()),
               "synapses_kept": int(np.abs(M.data).sum())}
    return M, removed


def main() -> None:
    t0 = time.perf_counter()
    probe = ShiuBrain(trials=1)
    M, removed = modified(counts().tocsr(), probe.mcns_type)
    del probe
    results = {"criteria": __doc__, "removed": removed}
    print("removed:", removed, flush=True)
    brain = ShiuBrain(trials=10, matrix=M)
    cells = {k: brain.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([brain.cells(["MN9"], side="L"), brain.cells(["MN9"], side="R")])
    print("calibration (10 trials per point)", flush=True)
    results["calibration"] = calibrate(brain, cells["sugar"], mn9)
    OUT.write_text(json.dumps(results, indent=1))
    w = results["calibration"]["w_syn"]
    if w is None:
        print("sugar never reached MN9; nothing to test", flush=True)
        results["pass"] = False
        OUT.write_text(json.dumps(results, indent=1))
        return
    print(f"calibrated w_syn = {w} mV; tests (30 trials)", flush=True)
    test_brain = ShiuBrain(w_syn=w, trials=30, matrix=M)
    results["tests"] = t = tests(test_brain, cells, mn9)
    print(f"    {json.dumps(t)}", flush=True)
    sugar = test_brain.run(1.0, drive=[(cells["sugar"], 100.0)], seed=1)
    kc = np.char.startswith(test_brain.mcns_type.astype(str), "KC")
    apl = test_brain.mcns_type == "APL"
    results["mushroom_body_during_sugar"] = {"kenyon_cell_mean_hz": round(float(sugar.rates[kc].mean()), 3),
                                             "kenyon_cells_over_100hz": int((sugar.rates[kc] > 100).sum()),
                                             "apl_hz": [round(float(x), 2) for x in sugar.rates[apl]]}
    OUT.write_text(json.dumps(results, indent=1))
    print("nulls (10 trials each)", flush=True)
    results["nulls"] = nulls(M.tocsc(), w, None, cells["sugar"], mn9)
    results["pass"] = bool(t["STABLE"] and t["SUGAR"] and results["nulls"]["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: STABLE {t['STABLE']} SUGAR {t['SUGAR']} NULL {results['nulls']['NULL']} "
          f"| WATER {t['WATER']} BITTER {t['BITTER']} IR94E {t['IR94E']} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
