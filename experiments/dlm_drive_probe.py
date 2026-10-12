"""Exploratory probe, not pre-registered and not a change to the model: which descending drive, in rung 6's brain, brings
the quieted DLM motor neurons to flies' flight rates?

dlm_splay_check2-4.py tested the flight motor neurons' splay state on five units alone, with every input imposed. A
test on the whole network needs a flight drive: in flight flies' five DLM motor neurons fire tonically at one rate
per fly, 4.5-8 Hz (3-13 Hz across 100 flies; ISI CV 0.22), and at rest they're silent
(research_notes/Rung 8 flight data/dlm_splay_state.md). rung6_relay.py's brain holds the ten DLMn (MaleCNS's "DLMn a, b"
and "DLMn c-f") silent at rest, with their group biases lowered by escape_relay.py. In MaleCNS 88-95% of each one's
input comes from neurons shared by its unit. The largest are IN19B043 and IN19B067 (about 11% each), IN03B089 (7%) and
IN06B066 (6%). Two synapses up from those premotor types, the descending neurons with the most weighted input are
DNa08, DNg27, DNg02_a and DNp31. DNg02, a population of near-identical pairs, sets wingbeat amplitude by how many of
its cells are active (Namiki et al. 2022). DNa08 and DNp31 also contact the DLMn directly (793 and 1,284 synapses
onto the ten).
Model: rung6_relay.build("intact"), 8 flies, at grey. Each condition drives its descending neurons with Poisson
spikes for 3 s after 1 s at rest (every event fires its neuron):
  DNg02          all DNg02 subtypes, at 25, 50, 100 and 200 Hz
  DNa08/p31/g27  DNa08, DNp31 and DNg27, at 25, 50, 100 and 200 Hz
  both           all of them, at 50 and 100 Hz
Measured over the last 2 s:
- each driven group's rate;
- the main premotor types' rates (IN19B043, IN19B067, IN03B089, IN06B066);
- each DLMn's rate, the five of each side's spread (SD over mean), and ISI CVs where a DLMn fires at least 5 spikes;
- PSI's and TTMn's rates, which should stay silent.
Read: a drive at which every DLMn fires tonically at 3-13 Hz, the five of a side within about 10% of each other, is a
candidate flight state for a whole-network splay test. If none does, that is the finding.

    python experiments/dlm_drive_probe.py      (writes experiments/dlm_drive_probe.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import rung6_relay as r6

OUT = Path(__file__).with_suffix(".json")
SEED = 7700
PREMOTOR = ("IN19B043", "IN19B067", "IN03B089", "IN06B066")
GROUPS = {"DNg02": lambda t: t.startswith("DNg02"), "DNa08/p31/g27": lambda t: t in ("DNa08", "DNp31", "DNg27")}
CONDITIONS = ([("DNg02", ("DNg02",), hz) for hz in (25, 50, 100, 200)]
              + [("DNa08/p31/g27", ("DNa08/p31/g27",), hz) for hz in (25, 50, 100, 200)]
              + [("both", ("DNg02", "DNa08/p31/g27"), hz) for hz in (50, 100)])


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    types = s.types.astype(str)
    c = relay.cells()
    dlmn = {side: c["dlmn"][side] for side in "LR"}
    idx = {g: np.flatnonzero([f(t) for t in types]) for g, f in GROUPS.items()}
    pre = {t: np.flatnonzero(types == t) for t in PREMOTOR}
    out = {"question": __doc__, "groups": {g: {"cells": int(len(v)), "types": sorted(set(types[v]))} for g, v in idx.items()},
           "dlmn": {side: [int(i) for i in v] for side, v in dlmn.items()}, "conditions": {}}
    print("built", json.dumps(out["groups"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    record = dlmn["L"] + dlmn["R"]
    for k, (name, groups, hz) in enumerate(CONDITIONS):
        driven = np.concatenate([idx[g] for g in groups])
        relay.rest(s, SEED + k)
        b.advance(int(round(1.0 / b.dt)), drive=[(driven, float(hz))])
        counts, spikes = b.advance(int(round(2.0 / b.dt)), drive=[(driven, float(hz))], record=record)
        rates = counts / 2.0
        row = {"drive_hz": hz, "driven": {g: round(float(rates[:, idx[g]].mean()), 1) for g in groups},
               "premotor_hz": {t: round(float(rates[:, v].mean()), 2) for t, v in pre.items()},
               "psi_hz": round(float(rates[:, [c["psi"]["L"], c["psi"]["R"]]].mean()), 2),
               "ttmn_hz": round(float(rates[:, [c["ttmn"]["L"], c["ttmn"]["R"]]].mean()), 2), "dlmn": {}}
        for side, v in dlmn.items():
            r = rates[:, v]                                   # (flies, 5)
            spread = [float(x.std() / x.mean()) if x.mean() > 0 else None for x in r]
            cvs = []
            for f in range(b.trials):
                for q, i in enumerate(v):
                    t = np.flatnonzero(spikes[f, :, record.index(i)]) * b.dt
                    if len(t) >= 5:
                        d = np.diff(t)
                        cvs.append(float(d.std() / d.mean()))
            row["dlmn"][side] = {"mean_hz": round(float(r.mean()), 2), "by_neuron_hz": [round(float(x), 2) for x in r.mean(0)],
                                 "spread_within_fly": round(float(np.nanmedian([x for x in spread if x is not None])), 3) if any(x is not None for x in spread) else None,
                                 "isi_cv": round(float(np.median(cvs)), 3) if cvs else None}
        out["conditions"][f"{name} {hz} Hz"] = row
        print(f"{name} {hz} Hz", json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
