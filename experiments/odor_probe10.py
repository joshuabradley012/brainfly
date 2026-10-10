"""Exploratory, not pre-registered: receptor neurons that fire as flies' do, rising with measured latencies and time
courses, adapting, and firing spontaneously at rest. Are the Kenyon cells then as sparse as a fly's, and does MBON11
hear them better?

odor_probe7.py to odor_probe9.py: 11-30% of Kenyon cells respond to an odor (flies: 6 +- 5%), mostly with spikes at
the odor's onset, before any inhibition arrives, and APL's slow inhibition doesn't change that. The model switches every
receptor neuron of an odor on at the same instant and at a constant rate (DoOR response x 200 Hz), and keeps them silent
at rest. Kenyon cells detect coincident input, so the synchrony of their inputs' onset matters. Measured
(research_notes/Rung 9 learning data/orn_dynamics.md):
  - latency from the odor's arrival falls steeply with drive: 3-4.4 ms to the first spike at high concentration,
    18-55 ms at low (Egea-Weiss et al. 2018), so strongly driven glomeruli lead weakly driven ones by tens of ms.
  - rise: a single response rises about as fast as the odor arrives, which for volatile esters and ketones takes
    tau_on of about 25-40 ms (Martelli et al. 2013); transduction adds little (LFP 10-90% rise 28-32 ms, spike rate
    peaking before the LFP; Nagel & Wilson 2011). Odors with vapor pressure under 1 mmHg arrive more slowly (tau_on
    0.15-1.5 s in Martelli's rig). The average over many odor-glomerulus pairs, with their spread of latencies, reaches
    90% of its peak about 120 ms after it starts (Bhandawat et al. 2007, read off their figure).
  - adaptation: from the peak toward about half, with a time constant of about 0.4 s (Nagel & Wilson 2011; plateau
    0.43-0.5 in Martelli et al. 2013 and Lazar & Yeh 2020); at 500 ms about 0.75 of the peak (Bhandawat).
  - offset: firing stops abruptly, with a brief silence recovering over about 0.5 s (Nagel & Wilson 2011).
  - spontaneous firing: wild-type antennal basiconic ORNs 1-15 spikes/s (median 6, 16 types), palp 3-32 (median 8),
    coeloconic 16-42 (median 19), via DoOR's compilation; ORN spike trains are independent.
Model: odor_probe7.py's current model. Each glomerulus's receptor neurons fire at their class's median spontaneous
rate (by the sensillum DoOR maps the glomerulus's receptor to: ab 6, pb 8, ac 19 spikes/s, otherwise 6), plus during
an odor DoOR's response above spontaneous v (brainfly.odors; with spontaneous firing, negative v lowers the rate, to
no less than 0) times 200 Hz times a time course: nothing for a latency of 4 + 46 x (1 - v) ms (linear in v
between Egea-Weiss's strong and weak latencies: an assumption), then (1 - exp(-t / tau_r)) (0.5 + 0.5 exp(-t / 0.4 s)),
scaled to peak at 1, with tau_r 30 ms (a volatile odor's arrival) or, as a variant, 150 ms (a slow one's; 3-octanol's
and 4-methylcyclohexanol's vapor pressures are near 1 mmHg, and their arrival wasn't measured). At the odor's end (plus the
latency) a driven glomerulus (v > 0.05) falls silent and recovers to its spontaneous rate with a time constant of
0.25 s. Spontaneous input moves the antennal lobe's resting state, so with it every neuron's bias is first lowered by
its mean spontaneous receptor input (rate x the depression's mean strength left, 1 / (1 + rate x 0.9 s x 0.22) for the
receptor neurons' 0.78 and 0.9 s, x weight x 5 ms), then rung 4's rate calibration polishes every group but the Kenyon
cells and the ring (rung 4's schedule, 8 rounds of 1 mV and 4 of 0.5 mV, eyes_at_rest.py's rule, with the receptor
neurons firing spontaneously; uniglomerular PNs aim at rung 4's 3 Hz, flies 1-5), and the Kenyon cells' rest is set
again to 21.5 mV below threshold. With tau_r 30 ms the time course peaks 104 ms after its start and is at 0.78 of its
peak at 425 ms and 0.63 at 1 s (Bhandawat's average: peak about 150 ms, 0.75 at about 425 ms); with 150 ms it peaks
at 345 ms.
Conditions:
  current                           odor_probe7.py's current model (instant, constant receptor drive; silent at rest)
  kinetics                          the time course above, no spontaneous firing
  kinetics + spontaneous            the time course and spontaneous firing, the resting state recalibrated
  kinetics + spontaneous, APL off   the same with APL silenced throughout (flies: about four times as many Kenyon
                                    cells active without APL)
  slow kinetics + spontaneous       kinetics + spontaneous with tau_r 150 ms
Odors, flies and measures as odor_probe7.py; seeds 40000 + 100 x condition + odor (Turner's protocol), + 50 + odor
(Hige's), + 60 to 71 (the resting calibration's rounds), + 80 to 82 (Kenyon cells' rest after it), + 90 (Kenyon cells'
rest before it), + 95 (the resting brain).

Ran (after the second review: DoOR's spontaneous level subtracted, so it is no longer counted on top of the receptor
neurons' spontaneous firing, inhibitory responses lowering the rate, the ring's offsets added once, and rung 4's full
calibration schedule; an earlier run without these is in git history): realistic receptor dynamics barely change the
Kenyon cells, and spontaneous firing makes them sparse for the wrong reason, by taking the projection neurons out of
the flies' range. Over the six odors:
  current                           7.3-19.4% of Kenyon cells respond (MCH 7.3%, OCT 17.1%); PNs 166-180 Hz in the
                                    first 100 ms, 86-98 over the second; MBON11 0.8-5.8 spikes
  kinetics                          6.5-18.6%: barely sparser; PNs 113-129 and 83-93 Hz; MBON11 2.5-5.0
  kinetics + spontaneous            1.6-5.0% (MCH 1.6%, OCT 4.0%), within the flies' 6 +- 5%, but each responding cell
                                    fires under 1.5 spikes (alpha/beta 0.8-1.4, alpha'/beta' 0.6-0.8; flies 2.2 and
                                    4.9), PNs fire only 65-80 Hz in the first 100 ms and 29-36 over the second (flies:
                                    100-200 at onset), APL barely releases (0.1-1.5 Hz in the first 100 ms), and MBON11
                                    gains -0.2 to 1.4 spikes
  kinetics + spontaneous, APL off   1.2-4.2%: without APL no more Kenyon cells respond (0.8-1.0 times), since APL isn't
                                    recruited (flies: about four times as many active without it)
  slow kinetics + spontaneous       0.9-2.4%; PNs 44-58 Hz in the first 100 ms
With spontaneous firing the receptor neurons fire 8.4-8.5 Hz at rest and give each uniglomerular PN 26 mV of mean
input (up to 74 mV in some neuron; 766 neurons get over 1 mV). After the offset and 12 rounds of calibration the PNs
rest at 5.2-5.7 Hz, above rung 4's 3 Hz target and at the top of flies' 1-5 (99.4% of groups within a factor of 2 of
their targets; the brain at 1.09-1.12 Hz against 0.96, no neuron over 100 Hz), and the Kenyon cells sit 21.0-21.8 mV
below threshold. The PNs' weak odor responses follow from the receptor synapses' depression (0.78 left per spike,
0.9 s to recover, fitted to nerve trains by Nagel et al. 2015): spontaneous firing already holds them at about half
strength at 6 Hz (a fifth at 19 Hz), and however fast an odor drives them they pass on at most about 5 full-strength
spikes a second per receptor neuron (1 / (0.9 s x 0.22)). The notes flag that this fit over-depresses single fibres at low rates (Kazama & Wilson 2008 saw
about 0.6 of full strength at 7 Hz where it predicts 0.44); the model has fewer receptor neurons per glomerulus than
flies (about 50 per type for both antennae against about 40 per antenna), which leaves each PN less input to spare.

    python experiments/odor_probe10.py         (writes experiments/odor_probe10.json)
"""
from __future__ import annotations

import csv
import functools
import json
import time
from pathlib import Path

import numpy as np

import odor_probe3 as p3
import odor_probe7 as p7
import rest_calibration as attempt1
from brainfly import odors
from brainfly.data import DATA
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
PEAK_HZ, PLATEAU, TAU_ADAPT, OFF_TAU = 200.0, 0.5, 0.4, 0.25
TAU_RISE = {"fast": 0.03, "slow": 0.15}
LATENCY = (0.004, 0.046)                  # s: 4 ms at v = 1, plus 46 ms x (1 - v)
SPONT = {"ab": 6.0, "pb": 8.0, "ac": 19.0}
SPONT_DEFAULT = 6.0
PIECE = 0.01
POLISH = [1.0] * 8 + [0.5] * 4            # rung 4's schedule (eyes_at_rest.ROUNDS)
CONDITIONS = {"current": {}, "kinetics": {"kinetics": "fast"},
              "kinetics + spontaneous": {"kinetics": "fast", "spont": True},
              "kinetics + spontaneous, APL off": {"kinetics": "fast", "spont": True, "silence_apl": True},
              "slow kinetics + spontaneous": {"kinetics": "slow", "spont": True}}


@functools.lru_cache(maxsize=None)
def _peak(tau_r: float) -> float:
    """The unnormalized time course's peak (computed once per tau_r; the receptor drive asks for it every 10 ms)."""
    grid = np.arange(0, 2.0, 1e-4)
    return ((1 - np.exp(-grid / tau_r)) * (PLATEAU + (1 - PLATEAU) * np.exp(-grid / TAU_ADAPT))).max()


def course(t, tau_r: float) -> np.ndarray:
    """The time course from the response's start, peaking at 1 (0 before the start)."""
    t = np.asarray(t, float)
    peak = _peak(tau_r)
    c = np.clip(t, 0, None)
    k = (1 - np.exp(-c / tau_r)) * (PLATEAU + (1 - PLATEAU) * np.exp(-c / TAU_ADAPT))
    return np.where(t >= 0, k / peak, 0.0)


def sensillum_class() -> dict:
    """Glomerulus -> sensillum class (ab, pb, ac, at, ...) from DoOR's mapping."""
    rows = list(csv.reader(open(DATA / "door" / "door_mappings.csv"), delimiter=";"))[1:]
    out = {}
    for r in rows:
        sens, g = r[2], r[4]
        if not sens or g in ("?", "") or "+" in sens:
            continue
        for part in g.split("+"):
            names = [part]
            if "/" in part:
                head, tail = part.split("/")
                names = [head, head[:-len(tail)] + tail]
            for name in names:
                out.setdefault(name, sens[:2])
    return out


class Receptors:
    """The receptor neurons' drive, piece by piece: spontaneous firing and odors with their time course."""

    def __init__(self, o: p7.Olfaction):
        b = o.brain
        types = o.types
        orn = np.flatnonzero(o.m["orn"])
        self.glomeruli = sorted({t[4:] for t in types[orn]})
        self.cells = {g: b.cells([f"ORN_{g}"]) for g in self.glomeruli}
        cls = sensillum_class()
        self.spont = {g: SPONT.get(cls.get(g, ""), SPONT_DEFAULT) for g in self.glomeruli}
        self.kinetics, self.spontaneous = False, False

    def plan(self, odor: str | None, seconds: float, peak: float):
        v = odors.glomeruli(odor, inhibition=self.spontaneous) if odor else {}      # inhibition needs a rate to lower
        rows = []
        for g in self.glomeruli:
            r = v.get(g, 0.0)
            rows.append((g, r, LATENCY[0] + LATENCY[1] * (1 - min(abs(r), 1.0))))
        return {"rows": rows, "seconds": seconds, "peak": peak}

    def at(self, plan: dict, t: float) -> list:
        """(cells, Hz) for the piece starting t s after the odor's onset (negative before it)."""
        mid = t + PIECE / 2
        out = []
        for g, v, lat in plan["rows"]:
            spont = self.spont[g] if self.spontaneous else 0.0
            if mid < 0 or v == 0:
                hz = spont
            elif not self.kinetics:
                hz = max(spont + (v * plan["peak"] if mid < plan["seconds"] else 0.0), 0.0)
            elif mid < plan["seconds"] + lat:
                hz = max(spont + v * plan["peak"] * float(course(mid - lat, TAU_RISE[self.kinetics])), 0.0)
            else:
                after = mid - plan["seconds"] - lat
                hz = spont * (1 - np.exp(-after / OFF_TAU)) if v > 0.05 else spont
            if hz > 0:
                out.append((self.cells[g], hz))
        return out


def make_runner(rec: Receptors):
    """A trial runner for odor_probe7.measure_odor with this drive (odor_probe7.run's protocol and outputs)."""
    def runner(o, odor, seed, seconds, after, silence=(), max_hz=PEAK_HZ):
        b = o.brain
        kc = np.flatnonzero(o.m["kc"])
        apl = np.searchsorted(b.graded, b.cells(["APL"]))
        plan = rec.plan(odor, seconds, max_hz)
        b.reset(seed)
        b.set_release(o.s.ol.neurons, o.s.silent)
        piece = int(round(PIECE / b.dt))
        t = -2.0
        for _ in range(100):                                       # 1 s to settle
            b.advance(piece, drive=rec.at(plan, t), silence=silence)
            t += PIECE
        rest_bins, cur = [], None
        for k in range(100):                                       # 1 s of rest, in 200 ms bins
            c = b.advance(piece, drive=rec.at(plan, t), silence=silence)
            t += PIECE
            cur = c if cur is None else cur + c
            if (k + 1) % 20 == 0:
                rest_bins.append(cur)
                cur = None
        rest = sum(rest_bins)
        n_odor, n_all = int(round(seconds / PIECE)), int(round((seconds + after) / PIECE))
        total, first, during, bins, cur, release = np.zeros_like(rest), None, None, [], np.zeros_like(rest[:, kc]), []
        t = 0.0
        for k in range(n_all):
            c = b.advance(piece, drive=rec.at(plan, t), silence=silence)
            t += PIECE
            total += c
            cur += c[:, kc]
            if k < n_odor:
                release.append(float(b.release[:, apl].mean()))
            if k == 9:
                first = total.copy()
            if k == n_odor - 1:
                during = total.copy()
            if (k + 1) % 20 == 0:
                bins.append(cur.copy())
                cur[:] = 0
        return {"rest": rest, "rest_bins": np.stack([r[:, kc] for r in rest_bins], 1), "first": first, "odor": during,
                "window": total, "bins": np.stack(bins, 1),
                "apl": [round(float(np.mean(release[:10])), 1), round(float(np.mean(release)), 1)]}
    return runner


def resting(o: p7.Olfaction, rec: Receptors, seed: int, silence=(), sample: bool = False) -> dict:
    """1 s to settle and 1 s of rest with the receptor neurons at their spontaneous rates (if on): rates per neuron
    (Hz, mean over flies) and, if sample, each neuron's mean membrane potential."""
    b = o.brain
    plan = rec.plan(None, 0.0, 0.0)
    b.reset(seed)
    b.set_release(o.s.ol.neurons, o.s.silent)
    piece = int(round(PIECE / b.dt))
    for _ in range(100):
        b.advance(piece, drive=rec.at(plan, -1.0), silence=silence)
    counts, u = 0, np.zeros(b.n)
    for _ in range(100):
        counts = counts + b.advance(piece, drive=rec.at(plan, -1.0), silence=silence)
        if sample:
            u += b.u.mean(0) / 100
    return {"hz": counts.mean(0), "u": u}


def recalibrate_rest(o: p7.Olfaction, rec: Receptors, seed: int) -> dict:
    """With spontaneous receptor firing: lower each neuron's bias by its mean spontaneous receptor input, polish the
    groups' rates toward rung 4's targets (Kenyon cells and the ring held), then set the Kenyon cells' rest."""
    b, s, m = o.brain, o.s, o.m
    f, rec_s = (b.params[b.cls[np.flatnonzero(m["orn"])[0]]][k] for k in ("depression", "recovery"))
    rate = np.zeros(b.n)
    for g, cells in rec.cells.items():
        rate[cells] = rec.spont[g]
    left = 1.0 / (1.0 + rate * rec_s * (1 - f))
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    e = m["orn"][pre]
    mean_input = np.bincount(b.idx[e], weights=rate[pre[e]] * left[pre[e]] * b.weights[e] * TAU, minlength=b.n)
    bias = o.own_bias() - mean_input                     # set_bias adds the ring's offsets back
    b.set_bias(bias)
    held = s.fixed | m["kc"]
    gid = s.gid
    G = gid.max() + 1
    free_n = np.bincount(gid, weights=~held, minlength=G)
    goal = np.bincount(gid, weights=s.target * ~held, minlength=G) / np.maximum(free_n, 1)
    log = {"mean_input_mv": {"uPN": round(float(mean_input[m["upn"]].mean()), 2), "max": round(float(mean_input.max()), 2),
                             "neurons_over_1mv": int((mean_input > 1).sum())}, "polish": []}
    for r, k in enumerate(POLISH):
        hz = resting(o, rec, seed + r)["hz"]
        got = np.bincount(gid, weights=hz * ~held, minlength=G) / np.maximum(free_n, 1)
        step = np.where(free_n > 0, np.clip(k * np.log((goal + attempt1.SOFT) / (got + attempt1.SOFT)), -k, k), 0.0)
        bias = bias + np.where(held, 0.0, step[gid])      # at most 2 mV over the rounds: unclipped, so rung 4's
                                                          # -30 mV floor can't undo the offset above
        b.set_bias(bias)
        log["polish"].append({"round": r + 1, "upn_hz": round(float(hz[m["upn"]].mean()), 2),
                              "groups_within_2x": round(float(attempt1.within_factor_2(got, goal)[free_n > 0].mean()), 4)})
        print("polish", json.dumps(log["polish"][-1]), flush=True)
    threshold = b.params[b.cls[np.flatnonzero(m["kc"])[0]]]["threshold"]
    kc_types = o.types[m["kc"]]
    for r in range(2):
        u = resting(o, rec, seed + 20 + r, sample=True)["u"]
        for t in np.unique(kc_types):
            mask = o.types == t
            bias[mask] += (threshold - p3.KC_GAP_MV) - u[mask].mean()
        b.set_bias(bias)
    u = resting(o, rec, seed + 22, sample=True)["u"]
    log["kc_gap_mv"] = {t: round(float(threshold - u[o.types == t].mean()), 2) for t in np.unique(kc_types)}
    print("Kenyon cells' distance below threshold:", json.dumps(log["kc_gap_mv"]), flush=True)
    return log


def condition(o: p7.Olfaction, rec: Receptors, name: str, c: int) -> dict:
    spec = CONDITIONS[name]
    base = 40000 + 100 * c
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    rec.kinetics, rec.spontaneous = spec.get("kinetics", False), spec.get("spont", False)
    if rec.spontaneous:
        out["resting_recalibration"] = recalibrate_rest(o, rec, base + 60)
    silence = o.brain.cells(["APL"]) if spec.get("silence_apl") else ()
    hz = resting(o, rec, base + 95, silence)["hz"]
    types, m = o.types, o.m
    out["rest"] = {"brain_hz": round(float(hz.mean()), 3), "over_100hz": int((hz > 100).sum()),
                   "kc_hz": round(float(hz[m["kc"]].mean()), 3), "upn_hz": round(float(hz[m["upn"]].mean()), 2),
                   "orn_hz": round(float(hz[m["orn"]].mean()), 2),
                   **{f"{x}_hz": round(float(hz[types == x].mean()), 2) for x in p7.MBONS}}
    runner = None if name == "current" else make_runner(rec)
    out["odors"], responders = {}, {}
    for k, odor in enumerate(p7.ODORS):
        row, responders[odor] = p7.measure_odor(o, odor, base + k, base + 50 + k, silence, PEAK_HZ, runner)
        out["odors"][odor] = row
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "spikes_per_response", "evoked_spikes_0_1.4s", "pn_hz")}), flush=True)
    out["overlap_jaccard"] = p7.overlaps(responders)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    rec = Receptors(o)
    t = np.arange(0, 1.0, 1e-3)
    shapes = {}
    for name, tau_r in TAU_RISE.items():
        k = course(t, tau_r)
        shapes[name] = {"tau_r_s": tau_r, "peak_at_s": round(float(t[np.argmax(k)]), 3), "t90_s": round(float(t[np.argmax(k >= 0.9)]), 3),
                        "at_0.425s": round(float(course(0.425, tau_r)), 3), "at_1s": round(float(course(1.0, tau_r)), 3)}
    out = {"question": __doc__, "flies": p7.FLIES, "time_course": shapes,
           "spontaneous_hz": rec.spont, "conditions": {}}
    print(json.dumps(out["time_course"]), flush=True)
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = condition(o, rec, name, c)
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
