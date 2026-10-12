"""Exploratory probe, not pre-registered and not a change to the model: does driving the song command neuron pIP10, in
rung 6's brain, make the wing steering motor neurons fire in volleys spaced like flies' song pulses?

Rung 8's song criterion is "song pulses about 35 ms apart". In flies at about 25 C the inter-pulse interval (IPI) is
34-35 ms (per-fly means 31.6-39.4 ms, pooled CV 0.22, mode about 31 ms). Driving pIP10, one cholinergic descending
neuron per side, gives near-natural IPIs that barely change with drive (33.3, 34.1 and 35.4 ms while pulses per minute
rose elevenfold; von Philipsborn et al. 2011). pIP10 drives pulse song in decapitated flies, so the rhythm is thoracic.
During pulse song the i1 and hg1-4 muscles are reliably active, b1 and b2 silent; the power muscles fire tonically
at about 14 Hz without locking to pulses. No recording resolves what times the pulses, and no model reproduces the IPI
(research_notes/Rung 8 flight data/courtship_song.md). The model has no wings, so a pulse has to be defined from motor
neuron spikes.
Model: rung6_relay.build("intact") (the brain and nerve cord of rung 6's test, its biases), 8 flies, at grey. Each
condition drives its neurons with Poisson spikes (every event fires its neuron) for 5 s after 1 s at rest, and the
last 4 s are read:
  rest            no drive
  pIP10           both pIP10 (MaleCNS 11116, 523998) at 25, 50, 100 and 200 Hz
  pIP10 + pMP2    with pMP2 (10765, 10930), the pulse-specific second command, at 50 and 100 Hz
Read, with the definitions fixed here before the run:
- each motor neuron group's rate (the steering motor neurons i1, b3, hg1-4, ps1 and MNwm35; b1 and b2, silent in
  flies' song; the power neurons DLMn and DVMn) and the core premotor types' (dPR1, vMS12, TN1A, dMS2, vPR9, dMS9);
- volleys: within a fly, a 5 ms window with spikes from at least 3 distinct steering motor neurons (both sides
  together), overlapping windows merged, timed by the first spike. Trains are volleys separated by at most 65 ms
  (Stern's rule), and IPIs are the intervals within trains. Reported: volleys per second, the IPIs' median, CV and
  share within 30-40 ms, and train lengths; also with 2 distinct neurons instead of 3;
- the steering motor neurons' summed spike train's autocorrelation, and the lag of its highest peak in 15-80 ms.
Read: a drive at which volleys recur in trains at a median IPI of 30-40 ms, holding as the drive rises, is a candidate
for a song test. Otherwise, what the steering neurons do instead is the finding.

Ran (2026-10-11, 151 s): no song. Driving pIP10 recruits part of the song circuit's core but not the steering motor
neurons.
- At rest the steering motor neurons fire at 1.7-2.3 Hz (the whole-brain calibration's rate). They fall into volleys of
  at least 3 within 5 ms 2.75 times a second, more than chance, so their resting input is correlated.
- pIP10 at 25-200 Hz drives dPR1 to 21-73 Hz, TN1A to 18-64 Hz and the GABAergic vPR9 to 20-73 Hz. vMS12, dMS2 and
  dMS9 stay at 6-10 Hz, about their resting rates. dMS2 and vMS12 are the steering motor neurons' largest core inputs
  (onto hg1-4, MNwm35 and ps1).
- The steering motor neurons barely change. b3, hg3 and hg4 rise to 3-6 Hz, i1, hg1, hg2 and ps1 stay at 1-3 Hz, and
  MNwm35 falls (to 0.2 Hz). Volleys get rarer as the drive rises (3.5 a second at 25-50 Hz, 1.5 at 200 Hz), and they
  don't form trains (median train length 1).
- The few IPIs within 65 ms (3-16 per condition with 3 neurons) have medians of 31-44 ms. A Poisson series of volleys
  at these rates, cut at 65 ms, gives about 27-29 ms. With 2 neurons the medians are 31-36 ms from 63-128 IPIs, with
  8-21% of them within 30-40 ms (Poisson about 15%). So the near-flies' medians are the 65 ms rule, not a rhythm. The
  summed train's autocorrelation peaks scatter over 15-79 ms.
- Adding pMP2 drives dPR1 to 56-82 Hz, and the volleys get rarer still (1.7 and 0.8 a second).
- b1 and b2 fall from 1.8 to 0.5-1.4 Hz; the power motor neurons stay at about 1-1.7 Hz.
So in rung 6's brain pIP10 reaches dPR1, TN1A and vPR9, but not dMS2 and vMS12, which carry most of the core's input
to the steering motor neurons, and those neurons stay near the calibration's resting rate. In flies dMS2 may act
largely through electrical synapses (courtship_song.md, summary 11), which the model doesn't have there, and vPR9's
GABA may hold the motor neurons down. A song test needs the nerve cord's song circuit to answer pIP10 first.

    python experiments/song_drive_probe.py      (writes experiments/song_drive_probe.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import rung6_relay as r6
from brainfly.hybrid import mcns_types

OUT = Path(__file__).with_suffix(".json")
SEED = 7800
STEERING = ("i1 MN", "b3 MN", "hg1 MN", "hg2 MN", "hg3 MN", "hg4 MN", "ps1 MN", "MNwm35")
CONTROL = ("b1 MN", "b2 MN")
POWER = ("DLMn a, b", "DLMn c-f", "DVMn 1a-c", "DVMn 2a, b", "DVMn 3a, b")
CORE = {"dPR1": ("dPR1",), "vMS12": ("vMS12_",), "TN1A": ("TN1a_",), "dMS2": ("dMS2",), "vPR9": ("vPR9_",), "dMS9": ("dMS9",)}
CONDITIONS = [("rest", (), 0)] + [("pIP10", ("pIP10",), hz) for hz in (25, 50, 100, 200)] + \
             [("pIP10 + pMP2", ("pIP10", "pMP2"), hz) for hz in (50, 100)]
READ_S, WINDOW_S, GAP_S = 4.0, 0.005, 0.065


def volleys(times: list[np.ndarray], need: int) -> np.ndarray:
    """Volley times: 5 ms windows (from each spike) holding spikes of at least `need` distinct neurons, merged."""
    if not any(len(t) for t in times):
        return np.empty(0)
    spikes = np.concatenate(times)
    who = np.concatenate([np.full(len(t), i) for i, t in enumerate(times)])
    order = np.argsort(spikes, kind="stable")
    spikes, who = spikes[order], who[order]
    out, last_end = [], -1.0
    j = 0
    for i in range(len(spikes)):
        while spikes[j] < spikes[i] - 1e-12 and j < i:
            j += 1
        k = np.searchsorted(spikes, spikes[i] + WINDOW_S, side="right")
        if len(set(who[i:k])) >= need:
            if spikes[i] > last_end:
                out.append(spikes[i])
            last_end = spikes[i] + WINDOW_S
    return np.array(out)


def ipis(events: np.ndarray) -> tuple[np.ndarray, list[int]]:
    if len(events) < 2:
        return np.empty(0), [len(events)] if len(events) else []
    d = np.diff(events)
    within = d <= GAP_S
    lengths, n = [], 1
    for w in within:
        if w:
            n += 1
        else:
            lengths.append(n)
            n = 1
    lengths.append(n)
    return d[within], lengths


def autocorr_peak(times: list[np.ndarray], dt: float = 0.001) -> float | None:
    bins = np.zeros(int(round(READ_S / dt)))
    for t in times:
        np.add.at(bins, np.minimum((t / dt).astype(int), len(bins) - 1), 1)
    x = bins - bins.mean()
    if not x.any():
        return None
    ac = np.correlate(x, x, "full")[len(x) - 1:]
    lo, hi = int(0.015 / dt), int(0.080 / dt)
    return round(float((lo + int(np.argmax(ac[lo:hi + 1]))) * dt * 1000), 1)


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    types = mcns_types().astype(str)
    sel = lambda names: np.flatnonzero(np.isin(types, names))
    steer, ctrl, power = sel(STEERING), sel(CONTROL), sel(POWER)
    core = {k: np.flatnonzero([any(t == p or (p.endswith("_") and t.startswith(p)) for p in v) for t in types]) for k, v in CORE.items()}
    drivers = {"pIP10": sel(("pIP10",)), "pMP2": sel(("pMP2",))}
    out = {"question": __doc__, "cells": {"steering": int(len(steer)), "control": int(len(ctrl)), "power": int(len(power)),
                                          **{k: int(len(v)) for k, v in core.items()}, **{k: int(len(v)) for k, v in drivers.items()}},
           "conditions": {}}
    print("built", json.dumps(out["cells"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    record = list(steer)
    for c, (name, groups, hz) in enumerate(CONDITIONS):
        driven = np.concatenate([drivers[g] for g in groups]) if groups else np.empty(0, np.int64)
        drive = [(driven, float(hz))] if len(driven) else ()
        relay.rest(s, SEED + c)
        b.advance(int(round(1.0 / b.dt)), drive=drive)
        counts, spikes = b.advance(int(round(READ_S / b.dt)), drive=drive, record=record)
        rates = counts / READ_S
        row = {"drive_hz": hz, "driven_hz": round(float(rates[:, driven].mean()), 1) if len(driven) else 0.0,
               "steering_hz": {t: round(float(rates[:, sel((t,))].mean()), 2) for t in STEERING},
               "control_hz": round(float(rates[:, ctrl].mean()), 2), "power_hz": round(float(rates[:, power].mean()), 2),
               "core_hz": {k: round(float(rates[:, v].mean()), 2) for k, v in core.items()}}
        for need in (3, 2):
            per_fly, all_ipi, all_len, peaks = [], [], [], []
            for f in range(b.trials):
                times = [np.flatnonzero(spikes[f, :, q]) * b.dt for q in range(len(record))]
                ev = volleys(times, need)
                ip, lengths = ipis(ev)
                per_fly.append(len(ev) / READ_S)
                all_ipi += list(ip * 1000)
                all_len += lengths
                peaks.append(autocorr_peak(times))
            ip = np.array(all_ipi)
            row[f"volleys_{need}"] = {
                "per_s": round(float(np.mean(per_fly)), 2),
                "ipi_median_ms": round(float(np.median(ip)), 1) if len(ip) else None,
                "ipi_cv": round(float(ip.std() / ip.mean()), 3) if len(ip) > 1 else None,
                "ipi_share_30_40": round(float(np.mean((ip >= 30) & (ip <= 40))), 3) if len(ip) else None,
                "trains_median_length": float(np.median(all_len)) if all_len else None,
                "ipis": int(len(ip))}
            if need == 3:
                row["autocorr_peak_ms"] = [p for p in peaks]
        out["conditions"][f"{name} {hz} Hz" if hz else name] = row
        print(f"{name} {hz} Hz", json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
