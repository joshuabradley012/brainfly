# The PN's resting state: resting receptor drive, tonic inhibition, glomerulus differences, sex, and models

Compiled 2026-10-10 from full texts (PMC HTML/XML via NCBI and Europe PMC), figures read at high resolution, and
supplements (Nature/Elsevier/eLife files), plus three released connectome tables:
- Nagel, Hong & Wilson 2015 (N15): text, Figs. 3 and 7, Supplementary Fig. 6.
- Gouwens & Wilson 2009 (GW09): text, Figs. 7 and 8, the seal-model equation.
- Olsen & Wilson 2008: Supplementary Figs. 2, 4 and 6. Olsen, Bhandawat & Wilson 2007: Figs. 1 and 2.
- Kazama & Wilson 2008/2009 (KW08, KW09), Gaudry et al. 2013 (Figs. 2, 3), Tobin et al. 2017, Jeanne & Wilson 2015,
  Kazama, Yaksi & Wilson 2011, Yaksi & Wilson 2010, Nagel & Wilson 2016, Hong & Wilson 2015, Wilson & Laurent 2005,
  Liu & Wilson 2013, Chou et al. 2010, Silbering & Galizia 2007, Martelli & Fiala 2019, Mohamed et al. 2019,
  Root et al. 2008, Bhandawat et al. 2007 (Supplementary Fig. 2), Olsen et al. 2010.
- Grabe et al. 2016 Table S1; Mosca & Luo 2014; Berg et al. 2025 (MaleCNS); Kohl et al. 2013 (abstract).
- Models: N15; Kao & Lo 2020 (author PDF); Liu, Li, Tang, Qin & Tu 2021; Kim, Lazar & Slutskiy 2015.
- ORN counts: FlyWire (Schlegel et al. 2024, `Supplemental_file1_neuron_annotations.tsv`), hemibrain (Schlegel et al.
  2021, Supplementary files 2-3), MaleCNS (brainfly's `~/fly-data/brain.npz`, `cell_type` column).

Purpose: decide which of deeper resting depression, tonic presynaptic inhibition, larger convergence or
glomerulus-specific synapses the literature supports for giving brainfly's PNs flies' small resting receptor drive
together with flies' steep weak-input transform. The model's side of the problem is in odor_resting_drive_check.py
(silencing every ORN drops the PNs 24.8 mV; DM1 18, DM4 13, DL5 19; GABAergic LNs 4.24 → 1.90 spikes/s) and pn_toy.py.

**Conventions** (as in the other notes)
- Text in quotation marks is verbatim.
- "(fig., approx.)" = read off a published figure with a pixel grid calibrated on its axis ticks. Expect ±3-5% of full
  scale; trace levels carry ±0.5 mV (Vm) or ±3-5 spikes/s (PSTH) extra from line width.
- "(derived)" = my arithmetic, shown or reproducible. "(count)" = my count from a released connectome table.
- "Not reported" = searched the text, legends and accessible supplement and did not find it.
- E = per-spike strength at rest as a fraction of the rested (0.033 Hz) unitary strength. D = a tonic divisor of
  release (N15's form: release and depletion both divided). Pools are written (weight, fraction released u = 1 − f,
  recovery τ): KW09 (1, 0.28, 2.4 s); M4 (0.5, 0.17, 7.5 s) + (0.5, 0.33, 0.3 s); N15 (1, 0.22, 0.893 s). For Poisson
  spikes at rate r a pool gives E = 1/(D + u·r·τ) per spike (orn_pn_depression.md §7.3, with D added).

**Access limits**
- Olsen & Wilson 2008 Full Methods (behind the Nature paywall): the glomerulus and genotype of the Supp. Fig. 6 cells
  are not known.
- Gaudry et al. 2013 Supplementary Information: PMC serves it through a JavaScript download page; not read.
- Grabe et al. 2016 main text: Cell Press returned 403 and ScienceDirect serves the body by script; only Table S1 read.
- Seki et al. 2010 (LN types): 403. Wechsler & Bhandawat 2025 (bioRxiv, Or7a/DL5): rate-limited; abstract only.
- Bhandawat 2007 Supp. Fig. 2 baselines are read on a 200-spikes/s scale (±5 spikes/s).

Related notes, not repeated here: [orn_pn_depression.md](orn_pn_depression.md) (train data, M4, the DM4 0.26),
[weak_input_gain.md](weak_input_gain.md) (Olsen 2010's transform, the toy, convergence, the DL5 contradiction),
[presynaptic_inhibition.md](presynaptic_inhibition.md) (evoked inhibition magnitudes, N15's I(t), LN rates),
[pn_ln_dynamics.md](pn_ln_dynamics.md) (PN passive properties, uEPSP time course, Rin by glomerulus),
[orn_dynamics.md](orn_dynamics.md) (ORN spontaneous rates), [lateral_excitation.md](lateral_excitation.md)
(deafferented PNs), [../Rung 4 resting state data/short_term_plasticity.md](../Rung%204%20resting%20state%20data/short_term_plasticity.md)
(PPR data incl. Fulterer 2018, Rozenfeld 2023).

## Summary

1. **Verdict.** Of the four levers, the literature directly supports **tonic inhibition at rest, set glomerulus by
   glomerulus**. It measures **deeper resting depression** where it has been tested (DM4), but offers nothing that keeps
   the transform steep with it. **Larger convergence** is not a female-vs-male correction except, possibly, in DM4.
   **Glomerulus-specific resting suppression** is clearly required (DM1 most of all), but nothing measured explains
   **DL5's** sensitivity. Items 2-9 give the evidence.
2. **Tonic inhibition at rest is measured, and it is about as large as the resting receptor drive itself.**
   - N15: "Blocking inhibition depolarized the mean PN membrane potential even in the absence of odors, likely by
     increasing the amount of spontaneous excitatory synaptic input onto PNs."
   - Mean of 17 PNs (DM6, VM2, VM7; 5 µM picrotoxin + 50 µM CGP54626): pre-odor Vm ≈ −55 to −58 mV in saline, ≈ −49
     to −51 mV with the antagonists, i.e. **+5 to +8 mV** (Figs. 3b and 7a, fig., approx.).
   - N15's own model, whose only inhibition is presynaptic and whose resting divisor (≈4-5) comes unscaled from the
     LNs' spontaneous rate, moves the pre-odor baseline by ≈7.5 mV (Fig. 7b, fig., approx.). Text: adding inhibition
     "decreased baseline (pre-odor) activity relative to the steady-state odor response. In this sense, inhibition
     increased the signal-to-noise ratio of postsynaptic activity."
   - Against GW09's ≈ −65 mV rest without ORN input, flies' resting receptor drive is ≈7-10 mV with inhibition and
     ≈15 mV without (derived; different cells and glomeruli). brainfly, which has no tonic inhibition, drops 13-19 mV
     in DM4, DL5 and DM1 (24.8 mV mean), close to the *uninhibited* fly value.
   - Corroborating, all qualitative: Wilson & Laurent 2005 ("In some cells, CGP54626 caused an increase in the
     spontaneous spiking rate of the cell"); Liu & Wilson 2013 ("GABA-LNs are spontaneously active and provide tonic
     inhibition to PNs"); Silbering & Galizia 2007 (picrotoxin at ≥10 µM "induced spontaneous calcium waves in the
     AL"); Olsen 2010 (DM1's high σ from "odor-evoked intra-glomerular GABA release and/or tonic inter-glomerular GABA
     release").
   - **Not measured: the locus at rest.** No paper reports spontaneous EPSC amplitude or frequency before and after
     the antagonists. Picrotoxin also blocks GluCl, and PNs have postsynaptic GABA-A and GABA-B responses.
3. **The DM4 comparison does not rule out a tonic divisor near 2.**
   - KW08 matched intact-fly spontaneous EPSCs (10.6 ± 1.2 pA, n = 3) with 4-Hz evoked uEPSCs after cutting the
     antennal nerves (10.7 ± 2.6 pA, n = 3). The ratio is 0.99 ± ≈0.27 (derived SE).
   - For a depleting synapse a release divisor lowers steady-state release only by (1 + u·r·τ)/(D + u·r·τ).
   - With DM4's own depression (KW09's pool), the point estimate gives D ≈ 1.3, one SE allows D ≤ 2.6, and two SE
     allow D ≤ 5.4. With brainfly's M4 the limits are D ≤ 1.55 (1 SE) and ≤ 2.9 (2 SE) (derived, §2.5).
   - KW08's p = 0.79 (multiple-probability fluctuation analysis in the same cut-nerve preparation) caps any tonic
     presynaptic inhibition *in that preparation* at 1/0.79 ≈ 1.27 if it acts on p (derived). So the rested 6.19-mV
     uEPSP brainfly is built on is effectively uninhibited.
4. **Deeper resting depression is measured too, and the two levers interact.**
   - DM4: 0.26-0.28 of rested at 3.4-4 spikes/s (orn_pn_depression.md §1.6, §2).
   - DM6: spontaneous EPSCs average 7.5 (ipsilateral) and 5.4 pA (contralateral) (Gaudry 2013 Fig. 3e, fig., approx.).
     Their rate, 58 Hz per antenna, puts DM6 ORNs at 2.2 spikes/s (Tobin 2017). Against the rested 13.3 pA (KW08)
     that is **E ≈ 0.41-0.56** (derived; an upper bound, since small events are missed).
   - KW09's pool predicts 0.30 (DM4) and 0.40 (DM6), M4 0.47 and 0.54. **One KW09-like synapse explains both
     glomeruli from their ORN rates; no glomerulus-specific depression is needed for these two.**
   - KW09's pool with FlyWire ORN counts and measured spontaneous rates gives resting drives of ≈6-8 mV for DM4, DM6,
     VM2, DL5 and VM7d but ≈13-15 mV for DM1, DL1 and DA1. M4 gives 9-38 mV (derived, §1.6). Deep depletion caps the
     drive near N/(u·τ)·A whatever the ORN rate.
   - **Interaction.** Under deep depletion a release divisor hardly changes the resting drive: removing D = 4 raises it
     only 1.4-1.5× at 7-10 spikes/s with KW09's pool. If VM2/VM7 synapses depleted like DM4's, N15's 5-8 mV would then
     need a postsynaptic part. Under M4- or N15-like depletion, D ≈ 2-5 reproduces it (derived, §2.5).
5. **Resting suppression must be glomerulus-specific; DM1 is the clearest case.**
   - DM1 PNs: "In DM1 PNs, spontaneous firing rates are close to zero" (Gaudry 2013, one antenna), although DM1 has
     68-86 ORNs (EM) firing 9-15 spikes/s.
   - Compare DM6 PNs: ≈8-10 (ipsilateral) and ≈5-6 spikes/s (contralateral) on 2.2-spikes/s ORNs (Gaudry Fig. 2e,
     fig., approx.). DL1 PNs: 5.6 spikes/s on 17.2-spikes/s ORNs (Olsen 2007, fig., approx.).
   - DM1's weak-input gain is GABA-limited (σ 45 → 13 with GABA blocked; weak_input_gain.md §1.3).
   - Sensitivity to GABA varies ≈25-fold across glomeruli and is "mainly an autonomous feature of that glomerulus"
     (Hong & Wilson 2015). CGP54626 raised odor responses in VM2, "slightly increased the response of DM4, but did
     not affect DM1" (Martelli & Fiala 2019).
   - DM4, DL5 and DM1 have no sensitivity measurement.
6. **Convergence: male and female EM counts agree, except in DM4** (counts, §4.2).

   | | FlyWire ♀ | hemibrain ♀ (right AL) | MaleCNS ♂ |
   |---|---|---|---|
   | DM4 | 41 | 60 | 32 |
   | DL5 | 42 | 39 | 43 |
   | DM1 | 68 | 86 | 74 |
   | VM7d | 33 | 44 (truncated) | 36 |

   - Grabe 2016's light-microscopy female excess (per antenna, DM4 23 vs 15.5, DL5 24 vs 21) is not reproduced.
   - Their DM4 and DL5 entries have no SD and equal their sensillum partners' (DM5, DA2), so they were not counted
     directly.
   - The MaleCNS paper: male bias "in just 4/60 types (DA1, VA1v, VA1d and VL2a)".
   - DL5 at 42-43 is only ≈12% below the toy's N ≈ 48.
7. **DL5's sensitivity is not explained by any of the four levers.**
   - Suppose odor-evoked ORN spikes were transmitted at the resting efficacy. Then the onset increment = resting drive
     × Δr/r0.
   - For DL5 (r0 14-20 spikes/s) and a 5-10 mV resting drive, +5.1 spikes/s adds only 1.3-3.6 mV. DM4 (r0 3.44)
     gets 7-15 mV for +5.0 (derived). Yet flies' DL5 PNs fire 44 spikes/s and DM4's 28.
   - So DL5's odor-evoked spikes must count several times more than its resting spikes. Alternatively, its true
     spontaneous rate in Olsen's flies was lower; that rate is not reported.
   - Facts specific to DL5: low-Rin PNs (≈360 MΩ) with faster uEPSPs (37% in ≈19 ms vs ≈30 ms in VM2); less lateral
     inhibition (m 4.19 vs 10.63 in VM7); "DL1 and DL5 did not show any mixture interaction" (Mohamed 2019).
   - Published candidate mechanisms, none measured in DL5: odor-evoked withdrawal of tonic inhibition from
     spontaneously active LNs (Kao & Lo 2020; pan-glomerular LNs "were either inhibited by odors or were only weakly
     excited", Chou 2010); faster recovery after activity (KW08 Fig. S8B, τ ≈ 0.4 s); facilitation (Liu 2021's fit;
     the paired-pulse data conflict).
8. **No published model reproduces resting drive, resting depression and Olsen's steep transform together.**
   - N15: resting divisor ≈4-5, which reproduces the measured resting disinhibition. But its resting drive is ≈18 mV
     above its −70 mV leak, ≈2× the fly estimate (derived from Fig. 7b). It was not fitted to Olsen's transform. Its
     Supp. Fig. 6: tonic presynaptic inhibition "causes the postsynaptic response to saturate at a higher presynaptic
     firing rate".
   - Kao & Lo 2020: tonic inhibition scaled to each glomerulus's spontaneous ORN rate, withdrawn at odor onset; one
     ORN per glomerulus; fitted to Olsen's Eq. 1 form.
   - Liu et al. 2021: fits Olsen's DL5 and VM7 data with facilitation + depression + presynaptic inhibition, but has
     no spontaneous input (rest is R = 0) and uses U = 0.24-0.31 against the measured p ≈ 0.79.
   - Jeanne & Wilson 2015's integrate-and-fire PN has no depression.
9. **Sex.**
   - I found no comparison of PN responses to general odors between sexes. For the pheromone channel: "First- and
     second-order olfactory neurons show identical pheromone responses" (Kohl 2013).
   - MaleCNS: "dimorphism of second order neurons is thus extremely limited".
   - The physiology above is from females except Jeanne & Wilson 2015 and Hong & Wilson 2015's LN-activation sEPSC
     experiments (shakB² males).

---

## 1. PN resting potential and resting receptor drive in vivo (Q1)

### 1.1 How Gouwens & Wilson 2009 got "−55 to −60" and "−65" ([PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/))
- **ORNs intact (Fig. 7).** They matched whole-cell firing to each cell's cell-attached rate by injecting current: "On
  average, we had to hyperpolarize the membrane from −47.8 ± 1.6 mV to −57.8 ± 1.5 mV to recapitulate the
  cell-attached firing rate (n = 12)".
  - The estimated cell-attached Vm of the 12 cells spans ≈ −68 to −49 mV (Fig. 7D, fig., approx.).
  - Cell-attached spontaneous rates span ≈0-20 spikes/s (Fig. 7B, n = 27, fig., approx.).
- **ORNs removed (Fig. 8).** "The antennae were acutely removed for all experiments except those in Figures 1 C and 7."
  - Zero-current potentials from slow voltage ramps average ≈ −59.5 mV (cells −52 to −65), and ≈ −60.5 mV in TTX
    (Fig. 8B,C, fig., approx.). These are whole-cell values.
  - Their seal model (Fig. 7F) predicts ≈4-5 mV of seal depolarization at 600 MΩ with no synaptic input (fig.,
    approx.). That would put the true value near −64 to −65 mV (derived). The paper does not show this step.
- **The −15 pA.** For the seal model, "E cell was set to −65 mV, E seal to 0 mV, and spontaneous synaptic input was
  represented by a constant −15 pA current when incorporated". 15 pA × 598 MΩ ≈ 9 mV (derived), consistent with their
  5-10 mV. It is an assumption, not a measurement.
- **Which PNs.** "Recordings from DM1 PNs were made from NP5221-Gal4,UAS-CD8GFP flies …, and all other recordings were
  made from either GH146-Gal4,UAS-CD8GFP … or NP3062-Gal4,UAS-CD8GFP".
  - DM1 PNs were used for the passive fits. The glomeruli of the Fig. 7 cells are not stated.
  - Since DM1 PNs fire ≈0 spontaneously (Gaudry 2013) and the Fig. 7 cells fired 0-20 spikes/s, the "mostly DM1"
    reading in the brief (and in odor_resting_drive_check.py) is probably wrong (my inference).
- Females, 2-10 d.

### 1.2 Resting Vm with inhibition blocked (Nagel, Hong & Wilson 2015, [PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/))
- Current clamp, "a small negative holding current (~10 pA) was applied to bring the resting membrane potential to
  between −50 and −60 mV, thereby counteracting the small depolarizing current created by the seal conductance".
- Glomeruli: "we pooled data from PNs in glomeruli DM6, VM2, and VM7". Females, 1-3 d.
- Pre-odor baseline of the mean of 17 PNs (Fig. 3b; the same traces as Fig. 7a; fig., approx.):

  | reading | saline | PTX 5 µM + CGP54626 50 µM | difference |
  |---|---|---|---|
  | Fig. 3b, before the 20-ms pulse | −56.0 mV | −51.4 mV | 4.7 mV |
  | Fig. 3b, before the 2-s pulse | −57.3 mV | −50.5 mV | 6.8 mV |
  | Fig. 7a, same traces | −55.2 / −57.6 mV | −49.3 / −49.9 mV | 5.9 / 7.7 mV |

- The example cell (DM6, Fig. 3a) sits ≈7 mV more depolarized with the antagonists (fig., approx.).
- Fig. 3e: "additional negative holding current was applied after blocking inhibition to bring the baseline membrane
  potential to the same level as control (n=8 PNs from 8 flies)". The amount of current is not reported.
- A related observation (Methods): "In a subset of PN recordings, we observed very little depolarization of PNs in
  response to odor. This type of response was associated with very low or absent spontaneous activity, and generally
  all the PNs in the preparation exhibited the same behavior." Those preparations were discarded.

### 1.3 PN spontaneous activity with and without its ORNs

| glomerulus | ORN spontaneous (spikes/s) | PN spontaneous, ORNs active | PN without its ORNs | source |
|---|---|---|---|---|
| VM2 | 7.1 (n = 14); 0.7 in *Or43b* mutants (n = 13) | 2.5 (n = 14) | 0.16 (*Or43b*, n = 10) | Olsen 2007 Fig. 2B (fig., approx.) |
| DL1 | 17.2 (n = 10); 1.1 in *Or10a* mutants (n = 21) | 5.6 (n = 13) | ≈0.1 (*Or10a*, n = 10) | same |
| DM3 | — | example with spontaneous spikes | "Spontaneous activity is abolished" (antennal nerves severed) | Olsen 2007 Fig. 1C,D |
| antennal PNs | — | — | "PNs postsynaptic to antennal glomeruli in antennae-less flies show no spontaneous activity" | Olsen 2007 |
| VM7 | "~10" | ≈2-5 with antennae intact and removed alike (Supp. Fig. 2, fig., approx.) | sEPSPs "now absent" with palps removed | Olsen & Wilson 2008 Supp. Figs. 2, 4 |
| DM6 | 2.2 (from the sEPSC rate) | ≈8-10 ipsi, ≈5-6 contra, one antenna (Fig. 2e, fig., approx.) | — | Gaudry 2013; Tobin 2017 |
| DM1 | 9 (de Bruyne 2001 via DoOR); ≈15 ± 5 (Bhandawat Supp. Fig. 2, fig., approx.) | "close to zero" (one antenna); ≈5 ± 5 (Bhandawat, fig., approx.) | — | Gaudry 2013 Fig. 2g legend |
| DM4 | 3.44 ± 0.16 (KW09); ≈4 ± 5 (Bhandawat, fig., approx.) | ≈4 ± 5 (Bhandawat, fig., approx.) | — | |
| DA1 (males) | 1.5 ± 1.1 (n = 58) | 8.6 ± 6.3 (n = 44) | — | Jeanne & Wilson 2015 |

- Olsen 2007: "Odorant receptor mutations reduce spontaneous activity in both ORNs and their postsynaptic PNs." The
  silent-receptor mutants keep the LNs and the rest of the lobe intact. So **PN spontaneous spiking is driven by the
  PN's own ORNs, not by lateral or tonic network input.**
- KW09 Supp. Fig. 3 (VM7, palps removed, antennae intact): "Note that the magnitude of fluctuations is much smaller
  without direct ORN input. Thus, the major source of noise under these conditions is direct ORN input".
- Kazama, Yaksi & Wilson 2011: "we observed that spike-driven spontaneous EPSPs are absent in postsynaptic PNs after ORN
  somata are removed".
- KW08 on the spread across glomeruli: PNs "show very different levels of total spontaneous activity (R.I.W.,
  unpublished observations), due to the different numbers of ORNs presynaptic to each glomerulus and the different
  spontaneous firing rates of these ORN types."
- Olsen & Wilson 2008 Supp. Fig. 4b (antennae removed): VM7 "sEPSPs prior to odor stimulation are similar to above, as
  expected". These are single traces; a 10-40% size change would not be visible.

### 1.4 Spontaneous EPSC/EPSP rates and sizes in intact flies

| glomerulus | condition | sEPSC rate | sEPSC/sEPSP size | rested unitary (KW08) | E (derived) |
|---|---|---|---|---|---|
| DM4 | one antenna removed | 74.9 ± 8.6 Hz (n = 8; predicted 17.4 × 3.44 = 60) | — | — | — |
| DM4 | antennae intact | — | 10.6 ± 1.2 pA (n = 3); cloud ≈3-20 pA (KW09 Fig. 5a) | ≈41 pA | 0.26 |
| DM6 | contralateral antenna removed | 58 Hz (Tobin 2017 re-analysis) | ipsi 7.5, contra 5.4 pA (n = 15 pairs; fig., approx.) | 13.3 pA | 0.41-0.56 (upper bound) |
| DA1 (males) | intact | — | sEPSP ≈2 mV ("based on visual inspection of spontaneous EPSPs") | not measured | — |
| random PNs (*w¹¹¹⁸* females; Hong & Wilson 2015's GABA-uncaging set) | intact | — | baseline SD of the current "4.27±0.13 pA" | — | — |

- KW09: "we found that the rate of spontaneous EPSCs in DM4 PNs (74.9 ± 8.6 Hz, n = 8, one antenna removed) is not
  substantially different from the mean firing rate of DM4 ORNs (3.44 ± 0.16 Hz, n = 11) multiplied by the mean number
  of DM4 ORNs (17.4 ± 0.9 per antenna, n = 5 antennae)."
- Tobin 2017 (Methods): "In all recordings we analyzed, the contralateral antenna had been removed just before the
  recording, so PNs were receiving spiking input from ipsilateral ORNs only. The rate of these events was 58 Hz, and so
  dividing by 26.5 ORNs, we obtain 2.2 spikes/s/ORN."
- Gaudry 2013: "Averaged across all experiments, ipsilateral sEPSCs were 39% larger than their contralateral
  counterparts". Fig. 3e means read 7.49 and 5.38 pA (fig., approx.; ratio 1.39).
- DM6 E (derived): 7.5/13.3 = 0.56 and 5.4/13.3 = 0.41. If KW08's 13.3 pA mixes ipsi and contra fibres equally and
  rested strengths differ by 1.39 as sEPSCs do, both sides come out at 0.49.
  - KW09 noted that in DM6 "some small EPSCs fall below the limit of our recording noise", so these are upper bounds.
- Resting efficacy elsewhere: Not reported.

### 1.5 Distance to threshold
- Jeanne & Wilson 2015 (DA1, males): "the distance to spike threshold, which was about 10 mV on average (Figure 4C)"
  (n = 18), measured "in the absence of any stimulus", i.e. with spontaneous ORN drive.
- GW09 (assumption): "assuming a spike threshold at the SIZ near −40 mV".

### 1.6 Resting drive by glomerulus (derived)
Resting drive = N × r × E × A, where A is the integral of a rested uEPSP. Assumptions:
- N: FlyWire female counts (both antennae).
- r: measured spontaneous rates (§1.3; DL5 14-20 from de Bruyne 2001 and Hallem 2004/2006 via orn_dynamics.md;
  VM7d 10-12.8 from Olsen 2008 and Nagel 2011's pb1A).
- A ≈ peak × (decay to 37%): DL5 7.0 mV × 19 ms; VM2 5.4 mV × 30 ms (KW08 Fig. 4C via pn_ln_dynamics.md). DM4
  6.9 mV × 19 ms is assumed like DL5 (both low-Rin, ≈260 and ≈360 MΩ). DM6 5.5 mV × 30 ms is assumed like VM2 (≈850 vs
  ≈1010 MΩ). The rest are assumed 6.19 mV × 25 ms.
- No tonic inhibition.

| glomerulus | N | r | E, KW09 / M4 | drive, KW09 pool | drive, M4 | KW09 cap N/(u·τ)·A |
|---|---|---|---|---|---|---|
| DM4 | 41 | 3.44 | 0.30 / 0.47 | 5.6 mV | 8.6 mV | 8.0 mV |
| DM6 | 52 | 2.2 | 0.40 / 0.54 | 7.6 | 10.2 | 12.8 |
| VM2 | 37 | 7.1 | 0.17 / 0.34 | 7.4 | 14.6 | 8.9 |
| VM7d | 33 | 10-12.8 | 0.10-0.13 / 0.25-0.29 | 6.6-6.8 | 14.7-16.3 | 7.6 |
| DL5 | 42 | 14-20 | 0.07-0.10 / 0.19-0.24 | 7.5-7.7 | 18.5-20.9 | 8.3 |
| DM1 | 68 | 9-15 | 0.09-0.14 / 0.23-0.30 | 13.4-14.2 | 28.8-35.7 | 15.7 |
| DL1 | 69 | 17.3 | 0.08 / 0.21 | 14.6 | 38.1 | 15.9 |
| DA1 | 126 | 1.5 | 0.50 / 0.61 | 14.6 | 17.8 | 29.0 |

- Cross-checks from measured sEPSCs (derived):
  - DM4: 2 × 74.9 Hz × 0.26 × 0.131 mV·s ≈ 5.1 mV.
  - DM6: 2 × 58 Hz × 0.49 × 0.165 mV·s ≈ 9.4 mV (upper bound).
  - Both are inside GW09's 5-10 mV.
- **Reading.** DM4's own low-rate depression, applied everywhere, gives fly-like drives in most glomeruli. It caps the
  drive near N/(u·τ)·A, so a high spontaneous rate (DL5) costs little resting drive. DM1, DL1 and DA1 stay at 13-15 mV.
  DM1's near-zero PN firing says it needs ≈2× more suppression.
- **brainfly's DM4, decomposed (derived).** Model/fly drive ≈ (6/3.44 rate) × (0.37/0.26-0.30 efficacy) × (≈1.6 PSP
  integral, if DM4's uEPSP is as fast as DL5's) × (32/41 ORNs) ≈ 2.7-3.1. Dividing brainfly's 13 mV by that gives
  ≈4.2-4.8 mV, consistent with the fly estimate. This ignores any difference between DM4's model uEPSP (scaled by
  MaleCNS synapse counts) and 6.9 mV.
  - The PSP-integral factor: brainfly's kernel (5-ms exponential current into τm 20 ms) has an integral of 31.7 ms ×
    peak, ×1.086 with the slow component, ≈34 ms per mV. DL5's measured uEPSP gives ≈22 ms per mV and VM2's ≈33 ms per
    mV (derived from pn_ln_dynamics.md §1.1).

## 2. Tonic inhibition at rest (Q2)

### 2.1 Evidence for
- **N15** (§1.2): resting depolarization of 5-8 mV with picrotoxin + CGP54626, attributed "likely" to "increasing the
  amount of spontaneous excitatory synaptic input onto PNs".
- **N15 Fig. 6** (presynaptic_inhibition.md §4): channelrhodopsin activation of LNs makes spontaneous EPSCs "slowly become
  smaller and less frequent". So resting ORN release is under LN control.
- **Wilson & Laurent 2005** ([PMC6725763](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/)), Methods: "In some cells,
  CGP54626 caused an increase in the spontaneous spiking rate of the cell. In these cases, additional constant
  hyperpolarizing current was added to the current command to return the cell to its original spontaneous spiking
  rate before testing any more odors."
  - Not quantified. The published CGP odor effects are therefore after re-hyperpolarizing.
- **Liu & Wilson 2013** ([PMC3690841](https://pmc.ncbi.nlm.nih.gov/articles/PMC3690841/)): "Importantly, GABA-LNs are
  spontaneously active and provide tonic inhibition to PNs" (citing Chou 2010 and Wilson & Laurent 2005).
  - Also: "picrotoxin likely has bidirectional effects on the total level of inhibition in the circuit", because Glu-LNs
    inhibit GABA-LNs through GluCl.
- **Chou et al. 2010** ([PMC2847188](https://pmc.ncbi.nlm.nih.gov/articles/PMC2847188/)): "pan-glomerular LNs had
  unusually high rates of spontaneous activity, suggesting that they may be particularly important in broadcasting
  tonic inhibition throughout the antennal lobe."
  - "Pan-glomerular LNs were either inhibited by odors or were only weakly excited. Because they are mainly GABAergic,
    inhibition of pan-glomerular LNs would tend to disinhibit the entire antennal lobe in response to odors."
  - Rates: pan-glomerular ≈10.2 vs others ≈5.4 spikes/s (presynaptic_inhibition.md §6).
- **Silbering & Galizia 2007** ([PMC6673347](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673347/)): "The concentration of
  PTX was set to 5 μm because concentrations of 10 μm and higher induced spontaneous calcium waves in the AL, which made
  it impossible to analyze the data."
- **Olsen et al. 2010** ([PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/)):
  - DM1: "modulated by inhibition arising from odor-evoked intra-glomerular GABA release and/or tonic inter-glomerular
    GABA release. This appears as a higher value of the semisaturation constant σ for this glomerulus."
  - VM7: with antagonists, the faintest stimulus (ORN +0.1 spikes/s) gave a PN response of ≈35 against ≈2.5 spikes/s
    in saline (weak_input_gain.md §1.2). Inhibition already acts at near-resting input.

### 2.2 Evidence against, or limits
- **KW08's DM4 comparison** (orn_pn_depression.md §1.6). It constrains D only weakly (§2.5): D ≤ 2.6 at 1 SE under
  DM4's own depression.
- **KW08's p = 0.79 in the cut-nerve preparation** (DL5 and DM4): "Estimated release probability was consistently high,
  with a mean value of 0.79." With the palps intact, any tonic presynaptic inhibition there is ≤1.27× if it acts on p
  (derived).
- **Olsen & Wilson 2008 Supp. Fig. 6** (supplement p. 6): "Symbols show the average EPSC amplitude immediately before
  odor stimulation (●) or during odor stimulation (○) for each trial."
  - Configuration: EPSCs evoked every 0.25 s from the cut ipsilateral nerve; contralateral antenna and palps intact;
    the recorded PN's receptor mutated.
  - Pre-odor EPSCs, one cell each (fig., approx.):

    | cell | saline | CGP | CGP + PCT |
    |---|---|---|---|
    | 6c | ≈17.5 pA | ≈17.3 pA | ≈17.1 pA |
    | 6f | ≈42 pA | ≈41 pA | ≈52 pA (+25%) |

  - These are 4-Hz-depressed EPSCs. Removing D = 2 would raise them 1.3× (KW09 pool) to 1.6× (M4) (derived). Cell 6c
    argues against D ≈ 2 in that cell. Cell 6f's +25% fits D ≈ 1.5 (M4) to ≈2 (KW09 pool). It appeared only when
    picrotoxin was added to CGP (CGP alone changed nothing), and picrotoxin also blocks GluCl.
- **Root et al. 2008** (explant; presynaptic_inhibition.md §3): "CGP54626 significantly increases PN response at high
  stimulus intensities but not at low intensities". No tonic GABA-B effect at low activity there.
- **Martelli & Fiala 2019** ([PMC6581506](https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/)): CGP54626 "did not affect
  DM1 response to methyl acetate" (odor-evoked, not resting).

### 2.3 Nagel et al. 2015's resting inhibition: how it was set and what it reproduces
- **Form.** "This inhibitory signal divided the input to the model (ORN firing rate) at each point in time. Note that
  this is equivalent to inhibition decreasing the probability of synaptic release, which governs both the rate of
  depression r and the amplitude of the synaptic conductance g syn."
- **Scale.** I(t) is the mean of 45 recorded LNs convolved with a 25-ms alpha function. "The magnitude of I(t) that we
  computed in this manner provided a good qualitative fit to the data, so its scale was not adjusted."
  - At rest the LNs fire 4.6 ± 2.8 spikes/s, so I_rest ≈ 4-5. presynaptic_inhibition.md §4 derives the same from
    Fig. 7c (A 0.67-0.69 with inhibition, 0.33-0.34 without).
  - For the modelled LN population (Fig. 8): "A positive offset of 1 spike per ms −1 was added to LN ( t ) to match
    measured baseline LN activity."
- **What it reproduces.** Fig. 7b, pre-odor (fig., approx.): ≈ −51 to −52 mV with inhibition, ≈ −44 mV without, a
  ≈7.5 mV difference. The data's is 5-8 mV (§1.2). The divisor's size was never fitted, yet it matches.
- **What it does not.**
  - PN model: "E leak was set to −70 mV, which is close to the resting potential of PNs in tetrodotoxin"; Rm 800 MΩ,
    τm 5 ms, E_syn −10 mV, 40 ORNs, VM7 ORN rates.
  - With inhibition the model rests ≈18 mV above its leak (≈26 mV without; derived). That is about twice flies'
    ≈7-10 mV. The absolute baseline still lands near the data (−56/−57 mV) because the leak sits ≈5 mV below GW09's
    ≈ −65 mV.
- **Steady-state transform with tonic inhibition** (Supp. Fig. 6a, 2-s steps from zero ORN rate): "adding increasing
  amounts of tonic presynaptic inhibition causes the postsynaptic response to saturate at a higher presynaptic firing
  rate. Small amounts of presynaptic inhibition have a more profound effect on the response to low presynaptic firing
  rates than on the response to high presynaptic firing rates."
  - This model has no spontaneous input, so it says nothing about the resting-depletion benefit that the toy found
    (weak_input_gain.md §9; pn_toy.py).

### 2.4 LN spontaneous activity in intact vs acutely deafferented lobes
- **Direct comparison: Not reported.** Spontaneous LN rates (2.3-16.8 spikes/s by line) all come from flies with
  antennae intact (presynaptic_inhibition.md §6).
- Indirect, after acute antennal removal with the palps intact:
  - Kazama, Yaksi & Wilson 2011 Fig. 3B: "Note large spontaneous IPSPs (arrowhead), which are typical of eLNs".
  - Yaksi & Wilson 2010 (antennae removed): "Cd 2+ blocks spontaneous IPSPs and so increases eLN excitability".
  - So spontaneous GABA release continues after acute antennal deafferentation, at an unknown rate.
- Kazama, Yaksi & Wilson 2011: "Palps were removed acutely to minimize spontaneous activity in the network." Some
  network activity therefore depends on palp ORNs.
- Nagel & Wilson 2016: "the distinction between regular-firing cells and bursty cells is due, at least in part, to
  differences in the intrinsic properties of these cells". The pattern is partly intrinsic; whether the rate needs
  ORN drive is not tested.
- brainfly's GABAergic LNs: 4.24 → 1.90 spikes/s when every ORN is silenced (odor_resting_drive_check.json).

### 2.5 Arithmetic: tonic divisors and depletion (derived; script logic in the conventions)
**A. KW08's DM4 test.** The intact sEPSC is modelled as Poisson at 3.44 spikes/s with divisor D, the cut-nerve train as
regular 4 Hz without one. Measured ratio 10.6/10.7 = 0.99. Combined SE ≈ 0.99 × √((1.2/10.6)² + (2.6/10.7)²) = 0.27.

| pool | 4-Hz evoked E | intact/evoked at D = 1 / 1.5 / 2 / 3 / 4 | D at ratio 0.99 | D at 1 SE (0.725) | D at 2 SE (0.46) |
|---|---|---|---|---|---|
| KW09 (DM4's own) | 0.282 | 1.07 / 0.93 / 0.82 / 0.67 / 0.56 | 1.27 | 2.59 | 5.41 |
| M4 (brainfly) | 0.482 | 0.97 / 0.74 / 0.61 / 0.45 / 0.36 | <1 | 1.55 | 2.92 |
| N15 | 0.595 | 1.00 / 0.77 / 0.63 / 0.46 / 0.36 | 1.02 | 1.64 | 2.98 |

**B. How much removing a divisor D raises the steady-state resting drive** (E(1)/E(D), Poisson):

| pool | r (spikes/s) | D = 1.5 | D = 2 | D = 3 | D = 4 | D = 5 |
|---|---|---|---|---|---|---|
| KW09 | 2.2 | 1.20 | 1.40 | 1.81 | 2.21 | 2.61 |
| KW09 | 7.1 | 1.09 | 1.17 | 1.35 | 1.52 | 1.69 |
| KW09 | 10 | 1.06 | 1.13 | 1.26 | 1.39 | 1.52 |
| M4 | 2.2 | 1.33 | 1.64 | 2.24 | 2.82 | 3.39 |
| M4 | 7.1 | 1.25 | 1.49 | 1.95 | 2.37 | 2.79 |
| M4 | 10 | 1.22 | 1.43 | 1.83 | 2.21 | 2.58 |
| N15 | 7.1 | 1.21 | 1.42 | 1.84 | 2.25 | 2.67 |

- Suppose N15's 5-8 mV is presynaptic, on top of a 5-10 mV inhibited drive. The drive then rises 1.5-2.6×, which needs
  D ≈ 2-5 with M4- or N15-like depletion at VM2/VM7 rates. At those rates (7-10 spikes/s) KW09-like depletion cannot
  deliver it (≤1.7× even at D = 5). At DM6's 2.2 spikes/s it can, with D ≈ 2.5-5.
- A divisor lowers the resting drive and the per-spike gain for an extra spike by the same factor E0. The toy's benefit
  from a divisor came from less depletion *during* the response and from a quieter PN (weak_input_gain.md §9;
  pn_toy.py).

## 3. Glomerulus-specific release, depression, and the DL5 puzzle (Q3)

### 3.1 What is measured, by glomerulus

| | DM4 | DL5 | DM1 | VM2 | DM6 | VM7(d) |
|---|---|---|---|---|---|---|
| ORN spontaneous (spikes/s) | 3.44 | 14-20 | 9-15 | 7.1 | 2.2 | ≈10-13 |
| ORNs, FlyWire ♀ / MaleCNS ♂ | 41 / 32 | 42 / 43 | 68 / 74 | 37 / 41 | 52 / 58 | 33 / 36 |
| rested uEPSC / uEPSP (KW08) | 41.4 pA / 6.9 mV | 37.0 / 7.0 | n.m. | 12.9 / 5.4 | 13.3 / 5.5 | n.m. |
| PN Rin at soma (KW08 Fig. S2) | ≈260 MΩ | ≈360 | n.m. | ≈1010 | ≈850 | n.m. |
| uEPSP decay to 37% | n.m. | ≈19 ms | n.m. | ≈30 ms | n.m. | n.m. |
| release probability | 0.79 (MPFA), uniform (single-p) | 0.79, uniform | n.m. | uniform | uniform | n.m. |
| resting E | 0.26 | n.m. | n.m. | n.m. | 0.41-0.56 | n.m. |
| LN-activation / GABA sensitivity (Hong & Wilson; max 1) | n.m. | n.m. | n.m. | 0.29 / 0.45 | 0.45 / 0.62 | — / 0.34 |
| lateral-inhibition slope m (Olsen 2010) | — | 4.19 | — | — | — | 10.63 |
| σ, saline (Olsen 2010) | 16.3 | 11.8 | 44.8 (13.4 with GABA blocked, refit in weak_input_gain.md) | — | — | 12.4 |
| PN spontaneous (spikes/s) | ≈4 | n.m. | ≈0-5 | 2.5 | 5-10 (one antenna) | ≈2-5 |

n.m. = not measured. Sources as in §1 and presynaptic_inhibition.md §5.

- KW08: "Estimates of p were uniform across glomeruli (Figure 7C). However, unlike values of q and p, values of N were
  significantly larger in large glomeruli (Figure 7D)."
- Mosca & Luo 2014 ([PMC4194450](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194450/)): "all observed ORN classes had a
  constant synaptic density of 0.56 Brp-Short puncta per µm3". ORN active-zone number scales with glomerular volume.
- **Depression at matched rates in different glomeruli: Not reported.** The trains are VM2 (KW08), DM6/VM2 (N15) and
  DM4 (KW09) at different rates.
  - The one cross-glomerulus check available, DM4 vs DM6 resting E, is consistent with a single KW09-like synapse
    (Summary 4).
- **Paired pulses.** Olsen & Wilson 2008: ≈0.55 at ≈25 ms (orn_pn_depression.md §5). Fulterer 2018: ≈0.93 at 10 Hz.
  Rozenfeld 2023: ≈1.5 at 10 ms and 1.2 at 30 ms (short_term_plasticity.md §1.1). These conflict; none splits by
  glomerulus.
- **GABA sensitivity and lateral inhibition** are glomerulus-specific (Hong & Wilson 2015; Olsen 2010; Root 2008's
  GABA-B R2 levels; Martelli & Fiala 2019's CGP effects VM2 > DM4 > DM1). Hong & Wilson: "tuning breadth was
  uncorrelated with either sensitivity to LN activation or sensitivity to GABA".
- **State-dependent presynaptic modulation in DM1** (abstracts only): starvation raises presynaptic sNPF facilitation
  in Or42b ORNs (Root et al. 2011), and LN tachykinin suppresses ORN presynaptic calcium (Ignell et al. 2009). Resting
  effects: Not reported.

### 3.2 DL5 (derived constraint and candidates)
- **The constraint.** If extra spikes are transmitted at E0, then resting drive / onset increment = r0/Δr (derived; the
  N·E0·A factor cancels). For a 5-10 mV resting drive:

  | glomerulus | r0 | Δr (Olsen's lowest point) | onset increment | flies' PN response |
  |---|---|---|---|---|
  | DL5 | 14 / 17 / 20 | 5.1 | 1.8-3.6 / 1.5-3.0 / 1.3-2.5 mV | 44 spikes/s |
  | DM4 | 3.44 | 5.0 | 7.3-14.5 mV | 28 spikes/s |
  | VM7 | ≈11 | 11.6 | 5.3-10.5 mV | 78 spikes/s |

  DL5 delivers ≥3-5× more PN spikes per predicted mV than DM4 (derived). Also, a KW09-like resting depression at
  17 spikes/s leaves E0 ≈ 0.08 (§1.6), so the small resting drive DL5 gets from deep depletion comes with almost no
  capacity for extra spikes.
- **DL5-specific facts.**
  - Large, low-Rin PN: N15's Methods note that "DL5 PNs have a distinctive large size and low input resistance".
  - Faster uEPSP than VM2 (KW08 Fig. 4C via pn_ln_dynamics.md). For a matched peak this lowers the resting drive per
    spike ≈1.5× and sharpens coincidence detection (my reading).
  - Olsen 2010: "The magnitude of inhibition was consistently smaller for DL5 than for VM7, implying that glomeruli
    differ in their sensitivity to lateral inhibition."
  - Mohamed et al. 2019 ([PMC6416470](https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/)): "the repellent-responsive
    glomeruli DL1 and DL5 did not show any mixture interaction, but mediate the lateral inhibition of the
    attractant-responsive glomeruli."
  - Liu et al. 2021 needed stronger depression *and* facilitation for DL5 than VM7 (fitted τD 368 vs 160 ms, τF 339 vs
    150 ms, U 0.31 vs 0.24).
- **DL5 ORN spontaneous rate in Olsen 2010's flies: Not reported.** The PSTHs in Supp. Fig. S2 have no zero line, and
  responses are baseline-subtracted.
- **Candidate mechanisms** (none measured in DL5):
  1. Odor-evoked withdrawal of tonic inhibition (Kao & Lo 2020, §5.2; Chou 2010's odor-inhibited pan-glomerular LNs;
     Glu-LN inhibition of GABA-LNs, Liu & Wilson 2013). This would make odor spikes more effective than resting ones
     without adding resting drive. But DL5's low sensitivity to lateral inhibition suggests weak GABA sensitivity, which
     cuts the other way.
  2. Recovery that speeds up with activity: KW08 Fig. S8B (τ ≈ 0.4 s after 50-200 Hz) vs S8D (7.5 s after 7 Hz). A
     single pool of this kind was rejected in orn_pn_depression.md §7.1 for flattening the rate dependence; untested
     with two pools.
  3. Facilitation at short intervals (Rozenfeld 2023's paired pulses; Liu 2021's fit). This conflicts with p ≈ 0.79 and
     with Olsen & Wilson 2008's paired-pulse ratios.

## 4. Female vs male ORN counts and PN responses (Q4)

### 4.1 Grabe et al. 2016, Table S1 (OSNs per antenna or palp, females / males; PNs; volumes in µm³)

| glomerulus (sensillum) | OSNs ♀ (SD) | OSNs ♂ (SD) | glomerular volume ♀ / ♂ | PNs ♀ / ♂ |
|---|---|---|---|---|
| DM4 (ab2) | 23 | 15.5 | 2597 / 2806 | 1 / 1 |
| DM5 (ab2) | 23 (6) | 15.5 (3.6) | 1269 / 912 | 2 / 1 |
| DL5 (ab4) | 24 | 21 | 2865 / 1456 | 1 / 1 |
| DA2 (ab4) | 24 (1.9) | 21 (3.6) | 1630 / 1050 | 6.5 / 5 |
| DM1 (ab1) | 38.5 (4.6) | 32 (5.9) | 4211 / 2821 | 1 / 1 |
| VA2 (ab1) | 43.5 | 32 (7.3) | 3278 / 4051 | 1 / 1 |
| DL1 (ab1) | 37.5 (6.5) | 26 (4) | 2267 / 2037 | 3 / 2 |
| VM7d (pb1) | 11.5 (6.5) | 15 (4.5) | 1578 / 1660 | 2 / 3 |
| VM2 (ab8) | 18 (6.5) | 15 (2.4) | 1551 / 1296 | 3 / 2 |
| DM6 (ab10) | 18 | 10.5 | 1439 / 1631 | 3 / 3 |
| DL4 (ab10) | 18 (3.2) | 10.5 (2) | 622 / 946 | 1 / 1 |
| DM2 (ab3) | 8 (3.9) | 8 (2.9) | 2241 / 2085 | 2 / 2 |
| DA1 (at1) | 62.5 (10.8) | 62.25 (11) | 4738 / 6182 | 8 / 10 |
| all | 1047.8 | 934.25 | 111593 / 103168 | 80.5 / 83 |

- Entries without SD repeat the sensillum partner's numbers exactly: DM4 = DM5, DL5 = DA2, DM6 = DL4 (derived from the
  table). So these were assigned, not counted.
- How the counts were made is in the main text, which was not accessible.

### 4.2 EM counts (both antennae; per brain, or per right AL for the hemibrain) (count)

| glomerulus | FlyWire ♀ | hemibrain ♀ (truncation) | MaleCNS ♂ | Grabe ×2, ♀ / ♂ | other |
|---|---|---|---|---|---|
| DM4 | 41 (21 L, 20 R) | 60 (none) | 32 | 46 / 31 (assigned) | KW09 light count 34.8 |
| DM5 | 42 | 23 (>25%) | 35 | 46 / 31 | |
| DL5 | 42 | 39 (none) | 43 | 48 / 42 (assigned) | |
| DA2 | 39 | 35 (<25%) | 48 | 48 / 42 | |
| DM1 | 68 | 86 (none) | 74 | 77 / 64 | |
| VM7d | 33 | 44 (<25%) | 36 | 23 / 30 | |
| VM2 | 37 | — (>25%) | 41 | 36 / 30 | |
| DM6 | 52 | 60 (none) | 58 | 36 / 21 (assigned) | Tobin 2017 EM: 53 |
| DL1 | 69 | 84 (none) | 83 | 75 / 52 | |
| DM2 | 54 | 79 (none) | 54 | 16 / 16 | |
| DA1 | 126 | 142 | 204 | 125 / 124.5 | male-biased (MaleCNS paper) |

- FlyWire: `cell_type` ORN_* rows of Schlegel et al. 2024's annotation table, both sides. Hemibrain: Schlegel 2021
  Supplementary file 3 (all "Traced"), truncation flags from file 2. MaleCNS: brainfly's `brain.npz` (2,635 ORNs, 53
  types; FlyWire 2,282).
- **Reading.**
  - EM agrees across sexes for DL5, DM1, VM7d, DM6 and VM2 within ±10%.
  - DM4 is the exception: MaleCNS 32 vs female 41 (FlyWire) or 60 (hemibrain). KW09's female light count (34.8) sits
    with the male value.
  - Grabe's light counts can miss badly: DM2 16 against 54-79 by EM (3-5×).
- MaleCNS paper (Berg et al. 2025, [PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)):
  - "Sorting glomeruli by the difference in male and female counts revealed a male bias in just 4/60 types (DA1, VA1v,
    VA1d and VL2a)." "For the remaining ORN types, there was good agreement between the numbers in female and male
    connectomes."
  - "Low resolution studies found volume differences in 3/4 Drosophila glomeruli highlighted above but no differences
    in numbers of receptor neurons". "Our examination of n=2 brains precludes statistical analysis".
  - "We observed a trend towards higher ORN and lower local interneuron (ALLN) input onto AL projection neuron (ALPN)
    in males but this was global and not specific to particular glomeruli". FAFB/FlyWire was "the outlier" in this
    comparison.
  - The male counts include fragments: "~70%" of receptor neurons were fully reconstructed.
- Mosca & Luo 2014: "sex-specific differences in synapse number for two glomeruli, DA1 and VA1lm, that coincide with
  known sex-specific differences in glomerular volume".

### 4.3 Sex differences in PN physiology
- General odors: Not reported. I found no study comparing male and female PN responses.
- Pheromones: Kohl et al. 2013: "First- and second-order olfactory neurons show identical pheromone responses,
  suggesting that sex genes differentially wire circuits deeper in the brain."
- MaleCNS: "dimorphism of second order neurons is thus extremely limited"; "Just 2/188 types are sexually dimorphic".
- Sex of the flies behind the numbers used here:
  - Females: KW08, KW09, GW09, Bhandawat 2007, Olsen 2007, N15, Nagel & Wilson 2016, Yaksi & Wilson 2010, Kazama et al.
    2011, Martelli & Fiala 2019, Rozenfeld 2023, Kim et al. 2015, and the Tobin 2017 EM brain.
  - Males: Jeanne & Wilson 2015 ("All experiments were performed in males"); Hong & Wilson 2015's shakB² experiments,
    which include the LN-activation sEPSC assay.
  - Not reported in the accessible text: Olsen & Wilson 2008, Olsen 2010, Gaudry 2013.

## 5. Models of the ORN→PN synapse plus PN (Q5)

### 5.1 Nagel, Hong & Wilson 2015
- **Synapse.** Fast component r = 0.23 spike⁻¹, τA = 1006 ms. Slow component fitted to disinhibited odor responses: r =
  0.0073, τA = 33,247 ms (orn_pn_depression.md §3.3).
- **Inhibition.** Presynaptic only. The resting divisor equals the LNs' resting rate in spikes/s (≈4-5), unscaled (§2.3).
- **PN.** Passive, conductance-based, E_leak −70 mV, 40 ORNs, VM7 ORN rates; no spikes.
- **Fits.** PN Vm responses to 20-ms and 2-s pulses and to pulse trains, with and without inhibition. It reproduces the
  resting disinhibition (≈7.5 vs 5-8 mV) and the observation that inhibition lowers baseline relative to the sustained
  response.
- **Not fitted.** Olsen's spike-rate transform. The resting drive (≈18 mV above leak) is ≈2× flies' (derived).
- Authors on their single-timescale variant: its assumptions "are incorrect" (orn_pn_depression.md §3.3).

### 5.2 Kao & Lo 2020, J Comput Neurosci 48:213 ([author PDF](https://webmail.life.nthu.edu.tw/~lablcc/publications/Lo-C-2020a.pdf); ModelDB 238959)
- Structure: "a scaled-down model of the AL, which contains 10 glomeruli. Each glomerulus is innervated by an ORN". LIF
  neurons, conductance synapses, presynaptic inhibition through terminal Ca²⁺ (power 3.5), short-term depression.
- Spontaneous LNs (SLNs): "SLNs fire spontaneously, without stimulus, and are turned off by the onset of an odor
  stimulus". "The default innervation strengths of SLNs in each glomerulus are proportional to the spontaneous firing
  rate of the ORN innervating that glomerulus."
- Rationale: "ORNs with higher levels of spontaneous activity require stronger SLN innervation to suppress the
  presynaptic activity." "Without the effect of GABA, ORN-to-PN synapses will become depressed before the odorant input
  and the frequency-dependent response decay will not occur."
- Calibration: fitted to Olsen's input-output form ("The power of 1.5 was pre-determined based on a previous study") and
  to odor-pulse-frequency data. ORNs at "8 spikes/s in the absence of an odor, on average".
- Not addressed: the resting Vm drive, the KW08/KW09 depression parameters, ORN convergence.
- This is the only published model with tonic presynaptic inhibition that scales with spontaneous ORN rate, i.e. the
  DL5 scenario (§3.2, candidate 1).

### 5.3 Liu, Li, Tang, Qin & Tu 2021, Front Comput Neurosci ([PMC8568954](https://pmc.ncbi.nlm.nih.gov/articles/PMC8568954/))
- Mean-field rate model: Tsodyks-Markram facilitation + depression at ORN→PN, presynaptic inhibition p = 1/(1 + ρ·R_LN).
  - "Without any presynaptic firing (R = 0), we have x = 1, u− = 0, and u+ = U at steady state." The rest state has no
    spontaneous input.
- Fits Olsen 2010's DL5 and VM7 data including public odors: "our model fails to fit experimental data without STP".
- Parameters (Table): DL5 ω_EE 160 nS, U 0.31, τD 368 ms, τF 339 ms; VM7 105 nS, 0.24, 160 ms, 150 ms.
- U ≈ 0.24-0.31 and net facilitation contradict KW08's p ≈ 0.79 and the depression data.

### 5.4 Others
- Jeanne & Wilson 2015 IF (weak_input_gain.md §5): no depression; Vrest −55, threshold −40 mV; first-spike latency
  near threshold only.
- Kim, Lazar & Slutskiy 2015 ([PMC4466247](https://pmc.ncbi.nlm.nih.gov/articles/PMC4466247/)): a phenomenological 2-D
  linear-nonlinear model of DM4 (ORN rate and its rate of change); no resting state.
- Olsen 2010 and Luo, Axel & Abbott 2010: the phenomenological Eq. 1.
- Gouwens & Wilson 2009: passive compartmental DM1 PN; the resting synaptic current is the assumed −15 pA (§1.1).
- **A model reproducing resting drive, resting depression and Olsen's transform together: Not reported.**

---

## What this means for brainfly (my reading)

1. **Add tonic inhibition at rest, in N15's form, before deepening depression.**
   - Make presynaptic inhibition proportional to the *total* GABAergic LN rate, so the resting 4.24 spikes/s already
     divides release. At present only the rate above rest counts.
   - Keep KW08's 6.19 mV as the uninhibited rested strength. KW08's p = 0.79 says their preparation had little or no
     tonic inhibition.
   - Calibration targets:
     - Silencing every ORN drops PNs ≈7-10 mV with inhibition intact (GW09; §1.6 per glomerulus).
     - Blocking inhibition at rest depolarizes PNs 5-8 mV (N15 Fig. 3b; DM6/VM2/VM7).
     - DM4's intact sEPSC stays within ≈25% of its 4-Hz deafferented uEPSC (D ≲ 2.6 with KW09-like depletion,
       ≲ 1.5 with M4).
     - DM1 PNs nearly silent at rest.
   - pn_toy.py's divisor of 2-2.5 is inside what the data allow for DM6/VM2/VM7-like glomeruli. Note that the tonic
     divisor also shrinks the *relative* step an odor's added inhibition makes (1 + kΔA/D_rest), which bears on the
     weak glomeruli an odor silences.
2. **Make it glomerulus-specific.** A uniform divisor cannot fit DM4 (≲2.6) and DM1 (needs ≈2× beyond DM4-like
   depression) at once. Hong & Wilson's GABA sensitivities exist for about 20 glomeruli, including DM6, VM2 and VM7,
   but not for DM4, DL5 or DM1. For DM1, Olsen's σ 45 → 13 with antagonists implies a weak-input divisor ≈3.3 (σ ratio).
3. **Use measured spontaneous ORN rates where they exist** (DM4 3.44, DM6 2.2, VM2 7.1, DL1 17.2, VM7d 10-13, DM1
   9-15, DL5 14-20, DA1 1.5). The basiconic median of 6 overstates DM4 by 1.7×; that alone explains much of DM4's
   excess drive (§1.6). But raising DL5 and DL1 to their rates worsens DL5 unless point 6 is solved.
4. **Shorten the PSP for low-Rin PNs** (DL5, probably DM4). brainfly's kernel integrates ≈34 ms per mV of peak against
   ≈22 ms for DL5's measured uEPSP. A per-glomerulus τm or kernel taken from KW08 Fig. 4C would cut those resting drives
   ≈1.5× at no cost to the peak.
5. **Check DM4's convergence.** MaleCNS has 32 ORNs against 41 (FlyWire) and 60 (hemibrain) in females. Elsewhere the
   sexes agree, so "use female counts" is not a general fix; it is a DM4-specific question (one male brain).
6. **DL5 stays open.** No measured mechanism lets its odor spikes count ≥3-5× more than its resting spikes.
   - The published candidate easiest to test is Kao & Lo's: tonic inhibition scaled to the glomerulus's spontaneous
     ORN rate and withdrawn at odor onset (Chou 2010's odor-inhibited pan-glomerular LNs).
   - Test it against DL5's points (5.1, 44) and (13.4, 85) with DL5's ORNs at 14-20 spikes/s.
   - Activity-dependent recovery is the other candidate.
7. **Diagnostics before building** (exploratory, as the project's other checks):
   - "GABA block at rest" in the model: does the uPN mean Vm rise 5-8 mV?
   - The deafferentation drop by glomerulus against §1.6.
   - DM1's resting rate against Gaudry's "close to zero".
   - DM4's sEPSC efficacy against 0.26.

## Sources

Primary physiology
- Gouwens NW, Wilson RI (2009). Signal propagation in *Drosophila* central neurons. *J Neurosci* 29:6239-6249.
  [PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/) (Figs. 7, 8 and the seal-model equation from the PMC
  page)
- Nagel KI, Hong EJ, Wilson RI (2015). Synaptic and circuit mechanisms promoting broadband transmission of olfactory
  stimulus dynamics. *Nat Neurosci* 18:56-65. [PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/);
  [Fig. 3](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/723d/4289142/0710edaedd1e/nihms642753f3.jpg);
  [Fig. 7](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/723d/4289142/4eb61c6ed1c7/nihms642753f7.jpg);
  [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnn.3895/MediaObjects/41593_2015_BFnn3895_MOESM98_ESM.pdf)
- Olsen SR, Wilson RI (2008). Lateral presynaptic inhibition mediates gain control in an olfactory circuit. *Nature*
  452:956-960. [PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/);
  [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnature06864/MediaObjects/41586_2008_BFnature06864_MOESM230_ESM.pdf)
  (Supp. Figs. 2, 4, 6)
- Olsen SR, Bhandawat V, Wilson RI (2007). Excitatory interactions between olfactory processing channels in the
  *Drosophila* antennal lobe. *Neuron* 54:89-103. [PMC2048819](https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/);
  [Fig. 2](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/6c54/2048819/d01df7eb8362/nihms22350f2.jpg)
- Olsen SR, Bhandawat V, Wilson RI (2010). Divisive normalization in olfactory population codes. *Neuron* 66:287-299.
  [PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/);
  [Supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0896627310002497-mmc1.pdf)
- Kazama H, Wilson RI (2008). Homeostatic matching and nonlinear amplification at identified central synapses.
  *Neuron* 58:401-413. [PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)
- Kazama H, Wilson RI (2009). Origins of correlated activity in an olfactory circuit. *Nat Neurosci* 12:1136-1144.
  [PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/);
  [Supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnn.2376/MediaObjects/41593_2009_BFnn2376_MOESM16_ESM.pdf)
- Gaudry Q, Hong EJ, Kain J, de Bivort BL, Wilson RI (2013). Asymmetric neurotransmitter release enables rapid odour
  lateralization in *Drosophila*. *Nature* 493:424-428. [PMC3590906](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/);
  [Fig. 2](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/8041/3590906/8b4271645492/nihms-420147-f0002.jpg);
  [Fig. 3](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/8041/3590906/fb6fe84f85e7/nihms-420147-f0003.jpg)
- Tobin WF, Wilson RI, Lee WCA (2017). Wiring variations that enable and constrain neural computation in a sensory
  microcircuit. *eLife* 6:e24838. [PMC5440167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/)
- Jeanne JM, Wilson RI (2015). Convergence, divergence, and reconvergence in a feedforward network improves neural
  speed and accuracy. *Neuron* 88:1014-1026. [PMC5488793](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/)
- Kazama H, Yaksi E, Wilson RI (2011). Cell death triggers olfactory circuit plasticity via glial signaling in
  *Drosophila*. *J Neurosci* 31:7619-7630. [PMC3119471](https://pmc.ncbi.nlm.nih.gov/articles/PMC3119471/)
- Yaksi E, Wilson RI (2010). Electrical coupling between olfactory glomeruli. *Neuron* 67:1034-1047.
  [PMC2954501](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/)
- Bhandawat V, Olsen SR, Gouwens NW, Schlief ML, Wilson RI (2007). Sensory processing in the *Drosophila* antennal lobe
  increases reliability and separability of ensemble odor representations. *Nat Neurosci* 10:1474-1482.
  [PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/);
  [Supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnn1976/MediaObjects/41593_2007_BFnn1976_MOESM22_ESM.pdf)
  (Supp. Fig. 2)

Inhibition and LNs
- Wilson RI, Laurent G (2005). Role of GABAergic inhibition in shaping odor-evoked spatiotemporal patterns in the
  *Drosophila* antennal lobe. *J Neurosci* 25:9069-9079. [PMC6725763](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/)
- Liu WW, Wilson RI (2013). Glutamate is an inhibitory neurotransmitter in the *Drosophila* olfactory system. *PNAS*
  110:10294-10299. [PMC3690841](https://pmc.ncbi.nlm.nih.gov/articles/PMC3690841/)
- Chou YH et al. (2010). Diversity and wiring variability of olfactory local interneurons in the *Drosophila* antennal
  lobe. *Nat Neurosci* 13:439-449. [PMC2847188](https://pmc.ncbi.nlm.nih.gov/articles/PMC2847188/)
- Silbering AF, Galizia CG (2007). Processing of odor mixtures in the *Drosophila* antennal lobe reveals both global
  inhibition and glomerulus-specific interactions. *J Neurosci* 27:11966-11977.
  [PMC6673347](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673347/)
- Nagel KI, Wilson RI (2016). Mechanisms underlying population response dynamics in inhibitory interneurons of the
  *Drosophila* antennal lobe. *J Neurosci* 36:4325-4338. [PMC4829653](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)
- Hong EJ, Wilson RI (2015). Simultaneous encoding of odors by channels with diverse sensitivity to inhibition.
  *Neuron* 85:573-589. [PMC5495107](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/)
- Root CM et al. (2008). A presynaptic gain control mechanism fine-tunes olfactory behavior. *Neuron* 59:311-321.
  [PMC2539065](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/)
- Martelli C, Fiala A (2019). Slow presynaptic mechanisms that mediate adaptation in the olfactory pathway of
  *Drosophila*. *eLife* 8:e43735. [PMC6581506](https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/)
- Mohamed AAM et al. (2019). Odor mixtures of opposing valence unveil inter-glomerular crosstalk in the *Drosophila*
  antennal lobe. *Nat Commun* 10:1201. [PMC6416470](https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/)
- Root CM, Ko KI, Jafari A, Wang JW (2011). Presynaptic facilitation by neuropeptide signaling mediates odor-driven food
  search. *Cell* 145:133-144. [PMC3073827](https://pmc.ncbi.nlm.nih.gov/articles/PMC3073827/) (abstract only)
- Ignell R et al. (2009). Presynaptic peptidergic modulation of olfactory receptor neurons in *Drosophila*. *PNAS*
  106:13070-13075. [PMC2722350](https://pmc.ncbi.nlm.nih.gov/articles/PMC2722350/) (abstract only)

Anatomy and sex
- Grabe V et al. (2016). Elucidating the neuronal architecture of olfactory glomeruli in the *Drosophila* antennal
  lobe. *Cell Rep* 16:3401-3413. [doi](https://doi.org/10.1016/j.celrep.2016.08.063);
  [Table S1](https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc1.pdf)
- Schlegel P et al. (2021). Information flow, cell types and stereotypy in a full olfactory connectome. *eLife*
  10:e66018. [PMC8298098](https://pmc.ncbi.nlm.nih.gov/articles/PMC8298098/);
  [Supplementary file 2](https://cdn.elifesciences.org/articles/66018/elife-66018-supp2-v2.csv);
  [Supplementary file 3](https://cdn.elifesciences.org/articles/66018/elife-66018-supp3-v2.csv)
- Schlegel P et al. (2024). Whole-body annotation and multi-connectome cell typing of *Drosophila*. *Nature*
  634:139-152. Annotation table:
  [flyconnectome/flywire_annotations](https://github.com/flyconnectome/flywire_annotations/blob/main/supplemental_files/Supplemental_file1_neuron_annotations.tsv)
- Berg S et al. (2025). Sexual dimorphism in the complete connectome of the *Drosophila* male central nervous system.
  bioRxiv 10.1101/2025.10.09.680999 (Cell 2026). [PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
- Mosca TJ, Luo L (2014). Synaptic organization of the *Drosophila* antennal lobe and its regulation by the Teneurins.
  *eLife* 3:e03726. [PMC4194450](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194450/)
- Kohl J, Ostrovsky AD, Frechter S, Jefferis GSXE (2013). A bidirectional circuit switch reroutes pheromone signals in
  male and female brains. *Cell* 155:1610-1623. [PMC3898676](https://pmc.ncbi.nlm.nih.gov/articles/PMC3898676/)
  (abstract)

Models
- Kao KW, Lo CC (2020). Short term depression, presynaptic inhibition and local neuron diversity play key functional
  roles in the insect antennal lobe. *J Comput Neurosci* 48:213-227.
  [doi](https://doi.org/10.1007/s10827-020-00747-4);
  [author PDF](https://webmail.life.nthu.edu.tw/~lablcc/publications/Lo-C-2020a.pdf);
  [ModelDB 238959](https://modeldb.science/238959)
- Liu Y, Li Q, Tang C, Qin S, Tu Y (2021). Short-term plasticity regulates both divisive normalization and adaptive
  responses in *Drosophila* olfactory system. *Front Comput Neurosci* 15:730431.
  [PMC8568954](https://pmc.ncbi.nlm.nih.gov/articles/PMC8568954/)
- Kim AJ, Lazar AA, Slutskiy YB (2015). Projection neurons in *Drosophila* antennal lobes signal the acceleration of
  odor concentrations. *eLife* 4:e06651. [PMC4466247](https://pmc.ncbi.nlm.nih.gov/articles/PMC4466247/)

Checked, nothing used beyond what is cited
- Fulterer A et al. (2018), *Cell Rep* 23:1259-1274 ([PMC6436828](https://pmc.ncbi.nlm.nih.gov/articles/PMC6436828/)), and
  Rozenfeld E et al. (2023), *Nat Commun* 14:2993 ([PMC10209050](https://pmc.ncbi.nlm.nih.gov/articles/PMC10209050/)):
  paired pulses and Unc13A/cacophony; neither splits by glomerulus.
- Raccuglia D et al. (2016), *eNeuro* 3:ENEURO.0080-16.2016 ([PMC4994068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4994068/)): no
  resting effects reported.
- Shimizu K, Stopfer M (2017) ([PMC5413558](https://pmc.ncbi.nlm.nih.gov/articles/PMC5413558/)): deafferented DA1
  lineage PNs (lateral_excitation.md).
- Wechsler SP, Bhandawat V (2025). bioRxiv 10.1101/2025.05.01.651725 (Or7a/DL5; abstract only).
