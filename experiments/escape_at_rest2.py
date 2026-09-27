"""Does the resting brain escape? escape_at_rest.py again, without synapses between visual projection
neurons of the same type (pre-registered).

escape_at_rest.py failed on REST alone. With short-term depression set by synapse class, looming
drove the loomed side's giant fiber by 50-111 Hz, but its left LPLC2, LC4 and giant fiber also ran
at rest (28, 8 and 28 Hz, fly means). ignition.py traced that to a loop among the left LPLC2s, which
are either quiet or at about 93 Hz. The calibration pushes the loop to that edge, because its quiet
state sits below the 2 Hz target (17 of 32 flies ignite after 12 rounds). The loop is LPLC2s exciting
each other: 16% of a left LPLC2's input, 11% of a right one's. MaleCNS puts most of those contacts
between axon terminals in the LPLC2 optic glomerulus. A neuron's own terminals are electrically far
from where it starts its spikes, but a point neuron takes every synapse as input to the cell.
vpn_axoaxonic.py (exploratory) removed every synapse between two visual projection neurons of the
same type (6.8% of those neurons' input), a rule for every such type, and kept every other synapse's
weight. Then no fly of 32 ignited after 12 rounds, 99.94% of groups calibrated within a factor of 2,
and the looming tests passed at gain 1 on seed 1 (giant fiber +25 Hz for either side's loom). This
test takes that rule and does nothing else.
Model: escape_at_rest.py's (rest_calibration2.py's per-type properties; depression by presynaptic
class from research_notes/Rung 4 resting state data/short_term_plasticity.md: every cholinergic
neuron 0.9 of the strength left per spike / 0.5 s to recover; none for sensory neurons other than
olfactory, thermo- and hygroreceptor ones, visual projection neurons or descending neurons; 0.78 /
0.9 s for those receptor neurons, 0.85 / 0.8 s for uniglomerular projection neurons, 0.5 / 1.5 s for
Kenyon cells), with every synapse from a visual projection neuron onto another of its own type
removed from rung 1's network (in the rewirings too, before rewiring).
Everything else as escape_at_rest.py: flyvis's eyes (model 001) as in eyes_at_rest.py, recalibrated
with the eyes open (12 fresh-start rounds from eyes_at_rest.py's biases); eyes_at_rest.py's scenes,
tests (REST, RELAY, SIDE, ESCAPE), gain sweep {1, 3, 10} on seed 1, confirmation of the lowest
passing gain on seed 2, and NULL (in 2 degree-preserving rewirings, recalibrated the same way from
rest_calibration2.py's rewired biases, ESCAPE fails for both looms). Pass: the confirmation passes
and NULL holds.
Reported, not gating: the drum's HS and DNa02 signals at each gain; rung 1's taste tests
(taste_at_rest.py's SUGAR, RESPONSE, BITTER measures, 8 trials) in this brain.

    python experiments/escape_at_rest2.py            (writes experiments/escape_at_rest2.json)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy import sparse

import escape_at_rest as escape
import rest_calibration as attempt1

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
FULL_NETWORK = attempt1.network


def without_same_type_vpn(M: sparse.spmatrix, types: np.ndarray, superclass: np.ndarray) -> sparse.csr_matrix:
    """M (rows postsynaptic) without the synapses from a visual projection neuron onto another of its type."""
    M = M.tocoo()
    vpn = superclass == "visual_projection"
    drop = vpn[M.row] & vpn[M.col] & (types[M.row] == types[M.col]) & (types[M.row] != "")
    return sparse.csr_matrix((M.data[~drop], (M.row[~drop], M.col[~drop])), shape=M.shape)


def network():
    M, scale, labels, types, superclass = FULL_NETWORK()
    return without_same_type_vpn(M, types, superclass), scale, labels, types, superclass


def main() -> None:
    attempt1.network = network
    escape.main(escape.model, OUT, HERE, __doc__)


if __name__ == "__main__":
    main()
