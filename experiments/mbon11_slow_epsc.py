"""Analysis of saved results, not a simulation and not a change to the model: if the Kenyon cell-to-MBON11 current were as
slow as Yamada et al. 2024's flash EPSC, what odor EPSC would the model's Kenyon cell activity give MBON11?

kc_flash_check.py: the model's flashed Kenyon cells fire their spikes within about 50 ms of the flash, so through the
model's 5 ms synaptic current no membrane time constant from 20 to 100 ms gives Yamada et al.'s flash EPSC (peak 102-118 ms
after the flash, 235-260 ms wide at half its peak); through a slow current (rising with 40 ms, decaying with 280 ms) the
same input does, and its paired-pulse ratio matches theirs at about one spike per flash, the reading the model's
depression rule rests on. Flies' odor EPSC in MBON11 (Hige et al. 2015, Fig. 3; research_notes/Rung 9 learning
data/mbon11_input.md 2.5) reaches about 380-430 pA, holds about 170 pA from 0.6 to 1.0 s (0.43 of the peak) and carries
245-275 pC over 0-1.4 s. It wasn't used to choose the slow current.
Input: mbon11_burst_check.py's recorded drive onto MBON11 (each Kenyon cell synapse's weight times its Kenyon cell's spikes
times the strength its depression has left, 10 ms bins, mean of 4 seeds of 8 flies), as in the learning test and with
the synapses not depressing, 3-octanol and 4-methylcyclohexanol; turned into pA per MBON11 cell with the model's 0.054 pC
per synapse (learning_pilot5.py) and passed through the model's current (5 ms, within a bin) and through the slow one,
both carrying the same charge; and, for MBON11's firing, Wang et al. 2026's gain (0.41 spikes/s per pA; odor_probe31.py).
Measured: each current's peak and when, its mean from 0.6 to 1.0 s and that over its peak, its charge over 0-1.4 s; and
the rate the gain makes of it, above MBON11's rest, at its peak and from 0.5 to 1 s, and as spikes over 0-1.4 s.

Ran (2026-10-11): through the slow current the model's Kenyon cell activity gives MBON11 flies' odor EPSC peak and about
half its plateau. To 3-octanol as in the learning test, the model's own current peaks at 4,007 pA per MBON11 cell at 75 ms
and holds 13 pA from 0.6 to 1.0 s (0.003 of its peak), carrying 187 pC; through the slow current it peaks at 347 pA at
0.235 s and holds 83 pA (0.24 of its peak), carrying 184 pC (flies about 380-430 pA at about 0.2-0.3 s, about 170 pA held,
0.43, and 245-275 pC). Undepressed, the slow current peaks at 744 pA and holds 447 (0.60), 579 pC: too much. To
4-methylcyclohexanol it peaks at 60 pA, with 27 pC (flies 230-273 pC): its Kenyon cells are too few however their current
runs. Through Wang et al.'s gain the slow current would raise MBON11 142 spikes/s above its rest at the peak (flies about
130 above about 6) and 41 above it from 0.5 to 1 s (flies about 90), 75 spikes over 0-1.4 s (flies 118); the model's own
current runs far past the gain's range (1,600 spikes/s at its peak by the gain, where the model's MBON11 saturates), so the
gain says nothing about it. So the slow reading of Yamada et al.'s flash EPSC, chosen without flies' odor EPSC, brings the
model's odor EPSC to flies' peak and about halfway to their plateau with the depression as measured; the rest of the
plateau's shortfall is the Kenyon cells' own decline (mbon11_burst_check.py: to 5-25% of their early rate by 0.5-1 s). The
times compare loosely: flies' EPSC starts about 0.18 s after their odor valve, the model's at once.

Correction (2026-10-11, after an independent review): flies' 3-octanol charge is about 245-250 pC (Hige et al.'s 248 and
244; mbon11_kc_activity.md section 4). The 245-275 above pools both odors; 4-methylcyclohexanol's is 265-273. No reading
changes.

    python experiments/mbon11_slow_epsc.py      (writes experiments/mbon11_slow_epsc.json; seconds)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = Path(__file__).with_suffix(".json")
CHARGE_PC, GAIN_HZ_PER_PA, TAU = 0.030 * 34.5 / 19.0, 0.41, 0.005   # learning_pilot5.py's, odor_probe31.py's, Shiu's
SLOW = (0.040, 0.280)                                               # kc_flash_check.py's


def main() -> None:
    d = json.loads((HERE / "mbon11_burst_check.json").read_text())
    flash = json.loads((HERE / "kc_flash_check.json").read_text())
    dt = d["bin_s"]
    t = d["t0"] + (np.arange(200) + 0.5) * dt
    w_syn = GAIN_HZ_PER_PA * CHARGE_PC / (d["held"]["gain"]["slope_hz_per_mv"] * TAU)
    to_pa = CHARGE_PC / w_syn / 2                                     # drive (weight x spikes/s) -> pA per MBON11 cell
    tt = (np.arange(300) + 0.5) * dt
    k = np.exp(-tt / SLOW[1]) - np.exp(-tt / SLOW[0])
    k /= k.sum() * dt
    out = {"question": __doc__, "w_syn": round(w_syn, 4), "pa_per_drive_unit": round(to_pa, 5),
           "flash_slow_current_at_one_spike": {tau: row["targets"]["1"]["current_slow"] for tau, row in flash["conditions"].items()
                                               if row["targets"].get("1")},
           "conditions": {}}
    for cond in ("as tested", "not depressing"):
        out["conditions"][cond] = {}
        for odor in ("3-octanol", "4-methylcyclohexanol"):
            r = d["conditions"][cond][odor]["series"]
            drive = np.sum([r["drive"][c] for c in r["drive"]], 0)
            drive = drive - drive[t < 0].mean()
            row = {}
            for name, cur in (("fast", drive * to_pa), ("slow", np.convolve(drive, k)[:len(t)] * dt * to_pa)):
                j = int(np.argmax(cur))
                late = float(cur[(t > 0.6) & (t < 1.0)].mean())
                hz = GAIN_HZ_PER_PA * cur
                row[name] = {"peak_pa": round(float(cur[j]), 1), "t_peak_s": round(float(t[j]), 3), "pa_0.6_to_1s": round(late, 1),
                             "late_over_peak": round(late / float(cur[j]), 3), "charge_pc_0_to_1.4s": round(float(cur[(t > 0) & (t < 1.4)].sum() * dt), 1),
                             "gain_hz_peak": round(float(hz.max()), 1), "gain_hz_0.5_to_1s": round(float(hz[(t > 0.5) & (t < 1.0)].mean()), 1),
                             "gain_spikes_0_to_1.4s": round(float(hz[(t > 0) & (t < 1.4)].sum() * dt), 1),
                             "series_pa": np.round(cur, 1).tolist()}
            out["conditions"][cond][odor] = row
            print(cond, odor, json.dumps({n: {x: v for x, v in r_.items() if x != "series_pa"} for n, r_ in row.items()}), flush=True)
    OUT.write_text(json.dumps(out))


if __name__ == "__main__":
    main()
