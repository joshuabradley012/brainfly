"""Exploratory check, not pre-registered: how much do the odor measures depend on the transient every run starts in?

odor_offset_check.py: in the window where every run measures its rest and starts its odor (1-2 s after the reset),
the antennal lobe hasn't settled (odor_probe30.py's model: the GABAergic LNs about a quarter above their steady rate,
the PNs at half theirs); odor_probe43.py: the PNs rest at about 1 spike/s there against 2.9 after 4 s. Flies meet an
odor from a settled state.
Model: odor_probe41.py's kw08_kept (its cache).
Measured: everything odor_probe40.py measures, on odor_probe41.py's seeds for that condition (391000), with every
reset replaced by a warm one: the state of all 8 flies after 6 s of spontaneous activity from seed 440000 (taken once,
before the measures), restored with fresh random streams from the run's own seed; each run's own settling time is
kept. Compared with odor_probe41.py's measures of the same model on the same seeds.

Ran: from a settled state the LNs answer as flies' do almost exactly (21.8, 12.5, 8.5 and 6.5 spikes/s per cell to
2-heptanone in Nagel et al.'s bins, against 22, 13, 8 and 6; root mean square log ratio 0.05, against 0.22 from the
reset) and rest at 3.9 spikes/s (4.4), the PNs rest at 1.6-2.0 spikes/s in the odor runs (0.4-0.6), and the receptor
synapses meet the odor at 0.94-0.97 of their strength (0.68-0.72). But the odor responses barely change: 3-octanol's
PNs peak at 102 spikes/s at 50-100 ms (103) and fall to 0.37 of it at 0.40-0.45 s (0.35); the transform's Rmax is
79-184 (84-198) and sigma 21-34 (23-34); 1.0-6.4% of Kenyon cells respond (1.1-6.0%), the alpha/beta cells firing
1.1-1.9 spikes per response (1.1-2.0); MBON11 gains 11 spikes to 3-octanol (13). Fewer PNs pass Turner's criterion over
their higher rest (19-36%, against 29-43%). So the transient every run starts in inflates the LNs' odor response and
holds the PNs' rest down, but leaves the PNs' and Kenyon cells' odor responses nearly as they are. Starting runs from a
settled state is the better protocol, and could skip most of each run's settling time.

    python experiments/odor_warm_check.py      (writes experiments/odor_warm_check.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_probe24 as p24
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe41 as p41
from brainfly.hybrid import HybridBrain

OUT = Path(__file__).with_suffix(".json")
SEED, SETTLE_S, BASE = 440000, 6.0, 391000
STATE = ("u", "x", "s", "until", "ad", "pending", "fpending", "pending_slow", "touched", "n_touched", "graded_input",
         "slow_graded_input", "_external_release", "external_input", "release", "driven", "left", "last", "left_s",
         "last_s", "presynaptic_state", "t")


def snapshot(o, rec) -> dict:
    b = o.brain
    b.reset(SEED)
    b.set_release(o.s.ol.neurons, o.s.silent)
    b.advance(int(round(SETTLE_S / b.dt)), drive=p24.spontaneous(rec))
    return {k: (getattr(b, k).copy() if isinstance(getattr(b, k), np.ndarray) else getattr(b, k)) for k in STATE}


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe41_kw08_kept", p41.builder(p36.KW08_CHARGE, True), p40.prepare)
    warm = snapshot(o, rec)
    cold = HybridBrain.reset

    def warm_reset(self, seed: int = 0) -> None:
        cold(self, seed)
        for k, v in warm.items():
            now = getattr(self, k)
            if isinstance(v, np.ndarray) and isinstance(now, np.ndarray) and now.shape == v.shape:
                now[...] = v                         # in place, as reset itself clears _external_release
            else:
                setattr(self, k, v.copy() if isinstance(v, np.ndarray) else v)
        self.rng = np.random.SeedSequence(seed).generate_state(self.trials, dtype=np.uint64)
    HybridBrain.reset = warm_reset
    try:
        entry = {"ln_response": p40.ln_measure(o, rec, BASE)}
        lr = entry["ln_response"]
        print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_upns", "rms_log_error")}),
              json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]),
              flush=True)
        entry.update(p36.measure(o, rec, built, BASE))
    finally:
        HybridBrain.reset = cold
    out = {"question": __doc__, "warm_settle_s": SETTLE_S, "condition": entry, "seconds": round(time.perf_counter() - t0)}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
