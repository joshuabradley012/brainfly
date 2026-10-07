"""The optic lobe with flyvis's fitted parameters, on MaleCNS's own wiring.

flyvis (Lappalainen et al. 2024, Nature; github.com/TuragaLab/flyvis, MIT) is the best-validated
model of the fly's early visual system: 65 cell types of graded, passive neurons whose 734
parameters (a time constant and a resting bias per type, and a synapse strength per connected type
pair) were fitted by training on optic flow, and which then predicted responses reported in 26
studies. Its dynamics, per neuron i of type t:

    tau_t dV_i/dt = -V_i + bias_t + sum_j sign * strength(t_j, t) * n_ij * relu(V_j) + x_i

with n_ij synapse counts from its own connectome (FIB-25/FIB-19 averages on a 721-column lattice)
and x_i the light reaching photoreceptors. Here the same equations and fitted parameters run on
MaleCNS's neurons and synapses. Two adjustments:
- scale: MaleCNS counts synapses on a different scale from flyvis's connectome. Each neuron's
  input from each presynaptic type is scaled to sum to flyvis's total for that type pair, keeping
  its own partners and their relative counts. (A hobby port found that transferring the parameters
  unscaled broke motion detection; matching only the average per type pair left some neurons with
  far more same-type recurrent input than flyvis allows, and T2/T4/T5/TmY18 loops ran away.) A
  lamina column with only some of its photoreceptors left counts as a full one, as under neural
  superposition all six view the same point.
- types: flyvis's R1-R6 map to MaleCNS's lumped R1-R6 (averaged parameters), its lamina amacrine
  "Am" to MaleCNS's Lai, and TmY9 to TmY9a/b/q. CT1 (two compartments in flyvis, one giant neuron
  in MaleCNS) and Mi3, Mi11, Mi12 and Tm28 (not in MaleCNS) are left out. Only connections between
  flyvis types that flyvis models are used; the rest of the optic lobe runs in FlyBrain.
Virtual photoreceptor bundles (FlyBrain(fill_retina=True)) are wired at flyvis's own per-column
totals.

Known deviations (experiments/flyvis_port.py): on a grey field this port rests at a different
operating point from flyvis on its own connectome. The inhibition flyvis gets from CT1 (left out),
Mi12 (not in MaleCNS) and R7/R8 (absent from the filled columns) goes missing, and recurrent loops
amplify the shift: T4a/b rest at +2.1 instead of 0, T2 at +7.7 instead of +3.5, and the OFF cells
Tm2, Tm4 and TmY3 so far below zero that an OFF step barely moves their output (Tm1 rests normally
but loses its OFF response). Only two of the four T5 subtypes get the right direction. The input
layers (R1-6, L1-L5, Tm9) match.
"""
from __future__ import annotations

import os
from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import DATA, ensure_data

MODEL = "flow/0000/000"     # flyvis's best published model; the inherited FlyvisOpticLobe's default
EYE = "flow/9014/000"       # rung 3's eye: flyvis's model 001 fine-tuned with rung 3's direction test and the known
                            # polarities in its loss (experiments/rung3_001.py); FlyvisNative's default
SHIPPED = {EYE: "flow/0000/001"}   # fine-tuned models brainfly ships (brainfly/models), by the flyvis model each came from
BACKGROUND = 0.5          # flyvis's grey
# A FlyBrain graded set covering every flyvis type: the retina and optic lobe, plus TmY14, which
# MaleCNS files under visual projection neurons.
GRADED = ["R1-6", "R7", "R8", "ol_intrinsic", "TmY14"]
R16 = ["R1", "R2", "R3", "R4", "R5", "R6"]
RENAME = {"Lai": "Am", "TmY9a": "TmY9", "TmY9b": "TmY9", "TmY9q": "TmY9", "TmY9q__perp": "TmY9"}


def ensure_model(model: str, data: Path | str | None = None) -> Path:
    """A flyvis model's folder under flyvis's results, fetching flyvis's pretrained models if needed. A fine-tuned
    model brainfly ships (SHIPPED) is built from the model it came from, with its checkpoint from brainfly/models."""
    data = DATA if data is None else Path(data)                 # flyvis's models only; not brainfly's network files
    os.environ.setdefault("FLYVIS_ROOT_DIR", str(data / "flyvis"))
    import flyvis

    folder = flyvis.results_dir / model
    if folder.exists():
        return folder
    source = SHIPPED.get(model, model)
    if not (flyvis.results_dir / source).exists():            # flyvis doesn't fetch its own pretrained models
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "flyvis_cli.download_pretrained_models", "--skip_large_files"],
                       check=True)
    if model in SHIPPED:
        import shutil
        shipped = Path(__file__).with_name("models") / model.replace("/", "_")
        shutil.copytree(flyvis.results_dir / source, folder, ignore=shutil.ignore_patterns("__cache__"))
        for name in ("best_chkpt", "validation_loss.h5", "brainfly.json"):
            shutil.copy(shipped / name, folder / name)
        shutil.copy(shipped / "best_chkpt", folder / "chkpts" / "chkpt_00000")
    return folder


def _network(model: str, data: Path):
    """flyvis's pretrained network (downloading or installing the model first if needed)."""
    from flyvis import NetworkView

    return NetworkView(ensure_model(model, data)).init_network(checkpoint="best")


def flyvis_params(model: str = MODEL, data: Path | str | None = None) -> dict:
    """Per-type time constants and biases, and per type pair (sign, strength, total synapses a
    target neuron receives), with flyvis's R1-R6 merged into one type "R1-6"."""
    data = ensure_data(data)
    cache = data / f"flyvis_{model.replace('/', '_')}.npz"
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        return z["params"].item()
    net = _network(model, data)
    arr = lambda p: p.semantic_values.detach().cpu().numpy()
    tau = dict(zip(net.node_params["time_const"].keys, arr(net.node_params["time_const"]).tolist()))
    bias = dict(zip(net.node_params["bias"].keys, arr(net.node_params["bias"]).tolist()))
    sign = dict(zip(net.edge_params["sign"].keys, arr(net.edge_params["sign"]).tolist()))
    strength = dict(zip(net.edge_params["syn_strength"].keys, arr(net.edge_params["syn_strength"]).tolist()))
    c = net.connectome
    u, v = np.asarray(c.nodes.u[:]), np.asarray(c.nodes.v[:])
    tgt = np.asarray(c.edges.target_index[:])
    centre = (u[tgt] == 0) & (v[tgt] == 0)                      # the central column: no lattice edge
    total: dict = {}
    for s, t, n in zip(np.asarray(c.edges.source_type[:]).astype(str)[centre],
                       np.asarray(c.edges.target_type[:]).astype(str)[centre], np.asarray(c.edges.n_syn[:])[centre]):
        total[(s, t)] = total.get((s, t), 0.0) + float(n)
    merge = lambda x: "R1-6" if x in R16 else x
    out = {"tau": {}, "bias": {}, "pairs": {}}
    for t in tau:
        out["tau"].setdefault(merge(t), []).append(tau[t])
        out["bias"].setdefault(merge(t), []).append(bias[t])
    out["tau"] = {t: float(np.mean(v)) for t, v in out["tau"].items()}
    out["bias"] = {t: float(np.mean(v)) for t, v in out["bias"].items()}
    acc: dict = {}
    for (s, t), n in total.items():
        key = (merge(s), merge(t))
        a = acc.setdefault(key, {"n": 0.0, "sw": 0.0, "sign": sign[(s, t)], "targets": set()})
        a["n"] += n
        a["sw"] += n * strength[(s, t)]
        a["targets"].add(t)
    for key, a in acc.items():   # a merged target type (R1-6) gets the average over R1..R6, not the sum
        k = len(a["targets"])
        out["pairs"][key] = (float(a["sign"]), a["sw"] / a["n"] if a["n"] else 0.0, a["n"] / k)
    np.savez(cache, params=np.array(out, dtype=object))
    return out


def flyvis_type(brain, mcns_type: np.ndarray, known: set) -> np.ndarray:
    """flyvis type of each FlyBrain neuron ("" if it isn't one of flyvis's)."""
    out = np.full(brain.n, "", dtype=object)
    n0 = len(mcns_type)
    ct = brain.cell_type.astype(str)
    for i in range(brain.n):
        name = ct[i] if i >= n0 else mcns_type[i]
        if name in ("R1-R6", "R1-6") or ct[i] == "R1-6":
            out[i] = "R1-6"
        elif ct[i] in ("R7", "R8"):
            out[i] = ct[i]
        else:
            name = RENAME.get(name, name)
            out[i] = name if name in known else ""
    return out


class FlyvisOpticLobe:
    """flyvis's optic lobe on MaleCNS wiring, feeding a FlyBrain built with graded optic lobe
    neurons (e.g. graded=["R1-6", "R7", "R8", "ol_intrinsic"]). Deterministic, so one simulation
    serves every fly in the batch."""

    def __init__(self, brain, model: str = MODEL, gain: float = 0.3, data: Path | str | None = None):
        from .shiu import counts, mcns_types

        data = ensure_data(data)
        p = flyvis_params(model, data)
        known = set(p["tau"])
        ftype = flyvis_type(brain, mcns_types(data), known)
        self.neurons = np.flatnonzero(ftype != "")
        missing = np.setdiff1d(self.neurons, brain.graded)
        if len(missing):
            raise ValueError(f"{len(missing)} flyvis-type neurons aren't graded in this FlyBrain "
                             f"(types {sorted(set(ftype[missing]))}); build it with graded=GRADED")
        self.types = ftype[self.neurons].astype(str)
        pos = -np.ones(brain.n, int)
        pos[self.neurons] = np.arange(len(self.neurons))
        C = abs(counts(data)).tocoo()                       # the connectome's own neurons, n0 of them
        n0 = C.shape[0]
        keep = (pos[C.row] >= 0) & (pos[C.col] >= 0)
        rows, cols, n = pos[C.row[keep]], pos[C.col[keep]], C.data[keep].astype(float)
        tt, ts = self.types[rows], self.types[cols]
        # each neuron's input from each presynaptic type sums to flyvis's total for that type pair
        w = np.zeros(len(n))
        for (s, t), (sign, strength, total) in p["pairs"].items():
            m = (ts == s) & (tt == t)
            if not m.any():
                continue
            per_target = np.bincount(rows[m], weights=n[m], minlength=len(self.neurons))
            w[m] = sign * strength * total * n[m] / per_target[rows[m]]
        W = sparse.csr_matrix((w, (rows, cols)), shape=(len(self.neurons),) * 2)
        # virtual photoreceptor bundles: one per blind column, at flyvis's per-column totals
        extra = []
        if brain.filled is not None:
            for x, targets in brain.filled.targets.items():
                out_pair = p["pairs"].get(("R1-6", x))      # bundle -> the column's L cell (a whole column's R1-6)
                back_pair = p["pairs"].get((x, "R1-6"))     # the column's L cell -> bundle (per photoreceptor)
                for k, cell in enumerate(targets):
                    if cell < 0 or pos[cell] < 0:
                        continue
                    if out_pair and x in ("L1", "L2", "L3"):
                        extra.append((pos[cell], pos[n0 + k], out_pair[0] * out_pair[1] * out_pair[2]))
                    if back_pair:
                        extra.append((pos[n0 + k], pos[cell], back_pair[0] * back_pair[1] * back_pair[2]))
        if extra:
            r, c_, v = zip(*extra)
            W = W + sparse.csr_matrix((v, (r, c_)), shape=W.shape)
        self.W = W.tocsr()
        self.tau = np.array([max(p["tau"][t], brain.dt) for t in self.types])
        self.bias = np.array([p["bias"][t] for t in self.types])
        self.dt = brain.dt
        self.gain = float(gain)
        vis = {int(i): k for k, i in enumerate(brain.visual)}
        self._input = np.array([k for k, i in enumerate(self.neurons) if int(i) in vis])
        self._visual_row = np.array([vis[int(self.neurons[k])] for k in self._input])
        self._settled = None
        self.reset()

    def _x(self, contrast):
        x = np.zeros(len(self.neurons))
        if contrast is not None:
            x[self._input] = BACKGROUND * (1 + np.asarray(contrast, float)[self._visual_row])
        else:
            x[self._input] = BACKGROUND
        return x

    def reset(self, seconds: float = 10.0) -> None:
        """Settle on a blank grey field; that state is what release changes are measured from.
        The settled state is computed once and restored on later resets."""
        if self._settled is None or self._settled[0] != seconds:
            self.V = self.bias.copy()
            x = self._x(None)
            for _ in range(int(round(seconds / self.dt))):
                self._advance(x)
            self._settled = (seconds, self.V.copy())
        self.V = self._settled[1].copy()
        self.rest = np.maximum(self.V, 0)

    def _advance(self, x) -> None:
        drive = self.W @ np.maximum(self.V, 0)
        self.V = self.V + self.dt / self.tau * (-self.V + self.bias + drive + x)

    def step(self, contrast) -> np.ndarray:
        """Advance one step (the brain's dt) on the light contrast per photoreceptor
        (CompoundEye.contrast); returns the release change of each neuron in self.neurons, per 20 ms
        as FlyBrain.set_graded takes it."""
        self._advance(self._x(contrast))
        return (self.gain * (np.maximum(self.V, 0) - self.rest)).astype(np.float32)


# flyvis on its own terms: its fitted network tiled onto the male eye's columns.

S3 = np.sqrt(3) / 2


def to_mcns(du, dv):
    """A flyvis lattice offset (source minus target, in flyvis's axial (u, v)) as a MaleCNS column
    offset (hex1, hex2). Found from anatomy (experiments/flyvis_native.py): under this map, and no
    other symmetry of the hex lattice, T4a-d's Mi4, Mi9 and C3 inputs and T5a-d's Tm9 inputs lie in
    the same directions from their Mi1 / Tm1 inputs in both connectomes, on both sides."""
    return -du, -du - dv


def from_mcns(a, b):
    """The inverse of to_mcns."""
    return -a, a - b


def plane(h1, h2) -> np.ndarray:
    """MaleCNS column coordinates as points in the plane, neighbouring columns one unit apart."""
    b = -np.asarray(h2, float)
    return np.stack([np.asarray(h1, float) + b / 2, S3 * b], -1)


def flyvis_filters(model: str = MODEL, data: Path | str | None = None) -> dict:
    """flyvis's network as it defines it, by spatial filters: per type a time constant and a bias;
    per type pair a sign and a strength; per filter element (source, target, du, dv) a synapse
    count, (du, dv) being the target's position minus the source's in flyvis's axial lattice
    coordinates; and the positions of the types that don't tile every column (Lawf1, Lawf2)."""
    data = ensure_data(data)
    cache = data / f"flyvis_filters_{model.replace('/', '_')}.npz"
    if cache.exists():
        return np.load(cache, allow_pickle=True)["filters"].item()
    net = _network(model, data)
    arr = lambda p: p.semantic_values.detach().cpu().numpy().tolist()
    npar, epar = net.node_params, net.edge_params
    out = {"tau": {str(k): x for k, x in zip(npar["time_const"].keys, arr(npar["time_const"]))},
           "bias": {str(k): x for k, x in zip(npar["bias"].keys, arr(npar["bias"]))},
           "sign": {(str(s), str(t)): x for (s, t), x in zip(epar["sign"].keys, arr(epar["sign"]))},
           "strength": {(str(s), str(t)): x for (s, t), x in zip(epar["syn_strength"].keys, arr(epar["syn_strength"]))},
           "count": {(str(s), str(t), int(du), int(dv)): x
                     for (s, t, du, dv), x in zip(epar["syn_count"].keys, arr(epar["syn_count"]))}}
    c = net.connectome
    ty = np.asarray(c.nodes.type[:]).astype(str)
    u, v = np.asarray(c.nodes.u[:]), np.asarray(c.nodes.v[:])
    full = int((ty == "L1").sum())
    out["sparse"] = {str(t): np.stack([u[ty == t], v[ty == t]], 1) for t in np.unique(ty) if (ty == t).sum() < full}
    out["radius"] = int(np.max(np.maximum(np.maximum(abs(u), abs(v)), abs(u + v))))
    np.savez(cache, filters=np.array(out, dtype=object))
    return out


def _sublattice(points: np.ndarray, radius: int) -> np.ndarray:
    """Basis (rows) of the lattice through the origin that `points` (flyvis (u, v)) fill inside
    flyvis's hexagon of this radius."""
    ring = lambda q: np.maximum(np.maximum(abs(q[..., 0]), abs(q[..., 1])), abs(q[..., 0] + q[..., 1]))
    diffs = {tuple(d) for d in (points[:, None] - points[None]).reshape(-1, 2).tolist() if any(d)}
    cand = sorted(diffs, key=lambda d: ring(np.array(d)))[:40]
    grid = np.array([(a, b) for a in range(-radius, radius + 1) for b in range(-radius, radius + 1)])
    grid = grid[ring(grid) <= radius]
    want = set(map(tuple, points.tolist()))
    best = None
    for i, b1 in enumerate(cand):
        for b2 in cand[i + 1:]:
            B = np.array([b1, b2], float)
            det = abs(np.linalg.det(B))
            if det < 0.5 or (best is not None and det >= best[0]):
                continue
            coef = np.linalg.solve(B.T, grid.T).T
            member = np.all(np.abs(coef - np.round(coef)) < 1e-6, 1)
            if set(map(tuple, grid[member].tolist())) == want:
                best = (det, np.array([b1, b2]))
    if best is None:
        raise ValueError("these cells don't form a lattice")
    return best[1]


def tile(columns: np.ndarray, origin: np.ndarray, f: dict):
    """flyvis's cells and synapses on MaleCNS columns (N, 2) of (hex1, hex2): one cell of each type
    per column, the sparse types on their sub-lattice through `origin`. Returns each cell's type,
    its column (an index into `columns`) and the weights (rows postsynaptic)."""
    cell_type, cell_col, rows, cols, element, keys = tile_entries(columns, origin, f)
    w = np.array([f["sign"][(s, t)] * f["strength"][(s, t)] * f["count"][(s, t, du, dv)] for s, t, du, dv in keys])
    W = sparse.csr_matrix((w[element], (rows, cols)), shape=(len(cell_type),) * 2)
    return cell_type, cell_col, W


def tile_entries(columns: np.ndarray, origin: np.ndarray, f: dict):
    """tile's cells and synapses before weighting: each cell's type and column, and per synapse its target and source
    cell and its filter element (an index into keys, f["count"]'s keys in order). brainfly.eyetorch weights them with
    a flyvis network's own parameters."""
    types = sorted(f["tau"])
    reach = int(np.abs(np.array([(k[2], k[3]) for k in f["count"]])).max()) * 2 + 1
    lo = columns.min(0) - reach
    grid = -np.ones((len(types),) + tuple(columns.max(0) - lo + reach + 1), int)
    cell_type, cell_col = [], []
    for k, t in enumerate(types):
        hosts = np.arange(len(columns))
        if t in f["sparse"]:
            B = _sublattice(f["sparse"][t], f["radius"]).astype(float)
            uv = np.stack(from_mcns(*(columns - origin).T), 1)
            coef = np.linalg.solve(B.T, uv.T).T
            hosts = hosts[np.all(np.abs(coef - np.round(coef)) < 1e-6, 1)]
        grid[k][tuple((columns[hosts] - lo).T)] = len(cell_type) + np.arange(len(hosts))
        cell_type += [t] * len(hosts)
        cell_col += hosts.tolist()
    cell_type, cell_col = np.array(cell_type), np.array(cell_col)
    of_type = {t: np.flatnonzero(cell_type == t) for t in types}
    index = {t: k for k, t in enumerate(types)}
    keys = list(f["count"])
    rows, cols, element = [], [], []
    for k, (s, t, du, dv) in enumerate(keys):
        tgt = of_type[t]
        src = grid[index[s]][tuple((columns[cell_col[tgt]] + (du, du + dv) - lo).T)]
        ok = src >= 0
        rows.append(tgt[ok])
        cols.append(src[ok])
        element.append(np.full(int(ok.sum()), k))
    return cell_type, cell_col, np.concatenate(rows), np.concatenate(cols), np.concatenate(element), keys



def matvec(W: sparse.csr_matrix, x: np.ndarray) -> np.ndarray:
    """W @ x, the same numbers scipy gives, about 3x faster: rows in parallel, each summed in order
    with fused multiply-adds, as scipy's compiled csr_matvec sums them (tests/test_optic.py checks
    they agree bit for bit)."""
    return _matvec(W.indptr, W.indices, W.data, np.ascontiguousarray(x, np.float64))


@numba.njit(parallel=True, fastmath={"contract"}, cache=True)
def _matvec(indptr, indices, data, x):
    out = np.empty(len(indptr) - 1)
    for r in numba.prange(len(indptr) - 1):
        total = 0.0
        for e in range(indptr[r], indptr[r + 1]):
            total += data[e] * x[indices[e]]
        out[r] = total
    return out


class FlyvisNative:
    """flyvis's fitted network on its own terms, driving a FlyBrain (set_graded) or a HybridBrain
    (set_release, whose release is in Hz: 50 x this class's output). Its cells and synapses are tiled
    onto the male fly's eye: one cell of each of flyvis's 65 types per MaleCNS optic lobe column
    (Lawf1/2 on flyvis's sparse sub-lattice), wired by flyvis's spatial filters and oriented by
    to_mcns, one copy per eye. Each column looks in its measured direction (brainfly.eye2d). A
    MaleCNS neuron of a flyvis type takes the activity of its type's cell in its column; neurons
    without an assigned column (T4, T5, T2, the TmY cells, photoreceptors, ...) take the column at
    the synapse-weighted centroid of their column-assigned partners. The change of relu(V) from rest, times `gain`, reaches FlyBrain
    as graded release (FlyBrain.set_graded), per 20 ms. Deterministic: one simulation serves every
    fly in a batch."""

    def __init__(self, brain, model: str = EYE, gain: float = 1.0, data: Path | str | None = None,
                 dt: float | None = None):
        """dt: the optic lobe's step, s (default the brain's; a HybridBrain's 0.1 ms is needlessly
        fine for flyvis, so step it every 2 ms and hold its output in between)."""
        import pyarrow.feather as feather

        from .eye2d import ACCEPTANCE_DEG, column_directions
        from .shiu import counts, mcns_types

        data = ensure_data(data)
        f = flyvis_filters(model, data)
        dirs = column_directions(data)
        blocks, cell_type, cell_col, cell_side, keys = [], [], [], [], []
        self.origin = {}
        for side in "LR":
            ks = sorted(k for k in dirs if k[0] == side)
            C = np.array([(h1, h2) for _, h1, h2 in ks])
            xy = plane(*C.T)
            self.origin[side] = C[np.argmin(((xy - xy.mean(0)) ** 2).sum(1))]
            ct, cc, W = tile(C, self.origin[side], f)
            blocks.append(W)
            cell_type.append(ct)
            cell_col.append(cc + len(keys))
            cell_side.append(np.full(len(ct), side))
            keys += ks
        self.W = sparse.block_diag(blocks, format="csr")
        self.cell_type = np.concatenate(cell_type)
        self.cell_col = np.concatenate(cell_col)
        self.cell_side = np.concatenate(cell_side)
        self.column_keys = keys                                    # (side, hex1, hex2) per column
        self.directions = np.array([dirs[k] for k in keys])
        self.sigma = np.radians(ACCEPTANCE_DEG) / (2 * np.sqrt(2 * np.log(2)))
        self.dt = brain.dt if dt is None else float(dt)
        self.tau = np.array([max(f["tau"][t], self.dt) for t in self.cell_type])
        self.bias = np.array([f["bias"][t] for t in self.cell_type])
        self._input = np.flatnonzero(np.isin(self.cell_type, R16 + ["R7", "R8"]))
        self.gain = float(gain)

        # MaleCNS neurons of flyvis types, and the cell(s) each one reads
        ftype = flyvis_type(brain, mcns_types(data), set(f["tau"]) | {"R1-6"})
        meta = np.load(data / "brain.npz")
        n0 = len(meta["ids"])
        ann = feather.read_table(data / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                                 columns=["bodyId", "assignedOlHex1", "assignedOlHex2"]).to_pandas()
        ann = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(meta["ids"])
        hexes = ann[["assignedOlHex1", "assignedOlHex2"]].to_numpy(float)
        has = ~np.isnan(hexes[:, 0])
        side = brain.side.astype(str)
        pos = np.full((n0, 2), np.nan)
        pos[has] = plane(hexes[has, 0], hexes[has, 1])
        col_index = {k: j for j, k in enumerate(keys)}
        col_xy = {s: (np.array([j for j, k in enumerate(keys) if k[0] == s]),
                      plane(*np.array([(k[1], k[2]) for k in keys if k[0] == s]).T)) for s in "LR"}
        cell_at = {(t, int(c)): i for i, (t, c) in enumerate(zip(self.cell_type, self.cell_col))}
        hosts = {t: np.unique(self.cell_col[self.cell_type == t]) for t in f["sparse"]}
        C = abs(counts(data)).tocsr()                              # rows postsynaptic
        partners = (C + C.T).tocsr()                               # inputs and outputs
        rows, cells, weights, neurons, types = [], [], [], [], []
        for i in np.flatnonzero(ftype != ""):
            t, s = ftype[i], side[i]
            if s not in "LR":
                continue
            if i >= n0:                                            # a filled photoreceptor bundle
                sc, h1, h2 = brain.filled.column[i - n0]
                col = col_index.get(("R" if sc == 1 else "L", int(h1), int(h2)))
            elif has[i]:
                col = col_index.get((s, int(hexes[i, 0]), int(hexes[i, 1])))
            else:                                                  # the centroid of its column-assigned partners
                row = partners[i]
                ok = has[row.indices] & (side[row.indices] == s)
                if not ok.any():
                    continue
                w = row.data[ok]
                centre = pos[row.indices[ok]].T @ w / w.sum()
                idx, xy = col_xy[s]
                allowed = np.isin(idx, hosts[t]) if t in hosts else slice(None)
                j = np.argmin(((xy[allowed] - centre) ** 2).sum(1))
                col = int(idx[allowed][j])
            if col is None:
                continue
            reads = [cell_at.get((r, col)) for r in (R16 if t == "R1-6" else [t])]
            reads = [r for r in reads if r is not None]
            if not reads:
                continue
            rows += [len(neurons)] * len(reads)
            cells += reads
            weights += [1.0 / len(reads)] * len(reads)
            neurons.append(i)
            types.append(t)
        self.neurons = np.array(neurons)
        self.types = np.array(types)
        missing = [] if hasattr(brain, "set_release") else np.setdiff1d(self.neurons, brain.graded)
        if len(missing):
            raise ValueError(f"{len(missing)} flyvis-type neurons aren't graded in this FlyBrain; build it with graded=GRADED")
        self.readout = sparse.csr_matrix((weights, (rows, cells)), shape=(len(neurons), len(self.cell_type)))
        self._settled = None
        self.reset()

    def contrast(self, objects: list) -> np.ndarray:
        """Contrast per column for eye2d objects (Disks, Edges), seen through the facet blur."""
        from .eye2d import render

        return render(self.directions, np.ones(len(self.directions), bool), objects, self.sigma)

    def _advance(self, contrast) -> None:
        x = np.zeros(len(self.cell_type))
        c = BACKGROUND if contrast is None else BACKGROUND * (1 + np.asarray(contrast, float)[self.cell_col[self._input]])
        x[self._input] = c
        drive = matvec(self.W, np.maximum(self.V, 0))
        self.V = self.V + self.dt / self.tau * (-self.V + self.bias + drive + x)

    def reset(self, seconds: float = 10.0) -> None:
        """Settle on a blank grey field (computed once, restored after); release changes are
        measured from this state."""
        if self._settled is None or self._settled[0] != seconds:
            self.V = self.bias.copy()
            for _ in range(int(round(seconds / self.dt))):
                self._advance(None)
            self._settled = (seconds, self.V.copy())
        self.V = self._settled[1].copy()
        self.rest = self.readout @ np.maximum(self.V, 0)

    def step(self, contrast) -> np.ndarray:
        """Advance one step on the contrast per column (self.contrast; None for grey); returns the
        release change of each neuron in self.neurons, per 20 ms, for FlyBrain.set_graded."""
        self._advance(contrast)
        return (self.gain * (self.readout @ np.maximum(self.V, 0) - self.rest)).astype(np.float32)
