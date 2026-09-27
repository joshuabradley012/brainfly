"""How fast a machine runs the current resting brain (taste_escape.py's model, with flyvis's eyes): one
calibration round (3 s at grey) and one looming run (1 s grey + 2 s of a fast loom), 8 trials, timed after a
warm-up that compiles the kernel. Prints trial-seconds simulated per wall second for each, and the spike
checksums (the same on every machine, since the simulation is deterministic).

    NUMBA_NUM_THREADS=8 python scripts/remote/bench_current.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments"))
import escape_at_rest2 as escape2  # noqa: E402
import rest_calibration as attempt1  # noqa: E402
import taste_escape as te  # noqa: E402
from eyepath_fast import scenes  # noqa: E402


def main() -> None:
    t = time.perf_counter()
    attempt1.network = escape2.network
    s, _ = te.build(None, seed=5)
    s.bias = np.load(ROOT / "experiments" / "taste_escape" / "intact.npz")["bias"]
    b = s.brain
    b.set_bias(s.bias[s.gid])
    setup = time.perf_counter() - t
    b.reset(1)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(200)
    t = time.perf_counter()
    b.reset(900)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(2.0 / b.dt)))
    t_rest = time.perf_counter() - t
    t = time.perf_counter()
    loom = s.run(scenes()["fastL"], 1.0, 1, (1.5, 2.0))["rates"]
    t_loom = time.perf_counter() - t
    print(f"{os.uname().nodename} ({os.cpu_count()} cpus, {os.environ.get('NUMBA_NUM_THREADS', 'all')} threads): setup {setup:.0f} s, "
          f"calibration round {24 / t_rest:.2f} trial-s/s, looming run {24 / t_loom:.2f} trial-s/s, "
          f"checksums {int(rest.sum())} {float(loom.sum()):.0f}", flush=True)


if __name__ == "__main__":
    main()
