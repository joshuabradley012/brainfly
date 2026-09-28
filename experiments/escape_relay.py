"""Exploratory, not pre-registered: the giant fiber's relay to the jump and flight motor neurons, and the constants
rung 6's test fixes before it runs.

Rung 6 (README): "giant fiber to jump muscle in 0.7-1.2 ms, slowing without the gap junctions as in shakB
mutants". research_notes/Embodied fly connectome simulation/escape_circuit.md collects the physiology and
proposes the test (its 1.1-1.4). The connectome has no electrical synapses, so the relay comes from the
literature:
- one-way spikelets from each giant fiber (DNp01) to its own side's TTMn (the jump motor neuron) and PSI: the
  rectifying ShakB junctions (Phelan et al. 2008), paired as King & Wyman (1980) found and as MaleCNS's
  chemical contacts agree. No depression: the TTM follows beyond 250 Hz.
- PSI -> DLMn (the flight power motor neurons) as a fast synapse: a jump of the DLMn's membrane 0.3 ms after
  each PSI spike (0.3-0.5 ms measured), depressing with PSI, onto every DLMn that MaleCNS's PSI makes at least 10
  synapses onto (each PSI reaches the 5 motor neurons of the opposite side's DLM). MaleCNS gives PSI no clear
  transmitter, so brainfly's network has no PSI synapses to replace.
- sizes by the notes' rule: 3x (TTMn) and 2.5x (PSI, DLMn) the target's distance from its median resting
  voltage to threshold (Augustin et al. 2019's model of the junction gives a safety factor of about 3).
This measures the constants in the brain that tastes and escapes (taste_escape.py's model and biases):
  1. QUIET: flies' jump and flight motor neurons are silent at rest (the TTM fires once, at takeoff), while
     the calibration holds them near 2 Hz. Only the TTMn, STTMm, PSI and DLMn groups' biases move: each group
     down by 2 mV after a round (8 flies x 10 s at rest) in which any of its neurons fired, until a round in
     which none does, and then every group down 4 mV more, since rung 6 asks for at most one spike per fly in
     100 s, far rarer than one silent round can show. (A first version stepped 0.5 mV, far too slowly: 3,123
     then 2,795 spikes a round.)
  2. VOLTAGE: each target's median membrane voltage over 8 flies x 20 s at rest (sampled every 5 ms), and from
     it the sizes.
  3. DEPRESSION: PSI's depression (f of its strength left after a spike, recovering with time constant tau)
     such that a second PSI spike 5.2 ms after a first just fires a DLMn at its median voltage (the DLM's
     twin-pulse refractory period; Engel & Wu 1996), and the DLMn follow 84% of the GF spikes in 10-spike trains
     at 100 Hz (Allen & Murphey 2007): f from the first condition for each tau on a grid, the tau whose following
     comes closest to 84%. Rung 6 tests following at 250 Hz, which this doesn't measure.
  RESET: every brainfly neuron resets 5 mV below rest after a spike (rest_calibration2.py), rest meaning the
     nominal one. Quieting lowers these motor neurons' rest by 30-55 mV, so that reset threw each spike's neuron back
     up near threshold: a first run of stage 3 found DLMn following 100% at 100 Hz for every tau. So the quieted types
     reset 5 mV below their own lowered rest (their group's bias - 5 mV), and stage 3 was rerun with that
     (python experiments/escape_relay.py --depression, which keeps stages 1 and 2's results).

    python experiments/escape_relay.py            (writes experiments/escape_relay.json and escape_relay/quiet.npz)
    python experiments/escape_relay.py --depression   (stage 3 again, keeping stages 1 and 2's results)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
import taste_escape as te
from brainfly.data import DATA
from brainfly.shiu import counts, mcns_types

OUT = Path(__file__).with_suffix(".json")
HERE = Path(__file__).with_suffix("")
ESCAPE = ["TTMn", "STTMm", "PSI", "DLMn a, b", "DLMn c-f"]
GF, TTMN, PSI = {"L": 10010, "R": 10001}, {"L": 804642, "R": 800146}, {"L": 802401, "R": 903327}
SAFETY = {"TTMn": 3.0, "PSI": 2.5, "DLMn": 2.5}
FAST_DELAY, MIN_SYNAPSES = 3e-4, 10
TWIN, FOLLOW_100 = 5.2e-3, 0.84
TAUS = [0.011, 0.013, 0.016, 0.02, 0.025, 0.032, 0.04]
KICK = 50.0                   # mV: a forced GF spike, as from electrodes in the brain
MARGIN = 4.0                  # mV more for the quieted groups, once a round is silent


def cells() -> dict:
    """The relay's neurons (indices): GF, TTMn and PSI by side, and each PSI's DLMn."""
    ids = np.load(DATA / "brain.npz")["ids"]
    at = lambda body: int(np.flatnonzero(ids == body)[0])
    C = counts().tocsc()
    types = mcns_types().astype(str)
    dlmn = np.flatnonzero(np.char.startswith(types, "DLMn"))
    out = {"gf": {s: at(b) for s, b in GF.items()}, "ttmn": {s: at(b) for s, b in TTMN.items()},
           "psi": {s: at(b) for s, b in PSI.items()}, "dlmn": {}}
    for s, p in out["psi"].items():
        col = np.abs(C[:, p].toarray().ravel())
        out["dlmn"][s] = [int(d) for d in dlmn if col[d] >= MIN_SYNAPSES]
    return out


def synapses(size: dict[int, float] | None):
    """eyes_at_rest.SYNAPSES for the relay, with `size` mV per target neuron; a target left out of `size` gets no
    relay synapse (None: none at all, the network alone)."""
    def build(M, types, side):
        if size is None:
            return M, None, None
        c = cells()
        g, f = [], []
        for s in "LR":
            g += [(c["ttmn"][s], c["gf"][s]), (c["psi"][s], c["gf"][s])]
            f += [(d, c["psi"][s]) for d in c["dlmn"][s]]
        matrix = lambda pairs: sparse.csr_matrix(([size[i] for i, _ in pairs], ([i for i, _ in pairs], [j for _, j in pairs])),
                                                 shape=M.shape)
        return M, matrix([p for p in g if p[0] in size]), matrix([p for p in f if p[0] in size])
    return build


def setup(size: dict[int, float] | None, psi_depression: tuple[float, float] | None, seed: int,
          bias: np.ndarray | None = None, rewiring: int | None = None, resets: dict[str, float] | None = None) -> eyes.Setup:
    """taste_escape.py's brain (model and targets), with the relay, PSI's depression and the quieted types' resets
    (mV, by type); biases from taste_escape/intact.npz unless given."""
    attempt1.network = escape2.network
    M, scale, labels, types, superclass = te.network_for(rewiring)
    te.use_route(te.sugar_route(M, scale, labels))
    route_model = attempt2.model

    def model(types, superclass):
        spec, sets = route_model(types, superclass)
        spec["PSI"] = {"depression": 1.0, "recovery": 1.0} if psi_depression is None else \
            {"depression": psi_depression[0], "recovery": psi_depression[1]}
        for t, r in (resets or {}).items():
            spec[t] = {**spec.get(t, {}), "reset": r}
        return spec, sets
    attempt2.model = model
    eyes.SYNAPSES = synapses(size)
    s = eyes.Setup(rewiring, seed=seed)
    s.bias = np.load(te.HERE / "intact.npz")["bias"] if bias is None else bias.copy()
    s.brain.set_bias(s.bias[s.gid])
    return s


def resets_from(s: eyes.Setup) -> dict[str, float]:
    """RESET: each quieted type resets 5 mV below its own rest, its group's bias."""
    return {t: round(float(s.bias[list(s.names).index(t)]) - 5.0, 2) for t in ESCAPE}


def set_resets(s: eyes.Setup, resets: dict[str, float]) -> None:
    """Change the quieted types' resets in place (each type a class of its own, as setup's resets make it)."""
    b = s.brain
    for t, r in resets.items():
        members = np.flatnonzero(s.types == t)
        k = int(b.cls[members[0]])
        assert set(np.flatnonzero(b.cls == k)) == set(members), f"{t} must have a class of its own"
        b.params[k] = {**b.params[k], "reset": r}
    b._tables_cache = None


def set_psi_depression(s: eyes.Setup, f: float, tau: float) -> None:
    """Change PSI's depression in place (its own class), without building the brain again."""
    b = s.brain
    psi = list(cells()["psi"].values())
    k = int(b.cls[psi[0]])
    assert set(np.flatnonzero(b.cls == k)) == set(psi), "PSI must have a class of its own (build it with its own depression)"
    b.params[k] = {**b.params[k], "depression": f, "recovery": tau}
    b._tables_cache = None


def quiet(s: eyes.Setup, seed: int, rounds: int = 30) -> list:
    """QUIET: each of the TTMn, STTMm, PSI and DLMn groups down by 2 mV after a round (8 flies x 10 s at rest) in
    which any of its neurons fired, until a round in which none does; then all of them 4 mV more (MARGIN).
    Changes s.bias; returns the log."""
    b = s.brain
    groups = np.unique(s.gid[np.isin(s.types, ESCAPE)])
    log = []
    for r in range(rounds):
        rest(s, seed + r)
        fired = b.advance(int(round(10.0 / b.dt))).sum(0)
        per_group = {int(g): int(fired[s.gid == g].sum()) for g in groups}
        log.append({"round": r + 1, "spikes": {str(s.names[g]): n for g, n in per_group.items()},
                    "bias": {str(s.names[g]): round(float(s.bias[g]), 2) for g in groups}})
        print(json.dumps(log[-1]), flush=True)
        if not any(per_group.values()):
            s.bias[groups] -= MARGIN
            break
        for g, n in per_group.items():
            if n:
                s.bias[g] -= 2.0
    return log


def rest(s: eyes.Setup, seed: int, settle: float = 1.0) -> None:
    """Fresh flies at grey (flyvis's neurons silent), `settle` s in."""
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(settle / b.dt)))


def stimulate(s: eyes.Setup, gf: list[int], times: list[float], record: list[int], seed: int, tail: float = 0.005) -> np.ndarray:
    """From rest (1 s to settle), force spikes in the `gf` neurons at `times` (s after settling), as electrodes
    in the brain do; each recorded neuron's spike steps relative to the first forced spike: (trials, steps, record),
    counts per step."""
    b = s.brain
    rest(s, seed, 1.0)
    at = sorted(set(int(round(t / b.dt)) for t in times))
    total = at[-1] + int(round(tail / b.dt)) + 1
    out = np.zeros((b.trials, total, len(record)), np.int8)
    k = 0
    for a in at + [total]:
        if a > k:
            _, out[:, k:a] = b.advance(a - k, record=record)     # the recorded neurons' spikes, step by step
            k = a
        if a < total:
            b.u[:, gf] = KICK
    return out


def follow(s: eyes.Setup, hz: float, trains: int, seed: int, record: list[int], window=(1, 12)) -> np.ndarray:
    """10-spike GF trains (both GFs) at `hz`, `trains` of them from fresh rests: the fraction of GF spikes each
    recorded neuron answers within `window` steps after it."""
    c = cells()
    gf = [c["gf"]["L"], c["gf"]["R"]]
    hit = np.zeros(len(record))
    n = 0
    for t in range(trains):
        times = [k / hz for k in range(10)]
        spikes = stimulate(s, gf, times, record, seed + t)
        for k in range(10):
            a = int(round(times[k] / s.brain.dt))
            hit += (spikes[:, a + window[0]:a + window[1]].sum(1) > 0).sum(0)
            n += spikes.shape[0]
    return hit / n


def main(depression_only: bool = False) -> None:
    t0 = time.perf_counter()
    HERE.mkdir(exist_ok=True)
    c = cells()
    if depression_only:                                   # stages 1 and 2 as saved
        out = json.loads(OUT.read_text())
        out["question"] = __doc__
        bias = np.load(HERE / "quiet.npz")["bias"]
        size = {int(k): v["size_mv"] for k, v in out["voltage"].items()}
        depression(out, size, bias, t0)
        return
    s = setup(None, None, seed=5)
    b, types = s.brain, s.types
    out = {"question": __doc__, "cells": c}

    # 1. QUIET
    out["quiet"] = quiet(s, 3000)
    np.savez_compressed(HERE / "quiet.npz", bias=s.bias, groups=s.names)

    # 2. VOLTAGE
    targets = [c["ttmn"]["L"], c["ttmn"]["R"], c["psi"]["L"], c["psi"]["R"]] + c["dlmn"]["L"] + c["dlmn"]["R"]
    rest(s, 3100, 1.0)
    samples = []
    for _ in range(int(round(20.0 / 0.005))):
        b.advance(50)
        samples.append(b.u[:, targets].copy())
    median = np.median(np.concatenate(samples), axis=0)
    theta = np.array([b.params[b.cls[i]]["threshold"] for i in targets])
    kind = ["TTMn"] * 2 + ["PSI"] * 2 + ["DLMn"] * (len(targets) - 4)
    size = {int(i): round(float(SAFETY[k] * (th - m)), 2) for i, k, th, m in zip(targets, kind, theta, median)}
    out["voltage"] = {str(int(i)): {"type": str(types[i]), "side": str(b.side[i]), "median_mv": round(float(m), 2),
                                    "threshold_mv": float(th), "size_mv": size[int(i)]}
                      for i, m, th in zip(targets, median, theta)}
    print(json.dumps(out["voltage"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))

    depression(out, size, s.bias, t0)


def depression(out: dict, size: dict, bias: np.ndarray, t0: float) -> None:
    """3. DEPRESSION, with the quieted types' resets (RESET)."""
    c = cells()
    groups = list(np.load(HERE / "quiet.npz")["groups"])
    out["resets_mv"] = resets = {t: round(float(bias[groups.index(t)]) - 5.0, 2) for t in ESCAPE}
    s = setup(size, (0.5, 0.02), seed=5, bias=bias, resets=resets)
    record = c["dlmn"]["L"] + c["dlmn"]["R"] + [c["ttmn"]["L"], c["ttmn"]["R"]]
    grid = []
    for tau in TAUS:
        f = 1.0 - 0.6 * np.exp(TWIN / tau)
        set_psi_depression(s, f, tau)
        fr = follow(s, 100.0, trains=10, seed=3200, record=record)
        grid.append({"tau_s": tau, "f": round(float(f), 4), "dlmn_following_100hz": round(float(fr[:-2].mean()), 3),
                     "ttmn_following_100hz": round(float(fr[-2:].mean()), 3)})
        print(json.dumps(grid[-1]), flush=True)
    best = min(grid, key=lambda g: abs(g["dlmn_following_100hz"] - FOLLOW_100))
    out["depression"] = {"grid": grid, "chosen": best}
    out["size_mv"] = size
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print("chosen:", json.dumps(best), flush=True)


if __name__ == "__main__":
    import sys
    main(depression_only="--depression" in sys.argv)
