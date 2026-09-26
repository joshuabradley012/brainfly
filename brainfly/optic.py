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

FlyvisOpticLobe steps these neurons and hands FlyBrain their output: the change of relu(V) from
its value on a blank field, times `gain`, as graded release (FlyBrain.set_graded). The first use
extracts the parameters with flyvis (pip install flyvis; its pretrained models download to
$FLYVIS_ROOT_DIR) and caches them in <data>/flyvis_<model>.npz.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from scipy import sparse

from .data import ensure_data

MODEL = "flow/0000/000"
BACKGROUND = 0.5          # flyvis's grey
# A FlyBrain graded set covering every flyvis type: the retina and optic lobe, plus TmY14, which
# MaleCNS files under visual projection neurons.
GRADED = ["R1-6", "R7", "R8", "ol_intrinsic", "TmY14"]
R16 = ["R1", "R2", "R3", "R4", "R5", "R6"]
RENAME = {"Lai": "Am", "TmY9a": "TmY9", "TmY9b": "TmY9", "TmY9q": "TmY9", "TmY9q__perp": "TmY9"}


def flyvis_params(model: str = MODEL, data: Path | str | None = None) -> dict:
    """Per-type time constants and biases, and per type pair (sign, strength, total synapses a
    target neuron receives), with flyvis's R1-R6 merged into one type "R1-6"."""
    data = ensure_data(data)
    cache = data / f"flyvis_{model.replace('/', '_')}.npz"
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        return z["params"].item()
    os.environ.setdefault("FLYVIS_ROOT_DIR", str(data / "flyvis"))
    import flyvis
    from flyvis import NetworkView

    net = NetworkView(flyvis.results_dir / model).init_network(checkpoint="best")
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
        self.reset()

    def _x(self, contrast):
        x = np.zeros(len(self.neurons))
        if contrast is not None:
            x[self._input] = BACKGROUND * (1 + np.asarray(contrast, float)[self._visual_row])
        else:
            x[self._input] = BACKGROUND
        return x

    def reset(self, steps: int = 500) -> None:
        """Settle on a blank grey field; that state is what release changes are measured from."""
        self.V = self.bias.copy()
        x = self._x(None)
        for _ in range(steps):
            self._advance(x)
        self.rest = np.maximum(self.V, 0)

    def _advance(self, x) -> None:
        drive = self.W @ np.maximum(self.V, 0)
        self.V = self.V + self.dt / self.tau * (-self.V + self.bias + drive + x)

    def step(self, contrast) -> np.ndarray:
        """Advance one step on the light contrast per photoreceptor (CompoundEye.contrast); returns
        the release change of each neuron in self.neurons, to pass to FlyBrain.set_graded."""
        self._advance(self._x(contrast))
        return (self.gain * (np.maximum(self.V, 0) - self.rest)).astype(np.float32)
