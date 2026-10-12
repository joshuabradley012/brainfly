"""Exploratory check, written after review 8 and before it runs, not pre-registered and not a change to the model: the
key conditions of dlm_splay_check2-4.py with the junctions at flies' coupling as flies measured it.

Review 8 found that flies' coupling coefficients (CC 0.023 between MN1-2 and MN3-4, 0.011 between the other MN1-4
pairs) are peak ratios of 20 ms current steps, while dlm_splay_check.py's ratios() converted them as steady-state
coefficients, CC / (1 - CC). In the unit's 20 ms membrane that passed only about 0.56 of flies' 20 ms ratio, and 0.44
of the AHP coupling flies' Fig. 2h pair shows. So every "measured" condition ran at about half flies' coupling.
Coupling: for each pair class, the conductance (as a share of the leak) at which a 20 ms step into one of two like
passive units gives the other a peak depolarization CC times the stepped unit's peak, found by bisection in the
simulator itself: strong pairs 0.023, weak pairs 0.011, MN5 to each of MN1-4 0.0075 (Hürkey et al.'s model's
convention, half the others' mean; MN5's was never measured). Spikelets, where used, are dlm_splay_check3.py's on the
strong pairs (0.035 mV) and scaled by CC on the others (0.0167 and 0.0114 mV), not by the conductance.
Conditions, each with its bias found again for 6.6 Hz, and the noise as its check calibrated it:
  LIF, private                 dlm_splay_check2.py's unit and kicks (10.8 Hz of 0.1 mV; CV 0.22), the junctions alone
  LIF, private + spikelets     the same with spikelets
  AHP, 95% shared + spikelets  dlm_splay_check4.py's AHP unit, its share-0.95 calibration (kicks and shared fluctuation)
  AHP, 95% shared              the same without spikelets
  AHP, 80% shared + spikelets  its share-0.8 calibration (the share whose uncoupled state looked like shakB flies')
Measured as dlm_splay_check4.py measures; 8 runs of 300 s after 3 s (seeds 4600 + 10 x condition, plus 100 x run in the
shared conditions). The uncoupled references are the earlier checks' own runs.

Ran (2026-10-11, 114 s): at flies' coupling no configuration meets every measure. The leaky integrator without
spikelets comes nearest, and the AHP unit with spikelets organizes MN1-4 but not MN5.
- Coupling: the fitted conductances are 0.0423, 0.0199 and 0.0135, 1.79-1.80 times the steady-state conversion, which
  gave 20 ms peak ratios of only 0.56 of flies' (0.0130, 0.0062, 0.0042).
- LIF, private (flies: splayness 0.73-0.79, r 0.49-0.63, dip10 0.02-0.10, preferred orders 48-70% of windows,
  coincidences below chance, strong pairs' vector strength about 0.7, 9% of windows with a repeat):
  - splayness 0.719, r 0.602, dip10 0.086;
  - preferred orders 51% of windows (76% of complete ones), coincidences 0.67 times chance;
  - MN2 at 0.50 of MN1's cycle with vector strength 0.59;
  - but 34% of windows with a repeat.
- LIF, private + spikelets: synchrony again. The strong pairs fire together (MN2 at 0.00 of MN1's cycle), with
  coincidences 4.5 times chance and splayness 0.544.
- AHP, 95% shared + spikelets:
  - MN1-4 organized more tightly than flies': preferred orders 78% of windows (81% of complete ones), 4% of windows
    with a repeat, the strong pairs in antiphase with vector strength 0.60, and coincidences 0.87 times chance;
  - but MN5 doesn't avoid MN4 (dip10 0.22, the null's 0.20; r 0.647), and splayness over the five is 0.647.
- AHP, 95% shared, no spikelets: nearly the same (splayness 0.650, dip10 0.20, preferred 76%), so with flies' AHP the
  spikelets barely act.
- AHP, 80% shared + spikelets: weaker order (44% of windows, 13% with a repeat), splayness 0.624, coincidences 1.05.
So at flies' strength the coupling does what flies' does to MN1-4 with either unit: the strong pairs fire in
antiphase, the preferred orders dominate, and spikes avoid each other. That holds for the leaky integrator only
without spikelets, and for the AHP unit with them. What fails is MN5. Its junctions are Hürkey et al.'s model's
convention (half the others' mean) and have never been measured, and with them MN5 fires independently of MN4.
Splayness over all five stays below flies' (0.65-0.72 against 0.73-0.79).

Correction (2026-10-11, review 9):
- The reading above blames MN5's assumed coupling for the AHP condition's shortfall. That is wrong. In that condition
  only the strong pairs and the order look like flies'. The four weakly coupled MN1-4 pairs, at measured coupling, fire
  about independently too: near-zero shares 0.16-0.21 and spikes within 10 ms at 0.83-1.10 times chance, against
  flies' 0.03-0.06 and 0.16-0.31 times. Coupling MN5 like a measured weak pair (0.0199) leaves its near-zero share at
  0.17 and splayness at 0.66 (0.14 and 0.66 at the strong-pair value; review 9's reruns). So the AHP unit organizes
  the strong pairs (in antiphase, vector strength 0.60 against flies' 0.70-0.73) and the order, not MN1-4. "Tighter
  than flies'" holds only for the order (78%; flies 48-70%) and the repeats (4%; flies 5-20%).
- For the leaky integrator it goes the other way. Its MN5 pairs already fall in flies' ranges (within 10 ms at
  0.42-0.45 times chance, flies 0.34-0.58), while its weak MN1-4 pairs are looser than flies' (0.55-0.61 times
  chance). With MN5 coupled like a weak pair, its splayness is 0.736, inside flies' 0.73-0.79 (review 9's rerun).
- "In flies' ranges on most measures": the leaky integrator is inside on four of the seven listed (r, dip10, orders,
  coincidences), and outside on splayness, the repeats and the strong pairs' vector strength (0.59 against
  0.70-0.73).
- The weak and MN5 spikelets, scaled by CC as the code does, are 0.0169 and 0.0115 mV (the docstring's 0.0167 and
  0.0114 are dlm_splay_check3.py's). They rest on the Fig. 2h pair being a strong one, which its AHP coupling (0.038,
  about r/(1 + r) for a strong pair) supports.
- The 1.8 times holds in the unit's 20 ms membrane; in flies' probable 13-15 ms membrane the same coefficients need
  1.5-1.6 times.

Correction (2026-10-11, review 10):
- The leaky-integrator conditions gave all five units one drive, so the units didn't fire at one rate. In "LIF,
  private" MN1-4 fire at 6.10-6.12 Hz (CV 0.28) and MN5 at 8.60 Hz (CV 0.13), 1.41 times as fast, because its assumed
  junctions load it less. In flies all five fire at one rate (MN5 at 0.98-1.26 times MN1-4) with similar CVs. So "at
  flies' rate and irregularity" is wrong. Review 9's note that MN5's pairs "already fall in flies' ranges" reflects MN5
  drifting past MN4 at another rate. At a common rate (review 10's rerun: MN5's drive 0.042 mV lower) MN4-MN5's dip10 is
  0.121 and MN5's within-10 ms ratios 0.67-0.70, outside flies' ranges, while splayness is 0.733. With spikelets MN5
  runs 1.10 times MN1-4; in the AHP conditions 1.01. dlm_splay_check6.py gives each unit its own drive and reports every
  pair.

    python experiments/dlm_splay_check5.py      (writes experiments/dlm_splay_check5.json)
"""
from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import sparse

import dlm_splay_check as c1
import dlm_splay_check3 as c3
import dlm_splay_check4 as c4
from brainfly.hybrid import HybridBrain

OUT = Path(__file__).with_suffix(".json")
SEED = 4600
CC = {"strong": 0.023, "weak": 0.011, "mn5": 0.0075}
SPIKELET_STRONG = c3.SPIKELET_MV


def pair_class(i: int, j: int) -> str:
    return "mn5" if 4 in (i, j) else "strong" if (i, j) in c1.STRONG else "weak"


def peak_ratio(ratio: float) -> float:
    """Two like passive units (the check unit's membrane, threshold out of reach), a 20 ms step of 10 mV into the first:
    the second's peak over the first's."""
    labels = {"cell_type": np.array(["a", "b"]), "side": np.array(["R", "R"]), "superclass": np.array(["t", "t"])}
    coupling = sparse.csr_matrix((np.array([ratio, ratio], np.float32), ([0, 1], [1, 0])), shape=(2, 2))
    b = HybridBrain(matrix=sparse.csr_matrix((2, 2), dtype=np.float32), labels=labels, trials=1, dt=c1.DT, w_syn=1.0,
                    types={"all": {**c1.UNIT, "threshold": 1e6}}, coupling=coupling)
    b.reset(0)
    trace = []
    b.set_bias(np.array([10.0, 0.0]))
    for _ in range(200):                           # 20 ms step
        b.advance(1)
        trace.append(b.u[0].copy())
    b.set_bias(np.array([0.0, 0.0]))
    for _ in range(400):                           # and 40 ms after it, for the partner's lagging peak
        b.advance(1)
        trace.append(b.u[0].copy())
    t = np.array(trace)
    return float(t[:, 1].max() / t[:, 0].max())


def fitted_ratio(cc: float) -> float:
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if peak_ratio(mid) < cc else (lo, mid)
    return 0.5 * (lo + hi)


def matrices(ratio: dict, spikelets: bool):
    rows, cols, vals, gvals = [], [], [], []
    for i, j in combinations(range(c1.N), 2):
        k = pair_class(i, j)
        rows += [i, j]
        cols += [j, i]
        vals += [ratio[k]] * 2
        gvals += [SPIKELET_STRONG * CC[k] / CC["strong"]] * 2
    coupling = sparse.csr_matrix((np.array(vals, np.float32), (rows, cols)), shape=(c1.N, c1.N))
    gap = sparse.csr_matrix((np.array(gvals, np.float32), (rows, cols)), shape=(c1.N, c1.N)) if spikelets else None
    return coupling, gap


def unit(kind: str, bias: float, kick_hz: float, kick_mv: float, coupling, gap, trials: int) -> HybridBrain:
    labels = {"cell_type": np.array([f"MN{k + 1}" for k in range(c1.N)]), "side": np.array(["R"] * c1.N),
              "superclass": np.array(["motor"] * c1.N)}
    u = c1.UNIT if kind == "LIF" else c3.UNIT
    return HybridBrain(matrix=sparse.csr_matrix((c1.N, c1.N), dtype=np.float32), labels=labels, trials=trials, dt=c1.DT,
                       w_syn=1.0, types={"all": {**u, "bias": bias, "noise_rate": kick_hz, "noise_kick": kick_mv}},
                       coupling=coupling, gap=gap, w_poi=40.0)


def private_bias(kick_hz: float, coupling, gap) -> float:
    """dlm_splay_check2.bias_for, for the LIF unit with these junctions."""
    mean_kick = kick_hz * c1.KICK_MV * c1.UNIT["tau_m"]
    lo, hi = 7.0 - mean_kick - 3.0, 7.0 - mean_kick + 3.0
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        t = c1.spike_times(unit("LIF", mid, kick_hz, c1.KICK_MV, coupling, gap, c1.RUNS), 60.0, c1.SEED - 1)
        rate = float(np.mean([[len(x) / 60.0 for x in run] for run in t]))
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi)


def shared_run(bias: float, kick_hz: float, sd_mv: float, seconds: float, seed: int, coupling, gap):
    """dlm_splay_check4.run, with these junctions."""
    b = unit("AHP", bias, kick_hz, c4.KICK_MV, coupling, gap, 1)
    b.reset(seed)
    rng = np.random.default_rng(seed)
    a = np.exp(-c4.PIECE / c4.TAU_SHARED)
    ou = rng.standard_normal()
    steps = int(round(c4.PIECE / c1.DT))
    burn, total = int(round(c1.BURN / c4.PIECE)), int(round(seconds / c4.PIECE))
    times = [[] for _ in range(c1.N)]
    for k in range(burn + total):
        ou = a * ou + np.sqrt(1 - a * a) * rng.standard_normal()
        b.set_bias(np.full(c1.N, sd_mv * ou))
        if k < burn:
            b.advance(steps)
            continue
        _, sp = b.advance(steps, record=np.arange(c1.N))
        for _, step, i in zip(*np.nonzero(sp)):
            times[i].append(((k - burn) * steps + step) * c1.DT)
    return [np.array(t) for t in times]


def shared_bias(kick_hz: float, sd_mv: float, coupling, gap) -> float:
    mean_kick = kick_hz * c4.KICK_MV * c1.UNIT["tau_m"]
    lo, hi = -mean_kick - 20.0, 120.0 - mean_kick
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        t = shared_run(mid, kick_hz, sd_mv, 60.0, c4.SEED - 1, coupling, gap)
        rate = float(np.mean([len(x) for x in t])) / 60.0
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi)


def summarize(runs) -> dict:
    res = c1.measure(runs)
    for r in res["runs"]:
        complete = 1.0 - r["orders"].get("rest", 0.0)
        r["preferred_share_of_complete"] = round(r["preferred_order_share"] / complete, 4) if complete > 0 else None
    vals = [r["preferred_share_of_complete"] for r in res["runs"] if r["preferred_share_of_complete"] is not None]
    res["summary"]["preferred_share_of_complete"] = [round(float(np.median(vals)), 4), round(min(vals), 4), round(max(vals), 4)]
    res["summary"]["repeat_share"] = round(float(np.median([r["orders"].get("rest", 0.0) for r in res["runs"]])), 4)
    res["summary"]["mn4_in_mn3"] = [round(float(np.median([r["mn4_in_mn3"][k] for r in res["runs"]])), 3) for k in (0, 1)]
    return res


def main() -> None:
    t0 = time.perf_counter()
    ratio = {k: fitted_ratio(cc) for k, cc in CC.items()}
    steady = {k: cc / (1 - cc) for k, cc in CC.items()}
    out = {"question": __doc__, "flies": json.loads(Path(c4.OUT).read_text())["flies"],
           "ratio_fitted_20ms": {k: round(v, 5) for k, v in ratio.items()},
           "ratio_steady_state": {k: round(v, 5) for k, v in steady.items()},
           "fitted_over_steady": {k: round(ratio[k] / steady[k], 3) for k in CC},
           "peak_ratio_at_steady_state_ratio": {k: round(peak_ratio(steady[k]), 5) for k in CC}, "conditions": {}}
    print("coupling", json.dumps({k: out[k] for k in ("ratio_fitted_20ms", "fitted_over_steady", "peak_ratio_at_steady_state_ratio")}),
          flush=True)
    d2 = json.loads(Path(c1.OUT).with_name("dlm_splay_check2.json").read_text())
    d4 = json.loads(Path(c4.OUT).read_text())
    lif_hz = d2["calibration"]["chosen"]["kick_hz"]
    conditions = [("LIF, private", "LIF", None, False), ("LIF, private + spikelets", "LIF", None, True),
                  ("AHP, 95% shared + spikelets", "AHP", "0.95", True), ("AHP, 95% shared", "AHP", "0.95", False),
                  ("AHP, 80% shared + spikelets", "AHP", "0.8", True)]
    for c, (name, kind, share, spikelets) in enumerate(conditions):
        coupling, gap = matrices(ratio, spikelets)
        if kind == "LIF":
            bias = private_bias(lif_hz, coupling, gap)
            runs = c1.spike_times(unit("LIF", bias, lif_hz, c1.KICK_MV, coupling, gap, c1.RUNS), c1.SECONDS, SEED + 10 * c)
        else:
            cal = d4["shares"][share]["calibration"]
            bias = shared_bias(cal["kick_hz"], cal["shared_sd_mv"], coupling, gap)
            runs = [shared_run(bias, cal["kick_hz"], cal["shared_sd_mv"], c1.SECONDS, SEED + 10 * c + 100 * r, coupling, gap)
                    for r in range(c1.RUNS)]
        res = summarize(runs)
        res["bias_mv"] = round(bias, 5)
        out["conditions"][name] = res
        print(name, f"bias {bias:.4f}", json.dumps(res["summary"]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
