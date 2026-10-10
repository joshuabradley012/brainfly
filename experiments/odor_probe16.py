"""Exploratory, not pre-registered: does the model's antennal lobe turn receptor input into projection neuron output as
flies' does?

odor_probe12.py and odor_probe15.py: weak DoOR responses become strong projection neuron (PN) responses at an odor's
onset (DoOR 0.05-0.08, receptors 10-16 Hz above spontaneous, give 94-142 Hz in the first 100 ms), so different odors'
PN patterns correlate more than their receptor patterns (3-octanol against 4-methylcyclohexanol: r = 0.62 against
0.35), and the Kenyon cells inherit the overlap. Olsen, Bhandawat & Wilson 2010 measured the transformation: with one
glomerulus's receptor neurons (ORNs) driven by a private odor, the PN's rise over the 500 ms stimulus follows
PN = Rmax ORN^1.5 / (ORN^1.5 + sigma^1.5), Rmax 163-170 and sigma 11.8-16.3 spikes/s in DM4, DL5 and VM7 (DM1: 144 and
44.8), in control saline; lateral input from other glomeruli divides it, as PN = Rmax ORN^1.5 / (ORN^1.5 + s^1.5 +
sigma^1.5) with s rising linearly with the summed ORN activity (research_notes/Embodied fly connectome simulation/
sensory_periphery.md).
Measured in odor_probe7.py's current model and with odor_probe14.py's correction (the cholinergic local neurons'
synapses onto PNs removed): each of Olsen's four glomeruli's ORNs driven alone at 5, 10, 20, 40, 80 and 160 Hz for
0.5 s, its uniglomerular PNs' rise over the 0.5 s (and over the first 100 ms); Rmax and sigma fitted by least squares as
Olsen fitted them. Then lateral input: the same glomerulus at 10, 20 and 40 Hz while every other glomerulus's ORNs
fire at 20 Hz, and the factor s that the suppression implies (from Eq. 2 with the fitted Rmax and sigma).
Seeds 90000 + 1000 x condition + 10 x glomerulus + rate.

    python experiments/odor_probe16.py         (writes experiments/odor_probe16.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

import odor_probe14 as p14
import odor_probe3 as p3
import odor_probe7 as p7

OUT = Path(__file__).with_suffix(".json")
SEED = 90000
GLOMERULI = ("DM4", "DL5", "VM7", "DM1")
RATES = (5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
LATERAL_RATES, BACKGROUND_HZ = (10.0, 20.0, 40.0), 20.0
OLSEN = {"DM4": (170, 16.3), "DL5": (167, 11.8), "VM7": (163, 12.4), "DM1": (144, 44.8)}
CONDITIONS = ("current", "no cholinergic LN->PN")


def olsen(x, rmax, sigma):
    return rmax * x ** 1.5 / (x ** 1.5 + abs(sigma) ** 1.5)


def drive_response(o: p7.Olfaction, drive: list, pns: np.ndarray, seed: int) -> dict:
    """1 s to settle, 1 s of rest, then `drive` for 0.5 s: the PNs' rise in Hz over the 0.5 s and the first 100 ms."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))[:, pns].mean()
    first = b.advance(int(round(0.1 / b.dt)), drive=drive)[:, pns].mean() / 0.1
    later = b.advance(int(round(0.4 / b.dt)), drive=drive)[:, pns].mean() / 0.4
    return {"whole": round(float((0.1 * first + 0.4 * later) / 0.5 - rest), 2), "first_100ms": round(float(first - rest), 2),
            "rest": round(float(rest), 2)}


def condition(o: p7.Olfaction, name: str, c: int) -> dict:
    base = SEED + 1000 * c
    o.set(p7.CURRENT, base + 900)
    out = {}
    if name != "current":
        out["removed"] = p14.remove(o, p14.cholinergic_ln_edges(o), base + 997)
    types, m, b = o.types, o.m, o.brain
    gloms = sorted({t[4:] for t in types[m["orn"]]})
    orns = {g: b.cells([f"ORN_{g}"]) for g in gloms}
    for gi, g in enumerate(GLOMERULI):
        pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
        row = {"orns": int(len(orns[g])), "pns": int(len(pns)), "alone": {}, "lateral": {}}
        for k, hz in enumerate(RATES):
            row["alone"][f"{hz:g}"] = drive_response(o, [(orns[g], hz)], pns, base + 10 * gi + k)
        x = np.array(RATES)
        y = np.array([row["alone"][f"{hz:g}"]["whole"] for hz in RATES])
        try:
            (rmax, sigma), _ = curve_fit(olsen, x, y, p0=(160.0, 15.0), maxfev=20000)
            row["fit"] = {"rmax": round(float(rmax), 1), "sigma": round(float(abs(sigma)), 1)}
        except RuntimeError:
            row["fit"] = None
        background = [(orns[h], BACKGROUND_HZ) for h in gloms if h != g and len(orns[h])]
        for k, hz in enumerate(LATERAL_RATES):
            r = drive_response(o, [(orns[g], hz)] + background, pns, base + 10 * gi + 7 + k)
            alone = row["alone"][f"{hz:g}"]["whole"]
            s = None
            if row["fit"] and 0 < r["whole"] < row["fit"]["rmax"]:
                rm, sg = row["fit"]["rmax"], row["fit"]["sigma"]
                inner = rm * hz ** 1.5 / r["whole"] - hz ** 1.5 - sg ** 1.5
                s = round(float(inner ** (2 / 3)), 1) if inner > 0 else 0.0
            row["lateral"][f"{hz:g}"] = {**r, "alone_whole": alone, "suppressed_to": round(r["whole"] / alone, 3) if alone > 0 else None, "s": s}
        row["olsen"] = {"rmax": OLSEN[g][0], "sigma": OLSEN[g][1]}
        out[g] = row
        print(name, g, json.dumps({"fit": row["fit"], "olsen": row["olsen"], "alone": {h: v["whole"] for h, v in row["alone"].items()},
                                   "lateral": {h: (v["whole"], v["suppressed_to"], v["s"]) for h, v in row["lateral"].items()}}), flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    out = {"question": __doc__, "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = condition(o, name, c)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
