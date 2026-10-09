"""Odors as olfactory receptor neuron drives, from the DoOR database (Münch & Galizia 2016, ropensci/DoOR.data).

DoOR's consensus response matrix gives each odorant's response at each receptor, scaled 0-1 per receptor (1 its
strongest response to any odorant). Its mapping assigns receptors to antennal lobe glomeruli, which MaleCNS names its
receptor neuron types by (ORN_DM1, ...). An odor here drives every receptor neuron of each glomerulus at its
response times `max_hz`, taking the strongest receptor where several share a glomerulus. A receptor DoOR maps to two
glomeruli (Or33b, in DM5's and DM3's neurons) or to a pair of subdivisions ("DL2d/v": Ir75b, Ir75c and the ac3A neuron)
drives both. Recordings DoOR keeps for a whole sensillum of several neurons (ac1, ac2, ac3 without Or35a) and receptors
with no glomerulus are left out.

    pattern = glomeruli("3-octanol")                     # {glomerulus: response 0-1}
    drive = orn_drive(brain, "3-octanol", max_hz=200)     # [(cells, Hz), ...] for HybridBrain.advance(drive=...)
"""
from __future__ import annotations

import csv
import urllib.request
from functools import lru_cache

import numpy as np

from .data import DATA

SOURCE = "https://raw.githubusercontent.com/ropensci/DoOR.data/master/data/"
FILES = ("door_response_matrix.csv", "door_mappings.csv", "odor.csv")


def _ensure() -> None:
    d = DATA / "door"
    d.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if not (d / f).exists():
            urllib.request.urlretrieve(SOURCE + f, d / f)


@lru_cache(maxsize=1)
def _tables():
    _ensure()
    d = DATA / "door"
    rows = list(csv.reader(open(d / "door_response_matrix.csv"), delimiter=";"))
    receptors, keys = rows[0], [r[0] for r in rows[1:]]
    M = np.array([[float(x) if x not in ("NA", "") else np.nan for x in r[1:]] for r in rows[1:]])
    glom = {}
    for r in list(csv.reader(open(d / "door_mappings.csv"), delimiter=";"))[1:]:     # rows carry a leading index
        receptor, neurons, g = r[1], r[3], r[4]
        if g in ("?", "") or ("+" in neurons and not receptor[:2] in ("Or", "Ir", "Gr")):
            continue                     # no glomerulus, or a whole sensillum's response
        names = []
        for part in g.split("+"):
            if "/" in part:              # "DL2d/v": both subdivisions
                head, tail = part.split("/")
                names += [head, head[:-len(tail)] + tail]
            else:
                names.append(part)
        glom[receptor] = names
    odor = list(csv.reader(open(d / "odor.csv"), delimiter=";"))
    head = odor[0]
    name_col, key_col = head.index("Name") + 1, head.index("InChIKey") + 1      # rows carry a leading index
    key_of = {r[name_col].lower(): r[key_col] for r in odor[1:]}
    return receptors, keys, M, glom, key_of


def glomeruli(name: str, floor: float = 0.0) -> dict[str, float]:
    """An odorant's response at each glomerulus with a mapped, measured receptor (above `floor`), 0-1."""
    receptors, keys, M, glom, key_of = _tables()
    key = key_of.get(name.lower())
    if key is None or key not in keys:
        raise KeyError(f"{name!r} isn't in DoOR")
    row = M[keys.index(key)]
    out: dict[str, float] = {}
    for rec, v in zip(receptors, row):
        if np.isnan(v) or v <= floor:
            continue
        for g in glom.get(rec, ()):
            out[g] = max(out.get(g, 0.0), float(v))
    return out


def orn_drive(brain, name: str, max_hz: float = 200.0, floor: float = 0.0) -> list[tuple[np.ndarray, float]]:
    """(cells, Hz) per glomerulus whose receptor neurons the brain has, for HybridBrain.advance(drive=...)."""
    out = []
    for g, v in glomeruli(name, floor).items():
        cells = brain.cells([f"ORN_{g}"])
        if len(cells):
            out.append((cells, v * max_hz))
    return out
