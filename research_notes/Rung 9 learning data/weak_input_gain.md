# Weak-input gain at the ORN→PN step: why flies' transform is so steep, and what the model should change

Compiled 2026-10-10 from full texts, figure legends, supplements and high-resolution figures (PMC XML/HTML, Elsevier
`gr*_lrg.jpg` and `mmc1` files, the Nature supplement of Bhandawat 2007). Purpose: find what in flies gives Olsen et
al. 2010's low σ (12-16 spikes/s) and strongly transient weak responses, and which brainfly settings most plausibly
explain the model's σ of 20-32 (odor_probe44, odor_weak_input_check, odor_transform_check).

**Conventions** (as in the other notes)
- Text in quotation marks is verbatim.
- "(fig., approx.)" = read off a published figure with a pixel grid calibrated on its ticks or scale bars. Expect ±2-4%
  of full scale.
- "(derived)" = my arithmetic on published numbers. "(toy)" = my simulation (§9), not a measurement. "(mine)" = my
  suggestion.
- "Not reported" = searched the text, legends and supplement and did not find it.
- ORN and PN "responses" in Olsen 2010 are evoked rates: spikes in the 500-ms odor period minus the preceding 500 ms.

**Access limits**
- Badel 2016 and Barth 2014 were not re-read; their PN/ORN ratios are in [oct_mch_input.md](oct_mch_input.md).
- Turner 2008's PN-responder criterion was not re-read (the model already applies it).

Related notes, not repeated here: [pn_ln_dynamics.md](pn_ln_dynamics.md) (PN intrinsic properties, peak rates),
[orn_pn_depression.md](orn_pn_depression.md) (depression protocols and fits, resting strength),
[presynaptic_inhibition.md](presynaptic_inhibition.md) (inhibition magnitudes and kinetics),
[lateral_excitation.md](lateral_excitation.md) (eLNs; T9 shows lateral excitation does not shape a private transform),
[oct_mch_input.md](oct_mch_input.md) (OCT/MCH input and equalization data), [orn_dynamics.md](orn_dynamics.md) (ORN
time courses, spontaneous rates).

## Summary

**What makes flies' transform steep at weak input and saturating at strong input**
1. **The measured account is the ORN→PN synapse plus convergence.** I found nothing in the literature that goes beyond
   this.
   - Every ORN of a type synapses on every PN of its glomerulus, from both antennae (99.6% of spontaneous EPSCs shared
     in contralateral DM4 pairs; KW09). Glomeruli receive 23-77 ORNs from both sides (Grabe 2016, females; Tobin 2017:
     52-53 in DM6).
   - Each connection is strong and reliable: 6.19 mV rested uEPSP, ≈51 release sites at p ≈ 0.79, CV 0.16 (KW08); ≈23
     synapses per connection (Tobin 2017).
   - PNs integrate over ≈20-30 ms and sit ≈10 mV below threshold, so ≈5 near-coincident ORN spikes fire a PN. The first
     PN spike comes before the typical ORN's first spike (Jeanne & Wilson 2015).
   - Depression (high p) and the PN's relative refractory period make it saturate (KW08; Olsen 2010; Wilson 2013:
     "probably due to the sublinear relationship between presynaptic spiking and postsynaptic current").
   - **No published model reproduces σ ≈ 12-16 from measured parameters.** Olsen 2010 and Luo 2010 use the
     phenomenological Eq. 1 (Rmax 165, σ 12, exponent 1.5). Nagel 2015 models voltage only, and Jeanne & Wilson's IF
     model covers brief near-threshold packets only.
2. **Part of the steepness comes from how Olsen measured it.**
   - Both axes are 500-ms means from valve opening, but ORN and PN responses start ≈100-125 ms later. Weak ORN responses
     rise slowly and run past the window.
   - For VM7 at 2-butanone 10⁻⁶, means over the response period are 1.23× (ORN) and 1.24× (PN) the window means
     (derived from Olsen Figs. S2 and 8A).
   - The model measures from a step at t = 0 (its time-course check had only 25 ms latency). In a toy with brainfly's
     synapse and PN settings that reproduces brainfly's DL5, measuring Olsen's way lowers the fitted σ by ≈1.3×
     (21.3 → 16.6) and Rmax by ≈0.88× (toy).
3. **σ is well constrained, but the low end is thin.**
   - My digitized points refit to the published values (DL5 166/11.7 vs 167/11.8; VM7 163.5/12.7 vs 163/12.4; DM4
     170.5/16.3, identical).
   - Ranges with Δχ² ≤ 4 (assumed PN SEM 6 spikes/s): DL5 9.6-14.3, VM7 10.0-16.1, DM4 14.1-18.9. Half-maxima read
     without a model are 12-18 Hz. An exponent of 1 instead of 1.5 raises σ by 26-43%; an exponent of 2 lowers it by
     7-8%.
   - Below 20 Hz of ORN input there are only 2 points each for DL5 and VM7, 4 for DM4 and 1 for DM1.
   - At the lowest points flies' PNs fire 5-9× their ORNs' evoked rate: DL5 5.1 → 44, DM4 5.0 → 28, VM7 11.6 → 78
     spikes/s.
4. **Transience at weak private input is moderate; the 6.9 needs a public odor.**
   - With no public odor, peak/mean is ≈2.3-2.5 for weak and intermediate private input and ≈1.9 for strong (Olsen
     Fig. 8C). The 3.8-6.9 values appear only when pentyl acetate is mixed in (lateral inhibition).
   - Measured from response onset (100-500 ms), flies' private-only ratio is ≈1.7 at both 10⁻⁶ and 10⁻⁵ (derived). The
     model's 1.4-1.75 is close.
   - What the model lacks at weak input is amplitude. Flies' VM7 PNs peak at 176 spikes/s for an ORN window mean of
     11.6 Hz; the model's DL5 and VM7d peak at 52-71 at 10 Hz.
5. **Weak ORN responses are tonic at this level, so the PN transient is made in the AL.**
   - In Olsen Fig. S2, VM7 ORNs at 2-butanone 10⁻⁶ and DL5 ORNs at trans-2-hexenal 10⁻⁸ rise slowly and hold or keep
     rising (last 100 ms ≈0.7-0.9 of peak). This agrees with Martelli 2013.
   - PNs answer the rise of ORN activity (Bhandawat 2007; Kim, Lazar & Slutskiy 2015), and depression then pulls them
     down. Flies' VM7 PNs fall to 0.42 of peak by 500 ms at 10⁻⁶.
6. **Equalization needs broader MCH input as well as a steep transform.**
   - With DoOR × 200 Hz inputs, Olsen/Luo's equation gives summed-PN MCH/OCT of 0.64 at σ = 12 against 0.59 at σ = 25.
     With Barth's ORN-imaging fills it gives 0.75 against 0.69 (derived). Flies' PN-level ratio is 0.85-0.98.
   - The rest needs MCH's weak, broad ORN input, which DoOR lacks (Badel's PN-only MCH glomeruli). A low σ is what
     turns those weak inputs into PN responses.

**What the model should change, ranked (mine; §9-10 give the evidence)**
1. **Measure the transform as Olsen did before changing parameters.**
   - Use a ≈100-120 ms ORN latency and the measured ORN time courses (weak: slow rise, tonic; strong: peak at ≈190-260 ms
     then ≈0.65 of peak). Let responses run ≈100 ms past valve closing.
   - Take 500-ms windows from valve opening and subtract baselines on both axes.
   - Compare transience with Fig. 8C's no-public-odor points.
   - Expected: σ about ÷1.3, Rmax about ×0.86-0.88, late/peak 0.25-0.32 → 0.42-0.50 (toy).
   - Applied to brainfly's step fits (derived, ÷1.28): DL5 23.4 → ≈18, VM7d 30.7 → ≈24, DM4 27.8 → ≈22. Flies: 11.8,
     12.4 and 16.3. The gap would shrink from ≈1.7-2.5× to ≈1.3-1.9×, with VM7d the furthest off.
2. **Check per-glomerulus input drive.**
   - MaleCNS is male; the fly data are from females. Per side, female vs male (Grabe 2016): DM4 23 vs 15.5, DL5 24 vs 21,
     DM1 38.5 vs 32, VM7d 11.5 vs 15.
   - In flies, uEPSPs are matched across glomeruli (KW08: DL5 7.0, DM4 6.9, DM6 5.5, VM2 5.4 mV). The model sets one
     global factor, so its per-glomerulus uEPSP follows MaleCNS synapse counts.
   - The model's DM4 (Rmax 81, σ 28) is the outlier to check first.
   - In the toy, σ falls roughly with 1/√N, while the unitary size barely moves σ. With Olsen's protocol at 6 Hz,
     N 32/40/48/60 gives σ 16.6/14.7/13.0/11.2.
   - Flies' DL5 points are matched at N ≈ 48 (Grabe's female count), ≈1.5× the brainfly-equivalent N of 32.
3. **Treat resting depletion as the strongest lever, and as unresolved.**
   - In the toy (N 40, step), σ rises steeply with spontaneous ORN rate: 13.7, 19.6, 23.3 and 36.6 at 3.4, 6, 8 and
     15 Hz. The single pool (f 0.78, τ 0.9 s) spends 40-75% of its sustained capacity at rest.
   - The model uses sensillum-class medians (antennal basiconic 6, palp 8 Hz). Flies' ab4A (DL5) fires 14-20 Hz, pb1A
     (VM7d) 10-16, ab1A (DM1) 9 and ab2A (DM4) 3.4-11.
   - Setting DL5 to its measured rate would make it the model's least sensitive glomerulus, the opposite of flies (DL5
     σ 11.8, the lowest).
   - So flies' synapse must keep more capacity at rest than this pool allows. No measurement says how; candidates are
     faster recovery during ongoing firing (KW08 Fig. S8B: τ ≈ 0.4 s after trains) and glomerulus-specific release
     properties.
   - Don't raise spontaneous rates without revisiting the depression model.
4. **Give DM1 its GABA sensitivity.** Flies' DM1 σ is 45 in saline and 13.4 with GABA antagonists (refit). The model's
   DM1 is its most sensitive glomerulus (σ 20).
5. **Revisit PN spike generation only if peaks stay low after 1-2.** A reset closer to threshold raises responses at
   every input (toy: σ 22.8, Rmax 318), so it is a lever on Rmax and peak rates, not σ. Pair it with a relative
   refractory term (toy: +6 mV threshold jump decaying over 3 ms).
6. **What did not help in the toy or the literature:**
   - tonic presynaptic inhibition alone, which makes responses too sustained (late/peak 0.55-0.87);
   - Nagel's large slow component (0.774), which is sustained (peak/mean 1.16);
   - deeper depression (KW09's 0.72 / 2.4 s, σ 40);
   - two-pool M4 (σ 26.6);
   - threshold 10 mV or τm 30 ms (σ unchanged);
   - eLN coupling, which does not change flies' private-odor responses (Yaksi & Wilson 2010, VC1 with antennae removed).

---

## 1. Olsen, Bhandawat & Wilson 2010, Neuron 66:287 ([PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/))

### 1.1 How the transform was measured
- **Preparation.** In vivo whole-cell current clamp from GFP-targeted PNs. ORNs by single-sensillum recording in separate
  flies. Saline 1.5 mM Ca²⁺, 4 mM Mg²⁺. Sex not reported (Bhandawat 2007 and KW08, same lab, used "adult female flies,
  2–7 days post-eclosion").
- **Response measure.** "the trial-averaged number of spikes during the 500-msec odor stimulus period, minus the
  trial-averaged baseline spike rate during the preceding 500 msec". "typically with 4 trials per stimulus spaced 40-60
  sec apart".
  - The x-axis is therefore the ORN's evoked rate (minus spontaneous), averaged over the 500 ms from valve opening.
- **Delivery** (supplement). "a constant stream of charcoal-filtered air (2.2 L/min) ... a three-way solenoid valve
  redirected a portion (0.20 L/min) through the headspace of the odor vial for 500 msec. Thus all odors were diluted an
  additional 10-fold in air". Odor streams rejoin the carrier "15 cm from the end of the delivery tube, which measured 3
  mm in diameter and was positioned 8 mm from the fly".
  - The valve-to-response delay is not reported. Measured from the figures in §1.4-1.5, it is ≈100-150 ms.
- **Private odors and concentrations** (Fig. 1B legend; v/v in paraffin oil, then 10× in air):

  | glomerulus (receptor) | odor | concentrations | points |
  |---|---|---|---|
  | DM4 (Or59b) | methyl acetate | 0, 10⁻¹¹, 10⁻¹⁰, 10⁻⁹, 3×10⁻⁸, 7×10⁻⁸, 10⁻⁷, 10⁻⁶, 10⁻⁵ | 9 |
  | DL5 (Or7a) | trans-2-hexenal | 10⁻⁹, 10⁻⁸, 10⁻⁷, 5×10⁻⁷ | 4 |
  | VM7 (Or42a) | 2-butanone | 10⁻⁷, 10⁻⁶, 10⁻⁵, 10⁻⁴ | 4 |
  | DM1 (Or42b) | ethyl acetate | 0, 10⁻¹⁴, 10⁻¹³, 10⁻¹², 10⁻¹¹, 10⁻⁹, 10⁻⁸, 10⁻⁷, 10⁻⁶ | 9 |

  - "All values are means of 6 -12 recordings, ± SEM."
  - Fig. S1: the private odors at their highest concentrations evoked "almost no response from non-cognate ORNs" (223
    ORNs; median −0.25 spikes/s, 90th percentile 5.2). The supplement adds: "the four 'private' stimuli are not strictly
    private at the highest concentration we used".
- **Fit.** "R_max and σ were free parameters." The exponent was fixed at 1.5: "We determined this by fitting the data in
  Figure 3 with different exponents between 1 and 2 in increments of 0.1. The mean squared error had a minimum for an
  exponent of 1.5 and 1.6 for glomeruli DL5 and VM7". So the exponent came from the public-odor experiments (Fig. 3),
  not from Fig. 1.
  - "Equation (1) fits these data better than the logarithmic function used in previous studies".

### 1.2 The points, digitized (Fig. 1B, high-resolution Elsevier figure; fig., approx.)
Each point is (ORN evoked rate, PN evoked rate) in spikes/s. Points hidden by others were read from 2× zooms.

| glomerulus | points |
|---|---|
| DM4 | (0.7, 8.7), (5.0, 27.9), (6.1, 31.5), (13.4, 63.9), (25.8, 115.9), (29.6, 129.5), (62.2, 143.8), (71.1, 153.4), (125.0, 164.1) |
| DL5 | (5.1, 44.2), (13.4, 84.9), (41.5, 148.6), (98.7, 158.4) |
| VM7 | (0.1, 2.5), (11.6, 78.0), (47.9, 138.3), (107.1, 161.4) |
| VM7 + PTX/CGP | (0.1, 35.4), (11.4, 87.8), (47.7, 135.0), (107.1, 139.0) |
| DM1 | (9.2, 20.9), (21.8, 40.1), (24.3, 44.0), (25.7, 51.5), (28.7, 40.1), (36.0, 61.9), (51.3, 73.6), (55.8, 72.0), (73.5, 105.2), (111.2, 122.6) |
| DM1 + PTX/CGP | (9.4, 73.8), (24.4, 112.8), (25.6, 126.6), (35.9, 137.6), (55.9, 159.4), (73.5, 170.7), (111.1, 164.1) |

- DM1 shows 10 marks for 9 concentrations, four of them clustered at 22-29 Hz. One may be an artifact of overlapping
  error bars.
- The DM4 point at (0.7, 8.7) is the "0" (solvent) stimulus.
- **Sampling.** Points below 20 Hz of ORN input: DM4 4 (0.7, 5.0, 6.1, 13.4), DL5 2 (5.1, 13.4), VM7 2 (0.1, 11.6), DM1
  1 (9.2). Below 10 Hz: 3, 1, 1 and 1.
- **PN/ORN at the lowest driven points** (derived): DM4 5.6× (5.0 Hz), 5.2× (6.1), 4.8× (13.4); DL5 8.7× (5.1), 6.3×
  (13.4); VM7 6.7× (11.6); DM1 2.3× in saline, 7.9× with GABA antagonists (9.2-9.4 Hz).
- **GABA antagonists in VM7.** The text says the antagonists "had no effect on a more typical glomerulus". But at
  2-butanone 10⁻⁷ (ORN ≈ 0.1 Hz) the PN response is 35 Hz with antagonists against 2.5 in saline. In saline, GABA
  silences the response to the faintest stimulus; above it the curves overlap.

### 1.3 Refits and how well σ is constrained (derived)
Fitted with Olsen's Eq. 1, PN = Rmax·x^n/(x^n + σ^n), by unweighted least squares.

| set | Rmax, σ (n = 1.5) | published | σ range, Δχ² ≤ 1 / ≤ 4 (assumed PN SEM 6) | σ at n = 1 / n = 2 | free n | half-max without a model |
|---|---|---|---|---|---|---|
| DM4 | 170.5, 16.3 | 170, 16.3 | 15.2-17.6 / 14.1-18.9 | 23.3 / 15.0 | 1.54 (σ 16.1) | 17.7 |
| DL5 | 166.4, 11.7 | 167, 11.8 | 10.6-12.9 / 9.6-14.3 | 15.6 / 10.9 | 1.30 (σ 12.6) | 12.2 |
| VM7 | 163.5, 12.7 | 163, 12.4 | 11.3-14.3 / 10.0-16.1 | 16.0 / 11.8 | 0.94 (σ 17.1) | 13.2 |
| DM1 | 152.3, 48.1 | 144, 44.8 | 43.0-53.8 / 38.4-60.4 | 125.6 / 36.6 | 0.85 (unbounded) | 35.8 |
| VM7 + antagonists | 143.2, 8.3 (rms 17.6, poor fit) | not given | — | — | — | 7.5 |
| DM1 + antagonists | 174.4, 13.4 | not given | 12.2-14.6 / 11.1-16.0 | 15.6 / 12.7 | 1.14 (σ 14.5) | 13.8 |

- "Half-max without a model" is the ORN rate where the PN response reaches half the highest observed response, by linear
  interpolation between points.
- **Reading.**
  - σ's position is set by the 13-30 Hz points and is robust: ±15-20% at Δχ² ≤ 4; +26-43% (n = 1) to −7-8% (n = 2)
    across exponents.
  - The shape below 10 Hz (expansive or linear) is not constrained: a free exponent gives 0.94-1.54.
  - The fly targets for a model are therefore the half-maximum (12-18 Hz) and the points themselves, more than the
    exponent.
- **Fit predictions** at 5/10/20/40 Hz (derived): DM4 25/55/98/135; DL5 36/73/115/144; VM7 32/67/109/139; DM1 5/13/32/66.
- **brainfly** (odor_weak_input_check, intact; step from t = 0) at 5/10/20/40 Hz: DL5 19/42/78/111, VM7d 13/34/70/108,
  DM4 9/19/31/46, DM1 24/50/82/114.

### 1.4 ORN time courses at weak and strong input (Fig. S2; supplement p. 6 rendered at 300 dpi; fig., approx.)
"Recordings from VM7 ORNs show the response to either 2-butanone alone or 2-butanone blended with pentyl acetate".
"Each peristimulus-time histogram is a mean of 4-8 recordings" (VM7) and "5-6 recordings" (DL5). Calibration: 200
spikes/s = 141 px; the odor bar, 500 ms, is 90 px. Values are for the private odor alone. Times are from valve opening.

| stimulus | window mean (evoked) | peak | time of peak | 20% of peak reached | share of response spikes inside 0-500 ms | mean over 500 ms from onset ÷ window mean | peak ÷ window mean |
|---|---|---|---|---|---|---|---|
| VM7, 2-butanone 10⁻⁶ | 12.0 | 24 | 233 ms | 122 ms | 0.81 | 1.23 | 2.0 (noisy) |
| VM7, 10⁻⁵ | 47.6 | 86 | 256 ms | 150 ms | 0.79 | 1.24 | 1.81 |
| VM7, 10⁻⁴ | 99.8 | 161 | 189 ms | 133 ms | 0.77 | 1.26 | 1.62 |
| DL5, trans-2-hexenal 10⁻⁸ | 15.5 | 28 | 461 ms (still rising) | 139 ms | 0.66 | 1.29 | 1.81 |
| DL5, 10⁻⁷ | 60.5 | 84 | 189 ms | 61 ms | 0.73 | 1.10 | 1.38 |
| DL5, 5×10⁻⁷ | 121.5 | 166 | 217 ms | 67 ms | 0.64 | 1.13 | 1.37 |

- **Lowest concentrations.** VM7 10⁻⁷ and DL5 10⁻⁹ are within noise. Their responses (≈5 Hz) peak after the valve
  closes, and only 35-41% of their spikes fall inside the window.
- **Calibration check.** VM7 window means match the panel-B bars (≈1-2, 10, 47 and 107). DL5 trace values run ≈20%
  above the bars (≈5, 13, 41 and 98), so treat DL5 absolute values with caution; ratios are unaffected.
- **Weak responses are tonic.** On the black traces, the last 100 ms of the odor are ≈0.68 (VM7 10⁻⁶) and ≈0.91 (DL5
  10⁻⁸) of the peak.
- **Strong responses are phasic but moderate.** VM7 10⁻⁴ peaks at ≈190 ms and is ≈0.65-0.7 of peak by 500 ms. Responses
  outlast the valve by ≈100-200 ms, and weak VM7 responses dip ≈10 Hz below baseline afterwards.

### 1.5 PN time courses and transience (Fig. 8; high-resolution figure; fig., approx.)
PSTHs are from 50-ms bins overlapping by 25 ms. VM7 PNs, n = 10-11. Samples are every 25 ms from valve opening.

| stimulus | samples 0-500 ms (spikes/s) | peak | 0.5 s / peak | mean 0-500 | peak/mean | mean 100-500 | peak/mean (100-500) |
|---|---|---|---|---|---|---|---|
| 2-butanone 10⁻⁶ alone | 2 2 2 2 2 58 160 176 161 143 122 110 99 109 82 84 81 74 74 80 74 | 176 at 175 ms | 0.42 | 83 | 2.13 | 103 | 1.71 |
| 10⁻⁶ + pentyl acetate 10⁻⁶ | 6 5 6 7 12 67 151 164 123 86 56 48 52 56 19 15 14 13 15 13 11 | 164 | 0.07 | 46.5 | 3.53 | 56 | 2.91 |
| 10⁻⁶ + pentyl acetate 10⁻³ | 2 0 2 2 5 38 75 68 41 19 6 3 1 2 3 1 1 1 1 1 1 | 75 | 0.02 | 13.6 | 5.55 | 16 | 4.58 |
| 2-butanone 10⁻⁵ alone | −1 −1 −1 −1 −1 219 296 263 236 221 193 170 159 141 136 142 136 135 135 131 129 | 296 at 150 ms | 0.44 | 139 | 2.13 | 174 | 1.71 |
| 10⁻⁵ + pentyl acetate 10⁻³ | 3 3 3 2 84 198 225 169 133 112 93 75 61 54 61 66 68 72 66 65 70 | 225 | 0.31 | 82 | 2.74 | 100 | 2.26 |

- **PN onset.** PN responses begin between 100 and 125 ms after the valve.
- **Fig. 8C**, as printed. Each curve is one 2-butanone concentration. "each point within a curve is a different
  concentration of pentyl acetate (0, 10⁻⁶, 10⁻⁵, 10⁻⁴, 10⁻³)". x is "field potential evoked by public odor".

  | private input | pentyl acetate 0 (x ≈ 0.49 mV·s) | x ≈ 0.7 | x ≈ 1.2 | x ≈ 2.2 | x ≈ 4.8 |
  |---|---|---|---|---|---|
  | weak (10⁻⁶) | ≈2.3-2.5 | 3.79 | 4.63 | 6.18 | 6.90 |
  | intermediate (10⁻⁵) | ≈2.3-2.5 | 2.66 | 2.80 | 3.00 | 3.05 |
  | strong (10⁻⁴) | 1.91 | 1.92 | 1.91 | 1.99 | 2.02 |

  - At pentyl acetate 0 the weak and intermediate points overlap at ≈2.27 and ≈2.50; which is which cannot be resolved.
  - My PSTH-based values (2.13) are lower than Fig. 8C's. Olsen's mean is baseline-subtracted (the Fig. 2C bar is ≈77
    against my 83) and was probably computed per cell.
- **Olsen's explanation.** "a strong public stimulus recruits ORNs faster ... Faster recruitment of the ORN population
  should recruit faster lateral inhibition, and thus more transient PN responses". "the effect of the public odor on PN
  dynamics was only large when the private odor concentration was low".
- **The response-period rescaling (derived).**
  - In VM7 at 10⁻⁶, the ORN response-period mean is 1.23× its window mean (§1.4) and the PN's is 1.24×.
  - Expressed in response-period units (what a step at t = 0 measures), flies' VM7 transform has roughly σ ≈ 1.23 ×
    12.4 ≈ 15 Hz and Rmax ≈ 1.25 × 163 ≈ 200 spikes/s, if the transform were instantaneous.
  - The peak/mean of flies' private-only responses is ≈1.7 in the same units.

### 1.6 The model in the paper
- Eq. 1 is phenomenological: "The saturating form of this function reflects the combined effects of short-term depression
  at ORN-PN synapses and the relative refractory period of PNs (Kazama and Wilson, 2008)." No mechanistic simulation.
- Population simulations: "R_max = 165 spikes/sec and σ = 12 spikes/sec" for all 24 glomeruli; input gain s = m·ΣORN/190
  with m = 10.63 (VM7) for all. "if the presynaptic ORN odor response was a negative number ... then the PN response was
  set to zero."
- Response-gain alternative: m = 0.164. Subtractive alternatives fit worse (MSE 846 and 149 spikes²/s² for a rightward
  shift; 245 and 80 for a downward shift; VM7 and DL5).
- "R_max and σ are essentially the same for all glomeruli (except that without GABA receptor antagonists σ is larger for
  the fourth glomerulus we examined)."
- DM1's σ is attributed to "inhibition arising from odor-evoked intra-glomerular GABA release and/or tonic
  inter-glomerular GABA release".
- "Mixing each private odor with 2-butanone produced only weak suppression of the VM7 PN response to 2-butanone (results
  not shown)". One active glomerulus recruits little lateral inhibition.
- **PN trial-to-trial noise** (Fig. S6, from Bhandawat 2007's data): "SD = (9.5 spikes/sec) – (7.2 spikes/sec) •
  e^(–mean/(76 spikes/sec))" over 500-ms windows, n = 787 blocks.

## 2. Kazama & Wilson 2008, Neuron 58:401 ([PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/))

The "nonlinear amplification" paper. In vivo, adult females 2-7 days; antennal nerves cut for evoked EPSCs. Depression
data and quantal numbers are in orn_pn_depression.md §1. Weak-input mechanisms stated:
- **Strong synapses.** "The synapse between olfactory receptor neurons (ORNs) and projection neurons (PNs) is very strong,
  reflecting a large number of vesicular release sites and a high release probability. This is likely one reason why weak
  ORN odor responses are amplified in PNs."
  - Quantal values (stated): "average estimated quantal size was 1.05 pA. Estimated release probability was consistently
    high, with a mean value of 0.79. The number of release sites was also high, with a mean value of 51."
- **Convergence.** "The convergence of many ORNs onto each PN is another likely reason why weak ORN odor responses are
  amplified in PNs".
- **Bilateral input.** "we have found that ORN-PN synapses are equally strong for both ipsi- and contralateral ORN
  projections. This effectively doubles the strength of ORN input as compared to an olfactory system with unilateral ORN
  projections."
  - Fig. 2D: "p > 0.54, t-test, n = 20 ipsilateral, 24 contralateral". Gaudry 2013 and Tobin 2017 later found ipsilateral
    connections stronger (§6).
- **Reliability.** "ORN-PN synapses are highly reliable, with an average CV of just 0.16".
- **Matching.** uEPSPs are matched across glomeruli while uEPSCs differ about 3-fold (DM4 41 pA, VM2 13 pA). "the
  number of presynaptic release sites per ORN fiber is higher for these synapses". The gain "is kept constant across
  different PN types".
- **Saturation.** "Short-term synaptic depression produces a nonlinear transformation of ORN responses." Charge transfer
  over 100 or 500 ms grows sublinearly with stimulus frequency (Fig. 9C,D; values in orn_pn_depression.md §1.4).
  - "PN firing rates only grow sublinearly with increasing synaptic currents (data not shown), due to the relative
    refractory period."
- **The quantitative statement.** "Odors that evoke small responses in ORNs (< 20 spikes/s) can evoke much stronger
  responses in postsynaptic PNs (> 100 spikes/s)." This comes from Bhandawat 2007's peak-epoch transform (§4).
- **Fig. 9A**, VM2 (reproduced from Bhandawat 2007): "Frequency is calculated over a 500-ms period of odor stimulation.
  Line is an exponential fit."
  - Neither axis is baseline-subtracted (Bhandawat Supp. Fig. 5). VM2 ORNs fire 7.1 and VM2 PNs 2.5 spikes/s at rest
    (Olsen 2007).
  - Points as (ORN total, PN total), fig., approx.: (8.1, 21.7), (17.2, 54.5), (17.9, 69.9), (19.4, 32.0), (23.9,
    83.8), (24.3, 77.9), ≈(29.7, 69) for two merged points, (30.0, 79.7), (49.8, 118.2), (53.2, 83.5), (56.9, 104.0),
    (69.4, 97.8), (76.4, 73.7), (91.2, 63.7), (95.7, 96.2), (129.1, 90.8).
  - The fit plateaus at ≈90 spikes/s.
  - So ORN totals of 17-24 Hz (≈10-17 Hz evoked) already give 55-84 spikes/s, with lateral input included (derived).

## 3. Kazama & Wilson 2009, Nat Neurosci 12:1136 ([PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/))

- **Complete convergence.** "Given an EPSC in one PN, we found that the probability of observing a time-locked EPSC in the
  other PN is 99.6 ± 0.1% for glomerulus DM4 (n = 3 pairs, all contralateral)... 96.1% for glomerulus DM6". "This implies
  that ORN-PN connections are completely convergent, with each PN receiving input from all ORNs."
- Ipsi-contra EPSC lag: "0.3 ± 0.10 ms, n = 3".
- **ORN independence.** ORN spike trains are independent at rest (DM4). Jeanne & Wilson confirmed this for DA1 and for
  odor-evoked first spikes (§5). So the only synchrony across a glomerulus's ORNs is stimulus-locked: the rate time
  course.
- **Regime near threshold.** "Odors that elicit only a modest increase in firing rate (10–30 spikes/sec above spontaneous
  firing rates) increase correlations just as much as odors that elicit a powerful increase in firing rate (>150
  spikes/sec). This is suggestive of a mechanism that is engaged in the regime near spike threshold."
  - "In the absence of odors, PNs fire spontaneously (typically 1–5 spikes/sec)".
- **Sister-PN coupling.** It is a mixed electrical/chemical synapse (lateral_excitation.md §5.2). Yaksi & Wilson 2010
  found it amplifies DA1 responses by 29-42%. It matters only in multi-PN glomeruli (VM7d 2-3 PNs; DL5, DM4 and DM1 1
  each; Grabe 2016).

## 4. Bhandawat, Olsen, Gouwens, Schlief & Wilson 2007, Nat Neurosci 10:1474 ([PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/); [supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnn1976/MediaObjects/41593_2007_BFnn1976_MOESM22_ESM.pdf))

"All experiments were performed on adult female flies 2–7 days post-eclosion." Seven glomeruli, 18 odors at 1:100 in
oil (1:1,000 effective).
- **Two windows.**
  - Fig. 6 uses "the mean spike rate during the 100-ms epoch when firing rates are peaking (with no baseline
    subtraction)".
  - Supp. Fig. 5 uses the 500-ms stimulus period: "baseline firing rates are not subtracted from each response
    magnitude". Its fits are "exponential fits (y=y0+A•e^kx)".
  - The peak-epoch transform is much steeper. At ORN responses of ≈5-20 spikes/s, VA2, VM2 and DM3 PNs reach ≈100-220 in
    the peak epoch (fig., approx.; from the low-resolution PMC figure).
- **Statements.**
  - "Even a small increase in ORN spike rate above baseline can produce a robust response in postsynaptic PNs. As a
    result, PN responses rise rapidly even when ORN responses build slowly."
  - "PNs act as high-pass filters, transmitting the rising phase of ORN responses preferentially over the tonic component
    of ORN responses. This rapid accommodation might be due to any of several mechanisms, including for example short-term
    synaptic depression".
  - On the glomerular functions: "they initially slope steeply, meaning that the gain of the transformation function is
    high for weak inputs" (all but DL1). "all of these functions have a y-intercept >0", attributed to lateral input.
  - The pheromone channel DA1 shows amplification without broadening: "Their postsynaptic PNs are also highly selective
    for this odor, but respond much more robustly".
- **Response histograms** (Supp. Fig. 5b, 500-ms totals, 126 pairs; bar heights, fig., approx.):

  | rate bin (spikes/s) | 0-20 | 20-40 | 40-60 | 60-80 | 80-100 | 100-120 | 120-140 | >140 |
  |---|---|---|---|---|---|---|---|---|
  | ORNs | 0.50 | 0.29 | 0.05 | 0.02 | 0.02 | 0.02 | 0.06 | 0.06 |
  | PNs | 0.23 | 0.21 | 0.19 | 0.15 | ≈0.07 | 0.10 | 0.02 | ≈0.03 |

  - The PN histogram's 80-100 bin was read beside the "PNs" label, so treat it as approximate.
  - In 79% of pairs the ORNs fire below 40 spikes/s in total, while 56% of PN responses exceed 40 (derived). This
    "histogram equalization" is the population signature of a low σ, and a check that needs no glomerulus-by-glomerulus
    fit.
- Grand-mean dynamics are in pn_ln_dynamics.md §2.1: PN peak at ≈150 ms, ORN at ≈225 ms; PN at 500 ms ≈0.48 of peak.
- Stevens 2015 ([PMC4522789](https://pmc.ncbi.nlm.nih.gov/articles/PMC4522789/)) fitted these peak rates with an
  exponential distribution of mean 162 spikes/s. That is a population statistic, not a mechanism.

## 5. Jeanne & Wilson 2015, Neuron 88:1014 ([PMC5488793](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/); [supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0896627315008843-mmc1.pdf))

The "≈3×" comparison comes from a different regime from Olsen's.
- **Regime.**
  - DA1, males ("All experiments were performed in males").
  - ChR2 in DA1 ORNs, light on one antenna only: "The contralateral antenna was not stimulated."
  - ORNs fire 1.5 ± 1.1 spikes/s at rest (n = 58), so their synapses are close to rested. PNs fire 8.6 ± 6.3 (n = 44).
  - The main stimulus is a 100-ms flash eliciting "an average of 1.7 spikes per ORN per trial". Gain points used
    20-100 ms flashes, and "For shorter stimuli (20-30 msec) we computed firing rates over 60 msec windows ... For the
    long stimulus (100 msec) ... over 120 msec windows".
  - "Overall, there was a linear relationship between ORN and PN spike counts in this near-threshold regime. PN spike
    rates were consistently about three-fold larger than ORN spike rates". "[depression and lateral inhibition] should be
    essentially absent in our study, because our stimuli elicit only one or two spikes per ORN".
  - **Implication (mine).** This measures brief packets through rested synapses, with half the convergent input. It is
    not a check on 500-ms means at 6-20 Hz spontaneous rates with both antennae. The model's "≈4× at 5-10 Hz" is not
    comparable as run.
  - A comparable test: one side's ORNs only, the glomerulus at ≈1.5 Hz spontaneous, a 100-ms packet of ≈1.7 spikes per
    ORN, PN spikes counted over 120 ms.
- **Threshold and integration.**
  - "the distance to spike threshold, which was about 10 mV on average (Figure 4C)" (n = 18).
  - "If an ORN spike depolarizes the PN by about 2 mV ..., then 5 synchronous ORN spikes would be needed to generate a
    spike in the PN".
  - The first evoked PN spike comes at 30 ms. By then (less a 4.5-ms delay) "0.28 spikes per ORN" had accumulated, "a
    spike in about 11 ORNs".
  - "the best-fitting filter had a duration of 23 msec"; "a PN integrates ORN spikes over a window of approximately
    20–30 msec".
- **The 2-mV EPSP.** "an average amplitude of 2 mV appears reasonable, based on visual inspection of spontaneous EPSPs".
  KW08's rested 6.19 mV is the cut-nerve value.
- **IF model** (supplement; it fits first-spike latency near threshold): Rm "0.3 G", Cm "0.117 pF" (must be nF; τ 35
  ms), Vrest −55, threshold −40, reset −55 mV, refractory 2 ms; alpha EPSG τ 3 ms, peak 0.7 nS (started at 0.54 nS =
  30 pA/55 mV), Vrev 0; 40 ORNs; no depression.
  - "PN first spike latency was also lengthened when we reduced the number of ORNs in the presynaptic pool, even though we
    proportionately increased the synaptic conductance" (1 ORN with 40× conductance). A 3-fold weaker synapse also slowed
    it.
- **Noise.** Fig. S8: "A model PN which simply linearly sums the spike trains of 40 ORNs ... clearly under-predicts the
  noise in real PN spike trains". Adding 40 contralateral ORNs at "30% lower synaptic efficacy" raised spontaneous rate
  "only slightly". "the additional noise in PNs likely depends on neurons which are themselves driven by ORNs, such as
  local interneurons".

## 6. Convergence numbers: Gaudry 2013, Tobin 2017, Grabe 2016

- **Gaudry, Hong, Kain, de Bivort & Wilson 2013, Nature 493:424** ([PMC3590906](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/)).
  - "each ORN spike releases ~40% more neurotransmitter from the axon branch ipsilateral to the soma".
  - "ipsilateral sEPSCs were 39% larger than their contralateral counterparts" (DM6 pairs, n = 15).
  - With one antenna removed, ipsilateral PN firing was "on average about 50% higher" (DM6 slope 1.47 ± 0.09; DM1
    1.86).
  - "In DM1 PNs, spontaneous firing rates are close to zero."
- **Tobin, Wilson & Lee 2017, eLife 6:e24838** ([PMC5440167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/)), serial
  EM of DM6.
  - "53 ORNs innervated DM6, with 27 axons coming from the left antenna and 26 from the right". "each glomerulus
    contained the axons of 52 ORNs". Each tested ORN "contacted all 5 DM6 PNs".
  - "On average, unitary ORN→PN connections were composed of about 23 synapses". Counts range 10-36 per connection (CV
    0.31).
  - "ipsilateral uEPSPs are 27% stronger than contralateral uEPSPs" (modeled).
  - Dendritic size equalizes uEPSPs across PNs.
- **Grabe et al. 2016, Cell Rep 16:3401** (Table S1, [mmc1](https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc1.pdf)).
  OSNs per antenna or palp (females / males) and PNs per glomerulus:

  | glomerulus | OSNs ♀ / ♂ | PNs |
  |---|---|---|
  | DM4 | 23 / 15.5 | 1 |
  | DL5 | 24 / 21 | 1 |
  | DM1 | 38.5 / 32 | 1 |
  | VM7d | 11.5 / 15 | 2-3 |
  | VM2 | 18 / 15 | 2-3 |
  | DM6 | 18 / 10.5 | 3 |
  | DA1 | 62.5 / 62.25 | 8-10 |
  | VA2 | 43.5 / 32 | 1 |
  | DM2 | 8 / 8 | 2 |
  | DM3 | 34 / 31 | 1-2 |

  - Totals over both sides are about twice these. Tobin's EM count for DM6 (26-27 per side) is higher than Grabe's
    Gal4-based 18, so the light-microscopy counts may undercount.
  - KW09 counted "17.4 ± 0.9 per antenna" for DM4 (orn_dynamics.md §4).

## 7. Dynamics: the PN transient at weak input, and where it comes from

- **ORN level.** Martelli 2013: "Stimuli at the lower end of the dynamic range usually elicit a tonic response"
  (orn_dynamics.md §1.4). Olsen's own ORNs confirm it (§1.4): weak responses rise over ≈100-150 ms and hold, with
  late/peak ≈0.7-0.9. So the weak-input PN peak (late/peak 0.42) is not inherited from ORNs.
- **PNs respond to rate of change.** Kim, Lazar & Slutskiy 2015, eLife ([PMC4466247](https://pmc.ncbi.nlm.nih.gov/articles/PMC4466247/)):
  DM4 PNs and Or59b ORNs, acetone waveforms with on-line PID.
  - "At a fixed OSN spike rate (60 spike/s ...), the PN spike rate varies from 0 to 280 spike/s depending on the
    rate-of-change value of the OSN spike rate."
  - "the gain of the PN output with respect to the OSN rate of change decreased monotonically with concentration".
  - "To step-like OSN signals, PN showed a phasic onset response, followed by a tonic spiking pattern".
  - The model's input nonlinearity "exhibits a relatively high slope at low input amplitudes".
  - These are the expected signatures of a depressing synapse driven from a partly depleted resting state.
- **Inhibition.** Nagel 2015 (presynaptic_inhibition.md §4):
  - Blocking inhibition made long-pulse PN responses decay more (late/peak p = 3.8e-4). "Presynaptic inhibition at
    ORN-to-PN synapses decreases both EPSC amplitude and the rate of synaptic depression".
  - So inhibition sustains PN responses, and the strong transience in Fig. 8C with public odor reflects inhibition rising
    faster than the private input.
- **Nagel 2015's PN model is voltage only**, not spikes: "we modeled PN membrane potential responses to ORN spike
  trains", with "40 model ORNs", conductance-based, E_syn −10 mV, E_leak −70 mV. It found a depression-only synapse "more
  transient than real PNs" (orn_pn_depression.md §3.3).

## 8. Equalization (OCT vs MCH) and the transform

Data: ORN-level MCH/OCT ≈0.41-0.51 and PN-level 0.85-0.98 (Barth 2014; Badel 2016; oct_mch_input.md).

- **Published model.** Luo, Axel & Abbott 2010 ([PMC2890779](https://pmc.ncbi.nlm.nih.gov/articles/PMC2890779/)) use
  Eq. 1, r_PN = R_max·r_ORN^1.5 / (σ^1.5 + r_ORN^1.5 + (m·s_ORN)^1.5), "with R_max = 165 Hz, σ = 12 Hz, and m = 0.05
  Hz", where s_ORN is the sum of all ORN rates (20 Hallem-Carlson receptors).
  - "much, but not all, of the response magnitude equalization arises from the feedforward nonlinearity". Lateral
    suppression does most of the decorrelation.
- **The model's inputs through this equation (derived; DoOR × 200 spikes/s, the oct_mch_input.md §1 table).**

  | input | m | summed-PN MCH/OCT at σ 8 / 12 / 16 / 20 / 25 / 32 | glomeruli with PN > 20 Hz, OCT : MCH (σ 12 → 25) |
  |---|---|---|---|
  | DoOR only (ORN-level ratio 0.43) | 0 | 0.53 / 0.50 / 0.48 / 0.46 / 0.45 / 0.43 | 22 : 13 → 21 : 12 |
  | DoOR only | 0.05 | 0.66 / 0.64 / 0.63 / 0.61 / 0.59 / 0.56 | 18 : 12 → 17 : 12 |
  | + Barth ORN fills (0.47) | 0 | 0.67 / 0.64 / 0.61 / 0.59 / 0.56 / 0.53 | 23 : 17 → 22 : 16 |
  | + Barth ORN fills | 0.05 | 0.77 / 0.75 / 0.73 / 0.71 / 0.69 / 0.66 | 18 : 16 → 18 : 14 |

  - Going from the model's σ ≈ 25 to flies' 12 adds only ≈0.05-0.06 to the ratio. MCH's strong DoOR glomeruli (VA3 175,
    D 127, DA2 55, DM2 51 Hz) and OCT's many strong ones are above σ either way.
  - Reaching 0.85-0.98 needs MCH input in the glomeruli where Badel's PNs respond but no ORN data exist (VM7v, DA3, DL4,
    DA4l, DL3, DA1, VM3). These must be weak ORN inputs, and a low σ is what makes them count.
  - For example, adding 10 Hz of MCH input in those seven glomeruli (with Barth's fills and m = 0.05) gives ≈18
    spikes/s each at σ = 12 and lifts the ratio to 0.80. At σ = 25 they give ≈14 each and the ratio is 0.73 (derived).
  - Imaging ΔF/F saturation compresses both measured ratios, so the fly targets are approximate.

## 9. Toy PN with brainfly's settings (derived; my simulation)

**Setup.**
- One leaky integrate-and-fire PN driven by N independent Poisson ORNs at a spontaneous rate r0, each through its own
  depressing synapse.
- PN: threshold 7 mV above rest, reset to rest, refractory 2.2 ms, τm 20 ms, synaptic current kept through spikes.
- Synapse: a 5-ms current whose rested PSP peak is 6.19 mV; single pool f 0.78, τ 0.893 s; slow component 0.086 of the
  fast charge (τ 80 ms, f 0.9927, τ 33.2 s).
- A bias holds rest at ≈3 spikes/s. No LNs, no inhibition. 150 trials per point.
- σ and Rmax come from Eq. 1 fitted to 500-ms means at 5-160 Hz. "late/pk" is the mean over 400-500 ms divided by the
  peak 50-ms bin, both at x = 10 Hz.
- **Validation.** brainfly's DL5 (step) gives 19/42/79/110/139/170 spikes/s at 5/10/20/40/80/160 Hz, σ 23.4,
  Rmax 170.
  - At the model's 6 Hz spontaneous rate the toy matches it with N = 32: 20/46/83/115/142/170, σ 21.3, Rmax 169.
  - N = 40 at 8 Hz also matches: 18/42/81/113/143/173.
  - So the core synapse and LIF account for the model's single-glomerulus transform; the LNs and inhibition add little,
    as odor_weak_input_check found.
  - If MaleCNS gives DL5 more than ≈32 ORNs, the full model transmits less per ORN than a 6.19-mV rested connection.
    That would be consistent with the global weight factor undershooting DL5 (KW08 measured 7.0 mV there). Not checked.
- **Resting drive.** In this regime, 40 ORNs at 8 Hz put ≈26 mV of mean drive on the PN at rest (≈31 mV with 50
  ORNs), offset by a bias of ≈−31 mV.
  - Flies' resting ORN drive is only ≈5-10 mV (Gouwens & Wilson 2009: true rest "approximately −55 to −60 mV when
    spontaneous synaptic input from ORNs is intact and approximately −65 mV when input from ORNs is removed").
  - For DM4 the fly numbers agree with that: 35-46 ORNs × 3.44 Hz × 0.26 efficacy × 6.9 mV × ≈25 ms ≈ 5-7 mV (derived).

**Step protocol** (windows from step onset; N = 40, r0 = 8 unless noted)

| variant | 500-ms mean at 5/10/20/40/80/160 Hz | peak at 10 | peak/mean @10 | late/pk @10 | Rmax | σ |
|---|---|---|---|---|---|---|
| base | 18/42/81/113/143/173 | 80 | 1.88 | 0.25 | 173 | 23.3 |
| N 60 | 28/66/115/154/186/218 | 117 | 1.78 | 0.30 | 216 | 18.9 |
| N 80 | 38/85/143/185/218/250 | 150 | 1.76 | 0.29 | 246 | 16.4 |
| r0 3.4 Hz | 44/91/143/176/203/231 | 134 | 1.48 | 0.47 | 224 | 13.7 |
| r0 6 Hz (model's basiconic median) | 23/56/101/135/164/194 | 98 | 1.75 | 0.32 | 192 | 19.6 |
| r0 6 Hz, N 32 (matches brainfly DL5) | 20/46/83/115/142/170 | 83 | 1.80 | 0.29 | 169 | 21.3 |
| r0 15 Hz | 8/20/43/67/94/123 | 45 | 2.31 | 0.14 | 131 | 36.6 |
| unitary PSP 9 mV | 20/50/97/136/171/206 | 95 | 1.90 | 0.24 | 208 | 23.4 |
| threshold 10 mV | 16/36/67/94/119/144 | 67 | 1.86 | 0.26 | 144 | 23.1 |
| τm 30 ms | 18/39/69/95/119/142 | 68 | 1.76 | 0.31 | 141 | 21.3 |
| reset 5.5 mV | 28/76/152/211/268/312 | 149 | 1.96 | 0.21 | 318 | 22.8 |
| reset 5.5 + threshold jump 6 mV (τ 3 ms) | 25/64/121/165/204/233 | 119 | 1.88 | 0.23 | 236 | 20.3 |
| fast pool τ 0.3 s | 26/66/134/193/233/258 | 103 | 1.54 | 0.48 | 267 | 20.7 |
| two pools (M4, orn_pn_depression.md §7) | 17/40/79/117/152/185 | 69 | 1.70 | 0.39 | 190 | 26.6 |
| KW09 pool (0.72, 2.4 s) | 11/25/46/71/103/141 | 48 | 1.93 | 0.21 | 151 | 40.2 |
| slow component 0.774 (Nagel's fit) | 38/96/178/248/307/350 | 112 | 1.16 | 0.78 | 355 | 20.6 |
| tonic presynaptic divisor 2 | 23/55/105/150/181/204 | 73 | 1.33 | 0.55 | 209 | 20.3 |
| tonic presynaptic divisor 3 | 23/55/107/157/194/217 | 66 | 1.20 | 0.71 | 224 | 21.6 |
| no fast depression | 76/169/282/352/393/410 | 178 | 1.05 | 0.98 | 420 | 12.9 (rest 7.9 Hz) |

- The tonic divisor follows Nagel 2015's form: release and depletion both divided.
- Same r0/N gives similar but not equal σ: 20.3, 23.3 and 29.4 for N 20/40/80 at r0 4/8/16. σ falls roughly as 1/√N and
  rises faster than √r0, because higher spontaneous rates also deepen resting depletion.

**Olsen-like protocol** (ORN shape from Olsen Fig. S2, approximated as follows)
- 100-ms latency; first-order rise τ 40 ms (x < 20) or 25 ms; for x ≥ 20 an adaptation toward 0.65 of peak (τ 0.25 s).
- Offset at 520 ms with τ 60 ms.
- Scaled so the ORN's 0-500 ms window mean above baseline equals x. PN 500-ms window from valve opening,
  baseline-subtracted.

| variant | 500-ms mean at 5/10/20/40/80/160 Hz | peak at 10 | peak/mean @10 | late/pk @10 | Rmax | σ |
|---|---|---|---|---|---|---|
| N 40, r0 8 | 23/50/85/111/130/156 | 97 | 1.93 | 0.42 | 151 | 17.3 |
| N 32, r0 6 (brainfly DL5 equivalent) | 24/52/85/111/129/154 | 93 | 1.78 | 0.50 | 149 | 16.6 |
| N 35, r0 6 | 29/58/93/119/137/162 | 105 | 1.81 | 0.50 | 156 | 15.2 |
| N 40, r0 6 | 30/63/102/128/147/173 | 115 | 1.82 | 0.49 | 166 | 14.7 |
| N 48, r0 6 | 38/78/117/144/163/189 | 138 | 1.78 | 0.52 | 181 | 13.0 |
| N 60, r0 6 | 49/96/138/164/184/209 | 168 | 1.75 | 0.55 | 199 | 11.2 |
| N 40, r0 3.4 | 51/94/136/160/177/201 | 153 | 1.63 | 0.64 | 192 | 10.6 |
| N 40, r0 6, reset 5.5 + jump | 44/95/145/172/190/212 | 167 | 1.76 | 0.53 | 207 | 11.6 |
| N 48, r0 15 | 13/31/56/82/103/130 | 69 | 2.26 | 0.28 | 130 | 25.4 |
| N 40, r0 8, tonic divisor 3 | 28/59/104/144/170/186 | 88 | 1.50 | 0.82 | 189 | 17.5 |

- **Fly DL5 targets**: points (5.1, 44), (13.4, 85), (41.5, 149), (98.7, 158); σ 11.8, Rmax 167.
- **Fly VM7 targets**: peak 176 at x = 11.6; late/pk 0.42; peak/mean ≈2.1-2.5.
- **Closest toy row**: N 48, r0 6 interpolates to ≈38/91/145/168 at the DL5 x-values. That is within ≈10-15% of the
  points, with late/pk 0.52 against 0.42.

**What the toy says** (derived; caveat: one cell, no LNs, my approximations of the ORN shape)
- **Protocol.** Measuring as Olsen did lowers σ by ≈1.3× (21.3 → 16.6 for the brainfly-equivalent cell) and Rmax by
  ≈0.86-0.88×, and brings late/peak to 0.42-0.50 (flies 0.42). It is the largest single correction that needs no new
  biology.
- **What sets σ.** In this architecture σ is set mainly by the signal-to-noise of the convergent resting input: more
  converging ORNs help; a higher spontaneous rate hurts twice, through more resting noise and deeper resting depletion.
  Matching flies' DL5 points with the Olsen protocol takes ≈1.5× the brainfly-equivalent convergence (N ≈ 48 vs 32),
  or less resting depletion.
- **What does not.** Unitary size, threshold distance and τm barely move σ once rest is recalibrated, because they scale
  signal and noise together. A shallower reset raises responses everywhere (Rmax).
- **Contradiction with flies.** The toy predicts high-spontaneous glomeruli to be the least sensitive. Flies' DL5 (ab4A
  14-20 Hz at rest) has the lowest σ, while DM1, with low-to-moderate spontaneous ORN rates, is the least sensitive
  because of GABA. Flies therefore don't follow this scaling, which points to resting-state mechanisms the model lacks:
  - recovery during ongoing firing faster than the 0.9-s pool;
  - glomerulus-specific synaptic tuning;
  - a resting PN state not set by ORN shot noise alone (Jeanne & Wilson's extra LN-driven noise).

## 10. For the model

### 10.1 Diagnostics to run first (mine)
1. **Olsen protocol.**
   - Rerun odor_transform_check with a ≈110-ms ORN latency and Fig. S2's shapes: weak tonic rise τ ≈40 ms; strong peak at
     ≈190-260 ms then ≈0.65; offset decay ≈60-100 ms after 500 ms.
   - Use valve-aligned 500-ms windows on both axes and baseline subtraction.
   - Compare peak/mean with Fig. 8C's pentyl-acetate-0 points (≈2.3-2.5 weak and intermediate, 1.9 strong). Compare the
     PSTH with §1.5 (VM7 10⁻⁶: onset 100-125 ms, peak 176 at 175 ms, 0.42 of peak at 500 ms; 10⁻⁵: 296 at 150 ms, 0.44).
2. **Per-glomerulus uEPSP and ORN count in the model**, against KW08 (5.4-7.0 mV, matched) and Grabe's female counts.
   Start with DM4 (Rmax 81).
3. **DM1 with GABA blocked.** Flies' DM1 σ is 45 → 13.4 and Rmax 152 → 174 with PTX + CGP (refit of Fig. 1B). If the
   model's DM1 does not change, it lacks DM1's tonic or intraglomerular GABA.
4. **Jeanne & Wilson's regime**, if the near-threshold gain is to be cited as matched: one antenna, ≈1.5 Hz spontaneous,
   100-ms packets of ≈1.7 spikes per ORN, PN spikes counted over 120 ms. Flies: PN ≈3× ORN; first PN spike at ≈30 ms,
   after ≈11 of 40 ORNs have spiked.

### 10.2 Targets

| # | quantity | fly value | source |
|---|---|---|---|
| W1 | half-max of the private transform, Olsen's windows | DL5 12.2, VM7 13.2, DM4 17.7 Hz (DM1 35.8; 13.8 with GABA blocked) | Olsen Fig. 1B (derived, no model) |
| W2 | σ, Rmax (n = 1.5) | DL5 11.7/166, VM7 12.7/163, DM4 16.3/170; Δχ² ≤ 4 ranges in §1.3 | refit = published |
| W3 | PN/ORN at the lowest driven points | 5-9× at 5-13 Hz (DL5 5.1 → 44; DM4 5.0 → 28; VM7 11.6 → 78) | Olsen Fig. 1B |
| W4 | weak-input PSTH (VM7, 2-butanone 10⁻⁶, x ≈ 11.6) | onset 100-125 ms; peak 176 at 175 ms; 0.42 of peak at 500 ms; window mean ≈77-83 | Olsen Fig. 8A |
| W5 | intermediate PSTH (10⁻⁵, x ≈ 48) | peak 296 at 150 ms; 0.44 at 500 ms; mean ≈135-139 | Olsen Fig. 8B |
| W6 | peak/mean, private only | ≈2.3-2.5 (weak, intermediate), 1.9 (strong), valve-aligned; ≈1.7 from response onset | Fig. 8C; derived |
| W7 | peak/mean with public odor (pentyl acetate 10⁻³) | 6.9 weak, 3.05 intermediate, 2.0 strong | Fig. 8C |
| W8 | ORN window vs response-period means | ×1.10-1.29 (median ≈1.24); 64-81% of ORN response spikes inside the window | Olsen Fig. S2 (derived) |
| W9 | natural-odor transform (VM2, totals) | ORN 17-24 Hz → PN 55-84; plateau ≈90 | KW08 Fig. 9A |
| W10 | response histograms, 7 glomeruli × 18 odors (totals) | ORN 79% < 40 Hz; PN 56% > 40 Hz (bins in §4) | Bhandawat Supp. Fig. 5b |
| W11 | OCT/MCH summed PN ratio | 0.85-0.98; Olsen/Luo with DoOR inputs gives 0.64-0.75 at σ 12 | §8 (derived) |

### 10.3 Settings: what the evidence says

| setting | brainfly now | literature | verdict (mine) |
|---|---|---|---|
| transform protocol | step at t = 0; windows from step onset (25-ms latency in the time-course check) | Olsen: valve-aligned windows, responses start ≈100-125 ms later, ORN tails after 500 ms | change first; ≈1.3× in σ (toy) |
| ORN convergence | MaleCNS (male), 32-74 per glomerulus for these four | Grabe ♀ per side: DM4 23, DL5 24, DM1 38.5, VM7d 11.5; EM DM6 52-53 total | check against females; σ ∝ ≈1/√N in the toy |
| unitary EPSP | 6.19 mV mean same-glomerulus connection, one global factor | matched per glomerulus 5.4-7.0 mV (KW08); ipsi ≈27-40% > contra (Gaudry, Tobin) or equal (KW08) | calibrate per glomerulus; affects Rmax more than σ |
| ORN spontaneous rate | class medians 6 (antennal basiconic), 8 (palp) Hz | DL5 14-20, VM7d 10-16, DM1 9, DM4 3.4-11 Hz | don't raise until the depression model is revisited (raising worsens σ) |
| fast depression | single pool f 0.78, τ 0.893 s, ≈0.4 at rest | train fits disagree (orn_pn_depression.md); in vivo DM4 resting efficacy 0.26; post-train recovery τ ≈0.4 s | the resting state is the open question for weak-input gain |
| slow component | 0.086 of the fast charge | KW08 unitary ≈1% at the fast peak; Nagel's odor fit 0.774 | 0.774 makes responses too sustained (toy and probe36) |
| presynaptic inhibition at rest | ≈0.95 of strength (little tonic inhibition) | Nagel's model I_rest ≈4; DM1 tonic GABA; one glomerulus recruits little | not the σ lever (model check and toy); needed for DM1 and for W7 |
| PN threshold, τm | 7 mV, 20 ms | ≈10 mV (J&W); 17-31 ms (Gouwens & Wilson) | fine for σ |
| PN reset and refractoriness | reset to rest, 2.2 ms | not measured; somatic spikes ride on a sustained depolarization (Iniguez 2013: "large sustained membrane depolarizations capped by small fast spikelets") | affects peaks and Rmax; revisit only if those are short after the steps above |
| lateral excitation | electrical coupling tested, worsened weak input | removing gap junctions doesn't change a private-odor transform (Yaksi 2010) | not a σ lever |

### 10.4 Conflicts and gaps
- **Sensitivity ordering across glomeruli.**
  - Flies, by σ: DL5 ≈ VM7 < DM4 ≪ DM1 (GABA).
  - Model, by response at a given input, most to least sensitive: DM1, DL5, VM7d, DM4. DM4's low Rmax (81) puts its
    fitted σ (27.8) below VM7d's (30.7).
  - The model's ordering follows convergence and spontaneous rates (DM1 has the most ORNs). Flies' doesn't, apart from
    DM1's inhibition.
  - No study explains why a high-spontaneous glomerulus (DL5) stays the most sensitive.
- **Near-threshold gain.** J&W's ≈3× (brief packets, rested synapses, one antenna) and Olsen's 5-9× (500-ms means, both
  antennae, spontaneous firing) measure different things. Neither contradicts the other.
- **Ipsilateral vs contralateral.** KW08 found them equal (n = 20/24). Gaudry 2013 (39% larger ipsilateral sEPSCs) and
  Tobin 2017 (27%, modeled) found ipsilateral stronger. Jeanne & Wilson modeled contralateral as 30% weaker.
- **Resting ORN drive.** Flies ≈5-10 mV (Gouwens & Wilson, mostly DM1 PNs). The toy carries ≈20-30 mV offset by bias;
  brainfly reported 24 mV in odor_probe24, with the larger slow component then in use. Fly arithmetic is consistent only with low resting efficacy: DM4 0.26 at 3.4 Hz, and DM1 lower still given its
  77 ORNs at ≈9 Hz.
- **Not measured.**
  - PN f-I in vivo, PN reset or AHP, and fly synapse recovery during ongoing spontaneous firing.
  - Olsen's valve-to-arrival delay and the sex of Olsen's flies.
  - A spiking AL model fitted to Olsen's σ from measured parameters. Generic spiking AL models (Betkiewicz, Lindner &
    Nawrot 2020; Rapp & Nawrot 2020) tune ORN→PN weights to spontaneous rates and don't target σ.

## Sources

- Olsen SR, Bhandawat V, Wilson RI (2010). Divisive normalization in olfactory population codes. *Neuron* 66:287-299.
  - [PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/)
  - Figures: [Fig. 1](https://ars.els-cdn.com/content/image/1-s2.0-S0896627310002497-gr1_lrg.jpg),
    [Fig. 8](https://ars.els-cdn.com/content/image/1-s2.0-S0896627310002497-gr8_lrg.jpg)
  - [Supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0896627310002497-mmc1.pdf) (Fig. S2 on p. 6)
- Kazama H, Wilson RI (2008). Homeostatic matching and nonlinear amplification at identified central synapses. *Neuron*
  58:401-413.
  - [PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)
  - [Fig. 9](https://ars.els-cdn.com/content/image/1-s2.0-S0896627308001840-gr9_lrg.jpg)
- Kazama H, Wilson RI (2009). Origins of correlated activity in an olfactory circuit. *Nat Neurosci* 12:1136-1144.
  [PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/)
- Bhandawat V, Olsen SR, Gouwens NW, Schlief ML, Wilson RI (2007). Sensory processing in the *Drosophila* antennal lobe
  increases reliability and separability of ensemble odor representations. *Nat Neurosci* 10:1474-1482.
  - [PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/)
  - [Supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnn1976/MediaObjects/41593_2007_BFnn1976_MOESM22_ESM.pdf)
- Jeanne JM, Wilson RI (2015). Convergence, divergence, and reconvergence in a feedforward network improves neural speed
  and accuracy. *Neuron* 88:1014-1026.
  - [PMC5488793](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/)
  - [Supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0896627315008843-mmc1.pdf)
- Gouwens NW, Wilson RI (2009). Signal propagation in *Drosophila* central neurons. *J Neurosci* 29:6239-6249.
  [PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/)
- Nagel KI, Hong EJ, Wilson RI (2015). Synaptic and circuit mechanisms promoting broadband transmission of olfactory
  stimulus dynamics. *Nat Neurosci* 18:56-65. [PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/)
- Gaudry Q, Hong EJ, Kain J, de Bivort BL, Wilson RI (2013). Asymmetric neurotransmitter release enables rapid odour
  lateralization in *Drosophila*. *Nature* 493:424-428. [PMC3590906](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/)
- Tobin WF, Wilson RI, Lee WCA (2017). Wiring variations that enable and constrain neural computation in a sensory
  microcircuit. *eLife* 6:e24838. [PMC5440167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/)
- Grabe V, Baschwitz A, Dweck HKM, Lavista-Llanos S, Hansson BS, Sachse S (2016). Elucidating the neuronal architecture of
  olfactory glomeruli in the *Drosophila* antennal lobe. *Cell Rep* 16:3401-3413.
  - [doi:10.1016/j.celrep.2016.08.063](https://doi.org/10.1016/j.celrep.2016.08.063)
  - [Table S1](https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc1.pdf)
- Kim AJ, Lazar AA, Slutskiy YB (2015). Projection neurons in *Drosophila* antennal lobes signal the acceleration of
  odor concentrations. *eLife* 4:e06651. [PMC4466247](https://pmc.ncbi.nlm.nih.gov/articles/PMC4466247/)
- Luo SX, Axel R, Abbott LF (2010). Generating sparse and selective third-order responses in the olfactory system of the
  fly. *PNAS* 107:10713-10718. [PMC2890779](https://pmc.ncbi.nlm.nih.gov/articles/PMC2890779/)
- Wilson RI (2013). Early olfactory processing in *Drosophila*: mechanisms and principles. *Annu Rev Neurosci*
  36:217-241. [PMC3933953](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)
- Martelli C, Carlson JR, Emonet T (2013). Intensity invariant dynamics and odor-specific latencies in olfactory receptor
  neuron response. *J Neurosci* 33:6285-6297. [PMC3678969](https://pmc.ncbi.nlm.nih.gov/articles/PMC3678969/) (via
  orn_dynamics.md)
- Stevens CF (2015). What the fly's nose tells the fly's brain. *PNAS* 112:9460-9465.
  [PMC4522789](https://pmc.ncbi.nlm.nih.gov/articles/PMC4522789/)
- Stevens CF (2016). A statistical property of fly odor responses is conserved across odors. *PNAS* 113:6737-6742.
  [PMC4914196](https://pmc.ncbi.nlm.nih.gov/articles/PMC4914196/)
- Betkiewicz R, Lindner B, Nawrot MP (2020). Circuit and cellular mechanisms facilitate the transformation from dense to
  sparse coding in the insect olfactory system. *eNeuro* 7:ENEURO.0305-18.2020.
  [PMC7294456](https://pmc.ncbi.nlm.nih.gov/articles/PMC7294456/)
- Rapp H, Nawrot MP (2020). A spiking neural program for sensorimotor control during foraging in flying insects. *PNAS*
  117:28412-28421. [PMC7668073](https://pmc.ncbi.nlm.nih.gov/articles/PMC7668073/)
- Cafaro J (2016). Multiple sites of adaptation lead to contrast encoding in the *Drosophila* olfactory system. *Physiol
  Rep* 4:e12762. [PMC4831330](https://pmc.ncbi.nlm.nih.gov/articles/PMC4831330/) (checked; PN adaptation to long
  backgrounds, not used here)
- Data cited through the related notes: Yaksi E, Wilson RI (2010), *Neuron* 67:1034
  ([PMC2954501](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/)); Iniguez J et al. (2013), *J Neurophysiol* 110:1490
  ([PMC4042424](https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/)); Barth J et al. (2014), *J Neurosci* 34:1819
  ([PMC6827587](https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/)); Badel L et al. (2016), *Neuron* 91:155
  ([doi](https://doi.org/10.1016/j.neuron.2016.05.022)).
