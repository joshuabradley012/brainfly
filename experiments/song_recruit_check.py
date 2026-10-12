"""Exploratory check, not pre-registered and not a change to the model: why doesn't driving pIP10 recruit dMS2 and vMS12
in rung 6's brain?

song_drive_probe.py: pIP10 at 25-200 Hz drove TN1A to 18-64 Hz and dPR1 to 21-73 Hz, but dMS2, vMS12 and dMS9 stayed at
6-10 Hz, about their resting rates. MaleCNS gives the paths: TN1A -> dMS2 7,913 synapses (dMS2's largest input), dPR1 ->
dMS9 822 and dMS9 -> vMS12 7,415. Half of dMS2's and vMS12's input synapses come from neurons brainfly's sign rule
makes inhibitory.
Model: rung6_relay.build("intact"), 8 flies, at grey: rest, and pIP10 at 100 Hz (song_drive_probe.py's protocol).
Measured over the last 4 s of 5:
- each group's rate (pIP10, TN1A, dPR1, vPR9, dMS2, dMS9, vMS12);
- the built network's weights onto each dMS2, dMS9 and vMS12 neuron: the summed weight (mV per presynaptic spike, as
  the kernel applies it) from each presynaptic group, split into excitatory and inhibitory, and the input those
  weights carry at the groups' measured rates (weight x rate, mV/s into the synaptic current, and times the
  synaptic current's time constant, the steady depolarization it would hold, ignoring depression);
- dMS2's, dMS9's and vMS12's membrane voltage below threshold, sampled every 10 ms (median and 95th percentile), and
  their biases.
Read: whether the targets get the TN1A and dPR1 drive and something cancels it (inhibition rising with it), or
whether the drive is too small to matter against their biases and thresholds.

Ran (2026-10-11, 37 s): the drive arrives on paper but not in the targets' voltages, and the synapses' depression
takes most of it.
- With pIP10 at 100 Hz, TN1A fires at 41 Hz and dPR1 at 47 Hz. Undepressed, the built weights would hold each dMS2
  38.8 mV above its resting input: TN1A 30.6 mV, dPR1 7.1, vMS12 4.3, against vPR9's -3.1. Yet dMS2's median voltage
  moves only from 12.6 to 11.2 mV below threshold (95th percentile 6.9 to 2.3), and it fires at 9.4 Hz.
- dMS9 would get 17.2 mV (dPR1 10.0) and reaches 4.4 mV below threshold, at 7.6 Hz. vMS12 gets only 3.1 mV net:
  dMS9's 5.6 mV is offset by its other inputs (-6.0) and vPR9 (-1.8), so vMS12 sinks to 11.9 mV below.
- TN1A, dPR1, dMS9, vMS12 and dMS2 sit in one class with the whole-brain model's default depression (0.9 of the strength
  left after each spike, recovering over 0.5 s), read from the brain's class table after the run. At 41-47 Hz that
  leaves about a third of each synapse's strength, so TN1A's 30.6 mV is about 10 in effect. pIP10 and vPR9 don't
  depress, so vPR9's GABA grows in full with the drive.
So in rung 6's brain pIP10 reaches dMS2 and vMS12 through the connectome's paths. The default depression (fitted
for no synapse here) cuts the sustained drive to a third, and non-depressing inhibition rises with it, so the steering
motor neurons' inputs stay near rest. Whether flies' VNC song synapses depress like this is unknown. This is one
concrete thing the nerve cord recipe would have to settle before a song test.

Correction (2026-10-11, review 9):
- The question's "about their resting rates" is wrong (dMS2 1.80 to 9.42 Hz here, vMS12 1.57 to 7.18).
- "The synapses' depression takes most of it": applied at each group's measured rate, the stated rule leaves about
  12 mV of the 38.6 mV rise (TN1A keeps about 1/3, dPR1 0.30, vMS12 about 0.77; vPR9 -2.9 mV). Against those 12 mV
  dMS2's median moves 1.4 mV (95th percentile 4.6). So depression accounts for about two thirds of the predicted
  drive, most of the rest is unexplained, and no run here turned depression off. song_recruit_check2.py does.

Correction (2026-10-11, review 10):
"Yet it moves about 1.4 mV" isn't evidence of lost drive: in song_recruit_check2.py, tripling dMS2's rate left
its median voltage unmoved, so a firing unit's median voltage doesn't measure its drive.

    python experiments/song_recruit_check.py      (writes experiments/song_recruit_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import rung6_relay as r6
from brainfly.hybrid import mcns_types
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED = 7900
GROUPS = {"pIP10": ("pIP10",), "TN1A": ("TN1a_",), "dPR1": ("dPR1",), "vPR9": ("vPR9_",), "dMS2": ("dMS2",),
          "dMS9": ("dMS9",), "vMS12": ("vMS12_",), "vMS11": ("vMS11",)}
TARGETS = ("dMS2", "dMS9", "vMS12")


def main() -> None:
    t0 = time.perf_counter()
    s = r6.build("intact")
    b = s.brain
    types = mcns_types().astype(str)
    member = lambda pref: np.flatnonzero([any(x == p or (p.endswith("_") and x.startswith(p)) for p in pref) for x in types])
    idx = {g: member(v) for g, v in GROUPS.items()}
    theta = np.array([b.params[k]["threshold"] for k in range(len(b.params))])[b.cls]
    out = {"question": __doc__, "cells": {g: int(len(v)) for g, v in idx.items()}, "conditions": {}}
    pre_of = np.repeat(np.arange(b.n), np.diff(b.ptr))       # each synapse's presynaptic neuron (CSC by presynaptic)
    for name, hz in (("rest", 0.0), ("pIP10 100 Hz", 100.0)):
        drive = [(idx["pIP10"], hz)] if hz else ()
        relay.rest(s, SEED)
        b.advance(int(round(1.0 / b.dt)), drive=drive)
        counts = np.zeros((b.trials, b.n))
        volts = {g: [] for g in TARGETS}
        for _ in range(400):                                  # 4 s in 10 ms pieces, voltages sampled after each
            counts += b.advance(int(round(0.01 / b.dt)), drive=drive)
            for g in TARGETS:
                volts[g].append((b.u[:, idx[g]] - theta[idx[g]]).ravel())
        rates = counts / 4.0
        rate = {g: round(float(rates[:, v].mean()), 2) for g, v in idx.items()}
        row = {"rates_hz": rate, "targets": {}}
        for g in TARGETS:
            tg = set(int(i) for i in idx[g])
            onto = np.isin(b.idx, list(tg))
            w = b.weights[onto]
            pre = pre_of[onto]
            per_group = {}
            for src, v in idx.items():
                sel = np.isin(pre, v)
                if sel.any():
                    ws = w[sel]
                    per_group[src] = {"exc_mv_per_spike": round(float(ws[ws > 0].sum()) / len(tg), 2),
                                      "inh_mv_per_spike": round(float(ws[ws < 0].sum()) / len(tg), 2),
                                      "input_mv_per_s": round(float(ws.sum()) / len(tg) * rate[src], 1),
                                      "steady_mv": round(float(ws.sum()) / len(tg) * rate[src] * TAU, 2)}
            others = ~np.isin(pre, np.concatenate(list(idx.values())))
            ww = w[others]
            pre_rates = rates.mean(0)[pre[others]]
            per_group["all others"] = {"exc_mv_per_spike": round(float(ww[ww > 0].sum()) / len(tg), 2),
                                       "inh_mv_per_spike": round(float(ww[ww < 0].sum()) / len(tg), 2),
                                       "input_mv_per_s": round(float((ww * pre_rates).sum()) / len(tg), 1),
                                       "steady_mv": round(float((ww * pre_rates).sum()) / len(tg) * TAU, 2)}
            v = np.concatenate(volts[g])
            bias = s.bias[s.gid[idx[g]]] if hasattr(s, "gid") else None
            row["targets"][g] = {"inputs": per_group, "v_below_threshold_mv": {"median": round(float(np.median(v)), 2),
                                                                                "p95": round(float(np.percentile(v, 95)), 2)},
                                 "bias_mv": round(float(np.mean(bias)), 2) if bias is not None else None}
        out["conditions"][name] = row
        print(name, json.dumps(row), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
