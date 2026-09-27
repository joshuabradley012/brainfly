"""brainfly.imaging: Turner et al.'s FC reproduced exactly, the region mapping, and the forward model."""
from __future__ import annotations

import numpy as np
import pytest

from brainfly import imaging
from brainfly.data import DATA

turner_data = pytest.mark.skipif(not ((DATA / "turner2021" / "labels.csv").exists()
                                      or (DATA / "raw" / "data_TurnerMannClandinin.tar.gz").exists()),
                                 reason="needs Turner et al.'s data: brainfly.imaging.turner() fetches it (246 MB)")


@turner_data
def test_reproduces_turners_published_fc():
    flies = imaging.turner()
    published = imaging.published_fc()
    names = list(published.index)
    mean, each = imaging.connectivity({fly: np.array([s[n] for n in names]) for fly, s in flies.items()})
    assert len(flies) == 20 and each.shape == (20, 37, 37)
    np.testing.assert_allclose(mean, published.to_numpy(), atol=1e-12, equal_nan=True)


@turner_data
def test_every_fly_has_every_rest_region():
    signals = imaging.rest_signals(imaging.turner())
    assert all(x.shape[0] == len(imaging.REGIONS) == 66 for x in signals.values())
    assert all(np.isfinite(x).all() for x in signals.values())


@pytest.mark.skipif(not (DATA / "region_weights.npz").exists() and not (DATA / "raw" / "roi_elements.feather").exists(),
                    reason="needs MaleCNS's roi_elements.feather (3.7 GB)")
def test_every_region_maps_onto_malecns_synapses():
    W = imaging.region_weights()
    totals = np.asarray(W.sum(0)).ravel()
    assert W.shape[1] == 66 and (totals > 10_000).all(), dict(zip(imaging.REGIONS, totals))


def test_regional_activity_is_a_synapse_weighted_mean():
    from scipy import sparse

    W = sparse.csr_matrix(np.array([[3.0, 0.0], [1.0, 2.0], [0.0, 2.0]]))      # 3 neurons, 2 regions
    counts = np.array([[2, 0, 4], [0, 1, 1]])                                     # 2 bins
    np.testing.assert_allclose(imaging.regional(counts, W), [[6 / 4, 8 / 4], [1 / 4, 4 / 4]])


def test_imaging_keeps_shared_fluctuations_and_not_independent_ones():
    """Two regions sharing a slow signal correlate strongly through the calcium kernel and 1.2 Hz
    frames; a third, independent region doesn't."""
    rng = np.random.default_rng(0)
    dt, bins = 0.01, 60_000                                          # 10 minutes in 10 ms bins
    slow = np.convolve(rng.normal(size=bins), np.ones(300) / 300, mode="same")
    activity = np.array([slow + 0.02 * rng.normal(size=bins), slow + 0.02 * rng.normal(size=bins),
                         np.convolve(rng.normal(size=bins), np.ones(300) / 300, mode="same")]) + 1.0
    frames = imaging.image(activity, dt)
    assert frames.shape == (3, 720)
    fc, _ = imaging.connectivity({"model": frames}, trims={})     # the first 100 frames go, as in the data:
    assert fc[0, 1] > 1.5 and abs(fc[0, 2]) < 0.2 and abs(fc[1, 2]) < 0.2   # the one-way high-pass's transient


def test_measurement_only_fc_comes_from_shared_neurons():
    """Regions sharing no neuron have zero FC under independent firing; regions sharing neurons
    don't."""
    from scipy import sparse

    W = sparse.csr_matrix(np.array([[4.0, 4.0, 0.0], [2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 5.0]]))
    z = imaging.measurement_only(W)
    assert z[0, 2] == pytest.approx(0.0, abs=1e-9) and z[0, 1] > 0.3 and np.isnan(z[0, 0])
