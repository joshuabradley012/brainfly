"""Exploratory, not pre-registered: the fly sees a looming disk and jumps, from the eyes to the legs in one chain.

brainfly now has each link: flyvis's eyes carry a looming disk to LC4, LPLC2 and the giant fiber (taste_escape.py's
brain); escape_relay.py's relay takes each giant fiber spike to its own jump motor neuron (TTMn) through a curated
electrical synapse; and brainfly.jump turns TTMn spikes into NeuroMechFly's jump. Here they run as one: the brain
(rung6_relay.py's intact model: taste_escape.py's model and biases, the relay, the jump and flight motor neurons
quieted at rest) watches eyepath_native.py's fast loom (a dark disk, r/v 0.04 s, contact 1.8 s after it starts,
gain 1) from the left (70 degrees), from the right, or head-on, 8 flies each. Each fly's TTMn spike times then drive
the jump. The body doesn't feed back to the brain: the loom stays on its course.
Recorded: when each fly's giant fibers and TTMns first fire, relative to contact; whether one or both TTMns fire;
takeoff before contact; launch speed, angle and heading; and the loomed side's LC4 and LPLC2 rates, for the figure
(assets/loom_jump.py).
Ran: every fly's giant fibers fired and every fly left the ground, but few escapes were good. A side loom fires
only that side's giant fiber, so the fly pushes with one middle leg and tumbles away sideways at 0.2 m/s. The
loom-evoked giant fiber spikes come late, mostly 2-52 ms before contact (the fly then leaves at or just before
contact), and head-on ones mostly after contact. And a few giant fiber spikes long before contact, while the disk was
still small, look spontaneous (the resting giant fiber fires about 0.1 Hz here, where a fly's is silent); with the
relay each of them makes a jump. Head-on, both jump motor neurons fired in every fly, but rarely within the same
push; one fly launched with both legs, at 0.47 m/s. ("sides" lists the TTMns that fired within 20 ms of the first,
not only during the push.)

    python experiments/loom_jump.py            (writes experiments/loom_jump.json and loom_jump.npz)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import eyes_at_rest as eyes
import rung6_relay as r6
from brainfly.eye2d import looming
from brainfly.jump import Jump
from eyepath_fast import FAST

OUT = Path(__file__).with_suffix(".json")
SCENES = {"left": 70.0, "right": -70.0, "head-on": 0.0}
CONTACT, BIN, SEED = FAST["contact"], 0.01, 8000
JUMP_SECONDS, LEAD = 0.03, 0.002          # physics per jump, and how long before the first TTMn spike it starts


def watch(s: eyes.Setup, azimuth: float, seed: int) -> dict:
    """1 s of grey, then the loom: per fly, the GF and TTMn spike times (s from the loom's start), and LC4 and LPLC2
    population rates on each side in BIN bins."""
    b, ol, c = s.brain, s.ol, relay.cells()
    scene = looming(azimuth, 0.0, **FAST)
    groups = {f"{t} {x}": b.cells([t], x) for t in ("LC4", "LPLC2") for x in "LR"}
    record = [c["gf"]["L"], c["gf"]["R"], c["ttmn"]["L"], c["ttmn"]["R"]]
    b.reset(seed)
    ol.reset()
    ol.gain = r6.GAIN
    per = int(round(eyes.OPTIC_DT / b.dt))
    for _ in range(int(round(eyes.SETTLE / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(None))
        b.advance(per)
    steps = int(round(eyes.SCENE / eyes.OPTIC_DT))
    spikes = np.zeros((b.trials, steps * per, len(record)), np.int8)
    bins = int(round(eyes.SCENE / BIN))
    rates = {k: np.zeros((b.trials, bins)) for k in groups}
    per_bin = int(round(BIN / eyes.OPTIC_DT))
    for k in range(steps):
        b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(scene(k * eyes.OPTIC_DT))))
        counts, spikes[:, k * per:(k + 1) * per] = b.advance(per, record=record)
        for name, idx in groups.items():
            rates[name][:, k // per_bin] += counts[:, idx].mean(1) / BIN
    times = lambda f, j: (np.flatnonzero(spikes[f, :, j]) * b.dt).tolist()
    return {"flies": [{"gf": {"L": times(f, 0), "R": times(f, 1)}, "ttmn": {"L": times(f, 2), "R": times(f, 3)}}
                      for f in range(b.trials)],
            "rates": {k: v.tolist() for k, v in rates.items()}}


def jump(body: Jump, ttmn: dict) -> dict | None:
    """The body's jump from one fly's TTMn spikes (the first 20 ms of them); None if no TTMn fired."""
    first = min((t[0] for t in ttmn.values() if t), default=None)
    if first is None:
        return None
    spikes = {x: [t - first + LEAD for t in ttmn[x] if t - first < 0.02] for x in "LR"}
    rec = body.run(spikes, seconds=JUMP_SECONDS)
    summary = rec["summary"]
    took = summary.get("took_off", False)
    return {"first_ttmn_s": round(first, 4), "sides": "".join(x for x in "LR" if ttmn[x]),
            "takeoff_before_contact_ms": round((CONTACT - (first - LEAD + summary["takeoff_ms"] * 1e-3)) * 1e3, 1) if took else None,
            **{k: summary[k] for k in ("took_off", "takeoff_ms", "launch_speed_m_s", "launch_angle_deg", "launch_heading_deg",
                                       "roll_at_takeoff_deg", "pitch_at_takeoff_deg") if k in summary}}


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    body = Jump()
    out = {"question": __doc__, "scenes": {}}
    for k, (name, az) in enumerate(SCENES.items()):
        w = watch(s, az, SEED + 100 * k)
        jumps = [jump(body, f["ttmn"]) for f in w["flies"]]
        first_gf = [min((t[0] for t in f["gf"].values() if t), default=None) for f in w["flies"]]
        out["scenes"][name] = {"azimuth_deg": az, "flies": w["flies"], "jumps": jumps, "rates": w["rates"],
                               "gf_fired": int(sum(g is not None for g in first_gf)),
                               "gf_first_before_contact_ms": [None if g is None else round((CONTACT - g) * 1e3, 1) for g in first_gf],
                               "jumped": int(sum(bool(j and j.get("took_off")) for j in jumps)),
                               "both_ttmn": int(sum(bool(j and j["sides"] == "LR") for j in jumps))}
        e = out["scenes"][name]
        print(name, json.dumps({x: e[x] for x in ("gf_fired", "jumped", "both_ttmn", "gf_first_before_contact_ms")}),
              json.dumps([j and {x: j[x] for x in ("sides", "takeoff_before_contact_ms", "launch_speed_m_s", "launch_heading_deg") if x in j} for j in jumps]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
