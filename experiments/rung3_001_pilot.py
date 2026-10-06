"""Exploratory, not pre-registered: can fine-tuning flyvis's model 001 fix T5a's direction and a contrast polarity
while keeping the T2 that answers darkening?

rung3_verdict.py: model 001, whose T2 answers light decrements as a real T2 does (Keles et al. 2020) and whose looming
reaches LC4, misses rung 3 on two counts. It gets 29 of 32 polarities (R3, L2 and Tm2 wrong; 30 needed), and T5a,
which should prefer front-to-back motion, has no direction preference to speak of (DSI 0.07 in the eye), so it misses
16 of 16. The earlier fine-tunes of models 006 and 000 (rung3_t2.py, rung3_t2_local.py) protected nothing but T2 and
broke directions or polarities. This one starts from 001 and protects what rung 3 measures.
Model: flow/0000/001, fine-tuned with brainfly.vistrain.fine_tune (flyvis's flow task on augmented Sintel batches of 4,
Adam on network and decoder, learning rate 1e-5, seed 0) for 1,500 iterations. Every fourth iteration adds, at four
times its weight, a penalty from three differentiable stand-ins for rung 3's measures, each simulated from grey's
steady state at dt 0.01 s:
  polarity   flashes of radius 6 (flyvis's Flashes: 1 s, light and dark from grey) after 0.2 s of grey, each
             response taken relative to a grey-only run from the same state. For each of flyvis's 32 known types, the
             central cell's peak during the light flash minus its peak during the dark one, over their sum of sizes:
             the sign of flyvis's flash response index. Penalty relu(0.05 - known sign x index), weight 300.
  direction  flyvis's MovingEdge (speed 19, 0.2 s of grey before and after) at the four angles nearest the
             directions model 001's T4s prefer on flyvis's lattice (T4a 179 deg, T4b 351, T4c 77, T4d 248): a 180, b 0,
             c 90, d 240. ON edges for T4, OFF edges for T5. For each T4/T5 subtype, the central cell's peak response
             (relative to its first 0.2 s) to its expected angle against each of the other three:
             relu(0.2 - (r_e - r_o) / (r_e + r_o)), plus relu(0.3 - r_e) so that it answers at all. Weight 300.
  T2         the same flashes: T2's peaks to light (on) and dark (off). relu(0.5 - on) + relu(0.5 - off) +
             relu(0.4 max(on, off) - min(on, off)), weight 300 (model 001: on 1.28, off 2.91). Unlike flyvis_t2_pilot5's penalty, the grey-only run
             cancels any drift of T2's own (t2_penalty_check.py).
Logged every 100 iterations: the losses and the stand-ins. The result is saved as flyvis model flow/9011/000.
Measured after training, as rung 3 measures them: polarity (rung3_verdict.polarity), direction selectivity with the
model tiled onto the male eye (flyvis_native.direction_selectivity, 16 of 16 needed), T2 as flyvis_screen.py measures
it, and flyvis's validation error (model 001: 5.20). Looming is left for a pre-registered test.
Ran: closer, not robust. On rung 3's own measures it gets 30 of 32 polarities (Tm2 fixed; R3 and L2 still wrong) and
16 of 16 directions in the eye, T5a now preferring front-to-back. T2 still answers both flashes (0.99 and 2.39), and
the validation error rose from 5.20 to 5.31. But both passes are thin: flyvis's index puts Tm2 at -0.007, and T5a's
direction selectivity in the eye is 0.02. The polarity stand-in disagreed with flyvis's index on R3 (+0.10 against
-0.03). flyvis compares the raw peaks, the frame before the flash included, at dt 0.005 s, where this subtracted a
grey run at 0.01 s. That matters for cells that barely answer.

    python experiments/rung3_001_pilot.py      (writes experiments/rung3_001_pilot.json; the model to flyvis's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch

from brainfly import vistrain as vt

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
START, NAME, ENSEMBLE = "flow/0000/001", "flow/9011/000", "flow/9011"
LR, ITERS, SEED, EVERY = 1e-5, 1_500, 0, 4
W_POL, W_DIR, W_T2 = 300.0, 300.0, 300.0
DT, T_PRE, T_FLASH = 0.01, 0.2, 1.0
ANGLES = {"a": 180, "b": 0, "c": 90, "d": 240}           # nearest to model 001's T4 preferences on flyvis's lattice


def edges() -> np.ndarray:
    """flyvis's MovingEdge at the four angles, OFF then ON: (8, frames, 1, hexals), rows (intensity, angle) in
    the order [(0, 0), (0, 90), (0, 180), (0, 240), (1, 0), ...]. Cached, since flyvis builds them slowly."""
    cache = HERE / "edges.npz"
    if cache.exists():
        return np.load(cache)["x"]
    from flyvis.datasets.moving_bar import MovingEdge
    angles = sorted(set(ANGLES.values()))
    me = MovingEdge(intensities=[0, 1], speeds=[19], angles=angles, dt=DT, t_pre=T_PRE, t_post=T_PRE, device="cpu")
    rows = me.arg_df.reset_index(drop=True)
    order = [int(rows[(rows.intensity == i) & (rows.angle == a)].index[0]) for i in (0, 1) for a in angles]
    x = np.stack([me[i].numpy() for i in order])[:, :, None].astype(np.float32)
    HERE.mkdir(exist_ok=True)
    np.savez_compressed(cache, x=x, angles=angles)
    return x


class Stand_ins:
    """The three penalties' measures on one network, with gradients."""

    def __init__(self, net):
        import flyvis
        from flyvis.utils.groundtruth_utils import polarity
        known = {k: v for k, v in polarity.items() if v != 0}
        types = [c.decode() if isinstance(c, bytes) else str(c) for c in net.node_params["bias"].keys]
        self.pol_idx = torch.tensor([types.index(k) for k in known], device=vt.DEVICE)
        self.pol_sign = torch.tensor([float(v) for v in known.values()], device=vt.DEVICE)
        self.pol_names = list(known)
        self.central = torch.as_tensor(np.asarray(net.connectome.central_cells_index[:]), device=vt.DEVICE)
        self.types = types
        f = vt._flashes(DT, T_PRE, T_FLASH, 6)                                           # (2, frames, 1, hexals): light, dark
        self.flashes = torch.from_numpy(np.concatenate([f, np.full_like(f[:1], 0.5)])).to(vt.DEVICE)
        self.edges = torch.from_numpy(edges()).to(vt.DEVICE)
        self.angles = sorted(set(ANGLES.values()))
        self.pre = int(round(T_PRE / DT))
        del flyvis

    def _run(self, net, x):
        with vt.on(vt.DEVICE):
            with torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=DT, batch_size=x.shape[0], value=0.5)
            net.stimulus.zero(x.shape[0], x.shape[1])
            net.stimulus.add_input(x)
            return net(net.stimulus(), DT, state=state)[:, :, self.central]               # (batch, frames, types)

    def flash_measures(self, net):
        a = self._run(net, self.flashes)
        r = a[:2, self.pre:] - a[2:, self.pre:]                                           # relative to the grey-only run
        on, off = r[0].max(0).values, r[1].max(0).values                                  # (types,)
        index = (on - off) / (on.abs() + off.abs() + 1e-2)
        t2 = self.types.index("T2")
        return index[self.pol_idx], on[t2], off[t2]

    def edge_measures(self, net):
        a = self._run(net, self.edges)
        r = a.max(1).values - a[:, :self.pre].mean(1)                                     # (8, types)
        out = {}
        for fam, row0 in (("T5", 0), ("T4", len(self.angles))):
            for sub, e in ANGLES.items():
                j = self.types.index(f"{fam}{sub}")
                out[f"{fam}{sub}"] = {ang: r[row0 + k, j] for k, ang in enumerate(self.angles)}
        return out

    def penalty(self, net):
        index, on, off = self.flash_measures(net)
        pol = torch.relu(0.05 - self.pol_sign * index).sum()
        t2 = torch.relu(0.5 - on) + torch.relu(0.5 - off) + torch.relu(0.4 * torch.maximum(on, off) - torch.minimum(on, off))
        d = 0.0
        for name, resp in self.edge_measures(net).items():
            e = ANGLES[name[-1]]
            d = d + torch.relu(0.3 - resp[e])
            for ang, r_o in resp.items():
                if ang != e:
                    d = d + torch.relu(0.2 - (resp[e] - r_o) / (resp[e].abs() + r_o.abs() + 1e-2))
        return W_POL * pol + W_DIR * d + W_T2 * t2, {"polarity": float(pol), "direction": float(d), "t2": float(t2)}

    def report(self, net) -> dict:
        with torch.no_grad():
            index, on, off = self.flash_measures(net)
            em = self.edge_measures(net)
        wrong = [n for n, s, v in zip(self.pol_names, self.pol_sign.tolist(), index.tolist()) if s * v <= 0]
        dsi = {}
        for name, resp in em.items():
            e = ANGLES[name[-1]]
            best = max(resp, key=lambda a: float(resp[a]))
            dsi[name] = {"expected_is_max": best == e, "r_expected": round(float(resp[e]), 3),
                         "r_best_other": round(max(float(v) for a, v in resp.items() if a != e), 3)}
        return {"polarity_correct": len(self.pol_names) - len(wrong), "polarity_wrong": wrong,
                "polarity_index": {n: round(v, 3) for n, v in zip(self.pol_names, index.tolist()) if n in ("R3", "R6", "L2", "L3", "Tm2", "T5a")},
                "t2_on": round(float(on), 3), "t2_off": round(float(off), 3),
                "directions_correct": sum(v["expected_is_max"] for v in dsi.values()), "directions": dsi}


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    m = Stand_ins(net)
    out = {"question": __doc__, "start": {**m.report(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}}
    print("start", json.dumps(out["start"] | {"directions": None}), flush=True)
    calls = {"n": 0, "last": {}}

    def penalty(n):
        calls["n"] += 1
        if calls["n"] % EVERY:
            return torch.zeros((), device=vt.DEVICE)
        p, parts = m.penalty(n)
        calls["last"] = parts
        return EVERY * p

    trace = []

    def log(row):
        rep = m.report(net)
        net.train()
        trace.append({**row, "parts": calls["last"], **rep})
        print(json.dumps({**row, "parts": calls["last"]} | {k: rep[k] for k in ("polarity_correct", "polarity_wrong", "t2_on", "t2_off", "directions_correct")}), flush=True)
        OUT.write_text(json.dumps({**out, "trace": trace}, indent=1))

    vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, seed=SEED, every=100, log=log)
    epe = vt.validation_epe(net, dec, task)
    vt.save(net, dec, NAME, source=START, val_epe=epe,
            note={"experiment": "experiments/rung3_001_pilot.py", "lr": LR, "iterations": ITERS, "seed": SEED,
                  "weights": {"polarity": W_POL, "direction": W_DIR, "t2": W_T2}, "every": EVERY})
    out.update({"trace": trace, "end": {**m.report(net), "val_epe": round(epe, 4)}})
    print("end", json.dumps(out["end"] | {"directions": None}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))

    from rung3_t2 import directions, screen_t2
    from rung3_verdict import polarity
    out["rung3"] = {"t2": screen_t2(ENSEMBLE, NAME)}
    pol = polarity([NAME], ensemble=ENSEMBLE)[NAME]
    out["rung3"]["polarity"] = {"correct": pol["correct"], "of": pol["of"], "wrong": pol["wrong"]}
    print("rung 3 polarity:", pol["correct"], "of", pol["of"], pol["wrong"], json.dumps(out["rung3"]["t2"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))
    ds = directions(NAME)
    out["rung3"]["direction"] = {"correct": int(sum(v["correct"] for v in ds.values())),
                                 "wrong": [k for k, v in ds.items() if not v["correct"]],
                                 "dsi": {k: v["dsi"] for k, v in ds.items()}}
    out["seconds"] = round(time.perf_counter() - t0)
    print("rung 3 direction:", out["rung3"]["direction"]["correct"], "of 16", out["rung3"]["direction"]["wrong"], flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
