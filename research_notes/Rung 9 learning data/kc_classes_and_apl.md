# Kenyon cell classes, APL inhibition and MBON11: measured values

Read 2026-10-08. This file adds to `kenyon_cell_odor_responses.md` (Turner 2008's pooled values) and
`../Rung 4 resting state data/adaptation.md`, which already holds the per-class intrinsic rows for Groschner 2018,
Chen 2026, Turner 2008 and Greenin-Whitehead 2025. Values from those rows are repeated here only where a comparison
needs them. KC→MBON short-term plasticity is in `../Rung 4 resting state data/short_term_plasticity.md` §3.4.

Conventions:
- (fig.): read off a figure by eye, good to about ±10–20%.
- derived: my own arithmetic.
- [other insect]: not Drosophila.
- WC: whole-cell.
- LJP: liquid junction potential. Groschner and Chen corrected for it. Inada did not. Turner does not say.
- Classes: αβc/αβs/αβp are αβ core, surface and posterior.

## Summary: numbers for per-class thresholds and APL strength

1. **Threshold order is α′β′ < αβ ≤ γ in every lab.** α′β′ fire 5.5 mV below αβ in Inada (ex vivo, uncorrected: αβ ≈ −38.5, α′β′ ≈ −44, γ ≈ −36 mV, fig.) and about 13 mV below in Groschner (in vivo: αβc ≈ −38, α′β′ ≈ −51.5) and Chen (ex vivo: αβ −33, α′β′ −46, γ −22, fig.). Somatic R_in does not differ between classes ex vivo (Inada, p = 0.30), so the difference lies in spike generation, not input gain.
2. **The rest-to-threshold gap depends on how "rest" was set.** αβc: 8.2 mV in vivo (Groschner, rest measured at break-in, which they say is too depolarized). α′β′: about 0. Their ramp threshold sits 4–5 mV *below* the measured rest (fig.), and "one or two EPSPs" suffice. Pooled: 21.5 ± 5.6 mV from a −58 mV holding potential (Turner). At R_in ≈ 10 GΩ, 1 pA moves V by 10 mV (derived). Use within-lab class offsets, not absolute values.
3. **Firing above threshold (soma current injection; Inada, fig.).** At −30 mV: α′β′ ≈ 14, αβ ≈ 9, γ ≈ 4 Hz. At −20 mV: ≈ 23, 22, 18 Hz.
4. **Odor responses by class (in vivo WC).**
   - Spikes per response: α′β′ 4.9 ± 3.0, αβ 2.2 ± 1.2 (Turner).
   - Response probability (derived from Turner Fig. 2D): α′β′ ≈ 8.5–13.5%, αβ ≈ 3–8%, γ ≈ 2%. Only 1 of 15 γ KCs spiked to any odor.
   - αβc: 6.7% with a locust-style criterion, 18.6% with "≥1 spike on ≥3 trials" (Murthy).
   - αβp KCs get no PN input and are *inhibited* by odors (Perisse 2013).
5. **Blocking APL (population).**
   - KC Ca²⁺ rises ×2–3: "two to threefold" (Bergmann). In the α lobe, ΔF/F goes 0.24 → 0.72 with APL>TeTx (Lin, fig.).
   - Somatic population sparseness drops 0.97 → 0.86–0.89, and inter-odor r rises 0.10 → 0.22–0.23 (Lin, fig.).
   - Treves–Rolls activity ratio, a ≈ 1 − S (derived): ≈ 3% → ≥ 11–14%, about 4× more active cells.
   - No open-access paper reports a cell-counted fraction with vs without APL.
6. **Size of APL→KC inhibition.**
   - Optogenetic APL drive hyperpolarizes every KC tested. It saturates at ≈ −10 to −12 mV, equally for αβ, α′β′ and γ (Inada, fig., ex vivo).
   - αβc → APL → αβc lateral inhibition reaches −15 mV, with a mean of ≈ −5.5 to −7.5 mV for 50–2000 ms drive (Vrontou, fig., in vivo). It survives TTX.
   - GABA_A carries ≈ 40% and GABA_B ≈ 35% of it (Inada Fig. 5C, derived).
   - It lags excitation by "several hundred ms" and lasts about 1 s (fig.).
7. **Who recruits APL.**
   - Feedback onto the spiking KC itself (Inada, fig.): α′β′ ≈ −1.0 mV/spike, αβ ≈ −0.2, γ ≈ −0.15 mV/spike.
   - APL Ca²⁺ is linear in KC Ca²⁺: "APL = k*KC" (Bergmann).
   - KC→APL synapses outnumber PN→APL synapses 9.5:1 in the calyx and 36:1 overall.
   - Each αβc KC makes 13.4 synapses onto APL and receives 10.0 from it (Vrontou).
8. **APL release gain is unmeasured in flies.**
   - Non-spiking insect interneurons release transmitter with 2–5 mV of depolarization (Amin; Vrontou). APL's R_in is ~120 MΩ (Chen).
   - Locust GGN [other insect]: rest −51 ± 5 mV; odor responses peak 10–20 mV above rest; unitary KC→GGN EPSP 1 ± 0.5 mV.
   - More than 5 mV of GGN depolarization suppresses KC firing, and GGN releases GABA tonically at rest.
9. **MBON11 (MBON-γ1pedc>α/β) odor responses.**
   - 1-s odor at 2% saturated vapour: 118 ± 8.3 extra spikes in 0–1.4 s, ≈ 84 Hz above baseline (derived). The PSTH peaks at ≈ 130 Hz (fig.) (Hige 2015, in vivo WC).
   - 15-s odors: ≈ 8 → 60–65 Hz at onset, then a plateau of ≈ 20 Hz (Vrontou, fig.).
   - 5-s odors: +35 Hz on a ≈ 37 Hz baseline (Huang 2024, voltage imaging, fig.).
   - Whole-cell baselines are ≈ 3–10 Hz (fig.).
10. **Against brainfly's numbers** (as of odor_probe5/6, 2026-10-08, before later corrections; the current model is in experiments/odor_probe7.py).
    - The model's α′β′ fire too few spikes and αβ too many. A threshold 5–13 mV lower for α′β′ than for αβ is supported everywhere.
    - The model's αβ spike counts (3.6–7 vs 2.2) point to an αβ threshold that is too low, or to APL feedback that is too weak or too slow.
    - The model's MBON11 rise (5–17 Hz) is 2–17× below the measured 35–85 Hz. "≈ 20 Hz" is only the late plateau of 15-s odors.

---

## 1. Per-class KC excitability

### 1.1 Inada, Tsuchimoto & Kazama 2017, Neuron 95:357 ([PDF](https://kazamalab.riken.jp/pdf/Neuron_Inada_2017.pdf))

Preparation:
- **Ex vivo explant:** "The entire brain was removed from the head capsule".
- "All the experiments were conducted at room temperature (25 C)".
- "Voltages were uncorrected for the liquid junction potential."
- KCs "were held at around [−]60 mV by injecting a hyperpolarizing current unless otherwise mentioned". The minus sign is lost in the PDF text.
- Females, 3 days old. Class identity from biocytin fills.

Measured values:
- R_in: "Input resistance measured at soma is not significantly different between cell types (n = 24, 19, 33 for α/β, α′/β′, and γ KCs, respectively; p = 0.30, one-way ANOVA)". Means are ≈ 11, 11.5 and 9.5 GΩ (fig.).
- Excitability: "The rank order of excitability is α′/β′ to α/β to γ. n = 15, 10, 7". "α′/β′ KCs have the lowest firing threshold (n = 15, 10, 8 …; *p < 0.05, **p < 0.01)".
- Thresholds (fig. 2C): αβ ≈ −38.5, α′β′ ≈ −44, γ ≈ −36 mV, uncorrected. Derived gaps from the −60 mV hold: ≈ 21.5, 16 and 24 mV.
- Firing rate vs membrane potential (fig. 2B):

| Class | −40 mV | −30 mV | −20 mV |
|---|---|---|---|
| α′β′ | ≈ 4.5 Hz | ≈ 14 Hz | ≈ 23 Hz |
| αβ | ≈ 1.5 Hz | ≈ 9 Hz | ≈ 22 Hz |
| γ | ≈ 1 Hz | ≈ 4 Hz | ≈ 18 Hz |

- Summation: "All KC types integrate inputs from multiple PNs approximately linearly (slope = 0.89, 0.75, 0.86 for α/β, α′/β′, and γ KCs, respectively, n = 4, 5, 15)". Linear at every holding potential tested.
- Their interpretation: the excitability order "can account for the previously reported rank order of broadness of odor tuning, spontaneous firing rate, and odor-evoked firing rate (Turner et al., 2008)".

### 1.2 Groschner et al. 2018, Cell ([PMC5947940](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/))

Preparation: in vivo WC, 21–23 °C, LJP corrected. The values (fig. 2) are in `adaptation.md`:
- αβc: rest ≈ −46 (n = 96), threshold ≈ −38 (n = 93), R_in ≈ 11.6 GΩ, τ ≈ 188 ms. Sigmoidal f–I: ≈ 25 Hz at 5 pA, ≈ 30 Hz at 7 pA.
- α′β′: rest ≈ −47 (n = 14), threshold ≈ −51.5 (n = 13), R_in ≈ 6.8 GΩ, τ ≈ 118 ms. Linear f–I of ≈ 3 Hz/pA.

New quotes:
- On rest: "The most negative membrane potential recorded immediately after break-in … was taken to represent the resting potential. Because of the high input resistances of KCs …, the true resting potentials are likely to be more hyperpolarized."
- On thresholds: "Spike thresholds … were estimated by recording voltage responses to 600 ms current ramps, from –2 to +20 pA, starting at a membrane potential of –75 ± 2 mV."
- αβc gap: "the membrane potentials of αβc KCs … climbed in a stepwise fashion from resting potential to spike threshold, bridging the average potential difference of 8.2 mV by integrating 4–30 synaptic quanta". Also: "A large voltage difference (equal to the linear sum of six or seven coincident EPSPs) separates resting potential and spike threshold".
- α′β′ gap: "just one or two EPSPs could close the narrow voltage gap between the resting potentials and spike thresholds of α’β’ KCs".
- Spontaneous firing: "In contrast to the characteristic quiescence of αβc KCs at rest, many FoxP-negative α’β’ KCs … were spontaneously active at similar membrane potential baselines …, reflecting their lower action potential thresholds".
- Derived: the α′β′ ramp threshold (≈ −51.5) lies below the break-in rest (≈ −47), consistent with their spontaneous firing.
- Capacitance: "averaging 2.41 ± 0.07 pF (n = 81 cells)" for wild-type αβc KCs. τ/R_in gives ≈ 16 pF (derived), so the soma-measured C is far below whole-cell C.
- Current: "because KCs lack significant Ca2+ currents, no measures were taken to block Ca2+ channels".

### 1.3 Other in vivo KC recordings

**Turner, Bazhenov & Laurent 2008, J Neurophysiol 99:734** ([PDF](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf))
- "Input resistance at the soma was >10 GΩ; KCs were held at −58 ± 2 (SD) mV in current clamp. KCs showed abundant and mostly depolarizing PSPs in the absence of odor stimulation but very low spontaneous firing (0.1 ± 0.4 spike/s)."
- Fig. 3G gives the "difference between resting potential and threshold for odor-evoked spikes (21.5 ± 5.6 mV, n = 17 KCs)". The model used "the experimentally determined spike threshold Vth = −36.3 mV".
- −58 + 21.5 = −36.5, so the "resting potential" here is the −58 mV holding level (derived).
- Fig. 2E baseline rates (fig.): α′β′ ≈ 0.3 Hz, αβ and γ ≈ 0.02–0.05 Hz. "α′/β′ KCs had the highest baseline firing rate".

**Murthy, Fiete & Laurent 2008, Neuron** ([PMC2654402](https://pmc.ncbi.nlm.nih.gov/articles/PMC2654402/))
- One-day-old females, reared at 25 °C. "All cells were held between −55mV and −70mV". "only KCs with input resistances >10 GOhm … were used".
- Odor depolarization vs holding potential showed "good linear fits over the range between −40 and −100mV. This indicates that KC synaptic responses in this range are mainly affected by driving force, and not by voltage-dependent rectifying or amplifying non-linearities."

**Hige et al. 2015 Neuron** ([PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/))
- The 15-pA step "roughly corresponded to 1.5 times the average spike threshold current". Derived: threshold current ≈ 10 pA (ramp at 20 pA/s).
- Holding current for KCs "< 5 pA" (Hige 2015 Nature methods). At ~10 GΩ, that is a shift of up to ~50 mV (derived).

**Vrontou et al. 2021, Curr Biol** ([PMC8612741](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/)): αβc, in vivo, 21–23 °C.
- "Action potentials backpropagating from the axon initial segment of αβc KCs arrived at the somatic recording site with severely attenuated amplitudes of 1.95 ± 0.09 mV (mean ± SEM; n = 34 cells), barely larger than those of single excitatory postsynaptic potentials … (mean ± SEM = 1.25 ± 0.05 mV; n = 36 cells)".
- The 1.25 mV EPSP agrees with Turner's 1.4 mV unitary EPSP.

### 1.4 How many active inputs make a KC spike

- Gruntman & Turner 2013: about 4 of 5–7 claws (in the existing notes).
- Elkahlah 2020, as summarized by Ahmed et al. 2023 ([PMC10529417](https://pmc.ncbi.nlm.nih.gov/articles/PMC10529417/)): "Kenyon cells in wild type animals were very likely to be activated when at least three of their inputs were active, that two active inputs often sufficed, and that one active input could activate a Kenyon cell in certain conditions."
- Ahmed 2023 also favours "a consistent Kenyon cell firing threshold". In Tao-RNAi flies, whose KCs have more claws, "twice as many Kenyon cells responded to each odor".

### 1.5 αβ subtypes, α′β′ and γ subdivisions

- αβc: "the ∼160 αβ core (αβc) neurons" (Perisse 2013, [PMC3765960](https://pmc.ncbi.nlm.nih.gov/articles/PMC3765960/)). In vivo electrophysiology exists only for αβc (Groschner, Murthy, Vrontou).
- αβp: "The αβp neurons, which do not receive direct olfactory input from projection neurons in the calyx". Their "dendrites arborize in the sub-region of the MB calyx known as the accessory calyx, where no olfactory input has been reported" (Hige 2015 Nature, [PMC4860018](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860018/)).
- Not found: any intrinsic recordings of αβs, αβp, the α′β′ subtypes, or γd/γmain.

## 2. Per-class odor responses

### 2.1 In vivo whole-cell recordings

**Turner 2008 by class** (Fig. 2D/E; n ≈ 29 αβ, 26 α′β′, 15 γ counted from the histograms, fig.)
- Statistics: "α′/β′ KCs were more broadly tuned than the other two types (P < 0.05, 1-way ANOVA). Overall, a trend of decreasing responsiveness could be detected from α′/β′ to α/β to γ KCs, with statistically significant differences only between γ and α′/β′ KCs".
- γ: "Only 1 of the 15 γ KCs we tested with this odor set (and 1 of the 23 total γ KCs recorded at all odor concentrations) showed a spiking response to an odor, although all had detectable subthreshold responses."
- Spikes: "they [α′/β′] fired 4.9 ± 3.0 spikes during an odor response, significantly more than α/β KCs (2.2 ± 1.2; P = 0.007, t-test)".
- Response probability (derived from the Fig. 2D histograms, using bin lower edges and bin midpoints): α′β′ ≈ 8.5–13.5%, αβ ≈ 3–8%, γ ≈ 2%.
  - Check: the lower-edge version pools to ≈ 5%, against the reported 6 ± 5%.
- Class-averaged PSTH peaks (fig. 2E, averaged over all KC–odor pairs): α′β′ ≈ 1.0, γ ≈ 0.35, αβ ≈ 0.2 spikes/s.

**Murthy 2008, αβc (NP7175, L-LP clone)**
- Stimulus: 12 odors at 10⁻¹, 10⁻² and 10⁻³; 1-s pulses.
- Criterion: "at least one action potential in the period 0–2s following stimulus onset, on at least 3 trials".
- "The probability of response (percentage of odors eliciting a response) was 18.6% for the GFP+ L-LP KCs, compared to 49% for the GFP− KCs". The GFP− group is 12 αβ, 3 α′β′ and 3 γ.
- "using response criteria from a previous study on locust KCs …, the probability of response for the GFP+ L-LP KCs dropped to 6.7%".
- "so many (20/50) of the KCs in our data set showed no spiking response to any odors tested".

**Vrontou 2021, αβc on/off cells** (15-s MCH steps, in vivo)
- On cells: ≈ 1 → 10 Hz during the odor (n = 9).
- Off cells: ≈ 2 → 8 Hz at offset (n = 6) (fig. 2D/E).
- For long odors, αβc firing is sustained at low rate rather than 2 spikes.

### 2.2 Imaging

**Inada 2017** (GCaMP5 in all KCs, medial lobe tips, ethyl butyrate)
- Latency: "α′/β′ KCs start to respond earlier than the other two cell types (*p < 0.05 …; n = 7 flies)". Onset ≈ 210 ms for α′β′, ≈ 340 ms for αβ, ≈ 370 ms for γ at 10⁻¹ (fig.).
- Sensitivity: α′β′ responded at 10⁻⁹ and 10⁻⁷, where the others "remained nearly unresponsive".

**Perisse 2013** (GCaMP5, α-lobe tip): "Each odor evoked a robust, odor-specific positive response in αβscp, αβs, and αβc neurons … In contrast, the odors evoked a marked reduction of GCaMP5 fluorescence in c708a αβp neurons" (n = 4–5).

**Honegger, Campbell & Turner 2011, J Neurosci** ([PMC3180869](https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/))
- Preparation: GCaMP3/OK107, 22–25 °C rearing, 1:100 air dilution of saturated vapour, 1-s pulses, 25-s ISI.
- Criterion: >2.33 SD on more than half the trials.
- "an odor evokes responses in about 5% of the KCs in an imaging plane (n = 8 flies and n = 933 neurons) … The mean proportion of responding cells did not exceed 0.1 for any odor, although the response from individual flies reached values up to 0.17."
- "On any given odor trial, about 20% of KCs may be active".
- Mixtures: "Presented individually, each of these odors activates 9% of KCs on average. When presented simultaneously, however, this proportion increases only slightly (11%) and is smaller than the linear sum … 15%".
- Concentration: "the very first odor presentation of the experiment typically evoked the broadest response, regardless of the concentration". Banana stays under 0.2 across concentrations.
- Spike count (an aside): "KCs fire a small number of spikes, typically 5 to 10".

**Campbell et al. 2013, J Neurosci** ([PMC3685844](https://pmc.ncbi.nlm.nih.gov/articles/PMC3685844/)): overlap. Same preparation; 1:100.
- "a PA-responsive KC also responds to BA (64.6% of all PA-responsive KCs across recordings) and vice versa (63.1%), whereas EL-responsive KCs rarely respond to either of these odors (21.8%)".
- "KCs that respond uniquely to either PA (70 of 2756 total KCs; 2.5%) or BA (75 of 2756 total KCs; 2.7%)".

**Ahmed et al. 2023: the threshold changes the answer.** GCaMP6s, cut-off "a 20% increase in fluorescence", 1:100, 2-s pulses.
- "~50% of cells responded to 0 or 1 odor, and ~10–15% of cells responded to all 4 odors".
- This is far denser than the 5–6% from Honegger and Turner.

## 3. APL

### 3.1 What blocking or knocking down APL does

**Lin et al. 2014, Nat Neurosci** ([PMC4000970](https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/))
- Preparation: in vivo GCaMP3 (mb247-LexA), 5-s ethyl acetate pulses. shi^ts1 at 32 °C vs 22 °C, with unlabelled hemispheres as controls.

Lobe Ca²⁺:
- "In hemispheres where APL expressed dTRPA1, Kenyon cell odor responses were almost completely suppressed at 32 °C …, whereas in hemispheres where APL expressed shits1, Kenyon cell responses were greatly boosted".
- Fig. 4 α-lobe peak ΔF/F (fig.):

| Condition | Before | After |
|---|---|---|
| Control, 22 → 32 °C | 0.28 | 0.16 |
| APL>shi, 22 → 32 °C (n = 30 hemispheres / 21 flies) | 0.27 | 0.47 |
| APL>TeTx-inactive → TeTx (n = 9 / 7) | 0.24 | 0.72 |
| APL>dTRPA1, 22 → 32 °C | 0.18 | 0.04 |

- Derived, temperature-corrected shi effect: (0.47 / 0.27) / (0.16 / 0.28) ≈ 3×.

Somata (7 odors):
- "when either Kenyon cell or APL synaptic output were blocked by shits1 or TeTx, Kenyon cell odor responses became much broader and more similar".
- The index is pixel-based: S = [1 − (Σr/N)² / (Σr²/N)] / (1 − 1/N), with a 2σ pixel threshold.
- Fig. 5c/d values (fig.):

| Condition | Sparseness | Inter-odor r |
|---|---|---|
| APL>shi labelled, 22 → 32 °C | 0.97 → 0.89 | 0.10 → 0.23 |
| APL>TeTx, inactive → active | 0.97 → 0.86 | 0.09 → 0.22 |
| KC>shi, 22 → 32 °C | 0.93 → 0.82 | 0.14 → 0.24 |
| Controls | 0.95–0.98 | 0.06–0.13 |

- Derived: for all-or-none responses the active fraction is a = 1 − S(1 − 1/N) (≈ 1 − S for many pixels; corrected from (1 − S)(1 − 1/N), which differs by about 1/N). Graded responses make this a bound, not a count. So ≈ 3% active → ≈ 11–14% with APL blocked, if responses were all-or-none.

Odor dependence: the increase "was greater for the IA:EB mixtures than for δ-DL … supporting the idea that inhibitory feedback is driven by overall Kenyon cell activity". Blocking APL did not change δ-DL's sparseness.

Which KCs drive APL (Fig. 2 legend):
- "blocking αβ neurons slightly increases odor responses only in the α lobes"
- "blocking α′β′ neurons does not affect odor responses"
- "blocking γ neurons does not affect odor responses"
- Only blocking all KCs gives the large increase.

GAD RNAi:
- APL>GAD-RNAi responses "were modestly higher in the α′ lobe …, but not the α lobe".
- "APL>GADRNAi had no effect on population sparseness".
- So partial loss of GABA affects α′β′ first.

**Other manipulations**
- Bergmann et al. 2026 ([PMC13039246](https://pmc.ncbi.nlm.nih.gov/articles/PMC13039246/)): "silencing APL increases KC GCaMP responses by two to threefold". APL>Ort plus histamine "drastically increased KC odour responses".
- Amin et al. 2020 ([PMC7541083](https://pmc.ncbi.nlm.nih.gov/articles/PMC7541083/)): histamine on APL>Ort "strongly increases Kenyon cell odor responses (as strongly as blocking APL synaptic output with tetanus toxin)".
- Lei et al. 2013, BBRC (abstract only; paywalled): "the down-regulation of GABAA but not GABAB receptors in KCs reduced the sparseness of odor representations in the MB, as shown by an increase in the population response probability and decrease in the odor selectivity of single KCs". Lowering GABA synthesis in APL did the same. The numbers are not in the abstract.
- Liu, Krause & Davis 2007, Neuron (abstract): "Rdl overexpression abolished the normal calcium responses of the MBs to odors while Rdl knockdown increased these responses."
- Inada 2017: picrotoxin plus CGP54626 "increases both response amplitude (mean ΔF/F) and trial-to-trial variability (standard deviation) in all cell types". It "narrow[s] the dynamic range … in α′/β′ KCs". Disinhibition at low concentrations "was particularly prominent in α′/β′ KCs".
- Chen et al. 2026 ([PMC13075853](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/)): sleep loss, via a larger SK-mediated AHP in APL, gave "a greater number of Kenyon cells responding to each odor". Population sparseness 0.94 → 0.90 (fig. 2D; NS n = 18, SD n = 13). Derived: a ≈ 6% → 10%. KC intrinsic properties were unchanged.
- Prisco et al. 2021 ([PMC8741211](https://pmc.ncbi.nlm.nih.gov/articles/PMC8741211/)): with APL output blocked by TNT, KC claw (homer::GCaMP3) responses follow PN bouton strength. With APL intact they are normalized: Mch vs Oct claw peaks are not different, while PN boutons differ.
- Mittal et al. 2020 ([PMC7039968](https://pmc.ncbi.nlm.nih.gov/articles/PMC7039968/)): APL>TNT "showed significantly more stereotypy" of total KC responses across flies.

### 3.2 APL's own odor response (no voltage recording in flies)

- **Driven by KCs.** "Thermal activation of Kenyon cells caused large increases in GCaMP3 and spH signals emitted by APL". Mean ± s.e.m.: "GCaMP3, mb247-LexA>dTRPA1, 1.90 ± 0.44 … spH, mb247-LexA>dTRPA1, 0.68 ± 0.09" (n = 5). The odor response is "blocked at the restrictive temperature" when KC output is blocked (Lin 2014).
- **Linear in KC activity.** "we did not observe consistent deviations from linearity, so we chose the most parsimonious model …: a linear relationship, or APL = k*KC" (Bergmann 2026, dual-colour Ca²⁺ imaging, 7 odours, 5-s pulses).
- **Lobe-specific at low strength, global at high strength** (Inada 2017, GCaMP6s, n = 6 flies). There were "Ca2+ responses in the β′ lobe even to low concentrations of odor (10⁻⁹ and 10⁻⁷), which only evoked negligible responses in the other two lobes". At 10⁻¹, ΔF/F ≈ 0.7 in β and γ and ≈ 1.4 in β′ (fig.).
- **Scales with PN input in the calyx** (Prisco 2021, GCaMP6m, 5-s odours at 1:100, n = 10). "Δ(Oct-Mch) = 45% ± 27%; Δ(Oct-δ-DL) = 76% ± 30%". The correlation with PN activity is "= 0.95".
- **Local.** "local stimulation of APL with P2X2 + ATP decayed to undetectable levels within as little as 100 µm". At a normalized λ = 50 µm, KCs inhibit themselves more than other single KCs ("the median imbalance is ~40%") (Amin 2020).
- **Graded, with few Na⁺/Ca²⁺ channels.** "voltage-gated Na+ and Ca2+ channels are expressed at lower levels in APL than in all other types of mushroom body neurons". Also: "as little as 2 mV depolarization can modulate neurotransmitter release in non-spiking insect interneurons" (Amin 2020).
- **Ex vivo electrophysiology.** "APL neurons are non-spiking and exhibit graded responses to somatic current injection". R_in is "∼120 MΩ", with a spikelet-like "bump" on strong depolarization (Chen 2026; see `adaptation.md`).
- **Odor and shock** both raise APL Ca²⁺ and spH release. After pairing, APL "showed a significant decrease in response towards the trained odor, but not the control odor" (Liu & Davis 2009, [PMC2680707](https://pmc.ncbi.nlm.nih.gov/articles/PMC2680707/)).

### 3.3 APL→KC inhibition in mV

**Inada 2017** (ex vivo, KC whole-cell)

APL driven directly (CsChrimson in APL):
- Responses "were mediated by both GABAA and GABAB receptors … and, critically, similar in strength between all types of KCs". "inhibition was observed in every single KC we examined".
- Saturating hyperpolarization (fig. 5D/E): ≈ −10 to −12 mV for all classes. Offset parameter p = 0.92, gain p = 0.72; n = 5, 8 and 9 KCs.
- Normalized response (fig. 5C): saline 1, PTX ≈ 0.6, PTX + CGP ≈ 0.25 (n = 10). Derived: GABA_A ≈ 40%, GABA_B ≈ 35%, remainder ≈ 25%.

Feedback from one KC's own spikes:
- "activation of single KCs recruits a hyperpolarizing offset response, but unexpectedly, only prominently in α′/β′ KCs".
- Slopes (fig. 4C), from 3–15 spikes in 500 ms, measured 500 ms after the step: α′β′ ≈ −1.0 mV/spike, αβ ≈ −0.2, γ ≈ −0.15 (n = 15, 19, 19). That is ≈ −10 mV after 15 α′β′ spikes.
- The feedback is abolished by TTX and cut by PTX + CGP, and by Arch in APL.
- Conclusion: "cell-type specificity of inhibition originates in the ability of α′/β′ KCs to activate APL neuron more strongly".

Lateral inhibition from PNs (Mz19 PNs, optogenetic):
- In KCs not connected to those PNs, offset responses range 0 to −10 mV (fig. 3E, n = 19). About half got none: "Some KCs were almost not hyperpolarized at all, suggesting that the inhibition is effective locally".
- PTX + CGP: ≈ −5.7 → −2.5 mV (n = 10, fig.).
- ACh iontophoresis in the calyx: ≈ −2.9 → −0.7 mV with Arch in APL (n = 7, fig.).
- Timing: "Inhibition followed excitation by several hundred ms and were often strong enough to override the initial depolarization".

**Vrontou 2021** (in vivo, αβc KCs)
- With CsChrimson in a random subset of αβc KCs, GFP+ (CsChrimson-negative) αβc KCs "showed deep, photon dose-dependent hyperpolarizations of up to 15 mV below the membrane potential baseline". "Picrotoxin blocked the inhibitory response".
- Means by light duration (fig. 7B):

| Light | 8 ms | 50 ms | 500 ms | 2000 ms |
|---|---|---|---|---|
| Hyperpolarization | ≈ −2 mV | ≈ −5.5 mV | ≈ −7 mV | ≈ −7.5 mV |

  n = 7–8; −0.3 to −2 mV with picrotoxin.
- It needs no spikes: "the light-induced hyperpolarizations of CsChrimson-negative αβc KCs persisted unabated when action potentials were blocked with TTX".
- Time course (fig. 7C): peak ≈ −10 mV within ≈ 0.2 s, recovery over ≈ 1 s.
- Release threshold: "in GGN and other non-spiking interneurons, depolarizations of 2–5 mV suffice to trigger secretion".

**Turner 2008:** subthreshold odor responses "could be depolarizing, hyperpolarizing or consist of" both. No mV values are given.

### 3.4 Wiring numbers

- "each αβc KC excites APL through an average of 13.4 synapses—that is, roughly one contact per 20 μm of dendrite—and is inhibited by APL via 10.0 reciprocal synapses" (Vrontou 2021).
- "KC>APL synapses outnumber PN > APL synapses by 9.5:1 in the calyx and 36:1 overall" (Bergmann 2026).
- "Out of the 136 PNs reported innervating the main calyx, 126 made and received synapses with APL" (Prisco 2021).
- "α/β KCs receive more inhibitory synapses along their dendritic trees compared to γ and α’/β’, where the majority of synapses received from the APL is localized on KC claws instead" (Prisco 2021).

### 3.5 [other insect] The locust GGN, APL's analogue

- Papadopoulou et al. 2011, Science ([PMC3242050](https://pmc.ncbi.nlm.nih.gov/articles/PMC3242050/)), in vivo sharp electrodes, 80 recordings:
  - "GGN, is a non-spiking neuron with a resting potential of −51 ± 5 mV." Odor depolarization "grew with stimulus concentration (tested over a million-fold) with a peak depolarization of 15 - 20 mV above rest".
  - "Unitary EPSPs were 1 ± 0.50 mV (n = 11 KCs), with some nearing 2 mV."
  - "In every pair, GGN depolarization beyond 5mV reduced current-evoked firing of the recorded KC." Activating GGN through KCs "was nearly twice as effective as via direct current injection".
  - Hyperpolarizing GGN enhanced the LFP, "indicating graded release of GABA at rest".
- Ray, Aldworth & Stopfer 2020, eLife ([PMC7145415](https://pmc.ncbi.nlm.nih.gov/articles/PMC7145415/)): "strong odor stimuli depolarize GGN by about 10 mV in recordings made near the base of the α lobe branch". The model attenuates this to ~5–9 mV in the calyx.

## 4. MBON11 (MBON-γ1pedc>α/β, MVP2) odor responses in vivo

**Hige, Aso, Modi, Rubin & Turner 2015, Neuron** ([PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/))
- Preparation: in vivo whole-cell or cell-attached. "cells were held at around -60 mV by injecting hyperpolarizing current (< 50 pA)".
- Odors: saturated vapour air-diluted "down to 1% (odor generalization experiments) or 2% (the rest of the experiments)", 1 L/min. 1-s pulses, 25-s ISI.
- Response: "MBON-γ1pedc responded to our two test odors, 3-octanol (OCT) and 4-methylcyclohexanol (MCH), with high spike rates that persisted throughout the duration of the 1-s odor pulse".
- Counts: OCT "118 ± 8.3 spikes", MCH "110 ± 11 spikes" (n = 7). "Odor-evoked spikes were counted within the time window of 0 to 1.4 sec from odor onset. Spontaneous spiking rates were subtracted." Derived: ≈ 84 and 79 Hz above baseline averaged over 1.4 s.
- PSTH (fig. 1E): OCT peaks ≈ 130 Hz at ≈ 0.3 s and falls to ≈ 70 Hz by 1 s; MCH peaks ≈ 100 Hz; baseline ≈ 5–10 Hz.
- Currents: "large odor-evoked EPSCs that typically exceeded 200 pA in amplitude and were sustained throughout the duration of the odor pulse".

**Vrontou 2021** (in vivo WC, 21–23 °C, odors at 1–20 ppm)
- Baseline: MBON-γ1pedc>αβ shows "persistent irregular spiking or bursting".
- Optogenetic drive of αβc KCs alone, about 160 cells (fig. 1H, n = 6): ≈ 3 → 40 Hz. With TTX, membrane potential ≈ −48 → −42 mV.
- 15-s odors (fig. 2B, n = 33):
  - Baseline ≈ 8 Hz.
  - On response ≈ 60–65 Hz at ≈ 0.5 s.
  - Decay to ≈ 20 Hz within a few seconds.
  - Off peak ≈ 25–30 Hz.
- The authors: rates "declined and stabilized at slightly (MBON-α2sc) or moderately elevated plateaux (MBON-β1>α and MBON-γ1pedc>αβ) before rising again to a second peak at the end of the pulse". The on and off peaks are attributed to on and off αβc KCs.

**Huang et al. 2024, Nature** ([PMC11525173](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525173/)): pAce voltage imaging on a trackball, no current injection, n = 20 flies.
- Spontaneous ≈ 37 Hz (fig. 1e; 37.2 ± 2.0 Hz in `adaptation.md`), burst ratio ≈ 45% (fig.).
- 5-s attractive odors (ACV, 1% ethyl acetate): +35 Hz (CS+) and +25 Hz (CS−) before training (fig. 3f).
- After training: "Depressions of CS+-evoked responses endured for less than 1 h in MBON-γ1pedc>α/β neurons".

**Perisse et al. 2016, Neuron** ([PMC4893166](https://pmc.ncbi.nlm.nih.gov/articles/PMC4893166/)): GCaMP6f, MB112C.
- Inputs: "Dendrites of MVP2 neurons … innervate the γ1 region and more densely innervate the αβs than the αβ core (αβc) region … MVP2 are therefore likely to be primarily driven by αβs KCs."
- Hunger: "Peak responses to MCH, OCT, ethyl acetate (EA), and pentyl acetate (PA) were all significantly greater in starved versus satiated flies."
- It is GABAergic and inhibits M4/6, not V2.

**Hige 2015 Nature:** MBON-γ1pedc Ca²⁺ responses are slow. "three MBONs (β1, γ1pedc, and γ4) that have axonal terminals in the MB lobes show slower time courses".

**How many KC spikes drive MBON11:** not measured.
- Activating ~160 αβc KCs optogenetically gives ≈ 40 Hz (Vrontou).
- The only unitary KC→MBON measurement is for α2sc: ≈ 0.1–0.2 mV steps, 5 of 24 pairs monosynaptic (fig.; Hige 2015 Nature; see `short_term_plasticity.md`).

## 5. For brainfly

- **Per-class thresholds.** Lower α′β′ by 5–13 mV relative to αβ. Set γ at or above αβ: 0 mV (Inada) to +11 mV (Chen).
  - Groschner's α′β′ sit at threshold. With rest held about 21.5 mV below the αβ threshold (Turner-style), α′β′ would be ≈ 8–16 mV below their own threshold.
  - This lifts α′β′ spike counts toward 4.9 and response probability toward 8–14%.
- **αβ.** 3.6–7 spikes against 2.2 and 3–8% responders suggests a slightly higher αβ threshold, or APL feedback that arrives sooner. In flies the inhibition lags by hundreds of ms, so it mainly trims late spikes.
- **APL strength targets** (fit, not measured gains):
  1. With all KCs driven, inhibition of non-responding KCs should reach about −7 to −15 mV (Vrontou; Inada's saturating −10 to −12 mV).
  2. Removing APL should multiply KC Ca²⁺-like activity 2–3× and raise the responding fraction about 4×, from ≈ 3–6% to ≥ 11–14% (Lin).
  3. Inhibition onto α′β′ and αβ should be equal per unit of APL activity (Inada).
  4. α′β′ should excite APL ~5× more per spike, or simply fire more.
  5. Graded release should start at ~2–5 mV of APL depolarization and saturate by ~10–20 mV (GGN range).
- **MBON11 target.** First-second odor response ≈ 35–85 Hz above baseline, depending on concentration (2% saturated vapour gives ≈ 84 Hz). A 15-s odor falls to a ≈ 20 Hz plateau within seconds.
  - Spontaneous rate is ≈ 37 Hz without current injection.
  - `adaptation.md` gives ≈ 9 mV of bias for 37 Hz.

## 6. Conflicts and gaps

**Absolute rest and threshold.**
- Rest: −46 mV (Groschner, break-in, "likely to be more hyperpolarized") vs −58 mV held (Turner) vs −55 to −65 mV (Chen, ex vivo, fig.).
- Threshold: −33 to −38.5 mV for αβ across labs, but LJP handling differs. A K-aspartate LJP of ~13 mV would move the uncorrected Inada and Turner values (derived caveat).
- R_in also differs 10× between labs for γ (≈ 9.5 GΩ Inada vs ≈ 1.5 GΩ Greenin-Whitehead; see `adaptation.md`).
- Only within-lab class differences are reliable.

**γ threshold.** It equals αβ in Inada (−36 vs −38.5, uncorrected) but is 11 mV higher in Chen (−22 vs −33). Turner's γ KCs almost never spiked to odors (1 of 15), yet γ lobes give clear Ca²⁺ responses at high concentrations (Inada Fig. 8A).

**Spikes per response.** Turner: 2.2 (αβ) and 4.9 (α′β′) in 2 s. Honegger: "typically 5 to 10", with no source given. Vrontou: on-αβc KCs fire ≈ 10 Hz throughout 15-s steps. Odor duration, concentration and criterion all differ.

**Response probability depends on the criterion.**
- αβc: 18.6% vs 6.7% on the same data (Murthy).
- Calcium imaging: 5% (2.33 SD, reliability; Honegger) vs about half of all cells responding to ≥ 2 of 4 odors (fixed 20% ΔF/F; Ahmed).
- Single-trial activity is ≈ 20% (Honegger).

**α′β′ and APL.**
- Inada: α′β′ KCs recruit APL most, and APL activity starts in β′.
- Lin 2014: blocking α′β′ output alone "does not affect odor responses"; only blocking all KCs disinhibits strongly.
- Both may hold if APL is driven by summed activity and acts locally.

**Local vs global inhibition.** Lin treats APL as global feedback. Inada, Amin and Prisco show local or compartment-restricted inhibition, with self-inhibition favoured ~40% at λ = 50 µm. A single-compartment graded APL in brainfly is a simplification.

**MBON11 spontaneous rate.**
- ≈ 3–10 Hz whole-cell (Hige, Vrontou; cells held or dialysed) vs ≈ 37 Hz by voltage imaging (Huang).
- Hige's MBON was held at −60 mV with < 50 pA, which suppresses the baseline.
- `adaptation.md` already flags this.

**Gaps (not found in open full text):**
- A cell-counted fraction of responding KCs with vs without APL. Lei 2013 may have it but is paywalled.
- APL membrane potential during odors in flies, and APL release gain (Hz or GABA per mV).
- Unitary KC→APL EPSPs in flies (locust: 1 ± 0.5 mV) and unitary APL→KC IPSPs.
- Short-term plasticity of KC↔APL synapses.
- Intrinsic properties of αβs, αβp, the α′β′ subtypes and γd.
- Per-class APL inhibition in vivo (Inada's equal-strength result is ex vivo).
- The number of KC spikes needed to drive MBON11, and the unitary KC→MBON11 EPSP.
- Temperature: all of the above is at 21–25 °C.
