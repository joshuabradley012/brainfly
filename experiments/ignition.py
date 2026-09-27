"""Exploratory, not pre-registered: does calibrating longer make the resting brain's left looming loop ignite?

escape_at_rest.py failed REST: its left LPLC2, LC4 and giant fiber ran at rest (28, 8 and 28 Hz,
fly means). Its pilots, and depression_classes.py after it, found every fly quiet at the same
settings. But they calibrated for 10 fresh-start rounds (depression_rules.measure sets its own),
while escape_at_rest.py ran eyes_at_rest.py's 12. So either the extra rounds tip the loop over, or
the formal run drew flies that ignite. Here, for escape_at_rest.py's model and for the same with
the visual projection neurons depressed mildly and fast (0.95 / 0.3 s, depression_classes.py's best),
each calibrated both ways from eyes_at_rest.py's eyes-open biases: each fly's resting LC4, LPLC2 and
giant fiber rates on each side (blank scene, the last 0.5 s, as REST measures them) on seeds 1, 11,
12 and 13, 32 flies. A fly counts as ignited if its giant fiber passes 5 Hz or its LC4 or LPLC2
passes 10 Hz on either side (REST's limits, applied to one fly). Seed 2, which confirms, isn't used.

    python experiments/ignition.py            (writes experiments/ignition.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import depression_classes as classes
import eyes_at_rest as eyes
import rest_calibration2 as attempt2

OUT = Path(__file__).with_suffix(".json")
SEEDS = [1, 11, 12, 13]
MODELS = {"escape_at_rest.py's model": classes.class_model(0.5, 0.0),
          "the same, VPNs 0.95 / 0.3 s": classes.class_model(0.5, 0.0, {"depression": 0.95, "recovery": 0.3})}
ROUNDS = {"10 rounds": [1.0] * 6 + [0.5] * 4, "12 rounds": [1.0] * 8 + [0.5] * 4}
LIMIT = {"LC4": 10.0, "LPLC2": 10.0, "DNp01": 5.0}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "runs": []}
    start = np.load(eyes.HERE / "intact.npz")["bias"]
    for label, model in MODELS.items():
        for rounds, schedule in ROUNDS.items():
            attempt2.model, eyes.ROUNDS = model, schedule
            s = eyes.Setup(None, seed=5)
            s.bias = start.copy()
            log = s.calibrate()
            fly = {k: [] for k in s.cells if k.split()[0] in LIMIT}
            for seed in SEEDS:
                rates = s.run(lambda t: [], 1.0, seed, window=(eyes.SCENE - eyes.LATE, eyes.SCENE))["rates"]
                for k in fly:
                    fly[k] += np.round(rates[:, s.cells[k]].mean(1), 1).tolist()
            hot = np.zeros(len(SEEDS) * eyes.TRIALS, bool)
            for k, v in fly.items():
                hot |= np.asarray(v) > LIMIT[k.split()[0]]
            out["runs"].append(r := {"model": label, "calibration": rounds, "last_round": log[-1],
                                     "ignited_flies": int(hot.sum()), "flies": len(hot), "per_fly_hz": fly})
            print(json.dumps({k: v for k, v in r.items() if k != "per_fly_hz"}), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
