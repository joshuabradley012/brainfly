"""Exploratory check, not pre-registered: does a broad odor suppress a glomerulus's PNs as much in the model as in flies,
for the same total receptor input?

odor_probe50.py: adding 4-methylcyclohexanol's weak receptor input in four glomeruli (about 4% more summed receptor input)
cut the other glomeruli's PN responses by 7-40%, so its summed PN response fell. In flies a broad odor's lateral
inhibition grows with the summed receptor input (Olsen et al. 2010's normalization). Olsen et al. measured it directly
(their Fig. 2C, research_notes/Rung 9 learning data/presynaptic_inhibition.md): a private odor's PN response in VM7 or
DL5, alone and mixed with pentyl acetate at 10^-6 to 10^-3, whose antennal field potentials (about 0.7, 1.2, 2.2 and 4.8
mV s) correspond to about 133, 228, 418 and 912 spikes/s of summed receptor input (Olsen et al.'s fit, s about 0.056 of
the summed rate for VM7 and m 10.63 per mV s; derived in presynaptic_inhibition.md). VM7's response to 2-butanone 10^-6
(77 spikes/s alone, 0.47 of its Rmax) kept 0.66, 0.47, 0.22 and 0.10 of it; at 10^-5 (135, 0.83 of Rmax) 0.90, 0.84,
0.67 and 0.55; at 10^-4 (161) 1.02, 0.98, 0.91 and 0.80. DL5 (trans-2-hexenal): 41 spikes/s alone kept 0.66, 0.44, and
0.12-0.29 at 10^-4; 83 kept 0.75, 0.65, 0.54; 147 kept 0.94, 0.88, 0.76.
Model: odor_probe49.py's, or another cached build named on the command line (odor_probe51), with its settled starts.
Measured: VM7d's and DL5's cholinergic PNs over the 500 ms from the valve's opening less the 500 ms before
(odor_olsen_protocol_check.py's protocol), their receptor neurons driven at x (Olsen et al.'s time course, window mean x)
chosen to give about the same share of the model's Rmax as flies' three private responses (10, 20 and 80 spikes/s), with
every other glomerulus's receptor neurons driven by pentyl acetate's DoOR pattern (the private glomerulus left out), with
the same time course for strong input, scaled to 0, 133, 228, 418 and 912 spikes/s of summed evoked receptor input; the
share of the response alone each keeps. Two seeds per point: 600000 + 1000 x glomerulus + 100 x rate + 10 x level + seed.

Ran (on odor_probe51.py's model): yes, for a response at the same share of the glomerulus's Rmax; the model's lateral
inhibition, fitted only to Olsen & Wilson 2008's EPSCs, reproduces Olsen et al.'s suppression. VM7d at x = 20 (56
spikes/s alone, 0.47 of the model's Rmax, as flies' 77 is of theirs) keeps 0.66, 0.45, 0.26 and 0.07 of it at 133, 228,
418 and 912 spikes/s of pentyl acetate input (flies 0.66, 0.47, 0.22, 0.10); at x = 80 (102, 0.81) 0.88, 0.78, 0.68 and
0.55 (flies, at 0.83: 0.90, 0.84, 0.67, 0.55); at x = 10 (30, 0.25) 0.46, 0.18, 0.02 and -0.07 (no fly point at that
share in VM7). DL5 at x = 10 (37, 0.31) keeps 0.58, 0.33, 0.13 and -0.04 (flies, 41 at 0.25: 0.66, 0.44, 0.12-0.29); at x
= 20 (61, 0.50) 0.74, 0.58, 0.40 and 0.19 (flies, 83 at 0.50: 0.75, 0.65, 0.54); at x = 80 (103, 0.85) 0.90, 0.83, 0.75
and 0.64 (flies, 147 at 0.88: 0.94, 0.88, 0.76): a little more suppression than flies' at the higher levels, and less
than VM7d's, as in flies (Olsen et al.'s m 4.19 against 10.63). So a broad odor divides the model's PN responses about
as flies' are divided. What differs is the responses themselves: the model's are half to two thirds of flies' at every
input (odor_olsen_protocol_check.py), so 4-methylcyclohexanol's weak glomeruli sit low on the transform, where the same
division leaves less, and its weak fills (odor_probe50.py) add little of their own.

    python experiments/odor_normalization_check.py [odor_probe51]     (writes experiments/odor_normalization_check[_<model>].json)
"""
from __future__ import annotations

import importlib
import json
import sys
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe10 as p10
import odor_probe24 as p24
import odor_probe44 as p44
import warm
from brainfly import odors
from brainfly.hybrid import consensus_transmitters

SEED, SEEDS = 600000, 2
GLOMERULI = ("VM7d", "DL5")
RATES = (10.0, 20.0, 80.0)
LEVELS = (0.0, 133.0, 228.0, 418.0, 912.0)
PUBLIC = "pentyl acetate"
FLIES = {"VM7d": {"77 (0.47 Rmax)": (1.0, 0.66, 0.47, 0.22, 0.10), "135 (0.83)": (1.0, 0.90, 0.84, 0.67, 0.55),
                  "161 (0.99)": (1.0, 1.02, 0.98, 0.91, 0.80)},
         "DL5": {"41 (0.25)": (1.0, 0.66, 0.44, 0.2, None), "83 (0.50)": (1.0, 0.75, 0.65, 0.54, None),
                 "147 (0.88)": (1.0, 0.94, 0.88, 0.76, None)}}


def run(o, rec, olsen, g: str, x: float, pattern: dict, level: float, pns: np.ndarray, seed: int) -> float:
    """The PNs' window mean less their rest, with g at x and the public pattern scaled to `level` summed Hz."""
    b = o.brain
    base = p24.spontaneous(rec)
    grid = np.arange(0, olsen.POST_S, p10.PIECE) + p10.PIECE / 2
    window = grid < olsen.WINDOW_S
    private = olsen.olsen_shape(grid, x)
    private *= x / float(private[window].mean())
    strong = olsen.olsen_shape(grid, 40.0)
    strong /= float(strong[window].mean())                 # window mean 1
    total = sum(pattern.values())
    lateral = {h: level * v / total for h, v in pattern.items()} if total > 0 else {}
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(0.5 / b.dt)), drive=base)
    piece = int(round(p10.PIECE / b.dt))
    n_pre = int(round(olsen.PRE_S / p10.PIECE))
    counts = [float(b.advance(piece, drive=base)[:, pns].mean()) for _ in range(n_pre)]
    for k in range(len(grid)):
        drive = []
        for h in rec.glomeruli:
            if not len(rec.cells[h]):
                continue
            extra = private[k] if h == g else lateral.get(h, 0.0) * strong[k]
            drive.append((rec.cells[h], max(rec.spont[h] + extra, 0.0)))
        counts.append(float(b.advance(piece, drive=drive)[:, pns].mean()))
    hz = np.array(counts) / p10.PIECE
    return float(hz[n_pre:n_pre + int(round(olsen.WINDOW_S / p10.PIECE))].mean() - hz[:n_pre].mean())


def main() -> None:
    t0 = time.perf_counter()
    name = sys.argv[1] if len(sys.argv) > 1 else "odor_probe49"
    probe = importlib.import_module(name)
    o, rec, built = brain_cache.load(name, probe.build, p44.prepare)
    import odor_olsen_protocol_check as olsen               # after the cache, so that its edits don't invalidate it
    out_path = Path(__file__).with_name(Path(__file__).stem + ("" if name == "odor_probe49" else f"_{name[len('odor_'):]}") + ".json")
    types, m = o.types, o.m
    cholinergic = np.asarray(consensus_transmitters()) == "acetylcholine"
    public = {h: v * p10.PEAK_HZ for h, v in odors.glomeruli(PUBLIC).items() if h in rec.cells and len(rec.cells[h])}
    out = {"question": __doc__, "model": name, "levels_hz": LEVELS, "rates_hz": RATES, "flies": FLIES, "glomeruli": {}}
    with warm.tracking(o, rec):
        for gi, g in enumerate(GLOMERULI):
            pns = np.flatnonzero(m["upn"] & np.char.startswith(types, f"{g}_"))
            pns = pns[cholinergic[pns]]
            pattern = {h: v for h, v in public.items() if h != g}
            rows = {}
            for ri, x in enumerate(RATES):
                means = [float(np.mean([run(o, rec, olsen, g, x, pattern, lv, pns, SEED + 1000 * gi + 100 * ri + 10 * li + s)
                                        for s in range(SEEDS)])) for li, lv in enumerate(LEVELS)]
                rows[f"{x:g}"] = {"window_mean_hz": [round(v, 1) for v in means],
                                  "kept": [round(v / means[0], 3) if means[0] > 0 else None for v in means]}
                print(g, f"x={x:g}", json.dumps(rows[f"{x:g}"]), flush=True)
            out["glomeruli"][g] = {"pns": int(len(pns)), "public_pattern_glomeruli": len(pattern), "rates": rows}
            out_path.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    out_path.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
