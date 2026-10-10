# Hige et al. 2015: how specific is the depression in MBON-γ1pedc (MBON11)?

Hige, Aso, Modi, Rubin & Turner 2015, "Heterosynaptic plasticity underlies aversive olfactory learning in Drosophila",
Neuron 88:985–998 ([PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/), doi:10.1016/j.neuron.2015.11.003).

Read 2026-10-10. Sources:
- PMC author manuscript: full text, figure legends and Experimental Procedures.
- The publisher's open-archive PDFs: "Article plus Supplemental Information" and "Supplemental Information" (Figures S1–S7
  and their legends).
- The publisher's 500-dpi figure images (Figures 1–7) and the 300-ppi images in the supplement.

Quotes are from the PMC author manuscript. The published version says the same with small copy-edits (for example
"90% ± 3.7%" and "repeated-measures").

Conventions:
- "(fig., approx.)" means I measured it from figure pixels. Each figure's section gives the tick calibration.
- "(derived)" means my own arithmetic.
- "±" on a figure value is half the error bar as drawn. The legends say bar plots are "± SEM".
- Percent "decrease" is 100 × (1 − post/pre).

## Summary

1. **Fig. 3: voltage clamp with QX-314, n = 5 cells, OCT paired in every cell.**
   - Charge over 0–1.4 s (fig., approx.):
     - OCT (CS+): 248 ± 40 → 26 ± 12 pC.
     - MCH (CS−): 273 ± 48 → 219 ± 46 pC.
   - Post/pre of the means: OCT 0.11, MCH 0.80 (derived).
   - Per cell, MCH post/pre was 0.81, 0.56, 0.52, 1.10 and 1.08 (fig., approx.). That is a mean decrease of 19 ± 12%,
     and two of the five cells went up slightly (derived).
   - Statistics, exactly as written: "Excitatory synaptic input decreased for CS+ (p < 0.005, Tukey’s post hoc test
     following repeated measures two-way ANOVA) but not for CS− (p > 0.1)."
   - Fig. 3 gives no odor × pairing interaction p.
   - CS+ in the text: "The average reduction in charge transfer was 90 ± 3.7 % (mean ± SEM; Fig 3D)".
   - Not counterbalanced: the Fig. 3B schematic pairs OCT, and no MCH-paired voltage-clamp group exists.
2. **Fig. 4: pairing under voltage clamp without QX-314, n = 6, same cells for spikes and EPSCs, OCT paired.**
   - Charge (fig., approx.):
     - OCT: 244 ± 28 → 62 ± 9 pC.
     - MCH: 230 ± 27 → 150 ± 22 pC.
   - Post/pre of the means: 0.25 for OCT and 0.65 for MCH (derived).
   - All six cells lost MCH charge. Per-cell post/pre ran from 0.56 to 0.78, a mean decrease of 35 ± 4% (derived). The
     CS+ per-cell decrease was 74 ± 3% (derived).
   - Spikes in the same cells, Fig. 4E (fig., approx.): OCT 116 ± 11 → 17 ± 4, MCH 110 ± 12 → 68 ± 17. MCH fell 38%
     (derived).
   - The quote you gave is exact: "Charge transfer decreased in CS+ (p < 0.001, Tukey’s post hoc test) and CS−
     (p < 0.001), but the effect of pairing was significantly different between the two odors (p < 0.005, repeated
     measures two-way ANOVA)."
   - "83 ± 4.5 %" is the share of odor-evoked spikes that the clamp blocked during the pairing trial. It is not a
     plasticity measure.
3. **Fig. 1: n = 7, OCT paired, MCH unpaired.**
   - The text numbers are confirmed: 118 ± 8.3 → 24 ± 7.4 and 110 ± 11 → 83 ± 14. My reading of Fig. 1F reproduces
     them within 0.5 spike.
   - OCT was CS+ in all 7 flies. The reciprocal, with MCH paired, is a separate group of flies (Fig. S3, n = 6).
     Fig. S4 mixes 3 OCT-paired and 3 MCH-paired flies.
   - The CS− decrease was itself significant: "CS− (MCH, p < 0.01)". The text gives the CS− reduction as
     "27 ± 7.1 %". Per fly it ran from 6 to 53% (fig., approx.).
4. **Other measurements of the unpaired odor (spike counts; table in §4).**
   - Reciprocal, Fig. S3 (OCT as CS−): −38%.
   - Fig. S4 time course: the CS− response was 0.70 ± 0.04 of pre at 10 min, recovering to 0.98 ± 0.06 at 40 min.
   - TH-GAL4 (Fig. 5H): −18%.
   - Single light pulse (Fig. S6I): "20 ± 6.3 %".
   - 1-min protocol in γ1pedc (Fig. S6E): −14%, not significant. 1-min protocol in α2sc (Fig. 6H): −11%, not
     significant.
   - No change with MB099C (Fig. 5D), in MBON-γ2α′1 (Fig. 5L), or in flies without the driver (Fig. S5).
   - Generalization odors (Fig. 7): depression of 12–36% for odors whose KC responses overlap little with the CS+, and
     66–73% for those that overlap a lot.
5. **Backward pairing (Fig. 1J, n = 7).**
   - The text gives no numbers. It says only "Backward pairing showed no effect (p > 0.05, repeated measures two-way
     ANOVA)".
   - From the figure: OCT 94 ± 12 → 100 ± 12 and MCH 83 ± 14 → 80 ± 12 (fig., approx.). That is +7% and −4% (derived).
6. **Kenyon cells (Fig. 2, Fig. S7).**
   - The text gives no response values, only n and p.
   - From the figure: per-cell post-vs-pre regression slopes are about 0.76 for CS+, 0.78 for CS− and 0.83 with no
     light (fig., approx.). The histograms of change peak at about −0.25 to −0.4 ΔF/F in all three groups.
   - Kolmogorov–Smirnov p > 0.1; population-distance p = 0.58.
   - γ KC excitability is unchanged (Fig. S7).
7. **Suggested pre-registered bands (§8).**
   - CS− spike decrease 10–45%. Flies: 27 ± 7.1%, n = 7, 95% CI 10–44% (derived).
   - CS− charge decrease 10–45%. Flies: 19% and 35% in the two groups, pooled 28 ± 6% with 95% CI 14–41% (derived).
   - CS+ decrease at least 65%, and at least 30 percentage points more than CS−.
   - Reciprocal (MCH paired): OCT decrease 15–50%.
   - Backward pairing: change within ±15%.

## 1. How the figure values were read

- **Images.** Main figures are the publisher's 500-dpi JPEGs (`1-s2.0-S0896627315009824-gr{1..7}_lrg.jpg` on
  ars.els-cdn.com). Supplementary figures are the images embedded in the Supplemental Information PDF (mmc1).
- **Calibration.** Tick centres are darkness-weighted centroids of the tick marks, fitted with a straight line. The
  residuals are under 0.7 px everywhere.
- **Bars and error bars.**
  - A bar's value is the centre of its top outline.
  - Error-bar caps were measured on the side of the error bar that the individual-fly lines don't reach: the left side
    for Pre bars, the right side for Post bars.
- **Individual-fly ("gray") lines.**
  - Each line was fitted as a straight segment through its gray pixels and evaluated at the two bar centres, where
    MATLAB draws the endpoints.
  - Every fit was checked by an overlay, and by requiring that the lines' means reproduce the bar heights.
- **Precision.** High-resolution figures: ±1 px is ±0.6–1.6 units (spikes or pC). Supplementary figures: about 1.1–1.4
  spikes per px. Where gray lines overlap, individual values are only good to about ±3–5 units, and those are marked
  "rough".
- **Validation against the text:**
  - Fig. 1F bars read 118.4 (+8.5/−7.9), 24.0 (+7.5/−7.2), 110.0 (+10.2/−10.7) and 82.8 (+13.7/−13.4). The text says
    118 ± 8.3, 24 ± 7.4, 110 ± 11 and 83 ± 14.
  - The per-fly CS− decrease from Fig. 1F's gray lines is 27.1 ± 7.2%; the text says 27 ± 7.1%.
  - The per-cell CS+ charge decrease from Fig. 3D's gray lines is 88.9 ± 3.8%; the text says 90 ± 3.7%.

## 2. Fig. 3: EPSCs with QX-314, pairing with spikes fully blocked (n = 5)

**Conditions**
- "Whole-cell voltage-clamp recordings were made from MBON-γ1pedc. Action potentials were completely suppressed by
  QX-314 in the pipette solution." (Fig. 3A)
- Internal solution: cesium aspartate with "QX-314, 10" mM. "Cells were held at −70 or −60 mV, and cells that showed
  unclamped spikes during odor response were discarded."
- "EPSC charge transfer was calculated using the same time window" as the spike counts: "0 to 1.4 sec from odor onset".

**Which odor was paired**
- OCT. Fig. 3B's protocol schematic shows OCT with the four red light pulses, and the columns are labelled OCT and MCH.
- The legend itself says only "CS+" and "CS−". No MCH-paired voltage-clamp group exists, so this was not
  counterbalanced.
- (The imaging methods say "using OCT as CS+".)

**Text and legend**
- "We observed large odor-evoked EPSCs that typically exceeded 200 pA in amplitude and were sustained throughout the
  duration of the odor pulse. After 1-s pairing of odor presentation and PPL1-γ1pedc activation, the EPSCs showed a
  marked depression in a stimulus-specific manner, with the current dramatically reduced early in the response, and
  essentially no sustained current visible at later time points (Figures 3B-3D)."
- "The average reduction in charge transfer was 90 ± 3.7 % (mean ± SEM; Fig 3D), which is of similar order to the
  80 ± 5.7 % reduction in spiking we observed (Figure 1F)."
- Fig. 3D legend: "(D) Mean charge transfer of EPSC (± SEM). Gray lines indicate data from individual flies. Excitatory
  synaptic input decreased for CS+ (p < 0.005, Tukey’s post hoc test following repeated measures two-way ANOVA) but not
  for CS− (p > 0.1)."
- Odor × pairing interaction p for Fig. 3: **Not reported.**
- Absolute charges: **not in the text.**

**Fig. 3D bars (fig., approx.).** y ticks 400/300/200/100/0 pC sit at y = 1792.0/1853.2/1915.5/1976.4/2038.6 px, i.e.
0.6165 px per pC (1 px ≈ 1.6 pC). The MCH axis is unlabelled but its ticks sit at the same pixels.

| Odor | Pre (pC) | Post (pC) | Post/pre of means (derived) |
|---|---|---|---|
| OCT (CS+) | 248 (+40.5/−40.2) | 26 (+12.0/−11.6) | 0.11 |
| MCH (CS−) | 273 (+47.2/−48.5) | 219 (+45.8/−46.7) | 0.80 |

**Fig. 3D individual cells (fig., approx.)**

| Odor | Cells, pre → post (pC) | Per-cell post/pre |
|---|---|---|
| OCT | 395→65, 263→≈0 (line reaches the axis; extrapolates to −6), 239→35, 201→37, 152→12 | 0.16, ≈0, 0.15, 0.19, 0.08 |
| MCH | 464→374, 256→143, 206→108, 213→235, 222→239 | 0.81, 0.56, 0.52, 1.10, 1.08 |

- Two MCH lines (213→235 and 222→239) overlap along most of their length, and the 222 end is hidden behind the
  error-bar cap. I read them from the edges of the gray band. The five MCH lines average 272 → 220 pC, matching the
  bars (273 → 219).
- (derived) OCT: mean per-cell decrease 88.9 ± 3.8% (SD 8.4).
- (derived) MCH: mean per-cell decrease 18.7 ± 12.3% (SD 27.5). The 95% CI is −15% to +53% (t₄ = 2.776).
- (derived) With n = 5 and an SD of 27.5%, "p > 0.1" does not mean the CS− response was unchanged. A paired t-test on
  these five values gives t ≈ 1.5, p ≈ 0.2, so the test had little power to detect a decrease of about 20%. The paper
  itself used Tukey tests after a two-way ANOVA.

## 3. Fig. 4: pairing under voltage clamp without QX-314 (n = 6)

**Conditions**
- Fig. 4B legend: "After recording baseline odor responses in current-clamp mode, recording mode was switched to voltage
  clamp to record EPSCs. Odor-light pairing (1-s odor with 1-ms light pulses × 4) was performed under voltage-clamp
  mode, which suppressed 83 ± 4.5 % of odor-evoked spikes (mean ± SEM, n = 6). After pairing, spikes and EPSCs were
  recorded by flipping the mode between current-clamp and voltage-clamp."
- The Results say the same: "This suppressed odor-evoked spikes by 83 ± 4.5 % (mean ± SEM, n = 6). In this condition,
  we still observed a similar level of depression in spike rates (Figures 4C-4E) as we observed after pairing in
  current-clamp mode (Figures 1D-1F). Importantly, EPSCs also underwent a similar degree of LTD (Figures 4F-4H) to that
  we observed with complete block of spiking (Figure 3)."
- So the 83% is how many spikes the clamp blocked during the pairing trial. The cell still fired some unclamped spikes.
- Internal solution was potassium-based. "For the data from voltage-clamp recordings with potassium-based internal
  solution, current surges associated with unclamped action potentials were removed by low-pass filtering with cut-off
  frequency of 100 Hz before calculating the charge transfer."
- The paired odor was OCT: Fig. 4B's protocol puts the red pulses on OCT.

**Legends**
- (E): "Spike counts decreased in both CS+ (p < 0.001, Tukey’s post hoc test) and CS− (p < 0.01), but the effect of
  pairing was significantly different between the two odors (p < 0.005, repeated measures two-way ANOVA)."
- (H): "Charge transfer decreased in CS+ (p < 0.001, Tukey’s post hoc test) and CS− (p < 0.001), but the effect of
  pairing was significantly different between the two odors (p < 0.005, repeated measures two-way ANOVA)."
- Means, SEMs and ratios: **not in the text**. The values below are from the figure.

**Fig. 4H charge (fig., approx.).** y ticks 300/200/100/0 pC at y = 1272.3/1345.7/1418.5/1492.1 px, i.e. 0.732 px per
pC.

| Odor | Pre (pC) | Post (pC) | Post/pre of means (derived) |
|---|---|---|---|
| OCT (CS+) | 244 (+28.1/−28.9) | 62 (drawn +9.8/−6.9; per-cell SEM 8.6) | 0.25 |
| MCH (CS−) | 230 (+26.8/−27.6) | 150 (+22.7/−22.3) | 0.65 |

- Individual cells (fig., approx.):
  - OCT: 359→60, 269→94, 260→52, 232→82, 187→47, 160→40. Per-cell post/pre 0.17, 0.35, 0.20, 0.35, 0.25, 0.25.
  - MCH: 336→218, 279→217, 221→124, 206→155, 174→102, 158→90. Per-cell post/pre 0.65, 0.78, 0.56, 0.75, 0.59, 0.57.
- (derived) OCT per-cell decrease 73.7 ± 3.1%. MCH per-cell decrease 35.0 ± 3.9% (SD 9.6), 95% CI 25–45% (t₅ = 2.571).
- **The CS− charge decrease was 35%. All six cells decreased, by between 22% and 44%.**

**Fig. 4E spikes in the same cells (fig., approx.).** y ticks 150/100/50/0 at y = 1250.1/1330.2/1410.4/1490.5 px, i.e.
1.603 px per spike.

| Odor | Pre | Post | Post/pre of means (derived) |
|---|---|---|---|
| OCT (CS+) | 116 (+11.1/−11.6) | 17 (+4.8/−3.9) | 0.14 |
| MCH (CS−) | 110 (+12.2/−11.6) | 68.5 (+17.0/−16.8) | 0.62 |

- Individual cells (fig., approx.; lines overlap, rough):
  - OCT: 157→15, 126→36, 121→23, 116→14, 103→19, 73→6.
  - MCH: 144→130, 143→91, 117→90, 95→35, ≈82→≈30, ≈80→≈38.
- (derived) MCH per-cell decrease 41 ± 9%.

## 4. Fig. 1: spikes, forward pairing (n = 7)

**Text**
- "We then carried out a single pairing of OCT (CS+; duration, 1 s) with four pulses of 1-ms light (2 Hz; Figure 1C),
  which evoked reliable spike trains in PPL1-γ1pedc (Figure S2). After this brief pairing, we observed a profound
  suppression in the MBON response to the CS+ (pre-pairing: 118 ± 8.3 spikes, post: 24 ± 7.4, mean ± SEM; n = 7),
  while the unpaired odor (MCH; CS-) was minimally affected (Figures 1D-1F; pre: 110 ± 11 spikes, post: 83 ± 14). We
  observed an equivalent effect when we used MCH as CS+ and OCT as CS− (Figure S3)."
- Confirmed. The figure reads 118.4, 24.0, 110.0 and 82.8 (§1).

**Legend**
- Fig. 1F: "(F) Mean odor-evoked spike count (± SEM). Gray lines indicate data from individual flies. Spike counts
  decreased in both CS+ (OCT, p < 10^−4, Tukey’s post hoc test) and CS− (MCH, p < 0.01), but the effect of pairing was
  significantly different between odors (p < 0.001, repeated measures two-way ANOVA)."
- **So the CS− decrease was itself significant (p < 0.01).** The text later says: "reciprocally pairing either OCT or
  MCH with DAN activation also slightly but significantly depressed responses to the other odor (Figures 1E and 1F and
  Figure S3)".

**Sizes stated in the text**
- CS−: "(20 ± 6.3 %, mean ± SEM; Figures S6G-S6I versus 27 ± 7.1 %; Figure 1)". So 27 ± 7.1% is the Fig. 1 CS−
  reduction.
- CS+: "80 ± 5.7 % reduction in spiking".
- (derived) Ratio of means for MCH: 83/110 = 0.75. The per-fly average (27%) is larger than the drop in the means
  (25%) because flies with smaller responses lost proportionally more.

**Counterbalancing**
- OCT was CS+ in all seven flies of Fig. 1. MCH as CS+ is a separate group (Fig. S3, n = 6).
- Fig. S4 used "Either OCT (n = 3) or MCH (n = 3)" as CS+.
- Fig. 1 E–F includes one cell-attached recording: "Since the effects on spikes were indistinguishable between
  whole-cell and cell-attached recordings, we present them as one data set."

**Fig. 1F individual flies (fig., approx.).** y ticks 150/100/50/0 at y = 474.7/556.0/636.4/717.7 px, i.e. 1.619 px per
spike.
- MCH (CS−): 150→136, 137→102, 109→102, 107→96, 102→61, 97→55, 65→30. Per-fly post/pre 0.90, 0.74, 0.94, 0.90, 0.60,
  0.56, 0.47.
- (derived) The decrease is 27.1 ± 7.2% (SD 19.0), with a 95% CI of 9.6–44.6% (t₆ = 2.447) and a range of 6–53%. Flies
  with larger responses lost less.
- OCT (CS+; three lines overlap near 120–128, rough): 149→47, 136→54, 128→9, 121→13, ≈118→≈20, 96→3, 85→31.
- (derived) OCT per-fly decrease ≈ 79%; the text says 80 ± 5.7%.

**Protocol timing** (Experimental Procedures)
- "Pre-pairing odor responses were measured by presenting 1-s odor pulses with inter-stimulus interval of 25 s. In
  experimental situations with just two odors, they were presented alternately."
- "After recording a stable odor-response baseline, which typically took 5 trials (ranging from 3 to 10), odor-light
  pairing was performed 1 min after the last odor pulse of the pre-pairing series."
- "The CS− was then presented 1 min after the CS+ pairing. Post-pairing odor responses were recorded starting 1 to
  1.5 min after this CS− presentation. Each odor was presented typically 5 times, at least 3 times, in this post-pairing
  period".
- (derived) So "post" spans roughly 2–6 min after pairing.

## 5. Every other measurement of the unpaired odor in the paper

All are MBON-γ1pedc spike counts unless the Condition column names another MBON. Test pulses are 1 s in every row,
and odors are 2% saturated vapour except in Fig. 7 (1%). Values are (fig., approx.); every % is (derived) from the
bar means.

| Figure | Condition | n | Paired odor: pre → post | Unpaired odor: pre → post | Unpaired change | Paper's statistics |
|---|---|---|---|---|---|---|
| S3D | MB320C, **MCH paired**, 4 pulses | 6 | MCH 103 ± 17 → 25 ± 10 (−76%) | OCT 94.5 ± 19 → 59 ± 15 | **−38%** | "Spike counts decreased in both CS+ (MCH, p < 0.001, Tukey’s post hoc test) and CS- (OCT, p < 0.01), but the effect of pairing was significantly different between odors (p < 0.005, repeated measures two-way ANOVA)." |
| 4E | Pairing under voltage clamp (§3) | 6 | OCT 116 → 17 (−86%) | MCH 110 → 68.5 | −38% | as §3 |
| 5H | TH-GAL4 (broad PPL1, incl. PPL1-γ1pedc) | 5 | OCT 98 ± 17 → 14 ± 4.5 (−86%) | MCH 101 ± 17 → 82 ± 14.5 | −18% | "Spike counts decreased in both CS+ (p < 0.01, Tukey’s post hoc test) and CS− (p < 0.01), but the effect of pairing was significantly different between the two odors (p < 0.05, repeated measures two-way ANOVA)." |
| S6I | MB320C, **single 1-ms pulse** 0.8 s after odor onset | 5 | OCT 106 ± 12 → 40 ± 7 (−62.5%) | MCH 97 ± 10 → 77 ± 9 | −20% (text "20 ± 6.3 %") | "Spike counts decreased in both CS+ (p < 0.001, Tukey’s post hoc test) and CS- (p < 0.05), but the effect of pairing was significantly different between the two odors (p < 0.005, repeated measures two-way ANOVA)." |
| S6E | MB320C, **1-min odor, 120 pulses** | 6 | OCT 82 ± 14.5 → 7 ± ≈2 (−92%) | MCH 90 ± 16 → 77 ± 12 | −14%, not significant | "Spike counts decreased in CS+ (p < 0.005, Tukey’s post hoc test) but not in CS- (p > 0.4), and the effect of pairing was significantly different between the two odors (p < 0.005, repeated measures two-way ANOVA)." |
| S5D | No driver (CsChrimson without GAL4), same light | 6 | OCT 75 ± 9 → 74 ± 11 (−1.5%) | MCH 89 ± 18 → 83 ± 16.5 | −7% | "Pairing had no significant effect (p > 0.3, repeated measures two-way ANOVA)." |
| 5D | MB099C (PPL1-γ2α′1 etc., not PPL1-γ1pedc) | 8 | OCT 74 ± 12 → 70 ± 13 (−6%) | MCH 87 ± 11 → 88 ± 10 | +0.5% | "Pairing had no significant effect (p > 0.05, repeated measures two-way ANOVA)." |
| 5L | **MBON-γ2α′1** recorded, MB320C pairing | 6 | OCT 105 ± 22 → 90 ± 15 (−14%) | MCH 89 ± 21 → 92 ± 17.5 | +3% | "Pairing showed no effect (p > 0.1, repeated measures two-way ANOVA)." |
| 6D | **MBON-α2sc**, MB099C, 1-s protocol | 7 | OCT 85 ± 7 → 76 ± 6 (−10%) | MCH 72 ± 7.5 → 72 ± 6 | +0.6% | "Pairing showed no effect (p > 0.1, Tukey’s post hoc test following repeated measures two-way ANOVA)." |
| 6H | **MBON-α2sc**, 1-min protocol | 6 | OCT 74 ± 6 → 5 ± 3 (−93%) | MCH 66 ± 7 → 59 ± 6 | −11%, not significant | "Spike counts decreased in CS+ (p < 10^−5, Tukey’s post hoc test) but not in CS− (p > 0.1), and the effect of pairing was significantly different between the two odors (p < 0.001, repeated measures two-way ANOVA)." |
| 7E | PA paired, single pulse, 1% odors | 7 | PA 106 ± 17 → 16.5 ± ≈3 (−84%) | BA 106 ± 17 → 28.5 ± 4.5; HP 91 ± 15.5 → 30 ± 6; EL 88 ± 15 → 72 ± 9 | BA −73%, HP −67%, EL −18% | "Depression was significant for PA, BA and HP (p < 0.005 ...) but not for EL (p > 0.1). Depression of PA was slightly stronger than BA and HP (p < 0.05, paired t-test)." |
| 7H | EL paired, single pulse, 1% odors | 5 | EL 83 ± 19 → 20 ± 9 (−76%) | PA 99 ± 9 → 70.5 ± 9; BA 98 ± 9.5 → 74.5 ± 10; HP 83 ± 9.5 → 53 ± 5.5 | PA −29%, BA −24%, HP −36% | "Depression was significant for EL (p < 0.01 ...) and HP (p < 0.05) but not for the others (p > 0.05). Depression of EL was stronger than HP (p < 0.05, paired t-test)." |

Calibration for these panels (fig., approx.):

| Panel | Ticks (top to bottom) | Pixel positions (y) | px per spike |
|---|---|---|---|
| 5D | 150/100/50/0 | 495.5/580.2/664.0/748.7 | 1.686 |
| 5H | 150/100/50/0 | 1399.5/1484.2/1569.9/1655.5 | 1.707 |
| 5L | 150/100/50/0 | 2320.2/2400.2/2480.1/2560.9 | 1.604 |
| 6D | 100/50/0 | 516.7/634.5/753.5 | 2.368 |
| 6H | 100/50/0 | 1394.4/1523.8/1654.2 | 2.598 |
| 7E | 150/100/50/0 | 474.0/536.4/598.9/661.4 | 1.249 |
| 7H | 150/100/50/0 | 1223.8/1297.8/1372.8/1447.8 | 1.494 |
| S3D | 150/100/50/0 | 285.0/321.5/358.0/394.5 | 0.730 |
| S5D | 150/100/50/0 | 260.0/304.5/349.5/394.5 | 0.897 |
| S6E | 150/100/50/0 | 259.0/303.5/348.5/393.5 | 0.897 |
| S6I | 150/100/50/0 | 264.0/307.5/351.0/394.5 | 0.870 |

**Fig. S3 individual flies, OCT as CS− (fig., approx.; rough, 1.4 spikes per px)**
- 172→127, 111→52, 95→75, 73→58, 73→34, 32→20. Per-fly post/pre 0.46–0.79; all six went down.
- (derived) Mean decrease ≈ 36 ± 6%, 95% CI ≈ 20–51%.
- This is the only measurement of OCT as the unpaired odor. No charge was measured with MCH paired: **Not reported**.

**Fig. S4C time course** ("normalized to pre-pairing data (± SEM; n = 6)"; 3 OCT-paired and 3 MCH-paired flies).
Ticks 1.2/1.0/…/0 at y = 88.5/157.5/226.5/295.5/364.0/433.0/502.0 px, i.e. 345 px per unit.

| Time after pairing | CS+ (normalized) | CS− (normalized) |
|---|---|---|
| 10 min | 0.18 ± 0.07 | 0.70 ± 0.04 |
| 20 min | 0.19 ± 0.06 | 0.75 ± 0.03 |
| 30 min | 0.21 ± 0.07 | 0.85 ± 0.03 |
| 40 min | 0.35 ± 0.11 | 0.98 ± 0.06 |

- All values (fig., approx.). Individual CS− flies at 10 min ≈ 0.6–0.8 (fig., approx.).
- Legend: "CS+ responses remained depressed at all time points (p < 0.05, Tukey’s post hoc test following repeated
  measures two-way ANOVA), while CS- responses were no longer significantly depressed after 30 min (p > 0.1)."
- Text: "The suppression persisted throughout the duration of the recordings, which lasted at least 40 min, and showed
  only a small sign of recovery in that time (Figure S4)."

**Fig. 7I, depression against KC overlap** (fig., approx.).
- Axis calibration: depression 0.8/0.6/0.4/0.2 at y = 1719.8/1822.3/1923.9/2025.6 px. Overlap 0.4/0.6/0.8/1.0 at
  x = 508.0/613.9/718.8/824.6 px.
- Points, as (overlap, depression [error-bar extent]):
  - (1.00, 0.80 [0.67–0.95]). The marker is larger than the others, probably two coincident points: PA after PA
    pairing and EL after EL pairing (my inference).
  - (0.63, 0.69 [0.61–0.76]) and (0.45, 0.66 [0.58–0.74]): match BA and HP after PA pairing.
  - (0.29, 0.28 [0.20–0.36]), (0.24, 0.23 [0.13–0.32]) and (0.11, 0.33 [0.22–0.44]): match PA, BA and HP after EL
    pairing.
  - (0.19, 0.12 [0.02–0.23]): matches EL after PA pairing.
  - These assignments are mine, matched to the Fig. 7E/H bar values.
- Regression line ≈ 0.71 × overlap + 0.15.
- Legend: "Magnitude of depression correlates with extent of overlap in KC response patterns (p < 0.005, Pearson’s
  r = 0.90). ... (overlap calculated from data in Campbell et al., 2013)."
- The OCT–MCH overlap in the text is a different number from a different source: "(33 % of MCH-responding KCs and 30 %
  of OCT-responding KCs respond to both these odors)".

## 6. Backward-pairing control (Fig. 1G–J, n = 7)

**Text and legends**
- Fig. 1G: "Backward pairing protocol. Odor was delivered 0.5 s after the last pulse of light." Same four 1-ms pulses at
  2 Hz.
- The backward-paired odor was OCT: Fig. 1G puts the light before OCT. MCH was unpaired.
- Text: "We used the same number of light pulses as before, but instead started odor delivery 0.5 s after the last
  pulse of light. We observed no change in odor responses with this protocol (Figures 1H and 1J)."
- Fig. 1J: "Mean odor-evoked spike count. Backward pairing showed no effect (p > 0.05, repeated measures two-way
  ANOVA)."
- Numbers in the text: **Not reported.**
- Per-odor p values: **Not reported.**
- One of the seven recordings is cell-attached.

**Fig. 1J bars (fig., approx.).** Ticks 150/100/50/0 at y = 1364.7/1441.5/1518.2/1595.9 px, i.e. 1.541 px per spike.

| Odor | Pre | Post | Change (derived) |
|---|---|---|---|
| OCT (light first) | 94 (+12.5/−12.4) | 100.5 (+12.0/−11.1) | +7% |
| MCH | 83 (+14.9/−14.2) | 80 (+12.0/−12.4) | −4% |

**Individual flies (fig., approx.; lines cross, rough)**
- OCT: 137→147, 119→117, 103→93, 100→121, 86→93, 80→77, 34→58. Post/pre 0.90–1.69.
- MCH: 156→148, 93→77, 87→81, 78→55, 72→83, 70→67, 27→49. Post/pre 0.70–1.82.
- (derived) The spread in single flies is ±20–30% even without plasticity.

## 7. Kenyon cells before and after pairing (Fig. 2, Fig. S7)

**What the paper says** (no response values are given)
- Text: "After pairing odor presentation with PPL1-γ1pedc activation using our 1-s protocol, response magnitudes of
  individual cells decreased slightly for both CS+ and CS− (Figures 2C-2F). However the magnitude of the decrease was
  indistinguishable between the two odors. Moreover, we observed a similar decrease when we omitted photostimulation
  (Figures 2E-2F), indicating that these small reductions are unrelated to the pairing."
- Fig. 2E: "Red and green points indicate CS+ (OCT; n = 53 cells from 5 flies) and CS− (MCH; n = 49) respectively.
  Gray points are from control experiments where no light pulses were delivered (OCT and MCH; n = 32 from 2 flies).
  Error bar, median absolute deviation. Solid lines, linear regressions. Dashed line, unity. All three data set showed
  small but significant decrease after pairing (p < 0.05, paired t-test)."
- Fig. 2F: "There was no difference between any combination of the distributions of CS+ responses (red), CS− (green)
  and control (gray; Kolmogorov Smirnov test, p > 0.1)."
- Fig. 2H: "There was no significant difference between CS+ (red) and CS− (green; p = 0.58, unpaired t-test)." The
  Methods add that cosine distance and Pearson correlation gave "p > 0.5 in each case".
- Methods: "We observed small decreases in the response magnitudes over the course of the experiments (Figure 2E).
  These were clearly unrelated to pairing because we observed similar reductions without photostimulation. The small
  decrease is likely attributable to technical factors related to imaging, such as photobleaching and photodamage of the
  GCaMP6f."
- Methods details:
  - "82 ± 9 cells per fly, mean ± SD; n = 7".
  - Response = average ΔF/F from 0.5 to 4.5 s after odor onset.
  - "Four pre- and post-pairing trials (imaging duration, 21 s) were alternately recorded for each odor (OCT and MCH),
    with a typical inter-stimulus interval of 40 s."
  - Pan-KC driver R13F02-LexA, GCaMP6f.
- Percent change per odor, mean change, and the regression parameters: **Not reported.**

**From the figures (fig., approx.)**
- Fig. 2E calibration: x ticks 0/2/4/6 at x = 236.2/378.4/520.3/662.6 px; y ticks 0/2/4/6 at y = 1546.7/1388.7/1230.4/
  1072.6 px.
- Fig. 2E regression lines, in median ΔF/F:
  - CS+: post ≈ 0.76 × pre + 0.06.
  - CS−: post ≈ 0.78 × pre − 0.07.
  - No light: post ≈ 0.83 × pre + 0.05.
  - At pre = 2 they give post ≈ 1.59, 1.48 and 1.71 (derived from the fitted lines). That is roughly a 15–25% loss in
    all three groups, light or not.
- Fig. 2F histograms of change (post − pre ΔF/F; x ticks −1/0/1 at x = 1169.7/1302.9/1436.2 px; y ticks 0/10/20% at
  y = 1585.9/1388.4/1191.2 px):

  | Group | Peak | Range and tails |
  |---|---|---|
  | CS+ | ≈ −0.35, 24.7% of cells | most cells from ≈ −0.6 to +0.5; small bump ≈ 4% near +1.0 |
  | CS− | ≈ −0.38, 28.8% | ≈ 22.5% from −0.17 to +0.1; tail to ≈ −1.7 at ≈ 2% |
  | No light | ≈ −0.25, 24.7% | ≈ 4% near +0.65 |

- Fig. 2H medians of normalized distance (the open-circle-with-dot marker; y ticks 1.2/1.0/0.8/0.6/0.4 at
  y = 1846.1/1960.4/2073.0/2188.6/2303.0 px):
  - OCT ≈ 0.62, with the thick bar ≈ 0.41–1.03.
  - MCH ≈ 0.74, with the thick bar ≈ 0.46–1.00.
  - The legend doesn't say what the marker and bars mean; they look like a compact box plot (median and IQR).
- (derived, my inference) 30% of the 53 OCT responders and 33% of the 49 MCH responders both come to about 16 cells,
  which is consistent with the paper's 30%/33% overlap coming from this dataset; the paper doesn't say where it came
  from. With 16 shared cells the Jaccard index would be about 0.19. About 10–11 responders per fly out of about 82
  imaged is roughly 12–13%.

**Fig. S7, γ KC excitability** (n = 9; whole-cell; pairing = 15 pA × 1 s depolarization with the 4 light pulses)
- Values (fig., approx.):
  - Spike threshold potential: −11.0 ± 1.6 → −11.1 ± 1.8 mV.
  - Threshold current: 11.8 ± 0.5 → 12.0 ± 0.4 pA.
  - Spikes for 15 pA × 1 s: 18.9 ± 1.5 → 18.8 ± 1.4.
- Legend p values: "p > 0.9; n = 9", "p > 0.4", "p > 0.7".

## 8. For a pre-registered test

**What the fly data pin down** (OCT paired, MCH unpaired, MBON-γ1pedc, 4 light pulses, test about 2–6 min later)
- Spikes:
  - Primary experiment, Fig. 1F (n = 7): 27 ± 7.1%, with SD 18.8% and 95% CI 9.6–44.4% (derived).
  - Same protocol, other groups: 18% (TH-GAL4, n = 5), 30% (Fig. S4 at 10 min, n = 6), 38–41% (Fig. 4E, n = 6).
  - (derived) The n-weighted average of those four groups is ≈ 29.5%.
  - Reciprocal (MCH paired): 36–38% (Fig. S3, n = 6).
- Charge:
  - 19 ± 12% with QX-314 (Fig. 3D, n = 5, not significant).
  - 35 ± 4% with potassium internal (Fig. 4H, n = 6, p < 0.001).
  - (derived) Pooling the 11 cells: 27.6 ± 6.2% (SD 20.5), 95% CI 13.9–41.4%.
- Conditions with no plasticity:
  - Backward pairing: +7% and −4%. No driver: −1.5% and −7%. MB099C: −6% and +0.5%.
  - The γ2α′1 recording: −14% for OCT and +3% for MCH.
  - These give the size of change flies show when nothing is induced: within about ±7% for groups of 6–8, and up to
    about 14% in one case.
- The paired odor in the same experiments: spikes 80 ± 5.7% (95% CI 66–94%, derived), 76–86% in the other 4-pulse
  groups, and 62.5% with a single pulse. Charge 90 ± 3.7% (Fig. 3) and 74 ± 3% (Fig. 4H, derived).
- (derived) The gap between paired and unpaired decreases runs from 38 to 70 percentage points across the groups.

**Suggested bands, with reasons**

1. **Unpaired-odor spikes, OCT paired: fly-like if the MCH decrease is 10–45% (post/pre 0.55–0.90).**
   - This covers the 95% CI of Fig. 1F (10–44%) and every same-protocol group mean (18–41%).
   - Below 10%, the result can't be told apart from the no-plasticity controls, yet flies show a significant CS− drop
     (p < 0.01 in Figs. 1F, 4E, 5H and S3D).
   - Above 45%, the result exceeds every fly group mean and closes most of the gap to the paired odor.
   - A tighter "good match" band is 20–34%, i.e. ±1 SEM around 27%.
2. **Unpaired-odor charge, OCT paired: fly-like if the MCH decrease is 10–45% (post/pre 0.55–0.90).**
   - The pooled 95% CI is 14–41%, and Fig. 4H alone gives 25–45%.
   - The upper bound is the same as for spikes, since charge and spikes fell by similar amounts in the same cells (35%
     vs 38% in Fig. 4).
   - A model run in the QX-314 condition (no MBON spikes during pairing) could justify a lenient lower bound of 0%,
     because Fig. 3D's CI (−15% to +53%) includes zero. Since the paper finds that MBON spikes don't matter
     ("MBON spikes do not contribute to this form of plasticity"), I'd keep 10% as the lower bound.
   - Charge should be measured the same way: voltage clamp, integrated over 0–1.4 s from odor onset.
3. **The paired odor and the gap: paired decrease at least 65%, and at least 30 percentage points more than the
   unpaired one.**
   - Both are met by every 4-pulse fly group. The smallest gap is 38 points.
   - This keeps "the effect of pairing was significantly different between odors" as part of the test.
4. **Reciprocal direction (MCH paired): fly-like if the OCT decrease is 15–50%.**
   - The only data are spikes in Fig. S3 (n = 6): −38% in the means and a rough per-fly 95% CI of 20–51% (derived).
   - The paper calls it "an equivalent effect". A model far more specific in one direction than the other (say 30% one
     way, 5% the other) would not be fly-like for the MCH-paired direction.
   - No charge data exist for this direction.
5. **Backward pairing: fly-like if both odors' mean change is within ±15%.**
   - Flies show +7% and −4% with "no effect (p > 0.05)".
   - ±15% also covers the largest change in any no-plasticity group (−14%).

**Things to fix before running**
- **Compare the right thing.**
  - A single run of one connectome is one "fly". The across-fly prediction interval is far too wide to test against:
    −22% to +77% for CS− spikes (derived from SD 18.8%, n = 7).
  - So either treat the model as the mean fly and test it against the CI of the group mean (the bands above), or run
    5–7 instances (KC noise seeds, trial noise) and compare means.
  - (derived) With fly-sized n, a model mean has to sit about 17 points from 27% to differ at p ≈ 0.1 (SEM of the
    difference ≈ 10 points), so wide bands are the honest choice.
- **Fix the metric in advance.** Use the per-animal mean of percent decrease, which is what the paper reports for
  27 ± 7.1%, 20 ± 6.3%, 80 ± 5.7% and 90 ± 3.7%. The ratio of group means is about 2 points smaller here (Fig. 1F CS−:
  24.5%).
- **Match the protocol.**
  - 1-s odors at 25-s intervals, alternated; about 5 pre trials.
  - The pairing 1 min after the last pre trial, then the CS− alone 1 min after pairing.
  - Post trials from about 2 to 6 min.
  - Spikes counted 0–1.4 s after odor onset with "Spontaneous spiking rates ... subtracted". The window used for the
    spontaneous rate is **Not reported**.
- **Time.** The CS− depression fades by 30–40 min (Fig. S4) while the CS+ depression stays. A model without recovery
  should be compared with the early window (Fig. 1F), not with Fig. S4 at 30–40 min.
- **KCs.** Flies show no pairing-specific change in KC responses (Fig. 2) or excitability (Fig. S7). A model where
  pairing changes KC responses, rather than KC→MBON weights, would not be fly-like, whatever its MBON numbers.
- **Optional overlap check.** Across eight odor pairs in flies (Fig. 7I, single-pulse protocol, 1% odors), depression
  rises with KC overlap: about 0.71 × overlap + 0.15. Low-overlap odors (0.11–0.29) lost 12–33% and high-overlap odors
  (0.45–0.63) lost 66–69%. Reporting the model's own OCT/MCH KC overlap next to its CS− depression would show whether
  the specificity comes from the overlap, as in flies.

**Not reported anywhere in the paper**
- Absolute charges and per-cell values; these come only from the figures.
- An odor × pairing interaction p for Fig. 3.
- Per-odor p values for backward pairing.
- Any voltage-clamp or charge data with MCH paired.
- Numbers for the Kenyon cell responses.
- The window used for the spontaneous rate.
