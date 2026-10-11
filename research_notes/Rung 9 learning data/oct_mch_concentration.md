# 3-octanol and 4-methylcyclohexanol at Hige's 2% saturated vapour: which receptors respond, and how strongly

Read 2026-10-10. This builds on [oct_mch_input.md](oct_mch_input.md) (DoOR sources, PN data, vapour pressures),
[weak_input_gain.md](weak_input_gain.md) (§1 Olsen's transform, §8 equalization),
[hige2015_specificity.md](hige2015_specificity.md) and [lateral_excitation.md](lateral_excitation.md). Their content is
not repeated except where re-checked.

**Conventions** (as in those notes)
- Quotes are exact.
- "(fig., approx.)" = read off a figure with a pixel grid calibrated on its ticks or colour bar.
- "(derived)" = my arithmetic on published numbers.
- "Not reported" = searched the text, legends and supplement and did not find it.
- "(helper)" = read by one of three helper agents in this session and not re-checked by me. Everything I re-checked is
  stated without the tag.
- "(model)" = read from brainfly's stored outputs (`experiments/odor_probe54.json`) or connectome counts. No new
  simulation was run.
- DoOR-equivalent units: the model drives a glomerulus at value × 200 spikes/s.
- "SV" = saturated vapour of the pure odorant. Hige's stimulus is 2% SV.

## Summary

1. **Concentration does not explain OCT's breadth.**
   - Hige's 2% SV is about 5-7 ppm of OCT and about 7.6 ppm of MCH (`oct_mch_input.md` §10; helper).
   - Alcohols in mineral or paraffin oil are strongly non-ideal. At 1% v/v the headspace is 0.2-0.5 of SV, not about 1%:
     0.42-0.53 for C3-C7 n-alcohols (Jennings et al. 2023) and 0.23-0.28 for 4-heptanol, the closest secondary-alcohol
     analog measured (Cometto-Muñiz et al. 2003; derived).
   - So the "10⁻²" behind most of DoOR delivered roughly Hige's concentration (derived, each ×/÷ 2.5-5):
     - Carlson-lab single-sensillum and empty-neuron recordings: 0.8-2.2× Hige.
     - Dweck 2013: about 1.1×.
     - Badel's PN imaging: 2.1×.
     - Barth's ORN and PN imaging: 2.5-3.6×.
     - Galizia-lab antennal imaging (DoOR's D, VA3 and DA2 values; Pelz's DM2 EC50s): 7.5-15×.
   - Badel's air dilution is 1:7.2. The "×1/1.4×10³" figure comes from Endo et al. 2020, whose text reads "a dilution of
     1.4 × 10⁻³" (oil 10⁻² × air 1:7.2) with the minus sign lost in text extraction.
   - **Per glomerulus, the concentration change alone moves OCT's single-sensillum and empty-neuron entries by
     ×0.9-1.1** (DM6 ×0.7) **and the imaging-based entries by ×0.25-0.8** (MCH: VA3 ×0.80, D ×0.52, DA2 ×0.27; §1.5).
     MCH's main DoOR inputs are the imaging-based ones, so the correction lowers MCH more than OCT.
2. **Where DoOR is wrong, it is mostly wrong for other reasons** (§2.2).
   - **D:** DoOR stores Münch & Galizia's imaging without solvent subtraction. The mineral-oil response adds 0.226 to
     every odor (OCT 0.741 → 0.515, MCH 0.635 → 0.409).
   - **DA2:** DoOR's ab4B consensus has a floor of about 0.30 under all odors. OCT's 0.241 and MCH's 0.274 are mostly
     floor; the raw imaging gives MCH 0.106 and OCT 0.022 of geosmin's response.
   - **DoOR × 200 vs measured rates:** DC2 116 Hz vs 162 measured (too low); DC1 75 vs 36 (too high); DM3 94 (empty
     neuron) vs 27 in the native ab5B neuron.
   - **Empty-neuron-only entries** (DA4m, DL4, and the small VM7d, DM1, VA6 values) are not supported by native neurons.
     They fall to about zero at 10⁻⁴ (Kreher 2008), and larval neurons with the same receptors don't respond to either
     odor up to 10⁻⁴ in water (Si et al. 2019).
3. **Dose-response data exist for few of these receptors** (§1.3).
   - Both odors: Or22a/DM2 (Pelz 2006 EC50s) and larval Or35a, Or13a, Or47a/Or33b, Or67b (Si 2019).
   - OCT only: Or13a (Galizia 2010 EC50 10⁻³·⁵⁰; MCH never reached half-maximum), and Kreher 2008's 10⁻² and 10⁻⁴ for all
     21 larval receptors (helper). For example Or35a 83 → 7 net spikes/s, Or47a 108 → 0, Or13a 138 → 15.
   - None for ab3B, ab7A, Or19a, Or67a, Or85d or the other palp neurons.
4. **OCT's glomeruli at Hige's concentration.**
   - Real and strong: DC2, VM5d, VM5v, VM2, VC3, D, DM6, DM2.
   - Real, moderate: VA4, DM3, VM7v, DC1, VC1.
   - Weak or doubtful: DL4, DA4m, VA3, VM3, DM1, DL1.
   - Artifacts: DA2 (DoOR floor) and the PN-inferred pheromone glomeruli DA1 and DL3. Their receptors don't detect food
     odors, Barth's PNs there are flat, and Badel's respond to every strong odor (lateral input).
   - Badel's low OCT values in VA4, VC1 and DL1 are not evidence against OCT input. Those glomeruli report weakly in NP225
     imaging: VA4's largest response to any pure odor is 36% ΔF/F, and OCT's 21% is 0.58 of it.
5. **MCH's glomeruli.**
   - Real and strong: VA3.
   - Real, moderate: D.
   - Real but weak (0.03-0.1): VC3, VC1, VC2, DM2, VM2, DM6, VM7d, DC1. VC3 is new: larval Or35a responds to MCH with
     an EC50 only 2× above OCT's (Si 2019).
   - Probably real, but the receptors were never tested: DA4l (cyclohexanol and cyclohexanone are among Or43a's best
     ligands, and MCH is DA4l's strongest PN response in Badel) and DL4 (PN responses in three datasets).
   - Not real or negligible at the receptor: DA1, DL3, DL5 (ORNs inhibited), DM3, DC2 (single sensillum −15 spikes/s,
     against imaging signals), and VM7v and VA4. de Bruyne 1999's pb3 neurons responded significantly to only 3 of 16
     odorants, MCH among those tested.
6. **Recommended receptor-level input at Hige's 2% SV** ("For the model"):
   - OCT: summed drive 5.32, with 13 glomeruli above 0.1 (17 at ≥ 0.05).
   - MCH: summed drive 1.99, with 2 above 0.1 (4 at ≥ 0.1, 9 at ≥ 0.05).
   - MCH/OCT 0.37 (0.28-0.48 across the ranges). Flies' receptor neurons: 0.41-0.51 (Barth) at 2.5-3.6× Hige's
     concentration.
   - The current model input (DoOR plus both fill tiers) is 8.56 (22 glomeruli above 0.1) against 5.26 (16).
7. **Much of the PN-level breadth for MCH has no receptor behind it.** Of Badel's 18 significant MCH glomeruli, 7 have
   direct receptor evidence and 2 more have analog evidence (DA4l, DL4). The other 9 sit on receptors that don't respond
   to MCH (for VM7v, by inference from de Bruyne 1999's screen). For OCT, 9 of 13 have receptor evidence (§2.3).
8. **No PN data exist at Hige's exact protocol.** The only measurement at Hige's stimulus is Hige's own KC overlap: 30-33%
   of each odor's responders respond to both. Honegger et al. 2011 at 1% SV agree: 9% of KCs each, 11% for the mixture,
   15% for the union.
9. **The equalization flies show is mostly reproduced once like is compared with like** (§5).
   - Flies' PN ratios (Barth 0.85, Badel 0.98) are sums over glomerulus sets that lack OCT's strongest targets (VM5d,
     VM5v, VC3; Badel also DC1).
   - On the same sets the model's per-glomerulus ratio is already 0.86-0.93 (Badel's 37) and 0.76-0.82 (Barth's 18)
     (model; verified from probe54). Its reported 0.52-0.59 is a per-cell sum over every glomerulus.
   - With the recommended inputs, Olsen/Luo's equation (σ 12, m 0.05) gives 0.90 and 0.79 on those sets, with equal
     glomerulus counts above 20 Hz (derived).
   - Other mechanisms are small or point the other way:
     - lateral excitation is about equal for both odors;
     - measured glomerulus-specific inhibition slightly disfavours MCH (VA3 is among the most inhibitable glomeruli;
       Hong & Wilson 2015);
     - ORN kinetics favour OCT by at most about 1.2× (helper);
     - GCaMP has never been calibrated against PN spikes.
   - One unmeasured lever is large: broad inputs recruit more LN activity than narrow ones at equal total ORN input (Hong
     & Wilson 2015). If OCT recruited 1.25-1.5× the inhibition its total predicts, the summed PN ratio would rise from
     0.64 to 0.75-0.86 (DoOR inputs, all glomeruli; helper, derived).
10. **The model's real gap is at the Kenyon cells:** 0.25 against flies' 0.73-0.92. In flies, APL equalizes KC claw
    responses: MCH/OCT peak 0.89 with APL working against 0.65 with it silenced (Prisco et al. 2021; helper).

## 1. Concentration

### 1.1 What each DoOR value rests on

Every glomerulus where DoOR (spontaneous level subtracted) gives either odor more than about 0.1. Raw values are from the
DoOR.data per-receptor files (downloaded 2026-10-10). "net" = minus the spontaneous rate.
- DoOR stores Kreher 2008's empty-neuron values with the spontaneous rate added back: DoOR = Kreher's Table S1A + SFR for
  all 21 receptors (helper, checked by arithmetic). Net values from Table S1A are used here.
- All receptor studies used 10⁻² (1% v/v) in paraffin or mineral oil unless stated. How each delivered it is in §1.2.

| Glomerulus (receptor, neuron) | DoOR OCT / MCH | Study → raw value, OCT; MCH | Method | Dose-response data for these odors |
|---|---|---|---|---|
| D (Or69a, ab9A) | 0.741 / 0.635 | Münch & Galizia 2016 → 2.412; 2.068 % ΔF/F (Table S5, net of solvent: 1.68 ± 0.47; 1.33 ± 0.27, n = 7) | antennal GCaMP1.3 imaging through the cuticle | none |
| VM5d (Or85b, ab3B) | 0.676 / 0.080 | de Bruyne 2001 → 112; 4 net spikes/s. Hallem 2004 → 245 (empty neuron), 254 (wild type), OCT only | single sensillum; empty neuron | none |
| VM5v (Or98a, ab7A) | 0.592 / 0.085 | de Bruyne 2001 category codes → 79; 0 | single sensillum | none |
| DC2 (Or13a, ab6A) | 0.579 / 0.078 | de Bruyne 2001 → 162; −15 net. Kreher 2008 → 138 net (OCT). Galizia 2010 → OCT the reference (1.0), MCH 0.42 | single sensillum; empty neuron; antennal imaging | Galizia 2010: OCT EC50 10⁻³·⁵⁰. Kreher 2008: 15 at 10⁻⁴. Larval Or13a: OCT EC50 10⁻⁶·²⁴, MCH none |
| DM3 (Or47a + Or33b, ab5B) | 0.468 / −0.002 | Kreher 2008 Or47a → 108 net (OCT). de Bruyne 2001 ab5B → 27; −2 net | empty neuron; single sensillum | Kreher 2008: 0 at 10⁻⁴. Larval Or33b/Or47a neuron: OCT 10⁻⁴·⁹⁸, MCH 10⁻²·⁴⁶ |
| VC3 (Or35a, ac3B) | 0.434 / not tested | Kreher 2008 → 83 net (OCT) | empty neuron | Kreher 2008: 7 at 10⁻⁴. Larval Or35a: OCT 10⁻⁴·¹⁷, **MCH 10⁻³·⁸⁷** |
| DC1 (Or19a, at3) | 0.374 / −0.048 | Dweck et al. 2013 → 36; 5 spikes/s | single sensillum | none |
| VA4 (Or85d, pb3B) | 0.369 / not tested | Goldman et al. 2005 → 81 (1% v/v). de Bruyne 1999 → 57.8 including SFR 9 (≈48 net, fig., approx.) | single sensillum | none |
| DM2 (Or22a, ab3A) | 0.337 / 0.254 | de Bruyne 2001 → 57; 13 net. Pelz et al. 2006 → EC50 only | single sensillum; AL imaging series | Pelz 2006: EC50 OCT 10⁻²·⁸⁰ (Hill 0.52), MCH 10⁻²·¹⁵ (Hill 0.45) |
| DM6 (Or67a, ab10A) | 0.319 / not tested | Hallem 2004 → 110 (empty neuron, OCT; spontaneous rate probably included) | empty neuron | none |
| DA2 (Or56a, ab4B) | 0.241 / 0.274 | Münch 2016 → 0.403; 1.889 % ΔF/F (geosmin 17.6). Stensmyr 2012 → −1.2 (OCT) | antennal imaging; single sensillum | none |
| VM7v (Or59c, pb3A) | 0.204 / not tested | Goldman 2005 → 46. de Bruyne 1999 → 40.6 including SFR 6 | single sensillum | none |
| VC1 (Or33c + Or85e, pb2A) | 0.153 / not tested | Goldman 2005 → Or33c 47, Or85e 41 (empty neuron); pb2A wild type 28 (Goldman), 11.6 including SFR 7 (de Bruyne 1999) | empty neuron; single sensillum | none |
| DA4m (Or2a, at3) | 0.133 / not tested | Kreher 2008 → 23 net (OCT) | empty neuron | Kreher 2008: 0 at 10⁻⁴ (Or2a not in Si 2019) |
| VA3 (Or67b, ab9B) | 0.123 / 0.876 | Galizia 2010 → OCT 0.37, MCH 1.17 × 1-hexanol. Kreher 2008 → 19 net (OCT) | antennal imaging; empty neuron | Kreher 2008: 1 at 10⁻⁴. Larval Or67b: MCH 10⁻⁴·²¹, OCT 10⁻³·³⁰ |
| DL1 (Or10a, ab1D) | 0.118 / 0.131 | de Bruyne 2001 → 2; 7 net. Münch 2016 → 1.009; 1.021 (Table S5: 0.52; 0.53) | single sensillum; antennal imaging | none |
| DL4 (Or49a + Or85f, ab10B) | 0.115 / not tested | Kreher 2008 → 31 net (Or49a, OCT) | empty neuron | Kreher 2008: 1 at 10⁻⁴. Larval Or49a: no response to either odor up to 10⁻⁴ |

The fills the model adds come from Barth et al. 2014's ORN imaging (OCT 1:500, MCH 1:750 in mineral oil) and, for the
PN-inferred tier, Badel 2016's PN imaging.

### 1.2 How each lab delivered "10⁻²", and how that compares with 2% SV

**The oil headspace is the dominant term.**
- The usual shorthand treats a 10⁻² oil dilution as about 1% of SV. Measured headspaces over alcohol solutions in
  mineral oil are 20-50 times higher.
- Jennings et al. 2023 (PID calibrated by full evaporation; Table 2, re-checked; power laws in % v/v): 1-propanol
  10,351·x^0.95 against an SV of 24,893 ppm; 1-butanol 4,716·x^1.02 against 8,837; 1-pentanol 1,572·x^0.93 against
  3,179; 1-hexanol 486.2·x^0.93 against 974; 1-heptanol 128.7·x^0.92 against 279. At 1% that is 0.42-0.53 of SV
  (derived). For comparison, hexyl acetate's 109.7·x^0.92 against 1,519 is 0.07.
- Cometto-Muñiz, Cain & Abraham 2003 (GC; re-checked): ppm at 1% in mineral oil = 429 for 1-hexanol, 60 for 1-octanol,
  10,947 for 2-butanol and 295 for 4-heptanol. With 4-heptanol's vapour pressure of 0.79-0.99 mmHg, its 295 ppm is
  0.23-0.28 of SV (helper, derived).
- Neither odor has been measured. The helper used 0.30 of SV (range 0.20-0.50) at 1% for both, scaling as
  concentration^0.86 below 1%.

**Air dilution and the result** (all derived by the delivery helper from each paper's flows; "× Hige" is the estimated
concentration at the antenna ÷ 2% SV, each ×/÷ about 2.5-5):

| Lab and studies | Delivery (numbers as in the papers) | Air dilution of the headspace | × Hige |
|---|---|---|---|
| de Bruyne 1999, 2001 (DoOR's ab and pb single-sensillum values) | 20 µl on filter paper in a 5-ml syringe; N₂ at 2 ml/s for 0.5 s into 35 ml/s | 1:18.5 | 0.8 (0.5-2.8) |
| Dobritsa 2003, Goldman 2005, Kreher 2005, 2008 (empty-neuron values) | 50 µl on a filter disc in a Pasteur pipette; 3.75 ml/s for 0.5 s into 37.5 ml/s | 1:11 | 1.2 (0.6-2.5) |
| Hallem 2004, Hallem & Carlson 2006 | same pipettes; 5.9 ml/s into 24 ml/s | 1:5.1 | 2.2 (1.0-6.1) |
| Dweck 2013 (Hansson lab) | Pasteur pipette into a continuous 1 l/min stream (Stökl 2010's method) | about 1:10 | 1.1 (0.4-2.5) |
| Badel 2016 (Kazama lab) | 250 ml/min bubbled through 4 ml of solution, merged into 1.55 l/min | 1:7.2 | 2.1 (1.2-3.5) |
| Barth 2014, Pech 2015 (Fiala lab) | about 1 ml/s through the odor vial itself (Riemensperger 2005) | 1:1 | OCT 3.6 (1.9-6.7), MCH 2.5 (1.3-4.8) |
| Münch & Galizia 2016 | 2 ml of headspace from sealed 20-ml vials, injected at 1 ml/s into 60 ml/min | 1:2 | 7.5 (4.5-12.5) |
| Galizia et al. 2010 | same autosampler, 2 ml of headspace in two 1-s pulses | 1:1-1:2 | 7.5-15 |
| Pelz et al. 2006 | "During stimulation (2 s) the constant air stream was interrupted ... and the autosampler injected 2 mL of headspace at a speed of 1 mL/s into the tube" | 1:1 | 15 (9-25) |
| Lin et al. 2014 (Miesenböck lab) | 10⁻² in oil (helper); 50 ml/min through the vial into a 450 ml/min carrier (Shang 2007's method) | 1:10 | 1.5 (0.9-2.5) |
| Honegger 2011, Campbell 2013 (Turner lab) | saturated vapour diluted 1:100 in air | | 0.5 |

- **Badel and Endo.** Badel's supplement: "The air stream (250 ml/min) was split into 16 parallel channels ... The outputs
  of all channels were pooled, mixed into the main air stream (1.55 l/min)". Opening 1 to 5 MCH-loaded channels gave the
  same PID signal (Fig. S7B), so the whole 250 ml/min passes through the open vials. Endo et al. 2020, same olfactometer:
  "merged with a main air stream (1,550 ml/min) to a dilution of 1.4 × 10⁻³". In the raw text the minus sign is a glyph
  (\x01) that is also the minus in the same paper's "p = 1.8 × 10⁻⁷". So 1.4 × 10⁻³ = 10⁻² (oil) × 250/1800 (air).
  This corrects the "1.4 × 10^3" quoted in `oct_mch_input.md` §8.
- **Hige's headspace is probably saturated.** Pure-odorant vials stayed saturated at flows up to 360 ml/min (MCH) and
  480 ml/min (OCT) in Claridge-Chang et al. 2009 (helper).
- **Depletion is small for these odors.** Andersson's thesis (the 2012 paper itself could not be obtained): OCT and MCH
  cartridges lose at most about 20% over the first 5-10 puffs (fig., approx.; helper).

**What this means.**
- DoOR's single-sensillum and empty-neuron values are at about Hige's concentration.
- Badel's PN pattern is at about twice it.
- DoOR's imaging values (D, VA3, DA2, the imaging parts of DL1 and DC2, and Pelz's DM2 EC50s) are at about 10 times it.

### 1.3 Dose-response data for these odors at these receptors

- **Kreher et al. 2008, Table S1, 3-octanol at 10⁻² and 10⁻⁴** (net spikes/s, 6 < n < 12; read from the supplement by the
  helper; the 10⁻² column reproduces DoOR exactly once SFR is added back).

  | Receptor (adult glomerulus) | 10⁻² | 10⁻⁴ |
  |---|---|---|
  | Or13a (DC2) | 138 ± 13 | 15 ± 5 |
  | Or47a (DM3) | 108 ± 15 | 0 ± 0 |
  | Or35a (VC3) | 83 ± 8 | 7 ± 6 |
  | Or42b (DM1) | 44 ± 6 | −2 ± 2 |
  | Or49a (DL4) | 31 ± 2 | 1 ± 1 |
  | Or42a (VM7d) | 27 ± 25 | −2 ± 2 |
  | Or2a (DA4m) | 23 ± 2 | 0 ± 2 |
  | Or67b (VA3) | 19 ± 3 | 1 ± 1 |
  | Or82a (VA6) | 14 ± 5 | −3 ± 5 |
  | Or85c (larval only) | 236 ± 15 | 128 ± 13 |

  - Legend (helper): "Mean spontaneous activity and mean response to solvent have been subtracted in each case. The data
    for the 10⁻² and 10⁻⁴ dilutions were collected separately".
  - A 100-fold dilution removes nearly all of OCT's empty-neuron responses (derived Hill coefficients about 0.6-1.0).
  - Mathew et al. 2013's Dataset S1 has an independent 10⁻⁴ column (helper): Or13a 38, Or42b 29, Or47a 14, Or67b 14,
    Or42a 13, Or35a 6, Or85c 169. MCH is not in their 479-odor panel.
- **Pelz et al. 2006, Or22a (DM2).** Re-checked: EC50 OCT 10⁻²·⁸⁰ ± 0.06, Hill 0.52; MCH 10⁻²·¹⁵ ± 0.11, Hill 0.45.
  - Hill coefficients "were all below 1 ... (0.53 ± 0.17; mean ± SD). These low Hill coefficient values correspond to a
    shallow dose-response curve that spanned about 3-4 log units".
  - Per-concentration values: Not reported.
- **Galizia et al. 2010, Or13a, Or67b, Or92a.** Concentration series were run, but only the 1:100 values are published
  (Table S3, helper): Or13a OCT 0.99, MCH 0.42; Or67b OCT 0.37, MCH 1.17; Or92a 0.02, 0.03.
  - DoOR's Or13a EC50 for OCT is 10⁻³·⁵⁰. MCH has none: it never reached half-maximum.
- **Si et al. 2019, larval ORNs.** Both odors at five concentrations (§1.4).
- **Hussain et al. 2018, DM6 PNs (GH146 > GCaMP3; helper, fig., approx.).** OCT 0 / 1 / 10 mM gave ≈12-13 / 41.5 / 46%
  ΔF/F in young flies. Concentration "mM" in the odor cup, solvent Not reported.
- **None** for ab3B (Or85b), ab7A (Or98a), Or19a, Or67a, Or85d, Or59c, Or59b, Or85a, the pb2 neurons, Or49b, or Or92a
  beyond Galizia's 1:100 values. Hallem 2004's concentration series used five other odorants (helper).

### 1.4 Si et al. 2019: larval receptor neurons, both odors at five concentrations

[Si et al. 2019, Neuron 101:950](https://pmc.ncbi.nlm.nih.gov/articles/PMC6756926/). Data from the authors' repository
(`samuellab/Larval-ORN`: `Figure2/data/Data S1.csv`, `Figure3/results/log_10_EC50.csv`); the averages and fractions are
mine (derived).
- All 21 larval ORNs were imaged together in a microfluidic device. Odorants were "diluted in deionized (DI) water", in
  five steps "from 10−8 dilution ... to 10−4 dilution". Both odors are in the 34-odor panel, n = 7 larvae each.
- Several of OCT's DoOR receptors are larval receptors whose DoOR values come from the empty-neuron screens, so this tests
  the same receptors with both odors in one preparation.
- Each value is the mean ΔF/F over 7 larvae as a fraction of that neuron's largest mean response to any of the 34 odors
  at any concentration:

| Receptor (adult glomerulus) | OCT 10⁻⁷ | 10⁻⁶ | 10⁻⁵ | 10⁻⁴ | log₁₀ EC50 (authors) | MCH 10⁻⁶ | 10⁻⁵ | 10⁻⁴ | log₁₀ EC50 (authors) |
|---|---|---|---|---|---|---|---|---|---|
| Or13a (DC2) | 0.10 | 0.38 | 0.72 | 0.71 | −6.24 | 0 | 0 | 0 | none |
| Or33b + Or47a (DM5, DM3) | 0.04 | 0.10 | 0.47 | 1.00 | −4.98 | 0.00 | 0.00 | 0.02 | −2.46 |
| Or35a (VC3) | 0.01 | 0.03 | 0.08 | 0.80 | −4.17 | 0.05 | 0.10 | 0.39 | −3.87 |
| Or67b (VA3) | 0.03 | 0.00 | 0.03 | 0.30 | −3.30 | 0.02 | 0.11 | 0.44 | −4.21 |
| Or42a, Or42b, Or49a, Or82a (VM7d, DM1, DL4, VA6) | 0 | 0 | 0 | 0 | none | 0 | 0 | 0 | none |

- The data file holds exact zeros for every larva at Or42a, Or42b, Or49a and Or82a. Undetected responses appear to be
  stored as 0, so "0" means below the authors' detection limit.
- MCH's Or35a values at 10⁻⁸-10⁻⁶ are noise from a few larvae with offsets. Its 10⁻⁴ response (1.82 ΔF/F, 0.39 of
  maximum) is real.
- **What this adds:**
  - **MCH drives Or35a (VC3)**, which no adult study tested. At equal aqueous dilution MCH gives 0.49 of OCT's response
    (0.39 vs 0.80 of maximum at 10⁻⁴), with an EC50 only 2× higher. Barth's adult ORN imaging agrees in direction (VC3:
    MCH 21% vs OCT 95% ΔF/F).
  - MCH is about 8× more potent than OCT at Or67b (VA3), as DoOR has it.
  - MCH barely drives Or13a (DC2) or the Or33b/Or47a neuron (DM3). This supports the single-sensillum zeros for MCH at
    ab6A (−15) and ab5B (−2) over the imaging signals at DC2.
  - Neither odor drives Or42a, Or42b, Or49a or Or82a up to 10⁻⁴. This agrees with the native adult neurons (pb1A about 6
    net; ab1A and ab5A coded 0) rather than with the empty-neuron responses at 10⁻².
  - Order of sensitivity to OCT: Or13a ≫ Or47a/Or33b > Or35a > Or67b.
- **Caveats.** The odor arrives in water, so the absolute EC50s do not transfer to air delivery. MCH is more
  water-soluble than OCT, which affects any comparison between the odors (qualitative; air-water partition coefficients
  for both were not found). The within-receptor comparisons and the rank order across receptors are the useful part.

### 1.5 Estimated response at Hige's concentration relative to the source value

The source value as a fraction of the receptor's maximum is moved by the concentration factor (Hige ÷ source, from §1.2)
through a Hill function with coefficient 0.7 (range 0.5-1.0; Kreher's two-point data imply about 0.6-1.0, Pelz's fits
0.53 ± 0.17). Derived. Receptor maxima are each study's largest response for that receptor.

| Odor | Glomerulus (source) | Source stimulus ÷ Hige | Source value ÷ receptor max | ×, central | range |
|---|---|---|---|---|---|
| OCT | DC2 (ab6A) | 0.8 (0.5-2.8) | 0.81 | 1.03 | 0.75-1.10 |
| OCT | DC2 (Or13a) | 1.2 (0.6-2.5) | 0.69 | 0.96 | 0.68-1.14 |
| OCT | VM5d (ab3B) | 0.8 (0.5-2.8) | 0.90 | 1.02 | 0.84-1.05 |
| OCT | VM5d (Or85b) | 2.2 (1-6.1) | 0.86 | 0.91 | 0.58-1.00 |
| OCT | VM5v (ab7A, category) | 0.8 (0.5-2.8) | 0.60 | 1.06 | 0.58-1.25 |
| OCT | VC3 (Or35a) | 1.2 (0.6-2.5) | 0.33 | 0.92 | 0.50-1.36 |
| OCT | DM6 (Or67a) | 2.2 (1-6.1) | 0.40 | 0.69 | 0.25-1.00 |
| OCT | DM2 (ab3A) | 0.8 (0.5-2.8) | 0.38 | 1.10 | 0.47-1.45 |
| OCT | VA4 (pb3B) | 0.8 (0.5-2.8) | 0.25 | 1.12 | 0.43-1.59 |
| OCT | VA4 (Or85d) | 1.2 (0.6-2.5) | 0.43 | 0.93 | 0.54-1.30 |
| OCT | DM3 (ab5B) | 0.8 (0.5-2.8) | 0.18 | 1.13 | 0.40-1.69 |
| OCT | DM3 (Or47a) | 1.2 (0.6-2.5) | 0.43 | 0.93 | 0.54-1.29 |
| OCT | DC1 (Or19a) | 1.1 (0.4-2.5) | 0.20 | 0.95 | 0.46-1.92 |
| OCT | VM7v (pb3A) | 0.8 (0.5-2.8) | 0.32 | 1.11 | 0.45-1.52 |
| OCT | VM7v (Or59c) | 1.2 (0.6-2.5) | 0.42 | 0.93 | 0.53-1.30 |
| OCT | VC1 (Or33c) | 1.2 (0.6-2.5) | 0.38 | 0.92 | 0.52-1.33 |
| OCT | DA4m (Or2a) | 1.2 (0.6-2.5) | 0.33 | 0.92 | 0.50-1.37 |
| OCT | VA3 (Or67b) | 1.2 (0.6-2.5) | 0.06 | 0.89 | 0.42-1.60 |
| OCT | DL4 (Or49a) | 1.2 (0.6-2.5) | 0.70 | 0.96 | 0.69-1.13 |
| OCT | D (Or69a, net of solvent) | 7.5 (4.5-12.5) | 0.88 | 0.73 | 0.42-0.88 |
| OCT | VA3 (Or67b imaging) | 11 (4.5-25) | 0.30 | 0.25 | 0.06-0.56 |
| OCT | DM2 (Pelz R/Rmax at 10⁻²) | 15 (9-25) | 0.72 | 0.39 | 0.13-0.64 |
| MCH | VA3 (Or67b imaging) | 11 (4.5-25) | 0.94 | 0.80 | 0.42-0.94 |
| MCH | D (Or69a, net of solvent) | 7.5 (4.5-12.5) | 0.70 | 0.52 | 0.22-0.75 |
| MCH | DA2 (Or56a imaging) | 7.5 (4.5-12.5) | 0.11 | 0.27 | 0.09-0.50 |
| MCH | DM2 (ab3A) | 0.8 (0.5-2.8) | 0.09 | 1.15 | 0.38-1.84 |
| MCH | DM2 (Pelz R/Rmax at 10⁻²) | 15 (9-25) | 0.54 | 0.28 | 0.08-0.52 |
| MCH | VC2 (pb1B) | 0.8 (0.5-2.8) | 0.09 | 1.15 | 0.38-1.83 |
| MCH | DL1 (ab1D) | 0.8 (0.5-2.8) | 0.04 | 1.16 | 0.37-1.93 |
| MCH | DC1 (Or19a) | 1.1 (0.4-2.5) | 0.03 | 0.94 | 0.41-2.40 |

- Saturated entries (DC2, VM5d) barely move. Moderate single-sensillum entries move by ×0.9-1.1, within a 0.4-1.9 range.
- The imaging entries move most because their stimulus was about 10× Hige's.
- These factors are applied in the "For the model" tables, on top of the corrections in §2.

## 2. Which glomeruli are real at Hige's concentration, and which are artifacts

### 2.1 What the PN data can and can't show

**Badel's PN data are at about twice Hige's concentration** (§1.2): 10⁻² in mineral oil, air bubbled through the vial,
then diluted 1:7.2 in the main stream. So Badel's pattern is the best available proxy for Hige's, probably somewhat
broader. In Badel's own series, a 10-fold dilution of benzaldehyde cut its glomeruli above 50% ΔF/F from 18 to 5, while
2-methylphenol (a narrow, high-affinity odor) barely changed over 1,000-fold (Table S2, derived).

**Some Badel glomeruli are weak reporters.** I took each glomerulus's largest mean ΔF/F over all 84 stimuli in Table S2
(derived). Low maxima mean that glomerulus's PNs report weakly in NP225 imaging, or that the odor set lacks its best
ligands. So a low OCT value there does not mean low ORN input.

| Glomerulus | Largest response, any stimulus (%) | Largest pure-odor response (%) | OCT | MCH | OCT / largest | MCH / largest |
|---|---|---|---|---|---|---|
| VA4 | 70 (mango mimic 10⁻³) | 36 (1-octen-3-ol, linalool) | 21 | 21 | 0.30 (0.58 of pure-odor max) | 0.30 |
| VC1 | 79 (2-methylphenol 10⁻³) | 65 (2-methylphenol) | 36 | 51 | 0.46 | 0.64 |
| DL1 | 121 (benzaldehyde) | 121 | 27 | 37 | 0.22 | 0.30 |
| DM1 | 80 (ethyl butyrate) | 80 | 9 | 14 | 0.12 | 0.17 |
| DA4l | 96 (MCH) | 96 | 15 | 96 | 0.15 | 1.00 |
| VA1d | 50 (MCH) | 50 | 7 | 50 | 0.15 | 1.00 |
| VA3 | 145 (benzaldehyde) | 145 | 18 | 108 | 0.12 | 0.75 |
| DM6 | 278 (OCT) | 278 | 278 | 88 | 1.00 | 0.32 |
| DM3 | 219 (OCT) | 219 | 219 | 87 | 1.00 | 0.40 |

- VA4 never exceeds 36% for any pure odor. Isopentyl acetate, which excites its receptor neuron pb3B (de Bruyne 1999),
  gives 19%. VA4's 21% for OCT is 0.58 of its largest pure-odor response. **Badel's VA4, VC1 and DL1 values therefore do not
  contradict DoOR's moderate OCT input there.** They say only that the responses are moderate relative to each
  glomerulus's own range.

**Pheromone glomeruli respond to broad odors in Badel's data, not in Barth's.**
- Badel's DA1 PNs (receptor Or67d, a cVA receptor) respond to ethyl butyrate 144, OCT 118, 2,3-butanedione 116,
  1-octen-3-ol 107 and MCH 78. DL3 (Or65a) responds to ethyl butyrate 180, OCT 166, 2,3-butanedione 138 and MCH 91
  (Table S2).
- These receptors are not known to respond to food odors. In Barth's GH146 PN imaging, DA1, DA3 and DL3 peak at only
  4-16% ΔF/F for both odors, against 109-255% in the glomeruli that respond (Fig. 5A, fig., approx.; my reading with the
  colour-bar lookup of `oct_mch_input.md` §8: DA1 MCH 5 / OCT 4, DA3 11 / 16, DL3 5 / 4). DL5 is also flat there (MCH 17,
  OCT 20). Barth's ORN imaging shows no DA1 ORN response to either odor (Fig. 3A).
- So Badel's DA1 and DL3 responses are most likely lateral input to PNs. The PN-inferred tier in
  `experiments/receptor_fills.py` turns them into ORN drive for both odors (OCT DL3 0.47, DA1 0.33; MCH DL3 0.25, DA1
  0.22).

**PN responses where the ORNs are silent or inhibited.** MCH evokes PN responses in Badel's data in glomeruli whose ORNs
show no MCH response or inhibition:
- DL5: Barth's ORN imaging −30% (inhibition) and de Bruyne 2001's coded 0 at ab4A, but Badel's PNs +77% (0.58 of
  DL5's maximum).
- DM3: ab5B −2 net spikes/s, Barth ORN about 8% (none), Churgin ORN near air; Badel PNs 87%, Yu 2004 "significant".
- VA5 (ab6B coded 0): Badel 110%. VA6 (ab5A coded 0): 69%.
- These are lateral excitation, disinhibition, or ORN input below the detection limit of single-sensillum category
  codes and GCaMP3. None is direct evidence of ORN drive.

**The two PN labs disagree glomerulus by glomerulus.** Already noted in `oct_mch_input.md` §8 (DA2, VM4, VC2). Add DM1:
Barth's PNs give OCT 256% (fig., approx., earlier reading); Badel's give 9%. DM1's ORNs show no OCT response in Barth's
ORN imaging, Münch's imaging (−0.47% ΔF/F) or Churgin's ORN imaging (Fig. 1G, fig., approx.: OCT and MCH cells at the air
level).

**Correction (2026-10-11).** [lateral_pn_responses.md](lateral_pn_responses.md) finds whole-cell recordings of DA1,
DL3 and DA2 PNs silent to general odors (including ethyl butyrate, 2,3-butanedione and 1-octen-3-ol, which give
107-362% ΔF/F in Badel's imaging), and several Badel glomeruli copying a neighbour (DA3 ~ D, DM3 ~ DM6, VM7v ~ VM7d, VM3
~ VM2). So Badel's DA1 and DL3 responses are not "lateral input to PNs" that fires them, and the 5-32 spikes/s of
lateral firing (Olsen 2007, VM2 and DL1 with silent receptors) doesn't apply there. The verdicts below (no ORN drive at
DA1, DL3) stand; the reasons change.

### 2.2 DoOR import artifacts

**D (Or69a): a solvent offset of about 0.22 in both odors.**
- DoOR stores Münch & Galizia's Or69a imaging values as OCT 2.412 and MCH 2.068 (% ΔF/F). The paper's Table S5 gives
  1.68 ± 0.47 (n = 7) and 1.33 ± 0.27 (n = 7). Its legend: "Corresponding solvent responses were subtracted from all
  responses." DoOR's dataset table marks `Muench.2015.AntGC1` as "solvents.subtracted: no" and sets SFR to 0 for imaging.
- The difference is the same for every odor: DoOR raw − Table S5 = 0.736 (range 0.731-0.741) over 105 odors for Or69a.
  It is 0.491 for Or10a (DL1), 0.342 for Or47b, 0.021 for Or56a and −0.018 for Or42b (each over 103-106 odors;
  derived). A constant offset per receptor is the unsubtracted mineral-oil response.
- For odors measured only by this study, DoOR's Or69a consensus equals 0.307 × raw ΔF/F (fitted, derived; 107 odors).
  The solvent response is therefore 0.307 × 0.735 ≈ 0.226 consensus units.
- Net of solvent: OCT 0.741 − 0.226 = **0.515**, MCH 0.635 − 0.226 = **0.409** (derived). The ratio, 0.79, is Table
  S5's.

**DA2 (ab4B, Or56a): a floor of about 0.3 under every odor.**
- DoOR's ab4B consensus has a median of 0.303 across 181 odors, with geosmin at 0.638 and SFR at 0.065 (derived).
  Odors with no measurable response sit at about 0.30-0.35.
- After SFR subtraction, OCT (0.241) and MCH (0.274) are mostly this floor.
- The raw data: Münch's imaging gives MCH 1.87 ± 0.34% and OCT 0.38 ± 0.14% against geosmin 17.59 ± 4.41% (Table S5),
  i.e. 0.106 and 0.022 of geosmin (derived). Stensmyr 2012's single-sensillum recording gives OCT −1.2 spikes/s against
  geosmin 146.4 (via DoOR).
- So DA2's receptor drive is small for MCH (about 0.1 of the receptor's best response, i.e. about 15 spikes/s if geosmin
  gives 146; derived) and about zero for OCT.
- DA2's PNs still respond strongly in Badel (OCT 140, MCH 236), and even more to ethyl butyrate (362), which ab4B's
  neurons do not detect: −0.4 (Stensmyr 2012), 7.6 (de Bruyne 2001) and −2 spikes/s (Marshall 2010), via DoOR. Most of
  DA2's PN response in Badel's data is not from its own ORNs.

**Global normalization makes DoOR × 200 Hz differ from measured rates.** The model's rate is DoOR × 200. Where a
single-sensillum rate exists, the two can differ by up to 2×:

| Glomerulus | DoOR × 200 (model, Hz) | Measured net rate at 10⁻² (spikes/s) | Source |
|---|---|---|---|
| DC2, OCT | 116 | 162 (native ab6A); 138 (empty neuron) | de Bruyne 2001; Kreher 2008 |
| DC1, OCT | 75 | 36 (native at3) | Dweck 2013 |
| DM3, OCT | 94 | 27 (native ab5B); 108 (Or47a in empty neuron) | de Bruyne 2001; Kreher 2008 |
| DM2, OCT / MCH | 67 / 51 | 57 / 13 (native ab3A) | de Bruyne 2001 |
| VM5d, OCT | 135 | 112 (native ab3B, de Bruyne); 254 (Hallem 2004, wild type) | |
| VA4, OCT | 74 | 48-81 (native pb3B) | de Bruyne 1999 (fig., approx.); Goldman 2005 |
| DA4m, OCT | 27 | 23 (Or2a in empty neuron) | Kreher 2008 |
| DL1, OCT / MCH | 24 / 26 | 2 / 7 (native ab1D) | de Bruyne 2001 |

- The DM3 entry illustrates the "larger receptor per glomerulus" rule: it takes the empty-neuron value for Or47a (108
  net) over the native neuron's 27 net spikes/s.
- DoOR stores Kreher 2008's values with each receptor's spontaneous rate added back (Table S1A + SFR, for all 21
  receptors; helper, checked by arithmetic), so DoOR's raw "95" for Or35a is 83 net and "40" for Or2a is 23 net. The
  consensus subtracts SFR again, so the model's values are net; only quoted raw numbers can mislead.

### 2.3 How much of Badel's PN breadth has receptor support

Badel's significant glomeruli (Fig. 2D, Mann-Whitney p < 0.01, as read by an earlier helper in `oct_mch_input.md` §8),
sorted by whether any receptor-level measurement shows the odor exciting that glomerulus's ORNs (my classification,
from §2.1-2.2 and the tables in "For the model"):

| Odor | Significant glomeruli with receptor-level support | Without (receptor silent, inhibited, or a pheromone receptor) |
|---|---|---|
| OCT (13) | DM6, DM3, VM2, D, VM7v, DM2, DC2, DC3 (weak), VM3 (weak) | DL3, DA1, DA3, DA2 |
| MCH (18) | D, VA3, DA2 (weak), VC1, DC3 (weak), DM6 (weak), VM7d (weak); probably DA4l, DL4 (analogs, untested receptors) | DA3, VA5, DL3, DM3, DA1, DL5 (ORNs inhibited), VM3, VA6, VM7v (pb3 screen) |

- OCT: 9 of 13 have receptor support. MCH: 7 of 18 have direct receptor evidence and 2 more (DA4l, DL4) have analog
  evidence. The other 9 sit on receptors that don't respond (VM7v by inference from de Bruyne 1999's pb3 screen). **Most of MCH's extra
  breadth at the PN level is in glomeruli whose ORNs do not respond to MCH.**
- These are the responses GCaMP6f (Badel) can see and GCaMP3 (Barth) cannot: Barth's PNs are flat in DA1, DA3, DL3 and
  DL5 (§2.1). Lateral excitation of 5-32 spikes/s (Olsen et al. 2007, `lateral_excitation.md`) is the likely source; a
  stronger GCaMP sees modest spiking that a weaker one misses (an inference, not tested in either paper).

**Correction (2026-10-11).** The last bullet's reading (lateral excitation as "the likely source" of Badel's
unsupported glomeruli) is revised by [lateral_pn_responses.md](lateral_pn_responses.md): in DA1, DL3 and DA2 the PNs
don't fire, and DA3, DM3, VM7v and VM3 look like neighbours' signals; lateral firing is real elsewhere (VA6, VA1d, DL5).
Without DA1, DL3, DA2 and DA3, flies' summed MCH/OCT is 0.99 (0.98 with them).

### 2.4 Verdicts

**3-octanol**

| Class | Glomeruli | Main reason |
|---|---|---|
| Real, strong | DC2, VM5d, VM5v, VM2, VC3, D, DM6, DM2 | native-neuron or empty-neuron rates of 57-232 net spikes/s at about Hige's concentration, or strong ORN imaging (VM2, VC3: Barth 82%, 95%) |
| Real, moderate | VA4, DM3, VM7v, DC1, VC1 | native neurons 27-81 net spikes/s; VA4's PN reporting is weak |
| Weak or doubtful | DL4, DA4m, VA3, VM3, DM1, DL1 | empty-neuron only (DL4, DA4m, DM1), small (VA3, VM3), or inhibited at the ORNs (DL1) |
| Artifact | DA2 | DoOR floor; ab4B −1.2 spikes/s |
| Not ORN drive | DA1, DL3 (and probably DA3) | pheromone receptors; Barth's PNs flat; Badel's respond to every strong odor |

**4-methylcyclohexanol**

| Class | Glomeruli | Main reason |
|---|---|---|
| Real, strong | VA3 | imaging 0.94 of Or67b's best; larval EC50 8× below OCT's; Barth ORN 75% |
| Real, moderate | D | imaging 0.70 of Or69a's best (after the solvent correction), at about 7.5× Hige's concentration |
| Real, weak | VC3, VC1, VC2, DM2, VM2, DM6, VM7d, DC1 | larval Or35a; Barth ORN 13-32%; single-sensillum 8-17 net spikes/s |
| Probably real, receptor untested | DA4l, DL4 | close analogs excite Or43a and Or85f; PN responses in one to three datasets |
| Not ORN drive | DA1, DL3, DL5, DM3, VA5, VA6, DC2, VM7v, VA4 | receptors silent, inhibited, or pheromone-specific; pb3's 16-odor screen |

## 3. The recommended patterns: basis

- **Rules.**
  - Start from measured rates (net spikes/s ÷ 200) where they exist, not DoOR's merged values.
  - Correct the DoOR artifacts of §2.2.
  - Apply the concentration factors of §1.5.
  - Where tiers disagree, follow the higher tier (native single sensillum > empty neuron > imaging > larval > analogs >
    PN-inferred), with the range covering the lower tiers.
  - Responses that are inhibitory at the ORNs (OCT at VA7l, DM4, DL1; MCH at DL5) are set to 0 because the model drives
    excitation only.
- **Totals** (derived; tables in "For the model"):

  | | OCT | MCH | MCH/OCT |
  |---|---|---|---|
  | Summed drive, central | 5.32 | 1.99 | 0.37 |
  | Glomeruli > 0.1 / ≥ 0.05 / > 0.2 | 13 / 17 / 10 | 2 / 9 / 2 (4 at ≥ 0.1) | |
  | Low ends / high ends of the ranges | 3.03 / 8.16 | 0.84 / 3.90 | 0.28 / 0.48 |
  | Current model input (DoOR + both fill tiers) | 8.56, 22 > 0.1 | 5.26, 16 > 0.1 | 0.61 |
  | DoOR alone | 6.41, 17 > 0.1 | 2.85, 5 > 0.1 | 0.45 |
  | Flies' receptor neurons | | | 0.41-0.51 (Barth ORN imaging, at 2.5-3.6× Hige's concentration) |

- **Why MCH falls further than DoOR suggests.** MCH's two main inputs (VA3, D) come from imaging at about 10× Hige's
  concentration. D also carries the solvent offset, and DA2's value is DoOR floor. OCT's main inputs come from
  single-sensillum recordings at about Hige's concentration.
- **Why OCT changes less** (6.41 in DoOR → 5.32, against MCH's 2.85 → 1.99). OCT loses DA2, the DA1, DL3, VM3 and DA3
  stand-ins, DL1, part of DA4m and D's solvent offset, but gains DC2's measured 162 spikes/s. Its strong inputs are
  single-sensillum values at about Hige's concentration.
- **The ranges are wide** because the concentration estimates are uncertain by 2.5-5×. They are not independent: a higher
  true Hige concentration raises both odors' weak entries together.

## 4. Measurements at Hige's exact protocol, and Kenyon cell data

**PNs at Hige's stimulus: none found.** No study I found imaged or recorded PNs with OCT and MCH at 2% saturated vapour,
1 L/min, 1-s pulses. The nearest:
- **Badel et al. 2016.** 10⁻² in mineral oil, air bubbled through the vial and diluted 1:7.2; in vivo GCaMP6f; 37
  glomeruli; 4-s odors. About twice Hige's concentration (§1.2).
- **Wang et al. 2003.** The same kind of stimulus (air dilution of saturated vapour; "The oxygen concentration at the
  position of the antennae was only 40% of the value calculated from the dilution ratio ... The factor of 40% was
  therefore applied to all odor concentration calculations"). But the preparation was ex vivo (antennae and brain in
  agarose, palps removed), the reporter was first-generation G-CaMP, and a glomerulus counted only above 20% ΔF/F: "At
  2% SV, many odors fail to elicit a significant response and those that do activate a small number of glomeruli".
  3-octanol only. Its thresholds reflect an insensitive readout, not the in vivo pattern.
- **Churgin et al. 2025.** "variably (10–25%) saturated airstream", ORN and PN imaging of five glomeruli only (DC2, DL5,
  DM1, DM2, DM3; `oct_mch_input.md` §7). In Fig. 1G, DM1 ORNs and PNs sit at the air level for both odors (fig.,
  approx.).
- **Davidson, Kaushik & Hige 2023** (Hige lab, eNeuro): "saturated vapor of odor was air-diluted to 1%". KC boutons and
  MBONs; no OCT/MCH responder counts or overlaps.
- **Hussain et al. 2018** (eLife): GH146 > GCaMP3; "50 μl of fresh odor solution ... diluted in distilled water or
  paraffin oil applied on Whatman chromatography paper"; airstream 2000 ml/min; 500-ms pulses. Only three glomeruli per
  odor were analysed: OCT (12 mM) DC2, DM6 and DP1; MCH (16 mM) DC1, DP1 and VC2.

**Kenyon cells at Hige's stimulus: Hige et al. 2015 itself.**
- Fig. 2E: "CS+ (OCT; n = 53 cells from 5 flies) and CS− (MCH; n = 49)". Pan-KC R13F02-LexA > GCaMP6f, "82 ± 9 cells per
  fly". Responder: above 2.33 SD on at least half the trials.
- "33 % of MCH-responding KCs and 30 % of OCT-responding KCs respond to both these odors". That is about 16 shared cells
  and a Jaccard index of about 0.19 (derived in `hige2015_specificity.md` §7).
- Responding fraction about 12-13% per odor (derived, same place).

**Honegger, Campbell & Turner 2011** (re-read for this note).
- Stimulus: "saturated vapor from pure odorant was serially diluted in air to achieve a dilution ratio of 1:100"; "Total
  airflow over the fly was 1 L/min"; valve open 0-1 s. So 1% saturated vapour, half of Hige's 2%.
- "Presented individually, each of these odors activates 9% of KCs on average. When presented simultaneously, however,
  this proportion increases only slightly (11%) and is smaller than the linear sum of the two activity patterns, 15%".
  n = 4 optical sections.
- Responder: "a peak dF/F value that was 2.33 SD (α = 0.01) greater than the baseline mean within a window 0.5–4.5 s
  after odor onset, on at least half of odor presentations".
- Per odor (Fig. 7A, fig., approx., from `oct_mch_input.md` §9): MCH 7.2%, OCT 9.8%, MCH/OCT 0.73.
- (derived) If the 15% "linear sum" is the union of the two patterns, about 3% of KCs respond to both, i.e. about a
  third of each odor's responders. That agrees with Hige's 30-33% at twice the concentration.

**Campbell et al. 2013** (re-read for this note).
- "Odors were presented using a custom-built delivery system that uses serial air dilutions to control odor
  concentration while maintaining a constant total airflow of 1 L/min at the fly."
- "Experiments were conducted at an odor dilution of 1:100 or, where appropriate, adjusted to match the concentrations
  used behaviorally. We used a photo-ionization detector (Aurora Scientific) to match concentrations between the imaging
  rig and the T-maze". T-maze: "MCH, 1.5:1000; OCT, 1:1000" in mineral oil.
- Which air dilution matched the T-maze: Not reported (also not in Honegger's thesis; helper). Per-odor responder
  fractions: Not reported.
- Pattern correlation OCT vs MCH r ≈ 0.22 (Fig. 3B, fig., approx.; earlier helper reading in `oct_mch_input.md` §9).

**Lin et al. 2014.**
- Stimulus: "Odors at 10−2 dilution were delivered by switching mass-flow controlled air/odor streams". The 10⁻² is an
  oil dilution, delivered with a 1:10 air dilution as in Shang et al. 2007 (helper): about 1.5× Hige's concentration
  (§1.2).
- "RNAi knockdown of GABA biosynthesis in the APL neuron does not affect sparseness or correlation of Kenyon cell
  responses to 4-methylcyclohexanol or 3-octanol" (Supplementary Fig. 8 title).
- Population sparseness in controls (fig., approx., `oct_mch_input.md` §9): MCH 0.940-0.982, OCT 0.916-0.971; taking
  1 − SP as the active fraction, MCH/OCT 0.61-0.71 (derived). Map correlation r = 0.04-0.11.

**Summary for Q4.** Only the KC overlap is measured at Hige's stimulus (30-33% shared). Turner-lab KC data at 1%
saturated vapour agree (about a third shared; MCH/OCT responders 0.73). The PN pattern at Hige's stimulus has to be
inferred, best from Badel's data at about twice Hige's concentration.

## 5. Other reasons the fly antennal lobe equalizes MCH with OCT

### 5.1 The biggest effect: what the fly ratios are summed over

**The imaging sets miss OCT's strongest glomeruli** (driver coverage from Grabe et al. 2016 Table S1, helper):
- NP225 (Badel) misses DC1, VC3, VM5d and VM5v.
- GH146 (Barth) is negative for VC3 and VM5d, and probably VM5v.
- Barth's 18 PN glomeruli also lack DM3, DC2, VA4, VM3, D and DC3 among OCT's targets, and VA3, D, VM7v, DA4l and VA5
  among MCH's (helper).

**The model on the same glomeruli** (derived from the per-glomerulus mean PN rates stored in `odor_probe54.json`, first
0.5 s, positive values summed; I recomputed these):

| Model condition | All 63 glomeruli | Badel's 37 | Barth's 18 |
|---|---|---|---|
| DoOR input | 0.56 | **0.86** | **0.82** |
| With both fill tiers | 0.66 | **0.93** | **0.76** |
| Flies | not measured | 0.98 | 0.85 |

- So on matched glomeruli the model's PN-level equalization is already close to flies'.
- The reported 0.52 / 0.59 sum over all uniglomerular PN cells. That weights glomeruli by PN number (VM5d 12, DA1 15,
  DL3 11, DA2 10 in MaleCNS; most others 2-7) and includes the four glomeruli the imaging misses.
- Weighting Badel's own values by MaleCNS PN counts lowers 0.98 to about 0.93 (helper).
- Flies' whole-AL PN ratio is unknown. Adding plausible OCT responses for the four missing glomeruli puts Badel at about
  0.70-0.92 (my range 0.76-0.92 from OCT 150-250% and MCH 30-100% there; helper 0.70-0.88).

**Real equalization on matched glomeruli** (Barth, one lab, 11 glomeruli imaged at both levels: DA1, DA2, DC1, DL1, DL5,
DM1, DM2, DM5, DM6, VC2, VM2):
- MCH/OCT is 0.15-0.35 at ORN terminals and 0.56-0.66 at PNs (helper; I get ≈0.2 and 0.62 from the readings in
  `oct_mch_input.md` and my Fig. 5A reading).
- In the model, the same 11 glomeruli give 0.83 at the PNs from an input ratio of 0.53 (DoOR), or 0.58 from 0.45 (filled)
  (model).

### 5.2 A fly-like transform with normalization equalizes the recommended inputs

- Flies' PNs respond strongly to weak private input: DL5 5.1 → 44 spikes/s, VM7 11.6 → 78, DM4 5.0 → 28 (Olsen et al.
  2010 Fig. 1B, `weak_input_gain.md` §1.2).
- With a whole odor, Olsen's normalization divides every glomerulus by the summed ORN input:
  r_PN = 165·r^1.5 / (σ^1.5 + r^1.5 + (m·Σr)^1.5), with m ≈ 0.05 (Luo et al. 2010; Olsen's population fit corresponds to
  m ≈ 0.056, `weak_input_gain.md` §1.6). MCH's summed input is less than half of OCT's, so its weak glomeruli are divided
  less.
- Evaluated on the recommended central inputs of "For the model" (derived arithmetic, not a model run; every positive
  entry × 200 Hz; normalization over all glomeruli). Each cell gives MCH/OCT, then glomeruli with PN > 20 Hz as
  OCT : MCH:

  | σ (Hz), m | All glomeruli | Badel's 37 | Barth's 18 |
  |---|---|---|---|
  | 12, 0.05 | 0.71 (14 : 11) | **0.90** (10 : 10) | **0.79** (5 : 5) |
  | 12, 0 | 0.64 (25 : 26) | 0.74 (19 : 20) | 0.74 (8 : 10) |
  | 16, 0.05 | 0.66 (14 : 11) | 0.84 (10 : 10) | 0.72 (5 : 5) |
  | 25, 0.05 | 0.57 (13 : 9) | 0.74 (9 : 8) | 0.59 (4 : 4) |

- **An ORN-level ratio of 0.37 becomes 0.79-0.90 on the imaged sets** with flies' σ and normalization, close to Barth's
  0.85 and Badel's 0.98. The input does not need to be PN-matched.
- What the equation cannot produce is Badel's larger number of MCH glomeruli (18 against 13). Most of that excess is in
  glomeruli without receptor input (§2.3), i.e. lateral.

### 5.3 Lateral excitation adds about the same to both odors

From `lateral_excitation.md` (not re-read here):
- Lateral excitation saturates at low input: half-maximal at about 7-10 ORN spikes/s from one ORN type and flat from 50
  to 150 spikes/s (Olsen et al. 2007). Five odors spanning at least a 7-fold range of total ORN activity gave equal lateral
  excitation (Yaksi & Wilson 2010, per `lateral_excitation.md`). Both odors are far above saturation.
- Size: PNs whose own ORNs are silenced still fire 6-32 spikes/s (VM2, mean 16.7) and 5-26 spikes/s (DL1, mean 13.2)
  (Olsen 2007). Removing gap junctions (shakB²) cut VC1's odor responses by 28-52%.
- eLNs respond about equally to the two odors (Huang et al. 2010 Fig. 7, as % of each cell's maximum): On responses OCT
  9-36%, MCH 6-35%; Off responses OCT 54-100%, MCH 51-100%.
- An equal additive term raises the smaller odor's summed response proportionally more, and adds glomeruli to both
  counts.
- In Badel's data the lateral responses are large (DA1, DL3: OCT 118 and 166%, MCH 78 and 91%). In Barth's GCaMP3 data
  they are invisible (§2.1).
- Caveat: in intact flies "the net effect of lateral input was always inhibitory" (Olsen 2010, as quoted in
  `lateral_excitation.md`).

### 5.4 Glomerulus-specific inhibition: measured, and slightly against MCH

**Hong & Wilson 2015, Neuron 85:573** ([PMC5495107](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/)).
- Method: ChR2 in NP3056 LNs in shakB² flies (46 PNs), or uncaging of GABA (52 PNs). Sensitivity is the slope of sEPSC
  suppression against light intensity, normalized to the most sensitive cell (helper).
- Quotes (re-checked):
  - "Sensitivity ranges from nearly totally insensitive (e.g. glomerulus DL4) to almost completely inhibited (e.g.
    glomerulus VA3)."
  - "the lifetime strength of lateral inhibition in each glomerulus is mainly an autonomous feature of that glomerulus,
    not a property of the LN network."
  - "LN activity scales with the logarithm of total ORN" spiking.
- Per glomerulus (helper, from Supplemental Table 1; LN activation / GABA):
  - VA3 0.90 / 0.87; DC2 – / 0.62; DM6 0.45 / 0.62; DC1 – / 0.54; DA2 0.44 / –; VC3 0.43 / 0.26; D 0.40 / –;
    VM5v 0.37 / 0.19; VM2 0.29 / 0.45; VM5d – / 0.21; DL4 0.18 / –.
- **VA3, MCH's dominant input, is among the most inhibitable glomeruli.** VM5d, VM5v, VC3 and DL4 are among the least.
  - Drive-weighted sensitivity is 0.57-0.62 for MCH's glomeruli against 0.38-0.42 for OCT's (helper, derived).
  - Scaling each glomerulus's m by these sensitivities changes the static MCH/OCT ratio by −0.06 to +0.01 (helper,
    derived).
- **Root et al. 2008** (GABA-B; [PMC2539065](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/), helper) points the other
  way for VA3: its ORN terminals show the second-weakest GABA-B suppression in Fig. 5G (27%, fig., approx.).
  - Hong's measure includes GABA-A, which could be strong at onset while GABA-B dominates sustained responses. Untested.
- **LN anatomy and the connectome show no OCT/MCH difference** (helper, derived):
  - Chou et al. 2010 innervation probabilities, drive-weighted: 0.851 vs 0.847.
  - MaleCNS GABA-LN→ORN synapses per ORN→uPN synapse: 0.27 vs 0.30.
  - These densities do not track Hong's sensitivities (r = −0.13 to −0.27).

### 5.5 Odor-dependent LN recruitment: the one unmeasured lever that could matter

- Hong & Wilson 2015 (re-checked): "not all odors were equally efficient at recruiting LN activity, even when they evoked
  equal levels of total ORN activity". 10⁻⁴ pentyl acetate recruited more LN activity than 10⁻⁶ E2-hexenal at equal ORN
  field potential. The authors suggest this "may reflect the fact that the pentyl acetate stimulus elicits ORN spiking
  that is distributed across more ORN types".
- At 1 mV·s of field potential: pentyl acetate ≈67% LN ΔF/F against ≈43% for E2-hexenal (Fig. 3D, fig., approx.; helper).
- OCT spreads its input over more ORN types than MCH does: 13 against 2-4 glomeruli above 0.1 here.
- If OCT recruited 1.25× or 1.5× the inhibition its summed input predicts, the static ratio would go from 0.64 to 0.75 or
  0.86 at σ 12 (helper, derived).
- Not measured for OCT against MCH.

### 5.6 ORN kinetics and adaptation

- Firing-rate time courses for OCT or MCH in any relevant ORN class: Not reported. Martelli et al. 2013's 27 odors
  include neither; nor do Nagel & Wilson 2011, Cao et al. 2016 or Montague et al. 2011 (helper).
- Barth's heat maps by time window (fig., approx.; helper):
  - ORN MCH/OCT is 0.52 at the peak but 0.26 for the integral over 10 s, because OCT's ORN calcium persists after offset.
  - PN MCH/OCT is 0.84-0.87 whichever window is used.
- A model using steady-state or 500-ms rates therefore overweights OCT's strong inputs by at most about 1.15-1.25×
  (helper, derived). Small, and in OCT's favour.

### 5.7 Imaging nonlinearity

- The helper found no calibration of GCaMP3 or GCaMP6f against PN spike rate. The only PN calibration found, for
  G-CaMP1.3 (Jayaraman & Laurent 2007), "failed to report even sustained (>1 second) activity if it was below 30
  sp/second" (helper).
- Larval NMJ calibrations give Hill coefficients of about 2.3 with half-maxima at 54-63 Hz for GCaMP1.6/GCaMP2 (Hendel
  et al. 2008; helper).
- Badel's preparation reaches 456% (DA2, geosmin), well above OCT's 278%, so hard clipping of OCT is unlikely. Barth's PN
  colour bar ends at 260% and OCT reads 255-256 in DA2 and DM1, so Barth's OCT may be clipped. At 300-350% Barth's ratio
  would be 0.76-0.81 (helper, derived).
- Saturation could turn a true 0.6 into 0.85-0.98 only if OCT's glomeruli fire at 100-200 spikes/s and MCH's deficit is
  in rate per glomerulus rather than in the number of glomeruli (helper, illustrative Hill model). Not established either
  way.

### 5.8 Kenyon cells add their own normalization

From Prisco et al. 2021 ([PMC8741211](https://pmc.ncbi.nlm.nih.gov/articles/PMC8741211/); 1:100 in mineral oil):
- PN boutons: "the number of active boutons was similar between Mch and Oct stimulations (Figure 3D, n = 10, p = 0.689,
  paired t-test), the average response peak among active boutons was higher when flies were exposed to Oct". Bouton peak
  MCH/OCT is about 0.69 (fig., approx., `oct_mch_input.md` §8).
- KC claws (helper, fig., approx.):

  | Condition | Claw peak MCH/OCT | Responding claws, MCH vs OCT |
  |---|---|---|
  | APL working | 0.89 | 17.5 vs 18.5 |
  | APL silenced | 0.65 | 21 vs 27.5 |

- APL calcium MCH/OCT ≈0.49 (helper).
- Lin et al. 2014: "RNAi knockdown of GABA biosynthesis in the APL neuron does not affect sparseness or correlation of
  Kenyon cell responses to 4-methylcyclohexanol or 3-octanol" (Supplementary Fig. 8 title).
- So in flies, MCH's PN output to the calyx is about as broad as OCT's but weaker per bouton, and APL removes most of the
  amplitude difference at the claws.

### 5.9 Model-side observations (stored outputs, not new simulations)

**(a) Weak inputs are suppressed during whole odors, with large differences between glomeruli.**

Source: `experiments/odor_probe54.json`, both fill tiers. Model PN is the mean rate per glomerulus over the odor's first
0.5 s, rest subtracted. The last column is Olsen/Luo's equation at the model's own private-odor transform (σ 15,
Rmax 130, m 0.05; derived).

| Glomerulus | Odor | ORN input (Hz) | Model PN (Hz) | Olsen/Luo, σ 15, Rmax 130 (Hz) |
|---|---|---|---|---|
| VC3 | OCT | 87 | 14 | 63 |
| VM7v | OCT | 41 | 9 | 30 |
| VC1 | OCT / MCH | 31 / 35 | 1 / 16 | 22 / 42 |
| VA3 | OCT | 25 | −1 | 16 |
| DL4 | OCT | 23 | 5 | 15 |
| VC3 | MCH | 25 | −2 | 29 |
| VA7l | MCH | 24 | 3 | 27 |
| VM5d / VM5v | MCH | 16 / 17 | 6 / 2 | 16 / 18 |
| DC2 | MCH | 16 | 0 | 16 |
| DL1 | MCH | 26 | 32 | 30 |
| DA4m | OCT | 27 | 43 | 18 |
| VM5d | OCT | 135 | 144 | 84 |

- The model's gain varies several-fold between glomeruli at similar input. Several of MCH's weak-input glomeruli (VC3, VC1,
  VA7l, VM5d, VM5v, DC2) are among the low-gain ones.
- In flies:
  - "R_max and σ are essentially the same for all glomeruli" except DM1 (Olsen 2010).
  - Unitary ORN→PN EPSPs are matched across glomeruli: DL5 7.0, DM4 6.9, DM6 5.5, VM2 5.4 mV (Kazama & Wilson 2008); "The
    gain ... is kept constant across different PN types" (`weak_input_gain.md` §2).
- The model sets one global synaptic factor, so its per-glomerulus gain follows MaleCNS synapse and ORN counts:
  - Model unitary EPSPs: DM6 7.0 and VM2 9.0 mV (helper).
  - ORN / PN counts (MaleCNS, both sides; read-only count): VC3 34 / 7, VC1 29 / 2, VA7l 29 / 2, VA3 30 / 4, VM7v 25 / 3,
    DA4m 35 / 2, DL1 83 / 4, VM5d 84 / 12, DA1 204 / 15.
  - ORN number alone does not explain the gains: DA4m and VC3 have similar ORN counts and very different gains.

**(b) On matched glomeruli the model's PNs are silent where flies' respond** (helper). In the unfilled model: DL3 and DA3
for both odors, VM2 for OCT, and DA4l, VA5, DM6, DM3, DL4 and VM7v for MCH. Most of these are lateral responses in flies
(§2.3), so the fix is lateral excitation or weak-input transmission, not more ORN drive.

## For the model

### Recommended receptor-level input at Hige's 2% SV

Units are DoOR-equivalent (value × 200 spikes/s). "Current" is the model's input now with both fill tiers
(`receptor_fills.applied(pn_inferred=True)`).

Tiers, strongest first:
- **R1** native-neuron single-sensillum recording;
- **R2** the receptor in the empty neuron;
- **I** calcium imaging of receptor neurons;
- **L** larval neuron with the same receptor (Si et al. 2019);
- **C** response to close analogs (cyclohexanol, cyclohexanone), receptor never tested with the odor;
- **P** inferred from PN responses only.

"×" factors in the basis column are the §1.5 concentration factors.

**3-octanol**

| Glomerulus | Recommended | Range | Current | Tiers | Basis |
|---|---|---|---|---|---|
| DC2 | 0.75 | 0.55-0.85 | 0.58 | R1 R2 I L | ab6A 162 net spikes/s, 0.93 of the class's best (de Bruyne 2001; stimulus ≈0.8× Hige's, ×1.03); Or13a in the empty neuron 138 net (Kreher 2008, ≈1.2×, ×0.96), 15 at 10⁻⁴; high affinity (imaging EC50 10⁻³·⁵⁰; larval EC50 10⁻⁶·²⁴). Badel PN 74 (0.47 of DC2's max) |
| VM5d | 0.65 | 0.55-0.95 | 0.68 | R1 R2 I | ab3B 112 net (de Bruyne 2001, ×1.02 → ≈115 Hz); Or85b in the empty neuron 245 (Hallem 2004, spontaneous rate probably included; stimulus ≈2.2× Hige's, ×0.91 → ≈210 Hz); Barth ORN VM5 92%. Near saturation |
| VM5v | 0.50 | 0.25-0.75 | 0.59 | R1 | ab7A top category (code 79) at 10⁻² (de Bruyne 2001); for Or98a that category spans 42-260 spikes/s in Hallem 2006's data |
| VM2 | 0.45 | 0.30-0.60 | 0.69 | I | Or43b never tested; Barth ORN 82% at ≈3.6× Hige's concentration (the old fill 0.69 × ≈0.65); PNs 171% in both Badel and Barth; Wang 2003 at 40% SV |
| D | 0.38 | 0.22-0.45 | 0.74 | I | Münch 2016 imaging 1.68% ΔF/F net of solvent (0.88 of Or69a's best): DoOR's 0.741 − 0.226 solvent offset = 0.515, ×0.73 because the imaging stimulus was ≈7.5× Hige's. Badel PN 146 |
| VC3 | 0.38 | 0.20-0.55 | 0.43 | R2 L I | Or35a in the empty neuron 83 net (Kreher 2008, ≈1.2×; ×0.92 → ≈76 Hz), 7 at 10⁻⁴; larval EC50 10⁻⁴·¹⁷; Barth ORN 95% (OCT's strongest). Not in either PN set |
| DM6 | 0.34 | 0.15-0.50 | 0.32 | R2 I | Or67a in the empty neuron 110 (Hallem 2004, ≈99 net; stimulus ≈2.2×, ×0.69 → ≈68 Hz); Barth ORN 63%; Badel PN 278 (DM6's largest response to anything) |
| DM2 | 0.31 | 0.20-0.42 | 0.34 | R1 I | ab3A 57 net (de Bruyne 2001, ×1.10 → ≈63 Hz); Pelz 2006 EC50 10⁻²·⁸⁰; Barth ORN 58%; Churgin ORN 1.06 vs air 0.32 ΔF/F |
| VA4 | 0.30 | 0.15-0.45 | 0.37 | R1 | pb3B ≈48 net (de Bruyne 1999, fig., approx.; OCT the best of the 7-odor panel used on pb3; ×1.12) and 81 (Goldman 2005, ×0.93). Badel's VA4 PNs report weakly (§2.1) |
| DM3 | 0.28 | 0.12-0.50 | 0.47 | R1 R2 L I | native ab5B 27 net (de Bruyne 2001, ×1.13 → ≈31 Hz) vs Or47a in the empty neuron 108 net (Kreher 2008, ×0.93 → ≈100 Hz; 0 at 10⁻⁴); larval Or33b/Or47a EC50 10⁻⁴·⁹⁸; Barth ORN 50%; Badel PN 219 (DM3's max) |
| VM7v | 0.20 | 0.12-0.28 | 0.20 | R1 | pb3A ≈35 net (de Bruyne 1999) and 46 (Goldman 2005); ×0.93-1.11; Badel PN 106 |
| DC1 | 0.17 | 0.08-0.35 | 0.37 | R1 I | at3 (Or19a) 36 spikes/s (Dweck 2013, ≈1.1×; ×0.95); Barth ORN 26% then a strong undershoot; Barth PN 197%. DoOR × 200 (75 Hz) is twice the measured rate |
| VC1 | 0.12 | 0.03-0.22 | 0.15 | R1 R2 I | pb2A ≈5-28 net in the native neuron (de Bruyne 1999: 11.6 including SFR 7; Goldman 2005: 28); Or33c / Or85e in the empty neuron 47 / 41; Barth ORN 47%; Badel PN 36 (0.46 of VC1's max) |
| DL4 | 0.08 | 0.02-0.14 | 0.12 | R2 | Or49a in the empty neuron 31 net only (Kreher 2008; 1 at 10⁻⁴); larval Or49a no response; PNs disagree (Badel 26, Barth 172, Pech ≈94) |
| DA4m | 0.06 | 0.02-0.12 | 0.13 | R2 | Or2a in the empty neuron 23 net only (Kreher 2008; 0 at 10⁻⁴); Barth ORN DA4 (DA4l and DA4m merged) shows nothing |
| VA3 | 0.06 | 0.03-0.12 | 0.12 | R2 I L | Or67b in the empty neuron 19 net (Kreher 2008; 1 at 10⁻⁴); imaging 0.30 of Or67b's best at ≈11× Hige's; larval EC50 8× weaker than MCH's; Barth ORN nothing; Badel PN 18 |
| VM3 | 0.06 | 0.02-0.12 | 0.34 | I | Or9a never tested; Barth ORN 21% at ≈3.6×; Badel PN 122 (may be partly lateral) |
| DC3 | 0.03 | 0.01-0.06 | 0.05 | R1 I | Or83c 10 spikes/s undiluted (Ronderos 2014) and 9 (Grabe 2016, dilution not reported); Barth ORN 21% |
| DM5 | 0.03 | 0.00-0.06 | 0.04 | R1 I | ab2B 7 (Stensmyr 2003, via DoOR); Barth ORN 17% |
| VM7d | 0.03 | 0.01-0.08 | 0.09 | R1 | pb1A ≈6 net (de Bruyne 1999, fig., approx.); Or42a in the empty neuron 27 net (Kreher 2008; −2 at 10⁻⁴); larval Or42a no response |
| DA3 | 0.02 | 0.00-0.10 | 0.32 | P | Or23a never tested; Badel PN 113 but Barth PN 16% (fig., approx.); likely lateral |
| DM1 | 0.02 | 0.00-0.15 | 0.06 | R1 R2 I | ab1A coded 0; Münch imaging −0.47% (inhibition); Barth and Churgin ORN nothing; only Or42b in the empty neuron responds (44 net in Kreher 2008, −2 at 10⁻⁴; 29 at 10⁻⁴ in Mathew 2013); larval Or42b no response |
| VA5 | 0.02 | 0.00-0.04 | 0.03 | R1 | ab6B coded 0 (DoOR residue) |
| VA6 | 0.02 | 0.00-0.06 | 0.05 | R1 R2 | ab5A coded 0; Or82a in the empty neuron 14 net (Kreher 2008; −3 at 10⁻⁴); larval Or82a no response |
| VC4 | 0.02 | 0.00-0.04 | 0.05 | R1 | ab7B coded 0 (DoOR residue) |
| DA2 | 0.01 | 0.00-0.03 | 0.24 | R1 I | ab4B −1.2 spikes/s (Stensmyr 2012); Münch imaging 0.022 of geosmin; DoOR's 0.241 is its floor (§2.2). PN responses (Badel 140, Barth 256) are not from these ORNs |
| DL1 | 0.01 | 0.00-0.05 | 0.12 | R1 I | ab1D 2 net; Münch imaging 0.52% (net of solvent); Barth ORN −18% (inhibition) |
| DL5 | 0.01 | 0.00-0.03 | 0.03 | R1 | ab4A coded 0; Stensmyr 2012 −5 (via DoOR) |
| VC2 | 0.01 | 0.00-0.03 | 0.01 | R1 | pb1B ≈2.5 net (de Bruyne 1999, fig., approx.) |
| DA1 | 0.00 | 0.00-0.03 | 0.33 | P | Or67d is a cVA receptor; Barth ORN and PN nothing; Badel's PN 118 is lateral (§2.1) |
| DL3 | 0.00 | 0.00-0.03 | 0.47 | P | Or65a (at4); Barth PN nothing; Badel's PN 166 is lateral (§2.1) |

In the current input but not listed above (set to 0): DM4 0.022

**4-methylcyclohexanol**

| Glomerulus | Recommended | Range | Current | Tiers | Basis |
|---|---|---|---|---|---|
| VA3 | 0.70 | 0.40-0.85 | 0.88 | I L | Galizia 2010 imaging 1.17 × 1-hexanol (0.94 of Or67b's best) at ≈11× Hige's concentration, ×0.80; larval Or67b EC50 10⁻⁴·²¹, 8× more potent than OCT; Barth ORN 75% (MCH's strongest); Badel PN 108 |
| D | 0.21 | 0.10-0.32 | 0.64 | I | Münch 2016 imaging 1.33% net of solvent (0.70 of Or69a's best): DoOR's 0.635 − 0.226 = 0.409, ×0.52 for the ≈7.5× stronger imaging stimulus. Badel PN 172 (≥ OCT's 146) |
| DA4l | 0.10 | 0.03-0.22 | 0.27 | C P | Or43a never tested with MCH; cyclohexanol (139 spikes/s) and cyclohexanone (127) are its third and fourth strongest ligands after 1-hexanol (Hallem 2004, via DoOR); Badel PN 96 is DA4l's largest response to any odor (OCT 15); Barth ORN DA4 (merged) shows nothing |
| VC3 | 0.10 | 0.05-0.20 | 0.12 | L I C | Or35a never tested with MCH in adults; larval Or35a responds (EC50 10⁻³·⁸⁷; 0.49 of OCT at 10⁻⁴); Barth ORN 21% (0.22 of OCT); Or35a responds to cyclohexanone (127, Kreher 2008) |
| VC1 | 0.09 | 0.04-0.18 | 0.17 | I C | Barth ORN 32% (0.68 of OCT's) at ≈2.5× Hige's; cyclohexanone is Or33c's best ligand (125) and Or85e's second (210; Goldman 2005); Badel PN 51 (0.64 of VC1's max) |
| VC2 | 0.09 | 0.04-0.14 | 0.08 | R1 | pb1B ≈17 net (de Bruyne 1999, fig., approx.; ×1.15): 'The only other response from pb1B that was significantly different from that of the paraffin oil control is the response to 4-methylcyclohexanol'; Barth ORN 14% |
| DL4 | 0.08 | 0.03-0.18 | 0.27 | C P | Or49a/Or85f never tested with MCH; Or85f responds to cyclohexanol (62; Hallem 2004), and acetophenone is both Or85f's best ligand (91) and DL4's largest PN response in Badel (144); PNs respond to MCH in three datasets (Badel 97 vs OCT 26; Barth 218 vs 172; Pech ≈125 vs ≈94); larval Or49a no response |
| DM2 | 0.08 | 0.04-0.18 | 0.25 | R1 I | ab3A 13 net (de Bruyne 2001; 0.23 of OCT; ×1.15 → ≈15 Hz); Pelz 2006 EC50 10⁻²·¹⁵ (4.5× above OCT's); Barth ORN 19% (0.33 of OCT); Churgin 0.24 of OCT (air-subtracted) |
| VM2 | 0.06 | 0.03-0.10 | 0.12 | I | Or43b never tested; Barth ORN 17% at ≈2.5× (0.21 of OCT); Badel PN 34, Barth PN 27 (OCT 171 in both) |
| DM6 | 0.04 | 0.02-0.08 | 0 | I | Or67a never tested with MCH; Barth ORN 13% (0.21 of OCT); PNs disagree (Badel 88, Barth 198) |
| VM7d | 0.04 | 0.02-0.06 | 0.06 | R1 | pb1A ≈8 net (de Bruyne 1999, fig., approx.); larval Or42a no response; Badel PN 84 |
| DC1 | 0.03 | 0.01-0.08 | 0 | R1 I | at3 (Or19a) 5 spikes/s (Dweck 2013) vs Barth ORN 18% (0.7 of OCT); DC1 PNs respond to MCH in the Fiala lab (Barth 109%, Pech 2015, Hussain 2018) |
| DC3 | 0.03 | 0.00-0.08 | 0.08 | R1 I | Or83c 17 spikes/s undiluted (Ronderos 2014) but −1 in the native sensillum (Grabe 2016, dilution not reported); Barth ORN 21% (equal to OCT) |
| DL1 | 0.03 | 0.01-0.07 | 0.13 | R1 I | ab1D 7 net; Münch imaging 0.53% net of solvent; Badel PN 37 |
| VA7l | 0.03 | 0.01-0.06 | 0.12 | I | Barth ORN 'VA7' 16%; Badel VA7l PN 26 (0.09 of its max) |
| VM5d | 0.03 | 0.00-0.10 | 0.08 | R1 I | ab3B 4 net (de Bruyne 2001) vs Barth ORN VM5 (merged) 32% |
| DA2 | 0.02 | 0.01-0.06 | 0.27 | I | Münch imaging 0.106 of geosmin's response at ≈7.5× Hige's (×0.27 → ≈4 spikes/s if geosmin gives 146); DoOR's 0.274 is mostly its floor (§2.2). PN responses (Badel 236, Barth 44) are not explained by these ORNs |
| DA3 | 0.02 | 0.00-0.10 | 0.32 | C P | Or23a never tested; cyclohexanone 54, cyclohexanol 43 (Hallem 2004); Badel PN 116 = OCT's 113; Barth PN 11% (fig., approx.) |
| DA4m | 0.02 | 0.00-0.08 | 0 | C | Or2a never tested with MCH; cyclohexanol 51 (Hallem 2004); Barth ORN DA4 nothing |
| DC2 | 0.02 | 0.00-0.10 | 0.08 | R1 L I | ab6A −15 net and larval Or13a no response vs imaging (Galizia 2010: 0.42 of OCT; Barth ORN 26%); Badel PN 20; Churgin 0.09 vs OCT 0.34 |
| DM5 | 0.02 | 0.00-0.04 | 0.01 | R1 | ab2B 3 net (de Bruyne 2001) |
| VA4 | 0.02 | 0.00-0.10 | 0 | R1 | as VM7v (pb3B); Badel PN 21 = OCT's 21; Or85d does not respond to cyclohexanone |
| VA5 | 0.02 | 0.00-0.04 | 0.03 | R1 | ab6B coded 0; Badel PN 110 (likely lateral) |
| VC4 | 0.02 | 0.00-0.04 | 0.05 | R1 | ab7B coded 0 (DoOR residue) |
| VM5v | 0.02 | 0.00-0.10 | 0.08 | R1 I | ab7A coded 0 vs Barth ORN VM5 (merged) 32% |
| VM7v | 0.02 | 0.00-0.10 | 0.34 | R1 | Or59c never tested with MCH by name, but pb3 neurons gave 'Significant responses ... only ... to 3 of the initial 16 odorants', a set that included MCH (de Bruyne 1999); Badel PN 121 (likely lateral) |
| DM3 | 0.01 | 0.00-0.03 | 0 | R1 L | ab5B −2 net; larval Or33b/Or47a EC50 10⁻²·⁴⁶ (≈300× above OCT's); Barth and Churgin ORN nothing; Badel PN 87 (likely lateral) |
| DM4 | 0.01 | 0.00-0.03 | 0.03 | R1 | ab2A 0 net |
| VA1v | 0.01 | 0.00-0.02 | 0.01 | I | Münch imaging 0.01% (DoOR residue) |
| VA6 | 0.01 | 0.00-0.04 | 0.02 | R1 | ab5A coded 0; larval Or82a no response; Badel PN 69 (likely lateral) |
| VM3 | 0.01 | 0.00-0.05 | 0.20 | I P | Or9a never tested; Barth ORN nothing for MCH; Badel PN 72 (OCT 122) |
| DA1 | 0.00 | 0.00-0.03 | 0.22 | P | Or67d (cVA receptor); Badel PN 78 is lateral |
| DL3 | 0.00 | 0.00-0.03 | 0.25 | P | Or65a; Badel PN 91 is lateral |
| DL5 | 0.00 | 0.00-0.01 | 0.06 | R1 I | Barth ORN −30% (inhibition); ab4A coded 0; Badel PN 77 is lateral or disinhibition |

### What the recommendation implies

1. **The input cannot equalize the odors without contradicting receptor data.**
   - Every receptor-level line of evidence puts MCH's summed drive at about 0.3-0.5 of OCT's at Hige's concentration
     (0.37 here; Barth's ORN imaging 0.41-0.51).
   - MCH has far fewer glomeruli above 0.1 (2-4 against 13).
   - Flies' PN- and KC-level equalization therefore has to come from downstream.
2. **Compare PN ratios on the glomeruli flies were imaged in, per glomerulus** (§5.1).
   - The model already gives 0.86-0.93 on Badel's 37 and 0.76-0.82 on Barth's 18 (flies 0.98 and 0.85).
   - Olsen/Luo's equation with the recommended inputs gives 0.90 and 0.79.
   - The 0.52-0.59 in `odor_equalization_check.py` sums over all uniglomerular PNs. It counts VM5d (12 PNs) and DA1
     (15) heavily and includes VM5d, VM5v, VC3 and DC1, which neither imaging set has.
3. **The gap that matters is the KC step** (model 0.25, flies 0.73-0.92).
   - KCs receive input from every glomerulus, so the sampling caveat does not apply there.
   - Flies' APL equalizes claw responses (Prisco 2021: claw peaks 0.89 with APL vs 0.65 silenced; helper). Check the
     model's APL and KC thresholds against that before changing the antennal lobe again.
4. **Weak-input suppression still costs breadth** (§5.9).
   - In probe54, glomeruli with 16-35 Hz of input give 0-16 Hz of PN response in VC3, VC1, VA7l, VA3, DC2, VM5v and
     VM5d. Flies' PNs answer 5-13 Hz of private input with 28-85 spikes/s.
   - With the recommended inputs, MCH's breadth at the PNs depends on passing 6-20 Hz inputs (0.03-0.1).
5. **Fix two DoOR artifacts regardless**; they affect both odors:
   - D's solvent offset (−0.226);
   - DA2's floor (OCT ≈ 0, MCH ≈ 0.02-0.06 instead of 0.24-0.27).
6. **Drop the PN-inferred pheromone glomeruli** (DA1, DL3) as ORN input for both odors. If those PN responses are wanted,
   model them as lateral excitation, which is about equal for the two odors (`lateral_excitation.md`).
7. **If PN-matched stand-ins are kept anyway,** label them as lateral or AL compensation, not receptor input. Make them
   symmetric where the PN data are symmetric (DA3: OCT 113, MCH 116).

### Unresolved

- Neither odor's oil headspace has been measured. The central concentration factors rest on homologous alcohols (0.30 of
  SV at 1%, range 0.20-0.50), and every "× Hige" carries a 2.5-5× uncertainty.
- No receptor-level MCH data exist for Or43a (DA4l), Or85f (DL4), Or67a (DM6), Or43b (VM2), Or9a (VM3), Or23a (DA3),
  Or65a (DL3) or Or67d (DA1). Or35a has only larval data.
- de Bruyne 1999's pb3 screen names only 2 of the 3 odorants that drove pb3. The MCH conclusion for VM7v and VA4 is an
  inference from MCH being among the 16 screened.
- Imaging and single-sensillum recordings disagree for MCH at DC2 (imaging 0.42 of OCT vs −15 spikes/s), at DM2 (Pelz
  0.75 of OCT vs 0.23) and at VM5 (Barth 32% vs 4 spikes/s).
- The model's per-glomerulus gain heterogeneity (§5.9) has not been traced to its cause: synapse counts, PN number, or LN
  targeting.
- Whether OCT's broader input recruits more LN inhibition than MCH's at equal total ORN activity has not been measured. It
  could account for 0.1-0.2 of the PN-level ratio (§5.5).

## Sources

**Read or re-analysed for this note**
- DoOR.data, <https://github.com/ropensci/DoOR.data> (master, downloaded 2026-10-10): per-receptor files `data/*.csv`,
  `door_dataset_info.csv`, `door_response_matrix.csv`, `door_mappings.csv`, `odor.csv`. The model's copies in
  `~/fly-data/door/` were used for the consensus values.
- Münch D, Galizia CG (2016) DoOR 2.0. Sci Rep 6:21841. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4766438/>.
  Supplementary information, Table S5 (`srep21841-s1.pdf`).
- Si G, Kanwal JK, Hu Y, Berck M, Vignoud G, Samuel ADT, et al. (2019) Structured odorant response patterns across a
  complete olfactory receptor neuron population. Neuron 101:950. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6756926/>.
  Data: <https://github.com/samuellab/Larval-ORN>.
- Badel L, Ohta K, Tsuchimoto Y, Kazama H (2016) Decoding of context-dependent olfactory behavior in Drosophila. Neuron
  91:155. Supplemental Information: <https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc1.pdf>; Table S2:
  <https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc2.xls>.
- Endo K, Tsuchimoto Y, Kazama H (2020) Neuron 108:367. Article with supplement:
  <https://ars.els-cdn.com/content/image/1-s2.0-S0896627320305730-mmc3.pdf> (the dilution sentence and its raw glyphs
  checked in the helper's text copy).
- Barth J, Dipt S, Pech U, Hermann M, Riemensperger T, Fiala A (2014) J Neurosci 34:1819.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/>. Fig. 3A (ORN) and Fig. 5A (PN) re-read.
- Pelz D, Roeske T, Syed Z, de Bruyne M, Galizia CG (2006) The molecular receptive range of an olfactory receptor in
  vivo (Drosophila melanogaster Or22a). J Neurobiol 66:1544. Methods and Table 1 re-read. KOPS copy:
  <https://kops.uni-konstanz.de/entities/publication/c8230e22-d285-4d39-8ecb-1cfb43d25493>.
- Galizia CG, Münch D, Strauch M, Nissler A, Ma S (2010) Integrating heterogeneous odor response data into a common
  response model: a DoOR to the complete olfactome. Chem Senses 35:551.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2924422/>. Methods re-read.
- de Bruyne M, Clyne PJ, Carlson JR (1999) J Neurosci 19:4520. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6782632/>. The
  pb3 passage re-read.
- Wang JW, Wong AM, Flores J, Vosshall LB, Axel R (2003) Two-photon calcium imaging reveals an odor-evoked map of
  activity in the fly brain. Cell 112:271. Methods and Fig. 3-4 legends re-read.
- Jennings et al. (2023), PID-calibrated vapour concentrations of odorants in mineral oil and other solvents.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10208748/>. Table 2 re-checked.
- Cometto-Muñiz JE, Cain WS, Abraham MH (2003) Quantification of chemical vapors in chemosensory research. Chem Senses
  28:467. <https://escholarship.org/uc/item/3qf2426m>. Table re-checked.
- Hong EJ, Wilson RI (2015) Simultaneous encoding of odors by channels with diverse sensitivity to inhibition. Neuron
  85:573. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/>. The quotes used were re-checked.
- Churgin MA et al. (2025) eLife 12:RP90511. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11896609/>. Fig. 1G re-viewed.
- Hige T, Aso Y, Modi MN, Rubin GM, Turner GC (2015) Neuron 88:985. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/>.
- Honegger KS, Campbell RAA, Turner GC (2011) J Neurosci 31:11772. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/>.
- Campbell RAA et al. (2013) J Neurosci 33:10568. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3685844/>.
- Lin AC, Bygrave AM, de Calignon A, Lee T, Miesenböck G (2014) Nat Neurosci 17:559.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/>.
- Davidson AM, Kaushik S, Hige T (2023) eNeuro 10:ENEURO.0275-23.2023.
  <https://www.eneuro.org/content/10/10/ENEURO.0275-23.2023>.
- Hussain A et al. (2018) eLife 7:e32018. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5790380/>.
- Mathew D, Martelli C, Kelley-Swift E, Brusalis C, Gershow M, Samuel ADT, Emonet T, Carlson JR (2013) PNAS 110:E2134.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3677458/>.
- Turner GC, Bazhenov M, Laurent G (2008) J Neurophysiol 99:734 (odor panels re-read).

**Read by helper agents in this session (not re-checked unless stated above)**
- Kreher SA, Mathew D, Kim J, Carlson JR (2008) Neuron 59:110, supplement Table S1 (3-octanol at 10⁻² and 10⁻⁴).
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2496968/>.
- Mathew et al. 2013 Dataset S1 (`1306976110_sd01.xlsx`) and Fig. 2.
- Galizia et al. 2010 supplement, Table S3. <https://pmc.ncbi.nlm.nih.gov/articles/instance/2924422/bin/bjq042v2_1.pdf>.
- Grabe V et al. (2016) Cell Rep 16:3401, Tables S1 (driver coverage) and S3 (Or83c responses).
  <https://pure.mpg.de/pubman/item/item_2328184>.
- Delivery methods: Dobritsa et al. 2003, Goldman et al. 2005, Kreher et al. 2005 (Neuron; Wayback copies of cell.com
  PDFs); Hallem, Ho & Carlson 2004; Hallem & Carlson 2006; Dweck et al. 2013; Stökl et al. 2010; Riemensperger et al.
  2005; Shang et al. 2007 (PMC2866183); Claridge-Chang et al. 2009 (PMC3920284); Pech et al. 2015 supplement.
- Andersson MN (2011) thesis, SLU, <https://pub.epsilon.slu.se/id/document/1531>. Andersson, Schlyter, Hill & Dekker
  2012, Chem Senses 37:403, could not be obtained (abstract only).
- Root CM et al. (2008) Neuron 59:311 (PMC2539065); Chou YH et al. (2010) Nat Neurosci 13:439 (Table S2); Schlegel P et al.
  (2021) eLife (PMC8298098); Olsen & Wilson 2008 (PMC2824883); Martelli et al. 2013 (PMC3678969); Jayaraman & Laurent
  2007; Hendel et al. 2008 (PMC6670390); Prisco L et al. (2021) eLife 10:e74172 (PMC8741211), claw and APL panels.
- MaleCNS synapse statistics (GABA-LN → ORN and uPN; helper analysis of `~/fly-data/raw`).

**Model outputs read (no new simulation)**
- `experiments/odor_probe54.json` (equalization measures, DoOR and both fill tiers), `experiments/odor_equalization_check.py`,
  `experiments/receptor_fills.py`, `brainfly/odors.py`; MaleCNS cell-type counts via `brainfly.hybrid.mcns_types()`.

**Project notes relied on** (`research_notes/Rung 9 learning data/`): `oct_mch_input.md`, `weak_input_gain.md`,
`hige2015_specificity.md`, `lateral_excitation.md`, `kc_classes_and_apl.md`, `mbon11_input.md`, `mbon11_kc_activity.md`.

