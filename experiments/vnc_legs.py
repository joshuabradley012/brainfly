"""Exploratory, not pre-registered: the nerve cord's DNg100 rhythm moving NeuroMechFly's front legs. Does the leg step,
or does it twitch?

Rung 5 (rung5_vnc.py) found that driving DNg100 in brainfly's copy of Pugliese et al.'s front-leg network gives
11.6-13.7 Hz rhythms in the front legs' motor neurons. This feeds those motor neurons into the body. brainfly.legs
turns each motor neuron's rate into torque on the front-leg joint its motor module moves (a 15 ms low-pass, times one
gain), with the thorax fixed in the air. Rate model, network and seeds are rung 5's. Each rate-model run is
simulated for 2 s, with the drive from 0.02 s. The body is scored from 0.5 s, after the onset transient.
Gain: calibrated once, on the reference replicate (the right DNg100 replicate in the README's rhythm figure,
assets/rhythm.py). Its active motor neurons move two joints of the left leg, ThC pitch and CTr pitch. The gain is set
so that, in geometric mean, those two joints swing peak to peak as far as the same joints in the fly step FlyGym
ships (PreprogrammedSteps, one step from NeuroMechFly's recordings of a walking fly: ThC pitch 31.7°, CTr pitch
57.7°). Every other run uses that gain.
Conditions:
  reference  the calibration replicate
  DNg100     the first 4 of rung 5's 32 replicates for each DNg100, with their parameters exactly, driven at 400
  none       the reference replicate's parameters with no drive
  rewired    rung 5's first degree-preserving rewiring, its first 4 replicates for each DNg100
  standing   the reference replicate with the fly on the ground: the front legs' adhesion is off, the others' on
Reported for each run and each front leg: every joint's mean, range and peak-to-peak excursion, plus its rhythm
score and frequency (rung 5's: the autocorrelation's best peak, scaled by a sine's; rhythmic above 0.5). The foot
(the last tarsal segment) relative to the thorax: its fore-aft, lateral and vertical ranges. The loop it draws seen
from the side: the signed area per cycle, over the area of an ellipse with the same ranges. A loop index of +1 is an
ellipse run forward at the top and back at the bottom, as in a step; 0 is a line and -1 the reverse loop. Also the
phase of each moving joint against ThC pitch, and of each motor module's summed rate against coxa swing. The
recorded fly step gets the same numbers, from forward kinematics. The JSON keeps some runs' joint traces (every 2 ms,
over the figure's window, 1.2-1.5 s).
Ran: the gain came out at 4.3 µN·mm per Hz. Each DNg100 moves the front leg on the other side (the right DNg100 the
left leg), and the other front leg moves less than 4°. The driven leg's joints swing at exactly their motor neurons'
frequency, 10.9-15.4 Hz, with rhythm scores near 1. That includes the one replicate rung 5 scores unrhythmic (0.43),
where the coxa swings at 15.4 Hz. Only ThC pitch (26-58° peak to peak) and CTr pitch (6-40°) move, because no tibia or
tarsus motor neuron is active. The left DNg100's replicates move mostly the coxa. The motor neurons' rates have a
large steady part, so the leg is also held 16-76° forward and up to 26° flexed. The torque cap is never reached. The
leg doesn't step. The promotors (coxa swing) fire within 8-32° of the femur's Tr flexors (femur/tr flex, a stance
module), and both raise the foot. The remotor (coxa stance) leads them by 76-109°, but it only works against the
promotors on the same joint. So CTr pitch runs 25-40° ahead of ThC pitch, where in the fly's step the two are 135°
apart: the fly extends the femur as the coxa swings forward. The foot runs up and down one path, with loop indices of
at most 0.11 against the fly step's 0.52. It travels 0.56-1.61 mm up and down but only 0.06-0.61 mm fore and aft; the
fly's step goes 0.76 and 0.80 mm. Standing, the driven foot is off the ground 98% of the time, bobbing in the air, and
the thorax moves 0.04 mm. With no drive no motor neuron fires and the legs stay at rest. Rewired, 100-108 motor
neurons are active with no rhythm (rung 5's scores 0.04-0.18), and every motor sits at its cap throughout. The legs
are held at the extremes the cap allows (up to 109° from rest), and some joints flip between them every second or so.

    python experiments/vnc_legs.py            (writes experiments/vnc_legs.json, about 5 min)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung5_vnc as r5
import vnc_rhythm as v
from brainfly import legs as L
from brainfly import nulls
from vnc_own import own_network

OUT = Path(__file__).with_suffix(".json")
REPS, WINDOW, G0 = 4, 0.5, 1.0            # replicates per DNg100, s before scoring the body, gain for calibration
MOVING = 0.5                               # degrees peak to peak: a joint below this counts as still


def rates_for(W, table, j, seed: int, reps: int, cols=None, drive: float = v.STIM) -> tuple[np.ndarray, dict]:
    """Rates (saves, n, k) of rung 5's replicates `cols` from params(seed, reps), neuron j driven (None: no drive)."""
    p = v.params(table, np.random.default_rng(seed), reps)
    cols = list(range(reps)) if cols is None else list(cols)
    p = {k: x[:, cols] for k, x in p.items()}
    stim = np.zeros((len(table), len(cols)))
    if j is not None:
        stim[j] = drive
    return r5.simulate(W, p, stim, v.T), p


def periodicity(x: np.ndarray) -> tuple[float, float | None]:
    """Rung 5's rhythm score and frequency for one trace in 1-ms samples."""
    raw, f = v._peak_score(np.asarray(x, float))
    if raw <= 1e-6 or f <= 0:
        return 0.0, None
    t = np.arange(len(x)) * v.SAVE
    ref = max(v._peak_score(np.sin(2 * np.pi * f * t))[0], v._peak_score(np.cos(2 * np.pi * f * t))[0])
    return (min(raw / ref, 1.0) if ref > 1e-6 else 0.0), f


def loop(foot: np.ndarray, freq: float | None, dt: float) -> dict:
    """The foot's ranges (mm) and its side-view loop index."""
    c = foot - foot.mean(0)
    x, z = c[:, 0], c[:, 2]
    out = {"fore_aft_mm": round(float(np.ptp(x)), 3), "lateral_mm": round(float(np.ptp(c[:, 1])), 3),
           "vertical_mm": round(float(np.ptp(z)), 3), "loop_index": None}
    if not freq or np.ptp(x) < 1e-3 or np.ptp(z) < 1e-3:
        return out
    cycles = freq * dt * (len(x) - 1)
    area = -0.5 * np.sum(x[:-1] * z[1:] - x[1:] * z[:-1]) / cycles          # > 0: forward at the top, back below
    out["loop_index"] = round(float(area / (np.pi * np.ptp(x) * np.ptp(z) / 4)), 3)
    return out


def phase(a: np.ndarray, b: np.ndarray, freq: float, dt: float) -> float:
    """Degrees by which a leads b at freq."""
    e = np.exp(-2j * np.pi * freq * dt * np.arange(len(a)))
    return float(np.degrees(np.angle(np.sum((a - a.mean()) * e) / np.sum((b - b.mean()) * e))))


def score_body(rec: dict) -> dict:
    """Each front leg's joints and foot after WINDOW s."""
    t, dt = rec["t"], rec["t"][1] - rec["t"][0]
    w = t >= WINDOW
    out = {}
    for li, leg in enumerate(L.LEGS):
        joints = {}
        for j, name in enumerate(L.JOINTS):
            a = rec["joints"][w, li, j]
            s, f = periodicity(a) if np.ptp(a) >= MOVING else (0.0, None)
            joints[name] = {"rest": round(float(rec["rest"][li, j]), 1), "mean": round(float(a.mean()), 1),
                            "min": round(float(a.min()), 1), "max": round(float(a.max()), 1),
                            "pp": round(float(np.ptp(a)), 2), "score": round(s, 3),
                            "freq_hz": round(f, 1) if f else None}
        moving = [n for n in L.JOINTS if joints[n]["pp"] >= MOVING]
        big = max(moving, key=lambda n: joints[n]["pp"]) if moving else None
        freq = joints[big]["freq_hz"] if big else None
        foot = loop(rec["foot"][w, li], freq, dt)
        if big and freq:
            ref = rec["joints"][w, li, L.JOINTS.index("ThC pitch")]
            foot["phase_vs_thc_pitch_deg"] = {n: round(phase(rec["joints"][w, li, L.JOINTS.index(n)], ref, freq, dt), 1)
                                              for n in moving}
        capped = np.abs(rec["torque"][w, li]) >= L.TORQUE_RANGE - 1e-6
        out[leg] = {"joints": joints, "moving": moving, "largest": big, "freq_hz": freq, "foot": foot,
                    "time_at_torque_cap": round(float(capped.any(1).mean()), 3)}
    return out


def motor_neurons(table, rates: np.ndarray, mn: np.ndarray, most: int = 20) -> list[dict] | dict:
    """The active motor neurons (peak over 0.01 Hz after rung 5's clip): module, type, side, peak, mean and trough;
    past `most` of them, only how many there are of each module on each side."""
    x = rates[v.CLIP:, mn]
    active = np.flatnonzero(x.max(0) > 0.01)
    cols = {k: table[k].to_numpy()[mn] for k in ("motor module", "type", "somaSide")}
    if len(active) > most:
        keys = [f"{cols['motor module'][i]} ({cols['somaSide'][i]})" for i in active]
        return {k: keys.count(k) for k in sorted(set(keys))}
    return [{"module": str(cols["motor module"][i]), "type": str(cols["type"][i]), "side": str(cols["somaSide"][i]),
             "peak_hz": round(float(x[:, i].max()), 2), "mean_hz": round(float(x[:, i].mean()), 2),
             "min_hz": round(float(x[:, i].min()), 2)} for i in active]


def module_phases(table, rates: np.ndarray, mn: np.ndarray, freq: float | None) -> dict:
    """Degrees by which each motor module's summed rate on each side leads that side's coxa swing, at freq."""
    if not freq:
        return {}
    x = rates[int(round(WINDOW / v.SAVE)):, mn].astype(float)
    mods, sides = table["motor module"].to_numpy()[mn], table["somaSide"].astype(str).to_numpy()[mn]
    active = rates[v.CLIP:, mn].max(0) > 0.01
    out = {}
    for side in L.LEGS:
        sums = {m: x[:, active & (mods == m) & (sides == side)].sum(1) for m in L.MODULES
                if (active & (mods == m) & (sides == side)).any()}
        if "coxa swing" in sums and np.ptp(sums["coxa swing"]) > 1e-3:
            out[side] = {m: round(phase(y, sums["coxa swing"], freq, v.SAVE), 1) for m, y in sums.items() if np.ptp(y) > 1e-3}
    return out


def traces(rec: dict, span=(1.2, 1.5), every: int = 2) -> dict:
    """The moving joints' angles (degrees) over `span` s, every `every` records (ms)."""
    t = rec["t"]
    k = np.flatnonzero((t >= span[0] - 1e-9) & (t <= span[1] + 1e-9))[::every]
    out = {"t_ms": np.round(t[k] * 1e3, 1).tolist()}
    for li, leg in enumerate(L.LEGS):
        out[leg] = {n: np.round(rec["joints"][k, li, j], 2).tolist() for j, n in enumerate(L.JOINTS)
                    if np.ptp(rec["joints"][k, li, j]) >= MOVING}
    return out


def body_run(legs: L.Legs, table, rates: np.ndarray, mn: np.ndarray, gain: float) -> dict:
    cols = [table[k].to_numpy()[mn] for k in ("motor module", "type", "somaSide")]
    return legs.run(L.torques(rates[:, mn], v.SAVE, *cols, gain=gain), v.SAVE)


def recorded_step(legs: L.Legs) -> dict:
    """The recorded fly step's front-leg joints and foot, by forward kinematics on the tethered body."""
    import mujoco as mj
    from flygym_demo.complex_terrain import PreprogrammedSteps

    steps = PreprogrammedSteps()
    m, d = legs.model, legs.sim.mj_data
    phases = np.linspace(0, 2 * np.pi, 540, endpoint=False)
    order = [L.JOINTS.index({"thorax coxa pitch": "ThC pitch", "thorax coxa roll": "ThC roll",
                             "thorax coxa yaw": "ThC yaw", "coxa trochanterfemur pitch": "CTr pitch",
                             "coxa trochanterfemur roll": "CTr roll", "trochanterfemur tibia pitch": "FTi pitch",
                             "tibia tarsus1 pitch": "TiTa pitch"}[" ".join(s)]) for s in steps.dofs_per_leg]
    angles = np.zeros((len(phases), len(L.JOINTS)))
    angles[:, order] = np.degrees(steps.get_joint_angles("lf", phases).T)
    mj.mj_setState(m, d, legs._rest_state, legs._spec)
    foot = np.zeros((len(phases), 3))
    for i, a in enumerate(angles):
        d.qpos[legs._qadr[0]] = np.radians(a)
        mj.mj_kinematics(m, d)
        foot[i] = (d.xpos[legs._feet[0]] - d.xpos[legs._thorax]) @ d.xmat[legs._thorax].reshape(3, 3)
    mj.mj_setState(m, d, legs._rest_state, legs._spec)
    mj.mj_forward(m, d)
    dt = steps.duration / len(phases)
    freq = 1.0 / steps.duration
    ref = angles[:, L.JOINTS.index("ThC pitch")]
    looped = np.concatenate([foot, foot[:1]])                   # one closed cycle
    return {"duration_s": round(float(steps.duration), 4), "freq_hz": round(freq, 2),
            "swing_fraction": round(float(steps.swing_period["lf"][1] / (2 * np.pi)), 3),
            "joints": {n: {"min": round(float(angles[:, j].min()), 1), "max": round(float(angles[:, j].max()), 1),
                           "pp": round(float(np.ptp(angles[:, j])), 2),
                           "phase_vs_thc_pitch_deg": round(phase(angles[:, j], ref, freq, dt), 1)}
                       for j, n in enumerate(L.JOINTS)},
            "foot": loop(looped, freq, dt),
            "foot_path": np.round(foot[::6], 3).tolist()}


def brief(r: dict) -> dict:
    return {leg: {"moving": r[leg]["moving"], "freq_hz": r[leg]["freq_hz"],
                  "pp": {n: r[leg]["joints"][n]["pp"] for n in r[leg]["moving"]},
                  "offset": {n: round(r[leg]["joints"][n]["mean"] - r[leg]["joints"][n]["rest"], 1) for n in r[leg]["moving"]},
                  **{x: r[leg]["foot"][x] for x in ("loop_index", "fore_aft_mm", "vertical_mm")}}
            for leg in L.LEGS}


def main() -> None:
    t0 = time.perf_counter()
    table, _ = v.network()
    W, _ = own_network(table)
    inst = table["instance"].astype(str).to_numpy()
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    dng100 = {name: int(np.flatnonzero(inst == name)[0]) for name in ("DNg100_L", "DNg100_R")}
    legs = L.Legs()
    out = {"question": __doc__, "constants": {"tau_s": L.TAU, "torque_range": L.TORQUE_RANGE, "window_s": WINDOW,
                                              "timestep_s": legs.timestep}}
    fly = recorded_step(legs)
    out["recorded_step"] = fly
    print("recorded step", json.dumps({k: fly[k] for k in ("freq_hz", "foot")}), flush=True)

    # calibration on the reference replicate (assets/rhythm.py's), plus the no-drive control with its parameters
    ref_rates, _ = rates_for(W, table, dng100["DNg100_R"], r5.SEED + 1, 1)
    none_rates, _ = rates_for(W, table, None, r5.SEED + 1, 1)
    rec = body_run(legs, table, ref_rates[:, :, 0], mn, G0)
    first = score_body(rec)
    calib = ["ThC pitch", "CTr pitch"]
    ratio = [fly["joints"][n]["pp"] / first["L"]["joints"][n]["pp"] for n in calib]
    gain = round(float(G0 * np.exp(np.mean(np.log(ratio)))), 1)
    rec = body_run(legs, table, ref_rates[:, :, 0], mn, gain)
    mnr = v.rhythm(ref_rates[:, :, 0], mn)
    runs = {"reference": {"mn_rhythm": mnr, "motor_neurons": motor_neurons(table, ref_rates[:, :, 0], mn),
                          "module_phase_deg": module_phases(table, ref_rates[:, :, 0], mn, mnr["freq_hz"]),
                          "body": score_body(rec), "traces": traces(rec)}}
    out["calibration"] = {"joints": calib, "fly_pp": [fly["joints"][n]["pp"] for n in calib],
                          f"pp_at_gain_{G0}": [first["L"]["joints"][n]["pp"] for n in calib], "gain": gain,
                          "pp_at_gain": [runs["reference"]["body"]["L"]["joints"][n]["pp"] for n in calib],
                          "module_gain": L.GAIN}
    print("calibration", json.dumps(out["calibration"]), flush=True)
    print("reference", json.dumps(brief(runs["reference"]["body"])), flush=True)
    runs["none"] = {"mn_rhythm": v.rhythm(none_rates[:, :, 0], mn),
                    "motor_neurons": motor_neurons(table, none_rates[:, :, 0], mn),
                    "body": score_body(body_run(legs, table, none_rates[:, :, 0], mn, gain))}
    still = [j for b in runs["none"]["body"].values() for j in b["joints"].values()]
    runs["none"]["largest_pp_deg"] = max(j["pp"] for j in still)
    runs["none"]["largest_offset_from_rest_deg"] = round(max(abs(j["mean"] - j["rest"]) for j in still), 2)
    print("none", runs["none"]["mn_rhythm"], runs["none"]["largest_pp_deg"], runs["none"]["largest_offset_from_rest_deg"],
          flush=True)
    out["runs"] = runs
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))

    rung5 = json.loads((Path(__file__).parent / "rung5_vnc.json").read_text())
    Wr = nulls.degree_preserving(W, np.random.default_rng(r5.SEED + 1000 + 1))
    for label, net, base, key in (("DNg100", W, r5.SEED, "dng100"), ("rewired", Wr, r5.SEED + 210, "nulls")):
        for k, name in enumerate(("DNg100_L", "DNg100_R")):
            rates, _ = rates_for(net, table, dng100[name], base + k, r5.DNG100_REPS, cols=range(REPS))
            saved = rung5[key][name] if key == "dng100" else rung5[key][0][name]
            for rep in range(REPS):
                mnr = v.rhythm(rates[:, :, rep], mn)
                rec = body_run(legs, table, rates[:, :, rep], mn, gain)
                body = score_body(rec)
                runs[f"{label} {name} {rep}"] = {
                    "mn_rhythm": mnr, "rung5_score": round(saved["replicates"][rep]["score"], 3),
                    "motor_neurons": motor_neurons(table, rates[:, :, rep], mn), "body": body}
                if label == "DNg100":
                    runs[f"{label} {name} {rep}"]["module_phase_deg"] = module_phases(table, rates[:, :, rep], mn, mnr["freq_hz"])
                if rep == 0:
                    runs[f"{label} {name} {rep}"]["traces"] = traces(rec)
                print(label, name, rep, "mn", {x: (round(y, 3) if isinstance(y, float) else y) for x, y in mnr.items()},
                      "rung5", round(saved["replicates"][rep]["score"], 3), json.dumps(brief(body)), flush=True)
            OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))

    stand = L.Legs(tethered=False)
    rec = body_run(stand, table, ref_rates[:, :, 0], mn, gain)
    w = rec["t"] >= WINDOW
    runs["standing"] = {"body": score_body(rec), "traces": traces(rec),
                        "front_feet_on_ground": [round(float(rec["contact"][w, k].mean()), 3) for k in (0, 3)],
                        "thorax_moved_mm": round(float(np.linalg.norm(rec["thorax"][w] - rec["thorax"][0], axis=1).max()), 3)}
    print("standing", json.dumps(brief(runs["standing"]["body"])), runs["standing"]["front_feet_on_ground"],
          runs["standing"]["thorax_moved_mm"], flush=True)

    out["summary"] = summary(runs, fly)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps(out["summary"], indent=1), flush=True)


def summary(runs: dict, fly: dict) -> dict:
    """Per condition: the driven leg's frequencies, excursions and loop, and whether the other leg moved."""
    out = {"recorded_step": {**{x: fly["foot"][x] for x in ("loop_index", "fore_aft_mm", "vertical_mm")},
                             "ctr_vs_thc_deg": fly["joints"]["CTr pitch"]["phase_vs_thc_pitch_deg"]}}
    for label in ("reference", "DNg100", "rewired"):
        keys = [k for k in runs if k == label or k.startswith(label + " ")]
        rows = []
        for k in keys:
            b = runs[k]["body"]
            leg = max(L.LEGS, key=lambda s: max([b[s]["joints"][n]["pp"] for n in L.JOINTS]))
            other = "R" if leg == "L" else "L"
            rows.append({"run": k, "mn_score": round(runs[k]["mn_rhythm"]["score"], 3),
                         "mn_freq_hz": round(runs[k]["mn_rhythm"]["freq_hz"], 1) if runs[k]["mn_rhythm"]["freq_hz"] else None,
                         "active_mn": runs[k]["mn_rhythm"]["active_mn"], "leg": leg,
                         "joint_freq_hz": {n: b[leg]["joints"][n]["freq_hz"] for n in b[leg]["moving"]},
                         "joint_score": {n: b[leg]["joints"][n]["score"] for n in b[leg]["moving"]},
                         "pp_deg": {n: b[leg]["joints"][n]["pp"] for n in b[leg]["moving"]},
                         "offset_deg": {n: round(b[leg]["joints"][n]["mean"] - b[leg]["joints"][n]["rest"], 1)
                                        for n in b[leg]["moving"]},
                         **{x: b[leg]["foot"][x] for x in ("loop_index", "fore_aft_mm", "vertical_mm")},
                         "ctr_vs_thc_deg": b[leg]["foot"].get("phase_vs_thc_pitch_deg", {}).get("CTr pitch"),
                         "module_vs_coxa_swing_deg": runs[k].get("module_phase_deg", {}).get(leg),
                         "other_leg_largest_pp_deg": max(b[other]["joints"][n]["pp"] for n in L.JOINTS),
                         "time_at_torque_cap": b[leg]["time_at_torque_cap"]})
        out[label] = rows
    return out


if __name__ == "__main__":
    main()
