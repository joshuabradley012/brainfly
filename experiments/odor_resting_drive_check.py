"""Exploratory check, not pre-registered: how much do the receptor neurons' spontaneous spikes depolarize the model's
projection neurons at rest, against flies'?

odor_weak_glomeruli_check.py: in a whole odor the model silences glomeruli with 8 spikes/s of receptor input or less
(they keep 0.10 of their response alone, where Olsen et al.'s normalization keeps 0.42), while the presynaptic
inhibition divides the receptor synapses by only 1.4; the PNs' resting drive, which that division also cuts, could be the
difference. Flies' PNs rest at "approximately -55 to -60 mV when spontaneous synaptic input from ORNs is intact and
approximately -65 mV when input from ORNs is removed" (Gouwens & Wilson 2009, mostly DM1 PNs), a resting receptor drive
of about 5-10 mV; for DM4, 35-46 receptor neurons x 3.4 spikes/s x 0.26 resting efficacy x 6.9 mV x about 25 ms give 5-7
mV (research_notes/Rung 9 learning data/weak_input_gain.md, section 9). A scratch run before this was written: the
cholinergic PNs' mean membrane potential falls 22.4 mV with every receptor neuron silenced.
Model: odor_probe56.py's (its cache).
Measured (2 seeds of 8 flies, 1 s from a start settled in each condition): the cholinergic uniglomerular PNs' mean
membrane potential and rate with every receptor neuron at its spontaneous rate and with all of them silenced (the
antennal lobe settled without them), by glomerulus and over all, and the GABAergic LNs' rate; the PNs' biases.

Ran: the model's receptor neurons hold its PNs two to four times as far above their deafferented rest as flies' do.
Silencing every receptor neuron takes the cholinergic PNs' mean membrane potential down 24.8 mV (by glomerulus 12.3-39.0,
5th-95th percentile, median 21.5): DM1 18.0 mV (flies about 5-10, Gouwens & Wilson's mostly DM1 PNs), DM4 13.0 (flies
about 5-7 by the arithmetic above), DL5 19.0. Their rate falls from 5.24 spikes/s to 0, and the GABAergic LNs' from 4.24
to 1.90. The PNs' biases (median -26.4 mV) offset that drive at rest. So when an odor's presynaptic inhibition divides the
receptor synapses, it takes away several times more tonic drive than in flies, which is how it silences weakly driven
glomeruli (odor_weak_glomeruli_check.py). Where the excess comes from is open: the model's spontaneous rates are its
sensillum classes' medians (DM4's 6 spikes/s against flies' 3.4), and its synapses keep 0.37 of their strength at rest,
where flies' DM4 synapses keep about 0.26 (research_notes/Rung 9 learning data/orn_pn_depression.md).

    python experiments/odor_resting_drive_check.py      (writes experiments/odor_resting_drive_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_eln_check as ec
import odor_probe10 as p10
import odor_probe24 as p24
import odor_probe44 as p44
import odor_probe56 as p56
import warm
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 750000, 2
FLIES_MV = (5.0, 10.0)                             # Gouwens & Wilson 2009


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe56", p56.build, p44.prepare)
    b = o.brain
    nt = np.asarray(consensus_transmitters())
    gloms = [g for g in rec.glomeruli if len(rec.cells[g])]
    pn_of = {g: np.flatnonzero(o.m["upn"] & (nt == "acetylcholine") & np.char.startswith(o.types, f"{g}_")) for g in gloms}
    pn_of = {g: v for g, v in pn_of.items() if len(v)}
    upn = np.concatenate(list(pn_of.values()))
    gaba = np.flatnonzero(np.array([bool(ec.p14.LN.match(t)) for t in o.types]) & (nt == "gaba"))
    piece = int(round(p10.PIECE / b.dt))
    out = {"question": __doc__, "flies_mv": FLIES_MV, "conditions": {},
           "upn_bias_mv": {"median": round(float(np.median(o.own_bias()[upn])), 2)}}
    for c, (name, silent) in enumerate((("intact", ()), ("receptor neurons silenced", gloms))):
        with ec.silenced(rec, silent), warm.settled(o, rec):
            u, hz, gh = np.zeros(b.n), np.zeros(b.n), 0.0
            for s in range(SEEDS):
                b.reset(SEED + 100 * c + s)
                b.set_release(o.s.ol.neurons, o.s.silent)
                drive = p24.spontaneous(rec)
                for _ in range(100):
                    cnt = b.advance(piece, drive=drive)
                    u += b.u.mean(0) / (100 * SEEDS)
                    hz += cnt.mean(0) / SEEDS
            out["conditions"][name] = {"upn_u_mv": round(float(u[upn].mean()), 2), "upn_hz": round(float(hz[upn].mean()), 2),
                                       "gaba_ln_hz": round(float(hz[gaba].mean()), 2),
                                       "by_glomerulus_u_mv": {g: round(float(u[v].mean()), 2) for g, v in pn_of.items()}}
            print(name, json.dumps({k: v for k, v in out["conditions"][name].items() if k != "by_glomerulus_u_mv"}), flush=True)
    a, d = out["conditions"]["intact"], out["conditions"]["receptor neurons silenced"]
    drop = {g: round(a["by_glomerulus_u_mv"][g] - d["by_glomerulus_u_mv"][g], 2) for g in pn_of}
    vals = np.array(list(drop.values()))
    out["drop_mv"] = {"all": round(a["upn_u_mv"] - d["upn_u_mv"], 2), "DM1": drop.get("DM1"), "DM4": drop.get("DM4"),
                      "DL5": drop.get("DL5"), "quantiles_5_50_95": [round(float(x), 2) for x in np.percentile(vals, [5, 50, 95])],
                      "by_glomerulus": drop}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("drop", json.dumps({k: v for k, v in out["drop_mv"].items() if k != "by_glomerulus"}), "flies 5-10 mV",
          f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
