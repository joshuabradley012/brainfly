"""Exploratory analysis, not pre-registered: does a receptor neuron-to-PN synapse whose recovery from depression speeds up
with activity fit flies' measurements better than brainfly's two pools, and in particular both of Kazama & Wilson's
recoveries: about 0.4 s after a 50-200 Hz train, 7.5 s with no fast phase after 4 s at 7 Hz?

brainfly's receptor synapse depresses as two pools (research_notes/Rung 9 learning data/orn_pn_depression.md, M4: half
leaving 0.83 of itself per spike and recovering over 7.5 s, half leaving 0.67 and recovering over 0.3 s). It recovers
fast after any train, so after 7 Hz it predicts a fast phase flies' synapses don't show (0.65 at 2 s against 0.50), and at
4 Hz it keeps about half its strength where DM4's keep 0.28 (Kazama & Wilson 2009). The resting drive it gives the PNs is
about three times flies' (odor_probe58.py, odor_probe60.py), and odor_probe58.py found that with two fixed pools a
glomerulus with a high spontaneous rate loses both resting drive and response, which flies' DL5 doesn't. At many synapses
residual calcium speeds recovery (Dittman, Kreitzer & Regehr 2000): slow at a low rate, fast during a burst, which would
let a synapse rest deeply depressed and still transmit an odor.
Models, each fitted by least squares to all the data below at once (amplitudes as fractions, every dataset weighted
alike, by its mean squared error):
    M4         two pools with fixed recovery (w, f_a, tau_a, f_b, tau_b), brainfly's
    DKR        one pool, each spike leaving f of it; recovery at rate 1/tau_0 + (1/tau_min - 1/tau_0) C / (C + K), where C,
               residual calcium, rises 1 with each spike and decays over tau_c
    M4-DKR     M4 with the slow pool recovering as DKR's pool (its tau_0 the slow pool's)
Data (orn_pn_depression.md, sections 1-3; read off figures, so approximate): Kazama & Wilson 2008 Fig. 8D/E (VM2, 7 Hz from
rest, pulses 2-8 of both examples), Fig. 8F (15, 20 and 50 Hz test trains after 4 s at 7 Hz, relative to their first
pulse), Fig. S8B (after a 50-200 Hz train, here 0.5 s at 100 Hz after 4 s at 7 Hz, 7 Hz probes relative to their plateau),
Fig. S8D (after 4 s at 7 Hz, one pulse after a pause of 0.5-30 s, relative to rested); Kazama & Wilson 2009 Supp. Fig. 2a
(DM4, 4 Hz from rest over 3 s); Nagel, Hong & Wilson 2015 Fig. 1c (DM6/VM2, 10 Hz from rest, 20 pulses).
Reported for each model: its parameters, each dataset's RMS error, and what it predicts at rest (the strength left at 4
and 7 spikes/s, Poisson-free regular trains after 30 s) and during an odor (after 0.5 s at 100 spikes/s from 7 spikes/s).

Ran: no model fits clearly better, and none rests more depressed while transmitting more during a burst, which is what
calcium-dependent recovery was meant to offer. Mean squared errors over the eight datasets: brainfly's two pools 0.0192,
refitted 0.0126 (w 0.48; slow pool 0.85 and 9.5 s, fast 0.75 and 1.15 s), DKR 0.0121 (f 0.77; recovery from 5.9 s down to
1.3 s with calcium decaying over 66 ms), M4-DKR 0.0121. Calcium-dependent recovery fits the slow recovery after 7 Hz a
little better (RMS 0.05 against 0.065 refitted and 0.09 as brainfly has it) and DM4's 4 Hz train about as well (0.09-0.10
against 0.20 as brainfly has it), but every model keeps about the same ratio of what it transmits during 0.5 s at 100
spikes/s to what it transmits at rest at 7 (about 2.5), because flies' own trains depress to almost nothing at 50 Hz
(Fig. 8F; no model follows that, RMS 0.20-0.21) and recover only 0.4-1.3 s after one. The refitted pools rest deeper
(0.23 left at 7 spikes/s against brainfly's 0.38; 0.33 at 4, DM4's 0.28) but transmit less in a burst (0.04 against
0.07). pn_toy2.py shows what that costs a PN.

    python experiments/orn_pn_recovery_fit.py      (writes experiments/orn_pn_recovery_fit.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from numba import njit
from scipy.optimize import minimize

OUT = Path(__file__).with_suffix(".json")
DT = 1e-3

KW08_7HZ = np.array([[0.77, 0.63, 0.57, 0.58, 0.50, 0.48, 0.49], [0.75, 0.73, 0.62, 0.46, 0.60, 0.43, 0.58]]).mean(0)
KW08_TEST = {15.0: [0.904, 0.861, 0.770, 0.741, 0.720, 0.694, 0.661],
             20.0: [0.861, 0.782, 0.701, 0.469, 0.519, 0.446, 0.456, 0.420, 0.356],
             50.0: [0.774, 0.462, 0.300, 0.165, 0.029] + [0.006] * 19}
S8B_T = np.array([0, 0.14, 0.29, 0.43, 0.57, 0.71, 0.86, 1.0, 1.14, 1.29, 1.43, 1.57, 1.71, 1.86, 2.0])
S8B = np.array([0.24, 0.48, 0.76, 1.91, 2.41, 2.16, 2.40, 2.49, 2.36, 2.68, 2.20, 2.77, 2.50, 2.46, 2.64]) / 2.62
S8D_T = np.array([0.5, 1.0, 2.0, 5.0, 10.0, 30.0])
S8D = np.array([0.46, 0.56, 0.50, 0.69, 0.91, 1.00])
KW09_4HZ = np.array([100, 72.7, 56.5, 48.3, 46.2, 36.2, 39.7, 35.1, 38.3, 33.9, 31.5, 30.0, 27.7]) / 100
N15_10HZ = np.array([1.00, 0.82, 0.64, 0.53, 0.51, 0.44, 0.44, 0.41, 0.41, 0.38, 0.36, 0.34, 0.37, 0.34, 0.38, 0.35, 0.36,
                     0.30, 0.33, 0.34])


def train(rate: float, seconds: float, start: float = 0.0) -> np.ndarray:
    """Spike times of a regular train."""
    return start + np.arange(int(round(rate * seconds))) / rate


@njit(cache=True)
def _run(spikes, until, w, f_a, tau_a, f_b, tau_b, tau_min, tau_c, k, a, b, c, t):
    """Synapse.run's loop: 1 ms steps between events."""
    out = np.empty(len(spikes))
    db, dc = np.exp(-DT / tau_b), np.exp(-DT / tau_c)
    n = len(spikes)
    for i in range(n + 1):
        to = spikes[i] if i < n else until
        while t + DT <= to + 1e-9:
            rate_a = 1.0 / tau_a + (1.0 / tau_min - 1.0 / tau_a) * c / (c + k)
            a += (1.0 - a) * (1.0 - np.exp(-DT * rate_a))
            b = 1.0 - (1.0 - b) * db
            c *= dc
            t += DT
        if i < n:
            out[i] = w * a + (1.0 - w) * b
            a, b, c = f_a * a, f_b * b, c + 1.0
    return out, a, b, c, t


class Synapse:
    """Pools a (weight w) and b (1 - w); each spike transmits w a + (1 - w) b of the rested strength, then leaves f_a of
    a and f_b of b. Pool b recovers over tau_b. Pool a recovers at 1/tau_a + (1/tau_min - 1/tau_a) C / (C + K), C rising
    1 per spike and decaying over tau_c (no calcium dependence when tau_min = tau_a)."""

    def __init__(self, w, f_a, tau_a, f_b=1.0, tau_b=1.0, tau_min=None, tau_c=0.1, k=1.0):
        self.w, self.f_a, self.tau_a, self.f_b, self.tau_b = w, f_a, tau_a, f_b, tau_b
        self.tau_min = tau_a if tau_min is None else tau_min
        self.tau_c, self.k = tau_c, k

    def run(self, spikes, until: float, state=None):
        """Amplitudes at each spike (fractions of rested), and the state (a, b, c, t) at `until`."""
        a, b, c, t = (1.0, 1.0, 0.0, 0.0) if state is None else state
        out, a, b, c, t = _run(np.asarray(spikes, np.float64), float(until), self.w, self.f_a, self.tau_a, self.f_b, self.tau_b,
                               self.tau_min, self.tau_c, self.k, a, b, c, t)
        return out, (a, b, c, t)


def predictions(syn: Synapse) -> dict:
    """Every dataset's model counterpart."""
    p = {}
    p["kw08_7hz"] = syn.run(train(7, 8 / 7), 8 / 7)[0][1:8]
    _, cond = syn.run(train(7, 4.0), 4.0 + 1 / 7)       # 4 s at 7 Hz, then the next interval
    for rate, data in KW08_TEST.items():
        amp, _ = syn.run(train(rate, (len(data) + 1) / rate - 1e-9, cond[3]), cond[3] + (len(data) + 1) / rate + 0.1, cond)
        p[f"kw08_test_{rate:g}"] = amp[1:len(data) + 1] / amp[0]
    _, burst = syn.run(np.concatenate([train(7, 4.0), train(100, 0.5, 4.0 + 1 / 7)]), 4.0 + 1 / 7 + 0.5)
    probes = burst[3] + S8B_T
    amp, _ = syn.run(probes, probes[-1] + 0.1, burst)
    p["s8b"] = amp / amp[-4:].mean()
    rec = []
    for pause in S8D_T:
        amp, _ = syn.run(np.array([cond[3] + pause]), cond[3] + pause + 0.1, cond)
        rec.append(amp[0])
    p["s8d"] = np.array(rec)
    p["kw09_4hz"] = syn.run(train(4, 3.25), 3.25)[0][:13]
    p["n15_10hz"] = syn.run(train(10, 2.0), 2.0)[0][:20]
    return p


DATA = {"kw08_7hz": KW08_7HZ, **{f"kw08_test_{r:g}": np.array(v) for r, v in KW08_TEST.items()}, "s8b": S8B, "s8d": S8D,
        "kw09_4hz": KW09_4HZ, "n15_10hz": N15_10HZ}


def errors(syn: Synapse) -> dict:
    p = predictions(syn)
    return {k: float(np.sqrt(np.mean((p[k][:len(v)] - v) ** 2))) for k, v in DATA.items()}


def resting_and_odor(syn: Synapse) -> dict:
    """Strength left after 30 s of a regular train at 4 and 7 spikes/s, and after 0.5 s at 100 from 7."""
    out = {}
    for rate in (4.0, 7.0):
        amp, st = syn.run(train(rate, 30.0), 30.0)
        out[f"rest_{rate:g}hz"] = round(float(amp[-1]), 3)
    amp, st = syn.run(np.concatenate([train(7, 10.0), train(100, 0.5, 10.0)]), 10.5)
    out["odor_100hz_after_0.5s"] = round(float(amp[-1]), 3)
    out["odor_100hz_mean_first_0.5s"] = round(float(amp[-50:].mean()), 3)
    out["transmitted_rest_7hz"] = round(7 * out["rest_7hz"], 2)
    out["transmitted_odor_100hz"] = round(100 * out["odor_100hz_mean_first_0.5s"], 2)
    return out


MODELS = {
    "M4": (lambda x: Synapse(w=x[0], f_a=x[1], tau_a=x[2], f_b=x[3], tau_b=x[4]),
           [0.5, 0.83, 7.5, 0.67, 0.3], [(0.05, 0.95), (0.3, 0.99), (0.5, 30.0), (0.2, 0.99), (0.05, 3.0)]),
    "DKR": (lambda x: Synapse(w=1.0, f_a=x[0], tau_a=x[1], tau_min=x[2], tau_c=x[3], k=x[4]),
            [0.75, 7.5, 0.3, 0.2, 1.0], [(0.3, 0.99), (0.5, 30.0), (0.02, 3.0), (0.01, 2.0), (0.05, 20.0)]),
    "M4-DKR": (lambda x: Synapse(w=x[0], f_a=x[1], tau_a=x[2], f_b=x[3], tau_b=x[4], tau_min=x[5], tau_c=x[6], k=x[7]),
               [0.5, 0.83, 7.5, 0.67, 0.3, 0.3, 0.2, 1.0],
               [(0.05, 0.95), (0.3, 0.99), (0.5, 30.0), (0.2, 0.99), (0.05, 3.0), (0.02, 3.0), (0.01, 2.0), (0.05, 20.0)]),
}


def fit(name: str) -> dict:
    make, x0, bounds = MODELS[name]
    loss = lambda x: float(np.mean([e ** 2 for e in errors(make(x)).values()]))
    best = None
    for k, start in enumerate([x0] + [[lo + (hi - lo) * f for (lo, hi), f in zip(bounds, np.random.default_rng(k).random(len(bounds)))]
                                      for k in range(1, 4)]):
        r = minimize(loss, start, method="L-BFGS-B", bounds=bounds, options={"maxiter": 200})
        if best is None or r.fun < best.fun:
            best = r
    syn = make(best.x)
    return {"params": [round(float(v), 4) for v in best.x], "loss": round(float(best.fun), 5),
            "rms": {k: round(v, 3) for k, v in errors(syn).items()}, "predicted": {k: np.round(v, 3).tolist() for k, v in predictions(syn).items()},
            "rest_and_odor": resting_and_odor(syn)}


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "data": {k: v.tolist() for k, v in DATA.items()}, "models": {}}
    out["models"]["M4 as brainfly has it"] = {"params": MODELS["M4"][1],
                                              "rms": {k: round(v, 3) for k, v in errors(MODELS["M4"][0](MODELS["M4"][1])).items()},
                                              "rest_and_odor": resting_and_odor(MODELS["M4"][0](MODELS["M4"][1]))}
    print("M4 as brainfly has it", json.dumps(out["models"]["M4 as brainfly has it"]), flush=True)
    for name in MODELS:
        out["models"][name] = fit(name)
        m = out["models"][name]
        print(name, m["params"], "loss", m["loss"], json.dumps(m["rms"]), json.dumps(m["rest_and_odor"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
