"""Exploratory, not pre-registered: with the projection neurons resting at flies' measured rate instead of rung 4's
default, does weak input reach them as it does in flies?

odor_probe41.py: with the receptor synapse's slow component at Kazama & Wilson's unitary size and the PNs keeping their
synaptic current through their spikes, the antennal lobe opens and accommodates roughly as flies' does, but weak input
reaches the PNs at about half flies' strength: the transform's sigma is 23-34 spikes/s of receptor input (Olsen et al.
2010: 12-16; DM1 45), 5 spikes/s of receptor input gives DL5's PNs 15 spikes/s (Olsen et al.'s fit: 36), only 29-43% of
PNs respond to an odor by Turner's criterion (flies 59 +- 14%), and 4-methylcyclohexanol reaches a quarter as many
Kenyon cells as 3-octanol (flies 0.73-0.92). Its PNs rest at 1.9 spikes/s, polished toward rung 4's 3 for every PN type.
Flies' PNs rest at 4.6 +- 4.2 spikes/s (Turner et al. 2008, n = 37) and about 4.5 in Bhandawat et al. 2007's mean of
843 responses (research_notes/Rung 9 learning data/pn_ln_dynamics.md, kenyon_cell_odor_responses.md), nearer threshold.
Model: odor_probe41.py's kw08_kept (odor_probe42.py's build at s = 0.17, the slow component at 0.086 of the fast
charge, the uniglomerular PNs keeping their current), rebuilt with every uniglomerular PN's resting target at 4.6
spikes/s, in the group polish and in the PN polish alike. Cached as odor_probe43.
Measured as odor_probe42.py measures. Seeds 240000 for the build (as odor_probe42.py offsets them); 430000 for the
measures (odor_probe40.py's offsets).

Ran: a little. The polishes bring the PNs to 4.6-4.8 spikes/s in their own windows, with the inhibition off; once it
is fitted the PNs rest at 2.9 spikes/s after 4 s (1.9 at rung 4's target) and at about 1 in the window where the odor
runs start (0.4-0.6 before), the inhibition's fluctuations above its offset holding the receptor synapses at 0.94 of
their strength. Weak input then works a little better: the transform's sigma is 20-32 (23-34 at rung 4's target;
flies 12-16), DL5's PNs give 19 spikes/s to 5 spikes/s of receptor input (15; Olsen et al.'s fit 36) and 47 to 10 (39;
73), and Rmax is unchanged (86-200). The rest barely moves: 29-39% of PNs respond by Turner's criterion (29-43%),
1.2-6.2% of Kenyon cells respond (1.1-6.0%) with alpha/beta cells firing 1.2-2.2 spikes per response (1.1-2.0),
4-methylcyclohexanol reaches 0.25 as many Kenyon cells as 3-octanol (0.23), MBON11 gains 13 spikes to 3-octanol (13),
and 3-octanol's PNs peak at 105 spikes/s at 50-100 ms (103) and fall to 0.38 of it at 0.40-0.45 s (0.35). The PNs'
resting rate isn't what keeps weak input from reaching them.

    python experiments/odor_probe43.py         (writes experiments/odor_probe43.json)
"""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path

import brain_cache
import odor_probe21 as p21
import odor_probe27 as p27
import odor_probe36 as p36
import odor_probe40 as p40
import odor_probe41 as p41

OUT = Path(__file__).with_suffix(".json")
SEED = 430000
PN_REST_HZ = 4.6                                   # Turner et al. 2008 (n = 37)


def build() -> tuple:
    """odor_probe41.builder(KW08, kept) with the uniglomerular PNs' resting target at PN_REST_HZ."""
    plain, polish = p21.build, p27.pn_polish

    def resting_target(o):
        out = plain(o)
        o.s.target = o.s.target.copy()
        o.s.target[o.m["upn"]] = PN_REST_HZ
        out["upn_rest_target_hz"] = PN_REST_HZ
        return out
    p21.build = resting_target
    p27.pn_polish = functools.partial(polish, goal=PN_REST_HZ)
    try:
        return p41.builder(p36.KW08_CHARGE, True)()
    finally:
        p21.build, p27.pn_polish = plain, polish


def main() -> None:
    t0 = time.perf_counter()
    out = {"question": __doc__, "pn_rest_target_hz": PN_REST_HZ, "flies": json.loads(p40.OUT.read_text())["flies"]}
    o, rec, built = brain_cache.load("odor_probe43", build, p40.prepare)
    entry = {"build": {x: built[x] for x in ("build", "presynaptic", "rest_check") if x in built},
             "ln_response": p40.ln_measure(o, rec, SEED)}
    lr = entry["ln_response"]
    print("LNs", json.dumps({x: lr[x] for x in ("rest_hz_gaba_lns", "rest_hz_upns", "rms_log_error")}),
          json.dumps(lr["odors"]["2-heptanone"]["ln_hz_nagel_bins"]), "OCT PNs", json.dumps(lr["odors"]["3-octanol"]["oct_pn_hz_50ms"][:8]),
          flush=True)
    out["condition"] = entry
    OUT.write_text(json.dumps(out, indent=1))
    entry.update(p36.measure(o, rec, built, SEED))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
