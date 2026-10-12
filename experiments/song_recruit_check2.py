"""Exploratory check, written after review 9 and before it runs, not pre-registered and not a change to the model: is
the whole-brain model's default synaptic depression what keeps pIP10 from recruiting the song circuit?

song_recruit_check.py: with pIP10 at 100 Hz, the built weights would raise each dMS2's input by 38.6 mV, mostly from
TN1A at 41 Hz. Yet dMS2's median voltage moved 1.4 mV and it fired at 9.4 Hz. TN1A, dPR1, dMS9, vMS12 and dMS2 share the
default depression (0.9 of the strength left after each spike, recovering over 0.5 s), which at 41-47 Hz leaves about a
third. Review 9 found that this accounts for only about two thirds of the predicted drive, and that no run had turned
depression off.
Model: rung6_relay.build("intact"), 8 flies, at grey, as song_drive_probe.py ran it, with one change: the song core's
neurons (pIP10, pMP2, dPR1, TN1A, vPR9, dMS2, vMS12, dMS9) are put in a named set whose synapses don't depress
(depression 1.0). Every other neuron's parameters are checked unchanged. Conditions: rest, and pIP10 at 25 and 100 Hz,
with song_drive_probe.py's protocol (1 s at rest, 1 s driven, 4 s read) and seeds (7800 + condition's index there).
Measured as song_drive_probe.py measures (rates; steering motor neurons' volleys of at least 3 within 5 ms, their
trains and IPIs), plus dMS2's and vMS12's voltage below threshold, sampled every 10 ms.
Read: if dMS2 and vMS12 now follow pIP10 (rates rising with the drive, voltages moving by the undepressed estimate),
the depression was the brake. If they still don't, something else is, such as the targets' other inputs or their
biases.

Ran (2026-10-11, 47 s): the depression was a main brake. Without it pIP10 recruits the song circuit and drives two
steering motor neurons hard, but tonically, not in pulses.
- Only depression changed, on the core's 77 neurons; every other neuron's parameters were unchanged.
- At rest, much as before: dMS2 2.7 Hz, the steering motor neurons 1.6-2.2 Hz.
- pIP10 at 25 Hz: dMS2 16.2 Hz, dMS9 15.8 and vMS12 13.4 (with depression 8.4-9.4, 7.3-8.6 and 6.2-7.6). hg3 fires at
  17.5 Hz, hg4 13.6, ps1 6.1, b3 5.7 and hg1 5.6. Volleys come at 14.8 a second in trains of median length 2, with a
  median IPI of 45 ms and 14% of IPIs within 30-40 ms.
- pIP10 at 100 Hz: dMS2 25.6 Hz, dMS9 28.0 and vMS12 19.8, with vPR9 at 71.7. hg3 fires at 42.1 Hz, hg4 33.8, ps1 9.3
  and b3 8.3. hg1 (1.8), hg2 (1.0), i1 (0.2) and MNwm35 (0.2) fall. Volleys come at 32.6 a second in long trains (median
  13.5), with a median IPI of 24.5 ms and 17% within 30-40 ms.
So the default depression held the circuit near rest. Without it, the recruitment follows the connectome's paths,
and the steering motor neurons that TN1A and dMS2 drive hardest fire tonically at 34-42 Hz. Their volleys then follow
those rates (every 25 ms or so), not a pulse rhythm. The share within 30-40 ms stays at the chance level (about 17%;
flies 59%), and so do the IPIs' spread and the motor neurons that flies use in pulse song: hg1, hg2 and i1 fall
instead of rising. Turning depression off isn't a fit to flies' synapses; it shows what the default was doing. A song
test still needs the circuit to make pulses, which neither setting does.

Correction (2026-10-11, review 10):
- The read named two criteria, and the Ran reported one. Rates passed: dMS2 9.5 to 25.6 Hz at 100 Hz, rising with the
  drive where with depression it was flat. Voltages didn't: by the undepressed estimate dMS2 should gain about 49 mV and
  vMS12 about 23. dMS2's median moved -0.1 mV (95th percentile from -6.7 to -2.7 mV), and vMS12's fell 4.6 mV. By the
  read, something besides depression also limits them: candidates are their inputs' growing inhibition and the reset of
  the synaptic current at each spike (keep_current 0). A firing unit's median voltage doesn't measure its drive, which
  also undercuts song_recruit_check.py's "moves 1.4 mV".
- "The default depression held the circuit near rest" brings back an error review 9 corrected. With depression on, dMS2,
  dMS9 and vMS12 rise 3.0-4.2 times rest. Depression held them to about a third of their undepressed rates, and hg3 and
  hg4 to about a tenth (4.2 against 42.1 Hz, 3.4 against 33.8). TN1A and dPR1 barely changed (pIP10, pMP2 and vPR9
  never depressed).
- "The steering motor neurons that TN1A and dMS2 drive hardest": TN1A's (hg3, hg4). dMS2's largest targets, hg1 and
  MNwm35, fall at 100 Hz.
- "hg1, hg2 and i1, which flies use in pulse song, fall" is selective. Flies' pulse song uses i1 and hg1-4. hg3 and hg4
  rise tenfold, hg1 rises 2.6 times at 25 Hz and at 100 Hz falls 17%, within run-to-run differences, and hg1 matters
  for sine song.
- The 30-40 ms share is at chance (independent Poisson units at these rates through the detector: 17%), but the volleys
  aren't chance events: 32.6 a second against 17.7 for independent units, in longer trains, with the median IPI at
  hg3's interspike interval (24 ms at 42 Hz). "The IPIs' spread" and "tonically" rest on nothing saved (no CV or
  autocorrelation here).
- Numbers: with depression dMS2 ran 8.4-9.6 Hz. Of the core's 77 neurons, 64 had depressed (pIP10 and pMP2 descend, and
  vPR9 is GABAergic).

    python experiments/song_recruit_check2.py      (writes experiments/song_recruit_check2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import rung6_relay as r6
import song_drive_probe as sp
from brainfly.hybrid import mcns_types

OUT = Path(__file__).with_suffix(".json")
CORE = ("pIP10", "pMP2", "dPR1", "TN1a_", "vPR9_", "dMS2", "vMS12_", "dMS9")
CONDITIONS = [("rest", 0.0, 0), ("pIP10 25 Hz", 25.0, 1), ("pIP10 100 Hz", 100.0, 3)]     # song_drive_probe's indices


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    types = mcns_types().astype(str)
    member = lambda pref: np.flatnonzero([any(x == p or (p.endswith("_") and x.startswith(p)) for p in pref) for x in types])
    core = member(CORE)
    before = [dict(b.params[b.cls[i]]) for i in range(b.n)]
    b.sets = {**b.sets, "song core": core}
    b.set_type("song core", depression=1.0)
    after = [dict(b.params[b.cls[i]]) for i in range(b.n)]
    others = np.setdiff1d(np.arange(b.n), core)
    changed = [int(i) for i in others if before[i] != after[i]]
    assert not changed, f"{len(changed)} neurons outside the core changed parameters"
    core_changed = sorted({k for i in core for k in after[i] if before[i].get(k) != after[i].get(k)})
    groups = {"pIP10": member(("pIP10",)), "TN1A": member(("TN1a_",)), "dPR1": member(("dPR1",)), "vPR9": member(("vPR9_",)),
              "dMS2": member(("dMS2",)), "dMS9": member(("dMS9",)), "vMS12": member(("vMS12_",))}
    steer = member(sp.STEERING)
    theta = np.array([b.params[k]["threshold"] for k in range(len(b.params))])[b.cls]
    out = {"question": __doc__, "core_cells": int(len(core)), "core_parameters_changed": core_changed,
           "others_unchanged": True, "conditions": {}}
    print("built", json.dumps({k: out[k] for k in ("core_cells", "core_parameters_changed")}), f"({time.perf_counter() - t0:.0f} s)",
          flush=True)
    record = list(steer)
    for name, hz, k in CONDITIONS:
        drive = [(groups["pIP10"], hz)] if hz else ()
        relay.rest(s, sp.SEED + k)
        b.advance(int(round(1.0 / b.dt)), drive=drive)
        counts = np.zeros((b.trials, b.n))
        spikes = []
        volts = {g: [] for g in ("dMS2", "vMS12")}
        for _ in range(400):
            c, sp_ = b.advance(int(round(0.01 / b.dt)), drive=drive, record=record)
            counts += c
            spikes.append(sp_)
            for g in volts:
                volts[g].append((b.u[:, groups[g]] - theta[groups[g]]).ravel())
        spikes = np.concatenate(spikes, axis=1)
        rates = counts / sp.READ_S
        row = {"rates_hz": {g: round(float(rates[:, v].mean()), 2) for g, v in groups.items()},
               "steering_hz": {t: round(float(rates[:, member((t,))].mean()), 2) for t in sp.STEERING},
               "v_below_threshold_mv": {g: {"median": round(float(np.median(np.concatenate(v))), 2),
                                            "p95": round(float(np.percentile(np.concatenate(v), 95)), 2)} for g, v in volts.items()}}
        per_fly, all_ipi, all_len = [], [], []
        for f in range(b.trials):
            times = [np.flatnonzero(spikes[f, :, q]) * b.dt for q in range(len(record))]
            ev = sp.volleys(times, 3)
            ip, lengths = sp.ipis(ev)
            per_fly.append(len(ev) / sp.READ_S)
            all_ipi += list(ip * 1000)
            all_len += lengths
        ip = np.array(all_ipi)
        row["volleys_3"] = {"per_s": round(float(np.mean(per_fly)), 2),
                            "ipi_median_ms": round(float(np.median(ip)), 1) if len(ip) else None,
                            "ipi_share_30_40": round(float(np.mean((ip >= 30) & (ip <= 40))), 3) if len(ip) else None,
                            "trains_median_length": float(np.median(all_len)) if all_len else None, "ipis": int(len(ip))}
        out["conditions"][name] = row
        print(name, json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
