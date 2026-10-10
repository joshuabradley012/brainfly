# MBON11 (MBON-γ1pedc>α/β, MVP2): measurements to set and test the Kenyon cell → MBON11 weight

Read 2026-10-09. Full texts came from PMC (NCBI efetch, JATS XML) and were searched in full, figure legends included.
Figures were read from the PMC images (800 px wide for the 2015 papers), by eye and by measuring pixels against the
axis ticks or scale bars. Hemibrain counts were computed from the public hemibrain v1.2 traced-adjacency export
(`exported-traced-adjacencies-v1.2.tar.gz`, Janelia, Dec 2020).

Conventions:
- (fig., approx.): read off a figure. Good to about ±10–20%, worse for the 800-px 2015 figures.
- (derived): my own arithmetic, shown inline.
- [other insect]: not Drosophila.
- "Not reported": I searched the full text and legends and it isn't there.
- VC/CC: voltage clamp / current clamp. KC: Kenyon cell. STA: spike-triggered average.

## Summary

1. **Nobody has measured MBON11's input resistance, time constant or capacitance, or a unitary KC→MBON11 EPSP.**
   The only MBON with passive properties is MBON-α3: Rm 926 MΩ, τm 16 ms, C 16.8 pF (ex vivo).
2. **MBON11 itself has been measured in four ways.**
   - Spikes and EPSCs to odors (Hige 2015 Neuron).
   - Optogenetic population EPSCs: about 80–117 pA from a 1-ms flash onto about 3–7% of γ KCs, ex vivo (Yamada 2024).
   - Optogenetic αβc KC drive in vivo: firing about 2.5 → 40 Hz, and +6.5 mV in TTX (Vrontou 2021).
   - In vivo current steps, giving an F–I slope of 0.35–0.47 Hz/pA (derived from Wang 2026 Source Data).
3. **The odor response.** Hige 2015 Neuron's counts are 118 ± 8.3 (OCT) and 110 ± 11 (MCH) spikes in 0–1.4 s,
   spontaneous rate subtracted, n = 7, at 2% saturated vapour, with the cell held at −60 mV by < 50 pA.
   - PSTH peak about 135–140 Hz at about 0.3 s, then about 95 Hz at 1 s (fig., approx.).
   - Mean odor EPSC about 400 pA peak and about 170 pA sustained; charge about 250–265 pC in the same window
     (fig., approx., n = 5).
   - In the same paper and protocol, **MBON-α2sc fired ≈ 71–85 spikes** (fig., approx.).
4. **The only unitary KC→MBON measurement is KC→MBON-α2sc** (Hige, Aso, Rubin & Turner 2015 Nature). It was paired
   in vivo whole-cell, **in 100 µM mecamylamine**.
   - First-spike EPSPs: mean ≈ 0.25 mV, range ≈ 0.14–0.45 mV across the 5 monosynaptic pairs (fig., approx.,
     Extended Data Fig. 9d).
   - Only 5 of 24 pairs were monosynaptic, although EM shows every passing α/β KC synapses onto α2sc.
   - 100 µM mecamylamine strongly reduces KC→MBON transmission (Barnstedt), and 10 µM halves the γKC→MBON11 EPSC
     (Yamada). The α2sc unitary EPSP is therefore probably an underestimate. Takemura 2017 says so explicitly.
5. **Hemibrain v1.2, derived.**
   - MBON11_R gets 22,647 KC synapses from 1,694 KCs (13.4 per KC), 86% of its input.
   - 63% of those synapses come from γ KCs, 37% from α/β.
   - MBON-α2sc_R gets 10,888 from 885 KCs (12.3 per KC).
   - MBON11 is ≈ 2.1–2.2× α2sc by synapse totals.
6. **Electrotonic structure.** No compartmental model of MBON11 exists.
   - Yamada chose MBON11 because its "relatively thick and short primary neurite" gives good space clamp.
   - Its somatic spikes are large: ≈ 20–27 mV (fig., approx.), against 4.3 mV in MBON-α3.
   - The one modelled MBON (α3) is electrotonically compact.
   - Nothing suggests MBON11 attenuates single-KC EPSPs beyond what its size implies.

---

## 1. MBON11 passive and active properties

**Not reported anywhere I found: input resistance, membrane time constant, capacitance.**

Papers checked: Hige 2015 Neuron, Hige 2015 Nature, Vrontou 2021, Yamada 2024, Wang 2026.
- Perisse 2016 and Pavlowsky 2018 are calcium imaging and anatomy only.
- Takemura 2017 has no MBON11 physiology.
- Huang 2024 is voltage imaging, with no passive properties.

### What exists

**Holding and leak (no Rin derivable).**
- Hige 2015 Neuron (in vivo, CC): "In current-clamp recordings, cells were held at around -60 mV by injecting
  hyperpolarizing current (< 50 pA)."
- Yamada 2024 (ex vivo, VC, Cs⁺/QX-314 internal): "Cells were held at −60 mV. Leak current was typically < 150 pA."
  Without the cell's zero-current potential under Cs⁺, this doesn't give an input resistance.

**Resting potential.**
- Vrontou 2021, Fig. 1H, in TTX, "+TTX" dark bar: ≈ −48.5 mV. Individual cells ≈ −43.5, −46, −47, −47.5, −50 and
  −56 mV, n = 6 (fig., approx.).
  - In vivo, 21–23 °C, K-aspartate internal. No liquid-junction correction is stated.
  - Inclusion rule: "Only cells with a measured resting potential below –30 mV and a spiking response to depolarizing
    current injections were characterized further."
- Wang et al. 2026 (Nat Commun; males; in vivo), Source Data for Supp. Fig. 8f, "Pre puff": −49.3 ± 5.8 mV
  (mean ± SD, n = 11, range −56.6 to −40.2) (derived from the 11 listed values).
  - Caveat: they recorded "in current-clamp mode, with bridge balancing and holding currents ranging from 0 to 100 pA
    to compensate for current leakage". So these values may include holding current.

**Spontaneous firing.** It depends on the method.
- Hige 2015 Neuron, Fig. 1E: pre-odor PSTH ≈ 6 Hz (fig., approx., n = 7). Cells were held with < 50 pA
  hyperpolarizing current.
- Vrontou 2021: MBON-γ1pedc>αβ shows "persistent irregular spiking or bursting".
  - Fig. 1H dark rate ≈ 2.5 Hz; individual cells 0, 0, 0, 0, ≈ 7 and ≈ 10 Hz; n = 6 (fig., approx.).
  - Fig. 2B pre-odor ≈ 7–8 Hz, n = 33 (fig., approx.).
- Huang 2024, pAce voltage imaging, no electrode, flies walking on a trackball: 37.2 ± 2.0 Hz, n = 20 (Source Data;
  see `../Rung 4 resting state data/rung4_data.md`).
- (derived) With the F–I slope below (0.35–0.47 Hz/pA), Hige's < 50 pA hold alone could remove up to about 18–24 Hz.
  This assumes the slope extends below the measured range. It would reconcile the whole-cell ≈ 3–8 Hz with the imaged
  37 Hz, but no paper makes this argument.

**F–I relation (Wang 2026; in vivo whole-cell, males).**
- Methods: "neurons were stimulated with 5 pA increments from −40 pA to 105 pA in current injection steps. Each step
  had a duration of 300 ms, with 3 s intervals between steps."
- Source Data gives rates for 40–105 pA. Rates are spikes per 300 ms step, quantized at 3.33 Hz. All of the following
  is derived from Source Data:

| Group (sheet) | n | Mean rate at 40 / 70 / 105 pA | Per-cell slope, mean (range) |
|---|---|---|---|
| Hungry (Fig. 6o) | 8 | 13.7 / 26.7 / 42.9 Hz | 0.47 Hz/pA (0.36–0.58) |
| Fed (Fig. 6o) | 4 | 8.3 / 20.0 / 30.8 Hz | 0.35 Hz/pA (0.16–0.44) |
| Before dopamine puff (Fig. 7l) | 5 | 24.0 / 37.3 / 51.3 Hz | 0.43 Hz/pA (0.36–0.47) |
| After dopamine puff (Fig. 7l) | 5 | 18.0 / 32.0 / 42.7 Hz | 0.36 Hz/pA (0.27–0.41) |

- Several cells fired 0 Hz at 40 pA. Steps are relative to whatever holding current was applied.
- Text: "We observed more evoked spikes in hungry males compared to fed males under the same current injection
  conditions". Also: "Dopamine reduces evoked action potentials across all currents".

**Somatic spike size.**
- Hige 2015 Neuron, Fig. 1D example cell: spontaneous spikes rise ≈ 25–27 mV from baseline. Odor-evoked spikes are
  ≈ 20–24 mV riding on the depolarization (fig., approx.; the 20-mV scale bar is ≈ 16.5 px).
- For comparison, MBON-α3 ex vivo: "The amplitude of action potentials was rather small (4.3±0.029 mV) ... The small
  amplitudes are likely a result of the unipolar morphology of the neuron with a long neurite connecting the dendritic
  input region to the soma" (Hafez 2023).

**Another MBON, for scale: MBON-α3, ex vivo, n = 5 (Hafez et al. 2023 eLife).**
- "the average resting membrane potential as -56.7±2.0 mV"
- "spontaneous firing activity of MBON-α3 with an average frequency of 12.1 Hz"
- "τm=16.06±2.3 ms"
- "Rm=926±55 MΩ, a rather high membrane resistance when compared to similarly sized neurons"
- "Cm=16.76±1.90 pF, which classifies MBON-α3 as a mid-sized neuron"

**Hunger and dopamine.**
- Perisse 2016 (imaging): "Peak responses to MCH, OCT, ethyl acetate (EA), and pentyl acetate (PA) were all
  significantly greater in starved versus satiated flies" (quote from `kc_classes_and_apl.md`).
- Wang 2026 attributes the hunger effect to excitability: shorter first-spike latency and smaller AHP.
- Hige's flies were fed (retinal food, 36–72 h).

## 2. Odor-evoked responses in vivo

### 2.1 Hige, Aso, Modi, Rubin & Turner 2015, Neuron: protocol and counting

- **Odor.** "40-ml vials were loaded with 5-ml pure odorants, and the saturated headspace vapors were diluted by two
  steps of air dilutions down to 1% (odor generalization experiments) or 2% (the rest of the experiments). Final flow
  rate of the air stream was set to 1 L/min".
- **Pulses.** "Pre-pairing odor responses were measured by presenting 1-s odor pulses with inter-stimulus interval of
  25 s." Baseline "typically took 5 trials (ranging from 3 to 10)".
- **Analysis.** "Spikes were automatically detected by custom-written scripts by first removing slow membrane potential
  deflections with a high pass filter, and then identifying spikes based on amplitude, and verifying by visual
  inspection. PSTHs were calculated by convolving spikes with a Gaussian kernel (SD = 50 ms). Odor-evoked spikes were
  counted within the time window of 0 to 1.4 sec from odor onset. Spontaneous spiking rates were subtracted. EPSC
  charge transfer was calculated using the same time window."
  - The window used to estimate the spontaneous rate is not stated.
- **Cell-attached recordings.** Some data are cell-attached: "Since the effects on spikes were indistinguishable between
  whole-cell and cell-attached recordings, we present them as one data set." Figure 1 E–F includes n = 1 cell-attached.
- **Results.** "MBON-γ1pedc responded to our two test odors, 3-octanol (OCT) and 4-methylcyclohexanol (MCH), with high
  spike rates that persisted throughout the duration of the 1-s odor pulse".
  - "(pre-pairing: 118 ± 8.3 spikes, post: 24 ± 7.4, mean ± SEM; n = 7)"
  - "(Figures 1D-1F; pre: 110 ± 11 spikes, post: 83 ± 14)"
- (derived) That is 84 and 79 Hz above baseline averaged over 1.4 s. The response starts ≈ 0.15 s after valve opening
  (below), so it is ≈ 90–100 Hz above baseline while it lasts.

### 2.2 Spike counts in the other pre-pairing groups (all fig., approx.)

| Figure | Group | n | Pre-pairing spike counts |
|---|---|---|---|
| 5D | MB099C flies, 2% | 8 | OCT ≈ 75, MCH ≈ 85 |
| 5H | TH-GAL4 flies, 2% | 5 | OCT ≈ 100, MCH ≈ 100 |
| 7E | 1% dilution | 7 | PA ≈ 105, BA ≈ 105, HP ≈ 90, EL ≈ 88 |
| 7H | 1% dilution | 5 | PA ≈ 100, BA ≈ 98, HP ≈ 85, EL ≈ 85 |

Pre-pairing MBON11 responses thus span ≈ 75–120 spikes across groups of flies.

### 2.3 PSTH shape (Fig. 1E, n = 7; pixel-measured; fig., approx.)

| | OCT, pre-pairing | MCH, pre-pairing |
|---|---|---|
| Baseline | ≈ 6 Hz | ≈ 6 Hz |
| Rise begins | ≈ 0.15 s | ≈ 0.15 s |
| Peak | ≈ 135–140 Hz at ≈ 0.30 s | ≈ 135 Hz at ≈ 0.26 s |
| Mid-response | ≈ 95–100 Hz at 0.7–1.05 s; ≈ 80 Hz at 1.15 s | ≈ 100 Hz at 0.6–0.9 s |
| End | near baseline by ≈ 1.45 s | similar |

- The MCH trace peaking at ≈ 97 Hz is the *post*-pairing (orange) trace.
- This corrects `kc_classes_and_apl.md` §4, which says OCT "falls to ≈ 70 Hz by 1 s" and "MCH peaks ≈ 100 Hz". I
  have not edited that file.

### 2.4 Subthreshold depolarization

- No mean value is reported.
- Fig. 1D, single example cell, pre-pairing (fig., approx.):
  - Spike troughs sit ≈ 15–20 mV above the −60 mV pre-odor level.
  - Spike peaks reach ≈ 40 mV above it.
- Legend: "Scale bar, 20 mV". Fig. 7C legend: "Gray line, −60 mV."

### 2.5 Odor-evoked EPSCs (Hige 2015 Neuron, Fig. 3; VC, n = 5)

- **Internal and hold.** Cs-aspartate with "QX-314, 10" mM. "Cells were held at −70 or −60 mV, and cells that showed
  unclamped spikes during odor response were discarded."
- **Text.** "We observed large odor-evoked EPSCs that typically exceeded 200 pA in amplitude and were sustained
  throughout the duration of the odor pulse."
- **Mean EPSC, Fig. 3C** (fig., approx.; scale bar 200 pA = 47 px):
  - Onset ≈ 0.18 s after the odor bar starts.
  - Peak ≈ 380–430 pA.
  - ≈ 200 pA at ≈ 0.35 s after onset.
  - ≈ 170 pA sustained from 0.6 to 1.0 s after onset.
  - Back to baseline ≈ 1.5 s after onset.
- **Charge transfer, Fig. 3D** (fig., approx.): ≈ 245–250 pC for OCT (error bar to ≈ 290) and ≈ 265 pC for MCH.
  (derived) That is a mean current of ≈ 175–190 pA over 1.4 s.

### 2.6 Vrontou et al. 2021: 15-s odors (fig., approx.; n = 33)

- Odors: "1–20 ppm 4-methyl-cyclohexanol [MCH], 3-octanol [OCT], isopentyl acetate, or ethyl acetate". Temperature
  21–23 °C. Rates are "400-ms moving averages".
- Fig. 2B values:

| Measure | Value |
|---|---|
| Baseline | ≈ 7–8 Hz |
| On peak | ≈ 62 Hz; quantified on-response bar ≈ 62 Hz, individual cells up to ≈ 140 |
| Plateau | ≈ 15–20 Hz |
| Off peak | ≈ 30 Hz |

- Text: rates "declined and stabilized at slightly (MBON-α2sc) or moderately elevated plateaux (MBON-β1>α and
  MBON-γ1pedc>αβ) before rising again to a second peak at the end of the pulse".

### 2.7 Huang et al. 2024 (voltage imaging, 5-s odors)

- +35 Hz to CS+ and +25 Hz to CS− for ACV and 1% ethyl acetate before training (fig.; from `kc_classes_and_apl.md`).

### 2.8 Concentration scaling

- **No concentration series exists for MBON11 in any paper found.** Huang 2024's 1% vs 10% series covers PPL1 DANs only.
- Cross-study comparison (derived):
  - 2% saturated vapour, 1-s pulse: ≈ 79–84 Hz above baseline.
  - 1% saturated vapour, different odors: ≈ 85–105 spikes, ≈ 61–75 Hz (Hige Fig. 7).
  - 1–20 ppm, 15-s pulse: on-response ≈ 55 Hz above baseline (Vrontou).

### 2.9 Same protocol, other MBONs (Hige 2015 Neuron; fig., approx.)

**MBON-α2sc (Fig. 6, MB099C flies).**
- Counts:

| Panel | n | OCT | MCH |
|---|---|---|---|
| 6D | 7 | ≈ 85 | ≈ 71 |
| 6H | 6 | ≈ 75 | ≈ 67 |

- PSTH: peak ≈ 120 Hz at ≈ 0.25 s, ≈ 55 Hz at 1 s, off-bump ≈ 35–40 Hz at ≈ 1.7 s, baseline ≈ 0–3 Hz.
- Vrontou: α2sc shows "quiescence or sparse firing".

**MBON-γ2α′1 (Fig. 5L, n = 6), a γ-lobe MBON.**
- ≈ 105 spikes (OCT) and ≈ 90 (MCH). PSTH peak ≈ 140 Hz.

**Calcium kinetics (Hige 2015 Nature).** "In the MBONs with axonal projections inside the MB lobes (β1, γ1pedc, and γ4
neurons), we observed prolonged rise times (Extended Data Fig. 4)".

**Individuality (Hige 2015 Nature, Extended Data Fig. 8a).** MBON11 tuning varies across flies but matches across
hemispheres: "tuning patterns of the neurons from the same fly are more correlated than those from different flies
(n = 8 flies per cell types; Mann-Whitney U-test)".

## 3. KC → MBON11 synaptic strength

**No unitary KC→MBON11 EPSP or EPSC has been reported.**
- Searched: Hige 2015 ×2, Yamada 2024, Vrontou 2021, Barnstedt 2016, Takemura 2017, Li 2020, Hafez 2023, Wang 2026,
  Europe PMC full-text search.
- Woitkuhn et al. 2020 (J Neurogenet) recorded KC→MBON-γ1pedc>α/β transmission optogenetically but is paywalled. Its
  abstract gives no numbers.

### 3.1 Yamada, Davidson & Hige 2024, J Physiol: population EPSCs onto MBON11, ex vivo

**Why ex vivo.** "light stimulation we used for optogenetic activation of KCs evoked an EPSC-like inward current in
MBON-γ1pedc as well as many of the randomly selected neurons in flies without CsChrimson transgene ... We therefore
decided to switch to the ex vivo preparation."

**Why MBON11.** "we targeted MBON-γ1pedc because the relatively thick and short primary neurite of this neuron allows
for superior membrane voltage control (i.e. space clamp) during somatic voltage-clamp recordings ... MBON-γ1pedc
receives the majority of its inputs from the γ subtype of KCs as well as a minor fraction from α/β KCs in the
pedunculus region of the MB".

**Stimulus.**
- "we can reliably label a random ~3–7% of γ KCs (Isaacman-Beck et al., 2020), roughly equivalent to the fraction of
  KCs reliably responsive to a typical odor".
- The labelled fraction comes from the SPARC paper, not from counts in these brains.
- "KCs were stimulated by 1-ms light pulses delivered through the objective at 4.25 mW/mm^2".
- "two 1-ms light pulses 400 ms apart".
- Cs-aspartate + 10 mM QX-314 internal, held at −60 mV, 1.5 mM Ca / 4 mM Mg saline.

**First EPSC amplitudes, Fig. 1 left panels** (fig., approx.; mean ± SEM, gray lines are individual cells):

| Panel | Control first EPSC | Individual cells | Manipulation | PPR at 400 ms (control → manipulation) |
|---|---|---|---|---|
| B, n = 6 | ≈ 80 ± 7 pA | ≈ 57–103 | 0.7 Ca / 5.5 Mg: ≈ 49 pA | ≈ 0.49 → ≈ 0.75 |
| C, n = 6 | ≈ 117 ± 16 pA | ≈ 65–185 | 5 Ca / 0.5 Mg: ≈ 238 pA | ≈ 0.68 → ≈ 0.36 |
| D, n = 5 | ≈ 86 ± 6 pA | ≈ 69–103 | 10 µM mecamylamine: ≈ 41 pA | ≈ 0.38 → ≈ 0.37 |

- (derived) Pooled control mean ≈ 95 pA over 17 cells.
- Text: "The time course data of EPSCs and PPRs are shown in normalized values because the initial EPSC size was highly
  variable presumably because of our stochastic labeling strategy of KCs".

**Kinetics (Fig. 1B black trace; fig., approx.).**
- Calibration: the 400-ms pulse interval spans 63 px, so 1 px ≈ 6.3 ms.
- Onset to peak ≈ 100–120 ms. Width at half amplitude ≈ 230 ms.
- This is a compound response to prolonged KC activity after the flash, not unitary kinetics. Spikes per KC per flash
  are not reported.

**Quantal size.** "We were unable to analyze the miniature EPSCs, the size of which could have provided more mechanistic
insight, due their small size."

**α/β KCs onto MBON11 (MB008C + SPARC, Fig. 8B).**
- One example first EPSC ≈ 300 pA (fig., approx.; the 100-pA scale bar is ≈ 36 px).
- Legend: "Horizontal and vertical scale bars ... indicate 300 ms and 100 pA" (30 pA for the γ-KC figures).
- This is a single example, not a mean.

**(derived) Per-KC scale.**
- Hemibrain has 701 γ KCs, all presynaptic to MBON11 (§4). 3–7% of 701 is ≈ 21–49 KCs.
- 80–117 pA ÷ 21–49 KCs ≈ 1.6–5.6 pA per labelled KC per flash.
- Per synapse: ÷ 21.4 synapses per γ-main KC ≈ 0.08–0.26 pA.
- Charge per flash ≈ 82 pA × ≈ 0.23 s ≈ 19 pC, so ≈ 0.4–0.9 pC per KC.
- Caveats:
  - Spikes per flash are unknown.
  - Which γ subtypes MB623C labels was not checked.
  - The recording was ex vivo, under Cs⁺/QX-314, held at −60 mV.

### 3.2 Vrontou et al. 2021, Curr Biol: population drive in vivo

**Text.** "Optogenetic activation of αβc KCs expressing CsChrimson caused depolarizations of up to 20 mV that elevated
the firing rates of all three core-innervating MBONs (Figures 1D–1I) ... Blocking voltage-gated sodium channels with
tetrodotoxin (TTX) eliminated action potentials but preserved the voltage deflection on which these action potentials
normally ride (Figures 1D–1I), while adding the nicotinic acetylcholine receptor antagonist mecamylamine on top of TTX
leveled also the subthreshold depolarization".

**Methods.**
- "αβc KCs (R58F02-LexA > lexAop-CsChrimson)".
- Light "11–80 mW cm^-2".
- Drug concentrations: "mecamylamine (500 μM) ... or tetrodotoxin (TTX, 1μM)".

**Fig. 1H, MBON-γ1pedc>αβ, n = 6** (fig., approx.):
- Spike rate dark ≈ 2.5 Hz → light ≈ 40.5 Hz. Individual cells reach ≈ 25–60 Hz.
- Membrane potential in TTX ≈ −48.5 → ≈ −42 mV, so ≈ +6.5 mV (individual cells ≈ +1 to +14 mV).
- Illumination for 1H isn't given in the legend. Example traces in 1E use 50–1000 ms.

**Not reported:** how many αβc KCs R58F02 labels, or their light-driven firing rate.
- In hemibrain, KCab-c supplies 1,538 synapses (6.8% of MBON11's KC synapses), or 5,759 (25%) if hemibrain "m" is
  counted as core (derived).
- How Vrontou's "αβc" maps onto hemibrain classes isn't established.

### 3.3 Related MBON: α/β KC → MBON-α1 (Takemura et al. 2017, Fig. 7—figure supplement 1; in vivo; n = 6)

- Text: "ChrimsonR-expressing α/β KCs were photostimulated for 100 msec ... Blue trace shows the response when spiking is
  blocked (1 μM tetrodotoxin (TTX)), indicating a strong monosynaptic connection. This response was effectively
  blocked by the addition of the nicotinic antagonist 250 μM mecamylamine (MEC)".
- Mean (fig., approx.):
  - Control ≈ −58.5 → −47.5 mV, so ≈ +11 mV peak.
  - TTX ≈ +10.5 mV, peaking at ≈ 0.1 s and gone by ≈ 0.4 s.
  - TTX + MEC ≈ +2 mV, a light artifact also seen without ChrimsonR.

### 3.4 Transmitter, receptors, kinetics

**Barnstedt et al. 2016 (calcium imaging, mostly M4/6 = MBON-β′2mp/γ5β′2a).**
- "Local ACh application, or direct Kenyon cell activation, evokes activity in mushroom body output neurons (MBONs).
  MBON activation depends on VAChT expression in Kenyon cells and is blocked by ACh receptor antagonism."
- "these optogenetically evoked M4/6 responses were also blocked by adding 250 μM mecamylamine".
- "100 μM mecamylamine did not abolish responses in this preparation but caused a strong and reversible reduction".
- MBON11 itself responds to puffed ACh: Fig. 3F, "GABAergic MBON in the heel region, MBON-γ1pedc>αβ (MVP2)/MB112C".
- **No EPSC kinetics.** Barnstedt is calcium imaging only.

**Direct nicotinic evidence on MBON11.**
- Yamada 2024: 10 µM mecamylamine "attenuated the first EPSC to an equivalent level to the low calcium condition",
  ≈ 86 → 41 pA, with PPR unchanged.
- Vrontou 2021: 500 µM leveled the TTX-resistant depolarization.

**Li et al. 2020.** MBONs "receive excitatory, cholinergic synapses from KCs (Barnstedt et al., 2016; Takemura et al.,
2017)."

**Unitary EPSP kinetics** exist only for KC→α2sc (§5) and in locust (Cassenaer 2007, §5).

### 3.5 Short-term plasticity

- γKC→MBON11 PPR at 400 ms ≈ 0.38–0.68 in three control groups (Yamada, fig., approx.).
- Low Ca²⁺ raises PPR and high Ca²⁺ lowers it, so release probability is high.
- Piao & Sigrist 2021, summarizing Woitkuhn 2020: KC-to-MBON γ1pedc>α/β synapses "operate with a high SV release
  probability" (see `../Rung 4 resting state data/short_term_plasticity.md` §3.4).
- In vivo, the odor EPSC falls from ≈ 400 pA to ≈ 170 pA within ≈ 0.5 s (Hige Fig. 3C). That is a ratio of ≈ 0.4,
  combining depression and KC adaptation (fig., approx.).

### 3.6 A model-based per-KC value for another MBON: MBON-α3 (Hafez et al. 2023 eLife)

This is not a measurement. Synaptic strength was calibrated to Hige 2015 Nature.
- Table 2: "The maximal conductance was determined to achieve the target MBON depolarization from monosynaptic KC
  innervation". Its Gmax "1.5627×10-5 (Hige et al., 2015b)".
- Text: "gmax=1.56×10-11 S, chosen to obtain response levels in agreement with the target values. The average number of
  synaptic contacts from a KC to this MBON is 13.47".
- Result: "Activating a single KC leads to a voltage excursion at the soma with a mean of 0.37 mV".
- Fifty random KCs (≈ 5%) give "a mean somatic depolarization of 15.24 mV".

## 4. Connectome counts

**Li et al. 2020** gives no per-MBON KC input totals in its text. They are in figures and supplementary data, which I did
not read.

### 4.1 Hemibrain v1.2, KC → MBON (derived)

Counts are from the traced-adjacency export, counting neuron types starting "KC". They are for cells with complete
right-MB arbors; the hemibrain fly is female. The model uses MaleCNS (male), whose counts will differ.

| MBON (hemibrain instance) | Presynaptic KCs | KC synapses | Synapses per connected KC (mean / median / max) | All input synapses | KC fraction |
|---|---|---|---|---|---|
| **MBON11 (γ1pedc>α/β)_R** | **1,694** | **22,647** | 13.4 / 12 / 67 | 26,228 | 0.86 |
| **MBON18 (α2sc)_R** | **885** | **10,888** | 12.3 / 13 / 32 | 12,340 | 0.88 |
| MBON14 (α3)_R, two cells | 894; 897 | 11,022; 11,723 | 12.3; 13.1 | 12,099; 12,816 | 0.91 |
| MBON07 (α1)_R, two cells | 917; 928 | 12,873; 12,777 | 14.0; 13.8 | 14,848; 14,781 | 0.87; 0.86 |
| MBON01 (γ5β′2a)_R | 984 | 26,853 | 27.3 | 31,190 | 0.86 |
| MBON05 (γ4>γ1γ2), instance "(AVM07)_L", arbor in the imaged MB | 786 | 21,280 | 27.1 | 25,688 | 0.83 |
| MBON12 (γ2α′1)_R, two cells | 1,027; 1,011 | 6,892; 6,572 | 6.7; 6.5 | 8,494; 8,167 | 0.81; 0.80 |

MBON11_R's KC inputs by type:

| KC type | KCs connected / KCs of that type | Synapses | Synapses per KC |
|---|---|---|---|
| KCg-m (γ main) | 590/590 | 12,653 | 21.4 |
| KCg-d | 99/99 | 1,285 | 13.0 |
| KCg-t | 8/8 | 137 | 17.1 |
| KCg-s1–4 | 4/4 | 150 | 37.5 |
| KCab-m | 354/354 | 4,221 | 11.9 |
| KCab-s | 223/223 | 2,005 | 9.0 |
| KCab-c | 250/252 | 1,538 | 6.2 |
| KCab-p | 60/60 | 511 | 8.5 |
| KCa′b′ (all three) | 106/337 | 147 | 1.4 |

- (derived) γ: 701 KCs, 14,225 synapses (62.8%). α/β: 887 KCs, 8,275 (36.5%). α′/β′: 0.6%.
- (derived) MBON18_R (α2sc) by type:
  - KCab-s: 223 KCs × 15.9 synapses.
  - KCab-m: 354 × 13.7.
  - KCab-c: 252 × 9.5.
  - KCab-p: 39 of 60 × 1.7.
  - α′/β′: 17 KCs, 21 synapses.
- The literature agrees qualitatively:
  - Yamada: "the majority of its inputs from the γ subtype of KCs as well as a minor fraction from α/β KCs".
  - Perisse 2016: "Dendrites of MVP2 neurons ... innervate the γ1 region and more densely innervate the αβs than the αβ
    core (αβc) region".

**Size relative to the median traced neuron** (derived; median input 362, median input+output 784 synapses):

| Neuron | Inputs | Outputs | Inputs / median | (Inputs + outputs) / median |
|---|---|---|---|---|
| MBON11_R | 26,228 | 5,167 | 72× | 40× |
| MBON18_R (α2sc) | 12,340 | 1,702 | 34× | 18× |
| MBON14_R (α3, two cells) | – | – | 33–35× | 18–20× |

MBON11 is ≈ 2.1–2.2× α2sc on either measure. The model's "29–40×" for MBON11 matches the input+output figure.

### 4.2 Takemura et al. 2017 (FIB-SEM α lobe; MBON-α2sc and α3 only)

MBON11's dendrites in γ1 and the peduncle are outside this volume.

**Table 2, "Direct connections from KCs to MBONs"** (presynaptic KCs, synapses, synapses per KC, % from α/βsc):

| MBON | Presynaptic KCs | Synapses | Synapses per KC | % from α/βsc |
|---|---|---|---|---|
| MBON-α2sc | 909 | 11,281 | 12.41 | 99.4% |
| MBON-α3-A | 948 | 12,770 | 13.47 | – |
| MBON-α3-B | 948 | 13,129 | 13.85 | – |

**Table 3, MBON-α2sc**: "480/480 × 14.13" (α/βs), "132/132 × 13.67" (α/βc outer), "259/259 × 10.14" (α/βc inner),
"38/78 × 1.76" (α/βp).

**Text.** "every KC passing through a layer of the compartment that was extensively innervated by an MBON made at least
one synapse with that MBON. Previous electrophysiological measurements of connectivity in the α2 compartment indicated
that only about 30% of KCs connect to MBON-α2sc (Hige et al., 2015b), suggesting the possibility that the majority of
KC>MBON synapses are functionally silent ... However, we cannot rule out a more trivial explanation: These measurements
were made in the presence of cholinergic antagonists that could have partially blocked synaptic events (Barnstedt et
al., 2016) and lead to an underestimate of total connectivity levels."

## 5. The measured KC → MBON-α2sc unitary EPSP

**Who.** Hige, Aso, Rubin & Turner 2015, Nature 526:258, "Plasticity-driven individualization of olfactory coding in
mushroom body output neurons". Paired in vivo whole-cell recordings, α/β KCs (c739) → MBON-α2sc (MZ160).

**Conditions.**
- "Since KCs are immunonegative for choline acetyltransferase and unlikely to be cholinergic, we applied the
  cholinergic blocker mecamylamine (100 μM) to the bath saline to minimize unrelated circuit activity that could obscure
  weak connections. In addition, we tested for connections using current injection (25.2 ± 5.5 pA, 175 ± 9.0 ms,
  mean ± SEM) to drive high frequency spike trains in the KCs (10.6 ± 0.8 spikes, mean ± SEM)."
- "Cells were held at around 60 mV by injecting hyperpolarizing current (< 20 pA for MBONs, < 5 pA for KCs)." The minus
  sign is missing in the PMC text.

**Connectivity.**
- Main text: "we found only 7 pairs out of 24 with an excitatory connection, only 5 of which were likely monosynaptic
  ... This gives a probability of connection of < 30%, far more selective than the all-to-one convergence suggested by
  the dendritic anatomy."
- Methods: "Out of 24 pairs recorded, we found only eight statistically significant postsynaptic responses. Five pairs
  were judged as monosynaptically connected because step-wise increments in membrane potential were obvious in
  spike-trigger-averaged traces and also because the delay between the KC spike and the onset of the EPSP was less than
  2 ms". Eight is 5 monosynaptic + 2 small excitatory + 1 inhibitory.
- "synaptic weights of KC- α2sc connections are highly heterogeneous, since some connections were strong enough for us
  to detect clear unitary synaptic events."

**Amplitudes.** No mean ± SEM is given in the text. Read from figures:
- **Extended Data Fig. 9d.** Legend: "The spike-trigger-averaged EPSPS from the first spike in the train from five
  different recordings are shown overlaid in gray. The mean across cells is shown in red." The axis is labelled in mV.
  - Mean first-spike EPSP ≈ 0.25 mV at ≈ 8 ms, ≈ 0.27 at 12 ms.
  - Individual pairs at ≈ 8–12 ms: ≈ 0.14, ≈ 0.22, ≈ 0.25, ≈ 0.29 and ≈ 0.43 mV (fig., approx.).
  - Rise from ≈ 1.5 to ≈ 6.5 ms, so 10–90% ≈ 4–5 ms (fig., approx.).
  - The trace after ≈ 12 ms includes the second KC spike: ≈ 60 Hz trains, ISI ≈ 16 ms (derived: 10.6 spikes / 175 ms).
- **Fig. 4c**, the example pair (fig., approx.):
  - Steps of ≈ 0.4 mV for the 1st, 2nd and 3rd KC spikes.
  - The summed PSP plateaus at ≈ 1.9 mV after ≈ 70 ms of firing.
- **Fig. 4d.** The five monosynaptic pairs' train responses peak at ≈ 0.3–2.0 mV (fig., approx.; 1-mV bar).
- This corrects `../Rung 4 resting state data/short_term_plasticity.md` §3.4, which says "~0.1–0.2 mV steps". I have
  not edited that file.

**Derived.**
- Per EM synapse: ≈ 0.25 mV / 12.4 synapses ≈ 0.020 mV (range 0.011–0.035), if every EM contact counts.
- Fig. 4c summation: plateau / step ≈ 4.75 at ≈ 60 Hz. With linear summation and no depression this implies an
  effective EPSP decay τ ≈ 70 ms (derived: 1/(1 − e^(−16.5/τ)) = 4.75). It is one pair, and depression would lengthen
  the estimate.

**Caveats.**
- The recordings were in 100 µM mecamylamine, so the unitary EPSP is likely underestimated (Barnstedt; Yamada; Takemura
  above). The size of the underestimate is unknown: no drug-free unitary measurement exists.
- 5–7 of 24 functional connections against EM all-to-one. If most EM contacts were really silent, scaling every EM
  synapse to this unitary value would *overestimate* population drive by about 3–5× (derived: 24/5 to 24/7).

**Other insect [locust], Cassenaer & Laurent 2007 Nature (KC → β-lobe neuron).** Quoted from the PDF; its text layer
renders ± as "6" and = as "5".
- "Monosynaptic connections were found in <2% of tested Kenyon cell (KC)–β-LN pairs (Fig. 1b). All were excitatory."
- "Unitary EPSPs were large (1.58 mV ± 1.11, n = 9 pairs)".
- "EPSP amplitude varied greatly across connected pairs (0.55–4 mV)".
- "unitary EPSP kinetics (10–90% rise time, 8.3 ms ± 2.3; time to 1−(1/e) of peak, 13.2 ms ± 4.4)".

## 6. Electrotonic structure

**No compartmental or cable model of MBON11 found.** A web search and a Europe PMC full-text search turned up only Hafez
2023, on MBON-α3.

**MBON11 specifically.**
- Yamada 2024: "the relatively thick and short primary neurite of this neuron allows for superior membrane voltage
  control (i.e. space clamp) during somatic voltage-clamp recordings".
- MBON11's somatic spikes are large: ≈ 20–27 mV in Hige 2015 Neuron Fig. 1D and ≈ 20–25 mV in Vrontou Fig. 1E
  (both fig., approx.; Vrontou's 10-mV bar is ≈ 11 px in the PMC image). MBON-α3's are 4.3 mV, attributed to "a long
  neurite connecting the dendritic input region to the soma" (Hafez).
- Both point to a soma electrotonically close to MBON11's spike-initiation and dendritic regions. No source draws that
  conclusion for MBON11.

**MBON-α3 (Hafez 2023).**
- "We show that this neuron is electrotonically compact".
- "λ≈1,300 μm. This is about twice the maximal path length between any two segments of the cell".
- Local dendritic EPSPs vary ≈ 30-fold (≈ 0.03 to ≈ 1 mV), yet "activation of each synapse has exactly the same effect
  at the soma, within less than one μV."

**MBON-α2sc (Hige 2015 Nature).** Somatic calcium signals can be absent, "presumably attributable to low expression of
voltage-gated calcium channels at the soma and/or to the extremely long primary neurite connecting the soma to the
axon and dendrites."

**[locust] β-LNs (Cassenaer & Laurent 2007).** "Simultaneous impalements of different dendrites in the same β-LN (n = 2
experiments), however, show that the amplitudes of most events were the same across recording sites (Pearson's
correlation > 0.9)".

**Bottom line.**
- Nothing indicates that MBON11's dendrites shrink single-KC somatic EPSPs below what its total membrane implies.
- In a compact cell, the size effect is total capacitance and conductance. That is what a 1/size weight rule
  represents.
- How large that effect is for MBON11 is unmeasured (§1).

---

## For the model

### What the data say about the 1–3-spike gap (derived reasoning)

1. **MBON-α2sc is the natural control.**
   - The model matches Hige's α2sc unitary EPSP.
   - In the same protocol, α2sc fired ≈ 71–85 extra spikes in 0–1.4 s, against MBON11's 110–118.
   - Hemibrain gives α2sc 885 KCs × 12.3 synapses and MBON11 1,694 × 13.4. Under a 1/size rule (MBON11 ≈ 2.2× α2sc),
     both cells get similar summed KC drive.
   - If the model's α2sc also fires only a few spikes to an odor, the shortfall lies in the shared KC→MBON calibration
     or in KC activity, not in MBON11's size.
2. **The calibration target may be low.** The α2sc unitary EPSP was recorded in 100 µM mecamylamine, and 10 µM alone
   halves the KC→MBON11 EPSC. So 0.25 mV is plausibly a lower bound per connected KC. The opposite caveat is the
   5–7 of 24 connectivity (§5).
3. **MBON11's input is 63% γ KCs** by synapse count. In Turner 2008 only 1 of 15 γ KCs spiked to odors (γ ≈ 2%; see
   `kc_classes_and_apl.md`). MBON11's drive depends on the model's γ-KC odor responses more than on the overall 6%.
4. **Match the recording conditions when testing.** Hige held MBON11 at −60 mV with < 50 pA and subtracted spontaneous
   spikes. The response starts ≈ 0.15 s after valve opening, and the 0–1.4 s window includes that delay.

### Candidate data-based ways to set the KC→MBON11 weight (most direct first)

**A. MBON11 population EPSC, measured ex vivo (Yamada 2024).**
- Data: 80–117 pA first EPSC (pooled ≈ 95 pA, n = 17) per 1-ms flash on ≈ 3–7% of γ KCs (≈ 21–49 KCs). That is
  ≈ 1.6–5.6 pA per KC (derived).
- The EPSC is slow: peak ≈ 0.1 s, half-width ≈ 0.23 s. PPR 0.4–0.7 at 400 ms.
- To use it: activate 21–49 random γ KCs once in the model, with MBON11 spiking off, and match the summed synaptic
  current. This needs a weight-to-pA mapping (D).
- Weaknesses: spikes per KC per flash unknown; ex vivo; Cs⁺/QX-314.

**B. MBON11 population drive, measured in vivo (Vrontou 2021).**
- Data: αβc KC activation gives +38 Hz (2.5 → 40.5) and +6.5 mV in TTX.
- To use it, the model's αβc KCs must be driven at the light-evoked rate. That rate and the labelled KC count are not
  in this paper (perhaps in Groschner 2018).
- Weak until those are found.

**C. Unitary EPSP measured on another MBON (Hige 2015 Nature).**
- Data: α2sc ≈ 0.25 mV mean (0.14–0.45) per connected KC; ≈ 0.02 mV per EM synapse (derived).
- Transferring it to MBON11 needs an assumption about MBON11's per-synapse somatic effect relative to α2sc. The model's
  1/size rule gives ×≈ 0.45.
- Treat it as a lower bound (mecamylamine). This is what the model currently satisfies.

**D. MBON11 intrinsic gain, measured in vivo (Wang 2026).**
- Data: F–I slope 0.35–0.47 Hz/pA over 40–105 pA, 300-ms steps, males.
- This fixes the model's MBON11 current-to-rate conversion independently of synapses.
- In an LIF, the high-rate slope is ≈ 1/(C·(V_θ − V_reset)). The measured slope implies C·ΔV ≈ 2.1–2.9 pC, e.g. C
  ≈ 210–290 pF for a 10-mV reset gap (derived; LIF approximation; adaptation and AHPs bias it). Note how much larger
  this effective C is than MBON-α3's measured 16.8 pF.
- Combined with A or C (in pA), it turns synaptic current into spikes without touching Hige's counts.

**E. In vivo odor EPSC (Hige 2015 Neuron, Fig. 3).**
- Data: ≈ 250–265 pC per 1.4 s (≈ 180 pA mean, ≈ 400 pA peak) to the same odors as the counts.
- It could set the total odor-evoked KC current given the model's KC activity, keeping spike counts as the test.
- But it comes from the same experiments as the counts, so it is only semi-independent.
- To compare with current clamp, scale by ≈ 0.6–0.75 for driving force (derived: E_rev ≈ 0–9 mV, holding −60/−70 mV,
  ≈ −45 mV during firing).

**F. Order-of-magnitude checks (derived).**
- Effective input resistance ≈ 150–300 MΩ: Hige's mean EPSC (≈ 170–190 pA in VC, ≈ 105–125 pA after driving-force
  correction) against the ≈ 18–30 mV depolarization in the Fig. 1D example (spike troughs ≈ 18 mV, middle of the spike
  band ≈ 30 mV). Different cells and internals, and spiking conductances are ignored. This is 3–6× below MBON-α3's
  926 MΩ.
- Per-KC charge from two routes, which agree within ≈ 2×:
  - ≈ 0.4–0.9 pC per KC per flash (Yamada).
  - ≈ 0.5–1.1 pC per KC spike, from Hige's ≈ 250 pC per odor ÷ ≈ 220–490 KC spikes. That assumes ≈ 6% of 1,694 KCs
    firing 2.2–4.9 spikes (Turner 2008).

### Keep for testing, not calibration

- Hige 2015 Neuron MBON11 counts: 118 ± 8.3 and 110 ± 11 (n = 7). Other groups ≈ 75–100 (Fig. 5). 1% odors ≈ 85–105
  (Fig. 7). All fig., approx., except Fig. 1.
- Hige 2015 Neuron MBON-α2sc counts: ≈ 85/71 (Fig. 6D) and ≈ 75/67 (Fig. 6H). Same protocol, so they test the shared
  KC→MBON calibration that C is built on.
- PSTH shape: peak ≈ 135–140 Hz at ≈ 0.3 s, ≈ 95 Hz at 1 s, off by ≈ 1.45 s.
- Vrontou 15-s odors: on ≈ 62 Hz, plateau ≈ 15–20 Hz, off ≈ 30 Hz. Huang's spontaneous 37 Hz without an electrode.
- LTD: ≈ 80% fewer spikes and ≈ 90% less charge after one pairing (`mushroom_body_plasticity.md`).
- If E is not used for calibration, Hige's EPSC charge and time course too.

---

## Sources

- Hige, Aso, Modi, Rubin & Turner 2015, Neuron 88:985,
  [PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/). Text, methods, Figs. 1, 3, 5, 6, 7.
- Hige, Aso, Rubin & Turner 2015, Nature 526:258, [PMC4860018](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860018/).
  Methods, Fig. 3, Fig. 4, Extended Data Figs. 4, 8, 9.
- Yamada, Davidson & Hige 2024, J Physiol 602:2019,
  [PMC11068490](https://pmc.ncbi.nlm.nih.gov/articles/PMC11068490/). Methods, Fig. 1, Fig. 8.
- Vrontou, Groschner, Szydlowski et al. 2021, Curr Biol,
  [PMC8612741](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/). Text, STAR Methods, Figs. 1, 2.
- Wang, Lv, Gao et al. 2026, Nat Commun, "Hunger states modulate aggression via opposing dopamine pathways",
  [PMC13624267](https://pmc.ncbi.nlm.nih.gov/articles/PMC13624267/), doi 10.1038/s41467-026-76608-y. Methods,
  Supplementary Fig. 7 legend, Source Data sheets Fig6o, Fig7l, Figs8f.
- Hafez, Escribano, Ziegler, Hirtz, Niebur & Pielage 2023, eLife 12:e77578,
  [PMC10069864](https://pmc.ncbi.nlm.nih.gov/articles/PMC10069864/).
- Takemura et al. 2017, eLife 6:e26975, [PMC5550281](https://pmc.ncbi.nlm.nih.gov/articles/PMC5550281/). Tables 2–3,
  Fig. 7—figure supplement 1.
- Li et al. 2020, eLife 9:e62576, [PMC7909955](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909955/).
- Hemibrain v1.2 traced adjacencies,
  `https://storage.googleapis.com/hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz`.
- Barnstedt et al. 2016, Neuron 89:1237, [PMC4819445](https://pmc.ncbi.nlm.nih.gov/articles/PMC4819445/).
- Perisse et al. 2016, Neuron 90:1086, [PMC4893166](https://pmc.ncbi.nlm.nih.gov/articles/PMC4893166/). Imaging and
  anatomy only.
- Pavlowsky et al. 2018, Curr Biol, [PMC5988562](https://pmc.ncbi.nlm.nih.gov/articles/PMC5988562/). Imaging only; no
  MBON11 electrophysiology.
- Huang et al. 2024, Nature, [PMC11525173](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525173/).
- Cassenaer & Laurent 2007, Nature 448:709 [other insect]. PDF via
  [Caltech course page](https://www.its.caltech.edu/~jkenny/nb250c/papers/Cassenaer-2007.pdf).
- Woitkuhn et al. 2020, J Neurogenet, doi 10.1080/01677063.2019.1710146. Paywalled; abstract only.
