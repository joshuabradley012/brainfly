"""Rung 6 (pre-registered): does the resting brain relay giant fiber spikes to the jump and flight muscles like a
fly, and does removing the giant fiber's electrical synapses, as in shakB2 mutants, slow or silence the relay as in
flies?

Rung 6 (README): "giant fiber to jump muscle in 0.7-1.2 ms, slowing without the gap junctions as in shakB
mutants". The test is research_notes/Embodied fly connectome simulation/escape_circuit.md's (its 1.4), with the
constants escape_relay.py (exploratory) measured, fixed here before any run of this test.
Model: taste_escape.py's brain (which tastes and escapes; its model and calibrated biases), plus escape_relay.py's
relay: one-way spikelets from each giant fiber (DNp01) to its own TTMn and PSI, and PSI -> DLMn fast synapses
(0.3 ms, depressing with PSI) onto the DLMn MaleCNS's PSI contacts; the jump and flight motor neurons (TTMn,
STTMm, PSI, DLMn) quieted at rest by escape_relay.py's procedure, each resetting 5 mV below its own lowered rest.
Constants (escape_relay.json): SIZES_MV (spikelets and fast synapses, per target neuron), PSI_DEPRESSION (f, tau),
  RESETS_MV (the quieted types' resets), QUIET_BIAS (the quieted group biases, escape_relay/quiet.npz)
  delays outside the model: GF axon 0.3 ms, TTMn -> TTM 0.5 ms, DLMn -> DLM 0.6 ms (Kadas et al. 2019; Thomas &
  Wyman 1984), so a muscle's latency is 0.3 ms + (motor neuron spike - GF spike) + its own delay
Conditions: INTACT; SHAKB, the spikelets removed (chemical synapses and the fast PSI -> DLMn synapse kept);
NULL, 2 degree-preserving rewirings of the chemical network (eyes_at_rest.py's), each recalibrated as
taste_escape.py's nulls were and quieted by the same procedure, with the same relay.
Protocols (8 flies each, both giant fibers forced to spike together, as by electrodes in the brain; fresh seeds):
  single   50 GF spikes, 1 s apart, after 1 s at rest
  trains   10 trains of 10 GF spikes at 100 Hz and at 250 Hz, each from a fresh rest
  quiet    100 s at rest
  looms    eyes_at_rest.py's fast loom on each side at gain 1 (escape_at_rest2.py's confirmed gain), 10 per fly
A motor neuron answers a GF spike if it fires within 0.5 ms (TTMn) or 1.2 ms (DLMn) after it; GF spikes that
fall in a motor neuron's own refractory period still count as stimuli.
Criteria, INTACT (all):
  W1  median TTM latency 0.7-1.2 ms, median DLM latency 1.3-1.7 ms, their difference 0.24-0.6 ms (single)
  W2  TTMn answer at least 95% of single GF spikes, DLMn at least 90%
  W3  TTMn follow at least 95% at 100 Hz and 80% at 250 Hz; DLMn at least 70% at 100 Hz and at most 60% at 250 Hz
      (flies: TTM 100% and 88-100%; DLM 84% and 28-57%)
  W4  in 100 s at rest, no fly's TTMn (both together) fire more than one spike without a GF spike in the 5 ms
      before, and likewise its PSI
  W5  in at least 95% of the looms that fire the loomed side's GF, that side's TTMn fires within 0.5 ms of the
      GF's first spike
Criteria, SHAKB (all):
  S1  TTMn answer at most 50% of single GF spikes, or their median latency is at least 0.4 ms longer than intact
  S2  TTMn follow at most 30% at 100 Hz (flies 10-26%)
  S3  DLMn answer at most 5% of single GF spikes (flies: none)
  S4  in at least 80% of the looms that fire the loomed side's GF, that side's TTMn doesn't fire within 2 ms of
      the GF's first spike
Criterion, NULL: in each rewiring, the loomed side's TTMn fires during the loom's last 0.5 s in at most half as
many looms as in INTACT.
Pass: every W, every S, and NULL.
Reported: latency distributions, twin pulses (10, 8, 6, 4, 3 and 2 ms apart; 5 pairs each), whether one or both
TTMn fire per loom, and an "aged" condition with the spikelets at 1.9/3 of their size (single spikes, trains).

    python experiments/rung6_relay.py            (writes experiments/rung6_relay.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import escape_relay as relay
import eyes_at_rest as eyes
from eyepath_fast import scenes

OUT = Path(__file__).with_suffix(".json")
FIXED = json.loads(Path(__file__).with_name("escape_relay.json").read_text())
SIZES_MV = {int(k): v for k, v in FIXED["size_mv"].items()}
PSI_DEPRESSION = (FIXED["depression"]["chosen"]["f"], FIXED["depression"]["chosen"]["tau_s"])
RESETS_MV = FIXED["resets_mv"]
D_GF, D_TTM, D_DLM = 0.3e-3, 0.5e-3, 0.6e-3
TTMN_WINDOW, DLMN_WINDOW = 5, 12                  # steps (0.5 and 1.2 ms)
GAIN, LOOMS, SEED = 1.0, 10, 6000


def quiet_bias(s: eyes.Setup) -> np.ndarray:
    """taste_escape's biases with escape_relay's quieted groups."""
    q = np.load(relay.HERE / "quiet.npz")
    assert np.array_equal(q["groups"], s.names)
    return q["bias"]


def build(condition: str) -> eyes.Setup:
    """intact; shakB, the spikelets gone and the fast PSI -> DLMn synapse kept; aged, spikelets at 1.9/3 of their size."""
    c = relay.cells()
    spikelet = {c["ttmn"]["L"], c["ttmn"]["R"], c["psi"]["L"], c["psi"]["R"]}
    size = {"intact": SIZES_MV,
            "shakB": {k: v for k, v in SIZES_MV.items() if k not in spikelet},
            "aged": {k: v * 1.9 / 3 if k in spikelet else v for k, v in SIZES_MV.items()}}[condition]
    s = relay.setup(size, PSI_DEPRESSION, seed=5, resets=RESETS_MV)
    s.bias = quiet_bias(s)
    s.brain.set_bias(s.bias[s.gid])
    return s


def stimulate(s: eyes.Setup, times: list[float], record: list[int], seed: int, tail: float = 0.005) -> np.ndarray:
    """From 1 s at rest, force both giant fibers to spike at `times` (s); the recorded neurons' spikes step by step
    from the first forced spike, (flies, steps, recorded)."""
    b, c = s.brain, relay.cells()
    gf = [c["gf"]["L"], c["gf"]["R"]]
    relay.rest(s, seed)
    at = sorted(set(int(round(t / b.dt)) for t in times))
    total = at[-1] + int(round(tail / b.dt)) + 1
    out = np.zeros((b.trials, total, len(record)), np.int8)
    k = 0
    for a in at + [total]:
        if a > k:
            _, out[:, k:a] = b.advance(a - k, record=record)
            k = a
        if a < total:
            b.u[:, gf] = relay.KICK
    return out


def answers(spikes: np.ndarray, at: list[int], window: int) -> tuple[np.ndarray, np.ndarray]:
    """For each stimulus step and fly and neuron: answered (bool) and latency in steps (nan if not)."""
    hit = np.zeros((len(at),) + spikes.shape[::2], bool)
    lat = np.full(hit.shape, np.nan)
    for q, a in enumerate(at):
        w = spikes[:, a + 1:a + 1 + window]                         # (flies, window, neurons)
        any_ = w.any(1)
        hit[q] = any_
        lat[q] = np.where(any_, w.argmax(1) + 1, np.nan)
    return hit, lat


def neurons() -> tuple[list[int], int, int]:
    c = relay.cells()
    record = [c["ttmn"]["L"], c["ttmn"]["R"], c["psi"]["L"], c["psi"]["R"]] + c["dlmn"]["L"] + c["dlmn"]["R"] + [c["gf"]["L"], c["gf"]["R"]]
    return record, 2, 4                                             # TTMn at 0-1, PSI at 2-3, DLMn from 4 to -2, GF last two


def part_a(s: eyes.Setup, seed: int) -> dict:
    record, _, _ = neurons()
    dt = s.brain.dt
    ttm, dlm = slice(0, 2), slice(4, len(record) - 2)
    out = {}
    times = [float(k) for k in range(50)]
    sp = stimulate(s, times, record, seed)
    at = [int(round(t / dt)) for t in times]
    h_t, l_t = answers(sp[:, :, ttm], at, TTMN_WINDOW)
    h_d, l_d = answers(sp[:, :, dlm], at, DLMN_WINDOW)
    lt, ld = D_GF + l_t * dt + D_TTM, D_GF + l_d * dt + D_DLM
    out["single"] = {"ttmn_answered": round(float(h_t.mean()), 4), "dlmn_answered": round(float(h_d.mean()), 4),
                     "ttm_latency_ms_median": None if np.isnan(lt).all() else round(float(np.nanmedian(lt)) * 1e3, 3),
                     "dlm_latency_ms_median": None if np.isnan(ld).all() else round(float(np.nanmedian(ld)) * 1e3, 3),
                     "ttm_latency_ms_counts": {str(round(v * 1e3, 1)): int(n) for v, n in zip(*np.unique(lt[~np.isnan(lt)], return_counts=True))},
                     "dlm_latency_ms_counts": {str(round(v * 1e3, 1)): int(n) for v, n in zip(*np.unique(ld[~np.isnan(ld)], return_counts=True))}}
    for hz in (100.0, 250.0):
        ht, hd = [], []
        for t in range(10):
            times = [k / hz for k in range(10)]
            sp = stimulate(s, times, record, seed + 100 + t + int(hz))
            at = [int(round(x / dt)) for x in times]
            ht.append(answers(sp[:, :, ttm], at, TTMN_WINDOW)[0].mean())
            hd.append(answers(sp[:, :, dlm], at, DLMN_WINDOW)[0].mean())
        out[f"train_{int(hz)}hz"] = {"ttmn_following": round(float(np.mean(ht)), 4), "dlmn_following": round(float(np.mean(hd)), 4)}
    twin = {}
    for gap_ms in (10, 8, 6, 4, 3, 2):
        second_t, second_d = [], []
        for rep in range(5):
            times = [0.0, gap_ms * 1e-3]
            sp = stimulate(s, times, record, seed + 500 + 10 * gap_ms + rep)
            at = [0, int(round(gap_ms * 1e-3 / dt))]
            second_t.append(answers(sp[:, :, ttm], at, TTMN_WINDOW)[0][1].mean())
            second_d.append(answers(sp[:, :, dlm], at, DLMN_WINDOW)[0][1].mean())
        twin[f"{gap_ms}ms"] = {"ttmn_second": round(float(np.mean(second_t)), 3), "dlmn_second": round(float(np.mean(second_d)), 3)}
    out["twin"] = twin
    return out


def quiet(s: eyes.Setup, seed: int, seconds: float = 100.0) -> dict:
    """Spikes of the TTMn and PSI at rest with no GF spike in the 5 ms before, per fly."""
    record, _, _ = neurons()
    b = s.brain
    relay.rest(s, seed)
    lone = np.zeros((b.trials, 2), int)
    chunk = int(round(1.0 / b.dt))
    carry = np.zeros((b.trials, 50), bool)                          # the previous chunk's last 5 ms of GF spikes
    for _ in range(int(seconds)):
        _, sp = b.advance(chunk, record=record)
        gf = np.concatenate([carry, sp[:, :, -2:].any(2)], 1)       # (flies, 50 + chunk)
        recent = np.zeros_like(gf)
        for d in range(1, 51):
            recent[:, d:] |= gf[:, :-d]
        recent = recent[:, 50:]
        for j, sl in ((0, slice(0, 2)), (1, slice(2, 4))):
            lone[:, j] += (sp[:, :, sl].any(2) & ~recent).sum(1)
        carry = gf[:, -50:]
    return {"ttmn_lone_spikes_per_fly": lone[:, 0].tolist(), "psi_lone_spikes_per_fly": lone[:, 1].tolist()}


def looms(s: eyes.Setup, seed: int) -> dict:
    """The fast loom on each side, LOOMS times per fly: per loom that fires the loomed side's GF, the delay from its
    first spike to that side's TTMn's first spike after it; and whether that TTMn fires in the last 0.5 s."""
    c = relay.cells()
    b, ol = s.brain, s.ol
    sc = scenes()
    per = int(round(eyes.OPTIC_DT / b.dt))
    out = {}
    for name, side in (("fastL", "L"), ("fastR", "R")):
        record = [c["gf"][side], c["ttmn"][side], c["ttmn"]["R" if side == "L" else "L"]]
        delays, late_fired, both = [], [], []
        for rep in range(LOOMS):
            b.reset(seed + rep + (0 if side == "L" else 1000))
            ol.reset()
            ol.gain = GAIN
            for _ in range(int(round(eyes.SETTLE / eyes.OPTIC_DT))):
                b.set_release(ol.neurons, 50.0 * ol.step(None))
                b.advance(per)
            steps = int(round(eyes.SCENE / eyes.OPTIC_DT))
            sp = np.zeros((b.trials, steps * per, 3), np.int8)
            for k in range(steps):
                b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(sc[name](k * eyes.OPTIC_DT))))
                _, sp[:, k * per:(k + 1) * per] = b.advance(per, record=record)
            late = int(round((eyes.SCENE - eyes.LATE) / b.dt))
            for f in range(b.trials):
                g = np.flatnonzero(sp[f, :, 0])
                late_fired.append(bool(sp[f, late:, 1].any()))
                both.append(bool(sp[f, late:, 1].any() and sp[f, late:, 2].any()))
                if len(g):
                    t = np.flatnonzero(sp[f, g[0] + 1:, 1])
                    delays.append(float((t[0] + 1) * b.dt) if len(t) else np.inf)
        d = np.array(delays)
        out[name] = {"gf_fired_looms": int(len(d)), "looms": int(LOOMS * b.trials),
                     "ttmn_within_0.5ms": round(float((d <= 0.5e-3 + 1e-9).mean()), 3) if len(d) else None,
                     "ttmn_not_within_2ms": round(float((d > 2e-3 + 1e-9).mean()), 3) if len(d) else None,
                     "ttmn_fired_late": round(float(np.mean(late_fired)), 3), "both_ttmn_late": round(float(np.mean(both)), 3),
                     "delay_ms_counts": {str(round(v * 1e3, 1)): int(n) for v, n in zip(*np.unique(d[np.isfinite(d)], return_counts=True))}}
    return out


def main() -> None:
    t0 = time.perf_counter()
    results = {"criteria": __doc__, "constants": {"sizes_mv": SIZES_MV, "psi_depression": PSI_DEPRESSION,
                                                  "delays_ms": [D_GF * 1e3, D_TTM * 1e3, D_DLM * 1e3]}}
    for condition in ("intact", "shakB"):
        s = build(condition)
        r = {"part_a": part_a(s, SEED), "looms": looms(s, SEED + 3000)}
        if condition == "intact":
            r["quiet"] = quiet(s, SEED + 7000)
        results[condition] = r
        print(condition, json.dumps(r), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    i, k = results["intact"], results["shakB"]
    si, sk = i["part_a"]["single"], k["part_a"]["single"]
    ld = (si["dlm_latency_ms_median"] or np.nan) - (si["ttm_latency_ms_median"] or np.nan)
    results["W1"] = bool(si["ttm_latency_ms_median"] is not None and 0.7 <= si["ttm_latency_ms_median"] <= 1.2
                         and si["dlm_latency_ms_median"] is not None and 1.3 <= si["dlm_latency_ms_median"] <= 1.7 and 0.24 <= ld <= 0.6)
    results["W2"] = bool(si["ttmn_answered"] >= 0.95 and si["dlmn_answered"] >= 0.90)
    t100, t250 = i["part_a"]["train_100hz"], i["part_a"]["train_250hz"]
    results["W3"] = bool(t100["ttmn_following"] >= 0.95 and t250["ttmn_following"] >= 0.80
                         and t100["dlmn_following"] >= 0.70 and t250["dlmn_following"] <= 0.60)
    results["W4"] = bool(max(i["quiet"]["ttmn_lone_spikes_per_fly"]) <= 1 and max(i["quiet"]["psi_lone_spikes_per_fly"]) <= 1)
    results["W5"] = bool(all(i["looms"][n]["ttmn_within_0.5ms"] is not None and i["looms"][n]["ttmn_within_0.5ms"] >= 0.95 for n in ("fastL", "fastR")))
    slower = sk["ttm_latency_ms_median"] is not None and si["ttm_latency_ms_median"] is not None and \
        sk["ttm_latency_ms_median"] - si["ttm_latency_ms_median"] >= 0.4
    results["S1"] = bool(sk["ttmn_answered"] <= 0.5 or slower)
    results["S2"] = bool(k["part_a"]["train_100hz"]["ttmn_following"] <= 0.30)
    results["S3"] = bool(sk["dlmn_answered"] <= 0.05)
    results["S4"] = bool(all(k["looms"][n]["ttmn_not_within_2ms"] is not None and k["looms"][n]["ttmn_not_within_2ms"] >= 0.8 for n in ("fastL", "fastR")))
    print({x: results[x] for x in ("W1", "W2", "W3", "W4", "W5", "S1", "S2", "S3", "S4")}, flush=True)
    OUT.write_text(json.dumps(results, indent=1))

    results["nulls"] = []
    for rw in (1, 2):
        n, _ = relay_null(rw)
        lv = looms(n, SEED + 4000 + 100 * rw)
        results["nulls"].append({"rewiring": rw, "looms": lv})
        print("null", rw, json.dumps(lv), flush=True)
        OUT.write_text(json.dumps(results, indent=1))
    results["NULL"] = bool(all(x["looms"][n]["ttmn_fired_late"] <= 0.5 * i["looms"][n]["ttmn_fired_late"]
                               for x in results["nulls"] for n in ("fastL", "fastR")))

    s = build("aged")
    results["aged"] = {"part_a": part_a(s, SEED + 9000)}
    tests = ("W1", "W2", "W3", "W4", "W5", "S1", "S2", "S3", "S4", "NULL")
    results["pass"] = bool(all(results[x] for x in tests))
    results["seconds"] = round(time.perf_counter() - t0)
    print(f"{'PASS' if results['pass'] else 'FAIL'}: " + " ".join(f"{x} {results[x]}" for x in tests), flush=True)
    OUT.write_text(json.dumps(results, indent=1))


def relay_null(rewiring: int) -> tuple[eyes.Setup, list]:
    """A rewired network with the relay: calibrated as taste_escape.py's nulls (from rest_calibration2.py's
    rewired biases, taste_escape's rounds), then its jump and flight motor neurons quieted as escape_relay.py does,
    each resetting 5 mV below its own new rest."""
    import rest_calibration2 as attempt2
    import taste_escape as te
    start = np.load(attempt2.HERE / f"rewired-{rewiring}.npz")["bias"]
    s = relay.setup(SIZES_MV, PSI_DEPRESSION, seed=50 + rewiring, bias=start, rewiring=rewiring, resets=RESETS_MV)
    relay.set_resets(s, {t: -5.0 for t in relay.ESCAPE})    # quieted as the intact brain was, at the usual reset
    eyes.ROUNDS = te.ROUNDS
    log = s.calibrate()
    relay.quiet(s, seed=3000 + 100 * rewiring)
    relay.set_resets(s, relay.resets_from(s))               # then its own lowered rest, as escape_relay.py's RESET
    return s, log


if __name__ == "__main__":
    main()
