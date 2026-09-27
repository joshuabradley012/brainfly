"""How fast a machine runs the resting brain: rest_fc.py's model (rung 1's network with background
for every neuron) for 8 trials, timed after a warm-up that also compiles the kernel. Prints trial-
seconds simulated per wall second, the number that sizes a job for scripts/remote/run.sh.

    NUMBA_NUM_THREADS=8 python scripts/remote/bench.py [seconds]
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "experiments"))
from brainfly.data import DATA  # noqa: E402
from brainfly.hybrid import HybridBrain, consensus_transmitters  # noqa: E402
from brainfly.shiu import counts, mcns_types  # noqa: E402
from shiu_rewiring import W_SYN  # noqa: E402
from shiu_scaled import sizes  # noqa: E402
from shiu_sensory import no_sensory_input  # noqa: E402
from shiu_signs import fast_network  # noqa: E402


def main() -> None:
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    C = counts().tocsr()
    meta = np.load(DATA / "brain.npz")
    types = mcns_types()
    labels = {"cell_type": meta["cell_type"], "side": meta["side"], "superclass": meta["superclass"], "mcns_type": types}
    M, _ = fast_network(C, consensus_transmitters(), meta["superclass"], np.char.startswith(types.astype(str), "KC"))
    M, _ = no_sensory_input(M, meta["superclass"])
    brain = HybridBrain(trials=8, w_syn=W_SYN, matrix=M, scale=1.0 / sizes(C), labels=labels,
                        types={"all": {"noise_rate": 200.0, "noise_kick": 1.0}, "APL": {"unit": "graded"}})
    brain.advance(5000)                                                     # compile, and leave rest
    t = time.perf_counter()
    spikes = brain.advance(int(round(seconds / brain.dt)))
    wall = time.perf_counter() - t
    print(f"{os.uname().nodename}: {os.environ.get('NUMBA_NUM_THREADS', 'all')} threads, {8 * seconds / wall:.2f} "
          f"trial-seconds per second ({wall:.1f} s for 8 x {seconds:g} s; mean rate {spikes.mean() / seconds:.1f} Hz)")


if __name__ == "__main__":
    main()
