"""The front legs moved by the nerve cord: NeuroMechFly's front legs driven by the rates of the leg motor neurons in
Pugliese et al.'s nerve cord model (experiments/rung5_vnc.py).

The body is brainfly.jump's: NeuroMechFly v2 in FlyGym 2.1, its 42 leg joints held by the demo position servos (kp
45 µN·mm/rad, ±65 µN·mm) at the walking controller's default pose. By default the thorax is fixed in the air
(FlyGym's TetheredWorld), like a suspended fly, so the front legs swing freely. With tethered=False the fly stands on
flat ground, with adhesion on for the middle and hind legs and off for the front legs, so that their motor neurons
alone decide whether the front feet touch the ground. Units are mm, g and s, so torque is in µN·mm.

Each front leg gets a motor on five joints, and each motor neuron pulls one of them one way, set by its motor module
(the annotation in Pugliese et al.'s table). The directions were checked by forward kinematics from the default pose.
They are the same on both sides, because the right leg's axes are mirrored:
  coxa swing       ThC pitch down: protraction. -10° moves the foot 0.17 mm forward and 0.15 mm up
  coxa stance      ThC pitch up: retraction
  femur/tr flex    CTr pitch down: flexion, the femur raised toward the coxa (+10° opens the coxa-femur angle 10°)
  femur/tr extend  CTr pitch up: extension, the femur lowered (as for the middle legs in brainfly.jump)
  tibia flex       FTi pitch up (0 is a straight tibia; +10° closes the femur-tibia angle 10°)
  tibia extend     FTi pitch down
  femur reductor   CTr roll down: turns the femur about its long axis so that the foot moves back (a guess: the
                   body has no trochanter-femur joint, and a reductor pulls the femur backward)
  substrate grip   TiTa pitch up: tarsus depression (a guess: the long tendon muscle flexes the claw, and the body
                   has no claw)
  tarsus control   TiTa pitch, by type: a Ta depressor MN pushes it up (depression), a Ta levator MN pulls it down
The coxa modules are lumped. Swing (promotor, anterior rotator, adductor) becomes protraction and stance (remotor/
abductor, posterior rotator) becomes retraction, both on NeuroMechFly's front-leg ThC pitch, which moves the foot
fore and aft. Each motor neuron works its soma's leg, since the table gives no root side. The one motor neuron that
has no module drives nothing.

Muscle: each motor neuron's rate goes through a first-order low-pass with time constant TAU = 15 ms. That value is an
assumption, between the jump muscle's 9 ms twitch decay (brainfly.jump) and the rate model's 20 ms. The result is
multiplied by GAIN (µN·mm per Hz, one number for every muscle) and summed with signs over each joint's motor
neurons. The servos stay on under the motors and pull each joint back to the rest pose, standing in for passive joint
elasticity: an unloaded small insect leg rests where passive forces put it (Hooper et al. 2009, J Neurosci
29:4109). With the joints' damping, a joint settles to a step of torque within about 5 ms, so at 12-14 Hz the legs
follow the torque closely. Only the ratio of GAIN to the servos' stiffness sets how far the joints move, so GAIN was
calibrated on that alone (experiments/vnc_legs.py). A linear gain is fitted to the rhythm's low rates (the driven
motor neurons peak at 12 Hz or less), so it would turn a motor neuron at the model's 200 Hz ceiling into an impossible
torque. Each motor is therefore capped at TORQUE_RANGE, the jump muscle's calibrated peak torque (brainfly.jump,
85.6 µN·mm), which no walking muscle should exceed. The front legs' servos get twice that range so that they stay
linear springs, and a capped joint turns at most 109° from rest. End stops were added, as in brainfly.jump, because
FlyGym 2.1 has no joint limits. CTr pitch stays between -180° and 0° (from the femur folded onto the coxa to the femur
in line with it). FTi pitch stays between 0° and 180° (from a straight tibia to one folded onto the femur).

    legs = Legs()
    torque = torques(rates, 1e-3, modules, types, sides)    # rates: time x motor neurons (Hz), one row per ms
    rec = legs.run(torque, 1e-3)
    rec["joints"]      # time x 2 legs (L, R) x 7 joints, degrees; rec["foot"]: the foot relative to the thorax
"""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

from .jump import TAU_MAX

TAU = 0.015                        # s, the muscle's low-pass (assumed)
GAIN = 4.3                         # µN·mm per Hz, calibrated once on joint excursions (experiments/vnc_legs.py)
TORQUE_RANGE = TAU_MAX             # µN·mm, each motor's limit: the jump muscle's calibrated peak torque
SPRING_RANGE = 2 * TORQUE_RANGE    # µN·mm, the front legs' servos: linear springs up to the motors' limit
STOP_SOLREF = (2e-4, 1.0)          # end stops as stiff as FlyGym's ground contact (brainfly.jump)
LEGS = ("L", "R")
JOINTS = ("ThC yaw", "ThC pitch", "ThC roll", "CTr pitch", "CTr roll", "FTi pitch", "TiTa pitch")
DOFS = ("c_thorax-{l}_coxa-yaw", "c_thorax-{l}_coxa-pitch", "c_thorax-{l}_coxa-roll",
        "{l}_coxa-{l}_trochanterfemur-pitch", "{l}_coxa-{l}_trochanterfemur-roll",
        "{l}_trochanterfemur-{l}_tibia-pitch", "{l}_tibia-{l}_tarsus1-pitch")
MODULES = {  # motor module: (joint, direction of the joint angle it pulls)
    "coxa swing": ("ThC pitch", -1), "coxa stance": ("ThC pitch", 1),
    "femur/tr flex": ("CTr pitch", -1), "femur/tr extend": ("CTr pitch", 1),
    "tibia flex": ("FTi pitch", 1), "tibia extend": ("FTi pitch", -1),
    "femur reductor": ("CTr roll", -1), "substrate grip": ("TiTa pitch", 1), "tarsus control": ("TiTa pitch", None),
}
TARSUS = {"Ta depressor MN": 1, "Ta levator MN": -1}
DRIVEN = ("ThC pitch", "CTr pitch", "CTr roll", "FTi pitch", "TiTa pitch")
STOPS = {"CTr pitch": (-np.pi, 0.0), "FTi pitch": (0.0, np.pi)}
ADHESION = np.array([0.0, 1.0, 1.0, 0.0, 1.0, 1.0])     # standing: lf, lm, lh, rf, rm, rh


def dof(leg: str, joint: str) -> str:
    """FlyGym's name for a front leg's joint: dof("L", "CTr pitch") is lf_coxa-lf_trochanterfemur-pitch."""
    return DOFS[JOINTS.index(joint)].format(l=f"{leg.lower()}f")


def pull(module, cell_type=None) -> tuple[int, int] | None:
    """The joint (index into JOINTS) a motor neuron pulls and the direction of the angle, or None."""
    if not isinstance(module, str) or module not in MODULES:
        return None
    joint, sign = MODULES[module]
    sign = TARSUS.get(cell_type) if sign is None else sign
    return None if sign is None else (JOINTS.index(joint), sign)


def matrix(modules, types, sides) -> np.ndarray:
    """(2 legs, 7 joints, neurons): each motor neuron's direction on the joint it pulls, on its soma's leg."""
    M = np.zeros((2, len(JOINTS), len(modules)))
    for i, (m, t, s) in enumerate(zip(modules, types, sides)):
        p = pull(m, t)
        if p is not None and s in LEGS:
            M[LEGS.index(s), p[0], i] = p[1]
    return M


def activation(rates: np.ndarray, dt: float, tau: float = TAU) -> np.ndarray:
    """Each rate (time along axis 0) through a first-order low-pass from rest, trapezoidal steps of dt."""
    e = np.exp(-dt / tau)
    return lfilter([(1 - e) / 2, (1 - e) / 2], [1, -e], np.asarray(rates, float), axis=0)


def torques(rates, dt: float, modules, types, sides, gain: float = GAIN, tau: float = TAU) -> np.ndarray:
    """Joint torques (time, 2 legs, 7 joints; µN·mm) from motor neuron rates (time, neurons; Hz)."""
    return gain * np.einsum("lji,ti->tlj", matrix(modules, types, sides), activation(rates, dt, tau))


class Legs:
    """NeuroMechFly with motors on its front legs' joints, tethered in the air by the thorax (or standing), settled
    once (`settle` seconds at `timestep`) and restored to that state before every run."""

    def __init__(self, tethered: bool = True, timestep: float = 1e-4, settle: float = 0.05):
        import mujoco as mj
        from flygym import Simulation
        from flygym.anatomy import ContactBodiesPreset
        from flygym.compose import ActuatorType, FlatGroundWorld, TetheredWorld
        from flygym.utils.math import Rotation3D
        from flygym_demo.complex_terrain import PreprogrammedSteps, make_locomotion_fly

        self.tethered = tethered
        self.fly = fly = make_locomotion_fly(name="nmf", add_adhesion=not tethered, colorize=True)
        joints = {j.name: j for j in fly.get_jointdofs_order()}
        self.dof_names = [[dof(leg, j) for j in JOINTS] for leg in LEGS]
        motors = [dof(leg, j) for leg in LEGS for j in DRIVEN]
        fly.add_actuators([joints[n] for n in motors], ActuatorType.MOTOR, forcerange=(-TORQUE_RANGE, TORQUE_RANGE))
        for joint, (lo, hi) in STOPS.items():
            for leg in LEGS:
                j = fly.jointdof_to_mjcfjoint[joints[dof(leg, joint)]]
                j.range, j.limited, j.solref_limit = [lo, hi], mj.mjtLimited.mjLIMITED_TRUE, list(STOP_SOLREF)
        if tethered:
            world = TetheredWorld()
            world.add_fly(fly, [0, 0, 2.0], Rotation3D("quat", [1, 0, 0, 0]))
        else:
            world = FlatGroundWorld()
            world.add_fly(fly, [0, 0, 0.8], Rotation3D("quat", [1, 0, 0, 0]),
                          bodysegs_with_ground_contact=ContactBodiesPreset("tibia_tarsus_only"))
        self.sim = Simulation(world, timestep=timestep)
        self.timestep = timestep
        m = self.model = self.sim.mj_model
        self._mj, self._position, self._motor = mj, ActuatorType.POSITION, ActuatorType.MOTOR
        order = [j.name for j in fly.get_actuated_jointdofs_order("motor")]
        self._motor_index = np.array([[order.index(dof(leg, j)) if j in DRIVEN else -1 for j in JOINTS] for leg in LEGS])
        self.stand = PreprogrammedSteps().default_pose_by_dof_order(fly.get_actuated_jointdofs_order("position"))
        servo = [j.name for j in fly.get_actuated_jointdofs_order("position")]
        self.rest = np.degrees([[self.stand[servo.index(n)] for n in names] for names in self.dof_names])
        ids = self.sim._intern_actuatorids_by_type_by_fly[ActuatorType.POSITION]["nmf"]
        for names in self.dof_names:
            for n in names:
                m.actuator_forcerange[int(ids[servo.index(n)])] = (-SPRING_RANGE, SPRING_RANGE)
        qadr = lambda name: int(m.jnt_qposadr[mj.mj_name2id(m, mj.mjtObj.mjOBJ_JOINT, f"nmf/{name}")])
        self._qadr = np.array([[qadr(n) for n in names] for names in self.dof_names])

        # MuJoCo fuses the head into the thorax, so c_head has no body of its own (see brainfly.jump)
        body = lambda seg: mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, f"nmf/{seg}")
        self.segments = [b.name for b in fly.get_bodysegs_order() if body(b.name) >= 0]
        self.bodies = np.array([body(b) for b in self.segments])
        self._thorax = int(self.bodies[0])
        self._feet = np.array([body(f"{leg.lower()}f_tarsus5") for leg in LEGS])

        self.sim.reset()
        self.sim.set_actuator_inputs("nmf", self._position, self.stand)
        self.sim.set_actuator_inputs("nmf", self._motor, np.zeros(len(order)))
        if not tethered:
            self.sim.set_leg_adhesion_states("nmf", ADHESION)
        self.sim.warmup(settle)
        self._spec = mj.mjtState.mjSTATE_INTEGRATION
        self._rest_state = np.empty(mj.mj_stateSize(m, self._spec))
        mj.mj_getState(m, self.sim.mj_data, self._rest_state, self._spec)

    def run(self, torque: np.ndarray, dt: float, every: float = 1e-3, bodies: bool = False) -> dict:
        """The fly from rest under `torque` (time, 2 legs, 7 joints; µN·mm), one row every `dt` s and linear in
        between. Kept every `every` s: the front legs' joint angles (degrees), each foot (the last tarsal segment)
        relative to the thorax in the thorax's frame (mm; x forward, y left, z up) and, with bodies=True, every
        body's position and orientation."""
        mj, m, d, sim = self._mj, self.model, self.sim.mj_data, self.sim
        mj.mj_setState(m, d, self._rest_state, self._spec)
        mj.mj_forward(m, d)
        torque = np.asarray(torque, float)
        n = int(round((len(torque) - 1) * dt / self.timestep))
        keep = int(round(every / self.timestep))
        t_in = np.arange(len(torque)) * dt
        t = np.arange(n + 1) * self.timestep
        flat = torque.reshape(len(torque), -1)
        u = np.stack([np.interp(t, t_in, flat[:, k]) for k in range(flat.shape[1])], 1).reshape(n + 1, 2, len(JOINTS))
        motor = np.zeros((n + 1, int(self._motor_index.max()) + 1))
        for leg in range(2):
            for j in range(len(JOINTS)):
                if self._motor_index[leg, j] >= 0:
                    motor[:, self._motor_index[leg, j]] = u[:, leg, j]
        saves = n // keep + 1
        rec = {"t": np.arange(saves) * keep * self.timestep, "joints": np.zeros((saves, 2, len(JOINTS))),
               "foot": np.zeros((saves, 2, 3)), "torque": u[::keep]}
        if bodies:
            rec["positions"] = np.zeros((saves, len(self.bodies), 3))
            rec["rotations"] = np.zeros((saves, len(self.bodies), 3, 3))
        if not self.tethered:
            rec["thorax"], rec["contact"] = np.zeros((saves, 3)), np.zeros((saves, 6), bool)

        def save(i):
            R = d.xmat[self._thorax].reshape(3, 3)
            rec["joints"][i] = np.degrees(d.qpos[self._qadr])
            rec["foot"][i] = (d.xpos[self._feet] - d.xpos[self._thorax]) @ R
            if bodies:
                rec["positions"][i] = d.xpos[self.bodies]
                rec["rotations"][i] = d.xmat[self.bodies].reshape(-1, 3, 3)
            if not self.tethered:
                rec["thorax"][i] = d.xpos[self._thorax]
                rec["contact"][i] = sim.get_ground_contact_info("nmf")[0] > 0

        save(0)
        sim.set_actuator_inputs("nmf", self._position, self.stand)
        for k in range(n):
            sim.set_actuator_inputs("nmf", self._motor, motor[k])
            sim.step()
            if (k + 1) % keep == 0:
                save((k + 1) // keep)
        rec.update(rest=self.rest, joint_names=list(JOINTS), segments=self.segments, timestep=self.timestep)
        return rec
