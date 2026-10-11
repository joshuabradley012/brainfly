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

RECOMMENDED replaces DoOR (and both tiers) for the two odors altogether, with research_notes/Rung 9 learning
data/oct_mch_concentration.md's receptor-level input at Hige et al.'s 2% of saturated vapour ("For the model"): each
glomerulus from its strongest receptor-level evidence (native single-sensillum recordings, then the empty neuron, imaging,
larval neurons, close analogs), scaled for each study's concentration, with DoOR's import errors corrected (D's
unsubtracted solvent response, DA2's floor) and no drive where flies' PN responses are lateral (DA1, DL3). Summed drive:
3-octanol 5.32 (13 glomeruli above 0.1), 4-methylcyclohexanol 1.99 (2 above 0.1); 0.37. applied(recommended=True).

Checked afterwards (2026-10-11; research_notes/Rung 9 learning data/lateral_pn_responses.md): whole-cell recordings find
DA1, DL3 and DA2 PNs silent to general odors, including those that give Badel et al.'s largest responses there, and
several of Badel et al.'s glomeruli copy a neighbour's signal (DA3 tracks D, DM3 DM6, VM7v VM7d, VM3 VM2). So
PN_INFERRED's DA1, DL3, DA3, VM7v and VM3 entries turn imaging artifacts into receptor drive and make PNs fire where flies'
don't; the tier is kept for reproducing the runs that used it, not for new ones. RECOMMENDED gives DA1 and DL3 no drive,
as the recordings say.
"""
from __future__ import annotations

import contextlib

import numpy as np

from brainfly import odors

FILLS = {"4-methylcyclohexanol": {"VC1": 0.175, "VC3": 0.125, "VM2": 0.12, "VA7l": 0.12},
         "3-octanol": {"VM2": 0.69}}
RECOMMENDED = {
    "3-octanol": {"DC2": 0.75, "VM5d": 0.65, "VM5v": 0.50, "VM2": 0.45, "D": 0.38, "VC3": 0.38, "DM6": 0.34, "DM2": 0.31,
                  "VA4": 0.30, "DM3": 0.28, "VM7v": 0.20, "DC1": 0.17, "VC1": 0.12, "DL4": 0.08, "DA4m": 0.06, "VA3": 0.06,
                  "VM3": 0.06, "DC3": 0.03, "DM5": 0.03, "VM7d": 0.03, "DA3": 0.02, "DM1": 0.02, "VA5": 0.02, "VA6": 0.02,
                  "VC4": 0.02, "DA2": 0.01, "DL1": 0.01, "DL5": 0.01, "VC2": 0.01},
    "4-methylcyclohexanol": {"VA3": 0.70, "D": 0.21, "DA4l": 0.10, "VC3": 0.10, "VC1": 0.09, "VC2": 0.09, "DL4": 0.08,
                             "DM2": 0.08, "VM2": 0.06, "DM6": 0.04, "VM7d": 0.04, "DC1": 0.03, "DC3": 0.03, "DL1": 0.03,
                             "VA7l": 0.03, "VM5d": 0.03, "DA2": 0.02, "DA3": 0.02, "DA4m": 0.02, "DC2": 0.02, "DM5": 0.02,
                             "VA4": 0.02, "VA5": 0.02, "VC4": 0.02, "VM5v": 0.02, "VM7v": 0.02, "DM3": 0.01, "DM4": 0.01,
                             "VA1v": 0.01, "VA6": 0.01, "VM3": 0.01}}
PN_INFERRED = {"4-methylcyclohexanol": {"VM7v": 0.34, "DA3": 0.32, "DL4": 0.27, "DA4l": 0.27, "DL3": 0.25, "DA1": 0.22,
                                        "VM3": 0.20},
               "3-octanol": {"DL3": 0.47, "VM3": 0.34, "DA1": 0.33, "DA3": 0.32}}


def measured(name: str) -> set:
    """The glomeruli DoOR has a measured response for the odor at (at any of their receptors)."""
    receptors, keys, M, glom, key_of, sfr = odors._tables()
    row = M[keys.index(key_of[name.lower()])]
    return {g for r, v in zip(receptors, row) if not np.isnan(v) for g in glom.get(r, ())}


def filling(plain, pn_inferred: bool = False, recommended: bool = False):
    """odors.glomeruli with the fills added where DoOR has no measurement (and, with pn_inferred, the PN-inferred tier
    where neither gives one); with recommended, RECOMMENDED's patterns in place of all of it for its two odors."""
    def glomeruli(name: str, floor: float = 0.0, inhibition: bool = False) -> dict:
        if recommended and name.lower() in RECOMMENDED:
            return {g: v for g, v in RECOMMENDED[name.lower()].items() if v > floor}
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
def applied(pn_inferred: bool = False, recommended: bool = False):
    plain = odors.glomeruli
    odors.glomeruli = filling(plain, pn_inferred, recommended)
    try:
        yield ({"recommended": RECOMMENDED} if recommended else
               {"receptor": FILLS, **({"pn_inferred": PN_INFERRED} if pn_inferred else {})})
    finally:
        odors.glomeruli = plain
