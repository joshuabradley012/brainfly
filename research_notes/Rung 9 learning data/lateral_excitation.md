# Lateral excitation in the fly antennal lobe, measured: eLNs, electrical coupling, strengths, effects on PN responses

Compiled 2026-10-10 from full texts, figure legends, supplements and high-resolution figures. Purpose: give brainfly
measured strengths for adding lateral excitation (eLN→PN electrical coupling) and published measurements to test it
against. Tags: (stated) or quotation marks = from the text; (fig., approx.) = read off a figure; (derived) = my arithmetic.

## Summary: numbers most useful for modeling

In one line: eLNs couple to PNs electrically, weakly per pair and broadly; one eLN spike moves a PN soma by ≈0.4 mV;
lateral excitation of a PN with no ORN input is a few mV and saturates at low input; in intact flies it is usually
outweighed by lateral inhibition, and broad PN tuning does not depend on it.

**Coupling strength (eLN → PN)**
1. One eLN spike → PN soma: **0.42 mV** mean spike-triggered-average peak (median 0.36, range 0.16-0.72; n = 12 pairs;
   explant; Huang 2010 Fig. 3K, fig., approx.). About 60% of that peak arrives before the spike (subthreshold coupling
   during the current step that evoked it), so the spike-locked part is ≈0.17 mV. Decay τ ≈ 30 ms; area ≈ 21 mV·ms
   (derived).
2. A 100-ms eLN burst of 4-6 spikes → **0.93 mV** in the PN (mean of 35 pairs, range 0.27-2.2; one eLN gave 0.37-1.83 mV
   in five PNs; Huang Fig. 2, stated "about 0.9 mV").
3. Coupling coefficients eLN → PN, depolarizing / hyperpolarizing: **0.0087 / 0.0024** in vivo (n = 37; Yaksi & Wilson
   2010); 0.0073 / 0.0021 (n = 36; Kazama, Yaksi & Wilson 2011); 0.015 / 0.007 subthreshold in explant (n = 12; Huang).
   Abolished in shakB²; not reduced by Cd²⁺, mecamylamine or D-tubocurarine; α-bungarotoxin −34% (n.s.) to −38%.
4. For brainfly's instantaneous kick (PN τm = 20 ms; derived, §8): **gw ≈ 0.17 mV** (spike-locked part only) **to ≈1 mV**
   (same charge per spike as the STA); ≈0.4 mV matches the STA peak. Check: 10 eLNs × 8 Hz (Kazama 2011's acute eLN odor
   rates) × 21 mV·ms ≈ 1.7 mV, inside the 1.4-3.1 mV measured in that preparation. Coupling more cells needs a smaller gw
   (≈0.4 mV for 30 per side, ≈0.2 mV for 68).
5. Other electrical links: PN → eLN 0.018 depolarizing (≈85% of it nicotinic, i.e. chemical) with an electrical part of
   0.004-0.010 and an STA of 0.21 mV; eLN ↔ eLN 0.025-0.027, STA ≈0.73 mV; sister PNs 0.018 / 0.0077 (DA1) and 0.035 /
   0.0136 (DM6, Cd²⁺-resistant part ≈0.011-0.016); heterotypic PN pairs < 0.003; eLN → iLN 0.012-0.017, mostly
   cholinergic. Lateral EPSCs start ≈1.5 ms after direct ones.

**PN responses without their own ORNs**
6. Silent receptor mutants (ORNs alive; lateral input normal per Kazama 2011): VM2 PNs **6-32 spikes/s** (mean 16.7) and
   DL1 PNs **5-26** (mean 13.2) over a 500-ms odor, for all 13 odors (means); wild type 21-118 (72.8) and 2-117 (34.2). Lateral
   tuning is uncorrelated with normal tuning (r² < 0.05) (Olsen 2007 Fig. 4, fig., approx.).
7. Acute deafferentation, depolarization with spikes filtered: **6.3-7.5 mV** peak (antennal PNs, palp odors; Olsen);
   **2.4-3.3 mV** mean over 100-300 ms, peaks 3.7-4.9 mV (VC1/VC2; Yaksi); 1.4-5.1 mV (Kazama 2011); 5.7-6.2 mV
   (DA1/VA5-lineage PNs, ≈0.5-0.8 mV in shakB²; Shimizu & Stopfer 2017); 0.1-1.1 mV in DM1. Chronic ablation inflates it
   2-6× (Kazama 2011), so avoid chronically deafferented data as targets.
8. Input dependence: half-maximal at **≈7-10 spikes/s** from one ORN type and flat from 50 to 150 spikes/s; plateau mean
   ≈3.8 mV (VA7l input) or ≈1.8 mV (VM7) over 100-600 ms; two ORN types give 68% of the linear sum; per-glomerulus scale
   varies 2.4-fold and is stereotyped (Olsen 2007). Five odors spanning a ≥7-fold range of total ORN activity gave equal
   lateral excitation (Yaksi).
9. Time course: peak 120-300 ms after valve opening, held at 60-90% of peak to odor offset (VC1/VC2), then a ≈1-3 mV
   undershoot.

**Contribution to PN responses and breadth**
10. Removing electrical synapses in intact flies (shakB²; Yaksi; PSTH means over 100-600 ms): VC1 **−28 / −45 / −52%** for
    fenchone 10^-2 / 10^-4 / 10^-6 (172 → 124, 124 → 68, 42 → 20 spikes/s; the 10^-6 change n.s.), mean −34% over the 6
    significant stimuli. VC2: two lateral-only responses (51 and 77 spikes/s) abolished, but own-ligand responses up to 2×
    larger (eLN-driven inhibition lost). DA1 cVA −29 to −42% (sister-PN coupling). DM1 unchanged.
11. Net sign: in intact flies the net effect of lateral input on PN spiking is usually inhibitory. Removing the antennae
    raised 18/20 (VM7) and 13/20 (VC1) palp-PN odor responses and lowered none (Olsen & Wilson 2008); "the net effect of
    lateral input was always inhibitory" (Olsen 2010).
12. Breadth: PN tuning stayed broad, and got broader, without lateral input (lifetime sparseness VM7 0.47 → 0.26; Olsen &
    Wilson 2008); "lateral excitation is not strictly necessary to explain the basic phenomenon of broad PN tuning" (Wilson
    2013). Purely lateral PN responses in intact flies do occur (VC2 above; DM2 output 32-93% of wild type with its ORNs
    silenced, Shang 2007) but were near zero in Olsen 2010's tests and invisible to Ca²⁺ imaging in several glomeruli.
13. Identity: the physiological eLNs are few (2-3 or more recorded per lobe in krasavietz-Gal4; 2 ± 1 to ≈10 cholinergic
    krasavietz cells by staining) and broad. MaleCNS labels 137 ALLNs cholinergic (68-70 per side); lLN1_bc and lLN2T are
    the literature-matched types, but on morphology only. ShakB is the AL gap-junction protein; EM cannot see the
    junctions.

## Conventions and access

**Conventions** (as in the other notes)
- Text in quotation marks is verbatim.
- "(fig., approx.)" = read off a published figure with a pixel grid calibrated on its axes or scale bars. Expect ±3-5% of
  full scale; trace amplitudes carry ≈±0.1 mV extra from line width.
- "(derived)" = my arithmetic, shown or reproducible from the stated numbers.
- "Not reported" = searched the text, legends and supplement and did not find it.
- Coupling coefficient = ΔV(postsynaptic soma)/ΔV(presynaptic soma) during a current step. All are somatic and, per the
  authors, underestimate coupling at the junction.
- Times are from the odor-valve command unless stated.

**Access limits**
- Huang et al. 2010: cell.com and ScienceDirect return 403. The text was read from a 2022 Wayback capture and the figures
  from ars.els-cdn.com.
- No paper found reports a pharmacological gap-junction blocker (carbenoxolone etc.) in the fly AL. All evidence for
  electrical synapses is genetic (shakB²) or from paired recordings and dye coupling.
- Sections 5-7 were compiled by helper agents from the cited full texts; I spot-checked the key quotes and numbers I rely on
  in the summary.

Related notes: [pn_ln_dynamics.md](pn_ln_dynamics.md) (PN and LN intrinsic properties, the Huang 2010 Fig. S1 table),
[presynaptic_inhibition.md](presynaptic_inhibition.md), [orn_pn_depression.md](orn_pn_depression.md) (Kazama & Wilson 2008).

## 1. Olsen, Bhandawat & Wilson 2007, Neuron 54:89 ([PMC2048819](https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/))

**Setup.** In vivo whole-cell current clamp from PN somata, adult females 2-7 days old. One PN per fly, identified by a
biocytin fill. Odors 1:100 in paraffin oil, diluted a further 10-fold in air, 500-ms pulses, 6 trials per odor (VM7-only
odors were diluted further, 10^-2 to 10^-6). Recording temperature: not reported. Analysis:
- "Depolarization area was computed as the area under the zeroed membrane potential over a 500-ms window starting 100 ms
  after opening of the odor valve" (traces low-pass filtered at 13 Hz to remove spikes).
- Tuning curves (Fig. 4): "mean firing rate over the 500-ms odor presentation, minus the baseline firing rate".

**Headline statements (verbatim).**
- "PNs postsynaptic to the silent glomerulus receive substantial lateral excitatory input from other glomeruli."
- "The net effect of lateral synaptic inputs to PNs is predominantly excitatory and can be strong enough to trigger a train
  of action potentials."
- "Stimulation of just one ORN type is sufficient to recruit lateral excitatory inputs to other glomeruli, but this
  sensitivity also leads to saturation as more ORN types are activated."
- "every PN we recorded from (87 of 87 cells) received at least weak lateral input from that glomerulus."
- No mecamylamine or gap-junction-blocker experiments in this paper. The mechanism was unknown; the Discussion suggests
  Shang et al.'s cholinergic LNs as "plausible".

### 1.1 Antennal nerves cut, palp odors (Fig. 1)

- Antennal PNs lose all spontaneous activity after acute antennal-nerve section (stated; recordings 10-20 min after
  surgery), but palp odors depolarize them (n = 6 PNs in 6 flies, different antennal glomeruli; VC3 and DM3 shown).
  Removing palps too abolishes the response (n = 3). Paraffin oil: no response.
- Pooled depolarization (Fig. 1G, 6 trials per cell, spikes filtered, n = 6; fig., approx., 8-mV bar = 268 px):

  | odor (1:100) | peak (mV) | time of peak after valve | at odor end (500 ms) | after offset |
  |---|---|---|---|---|
  | ethyl butyrate | 7.3 | ≈125 ms | 3.9 mV | +0.5 to +1.0 mV tail |
  | 2-heptanone | 7.5 | ≈165 ms | 3.1 mV | −0.4 mV dip, then +0.4 mV |
  | benzaldehyde | 6.3 | ≈175 ms | 2.4 mV | −0.3 mV dip, then +0.5 mV |
  | paraffin oil | ≈0 | | | |

  - Onset ≈95 ms after valve opening (fig., approx.; olfactometer delay included).
  - Single trials: a VC3 PN fired a spike train (Fig. 1E, ≈12 spikes in 500 ms, fig., approx.); a DM3 PN depolarized by
    only ≈5 mV without spikes (Fig. 1D, fig., approx.).

### 1.2 PNs whose own ORNs lack a receptor: VM2 (Or43b¹) and DL1 (Or10a^f03694) (Figs. 2-4)

- Spontaneous activity, wild type vs mutant (Fig. 2B, mean, fig., approx.):
  - VM2 ORNs 7.1 (n = 14) vs 0.7 (n = 13) spikes/s; VM2 PNs 2.5 (n = 14) vs 0.3 (n = 10).
  - DL1 ORNs 17.3 (n = 10) vs 1.1 (n = 21); DL1 PNs 5.6 (n = 13) vs 0.2 (n = 10).
- "In flies with silent VM2 ORNs, all VM2 PNs were depolarized by every odor we tested (n=10 cells in 10 flies), with the
  exception of 4-methyl phenol, which failed to elicit any activity in two cells. These depolarizations were typically
  large enough to trigger a train of action potentials." Same for DL1 (n = 10 cells in 10 flies). Responses were also seen
  cell-attached before break-in.
- "in PNs postsynaptic to silent ORNs, odor-evoked responses were often more transient than in wild-type PNs."
- Odors that do not drive the PN's own ORNs give similar responses with or without them: 2,3-butanedione in VM2 is
  "virtually unaltered"; ethyl acetate in DL1 is "undiminished".
- Tuning with vs without own ORN input: "the odor tuning of wild type and mutant PNs showed no significant correlation (both
  comparisions Pearson's r^2<0.05, p>0.4)". The lateral tuning of VM2 and DL1 is correlated (r² = 0.31, p < 0.05), but
  butyric acid drives VM2 more than DL1 (p = 0.05, n = 6 each).
- Firing rates (Fig. 4A-C; spikes/s over 500 ms minus baseline; mean across cells, up to n = 10 per genotype; fig., approx.,
  ±3 spikes/s for wild type, ±1 for mutants):

  | VM2: odor | wild type | Or43b mutant | | DL1: odor | wild type | Or10a mutant |
  |---|---|---|---|---|---|---|
  | methyl salicylate | 21 | 10.0 | | cyclohexanone | 2 | 9.2 |
  | 2,3-butanedione | 32 | 27.7 | | ethyl acetate | 10 | 23.2 |
  | γ-valerolactone | 54 | 12.6 | | 2,3-butanedione | 12 | 25.9 |
  | ethyl acetate | 64 | 25.4 | | cis-3-hexen-1-ol | 14 | 11.2 |
  | cyclohexanone | 69 | 12.0 | | butyric acid | 25 | 9.3 |
  | 3-methylthio-1-propanol | 75 | 11.0 | | 1-butanol | 25 | 14.6 |
  | benzaldehyde | 77 | 12.0 | | geranyl acetate | 28 | 17.7 |
  | geranyl acetate | 80 | 6.0 | | 4-methyl phenol | 30 | ≈7 (marker hidden) |
  | cis-3-hexen-1-ol | 84 | 18.1 | | 3-methylthio-1-propanol | 42 | 5.4 |
  | 4-methyl phenol | 86 | 7.2 | | ethyl butyrate | 43 | 23.0 |
  | ethyl butyrate | 91 | 23.9 | | γ-valerolactone | 48 | 7.8 |
  | butyric acid | 96 | 31.5 | | benzaldehyde | 51 | 6.6 |
  | 1-butanol | 118 | 19.8 | | methyl salicylate | 117 | 10.2 |
  | **mean of 13** | **72.8** | **16.7** | | **mean of 13** | **34.2** | **13.2** |

  - (derived) Mutant/wild-type ratio of the 13-odor means: 0.23 (VM2), 0.39 (DL1). Range of purely lateral responses:
    6-32 spikes/s (VM2), 5-26 spikes/s (DL1).
  - Every odor in the set evoked a mean lateral response above baseline in both glomeruli. Five odors that still weakly
    drive the mutant ORNs (e.g. 2-octanone, pentyl acetate; "may be mediated by Or83b") were excluded (Supp. Fig. S2).
  - In DL1, three odors that do not excite DL1 ORNs (cyclohexanone, ethyl acetate, 2,3-butanedione) gave larger mean
    responses in the mutant than in wild type (9-26 vs 2-12 spikes/s). The authors do not comment. Errors are large.
  - The receptor mutation is lifelong, but silent (living) ORNs do not trigger the upregulation of lateral excitation
    that chronic ORN death does (Kazama, Yaksi & Wilson 2011, §5.3), so these are normal-circuit values.
- GABA receptor antagonists do not reduce the lateral depolarization (Supp. Fig. S7; VM2 PNs in Or43b¹): CGP54626 50 µM
  "unaffected" (n = 3; and n = 2 in VA7l-only flies); picrotoxin 10 µM "unaffected" (n = 3; and n = 4 in VA7l-only flies);
  "In some experiments, picrotoxin speeded the kinetics of the lateral depolarization but did not diminish it."

### 1.3 Only one ORN type active (Figs. 5-9)

Two preparations, both with antennal nerves cut and recordings from antennal PNs:
- Experiment 1: Or83b² mutant with Or83b rescued only in VA7l ORNs (pb2B); 72 PNs in 24 of 49 glomeruli, one per fly.
  Rescued VA7l ORN responses match wild type (Supp. Fig. S4).
- Experiment 2: Δ85 background with a 14-odor set that activates only VM7 ORNs (pb1A) among the functional palp ORNs; 15 PNs.
  With VM7 ORNs also silenced (Or42a^f04305;Δ85), "we saw essentially no odor responses in any PNs (Fig. 6D, open
  circles, n=3)".

**Saturation.** "Odors that evoked only a small ORN response produced a near-maximal lateral depolarization in PNs." "In
experiments where we stimulated only one ORN type, increasing the rate of incoming ORN spikes from 50 to 150
spikes/second had little effect on the amount of lateral excitatory input that was broadcast to other glomeruli."

- Fig. 6C, VA7l only, all 72 PNs (x = VA7l ORN rate change, y = depolarization area; fig., approx.):

  | ORN rate (spikes/s) | −20 | −12.5 | 1 | 3 | 10 | 56 | 147 | 169 |
  |---|---|---|---|---|---|---|---|---|
  | area (mV·s) | −0.19 | −0.02 | 0.19 | −0.02 | 1.54 | 1.81 | 1.88 | 1.89 |

  Exponential fit read off the plotted curve (derived): area ≈ 1.88 × (1 − e^(−(r − 1.5)/7.5)) mV·s, i.e. half-maximal at
  ≈7 ORN spikes/s and 90% at ≈19 spikes/s. Inhibiting VA7l (3-octanol) gives a small hyperpolarization, read by the
  authors as loss of tonic lateral excitation driven by spontaneous VA7l spikes.
- Fig. 6D, VM7 only, 15 PNs (fig., approx.): (1.6, 0.22), (8.5, 0.34), (13, 0.50), (16, 0.69), (20.5, 0.83), (32, 0.79),
  (36.5, 0.68), (44.5, 0.82), (116, 0.87), (159, 0.94) as (ORN spikes/s, mV·s). Fit read off the curve (derived): area ≈
  0.89 × (1 − e^(−(r + 2)/16.6)) mV·s, half-maximal at ≈10 ORN spikes/s. "The average magnitude of this depolarization was
  about half of that observed in experiment 1."
- (derived) Mean depolarization over the 500-ms window at saturation: 1.88/0.5 ≈ 3.8 mV (VA7l), 0.89/0.5 ≈ 1.8 mV (VM7).
- Peak depolarization of the all-cell averages (Fig. 6A,B; fig., approx.):
  - VA7l only: 4-methyl phenol 3.8 mV at ≈200 ms; methyl salicylate 3.75 mV; 1-butanol 3.3 mV; tails of ≈0.6-0.8 mV for
    >1 s after offset.
  - VM7 only: 2-pentanone 1.9 mV; 2-butanone 1.9; methyl acetate 1.7; geranyl acetate 1.1; paraffin oil 0.5 mV.
  - **Inconsistency.** Integrating these traces over the paper's window with the printed bars (5 mV and 3 mV) gives areas
    ≈27% (VA7l) and ≈15% (VM7) smaller than the Fig. 6C,D points. The same check on Fig. 8 traces agrees with the Fig. 8
    bars within 5%. So the Fig. 6A,B scale bars are probably slightly off; peaks scaled to the Fig. 6C areas would be ≈5.3
    mV (VA7l, 4-methyl phenol) and ≈2.3 mV (VM7, 2-pentanone) (derived).
- Range across cells: "the response evoked by the strongest odor (4-methyl phenol) ranged from 1.7 mV to 11.8 mV.
  Responses in some PNs were large enough to elicit a few spikes".
- **Two ORN types sum sublinearly** (Fig. 7; n = 8 PNs in DL5, DM6 or VM2; areas, fig., approx.): VM7 alone (2-butanone
  10^-5) 0.93 mV·s; VA7l alone (methyl salicylate 10^-2) 1.33; both 1.54; linear sum 2.25. Blend > either alone (p ≤ 0.01);
  blend < sum (p < 10^-4). (derived) Blend/sum = 0.68.
- **Glomerulus-specific, stereotyped strength** (Fig. 8; areas in mV·s, fig., approx.):
  - VA7l-only, 4-methyl phenol (Fig. 8C; glomeruli hit ≥3 times except DM6 n = 2): VC4 3.03, DL5 2.68, DL1 2.37, VM5v
    2.09, DM3 1.90, DC3 1.74, VM3 1.69, VC3 1.64, VM2 1.57, VA1v 1.57, VA1d 1.46, DM6 1.26; all PNs 1.89. Max/min ≈2.4
    (derived). VC4 > VA1v, p < 0.05 (VC4 n = 7, VA1v n = 8).
  - VM7-only, 2-pentanone (Fig. 8F): DL5 1.31 (n = 5), DM6 0.76 (n = 7), VM2 0.74 (n = 3); all 0.94.
  - Peaks of the glomerulus averages (Fig. 8A,D): VC4 ≈9.0 mV and VA1v ≈4.2 mV (4-methyl phenol); DL5 ≈3.4 mV and DM6 ≈1.9
    mV (2-pentanone).
  - "the nonlinear relationship between the lateral depolarization and ORN firing rate had a similar sensitivity and
    exponential shape across different glomeruli; it is the saturation level that differs (Fig. 8B,E)."
  - Not explained by distance (Fig. 9A), sensillum class (basiconic n = 14, coeloconic n = 3, trichoid n = 6 glomeruli; Fig.
    9B), ORN tuning similarity (Fig. 9C), or input resistance ("Pearson's r^2=0.027").
- **Density.** "Excitatory connections between glomeruli appear to be very dense, perhaps all-to-all." Evidence listed:
  lateral depolarization grows with the number of intact ORN types (most ORNs > palps only > one type); 87/87 PNs received
  input from one ORN type; lateral tuning is broad; VM2 and DL1 lateral tuning is similar.

## 2. Yaksi & Wilson 2010, Neuron 67:1034 ([PMC2954501](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/))

**Setup.** In vivo whole-cell current clamp (Axopatch 200B), adult females 1-3 days, flies raised at 25 °C; recording
temperature not reported. External saline 1.5 mM Ca²⁺, 4 mM Mg²⁺. Odors 500 ms every 45 s, 6 trials. Dual recordings were
done with the antennae removed; current steps of 500 ms set to give "voltage deflections of approximately ± 40 mV" in the
injected cell, 40-50 trials, postsynaptic trace low-pass filtered at 50 Hz. "The coupling coefficient was computed as the
average change in membrane potential of postsynaptic neuron divided by that of the presynaptic neuron." Analysis windows:
- PN spiking: "average spike rate during a 500-msec window beginning 100 msec after nominal stimulus onset".
- Lateral excitation: "average odor-evoked change in membrane potential ... during a 200-msec time window beginning 100 msec
  after nominal stimulus onset".

High-resolution figures (Elsevier `gr*_lrg.jpg`) and the Elsevier supplement were used for all readings below.

**Headline statements (verbatim).**
- "eLN-to-PN synapses transmit both hyperpolarization and depolarization, are not diminished by blocking chemical
  neurotransmission, and are abolished by a gap junction mutation. This mutation eliminates odor-evoked lateral excitation
  in PNs and diminishes some PN odor responses."
- "eLNs have two opposing effects on PNs, driving both direct excitation and indirect inhibition. We propose that when
  stimuli are weak, lateral excitation promotes sensitivity, whereas when stimuli are strong, lateral excitation helps
  recruit inhibitory gain control."
- On the coupling coefficients: "although these coefficients are small, they almost certainly underestimate the strength of
  the connection at the synapse. This is because both electrodes are located at the soma". "depolarizing signals were
  transmitted more effectively across this electrical connection than were hyperpolarizing signals".
- Speed: "electrical stimulation of the antennal nerve elicits depolarization in maxillary palp glomeruli only about 1.5
  msec after onset of depolarization in an antennal glomerulus (Kazama and Wilson, 2008)". "we often saw differences
  between control and shakB2 mutant PNs during the earliest epoch of PN responses".
- "eLN synapses onto iLNs are stronger than their synapses onto PNs. This implies that a major function of eLNs is to
  recruit GABAergic inhibition."

### 2.1 Identifying eLNs (Figs. 1-2)

- "about half of the LNs labeled by krasavietz-Gal4 are GABA-negative (58–61%; Chou et al., 2010; Shang et al., 2007)".
  (Chou 2010's own table gives 12 ± 3 of 16 ± 4 krasavietz LNs GABA+, see §7.1.) "The krasavietz-Gal4 line drives Gal4
  expression in at least three eLNs per antennal lobe".
- ChR2 in krasavietz LNs (500-ms light; PN responses averaged over n = 5 cells; Fig. 1D, fig., approx.):
  - Control: depolarization peaking at ≈1.5 mV ≈70 ms after light onset, back to ≈0 by the end of the light, then ≈−1.1 mV
    ≈140 ms after light offset.
  - With Cd²⁺ (100 µM): peak ≈1.45 mV, then a sustained ≈1.0 mV during the light. "the Cd2+-sensitive component is
    hyperpolarizing and slow, whereas the Cd2+-insensitive component is depolarizing and fast".
  - Flies without the Gal4 driver: "0.2 ± 0.2 mV, n=5".
- Paired krasavietz LN → PN: "we performed 74 dual recordings ... of which 37 showed an excitatory LN-PN connection, 17
  showed an inhibitory LN-PN connection, and the remainder showed no connection." Excitatory LNs had ventrolateral somata.
- eLN signature: always "barraged by spontaneous inhibitory postsynaptic potentials (IPSPs)", "small events resembling
  attenuated action potentials (~10 mV amplitude)" plus "full-sized spikes (~40 mV amplitude)". "every LN with these
  properties also made an excitatory connection with the PN, implying that each eLN is connected to most or all PNs."

### 2.2 eLN odor responses and lateral excitation vs total ORN input (Fig. 3)

"all the odors in our test panel elicited similar eLN responses, regardless of their chemical structure or the total amount
of ORN activity they elicited". "Every eLN we recorded from was broadly tuned to odors and was sensitive to even weak ORN
input." Legend: "All eLNs we recorded were disproportionately sensitive to the weaker odors and were broadly tuned. All these
stimuli elicited similar spike rates as well as similar levels of depolarization." Dilutions are not given in the legend.

| odor | antennal LFP, min (mV; n = 8) | eLN depolarization peak (mV; n = 8, spikes filtered) | PN lateral excitation, peak / mean 100-300 ms (mV; n = 12) |
|---|---|---|---|
| ethyl acetate | −9.2 | ≈8 | 2.9 / 2.0 |
| pentyl acetate | −4.9 | ≈7 | 2.6 / 2.1 |
| methyl salicylate | −1.3 | ≈8-10 | 2.9 / 1.8 |
| heptanoic acid | ≈0 | ≈9-11 | 2.7 / 1.5 |
| ethyl cinnamate | ≈0 | ≈8 | 2.5 / 1.35 |

(all fig., approx.) PNs: VC1, VC2 and DM1 pooled, each deafferented by removing the organ holding its own ORNs. eLN
depolarization peaks ≈180-330 ms after nominal onset and decays during the odor (to ≈3-6 mV at 450-500 ms). The PN lateral
depolarization peaks ≈240-310 ms, holds near 2 mV to the end of the odor, and is followed by a ≈0.6-1.2 mV undershoot.
(derived) A ≥7-fold range of antennal LFP (and two odors with no detectable LFP) gives lateral excitation within ±10%.

### 2.3 Coupling coefficients (Figs. 4-6 and S1; fig., approx., ±0.0005)

| connection | depolarizing steps | hyperpolarizing steps | n | effect of blockers / shakB² |
|---|---|---|---|---|
| eLN → PN | 0.0087 | 0.0024 | 37 pairs | shakB²: −0.001 / −0.001 (abolished; n = 19, p < 0.0001) |
| eLN → PN, Cd²⁺ subset | 0.0106 → 0.0150 with Cd²⁺ | 0.0036 → 0.0028 | 6 | Cd²⁺ n.s. ("slightly increased, probably because Cd2+ blocks spontaneous IPSPs") |
| eLN → PN, mecamylamine 50 µM | 0.0111 → 0.0100 | 0.0035 → 0.0033 | 4 | n.s. |
| eLN → PN, α-bungarotoxin 5 µM | 0.0121 → 0.0080 | 0.0030 → 0.0024 | 6 | n.s.; "a trend toward a decrease ... but in some experiments input resistance also decreased" |
| eLN → PN, D-tubocurarine 50 µM | 0.0080 → 0.0066 | 0.0015 → 0.0018 | 3 | n.s. |
| PN → eLN | 0.0183 | 0.0039 | 39 pairs | shakB²: 0.0159 / −0.003 (hyperpolarizing component abolished, depolarizing kept) |
| PN → eLN, Cd²⁺ subset | 0.0319 → 0.0051 | 0.0060 → 0.0043 | 6 | Cd²⁺ p < 0.05 on depolarization |
| PN → eLN, mecamylamine / α-BTX / D-TC | 0.0102 → 0.0015 / 0.0237 → 0.0030 / 0.0133 → 0.0019 | ≈unchanged | 4 / 6 / 3 | each p < 0.05 |
| eLN → iLN | 0.0119 | 0.0034 | 39 pairs | shakB²: ≈−0.001 / −0.0015 (abolished, n = 25) |
| eLN → iLN, Cd²⁺ subset | 0.017 → 0.0028 | 0.0019 → 0.0022 | 6 | Cd²⁺ p < 0.005; mecamylamine "substantially decreased" (n = 2) |
| iLN → eLN | ≈−0.004 (heterogeneous) | ≈0 | 39 | n.s. for Cd²⁺ or shakB²; some pairs GABAergic |
| PN ↔ PN, sister DA1 PNs | 0.0181 | 0.0077 | 4 pairs (8 coefficients) | shakB²: −0.002 / −0.002 (abolished, p < 0.0005) |

- Electrical vs cholinergic share (derived from the table): eLN→PN keeps ≥66% of its depolarizing transmission under any
  nicotinic antagonist (≥90% under mecamylamine) and all of it under Cd²⁺, and loses all of it in shakB². PN→eLN depolarizing
  transmission falls by 84-87% under Cd²⁺ or any nicotinic antagonist; its electrical part (hyperpolarizing coefficient
  0.004-0.006) is what shakB² removes. eLN→iLN falls 84% under Cd²⁺.
- "shakB2 mutation abolishes the transmission of hyperpolarizing steps but not depolarizing steps" (PN→eLN). "connections
  from eLNs onto iLNs were completely gone in mutant flies ... This result implies that the electrical component of this
  synapse is required for the proper development of the chemical component." Same logic for sister PNs.
- shakB is expressed in PNs: nested RT-PCR from pooled GH146 PN somata (10-15 somata per tube, 9 experiments; Fig. S2;
  primers do not distinguish shakB.neural from shakB.lethal).
- (derived) A 40-mV depolarization of one eLN (with spiking) moves the PN soma by ≈0.35 mV (0.0087 × 40); a 40-mV
  hyperpolarization by ≈0.1 mV.

### 2.4 shakB² abolishes odor-evoked lateral excitation (Fig. 7, S3)

VC1/VC2 PNs with palps removed (antennal odors give purely lateral input; n = 7 control, 7 shakB², pooled 4 VC1 + 3 VC2) and
DM1 PNs with antennae removed (palp odors; n = 5, 5). "p<0.001 for all odors" (VC1/VC2); "p<0.05 for all odors except the
last" (DM1). Values in mV, fig., approx.:

| odor | VC1/VC2 control: peak / mean 100-300 ms | VC1/VC2 shakB²: mean 100-300 ms | DM1 control: peak / mean 100-300 ms | DM1 shakB²: mean 100-300 ms |
|---|---|---|---|---|
| ethyl acetate | 3.7 / 2.6 | −1.2 | 2.1 / 1.1 | −0.8 |
| pentyl acetate | 3.9 / 3.3 | −1.35 | 1.45 / 0.65 | −0.3 |
| methyl salicylate | 4.9 / 3.1 | −0.1 | 0.5 / 0.1 | ≈0 |
| heptanoic acid | 4.4 / 2.6 | ≈0 | 0.5 / 0.2 | −0.1 |
| ethyl cinnamate | 4.1 / 2.4 | ≈0 | 0.3 / 0.1 | −0.1 |

- Control VC1/VC2 peaks fall 170-305 ms after nominal onset; means over 100-600 ms are 2.6-3.6 mV; after offset the
  membrane undershoots by 0.8-1.7 mV (fig., approx.).
- "in the mutant, weak odor-evoked lateral inhibition was observed; this is consistent with a previous report that there is
  a small amount of postsynaptic lateral inhibition in this circuit (Olsen and Wilson, 2008)".
- "wild-type VC1 and VC2 PNs showed lateral excitation of a size that was typical of most other glomeruli (Olsen et al.,
  2007), whereas wild-type DM1 PNs consistently showed smaller lateral excitation". Interpreted as "stronger electrical
  coupling with the eLN network in some glomeruli, and weaker coupling in other glomeruli."
- Rescue (Fig. S3): adult heat-shock expression of UAS-shakB.neural in shakB² restored "robust odor-evoked lateral
  excitation ... in many (although not all) presumptive antennal PNs" (n = 40 heat-shocked, 30 not heat-shocked, 15 no
  Gal4; all pairwise p < 0.05).
- Controls in shakB²: normal PN morphology, normal ab2A ORN responses (n = 5 vs 6), normal iLN↔PN connections (n = 35 vs 19).
  shakB² "significantly increased PN input resistance in PNs that normally receive relatively strong lateral excitation
  (p<0.05 for VC1 and VC2 ...; not significant in DA1 and DM1)" (magnitude not reported).

### 2.5 PN spiking with and without electrical synapses (Figs. 8, 9, S5)

Spike rates are means over 100-600 ms after nominal onset, read off the high-resolution PSTHs (fig., approx., ±5
spikes/s; not baseline-subtracted) and cross-checked against the summary dots (Figs. 8C, 9C). Baselines in the PSTHs: ≈5-13
spikes/s in controls, ≈10-15 in shakB² (fig., approx.; not commented on by the authors).

**VC1 (one PN in the glomerulus; intact circuit; n = 8-9 control, 6-8 shakB²).** "responses to all the test odors were
weaker in shakB2 flies as compared to controls, and for many odors, this difference was statistically significant".

| stimulus | control | shakB² | shakB²/control (derived) |
|---|---|---|---|
| fenchone 10^-2 | 172 | 124 | 0.72 |
| fenchone 10^-4 | 124 | 68 | 0.55 |
| fenchone 10^-6 | 42 | 20 | 0.48 (n.s.) |

- Fig. 8C, all 15 stimuli (dots, high-resolution figure): the 6 significant pairs are ≈181→131, ≈179→128, ≈138→68,
  ≈95→74, ≈93→64, ≈86→50 spikes/s (fenchone 10^-2 and 10^-4, cyclohexanone 10^-2 and 10^-4, isoamyl acetate 10^-2,
  4-methylphenol 10^-3; pairing of dots to odors not resolvable). (derived) shakB²/control = 0.49-0.78, mean 0.66; mean loss
  ≈43 spikes/s. Non-significant pairs: ≈142→128, ≈119→97, ≈40→20, ≈28→21 and four or five pairs at 11-15 → 5-11.
- Antennae removed (fenchone becomes private to VC1 ORNs; n = 6 control, 5 shakB²): no difference. Fenchone 10^-2 ≈244
  vs ≈229; 10^-4 ≈146 vs ≈165; 10^-6 ≈38 vs ≈36 spikes/s. (derived) Removing the antennae raised control VC1 responses to
  fenchone 10^-2 from ≈172 to ≈244 spikes/s, i.e. antennal input inhibits VC1 more than it excites it at this
  concentration (as in Olsen & Wilson 2008, §5.4).
- shakB² did not raise VC1 responses to direct input despite higher input resistance; the authors suggest the change "may
  be too small" or is compensated.

**DA1 (seven sister PNs; cis-vaccenyl acetate is nearly private; n = 5 control, 7 shakB²).** cVA 1X: ≈119 → ≈71-85 (the
mutant trace is partly hidden behind the control trace); cVA 10^-2: ≈69 → ≈40; cVA 10^-4: ≈0 (spikes/s). (derived) ≈29-42%
loss, attributed to loss of PN-PN coupling: "PN-PN synapses can amplify odor responses."

**VC2 (one PN; n = 6 control, 6 shakB²).**

| stimulus | control | shakB² | note |
|---|---|---|---|
| 4-methylphenol 10^-1 | 138 | 163 | n.s. |
| 4-methylphenol 10^-2 | 98 | 146 | larger in mutant |
| 4-methylphenol 10^-3 | 61 | 132 | larger in mutant |
| fenchone 10^-2 | 51 | 7 | lateral-only response, abolished |
| cyclohexanone 10^-2 | 77 (peak ≈170) | 4 | lateral-only response, abolished |
| fenchone 10^-6, 2-heptanone 10^-6 | ≈11 | ≈20-21 | significant; direction read from Fig. 9C |

- Interpretation (stated): shakB² removes eLN→iLN drive, so "the disinhibitory effect of adding the antagonists [5 µM
  picrotoxin + 20 µM CGP54626] was significantly smaller in the mutant than in controls" (4 cells each, p < 0.005).
- (derived) In an intact fly, lateral excitation alone drove VC2 to 50-80 spikes/s (100-600 ms mean) and ≈170 spikes/s at
  the onset peak, for two odors whose responses vanish in shakB² and so did not come from VC2's own ORNs (shakB² leaves ORN
  responses normal, Fig. S4).

**DM1 (one PN; weak lateral excitation).** shakB² had no significant effect (n = 2 control, 5 shakB²; Fig. S5).

## 3. Huang, Zhang, Qiao, Hu & Wang 2010, Neuron 67:1021 ([doi](https://doi.org/10.1016/j.neuron.2010.08.025))

**Access.** Main text from the Wayback Machine copy of the cell.com full-text page (2022-07-01 capture). Figures from
Elsevier's high-resolution `gr*_lrg.jpg` files; supplement `mmc1.pdf` from ars.els-cdn.com.

**Setup.** Paired whole-cell recordings in an **isolated-brain explant** (1-day-old females, perineural sheath removed;
saline 1.5 mM Ca²⁺, 4 mM Mg²⁺). Odor responses **in vivo** (2-day-old females; 1-s odor pulses, 6 trials at 30-s intervals;
dilutions not stated in the accessible text). Flies raised at 25 °C; recording temperature not reported. eLNs were
krasavietz-Gal4 GFP cells; PNs were recorded in the anterior-dorsal cluster and identified by small spikes ("<10 mV") and
biocytin fills.

**Headline statements (verbatim).**
- "Paired recordings of krasavietz eLNs and PNs showed reciprocal excitatory connections mediated by dendrodendritic
  cholinergic synapses and gap junctions."
- "the connection from eLNs to PNs is largely mediated by gap junctions, whereas the PNs to eLNs connection is predominantly
  mediated by chemical synapses."
- "These gap junctions show rectifying properties, with eLNs to PNs junctions showing significantly higher coupling ratio".
- "each eLN responded with distinct patterns to different odors, and each odor elicited distinct responses in different
  eLNs, with specific temporal patterns of spiking".

### 3.1 Two krasavietz cell types (Fig. 1, S1, S2)

- Type I (the eLNs): "a transient high-frequency burst spiking followed by sparse spiking"; initial spike frequency over
  the first 150 ms of a step ≈62 Hz (range ≈40-100, n = 52); ≈17 action currents during a 500-ms ramp (12-23). Type II: a
  "low-frequency adapting spike train", ≈27 Hz (13-40, n = 33); ≈11 action currents (6-14). (fig., approx.)
- Dye coupling: "for the great majority of type I krasavietz neurons (23/27), biocytin diffused from the single recorded
  krasavietz neuron to many other antennal lobe neurons, whereas none of type II krasavietz neurons (0/7)". Biocytin spread
  to PNs was confirmed with GH146-LexA labeling (Fig. 3J); PN fills rarely spread ("more severe rectification of dye
  spreading").
- Type II krasavietz cells had no effect on any of 15 paired PNs (Fig. S3) but were excited by PNs; they are treated as
  iLNs.
- Fig. S2: "Krasavietz eLNs usually send their arbors to all glomeruli except DA1, DL3." Discussion: "dense arborization
  that covers almost all glomeruli".
- Intrinsic properties (Fig. S1A, stated): krasavietz eLN spike amplitude 25.69 ± 4.78 mV, threshold −36.97 ± 6.37 mV,
  input resistance 0.40 ± 0.09 GΩ (n = 14); PN 6.62 ± 1.76 mV, −29.70 ± 4.72 mV, 0.61 ± 0.17 GΩ (n = 16-27).

### 3.2 eLN → PN and PN → eLN, 100-ms steps (Fig. 2)

- Protocol: "100-ms inward current pulses which usually triggered 4–6 spikes"; 10 trials per pair.
- "In 35 pairs (from 16 flies) examined, krasavietz type I neuron could elicit detectable excitatory responses in the PNs".
  Every pair was reciprocal.
- "The average amplitude of PN depolarization (for 100 ms eLN stimulation) was about 0.9 mV, and that from PN to eLN was
  about 0.6 mV (Figure 2D)." Fig. 2D bars ≈0.93 and ≈0.67 mV (fig., approx.).
- Fig. 2C (fig., approx.): eLN→PN 0.27-2.2 mV across the 35 pairs (my readings average 0.93 mV, matching the text). One eLN
  tested against 5 PNs gave 1.83, 0.37, 0.37, 0.63 and 0.86 mV: "there are indeed differences in the strength of
  connections from the same krasavietz eLN to different PNs".
- Example pair (Fig. 2B): the eLN, stepped from ≈−57 mV, fired ≈6 spikes; the PN depolarized by ≈1.7 mV from ≈−56.8 mV,
  peaking at the end of the step and decaying over ≈60 ms (fig., approx.).
- PN→eLN excitation survived removal of PN axon targets (mushroom body and lateral horn excised; n = 15, p = 0.937), so it
  is dendrodendritic.

### 3.3 Coupling ratios, pharmacology and single-spike transmission (Fig. 3)

- Subthreshold coupling, 200-ms steps, 20 trials (Fig. 3D, n = 12 pairs, fig., approx.):
  - eLN→PN 0.015 (depolarization), 0.007 (hyperpolarization).
  - PN→eLN 0.008 (depolarization), 0.010 (hyperpolarization).
  - Depolarizing coupling eLN→PN > PN→eLN, p < 0.005; hyperpolarizing n.s. (p = 0.116). Individual pairs: depolarizing
    eLN→PN 0.0075-0.021.
- Nicotinic antagonists on 100-ms-step responses (Fig. 3A,B; % of control, fig., approx.):
  - eLN→PN: mecamylamine 100 µM ≈105% (n = 8, p = 0.834); α-bungarotoxin 5 µM ≈62% (n = 7, p < 0.01).
  - PN→eLN: mecamylamine ≈22% (n = 6, p < 0.005); α-bungarotoxin ≈22% (n = 6, p < 0.01).
- **Single-spike transmission (spike-triggered averages; Fig. 3E-K).** A ≈30-40-ms current pulse triggered one presynaptic
  spike; 50-100 trials, aligned on the spike peak.
  - eLN→PN STA amplitudes for 12 pairs (Fig. 3K; mV; fig., approx.): 0.52, 0.16, 0.38, 0.32, 0.20, 0.17, 0.63, 0.69, 0.20,
    0.72, 0.66, 0.33. (derived) Mean 0.42 mV, median 0.36 mV, range 0.16-0.72 mV.
  - PN→eLN STA amplitudes for 11 pairs: 0.14, 0.74, 0.20, 0.23, 0.09, 0.17, 0.33, 0.07, 0.10, 0.19, 0.11. (derived) Mean
    0.21 mV.
  - Fraction of the STA peak already reached before the presynaptic spike (Fig. 3I): ≈60% (eLN→PN), ≈43% (PN→eLN). The
    pre-spike part is subthreshold electrical coupling during the current pulse.
  - Time course of the example eLN→PN pair (Fig. 3E, pair 9; fig., approx.): rise begins with the eLN's depolarization
    (≈37 ms before the spike peak); 0.47 mV at the spike peak; peak 0.71 mV at ≈+8 ms; 0.53 mV at +26 ms, 0.35 at +38 ms,
    0.23 at +50 ms, 0.14 at +66 ms, ≈0.04 at +86 ms. (derived) Decay τ ≈35-40 ms after the peak; spike-locked increment
    ≈0.24 mV in this pair.
  - (derived) Applying the 60% pre-spike share to the mean, the spike-locked increment averages ≈0.17 mV (range ≈0.06-0.29).

### 3.4 eLN ↔ eLN (Fig. 4)

- 100-ms steps: responses 1.4-2.55 mV across 10 pairs, reciprocal 0.85-2.35 mV (Fig. 4B, fig., approx.).
- Coupling ratio ≈0.025 (hyperpolarization) and ≈0.027 (depolarization), n = 14; individual pairs 0.016-0.042 (Fig. 4D,
  fig., approx.).
- eLN→eLN STAs (8 of 10 pairs read, Fig. 4F): peaks 0.59-1.01 mV (mean ≈0.73) at +13 to +23 ms; 40-77% of the peak reached
  before the presynaptic spike (fig., approx.). Dye coupling between eLNs (Fig. 4G).

### 3.5 eLN ↔ iLN (Fig. 5)

- "rhythmic spontaneous IPSPs (or IPSCs) in about 50% krasavietz eLNs ... about 0.8 mV and 10 Hz" (n = 45), blocked by
  picrotoxin 200 µM or CGP54626 50 µM (n = 5 each).
- "Out of 10 potential iLN - eLN pairs, only one pair showed that activation of putative iLN induced inhibitory responses
  in krasavietz eLN ... no detectable excitation in iLNs was observed by activation of krasavietz eLNs. Therefore, the
  connections between krasavietz eLNs and iLNs are rare." (iLNs sampled only in the dorsolateral AL.)

### 3.6 ORN input to eLNs (Fig. 6, S5)

- Antennal-nerve stimulation (0.1-ms pulses): onset latency ≈2.0 ms in eLNs (n = 16) and ≈2.0-2.25 ms in PNs (n = 15),
  independent of intensity; all latencies 1.5-3.5 ms (n = 27 eLNs, 25 PNs; Fig. 6B,C, fig., approx.). eLN responses
  "could be abolished by application of α-BTX". Conclusion: "ORNs make monosynaptic connections with krasavietz eLNs."
- Weak nerve stimulation in 21 simultaneously recorded eLN-PN pairs (Fig. S5, peak inward current excluding action
  currents; fig., approx.): eLNs 12-160 pA (median ≈60), PNs 8-53 pA (median ≈14); the eLN current was larger in 19/21
  pairs. "the krasavietz eLN responses were much larger than those of PNs in response to the same low-intensity antennal
  nerve stimulation."

### 3.7 eLN odor responses in vivo (Fig. 7)

- 12 eLNs, 11 odors (2,3-butanedione, acetone, cyclohexanone, carvone, methyl salicylate, ethyl acetate, isoamyl acetate,
  pentyl acetate, benzaldehyde, 3-octanol, methylcyclohexanol) plus paraffin oil.
- Responses were odor-selective, and either On (0-1.5 s) or Off (1.5-3 s after onset; e.g. "robust responses to 7 of 11
  tested odorants at 0.5 to 1 s after the termination of the odorant stimulus" in eLN #5).
- Example eLN #1 (raster spike counts, fig., approx.): ethyl acetate ≈9-12 spikes per trial between ≈0.18 and 0.48 s after
  odor-bar onset (≈35 Hz); acetone 12-18 spikes per trial between ≈0.10 and 0.85 s (≈20 Hz); very little spontaneous
  firing.
- Normalized responses (% of each cell's maximum over the 11 odors; Fig. 7C,D, fig., approx.), for the two odors brainfly
  uses: On responses (0-1.5 s; eLNs #1-#4) to 3-octanol 9, 36, 12, 10% and to methylcyclohexanol 6, 9, 35, 19%; Off
  responses (1.5-3 s; eLNs #5-#8) to 3-octanol 90, 100, 54, 94% and to methylcyclohexanol 78, 66, 51, 100% (Huang's
  "methylcyclohexanol", isomer not stated). Acetone was the maximum for all four On cells. Absolute spike counts for these
  panels are not given.

### 3.8 KL107 eLNs (Fig. S6)

- KL107-Gal4 ventral LNs are excitatory (local ATP/P2X2 activation depolarized PNs by ≈16 mV, reduced to ≈5 mV by α-BTX;
  fig., approx.), with sparse arbors in "many but not all glomeruli" and "tonic action potentials of small amplitudes".
- Pairs: "among the 8 KL107 eLN - PN pairs recorded, only 3 KL107 eLNs were able to excite their paired PN, and 4 PNs made
  excitatory connections with their paired KL107 eLN." eLN→PN amplitudes ≈1.0, 2.0 and 0.7 mV; PN→eLN ≈5.1, 4.1, 3.1 and
  3.8 mV (fig., approx.).

### 3.9 Where Huang 2010 and Yaksi & Wilson 2010 disagree

| issue | Yaksi & Wilson (in vivo) | Huang et al. (explant pairs; in vivo odors) |
|---|---|---|
| eLN odor tuning | broad, saturating, similar for all odors | selective, On or Off types |
| eLN → iLN | strong, mostly cholinergic, needs shakB | rare (0/10 excitatory) |
| eLN → PN mechanism | electrical; no nicotinic block | mostly electrical; α-BTX removes ≈38%, mecamylamine nothing |
| eLN → PN coupling (depolarizing) | 0.0087 (with spikes, 500-ms steps) | 0.015 (subthreshold, 200-ms steps) |
| eLN → PN coverage | each eLN to "most or all PNs" | every tested pair connected, with strengths varying 7-fold |

## 4. Shang, Claridge-Chang, Sjulson, Pypaert & Miesenböck 2007, Cell 128:601 ([PMC2866183](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866183/))

**Setup.** Two-photon imaging of synapto-pHluorin (spH) in ORN, PN or LN terminals; 2-s pulses at 0.1% saturated vapor
(1:100 in paraffin oil, 50 ml/min into 450 ml/min carrier); measured concentrations 0.6-35 ppm isobutylene equivalent.

- **PN responses without their own ORNs.** In Δhalo flies (Or22a/b deleted; ab3A ORNs virtually silent), DM2 PNs still
  responded to E2-hexenal, γ-valerolactone, ethyl acetate and 2-heptanone: "DM2 PN response amplitudes were only
  moderately attenuated; they reached 32–93 % of wild-type levels". Wild-type DM3 and DM6 PNs responded to odors that did
  not activate their own ORNs (Figs. 2C,D).
- **Not disinhibition.** Picrotoxin 250 µM + CGP54626 50 µM "caused a modest generalized increase in PN response
  amplitudes (from 4.02 ± 1.57 to 4.73 ± 1.77 % ΔF/F, mean ± SD, n = 84 glomerulus-odor pairings; p < 0.0005 ...)", and DM2
  responses in Δhalo "persisted slightly enhanced or undiminished".
- **Cholinergic LNs** (Tables S1, S2; mean ± SEM):
  - krasavietz-Gal4 ("a dozen or so LNs"): 63.1 ± 4.7% ChAT+ (n = 9 brains), 39.4 ± 5.8% GABA+ (n = 10). With a Cha-dsRed
    reporter: 11.6 ± 1.5 labeled cells per lobe, of which 10.5 ± 1.4 (86.7%) were dsRed+ (n = 7). "eight to 11 large,
    brightly fluorescent neurons extending a visible process into the lobe were identified as cholinergic".
  - KL107-Gal4 (≈50 LNs, also some ORNs, ventral PNs and KCs): 70.9 ± 6.0% ChAT+, 32.6 ± 6.5% GABA+ (n = 8).
  - Controls: GH146 94.1 ± 1.1% ChAT+; GH298 81.2 ± 4.7% GABA+.
  - Immuno-EM: 23% of krasavietz spH-positive profiles ChAT+ (n = 562 profiles).
  - MARCM: "all cholinergic LNs we observed (n = 25) were commissure- and axonless cells that extended a single dendritic
    trunk into the center of one antennal lobe. There, the process arborized into numerous branches terminating in most, if
    not all, glomeruli".
- **eLN activity is spatially diffuse.** krasavietz spH signals: "Very little odor-specific spatial structure ... whose
  response amplitudes appeared nearly uniform across glomeruli".
- Proposed function: "the addition of a positive offset to many or all glomerular channels"; "excitatory LNs play an
  analogous, but opposite, role at low odor concentrations, increasing and redistributing odor-evoked activity over a larger
  ensemble of PNs" (stochastic-resonance argument). Yaksi & Wilson later argued eLN-PN coupling is electrical and adds
  little noise.

## 5. Wilson-lab follow-ups: latency, sister-PN coupling, plasticity, and the net sign of lateral input

Compiled by a helper agent from the PMC full texts, PDFs (figures at 300 ppi) and supplements; tags as above.

### 5.1 Kazama & Wilson 2008, Neuron 58:401 ([PMC2429849](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/))

In vivo, antennae (and palps) cut just before recording, antennal nerve stimulated with a suction electrode, PNs voltage
clamped at −65 mV.
- Lateral EPSCs in palp (VM7) PNs with all ORN input to them removed: "evoked smaller and slower EPSCs than those recorded in
  antennal PNs ... These slow EPSCs must reflect lateral input, probably from cholinergic interneurons. The response grew
  gradually when we progressively increased the stimulus intensity." Legend: "Mecamylamine (50 uM) blocks this response."
  (Consistent with the ORN→eLN step being nicotinic; the eLN→PN step is electrical.)
- Size and shape (one VM7 PN, fig., approx.): ≈0.7-6.4 pA peak with rising stimulus intensity, time-to-peak ≈12 ms, decay
  over ≈150 ms.
- Latency: "The onset of the lateral component is about 1.5 ms later than direct component (p < 10^-4, t-test, n = 32
  direct, 5 lateral) and the jitter of the lateral component is larger". Fig. 1H (fig., approx.): onset 4.69 vs 6.07 ms
  after the stimulus; onset SD 0.25 vs 0.43 ms. "this delay is insufficient for multisynaptic propagation ... excitatory
  interneurons receive monosynaptic input from ORNs".
- "In most of our experiments, the slow component was relatively small, on average only about 1 % as large as the fast
  component at the time when the fast component peaks." (Measured at the fast peak, before the slow component has risen;
  not a ratio of peaks.)
- Chronic palp removal (4-7 days) made "a population of large mEPSCs" appear in VM7 PNs: "This might ... reflect a
  potentiation of lateral excitatory connections in response to sensory deprivation."
- Discussion: lateral excitation "should decrease the odor selectivity of PNs", but "Synaptic depression is also likely to be
  a major reason why PNs are more broadly tuned to odors than the presynaptic ORNs".

### 5.2 Kazama & Wilson 2009, Nat Neurosci 12:1136 ([PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/))

In vivo, females 2-5 days, whole-cell current clamp; voltages "uncorrected for liquid junction potential of 13 mV".
- Sister PNs (DM6 pairs, antennae removed, 50-trial averages) are reciprocally coupled. Coupling coefficients (Fig. 7d, fig.,
  approx.): hyperpolarizing 0.0136 ± 0.0013, unchanged by 100 µM Cd²⁺ (0.0112 ± 0.0009); depolarizing 0.035 ± 0.0045,
  reduced to 0.016 ± 0.002 by Cd²⁺ ("consistent with a mixed electrical/chemical synapse"). n pairs not stated. Largest
  responses ≈−0.9 mV for a ≈−60 mV command and +1.4 to +2.1 mV for ≈+60 mV (command cell spiking).
- Heterotypic PN pairs: "Coupling is negligible" (responses ≈0-0.2 mV for 30-65-mV commands; coefficient ≲0.003, derived).
- Spikelets: legend "Note small action potentials when the Command neuron is depolarized above its threshold". Spikelet size
  per spike: not reported. Dye: "Biocytin and Alexa dyes did not reveal coupling between a PN and any other neurons".
- Correlations: sister PNs share 96-99.6% of EPSCs. Spike-count correlation (2-ms bins): homotypic ipsilateral 0.14
  (spontaneous) / 0.20 (odor), n = 15; heterotypic ipsilateral 0.004 / 0.015, n = 8 (fig., approx.). "The absence of
  correlations in heterotypic ipsilateral PNs argues that LNs contribute relatively little correlated noise to PNs."
- Deafferented sister PNs (palps removed) still share slow ≈1-2-mV membrane fluctuations (Vm correlation 0.61-0.69
  ipsilateral), "much smaller than the correlated membrane potential fluctuations driven by ORNs".

### 5.3 Kazama, Yaksi & Wilson 2011, J Neurosci 31:7619 ([PMC3119471](https://pmc.ncbi.nlm.nih.gov/articles/PMC3119471/))

In vivo whole-cell; "acute" = antennae or palps removed from 2-day-old flies and recording "typically initiated within 20
min"; "chronic" = removed within hours of eclosion and recorded 2 days later. Odors 1:100, 10-fold air dilution, 500 ms.
- Abstract: "In the normal circuit, excitatory connections between glomeruli are weak. However, after we chronically severed
  receptor neuron axons projecting to a subset of glomeruli, we found that odor-evoked lateral excitatory input to
  deafferented projection neurons was potentiated severalfold. This was caused, at least in part, by strengthened electrical
  coupling from excitatory local neurons onto projection neurons, as well as increased activity in excitatory local neurons.
  Merely silencing receptor neurons was not sufficient to elicit these changes."
- krasavietz-Gal4 "drives Gal4 expression in at least 2 antennal lobe excitatory LNs (eLNs) and sometimes 3".
- eLN→PN pairs: "In every pair we recorded from, both hyperpolarizing and depolarizing steps were transmitted ... each eLN
  makes an electrical synapse onto many (or all) PNs." After chronic removal the synapses "seem to be purely electrical, with
  little or no chemical component" (mecamylamine 50 µM no effect, data not shown).
- Coupling coefficients (Fig. 2C, 4B; fig., approx.; antennae and palps removed acutely):

  | PN group | condition | hyperpolarizing | depolarizing | n |
  |---|---|---|---|---|
  | antennal PNs | acute | 0.0021 ± 0.0004 | 0.0073 ± 0.0008 | 36 |
  | antennal PNs | chronic | 0.0028 ± 0.0012 | 0.0131 ± 0.0019 | 22 |
  | palp PNs (VA4) | acute / chronic | 0.0014 / 0.0028 | 0.0036 / 0.0087 | 4 / 5 |

  Input resistance (fig., approx.): PNs 862 ± 44 MΩ acute; eLNs 476 ± 67 MΩ; unchanged by chronic removal.
- Example pair (Fig. 2B; fig., approx.; 50-trial PN average): eLN +29 mV with ≈22 Hz spiking for 0.5 s → PN +0.2 mV,
  still rising at the end of the step; eLN −39 mV → PN −0.1 mV. No spikelets resolvable.
- Lateral depolarization in acutely deafferented PNs (mean, mV; fig., approx.; n = 5-11):

  | PNs | odors | pentyl acetate | ethyl acetate | methyl salicylate | paraffin oil |
  |---|---|---|---|---|---|
  | VM2, antennae removed | palp | 2.5 | 1.8 | 1.4 | 0.8 |
  | VM7, palps removed | antennal | 4.9 | 5.1 | 3.9 | 4.3 |
  | antennal PNs (unlabeled), antennae removed | palp | 2.6 | 2.7 | 1.5 | 0.27 (odor mix 3.1) |

  Chronic (2 days) values were 2-6× larger (e.g. VM2 pentyl acetate 10.2, ethyl acetate 9.9 mV; 5 days larger still), and
  chronic responses "generally elicited a train of action potentials". The plasticity needs glia (Draper/Wld^S, glial
  shibire^ts).
- eLN firing (palp odors, antennae removed; 100-600 ms; fig., approx.): acute pentyl acetate 5.6 ± 1.4, ethyl acetate 6.0 ±
  1.2, methyl salicylate 11.2 ± 0.6, paraffin oil 3.7 ± 0.7 Hz (n = 7); chronic 14.9-38.5 Hz (n = 6). eLN resting Vm ≈−35
  mV (uncorrected).
- **Receptor mutants keep normal lateral input.** Or43b-mutant VM2 PNs, acute, palp odors: pentyl acetate 1.60 vs 2.44
  (control), ethyl acetate 1.50 vs 1.80, methyl salicylate 0.80 vs 1.42, paraffin oil 0.06 vs 0.79 mV; "no significant
  difference" (n = 5 each). Or83b-mutant VM7 PNs: responses to 1,4-diaminobutane "very similar in controls and mutants"
  (n = 4, 2). "merely suppressing electrical activity in ORNs is not sufficient to trigger an upregulation of the eLN
  network." So Olsen 2007's receptor-mutant responses (§1.2) reflect the normal circuit; chronically ablated preparations do
  not.

### 5.4 Olsen & Wilson 2008, Nature 452:956 ([PMC2824883](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/))

- Removing most lateral input (antennae cut; palp PNs, palp odors): "removing the antennae increased most of the odor
  responses of these PNs ... No odor responses were decreased. This implies that most of our odors normally evoke lateral
  inhibitory input to these glomeruli, and this outweighs the effect of lateral excitatory input." Disinhibited: 18/20 odors
  in VM7, 13/20 in VC1.
- Breadth without lateral input: "When we removed most lateral input to PNs, the nonlinearity persisted (Fig. 1d), and PNs
  became even more broadly tuned (Fig. 1e) ... broad PN tuning results mainly from purely intra-glomerular mechanisms ...
  Lateral excitation should tend to broaden PN tuning even more, but lateral inhibition evidently counteracts this." Lifetime
  sparseness (fig., approx.): VM7 ORN 0.65, PN intact 0.47, PN antennae removed 0.26; VC1 0.61, 0.57, 0.25.
- Lateral input alone (palps removed, antennal odors, VM7 PNs, n = 6-7; fig., approx.): peak ≈4.8 mV (ethyl butyrate), ≈5.0
  (pentyl acetate), ≈2.4 (4-methyl phenol), decaying to ≈2 mV by odor offset, then an undershoot of ≈2-3 mV. "For all 20
  odors in our panel, lateral input depolarized VM7 PNs when their cognate ORNs were absent ... and hyperpolarized these PNs
  when their ORNs were spontaneously active" (net −3.5 to −8 mV with palps present but shielded; fig., approx.).
- Voltage clamp, Or43b-mutant VM2 PN at −85 mV, 1-s odor to the other antenna and palps (one cell, 20 trials): lateral inward
  current ≈33 pA peak at ≈170 ms, ≈7 pA sustained, "resistant to GABA antagonists" (fig., approx.).

### 5.5 Olsen, Bhandawat & Wilson 2010, Neuron 66:287 ([PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/))

Intact flies (no deafferentation); response = spikes in the 500-ms odor minus the preceding 500 ms.
- Transform fits include whatever lateral excitation is present: "R_max = 170, 167, 163, and 144, and sigma = 16.3, 11.8,
  12.4, and 44.8, for glomeruli DM4, DL5, VM7, and DM1"; simulations used Rmax = 165, σ = 12 spikes/s, exponent 1.5; input
  gain control m = 10.63 (VM7), 4.19 (DL5).
- "we found that the net effect of lateral input was always inhibitory. However, this does not imply that lateral
  excitatory connections make no contribution - only that they do not dominate."
- GABA antagonists (5 µM picrotoxin + 10 µM CGP54626) abolished suppression of the VM7 response to 2-butanone 10^-6 by
  pentyl acetate 10^-3: blend "not significantly different from the response to the private odor alone (p=0.18)" (n = 5),
  i.e. no detectable net lateral excitation even with inhibition blocked in this test.
- Odors that barely drive a PN's own ORNs gave near-zero net PN responses in intact flies: VM7 −2.5 to +9 Hz for ORN
  responses of −2 to 12 Hz; DL5 −1.1 Hz (fig., approx.).

### 5.6 Bhandawat et al. 2007, Nat Neurosci 10:1474 ([PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/))

Intact flies; 7 glomeruli × 18 odors at 1:100 (then 10× in air); main metric = rate 100-200 ms after onset minus baseline.
- Lifetime sparseness ORN → PN (fig., approx.): DL1 0.90 → 0.47, DM1 0.78 → 0.36, DM2 0.78 → 0.42, DM3 0.84 → 0.57, DM4
  0.81 → 0.42, VA2 0.76 → 0.17, VM2 0.49 → 0.12 (means 0.77 → 0.36).
- Responses >20 Hz: 39/126 ORN-odor pairs vs 105/126 PN-odor pairs (helper agent's readout of all Fig. 3a bars).
- When the cognate ORN response was ≤5 Hz (56 pairs): PN median 28 Hz, mean 34 Hz, 64% >20 Hz (derived). Caveat: 1-5 Hz of
  ORN input alone can drive 10-30 Hz through the steep transform, so this is not purely lateral.
- Statements: "a portion of a PN's odor response profile is not systematically related to its direct ORN inputs, likely
  reflecting lateral connections between glomeruli"; PN-vs-ORN functions have "a y-intercept >0 ... Lateral excitatory
  connections are strong enough to trigger these responses".
- Weak odors (DM4, 500 ms): at 1:100,000 only 2,3-butanedione (≈24 Hz) and ethyl acetate (≈21 Hz) drive DM4 ORNs, yet DM4
  PNs respond 37 and 61 Hz to those and 9-23 Hz to benzaldehyde, butyric acid, ethyl butyrate, 2-octanone and pentyl acetate
  (fig., approx.); "for a few odors, the PN response is larger for the lowest concentration (1:100,000) as compared to an
  intermediate concentration (1:10,000)".

### 5.7 Other Wilson-lab statements

- Nagel, Hong & Wilson 2015 (Methods): lateral excitation "contributes to PN odor responses. However, its overall
  contribution is small in most cases, relative to the contribution of feedforward excitation" (VM7 pilot, palps intact vs
  removed; numbers not reported). Their GABA-LN optogenetics used shakB² "in order to eliminate lateral excitation".
- Hong & Wilson 2015: "stimulating GABAergic LNs can recruit not only lateral inhibition, but also lateral excitation,
  because GABAergic LNs are electrically coupled to specialized cells that also couple to PNs", so they used shakB².
- Wilson 2013 review ([PMC3933953](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)): "lateral excitation is not strictly
  necessary to explain the basic phenomenon of broad PN tuning"; "the contribution of eLNs to PN odor responses is not
  negligible ... The net effect of the eLN network on a PN - either excitation or inhibition - appears to depend on both the
  glomerulus and the odor stimulus"; open question: "Are these neurons actually important for boosting sensitivity near
  absolute threshold for odor detection?"

## 6. Other labs: imaging, food-odor synergy, shakB-independent lateral excitation

Compiled by a helper agent from PMC full texts, SI files and figure pixels (spot-checked: the Shimizu & Stopfer numbers and
quotes). Imaging studies report ΔF/F, not rates.

### 6.1 Das, Trona, Khallaf, Schuh, Knaden, Hansson & Sachse 2017, PNAS 114:E9962 ([PMC5699073](https://pmc.ncbi.nlm.nih.gov/articles/PMC5699073/))

In vivo widefield Ca²⁺ imaging (GCaMP3; 4 Hz; 2-s odor; response = frames 10-18, ≈0.25-2.5 s after onset); virgin females
unless noted. No PN electrophysiology; no pharmacological gap-junction blockers.
- "in virgin females cVA and the complex food odor vinegar evoke a synergistic response in the cVA-responsive glomerulus
  DA1. This synergism, however, does not appear at the input level of the glomerulus, but is restricted to the projection
  neuron level only. Notably, it is abolished by a mutation in gap junctions in projection neurons and is found to be
  mediated by electrical synapses between excitatory local interneurons and projection neurons."
- DA1 PN responses (medians, fig., approx.): vinegar alone ≈0-2%. cVA alone vs cVA + vinegar: 10^-3 8.4 vs ≈8.3% (n = 11,
  n.s.); 10^-2 5.3 vs 22.0% (n = 20, p < 0.001); 10^-1 15.9 vs 23.8% (n = 23, p < 0.01). Means vs the linear sum (Fig. S1A):
  22.2 vs 12.7% and 27.0 vs 19.4% (derived: 1.75× and 1.39×). "only the 1:1 mixture induced a synergistic response".
- No boost at the input: Or67d ORNs (n = 9) cVA 74 vs mix 65 Hz (10^-2), 90 vs 105 Hz (10^-1); DA1 ORN axon Ca²⁺ 9.6 vs
  9.1%.
- Genetics (cVA vs mix, %): shakB² 11.4 vs 12.9 and 17.4 vs 21.9 (n = 9, n.s.); GH146>shakB-RNAi 8.1 vs 6.1 and 13.1 vs
  12.2 (n = 7, n.s.); shakB.neural rescued in GH146 PNs + krasavietz eLNs in shakB² 4.2 vs 9.3 and 14.4 vs 24.2 (n = 8, 7;
  p < 0.01, < 0.05). Responses to cVA alone were not reduced by shakB loss.
- Specificity: no synergy with limonene, 1-hexanol or acetic acid; none in males or mated females; no other GH146 glomerulus
  interacted (the most vinegar-responsive glomeruli were not GH146-labeled).
- krasavietz eLN Ca²⁺ in DA1: "responded only minimally to all three odorants at the two lower concentrations ... clearly
  and strongly to odorants at the highest concentration"; at 10^-1 vinegar 3.5%, cVA 1.7%, mix 5.2% (n = 15); ≤2.3% at
  10^-2. Photoactivated krasavietz label spread from DA1 to DM3, DM1, DM2, DM4, DL2d, DL2v (vinegar glomeruli).
- Model (stated): lateral excitation reaches DA1 more strongly than other glomeruli, and "As glomerulus DA1 possesses a large
  number of electrically coupled sister PNs, the signal gets further amplified" (DA1 has "seven to eight PNs").
- Note: Huang 2010 reported krasavietz eLNs avoiding DA1 and DL3; Das found krasavietz processes in DA1.

### 6.2 Shimizu & Stopfer 2017, Front Neural Circuits 11:30 ([PMC5413558](https://pmc.ncbi.nlm.nih.gov/articles/PMC5413558/))

In vivo whole-cell, saline at 23-24 °C; antennae removed, palp odors at 0.3%, 1-s puffs.
- shakB² removes most lateral excitation in one PN lineage: "for ethyl acetate, peak depolarization was 5.71 ± 1.89 mV in
  control flies and 0.76 ± 0.67 mV in shakB^2 mutants. For ethyl butyrate, peak depolarization was 6.23 ± 2.60 mV in control
  flies and 0.48 ± 0.46 mV in shakB^2 mutants; n = 13 for control and n = 6 for shakB^2 mutant including ePNs in DA1 and
  VA5, p < 0.001".
- But not everywhere: "in two other glomeruli, VC3 and VM5v, in the same shakB^2 mutants we observed large amplitude
  odor-elicited depolarizations ... shakB-dependent electrical synapses between ePNs and eLNs do not provide the sole
  mechanism underlying lateral excitatory interactions". Fig. 5B (fig., approx.): VC3 ≈13-14 mV control vs ≈14-16 mV
  shakB²; VM5 ≈8 mV vs an early ≈4 and late ≈7-8 mV.
- GABAergic ventral PNs (MZ699) excite ePNs through chemical synapses (latency 1.33 ± 0.13 ms, n = 5), but silencing them
  (His-Cl) did not reduce lateral excitation (6 ePNs, 7 odor-ePN pairs, p = 0.23) or intact odor responses (13 ePNs).
- Their argument (verbatim): "Because the number of eLNs is small (two or three), and the coupling reported between each eLN
  and ePN is weak (1–2 mV EPSPs), it is not clear how activity mediated by electrical synapses is sufficient to explain the
  strong odor-evoked lateral excitation observed in some glomeruli (~8 mV on average, up to 20 mV, Olsen et al., 2007, and
  Figure 5)." (Olsen 2007 states 1.7-11.8 mV across cells for the strongest single-ORN-type odor, and its palp-only means
  peak at ≈6-7.5 mV; I did not find "20 mV" stated there. Yaksi & Wilson give coupling coefficients rather than EPSP sizes;
  their coefficients imply ≈0.35 mV for a 40-mV eLN step, and Huang's 100-ms eLN bursts gave 0.27-2.2 mV, mean 0.93 mV.)

### 6.3 Wang, Gong, Wang, Li, Cheng, Liu, Zeng & Wang 2014, PNAS 111:3164 ([PMC3939862](https://pmc.ncbi.nlm.nih.gov/articles/PMC3939862/))

Ex vivo; optogenetic activation of whole populations (fig., approx.):
- GABAergic mlPNs (vPNs) → mPN ≈0.8 mV (shakB² ≈0.2 mV; n = 10); mPNs → mlPN ≈5 mV, ≈1.2 mV of it mecamylamine-resistant
  (n = 5); mPNs of other glomeruli → mPN via mlPNs ≈4.1 mV, ≈0.5 mV with mecamylamine or in shakB² (n = 6). Dye coupling
  mPN → mlPN in 23/29 brains.
- "the limited number of eLNs (two to three in each AL) and the low coupling efficacy between eLNs and mPNs appear to be
  insufficient to account for the strong lateral excitation ... whereas eLNs are responsible for global crosstalk, mlPNs
  provide a means for communication among selected glomeruli."

### 6.4 Root, Semmelhack, Wong, Flores & Wang 2007, PNAS 104:11826 ([PMC1913902](https://pmc.ncbi.nlm.nih.gov/articles/PMC1913902/))

Explant (brain with antennae, 113 mM Na⁺), loose-patch VM2 PN recordings, odors applied in liquid for 1 s; imaging with
airborne odor at 8% saturated vapor.
- Or43b-mutant VM2 PNs, spikes in the first second (wild type vs mutant, fig., approx.; n = 4-9): isoamyl acetate high 23.9
  vs ≈4, medium 28.9 vs <1, low 18.9 vs <1; 1-hexanol 25.4 vs ≈5, 25.4 vs ≈5, 10.2 vs ≈3. "the wild-type response was five
  to six times greater than that of the mutant" (high concentration).
- With GABA_A + GABA_B blocked (picrotoxin 125 µM, CGP54626 25 µM): "from an average of 4 to 23 spikes in the first second
  (n = 2), and from 5 ± 1 to 23 ± 9 spikes (n = 3) for hexanol, revealing a strong lateral excitatory connection ... a
  balance between opposing excitatory and inhibitory lateral interactions."
- Imaging: silenced VM2 (Or43b) and DM1 (Or42b) PN dendrites showed ≈0-4% ΔF/F while neighbors reached 40-160%. Authors:
  "our mutant results show that there is no mechanism for broadening PN tuning". They attribute the gap to Olsen 2007 to
  whole-cell vs loose patch, whole fly vs explant, gas vs liquid odor, and saline.

### 6.5 Silbering & Galizia 2007 and Silbering, Okada, Ito & Galizia 2008, J Neurosci ([PMC6673347](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673347/), [PMC6671615](https://pmc.ncbi.nlm.nih.gov/articles/PMC6671615/))

In vivo widefield G-CaMP 1.3, 1-s odors.
- 2008: "Given the absence of OSN input, PN activity in glomerulus DL5 must have been driven by lateral connections across
  glomeruli. Similar broadening effects were found in 12 of 24 odor/glomerulus combinations, although in most cases only at
  the highest concentration." DL5 with isopentyl acetate 10^-7 to 10^-2 (medians, normalized to DM2's response to 1-butanol
  10^-3; fig., approx.): PNs 0.12, 0.05, 0.10, 0.17, 0.41, 0.75; ORNs 0.13, 0.12, 0.13, 0.12, 0.05, 0.05; krasavietz LNs
  0.21, 0.21, 0.35, ≈0.57, ≈0.92, 1.23.
- krasavietz LN signals (2008): focal glomerular responses to diagnostic odors (suggesting direct ORN input); "the response
  peak was reached ~1 s after stimulus onset and calcium level returned quickly back to baseline, with no inhibitory
  responses to any odor in any glomerulus"; thresholds equal to or lower than PNs' (isopentyl acetate 10^-5; "for propionic
  acid, KRAS local neurons were more sensitive than both PNs and OSNs in most glomeruli").
- 2007: no mixture synergism; correlations between ORN input to one glomerulus and reduced mixture suppression in others,
  read as "excitatory LNs and/or a disinhibitory circuit".

### 6.6 Mohamed et al. 2019, Nat Commun 10:1201 ([PMC6416470](https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/))

Two-photon GCaMP6s in GH146 PNs, 2-s odors. With DL1 (Or10a⁻/⁻, n = 10) or DL5 (Or7a⁻/⁻, n = 12) input silenced, "Both
mutants revealed no odor-evoked PN activity in the corresponding glomerulus, indicating that lateral excitation seems not to
take place in these cases" (≈0 ΔF/F0 vs ≈7 in the intact partner; fig., approx.). Contrast Olsen 2007's DL1 spiking (§1.2)
and Silbering 2008's DL5. Mixtures of opposing valence produced glomerulus-specific lateral inhibition (DM1-DM4 only).

### 6.7 Seki, Dweck, Rybak, Wicher, Sachse & Hansson 2017, BMC Biol 15:56 ([PMC5493115](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493115/))

In vivo whole-cell, 67 PNs from 31 glomeruli, 17 odors at 10^-2 (≈10× air dilution), 1-s pulses, window 0.05-1.05 s;
ORNs by single-sensillum recording.
- "odor representation from olfactory sensory neurons to PNs is generally conserved, while transformation of odor tuning
  curves is glomerulus-dependent"; OSN-PN profile correlation "r = 0.72 ± 0.38, n = 29". Lateral excitation not invoked.
- From their Tables S2/S3 (helper agent, derived): lifetime sparseness median ORN 0.84 vs PN 0.73 (PN broader in 17/27
  glomeruli); glomerulus-odor pairs ≥20 spikes/s 115 (ORN) → 140 (PN), +22%; 10 of 235 pairs with cognate ORN ≤5 Hz had PN
  responses ≥30 spikes/s (e.g. DM4 + acetic acid 107, VC2 + benzaldehyde 98.5).

### 6.8 Models and papers checked without relevant data

- Assisi, Stopfer & Bazhenov 2012 (PLoS Comput Biol; [PMC3395596](https://pmc.ncbi.nlm.nih.gov/articles/PMC3395596/)) is a
  locust AL model (300 PNs, 100 LNs, 50 eLNs) with chemical (nicotinic) eLN→PN synapses and no gap junctions; P(eLN→PN) =
  0.1, P(PN→eLN) = 0.5; best classification at gACh 0.0002-0.0006 mS with gGABA_B 0.0002-0.0004 mS. Model choices, not
  fly measurements. Claim: "lateral excitation amplified differences between representations of similar odors by
  recruiting projection neurons that did not receive direct input from olfactory receptors. However, this increased
  sensitivity also amplified noisy variations."
- Root et al. 2008 (Neuron; [PMC2539065](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/)) is about GABA_B presynaptic gain
  control (heterogeneous across glomeruli); nothing on eLNs or lateral excitation.
- Coates et al. 2017 ([PMC5546105](https://pmc.ncbi.nlm.nih.gov/articles/PMC5546105/)) and 2020
  ([PMC7424878](https://pmc.ncbi.nlm.nih.gov/articles/PMC7424878/)) concern the serotonergic CSD neuron; neither reports shakB
  in the AL (2020: "gap junctions cannot be visualized within the EM dataset"). The papers with AL shakB data are Yaksi &
  Wilson 2010, Kazama et al. 2011, Nagel et al. 2015, Hong & Wilson 2015, Wang et al. 2014, Das et al. 2017, Shimizu &
  Stopfer 2017 and the anatomical survey of Ammer et al. 2022.
- Tootoonian & Laurent 2010 (Neuron 67:903, the preview of Huang and Yaksi): not accessible; abstract: "cholinergic
  krasavietz local interneurons are a major substrate for this spread of excitation, predominantly via electrical
  coupling."
- Fuenzalida-Uribe et al. 2025 (Front Neural Circuits; [PMC12062127](https://pmc.ncbi.nlm.nih.gov/articles/PMC12062127/)):
  GH146>Inx7-RNAi raised whole-AL vinegar responses by ≈30% (7.8 → 10.1% ΔF/F at 1% vinegar; trials pooled) and removed
  synchrony between cultured PNs. See §7.4 for why Inx7 in PNs is doubtful.

## 7. Which neurons are the eLNs? Counts, transmitters, connectome types, innexins

Sections 7.1-7.4 were compiled by a helper agent from the full texts and supplements cited (spot-checked: the Eckstein 2024
quotes). The MaleCNS tallies are from the public v1.0 flat files (local copies in ~/fly-data/raw, read only).

### 7.1 Counts and transmitter identity from staining (measured)

| source | line or population | LNs per lobe | cholinergic | GABAergic |
|---|---|---|---|---|
| Shang 2007 (antibody) | krasavietz-Gal4 | "a dozen or so" | 63.1 ± 4.7% ChAT+ (n = 9) | 39.4 ± 5.8% (n = 10) |
| Shang 2007 (Cha-dsRed reporter) | krasavietz-Gal4 | 11.6 ± 1.5 | 10.5 ± 1.4 cells (86.7%) | — |
| Shang 2007 (antibody) | KL107-Gal4 | ≈50 (plus ORNs, PNs, KCs) | 70.9 ± 6.0% | 32.6 ± 6.5% |
| Chou 2010 (antibody, Supp. Table 1) | krasavietz (Line 9) | 16 ± 4 | 2 ± 1 GABA−ChAT+ | 12 ± 3 (plus 5 ± 2 neither) |
| Chou 2010 | each of 8 LN lines | 5-103 | 0-2 GABA−ChAT+ per line | majority |
| Seki 2010 (antibody) | krasavietz | ≈15 | 6.9 ± 10.1% (n = 5); 0.8 ± 1.6% in GCaMP-labeled cells | 76.6 ± 6.0%; 94.5% |
| Seki 2010, citing Okada 2009 | NP1227 (LN1), NP2426 (LN2) | ≈18, ≈37 | — | "~95%" |
| Yaksi & Wilson 2010 (physiology) | krasavietz | — | "at least three eLNs per antennal lobe" recorded | — |

- Chou 2010: "the vast majority of LNs are GABAergic; however, there are a few cholinergic cells, and a larger minority that
  are neither"; lower bound "~100 ipsilaterally projecting and ~100 bilaterally projecting LNs for each antennal lobe"; ≈62-71
  glutamatergic LNs, mostly ventral (ALv2 lineage; Das 2011: 62.2 ± 1.4 OK371+ cells, none GABA+). Footnote: most
  krasavietz LNs being GABA+ "disagrees with a previous study [Shang et al. 2007]".
- The two GABA-negative krasavietz clones in Chou's per-cell table innervated 47 and 51 of 54 glomeruli (derived from Supp.
  Table 2). One broad Line 9 LN "was mainly inhibited by all odors"; a sparser one "was excited by all odors" (Fig. 4b).
- Nagel & Wilson 2016: "Within each antennal lobe, ∼50 GABAergic LNs express Gal4 [NP3056], whereas the remaining ∼50
  GABAergic LNs do not".
- Liou et al. 2018 (Nat Commun; [PMC5993751](https://pmc.ncbi.nlm.nih.gov/articles/PMC5993751/)): several LN Gal4 lines
  label only GABA-negative LNs (1-3 per lobe; e.g. IS-68 2.75, IS-351 3.0 per lobe); "the neurotransmitter identities of
  these neurons are currently unknown". No ChAT or innexin staining.
- Das et al. 2008 (Neural Dev): NP1227 and NP2426 LNs mostly GABA+, with "A few cells expressing Cha-dsRed". They place
  krasavietz, KL78 and KL107 LN somata "lateral or dorsolateral to the antennal lobe", at odds with Huang's ventral KL107
  eLNs.
- So the physiologically defined eLNs are few (a handful to ≈10 per lobe), broad, with lateral/ventrolateral somata. The
  staining studies disagree on how many krasavietz cells they are.

### 7.2 Connectome types (hemibrain, FlyWire, MaleCNS)

- Single-glomerulus EM: Tobin, Wilson & Lee 2017 (DM6, FAFB; [PMC5440167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/))
  did not type LNs ("Most of these profiles are probably inhibitory local neurons"); PNs get "~75%" of input synapses from
  ORNs and "~20%" from multiglomerular neurons. Horne et al. 2018 (VA1v; [PMC6234030](https://pmc.ncbi.nlm.nih.gov/articles/PMC6234030/))
  found 56 LNs in VA1v (LN1 17, LN2L 24, others 1-4 each), treated them as GABAergic or glutamatergic, and identified no
  eLN; LN output was 27.8% of VA1v synapses (10.4% onto PNs).
- Schlegel 2021 (hemibrain, right AL): "196 ALLNs ... 5 lineages, 4 morphological classes, 25 anatomical groups and 74 cell
  types". No transmitters assigned. lLN1 (16, broad; = Tanaka LN1, i.e. NP1227), lLN2T (16, broad, "Tortuous"), lLN2P (14,
  patchy), v2LN3A/B (7, regional bilateral; = Tanaka LN3), v2LN4 (3), il3LN6 (2, keystone).
- Eckstein et al. 2024 (machine-learning transmitter predictions; ALLNs were not in their ground truth):
  - "Surprisingly, 18%–27% of antennal lobe local neurons may be cholinergic, suggesting that lateral excitation is a more
    prominent feature of antennal lobe processing than previously thought."
  - ALl1 dorsal hemilineage, FlyWire: "∼ 126 local neurons per hemisphere"; predicted "143 (left: 74, right: 69) ...
    GABAergic, 48 (left: 20, right: 28) cholinergic, 13 ... dopaminergic, 14 ... glutamatergic and 37 ... serotonergic";
    expected from the literature "perhaps as many as ∼ 15 cholinergic local neurons".
  - "The predicted cholinergic neurons are unilateral and 'broad', i.e., pan-glomerular, in accordance with previous
    descriptions [Shang 2007; Huang 2010] but more numerous." Some lLN1_bc were predicted dopaminergic, suspected to be
    cholinergic. "∼ 13 lLN2T_abc neurons ... have a cell body placement and general morphology most similar to reported
    cholinergic local neurons" (these were mispredicted serotonergic).
  - Patchy lLN2P_a predicted glutamatergic, lLN2P_b/c GABAergic.
  - ALv2: "133 (left: 67, right: 66) glutamatergic neurons alongside a newly identified sub-population of 28 (left: 14,
    right: 16) potential cholinergic neurons"; "specific lateral excitation between glomeruli on different sides of the brain
    should be possible."
- FlyWire annotations (v3.x): 429 ALLNs; ML top transmitter Glu 148, GABA 147, ACh 80, 5-HT 40, DA 12. The literature field
  "acetylcholine (Shang et al., 2007 (immuno))" is attached to lLN1_bc (30), lLN2T_b (4), lLN2T_c (4), lLN2X03 (6) — a
  morphology-based assignment, not staining of these types. lLN2P_b is "gaba, MIP; acetylcholine-negative".
- MaleCNS v1.0 (derived tallies): 420 ALLNs; consensus transmitter ACh 137 (left 70, right 67), GABA 115, Glu 99, unclear 67.
  ALl1 dorsal ACh 50/49 per side, ALv2 ACh 20/18. The `ground_truth` column lists ACh for lLN1_bc (30), lLN2T_a (5),
  lLN2T_b (4), lLN2T_c (4), lLN2X05 (4) (same literature mapping).
- **Conflict.** hemibrain lLN1/lLN2 are named for Tanaka's LN1 (NP1227) and LN2 (NP2426) lines, which are ≈95%
  GABA-immunoreactive (Seki 2010, Okada 2009). The ACh label on lLN1_bc rests on a morphology match.
- **Size of the chemical cholinergic-LN input in MaleCNS** (derived): of 984,247 synapses onto all 284 uniglomerular PNs,
  ORNs give 43.1%, consensus-ACh ALLNs 16.7% (164,178), GABA ALLNs 9.0%, Glu ALLNs 1.0%. lLN1_bc alone gives 64,769 (6.6%).
  Each lLN1_bc neuron gets little ORN input (≈262 synapses) and much uPN input (≈2,689).

### 7.3 Best candidates for the physiological eLNs (helper agent's mapping; hypotheses)

- **krasavietz type I eLNs** (cholinergic, 8-11 per lobe, lateral/ventrolateral somata, unilateral, broad, sparing DA1/DL3,
  contact "most or all PNs", bursting):
  - Literature-matched: lLN1_bc (15 per side) and lLN2T_a/lLN2X05, lLN2T_b, lLN2T_c (≈8-9 per side). Each contacts 69-83%
    of ipsilateral uPNs at ≥5 synapses (derived). Against: LN1/LN2 lines are GABAergic by staining; FlyWire ML calls these
    types DA/5-HT.
  - ML-only ACh, broad, unilateral: lLN2X12 (5-6 per side), lLN2X11 (2), lLN2X04 (2), lLN2T_e (2), lLN1_a (1).
  - DA1/DL3-sparing (relative synapse share in DA1/DL3 vs the ALLN average, derived): lLN2X05 0.26/0.00, lLN2X11 0.14/0.09,
    lLN2X12 0.28/0.22, lLN1_a 0.30/0.01; lLN1_bc 0.49/0.42; lLN2T_b/c/e none. The subset lLN2X12 + lLN2X11 + lLN2X05 +
    lLN1_a (≈10-11 per side) fits both Huang's DA1/DL3 sparing and Shang's count. Hypothesis only.
- **KL107 ventral eLNs** (sparse arbors, "many but not all glomeruli", restricted PN connections): no published match.
  Candidates are the ALv2 consensus-ACh types (18-20 per side), e.g. v2LN3A1_b (4-5 per side, regional bilateral, 23-28
  glomeruli), vLN24 (2), and sparse thermo-/hygrosensory types (v2LN4, v2LN5, v2LN33, v2LN38, v2LN34C/F). They contact only
  0-14% of ipsilateral uPNs (derived).
- Not candidates: patchy lLN2P (GABA or Glu; not in krasavietz), il3LN6 (GABA), lLN8, lLN2F, lLN2R_a and most CB-named
  lateral types (GABA).
- brainfly check (read only): odor_probe14.py's regex `^(lLN|il\dLN|v\dLN|vLN\d|lvLN|l\dLN|LN\d)` selects 120 consensus-ACh
  ALLNs; it misses CB3202 (5), CB2908 (4), CB3679 (1) and 7 untyped consensus-ACh ALLNs, whose synapses onto uPNs (2,879
  from the CB types, plus the untyped ones) stay as chemical excitation (helper agent, derived).

### 7.4 ShakB and other innexins

- Ammer, Vieira, Fendl & Borst 2022 (Curr Biol; immunostaining of all eight innexins): "shakB is the only innexin that is
  widely expressed in many neurons of the brain and VNC"; ogre, inx2, inx3 are glial; "We did not detect zpg and inx7
  protein". Antennal lobe: "weaker expression in the antennal lobes" than in AMMC, wedge, giant fiber etc. AL cell types not
  identified.
- Yaksi & Wilson 2010: shakB transcripts in pooled GH146 PN somata (RT-PCR). Re-analysis of Li et al. 2017 PN single-cell
  RNA-seq (helper agent, derived): shakB detected (CPM > 10) in 89% of GH146+ PNs at 24 h APF and 76% of adult Mz19+ PNs
  (median CPM 55); Inx7 in ≤2% of PNs; Inx5, Inx6, zpg absent. No LN innexin data found in any dataset searched.
- Fuenzalida-Uribe et al. 2025 (Front Neural Circuits) report Inx7 in PNs (GH146>Inx7-RNAi abolished synchrony between
  cultured PNs). This conflicts with Ammer 2022 and the transcriptome; treat as unconfirmed.
- Das et al. 2017 rescued food-odor synergy in DA1 by expressing shakB in "Krasavietz-positive eLNs and GH146-positive PNs"
  in shakB² (§6.1), so ShakB is needed in PNs and/or eLNs.
- Horne 2018 (VA1v FIB-SEM): "unable to annotate appositions that we could reliably interpret as putative gap junctions".
  EM connectomes therefore cannot locate eLN-PN junctions; chemical contacts are only a proxy.

## 8. Derived: turning the measurements into a spike-triggered kick

All of this is my arithmetic (derived) on the numbers above. brainfly's electrical synapse "raises each of its electrical
partners ... by gw mV at once (no delay, no depression)" (brainfly/hybrid.py); the jump then decays with the partner's
membrane time constant. brainfly's PN LIF uses τm = 20 ms (pn_ln_dynamics.md).

### 8.1 eLN → PN, one spike

- Measured directly (Huang Fig. 3K): mean STA peak 0.42 mV (median 0.36, range 0.16-0.72; n = 12; explant; somatic).
- Shape (example pair, Fig. 3E): area over −40 to +100 ms = 51 ms × peak; decay τ ≈ 30 ms after the peak; ≈60% of the peak
  is reached before the spike, from subthreshold coupling during the current step that evoked the spike.
- Area for the mean pair ≈ 0.42 × 51 ≈ 21 mV·ms.
- Candidate gw values:

  | matching criterion | gw (mV per eLN spike, per PN) | comment |
  |---|---|---|
  | spike-locked part only | ≈0.17 (0.06-0.29) | leaves out the eLN's subthreshold depolarization, which the model cannot transmit |
  | STA peak | ≈0.42 (0.16-0.72) | the kick decays faster (20 ms) than the STA (30 ms), so less charge per spike |
  | STA area, τm = 20 ms | ≈1.05 (0.4-1.8) | same time-integral of depolarization per spike, pre-spike part included |
  | 100-ms eLN burst of ≈5 spikes → 0.93 mV (Fig. 2) | ≈0.55 | peak after 5 kicks 16-20 ms apart = gw × 1.6-1.8 |
  | same burst, minus subthreshold coupling | ≈0.3 | the step holds the eLN ≈30 mV above rest; × 0.015 ≈ 0.45 mV of the 0.93 mV is DC coupling |

- Measured bounds: ≈0.17 mV (spike-locked part) to ≈1 mV (all charge per spike).
- In vivo vs explant: the in vivo eLN→PN coefficient (0.0073-0.0087 with spikes; Yaksi, Kazama 2011) is ≈0.5-0.6× the
  explant subthreshold value (0.015, Huang). Scaling by 0.55 gives gw ≈ 0.1-0.6 mV for an in vivo PN soma.
- An indirect estimate from somatic coefficients × eLN spike area (helper agent: 0.002-0.007 × 40-80 mV·ms / 5-20 ms) gives
  only 0.004-0.11 mV per spike, an order of magnitude below the directly measured STA. The STA is the better basis.
- Somatic numbers understate coupling at the junction and at the spike initiation zone (Yaksi's caveat); whether the spike
  initiation zone sees more is not known.

### 8.2 Population checks against odor-evoked lateral excitation

- For N coupled eLNs, each firing at rate r and delivering area A per spike, the mean lateral depolarization is ≈ N·r·A
  (linear superposition, no saturation).
- Kazama, Yaksi & Wilson 2011 (acute, palp odors, one preparation): eLNs fired 5.6-11.2 Hz over 100-600 ms and antennal PNs
  depolarized by 1.4-3.1 mV. With A = 21 mV·ms and N = 10, r = 8 Hz predicts 10 × 8 × 0.021 ≈ 1.7 mV. The full-charge kick
  (≈1 mV at τm = 20 ms) with ≈10 eLNs matches without fitting.
- Yaksi Fig. 7 (VC1/VC2, antennal odors): 2.4-3.6 mV needs N·r ≈ 140 spikes/s per PN, e.g. 10 eLNs at 14 Hz. Huang's
  example eLN fired ≈20-35 Hz to preferred odors; type I cells burst at ≈60 Hz initially.
- With only the spike-locked area (≈5 mV·ms), N·r ≈ 400-600 spikes/s, i.e. 40-60 Hz per eLN for 10 eLNs: more than measured.
  The eLN's odor-evoked depolarization (≈5-8 mV peak, spikes filtered; Yaksi Fig. 3D) would add only ≈0.05-0.07 mV per eLN
  through the somatic coefficient. So either the junction delivers more than the spike-locked part, or more than 10 eLNs
  couple to each PN.
- If the model couples more cells, gw per pair must shrink. Keeping ≈2 mV at 8 Hz: N = 30 (the broad lateral cholinergic
  candidates per side, §7.3) needs A ≈ 8 mV·ms, gw ≈ 0.4 mV; N = 68 (all MaleCNS consensus-ACh ALLNs per side) needs A ≈ 4
  mV·ms, gw ≈ 0.2 mV.
- Practical rule: choose the coupled set (§7.3), then fit one gw inside 0.17-1 mV so that the model reproduces the
  deafferentation tests (T1, T5, T13 in §9) with the model's own eLN rates; hold out the rest.

### 8.3 Saturation must come from eLN firing, not from the junction

- Lateral depolarization is half-maximal at ≈7-10 spikes/s of input from one ORN type and changes little from 50 to 150
  spikes/s (Olsen Fig. 6). Five odors spanning a ≥7-fold range of antennal LFP gave lateral excitation within ±10% (Yaksi
  Fig. 3). Electrical coupling is linear in presynaptic voltage, so the model's eLNs themselves must saturate: high
  sensitivity to weak ORN input (eLN EPSCs ≈4× PN EPSCs for the same weak nerve stimulus, Huang Fig. S5) and a ceiling on
  firing (eLNs are "barraged by spontaneous IPSPs"; Kazama 2011's acute eLN rates were only 4-11 Hz).

### 8.4 Other electrical partners, if added

- PN → eLN: depolarizing transmission is ≈85% nicotinic (Cd²⁺ and three antagonists, Yaksi) and already present in the
  connectome as chemical synapses. The electrical part (hyperpolarizing coefficient 0.004-0.010) is 0.5-1.5× the eLN→PN
  hyperpolarizing value; PN→eLN STA mean 0.21 mV (≈43% before the spike). A PN→eLN kick of ≈0.1 mV on top of the chemical
  synapses fits.
- eLN ↔ eLN: coupling 0.025-0.027, STA 0.59-1.01 mV (Huang). The strongest electrical link measured in the AL; it would
  synchronize eLNs.
- Sister PN ↔ PN: 0.018 / 0.0077 (DA1, Yaksi); 0.035 / 0.0136, of which ≈0.011-0.016 is Cd²⁺-resistant (DM6, Kazama &
  Wilson 2009). Removing it cut DA1 cVA responses by ≈30-40% (Yaksi). Heterotypic PN pairs: negligible.
- eLN → iLN: 0.012-0.017 depolarizing, 84% Cd²⁺-sensitive (Yaksi); Huang found these connections rare. Keeping the
  connectome's cholinergic LN → GABAergic LN synapses chemical matches Yaksi.
- Constraint: heterotypic PN spike-count correlations are only 0.004 (spontaneous) to 0.015 (odor) (Kazama & Wilson 2009).
  An eLN network strong enough to synchronize PNs across glomeruli would violate this.

### 8.5 Glomerulus-specific strength

- Lateral depolarization varies ≈2.4-fold across glomeruli (VC4 3.03 to DM6 1.26 mV·s, Olsen Fig. 8C); DM1 receives much
  less (Yaksi); VC3 and VM5v keep large lateral excitation without shakB (Shimizu & Stopfer). The ordering is stereotyped
  and unrelated to distance, sensillum class, ORN tuning or input resistance. A model could scale gw per glomerulus (e.g. by
  eLN arbor or synapse density in that glomerulus) and test the Olsen Fig. 8C ordering as a held-out check.

## 9. Held-out tests

Each row is a published measurement the model can be run against. Suggested split: fit gw to T1, T5 and T13; hold out the
rest.

| # | manipulation in the model | measured result | source |
|---|---|---|---|
| T1 | Silence all antennal ORNs; palp odors (ethyl butyrate, 2-heptanone, benzaldehyde, 1:100) | antennal PNs: no spontaneous activity; depolarization peak 6.3-7.5 mV at ≈125-175 ms, 2.4-3.9 mV at 500 ms (n = 6, spikes filtered) | Olsen 2007 Fig. 1G |
| T2 | Only VA7l ORNs active, graded rates | area (100-600 ms) vs VA7l rate: half-max ≈7 spikes/s, plateau ≈1.9 mV·s; per glomerulus VC4 3.03 ... DM6 1.26 mV·s (§1.3) | Olsen 2007 Figs. 6, 8 |
| T3 | Only VM7 ORNs active | half-max ≈10 spikes/s, plateau ≈0.9 mV·s; DL5 1.31, DM6 0.76, VM2 0.74 mV·s | Olsen 2007 Figs. 6, 8 |
| T4 | VM7 and VA7l ORNs together vs alone | 0.93 and 1.33 alone, 1.54 together (68% of the sum) | Olsen 2007 Fig. 7 |
| T5 | Silence palp ORNs, antennal odors: VC1/VC2 PNs; silence antennal ORNs, palp odors: DM1 PNs | VC1/VC2 2.4-3.3 mV (100-300 ms), peaks 3.7-4.9 mV, near-equal for 5 odors spanning a ≥7-fold LFP range; DM1 0.1-1.1 mV | Yaksi 2010 Figs. 3, 7 |
| T6 | T5 without eLN→PN electrical synapses | VC1/VC2 −1.2 to −1.35 mV for ethyl acetate and pentyl acetate, ≈0 for the others; DM1 −0.8 / −0.3 / ≈0 | Yaksi 2010 Fig. 7 |
| T7 | Silence VM2 (Or43b) or DL1 (Or10a) ORNs; 13 odors at 1:100 | VM2 PNs 6-32 spikes/s (mean 16.7), DL1 5-26 (13.2), every odor positive; uncorrelated with wild-type tuning (r² < 0.05); VM2 vs DL1 r² = 0.31 | Olsen 2007 Fig. 4 |
| T8 | Remove all electrical synapses, intact model | VC1 fenchone 10^-2/10^-4/10^-6: 172/124/42 → 124/68/20 spikes/s; VC2 fenchone 10^-2 51 → 7, cyclohexanone 10^-2 77 → 4, 4-methylphenol 10^-2 98 → 146, 10^-3 61 → 132; DA1 cVA 1X 119 → 71-85, 10^-2 69 → 40; DM1 unchanged | Yaksi 2010 Figs. 8, 9 |
| T9 | T8 with antennal ORNs silenced (fenchone private to VC1) | no change (fenchone 10^-2 ≈244 vs ≈229; 10^-4 ≈146 vs ≈165 spikes/s) | Yaksi 2010 Fig. 8E |
| T10 | Depolarize krasavietz-like LNs for 500 ms | PN +1.5 mV peak at ≈70 ms, ≈0 by 500 ms, −1.1 mV after offset; with chemical synapses blocked +1.0 mV sustained | Yaksi 2010 Fig. 1 |
| T11 | Silence DM2 ORNs; 4 odors, 2 s, 0.1% saturated vapor | DM2 PN output (spH) 32-93% of wild type | Shang 2007 |
| T12 | eLN responses | odor depolarization ≈7-10 mV peak, similar across odors; EPSC to weak nerve stimulation ≈4× the PN's; latency ≈2 ms | Yaksi 2010, Huang 2010 |
| T13 | Acute deafferentation (Kazama protocol) | VM2 PNs, palp odors: pentyl acetate 2.5, ethyl acetate 1.8, methyl salicylate 1.4 mV; VM7 PNs, antennal odors: 4.9, 5.1, 3.9 mV; eLN rates 5.6-11.2 Hz; Or43b-mutant VM2 PNs not different from controls | Kazama 2011 |
| T14 | Silence all antennal ORNs; record palp PNs (VM7, VC1) to 20 palp odors | responses increase for 18/20 (VM7) and 13/20 (VC1) odors, none decrease; lifetime sparseness 0.47 → 0.26 and 0.57 → 0.25 | Olsen & Wilson 2008 |
| T15 | Intact model; odors that barely drive VM7 or DL5 ORNs | net PN response −2.5 to +9 Hz (500 ms); a public odor suppresses a fixed private response (VM7 2-butanone 10^-6: 77 → 52 → 37 → 17 → 9 Hz with pentyl acetate 0 to 10^-3) | Olsen 2010 |
| T16 | T1-like deafferentation without shakB | DA1/VA5-lineage PNs 5.7-6.2 → 0.5-0.8 mV peak; VC3 and VM5v unchanged | Shimizu & Stopfer 2017 |
| T17 | cVA + vinegar (equal concentrations) vs cVA alone | DA1 PN Ca²⁺ 1.4-1.75× the linear sum at 10^-2 and 10^-1, none at 10^-3; no change in Or67d ORNs; abolished without shakB | Das 2017 |
| T18 | DM4 dilution series (1:1,000 to 1:100,000) | at 1:100,000 DM4 ORNs answer only 2,3-butanedione (≈24 Hz) and ethyl acetate (≈21 Hz), DM4 PNs answer those (37, 61 Hz) and five more odors (9-23 Hz) | Bhandawat 2007 Fig. 4 |
| T19 | Spontaneous and odor activity, PN pairs | heterotypic spike-count correlation 0.004 (spontaneous), 0.015 (odor); homotypic 0.14, 0.20 | Kazama & Wilson 2009 |

## 10. What this means for brainfly's antennal lobe (my reading)

These are inferences, not measurements. They compare the fly data with what odor_probe12/14 report for the model.

- **Size.** Lateral excitation onto a PN with no ORN input is a few mV in flies: 1.4-7.5 mV across acute deafferentation
  studies, 0.1-1.1 mV in DM1, up to ≈13-16 mV (shakB-independent) in VC3. Spiking from it alone is 5-32 spikes/s averaged
  over 500 ms (Olsen's receptor mutants) and up to 50-80 spikes/s (VC2, intact fly). Odor-evoked lateral current in one
  voltage-clamped PN was ≈33 pA at peak and ≈7 pA sustained (Olsen & Wilson 2008), against ≈29 pA for a single ORN spike's
  unitary EPSC (Kazama & Wilson 2008).
- **Time course.** Lateral depolarization starts with the direct response (≈1.5 ms later after nerve stimulation), peaks
  120-300 ms after valve opening, holds at 60-90% of peak in VC1/VC2 to odor offset, and undershoots by ≈1-3 mV after. The
  model's old chemical route (152,952 synapses; odor_probe14) gave a 100-ms onset rise of +16-26 Hz in undriven glomeruli
  and "hardly at all over the whole 0.5 s". The magnitude is in the fly range, but the shape is wrong: in flies lateral
  excitation is moderate and sustained.
- **Net sign in an intact circuit.** In intact flies the net effect of lateral input on PN spiking is usually inhibitory
  (Olsen & Wilson 2008: removing antennae raised most palp-PN responses and none fell; Olsen 2010: "the net effect of lateral
  input was always inhibitory"), and odors that do not drive a PN's ORNs give near-zero net responses (−2.5 to +9 Hz). The
  excitation is real (shakB² cuts VC1 responses by a third) but is usually outweighed by lateral inhibition. A model that
  adds eLN coupling should still pass T14 and T15.
- **Breadth and weak odors.** Broad PN tuning does not need lateral input ("lateral excitation is not strictly necessary";
  tuning got broader when lateral input was removed, Olsen & Wilson 2008). In flies it comes mainly from the steep
  ORN→PN transform (short-term depression; Kazama & Wilson 2008, Wilson 2013). So eLN coupling is unlikely to fix the model's
  too-high σ (23-34 vs 12-16 spikes/s) or its 30-43% responding fraction on its own. The fly property that favors weak odors
  is that the eLN pathway saturates at low input (half-maximal at ≈7-10 ORN spikes/s in one ORN type; equal for odors
  spanning a ≥7-fold range of ORN activity), so a few mV of nearly odor-independent depolarization adds proportionally more
  to weak responses. Single-glomerulus evidence is mixed: removing electrical synapses cut VC1's fenchone 10^-6 response by
  ≈52% (n.s.) vs 28% at 10^-2, but raised VC2's responses to 10^-6 odors (≈11 → 20 spikes/s).
- **Inhibition coupled to it.** shakB² also removed eLN→iLN drive (VC2 4-methylphenol responses doubled; GABA antagonists
  disinhibited less). If the model keeps cholinergic LN → GABAergic LN chemical synapses, adding eLN→PN coupling should not
  change inhibition by itself.
- **Which neurons.** Physiological eLNs are few (2-3 or more recorded per lobe; 2 ± 1 to ≈10 krasavietz cholinergic cells
  by staining), broad, with lateral/ventrolateral somata. MaleCNS labels 137 ALLNs cholinergic (≈68 per side), led by lLN1_bc
  (15 per side), whose ACh label rests on a morphology match. Coupling all of them to all PNs at a per-pair gw from paired
  recordings would overshoot; scale gw to the number coupled (§8.2). odor_probe14's regex left 17 consensus-ACh ALLNs'
  chemical synapses onto uPNs in place (§7.3).
- **Imaging disagrees.** Ca²⁺ imaging found no lateral PN signal in silenced VM2, DM1, DL1 or DL5 glomeruli (Root 2007,
  Mohamed 2019), while electrophysiology finds a few mV and 5-30 spikes/s. Imaging is probably insensitive at this level, so
  imaging-based held-out tests should not be expected to show lateral responses.

## 11. Sources

Primary papers read in full (or as stated):
- Olsen SR, Bhandawat V, Wilson RI (2007). Excitatory interactions between olfactory processing channels in the Drosophila
  antennal lobe. Neuron 54:89-103. https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/ (PDF and supplement via PMC).
- Yaksi E, Wilson RI (2010). Electrical coupling between olfactory glomeruli. Neuron 67:1034-1047.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/ ; figures https://ars.els-cdn.com/content/image/1-s2.0-S0896627310006847-gr4_lrg.jpg
  (gr1-gr9); supplement https://ars.els-cdn.com/content/image/1-s2.0-S0896627310006847-mmc1.pdf
- Huang J, Zhang W, Qiao W, Hu A, Wang Z (2010). Functional connectivity and selective odor responses of excitatory local
  interneurons in Drosophila antennal lobe. Neuron 67:1021-1033. https://doi.org/10.1016/j.neuron.2010.08.025 ; text
  http://web.archive.org/web/20220701025509/https://www.cell.com/neuron/fulltext/S0896-6273(10)00635-5 ; figures
  https://ars.els-cdn.com/content/image/1-s2.0-S0896627310006355-gr3_lrg.jpg (gr1-gr7); supplement
  https://ars.els-cdn.com/content/image/1-s2.0-S0896627310006355-mmc1.pdf ; abstract https://pubmed.ncbi.nlm.nih.gov/20869598/
- Shang Y, Claridge-Chang A, Sjulson L, Pypaert M, Miesenböck G (2007). Excitatory local circuits and their implications for
  olfactory processing in the fly antennal lobe. Cell 128:601-612. https://pmc.ncbi.nlm.nih.gov/articles/PMC2866183/
- Kazama H, Wilson RI (2008). Homeostatic matching and nonlinear amplification at identified central synapses. Neuron
  58:401-413. https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/
- Kazama H, Wilson RI (2009). Origins of correlated activity in an olfactory circuit. Nat Neurosci 12:1136-1144.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/
- Kazama H, Yaksi E, Wilson RI (2011). Cell death triggers olfactory circuit plasticity via glial signaling in Drosophila. J
  Neurosci 31:7619-7630. https://pmc.ncbi.nlm.nih.gov/articles/PMC3119471/
- Olsen SR, Wilson RI (2008). Lateral presynaptic inhibition mediates gain control in an olfactory circuit. Nature
  452:956-960. https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/
- Olsen SR, Bhandawat V, Wilson RI (2010). Divisive normalization in olfactory population codes. Neuron 66:287-299.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/
- Bhandawat V, Olsen SR, Gouwens NW, Schlief ML, Wilson RI (2007). Sensory processing in the Drosophila antennal lobe
  increases reliability and separability of ensemble odor representations. Nat Neurosci 10:1474-1482.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/
- Nagel KI, Hong EJ, Wilson RI (2015). Synaptic and circuit mechanisms promoting broadband transmission of olfactory stimulus
  dynamics. Nat Neurosci 18:56-65. https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/
- Hong EJ, Wilson RI (2015). Simultaneous encoding of odors by channels with diverse sensitivity to inhibition. Neuron
  85:573-589. https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/
- Nagel KI, Wilson RI (2016). Mechanisms underlying population response dynamics in inhibitory interneurons of the
  Drosophila antennal lobe. J Neurosci 36:4325-4338. https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/
- Wilson RI (2013). Early olfactory processing in Drosophila: mechanisms and principles. Annu Rev Neurosci 36:217-241.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/
- Das S, Trona F, Khallaf MA, Schuh E, Knaden M, Hansson BS, Sachse S (2017). Electrical synapses mediate synergism between
  pheromone and food odors in Drosophila melanogaster. PNAS 114:E9962-E9971. https://pmc.ncbi.nlm.nih.gov/articles/PMC5699073/
- Shimizu K, Stopfer M (2017). A population of projection neurons that inhibits the lateral horn but excites the antennal
  lobe through chemical synapses in Drosophila. Front Neural Circuits 11:30. https://pmc.ncbi.nlm.nih.gov/articles/PMC5413558/
- Wang K, Gong J, Wang Q, Li H, Cheng Q, Liu Y, Zeng S, Wang Z (2014). Parallel pathways convey olfactory information with
  opposite polarities in Drosophila. PNAS 111:3164-3169. https://pmc.ncbi.nlm.nih.gov/articles/PMC3939862/
- Root CM, Semmelhack JL, Wong AM, Flores J, Wang JW (2007). Propagation of olfactory information in Drosophila. PNAS
  104:11826-11831. https://pmc.ncbi.nlm.nih.gov/articles/PMC1913902/
- Root CM, Masuyama K, Green DS, et al. (2008). A presynaptic gain control mechanism fine-tunes olfactory behavior. Neuron
  59:311-321. https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/
- Silbering AF, Galizia CG (2007). Processing of odor mixtures in the Drosophila antennal lobe reveals both global inhibition
  and glomerulus-specific interactions. J Neurosci 27:11966-11977. https://pmc.ncbi.nlm.nih.gov/articles/PMC6673347/
- Silbering AF, Okada R, Ito K, Galizia CG (2008). Olfactory information processing in the Drosophila antennal lobe:
  anything goes? J Neurosci 28:13075-13087. https://pmc.ncbi.nlm.nih.gov/articles/PMC6671615/
- Mohamed AAM, Retzke T, Das Chakraborty S, et al. (2019). Odor mixtures of opposing valence unveil inter-glomerular crosstalk
  in the Drosophila antennal lobe. Nat Commun 10:1201. https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/
- Seki Y, Dweck HKM, Rybak J, Wicher D, Sachse S, Hansson BS (2017). Olfactory coding from the periphery to higher brain
  centers in the Drosophila brain. BMC Biol 15:56. https://pmc.ncbi.nlm.nih.gov/articles/PMC5493115/
- Assisi C, Stopfer M, Bazhenov M (2012). Excitatory local interneurons enhance tuning of sensory information. PLoS Comput
  Biol 8:e1002563. https://pmc.ncbi.nlm.nih.gov/articles/PMC3395596/
- Fuenzalida-Uribe N, et al. (2025). Front Neural Circuits 19:1563401. https://pmc.ncbi.nlm.nih.gov/articles/PMC12062127/
- Tootoonian S, Laurent G (2010). Electric times in olfaction. Neuron 67:903-905 (abstract only).

Cell identity, connectome and innexins:
- Chou YH, Spletter ML, Yaksi E, Leong JC, Wilson RI, Luo L (2010). Diversity and wiring variability of olfactory local
  interneuron types in the Drosophila antennal lobe. Nat Neurosci 13:439-449. https://pmc.ncbi.nlm.nih.gov/articles/PMC2847188/
- Seki Y, Rybak J, Wicher D, Sachse S, Hansson BS (2010). Physiological and morphological characterization of local
  interneurons in the Drosophila antennal lobe. J Neurophysiol 104:1007-1019. https://journals.physiology.org/doi/full/10.1152/jn.00249.2010
  (read via a Wayback capture)
- Liou NF, Lin SH, Chen YJ, et al. (2018). Diverse populations of local interneurons integrate into the Drosophila adult
  olfactory circuit. Nat Commun 9:2232. https://pmc.ncbi.nlm.nih.gov/articles/PMC5993751/
- Das A, Chiang A, Davla S, et al. (2011). Identification and analysis of a glutamatergic local interneuron lineage in the
  adult Drosophila olfactory system. Neural Syst Circuits 1:4. https://pmc.ncbi.nlm.nih.gov/articles/PMC3257541/ ; Das A,
  Sen S, Lichtneckert R, et al. (2008). Neural Dev 3:33. https://pmc.ncbi.nlm.nih.gov/articles/PMC2647541/
- Tobin WF, Wilson RI, Lee WCA (2017). Wiring variations that enable and constrain neural computation in a sensory
  microcircuit. eLife 6:e24838. https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/
- Horne JA, Langille C, McLin S, et al. (2018). A resource for the Drosophila antennal lobe provided by the connectome of
  glomerulus VA1v. eLife 7:e37550. https://pmc.ncbi.nlm.nih.gov/articles/PMC6234030/
- Schlegel P, Bates AS, Stürner T, et al. (2021). Information flow, cell types and stereotypy in a full olfactory
  connectome. eLife 10:e66018. https://pmc.ncbi.nlm.nih.gov/articles/PMC8298098/ ; data
  https://github.com/flyconnectome/hemibrain_olf_data
- Eckstein N, Bates AS, Champion A, et al. (2024). Neurotransmitter classification from electron microscopy images at
  synaptic sites in Drosophila melanogaster. Cell 187:2574-2594. https://pmc.ncbi.nlm.nih.gov/articles/PMC11106717/
- FlyWire annotations: https://github.com/flyconnectome/flywire_annotations
- MaleCNS v1.0 flat files: https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/ (Berg et al.
  2025, bioRxiv https://doi.org/10.1101/2025.10.09.680999; text not accessed)
- Ammer G, Vieira RM, Fendl S, Borst A (2022). Anatomical distribution and functional roles of electrical synapses in
  Drosophila. Curr Biol 32:2022-2036. https://doi.org/10.1016/j.cub.2022.03.040
- Li H, Horns F, Wu B, et al. (2017). Classifying Drosophila olfactory projection neuron subtypes by single-cell RNA
  sequencing. Cell 171:1206-1220. https://pmc.ncbi.nlm.nih.gov/articles/PMC6095479/ (GEO GSE100058; re-analyzed for innexins)
