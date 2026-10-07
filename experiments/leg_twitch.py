"""Exploratory, not pre-registered: with its muscles scaled to flies' maximum force and a motor neuron spike set to
flies' force per spike, does FlyMimic's tibia flexor twitch like a fly's?

leg_probe.py: FlyMimic's tibia flexor pushes a fly's force probe 40 times more weakly than a fly's (2.3 against about
100 uN). Azevedo et al. 2020 measured a fly's front-leg tibia flexor against that probe
(research_notes/Embodied fly connectome simulation/leg_twitch_data.md). One fast motor neuron spike gives about 9 uN
(5.4-15.4), reaching half its peak about 8.5 ms after the spike (7.7-9.7 across cells), peaking at about 17-23 ms and
falling to half about 12-16 ms after the peak. Two spikes 12 ms apart give 1.4-1.6 times one; the whole muscle, close
to 100 uN.
Setup: leg_probe.leg(90): FlyMimic's left front leg, every joint held but the femur-tibia joint, which carries the
probe; every other muscle at FlyMimic's floor (1e-4). Two numbers are fitted:
  - every muscle's maximum force times one factor, so that full activation of the tibia flexor pushes the probe with
    100 uN after 100 ms;
  - a spike, a control pulse of 1 lasting long enough that one spike gives a 9 uN peak.
Measured, as predictions:
  - the single-spike twitch's time to half its peak, time to peak, and half-decay after the peak, from the pulse's
    start. A fly's are timed from the somatic spike, so they include the motor neuron's conduction and the synapse,
    a few ms.
  - the ratio of two spikes 12 ms apart to one;
  - the peak for 1 to 17 spikes at 80 Hz. A fly's saturates near 28-30 uN, which the authors put down to fatigue,
    and this model has none.
FlyMimic's activation and deactivation time constants are reported.

Ran: no, and it couldn't. FlyMimic's muscle activation and deactivation time constants are 0.1 and 0.4 ms, a hundred
times faster than MuJoCo's defaults and than a fly's twitch, so a twitch's shape comes almost entirely from the probe.
Full activation reaches 100 uN only with every maximum force times 607, not the 44 leg_probe.py's small-deflection
estimate gave. 100 uN deflects the probe about 450 um, folding the tibia some 60 deg, where the flexor's moment arm has
shrunk from 15 to about 9 um. A spike set to give 9 uN (a 1.4 ms pulse) then twitches 20 times too fast: half its peak
at 0.4 ms (flies: 7.7-9.7), the peak at 3.3 ms (17-23), half gone 6.6 ms later (12-16). Two spikes 12 ms apart sum to
1.17 times one (1.4-1.6), and 80 Hz trains saturate at 11.9 uN (flies: 28-30). Matching flies' twitches in FlyMimic
means fitting its activation dynamics, so rung 7's force-per-spike and twitch-time criteria would be fitted, not
tested.

    python experiments/leg_twitch.py           (writes experiments/leg_twitch.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import mujoco as mj
import numpy as np

import leg_probe as lp

OUT = Path(__file__).with_suffix(".json")
FLEXOR = lp.MUSCLES["tibia flexor"]
FLY = {"max_uN": 100.0, "spike_uN": 9.0, "half_ms": (7.7, 9.7), "peak_ms": (17.0, 23.0), "half_decay_ms": (12.0, 16.0),
       "two_spike_ratio": (1.4, 1.6), "isi_ms": 12.0}
SECONDS = 0.15


def leg(scale: float):
    """leg_probe.leg(90) with every muscle's maximum force times `scale`, settled with every muscle at the floor."""
    m, d = lp.leg(90)
    muscles = m.actuator_dyntype == mj.mjtDyn.mjDYN_MUSCLE
    m.actuator_gainprm[muscles, 2] *= scale
    m.actuator_biasprm[muscles, 2] *= scale
    q = m.jnt_qposadr[m.joint(lp.FTI).id]
    d.ctrl[:] = lp.FLOOR
    for _ in range(int(0.05 / m.opt.timestep)):
        mj.mj_step(m, d)
    return m, d, q, d.qpos[q]


def force_trace(scale: float, pulses: list[tuple[float, float]], seconds: float = SECONDS) -> np.ndarray:
    """The probe force (uN, positive when flexing) every step for `seconds`, the flexor's control 1 during each
    (start, duration) pulse in seconds and at the floor otherwise."""
    m, d, q, rest = leg(scale)
    a = m.actuator(FLEXOR).id
    dt = m.opt.timestep
    out = np.zeros(int(round(seconds / dt)))
    for k in range(len(out)):
        t = k * dt
        d.ctrl[a] = 1.0 if any(s <= t < s + w for s, w in pulses) else lp.FLOOR
        mj.mj_step(m, d)
        out[k] = lp.K * lp.ARM * (d.qpos[q] - rest)
    return out


def bisect(f, target: float, lo: float, hi: float, n: int = 40) -> float:
    """x in (lo, hi) with f(x) = target, f increasing."""
    for _ in range(n):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if f(mid) < target else (lo, mid)
    return float(np.sqrt(lo * hi))


def shape(trace: np.ndarray, dt: float) -> dict:
    k = int(np.argmax(trace))
    peak = trace[k]
    half = int(np.argmax(trace >= 0.5 * peak))
    after = np.flatnonzero(trace[k:] <= 0.5 * peak)
    return {"peak_uN": round(float(peak), 2), "half_ms": round(half * dt * 1e3, 2), "peak_ms": round(k * dt * 1e3, 2),
            "half_decay_ms": round(float(after[0]) * dt * 1e3, 2) if len(after) else None}


def main() -> None:
    m, _, _, _ = leg(1.0)
    dt = m.opt.timestep
    a = m.actuator(FLEXOR).id
    out = {"question": __doc__, "timestep_ms": dt * 1e3,
           "activation_time_constants_ms": [round(float(x) * 1e3, 1) for x in m.actuator_dynprm[a][:2]],
           "flexor_max_force_uN": round(float(m.actuator_gainprm[a][2]), 1)}
    full = lambda s: force_trace(s, [(0.0, 0.1)], 0.1)[-1]
    scale = bisect(full, FLY["max_uN"], 1.0, 1000.0)
    out["scale"] = round(scale, 3)
    print("scale", round(scale, 2), "->", round(full(scale), 2), "uN at full activation", flush=True)
    one = lambda w: force_trace(scale, [(0.0, w)]).max()
    width = bisect(one, FLY["spike_uN"], dt, 0.02)
    out["spike_pulse_ms"] = round(width * 1e3, 3)
    single = force_trace(scale, [(0.0, width)])
    out["single_spike"] = shape(single, dt)
    print("spike pulse", round(width * 1e3, 3), "ms ->", json.dumps(out["single_spike"]), flush=True)
    two = force_trace(scale, [(0.0, width), (FLY["isi_ms"] / 1e3, width)])
    out["two_spike_ratio"] = round(float(two.max() / single.max()), 3)
    out["train_80Hz"] = {n: round(float(force_trace(scale, [(i / 80.0, width) for i in range(n)], 0.4).max()), 2)
                         for n in (1, 2, 3, 5, 10, 17)}
    out["fly"] = FLY
    print("two spikes:", out["two_spike_ratio"], "| 80 Hz trains:", json.dumps(out["train_80Hz"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
