"""Exploratory, not pre-registered: does the fitted head-direction ring keep its bump inside the whole resting
brain?

ring_fit.py (and ring_fit2.py, which also penalizes preferred places) fitted the ring's class gains,
slow current, depression and group biases in its 460-neuron sub-network, where ring neurons get only the
background. Here those settings go into escape_at_rest2.py's resting brain (which passed): the class
gains on every synapse between two of the 460 neurons, the excitatory ring edges through the slow
current, the depression on the ring's excitatory outputs. The ring can't be calibrated the way the rest
of the brain is (ring_calibrated.py: it's bistable), so its groups keep the fitted biases, each less
the mean input its neurons get from outside the ring at rest (each input's resting rate times its
weight, its depression's steady efficacy at that rate and the 5 ms synaptic time constant), and are
left out of the calibration. Procedure: the eyes-open start (escape_at_rest2.py's biases), the ring's
biases uncorrected, 8 fresh-start rounds of the usual calibration (k = 1 mV, then 0.5) for everything
else; then the correction from a 2-s resting run, and 4 more rounds (k = 0.5). Measured: rung 4's BUMP
over 8 runs of 60 s at grey (strength per bridge side, 1,000 shuffles, the resultant), the bump's
position entropy over the 16 wedges (as ring_fit2.py), width, the busiest wedge, the ring's group
rates, and the brain's own mean rate and neurons over 100 Hz.

With --homeostasis, each ring neuron also keeps its own bias from ring_homeostasis.py --slow (for that
fit), and the correction for outside input is made neuron by neuron rather than per group, so outside input
adds no new unevenness around the ring. Also measured then: the bump's drift (ring_drift.py's D, from
0.5-s windows).

--insitu N (with --homeostasis): the bump inside the whole brain favors half the ring (ring_fit3's run),
though outside input is corrected neuron by neuron, so loops through the rest of the brain carry where the
bump sits back to the ring. Homeostasis in a real brain runs in place, so this runs N more rounds of
ring_homeostasis.py's slow homeostasis inside the whole brain before measuring: 8 fresh runs of 30 s a
round (1 s settle), each ring neuron's offset moved by at most 0.3 mV toward its type's rate in the fit,
rates averaged over rounds (weight 0.3), the rest of the brain's biases unchanged. The offsets are saved
(experiments/ring_whole/<fit>_insitu.npz).

    python experiments/ring_whole.py --fit ring_fit3 --homeostasis   (writes experiments/ring_whole/<fit>[_homeostasis].json)
    python experiments/ring_whole.py --fit ring_fit3 --homeostasis --insitu 30   (writes .../<fit>_insitu.json)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import escape_at_rest as escape
import escape_at_rest2 as escape2
import eyes_at_rest as eyes
import rest_calibration as attempt1
import rest_calibration2 as attempt2
import ring_er
from brainfly.hybrid import TAU
from shiu_rewiring import W_SYN

HERE = Path(__file__).with_suffix("")
PEN = ["PEN_a(PEN1)", "PEN_b(PEN2)"]
SECONDS = 60


def ring_members(types: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    er = np.char.startswith(types, "ER") & np.array([t[2:3].isdigit() for t in types]) | np.char.startswith(types, "ExR")
    return np.isin(types, ring_er.RING) | er, er


def subnetwork(p: dict):
    """eyes_at_rest.SUBNETWORK for the fitted ring: class gains inside the ring, its slow edges split off."""
    def apply(M, types, superclass):
        ring, er = ring_members(types)
        M = M.tocoo()
        pre, post = M.col, M.row
        inside = ring[pre] & ring[post]
        tp, tq = types[pre], types[post]
        ring_exc = np.isin(types, ring_er.EXC)
        g = np.where(M.data > 0, p["gE"], p["gI"])
        g = g * np.where(((tp == "EPG") & np.isin(tq, PEN)) | (np.isin(tp, PEN) & (tq == "EPG")), p["loop"], 1.0)
        g = g * np.where((tp == "EPG") & (tq == "EPG"), p["epg_epg"], 1.0)
        g = g * np.where(tp == "Delta7", p["delta7"], 1.0)
        g = g * np.where(ring_exc[pre] & er[post], p["to_er"], 1.0)
        g = g * np.where(er[pre] & ~er[post], p["from_er"], 1.0)
        g = g * np.where(er[pre] & er[post], p["er_er"], 1.0)
        if p.get("wedge_norm", 0.0):
            epg, side, glom = attempt1.epgs(types)
            wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
            n_w = np.bincount(wedge, minlength=16)
            f = np.ones(len(types))
            f[epg] = (n_w.mean() / n_w[wedge]) ** p["wedge_norm"]
            g = g * f[pre]
        data = np.where(inside, M.data * g, M.data)
        slow_edge = inside & ring_exc[pre] & np.isin(tq, ring_er.RING) & (data > 0)
        slow = sparse.csr_matrix((data[slow_edge] * TAU / p["slow_tau"], (post[slow_edge], pre[slow_edge])), shape=M.shape)
        fast = sparse.csr_matrix((np.where(slow_edge, 0.0, data), (post, pre)), shape=M.shape)
        fast.eliminate_zeros()
        return fast, slow, p["slow_tau"]
    return apply


def model_with_ring(p: dict):
    def model(types, superclass):
        spec, sets = escape.model(types, superclass)
        for t in ring_er.EXC:
            spec[t] = {"depression": p["dep_f"], "recovery": p["dep_tau"]}
        return spec, sets
    return model


def group_of(types: np.ndarray) -> dict:
    ring, er = ring_members(types)
    return {"EPG": np.isin(types, ["EPG", "EPGt"]), "PEN_a": types == "PEN_a(PEN1)", "PEN_b": types == "PEN_b(PEN2)",
            "PEG": types == "PEG", "Delta7": types == "Delta7", "ER": er & ~np.char.startswith(types, "ExR"),
            "ExR": np.char.startswith(types, "ExR")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", default="ring_fit")
    ap.add_argument("--homeostasis", action="store_true")
    ap.add_argument("--insitu", type=int, default=0)
    args = ap.parse_args()
    fit_name, homeostasis, insitu = args.fit, args.homeostasis, args.insitu
    t0 = time.perf_counter()
    p = json.loads((Path(__file__).with_name(f"{fit_name}.json")).read_text())["best"]["params"]
    attempt2.model, attempt1.network = model_with_ring(p), escape2.network
    eyes.SUBNETWORK = subnetwork(p)
    s = eyes.Setup(None, seed=5)
    s.bias = np.load(escape2.HERE / "intact.npz")["bias"]
    b, types = s.brain, s.types
    ring, _ = ring_members(types)
    groups = group_of(types)
    ring_groups = np.unique(s.gid[ring])
    fitted = np.zeros(b.n)
    for g, m in groups.items():
        fitted[m] = p[f"b_{g}"]
    for k in ring_groups:
        s.bias[k] = fitted[s.gid == k].mean()
    extra = np.zeros(b.n)                     # per-neuron offsets on top of the group biases (the ring's only)
    if homeostasis:
        suffix = "" if fit_name == "ring_fit2" else f"_{fit_name}"
        for t, vals in json.loads(Path(__file__).with_name(f"ring_homeostasis_slow{suffix}.json").read_text())["extra_bias_mv"].items():
            extra[types == t] = vals
    homeo = extra.copy()
    group_bias = b.set_bias
    b.set_bias = lambda bias: group_bias(None if bias is None else np.asarray(bias) + extra)
    s.fixed |= ring
    eyes.ROUNDS = [1.0] * 4 + [0.5] * 4
    log = s.calibrate()

    # the ring's correction: mean input from outside the ring at rest
    b.reset(3)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(1.0 / b.dt)))
    rate = b.advance(int(round(2.0 / b.dt))).mean(0) / 2.0
    f = np.array([q["depression"] for q in b.params])[b.cls]
    tau = np.array([q["recovery"] for q in b.params])[b.cls]
    efficacy = 1.0 / (1.0 + (1.0 - f) * rate * tau)
    M = eyes.SUBNETWORK(escape2.network()[0], types, np.asarray(b.superclass))[0].tocsr()
    outside = np.where(ring, 0.0, rate * efficacy)
    ext = (M @ outside) * b.scale * W_SYN * TAU                       # mV of mean depolarization per neuron
    if homeostasis:
        extra[:] = np.where(ring, homeo - ext, 0.0)
    else:
        for k in ring_groups:
            s.bias[k] = fitted[s.gid == k].mean() - ext[s.gid == k].mean()
    eyes.ROUNDS = [0.5] * 4
    log += s.calibrate()
    insitu_log = []
    if insitu:
        fit_rates = json.loads((Path(__file__).with_name(f"{fit_name}.json")).read_text())["best"]["group_hz"]
        target = np.zeros(b.n)
        for g, m in groups.items():
            if g in fit_rates and g not in ("ER", "ExR"):
                target[m] = fit_rates[g]
        tune = ring & (target > 0)
        smooth = None
        for k in range(insitu):
            b.reset(500 + k)
            b.set_release(s.ol.neurons, s.silent)
            b.set_bias(s.bias[s.gid])
            b.advance(int(round(1.0 / b.dt)))
            r_k = b.advance(int(round(30.0 / b.dt))).mean(0) / 30.0
            smooth = r_k if smooth is None else 0.7 * smooth + 0.3 * r_k
            extra[:] = np.where(tune, extra + np.clip(0.3 * np.log((target + 0.5) / (smooth + 0.5)), -0.3, 0.3), extra)
            insitu_log.append({"round": k + 1, "epg_hz": round(float(r_k[epg_idx := attempt1.epgs(types)[0]].mean()), 2),
                               "epg_rate_cv": round(float(r_k[epg_idx].std() / max(r_k[epg_idx].mean(), 1e-9)), 3)})
            print(json.dumps(insitu_log[-1]), flush=True)
        HERE.mkdir(exist_ok=True)
        np.savez_compressed(HERE / f"{fit_name}_insitu.npz", extra=extra, group_bias=s.bias)

    # measure
    b.reset(11)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(2.0 / b.dt)))
    epg, side, glom = attempt1.epgs(types)
    half, total = [], np.zeros((eyes.TRIALS, b.n))
    for _ in range(2 * SECONDS):
        c = b.advance(int(round(0.5 / b.dt)))
        half.append(c[:, epg])
        total += c
    half = np.stack(half, 1)
    w = half.reshape(half.shape[0], SECONDS, 2, -1).sum(2)
    rate = total / SECONDS
    bump = attempt1.bump(w, side, glom, np.random.default_rng(7))
    wedge = np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)
    prof = np.stack([w[..., wedge == k].mean(-1) for k in range(16)], -1)
    z = prof @ np.exp(2j * np.pi * np.arange(16) / 16)
    seen = prof.sum(-1) > 0
    hist = np.bincount(np.round(np.angle(z[seen]) / (2 * np.pi / 16)).astype(int) % 16, minlength=16) / max(int(seen.sum()), 1)
    entropy = float(-(hist[hist > 0] * np.log(hist[hist > 0])).sum() / np.log(16))
    flat = prof.reshape(-1, 16)
    flat = flat[flat.max(1) > 0]
    aligned = np.array([np.roll(x, 8 - int(np.argmax(x))) for x in flat]).mean(0) if len(flat) else np.zeros(16)
    hp = np.stack([half[..., wedge == k].mean(-1) for k in range(16)], -1)
    theta = np.unwrap(np.angle(hp @ np.exp(2j * np.pi * np.arange(16) / 16)), axis=1)
    lags = np.arange(1, 41)
    msd = np.array([np.mean((theta[:, k:] - theta[:, :-k]) ** 2) for k in lags])
    drift = float(np.polyfit(lags * 0.5, msd, 1)[0] / 2)
    ok = all(bump[x]["strength"] >= attempt1.MIN_BUMP and bump[x]["strength"] > bump[x]["shuffle_p99"]
             and bump[x]["resultant"] < attempt1.MAX_RESULTANT for x in "LR")
    out = {"question": __doc__, "fit": fit_name, "params": p, "calibration": log[-1], "insitu": insitu_log, "BUMP": bool(ok), "bump": bump,
           "position_entropy": round(entropy, 3), "drift_D_rad2_per_s": round(drift, 3), "position_histogram": np.round(hist, 3).tolist(),
           "fwhm_deg": 22.5 * float((aligned >= aligned.max() / 2).sum()) if len(flat) else None,
           "busiest_wedge_hz": round(float(flat.max(1).mean()), 1) if len(flat) else 0.0, "epg_hz": round(float(rate[:, epg].mean()), 2),
           "ring_group_hz": {g: round(float(rate[:, m].mean()), 2) for g, m in groups.items()},
           "outside_input_mv": {g: round(float(ext[m].mean()), 2) for g, m in groups.items()},
           "own_mean_hz": round(float(rate[:, ~s.fixed].mean()), 3), "own_over_100hz": int((rate[:, ~s.fixed].mean(0) > 100).sum()),
           "seconds": round(time.perf_counter() - t0)}
    HERE.mkdir(exist_ok=True)
    tag = "_insitu" if insitu else "_homeostasis" if homeostasis else ""
    (HERE / f"{fit_name}{tag}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("question", "params")}), flush=True)


if __name__ == "__main__":
    main()
