"""Exploratory, not pre-registered: does the brain that passed rung 4 carry an odor to the mushroom body as a fly's does?

Rung 9's first test pairs an odor with dopamine and asks that MBON-γ1pedc's response to it fall 80-90% (Hige et al.
2015; research_notes/Rung 9 learning data/mushroom_body_plasticity.md). Before any plasticity, the odor itself has to
reach MBON-γ1pedc (MBON11) through sparse Kenyon cell activity. In flies, an odor activates about 5-10% of Kenyon cells
(Honegger et al. 2011; Lin et al. 2014), and MBON-γ1pedc fires about 57 Hz at an odor's onset against about 37 Hz at
rest (Hige et al. 2015, research_notes/Rung 4 resting state data/adaptation.md).
Model: rung4_scaling.py's intact brain (biases, ring offsets and factors from its saved state), 8 flies, flyvis's
neurons silent at grey.
Odors: an odor drives every olfactory receptor neuron of four glomeruli, on both antennae, at 100 Hz for 1 s. Odor A:
DM1, DM2, DM3, DM4 (glomeruli that esters such as ethyl acetate drive); odor B: DL5, DA2, VA2, VM2. Each trial: 1 s to
settle, 1 s of rest, the odor's 1 s, then 1 s (seed 9400 for A, 9401 for B).
Measured: the driven glomeruli's uniglomerular projection neurons' rates; the Kenyon cells that rise by more than 5 Hz
over rest (their share, by KC class, and the two odors' overlap); APL; MBON11 (MBON-γ1pedc>α/β), MBON01 (γ5β'2a) and
MBON18 (α2sc); PPL101 (PPL1-γ1pedc). Rest and odor rates, mean over flies.

Ran: no. The odor reaches the projection neurons (3 to 21 Hz for A, 3 to 32 for B) and stops there: one Kenyon cell
of 4,064 responds to A and none to B (flies: 5-10%), MBON11 stays at 37 Hz, and APL is silent throughout. Afterwards
(not pre-registered): the rest calibration, which aims Kenyon cells at 0 Hz against the brain's background, left their
biases at a median of -11 mV, 27 mV below their 16 mV threshold. An odor's projection neurons at 25 Hz give the Kenyon
cells they reach about 1.2 mV on average. Their synapses' depression (0.85 left per spike, 0.8 s recovery) takes three
quarters of it; without it, 4.6 mV. Only 2 Kenyon cells would reach threshold either way. The resting brain's mushroom
body can't hear odors.

    python experiments/odor_probe.py           (writes experiments/odor_probe.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import eyes_at_rest as eyes
import rung4_scaling as r4s

OUT = Path(__file__).with_suffix(".json")
ODORS = {"A": ["DM1", "DM2", "DM3", "DM4"], "B": ["DL5", "DA2", "VA2", "VM2"]}
SEEDS = {"A": 9400, "B": 9401}
RATE, RISE = 100.0, 5.0
READ = {"MBON11": "MBON-γ1pedc>α/β", "MBON01": "MBON-γ5β'2a", "MBON18": "MBON-α2sc", "PPL101": "PPL1-γ1pedc", "APL": "APL"}


def trial(s, odor: list[str], seed: int) -> dict:
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))
    orns = b.cells([f"ORN_{g}" for g in odor])
    driven = b.advance(int(round(1.0 / b.dt)), drive=[(orns, RATE)])
    b.advance(int(round(1.0 / b.dt)))
    return {"rest": rest, "odor": driven, "orns": orns}               # spikes per neuron over each 1 s window


def main() -> None:
    t0 = time.perf_counter()
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    kc = np.char.startswith(types, "KC")
    out = {"question": __doc__, "odors": ODORS, "kc_total": int(kc.sum()), "conditions": {}}
    responders = {}
    for name, odor in ODORS.items():
        r = trial(s, odor, SEEDS[name])
        rest, odr = r["rest"].mean(0), r["odor"].mean(0)                # Hz, mean over flies
        pn = np.isin(types, [f"{g}_{k}" for g in odor for k in ("adPN", "lPN", "vPN", "ilPN", "lvPN")])
        up = kc & (odr - rest > RISE)
        responders[name] = up
        row = {"pn_hz": [round(float(rest[pn].mean()), 2), round(float(odr[pn].mean()), 2)], "pn_count": int(pn.sum()),
               "kc_share_responding": round(float(up.sum() / kc.sum()), 4),
               "kc_by_class": {c: round(float((up & (types == c)).sum() / max((types == c).sum(), 1)), 4)
                               for c in ("KCg-m", "KCg-d", "KCab", "KCab-p", "KCapbp-m", "KCapbp-ap1", "KCapbp-ap2")},
               "kc_hz": [round(float(rest[kc].mean()), 2), round(float(odr[kc].mean()), 2)],
               "read": {k: [round(float(rest[types == k].mean()), 2), round(float(odr[types == k].mean()), 2)] for k in READ}}
        out["conditions"][name] = row
        print(name, json.dumps(row), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    a, bb = responders["A"], responders["B"]
    out["kc_overlap"] = {"both": int((a & bb).sum()), "A": int(a.sum()), "B": int(bb.sum()),
                         "jaccard": round(float((a & bb).sum() / max((a | bb).sum(), 1)), 4)}
    out["seconds"] = round(time.perf_counter() - t0)
    print("overlap", json.dumps(out["kc_overlap"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
