"""Exploratory, not pre-registered: why does MBON11 turn its Kenyon cell input into fewer spikes than flies' MBON11?

odor_probe31.py: with the Kenyon cell-to-MBON11 synapses set from Yamada et al. 2024's charge and Wang et al. 2026's gain,
MBON11 makes 0.11-0.27 spikes per pC of its Kenyon cell input, where flies' make about 0.45 (Hige et al. 2015: 118
spikes from about 250 pC), as Wang et al.'s gain predicts (0.41), and its response grows only about as the square root
of the charge per synapse. The model's synapses were set so that, through MBON11's own gain near rest (3.7 spikes/s per
mV), each pC brings 0.41 spikes; so either MBON11's rate stops following its drive at the rates odors reach, or the
drive comes in too short a burst, or other inputs cancel part of it. Flies' MBON11 (Hige et al. 2015, Fig. 1E and 3C,
read off the figures; research_notes/Rung 9 learning data/mbon11_input.md) fires from about 0.15 s after the valve
opens, peaks at 135-140 Hz at about 0.3 s and holds 95-100 Hz from 0.6 to 1.05 s over a held baseline of about 6 Hz; its
odor EPSC peaks at about 380-430 pA and holds about 170 pA from 0.6 to 1.0 s.
Model: odor_probe30.py's brain (odor_probe31.build on its seeds; brain_cache.py keeps it) with the Kenyon cell-to-MBON11
synapses at odor_probe31.py's middle charge (q = 0.030 pC per synapse; the gain measured as odor_probe31.py measures it).
Measured:
  1. MBON11's F-I curve: its rate over 1 s of rest with its bias moved by -12 to +64 mV (spontaneous receptor firing
     on);
  2. for 3-octanol and 4-methylcyclohexanol (4 seeds, 8 flies each), in 50 ms bins from 0.5 s before the odor to 1.5 s
     after its onset: MBON11's rate; its Kenyon cell input as a current per cell (pC per bin through q); and the drive,
     in mV, from its Kenyon cells, its other excitatory inputs and its inhibitory inputs (spiking and graded), each spike
     counting w x 5 ms (the synaptic current's decay) and each Hz of graded release like a spike per second; with the
     rate the linear gain predicts from the drive above rest;
  3. the same Kenyon cell charge delivered evenly: MBON11's bias raised for 1.4 s, without an odor, by the mean drive
     its Kenyon cells give it over the odor's 1.4 s window above rest, and the spikes it adds;
  4. the two odors with MBON11's other inputs cut: its evoked spikes as Hige et al. counted them;
  5. the two odors with MBON11 held, as Hige et al. held their cells (at about -60 mV by < 50 pA, which left it firing
     about 6 Hz before the odors; the model's MBON11 rests at 34 Hz, as flies' imaged without an electrode, 37 Hz): its
     bias lowered by the step at which the F-I curve crosses 6 Hz (interpolated), and its evoked spikes.
Seeds 270000 (+ 10 x step for the F-I curve, + 100 + 10 x odor + seed for the odors, + 200 + ... with the other inputs
cut and intact, + 300 + ... for the even drive, + 400 + ... held).

Ran: MBON11's other inputs don't matter; its Kenyon cell input comes too large for 3-octanol, too small for
4-methylcyclohexanol, and in a form it turns into spikes inefficiently. Its F-I curve (rest 34 Hz): 0 spikes/s at -12
mV, 11 at -6, 34 at 0, 87 at +16, 127 at +32 and 186 at +64 mV, 3.7 spikes/s per mV near rest falling to about 1.6 at
150-190 Hz. To 3-octanol its Kenyon cell input carries 545 pC per cell (on average 43 mV of drive above rest over 0-1.4
s; flies about 250 pC), as a current that peaks at 845 pA at 0.3-0.35 s and falls to 311 pA by 1 s (flies' EPSC: about
400 pA at its peak, soon after its onset 0.18 s after the valve opens, then 170-200 pA); MBON11 rises from 35 to 132
spikes/s at 0.4-0.45 s and falls to 87 by 1 s (flies: 135-140 at about 0.3 s after the valve opens and 95-100 at
0.6-1.05 s, from a held 6 Hz): 72 spikes evoked. The same mean drive given evenly as a step of its bias adds 163 spikes,
as the F-I curve predicts, and its gain near rest would give 224 (0.41 x 545). To 4-methylcyclohexanol its input carries
128 pC (10 mV; flies about 265), peaking at 172 pA with no onset peak; MBON11 peaks at 70 spikes/s and holds 55-65: 27
spikes, against 50 for the even drive (near the gain's 52). Cutting MBON11's other inputs changes nothing (3-octanol 75
spikes against 76 intact, 4-methylcyclohexanol 29 against 29; its inhibitory inputs bring -1.3 mV during 3-octanol). So
about half of the Kenyon cell input is lost in its fine timing, the even drive giving twice the spikes (coincident
volleys or each cell's burst of 4-6 spikes arriving faster than MBON11 can follow; not separated here), and at
3-octanol's size the F-I curve's bend costs another quarter. Held at 6.4 Hz, as Hige et al. held their cells (its bias
7.25 mV lower), MBON11 gains 91 spikes to 3-octanol and 36 to 4-methylcyclohexanol (76 and 29 at rest; flies 118 and
110): in Hige et al.'s condition 3-octanol's response comes within a quarter of flies' and 4-methylcyclohexanol's stays
at a third.

    python experiments/odor_probe32.py         (writes experiments/odor_probe32.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import brain_cache
import odor_probe10 as p10
import odor_probe21 as p21
import odor_probe24 as p24
import odor_probe31 as p31

OUT = Path(__file__).with_suffix(".json")
SEED = 270000
CHARGE_PC = 0.030
STEPS_MV = (-12.0, -8.0, -6.0, -4.0, -2.0, 0.0, 4.0, 8.0, 16.0, 24.0, 32.0, 48.0, 64.0)
HELD_HZ = 6.0                                      # Hige et al. 2015's pre-odor rate, cells held at about -60 mV
ODORS = ("3-octanol", "4-methylcyclohexanol")
SEEDS = 4
BIN, PRE, POST = 0.05, 0.5, 1.5
FLIES = {"psth_hz": {"baseline": 6, "rise_s": 0.15, "peak": "135-140 at 0.30 s", "0.6-1.05 s": "95-100", "end_s": 1.45},
         "epsc_pa": {"onset_s": 0.18, "peak": "380-430", "at_0.35_s": 200, "0.6-1.0 s": 170, "end_s": 1.5},
         "spikes": {"3-octanol": 118, "4-methylcyclohexanol": 110}, "charge_pc": {"3-octanol": "245-250", "4-methylcyclohexanol": 265}}


def inputs(o, mb: np.ndarray) -> dict:
    """Sparse maps (neurons x MBON11 cells) of each input group's weights, and the Kenyon cells' synapse counts."""
    b = o.brain
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = np.flatnonzero(np.isin(b.idx, mb))
    col = np.searchsorted(mb, b.idx[e])
    is_kc, w = o.m["kc"][pre[e]], b.weights[e].astype(np.float64)
    graded = np.isin(pre[e], b.graded)

    def mat(keep, values):
        return sparse.csr_matrix((values[keep], (pre[e][keep], col[keep])), shape=(b.n, len(mb)))
    gi = np.searchsorted(b.graded, pre[e])
    return {"kc_w": mat(is_kc, w), "kc_syn": mat(is_kc, b._counts[e].astype(np.float64)),
            "exc_w": mat(~is_kc & ~graded & (w > 0), w), "inh_w": mat(~is_kc & ~graded & (w < 0), w),
            "graded_w": sparse.csr_matrix((w[graded], (gi[graded], col[graded])), shape=(len(b.graded), len(mb))),
            "other_edges": e[~is_kc]}


def course(o, rec, odor: str, seed: int, mb: np.ndarray, maps: dict) -> dict:
    """Per 50 ms bin, mean over flies and MBON11's two cells: its rate (Hz), its Kenyon cell current (pA) and each
    input group's drive (mV)."""
    b = o.brain
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    plan = rec.plan(odor, 1.0, p10.PEAK_HZ)
    piece, per = int(round(p10.PIECE / b.dt)), int(round(BIN / p10.PIECE))
    rows = {k: [] for k in ("rate_hz", "kc_pa", "kc_mv", "exc_mv", "inh_mv", "graded_mv")}
    t = -PRE
    for _ in range(int(round((PRE + POST) / BIN))):
        c, g = 0, 0
        for _ in range(per):
            c = c + b.advance(piece, drive=rec.at(plan, t))
            g = g + b.release * p10.PIECE                        # graded release, Hz x s: spikes' worth
            t += p10.PIECE
        rows["rate_hz"].append(float(c[:, mb].mean() / BIN))
        rows["kc_pa"].append(float((c @ maps["kc_syn"]).mean() * CHARGE_PC / BIN))
        for k in ("kc", "exc", "inh"):
            rows[f"{k}_mv"].append(float((c @ maps[f"{k}_w"]).mean() * p21.TAU / BIN))
        rows["graded_mv"].append(float((g @ maps["graded_w"]).mean() * p21.TAU / BIN) if len(b.graded) else 0.0)
    return rows


def evoked(o, rec, odor: str, seed: int, mb: np.ndarray, runner) -> float:
    h = runner(o, odor, seed, 1.0, 0.4)
    return float((h["window"] - 1.4 * h["rest"])[:, mb].mean())


def even_drive(o, rec, mb: np.ndarray, extra_mv: float, seed: int) -> float:
    """Spikes MBON11 adds over 1.4 s with its bias raised by extra_mv, against 1.4 s of its rest before."""
    b = o.brain
    base = o.own_bias()
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    rest = b.advance(int(round(1.0 / b.dt)), drive=p24.spontaneous(rec))
    bias = base.copy()
    bias[mb] += extra_mv
    b.set_bias(bias)
    try:
        on = b.advance(int(round(1.4 / b.dt)), drive=p24.spontaneous(rec))
    finally:
        b.set_bias(base)
    return float((on - 1.4 * rest)[:, mb].mean())


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.probe30()
    b, types = o.brain, o.types
    mb = np.flatnonzero(types == "MBON11")
    out = {"question": __doc__, "flies": FLIES}
    gain = p31.mbon_gain(o, rec, mb)
    w_syn = p31.GAIN_HZ_PER_PA * CHARGE_PC / (gain["slope_hz_per_mv"] * p21.TAU)
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    onto = np.flatnonzero(o.m["kc"][pre] & np.isin(b.idx, mb))
    w0 = b.weights.copy()
    w0[onto] = b._counts[onto] * w_syn
    b.weights, b._external_matrix = w0.copy(), None
    out["mbon11_gain"], out["weight_per_synapse_mv"] = gain, round(w_syn, 4)
    print("MBON11 gain", json.dumps(gain), "weight per synapse", round(w_syn, 4), flush=True)

    base = o.own_bias()
    fi = []
    for k, d in enumerate(STEPS_MV):
        bias = base.copy()
        bias[mb] += d
        b.set_bias(bias)
        fi.append(round(float(p10.resting(o, rec, SEED + 10 * k)["hz"][mb].mean()), 2))
    b.set_bias(base)
    out["fi"] = {"steps_mv": list(STEPS_MV), "rate_hz": fi}
    print("F-I", json.dumps(out["fi"]), flush=True)

    maps = inputs(o, mb)
    runner = p10.make_runner(rec)
    n_pre = int(round(PRE / BIN))
    out["odors"] = {}
    for j, odor in enumerate(ODORS):
        runs = [course(o, rec, odor, SEED + 100 + 10 * j + s, mb, maps) for s in range(SEEDS)]
        mean = {k: np.mean([r[k] for r in runs], 0) for k in runs[0]}
        rest = {k: float(v[:n_pre].mean()) for k, v in mean.items()}
        drive = sum(mean[f"{k}_mv"] for k in ("kc", "exc", "inh", "graded"))
        drive_rest = sum(rest[f"{k}_mv"] for k in ("kc", "exc", "inh", "graded"))
        predicted = rest["rate_hz"] + gain["slope_hz_per_mv"] * (drive - drive_rest)
        window = slice(n_pre, n_pre + int(round(1.4 / BIN)))
        kc_extra_mv = float((mean["kc_mv"][window] - rest["kc_mv"]).mean())
        charge = float(((mean["kc_pa"][window] - rest["kc_pa"]) * BIN).sum())
        row = {"bin_s": BIN, "start_s": -PRE, **{k: [round(float(x), 2) for x in v] for k, v in mean.items()},
               "predicted_rate_hz": [round(float(x), 1) for x in predicted], "rest": {k: round(v, 3) for k, v in rest.items()},
               "evoked_spikes_from_bins": round(float(((mean["rate_hz"][window] - rest["rate_hz"]) * BIN).sum()), 1),
               "kc_charge_pc_per_cell": round(charge, 1), "kc_mean_extra_drive_mv": round(kc_extra_mv, 2)}
        row["even_drive_spikes"] = round(float(np.mean([even_drive(o, rec, mb, kc_extra_mv, SEED + 300 + 10 * j + s)
                                                         for s in range(SEEDS)])), 1)
        out["odors"][odor] = row
        print(odor, json.dumps({k: row[k] for k in ("evoked_spikes_from_bins", "kc_charge_pc_per_cell",
                                                     "kc_mean_extra_drive_mv", "even_drive_spikes")}), flush=True)
        print("  rate", row["rate_hz"][8:32], flush=True)
        print("  predicted", row["predicted_rate_hz"][8:32], flush=True)
        OUT.write_text(json.dumps(out, indent=1))

    w = w0.copy()
    w[maps["other_edges"]] = 0.0
    b.weights, b._external_matrix = w, None
    out["other_inputs_cut"] = {odor: round(float(np.mean([evoked(o, rec, odor, SEED + 200 + 10 * j + s, mb, runner)
                                                           for s in range(SEEDS)])), 1) for j, odor in enumerate(ODORS)}
    b.weights, b._external_matrix = w0.copy(), None
    out["intact"] = {odor: round(float(np.mean([evoked(o, rec, odor, SEED + 200 + 10 * j + s, mb, runner)
                                                 for s in range(SEEDS)])), 1) for j, odor in enumerate(ODORS)}
    print("other inputs cut", json.dumps(out["other_inputs_cut"]), "intact", json.dumps(out["intact"]), flush=True)
    k = next((i for i, r in enumerate(fi) if r >= HELD_HZ), 0)                  # the first step at or above 6 Hz
    hold = STEPS_MV[k] if k == 0 else float(np.interp(HELD_HZ, fi[k - 1:k + 1], STEPS_MV[k - 1:k + 1]))
    bias = base.copy()
    bias[mb] += hold
    b.set_bias(bias)
    try:
        out["held"] = {"bias_step_mv": round(hold, 2), "rest_hz": round(float(p10.resting(o, rec, SEED + 490)["hz"][mb].mean()), 2),
                       **{odor: round(float(np.mean([evoked(o, rec, odor, SEED + 400 + 10 * j + s, mb, runner)
                                                     for s in range(SEEDS)])), 1) for j, odor in enumerate(ODORS)}}
    finally:
        b.set_bias(base)
    print("held", json.dumps(out["held"]), flush=True)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
