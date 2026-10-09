# ORN firing dynamics, measured: latency, rise, adaptation, off-response, spontaneous rates, PN timing

Compiled 2026-10-09 from full texts (PMC, publisher PDFs or released code), for replacing brainfly's instant, constant
Poisson step (DoOR response × max_hz from odor onset to offset, silent ORNs at rest).
Conventions: text in quotation marks is verbatim; "(fig.)" = read off a published figure by eye (expect ±10-20% of a
tick interval); "derived" = my arithmetic; "via DoOR" = the value as entered in the DoOR.data per-receptor files
(row "SFR"), not checked against the original paper. Recording temperature is room temperature (not stated) unless
given. Not repeated here (see [sensory_periphery.md §2](../Embodied%20fly%20connectome%20simulation/sensory_periphery.md)):
DoOR 2.0, Olsen 2010's PN transform, Kazama & Wilson 2008's unitary EPSP, Alvarez-Salvado 2018's behavioural ORN model.

## Summary: numbers a simulation would use

1. **Odor arrival (the stimulus itself).** Valve-to-antenna delay 50-100 ms in standard rigs. Concentration at the
   antenna rises with τ_on ≈ 25-40 ms for volatile esters and ketones (10-90% ≈ 55-90 ms, derived) but 0.1-1.5 s for
   low-volatility odors (every odor with τ_on > 100 ms had vapor pressure < 1 mmHg). Decay τ_off ranges 30 ms-1 s
   (Martelli 2013, 27 odors).
2. **Latency from arrival.** First spike 3-4.4 ms at high and 18-55 ms at low concentration, with trial-to-trial jitter
   0.2-0.5 ms vs 4-106 ms (Egea-Weiss 2018, 3.6 ms-rise stimulus). Other measures: 12 ms filter delay (Martelli
   2013), < 10 ms transduction latency (Nagel & Wilson 2011).
3. **Rise.** The fastest firing responses peak < 30 ms after onset; LFP 10-90% rise is 28-32 ms and the spike rate
   peaks before the LFP (Nagel & Wilson 2011). With ordinary 500 ms puffs, the mean ORN response starts about 75 ms
   after the valve opens and reaches 90% of peak at about 195 ms (fig.; ≈ 110 ms 10-90%, derived; Bhandawat 2007).
4. **Peak.** 100-300 spikes/s for strong stimuli, saturating at about 225-300 spikes/s. ORNs "are capable of spiking up
   to ~300 Hz" but stay within 0-50 Hz during fluctuating plumes (Gorur-Shandilya 2017).
5. **Plateau/peak.** About 0.5 at 500 ms for fast odors mid-range (Martelli 2013). 0.43-0.44 for steps (Lazar & Yeh
   2020 on Kim et al. data). About 0.7 for a strong pb1A response (Nagel 2011, fig.); 0.3-0.85 across Nagel's
   examples (fig.). About 0.75 at 500 ms averaged over 69 odor-glomerulus pairs (Bhandawat, fig.). In a 25 s step:
   25% of peak after 1 s, 15% after 25 s (de Bruyne 1999).
6. **Adaptation time constants.** Decay from peak τ ≈ 0.4 s (range about 0.15-1 s; Nagel Fig. 5c, fig.). Elsewhere:
   "~100 ms" (Martelli & Fiala 2019), τ ≈ 250 ms in the standard model (Kadakia & Emonet 2019). Recovery from adaptation
   τ = 1.27 s (Cao 2016). Ir ORNs don't adapt within 2 s pulses (Getahun 2012).
7. **Off-response.** Firing stops abruptly at offset, with a brief dose-dependent silence for many odor-receptor pairs.
   In Nagel's Fig. 1 it drops from about 40 Hz to about 0, recovering over about 0.5 s (fig.). The fastest responses
   "terminate in <200 ms". Others are prolonged by slow odor clearance (τ_off up to about 1 s) or are
   "supersustained" (19 of 525 pyrazine-receptor pairs; Montague 2011).
8. **Spread across ORN types for one odor.** Latency falls steeply with drive (3 ms vs 18-55 ms), so strongly driven
   types lead weakly driven ones by tens of ms. At high concentration, Or59b and Or22a differ by about 1 ms. Other
   measured spreads:
   - odor-specific physiological delays up to 12-18 ms within one ORN type (Martelli);
   - stimulus-to-firing lags of 50-95 ms across 4 odor-ORN pairs (Gorur-Shandilya Fig. 7, fig.);
   - isoamyl acetate transduction several-fold slower in pb1A than in pb3B (Nagel Fig. 4, fig.).
9. **Spontaneous rates.** Wild-type antennal basiconic ORNs 1-15 spikes/s (median 6, 16 types; via DoOR). Palp
   ORNs mostly 3-13 (pb2B 32 ± 7). Coeloconic ORNs 16-42 (median 19; via DoOR). DM4 ORNs 3.44 ± 0.16; pb1A
   12.8 ± 2.6. ORN spike trains are mutually independent. At rest, PNs fire 1-5 spikes/s, driven by these spontaneous
   ORN spikes (Kazama & Wilson 2009).
10. **PNs.** PNs start firing with ORNs (about 75 ms after the valve; Bhandawat 2007, fig.), but rise and decay faster:

    | | 90% of peak | peak | half-decay | at 500 ms |
    |---|---|---|---|---|
    | PN | about 140 ms | about 150 ms | about 185 ms | about 0.5 of peak |
    | ORN | about 195 ms | about 225 ms | about 325 ms | about 0.75 of peak |

    An ORN spike starts a PN EPSP 4.5 ms later, and PNs integrate over about 20-30 ms (Jeanne & Wilson 2015). PNs
    from different glomeruli are nearly uncorrelated: 0.9 ± 0.7% of spikes fall within 1.6 ms of each other
    (Kazama & Wilson 2009). Turner 2008 found no periodicity in KC membrane potential.
11. **Ready-made models.**
    - Kadakia & Emonet 2019: Or-Orco activity with Weber adaptation (τ ≈ 250 ms), then a bi-lobed Gamma filter
      and a rectifier. The released code's defaults are K = (1/0.63)[Γ(2, 6 ms) − 0.5 Γ(3, 8 ms)] × 300 Hz.
    - Gorur-Shandilya 2017: α = 12.5 s⁻¹, β = 1.26 s⁻¹, ε_L = 0.86, K_on = 0.1 V, K_off = 400 V (PID units).
    - Lazar & Yeh 2020: binding rate 2.17×10⁻² (ppm·s)⁻¹, dissociation 2.94 s⁻¹, plus 11 fitted parameters.
    - Nagel, Hong & Wilson 2015: ORN-to-PN depressing synapse with a fast and a slow component.

## 1. ORN firing-rate time course to odor steps and pulses (Q1)

### 1.1 Two stages: transduction smooths, spike generation differentiates
[Nagel & Wilson 2011, Nat Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC3030680/). Single-sensillum recordings
from palp sensilla pb1-pb3 (females, 2-7 d), with LFP and spikes from one ORN (partner ablated or mutant).
Delivery: "A continuous stream of air (100 mL/min) passed over the vial and was diluted in a second air stream
(100 mL/min)"; a solenoid switched it "into a delivery air stream (1 L/min) directed at the fly". Pulses lasted 1.7 s,
and the delivered pulse "is not square because it is slightly smoothed by our odor delivery device".
- Odor-to-LFP filter: "The width of this lobe (105 ms half-width) indicates that the LFP faithfully tracks odor
  fluctuations up to ~6Hz (20 dB attenuation). The interval between the lobe and zero indicates the absolute latency
  of the response, which is less than 10 ms."
- "The filter relating the LFP to the spike rate was biphasic… The slightly larger negative lobe indicates that the
  spike rate remains above baseline as long as a steady negative LFP deflection persists." The filter as computed is
  widened by the LFP's slow time course ("its width is over-estimated").
- Fig. 3e (fig.): positive lobe about +7 spikes/s per mV just before zero lag, negative lobe about −12 at +20-40 ms,
  both within ±100 ms.
- Onset and offset: "transduction onset was always faster than offset". "For both odors, we found that the onset rate
  grew with increasing concentration, whereas the offset rate was much less sensitive to concentration". Adaptation
  "reduced the onset rate of the test pulse".
- Plume hits (2-butanone 0.1×, pb1A): "The range of rise times (time from 10% to 90% of peak) was 28-32 ms." "The
  spike response consistently peaked before the LFP response". "the fastest responses could peak in <30 ms and
  terminate in <200 ms (Fig. 8e)".
- Fig. 8f-g (fig.): spike-rate events about 50 ms wide at half height. Peak rate rises from about 80 spikes/s for a
  2 mV LFP event to about 250 spikes/s for a 26 mV event.
- Gain at the spiking stage "was largely invariant to the ten-fold change in the mean stimulus… with a 1 mV change in LFP
  leading to a ~ 10 Hz change in the firing rate" ([Gorur-Shandilya 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5524537/),
  ab3A).
- Gorur-Shandilya 2017 adds that the stage kinetics are coupled: "While the transduction response time slowed down with
  increasing stimulus intensity, the spiking machinery sped up to compensate. These complementary kinetic changes
  caused the firing rate response time to remain invariant with stimulus intensity."

### 1.2 Latency (odor arrival to first spike)
- [Egea-Weiss et al. 2018, iScience](https://pmc.ncbi.nlm.nih.gov/articles/PMC6147046/): paired recordings of
  ab2A (Or59b) and ab3A (Or22a) neurons, methyl butyrate and ethyl acetate at 10⁻⁶-10⁻², stimulus "rise time (5% to 95%
  within 3.6 ms)". Results:
  - "first spike latencies ranging from 18 to 55 ms for low concentrations and 3 to 4.4 ms for high concentrations
    (median latencies for 10 repeated stimulations)".
  - "an average SD (trial-to-trial jitter) of 4.36–106 ms for low odorant concentrations and 0.19–0.49 ms for high
    concentrations". "The neuron-to-neuron jitter was similar to the trial-to-trial jitter".
  - The 3 ms minimum "is shorter than previously reported for insect olfactory receptor neurons (10–30 ms)", which they
    attribute to stimulus rise time being "one to two orders of magnitude shorter than… commonly used olfactory
    stimulators".
- [Martelli, Carlson & Emonet 2013, J Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC3678969/), ab3A, flickering
  methyl butyrate: "Comparing the time to peak of this filter with the time to peak of the filter obtained for the
  signal (Fig. 7b) we estimated a 12ms delay between the stimulus arrival and the ORN response."
- [de Bruyne, Clyne & Carlson 1999, J Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC6782632/), palp, 20 °C:
  "Excitatory responses started ∼80 msec after odor was administered; calculations reveal that 50 msec is required for
  odor to reach the preparation, indicating a response latency of ≤30 msec."
- [Cao et al. 2016, PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC4763727/), antennal slice with perforated patch;
  odors in solution, and 33 ms of delivery delay subtracted.
  - Or-OSNs: "a latency (tlatency) of 66 ± 25 ms (n = 25) (i.e., time from odor arrival to 10% of response peak
    amplitude…) and a time-to-peak (tpeak) of 138 ± 42 ms".
  - Ir-OSNs (ac3A-like, butyric acid): "the average tlatency, trise, tpeak, and tint were 35 ± 16, 52 ± 14, 104 ± 25, and
    225 ± 106 ms".
- [Szyszka et al. 2014, PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC4250155/) used EAG in cockroaches, locust,
  honeybee and moth at 28 °C, not Drosophila. "Odor-evoked mean EAG responses began between 1.6 and 26.4 ms after odors
  arrived at the antenna". Latency "depended on odor identity and decreased with increases in concentration". This is
  an upper bound on transduction speed.
- [Getahun et al. 2012, Front Cell Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC3499765/): "a 20 ms stimulation
  was sufficient to elicit a response" in Or59b ORNs (methyl acetate 10⁻⁵).
- [Kim, Lazar & Slutskiy 2015, eLife](https://pmc.ncbi.nlm.nih.gov/articles/PMC4466247/), Or59b ORNs and DM4 PNs:
  "all responses initiated within a few tens of milliseconds of the odor onset".

### 1.3 Rise to peak, and peak rate
- [Bhandawat et al. 2007, Nat Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/): 500 ms pulses, "standard
  concentration (1:1,000 dilution)", 69 odor-glomerulus pairs. "ORN responses typically do not peak until 100–300 ms
  after odor onset" (citing de Bruyne 1999). Fig. 2 (fig.):
  - mean peak-normalized ORN PSTH starts rising at about 75 ms after valve opening, reaches 90% of peak at
    195 ± about 15 ms (s.e.m.), and peaks at about 225 ms;
  - examples peak at about 55 spikes/s (at about 250 ms) and about 270 spikes/s (at about 150 ms).
- Martelli 2013 Fig. 3 (fig.), ab3A with 500 ms ethyl acetate puffs: rate rises to peak within about 50 ms of response
  onset. Peak goes from about 15 spikes/s at 10⁻⁵ to about 240 spikes/s at 10⁻¹ (sigmoid in log dilution). Spontaneous
  rate is about 5-10 spikes/s.
- Cao 2016: receptor current 10-90% rise "62 ± 23 ms (n = 25)" (Or), 52 ± 14 ms (Ir).
- Peak rates elsewhere:
  - de Bruyne 1999: pb1A ethyl propionate dose-response "reaching saturation at ∼225 spikes/sec".
  - Nagel 2011 Fig. 5a (fig.): pb1A, 2-butanone 0.1×, peak about 270-300 spikes/s.
  - Lazar & Yeh 2020 ([PMC7182276](https://pmc.ncbi.nlm.nih.gov/articles/PMC7182276/)), from the raw data of Kim
    et al.: "(methyl butyrate, Or59b)… steady-state spike rate at 87 spikes per second and the peak spike rate at 197
    spikes per second in response to a constant stimulus with amplitude 20 ppm". For (butyraldehyde, Or7a): "43 spikes
    per second and the peak spike rate at 101 spikes per second… 173 ppm".
  - Gorur-Shandilya 2017: "ORNs are capable of spiking up to ~300 Hz; however… ORNs maintained firing rates between 0–50
    Hz to fluctuating odor stimuli, even with a ten-fold increase in the mean stimulus."

### 1.4 Adaptation: plateau/peak ratio and time constants
- Martelli 2013 (ab3A, ab2A, ab3B, ab7A; Canton-S females):
  - Degree of adaptation is "the peak response minus the adapted response (measured 500ms after stimulus onset) divided
    by the peak response". For fast odors, ORNs "show a phasic response with a degree of adaptation around 0.5". Fig. 3b
    (fig.): about 0.5-0.65 across the mid-range of ethyl acetate.
  - "the degree of adaptation is nearly constant for all the dilutions in the middle of the dynamic range where the peak
    response is nearly linear with log-changes in concentration (between 10% and 90% of the maximum firing rate)"; "not
    only the degree of adaptation but the entire response dynamics are independent of odor dilution."
  - Three regimes: "Stimuli at the lower end of the dynamic range usually elicit a tonic response… Response becomes more
    phasic and concentration invariant for stimuli in the middle of the dynamic range. Stimuli near the upper end…
    elicit saturated responses characterized by prolonged dynamics."
  - "ORN responses to slow odorants tend to be more tonic (lower degree of adaptation)". Background: ab3A adapts "within
    few seconds to a stationary firing rate that is concentration-dependent". Under flicker, "the linear filter k(r)
    remains invariant, the nonlinear function N becomes less steep".
- Nagel 2011 Fig. 5 (fig.; pb1A, 2-butanone 0.1×, n = 20-22 sensilla per genotype):
  - controls: peak about 270-300 spikes/s, decay τ from peak about 0.4 s (spread about 0.15-1 s), peak-to-steady-state
    ratio about 1.4 (plateau/peak about 0.7, derived), spontaneous rate about 16 spikes/s;
  - DmNav knock-down: τ about 0.18 s, ratio about 2; the text's "1.7-2.3" refers to these knock-down ORNs.
  - Steady state is defined as "the mean firing rate over a 400-ms period beginning 800 ms after nominal stimulus onset".
- Nagel 2011 Fig. 1 (fig.; 1.7 s pulses):

  | stimulus | ORN | baseline | peak | plateau | offset |
  |---|---|---|---|---|---|
  | 2-butanone 0.001× | pb1A | about 10 Hz | about 90 Hz | about 40 Hz | drops to about 0 |
  | isoamyl acetate 0.1× | pb1A | | about 70 Hz | about 60 Hz | slow decay, no undershoot |
  | isoamyl acetate 0.1× | pb3B | | about 90 Hz | about 25-30 Hz | undershoot |
  | fenchone 0.25× | pb2A | | about 170 Hz | about 50 Hz | |
- de Bruyne 1999, 25 s ethyl propionate step on pb1A: "The spike frequency quickly rises to a peak of 200 spikes/sec and
  then rapidly declines to 25% of its peak value, over a period of 1 sec; it then slowly declines over the ensuing 24
  sec to 15% of its peak value." Cross-adaptation: an unadapted ethyl acetate response of 250 spikes/s fell to 125
  spikes/s 1 s after that step.
- [Kim, Lazar & Slutskiy 2011, J Comput Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC3736744/), Or59b with an
  acetone staircase: "when the odor concentration is increased by 40 ppm at time t = 10 s, the spike rate of the neuron
  jumps from 40 Hz to 70 Hz". At steady state between steps it "goes up from 40 Hz to 50 Hz". Derived: the transient
  increment (30 Hz) is 3× the sustained increment (10 Hz).
- Gorur-Shandilya 2017:
  - gain control: "the gain changed within ~130 ms following the change in stimulus variance"; deviations fall with the
    mean stimulus over the preceding 300 ms;
  - gain scales as 1/mean (Weber-Fechner) at transduction.
  - [Kadakia & Emonet 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6609331/) summarize the fast adaptation as
    "τ ≃ 250 ms".
- [Martelli & Fiala 2019, eLife](https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/) (20 °C):
  - "In Drosophila, ORN firing rates adapt to sustained odor stimuli on timescales on the order of ~100 ms."
  - ORN axon-terminal calcium does not adapt over 2 min: "mean degree of adaptation across glomeruli: -0.06 ± 0.1 for
    ORNs and 0.57 ± 0.1 for PNs".
- Cao 2016: paired-pulse recovery of the receptor current "is fit with an exponential function with a time constant of
  1.27 s"; at 500 ms intervals the second response is smaller.
- Getahun 2012: "IR-expressing OSNs did not exhibit adaptation to longer stimulations, unlike OR- and Gr21a-OSNs".
  Or59b's maximum fell for stimulations ≥ 1 s at 10⁻³ but not at 10⁻⁶.

### 1.5 Off-response
- de Bruyne 1999: "Excitatory responses terminated abruptly after the end of the odor stimulation period in most
  cases… we often observed a brief period in which no action potentials were recorded from this neuron. The duration of
  this poststimulus quiescence appeared to be dose-dependent… Poststimulus quiescence was not, however, observed for
  all odors. In fact, in some cases excitation continues long past the end of od[or stimulation]".
- Martelli 2013: "A post-stimulus silent period can be observed with intermediate concentrations." Saturating stimuli
  give "prolonged" responses, and slow odors give "prolonged dynamics that reflects the long decay of the odor following
  the closing of the valve".
- Nagel 2011:
  - The biphasic spike filter "predicts which responses show onset transients and offset inhibition". It also "predicts
    elevated spiking after offset of an inhibitory odor".
  - Some odor-receptor pairs give a transient, then offset inhibition, then renewed spiking (Fig. 1d).
  - Fig. 1a (fig.): the undershoot to about 0 recovers to baseline over about 0.5-1 s.
- Bhandawat 2007 Fig. 2e (fig.): ORN peak-to-half-decay about 325 ms (PN about 185 ms), for 500 ms pulses.
- [Montague, Mathew & Carlson 2011, J Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC3116233/):
  - "Typical excitatory responses returned to spontaneous firing levels within several seconds after the end of the
    odor stimulus period".
  - Supersustained (> 2 SD above baseline 9 s after a 0.5 s pulse): "9 of the Or33b responses and 10 of the Or59a
    responses… of the 525 pyrazine–receptor combinations". They also occur in wild-type ab3A (methyl hexanoate).

## 2. How synchronous are the ORN onsets of different glomeruli for one odor? (Q2)
- **Latency depends on drive** (Egea-Weiss 2018):
  - First-spike latency runs from 18-55 ms (weak) to 3-4.4 ms (strong), and jitter shrinks from tens of ms to < 1 ms.
  - Order across types is odor-specific: "OR59b neurons responded faster… to ethyl acetate than OR22a neurons, whereas
    OR22a neurons responded slightly faster and with higher spike rates to methyl butyrate". Classification used "a
    single classification threshold for all concentrations (0.76 ms difference in first spike latencies…)", so the
    strongly driven pair differs by about 1 ms.
  - "the first wave of odorant-evoked spikes across the population of the first responding olfactory receptor neuron
    type encodes the onset of an odorant (spikes are almost in synchrony, due to low jitter…)".
- **Odor-specific delays within one ORN type, after removing stimulus dynamics** (Martelli 2013):
  - "the odor-to-ORN filters estimated for pairs of odors have different response delays with shifts of up to 12ms";
    for pb1A, 2-butanone vs isoamyl acetate, "a small delay (18ms)"; ab3A, 1-octen-3-ol vs methyl butyrate, "a small
    4ms delay".
  - "the shape of the response function only depends mildly on odorant identity but shows odor-dependent delays with
    differences up to 18ms". The delays held from the start to the end of 60 s flicker despite gain adaptation.
- **Same odor, different ORN type** (Nagel 2011 Fig. 4, fig.): the transduction filter for isoamyl acetate is broad in
  pb1A (extending about 1 s back) but narrow in pb3B (about 0.15 s). The pb1A LFP takes about 1 s to plateau vs about
  0.2 s in pb3B, and filters for 2-butanone/pb1A and fenchone/pb2A are narrow. Quote: "transduction can be approximately
  described as a low-pass filter with a stimulus- and receptor-dependent width and polarity".
- **Cross-correlation lags** (Gorur-Shandilya 2017 Fig. 7, fig.; Gaussian odor noise around a mean, lag measured from
  PID): ab3A-ethyl acetate firing lag about 50-60 ms (LFP 65-160 ms, rising with mean); ab3A-1-pentanol about 75-95 ms;
  ab2A-1-pentanol about 70-85 ms; ab2A-2-butanone about 45-60 ms. Firing lags did not change with mean concentration
  ("p>0.1, Spearman test"; per-panel p = 0.15-0.8). Spread across these 4 pairs is about 40 ms.
- **Receptor family:**
  - Getahun 2012 Fig. 3E (fig.): time to maximum on the 1st pulse of a 1 Hz train was about 120 ms for Or59b (methyl
    acetate), about 210 ms for Gr21a (CO2), about 225 ms for Ir84a (phenylacetaldehyde) and about 455 ms for Ir75abc
    (butyric acid). The delay is measured from valve, through "Teflon tubing 150 cm long", and "mechanical delay was
    not considered".
  - Cao 2016, in the slice, found the reverse: "The key difference between Or- and Ir-expressing OSNs is the shorter
    tlatency and tpeak of the latter". Across cells the SD of latency is 16-25 ms.
- **Population spread in an ordinary rig** (Bhandawat 2007): ORN time to 90% of peak is 195 ± about 15 ms (s.e.m.,
  fig.). If n ≥ 69 pairs, the across-pair SD is ≥ about 120 ms (derived, rough; it mixes latency, rise time and slow
  odors).
- **Honeybee PNs (comparative, two-photon calcium, 10 ms resolution)** ([Paoli et al. 2018, J
  Neurosci](https://pmc.ncbi.nlm.nih.gov/articles/PMC6705991/)):
  - "odor delivery kinetics was highly reproducible and odorant specific, showing onsets between 18 ± 2 ms (1-hexanol)
    and 41 ± 2 ms (acetophenone) after valve opening".
  - Glomerular onsets: "one uniformly distributed over the whole stimulus duration and the other one normally
    distributed, with short latencies ∼125 ms". Fig. 3A (fig.): early-component SD about 50 ms.
  - Absolute latencies "varying between 86 ms for acetophenone and 112 ms for 1-nonanol". Onset rank order is
    odor-specific and conserved across bees.
- **Odor components can arrive at different times.** In [Su et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3064350/),
  PID showed that linalool and methyl butyrate, "although… premixed in solution and carried via the same puff of air,
  their vapors may reach the fly's antenna at different rates".
- **Synthesis (derived).** At moderate concentration, strongly activated ORN types should start within about 5-15 ms
  of arrival and peak about 30-60 ms later. Weakly activated types start 20-60 ms later with jitter of tens of ms, and
  odor arrival itself (τ_on ≥ 25 ms) smears everything. So onsets are spread over more than one KC EPSP decay (11.5 ms),
  except among the most strongly driven glomeruli, which arrive within a few ms of each other. No Drosophila study has
  measured onset latencies across many glomeruli for the same odor at ms resolution (see gaps).

## 3. Odor concentration at the antenna, and what ORNs read from it (Q3)
- Martelli 2013 used Pasteur-pipette puffs: "an air stream (3ml/sec)" injected into "a clean air stream (30ml/sec)",
  with the PID "~1.5cm downstream from the exit of the delivery tube".
  - "The time-scales of the rise and decay phases of the PID traces are broadly distributed (Fig. 1b–c) between 30ms and
    1s. Rise and decay phases are correlated but not identical." "all odors with long rising time (>100ms) had low vapor
    pressure (<1mmHg)".
  - Fast odors keep their dynamics across dilutions, but slow ones shift "up to hundreds of milliseconds", attributed to
    "interactions between odor molecules and the surfaces of the delivery system".
  - Fig. 1 (fig.): τ_on is about 25-40 ms for ethyl acetate, methyl acetate, methyl butyrate, 2,3-butanedione and
    isobutyl acetate; about 0.15 s for 4-methylphenol; about 0.25 s for γ-hexalactone; about 0.55 s for diethyl
    succinate; and about 1.5 s for pentanoic acid. τ_off is about 0.03-1 s.
  - Valve-to-PID filter: "peaks at 56ms, consistent with the air travel time and exhibits a long tail (~200ms…)… The
    function N is a straight line revealing that the delivery system is linear."
- [Gorur-Shandilya et al. 2019, J Exp Biol](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918787/) (delivery physics):
  - Air replacement time is "τ2=50 ms" for their delivery tube. "for volatile odorants that do not interact strongly
    with the surfaces of the delivery system, correlation times as fast as 30 ms can be realized".
  - "Teflon tubing… odorants stuck to this material minimally (other common tubing materials such as soft Tygon plastic
    bound far more…)". "stimuli delivered in this way typically exhibit intrinsic odorant-dependent dynamics before any
    interaction with the animal takes place".
- Fast stimulators: 3.6 ms 5-95% rise (Egea-Weiss 2018). With TiCl₄ smoke, odor reached the antenna "3.3 ± 0.3 ms…
  after triggering the valve" (Szyszka 2014). The miniPID itself has "10–90% rise time of 0.6 ms"
  ([Kazama & Wilson 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/)).
- Valve-to-antenna delays in common rigs:
  - de Bruyne 1999: 50 ms (air 35 ml/s, 180 cm/s, outlet 8 mm away);
  - [Turner et al. 2008](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf): analysis
    windows began "100 ms after valve opening (because air flow rates introduce a delay in the arrival of the odor at
    the fly's antennae)". Constant flow was 37.5 ml/s, with 3.75 ml/s diverted through the odor vial for the 500 ms
    pulses, and no PID;
  - [Seki et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493115/): "0.05 s was an approximate delay for the
    odors to reach the antennae".
- Natural plumes (Nagel 2011): windspeed 0.11-0.39 m/s. "LFP signals were low-pass filtered with a cutoff frequency
  that depended on the odor-receptor combination". "spike generation tends to emphasize encounters with weak stimuli"
  and "increases the speed of encoding".
- Rate of change:
  - Kim 2011: "the response of an OSN depends not only on the concentration, but also on the rate of change of the odor
    concentration"; Or59b bandwidth "roughly 25 Hz".
  - Nagel 2011: "the spike rate is sensitive to the slope of the LFP"; "sensitivity to the rate of change arises mostly
    at the level of spiking, rather than transduction".
  - Kim 2015: PNs "primarily signal the acceleration and the rate of change". For triangle stimuli, OSN peaks "advanced
    by 400–1000 ms relative to the stimulus peak".
- Pulse following: Getahun 2012 found Or ORNs follow 50 ms pulses "up to 5 Hz" (with 150 cm tubing).

## 4. Spontaneous ORN firing rates (Q4)
Primary text:
- de Bruyne 1999 (palp, 20 °C): "most neurons exhibiting frequencies between 3 and 13 spikes/sec… some neurons had
  noticeably higher spontaneous rates of ∼30 spikes/sec". "the spontaneous firing frequency of pb2B is 32 ± 7
  spikes/sec". A single cell's rate "stayed within a range of ±3 spikes/sec" over up to 60 min.
- Nagel 2011: pb1A "12.8 ± 2.6 spikes/s s.d." (vs 36.4 ± 17.9 when misexpressing Or47b). Fig. 5b (fig.): controls
  about 16, range about 8-22.
- Kazama & Wilson 2009: "the mean firing rate of DM4 ORNs (3.44 ± 0.16 Hz, n = 11)" with "17.4 ± 0.9 per antenna".
  This predicts the DM4 PN spontaneous EPSC rate (74.9 ± 8.6 Hz, one antenna); derived 17.4 × 3.44 ≈ 60/s.
- Cao 2016 (slice): Or22a-OSN "spontaneous firing at a frequency of 4 Hz".

Compilation via DoOR (studies that reported spontaneous rates; spikes/s):

| DoOR dataset | preparation | types | median | range | examples |
|---|---|---|---|---|---|
| Bruyne.2001.WT | wild-type antennal basiconic | 16 | 6 | 1-15 | ab2B 1, ab5B 2, ab3A 4, ab2A 5, ab1D 6, ab1A 9, ab4A 14, ab6A 14, ab1C (CO₂) 15 |
| Bruyne.1999.WT | wild-type palp | 6 | 8 | 6-32 | pb1A 11, pb2B 32 |
| Yao.2005.WT | wild-type coeloconic | 7 | 19 | 16-42 | ac3A 16, ac3B 26, ac4 42 |
| Hallem.2004.WT | wild-type | 4 | 15.5 | 6.9-61 | ab3A 6.9, ab2A 11.1, ab4A 19.9, at4A (Or47b) 61.1 |
| Hallem.2006.EN | receptor in the ab3A "empty neuron" | 24 | 12.5 | 1-47 | Or59b 2, Or22a 4, Or7a 17, Or19a 29, Or47b 47 |
| Kreher.2008.EN | receptor in the empty neuron | 23 | 11 | 1-18 | |

Source: DoOR.data per-receptor CSVs at <https://github.com/ropensci/DoOR.data>. Empty-neuron rates partly reflect the
ectopic receptor; Or47b gives high rates in both Hallem and Nagel.

Related facts:
- ORNs fire independently: "No correlation between DM4 ORN spike trains" (Kazama & Wilson 2009). For DA1, "ORNs are
  statistically independent" ([Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/)).
- Spontaneous ORN spikes drive PNs at rest: "In the absence of odors, PNs fire spontaneously (typically 1–5
  spikes/sec)" (Kazama & Wilson 2009). Spontaneous EPSCs in PNs "virtually always occur synchronously in ipsilateral
  homotypic PNs". Turner 2008 found PN spontaneous rate 4.6 ± 4.2/s and KC spontaneous EPSPs at 32.6 ± 12.7/s (see
  kenyon_cell_odor_responses.md).
- Glomerulus sizes: "Each Drosophila odorant receptor is expressed by ~40 olfactory receptor neurons (ORNs) in each
  antenna, on average" (Jeanne & Wilson 2015), with DM4 at 17.4 per antenna.

## 5. PN onset timing, synchrony across glomeruli, peak vs plateau (Q5)
- Bhandawat 2007: "PN responses rise and accommodate rapidly, emphasizing odor onset." "PN responses peak significantly
  faster than ORN responses (Fig. 2d, p<10⁻⁷, paired t-test, n=69 odor/glomerulus combinations), and the time to
  half-decay of the response is shorter for PNs". "the PN response is robust at a time point when the ORNs have just
  begun to respond, and the PN response begins decaying before the ORNs have peaked." Fig. 2 (fig.):
  - both PSTHs start rising at about 75 ms after valve opening;
  - PNs reach 90% of peak at about 140 ms (ORNs about 195 ms), peak at about 150 ms (ORNs about 225 ms) and fall to
    half at about 185 ms after peak (ORNs about 325 ms);
  - by 500 ms PNs are at about 0.48 of peak (ORNs about 0.75);
  - the first 200 ms holds about 37% of PN spikes (ORNs about 23%);
  - an example PN peaks at about 200 spikes/s while its ORNs reach about 55 spikes/s.
- Kazama & Wilson 2009: PN response onset ("10% of its peak") is "generally about 100 ms after nominal stimulus onset".
  On synchrony:
  - Sister PNs: "16.7 ± 1.3% versus 13 ± 1.0% of spikes occur within a 1.6-ms window of a spike in the other cell" (odor
    vs spontaneous).
  - Different glomeruli: "only 0.9 ± 0.7% of spikes are synchronous during odor-evoked activity (n = 15)".
  - "These correlations are non-oscillatory, are largely restricted to an individual glomerulus".
- Jeanne & Wilson 2015 (DA1, optogenetic ORN stimulation, so no odor transduction):
  - delays: "a delay of ~4.5 msec between an ORN spike and the start of an excitatory postsynaptic potential (EPSP) in a
    PN"; "The average time of the first evoked PN spike is 30 msec";
  - integration: an ORN-to-PN filter "had a duration of 23 msec"; "PNs integrate ORN spikes over a window of
    approximately 20–30 msec";
  - first spikes: "the typical first stimulus-evoked PN spike… actually precedes the typical first spike in any given
    ORN";
  - PN rates "were consistently about three-fold larger than ORN spike rates"; PN responses were "more prolonged" than
    ORN responses to the flash.
- [Nagel, Hong & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/): PN model "ORN spikes were delayed by a
  fixed amount (10 ms) such that the model and measured PN responses commenced with the same delay". Inhibition "is
  transient but grows slowly". "In a sparse regime, modeled inhibition decreased the duration of the impulse response
  (from 145 to 90 ms at half-maximum)". The functional effect of inhibition on PNs "begins ~100 ms after the peak in LN
  spiking".
- Kim 2015 (DM4): "To step-like OSN signals, PN showed a phasic onset response, followed by a tonic spiking pattern".
  For triangle ramps, "PNs consistently produced peak output… at around 200 ms after the stimulus onset, regardless of
  the dynamics of the odor/OSN signals".
- Seki 2017 (PNs from 31 glomeruli): "separation peaked at 150 ms and gradually declined to the baseline at 2 s after
  the onset".
- Slow PN adaptation (Martelli & Fiala 2019): "calcium activity in PNs decreases in all glomeruli proportionally to the
  initial response on timescales that vary in the range between 1 and 40 s"; mean degree of adaptation 0.57. This
  correlates with presynaptic vesicle depletion (τ₂ "of the order of ~10 s").
- Oscillations and periodic synchrony:
  - [Tanaka, Ito & Stopfer 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2753235/) (23 °C) found "oscillatory responses
    with an average frequency of ∼10 Hz", with PN spikes "tightly phase-locked to LFP oscillations recorded in the MB…
    126 +/− 46°". But "oscillations were typically not elicited by the first presentation of an odor, but rather
    emerged gradually upon repeated presentations", and could begin "up to 500 ms delay" after odor arrival.
  - Turner 2008: "We could find no significant evidence for consistent periodicity in these [KC] traces"; "in systems
    with low convergence, such as Drosophila, sparseness can be achieved without oscillations".
- Not read: Wilson, Turner & Laurent 2004 (Science), the PN source of Turner 2008's model inputs.

## 6. Published ORN models with fitted parameters (Q6)
- **Kadakia & Emonet 2019** (eLife; code at <https://github.com/emonetlab/ORN-WL-gain-control>).
  - Activity: "A_a(t) = [1 + exp(ε_a(t) + ln((1 + K_a·s(t))/(1 + K*_a·s(t))))]⁻¹".
  - Adaptation: "τ dε_a(t)/dt = A_a(t) − A_0a", with ε bounded by ε_L (which sets the spontaneous rate) and ε_H, and
    "τ ≃ 250 ms".
  - Output: "r_a(t) = f(h(t) ⊗ A_a(t))", with "Nonlinearity f… a linear rectifier with 5 Hz threshold" and "Euler method
    with a 2 ms time step". "A_0a ≃ 0.1 (corresponding to 30 Hz on a 300 Hz firing rate scale)".
  - Paper's filter: "h(t) = A pGam(t; α1, τ1) − B pGam(t; α2, τ2), A = 190, B = 1.33, α1 = 2, α2 = 3, τ1 = 0.012, and
    τ2 = 0.016".
  - Code's filter (`src/kinetics.py`, `src/four_state_receptor_CS.py`): kernel = kernel_scale·[gamma.pdf(t, 2,
    scale = 0.006) − 0.5·gamma.pdf(t, 3, scale = 0.008)], kernel_scale = 1/0.63, then × NL_scale 300 with threshold
    0.05, capped at 300 Hz.
  - The two disagree. Derived shapes:

    | version | shape | net/positive area | steady-state rate at A = 0.1 |
    |---|---|---|---|
    | paper as printed | essentially monophasic (negative lobe area 0.0004 vs positive 189) | about 1.0 | about 19 Hz |
    | code defaults | peak 5 ms, zero-crossing 22 ms, trough 32 ms | 0.80 | about 24 Hz |

    Only the code version is the "derivative-taking bi-lobed filter" the text describes.
  - The same τ, h and f are used for every receptor, justified by "adaptation is not intrinsic to the receptor".
- **Gorur-Shandilya et al. 2017** (two-state Or-Orco complex with chemotaxis-like integral feedback).
  - Equations:
    - "da/dt = (1 − a) w₊(S, ε) − a w₋(S, ε)"
    - "dε/dt = β(a − a₀)"
    - steady state "ā = 1/(1 + e^ε (1 + S/K_off)/(1 + S/K_on))"
    - "w₊ᵘ + w₋ᵘ = α = w₊ᵇ + w₋ᵇ"
    - LFP = C₀ (K_LFP ⊗ a), with K_LFP a Gamma kernel "t^m e^(−t/τ)/(m! τ^(m+1))"
    - firing "R_F = N(K_F ⊗ ā)", with "K_F = K₁ + αK₂" (two Gamma kernels) and N threshold-linear.
  - Fit (LFP, ab3A/ab2A): "α = 12.5 s⁻¹, β = 1.26 s⁻¹, ε_L = 0.86, K_on = 0.1 V and K_off = 400 V" (PID volts). The K_F
    kernel parameters were not given in the text.
  - The model reproduces Weber-Fechner gain and the slowdown of LFP kinetics with background.
- **Lazar & Yeh 2020** (PLoS Comput Biol; fitted to Or59b/acetone from Kim et al.).
  - Equations:
    - "v = h ⊗ u + γ h ⊗ du" (rectified)
    - "dx₁/dt = b·v·(1 − x₁) − d·x₁"
    - "dx₂/dt = α₂·x₁(1 − x₂) − β₂·x₂ − κ·x₂^(2/3)·x₃^(2/3)"
    - "dx₃/dt = α₃·x₂ − β₃·x₃"
    - "I = x₂^p/(x₂^p + c^p)·I_max"
    - spikes from a Connor-Stevens model.
  - Table 2: α₁ = 45 s⁻¹ and β₁ = 0.8 (peri-receptor low-pass), γ = 0.2105 s, α₂ = 146.1 s⁻¹, β₂ = 117.2 s⁻¹, α₃ = 2.539
    s⁻¹, β₃ = 0.9096 s⁻¹, κ = 8841 s⁻¹, c = 0.06546, p = 1, I_max = 62.13 pA.
  - Rates: binding "2.17 ⋅ 10⁻² ⋅ (ppm ⋅ s)⁻¹", dissociation "2.94 ⋅ s⁻¹". 2-butanone binding is 2.18×10⁻¹. Or59b/methyl
    butyrate: affinity 4.264×10⁻³ ppm⁻¹ and dissociation 3.788 s⁻¹. Or7a/butyraldehyde: 7.649×10⁻⁴ ppm⁻¹ and 8.609 s⁻¹.
  - "the OTP/BSG cascades reach steady state roughly after 3 seconds". Derived: 1/d ≈ 0.34 s sets the unbinding/off
    time scale.
- **Martelli 2013 LN model** (ab3A, methyl butyrate).
  - Odor-to-ORN filter: "a positive and a negative lobe… integration time… ~100ms". Fig. 7d (fig.): positive peak at
    about +10 ms, trough about −0.5 at about +35 ms, back to about 0 by about 60-100 ms.
  - Nonlinearity "r = 1/(1 + (H/r_lin)^n)", a rectifier. Prediction quality NR = 0.41 (< 1 means within trial noise).
  - The same filter shifted 4 ms predicted 1-octen-3-ol responses from the PID trace (NR = 0.44). pb1A has "a smaller
    negative lobe".
- **Kim, Lazar & Slutskiy 2011** 2-D LN model (Or59b/acetone): "h1… a low-pass filter with a −3 dB cut-off frequency
  of about 20 Hz"; "h2(t) exhibits a biphasic pattern with positive and negative peaks at around 75 ms and 150 ms",
  band-pass 1-12 Hz.
- **Nagel & Wilson 2011**: a kinetic binding scheme (forward rate ∝ concentration; adaptation lowers affinity or gating
  efficacy) feeds a universal biphasic LFP-to-spike filter (Fig. 3e shape above). No numeric parameters were published
  in the main text.
- **ORN-to-PN synapse parameters**:
  - Nagel, Hong & Wilson 2015, fast component: "r = 0.23 spike⁻¹, τA = 1006 ms, k = 20 nS/spike, and τg = 9.3 ms".
  - Their slow component: "r = 0.0073 spike⁻¹, τA = 33247 ms, k = 1.8 nS/spike, and τg = 80 ms". Their PN uses Rm =
    800 MΩ, τm = 5 ms and a unitary EPSP of about 7 mV.
  - Kazama & Wilson 2009 depression fit: "α = 0.72 and τ = 2.4 s".

## 7. Inferences for brainfly (mine, not from the literature)
- The instant, constant, all-glomeruli-at-once step is the most synchronous input the KCs could get. Real onsets are
  ordered by drive. Strong glomeruli fire within about 5-15 ms of arrival, nearly together. Weak ones follow 20-60 ms
  later with large jitter. On top, odor arrival rises over τ_on ≥ 25 ms and ORN firing over about 30-120 ms. Whether
  this lowers KC response density is an empirical question for the model. The near-threshold KCs are the ones driven
  by several moderate glomeruli, and those are the ones the spread desynchronizes.
- A minimal replacement drive per glomerulus g with DoOR response s_g in 0-1 (my synthesis, to be tuned):
  - spontaneous rate from the DoOR SFR row, 2-15 Hz per ORN;
  - onset at t_arrival + L(s_g), with L about 3-5 ms for s near 1, rising to about 30-50 ms for s near 0.1, plus
    trial jitter of the same order at low s;
  - rise with τ_r about 20-40 ms to a peak of s_g·max_hz;
  - decay with τ_a about 0.1-0.4 s to a plateau of 0.4-0.7 of peak;
  - at offset, a drop to about 0 for about 100-300 ms (dose-dependent), then recovery to spontaneous over about 0.5 s.
  - Alternative: run Kadakia & Emonet's code-default filter on an adapting activity A(t), with the odor input low-passed
    by τ_on (25 ms for esters, longer for low-volatility odors).
- Spontaneous ORN firing (about 20-40 ORNs × 2-15 Hz per glomerulus per antenna) gives PNs 1-5 spikes/s at rest, and
  KCs a steady background of PN EPSPs (Turner: 32.6/s spontaneous EPSPs). With silent ORNs, KCs start each odor from a
  quieter state than in vivo.
- Three emergent checks for the PN layer: PN 90%-of-peak about 55 ms ahead of ORNs; PN at about 0.5 of peak by 500 ms;
  heterotypic PN spike synchrony near 1%. PN onset sharpening comes from ORN-to-PN depression plus slow-growing
  inhibition, not from the ORN drive.
- Turner 2008's sparseness (6 ± 5%) came from 500 ms pulses at 1:1000 with about 100 ms delivery delay, counted over 2
  s. Under those conditions ORN rates fall to about 0.5-0.75 of peak by pulse end. Their model reproduced 6% using
  recorded PN time courses (benzaldehyde, 23 PNs), not steps.

## Conflicts and gaps
- **"Latency" is measured several ways**, giving 3 to about 450 ms for related quantities:
  - first spike from PID-measured arrival: 3-55 ms;
  - filter-peak delay after deconvolution: 12 ms;
  - LFP filter absolute latency: < 10 ms;
  - receptor current to 10% of peak in liquid: 35-66 ms;
  - cross-correlation lag to Gaussian noise: 50-95 ms, which includes integration time;
  - time to peak from the valve: 100-450 ms, which includes delivery.
  Compare only like with like.
- **Concentration dependence:** Egea-Weiss finds first-spike latency falls steeply with concentration. Martelli
  (normalized PSTH shape) and Gorur-Shandilya (firing lag vs background) find timing roughly invariant mid-range. The
  measures differ (first spike from rest vs smoothed PSTH or adapted-state lags), and 10-20 ms latency shifts would be
  hidden by 50 ms smoothing. Nagel finds LFP onset rate rises with concentration.
- **Or vs Ir speed:** Getahun (air, with slow acids through 150 cm tubing) finds Ir ORNs slower. Cao (liquid
  application in slices) finds them faster. Odor delivery is the likely confound.
- **Plateau/peak** ranges 0.3-0.85 across odor-receptor pairs and concentrations. Bhandawat's mean of about 0.75 at
  500 ms vs Martelli's about 0.5 likely reflects the inclusion of slow and tonic odor-glomerulus pairs.
- **Spontaneous rates:** Kadakia & Emonet cite "1–10 Hz (Hallem and Carlson, 2006)", but DoOR's Hallem.2006.EN rows
  span 1-47 Hz (median 12.5) and are empty-neuron values. Hallem & Carlson 2006 and de Bruyne 2001 full texts were not
  accessible (Cell Press blocked), so their values here are via DoOR only.
- **Kadakia & Emonet's printed filter coefficients vs their released code** are inconsistent (§6). Use the code
  defaults if a bi-lobed filter is wanted.
- **Correction to sensory_periphery.md §2:** the "peak-to-steady-state ratio 1.7-2.3" it cites from Nagel & Wilson 2011
  belongs to the DmNav knock-down ORNs. Controls are about 1.4 (Fig. 5d, fig.).
- **Main gap:** no Drosophila study has measured ORN or PN onset latencies across many glomeruli simultaneously for one
  odor at ms resolution. The closest are Egea-Weiss (2 ORN types) and Paoli 2018 (honeybee PNs, calcium imaging).
- **Other gaps:**
  - No PID record exists for Turner 2008's rig.
  - No dataset maps DoOR response magnitude to latency across ORN types.
  - Egea-Weiss's Transparent Methods (temperature, n per condition) were not read.
  - Temperature dependence of ORN kinetics was not found; most recordings are at about 20-25 °C.
  - Trichoid (pheromone) ORN kinetics were not covered.
  - Wilson, Turner & Laurent 2004 PN data were not read.
  - The Gorur-Shandilya K_F kernel parameters are not in the text.
- **Title check:** the brief's "Kim, Lazar & Wilson 2011 J Neurosci 'Smoothing…'" does not exist in PubMed. The
  matching paper is Kim, Lazar & Slutskiy 2011, J Comput Neurosci, "System identification of Drosophila olfactory
  sensory neurons" (PMC3736744). Lazar's lab followed it with Kim et al. 2015 eLife and Lazar & Yeh 2020.
