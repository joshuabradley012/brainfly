"""A 2-D compound eye: every photoreceptor looks in its own measured direction.

eyes.py gives each photoreceptor a single azimuth taken from one column coordinate, so its eye is a
1-D strip. Here each photoreceptor gets a 3-D viewing direction from the eye map of Zhao et al.,
"Eye structure shapes neuron function in Drosophila motion vision": micro-CT viewing directions of
the facets of a female right eye, matched to FlyWire's medulla columns. The data are downloaded
from github.com/reiserlab/eyemap_T4 (GPL-3.0) on first use and not redistributed here.

MaleCNS's column coordinates are FlyWire's with the two axes swapped and shifted by 19:
(hex1, hex2) = (y + 19, x + 19). Under that map the male lattice covers every one of the 778
FlyWire columns, and MaleCNS's dorsal-rim columns (those R7d/R8d feed) land at the top of the eye,
mean elevation z = +0.8 against +0.1 for the whole eye. The male eye has more columns (~890 per
side); the ~100 per side the female map lacks (all within two lattice steps of it) get directions
by smooth extrapolation, held within 5 deg per step of the nearest mapped column. The left eye is
the mirror image. Frame: x anterior, y left, z dorsal.

(eyes.py's 1-D azimuth, taken from hex1, turns out to follow elevation, r = 0.93, not azimuth:
its "loom from the left" was a band sweeping vertically across the left eye.)

A photoreceptor looks where its column looks: R1-6 through the lamina column they feed, R7/R8
through their strongest column-assigned target, and a filled bundle (FlyBrain(fill_retina=True))
through its own column. Each facet sees a Gaussian blur 7.7 deg wide at half maximum
(light-adapted R1-6; Gonzalez-Bellido et al. 2011).

    eye = CompoundEye(brain)
    loom = looming(azimuth=70, elevation=0, r_over_v=0.4, contact=2.2)   # on the left
    brain.step(eye.contrast(loom(t)))
"""
from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import sparse

from .data import ensure_data

EYEMAP_URL = "https://raw.githubusercontent.com/reiserlab/eyemap_T4/main/data"
EYEMAP_FILES = ("eyemap.RData", "med_ixy.RData")
OFFSET = 19               # MaleCNS (hex1, hex2) = FlyWire medulla (y, x) + OFFSET
ACCEPTANCE_DEG = 7.7      # facet blur, full width at half maximum
STEP_DEG = 5.0            # at most this far per lattice step beyond the mapped columns (map: 4.8 median)


@dataclass
class Disk:
    """A dark disk: centre (unit vector), angular radius (radians), darkness 0..1."""
    center: np.ndarray
    radius: float
    darkness: float = 0.9


@dataclass
class Edge:
    """A straight edge sweeping across the field along one axis ("azimuth" or "elevation", in
    degrees; azimuth positive to the fly's left). Where it has passed (coordinate on the `behind`
    side of `position`: -1 below it, +1 above it) the contrast is `contrast` (+1 ON, -1 OFF)."""
    axis: str
    position: float
    behind: int
    contrast: float


@dataclass
class Grating:
    """A sine grating on a distant vertical cylinder around the fly, as on a drum: contrast varies
    as `contrast` x sin(2 pi (azimuth - phase) / period) (degrees; azimuth positive to the fly's
    left) at every elevation. Added to the other objects' contrast."""
    period: float
    phase: float
    contrast: float = 1.0


def direction(azimuth: float, elevation: float) -> np.ndarray:
    """Unit vector for an azimuth (degrees from straight ahead, positive to the fly's left) and an
    elevation (degrees above the horizon)."""
    a, e = np.radians(azimuth), np.radians(elevation)
    return np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])


def looming(azimuth: float, elevation: float, r_over_v: float, contact: float, max_deg: float = 45.0,
            darkness: float = 0.9):
    """A dark disk approaching at constant speed: angular radius atan(r/v / (contact - t)), capped
    at max_deg. Returns t -> [Disk]."""
    center, cap = direction(azimuth, elevation), np.radians(max_deg)

    def scene(t: float) -> list[Disk]:
        return [Disk(center, float(min(np.arctan(r_over_v / max(contact - t, 1e-9)), cap)), darkness)]
    return scene


def _eyemap(data: Path):
    """FlyWire medulla hex (x, y) of each mapped column, and its facet's viewing direction (right eye)."""
    import rdata

    folder = data / "eyemap"
    folder.mkdir(exist_ok=True)
    for name in EYEMAP_FILES:
        if not (folder / name).exists():
            urllib.request.urlretrieve(f"{EYEMAP_URL}/{name}", folder / name)
    load = lambda name: rdata.conversion.convert(rdata.parser.parse_file(folder / name))
    em = load("eyemap.RData")
    pairs = np.asarray(em["eyemap"]).astype(int)                  # row k: (Mi1 id, lens id)
    med = {int(r[0]): (int(r[1]), int(r[2])) for r in np.asarray(load("med_ixy.RData")["med_ixy"])}
    hexes = np.array([med[m] for m in pairs[:, 0]])
    return hexes, np.asarray(em["ucl_rot_sm"], float)            # ucl_rot_sm[k]: facet k's direction


def column_directions(data: Path | str | None = None) -> dict:
    """Viewing direction of every MaleCNS optic lobe column: (side, hex1, hex2) -> unit vector."""
    import pyarrow.feather as feather
    from scipy.interpolate import RBFInterpolator

    from .build import download_all

    data = ensure_data(data)
    download_all(data / "raw")
    hexes, dirs = _eyemap(data)
    fit = RBFInterpolator(hexes.astype(float), dirs, kernel="thin_plate_spline", smoothing=0.0)
    meta = np.load(data / "brain.npz")
    ann = feather.read_table(data / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "assignedOlHex1", "assignedOlHex2"]).to_pandas()
    ann = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(meta["ids"])
    h = ann[["assignedOlHex1", "assignedOlHex2"]].to_numpy(float)
    side = meta["side"].astype(str)
    keys = sorted({(side[i], int(h[i, 0]), int(h[i, 1])) for i in np.flatnonzero(~np.isnan(h[:, 0])) if side[i] in "LR"})
    xy = np.array([(h2 - OFFSET, h1 - OFFSET) for _, h1, h2 in keys], float)
    v = fit(xy)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    # Past the female map the spline can overshoot: keep each extrapolated column within
    # STEP_DEG per lattice step of the nearest mapped column, along the spline's direction.
    mapped = {tuple(p) for p in hexes}
    known = np.array([p for p in xy if tuple(p.astype(int)) in mapped])
    known_dir = fit(known)
    known_dir /= np.linalg.norm(known_dir, axis=1, keepdims=True)
    for k, p in enumerate(xy):
        if tuple(p.astype(int)) in mapped:
            continue
        steps = np.abs(known - p).max(1)
        j = np.argmin(steps)
        limit = np.radians(STEP_DEG) * steps[j]
        near = known_dir[j]
        ang = np.arccos(np.clip(v[k] @ near, -1.0, 1.0))
        if ang > limit:                                          # slerp from `near` towards v[k], stop at the limit
            ortho = v[k] - (v[k] @ near) * near
            ortho /= np.linalg.norm(ortho)
            v[k] = np.cos(limit) * near + np.sin(limit) * ortho
    out = {}
    for (s, h1, h2), d in zip(keys, v):
        out[(s, h1, h2)] = d * (1, -1, 1) if s == "L" else d          # the map is a right eye; mirror for the left
    return out


class CompoundEye:
    """Renders dark disks onto a FlyBrain's photoreceptors. contrast() returns what FlyBrain.step
    takes as eye_drive for graded photoreceptors: 0 on the background, -darkness x coverage."""

    def __init__(self, brain, acceptance_deg: float = ACCEPTANCE_DEG, data: Path | str | None = None):
        import pyarrow.feather as feather

        from .shiu import counts

        data = ensure_data(data)
        cols = column_directions(data)
        meta = np.load(data / "brain.npz")
        n0 = len(meta["ids"])
        ann = feather.read_table(data / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                                 columns=["bodyId", "assignedOlHex1", "assignedOlHex2"]).to_pandas()
        ann = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(meta["ids"])
        h = ann[["assignedOlHex1", "assignedOlHex2"]].to_numpy(float)
        side = meta["side"].astype(str)
        has = ~np.isnan(h[:, 0])
        out_syn = abs(counts(data)).T.tocsr()                          # rows = presynaptic
        self.directions = np.full((len(brain.visual), 3), np.nan)
        for k, i in enumerate(brain.visual):
            if i >= n0:                                                # a filled bundle: its own column
                s, h1, h2 = brain.filled.column[i - n0]
                key = ("R" if s == 1 else "L", int(h1), int(h2))
            else:
                row = out_syn[i]
                ok = has[row.indices]
                if not ok.any():
                    continue
                tally: dict = {}
                for j, w in zip(row.indices[ok], row.data[ok]):
                    c = (side[j], int(h[j, 0]), int(h[j, 1]))
                    tally[c] = tally.get(c, 0.0) + w
                key = max(tally, key=tally.get)
            if key in cols:
                self.directions[k] = cols[key]
        self.placed = ~np.isnan(self.directions[:, 0])
        self.sigma = np.radians(acceptance_deg) / (2 * np.sqrt(2 * np.log(2)))

    def contrast(self, objects: list) -> np.ndarray:
        """Contrast per photoreceptor for dark Disks (the darkest one wins where they overlap) and
        Edges (added), clipped to [-1, 1]."""
        return render(self.directions, self.placed, objects, self.sigma)


def render(directions: np.ndarray, placed: np.ndarray, objects: list, sigma: float) -> np.ndarray:
    """Contrast seen along each of `directions` (unit vectors; only rows where `placed` is true are
    drawn, the rest stay 0) through a Gaussian blur of width sigma (radians), for dark Disks (the
    darkest one wins where they overlap) and Edges and Gratings (added), clipped to [-1, 1]."""
    from scipy.special import chdtr, chndtr, ndtr      # what scipy.stats' ncx2 and chi2 cdfs call, without their per-call checks

    cover = np.zeros(len(directions))
    edges = np.zeros(len(directions))
    d = directions[placed]
    for obj in objects:
        if isinstance(obj, Grating):
            # a sine grating through a Gaussian blur keeps its shape and loses amplitude by
            # exp(-2 pi^2 sigma^2 / lambda^2); at elevation e its period spans lambda cos(e) of visual angle
            az = np.degrees(np.arctan2(d[:, 1], d[:, 0]))
            lam = np.radians(obj.period) * np.sqrt(np.maximum(1 - d[:, 2] ** 2, 1e-6))
            edges[placed] += obj.contrast * np.sin(2 * np.pi * (az - obj.phase) / obj.period) * np.exp(-2 * np.pi ** 2 * sigma ** 2 / lam ** 2)
            continue
        if isinstance(obj, Edge):
            if obj.axis == "azimuth":
                q = np.degrees(np.arctan2(d[:, 1], d[:, 0]))
            else:
                q = np.degrees(np.arcsin(np.clip(d[:, 2], -1.0, 1.0)))
            passed = ndtr(obj.behind * (q - obj.position) / np.degrees(sigma))
            edges[placed] += obj.contrast * passed
            continue
        delta = np.arccos(np.clip(d @ obj.center, -1.0, 1.0))
        x = (obj.radius / sigma) ** 2
        nc = (delta / sigma) ** 2
        # share of a Gaussian blur centred delta from the disk's centre that falls inside it
        frac = np.where(nc > 1e-12, chndtr(x, 2, np.maximum(nc, 1e-12)), chdtr(2, x))
        cover[placed] = np.maximum(cover[placed], obj.darkness * frac)
    return np.clip(edges - cover, -1.0, 1.0).astype(np.float32)
