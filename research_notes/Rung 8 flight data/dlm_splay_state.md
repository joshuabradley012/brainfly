# DLM motor neurons MN1–5: the splay state, its electrical coupling and its drive

Read 2026-10-11. Groundwork for a pre-registered rung 8 test: given unpatterned drive, do brainfly's DLM motor neurons,
coupled by weak electrical synapses, fire in flies' splay state, and does removing the coupling make them more
synchronous, as shakB knockdown does? GF/PSI→DLMn escape wiring is in
`../Embodied fly connectome simulation/escape_circuit.md` and is not repeated here.

## Summary: what a model test should use

1. **Drive and rates.** One shared, unpatterned excitatory (cholinergic) drive. Within a fly all 5 MNs fire at the same mean rate: 4.5–8.0 Hz per fly (n = 8). Across 100 flies MN5 ran 5.8 ± 1.9 Hz (3.0–13.2). ISI CV 0.22 ± 0.07. MN5 runs −2% to +26% relative to MN1–4 (median ×1.10, [SD]); the difference was n.s. in 41 flies.
2. **Coupling must be imposed: no connectome shows gap junctions.** It is bidirectional, non-rectifying and ShakB-dependent. CC(MN1–2, MN3–4) = 0.023 ± 0.003 (6 pairs). CC(other MN1–4 pairs) = 0.011 ± 0.003 (10 pairs; only 1–3, 1–4 and 2–3 were sampled). MN5's coupling was never measured.
3. **What CC means.** CC = peak post/peak pre for 20 ms steps. The spike AHP passes with CC 0.042, the overshoot with 0.01. Hürkey's model used couplings 2.3–2.5× weaker: CC 0.010 / 0.0044 / 0.0031 for strong / weak / MN5 pairs ([D]).
4. **Intrinsic targets.** Rest ≈ −60 mV (source traces: −52 to −66, median −58). f–I is roughly linear over 2–30 Hz: ≈62 Hz/nA on the Fig. 1e mean (0.1–0.5 nA), 75 Hz/nA per-cell median [D]. Rheobase is 0.1–0.4 nA (median 0.3), saturating near 40 Hz at 1 nA. Rin is 49–148 MΩ ([D], includes series error); MN5's published Rin is 97 ± 31 MΩ. τm, threshold and the AHP were not reported ([D] estimates in §2.8–2.9).
5. **Splayness (Hürkey's code; N = 5).** Controls 0.76 ± 0.02 (0.73–0.79, n = 8). Independent phases give 0.59. Two shakB-RNAi flies gave 0.52 and 0.69.
6. **Order of MN1–4, controls (sliding 4-spike windows, n = 8, medians).** 1423 = 35.6%, 1324 = 21.9%, the other four orders 4.8–7.1%, rest 8.9%. Preferred share (1423 + 1324) is 48–70% per fly. In both preferred orders the strongly coupled pairs (1–2, 3–4) sit opposite each other.
7. **Persistence.** The next MN1 cycle keeps the same order with P = 0.46–0.86 (median 0.75, [D]); the thesis gives 42–85%, mean 63%. Runs of one order last up to 114 cycles (~22 s); mean runs are 2–9 cycles.
8. **Pairwise, controls.** Strong pairs fire in antiphase: MN2 sits at 0.42–0.61 of MN1's cycle (r = 0.27–0.51, vector strength ≈ 0.7). The same holds for MN3–4 (r = 0.31–0.51). The other pairs show only a gap near zero phase (r = 0.50–0.71). Within ±10 ms of a partner spike there are 0.05× chance partner spikes for MN1–2, 0.20× for MN3–4 and 0.16–0.58× for the other pairs [D].
9. **MN4–MN5 (the pair used for genotypes).** Control: sync index r = 0.56 (0.49–0.63, n = 11) and dip10 = 0.06 (0.02–0.10). Independent phases give r = 2/π = 0.637 and dip10 = 0.20. A perfect 5-neuron splay gives a mean pairwise r of 0.559.
10. **shakB RNAi (coupling below detection).** Rates are unchanged. MN4–5 r = 0.61 (0.56–0.72, n = 9; p = 0.033) and dip10 = 0.24 (0.18–0.41; p = 0.0002, [D]). Coincident spikes (≤3 ms) occur at 1.2–2.7× chance across all pairs of 2 five-unit flies (1.7× for MN4–5 pair recordings). No order is preferred (top order 20–26%, rest 11–40%).
11. **Coupling removed means random, not lockstep.** "More synchronous" is r up ≈0.05 and the zero-phase gap filled, with a slight in-phase excess.
12. **Positive control (ShakB(N+16) overexpression).** r = 0.84 (0.57–1.0, n = 7), with 77% of MN5 spikes within 3 ms of MN4. The model synchronizes fully above CC ≈ 0.21 and loses the splay above ≈ 0.05.
13. **Hürkey's mechanism.** A 3-variable conductance model (Na + Shab-like K; Berger & Crook 2015) sits near the small saddle-node-loop point. Its PRC is high early and falls through phase 0.5, so weak gap junctions repel pairs to antiphase. Drive is identical DC plus independent noise (σ = 0.949 pA·ms^½, tuned so splayness ≈ 0.76). The neurons fire at 6.6 Hz with no pronounced AHP. Flies' PRC was never measured.
14. **Brainfly's LIF.** A continuous gap current g(Vj − Vi) carries each partner's reset as a hyperpolarizing kick. That favours antiphase at low rates, while the spike itself favours synchrony (Lewis & Rinzel 2003).
15. **Brainfly's committed rule would push toward synchrony.** It is spike-only and excitatory ("raises each of its electrical partners … by gw mV at once"), which theory predicts synchronizes. That blocks a fair test. An uncommitted change in the working tree on 2026-10-11 (`HybridBrain.set_coupling`) adds conductance junctions with ratio = CC/(1 − CC), passing subthreshold voltage and resets. Merged, it would lift the block.
16. **Connectome identity (MaleCNS).** "DLMn a, b" = MN5, one per side, soma contralateral to its muscle. "DLMn c-f" = MN1–4, four per side, which the connectome does not tell apart. A DLM unit is 4 c-f plus the opposite-soma a,b, which matches PSI's targets.
17. **Input to one DLMn.** 7.0–10.7k synapses; 88–95% of each one's input comes from neurons shared by all five of its unit; 34–39% come from GABA/Glu neurons. The largest inputs are IN19B043/067 ("Tect INs", ≈ 20%). DNg02 contributes 0.3–1.1% and PSI 0.2–0.7%.
18. **Run length.** Weak coupling locks in ≈1/g cycles (hundreds at CC ≈ 0.01). Hürkey simulated 60–300 s; flies' statistics use 10 min (≈3000 spikes per MN). Discard the first ≥ 3 s. Use several seeds.

Conventions:
- [P] stated in Hürkey et al. 2023 (quoted where the wording matters).
- [fig.] read off a published figure by eye, about ±5%.
- [SD] taken from the authors' Zenodo source data (xlsx/npy) as they tabulated it.
- [D] derived by me: a reanalysis of their source data with re-implemented code (scripts in the scratchpad, not the repo), or plain arithmetic.
- [M] a value inside Hürkey's model.
- [T] Hürkey's 2024 PhD thesis.
- [2°] classic work known only through abstracts or later citation (full text behind Cloudflare/Springer).
- MN numbering follows Hürkey: MN1–4 innervate DLM fibres 1–4, ventral to dorsal (= fibres f, e, d, c). MN5 innervates fibres 5 and 6 (= b, a).
- "r" is Hürkey's synchronization index: the time-averaged Kuramoto order parameter of the two interpolated phases.
- "dip10" is the fraction of MN5 spikes falling at phase < 0.1 or ≥ 0.9 of MN4's interspike interval.

---

## 1. Hürkey et al. 2023, Nature 618:118 ("Gap junctions desynchronize a neural circuit to stabilize insect flight")

### 1.1 Preparation

- Animals: 2–5-day-old males, reared at 25 °C. The recording temperature is not stated [P].
- Recording: tethered flight with EMG of each DLM fibre by sharpened tungsten wires. "the EMG spikes recorded from the DLM fibres are a 1:1 reflection of the activity patterns of MN1–5" [P].
- Unit identity came from electrode depth: "Starting from dorsal and slowly moving ventrally, the first unit to appear is MN5, the second one is MN4, the third one is MN3 and so on" [P].
- Wingbeat was measured with a laser light barrier.
- Inclusion and trimming:
  - Flies recorded for ≥ 10 min of flight entered the phase analyses (≈3000 spikes per MN) [P].
  - "The first and last 3 s of each flight bout were discarded… At the beginning of flight bouts, the MN spikes occur at higher frequency and with the highest irregularity, whereas, at the end of a flight bout, the firing frequency decreases" [P].
- Genetics:
  - MN1–5 were targeted with split-GAL4 GMR23H06-AD; GMR30A07-DBD.
  - shakB RNAi: BDSC 57706 (TRiP HMC04895), "targets all shakB isoforms".
  - Overexpression used UAS-shakB(N+16).
  - Shab was raised with UAS-Shab (made in the paper) and lowered with BDSC 41999.
  - GluCl RNAi: VDRC 105754; Rdl RNAi: VDRC 41103.
  - Optogenetics used UAS-ChR2-XXL.
  - Controls were the split-GAL4 crossed to UAS-GFP.VALIUM10 or w1118.

### 1.2 Firing rates in flight

- "each MN fires only every approximately 20th to 40th wingbeat… within a given animal and power demand, all five MNs always fire at the same frequencies (Fig. 1b) and with similar variance in the interspike interval (ISI; coefficient of variation is 0.22 ± 0.07 (mean ± s.d.) for each MN)" [P].
- Fig. 1b per-fly mean rates, Hz, MN1/2/3/4/5 [SD, Figure 1.xlsx]:

| fly (file) | MN1 | MN2 | MN3 | MN4 | MN5 | mean ± SD | MN5 ÷ mean(MN1–4) [D] |
|---|---|---|---|---|---|---|---|
| #1 (201005) | 5.09 | 5.10 | 5.09 | 4.93 | 5.67 | 5.17 ± 0.26 | 1.12 |
| #2 (181029, Canton-S) | 4.39 | 4.40 | 4.51 | 4.25 | 4.95 | 4.50 ± 0.24 | 1.13 |
| #3 (200824) | 7.14 | 6.72 | 6.92 | 7.10 | 7.52 | 7.08 ± 0.27 | 1.08 |
| #4 (190522, Canton-S) | 6.33 | 6.35 | 5.91 | 6.18 | 6.22 | 6.20 ± 0.16 | 1.00 |
| #5 (200818) | 7.83 | 7.80 | 7.73 | 7.59 | 7.60 | 7.71 ± 0.10 | 0.98 |
| #6 (171106, Canton-S) | 7.56 | 7.70 | 7.25 | 7.47 | 9.21 | 7.84 ± 0.70 | 1.23 |
| #7 (200305) | 8.56 | 7.69 | 7.92 | 7.96 | 7.89 | 8.00 ± 0.29 | 0.98 |
| #8 (200827, Canton-S) | 6.41 | 6.42 | 6.36 | 7.64 | 8.44 | 7.05 ± 0.84 | 1.26 |

- Working range:
  - "a nearly linear input–output relationship as observed in f–I curves (3–30 Hz; Fig. 1e) covers and even exceeds the working range observed during tethered flight (approximately 3–12 Hz; Fig. 1c)" [P].
  - The Methods say "3—15 Hz during normal flight" instead [P].
- Fig. 1c, MN rate against wingbeat frequency:
  - Across flies: r² = 0.31 (n = 100). Within one fly: r² = 0.63 in the text but **0.66 printed on the figure**. My refit gives 0.658 (§2.7).
  - Changes track each other better than levels do: Δ MN against Δ wingbeat in 1 s bins gives Pearson r = 0.6 within a fly (ED Fig. 4f) [P].
- Somatic current that matches flight rates:
  - Fig. 1e's shaded "MN firing range during flight" spans ≈0.09–0.35 nA and ≈2–12 Hz, with a red line at ≈5 Hz [fig.].
  - Fig. 4c stimulated one MN at 0.5, 1, 2, 5 and 10 Hz, "spanning the normal range during flight" [P].

### 1.3 Intrinsic properties

In situ whole-cell patch of MN1–4 (ventral access, sheath digested with protease):
- Internal: K-gluconate with 11 mM EGTA. Pipettes 5–6 MΩ; series resistance ≤ 15 MΩ.
- External: 1.8 mM Ca and 4 mM Mg.
- "Resting membrane potential was around −60 mV without current injection" [P].
- f–I protocol: "firing was induced by 1,000 ms square pulse current injections up to 1 nA in 0.1 nA increments". n = 15 flies; mean ± s.e.m. [P].
  - **The stored source traces disagree for 12 of the 15 MNs**, whose steps were 400 ms (§2.8).
- Fig. 1e means, read from the full-resolution figure [fig.]:

| current (nA) | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rate (Hz) | ≈0 | 2.1 | 4.1 | 10.5 | 19.8 | 26.8 | 30.4 | 34.2 | 37.7 | 40.0 | 41.0 |

- The figure overlays a sigmoid fit. "approximately linearly related for 2–30 Hz" [P].
- Fig. 1d shows tonic firing at 0.2, 0.4 and 0.6 nA (1 s) with a clear AHP after each spike [fig.].
- The thesis adds that "somatic current injection causes prominent spike frequency adaptation, so that it is not possible to keep the neurons firing at a constant rate" [T].
- **Not reported:** input resistance, membrane time constant, spike threshold, rheobase and AHP amplitude/time course. Only the coupling coefficient of the AHP is given.
- Shab (Kv2) currents:
  - Shab carries "around 50% of the delayed rectifier current" (quinidine-sensitive, measured in TTX) [P].
  - Shab overexpression roughly doubles the Shab current. Shab RNAi cuts it by ≈70% [P].
  - Fig. 3f labels: control Shab current "Imax 234 ± 33 nA, n = 6"; overexpression "421 ± 52 nA, n = 5". The units are printed as nA beside a 10 nA scale bar, so treat the absolute value with care [fig.].

### 1.4 Electrical coupling (dual whole-cell, MN1–4 only)

- "the electrical synapses are weak, bidirectional and non-rectifying (Fig. 2d). Non-rectifying, because depolarizing and hyperpolarizing current injections (20 ms duration) into one MN cause gap junctional potentials in the other MN. The relationship between presynaptic and postsynaptic charge is linear" [P].
- "Compared with common CCs… estimated in different types of neurons (0.02–0.2), electrical synapses between the five MNs are weak, but coupling is twice as strong for the MN1–MN2 and MN3–MN4 pairs (coupling coefficients (CC) = 0.023 ± 0.003) compared with all of the other possible combinations of MN1–4 pairs (CC = 0.01 ± 0.0027; Fig. 2f)" [P].
- CC definition: "postsynaptic peak voltage divided by presynaptic peak voltage" [P].
- Per-pair CCs [SD, Figure 2.xlsx, Fig. 2f right]:
  - Each value is the mean over 12–40 sweeps of post/pre ΔV, from 2 sweeps per step.
  - Presynaptic deflections were 4–143 mV.

| strong pairs (n = 6) | CC | weak pairs (n = 10) | CC |
|---|---|---|---|
| MN1/2 | 0.0218 | MN1/3 | 0.0167 |
| MN3/4 | 0.0181 | MN3/2 | 0.0099 |
| MN4/3 | 0.0213 | MN2/3 | 0.0092 |
| MN1/2 | 0.0221 | MN1/4 | 0.0143 |
| MN2/1 | 0.0265 | MN2/3 | 0.0122 |
| MN4/3 | 0.0280 | MN2/3 | 0.0156 |
| | | MN4/1 | 0.0103 |
| | | MN1/3 | 0.0068 |
| | | MN3/2 | 0.0085 |
| | | MN2/3 | 0.0081 |
| **mean ± SD** | **0.0230 ± 0.0033** | | **0.0112 ± 0.0032** (sheet; text: 0.01 ± 0.0027) |

- Notes on the table [D]:
  - The weak set contains MN2–3 six times, MN1–3 twice and MN1–4 twice. **No MN2–MN4 pair was measured**, although the caption lists it.
  - The sheet's two-sided t-test gives p = 7e-5 (strong against weak) [SD].
  - **MN5 was never patched**: "MN5 is excluded since it was not included for patch clamp recordings, because of its contralateral location" [T].
- Coupling of spike components:
  - "the AHP of MN spikes is transmitted more effectively (CC, 0.042 ± 0.04) through ShakB-mediated electrical synapses than the brief spike overshoot (CC, 0.01 ± 0.004; Fig. 2h)" [P].
  - "CCs can differ for different components of the action potential because the duration of the presynaptic signal and the time constant of the postsynaptic membrane shape the junction potential" [P].
  - Waveform numbers are in §2.9.
- Interaction during firing: "Paired in situ current-clamp recordings of MNs that were induced to fire tonically by somatic current injection indicate that firing of one MN can depress firing of the other during and shortly after the AHP (Fig. 2i)". Firing was induced at 3–8 Hz [P].
  - The thesis adds that the paired MNs "tend to fire not shortly after one another… but there is no exclusion band before synchronous firing, as seen in the phase histograms during flight" [T].
- Effect of shakB RNAi: it "reduces electrical coupling below the detection threshold in paired patch-clamp recordings" (3 flies). Carbenoxolone also blocked coupling in situ but had no effect when injected into the thorax in flight [T].
- Dye coupling:
  - Not seen normally. It appears with dfmr1 RNAi: "In this genetic background dye coupling of MNs is reliably observed" [P].
  - The thesis reports dye reaching the contralateral MN5 [T].
  - In Calliphora, flight power MNs are dye coupled (Schlurmann & Hausen 2007) [P/T].
- Location and isoform:
  - Junction location is unknown ("A protein trap fly line with a tagged ShakB was nonfunctional") [T].
  - Isoform-specific RNAi against ShakB(N) or ShakB(L) had no effect. N+16 overexpression did. So the thesis infers mostly homotypic ShakB(N+16) channels [T].

### 1.5 The splay state: definition, sequences, phase histograms

- Definition: "A network splay state means that each individual cell in a network of N neurons fires regularly, yet with a constant, non-zero phase relationship with respect to the firing of each other neuron. Firing phase differences between neurons approximately correspond to 1/Nth of a neuron's ISI or a multiple (<N) thereof" [P].
- Switching: "the sequence of MN1–5 firing can change intermittently, but the CPG robustly slides back into one or two of the most preferred splay states. Notably, the same splay states are preferred across animals" [P].
- Near-synchrony: "synchronous spikes between MN pairs occasionally occur during switches between different splay states, but not within a stable splay state" [P].
- Fig. 1f per-fly order occurrences (%) of MN1–4 [SD, Figure 1.xlsx]:
  - The preferred column is [D].
  - The order is cyclic, read from MN1.

| fly (file) | 1234 | 1243 | 1324 | 1342 | 1423 | 1432 | rest | preferred (1423 + 1324) [D] |
|---|---|---|---|---|---|---|---|---|
| #1 (201005) | 3.86 | 12.71 | 31.45 | 2.54 | 35.38 | 8.88 | 5.17 | 66.8 |
| #2 (181029) | 3.17 | 5.35 | 33.53 | 3.11 | 35.92 | 9.19 | 9.74 | 69.5 |
| #3 (200824) | 6.50 | 1.96 | 19.20 | 12.24 | 46.39 | 3.87 | 9.83 | 65.6 |
| #4 (190522) | 7.68 | 2.87 | 34.96 | 7.60 | 35.08 | 2.17 | 9.64 | 70.0 |
| #5 (200818) | 1.03 | 7.97 | 20.29 | 3.04 | 36.77 | 25.59 | 5.29 | 57.1 |
| #6 (171106) | 27.65 | 4.27 | 21.96 | 4.27 | 35.81 | 0.84 | 5.21 | 57.8 |
| #7 (200305) | 10.50 | 4.80 | 21.89 | 8.85 | 30.46 | 3.77 | 19.73 | 52.3 |
| #8 (200827) | 9.22 | 15.26 | 18.74 | 13.55 | 29.50 | 5.67 | 8.07 | 48.2 |
| **median** | 7.09 | 5.07 | 21.92 | 5.93 | 35.60 | 4.77 | 8.85 | 61.7 |

- Sequence counting [D, from the code]:
  - The paper does not define it. The authors' model code (`F3J_ana_hethom.py`) slides a 4-spike window, one spike at a time, over the merged MN1–4 spike train, rotates each window to start at its lowest label, and counts the six permutations. Any window with a repeated MN counts as "rest".
  - Applied to their in vivo spike trains, this reproduces the medians within 1 point (§2.2). The exact in vivo routine is "available on request".
- Why these orders [D]:
  - In 1423 and 1324 the strongly coupled pairs 1–2 and 3–4 sit opposite each other (half a cycle apart). In all four other orders both strong pairs are adjacent.
  - 1423 and 1324 are mirror images. Swapping labels 1↔2 (or 3↔4) maps one onto the other.
- Phase histograms:
  - "Each ISI of an event channel with the timepoints of the units of a given MN was compared to when the units of a second MN occur within the ISIs and counted into bins. All ISIs were normalized to 1 (phase 0 to phase 1), divided into 100 bins…" [P].
  - "The phase relationships of all MN1–5 pairs show a gap around phase zero, indicating out-of-phase firing" [P].
- Splayness index (definition in §1.8):
  - ED Fig. 6c: controls plus Canton-S ≈ 0.76, with 8 points at 0.73–0.79 [fig.]. The dashed reference sits at ≈0.59 [fig.].
  - My recomputation gives 0.759 ± 0.024 for the flies and 0.592 for independent phases (§2.6).
- Dip as a proxy: "For MN4-5 histograms the dip around zero is quantified using the fraction that falls within (−0.1,0.1). This fraction is negatively correlated to full network splayness… (r = −0.94, p < 0.0001, n = 10)" (ED Fig. 6d) [P].

### 1.6 Manipulations

- **shakB RNAi in MN1–5:**
  - "Genetic manipulation of shakB in the five MNs disrupts the splay state without affecting the firing frequencies" [P].
  - "with shakB KD in MN1–5, the gap around phase 0 is absent and firing is more random with a slight preference for in-phase firing (Fig. 2a,b (middle))" [P].
- **Synchronization index, MN4–MN5** (Fig. 3d; numbers from the Methods) [P]:
  - Control median 0.56 (n = 11).
  - shakB RNAi 0.61 (n = 9): U = 78, P = 0.0334.
  - ShakB(N+16) overexpression 0.84 (n = 7): U = 73, P = 0.0008.
  - Model: weak coupling (CC 0.005) 0.54, strong (CC 0.258) 1.0, with U = 100 and P = 0.0002 (10 runs × 60 s each).
  - The thesis gives the overexpression range as "~0.55–1" [T].
- **Fig. 2b sample sizes:** the caption says "n = 10 animals for each genotype", but the text says control n = 7 and the Methods "7 biological replicates in each group". The Zenodo set holds 7 pair recordings per genotype [SD]. Fig. 3d's n = 11 and 9 add the five-unit files (§2.5).
- **Shab:**
  - Overexpression raised MN3–MN4 r from a median of 0.43 (n = 8) to 0.52 (n = 10), P = 0.0434. The model went from 0.26 (SNL) to 0.99 (SNIC) [P].
  - Shab RNAi: "median synchronization indices are 0.559 for control flies (n = 11 animals) and 0.598 for Shab KD (n = 11) and were not statistically different; P = 0.393, U = 74" [P].
  - Shab plus ShakB overexpression together synchronized 90–100% of MN3–4 spikes (median r 0.998) [T].
- **Inhibitory receptors:** "Knockdown (KD) of receptors for inhibitory transmitter (GABA A receptors (GABA-ARs) and glutamate-gated chloride channel (GluCl)) increases MN firing frequencies, but the phase relationships remain similar" (n = 10 GluCl, 8 Rdl) [P].
- **Unpatterned drive:**
  - Constant blue light on ChR2-XXL in cholinergic neurons (n = 11) or in MN1–5 (n = 7) "increases MN firing frequencies without changing their phase relationships" [P].
  - Sizes, from the thesis: cholinergic drive +3 Hz in MN4/5 and +12 Hz in wingbeat; MN drive +2 Hz and +8 Hz [T].
  - ChR2-XXL off-τ is 76 ± 12 s, so rates outlast the light [P].
  - "UAS-CsChrimson… caused few MN spikes followed by silence, probably caused by a depolarization block" [P].
- **Common input:**
  - Activity-dependent GRASP shows cholinergic input onto MN dendrites (ED Fig. 4a,b).
  - Dual current clamp of MN3 and MN4 shows "highly similar patterns of PSPs, providing direct evidence for shared synaptic input" [P].
- **No central output:** trans-Tango shows no postsynaptic partners of MN1–5 in the VNC. Brp-short puncta appear only in somata and at the NMJ [P].

### 1.7 Muscle calcium and wingbeat consequences

- DLM fibre voltage after one MN spike decays with τfast ≈ 1.7 ms and τslow ≈ 14 ms (n = 3) [P]. The thesis gives τfast 1.2 ms [T].
- Myoplasmic Ca²⁺ (GCaMP8f): rise τ 6.2 ± 1.7 ms, decay τ 82 ± 6.7 ms (n = 7) [P]. The thesis gives 79 ± 13 ms [T].
- "summation as caused by an incomplete return to resting calcium levels between MN spikes starts at 2 Hz and increases at higher frequencies" [P].
- "Synchronous MN firing causes peak wingbeat frequencies after 7.3 ± 1.3 ms… that decline with a time constant τ = 83 ± 27 ms" [P].
- "synchronous MN firing causes 8× higher wingbeat frequency fluctuations over time compared with firing in splay state" [P].
- Spike-triggered wingbeat change [T]:
  - Control: about ±0.4 Hz.
  - shakB RNAi: ≈1 Hz, or at least 3 Hz when all MNs are counted.
  - ShakB(N+16) overexpression: ≈5 Hz.
  - Shab + ShakB overexpression: ≈18 Hz.

### 1.8 The model (Methods, Supplementary Tables 2–4 and Zenodo code)

**Neuron.** One compartment, Berger & Crook (2015) as refitted:
- Equation: C dv/dt = I_in − g_L(v − E_L) − g_shab b⁴(v − E_K) − g_Na m∞³(v)(1 − h)(v − E_Na) + Σ_j g_gap,ij (v_j − v_i).
- Gate kinetics, Supplementary Table 3:
  - Steady state: p∞ = 1/(1 + e^(−Q z_p (v − v_p))).
  - Time constant: τ_p = e^(−Q z_p γ_p (v − v_p)) / [r_p (1 + e^(−Q z_p (v − v_p)))], with Q = 0.0392 /mV.
- Parameters [M]:
  - C = 0.13 nF; g_Na = 0.4312 µS; g_L = 8.624 nS.
  - E_L = −60 mV, E_K = −72 mV, E_Na = 55 mV.
  - m: z = 3, v_m = −33 mV.
  - h: z = 5.2, v_h = −39.14 mV, r = 0.2/ms, γ = 0.38.
  - b: z = 1.1056, v_b = −42.14 mV, r = 0.2/ms, γ = 0.38.

| regime | g_shab | I_in | onset bifurcation / PRC | unperturbed rate [D, from their saved run] |
|---|---|---|---|---|
| HOM near small SNL ("SNL") | 0.13768216 µS | 108.75 pA | homoclinic; PRC peaks early and falls through 0.5 | 6.59 Hz (ISI 151.7 ms); v swings −49 to +3 mV, interspike plateau ≈ −49 mV |
| SNIC | 0.2156 µS | 175 pA | symmetric type I | 6.56 Hz |
| Hopf | 0.34496 µS | 330 pA | type II | — |

- Derived passive values [D]:
  - τ = C/g_L = 15.1 ms, and 1/g_L = 116 MΩ.
  - At −60 mV the resting Shab conductance (b∞⁴ ≈ 0.0099) adds ≈1.4 nS. That gives Rin ≈ 100 MΩ, τ ≈ 13 ms and rest ≈ −61.5 mV with I_in = 0.
- "Note that the minimal conductance-based model does not contain a pronounced AHP (Fig. 3b (spike shape)), showing that the presynaptic AHP is not mandatory for network desynchronization" [P].
- Hopf ruled out: "the region in which tonic spiking commences through the FLC/Hopf bifurcation has a finite, non-zero frequency at the rheobase… around 47 Hz and therefore above the dynamic range of the in vivo measures f–I curves" [P].

**Coupling** [M]:
- Linear, symmetric: I_gap,ij = g_gap,ij (v_j − v_i).
- CC = g_gap/(g_gap + g_L), computed pairwise with all voltage-gated channels closed. CC conversions below are [D].
- Homogeneous: g_gap = 43.5 pS (CC 0.0050).
- Heterogeneous:
  - Ratios set by Fig. 2f: MN1–2 and MN3–4 86.59 pS (CC 0.0099); other MN1–4 pairs 38.27 pS (CC 0.0044).
  - "MN5 was coupled in with a coupling strength half of the mean of the other connections": 27.19 pS (CC 0.0031).
  - The mean is 43.50 pS, equal to the homogeneous case.
- Strong: 3 nS (CC 0.258).
- So the published model's "weak" CCs are ≈2.3× below the measured ones. Yet the model is splayed for every CC in 0.012–0.045 in Fig. 3c, so the measured values sit inside its splay regime [D].

**Drive and noise** [M]:
- Every neuron gets the same constant I_in plus independent zero-mean white noise.
- σ = 0.949 pA·ms^½ (code: `sig*xi` with 3e-8 µA·s^½). No shared fluctuations.
- ED Fig. 6a,c sets σ by matching splayness: σ = 0.5 / 0.7 / 0.9 / 1.9 / 3.8 / 7.6 pA·ms^½ give splayness ≈ 0.87 / 0.81 / 0.76 / 0.68 / 0.62 / 0.59 [fig.]. So σ ≈ 0.9–0.95 reproduces flies' 0.76.

**Integration and runs** [M]:
- Noisy runs: Heun, dt = 3 µs, 60 s (Fig. 3d,h) or 300 s (Fig. 3j), 10 runs each.
- Deterministic runs: RK4, dt = 100 µs (Fig. 3b,c).
- Fig. 3c used 200 random initial conditions × 40 values of g_gap (0–4 nS), 3 s each. Splayness came from the last ≈0.6–0.7 s (t > 2 s).
- Spikes were detected at v > −10 mV, with a 10 ms detection refractory window.
- Neurons start at random phases of an uncoupled cycle.

**Results** [P/M]:
- Fig. 3c regimes:
  - "Weak CCs (<0.05) cause high splayness indices; intermediate CCs (0.05–0.21) decrease splayness and yield multiple stable network states; CCs of >0.21 yield network synchrony (splayness = 0)".
  - At CC = 0 (uncoupled, deterministic) splayness spreads widely, with a mean "slightly above 0.5" [T]. The black average line starts near 0.6 [fig.].
- Fig. 3j, occurrences [fig.]:
  - Homogeneous coupling: every order about 0.15–0.18; rest ≈ 0.03.
  - Heterogeneous coupling: 1423 ≈ 0.42, 1324 ≈ 0.35, the other four ≈ 0.04–0.05, rest ≈ 0.03.
  - The authors' in vivo medians, from `F3J_plot.py`: 7.09, 5.07, 21.92, 5.93, 35.60, 4.77 and 8.85% [SD].
- **Symmetry caveat [D].** The heterogeneous g matrix is unchanged by relabelling 1↔2 (or 3↔4), which maps 1423 onto 1324. So the model gives both equal probability in expectation, and its 0.42 against 0.35 is sampling noise.
  - Flies' 35.6% against 21.9% therefore needs something the model lacks: asymmetric coupling, unequal intrinsic rates or unequal drive.
  - Don't pre-register a 1423 > 1324 target for a symmetric model.

**PRC theory** [P]:
- Phase reduction gives the averaged coupling function G(ψ) = ∫ Z(φ) g_gap (v(φ − ψ) − v(φ))/C dφ.
- Stable phase differences are stable zeros of G_odd(ψ) = G(ψ) − G(−ψ).
- "for weak reciprocal electrical coupling, out-of-phase firing of identical neurons can be obtained only in combination with a PRC that is monotonically decreasing around phase 0.5".
- Five neurons cannot all be pairwise antiphase ("frustrated"). The splay state is the low-frustration solution.
- Why near SNL rather than deeper in HOM: "the slope of the neurons' firing-rate versus current-input (f–I) curves is not as steep as deeper in the HOM regime, therefore enabling smooth control".
- **Not measured in flies:** "Ideally one would confirm the HOM excitability class by PRC estimation in vivo… this is not possible for the DLM-MNs… Therefore, we cannot be sure that the PRC is really of the HOM type in vivo" [T].

**Metric code** (`spiketime_analysis_helper.py`) [SD]:
- Phases: φ(t) = (t − t_n)/(t_{n+1} − t_n), sampled every 1 ms.
- Time window: from the first spike of the last neuron to start to the last spike of the first neuron to stop.
- Flight stops are excluded: a gap between wingbeats > 60 ms opens a break, cut from the last spike before it to the first spike after it.
- **Splayness:**
  - Sort the N phases at each time step and take the N gaps ψ_i (the last one wraps around to sum to 1).
  - r_k = Σ_i (ψ_i − 1/N)² / [(N−1)/N² + (1 − 1/N)²] = N/(N−1) Σ_i (ψ_i − 1/N)².
  - s = 1 − √(mean_k r_k). **The square root is in eq. 7 (PMC MathML) and in the code, but plain-text renderings drop it.** Without it, controls would read 0.93–0.96.
- **Sync index:** r = time mean of |½ Σ_j e^{i2πφ_j}| = time mean of |cos(π Δφ)|.

### 1.9 Inconsistencies to keep in mind

- Within-fly r²: 0.63 in the text against 0.66 on the figure.
- Fig. 2b sample size: n = 10 in the caption against 7 in the text and data.
- Weak CC SD: 0.0027 in the text against 0.0032 in the sheet. MN2–4 is listed but was never measured.
- f–I step length: 1,000 ms in the Methods, but 400 ms in 12 of the 15 source traces.
- Fig. 2f's y-axis tick "−0.105" should read −0.015.
- Flight range: 3–12 Hz in the main text against 3–15 Hz in the Methods.
- ED Fig. 8 shows 3 five-unit RNAi flies; Zenodo has 2, one of them only 60 s. The thesis analyses 3 flies of 600 s.
- The thesis calls model weak coupling "CC=0.05"; the code uses 0.005.
- **Labels:** in the Zenodo model-code file `split23h06xValium_5units_200824_m1_600sec_SpE.npy`, MN2 and MN3 are swapped relative to the Figure 1.xlsx tables for the same fly.
  - The file's rates come out as MN2 6.92, MN3 6.72 against the sheet's 6.72, 6.92.
  - The file's dominant order is "1432" (47.6%) against the sheet's 1423 at 46.4%.
  - Relabelling 2↔3 reproduces the sheet [D]. I use the relabelled file below.

---

## 2. Derived from the authors' source data (my reanalysis)

### 2.1 Validation

- I re-implemented the phase interpolation, break removal and Kuramoto r without brian2, using Zenodo 7740678 spike trains.
- MN4–MN5 medians come out at:
  - control 0.559 (n = 11; published 0.56);
  - shakB RNAi 0.613 (n = 9; 0.61), with U = 78, P = 0.0334, exactly as published;
  - overexpression 0.840 (n = 7; 0.84), with U = 73, P = 0.00075;
  - Shab RNAi 0.598 (0.598).
- MN3–MN4: Shab overexpression 0.522 (0.52); control plus Canton-S 0.426 (0.43).
- Splayness of the 8 five-unit controls is 0.727–0.794 (ED Fig. 6c shows ≈0.73–0.79).
- So the definitions below match the paper's [D].

### 2.2 Five-unit flight recordings (8 controls: 4 Canton-S + 4 split-GAL4 > VALIUM10; 2 shakB RNAi)

| file | flight s | wingbeat Hz | rates MN1–5 (Hz) | CV MN1–5 | splayness (N=5) | preferred share of complete MN1 cycles | P(next cycle same order) | longest run (cycles) |
|---|---|---|---|---|---|---|---|---|
| CS 200827 | 600 | 141 | 6.41 6.42 6.36 7.64 8.44 | 0.14–0.16 | 0.732 | 0.51 | 0.46 | 14 |
| CS 190522 | 410 | 153 | 6.34 6.35 5.91 6.18 6.22 | 0.19–0.22 | 0.794 | 0.78 | 0.75 | 62 |
| CS 181106 | 253 | 137 | 7.60 7.75 7.29 7.52 9.27 | 0.12–0.23 | 0.745 | 0.63 | 0.74 | 52 |
| CS 181029 | 438 | 189 | 4.40 4.41 4.52 4.26 4.96 | 0.27–0.31 | 0.781 | 0.79 | 0.75 | 41 |
| VAL 200305 | 181 | 176 | 8.56 7.69 7.92 7.97 7.90 | 0.18–0.23 | 0.727 | 0.68 | 0.68 | 21 |
| VAL 200824 | 600 | 185 | 7.14 6.72 6.92 7.10 7.52 | 0.23–0.31 | 0.759 | 0.76 | 0.78 | 51 |
| VAL 201005 | 600 | 168 | 5.09 5.10 5.09 4.93 5.67 | 0.11–0.13 | 0.760 | 0.71 | 0.82 | 114 |
| VAL 20818 | 600 | 196 | 7.83 7.80 7.73 7.59 7.60 | 0.18–0.23 | 0.776 | 0.61 | 0.86 | 72 |
| RNAi 180117 | 60 | 168 | 9.92 10.63 9.52 10.97 10.20 | 0.13–0.17 | 0.519 | 0.32 | 0.54 | 8 |
| RNAi 200331 | 600 | 165 | 4.30 3.77 4.18 4.19 3.98 | 0.15–0.17 | 0.685 | 0.39 | 0.61 | 13 |

Definitions [D]:
- Rates are spikes ÷ flight time.
- "Complete cycle" = an MN1 ISI (< 0.5 s) holding exactly one spike each of MN2–4. These are 72–92% of MN1 ISIs in controls and 75–81% in RNAi.
- An unbiased choice among the six orders would give a preferred share of 0.33.
- The preferred share in sliding windows (Fig. 1f's method) is 48–70% in controls and 27% and 35% in RNAi.
- Mean run of one order:
  - controls 1.8–7.1 cycles; runs of the preferred orders average 2.2–9.2 cycles;
  - RNAi 2.2–2.5 cycles, longest 8–13.
- The thesis gives "probability of staying in the same pattern" as control 42–85% (mean 63%) against RNAi 32–33% (n = 3 each), and a longest control run of 109 [T]. Its definition isn't given, and its code DOI (zenodo.8316179) doesn't resolve.
- My sliding-window medians with the 200824 fix: 1234 8.1, 1243 6.2, 1324 22.5, 1342 6.4, 1423 35.2, 1432 4.2, rest 8.4%. Published: 7.1, 5.1, 21.9, 5.9, 35.6, 4.8, 8.9.
- RNAi sliding-window orders (%), 1234/1243/1324/1342/1423/1432/rest:
  - 180117: 13.2 5.6 8.9 26.1 18.0 12.9 15.3.
  - 200331: 7.3 6.6 19.7 21.3 15.2 19.0 10.9.

### 2.3 Pairwise phase relations (8 controls; RNAi values in the last column)

Columns [D]:
- r: Hürkey's sync index.
- dip10: the fraction of the later-numbered MN's spikes at phase < 0.1 or ≥ 0.9 of the earlier MN's ISI. Independent = 0.20.
- Circular mean phase and vector strength R: of the later MN in the earlier MN's ISI.
- Coincidence: the fraction within 5 ms of a partner spike, against the chance 1 − e^(−2·0.005·rate) ≈ 0.064–0.071.

| pair | r, median [range] | dip10 | circular mean phase (8 flies) | R | ≤5 ms coincidence | RNAi r (2 flies) | RNAi dip10 |
|---|---|---|---|---|---|---|---|
| **MN1–MN2** | **0.336 [0.271–0.513]** | 0.006 [0–0.133] | 0.43 0.45 0.42 0.50 0.61 0.59 0.44 0.53 | **0.73** | 0.006 | 0.673, 0.492 | 0.33, 0.09 |
| MN1–MN3 | 0.659 [0.547–0.709] | 0.056 | spread (0.57–1.0) | 0.12 | 0.026 | 0.659, 0.599 | 0.32, 0.03 |
| MN1–MN4 | 0.666 [0.635–0.712] | 0.054 | spread | 0.08 | 0.026 | 0.645, 0.595 | 0.26, 0.07 |
| MN1–MN5 | 0.621 [0.613–0.677] | 0.141 | spread | 0.07 | 0.042 | 0.704, 0.543 | 0.38, 0.11 |
| MN2–MN3 | 0.623 [0.504–0.647] | 0.030 | spread | 0.23 | 0.018 | 0.659, 0.582 | 0.28, 0.15 |
| MN2–MN4 | 0.598 [0.517–0.664] | 0.049 | spread | 0.15 | 0.028 | 0.714, 0.591 | 0.34, 0.20 |
| MN2–MN5 | 0.618 [0.527–0.639] | 0.108 | spread | 0.10 | 0.036 | 0.717, 0.633 | 0.35, 0.31 |
| **MN3–MN4** | **0.394 [0.314–0.510]** | 0.025 [0.004–0.065] | 0.41 0.41 0.41 0.57 0.47 0.40 0.64 0.64 | **0.70** | 0.024 | 0.623, 0.580 | 0.24, 0.09 |
| MN3–MN5 | 0.588 [0.546–0.624] | 0.063 | spread | 0.18 | 0.031 | 0.654, 0.585 | 0.28, 0.15 |
| MN4–MN5 | 0.570 [0.502–0.637] | 0.063 [0.016–0.097] | spread | 0.23 | 0.031 | 0.637, 0.561 | 0.27, 0.18 |

- Reading it:
  - The two strong pairs are the only phase-locked ones: antiphase, with high R. The weak pairs and MN5 show only the zero-phase gap, because their relative phase changes with the order.
  - MN5 is the least locked. "In the phase histogram of MN1 to MN5 the distribution is uniform, showing no local maxima" [T].
- Phase templates in the preferred orders: mean phase of each MN's first spike in complete MN1 cycles [D].
  - In 1423: MN4 0.18–0.31, MN2 0.42–0.57, MN3 0.71–0.82, MN5 0.40–0.60 (SD 0.13–0.30).
  - In 1324: MN3 0.18–0.30, MN2 0.44–0.58, MN4 0.68–0.83, MN5 0.40–0.53 (SD 0.18–0.29).
  - The SD of MN2–4 phases is 0.06–0.12 in controls and 0.11–0.25 in RNAi. MN5 usually lands next to MN2, e.g. 14253, 14523, 13524, 13254.

### 2.4 Exclusion bands in milliseconds (controls; 200824 relabelled)

- Fraction of partner spikes within ±10 / ±20 / ±35 ms, as observed ÷ chance [D]:
  - MN1–2: 0.05 / 0.04 / 0.26.
  - MN3–4: 0.20 / 0.17 / 0.32.
  - Weak MN1–4 pairs: 0.16–0.31 / 0.35–0.70 / 1.06–1.33.
  - MN5 pairs: 0.34–0.58 / 0.50–0.93 / 1.03–1.30.
- The 2.5th percentile of |Δt|, excluding coincidences ≤ 3 ms, by median across flies:
  - MN1–2: 28 ms (6–47); MN3–4: 27 ms (19–40).
  - Weak pairs: 12–18 ms; MN5 pairs: 10–16 ms.
- In shakB RNAi the same percentiles fall to 4–13 ms, and near-coincidences rise above chance: ±10 ms ratios 0.9–2.3.
- ≤ 3 ms coincidences:
  - Controls 0.6–3.7% of spikes against ≈3.5–4% chance. The thesis says "ranges from 0.1% (MN1 and MN2) to 3%" [T].
  - shakB RNAi 4–11%.
- Classic description: "no firing of one MN occurs shortly before and after (±20 ms) the firing of another MN" (Harcombe & Wyman 1977, via [T]).
- Merged train: "most MNs fire around 35 ms after the previous MN firing" [T]. That is ≈ 1/5 of a 170 ms ISI.

### 2.5 MN4–MN5 pair recordings by genotype (Zenodo `SpEs_45` + five-unit files, as in Fig. 3d)

| group | n | r median [range] | dip10 median [range] | ≤3 ms (chance) | ≤10 ms (chance) | ≤20 ms (chance) | MN4 Hz | wingbeat Hz |
|---|---|---|---|---|---|---|---|---|
| control (7 pair-only + 4 five-unit) | 11 | 0.559 [0.485–0.629] | 0.060 [0.020–0.097] | 0.026 (0.033)* | 0.029 [0.011–0.044] (0.105)* | 0.068 (0.199)* | 5.8 | 196 |
| Canton-S five-unit | 4 | 0.552 [0.502–0.637] | 0.054 [0.016–0.097] | — | — | — | 6.9 | 147 |
| shakB RNAi (7 + 2) | 9 | 0.613 [0.561–0.719] | 0.236 [0.181–0.413] | 0.071 (0.041)* | 0.179 [0.142–0.331] (0.131)* | 0.314 (0.245)* | 7.0 | 195 |
| ShakB(N+16) OE | 7 | 0.840 [0.568–0.997] | 0.772 [0.091–0.992] | 0.771 (0.034) | 0.772 (0.110) | 0.773 (0.208) | 5.8 | 199 |
| Shab RNAi | 11 | 0.598 [0.510–0.637] | 0.112 [0.062–0.233] | 0.046 (0.036) | 0.053 (0.116) | 0.119 (0.219) | 6.2 | 173 |

- \* = the 7 pair-only recordings.
- MWU tests [D]:
  - dip10, RNAi against control: U = 99, p = 0.0002. It separates the genotypes far better than r (p = 0.033).
  - r, overexpression against control: p = 0.00075.
- Rates differed little between genotypes (median MN4 5.5–7.0 Hz), in line with "without affecting the firing frequencies" [P].
- Wingbeats per MN4 spike: 38 in controls against 28 in shakB RNAi, a significant difference [T]. The thesis attributes it to the RNAi flies firing faster within the normal rate–efficiency curve.

### 2.6 Null levels (what "removing all interaction" looks like) [D]

- Independent uniform phases:
  - splayness 0.592 (N = 5), 0.553 (N = 4);
  - pairwise r = 0.636 (2/π);
  - dip10 = 0.200.
- Perfect 5-neuron splay: pairwise r = |cos(πk/5)| = 0.809 for neighbours and 0.309 for next-but-one; mean 0.559. Perfect antiphase pair: r = 0.
- Each fly's own trains, with every MN circularly shifted at random (20 shifts):
  - splayness 0.590 ± 0.005; r(MN4–5) 0.635–0.642; dip10 0.199–0.207;
  - all six orders equal, 4–13% each;
  - "rest" 19–75% (one 181 s recording with long breaks excluded), depending on ISI regularity, against 4–15% in flies.
- So flies' low "rest" fraction (few repeats of one MN inside 4 spikes) is itself a coupling signature.
- Model at CC = 0: splayness spreads widely around ≈0.6 with deterministic drive [fig.].

### 2.7 Wingbeat against MN rate (Fig. 1c source data) [SD → D]

- 100 flies, one mean per recording, MN5 only:
  - MN5 5.76 ± 1.85 Hz (median 5.54; range 3.00–13.15; 5–95% 3.4–9.2).
  - Wingbeat 192.9 ± 18.6 Hz (156–245).
  - Fit: wingbeat = 160.7 + 5.60 × MN rate (r² = 0.309; p = 2e-9).
  - Wingbeats per MN spike: median 34.9 (IQR 30–40; 16–65).
- One fly over 30.5 s (0.1 s samples): wingbeat = 177.6 + 3.21 × MN rate (r² = 0.658), with MN 6.3–9.4 Hz and wingbeat 194.5–210.7 Hz.
- Optogenetic gains from the thesis:
  - +12 Hz wingbeat for +3 Hz MN (cholinergic drive) and +8 Hz for +2 Hz (MN drive), i.e. ≈4 Hz of wingbeat per Hz [T, D].
- 41 flies: MN5 4.9 Hz, MN4 4.7 Hz, p = 0.47 [T].

### 2.8 Intrinsic properties recounted from the Fig. 1e source traces (15 MNs) [SD → D]

- Traces:
  - Flies 1–3: 1,000 ms steps at 50 kHz.
  - Flies 4–15: 400 ms steps at 20 kHz. Flies 4 and 5 stop at 0.8 nA, and flies 9, 10, 12, 14 and 15 at 0.9 nA.
- Resting potential at I = 0, before the step: −52.3 to −65.6 mV, median −58.0 mV.
- Spike counts ÷ step length. Two detectors were used, prominence ≥ 8 mV or ≥ 3.5 mV with a fast upstroke; they agree except in 3 MNs.
- Mean rate by current:
  - 0.1 nA 1.0 Hz; 0.2 nA 2.1; 0.3 nA 7.2–8.3; 0.4 nA 14.9–15.9; 0.5 nA 21.6–22.7.
  - 0.6 nA 26–27; 0.7 nA 30–32; 0.8 nA 34; 0.9 nA 34–35; 1.0 nA 37–40.
  - That runs 20–50% below Fig. 1e at 0.1–0.4 nA. The paper probably used instantaneous ISI rates or counted small spikes I missed. Use Fig. 1e for targets and these numbers for spread.
- Rheobase (lowest step with ≥ 1 spike):
  - 0.1 nA in 1 MN, 0.2 in 4, 0.3 in 6, 0.4 in 4; median 0.3 nA.
  - Minimum sustained rates seen were ≈5–9 Hz in the 1 s steps: no high-rate onset, consistent with continuous (type I/HOM-like) onset.
- Gain: a linear fit over steps with 0–32 Hz gives a median of 75 Hz/nA (IQR 45–82; range 21–100). The extrapolated x-intercept has a median of ≈0.2 nA.
- Saturation is ≈35–50 Hz at 0.8–1.0 nA. Counts in traces with small spikes are unreliable at high current (the two detectors disagree there).
- Input resistance: ΔV at the 0.1 nA step gives 49–148 MΩ (median ≈ 80, n = 14).
  - This includes any uncompensated series resistance: bridge jumps are visible at step onset in several traces.
  - Berger & Crook (2015) cite MN5's Rin as 97 ± 31 MΩ (Duch et al. 2008). The Hürkey model is 100–116 MΩ.
- Membrane τ can't be read from these traces because of the bridge artefacts. Use the model's 13–15 ms with that caveat.
- Spike shape near the lowest repetitive current, as voltages relative to threshold within a trace (these don't depend on the constant bridge offset):
  - amplitude median ≈33 mV (5–49);
  - fast AHP trough median ≈18 mV below threshold (3–26), 2.4–10 ms after the peak.
  - Many somatic spikes are small, as expected if spikes start distally.
  - Absolute thresholds (−42 to +4 mV) are unreliable.

### 2.9 Spike and AHP coupling waveform (Fig. 2h source trace, one pair) [SD → D]

- Presynaptic MN (held depolarized; pre-spike baseline −15.8 mV, absolute value unreliable):
  - spike 36.4 mV above baseline, half-width 1.86 ms;
  - AHP trough 14.4 mV below baseline at +11.5 ms, still −10.4 mV at +50 ms and −8.7 mV at +100 ms;
  - **the AHP lasts more than 100 ms**.
- Postsynaptic MN at −64.0 mV:
  - spikelet +0.38 mV, peaking at ≈0.4 ms (CC 0.010);
  - then a hyperpolarization of −0.55 mV peaking at +37.5 ms (AHP CC 0.038; published 0.042), still −0.43 mV at +100 ms.
  - So each partner spike delivers ≈0.4 mV of brief excitation and ≈0.5 mV of inhibition lasting ~100 ms, a large share of the 150–200 ms ISI.

---

## 3. Hürkey 2024 thesis (Mainz): additions not in the paper

- "During flight, all five MNs fire at the same average frequency within each animal, typically ranging from 4 to 8 Hz… with an inter animal average of around 5 Hz (mean MN5 frequency = 4.9 Hz and MN4 frequency = 4.7 Hz, n=41)."
- "MN5 fires around 10% faster and is therefore changing its position in the sequence more frequently" (after Harcombe & Wyman 1977). This was n.s. in 41 flies.
- Poincaré plots: single MN ISIs fall within ≈0.2 ± 0.1 s, with "nearly no ISIs shorter than 0.1 s".
  - In RNAi the merged MN1–5 train gains many short intervals (< 15 ms), while single-MN variability and CV are unchanged.
- Order statistics, 3 controls against 3 RNAi (600 s each):
  - Controls always prefer 1423 at nearly 40%.
  - RNAi top orders are 24% (1423), 21% (1342) and 22% (1324): "there are no preferred sequences".
  - Rest: 13–40% in RNAi against 5–10% in controls.
  - Stay probability 63% against 33%. Longest run: 109 cycles against 11.
- Firing rate depends on the order: 34 of 45 order pairs differ in controls and 19 of 45 in RNAi. The preferred orders "tend to fire at lower frequencies".
- Wingbeat by order: no consistent effect. Pattern 1342 is the least or second-least efficient in 5 of 6 flies (n.s.).
- "The farther apart the MNs are in respect to their muscle fiber, the smaller the exclusion bands become. Accordingly, the weakest interactions are found between MN1 and MN5."
- Isoform-specific RNAi of ShakB(N) and ShakB(L) had no effect. The pan-isoform RNAi did.
- Carbenoxolone injected into the thorax in flight had no effect, probably because it doesn't cross the sheath; it did block coupling in situ.
- PARIS, an optical coupling assay, didn't work.

---

## 4. Classic work on DLM motor unit firing

- **Wyman 1965** (Biophys J; Calliphora [2°]) is the first statistical description of out-of-phase DLM units.
- **Wyman 1966** (J Neurophysiol 29:807, "Multistable firing patterns among several neurons") [2°]: "when the muscle units are activated sequentially the muscle will always contain some freshly re-excited units and some units that are relatively weak. Possibly this smoothing of the power output is the purpose of the sequential pattern of activation" (quoted in [T]).
- **Wyman 1969 I/II** (J Neurophysiol 32:297, 307) [2°]: "lateral inhibition" with autorhythmic MNs.
  - Each ISI is set by the inhibitions received from the others. "Synchronous firing within 3 ms is possible because inhibition by chemical synapses would be too slow" ([T]'s paraphrase).
  - Coined "exclusion band".
- **Levine & Wyman 1973** (PNAS 70:1050, abstract):
  - "There are 26 singly-innervated muscle fibers. There are two basic firing patterns: phase progression, shown by units that receive a common input but have no cross-connections, and phase stability, in which synergic units, receiving a common input and inhibiting each other, fire in a repeating sequence."
  - In the flightless mutant *stripe*, "the patterning within bursts shows many of the characteristics of the wild type".
- **Harcombe & Wyman 1977** (J Neurophysiol 40:1066) [2°, via thesis and the paper]:
  - Common input.
  - Occasional synchrony within 3 ms; no firing ±20 ms around another unit; broader windows for MN1+2 and MN3+4.
  - 1324 and 1423 "around ~80% of the time".
  - MN5 ≈10% faster.
  - A schematic of graded "inhibitory" interconnection strengths, thickest for 1–2 and 3–4.
  - Proposed that each MN "summate[s] many small excitatory postsynaptic potentials from a common source" (Cheong 2026's paraphrase).
- **Harcombe & Wyman 1978** (J Comp Physiol 123:271) [2°]: sequences last "several hundred cycles" continuously ([T]).
  - Semantic Scholar TLDR: "apparently are driven by a common input, yet each is phase-locked to a different time in a repeating cycle".
  - Mine run ≤ 114 cycles in 8 flies (§2.2).
- **Koenig & Ikeda 1980, J Exp Biol 87:121** (abstract):
  - "the influence is insignificant except when one unit would have fired soon after another. Then, a neural interaction occurs that can cause a unit to fire either earlier or later, depending on its firing relationship with the other units".
  - "the observation that no DLM fibre fires soon after another is the result of both a delaying effect and an effect which causes a cell to fire earlier than it normally would have fired."
- **Koenig & Ikeda 1980, J Exp Biol 87:137** (abstract):
  - All 10 bilateral units: pooled intervals "fluctuate in a serially correlated manner… suggest that two (or more) oscillating inputs are involved in commonly driving these units".
  - "a coupling in frequency and timing was observed between certain pairs of ipsilateral units, as well as between the units of one side relative to those of the other side".
  - Proposed pathways "one leading to units 1 and 2, another to units 3 and 4, and a third to unit 5/6".
- **Koenig & Ikeda 1980, J Neurobiol 11:509**: *shibire*ts flies at 26–27 °C produce a wild-type-like DLM pattern. "At higher temperatures, the pattern became abnormal, characterized by many synchronous firings among the fibers and occasional bursting."
- **Koenig & Ikeda 1983** (J Comp Physiol 150:295 and 150:305) [2°, Semantic Scholar TLDRs only]:
  - MNs appear driven by "two (or more) rapidly firing inputs mediated by electrical rather than chemical junctions".
  - The no-firing-after-another effect "might be due to a partial resetting of the other neuron's timing, triggered by a 'local' excitatory response caused by firing in the first neuron" ("Reciprocal excitation…").
- **Ikeda, Koenig & Tsuruhara 1980** (J Neurocytol 9:799): "axons 1-2 and 3-4 make particular pairs with long shared pathways… the axons are unusually closely associated with each other within the nerve". This is a candidate site for the stronger 1–2 and 3–4 coupling ([T]).
- **Ikeda & Koenig 1988** (J Comp Neurol 273:436, abstract):
  - "DLM1-6 from ventral to dorsal… The somata of MN1 and 2 lie side by side in a horizontal plane with MN1 in a more anterior position. Those of MN3 and 4 lie ventrally to those of MN1 and 2… with MN3 in the more anterior position. The soma of MN5 is located contralaterally… next to the midline".
- Not read: Mulloney 1970 (J Neurophysiol 33:86); Tanouye & Wyman 1981; Hürkey's 2022 bioRxiv preprint.

---

## 5. Wingbeat against MN firing (asynchronous muscle)

- **Gordon & Dickinson 2006** (PNAS 103:4311, intracellular recordings from identified DLM/DVM fibres in tethered flight):
  - "The motor neurons of the A-IFMs fire at a rate (≈5 Hz in Drosophila) well below contraction frequency (≈200 Hz in Drosophila)".
  - Under vertically oscillating gratings (0.08 Hz), "An ≈2-fold change in power accompanied a 3-fold change in steady-state spike frequency". Correlations with power: r = 0.34–0.67 (111 experiments).
  - "During steady-state flight, a 3-fold increase in spike frequency (from 3 to 9 Hz) results in a 1.7-fold increase in power output".
  - Paired fibres: "the correlation in instantaneous spike frequency was very high (range 0.55–0.91)" (14 pairs); "no evidence for differential recruitment".
  - Spike rate steps with τ 0.134 s (rise) and 0.329 s (fall). Power follows with 0.442 s and 1.79 s.
  - "the onset of flight was accompanied by a brief burst in A-IFM spike rate".
  - Calcium rises linearly with stimulation rate. Electrical drive via the giant fiber works up to 25 Hz, "at which point synapses in the pathway began to fail".
  - Lehmann & Bartussek's 2017 review summarizes the maneuvering spike rates as "up to ~20 Hz".
- **Ryglewski et al. 2014** (PNAS): "wing motoneurons fire tonically at frequencies of 4–20 Hz".
- **Ryglewski et al. 2017** (Neuron): MN5 during optomotor stimulation. Upward stripe motion raised firing by "~9 Hz"; downward lowered it by "~2 Hz" (controls).
- **Lehmann et al. 2013** (via the 2017 review): DLM calcium against muscle power is linear (R² ≈ 0.95) over ≈20–120 W/kg, within a narrow calcium range (≈56–79 nM). Turning uses left–right calcium differences.
- **Namiki et al. 2022** (Curr Biol, DNg02): "a population of at least 15 DNg02 cell pairs".
  - Activating more cells raises wingbeat amplitude over a wide range ("population code").
  - Peak activation drove amplitude–frequency pairs along a power isoline (P*mech ≈ 200 W/kg), suggesting "peak activation of the indirect flight muscle motor neurons".
- **Hürkey:** the working range is ≈3–12 Hz MN at ≈150–250 Hz wingbeat (§1.2, §2.7). Each MN spike adds a Ca²⁺ transient (rise 6 ms, decay 80 ms) that sums from 2 Hz up.
- **Rule of thumb for brainfly [D]:**
  - Across flies, wingbeat ≈ 161 + 5.6 × MN rate (Hz). Within a fly the slope is ≈3.2 Hz per Hz.
  - Rates of 3, 6, 9 and 12 Hz map to ≈178, 194, 211 and 228 Hz across flies.
  - Wingbeat amplitude also rises with power: profile power ∝ (frequency × amplitude)³ (Gordon & Dickinson 2006; Namiki et al. 2022).

---

## 6. Identity and inputs in connectomes

- **Names:**
  - MANC and MaleCNS: "DLMn a, b" = MN5 (fibres a, b = 6, 5), and "DLMn c-f" = MN1–4, which are not individually typed.
  - FANC: "DLM1–5". "We differentiated the first four DLMs based on the position of their axons along the anterior–posterior axis; DLM5… is identifiable by its large contralateral cell body… we labelled the DLM MN with the anteriormost axon as DLM1" (Azevedo et al. 2024). That is a heuristic, not a fibre-verified identity.
  - Ikeda & Koenig 1988's soma rules (§4) are the only published route to tell MN1–4 apart from morphology.
- **MaleCNS v1.0** (brainfly's `~/fly-data/brain.npz`/`counts.npz`, minconf 0.5; my query, [D]):
  - 10 DLMn.
    - Left somata: c-f 800718, 800890, 801895, 803013; a,b 801970.
    - Right somata: c-f 801998, 802544, 803048, 1050014552; a,b 801295.
  - PSI_L (802401) synapses onto the four right c-f (35–67 synapses) and the left a,b (17). PSI_R (903327) synapses onto the four left c-f (24–68) and the right a,b (26).
  - So each **DLM unit = 4 c-f plus the a,b whose soma is on the other side**, matching MN5's contralateral soma. escape_circuit.md reached the same grouping.
- **Inputs per DLMn:**
  - 6,995–10,697 input synapses from 438–603 neurons.
  - VNC intrinsic 84–90%, DNs 6–10.5%, ANs 2–4%. GABA/Glu/His-signed share 34–39%.
  - Main inputs, all ten alike:
    - IN19B043 (+, 9–12.5%) and IN19B067 (+, 9–12%);
    - IN03B089 (−, 5–8.5%) and IN06B066 (−, 5–7.7%);
    - IN17A071/081 (+, 2.5–5%), IN19B075 (+, 2.5–4.4%), IN03B086_d (−, 2–4%), IN18B034, IN19B040, IN06B077.
  - Direct DN input, synapses per DLMn: DNp31 39–201, DNa08 16–149, DNp03 16–101, DNg02 (29 cells) 28–111, DNg27 1–84.
  - GF (DNp01) makes 0 chemical synapses onto DLMn. Its route is GF→PSI (electrical) →DLMn.
  - DLMn→DLMn chemical synapses: 0–12 per pair, i.e. essentially none, consistent with Brp-short.
- **Shared input:**
  - Cosine similarity of input vectors: 0.87–0.96 among the four c-f of one side. The a,b neuron resembles its own unit's c-f at 0.81–0.89 and the other unit's at 0.72–0.81.
  - The 296–301 neurons that contact all five MNs of a unit carry 88–95% of each MN's input synapses.
  - **So the connectome drive is common and highly correlated, unlike the Hürkey model's independent noise.**
- **Cheong et al. 2026** (eLife 96084, MANC):
  - "all power MNs receive heavy shared input from a population of ~21 pairs of wing upper tectular intrinsic neurons ('Tect IN')… (mean of 22 synapses per Tect IN with each power MN), together they comprise 7–23% of total input to each power MN". They are likely cholinergic (hemilineage 19B), with 7% recurrent input among themselves.
  - DNa08 and DNp31 are "the strongest direct DN inputs to power MNs". IN06B066 (likely GABAergic, 6B) "inhibits the DLMns".
  - The Tect INs target the octopaminergic mesVUM-MJ.
  - They read the diffuse input as consistent with "prior theory that power MNs summate many weak excitatory inputs to drive staggered spiking (Harcombe and Wyman, 1977)". They note "power MN spiking (~5 Hz)".
- **Lesser et al. 2024** (FANC premotor):
  - "dorsolongitudinal motor units (DLMs, five MNs)… contract at around 200 Hz (asynchronously from the approximately 6 Hz firing rates of their MNs)".
  - Within the wing power modules the first principal component of premotor input explains > 90% of the variance, i.e. common drive.
  - FANC: GF-coupled preMNs (GFC2, GFC4) also target DLM MNs (Azevedo et al. 2024).
- **Electrical synapses in connectomes:**
  - None is annotated. "Sample-preserving imaging approaches such as serial-section transmission electron microscopy have the capacity for higher-resolution imaging at identified locations, potentially enabling visualization of gap junctions" (Azevedo et al. 2024).
  - Cheong et al. rank-ordered INs with few presynaptic sites to find candidate electrical INs; DLMns aren't discussed there.
- **ShakB isoforms:**
  - In the GF circuit: ShakB(N+16) presynaptic in the GF and ShakB(L) in TTMn/PSI, forming rectifying heterotypic junctions (Phelan 2008, via [T]).
  - In DLM MNs: pan-shakB RNAi abolishes coupling, N+16 overexpression strengthens it, and N- or L-specific RNAi does nothing [T].
- **GF/PSI escape input:** see escape_circuit.md: GF→DLM latency 1.3–1.7 ms; PSI→DLMn 0.3–0.5 ms; DLM following 84% at 100 Hz.

---

## 7. Theory relevant to a brainfly (LIF) implementation

- **Hürkey's condition** (conductance model): weak coupling plus a PRC that falls through phase 0.5. Their SNL/HOM type has phase advance early in the ISI and delay late in the odd part, which gives antiphase per pair and a splay state for 5.
  - Stronger Shab (SNIC/Hopf) gives synchrony. CC > 0.21 synchronizes; 0.05–0.21 is multistable.
- **Lewis & Rinzel 2003** (LIF pair, gap junction g(v_j − v_i) plus a delta "spike effect" β; weak coupling, identical, noise-free):
  - "The term… scaled by β accounts for the effect of the suprathreshold portion of the spike. This term… always tends to synchronize the cells".
  - With β = 0, "the synchronous state… is unstable and the antisynchronous state φ* = 0.5 is stable for all I… This can be understood in terms of the effect of the fast reset (repolarization)".
  - With β > 0, synchrony stays stable. Antisynchrony is also stable below a critical drive I_c* where β = (I_c* − ½) ln(I_c*/(I_c* − 1)) − 1, and it "increases in dominance as intrinsic frequency decreases".
  - "the cells take on the order of 1/g_tot cycles to appear phase-locked. Thus, if g_tot ∼ 0.01, then hundreds of cycles are needed".
- **LIF critical rates [D]:** threshold 1, reset 0, period T = τm ln(I/(I − 1)).
  - β = 0.1 gives a critical rate of 45 Hz at τm = 20 ms (60 Hz at τm = 15 ms). β = 0.5 gives 19 Hz (26 Hz); β = 1 gives 13 Hz (17 Hz).
  - Flies' 3–12 Hz is below all of these, so an LIF pair with reset-transmitting gap junctions should sit in the bistable or antiphase-dominant regime.
  - But an LIF with τm = 20 ms firing at 6 Hz needs I ≈ 1.00024 × threshold: it is fluctuation-driven, and its CV will exceed flies' 0.2 unless something slow (adaptation, an AHP current) regularizes it.
- **Chow & Kopell 2000** (not read; per Lewis & Rinzel the same bifurcation structure except at very high rates) and **Ostojic, Brunel & Hakim 2009** (cited by Hürkey; noise and heterogeneity) are the other standard references.
- **Spike-only excitatory pulse coupling** is exactly brainfly's current electrical-synapse rule: "A spike of neuron i also raises each of its electrical partners… by gw mV at once (no delay, no depression)" (`brainfly/hybrid.py`).
  - It is the β-only term above, which always synchronizes. For leaky integrate-and-fire oscillators with instantaneous excitatory pulses this is the Mirollo–Strogatz (1990) synchrony result (classic; not re-read).
  - Not yet committed: on 2026-10-11 the working tree had `HybridBrain.set_coupling(ratio)`.
    - Each step a coupled neuron moves by (1 − e^(−dt/τm)) × ratio × (u_j − u_i), with ratio = g_c/g_L = CC/(1 − CC) each way.
    - Its docstring says "a partner's subthreshold changes reach it, and so does a partner's reset after a spike". The spikelet can still be added through `gap`.
    - That is Lewis & Rinzel's g_c(v_j − v_i) + β model, the configuration this test needs.
  - Flies' coupled MNs instead pass a hyperpolarizing AHP four times more effectively than the spike.
  - [D] A faithful test needs a continuous junction current (subthreshold and reset/AHP both pass), or at least a delayed inhibitory component per partner spike: ≈ −0.5 mV peaking ≈35 ms and lasting ~100 ms at CC 0.01–0.02 (§2.9).

---

## 8. For the pre-registered test: what to impose, what to measure, what blocks it

**Impose (from data):**
- Coupling pairs: 1–2 and 3–4 strong (CC 0.023), the other MN1–4 pairs weak (0.011). MN5 is unmeasured; the paper's model used half the MN1–4 mean, i.e. ≈0.0075 in measured-CC units [D].
  - Choose a stated CC→conductance rule. The model's g = CC·g_L/(1 − CC) ignores the 20 ms peak-ratio measurement.
  - Since c-f identities are unknown, assign the pairs in each unit arbitrarily (or by input similarity [D]: left {800718, 800890} + {801895, 803013}; right {801998, 802544} + {803048, 1050014552}, weak evidence). Pre-register the assignment.
- Cross-side coupling (Koenig & Ikeda's left–right coupling; MN5 dye coupling across sides) is unmeasured. Leave it out, or treat it as a sensitivity arm.
- Drive: unpatterned, shared, setting rates in 3–12 Hz (target ≈6 Hz) with CV 0.15–0.3, all 5 rates within ≈10% (MN5 up to 26% higher allowed).

**Measure (flies' values; use the authors' definitions, §1.8):**
- Coupled:
  - splayness (N = 5) 0.73–0.79;
  - MN4–5 r 0.49–0.63 and dip10 0.02–0.10;
  - strong-pair r 0.27–0.51, circular mean 0.40–0.65;
  - preferred-order share 48–70% (sliding windows) or 0.51–0.79 (complete cycles);
  - ≤ 3 ms coincidences ≤ chance.
- Uncoupled (shakB RNAi):
  - r 0.56–0.72, dip10 0.18–0.41, splayness 0.52–0.69 (n = 2);
  - preferred share ≈ 27–39%; coincidences 1.2–2.7× chance; rates unchanged.
- Positive control (strong coupling, CC ≳ 0.2): r → 0.84–1.0.
- Report the CC = 0 model against independent-phase nulls (r 0.637, dip10 0.20, splayness 0.59). With shared connectome input, the uncoupled model should lean in-phase, like flies.

**Would block or weaken the test:**
1. **The electrical synapse rule.**
   - Brainfly's committed spike-only excitatory kicks are expected to synchronize, the opposite of the effect tested.
   - The test needs a continuous g(Vj − Vi) term, so the reset/AHP passes as hyperpolarization. The uncommitted `set_coupling` provides one.
   - Calibrate its ratio to CC 0.023 / 0.011 (ratio 0.0235 / 0.0111). Choose the reset depth so a partner's post-spike drop resembles flies' (AHP ≈14 mV, >100 ms). Add a spikelet only at overshoot CC ≈ 0.01.
2. **Missing data from connectomes.**
   - No gap junctions and no MN1–4 identities, so every coupling value is imposed: a test of dynamics, not of the connectome.
   - MN5 coupling is unmeasured.
3. **Neuron class.**
   - Hürkey's mechanism rests on a HOM/SNL PRC that was never measured in flies.
   - An LIF works through a different route (reset transmission at low rates) and is bistable with synchrony whenever spikes are transmitted.
4. **Quiet DLMn and correlated drive.**
   - Brainfly's DLMn are currently biased ≈12–13 mV below threshold to stay quiet at rest (rung 6). A flight drive state must be defined first.
   - 88–95% of DLMn input is shared, which pushes toward in-phase firing. The Hürkey model had no shared noise.
5. **Duration and statistics.**
   - Lock-in takes ~1/CC cycles: 60–300 s of simulated flight per condition and several seeds.
   - In flies the coupled/uncoupled contrast in r is small (0.56 against 0.61, p = 0.03). dip10, splayness and coincidence rates separate the genotypes better.
   - Five-unit RNAi data exist for only 2 flies (Zenodo) or 3 (thesis).
6. **Order asymmetry.** 1423 > 1324 can't come from symmetric coupling. Score the preferred pair together.

---


**Note (2026-10-11, after a review).** `HybridBrain.set_coupling` was committed in 7fc9c42; the "uncommitted" remarks in
summary 15, §7 and §8 predate it. §8.1's "ratio 0.0235 / 0.0111" is the steady-state conversion that §8's first point
warns against. Flies' CCs are 20 ms peak ratios; in a 20 ms membrane the conductance that reproduces them is about 1.8
times larger (0.0423 / 0.0199), and 1.5-1.6 times in a 13-15 ms one.

## Sources

- Hürkey S, Niemeyer N, Schleimer J-H, Ryglewski S, Schreiber S, Duch C (2023) Nature 618:118–125.
  - https://doi.org/10.1038/s41586-023-06099-0
  - Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC10232364/
  - Supplementary Tables 1–5: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-023-06099-0/MediaObjects/41586_2023_6099_MOESM1_ESM.pdf
  - Figures: https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41586-023-06099-0/MediaObjects/41586_2023_6099_Fig1_HTML.png (Fig2–4 likewise; ED figures as …_Fig5_ESM.jpg to …_Fig14_ESM.jpg)
- Zenodo, Hürkey model code and spike trains (drosophila_wing_cpg.zip): https://doi.org/10.5281/zenodo.7740678 (https://zenodo.org/records/7740678)
- Zenodo, Hürkey source data (Figure 1.xlsx, Figure 2.xlsx, recordings): https://doi.org/10.5281/zenodo.7737730 (https://zenodo.org/records/7737730)
- Hürkey S (2024) PhD thesis, "Mechanisms and function of asynchronous flight motor pattern generation", JGU Mainz: https://openscience.ub.uni-mainz.de/bitstream/20.500.12030/10095/1/mechanisms_and_function_of_as-20240214121930397.pdf
- Hürkey et al. bioRxiv preprint (not read): https://www.biorxiv.org/content/10.1101/2022.02.02.478622
- Berger SD, Crook SM (2015) Front Comput Neurosci 9:139: https://pmc.ncbi.nlm.nih.gov/articles/PMC4649037/
- Gordon S, Dickinson MH (2006) PNAS 103:4311: https://pmc.ncbi.nlm.nih.gov/articles/PMC1449689/
- Lehmann F-O, Bartussek J (2017) J Comp Physiol A (review): https://pmc.ncbi.nlm.nih.gov/articles/PMC5263198/
- Ryglewski S et al. (2014) PNAS 111:18049: https://pmc.ncbi.nlm.nih.gov/articles/PMC4273390/
- Ryglewski S et al. (2017) Neuron 93:632: https://pmc.ncbi.nlm.nih.gov/articles/PMC5614441/
- Harcombe ES, Wyman RJ (1977) J Neurophysiol 40:1066: https://doi.org/10.1152/jn.1977.40.5.1066
- Harcombe ES, Wyman RJ (1978) J Comp Physiol 123:271: https://doi.org/10.1007/BF00656881
- Koenig JH, Ikeda K (1980) J Exp Biol 87:121: https://doi.org/10.1242/jeb.87.1.121
- Koenig JH, Ikeda K (1980) J Exp Biol 87:137: https://doi.org/10.1242/jeb.87.1.137
- Koenig JH, Ikeda K (1980) J Neurobiol 11:509: https://doi.org/10.1002/neu.480110510
- Koenig JH, Ikeda K (1983) J Comp Physiol 150:295: https://doi.org/10.1007/BF00605019
- Koenig JH, Ikeda K (1983) J Comp Physiol 150:305: https://doi.org/10.1007/BF00605020
- Ikeda K, Koenig JH, Tsuruhara T (1980) J Neurocytol 9:799: https://doi.org/10.1007/BF01205020
- Ikeda K, Koenig JH (1988) J Comp Neurol 273:436: https://doi.org/10.1002/cne.902730312
- Levine JD, Wyman RJ (1973) PNAS 70:1050: https://pmc.ncbi.nlm.nih.gov/articles/PMC433423/
- Wyman RJ (1969) J Neurophysiol 32:297: https://doi.org/10.1152/jn.1969.32.3.297
- Wyman RJ (1969) J Neurophysiol 32:307: https://doi.org/10.1152/jn.1969.32.3.307
- Wyman RJ (1966) J Neurophysiol 29:807: https://doi.org/10.1152/jn.1966.29.5.807
- Wyman RJ (1965) Biophys J 5:447: https://doi.org/10.1016/S0006-3495(65)86729-7
- PubMed abstracts used (efetch): https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=409808,6775052,6775035,7420011,6162923,3145293,4306895,4306896&rettype=abstract&retmode=text
- Semantic Scholar records (TLDRs for the 1978 and 1983 papers): https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/BF00656881?fields=title,tldr and https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/BF00605020?fields=title,tldr
- Cheong HSJ et al. (2026) eLife 96084 (MANC premotor circuits): https://elifesciences.org/articles/96084 (text via https://api.elifesciences.org/articles/96084)
- Azevedo A et al. (2024) Nature (FANC): https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/
- Lesser E et al. (2024) Nature (leg and wing premotor networks): https://pmc.ncbi.nlm.nih.gov/articles/PMC11356479/
- Namiki S et al. (2022) Curr Biol (DNg02): https://pmc.ncbi.nlm.nih.gov/articles/PMC9206711/
- Berg S et al. (2025) MaleCNS connectome, bioRxiv: https://doi.org/10.1101/2025.10.09.680999 (synapse tables used through brainfly's `~/fly-data` build)
- Lewis TJ, Rinzel J (2003) J Comput Neurosci 14:283: https://www.math.ucdavis.edu/~tjlewis/pubs/lewisjcns03.pdf
- Chow CC, Kopell N (2000) Neural Comput 12:1643 (not read): https://doi.org/10.1162/089976600300015295
- Ostojic S, Brunel N, Hakim V (2009) J Comput Neurosci 26:369 (not read): https://doi.org/10.1007/s10827-008-0117-3
- Mirollo RE, Strogatz SH (1990) SIAM J Appl Math 50:1645 (not re-read): https://doi.org/10.1137/0150098
- Gutierrez GJ, Wang Y (2023) Curr Biol dispatch on Hürkey (not read): https://doi.org/10.1016/j.cub.2023.06.058
- Schlurmann M, Hausen K (2007) J Comp Neurol 500:448 (via Hürkey and the thesis): https://doi.org/10.1002/cne.21182
- Internal: `brainfly/hybrid.py` (the current electrical-synapse rule) and `research_notes/Embodied fly connectome simulation/escape_circuit.md` (GF/PSI→DLMn).
