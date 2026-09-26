"""A body for the brain: NeuroMechFly walking in a virtual-reality arena.

The body is NeuroMechFly v2 as packaged in FlyGym 2.1 (Wang-Chen et al. 2024, Nature Methods;
github.com/NeLy-EPFL/flygym, Apache-2.0; pip install "brainfly[body]", Python 3.12+): the fly's
exoskeleton and 42 actuated leg joints in MuJoCo at 0.1 ms steps, on flat ground, walking under
FlyGym's hybrid turning controller (NeuroMechFly v2's central pattern generators with stepping
rules). The controller takes one descending drive per side of the body: its magnitude sets that
side's stepping amplitude, its sign the stepping direction. The nerve cord isn't simulated; the
controller stands in for it.

The eyes see an analytic scene, as a fly does in a virtual-reality arena: objects around the fly
(a grating drum, dark balls) are drawn in its head frame from its current position and heading,
through the measured eye map (FlyvisNative.contrast). Level head assumed: only the heading turns
the scene.

Loop steps brain and body together. Its link from brain to body is an assumption, stated here:
descending neuron rates (by default DNa02, whose activity on one side predicts turning to that
side; Rayshubskiy et al. 2020, bioRxiv 2020.06.21.163261) set the two drives around a constant
walking drive, from their change against a baseline measured at the start.

    body = Body(control_dt=brain.dt)
    loop = Loop(brain, FlyvisNative(brain), body, arena=[Drum(period=30, speed=40)])
    record = loop.run(seconds=2.0)
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .eye2d import Disk, Grating


@dataclass
class Drum:
    """A sine grating on a distant cylinder around the fly, rotating about the vertical at `speed`
    deg/s (positive counterclockwise seen from above: leftward in front of the fly)."""
    period: float = 30.0
    speed: float = 40.0
    contrast: float = 1.0


@dataclass
class Ball:
    """A dark sphere moving at constant velocity: start and velocity in mm and mm/s, world frame."""
    start: tuple
    velocity: tuple
    radius: float
    darkness: float = 0.9


@dataclass
class Pose:
    """Where the fly is: its thorax and head positions (mm, world frame; the head position is midway
    between the eyes) and heading (radians, counterclockwise from the world's x axis)."""
    thorax: np.ndarray
    head: np.ndarray
    heading: float


def scene(arena: list, pose: Pose, t: float, closed: bool = True) -> list:
    """The arena's objects as the fly sees them at time t, as eye2d objects in its head frame. With
    closed=False the fly's own heading and position don't change what it sees (open loop)."""
    heading = pose.heading if closed else 0.0
    out = []
    for obj in arena:
        if isinstance(obj, Drum):
            out.append(Grating(obj.period, obj.speed * t - np.degrees(heading), obj.contrast))
        elif isinstance(obj, Ball):
            eye = pose.head if closed else np.zeros(3)
            c = np.asarray(obj.start, float) + np.asarray(obj.velocity, float) * t - eye
            dist = np.linalg.norm(c)
            ch, sh = np.cos(-heading), np.sin(-heading)
            d = np.array([ch * c[0] - sh * c[1], sh * c[0] + ch * c[1], c[2]]) / max(dist, 1e-9)
            radius = np.pi if dist <= obj.radius else float(np.arcsin(obj.radius / dist))
            out.append(Disk(d, radius, obj.darkness))
        else:
            raise TypeError(f"unknown arena object {obj!r}")
    return out


class Body:
    """NeuroMechFly on flat ground under FlyGym's hybrid turning controller, stepped `control_dt` at
    a time (the controller updates once per call, physics runs at `timestep`)."""

    def __init__(self, control_dt: float = 0.002, timestep: float = 1e-4, seed: int = 0):
        import mujoco as mj
        from flygym import Simulation
        from flygym.anatomy import ContactBodiesPreset
        from flygym.compose import FlatGroundWorld
        from flygym.utils.math import Rotation3D
        from flygym_demo.complex_terrain import PreprogrammedSteps, make_locomotion_fly

        self.fly = make_locomotion_fly(name="nmf", add_adhesion=True, colorize=True)
        world = FlatGroundWorld()
        world.add_fly(self.fly, [0, 0, 0.8], Rotation3D("quat", [1, 0, 0, 0]),
                      bodysegs_with_ground_contact=ContactBodiesPreset("tibia_tarsus_only"))
        self.sim = Simulation(world, timestep=timestep)
        self.timestep, self.control_dt = timestep, control_dt
        self.substeps = int(round(control_dt / timestep))
        self._steps = PreprogrammedSteps()
        self._dofs = self.fly.get_actuated_jointdofs_order("position")
        body_id = lambda seg: mj.mj_name2id(self.sim.mj_model, mj.mjtObj.mjOBJ_BODY, f"{self.fly.name}/{seg}")
        self._thorax = body_id("c_thorax")
        self._eyes = [body_id("l_eye"), body_id("r_eye")]
        self.reset(seed)

    def reset(self, seed: int = 0) -> None:
        from flygym_demo.complex_terrain import (HybridTurningController, LocomotionAction,
                                                 apply_locomotion_action)

        self.sim.reset()
        self.controller = HybridTurningController(timestep=self.control_dt, preprogrammed_steps=self._steps,
                                                  output_dof_order=self._dofs)
        self.controller.reset(seed=seed)
        apply_locomotion_action(self.sim, self.fly.name, LocomotionAction(
            joint_angles=self._steps.default_pose_by_dof_order(self._dofs), adhesion_onoff=np.ones(6, dtype=bool)))
        self.sim.warmup()

    def walk(self, drive) -> None:
        """One control step (control_dt) under descending drives (left, right)."""
        from flygym_demo.complex_terrain import HybridControllerObservation, apply_locomotion_action

        obs = HybridControllerObservation.from_sim(self.sim, self.fly.name)
        apply_locomotion_action(self.sim, self.fly.name, self.controller.step(np.asarray(drive, float), obs))
        for _ in range(self.substeps):
            self.sim.step()

    def pose(self) -> Pose:
        d = self.sim.mj_data
        forward = d.xmat[self._thorax].reshape(3, 3)[:2, 0]                    # the thorax's x axis, on the ground
        return Pose(thorax=d.xpos[self._thorax].copy(), head=d.xpos[self._eyes].mean(0),
                    heading=float(np.arctan2(forward[1], forward[0])))


class Loop:
    """A brain (FlyBrain), its optic lobe (FlyvisNative) and a Body stepped together at the brain's
    dt. Each step the eyes render the arena, the optic lobe steps and hands FlyBrain its release,
    FlyBrain steps, the steering neurons' rates are updated (exponential filter, time constant
    `tau`), and the body walks one step with drives (base - gain * s, base + gain * s), where s is
    the steering neurons' left-minus-right rate change (Hz) from their baseline."""

    def __init__(self, brain, optic, body: Body, arena: list, steer: tuple = ("DNa02",), base: float = 1.0,
                 gain: float = 0.05, tau: float = 0.1, closed: bool = True):
        if brain.batch != 1:
            raise ValueError("Loop drives one body: build the FlyBrain with batch=1")
        if abs(body.control_dt - brain.dt) > 1e-12:
            raise ValueError("the body's control_dt must equal the brain's dt")
        self.brain, self.optic, self.body, self.arena = brain, optic, body, arena
        self.steer = {s: brain.cells(list(steer), s) for s in "LR"}
        self.base, self.gain, self.tau, self.closed = base, gain, tau, closed
        self.watch = {f"{t} {s}": brain.cells([t], s) for t in ("LC4", "LPLC2", "DNp01") for s in "LR"}

    def run(self, seconds: float, baseline: float = 0.5, seed: int = 1) -> dict:
        """Settle for `baseline` seconds (static arena, walking at the base drive) to measure the
        steering neurons' resting rates, then run for `seconds`. Returns per-step time series."""
        b, dt = self.brain, self.brain.dt
        b.reset(seed)
        self.optic.reset()
        decay = np.exp(-dt / self.tau)
        rate = {s: 0.0 for s in "LR"}
        rest = {s: 0.0 for s in "LR"}
        n_base, n_run = int(round(baseline / dt)), int(round(seconds / dt))
        rec = {k: [] for k in ("t", "x", "y", "heading", "drive_left", "drive_right", "steer_left_hz", "steer_right_hz")}
        rec.update({k: [] for k in self.watch})
        for k in range(n_base + n_run):
            t = (k - n_base) * dt
            pose = self.body.pose()
            rel = self.optic.step(self.optic.contrast(scene(self.arena, pose, max(t, 0.0), self.closed)))
            b.set_graded(self.optic.neurons, rel)
            fired = set(b.step().tolist())
            for s in "LR":
                spikes = sum(i in fired for i in self.steer[s]) / max(len(self.steer[s]), 1)
                rate[s] = rate[s] * decay + spikes / self.tau
            if k < n_base:
                for s in "LR":
                    rest[s] += rate[s] / n_base
                drive = (self.base, self.base)
            else:
                steer = (rate["L"] - rest["L"]) - (rate["R"] - rest["R"])
                drive = (self.base - self.gain * steer, self.base + self.gain * steer)
            self.body.walk(drive)
            if k >= n_base:
                rec["t"].append(t)
                rec["x"].append(float(pose.thorax[0]))
                rec["y"].append(float(pose.thorax[1]))
                rec["heading"].append(pose.heading)
                rec["drive_left"].append(drive[0])
                rec["drive_right"].append(drive[1])
                rec["steer_left_hz"].append(rate["L"])
                rec["steer_right_hz"].append(rate["R"])
                for name, idx in self.watch.items():
                    rec[name].append(int(sum(i in fired for i in idx)))
        rec["steer_rest_hz"] = rest
        return rec
