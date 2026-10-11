"""Recording, not a test: one trial of each odor through the current olfactory pathway, for the README's animation
(assets/olfaction_movie.py).

Model: odor_probe60.py's antennal lobe (its cache) with mb_calibration4.py's mushroom body (APL's synapses onto the
Kenyon cells a conductance, reversing 20 mV below each cell's rest and fading over 0.3 s), the Kenyon cells' rest as the
learning pilots set it, MBON11 keeping its synaptic current as in the learning pilots (not held near 6 Hz here). Input:
the receptor input the evidence supports (receptor_fills.RECOMMENDED), 3-octanol and 4-methylcyclohexanol for 1 s from
t = 0, from a settled start, 8 flies (seed 880000 + odor).
Recorded in 10 ms pieces from -0.3 to 1.5 s: each glomerulus's uniglomerular PNs' mean rate (mean over flies), every
Kenyon cell's spikes in fly 0 (only the cells that spike at all), APL's release (mean over flies and both APLs) and
MBON11's rate (mean over flies).

    python experiments/olfaction_movie.py      (writes experiments/olfaction_movie.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm

OUT = Path(__file__).with_suffix(".json")
SEED = 880000
ODORS = ("3-octanol", "4-methylcyclohexanol")
T0, T1 = -0.3, 1.5


def record(o, rec, odor: str, seed: int) -> dict:
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    upn = np.flatnonzero(o.m["upn"])
    glom = np.array([t.split("_")[0] for t in o.types[upn]])
    names = sorted(set(glom))
    apl = b.cells(["APL"])
    q = [int(np.flatnonzero(b.graded == i)[0]) for i in apl]
    mbon = b.cells(["MBON11"])
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -1.5
    while t < T0 - 1e-9:
        b.advance(piece, drive=rec.at(plan, t))
        t += p10.PIECE
    pn, kcs, release, mbon_hz = [], [], [], []
    while t < T1 - 1e-9:
        counts = b.advance(piece, drive=rec.at(plan, t))
        rates = counts[:, upn].mean(0) / p10.PIECE
        pn.append([float(rates[glom == g].mean()) for g in names])
        kcs.append(counts[0, kc].copy())
        release.append(float(b.release[:, q].mean()))
        mbon_hz.append(float(counts[:, mbon].mean() / p10.PIECE))
        t += p10.PIECE
    kcs = np.array(kcs)                                    # (pieces, Kenyon cells), fly 0
    active = np.flatnonzero(kcs.sum(0) > 0)
    spikes = {int(kc[i]): [round(T0 + (k + 0.5) * p10.PIECE, 3) for k in np.flatnonzero(kcs[:, i]) for _ in range(int(kcs[k, i]))]
              for i in active}
    return {"glomeruli": names, "pn_hz": np.round(np.array(pn), 1).tolist(), "kc_spikes": spikes,
            "kc_types": {int(kc[i]): str(o.types[kc[i]]) for i in active}, "apl_release_hz": np.round(release, 2).tolist(),
            "mbon11_hz": np.round(mbon_hz, 1).tolist()}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "t0": T0, "t1": T1, "piece_s": p10.PIECE,
           "kenyon_cells": int(o.m["kc"].sum()), "odors": {}}
    with warm.tracking(o, rec), receptor_fills.applied(recommended=True):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        o.brain.set_type("MBON11", keep_current=1.0)
        for j, odor in enumerate(ODORS):
            out["odors"][odor] = record(o, rec, odor, SEED + j)
            r = out["odors"][odor]
            print(odor, "Kenyon cells spiking (fly 0):", len(r["kc_spikes"]), "APL peak", max(r["apl_release_hz"]),
                  "MBON11 peak", max(r["mbon11_hz"]), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
