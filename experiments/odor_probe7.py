"""Exploratory, not pre-registered: odor_probe3.py to odor_probe6.py's olfactory pathway rebuilt with three corrections
and measured as the flies were. How close do Kenyon cells and MBON11 come to the flies' numbers?

Corrections, found on checking those probes:
  - ORN to PN. Kazama & Wilson 2008's 6.19 mV unitary EPSP is between an ORN and a PN of the same glomerulus. Those
    connections average 32 synapses in MaleCNS (Tobin et al. 2017 counted about 23 in DM6). odor_probe3.py averaged over
    every ORN-to-uniglomerular-PN connection, a quarter of which join different glomeruli with about 2 synapses (8% of
    the weight), so its factor was 8.8. Here the factor makes the mean same-glomerulus connection's rested peak PSP
    6.19 mV (7.3), applied to every ORN-to-PN synapse.
  - PN to KC. The factor setting the mean connection to Turner et al. 2008's 1.4 mV now averages and scales only the
    excitatory connections (0.4% are from GABAergic PNs, left as they were).
  - Odors. brainfly.odors now gives a receptor DoOR maps to two glomeruli, or to a pair of subdivisions, to both
    (Or33b: DM5 and DM3; Ir75b, Ir75c and the ac3A neuron: DL2d and DL2v); before, they drove nothing.
Measured as the flies were:
  - Kenyon cells as Turner et al. 2008 did: a 0.5 s odor; spikes in 200 ms bins; a cell responds if, on at least half of
    the flies, some bin within 2 s of the odor's onset exceeds its baseline's mean by 3.5 SD (baseline: the five 200 ms
    bins of the second before the odor, over all flies); spikes per response are the responding cells' spikes in those
    2 s less twice their rest second's, mean over flies, by class. Flies: 6 +- 5% of Kenyon cells respond to a given
    odor; alpha/beta cells fire 2.2 +- 1.2 spikes per response, alpha'/beta' ones 4.9 +- 3.0.
  - MBON11 as Hige et al. 2015 did: a 1 s odor; spikes from 0 to 1.4 s after onset, less 1.4 s of its spontaneous rate
    (from the second before the odor); mean over flies and both cells. Flies, before pairing: 118 +- 8.3 spikes to
    3-octanol and 110 +- 11 to 4-methylcyclohexanol (mean +- SEM, n = 7). The comparison odor_probe3.py to
    odor_probe6.py used, about 37 Hz at rest to 57 at an odor's onset, combined a resting rate from voltage imaging on a
    trackball (Huang et al. 2024) with an onset rate read off a figure of 15 s odors; it isn't the pairing experiment's.
Conditions (each Kenyon cell rest set again to 21.5 mV below threshold where marked, as odor_probe3.py):
  rung 4 brain              rung4_scaling.py's intact brain, unchanged
  measured receptor input   ORN-to-PN synapses at 6.19 mV per same-glomerulus connection; Kenyon cells' rest set
  + Turner's Kenyon cells   Kenyon cells' membrane time constant 11.5 ms (their EPSPs' decay), excitatory PN-to-KC
                            connections at 1.4 mV mean, undepressed (Turner's model; no fly data, none in locusts)
  + undepressed outputs     Kenyon cell to MBON synapses undepressed too: the current model (odor_probe6.py's)
  current, PN-KC depressed  the current model with PN-to-KC synapses keeping the PNs' depression
The two undepressed choices have no fly measurement behind them and were made after seeing the depressed versions
fall silent (odor_probe5.py, odor_probe6.py), so they are informed by the outcome; the last condition shows how much
the first matters.
Odors: 3-octanol (OCT), 4-methylcyclohexanol (MCH), ethyl acetate, isopentyl acetate, benzaldehyde, 2-heptanone, each
glomerulus's receptor neurons at its DoOR response times 200 Hz. 8 flies; seeds 10000 + 100 x condition + odor
(Turner's protocol), + 50 + odor (Hige's), + 90 (Kenyon cells' rest), + 95 (the resting brain).
Also reported: the driven PNs' rates (glomeruli above 0.2; first 100 ms and the odor's second, Hige's protocol), APL's
release, the share of Kenyon cells with at least one extra spike in the 1 s odor in at least half the flies (the
earlier probes' measure), the overlap (Jaccard) of the responding Kenyon cells between odors, and MBON01's and
MBON18's responses. Known gap: receptor neurons are silent at rest here, while flies' fire a few spikes a second, which
holds their synapses partly depressed when an odor arrives.

Ran: the projection neurons are right; the Kenyon cells respond too densely and in the wrong classes, and MBON11
hears them ten to fifty times too faintly. The factors: 7.3 for ORN to PN (12,393 same-glomerulus connections of
16,265, 32 synapses each on average) and 0.28 for PN to KC. Over the six odors:
  rung 4 brain              21-35% of Kenyon cells pass Turner's criterion, each firing under one extra spike (0.6-0.8):
                            a single, reliable spike at the odor's onset. PNs 70-86 Hz in the first 100 ms, 20-28 Hz
                            over the second. MBON11 gains 0.3-1.1 spikes.
  measured receptor input   PNs 162-181 Hz in the first 100 ms and 86-97 over the second. 32-51% of Kenyon cells
                            respond, still under one spike each. MBON11 -0.4 to 1.5.
  + Turner's Kenyon cells   11-31%; alpha/beta 2.5-4.2 spikes per response, alpha'/beta' 1.0-1.4, gamma 1.9-3.1.
                            MBON11 1.5-4.1.
  + undepressed outputs     11-30% (MCH 10.8%, OCT 20.3%, ethyl acetate 29.5%). By class, alpha/beta 11-39%,
                            alpha'/beta' 2-5%, gamma 15-29%, where Turner's flies (derived from his Fig. 2D) show
                            alpha'/beta' most (about 9-14%), alpha/beta 3-8% and gamma about 2%. Spikes per response:
                            alpha/beta 2.5-4.4 (flies 2.2 +- 1.2), alpha'/beta' 1.0-1.4 (4.9 +- 3.0), gamma 1.9-3.2.
                            Responding cells overlap between odors by a Jaccard index of 0.26-0.76 (mean 0.52; OCT and
                            MCH 0.42). APL releases 11-38 Hz in the first 100 ms. MBON11 gains 2.3-11.0 spikes (OCT 4.1,
                            MCH 2.3; flies 118 and 110), MBON18 3.7-21.2, MBON01 2.6-7.5.
  current, PN-KC depressed  1.4-2.6% respond, under one extra spike each; the MBONs don't move.
The resting brain stays at 0.95-0.98 Hz with no neuron over 100 Hz in every condition.

    python experiments/odor_probe7.py          (writes experiments/odor_probe7.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe4 as p4
import odor_probe5 as p5
import rung4_scaling as r4s
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
ODORS = p3.ODORS
CLASSES = {"alpha/beta": "KCab", "alpha'/beta'": "KCa'b'", "gamma": "KCg"}
MBONS = ("MBON11", "MBON01", "MBON18")
FLIES = {"kc_share": "6 +- 5%", "spikes_per_response": {"alpha/beta": "2.2 +- 1.2", "alpha'/beta'": "4.9 +- 3.0"},
         "MBON11_evoked_spikes": {"3-octanol": "118 +- 8.3", "4-methylcyclohexanol": "110 +- 11"}}
CONDITIONS = {"rung 4 brain": dict(orn=False, rest=False, turner=False, pnkc_full=False, kcmbon_full=False),
              "measured receptor input": dict(orn=True, rest=True, turner=False, pnkc_full=False, kcmbon_full=False),
              "+ Turner's Kenyon cells": dict(orn=True, rest=True, turner=True, pnkc_full=True, kcmbon_full=False),
              "+ undepressed outputs": dict(orn=True, rest=True, turner=True, pnkc_full=True, kcmbon_full=True),
              "current, PN-KC depressed": dict(orn=True, rest=True, turner=True, pnkc_full=False, kcmbon_full=True)}
CURRENT = "+ undepressed outputs"
BIN = 0.2


class Olfaction:
    """rung4_scaling.py's intact brain with the olfactory pathway's measured properties switchable (CONDITIONS)."""

    def __init__(self):
        self.s = r4s.prepare("intact")[0]
        b = self.brain = self.s.brain
        self.types = np.asarray(self.s.types).astype(str)
        self.m = m = p3.masks(self.types)
        self.w0, self.bias0 = b.weights.copy(), self.s.bias[self.s.gid].astype(np.float64)
        self.tau0 = b.params[b.cls[np.flatnonzero(m["kc"])[0]]]["tau_m"]
        pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
        self.orn_pn = p3.edges(b, m["orn"], m["upn"])
        e = np.flatnonzero(self.orn_pn)                       # ORN_<glomerulus> onto <glomerulus>_<kind>PN
        glom_pre = np.array([t[4:] for t in self.types[pre[e]]])
        glom_post = np.array([t.split("_")[0] for t in self.types[b.idx[e]]])
        same = np.zeros_like(self.orn_pn)
        same[e[glom_pre == glom_post]] = True
        self.orn_factor = p3.UNITARY_MV / (p3.PEAK * float(self.w0[same].mean()))
        self.pn_kc = p3.edges(b, m["upn"], m["kc"]) & (self.w0 > 0)
        self.kc_factor = p5.KC_UNITARY_MV / (p5.peak(p5.KC_TAU) * float(self.w0[self.pn_kc].mean()))
        self.kc_mbon = p3.edges(b, m["kc"], np.char.startswith(self.types, "MBON"))
        self.facts = {"orn_pn_same_glomerulus": {"connections": int(same.sum()), "of": int(self.orn_pn.sum()),
                                                 "mean_synapses": round(float(b._counts[same].mean()), 1),
                                                 "factor": round(self.orn_factor, 3)},
                      "pn_kc_excitatory": {"connections": int(self.pn_kc.sum()), "factor": round(self.kc_factor, 3)}}

    def set(self, name: str, seed: int) -> list:
        """Put the brain in condition `name`; returns the Kenyon cells' rest calibration, if any."""
        c, b, m = CONDITIONS[name], self.brain, self.m
        w = self.w0.copy()
        if c["orn"]:
            w[self.orn_pn] *= self.orn_factor
        if c["turner"]:
            w[self.pn_kc] *= self.kc_factor
        b.weights, b._external_matrix = w.astype(np.float32), None
        p4.set_kc_tau(b, m["kc"], p5.KC_TAU if c["turner"] else self.tau0)
        b.full_strength[:] = (self.pn_kc if c["pnkc_full"] else False) | (self.kc_mbon if c["kcmbon_full"] else False)
        bias = self.bias0.copy()
        b.set_bias(bias)
        return p3.set_kc_rest(self.s, m["kc"], self.types, bias, seed)[-1] if c["rest"] else []


def run(o: Olfaction, odor: str, seed: int, seconds: float, after: float, silence=(), max_hz: float = p3.MAX_HZ) -> dict:
    """1 s to settle and 1 s of rest, then the odor for `seconds` and `after` more, in 10 ms pieces: spike counts per
    neuron (rest, the first 100 ms, the odor, the whole window), the Kenyon cells' counts per 200 ms bin (rest's five,
    then the window's), and APL's release (first 100 ms, the odor), each per fly. silence: neurons silenced throughout
    (HybridBrain.advance's); max_hz: the receptor neurons' rate at a DoOR response of 1."""
    b = o.brain
    kc = np.flatnonzero(o.m["kc"])
    apl = np.searchsorted(b.graded, b.cells(["APL"]))
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), silence=silence)
    piece = int(round(0.01 / b.dt))
    per_bin = int(round(BIN / 0.01))
    rest_bins = [b.advance(int(round(BIN / b.dt)), silence=silence) for _ in range(int(round(1.0 / BIN)))]
    rest = sum(rest_bins)
    drive = odors.orn_drive(b, odor, max_hz)
    n_odor, n_all = int(round(seconds / 0.01)), int(round((seconds + after) / 0.01))
    total, first, during, bins, cur, release = np.zeros_like(rest), None, None, [], np.zeros_like(rest[:, kc]), []
    for k in range(n_all):
        c = b.advance(piece, drive=drive if k < n_odor else (), silence=silence)
        total += c
        cur += c[:, kc]
        if k < n_odor:
            release.append(float(b.release[:, apl].mean()))
        if k == 9:
            first = total.copy()
        if k == n_odor - 1:
            during = total.copy()
        if (k + 1) % per_bin == 0:
            bins.append(cur.copy())
            cur[:] = 0
    return {"rest": rest, "rest_bins": np.stack([r[:, kc] for r in rest_bins], 1), "first": first, "odor": during,
            "window": total, "bins": np.stack(bins, 1),
            "apl": [round(float(np.mean(release[:10])), 1), round(float(np.mean(release)), 1)]}


def turner_responders(r: dict) -> np.ndarray:
    """Turner et al. 2008's criterion over the Kenyon cells: some 200 ms bin within the window above the baseline
    bins' mean + 3.5 SD, on at least half of the flies."""
    base = r["rest_bins"].reshape(-1, r["rest_bins"].shape[2])                # (flies x 5, kc)
    theta = base.mean(0) + 3.5 * base.std(0)
    hit = (r["bins"] > theta).any(1)                                          # (flies, kc)
    return hit.mean(0) >= 0.5


def measure_odor(o: Olfaction, odor: str, turner_seed: int, hige_seed: int, silence=(), max_hz: float = p3.MAX_HZ):
    """One odor's measures (see the docstring) and its Kenyon cells responding by Turner's criterion."""
    types, m = o.types, o.m
    kc = np.flatnonzero(m["kc"])
    kc_types = types[kc]
    t = run(o, odor, turner_seed, 0.5, 1.5, silence, max_hz)                  # Turner's protocol
    resp = turner_responders(t)
    extra = (t["window"][:, kc] - 2 * t["rest"][:, kc]).mean(0)
    h = run(o, odor, hige_seed, 1.0, 0.4, silence, max_hz)                    # Hige's protocol
    evoked = h["window"] - 1.4 * h["rest"]
    gl = [g for g, v in odors.glomeruli(odor).items() if v > 0.2]
    pn = np.isin(types, [f"{g}_{x}" for g in gl for x in p3.PN_SUFFIX])
    one = ((h["odor"][:, kc] - h["rest"][:, kc]) >= 1).mean(0) >= 0.5
    row = {"kc_share": round(float(resp.mean()), 4),
           "kc_share_by_class": {cl: round(float(resp[np.char.startswith(kc_types, p)].mean()), 4) for cl, p in CLASSES.items()},
           "spikes_per_response": {cl: (round(float(extra[resp & np.char.startswith(kc_types, p)].mean()), 2)
                                        if (resp & np.char.startswith(kc_types, p)).any() else None) for cl, p in CLASSES.items()},
           "kc_share_1spike_1s": round(float(one.mean()), 4),
           "evoked_spikes_0_1.4s": {x: round(float(evoked[:, types == x].mean()), 1) for x in MBONS},
           "pn_hz": {"rest": round(float(h["rest"][:, pn].mean()), 2), "first_100ms": round(float(h["first"][:, pn].mean() / 0.1), 1),
                     "odor_second": round(float(h["odor"][:, pn].mean()), 1), "count": int(pn.sum()), "glomeruli": len(gl)},
           "apl_release_hz": {"turner": t["apl"], "hige": h["apl"]}}
    return row, resp


def rest_measures(o: Olfaction, seed: int, silence=()) -> dict:
    b, types, m = o.brain, o.types, o.m
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), silence=silence)
    rest = b.advance(int(round(1.0 / b.dt)), silence=silence).mean(0)
    return {"brain_hz": round(float(rest.mean()), 3), "over_100hz": int((rest > 100).sum()),
            "kc_hz": round(float(rest[m["kc"]].mean()), 3), "upn_hz": round(float(rest[m["upn"]].mean()), 2),
            **{f"{x}_hz": round(float(rest[types == x].mean()), 2) for x in MBONS}}


def overlaps(responders: dict) -> dict:
    names = list(responders)
    return {f"{a} | {z}": round(float((responders[a] & responders[z]).sum() / max((responders[a] | responders[z]).sum(), 1)), 3)
            for i, a in enumerate(names) for z in names[i + 1:]}


def condition(o: Olfaction, name: str, c: int) -> dict:
    base = 10000 + 100 * c
    out = {"kc_rest_calibration": o.set(name, base + 90)}
    out["rest"] = rest_measures(o, base + 95)
    out["odors"], responders = {}, {}
    for k, odor in enumerate(ODORS):
        row, responders[odor] = measure_odor(o, odor, base + k, base + 50 + k)
        out["odors"][odor] = row
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "spikes_per_response", "evoked_spikes_0_1.4s", "pn_hz")}), flush=True)
    out["overlap_jaccard"] = overlaps(responders)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = Olfaction()
    out = {"question": __doc__, "flies": FLIES, **o.facts, "kc_total": int(o.m["kc"].sum()), "conditions": {}}
    print(json.dumps(o.facts), flush=True)
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = condition(o, name, c)
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
