"""Build brainfly's network files from the MaleCNS v1.0 connectome.

Every neuron MaleCNS assigns a superclass becomes a node. A connection's weight is its synapse
count, negative when the presynaptic neuron's consensus transmitter is inhibitory (GABA,
glutamate, histamine); each neuron's inputs are then divided by their total absolute count, or by
1 if that is smaller, so no neuron receives more than one unit of input. Photoreceptors get an
azimuth from the medulla column they belong to (MaleCNS's optic column assignments), or failing
that from the column of their strongest column-assigned target. The recipe follows Fly64
(github.com/ornata/fly); this is an independent implementation.

Writes <data>/weights.npz (the connection matrix, rows postsynaptic), <data>/brain.npz (cell types,
sides, soma positions, superclasses, descending neuron groups, photoreceptors and their azimuths)
and <data>/brain.json (counts).

    brainfly build [--data DIR]      (needs pip install "brainfly[build]")
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
from scipy import sparse

from .data import DATA

ANNOTATIONS = "body-annotations-male-cns-v1.0-minconf-0.5.feather"
TRANSMITTERS = "body-neurotransmitters-male-cns-v1.0.feather"
CONNECTIONS = "connectome-weights-male-cns-v1.0-minconf-0.5.feather"
COLUMNS = "optic-columns.xlsx"
_FLYEM = "https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome"
SOURCES = {
    ANNOTATIONS: f"{_FLYEM}/{ANNOTATIONS}",
    TRANSMITTERS: f"{_FLYEM}/{TRANSMITTERS}",
    CONNECTIONS: f"{_FLYEM}/{CONNECTIONS}",
    COLUMNS: "https://raw.githubusercontent.com/flyconnectome/2025malecns/67767d2233657983993ff6c2be48e836a935863c/"
             "supplemental_data/optic-column-type-assignments-v1.0.xlsx",
}
# sha256 of each source file as released; the three FlyEM tables match the hashes doomfly
# (github.com/nftechie/doomfly) locked independently
SHA256 = {
    ANNOTATIONS: "2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2",
    TRANSMITTERS: "95c9289220663abeb3409f3ad9e5a7f8a53f8093f5139d15502cd08da8879621",
    CONNECTIONS: "e35da783d1c686b2b58b3b87cd6a403ae43bfcfba8bff28e08ef752c1a56afc1",
    COLUMNS: "d4af1cacb751036f7e84bfecc9bec79ca010066ac066559c29b566003ec080d3",
}
INHIBITORY = "gaba|glutamate|histamine"    # consensus transmitters that make a connection negative
PHOTORECEPTORS = ["R1-6", "R7", "R8"]
# Descending neurons kept as named read-outs: forward walking (DNg100), steering (DNa02), the giant
# fiber's escape (DNp01) and backward walking (MDN, the "moonwalker" neurons).
COMMANDS = {"forward": ["DNg100"], "steer": ["DNa02"], "escape": ["DNp01"], "backward": ["MDN"]}
_CHUNK = 4_000_000                          # connection rows handled at a time


def download_all(raw: Path) -> None:
    """Fetch whichever MaleCNS source files (about 1.1 GB in all) aren't in `raw` yet, keeping each
    only if its sha256 matches the released file's."""
    raw.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        dest = raw / name
        if dest.exists():
            continue
        tmp = dest.parent / f"{dest.name}.part"
        digest = hashlib.sha256()
        print(f"fetching {name}", flush=True)
        with urllib.request.urlopen(url) as response, open(tmp, "wb") as out:
            size, got = int(response.headers.get("Content-Length") or 0), 0
            while block := response.read(1 << 22):
                out.write(block)
                digest.update(block)
                got += len(block)
                if size:
                    print(f"\r  {got / 1e6:,.0f} of {size / 1e6:,.0f} MB", end="", flush=True)
        print()
        if digest.hexdigest() != SHA256[name]:
            tmp.unlink(missing_ok=True)
            raise RuntimeError(f"{name} from {url} doesn't match the released file's sha256; discarded it")
        tmp.replace(dest)


def verify(raw: Path) -> None:
    """Check every source file in `raw` against its released sha256."""
    for name, sha256 in SHA256.items():
        digest = hashlib.sha256()
        with open(raw / name, "rb") as f:
            while block := f.read(1 << 22):
                digest.update(block)
        if digest.hexdigest() != sha256:
            raise RuntimeError(f"{raw / name} doesn't match the released file's sha256; delete it and build again")


def column_assignments(path: Path) -> dict[int, tuple[str, int, int]]:
    """MaleCNS's optic column assignments: body id -> (side, hex1, hex2) for the L1, R7 and R8
    neurons listed against each medulla column (a body listed twice keeps its last column)."""
    import pandas as pd

    out: dict[int, tuple[str, int, int]] = {}
    for sheet in ("Right OL", "Left OL"):
        table = pd.read_excel(path, sheet_name=sheet)
        where = table["column"].astype(str).str.extract(r"^ME_([LR])_col_(\d+)_(\d+)$")
        members = table[["L1", "R7", "R8"]].apply(pd.to_numeric, errors="coerce").to_numpy()
        for (eye, h1, h2), bodies in zip(where.itertuples(index=False), members):
            if not isinstance(eye, str):
                continue
            for body in bodies:
                if body > 0:
                    out[int(body)] = (eye, int(h1), int(h2))
    return out


def _lookup(ids: np.ndarray, bodies: np.ndarray):
    """Row of each body id in the sorted `ids`, and whether it is there at all."""
    row = np.searchsorted(ids, bodies)
    row[row == len(ids)] = 0
    return row, ids[row] == bodies


def connections(path: Path, ids: np.ndarray):
    """Presynaptic row, postsynaptic row and synapse count of every connection between nodes, in
    file order."""
    import pyarrow.feather as feather

    table = feather.read_table(path, columns=["body_pre", "body_post", "weight"], memory_map=True)
    pres, posts, counts = [], [], []
    for start in range(0, table.num_rows, _CHUNK):
        part = table.slice(start, _CHUNK)
        pre, ok_pre = _lookup(ids, part.column("body_pre").to_numpy())
        post, ok_post = _lookup(ids, part.column("body_post").to_numpy())
        keep = ok_pre & ok_post
        pres.append(pre[keep].astype(np.int32))
        posts.append(post[keep].astype(np.int32))
        counts.append(part.column("weight").to_numpy()[keep].astype(np.float32))
        print(f"\r  read {min(start + _CHUNK, table.num_rows):,} of {table.num_rows:,} connection rows", end="", flush=True)
    print()
    return np.concatenate(pres), np.concatenate(posts), np.concatenate(counts)


def transmitter_signs(raw: Path, ids: np.ndarray) -> np.ndarray:
    """-1 for each neuron of `ids` whose consensus transmitter is inhibitory, else +1 (float32)."""
    import pyarrow.feather as feather

    transmitter = feather.read_table(raw / TRANSMITTERS, columns=["body", "consensus_nt"]).to_pandas()
    transmitter = transmitter.drop_duplicates("body").set_index("body")["consensus_nt"].reindex(ids)
    inhibitory = transmitter.fillna("unclear").str.lower().str.contains(INHIBITORY).to_numpy()
    return np.where(inhibitory, np.float32(-1.0), np.float32(1.0))


def _position(value) -> np.ndarray | None:
    return value if isinstance(value, (list, np.ndarray)) and len(value) == 3 else None


def build(data: Path | str = DATA) -> None:
    """Fetch MaleCNS v1.0 into <data>/raw if needed and write weights.npz, brain.npz and brain.json."""
    import pyarrow.feather as feather

    data = Path(data)
    raw = data / "raw"
    download_all(raw)
    verify(raw)

    nodes = feather.read_table(raw / ANNOTATIONS).to_pandas()
    nodes = nodes[nodes["superclass"].fillna("") != ""]
    nodes = nodes.drop_duplicates("bodyId").sort_values("bodyId").set_index("bodyId")
    ids = nodes.index.to_numpy(np.int64)
    n = len(ids)
    print(f"{n:,} neurons", flush=True)

    sign = transmitter_signs(raw, ids)
    pre, post, w = connections(raw / CONNECTIONS, ids)
    w *= sign[pre]
    total_in = np.bincount(post, weights=np.abs(w), minlength=n).astype(np.float32)
    w /= np.maximum(total_in[post], 1.0)
    W = sparse.csr_matrix((w, (post, pre)), shape=(n, n), dtype=np.float32)
    del pre, post, w
    print(f"{W.nnz:,} connections", flush=True)

    cell_type = nodes["flywireType"].combine_first(nodes["type"]).fillna("").astype(str)
    side = nodes["somaSide"].combine_first(nodes["rootSide"]).fillna("").astype(str).str.upper()
    instance = nodes["instance"].fillna("").astype(str).str.upper()
    positions = np.full((n, 3), np.nan, np.float32)
    for row, (soma, tract) in enumerate(zip(nodes["somaLocation"], nodes["tosomaLocation"])):
        at = _position(soma)
        at = _position(tract) if at is None else at
        if at is not None:
            positions[row] = at

    def of_types(types: list[str], on_side: str | None = None) -> np.ndarray:
        chosen = cell_type.isin(types)
        if on_side:
            chosen &= (side == on_side) | instance.str.contains(f"_{on_side}")
        return np.flatnonzero(chosen.to_numpy()).astype(np.int32)

    groups = {f"{name}_{s}": of_types(types, s) for name, types in COMMANDS.items() for s in "LR"}
    empty = [name for name, rows in groups.items() if not len(rows)]
    if empty:
        raise RuntimeError(f"no neurons for the read-out groups {empty}; check COMMANDS")

    # Photoreceptor azimuths: -1 far left ... +1 far right, from how far back its column sits (hex1)
    visual = of_types(PHOTORECEPTORS)
    columns = column_assignments(raw / COLUMNS)
    placed = np.array([row for row, body in enumerate(ids) if int(body) in columns], np.int32)
    to_placed = abs(W[placed][:, visual]).tocsc()       # column k: photoreceptor k's column-assigned targets
    last_h1 = max(h1 for _, h1, _ in columns.values())
    eye = side.to_numpy()[visual].astype(str)
    azimuth = np.full(len(visual), np.nan, np.float32)
    for k, cell in enumerate(visual):
        where = columns.get(int(ids[cell]))
        if where is None:
            lo, hi = to_placed.indptr[k], to_placed.indptr[k + 1]
            if hi > lo:
                strongest = to_placed.indices[lo + np.argmax(to_placed.data[lo:hi])]
                where = columns[int(ids[placed[strongest]])]
        if where is not None:
            eye[k] = where[0]
            depth = (where[1] - 1) / max(last_h1 - 1, 1)
            reach = 0.06 + 0.94 * depth
            azimuth[k] = -reach if where[0] == "L" else reach
    unplaced = np.isnan(azimuth)
    azimuth[unplaced] = np.where(eye[unplaced] == "L", -0.5, 0.5)    # no column: mid-eye
    print(f"{len(visual):,} photoreceptors, {int(unplaced.sum())} without a column", flush=True)

    sparse.save_npz(data / "weights.npz", W, compressed=False)
    text = {name: column.to_numpy().astype(str) for name, column in
            (("cell_type", cell_type), ("side", side), ("superclass", nodes["superclass"]))}
    # in the released file's order, so the build reproduces it byte for byte
    arrays = dict(ids=ids, visual=visual, azimuth=azimuth, cell_type=text["cell_type"], side=text["side"],
                  positions=positions, superclass=text["superclass"])
    arrays.update({f"group_{name}": rows for name, rows in groups.items()})
    np.savez(data / "brain.npz", **arrays)
    summary = {"neurons": n, "connections": int(W.nnz), "photoreceptors": int(len(visual)),
               "groups": {name: int(len(rows)) for name, rows in groups.items()}}
    (data / "brain.json").write_text(json.dumps(summary, indent=2))
    print(f"saved to {data}", flush=True)


if __name__ == "__main__":
    build()
