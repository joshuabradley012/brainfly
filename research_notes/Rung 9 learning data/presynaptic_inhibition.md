# Presynaptic inhibition at the ORN→PN synapse, measured: magnitude, GABA-A/GABA-B split, time course, LN rates

Compiled 2026-10-09 from full texts, figures and supplements (PMC HTML, Elsevier/Nature supplementary files, the Hong &
Wilson 2015 Supplemental Table 1 spreadsheet). Purpose: set k_fast, k_slow, tau_fast, tau_slow in brainfly's
`w_eff = w / (1 + sum_j k_j A_j)` (A_j = summed GABAergic LN rate, low-passed with tau_j) without fitting to Olsen 2010's
ORN→PN transform.
Conventions: text in quotation marks is verbatim; "(fig., approx.)" = read off a published figure with a pixel grid
(expect ±3-5 % of full scale); "(derived)" = my arithmetic, shown; "not reported" = searched the text, legends and
supplement and did not find it. Sample sizes are as stated by the authors.

## 1. Olsen & Wilson 2008, Nature 452:956 ([PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/); supplement from nature.com)

Setup. In vivo whole-cell PN recordings. Methods summary: "Antagonists (CGP54626 50 µM and picrotoxin 5 µM) were added to
the saline which perfused the brain." "The odor stimulus period was 500 ms (shown as black bar in Figures)." The Full
Methods (which odor and which receptor-mutant glomerulus were used in Fig. 3) were not accessible (PMC supplement behind
reCAPTCHA, Nature text paywalled): not reported here.

**Headline quotes.**
- "The strength of this inhibitory signal scales with total feedforward input to the entire antennal lobe, and has similar
  tuning in different glomeruli. A substantial portion of this inter-glomerular inhibition acts at a presynaptic locus, and
  our results imply this is mediated by both GABA_A and GABA_B receptors on the same nerve terminal."
- Supp. Fig. 1: "the amount of lateral inhibition evoked by an odor stimulus is proportional to the total number of ORN
  spikes produced by that stimulus, suggesting that inhibition reflects pooled input from all ORN types."

**(a) ORN-evoked EPSC in a PN (Fig. 3; antennal-nerve-evoked EPSCs; lateral input from odor on the contralateral antenna
and palps; the recorded PN's own receptor mutated).**
- Legend 3b: "Electrical stimulation of the antennal nerve (arrowheads) evokes EPSCs in a PN (average of 20 trials).
  Olfactory stimulation (500 ms) inhibits EPSCs."
- Supp. Fig. 7 (text, mean ± s.e.m.): "GABA suppressed EPSC1 to 15 ± 2% of the control value, while odor suppressed EPSC1
  to 46 ± 4%" (odor n = 7; GABA n = 7).
- Fig. 3c time course, EPSC as % of baseline (fig., approx.; EPSCs evoked every 0.25 s; time from odor onset on the plotted
  axis; control n = 12, PCT n = 5, CGP n = 5, CGP+PCT n = 5):

  | t (s) | 0.32 | 0.57 | 0.82 | 1.07 | 1.32 | 1.57 | 1.82 | 2.07 | 2.32 |
  |---|---|---|---|---|---|---|---|---|---|
  | control | 27 | 32 | 33 | 37 | 47 | 66 | 71 | 77 | 76 |
  | PCT (GABA-B left) | 20 | 21 | 33 | 32 | 50 | 64 | 80 | 71 | 68 |
  | CGP (GABA-A left) | 52 | 68 | 77 | 81 | 102 | 106 | 111 | 111 | 104 |
  | CGP+PCT | 105 | 100 | 94 | 94 | 77 | 92 | 99 | 100 | 97 |

  Legend: "All pairwise comparisons are significantly different except control versus PCT (p < 0.05, t-tests)."
  **Discrepancy:** the odor bar in Figs. 3b,c spans ≈1.0 s of the plotted axis (four 0.25-s EPSC intervals; the outward
  "off" current in 3b also starts ≈1.0 s after onset), although the legend says "(500 ms)". I read times off the axis.
- Fig. 3f, same measure after a GABA iontophoresis pulse at t = 0 (Supp. Fig. 8: "Asterisk indicates GABA pulse
  (3-20 ms)"; control n = 13, PCT n = 5, CGP n = 6, CGP+PCT n = 7) (fig., approx.):

  | t (s) | 0.15 | 0.40 | 0.65 | 0.90 | 1.15 | 1.40 | 1.65 | 1.90 | 2.15 | 2.40 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | control | 37 | 8 | 7 | 15 | 33 | 47 | 63 | 73 | 76 | 77 |
  | PCT | - | 10 | 9 | 14 | 25 | 40 | 54 | 70 | 67 | 70 |
  | CGP | 47 | 12 | 20 | 51 | 81 | 86 | 91 | 88 | 86 | 91 |
  | CGP+PCT | 96 | 81 | 76 | 83 | 81 | 92 | 93 | 93 | 86 | 89 |

**GABA-A vs GABA-B, early vs late.** "A GABA_B receptor antagonist blocked the late phase of this inhibition, but had only a
modest effect on the early phase (Fig. 3c,f). Adding a GABA_A antagonist to the GABA_B antagonist blocked the residual
early portion of the inhibition (Fig. 3c,f). The GABA_A antagonist alone had no effect (Fig. 3c,f). Taken together, these
results suggest that both GABA_A and GABA_B receptors are present on the same ORN axon terminals, and either GABA_A or
GABA_B receptors alone are sufficient to mediate substantial inhibition of EPSCs just after GABA release. The late phase of
inhibition evidently involves only GABA_B receptors." Discussion: "GABA_A receptors were required for the a brief early
phase of inhibition after odor onset (Fig. 5), while GABA_B receptors were required for the long, late phase (Fig. 3 and
Fig. 5)."
- Fraction of the odor-evoked inhibition blocked by CGP (GABA-B) (derived from table, inhibition = 100 − EPSC%): at 0.32 s,
  control 73 vs CGP 48 → CGP blocks (73 − 48)/73 = 34 %; at 0.82-1.07 s, 67-63 vs 23-19 → 66-70 %; after offset
  (1.32-2.32 s) → 100 %. Picrotoxin alone blocks ≈0 % at every time point (PCT ≈ control, n.s.). So the two components
  **occlude** rather than add: GABA-B alone gives the full inhibition; GABA-A alone gives about half at peak.

**Time course.** Inhibition is already maximal at the first sample after odor onset (0.32 s) and stays at 63-68 %
through the odor; the GABA-A-only (CGP) inhibition peaks at 48 % (0.32 s) and wanes to 19 % by the end of the odor
(fig., approx.). After odor offset: CGP inhibition is gone within one 0.25-s sample (81 % → 102 %); control/PCT inhibition
recovers to only ≈77 % by 1.3 s after offset (fig., approx.).
- Derived decay constants: control deficit after offset 63 → 53 → 34 → 29 → 23 → 24 % at 0, 0.25, ..., 1.25 s, i.e.
  ln(deficit) falls ≈1.0 per s → **tau_slow ≈ 1 s (0.8-1.4 s)**, with an incomplete tail. CGP: 19 % → ≤ 2 % within 0.25 s →
  **tau_fast ≲ 0.1-0.15 s** (bound set by 4-Hz sampling).
- Genetic removal of presynaptic GABA-B (pertussis toxin in ORNs), Fig. 4b legend: "GABAergic inhibition of EPSCs (solid
  line, n = 11) is more transient than in control flies (dotted line, n = 13, reproduced from Fig. 3f)." Values (fig., approx.;
  GABA pulse at 0): PTX-ORN 45, 5, 9, 54, 81, 97, 98 % at 0.15-1.65 s vs normal 37, 9, 8, 15, 32, 47, 64 %. Derived: after the
  0.4-0.65 s trough, PTX-ORN recovery tau ≈ 0.2-0.3 s; normal ≈ 1 s. Both include iontophoretic GABA clearance, so these
  bound the receptor kinetics rather than measure synaptic decay. Text: "Unlike in wild-type flies, this inhibition was
  completely resistant to the GABA_B antagonist and completely blocked by the GABA_A antagonist".

**(b) PN odor-evoked firing.**
- Antennae removed (palp glomeruli VM7, VC1): "Responses to 18 of 20 odors are significantly disinhibited in VM7; 13 of 20 in
  VC1 (p < 0.05, t-tests)." "No odor responses were decreased." VM7 input-output plateau ≈108 spikes/s intact vs ≈149
  removed; VC1 both ≈165-170 at high input (Fig. 1d, fig., approx.).
- Fig. 2d: VM7 PN disinhibition across 20 odors ≈4-19 spikes/s; regression ≈4.4 + 1.46 × (−lateral input, mV·s)
  (fig., approx.); "n = 20 odors, Pearson's r^2 = 0.65, p < 0.0001".
- Fig. 5b (pentyl acetate, VM7, "Average spike rates during odor stimulus period, minus baseline spike rates (n = 5–6 PNs for
  each condition)"): ORN ≈12; PN intact control ≈0, +PCT ≈4, +CGP ≈5, +CGP+PCT ≈73; antennae removed ≈56 spikes/s
  (fig., approx.).

**Scaling with total ORN activity.** "We estimated total ORN activity by summing the spiking responses of each antennal ORN
type^23, and found that this measure predicted the strength of lateral inhibition evoked by each odor in the shielded-palps
experiment (Fig. 2e, n = 14 odors, Pearson's r^2 = 0.73, p < 0.0005)." Lateral input = "the time-integrated change in
membrane potential" of VM7 PNs. Slope (fig., approx.): −lateral input ≈ 1.5 mV·s + 3.9 mV·s per 1000 spikes/s of summed
antennal ORN rate (Hallem & Carlson sums, range ≈340-1780 spikes/s). This is in mV·s, not a synaptic fraction; the
antennal LFP was not used in this paper (that is Olsen 2010). Other glomerulus: VC1 "Pearson's r^2 = 0.32, p < 0.01".

**Paired-pulse ratio.** "We found that both the GABA_A and GABA_B components of EPSC inhibition are associated with an
increase in the paired-pulse ratio (Supplementary Fig. 7)." Supp. Fig. 7d: odor n = 7, p < 0.001; GABA "n = 7 without
antagonists, p < 0.005; n = 5 in CGP, p < 0.005; n = 5 in PCT, p < 0.05"; with both antagonists "a small but non-significant
change in PPR (n = 4, p = 0.22". Values (fig., approx.): odor PPR ≈0.40-0.87 → 0.55-0.93 (mean ≈0.55 → 0.72); GABA
≈0.37-0.78 → 0.63-1.18. Paired-pulse interval: not reported in the accessible text.

Other: lateral postsynaptic inhibition also exists but is not GABAergic: "Blocking GABAA and GABAB receptors with a
combination of picrotoxin and CGP54626 did not eliminate the postsynaptic inhibition evoked by pentyl acetate" (Supp. Fig. 5).
VM7 ORNs fire "spontaneously at ~10 spikes/s".

## 2. Olsen, Bhandawat & Wilson 2010, Neuron 66:287 ([PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/); Elsevier supplement mmc1)

**Equations, verbatim (exponent 1.5 throughout).**
- Eq. 1: PN = R_max · ORN^1.5 / (ORN^1.5 + σ^1.5).
- Eq. 2 (input gain): PN = R_max · ORN^1.5 / (ORN^1.5 + s^1.5 + σ^1.5).
- Eq. 3 (response gain): PN = (1/(s^1.5 + 1)) · R_max · ORN^1.5/(ORN^1.5 + σ^1.5).
- Eq. 4: "s = m·LFP" "where the slope m represents the sensitivity of each glomerulus to lateral inhibition."
- Eq. 5: "LFP = (Σ_{i=1}^{24} r_i)/190 mV·sec^2/spikes"; Fig. S3: "The slope of the fitted line is (1/190) mV•sec2 / spikes."
- Eq. 6: s = m · (Σ_{i=1}^{24} r_i)/190.
- Values: "The relationship between s and the LFP was obtained from the linear fit in Figure 3H (m = 10.63 for VM7 and 4.19 for
  DL5)." Simulations: "The constant m in Equation (6) was set to 10.63 for all glomeruli." Response-gain model "(m = 0.164)".
- Units of m: not stated. s is in spikes/s and LFP in mV·s, so m is in spikes/(mV·s²) (derived). Combining Eqs. 4-5:
  **s ≈ 0.056 × Σr_i (VM7) and 0.022 × Σr_i (DL5)**, Σ over the 24 Hallem & Carlson ORN types in spikes/s (derived:
  10.63/190, 4.19/190).
- Fig. 3H points (fig., approx.; LFP includes the private odor's own LFP): VM7 s = 0, 10.6, 17.9, 32.0, 45.4 at
  LFP 0.43, 0.69, 1.17, 2.15, 4.75 mV·s; DL5 s = 0, 8.5, 12.7, 20.3 at 0.79, 1.50, 2.45, 5.09 mV·s. The fit passes through
  the origin. Fig. S4: "A sublinear function (exponential or hyperbolic) would not be a good description of this data."
- "The magnitude of inhibition was consistently smaller for DL5 than for VM7, implying that glomeruli differ in their
  sensitivity to lateral inhibition." "our analysis of a published data set comprising seven additional glomeruli (Bhandawat
  et al., 2007) suggests that the values of m for VM7 and DL5 fall within the typical range."
- Prediction quality with m fixed: "accounting for 95% of the variance" (VM7), "87%" (DL5) on novel odors (Fig. 4).

**Windows.** "Responses were quantified as spike rates over the 500-msec stimulus period." Methods: "the trial-averaged number
of spikes during the 500-msec odor stimulus period, minus the trial-averaged baseline spike rate during the preceding 500
msec." "LFP recordings were quantified as the integral during the 500-msec odor stimulus period, minus the integral during
the 500 msec preceding the stimulus." Odor: valve redirected 0.20 of 2.2 L/min "through the headspace of the odor vial for 500
msec. Thus all odors were diluted an additional 10-fold in air".

**Rmax/σ: control saline only.** "R_max = 170, 167, 163, and 144, and σ = 16.3, 11.8, 12.4, and 44.8, for glomeruli DM4, DL5,
VM7, and DM1, respectively." "R_max and σ are essentially the same for all glomeruli (except that without GABA receptor
antagonists σ is larger for the fourth glomerulus we examined)." Fig. 1B legend: "GABA receptor antagonists (5 μM
picrotoxin +10 μM CGP54626) increase the gain in DM1 but not VM7 (red)." So all four fits are in saline (no antagonists);
the antagonist curves (VM7, DM1; red in Fig. 1B) are not given numerically. DM1's high σ is attributed to "inhibition arising
from odor-evoked intra-glomerular GABA release and/or tonic inter-glomerular GABA release." In Figs. 3-4 s is defined
relative to these saline fits, so s = 0 by construction for private odors. Simulations: "R_max = 165 spikes/sec and σ = 12
spikes/sec."

**Size of the suppression.** Fig. 2C, PN rate over the 500-ms odor (fig., approx.), private odor alone → +pentyl acetate
10^-6 / 10^-5 / 10^-4 / 10^-3:
- VM7, 2-butanone 10^-6: 77 → 51 / 36 / 17 / 8 (PA 10^-3 leaves 10 %); 10^-5: 135 → 122 / 114 / 90 / 74 (55 %);
  10^-4: 161 → 164 / 157 / 146 / 129 (80 %). n = 10-11 PNs.
- DL5 (no 10^-6), trans-2-hexenal 10^-9: 41 → 27 / 18 / ≈5-12; 10^-8: 83 → 62 / 54 / 45 (54 %); 10^-7: 147 → 138 / 129 / 112
  (76 %); 5×10^-7: 160 → 156 / 153 / 141 (88 %). n = 9-19.
- Fig. 2D: "GABA receptor antagonists block the suppressive effect of pentyl acetate (10^-3) ... (2-butanone 10^-6; n=5".
- Typical lateral odors: LFPs for 1:100 test odors and blends were 2.7-11.4 mV·s (VM7 set, median ≈6.5) and 0.7-11.4
  (DL5 set, median ≈3.7) (Fig. 4A,B, fig., approx.).
- A single active glomerulus inhibits little: "We used private odors to drive robust activity (∼100 spikes/sec) in a single
  ORN type ... Mixing each private odor with 2-butanone produced only weak suppression of the VM7 PN response to 2-butanone
  (results not shown)."
- Derived from Eqs. 2, 4, 5 (VM7: R_max 163, σ 12.4, m 10.63; DL5: 167, 11.8, 4.19). The effective input divisor is
  g = (1 + (s/σ)^1.5)^(2/3), since Eq. 2 equals Eq. 1 with ORN replaced by ORN/g:

  | LFP (mV·s) | Σr (spikes/s) | VM7 s, g | VM7 PN/PN₀ at ORN 10/50/150 | DL5 s, g | DL5 PN/PN₀ at 10/50/150 |
  |---|---|---|---|---|---|
  | 1 | 190 | 10.6, 1.48 | 0.68 / 0.92 / 0.98 | 4.2, 1.14 | 0.89 / 0.98 / 1.00 |
  | 3 | 570 | 31.9, 2.97 | 0.29 / 0.69 / 0.91 | 12.6, 1.64 | 0.62 / 0.90 / 0.98 |
  | 5 | 950 | 53.2, 4.60 | 0.16 / 0.51 / 0.83 | 21.0, 2.25 | 0.43 / 0.80 / 0.95 |
  | 8 | 1520 | 85.0, 7.11 | 0.09 / 0.34 / 0.71 | 33.5, 3.22 | 0.27 / 0.67 / 0.91 |

**Dynamics.** "Overall, increasing total ORN activity makes PN responses more transient." Mechanism offered: "shorter
integration times are likely due to increasingly rapid recruitment of lateral inhibition by increasingly intense afferent
activity."

## 3. Root, Masuyama, Green, Enell, Nässel, Lee & Wang 2008, Neuron 59:311 ([PMC2539065](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/))

Prep: explant ("Isolated brain preparations"; "The antenna and brain preparation was pinned in a sylgard dish"), imaged by
two-photon GCaMP or synapto-pHluorin (spH) at 4 frames/s. "Input-output functions were fit with y=m*log(x) + b."

**The 105 % figure: confirmed.** "Addition of CGP54626 significantly increases PN response at high stimulus intensities but
not at low intensities, and significantly increased the slope of the input-output function by 105% with no effect on the
offset, thus revealing a multiplicative gain modulation." Stimulus: olfactory-nerve electrical stimulation, "100 Hz, 1 ms in
duration and 10 V in amplitude", 1-100 pulses (x-axis "Stimulus intensity (spikes)"). Readout: PN dendritic GCaMP (GH146),
"Mean integrated fluorescence change over time across preparations", "ΔF/F was measured from all glomeruli in the optical
section"; 25 µM CGP54626; "n, 4–8". So the window is the time-integrated ΔF/F of the whole response, not a fixed
epoch. At 100 pulses, ∫ΔF/F ≈47 (saline) vs ≈91 (CGP) (Fig. 1A, fig., approx.).
- Odors (2-s pulses): "The slope of PN response to cis-vaccenyl acetate, ethyl hexanoate and 2-phenylethanol is increased by
  153%, 67%, and 43%, respectively, in the presence of CGP54626. In contrast, the slope of PN response to CO_2 is not
  altered by CGP54626." (DA1, DM2, VA3, V).
- ORN release (spH): GABA-B2 knockdown in ORNs gives "a 110% increase in the slope". Endogenous tone: with 80 pulses at
  100 Hz, spH ∫ΔF/F ≈9.8 (saline), 3.2 (SKF97541), 14.0 (CGP) (Fig. 3D, fig., approx.). Fig. 4B: CGP +44 %, SKF −60 % in
  controls; ≈0 to +12 % in knockdowns (fig., approx.). Fig. 4C at 80 pulses: ≈10.4 (control) vs ≈21.4 (knockdown).
- LN drive (VR1 in GH298 LNs, capsaicin): ORN-terminal Ca ∫ΔF/F ≈63 → 19 → 56 with capsaicin+CGP (Fig. 3F, fig., approx.;
  45 pulses at 100 Hz).
- VA1lm PN firing (ChR2 in Or47b ORNs, loose patch, 500-ms light): ≈15.8 Hz (control) vs ≈22.8 Hz (ORN GABA-B knockdown) at the
  highest light (Fig. 4E, fig., approx.; n = 8).

**GABA-A.** No PN-slope number. ORN-terminal Ca (45 pulses): saline ≈67, GABA 20 µM ≈20, GABA+125 µM PTX ≈39, GABA+CGP ≈86
(Fig. 3B, fig., approx.; "n, 3–18"). Text: "the reduction caused by GABA is prevented by 25 µM CGP54626, but not by 125 µM
picrotoxin". Discussion: "our study, which employed direct optical measurements of presynaptic calcium and synaptic vesicle
release, suggests that GABA_BRs but not GABA_ARs are involved in presynaptic inhibition."

**Per-glomerulus GABA-B.** "ORNs innervating the VC3 and DM2 glomeruli have relatively weak intensity. In contrast, the VC1,
VA4 and VM7 glomeruli ... exhibit very high intensity. Additionally, the pheromone sensing glomeruli VA1lm and DA1 ... also
exhibit high intensity." V (Gr21a, CO₂): "little or no fluorescence intensity". Fig. 5G, ORN-terminal Ca suppression by 20 µM
SKF97541 vs GABA_B-R2 reporter intensity (fig., approx.; "n, 3–5"):

| glom. | V | DM2 | VA3 | VC3 | VM4 | DA4 | VA1d | VA4 | VC1 | VA1lm | VM7 | DC2 | DA1 | VA6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R2 intensity | 0.10 | 0.50 | 0.58 | 0.59 | 0.64 | 0.82 | 0.82 | 1.11 | 1.13 | 1.22 | 1.35 | 1.67 | 1.69 | 2.35 |
| % Ca suppression | 16 | 67 | 27 | 59 | 55 | 69 | 82 | 75 | 89 | 93 | 97 | 89 | 84 | 91 |

DL5, DM5, DM4, DM1: outlined in Fig. 5F but no numbers reported. Across 118 glomeruli in 5 preparations, control
suppression averages ≈55-63 % (Fig. 6A, fig., approx.). PN gain change vs ORN suppression (Fig. 6B): V 0 %, VA3 +43 %,
DM2 +67 %, DA1 +153 %.

## 4. Nagel, Hong & Wilson 2015, Nat Neurosci 18:56 ([PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/); supplement from nature.com)

**Time course: confirmed.** "Because ORNs spike spontaneously and produce spontaneous EPSCs in PNs^28, spontaneous EPSCs in
PNs provide a sensitive measure of the time course of presynaptic inhibition. The time course of inhibition could be fit with
an alpha function with a time constant of about 25 ms. These data provide direct evidence that LNs have slow effects on ORN
neurotransmitter release." Experiment: ChR2 in NP3056 LNs, shakB² background ("to eliminate lateral excitation"), 17-20
mW/mm²; PNs "n=7 PNs from 7 flies, VM2 or DM6"; LN rates "n=4 LNs from 4 flies". Odor version: "the functional effects of
inhibition peak ~100 ms later" than LN firing, and "The main effect of blocking inhibition on the PN odor response begins
~100 ms after the peak in LN spiking, and also outlasts the burst in LN spiking."
- My reading of Fig. 6c-f (fig., approx.): ChR2-LN rate jumps to ≈50-60 spikes/s within ≈10 ms of light onset; the PN mean
  holding current shifts ≈5 pA outward, starting ≈30 ms after light onset and reaching 90 % at ≈145 ms.

**Magnitude: not reported as a fraction.** The ChR2 experiment used one light level, and there is no LN-rate dose-response.
The SD of PN current falls by ≈1 unit on a scale bar labelled "1 pA²", but the absolute baseline isn't shown, so no
fractional reduction can be computed. Blocking inhibition (5 µM PTX + 50 µM CGP) made 20-ms-pulse responses longer (p = 7.0e-6)
and long-pulse responses decay more (late/peak, p = 3.8e-4; n = 17 PNs, DM6/VM2/VM7, 2-heptanone).

**Their model (a usable operational form).** "we divided ORN firing rates (recorded in separate experiments) by a parameter
I(t) that represents the time-varying amplitude of inhibition. This procedure essentially models inhibition as a decrease in
presynaptic release probability. I(t) was estimated by taking the average spiking activity of all LNs, and filtering this
signal with a 25 ms alpha function". Methods: "This inhibitory signal divided the input to the model (ORN firing rate) at each
point in time." "The magnitude of I(t) that we computed in this manner provided a good qualitative fit to the data, so its
scale was not adjusted." Supp. Fig. 6a shows tonic levels "inhibition = 1, 3, 9, 15" (1 = none).
- Derived scale: Fig. 7c shows the resting depression variable A at ≈0.68 with inhibition and ≈0.33 without (fig.,
  approx.). Their Eq. 3 gives A = 1/(1 + r·τ_A·rate). With the fast-component values (r = 0.23 spike⁻¹, τ_A = 1006 ms),
  A ≈ 0.33 implies a spontaneous ORN input of ≈8 spikes/s. A ≈ 0.68 then needs rate/I ≈ 2 spikes/s, i.e.
  I_rest ≈ 4-5. The slow component (r = 0.0073, τ_A = 33,247 ms) gives the same. This equals the mean LN spontaneous rate
  in spikes/s, consistent with I(t) = (unit-area alpha) ∗ (mean LN rate in spikes/s). The tonic curve in Supp. Fig. 6b also
  falls between their "inhibition = 3" and "= 9". So relative to rest, Nagel's model divides synapses by
  I(t)/I_rest = 1 + ΔLN/4.6. This is an unscaled modelling assumption, not a measured magnitude.
- Variants they tested: with a 5-ms alpha (faster), "inhibition began to act on the synapse before the PN response had
  peaked, and so the peak response was attenuated and response onset was slowed"; with I clamped at its peak, "the PN
  response ran down during a long stimulus". Their model has one inhibitory component (no separate GABA-B tail).
- Pharmacology note: "picrotoxin (an antagonist of inhibitory GABA_A and GluCl receptors). Both antagonists are required to
  block inhibition in this circuit"

## 5. Hong & Wilson 2015, Neuron 85:573 ([PMC5495107](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/); Supplemental Table 1 = Elsevier mmc2.xlsx)

**Method.** ChR2 in NP3056 LNs ("labels between 50 – 60 LNs"), shakB² males, 1-s light at 2-22 mW/mm² (Supp. methods),
whole-cell PN voltage clamp. Metric: "% sEPSC activity" = 100 × SD(current, light)/SD(current, baseline), in 50-ms epochs,
4-Hz high-passed. "we fit a line to the average SDlight:SDbaseline at each light intensity ... constraining this ratio to be 1
at zero light intensity. We took the slope of this line to be a metric of inhibition ... we then normalized the slope values so
that the most negative slope ... had a sensitivity of 1." GABA sensitivity was measured the same way with flash photolysis
of DPNI-caged GABA, at 1-11 mW/mm².
- Absolute anchors: "sEPSCs were completely suppressed in the most sensitive PNs, whereas sEPSCs were almost completely
  unaffected in other PNs (Figure 5B)" (22 mW/mm²). Fig. 4D, 22 mW/mm², n = 3: % sEPSC ≈32 (saline), ≈91 (PTX+CGP), ≈38
  (wash) (fig., approx.). Representative cell (Fig. 4F): ≈74, 72, 64, 58, 49 % at 6, 8, 15, 22, 30 mW/mm²; no-ChR control
  ≈95-87 % (fig., approx.).
- LN rates under the same light (Fig. S3, n = 5, 500-ms light, PSTH in 50-ms bins; Δ from the pre-light level):
  ≈+1-3 at 5 mW/mm², ≈+12 plateau/+21 peak at 8, ≈+21-24 plateau/+33 peak spikes/s at 15 (fig., approx.). 22 mW/mm² was
  not measured.
- Baseline SD of PN current: "4.27±0.13 pA vs. 4.29±0.15 pA" (saline vs DPNI-GABA; the "±" was lost in PDF text
  extraction and is restored here).
- Mechanism: "sensitivity to LN activation, measured by optogenetic activation of LNs (Figure 5), was highly correlated with
  sensitivity to GABA (Figure 8D)" (R² = 0.65). Sensitivity "is not correlated with the density of LN release sites (R^2 =
  0.02, p = 0.67, permutation test)" and "not significantly correlated with LN calcium signals (R^2=0.28, p=0.12)".
- LN recruitment: "focal activation of even a single glomerulus recruits GABAergic interneurons in all glomeruli"; "the
  relative level of LN activity varied about three-fold across glomeruli"; "we can infer that LN activity scales with the
  logarithm of total ORN spike rate". Fig. 3D slope ≈33-45 %ΔF/F (GCaMP3, averaged over glomeruli) per 10-fold increase in
  LFP. The LFP range is 0.02-18 mV·s, with LN ΔF/F rising from ≈10 % to ≈100 % (fig., approx.).

**Per-glomerulus values (Supplemental Table 1; my means ± s.e.m. over cells, normalized to the most sensitive cell = 1).**

| glomerulus | LN-activation sensitivity (n) | GABA sensitivity (n) |
|---|---|---|
| DM5 | 0.98 (1) | 0.64 (1) |
| DL2v / DL2 / DL2d | 0.97 (1) | 0.68 ± 0.00 (2) / 0.75 (1) |
| VA3 | 0.89 ± 0.05 (3) | 0.87 ± 0.04 (3) |
| DA1 | - | 0.97 ± 0.03 (2) |
| VA7 | 0.71 (1) | - |
| DL1, VM3 | 0.55 (1), 0.55 (1) | -, 0.37 (1) |
| DM6 | 0.45 ± 0.03 (6) | 0.62 ± 0.01 (2) |
| DA2 | 0.44 ± 0.03 (5) | - |
| VC3 | 0.43 ± 0.08 (7) | 0.26 ± 0.16 (3) |
| VA1d | 0.41 (1) | 0.15 ± 0.05 (2) |
| D | 0.40 ± 0.07 (5) | - |
| VC2 | 0.38 (1) | 0.20 (1) |
| VM5v | 0.37 (1) | 0.19 ± 0.03 (2) |
| "1" | 0.36 ± 0.06 (6) | 0.47 ± 0.04 (3) |
| DC3 | 0.30 (1) | 0.25 ± 0.05 (2) |
| VM2 | 0.29 (1) | 0.45 ± 0.06 (6) |
| DL4 | 0.18 ± 0.03 (2) | - |
| DC4 | 0.04 (1) | 0.05 (1) |
| VM7 | - | 0.34 ± 0.08 (3) |
| DC2, DC1, VA1v, VC4, VM5d, mgPN | - | 0.62, 0.54, 0.28, 0.24, 0.21, 0.15 |

- VC3 values come from the separate worksheet. The authors excluded VC3 from their analyses "because the odor tuning of VC3 PNs
  varied dramatically across experimental replicates".
- **DM4, DL5, DM1: not measured** for sensitivity. Only LN measures are given: LN Ca (normalized) DM4 0.87, DL5 0.77,
  VM7 0.70, DM1 0.89; brp:GFP density DM4 0.36, DL5 0.70, VM7 0.45, DM1 0.46.
- Derived conversion (assumes linear % sEPSC vs light and that the S = 1 cell reached 0 % at 22 mW/mm²): % sEPSC at 22
  mW/mm² ≈ 100 (1 − S), so in brainfly's form k·A = S/(1 − S). That gives DM6 0.8, DA2 0.8, D 0.7, VM2 0.4, DL4 0.2, DC4 0.04,
  VA3 ≈8, DM5/DL2v ≥30.

## 6. GABAergic LN firing rates

- Nagel, Hong & Wilson 2015 (n = 45 LNs, cell-attached, 2-heptanone 1:100): "nearly all LNs we recorded were spontaneously
  active (4.6 ± 2.8 spikes/s, mean ± s.d. across cells)"; "odor-evoked activity in LNs was highly transient, with a sharp burst
  of spikes at odor onset ... Most LNs did not respond in a sustained manner to long odor pulses. Indeed, responses were
  actually suppressed during long stimuli in many LNs". Fig. 5b mean (fig., approx.): baseline ≈4-5, onset peak ≈43 spikes/s
  for both 20-ms and 2-s pulses. During the 2-s pulse the rate is ≈6-8 after the first ≈200 ms; after offset ≈11-12 for
  ≈1 s. Dense pulse trains recruit LNs "mainly at the onset of the train".
- Nagel & Wilson 2016, J Neurosci ([PMC4829653](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)): "Most LNs in our sample
  exhibited spontaneous spiking in loose-patch recordings (4.6 ± 2.8 spikes/s, mean ± SD)"; "we never observed stable and
  persistent responses to odor in any LNs"; ON and OFF LNs form a continuum. ORN→LN EPSCs depress more than ORN→PN: "f and τ
  are 0.75 and 1566 ms for LNs; 0.78 and 893 ms for PNs." ChR2-driven LNs peak ≈68 and decay to ≈25-30 spikes/s over 1 s
  (Fig. 6E, n = 5, fig., approx.). The LN→LN outward current "grew slowly over time" (Fig. 6F: 10-90 % ≈160 ms, i.e.
  alpha tau ≈50 ms, derived from fig.).
- Chou et al. 2010, Nat Neurosci ([PMC2847188](https://pmc.ncbi.nlm.nih.gov/articles/PMC2847188/)): whole-cell recordings,
  10 odors at 1:100 (further 10× in air); "rates were measured over a 1-sec period beginning at odor onset, and are expressed as
  a change in firing rate relative to the spontaneous firing rate". Fig. 4c (mean ± SEM; recorded n: Line5 55, Line6 18, Line7
  21, Line8 8, Line9 11):

  | Gal4 line | spontaneous | max odor response | mean odor response | % spikes in 1st 100 ms |
  |---|---|---|---|---|
  | Line5 | 4.0 ± 0.4 | 15.7 ± 1.7 | 8.7 ± 1.4 | 14 ± 1 |
  | Line6 | 4.5 ± 0.7 | 7.0 ± 1.0 | 2.5 ± 0.6 | 21 ± 2 |
  | Line7 | 16.8 ± 1.7 | 1.5 ± 1.2 | −3.1 ± 1.2 | 23 ± 2 |
  | Line8 | 5.2 ± 0.6 | 2.7 ± 1.1 | −0.3 ± 0.7 | 43 ± 4 |
  | Line9 | 7.8 ± 2.1 | 18.1 ± 5.5 | 7.7 ± 3.5 | 17 ± 3 |

  "All ∼56 cells labeled by Line5 are LNs" (Line5 = NP3056). Pan-glomerular LNs (n = 26) vs others (n = 67): spontaneous ≈10.2
  vs ≈5.4, mean odor-evoked ≈1.7 vs ≈6.2, max ≈6.4 vs ≈12.8 spikes/s (Fig. 5b, fig., approx.). "All these LNs fired spontaneous
  action potentials, and their spiking was always modulated by odors." Counts: "the lower bound for Drosophila LNs (labeled by
  our Gal4 lines) is ∼100 ipsilaterally projecting and ∼100 bilaterally projecting LNs for each antennal lobe." Nagel &
  Wilson 2016: "Within each antennal lobe, ∼50 GABAergic LNs express Gal4 [NP3056], whereas the remaining ∼50 GABAergic LNs
  do not".
- Wilson & Laurent 2005, J Neurosci ([PMC6725763](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/)): spontaneous "2.3 ± 0.2"
  spikes/s (cell-attached, n = 12); "Each LN responded with at least a small firing rate increase to every stimulus" (6 LNs,
  7 odors); "GABA inhibits LNs solely via a GABA_A-type conductance."
- Seki et al. 2010, J Neurophysiol 104:1007: only the abstract was accessible ("one class of LNs had characteristic burst
  firing properties, whereas the others were tonically active"). Rates not extracted.
- Breadth: LNs are broadly recruited (Hong 2015, all glomeruli for single-glomerulus input; Wilson et al. 2004: "monomolecular
  odors generally elicit responses in large ensembles of antennal lobe neurons"). Chou 2010: "LN odor responses were remarkably
  diverse and typically varied more across cells than across odors within a cell".

## 7. Other direct evidence

- Wilson & Laurent 2005 (PN level, pre- plus postsynaptic, 1-s odor). PTX vs CGP: "CGP54626 significantly increased the number
  of PN spikes in the first 500 ms ... (p < 10^-7; ... n = 41 PN-odor combinations from 11 PNs)"; "picrotoxin had an even greater
  disinhibitory effect (p < 0.01; n = 14 PN-odor combinations from five PNs" "blocking GABA_A receptors had no significant effect
  on the later phase of the odor response (1.5-2.5 s after stimulus onset; p > 0.9) ... blocking GABA_B receptors increased the
  odor-evoked spike rate during this late epoch (p < 10^-5)". Fig. 3C,D (fig., approx.): 0-0.5 s, PTX 48 → 73 and CGP 34 → 47
  spikes/s; 1.5-2.5 s, CGP 6.6 → 12.6 and PTX 5.7 → 5.8. Note: "GABA_B-mediated inhibition is known to depend strongly on the
  number of presynaptic action potentials".
- Silbering & Galizia 2007, J Neurosci ([PMC6673347](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673347/)), PN Ca imaging, 5 µM PTX,
  n = 15: "the time to reach the maximum was shifted from ∼1000 ms to ∼500 ms after stimulus onset during PTX application";
  "a PTX sensitive inhibitory global network that acts on all glomeruli with proportional strength to the global AL input".
  No synaptic fractions.
- Raccuglia et al. 2016, eNeuro ([PMC4994068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4994068/)), ArcLight in DM2 ORN terminals,
  1-s ethyl butyrate: "only the simultaneous pharmacological inhibition of GABA_A and GABA_B receptors significantly increases
  amplitude"; RNAi in Or22a ORNs: "For 1:5 and 1:3 dilutions, sharpness is reduced during a very narrow time window of 1.02
  and 1.84 s after the odor offset". This supports a 1-2 s presynaptic GABA tail. CGP 100 µM, PTX 200 µM.
- Mohamed et al. 2019, Nat Commun ([PMC6416470](https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/)), PN/ORN Ca imaging: "Glomeruli DM2
  and DM3 are inhibited at the presynaptic locus through the GABA_B receptor, while DM1 and DM4 are inhibited at their pre- and
  postsynaptic terminals via GABA_B and GABA_A receptors, respectively". The inhibition comes from DL1/DL5 via patchy LN
  subsets, so it is glomerulus-specific, not global.
- Wilson 2013 review, Annu Rev Neurosci ([PMC3933953](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)): LN→PN pairs show "clear
  unitary synaptic connections are never observed ... a train of spikes in the LN is always required ... and the PN response
  grows slowly throughout the train" (Yaksi & Wilson 2010); LN-LN connections "seem to be weak and slow"; at rest "ORNs as a
  population continuously barrage the brain with ~20,000 ORN spikes/s".
- Asahina et al. 2009, J Biol ([PMC2656214](https://pmc.ncbi.nlm.nih.gov/articles/PMC2656214/)), larva: "We found no evidence of
  such presynaptic inhibition in the larva"; larval LNs "only responded to high ethyl butyrate concentrations upon summed
  activation of at least two OSNs". Adult values should not be transferred to larvae.

## For the model

Form check: the data support a divisive presynaptic factor acting before the PN saturation, i.e. input gain. Olsen 2010
found input gain fit better than response-gain or subtractive models. Its "s" maps to an input divisor
g = (1 + (s/σ)^1.5)^(2/3), not to 1 + kA directly (derived).

**Time constants**

| quantity | value | source | how direct |
|---|---|---|---|
| onset of total presynaptic inhibition after LN spikes | alpha, tau ≈ 25 ms | Nagel 2015 Fig. 6 (n = 7 PNs) | direct (ChR2-LN → PN sEPSC); does not separate A from B |
| tau_fast (GABA-A) decay | ≲ 0.1-0.25 s | Olsen 2008 Fig. 3c CGP (gone within one 0.25-s sample after offset); Fig. 4b PTX-ORN recovery tau ≈ 0.2-0.3 s after a GABA pulse | derived from fig.; upper bounds (sampling; GABA clearance) |
| tau_slow (GABA-B) decay | ≈ 1 s (0.8-1.4 s), incomplete tail at 1.3-2.4 s | Olsen 2008 Fig. 3c control/PCT after offset (n = 12/5); Fig. 4b normal vs PTX-ORN (n = 13/11) | derived from fig.; includes any LN off-firing (≈11-12 spikes/s for ≈1 s after offset, Nagel Fig. 5b) |
| tau_slow rise | ≲ 0.3 s (GABA-B-only inhibition already 80 % at the first 0.32-s sample) | Olsen 2008 Fig. 3c PCT | bound |
| corroborating windows | GABA-B effects persist 1.5-2.5 s after onset of a 1-s odor; terminal effects 1.0-1.8 s after offset | Wilson & Laurent 2005; Raccuglia 2016 | indirect |
| LN→LN (GABA-A only) growth | 10-90 % ≈ 160 ms (alpha tau ≈ 50 ms) | Nagel & Wilson 2016 Fig. 6F | derived from fig.; a different synapse |

**Magnitudes, as measured divisors D = 1 + Σk_jA_j = 1/(fraction of transmission left)**
- Olsen 2008, strong lateral odor (LN rate not measured; odor identity not accessible): D ≈ 3.7 at 0.3 s and 2.7-3.1
  sustained (Fig. 3c, n = 12); EPSC1 46 ± 4 % → D ≈ 2.2 (Supp. Fig. 7, n = 7); GABA iontophoresis 15 ± 2 % → D ≈ 6.7.
  - GABA-A alone (CGP): D ≈ 1.9 at 0.3 s and 1.2-1.5 sustained; GABA-B alone (PCT): D ≈ 5 at 0.3 s and 3.0-3.1 sustained, n.s.
    from control. **The components occlude.** If forced to add: k_fastA_fast ≈ 0.9 and k_slowA_slow ≈ 1.8 at 0.3 s;
    ≈ 0.2-0.5 vs ≈ 1.4-1.9 late in the odor; ≈ 0 vs ≈ 0.3-1.1 after offset (derived). GABA-A is thus ≈1/3 of the total at
    onset and ≈1/6 later.
- Hong 2015, ChR2 on ≈50-60 NP3056 LNs: D ≈ 3.1 (mean of 3 PNs, 22 mW/mm²); representative cell D ≈ 1.56 at 15 mW/mm², where
  each driven LN is at ≈+21-33 spikes/s. Per-glomerulus D ≈ 1/(1 − S) spans 1.04 (DC4) to ≥30 (DM5, DL2v) (derived). This
  assumes SD ratio ≈ release fraction, which holds if inhibition scales sEPSC amplitude without failures.
- Root 2008, endogenous GABA-B on ORN release under whole-nerve 100-Hz × 80-pulse drive: D_slow ≈ 14.0/9.8 ≈ 1.4 (spH, derived;
  explant). PN gain +105 % (electrical), +43 to +153 % (odors, glomerulus-dependent).
- Olsen 2010: m = 10.63 (VM7), 4.19 (DL5) per mV·s of antennal LFP; s ≈ 0.056 Σr (VM7), 0.022 Σr (DL5) (derived). At
  LFP 5 mV·s (Σr ≈ 950 spikes/s) the input divisor g ≈ 4.6 (VM7) and 2.25 (DL5). This is a different experiment (public-odor
  mixtures, Fig. 3H) from the Rmax/σ test target, but the same paper.
- Nagel 2015 model: D(t) = α₂₅ ∗ (mean LN rate, spikes/s), unscaled; I_rest ≈ 4-5. Relative to rest, k ≈ 1/4.6 ≈ 0.22 per
  spike/s of mean LN rate (derived; a modelling choice that "provided a good qualitative fit", not a measurement).

**Derived k in brainfly units (per spike/s of summed GABAergic-LN rate; order of magnitude only)**
- Olsen 2008 sustained kA ≈ 1.7-2.1 with an assumed broad-odor recruitment of ≈+5-6 spikes/s per LN over 1 s (Chou 2010,
  non-pan-glomerular mean +6.2, pan-glomerular +1.7) across 100-200 LNs (ΣΔA ≈ 500-1200 spikes/s) gives
  **k_total ≈ 0.0015-0.004**.
- Hong 2015 representative cell: kA ≈ 0.56 at ΣΔA ≈ 55 × (21-33) ≈ 1150-1800 spikes/s gives **k ≈ 0.0003-0.0005**. The
  3-cell mean at 22 mW/mm² gives kA ≈ 2.1 with ΣΔA ≥ 1150-1800, so **k ≲ 0.0012-0.0018**. The most sensitive glomeruli are
  ≥10× higher.
- Nagel model with ≈100 GABAergic LNs: k ≈ 0.22/100 ≈ **0.002**.
- Split: k_fast/k_total ≈ 1/3 at onset (Olsen Fig. 3c). If both components see the same A, let tau_slow make the slow
  component dominate after ≈0.3 s rather than enlarging k_slow. Single-blocker data overstate the sum because the
  components occlude.

**Caveats that matter for calibration**
1. Per-glomerulus sensitivity varies ≈25× (Hong S 0.04-0.98) and tracks GABA sensitivity and GABA_B-R2 level (Hong R² = 0.65;
   Root Fig. 5G). It does not track LN release-site density (R² = 0.02), so connectome LN→ORN synapse counts alone should not be
   expected to reproduce it. DM4, DL5 and DM1 have no sensitivity measurement; VM7 GABA sensitivity is 0.34 (n = 3), Root's
   VM7 GABA_B-R2 is high (97 % SKF suppression), and DM2 is low (Root 0.50 intensity).
2. LN Ca grows with log(total ORN input) (Hong), while Olsen's s grows linearly with LFP. If kA is linear in LN rate, the
   LN rate model sets this curvature. GABA-B activation may be supralinear in LN spike count (Wilson & Laurent 2005).
3. The test target already contains tonic and intraglomerular inhibition: the Olsen 2010 fits are in saline with s = 0 by
   construction, and one active glomerulus gave "only weak suppression". DM1's σ = 44.8 is attributed to GABA.
4. The Olsen 2008 Fig. 3 odor lasted ≈1 s on the plotted axis versus "500 ms" in the legend. If it was 0.5 s, the GABA-B tail
   after offset is ≈0.5 s longer than stated above.
5. Root's preparation is an explant read out with GCaMP/spH log fits. Its GABA-A null result conflicts with Olsen's
   electrophysiology. Picrotoxin also blocks GluCl (glutamatergic LNs).
