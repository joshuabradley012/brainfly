"""Exploratory, not pre-registered: fine-tuning flyvis's model 001 with rung 3's direction test itself in the loss.

rung3_001_pilot.py and rung3_001_pilot2.py protected T4/T5 directions on flyvis's own lattice, and T5a's direction in
the eye (FlyvisNative, the model tiled onto the male eye, where rung 3 measures it) came out right by 0.02 in one and
wrong in the other. No lattice stand-in tried predicts T5a in the eye. brainfly.eyetorch now runs the eye's network in
PyTorch with the flyvis model's own parameters (matching FlyvisNative within 0.0004 [corrected afterwards: no saved result
shows that; tests/test_eyetorch.py checks T5 responses agree within 0.002]), so the direction test can be trained on
directly.
Model: flow/0000/001, fine-tuned with brainfly.vistrain.fine_tune (flyvis's flow task on augmented Sintel batches of 4,
Adam on network and decoder, learning rate 1e-5, seed 0) for 1,500 iterations. Every fourth iteration adds, at four
times its weight:
  direction  flyvis_native.direction_selectivity's edges (40 deg/s, ON for T4, OFF for T5) across the right eye at
             dt 0.02 s (where the test gives the same verdicts as at its 0.002), through brainfly.eyetorch. For each
             T4/T5 subtype, the mean over its cells of each sweep's peak change of relu(V) from grey's rest, r_e for
             its expected direction against each other direction r_o: relu(m - (r_e - r_o) / (r_e + r_o)), m 0.1 for
             T5 and 0.2 for T4. Weight 300.
  polarity   flyvis's flash response index exactly as rung3_001_pilot2.py computes it (Flashes at dt 0.005 s after a
             0.25 s lead-in), relu(0.05 - known sign x index) for the 32 known types except L2, whose sign is far off
             (+0.26) and whose push in pilot 2 came with the validation error rising to 5.62. Rung 3 asks 30: R3 and
             Tm2, near zero in model 001, would make 31. Weight 500.
  T2         from the same flashes against a grey-only run: relu(0.5 - on) + relu(0.5 - off) +
             relu(0.4 max(on, off) - min(on, off)). Weight 300.
Logged every 100 iterations: the losses, the eye's direction verdict (right eye, dt 0.02), the polarity count by the
index and T2. Saved as flow/9013/000; measured after training as rung 3 measures it (polarity, direction in both
eyes at dt 0.002, T2) with flyvis's validation error (model 001: 5.20).

Ran: it works on rung 3's own measures. 31 of 32 polarities, with flyvis's index putting R3 at +0.054 and Tm2 at -0.043
(only L2, untargeted, still wrong). 16 of 16 directions in both eyes at dt 0.002: T5a's DSI is 0.30-0.31 (pilot 1's
0.02), and in the eye it answers front-to-back edges with 0.092 against at most 0.049 for the others, though that is
a sixth of the other T5s' responses (0.45-1.02). T2 still answers both flashes (1.60 and 3.09), and the validation
error is 5.24 (model 001: 5.20). Looming wasn't measured. One seed.

    python experiments/rung3_001_pilot3.py      (writes experiments/rung3_001_pilot3.json; the model to flyvis's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch

from brainfly import vistrain as vt
from brainfly.eyetorch import EyeTorch
from flyvis_native import EXPECTED, OPPOSITE

OUT = Path(__file__).with_suffix(".json")
START, NAME, ENSEMBLE = "flow/0000/001", "flow/9013/000", "flow/9013"
LR, ITERS, SEED, EVERY = 1e-5, 1_500, 0, 4
W_DIR, W_POL, W_T2 = 300.0, 500.0, 300.0
MARGIN = {"T5": 0.1, "T4": 0.2}
FLASH_DT, LEAD = 0.005, 0.25
UNTARGETED = ("L2",)


class Measures:
    def __init__(self, net):
        from flyvis.datasets.flashes import Flashes
        from flyvis.utils.groundtruth_utils import polarity
        known = {k: v for k, v in polarity.items() if v != 0}
        self.types = [c.decode() if isinstance(c, bytes) else str(c) for c in net.node_params["bias"].keys]
        self.pol_names = list(known)
        self.pol_idx = torch.tensor([self.types.index(k) for k in known], device=vt.DEVICE)
        self.pol_sign = torch.tensor([float(v) for v in known.values()], device=vt.DEVICE)
        self.pol_on = torch.tensor([k not in UNTARGETED for k in known], device=vt.DEVICE)
        self.central = torch.as_tensor(np.asarray(net.connectome.central_cells_index[:]), device=vt.DEVICE)
        fl = Flashes(dynamic_range=[0, 1], t_stim=1, t_pre=1.0, dt=FLASH_DT, radius=[6], alternations=(0, 1, 0))
        onset = int(round(1.0 / FLASH_DT))
        start = onset - int(round(LEAD / FLASH_DT))
        f = np.stack([np.asarray(fl[i]) for i in (1, 0)])[:, start:onset + int(round(1.0 / FLASH_DT)) + 1, None]   # light, dark
        self.flashes = torch.from_numpy(np.concatenate([f, np.full_like(f[:1], 0.5)]).astype(np.float32)).to(vt.DEVICE)
        self.window = onset - start - 1
        self.eye = EyeTorch(net, "R", dt=0.02)
        self.sweeps = {+1.0: self.eye.edge_sweeps(+1.0), -1.0: self.eye.edge_sweeps(-1.0)}
        self.names = self.sweeps[-1.0][2]

    def flash(self, net):
        with vt.on(vt.DEVICE):
            with torch.no_grad():
                state = net.steady_state(t_pre=1.0, dt=FLASH_DT, batch_size=3, value=0.5)
            net.stimulus.zero(3, self.flashes.shape[1])
            net.stimulus.add_input(self.flashes)
            a = net(net.stimulus(), FLASH_DT, state=state)[:, :, self.central]
        w = a[:2, self.window:]
        shift = w.amin(dim=(0, 1)).abs()
        on_p, off_p = w[0].amax(0) + shift, w[1].amax(0) + shift
        index = ((on_p - off_p) / (on_p + off_p + 1e-16))[self.pol_idx]
        r = a[:2, self.window + 1:] - a[2:, self.window + 1:]
        t2 = self.types.index("T2")
        return index, r[0, :, t2].max(), r[1, :, t2].max()

    def eye_means(self, net, rest):
        out = {}
        for fam, pol in (("T4", +1.0), ("T5", -1.0)):
            peak = self.eye.peaks(net, self.sweeps[pol], rest)
            for sub in "abcd":
                out[f"{fam}{sub}"] = dict(zip(self.names, self.eye.type_means(peak, f"{fam}{sub}")))
        return out

    def penalty(self, net):
        rest = self.eye.settle(net, seconds=2.0)
        d = 0.0
        for name, r in self.eye_means(net, rest).items():
            e, m = EXPECTED[name[-1]], MARGIN[name[:2]]
            for o in self.names:
                if o != e:
                    d = d + torch.relu(m - (r[e] - r[o]) / (r[e] + r[o] + 1e-6))
        index, on, off = self.flash(net)
        pol = (torch.relu(0.05 - self.pol_sign * index) * self.pol_on).sum()
        t2 = torch.relu(0.5 - on) + torch.relu(0.5 - off) + torch.relu(0.4 * torch.maximum(on, off) - torch.minimum(on, off))
        return W_DIR * d + W_POL * pol + W_T2 * t2, {"direction": float(d), "polarity": float(pol), "t2": float(t2)}

    def report(self, net) -> dict:
        with torch.no_grad():
            rest = self.eye.settle(net, seconds=2.0)
            means = self.eye_means(net, rest)
            index, on, off = self.flash(net)
        eye = {}
        for name, r in means.items():
            e = EXPECTED[name[-1]]
            r = {k: float(v) for k, v in r.items()}
            best = max(r, key=r.get)
            eye[name] = {"correct": best == e, "dsi_expected": round((r[e] - r[OPPOSITE[e]]) / (r[e] + r[OPPOSITE[e]] + 1e-9), 3),
                         "r_expected": round(r[e], 3), "r_best_other": round(max(v for k, v in r.items() if k != e), 3)}
        wrong = [n for n, s, v in zip(self.pol_names, self.pol_sign.tolist(), index.tolist()) if s * v <= 0]
        return {"eye_correct": sum(v["correct"] for v in eye.values()), "eye": eye,
                "polarity_correct": len(self.pol_names) - len(wrong), "polarity_wrong": wrong,
                "polarity_index": {n: round(v, 3) for n, v in zip(self.pol_names, index.tolist()) if n in ("R3", "R6", "L2", "L3", "Tm2", "T5a")},
                "t2_on": round(float(on), 3), "t2_off": round(float(off), 3)}


def train(seed: int, name: str, out: dict, path: Path, experiment: str):
    """This pilot's fine-tune of model 001 with `seed`, saved as flyvis model `name`; the start, trace and end go into
    `out`, written to `path` as it goes. Returns the network, decoder and measures."""
    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    m = Measures(net)
    m.eye.settle(net)                                    # 10 s from rest, as FlyvisNative; later calls warm-start
    out["start"] = {**m.report(net), "val_epe": round(vt.validation_epe(net, dec, task), 4)}
    print("start", json.dumps(out["start"] | {"eye": {k: v["correct"] for k, v in out["start"]["eye"].items()}}), flush=True)
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
        print(json.dumps({**row, "parts": calls["last"]} | {k: rep[k] for k in ("eye_correct", "polarity_correct", "polarity_wrong", "t2_on", "t2_off")}
                         | {"T5a": rep["eye"]["T5a"]}), flush=True)
        path.write_text(json.dumps({**out, "trace": trace}, indent=1))

    vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, seed=seed, every=100, log=log)
    epe = vt.validation_epe(net, dec, task)
    vt.save(net, dec, name, source=START, val_epe=epe,
            note={"experiment": experiment, "lr": LR, "iterations": ITERS, "seed": seed,
                  "weights": {"direction": W_DIR, "polarity": W_POL, "t2": W_T2}, "every": EVERY})
    out.update({"trace": trace, "end": {**m.report(net), "val_epe": round(epe, 4)}})
    print("end", json.dumps(out["end"] | {"eye": {k: (v["correct"], v["dsi_expected"]) for k, v in out["end"]["eye"].items()}}), flush=True)
    path.write_text(json.dumps(out, indent=1))
    return net, dec, m


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__}
    train(SEED, NAME, out, OUT, "experiments/rung3_001_pilot3.py")

    from rung3_t2 import directions, screen_t2
    from rung3_verdict import polarity
    out["rung3"] = {"t2": screen_t2(ENSEMBLE, NAME)}
    pol = polarity([NAME], ensemble=ENSEMBLE)[NAME]
    out["rung3"]["polarity"] = {"correct": pol["correct"], "of": pol["of"], "wrong": pol["wrong"],
                                "fri": {k: v["fri"] for k, v in pol["types"].items() if k in ("R3", "R6", "L2", "L3", "Tm2", "T5a")}}
    print("rung 3 polarity:", pol["correct"], "of", pol["of"], pol["wrong"], json.dumps(out["rung3"]["t2"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))
    ds = directions(NAME)
    out["rung3"]["direction"] = {"correct": int(sum(v["correct"] for v in ds.values())),
                                 "wrong": [k for k, v in ds.items() if not v["correct"]],
                                 "dsi": {k: v["dsi"] for k, v in ds.items()},
                                 "responses": {k: v["responses"] for k, v in ds.items() if "T5" in k}}
    out["seconds"] = round(time.perf_counter() - t0)
    print("rung 3 direction:", out["rung3"]["direction"]["correct"], "of 16", out["rung3"]["direction"]["wrong"],
          json.dumps(out["rung3"]["direction"]["dsi"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
