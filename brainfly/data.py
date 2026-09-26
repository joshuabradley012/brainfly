"""Where brainfly keeps its network files, and fetching a prebuilt copy.

FlyBrain runs on two files that brainfly.build makes from the MaleCNS v1.0 connectome: weights.npz,
the signed and normalised connection matrix, and brain.npz, which holds cell types, sides, soma
positions, superclasses, read-out groups and the photoreceptors with their azimuths. They are too
big to ship with the package, so the first FlyBrain() fetches a prebuilt copy (~260 MB) from this
project's GitHub release into $FLY_DATA (default ~/fly-data), checking each file's sha256.
`brainfly build` makes the same files from the MaleCNS release instead.
"""
from __future__ import annotations

import hashlib
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DATA = Path(os.environ.get("FLY_DATA", Path.home() / "fly-data"))
RELEASE_URL = os.environ.get("BRAINFLY_DATA_URL",
                             "https://github.com/joshuabradley012/brainfly/releases/download/brain-v2")
# sha256 of the released files, built by brainfly.build (166,700 neurons, 25,582,938 connections)
FILES = {
    "brain.npz": "8fba1e790aabe8655ad0895c3fdcbb8e458f4bd5088fb601c48126b67cd9902f",
    "weights.npz": "e00e3f2a9828c921fe1f093cc567bf45a85adad0526176be0aa1b8be09336eeb",
}


def has_data(data: Path | str = DATA) -> bool:
    """Whether both network files are in `data`."""
    folder = Path(data)
    return all((folder / name).is_file() for name in FILES)


def _fetch(url: str, dest: Path, sha256: str) -> None:
    """Stream `url` into `dest` via a .part file, keeping it only if its checksum matches."""
    tmp = dest.parent / f"{dest.name}.part"
    digest = hashlib.sha256()
    try:
        with urllib.request.urlopen(url) as response, open(tmp, "wb") as out:
            size, got = int(response.headers.get("Content-Length") or 0), 0
            while block := response.read(1 << 20):
                out.write(block)
                digest.update(block)
                got += len(block)
                if size:
                    print(f"\r  {got / 1e6:,.0f} of {size / 1e6:,.0f} MB", end="", file=sys.stderr)
        print(file=sys.stderr)
    except (urllib.error.URLError, OSError) as err:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"could not fetch {url}: {err}") from err
    if digest.hexdigest() != sha256:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{url} doesn't match its published checksum; discarded it")
    tmp.replace(dest)


def download(data: Path | str = DATA, url: str = RELEASE_URL, force: bool = False) -> Path:
    """Fetch the prebuilt network files into `data`. Files already there are kept unless force=True."""
    folder = Path(data)
    folder.mkdir(parents=True, exist_ok=True)
    for name, sha256 in FILES.items():
        dest = folder / name
        if dest.exists() and not force:
            continue
        print(f"fetching {name}", file=sys.stderr)
        _fetch(f"{url.rstrip('/')}/{name}", dest, sha256)
    return folder


def ensure_data(data: Path | str | None = None) -> Path:
    """The data folder, after fetching the prebuilt network files into it if they're missing."""
    folder = DATA if data is None else Path(data)
    if has_data(folder):
        return folder
    print(f"brainfly: no network files in {folder}; fetching the prebuilt ones (~260 MB, once)", file=sys.stderr)
    try:
        download(folder)
    except RuntimeError as err:
        raise FileNotFoundError(
            f"no network files in {folder}, and fetching them failed ({err}). Build them from the MaleCNS "
            f"release instead: pip install \"brainfly[build]\" && brainfly build --data \"{folder}\"") from err
    return folder
