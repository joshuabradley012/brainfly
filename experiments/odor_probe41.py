"""Exploratory, not pre-registered: on the antennal lobe rebuilt around local neurons that answer odors as flies' do, do
the receptor synapse's slow component at its unitary size and projection neurons that keep their synaptic current
through their spikes give flies' strong onset and accommodation?

odor_probe42.py: with the presynaptic inhibition fitted after the resting polishes (so that it acts only above the
finished model's resting rate) and every synapse onto the antennal lobe's LNs at 0.17 of its strength, the GABAergic
LNs answer 2-heptanone as flies' do (23, 16, 10 and 7.5 spikes/s per cell in Nagel et al.'s bins, against 22, 13, 8 and
6) from a rest of 3.8 spikes/s. But the projection neurons still climb through an odor: 3-octanol's fire 90 spikes/s at
50-100 ms, peak at 120 at 0.25-0.35 s and hold 0.93 of that at 0.5 s (flies' fall to 0.48), the inhibition, refitted to
Olsen & Wilson's late suppression, holding the receptor synapses at 0.34-0.41 of their strength from 100 ms on.
odor_probe36.py: the slow component carries the PNs' sustained drive; at Kazama & Wilson 2008's unitary size (0.086 of
the fast charge) the PNs accommodate as flies' do, but at half the rate, and the Kenyon cells fall silent. odor_probe32.py and odor_probe35.py: the spike rule from Shiu et al. (the synaptic current zeroed at each
spike, input dropped while refractory) throws away much of the charge of a neuron driven fast through synapses (40 mV
of synaptic drive gives 95 spikes/s, against 167 for a bias), which flies' neurons don't; the PNs fire at up to 100-300
spikes/s in odors.
Model: odor_probe42.py's at the scale whose LNs came closest to Nagel et al.'s PSTH there (0.17), rebuilt and refitted
for each condition exactly as odor_probe42.py builds it:
  kw08         the slow component at 0.086 of the fast charge (odor_probe36.py's KW08), the unitary EPSP's correction
               for it recomputed
  kw08_kept    the same, with every uniglomerular PN keeping its synaptic current through its spikes (keep_current)
               from the start of the build
  nagel_kept   the slow component at Nagel et al.'s 0.774 (the current model's), the PNs keeping their current
With odor_probe42.py's own model at 0.17 (Nagel's 0.774, the spike rule as Shiu et al.'s) these cross the two
changes. Each built model is cached (odor_probe41_kw08, odor_probe41_kw08_kept, odor_probe41_nagel_kept).
Measured as odor_probe42.py measures. Seeds 240000 for the builds (odor_probe30.py's, as odor_probe42.py offsets them);
390000 + 1000 x condition for the measures (odor_probe40.py's offsets).

Ran: the slow component's size sets whether the projection neurons accommodate and keeping their current sets how hard
they open; only the two together give flies' kind of response. In every condition the LNs still answer as flies' do
(root mean square log ratio 0.20-0.22) and the inhibition's fit is as before (k_A 0.0012, k_B 0.0061-0.0069; the
synapses resting at 0.94-0.99 of their strength, the PNs at 1.9-2.4 spikes/s). kw08: 3-octanol's PNs peak at once, at
56 spikes/s at 50-100 ms, and fall to 0.36 of that by 0.5 s and 0.25 by 0.95 s, but the transform's Rmax is 62-135
(flies 144-170) and the Kenyon cells nearly fall silent (0.05-0.4%), as in odor_probe36.py. kw08_kept: they peak at 103
at 50-100 ms (the strongly driven ones at 186) and fall to 0.35 of it at 0.40-0.45 s, 0.30 at 0.5 s and 0.20 at 0.95 s
(flies: about 0.48 at 0.43 s, 500 ms after the valve); they fire 101-122 spikes/s over the first 100 ms of each odor and
52-75 over the second; the transform's Rmax is 174-198 in DL5, VM7d and DM1 (flies 163-170) and 84 in DM4 (170), its
sigma 23-34 (12-16; DM1 45); 1.1-6.0% of Kenyon cells respond (flies 6 +- 5%), mean Jaccard 0.14, the responding
alpha/beta cells firing 1.1-2.0 spikes per response (flies 2.2) and 3.6 over 1.4 s to 3-octanol (11 with Nagel's
component); but alpha'/beta' cells respond no more than alpha/beta (5.2% and 5.9% to 3-octanol; flies 9-14% and 3-8%),
4-methylcyclohexanol reaches a quarter as many Kenyon cells as 3-octanol (1.1% against 4.7%; flies 0.73-0.92) though its
PNs answer as hard (122 spikes/s per PN over the first 100 ms, against 120), only 29-43% of PNs respond by Turner's
criterion (flies 59 +- 14%), and MBON11 gains 13 spikes to 3-octanol from 44 pC per cell (flies 118 from about 250).
nagel_kept: the PNs open hardest (117 spikes/s at 50-100 ms, the strongly driven ones at 217) but never accommodate (a
peak of 127 at 0.25 s, 0.94 of it at 0.5 s and 0.74 at 0.95 s); the transform's Rmax is 213-359 and sigma 19-30; the
Kenyon cells respond at 5.3-20% and fire 5.2-8.1 spikes per response (alpha/beta); MBON11 gains 203 spikes from 1094 pC.
So with the measured unitary slow component and the PNs keeping their current, the antennal lobe opens and accommodates
roughly as flies' does and the Kenyon cells fire as few spikes as flies'; what remains is weak input (the transform's
sigma, PN breadth, 4-methylcyclohexanol's reach), the alpha'/beta' cells and MBON11's input.

    python experiments/odor_probe41.py         (writes experiments/odor_probe41.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import brain_cache
import odor_probe17 as p17
import odor_probe21 as p21
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe42 as p42

OUT = Path(__file__).with_suffix(".json")
SEED = 390000
_p42 = json.loads(p42.OUT.read_text())
SCALE = float(min(_p42["conditions"], key=lambda s: _p42["conditions"][s]["ln_response"]["rms_log_error"]))
CONDITIONS = {"kw08": (p36.KW08_CHARGE, False), "kw08_kept": (p36.KW08_CHARGE, True), "nagel_kept": (p17.SLOW_CHARGE, True)}


def builder(slow: float, kept: bool):
    """odor_probe42.built_inhibition_last(SCALE) with the slow component at slow of the fast charge (and the unitary EPSP's correction
    for it recomputed, as odor_probe36.kw08_build sets it) and, if kept, the uniglomerular PNs keeping their synaptic
    current through their spikes from the start of the build (straight after odor_probe21.build)."""
    def build() -> tuple:
        charge, ratio, plain = p17.SLOW_CHARGE, p21.combined_peak_ratio, p21.build

        def keeping(o):
            out = plain(o)
            if kept:
                o.brain.set_type("uPN", keep_current=1.0)
            out["upn_keep_current"] = kept
            return out
        p17.SLOW_CHARGE = slow
        p21.combined_peak_ratio = functools.partial(ratio, charge=slow)
        p21.build = keeping
        try:
            return p42.built_inhibition_last(SCALE)()
        finally:
            p17.SLOW_CHARGE, p21.combined_peak_ratio, p21.build = charge, ratio, plain
    return build


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "ln_scale": SCALE, "flies": _p42["flies"], "conditions": {}}
    for c, (name, (slow, kept)) in enumerate(CONDITIONS.items()):
        o, rec, built = brain_cache.load(f"odor_probe41_{name}", builder(slow, kept), p40.prepare)
        base = SEED + 1000 * c
        entry = {"slow_over_fast_charge": round(slow, 4), "upn_keep_current": kept,
                 "build": {x: built[x] for x in ("build", "presynaptic", "rest_check") if x in built},
                 "ln_response": p40.ln_measure(o, rec, base)}
        lr = entry["ln_response"]
        print(name, "LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_upns", "rms_log_error")}),
              json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]),
              flush=True)
        out["conditions"][name] = entry
        OUT.write_text(json.dumps(out, indent=1))
        entry.update(p36.measure(o, rec, built, base))
        OUT.write_text(json.dumps(out, indent=1))
        print(name, f"done ({time.perf_counter() - t0:.0f} s)", flush=True)
        del o, rec
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
