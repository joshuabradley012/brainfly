"""Exploratory, not pre-registered: with its muscles scaled to flies' maximum force and a motor neuron spike set to
flies' force per spike, does FlyMimic's tibia flexor twitch like a fly's?

leg_probe.py: FlyMimic's tibia flexor pushes a fly's force probe 40 times more weakly than a fly's (2.3 against about
100 uN). Azevedo et al. 2020 measured a fly's front-leg tibia flexor against that probe
(research_notes/Embodied fly connectome simulation/leg_twitch_data.md). One fast motor neuron spike gives about 9 uN
(5.4-15.4), reaching half its peak about 8.5 ms after the spike (7.7-9.7 across cells). Read from example traces (the
paper reports neither): the peak at about 17-23 ms, and half the force gone about 12-16 ms after it. Two spikes give
1.4-1.6 times one (across cells, at intervals not stated; about 12 ms apart in the example shown); the whole muscle,
close to 100 uN.
Setup: leg_probe.leg(90): FlyMimic's left front leg, every joint held by joint limits but the femur-tibia joint,
which carries the probe; every other muscle at FlyMimic's floor (1e-4). Two numbers are fitted:
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
FlyMimic's activation and deactivation time constants are reported. In the model FlyGym ships they are 0.1 and 0.4
ms, though Ozdil et al. say they used OpenSim's defaults (10 and 40 ms, MuJoCo's too). Added 2026-10-09, after a
review: the same run with those time constants, and with the held joints held stiffly (limits with a 0.2 ms time
constant instead of MuJoCo's 20 ms); and what the scale works against (the leg at rest and fully flexed, and the
flexor scaled alone).

Ran: as shipped, no. Full activation reaches 100 uN only with every maximum force times 607, not the 44 leg_probe.py's
small-deflection estimate gave, mostly because scaling every muscle also scales the tibia extensor's passive tension.
It holds the resting tibia at 72 degrees rather than 90, and with 100 uN on the probe (the tibia at 133 degrees) it
cancels 417 of the flexor's 486 uN mm. The flexor scaled alone can't reach 100 uN: it folds the tibia toward 148
degrees, where its moment arm (15 um at 90 degrees) vanishes, and tops out near 92 uN (at 1000 times; 3000 times runs
unstable). A spike set to give 9 uN (a 1.4 ms pulse) reaches
half its peak 20 times sooner than a fly's (0.4 ms against 7.7-9.7) and peaks 5-7 times sooner (3.3 ms against
17-23), and half of it is gone 6.6 ms after the peak (12-16). Two spikes 12 ms apart sum to 1.17 times one (1.4-1.6),
and 80 Hz trains saturate at 11.9 uN (flies: 28-30). At this scale the leg's own passive stiffness about the joint
(123 uN mm/rad) exceeds the probe's (39), so the leg as much as the probe shapes the twitch. The joints meant to be
held give way at this scale (one by 96 degrees), but held stiffly the results barely move: a scale of 605, 0.4, 3.3
and 6.9 ms, and 1.19 times.
With the paper's stated time constants, mostly yes: a scale of 614, and a 0.1 ms pulse (the shortest the 0.1 ms step
allows) gives 9.0 uN, reaching half its peak at 6.1 ms (7.7-9.7, which include a few ms of conduction) and peaking at
17.1 ms (17-23). Two spikes sum to 1.61 times one (1.4-1.6), and 80 Hz trains level off at 26.9 uN (28-30) without
any fatigue. But it relaxes about four times too slowly: half of it is gone 58 ms after the peak (12-16). So FlyMimic's
own stated parameters predict a fly's twitch rise, summation and plateau but not its relaxation, and the shipped ones
predict none of them.

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
PAPER = (0.01, 0.04)        # s: the activation and deactivation time constants Ozdil et al. state (OpenSim's defaults)
HOLD = 2e-4                 # s: a stiff hold's time constant (MuJoCo's default, 0.02, gives way at large forces)


def leg(scale: float, time_constants: tuple | None = None, hold: float | None = None):
    """leg_probe.leg(90, hold) with every muscle's maximum force times `scale` (and its activation and deactivation
    time constants, s, if given), settled with every muscle at the floor."""
    m, d = lp.leg(90, hold)
    muscles = m.actuator_dyntype == mj.mjtDyn.mjDYN_MUSCLE
    m.actuator_gainprm[muscles, 2] *= scale
    m.actuator_biasprm[muscles, 2] *= scale
    if time_constants is not None:
        m.actuator_dynprm[muscles, 0], m.actuator_dynprm[muscles, 1] = time_constants
    q = m.jnt_qposadr[m.joint(lp.FTI).id]
    d.ctrl[:] = lp.FLOOR
    for _ in range(int(0.05 / m.opt.timestep)):
        mj.mj_step(m, d)
    return m, d, q, d.qpos[q]


def force_trace(scale: float, pulses: list[tuple[float, float]], seconds: float = SECONDS,
                time_constants: tuple | None = None, hold: float | None = None) -> np.ndarray:
    """The probe force (uN, positive when flexing) every step for `seconds`, the flexor's control 1 during each
    (start, duration) pulse in seconds and at the floor otherwise."""
    m, d, q, rest = leg(scale, time_constants, hold)
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


def twitch(dt: float, time_constants: tuple | None = None, hold: float | None = None) -> dict:
    """The force scale, the spike's pulse and the measures, with these time constants (FlyMimic's own if None)."""
    trace = lambda scale, pulses, seconds=SECONDS: force_trace(scale, pulses, seconds, time_constants, hold)
    out = {}
    full = lambda s: trace(s, [(0.0, 0.1)], 0.1)[-1]
    scale = bisect(full, FLY["max_uN"], 1.0, 1000.0)
    out["scale"] = round(scale, 3)
    print("scale", round(scale, 2), "->", round(full(scale), 2), "uN at full activation", flush=True)
    one = lambda w: trace(scale, [(0.0, w)]).max()
    width = bisect(one, FLY["spike_uN"], dt, 0.02)
    out["spike_pulse_ms"] = round(width * 1e3, 3)
    single = trace(scale, [(0.0, width)])
    out["single_spike"] = shape(single, dt)
    print("spike pulse", round(width * 1e3, 3), "ms ->", json.dumps(out["single_spike"]), flush=True)
    two = trace(scale, [(0.0, width), (FLY["isi_ms"] / 1e3, width)])
    out["two_spike_ratio"] = round(float(two.max() / single.max()), 3)
    out["train_80Hz"] = {n: round(float(trace(scale, [(i / 80.0, width) for i in range(n)], 0.4).max()), 2)
                         for n in (1, 2, 3, 5, 10, 17)}
    print("two spikes:", out["two_spike_ratio"], "| 80 Hz trains:", json.dumps(out["train_80Hz"]), flush=True)
    return out


def mechanics(scale: float) -> dict:
    """What the scale works against: the leg at rest and after 100 ms of the flexor's full activation, at `scale`."""
    m, d, q, rest = leg(scale)
    dof = m.jnt_dofadr[m.joint(lp.FTI).id]
    held = [j for j in range(m.njnt) if m.joint(j).name.startswith("joint_LF") and m.joint(j).name != lp.FTI]
    moved = max(abs(np.degrees(d.qpos[m.jnt_qposadr[j]] - m.qpos0[m.jnt_qposadr[j]])) for j in held)

    def probe(x: float, what: str) -> np.ndarray:
        """The muscles' torques (qfrc_actuator) or lengths with the tibia moved to x."""
        e = mj.MjData(m)
        e.qpos[:], e.act[:], e.ctrl[:] = d.qpos, d.act, d.ctrl
        e.qpos[q] = x
        mj.mj_forward(m, e)
        return e.qfrc_actuator[dof] if what == "torque" else e.actuator_length.copy()
    step = np.radians(1.0)
    stiffness = -(probe(rest + step, "torque") - probe(rest - step, "torque")) / (2 * step)
    a = m.actuator(FLEXOR).id
    for _ in range(int(round(0.1 / m.opt.timestep))):
        d.ctrl[a] = 1.0
        mj.mj_step(m, d)
    arm = -(probe(d.qpos[q] + 1e-5, "length") - probe(d.qpos[q] - 1e-5, "length")) / 2e-5      # mm, + flexing
    torque = {name: round(float(-arm[m.actuator(x).id] * d.actuator_force[m.actuator(x).id]), 1) for name, x in lp.MUSCLES.items()}
    return {"tibia_at_rest_deg": round(float(np.degrees(rest)), 1), "held_joints_moved_deg": round(float(moved), 1),
            "passive_stiffness_uN_mm_per_rad": round(float(stiffness), 1),
            "probe_stiffness_uN_mm_per_rad": round(lp.K * lp.ARM ** 2, 1),
            "full_flexor": {"tibia_deg": round(float(np.degrees(d.qpos[q])), 1),
                            "probe_uN": round(float(lp.K * lp.ARM * (d.qpos[q] - rest)), 1),
                            "flexor_arm_um": round(float(arm[a]) * 1e3, 1), "torque_uN_mm": torque}}


def flexor_only(scale: float) -> dict:
    """The probe force after 100 ms of full activation with only the flexor's maximum force times `scale`."""
    m, d = lp.leg(90)
    a = m.actuator(FLEXOR).id
    m.actuator_gainprm[a, 2] *= scale
    m.actuator_biasprm[a, 2] *= scale
    q = m.jnt_qposadr[m.joint(lp.FTI).id]
    d.ctrl[:] = lp.FLOOR
    for _ in range(int(0.05 / m.opt.timestep)):
        mj.mj_step(m, d)
    rest = d.qpos[q]
    for _ in range(int(round(0.1 / m.opt.timestep))):
        d.ctrl[a] = 1.0
        mj.mj_step(m, d)
    return {"probe_uN": round(float(lp.K * lp.ARM * (d.qpos[q] - rest)), 1), "tibia_deg": round(float(np.degrees(d.qpos[q])), 1),
            "unstable": bool(d.warning[mj.mjtWarning.mjWARN_BADQACC].number)}


def main() -> None:
    m, _, _, _ = leg(1.0)
    dt = m.opt.timestep
    a = m.actuator(FLEXOR).id
    out = {"question": __doc__, "timestep_ms": dt * 1e3,
           "activation_time_constants_ms": [round(float(x) * 1e3, 1) for x in m.actuator_dynprm[a][:2]],
           "flexor_max_force_uN": round(float(m.actuator_gainprm[a][2]), 1)}
    out.update(twitch(dt))
    out["mechanics"] = mechanics(out["scale"])
    out["flexor_only"] = {s: flexor_only(s) for s in (100, 300, 1000, 3000)}
    out["flexor_arm_um_by_angle"] = {a: round(lp.moment_arms(a)["tibia flexor"] * 1e3, 1) for a in (90, 120, 140, 145, 148)}
    print(json.dumps({k: out[k] for k in ("mechanics", "flexor_only", "flexor_arm_um_by_angle")}), flush=True)
    out["stiff_holds"] = {"hold_time_constant_ms": HOLD * 1e3, **twitch(dt, hold=HOLD)}
    out["paper_time_constants"] = {"activation_time_constants_ms": [x * 1e3 for x in PAPER], **twitch(dt, PAPER)}
    out["fly"] = FLY
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
