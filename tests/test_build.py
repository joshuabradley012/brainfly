"""Building from the four checksummed MaleCNS source files reproduces the released network files
byte for byte (about 10 s). Needs the 1.1 GB of sources in <data>/raw, which python -m brainfly
build downloads; skipped without them.
"""
from __future__ import annotations

import hashlib

import pytest

from brainfly import build
from brainfly.data import DATA, FILES


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def test_build_reproduces_the_release(tmp_path):
    raw = DATA / "raw"
    if not all((raw / name).is_file() for name in build.SHA256):
        pytest.skip(f"the sources aren't in {raw}: python -m brainfly build downloads them")
    (tmp_path / "raw").symlink_to(raw)
    build.build(tmp_path)
    for name, digest in FILES.items():
        assert sha256(tmp_path / name) == digest, name
