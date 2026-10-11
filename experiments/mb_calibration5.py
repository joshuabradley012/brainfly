"""The mushroom body's Kenyon cell-to-MBON synapses in a slow current, as learning_pilot12.py adopted them (2026-10-11).

Yamada et al. 2024's flash EPSC in MBON11 peaks about 100 ms after a 1 ms flash of a few percent of the gamma Kenyon
cells, is 235-260 ms wide at half its peak and decays with a time constant of 256-333 ms; the model's flashed Kenyon cells
fire within about 50 ms, so through the model's 5 ms synapses the current came and went within 20 ms
(kc_flash_check.py). A slow current rising with 40 ms and decaying with 280 ms gives their flash EPSC from about one spike
per flashed cell, and their paired-pulse ratio with the depression the model already has (0.5 of the strength left per
spike, recovering over 1.5 s). Adopted by learning_pilot12.py's rule, stated before it ran: the flash EPSC matched, and
MBON11's response to 3-octanol moved toward flies' on measures the current wasn't chosen from (70.8 evoked spikes against
38.6, flies 118; 50.8 spikes/s from 0.5 to 1 s against 12.4, flies 95-100; a peak of 122 spikes/s, flies 135-140).

    import mb_calibration5
    ...                                  # the Kenyon cell-to-MBON11 synapses set first (mbon11_burst_check.hold, or
    mb_calibration5.install(o)           # learning_pilot4.variant's setup): install moves the fast weights it finds

Every Kenyon cell-to-MBON synapse moves into its target's slow current with its weight times 5 ms / 280 ms, so that a
spike carries the charge it did, depressing with its Kenyon cell as before; the MBONs' slow current rises with RISE,
decays with TAU_SLOW and is kept through their spikes (HybridBrain's slow_rise, tau_slow and slow_keep). The fast
synapses stay in the brain at zero weight: anything that sets the Kenyon cell-to-MBON fast weights afterwards (as the
learning pilots' setup does) would put the fast path back, so install comes last.
"""
from __future__ import annotations

import numpy as np

import mb_calibration3 as mb3
from brainfly.shiu import TAU

TAU_SLOW, RISE = 0.280, 0.040


def install(o) -> dict:
    """Every Kenyon cell-to-MBON synapse with a weight moved into its target's slow current; returns what moved."""
    b = o.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    moved = np.flatnonzero(o.kc_mbon & (b.weights != 0))
    mbons = np.unique(b.idx[moved])
    if np.isin(mbons, b.stargets).any():
        raise RuntimeError("an MBON already has slow input, whose time constant this would change")
    w = b.weights.copy()
    weights = w[moved] * np.float32(TAU / TAU_SLOW)
    w[moved] = 0.0
    b.weights, b._external_matrix = w, None
    mb3.add_slow_edges(b, pre[moved], b.idx[moved], b._counts[moved], weights)
    b.sets = {**b.sets, "mbons_from_kcs": mbons}
    b.set_type("mbons_from_kcs", tau_slow=TAU_SLOW, slow_rise=RISE, slow_keep=1.0)
    return {"synapses_moved": int(len(moved)), "mbons": int(len(mbons)), "tau_slow_s": TAU_SLOW, "rise_s": RISE}
