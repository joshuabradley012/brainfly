"""Exploratory, not pre-registered: does ring_fit.py's best ring hold its bump on seeds it wasn't fitted on,
over rung 4's full runs?

ring_fit.py fitted the head-direction ring's class gains and biases on one seed, with 8 runs of 20 s.
Here its best parameters run as rung 4 scores the bump (rest_calibration.py's BUMP: 8 runs of 300 s
after 2 s to settle, strength per bridge side in 1-s windows against 1,000 glomerulus-label shuffles,
and the resultant of the runs' mean positions under 0.6) on four seeds it never saw (2 to 5), with
ring_fit.py's width, busiest wedge and group rates.

    python experiments/ring_heldout.py            (writes experiments/ring_heldout.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rest_calibration as attempt1
import ring_fit

OUT = Path(__file__).with_suffix(".json")
SEEDS, RUNS, SECONDS, SETTLE = (2, 3, 4, 5), 8, 300, 2.0


def main() -> None:
    t0 = time.perf_counter()
    p = json.loads(ring_fit.OUT.read_text())["best"]["params"]
    out = {"question": __doc__, "params": p, "seeds": []}
    for seed in SEEDS:
        r = ring_fit.Ring(p, RUNS, seed=seed)
        b = r.brain
        b.advance(int(round(SETTLE / b.dt)))
        w, total = [], np.zeros((RUNS, b.n))
        for _ in range(SECONDS):
            c = b.advance(int(round(1.0 / b.dt)))
            w.append(c[:, r.epg])
            total += c
        w = np.stack(w, 1)
        rate = total / SECONDS
        bump = attempt1.bump(w, r.side, r.glom, np.random.default_rng(7))
        ok = all(bump[s]["strength"] >= attempt1.MIN_BUMP and bump[s]["strength"] > bump[s]["shuffle_p99"]
                 and bump[s]["resultant"] < attempt1.MAX_RESULTANT for s in "LR")
        prof = np.stack([w[..., r.wedge == k].mean(-1) for k in range(16)], -1).reshape(-1, 16)
        prof = prof[prof.max(1) > 0]
        aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in prof]).mean(0)
        out["seeds"].append(row := {"seed": seed, "BUMP": bool(ok), "bump": bump,
                                    "fwhm_deg": 22.5 * float((aligned >= aligned.max() / 2).sum()),
                                    "busiest_wedge_hz": round(float(prof.max(1).mean()), 1), "epg_hz": round(float(rate[:, r.epg].mean()), 2),
                                    "group_hz": {g: round(float(rate[:, m].mean()), 2) for g, m in r.groups.items()}})
        print(json.dumps({k: v for k, v in row.items() if k != "bump"}),
              {s: (v["strength"], v["shuffle_p99"], v["resultant"], v["run_positions_deg"]) for s, v in bump.items()}, flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
