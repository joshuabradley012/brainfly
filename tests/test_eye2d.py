"""brainfly.eye2d's renderer on hand-made viewing directions (no eye map needed)."""
import numpy as np

from brainfly.eye2d import Edge, ElevationGrating, Grating, direction, render


def _meridian(n=37):
    """Directions straight ahead at elevations -45..45 deg."""
    el = np.linspace(-45.0, 45.0, n)
    return el, np.array([direction(0.0, e) for e in el])


def test_an_elevation_grating_is_a_blurred_sine_of_elevation():
    el, d = _meridian()
    sigma = np.radians(7.7) / 2.3548
    got = render(d, np.ones(len(d), bool), [ElevationGrating(30.0, 5.0, 0.8)], sigma)
    want = 0.8 * np.sin(2 * np.pi * (el - 5.0) / 30.0) * np.exp(-2 * np.pi ** 2 * sigma ** 2 / np.radians(30.0) ** 2)
    assert np.allclose(got, want, atol=1e-6)


def test_raising_the_phase_moves_the_stripes_up():
    el, d = _meridian(361)
    sigma = np.radians(1.0)
    a = render(d, np.ones(len(d), bool), [ElevationGrating(30.0, 0.0)], sigma)
    b = render(d, np.ones(len(d), bool), [ElevationGrating(30.0, 2.5)], sigma)
    # the peak nearest the horizon moves from 7.5 deg up to 10 deg
    near = np.abs(el) < 15
    assert abs(el[near][np.argmax(a[near])] - 7.5) < 0.5 and abs(el[near][np.argmax(b[near])] - 10.0) < 0.5


def test_adding_the_elevation_grating_leaves_the_other_objects_as_they_were():
    rng = np.random.default_rng(0)
    v = rng.normal(size=(200, 3))
    d = v / np.linalg.norm(v, axis=1, keepdims=True)
    placed = rng.random(200) < 0.8
    objs = [Grating(30.0, 12.0, 0.5), Edge("elevation", 10.0, 1, -0.4)]
    sigma = np.radians(3.0)
    alone = render(d, placed, objs, sigma)
    with_zero = render(d, placed, objs + [ElevationGrating(30.0, 0.0, 0.0)], sigma)
    assert np.array_equal(alone, with_zero)
