"""Does looming reach the looming detectors when the fly sees through a real 2-D eye?

eyepath.py and eyepath_filled.py showed stimuli to a 1-D eye: each photoreceptor had one azimuth,
taken from a column coordinate that turned out to follow elevation (brainfly.eye2d), so the
"object looming from the left" was a band sweeping vertically across the left eye. It also crossed
the midline at the end. brainfly.eye2d.CompoundEye gives every photoreceptor its measured viewing
direction (Zhao et al.'s eye map registered to MaleCNS) and renders a dark disk through 7.7 deg
facet blur. This repeats eyepath_filled.py (retina filled, same graded sets, knobs, seeds, sweep
and confirmation) with that eye and a proper looming disk.

Scenes, 2 s each, rates from 0.5 to 2 s, same noise in every scene (paired by fly):
  blank    no object
  loomL    a dark disk (90% darker) centred 70 deg to the left at the horizon, approaching at
           constant speed with r/v = 0.4 s (radius atan(0.4 / (2.2 s - t))), capped at 45 deg, so
           it grows from 13 deg at 0.5 s to 45 deg and never reaches the other eye
  loomR    its mirror image
Pass criteria, fixed before the first run (all must hold), exactly eyepath_filled.py's:
  REST    blank field: LC4 and LPLC2 <= 10 Hz and DNp01 <= 5 Hz on both sides; <= 5% of graded
          neurons at their release limits; the neurons outside the optic lobe and retina fire at no
          more than 1.2 x their rate in the original all-spiking model
  RELAY   loomL raises left LC4 and left LPLC2 by >= 3 Hz each (t >= 4 over flies); loomR likewise on the right
  SIDE    loomL raises left LC4 and left LPLC2 more than their right copies, by >= 2 Hz (t >= 4); loomR mirrored
Secondary: ESCAPE (same-side giant fiber DNp01 up >= 3 Hz and >= 2 Hz above the other side, t >= 4).
Sweep on seed 1 with 6 flies; for each graded set the passing config with the lowest graded_gain
(then lowest graded_release) is re-run on seed 2 with 8 flies, and only that confirmation counts.

Descriptive, not a criterion (the intact-vs-blind test the 1-D eye couldn't do): in each eye, a
small loom (same approach, capped at 20 deg) centred on the mean direction of the intact columns
(L1 with >= 5 R1-6 partners), and one centred on the blind columns (no R1-6 input), with the fill
off and on, at eyepath_filled.py's closest setting (optic set, graded_gain 0.15, graded_release
0.3). Reported: the same-side LPLC2, LC4 and DNp01 change. Without the fill the blind-region loom
should do little; with it, both should work.

    python experiments/eyepath_2d.py            (writes experiments/eyepath_2d.json)
"""
from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.data import DATA
from brainfly.eye2d import CompoundEye, column_directions, looming
from brainfly.retina import INTACT, _columns
from brainfly.shiu import counts
from eyepath import GRADED, GRADED_GAIN, GRADED_RELEASE, SECONDS, STATIONS, WARM
from eyepath_filled import N0, measure as measure_1d, verdict

OUT = Path(__file__).with_name("eyepath_2d.json")
LOOM = dict(r_over_v=0.4, contact=2.2)


def scenes(max_deg: float = 45.0, left=(70.0, 0.0), right=(-70.0, 0.0)) -> dict:
    return {"blank": lambda t: [],
            "loomL": looming(*left, max_deg=max_deg, **LOOM),
            "loomR": looming(*right, max_deg=max_deg, **LOOM)}


def measure(brain: FlyBrain, eye: CompoundEye, scene, seed: int, rest_pop: np.ndarray) -> dict:
    brain.reset(seed)
    steps, warm = int(SECONDS / brain.dt), int(WARM / brain.dt)
    B = brain.batch
    spikes = np.zeros((brain.n, B), np.float32)
    release = np.zeros((len(brain.graded), B), np.float32)
    bounds = 0.0
    for s in range(steps):
        fired = brain.step(eye.contrast(scene(s * brain.dt)))
        if s < warm:
            continue
        for b, f in enumerate(fired if B > 1 else [fired]):
            spikes[f, b] += 1
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
            if idx[0] in graded_pos:
                rates[f"{name} {side}"] = (release[[graded_pos[int(i)] for i in idx]].mean(0) / window).tolist()
            else:
                rates[f"{name} {side}"] = (spikes[idx].mean(0) / window).tolist()
    return {"rates": rates, "rest_pop_hz": float(spikes[rest_pop].mean() / window),
            "graded_at_bounds": bounds / (steps - warm)}


def run_config(brain, eye, seed, rest_pop, rest_ref_hz, sc) -> dict:
    m = {name: measure(brain, eye, fn, seed, rest_pop) for name, fn in sc.items()}
    v = verdict(m, rest_ref_hz)
    v["stations"] = {k: {name: round(float(np.mean(m[name]["rates"][k])), 2) for name in sc} for k in m["blank"]["rates"]}
    return v


def region_centres() -> dict:
    """Mean viewing direction of each eye's intact and blind columns, as (azimuth, elevation) degrees."""
    meta = np.load(DATA / "brain.npz")
    C = counts().tocsr()
    A = abs(C).tocsr()
    cols, _ = _columns(DATA, C, meta["cell_type"].astype(str), meta["side"].astype(str))
    is_r = meta["cell_type"].astype(str) == "R1-6"
    dirs = column_directions()
    groups: dict = {}
    for k, c in cols.items():
        if "L1" not in c or k not in dirs:
            continue
        n = int(is_r[A[c["L1"]].indices].sum())
        region = "intact" if n >= INTACT else "blind" if n == 0 else None
        if region:
            groups.setdefault((k[0], region), []).append(dirs[k])
    out = {}
    for (s, region), vs in groups.items():
        v = np.mean(vs, axis=0)
        v /= np.linalg.norm(v)
        out[f"{s} {region}"] = (float(np.degrees(np.arctan2(v[1], v[0]))), float(np.degrees(np.arcsin(v[2]))), len(vs))
    return out


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "sweep": [], "confirm": {}}
    ref = FlyBrain(batch=6)
    optic = np.zeros(N0, bool)
    optic[ref.cells(GRADED["optic"])] = True
    rest_pop = np.flatnonzero(~optic)
    from eyepath import SCENES as SCENES_1D
    rest_ref_hz = measure_1d(ref, SCENES_1D["blank"], False, 1, rest_pop)["rest_pop_hz"]
    results["rest_reference_hz"] = round(rest_ref_hz, 2)
    del ref
    sc = scenes()
    for name in ("lamina", "optic"):
        brain = FlyBrain(batch=6, graded=GRADED[name], fill_retina=True)
        eye = CompoundEye(brain)
        if name == "lamina":
            results["photoreceptors_placed"] = f"{int(eye.placed.sum())} of {len(eye.placed)}"
        for gain, release in itertools.product(GRADED_GAIN, GRADED_RELEASE):
            t1 = time.perf_counter()
            brain.graded_gain, brain.graded_release = gain, release
            v = run_config(brain, eye, 1, rest_pop, rest_ref_hz, sc)
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
        eye = CompoundEye(brain)
        brain.graded_gain, brain.graded_release = pick["graded_gain"], pick["graded_release"]
        v = run_config(brain, eye, 2, rest_pop, rest_ref_hz, sc)
        results["confirm"][name] = {"graded_gain": pick["graded_gain"], "graded_release": pick["graded_release"], **v}
        print(f"CONFIRM {name} (gain {pick['graded_gain']}, release {pick['graded_release']}): {'PASS' if v['pass'] else 'FAIL'} "
              f"REST {v['REST']} RELAY {v['RELAY']} SIDE {v['SIDE']} ESCAPE {v['ESCAPE']}", flush=True)
        OUT.write_text(json.dumps(results, indent=1))

    centres = region_centres()
    results["region_centres"] = {k: {"azimuth": round(a, 1), "elevation": round(e, 1), "columns": n} for k, (a, e, n) in centres.items()}
    print("region centres:", results["region_centres"], flush=True)
    regional = {}
    for fill in (False, True):
        brain = FlyBrain(batch=6, graded=GRADED["optic"], fill_retina=fill)
        eye = CompoundEye(brain)
        brain.graded_gain, brain.graded_release = 0.15, 0.3
        for region in ("intact", "blind"):
            L, R = centres[f"L {region}"][:2], centres[f"R {region}"][:2]
            v = run_config(brain, eye, 1, rest_pop, rest_ref_hz, scenes(max_deg=20.0, left=L, right=R))
            for side in ("L", "R"):
                scene = f"loom{side}"
                row = {st: v["stations"][f"{st} {side}"][scene] - v["stations"][f"{st} {side}"]["blank"] for st in ("LPLC2", "LC4", "DNp01")}
                key = f"{'fill' if fill else 'no fill'} | {region}-region loom, {side} eye"
                regional[key] = {k: round(x, 2) for k, x in row.items()}
                print(f"  {key}: {regional[key]}", flush=True)
    results["regional"] = regional
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
