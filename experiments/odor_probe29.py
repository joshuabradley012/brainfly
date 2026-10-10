"""Exploratory, not pre-registered: if presynaptic inhibition acts on the receptor neurons' synapses onto projection
neurons but not onto the local neurons, do the local neurons keep more sustained activity, so that the inhibition
fitted to flies' EPSCs no longer swamps an odor's onset?

odor_probe27.py and odor_probe28.py: with inhibition evoked above the GABAergic LNs' resting rate and fitted to Olsen &
Wilson 2008's EPSCs, the LNs burst at an odor's onset (about 46 spikes/s each over the first 50 ms) and then fall back
to near their resting rate, so their activity above rest is about 45 times larger in the burst than later (flies'
LNs: 22 spikes/s over the first 50 ms against 6-8 later, over a rest of about 4: about 6 times; Nagel et al. 2015).
The strengths fitted where the LNs have quieted then swamp the onset: the synapses fall to about 0.05 of their resting
strength within 50 ms and the projection neurons are suppressed at onset, with or without an alpha-shaped onset
(odor_probe28.py). One reason the LNs quiet so far may be the model's own choice that the inhibition acts on every
receptor-neuron output, onto the LNs too, so that their activity cuts their own input. Olsen & Wilson measured the
inhibition only at receptor-to-PN synapses.
Model: odor_probe28.py's (two-stage GABA-A and GABA-B traces evoked above the LNs' rest; spontaneous receptor firing;
the PNs polished one by one), with only the receptor neurons' synapses onto uniglomerular PNs, fast and slow, inhibited
(the receptor neurons' depletion still follows the gain, as their synapses onto PNs dominate it), and k_A and k_B fitted
again. Measured as odor_probe28.py measures. Seeds 230000 (otherwise as odor_probe28.py's, with its offsets).

    python experiments/odor_probe29.py         (writes experiments/odor_probe29.json)
"""
from __future__ import annotations

import odor_probe21 as p21
import odor_probe28 as p28

SEED = 230000
_masks = p21.masks


def pn_only_masks(o):
    """odor_probe21.masks with the fast flags limited to the receptor neurons' synapses onto uniglomerular PNs."""
    mk = _masks(o)
    mk["fast"] = o.orn_pn & (o.brain.weights > 0) & o.m["upn"][o.brain.idx]
    return mk


if __name__ == "__main__":
    from pathlib import Path
    p21.masks = pn_only_masks
    p28.SEED, p28.OUT, p28.__doc__ = SEED, Path(__file__).with_suffix(".json"), __doc__
    p28.main()
