# Rung 4: spike-frequency adaptation and intrinsic properties for the MaleCNS LIF

Compiled 26 Sep 2026 by a research agent (four literature sub-agents plus my own checks, code reading and toy simulations). Drosophila melanogaster measurements only unless flagged **[other insect]**.

**Conventions**
- **[PP]** = preprint. WC = whole-cell. RT = room temperature.
- **fig.** = read off a figure (±5–10%). **derived** = my arithmetic on published numbers. **toy** = my simulation (§6).
- Wilson-, Jefferis-, Jeanne-, Maimon- and Nagel-lab voltages are usually *not* corrected for the ~13 mV liquid-junction potential, so true Vm is ~13 mV lower. Somatic resting potentials are also biased depolarized by the seal shunt in these GΩ cells.
- I re-read the key quoted sentences in the full texts. Figure read-offs and the Seki 2010 table (read by a sub-agent in a browser; journals.physiology.org blocks scripts) were not re-checked by me.

---

## 0. Recommendations (summary)

### 0.1 Model form and conversion rules

```
tau_m dV/dt = -(V - V_rest) + g + bias + noise - a1 - a2      (same mV units as Shiu's g)
tau1 da1/dt = -a1        on spike: a1 += b1                    fast SFA ("mAHP-like")
tau2 da2/dt = -a2        on spike: a2 = min(a2 + b2, a2max)    slow Na+/K+-pump AHP
on spike: V -> V_reset, g -> 0 (Shiu's code does this; HybridBrain already does)
```

Rules, all derived in §6 and checked by simulating one Shiu-constant LIF:
- **k = b·τ** (mV per Hz) sets the steady state: ⟨a⟩ = k·r. τ only sets how fast it arrives.
- **Adaptation ratio A** (steady rate ÷ unadapted rate) ≈ 1/(1 + G·k). G ≈ 5 Hz/mV for Shiu constants (3–7 over 10–150 Hz). So k ≈ (1/A − 1)/5.

  | A | 0.9 | 0.8 | 0.7 | 0.6 | 0.5 | 0.4 | 0.3 | 0.2 |
  |---|---|---|---|---|---|---|---|---|
  | k (mV/Hz) | 0.02 | 0.05 | 0.09 | 0.13 | 0.2 | 0.3 | 0.47 | 0.8 |

- The rate relaxes with τ_obs ≈ τ·A, so a measured decay time converts as τ ≈ τ_obs/A.
- **Recalibrate the tonic bias:** bias_new ≈ bias_old + (k1 + k2)·r_target, then re-check (noise-driven firing is not exactly linear).
- **Ignition:** a loop holds itself at rate r if J − k ≥ (μ(r) − μ0)/r. Here J is drive per Hz of partner firing: 0.275 mV × 5 ms = 0.0014 mV/Hz per co-active loop synapse. μ0 is the tonic bias.
  - The threshold is lowest at **0.217 mV/Hz, near 80–100 Hz** (about 160 co-active loop synapses). That is why ignited loops sit at ≥100 Hz.
  - Bias lowers it: 0.19 mV/Hz with 2 mV of bias, 0.16 mV/Hz with 4 mV.
  - Adaptation raises it one for one with k.

### 0.2 First-pass values

| Component | τ | b per spike | k = b·τ | Apply to | Evidence (details §1, §3) |
|---|---|---|---|---|---|
| **Fast SFA, class N** (none) | – | 0 (≤ 0.1 mV) | ≤ 0.02 | uniglomerular ALPNs; KCs; l-LNv; MBONs; tonic MNs; DNg13; slow tibia MN | PN rate 104.2% of initial after 500 ms at >100 Hz ([KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)); larval MNs "no evidence of accommodation or adaptation during 400 ms" ([Schaefer 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2944697/)); SFA in 1% (3/253) of l-LNvs ([Buhl 2026 PP](https://doi.org/10.64898/2026.02.04.703843)); KC trains sustained through 0.75–1 s steps, AHP ≈2.8 mV ([Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/); [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/)) |
| **Fast SFA, class M** (moderate; default for unmeasured spiking types) | **200 ms** (100–500) | **0.5–1 mV** | 0.1–0.2 | AL LNs (Krasavietz-like, dorsolateral); pIP10-like DNs; MN5 subset | LN rate ratio 0.61–0.65 ([Seki 2010](https://doi.org/10.1152/jn.00249.2010)); first/final-ISI ratio 0.49 at 22 °C ([Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/)); pIP10 10th/1st ISI 0.45–0.77 ([Roemschied 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10600009/)); adaptive cultured neurons f_last/f_first < 0.7 ([Zhao & Wu 1997](https://pmc.ncbi.nlm.nih.gov/articles/PMC6793766/)) |
| **Fast SFA, class S** (phasic) | 200 ms | 2.5–5 mV | 0.5–1 | NP2426-like LNs (lLN2?); giant-fibre-like single spikers; NP1227 bursters (better as a burst model) | NP2426 rate ratio 0.13, NP1227 0.04 (bursting) ([Seki 2010](https://doi.org/10.1152/jn.00249.2010)); one GF spike per escape ([Dombrovski 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/)) |
| **Slow pump AHP** | **3 s** (2–10) | **0.03–0.1 mV**, a2max ≈ 15 mV | 0.1–0.3 | LH neurons (measured); plausibly all spiking types | LHPD2a1/b1 in vivo: Na⁺/K⁺-ATPase "divisive adaptation", kernel >3 s, gain ×~0.6, roughly k ≈ 0.13 if read as subtractive ([Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/)). Larval MNs: "~20 mV" after 5 s at 100 pA, "15–20 sec" recovery, "proportional to spike number", ~0.06–0.11 mV per spike, saturating ~15 mV (fig.) ([Pulver & Griffith 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2839136/)) |
| **Fast AHP via reset** | instantaneous | V_reset = V_rest − 5 mV (0 to −10) | – | all spiking | Somatic spike AHPs: LNs −1.5 to −6.9 mV ([Seki 2010](https://doi.org/10.1152/jn.00249.2010)); KCs ≈−2.8 mV (fig., [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/); [Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/)); IPCs 8.1 ± 0.2 mV ([Kréneisz 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3075590/)); l-LNv 5 ± 1 mV ([Sheeba 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2692874/)). Kakaria's −20 mV undershoot is a model choice |

**One global setting**, if you want one:
- b1 = 0.5 mV at τ1 = 200 ms, plus b2 = 0.05 mV at τ2 = 3 s (a2max 15 mV), with b1 = 0 for ALPNs and KCs.
- That gives k ≈ 0.25 mV/Hz, so add ~1.25 mV of bias for a 5 Hz target and ~9 mV for a 37 Hz one (MBON11).
- At a sustained 100 Hz: a1 → 10 mV (τ 0.2 s) and a2 → 15 mV (the cap; τ 3 s). Holding 100 Hz then needs ~2× the recurrent drive (21.7 + 25 mV instead of 21.7 mV).

**What to expect** (toy results §6, and other groups §4):
1. **Adaptation raises the ignition threshold by about k.** 100–300 Hz fixed points disappear once k > J − 0.22 mV/Hz.
2. **Adaptation alone can make things worse.** If a loop is well above threshold and bias holds its cells near firing, τ1 ≈ 200 ms turns the runaway into ~1 Hz population bursts, and τ2 of seconds gives slower relaxation cycles. Both would dominate a 1.2 Hz resting-state FC fit. If bursts appear, the loop is still supercritical: fix J (signs, weights, depression), not b.
3. **Evidence from other whole-brain runs:**
   - kazemi (MaleCNS, Shiu LIF): SFA with k ≤ 0.2 mV/Hz and τ = 100 ms did **not** end self-sustained states (6–9/9 trials still ignited). STD of 5–10% per spike with 200 ms recovery ended all of them ([STABILITY.md](https://github.com/kazemi-mahdi/fly-escape-circuit/blob/main/STABILITY.md)).
   - flybench (FlyWire, gain 0.45): b = 2 mV, τ = 200 ms (k = 0.4) fixed return-to-rest ([results](https://github.com/brandoncho369/flybench/blob/master/results/adaptive-lif-b-2-mv-tau-200-ms.json)).
4. **Measured fast SFA is mostly k ≤ 0.2.** Stopping LH/SLP ignition will need the slow pump term (measured in LH), STD and fixes to drive. Fast SFA alone won't do it.

### 0.3 Levers the data support more strongly than generic SFA
- **Threshold gap per type.**
  - Data: PNs and LH neurons need ~10 mV of depolarization to spike ([Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/)). KCs sit 21.5 ± 5.6 mV below threshold ([Turner 2008](https://doi.org/10.1152/jn.01283.2007)); 8.2 mV for αβc ([Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/)); γ KC threshold ≈−22 mV vs rest ≈−61 mV (fig., [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/)).
  - The model uses 7 mV everywhere. The ignition threshold scales linearly with the gap (derived): 0.31 mV/Hz at 10 mV, 0.46 at 15 mV.
- **Lower resting targets for LH.** LHONs 0.1 Hz, LHLNs 1 Hz, PNs 1.4 Hz ([Frechter 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/)). Every mV of tonic bias lowers the ignition threshold.
- **STD on recurrent excitatory synapses.**
  - ORN→PN: f = 0.78, τ_rec = 893 ms ([Nagel 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/)). ORN→LN: f = 0.75, τ_rec = 1566 ms ([Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)).
  - PV5a1's transience is PN→LHN depression with slow recovery, not intrinsic ([Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/)).
  - In the toy loop, STD with ORN→PN values stabilized loops that adaptation could not.
- **AL LN transmitter signs.**
  - 120 AL LNs labelled cholinergic in the MaleCNS export carry two thirds of kazemi's seizure state; making them inhibitory stops smell-triggered ignition ([STABILITY.md](https://github.com/kazemi-mahdi/fly-escape-circuit/blob/main/STABILITY.md)).
  - Seki found the Krasavietz LNs, reported earlier as cholinergic, "were mostly GABAergic" ([Seki 2010](https://doi.org/10.1152/jn.00249.2010), abstract).
- **Non-spiking types should be graded.**
  - APL: "non-spiking and exhibit graded responses", Rin ~120 MΩ ([Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/)).
  - Patchy LNs: no action potentials, no Na⁺ current ([Schenk & Gaudry 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9884108/)).
  - B1 and APN2 are graded ([Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/); [Suver 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6533146/)).
- **Refractory period.**
  - Measured sustained maxima: PNs ~160 Hz over 500 ms (fig., [KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)); odor-evoked R_max 165 Hz ([Olsen 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/)); LN peak instantaneous 105 Hz at 22 °C and 205 Hz at 30 °C ([Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/)); larval MN bursts 90–110 Hz ([Kadas 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC8130532/)).
  - The 2.2 ms refractory allows 455 Hz. A 4 ms refractory caps at 250 Hz and raises the drive for 100 Hz from 21.7 to 27 mV (derived).

### 0.4 Firing-rate homeostasis (details §5)
- **Where it is shown:** embryonic and larval motor neurons, and cultured embryonic neurons, over hours to days. Channel compensation restores the evoked f–I curve ([Kulik 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6491091/); [Baines 2001](https://pmc.ncbi.nlm.nih.gov/articles/PMC6762927/); [Parrish 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4104505/)).
- **Adult central brain:** only partial, days-long, circuit-level compensation.
  - KC responses rose 1.3–2.6× after 4 days of excess APL inhibition; there was none after APL block ([Apostolopoulou & Lin 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7368247/)).
  - Shal and nAChR rose after 24 h of curare in brain explants, stabilizing EPSPs ([Ping & Tsunoda 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3888491/)).
  - State switches in sleep neurons ([Pimentel 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/)).
- **Anti-homeostatic cases also exist** ([Lin 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3400946/); [Coulson 2025 PP](https://doi.org/10.64898/2025.12.01.691172)).
- **No study shows per-neuron spontaneous-rate set points in adult central neurons.** Per-type bias calibration to measured rates is a modelling convenience, not a biological mechanism. Kennedy's KC model used per-neuron thresholds as a stated assumption, noting "homeostatic plasticity of KCs has not been reported" ([Kennedy 2019 PP](https://doi.org/10.1101/783191)).

---

## 1. Measured adaptation by cell type

### 1a. Antennal lobe and lateral horn

| Type (MaleCNS) | Adaptation evidence | Prep | Source |
|---|---|---|---|
| Uniglomerular ALPNs (DM1_lPN, DM6/VM2/DL5/DM4_adPN, VM7d_adPN, DA1_lPN) | **None over 500 ms:** "Even when injected current was sufficient to produce firing rates >100 spikes/s, PN responses did not decline over the course of 500 ms (final firing rates were 104.2% of the initial rate, n = 8 cells)". Odor transience is synaptic: ORN→PN depression (f 0.78, τ_rec 893 ms; components f 0.77 / 1006 ms and 0.91 / 629 ms) plus presynaptic inhibition rising with an α-function of τ ≈ 25 ms | in vivo WC | [KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/); [Nagel 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/) |
| same | Slow adaptation of spike generation over seconds (10-s odor backgrounds): "Background adaptation is strongest at the level of PN spikes". Values in fig. only; mechanism unknown | in vivo WC | [Cafaro 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4831330/) |
| same | Single-spike AHP decay ~80–110 (units unstated, probably ms) | ex vivo perforated | [Leier 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11781797/) |
| same | α1T (Cav3) knockdown raises evoked spikelet frequency and gives "a fourfold increase in the number of spikelets/burst"; ex vivo bursts at 0.22 Hz in blockers | ex vivo, RT | [Iniguez 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/) |
| Postsynaptic GABA-B in PNs | Picrotoxin blocks only 46 ± 5% of the GABA response; GABA-B shapes the 1.5–2.5 s epoch, "inhibitory epochs on the timescale of tens to thousands of milliseconds". No IPSC τ in the text | in vivo | [Wilson & Laurent 2005](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/) |
| AL LNs, Krasavietz class 1 / class 2 | Spike adaptation (spikes in first 500 ms ÷ first 1 s; 50% = none): 60.5 ± 5.0% (n = 5) and 62.3 ± 9.0% (n = 6). Rate ratio (2nd ÷ 1st 500 ms, derived) 0.65 / 0.61 → k ≈ 0.11–0.13 | ex vivo, held ~−50 mV, 3-s steps of 3–20 pA | [Seki 2010](https://doi.org/10.1152/jn.00249.2010) (Table 1) |
| NP1227 class 1 (→ lLN1?) | 96.1 ± 7.2%; bursts of 7.4 ± 3.1 spikes at 43.7 ± 22.3 Hz | same | same |
| NP2426 class 1 (→ lLN2?) | 88.3 ± 8.4% (rate ratio 0.13): "fast spike adaptation and terminated spiking after a few action potentials" | same | same |
| Dorsolateral AL LNs | "Adaptation ratio (ISI first/ISI final at half-maximal firing)" 0.49 ± 0.07 at 22 °C, 0.27 ± 0.05 at 30 °C (k ≈ 0.21 and 0.54); peak instantaneous 104.7 ± 12.4 Hz / 205.3 ± 22.8 Hz | ex vivo, 600-ms steps, curare + picrotoxin | [Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/) |
| AL LNs in vivo | Rebound spiking in "eight of eight LNs"; bursty cells repolarize slowly; ORN→LN depression f 0.75, τ 1566 ms; LN→LN inhibition builds slowly and facilitates | in vivo WC | [Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/) |
| Patchy LNs (R32F10) | Non-spiking: "we did not detect action potentials nor sodium current" | in vivo | [Schenk & Gaudry 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9884108/) |
| **LHPD2a1/b1** ("LHN1") | **Intrinsic slow adaptation:** "Divisive adaptation is due to slow cellular gain control implemented by the Na+/K+ ATPase in the postsynaptic neuron". "Hyperpolarization was also evident after pulses of current injection". Fig.: trough about −3.5 mV (odor) and −5 mV (+15 pA pulses at 1.25 Hz) vs −1 mV with dominant-negative ATPase; kernel >3 s; adapted/unadapted gain ~0.6 (0.95 with dominant-negative). Odor 5 Hz pulses: ~19 → ~5 sp/s including synaptic depression. "adaptation had minimal direct impact on LHN excitability" (threshold) | in vivo WC | [Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/) |
| LHPV5a1 ("LHN2") | Transient (~23 → ~0.5 sp/s, fig.) but synaptic: slow recovery from PN→LHN depression plus facilitation; inhibition blockers did not remove it | in vivo WC | same |
| DA1-recipient LHNs (aSP-f/g subset) | "more transient than those of PNs"; "Stimulus onset lowered the threshold for LHN spikes by about 20%" (dynamic threshold) | in vivo WC | [Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/) |
| Mz671 type I / NP6099 type II LHNs | Type I "steady over time"; spikes shrink at high rates (consistent with Na⁺ inactivation). Type II transient, attributed to inhibition | in vivo WC | [Fişek & Wilson 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3992254/) |
| SLP intrinsic types | No whole-cell data found | – | – |
| ORNs (model inputs) | Spike generator is a "differentiating linear filter"; receptor-current adaptation recovers with τ 1.27 s (Or22a); gain control within ~130 ms | extracellular; slice | [Nagel & Wilson 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3030680/); [Cao 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4763727/); [Gorur-Shandilya 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5524537/) |
| JONs / APN3 / AMMC-VLP | JON adaptation "5–20 ms", in the generator current; APN3 τ 1.1 / 5.2 s (partly inherited); AMMC/VLP mostly graded, ~2 s in a phenomenological model | various | [Clemens 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5760620/); [Chang 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5749228/); [Clemens 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4629847/) |

### 1b. Mushroom body

| Type | Adaptation evidence | Prep | Source |
|---|---|---|---|
| KCs (all subtypes) | **No Drosophila SFA index or τ exists.** Example trains stay sustained through 1-s (Groschner), 750-ms (Chen) and 1-s (Greenin-Whitehead) steps. AHP ≈2.8 mV (fig.). "current injection experiments showed no evidence of a non-linear component … other than spike threshold". αβc Shal: inactivation τ 37.2 ± 2.4 ms at +50 mV; "KCs lack significant Ca2+ currents" (argues against a big K_Ca AHP) | in vivo / ex vivo | [Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/); [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/); [Greenin-Whitehead 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12487611/); [Gruntman & Turner 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/) |
| γ KCs after learning | "Pairing KC depolarization with PPL1-γ1pedc activation did not change the spike threshold or the sustained spike rate" | in vivo | [Hige 2015 Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/) |
| MBON11 (γ1pedc>α/β), MBON18 (α2sc), MBON06 (β1>α) | Sustained through 1-s odor ("persisted throughout the duration of the 1-s odor pulse"). 15-s odor decays are network-driven (fig.): α2sc ≈37 → 6 Hz, γ1pedc ≈57 → 20, β1>α ≈36 → 17 | in vivo WC | [Hige 2015 Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/); [Vrontou 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/) |
| MBON07 (α1) | Sustained firing through 1-s steps of 0–10 pA (qualitative) | in vivo | [Nanami 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11238178/) |
| APL | Non-spiking. SK-type AHP after a 1-nA step: ≈2.5 mV rested vs ≈6 mV after 12 h of sleep deprivation (fig.); "decay time constant of the enhanced AHP is 491.1 ± 72.17 ms" | ex vivo | [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/) |
| **[other insect]** KCs | Cockroach: "strong spike frequency adaptation" via I_Ca and I_O(Ca) ([Demmer & Kloppenburg 2009](https://doi.org/10.1152/jn.00183.2009)). Honeybee culture: "little frequency adaptation" ([Wüstenberg 2004](https://doi.org/10.1152/jn.01259.2003)). The strong KC SFA in Nawrot-lab fly models (§4) rests on these | – | – |

### 1c. Central complex, sleep and clock

| Type (MaleCNS) | Evidence | Prep | Source |
|---|---|---|---|
| PEN_a / PEN_b | No step-adaptation data. "strong rhythmic/burst activity with an interval of approximately 350 msec". Rebound after hyperpolarizing pulses | in vivo WC | [Currier 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793622/); [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PFNa | T-type "wide (~200 ms) calcium spikes", 2–6 Hz when hyperpolarized | in vivo WC | [Ishida 2026 Cell](https://pmc.ncbi.nlm.nih.gov/articles/PMC12758628/) |
| dFB sleep neurons (FB6A/C/E/G/I/Z …) | Two states. OFF (dopamine, Sandman K2P leak): "Input resistances and membrane time constants dropped to 53.3 ± 1.8 and 24.0 ± 1.3% of their initial values"; switching τ 1.07–1.10 min; OFF lasts 7–60 min (mean 25.86). I_A inactivation τ 7.5 ± 2.1 ms supports fast firing rather than causing adaptation | in vivo WC | [Pimentel 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/); [Donlea 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3969244/); [Kempf 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6522370/) |
| ExR1 (helicon) | UP state "16.9 ± 3.6 Hz", DOWN "< 1 Hz", baselines 10.9 ± 2.3 mV apart | in vivo WC | [Donlea 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5779612/) |
| ER5 ("R2" in Liu 2016) | Spontaneous rate "~3-fold" higher at ZT13–15 than ZT0–2, higher still after sleep deprivation; bursting in "6 of 8" sleep-deprived cells, never at baseline; Rin unchanged | perforated patch | [Liu 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4892967/) |
| l-LNv | "only 1% (3 of 253)" slow and stop within a pulse (26% of mouse VIP neurons); "typically fired repetitively throughout the entire depolarising pulse" | ex vivo, 20–22 °C | [Buhl 2026 PP](https://doi.org/10.64898/2026.02.04.703843) |
| DN1p | "all experimental conditions showed a spike frequency adaptation" (300-ms steps). Monoexponential fit: half-life 2.8–12.8 ms, plateau 20.7–27.1 ms (units as printed, not convertible); aging weakens it. Night-time slowpoke (K_Ca) rise deepens the AHP | ex vivo | [Nguyen 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8959858/); [Tabuchi 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6239908/) |
| PI neurons | Dh31/Dh44 change the SFA index (1st ÷ nth ISI); AHP sensitive to Cd²⁺ not apamin: "KCa channels other than SK channels are likely to be the primary effectors" | ex vivo | [Chong 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11906214/) |

### 1d. Descending and motor neurons

| Type | Evidence | Prep | Source |
|---|---|---|---|
| **pIP10** | **Measured SFA** (my analysis of Extended Data Fig. 8 source data): 10th-ISI rate ÷ 1st = 0.24 / 0.45 / 0.67 / 0.71 / 0.77 at 13 / 28 / 44 / 59 / 74 pA (k ≈ 0.06–0.24 for 28–74 pA); median instantaneous rate 5.9 / 22.4 / 34.1 / 45.7 / 52.4 Hz (≈0.77 Hz/pA). One 5-s trial at 74 pA: first ISI 36 ms (~28 Hz) but 6.6 Hz over the step, with doublets. Raw Vm −37.8 mV (LJP uncorrected); rebound spikes | in vivo WC | [Roemschied 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10600009/) |
| DNg13 | "neither adapted during the step" (0.5–1 s, −75 / +100 pA) | in vivo WC, 28–30 °C | [Yang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12778575/) |
| DNa02 vs DNa01 | "DNa02 fires more transiently than DNa01" in behaviour (not tested with current steps) | in vivo WC | [Rayshubskiy 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12279373/) |
| Giant fibre (DNp01) | One spike per escape; head-fixed it depolarizes to looms without spiking | in vivo WC | [Dombrovski 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/) |
| DNp03 | Activity outlasts the visual stimulus; looms spaced 30 s "to prevent habituation" | in vivo WC | [Croke 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12977095/) |
| Tibia flexor MNs | Intermediate: brief onset burst at 180 pA (example trace); slow: rate raised through a 50-pA step with no visible adaptation | in vivo WC, RT | [Azevedo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7347388/) |
| MN5 (DLM) | 38% fire one spike at low current, then "additional APs with spike frequency adaptation"; 42% tonic | in situ WC, ~22 °C | [Herrera-Valdez 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC6595220/) |
| MN5 in flight | Spike-count memory: one extra spike lengthens the next ISI "roughly 15%"; 3 → 9 extra spikes take it from 1.3× to "nearly 3-fold", no further at 11; depends on spike number, not frequency; partly HCN (ZD7288 hyperpolarizes 10 mV); "time courses between 100 and 600 ms" | in vivo, tethered flight | [Huthmacher 2025 PP](https://doi.org/10.1101/2025.06.16.659928) |
| MN1–5 (DLM) | "MN1–5 respond to constant input with slow tonic firing"; f–I "approximately linearly related for 2–30 Hz" | in situ WC | [Hürkey 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10232364/) |
| Larval aCC, RP2, RP3, MNISN-Is | "no evidence of accommodation or adaptation during 400 ms current injections" | ex vivo L3 | [Schaefer 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2944697/) |
| Larval MNISN-Is, MN30-Ib | **Na⁺/K⁺-pump ultraslow AHP.** After a 5-s 100-pA step "the membrane potential hyperpolarizes by ~20 mV and then takes 15–20 sec to return to baseline". Input resistance unchanged; ouabain abolishes it; "AHP amplitudes were proportional to spike number regardless of" pattern. Fig.: ~0.06–0.11 mV per spike, saturating ~15 mV; recovery τ ≈ 4 s early and 8–12 s late (derived). Over 20 bursts the intraburst rate falls only 10–20%, but first-spike delay lengthens (Shal de-inactivation) | ex vivo fillet | [Pulver & Griffith 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2839136/) |
| Cultured embryonic neurons | Classes: "Adaptive" = latency <100 ms and f_last/f_first < 0.7; "Tonic" > 0.7. "TEA-sensitive, slowly inactivating K+ currents were predominant in adaptive cells". Adaptive cells fired less after a 2-s prepulse (a slower component) | culture | [Zhao & Wu 1997](https://pmc.ncbi.nlm.nih.gov/articles/PMC6793766/) |

---

## 2. Intrinsic properties by cell type

| Type (MaleCNS) | Rin | τm | Vrest | Threshold / rheobase / f–I | Spontaneous / max rate | Prep | Source |
|---|---|---|---|---|---|---|---|
| Uniglomerular ALPNs | 598 ± 69 MΩ (n = 14); 459 ± 30 MΩ ex vivo; median 0.3 GΩ in Frechter's population | 17–31 ms (Rm·Cm of 3 DM1 fits, derived); uEPSP τ ~30 ms | "approximately −55 to −60 mV" with ORNs intact, "approximately −65 mV" without | ~10 mV above mean Vm | 1–5 Hz typical; 5 ± 0.7 Hz (0–17); 1.4 Hz. Max ~160 Hz over 500 ms (fig.); odor R_max 165 Hz | in vivo WC | [Gouwens & Wilson 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/); [Iniguez 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/); [Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/); [Kazama & Wilson 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/); [Wilson 2004](https://doi.org/10.1126/science.1090782); [Frechter 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/); [KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/); [Olsen 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/) |
| AL LNs (GH298), in vivo | "1-4 GΩ" | – | – | – | 2.3 ± 0.2 Hz; 4.6 ± 2.8 Hz | in vivo | [Wilson & Laurent 2005](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/); [Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/) |
| AL LN classes (Seki) | 0.74–1.24 GΩ | – | held −50 | threshold −22.2 to −39.1 mV | – | ex vivo | [Seki 2010](https://doi.org/10.1152/jn.00249.2010) |
| Dorsolateral AL LNs | 0.64 ± 0.02 GΩ; C 20.3 ± 2.1 pF | ≈13 ms (derived) | – | −52.5 mV (22 °C) | peak 105 Hz (22 °C) / 205 Hz (30 °C) | ex vivo | [Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/) |
| LH output neurons (group) | median 2.7 GΩ | – | – | – | 0.1 Hz ("10x quieter than PNs"); evoked 14 Hz | in vivo WC | [Frechter 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/) |
| LH local neurons (group) | median 4.6 GΩ | – | – | – | 1 Hz; evoked 14.3 Hz | in vivo WC | same |
| 14 LHN types (IV protocol; sub-agent's calc from [physplitdata](https://github.com/jefferislab/physplitdata)) | medians 2.5 (PV4a7) to 8.5 GΩ (PV5c3); AD1b1 4.0, AV6a1 3.8, PD2a2 2.8, PV5a1 3.1 | – | – | – | – | in vivo | same |
| LHPD2a1/b1 | 2.7 ± 0.5 GΩ | ~54 ms (derived with the authors' assumed 20 pF) | – | – | ~3 Hz; peaks ~40 sp/s (both fig.) | in vivo | [Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/) |
| LHPV5a1 | 4.1 ± 0.9 GΩ | ~51 ms (derived, assumed 12.5 pF) | – | – | "almost completely silent" | in vivo | same |
| DA1-recipient LHNs | – | – | – | ~10 mV to spike; dynamic threshold (−20% at onset) | below PNs | in vivo | [Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/) |
| KC αβ core (KCab-c) / α′β′ | ≈11.6 / 6.8 GΩ | ≈188 / 118 ms | ≈−46 / −46 mV | ≈−38.5 / −51.5 mV; αβc gap "8.2 mV" (text); αβc sigmoidal f–I ~25 Hz at 5 pA, α′β′ ~linear ~3 Hz/pA | αβc "quiescence"; α′β′ often spontaneously active | in vivo, 21–23 °C, LJP corrected (≈ values fig.) | [Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/) |
| KC αβ / α′β′ / γ | ≈12 / 8 / 8 GΩ (text "∼8–11 GΩ") | ≈185 / 130 / 125 ms | ≈−65 / −55 / −61 mV | ≈−33 / −46 / −22 mV (ramp); ~20 Hz at 5 pA (αβ), ~2.5 Hz/pA (α′β′), ~15 Hz at 12 pA (γ) | – | ex vivo, LJP corrected (all fig.) | [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/) |
| KCs, all (Turner) | ">10 GΩ" | ">200 ms" | held −58 ± 2 mV | gap 21.5 ± 5.6 mV (n = 17) | 0.1 ± 0.4 Hz; α′β′ highest (≈0.25–0.3 Hz, fig.) | in vivo | [Turner 2008](https://doi.org/10.1152/jn.01283.2007) |
| KC γ (other labs) | ≈1.5 GΩ (a 10× lab discrepancy; C 14.7 ± 4.4 pF agrees with the τ/R-derived ~15–17 pF) | – | – | onset ~30–40 pA; ~100 Hz peak at 100 pA | – | in vivo, 25 °C | [Greenin-Whitehead 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12487611/); ex vivo 1.0 GΩ, −60.9 mV, silent: [Gu & O'Dowd 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC6674319/) |
| MBON14 (α3) | Rm 926 ± 55 MΩ | 16.06 ± 2.3 ms; C 16.76 ± 1.9 pF | −56.7 ± 2.0 mV | – | 12.1 Hz | ex vivo, RT, n = 5 | [Hafez 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10069864/) |
| MBON11 / MBON18 / MBON06 | – | – | – | – | ≈3–8 / 1.5–3 / 3–10 Hz whole-cell (fig.); MBON11 37.2 ± 2.0 Hz by voltage imaging on a trackball | in vivo | [Vrontou 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/); [Huang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525173/) |
| PPL1 DANs | – | – | – | – | ≈0.5–2.5 Hz (fig.) | in vivo | [Vrontou 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/) |
| APL | ~120 MΩ | – | – | non-spiking, graded | – | ex vivo | [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/) |
| PEN (P-EN) | 1.9 ± 0.8 GΩ | – | per cell −42 to −57 mV (uncorr.) | per cell −25 to −41 mV | 3.9 ± 2.6 Hz standing (loose patch); max 31–80 Hz in 50-ms windows | in vivo | [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) (Supp. file 1) |
| PFNm/p, PFNa, PFNd, PFNv, PEN_a, PEN_b, PFL-class, PFR-class, EPG | 6.21, 4.86, 2.58, 6.00, 2.52, 3.30, 2.75, 7.89, 2.30 GΩ | – | −18 to −40 mV (uncorr., seal-shunted) | – | – | in vivo | [Currier 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793622/) (Table 1) |
| PFL3 | – | – | – | softplus rate vs Vm | spike detection capped at 200 Hz, and "the activity levels of all our cells stayed well below this upper limit" | in vivo | [Mussells Pires 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10881393/) |
| ER1 / ER3a / WL-L | – | – | – | – | 4.5 ± 1.7 / 5.2 ± 2.7 / 31 ± 12.6 Hz | in vivo | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| ExR2 (PPM3) | – | – | – | – | 0.02–0.52 Hz (5 cells) | in vivo | [Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/) |
| l-LNv | 2.59 GΩ (MESOR); C 33.7 pF, so τ ≈ 87 ms (derived) | – | −54.4 mV (LJP corrected) | rheobase 25.3 pA; gain 0.62 Hz/pA; 22.2 Hz at +30 pA | 0.86 Hz | ex vivo, n ≈ 250 | [Buhl 2026 PP](https://doi.org/10.64898/2026.02.04.703843) |
| l-LNv (older) | 305 ± 30 MΩ, 12 ± 2 pF (n = 4, voltage clamp at break-in) | – | −49 ± 1 mV (tonic) | – | 1.57 ± 0.24 Hz tonic; 3.24 ± 0.89 Hz bursting | ex vivo, 24 °C | [Sheeba 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2692874/) |
| IPCs | 1126 ± 67 MΩ; C 3.5 ± 0.7 pF | ~4 ms (derived) | −62 ± 4 mV | threshold −36 ± 1.4 mV | – | ex vivo, RT | [Kréneisz 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3075590/) |
| OA descending (VUMd) | 0.4–1.5 GΩ (inclusion range) | – | – | – | 4.12 ± 3.12 Hz, ISI CV 0.43, tonic | in vivo | [Babski 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064449/) |
| Giant fibre (DNp01) | "50 to 100 MΩ" (cited) | ≈1.6 ms (passive fit, derived) **[PP]** | fit E_rev −66.6 mV | – | ~1 spike per escape | in vivo | [Jang 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10263144/); [Moreno-Sanchez 2024 PP](https://doi.org/10.1101/2024.04.24.591016) |
| DNp03 | 281 ± 64 MΩ (SD) | ≈2.5 ms (fit) **[PP]** | < −50 mV (criterion) | – | – | in vivo | [Croke 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12977095/) |
| DNp07 / DNp10 | – | – | – | DNp07 spikes at 50 pA; DNp10 not drivable | 0.017 / 0.003 Hz at rest; >50 Hz visual in flight | in vivo, 22 °C | [Ache 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/) |
| DNOVS2 / DNHS1 | – | – | −40.9 / −43.1 mV (LJP corrected) | 8.2–8.8 / 3.9–5.9 Hz per mV | – | in vivo, 20 °C | [Suver 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5125229/) |
| DNa02 | – | – | – | – | stride modulation "only about 15 spikes/sec (approximately 10% of the cell's dynamic range)" | in vivo | [Yang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12778575/) |
| Tibia flexor MNs fast / intermediate / slow | 150 / 300 / 700 MΩ | – | −68 / −60 / −48 mV | fast and intermediate not reliably drivable | slow ≈30 Hz at rest; others silent | in vivo, RT | [Azevedo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7347388/) |
| MN5 (DLM) | 97 ± 31 MΩ; 127 ± 16 pF | ≈12 ms (derived) | −67.8 ± 5.5 mV | – | 4–20 Hz in flight | in situ | [Herrera-Valdez 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC6595220/); [Ryglewski 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4433752/) |
| Larval MNs (aCC, RP2, RP3, MNSNb/d-Is) | 496–1091 MΩ; 14–32 pF | 7–26 ms (derived) | −47 to −51 mV | somatic threshold −16 to −24 mV; rheobase ~45–70 pA (fig.) | bursts 90–110 Hz, >120 max | ex vivo | [Schaefer 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2944697/); [Kadas 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC8130532/) |
| HS cells (LPTC) | 205 ± 45 MΩ | 4.9 ms | – | – | graded | in vivo | [Cuntz 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3747245/) |
| B1 (AMMC) | 0.52 GΩ (leak) | – | −51 mV | graded, rest in depolarization block | 0 | in vivo | [Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/) |
| APN3 / WPN | – | – | ~−55 mV (APN3) | – | 28.6 / 8.4 Hz | in vivo | [Chang 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5749228/); [Suver 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6533146/) |

Notes on this table:
- Measured τm spans ~2 ms (large DNs, passive fits), 12–31 ms (MN5, PNs, larval MNs, MBON14) and 120–200 ms (KCs).
- A uniform 20 ms is about right for PNs and MNs, ~10× too long for large DNs and 6–10× too short for KCs. Per-type θ (equivalently, input gain) captures much of the difference in a current-based LIF; KCs may also need their own τm.

---

## 3. Mechanisms and time constants

| Mechanism | Effect and time course | Where shown | Source |
|---|---|---|---|
| **Na⁺/K⁺-ATPase current** | Ultraslow, spike-count-proportional AHP. Larval MNs: ~20 mV after 5 s, 15–20 s recovery, no conductance change. LH neuron: divisive gain ×~0.6, kernel >3 s. DN1p: NaKβ speeds spike onset (a different role) | larval MNs; LHPD2a1/b1 (in vivo); DN1p | [Pulver & Griffith 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2839136/); [Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/); [Tabuchi 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6239908/) |
| HCN (Ih) | Spike-count memory over 100–600 ms in MN5 **[PP]**; l-LNv sag ~5.1 mV at −30 pA **[PP]**; Ih mutant bursts less (26.2 vs 17.5 bursts/min) | flight MNs; l-LNv | [Huthmacher 2025 PP](https://doi.org/10.1101/2025.06.16.659928); [Buhl 2026 PP](https://doi.org/10.64898/2026.02.04.703843); [Fernandez-Chiappe 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7842748/) |
| BK / slowpoke, K_Ca | Fast AHP that supports high rates (larval MNs); night-time K_Ca rise deepens the DN1p AHP; PI-neuron AHP K_Ca-dependent but not SK; removing Ca²⁺ shrinks the aCC/RP2 AHP and raises firing | larval MNs; DN1p; PI | [Kadas 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC8130532/); [Tabuchi 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6239908/); [Chong 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11906214/); [Worrell & Levine 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2525733/) |
| SK | Slow AHP, τ 491 ± 72 ms, in non-spiking APL (grows with sleep loss); photoreceptors. **No SK-mediated mAHP found in a spiking central neuron** | APL; retina | [Chen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/); [Abou Tayoun 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3758547/) |
| Shal / Kv4 (I_A) | First-spike delay; needed for sustained repetitive firing (without it cultured neurons fall into a Na⁺-inactivated "adapted, non-excitable state"). Inactivation τ: KC αβc 37.2 ms; dFB 7.5 ms; l-LNv τ_fast 2.7–3.2 / τ_slow 31.6–34.9 ms **[PP]** | culture; KCs; dFB; l-LNv | [Ping 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3022017/); [Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/); [Pimentel 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/); [Buhl 2026 PP](https://doi.org/10.64898/2026.02.04.703843) |
| Sustained I_K (TEA-sensitive; Shab) | Dominant in adaptive cultured neurons (I_K/I_A > 2); Shab sustains firing over hundreds of ms (abstract) | culture | [Zhao & Wu 1997](https://pmc.ncbi.nlm.nih.gov/articles/PMC6793766/); [Peng & Wu 2007](https://doi.org/10.1152/jn.01012.2006) |
| T-type Ca (α1T) | Limits PN burst length; ~200-ms Ca spikes in PFNa | PNs; PFNa | [Iniguez 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/); [Ishida 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12758628/) |
| Na⁺ inactivation / depolarization block | Spikes shrink at high rates (LHN type I); B1 rests in block; LNs of para GEFS+/DS knock-ins go into depolarization block at 30–35 °C and the flies seize | LHN; B1; LNs | [Fişek & Wilson 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3992254/); [Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/); [Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/) |
| K2P leak (Sandman) | Switches dFB neurons OFF for tens of minutes (τ_switch ~1 min) | dFB | [Pimentel 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/) |
| Persistent Na⁺ | 4.1–9.5% of transient I_Na in larval aCC; pro-excitatory | larval MNs | [Lin 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2746785/) |

**No Drosophila central neuron has a measured adaptation-current time constant in the 50–500 ms range.**
- The fast τ1 ≈ 200 ms is supported only indirectly: the MN5 memory window of 100–600 ms [PP]; LN adaptation seen between 0.5 and 1 s windows; the pIP10 decline over ~0.3–0.5 s in one trial; and the slower component seen in cultured adaptive cells.
- flybench and the Nawrot-lab models use similar values (§4).

---

## 4. How other fly network models handled adaptation and runaway

| Model | Neuron / adaptation | Runaway handling | Values | Source |
|---|---|---|---|---|
| Shiu et al. 2024 (FlyWire LIF) | LIF, **no adaptation** | None active: basal rate 0, no background, feed-forward tests at 10–200 Hz input; "absolute firing rate predictions are unlikely to be accurate". The code reset `'v = v_rst; w = 0; g = 0 * mV'` zeroes the synaptic variable at each spike (I confirmed in Brian2 2.10.1; `w = 0` is a no-op temporary) | V_rest = V_reset −52, V_th −45 mV; R_m 10 kΩ·cm² × C_m 2 µF/cm² = 20 ms; t_ref 2.2 ms; τ_syn 5 ms; delay 1.8 ms; w_syn 0.275 mV | [PMC11446845](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/); [model.py](https://github.com/philshiu/Drosophila_brain_model/blob/main/model.py) |
| Kakaria & de Bivort 2017 (60-cell PB–EB LIF) | No adaptation current, but each spike is a 2-ms template ending at a **−72 mV undershoot** (20 mV below rest; cited to Nagel et al. 2015) from which integration resumes | The undershoot is a reset below rest. Shiu cites Kakaria for V_reset −52 mV, but Kakaria's post-spike voltage was −72 mV | C_m 0.002 µF (10⁻³ cm²), R_m 10 MΩ, V0 −52, V_th −45 mV; PSC 5 nA, 5-ms half-life; 5 Hz background Poisson into E-PGs | [PMC5306390](https://pmc.ncbi.nlm.nih.gov/articles/PMC5306390/) |
| Pospisil et al. 2024 (effectome) | **Not LIF**: linear VAR(1) with the signed connectome as prior | W "scaled for stability" (circuit sims: max eigenvalue 1, τ 0.5 ms, rectification); edges < 5 synapses zeroed. Top olfactory eigencircuits localize to the MB and to AL→LH PNs; non-localized ones span AL, LH and LAL | ACh/DA +; GABA/Glu/5-HT/OA − | [PMC11446844](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446844/) |
| Lappalainen et al. 2024 (flyvis) | Graded threshold-linear, no adaptation | Trained; per-type τ (initialized at 50 ms, clamped ≥ dt) and V_rest | 734 parameters | [PMC11525180](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/) |
| Pugliese et al. 2025/26 **[PP]** (VNC rate model) | Rate, no adaptation | Rectified-tanh saturation; gain and threshold normalized by neuron size; one scale per transmitter (b_ACh 0.03: "Increasing b_ACh to 0.045 still produced viable oscillatory dynamics, but larger deviations resulted in either runaway network activity or insufficient neuron recruitment"); input auto-tuned; runs with >1,500 recruited neurons discarded as "oversaturated … generally unstable". Rhythm from an E-E-I motif with delayed inhibition | τ ~ N(20, 2) ms; r_max ~ N(200, 10) Hz; θ ~ N(7.5, 0.6); gain ~ N(1, 0.1). LIF check with Shiu constants, 0.15 nA input, dt 0.01 ms | [PMC13142387](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/) |
| Eon Systems 2026 [unreviewed] | Shiu LIF, no adaptation | PyTorch port keeps the g-reset at spike | Shiu constants | [run_pytorch.py](https://github.com/eonsystemspbc/fly-brain/blob/main/code/run_pytorch.py) |
| Wang et al. 2026 Nat Commun (FlyWire LIF fit to Turner 2021) | Shiu LIF, no adaptation (ALIF only in their ML benchmarks) | Trains all weight magnitudes (signs fixed); a GRU encoder turns last step's neuropil rates into Poisson drive; lists "homeostatic rules" as future work | Shiu constants | [PMC12913608](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913608/) |
| Li, Ping, Zhang & Wang 2026 **[PP]** | Rate (ReLU), Δt = 1/1.2 s, no adaptation or clipping | Trains weights, per-neuron τ and global noise. Rest is held by sparse inhibitory hubs (MBON06, LPi13, LPi15 …): "Silencing one inhibitory hub releases its excitatory partner into runaway activity" | – | [bioRxiv](https://doi.org/10.64898/2026.08.21.745055) |
| Su et al. 2017 (EB–PB conductance LIF) | No adaptation; NMDA synapses | Reset 20 mV below threshold (at rest); bump needs NMDA τ ≳ 50 ms | C_m 0.01 nF (ring) / 0.1 nF; τ_m 15 ms; V_L −70, V_th −50, V_reset −70 mV | [PMC5529380](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/) |
| flybench adaptive LIF (hobby) | Shiu LIF plus subtractive a (flybench's form): a += **2 mV** per spike, **τ_a 200 ms** (k = 0.4), global | FlyWire 783 at 0.45× gain, vs the reference: MN9 1.0–1.3 s after sugar 354 → 0 Hz; network 10.9 → 0 Hz; active fraction 7.7% → 0; MN9 during sugar ~400 → 53 Hz; PN ceiling 434 → 233 Hz. Still fails the single GF spike (129 → 116 spikes) and two-pulse habituation with a 300-ms gap | b 2 mV, τ 200 ms | [adaptive_lif.py](https://github.com/brandoncho369/flybench/blob/master/flybench/models/adaptive_lif.py); [adaptive](https://github.com/brandoncho369/flybench/blob/master/results/adaptive-lif-b-2-mv-tau-200-ms.json) vs [reference](https://github.com/brandoncho369/flybench/blob/master/results/flywire783_gain0.45.json) |
| kazemi-mahdi/fly-escape-circuit (hobby; MaleCNS v1.0, Shiu LIF) | SFA of +0.5 / 1 / 2 mV per spike at τ 100 ms (k ≤ 0.2) | Ignition threshold 0.8–0.9× published w_syn; 120 cholinergic-labelled AL LNs carry two thirds of the self-sustained state. SFA did not stop it (9/9, 9/9, 6/9 at 0.7×; 4/4 at 1.0×; mean rate 3.9 → 1.23 Hz at 2 mV). STD of 5–10% per spike with 200-ms recovery stopped all (10% also at 1.0×) but cut reflex output (TTMn 2.33 → 0.67 spikes per loom) | – | [STABILITY.md](https://github.com/kazemi-mahdi/fly-escape-circuit/blob/main/STABILITY.md) |
| Nanami et al. 2024 (data-driven AL–MB spiking network) | Piecewise-quadratic models fitted to current steps from PNs and MBON07 (new), KCs (Inada data) and 4 LN classes (Seki data); abstract units | PN model carries a slow rate-homeostasis term du/dt = κ(F_target − F)/τ, a synaptic-scaling analogy | – | [PMC11238178](https://pmc.ncbi.nlm.nih.gov/articles/PMC11238178/) |
| Betkiewicz, Lindner & Nawrot 2020 | Current-based SFA in all neurons | ΔI_A 0.132 nA (≈4.6 mV per spike at g_L 28.95 nS), τ_A 389 ms, so k ≈ 1.8 mV/Hz against a 13-mV threshold gap. Basis: cockroach and bee KC SFA **[other insect]** | C 289.5 pF; E_L = V_R −70, V_T −57 mV; τ_ref 5 ms | [PMC7294456](https://pmc.ncbi.nlm.nih.gov/articles/PMC7294456/) |
| Rapp & Nawrot 2020 | Conductance SFA in KCs only (from their code) | b_KC 5 nS per spike, τ 50 ms, E −90 mV (≈5.7 mV per spike, sub-agent's calc); ORNs 2 nS at 1 s | – | [PMC7668073](https://pmc.ncbi.nlm.nih.gov/articles/PMC7668073/) |
| Jürgensen et al. 2021 / 2024 (larva) | KC SFA 0.05 / 0.02 nS at τ 1 s (from code); authors: "It remains an open question whether the SFA mechanism is at all present in the KCs during larval stages" (via summary) | – | – | [2021](https://doi.org/10.1088/2634-4386/ac3ba6); [PMC10824792](https://pmc.ncbi.nlm.nih.gov/articles/PMC10824792/) |
| Kennedy 2019 **[PP]** | No KC SFA; LIF τ 10 ms; a "homeostatic" variant sets per-KC thresholds | – | – | [bioRxiv](https://doi.org/10.1101/783191) |
| Roemschied 2023 / Steinfath 2025 (song circuit rate models) | Steinfath's model gives both song DNs adaptation "supported by the observation of spike-frequency adaptation in patch clamp recordings of pIP10" | – | – | [PMC10600009](https://pmc.ncbi.nlm.nih.gov/articles/PMC10600009/); [PMC12559195](https://pmc.ncbi.nlm.nih.gov/articles/PMC12559195/) |

Not checked for adaptation: Xi & Chen 2025 **[PP]** (FlyWire, Shiu-type; bioRxiv rate-limited); Liew et al. NeurIPS 2025; Sandia Loihi port (parity only).

---

## 5. Homeostasis and intrinsic plasticity

| Study | Perturbation → compensation (magnitude) | Time scale | Set point restored? | Adult central? | Source |
|---|---|---|---|---|---|
| Kulik 2019 | Chronic Shal RNAi in MN1-Ib: f–I unchanged (~100 Hz at 200 pA) vs acute 4-AP (higher rates, depolarization block); I_KCa and I_KDR rise | days | yes (evoked f–I) | no (larval MN) | [PMC6491091](https://pmc.ncbi.nlm.nih.gov/articles/PMC6491091/) |
| Baines 2001; Baines 2003; Mee 2004 | Synaptic block raises I_Na, I_Kfast and I_Kslow (e.g. I_Na 39 vs 30 pA/pF); more drive lowers I_Na 24–38% via PKA; para mRNA ×2.5–3.9 in opposite directions (Pumilio). Kir2.1 spike suppression had no effect: cells "do not use the number of action potentials" | embryo / L1 | direction homeostatic | no | [PMC6762927](https://pmc.ncbi.nlm.nih.gov/articles/PMC6762927/); [PMC6740429](https://pmc.ncbi.nlm.nih.gov/articles/PMC6740429/); [PMC6729971](https://pmc.ncbi.nlm.nih.gov/articles/PMC6729971/) |
| Bergquist 2010; Parrish 2014 | shal null raises shaker mRNA to 252 ± 31%; Krüppel induced 18–24 h after Shal loss, driving Shaker and slo | ~1 day to chronic | not measured | no | [PMC2864777](https://pmc.ncbi.nlm.nih.gov/articles/PMC2864777/); [PMC4104505](https://pmc.ncbi.nlm.nih.gov/articles/PMC4104505/) |
| Peng & Wu 2007 | cac loss or Ca²⁺-channel block: I_A rises to match the I_K(Ca) loss (total K⁺ conserved); "days instead of minutes" | days | total current conserved | culture | [PMC6673189](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673189/) |
| Ping & Tsunoda 2012 | 24 h curare: Dα7 nAChR up >60% and Shal ~+80%, stabilizing EPSPs; nothing at ≤12 h | ~24 h | EPSPs (not rates) | brain explants | [PMC3888491](https://pmc.ncbi.nlm.nih.gov/articles/PMC3888491/) |
| Apostolopoulou & Lin 2020 | 4 days of excess APL activity: KC odor Ca²⁺ ×1.3–2.6 (fig.); not significant at 1 day; gone 1–2 days after stopping; APL block gives no compensation | days | partial | yes (MB) | [PMC7368247](https://pmc.ncbi.nlm.nih.gov/articles/PMC7368247/) |
| Greenin-Whitehead 2025 | NaChBac in KCs suppresses spiking and lowers endogenous Para at the spike-initiation zone; Ca²⁺ normal only after 4 days of adult expression | ~4 days | partial | yes | [PMC12487611](https://pmc.ncbi.nlm.nih.gov/articles/PMC12487611/) |
| Bergmann 2026 | 24 h KC activation: "KCs compensate … by reducing excitation, yet this change is opposed by reduced inhibition from APL" | 24 h | no net | yes | [PMC13039246](https://pmc.ncbi.nlm.nih.gov/articles/PMC13039246/) |
| Abdelrahman, Vasilaki & Lin 2021 | Hemibrain: "≈6−15% fewer input synapses per PN–KC connection for each additional PN per KC". Thresholds "cannot be measured in the connectome" (no physiology) | – | anatomical correlation | yes | [PMC8670477](https://pmc.ncbi.nlm.nih.gov/articles/PMC8670477/) |
| Kazama & Wilson 2008 | ORN→PN unitary current matched to PN size (homeostatic matching; synaptic) | developmental | – | yes | [PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/) |
| Pimentel 2016; Donlea 2014 | Sleep pressure switches dFB neurons ON (high Rin, spiking) or OFF (Sandman leak) | ~1 min switch; states last 7–60 min | state switch | yes | [PMC4998959](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/); [PMC3969244](https://pmc.ncbi.nlm.nih.gov/articles/PMC3969244/) |
| Liu 2016; Ho 2022 | ER5 firing ~3× higher at ZT13–15 and after sleep deprivation; EPG ~2× after SD, attributed to "changes in extrinsic input, rather than intrinsic excitability" | hours | – | yes | [PMC4892967](https://pmc.ncbi.nlm.nih.gov/articles/PMC4892967/); [PMC9691613](https://pmc.ncbi.nlm.nih.gov/articles/PMC9691613/) |
| Lin 2012; Coulson 2025 **[PP]** | **Anti-homeostatic:** picrotoxin feeding raises persistent I_Na; embryonic critical-period excitation raises excitability in interneurons A27h/A31k for ~5 days (aCC unchanged) | chronic | no | no | [PMC3400946](https://pmc.ncbi.nlm.nih.gov/articles/PMC3400946/); [bioRxiv](https://doi.org/10.64898/2025.12.01.691172) |

---

## 6. Derivations and toy simulations (mine, not literature)

Constants throughout: Shiu's (τ_m 20 ms, θ 7 mV above rest, reset at rest, t_ref 2.2 ms, τ_syn 5 ms, dt 0.1 ms). Scripts are in the session scratchpad (`sfa/lif_adapt.py`, `loop_sim.py`, `loop_mech.py`), not in the repo.

**f–I of the Shiu LIF** (Siegert formula, free-Vm noise SD 1–4 mV):
- G = 1–6 Hz/mV at 1–5 Hz; 4–7.5 at 10–50 Hz; 4.2–4.4 at 100 Hz; 2.2 at 200 Hz.
- Deterministic drive needed: 7.05 mV for 10 Hz, 11.9 for 50, 21.7 for 100, 53.6 for 200.

**Single neuron with adaptation**, 50 Hz and 100 Hz steps, 3-s runs:
- A ≈ 1/(1 + 5k) holds within a few percent. Examples: k = 0.05 → A 0.80–0.86; 0.1 → 0.64–0.68; 0.2 → 0.45–0.49; 0.4 → 0.29–0.32; 0.8 → 0.18–0.19.
- The steady state depends on k = b·τ, not on b or τ separately.

**Resets and refractory** (deterministic):

| Setting | Drive for 10 / 50 / 100 / 150 Hz (mV) | Ignition threshold at bias 0 / 2 / 4 mV (mV/Hz, at rate) |
|---|---|---|
| reset at rest | 7.1 / 11.9 / 21.7 / 35.0 | 0.217 @100 Hz / 0.192 @80 / 0.157 @40 |
| reset −5 mV | 7.1 / 15.4 / 32.2 / 55.0 | 0.305 @60 / 0.266 @40 / 0.207 @30 |
| reset −10 mV | 7.1 / 18.8 / 42.6 / 74.9 | 0.375 @40 / 0.318 @30 / 0.236 @20 |
| reset −20 mV (Kakaria) | 7.2 / 25.8 / 63.6 / 114.9 | 0.474 @30 / 0.386 @20 / 0.275 @15 |
| t_ref 4 ms / 6 ms | 100 Hz needs 27.0 / 38.6 mV | caps at 250 / 167 Hz |

**Toy loop:** 200 all-to-all excitatory Shiu cells, noise SD 2 mV, 100-ms kick, population rate in Hz.

| Setting | J = 0.25 mV/Hz | J = 0.40 mV/Hz |
|---|---|---|
| no bias, no adaptation | sustained 175 | sustained 287 |
| no bias, k = 0.1 (b 0.5 mV @ 200 ms) | back to 0.1 | sustained 229 |
| no bias, k = 0.2 | back to 0.1 | back to 0.1 |
| bias 3 mV (rest ≈ 5–7 Hz), no adaptation | ignites unprompted, ~195 | ~295 |
| bias 3 mV, k = 0.1 @ 200 ms | **bursts** (~150 Hz, every ~0.8 s) | sustained ~240 |
| bias 3 mV, k = 0.2 @ 200 ms | stable ~5 | bursts every ~1 s |
| bias 3 mV, slow k = 0.2 @ 2 s | runs ~0.5 s, then silent, slow recovery | runs ~2 s, then silent |
| bias 3 mV, fast 0.1 + slow 0.2 | off, recovers to 1–4 over seconds | off after ~0.5 s |
| bias 3 mV, STD f 0.78, τ_rec 0.9 s | stable 5–8 | stable ~9 |
| bias 3 mV, reset −20 mV | stable ~12 | stable ~38 |
| bias 3 mV, reset −20 mV + k = 0.1 | ~6 | ~18, irregular |

Take-aways:
- Adaptation shifts the ignition threshold by about k.
- Supercritical loops with bias burst rather than rest.
- A reset below rest caps rates without adding slow dynamics.
- STD gave the most robust low-rate rest.
- These are homogeneous toy loops. The MaleCNS loops are heterogeneous, so re-measure J (or the local spectral radius) for the LH/SLP/AL-LN sets that ignite.

---

## 7. Gaps and caveats
- **No Drosophila adaptation-current time constant** in the 50–500 ms range has been measured in any central neuron, and there is no SFA index for KCs, MBONs, LHNs (fast), CX neurons, PAM/DPM or SLP neurons.
- In vivo LN current-step adaptation, LN/LHN membrane τ, and PN/LN f–I slopes are missing.
- **Lab-to-lab discrepancies:**
  - KC Rin (8–12 GΩ vs 1–1.5 GΩ); matching capacitance points to shunted recordings in the low group.
  - l-LNv Rin (305 MΩ at break-in vs 2.59 GΩ).
  - MBON11 rate (3–8 Hz whole-cell vs 37 Hz by voltage imaging).
- **Temperature matters.** LN first/final-ISI ratio goes from 0.49 to 0.27 and peak rate from 105 to 205 Hz between 22 and 30 °C ([Roemmich 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454921/)). Most data are at 20–25 °C.
- **Rates depend on state.** Flight, walking and octopamine raise DN baselines ([Ache 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/); [Suver 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5125229/)).
- **The pump term is measured in only two cell classes** (larval MNs; one LH type). Its per-spike size in other adult central neurons is an extrapolation.
- **Sub-agent coverage.** One sub-agent's report (CX / sleep / clock) was cut off. I rebuilt its missing parts (DN1p, PI neurons, IPCs, persistent activity) from its downloaded texts. P1/pC1 intrinsic data were not recovered.
- **Persistent states are real in some fly circuits:**
  - pC1d/e drive "minutes-long" persistent activity through recurrent pC1–aIPg connectivity ([Deutsch 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7787663/)).
  - The EPG bump persists in darkness ([Seelig & Jayaraman 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/)).
  - Target rates for these circuits should not be forced to zero. None of these states involves sustained >100 Hz firing.
