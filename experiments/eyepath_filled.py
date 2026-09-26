"""Does filling in the missing photoreceptor input let looming through to the looming detectors?

eyepath.py: with a graded retina and lamina, a dark object looming on one side moved LC4 and LPLC2 on
that side, with the right signs all along the pathway, but by only about 1.5 Hz on average, short of
its 3 Hz bar. Part of the reason is in the data: in MaleCNS v1.0, 962 of 1,769 lamina columns have no
photoreceptor input (brainfly.retina). This repeats eyepath.py with FlyBrain(fill_retina=True): the
same graded sets, knobs, scenes, seeds, criteria, sweep and confirmation, with one fix to a criterion
known to be broken before this run.

Pass criteria, fixed before the first run (all must hold):
  REST    blank field: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; <= 5% of graded
          neurons at the floor or ceiling of their release; and the neurons outside the optic lobe
          and retina (the same population in every condition) fire at no more than 1.2 x their rate
          in the original all-spiking model, measured here. That replaces eyepath.py's "mean rate of
          all spiking neurons <= 5 Hz", which changed its denominator from one graded set to another.
  RELAY   loomL raises left LC4 and left LPLC2 by >= 3 Hz each (t >= 4 over flies); loomR likewise on the right
  SIDE    loomL raises left LC4 and left LPLC2 more than their right copies, by >= 2 Hz (t >= 4); loomR mirrored
Secondary: ESCAPE as in eyepath.py. Sweep on one seed with 6 flies; for each graded set the passing
config with the lowest graded_gain (then lowest graded_release) is re-run on a fresh seed with 8
flies, and only that confirmation counts.

Descriptive, not a criterion: LC4 and LPLC2 grouped by the columns they draw on. Column intactness
(1 = the column's L1 gets photoreceptor input, 0 = blind) is spread through the connectome from the
columnar neurons, three synapses deep, as a synapse-weighted average. Detectors >= 0.75 count as
intact-column, <= 0.25 as blind-column. Their per-neuron loom responses are reported with the fill
off and on, at eyepath.py's strongest setting that kept the network at rest (lamina set,
graded_gain 0.15, graded_release 0.3). If the fill is faithful, blind-column detectors should be
silent without it and respond like intact-column ones with it.

    python experiments/eyepath_filled.py            (writes experiments/eyepath_filled.json)
"""
from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly import FlyBrain
from brainfly.eyes import Eyes
from brainfly.retina import _columns
from brainfly.shiu import counts
from eyepath import GRADED, GRADED_GAIN, GRADED_RELEASE, SCENES, SECONDS, STATIONS, WARM, stat

OUT = Path(__file__).with_name("eyepath_filled.json")
N0 = 166_700   # neurons before the fill; the fixed REST population is drawn from these


def measure(brain: FlyBrain, scene, contrast: bool, seed: int, rest_pop: np.ndarray) -> dict:
    brain.reset(seed)
    eyes = Eyes(brain.azimuth)
    steps, warm = int(SECONDS / brain.dt), int(WARM / brain.dt)
    B = brain.batch
    counts_ = np.zeros((brain.n, B), np.float32)
    release = np.zeros((len(brain.graded), B), np.float32)
    bounds = 0.0
    for s in range(steps):
        blobs = scene(s * brain.dt)
        fired = brain.step(eyes.contrast(blobs) if contrast else eyes.drive(blobs))
        if s < warm:
            continue
        for b, f in enumerate(fired if B > 1 else [fired]):
            counts_[f, b] += 1
        if len(brain.graded):
            out = brain.graded_out
            release += out
            bounds += float(np.mean((out <= -brain.graded_release + 1e-6) | (out >= 1 - brain.graded_release - 1e-6)))
    window = (steps - warm) * brain.dt
    graded_pos = {int(i): k for k, i in enumerate(brain.graded)}
    rates = {}
    for name, types in STATIONS.items():
        for side in "LR":
            idx = brain.cells(types, side)
            idx = idx[idx < N0]
            if len(brain.graded) and idx[0] in graded_pos:
                rows = [graded_pos[int(i)] for i in idx]
                rates[f"{name} {side}"] = (release[rows].mean(0) / window).tolist()
            else:
                rates[f"{name} {side}"] = (counts_[idx].mean(0) / window).tolist()
    return {"rates": rates, "rest_pop_hz": float(counts_[rest_pop].mean() / window),
            "graded_at_bounds": bounds / (steps - warm) if len(brain.graded) else 0.0,
            "per_neuron_hz": counts_[:N0] / window}


def verdict(m: dict, rest_ref_hz: float) -> dict:
    r = {scene: {k: np.array(v) for k, v in m[scene]["rates"].items()} for scene in SCENES}
    rest = m["blank"]
    ok_rest = (all(r["blank"][f"{st} {s}"].mean() <= 10 for st in ("LC4", "LPLC2") for s in "LR")
               and all(r["blank"][f"DNp01 {s}"].mean() <= 5 for s in "LR")
               and rest["graded_at_bounds"] <= 0.05 and rest["rest_pop_hz"] <= 1.2 * rest_ref_hz)
    relay, side, escape = {}, {}, {}
    for scene, near, far in (("loomL", "L", "R"), ("loomR", "R", "L")):
        d = {k: r[scene][k] - r["blank"][k] for k in r[scene]}
        for st in ("LC4", "LPLC2", "DNp01"):
            up = stat(d[f"{st} {near}"])
            lateral = stat(d[f"{st} {near}"] - d[f"{st} {far}"])
            (escape if st == "DNp01" else relay)[f"{scene} {st}"] = up
            (escape if st == "DNp01" else side)[f"{scene} {st} near-far"] = lateral
    rises = lambda x, lo: x["delta"] >= lo and x["t"] >= 4
    ok_relay = all(rises(x, 3) for x in relay.values())
    ok_side = all(rises(x, 2) for x in side.values())
    ok_escape = all(rises(x, 3 if "near-far" not in k else 2) for k, x in escape.items())
    return {"REST": bool(ok_rest), "RELAY": bool(ok_relay), "SIDE": bool(ok_side), "pass": bool(ok_rest and ok_relay and ok_side),
            "ESCAPE": bool(ok_escape),
            "rest_hz": {k: round(float(r["blank"][k].mean()), 2) for k in ("LC4 L", "LC4 R", "LPLC2 L", "LPLC2 R", "DNp01 L", "DNp01 R")},
            "rest_pop_hz": round(rest["rest_pop_hz"], 2), "rest_ref_hz": round(rest_ref_hz, 2),
            "graded_at_bounds": round(rest["graded_at_bounds"], 4), "relay": relay, "side": side, "escape": escape}


def run_config(brain: FlyBrain, contrast: bool, seed: int, rest_pop: np.ndarray, rest_ref_hz: float, keep=False):
    m = {scene: measure(brain, fn, contrast, seed, rest_pop) for scene, fn in SCENES.items()}
    v = verdict(m, rest_ref_hz)
    v["stations"] = {k: {scene: round(float(np.mean(m[scene]["rates"][k])), 2) for scene in SCENES} for k in m["blank"]["rates"]}
    return (v, m) if keep else v


def intactness() -> np.ndarray:
    """Per neuron: synapse-weighted share of its column-assigned inputs, three synapses deep, that come
    from intact columns (nan where no columnar input reaches it)."""
    from brainfly.data import DATA
    meta = np.load(DATA / "brain.npz")
    C = counts().tocsr()
    A = abs(C).tocsr()
    cell_type, side = meta["cell_type"].astype(str), meta["side"].astype(str)
    cols, _ = _columns(DATA, C, cell_type, side)
    is_r = cell_type == "R1-6"
    score = np.full(A.shape[0], np.nan)
    for c in cols.values():
        if "L1" not in c:
            continue
        ok = float(is_r[A[c["L1"]].indices].any())
        for i in c.values():
            score[i] = ok
    known = ~np.isnan(score)
    for _ in range(3):
        s = np.nan_to_num(score)
        num = A @ (s * known)
        den = A @ known.astype(float)
        new = np.where(den > 0, num / np.maximum(den, 1e-12), np.nan)
        score = np.where(known, score, new)
        known = ~np.isnan(score)
    return score


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "sweep": [], "confirm": {}}
    ref = FlyBrain(batch=6)
    optic_or_retina = np.zeros(N0, bool)
    optic_or_retina[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic_or_retina)
    rest_ref_hz = measure(ref, SCENES["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    print(f"REST population: {len(rest_pop):,} neurons outside the optic lobe and retina; original model {rest_ref_hz:.2f} Hz", flush=True)
    del ref
    for name in ("lamina", "optic"):
        brain = FlyBrain(batch=6, graded=GRADED[name], fill_retina=True)
        for gain, release in itertools.product(GRADED_GAIN, GRADED_RELEASE):
            t1 = time.perf_counter()
            brain.graded_gain, brain.graded_release = gain, release
            v = run_config(brain, True, 1, rest_pop, rest_ref_hz)
            results["sweep"].append({"graded": name, "graded_gain": gain, "graded_release": release, **v})
            fmt = lambda d: " ".join(f"{k}:{x['delta']:+.1f}(t{x['t']:.0f})" for k, x in d.items())
            print(f"{name} gain {gain} release {release}: {'PASS' if v['pass'] else 'fail'}  REST {v['REST']} {v['rest_hz']} "
                  f"pop {v['rest_pop_hz']} bounds {v['graded_at_bounds']} | RELAY {v['RELAY']} {fmt(v['relay'])} | SIDE {v['SIDE']} | "
                  f"ESCAPE {v['ESCAPE']} {fmt(v['escape'])} ({time.perf_counter() - t1:.0f} s)", flush=True)
            OUT.write_text(json.dumps(results, indent=1))
        passing = [r for r in results["sweep"] if r["graded"] == name and r["pass"]]
        if not passing:
            print(f"{name}: no config passed the sweep; nothing to confirm", flush=True)
            continue
        pick = min(passing, key=lambda r: (r["graded_gain"], r["graded_release"]))
        brain = FlyBrain(batch=8, graded=GRADED[name], fill_retina=True)
        brain.graded_gain, brain.graded_release = pick["graded_gain"], pick["graded_release"]
        v = run_config(brain, True, 2, rest_pop, rest_ref_hz)
        results["confirm"][name] = {"graded_gain": pick["graded_gain"], "graded_release": pick["graded_release"], **v}
        print(f"CONFIRM {name} (gain {pick['graded_gain']}, release {pick['graded_release']}): {'PASS' if v['pass'] else 'FAIL'} "
              f"REST {v['REST']} RELAY {v['RELAY']} SIDE {v['SIDE']} ESCAPE {v['ESCAPE']}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))

    # descriptive: detectors by column intactness, fill off vs on
    score = intactness()
    groups = {}
    base = FlyBrain(batch=6, graded=GRADED["lamina"])
    for st in ("LC4", "LPLC2"):
        for s in "LR":
            idx = base.cells([st], s)
            groups[f"{st} {s}"] = {"intact": idx[score[idx] >= 0.75], "blind": idx[score[idx] <= 0.25]}
    split = {}
    for fill in (False, True):
        brain = FlyBrain(batch=6, graded=GRADED["lamina"], fill_retina=fill)
        brain.graded_gain, brain.graded_release = 0.15, 0.3
        _, m = run_config(brain, True, 1, rest_pop, rest_ref_hz, keep=True)
        for scene, near in (("loomL", "L"), ("loomR", "R")):
            d = (m[scene]["per_neuron_hz"] - m["blank"]["per_neuron_hz"]).mean(1)
            for st in ("LC4", "LPLC2"):
                for region, idx in groups[f"{st} {near}"].items():
                    key = f"{'fill' if fill else 'no fill'} | {scene} {st} {near} {region}-column"
                    split[key] = {"n": int(len(idx)), "mean_hz": round(float(d[idx].mean()), 2) if len(idx) else None,
                                  "top10pct_hz": round(float(np.sort(d[idx])[::-1][:max(1, len(idx) // 10)].mean()), 2) if len(idx) else None}
                    print(f"  {key}: {split[key]}", flush=True)
    results["detectors_by_column"] = split
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
