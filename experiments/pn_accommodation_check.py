"""Analysis of a saved recording, not a simulation: do the model's projection neurons accommodate during an odor as
flies' do, or does their decline explain the Kenyon cells'?

mbon11_burst_check.py: as in the learning test, the Kenyon cells fire from 0.5 to 1 s at 0.18 (alpha/beta), 0.25
(alpha'/beta') and 0.05 (gamma) of their rate in the first 0.3 s, and silencing APL barely changes that (0.24, 0.35 and
0.09), so most of the decline isn't APL's; with the slow Kenyon cell current (learning_pilot12.py) it is what still holds
MBON11's plateau at 51 spikes/s against flies' 95-100. Flies' projection neurons accommodate too: averaged over 843
responses they peak at about 88 spikes/s 140-150 ms after the valve and keep 0.48 of the peak at 500 ms, strong responses
0.43-0.48 (Bhandawat et al. 2007, Fig. 1b; research_notes/Rung 9 learning data/pn_ln_dynamics.md).
Input: olfaction_movie.py's recording (the current model's antennal lobe, one trial of 8 flies per odor, the projection
neurons' rate per glomerulus in 10 ms bins), in Bhandawat et al.'s 50 ms bins.
Measured, for each odor's responding glomeruli (more than 20 spikes/s above rest at their peak in the first 0.4 s): the
rate at 0.5 s over the peak, glomerulus by glomerulus and for their mean, and when they peak.

Ran (2026-10-11): the projection neurons accommodate as flies' do, so the Kenyon cells' decline arises in the Kenyon cells.
3-octanol's 16 responding glomeruli keep a median 0.47 of their peak at 0.5 s (0.30-0.60; flies 0.48, strong responses
0.43-0.48), their mean 0.50 (133 spikes/s at its peak, 66 at 0.5 s and 55 at 0.9 s); 4-methylcyclohexanol's 13 a median
0.54. They peak at 0.075 s (median), against flies' 140-150 ms after the valve, which includes the odor's travel. So
where the projection neurons halve, the Kenyon cells fall to a fifth (alpha/beta), a quarter (alpha'/beta') and a
twentieth (gamma, two thirds of MBON11's Kenyon cell synapses): their thresholds turn a halved input into far fewer
spikes, the gamma cells (32.5 mV below threshold) most. Whether flies' Kenyon cells, gamma especially, hold more of their
firing through an odor isn't measured class by class (one responding gamma cell in Turner et al. 2008;
mbon11_kc_activity.md).

Correction (2026-10-11, after an independent review): silencing APL doesn't "barely" change the cells' late-over-early
ratios. As tested they are 0.18, 0.25 and 0.05; silenced 0.24, 0.35 and 0.09, 1.3-1.7 times as much. "Most of the decline
isn't APL's" stands.

    python experiments/pn_accommodation_check.py      (writes experiments/pn_accommodation_check.json; seconds)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = Path(__file__).with_suffix(".json")


def main() -> None:
    d = json.loads((HERE / "olfaction_movie.json").read_text())
    out = {"question": __doc__, "flies": {"peak_hz": 88, "peak_s": [0.14, 0.15], "at_500ms_over_peak": 0.48,
                                          "strong_at_500ms_over_peak": [0.43, 0.48]}, "odors": {}}
    for odor, o in d["odors"].items():
        pn = np.asarray(o["pn_hz"])
        n = (len(pn) // 5) * 5
        b50 = pn[:n].reshape(n // 5, 5, -1).mean(1)
        t = d["t0"] + (np.arange(n // 5) + 0.5) * 0.05
        base = b50[t < 0].mean(0)
        early = (t > 0) & (t < 0.4)
        peak = b50[early].max(0)
        responding = (peak - base) > 20
        at500 = b50[np.argmin(np.abs(t - 0.5))]
        t_peak = t[early][np.argmax(b50[early], 0)]
        mean = b50[:, responding].mean(1)
        row = {"responding": int(responding.sum()),
               "at_500ms_over_peak": {"median": round(float(np.median(at500[responding] / peak[responding])), 3),
                                      "range": [round(float((at500 / peak)[responding].min()), 3), round(float((at500 / peak)[responding].max()), 3)]},
               "peak_s_median": round(float(np.median(t_peak[responding])), 3),
               "mean_of_responding": {"peak_hz": round(float(mean[early].max()), 1), "at_500ms_hz": round(float(mean[np.argmin(np.abs(t - 0.5))]), 1),
                                      "at_900ms_hz": round(float(mean[np.argmin(np.abs(t - 0.9))]), 1)},
               "glomeruli": {o["glomeruli"][g]: {"rest": round(float(base[g]), 1), "peak": round(float(peak[g]), 1),
                                                  "at_500ms": round(float(at500[g]), 1)} for g in np.flatnonzero(responding)}}
        row["mean_of_responding"]["at_500ms_over_peak"] = round(row["mean_of_responding"]["at_500ms_hz"] / row["mean_of_responding"]["peak_hz"], 3)
        out["odors"][odor] = row
        print(odor, json.dumps({k: v for k, v in row.items() if k != "glomeruli"}), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
