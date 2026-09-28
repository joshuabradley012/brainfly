"""Exploratory, not pre-registered: does FlyMimic's front-leg tibia flexor push a force probe as hard as a fly's?

Rung 7 drives a musculoskeletal leg from the connectome's motor neurons, and the ladder asks that its force per
spike and twitch time match flies'. The only such data for a Drosophila leg muscle are Azevedo et al. 2020's
(research_notes/Embodied fly connectome simulation/leg_twitch_data.md). The femur is glued, the tibia starts about
90 degrees to the femur, and it pushes a probe 417 um from the joint. One fast tibia flexor motor neuron spike gives
about 9 uN at that probe, 10 of them about 30 uN, and the whole muscle close to 100 uN. FlyGym 2.1 ships FlyMimic's
left front leg (Ozdil et al. 2025), 15 Hill-type muscles with maximum forces from X-ray cross-sections. Before its
muscles are driven by spikes, this asks how hard they can push at all.
Setup: FlyMimic's model as FlyGym loads it; every left front leg joint held but the femur-tibia joint. The probe is
flies' (k = 0.2234 uN/um, 0.1702 mg, drag 0.14 g/s), 417 um from the joint, as an equivalent spring, inertia and
damping on the joint (small angles). The tibia starts at the probe's rest angle, 60, 90 or 120 degrees from straight.
Measured: the probe force (k times its deflection) after 100 ms of full activation of the tibia flexor, then of the
extensor (every other muscle at FlyMimic's floor, 1e-4); the muscles' moment arms at 90 degrees; and what maximum
force the flexor would need to reach flies' 100 uN.
Ran: no, by a factor of about 40. FlyMimic's tibia flexor pushes the probe with 2.0-2.3 uN from 60 to 120 degrees: a
fortieth of a fly's whole muscle and a quarter of one fast motor neuron spike. Its 68 uN maximum force acts through a
15 um moment arm; to push 100 uN it would need about 3 mN. The extensor (304 uN through 35 um) pushes 17-28 uN.

    python experiments/leg_probe.py            (writes experiments/leg_probe.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import mujoco as mj
import numpy as np
from flygym.compose.fly import musculoskeletal as ms

OUT = Path(__file__).with_suffix(".json")
XML = ms.MUSCULOSKELETAL_MODEL_DIR / "best_combined_arm_damping_stiff_cvt3.xml"
K, MASS, DRAG, ARM = 223.4, 1.702e-4, 0.14, 0.417        # probe: uN/mm, g, g/s; lever arm, mm (Azevedo et al. 2020)
FLY_MAX, FLY_FAST = 100.0, 9.0                            # uN: the whole muscle, one fast motor neuron spike
FTI = "joint_LFTibia_pitch"
MUSCLES = {"tibia flexor": "LFTibia_flex_93434", "tibia extensor": "LFTibia_extensor_93932"}
ANGLES = (60, 90, 120)                                    # degrees from a straight tibia (FlyMimic's FTi pitch)
SECONDS, FLOOR = 0.1, 1e-4


def leg(angle: float) -> tuple[mj.MjModel, mj.MjData]:
    """FlyMimic with every left front leg joint held but the femur-tibia joint, which carries the probe."""
    spec = ms._load_mjcf(XML)
    m = spec.compile()
    for j in spec.joints:
        if j.name.startswith("joint_LF") and j.name != FTI:
            v = m.qpos0[m.jnt_qposadr[m.joint(j.name).id]]
            j.limited, j.range = True, [v - 1e-4, v + 1e-4]
    fti = next(j for j in spec.joints if j.name == FTI)
    fti.stiffness = fti.stiffness + K * ARM ** 2
    fti.armature = fti.armature + MASS * ARM ** 2
    fti.damping = fti.damping + DRAG * ARM ** 2
    fti.springref = np.radians(angle)
    m = spec.compile()
    d = mj.MjData(m)
    d.qpos[m.jnt_qposadr[m.joint(FTI).id]] = np.radians(angle)
    return m, d


def push(angle: float, muscle: str) -> dict:
    """Full activation of one muscle from rest: the probe force over time (uN, positive when flexing)."""
    m, d = leg(angle)
    q = m.jnt_qposadr[m.joint(FTI).id]
    d.ctrl[:] = FLOOR
    for _ in range(int(0.05 / m.opt.timestep)):                   # settle with every muscle at the floor
        mj.mj_step(m, d)
    rest = d.qpos[q]
    d.ctrl[m.actuator(muscle).id] = 1.0
    force = []
    for _ in range(int(SECONDS / m.opt.timestep)):
        mj.mj_step(m, d)
        force.append(K * ARM * (d.qpos[q] - rest))
    force = np.array(force)
    return {"force_uN": round(float(force[-1]), 2), "peak_uN": round(float(np.abs(force).max()), 2),
            "ms_to_half": round(float(np.argmax(np.abs(force) >= 0.5 * abs(force[-1])) * m.opt.timestep * 1e3), 2)}


def moment_arms(angle: float = 90.0) -> dict:
    """Each tibia muscle's moment arm (mm, positive for flexion), from its tendon length's change with the joint."""
    m, d = leg(angle)
    q = m.jnt_qposadr[m.joint(FTI).id]
    arms = {}
    for name, muscle in MUSCLES.items():
        t = m.actuator_trnid[m.actuator(muscle).id][0]
        lengths = []
        for dq in (0.0, 1e-4):
            d.qpos[q] = np.radians(angle) + dq
            mj.mj_forward(m, d)
            lengths.append(d.ten_length[t])
        arms[name] = round(float(-(lengths[1] - lengths[0]) / 1e-4), 4)
    return arms


def main() -> None:
    m, _ = leg(90)
    f0 = {name: round(float(m.actuator_gainprm[m.actuator(mus).id][2]), 1) for name, mus in MUSCLES.items()}
    out = {"question": __doc__, "max_force_uN": f0, "moment_arm_mm_at_90": moment_arms(), "pushes": {}}
    for name, muscle in MUSCLES.items():
        out["pushes"][name] = {str(a): push(a, muscle) for a in ANGLES}
        print(name, json.dumps(out["pushes"][name]), flush=True)
    flex = out["pushes"]["tibia flexor"]["90"]["force_uN"]
    out["flexor_vs_fly"] = {"of_whole_muscle": round(flex / FLY_MAX, 3), "of_one_fast_spike": round(flex / FLY_FAST, 3),
                            "max_force_needed_uN": round(f0["tibia flexor"] * FLY_MAX / flex, 0)}
    print(json.dumps({k: out[k] for k in ("max_force_uN", "moment_arm_mm_at_90", "flexor_vs_fly")}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
