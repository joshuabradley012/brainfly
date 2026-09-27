"""The escape jump in the body: NeuroMechFly pushed off the ground by its jump muscles, from the spike times
of the jump motor neurons (TTMn).

The body is body.py's: NeuroMechFly v2 in FlyGym 2.1 on flat ground, standing in the walking controller's
default pose with adhesion on, its 42 leg joints held by the demo position actuators (kp 45 µN·mm/rad,
±65 µN·mm). Units are mm, g and s, so force is in µN and torque in µN·mm; the fly weighs 1.02 mg.
The jump follows research_notes/Embodied fly connectome simulation/escape_circuit.md, section 1.5:

- TTM: a motor on each middle leg's coxa-trochanter pitch (lm_ and rm_coxa-..._trochanterfemur-pitch, range
  ±250 µN·mm). An increase depresses the femur: checked by forward kinematics, +60° from the standing pose
  (-97°) lowers the foot 0.78 mm relative to the thorax, on both sides. Torque tau_max * a(t) on the TTMn's
  own side.
- a(t) = sum over the TTMn's spikes of a twitch k(t - t_spike - d), capped at 1. d = 1 ms, both halves
  assumed: 0.5 ms from TTMn spike to the TTM's muscle potential (thoracic stimulation gives 0.55-0.84 ms;
  Thomas & Wyman 1984, Kadas et al. 2019) and 0.5 ms from muscle potential to force (unmeasured). k rises
  with time constant 1.3 ms (Kolomenskiy et al. 2016's ramp, fitted to Zumstein et al. 2004's force slope)
  and decays with 9 ms (Zumstein 2004 via Elliott et al. 2007: 8-10 ms, a twitch of about 20 ms), scaled
  to peak 1, reached 2.7 ms after onset.
- The tibia extensor, SCRIPTED: its motor neuron (the TLMn) isn't identified in MaleCNS yet. Each side's
  femur-tibia pitch gets -tibia * tau_max * a(t - 0.5 ms), toward extension. FTi pitch is the femur-tibia
  angle (0 is a straight leg), so extension is a decrease.
- Adhesion: off for a middle leg when its TTM force starts, and for the other legs `release` (1 ms) after
  the first force onset, a fixed time. Takeoff can't release them: they would hold the fly down.
- The servos: from its force onset, a pushing leg's coxa-trochanter and femur-tibia servos hold their
  targets at the current angles, so they exert no torque. The same leg's other servo joints (coxa yaw,
  pitch and roll, trochanter roll, tibia-tarsus pitch) are braced: their gain and force range are
  multiplied by `brace` (20). The push loads the coxa with up to 65 µN·mm. The demo servos, at 45 µN·mm
  per radian, let it turn 48° before takeoff, so the femur sweeps the leg round instead of lifting the
  body, and the jump needs 2.5 times the torque. Braced, the coxa stays within 4°. In the fly the TTM pulls
  on the thorax itself, and the coxal muscles hold the coxa. Bracing 10x to 40x moves launch speed and
  angle by under 1%. Braced servos are stable at 0.1 ms steps up to about 30x.

Two additions to FlyGym 2.1, which has no joint limits: end stops on the middle legs' coxa-trochanter pitch
(at most 0°, the femur in line with the coxa) and femur-tibia pitch (at least 0°, a straight tibia).
Without them the twitch spins the legs through full turns after takeoff and bends the tibia backwards.
The stops are as stiff as FlyGym's ground contact (solref 0.2 ms).

Physics runs at 0.05 ms steps, from a standing state settled once and restored before each run. Halving
the step moves the calibrated jump's launch speed by 0.4%, takeoff by 0.05 ms and pitch at takeoff by
0.01° (experiments/jump_calibration.json). At the brain's 0.1 ms step the launch is within 1%, but pitch
at takeoff isn't converged (-0.3° against -4.1°). To couple it to the brain, take two physics steps per
brain step.

    jump = Jump()
    record = jump.run({"L": [0.0], "R": [0.0]}, seconds=0.02)
    record["summary"]      # takeoff time, launch speed and angle, peak acceleration, pitch at takeoff...
"""
from __future__ import annotations

import numpy as np

TTM_DELAY = 1.0e-3                 # s, TTMn spike to TTM force onset (0.5 ms + 0.5 ms, both assumed)
GF_TO_TTMN = 0.4e-3                # s, GF spike in the brain to TTMn spike: 0.3 ms axon + 0.1 ms junction
RISE, DECAY = 1.3e-3, 9.0e-3       # s, the twitch's rise and decay time constants
TIBIA, TIBIA_LAG = 0.5, 0.5e-3     # scripted tibia extensor: fraction of tau_max, lag behind the TTM
TORQUE_RANGE = 250.0               # µN·mm
RELEASE = 1.0e-3                   # s after the first force onset: the other legs let go
BRACE = 20.0                       # a pushing leg's other servos are this much stiffer during the push
STOP_SOLREF = (2e-4, 1.0)          # end stops as stiff as FlyGym's ground contact
TAU_MAX = 85.6                     # µN·mm, calibrated once on launch speed (experiments/jump_calibration.py)
LEGS = ["lf", "lm", "lh", "rf", "rm", "rh"]
MIDDLE_JOINTS = ["c_thorax-{s}m_coxa-yaw", "c_thorax-{s}m_coxa-pitch", "c_thorax-{s}m_coxa-roll",
                 "{s}m_coxa-{s}m_trochanterfemur-pitch", "{s}m_coxa-{s}m_trochanterfemur-roll",
                 "{s}m_trochanterfemur-{s}m_tibia-pitch", "{s}m_tibia-{s}m_tarsus1-pitch"]

_PEAK_AT = RISE * np.log(1 + DECAY / RISE)
_PEAK = (1 - np.exp(-_PEAK_AT / RISE)) * np.exp(-_PEAK_AT / DECAY)


def twitch(t):
    """The TTM's activation after one spike, t seconds after force onset: 0 before, peak 1."""
    t = np.maximum(np.asarray(t, float), 0.0)
    return (1 - np.exp(-t / RISE)) * np.exp(-t / DECAY) / _PEAK


def activation(t, spikes, delay: float = TTM_DELAY):
    """a(t) from one TTMn's spike times (s): its twitches summed, capped at 1."""
    t = np.asarray(t, float)
    total = sum((twitch(t - s - delay) for s in spikes), np.zeros_like(t))
    return np.minimum(total, 1.0)


def angles(xmat) -> tuple[float, float, float]:
    """Body pitch (head up +), roll (left side up +) and yaw (counterclockwise from above +), degrees."""
    R = np.asarray(xmat).reshape(3, 3)
    return (float(np.degrees(np.arcsin(np.clip(R[2, 0], -1, 1)))), float(np.degrees(np.arctan2(R[2, 1], R[2, 2]))),
            float(np.degrees(np.arctan2(R[1, 0], R[0, 0]))))


class Jump:
    """NeuroMechFly standing on flat ground with a TTM on each middle leg, settled once (`settle` seconds
    at `timestep`) and restored to that state before every run."""

    def __init__(self, timestep: float = 5e-5, settle: float = 0.1):
        import mujoco as mj
        from flygym import Simulation
        from flygym.anatomy import ContactBodiesPreset
        from flygym.compose import ActuatorType, FlatGroundWorld
        from flygym.utils.math import Rotation3D
        from flygym_demo.complex_terrain import PreprogrammedSteps, make_locomotion_fly

        self.fly = fly = make_locomotion_fly(name="nmf", add_adhesion=True, colorize=True)
        joints = {j.name: j for j in fly.get_jointdofs_order()}
        ctr = [joints[f"{s}m_coxa-{s}m_trochanterfemur-pitch"] for s in "lr"]
        fti = [joints[f"{s}m_trochanterfemur-{s}m_tibia-pitch"] for s in "lr"]
        fly.add_actuators(ctr + fti, ActuatorType.MOTOR, forcerange=(-TORQUE_RANGE, TORQUE_RANGE))
        for dofs, lo, hi in ((ctr, -np.pi, 0.0), (fti, 0.0, np.pi)):
            for j in dofs:
                joint = fly.jointdof_to_mjcfjoint[j]
                joint.range, joint.limited, joint.solref_limit = [lo, hi], mj.mjtLimited.mjLIMITED_TRUE, list(STOP_SOLREF)
        world = FlatGroundWorld()
        world.add_fly(fly, [0, 0, 0.8], Rotation3D("quat", [1, 0, 0, 0]),
                      bodysegs_with_ground_contact=ContactBodiesPreset("tibia_tarsus_only"))
        self.sim = Simulation(world, timestep=timestep)
        self.timestep = timestep
        m = self.model = self.sim.mj_model
        self._mj, self._position, self._motor = mj, ActuatorType.POSITION, ActuatorType.MOTOR

        servo = [j.name for j in fly.get_actuated_jointdofs_order("position")]
        self.stand = PreprogrammedSteps().default_pose_by_dof_order(fly.get_actuated_jointdofs_order("position"))
        qadr = lambda name: int(m.jnt_qposadr[mj.mj_name2id(m, mj.mjtObj.mjOBJ_JOINT, f"nmf/{name}")])
        self.joint_names = {s: [n.format(s=s.lower()) for n in MIDDLE_JOINTS] for s in "LR"}
        self._qadr = {s: [qadr(n) for n in self.joint_names[s]] for s in "LR"}
        # per side: the servos released during the push (CTr and FTi pitch) and those braced (the rest)
        self._limp = {s: [servo.index(self.joint_names[s][i]) for i in (3, 5)] for s in "LR"}
        self._limp_q = {s: [self._qadr[s][i] for i in (3, 5)] for s in "LR"}
        ids = self.sim._intern_actuatorids_by_type_by_fly[ActuatorType.POSITION]["nmf"]
        self._braced = {s: [int(ids[servo.index(self.joint_names[s][i])]) for i in (0, 1, 2, 4, 6)] for s in "LR"}
        self._servo_params = (m.actuator_gainprm.copy(), m.actuator_biasprm.copy(), m.actuator_forcerange.copy())

        # MuJoCo fuses the head into the thorax (no joint between them), so c_head has no body of its own:
        # FlyGym's get_body_positions reads id -1 for it, the last body. Keep the segments that are bodies;
        # every geom's pose, the head's too, follows from its body's.
        body = lambda seg: mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, f"nmf/{seg}")
        self.segments = [b.name for b in fly.get_bodysegs_order() if body(b.name) >= 0]
        self._bodies = np.array([body(b) for b in self.segments])
        self._thorax = int(self._bodies[0])
        self.mass = float(m.body_subtreemass[self._thorax])

        self.sim.reset()
        self.sim.set_actuator_inputs("nmf", ActuatorType.POSITION, self.stand)
        self.sim.set_actuator_inputs("nmf", ActuatorType.MOTOR, np.zeros(4))
        self.sim.set_leg_adhesion_states("nmf", np.ones(6))
        self.sim.warmup(settle)
        self._spec = mj.mjtState.mjSTATE_INTEGRATION
        self._rest = np.empty(mj.mj_stateSize(m, self._spec))
        mj.mj_getState(m, self.sim.mj_data, self._rest, self._spec)

    def _brace(self, side: str, factor: float) -> None:
        m = self.model
        gain, bias, frc = self._servo_params
        for a in self._braced[side]:
            m.actuator_gainprm[a, 0], m.actuator_biasprm[a, 1] = gain[a, 0] * factor, bias[a, 1] * factor
            m.actuator_forcerange[a] = frc[a] * factor

    def run(self, ttmn_spikes: dict, seconds: float = 0.02, tau_max: float = TAU_MAX, tibia: float = TIBIA,
            release: float = RELEASE, brace: float = BRACE) -> dict:
        """The fly from rest (t = 0) for `seconds`, with each TTMn's spike times ({"L": [s...], "R": [...]},
        seconds from the start). Returns the state at every physics step and a `summary` (see summarize)."""
        mj, m, d, sim = self._mj, self.model, self.sim.mj_data, self.sim
        mj.mj_setState(m, d, self._rest, self._spec)
        for s in "LR":
            self._brace(s, 1.0)
        mj.mj_forward(m, d)
        spikes = {s: sorted(float(x) for x in ttmn_spikes.get(s, [])) for s in "LR"}
        onset = {s: spikes[s][0] + TTM_DELAY if spikes[s] else np.inf for s in "LR"}
        first = min(onset.values())
        n, dt = int(round(seconds / self.timestep)), self.timestep
        t = np.arange(n + 1) * dt
        act = np.stack([activation(t, spikes[s]) for s in "LR"], 1)
        act_tibia = np.stack([activation(t - TIBIA_LAG, spikes[s]) for s in "LR"], 1)
        torque = np.concatenate([tau_max * act, -tibia * tau_max * act_tibia], 1)      # CTr L, R; FTi L, R
        rec = {k: np.zeros((n + 1,) + shape) for k, shape in
               (("thorax", (3,)), ("thorax_velocity", (3,)), ("com", (3,)), ("pitch", ()), ("roll", ()), ("yaw", ()),
                ("positions", (len(self.segments), 3)), ("rotations", (len(self.segments), 3, 3)))}
        rec["joints"] = {name: np.zeros(n + 1) for s in "LR" for name in self.joint_names[s]}
        contact = np.zeros((n + 1, 6), bool)
        vel = np.zeros(6)

        def keep(i):
            rec["thorax"][i] = d.xpos[self._thorax]
            mj.mj_objectVelocity(m, d, mj.mjtObj.mjOBJ_BODY, self._thorax, vel, 0)
            rec["thorax_velocity"][i] = vel[3:]
            rec["com"][i] = d.subtree_com[self._thorax]
            rec["pitch"][i], rec["roll"][i], rec["yaw"][i] = angles(d.xmat[self._thorax])
            rec["positions"][i] = d.xpos[self._bodies]
            rec["rotations"][i] = d.xmat[self._bodies].reshape(-1, 3, 3)
            for s in "LR":
                for name, q in zip(self.joint_names[s], self._qadr[s]):
                    rec["joints"][name][i] = np.degrees(d.qpos[q])

        keep(0)
        target, braced = self.stand.copy(), set()
        for k in range(n):
            for s in "LR":
                if t[k] >= onset[s]:
                    if s not in braced:
                        self._brace(s, brace)
                        braced.add(s)
                    target[self._limp[s]] = d.qpos[self._limp_q[s]]
            glue = np.ones(6)
            glue[[1, 4]] = [t[k] < onset["L"], t[k] < onset["R"]]
            if t[k] >= first + release:
                glue[:] = 0
            sim.set_actuator_inputs("nmf", self._position, target)
            sim.set_actuator_inputs("nmf", self._motor, torque[k])
            sim.set_leg_adhesion_states("nmf", glue)
            sim.step()                                   # contacts found at state k, then integrated to k + 1
            contact[k] = sim.get_ground_contact_info("nmf")[0] > 0
            keep(k + 1)
        mj.mj_forward(m, d)
        contact[n] = sim.get_ground_contact_info("nmf")[0] > 0
        for s in "LR":
            self._brace(s, 1.0)
        rec.update(t=t, contact=contact, activation=act, torque=torque, spikes=spikes, onset=onset,
                   segments=self.segments, legs=LEGS, mass=self.mass,
                   params=dict(tau_max=tau_max, tibia=tibia, release=release, brace=brace, timestep=dt))
        rec["summary"] = summarize(rec)
        return rec


def summarize(rec: dict, flight: float = 2e-3, smooth: float = 0.5e-3) -> dict:
    """A run's takeoff numbers, times in ms from the first TTMn spike (and from the GF spike, GF_TO_TTMN
    earlier). Takeoff: the first moment after which no leg touches the ground for the rest of the run.
    Leg extension: from the first 1° of coxa-trochanter extension in a pushing leg to takeoff. Launch
    speed and angle: the centre of mass's mean velocity over the first `flight` s of flight. Peak
    acceleration: the centre of mass's, from velocities over `smooth` s, from rest to takeoff."""
    t, com, contact = rec["t"], rec["com"], rec["contact"]
    dt = t[1] - t[0]
    fired = [s for s in "LR" if rec["spikes"][s]]
    t_spike = min(rec["spikes"][s][0] for s in fired) if fired else np.nan
    ms = lambda x: round(float(x - t_spike) * 1e3, 3)
    touching = np.flatnonzero(contact.any(1))
    out = {"sides_fired": "".join(fired), "took_off": bool(len(touching) and touching[-1] < len(t) - 1)}
    if not out["took_off"]:
        return out
    i = touching[-1] + 1
    w = int(round(flight / dt))
    ctr = np.stack([rec["joints"][f"{s.lower()}m_coxa-{s.lower()}m_trochanterfemur-pitch"] for s in fired], 1)
    moving = np.flatnonzero((ctr - ctr[0] > 1.0).any(1))
    v = np.gradient(com, dt, axis=0)
    h = max(1, int(round(smooth / 2 / dt)))
    acc = np.zeros_like(v)
    acc[h:-h] = (v[2 * h:] - v[:-2 * h]) / (2 * h * dt)
    out.update(takeoff_ms=ms(t[i]), takeoff_after_gf_ms=round(ms(t[i]) + GF_TO_TTMN * 1e3, 3),
               extension_ms=round(float(t[i] - t[moving[0]]) * 1e3, 3) if len(moving) else None,
               force_to_takeoff_ms=round(float(t[i] - min(rec["onset"].values())) * 1e3, 3),
               legs_off_ms=[ms(t[np.flatnonzero(contact[:, j])[-1] + 1]) if contact[:, j].any() else None for j in range(6)])
    if i + w < len(t):
        launch = (com[i + w] - com[i]) / (w * dt)
        out.update(launch_speed_m_s=round(float(np.linalg.norm(launch)) / 1e3, 4),
                   launch_angle_deg=round(float(np.degrees(np.arctan2(launch[2], np.hypot(launch[0], launch[1])))), 2),
                   launch_velocity_mm_s=[round(float(x), 1) for x in launch],
                   launch_heading_deg=round(float(np.degrees(np.arctan2(launch[1], launch[0]))), 1))
    push = slice(0, i + 1)
    out.update(peak_vertical_acceleration_m_s2=round(float(acc[push, 2].max()) / 1e3, 1),
               peak_horizontal_acceleration_m_s2=round(float(np.hypot(acc[push, 0], acc[push, 1]).max()) / 1e3, 1),
               com_rise_mm=round(float(com[i, 2] - com[0, 2]), 3))
    turn = {k: np.degrees(np.unwrap(np.radians(rec[k]))) for k in ("pitch", "roll", "yaw")}   # no jumps at ±180°
    for k, a in turn.items():
        out[f"{k}_at_takeoff_deg"] = round(float(a[i] - a[0]), 2)
        out[f"{k}_at_end_deg"] = round(float(a[-1] - a[0]), 2)
    up = turn["pitch"][:i + 1] - turn["pitch"][0]
    out.update(most_head_up_before_takeoff_deg=round(float(up.max()), 2), most_head_up_at_ms=ms(t[np.argmax(up)]))
    for k, a in turn.items():
        out[f"{k}_rate_at_takeoff_deg_s"] = round(float(np.gradient(a, dt)[i]), 0)
    for s in fired:
        for short, name in (("ctr", f"{s.lower()}m_coxa-{s.lower()}m_trochanterfemur-pitch"),
                            ("fti", f"{s.lower()}m_trochanterfemur-{s.lower()}m_tibia-pitch")):
            out[f"{short}_{s}_deg_rest_takeoff"] = [round(float(rec["joints"][name][0]), 1), round(float(rec["joints"][name][i]), 1)]
    return out
