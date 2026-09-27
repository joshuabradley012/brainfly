"""Rung 3, attempt 2 (pre-registered): does flyvis's model 000, with only its T2 fine-tuned to answer light
decrements, meet all of rung 3's criteria?

rung3_t2.py fine-tuned every parameter of model 006 and failed: T2 answered darkening and 31 of 32 polarities held,
but only 6 of the 16 T4/T5 subtypes kept their direction (006 itself gets 12), and looms barely moved LC4. This
attempt starts from 000, flyvis's best model by validation error, which on the male eye gets all 16 directions
right (flyvis_native.py) and 30 of 32 polarities (C3 and T4d wrong; flyvis_screen.py); its T2 falls when the field
darkens. Only T2 changes. The pilots (flyvis_t2_pilot4-6.py; exploratory, none measured the tests below) found that
freeing T2's own synapse onto itself lets T2 run away, and that the frozen flow decoder misreads the new T2, which is
one of its inputs.
Model: flow/0000/000, fine-tuned with brainfly.vistrain on flyvis's own task (Sintel flow, Adam, batch 4) plus
flyvis_t2_pilot5.py's penalty on T2's flash responses (T2's mean change over a dark flash's first 0.25 s at least
1, the smaller peak at least half the larger, both peaks between 0.1 and 5; weight 1000), for 500 iterations at
learning rate 1e-4, seed 1 (the pilots used seed 0), keeping the final state. Free: T2's resting potential and time
constant and the strengths of the synapses onto T2 except its own (flyvis_t2_pilot5.masks), and the flow decoder,
which only reads the network. Saved as flyvis model flow/9000/000.
Tests, rung 3's criteria as rung3_verdict.py and rung3_t2.py read them:
  POLARITY   flyvis's flash response index (the central cell of each type, Flashes at radius 6) has the known
             polarity's sign for at least 30 of flyvis's 32 known types
  DIRECTION  flyvis_native.py's direction-selectivity check with this model tiled onto the male eye: all 8 T4/T5
             subtypes prefer their expected direction in both eyes, 16 of 16
  LOOMING    eyepath_native.py's protocol with this model: the gain sweep {0.3, 1, 3, 10} on seed 1 (6 flies), the
             lowest gain passing REST, RELAY and SIDE confirmed on seed 2 (8 flies); in the confirmation the fast loom
             drives the loomed side's LC4 and LPLC2 to peaks of at least 20 Hz, for looms on either side. No
             confirmed gain means no LOOMING.
Pass: all three. POLARITY and DIRECTION check that changing T2 keeps what 000 already had (000 was chosen knowing
both); LOOMING, where 000 fails because its T2 ignores darkening, is the test of the change.
Reported: T2 as flyvis_screen.py measures it (trained on, so not a test), and flyvis's validation error (000: 5.13).

    python experiments/rung3_t2_local.py            (writes experiments/rung3_t2_local.json; the model to flyvis's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch

import eyepath_native
from brainfly import vistrain as vt
from flyvis_t2_pilot5 import masks, penalty
from rung3_t2 import directions, screen_t2
from rung3_verdict import polarity

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
START, NAME, ENSEMBLE = "flow/0000/000", "flow/9000/000", "flow/9000"
LR, ITERS, SEED = 1e-4, 500, 1


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

    rows = vt.fine_tune(net, dec, task, penalty, ITERS, lr=LR, seed=SEED, every=50, log=log, masks=masks(net), train_decoder=True)
    epe = vt.validation_epe(net, dec, task)
    vt.save(net, dec, NAME, source=START, val_epe=epe,
            note={"experiment": "experiments/rung3_t2_local.py", "free": "T2's parameters and its inputs but not T2->T2; the decoder",
                  "lr": LR, "iterations": ITERS, "seed": SEED})
    results["training"] = {"trace": rows, "val_epe_start": round(epe_start, 4), "val_epe": round(epe, 4), "device": str(vt.DEVICE)}
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
    results["seconds"] = round(time.perf_counter() - t0)
    print({k: results[k] for k in ("POLARITY", "DIRECTION", "LOOMING", "pass")}, results["looming_peaks_hz"], flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
