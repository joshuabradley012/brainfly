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

Ran: the LNs keep sustained activity and the PNs keep their onsets, and the fit to flies' EPSCs is the closest yet; the
PNs still don't accommodate. With their own input uninhibited, the GABAergic LNs fire 60 spikes/s each over an odor's
first 50 ms and about 11 from 300 ms on (resting 0.5), a burst about 5.5 times their later activity (flies: 22 and 6-8
over a rest of about 4, about 6 times), so the fit needs far less inhibition: k_A = 0.00044 and k_B = 0.0021 per spike/s
above rest (it oscillated between rounds, the LNs' activity depending strongly on the inhibition through the PNs), giving
EPSCs at 0.32-0.33 of baseline (flies 0.27-0.37) and with GABA-B blocked 0.61-0.71 (0.52-0.81). The synapses then hold
at 0.26-0.39 of their resting strength through an odor, with no onset crash, and the driven PNs fire 130-156 Hz in the
first 100 ms (flies 100-200) but rise through the odor (3-octanol: 83 Hz in the first 50 ms, 122 by 450 ms; 158-206 over
1 s; flies fall to about half by 500 ms). 25-38% of PNs respond by Turner's criterion (flies 59 +- 14%). 3.4-15.9% of
Kenyon cells respond (flies 6 +- 5%), with mean Jaccard 0.19 (flies' dissimilar odors about 0.22) and PN patterns
correlating 0.32, but 65% of 4-methylcyclohexanol's responders also answer 3-octanol, and responding cells fire too
many spikes (alpha/beta 6.3, flies 2.2), as the PNs' rising responses would give; alpha'/beta' cells respond at 1-6%
(flies about 9-14%), gamma at 4-14% (about 2). MBON11 gains 4.5-21 spikes and MBON-alpha2sc 6-39 (flies 110-118 and about
71-85). The transform stays too steep (Rmax 194, 320, 339 and 307; sigma 39, 32, 32 and 28; Olsen 144-170 and 12-16, DM1
45), weak input held back by the synapses' resting depression with spontaneous firing (about 0.4 of full strength; the
notes record about 0.6 at 7 Hz in Kazama & Wilson 2008, where the depression fit predicts 0.44), and lateral input still
divides too much (to 0-0.52). PNs rest at 1.7 Hz, the brain at 1.11 Hz.

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
