"""Exploratory check, not pre-registered and not a change to the model: how much stronger or broader would
4-methylcyclohexanol's receptor input have to be for its Kenyon cells to answer as densely as flies' do?

Every other odor of the learning pilots reaches 8-17% of the model's Kenyon cells (learning_pilot9.py, learning_pilot11.py;
flies about 12% for 3-octanol and 4-methylcyclohexanol alike, Hige et al. 2015), but 4-methylcyclohexanol with the
receptor input the evidence supports (receptor_fills.RECOMMENDED: VA3 0.70, D 0.21, the rest 0.10 or less; summed 0.38 of
3-octanol's) reaches only 2-3%, and that is what keeps rung 9's reciprocal failing. The Kenyon cell stage matches flies'
density for five odors, so the input is worth asking about; this check sizes the question and doesn't answer it.
Model: odor_probe60.py's (its cache) with mb_calibration4.py's mushroom body, the Kenyon cells' rest as the learning
pilots set it. 3-octanol with RECOMMENDED; 4-methylcyclohexanol with RECOMMENDED scaled 1, 1.5, 2 and 3 (each glomerulus
capped at DoOR's maximum, 1), with RECOMMENDED plus receptor_fills.PN_INFERRED (the glomeruli inferred only from flies'
PN imaging, some of which whole-cell recordings find silent), and with DoOR's own values. odor_apl_check.trial's protocol
(a 1 s odor after 1.5 s, 2 seeds of 8 flies, APL working).
Measured: the Kenyon cells answering (more than half a spike over the odor's first second, on average) and the share of
4-methylcyclohexanol's that answer 3-octanol and of 3-octanol's that answer 4-methylcyclohexanol (flies 0.33 and 0.30),
4-methylcyclohexanol's summed receptor drive against 3-octanol's (flies' receptor imaging 0.41-0.51).

Ran (3 minutes): strength alone can't get there; breadth helps more. 3-octanol reaches 597 Kenyon cells (14.7%).
4-methylcyclohexanol with RECOMMENDED reaches 109 (2.7%); scaled 1.5, 2 and 3 times, 156, 202 and 285 (3.8, 5.0 and 7.0%),
though at 3 times its summed drive is 0.92 of 3-octanol's, about twice what flies' receptor imaging gives (0.41-0.51).
Throughout, half of its answering cells also answer 3-octanol (0.49-0.51; flies 0.33): a pattern dominated by VA3 keeps
recruiting the cells 3-octanol recruits. With the glomeruli inferred from flies' PN imaging added (summed drive 0.68),
233 answer (5.7%) and only 0.28 of them answer 3-octanol (flies 0.33), a fly-like overlap for the first time. DoOR's own
values (0.54) give 269 (6.6%) and 0.47. So flies' 4-methylcyclohexanol is probably broader at the projection neurons than
the receptor-level evidence makes it, through lateral excitation, receptor responses no dataset has, or both.

    python experiments/odor_mch_input_sensitivity.py      (writes experiments/odor_mch_input_sensitivity.json)
"""
from __future__ import annotations

import contextlib
import json
import time
from pathlib import Path

import numpy as np

import brain_cache
import odor_apl_conductance_check as cc
import odor_probe33 as p33
import odor_probe44 as p44
import odor_probe60 as p60
import odor_probe8 as p8
import warm
from brainfly import odors

OUT = Path(__file__).with_suffix(".json")
SEED, SEEDS = 890000, 2
MCH, OCT = "4-methylcyclohexanol", "3-octanol"


@contextlib.contextmanager
def mch_input(kind: str, scale: float = 1.0):
    """odors.glomeruli with 4-methylcyclohexanol's pattern replaced: RECOMMENDED x scale (capped at 1), RECOMMENDED plus
    PN_INFERRED, or DoOR's; 3-octanol keeps RECOMMENDED."""
    import receptor_fills as rf
    plain = odors.glomeruli
    recommended = rf.filling(plain, recommended=True)

    def glomeruli(name: str, floor: float = 0.0, inhibition: bool = False) -> dict:
        if name.lower() != MCH:
            return recommended(name, floor, inhibition)
        if kind == "DoOR":
            return plain(name, floor, inhibition)
        out = {g: min(v * scale, 1.0) for g, v in rf.RECOMMENDED[MCH].items()}
        if kind == "plus PN-inferred":
            for g, v in rf.PN_INFERRED[MCH].items():
                out[g] = max(out.get(g, 0.0), v)
        return {g: v for g, v in out.items() if v > floor}
    odors.glomeruli = glomeruli
    try:
        yield
    finally:
        odors.glomeruli = plain


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe60", p60.build, p44.prepare)
    import mb_calibration4                             # after the cache, so that their edits don't invalidate it
    out = {"question": __doc__, "mb_calibration": mb_calibration4.apply(o), "conditions": {}}
    apl = o.brain.cells(["APL"])
    answering = lambda rs: np.concatenate([r["spikes"] for r in rs]).mean(0) > 0.5
    conditions = [("RECOMMENDED x1", "scaled", 1.0), ("RECOMMENDED x1.5", "scaled", 1.5), ("RECOMMENDED x2", "scaled", 2.0),
                  ("RECOMMENDED x3", "scaled", 3.0), ("RECOMMENDED plus PN-inferred", "plus PN-inferred", 1.0), ("DoOR", "DoOR", 1.0)]
    with warm.tracking(o, rec):
        out["kc_rest"] = p33.set_rest(o, rec, p8.class_gaps(o, None), SEED + 900)
        with mch_input("scaled", 1.0):
            a = answering([cc.trial(o, rec, OCT, SEED + k, apl, ()) for k in range(SEEDS)])
            oct_drive = sum(odors.glomeruli(OCT).values())
        out["3-octanol"] = {"kcs_answering": int(a.sum()), "summed_drive": round(oct_drive, 3)}
        print("3-octanol", json.dumps(out["3-octanol"]), flush=True)
        for name, kind, scale in conditions:
            with mch_input(kind, scale):
                c = answering([cc.trial(o, rec, MCH, SEED + 10 + k, apl, ()) for k in range(SEEDS)])
                drive = sum(odors.glomeruli(MCH).values())
            both = int((a & c).sum())
            row = {"kcs_answering": int(c.sum()), "share_of_kcs": round(float(c.mean()), 4),
                   "summed_drive_over_3_octanol": round(drive / oct_drive, 3),
                   "share_answering_both": {MCH: round(both / max(int(c.sum()), 1), 3), OCT: round(both / max(int(a.sum()), 1), 3)}}
            out["conditions"][name] = row
            print(name, json.dumps(row), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
