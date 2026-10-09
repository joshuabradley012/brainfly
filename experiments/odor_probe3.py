"""Exploratory, not pre-registered: with the olfactory pathway's two measured numbers in place, do real odors reach the
Kenyon cells, and how sparsely?

odor_probe.py and odor_probe2.py found the brain that passed rung 4 deaf to odors: projection neurons saturate near
28 Hz whatever the receptor neurons' rate, and at most 1 of 4,064 Kenyon cells responds (flies: 5-10%). Two of the
pathway's numbers differ from measurements:
  - ORN to PN. A rested unitary connection gives a 6.19 +- 0.45 mV EPSP (Kazama & Wilson 2008; similar across
    glomeruli). Here its peak PSP is 0.1575 times the connection's weight (Shiu's 5 ms current into a 20 ms membrane),
    about 0.7 mV for the mean MaleCNS connection. With the measured depression on top (0.78 per spike, 0.9 s), a
    receptor neuron passes on at most about 5 spikes' worth a second however fast it fires, so a weight that small
    caps the projection neurons.
  - Kenyon cells at rest. Turner et al. 2008: 21.5 +- 5.6 mV below threshold. The rest calibration aimed them at 0 Hz,
    which doesn't constrain how far below threshold they sit, and left them about 27 mV below.
Changes, each alone and both:
  ORN   every ORN-to-uniglomerular-PN weight times one factor, so that the mean connection's rested peak PSP is
        6.19 mV;
  KC    each Kenyon cell type's bias moved so that its mean membrane potential over 1 s of rest (sampled every 10 ms,
        8 flies, 2 rounds) sits 21.5 mV below threshold.
The PN-to-KC synapses are left as they are. As a check against Gruntman & Turner 2013 (a KC needs about 4 of its 5-7
claws coactive to spike; with Turner's 21.5 mV that is roughly 5 mV per claw, the depolarization plateauing within
about 30 ms of >100 Hz PN input), the mean PN-to-KC connection's depolarization after 30 ms of 100 Hz from rest,
depression included, is reported.
Odors: DoOR odors as brainfly.odors makes them, every receptor neuron of each glomerulus at its response times 200 Hz,
for 1 s: 3-octanol and 4-methylcyclohexanol (aversive conditioning's pair), plus ethyl acetate, isopentyl (isoamyl) acetate,
benzaldehyde and 2-heptanone. Model and trial as odor_probe2.py (rung4_scaling.py's intact brain, 8 flies); seeds
9500 + 10 x condition + odor.
Measured: the driven projection neurons' (glomeruli above 0.2) rates over the first 100 ms and the whole second; the
Kenyon cells rising by more than 5 Hz, and by at least 1 spike in the second, as shares; pairwise overlap; APL;
MBON11, MBON01, MBON18; and at rest the Kenyon cells' rate (flies: about 0.1 Hz), the brain's mean rate and how many
neurons run over 100 Hz.

Ran: the projection neurons now answer like a fly's, and the Kenyon cells still don't. The ORN-to-PN factor is 8.8
(0.70 to 6.19 mV per connection). With it, the driven PNs fire 172-192 Hz in an odor's first 100 ms and 94-105 Hz
over the second (rung 4's brain: 69-87 and 21-28; flies: 100-200 at onset), and the brain still rests at 0.97 Hz
with no neuron over 100 Hz. Two rounds put every Kenyon cell type 21.4-21.6 mV below threshold (from 12-35). Yet with
both changes 2 Kenyon cells (0.05%) rise by 5 Hz for every odor, the same two each time, while 34-55% fire at least
one extra spike. The mean PN-to-KC connection gives 6.8 mV after 30 ms of 100 Hz (with the PNs' depression),
close to the 5 mV per claw Gruntman & Turner's numbers imply. APL reads 0 because it is graded and never spikes: this probe missed its
release (odor_probe4.py measures it).
Checked afterwards (odor_probe7.py): Kazama & Wilson's 6.19 mV is between an ORN and a PN of the same glomerulus, and
those connections are stronger than the average used here (a quarter of the ORN-to-PN connections join different
glomeruli, with about 2 synapses each), so the factor should be 7.3, not 8.8. The saved overlap ("overlap_jaccard") is
over the cells rising by 5 Hz only, and "kc_by_class" names several classes by types MaleCNS doesn't have (KCab,
KCapbp-*), so those fields read 0. And DoOR's responses here include each receptor's spontaneous level (DoOR's SFR row, 0-0.2 of its strongest
response), which brainfly.odors now subtracts, as DoOR's own reset_sfr does; so every glomerulus was driven harder
than its odor drives it, and receptors at or below their spontaneous rate were driven too (odor_probe7.py reruns
the current model without this).

    python experiments/odor_probe3.py          (writes experiments/odor_probe3.json)
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np

import rung4_scaling as r4s
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
ODORS = ("3-octanol", "4-methylcyclohexanol", "ethyl acetate", "isopentyl acetate", "benzaldehyde", "2-heptanone")
MAX_HZ, RISE = 200.0, 5.0
UNITARY_MV, KC_GAP_MV = 6.19, 21.5
PEAK = 0.1575                       # peak PSP per unit weight: 5 ms current into a 20 ms membrane
KC_CLASSES = ("KCg-m", "KCg-d", "KCab", "KCab-p", "KCapbp-m", "KCapbp-ap1", "KCapbp-ap2")
READ = {"MBON11": "MBON-γ1pedc>α/β", "MBON01": "MBON-γ5β'2a", "MBON18": "MBON-α2sc", "PPL101": "PPL1-γ1pedc", "APL": "APL"}
PN_SUFFIX = ("adPN", "lPN", "vPN", "ilPN", "lvPN")


def masks(types: np.ndarray) -> dict:
    return {"orn": np.char.startswith(types, "ORN_"), "kc": np.char.startswith(types, "KC"),
            "upn": np.array([bool(re.search(r"_[a-z]*PN$", t)) for t in types])}


def edges(b, pre_mask, post_mask) -> np.ndarray:
    pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
    return pre_mask[pre] & post_mask[b.idx]


def rest_state(s, seed: int, sample: bool) -> dict:
    """1 s to settle, then 1 s of rest: spike counts, and each neuron's mean membrane potential if `sample`."""
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    if not sample:
        return {"counts": b.advance(int(round(1.0 / b.dt)))}
    counts, u = np.zeros((b.trials, b.n)), np.zeros(b.n)
    for _ in range(100):
        counts += b.advance(int(round(0.01 / b.dt)))
        u += b.u.mean(0) / 100
    return {"counts": counts, "u": u}


def set_kc_rest(s, kc: np.ndarray, types: np.ndarray, bias: np.ndarray, seed: int) -> list:
    b, log = s.brain, []
    threshold = b.params[b.cls[np.flatnonzero(kc)[0]]]["threshold"]
    for r in range(2):
        u = rest_state(s, seed + r, True)["u"]
        row = {}
        for c in np.unique(types[kc]):
            m = types == c
            row[c] = round(float(threshold - u[m].mean()), 2)
            bias[m] += (threshold - KC_GAP_MV) - u[m].mean()
        b.set_bias(bias)
        log.append(row)
        print("KC gap to threshold before round", r + 1, json.dumps(row), flush=True)
    u = rest_state(s, seed + 2, True)["u"]
    log.append({c: round(float(threshold - u[types == c].mean()), 2) for c in np.unique(types[kc])})
    print("after", json.dumps(log[-1]), flush=True)
    return log


def claw_check(b, m: dict) -> float:
    """The mean PN-to-KC connection's depolarization after 30 ms of 100 Hz from rest (3 spikes, depression included),
    in a 20 ms membrane with the 5 ms current, mV."""
    w = float(b.weights[edges(b, m["upn"], m["kc"])].mean())
    f = b.params[b.cls[np.flatnonzero(m["upn"])[0]]]["depression"]
    t = np.arange(0, 0.0301, 1e-4)
    v = np.zeros_like(t)
    tau_s, tau_m = 0.005, 0.02
    for k, ts in enumerate((0.0, 0.01, 0.02)):
        dt_ = np.clip(t - ts, 0, None)
        v += (t >= ts) * w * f ** k * tau_s / (tau_s - tau_m) * (np.exp(-dt_ / tau_s) - np.exp(-dt_ / tau_m))
    return round(float(v.max()), 2)


def odor_trial(s, odor: str, seed: int) -> dict:
    b = s.brain
    b.reset(seed)
    b.set_release(s.ol.neurons, s.silent)
    b.advance(int(round(1.0 / b.dt)))
    rest = b.advance(int(round(1.0 / b.dt)))
    drive = odors.orn_drive(b, odor, MAX_HZ)
    onset = b.advance(int(round(0.1 / b.dt)), drive=drive)
    late = b.advance(int(round(0.9 / b.dt)), drive=drive)
    b.advance(int(round(1.0 / b.dt)))
    return {"rest": rest, "onset": onset, "odor": onset + late}


def condition(s, name: str, types: np.ndarray, m: dict, c: int) -> dict:
    b = s.brain
    kc = m["kc"]
    at_rest = rest_state(s, 9590 + c, False)["counts"].mean(0)
    out = {"rest": {"brain_hz": round(float(at_rest.mean()), 3), "over_100hz": int((at_rest > 100).sum()),
                    "kc_hz": round(float(at_rest[kc].mean()), 3), "upn_hz": round(float(at_rest[m["upn"]].mean()), 2)},
           "claw_30ms_mv": claw_check(b, m), "odors": {}}
    responders = {}
    for k, odor in enumerate(ODORS):
        r = odor_trial(s, odor, 9500 + 10 * c + k)
        rest, onset, odr = r["rest"].mean(0), r["onset"].mean(0) / 0.1, r["odor"].mean(0)
        gl = [g for g, v in odors.glomeruli(odor).items() if v > 0.2]
        pn = np.isin(types, [f"{g}_{x}" for g in gl for x in PN_SUFFIX])
        up = kc & (odr - rest > RISE)
        any_ = kc & ((r["odor"] - r["rest"] >= 1).mean(0) >= 0.5)          # at least 1 extra spike in half the flies
        responders[odor] = up
        out["odors"][odor] = {
            "pn_hz": {"rest": round(float(rest[pn].mean()), 2), "first_100ms": round(float(onset[pn].mean()), 1),
                      "second": round(float(odr[pn].mean()), 1), "count": int(pn.sum())},
            "kc_share": round(float(up.sum() / kc.sum()), 4), "kc_share_1spike": round(float(any_.sum() / kc.sum()), 4),
            "kc_by_class": {x: round(float((up & (types == x)).sum() / max((types == x).sum(), 1)), 4) for x in KC_CLASSES},
            "kc_responders_hz": round(float(odr[up].mean()), 1) if up.any() else None,
            "spikes_per_response": {x: round(float((r["odor"] - r["rest"]).mean(0)[any_ & np.char.startswith(types, x)].mean()), 2)
                                    if (any_ & np.char.startswith(types, x)).any() else None for x in ("KCab", "KCa'b'", "KCg")},
            "read": {x: [round(float(rest[types == x].mean()), 2), round(float(odr[types == x].mean()), 2)] for x in READ}}
        if "apl" in r:
            out["odors"][odor]["apl_release_hz"] = r["apl"]          # first 100 ms, whole second (odor_probe4.py)
        print(name, odor, json.dumps({k2: v for k2, v in out["odors"][odor].items() if k2 != "kc_by_class"}), flush=True)
    names = list(responders)
    out["overlap_jaccard"] = {f"{a} | {c2}": round(float((responders[a] & responders[c2]).sum() / max((responders[a] | responders[c2]).sum(), 1)), 3)
                              for i, a in enumerate(names) for c2 in names[i + 1:]}
    return out


def main() -> None:
    t0 = time.perf_counter()
    s = r4s.prepare("intact")[0]
    b = s.brain
    types = np.asarray(s.types).astype(str)
    m = masks(types)
    w0, bias0 = b.weights.copy(), s.bias[s.gid].astype(np.float64)
    orn_pn = edges(b, m["orn"], m["upn"])
    factor = UNITARY_MV / (PEAK * float(w0[orn_pn].mean()))
    out = {"question": __doc__, "orn_pn": {"connections": int(orn_pn.sum()), "mean_weight": round(float(w0[orn_pn].mean()), 3),
                                           "rested_peak_mv_before": round(PEAK * float(w0[orn_pn].mean()), 3),
                                           "factor": round(factor, 3)},
           "kc_total": int(m["kc"].sum()), "conditions": {}}
    print(json.dumps(out["orn_pn"]), flush=True)
    kc_bias = None
    for c, (name, orn, kcr) in enumerate((("rung 4 brain", False, False), ("ORN", True, False),
                                          ("KC", False, True), ("ORN + KC", True, True))):
        w = w0.copy()
        if orn:
            w[orn_pn] *= factor
        b.weights, b._external_matrix = w.astype(np.float32), None
        if kcr and kc_bias is None:
            bias = bias0.copy()
            b.set_bias(bias)
            out["kc_rest_calibration"] = set_kc_rest(s, m["kc"], types, bias, 9580)
            kc_bias = bias.copy()
        b.set_bias(kc_bias if kcr else bias0)
        out["conditions"][name] = condition(s, name, types, m, c)
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
