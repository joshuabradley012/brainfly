"""Exploratory check, not pre-registered: with the antennal lobe's excitatory local neurons driven as flies' are and
coupled electrically to the projection neurons at measured strength, does the model show flies' lateral excitation?

odor_probe55.py: with the receptor input the evidence supports, flies' PNs answer odors in many glomeruli that get no
receptor input, and the model's sit at rest. In flies, PNs whose own receptor neurons are silent or cut still answer
odors, through excitatory local neurons (eLNs) electrically coupled to them (Olsen et al. 2007; Yaksi & Wilson 2010;
Huang et al. 2010; Kazama et al. 2011; research_notes/Rung 9 learning data/lateral_excitation.md). The model removed the
cholinergic LNs' chemical synapses onto PNs (odor_probe14.py) and has no electrical ones. odor_lateral_check.py coupled
them both ways at unmeasured strengths and was stopped (the PN-to-eLN link is mostly chemical, which the model has).
Checked before this was written (on odor_probe54.py's model): the cholinergic LNs barely answer odors (1.9 Hz at rest,
2.7-4.7 over a 0.5 s odor; with the antennae removed 1.2-1.3 Hz for palp odors against 1.1 for none, where flies' eLNs
fire 5.6-11.2 against 3.7; Kazama et al. 2011), because their receptor neurons' synapses were never calibrated: 0.018
mV per synapse against the PNs' 1.14 (fitted to unitary EPSPs), so an LN gets 0.014 of a PN's summed antennal receptor
input, where flies' eLNs take about 4 times a PN's current from the same weak antennal nerve stimulation (Huang et al.
2010 Fig. S5; about 2.2-2.6 times in voltage, the eLNs' input resistance being 0.55-0.66 of the PNs').
Model: odor_probe54.py's (its cache). eLNs: the cholinergic antennal lobe LNs MaleCNS connects to uniglomerular PNs by at
least 5 chemical synapses (the note's contact criterion). Their receptor neurons' synapses are multiplied by g, and
their bias lowered by the mean input that adds at rest (each receptor neuron's spontaneous rate x the added weight x
its synapses' resting depression x the 5 ms synaptic time constant), so that they rest as before. Coupling: an
electrical synapse from each eLN onto each PN it contacts, one way; each eLN spike raises the PN by k mV at once,
decaying with the PN's 20 ms membrane time constant (paired recordings: 0.42 mV at the spike-triggered average's peak,
bounds 0.17-1 mV; lateral_excitation.md section 8.1), and each PN's bias lowered by the mean input that gives it at
rest (the eLNs' resting rates x k x 20 ms). With these contacts as the coupling, the per-glomerulus strength ranks as
flies' lateral excitation does (Olsen et al. 2007 Fig. 8C; Spearman 0.87 over 12 glomeruli, from the connectome before
this ran); DM1, where flies' is weakest (Yaksi & Wilson 2010), has the most contacts, and DA1, DL3, DA2 and DA3, where
Badel et al.'s PNs answer many odors, the fewest.
Stage 1, the eLNs' gain: k = 0, g = 1, 10, 30, 100 or 300. Measured: the eLNs' rates with the antennal receptor neurons
silenced, for palp odors (pentyl acetate, ethyl acetate, methyl salicylate) and none (Kazama et al. 2011, acute: 5.6,
6.0, 11.2 and 3.7 Hz), and in the intact model for Yaksi & Wilson's odors (ethyl acetate, pentyl acetate, methyl
salicylate, heptanoic acid, ethyl cinnamate; flies' eLNs depolarize 7-11 mV at the peak for all of them, spikes
filtered, though their receptor input spans more than 7-fold), with the GABAergic LNs' and PNs' rates. Chosen, as
stated before running: the g at which the eLNs' mean rise over the three palp odors, less none, matches flies' (3.9 Hz),
interpolated in log g; stage 2 runs only if the gains bracketing it leave the eLNs' intact resting rate within twice
g = 1's (a gain that only works by running the eLNs away at rest isn't flies' eLN).
Stage 2, the coupling: at that g, k = 0, 0.2, 0.4 or 0.8 mV. Measured (as T13 to T2 below; the model's odor onset taken
as 100 ms after the valve, as odor_olsen_protocol_check.py takes it; depolarizations are the cholinergic PNs' mean
membrane potential relative to the 400 ms before the odor; removing an organ silences its receptor neurons'
spontaneous and odor firing, and the antennal lobe settles without them first, as flies' recordings began 10-20 min
after the cut):
  rest  the PNs', eLNs' and GABAergic LNs' resting rates.
  T13   Kazama et al. 2011, acute. Antennal receptor neurons silenced, palp odors (pentyl acetate, ethyl acetate,
        methyl salicylate, none): VM2's PNs (flies 2.5, 1.8, 1.4 and 0.8 mV) and all antennal PNs (2.6, 2.7, 1.5 and
        0.3 mV); palp receptor neurons silenced, antennal odors: VM7d's PNs (4.9, 5.1, 3.9 and 4.3 mV). All over
        100-600 ms after the valve.
  T1    Olsen et al. 2007. Antennal receptor neurons silenced; ethyl butyrate, 2-heptanone, benzaldehyde: the antennal
        PNs' peak depolarization (50 ms running mean; flies 7.3, 7.5 and 6.3 mV at 125-175 ms) and at 500 ms (3.9, 3.1
        and 2.4 mV).
  T5    Yaksi & Wilson 2010. Palp receptor neurons silenced; antennal odors (ethyl acetate, pentyl acetate, methyl
        salicylate, heptanoic acid, ethyl cinnamate): VC1's and VC2's PNs over 100-300 ms after the valve (flies 2.6,
        3.3, 3.1, 2.6 and 2.4 mV). Antennal receptor neurons silenced, the same odors: DM1's (1.1, 0.65, 0.1, 0.2 and
        0.1 mV).
  T7    Olsen et al. 2007. VM2's and DL1's receptor neurons silenced (the Or43b and Or10a mutants), 13 odors: their
        PNs' rates over the 500 ms odor less before (flies: VM2 6-32 Hz, mean 16.7; DL1 5-26 Hz, mean 13.2; every odor
        positive), and with their receptor neurons working (flies' means 72.8 and 34.2 Hz).
  T2    Olsen et al. 2007. Every receptor neuron silenced except VA7l's; VA7l's driven 3, 10, 56 or 147 Hz above its
        spontaneous rate for 500 ms. Measured: the antennal PNs' depolarization area over 100-600 ms after the valve
        (flies -0.02, 1.54, 1.81 and 1.88 mV s, half-maximal at about 7 Hz), and per glomerulus at 147 Hz (flies'
        Fig. 8C: VC4 3.03, DL5 2.68, DL1 2.37, VM5v 2.09, DM3 1.90, DC3 1.74, VM3 1.69, VC3 1.64, VM2 1.57, VA1v 1.57,
        VA1d 1.46, DM6 1.26 mV s).
Chosen, as stated before running: the k at which the model's mean T13 depolarization (its nine odor values) matches
flies' (2.93 mV), interpolated linearly in k between the conditions; everything else is then a test.

Ran (stage 1; stopped by its rule, so the coupling wasn't run): no gain makes the model's cholinergic LNs answer as
flies' eLNs do. Multiplying their receptor neurons' synapses by 10, 30, 100 or 300 (their summed antennal receptor input
then 0.14, 0.43, 1.4 and 4.3 times a PN's) raises their rise to the three palp odors with the antennae removed from 0.05
Hz to only 0.18, 0.25, 0.37 and 0.49 (flies 1.9-7.5, mean 3.9), and drops their baseline there from 1.18 Hz to 0.45-0.63
(flies 3.7): held at their rest by a lower bias, they lean on the antennal receptor neurons' spontaneous firing, and the
palp receptor neurons give them little. In the intact model they answer more (x10: 23.7 Hz to ethyl acetate and 27.2 to
pentyl acetate, against 4.0 and 4.9; Huang et al.'s eLNs 20-35 Hz to preferred odors), but not alike (3.6 Hz to ethyl
cinnamate; flies' eLNs depolarize alike to all five odors), and from x30 they run away at rest (23-59 Hz; the mean-input
offset can't hold them against their input's fluctuations and their chemical excitation of each other), the GABAergic
LNs follow (7.3-8.9 Hz at rest, against 3.9) and the PNs fall silent. So the model's cholinergic LNs can't be made into
flies' eLNs through their receptor input: flies' keep firing without the antennae and answer palp odors and weak odors
alike, which takes input or excitability the model's lack. Which MaleCNS cells the eLNs are is itself uncertain
(lateral_excitation.md section 7: the acetylcholine label on lLN1_bc, the largest group here, rests on morphology, and
the LN1 and LN2 lines it's named for are about 95% GABAergic by staining). Lateral excitation waits on that.

Checked afterwards (2026-10-11; research_notes/Rung 9 learning data/lateral_pn_responses.md): flies' DA1, DL3 and DA2
PNs don't fire to general odors (lateral input reaches DA1 only as 5.7-6.2 mV of subthreshold depolarization when the
antennae are removed), and LNs largely skip that anterolateral cluster, as the connectome's sparse contacts there say;
so a connectome-based coupling that leaves them near rest matches flies. Lateral firing without receptor input is real
in VA6, VA1d, DL5 and DM3, which give an eLN model better held-out tests (that note's T20-T24).

    python experiments/odor_eln_check.py      (writes experiments/odor_eln_check.json)
"""
from __future__ import annotations

import contextlib
import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.stats import spearmanr

import brain_cache
import odor_probe10 as p10
import odor_probe14 as p14
import odor_probe44 as p44
import odor_probe54 as p54
import warm
from brainfly.hybrid import consensus_transmitters
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 710000, 2
GAINS = (1.0, 10.0, 30.0, 100.0, 300.0)
KICKS_MV = (0.0, 0.2, 0.4, 0.8)
MIN_SYNAPSES = 5
VALVE_S = 0.1                          # the model's odor onset after the valve (odor_olsen_protocol_check.LATENCY_S)
LEAD_S, PRE_S, ODOR_S, POST_S = 0.3, 0.5, 0.5, 0.3
PALP = ("VA4", "VA7l", "VC1", "VC2", "VM7d", "VM7v")          # odor_probe10.sensillum_class() == "pb"
PALP_ODORS = ("pentyl acetate", "ethyl acetate", "methyl salicylate")
T1_ODORS = ("ethyl butyrate", "2-heptanone", "benzaldehyde")
T5_ODORS = ("ethyl acetate", "pentyl acetate", "methyl salicylate", "heptanoic acid", "ethyl cinnamate")
T7_ODORS = ("methyl salicylate", "2,3-butanedione", "gamma-valerolactone", "ethyl acetate", "cyclohexanone",
            "3-methylthio-1-propanol", "benzaldehyde", "geranyl acetate", "Z3-hexenol", "4-methylphenol",
            "ethyl butyrate", "butyric acid", "1-butanol")
T2_RATES = (3.0, 10.0, 56.0, 147.0)
FLIES = {
    "eLN": {"rates, antennae removed": {"pentyl acetate": 5.6, "ethyl acetate": 6.0, "methyl salicylate": 11.2, "none": 3.7},
            "depolarization peak, intact": {"range": [7, 11]}, "weak-stimulation current over PNs'": 4.0},
    "T13": {"VM2, antennae removed": {"pentyl acetate": 2.5, "ethyl acetate": 1.8, "methyl salicylate": 1.4, "none": 0.8},
            "antennal PNs, antennae removed": {"pentyl acetate": 2.6, "ethyl acetate": 2.7, "methyl salicylate": 1.5, "none": 0.27},
            "VM7d, palps removed": {"pentyl acetate": 4.9, "ethyl acetate": 5.1, "methyl salicylate": 3.9, "none": 4.3}},
    "T1": {"peak": {"ethyl butyrate": 7.3, "2-heptanone": 7.5, "benzaldehyde": 6.3},
           "peak_ms_after_valve": {"ethyl butyrate": 125, "2-heptanone": 165, "benzaldehyde": 175},
           "at_500ms": {"ethyl butyrate": 3.9, "2-heptanone": 3.1, "benzaldehyde": 2.4}},
    "T5": {"VC1/VC2, palps removed": dict(zip(T5_ODORS, (2.6, 3.3, 3.1, 2.6, 2.4))),
           "DM1, antennae removed": dict(zip(T5_ODORS, (1.1, 0.65, 0.1, 0.2, 0.1)))},
    "T7": {"VM2 silent": {"mean": 16.7, "range": [6, 32]}, "DL1 silent": {"mean": 13.2, "range": [5, 26]},
           "VM2 working": {"mean": 72.8}, "DL1 working": {"mean": 34.2}},
    "T2": {"area_mv_s": dict(zip(("3", "10", "56", "147"), (-0.02, 1.54, 1.81, 1.88))),
           "fig8c_mv_s": {"VC4": 3.03, "DL5": 2.68, "DL1": 2.37, "VM5v": 2.09, "DM3": 1.90, "DC3": 1.74, "VM3": 1.69,
                          "VC3": 1.64, "VM2": 1.57, "VA1v": 1.57, "VA1d": 1.46, "DM6": 1.26}},
}
ELN_TARGET = float(np.mean([v - FLIES["eLN"]["rates, antennae removed"]["none"]
                            for od, v in FLIES["eLN"]["rates, antennae removed"].items() if od != "none"]))
T13_TARGET = float(np.mean([v for row in FLIES["T13"].values() for od, v in row.items() if od != "none"]))


def pairs(o) -> tuple:
    """(cholinergic LN, uniglomerular PN) for every pair MaleCNS connects by at least MIN_SYNAPSES chemical synapses
    (odor_probe14.py's edges, whose chemical weights the model holds at zero)."""
    b = o.brain
    edges = p14.cholinergic_ln_edges(o)
    assert not b.weights[edges].any()
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = edges & (b._counts >= MIN_SYNAPSES)
    return pre[e], b.idx[e]


def resting_strength(o, rec) -> np.ndarray:
    """Each receptor neuron's spike strength at its spontaneous rate (its pools' mean depression; warm.rest_depression)."""
    b = o.brain
    s = np.ones(b.n)
    g = warm.resting_gain(b)
    dep = np.zeros(b.n, bool) if b._presynaptic is None else np.asarray(b._presynaptic["depleting"], bool)
    for gl, cells in rec.cells.items():
        r = rec.spont[gl]
        for c in np.unique(b.cls[cells]):
            p, sel = b.params[c], cells[b.cls[cells] == c]
            gi = np.where(dep[sel], g, 1.0)
            pool = lambda f, tau: 1.0 / (1.0 + r * tau * (1 - f) * gi) if 0 < f < 1 else np.ones(len(sel))
            s1 = pool(p["depression"], p["recovery"])
            share = p.get("share2", 0.0)
            s[sel] = (1 - share) * s1 + share * pool(p.get("depression2", 1.0), p.get("recovery2", 1.0)) if share > 0 else s1
    return s


def gain_offset(o, rec, e: np.ndarray, w0: np.ndarray, g: float) -> np.ndarray:
    """The mean input at rest that multiplying the receptor-to-eLN synapses e by g adds to each neuron."""
    b = o.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))[e]
    rate = np.zeros(b.n)
    for gl, cells in rec.cells.items():
        rate[cells] = rec.spont[gl]
    s = resting_strength(o, rec)
    return np.bincount(b.idx[e], weights=(g - 1.0) * w0[e] * rate[pre] * s[pre] * TAU, minlength=b.n)


def couple(o, ln: np.ndarray, pn: np.ndarray, kick: float, ln_rest: np.ndarray) -> np.ndarray:
    """Electrical synapses eLN -> PN of `kick` mV per spike (csc: columns presynaptic); returns the mean input they give
    each PN at rest."""
    b = o.brain
    G = sparse.csc_matrix((np.full(len(ln), kick, np.float32), (pn, ln)), shape=(b.n, b.n)) if kick else \
        sparse.csc_matrix((b.n, b.n), dtype=np.float32)
    b.gptr, b.gidx, b.gap_mv = G.indptr, G.indices, G.data.astype(np.float32)
    tau = b.params[b.cls[pn[0]]]["tau_m"]
    return np.bincount(pn, weights=ln_rest[ln] * kick * tau, minlength=b.n)


@contextlib.contextmanager
def silenced(rec, gloms):
    """Within the block, these glomeruli's receptor neurons fire neither spontaneously nor to odors."""
    gloms = set(gloms)
    spont, plan = dict(rec.spont), rec.plan
    for g in gloms:
        rec.spont[g] = 0.0

    def quiet(odor, seconds, peak):
        p = plan(odor, seconds, peak)
        p["rows"] = [(g, 0.0 if g in gloms else v, lat) for g, v, lat in p["rows"]]
        return p
    rec.plan = quiet
    try:
        yield
    finally:
        rec.spont.clear()
        rec.spont.update(spont)
        del rec.plan


def trial(o, rec, drive_at, seed: int, sets: dict, elns: np.ndarray) -> dict:
    """Each set's mean membrane potential and rate in 10 ms pieces from -PRE_S to ODOR_S + POST_S around the model's
    odor onset, and each eLN's rate over the 400 ms before the odor."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(p10.PIECE / b.dt))
    t = -PRE_S - LEAD_S
    for _ in range(int(round(LEAD_S / p10.PIECE))):
        b.advance(piece, drive=drive_at(t))
        t += p10.PIECE
    n = int(round((PRE_S + ODOR_S + POST_S) / p10.PIECE))
    u = {k: np.zeros(n) for k in sets}
    hz = {k: np.zeros(n) for k in sets}
    eln_pre = np.zeros(len(elns))
    n_pre = int(round((PRE_S - 0.1) / p10.PIECE))
    for i in range(n):
        c = b.advance(piece, drive=drive_at(t))
        for k, cells in sets.items():
            u[k][i] = float(b.u[:, cells].mean())
            hz[k][i] = float(c[:, cells].mean()) / p10.PIECE
        if i < n_pre:
            eln_pre += c[:, elns].mean(0)
        t += p10.PIECE
    return {"u": u, "hz": hz, "eln_pre_hz": eln_pre / (PRE_S - 0.1)}


def _times(x: np.ndarray) -> np.ndarray:
    return -PRE_S + p10.PIECE * (np.arange(len(x)) + 0.5)


def _less_base(x: np.ndarray) -> np.ndarray:
    t = _times(x)
    return x - x[(t >= -PRE_S) & (t < -0.1)].mean()


def window(x: np.ndarray, lo: float, hi: float) -> float:
    """Mean over model times [lo, hi) from the odor onset, less the baseline (-0.5 to -0.1 s)."""
    t = _times(x)
    return float(_less_base(x)[(t >= lo) & (t < hi)].mean())


def peak(x: np.ndarray) -> tuple:
    """The 50 ms running mean's peak over the odor (less baseline) and its time after the valve (ms)."""
    t = _times(x)
    sm = np.convolve(_less_base(x), np.ones(5) / 5, mode="same")
    inside = np.flatnonzero((t >= 0) & (t < ODOR_S))
    k = int(inside[np.argmax(sm[inside])])
    return float(sm[k]), int(round((t[k] + VALVE_S) * 1000))


def at(x: np.ndarray, when: float) -> float:
    """The 50 ms running mean (less baseline) at model time `when`."""
    sm = np.convolve(_less_base(x), np.ones(5) / 5, mode="same")
    return float(sm[int(np.argmin(np.abs(_times(x) - when)))])


def run_condition(o, rec, silent, stimuli, base: int, sets: dict, elns: np.ndarray) -> dict:
    """{stimulus: mean trial over SEEDS} with `silent` glomeruli's receptor neurons silenced, settled without them;
    stimuli() gives {name: drive_at} once they're silenced."""
    out = {}
    with silenced(rec, silent), warm.settled(o, rec):
        for j, (name, drive_at) in enumerate(stimuli().items()):
            rs = [trial(o, rec, drive_at, base + 10 * j + s, sets, elns) for s in range(SEEDS)]
            out[name] = {"u": {k: np.mean([r["u"][k] for r in rs], 0) for k in sets},
                         "hz": {k: np.mean([r["hz"][k] for r in rs], 0) for k in sets},
                         "eln_pre_hz": np.mean([r["eln_pre_hz"] for r in rs], 0)}
    return out


def odor_stimuli(rec, odors_: tuple, blank: bool = True) -> dict:
    out = {}
    for od in ((None,) if blank else ()) + tuple(dict.fromkeys(odors_)):
        plan = rec.plan(od, ODOR_S, p10.PEAK_HZ)
        out["none" if od is None else od] = (lambda p: (lambda t: rec.at(p, t)))(plan)
    return out


def r2(x) -> float:
    return round(float(x), 2)


def interpolate(xs, ys, target: float, log: bool) -> float | None:
    """x where y crosses target, linearly between neighbouring conditions (in log x if log)."""
    xs = np.log(xs) if log else np.asarray(xs, float)
    for a in range(len(xs) - 1):
        if (ys[a] - target) * (ys[a + 1] - target) <= 0 and ys[a + 1] != ys[a]:
            x = xs[a] + (target - ys[a]) * (xs[a + 1] - xs[a]) / (ys[a + 1] - ys[a])
            return float(np.exp(x) if log else x)
    return None


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    b = o.brain
    assert len(b.gap_mv) == 0
    nt = np.asarray(consensus_transmitters())
    gloms = [g for g in rec.glomeruli if len(rec.cells[g])]
    pn_of = {g: np.flatnonzero(o.m["upn"] & (nt == "acetylcholine") & np.char.startswith(o.types, f"{g}_")) for g in gloms}
    pn_of = {g: v for g, v in pn_of.items() if len(v)}
    antennal = [g for g in pn_of if g not in PALP]
    ln, pn = pairs(o)
    elns = np.unique(ln)
    gaba_lns = np.flatnonzero(np.array([bool(p14.LN.match(t)) for t in o.types]) & (nt == "gaba"))
    sets = dict(pn_of)
    sets.update({"antennal": np.concatenate([pn_of[g] for g in antennal]),
                 "VC1/VC2": np.concatenate([pn_of[g] for g in ("VC1", "VC2")]), "eLN": elns, "GABA LN": gaba_lns})
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e_orn = o.m["orn"][pre] & np.isin(b.idx, elns)
    w0, bias0 = b.weights.copy(), o.own_bias()
    upn = np.flatnonzero(o.m["upn"] & (nt == "acetylcholine"))
    ant_orn = o.m["orn"] & ~np.isin(o.types, [f"ORN_{g}" for g in PALP])
    summed = lambda cells, w: np.bincount(b.idx[ant_orn[pre]], weights=w[ant_orn[pre]], minlength=b.n)[cells]
    per_pn = np.bincount(pn, minlength=b.n)[np.flatnonzero(o.m["upn"])]
    out = {"question": __doc__, "flies": FLIES, "eln_target_hz": round(ELN_TARGET, 3), "t13_target_mv": round(T13_TARGET, 3),
           "coupling": {"pairs": int(len(ln)), "elns": int(len(elns)), "pns": int(len(np.unique(pn))),
                        "elns_per_upn": {"median": float(np.median(per_pn)), "min": int(per_pn.min()), "max": int(per_pn.max())},
                        "contacts_per_glomerulus": {g: r2(np.bincount(pn, minlength=b.n)[pn_of[g]].mean()) for g in pn_of}},
           "receptor_synapses": {"onto_elns": int(e_orn.sum()), "per_synapse_mv": round(float(w0[e_orn].sum() / b._counts[e_orn].sum()), 4),
                                 "summed_antennal_eln_over_pn": round(float(np.median(summed(elns, w0)) / np.median(summed(upn, w0))), 4)},
           "glomeruli": {"antennal": antennal, "palp": [g for g in pn_of if g in PALP]}, "gain": {}, "coupled": {}}

    def set_gain(g: float) -> np.ndarray:
        w = w0.copy()
        w[e_orn] *= g
        b.weights, b._external_matrix = w.astype(np.float32), None
        return gain_offset(o, rec, e_orn, w0, g)

    # Stage 1: the eLNs' gain
    for i, g in enumerate(GAINS):
        off = set_gain(g)
        b.set_bias(bias0 - off)
        base = SEED + 1000 * i
        intact = run_condition(o, rec, (), lambda: odor_stimuli(rec, T5_ODORS), base, sets, elns)
        no_ant = run_condition(o, rec, antennal, lambda: odor_stimuli(rec, PALP_ODORS), base + 500, sets, elns)
        rise = {od: r2(no_ant[od]["hz"]["eLN"][50:100].mean() - no_ant["none"]["hz"]["eLN"][50:100].mean()) for od in PALP_ODORS}
        row = {"bias_lowered_mv": {"eln_mean": r2(off[elns].mean())},
               "summed_antennal_eln_over_pn": round(float(np.median(summed(elns, b.weights)) / np.median(summed(upn, w0))), 3),
               "rest_hz": {k: r2(intact["none"]["hz"][k][:40].mean()) for k in ("eLN", "GABA LN", "antennal")},
               "eln_hz_antennae_removed": {od: r2(no_ant[od]["hz"]["eLN"][50:100].mean()) for od in PALP_ODORS + ("none",)},
               "eln_rise_antennae_removed": rise, "eln_mean_rise": r2(np.mean(list(rise.values()))),
               "intact": {od: {"eln_hz": r2(intact[od]["hz"]["eLN"][50:100].mean()),
                               "eln_depolarization_peak_mv": r2(peak(intact[od]["u"]["eLN"])[0]),
                               "gaba_ln_hz": r2(intact[od]["hz"]["GABA LN"][50:100].mean()),
                               "antennal_pn_hz": r2(intact[od]["hz"]["antennal"][50:100].mean())} for od in ("none",) + T5_ODORS},
               "traces": {"antennae removed": {od: no_ant[od]["hz"]["eLN"].round(2).tolist() for od in no_ant},
                          "intact": {od: intact[od]["hz"]["eLN"].round(2).tolist() for od in intact}}}
        out["gain"][f"g {g:g}"] = row
        print(f"g {g:g}:", json.dumps({k: row[k] for k in ("rest_hz", "eln_hz_antennae_removed", "eln_mean_rise",
                                                          "summed_antennal_eln_over_pn")}),
              "intact", json.dumps(row["intact"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    rises = [out["gain"][f"g {g:g}"]["eln_mean_rise"] for g in GAINS]
    g_fit = interpolate(GAINS, rises, ELN_TARGET, log=True)
    out["chosen_gain"] = None if g_fit is None else round(g_fit, 2)
    print("eLN rises", json.dumps(dict(zip([f"{g:g}" for g in GAINS], rises))), "target", round(ELN_TARGET, 2),
          "chosen g", out["chosen_gain"], flush=True)
    OUT.write_text(json.dumps(out, indent=1))
    rest1 = out["gain"]["g 1"]["rest_hz"]["eLN"]
    upper = next((g for g in GAINS if g >= (g_fit or np.inf)), None)
    if g_fit is None or out["gain"][f"g {upper:g}"]["rest_hz"]["eLN"] > 2 * rest1:
        out["seconds"] = round(time.perf_counter() - t0)
        out["stopped"] = "no gain reaches flies' eLN rise" if g_fit is None else "the gain that does runs the eLNs away at rest"
        OUT.write_text(json.dumps(out, indent=1))
        print(f"{out['stopped']}; stopped ({out['seconds']} s)", flush=True)
        return

    # Stage 2: the coupling, at the chosen gain
    gain_off = set_gain(g_fit)
    eln_rest = None
    for i, kick in enumerate(KICKS_MV):
        row = {}
        couple_off = couple(o, ln, pn, kick, eln_rest) if kick else np.zeros(b.n)
        b.set_bias(bias0 - gain_off - couple_off)
        row["bias_lowered_mv"] = {"upn_mean": r2(couple_off[upn].mean()), "upn_max": r2(couple_off[upn].max())}
        base = SEED + 10000 * (i + 1)
        intact = run_condition(o, rec, (), lambda: odor_stimuli(rec, T7_ODORS, blank=False), base, sets, elns)
        if eln_rest is None:                                       # each eLN's resting rate, uncoupled
            eln_rest = np.zeros(b.n)
            eln_rest[elns] = np.mean([v["eln_pre_hz"] for v in intact.values()], 0)
        row["rest_hz"] = {k: r2(np.mean([v["hz"][k][:40].mean() for v in intact.values()])) for k in ("antennal", "eLN", "GABA LN")}
        no_ant = run_condition(o, rec, antennal, lambda: odor_stimuli(rec, PALP_ODORS + T1_ODORS + T5_ODORS), base + 1000, sets, elns)
        no_palp = run_condition(o, rec, PALP, lambda: odor_stimuli(rec, PALP_ODORS + T5_ODORS), base + 2000, sets, elns)
        mutants = run_condition(o, rec, ("VM2", "DL1"), lambda: odor_stimuli(rec, T7_ODORS, blank=False), base + 3000, sets, elns)
        va7l = {f"{r:g}": (lambda r: (lambda t: [(rec.cells["VA7l"], rec.spont["VA7l"] + (r if 0 <= t + p10.PIECE / 2 < ODOR_S else 0.0))]))(r)
                for r in (0.0,) + T2_RATES}
        only = run_condition(o, rec, [g for g in gloms if g != "VA7l"], lambda: va7l, base + 4000, sets, elns)

        dep = lambda d, k: window(d["u"][k], 0.0, 0.5)
        t13 = {"VM2, antennae removed": {od: r2(dep(no_ant[od], "VM2")) for od in PALP_ODORS + ("none",)},
               "antennal PNs, antennae removed": {od: r2(dep(no_ant[od], "antennal")) for od in PALP_ODORS + ("none",)},
               "VM7d, palps removed": {od: r2(dep(no_palp[od], "VM7d")) for od in PALP_ODORS + ("none",)}}
        t13_mean = float(np.mean([v for r in t13.values() for od, v in r.items() if od != "none"]))
        elnr = {"eln_hz_antennae_removed": {od: r2(no_ant[od]["hz"]["eLN"][50:100].mean()) for od in PALP_ODORS + ("none",)}}
        t1 = {"peak": {}, "peak_ms_after_valve": {}, "at_500ms": {}}
        for od in T1_ODORS:
            pk, ms = peak(no_ant[od]["u"]["antennal"])
            t1["peak"][od], t1["peak_ms_after_valve"][od] = r2(pk), ms
            t1["at_500ms"][od] = r2(at(no_ant[od]["u"]["antennal"], 0.5 - VALVE_S))
        t5 = {"VC1/VC2, palps removed": {od: r2(window(no_palp[od]["u"]["VC1/VC2"], 0.0, 0.2)) for od in T5_ODORS},
              "DM1, antennae removed": {od: r2(window(no_ant[od]["u"]["DM1"], 0.0, 0.2)) for od in T5_ODORS}}
        rate = lambda d, k: window(d["hz"][k], -VALVE_S, ODOR_S - VALVE_S)
        t7 = {}
        for gl in ("VM2", "DL1"):
            silent_ = {od: r2(rate(mutants[od], gl)) for od in T7_ODORS}
            working = {od: r2(rate(intact[od], gl)) for od in T7_ODORS}
            t7[f"{gl} silent"] = {"mean": r2(np.mean(list(silent_.values()))), "min": min(silent_.values()),
                                  "max": max(silent_.values()), "positive": int(sum(v > 0 for v in silent_.values())),
                                  "odors": silent_}
            t7[f"{gl} working"] = {"mean": r2(np.mean(list(working.values()))), "odors": working}
            sv, wv = np.array(list(silent_.values())), np.array(list(working.values()))
            t7[f"{gl} silent vs working r2"] = r2(np.corrcoef(sv, wv)[0, 1] ** 2) if sv.std() > 0 and wv.std() > 0 else None
        area = lambda d, k: 0.5 * window(d["u"][k], 0.0, 0.5)
        t2 = {"area_mv_s": {f"{r:g}": r2(area(only[f"{r:g}"], "antennal")) for r in (0.0,) + T2_RATES},
              "eln_hz": {f"{r:g}": r2(only[f"{r:g}"]["hz"]["eLN"][50:100].mean()) for r in (0.0,) + T2_RATES}}
        fig8 = FLIES["T2"]["fig8c_mv_s"]
        t2["fig8c_mv_s"] = {gl: r2(area(only["147"], gl)) for gl in fig8 if gl in pn_of}
        x, y = [t2["fig8c_mv_s"][gl] for gl in t2["fig8c_mv_s"]], [fig8[gl] for gl in t2["fig8c_mv_s"]]
        t2["fig8c_spearman"] = r2(spearmanr(x, y).correlation) if np.std(x) > 0 else None
        t2["DM1_147"] = r2(area(only["147"], "DM1"))
        row.update({"T13": t13, "T13_mean_mv": round(t13_mean, 3), "eLN": elnr, "T1": t1, "T5": t5, "T7": t7, "T2": t2,
                    "traces": {"antennae removed": {od: {"antennal_u": no_ant[od]["u"]["antennal"].round(3).tolist(),
                                                         "VM2_u": no_ant[od]["u"]["VM2"].round(3).tolist(),
                                                         "eln_hz": no_ant[od]["hz"]["eLN"].round(2).tolist()} for od in no_ant},
                               "palps removed": {od: {"VC1/VC2_u": no_palp[od]["u"]["VC1/VC2"].round(3).tolist(),
                                                      "VM7d_u": no_palp[od]["u"]["VM7d"].round(3).tolist()} for od in no_palp},
                               "VA7l only": {r: {"antennal_u": only[r]["u"]["antennal"].round(3).tolist(),
                                                 "eln_hz": only[r]["hz"]["eLN"].round(2).tolist()} for r in only},
                               "mutants": {od: {gl: mutants[od]["hz"][gl].round(1).tolist() for gl in ("VM2", "DL1")} for od in mutants}}})
        out["coupled"][f"k {kick:g}"] = row
        print(f"k {kick:g}:", json.dumps({"rest": row["rest_hz"], "T13_mean": row["T13_mean_mv"], "T13": t13, "eLN": elnr}), flush=True)
        print("   T1", json.dumps(t1), "T5", json.dumps(t5), flush=True)
        print("   T7", json.dumps({k: (v if not isinstance(v, dict) else {x: v[x] for x in ("mean", "min", "max", "positive") if x in v})
                                   for k, v in t7.items()}), flush=True)
        print("   T2", json.dumps(t2), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    ms = [out["coupled"][f"k {k:g}"]["T13_mean_mv"] for k in KICKS_MV]
    k_fit = interpolate(KICKS_MV, ms, T13_TARGET, log=False)
    out["chosen_kick_mv"] = None if k_fit is None else round(k_fit, 3)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("T13 means", json.dumps(dict(zip([f"{k:g}" for k in KICKS_MV], ms))), "target", round(T13_TARGET, 2),
          "chosen k", out["chosen_kick_mv"], f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
