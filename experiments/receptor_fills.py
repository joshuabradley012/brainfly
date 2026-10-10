"""Receptor input DoOR lacks, from a receptor-level measurement: Barth et al. 2014's receptor neuron calcium imaging.

DoOR (brainfly.odors) has 4-methylcyclohexanol data for only 22 of the 35 glomerulus-mapped receptors that have
3-octanol data; the model drives the others with nothing, as if the odor didn't reach them. Barth et al. 2014 imaged the
receptor neurons' terminals in 29 glomeruli (Or83b-GAL4 > GCaMP3) with both odors and saw 4-methylcyclohexanol weakly
exciting four glomeruli DoOR has no data for, and 3-octanol strongly exciting one (VM2, with no data for either).
Converted to DoOR units as research_notes/Rung 9 learning data/oct_mch_input.md ("For the model", 2) converts them
(3-octanol's DoOR value times the two odors' ratio of ΔF/F, or 0.0087 DoOR units per % ΔF/F, the median of 10
glomerulus-odor anchors; the middle of the range where both apply):
  4-methylcyclohexanol: VC1 0.175 (0.10-0.25), VC3 0.125 (0.09-0.16), VM2 0.12, VA7l 0.12
  3-octanol: VM2 0.69
Barth et al.'s "VA7" is taken as VA7l, the subdivision DoOR maps a receptor to (Or46a). A fill applies only where DoOR
has no measurement for the odor at any of the glomerulus's receptors; DoOR's values stand everywhere else (the note keeps
single-sensillum recordings over imaging where they conflict). With them, 4-methylcyclohexanol's summed receptor drive
is 0.48 of 3-octanol's (DoOR alone 0.445; flies' receptor neurons about 0.45, Barth et al. 0.41-0.51).

    with receptor_fills.applied():
        ...                                    # brainfly.odors.glomeruli (and so Receptors.plan) includes the fills

A second tier, PN_INFERRED, is a stand-in, not a measurement: for receptors no study has recorded with the odor at the
receptor level (DoOR or Barth et al.), the receptor input that would give Badel et al. 2016's significant PN responses,
converted at 0.0028 DoOR units per % PN ΔF/F (the median of 10 glomerulus-odor anchors, range 0.0012-0.0081;
oct_mch_input.md, "For the model" 5a). It applies only with applied(pn_inferred=True), after the receptor fills, and only
where neither DoOR nor the receptor fills give a value. With both tiers 4-methylcyclohexanol's summed drive is 0.61 of
3-octanol's.
"""
from __future__ import annotations

import contextlib

import numpy as np

from brainfly import odors

FILLS = {"4-methylcyclohexanol": {"VC1": 0.175, "VC3": 0.125, "VM2": 0.12, "VA7l": 0.12},
         "3-octanol": {"VM2": 0.69}}
PN_INFERRED = {"4-methylcyclohexanol": {"VM7v": 0.34, "DA3": 0.32, "DL4": 0.27, "DA4l": 0.27, "DL3": 0.25, "DA1": 0.22,
                                        "VM3": 0.20},
               "3-octanol": {"DL3": 0.47, "VM3": 0.34, "DA1": 0.33, "DA3": 0.32}}


def measured(name: str) -> set:
    """The glomeruli DoOR has a measured response for the odor at (at any of their receptors)."""
    receptors, keys, M, glom, key_of, sfr = odors._tables()
    row = M[keys.index(key_of[name.lower()])]
    return {g for r, v in zip(receptors, row) if not np.isnan(v) for g in glom.get(r, ())}


def filling(plain, pn_inferred: bool = False):
    """odors.glomeruli with the fills added where DoOR has no measurement (and, with pn_inferred, the PN-inferred tier
    where neither gives one)."""
    def glomeruli(name: str, floor: float = 0.0, inhibition: bool = False) -> dict:
        out = plain(name, floor, inhibition)
        tiers = [FILLS.get(name.lower(), {})] + ([PN_INFERRED.get(name.lower(), {})] if pn_inferred else [])
        if any(tiers):
            have = measured(name)
            for fills in tiers:
                for g, v in fills.items():
                    if g not in have and g not in out and v > floor:
                        out[g] = v
        return out
    return glomeruli


@contextlib.contextmanager
def applied(pn_inferred: bool = False):
    plain = odors.glomeruli
    odors.glomeruli = filling(plain, pn_inferred)
    try:
        yield {"receptor": FILLS, **({"pn_inferred": PN_INFERRED} if pn_inferred else {})}
    finally:
        odors.glomeruli = plain
