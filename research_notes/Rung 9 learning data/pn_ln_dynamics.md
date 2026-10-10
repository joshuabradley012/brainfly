# PN firing limits and LN odor-response dynamics, measured: intrinsic excitability, peak rates, LN time course, inhibition onset

Compiled 2026-10-09 from full texts, figure images, legends and supplements: PMC XML/HTML, Elsevier `mmc1` supplements,
the Nature supplement of Bhandawat 2007, and the Caltech copy of Wilson 2004's SOM.
Purpose: decide whether brainfly's uniglomerular PNs need refractoriness, an AHP or saturation beyond the current LIF
(τm 20 ms, 2.2 ms absolute refractory period). That LIF lets them fire about 330-350 spikes/s for 0.5 s. Also: whether
the model's synchronous LN onset burst (about 77 spikes/s per LN over the first 50 ms, then 8-10) matches flies.

**Conventions**
- Text in quotation marks is verbatim.
- "(fig., approx.)" means read off a published figure with a pixel grid. Expect ±3-5% of full scale, more where traces
  overlap.
- "(derived)" means my arithmetic, shown.
- "not reported" means I searched the text, the legends and the supplement (where accessible) and did not find it.
- n is as stated by the authors.
- Times are from the valve command ("nominal onset") unless stated.

Related notes, not repeated here:
- [presynaptic_inhibition.md](presynaptic_inhibition.md): magnitudes, GABA-A/B split, decay constants, Chou 2010 LN
  table.
- [orn_dynamics.md](orn_dynamics.md): ORN latency, rise and onset spread (§1.2, §2); PN timing (§5).

**Access limits**
- Wilson, Turner & Laurent 2004 (Science): main text not accessible (Science and the Wilson-lab site return 403). Only
  the SOM was read.
- Huang et al. 2010 (Neuron): main text not accessible. Only the PubMed abstract and the Supplemental Information were
  read.
- Seki et al. 2010 (J Neurophysiol): only the abstract was accessible.
- "Murthy & Turner": I found no paper by them with PN intrinsic data. Their Drosophila recording papers I know of are
  Kenyon-cell studies or methods protocols, which are out of scope.

## Summary: key numbers

1. **PN passive properties.**
   - Membrane time constant 16.6-30.6 ms (derived as Rm·Cm from Gouwens & Wilson 2009's three fitted DM1 PNs).
   - Somatic input resistance:
     - 598 ± 69 MΩ (n = 14, Gouwens & Wilson 2009);
     - 0.61 ± 0.17 GΩ (n = 16, Huang 2010);
     - 459 ± 30 MΩ (explant, Iniguez 2013).
     - By glomerulus: ≈260 MΩ (DM4) to ≈1010 MΩ (VM2) (Kazama & Wilson 2008 Fig. S2, fig., approx.).
   - True resting potential "approximately −55 to −60 mV" with ORN input intact.
   - Somatic spikes are only "5 to 15 mV" (6.6 ± 1.8 mV, Huang 2010).
2. **PN firing limit under constant current.**
   - The "average maximum frequency at which PNs can fire constantly over a 500-ms period of somatic current
     injection" is ≈164 spikes/s (n = 8; Kazama & Wilson 2008 Fig. 9A dotted line, fig., approx.).
   - At >100 spikes/s, firing does not decline over 500 ms ("104.2% of the initial rate, n = 8").
   - PN "firing rates only grow sublinearly with increasing synaptic currents (data not shown), due to the relative
     refractory period".
   - **No refractory period, AHP, spike width or rheobase has been published for fly PNs.**
3. **Peak odor-evoked PN rates are about twice the 500-ms saturation.** In 50-ms bins (overlapping 25 ms), trial- and
   experiment-averaged:
   - The strongest PN responses peak at ≈300 spikes/s: 12 of 126 glomerulus-odor pairs exceed ≈250 and the maximum is
     ≈303 (Bhandawat 2007 Suppl. Fig. 2, fig., approx.).
   - VM7 PNs to 2-butanone 10⁻⁵ peak at ≈295-310 spikes/s about 150 ms after onset and fall to ≈130 by 500 ms
     (Olsen 2010 Fig. 8B, fig., approx.).
   - The 500-ms mean saturates at Rmax 144-170 spikes/s. For strong private input, peak/mean ≈ 2.0 (Olsen 2010 Fig.
     8C).
   - Averaged over all 843 PN responses, the peak is ≈88 spikes/s at ≈150 ms and ≈0.48 of the peak at 500 ms
     (Bhandawat Fig. 1b, fig., approx.).
4. **The LN population fires a sharp onset transient, but it is much smaller than the model's.** Mean of 45 LNs
   (Nagel 2015 Fig. 5b, 2-heptanone, fast valve, fig., approx.):

   | window | rate (spikes/s) |
   |---|---|
   | baseline | ≈4 |
   | peak, 20-ms Hann smoothing | ≈43, ≈15-25 ms after the valve |
   | 0-50 ms | ≈22 |
   | 50-100 ms | ≈13 |
   | 100-200 ms | ≈8 |
   | 200-500 ms | ≈6 |
   | 1-2 s into a 2-s pulse | ≈3 (below baseline) |
   | after offset, for about 1 s | ≈7-11 |

   - The model's 77 spikes/s per LN over the first 50 ms is ≈3.5× the fly mean (77/22, derived).
   - Over 10 odors with a standard olfactometer, the population PSTH peaks at only ≈22-26 spikes/s, ≈150 ms after
     nominal onset (Chou 2010 Fig. 5d, n = 84 + 9, fig., approx.).
   - LNs are diverse: ON, OFF and intermediate cells, "fast" and "slow" cells (Nagel & Wilson 2016). "Pan-glomerular"
     LNs (28%) are often inhibited by odors (Chou 2010).
5. **LN synchrony is not measured directly.** No paired LN odor recordings were found.
   - Indirect evidence: the 45-LN mean onset transient has a half-width of ≈26 ms, which includes the 20-ms smoothing
     (derived from Nagel 2015 Fig. 5b). So ON-cell onset bursts in separately recorded LNs are stimulus-locked to
     within about 25 ms.
   - Oscillatory LN synchrony (≈10 Hz, spikes phase-locked to the LFP) starts with odor-dependent delays "up to 500
     ms" after odor arrival (Tanaka 2009). The Wilson lab did not observe oscillations (Kazama & Wilson 2009).
6. **Presynaptic inhibition builds slowly relative to LN spiking.**
   - "LN firing rates peak rapidly after odor onset, but the functional effects of inhibition peak ~100 ms later".
   - Fit: an "alpha function with a time constant of about 25 ms" applied to the LN rate (Nagel 2015).
   - Under a step of ChR2-driven LN spiking, the PN's inhibition reaches 50% at ≈50-70 ms and 90% at ≈150-160 ms; LN
     firing peaks at ≈20-25 ms (Nagel 2015 Fig. 6, fig., approx.).
   - GABA-B alone lets the first ≈60 ms of a PN response through (Olsen & Wilson 2008 Fig. 5a, one PN, fig.). So
     inhibition in flies is **not** strongest at the very onset; it grows over 50-150 ms and persists.

---

## 1. PN intrinsic excitability (Q1)

### 1.1 Kazama & Wilson 2008, Neuron 58:401 ([PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/); supplement = Elsevier mmc1)

In vivo whole-cell recordings; PN types DM6, VM2, DL5, DM4, VM7. "Voltages are uncorrected for liquid junction
potential."

- **Constant firing under current injection, no decline.**
  - Fig. 8C legend (text): "Raster plots of spikes evoked by somatic current injection in a PN. Gray bar indicates 500-ms
    period of current injection. Even when injected current was sufficient to produce firing rates >100 spikes/s, PN
    responses did not decline over the course of 500 ms (final firing rates were 104.2% of the initial rate, n = 8
    cells)."
  - Results (text): "Sustained current injection at the soma produces PN firing rates that are quite constant over
    time (Figure 8C). Thus, a change in PN intrinsic conductances is unlikely to account for the large decline in
    odor-evoked PN responses over this time interval."
  - The example raster has 48-51 spikes per 500-ms trial, i.e. ≈96-102 spikes/s. The first spike comes ≈17 ms after
    current onset and the trains are regular (fig., approx.).
- **Maximum sustained rate.**
  - Fig. 9A legend (text): "Dotted line indicates the average maximum frequency at which PNs can fire constantly over a
    500-ms period of somatic current injection (n = 8 cells)."
  - The dotted line sits at **≈164 spikes/s** (fig., approx.: y-ticks 0 and 100 at pixels 241.5 and 129.5, line at
    57.5; (241.5 − 57.5)/112 × 100 = 164, derived).
  - In the same panel, VM2 PN odor responses (500-ms means, from Bhandawat 2007) plateau at ≈90 spikes/s on the
    exponential fit, with points up to ≈120 (fig., approx.).
  - The paper does not say what limits firing above this rate.
- **Relative refractoriness (qualitative, no data shown).** Discussion: "Although PNs are capable of firing at very high
  rates, firing rates only grow sublinearly with increasing synaptic currents (data not shown), due to the relative
  refractory period." No refractory period duration, AHP amplitude or spike width is given anywhere in the paper or
  supplement.
- **Input resistance.**
  - Fig. S2 legend: "Input resistance measured at the soma (Rinput, soma) for four different glomeruli (n = 9, 10, 9,
    and 10 for DM6, VM2, DL5, and DM4). This value differs significantly across glomeruli (p < 10-12, ANOVA)."
  - Bar heights (fig., approx.): DM6 ≈850 MΩ, VM2 ≈1010 MΩ, DL5 ≈360 MΩ, DM4 ≈260 MΩ.
  - Kir2.1 test (text): "we observe a significant decrease in Rinput, soma (301 ± 14 MΩ vs 187 ± 14 MΩ, p < 0.0005,
    t-test, n = 26 and 4)". The main-text Fig. 4D legend gives n = 26 and 9 for the same comparison.
  - Input resistance was measured "just after breaking into the cell".
- **Unitary inputs.** "Averaged across PNs, uEPSP amplitude was 6.19 ± 0.45 mV (n = 23)". The uEPSC was 29.0 ± 2.6 pA
  (n = 45).
  - The uEPSP in Fig. 4C decays from peak to 50% in ≈21 ms and to 37% in ≈30 ms (VM2), versus ≈14 ms and ≈19 ms
    (DL5) (fig., approx., traced against the pre-stimulus baseline).
  - Jeanne & Wilson 2015 summarise this as "a time constant of roughly 30 msec".
- **Synaptic saturation (the other half of Olsen 2010's attribution).**
  - Discussion: "We observed strong depression at all frequencies above about 50 spikes/s."
  - Fig. 8F: "Strong inputs rapidly depress ORN-PN synapses (n = 6 cells)". At 50 Hz the uEPSC falls to ≈45% of its
    initial amplitude by 40 ms and to ≈0-10% by 100 ms; at 20 Hz to ≈35-50% by 200-450 ms (fig., approx.).
- **Amplification of weak input.** "Odors that evoke small responses in ORNs (< 20 spikes/s) can evoke much stronger
  responses in postsynaptic PNs (> 100 spikes/s)."

### 1.2 Gouwens & Wilson 2009, J Neurosci 29:6239 ([PMC2709801](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/))

DM1 PNs (and others), in vivo, corrected for liquid junction potential (13 mV).

- **Spike size at the soma.** "Action potentials recorded at the soma in current-clamp mode are only 5 to 15 mV in
  amplitude (Fig. 1B)." Spikes are believed to start far from the soma: "Simulations predict that action potentials
  initiate at a location distant from the soma, in the proximal portion of the axon."
  - "Because a voltage step at the soma declines to ∼40–70% of its original amplitude at the predicted spike initiation
    zone, we can easily explain the observation that action potentials persist when the soma is substantially
    hyperpolarized."
  - "Hyperpolarizing the soma below −70 mV typically does not completely suppress spontaneous firing (Fig. 1C)."
- **Spike width: not reported.** For modelling, an LN spike "was sped up 16-fold and doubled in height" to match DM1 PN
  somatic spikes after passive propagation. That is a modelling step, not a width measurement.
- **Input resistance.** "Drosophila neurons are extremely small and have high input resistances (598.0 ± 69.3 MΩ, n =
  14, measured with antennae removed)." Seal resistance was "10.1 ± 1.6 GΩ, n = 13".
- **Resting potential.**
  - "On average, we had to hyperpolarize the membrane from −47.8 ± 1.6 mV to −57.8 ± 1.5 mV to recapitulate the
    cell-attached firing rate (n = 12)".
  - Discussion: "we estimate that the true resting potential of these neurons is approximately −55 to −60 mV when
    spontaneous synaptic input from ORNs is intact and approximately −65 mV when input from ORNs is removed."
  - "EK, equal to −97 mV for our solutions". The Na:K permeability ratio was estimated at "0.080".
- **Passive fits (Table 1, three DM1 PNs, text).**

  | cell | Rm (kΩ cm²) | Cm (µF cm⁻²) | Ri (Ω cm) | τm = Rm·Cm (derived) |
  |---|---|---|---|---|
  | 1 | 8.3 | 2.6 | 163.9 | 21.6 ms |
  | 2 | 20.4 | 1.5 | 102.5 | 30.6 ms |
  | 3 | 20.8 | 0.8 | 266.1 | 16.6 ms |

  - Table 2 (three synthetic dendritic tufts, cell 3's data) gives τm = 15.4, 16.4 and 16.1 ms (derived).
  - The authors note that "core properties (like the membrane time constant ...)" are more robust than the raw Rm and
    Cm.
- **Threshold, an assumption.** "Given that the true resting potential of these neurons is approximately −60 mV, and
  assuming a spike threshold at the SIZ near −40 mV, this implies that three nearly synchronous ORN spikes should be
  sufficient to drive a PN spike if unitary EPSPs summed linearly."
- **Rate versus somatic Vm, with ORN input intact (Fig. 7C).** "Relationship between firing rate and Vm measured in
  whole-cell mode. Vm was varied by injecting different amounts of holding current. Each gray line represents a
  different cell."
  - n = 12. Rates rise from ≈0-5 spikes/s near −70 mV to ≈20-40 spikes/s near −40 to −35 mV (fig., approx.).
  - This is a rate-voltage curve under spontaneous synaptic drive, not an f-I curve.

### 1.3 Huang, Zhang, Qiao, Hu & Wang 2010, Neuron 67:1021 (Supplemental Fig. S1A; main text not accessed)

Table in Fig. S1A, read from the figure's printed table (the values are printed as numbers):

| cell type | AP amplitude (mV) | AP threshold (mV) | input resistance (GΩ) |
|---|---|---|---|
| PN | 6.62 ± 1.76 | −29.70 ± 4.72 | 0.61 ± 0.17 |
| GH298 iLN | 32.52 ± 6.49 | −35.20 ± 6.06 | 1.31 ± 0.39 |
| Np1227 iLN | 29.92 ± 5.52 | −34.37 ± 6.26 | 1.18 ± 0.39 |
| Np2426 iLN | 39.08 ± 5.22 | −38.50 ± 5.56 | 1.00 ± 0.28 |
| krasavietz eLN | 25.69 ± 4.78 | −36.97 ± 6.37 | 0.40 ± 0.09 |

- Legend: "Action potential amplitudes and thresholds of the recorded neurons were measured by applying a series of
  increasing step-depolarizing currents under current clamp to induce action potentials. PNs were labeled by
  GH146-Gal4 (n = 27)."
- Legend: "Input resistance of the recorded neurons was calculated as Rin = ΔV/ΔI. (n = 16, 11, 16, 10, and 14 for PNs,
  GH298 iLNs, Np1227 iLNs, Np2426 iLNs, and krasavietz eLNs, respectively.)"
- Not given in the accessible material: whether ± is SD or SEM, any liquid-junction or seal correction, f-I curves, and
  maximum rates.
- The PN "threshold" is measured at the soma, which is electrotonically far from the spike initiation zone (§1.2).
  Seal correction is unknown.

### 1.4 Iniguez, Schutte & O'Dowd 2013, J Neurophysiol 110:1490 ([PMC4042424](https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/))

The only published PN f-I curve found. It comes from an **isolated adult brain** (1-2 days old), at **room
temperature**, "in external solution that contained picrotoxin and d-tubocurarine to block synaptic transmission",
with cells held at −75 mV.

- "In both wild-type and RNAi-1T-a knockdown PNs, suprathreshold current injections resulted in large sustained
  membrane depolarizations capped by small fast spikelets (Fig. 4, A and B)."
- "In both genotypes, firing frequency increased steadily with increasing current injection".
- **Wild-type f-I** (Fig. 4C, steps ≈0.57 s long, fig., approx.):

  | step (pA) | ≤30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
  |---|---|---|---|---|---|---|---|---|
  | spikelets/s | 0 | ≈3 | ≈5 | ≈9 | ≈18 | ≈27 | ≈38 | ≈45 |

  - Slope ≈0.9 Hz/pA over 70-100 pA (derived: (45 − 18)/30).
  - Steps stop at 100 pA, so no maximum rate is reached.
  - Legend n = 16 wild type and 15 knockdown; the panel labels say n = 18 each.
- **Input resistance and rest.**
  - "wild type (459 ± 30 mΩ; means ± SE; n = 18; P < 0.05, t-test)". The unit is printed "mΩ" and is evidently MΩ.
  - Resting potential −59.5 ± 1.47 mV (n = 11, Table 1, synaptic blockers present).
- Calcium-channel knockdown raised firing (≈100 Hz at 100 pA). PN excitability is therefore shaped by Ca²⁺ currents
  (the authors suggest Ca-activated K⁺ channels as one possibility). This is not a refractoriness measurement.

### 1.5 Other PN intrinsic statements

- **Wilson, Turner & Laurent 2004, SOM** ([Caltech copy](https://authors.library.caltech.edu/records/4q1g0-w5803)).
  - "Cells were accepted for recording if Rinput>500 MΩ and Raccess<50 MΩ".
  - "Spikes were not observed in PN recordings in cell-attached mode, probably because spikes are not actively
    propagated to the soma in these neurons (Fig. 1B)". Later work did record PN spikes cell-attached (Gouwens & Wilson
    2009; Kazama & Wilson 2009).
  - Spontaneous rate "(mean: 5 ± 0.7 Hz) varied widely across PNs (range: 0-17 Hz)".
- **Wilson & Laurent 2005** ([PMC6725763](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/)).
  - "In every case, cells with small-amplitude action potentials (<12 mV in amplitude) were PNs, whereas cells with
    large action potentials (always >40 mV) were confirmed as LNs."
  - The internal solution "yielded ... a spike threshold near -40 mV".
- **Kazama & Wilson 2009** ([PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/)).
  - "In the absence of odors, PNs fire spontaneously (typically 1–5 spikes/sec)".
  - Sister PNs are electrically coupled (Fig. 7). That figure shows "small action potentials when the Command neuron is
    depolarized above its threshold".
- **Jeanne & Wilson 2015** ([PMC5488793](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/), DA1 PNs).
  - Distance to threshold: "We measured the average voltage at which a spontaneous PN spike initiates, as well as the
    average PN voltage overall (in the absence of any stimulus). The difference between these values is the distance to
    spike threshold, which was about 10 mV on average (Figure 4C)."
  - Integration window: "a PN integrates ORN spikes over a window of approximately 20–30 msec". The best-fitting
    ORN→PN filter is 23 ms wide.
  - Spontaneous rates (supplement): "In PNs, spontaneous spike rates were 8.6±6.3 spikes/sec (n = 44) with
    channelrhodopsin and 8.3±7.1 spikes/sec (n = 5) without".
  - Their PN integrate-and-fire model is a modelling choice validated only for near-threshold first-spike latency
    (supplement):
    - Rm "0.3 G"; Cm "0.117 pF"; Vrest −55 mV; spike threshold −40 mV; reset −55 mV; "Refractory period 2 ms";
      alpha-function EPSG τ 3 ms, peak 0.7 nS, Vrev 0 mV.
    - "The voltage was then clamped at reset for a 2 msec refractory period."
    - The Cm unit must be nF for a sensible τ: 0.3 GΩ × 0.117 nF = 35 ms (derived).
- **Nagel, Hong & Wilson 2015 model (choices, not measurements).** "The constant Rm was set at 800 MΩ, which is close to
  published measurements^63, while τm (5 ms) was adjusted so that a unitary EPSP decayed with a half-width of about 50
  ms". Eleak was −70 mV.
- **Olsen, Bhandawat & Wilson 2010** (main text; the supplement does not mention refractoriness).
  - "The saturating form of this function reflects the combined effects of short-term depression at ORN-PN synapses and
    the relative refractory period of PNs (Kazama and Wilson, 2008)."
  - Discussion: "The major nonlinearities in the intra-glomerular transformation are short-term synaptic depression and
    the postsynaptic refractory period (Kazama and Wilson, 2008)".
- **Olsen & Wilson 2008.** "These could include short-term synaptic depression at ORN-PN connections, and/or an
  intrinsic ceiling on PN firing rates."

### 1.6 PN intrinsic properties: what is and is not measured

| property | value | source, n | how |
|---|---|---|---|
| membrane τ | 16.6-30.6 ms | Gouwens & Wilson Table 1, 3 DM1 PNs | derived Rm·Cm from passive fits |
| input resistance | 598 ± 69 MΩ (antennae removed) | Gouwens & Wilson, n = 14 | text |
| | 0.61 ± 0.17 GΩ | Huang 2010, n = 16 | suppl. table |
| | ≈260 (DM4) to ≈1010 MΩ (VM2) | Kazama & Wilson Fig. S2, n = 9-10 per glomerulus | fig., approx. |
| | 459 ± 30 MΩ | Iniguez 2013 explant, n = 18 | text |
| resting potential | −55 to −60 mV (ORNs intact); −65 mV (ORNs removed) | Gouwens & Wilson, n = 12 | text, seal-corrected |
| spike amplitude at soma | 5-15 mV; 6.62 ± 1.76 mV | Gouwens & Wilson; Huang, n = 27 | text; table |
| threshold | −29.7 ± 4.7 mV (soma); ≈10 mV above mean Vm | Huang; Jeanne & Wilson | table; text |
| f-I curve | ≈0.9 Hz/pA, 45 Hz at 100 pA (explant, room temperature, synaptic blockers) | Iniguez Fig. 4C | fig., approx. |
| in vivo f-I | "firing rates only grow sublinearly ... (data not shown)" | Kazama & Wilson 2008 | text, no data |
| max sustained rate | ≈164 spikes/s over 500 ms | Kazama & Wilson Fig. 9A, n = 8 | fig., approx. |
| adaptation at >100 spikes/s | none: final/initial = 104.2% over 500 ms | Kazama & Wilson, n = 8 | text |
| max instantaneous rate | not reported; ≥300 spikes/s sustained over a 50-ms bin in odor responses (§2) | Bhandawat, Olsen | fig., derived lower bound |
| refractory period, AHP, spike width, rheobase in vivo | **not reported** | n/a | n/a |

## 2. Highest PN firing rates in odor responses (Q2)

### 2.1 Bhandawat et al. 2007, Nat Neurosci 10:1474 ([PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/); supplement from nature.com)

PSTH method (supplement): "counting the number of spikes in 50-ms bins that overlapped by 25 ms. These single-trial
PSTHs were averaged together". Suppl. Fig. 2: "Baseline firing rates were not subtracted from the data displayed in
this figure." Latencies are upper bounds: "We do not know the absolute latency between the trigger pulse and the time
the odor stimulus actually reaches the antennae".

- **Grand mean** (Fig. 1b: "Spikes were counted in 50-ms bins and averaged across 5 trials with the same odor, then
  averaged across all blocks of trials (all odors and all experiments)"; n = 843 PN and 779 ORN responses), fig.,
  approx.:
  - PN: baseline ≈4.5 spikes/s; peak ≈4.4 spikes/bin ≈ **88 spikes/s** at ≈140-150 ms; ≈42 at 500 ms (0.48 of peak,
    derived).
  - ORN: baseline ≈7; peak ≈51 at ≈170-200 ms; ≈37 at 500 ms (0.73, derived).
- **Fig. 2 (fig., approx.).**
  - (d) latency to 90% of peak: ORN ≈197 ms, PN ≈143 ms.
  - (e) peak to half-peak: ORN ≈325 ms, PN ≈185 ms.
  - (f) share of spikes in the first 200 ms: ORN ≈23%, PN ≈37%.
  - (b) VA2 to geranyl acetate: PN peak ≈205 spikes/s.
  - (c) DM1 to ethyl butyrate: PN peak ≈210 at ≈100 ms, then ≈100.
- **Strongest responses** (Suppl. Fig. 2, all 126 glomerulus-odor PSTHs, 1:1,000 effective dilution). I traced the top
  of each mean PN line with a pixel script, so values are approximate:
  - Median PN peak ≈108 spikes/s; 22 of 126 pairs reach ≥200 and 12 reach ≥250.
  - Maximum per glomerulus:
    - DM3 ≈303 (2-octanone; also 3-methylthio-1-propanol ≈303, pentyl acetate and isoamyl acetate ≈297);
    - DM2 ≈295 (pentyl acetate);
    - VA2 ≈287 (ethyl acetate; 2,3-butanedione ≈278);
    - VM2 ≈274 (trans-2-hexenal);
    - DL1 ≈236 (methyl salicylate);
    - DM1 ≈202 (ethyl butyrate);
    - DM4 ≈183 (ethyl acetate).
  - These peaks are brief: for example, VA2 to 2,3-butanedione falls from ≈280 to ≈100 within ≈100 ms while its ORNs
    stay at ≈250.
- Text: "PN responses rise and accommodate rapidly, emphasizing odor onset." "Drosophila PNs accommodate rapidly and
  typically do not burst after stimulus offset".

### 2.2 Olsen, Bhandawat & Wilson 2010, Neuron 66:287 ([PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/))

Responses are "the trial-averaged number of spikes during the 500-msec odor stimulus period, minus the trial-averaged
baseline spike rate during the preceding 500 msec". PSTHs use "50-msec bins that overlapped by 25 msec".

- **Rmax (500-ms means).** "Rmax = 170, 167, 163, and 144, and σ = 16.3, 11.8, 12.4, and 44.8, for glomeruli DM4, DL5,
  VM7, and DM1, respectively."
  - In Fig. 1B, the highest-concentration private odors drive ORNs to ≈100-125 spikes/s and PNs to ≈160-165 (DM4, DL5,
    VM7) or ≈122 (DM1) (fig., approx.).
  - Simulation default: "Rmax = 165 spikes/sec and σ = 12 spikes/sec".
- **Peaks (Fig. 8, VM7 PNs, 2-butanone private odor, n = 10-11, fig., approx.).**

  | 2-butanone | public odor | peak (spikes/s) | at 480-500 ms |
  |---|---|---|---|
  | 10⁻⁶ (Fig. 8A) | none | ≈177 at ≈175 ms | ≈78 |
  | 10⁻⁵ (Fig. 8B) | none | ≈295-310 at ≈150 ms | ≈130 |
  | 10⁻⁵ (Fig. 8B) | weak | ≈308 | ≈95 |
  | 10⁻⁵ (Fig. 8B) | strong | ≈226 | ≈68 |

- **Peak-to-mean ratio (Fig. 8C).**
  - "We quantified transience as the ratio of the peak firing rate to the mean firing rate".
  - Strong private input (2-butanone 10⁻⁴): ≈1.9-2.0 at all public-odor levels.
  - Intermediate (10⁻⁵): ≈2.3-3.05. Weak (10⁻⁶): ≈2.5-6.9.
  - With the strong-private 500-ms mean ≈160-165 (Fig. 2C, fig.), the peak is ≈310-330 spikes/s (derived: 2.0 × 163).

### 2.3 Other peak-rate data

- **Kazama & Wilson 2009.**
  - Text: "Odors that elicit only a modest increase in firing rate (10–30 spikes/sec above spontaneous firing rates)
    increase correlations just as much as odors that elicit a powerful increase in firing rate (>150 spikes/sec)."
  - Fig. 3d (n = 15 homotypic pairs) uses rates "computed over a 100-ms period beginning at odor response onset (the
    time when the trial-averaged peri-stimulus time histogram reached 10% of its peak)". The maximum is ≈190
    spikes/s (fig., approx.).
- **Jeanne & Wilson 2015.** In the near-threshold optogenetic regime, "PN spike rates were consistently about three-fold
  larger than ORN spike rates (Figure 1C)".
- **Maximum instantaneous rate (minimum ISI): not reported anywhere.** A 50-ms bin averaging ≈300 spikes/s needs about
  15 spikes in 50 ms. The mean ISI is therefore ≤3.3 ms during the peak (derived: 50/15).

## 3. GABAergic LN odor responses (Q3)

### 3.1 Time course

- **Nagel, Hong & Wilson 2015, Nat Neurosci 18:56** ([PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/)).
  - Setup: 45 LNs (38 flies), cell-attached, from GH298, NP3056 and LCCH3 lines ("collectively label eight of the nine
    major morphological types of GABAergic LNs"). Odor 2-heptanone, 1:100 v/v (effective concentration lower). The fast
    valve was verified by PID to "reliably deliver square pulses of durations from 20 ms to 2 s".
  - "First, nearly all LNs we recorded were spontaneously active (4.6 ± 2.8 spikes/s, mean ± s.d. across cells) ...
    Second, odor-evoked activity in LNs was highly transient, with a sharp burst of spikes at odor onset (Fig. 5a,b).
    Most LNs did not respond in a sustained manner to long odor pulses. Indeed, responses were actually suppressed
    during long stimuli in many LNs (Fig. 5a)."
  - "By contrast, a dense train of intermittent pulses recruited LNs mainly at the onset of the train (Fig. 5c). In
    this respect LNs differ from PNs, which can show sustained responses to dense pulse trains".
  - Fig. 5b legend: "Firing rate was obtained by taking the average number of spikes per 1 ms bin (trial averages for
    each LN were averaged together) and smoothing with a 20 ms-wide hanning window. On average, both the short stimulus
    (20 ms) and the long stimulus (2 s) elicit mainly transient excitation, shifting towards inhibition during the later
    part of the long stimulus."
  - Digitized mean of 45 LNs (fig., approx.):
    - 20-ms pulse: baseline ≈4; peak ≈43 at ≈22 ms after valve onset. Half-maximum width ≈26 ms (≈153-163 px at
      2.6 ms/px, derived). Back to ≈11 by ≈60 ms, ≈8 over 75-135 ms, and ≈4-6 by ≈150-160 ms.
    - 2-s pulse: peak ≈43-44 within the first ≈15 ms (±15 ms at this resolution). Means by window:

      | window | rate (spikes/s) |
      |---|---|
      | 0-50 ms | ≈22 |
      | 50-100 ms | ≈13 |
      | 100-200 ms | ≈8 |
      | 200-500 ms | ≈6 |
      | 0.5-1 s | ≈5 |
      | 1-2 s | ≈3-3.6 (below baseline) |
      | 2-2.5 s (after offset) | ≈7, bump to ≈10-12 |
      | 2.5-3 s | ≈6 |

  - LN versus PN synaptic currents (whole-cell voltage clamp, −60 mV): "odor –evoked inward current was more transient in
    LNs than in PNs (Fig. 5d–f). Inward current in LNs was transient even after pharmacological blockade of inhibition".
    - Fig. 5f is "The ratio of the synaptic current late in the response to a long pulse (the last 200 ms of the stimulus
      period) to the peak synaptic current. This ratio is significantly higher in PNs than in LNs (p=1.7e-3, t-test)".
    - LNs ≈−0.37 to +0.25, clustered near 0 (n = 22); PNs ≈+0.1 to +0.47 (n = 9) (fig., approx.).
- **Nagel & Wilson 2016, J Neurosci 36:4325** ([PMC4829653](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)). Same 45
  LNs, an 18-stimulus panel, 2-heptanone; PSTHs smoothed with a 100-ms Hanning window.
  - "When we presented a dense train of brief odor pulses, we found that most LNs were excited at either the onset or the
    offset of the train (Fig. 1C–F). We term these ON and OFF cells. When we presented a long odor pulse, ON cells
    responded most strongly to the onset of a long pulse (Fig. 1C,D), whereas OFF cells responded at pulse offset (Fig.
    1E,F). ON responses typically decayed over the course of a pulse train or a long pulse."
  - "Some LNs responded with short latency and were able to track rapid pulse rates relatively accurately ("fast"
    cells). These cells also tended to have more transient responses to prolonged (2 s) pulses. Other LNs showed longer
    latencies to peak excitation and only responded repetitively when stimuli were longer and spaced further apart
    ("slow" cells)."
  - "we never observed stable and persistent responses to odor in any LNs."
  - "LNs were continuously distributed in the space of these two PCs, representing a smooth continuum between ON and OFF
    behavior."
  - Example single-cell peaks (Fig. 1, 100-ms smoothing, fig., approx.): fast ON ≈55-60 spikes/s at onset; slow ON
    ≈20; fast OFF ≈50 at offset.
  - Mechanism: "Both ON and OFF cells receive net inward current at stimulus onset, but OFF cells switch to net outward
    current by the end of the stimulus." "excitatory synapses onto LNs are fast and depressing, whereas inhibitory
    synapses are slow and facilitating."
  - ORN→LN depression: "Values of f and τ are 0.75 and 1566 ms for LNs; 0.78 and 893 ms for PNs."
- **Chou et al. 2010, Nat Neurosci 13:439** ([PMC2847188](https://pmc.ncbi.nlm.nih.gov/articles/PMC2847188/)).
  - Setup: whole-cell; 10 odors at 1:100, headspace diluted 10-fold; PSTHs in 50-ms bins overlapping 25 ms.
  - Fig. 4 legend: "there is a delay of about 100msec before odor reaches the fly."
  - Pan-glomerular LNs: "In the presence of an odor, spontaneous spiking in many pan-glomerular cells shut down
    completely, sometimes after a brief burst at odor onset, while others modestly increased their firing rate in the
    presence of odors (Fig. 5a). Overall, odor-evoked changes in firing rate were significantly weaker in pan-glomerular
    cells that in other LNs".
    - "This class comprised 28% of the cells we recorded from."
  - Pheromone-avoiding LNs: "These cells differed from other LNs in having especially transient bursts of excitation at
    odor onset (Fig. 5c)." "Thus, these LNs could create a transient pulse of GABAergic inhibition at odor onset."
  - Fig. 5d legend: "pheromone-avoiding LNs (n=9) fire a significantly higher percentage of their spikes during the
    first 100ms of the odor response as compared to all other LNs (n=84) (p<0.01, t-test; spikes counted during the
    period 100-200msec after nominal odor onset, divided by total spikes during the 1-sec period shown in rasters)".
    - Share of spikes in the first 100 ms: ≈29% vs ≈18% (fig., approx.).
    - Mean PSTH (fig., approx.):

      | | pheromone-avoiding (n = 9) | all other LNs (n = 84) |
      |---|---|---|
      | baseline | ≈5 | ≈6 |
      | peak, ≈150 ms after nominal onset | ≈25-26 | ≈22-23 |
      | at 500 ms | ≈7 | ≈14-15 |
      | dip at 0.7-0.8 s | ≈0-1 | ≈3.5 |

    - The rise starts ≈60-80 ms after nominal onset.
  - Fig. 4c "Percentage of spikes in 1st 100ms of response" by Gal4 line: Line5 14 ± 1, Line6 21 ± 2, Line7 23 ± 2,
    Line8 43 ± 4, Line9 17 ± 3 (text in figure table; full table in presynaptic_inhibition.md §6).
  - "Some cells (Fig. 6b,c) showed a transient burst at the onset of almost every odor, followed by inhibition. Other
    cells (Fig. 6d,e) exhibited sustained excitation, off-excitation, and more odor-specific tuning."

### 3.2 Rates at rest and during odors

| measure | value (spikes/s) | source, n, method |
|---|---|---|
| spontaneous | 2.3 ± 0.2 | Wilson & Laurent 2005, n = 12, cell-attached |
| spontaneous | 4.6 ± 2.8 (mean ± s.d.) | Nagel 2015 / Nagel & Wilson 2016, n = 45, cell-attached |
| spontaneous by line | 4.0 to 16.8 | Chou 2010 Fig. 4c (Lines 5-9) |
| spontaneous by class | pan-glomerular ≈10.2 vs others ≈5.4 | Chou 2010 Fig. 5b, n = 26 vs 67 (fig.) |
| odor, 1-s window, change from baseline | max 1.5 to 18.1; mean −3.1 to +8.7 by line | Chou 2010 Fig. 4c |
| odor, population mean, first 50 ms | ≈22 (peak ≈43 with 20-ms smoothing) | Nagel 2015 Fig. 5b (fig.) |
| odor, population mean, 0.2-0.5 s | ≈6 | Nagel 2015 Fig. 5b (fig.) |
| odor, population mean, peak 50-ms bin | ≈22-26 | Chou 2010 Fig. 5d (fig.) |
| ChR2-driven LN firing | ≈50-65, oscillating, for 1 s | Nagel 2015 Fig. 6c, n = 4 (fig.) |

### 3.3 Breadth across odors and glomeruli

- Wilson & Laurent 2005: "We measured odor-evoked activity in six LNs in response to seven odors plus a solvent control
  (paraffin oil)... Each LN responded with at least a small firing rate increase to every stimulus. In comparison to
  PNs, LN responses are relatively uniform across odors, both in magnitude and temporal profile (Wilson et al., 2004).
  However, different LNs did display specific odor preferences, both in terms response magnitude and latency (Fig.
  6A)."
- Chou 2010: "All these LNs fired spontaneous action potentials, and their spiking was always modulated by odors. LN
  odor responses were remarkably diverse and typically varied more across cells than across odors within a cell (Fig.
  4a,b)."
- Hong & Wilson 2015 ([PMC5495107](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/)), GCaMP3 in NP3056 LNs:
  - "We found that each private odor elicited LN activity in all glomeruli".
  - "we can infer that LN activity scales with the logarithm of total ORN spike rate."
- Wilson 2013 review ([PMC3933953](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)): "Most LNs are broadly tuned to
  odors; such tuning is consistent with broad connectivity".

### 3.4 Are LN onset responses synchronous across LNs?

- **Direct test: not found.** No study recorded pairs of GABAergic LNs during odors and reported spike synchrony.
  Paired LN recordings exist only as connectivity tests with current injection (Liu & Wilson 2013; Huang 2010; Yaksi &
  Wilson 2010).
- **Indirect, onset-locking.** The mean of 45 separately recorded LNs (Nagel 2015 Fig. 5b) peaks ≈22 ms after a 20-ms
  pulse, with a half-width of ≈26 ms after 20-ms Hann smoothing (fig., derived).
  - A Hann window 20 ms wide has a 10-ms half-width. The unsmoothed population transient is therefore roughly
    √(26² − 10²) ≈ 24 ms wide (derived, assuming Gaussian-like shapes).
  - So ON LNs that burst at onset do so within about 25 ms of each other in a fast-valve rig. This includes trial
    jitter, and it is not a measure of spike-level synchrony.
- **But not all LNs burst at onset.**
  - OFF cells are silenced during the odor and fire at offset.
  - "Slow" ON cells peak later (Nagel & Wilson 2016).
  - Many pan-glomerular LNs (28%) shut down during odors (Chou 2010).
- **Oscillatory synchrony is delayed and weak.** Tanaka, Ito & Stopfer 2009
  ([PMC2753235](https://pmc.ncbi.nlm.nih.gov/articles/PMC2753235/); sharp electrodes):
  - "oscillatory responses with an average frequency of ∼10 Hz could be elicited by an assortment of natural odorants".
  - "For LN1, the mean spike phase was 146 ± 49° (362 spikes from 4 cells) and, for LN2, 143 ± 44° (234 spikes from 6
    cells)."
  - "In Drosophila, in which LNs generate fast sodium spikes, PNs led LNs by ∼20° each cycle."
  - "We found that oscillations could begin at odorant-dependent times relative to the initial deflection in the LFP
    that indicates the arrival of odorant at the antenna (up to 500 ms delay in the fly compared with a typical 200 ms
    delay in locust)."
  - Picrotoxin abolished the oscillations, and the LN2 class was required for them.
  - Kazama & Wilson 2009: "We have not observed odor-evoked oscillations in the Drosophila antennal lobe, but they have
    been observed by other investigators".
  - Wilson 2013: "Oscillatory synchrony is less prominent in the Drosophila olfactory system than in the olfactory
    systems of other insects (Turner et al. 2007)".

### 3.5 LN intrinsic properties (brief)

- **Spike amplitudes and input resistances.** LN somatic spikes are 30-39 mV, versus 6.6 mV for PNs. Input resistances
  are 1.0-1.3 GΩ (Huang 2010 table, §1.3). Wilson & Laurent: LN spikes "always >40 mV".
- **Seki et al. 2010, abstract only.** "Each class of LN displayed unique characteristics in intrinsic
  electrophysiological properties, showing differences in firing patterns, degree of spike adaptation, and amplitude of
  spike afterhyperpolarization. Notably, one class of LNs had characteristic burst firing properties, whereas the
  others were tonically active." The numbers were not accessible.
- **Nagel & Wilson 2016.** "Cells with regular spontaneous firing repolarize rapidly, whereas cells with bursty
  spontaneous firing repolarize slowly." "Overall, the resting potential of bursty cells is more hyperpolarized than
  that of regular-firing cells" (n = 14).

## 4. Time course of presynaptic inhibition during an odor (Q4)

- **Nagel, Hong & Wilson 2015.** Section heading: "Inhibition grows slowly relative to local neuron spiking".
  - "We noted that LN firing rates peak rapidly after odor onset, but the functional effects of inhibition peak ~100 ms
    later in our PN data. The effects of inhibition also outlast the odor-evoked increase in average LN firing rates
    (Fig. 6a,b). These observations suggest that there is some slow process between LN spiking and the effects of
    inhibition on target cells."
  - Fig. 6a legend: "The main effect of blocking inhibition on the PN odor response begins ~100 ms after the peak in LN
    spiking, and also outlasts the burst in LN spiking."
  - ChR2 in NP3056 LNs (shakB² background; PNs n = 7, DM6 or VM2): "While light-evoked firing rates rose rapidly in LNs
    (Fig. 6c), inhibition measured in PNs progressed more slowly (Fig. 6d–f)... spontaneous EPSCs in PNs provide a
    sensitive measure of the time course of presynaptic inhibition. The time course of inhibition could be fit with an
    alpha function with a time constant of about 25 ms. These data provide direct evidence that LNs have slow effects
    on ORN neurotransmitter release."
  - Legends: Fig. 6d, "During the light stimulus, spontaneous EPSCs slowly become smaller and less frequent, and the
    mean inward current decreases"; Fig. 6e, "The mean holding current changes slowly compared to the time course of
    LN spiking"; Fig. 6f, "Note that by this measure, presynaptic inhibition also builds slowly."
  - My reading of Fig. 6c, e, f (light onset at x = 594.5 px, 2.6 ms/px; fig., approx.):
    - Mean LN firing (n = 4) rises at ≈17-22 ms and peaks at ≈23 ms.
    - PN mean holding current reaches 50% of its plateau at ≈68 ms and 90% at ≈159 ms.
    - The SD-of-current measure reaches 50% at ≈52 ms and 90% at ≈149 ms.
    - Ten-percent times are lost in baseline noise.
  - For comparison, an alpha kernel with τ = 25 ms applied to a step gives 1 − (1 + t/τ)e^(−t/τ): 10% at 13 ms, 50% at
    42 ms, 90% at 97 ms (derived). To an impulse it peaks at 25 ms, with half-maximum at 6 and 67 ms (derived).
  - Model: "Dynamic inhibition was added to the model in Fig. 7 by taking the average recorded spiking activity of all
    LNs (Fig. 5b), and then convolving this signal with a 25 ms alpha function to generate a measure of functional
    inhibition at each time point (I(t) ...). This inhibitory signal divided the input to the model (ORN firing rate) at
    each point in time... The magnitude of I(t) that we computed in this manner provided a good qualitative fit to the
    data, so its scale was not adjusted."
  - Why the slow growth matters: "When we filtered LN activity less strongly (thereby making the time course of
    inhibition more similar to the time course of LN activity), inhibition began to act on the synapse before the PN
    response had peaked, and so the peak response was attenuated and response onset was slowed (Fig. 7e)."
  - "When we clamped LN firing rates at their peak level throughout the odor stimulus, the PN response ran down during a
    long stimulus (Fig. 7d)."
- **Nagel & Wilson 2016 (LN→LN, GABA-A only onto LNs).**
  - "Outward currents grew slowly over time, in contrast to the rapid onset of spiking in the ChR+ LNs (Fig. 6D–F). Note
    that although outward currents were growing, firing rates in the ChR+ LNs were in fact decaying slightly. This
    observation implies that there is some slowly growing process that intervenes between presynaptic spikes and
    postsynaptic inhibitory potentials. For example, neurotransmitter release from LNs might facilitate during a
    presynaptic train, or GABA might take some time to reach distant receptors."
  - presynaptic_inhibition.md reads the Fig. 6F rise as 10-90% ≈160 ms.
- **Olsen & Wilson 2008** ([PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/)). It does not use the phrase
  "builds slowly".
  - Discussion: "Although both receptor types were co-active during most of the odor response, we noticed that GABAA
    receptors were required for the a brief early phase of inhibition after odor onset (Fig. 5), while GABAB receptors
    were required for the long, late phase (Fig. 3 and Fig. 5)."
  - Fig. 3c (EPSCs evoked every 0.25 s while a lateral odor inhibits them; control n = 12; fig., approx.): the sample at
    ≈+0.05 s after nominal onset shows no inhibition (≈100% of baseline). The next, at ≈+0.31 s, is ≈27%. Inhibition
    therefore develops between these samples; the first 300 ms are not resolved.
  - Fig. 5a, one VM7 PN, pentyl acetate (fig., approx.):

    | condition | spike timing |
    |---|---|
    | antennae removed | dense firing from ≈0.10 to ≈0.60 s |
    | picrotoxin alone (GABA-B intact) | brief burst only, ≈0.09-0.15 s, then silence |
    | CGP54626 alone (GABA-A intact) | sparse spikes from ≈0.2 to ≈0.55 s |
    | both | dense firing ≈0.05-0.70 s |

    So with only GABA-B available, the first ≈60 ms of the response escape inhibition. With only GABA-A available, the
    onset is suppressed.
- **Wilson & Laurent 2005**, abstract: "Whereas GABAA receptors shape PN odor responses during the early phase of odor
  responses, GABAB receptors mediate odor-evoked inhibition on longer time scales."
- **Wilson 2013 review, on LN→PN pairs (Yaksi & Wilson 2010)**:
  - "clear unitary synaptic connections are never observed in these paired recordings. Rather, a train of spikes in the
    LN is always required to see any measurable PN response in single trials, and the PN response grows slowly
    throughout the train."
  - LN-LN connections "seem to be weak and slow".
- Magnitudes and decay time constants (GABA-B tail ≈1 s after offset) are in presynaptic_inhibition.md §1, §4 and the
  "For the model" table.

## 5. ORN onset, as it bears on a synchronous LN burst (Q5, brief)

Details are in orn_dynamics.md §1.2-1.3 and §2. Latency falls steeply with drive (3-4 ms at high and 18-55 ms at low
concentration, Egea-Weiss 2018), so strongly driven ORN types lead weakly driven ones by tens of ms.

Additions from the papers read here:
- **Fast valve.** Nagel 2015 Fig. 1d: VM7 ORNs to 2-heptanone peak at ≈250 spikes/s within ≈20-30 ms of the valve, for
  both a 20-ms and a 2-s pulse (fig., approx.). The LN population transient is equally fast (§3.1). In this regime the
  ORN drive to LNs is nearly a step, so an onset-locked LN burst is expected.
- **Standard olfactometers.** Arrival is delayed and slower.
  - Wilson 2004 SOM: "Because the shortest-latency OSN responses were detected about 130 ms after odor onset, we always
    shifted our 100ms bins so that a bin began at 30ms after the trigger".
  - Chou 2010: "a delay of about 100msec before odor reaches the fly".
  - The mean ORN PSTH starts ≈75 ms after the valve and reaches 90% of peak at ≈195 ms (Bhandawat 2007).
  - In the same kind of rig, the LN population peaks ≈150 ms after nominal onset (Chou 2010 Fig. 5d).
- **Downstream delays.**
  - "there is a delay of ~4.5 msec between an ORN spike and the start of an excitatory postsynaptic potential (EPSP) in
    a PN (Kazama and Wilson, 2008)".
  - "The average time of the first evoked PN spike is 30 msec (Figure 2G)" after an optogenetic ORN flash (Jeanne &
    Wilson 2015).
  - Ipsi- versus contralateral EPSC arrival lag is "small (0.3 ± 0.10 ms, n = 3)" (Kazama & Wilson 2009).

---

## For the model

Status labels: **direct** = the quantity was measured as stated; **indirect** = inferred from a related measurement;
**choice** = a published modelling assumption; **mine** = my suggestion, not from the literature.

### A. PN refractoriness and saturation

| # | constraint | value | source | status |
|---|---|---|---|---|
| A1 | membrane τ | 17-31 ms (brainfly's 20 ms is inside) | Gouwens & Wilson Table 1 | direct (passive fit), derived |
| A2 | absolute refractory period | ≤ ≈3.3 ms. Odor PSTH peaks of ≈300 spikes/s over a 50-ms bin need ≥15 spikes per 50 ms | Bhandawat Suppl. Fig. 2; Olsen Fig. 8B | indirect lower bound on peak rate (derived) |
| A3 | maximum sustained rate under constant somatic drive | ≈164 spikes/s over 500 ms ("can fire constantly") | Kazama & Wilson Fig. 9A, n = 8 | direct, but figure-read; mechanism not stated |
| A4 | no slow spike-frequency adaptation | at >100 spikes/s, rate after 500 ms = 104.2% of initial | Kazama & Wilson Fig. 8C, n = 8 | direct |
| A5 | sublinear f-I "due to the relative refractory period" | qualitative | Kazama & Wilson 2008 | asserted, "data not shown" |
| A6 | 500-ms mean at saturating private input | Rmax 144-170 spikes/s (≈165 typical) | Olsen 2010 | direct (circuit-level, baseline-subtracted) |
| A7 | response shape at strong input | peak/mean ≈2.0; peak ≈300 at ≈150 ms; ≈0.43-0.48 of peak at 500 ms | Olsen Fig. 8B,C; Bhandawat Fig. 1b, 2a | direct (fig.) |
| A8 | published PN LIF | 2-ms absolute refractory period, Vth −40, reset −55, Vrest −55 mV | Jeanne & Wilson 2015 suppl. | choice (validated near threshold only) |
| A9 | an AHP or relative refractory period with measured amplitude or τ | none published for PNs | n/a | gap |

Implications (mine):
- **The data do not support capping PN firing with a long refractory period.**
  - Flies' PNs reach ≈300 spikes/s in their first 50-100 ms (A2, A7). A refractory period long enough to bring
    brainfly's 330-350 spikes/s 500-ms mean down to ≈165 (≈6 ms absolute, derived as 1/165 s) would also clip these
    peaks to ≤165.
- **The intrinsic part must allow ≥300 Hz transiently and not adapt over hundreds of ms (A4).** Slow adaptation currents
  are excluded at ≥100 Hz. A fast relative refractory period recovering within a few ms is not excluded but is not
  measured.
  - Example, to be tuned against A2/A3 under brainfly's own drive: t_ref = 2-3 ms, plus a spike-triggered threshold
    jump of a few mV decaying with τ ≈ 2-5 ms.
- **The decline from peak to plateau is not intrinsic (A4).** Kazama & Wilson attribute it to ORN→PN depression; Nagel
  2015 adds slowly growing presynaptic inhibition. Measured depression parameters:
  - "f = 0.78 and τ = 893 ms" (10-Hz train; Nagel 2015 Fig. 1c, n = 19 PNs).
  - Fast component "f = 0.77, and τ = 1006 ms"; slow (curare-resistant) component "f = 0.91, τ = 629 ms".
  - At 50 Hz the uEPSC is ≈0-10% of its initial amplitude by 100 ms (Kazama & Wilson Fig. 8F, fig.).
  - Without depression, a model PN driven by a sustained 160-Hz ORN input has no mechanism, besides inhibition, to fall
    from ≈300 to ≈130-165.
- **One unresolved tension.** A3 (≈164 sustained under current) and A2 (≈300 in odor peaks) can both hold only if
  current-driven firing above ≈164 is possible briefly but not sustained.
  - The paper's phrase "can fire constantly" is compatible with that reading, but it does not show it.
  - If brainfly needs an intrinsic ceiling, make it use-dependent on a ≥50-ms timescale, not a fixed refractory period
    (mine). An example is a voltage- or rate-driven threshold rise that is small at ≤100 Hz, per A4.
- **Test targets for brainfly's protocol** (one glomerulus's ORNs at 5-160 Hz for 0.5 s):
  - 500-ms mean ≤ ≈170 at the top ORN rates;
  - peak 50-ms bin ≈250-310 at ≈100-150 ms after drive onset (shift by ORN latency);
  - value at 450-500 ms ≈0.4-0.5 of the peak;
  - half-maximum mean at ORN ≈12-16 spikes/s (σ for DM4, DL5, VM7);
  - spontaneous PN rate 1-9 spikes/s (Kazama & Wilson 2009 "typically 1–5"; Wilson 2004 5 ± 0.7; Jeanne & Wilson DA1
    8.6 ± 6.3).

### B. LN response time course

| # | constraint | value | source | status |
|---|---|---|---|---|
| B1 | population-mean LN onset transient, fast odor step | peak ≈43 spikes/s (20-ms smoothing) at ≈15-25 ms; half-width ≈26 ms (≈24 ms unsmoothed) | Nagel 2015 Fig. 5b, n = 45 | direct (fig.), derived width |
| B2 | population-mean LN rate by window | 0-50 ms ≈22; 50-100 ≈13; 100-200 ≈8; 0.2-0.5 s ≈6; 1-2 s ≈3 (baseline ≈4); after offset ≈7-11 for ≈1 s | Nagel 2015 Fig. 5b | direct (fig.) |
| B3 | population PSTH, standard olfactometer, 10 odors | peak ≈22-26 at ≈150 ms after nominal onset (≈50 ms after arrival); at 0.5 s ≈7 (pheromone-avoiding) or ≈15 (others) | Chou 2010 Fig. 5d, n = 9 + 84 | direct (fig.) |
| B4 | share of LN spikes in the first 100 ms of a 1-s response | 14-43% by Gal4 line; ≈18% vs ≈29% by class | Chou 2010 Figs. 4c, 5d | direct |
| B5 | LN subpopulations | ON and OFF continuum; fast and slow; pan-glomerular 28%, often inhibited | Nagel & Wilson 2016; Chou 2010 | direct (qualitative) |
| B6 | LN synaptic excitation more transient than PN excitation | late/peak current ratio ≈0 (LN) vs ≈0.25 (PN) | Nagel 2015 Fig. 5f, n = 22 vs 9 | direct (fig.) |
| B7 | ORN→LN depression | f = 0.75, τ = 1566 ms | Nagel & Wilson 2016 | direct |
| B8 | LN rest | 2.3-4.6 spikes/s (lines up to 16.8) | Wilson & Laurent 2005; Nagel 2015; Chou 2010 | direct |
| B9 | spike-level LN synchrony at onset | not measured; ≈10-Hz phase-locking appears only after delays up to 500 ms | Tanaka 2009 | gap / indirect |

Implications (mine):
- brainfly's LN onset (≈77 spikes/s per LN over 0-50 ms) is ≈3.5× the fly population mean (≈22) and ≈1.8× the fly
  peak with 20-ms smoothing (≈43) (derived: 77/22 and 77/43).
- Its later 8-10 spikes/s is close to flies' 0.1-0.5 s level (≈6-8 in Nagel; ≈10-15 in Chou). It lacks two fly
  features: below-baseline firing late in long odors, and an OFF rebound.
- A per-LN onset rate of ≈20-45 spikes/s for ON cells is closer to the data. A fraction of LNs (OFF and pan-glomerular)
  should be suppressed rather than excited. ORN→LN synapses should depress more than ORN→PN (B7) so that LN responses
  are more transient than PN responses (B6).

### C. Inhibition onset (cross-reference; magnitudes in presynaptic_inhibition.md)

- **Filter.** Effective presynaptic inhibition ≈ LN population rate convolved with an alpha function, τ ≈ 25 ms
  (Nagel 2015 fit; direct ChR2 data, n = 7).
  - Measured step response: 50% at ≈50-70 ms, 90% at ≈150-160 ms (fig.). This is somewhat slower than the τ = 25 ms
    alpha (42 and 97 ms, derived), so τ ≈ 35-40 ms would match the digitized 50%/90% times better (mine; the authors'
    fit says 25).
- **Consequence.** In flies, inhibition peaks ≈100 ms after the LN burst and outlasts it (Nagel 2015 Fig. 6a). The
  GABA-B part lets the first ≈60 ms of a PN response through (Olsen & Wilson 2008 Fig. 5a, one cell). If brainfly's
  inhibition is strongest at onset, it acts too early.
  - Nagel 2015's model shows that too-early inhibition attenuates the PN peak and slows its onset (Fig. 7e).

### Conflicts and gaps

- **Missing measurements.** No direct PN refractory-period, AHP, spike-width or in vivo f-I measurement was found. The
  "relative refractory period" (Kazama & Wilson 2008) is "data not shown"; Olsen 2010 cites it.
- **Sample-size inconsistencies.**
  - Kazama & Wilson 2008 give n = 26 and 9 (Fig. 4D) but n = 26 and 4 (Fig. S2 text) for the Kir2.1 input-resistance
    comparison.
  - Iniguez 2013's legend says n = 16 and 15, but the panels say n = 18; its resistances are printed in "mΩ".
- **Threshold measures.** The somatic "threshold" of −29.7 mV (Huang 2010) is not the SIZ threshold. The soma is
  electrotonically distant and seal-depolarized by ≈10 mV (Gouwens & Wilson 2009). Jeanne & Wilson's ≈10 mV
  distance-to-threshold is the more usable number.
- **Units.** Jeanne & Wilson 2015's model lists "Cm 0.117 pF", which must be nF.
- **Olsen & Wilson 2008 Fig. 3b,c timing.** The odor bar spans ≈1.0 s on the plotted time axis (ticks every 178.5 px
  per s; bar 537-717 px). The legend and methods say 500 ms. Treat the EPSC-sampling times as relative to the bar's
  start.
- **Not read in full.** The Seki 2010 LN class numbers (AHP amplitudes, adaptation) and the main texts of Huang 2010
  and Wilson 2004 were inaccessible.
