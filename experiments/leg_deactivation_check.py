"""Exploratory check, not pre-registered: can any deactivation time constant give FlyMimic's tibia flexor a fly's fast
relaxation and keep its rise, summation and plateau?

leg_twitch.py: with the activation and deactivation time constants Ozdil et al. state (10 and 40 ms), FlyMimic's tibia
flexor twitches like a fly's in its rise, summation and 80 Hz plateau but relaxes about four times too slowly (half of
it gone 58 ms after the peak, flies 12-16 ms; Azevedo et al. 2020, research_notes/Embodied fly connectome
simulation/leg_twitch_data.md). In a first-order activation model the relaxation follows the deactivation time constant.
Setup: leg_twitch.twitch with activation 10 ms and deactivation 40 (the stated value), 20, 15 or 10 ms; for each, every
muscle's maximum force scaled so that full activation pushes the probe with 100 uN, and a spike set to give 9 uN (the
0.1 ms step makes the spike's pulse coarse, so its peak comes out at 7.4-9.0 uN). Measured as leg_twitch.py measures:
the single twitch's half-rise, peak time and half-decay, two spikes 12 ms apart against one, and 1-17 spikes at 80 Hz.

Ran: no; a single deactivation time constant trades the fly's relaxation against its summation. At 10 ms the twitch
relaxes like a fly's (half gone 15.5 ms after the peak; flies 12-16) and two spikes still sum to 1.60 times one (flies
1.4-1.6), but it peaks at 13.6 ms (flies 17-23) and 80 Hz trains level off at 16.9 uN (flies 28-30). At the stated 40 ms
the plateau is a fly's (26.9 uN) and the relaxation four times too slow (58 ms); 15 and 20 ms fall between (21.5 and 28.8
ms; 16.9 and 19.6 uN). A fly's muscle relaxes fast yet sums to three times a twitch at 80 Hz, which a first-order
activation with one time constant each way can't do; rung 7's twitch test needs an activation model with more than that
(calcium release and reuptake, or force that sums beyond the activation), or a criterion on rise and summation alone.

    python experiments/leg_deactivation_check.py      (writes experiments/leg_deactivation_check.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import leg_twitch as lt

OUT = Path(__file__).with_suffix(".json")
DEACTIVATION_S = (0.04, 0.02, 0.015, 0.01)
ACTIVATION_S = 0.01


def main() -> None:
    m, _, _, _ = lt.leg(1.0)
    dt = m.opt.timestep
    out = {"question": __doc__, "flies": lt.FLY, "activation_ms": ACTIVATION_S * 1e3, "conditions": {}}
    for td in DEACTIVATION_S:
        r = lt.twitch(dt, time_constants=(ACTIVATION_S, td))
        out["conditions"][f"{td * 1e3:g} ms"] = r
        print(f"deactivation {td * 1e3:g} ms:", json.dumps({k: r[k] for k in ("single_spike", "two_spike_ratio")}),
              "80 Hz", json.dumps(r["train_80Hz"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
