"""Exploratory, not pre-registered: APL's inhibition with its measured slow (GABA_B) part. Does lasting inhibition make
the Kenyon cells sparser, and does APL then matter as much as a fly's?

odor_probe8.py: silencing the model's APL makes 1.4-1.6 times as many Kenyon cells respond, where blocking flies' APL
lowers their population sparseness as much as about four times as many active cells would (Lin et al. 2014; derived,
research_notes/Rung 9 learning data/kc_classes_and_apl.md).
The model's APL inhibits Kenyon cells through the fast current only. Its peak, about 11 mV during an odor's onset,
matches the measured saturation (10-12 mV, Inada et al. 2017), but it fades within about 100 ms, as the Kenyon cells
fall quiet. Flies' lasts: in vivo it peaks within about 0.2 s and recovers over about a second (Vrontou et al. 2021),
and lateral inhibition follows excitation "by several hundred ms" (Inada). Inada's pharmacology splits it: picrotoxin
(GABA_A) leaves about 0.6 of it and adding CGP54626 (GABA_B) about 0.25, so GABA_A carries about 40% and GABA_B about
35%.
Model: odor_probe7.py's current model, with each APL-to-KC synapse split in those proportions (the unblocked quarter
shared between them): 53% of its weight stays on the fast current and the rest goes to the slow current, scaled by
5 ms / 0.5 s so that sustained release holds the Kenyon cell at the same depolarization as before. The slow current's
time constant is the one the brain already has (0.5 s, the head-direction ring's); no fly measurement sets GABA_B's
here. (HybridBrain now passes graded release along slow synapses.)
Conditions:
  current                 odor_probe7.py's current model
  APL silenced            the same with APL silenced throughout (as odor_probe8.py)
  GABA_B                  APL's inhibition split as above
  GABA_B + Inada classes  plus the Kenyon cell classes' threshold offsets from Inada et al. 2017 (odor_probe8.py:
                          alpha'/beta' 5.5 mV nearer threshold than alpha/beta, gamma 2.5 mV farther, mean 21.5 mV)
Odors, flies and measures as odor_probe7.py; seeds 30000 + 100 x condition + odor (Turner's protocol), + 50 + odor
(Hige's), + 90 (Kenyon cells' rest), + 80 (their class offsets), + 95 (the resting brain). The four-fold comparison
is loose: Lin et al. measured somatic calcium over 5 s pulses of ethyl acetate, this the share of Kenyon cells
responding by Turner's criterion over 2 s from a 0.5 s pulse. (Lin et al.'s sparseness came from somatic calcium
over a 7-odor panel; their lobe imaging used 5 s pulses of ethyl acetate.)

Ran (after the second review: DoOR's spontaneous level subtracted, and the ring's offsets, which an earlier run added
twice in the GABA_B conditions and three times in the last, added once; the first run is in git history): lasting
inhibition doesn't make the Kenyon cells sparser. Over the six odors:
  current                 6.6-19.4% respond (MCH 6.6%, OCT 16.3%); MBON11 0.8-5.3 spikes
  APL silenced            9.7-31.9%, 1.4-1.6 times the current model's for each odor
  GABA_B                  7.7-20.5%, 1.00-1.16 times the current model's; spikes per response about as before (alpha/beta
                          1.6-3.7, alpha'/beta' 0.9-1.3, gamma 1.5-2.2); MBON11 2.1-5.2
  GABA_B + Inada classes  7.3-20.3%; by class alpha/beta 7-26%, alpha'/beta' 8-20%, gamma 8-16%; alpha'/beta' fire
                          1.2-2.1 spikes per response; MBON11 1.0-4.9
The resting brain stays at 0.97-0.98 Hz with no neuron over 100 Hz. Moving 47% of APL's weight to the slow current
weakens its fast inhibition while the slow part builds up too late to stop the Kenyon cells that fire at the odor's
onset, and those are most of the responses. Flies' APL can't stop them either (its inhibition lags excitation by
hundreds of ms).

    python experiments/odor_probe9.py          (writes experiments/odor_probe9.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import sparse

import odor_probe7 as p7
import odor_probe8 as p8
from brainfly.shiu import TAU

OUT = Path(__file__).with_suffix(".json")
GABA_B = 0.35 / 0.75
CONDITIONS = {"current": {}, "APL silenced": {"silence_apl": True}, "GABA_B": {"gaba_b": True},
              "GABA_B + Inada classes": {"gaba_b": True, "offsets": "Inada"}}


class Inhibition:
    """Switches APL's inhibition of Kenyon cells between fast only and split fast/slow, on an Olfaction brain."""

    def __init__(self, o: p7.Olfaction):
        b = self.brain = o.brain
        self.apl = b.cells(["APL"])
        pre = np.repeat(np.arange(b.n), np.diff(b.ptr))
        self.edges = np.flatnonzero(np.isin(pre, self.apl) & o.m["kc"][b.idx])
        self.slow0 = sparse.csc_matrix((b._slow_counts, b.sidx, b.sptr), shape=(b.n, b.n))
        add = sparse.csc_matrix((b._counts[self.edges] * GABA_B * TAU / b.tau_slow, (b.idx[self.edges], pre[self.edges])),
                                shape=(b.n, b.n))
        self.slow_split = (self.slow0 + add).tocsc()
        w_expected = b._counts[self.edges] * b.w_syn * b.scale[b.idx[self.edges]]
        assert np.allclose(o.w0[self.edges], w_expected, rtol=1e-4), "APL's weights aren't counts x w_syn x scale"

    def set(self, split: bool) -> None:
        """Call after Olfaction.set (which restores the fast weights)."""
        b = self.brain
        if split:
            w = b.weights.copy()
            w[self.edges] *= 1 - GABA_B
            b.weights, b._external_matrix = w, None
        b.set_slow(self.slow_split if split else self.slow0)


def condition(o: p7.Olfaction, inh: Inhibition, name: str, c: int) -> dict:
    spec = CONDITIONS[name]
    base = 30000 + 100 * c
    out = {"kc_rest_calibration": o.set(p7.CURRENT, base + 90)}
    inh.set(spec.get("gaba_b", False))
    if spec.get("gaba_b"):
        out["kc_rest_after_split"] = p8.set_rest(o, {t: 21.5 for t in np.unique(o.types[o.m["kc"]])}, base + 70)[-1]
    if "offsets" in spec:
        gaps = p8.class_gaps(o, p8.OFFSETS[spec["offsets"]])
        out["gaps_mv"] = {t: round(g, 2) for t, g in gaps.items()}
        out["kc_rest_by_class"] = p8.set_rest(o, gaps, base + 80)[-1]
    silence = inh.apl if spec.get("silence_apl") else ()
    out["rest"] = p7.rest_measures(o, base + 95, silence)
    out["odors"], responders = {}, {}
    for k, odor in enumerate(p7.ODORS):
        row, responders[odor] = p7.measure_odor(o, odor, base + k, base + 50 + k, silence)
        out["odors"][odor] = row
        print(name, "|", odor, json.dumps({x: row[x] for x in ("kc_share", "kc_share_by_class", "spikes_per_response", "evoked_spikes_0_1.4s")}), flush=True)
    out["overlap_jaccard"] = p7.overlaps(responders)
    return out


def main() -> None:
    t0 = time.perf_counter()
    o = p7.Olfaction()
    inh = Inhibition(o)
    out = {"question": __doc__, "flies": p7.FLIES, "gaba_b_share": round(GABA_B, 3), "tau_slow_s": o.brain.tau_slow,
           "apl_kc_synapses": int(len(inh.edges)), "conditions": {}}
    for c, name in enumerate(CONDITIONS):
        out["conditions"][name] = condition(o, inh, name, c)
        print(name, json.dumps(out["conditions"][name]["rest"]), flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    inh.set(False)
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
