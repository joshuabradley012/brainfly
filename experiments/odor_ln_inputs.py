"""Exploratory check, not pre-registered: what drives the GABAergic local neurons' onset burst?

odor_probe38.py: scaling every receptor neuron-to-LN synapse down to a quarter barely lowers the GABAergic LNs' onset
burst (2-heptanone: 66 spikes/s per LN at 50-100 ms at full strength, 53 at a quarter), while their later firing falls
with the synapses (19 to 4 spikes/s over 0.2-0.5 s). So the burst is driven by something else.
Model: odor_probe30.py's brain (brain_cache.py). For 2-heptanone and 3-octanol (2 seeds of 8 flies), the GABAergic LNs'
mean rate per cell in 50 ms bins over the odor's first 0.5 s, and their synaptic drive from each presynaptic group
(receptor neurons, uniglomerular PNs, other PNs, LNs, everything else; each spike counting w x 5 ms, graded release
like a spike per second), intact and with each group's synapses onto the LNs cut in turn. Seeds 360000 + 10 x odor +
seed (the same in every condition).

Ran: the onset burst comes from all of the LNs' inputs at once, each from its synapses' rested strength; no one input
carries it. To 2-heptanone the GABAergic LNs fire 63 spikes/s per cell at 50-100 ms and about 12 by 0.45-0.5 s; cutting
their receptor neuron inputs leaves 43 (later 4-6), their uniglomerular PN inputs 51, their other PN inputs 56, their LN
inputs 53 (later firing then higher, 17: the LN inputs excite at onset and inhibit after), and the rest 61 (3-octanol
alike). Their synaptic drive (spikes x weights x 5 ms, depression not counted) at 50-100 ms is 36 mV from receptor
neurons, 21 from uniglomerular PNs, 6 from other PNs and 20 from LNs; later 35-40, 25-30, under 1 and about -1.3. So the
counted drive falls only from 85 to about 67 mV while the firing falls fivefold: the receptor and PN synapses depress
through the odor, and the burst is the onset of all of them together.

    python experiments/odor_ln_inputs.py       (writes experiments/odor_ln_inputs.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import brain_cache
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe21 as p21
import odor_probe24 as p24

OUT = Path(__file__).with_suffix(".json")
SEED = 360000
ODORS = ("2-heptanone", "3-octanol")
SEEDS, BIN, T_END = 2, 0.05, 0.5


def groups(o) -> dict:
    """Presynaptic groups (boolean masks over neurons)."""
    types, m = o.types, o.m
    ln = np.array([bool(p14.LN.match(t)) for t in types])
    pn = np.char.find(types.astype(str), "PN") >= 0
    return {"receptor neurons": m["orn"], "uniglomerular PNs": m["upn"], "other PNs": pn & ~m["upn"] & ~m["orn"],
            "LNs": ln, "other": ~(m["orn"] | pn | ln)}


def run(o, rec, odor: str, seed: int, inhibitors: np.ndarray, maps: dict) -> dict:
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(2.0 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece, per = int(round(p10.PIECE / b.dt)), int(round(BIN / p10.PIECE))
    rate, drive = [], {g: [] for g in maps}
    t = 0.0
    for _ in range(int(round(T_END / BIN))):
        c, g = 0, 0
        for _ in range(per):
            c = c + b.advance(piece, drive=rec.at(plan, t))
            g = g + b.release * p10.PIECE
            t += p10.PIECE
        rate.append(float(c[:, inhibitors].mean() / BIN))
        for name, (W, G) in maps.items():
            d = (c @ W).mean() + ((g @ G).mean() if G is not None else 0.0)
            drive[name].append(float(d * p21.TAU / BIN))
    return {"rate": rate, "drive": drive}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b = o.brain
    inhibitors = p21.masks(o)["inhibitors"]
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.isin(b.idx, inhibitors)
    col = np.searchsorted(inhibitors, b.idx)
    gr = groups(o)
    graded = np.isin(pre, b.graded)
    gi = np.searchsorted(b.graded, pre)
    maps = {}
    for name, mask in gr.items():
        e = np.flatnonzero(onto & mask[pre] & ~graded)
        W = sparse.csr_matrix((b.weights[e].astype(np.float64) / len(inhibitors), (pre[e], np.zeros(len(e), int))), shape=(b.n, 1))
        eg = np.flatnonzero(onto & mask[pre] & graded)
        G = sparse.csr_matrix((b.weights[eg].astype(np.float64) / len(inhibitors), (gi[eg], np.zeros(len(eg), int))),
                              shape=(len(b.graded), 1)) if len(eg) else None
        maps[name] = (W, G)
    w0 = b.weights.copy()
    out = {"question": __doc__, "bins_s": BIN, "gaba_lns": int(len(inhibitors)), "conditions": {}}
    for cond in ["intact"] + [f"cut {name}" for name in gr]:
        w = w0.copy()
        if cond != "intact":
            w[np.flatnonzero(onto & gr[cond[4:]][pre])] = 0.0
        b.weights, b._external_matrix = w, None
        res = {}
        for j, odor in enumerate(ODORS):
            runs = [run(o, rec, odor, SEED + 10 * j + s, inhibitors, maps) for s in range(SEEDS)]
            res[odor] = {"rate_hz": [round(float(x), 1) for x in np.mean([r["rate"] for r in runs], 0)],
                         "drive_mv": {g: [round(float(x), 2) for x in np.mean([r["drive"][g] for r in runs], 0)] for g in gr}}
        out["conditions"][cond] = res
        print(cond, json.dumps({od: r["rate_hz"] for od, r in res.items()}), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    b.weights, b._external_matrix = w0, None
    print("intact drive, 2-heptanone:", json.dumps(out["conditions"]["intact"]["2-heptanone"]["drive_mv"]), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
