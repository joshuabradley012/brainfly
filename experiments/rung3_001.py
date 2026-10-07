"""Rung 3, pre-registered: does flyvis's model 001, fine-tuned with rung 3's direction test and the known polarities in
its loss, meet all of rung 3's criteria on a fresh seed?

rung3_verdict.py: model 001, whose T2 answers light decrements as a real T2 does (Keles et al. 2020) and with which
looming reaches LC4 (eyepath_native_t2.py), got 29 of 32 polarities and T5a's direction wrong. Two pre-registered
fine-tunes that protected only T2 failed: model 006's broke directions and looming (rung3_t2.py), model 000's broke
polarities and LPLC2's looming (rung3_t2_local.py). Exploratory pilots then fine-tuned 001 with rung 3's measures
protected. Protecting directions on flyvis's own lattice doesn't predict them in the eye, where rung 3 measures them
(rung3_001_pilot.py, rung3_001_pilot2.py). brainfly.eyetorch puts the eye's own direction test into the loss, and
rung3_001_pilot3.py (seed 0) then reached on rung 3's measures 31 of 32 polarities and 16 of 16 directions (T5a's
DSI 0.30), with T2 answering both flashes and flyvis's validation error 5.24 (model 001: 5.20). Its looming wasn't
measured.
Model: rung3_001_pilot3.py's procedure exactly (rung3_001_pilot3.train), with seed 1 (the pilot used seed 0): model
001; flyvis's flow task on augmented Sintel batches of 4; Adam on network and decoder at learning rate 1e-5 for 1,500
iterations. Every fourth iteration adds, at four times its weight:
- the eye's own direction test through brainfly.eyetorch (right eye, dt 0.02 s; margins 0.1 for T5 and 0.2 for T4;
  weight 300);
- flyvis's flash response index for the 32 known types except L2 (margin 0.05, weight 500);
- T2's answers to light and dark, each read against a grey run (weight 300).
Saved as flyvis model flow/9014/000.
Tests, rung 3's criteria as rung3_verdict.py and rung3_t2.py read them:
  POLARITY   flyvis's flash response index (rung3_verdict.polarity) has the known sign for at least 30 of the 32
             types flyvis's ground truth gives one
  DIRECTION  flyvis_native.py's direction-selectivity check with this model tiled onto the male eye (dt 0.002 s, both
             eyes): all 8 T4/T5 subtypes prefer their expected direction in both eyes, 16 of 16
  LOOMING    eyepath_native.py's protocol with this model: the gain sweep {0.3, 1, 3, 10} on seed 1 (6 flies), the
             lowest gain passing REST, RELAY and SIDE confirmed on seed 2 (8 flies). In the confirmation, the fast loom
             drives the loomed side's LC4 and LPLC2 to peaks of at least 20 Hz, for looms on either side. No
             confirmed gain means no LOOMING.
Pass: all three.
What it tests: POLARITY and DIRECTION are in the loss (the polarity index on flyvis's lattice; the direction test at
dt 0.02 s in one eye). Passing them shows that the fitting carries over to a new seed and to rung 3's exact measures;
it predicts nothing. LOOMING played no part in the fine-tune. It is the test of whether the fine-tuned eye still
carries a loom to LC4, LPLC2 and the giant fiber as a fly's does.
Reported: T2 as flyvis_screen.py measures it (trained on); flyvis's validation error; the T5s' responses in the eye;
the polarities that changed from model 001's.

    python experiments/rung3_001.py            (writes experiments/rung3_001.json; the model to flyvis's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import eyepath_native
import rung3_001_pilot3 as pilot
from rung3_t2 import directions, screen_t2
from rung3_verdict import polarity

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
NAME, ENSEMBLE, SEED = "flow/9014/000", "flow/9014", 1


def main() -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    results = {"criteria": __doc__, "start": pilot.START, "model": NAME, "seed": SEED}
    training = {"question": __doc__}
    pilot.train(SEED, NAME, training, HERE / "training.json", "experiments/rung3_001.py")
    end = training["end"]
    results["training"] = {"val_epe_start": training["start"]["val_epe"], "val_epe": end["val_epe"],
                           "stand_ins_at_end": {k: end[k] for k in ("eye_correct", "polarity_correct", "polarity_wrong", "t2_on", "t2_off")}}
    results["t2"] = screen_t2(ENSEMBLE, NAME)
    print("trained:", json.dumps(results["training"]), json.dumps(results["t2"]), flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    pol = polarity([NAME], ensemble=ENSEMBLE)[NAME]
    before = json.loads(Path(__file__).with_name("rung3_verdict.json").read_text())["polarity"]["flow/0000/001"]["types"]
    results["polarity"] = {"correct": pol["correct"], "of": pol["of"], "wrong": pol["wrong"],
                           "changed_from_001": {k: {"001": before[k]["fri"], "now": v["fri"], "correct_now": v["correct"]}
                                                for k, v in pol["types"].items() if v["correct"] != before[k]["correct"]},
                           "types": pol["types"]}
    results["POLARITY"] = bool(pol["correct"] >= 30)
    print("polarity:", pol["correct"], "of", pol["of"], "wrong:", pol["wrong"], flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    ds = directions(NAME)
    results["direction_selectivity"] = ds
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
