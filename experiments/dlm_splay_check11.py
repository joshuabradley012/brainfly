"""Exploratory check, written after review 12 and before it runs, not pre-registered and not a change to the model: four
things review 12 found missing from dlm_splay_check8.py's reading, put on record with this check's own runs.

Review 12 found:
- dlm_splay_check8.py's conclusion ("a falling phase response alone doesn't give flies' weak pairs") compared two
  things that differed in three ways at once:
  - Hürkey et al.'s model as published (condition A: about a quarter of flies' 20 ms coupling, ISI CV 0.064, MN1-4 at
    8.68 Hz and MN5 at 7.81);
  - leaky integrators at flies' coupling, CV 0.22 and 6.6 Hz.
- The conditions meant to test it at flies' coupling (B and C) failed calibration.
- At flies' coupling the network is bistable: once firing, it keeps firing below the drive at which it starts from
  rest.
- The implementation's network values, not only its single unit, can be checked against the paper.
Its numbers came from review-only runs.
Part 1, Hürkey et al.'s model as the paper ran it for those figures: dlm_splay_check8.py's equations, with 108.75 pA
for every unit:
- uncoupled, at noise 0.949 pA ms^0.5;
- homogeneous coupling (43.5 pS between every pair; their Fig. 3d and ED Fig. 6a) at noise 0.949 and 1.9.
The paper gives MN4-MN5's sync index as 0.54 (Fig. 3d), and splayness about 0.76 at 0.9 and 0.68 at 1.9 (ED Fig. 6a).
Part 2, leaky integrators like for like with dlm_splay_check8.py's A and D: dlm_splay_check6.py's units, with junctions
fitted (dlm_splay_check5.fitted_ratio) to A's 20 ms peak ratios (0.00551, 0.00244, 0.00174). Two conditions:
- "as A": each unit's kicks set uncoupled (dlm_splay_check10.kicks_for) for A's main-run CV at A's main-run rate
  (MN1-4: 0.064 at 8.678 Hz; MN5: 0.071 at 7.808 Hz). Each unit's bias is then found for that rate with the junctions:
  dlm_splay_check7.py's two passes on 8 runs of 60 s, with each unit within 2% or the condition reported as failing
  calibration.
- "as D": dlm_splay_check2.py's kicks (CV 0.22 at 6.6 Hz), all five at 6.6 Hz, biases found the same way.
Part 3, the firing branch at flies' coupling (dlm_splay_check8.py's fitted conductances), all five at one drive, at
noise 0.949 and 2.30. From rest, the drive is raised from 107.0 to 108.5 pA in steps of 0.05 pA, each held 10 s. Then,
from 20 s of firing at 108.5 pA, it is lowered back to 107.0 the same way. 4 starts each (seeds 5300 + start); each
step's rates.
Part 4, the switching in dlm_splay_check8.py's B and C: their main runs regenerated, with drives found again by
dlm_splay_check8.calibrated_drives, seeds as there, and checked against the JSON's per-run rates. In each run, the first
time MN1-4's mean rate over a 10 s window (stepped by 1 s) exceeds 5 Hz.
Parts 1 and 2 are measured as dlm_splay_check6.py measures (8 runs of 300 s after 3 s; seeds 5200 + 10 x condition),
with each unit's rate and CV, and the ten pairs against flies'.
Read:
- Part 1 checks the implementation at the network level.
- Part 2: if the leaky integrators' weak pairs come out nearer flies' (within 10 ms 0.16-0.31 times chance, dip10
  0.030-0.056) than A's and D's, then Hürkey et al.'s falling phase response holds them apart no better than the leaky
  integrator at the same coupling, irregularity and rates. If they come out about as A's and D's, the unit type doesn't
  matter there; if farther, the falling phase response helps.
- Part 3 gives the firing branch's lowest steady rates, and whether any drive gives all five 4.5-8 Hz.
- Part 4 gives when B's and C's runs switch on.

Ran (2026-10-12, 6 minutes):
- Part 1: the implementation reproduces the paper's network values. With homogeneous coupling, splayness is 0.761 at
  noise 0.949 and 0.679 at 1.9 (ED Fig. 6a: about 0.76 and 0.68), and MN4-MN5's sync index is 0.564 (Fig. 3d: 0.54).
  Uncoupled, the units fire at 6.56-6.58 Hz with CV 0.09 and independent phases (splayness 0.593). The coupling raises
  them to 8.42-8.43 Hz (8.29 at noise 1.9).
- Part 2: at the same coupling, irregularity and rates, the leaky integrators hold the weak pairs apart better than
  Hürkey et al.'s model, not equally. Both conditions calibrated within 2%.
  - As A (CV 0.064-0.066, MN1-4 at 8.66-8.69 Hz, MN5 at 7.82):
    - splayness 0.762 (A 0.713); preferred orders 0.77 (0.81); repeats 0.033 (0.023);
    - weak pairs: within 10 ms 0.33-0.38 times chance and dip10 0.065-0.074 (A 0.55-0.59 and 0.10-0.11; flies 0.16-0.31
      and 0.030-0.056);
    - MN5's pairs: 0.63-0.72 (A 1.03-1.06);
    - strong pairs: 0.015-0.022 (A 0.00; flies' two pairs 0.05 and 0.20).
  - As D (CV 0.24-0.25, 6.56-6.66 Hz):
    - splayness 0.712 (D 0.642); repeats 0.31 (D 0.21);
    - weak pairs: 0.60-0.67 times chance, dip10 0.11-0.12 (D 0.90-0.95 and 0.17-0.18);
    - MN5's pairs: 0.63-0.67 (D 0.94-0.99);
    - strong pairs: 0.63-0.65 (D 0.61).
  By the reading, Hürkey et al.'s falling phase response holds the weak pairs apart no better than the leaky integrator
  at the same coupling, irregularity and rates. Here it does worse. At flies' irregularity neither comes near flies'
  weak pairs.
- Part 3: at flies' coupling the network is bistable, and its firing branch never comes down to flies' rates.
  - At noise 0.949: rising from rest, the units stay silent through 108.15 pA and fire from 108.2 (11.8-12.7 Hz; 15.5-16.8
    Hz at 108.25-108.5). Lowered from firing, they keep firing down to 107.45 pA (MN1-4 at 9.1-9.3 Hz, MN5 at 4.9-5.2) and
    have stopped by 107.35.
  - At noise 2.30: silent through 108.05 pA, firing from 108.1-108.15 (14.7 Hz and up). Lowered, they fire down to 107.6
    (10.3-10.7 Hz, MN5 6.6-6.9) and have stopped by 107.45.
  - MN1-4's lowest steady rate is about 9-11 Hz, with MN5 at about 0.55-0.65 times theirs. No drive gives all five
    4.5-8 Hz, and none gives MN5 flies' ratio (0.98-1.26).
- Part 4: B's and C's main runs regenerate exactly (every run's rates as in dlm_splay_check8.json).
  - MN1-4 switch on at 0, 18, 18, 24, 29, 60, 79 and 115 s in B, and at 0, 0, 4, 16, 49, 61, 68 and 77 s in C (sorted).
  - Afterwards they fire at 14.3-14.6 Hz in B (MN5 11.2-11.4) and 13.5-13.9 Hz in C (MN5 10.7-11.0).

Correction (2026-10-12, review 13):
- Part 3's "fire from 108.2 (11.8-12.7 Hz ...)": that 10 s step switches on partway. At 108.2 pA the units stay silent
  for 1.7-2.2 s and then fire at 15.0-15.5 Hz (15.3 Hz on the way down; review 13, from these runs' spike times). From
  rest the network starts firing at about 15 Hz at noise 0.949. At 2.30 the first full firing step gives 14.7 Hz.
- Part 4's switch times are the starts of the first 10 s windows whose mean exceeds 5 Hz, 4-7 s before the switch. The
  onsets of steady firing are 4-121 s in B and 0-83 s in C. After them MN1-4 fire at 14.8 Hz in every B run and 13.9 Hz
  in C (review 13). The "rates after the switch" above count silent seconds.
- The like-for-like irregularity is approximate, and the approximation is conservative:
  - "As A" puts MN5's CV at 0.083, against A's 0.071.
  - "As D" runs at CV 0.24-0.25, against D's 0.21-0.22.
  Both make the leaky integrators more irregular, which works against them in the comparison.
- "As the paper ran it for those figures": these runs are 8 of 300 s at 10 us, where the paper ran 10 of 60 s at 3 us.
  MN4-MN5's 0.564 spans 0.49-0.59 across runs, against Fig. 3d's 0.54.
- The docstring's "8.678 Hz" is A's rounded MN1-4 rate; the code targets the four units' mean, 8.676 Hz. "Seeds 5300 +
  start" is, in the code, 5300 x 1000 + start going up and 5310 x 1000 + start going down, the same at both noises.

Correction (2026-10-12, review 14): the review-13 note's "4-7 s before the switch": the window starts lead the onsets
by 3.7-6.6 s in B and 0-6.3 s in C, where two runs fire from the start.

    python experiments/dlm_splay_check11.py      (writes experiments/dlm_splay_check11.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numba
import numpy as np

import dlm_splay_check as c1
import dlm_splay_check5 as c5
import dlm_splay_check6 as c6
import dlm_splay_check7 as c7
import dlm_splay_check8 as c8
import dlm_splay_check10 as c10

OUT = Path(__file__).with_suffix(".json")
SEED = 5200
HOMOGENEOUS_NS = 0.0435
LEVELS = np.round(np.arange(107.0, 108.5 + 1e-9, 0.05), 2)
STEP_S, BURN_S, STARTS = 10.0, 20.0, 4


@numba.njit(parallel=True, cache=True)
def _ramp(levels, step_steps, burn_steps, sigma, g, g_shab, dt, seeds, v0):
    """Each unit's spikes per level (levels, trials, n): the drive, the same for every unit, held at levels[0] for
    burn_steps and then at each level for step_steps; dlm_splay_check8._simulate's integration and spike detection."""
    trials, n = v0.shape
    counts = np.zeros((len(levels), trials, n), np.int64)
    for r in numba.prange(trials):
        np.random.seed(seeds[r])
        v = v0[r].copy()
        h, b = np.empty(n), np.empty(n)
        c8._steady(v, h, b)
        k1v, k1h, k1b = np.empty(n), np.empty(n), np.empty(n)
        k2v, k2h, k2b = np.empty(n), np.empty(n), np.empty(n)
        vs, hs, bs, noise, d = np.empty(n), np.empty(n), np.empty(n), np.empty(n), np.empty(n)
        last = np.full(n, -10 ** 12)
        above = np.zeros(n, np.bool_)
        dead = int(round(c8.DEAD_MS / dt))
        amp = sigma * np.sqrt(dt) / c8.C_PF
        for s in range(burn_steps + len(levels) * step_steps):
            k = 0 if s < burn_steps else (s - burn_steps) // step_steps
            for i in range(n):
                d[i] = levels[k]
                noise[i] = amp * np.random.normal(0.0, 1.0)
            c8._derivs(v, h, b, d, g, g_shab, k1v, k1h, k1b)
            for i in range(n):
                vs[i] = v[i] + k1v[i] * dt + noise[i]
                hs[i] = h[i] + k1h[i] * dt
                bs[i] = b[i] + k1b[i] * dt
            c8._derivs(vs, hs, bs, d, g, g_shab, k2v, k2h, k2b)
            for i in range(n):
                v[i] += 0.5 * (k1v[i] + k2v[i]) * dt + noise[i]
                h[i] += 0.5 * (k1h[i] + k2h[i]) * dt
                b[i] += 0.5 * (k1b[i] + k2b[i]) * dt
                up = v[i] > c8.SPIKE_MV
                if up and not above[i] and s - last[i] >= dead:
                    last[i] = s
                    if s >= burn_steps:
                        counts[k, r, i] += 1
                above[i] = up
    return counts


def ramp(levels: np.ndarray, sigma: float, g: np.ndarray, seed: int, v0: np.ndarray) -> np.ndarray:
    dt = c8.DT_MS
    counts = _ramp(np.asarray(levels, np.float64), int(round(STEP_S * 1e3 / dt)), int(round(BURN_S * 1e3 / dt)), sigma, g,
                   c8.G_SHAB["SNL"], dt, seed * 1000 + np.arange(len(v0)), v0)
    return counts / STEP_S                                      # rates (levels, starts, units)


def hurkey(name: str, g: np.ndarray, sigma: float, seed: int) -> dict:
    res = {"g_ns": float(g.max()), "sigma_pa_ms05": sigma, "drive_pa": c8.PUBLISHED["drive_pa"]}
    res.update(c6.summarize(c8.runs(np.full(c1.N, c8.PUBLISHED["drive_pa"]), sigma, g, c1.SECONDS, seed)))
    return res


def lif(kicks: tuple[float, float], targets: np.ndarray, coupling, start: np.ndarray, seed: int) -> dict:
    rates_for = lambda bb: np.array([np.mean([len(r[i]) / 60.0 for r in c1.spike_times(c10.brain(kicks, coupling, bb), 60.0, c1.SEED - 1)])
                                     for i in range(c1.N)])
    first = c7.biases_for(targets, rates_for, start, 3.0)
    biases = c7.biases_for(targets, rates_for, first, 0.05)
    cal = rates_for(biases)
    res = {"kick_hz": {"MN1-4": kicks[0], "MN5": kicks[1]}, "targets_hz": [round(float(x), 3) for x in targets],
           "calibration_rates_hz": [round(float(x), 3) for x in cal],
           "calibrated_within_2pct": bool(np.all(np.abs(cal / targets - 1) <= 0.02)), "unit_biases_mv": [round(float(x), 5) for x in biases]}
    res.update(c6.summarize(c1.spike_times(c10.brain(kicks, coupling, biases), c1.SECONDS, seed)))
    return res


def switch_times(runs: list[list[np.ndarray]]) -> list[float | None]:
    out = []
    for r in runs:
        t = np.sort(np.concatenate(r[:4]))
        starts = np.arange(0.0, c1.SECONDS - 10.0 + 1e-9, 1.0)
        n = np.searchsorted(t, starts + 10.0) - np.searchsorted(t, starts)
        hit = np.flatnonzero(n / (4 * 10.0) > 5.0)
        out.append(float(starts[hit[0]]) if len(hit) else None)
    return out


def show(name: str, res: dict, t0: float) -> None:
    s = res["summary"]
    print(name, json.dumps({k: res.get(k) for k in ("calibrated_within_2pct", "calibration_rates_hz", "unit_rates_hz", "unit_isi_cv")}),
          json.dumps({"splayness": s["splayness"][0], "r_mn4_mn5": s["r_mn4_mn5"][0], "preferred": s["preferred_order_share"][0],
                      "repeats": s["repeat_share"], "coincidence": s["coincidence_vs_chance_3ms"][0], "pairs": res["pairs"]}),
          f"({time.perf_counter() - t0:.0f} s)", flush=True)


def main() -> None:
    t0 = time.perf_counter()
    d2 = json.loads(Path(c1.OUT).with_name("dlm_splay_check2.json").read_text())
    d8 = json.loads(Path(c8.OUT).read_text())
    out = {"question": __doc__, "flies_pairs": c6.FLIES_PAIRS, "part1": {}, "part2": {}, "part3": {}, "part4": {}}
    # Part 1
    homogeneous = np.full((c1.N, c1.N), HOMOGENEOUS_NS) - np.eye(c1.N) * HOMOGENEOUS_NS
    for c, (name, g, sigma) in enumerate([("uncoupled, noise 0.949", np.zeros((c1.N, c1.N)), 0.949),
                                          ("homogeneous 43.5 pS, noise 0.949", homogeneous, 0.949),
                                          ("homogeneous 43.5 pS, noise 1.9", homogeneous, 1.9)]):
        out["part1"][name] = hurkey(name, g, sigma, SEED + 10 * c)
        show(f"part1 {name}", out["part1"][name], t0)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    # Part 2
    a = d8["conditions"]["A, as published"]
    ratio_a = {k: c5.fitted_ratio(v) for k, v in d8["implementation"]["published_peak_ratio_20ms"].items()}
    coupling_a, _ = c6.junctions(ratio_a, d8["implementation"]["published_peak_ratio_20ms"], False)
    out["part2"]["ratios_fitted_to_a"] = {k: round(v, 6) for k, v in ratio_a.items()}
    rates_a = np.array(a["unit_rates_hz"])
    cv_a = np.array(a["unit_isi_cv"])
    k14 = c10.kicks_for(float(round(rates_a[:4].mean(), 3)), float(round(cv_a[:4].mean(), 3)))
    k5 = c10.kicks_for(float(round(rates_a[4], 3)), float(round(cv_a[4], 3)))
    out["part2"]["kicks_as_a"] = {"MN1-4": k14, "MN5": k5}
    print("part2 kicks as A", json.dumps({"MN1-4": k14["chosen"], "MN5": k5["chosen"]}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
    start = np.array([k14["chosen"]["bias_mv"]] * 4 + [k5["chosen"]["bias_mv"]])
    targets = np.array([round(rates_a[:4].mean(), 3)] * 4 + [round(rates_a[4], 3)])
    out["part2"]["as A"] = lif((k14["chosen"]["kick_hz"], k5["chosen"]["kick_hz"]), targets, coupling_a, start, SEED + 30)
    show("part2 as A", out["part2"]["as A"], t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    hz = d2["calibration"]["chosen"]["kick_hz"]
    out["part2"]["as D"] = lif((hz, hz), np.full(c1.N, c1.TARGET_HZ), coupling_a, np.full(c1.N, d2["calibration"]["chosen"]["bias_mv"]), SEED + 40)
    show("part2 as D", out["part2"]["as D"], t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    # Part 3
    g_flies = c8.matrix(d8["fitted_g_ns"])
    rng = np.random.default_rng(5300)
    for sigma in (d8["published"]["sigma_pa_ms05"], d8["noise_for_cv"]["sigma_pa_ms05"]):
        row = {}
        for direction, levels, v0 in (("up from rest", LEVELS, np.full((STARTS, c1.N), -61.2) + rng.uniform(-0.2, 0.2, (STARTS, c1.N))),
                                      ("down from firing", LEVELS[::-1], rng.uniform(-62.0, -48.0, (STARTS, c1.N)))):
            r = ramp(levels, sigma, g_flies, 5300 + (0 if direction.startswith("up") else 10), v0)
            row[direction] = [{"drive_pa": float(lv), "mn1_4_hz": [round(float(x), 2) for x in r[k, :, :4].mean(1)],
                               "mn5_hz": [round(float(x), 2) for x in r[k, :, 4]]} for k, lv in enumerate(levels)]
        out["part3"][f"noise {sigma}"] = row
        print(f"part3 noise {sigma}", json.dumps({d: [(x["drive_pa"], float(np.median(x["mn1_4_hz"])), float(np.median(x["mn5_hz"]))) for x in v]
                                                    for d, v in row.items()}), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    # Part 4
    for c, name in ((1, "B, flies' coupling"), (2, "C, flies' coupling and irregularity")):
        cond = d8["conditions"][name]
        sigma = cond["sigma_pa_ms05"]
        drives = c8.calibrated_drives(sigma, g_flies)["drives_pa"]
        rs = c8.runs(drives, sigma, g_flies, c1.SECONDS, c8.SEED + 10 * c)
        rates = [[round(len(t) / c1.SECONDS, 2) for t in r] for r in rs]
        same = all(abs(x[0] - y["rate_hz"][0]) < 0.006 and abs(x[4] - y["rate_hz"][4]) < 0.006 for x, y in zip(rates, cond["runs"]))
        sw = switch_times(rs)
        firing = [[round(float(np.sum(t >= s) / (c1.SECONDS - s)), 2) for t in r] if s is not None else None for r, s in zip(rs, sw)]
        out["part4"][name] = {"drives_pa": [round(float(x), 4) for x in drives], "same_as_check8": same, "switch_s": sw,
                              "rates_after_switch_hz": firing}
        print(f"part4 {name}", json.dumps(out["part4"][name]), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
