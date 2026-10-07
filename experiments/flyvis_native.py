"""Validating brainfly.optic.FlyvisNative: flyvis's own network, tiled onto the male fly's eye.

flyvis_port.py found that porting flyvis's parameters onto MaleCNS's wiring moves its operating
point. FlyvisNative keeps flyvis as its authors fitted and validated it: one cell of each type per
column, wired by flyvis's spatial filters, but laid on the male eye's real column lattice so each
column looks where MaleCNS's does. Three checks, in order:
  1. ORIENTATION, from anatomy alone. For T4a-d and T5a-d, the vector from the centroid of their
     Mi1 (T4) or Tm1 (T5) inputs to the centroid of each other column-assigned input type (Mi4,
     Mi9, C3; Tm9, Tm2, Tm4), in both connectomes. The hex-lattice symmetry (6 rotations x
     reflection) that best maps flyvis's vectors onto MaleCNS's, per side. brainfly.optic.to_mcns
     must be the winner on both sides.
  2. EXACT. Tiled onto flyvis's own 721-column lattice, the tiler must rebuild flyvis's network (same
     cells, synapses and weights) and its dynamics must reproduce flyvis's simulation of a flash.
  3. DIRECTION SELECTIVITY, on the male eye (the test of 1, as responses weren't used to orient).
     ON edges (T4) and OFF edges (T5) sweeping front-to-back, back-to-front, up and down across each
     eye at 40 deg/s, 2 ms steps; each subtype's peak response, preferred direction and direction
     selectivity index. Expected (Maisak et al. 2013), in both eyes: a front-to-back,
     b back-to-front, c up, d down.
Also reported: how many MaleCNS neurons of flyvis types FlyvisNative drives.

    python experiments/flyvis_native.py            (writes experiments/flyvis_native.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.data import DATA
from brainfly.eye2d import Edge
from brainfly.optic import (GRADED as OPTIC, MODEL, R16, FlyvisNative, _network, flyvis_filters, flyvis_type,
                            plane, tile, to_mcns)
from brainfly.shiu import counts, mcns_types

OUT = Path(__file__).with_name("flyvis_native.json")
PLAN = {"T4": ("Mi1", ["Mi4", "Mi9", "C3"]), "T5": ("Tm1", ["Tm9", "Tm2", "Tm4"])}
EXPECTED = {"a": "front-to-back", "b": "back-to-front", "c": "upward", "d": "downward"}
OPPOSITE = {"front-to-back": "back-to-front", "back-to-front": "front-to-back", "upward": "downward", "downward": "upward"}


def symmetries():
    """The 12 symmetries of the hex lattice, as maps of the plane."""
    for reflect in (False, True):
        for k in range(6):
            a = np.radians(60 * k)
            R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
            yield (60 * k, reflect), R @ (np.diag([1.0, -1.0]) if reflect else np.eye(2))


def orientation(net) -> dict:
    c = net.connectome
    st, tt = np.asarray(c.edges.source_type[:]).astype(str), np.asarray(c.edges.target_type[:]).astype(str)
    su, sv = np.asarray(c.edges.source_u[:]), np.asarray(c.edges.source_v[:])
    tu, tv = np.asarray(c.edges.target_u[:]), np.asarray(c.edges.target_v[:])
    n = np.asarray(c.edges.n_syn[:])
    central = (tu == 0) & (tv == 0)
    fplane = lambda u, v: np.stack([u + v / 2, np.sqrt(3) / 2 * v], -1)     # flyvis axial -> plane
    fv = {}
    for fam, (ref, others) in PLAN.items():
        for sub in "abcd":
            t = f"{fam}{sub}"
            cen = {}
            for s in [ref] + others:
                m = central & (tt == t) & (st == s)
                cen[s] = fplane(su[m], sv[m]).T @ n[m] / n[m].sum()
            for s in others:
                fv[(t, s)] = cen[s] - cen[ref]
    import pyarrow.feather as feather
    meta = np.load(DATA / "brain.npz")
    ann = feather.read_table(DATA / "raw" / "body-annotations-male-cns-v1.0-minconf-0.5.feather",
                             columns=["bodyId", "assignedOlHex1", "assignedOlHex2"]).to_pandas()
    ann = ann.drop_duplicates("bodyId").set_index("bodyId").reindex(meta["ids"])
    h = ann[["assignedOlHex1", "assignedOlHex2"]].to_numpy(float)
    has = ~np.isnan(h[:, 0])
    xy = np.full((len(h), 2), np.nan)
    xy[has] = plane(h[has, 0], h[has, 1])
    side, mt = meta["side"].astype(str), mcns_types(DATA)
    C = abs(counts(DATA)).tocsr()
    mc = {}
    for sd in "LR":
        for fam, (ref, others) in PLAN.items():
            for sub in "abcd":
                t = f"{fam}{sub}"
                acc = {s: [] for s in others}
                for i in np.flatnonzero((mt == t) & (side == sd)):
                    pre, w = C[i].indices, C[i].data
                    cen = {}
                    for s in [ref] + others:
                        m = (mt[pre] == s) & has[pre]
                        cen[s] = (xy[pre[m]].T @ w[m] / w[m].sum(), w[m].sum()) if m.any() else None
                    if cen[ref] is None:
                        continue
                    for s in others:
                        if cen[s] is not None:
                            acc[s].append((cen[s][0] - cen[ref][0], min(cen[s][1], cen[ref][1])))
                for s in others:
                    if acc[s]:
                        v = np.array([a for a, _ in acc[s]])
                        w = np.array([b for _, b in acc[s]])
                        mc[(sd, t, s)] = v.T @ w / w.sum()
    out = {}
    unit = {"u": np.array([1.0, 0.0]), "v": np.array([0.5, np.sqrt(3) / 2])}
    for sd in "LR":
        scores = sorted((float(sum(np.sum((T @ fv[k] - mc[(sd,) + k]) ** 2) for k in fv if (sd,) + k in mc)), key)
                        for key, T in symmetries())
        T = dict(symmetries())[scores[0][1]]
        # the winner as a map of lattice offsets: where do flyvis's unit offsets land in MaleCNS columns?
        land = {name: T @ e for name, e in unit.items()}
        to_col = lambda p: (int(round(p[0] - p[1] / np.sqrt(3))), int(round(-2 * p[1] / np.sqrt(3))))  # plane -> (hex1, hex2)
        out[sd] = {"best": {"rotation_deg": scores[0][1][0], "reflect": scores[0][1][1], "error": round(scores[0][0], 2)},
                   "runner_up_error": round(scores[1][0], 2),
                   "flyvis (1,0) ->": to_col(land["u"]), "flyvis (0,1) ->": to_col(land["v"]),
                   "matches_to_mcns": to_col(land["u"]) == to_mcns(1, 0) and to_col(land["v"]) == to_mcns(0, 1)}
    return out


def exact(net, f) -> dict:
    import torch
    c = net.connectome
    ty = np.asarray(c.nodes.type[:]).astype(str)
    u, v = np.asarray(c.nodes.u[:]), np.asarray(c.nodes.v[:])
    R = f["radius"]
    uv = np.array([(a, b) for a in range(-R, R + 1) for b in range(-R, R + 1) if max(abs(a), abs(b), abs(a + b)) <= R])
    ct, cc, W = tile(np.stack(to_mcns(uv[:, 0], uv[:, 1]), 1), np.zeros(2, int), f)
    mine = {(t, int(uv[k, 0]), int(uv[k, 1])): i for i, (t, k) in enumerate(zip(ct, cc))}
    order = np.array([mine[(t, int(a), int(b))] for t, a, b in zip(ty, u, v)])
    src, tgt = np.asarray(c.edges.source_index[:]), np.asarray(c.edges.target_index[:])
    p = {k: net.edge_params[k] for k in ("sign", "syn_count", "syn_strength")}
    wf = np.prod([p[k].semantic_values.detach().numpy()[np.asarray(p[k].indices)] for k in p], axis=0)
    dw = float(np.abs(np.asarray(W[order[tgt], order[src]]).ravel() - wf).max())
    dt, pre, stim = 0.002, 100, 50
    with torch.no_grad():
        state = net.steady_state(1.0, dt, 1)
        movie = torch.full((1, pre + stim, 1, len(uv)), 0.5)
        movie[:, pre:] = 0.1
        ref = net.simulate(movie, dt, initial_state=state).cpu().numpy()[0]
    tau = np.array([max(f["tau"][t], dt) for t in ct])
    bias = np.array([f["bias"][t] for t in ct])
    inp = np.flatnonzero(np.isin(ct, R16 + ["R7", "R8"]))
    V = state.nodes.activity.detach().numpy().ravel()[np.argsort(order)]
    dv = 0.0
    for k in range(pre + stim):
        x = np.zeros(len(ct))
        x[inp] = float(movie[0, k, 0, 0])
        V = V + dt / tau * (-V + bias + W @ np.maximum(V, 0) + x)
        dv = max(dv, float(np.abs(V[order] - ref[k]).max()))
    return {"cells": [len(ct), len(ty)], "synapses": [int(W.nnz), len(src)], "max_weight_difference": dw,
            "max_voltage_difference": dv, "max_voltage": float(np.abs(ref).max())}


def direction_selectivity(ol: FlyvisNative, speed: float = 40.0) -> dict:
    moves = {"R": {"front-to-back": ("azimuth", 20, -180, +1), "back-to-front": ("azimuth", -180, 20, -1),
                   "upward": ("elevation", -90, 90, -1), "downward": ("elevation", 90, -90, +1)},
             "L": {"front-to-back": ("azimuth", -20, 180, -1), "back-to-front": ("azimuth", 180, -20, +1),
                   "upward": ("elevation", -90, 90, -1), "downward": ("elevation", 90, -90, +1)}}
    out = {}
    for sd, mv in moves.items():
        peak = {}
        for polarity in (+1.0, -1.0):
            for name, (axis, a, b, behind) in mv.items():
                ol.reset()
                rest = np.maximum(ol.V, 0)
                best = np.zeros(len(ol.V))
                for s in range(int((abs(b - a) / speed + 0.5) / ol.dt)):
                    ol._advance(ol.contrast([Edge(axis, a + np.sign(b - a) * speed * s * ol.dt, behind, polarity)]))
                    best = np.maximum(best, np.maximum(ol.V, 0) - rest)
                peak[(polarity, name)] = best
        for fam, polarity in (("T4", +1.0), ("T5", -1.0)):
            for sub in "abcd":
                m = (ol.cell_type == f"{fam}{sub}") & (ol.cell_side == sd)
                r = {k: float(peak[(polarity, k)][m].mean()) for k in mv}
                pref = max(r, key=r.get)
                out[f"{sd} {fam}{sub}"] = {"responses": {k: round(x, 3) for k, x in r.items()}, "preferred": pref,
                                           "dsi": round((r[pref] - r[OPPOSITE[pref]]) / (r[pref] + r[OPPOSITE[pref]] + 1e-9), 3),
                                           "expected": EXPECTED[sub], "correct": pref == EXPECTED[sub]}
    ol.reset()
    return out


def main() -> None:
    f = flyvis_filters(MODEL)
    net = _network(MODEL, DATA)
    results = {"description": __doc__}
    results["orientation"] = orientation(net)
    print("orientation:", json.dumps(results["orientation"]), flush=True)
    results["exact"] = exact(net, f)
    print("exact:", results["exact"], flush=True)
    brain = FlyBrain(batch=1, graded=OPTIC, dt=0.002, refractory=0.004)
    ol = FlyvisNative(brain, model=MODEL)
    ft = flyvis_type(brain, mcns_types(DATA), set(f["tau"]) | {"R1-6"})
    results["coverage"] = {"cells": len(ol.cell_type), "synapses": int(ol.W.nnz), "columns": len(ol.column_keys),
                           "malecns_neurons_of_flyvis_types": int((ft != "").sum()), "driven": len(ol.neurons)}
    print("coverage:", results["coverage"], flush=True)
    results["direction_selectivity"] = ds = direction_selectivity(ol)
    print("direction selectivity:", {k: (v["preferred"], v["dsi"], "OK" if v["correct"] else "x") for k, v in ds.items()}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
