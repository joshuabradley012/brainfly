"""Exploratory check, not pre-registered: why does the model's PN response keep rising at strong receptor input, where
flies' saturates?

odor_olsen_protocol_check.py and odor_probe52.py: measured as Olsen et al. measured flies, DL5's PNs rise 105, 129 and 150
spikes/s for 40, 80 and 160 spikes/s of receptor input, where flies' saturate by about 50 (149 at 41.5, 158 at 98.7), so
3-octanol's strong glomeruli keep outpacing 4-methylcyclohexanol's moderate ones (odor_probe53.py). The synapse's own
charge saturates by about 50 spikes/s in flies (Kazama & Wilson 2008 Fig. 9D, after 7 Hz: 107% of the 100 Hz charge at 50,
87% at 200), and the model's two-pool synapse comes close above 50 (derived: 89% at 50, 106% at 200), so the rise may
come from the PNs' own input-output relation or from the onset transient rather than from the synapse.
Model: odor_probe52.py's (its cache), settled starts.
Measured: DL5's cholinergic PNs under odor_olsen_protocol_check.py's protocol at 10, 20, 40, 80 and 160 spikes/s of
receptor input (two seeds), every 10 ms: the PNs' rate, their fast and slow synaptic currents and membrane voltage
(means over PNs and flies), DL5's receptor neurons' rate and fast synapses' mean strength (the two pools together) and
the presynaptic gain; their means over the 500 ms window, its first 100 ms and its last 300 ms. Seeds 650000.

    python experiments/odor_drive_check.py      (writes experiments/odor_drive_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe24 as p24
import odor_probe44 as p44
import odor_probe52 as p52
import warm
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 650000, 2
RATES = (10.0, 20.0, 40.0, 80.0, 160.0)


def strength(b, cells: np.ndarray) -> float:
    """The cells' fast synapses' mean strength (both pools, weighted by their shares) for the next spike."""
    p = b.params[b.cls[cells[0]]]
    first = 1.0 - (1.0 - b.left[:, cells]) * np.exp(-(b.t - b.last[:, cells]) / (p["recovery"] / b.dt))
    if p.get("share2", 0.0) > 0:
        second = 1.0 - (1.0 - b.left2[:, cells]) * np.exp(-(b.t - b.last2[:, cells]) / (p["recovery2"] / b.dt))
        return float(((1 - p["share2"]) * first + p["share2"] * second).mean())
    return float(first.mean())


def gain(b) -> float:
    pres = b._presynaptic
    if pres is None:
        return 1.0
    a = np.maximum(np.asarray(b.presynaptic_state, float) - pres["offset"], 0.0) ** pres["power"]
    return float(np.mean(1.0 / (1.0 + (a * pres["k"]).sum(1))))


def run(o, rec, olsen, x: float, pns: np.ndarray, orns: np.ndarray, seed: int) -> dict:
    b = o.brain
    base = p24.spontaneous(rec)
    grid = np.arange(0, olsen.POST_S, p10.PIECE) + p10.PIECE / 2
    window = grid < olsen.WINDOW_S
    extra = olsen.olsen_shape(grid, x)
    extra *= x / float(extra[window].mean())
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=base)
    piece = int(round(p10.PIECE / b.dt))
    rows = []
    for k, e in enumerate(extra[window]):
        drive = [(rec.cells[h], rec.spont[h] + (e if h == "DL5" else 0.0)) for h in rec.glomeruli if len(rec.cells[h])]
        c = b.advance(piece, drive=drive)
        rows.append([float(c[:, pns].mean()) / p10.PIECE, float(c[:, orns].mean()) / p10.PIECE, float(b.x[:, pns].mean()),
                     float(b.s[:, pns].mean()) if b.s.shape[1] else 0.0, float(b.u[:, pns].mean()), strength(b, orns), gain(b)])
    return np.array(rows)


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe52", p52.build, p44.prepare)
    import odor_olsen_protocol_check as olsen               # after the cache, so that its edits don't invalidate it
    types, m = o.types, o.m
    cholinergic = np.asarray(consensus_transmitters()) == "acetylcholine"
    pns = np.flatnonzero(m["upn"] & np.char.startswith(types, "DL5_"))
    pns = pns[cholinergic[pns]]
    orns = np.asarray(rec.cells["DL5"])
    names = ("pn_hz", "orn_hz", "pn_fast_current", "pn_slow_current", "pn_voltage", "orn_synapse_strength", "presynaptic_gain")
    out = {"question": __doc__, "rates": RATES, "series_names": names, "rates_hz": {}}
    with warm.tracking(o, rec):
        for k, x in enumerate(RATES):
            r = np.mean([run(o, rec, olsen, x, pns, orns, SEED + 10 * k + s) for s in range(SEEDS)], 0)
            row = {"series": {n: r[:, i].round(4).tolist() for i, n in enumerate(names)},
                   "window": {n: round(float(r[:, i].mean()), 3) for i, n in enumerate(names)},
                   "first_100ms": {n: round(float(r[:10, i].mean()), 3) for i, n in enumerate(names)},
                   "last_300ms": {n: round(float(r[20:, i].mean()), 3) for i, n in enumerate(names)}}
            out["rates_hz"][f"{x:g}"] = row
            print(f"x={x:g}", "window", json.dumps(row["window"]), "last300", json.dumps(row["last_300ms"]), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
