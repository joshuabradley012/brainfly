"""Does what the fly sees reach its command neurons? Fly64's settings against brainfly's.

Fly64 (github.com/ornata/fly) drove Super Mario 64 from this connectome, reading Mario's controls
from descending neurons: DNg100 forward, DNa02 steering, DNp01 jump. Its tonic drive (0.18 per 20 ms)
and gain (1.5) put every neuron's resting voltage at threshold (0.18 / (1 - exp(-0.2)) = 0.99, plus
the noise), so the network fires on its own whatever it sees. brainfly's defaults (tonic 0.14, gain
3.0) rest neurons below threshold instead. This shows the 1-D eye (brainfly.eyes) seven scenes under
each setting and records the four command groups built into brain.npz (forward DNg100, steer DNa02,
escape DNp01, backward MDN) on each side.

Scenes, 3 s each, rates over the last 2 s, 8 flies, the same noise in every scene: dark (no eye
input), a blank bright field, a still object on the left or right, an object looming from the left or
right, a bar sweeping across. Measure: each group's rate, and its change from the blank field
(t over flies).
Question, stated before the run: under Fly64's settings, does any scene change any command group by
at least 3 Hz with t >= 4? (A signal would have to stand out from the network's own firing.)

    python experiments/motor_readout.py            (writes experiments/motor_readout.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from brainfly import FlyBrain
from brainfly.eyes import Eyes, blob_for

OUT = Path(__file__).with_name("motor_readout.json")
SECONDS, SKIP, FLIES, SEED = 3.0, 1.0, 8, 64
SETTINGS = {"Fly64 (tonic 0.18, gain 1.5)": (0.18, 1.5), "brainfly (tonic 0.14, gain 3.0)": (0.14, 3.0)}
SCENES = {
    "dark": None,
    "blank": lambda t: [],
    "object left": lambda t: [blob_for(-60, 30, 0.8)],
    "object right": lambda t: [blob_for(60, 30, 0.8)],
    "looming left": lambda t: [blob_for(-110 + 35 * t, 30, 0.8)],
    "looming right": lambda t: [blob_for(110 - 35 * t, 30, 0.8)],
    "bar sweeping": lambda t: [blob_for(-110 + 73 * t, 12, 0.9)],
}


def rates(brain: FlyBrain, scene) -> dict[str, np.ndarray]:
    """Spikes per neuron per second of each command group, per fly, over the last 2 s."""
    brain.reset(SEED)
    eyes = Eyes(brain.azimuth)
    member = np.full(brain.n, -1)
    names = list(brain.groups)
    for g, name in enumerate(names):
        member[brain.groups[name]] = g
    counts = np.zeros((len(names), brain.batch))
    steps = int(round(SECONDS / brain.dt))
    for s in range(steps):
        t = s * brain.dt
        fired = brain.step(None if scene is None else eyes.drive(scene(t)))
        if t < SKIP:
            continue
        for b, idx in enumerate(fired):
            g = member[idx]
            np.add.at(counts[:, b], g[g >= 0], 1)
    window = SECONDS - SKIP
    return {name: counts[g] / (len(brain.groups[name]) * window) for g, name in enumerate(names)}


def main() -> None:
    brain = FlyBrain(batch=FLIES)
    out = {"question": __doc__, "settings": {}}
    for label, (tonic, gain) in SETTINGS.items():
        brain.tonic, brain.gain = tonic, gain
        measured = {name: rates(brain, scene) for name, scene in SCENES.items()}
        blank = measured["blank"]
        changes = {}
        for name, r in measured.items():
            if name == "blank":
                continue
            for group in r:
                d = r[group] - blank[group]
                sd = d.std(ddof=1)
                changes[f"{name}: {group}"] = {"delta": round(float(d.mean()), 2),
                                               "t": round(float(d.mean() / (sd / np.sqrt(len(d)))), 1) if sd > 0 else 0.0}
        strong = {k: v for k, v in changes.items() if abs(v["delta"]) >= 3 and abs(v["t"]) >= 4}
        out["settings"][label] = {"rates": {name: {g: round(float(v.mean()), 2) for g, v in r.items()} for name, r in measured.items()},
                                  "changes": changes, "strong_changes": strong}
        print(f"\n{label}")
        print(f"{'scene':14s} " + " ".join(f"{g:>11s}" for g in brain.groups))
        for name, r in measured.items():
            print(f"{name:14s} " + " ".join(f"{float(v.mean()):11.1f}" for v in r.values()))
        print(f"scene changes of >= 3 Hz with t >= 4: {len(strong)} {sorted(strong)[:6]}")
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
