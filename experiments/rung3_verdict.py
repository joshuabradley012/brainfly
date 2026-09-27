"""Rung 3's verdict for flyvis flow/0000/001, the model with which eyepath_native_t2.py's looming
reached LC4 (pre-registered; written after that result, before any of the checks below were run).

Rung 3 passes, by the ladder's criteria (README, fixed when the ladder was drawn up), on "contrast
polarity for at least 30 of 32 cell types; T4/T5 direction selectivity; looming responses of tens of
Hz". For model 001, read as:
  POLARITY   flyvis's flash response index (flyvis.analysis.flash_responses.flash_response_index on
             its Flashes at radius 6, the central cell of each type) has the sign of the known
             polarity for at least 30 of the 32 types flyvis's ground truth gives one
             (flyvis.utils.groundtruth_utils.polarity)
  DIRECTION  flyvis_native.py's direction-selectivity check, run on model 001 tiled onto the male eye:
             all 8 T4/T5 subtypes prefer their expected direction (Maisak et al. 2013) in both eyes,
             16 of 16
  LOOMING    in eyepath_native_t2.py's confirmation (recorded before this test), the fast loom drives
             the loomed side's LC4 and LPLC2 to peaks of at least 20 Hz, for looms on either side
Pass: all three.
Also reported: the same polarity count for model 000, which flyvis's authors report as 30 of 32,
checking that this reading of their method reproduces theirs.

    python experiments/rung3_verdict.py            (writes experiments/rung3_verdict.json)
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.data import DATA
from brainfly.optic import GRADED as OPTIC, FlyvisNative
from flyvis_native import direction_selectivity

OUT = Path(__file__).with_suffix(".json")
MODEL = "flow/0000/001"


def polarity(models: list[str]) -> dict:
    os.environ.setdefault("FLYVIS_ROOT_DIR", str(DATA / "flyvis"))
    import flyvis
    from flyvis.analysis.flash_responses import flash_response_index
    from flyvis.analysis.stimulus_responses import flash_responses
    from flyvis.network import EnsembleView
    from flyvis.utils.groundtruth_utils import polarity as known

    known = {k: v for k, v in known.items() if v != 0}
    ens = EnsembleView(flyvis.results_dir / "flow/0000")
    fri = flash_response_index(flash_responses(ens, radius=(6,), dt=0.005, batch_size=4), radius=6)
    fri = fri.squeeze("sample") if "sample" in fri.dims else fri                  # (network_id, neuron)
    names = list(fri["network_name"].values)
    cells = list(fri["cell_type"].values)
    out = {}
    for model in models:
        v = fri.isel(network_id=names.index(model)).values
        rows = {ct: {"fri": round(float(v[cells.index(ct)]), 3), "known": int(pol),
                     "correct": bool(np.sign(v[cells.index(ct)]) == pol)} for ct, pol in known.items()}
        out[model] = {"correct": int(sum(r["correct"] for r in rows.values())), "of": len(rows),
                      "wrong": [ct for ct, r in rows.items() if not r["correct"]], "types": rows}
    return out


def main() -> None:
    results = {"criteria": __doc__, "model": MODEL}
    results["polarity"] = pol = polarity([MODEL, "flow/0000/000"])
    print("polarity:", {m: (p["correct"], p["of"], p["wrong"]) for m, p in pol.items()}, flush=True)
    brain = FlyBrain(batch=1, graded=OPTIC, dt=0.002, refractory=0.004)
    ol = FlyvisNative(brain, model=MODEL)
    results["direction_selectivity"] = ds = direction_selectivity(ol)
    print("direction:", {k: (v["preferred"], v["dsi"], "OK" if v["correct"] else "x") for k, v in ds.items()}, flush=True)
    loom = json.loads(Path(__file__).with_name("eyepath_native_t2.json").read_text())["confirm"]["trace_hz"]
    peaks = {f"{scene} {cell} {side}": round(float(np.max(loom[scene][f"{cell} {side}"])), 1)
             for scene, side in (("fastL", "L"), ("fastR", "R")) for cell in ("LC4", "LPLC2")}
    results["looming_peaks_hz"] = peaks
    results["POLARITY"] = pol[MODEL]["correct"] >= 30
    results["DIRECTION"] = all(v["correct"] for v in ds.values()) and len(ds) == 16
    results["LOOMING"] = all(p >= 20 for p in peaks.values())
    results["pass"] = bool(results["POLARITY"] and results["DIRECTION"] and results["LOOMING"])
    print({k: results[k] for k in ("POLARITY", "DIRECTION", "LOOMING", "pass")}, peaks, flush=True)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
