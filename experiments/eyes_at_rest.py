"""Does the resting brain see? Looming through flyvis's eyes to the escape neuron, in rung 4's
resting brain (pre-registered).

eyepath_native_t2.py carried looming to LC4, LPLC2 and the giant fiber through flyvis's model 001
(whose T2 answers darkening), but into FlyBrain, the inherited model. The vision probes on HybridBrain
(optomotor_hybrid.py, optomotor_hybrid2.py) found no gain at which a visual signal passed through a
brain that is silent at rest without igniting it. rest_calibration2.py's brain now rests at the
measured rates with nothing running away. Here it gets flyvis's eyes.
Model: rest_calibration2.py's (its per-type properties and intact biases as the starting point),
with FlyvisNative (flow/0000/001, 2 ms steps) setting the release of the 69,917 neurons of flyvis
types (Hz = 50 x its output per 20 ms x the gain G). flyvis passes on changes from its grey-screen
rest, so at grey those neurons are silent. The brain's other groups are recalibrated for that, as
in rest_calibration2.py but from its biases: 12 fresh-start rounds (1 s to settle, 2 s measured),
k = 1 mV (rounds 1-8) and 0.5 (9-12), rates counted over the neurons flyvis doesn't drive.
Scenes (eyepath_native.py's fast looms, after 1 s of grey): blank; fastL and fastR, a dark disk
70 deg to one side, r/v 0.04 s, contact at 1.8 s. Rates in LATE, the last 0.5 s of the 2 s scene,
8 flies (trials).
Tests, all at one gain:
  REST    blank: mean rate of the brain's own neurons 4 Hz or less, at most 0.1% of them over 100
          Hz; LC4 and LPLC2 at most 10 Hz and the giant fiber (DNp01) at most 5 Hz on each side
  RELAY   fastL raises left LC4 and left LPLC2 by at least 3 Hz over blank (t >= 4 over flies);
          fastR the right ones
  SIDE    the loomed side's LC4 and LPLC2 rise at least 2 Hz more than the other side's (t >= 4)
  ESCAPE  the loomed side's giant fiber rises at least 3 Hz, and 2 Hz more than the other side's
          (t >= 4)
Sweep G in {1, 3, 10} on seed 1; the lowest G passing all four is confirmed on seed 2, and only
the confirmation counts. Then NULL: in 2 degree-preserving rewirings (rest_calibration2.py's, their
biases as the starting point), recalibrated the same way and run at that G on seed 2, ESCAPE fails
for both looms. Pass: the confirmation passes and NULL holds.
Reported, not gating: a drum (a vertical grating, period 30 deg, rotating at 40 deg/s either way,
rates over 0.5-2 s) at each gain: the HS cells' direction signal, (left - right) under
counterclockwise minus under clockwise, and the steering neuron DNa02's; and time courses in 20 ms
bins for the figure.

    python experiments/eyes_at_rest.py            (writes experiments/eyes_at_rest.json and eyes_at_rest/*.npz)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import rest_calibration2 as attempt2
from brainfly import nulls
from brainfly.eye2d import Grating
from brainfly.hybrid import HybridBrain
from brainfly.optic import FlyvisNative
from eyepath_fast import scenes
from shiu_rewiring import W_SYN

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
MODEL, OPTIC_DT, TRIALS = "flow/0000/001", 0.002, 8
GAINS = [1.0, 3.0, 10.0]
ROUNDS = [1.0] * 8 + [0.5] * 4
SETTLE, SCENE, LATE, BIN = 1.0, 2.0, 0.5, 0.02
TRACE = ["LC4", "LPLC2", "DNp01"]
SUBNETWORK = None      # (M, types, superclass) -> (M, slow, tau_slow), for later models; None here


class Setup:
    def __init__(self, rewiring: int | None, seed: int):
        M, scale, labels, self.types, superclass = attempt1.network()
        if rewiring is not None:
            M = nulls.degree_preserving(M, np.random.default_rng(100 + rewiring))
        key = np.where(self.types != "", self.types, np.char.add("superclass:", superclass))
        self.names, self.gid = np.unique(key, return_inverse=True)
        self.target = attempt1.targets(self.types, superclass, 2.0)
        spec, sets = attempt2.model(self.types, superclass)
        slow, tau_slow = None, 0.1
        if SUBNETWORK is not None:          # later models' per-class changes, applied after any rewiring
            M, slow, tau_slow = SUBNETWORK(M, self.types, superclass)
        start = attempt2.HERE / ("intact.npz" if rewiring is None else f"rewired-{rewiring}.npz")
        saved = np.load(start)
        assert np.array_equal(saved["groups"], self.names)
        self.bias = saved["bias"].copy()
        self.brain = HybridBrain(trials=TRIALS, w_syn=W_SYN, matrix=M, slow=slow, tau_slow=tau_slow, scale=scale, labels=labels,
                                 seed=seed, types=spec, sets=sets, bias=self.bias[self.gid])
        self.ol = FlyvisNative(self.brain, model=MODEL, dt=OPTIC_DT)
        self.silent = np.zeros(len(self.ol.neurons), np.float32)
        self.brain.set_release(self.ol.neurons, self.silent)
        self.fixed = np.zeros(self.brain.n, bool)
        self.fixed[self.brain.graded] = True
        self.fixed |= self.brain.external
        self.cells = {f"{c} {s}": self.brain.cells([c], s) for c in TRACE + ["DNa02"] for s in "LR"}
        self.cells.update({f"HS {s}": self.brain.cells(["HSN", "HSE", "HSS"], s) for s in "LR"})

    def calibrate(self) -> list:
        b, gid = self.brain, self.gid
        G = gid.max() + 1
        free_n = np.bincount(gid, weights=~self.fixed, minlength=G)
        free = free_n > 0
        goal = np.bincount(gid, weights=self.target * ~self.fixed, minlength=G) / np.maximum(free_n, 1)
        log = []
        for r, k in enumerate(ROUNDS):
            b.reset(seed=900 + r)
            b.set_release(self.ol.neurons, self.silent)
            b.set_bias(self.bias[gid])
            b.advance(int(round(1.0 / b.dt)))
            rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
            got = np.bincount(gid, weights=rate * ~self.fixed, minlength=G) / np.maximum(free_n, 1)
            step = np.where(free, np.clip(k * np.log((goal + attempt1.SOFT) / (got + attempt1.SOFT)), -k, k), 0.0)
            self.bias = np.clip(self.bias + step, attempt1.LOW, attempt1.HIGH)
            log.append({"round": r + 1, "mean_hz_own": round(float(rate[~self.fixed].mean()), 3),
                        "over_100hz": int((rate[~self.fixed] > 100).sum()),
                        "groups_within_2x": round(float(attempt1.within_factor_2(got, goal)[free].mean()), 4)})
            print(json.dumps(log[-1]), flush=True)
        b.set_bias(self.bias[gid])
        return log

    def run(self, scene, gain: float, seed: int, window: tuple[float, float]) -> dict:
        """1 s of grey, then the scene: each neuron's rate per fly in the window (scene time), the
        brain's own mean rate, and the traced cells' time courses (fly means, 20 ms bins)."""
        b, ol = self.brain, self.ol
        b.reset(seed)
        ol.reset()
        ol.gain = gain
        per = int(round(OPTIC_DT / b.dt))
        for _ in range(int(round(SETTLE / OPTIC_DT))):
            b.set_release(ol.neurons, 50.0 * ol.step(None))
            b.advance(per)
        steps = int(round(SCENE / OPTIC_DT))
        a, z = int(round(window[0] / OPTIC_DT)), int(round(window[1] / OPTIC_DT))
        acc = np.zeros((TRIALS, b.n))
        bins = int(round(SCENE / BIN))
        trace = {k: np.zeros(bins) for k in self.cells if k.split()[0] in TRACE}
        per_bin = int(round(BIN / OPTIC_DT))
        for k in range(steps):
            b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(scene(k * OPTIC_DT))))
            c = b.advance(per)
            if a <= k < z:
                acc += c
            for name in trace:
                trace[name][k // per_bin] += c[:, self.cells[name]].mean()
        rates = acc / (window[1] - window[0])
        return {"rates": rates, "own_mean_hz": float(rates[:, ~self.fixed].mean()),
                "own_over_100hz": float((rates[:, ~self.fixed].mean(0) > 100).mean()),
                "trace_hz": {k: np.round(v / BIN, 2).tolist() for k, v in trace.items()}}   # fly and cell means


def stat(d) -> dict:
    d = np.asarray(d, float)
    sd = d.std(ddof=1)
    t = float(d.mean() / (sd / np.sqrt(len(d)))) if sd > 0 else (np.inf if d.mean() > 0 else (-np.inf if d.mean() < 0 else 0.0))
    return {"delta": round(float(d.mean()), 2), "t": (round(t, 1) if np.isfinite(t) else ("inf" if t > 0 else "-inf"))}


def rises(x: dict, lo: float) -> bool:
    t = {"inf": np.inf, "-inf": -np.inf}.get(x["t"], x["t"])
    return x["delta"] >= lo and t >= 4


def loom_tests(s: Setup, gain: float, seed: int) -> dict:
    sc = scenes()
    late = (SCENE - LATE, SCENE)
    runs = {name: s.run(sc[name], gain, seed, late) for name in ("blank", "fastL", "fastR")}
    cell = lambda run, name: run["rates"][:, s.cells[name]].mean(1)          # per fly
    blank = runs["blank"]
    rest = {k: round(float(cell(blank, k).mean()), 2) for k in s.cells if k.split()[0] in TRACE}
    ok_rest = (blank["own_mean_hz"] <= 4 and blank["own_over_100hz"] <= 0.001
               and all(rest[f"{c} {x}"] <= 10 for c in ("LC4", "LPLC2") for x in "LR") and all(rest[f"DNp01 {x}"] <= 5 for x in "LR"))
    relay, side, escape = {}, {}, {}
    for scene, near, far in (("fastL", "L", "R"), ("fastR", "R", "L")):
        d = {k: cell(runs[scene], k) - cell(blank, k) for k in s.cells}
        for c in ("LC4", "LPLC2"):
            relay[f"{scene} {c}"] = stat(d[f"{c} {near}"])
            side[f"{scene} {c} near-far"] = stat(d[f"{c} {near}"] - d[f"{c} {far}"])
        escape[f"{scene} DNp01"] = stat(d[f"DNp01 {near}"])
        escape[f"{scene} DNp01 near-far"] = stat(d[f"DNp01 {near}"] - d[f"DNp01 {far}"])
    v = {"gain": gain, "seed": seed, "rest_hz": rest, "own_mean_hz": round(blank["own_mean_hz"], 3),
         "own_over_100hz": round(blank["own_over_100hz"], 5), "relay": relay, "side": side, "escape": escape,
         "REST": bool(ok_rest), "RELAY": all(rises(x, 3) for x in relay.values()),
         "SIDE": all(rises(x, 2) for x in side.values()),
         "ESCAPE": all(rises(x, 3 if "near-far" not in k else 2) for k, x in escape.items()),
         "trace_hz": {name: runs[name]["trace_hz"] for name in runs}}
    v["pass"] = bool(v["REST"] and v["RELAY"] and v["SIDE"] and v["ESCAPE"])
    return v


def drum(s: Setup, gain: float, seed: int) -> dict:
    grating = {"ccw": lambda t: [Grating(30.0, 40.0 * t)], "cw": lambda t: [Grating(30.0, -40.0 * t)]}
    r = {name: s.run(g, gain, seed, (0.5, SCENE)) for name, g in grating.items()}
    lr = lambda sc, g: float(r[sc]["rates"][:, s.cells[f"{g} L"]].mean() - r[sc]["rates"][:, s.cells[f"{g} R"]].mean())
    return {"HS_signal_hz": round(lr("ccw", "HS") - lr("cw", "HS"), 2), "DNa02_signal_hz": round(lr("ccw", "DNa02") - lr("cw", "DNa02"), 2),
            "HS_hz": {sc: {x: round(float(r[sc]["rates"][:, s.cells[f"HS {x}"]].mean()), 1) for x in "LR"} for sc in r},
            "DNa02_hz": {sc: {x: round(float(r[sc]["rates"][:, s.cells[f"DNa02 {x}"]].mean()), 2) for x in "LR"} for sc in r},
            "own_over_100hz": {sc: round(r[sc]["own_over_100hz"], 5) for sc in r}}


def show(tag: str, v: dict) -> None:
    fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t']})" for k, x in d.items())
    print(f"{tag}: {'PASS' if v['pass'] else 'fail'} REST {v['REST']} ({v['own_mean_hz']} Hz, {v['own_over_100hz']:.4%} hot) | "
          f"RELAY {v['RELAY']} {fmt(v['relay'])} | SIDE {v['SIDE']} | ESCAPE {v['ESCAPE']} {fmt(v['escape'])}", flush=True)


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    results = {"criteria": __doc__, "model": MODEL, "sweep": [], "drum": {}, "confirm": None, "nulls": []}
    s = Setup(None, seed=5)
    results["calibration"] = s.calibrate()
    np.savez_compressed(HERE / "intact.npz", groups=s.names, bias=s.bias)
    for gain in GAINS:
        v = loom_tests(s, gain, seed=1)
        results["sweep"].append(v)
        show(f"gain {gain}", v)
        results["drum"][str(gain)] = d = drum(s, gain, seed=1)
        print(f"  drum: HS {d['HS_signal_hz']:+.1f} Hz, DNa02 {d['DNa02_signal_hz']:+.2f} Hz", flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    passing = [v["gain"] for v in results["sweep"] if v["pass"]]
    if not passing:
        results["pass"] = False
        print("FAIL: no gain passes the sweep", flush=True)
    else:
        gain = min(passing)
        results["confirm"] = v = loom_tests(s, gain, seed=2)
        show(f"CONFIRM gain {gain}", v)
        for k in (1, 2):
            null = Setup(k, seed=50 + k)
            log = null.calibrate()
            n = loom_tests(null, gain, seed=2)
            results["nulls"].append({"rewiring": k, "calibration": log[-1], **{f: n[f] for f in ("escape", "relay", "ESCAPE", "RELAY", "own_mean_hz")}})
            print(f"  rewiring {k}: ESCAPE {n['ESCAPE']}, RELAY {n['RELAY']}", flush=True)
        results["NULL"] = not any(n["ESCAPE"] for n in results["nulls"])
        results["pass"] = bool(v["pass"] and results["NULL"])
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'} ({results['seconds']} s)", flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
