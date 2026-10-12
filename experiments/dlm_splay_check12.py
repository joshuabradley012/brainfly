"""Exploratory check, written after review 13 and before it runs, not pre-registered and not a change to the model: how
close to threshold the leaky-integrator units of the splay checks sit, once the junctions' current is counted.

The README's caveat on the leaky integrators said that, with a 20 ms membrane, one fires regularly at 6.6 Hz only with
its drive within about 0.1 mV of threshold. As evidence it set the coupled units' biases (7.07-7.11 mV against a 7 mV
threshold; dlm_splay_check6.py) beside the uncoupled unit's (a few microvolts above it; dlm_splay_check2.py). Review 13
found that the biases leave out the junctions' current, which near threshold draws back about as much as the biases
add. So the coupled units may sit as close to threshold as the uncoupled ones. Its numbers came from a review-only run.
Model: dlm_splay_check6.py's "LIF, MN5 assumed" (its biases, dlm_splay_check2.py's kicks, flies' coupling as 20 ms
peak ratios), and the same units uncoupled at dlm_splay_check2.py's bias. 8 runs of 60 s after 3 s (seeds 5400 and 5401),
stepped 0.1 ms at a time. Each step, from that step's starting voltages, each unit's junction term is
J_i = sum_j r_ij (u_j - u_i), in mV of drive as HybridBrain applies it.
Measured, for each unit while its voltage is within 0.1 mV, and within 0.02 mV, below threshold:
- J's mean and SD;
- the net margin, bias + the kicks' mean drive (rate x 0.1 mV x 20 ms) + J's mean - 7 mV.
Also each unit's rate, and the margin a noise-free unit needs for 6.6 Hz, from its interspike interval
tau ln((b - reset)/(b - threshold)) + refractory.
Read: if the coupled units' net margin near threshold is no larger than the uncoupled unit's margin (0.02-0.03 mV), they
sit as close to threshold as the uncoupled, and the caveat should give that margin instead of the biases.

Ran (2026-10-12, 72 s): coupled, the units sit as close to threshold as uncoupled.
- A noise-free unit needs its drive 0.0069 mV above threshold to fire at 6.6 Hz.
- Uncoupled (6.53-6.57 Hz), the bias and the kicks' mean drive (0.0216 mV) put the units 0.023 mV above threshold.
  They spend 38% of the time within 0.1 mV below it, and 22% within 0.02 mV.
- Coupled (6.53-6.64 Hz):
  - Within 0.1 mV below threshold (25% of the time for MN1-4, 36% for MN5), the junction term averages -0.135 mV for
    MN1-4 (SD 0.10) and -0.088 mV for MN5 (SD 0.06). The net margin is -0.002 to -0.001 mV.
  - Within 0.02 mV (3% and 5% of the time), it averages -0.078 and -0.056 mV (SD 0.07 and 0.06). The net margin is
    +0.054 to +0.055 mV for MN1-4 and +0.031 for MN5.
So by the reading, the biases' 0.07-0.11 mV above threshold only offset what the junctions draw back near threshold.
Coupled or not, these units fire with their drive within a few hundredths of a millivolt of threshold, and junction
currents that fluctuate by 0.06-0.10 mV decide when they cross.

Correction (2026-10-12, review 14): by the reading as written, the outcome is split. Within 0.1 mV of threshold the
coupled units sit at -0.002 to -0.001 mV, as close as uncoupled. Within 0.02 mV they sit at +0.031 (MN5) to +0.055 mV
(MN1-4), 1.4-2.4 times the uncoupled 0.023, outside the reading's 0.02-0.03 mV. Nearest threshold the junctions offset
58-59% of MN1-4's drive above threshold, not all of it. The substance stands: coupled or not, the units sit a few
hundredths of a millivolt from threshold, not the 0.07-0.11 mV the biases suggest.

    python experiments/dlm_splay_check12.py      (writes experiments/dlm_splay_check12.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6

OUT = Path(__file__).with_suffix(".json")
SEED = 5400
SECONDS = 60.0
WINDOWS = (0.1, 0.02)


def noise_free_margin(hz: float = c1.TARGET_HZ) -> float:
    """b - threshold for a noise-free unit firing at hz (bisection on its interspike interval)."""
    u = c1.UNIT
    isi = lambda b: u["tau_m"] * np.log((b - u["reset"]) / (b - u["threshold"])) + u["refractory"]
    lo, hi = 1e-9, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if isi(u["threshold"] + mid) > 1.0 / hz else (lo, mid)
    return 0.5 * (lo + hi)


def measure(biases: np.ndarray, kick_hz: float, coupling, seed: int) -> dict:
    b = c5.unit("LIF", 0.0, kick_hz, c1.KICK_MV, coupling, None, c1.RUNS)
    b.set_bias(np.asarray(biases, np.float64))
    b.reset(seed)
    b.advance(int(round(c1.BURN / c1.DT)))
    r = coupling.toarray().astype(np.float64) if coupling is not None else np.zeros((c1.N, c1.N))
    rs = r.sum(1)
    th = c1.UNIT["threshold"]
    acc = {w: [np.zeros(c1.N), np.zeros(c1.N), np.zeros(c1.N)] for w in WINDOWS}
    spikes = np.zeros(c1.N)
    for _ in range(int(round(SECONDS / c1.DT))):
        u = b.u.astype(np.float64)
        j = u @ r.T - u * rs
        for w, (n, s1, s2) in acc.items():
            m = (u >= th - w) & (u < th)
            n += m.sum(0)
            s1 += (j * m).sum(0)
            s2 += (j * j * m).sum(0)
        _, sp = b.advance(1, record=np.arange(c1.N))
        spikes += np.asarray(sp).reshape(-1, c1.N).sum(0)
    mean_kick = kick_hz * c1.KICK_MV * c1.UNIT["tau_m"]
    out = {"rate_hz": [round(float(x), 3) for x in spikes / (c1.RUNS * SECONDS)], "mean_kick_mv": round(mean_kick, 5),
           "biases_mv": [round(float(x), 5) for x in biases]}
    for w, (n, s1, s2) in acc.items():
        mj = s1 / np.maximum(n, 1)
        sd = np.sqrt(np.maximum(s2 / np.maximum(n, 1) - mj ** 2, 0.0))
        out[f"within {w} mV below threshold"] = {
            "share_of_time": [round(float(x), 4) for x in n / (c1.RUNS * SECONDS / c1.DT)],
            "junction_mean_mv": [round(float(x), 4) for x in mj], "junction_sd_mv": [round(float(x), 4) for x in sd],
            "net_margin_mv": [round(float(x), 4) for x in np.asarray(biases) + mean_kick + mj - th]}
    return out


def main() -> None:
    t0 = time.perf_counter()
    d2 = json.loads(Path(c1.OUT).with_name("dlm_splay_check2.json").read_text())
    d6 = json.loads(Path(c6.OUT).read_text())
    kick = d2["calibration"]["chosen"]["kick_hz"]
    coupling, _ = c6.junctions(d6["ratios"]["assumed_mn5"], c5.CC, False)
    out = {"question": __doc__, "noise_free_margin_mv_at_6.6hz": round(noise_free_margin(), 5), "conditions": {}}
    print("noise-free margin", out["noise_free_margin_mv_at_6.6hz"], flush=True)
    for k, (name, biases, junction) in enumerate([
            ("coupled (check 6's LIF, MN5 assumed)", np.array(d6["conditions"]["LIF, MN5 assumed"]["unit_biases_mv"]), coupling),
            ("uncoupled (check 2's bias)", np.full(c1.N, d2["calibration"]["chosen"]["bias_mv"]), None)]):
        out["conditions"][name] = measure(biases, kick, junction, SEED + k)
        print(name, json.dumps(out["conditions"][name]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
