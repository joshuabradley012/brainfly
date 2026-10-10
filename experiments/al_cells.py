"""The antennal lobe's local neurons as MaleCNS classes them, instead of by their type names.

odor_probe14.LN, a pattern on type names (lLN..., v2LN..., LN60 and the like), selects 321 neurons; MaleCNS's own class
ALLN has 420. The pattern misses 101 of them (17 cholinergic, 25 GABAergic, 27 glutamatergic, 30 unclear and 2
octopaminergic: CB4083, CB1824, CB3417, CB1048, CB3202 and other CB-named types, and 21 untyped) and takes in two
neurons MaleCNS classes ALON (v2LN37). So 25 of the 115 GABAergic local neurons were missing from the presynaptic
inhibition's inhibitors, and 17 cholinergic ones kept their chemical synapses onto PNs (research_notes/Rung 9 learning
data/lateral_excitation.md). These masks take the class itself.
"""
from __future__ import annotations

import functools

import numpy as np
import pyarrow.feather as feather

from brainfly.data import DATA
from brainfly.hybrid import consensus_transmitters


@functools.lru_cache(maxsize=1)
def _classes() -> np.ndarray:
    ids = np.load(DATA / "brain.npz")["ids"]
    ann = feather.read_table(DATA / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "class"]).to_pandas()
    return ann.drop_duplicates("bodyId").set_index("bodyId").reindex(ids)["class"].fillna("").astype(str).to_numpy()


def alln(o) -> np.ndarray:
    """Every neuron MaleCNS classes ALLN (boolean mask over the brain's neurons)."""
    cls = _classes()
    assert len(cls) == o.brain.n
    return cls == "ALLN"


def transmitter(o, nt: str) -> np.ndarray:
    """The ALLNs whose consensus transmitter is nt (boolean mask)."""
    t = np.asarray(consensus_transmitters())
    assert len(t) == o.brain.n
    return alln(o) & (t == nt)


def cholinergic_ln_edges(o) -> np.ndarray:
    """odor_probe14.cholinergic_ln_edges with every cholinergic ALLN: their edges onto uniglomerular PNs."""
    b = o.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    return transmitter(o, "acetylcholine")[pre] & o.m["upn"][b.idx]


def masks(o, plain) -> dict:
    """odor_probe29.pn_only_masks (passed as plain) with the inhibitors every GABAergic ALLN."""
    mk = plain(o)
    mk["inhibitors"] = np.flatnonzero(transmitter(o, "gaba"))
    return mk
