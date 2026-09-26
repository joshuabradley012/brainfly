"""Fill in the photoreceptor input MaleCNS v1.0 lost at the edge of its imaged volume.

The lamina, where photoreceptors R1-6 feed L1-L3, lies at the edge of the MaleCNS volume. Every L1-L3
cell is there (one per column, since most of each cell lies deeper, in the medulla), but in a
contiguous part of each eye their lamina ends were not imaged. About half of the L1 cells receive no
R1-6 synapse at all (two-thirds in the left eye), and the input can't be recovered from the raw
tables: unassigned fragments add about 11 synapses to such a cell and are not histaminergic.

fill() adds one virtual photoreceptor bundle per blind column: the column's six R1-6 cells, which by
neural superposition all view the same point, wired like the median intact column of the same fly:
  bundle -> the column's L1, L2 and L3     synapse counts: median over intact columns
  L2 -> bundle, L4 -> bundle               input shares: median over intact columns' R1-6
A column is an L1 cell's optic-lobe hex coordinate. L2 matches by the same coordinate; L3 by it where
annotated, else by its strongest hex-assigned target (Tm9, Tm20 ...); L4 by its strongest L2 partner,
only where that pick is unambiguous. A bundle looks where build.py points the photoreceptors of its
column (on intact columns that assignment follows the L1 hex coordinate with r = 0.99). Everything
else in these cartridges (amacrine and wide-field partners) stays missing, and the counts are
imputed from other columns, not observed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import sparse

from .data import DATA, ensure_data

INTACT = 5          # R1-6 partners an L1 needs for its column to serve as a template


@dataclass
class Fill:
    """What fill() added. The virtual bundles are neurons n, n+1, ... of the filled network."""
    column: np.ndarray        # (V, 3): side (0 left / 1 right), hex1, hex2 of each bundle
    azimuth: np.ndarray       # (V,)
    targets: dict             # "L1"/"L2"/"L3" -> (V,) neuron index of that column's cell, -1 if none
    template: dict            # median synapse counts and input shares used
    blind_l1: np.ndarray      # L1 cells that had no R1-6 input
    intact_l1: np.ndarray     # L1 cells whose columns served as templates


def _columns(data: Path, C: sparse.csr_matrix, cell_type: np.ndarray, side: np.ndarray):
    import pyarrow.feather as feather

    from .build import download_all

    download_all(data / "raw")
    ids = np.load(data / "brain.npz")["ids"]
    ann = feather.read_table(data / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "type", "assignedOlHex1", "assignedOlHex2"]).to_pandas()
    ann = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(ids)
    t = ann["type"].fillna("").astype(str).to_numpy()
    h1, h2 = ann["assignedOlHex1"].to_numpy(float), ann["assignedOlHex2"].to_numpy(float)
    has = ~np.isnan(h1)
    key = lambda i: (side[i], int(h1[i]), int(h2[i]))
    cols: dict = {}
    for typ in ("L1", "L2", "L3"):
        for i in np.flatnonzero((t == typ) & has):
            cols.setdefault(key(i), {})[typ] = i
    A = abs(C).tocsr()
    # L3 without a coordinate: the column of its strongest hex-assigned target
    AT = A.T.tocsr()                                     # rows = presynaptic
    for i in np.flatnonzero((t == "L3") & ~has):
        row = AT[i]
        ok = has[row.indices]
        if ok.any():
            j = row.indices[ok][np.argmax(row.data[ok])]
            c = cols.setdefault(key(j), {})
            c.setdefault("L3", i)
    # L4: the column of its strongest L2 partner (either direction), if clearly strongest
    l2 = {c["L2"]: k for k, c in cols.items() if "L2" in c}
    l2_idx = np.fromiter(l2, int)
    l4_idx = np.flatnonzero(t == "L4")
    S = (A[l4_idx][:, l2_idx] + A[l2_idx][:, l4_idx].T).toarray()   # L4 x L2 synapses, both directions
    for k, i in enumerate(l4_idx):
        order = np.argsort(S[k])[::-1]
        if S[k, order[0]] > 0 and S[k, order[0]] >= 1.5 * S[k, order[1]]:
            cols[l2[l2_idx[order[0]]]].setdefault("L4", i)
    return cols, h1


def fill(W: sparse.spmatrix, data: Path | str | None = None) -> tuple[sparse.csr_matrix, Fill, dict]:
    """W: the normalised weights (rows = postsynaptic) of brain.npz's neurons. Returns the filled
    weights, (n + V) x (n + V), with every untouched row exactly as in W; what was added; and the new
    neurons' metadata (cell_type, side, superclass) to append."""
    from .shiu import counts

    data = ensure_data(data)
    meta = np.load(data / "brain.npz")
    cell_type, side = meta["cell_type"].astype(str), meta["side"].astype(str)
    visual, azimuth = meta["visual"], meta["azimuth"]
    C = counts(data).tocsr()
    n = C.shape[0]
    A = abs(C).tocsr()
    is_r = cell_type == "R1-6"
    cols, h1 = _columns(data, C, cell_type, side)
    r_in = lambda i: A[i].indices[is_r[A[i].indices]]

    # template: median over intact columns
    out = {x: [] for x in ("L1", "L2", "L3")}
    share = {"L2": [], "L4": []}
    intact = []
    for k, c in cols.items():
        if "L1" not in c or len(r_in(c["L1"])) < INTACT:
            continue
        intact.append(c["L1"])
        rs = np.unique(np.concatenate([r_in(c[x]) for x in ("L1", "L2", "L3") if x in c]))
        for x in out:
            if x in c:
                out[x].append(A[c[x], rs].sum())
        total = A[rs].sum()
        for x in share:
            if x in c and total > 0:
                share[x].append(A[rs][:, [c[x]]].sum() / total)
    template = {f"R1-6 -> {x}": float(np.median(v)) for x, v in out.items()}
    template.update({f"{x} -> R1-6 share": float(np.median(v)) for x, v in share.items()})
    template["intact columns"] = len(intact)

    # one bundle per blind column
    az_of = dict(zip(visual.tolist(), azimuth.tolist()))
    h1_max = np.nanmax(h1)
    blind, rows, colsv, vals, fb = [], [], [], [], []
    column, azs, targets = [], [], {x: [] for x in ("L1", "L2", "L3")}
    for k, c in sorted(cols.items()):
        if "L1" not in c or len(r_in(c["L1"])):
            continue
        v = n + len(column)
        blind.append(c["L1"])
        s, hx1, hx2 = k
        column.append((1 if s == "R" else 0, hx1, hx2))
        frac = (hx1 - 1) / max(h1_max - 1, 1)
        azs.append((0.06 + 0.94 * frac) * (1 if s == "R" else -1))
        for x in ("L1", "L2", "L3"):
            i = c.get(x, -1)
            targets[x].append(i)
            if i >= 0 and not len(r_in(i)):          # only cells with no R1-6 input of their own
                rows.append(i); colsv.append(v); vals.append(-template[f"R1-6 -> {x}"])   # histamine
        for x in ("L2", "L4"):
            if x in c:
                fb.append((v, c[x], template[f"{x} -> R1-6 share"]))
    V = len(column)

    # new rows: blind L cells renormalised with their bundle, bundles with their feedback shares
    W = W.tocsr()
    changed = sorted(set(rows))
    extra = sparse.csr_matrix((vals, (rows, colsv)), shape=(n, n + V))
    Cn = sparse.hstack([C, sparse.csr_matrix((n, V))]).tocsr() + extra
    new = Cn[changed]
    tot = np.asarray(abs(new).sum(1)).ravel()
    new = sparse.diags((1 / np.maximum(tot, 1.0)).astype(np.float32)) @ new
    keep = np.ones(n, bool)
    keep[changed] = False
    base = sparse.diags(keep.astype(np.float32)) @ sparse.hstack([W, sparse.csr_matrix((n, V))]).tocsr()
    place = sparse.csr_matrix((np.ones(len(changed), np.float32), (changed, np.arange(len(changed)))), shape=(n, len(changed)))
    top = (base + place @ new).tocsr()
    fb_rows, fb_cols, fb_vals = zip(*fb) if fb else ((), (), ())
    bottom = sparse.csr_matrix((np.asarray(fb_vals, np.float32), (np.asarray(fb_rows) - n, fb_cols)), shape=(V, n + V))
    Wf = sparse.vstack([top, bottom]).tocsr().astype(np.float32)
    info = Fill(column=np.array(column, int).reshape(-1, 3), azimuth=np.array(azs, np.float32),
                targets={x: np.array(v, int) for x, v in targets.items()}, template=template,
                blind_l1=np.array(blind, int), intact_l1=np.array(intact, int))
    new_meta = {"cell_type": np.full(V, "R1-6"), "side": np.where(info.column[:, 0] == 1, "R", "L"),
                "superclass": np.full(V, "ol_sensory")}
    return Wf, info, new_meta
