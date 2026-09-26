"""The first eye brainfly had: a one-dimensional panorama across the 6,006 photoreceptors.

Each photoreceptor has one number, an azimuth from -1 (far left) to +1 (far right), taken from its
medulla column by brainfly.build. The scene is a bright background with dark blobs, each covering
an interval of azimuth. Superseded by brainfly.eye2d: this "azimuth" in fact follows elevation.
Kept so the early eye experiments still run.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BACKGROUND = 0.9    # luminance of the empty scene


@dataclass
class Blob:
    """A dark interval of the panorama: centre azimuth (-1..1), half its width (azimuth units),
    and how dark it is (0 invisible, 1 black)."""
    center: float
    half_width: float
    darkness: float


def _luminance(azimuth: np.ndarray, blobs: list[Blob]) -> np.ndarray:
    """Luminance at each azimuth: the background, darkened under each blob (the darkest wins)."""
    lum = np.full(len(azimuth), BACKGROUND, np.float32)
    for blob in blobs:
        under = np.abs(azimuth - blob.center) <= blob.half_width
        lum[under] = np.minimum(lum[under], BACKGROUND * (1 - blob.darkness))
    return lum


class Eyes:
    """Turns scenes into input for FlyBrain's photoreceptors (FlyBrain.azimuth gives the layout)."""

    def __init__(self, azimuth: np.ndarray):
        self.azimuth = azimuth
        self.previous: np.ndarray | None = None

    def drive(self, blobs: list[Blob]) -> np.ndarray:
        """Input for spiking photoreceptors, 0..1: mostly the luminance, plus how much it changed
        since the last call."""
        lum = _luminance(self.azimuth, blobs)
        changed = np.zeros_like(lum) if self.previous is None else np.abs(lum - self.previous)
        self.previous = lum
        return np.clip(0.45 * lum + 1.6 * changed, 0, 1)

    def contrast(self, blobs: list[Blob]) -> np.ndarray:
        """Signed contrast against the background the eye is adapted to: 0 on a blank
        field, -darkness under a blob. The drive for graded photoreceptors, which
        depolarise with light and hyperpolarise with dark; unlike drive(), a darkening
        never excites them."""
        return _luminance(self.azimuth, blobs) / BACKGROUND - 1


def blob_for(dx: float, size: float, darkness: float) -> Blob:
    """A dark object of width `size`, `dx` units to the fly's side (screen units: 110 of them span
    the half-panorama; nearer than 8 units counts as 8)."""
    near = max(abs(dx), 8.0)
    center = float(np.clip(dx / 110.0, -1, 1))
    return Blob(center, float(np.clip(0.5 * size / near, 0.03, 0.7)), darkness)
