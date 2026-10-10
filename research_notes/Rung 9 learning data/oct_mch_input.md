# 3-octanol vs 4-methylcyclohexanol: how strongly should MCH drive the model at Hige's 2% saturated vapour?

Read 2026-10-10.

**The question.** The model drives each olfactory receptor neuron (ORN) type at its DoOR 2.0 consensus response
(spontaneous level subtracted) times 200 spikes/s. Its two learning odours come out very unequal:

- 3-octanol (OCT): 12 glomeruli above 0.2, summed response 6.4.
- 4-methylcyclohexanol (MCH): 4 glomeruli above 0.2, summed response 2.85.
- So OCT recruits about four times as many Kenyon cells (KCs), and the mushroom body output neuron MBON11 gains 132
  spikes to OCT but only 41 to MCH.
- In flies (Hige et al. 2015, MBON-γ1pedc, both odours at "2% of saturated vapor") the two responses are about equal:
  118 ± 8.3 vs 110 ± 11 spikes, and about 250 vs 265 pC of EPSC charge.

Does MCH really drive about as much as OCT at Hige's concentration, and by how much does the DoOR-based input
understate it?

**Conventions.**
- Quotes are exact.
- "(fig., approx.)" means I measured the value from figure pixels by fitting a line to the axis ticks. Each case gives
  the calibration.
- "(derived)" means my own arithmetic.
- "via DoOR" means the value as entered in the DoOR.data per-receptor tables
  (<https://github.com/ropensci/DoOR.data>, `data/*.csv`), because the original paper was not accessible.
- "Not reported" means I looked in the full text, legends and supplement and the value is not there.
- Glomeruli are named as DoOR maps the receptors (D = Or69a, VA3 = Or67b, DA2 = Or56a/ab4B, DM2 = Or22a, and so on).
- Some readings come from two helper agents that searched in parallel. They are marked "(helper)" and are reported as
  the helpers gave them. I re-checked Badel 2016's Table S2 and Barth 2014's two heat maps myself.

## Summary

1. **Answer: downstream of the receptors yes, at the receptors no.**
   - **Receptor neurons (ORNs).** MCH's summed response is about 0.4–0.5 of OCT's.
     - Barth et al. 2014 imaged ORN terminals in 29 glomeruli (Or83b-GAL4 > GCaMP3, odour concentrations balanced for
       naive preference): MCH/OCT 0.41–0.51 (fig., approx., my reading; 0.43 in a helper agent's independent reading).
     - Glomeruli above 40% ΔF/F: OCT 7, MCH 1 (VA3).
     - DoOR gives 0.45.
     - In single-sensillum recordings MCH never exceeds 13 spikes/s in antennal ab1–ab7, where OCT reaches 162.
   - **Projection neurons (PNs).** MCH is about equal.
     - Barth 2014, same lab and odours: 0.85 (fig., approx.). Glomeruli at or above 100% ΔF/F: OCT 9, MCH 8.
     - Badel et al. 2016, 37 glomeruli at 10⁻² in oil: 0.98 (derived from Table S2). 18 glomeruli respond
       significantly to MCH against 13 to OCT.
     - Prisco et al. 2021: the same number of active PN boutons in the calyx (0.98).
   - **Kenyon cells (KCs).** MCH recruits 0.7–0.9 times as many.
     - Hige 2015 at its own 2% saturated vapour: 49 vs 53 responders (0.92).
     - Honegger 2011 at 1% saturated vapour: 0.73.
     - Lin 2014 at 10⁻² in oil: 0.6–0.7.
     - Prisco 2021: KC claws 0.97.
   - **MBON11** (Hige 2015): 0.93 in spikes.
   - **Physics.** The two odours have nearly the same vapour pressure, so "2% of saturated vapour" delivers about the
     same number of molecules of each (OCT/MCH ≈ 0.93, derived).
   - **So the antennal lobe roughly doubles MCH's relative strength,** from about 0.45 at the ORNs to 0.85–0.98 at the
     PNs. The model's KC ratio (1 : 4) and MBON11 ratio (0.31) are about 3 times too unequal. Since DoOR's ORN-level
     total roughly matches the ORN measurements, most of that gap has to come from how the model transforms ORN input
     into PN output. DoOR's missing weak MCH inputs add to it.
2. **DoOR's total is about right; its breadth is not.**
   - DoOR has MCH data for only 22 of the 35 glomerulus-mapped receptors that have OCT data.
   - The 13 receptors with OCT data only (Or47a, Or35a, Or85d, Or67a, Or59c, Or33c, Or85e, Or2a, Or49a, Or46a, Or33a,
     Or33b, Gr21a/Gr63a) supply 1.98 of OCT's summed 6.41. That is 56% of the 3.56 gap (derived).
   - **Like-for-like.** On the 22 receptors measured for both odours, MCH/OCT is 0.64 (derived).
   - **But filling those 13 receptors would not close much of the gap.** Barth's ORN imaging covers several of them,
     and MCH is weak there: VC3 21 vs 95% ΔF/F, DM3 about 8 (no response) vs 50, DM6 13 vs 63, VM7 about 7 vs 21. VC1
     (32 vs 47) is the exception.
   - **What the ORN imaging adds.** Barth's ORN imaging shows MCH weakly exciting several glomeruli where DoOR gives
     it nothing: VC1 32, VC3 21, VM2 17 and VA7 16% ΔF/F, against 47, 95, 82 and 6 for OCT. It also shows MCH strongly
     inhibiting DL5 (−30%).
   - **Untested receptors.** Badel's PNs respond to MCH in seven glomeruli whose receptors were never tested with MCH
     (VM7v, DA3, DL4, DA4l, DL3, DA1, VM3).
3. **MCH's four strong glomeruli in DoOR each rest on one or two studies.**
   - VA3 (0.876): one antennal imaging dataset (Galizia et al. 2010), where MCH is 1.17 times the reference odour
     1-hexanol and OCT is 0.37. Barth's ORN imaging agrees: VA3 is MCH's only strong ORN glomerulus.
   - D (0.635): one imaging dataset (Münch & Galizia 2016), MCH 1.33 vs OCT 1.68 % ΔF/F.
   - DA2 (0.274): the same study, MCH 1.87 vs OCT 0.38 % ΔF/F, against 17.6 for geosmin. Barth's ORN imaging shows no
     DA2 response to MCH (D was not among its 29 glomeruli). Badel's PNs respond strongly to both odours in DA2 and D.
   - DM2 (0.254): single-sensillum recordings (de Bruyne 2001: MCH 13 vs OCT 57 net spikes/s) and Pelz 2006's EC50s
     (10⁻²·¹⁵ vs 10⁻²·⁸⁰ v/v).
4. **Single-sensillum recordings that tested both odours in one study** (10⁻² or 1% v/v in paraffin oil).
   - **Antennal basiconic ab1–ab7** (de Bruyne 2001, via Schmuker 2007 and DoOR). OCT excites five classes strongly:
     ab6A 162, ab3B 112, ab7A (DoOR category 79), ab3A 57 and ab5B 27 net spikes/s. MCH tops out at 13 (ab3A) and
     inhibits ab6A (−15).
   - **Palp pb1** (de Bruyne 1999, fig., approx.). MCH 17–18 in both neurons. OCT 14 in pb1A and 3.5 in pb1B. The
     paraffin-oil control is 8.4 and about 1.
   - **Or19a/DC1** (Dweck 2013, via DoOR): OCT 36, MCH 5.
   - Summed over the single-neuron classes recorded with both odours, MCH ≈ 0.15 × OCT (derived).
5. **Hallem & Carlson 2006 tested neither odour.** Table S1 of their supplement lists 110 odorants, with 1-octanol and
   1-octen-3-ol but no 3-octanol or 4-methylcyclohexanol.
   - Hallem 2004, Kreher 2005/2008 and Goldman 2005 tested OCT only. This is why so many receptors have OCT data and no
     MCH data.
6. **DoOR has no concentration axis.**
   - DoOR 2.0 says: "Aspects that might be covered in future versions include odorant concentrations."
   - The only dose–response data are EC50s: Or22a/DM2 for both odours (Pelz 2006) and Or13a/DC2 for OCT only
     (10⁻³·⁵).
   - Wang et al. 2003 (ex vivo, air dilution of saturated vapour) saw no PN glomerulus respond to 3-octanol at 2%
     saturated vapour, and five at 40%. MCH was not tested.
7. **Which glomeruli MCH strongly activates, by direct measurement.**
   - ORNs (Barth): VA3 strongly. Weakly VC1, VM5, DC2, DC3, VC3, DM2, DC1, VM2.
   - PNs (Badel): DA2 236, D 172, VM7v 121, DA3 116, VA5 110, VA3 108, DC3 101, DL4 97, DA4l 96, DL3 91, DM6 88,
     DM3 87.
   - PNs (Barth, a different subset of 18 glomeruli): VM4 241, DL4 218, DM6 198, VC2 168, DM2 166, DM5 162, VM1 161,
     DC1 109.
   - PNs (Pech et al. 2015, Fiala lab): DL4.
   - The two labs agree on DL4 and DM6 but otherwise differ widely, for example VM4 241 vs 10 and VC2 168 vs 40. DoOR's
     VA3, D and DA2 are among Badel's top six.
8. **KC overlap.**
   - 30–33% of each odour's responders also respond to the other (Hige 2015), a Jaccard index of about 0.19 (derived).
   - The pattern correlation is r ≈ 0.22 (Campbell 2013).
9. **How labs chose concentrations.**
   - Hige 2015 gives no reason for 2% of saturated vapour for both odours. Their behaviour supplement uses 1:1000 in
     oil for both.
   - Labs that balanced naive behaviour ended up on different sides:
     - Campbell 2013 (Turner lab): "MCH, 1.5:1000; OCT, 1:1000".
     - Barth 2014 (Fiala lab): MCH 1:750, OCT 1:500.
     - Churgin 2025 adjusted dilutions week by week.
10. **Correction, with numbers.**
    - **Do not scale MCH's ORN drive by about 2.** Summed across glomeruli, every ORN-level measurement puts MCH at
      0.15–0.5 of OCT. Single glomeruli vary:
      - MCH is larger at VA3 and DA2 (imaging).
      - It is about 0.8 of OCT at D.
      - At DM2 it is 0.2–0.8, depending on the study (single sensillum 0.23, Barth 0.30, Pelz 0.75–0.80).
    - **Fill DoOR's gaps with weak drive taken from Barth's ORN imaging** (derived; crude ΔF/F-to-DoOR conversions):
      - MCH: VC1 0.10–0.25, VC3 0.09–0.16, VM2 ≈ 0.12, VA7 ≈ 0.12.
      - OCT: VM2 ≈ 0.69. DoOR has neither odour there.
      - MCH's summed drive becomes 3.3–3.5 against OCT's 7.1. The ratio stays at 0.46–0.49, as at real ORNs.
    - **Make the model's antennal lobe reproduce the equalisation.** In Barth's data an ORN ratio of 0.41–0.51 becomes
      0.85 at the PNs (0.98 in Badel). Then the KCs should land at 0.73–0.92, with about 30% shared responders, and
      MBON11 at about 0.93.
    - **Stopgap if the antennal lobe cannot be fixed:** a PN-matched input. One version fills Badel's PN glomeruli
      that have no ORN data into DoOR units (MCH 2.85 → 5.12, OCT 6.41 → 8.35, ratio 0.61). The other scales MCH by
      about 2. Both stand in for missing normalisation; neither is what the ORNs do. See "For the model".

## 1. The model's input: DoOR consensus minus SFR, the larger receptor per glomerulus

Computed from `door_response_matrix.csv`, `door_mappings.csv` and `odor.csv` (DoOR.data master, downloaded 2026-10-06).
The rules match `brainfly/odors.py`:
- Subtract each receptor's SFR row.
- Where several receptors share a glomerulus, take the largest value.
- Drop whole-sensillum units (ac1, ac2, ac3_noOr35a, ac4) and receptors with no glomerulus.

Glomeruli where either odour exceeds 0.05:

| Glomerulus | OCT (receptor) | MCH (receptor) |
|---|---|---|
| D | 0.741 (Or69a) | 0.635 (Or69a) |
| VA3 | 0.123 (Or67b) | **0.876** (Or67b) |
| VM5d | **0.676** (Or85b) | 0.080 (Or85b) |
| VM5v | **0.592** (Or98a) | 0.085 (Or98a) |
| DC2 | **0.579** (Or13a) | 0.078 (Or13a) |
| DM3 | **0.468** (Or47a) | −0.002 (ab5B; Or47a not tested) |
| VC3 | **0.434** (Or35a) | not tested |
| DC1 | 0.374 (Or19a) | −0.048 (Or19a) |
| VA4 | 0.369 (Or85d) | not tested |
| DM2 | 0.337 (Or22a) | 0.254 (Or22a) |
| DM6 | 0.319 (Or67a) | not tested |
| DA2 | 0.241 (ab4B) | 0.274 (ab4B) |
| VM7v | 0.204 (Or59c) | not tested |
| VC1 | 0.153 (Or33c) | not tested |
| DA4m | 0.133 (Or2a) | not tested |
| DL1 | 0.118 (Or10a) | 0.131 (Or10a) |
| DL4 | 0.115 (Or49a) | not tested |
| VM7d | 0.094 (Or42a) | 0.061 (Or42a) |
| VC2 | 0.010 (Or71a) | 0.083 (Or71a) |
| DC3 | 0.046 (Or83c) | 0.078 (Or83c) |
| DL5 | 0.032 (Or7a) | 0.060 (Or7a) |
| DM1 | 0.063 (Or42b) | −0.012 (Or42b) |
| VA6 | 0.055 (Or82a) | 0.024 (Or82a) |

Totals (derived):

| | OCT | MCH |
|---|---|---|
| Glomeruli > 0.2 | 12 (sum 5.33) | 4 (sum 2.04) |
| Glomeruli > 0 | 27 (sum 6.41) | 18 (sum 2.85) |
| Only the 22 receptors measured for both odours: glomeruli > 0.2 | 8 (sum 3.75) | 4 |
| Only the 22 receptors measured for both odours: positive sum | 4.43 | 2.85 |

- The 13 mapped receptors with OCT data but no MCH data are Gr21a.Gr63a, Or2a, Or33a, Or33b, Or33c, Or35a, Or46a,
  Or47a, Or49a, Or59c, Or67a, Or85d and Or85e. No receptor has MCH data without OCT data.
- Small MCH values of 0.06–0.09 at VM5v, VM5d and DC2 are normalisation residue. The underlying single-sensillum
  recordings are 0 (VM5v, de Bruyne 2001's coded value), 4 net spikes/s (VM5d) and −15 net spikes/s (DC2). Calcium
  imaging does show weak MCH signals in VM5 and DC2 (§7), so this is contested.

## 2. DoOR 2.0: which studies feed OCT and MCH

[Münch & Galizia 2016, Sci Rep 6:21841](https://pmc.ncbi.nlm.nih.gov/articles/PMC4766438/), with the DoOR.data tables.
Raw values are as stored in the per-receptor CSVs. Concentrations are from `door_dataset_info.csv` unless stated.

| Receptor (glomerulus) | Study (DoOR column) | Method, concentration | OCT | MCH |
|---|---|---|---|---|
| Or69a (D) | Muench.2016.AntGC1 | antennal GCaMP1.3 imaging, 10⁻² in mineral oil | 2.412 | 2.068 |
| Or67b (VA3) | Galizia.2009.nmr | antennal imaging, 10⁻² highest (Galizia 2010) | 0.371 | 1.172 |
| Or67b (VA3) | Kreher.2005.EN / Kreher.2008.EN | larval receptor in the empty neuron (spikes/s) | 34 / 31 | — |
| Or85b (VM5d) | Schmuker.2007.TR = de Bruyne 2001 | SSR, 10⁻² | 120 (= 112 net + SFR 8) | 12 (= 4 + 8) |
| Or85b (VM5d) | Hallem.2004.EN / .WT | empty neuron / wild-type ab3B | 245 / 254 | — |
| Or98a (VM5v) | Bruyne.2001.RR | SSR, 10⁻², coded values | 79 | 0 |
| Or13a (DC2) | Schmuker.2007.TR | SSR, 10⁻² | 176 (= 162 + 14) | −1 (= −15 + 14) |
| Or13a (DC2) | Kreher.2008.EN | empty neuron | 143 | — |
| Or13a (DC2) | Nissler.2007.nmr / .EC50 | antennal imaging (Galizia 2010) | 0.99 (reference) / EC50 3.504 | 0.42 / — |
| Or47a (DM3) | Kreher.2008.EN | empty neuron | 109 | — |
| ab5B (DM3) | Schmuker.2007.TR | SSR, 10⁻² | 29 (= 27 + 2) | 0 (= −2 + 2) |
| Or35a (VC3) | Kreher.2008.EN | empty neuron | 95 | — |
| Or19a (DC1) | Dweck.2013.WT | SSR, 10⁻² | 36 | 5 |
| Or85d (VA4) | Goldman.2005.WT / Bruyne.1999.WT | SSR, 1% v/v / 10⁻² | 81 / 57.8 | — |
| Or22a (DM2) | Schmuker.2007.TR | SSR, 10⁻² | 61 (= 57 + 4) | 17 (= 13 + 4) |
| Or22a (DM2) | Pelz.2006.ALEC50 | AL imaging, −log₁₀ EC50 (v/v) | 2.8 | 2.15 |
| Or67a (DM6) | Hallem.2004.EN | empty neuron | 110.2 | — |
| ab4B (DA2) | Muench.2016.AntGC3 | antennal GCaMP3 imaging, 10⁻² | 0.403 | 1.889 |
| ab4B (DA2) | Stensmyr.2012.WT | SSR | −1.2 | — |
| ab4B (DA2) | Bruyne.2001.RR | SSR, 10⁻² (excluded by DoOR for ab4B) | 0 | 0 |
| Or59c (VM7v) | Goldman.2005.WT / Bruyne.1999.WT | SSR | 46 / 40.6 | — |
| Or10a (DL1) | Schmuker.2007.TR / Muench.2016.AntGC1 | SSR / imaging | 8 / 1.009 | 13 / 1.021 |
| Or42a (VM7d) | Bruyne.1999.WT | SSR, 10⁻² | 24.0 | 27.2 |
| Or71a (VC2) | Bruyne.1999.WT | SSR, 10⁻² | 8.1 | 23 |
| Or83c (DC3) | Ronderos.2014.WT | SSR, Or83c in at1, undiluted | 10 | 17 |
| Or42b, Or49b, Or67c, Or7a, Or82a, Or92a | Bruyne.2001.RR | SSR, 10⁻² | 0 | 0 |
| Or92a (VA2) | Galizia.2009.nmr | antennal imaging | 0.023 | 0.025 |
| Or47b (VA1v) | Pelz.2005.Or47bnmr / Muench.2016.AntGC1 | imaging | — / 0.236 | 1.41 / 0.355 |
| ac1 / ac2 / ac3 (Or35a knocked down) / ac4 | Silbering.2011.WT | whole-sensillum SSR, 1% v/v | 8.5 / 15 / 14 / −5 | 29 / −6 / −0.5 / −15.1 |

- **Bruyne.2001.RR.** Its values take only 0, 30, 59 (oil), 79, 147 and 203 across 47 odorants and 8 neuron classes.
  They look like category codes (derived from inspecting the column). I could not check what each category means: the
  de Bruyne 2001 full text was paywalled, and its 47-odour figure is not on the publisher's image server.
- **Exclusions.** `door_excluded_data.csv` drops Bruyne.2001.RR and Marshall.2010.WT for ab4B. So DA2's consensus rests
  on the imaging data and Stensmyr 2012.
- **Compression.** DoOR's ab4B consensus puts MCH at 0.274 against geosmin at 0.573 (48%). In the raw imaging, MCH is
  only 1.889/17.611 = 11% of geosmin (derived). DoOR's dataset merging compresses the scale.
- **The Or69a values disagree between sources.** DoOR stores OCT 2.412 and MCH 2.068. The paper's Table S5 gives
  OCT 1.68 ± 0.47 (n = 7) and MCH 1.33 ± 0.27 (n = 7), "solvent subtracted" according to the helper's reading. The MCH/OCT
  ratio is 0.86 in DoOR and 0.79 in Table S5.
- **On concentration** (Discussion):
  > "Aspects that might be covered in future versions include odorant concentrations. Merging responses of different
  > odorant concentrations across labs is difficult because it is difficult if not impossible to measure absolute
  > concentration in a controlled way. For one, the absolute odorant concentrations reaching the animal depends on the
  > vapor pressure of a compound. Concentrations are also influenced by how a stimulus is presented."

  > "butyl acetate and ethyl hexanoate elicit equally strong responses from Or22a expressing OSNs when tested at a 1:100
  > dilution but the OSNs are sensitive to an almost three log steps lower concentration of ethyl hexanoate as compared
  > to butyl acetate (quantified as the dose eliciting the half maximal response in Pelz et al.)."
- **SFR handling:** "We treated SFR as a normal odorant. For all studies that subtracted but did not report SFR or for
  calcium imaging studies, we set SFR to 0. To regain negative response values (inhibitory odorants) we then subtracted
  the individual SFR values from all other response values".
- **The new imaging data** (AntGC1, AntGC3). Methods:
  - "All odorants were applied at 10⁻² diluted in 5 mL mineral oil".
  - "A head space of 2 mL was injected in two 1 mL portions at time points 6 s and 9 s with an injection speed of
    1 mL s⁻¹ into a continuous flow (60 mL min⁻¹) of purified air."
  - "Response values were calculated as the mean response during 5 s after stimulus onset subtracted by the mean
    response during 2.5 s before stimulation."
  - On Or69a: "Or69a OSNs responded particularly broad, showing activity towards most of the odorants in our set: the
    receptor kurtosis was −0.36. We found the strongest responses for ethyl 3-hydroxyhexanoate, alpha-terpineol,
    3-octanol and linalool."
- **DoOR's EC50 data.**
  - Or22a (Pelz.2006.ALEC50): OCT 2.8, MCH 2.15. These are −log₁₀ of the v/v dilution giving half-maximal response, so
    OCT is 10^0.65 ≈ 4.5 times more potent (derived). §7 has Pelz's own numbers.
  - Or13a (Nissler.2007.EC50): OCT 3.504. MCH not measured.

## 3. Hallem & Carlson 2006 and Hallem et al. 2004

**Hallem & Carlson 2006.** Cell 125:143. Supplement:
<https://ars.els-cdn.com/content/image/1-s2.0-S0092867406003631-mmc1.pdf>.
- Legend: "Table S1. Odorant Responses of 24 Receptors to 110 Odorants ... Data for the set of odorants tested across
  concentrations are from Figure 4 and n = 6; for all other odorants, n = 6 except that n = 4 for responses of
  <50 spikes/s."
- Stimulus, from the Figure S1 legend: "Odorant was delivered as a 10-2 dilution of geranyl acetate in paraffin oil."
- **Neither odour is in the panel.** Table S1's alcohols are methanol, ethanol, 1-propanol, 1-butanol, 1-pentanol,
  1-hexanol, 1-octanol, 2-pentanol, 3-methylbutanol, 3-methyl-2-buten-1-ol, 1-penten-3-ol, 1-octen-3-ol, E2-hexenol,
  Z2-hexenol, E3-hexenol, Z3-hexenol, glycerol and 2,3-butanediol.
- DoOR's import (Hallem.2006.EN, 24 receptors × 111 rows including the SFR row) agrees.
- So the 24 receptors in this study have no OCT or MCH data from it.
- Eight adult receptors have no DoOR consensus value for either odour from any study: Or9a (VM3), Or23a (DA3), Or43a
  (DA4l), Or43b (VM2), Or65a (DL3), Or67d (DA1), Or85f (DL4) and Or88a (VA1d). The IR classes have only coeloconic
  whole-sensillum data.

**Hallem, Ho & Carlson 2004.** Cell 117:965. Via DoOR.
- 3-octanol only, at Or85b (ab3B: 245 spikes/s in the empty neuron, 254 in the wild type) and Or67a (110).
- 4-methylcyclohexanol is not in its 56-odour panel. The panel does include cyclohexanol and cyclohexanone.
- **A possible MCH receptor nobody has tested.** Or43a (DA4l) responds to cyclohexanol (139 spikes/s) and
  cyclohexanone (127) in Hallem 2004's empty-neuron data, via DoOR. MCH has never been tested on Or43a. Badel 2016's DA4l
  PNs respond to MCH (96% ΔF/F) and hardly to OCT (15%) (§8).

## 4. de Bruyne, Clyne & Carlson 1999: maxillary palp

J Neurosci 19:4520 ([PMC6782632](https://pmc.ncbi.nlm.nih.gov/articles/PMC6782632/)).

**Stimulus quotes:**
- "A glass tube held 8 mm from the preparation continuously supplied humidified air to the preparation (35 ml/sec giving
  an airspeed of 180 cm/sec). For reliably delivering odor puffs using many odorants without cross-contamination, we
  used the headspace from 5 ml disposable syringes. A 2 ml/sec flow of nitrogen entered the airstream".
- "a syringe containing a small piece of filter paper laden with the odorant dissolved in 20 μl of paraffin oil at a
  10⁻² dilution (unless otherwise indicated)."
- "4-methylcyclohexanol was a mix of cis and trans isomers."

**Panel.**
- "a chemically diverse group of 16 odorants". 3-octanol was chosen because it is among the odorants that "had been
  used extensively in previous research on Drosophila olfaction and are known to induce strong behavioral responses."
- MCH was tested only on pb1, the sensillum shown in Fig. 5. The "diagnostic subset of 7 of the 16 odors" used for pb2
  and pb3 is ethyl acetate, isoamyl acetate, 4-methylphenol, benzaldehyde, 3-octanol, E2-hexenal and cyclohexanone. It
  does not include MCH.

**Results quotes:**
- "The pb1B cell responds strongly to only one of the tested odorants, 4-methylphenol, to which it shows an increase in
  spike frequency of 178 ± 47 spikes/sec (± SD; n = 13). The only other response from pb1B that was significantly
  different from that of the paraffin oil control is the response to 4-methylcyclohexanol, an odor molecule
  structurally similar to 4-methylphenol."
- "pb2B is strongly inhibited by 3-octanol and several other odors. Specifically, the spontaneous firing frequency of
  pb2B is 32 ± 7 spikes/sec and is reduced 80–100% by 3-octanol. The pb3 sensillum contains two neurons that are both
  excited by 3-octanol and isoamyl acetate".

**Fig. 5 readings** (fig., approx.):
- Legend: "Responses of the two pb1 neurons to a set of 16 odorants (error bars indicate SD; n = 13)".
- Calibration: on the PMC image (786 × 1199 px), the x-ticks at 0, 50, 100, 150 and 200 spikes/s sit at columns 239,
  347, 455, 562.5 and 670, giving 2.155 px per spike/s. Each bar end is the centre of the bar's right edge.

| | pb1A (Or42a, VM7d) | pb1B (Or71a, VC2) |
|---|---|---|
| MCH | 16.7 (SD ≈ 5.6) | 17.9 (SD ≈ 7.2) |
| OCT | 14.4 (SD ≈ 6.5) | 3.5 (SD ≈ 3.9) |
| Paraffin oil | 8.4 (SD ≈ 4.6) | ≈ 1 |

- Net of the oil control, pb1A gives MCH ≈ 8 and OCT ≈ 6, and pb1B gives MCH ≈ 17 and OCT ≈ 2.5 (derived).
- DoOR stores higher values: pb1A OCT 24.0 and MCH 27.2, pb1B OCT 8.1 and MCH 23 ("Updated with original Data in DoOR
  v2.0"). These match the Fig. 5 values plus the spontaneous rates printed in Fig. 6 (pb1A "11 ± 1", pb1B "6 ± 1"
  spikes/s): 25.4, 27.7, 9.5 and 23.9 (derived).
- Fig. 6 confirms that the seven-odour panel used on pb2 and pb3 (n = 15 and 14) has no MCH. On it, 3-octanol excites
  pb3A (Or59c, VM7v) by about 32 and pb3B (Or85d, VA4) by about 48 spikes/s, and inhibits pb2B (fig., approx.).
  Calibration: on the PMC image (612 × 1280 px), the ticks at −50 to 250 sit at columns 158.5, 232, 305.5, 381, 455,
  529 and 604.5, giving 1.486 px per spike/s.

## 5. de Bruyne, Foster & Carlson 2001: antennal basiconic sensilla, via Schmuker et al. 2007 and DoOR

**Sources.**
- The paper (Neuron 30:537) was paywalled (403). Its 47-odour data are published in Additional file 2 of
  [Schmuker, de Bruyne, Hähnel & Schneider 2007, Chem Cent J 1:11](https://pmc.ncbi.nlm.nih.gov/articles/PMC1994056/).
  de Bruyne is a co-author.
- Schmuker: "we used the responses of Drosophila ORNs to 47 odorants that were measured by electrophysiological in vivo
  recordings in a previous study [18]", where [18] is de Bruyne et al. 2001.
- Additional file 2 caption: "Activity values (in spikes/s) and per-ORN thresholds. Spike rates of "active" odorants are
  set in bold in the respective column. Compounds in brackets have uncertain activity (i.e. spike rates between the
  upper and lower threshold)."
- DoOR gives de Bruyne 2001's concentration as 10⁻². Schmuker's own new recordings used the same method: "Most odorants
  were dissolved at 1% v/v in paraffin oil and air from a 5 ml syringe, containing 10 μl on a small piece of filter
  paper, was injected with a ca. 9-fold dilution factor [18]."

**Net spikes/s:**

| Neuron (glomerulus) | 3-octanol | 4-methylcyclohexanol | Lower / upper threshold |
|---|---|---|---|
| ab1D (DL1) | 2 | 7 | 20 / 30 |
| ab2A (DM4) | −2 | 0 | 20 / 30 |
| ab2B (DM5) | 7 | 3 | 10 / 20 |
| ab3A (DM2) | 57 | (13) | 10 / 30 |
| ab3B (VM5d) | 112 | 4 | 20 / 35 |
| ab5B (DM3) | 27 | −2 | 10 / 20 |
| ab6A (DC2) | 162 | −15 | 20 / 40 |

**The other eight classes**, via DoOR's Bruyne.2001.RR coded values:
- ab7A (Or98a, VM5v): OCT 79, MCH 0.
- ab1A (DM1), ab1B (VA2), ab4A (DL5), ab4B (DA2), ab5A (VA6), ab6B (VA5) and ab7B (VC4): 0 for both.

**Counts (derived).** Of the 15 ab1–ab7 classes:
- OCT clears the "active" upper threshold in 4 (ab3A, ab3B, ab5B, ab6A). ab7A also responds (coded 79).
- MCH clears none. Its largest response, 13 at ab3A, is "uncertain".

**Context.** ab8–ab10, where D, VA3, DM6 and DL4 live, were not part of this survey.

## 6. Other single-sensillum data

- **[Silbering et al. 2011, J Neurosci 31:13357](https://pmc.ncbi.nlm.nih.gov/articles/PMC6623294/).** Coeloconic
  sensilla.
  - Stimulus: "Odors (Sigma and Fluka) were diluted to 1% (v/v) unless otherwise noted in the figures".
  - "Corrected responses were quantified by counting all spikes recorded from an individual sensillum [because of
    difficulties in reliably distinguishing spikes from individual neurons (Yao et al., 2005)] during a 0.5 s window
    starting 150–200 ms after the stimulus trigger."
  - Values via DoOR, OCT then MCH: ac1 8.5 vs 29; ac2 15 vs −6; ac3 (Or35a knocked down, DoOR: "summed responses from
    the ac3 sensillum, Or35a was knocked down") 14 vs −0.5; ac4 −5 vs −15.1.
  - These are whole-sensillum sums, so they cannot be assigned to glomeruli. They say nothing about Or35a (VC3).
- **Dweck et al. 2013, Curr Biol.** Or19a/DC1, via DoOR: OCT 36, MCH 5 spikes/s, at 10⁻² (DoOR dataset info).
- **[Ronderos et al. 2014, J Neurosci 34:3959](https://pmc.ncbi.nlm.nih.gov/articles/PMC3951695/).** Or83c/DC3,
  via DoOR: OCT 10, MCH 17.
  - Or83c was expressed in at1 neurons.
  - "Odorants ... used to generate the tuning curves in Figure 2, A, B, and E, were undiluted to maximize the
    probability of a response."
  - "no other odorant in the panel produced >50 spikes/s even in undiluted form".
  - Grabe et al. 2016's table gives Or83c 3-octanol 9 and 4-methylcyclohexanol −1 (helper).
- **Kreher et al. 2005 / 2008 (larval receptors in the empty neuron) and Goldman et al. 2005 (palp).** Values via
  DoOR.
  - Their panels contain 3-octanol but not 4-methylcyclohexanol: Kreher 2008 lists 30 entries, Kreher 2005 32, and
    Goldman 2005 12.
  - [Kreher 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2496968/) says: "We have expressed all 25 genes in the empty
    neuron system and tested them with a diverse panel of odorants" and "We initially tested the odorants as "10 -2"
    dilutions". Its full text never mentions methylcyclohexanol.
  - They are the source of OCT's VC3, DM3 (Or47a), DA4m, DL4, VA4 and VM7v values.

## 7. ORN calcium imaging that tested both odours

- **Münch & Galizia 2016, Table S5** (helper; 10⁻² in mineral oil, 2 mL headspace, mean ΔF/F % ± SEM (n), solvent
  subtracted):

  | Receptor (glomerulus) | OCT | MCH | Reference odours |
  |---|---|---|---|
  | Or56a (DA2) | 0.38 ± 0.14 (9) | 1.87 ± 0.34 (9) | 2-hexanol 2.28; geosmin 17.59 ± 4.41 (4) |
  | Or69a (D) | 1.68 ± 0.47 (7) | 1.33 ± 0.27 (7) | isopentanoic acid 0.48 |
  | Or10a (DL1) | 0.52 ± 0.15 (7) | 0.53 ± 0.16 (9) | |
  | Or42b (DM1) | −0.47 ± 0.04 (5) | −0.18 ± 0.05 (5) | |
  | Or47b (VA1v) | −0.11 ± 0.09 (8) | 0.01 ± 0.08 (8) | |

- **Galizia, Münch, Strauch, Nissler & Ma 2010, Chem Senses 35:551** (helper; [PMC2924422](https://pmc.ncbi.nlm.nih.gov/articles/PMC2924422/)).
  - These are the new data behind DoOR's Galizia.2009.nmr and Nissler.2007 columns.
  - OrX-GAL4 > G-CaMP, imaged "through the intact antenna cuticle". The highest concentration was 10⁻² in mineral oil,
    with decadic steps below it.
  - Responses are normalised to a reference odour, which is "3-octanol (589-98-0) for dOr13a, 1-hexanol (111-27-3) for
    dOr67b, and 2,3-butanedione (431-03-8) for dOr92a."
  - So for Or67b/VA3, MCH = 1.17 and OCT = 0.37 times 1-hexanol. For Or13a/DC2, MCH = 0.42 times OCT, which conflicts
    with de Bruyne 2001's −15 spikes/s. For Or92a/VA2, both are about 0.02 times 2,3-butanedione.
- **Pelz, Roeske, Syed, de Bruyne & Galizia 2006, J Neurobiol 66:1544** (helper).
  - Or22a-GAL4 > cameleon. 104 odours at 10⁻² v/v in mineral oil, then decadic series.
  - Table 1, AL (DM2 ORN terminals) EC50s: 3-octanol −2.80 ± 0.06 (Hill 0.52); 4-methylcyclohexanol −2.15 ± 0.11 (Hill
    0.45).
  - Antenna, normalised response at 10⁻²: OCT 0.41 ± 0.11, MCH 0.33 ± 0.10.
  - At 10⁻², the Hill fits give R/Rmax OCT 0.72 and MCH 0.54 (derived by the helper). MCH reaches 0.75 of OCT at DM2.

- **[Barth et al. 2014, J Neurosci 34:1819](https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/)** (Fiala lab). ORN
  axon terminals in the antennal lobe; the same lab and odours as the PN data in §8.
  - Concentrations were balanced behaviourally: "we first adjusted the respective odorant concentrations so that the
    flies' naive odor preferences were completely balanced". From the Fig. 1B labels (helper): 3-octanol 1:500,
    MCH 1:750 in mineral oil.
  - Fig. 3A legend: "Odor-evoked changes in fluorescence emitted by the Ca 2+ sensor protein GCaMP3.0 over time, shown
    as false colors in 29 identified glomeruli, in response to the odorants MCH, 3-Oct, and 1-Oct. Gray lines indicate
    odor onset and offset. Values indicate mean; n = 6 animals." The driver is Or83b-Gal4. D, DL4, DL3, DA3, VA5 and VM4
    are not in the set. VM5d and VM5v are merged as "VM5", and VM7d and VM7v as "VM7".
  - **My reading** (fig., approx.):
    - Image: the 606 × 639 PMC image. Colour bar −31 to 97% at y 28–380 (x 571–577). Values come from a nearest-colour
      lookup.
    - Per glomerulus: the peak of a 3-column running median over a 5-row band, taken from odour onset to 1.5 s after
      offset. The odour runs 1–3 s, and the time ticks give 12.8 px/s. The odour-line columns are masked.
    - Pre-stimulus pixels read about 2.5%.
  - **Peaks (% ΔF/F):**
    - MCH: VA3 75, VC1 32, VM5 32, DC2 26, DC3 21, VC3 21, DM2 19, DC1 18, VM2 17, VA7 16, VA6 14, VC2 14. DL5 is
      inhibited to −30.
    - OCT: VC3 95, VM5 92, VM2 82, DM6 63, DM2 58, DM3 50, VC1 47, DC1 26, DC2 21, DC3 21, VM3 21, VM7 21, DM5 17. DL1 is
      inhibited to −18 and DM4 to −20.
  - **Totals (derived):**
    - Σ(peak − 8)₊: MCH 211 vs OCT 509 (0.41). The helper's independent reading gives 217 vs 510 (0.43).
    - Σ(peak − baseline)₊: 320 vs 624 (0.51).
    - Glomeruli ≥ 40% above baseline: OCT 7, MCH 1.
  - **Text:** "1-Oct and 3-Oct both evoked strong Ca 2+ activity in a largely overlapping subset of glomeruli ... On the
    other hand, MCH induced a relatively more distinct activity pattern".
  - **Imaging and single-sensillum data disagree in places.** MCH shows weak signals in VM5, DC1 and DC2, where
    single-sensillum recordings show MCH ≤ 5 spikes/s or inhibition (ab3B 4, Or19a 5, ab6A −15). And OCT's DC2 imaging
    signal (21%) is small next to ab6A's 162 spikes/s. GCaMP3 saturation and spread from neighbouring glomeruli could
    both contribute; not resolved.
- **[Churgin et al. 2025, eLife](https://pmc.ncbi.nlm.nih.gov/articles/PMC11896609/)** (helper). Orco > GCaMP6m.
  - "Saturated headspace from 40 ml vials containing 5 ml pure odorant were serially diluted via carbon-filtered air to
    generate a variably (10–25%) saturated airstream".
  - Only DM1, DM2, DM3, DL5 and DC2 were analysed. These all prefer OCT.
  - Peak Δf/f (Fig. 1G, fig., approx.): DM2 OCT 1.06 vs MCH 0.50; DM3 0.51 vs 0.09; DC2 0.34 vs 0.09. Air alone gives
    DM2 0.32 and DM3 0.20.
  - Air-subtracted sum over the five glomeruli: OCT 1.41, MCH 0.27 (derived).

## 8. Projection neuron and glomerular responses

- **[Badel, Ohta, Tsuchimoto & Kazama 2016, Neuron 91:155](https://doi.org/10.1016/j.neuron.2016.05.022).** Table S2:
  <https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc2.xls>, re-extracted by me.
  - **Setup** (helper):
    - NP225-Gal4 > GCaMP6f, in vivo two-photon imaging, 37 glomeruli, 4-s odour, n = 4–9 brains.
    - Table S1: "3-octanol 32 oil 10-2 Tokyo chemical industry P2" and "4-methylcyclohexanol 31 oil 10-2 Sigma-Aldrich
      P2".
    - Delivery: "The air stream (250 ml/min) was split into 16 parallel channels … pooled, mixed into the main air
      stream (1.55 l/min)".
    - Endo et al. 2020 used the same olfactometer and describes the result as "merged with a main air stream
      (1,550 ml/min) to a dilution of 1.4 × 10^3".
  - **Mean ΔF/F (%), both odours sorted by OCT:**

    | Glomerulus | DM6 | DM3 | VM2 | DL3 | D | DA2 | VM3 | DA1 | DA3 | VM7v | DM2 | DC3 | DC2 | DM5 | VM4 | DL5 | VM1 | VC1 | VA2 |
    |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
    | OCT | 278 | 219 | 171 | 166 | 146 | 140 | 122 | 118 | 113 | 106 | 97 | 86 | 74 | 53 | 48 | 38 | 36 | 36 | 32 |
    | MCH | 88 | 87 | 34 | 91 | 172 | 236 | 72 | 78 | 116 | 121 | 42 | 101 | 20 | 43 | 10 | 77 | 24 | 51 | 19 |

    | Glomerulus | DL1 | DL4 | VM7d | VA6 | VA7m | VA4 | VA5 | VA3 | DA4l | DM4 | VC2 | VA7l | DP1m | DM1 | VA1d | VL2a | VL2p | VA1v |
    |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
    | OCT | 27 | 26 | 26 | 25 | 25 | 21 | 19 | 18 | 15 | 12 | 12 | 12 | 10 | 9 | 7 | −1 | −10 | −33 |
    | MCH | 37 | 97 | 84 | 69 | 16 | 21 | 110 | 108 | 96 | 23 | 40 | 26 | 15 | 14 | 50 | −1 | −3 | 17 |

  - **Significant responses** (Fig. 2D white dots, Mann–Whitney p < 0.01, read from the figure by the helper):
    - OCT: 13 excitatory (DM6, DM3, VM2, DL3, D, DA2, VM3, DA1, DA3, VM7v, DM2, DC3, DC2) plus inhibition of VA1v.
    - MCH: 18 (DA2, D, VM7v, DA3, VA5, VA3, DC3, DL4, DA4l, DL3, DM6, DM3, VM7d, DA1, DL5, VM3, VA6, VC1).
  - **Totals (derived):**
    - Positive sum over 37 glomeruli: OCT 2346, MCH 2305 (MCH/OCT 0.98).
    - Glomeruli > 50%: OCT 14, MCH 19. Glomeruli > 100%: OCT 10, MCH 7.
    - Rank among the 84 stimulus rows of Table S2 (single odours, mixtures and dilutions): OCT 4th, MCH 6th. The first
      is ethyl butyrate at 3647.
    - Restricted to the eight of the model's OCT glomeruli that NP225 covers (D, DC2, DM3, VA4, DM2, DM6, DA2, VM7v):
      OCT 1081, MCH 787 (0.73; helper's arithmetic).
  - **Glomeruli missing from the set.** NP225 does not cover VM5d, VM5v, VC3 or DC1. Those are OCT's strongest
    targets by single-sensillum recording (ab3B, ab7A, Or35a, Or19a), so OCT's true PN total is above 2346.
  - **No concentration series** for OCT or MCH in Table S2. Only vinegar, benzaldehyde, mango mimic and 2-methylphenol
    were diluted.
  - **Comparison with DoOR.**
    - MCH's PN responses agree in direction with the Galizia-lab ORN imaging (§7): DA2 236 vs OCT 140, D 172 vs 146,
      VA3 108 vs 18. Barth's ORN imaging shows no DA2 response to either odour.
      They also agree with de Bruyne 1999's palp recordings: VM7d 84 vs 26 and VC2 40 vs 12.
    - OCT is stronger, again matching the single-sensillum data, at DC2 (74 vs 20), DM2 (97 vs 42) and DM3 (219 vs 87).
    - Some MCH PN responses come from ORN classes that showed MCH ≈ 0 in de Bruyne 2001: DL5 (ab4A), VA6 (ab5A), VA5
      (ab6B) and DM3 (ab5B). They may be PN amplification of sub-threshold ORN input or lateral excitation, rather than
      direct ORN drive. The coded "0" may also hide responses of up to roughly 20 spikes/s; not verified.
- **Pech et al. 2015, Cell Rep 10:2083** (Fiala lab; helper).
  - "Throughout the study, MCH was diluted 1:750, 3Oct 1:500 in mineral oil".
  - "OPNs innervating DL4 respond to both MCH and 3Oct". The paper also mentions "glomeruli DC1, DM3, and DL5, which
    respond to MCH, 3Oct, and apple and banana, respectively".
  - One focal-plane example (Fig. 4E, fig., approx., by the helper):
    - MCH: DL4 ≈ 125, DM3 ≈ 51, DM2 ≈ 39, DA3 ≈ 29, DL5 ≈ 29.
    - OCT: DM6 ≈ 146 (saturated), DL4 ≈ 94, DM3 ≈ 61, DM2 ≈ 18, DA3 ≈ 18.
- **Barth et al. 2014, PNs** (same paper as §7). GH146 > GCaMP3, "18 identified glomeruli", n = 20 (Fig. 5A).
  - **My reading** (fig., approx.): the 640 × 565 PMC image, colour bar −20 to 260% at y 29–261 (x 602–609), time
    ticks at 13.9 px/s, odour 1–3 s. The method is otherwise as in §7.
  - **Peaks (% ΔF/F):**
    - MCH: VM4 241, DL4 218, DM6 198, VC2 168, DM2 166, DM5 162, VM1 161, DC1 109, DA2 44, VM2 27.
    - OCT: DA2 256, DM1 256, DM2 209, DC1 196, DL4 172, DM5 171, VM2 171, VM1 161, DM6 128, DP1 39.
  - **Totals (derived):** Σ(peak − 10)₊ is MCH 1428 vs OCT 1680 (0.85). The helper's reading gives 1435 vs 1696 (0.85).
    Glomeruli ≥ 100%: MCH 8, OCT 9.
  - **The ORN-to-PN equalisation.** In one lab, with one stimulus, MCH goes from 0.41–0.51 of OCT at the ORNs to 0.85
    at the PNs.
  - **Disagreements with Badel.** The two labs' PN patterns differ widely for MCH: VM4 241 vs 10 and VC2 168 vs 40.
    DA2 is MCH's strongest PN glomerulus in Badel (236 vs OCT 140), but in Barth it is OCT's (256 vs 44). VA3 is not in
    Barth's GH146 set.
- **Yu, Ponomarev & Davis 2004, Neuron 42:437** (helper; read from the SDB Interactive Fly reproduction because the
  primary text was blocked). Synapto-pHluorin in PNs, 8 identified glomeruli.
  - "Four of the eight glomeruli were activated reproducibly by OCT": DM6, DM2, DM3 and DL3.
  - "PNs innervating the three glomeruli DM6, DM2, and DM3 exhibited significant responses to MCH alone". MCH responses
    "were more variable between flies than for OCT".
  - Concentrations: Not reported in the accessible text.
- **Churgin et al. 2025, PNs** (helper; GH146 > GCaMP6m, five glomeruli, 10–25% saturated vapour). Air-subtracted sum:
  OCT 2.59 vs MCH 0.75, in five glomeruli that all prefer OCT (derived).
- **Hussain et al. 2018, eLife** (helper). OCT at 12 mM: DC2, DM6 and DP1 responsive. MCH at 16 mM: DC1, DP1 and VC2.
- **[Prisco et al. 2021, eLife 10:e74172](https://pmc.ncbi.nlm.nih.gov/articles/PMC8741211/)** (helper). PN boutons
  in the calyx, odours at 1:100 in mineral oil.
  - "While the number of active boutons was similar between Mch and Oct stimulations (Figure 3D, n = 10, p = 0.689,
    paired t-test), the average response peak among active boutons was higher when flies were exposed to Oct (Figure 3B,
    n = 10, p = 0.0002, paired t-test)."
  - Readings (fig., approx.): active boutons MCH 26.8 vs OCT 27.4 (0.98); peak ΔF/F₀ 115 vs 166 %max (0.69).
- **Wang, Wong, Flores, Vosshall & Axel 2003, Cell 112:271** (helper).
  - Ex vivo explant, air dilution of saturated vapour. MCH is not in the panel; cyclohexanol and cyclohexanone are.
  - 3-octanol (fig., approx.): no glomerulus at 2% saturated vapour; DM1 at 5–10%; DM1 and DC2 at 20%; five glomeruli
    at 40% (VM2, DM2, DM1, DM6, DC2).
  - Their glomerulus set lacks VM5d, VM5v, VC3, VA4 and VM7v.
- **No OCT/MCH glomerular identities** (helper): Ng et al. 2002 (fruit odours); Fiala et al. 2002 ("octanol",
  glomeruli not identified); Parnas et al. 2013; Wilson et al. 2004 (3-octanol only); Silbering & Galizia 2007;
  Silbering et al. 2008; Strutz 2014; Mohamed 2019; Knaden 2012; Seki 2017; Hong & Wilson 2015; Bhandawat 2007;
  Olsen 2010; Root 2007.
- **Endo et al. 2020** (Neuron 108:367) imaged both odours in 37–47 glomeruli with Badel's olfactometer, but the data
  are "available from the corresponding author on request".

## 9. Kenyon cells

Read by the helper unless marked otherwise.

- **Hige et al. 2015, Neuron 88:985** ([PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/)). This is the
  only dataset at Hige's own stimulus.
  - Imaging: GCaMP6f in all KCs (R13F02-LexA), "82 ± 9 cells per fly, mean ± SD; n = 7". A cell counted as responsive
    above 2.33 SD on at least half of the trials.
  - Fig. 2E legend: "CS+ (OCT; n = 53 cells from 5 flies) and CS− (MCH; n = 49)". MCH/OCT = 0.92 (derived).
  - "33 % of MCH-responding KCs and 30 % of OCT-responding KCs respond to both these odors". About 16 cells respond to
    both, about 86 to either, a Jaccard index of 0.19 (derived).
  - Responding fraction about 12.9% for OCT and 12.0% for MCH (derived; assumes 82 cells in each of the 5 flies).
  - In one representative fly (Fig. 2A–B, fig., approx.), MCH was broader than OCT: 27–28 vs 18–19 rows above 0.5 ΔF/F.
- **[Honegger, Campbell & Turner 2011, J Neurosci 31:11772](https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/).**
  - Stimulus: "saturated vapor from pure odorant was serially diluted in air to achieve a dilution ratio of 1:100".
  - "The odors 3-octanol and 4-methylcyclohexanol activate very different populations of KCs (Fig. 7D,E). Presented
    individually, each of these odors activates 9% of KCs on average. When presented simultaneously, however, this
    proportion increases only slightly (11%) and is smaller than the linear sum of the two activity patterns, 15%
    (Fig. 7A)."
  - Fig. 7A (fig., approx.; 1418.4 px per unit, n = 4 sections):

    | | Per section | Mean |
    |---|---|---|
    | MCH | 0.137, 0.095, 0.034, 0.019 | 0.0715 |
    | OCT | 0.143, 0.107, 0.082, 0.059 | 0.0975 |

    MCH/OCT = 0.73 (derived).
  - In one section's 45 strongest responders (Fig. 3C/D), 12 respond to OCT and 8 to MCH (0.67).
- **[Campbell et al. 2013, J Neurosci 33:10568](https://pmc.ncbi.nlm.nih.gov/articles/PMC3685844/).**
  - OCT and MCH response fractions are Not reported.
  - Pattern correlation for pure OCT against pure MCH (Fig. 3B, n = 11, fig., approx.): r = 0.217, 95% CI
    0.076–0.356.
- **[Lin et al. 2014, Nat Neurosci 17:559](https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/).**
  - Stimulus: "Odors at 10−2 dilution were delivered ... The flow rate at the fly was 0.5 l/min".
  - Population sparseness of pixel maps in control groups (Suppl. Fig. 8, fig., approx.):

    | Control group | SP, MCH | SP, OCT |
    |---|---|---|
    | 1 | 0.982 | 0.971 |
    | 2 | 0.969 | 0.956 |
    | 3 | 0.940 | 0.916 |

  - Taking 1 − SP as the active fraction, MCH/OCT is 0.61–0.71 (derived). The map correlation r(MCH, OCT) is
    0.04–0.11.
- **Prisco et al. 2021.** KC claws (fig., approx.): 19.4 responding for MCH vs 20.0 for OCT (0.97, p = 0.727). Peak
  138 vs 150 (0.92).
- **Ahmed et al. 2023.** Control flies (fig., approx.): OCT 0.359, MCH 0.246 (0.69). Mineral oil alone scores 0.335 by
  the same 0.2 ΔF/F criterion, so this is not comparable with the rest.
- **No per-odour OCT/MCH fractions:** Turner, Bazhenov & Laurent 2008 (both odours in the panel at 1:1000; only
  "6 ± 5%" overall); Murthy et al. 2008 and Inada et al. 2017 (neither odour tested).

## 10. Physical: vapour pressures and molecules delivered at "2% of saturated vapor"

**Hige's stimulus**, as quoted in `mbon11_input.md`: "40-ml vials were loaded with 5-ml pure odorants, and the saturated
headspace vapors were diluted by two steps of air dilutions down to 1% (odor generalization experiments) or 2% (the
rest of the experiments). Final flow rate of the air stream was set to 1 L/min".

**3-octanol** (CAS 589-98-0, MW 130.23, density about 0.82).
- NIST WebBook Antoine equation, from Geiseler, Fruwert & Hüttig 1966 ("Coefficents calculated by NIST from author's
  data"), valid 283–353 K: log₁₀(P/bar) = 4.8465 − 1663.322/(T − 97.47).
- That gives 0.166 mmHg at 20 °C, 0.203 at 22 °C and 0.271 at 25 °C (derived). The slope gives ΔvapH ≈ 70 kJ/mol at
  298 K (derived).
- DoOR's `odor.csv` VP.25 column gives 0.26 mmHg.
- EPA CompTox predictions: TEST 0.231, OPERA 0.257, ACD/Percepta 0.512 mmHg. The Good Scents Company's 0.512 is the
  ACD estimate.
- A supplier value of "1 mm Hg at 20 °C" (ChemicalBook/Sigma, from search snippets) is 6 times the NIST-derived value.
  I disregard it.
- PubChem has no vapour-pressure record for 3-octanol.

**4-methylcyclohexanol** (CAS 589-91-3, cis/trans mixture, MW 114.19, density about 0.914).
- PubChem gives "0.29 [mmHg]" from Haz-Map, without a temperature. DoOR's VP.25 column also gives 0.29.
- CompTox predictions: OPERA 0.380, TEST 0.408, ACD 0.475 mmHg.
- NIST lists no vapour-pressure equation. It gives the boiling point (445.2 K, Aldrich) and
  ΔvapH°(298 K) = 65.9 kJ/mol (Chickos et al. 1995).
- Supplier snippets of "1.5 mmHg at 30 °C" and "4.5 hPa at 20 °C" contradict each other. They are also implausible:
  cyclohexanol boils 11 °C lower and has only 0.657 mm Hg at 25 °C (PubChem). I disregard them.
- Plausibility check (PubChem): 2-octanol (bp 179 °C) 0.242 mmHg at 25 °C; 1-octanol (bp 195 °C) 0.0794. Both
  odours boil at about 172–176 °C.

**Ratio (derived).**
- Saturated vapour concentration OCT/MCH = 0.271/0.29 = 0.93 with the best-documented values. Across the predicted
  values the range is 0.57–1.08.
- At 2% of saturation and 25 °C that is about 7.1 ppm OCT and about 7.6 ppm MCH.
- So Hige's stimulus delivers about the same number of molecules of each. MCH/OCT is 1.07 with the best-documented
  pair and 0.93–1.75 across all sources. MCH is not under-delivered.

**Oil dilutions.**
- At equal v/v in oil, MCH supplies 8.00/6.30 = 1.27 times as many moles as OCT (derived).
- The single-sensillum and imaging comparisons at 10⁻² therefore do not handicap MCH either.
- Exactly how a 10⁻² paraffin-oil dilution relates to a percentage of saturated vapour was not established. It depends
  on activity coefficients and the delivery dilution.

## 11. How the labs chose OCT and MCH concentrations

Quotes from the helper unless marked otherwise.

- **Hige et al. 2015 (Neuron).**
  - 2% of saturated vapour for both odours. No rationale is given in the main text or the supplement.
  - The behaviour supplement uses equal oil dilutions: "3-octanol (OCT; 1:1000; Merck) and 4-methylcyclohexanol (MCH;
    1:1000; Sigma–Aldrich)".
- **Hige, Aso, Rubin & Turner 2015 (Nature).** KCs imaged at 10% or 5% of saturated vapour.
- **Honegger 2011.** 1:100 saturated vapour for every odour.
- **Campbell 2013.**
  - "Experiments were conducted at an odor dilution of 1:100 or, where appropriate, adjusted to match the
    concentrations used behaviorally. We used a photo-ionization detector (Aurora Scientific) to match concentrations
    between the imaging rig and the T-maze".
  - "Pure odors were diluted in mineral oil and their concentrations adjusted so that flies exhibited no bias to either
    odor (MCH, 1.5:1000; OCT, 1:1000)."
  - So balancing behaviour took 1.5 times more MCH than OCT in the oil.
- **Others.**
  - Chen et al. 2026 used MCH at 1.33 times OCT (imaging 1:37.5 vs 1:50; behaviour 1:375 vs 1:500), with no reason
    given.
  - Lin 2014, Ahmed 2023 and Davidson 2023 (Hige lab) used equal dilutions (helper).
- **Pech et al. 2015.** MCH 1:750, OCT 1:500 in mineral oil. No reason quoted (helper).
- **Barth et al. 2014.** The same 1:750 vs 1:500, chosen so that "the flies' naive odor preferences were completely
  balanced".
- **Churgin et al. 2025.** "dilution factors for odorants were adjusted on a week-by-week basis to ensure that the mean
  preference was approximately 50%" (helper).
- **[Niewalda et al. 2011, PLoS One 6:e24300](https://pmc.ncbi.nlm.nih.gov/articles/PMC3170316/).** Adult flies,
  balanced for learnability rather than preference.
  - Fig. 1 legend: "Note that while asymptotic learning scores do not differ between dilutions, the dilutions at which
    that asymptote is reached differ between odours across almost two orders of magnitude. Dilutions for further
    experiments are chosen such that learning indices are the same and, for each kind of odour, have just about reached
    asymptotic levels (stippled grey line and grey arrows) (B: 1∶66; O: 1∶1000; M: 1∶25; A: 1∶1000)."
  - So equal learnability needed MCH 40 times more concentrated than OCT in oil.
- **Summary.** "Balanced" MCH : OCT oil ratios range from 0.67 (Barth, Pech) to 1.5 (Campbell) to 40 (Niewalda),
  depending on the task and the setup. None of the papers checked here balanced the odours physiologically.

## For the model

1. **Where the gap is.** In flies, MCH/OCT is:

   | Stage | MCH/OCT | Source |
   |---|---|---|
   | ORNs, summed response | ≈ 0.45 | Barth ORN imaging 0.41–0.51; DoOR 0.45; single sensilla about 0.15 (ab1–ab7, pb1, Or19a, Or83c) |
   | PNs | 0.85–0.98 | Barth 0.85; Badel 0.98, with MCH broader (18 vs 13 glomeruli) |
   | KCs | 0.73–0.92 | 0.92 at Hige's 2% saturated vapour |
   | MBON11 | ≈ 0.93 in spikes, ≈ 1.06 in charge | Hige 2015 |

   - DoOR's input already looks like real ORNs.
   - The model's KCs (≈ 0.25) and MBON11 (0.31) fall below even the ORN ratio. So the model loses ground for MCH
     between ORNs and KCs, exactly where flies gain it.
   - That points mainly at the model's antennal-lobe transform (and possibly APL normalisation in the mushroom body),
     not at the ORN table.
2. **ORN-level input changes the data support.** These are small (derived).
   - Treat untested receptors as unknown, not zero. 13 mapped receptors were never tested with MCH. Eight (Or9a, Or23a,
     Or43a, Or43b, Or65a, Or67d, Or85f, Or88a) were never tested with either odour.
   - Fill from Barth's ORN imaging only where no single-sensillum MCH data exist:

     | Odour | Glomerulus | DoOR units |
     |---|---|---|
     | MCH | VC1 (Or33c/Or85e) | 0.10–0.25 |
     | MCH | VC3 (Or35a) | 0.09–0.16 |
     | MCH | VM2 (Or43b) | ≈ 0.12 |
     | MCH | VA7 | ≈ 0.12 |
     | OCT | VM2 | ≈ 0.69 |

   - Conversion: either OCT's DoOR value scaled by the MCH/OCT ΔF/F ratio, or 0.0087 DoOR units per % ΔF/F. The latter
     is the median of 10 glomerulus–odour anchors; the anchors range 0.0034–0.032.
   - Result: MCH 3.3–3.5 against OCT 7.1, a ratio of 0.46–0.49. The input stays ORN-like.
   - Where imaging and single-sensillum recordings conflict (VM5, DC1, DC2), keep the single-sensillum values.
   - DA2's OCT drive (0.241) conflicts with single-sensillum zeros at ab4B. Münch's imaging (0.38% ΔF/F) and both PN
     datasets (Badel 140, Barth 256) show OCT reaching DA2, so leave it.
3. **The main fix: make the antennal lobe equalise as flies' does.**
   - Flies turn an ORN ratio of about 0.45 into 0.85–0.98 at the PNs.
   - The standard account is a compressive PN input–output function combined with divisive normalisation by total ORN
     input (Olsen et al. 2010). That boosts weak, broad inputs relative to strong, focused ones.
   - Checks to run on the model (none were run here):
     - (a) Summed PN rate, and the number of PN types above threshold, for MCH vs OCT.
     - (b) The PN response to a 10–30 Hz ORN increase in one glomerulus. Flies' PNs respond strongly to weak ORN input.
     - (c) Whether lateral inhibition scales with total ORN input.
     - (d) Whether APL feedback compresses the KC difference.
4. **Targets for validation:**
   - PNs: summed MCH/OCT 0.85–0.98, with MCH active in at least as many glomeruli as OCT (Badel 18 vs 13).
   - KCs: MCH/OCT responders 0.73–0.92, with about 30% of responders shared (Jaccard ≈ 0.19).
   - MBON11: about 0.93 in spikes.
5. **Stopgap if the antennal lobe cannot be fixed: drive the ORNs at PN-matched strength.** Label this as a stand-in for
   normalisation, not as ORN data.
   - **(a) Fill from Badel's PN data.** Fill Badel's significant glomeruli that lack ORN data, converted at 0.0028
     DoOR units per % PN ΔF/F. That is the median over 10 anchors (OCT at DM6, DA2, VM7v, DM3, DM2, D, DC2; MCH at DA2,
     D, VA3); the anchors range 0.0012–0.0081.

     | Odour | Glomeruli filled (DoOR units) | Summed drive |
     |---|---|---|
     | MCH | VM7v 0.34, DA3 0.32, DL4 0.27, DA4l 0.27, DL3 0.25, DM6 0.25, DA1 0.22, VM3 0.20, VC1 0.14 | 2.85 → 5.12 (12 glomeruli > 0.2) |
     | OCT | VM2 0.48, DL3 0.47, VM3 0.34, DA1 0.33, DA3 0.32 | 6.41 → 8.35 (17 > 0.2) |

     - Ratio 0.61, or 0.52–0.83 across the anchor range.
     - Also raising MCH's weakly measured glomeruli (VA5 0.31, DC3 0.28, DM3 0.24, VM7d 0.23, DL5 0.22, VA6 0.19) gives
       6.35/8.54 = 0.74. But single-sensillum recordings show those ORNs (ab6B, ab4A, ab5A, ab5B) barely respond to MCH.
   - **(b) Scale MCH's drive by about 2**, to 0.9 × OCT's summed 6.41, capping each glomerulus at 1.0 (VA3 would
     exceed it). This keeps MCH concentrated in VA3, D, DA2 and DM2, while PNs show 18 glomeruli. KC recruitment depends
     on how many PN types are co-active, so (a) is the better stopgap.
6. **Unresolved.**
   - Both ΔF/F-to-DoOR conversions are single linear factors for non-linear calcium signals. Their anchors vary 7- to
     9-fold.
   - Badel's set lacks VM5d, VM5v, VC3 and DC1 (strong OCT glomeruli), so the PN-level MCH/OCT is probably below
     0.98. Barth's PN 0.85 includes DC1, but not VM5d, VM5v or VC3.
   - The two PN datasets disagree glomerulus by glomerulus (DA2, VM4, VC2) while agreeing on totals.
   - No study gives ORN-level MCH responses for Or35a (VC3), the palp pb2/pb3 neurons (VC1, VA7l, VM7v, VA4), Or67a
     (DM6), Or43a (DA4l), Or23a (DA3), Or65a (DL3), Or67d (DA1) or Or9a (VM3) by single-sensillum recording.
   - No study gives a PN-level concentration series for either odour. Wang 2003 saw no PN glomerulus respond to
     3-octanol at 2% saturated vapour ex vivo.
   - Settled: the direction and size of the downstream targets. MCH ≈ OCT at PNs, and 0.73–0.92 at KCs at Hige-like
     concentrations. Also settled: the summed ORN-level ratio is about 0.4–0.5, lower (about 0.15) in the classes
     recorded by single sensillum.
   - Not settled: the exact ORN rates for MCH's untested receptors, and which antennal-lobe mechanism the model is
     missing.

## Sources

- Münch D, Galizia CG (2016) DoOR 2.0. Sci Rep 6:21841. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4766438/>. Data:
  <https://github.com/ropensci/DoOR.data> (`door_response_matrix.csv`, `door_mappings.csv`, `door_dataset_info.csv`,
  `door_excluded_data.csv`, `door_response_range.csv`, `odor.csv`, per-receptor CSVs; `man/odor.Rd`).
- Hallem EA, Carlson JR (2006) Cell 125:143. Supplement:
  <https://ars.els-cdn.com/content/image/1-s2.0-S0092867406003631-mmc1.pdf>.
- Hallem EA, Ho MG, Carlson JR (2004) Cell 117:965. Via DoOR.
- de Bruyne M, Clyne PJ, Carlson JR (1999) J Neurosci 19:4520. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6782632/>.
- de Bruyne M, Foster K, Carlson JR (2001) Neuron 30:537. Paywalled. Data via Schmuker et al. 2007 and DoOR. Figures
  at `https://ars.els-cdn.com/content/image/1-s2.0-S0896627301002896-gr{1,3,6,7}_lrg.jpg` (the 47-odour figure is not
  among them).
- Schmuker M, de Bruyne M, Hähnel M, Schneider G (2007) Chem Cent J 1:11.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC1994056/>. Additional file 2:
  <https://static-content.springer.com/esm/art%3A10.1186%2F1752-153X-1-11/MediaObjects/13065_2007_11_MOESM2_ESM.pdf>.
- Silbering AF et al. (2011) J Neurosci 31:13357. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6623294/>.
- Ronderos DS et al. (2014) J Neurosci 34:3959. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3951695/>.
- Dweck HKM et al. (2013) Curr Biol 23:2472; Kreher SA et al. (2005) Neuron 46:445; Goldman AL et al. (2005) Neuron
  45:661; Stensmyr MC et al. (2012) Cell 151:1345. All via DoOR.
- Galizia CG, Münch D, Strauch M, Nissler A, Ma S (2010) Chem Senses 35:551.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2924422/>.
- Pelz D, Roeske T, Syed Z, de Bruyne M, Galizia CG (2006) J Neurobiol 66:1544. Konstanz repository PDF (helper).
- Badel L, Ohta K, Tsuchimoto Y, Kazama H (2016) Neuron 91:155. Table S2:
  <https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc2.xls>.
- Pech U et al. (2015) Cell Rep 10:2083. <https://ars.els-cdn.com/content/image/1-s2.0-S2211124715002429-mmc4.pdf>.
- Prisco L et al. (2021) eLife 10:e74172. <https://pmc.ncbi.nlm.nih.gov/articles/PMC8741211/>.
- Wang JW, Wong AM, Flores J, Vosshall LB, Axel R (2003) Cell 112:271.
  <https://www.rockefeller.edu/research/uploads/www.rockefeller.edu/sites/8/2018/09/WangAxel03.pdf>.
- Endo K, Tsuchimoto Y, Kazama H (2020) Neuron 108:367. doi:10.1016/j.neuron.2020.07.029.
- Barth J, Dipt S, Pech U, Hermann M, Riemensperger T, Fiala A (2014) J Neurosci 34:1819.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/>. Figures: PMC images `zns9991451160003.jpg` (Fig. 3, ORN) and
  `zns9991451160005.jpg` (Fig. 5, PN).
- Churgin MA et al. (2025) eLife 12:RP90511. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11896609/> (helper).
- Yu D, Ponomarev A, Davis RL (2004) Neuron 42:437. Read via the SDB Interactive Fly reproduction,
  <https://www.sdbonline.org/sites/fly/aignfam/mushroom.htm> (helper).
- Hussain A et al. (2018) eLife 7:e32018. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5790380/> (helper).
- Niewalda T et al. (2011) PLoS One 6:e24300. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3170316/>.
- Kreher SA, Mathew D, Kim J, Carlson JR (2008) Neuron 59:110. <https://pmc.ncbi.nlm.nih.gov/articles/PMC2496968/>.
- Olsen SR, Bhandawat V, Wilson RI (2010) Neuron 66:287. <https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/>. Cited for
  the normalisation model only; not re-read here.
- Chen CC et al. (2026) Curr Biol 36:1633. <https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/> (helper; dilutions
  only).
- Hige T, Aso Y, Modi MN, Rubin GM, Turner GC (2015) Neuron 88:985. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/>.
- Honegger KS, Campbell RAA, Turner GC (2011) J Neurosci 31:11772. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/>.
- Campbell RAA et al. (2013) J Neurosci 33:10568. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3685844/>.
- Lin AC, Bygrave AM, de Calignon A, Lee T, Miesenböck G (2014) Nat Neurosci 17:559.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/>.
- Ahmed M et al. (2023) Curr Biol 33:2742. <https://pmc.ncbi.nlm.nih.gov/articles/PMC10529417/>.
- Turner GC, Bazhenov M, Laurent G (2008) J Neurophysiol 99:734.
- NIST Chemistry WebBook, 3-octanol: <https://webbook.nist.gov/cgi/cbook.cgi?ID=C589980&Mask=4>.
  4-Methylcyclohexanol: <https://webbook.nist.gov/cgi/cbook.cgi?ID=C589913&Mask=4> (cis C7731284, trans C7731295).
- PubChem: 4-methylcyclohexanol CID 11524 (vapour pressure from Haz-Map; ICSC 0296), 3-octanol CID 11527, cyclohexanol
  CID 7966, 2-octanol CID 20083, 1-octanol CID 957. <https://pubchem.ncbi.nlm.nih.gov/>.
- EPA CompTox predicted properties: DTXSID0060434 (4-methylcyclohexanol), DTXSID10862252 (3-octanol).
  <https://comptox.epa.gov/dashboard/>.
