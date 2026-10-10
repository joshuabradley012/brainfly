# ORN→PN short-term depression: protocols, train data, recovery and resting strength

Compiled 2026-10-10 from full texts, figure legends and supplements:
- Kazama & Wilson 2008 (KW08): the PMC author manuscript, the published PDF (Kazama-lab copy), the Elsevier `mmc1`
  supplement, and Elsevier's high-resolution figures (`gr4/8/9_lrg.jpg`).
- Kazama & Wilson 2009 (KW09): PMC XML and the Nature supplement.
- Nagel, Hong & Wilson 2015 (N15): PMC XML, the Nature supplement and the nature.com figures.
- Nagel & Wilson 2016 (NW16): PMC HTML.
- Olsen & Wilson 2008: PMC HTML and the Nature supplement.
- Gouwens & Wilson 2009: PMC HTML.

Purpose: settle the apparent conflict between KW08/KW09 and N15 on depression at the ORN→PN synapse. Then decide what
resting strength brainfly's spontaneously firing ORNs (6-19 Hz) should leave at their PN synapses.

**Conventions** (as in the other notes)
- Text in quotation marks is verbatim.
- "(fig., approx.)" means read off a published figure with a pixel grid calibrated on the axis ticks or labels. Expect
  ±0.02-0.03 of full scale; trace amplitudes carry about ±0.02 extra from line width.
- "(derived)" means my arithmetic, shown or reproducible from the stated numbers.
- "Not reported" means I searched the text, the legends and the supplement and did not find it.
- f is the fraction of synaptic strength *left* after each spike. τ is the recovery time constant toward 1. "Rested" means
  the amplitude at 0.033 Hz (one stimulus per 30 s).

**Access limits**
- KW08 has an erratum (Neuron 59:183, doi:10.1016/j.neuron.2008.06.015). Elsevier and Cell returned 403, so I could not see
  what it corrects.
- The published KW08 PDF has the same 7-Hz sentence and the same DM4 numbers as the manuscript.

Related notes: [pn_ln_dynamics.md](pn_ln_dynamics.md) (PN intrinsic limits, the uEPSP time course) and
[presynaptic_inhibition.md](presynaptic_inhibition.md) (GABA magnitudes, N15's I(t)).

## Summary

1. **Protocols.** Every train measurement comes from a reduced preparation. The stimulated ORN axons were cut off from
   their somata just before recording, so they were silent and their synapses were rested before each trial.
   - KW08 and KW09 severed the antennal nerves at the first antennal segment and minimally stimulated one axon. Rested
     uEPSCs were collected every 30 s. Every KW08 train trial began with 4 s at 7 Hz.
   - N15 and NW16 removed the third antennal segments and used multi-fibre stimulation (7.5-150 µA, first EPSC < 80 pA).
   - GABA receptors were not blocked in any train experiment. Blocking them "had little effect" on 10-Hz depression (N15
     Supp. Fig. 1, n = 4).
   - All recordings were in voltage clamp with a Cs internal. Saline: 1.5 mM Ca, 4 mM Mg.
   - **Recording temperature is not reported in any of the four papers.** Flies were reared at 25 °C.
2. **The "≈0.6 at 7 Hz" figure is text-only.** KW08's Discussion says 7-Hz responses "depress by about 40%". Its figures
   show more depression:
   - Two 7-Hz example traces plateau at **0.46 and 0.50** of the first uEPSC (Fig. 8D/E; VM2; low-pass-filtered
     averages).
   - The fit in Fig. S8D extrapolates to **0.43** at zero pause.
   - Pooled single-trial ratios cluster at **0.15-0.35** (Fig. 8G).

   N15's single pool (f 0.78, τ 893 ms) predicts 0.44 at 7 Hz. It reproduces the mean of the two example traces (RMS
   0.06 over 28 pulses, derived). **There is no steady-state conflict at 7 Hz.**
3. **The real conflict is the recovery time.**
   - After 4 s at 7 Hz, recovery is single-exponential with **τ = 7.5 s** (KW08 Fig. S8D). Amplitudes are ≈0.46, 0.56,
     0.50, 0.69, 0.91 and 1.00 after pauses of 0.5, 1, 2, 5, 10 and 30 s (fig., approx.).
   - N15's pool predicts 0.63, 0.79, 0.93, 1.00 and 1.00 at the first five pauses (derived).
   - After 50-200 Hz trains, 7-Hz probes return to their plateau with an apparent τ ≈ 0.4 s (Fig. S8B, fig., approx.).
   - N15's τ of 0.9-1.0 s was fitted to the depression *during* 20-pulse 10-Hz trains. It was never a direct recovery
     measurement.
4. **DM4 depresses more at low rates.**
   - Minimal-stimulation 4-Hz trains fall to 0.73, 0.57, 0.48 and 0.46, and reach 0.28 by 3 s (KW09 Supp. Fig. 2a,
     n = 3, fig., approx.). KW09 fitted **α = 0.72, τ = 2.4 s** to these data.
   - N15's pool predicts a 4-Hz floor of 0.60. KW09's pool predicts 0.13 by the 20th pulse of a 10-Hz train, where N15
     measured 0.34 (derived).
   - **No single pool fits both labs' data.**
5. **Resting strength in an intact fly has one direct estimate.**
   - DM4 spontaneous EPSCs with the antennae intact (10.6 ± 1.2 pA) match uEPSCs evoked at 4 Hz (10.7 ± 2.6 pA, n = 3).
   - Rested DM4 uEPSCs are ≈41 pA (Fig. 4A, fig., approx.). So **the resting synapse transmits ≈0.26 of its rested
     strength** at DM4's 3.4-4 Hz (derived).
   - KW09's spontaneous-EPSC cloud agrees (Fig. 5a).
   - KW08's "homeostatic" matching concerns rested (0.033 Hz) uEPSPs. It says nothing about resting strength in vivo.
6. **Odor-rate trains.** After 4 s at 7 Hz, relative to the first test EPSC (KW08 Fig. 8F, n = 6, fig., approx.):

   | test train | result |
   |---|---|
   | 15 Hz | 0.66 at 469 ms |
   | 20 Hz | 0.36 at 450 ms |
   | 50 Hz | 0.03 at 100 ms, then ≈0 |

   - Relative to rested, these are ≈0.30, ≈0.17 and ≈0 (derived).
   - The 50-Hz zero may include axon-recruitment failures (KW08 Supp.).
   - N15's multi-fibre 50-Hz trains keep late ripples ≈0.2 of the first EPSC (Fig. 2e, fig., approx.).
   - The paired-pulse ratio at ≈25 ms is ≈0.55-0.6 (Olsen & Wilson 2008, fig., approx.). That is deeper than any 10-Hz
     fit predicts (≈0.78).
7. **N15's "slow component" numbers come in two kinds.**
   - Measured, on curare-resistant EPSCs: f = 0.91, τ = 629 ms.
   - Fitted model parameters: r = 0.0073 spike⁻¹, τA = 33,247 ms, τg = 80 ms. These were fitted to disinhibited odor
     responses, not measured at the synapse.
   - KW08 attributed the slow part of evoked EPSCs to lateral input. N15 attributes it to a second nicotinic component
     present in single spontaneous EPSCs.
8. **N15's model at rest (Fig. 7c, fig., approx.).**
   - The depression variable A is 0.67 (fast) and 0.69 (slow) with presynaptic inhibition, and 0.34 and 0.33 without.
   - These imply an ORN rate of ≈8.5 spikes/s and a resting I ≈ 4 (derived).
   - The model's per-spike efficacy with inhibition, A/I ≈ 0.17 (derived), lies below the DM4 measurement (0.26); its
     A without inhibition (0.34) lies above it.
9. **None of the papers reconciles the parameter sets.** N15 itself says its single-timescale model's assumptions "are
   incorrect" for odor responses.
10. **Recommendation: two pools in parallel**, each half the synapse (derived fit, §7).
    - Slow pool: f 0.83 (17% released per spike), τ 7.5 s. Fast pool: f 0.67 (33% per spike), τ 0.3 s.
    - It halves the joint misfit of the best single pool (cost 0.014 against 0.029) and cuts N15's published pool's
      (0.037) to about a third. It reproduces the S8D recovery, the flat plateau in S8B, and the flat 1-5 s plateau of a
      10-Hz train.
    - Predicted resting strength for Poisson firing: **0.37 at 6 Hz, 0.32 at 8 Hz, 0.19 at 19 Hz** (regular firing:
      0.40, 0.35, 0.20).
    - DM4 and minimal-stimulation data point lower: 0.26 measured in vivo against 0.47 predicted at 3.44 Hz.
    - **brainfly's current ≈0.4 at rest is at the upper end of the literature. Nothing supports raising it to 0.6.**

---

## 1. Kazama & Wilson 2008, Neuron 58:401 ([PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/))

### 1.1 Protocol
- **Cut nerve; one fibre; rested baseline.**
  - "Immediately prior to recording, the antennal nerves were gently severed with fine forceps where they enter the first
    antennal segment."
  - "Except for the recordings in Figure 1, a minimal stimulation protocol was used throughout the study to stimulate
    only one ORN axon that was directly presynaptic to the recorded PN"
  - Pulses: "a brief pulse (50 μs) of current".
  - Supplement: "Once a stable recording was achieved, the nerve was stimulated every 30 s to collect 20–100 (average 35)
    uEPSCs."
  - The palps were left intact except in the experiments that state otherwise, so palp ORNs still fired spontaneously.
- **Clamp and solutions.**
  - "In voltage clamp recordings, the command potential was −65 mV. Signals were low-pass filtered at 1 kHz and digitized
    at 5 kHz. Voltages are uncorrected for liquid junction potential."
  - Internal: "140 cesium aspartate, 10 HEPES, 4 MgATP, 0.5 Na3GTP, 1 EGTA, 1 KCl, 13 biocytin hydrazide, and 10 QX-314".
    For current clamp, "QX-314 was removed and cesium was replaced with an equal concentration of potassium."
  - External: 103 NaCl, 3 KCl, 5 TES, 8 trehalose, 10 glucose, 26 NaHCO3, 1 NaH2PO4, 1.5 CaCl2, 4 MgCl2 (mM).
  - Temperature: not reported.
- **GABA.** No antagonists were used in the train experiments.
- **Train design.** "These ORNs fire spontaneously at about 7 spikes/s (R.I.W., unpublished observations). To mimic this,
  we began every trial with a long train of pulses at this frequency (Figures 8D-8G), which itself produced some synaptic
  depression. This was immediately followed by a second train mimicking a variable level of odor-evoked ORN input."
  - All train data are from VM2 PNs.
  - The inter-trial interval for trains is not reported. The 30-s point in S8D sits at exactly 1.00, which suggests
    ≥30 s (my inference).

### 1.2 Rested unitary synapse
- "minimal stimulation of the antennal nerve at 0.033 Hz evoked an average uEPSC measuring 29.0 ± 2.6 pA (n = 45) in
  antennal PNs" and "Averaged across PNs, uEPSP amplitude was 6.19 ± 0.45 mV (n = 23)."
  - Discussion: "at low stimulus frequencies (0.033 Hz), a single spike in one ORN axon is sufficient to depolarize a PN by
    about 6 mV."
- Quantal parameters, from multiple-probability fluctuation analysis in DL5 and DM4: "N = 51.4 ± 7.8, q = 1.05 ± 0.11 pA,
  and p = 0.79 ± 0.02". The Discussion rounds p to "near 0.75". The single-p method gives p uniform across glomeruli
  (Fig. 7C).
- By glomerulus (fig., approx.):

  | glomerulus | uEPSC (Fig. 4A) | uEPSP (Fig. 4B) |
  |---|---|---|
  | DM6 | 13.3 pA | 5.5 mV |
  | VM2 | 12.9 pA | 5.4 mV |
  | DL5 | 37.0 pA | 7.0 mV |
  | DM4 | 41.4 pA | 6.9 mV |

  - n = 9, 10, 9 and 10 for the uEPSCs and 7, 5, 5 and 6 for the uEPSPs.
  - The four uEPSPs average 6.18 mV, matching the text's 6.19 (derived).
  - N·p·q = 51.4 × 0.79 × 1.05 = 42.6 pA, which matches the DL5 and DM4 values (derived).
- **Slow component.** "the slow component was relatively small, on average only about 1 % as large as the fast component
  at the time when the fast component peaks". KW08 concluded it "reflects lateral input to a PN".

### 1.3 Seven-hertz trains from rest (Fig. 8D, 8E, 8G)
- Fig. 8D legend: "Traces are averaged over several trials and low-pass filtered to remove stimulus artifacts. All data
  in (D)–(G) are recordings from PNs in glomerulus VM2."
- Digitized EPSC amplitudes, as trough minus the preceding baseline (fig., approx.; 2 pA bar = 50 px):

  | trace | first uEPSC (filtered) | pulses 2-8 (fraction of first) | pulses 10-28 |
  |---|---|---|---|
  | 8D | 6.96 pA | 0.77, 0.63, 0.57, 0.58, 0.50, 0.48, 0.49 | mean 0.46 (0.39-0.56) |
  | 8E | 7.52 pA | 0.75, 0.73, 0.62, 0.46, 0.60, 0.43, 0.58 | mean 0.50 (0.37-0.69) |

  - The plateau is reached within ≈1 s (6-8 pulses) and stays flat to 4 s.
  - Measuring to the line centre lowers the ratios by ≈0.01-0.02.
- **Fig. 8G**, axis "ratio of mean uEPSC amplitude (x th / 1 st)" (fig., approx.).
  - Roughly 150-250 dots, many overlapping, form a dense cluster at x ≈ 0.12-0.40.
  - The median of dot area is 0.29 (IQR 0.21-0.36). Overlap in the cluster biases this upward.
  - About 10% of the dot area lies at x > 0.45; these are presumably the first pulses of each train. One point sits at
    (1, 1).
  - n is not stated.
  - So unfiltered, pooled single-trial measurements show *deeper* 7-Hz depression (≈0.25) than the filtered example
    traces (≈0.46-0.50).
- Legend: "Repetitive stimulation (7 Hz) causes a decrease in inverse of the square of the coefficient of variation
  (1/CV^2) which is correlated with the decrease in uEPSC amplitude, implying a presynaptic locus for this depression.
  Gray line is a linear fit (Pearson's r = 0.79, p < 10^−4)."
  - Text: "This may, of course, reflect presynaptic inhibition in addition to presynaptic vesicle depletion. At higher
    stimulus frequencies, postsynaptic factors (such as receptor saturation or desensitization) may also play a role."
- **Discussion (the source of "0.6").** "At frequencies mimicking the basal firing rate of a typical ORN (7 Hz), synaptic
  responses depress by about 40% but remain relatively strong."
  - Taken literally that is 0.60 remaining. None of the 7-Hz panels shows 0.60 after the first 3-4 pulses.

### 1.4 Test trains after 4 s at 7 Hz (Fig. 8F; Fig. 9)
- Fig. 8F: "Change in uEPSC amplitude during the 500-ms stimulation period mimicking odor-evoked input. Strong inputs
  rapidly depress ORN-PN synapses (n = 6 cells)."
- Amplitudes are normalized to the first test pulse (fig., approx.; ticks 100/50/0 % and 0/250/500 ms):

  | train | values (time: % of first test EPSC) |
  |---|---|
  | 15 Hz | 67 ms 90.4 · 134 ms 86.1 · 201 ms 77.0 · 268 ms 74.1 · 335 ms 72.0 · 402 ms 69.4 · 469 ms 66.1 |
  | 20 Hz | 50 ms 86.1 · 100 ms 78.2 · 150 ms 70.1 · 200 ms 46.9 · 250 ms 51.9 · 300 ms 44.6 · 350 ms 45.6 · 400 ms 42.0 · 450 ms 35.6 |
  | 50 Hz | 20 ms 77.4 · 40 ms 46.2 · 60 ms 30.0 · 80 ms 16.5 · 100 ms 2.9 · then −5.8 to +8.4, mean 0.6 over 120-480 ms (19 points) |

  - Relative to rested, multiply by the 7-Hz level after 4 s (0.43-0.50):
    - 15 Hz at 469 ms: 0.28-0.33.
    - 20 Hz at 450 ms: 0.15-0.18.
    - 50 Hz: ≈0.00-0.04 (derived).
    - With Fig. 8G's ≈0.25 level instead, these become ≈0.17, ≈0.09 and ≈0.
- KW08 on high rates: "We observed strong depression at all frequencies above about 50 spikes/s." The supplement
  cautions: "During repetitive nerve stimulation at high-frequency (50–200 Hz), it is difficult to discriminate between
  successful and unsuccessful axon recruitment, especially toward the end of the stimulation period. However, we
  confirmed that axon recruitment failure is not occurring for every stimulation during the train".
- **Fig. 9B-D** (n = 4): "Every experiment was preceded by antennal nerve stimulation mimicking spontaneous ORN firing
  rates (7 Hz, 4 s)."
  - Charge transfer, normalized to 100 Hz (fig., approx.; read against the axis labels, since the axes have no ticks):

    | rate (Hz) | 10 | 15 | 20 | 30 | 50 | 100 | 200 |
    |---|---|---|---|---|---|---|---|
    | first 100 ms (%) | 14 | 23 | 21 | 34 | 66 | 100 | 98 |
    | first 500 ms (%) | 27 | 43 | 59 | 75 | 107 | 100 | 87 |

  - Every depletion model I tried overpredicts the low-rate charge relative to 100 Hz (e.g. 48-61% against 27% at 10 Hz
    over 500 ms, derived).
  - At 50-200 Hz the traces are dominated by a large, slow, summating inward current (Fig. 8E, 9B). These charge data
    therefore don't test depletion cleanly, and I did not fit them.

### 1.5 Recovery (Fig. S8; Elsevier mmc1 p. 14)
- **Recovery after high-frequency trains.** "(B) Recovery rate of uEPSC amplitude following trains of antennal nerve
  stimulation delivered at 50–200 Hz. Gray curve is an exponential fit. The gradual recovery of uEPSC amplitudes following
  the high-frequency train demonstrates that axon recruitment failure (which would be all-or-none) cannot explain the
  depression in the postsynaptic response to the train."
  - Probes come at ≈7 Hz (arrows in S8A, 15 points over 2 s). Whether the train was preceded by 7-Hz conditioning is not
    stated.
  - Points in pA, on filtered traces (fig., approx.):

    | t after train (s) | 0 | 0.14 | 0.29 | 0.43 | 0.57 | 0.71 | 0.86 | 1.0 | 1.14 | 1.29 | 1.43 | 1.57 | 1.71 | 1.86 | 2.0 |
    |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
    | uEPSC (pA) | 0.24 | 0.48 | 0.76 | 1.91 | 2.41 | 2.16 | 2.40 | 2.49 | 2.36 | 2.68 | 2.20 | 2.77 | 2.50 | 2.46 | 2.64 |

  - The drawn fit is ≈2.62·(1 − e^(−t/0.40 s)) (fig., approx.; τ is not stated). After ≈0.5 s the plateau is flat
    (last/fifth probe = 1.10).
  - The plateau is the 7-Hz-probe level, not the rested amplitude, so this panel cannot give the depth.
- **Recovery after 7-Hz conditioning.** "(C) Unitary EPSCs evoked by antennal nerve stimulation at 7 Hz before and after
  a pause to examine the speed of recovery from synaptic depression caused by spontaneous ORN firing rates. (D) Recovery
  rate of uEPSC amplitude is slow (time constant = 7.5 s). Gray curve is an exponential fit. This suggests that the
  recovery of uEPSC amplitude likely does not account for odor-offset PN excitation in response to odors that suppress
  activity in the direct ORN inputs to those PNs".
  - The y-axis, "recovery ratio", is not defined. The 30-s point is 1.00 without an error bar.
  - Points (fig., approx.):

    | pause (s) | 0.5 | 1 | 2 | 5 | 10 | 30 |
    |---|---|---|---|---|---|---|
    | recovery ratio | 0.46 | 0.56 | 0.50 | 0.69 | 0.91 | 1.00 |

  - The drawn fit is ≈1.03 − 0.60·e^(−t/7.5 s), so 0.43 at t = 0 (fig., approx.).
  - **There is no fast phase.** The 0.5-2 s points lie on the 7.5-s curve.
  - n is not stated for S8.

### 1.6 Resting strength in vivo (the DM4 comparison)
- **The comparison.** "To test this prediction, we recorded from PNs in glomerulus DM4 and stimulated the antennal nerve
  with a minimal stimulus intensity at frequencies approximating the spontaneous firing rates of DM4 ORNs (4 spikes/s;
  R.I.W., unpublished observations). The amplitude of evoked uEPSCs at this stimulus frequency was similar to the
  amplitude of spontaneous EPSCs we recorded in DM4 PNs with antennae intact (10.7 ± 2.6 pA vs 10.6 ± 1.2 pA, n = 3,
  Figure 2C)."
  - "Most or all of these spontaneous EPSCs must originate from ORN-PN synapses because they are completely absent when
    direct ORN input to a glomerulus is removed while keeping the lateral inputs intact".
- **Arithmetic** (derived; different cells for numerator and denominator): 10.6/41.4 = **0.26**, and 10.7/41.4 = 0.26.
  - KW09's 4-Hz train (Supp. Fig. 2a, also n = 3 DM4 cells, possibly the same ones) reaches 0.28 at 3 s, i.e.
    0.28 × 41.4 = 11.6 pA.
- **What the homeostasis results do and don't show.** KW08's size matching uses rested uEPSPs: "we have found that PNs of
  different sizes have matched uEPSPs, but nevertheless these PNs show very different levels of total spontaneous activity
  (R.I.W., unpublished observations)… If size matching in PNs does reflect homeostatic regulation, then the set-point for
  this system must be defined in terms of uEPSPs, not total postsynaptic spike rates."
  - Nothing in the paper measures matching of the *depressed* resting strength.

### 1.7 Mechanism statements
- "Many mechanisms in addition to vesicular depletion are likely to contribute to this depression (presynaptic
  inhibition, for example)."
- Postsynaptic receptor saturation by a single spike was excluded: the paired-pulse ratio at 30 ms is unchanged in
  vesamicol, "p > 0.28, paired t-test, n = 5 cells" (Fig. S5).

## 2. Kazama & Wilson 2009, Nat Neurosci 12:1136 ([PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/))

"Origins of correlated activity in an olfactory circuit." **This is the source of f = 0.72 and τ = 2.4 s.**

- **Model and fit.** "After the arrival of each action potential, A(t) decreased to a fraction α of the previous value
  (αA(t)) and recovered exponentially with a time constant τ". "To characterize the dynamics of ORN-PN synapses, the
  antennal nerve was stimulated with a suction electrode at a constant frequency mimicking the mean spontaneous firing
  rate of DM4 ORNs (Supplementary Fig. 2). The parameters α = 0.72 and τ = 2.4 s were obtained from a least-squares
  regression using these data."
- **Data.** Supp. Fig. 2a legend: "A single ORN axon directly presynaptic to the recorded DM4 PN was stimulated using a
  minimal stimulation protocol (Kazama and Wilson, 2008). The unitary EPSC amplitude depressed smoothly and rapidly during
  4 Hz stimulation (n = 3, error bars are s.e.m.)."
  - Values, as % of initial (fig., approx.):

    | t (s) | 0 | 0.25 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 1.75 | 2.0 | 2.25 | 2.5 | 2.75 | 3.0 |
    |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
    | % initial | 100 | 72.7 | 56.5 | 48.3 | 46.2 | 36.2 | 39.7 | 35.1 | 38.3 | 33.9 | 31.5 | 30.0 | 27.7 |

  - The amplitude is still declining slowly at 3 s.
  - My re-fit check: α 0.72, τ 2.4 s gives RMS 0.037 against these points, with a 4-Hz steady state of
    (1 − e^(−0.25/2.4))/(1 − 0.72·e^(−0.25/2.4)) = 0.0989/0.3512 = 0.282 (derived).
- **Rested versus 4 Hz.** Fig. 5b: "When ORNs are stimulated with a long inter-pulse interval (30 s), EPSCs are
  consistently large (top). A short inter-pulse interval (0.25 s) produces short-term depression (bottom)."
- **In vivo amplitudes.** Fig. 5a is a contralateral DM4 pair with one antenna removed. The spontaneous EPSC amplitudes
  form a cloud mostly at ≈3-20 pA, with a tail to ≈60 pA (fig., approx.).
  - The undepressed model (Fig. 5f) clusters near 40 pA. The depressed one with recorded DM4 spike trains (Fig. 5e)
    clusters near ≈15 pA (fig., approx.).
  - Model inputs: "N = 51, p = 0.79, and q = 1.05 pA", with N drawn per fibre from a Gaussian with "mean 51 and standard
    deviation 11".
- **Spontaneous rate.** "the mean firing rate of DM4 ORNs (3.44 ± 0.16 Hz, n = 11)". The ISI histogram peaks at ≈40-50 ms
  with a long tail (Fig. 5c), so firing is irregular.
- **Protocol.** Voltage clamp in Cs aspartate with 10 QX-314 at −60 or −65 mV, filtered at 1 kHz. "Voltages were
  uncorrected for liquid junction potential of 13 mV."
  - Temperature, GABA blockers (in the train experiment) and the inter-trial interval: not reported.
- KW09 does not compare its τ with KW08's 7.5 s.

## 3. Nagel, Hong & Wilson 2015, Nat Neurosci 18:56 ([PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/))

### 3.1 Protocol
- **Preparation and stimulation.** "The third segments of both antennae were removed with fine forceps just prior to
  opening the head capsule. The antennal nerve ipsilateral to the recorded PN was drawn into a large-diameter saline-filled
  pipette and stimulated with 50 μs pulses … in constant current mode. The stimulus amplitude was adjusted for each
  experiment to produce a reliable EPSC waveform with minimal unclamped spiking (7.5–150 μA). Empirically, we found that
  recordings with initial EPSCs larger than 80 pA tended to produce unclamped spikes. We therefore analyzed only recordings
  in which the initial EPSC amplitude was less than 80 pA."
  - Recordings were pooled from DM6 and VM2 PNs.
- **Multi-fibre.** The example first EPSC in Fig. 1b is ≈43 pA (fig., approx.; 20 pA bar). The rested unitary EPSC in
  DM6/VM2 is ≈13 pA, so this is several fibres.
- **Clamp.** Voltage clamp with "140 mM CsOH in place of KOH" (140 aspartic acid, 10 HEPES, 1 EGTA, 1 KCl, 4 MgATP,
  0.5 Na3GTP), plus "5 mM QX-314" in a subset. Filtered at 2 kHz and digitized at 10 kHz.
  - Holding potential for the nerve-evoked EPSCs: not reported. −60 mV is given only for odor-evoked currents.
- Same saline as KW08. Temperature and the inter-trial interval: not reported. Fig. 1b is the "average of 7 trials";
  Supp. Fig. 1 used "2-5 trials per PN".
- **GABA.** Not blocked for Figs. 1-2. Supp. Fig. 1: "ORN axons in the antennal nerve were stimulated with a train of 20
  stimuli at 10 Hz (as in Figure 1b,c)… both before and after blocking synaptic inhibition (with bath application of 25 –
  50 µM CGP54626 and 5 µM picrotoxin)… n = 4 PNs). Blocking inhibition had little effect on the dynamics of short-term
  depression at this presynaptic firing rate."
  - The example in Fig. 1b is in fact ≈50 stimuli (5 s) at 10 Hz (fig., counted). Fig. 1c plots the first 20.

### 3.2 Ten-hertz trains and fits
- Fig. 1c: "Mean normalized EPSC amplitudes during a 10 Hz train (±s.e.m., n=19 PNs from 19 flies in glomerulus DM6 or
  VM2). Line is a fit of the simple synaptic depression model (Equation 1, see Methods; f = 0.78 and τ = 893 ms)."
- Equation 1 (Δt = 1 ms): "if s(t)=1, A(t+Δt)=f∗s(t)∗A(t); if s(t)=0, A(t+Δt)=A(t)+(1-A(t))Δt/τ".
- Fig. 1c points, stimuli 1-20 (fig., approx.):

  | stimulus | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | normalized | 1.00 | 0.82 | 0.64 | 0.53 | 0.51 | 0.44 | 0.44 | 0.41 | 0.41 | 0.38 | 0.36 | 0.34 | 0.37 | 0.34 | 0.38 | 0.35 | 0.36 | 0.30 | 0.33 | 0.34 |

  - Refitting these points gives f 0.775, τ 0.891 s, which validates the digitization (derived).
- The Fig. 1b example (DM6) holds a flat plateau: mean 0.36 over stimuli 11-20, 0.37 over 21-30, 0.40 over 31-40 and
  0.36 over 41-50 (fig., approx.). There is no further depression between 1 and 5 s at 10 Hz.
- **Two components** (Fig. 2): "For the IMI-resistant component, these parameters were f = 0.77, and τ = 1006 ms, whereas
  for the curare-resistant component, these parameters were f = 0.91, τ = 629 ms, indicating a much slower rate of
  depression."
  - Fig. 2 n: control "mean of 13 PNs"; curare 5-10 µM "7 PNs"; IMI 50-100 nM "n=6 PNs".
  - N15 reads the components as "two types of nicotinic receptor with distinct kinetics. Alternatively, the two components
    might represent different states of the same receptor."
  - Single spontaneous EPSCs show both components: "Each EPSC arises from a single ORN spike, and so any dynamics present
    in these EPSCs must arise from unitary ORN-to-PN connections." Methods add: "Lateral excitation can contribute to the
    slow component of EPSCs evoked by electrical stimulation of ORN axons".
- **50-Hz trains** (Fig. 2e, from rest). In control, late ripples (≈0.5-0.7 s into the train) are ≈0.2-0.25 of the first
  EPSC, measured peak-to-trough (fig., approx.). The two drugs together blocked "70±12% of the evoked current during the
  50 Hz stimulus".

### 3.3 Model parameters (the source of 0.0073 and 33 s)
- **Fast component.** "r = 0.23 spike^−1, τ_A = 1006 ms, k = 20 nS/spike, and τ_g = 9.3 ms." "The values for r and τ_A
  were taken from the fits of EPSC amplitude as a function of stimulus number in IMI, while the parameter τ_g was taken
  from the faster exponential fit to the EPSC shape in IMI."
- **Slow component.** "Fitted parameters for the slow component were r = 0.0073 spike^−1, τ_A = 33247 ms, k = 1.8
  nS/spike, and τ_g = 80 ms."
  - These were fitted "in order to minimize the difference between the predicted PN membrane potential in response to 55%
    density stimulus and the actual disinhibited response". They are **not synaptic measurements.**
  - N15's reason: "It is likely that curare incompletely blocks the fast component, so when we fit the slow component to
    the curare data, it depressed too quickly. We therefore subsequently fit the slow component to PN odor response data
    with inhibition blocked".
- **Equation 3** (rate input): dA/dt = −r·s(t)·A(t) + (1 − A(t))/τA. For a constant rate s it gives A = 1/(1 + r·τA·s).
- **Unitary strength.** "The maximum amplitude of this conductance (0.28 nS) was set such that the amplitude of a unitary
  EPSC prior to depression was ~13.5 pA and the amplitude of a unitary EPSP was ~7 mV". For the two-component model: "0.22
  nS (fast component) and 0.06 nS (slow component)".
- **Fig. 7c** ("Solid traces show this parameter with inhibition while dashed traces show this parameter without
  inhibition. Without inhibition, synapses are weaker both before and during the stimulus"). Resting A (fig., approx.):

  | component | with inhibition | without |
  |---|---|---|
  | fast | 0.67 | 0.34 |
  | slow | 0.69 | 0.33 |

  - Without inhibition, Eq. 3 gives the ORN rate: (1/0.338 − 1)/(0.23 × 1.006) = 8.5 spikes/s (derived). The slow
    component's parameters give the same.
  - With inhibition, s/I = (1/0.673 − 1)/0.2314 = 2.1, so I_rest ≈ 4.0 (derived).
  - I(t) divides the input rate, so the per-spike efficacy is A/I ≈ 0.17 with inhibition against 0.34 without (derived).
  - On I(t)'s scale: "The magnitude of I(t) that we computed in this manner provided a good qualitative fit to the data,
    so its scale was not adjusted."
- **What N15 says about its own single pool.** "This comparison makes clear that the assumptions of this simple
  depression model are incorrect. In particular, the model assumes that there is one timescale of synaptic dynamics, and
  that the parameters specifying synaptic dynamics (f and τ) are constant over time." Also: "As we would expect for a
  depressing synapse, this model predicted transient responses to long odor pulses (Fig. 1d). In contrast, real PNs
  produced more sustained responses".
- **Presynaptic inhibition.** "Presynaptic inhibition at ORN-to-PN synapses decreases both EPSC amplitude and the rate of
  synaptic depression in experimental data" (citing Olsen & Wilson 2008).
- N15 never discusses KW08's 7.5-s recovery, the "about 40%" sentence, or KW09's α and τ. It cites KW08 only for the
  existence of depression and for unitary EPSC/EPSP sizes.

## 4. Nagel & Wilson 2016, J Neurosci 36:4325 ([PMC4829653](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/))

- Fig. 6B legend: "EPSC amplitude versus stimulus number for LNs and PNs (mean ± SEM, n = 9 for LNs and 19 for PNs). PN
  data are reproduced from Nagel et al. (2015)… Values of f and τ are 0.75 and 1566 ms for LNs; 0.78 and 893 ms for PNs."
- Protocol as in N15: third antennal segments removed, multi-fibre stimulation at 10 Hz, initial EPSC < 80 pA, Cs
  internal. The number of stimuli in the LN trains is not stated in the text.
- "Notably, EPSCs measured in LNs showed more pronounced depression than those measured in PNs did."
- The PN numbers are not new data.

## 5. Other primary sources checked

- **Olsen & Wilson 2008, Nature 452:956** ([PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/); Supp.
  Fig. 7). The paired-pulse ratio is "defined as the the amplitude of EPSC2/EPSC1"; "Reducing presynaptic release
  probability decreases vesicular depletion".
  - Interval: not stated. It is ≈25 ms, measured off Supp. Fig. 7a (EPSC onsets 32.5 px apart against a 65-px 50-ms bar;
    fig., approx.).
  - Control PPRs (fig., approx.):

    | group | n | control PPRs |
    |---|---|---|
    | Cd²⁺ set | 5 | 0.42, 0.44, 0.60, 0.62, 0.96 |
    | other groups | — | ≈0.37-1.0 |
    | odor group | 7 | ≈0.38-0.86, mean ≈0.55 |

  - "GABA suppressed EPSC1 to 15 ± 2% of the control value, while odor suppressed EPSC1 to 46 ± 4%".
  - In this experiment the contralateral antenna and the palps were intact.
- **Gouwens & Wilson 2009** ([PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/)). "we estimate that the true
  resting potential of these neurons is approximately −55 to −60 mV when spontaneous synaptic input from ORNs is intact and
  approximately −65 mV when input from ORNs is removed."
  - This is the only other in vivo measure of resting ORN drive. It does not separate depression from rate.
- **Gaudry et al. 2013** ([PMC3590906](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/)). Ipsilateral sEPSCs are "39%
  larger" than contralateral ones (DM6). No train or depression data.
- **Kazama, Yaksi & Wilson 2011** ([PMC3119471](https://pmc.ncbi.nlm.nih.gov/articles/PMC3119471/)). Chronic ORN loss
  strengthens excitatory-LN coupling. No ORN→PN unitary depression data.
- **Not reported anywhere I looked**: train data at 1, 2 or 5 Hz, and any measurement of PN unitary EPSPs (rather than
  EPSCs) during trains.

## 6. What explains the discrepancies (my synthesis)

- **The data sets disagree by protocol more than by lab.**

  | data | method | depressed level |
  |---|---|---|
  | VM2/DM6, KW08 examples | filtered averages, single fibre | 0.46-0.50 at 7 Hz |
  | VM2/DM6, N15 | multi-fibre peaks, n = 19 | 0.34 at 10 Hz |
  | VM2, KW08 Fig. 8G | unfiltered single-trial ratios | ≈0.25 at 7 Hz |
  | DM4, KW09 / KW08 | single fibre | 0.28 at 4 Hz (and 0.26 in vivo) |

  Candidate causes, none tested by the authors:
  - Low-pass filtering of the example traces.
  - Space-clamp compression of N15's large (≤80 pA) first EPSCs, which would inflate later/first ratios.
  - N15's EPSC peaks include the less-depressing slow component.
  - Glomerular differences.
- **The recovery is the robust disagreement.** Train-shape fits (N15 0.9-1.0 s; KW09 2.4 s) compare against the one
  direct recovery measurement after tonic firing (7.5 s, KW08 S8D) and a fast probe-driven return after high-rate trains
  (≈0.4 s, S8B).
  - A single pool cannot do both. A train's decline sets f·e^(−d/τ) per pulse; its plateau then fixes τ near 0.7-1.1 s at
    7 Hz, which forbids a 7.5-s recovery afterwards (derived).
- **The very-short-interval depression (≈0.55-0.6 at 25 ms) and the near-zero 50-Hz increments** suggest a fast, high-p
  component that refills within ≈100 ms. That fits p ≈ 0.79 from fluctuation analysis while the 100-250 ms paired-pulse
  ratios are 0.73-0.82.
  - Some of the 50-Hz zero in KW08 may be axon-recruitment failure under minimal stimulation.

## 7. For the model

### 7.1 Fits to the digitized data (derived)
- **Data sets**:

  | code | source |
  |---|---|
  | D1 | KW09 4 Hz |
  | D2 | N15 Fig. 1c, 10 Hz |
  | D3 | KW08 7 Hz, mean of Fig. 8D and 8E |
  | D4 | KW08 S8D recovery |
  | F15, F20 | KW08 Fig. 8F 15 and 20 Hz after 4 s at 7 Hz |

  - The 50-Hz train was excluded because of the recruitment-failure caveat and the measurement on summating, filtered
    traces.
  - Each data set gets equal weight. Recovery is between spikes; f is applied at each spike.

- **Results**: RMS error per data set, and predicted resting strength (Poisson formula, §7.3). The two-pool model (M4,
  bold) is recommended.

  | model | parameters | D1 | D2 | D3 | D4 | F15 | F20 | rest 6 / 8 / 19 Hz |
  |---|---|---|---|---|---|---|---|---|
  | N15 single pool (published) | f 0.78, τ 0.893 s | 0.228 | 0.021 | 0.061 | 0.247 | 0.036 | 0.089 | 0.46 / 0.39 / 0.21 |
  | N15 fast (IMI) | f 0.77, τ 1.006 s | 0.192 | 0.035 | 0.088 | 0.228 | 0.047 | 0.078 | 0.42 / 0.35 / 0.19 |
  | KW09 (published) | f 0.72, τ 2.4 s | 0.037 | 0.190 | 0.275 | 0.134 | 0.101 | 0.054 | 0.20 / 0.16 / 0.07 |
  | best single pool on D2-D4, F15, F20 | f 0.836, τ 1.78 s | 0.173 | 0.055 | 0.124 | 0.158 | 0.012 | 0.120 | 0.36 / 0.30 / 0.15 |
  | M2: fast × slow, multiplied | 0.779 / 0.407 s × 0.968 / 7.5 s | 0.257 | 0.039 | 0.090 | 0.058 | 0.062 | 0.069 | 0.27 / 0.20 / 0.07 |
  | **M4: two pools, added** | **w 0.5; slow f 0.83, τ 7.5 s; fast f 0.67, τ 0.3 s** | 0.198 | 0.026 | 0.092 | 0.075 | 0.048 | 0.102 | **0.37 / 0.32 / 0.19** |

  - Joint cost on D2-D4, F15 and F20 (½Σ residual²/n per data set):

    | model | cost |
    |---|---|
    | N15 published | 0.037 |
    | best single pool | 0.029 |
    | M2 | 0.011 |
    | M4, free fit (w 0.517, 0.835/7.5 s, 0.674/0.289 s) | 0.014 |

    The rounded parameters fit as well as the free fit.
  - **M4 versus M2.** Both capture the slow recovery. M2 fails three checks that M4 passes (derived):

    | check | observed | M2 | M4 |
    |---|---|---|---|
    | S8B probe 15 / probe 5 | 1.10 | 1.59 | 1.08 |
    | 10-Hz pulse 50 / pulse 20 (N15 Fig. 1b) | ≈1.0 | 0.62 | 0.97 |
    | strength left after 0.5 s at 100 Hz, from 8-Hz rest | — | 0.010 | 0.05 |

    M2's slow factor keeps depleting at high rates, so its sustained odor transmission collapses.
  - A single pool with activity-dependent (residual-Ca-like) recovery was also tried and rejected. It flattens the
    rate-dependence and misses F20 (RMS 0.165) and F50.
  - **Remaining misfits of M4.**
    - DM4 is too shallow: 0.51 against 0.28 at 3 s of 4 Hz.
    - 20-50 Hz post-conditioning depression is underpredicted: 0.54 against 0.36 at 450 ms of 20 Hz.
    - The 25-ms paired-pulse ratio is 0.76, against ≈0.55-0.6 observed.

### 7.2 Recommended model (M4)
- **Equations.** For each ORN axon there are two state variables, a (slow pool) and b (fast pool), both starting at 1.
  - Between spikes: a ← 1 − (1 − a)·e^(−Δt/τA), and b ← 1 − (1 − b)·e^(−Δt/τB).
  - At a spike, transmitted strength = W_rested × [w·a + (1 − w)·b]. Then a ← fA·a and b ← fB·b.
- **Parameters**: w = 0.5, fA = 0.83, τA = 7.5 s (the KW08 S8D value, held fixed), fB = 0.67, τB = 0.3 s.
- **Rested weight.** W_rested is the 0.033-Hz unitary strength, a uEPSP of 6.19 mV (≈5.4-7.0 by glomerulus) or a uEPSC
  of ≈13 (DM6/VM2) to ≈41 pA (DM4).
- **What it reproduces.**
  - The 7-Hz decline and plateau (0.38 at 4 s, against 0.44 in the examples).
  - The S8D recovery: 0.52, 0.59, 0.65, 0.76, 0.88, 0.99 at 0.5-30 s.
  - N15's 10-Hz curve: 0.80, 0.67, 0.49 and 0.32 at stimuli 2, 3, 6 and 20 (observed 0.82, 0.64, 0.44, 0.34).
  - The 15-Hz test train (0.66 against 0.66 at 469 ms).
  - A flat plateau over long 7-10 Hz trains and after high-rate trains.
- **Odor-like step from 8-Hz rest to 100 Hz** (derived): per-spike strength 0.35 at the first spike, 0.10 at 50 ms,
  0.06 at 100 ms and 0.05 at 490 ms.
  - For comparison, N15's single pool gives 0.41, 0.15, 0.08 and 0.05.
  - So the resting level does not remove the onset transient. Per-spike strength still falls 6-8× within 100-500 ms.

### 7.3 Arithmetic (derived)
- **Formulas.**
  - Regular spikes at interval d, per pool: x = (1 − z)/(1 − f·z), with z = e^(−d/τ). This is the strength just before
    each spike.
  - Poisson spikes at rate λ, per pool: E[x] = 1/(1 + (1 − f)·λ·τ). This is exact, because E[e^(−Δ/τ)] = λτ/(1 + λτ)
    for exponential intervals.
  - Two additive pools: combine as w·x_A + (1 − w)·x_B. This stays exact for Poisson input, by linearity.
  - For multiplied factors (M2), the Poisson mean is not the product of the means. The exact form is
    [1 − m1 − m2 + m12 + f2·B·(m2 − m12) + f1·A·(m1 − m12)] / (1 − f1·f2·m12), where mi = λτi/(1 + λτi),
    m12 = λ/(λ + 1/τ1 + 1/τ2), and A, B are the per-factor Poisson means.
- **M4 at 6 Hz** (d = 0.1667 s):
  - Slow: z = e^(−0.0222) = 0.97802, so x = 0.02198/(1 − 0.83 × 0.97802) = 0.02198/0.18824 = 0.1168.
  - Fast: z = e^(−0.5556) = 0.57375, so x = 0.42625/(1 − 0.67 × 0.57375) = 0.42625/0.61559 = 0.6924.
  - Regular total: 0.5 × (0.1168 + 0.6924) = **0.405**.
  - Poisson: slow 1/(1 + 0.17 × 6 × 7.5) = 1/8.65 = 0.1156; fast 1/(1 + 0.33 × 6 × 0.3) = 1/1.594 = 0.6274. Total
    **0.371**.
- **M4 at 8 Hz** (d = 0.125 s):
  - Slow: z = 0.98347, so x = 0.01653/0.18372 = 0.0900. Fast: z = 0.65924, so x = 0.34076/0.55831 = 0.6103.
  - Regular total: **0.350**.
  - Poisson: slow 1/11.2 = 0.0893; fast 1/1.792 = 0.5580. Total **0.324**.
- **M4 at 19 Hz** (d = 0.05263 s):
  - Slow: z = 0.99301, so x = 0.00699/0.17580 = 0.0398. Fast: z = 0.83909, so x = 0.16091/0.43781 = 0.3675.
  - Regular total: **0.204**.
  - Poisson: slow 1/25.225 = 0.0396; fast 1/2.881 = 0.3471. Total **0.193**.
- **N15 single pool** (f 0.78, τ 0.893 s):

  | rate | z | regular | Poisson |
  |---|---|---|---|
  | 6 Hz | 0.82975 | 0.17025/0.35279 = 0.483 | 1/(1 + 0.22 × 6 × 0.893) = 0.459 |
  | 7 Hz | 0.85217 | 0.441 | — |
  | 8 Hz | 0.86938 | 0.13062/0.32188 = 0.406 | 0.389 |
  | 19 Hz | 0.94277 | 0.05723/0.26464 = 0.216 | 0.211 |

- **KW09** (f 0.72, τ 2.4 s): regular 0.204, 0.160, 0.073 and Poisson 0.199, 0.157, 0.073 at 6, 8 and 19 Hz.
- **Check against the one in vivo point** (DM4, 3.44 Hz, Poisson):

  | source | resting strength |
  |---|---|
  | measured | 0.26 |
  | M4 | 0.466 |
  | N15 | 0.596 |
  | KW09 | 0.302 |

  - With M4's other parameters fixed, the measured 0.26 needs w ≈ 0.88 (derived). On n = 3 that bounds a DM4-like
    synapse; it is not a parameter to adopt.

### 7.4 Implications for brainfly (mine)
- **Keep the resting synapse at or below ≈0.4 of rested strength at 6-8 Hz.**
  - VM2/DM6-based fits (M4, N15) give 0.32-0.46.
  - DM4 and minimal-stimulation data (KW09, KW08 Fig. 8G and the in vivo comparison) give 0.16-0.30.
  - At 19 Hz, everything gives ≤0.21.
- **Nothing in the primary data supports ≈0.6 at 7 Hz**, so raising the resting strength is not justified by the
  literature.
- **The main thing a single pool misses is the 7.5-s recovery of half the synapse after tonic firing.** It matters for:
  - odor pulses or pairings 1-10 s apart;
  - recovery after an odor ends;
  - silencing ORNs (inhibitory odors). KW08 note that this recovery is too slow to explain odor-offset PN excitation.

  If only one pool can be implemented, N15's 0.78 / 0.893 s gives nearly the same resting levels as M4 (0.46/0.39/0.21
  against 0.37/0.32/0.19, Poisson) and the same odor-step depression. It recovers too fast after tonic firing: 0.79 at
  1 s against 0.56 measured.
- **On PN accommodation.** Every depletion variant cuts per-spike strength 6-8× during a 100-Hz step from rest (§7.2).
  N15 found its depression-only PN model *more* transient than real PNs, and needed the slow component plus slowly growing
  presynaptic inhibition for sustained responses.
  - So a brainfly PN that fails to accommodate is unlikely to be explained by the resting level of fast depression.
  - The non-depressing slow component (brainfly's 0.9927 / 33.2 s, from N15's odor-fitted model), PN output saturation,
    and the timing of inhibition are the more likely levers. This is untested here.
- **Tonic presynaptic inhibition, if modelled as reduced release, also reduces depletion** (Olsen & Wilson 2008: inhibited
  synapses have higher paired-pulse ratios).
  - In N15's model, resting inhibition doubles A (0.34 → 0.67) but halves the net per-spike efficacy (0.17).
  - KW08's DM4 point (net ≈0.26 in an intact fly) constrains the product, not either factor.
- **High rates.** Depression at ≥20-50 Hz is faster and deeper in the data than in any 10-Hz-based model (KW08 Fig. 8F;
  the 25-ms paired-pulse ratio).
  - If odor-onset PN peaks come out too large, a third, fast-refilling, high-p component (release ≈0.4-0.5 per spike,
    refilling in ≲0.1 s) is what the data suggest.
  - Its size is unconstrained by the available figures.

## Sources

- Kazama H, Wilson RI (2008). Homeostatic matching and nonlinear amplification at identified central synapses.
  *Neuron* 58:401-413. doi:10.1016/j.neuron.2008.02.030.
  - [PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)
  - [Published PDF (Kazama lab)](https://kazamalab.riken.jp/pdf/Neuron_Kazama&Wilson_2008.pdf)
  - [Supplement mmc1](https://ars.els-cdn.com/content/image/1-s2.0-S0896627308001840-mmc1.pdf)
  - High-resolution figures:
    [Fig. 4](https://ars.els-cdn.com/content/image/1-s2.0-S0896627308001840-gr4_lrg.jpg),
    [Fig. 8](https://ars.els-cdn.com/content/image/1-s2.0-S0896627308001840-gr8_lrg.jpg),
    [Fig. 9](https://ars.els-cdn.com/content/image/1-s2.0-S0896627308001840-gr9_lrg.jpg)
  - Erratum: *Neuron* 59:183, doi:10.1016/j.neuron.2008.06.015 (not accessible).
- Kazama H, Wilson RI (2009). Origins of correlated activity in an olfactory circuit. *Nat Neurosci* 12:1136-1144.
  doi:10.1038/nn.2376.
  - [PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/)
  - [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnn.2376/MediaObjects/41593_2009_BFnn2376_MOESM16_ESM.pdf)
- Nagel KI, Hong EJ, Wilson RI (2015). Synaptic and circuit mechanisms promoting broadband transmission of olfactory
  stimulus dynamics. *Nat Neurosci* 18:56-65. doi:10.1038/nn.3895.
  - [PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/)
  - [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnn.3895/MediaObjects/41593_2015_BFnn3895_MOESM98_ESM.pdf)
  - [Figures (nature.com)](https://www.nature.com/articles/nn.3895)
- Nagel KI, Wilson RI (2016). Mechanisms underlying population response dynamics in inhibitory interneurons of the
  *Drosophila* antennal lobe. *J Neurosci* 36:4325-4338. doi:10.1523/JNEUROSCI.3887-15.2016.
  [PMC4829653](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)
- Olsen SR, Wilson RI (2008). Lateral presynaptic inhibition mediates gain control in an olfactory circuit. *Nature*
  452:956-960.
  - [PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/)
  - [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnature06864/MediaObjects/41586_2008_BFnature06864_MOESM230_ESM.pdf)
- Gouwens NW, Wilson RI (2009). Signal propagation in *Drosophila* central neurons. *J Neurosci* 29:6239-6249.
  [PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/)
- Gaudry Q et al. (2013). Asymmetric neurotransmitter release enables rapid odour lateralization in *Drosophila*.
  *Nature* 493:424-428. [PMC3590906](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/)
- Kazama H, Yaksi E, Wilson RI (2011). Cell death triggers olfactory circuit plasticity via glial signaling in
  *Drosophila*. *J Neurosci* 31:7619-7630. [PMC3119471](https://pmc.ncbi.nlm.nih.gov/articles/PMC3119471/)
