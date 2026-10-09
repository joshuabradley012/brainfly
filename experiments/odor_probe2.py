"""Exploratory, not pre-registered: odor_probe.py with real odors. Does an odor as DoOR describes it reach the Kenyon
cells of the brain that passed rung 4?

odor_probe.py drove four glomeruli per odor at 100 Hz and found the Kenyon cells deaf (1 of 4,064 responding; flies:
5-10%), 27 mV below threshold with an odor giving them 1-5 mV. Real odors drive many glomeruli to different degrees.
Odors: 3-octanol (OCT) and 4-methylcyclohexanol (MCH), the pair aversive conditioning uses, as brainfly.odors makes
them from DoOR: every receptor neuron of each glomerulus at its consensus response (0-1) times max_hz, for max_hz of
100, 200 and 400, for 1 s (OCT 30 glomeruli above 0.05, MCH 21). Model, trial and measures as odor_probe.py, seeds
9410 + condition.

Ran: no. Real odors don't wake the Kenyon cells either: at most 1 of 4,064 responds to OCT and none to MCH, at every
max_hz, and MBON11 and APL don't move. The projection neurons of the glomeruli each odor drives rise from about 3 to
25-29 Hz, whatever the receptor neurons' rate (100, 200 or 400 Hz). Flies' projection neurons reach about 100-200 Hz
at an odor's onset. So the pathway is limited twice: projection neurons that saturate low, and Kenyon cells that are
far from threshold and weakly driven (odor_probe.py).
Checked afterwards: DoOR's responses here include each receptor's spontaneous level (DoOR's SFR row, 0-0.2 of its strongest
response), which brainfly.odors now subtracts, as DoOR's own reset_sfr does; so every glomerulus was driven harder
than its odor drives it, and receptors at or below their spontaneous rate were driven too (odor_probe7.py reruns
the current model without this). The glomerulus counts above (30 and 21) include
4 and 3 DoOR entries with no receptor neurons in MaleCNS, so 26 and 18 were driven.

    python experiments/odor_probe2.py          (writes experiments/odor_probe2.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import rung4_scaling as r4s
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
ODORS = ("3-octanol", "4-methylcyclohexanol")
MAX_HZ = (100.0, 200.0, 400.0)
RISE = 5.0
READ = {"MBON11": "MBON-γ1pedc>α/β", "MBON01": "MBON-γ5β'2a", "MBON18": "MBON-α2sc", "PPL101": "PPL1-γ1pedc", "APL": "APL"}


def trial(s, odor: str, max_hz: float, seed: int) -> dict:
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))
    driven = b.advance(int(round(1.0 / b.dt)), drive=odors.orn_drive(b, odor, max_hz))
    b.advance(int(round(1.0 / b.dt)))
    return {"rest": rest, "odor": driven}                             # spikes per neuron over each 1 s window


def main() -> None:
    t0 = time.perf_counter()
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    kc = np.char.startswith(types, "KC")
    out = {"question": __doc__, "odors": ODORS, "kc_total": int(kc.sum()), "conditions": {}}
    responders = {}
    for c, (odor, max_hz) in enumerate((o, m) for m in MAX_HZ for o in ODORS):
        name = f"{odor} at {max_hz:g} Hz"
        r = trial(s, odor, max_hz, 9410 + c)
        rest, odr = r["rest"].mean(0), r["odor"].mean(0)                # Hz, mean over flies
        gl = [g for g, v in odors.glomeruli(odor).items() if v > 0.2]
        pn = np.isin(types, [f"{g}_{k}" for g in gl for k in ("adPN", "lPN", "vPN", "ilPN", "lvPN")])
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
    out["kc_overlap"] = {}
    for m in MAX_HZ:
        a, bb = responders[f"{ODORS[0]} at {m:g} Hz"], responders[f"{ODORS[1]} at {m:g} Hz"]
        out["kc_overlap"][f"{m:g} Hz"] = {"both": int((a & bb).sum()), "OCT": int(a.sum()), "MCH": int(bb.sum()),
                                          "jaccard": round(float((a & bb).sum() / max((a | bb).sum(), 1)), 4)}
    out["seconds"] = round(time.perf_counter() - t0)
    print("overlap", json.dumps(out["kc_overlap"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
