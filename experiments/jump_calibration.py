"""Exploratory, not pre-registered: does one spike in each jump motor neuron make NeuroMechFly jump like a fly,
once the jump muscle's strength is calibrated on launch speed alone?

brainfly.jump drives the body with the jump motor neurons' (TTMn) spike times: a TTM twitch on each middle
leg's coxa-trochanter joint, 1 ms after its own side's TTMn spike, with a scripted tibia extension half as
strong 0.5 ms later. The research notes (escape_circuit.md, 1.5) give the recipe and the numbers to check it
against. This calibrates the one free number, the TTM's peak torque tau_max, once: one spike in each TTMn at
t = 0, and a 1-D search over tau_max (30-300 µN·mm) for a launch speed of 0.48 m/s, the centre of mass's mean
speed over the first 2 ms of flight in flies' escape takeoffs (Card & Dickinson 2008, J Exp Biol). Then,
without retuning, it reports the checks the notes list, against these ranges:
  - leg extension (first 1° of femur extension to takeoff): flies 3.33 ms (IQR 0.46); accept 2-5 ms.
  - takeoff after the giant fiber spike, which comes 0.4 ms before the TTMn spike (0.3 ms axon, 0.1 ms
    junction): about 7 ms (Fotowat et al. 2009, across preparations); accept 5-10 ms.
  - launch angle: "roughly 45° from the horizontal" (Card & Dickinson 2008). The notes give no spread;
    accept 30-60°.
  - pitch at takeoff: head up (39 of 43 flies started takeoff pitching head up); accept any head-up change
    from rest.
  - peak acceleration of the centre of mass (velocities over 0.5 ms), each axis: flies 112 m/s² vertical
    (IQR 47.8) and 107 m/s² horizontal; accept 60-160 m/s², about the median ± one IQR.
It also reports what the brain can send: a loom on one side fires only that side's TTMn (own-side pairing,
escape_circuit.md 1.2 point 5). Does the fly still take off on one leg, and how does it turn? And it reports
how much the answers depend on choices the notes don't fix: the timestep (halved and doubled), when the
other legs let go, the scripted tibia extension, and the braced coxa.

Ran: tau_max = 85.6 µN·mm (109 µN per leg) gives 0.48 m/s. 2 of the 6 checks pass, both on timing: takeoff 5.8 ms
after the giant fiber spike (flies: about 7) and a 4.1 ms leg extension (flies: 3.33 ms, IQR 0.46, so inside the
window but 1.7 IQRs slower than their median). The launch is too steep and slightly backward (79°), pitched head-down
(-4° at takeoff), 1.7 times too hard upward (190 m/s²) and 2.7 times too weak horizontally (40 m/s²). Without the
scripted tibia extension it still leaves at 81°, so that isn't what makes it steep. The timing pass depends on the
braced coxa: unbraced and recalibrated, takeoff comes 4.3 ms after the giant fiber spike, failing, while the pitch
turns head-up (+11°), passing. Halving or doubling the timestep, or when the other legs let go, changes little. One
TTMn alone gives a weak, tumbling launch (0.2 m/s at 44°, rolled 82° at takeoff).

    python experiments/jump_calibration.py         (writes experiments/jump_calibration.json, about 1 min)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from brainfly import jump as J

OUT = Path(__file__).with_suffix(".json")
TARGET = 0.48                     # m/s
BOTH = {"L": [0.0], "R": [0.0]}
SECONDS = 0.02
GRID = [30, 50, 75, 100, 150, 200, 300]
CHECKS = {  # summary key: (flies, low, high)
    "extension_ms": ("3.33 ms (IQR 0.46)", 2.0, 5.0),
    "takeoff_after_gf_ms": ("about 7 ms", 5.0, 10.0),
    "launch_angle_deg": ("about 45°", 30.0, 60.0),
    "pitch_at_takeoff_deg": ("head up in 39 of 43", 0.0, np.inf),
    "peak_vertical_acceleration_m_s2": ("112 m/s² (IQR 47.8)", 60.0, 160.0),
    "peak_horizontal_acceleration_m_s2": ("107 m/s²", 60.0, 160.0),
}


def speed(jump: J.Jump, tau: float, **kw) -> float:
    s = jump.run(BOTH, SECONDS, tau_max=tau, **kw)["summary"]
    return s.get("launch_speed_m_s", 0.0) if s["took_off"] else 0.0


def calibrate(jump: J.Jump, **kw) -> tuple[float, list]:
    """tau_max for TARGET, by Brent's method inside the first bracket of a coarse grid."""
    log = [(tau, speed(jump, tau, **kw)) for tau in GRID]
    k = next(i for i in range(len(log) - 1) if log[i][1] < TARGET <= log[i + 1][1])
    tau = brentq(lambda x: speed(jump, x, **kw) - TARGET, log[k][0], log[k + 1][0], xtol=0.05)
    return round(float(tau), 1), [[t, round(v, 4)] for t, v in log]


def kernel() -> dict:
    t = np.arange(0, 0.03, 1e-6)
    k = J.twitch(t)
    at = lambda f: float(t[np.argmax(k >= f)] * 1e3)
    return {"peak_ms": round(float(t[np.argmax(k)] * 1e3), 2), "rise_10_90_ms": round(at(0.9) - at(0.1), 2),
            "half_decay_after_onset_ms": round(float(t[np.flatnonzero(k >= 0.5)[-1]] * 1e3), 1),
            "two_spikes_1ms_apart_peak": round(float(J.activation(t, [0.0, 1e-3], delay=0.0).max()), 3)}


def main() -> None:
    start = time.time()
    jump = J.Jump()
    tau, log = calibrate(jump)
    print(f"tau_max {tau} µN·mm; grid {log}", flush=True)
    both = jump.run(BOTH, SECONDS, tau_max=tau)["summary"]
    checks = {}
    for key, (flies, lo, hi) in CHECKS.items():
        v = both.get(key)
        checks[key] = {"model": v, "flies": flies, "accept": [lo, hi if np.isfinite(hi) else None],
                       "pass": bool(v is not None and lo <= v <= hi)}
        print(f"{key}: {v} (flies {flies}; accept {lo}-{hi}) {'PASS' if checks[key]['pass'] else 'FAIL'}", flush=True)
    one_side = {s: jump.run({s: [0.0]}, SECONDS, tau_max=tau)["summary"] for s in "LR"}
    for s, v in one_side.items():
        print(f"{s} TTMn only: {v}", flush=True)

    keep = ["took_off", "takeoff_after_gf_ms", "extension_ms", "launch_speed_m_s", "launch_angle_deg",
            "peak_vertical_acceleration_m_s2", "peak_horizontal_acceleration_m_s2", "pitch_at_takeoff_deg"]
    brief = lambda s: {k: s.get(k) for k in keep}
    sens = {}
    for name, dt in (("timestep 0.025 ms (halved)", 2.5e-5), ("timestep 0.1 ms (doubled)", 1e-4)):
        sens[name] = brief(J.Jump(timestep=dt).run(BOTH, SECONDS, tau_max=tau)["summary"])
    for name, kw in (("other legs let go at force onset", {"release": 0.0}),
                     ("other legs let go 2 ms after force onset", {"release": 2e-3}),
                     ("no tibia extension", {"tibia": 0.0}),
                     ("coxa not braced (the demo servos)", {"brace": 1.0})):
        sens[name] = brief(jump.run(BOTH, SECONDS, tau_max=tau, **kw)["summary"])
    tau_loose, _ = calibrate(jump, brace=1.0)
    loose = jump.run(BOTH, SECONDS, tau_max=tau_loose, brace=1.0)["summary"]
    sens["coxa not braced, recalibrated"] = {"tau_max": tau_loose, **brief(loose)}
    for name, v in sens.items():
        print(f"{name}: {v}", flush=True)

    out = {"question": __doc__,
           "constants": {"ttm_delay_ms": J.TTM_DELAY * 1e3, "gf_to_ttmn_ms": J.GF_TO_TTMN * 1e3,
                         "twitch_rise_ms": J.RISE * 1e3, "twitch_decay_ms": J.DECAY * 1e3, "tibia": J.TIBIA,
                         "tibia_lag_ms": J.TIBIA_LAG * 1e3, "release_ms": J.RELEASE * 1e3, "brace": J.BRACE,
                         "torque_range": J.TORQUE_RANGE, "timestep_ms": jump.timestep * 1e3, "mass_mg": jump.mass * 1e3},
           "twitch": kernel(),
           "calibration": {"target_m_s": TARGET, "grid": log, "tau_max": tau,
                           "tau_max_as_force_per_leg_uN": round(tau / 0.784, 1)},
           "bilateral": both, "checks": checks,
           "passed": sum(c["pass"] for c in checks.values()), "of": len(checks),
           "unilateral": one_side, "sensitivity": sens, "seconds": round(time.time() - start, 1)}
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"wrote {OUT} ({out['passed']} of {out['of']} checks pass; {out['seconds']} s)")


if __name__ == "__main__":
    main()
