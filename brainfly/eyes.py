"""The original 1-D eye: a panorama projected onto the 6,006 photoreceptors.

Each photoreceptor has an azimuth (-1 = far left, +1 = far right) estimated from
the MaleCNS optic-column tables. Superseded by eye2d.py (this "azimuth" in fact
tracks elevation); kept so the early eye experiments still run.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BACKGROUND = 0.9


@dataclass
class Blob:
    center: float      # azimuth, -1..1
    half_width: float  # azimuth units
    darkness: float    # 0 = invisible, 1 = black


def render(azimuth: np.ndarray, blobs: list[Blob]) -> np.ndarray:
    lum = np.full(len(azimuth), BACKGROUND, np.float32)
    for b in blobs:
        inside = np.abs(azimuth - b.center) <= b.half_width
        lum[inside] = np.minimum(lum[inside], BACKGROUND * (1 - b.darkness))
    return lum


class Eyes:
    def __init__(self, azimuth: np.ndarray):
        self.azimuth = azimuth
        self.previous: np.ndarray | None = None

    def drive(self, blobs: list[Blob]) -> np.ndarray:
        lum = render(self.azimuth, blobs)
        change = np.zeros_like(lum) if self.previous is None else np.abs(lum - self.previous)
        self.previous = lum
        return np.clip(0.45 * lum + 1.6 * change, 0, 1)

    def contrast(self, blobs: list[Blob]) -> np.ndarray:
        """Signed contrast against the background the eye is adapted to: 0 on a blank
        field, -darkness under a blob. The drive for graded photoreceptors, which
        depolarise with light and hyperpolarise with dark; unlike drive(), a darkening
        never excites them."""
        return render(self.azimuth, blobs) / BACKGROUND - 1


def blob_for(dx: float, size: float, darkness: float) -> Blob:
    """An object `dx` world units to the side (screen coordinates) of the fly."""
    distance = max(abs(dx), 8.0)
    return Blob(center=float(np.clip(dx / 110.0, -1, 1)),
                half_width=float(np.clip(size / distance * 0.5, 0.03, 0.7)),
                darkness=darkness)
