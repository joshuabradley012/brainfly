"""Exploratory check, not pre-registered: does a calcium-like active state with a steep link (the Ding/Wilson two-state
model) give FlyMimic's tibia flexor a fly's twitch, doublet and plateau, where one first-order activation trades the
relaxation against the summation? And how do the first-order runs read on flies' time base and at higher rates?

leg_deactivation_check.py: with one deactivation time constant FlyMimic's flexor relaxes like a fly's (10 ms) or levels
off at 80 Hz like a fly's (40 ms), not both. research_notes/Embodied fly connectome simulation/muscle_activation.md
(2026-10-10): flies' times run from the somatic spike, about 2.5 ms before the muscle (0.6-1.0 ms of conduction to the
EMG; 2.1 ms from the motor axon to force onset in the blowfly's b1); the 80 Hz of those checks isn't Azevedo et al.'s,
whose burst rates weren't reported (leg_twitch_data.md said so too), and a fly-shaped twitch summed linearly gives 2.0-2.1
times one at 80 Hz and 3.0-3.1 at 120 Hz; the 28-30 uN plateau is one motor unit's (the fast motor neuron's), about 0.3
of the muscle. In fast insect and vertebrate muscle each spike gives a brief, nearly saturating active state, and force
develops more slowly than that lasts and relaxes as it ends. The note's model, per motor unit: c rises by 1 at each spike
(d after the soma) and decays with tau_c; x = c^m / (c^m + k^m); dF/dt = A x - F / (tau1 + tau2 x), whose ceiling is
A (tau1 + tau2).
Setup: leg_twitch.leg with every muscle's maximum force scaled as leg_twitch.py found it (full activation pushes the
probe with 100 uN), FlyMimic's own near-instant activation (0.1 and 0.4 ms), and the flexor's control g F / F_ceiling,
with F from the model and g the held control that pushes the probe with 29 uN, the fast unit's ceiling. The note's
starting set (d 2.5 ms, tau_c 8 ms, k 0.3, m 8, tau1 10 ms, tau1 + tau2 28 ms) and its four variants, as given: nothing
is fitted to the leg. For comparison, the first-order runs of leg_deactivation_check.py (activation 10 ms, deactivation
10 or 40 ms, their scales, and the spike's pulse found again as leg_twitch.twitch finds it), with their spikes reaching
the muscle 2.5 ms after the soma.
Measured, from the somatic spike: the single twitch's size, half-rise, peak and half-decay after the peak; two spikes 12
and 15 ms apart against one; the peak for 1-17 spikes at 80, 120, 150 and 200 Hz.

Ran: neither model fits everything, and the doublet, not the plateau, separates them while flies' burst rates are
unknown. The two-state model as the note gives it (the flexor held at 0.141 for its 29 uN ceiling) twitches with 8.1 uN
(flies 9), reaching half at 10.4 ms (7.7-9.7) and its peak at 18.5 ms (17-23), and half of it is gone 10.9 ms after the
peak (12-16). Two spikes 12 ms apart give 1.82 times one (flies 1.4-1.6; 1.71 at 15 ms), above the note's idealised 1.66:
the leg smooths a brief twitch more than a longer doublet. Seventeen spikes reach 25.5 uN at 80 Hz and 28.2-28.8 at
120-200 Hz, the ceiling set from flies' plateau. Its four variants move none of this much (twitch 7.2-8.6 uN, half-decay
10.4-11.1 ms, doublet 1.78-1.89). The first-order runs, timed from the soma: with 10 ms deactivation 8.3 uN, 7.5, 16.1 and
15.5 ms, and doublets of 1.60 and 1.56, all a fly's, but 17 spikes give 16.9, 20.8, 23.2 and 26.4 uN at 80, 120, 150 and
200 Hz, so flies' 28-30 would need more than 200 Hz; with the stated 40 ms, 9.0 uN at 8.6 and 19.6 ms, still relaxing four
times too slowly (58 ms), doublets of 1.61, and up to 37 uN at 200 Hz, past the unit's ceiling. The first-order spikes are
0.1-0.3 ms control pulses, which the 0.1 ms step makes 1-3 steps long depending on rounding at each spike's time, so their
trains move irregularly with rate (the 40 ms run's two spikes: 14.6 uN at 80 Hz, 12.0 at 120); the two-state model's
spikes are exact. Next: flies' burst rates from Azevedo et al.'s spike times (Dryad), and the two-state model fitted in
the leg to the twitch, holding the doublet and the plateau out, before a pre-registered twitch test.

    python experiments/leg_activation_check.py      (writes experiments/leg_activation_check.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import mujoco as mj
import numpy as np

import leg_probe as lp
import leg_twitch as lt

OUT = Path(__file__).with_suffix(".json")
DELAY_S = 0.0025                 # soma to muscle
CEILING_UN = 29.0                # the fast unit's plateau (Azevedo et al. 2020)
NOTE = {"tau_c": 0.008, "k": 0.3, "m": 8.0, "tau1": 0.010, "tau_on": 0.028}       # tau_on = tau1 + tau2
VARIANTS = {"note's set": {}, "tau1 + tau2 25 ms": {"tau_on": 0.025}, "tau1 + tau2 35 ms": {"tau_on": 0.035},
            "tau_c 6 ms, k 0.2": {"tau_c": 0.006, "k": 0.2}, "tau_c 10 ms, k 0.4": {"tau_c": 0.010, "k": 0.4}}
RATES = (80.0, 120.0, 150.0, 200.0)
COUNTS = (1, 2, 3, 5, 10, 17)
FLY = {**lt.FLY, "plateau_uN": (28.0, 30.0), "two_spike_isi_ms": "about 12 (an example trace)", "burst_rates": "not reported"}


def two_state(spikes: list[float], steps: int, dt: float, p: dict) -> np.ndarray:
    """The model's force every step as a fraction of its ceiling, the spikes (s, at the soma) reaching it DELAY_S later;
    exact updates with x held through each step."""
    arrive = np.bincount([int(round((s + DELAY_S) / dt)) for s in spikes], minlength=steps)[:steps]
    decay, km = np.exp(-dt / p["tau_c"]), p["k"] ** p["m"]
    a = 1.0 / p["tau_on"]                               # ceiling A (tau1 + tau2) = 1
    c = f = 0.0
    out = np.zeros(steps)
    for k in range(steps):
        c = c * decay + arrive[k]
        x = c ** p["m"] / (c ** p["m"] + km)
        tau = p["tau1"] + (p["tau_on"] - p["tau1"]) * x
        f = a * x * tau + (f - a * x * tau) * np.exp(-dt / tau)
        out[k] = f
    return out


def probe(scale: float, ctrl: np.ndarray, time_constants: tuple | None = None) -> np.ndarray:
    """The probe force (uN) every step with the flexor's control following ctrl (never below FlyMimic's floor)."""
    m, d, q, rest = lt.leg(scale, time_constants)
    a = m.actuator(lt.FLEXOR).id
    out = np.zeros(len(ctrl))
    for k, u in enumerate(ctrl):
        d.ctrl[a] = max(float(u), lp.FLOOR)
        mj.mj_step(m, d)
        out[k] = lp.K * lp.ARM * (d.qpos[q] - rest)
    return out


def traces(force, dt: float, shift_ms: float) -> dict:
    """The probe force every 0.5 ms from the soma for one spike, two 12 ms apart and 17 at 120 Hz (for the figure)."""
    step = int(round(0.0005 / dt))
    pad = int(round(shift_ms / 1e3 / dt))
    shown = lambda x: [round(float(v), 2) for v in np.concatenate([np.zeros(pad), x])[::step]]
    return {"dt_ms": 0.5, "one spike": shown(force([0.0], lt.SECONDS)), "two spikes 12 ms apart": shown(force([0.0, 0.012], lt.SECONDS)),
            "17 spikes at 120 Hz": shown(force([i / 120.0 for i in range(17)], 17 / 120.0 + 0.15))}


def measures(force, dt: float, shift_ms: float) -> dict:
    """Twitch, doublets and trains from force(spike times, seconds) -> probe trace; times shifted to the soma."""
    single = force([0.0], lt.SECONDS)
    s = lt.shape(single, dt)
    s["half_ms"], s["peak_ms"] = round(s["half_ms"] + shift_ms, 2), round(s["peak_ms"] + shift_ms, 2)
    out = {"single_spike": s,
           "two_spike_ratio": {f"{isi:g} ms": round(float(force([0.0, isi / 1e3], lt.SECONDS).max() / single.max()), 3)
                               for isi in (12, 15)},
           "trains_uN": {f"{r:g} Hz": {n: round(float(force([i / r for i in range(n)], n / r + 0.15).max()), 2) for n in COUNTS}
                         for r in RATES}}
    print(json.dumps(out), flush=True)
    return out


def main() -> None:
    m, _, _, _ = lt.leg(1.0)
    dt = m.opt.timestep
    twitch, deact = (json.loads((OUT.parent / f"{n}.json").read_text()) for n in ("leg_twitch", "leg_deactivation_check"))
    scale = twitch["scale"]                              # FlyMimic's own activation, 100 uN at full activation
    steps = int(round(lt.SECONDS / dt))
    g = lt.bisect(lambda u: probe(scale, np.full(int(round(0.1 / dt)), u))[-1], CEILING_UN, 1e-3, 1.0)
    out = {"question": __doc__, "fly": FLY, "delay_ms": DELAY_S * 1e3, "scale": scale, "ceiling_control": round(g, 5),
           "ceiling_uN": round(float(probe(scale, np.full(int(round(0.1 / dt)), g))[-1]), 2), "two_state": {}, "first_order": {}}
    print("ceiling control", round(g, 4), "->", out["ceiling_uN"], "uN", flush=True)
    for name, change in VARIANTS.items():
        p = {**NOTE, **change}
        print("two-state:", name, json.dumps(p), flush=True)
        force = lambda spikes, seconds: probe(scale, g * two_state(spikes, int(round(seconds / dt)), dt, p))
        out["two_state"][name] = {"parameters": p, **measures(force, dt, 0.0)}
        if name == "note's set":
            out["two_state"][name]["traces"] = traces(force, dt, 0.0)
        OUT.write_text(json.dumps(out, indent=1))
    for name in ("10 ms", "40 ms"):
        run = deact["conditions"][name]
        tc = (0.01, float(name.split()[0]) / 1e3)
        width = lt.bisect(lambda w: lt.force_trace(run["scale"], [(0.0, w)], lt.SECONDS, tc).max(), lt.FLY["spike_uN"], dt, 0.02)
        print("first-order: deactivation", name, "spike pulse", round(width * 1e3, 4), "ms", flush=True)    # as leg_twitch.twitch finds it
        force = lambda spikes, seconds: lt.force_trace(run["scale"], [(s, width) for s in spikes], seconds, tc)
        out["first_order"][f"deactivation {name}"] = {"scale": run["scale"], "spike_pulse_ms": round(width * 1e3, 4),
                                                      "pulse_steps": sum(k * dt < width for k in range(int(0.02 / dt) + 2)), **measures(force, dt, DELAY_S * 1e3),
                                                      "traces": traces(force, dt, DELAY_S * 1e3)}
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
