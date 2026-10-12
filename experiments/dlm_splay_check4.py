"""Exploratory check, written after dlm_splay_check3.py's result and before it runs, not pre-registered and not a change
to the model: do the DLM units splay as flies' do if most of their irregularity is shared?

dlm_splay_check3.py gave the unit flies' AHP, and the spikelets stopped synchronizing the units. But the AHP makes the
unit so regular that the private noise needed for its irregularity left the measured coupling little pull: splayness
0.61-0.64 (flies 0.73-0.79), at a CV of only 0.16. Hürkey et al.'s model, and these checks so far, give each unit
private noise. Flies' DLM motor neurons share 88-95% of their input (MaleCNS), all five fire at one rate that changes
with power, and their 4-spike windows hold a repeat only 9% of the time, against 24-35% in these runs. So flies'
irregularity may be largely shared.
Model: dlm_splay_check3.py's unit (flies' AHP), five units, the spikelets as there. Each run's drive is the unit's bias
plus a shared fluctuation, an Ornstein-Uhlenbeck process with a 0.5 s time constant (a few interspike intervals; flies'
time scale isn't known), the same for all five and applied every 10 ms, plus private kicks of 0.3 mV (larger than
check 3's 0.1 mV, so that private noise alone can reach the target). For each shared share f of the ISI variance (0.5,
0.8 and 0.95), the private kicks' rate is set so that private noise alone gives a CV of 0.22 x sqrt(1 - f). The shared
fluctuation's size is then set so that both together give 0.22, and the bias so that the units fire at 6.6 Hz, all on
the uncoupled units (bisection, 60 s). Conditions at each share, the bias found again for 6.6 Hz in each:
  uncoupled
  measured + spikelet   (CCs 0.023 / 0.011, MN5 0.0075; spikelets as dlm_splay_check3.py's)
Measured as dlm_splay_check3.py measures, with the share of 4-spike windows holding a repeat (flies 9%). 8 runs of 300 s
after 3 s each, run one at a time, each with its own shared fluctuation (seeds 4500 + 10 x share's index + condition,
plus 100 x run).

    python experiments/dlm_splay_check4.py      (writes experiments/dlm_splay_check4.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import dlm_splay_check as c1
import dlm_splay_check3 as c3

OUT = Path(__file__).with_suffix(".json")
KICK_MV = 0.3
TAU_SHARED, PIECE = 0.5, 0.01
SHARES = (0.5, 0.8, 0.95)
SEED = 4500


def unit_brain(bias: float, kick_hz: float, coupling=None, spikelet: float = 0.0):
    b = c3.brain(bias, kick_hz, coupling, spikelet, trials=1)
    b.set_type("all", noise_kick=KICK_MV)
    return b


def run(bias: float, kick_hz: float, sd_mv: float, seconds: float, seed: int, coupling=None, spikelet: float = 0.0):
    """One run's spike times per unit, the shared fluctuation (sd_mv, OU over TAU_SHARED) set every PIECE s."""
    b = unit_brain(bias, kick_hz, coupling, spikelet)
    b.reset(seed)
    rng = np.random.default_rng(seed)
    a = np.exp(-PIECE / TAU_SHARED)
    ou = rng.standard_normal()
    steps = int(round(PIECE / c1.DT))
    burn, total = int(round(c1.BURN / PIECE)), int(round(seconds / PIECE))
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


def rate_cv(times) -> tuple:
    rate = float(np.mean([len(t) for t in times])) / 60.0
    cvs = [np.diff(t).std() / np.diff(t).mean() for t in times if len(t) > 2]
    return rate, float(np.mean(cvs)) if cvs else 0.0


def bias_for(kick_hz: float, sd_mv: float, coupling=None, spikelet: float = 0.0) -> tuple:
    mean_kick = kick_hz * KICK_MV * c1.UNIT["tau_m"]
    lo, hi = -mean_kick - 20.0, 120.0 - mean_kick
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        rate, cv = rate_cv(run(mid, kick_hz, sd_mv, 60.0, SEED - 1, coupling, spikelet))
        lo, hi = (mid, hi) if rate < c1.TARGET_HZ else (lo, mid)
    return 0.5 * (lo + hi), rate, cv


def calibrate(share: float) -> dict:
    target_private = c1.TARGET_CV * np.sqrt(1 - share)
    lo, hi = 0.2, 50000.0
    for _ in range(14):                              # private kicks alone for target_private
        mid = float(np.sqrt(lo * hi))
        bias, rate, cv = bias_for(mid, 0.0)
        lo, hi = (mid, hi) if cv < target_private else (lo, mid)
    kick_hz, private_cv = mid, cv
    lo, hi = 0.0, 40.0
    for _ in range(14):                              # then the shared fluctuation's size for 0.22 in all
        sd = 0.5 * (lo + hi)
        bias, rate, cv = bias_for(kick_hz, sd)
        lo, hi = (sd, hi) if cv < c1.TARGET_CV else (lo, sd)
    return {"share": share, "kick_hz": round(kick_hz, 3), "private_cv": round(private_cv, 3),
            "target_private_cv": round(float(target_private), 3), "shared_sd_mv": round(sd, 4), "bias_mv": round(bias, 4),
            "rate_hz": round(rate, 2), "isi_cv": round(cv, 3)}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "flies": {**c1.FLIES, "repeat_share": 0.089}, "unit": c3.UNIT, "kick_mv": KICK_MV,
           "tau_shared_s": TAU_SHARED, "spikelet_mv": c3.SPIKELET_MV, "shares": {}}
    measured = c1.ratios(0.023, 0.011, 0.0075)
    for si, share in enumerate(SHARES):
        cal = calibrate(share)
        print("calibrated", json.dumps(cal), f"({time.perf_counter() - t0:.0f} s)", flush=True)
        row = {"calibration": cal, "conditions": {}}
        for c, (name, coupling, spikelet) in enumerate([("uncoupled", None, 0.0),
                                                        ("measured + spikelet", measured, c3.SPIKELET_MV)]):
            bias, rate, cv = bias_for(cal["kick_hz"], cal["shared_sd_mv"], coupling, spikelet)
            runs = [run(bias, cal["kick_hz"], cal["shared_sd_mv"], c1.SECONDS, SEED + 10 * si + c + 100 * r, coupling, spikelet)
                    for r in range(c1.RUNS)]
            res = c1.measure(runs)
            for r in res["runs"]:
                complete = 1.0 - r["orders"].get("rest", 0.0)
                r["preferred_share_of_complete"] = round(r["preferred_order_share"] / complete, 4) if complete > 0 else None
            vals = [r["preferred_share_of_complete"] for r in res["runs"] if r["preferred_share_of_complete"] is not None]
            res["summary"]["preferred_share_of_complete"] = [round(float(np.median(vals)), 4), round(min(vals), 4),
                                                             round(max(vals), 4)]
            res["summary"]["repeat_share"] = round(float(np.median([r["orders"].get("rest", 0.0) for r in res["runs"]])), 4)
            res["bias_mv"] = round(bias, 4)
            row["conditions"][name] = res
            print(f"share {share}", name, f"bias {bias:.3f}", json.dumps(res["summary"]), f"({time.perf_counter() - t0:.0f} s)",
                  flush=True)
            out["shares"][str(share)] = row
            OUT.write_text(json.dumps(out, indent=1, default=float))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1, default=float))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
