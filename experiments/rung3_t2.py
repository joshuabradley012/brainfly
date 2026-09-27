"""Rung 3 (pre-registered): does flyvis's model 006, fine-tuned so that its T2 answers light decrements, meet all of
rung 3's criteria?

rung3_verdict.py tested flow/0000/001, whose T2 answers light increments and decrements as a real T2 does (Keles
et al. 2020). With it, looming drives LC4 (eyepath_native_t2.py), but it got 29 of the 32 known contrast
polarities (30 needed) and T5a's direction wrong. flyvis_screen.py found no pretrained flyvis model with both a
T2 that answers decrements and at least 30 polarities. So a model has to be trained with T2's decrement response
as a constraint. T2 is not among flyvis's 32 known polarities, so the constraint leaves them untouched. The pilots
(flyvis_t2_pilot.py, 2 and 3; exploratory, none measured the tests below) found:
- fine-tuning flyvis's best model, 000, only shrinks T2's ON response;
- model 006, the one flyvis model with all 32 polarities right, has a T2 that already answers decrements weakly
  (0.95 against 4.94). Fine-tuned, it answers both within 150 iterations (ON 4.6, OFF 4.0 after 500), with
  flyvis's validation error rising from 5.27 to 5.50.
Model: flow/0000/006, fine-tuned with brainfly.vistrain on flyvis's own training task (Sintel flow, Adam, batch 4)
plus flyvis_t2_pilot3.py's symmetric T2 penalty at weight 1000 and learning rate 5e-6, for 1000 iterations,
seed 1 (the pilots used seed 0), keeping the final state. It is saved as flyvis model flow/9006/000. Its
direction selectivity and looming responses were never measured, before or after fine-tuning.
Tests, rung 3's criteria as rung3_verdict.py reads them:
  POLARITY   flyvis's flash response index (the central cell of each type, Flashes at radius 6) has the known
             polarity's sign for at least 30 of flyvis's 32 known types
  DIRECTION  flyvis_native.py's direction-selectivity check with this model tiled onto the male eye: all 8 T4/T5
             subtypes prefer their expected direction in both eyes, 16 of 16
  LOOMING    eyepath_native.py's protocol with this model: the gain sweep {0.3, 1, 3, 10} on seed 1 (6 flies),
             the lowest gain passing REST, RELAY and SIDE confirmed on seed 2 (8 flies). In the confirmation,
             the fast loom drives the loomed side's LC4 and LPLC2 to peaks of at least 20 Hz, for looms on
             either side. No confirmed gain means no LOOMING.
Pass: all three. POLARITY is a check that fixing T2 keeps 006's polarities, not a prediction, since 006 was
chosen for getting all 32. DIRECTION and LOOMING played no part in choosing anything.
Reported: T2 as flyvis_screen.py measures it (trained on, so not a test); flyvis's validation error; which
polarities changed from 006's; and, measured after the tests, 006's own direction selectivity.

    python experiments/rung3_t2.py            (writes experiments/rung3_t2.json; the model to flyvis's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch

import eyepath_native
from brainfly import FlyBrain
from brainfly import vistrain as vt
from brainfly.optic import GRADED as OPTIC, FlyvisNative
from flyvis_native import direction_selectivity
from flyvis_t2_pilot3 import t2_penalty
from rung3_verdict import polarity

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
START, NAME, ENSEMBLE = "flow/0000/006", "flow/9006/000", "flow/9006"
WEIGHT, LR, ITERS, SEED = 1000.0, 5e-6, 1000, 1


def screen_t2(ensemble: str, model: str) -> dict:
    """T2's flash peaks as flyvis_screen.py measures them (flyvis's Flashes, radius 6, dt 0.005, the central T2's
    peak change in the second after onset) and its criterion: both over 0.02, the smaller at least a third."""
    import flyvis
    from flyvis.analysis.stimulus_responses import flash_responses
    from flyvis.network import EnsembleView
    resp = flash_responses(EnsembleView(flyvis.results_dir / ensemble), radius=(6,), dt=0.005, batch_size=4)
    m = list(resp["network_name"].values).index(model)
    t, j = resp["time"].values, list(resp["cell_type"].values).index("T2")
    R = resp["responses"].values
    intensity = list(resp["intensity"].values)

    def peak(sample):
        x = R[m, sample, :, j]
        return float((x[(t >= 0) & (t < 1)] - x[t < 0].mean()).max())

    on, off = peak(intensity.index(1)), peak(intensity.index(0))
    return {"t2_on": round(on, 3), "t2_off": round(off, 3), "T2": bool(on > 0.02 and off > 0.02 and min(on, off) / max(on, off) >= 1 / 3)}


def directions(model: str) -> dict:
    brain = FlyBrain(batch=1, graded=OPTIC, dt=0.002, refractory=0.004)
    return direction_selectivity(FlyvisNative(brain, model=model))


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    results = {"criteria": __doc__, "start": START, "model": NAME}

    view, net, dec = vt.load(START)
    task = vt.sintel(view)
    epe_start = vt.validation_epe(net, dec, task)

    def log(row):
        with torch.no_grad():
            row = {**row, "t2_peaks": [round(x, 3) for x in vt.flash_peaks(net, "T2").tolist()]}
        print(json.dumps(row), flush=True)

    rows = vt.fine_tune(net, dec, task, lambda n: t2_penalty(n, "symmetric", WEIGHT), ITERS, lr=LR, seed=SEED, every=100, log=log)
    epe = vt.validation_epe(net, dec, task)
    vt.save(net, dec, NAME, source=START, val_epe=epe,
            note={"experiment": "experiments/rung3_t2.py", "penalty": "symmetric T2", "weight": WEIGHT, "lr": LR,
                  "iterations": ITERS, "seed": SEED})
    results["training"] = {"trace": rows, "val_epe_start": round(epe_start, 4), "val_epe": round(epe, 4),
                           "val_epe_000": 5.1348, "device": str(vt.DEVICE)}
    results["t2"] = screen_t2(ENSEMBLE, NAME)
    print("trained:", json.dumps(results["training"] | {"trace": None}), json.dumps(results["t2"]), flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    results["polarity"] = pol = polarity([NAME], ensemble=ENSEMBLE)[NAME]
    results["POLARITY"] = bool(pol["correct"] >= 30)
    print("polarity:", pol["correct"], "of", pol["of"], "wrong:", pol["wrong"], flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    results["direction_selectivity"] = ds = directions(NAME)
    results["DIRECTION"] = bool(len(ds) == 16 and all(v["correct"] for v in ds.values()))
    print("direction:", {k: (v["preferred"], v["dsi"], "OK" if v["correct"] else "x") for k, v in ds.items()}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    eyepath_native.main(model=NAME, out=HERE / "looming.json", criteria=__doc__)
    confirm = json.loads((HERE / "looming.json").read_text())["confirm"]
    if confirm is None:
        results["looming_peaks_hz"], results["LOOMING"] = None, False
    else:
        loom = confirm["trace_hz"]
        peaks = {f"{scene} {cell} {side}": round(float(np.max(loom[scene][f"{cell} {side}"])), 1)
                 for scene, side in (("fastL", "L"), ("fastR", "R")) for cell in ("LC4", "LPLC2")}
        results["looming_gain"], results["looming_peaks_hz"] = confirm["gain"], peaks
        results["LOOMING"] = bool(confirm["pass"] and all(p >= 20 for p in peaks.values()))
    results["pass"] = bool(results["POLARITY"] and results["DIRECTION"] and results["LOOMING"])
    print({k: results[k] for k in ("POLARITY", "DIRECTION", "LOOMING", "pass")}, results["looming_peaks_hz"], flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    # reported, after the tests: 006's own direction selectivity
    ds0 = directions(START)
    results["direction_selectivity_006"] = {"correct": int(sum(v["correct"] for v in ds0.values())),
                                            "wrong": [k for k, v in ds0.items() if not v["correct"]], "types": ds0}
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))
    print("006 direction:", results["direction_selectivity_006"]["correct"], results["direction_selectivity_006"]["wrong"], flush=True)


if __name__ == "__main__":
    main()
