# Kenyon cell integration of PN input: time course, summation and short-term plasticity

Read 2026-10-10. Adds to `kenyon_cell_odor_responses.md` (Turner 2008 summary), `kc_classes_and_apl.md` (per-class
excitability, APL), `../Rung 4 resting state data/short_term_plasticity.md` §3.3 (the PN → KC rows) and
`../Rung 4 resting state data/adaptation.md` (intrinsic rows). The question: how should brainfly model the PN → KC synapse
(depression per spike, recovery) and Kenyon cell (KC) integration (membrane time constant)?

Conventions:
- Quotes are verbatim from the full text or legends. Citation numbers inside quotes are dropped.
- (fig., approx.): measured off the figure by pixel tracing against the axis ticks or scale bars named with each value,
  good to roughly ±5-10% of full scale unless stated. "(fig., by eye)" marks values only read visually.
- (derived): my own arithmetic. Fits marked "fit" are least-squares single exponentials to traced curves.
- [other insect]: not Drosophila.
- "Not reported": searched in the full text and legends and not found.
- CC: "connected claws", Gruntman & Turner's term for claws contacted by a ChR2-expressing PN bouton.
- Gruntman & Turner figure letters are the published (Nature) ones. The PMC author manuscript shows the same figure image
  but its legend lists Fig. 3's panels in a different order (manuscript "b" = rasters = published 3c, manuscript "c" =
  PN rates = published 3f, manuscript "d"/"e" = published 3d/3g, manuscript "f"/"g" = published 3b/3e). The text's panel
  calls follow the manuscript order.

## Summary

1. **The PN drive in Gruntman & Turner's optogenetic experiment is not constant.** ChR2 in the 13 Mz19 PNs (DA1, DC3,
   VA1d) gives about 335 Hz at light onset, 184 Hz at 25 ms, 137 Hz at 50 ms and 110-119 Hz from 100 to 250 ms (Fig. 3f,
   mean of 8 PNs, fig., approx.). A 25 ms pulse "evokes 7 PN spikes on average during the light pulse" (text).
2. **KC voltage under that drive** (Fig. 4a, averages by connected claws, baseline about −55 mV, 250 ms light; fig., approx.):
   - 1 CC (n = 17): +4.0 mV at 30 ms, highest +4.5 mV at about 60 ms, +4.1 mV at 99 ms.
   - 2 CC (n = 14): +7.0 mV at 30 ms, still rising to +9.8 mV at about 80 ms.
   - 3 CC (n = 6): +8.9 mV at 30 ms, +10.5 mV at 99 ms.
   - 5 CC (n = 2): +8.1 mV at 30 ms, highest +8.6 mV at 35-40 ms, then down to +6.8 mV at 99 ms (−22%).
   - The response starts about 7 ms after light onset. 10-90% rise: about 22 ms (1 CC), 20 ms (5 CC), 32-39 ms (2-3 CC)
     (derived from the traces).
   - Peak size stops growing between 25 and 50 ms of light (Fig. 4b): 1 CC 4.0, 4.5 and 4.4 mV for 25, 50 and 250 ms.
   - The paper: "The plateau occurred roughly 30 ms following stimulus onset, irrespective of the number of activated
     claws."
3. **Unitary (single-claw) EPSPs** (Supp. Fig. 6; first EPSP of 25 ms trains; 16 one-claw KCs, 270 EPSPs; fig., approx.):
   - Cell medians 0.75-1.92 mV.
   - Pooled: mean about 1.5 mV, median about 1.2, mode about 0.75; about 24% are above 2 mV. One cell has a 6.7 mV
     outlier.
   - This matches Turner's spontaneous EPSPs (1.4 ± 0.8 mV, median 1.2) and Groschner's αβc EPSPs (about 1.25 mV).
   - Gruntman & Turner report no unitary EPSP kinetics (Not reported).
4. **How fast PN-evoked depolarization decays** (Gruntman & Turner; fig., approx., fits):
   - After 1-2 ms light pulses the averaged responses decay with τ ≈ 35-60 ms (1, 3 and 5 CC) and τ ≈ 110 ms (2 CC).
   - One KC's response to 10 ms of light peaks at about 75 ms and decays with τ ≈ 150-200 ms.
   - A 3 ms somatic current pulse decays with a fast component (≈ 8.5 ms) and then a slow one (≈ 100 ms).
   - None of these is the 11.5 ms of Turner 2008.
5. **Turner 2008, checked in the PDF.**
   - EPSPs: spontaneous "well-isolated" events picked by eye (50 EPSPs from 7 KCs held at −58 ± 2 mV). 10-90% rise
     2.1 ± 0.5 ms; single-exponential decay 11.5 ± 5.3 ms.
   - EPSCs (Vhold −60 mV; 50 EPSCs, 5 flies): rise 0.9 ± 0.4 ms, decay 2.8 ± 1.2 ms.
   - Somatic τ_m is "very long (>200 ms)"; R_in > 10 GΩ.
   - Spikes per response: αβ 2.2 ± 1.2, α′β′ 4.9 ± 3.0. Responses were counted in 200 ms bins over 0-2 s after a
     500 ms odor. "Average KC response profiles were single-peaked and closely followed the stimulus time course in all
     KC types."
6. **Groschner 2018 (αβc KCs, in vivo, 21-23 °C).**
   - Fig. 2: τ_m ≈ 189 ms and R_m ≈ 11.5 GΩ (n = 108); α′β′ τ_m ≈ 118 ms and R_m ≈ 6.8 GΩ (n = 18) (fig., approx.).
   - Fig. S3: spontaneous EPSPs ≈ 1.25 mV (n = 36), decaying with τ ≈ 263 ms (n = 31). The average EPSP is still at 95%
     of its peak 20 ms after the peak, 68% at 100 ms and 46% at 200 ms (fig., approx.). EPSC ≈ −3.6 pA, τ ≈ 2.1 ms at
     −90 mV (n = 27).
   - Under 10 Hz antennal-nerve stimulation the voltage steps up by about 1-2.6 mV per EPSP (one step 0.4 mV) and keeps
     most of each step until the next pulse 100 ms later (τ ≈ 180-620 ms in the one cell shown; fig., approx.).
   - Text: "even EPSPs spaced 50 or even 100 ms apart could add up sufficiently to drive spiking".
7. **Nobody has tested what causes the plateau.**
   - Gruntman & Turner excluded voltage-dependent boosting: summation was passive, and responses were smaller at
     depolarized holding potentials. They confirmed spike-dependent nicotinic transmission (TTX, mecamylamine).
   - They did no picrotoxin, APL-block or paired-pulse test: "inhibitory circuit elements could potentially play an
     important role in controlling this selectivity, a possibility we have not addressed here".
   - Inada 2017 used the same Mz19 PNs with ReaChR and 1 s of light, ex vivo (fig., approx.):
     - KC depolarization peaks at 0.26-0.46 s, at about +9.5 mV for the strongest light.
     - It falls back to baseline before the light ends, then −8 mV of offset inhibition follows.
     - "Inhibition followed excitation by several hundred ms".
     - PTX + CGP cut the offset inhibition from about −6 to about −2.5 mV.
8. **No Drosophila measurement of PN → KC short-term plasticity exists.** Checked: Gruntman & Turner, Groschner, Inada,
   Turner, Murthy, and web searches.
   - Locust [other insect]: no paired-pulse facilitation or depression at intervals of 0-50, 50-100 and 100-150 ms
     (p = 0.37, 0.82, 0.84; Jortner 2007).
   - Indirect fly evidence comes from Groschner: one αβc KC's 10 Hz nerve-evoked EPSCs are 5.9, 6.1, 3.4, 4.3, 4.9, 5.0
     and 4.1 pA (fig., approx.; one trial; whole ORN → PN → KC pathway). The within-trial CV of 0.44 is "comparable to
     that attributed to quantal variability".
   - Sato 2018 found AL → MB depression lasting at least 30 min after 40 or more trains of 30 pulses at 100 Hz. That is
     long-term, not short-term, plasticity.
9. **When KC spikes happen in odor responses.**
   - αβc KCs, 1 s odors (Murthy 2008):
     - The depolarization peaks 0.15-0.3 s after the valve opens. By 0.95 s it is at a median of about 40% of its peak
       (range: below baseline to about 80%; 26 KC-odor pairs with peaks ≥ 10 mV; fig., approx.).
     - Strong spiking responses are bursts of about 5-12 spikes per trial within about 0.1-0.55 s. Weak ones are 1-2
       spikes at about 0.1-0.2 s. Some cells fire off responses after 1 s.
   - Turner's example rasters (500 ms odor; 6 responses in 3 KCs; fig., approx.):
     - First spike 89-438 ms after the valve opens; 2.7-8 spikes per trial.
     - 23-100% of spikes fall within 200 ms of the first; median ISI 36-89 ms.
     - Firing lasts to the odor's end and sometimes 0.2-0.4 s beyond.
   - Groschner: first spikes come < 300 ms after a tenfold concentration step.
   - Honeybee [other insect]: KC onset "within the first 200 ms" and "brief phasic responses".
   - Gruntman & Turner, light (fig., by eye): a 4-claw KC fires its first spike about 20-30 ms after light onset in nearly
     every trial, then keeps firing irregularly through 250 ms of light.
10. **For the model (details below).**
    - Point-neuron limit: no single parameter set meets all three constraints. In an LIF a single EPSP decays with τ_m,
      so Turner's 11.5 ms (1.3% left after 50 ms) and Groschner's summation over 50-100 ms (which needs τ ≳ 150 ms; 263
      ms leaves 83% and 68%) exclude each other. Depression changes EPSP amplitudes, not their decay.
    - Gruntman & Turner's fast plateau needs no depression. Their PN rate itself falls from 335 to 115 Hz, and a 20-50 ms
      integration time turns that into a flat plateau by about 30 ms.
      - τ_m = 11.5 ms instead predicts an early peak and a 20-40% sag, which they did not see.
      - τ_m = 189 ms predicts a voltage still climbing at 250 ms, unless the synapse depresses to x_ss ≈ 0.1-0.15 at
        115 Hz.
    - Recommendations:
      - τ_m 20-50 ms.
      - PN → KC depression none to mild (f 0.85-1.0, τ_rec ≈ 0.05-0.2 s).
      - Weights scaled so a single PSP peaks at 1.2-1.5 mV and the steady depolarization per connection at ≈ 115 Hz is
        ≈ 4-4.5 mV.
      - Not rung 4's PN depression (0.85, 0.8 s): x_ss = 0.068 at 115 Hz gives 0.24 mV per connection in the current
        model, against Gruntman & Turner's 4.4 mV.
    - These changes will not cut spikes per response. Drive calibrated to Gruntman & Turner at 40 Hz is 1.6-2.8 mV per
      connection, against the current model's 1.2 mV. Flies' temporal sparsening tracks a KC depolarization that falls to
      about 40% of its peak within 1 s, and APL inhibition that lags by several hundred ms.

---

## 1. Gruntman & Turner 2013, Nat Neurosci 16:1821 ([PMC3908930](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/))

Full text (PMC efetch XML), main figures and supplementary figures (Nature's integrated supplementary information).

### 1.1 Preparation

- In vivo whole-cell KC recordings. "4 to 7 day old heterozygous females generated by crossing Mz19-Gal4 … to
  UAS-ChR2-YFP", fed all-trans-retinal. "This driver labels 13 PNs from 3 different glomeruli (DA1, DC3 and VA1d)."
- "the antennae were surgically removed to reduce baseline synaptic activity".
- Light: blue LED (470 nm), wide field through the 60× objective. "Photostimulus durations of 1, 2, 5, 10, 25, 50, 100
  and 250 ms were presented in a randomly interleaved fashion."
- "Whole cell recordings from KCs were as described" (Turner 2008). Temperature: Not reported.
- Sample: "We recorded from 80 KCs, of which 39 exhibited a clear synaptic response upon PN stimulation and were
  adequately filled to visualize the entire dendritic tree." The connected KCs had 1, 2, 3 or 5 CC (n = 17, 14, 6, 2).
- Response magnitude, quoted: "We calculated the magnitude of KC responses to photostimulation by averaging membrane
  potential traces for each stimulus duration and then measuring the difference between the peak of the response and
  baseline."

### 1.2 PN firing during the light (Fig. 3c rasters, Fig. 3f rates)

- "Cell-attached recordings in PNs confirmed that light-evoked spiking rates were similar to those observed during strong
  odor responses (Fig. 3b), although the dynamics of PN spiking were different, as there was a transient peak in firing
  that was more prominent with ChR2-based stimulation than in a typical odor response (Fig. 3c)" (manuscript panel
  letters; published 3c and 3f).
- Legend (published 3f): "Mean projection neuron spiking rates (n = 8) obtained with different photostimulation durations."
- The 250 ms trace (fig., approx.). Calibration: y labels 0/100/200/300 Hz, 81.8 px per 100 Hz; x labels 0/200/400 ms,
  0.67 px/ms (1.5 ms per pixel); the trace centre line was traced.

| Time from light onset (ms) | ≈ 0-5 (peak) | 15 | 25 | 30 | 50 | 100 | 200 | 240 | ≈ 255-265 |
|---|---|---|---|---|---|---|---|---|---|
| PN rate (Hz) | 335 | 240 | 184 | 168 | 137 | 119 | 111 | 110 | falls to 0 |

- r(t) ≈ 112 + 223·e^(−t/22 ms) Hz fits these within about 10% from 15 ms on (derived).
- "The 25 msec stimulation evokes 7 PN spikes on average during the light pulse, so KCs with multiple PN connections
  receive high frequency input from several PNs in this brief period." Integrating the rate over 0-25 ms gives about 6
  spikes, consistent with this (derived). A 250 ms pulse gives about 34 spikes per PN (derived).
- Each claw contacts one PN bouton: "each KC claw contacts a single PN bouton". In a few cases one claw contacted more
  than one labelled bouton (Supp. Fig. 2).

### 1.3 KC membrane potential under the light

- Text: "KCs responded with an initial depolarization, which subsequently plateaued at a steady membrane potential
  (Fig. 4a). The plateau occurred roughly 30 ms following stimulus onset, irrespective of the number of activated claws.
  After this point, even though PN spiking persisted at >100 spikes/sec, the membrane potential got no closer to spike
  threshold. However, the rate of depolarization within the initial time window was greater when more claws were
  activated (Supplementary Fig. 4). Consequently, the membrane potential climbed to a higher level for KCs with more
  activated claws (Fig. 4b)."
- Fig. 4a legend: "Average timecourses of KC membrane potential in response to different durations of photostimulation
  (colorbar). KC responses are grouped according to the number of claws receiving direct PN input (connected claws, CC)."
- The 250 ms (black) averages (fig., approx.). Calibration: y ticks −45/−50/−55 mV at 14.8 px/mV; x ticks 0/50/100 ms at
  3.38 px/ms. Fig. 4a shows only 0-100 ms. "Δ" is change from the pre-light baseline.

| CC (n) | Baseline | Δ at 18 ms | Δ at 30 ms | Δ at 50 ms | Highest Δ in 0-100 ms | Δ at 99 ms | 90% of highest reached at |
|---|---|---|---|---|---|---|---|
| 1 (17) | −55.2 mV | +2.5 | +4.0 | +4.4 | +4.5 at ≈ 60 ms | +4.1 | ≈ 30 ms |
| 2 (14) | −54.8 | +4.2 | +7.0 | +8.9 | +9.8 at ≈ 80 ms | +9.3 | ≈ 49 ms |
| 3 (6) | −55.0 | +6.3 | +8.9 | +10.0 | +10.5 at 99 ms (still rising) | +10.5 | ≈ 38-40 ms |
| 5 (2) | −55.1 | +5.4 | +8.1 | +7.7 | +8.6 at 35-40 ms | +6.8 | ≈ 28 ms |

- The onset is about 6-8 ms after light onset for all groups (derived). 10-90% rise of the 0-100 ms response: ≈ 22 ms
  (1 CC), 39 ms (2 CC), 32 ms (3 CC), 20 ms (5 CC) (derived).
- So the "30 ms plateau" is the fast phase. In 2-3 CC KCs the voltage keeps creeping up by another 10-30% to 60-100 ms;
  in 5 CC KCs it falls 22% by 100 ms.
- Fig. 4b, peak response by light duration (fig., approx.; y ticks 0/4/8/12 mV at 28.5 px/mV; the 2 CC point at 1 ms
  could not be separated from overlapping symbols):

| Light (ms) | 1 | 2 | 5 | 10 | 25 | 50 | 100 | 250 |
|---|---|---|---|---|---|---|---|---|
| 1 CC (mV) | ≈ 1.0 | 1.5 | 2.2 | 2.6 | 4.0 | 4.5 | 4.4 | 4.4 |
| 2 CC | – | ≈ 2.1-2.4 | 3.5 | 5.0 | 7.4 | 9.0 | 9.7 | 9.9 |
| 3 CC | 1.2 | ≈ 2.2 | 4.8 | 6.2 | 8.9 | 10.1 | 10.6 | 10.4 |
| 5 CC | 1.5 | 3.0 | 4.5 | 5.7 | 8.1 | 8.4 | 8.6 | 8.4 |

- Supp. Fig. 4 legend: "Slope was calculated by fitting a 2nd or 3rd degree polynomial to the rising phase of the
  depolarization, finding the midpoint in the response and analytically calculating the derivative."
  - Mid-rise dV/dt for 250 ms light: ≈ 0.15 (1 CC), 0.21 (2 CC), 0.31 (3 CC), 0.24 mV/ms (5 CC).
  - The largest values come with 10-25 ms light: ≈ 0.18, 0.27, 0.41, 0.37 mV/ms.
  - fig., approx.; y ticks 0/0.25/0.50 mV/ms.
- **Example KC (Fig. 3d)**: "Note that for this KC, the strongest stimulation evoked a response containing several spikes".
  Mean of 50 trials, traced (fig., approx.; y labels −30/−55 mV at 4.1 px/mV; x labels 0/200 ms at 0.67 px/ms).
  - 250 ms light: from −52 mV to +8 mV at 30 ms, +12.4 mV at 50 ms and +15.8 mV at 100 ms. Peak ≈ +17 mV at ≈ 120 ms,
    then +13.8 mV at 200 ms and +12.5 mV at 240 ms: −25% from the peak with the light still on.
  - After light off it falls to +6 mV within 40 ms and to about +1 mV by 90 ms.
  - With 100 ms of light it rises to +16.8 mV at 100 ms and decays with τ ≈ 75 ms after the light ends.
  - So in this strongly driven KC the rise lasts about 100 ms, not 30.

### 1.4 How fast PN-evoked responses decay

- **Brief light** (Fig. 4a yellow and orange traces). Fits over 35-99 ms after light onset (fig., approx., fit), with the
  baseline either fixed at the pre-light level or left free:

| CC | 1 ms light: peak; τ (fixed / free baseline) | 2 ms light: peak; τ (fixed / free) |
|---|---|---|
| 1 | +1.35 mV at 22-25 ms; 47 / 58 ms | +1.86 mV at 25 ms; 49 / 35 ms |
| 2 | – ; 109 ms (free fit unconstrained) | – ; 108 ms (free fit unconstrained) |
| 3 | – ; 37 / 41 ms | – ; 48 / 52 ms |
| 5 | – ; 49 / 29 ms | – ; 54 / 33 ms |

  The PN rasters for 1-2 ms light (Fig. 3c) end within about 20-30 ms of onset, so most of the 35-99 ms window follows
  PN input (fig., by eye).
- **Fig. 4d** shows one KC (light with somatic current; fig., approx.; y ticks −50/−55/−60 mV at 18.2 px/mV; x labels
  0/100/200 ms at 1.49 px/ms).
  - Current alone, 3 ms pulse: +7.7 mV peak. A fast decay (τ ≈ 8.5 ms) takes it to about 40% of the peak, then a slow
    decay follows (τ ≈ 100 ms with a free baseline).
  - Light alone, 10 ms: from −61.8 mV, the onset comes at about 6-8 ms. It reaches +5 mV at 30 ms and peaks at +6.3 mV
    at ≈ 75 ms, long after PN firing has stopped, then decays with τ ≈ 150-200 ms.
- Fig. 4e: observed/expected for light plus current is ≈ 1.0 for timings of −50 to +50 ms (n = 7 KCs). Text: "KCs are not
  particularly sensitive to the relative timing of these two inputs".
- Gruntman & Turner give no unitary EPSP or EPSC rise or decay (Not reported). The words "kinetic", "decay", "EPSC",
  "time constant", "depress", "adapt", "GABA", "picrotoxin" and "APL" do not occur in the body text.

### 1.5 Single-claw EPSP amplitudes (Supp. Fig. 6)

- Methods: "To quantify the range of PN-KC synaptic strengths, we measured the amplitudes of individual EPSPs from KCs
  connected via a single claw. Using the 25 ms photostimulation trials, we selected individual trials in which EPSPs were
  identifiable, manually marked the base and peak of the first EPSP in each train, and took the difference as the EPSP
  amplitude."
- Legend: "Left: Distribution of EPSP sizes for KCs (n=16) connected via only one claw. Measurements are from the first
  EPSP in response to 25 ms photostimulation. Asterisk above cell 14 represents an outlier beyond the axis limit (6.7 mV).
  Mean number of EPSPs measured per cell: 17 ± 8. Right: Histogram of EPSP amplitudes from all 16 KCs (n=270 EPSPs)."
- Per-cell medians, in cell order (fig., approx.; y ticks 0-4 mV at 271 px/mV): 0.75, 0.79, 0.79, 0.86, 0.91, 1.04, 1.14,
  1.20, 1.34, 1.40, 1.50, 1.52, 1.67, 1.68, 1.75, 1.92 mV. Their mean is 1.27 mV (derived).
- Pooled histogram, weighted by its curve (derived): mean ≈ 1.5 mV, median ≈ 1.2, mode ≈ 0.75; ≈ 24% of EPSPs are above
  2 mV.
- Caveat: only trials with identifiable EPSPs were measured, which biases the values toward larger events and leaves out
  failures.

### 1.6 Additivity, and how many claws a KC needs to spike

- "We found that response amplitudes of KCs with two connected claws were not significantly different from doubling the
  responses observed upon activation of a single claw. For KCs with three connected claws, there was a trend towards a
  sublinear interaction between claws; this was more prominent with the KCs we found connected via five claws".
  - Fig. 4c: 5 CC gives ≈ 8.4 mV where the linear prediction is ≈ 22 mV (fig., by eye).
  - Discussion: "claws interact linearly when small numbers are coactive, and sub-linearly when larger numbers are
    stimulated, likely due to shunting effects on the dendritic tree."
- Voltage dependence: "We optogenetically stimulated inputs while holding the KC at different membrane potentials, but
  found no indication of voltage-dependent amplification of the synaptic response (Supplementary Fig. 5a, b).
  Additionally, current injection experiments showed no evidence of a non-linear component in the KC membrane potential
  response, other than spike threshold (Supplementary Fig. 5c, d)." Supp. Fig. 5 legend: "Response magnitude tended to
  decrease at more depolarized holding potentials, as expected of a passive (i.e. non-voltage-dependent) membrane
  potential response."
- Spiking:
  - "Only 2 of 39 KCs climbed above spike threshold with sufficient reliability to resemble a significant odor response
    (i.e. >0.5 spikes/trial). These responses were found only in cells with three or five connected claws (Fig. 5a)."
  - "In particular, there was a prominent increase in the proportion of spiking responses between 3 and 4 contacted
    claws. KCs have 7 claws on average (Supplementary Fig. 3), so these results suggest that strongly activating more than
    half of the dendritic inputs is required to drive a KC to spike."
  - Fig. 5d, proportion of KCs spiking (fig., approx.): 1 CC ≈ 0.04, 2 CC ≈ 0.12, 3 CC ≈ 0.08, 4-6 CC ≈ 0.57.
  - "Surprisingly, we found that the number of spikes evoked by photostimulation was not strongly dependent on the number
    of connected claws (Fig. 5c; linear regression R2= 0.02)." Fig. 5c spikes per trial, 13 spiking KCs (fig., by eye):
    1 CC 1.6, 1.8; 2 CC 0.4, 0.7, 3.8; 3 CC 0.45; 4 CC 0.7, 1.0, 1.5, 2.2, 4.5, 4.9; 6 CC 1.4. Spike counts used the
    window "from stimulus onset to 200 ms after stimulus offset", minus baseline. The light duration behind Fig. 5c is not
    stated.
  - "even a very small number of KCs that spiked when connected via only a single claw (2 of 191 total recorded KCs)".
- Spike timing under light (Fig. 5b, 250 ms; fig., by eye):
  - 6 CC KC: 1-2 spikes at about 20-50 ms.
  - 4 CC KC: a first spike at about 20-30 ms in nearly every trial, then irregular firing to the light's end, about 5
    spikes per trial in total.
  - 1 CC KC: about 2-4 spikes spread over 40-250 ms.

### 1.7 Was the plateau's cause tested?

- Tested:
  - Spike-dependent nicotinic transmission. "Pharmacological blockade showed that KC responses were mediated by
    spike-dependent synaptic transmission (Supplementary Fig. 1)" (1 μM TTX; 100 μM mecamylamine).
  - The absence of voltage-dependent boosting (§1.6).
- Not tested: depression, inhibition (no picrotoxin, CGP or APL block) and intrinsic adaptation. The authors write:
  "Moreover, inhibitory circuit elements could potentially play an important role in controlling this selectivity, a
  possibility we have not addressed here".
- Their discussion of what drives KCs: "it seems likely that the main factor driving KCs to spike threshold in
  Drosophila, like Dp neurons, is the slow wave of depolarization that arises from the summation of PN input from several
  dendritic claws."
- The PN rate's own fall (§1.2) is shown in their figure but is not offered as an explanation. For what it implies, see
  "For the model".

---

## 2. Turner, Bazhenov & Laurent 2008, J Neurophysiol 99:734 ([PDF](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf))

### 2.1 Preparation

- "All flies were wild-type Canton-S females. For KC recordings, the animals were aged 1–2 days posteclosion".
- Recording: pressure-polished pipettes, Axoclamp-2B in bridge mode, "Signals were filtered at 3 kHz and acquired at 10
  kHz". Temperature: Not reported.
- "Input resistance at the soma was >10 GΩ; KCs were held at −58 ± 2 (SD) mV in current clamp."

### 2.2 How EPSPs were measured, and their kinetics

- Methods: "We identified excitatory postsynaptic potentials (EPSPs) using a time-derivative-based algorithm." Also: "We
  constructed average waveforms from 49 well-isolated EPSPs (7 different KC recordings, and 7 EPSPs per recording) and 50
  excitatory postsynaptic currents (EPSCs, 5 different recordings, 10 EPSCs per recording), identified by eye."
- Results:
  - "EPSP kinetics were surprisingly fast for neurons with input resistance >10 GΩ (Fig. 3D). We examined the time course
    of 50 well-isolated EPSPs from seven independent recordings. EPSP 10–90% rise times were 2.1 ± 0.5 ms, and decays
    were well fit with a single exponential (11.5 ± 5.3 ms)."
  - "We measured the kinetics of 50 EPSCs from voltage-clamp recordings (Vhold = −60 mV) in five different flies. EPSC
    rise time was 0.9 ± 0.4 ms, and decay time constant was 2.8 ± 1.2 ms (Fig. 3D)."
  - "Although EPSP kinetics were fast, the membrane time constant, measured at the soma by hyperpolarizing current
    injection, was very long (>200 ms). These observations suggest that EPSP kinetics are determined mostly by synaptic
    (and possibly, voltage-gated) conductances in the dendrites."
- So the EPSPs were spontaneous, not evoked. Both the derivative detector and the selection of "well-isolated" events
  favour fast events.
  - In Fig. 3A (50 ms scale bar) spontaneous EPSPs fall back within about 10-20 ms (fig., by eye).
  - The Fig. 3D average returns near baseline by about 40 ms (fig., by eye).
  - The class of the 7 KCs is not stated.
- Frequency: "their frequency dropped significantly when TTX was added to the saline (control: 19.8 ± 13.2 s−1; TTX: 1.8 ±
  1.3 s−1, n = 8 KCs; Fig. 3B)". Fig. 3E gives 32.6 ± 12.7 s−1 (n = 27).
- Amplitude: "control: 1.4 ± 0.8 mV; TTX: 1.0 ± 0.5 mV".
- Their model: "Model parameters were tuned to produce the experimentally measured EPSP decay time constant: τ = 11.5 ms."
  - Cm = 1.0 μF/cm² and gL = 0.089 mS/cm² give τ = 11.2 ms (derived).
  - Synaptic β = 0.4 ms⁻¹ gives a 2.5 ms current decay (derived).
  - The model has no depression.
- Discussion: "In Drosophila, by contrast, PN:KC convergence is low (∼5% or ∼10 PNs per KC) relative to the minimum
  number of EPSPs needed to get a KC to spike (15 inputs minimum: 21.5 mV from Vrest to Vspike, 1.4 mV EPSP amplitude).
  This implies a need for input amplification and/or temporal summation. Indeed we find no evidence for a periodic voltage
  reset by IPSPs, as seen in locust, allowing considerable temporal integration by KCs."

### 2.3 Odor responses: spikes per class, timing, window

- Stimulus: "The valves controlling odor flow were opened for 500 ms." Also: "air flow rates introduce a delay in the
  arrival of the odor at the fly’s) antennae" (their PSD window starts 100 ms after valve opening).
- Criterion: "KC firing rates were measured in successive 200-ms bins and averaged across all trials. To qualify as a
  response, a KC’s firing rate had to exceed 3.5 SD of baseline firing rate in a window 0 –2 s after odor onset on at
  least half of the trials (typically 3 of 6 trials)."
- Spikes per response: α′/β′ KCs "fired 4.9 ± 3.0 spikes during an odor response, significantly more than α/β KCs (2.2 ±
  1.2; P = 0.007, t-test)." γ: "Only 1 of the 15 γ KCs we tested with this odor set … showed a spiking response", so no
  γ count is given.
- Timing: "Average KC response profiles were single-peaked and closely followed the stimulus time course in all KC
  types."
- Fig. 2E is averaged over all odors, including non-responses, on a 15 s axis (fig., by eye against the 0.2 sp/s ticks):
  αβ peaks at ≈ 0.2 sp/s; α′β′ at ≈ 1.05 sp/s on a ≈ 0.27 sp/s baseline; γ at ≈ 0.35 sp/s. The elevation lasts about
  0.5-1 s from onset.
- Fig. 1D, pentenal: the depolarization and its spikes last the whole 500 ms odor (fig., by eye).
- Fig. 1E-H example rasters (selected spiking KCs, class not given). Spike ticks were detected automatically at 600 dpi.
  Calibration: frame = 0-4 s at 169 px/s, odor shading 1.0-1.5 s. Times are from valve opening (fig., approx.).

| Panel, odor | Trials with spikes | Spikes/trial (range) | First spike, median (range) | Last spike | Share within 200 ms of first spike | Share during the 500 ms odor | Median ISI |
|---|---|---|---|---|---|---|---|
| E, pentenal | 5 | 6.4 (5-9) | 166 ms (163-175) | 485 ms | 0.91 | 1.00 | 36 ms |
| E, 1-hexanol | 5 | 8.0 (6-11) | 101 ms (89-107) | 941 ms | 0.23 | 0.33 | 47 ms |
| F, ethyl propionate | 5 | 2.8 (2-3) | 429 ms (225-438) | 512 ms | 0.79 | 0.86 | 44 ms |
| F, ethyl butyrate | 3 | 2.7 (1-4) | 402 ms (393-417) | 541 ms | 1.00 | 0.88 | 50 ms |
| H, ethyl propionate | 6 | 5.3 (2-7) | 215 ms (206-230) | 692 ms | 0.53 | 0.69 | 89 ms |
| H, ethyl acetate | 4 | 6.2 (4-11) | 273 ms (233-301) | 834 ms | 0.36 | 0.44 | 86 ms |

  The E, 1-hexanol response has an onset burst at 0.09-0.15 s and a second burst at 0.56-0.82 s, after the odor ends.
  Panel G uses dot glyphs. Its 1-hexanol response starts at 0.06-0.31 s and runs to about 0.45 s, with a few spikes up
  to 0.7 s.

---

## 3. Groschner et al. 2018, Cell 173:894 ([PMC5947940](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/))

Full text via PMC efetch; high-resolution figures from the publisher.

### 3.1 Preparation

- "For whole-cell patch-clamp recordings in vivo, male flies aged 6–24 h post-eclosion were prepared as for functional
  imaging, but the perineural sheath was also removed to provide access to KC somata while the antennae and antennal
  nerves were left intact for eliciting odor responses."
- "Signals were acquired at room temperature (21–23°C)"; "Data were corrected for liquid junction potential".
- αβc KCs were labelled with NP7175-GAL4, α′β′ KCs with VT030604-GAL4.

### 3.2 Membrane time constant and input resistance (Fig. 2; methods)

- Methods: "Input resistances were calculated from linear fits of the steady-state voltage changes elicited by 750 ms
  steps of hyperpolarizing currents (1 pA increments, starting at –4 pA) from a pre-pulse potential of –70 ± 5 mV.
  Membrane time constants were determined by fitting a single exponential to the voltage deflection caused by a
  hyperpolarizing 2.5 pA current step lasting 750 ms."
- Wild-type means (fig., approx.; Fig. 2G/P ticks every 5 GΩ, 21.7 px/GΩ; Fig. 2H/Q ticks every 100 ms, 1.09 px/ms):
  - αβc: R_m ≈ 11.5 GΩ, τ_m ≈ 189 ms (n = 108).
  - α′β′: R_m ≈ 6.8 GΩ, τ_m ≈ 118 ms (n = 18).
  These agree with `adaptation.md` (11.6 GΩ, 188 ms).
- FoxP-deficient αβc KCs have "lower input resistances (Rm) (G, p < 0.0001) and shorter membrane time constants (τm)".
- Ex vivo (Chen 2026, values as recorded in `adaptation.md`, not re-read): τ_m ≈ 185, 130 and 125 ms for αβ, α′β′ and γ
  KCs.

### 3.3 Unitary EPSPs and EPSCs (Fig. S3)

- Methods: "EPSP waveforms represent averages of individual, baseline-subtracted EPSPs occurring spontaneously at a
  membrane potential of –70 ± 5 mV. Decay time constants were determined by fitting single exponentials to the averaged
  EPSP waveforms."
- Legend: "FoxP-deficient αβc KCs have lower mEPSP amplitudes (H, p < 0.0036) and shorter decay time constants (τdecay)
  than wild-type cells (I, p = 0.0299). … In 5 αβc KCs of wild-type flies, 1 αβc KC of a FoxP5-SZ-3955 mutant, and 1 αβc
  KC of a FoxPRNAi fly, a satisfactory single-exponential fit to the decaying phase of the EPSP could not be found; these
  cells were excluded from the analyis of τdecay in (I)."
- Wild-type αβc values read from the dotted mean lines (fig., approx.):
  - EPSP peak ≈ 1.25 mV (n = 36; ticks every 0.1 mV, 239 px/mV).
  - EPSP τ_decay ≈ 263 ms (n = 31; ticks every 100 ms, 0.48 px/ms). Single cells range from about 30 to 880 ms (fig., by
    eye).
  - EPSC peak ≈ −3.6 pA at −90 mV (n = 27; ticks every 0.5 pA).
  - EPSC τ_decay ≈ 2.1 ms (n = 27; ticks every 0.5 ms).
  - Spontaneous EPSC rate ≈ 4 Hz (fig., by eye).
- FoxP-deficient cells (fig., by eye): EPSP ≈ 1.1 mV; τ_decay ≈ 140 ms (mutant) and ≈ 165 ms (RNAi).
- Vrontou 2021 (same lab, per `kc_classes_and_apl.md`) gives "1.25 ± 0.05 mV; n = 36 cells".
- The wild-type average EPSP waveform (Fig. S3G), traced (fig., approx.; scale bars 0.5 mV ≈ 124 px, 100 ms = 127 px):
  - 10-90% rise ≈ 5 ms (±1 ms at this resolution).
  - Relative to the peak: 98% at 10 ms after it, 95% at 20 ms, 85% at 50 ms, 68% at 100 ms, 46% at 200 ms.
  - Single-exponential fit τ ≈ 255 ms. No fast component is visible.

### 3.4 Summation of PN input (Fig. 5, Fig. S6)

- Text: "To test for a role of Shal (and, indirectly, of FoxP) in synaptic integration, we recorded from αβc and α’β’ KCs
  in vivo while electrically stimulating 30 synaptic inputs from olfactory projection neurons at different frequencies
  (Figures 5A, 5B, and S6). The majority of evoked events (∼80%) were unitary, as the average synaptic current exceeded
  the average miniature EPSC by 12%–25% (Figure S6). During stimulus trains, the membrane potentials of αβc KCs in
  wild-type flies climbed in a stepwise fashion from resting potential to spike threshold, bridging the average potential
  difference of 8.2 mV by integrating 4–30 synaptic quanta (Figures 5B and 5C). Inputs were summed most efficiently when
  delivered at high frequencies (Figures 5C and 5D), but even EPSPs spaced 50 or even 100 ms apart could add up
  sufficiently to drive spiking (Figure 5B)."
- The stimulus is the antennal nerve, so this is ORN → PN → KC, not isolated PN → KC.
- "30 synaptic inputs" matches trains of about 30 pulses: the Fig. 5C train bars last ≈ 0.33 s at 90 Hz, 0.49 s at 60 Hz
  and 1.0 s at 30 Hz against the 400 ms scale bar (derived).
- Methods: "The amplitude of 50 μs voltage pulses delivered by a constant voltage stimulator (Digitimer) was gradually
  increased until EPSCs or EPSPs could be detected in the recorded KC; the stimulus intensity was then further increased
  by ∼25% to minimize the fraction of transmission failures."
- Also: "The coefficient of variation (CV) of EPSC amplitudes within a trial was 0.440 ± 0.019 (mean ± SEM, n = 22 trials),
  comparable to that attributed to quantal variability at individual excitatory synapses (McAllister and Stevens, 2000).
  Consistent with this interpretation, the variation of mean evoked EPSC amplitudes between trials was smaller than the
  variation within trials (CV = 0.134 ± 0.014; mean ± SEM, n = 3 cells)."
- Fig. S6 legend: "The peak currents of spontaneously occurring miniature EPSCs in 1 μM TTX (mEPSCs, right) averaged
  80–89% of those of eEPSCs."
- Fig. 5B, one αβc KC at 10 Hz, traced (fig., approx.; 4 mV = 112 px, 200 ms = 136 px, 10 pA ≈ 89 px ±10%):
  - EPSP steps: 1.14, 1.60, 1.01, 2.14 and 1.20 mV. The 5th triggers a spike and an AHP to +0.35 mV. Then 2.58 and
    0.44 mV.
  - Depolarization just before pulses 2-5: +0.87, +2.01, +2.15, +3.87 mV. Before pulse 5 the four steps (5.9 mV) are
    65% retained.
  - Decay between pulses before the spike, fitted toward rest: τ ≈ 224, 366, 181, 622 ms. After the spike: ≈ 68 ms.
  - Evoked EPSCs (holding −70 mV): 5.9, 6.1, 3.4, 4.3, 4.9, 5.0, 4.1 pA; the average mEPSC is 3.7 pA. The two-step drop
    after pulse 2 sits within the quantal CV.
- Fig. 5D, wild-type αβc peak ΔVm by frequency (n = 6; fig., approx.; y labels 0/5/10/15 mV, 17.4 px/mV):

| Hz | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| ΔVm (mV) | 5.6 | 6.2 | 8.8 | 9.3 | 9.9 | 10.8 | 10.2 | 11.6 | 11.2 | 12.5 |

  - With TTX: ≈ 1 mV at every frequency.
  - 150 μM Ba²⁺ (Shal block) raises the 10 Hz point to ≈ 9.5 mV, and the curve saturates near 11 mV (fig., by eye).
  - Peaks above the 8.2 mV threshold gap include spiking.
- Interpretation quotes:
  - "spontaneous EPSPs in αβc KCs of FoxP mutants were smaller and decayed faster (Figures S3G–S3I), and evoked EPSPs
    were dissipated more readily (Figure 5C), than those in wild-type cells. As a consequence, opportunities for temporal
    summation of synaptic inputs were curtailed, and only high-frequency stimulation could produce cumulative membrane
    depolarizations that breached action potential threshold".
  - "A long membrane time constant (Figure 2H) provides accumulator memory (Figures 5B and 5C), whereas Shal currents may
    improve accuracy by reducing noise (Figure 7J) and discounting sporadic sensory events (Figures 5C and 5D)."
- Short-term plasticity: Not reported. There is no paired-pulse or train-amplitude analysis.

### 3.5 Odor-response timing

- "In wild-type flies, large fractional increases in odor intensity (from 2 to 20 ppm MCH, a concentration ratio of 0.1)
  evoked action potentials with short latencies (< 300 ms) that were preceded by steep membrane depolarizations (Figures
  7F and 7G)".
- "αβc KCs showed virtually no background spiking activity, regardless of base MCH concentration, and instead responded
  to concentration changes".

---

## 4. Short-term plasticity at PN → KC synapses

- **Drosophila: no paired-pulse, train or recovery measurement found.**
  - Searched: Gruntman & Turner 2013, Groschner 2018, Inada 2017, Turner 2008 and Murthy 2008 (full texts), plus web
    searches for PN-KC paired-pulse, depression and facilitation.
  - The Rung 4 entry "PN → KC and APL ↔ KC: no fly paired-pulse or train data" still stands.
  - No Kohl et al. paper with PN → KC train data was found.
- **Locust [other insect], Jortner, Farivar & Laurent 2007** ([PMC6673743](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673743/),
  quoted from the PMC page):
  - Method: spike-triggered averages of KC voltage on spontaneous PN spikes.
  - "PN–KC EPSPs are very small and mostly distributed around 60–110 μV" (mean 86 ± 44 μV, n = 28).
  - Fig. 6B, C legend: "No evidence is found for paired-pulse facilitation (or depression)."
  - Text: "STAs produced by these selected spikes were, on average, no different from those produced using all spikes
    (p = 0.37, 0.82, 0.84, respectively). This result is inconsistent with significant homosynaptic facilitation and,
    thus, with high failure rates at the PN–KC synapse." The ISI ranges were 0-50, 50-100 and 100-150 ms.
- **Indirect fly evidence (Groschner).** See §3.4: the 10 Hz nerve-evoked EPSCs in one αβc KC show no consistent decline
  after pulse 2, and the within-trial CV is attributed to quantal variability. This covers the whole ORN → PN → KC
  pathway at one frequency.
- **Gruntman & Turner.** They did no paired-pulse test. For what their plateau allows, see "For the model".
- **Inada 2017** ([PDF](https://kazamalab.riken.jp/pdf/Neuron_Inada_2017.pdf)):
  - Ex vivo, about 25 °C. "LED light was pulsated at 80 Hz"; "blue light was sufficient to make the PNs expressing ReaChR
    fire at 200 Hz (Figure S3A)".
  - No PN → KC train-amplitude analysis.
  - Fig. 3B (Mz19 > ReaChR, about 1 s of light; one KC, mean of 3 trials; fig., approx.; 5 mV ≈ 157 px, 1 s = 174 px):

    | Light | Rise | Peak | Later during light | End of light (0.98 s) | Offset |
    |---|---|---|---|---|---|
    | 11 μW | +8.9 mV at 0.2 s | +9.5 mV at 0.26 s | +6.0 mV at 0.5 s; +2.7 mV at 0.7 s | 0 mV | −8.2 mV at 1.4-2.1 s |
    | 1.9 μW | – | +4.6 mV at 0.46 s | – | +1.4 mV | −4.1 mV at 1.5 s |

  - Legend: "Stronger stimulation recruited stronger excitation and offset inhibition."
  - Discussion: "Inhibition followed excitation by several hundred ms and were often strong enough to override the initial
    depolarization (Figures 3B and S3B). This is likely one mechanism that generates spatially … and temporally sparse
    odor representations in KCs".
  - Fig. 3F: offset inhibition 500 ms after the light, about −6 mV in saline and about −2.5 mV with PTX + CGP (n = 10;
    fig., by eye).
  - Depression and inhibition are not separated during the light.
- **Long-term, not short-term: Sato et al. 2018** ([PMC6002214](https://pmc.ncbi.nlm.nih.gov/articles/PMC6002214/); ex vivo
  calcium imaging):
  - "The degree of Ca2+ responses after repetitive AL stimulation is significantly reduced in the dendritic region of MB
    neurons (calyx) compared with those before AL stimulation, and this reduction of Ca2+ responses remains for at least
    30 min."
  - Protocol, as given on the PMC page: test stimuli were "three trains of 30 pulses (100 Hz, 1.0 ms pulse duration …)";
    conditioning was "10–100 trains of 30 pulses (100 Hz …)" at 1 s intervals. Within-train changes: Not reported.

---

## 5. KC odor-response time courses

- **Turner 2008**: §2.3.
- **Murthy, Fiete & Laurent 2008, Neuron** ([PMC2654402](https://pmc.ncbi.nlm.nih.gov/articles/PMC2654402/)). These are
  NP7175 GFP+ "L-LP" KCs, i.e. αβc.
  - Setup: "Odors were presented as 1s pulses during 20s trials in blocks of 6 trials each, on average." "All cells were
    held between −55mV and −70mV, in current-clamp mode". Only KCs with R_in > 10 GΩ were used.
  - Criterion: "a KC was considered responsive to an odor if it produced at least one action potential in the period
    0–2s following stimulus onset, on at least 3 trials." PSTHs: "smoothed with a 30ms Gaussian filter".
  - "“Subthreshold” responses (red, Figure 2B), in contrast, were low-passed voltage responses (see methods) and thus
    include both sub- and supra- threshold odor responses and trials".
  - Fig. 2B, KC24 with isoamyl acetate (fig., by eye; y ticks −20/−40/−60 mV):
    - Vm rises from −60 to about −30 mV within about 0.1 s of response onset.
    - Spikes ride on roughly the first 0.3 s.
    - About −40 mV at 1 s.
  - Fig. 2D, subthreshold responses of 6 KCs to 6 odors, traced. Calibration: shading 0-1 s at about 85 px (11.5-11.9
    ms/px); 0 and 40 mV labels ≈ 107 px apart. 26 KC-odor pairs had peaks ≥ 10 mV:
    - Peaks come 0.15-0.3 s after the valve opens; a few at 0.4-0.46 s.
    - At 0.95 s, Δ/peak has a median of ≈ 0.40 (range −0.47 to 0.82; 17 of 26 between 0.2 and 0.7).
    - Several traces dip below baseline after their peak.
    - fig., approx. Overlapping coloured traces make single values uncertain by several mV.
  - Fig. 2C rasters (0-2 s; fig., by eye, about ±25 ms):
    - KC11 2,3-butanedione: about 6-10 spikes per trial at 0.2-0.4 s.
    - KC12 isoamyl acetate: about 8-12 per trial at 0.15-0.55 s.
    - KC11 ethyl butyrate: 2-3 at 0.08-0.15 s. KC11 ethyl acetate: 1-2 at about 0.15 s.
    - KC11 isoamyl acetate: 3-5 per trial spread over 0.1-1.0 s, plus 2-3 more at 1.0-1.8 s.
    - Single onset spikes at about 0.1-0.2 s: KC14, KC16, KC21.
    - Off responses at 1.1-1.9 s: KC6, KC14, KC16.
- **Groschner 2018**: first spikes "< 300 ms" after a tenfold step (§3.5).
- **Inada 2017** (GCaMP5): "α′/β′ KCs, indeed, responded to ethyl butyrate with shorter latency as compared to the other
  two cell types". These are calcium onsets, not spike times; values not extracted.
- **Honeybee [other insect], Szyszka et al. 2005** (abstract): "the onset of Kenyon cell responses to projection neurons
  occurred within the first 200 ms and complex temporal patterns were transformed into brief phasic responses."
- **Firing-rate ceiling** (Groschner Fig. 2I, R, in `adaptation.md`): αβc ≈ 25 Hz at 5 pA, ≈ 30 Hz at 7 pA; α′β′ ≈ 3 Hz/pA.
  Responding KCs fire at a few to about 40 Hz (derived from the ISIs above).
- **brainfly for comparison** (`experiments/odor_kc_timing.json`, 2026-10-10):
  - Responding KCs fire 10.8-11.1 spikes over the odor's first 1.4 s.
  - First spike at a median of 173-201 ms; spike times spread with an SD of 209-240 ms.
  - No intervals under 10 ms: steady firing at about 8 Hz.
  - The brief describes the model's KCs as firing 4-6 spikes per response, mostly early; the newer run supersedes that.

---

## For the model

### A. What brainfly has (from the repo)

- KCs are current-based LIF neurons with τ_m = 11.5 ms, from Turner's EPSP decay ("In this model a neuron's membrane time
  constant is what sets its EPSP's decay", `odor_probe5.py`).
- Rest is 21.5 mV below threshold. The mean PN → KC connection's peak PSP is 1.4 mV. There is no PN → KC depression.
- `odor_probe5.peak()` models the synaptic current as decaying with τ_s = 5 ms. The arithmetic below assumes τ_s = 5 ms.
  - PSP per spike: V(t) = w·τ_s/(τ_m − τ_s)·(e^(−t/τ_m) − e^(−t/τ_s)), with the current jumping by w per spike (DC gain 1).
  - PSP area per spike = w·τ_s. Steady state V_ss = w·τ_s·r·x_ss, which does not depend on τ_m. Here r is the PN rate
    and x_ss the depression factor.
  - Peak per unit w and area/peak (derived):

| τ_m (ms) | 11.5 | 20 | 30 | 50 | 100 | 189 |
|---|---|---|---|---|---|---|
| PSP peak per unit w | 0.229 | 0.158 | 0.117 | 0.077 | 0.043 | 0.024 |
| Area/peak (ms) | 21.8 | 31.7 | 42.9 | 64.6 | 117 | 209 |

- Current model: w = 1.4/0.229 = 6.11 mV. V_ss per connection = 3.5 mV at 115 Hz and 1.2 mV at 40 Hz (derived).

### B. Turner's decay against Groschner's summation

How much of a single EPSP remains after 50 and 100 ms (derived):

| EPSP decay τ (ms) | 11.5 (Turner) | 20 | 30 | 50 | 118 (α′β′ τ_m) | 189 (αβc τ_m) | 263 (αβc EPSP) |
|---|---|---|---|---|---|---|---|
| Left after 50 ms | 1.3% | 8% | 19% | 37% | 66% | 77% | 83% |
| Left after 100 ms | 0.02% | 0.7% | 4% | 14% | 43% | 59% | 68% |

- In Groschner's one 10 Hz example the depolarization decays between pulses with τ ≈ 180-620 ms, so 58-85% survives each
  100 ms interval (derived: e^(−100/181) to e^(−100/622); §3.4).
- Summing EPSPs 50-100 ms apart to the 8.2 mV gap requires τ well above 100 ms.
- In a point LIF a single EPSP decays with τ_m whatever the synapse does: depression scales amplitudes, not decay. So
  Turner's 11.5 ms and Groschner's summation cannot both hold in one parameter set.
- Turner's fit was of isolated spontaneous EPSPs picked by eye, in unclassified 1-2-day-old female KCs held at −58 mV.
  Groschner averaged spontaneous EPSPs in αβc KCs of 6-24 h males at −70 mV.
- The two labs' saline, pipettes and filtering also differ (3 vs 10 kHz). Neither paper discusses the other's number.
- Gruntman & Turner's evoked compound responses (Turner lab, 2013) decay in between, at τ ≈ 35-60 ms (§1.4).

### C. What Gruntman & Turner's plateau requires

- Per claw, 1 CC KCs reach V_ss ≈ 4.4 mV at r ≈ 115 Hz (§1.2-1.3). The first EPSP is E1 ≈ 1.48 mV (mean) or 1.24 mV
  (median) (§1.5).
- In the LIF, V_ss = E1·(area/peak)·r·x_ss, so x_ss = 4.4/(E1 × 0.115 × area/peak[ms]) (derived):

| Kernel | Area/peak (ms) | x_ss needed (E1 1.48 mV) | x_ss needed (E1 1.24 mV) |
|---|---|---|---|
| Turner's own kernel (11.5 ms decay, 2.1 ms rise) | ≈ 12.5 | 2.07 | 2.47 |
| brainfly now (τ_m 11.5, τ_s 5) | 21.8 | 1.19 | 1.42 |
| τ_m 20 | 31.7 | 0.82 | 0.97 |
| τ_m 30 | 42.9 | 0.60 | 0.72 |
| τ_m 50 | 64.6 | 0.40 | 0.48 |
| τ_m 100 | 117 | 0.22 | 0.26 |
| τ_m 189 | 209 | 0.12 | 0.15 |
| Single-exponential 263 ms | 263 | 0.10 | 0.12 |

- An 11.5 ms kernel needs x_ss ≥ 1. The plateau is already as large as an undepressed fast EPSP can give, and twice what
  Turner's own kernel gives, so any depression undershoots it.
- Long kernels (≥ 100 ms) need strong depression (x_ss ≤ 0.25 at 115 Hz).

### D. Is the plateau's timing explained by the PN rate alone?

- Closed-form mean response to r(t) = 112 + 223·e^(−t/22 ms) Hz (§1.2), through the τ_s = 5 ms current and τ_m (derived):
  - V(t) = w·τ_s·b·[1 − (τ_m e^(−t/τ_m) − τ_s e^(−t/τ_s))/(τ_m − τ_s)]
    + w·c·τ_s·τ_r/(τ_r − τ_s)·[τ_r (e^(−t/τ_r) − e^(−t/τ_m))/(τ_r − τ_m) − τ_s (e^(−t/τ_s) − e^(−t/τ_m))/(τ_s − τ_m)]
  - Here b = 112 Hz, c = 223 Hz, τ_r = 22 ms.
- Times are from the KC response onset, about 7 ms after light onset. The fly ratios come from the 1 CC trace in §1.3.

| Model | V(11)/V(53) | V(23)/V(53) | V(93)/V(53) | Highest V / V(243) |
|---|---|---|---|---|
| Flies, 1 CC | 0.56 | 0.89 | 0.91 | Fig. 4b: peak at 250 ms ≈ peak at 50-100 ms |
| τ_m 11.5, no depression (brainfly now) | 0.76 | 1.21 | 0.77 | 1.72: early peak, then a 42% sag |
| τ_m 20, none | 0.51 | 0.94 | 0.81 | 1.47 |
| τ_m 30, none | 0.39 | 0.79 | 0.89 | 1.28 |
| τ_m 50, none | 0.31 | 0.66 | 1.03 | 1.07 |
| τ_m 50, effective drive ≈ 43 + 290·e^(−t/8 ms) Hz (≈ f 0.85, τ_rec 0.1 s) | 0.56 | 0.93 | 0.95 | ≈ 1.1 |
| τ_m 189, none | 0.22 | 0.53 | 1.34 | still rising: V(243) = 2.75 × V(33) |
| τ_m 189, effective drive ≈ 12 + 320·e^(−t/6 ms) Hz (≈ f 0.5, τ_rec 0.15 s) | 0.58 | 0.91 | 1.02 | ≈ 1.0 |

- The depressed rows replace r(t)·x(t) with a hand-fitted exponential. I matched x at onset (1), its steady state at
  115 Hz (table E) and a fast fall within the first few spikes. They are approximate, not computed spike by spike.
- With Turner's instant-rise 11.5 ms kernel and no depression, V peaks at about 20 ms and sags to 57% of that peak by
  100 ms (derived).
- So the flat plateau by about 30 ms follows from the PN rate's own fall plus an integration time of about 20-30 ms (no
  depression), or about 50 ms with mild depression.
- An 11.5 ms membrane gives an early peak and a sag that the flies don't show. A 189 ms membrane without depression keeps
  climbing.
- 5 CC KCs do sag (−22% by 100 ms). Shunting, depression or slow inhibition could each explain it.

### E. Steady state of a depleting synapse

- Model: x ← f·x at each spike, recovery τ_rec, regular interval d = 1/r. Then x_ss = (1 − e^(−d/τ_rec))/(1 − f·e^(−d/τ_rec)).
- The effective rate r·x_ss saturates at 1/((1 − f)·τ_rec) (derived).

| f | τ_rec (s) | 10 Hz | 20 Hz | 30 Hz | 50 Hz | 115 Hz | 335 Hz | r·x_ss limit | Label |
|---|---|---|---|---|---|---|---|---|---|
| 0.50 | 1.5 | 0.121 | 0.063 | 0.043 | 0.026 | 0.011 | 0.004 | 1.3 Hz | rung 4 KC → MBON (Yamada-based) |
| 0.85 | 0.8 | 0.470 | 0.301 | 0.221 | 0.144 | 0.068 | 0.024 | 8.3 Hz | rung 4 PN depression (odor_probe5 "depressed") |
| 0.50 | 0.15 | 0.655 | 0.442 | 0.332 | 0.222 | 0.107 | 0.039 | 13 Hz | strong, fast |
| 0.60 | 0.08 | 0.862 | 0.685 | 0.564 | 0.415 | 0.223 | 0.087 | 31 Hz | strong, faster |
| 0.80 | 0.1 | 0.896 | 0.764 | 0.664 | 0.525 | 0.312 | 0.132 | 50 Hz | moderate |
| 0.85 | 0.1 | 0.920 | 0.812 | 0.725 | 0.596 | 0.377 | 0.168 | 67 Hz | mild-moderate |
| 0.90 | 0.1 | 0.945 | 0.866 | 0.798 | 0.689 | 0.476 | 0.233 | 100 Hz | mild |
| 0.95 | 0.1 | 0.972 | 0.928 | 0.888 | 0.816 | 0.645 | 0.377 | 200 Hz | very mild |

- **Rung 4's PN depression on the current model**: 6.11 × 0.005 × 115 × 0.068 = 0.24 mV per connection at 115 Hz, against
  Gruntman & Turner's 4.4 mV, 18 times too weak (derived).
- During a 250 ms train at 115 Hz, x would fall to about 0.23 after 10 spikes and about 0.10 after 20 spikes (λ = f·E =
  0.84 per spike; derived). That gives a > 70% sag through the light, where flies stay flat to 250 ms.
- Rung 4's KC → MBON depression (0.5, 1.5 s) leaves 1% at 115 Hz.
- Neither belongs at PN → KC.

### F. Candidate parameter sets

Each set has w chosen for a PSP peak of 1.2-1.5 mV and the measured plateau. All entries derived. "Brief-input decay" is
the decay after 1-2 ms of light (flies: 35-60 ms).

| Set | τ_m | Depression (f, τ_rec) | PSP peak | V_ss/connection at 115 Hz (flies 4.4) | Shape (flies 0.56 / 0.89 / 0.91) | Brief-input decay | Left after 50 / 100 ms (Groschner αβc) | Turner 11.5 ms | V_ss/connection at 40 Hz (now 1.22) |
|---|---|---|---|---|---|---|---|---|---|
| Now | 11.5 ms | none | 1.4 mV | 3.5 mV | 0.76 / 1.21 / 0.77 ✗ | 11.5 ms ✗ | 1% / 0% ✗ | ✓ | 1.22 mV |
| A | 20 ms | none | 1.24 | 4.5 | 0.51 / 0.94 / 0.81 ~ | 20 ms (short) | 8% / 0.7% ✗ | ✗ | 1.57 |
| B | 30 ms | 0.95, 0.1 s | 1.3 | 4.2 | not computed; between the τ_m 30 row (0.39 / 0.79 / 0.89) and set C ~ | 30 ms ~ | 19% / 4% ✗ | ✗ | 1.90 |
| C | 50 ms | 0.85, 0.1 s | 1.4 | 3.9 | 0.56 / 0.93 / 0.95 ✓ | 50 ms ✓ | 37% / 14% partial | ✗ | 2.37 |
| D | 189 ms | 0.5, 0.15 s | 1.25 | 3.2 | 0.58 / 0.91 / 1.02 ✓ | 189 ms ✗ (✓ for Groschner) | 77% / 59% ✓ | ✗ | 2.77 |

- At 10 Hz, set C keeps x_ss = 0.92 and set D 0.66 (table E). Groschner's 10 Hz steps show no clear decline in one trial,
  which mildly favours C.
- Under set D the mean depolarization at 10 Hz is ≈ 1.7 mV (x_ss = 0.66), against 2.6 mV undepressed with the same kernel
  (3.3 mV for 1.25 mV EPSPs decaying with a 263 ms single exponential). Groschner's 10 Hz figure is a peak, 5.6 mV over
  30 pulses, which the undepressed case approaches more closely (derived).

### G. Recommendation

1. **KC membrane time constant: 20-50 ms (central value 30-50 ms) for all classes**, not 11.5 ms.
   - Reasons:
     - 11.5 ms needs facilitation to give Gruntman & Turner's plateau and predicts an overshoot and sag that they did not
       see (C, D).
     - It cannot sum inputs over 50-100 ms (B).
     - Every somatic τ_m measured is 118-200+ ms. Gruntman & Turner's own evoked responses decay with τ ≈ 35-60 ms.
     - Turner's 11.5 ms remains the one measurement supporting it.
   - If the classes are separated, αβc could go longer (≈ 190 ms) only together with set D's strong, fast depression.
     No fly measurement shows that depression, and it contradicts Gruntman & Turner's decays.
2. **PN → KC depression: none, or mild with fast recovery (f 0.85-1.0, τ_rec 0.05-0.2 s).**
   - Use none with τ_m ≈ 20 ms; f ≈ 0.95 with 30 ms; f ≈ 0.85, τ_rec ≈ 0.1 s with 50 ms.
   - Reasons:
     - No fly measurement of PN → KC STP exists. Locust shows none at 0-150 ms (§4).
     - Gruntman & Turner's plateau stays flat for 250 ms at about 115 Hz, which rules out slow-recovery depression
       (E).
     - Groschner's 10 Hz EPSCs show no consistent decline.
   - Never import rung 4's PN or KC → MBON values.
3. **Scale w, not τ_m alone.**
   - Keep a single PSP peak at 1.2-1.5 mV: Turner 1.4 (median 1.2), Gruntman & Turner ≈ 1.5 (median 1.2), Groschner αβc
     ≈ 1.25.
   - Also keep the steady depolarization per connection at about 115 Hz near 4-4.5 mV.
   - Check the plateau shape against §1.3: V(23)/V(53) ≈ 0.9 and V(93)/V(53) ≈ 0.9 under the measured PN rate.
4. **Optional: sublinear summation.** 3-5 coactive claws sum sublinearly (5 CC: ≈ 8.4 mV where linear predicts ≈ 22 mV).
   Inada's two- and three-glomerulus slopes are 0.75-0.89. A conductance-based PN → KC synapse (E_syn ≈ 0 mV, so about
   18% less drive 10 mV above a −55 mV rest) gives only part of this. Gruntman & Turner attribute the rest to dendritic
   shunting.

### H. What this does not fix: spikes per response

- Every Gruntman & Turner-consistent set raises the sustained per-connection drive at moderate PN rates.
  - At 40 Hz: 1.6-2.8 mV against 1.2 mV now (F).
  - Reason: the current model is 20% under Gruntman & Turner's plateau at 115 Hz, and depression compresses the rate
    dependence.
- So neither PN → KC depression nor KC τ_m is the lever for the excess spikes: about 11 spikes over 1.4 s at about 8 Hz,
  against flies' αβ 2.2 ± 1.2.
- What the fly data point to instead:
  - The αβc KC depolarization peaks at 0.15-0.3 s and is at a median of about 40% of its peak by 0.95 s (Murthy).
  - APL inhibition arrives several hundred ms after excitation and can override it (Inada).
  - PNs adapt after odor onset (their rates are not measured here).
- The comparison worth making: the model KC's odor-evoked Vm time course against Murthy Fig. 2D, before touching the
  synapse.
- Gruntman & Turner's light experiments show that KCs with ≥ 4 strongly driven claws can fire through 250 ms of input
  (§1.6). Intrinsic adaptation is not what ends fly KC responses (`adaptation.md`: no KC SFA).

### I. Unresolved

1. **EPSP decay: 11.5 ms (Turner) against 263 ms (Groschner αβc).** Turner's fit was of isolated, by-eye spontaneous
   EPSPs from unidentified classes in females at −58 mV. Groschner's are averaged spontaneous EPSPs in αβc males at −70 mV.
   - Shal (A-type K⁺) shortens αβc EPSPs: FoxP mutants are 140-165 ms. But Shal half-inactivates at −72.9 mV, so it should
     act less at −58 mV, not more. Voltage does not explain the gap.
   - Background synaptic conductance in Turner's antenna-intact prep (≈ 33 EPSPs/s × ≈ 40 pS × 2.8 ms ≈ 4 pS) is
     negligible against an ≈ 87 pS leak (1/11.5 GΩ) (derived).
2. **Gruntman & Turner's decays (35-60 ms; one KC 150-200 ms) sit between the two.** Mz19 light drives many PNs at once
   and may recruit inhibition that shortens decays. ChR2 in the boutons, lit directly, may also change release. Neither
   was tested.
3. **No fly PN → KC STP data.** Every depression parameter above is inferred from the plateau through an assumed kernel.
4. **The plateau's cause was never tested** with picrotoxin, CGP, APL silencing or paired pulses in vivo. Inada's ex vivo
   inhibition is slower (hundreds of ms) than the 30 ms plateau, but could explain the late declines: 5 CC (−22% by
   100 ms) and the Fig. 3d KC (−25% by 240 ms).
5. **Gruntman & Turner's first-EPSP amplitudes are biased.** Only trials with identifiable EPSPs were measured. With
   failures, the mean per-spike EPSP would be smaller, which lowers the x_ss each kernel needs (C).
6. **Per-class data are thin.** τ_m and EPSP decay are measured only for αβc (Groschner) and α′β′ (τ_m only). Gruntman &
   Turner's and Turner's KCs are unclassified.

---

## Sources

- Gruntman E, Turner GC (2013) Integration of the olfactory code across dendritic claws of single mushroom body neurons.
  Nat Neurosci 16:1821-1829. [PMC3908930](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/) (full text and figures);
  [nature.com/articles/nn.3547](https://www.nature.com/articles/nn.3547) (published figures, supplementary figures 1-6
  and legends).
- Turner GC, Bazhenov M, Laurent G (2008) Olfactory representations by Drosophila mushroom body neurons. J Neurophysiol
  99:734-746. [doi:10.1152/jn.01283.2007](https://doi.org/10.1152/jn.01283.2007);
  [PDF](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf) (read in full, figures rendered).
- Groschner LN, Chan Wah Hak L, Bogacz R, DasGupta S, Miesenböck G (2018) Dendritic integration of sensory evidence in
  perceptual decision-making. Cell 173:894-905. [PMC5947940](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/)
  (full text); figures 2, 5, S3 and S6 at publisher resolution
  ([doi:10.1016/j.cell.2018.03.075](https://doi.org/10.1016/j.cell.2018.03.075)).
- Murthy M, Fiete I, Laurent G (2008) Testing odor response stereotypy in the Drosophila mushroom body. Neuron
  59:1009-1023. [PMC2654402](https://pmc.ncbi.nlm.nih.gov/articles/PMC2654402/).
- Inada K, Tsuchimoto Y, Kazama H (2017) Origins of cell-type-specific olfactory processing in the Drosophila mushroom
  body circuit. Neuron 95:357-367. [PDF](https://kazamalab.riken.jp/pdf/Neuron_Inada_2017.pdf).
- Jortner RA, Farivar SS, Laurent G (2007) A simple connectivity scheme for sparse coding in an olfactory system.
  J Neurosci 27:1659-1669. [PMC6673743](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673743/) [other insect].
- Sato S, Ueno K, Saitoe M, Sakai T (2018) Synaptic depression induced by postsynaptic cAMP production in the Drosophila
  mushroom body calyx. J Physiol 596:2447-2461. [PMC6002214](https://pmc.ncbi.nlm.nih.gov/articles/PMC6002214/)
  (abstract and protocol; full text not downloadable as XML).
- Szyszka P, Ditzen M, Galkin A, Galizia CG, Menzel R (2005) Sparsening and temporal sharpening of olfactory
  representations in the honeybee mushroom bodies. J Neurophysiol 94:3303-3313.
  [doi:10.1152/jn.00397.2005](https://doi.org/10.1152/jn.00397.2005) (abstract only) [other insect].
- Repo files: `experiments/odor_probe5.py` (KC τ_m, PSP kernel), `experiments/odor_kc_timing.py` and `.json` (model KC
  spike timing), `experiments/odor_probe34.py`, and `../Rung 4 resting state data/short_term_plasticity.md` and
  `adaptation.md`.
