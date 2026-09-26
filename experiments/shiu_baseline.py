"""Does Shiu et al.'s validated whole-brain recipe reproduce its taste results on the MaleCNS connectome?

Rung 1 of the research report's plan. brainfly.shiu.ShiuBrain runs Shiu et al. 2024's leaky
integrate-and-fire model (raw synapse counts x w_syn, 0.1 ms steps, silent at rest, Poisson drive)
on MaleCNS v1.0, which unlike FlyWire includes the nerve cord.

Neuron sets, all on the left side (MaleCNS types; the taste-modality labels are provisional):
  sugar LB3b + LB3c   water LB3a   bitter LB1a-d   Ir94e LB1e   readout MN9 (left; right reported)
  LB1a-d = bitter and LB1e = Ir94e-like follow the gustatory connectome papers as search results
  summarise them (primary text not opened). LB3a = water, LB3b-c = sugar, LB3d = high salt follow the
  flymsg MaleCNS port (unreviewed). Per-side counts agree with FlyWire's GRN lists (bitter 19 vs 20,
  Ir94e 9.5 vs 9).

Calibration, Shiu's procedure ("activation of sugar GRNs at 100 Hz resulted in roughly 80% of maximal
MN9 firing"): for w_syn = 0.275 x {1, 0.8, 0.65, 0.55, 0.45, 0.35} mV, drive sugar at
{10, 25, 50, 100, 150, 200} Hz (10 trials of 1 s each). Pick the w_syn whose MN9 L rate at 100 Hz is
closest to 80% of its maximum over those rates.

Tests at the calibrated w_syn, 30 trials of 1 s, drive at 100 Hz. Pass criteria, fixed before the
first run (all must hold):
  SUGAR   sugar raises MN9 L above 0 Hz (Shiu's "activated"). This is the calibration target, not an
          independent test.
  WATER   water raises MN9 L to >= 5 Hz (t >= 4 over trials)
  BITTER  sugar + bitter leaves MN9 L at least 25% below sugar alone (Welch t >= 4)
  IR94E   sugar + Ir94e leaves MN9 L at least 25% below sugar alone (Welch t >= 4)
  STABLE  after 1 s of sugar drive, the last 250 ms of a 500 ms drive-free tail carries < 1% of the
          network's spike rate during the drive, and <= 20 undriven neurons exceed 100 Hz during the drive
  NULL    sugar activates MN9 L (> 0 Hz over 10 trials) in <= 2 of 20 weight shuffles (Shiu's null:
          weights permuted across all connections) and in <= 2 of 20 degree-preserving rewirings
          (targets permuted: each neuron keeps its in- and out-degree and its outgoing weights and signs)
Not testable here: Shiu's JO-CE vs JO-F -> aBN1 grooming result, because MaleCNS v1.0 has no aBN1
annotation.
Reported but not criteria: the same tests at Shiu's raw w_syn = 0.275; MN9 R; how many neurons sugar
activates (Shiu, FlyWire: 45 at 10 Hz, 455 at 200 Hz).

Re-run 2026-09-26 on brainfly.shiu's corrected kernel, which now matches Brian2 spike for spike
(tests/test_shiu_brian2.py). The first run used a kernel that kept input arriving during
refractoriness, where Brian2 drops it, and ran its steps in a different order; that run is in git
history.

    python experiments/shiu_baseline.py            (writes experiments/shiu_baseline.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

from brainfly.shiu import W_SYN, ShiuBrain, counts

SETS = {"sugar": ["LB3b", "LB3c"], "water": ["LB3a"], "bitter": ["LB1a", "LB1b", "LB1c", "LB1d"], "ir94e": ["LB1e"]}
SCALES = [1.0, 0.8, 0.65, 0.55, 0.45, 0.35]
RATES = [10, 25, 50, 100, 150, 200]
SHUFFLES = 20
OUT = Path(__file__).with_name("shiu_baseline.json")


def welch(a: np.ndarray, b: np.ndarray) -> float:
    """t for mean(a) - mean(b), unequal variances."""
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else (np.inf if a.mean() != b.mean() else 0.0)


def calibrate(brain: ShiuBrain, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    grid = []
    for scale in SCALES:
        brain.w_syn = W_SYN * scale
        mn = [float(brain.run(1.0, drive=[(sugar, r)], seed=100 + r).rates[mn9[0]]) for r in RATES]
        ratio = mn[RATES.index(100)] / max(mn) if max(mn) > 0 else None
        grid.append({"w_syn": round(brain.w_syn, 4), "mn9_L_hz": [round(m, 2) for m in mn],
                     "ratio_100": None if ratio is None else round(ratio, 3)})
        print(f"  w_syn {brain.w_syn:.4f}: MN9 L {[round(m, 1) for m in mn]} Hz at {RATES} Hz sugar, "
              f"100 Hz / max = {grid[-1]['ratio_100']}", flush=True)
    pick = min((g for g in grid if g["ratio_100"] is not None), key=lambda g: abs(g["ratio_100"] - 0.8))
    return {"grid": grid, "w_syn": pick["w_syn"]}


def tests(brain: ShiuBrain, cells: dict, mn9: np.ndarray, sugar_rates=(10, 200)) -> dict:
    run = lambda drive, **kw: brain.run(1.0, drive=[(cells[k], 100.0) for k in drive], **kw)
    sugar = run(["sugar"], seed=1, tail=0.5)
    water, bitter, ir94e = run(["water"], seed=2), run(["sugar", "bitter"], seed=3), run(["sugar", "ir94e"], seed=4)
    L = lambda r: r.trial_rates[:, mn9[0]]
    t_water = L(water).mean() / (L(water).std(ddof=1) / np.sqrt(len(L(water))) + 1e-12)
    drop = lambda r: 1 - L(r).mean() / L(sugar).mean() if L(sugar).mean() > 0 else 0.0
    driven = np.zeros(brain.n, bool)
    driven[cells["sugar"]] = True
    bins_drive = sugar.timeline[:, : int(round(1.0 / sugar.bin))]
    bins_last = sugar.timeline[:, -int(round(0.25 / sugar.bin)):]
    tail_frac = float(bins_last.mean() / bins_drive.mean()) if bins_drive.mean() > 0 else 0.0
    hot = int((sugar.rates[~driven] > 100).sum())
    activated = {f"{r} Hz": int((brain.run(1.0, drive=[(cells["sugar"], r)], seed=50 + r).rates > 0).sum())
                 for r in sugar_rates}
    out = {
        "SUGAR": bool(L(sugar).mean() > 0), "WATER": bool(L(water).mean() >= 5 and t_water >= 4),
        "BITTER": bool(drop(bitter) >= 0.25 and welch(L(sugar), L(bitter)) >= 4),
        "IR94E": bool(drop(ir94e) >= 0.25 and welch(L(sugar), L(ir94e)) >= 4),
        "STABLE": bool(tail_frac < 0.01 and hot <= 20),
        "mn9_L_hz": {"sugar": round(float(L(sugar).mean()), 2), "water": round(float(L(water).mean()), 2),
                     "sugar+bitter": round(float(L(bitter).mean()), 2), "sugar+ir94e": round(float(L(ir94e).mean()), 2)},
        "mn9_R_hz": {k: round(float(r.rates[mn9[1]]), 2) for k, r in
                     (("sugar", sugar), ("water", water), ("sugar+bitter", bitter), ("sugar+ir94e", ir94e))},
        "t_water": round(float(t_water), 2), "bitter_drop": round(float(drop(bitter)), 3),
        "t_bitter": round(welch(L(sugar), L(bitter)), 2), "ir94e_drop": round(float(drop(ir94e)), 3),
        "t_ir94e": round(welch(L(sugar), L(ir94e)), 2), "tail_fraction": round(tail_frac, 5),
        "undriven_over_100hz": hot, "network_hz_during_sugar": round(float(bins_drive.mean()), 1),
        "activated_by_sugar": activated,
    }
    return out


def nulls(C: sparse.csc_matrix, w_syn: float, sugar: np.ndarray, mn9: np.ndarray) -> dict:
    rng = np.random.default_rng(7)
    result = {}
    for name in ("weight_shuffle", "degree_preserving"):
        hits = []
        for k in range(SHUFFLES):
            if name == "weight_shuffle":
                M = sparse.csc_matrix((rng.permutation(C.data), C.indices, C.indptr), shape=C.shape)
            else:
                M = sparse.csc_matrix((C.data, rng.permutation(C.indices), C.indptr), shape=C.shape)
            rate = float(ShiuBrain(w_syn=w_syn, trials=10, matrix=M).run(1.0, drive=[(sugar, 100.0)], seed=200 + k).rates[mn9[0]])
            hits.append(rate)
        result[name] = {"mn9_L_hz": [round(h, 2) for h in hits], "activated": int(sum(h > 0 for h in hits))}
        print(f"  {name}: MN9 L activated in {result[name]['activated']}/{SHUFFLES} ({result[name]['mn9_L_hz']})", flush=True)
    result["NULL"] = all(result[k]["activated"] <= 2 for k in ("weight_shuffle", "degree_preserving"))
    return result


def main() -> None:
    t0 = time.perf_counter()
    C = counts().tocsc()
    brain = ShiuBrain(trials=10)
    cells = {k: brain.cells(v, side="L") for k, v in SETS.items()}
    mn9 = np.concatenate([brain.cells(["MN9"], side="L"), brain.cells(["MN9"], side="R")])
    print({k: len(v) for k, v in cells.items()}, "MN9", mn9, flush=True)
    results = {"criteria": __doc__, "sets": {k: len(v) for k, v in cells.items()}}

    print("calibration (10 trials per point)", flush=True)
    results["calibration"] = cal = calibrate(brain, cells["sugar"], mn9)
    print(f"calibrated w_syn = {cal['w_syn']} mV", flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    brain = ShiuBrain(w_syn=cal["w_syn"], trials=30)
    results["tests"] = t = tests(brain, cells, mn9)
    print("tests:", json.dumps(t), flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    print("nulls (10 trials each)", flush=True)
    results["nulls"] = nl = nulls(C, cal["w_syn"], cells["sugar"], mn9)
    results["pass"] = bool(all(t[k] for k in ("SUGAR", "WATER", "BITTER", "IR94E", "STABLE")) and nl["NULL"])
    print(f"PASS: {results['pass']}", flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    brain = ShiuBrain(w_syn=W_SYN, trials=30)
    results["raw_w_syn_0.275"] = raw = tests(brain, cells, mn9)
    print("at raw w_syn 0.275:", json.dumps(raw), flush=True)
    results["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
