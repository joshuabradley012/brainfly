"""Exploratory, not pre-registered: which class gains and biases give the head-direction ring a bump like a
fly's at rest?

ring_er.py's recipe (the ring with its ring neurons, a slow current on the ring's excitation, depression on
its excitatory outputs, gains of 3 and 1.5) holds a bump, but a narrow (45 deg), hot (busiest wedge 31 Hz,
EPGs 3.75 Hz on average) one that settles on the same few wedges. ring_calibrated.py found that rung 4's
rate calibration can't repair it, because the ring is bistable and the fit swings between a hot bump and
none. Every connectome-constrained compass model in research_notes/Rung 4 resting state data/
head_direction_models.md fitted gains per cell-type pair. This does the same in ring_er.py's 460-neuron
sub-network, with CMA-ES (Hansen 2016) over 18 parameters:
  gains        all excitatory, all inhibitory, the EPG-PEN loop (both ways), EPG to EPG, Delta7's outputs,
               ring-type excitatory cells onto ER and ExR, ER and ExR onto the ring's six types, ER and ExR
               onto each other
  depression   strength left per spike and recovery time on the ring's excitatory outputs
  slow current its time constant
  biases       one per group: EPG, PEN_a, PEN_b, PEG, Delta7, ER, ExR
The score adds penalties, each zero inside its range: a bump in every run (strength at least 0.5 in each
run and on each side) that clears the label shuffles' 99th percentile by 0.05; full width at half maximum
near 100 deg (flies: 80-120 deg in darkness); runs settling in different places (resultant under 0.45);
seeded bumps held within 45 deg after 6 s; resting rates in the measured ranges (EPG 0.5-2 Hz, the busiest
wedge at most 20 Hz, PEN_a 2-6 Hz, ER 2.5-8 Hz; PEN_b, PEG, Delta7 and ExR 0.5-20 Hz); nothing over 100 Hz.
Each evaluation runs 8 spontaneous runs of 20 s and 8 seeded ones (4 positions) of 6 s. 12 candidates a
generation, 100 generations, in parallel processes.

    python experiments/ring_fit.py            (writes experiments/ring_fit.json)
"""
from __future__ import annotations

import json
import os
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy import sparse

OUT = Path(__file__).with_suffix(".json")
PEN = ["PEN_a(PEN1)", "PEN_b(PEN2)"]
GROUPS = {"EPG": ["EPG", "EPGt"], "PEN_a": ["PEN_a(PEN1)"], "PEN_b": ["PEN_b(PEN2)"], "PEG": ["PEG"], "Delta7": ["Delta7"]}
# name: (low, high, log scale, start)
SPACE = {"gE": (0.5, 8, True, 3.0), "gI": (0.5, 8, True, 1.5), "loop": (0.25, 4, True, 1.0), "epg_epg": (0.25, 4, True, 1.0),
         "delta7": (0.1, 10, True, 1.0), "to_er": (0.25, 4, True, 1.0), "from_er": (0.25, 4, True, 1.0), "er_er": (0.1, 4, True, 1.0),
         "dep_f": (0.8, 0.98, False, 0.9), "dep_tau": (0.1, 1.0, True, 0.3), "slow_tau": (0.03, 0.3, True, 0.1),
         "b_EPG": (-10, 10, False, 0.0), "b_PEN_a": (-10, 10, False, 0.0), "b_PEN_b": (-10, 10, False, 0.0), "b_PEG": (-10, 10, False, 0.0),
         "b_Delta7": (-10, 10, False, 0.0), "b_ER": (-10, 10, False, 0.0), "b_ExR": (-10, 10, False, 0.0)}
NAMES = list(SPACE)
RUNS, SPONT, FREE, POSITIONS = 8, 20, 6, (0, 4, 8, 12)
LAMBDA, GENERATIONS, SIGMA0 = 12, 100, 0.2


def decode(u: np.ndarray) -> dict:
    """Parameters from a point in the unit cube (clipped to it)."""
    out = {}
    for x, name in zip(np.clip(u, 0, 1), NAMES):
        lo, hi, log, _ = SPACE[name]
        out[name] = float(np.exp(np.log(lo) + x * (np.log(hi) - np.log(lo)))) if log else float(lo + x * (hi - lo))
    return out


def encode(p: dict) -> np.ndarray:
    u = []
    for name in NAMES:
        lo, hi, log, _ = SPACE[name]
        u.append((np.log(p[name]) - np.log(lo)) / (np.log(hi) - np.log(lo)) if log else (p[name] - lo) / (hi - lo))
    return np.array(u)


class Ring:
    """ring_er.py's sub-network with per-class gains, depression, slow current and group biases."""

    def __init__(self, p: dict, trials: int, seed: int):
        import ring_er
        from brainfly.hybrid import TAU, HybridBrain
        from shiu_rewiring import W_SYN
        import rest_calibration as attempt1
        M, scale, labels, types, (epg, side, glom), ring_neurons = ring_er.whole()
        sel = np.flatnonzero(np.isin(types, ring_er.RING + ring_neurons))
        Ms = M[sel][:, sel].tocoo()
        t = types[sel]
        pre, post = t[Ms.col], t[Ms.row]
        er = np.isin(t, ring_neurons)
        ring_exc = np.isin(t, ring_er.EXC)
        data = np.where(Ms.data > 0, Ms.data * p["gE"], Ms.data * p["gI"])
        data *= np.where(((pre == "EPG") & np.isin(post, PEN)) | (np.isin(pre, PEN) & (post == "EPG")), p["loop"], 1.0)
        data *= np.where((pre == "EPG") & (post == "EPG"), p["epg_epg"], 1.0)
        data *= np.where(pre == "Delta7", p["delta7"], 1.0)
        data *= np.where(ring_exc[Ms.col] & er[Ms.row], p["to_er"], 1.0)
        data *= np.where(er[Ms.col] & ~er[Ms.row], p["from_er"], 1.0)
        data *= np.where(er[Ms.col] & er[Ms.row], p["er_er"], 1.0)
        if p.get("wedge_norm", 0.0):                 # synaptic scaling: each wedge's EPGs give the same total output
            at_sub = {g: k for k, g in enumerate(sel)}
            wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
            n_w = np.bincount(wedge, minlength=16)
            f = np.ones(len(sel))
            f[[at_sub[i] for i in epg]] = (n_w.mean() / n_w[wedge]) ** p["wedge_norm"]
            data *= f[Ms.col]
        m = ring_exc[Ms.col] & np.isin(post, ring_er.RING) & (data > 0)
        slow = sparse.csr_matrix((data[m] * TAU / p["slow_tau"], (Ms.row[m], Ms.col[m])), shape=(len(sel),) * 2)
        W = sparse.csr_matrix((np.where(m, 0.0, data), (Ms.row, Ms.col)), shape=(len(sel),) * 2)
        W.eliminate_zeros()
        spec = {"all": attempt1.BACKGROUND | {"bias": 0.0}} | {x: {"depression": p["dep_f"], "recovery": p["dep_tau"]} for x in ring_er.EXC}
        self.brain = HybridBrain(trials=trials, w_syn=W_SYN, matrix=W, slow=slow, tau_slow=p["slow_tau"], scale=scale[sel],
                                 labels={k: v[sel] for k, v in labels.items()}, seed=seed, types=spec)
        self.groups = {g: np.isin(t, v) for g, v in GROUPS.items()} | {"ER": np.char.startswith(t, "ER"), "ExR": np.char.startswith(t, "ExR")}
        self.bias = np.zeros(len(sel))
        for g, mask in self.groups.items():
            self.bias[mask] = p[f"b_{g}"]
        self.brain.set_bias(self.bias)
        at = {g: k for k, g in enumerate(sel)}
        self.epg, self.side, self.glom = np.array([at[i] for i in epg]), side, glom
        self.wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)


def strengths(w: np.ndarray, side: np.ndarray, glom: np.ndarray, labels: np.ndarray | None = None) -> np.ndarray:
    """Per run and side: mean over windows of the population vector's length over the total (runs x 2)."""
    labels = glom if labels is None else labels
    out = np.zeros((w.shape[0], 2))
    phase = np.exp(2j * np.pi * np.arange(8) / 8)
    for k, s in enumerate("LR"):
        mine = np.flatnonzero(side == s)
        per = np.stack([w[..., mine[labels[mine] == g + 1]].sum(-1) for g in range(8)], -1)
        tot = per.sum(-1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[:, k] = np.nan_to_num(np.nanmean(np.where(tot > 0, np.abs(per @ phase) / tot, np.nan), 1))
    return out


def band(x: float, lo: float, hi: float) -> float:
    x = max(x, 1e-3)
    return float(np.log(lo / x) ** 2 if x < lo else np.log(x / hi) ** 2 if x > hi else 0.0)


def evaluate(u: np.ndarray, detail: bool = False):
    p = decode(u)
    r = Ring(p, RUNS, seed=1)
    b = r.brain
    b.advance(int(round(1.0 / b.dt)))
    w, total = [], np.zeros((RUNS, b.n))
    for _ in range(SPONT):
        c = b.advance(int(round(1.0 / b.dt)))
        w.append(c[:, r.epg])
        total += c
    w = np.stack(w, 1)
    rate = total / SPONT
    group_hz = {g: float(rate[:, m].mean()) for g, m in r.groups.items()}
    epg_hz = float(rate[:, r.epg].mean())
    per_run = strengths(w, r.side, r.glom)
    rng = np.random.default_rng(7)
    shuffles = []
    for _ in range(200):
        lab = r.glom.copy()
        for s in "LR":
            mine = np.flatnonzero(r.side == s)
            lab[mine] = rng.permutation(lab[mine])
        shuffles.append(strengths(w, r.side, r.glom, lab).mean(0))
    p99 = np.percentile(np.array(shuffles), 99, axis=0)
    strength = per_run.mean(0)
    phase = np.exp(2j * np.pi * np.arange(8) / 8)
    resultant = []
    for s in "LR":
        mine = np.flatnonzero(r.side == s)
        per = np.stack([w[..., mine[r.glom[mine] == g + 1]].sum(-1) for g in range(8)], -1)
        pos = np.angle((per @ phase).sum(1))
        resultant.append(float(np.abs(np.exp(1j * pos).mean())))
    prof = np.stack([w[..., r.wedge == k].mean(-1) for k in range(16)], -1).reshape(-1, 16)
    prof = prof[prof.max(1) > 0]
    if len(prof):
        aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in prof]).mean(0)
        fwhm = 22.5 * float((aligned >= aligned.max() / 2).sum())
        busiest = float(prof.max(1).mean())
    else:
        fwhm, busiest = 360.0, 0.0
    held = []
    for k, start in enumerate(POSITIONS):
        s = Ring(p, 2, seed=10 + k)
        bb = s.brain
        bb.advance(int(round(1.0 / bb.dt)))
        kick = s.bias.copy()
        kick[s.epg[np.isin(s.wedge, [(start + d) % 16 for d in (-1, 0, 1)])]] += 10.0
        bb.set_bias(kick)
        bb.advance(int(round(0.3 / bb.dt)))
        bb.set_bias(s.bias)
        bb.advance(int(round((FREE - 1) / bb.dt)))
        c = bb.advance(int(round(1.0 / bb.dt)))[:, s.epg]
        z = np.stack([c[:, s.wedge == q].mean(-1) for q in range(16)], -1) @ np.exp(2j * np.pi * np.arange(16) / 16)
        held += (np.degrees(np.abs(np.angle(z * np.exp(-2j * np.pi * start / 16)))) < 45).tolist()
    score = (4 * float(np.maximum(0, 0.5 - per_run).mean()) + 2 * float(np.maximum(0, p99 + 0.05 - strength).sum())
             + ((fwhm - 100) / 45) ** 2 + 2 * sum(max(0.0, x - 0.45) for x in resultant) + 2 * (1 - float(np.mean(held)))
             + 4 * band(epg_hz, 0.5, 2) + band(busiest, 1e-3, 20) + band(group_hz["PEN_a"], 2, 6) + 0.5 * band(group_hz["ER"], 2.5, 8)
             + 0.5 * sum(band(group_hz[g], 0.5, 20) for g in ("PEN_b", "PEG", "Delta7")) + 0.25 * band(group_hz["ExR"], 0.5, 20)
             + (10.0 if max(group_hz.values()) > 100 else 0.0))
    if not detail:
        return float(score)
    return {"score": round(float(score), 3), "params": {k: round(v, 4) for k, v in p.items()},
            "strength": np.round(strength, 3).tolist(), "shuffle_p99": np.round(p99, 3).tolist(),
            "weakest_run": np.round(per_run.min(0), 3).tolist(), "resultant": np.round(resultant, 3).tolist(),
            "fwhm_deg": fwhm, "busiest_wedge_hz": round(busiest, 1), "epg_hz": round(epg_hz, 2),
            "group_hz": {g: round(v, 2) for g, v in group_hz.items()}, "held": f"{int(np.sum(held))}/{len(held)}"}


def _init():
    os.environ.setdefault("NUMBA_NUM_THREADS", "1")


def cma_es(f, x0: np.ndarray, sigma: float, lam: int, generations: int, pool, log):
    """(mu/mu_w, lambda)-CMA-ES as in Hansen's tutorial (arXiv:1604.00772)."""
    n = len(x0)
    mu = lam // 2
    w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
    w /= w.sum()
    mueff = 1 / np.sum(w ** 2)
    cc, cs = (4 + mueff / n) / (n + 4 + 2 * mueff / n), (mueff + 2) / (n + mueff + 5)
    c1 = 2 / ((n + 1.3) ** 2 + mueff)
    cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff))
    damps = 1 + 2 * max(0, np.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chin = np.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n ** 2))
    m, C, pc, ps = x0.copy(), np.eye(n), np.zeros(n), np.zeros(n)
    B, D = np.eye(n), np.ones(n)
    rng = np.random.default_rng(0)
    best = (np.inf, x0)
    for g in range(generations):
        y = rng.standard_normal((lam, n)) @ (B * D).T
        x = m + sigma * y
        fx = np.array(pool.map(f, list(x))) + 10 * np.sum(np.clip(x - 1, 0, None) ** 2 + np.clip(-x, 0, None) ** 2, 1)
        order = np.argsort(fx)
        if fx[order[0]] < best[0]:
            best = (float(fx[order[0]]), x[order[0]].copy())
        yw = w @ y[order[:mu]]
        m = m + sigma * yw
        inv_sqrt = B @ np.diag(1 / D) @ B.T
        ps = (1 - cs) * ps + np.sqrt(cs * (2 - cs) * mueff) * inv_sqrt @ yw
        hsig = np.linalg.norm(ps) / np.sqrt(1 - (1 - cs) ** (2 * (g + 1))) / chin < 1.4 + 2 / (n + 1)
        pc = (1 - cc) * pc + hsig * np.sqrt(cc * (2 - cc) * mueff) * yw
        ys = y[order[:mu]]
        C = ((1 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + (1 - hsig) * cc * (2 - cc) * C)
             + cmu * (ys.T * w) @ ys)
        sigma *= np.exp((cs / damps) * (np.linalg.norm(ps) / chin - 1))
        C = np.triu(C) + np.triu(C, 1).T
        D2, B = np.linalg.eigh(C)
        D = np.sqrt(np.maximum(D2, 1e-20))
        log({"generation": g + 1, "best": round(best[0], 3), "generation_best": round(float(fx[order[0]]), 3),
             "median": round(float(np.median(fx)), 3), "sigma": round(float(sigma), 4)})
    return best, m


def main() -> None:
    t0 = time.perf_counter()
    x0 = encode({k: v[3] for k, v in SPACE.items()})
    out = {"question": __doc__, "start": evaluate(x0, detail=True), "log": []}
    print("start:", json.dumps(out["start"]), flush=True)

    def log(row):
        out["log"].append(row)
        print(json.dumps(row), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    with Pool(LAMBDA, initializer=_init) as pool:
        (score, x), mean = cma_es(evaluate, x0, SIGMA0, LAMBDA, GENERATIONS, pool, log)
    out["best"] = evaluate(x, detail=True)
    out["mean"] = evaluate(mean, detail=True)
    out["seconds"] = round(time.perf_counter() - t0)
    print("best:", json.dumps(out["best"]), "\nmean:", json.dumps(out["mean"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
