"""Exploratory, not pre-registered: with 3-octanol's and 4-methylcyclohexanol's receptor input as the receptor-level
evidence puts it at Hige et al.'s concentration, how do the model's projection neurons and Kenyon cells answer them,
compared like for like with flies'?

research_notes/Rung 9 learning data/oct_mch_concentration.md: weighing every receptor-level measurement by tier and
concentration, correcting DoOR's import errors (D's unsubtracted solvent response, DA2's floor) and giving no drive where
flies' PN responses are lateral (DA1, DL3), 4-methylcyclohexanol's summed receptor drive at 2% of saturated vapour is
0.37 of 3-octanol's (receptor_fills.RECOMMENDED: 1.99 against 5.32; 2 glomeruli above 0.1 against 13), so the receptor
input can't equalize the odors, and flies' equalization has to come downstream. mch_oct_equalization.md: flies' PN ratios
(0.98 over Badel et al.'s 37 glomeruli, 0.85 over Barth et al.'s 18) leave out 3-octanol's strongest glomeruli (VM5d,
VM5v, VC3, DC1), and summed over Badel's 37 the model's odor_probe54.py already gives 0.86 (0.93 with the fills),
against 0.56 over every glomerulus; at the Kenyon cells the model gives 0.25 where flies' give 0.73-0.92, and flies' APL
holds 3-octanol back more (Prisco et al. 2021), which the model's, saturating, doesn't (odor_apl_check.py,
odor_apl_range_check.py).
Model: odor_probe54.py's (its cache) with mb_calibration.py's mushroom body.
Measured, with receptor_fills.RECOMMENDED's input: odor_equalization_check.py's measures (now with the ratio over
Badel et al.'s glomeruli and per glomerulus over all of them) and odor_probe36.measure's (Kenyon cells by class and
odor, overlap, MBON11). Seeds 690000 (odor_probe36.measure) and 695000 (equalization).

Ran: with the receptor input the evidence supports, the model is far from equalizing the odors even where flies' PNs
were imaged. 4-methylcyclohexanol's summed receptor response is 0.31 of 3-octanol's over the first 0.5 s; its PNs sum
0.51 of 3-octanol's over Badel et al.'s 37 glomeruli (flies 0.98; with DoOR's input 0.86, odor_probe54.py), 0.35 per
glomerulus over all of them and 0.19 over every PN (0.52 with DoOR's); 1.38% of Kenyon cells answer it against 8.96% for
3-octanol (0.15; flies 0.73-0.92), and MBON11 gains 4.4 spikes against 31.5 (flies 110 and 118). Its PNs answer in 9
glomeruli over 10 spikes/s (3-octanol 13), at 86 (VA3) and 76 (D) spikes/s and 19-28 in seven more. Where flies' PNs
answer 4-methylcyclohexanol without receptor input the evidence supports (Badel et al.: DA2 236, VM7v 121, DA3 116, VA5
110, DC3 101, DL3 91, DM3 87, VM7d 84, DA1 78, DL5 77, VM3 72, VA6 69% ΔF/F), the model's sit at rest, and the same holds
for 3-octanol's (DL3 166, DA2 140, VM3 122, DA1 118, DA3 113, DC3 86); with DoOR's broader input for
4-methylcyclohexanol (D and DA2 inflated by import errors) the model's PNs had answered in several of them. So the model's
antennal lobe lacks what produces flies' PN responses beyond the receptor input, about as large for
4-methylcyclohexanol as for 3-octanol. Lateral excitation through electrically coupled excitatory LNs gives a PN with no
receptor input only 6-32 spikes/s (lateral_excitation.md), and the two labs' PN imaging disagree widely in several of
these glomeruli (DA2: Badel 236, Barth 44), so how much of it is real input, lateral excitation or imaging remains open.

    python experiments/odor_probe55.py         (writes experiments/odor_probe55.json)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import brain_cache
import odor_probe36 as p36
import odor_probe44 as p44
import odor_probe54 as p54
import warm

OUT = Path(__file__).with_suffix(".json")
SEED, EQUALIZATION_SEED = 690000, 695000


def main() -> None:
    t0 = time.perf_counter()
    o, rec, built = brain_cache.load("odor_probe54", p54.build, p44.prepare)
    import mb_calibration                              # after the cache, so that their edits don't invalidate it
    import odor_equalization_check as eq
    import receptor_fills
    out = {"question": __doc__, "mb_calibration": mb_calibration.apply(o)}
    with receptor_fills.applied(recommended=True) as inputs, warm.tracking(o, rec) as held:
        out["inputs"] = inputs
        out["equalization"] = eq.measure(o, rec, EQUALIZATION_SEED)
        OUT.write_text(json.dumps(out, indent=1))
        out.update(p36.measure(o, rec, built, SEED))
        od = out["odors"]
        print("KCs", json.dumps({x[:6]: round(100 * od[x]["kc_share"], 2) for x in ("3-octanol", "4-methylcyclohexanol")}),
              "MCH/OCT KC", round(od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"], 3),
              "MBON11", json.dumps({x[:6]: r["MBON11"] for x, r in out["mbon11_input"].items()}), flush=True)
        out["measure_settles"] = held["settles"]
    out["seconds"] = round(time.perf_counter() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done ({out['seconds']} s)", flush=True)


if __name__ == "__main__":
    main()
