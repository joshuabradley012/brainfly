"""Exploratory check, not pre-registered: how far do the model's projection neurons depolarize at rest when the antennal
lobe's GABA receptors are blocked, against flies' 5-8 mV? And do its DM1 PNs rest nearly silent, as flies' do?

research_notes/Rung 9 learning data/orn_pn_resting_state.md (2026-10-10): Nagel, Hong & Wilson 2015 found that picrotoxin
(5 uM) with CGP54626 (50 uM) "depolarized the mean PN membrane potential even in the absence of odors", by about 5-8 mV
in 17 PNs of DM6, VM2 and VM7 (their Figs. 3b and 7a, read from the figures). Their model, whose only inhibition is
presynaptic and divides release by the LNs' resting rate (a divisor of about 4-5), moves its baseline about 7.5 mV.
brainfly's presynaptic inhibition acts only on the LNs' activity above their resting rate (odor_probe27.py's choice:
"flies have little tonic presynaptic inhibition"), so at rest only the LNs' synapses onto the PNs and other LNs inhibit.
DM1 PNs fire "close to zero" spontaneously in flies (Gaudry et al. 2013), although DM1 has 68-86 receptor neurons firing
9-15 spikes/s.
Model: odor_probe56.py's (its cache). Conditions, each settled as the model settles (warm.settled) and measured over 1 s
from it, 2 seeds of 8 flies: intact; GABA receptors blocked, as a bath of the two antagonists blocks them on their
targets: every GABAergic synapse (fast and slow) onto the antennal lobe's PNs and LNs removed and the presynaptic
inhibition off; the same with the glutamatergic synapses onto them removed too (picrotoxin also blocks the
glutamate-gated chloride channels the glutamatergic LNs act through; Liu & Wilson 2013); and every receptor neuron
silenced (as odor_resting_drive_check.py, for the resting drive by glomerulus with inhibition intact; flies about 7-10 mV
for most glomeruli by the note's section 1.6, Gouwens & Wilson's 5-10 mV over all).
Measured: the cholinergic uniglomerular PNs' mean membrane potential and rate, over all and by glomerulus (DM6, VM2 and
VM7, Nagel et al.'s, and others), and the GABAergic and glutamatergic LNs' rates; and the receptor synapses' resting
efficacy by glomerulus (each spike's strength as a fraction of the rested, uninhibited one: sum over the two pools of
weight / (D + u r tau), D the resting presynaptic divisor; the note's conventions), against flies' DM4 0.26 (Kazama &
Wilson 2008) and DM6 0.41-0.56 (Gaudry et al. 2013, an upper bound). measure() serves other models' checks too.

Ran (odor_probe56.py's model): its PNs disinhibit at rest about half as much as flies', and all of that is postsynaptic.
Blocking GABA raises the cholinergic PNs 3.1 mV in DM6, VM2 and VM7 (2.4-3.6 mV each; flies 5-8) and 2.5 mV over all
(5th-95th percentile by glomerulus 1.2-3.6), their rate from 5.05 to 11.95 spikes/s; adding the glutamate-gated channels
changes it little (3.2 mV). The model has no tonic presynaptic inhibition (resting divisor 1.0), so this is the LNs'
synapses onto the PNs and LNs alone. Silencing every receptor neuron drops the PNs 24.8 mV (27.3 in DM6, VM2 and VM7;
DM4 13.2, DL5 19.0, DM1 18.3), several times the note's 6-8 mV estimates for most of them. DM1's PNs rest at 5.3
spikes/s like the others (the polish gives every uniglomerular PN the same target), where flies' are nearly silent. The
receptor synapses keep 0.37 of their strength at rest (0.32 in the palps' VM7, at 8 spikes/s), from the class median
rates: at DM4's measured 3.44 spikes/s they would keep 0.47 (flies 0.26), and at DM6's 2.2, 0.54 (flies 0.41-0.56).

    python experiments/odor_gaba_block_check.py      (writes experiments/odor_gaba_block_check.json)
"""
from __future__ import annotations

import contextlib
import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_eln_check as ec
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe24 as p24
import odor_probe44 as p44
import odor_probe56 as p56
import warm
from brainfly.hybrid import consensus_transmitters

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 760000, 2
FLIES_MV = (5.0, 8.0)                                  # Nagel, Hong & Wilson 2015 (DM6, VM2, VM7)
SHOWN = ("DM6", "VM2", "VM7d", "VM7v", "DM4", "DL5", "DM1", "DA1", "DL1", "VA6", "DM2")
FLY_EFFICACY = {"DM4": 0.26, "DM6": (0.41, 0.56)}


@contextlib.contextmanager
def blocked(b, sources: np.ndarray, targets: np.ndarray):
    """Synapses from `sources` onto `targets` (fast and slow) removed and the presynaptic inhibition off; put back after."""
    weights, slow, pre = b.weights, b.slow_weights, b._presynaptic
    src, tgt = np.zeros(b.n, bool), np.zeros(b.n, bool)
    src[sources], tgt[targets] = True, True
    col = np.repeat(np.arange(b.n), np.diff(b.ptr))
    scol = np.repeat(np.arange(b.n), np.diff(b.sptr))
    b.weights = np.where(src[col] & tgt[b.idx], np.float32(0), weights).astype(np.float32)
    b.slow_weights = np.where(src[scol] & tgt[b.sidx], np.float32(0), slow).astype(np.float32)
    b._presynaptic = None
    try:
        yield int((src[col] & tgt[b.idx]).sum() + (src[scol] & tgt[b.sidx]).sum())
    finally:
        b.weights, b.slow_weights, b._presynaptic = weights, slow, pre


def resting_efficacy(o, rate: float) -> float:
    """The receptor synapses' mean strength per spike at a steady Poisson rate, as a fraction of the rested, uninhibited
    strength, from their pools (fraction released u, recovery tau) and the resting presynaptic divisor D (release and
    depletion both divided): sum of weight / (D + u rate tau)."""
    b = o.brain
    orn = np.flatnonzero(o.m["orn"])
    p = b.params[int(np.bincount(b.cls[orn]).argmax())]
    d = 1.0 / warm.resting_gain(b)
    share = p["share2"]
    pools = [(1 - share, 1 - p["depression"], p["recovery"]), (share, 1 - p["depression2"], p["recovery2"])]
    return float(sum(w / (d + u * rate * tau) for w, u, tau in pools if w > 0))


def measure(o, rec, seed: int = SEED) -> dict:
    """The conditions above on the model (o, rec), each settled as it settles and measured over 1 s, SEEDS seeds."""
    b = o.brain
    nt = np.asarray(consensus_transmitters())
    gloms = [g for g in rec.glomeruli if len(rec.cells[g])]
    pn_of = {g: np.flatnonzero(o.m["upn"] & (nt == "acetylcholine") & np.char.startswith(o.types, f"{g}_")) for g in gloms}
    pn_of = {g: v for g, v in pn_of.items() if len(v)}
    upn = np.concatenate(list(pn_of.values()))
    ln = np.array([bool(p14.LN.match(t)) for t in o.types])
    gaba_ln, glu_ln = np.flatnonzero(ln & (nt == "gaba")), np.flatnonzero(ln & (nt == "glutamate"))
    targets = np.flatnonzero(o.m["upn"] | ln)
    gaba, glu = np.flatnonzero(nt == "gaba"), np.flatnonzero(nt == "glutamate")
    piece = int(round(p10.PIECE / b.dt))
    out = {"resting_divisor": round(1.0 / warm.resting_gain(b), 3),
           "resting_efficacy": {g: round(resting_efficacy(o, rec.spont[g]), 3) for g in SHOWN if g in rec.spont},
           "spontaneous_hz": {g: rec.spont[g] for g in SHOWN if g in rec.spont}, "fly_efficacy": FLY_EFFICACY, "conditions": {}}
    conditions = (("intact", None), ("GABA receptors blocked", gaba),
                  ("GABA and glutamate-gated chloride blocked", np.concatenate([gaba, glu])), ("receptor neurons silenced", "orn"))
    for c, (name, sources) in enumerate(conditions):
        if sources is None:
            block = contextlib.nullcontext(0)
        elif isinstance(sources, str):
            block = ec.silenced(rec, gloms)
        else:
            block = blocked(b, sources, targets)
        with block as removed, warm.settled(o, rec):
            u, hz = np.zeros(b.n), np.zeros(b.n)
            for s in range(SEEDS):
                b.reset(seed + 100 * c + s)
                b.set_release(o.s.ol.neurons, o.s.silent)
                drive = p24.spontaneous(rec)
                for _ in range(100):
                    cnt = b.advance(piece, drive=drive)
                    u += b.u.mean(0) / (100 * SEEDS)
                    hz += cnt.mean(0) / SEEDS
        out["conditions"][name] = {"synapses_removed": removed or 0, "upn_u_mv": round(float(u[upn].mean()), 2),
                                   "upn_hz": round(float(hz[upn].mean()), 2), "gaba_ln_hz": round(float(hz[gaba_ln].mean()), 2),
                                   "glu_ln_hz": round(float(hz[glu_ln].mean()), 2),
                                   "by_glomerulus_u_mv": {g: round(float(u[v].mean()), 2) for g, v in pn_of.items()},
                                   "by_glomerulus_hz": {g: round(float(hz[v].mean()), 2) for g, v in pn_of.items()}}
        r = out["conditions"][name]
        print(name, json.dumps({k: v for k, v in r.items() if not k.startswith("by_")}),
              "| DM1, DM6, VM2, VM7d, VM7v Hz:", [r["by_glomerulus_hz"].get(g) for g in ("DM1", "DM6", "VM2", "VM7d", "VM7v")], flush=True)
    a = out["conditions"]["intact"]
    for name in list(out["conditions"])[1:]:
        d = out["conditions"][name]
        change = {g: round(d["by_glomerulus_u_mv"][g] - a["by_glomerulus_u_mv"][g], 2) for g in pn_of}
        vals = np.array(list(change.values()))
        d["change_mv"] = {"all": round(d["upn_u_mv"] - a["upn_u_mv"], 2), "nagel_glomeruli": round(float(np.mean(
            [change[g] for g in ("DM6", "VM2", "VM7d", "VM7v") if g in change])), 2),
            **{g: change.get(g) for g in SHOWN}, "quantiles_5_50_95": [round(float(x), 2) for x in np.percentile(vals, [5, 50, 95])]}
        print(name, "change", json.dumps(d["change_mv"]), "(flies: +5-8 mV blocked; about -7 to -10 silenced)", flush=True)
    print("resting divisor", out["resting_divisor"], "efficacy", json.dumps(out["resting_efficacy"]), flush=True)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe56", p56.build, p44.prepare)
    out = {"question": __doc__, "flies_mv": FLIES_MV, **measure(o, rec)}
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
