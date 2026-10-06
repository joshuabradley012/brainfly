"""Exploratory, not pre-registered: rung3_001_pilot.py again, with stand-ins that match rung 3's measures more closely.

rung3_001_pilot.py fine-tuned flyvis's model 001 to 30 of 32 polarities and 16 of 16 directions, both thinly: flyvis's
index put Tm2 at -0.007 and R3 still wrong, and T5a's direction selectivity in the eye was 0.02. Its polarity stand-in
disagreed with flyvis's index on R3. This pilot changes three things:
  polarity   flyvis's own index: its Flashes movie (dt 0.005 s, radius 6, light and dark, each 1 s), starting from
             the steady state after 1 s of grey and 0.25 s of the movie's grey lead-in, the central cells' activity
             from one frame before the flash to the first frame after it, shifted by its minimum, (peak light - peak
             dark) / (sum). On models 001 and rung3_001_pilot.py's result this matches flyvis's values for R3, R6, L2 and
             Tm2 to the third decimal (with the full 1 s lead-in; shorter ones move L2 by about 0.01). Penalty relu(0.05 -
             known sign x index) for the 32 known types, weight 1000.
  direction  flyvis's MovingEdge as before (speed 19), plus OFF edges at speed 9.7 for the T5s, whose margin rises
             from 0.2 to 0.35 (T4 keeps 0.2).
  T2         from the polarity simulation, against a grey-only run from the same state (as before).
Everything else as rung3_001_pilot.py: model 001, flyvis's flow task, Adam on network and decoder at 1e-5, the penalty
every fifth iteration at five times its weight, for 2,000 iterations, seed 0. Saved as flow/9012/000 and measured
as rung 3 measures it (polarity, direction in the eye, T2, validation error).

Ran: worse on rung 3's own measures. Polarity 30 of 32 (R3 now right at +0.05, but Tm2 back to wrong at +0.025, L2
still wrong), directions 14 of 16 in the eye: T5a wrong in both eyes, preferring back-to-front (0.77 against 0.65 for
front-to-back), although on flyvis's lattice it now strongly prefers front-to-back (0.48 against 0.23). The validation
error rose to 5.62 (model 001: 5.20). Afterwards (not pre-registered): T5a's preference in the eye is not a rim effect.
86% of its interior cells (4 or more columns from the rim) prefer back-to-front. It isn't the edge speed either: on
the lattice at the eye test's 40 deg/s (6.9 columns/s) the central T5a still prefers front-to-back. A full-width sweep
averaged over every T5a cell, as the eye test averages, doesn't reproduce the eye's verdicts for T5a, T5c or T5d in
models 001, rung3_001_pilot.py's or this one. The eye model (FlyvisNative tiles flyvis's filters onto the male eye's
irregular columns) treats weakly tuned cells differently from flyvis's regular lattice. No lattice stand-in tried
predicts T5a there.

    python experiments/rung3_001_pilot2.py      (writes experiments/rung3_001_pilot2.json; the model to flyvis's results)
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
START, NAME, ENSEMBLE = "flow/0000/001", "flow/9012/000", "flow/9012"
LR, ITERS, SEED, EVERY = 1e-5, 2_000, 0, 5
W_POL, W_DIR, W_T2 = 1000.0, 300.0, 300.0
FLASH_DT, LEAD = 0.005, 0.25
SPEEDS, T5_MARGIN = (19, 9.7), 0.35
DT, T_PRE, T_FLASH = 0.01, 0.2, 1.0
ANGLES = {"a": 180, "b": 0, "c": 90, "d": 240}           # nearest to model 001's T4 preferences on flyvis's lattice


def edges() -> np.ndarray:
    """flyvis's MovingEdge at the four angles: (12, frames, 1, hexals), rows OFF then ON at speed 19, then OFF at
    9.7. flyvis pads the faster edges with NaN to the slower ones' length; those frames repeat the last real one.
    Cached, since flyvis builds them slowly."""
    cache = HERE / "edges.npz"
    if cache.exists():
        return np.load(cache)["x"]
    from flyvis.datasets.moving_bar import MovingEdge
    angles = sorted(set(ANGLES.values()))
    me = MovingEdge(intensities=[0, 1], speeds=list(SPEEDS), angles=angles, dt=DT, t_pre=T_PRE, t_post=T_PRE, device="cpu")
    rows = me.arg_df.reset_index(drop=True)
    order = [int(rows[(rows.speed == v) & (rows.intensity == i) & (rows.angle == a)].index[0])
             for v, i in ((SPEEDS[0], 0), (SPEEDS[0], 1), (SPEEDS[1], 0)) for a in angles]
    seqs = []
    for i in order:
        q = me[i].numpy()
        ok = ~np.isnan(q).any(axis=tuple(range(1, q.ndim)))
        q = q.copy()
        q[~ok] = q[np.flatnonzero(ok)[-1]]
        seqs.append(q)
    x = np.stack(seqs)[:, :, None].astype(np.float32)
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
        from flyvis.datasets.flashes import Flashes
        fl = Flashes(dynamic_range=[0, 1], t_stim=1, t_pre=1.0, dt=FLASH_DT, radius=[6], alternations=(0, 1, 0))
        onset = int(round(1.0 / FLASH_DT))
        start = onset - int(round(LEAD / FLASH_DT))
        f = np.stack([np.asarray(fl[i]) for i in (1, 0)])[:, start:onset + int(round(1.0 / FLASH_DT)) + 1, None]   # light, dark
        self.flashes = torch.from_numpy(np.concatenate([f, np.full_like(f[:1], 0.5)]).astype(np.float32)).to(vt.DEVICE)
        self.window = onset - start - 1                   # flyvis's index: one frame before onset to t_stim
        self.edges = torch.from_numpy(edges()).to(vt.DEVICE)
        self.angles = sorted(set(ANGLES.values()))
        self.pre = int(round(T_PRE / DT))
        del flyvis

    def _run(self, net, x, dt=DT, t_steady=0.5):
        with vt.on(vt.DEVICE):
            with torch.no_grad():
                state = net.steady_state(t_pre=t_steady, dt=dt, batch_size=x.shape[0], value=0.5)
            net.stimulus.zero(x.shape[0], x.shape[1])
            net.stimulus.add_input(x)
            return net(net.stimulus(), dt, state=state)[:, :, self.central]               # (batch, frames, types)

    def flash_measures(self, net):
        a = self._run(net, self.flashes, dt=FLASH_DT, t_steady=1.0)
        w = a[:2, self.window:]                                                           # flyvis's flash response index
        shift = w.amin(dim=(0, 1)).abs()
        on_p, off_p = w[0].amax(0) + shift, w[1].amax(0) + shift
        index = (on_p - off_p) / (on_p + off_p + 1e-16)
        r = a[:2, self.window + 1:] - a[2:, self.window + 1:]                             # T2, relative to the grey-only run
        t2 = self.types.index("T2")
        return index[self.pol_idx], r[0, :, t2].max(), r[1, :, t2].max()

    def edge_measures(self, net):
        a = self._run(net, self.edges)
        r = a.max(1).values - a[:, :self.pre].mean(1)                                     # (12, types)
        out, n = {}, len(self.angles)
        for fam, speed, row0 in (("T5", SPEEDS[0], 0), ("T4", SPEEDS[0], n), ("T5", SPEEDS[1], 2 * n)):
            for sub, e in ANGLES.items():
                j = self.types.index(f"{fam}{sub}")
                out[(f"{fam}{sub}", speed)] = {ang: r[row0 + k, j] for k, ang in enumerate(self.angles)}
        return out

    def penalty(self, net):
        index, on, off = self.flash_measures(net)
        pol = torch.relu(0.05 - self.pol_sign * index).sum()
        t2 = torch.relu(0.5 - on) + torch.relu(0.5 - off) + torch.relu(0.4 * torch.maximum(on, off) - torch.minimum(on, off))
        d = 0.0
        for (name, speed), resp in self.edge_measures(net).items():
            e, margin = ANGLES[name[-1]], T5_MARGIN if name.startswith("T5") else 0.2
            d = d + torch.relu(0.3 - resp[e])
            for ang, r_o in resp.items():
                if ang != e:
                    d = d + torch.relu(margin - (resp[e] - r_o) / (resp[e].abs() + r_o.abs() + 1e-2))
        return W_POL * pol + W_DIR * d + W_T2 * t2, {"polarity": float(pol), "direction": float(d), "t2": float(t2)}

    def report(self, net) -> dict:
        with torch.no_grad():
            index, on, off = self.flash_measures(net)
            em = self.edge_measures(net)
        wrong = [n for n, s, v in zip(self.pol_names, self.pol_sign.tolist(), index.tolist()) if s * v <= 0]
        dsi = {}
        for (name, speed), resp in em.items():
            e = ANGLES[name[-1]]
            best = max(resp, key=lambda a: float(resp[a]))
            dsi[f"{name} at {speed}"] = {"expected_is_max": best == e, "r_expected": round(float(resp[e]), 3),
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
            note={"experiment": "experiments/rung3_001_pilot2.py", "lr": LR, "iterations": ITERS, "seed": SEED,
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
