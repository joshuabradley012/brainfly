# Which receptor neurons and glomeruli respond to 4-methylcyclohexanol: a breadth search beyond DoOR

Read 2026-10-11.

**The question.** In flies, 4-methylcyclohexanol (MCH) and 3-octanol (OCT), each at Hige et al. 2015's "2% of saturated
vapor", drive MBON-γ1pedc about equally and reach Kenyon cell sets of about the same size. In the model, MCH's receptor
input (`experiments/receptor_fills.py`, `RECOMMENDED`: VA3 0.70, D 0.21, everything else 0.10 or less) is narrow, and
most of its Kenyon cells are also OCT's. `experiments/odor_mch_input_sensitivity.py` concluded that flies' MCH is
"probably broader at the projection neurons than the receptor-level evidence makes it, through lateral excitation,
receptor responses no dataset has, or both." This note asks which olfactory receptor neuron (ORN) classes and glomeruli
respond to MCH, looking for evidence that [oct_mch_input.md](oct_mch_input.md),
[lateral_pn_responses.md](lateral_pn_responses.md), [mch_oct_equalization.md](mch_oct_equalization.md) and
[oct_mch_concentration.md](oct_mch_concentration.md) don't already have. It looks especially at ionotropic receptor
(Ir) neurons, gustatory receptor (Gr) and CO2 pathways, recordings published after 2015, and imaging across many
glomeruli.

**Conventions** (as in the other notes)
- Quotes are exact.
- "(fig., approx.)" = read off a figure with a pixel grid calibrated on its axis ticks; each case gives the calibration.
- "(derived)" = my arithmetic on published numbers or tables.
- "Not reported" = I searched the full text, legends and supplement (or the data files) and the value is not there.
- "× Hige" = the estimated concentration at the antenna divided by Hige's 2% of saturated vapour (SV). It uses
  [oct_mch_concentration.md](oct_mch_concentration.md) §1.2's method (oil headspace about 0.3 of SV at 1% v/v, range
  0.2–0.5). Each value is uncertain by ×/÷ 2.5–5. New estimates are marked (derived).
- Glomeruli of the Ir and Gr classes, by receptor and sensillum: VM1 (Ir92a, ac1), VL2p (Ir31a, ac1), VL1 (Ir75d; ac1,
  ac2, ac4), DP1l (Ir75a, ac2), VC5 (Ir41a, ac2), DL2d/v (Ir75a/b/c, ac3), VM4 (Ir76a, ac4), VL2a (Ir84a, ac4), DP1m and
  DC4 (Ir64a, sacculus chamber III), V (Gr21a/Gr63a, ab1C). The model has receptor neurons for all of them (MaleCNS
  types ORN_VM1 ... ORN_V), but `RECOMMENDED` drives none of them for either odour.
- "Model" values are `receptor_fills.RECOMMENDED` (DoOR-equivalent units; the model drives value × 200 spikes/s).

## Summary

1. **No new receptor-level evidence broadens MCH much.** The receptor picture stays narrow: VA3 strong, D moderate,
   a handful weak. The new material mostly confirms `RECOMMENDED`, and adds one plausible untested receptor (DP1m).
2. **What is new, glomerulus by glomerulus** (evidence strength in brackets):
   - **Coeloconic Ir glomeruli (VM1, VL2p, VL1, DP1l, VC5, DL2d/v, VM4, VL2a).** [Moderate, against.] The notes had
     Silbering et al. 2011's four whole-sensillum numbers. Ranked among all 171 odours of that screen (derived from
     DoOR's import, 1% v/v):
     - ac1 (VM1, VL2p, VL1): MCH +29 spikes/s, 28 odours higher. The median odour gives +19.5, so MCH is only about
       10 above a typical odour. Esters and terpenes that Ir neurons are not known to detect give 30–42.
     - ac2: −6 (149 odours higher). ac3 (Or35a removed): −0.5 (154 higher).
     - ac4 (VM4, VL2a, VL1): −15.1. Only 5 of 171 odours inhibit ac4 more.
     - So MCH does not excite ac2–ac4 Ir neurons, and it inhibits ac4. Its ac1 effect is small and cannot be assigned
       to a neuron. No Ir-specific MCH recording exists (Not reported).
   - **DP1m (Ir64a, sacculus).** [Low for MCH; moderate for OCT.] The best new candidate among untested receptors.
     - Its ORNs are broadly tuned: "DP1m was activated by acidic and non-acidic odorants" (Ai et al. 2010).
     - That includes 1% 3-octanol: about 86 in integrated ΔF/F, against about 230 for the best acid (fig., approx.;
       about 10–25× Hige, derived). MCH was never tested on Ir64a neurons (Not reported).
     - Hussain et al. 2018's GH146 "DP1" is DP1m: GH146 labels one DP1m projection neuron (PN), and DP1l is "GH146
       negative" (Grabe et al. 2016). From Hussain's source data (derived; n = 9 young flies; about 3–4× Hige):
       DP1m PNs give MCH 53 ± 6% and OCT 86 ± 4% ΔF/F₀. Badel et al. 2016: MCH 15%, OCT 10%.
   - **DA2, DC2, DL1, DM1, DM2, DM3, VA2.** [Moderate, against.] Lüdke, Kumaraswamy & Galizia 2025 imaged seven receptor
     lines with gas-chromatography-purified odorants. Their main text never names MCH, but their tables do.
     - Racemic MCH is "category 0" (no significant response) at all seven receptors, and so are both of its GC peaks
       where they were tested.
     - Largest MCH value at 10⁻², as a fraction of each receptor's largest response: 0.00–0.02 (derived).
     - This includes DA2 (Or56a): MCH 0.20 ± 0.52 against geosmin 23.26 ± 10.04. And DC2 (Or13a): MCH 0.24 ± 0.24
       against OCT 8.96 ± 3.87.
     - Caveat: their delivery is weak, about 0.1–0.5× Hige (derived, rough). It also misses OCT at Or22a, where single
       sensillum recordings find 57 spikes/s. So these nulls rule out strong responses, not weak ones.
   - **DL1 (Or10a).** [Moderate that it is small and shared.] MCH ≈ OCT in every dataset:
     - ab1D: 7 vs 2 net spikes/s (in the notes).
     - Lüdke 2025: 0.21 vs 0.44, both category 0, against ethyl benzoate 10.08.
     - Badel PNs: 37 vs 27%.
     - New: Avishai & Parnas 2025's GH146 PNs at a "final odor concentration" of 5 × 10⁻² (well above Hige):
       peak ΔF/F 5.3–5.6 vs 5.1–5.3 with GCaMP6f, and 2.0 vs 1.7 with GCaMP7b (fig., approx.).
   - **DL5 and DM3: PN responses without receptor support, in a third lab.** [Moderate.] Avishai & Parnas 2025 picked
     glomeruli "located in the dorsal plane of the AL", not by response. At 5 × 10⁻², MCH gives PN peaks (fig., approx.):
     - DL5: 3.5–3.6 (OCT 5.3–6.3) with GCaMP6f; 0.75 (OCT 0.55) with GCaMP7b.
     - DM3: 3.5–4.0 (OCT 8.5) with GCaMP6f; 1.13 (OCT 1.15) with GCaMP7b.
     - DL3: 0.2–0.5 (OCT 2.4–3.6) with GCaMP6f; 0.49 (OCT 0.85) with GCaMP7b.
     - DL5's ORNs are inhibited by MCH and DM3's don't respond (oct_mch_input.md §7–8; Lüdke: Or47a 0.00). So this
       replicates Badel's DL5 and DM3 breadth as projection-neuron, not receptor, activity, at a high concentration.
   - **DC1 and VC2.** [Low; nothing changes.] Hussain 2018's numbers (derived; Grunwald Kadow lab; probably about 3–4×
     Hige): MCH DC1 192 ± 28% and VC2 117 ± 17%. This is a second lab after Barth 2014 (DC1 109, VC2 168). The receptor
     values stay small: Or19a 5 spikes/s, pb1B about 17 net (in the notes).
   - **V (CO2 neurons, Gr21a/Gr63a).** [Untested.] No study tested MCH on ab1C (Not reported). MacWilliam et al.
     2018's 60-odorant screen drew 54 odorants from Hallem & Carlson 2006's panel, which has neither odour. DoOR's
     ab1C data have OCT (−7 spikes/s, Turner & Ray 2009) but no MCH.
   - **Gustatory neurons.** [Real, but not an antennal lobe pathway.] Wei, Lam & Kazama 2025: MCH vapour excites
     labellar Gr5a (sweet) and Gr66a (bitter) taste neurons. The default stimulus was 0.5 v/v; taste sensilla were
     tested with MCH at 1% in contact. These neurons project to the subesophageal zone, not to the antennal lobe or
     the calyx.
   - **DA4l (Or43a).** [Low; analog only.] Still never tested with MCH. Wetzel et al. 2001's rule for Or43a's ligands,
     "All active ligands share the cyclic 6-carbon structure with a polar functional group attached to the ring", fits
     MCH. But their oocyte assay also rejected 1-hexanol, Or43a's best ligand in vivo, so it is a weak guide.
3. **Side findings for OCT that matter for the ratio.**
   - Lüdke 2025: "we assume that commercial 3‐octanol is consistently contaminated with 1‐octen‐3‐ol, the best ligand
     for Or13a, leading to a false positive response to 3‐octanol in the literature". Purified OCT is a "medium" Or13a
     ligand (8.96 against 2-heptanol's 34.36). Commercial OCT, which flies in Hige's experiment also smelled,
     presumably carries the contaminant.
   - DP1m answers OCT (Ai 2010). Neither DoOR nor `RECOMMENDED` gives OCT any DP1m drive.
4. **What this changes in the earlier conclusion.**
   - "Receptor responses no dataset has": the coeloconic Ir neurons are now effectively tested, and they are not MCH
     targets. The untested receptors that remain plausible are DP1m (Ir64a), DA4l (Or43a) and DL4 (Or85f/Or49a). DM6
     (Or67a) and VM2 (Or43b) remain untested too.
   - "Lateral excitation": the projection-neuron breadth without receptor support (DL5, DM3, VM4) now appears in a
     third lab. That points to antennal lobe mechanisms, as lateral_pn_responses.md argued for other glomeruli.

## 1. Coeloconic (Ir) sensilla: Silbering et al. 2011 in context

[Silbering et al. 2011, J Neurosci 31:13357](https://pmc.ncbi.nlm.nih.gov/articles/PMC6623294/). The values are from
DoOR's import of the screen (`ac1.csv`, `ac2.csv`, `ac3_noOr35a.csv`, `ac4.csv`, column `Silbering.2011.WT`; 171 odour
entries plus the spontaneous-rate row). The paper says 168 odours.

**Method quotes.**
- "Odors (Sigma and Fluka) were diluted to 1% (v/v) unless otherwise noted in the figures".
- Fig. 1 legend: "Electrophysiological responses in the four antennal coeloconic sensilla classes (ac1–ac4) to 168 odors
  (mean ± SEM; n ≥ 4, mixed genders), representing the summed, solvent-corrected activities of the IR-expressing neurons
  they house".
- "we performed our screen of this sensillum class in OR35a mutants to remove contributions of this receptor to the
  analyzed odor responses" (ac3).
- "Notably, the vast majority of IR neuron agonists belong to two chemical classes: amines and carboxylic acids".
- Delivery: recordings "were performed essentially as described (Benton et al., 2007)". I did not re-read Benton 2007.
  I assume a pipette-puff method like the Carlson lab's, which oct_mch_concentration.md §1.2 puts at about 1–2× Hige
  for 10⁻² (my inference).

**MCH and OCT against the whole screen** (net spikes/s; derived from the DoOR table):

| Sensillum (Ir glomeruli) | Median of 171 odours | 75th / 90th percentile | MCH (odours higher) | OCT (odours higher) | Cyclohexanol / cyclohexanone |
|---|---|---|---|---|---|
| ac1 (VM1, VL2p, VL1) | 19.5 | 26.5 / 36.5 | **29.0** (28) | 8.5 (144) | 14.0 / 14.5 |
| ac2 (DP1l, VC5, VL1) | 10.5 | 21.5 / 41.0 | −6.0 (149) | 15.0 (67) | 0.0 / 6.0 |
| ac3, Or35a mutant (DL2d/v) | 18.0 | 24.0 / 30.0 | −0.5 (154) | 14.0 (106) | −2.75 / 10.0 |
| ac4 (VM4, VL2a, VL1) | −0.5 | 2.3 / 10.9 | **−15.1** (165) | −5.0 (135) | −16.0 / 4.3 |

- The odours above MCH in ac1 include butyl acetate 41.8, ethyl hexanoate 40.3, propyl acetate 39.3 and hexyl acetate
  38.0, as well as the amines and acids that are its real ligands (ammonium hydroxide 141.8, dimethylamine 84.0).
- The five odours more inhibitory than MCH at ac4 are n-methylpiperidine (−33.5), cyclohexylamine (−25.5),
  2-methylphenol (−20.3), cyclohexanol (−16.0) and Z3-hexenol (−15.3).
- **Imaging of single Ir populations did not include MCH.** "For each IR population, we screened the subset of odors
  shown to evoke electrophysiological activity in the corresponding sensillum class in the antenna (Figs. 1, 2A)."
  DoOR's import of that imaging (`Silbering.2011.AL`, `Silbering.2011.AL_8a`, for Ir31a, Ir41a, Ir64a, Ir75a, Ir75d,
  Ir76a, Ir84a, Ir92a) has no MCH entry.
- Other coeloconic screens have no MCH (searched): Yao et al. 2005 (45 odours; DoOR `Yao.2005.WT`), Benton et al.
  2009, Abuin et al. 2011, Min et al. 2013, Marshall et al. 2010 (DoOR `Marshall.2010.WT`).

**Reading (mine).**
- These are summed responses of three or four neurons, so the ac1 value cannot be assigned to VM1, VL2p or VL1.
- MCH is about 10 spikes/s above a typical odour in ac1. That is weak, and the screen's own text says Ir neurons answer
  amines and acids.
- MCH inhibits ac4. So Barth et al. 2014's PN response of 241% at VM4 (Ir76a, ac4; oct_mch_input.md §8) has no
  receptor support. Badel's VM4 gives MCH 10% against OCT 48%.
- PN data for the ac1 glomeruli don't single out MCH: Barth's VM1 gives 161% for both odours; Badel's VM1 gives 24 vs
  36% (MCH vs OCT), and VL2p −3 vs −10%.

## 2. The sacculus Ir64a neurons and DP1m

**Ai et al. 2010, Nature 468:691** ([PMC3105465](https://pmc.ncbi.nlm.nih.gov/articles/PMC3105465/); supplement
`41586_2010_BFnature09537_MOESM268_ESM.pdf` from nature.com).
- IR64a-GAL4 > G-CaMP, two-photon imaging of DC4 and DP1m terminals.
- "All acids examined, but not non-acidic odorants, activated DC4 (Fig. 3a and b, and Supplementary Table 1). In
  contrast, DP1m was activated by acidic and non-acidic odorants (Fig. 3b and Supplementary Fig. 3)."
- "ectopic expression of IR64a induces odor sensitivity in VM4 to organic acids and 3-octanol, which normally activate
  DP1m (Supplementary Fig. 5)".
- Stimulus: "Odorants and acids were dissolved in water or paraffin oil (v/v%)". The water list is the inorganic and
  short-chain acids, vinegar, sodium hydroxide, methanol, ethanol, formaldehyde and four short aldehydes; "Other
  odorants were dissolved in paraffin oil. Diluted odorants (300ul) or control solvent were placed in 16 ml glass
  vials". A pump generated a "22ml/min flow of humidified air-stream", and the odour valve opened "for 1 second to allow
  odorant in the head space of the vial to be delivered to the fly antennae". So 3-octanol was undiluted headspace of 1%
  in paraffin oil, about 10–25× Hige (derived).
- Fig. 3b, DP1m bars (fig., approx.). Calibration: on the 946 × 590 px nature.com image, the y-axis (∫ΔF/F Δt) ticks
  0, 100, 200 and 300 sit at rows 510, 457.5, 405 and 352.5, so 0.525 px per unit. Values:
  - 1% "octan-3-ol" 86.
  - 1% benzaldehyde 110; 1% β-citronellol 187.
  - 1% isobutyric acid 230 (the largest DP1m bar); 1% butyric acid 229.
  - Mineral oil about 2; air about 13.
  - So OCT is about 0.37 of DP1m's largest response at about 10–25× Hige (derived).
- Supplementary Table 2 (the legend's scale is "-, ΔF/F<10%; +, ΔF/F 10~20%; ++, ΔF/F 21~40%; +++, ΔF/F >40%"):
  "1% Octanol" gives DC4 "-" and DP1m "++".
- Supplementary Table 1 (DC4 only, 1% unless stated) includes "3-octanol -". Neither table includes MCH.

**Ai et al. 2013, J Neurosci 33:10741** ([PMC3693055](https://pmc.ncbi.nlm.nih.gov/articles/PMC3693055/)).
- "β-citronellol, benzaldehyde, and 3-octanol, all of which strongly activated the DP1m glomerulus in vivo, failed to
  elicit inward currents in IR64a+IR8a-expressing oocytes (data not shown)."
- One ambiguity: this paper's Fig. 1 legend abbreviates "Oct, 1-octanol (1%)". The 2010 figure is labelled
  "octan-3-ol". MCH: Not reported in either paper.

**Hussain et al. 2018, eLife 7:e32018** ([PMC5790380](https://pmc.ncbi.nlm.nih.gov/articles/PMC5790380/)). The notes
already list its glomeruli; the numbers and the DP1 identity are new here.
- Legends: "(C, C´) GCaMP fluorescence changes are recorded in three different responsive glomeruli (DC2, DM6 and DP1)
  upon stimulation with 3-octanol (12 mM). (D-D´) GCaMP fluorescence changes were measured in three responsive glomeruli
  (DC1, DP1 und VC2) upon stimulation with 4-methylcyclohexanol (16 mM) in 1, 4 and 6 weeks old flies."
- Setup: GH146-Gal4 > GCaMP3, two-photon. "A custom-built device was used as odor delivery system to supply odors with a
  constant flow rate of 1 ml/s to the fly's antennae for 2 s." Glomeruli were imaged "at three different levels of the
  AL", so the "responsive glomeruli" are those in the imaged planes, not a full survey.
- Concentrations (derived):
  - MCH 16 mM is about 0.2% v/v (MW 114.19, density 0.914).
  - OCT 12 mM is about 0.19% v/v (MW 130.23, density 0.822). The source data label the OCT series "3oct (PO)", i.e. in
    paraffin oil.
  - Both are close to Barth et al. 2014's 1:500 (OCT) and 1:750 (MCH). The two-photon delivery is described only as
    the sentence above, so its air dilution is Not reported. If the 1 ml/s passes through the vial with no further
    dilution, as in Barth's setup, this is about 3–4× Hige (oct_mch_concentration.md §1.2). (Hussain's widefield
    experiments instead injected the cup's headspace into a 2000 ml/min stream.)
- Per-fly maximum ΔF/F₀ (%), 1-week-old flies, n = 9 each (derived: mean ± SEM of the values in
  `elife-32018-fig2-data1-v2.xlsx`, sheets "Fig. 2C" and "Fig. 2D"):

  | Odour | Glomerulus 1 | Glomerulus 2 | Glomerulus 3 |
  |---|---|---|---|
  | OCT (12 mM) | DC2 113 ± 14 | DM6 116 ± 17 | DP1 86 ± 4 |
  | MCH (16 mM) | DC1 192 ± 28 | DP1 53 ± 6 | VC2 117 ± 17 |

- **Which DP1.** Grabe et al. 2016, Table S1: "DP1l Ac2 Ir75a ... GH146 negative". DP1m (Sac III, Ir64a) has "1 (0)"
  GH146-labelled PNs in each sex. So GH146's "DP1" is DP1m. Barth's GH146 "DP1" (OCT 39%; MCH not among its listed
  values of 27% and above) is presumably DP1m too.
- Badel 2016 (NP225; oct_mch_input.md §8): DP1m MCH 15%, OCT 10%.

**Reading (mine).**
- DP1m is the one Ir glomerulus with a broadly tuned receptor that answers non-acidic odours, alcohols included.
- Its PNs answer MCH in two labs (53% in Hussain, 15% in Badel).
- MCH was never tested on its ORNs. OCT was, and drives them, more strongly than MCH drives the PNs in Hussain's data.
  So DP1m would broaden both odours, not make MCH more distinct.

## 3. Purified odorants on seven receptors: Lüdke, Kumaraswamy & Galizia 2025

[Eur J Neurosci 61:e70036](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891828/) (doi:10.1111/ejn.70036). The tables
are in the supplementary files (Table S1, Appendix Table 1, Table S2 = the Or10a sheet, Appendix Table 2 = the other
six), obtained through Europe PMC.

**Method quotes.**
- "Odorants were diluted in mineral oil (MOL, Acros Organics, CAS 8042‐47‐5) at 10−2, 10−4, and 10−6."
- "One‐milliliter headspace was injected ... into a gas chromatograph (GC ...) ... at split mode with the injector
  temperature set to 200°C, the split flow to 15 mL min−1, and the split ratio to 10."
- The column effluent was split between the detector and the fly. "The transfer line ended in a glass tube directed to
  the Drosophila antennae for calcium imaging (inner diameter 7 mm, ending with a 2 mm opening, air stream 1 mL s−1,
  with the exit positioned ~2 mm from the antenna)."
- Imaging: "Calcium imaging of dendrites and somata of olfactory sensory neurons on the third antennal segment", with
  GCaMP6m under each Or-Gal4. Animals: Or10a 107, Or13a 66, Or22a 102, Or42b 32, Or47a 97, Or56a 50, Or92a 73.
- "Responses were classified as significant if their magnitude was 2.5 times higher than noise".
- Categories (from the text): 3 = significant down to 10⁻⁶; 2 = "significant to dilution of 10−2 and 10−4"; 1 =
  "significant only to the highest concentration, dilution 10−2"; 0 = not significant.
- MCH source (Appendix Table 1): "4-methylcyclohexanol (rac) 589-91-3 hexahydro-p-cresol 153095-250ML 98 % Aldrich". The
  GC split it into two peaks, "peak1" and "peak2" (presumably the cis and trans isomers; my inference).

**Values** (modelled responses as tabulated, mean ± SD or SEM as tabulated, at 10⁻² / 10⁻⁴ / 10⁻⁶; category; n):

| Receptor (glomerulus) | Largest at 10⁻² | MCH (racemic) | OCT |
|---|---|---|---|
| Or10a (DL1) | ethyl benzoate 10.08 ± 1.61 | 0.21 ± 0.38 / 0.22 ± 0.14 / −0.15 ± 0.08; 0; n 5 (peak1 0.07, peak2 0.14 at 10⁻²) | 0.44 ± 0.29 / 0.20 ± 0.18 / 0.14 ± 0.14; 0; n 5 |
| Or13a (DC2) | 2-heptanol 34.36 ± 5.59 (1-octen-3-ol 29.62 ± 7.53) | 0.24 ± 0.24 / 0.31 ± 0.13 / 0.00 ± 0.00; 0; n 7 | 8.96 ± 3.87 / 7.53 ± 1.36 / 0.70 ± 0.42; **2**; n 9 |
| Or22a (DM2) | ethyl propionate 66.94 ± 12.49 | 0.19 ± 0.14 / 0.05 ± 0.54 / 0.35 ± 0.22; 0; n 8 | −0.01 ± 2.89 / 0.05 ± 0.90 / 0.53 ± 0.51; 0; n 4 |
| Or42b (DM1) | ethyl propionate 27.50 ± 3.10 | −0.13 ± 0.48 / −0.21 ± 0.26 / −0.00 ± 0.11; 0; n 5 | 0.00 ± 0.00 / −0.00 ± 0.71 / −0.11 ± 0.53; 0; n 5 |
| Or47a (DM3) | pentyl acetate 68.98 ± 10.29 | 0.00 ± 0.00 / 0.23 ± 0.23 / 0.46 ± 0.20; 0; n 9 | 13.43 ± 6.32 / 0.58 ± 0.34 / −0.22 ± 0.13; **1**; n "36,10" |
| Or56a (DA2) | geosmin 23.26 ± 10.04 | 0.20 ± 0.52 / 0.13 ± 0.29 / −0.00 ± 0.33; 0; n 5 | −0.34 ± 0.20 / −0.33 ± 0.86 / −0.74 ± 0.03; 0; n 3 |
| Or92a (VA2) | 2,3-butanedione 42.92 ± 14.07 | 0.49 ± 0.00 / −0.07 ± 0.25 / 0.38 ± 0.47; 0; n 3 (peak1 0.12, peak2 −0.37 at 10⁻²) | 0.35 ± 1.20 / 0.41 ± 0.89 / 0.52 ± 0.52; 1 (as tabulated); n 12 |

- MCH at 10⁻² as a fraction of each receptor's largest response (derived): Or10a 0.021, Or13a 0.007, Or22a 0.003,
  Or42b < 0, Or47a 0.00, Or56a 0.009, Or92a 0.011.
- OCT: Or13a 0.26, Or47a 0.19, Or10a 0.044, the others about 0 (derived).
- Text on DoOR: "for weaker ligands, DoOR generally overestimated the response, indicating false positives in the
  database".
- And: "the response to 3‐octanol (OC3L) in Or13a is highly overestimated in the DoOR database. Indeed, in our data, we
  found that 3‐octanol was systematically contaminated with 1‐octen‐3‐ol, creating false‐positive recordings
  (Figure 7)". Table S1 lists "1-octen-3-ol contamination" and "pentyl acetate contamination" as separate stimuli. No
  contaminant is listed for MCH.

**How strong was the stimulus?** (derived, rough)
- Per injection, about 1/11 of 1 mL of vial headspace enters the column (split ratio 10), and roughly half of the
  column effluent goes to the fly.
- It elutes as a peak lasting a few seconds into a 1 mL/s air stream. So the antenna sees about 1–2% of the vial's
  headspace concentration.
- Münch & Galizia 2016 (same lab, same vials) injected 2 mL of headspace into 60 mL/min, about 50% of headspace
  (oct_mch_concentration.md §1.2). That is roughly 25–50 times more.
- With that study at about 7.5× Hige, Lüdke's 10⁻² is about 0.15–0.3× Hige (range about 0.1–0.5×).
- Consistent with this, purified OCT gives nothing at Or22a. At about 0.8× Hige, ab3A fires 57 net spikes/s to OCT
  (de Bruyne 2001).

**Reading (mine).**
- At about a quarter of Hige's concentration, purified MCH drives none of these seven receptors detectably.
- For DA2 and DC2 this disagrees with the older imaging values behind DoOR (MCH 0.106 of geosmin at Or56a in Münch 2016;
  0.42 of OCT at Or13a in Galizia 2010). It agrees with the single-sensillum and larval data (ab6A −15 spikes/s; larval
  Or13a no response).
- A weak real response, scaled down by about 30× in concentration, would also fall below detection: 0.106 × 30^−0.7 ≈
  0.01 of maximum for DA2 (derived, Hill coefficient 0.7). So this cannot distinguish "contaminant" from "weak".
- Either way it supports `RECOMMENDED`'s near-zero MCH values at DA2 (0.02), DC2 (0.02), DM3 (0.01) and DL1 (0.03).

## 4. Projection-neuron imaging that included MCH

**Avishai & Parnas 2025, Commun Biol 8:1555** ([PMC12612080](https://pmc.ncbi.nlm.nih.gov/articles/PMC12612080/);
doi:10.1038/s42003-025-08922-y). A study of dopamine in the antennal lobe; MCH, OCT and isoamyl acetate were the odours.
- "Odors were diluted in mineral oil (Sigma-Aldrich). For all odors, the final odor concentration reaching the flies was
  5 × 10−2." How that was produced: Not reported here (only "as previously described"). It is well above Hige's
  concentration (my reading; if it means 5% v/v-equivalent headspace, about 10–25× Hige, derived).
- Glomerulus choice: "we identified using the in vivo AL atlas100, five AL glomeruli located in the dorsal plane of the
  AL: D, DL3, DL1, DL5 and DM3." They were chosen by position, not by response.
- Fig. 3: "GCaMP6f was expressed in GH146 ePNs"; "2-second-long odor pulses". MCH n for DL3, DL1, DL5 and DM3: "DA, 10,
  13, 9, 8; ES, 10, 11, 10, 10".
- Fig. 9: "LexAop-GCaMP7b was expressed in ePNs using GH146-LexA driver line"; "5-s-long odor pulses"; control n for D,
  DL3, DL1, DL5, DM3 = "13, 9, 13, 11, 10".
- Text: "In the case of MCH, a significant increase in odor response was observed in only one glomerulus, DL1". That is
  the dopamine effect, not the odour response.
- The Supplementary Data hold only statistics. So the values below are my readings of the "before" bars (fig., approx.),
  as peak ΔF/F (a fraction; 1 = 100%):
  - Fig. 3: on the 1452 × 2327 px Springer image, each panel calibrated on its own ticks. For example, DL1 MCH has
    ticks 14, 7, 0 at rows 1356, 1414, 1472 (8.29 px per unit). The two "before" bars (control and dopamine groups)
    give the range.
  - Fig. 9: on the 995 × 1943 px image, ticks 5, 2.5, 0 (about 36.3 px per unit). Control-genotype bars.

  | Glomerulus | MCH, GCaMP6f (Fig. 3) | OCT, GCaMP6f | MCH, GCaMP7b (Fig. 9) | OCT, GCaMP7b | Isoamyl acetate, GCaMP7b |
  |---|---|---|---|---|---|
  | D | not shown | not shown | 0.29 | 0.33 | 0.29 |
  | DL3 | 0.2–0.5 | 2.4–3.6 | 0.49 | 0.85 | 0.81 |
  | DL1 | 5.3–5.6 | 5.1–5.3 | 1.97 | 1.70 | 2.16 |
  | DL5 | 3.5–3.6 | 5.3–6.3 | 0.75 | 0.55 | 0.84 |
  | DM3 | 3.5–4.0 | 8.5 | 1.13 | 1.15 | 1.21 |

- The two indicators disagree on MCH/OCT: DL5 0.6 vs 1.4, DM3 0.44 vs 0.98, DL3 about 0.1 vs 0.58 (derived). Genotype,
  pulse length and flies all differ.

**Reading (mine).**
- At a high concentration, MCH drives GH146 PNs in DL1, DL5 and DM3 strongly, in a third lab.
- DL1's receptor responds to MCH about as much as to OCT, and weakly (§3).
- DL5's ORNs are inhibited by MCH (Barth ORN −30%) and coded 0 at ab4A. DM3's are silent at 10⁻² (ab5B −2 spikes/s;
  Or47a 0.00). Larval Or33b/Or47a has an MCH EC50 of 10⁻²·⁴⁶ in water (oct_mch_concentration.md §1.4), so some DM3
  receptor drive at 5 × 10⁻² is possible.
- These PN responses therefore come mainly from the antennal lobe, not from receptor input. They match Badel's (DL5 77%,
  DM3 87%) and Yu et al. 2004's ("PNs innervating the three glomeruli DM6, DM2, and DM3 exhibited significant responses
  to MCH alone"). lateral_pn_responses.md already treats DL5 as a glomerulus with real lateral firing, and Badel's DM3 as
  a copy of DM6.

**Hussain et al. 2018** (§2; Grunwald Kadow and Sigrist labs): MCH 16 mM gives DC1 192 ± 28%, DP1m 53 ± 6% and VC2
117 ± 17% (derived). The concentration is similar to Barth 2014's (DC1 109, VC2 168), so these two PN datasets agree
in a second lab.

**Other PN datasets checked, with no glomerulus-level MCH values:**
- Rozenfeld et al. 2019 (Cell Rep): GH146 > GCaMP6f responses to "isoamyl acetate (IAA), 4-methylcyclohexanol (MCH),
  3-octanol (3-OCT), and linalool", but for the whole lobe only.
- Frechter et al. 2019 (eLife; 84 identified PNs, whole-cell): its 36-odour set (Supplementary file 5) has neither MCH
  nor OCT.
- Endo et al. 2020: data on request (in the notes). Someya et al. 2025 (Cell 188:6892; lateral horn): not accessed.

## 5. Gr and CO2 pathways

- **CO2 neurons (ab1C, Gr21a/Gr63a → V).** MCH on ab1C: Not reported.
  - DoOR's ab1C datasets (Kwon 2007, Turner 2009, de Bruyne 2001, Marshall 2010) have no MCH entry. Turner & Ray 2009
    give OCT −7 spikes/s, via DoOR.
  - MacWilliam et al. 2018 ([PMC5871350](https://pmc.ncbi.nlm.nih.gov/articles/PMC5871350/)): "we selected a large
    panel of 60 structurally-diverse odorants, of which 54 were randomly selected from a larger panel that have been
    tested for activity on 24 Or receptors, the majority of those present in the antenna (Hallem and Carlson, 2006)".
    MCH is not mentioned.
  - Kumar et al. 2020 ([PMC7552916](https://pmc.ncbi.nlm.nih.gov/articles/PMC7552916/)) and Grabe 2016's Table S3
    (Gr21a column): no MCH.
- **Labellar taste neurons.** Wei, Lam & Kazama 2025, eLife 13:RP101440
  ([PMC12321263](https://pmc.ncbi.nlm.nih.gov/articles/PMC12321263/)).
  - "Odor-evoked PER requires the function of sugar-sensing GRNs but not olfactory organs. Calcium imaging and
    electrophysiological recording show that GRNs directly respond to odors."
  - MCH was one of six odours. Gr5a GRN imaging shows "Peak fluorescence intensity of GCaMP6s ... after stimulation
    with 4-methylcyclohexanol", and "Responses to 4-methylcyclohexanol are positively correlated with that to sucrose
    (0.25%) in Gr5a GRNs (R2 = 0.73, p = 0.031)".
  - Tip recordings: "L-type sensilla housing a sweet-sensing GRN robustly responded to sucrose, but also to two tested
    odors, 4-methylcyclohexanol and banana odor", with MCH at "(1%)" in 30 mM tricholine citrate.
  - Stimulus: "an air stream (300 ml/min) was passed through 4 ml of odor solution diluted with mineral oil ... The
    concentration of odor was varied between 10–4, 10–2, 10–1, and 0.5 (v/v), but the default was 0.5 unless otherwise
    noted", then mixed into 500 ml/min.
  - These neurons are not part of the antennal lobe input. At Hige's 2% SV their activation is untested.
- **Orco-independent antennal responses to MCH:** no study found that tested MCH in Orco mutants at the receptor or
  glomerulus level (Not reported).

## 6. Receptors never tested with MCH: what the searches add

- **Or43a (DA4l).**
  - Wetzel et al. 2001 ([PMC55428](https://pmc.ncbi.nlm.nih.gov/articles/PMC55428/); Xenopus oocytes): "Six
    structurally related substances (1,3-cyclohexanedione, 1,4-cyclohexanedione, toluene, 3-phenylpropionaldehyde,
    phenylacetaldehyde, hexanol) and two structurally unrelated Drosophila odorants (propionaldehyde or isopropylacetate)
    (in millimolar concentrations) failed to activate Or43a". Also: "All active ligands share the cyclic 6-carbon
    structure with a polar functional group attached to the ring."
  - Störtkuhl & Kettler 2001 ([PMC55429](https://pmc.ncbi.nlm.nih.gov/articles/PMC55429/); antennal misexpression,
    electroantennogram) and Benton et al. 2006 ([PMC1334387](https://pmc.ncbi.nlm.nih.gov/articles/PMC1334387/); Or43a
    in the CO2 neurons) also did not test MCH.
  - Benton 2006 found that Or43a in vivo responds to hexanol, which the oocytes rejected. So the oocyte negatives are not
    reliable.
- **Or33c/Or85e (VC1), Or59c (VM7v), Or85d (VA4), Or46a (VA7l), Or42a (VM7d), Or69a (D), Or47b, Or67d, Or88a.** Grabe et
  al. 2016's Table S3 (`mmc2.xlsx`) tested these with a smaller panel without MCH. MCH appears only for Or83c (−1),
  which is in the notes. The same table gives Or83c 3-methylcyclohexanol 13 and cyclohexanol 19.
- **Larval receptors (Si et al. 2019 data, `log_10_EC50.csv`).** MCH EC50s exist for Or33b/Or47a −2.46, Or35a −3.87 and
  Or67b −4.21 (all in the notes). The others are larval-only receptors with no adult glomerulus in DoOR's map: Or83a
  −2.96, Or85c −2.56, Or22c −3.46, Or74a −2.73. Or7a (DL5) and Or2a (DA4m) are not in the set.
- **Ellis et al. 2024, Nat Commun 15:4872** (Caron lab): "4-methylcyclohexanol and 3-octanol, which are detected by at
  least three and nine different types of olfactory sensory neuron, respectively31,33". Refs 31 and 33 are Hallem &
  Carlson 2006 and DoOR 2.0, so this adds no data. Their behaviour used both odours at 1:1000 in mineral oil: "3-octanol,
  which activates the largest number of glomeruli, gave rise to larger Performance Indices than 4-methycyclohexanol".
- Still untested with MCH at the receptor (unchanged): Or43a (DA4l), Or85f/Or49a (DL4), Or67a (DM6), Or43b (VM2), Or9a
  (VM3), Or23a (DA3), Or33c/Or85e (VC1), Or46a (VA7l), Or59c (VM7v), Or85d (VA4), Or2a (DA4m), Or65a/b/c (DL3), Or67d
  (DA1), Or88a (VA1d), Ir64a (DP1m, DC4), Gr21a/Gr63a (V). Single Ir neurons were tested only as whole-sensillum sums
  (§1).

## 7. Searched, with no MCH data

- Antennal single-sensillum or imaging: Lin & Potter 2015 (10 standard odorants); Ebrahim et al. 2015 (ab10); Dweck et
  al. 2016 (palp); Keesey et al. 2019, 2020, 2022; Martelli & Fiala 2019; Xiao et al. 2025 and 2026 (simultaneous spikes
  and calcium); Benton et al. 2025 (integrated olfactory atlas, bioRxiv). MCH not in the texts.
  - Benton 2025 does describe the ac3B (Or35a, VC3) neuron as a "hybrid" that also expresses Ir76a. There, "responses
    to amines – notably phenethylamine and amylamine – require instead the Ir co-receptors".
- Andersson 2011 thesis (SLU): its MCH recordings are from a mosquito neuron (Culex short sharp trichoid 3A), not
  Drosophila. The 2012 Chem Senses paper is paywalled; its abstract reports ab3A dose responses ("highly specific for
  ethyl hexanoate").
- DoOR.data (per-receptor files, downloaded 2026-10-11): the only datasets with MCH are the 12 already listed in
  oct_mch_input.md §2 (Bruyne 1999 and 2001, Dweck 2013, Galizia 2009, Münch 2016 AntGC1 and AntGC3, Nissler 2007,
  Pelz 2005 and 2006, Ronderos 2014, Schmuker 2007, Silbering 2011).

## 8. Side findings for OCT (outside the question, but they bear on the MCH/OCT breadth comparison)

- **Contaminated OCT at DC2.** Lüdke 2025: purified OCT is a "medium" Or13a ligand (8.96 at 10⁻², 7.53 at 10⁻⁴), and
  "we assume that commercial 3‐octanol is consistently contaminated with 1‐octen‐3‐ol".
  - Hige's flies smelled commercial OCT, so the contaminant was probably part of their stimulus too. The model's large
    OCT drive at DC2 (`RECOMMENDED` 0.75, from ab6A's 162 spikes/s with commercial OCT) may be right for that
    stimulus, for a reason other than OCT itself.
  - How much 1-octen-3-ol Hige's vials delivered: Not reported.
- **OCT at DP1m.** Ai 2010 and 2013: 3-octanol drives DP1m ORNs (about 0.37 of their largest response at about 10–25×
  Hige). PNs: Hussain 86 ± 4%, Barth 39%, Badel 10%. The model has no OCT input there.
- **OCT at DM2 with purified odour.** Or22a gives −0.01 ± 2.89 (category 0) in Lüdke 2025. This most likely reflects
  the weak GC delivery (§3), not an absent response.

## For the model

1. **The receptor-level evidence still does not support a broad MCH input.**
   - New negatives: purified MCH is inert at Or10a, Or13a, Or22a, Or42b, Or47a, Or56a and Or92a (§3). MCH does not
     excite ac2–ac4 Ir neurons and inhibits ac4 (§1).
   - New positives at the receptor: none for antennal lobe inputs. The labellar taste responses (§5) don't reach the
     antennal lobe.
   - Keep `RECOMMENDED` as it is for VA3, D and the near-zero glomeruli. In particular keep about 0 at DA2, DC2, DM3,
     DM1, VA2 and the coeloconic Ir glomeruli.
2. **Candidates for small additions (all low confidence; none would equalize the odours):**

   | Glomerulus | Model MCH now | Evidence (concentration) | Suggestion | Confidence |
   |---|---|---|---|---|
   | DP1m (Ir64a) | 0 | PNs: Hussain 53 ± 6% (probably about 3–4× Hige), Badel 15% (about 2×); receptor untested; broadly tuned to non-acid odours; OCT drives its ORNs (Ai 2010, about 10–25×) | If added, add for both odours: MCH about 0.04 and OCT at least 0.03. That is Badel's 15% and 10% × 0.0028 DoOR units per % (the notes' PN conversion; range ×0.4–3) (derived). Ai's ORN data suggest OCT's could be larger | low |
   | DL1 (Or10a) | 0.03 | MCH ≈ OCT at the receptor (ab1D 7 vs 2 spikes/s at about 0.8×; Lüdke both about 0 at about 0.25×) and PNs (Badel 37 vs 27%; Avishai about equal at 5 × 10⁻²) | keep 0.03 (at most 0.05), above OCT's 0.01 | moderate that it is small |
   | VC2 (Or71a) | 0.09 | pb1B about 17 net spikes/s (about 0.8×); PNs Barth 168%, Hussain 117 ± 17% (about 3–4×) | keep 0.09 (at most 0.12) | moderate |
   | DC1 (Or19a) | 0.03 | Or19a 5 spikes/s (about 1.1×); PNs Barth 109% (Fiala lab), Hussain 192 ± 28% (Grunwald Kadow lab); Badel's NP225 doesn't cover DC1 | keep; at most 0.08 if these PN data are trusted over the receptor recording | low |
   | VM1, VL2p, VL1 (ac1) | 0 | ac1 sum +29 vs a median odour's +19.5 (1%, about 1–2×); cannot be assigned | none (or 0.02 or less) | very low |
   | DA4l (Or43a) | 0.10 | analogs (Hallem 2004); Wetzel's structural rule fits; PNs Badel 96 vs 15% | keep 0.10 | low |

3. **What not to add as receptor drive.**
   - DL5 and DM3: PNs respond to MCH in Badel and now in Avishai, but the ORNs are inhibited or silent at Hige-like
     concentrations. If the model should reproduce these PN responses, it has to come from the antennal lobe (lateral
     excitation; lateral_excitation.md, lateral_pn_responses.md).
   - VM4 (Barth's 241%) is ruled out by ac4 inhibition.
4. **On breadth versus overlap.** The Kenyon cell overlap problem in `odor_mch_input_sensitivity.py` (half of MCH's
   cells also answer OCT) needs MCH input where OCT has little.
   - Among MCH-biased glomeruli, only VC2 has receptor evidence (pb1B).
   - DA4l and DL4 (`RECOMMENDED` 0.10 and 0.08) rest on untested receptors. This pass found nothing new on DL4.
   - DP1m and DL1 are shared with OCT, so adding them would broaden MCH without making it more distinct.
5. **Measurements that would settle it.** In order of value for this question:
   - Ir64a (DP1m), Or43a (DA4l) and Or85f/Or49a (DL4) recorded with MCH and OCT at about Hige's concentration.
   - Or67a (DM6) and Or43b (VM2), likewise.
   - ab1C with MCH.
   - A single-sensillum check of ac1 neurons' MCH response.

## Sources

**Read for this note**
- Silbering AF, Rytz R, Grosjean Y, et al. (2011) Complementary function and integrated wiring of the evolutionarily
  distinct Drosophila olfactory subsystems. J Neurosci 31:13357. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6623294/>.
  Screen values from DoOR.data `ac1.csv`, `ac2.csv`, `ac3_noOr35a.csv`, `ac4.csv`
  (<https://github.com/ropensci/DoOR.data/tree/master/data>, downloaded 2026-10-11).
- Ai M, Min S, Grosjean Y, et al. (2010) Acid sensing by the Drosophila olfactory system. Nature 468:691.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3105465/>. Supplement:
  <https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnature09537/MediaObjects/41586_2010_BFnature09537_MOESM268_ESM.pdf>.
  Fig. 3:
  <https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fnature09537/MediaObjects/41586_2010_Article_BFnature09537_Fig3_HTML.jpg>.
- Ai M, Blais S, Park JY, et al. (2013) Ionotropic glutamate receptors IR64a and IR8a form a functional odorant receptor
  complex in vivo in Drosophila. J Neurosci 33:10741. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3693055/>.
- Hussain A, Pooryasin A, Zhang M, et al. (2018) Inhibition of oxidative stress in cholinergic projection neurons fully
  rescues aging-associated olfactory circuit degeneration in Drosophila. eLife 7:e32018.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC5790380/>. Figure 2 source data:
  <https://cdn.elifesciences.org/articles/32018/elife-32018-fig2-data1-v2.xlsx>.
- Grabe V, Baschwitz A, Dweck HKM, et al. (2016) Cell Rep 16:3401. Table S1:
  <https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc1.pdf>. Table S3:
  <https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc2.xlsx>.
- Lüdke A, Kumaraswamy A, Galizia CG (2025) Olfactory receptor responses to pure odorants in Drosophila melanogaster. Eur
  J Neurosci 61:e70036. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11891828/>. Supplementary files:
  <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11891828/supplementaryFiles>.
- Avishai G, Parnas M (2025) Differential dopaminergic modulation of the antennal lobe of Drosophila melanogaster.
  Commun Biol 8:1555. <https://pmc.ncbi.nlm.nih.gov/articles/PMC12612080/>. Figures:
  <https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs42003-025-08922-y/MediaObjects/42003_2025_8922_Fig3_HTML.png>
  and `..._Fig9_HTML.png`. Supplementary Data 1:
  <https://static-content.springer.com/esm/art%3A10.1038%2Fs42003-025-08922-y/MediaObjects/42003_2025_8922_MOESM3_ESM.xlsx>.
- Wei H, Lam TKC, Kazama H (2025) Odors drive feeding through gustatory receptor neurons in Drosophila. eLife
  13:RP101440. <https://pmc.ncbi.nlm.nih.gov/articles/PMC12321263/>.
- MacWilliam D, Kowalewski J, Kumar A, Pontrello C, Ray A (2018) Neuron 97:1153.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC5871350/>.
- Kumar A, Tauxe GM, Perry S, et al. (2020) Cell Rep 31:107510. <https://pmc.ncbi.nlm.nih.gov/articles/PMC7552916/>.
- Wetzel CH, Behrendt HJ, Gisselmann G, et al. (2001) PNAS 98:9377. <https://pmc.ncbi.nlm.nih.gov/articles/PMC55428/>.
- Störtkuhl KF, Kettler R (2001) PNAS 98:9381. <https://pmc.ncbi.nlm.nih.gov/articles/PMC55429/>.
- Benton R, Sachse S, Michnick SW, Vosshall LB (2006) PLoS Biol 4:e20.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC1334387/>.
- Ellis KE, Bervoets S, Smihula H, et al. (2024) Evolution of connectivity architecture in the Drosophila mushroom body.
  Nat Commun 15:4872. doi:10.1038/s41467-024-48839-4. <https://www.osti.gov/pages/servlets/purl/2471926>.
- Si G, Kanwal JK, Hu Y, et al. (2019) Neuron 101:950. Data: <https://github.com/samuellab/Larval-ORN>
  (`Figure3/results/log_10_EC50.csv`).
- Frechter S, Bates AS, Tootoonian S, et al. (2019) eLife 8:e44590. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/>.
  Odour set: <https://cdn.elifesciences.org/articles/44590/elife-44590-supp5-v2.csv>.
- Rozenfeld E, Lerner H, Parnas M (2019) Cell Rep 29:3253. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6900217/>.
- Benton R, Mermet J, Jang A, et al. (2025) An integrated anatomical, functional and evolutionary view of the Drosophila
  olfactory system. bioRxiv. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11760703/>.

**Searched, no MCH data (or no glomerulus-level MCH data)**
- Yao CA, Ignell R, Carlson JR (2005) J Neurosci 25:8359. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6725686/>.
- Benton R, Vannice KS, Gomez-Diaz C, Vosshall LB (2009) Cell 136:149. <https://pmc.ncbi.nlm.nih.gov/articles/PMC2709536/>.
- Abuin L, Bargeton B, Ulbrich MH, et al. (2011) Neuron 69:44. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3050028/>.
- Min S, Ai M, Shin SA, Suh GSB (2013) PNAS 110:E1321. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3619346/>.
- Lin CC, Potter CJ (2015) PLoS One 10:e0139675. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4592000/>.
- Ebrahim SAM, Dweck HKM, Stökl J, et al. (2015) PLoS Biol 13:e1002318. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4687525/>.
- Dweck HKM, Ebrahim SAM, Khallaf MA, et al. (2016) eLife 5:e14925. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4927298/>.
- Keesey IW, Grabe V, Gruber L, et al. (2019) Nat Commun 10:1162. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6411718/>.
  Keesey et al. (2020) eLife 9:e57008, <https://pmc.ncbi.nlm.nih.gov/articles/PMC7402680/>; Keesey et al. (2022)
  iScience 25:104212, <https://pmc.ncbi.nlm.nih.gov/articles/PMC9093017/>.
- Martelli C, Fiala A (2019) eLife 8:e43735. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/>.
- Xiao Y, Wu ST, Xuan Y, Rifkin SA, Su CY (2025) bioRxiv / J Neurogenet. <https://pmc.ncbi.nlm.nih.gov/articles/PMC12262726/>.
  Xiao Y, Wu ST, Ng R, Su CY (2026) J Neurosci 46:e2132252026, <https://pmc.ncbi.nlm.nih.gov/articles/PMC13107351/>.
- Andersson MN (2011) PhD thesis, SLU. <https://pub.epsilon.slu.se/id/document/1531>. Andersson MN, Schlyter F, Hill SR,
  Dekker T (2012) Chem Senses 37:403 (abstract only; paywalled).
- Someya et al. (2025) Distinct circuit motifs evaluate opposing innate values of odors. Cell 188:6892 (not accessed).

**Cited through the existing notes:** Barth et al. 2014, Badel et al. 2016, Pech et al. 2015, Yu et al. 2004,
de Bruyne et al. 1999 and 2001, Dweck et al. 2013, Münch & Galizia 2016, Galizia et al. 2010, Pelz et al. 2006,
Churgin et al. 2025, Hallem et al. 2004 ([oct_mch_input.md](oct_mch_input.md)); the concentration estimates and Si et
al. 2019 ([oct_mch_concentration.md](oct_mch_concentration.md)); Badel's glomerulus reliability and lateral firing
([lateral_pn_responses.md](lateral_pn_responses.md)).
