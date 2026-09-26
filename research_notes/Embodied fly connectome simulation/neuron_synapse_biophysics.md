# Drosophila neuron and synapse biophysics for per-cell-type whole-CNS connectome simulation

Notes compiled 2026-09-25 for a project simulating Janelia MaleCNS v1.0 (166,691 neurons, 25.6M edges) as identical LIF units (tau 100 ms, threshold 1, reset 0, 20 ms steps, synapse-count weights, sign from predicted transmitter, inputs normalised to sum 1). Conventions: "preprint" = not peer-reviewed as of Sept 2026; "derived" = arithmetic I did on published numbers (flagged in Inferences where it matters). DOIs were checked against Europe PMC metadata; key numbers were pulled from full texts where open access.

## 1. Which fly neuron classes spike, which are graded/non-spiking, and is there a systematic list or database?

### Takeaway
Spiking vs graded signalling is known from direct intracellular recordings for only a small number of Drosophila cell types, and no systematic database exists. The pattern that emerges is that photoreceptors, lamina monopolar cells, the medulla columnar and T4/T5 motion pathway, amacrine-like wide-field cells (CT1, APL, "patchy" antennal-lobe LNs), some VNC premotor interneurons, and a few descending neurons are graded or nonspiking. Long-range projection neurons (ORNs, PNs, KCs, MBONs, DANs, central-complex columnar cells, most DNs, motor neurons) spike. Expression of the only fly Na<sub>V</sub> gene (*para*) is not a reliable marker of spiking.

### Cited Findings

#### Photoreceptors and lamina (graded)
- LMCs (lamina monopolar cells) respond to light with transient *hyperpolarisations* reaching 45 mV. LMC resting potentials were −40 to −70 mV, and photoreceptor axons rested at −65 to −80 mV. Photoreceptor axons begin to depolarise ~9 ms after light onset, set by the absolute phototransduction delay. In *ort* (histamine receptor) mutants, the maximal LMC response drops from >40 mV (WT) to >15 mV — [Zheng et al. 2006, J Gen Physiol](https://doi.org/10.1085/jgp.200509470)
- L1 and L2 hyperpolarise to light increments and depolarise to decrements (graded contrast signals feeding the motion pathways) — [Behnia et al. 2014, Nature](https://doi.org/10.1038/nature13427)
- R7/R8 are linked to R6 by gap junctions in the lamina, and depolarising responses in some LMCs suggest gap junctions between L2 and R8 axons. This is electrical coupling among graded cells — [Wardill et al. 2012, Science](https://doi.org/10.1126/science.1215317)

#### Medulla, T4/T5, amacrine cells (graded)
- In in-vivo whole-cell current clamp, Mi1 and Tm3 give transient depolarisations at light onset and hyperpolarise at offset. Tm1 and Tm2 do the opposite. The offset/onset asymmetry was 11% (Mi1), 36.6% (Tm3), 26.1% (Tm1) and 17.7% (Tm2), reported as membrane-potential changes. My full-text search found no spikes reported — [Behnia et al. 2014](https://doi.org/10.1038/nature13427)
- The authors expected T4 cells to signal through graded synapses. T4 recordings "only occasionally feature very weak, fast transients (~1–2 mV) that could not be verified as spikes", so the analysis used graded subthreshold responses — [Gruntman, Romani & Reiser 2018, Nat Neurosci](https://doi.org/10.1038/s41593-017-0046-4)
- Nonetheless, *para* (Na<sub>V</sub>) protein is "strongly expressed in the axonal fibers connecting dendrites and axon terminals" of T4/T5, and Ih is found on T4/T5 dendrites. GABA-B-R1 was not detected in T4/T5 — [Fendl, Vieira & Borst 2020, eLife](https://doi.org/10.7554/eLife.62953)
- Voltage imaging (GEVI) of the OFF pathway shows that direction-selective voltage signals arise through linear spatial summation — [Wienecke, Leong & Clandinin 2018, Neuron](https://doi.org/10.1016/j.neuron.2018.07.005)
- CT1 (amacrine-like, spanning ~700 columns in two neuropils) has highly compartmentalised retinotopic responses in neighbouring terminals, "with each terminal acting as an independent functional unit" — [Meier & Borst 2019, Curr Biol](https://doi.org/10.1016/j.cub.2019.03.070)

#### Lobula plate tangential cells (graded with small spikes; coupled)
- HS cells (HSN/HSE/HSS) in the first Drosophila whole-cell recordings rested at about −55 mV with input resistance 100–200 MΩ (n = 25). Neurobiotin coupling linked ipsilateral HS cells to each other and to contralateral-dendrite tangential cells — [Schnell et al. 2010, J Neurophysiol](https://doi.org/10.1152/jn.00950.2009). The resting potential and input-resistance values come from the paper's reported results via search summary; I could not open the full text (paywalled).
- VS cells show lateral connections that widen receptive fields — [Joesch et al. 2008, Curr Biol](https://doi.org/10.1016/j.cub.2008.02.022)
- VS peak-to-peak responses roughly double during flight, and passive membrane resistance falls, consistent with increased synaptic drive — [Maimon, Straw & Dickinson 2010, Nat Neurosci](https://doi.org/10.1038/nn.2492)

#### Descending neurons (mostly spiking, some graded)
- The giant fiber (GF, DNp01) fires single spikes, and GF spike timing relative to parallel circuits selects short vs long escape takeoffs — [von Reyn et al. 2014, Nat Neurosci](https://doi.org/10.1038/nn.3741); [Ache et al. 2019, Curr Biol](https://doi.org/10.1016/j.cub.2019.01.079)
- Among visual DNs, **DNOVS1 is nonspiking**, while DNOVS2 and DNHS1 fire small spikes riding on graded potentials. Rate–voltage gains were 8.2–8.8 Hz/mV (DNOVS2) and 3.9–5.9 Hz/mV (DNHS1) — [Suver et al. 2016, J Neurosci](https://doi.org/10.1523/JNEUROSCI.2277-16.2016)
- The steering DNs DNa01 and DNa02 spike and can be told apart by spike waveform in dual recordings — [Rayshubskiy et al. 2025, eLife](https://doi.org/10.7554/eLife.102230)

#### Antennal lobe
- ORNs spike. Their spike-generation step acts as a stereotyped differentiating linear filter that depends on Na<sup>+</sup> channel levels — [Nagel & Wilson 2011, Nat Neurosci](https://doi.org/10.1038/nn.2725)
- PNs spike. With somatic current injection they sustain >100 spikes/s for 500 ms, ending at 104.2% of their initial rate (n = 8) — [Kazama & Wilson 2008, Neuron](https://doi.org/10.1016/j.neuron.2008.02.030)
- LNs: in one large survey, every LN recorded fired spontaneous action potentials with odour-modulated spiking. Most LNs are GABAergic, "a large number of (mostly ventral)" LNs are glutamatergic and a few are dopaminergic — [Chou et al. 2010, Nat Neurosci](https://doi.org/10.1038/nn.2489)
- **Nonspiking LNs exist.** "Patchy" LNs labelled by R32F10-Gal4 lack detectable voltage-gated Na<sup>+</sup> current and show spatially restricted, odour-specific activity. They *transcribe* *para* normally but carry much less Para protein (FlpTag), pointing to post-transcriptional control — [Schenk & Gaudry 2023, eNeuro](https://doi.org/10.1523/ENEURO.0109-22.2022)
- Excitatory cholinergic LNs (eLNs) connect to PNs electrically, not chemically (see Q5) — [Yaksi & Wilson 2010, Neuron](https://doi.org/10.1016/j.neuron.2010.08.041)

#### Mushroom body
- KCs spike sparsely. PN→KC EPSPs decay rapidly, each KC receives input from about 10 PNs, and KC firing thresholds are high — [Turner, Bazhenov & Laurent 2008, J Neurophysiol](https://doi.org/10.1152/jn.01283.2007)
- α′/β′ KCs generate spikes most readily of the three KC classes, even though glomerular inputs sum similarly in all of them — [Inada, Tsuchimoto & Kazama 2017, Neuron](https://doi.org/10.1016/j.neuron.2017.06.039)
- **APL is nonspiking** (no somatic action potentials, like the locust GGN), and its activity can stay spatially localised within the lobes — [Amin et al. 2020, eLife](https://doi.org/10.7554/eLife.56954)
- MBON-γ1pedc fires high spike rates during 1 s odours, and PPL1-γ1pedc DANs fire reliable spike trains when optogenetically driven — [Hige et al. 2015, Neuron](https://doi.org/10.1016/j.neuron.2015.11.003)

#### Central complex, clock, sleep circuits
- Whole-cell recordings of P-EN and E-PG neurons show spike rates tuned to heading and angular velocity — [Turner-Evans et al. 2017, eLife](https://doi.org/10.7554/eLife.23496)
- Sleep-drive EB ring neurons (R5) switch from tonic spiking to burst firing after sleep loss — [Liu et al. 2016, Cell](https://doi.org/10.1016/j.cell.2016.04.013)
- l-LNv clock neurons: during the day, RMP −41.5 ± 1.1 mV and 3.1 ± 0.4 Hz with high-rate burst firing. At night, −45 ± 3 mV and 1.7 ± 0.5 Hz with tonic or no firing. Somatic AP duration is ~23 ms — [Sheeba et al. 2008, Curr Biol](https://doi.org/10.1016/j.cub.2008.08.033)

#### Ventral nerve cord and antennal motor system
- Leg proprioceptive interneurons: all 13Bα cells lacked detectable action potentials, and in 10Bα cells current injection failed to evoke identifiable APs. 9Aα cells fire small spikes, and 9Aα2 cells have larger spikes (>2 mV at the soma) — [Agrawal et al. 2020, eLife](https://doi.org/10.7554/eLife.60299)
- A 2025 VNC modelling study chose a rate model "in part because many neurons in the insect VNC, including premotor neurons active during walking, are nonspiking" — [Pugliese et al. 2025, bioRxiv preprint](https://doi.org/10.1101/2025.09.12.675944)
- APN2 (AMMC projection neuron 2) is a nonspiking interneuron. It gives graded hyperpolarisations to antennal displacement and integrates motor-command signals — [Nunn et al. 2026, bioRxiv preprint](https://doi.org/10.64898/2026.04.16.718965)
- Leg motor neurons spike; an intermediate tibia flexor MN rested at ~−51 mV with a spontaneous rate of 28 Hz — [Azevedo et al. 2020, eLife](https://doi.org/10.7554/eLife.56754)
- Flight motor neurons (the asynchronous-flight CPG) spike. Weak electrical synapses between them produce splayed, desynchronised firing — [Hürkey et al. 2023, Nature](https://doi.org/10.1038/s41586-023-06099-0)

#### Molecular markers and why they fail
- A *para*-T2A-GAL4 reporter labels 94 ± 5% of Elav<sup>+</sup> neurons in the adult central brain and thoracic ganglion, versus 23 ± 1% of neurons in the embryonic/larval CNS. Para protein sits at a distal axonal segment, the spike initiation zone (an AIS-like domain) — [Ravenscroft et al. 2020, J Neurosci](https://doi.org/10.1523/JNEUROSCI.0142-20.2020)
- Counter-examples: graded T4/T5 carry axonal Para protein ([Fendl et al. 2020](https://doi.org/10.7554/eLife.62953)), and nonspiking patchy LNs transcribe *para* ([Schenk & Gaudry 2023](https://doi.org/10.1523/ENEURO.0109-22.2022))

#### Systematic lists and how existing models handle it
- The whole-brain LIF model "does not account for gap junctions, non-spiking neurons, internal state or long-range neuropeptides, and assumes that the basal firing of each neuron is zero" — [Shiu et al. 2024, Nature](https://doi.org/10.1038/s41586-024-07763-9)
- The optic-lobe DMN models all 64 cell types (45,669 neurons) as "passive leaky linear non-spiking" units with threshold-linear output — [Lappalainen et al. 2024, Nature](https://doi.org/10.1038/s41586-024-07939-3)
- Searches for a compiled Drosophila electrophysiology database (a NeuroElectro-like resource) found none. Existing resources are connectome/annotation tools (neuPrint, Codex, Virtual Fly Brain) that record no spiking status — [male-cns.janelia.org portal](https://male-cns.janelia.org/); [FlyWire Codex BANC](https://codex.flywire.ai/banc)

### Inferences
- A defensible first-pass "graded" flag for the MaleCNS would cover:
  - all photoreceptors, lamina intrinsic cells and lamina monopolar cells;
  - medulla columnar Mi/Tm/TmY and T4/T5 types (each directly recorded type has been graded);
  - amacrine-like wide-field cells (CT1, APL, R32F10-type patchy LNs);
  - specific recorded VNC and antennal interneurons (13Bα, 10Bα, APN2) and DNOVS1.

  Everything else would default to spiking. The optic-lobe part of this flag is large: one optic lobe alone holds ~53,000 neurons in 732 types ([Nern et al. 2025](https://doi.org/10.1038/s41586-025-08746-0)), so it is a large fraction of the 166,691 neurons.
- Morphology fits the pattern: compact local or amacrine cells tend to be graded, and long-axon projection neurons spike. This matches Para being concentrated at a distal axonal SIZ. It is a plausible prior for unrecorded types, but it is not validated (T4/T5 have axonal Para yet are graded).
- *para* transcript or protein presence cannot be used to label spiking types. The larval figure (23%) versus the adult figure (94%) also warns against transferring larval physiology to adults.
- VNC hemilineages 13B and 10B include nonspiking members. Generalising "nonspiking" to whole hemilineages is tempting because hemilineages share transmitter identity (Q4), but only a few subtypes have been recorded.
- My rough judgement from the literature reviewed: direct intracellular spiking status is known for well under 5% of the ~11,700 MaleCNS cell types. Most assignments will therefore have to be priors plus validation against calcium or voltage imaging.

### Gaps
- No systematic database or count of spiking vs nonspiking cell types; I found no source quantifying coverage.
- Lobula/lobula-plate VPNs (LC/LPLC types) are widely assumed to spike, but in this search I did not find or verify whole-cell evidence type by type (much of the functional data is calcium imaging).
- I found no intracellular recordings in this search for L3–L5, C2/C3, T1, Lawf, Mi4/Mi9, Dm/Pm, LPi, or most central-brain local neurons.
- The fraction of AL LNs that are nonspiking is unknown ([Schenk & Gaudry 2023](https://doi.org/10.1523/ENEURO.0109-22.2022) characterised one class and did not estimate a fraction).
- Seki et al. 2010 ([J Neurophysiol](https://doi.org/10.1152/jn.00249.2010)) characterised LN physiology, but I could not access its full text to check its spiking/nonspiking classification.

## 2. Measured electrophysiological parameters by cell type (membrane time constant, input resistance, resting potential, threshold, rates, adaptation, bursting), morphology effects, and compiled databases

### Takeaway
Input resistance spans about two orders of magnitude across measured types: ~50–100 MΩ in the giant fiber, 100–200 MΩ in HS cells, 150–700 MΩ in leg MNs, ~600 MΩ in AL PNs, ~1 GΩ in KCs and ~5 GΩ in T4. Membrane time constants run from a few ms (large DNs, model-derived) to ~15–30 ms (PNs, derived from fitted cable parameters). All are far shorter than the project's 100 ms. Drosophila neurons are unipolar: the soma hangs off a thin primary neurite outside the signalling path, and spikes start in the proximal axon. Somatic recordings therefore see attenuated spikes and imperfect voltage control. No compiled electrophysiology database exists; values are scattered across single-cell-type papers.

### Cited Findings

#### Cable properties and unipolar morphology
- Compartmental fits to AL PNs (DM1) gave:
  - specific membrane resistance R<sub>m</sub> = 8.3, 20.4 and 20.8 kΩ·cm²;
  - specific capacitance C<sub>m</sub> = 2.6, 1.5 and 0.8 µF/cm²;
  - axial resistivity R<sub>i</sub> = 163.9, 102.5 and 266.1 Ω·cm, for three cells.

  Alternative dendritic-tuft models gave R<sub>m</sub> 19.2–26.4 kΩ·cm², C<sub>m</sub> 0.61–0.80 µF/cm² and R<sub>i</sub> 224–311 Ω·cm. The literature range for R<sub>i</sub> is 30–400 Ω·cm — [Gouwens & Wilson 2009, J Neurosci](https://doi.org/10.1523/JNEUROSCI.0764-09.2009); model code: [ModelDB 118662](https://modeldb.science/118662)
- Other findings from the same study:
  - PNs "are electrotonically extensive", and somatic voltage is "substantially attenuated in the dendrite and severely attenuated in the axon", largely along the primary neurite.
  - The best fit put spike initiation "near the start of the axon, just distal to the location where the primary neurite bifurcates".
  - Unitary ORN input could only be reproduced by "dozens of release sites distributed across many dendritic branches".
  - Input resistance was 598.0 ± 69.3 MΩ (n = 14, antennae removed).
  - Seal resistance was 10.1 ± 1.6 GΩ, so going whole-cell depolarises the cell by several mV. Published in-situ resting potentials of −50 to −60 mV are therefore likely too depolarised, and a leak Na<sup>+</sup> conductance also contributes.
  - About 3 synchronous unitary ORN inputs should bring a PN from rest to threshold.

  Sources: [Gouwens & Wilson 2009](https://doi.org/10.1523/JNEUROSCI.0764-09.2009); [Wilson 2013 review, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)
- Looming-responsive DNs, multicompartment fits on EM morphologies:
  - DNp01 (GF): g<sub>leak</sub> = 4.35×10⁻⁴ S/cm², E<sub>rev</sub> = −66.6 mV, R<sub>a</sub> = 212 Ω·cm, C<sub>m</sub> = 0.7 µF/cm².
  - DNp03: g<sub>leak</sub> = 3.17×10⁻⁴ S/cm², E<sub>rev</sub> = −61.2 mV, R<sub>a</sub> = 50 Ω·cm, C<sub>m</sub> = 0.8 µF/cm².
  - Single-synapse EPSPs vary widely at the synapse (DNp01 0.2–5 mV; DNp03 0.2–1.7 mV) but are normalised at the SIZ to 0.045–0.061 mV (DNp01) and 0.16–0.19 mV (DNp03).

  Source: [Moreno-Sanchez et al. 2024, bioRxiv / eLife reviewed preprint](https://doi.org/10.1101/2024.04.24.591016)
- In a larval motoneuron (aCC/MN1-Ib) model, the SIZ is predicted on the primary axon 70 µm beyond the most distal dendritic branch point, and currents from the SIZ are filtered on the way to the soma — [Günay et al. 2015, PLoS Comput Biol](https://doi.org/10.1371/journal.pcbi.1004189)
- Para protein localises to a distal axonal segment (the SIZ) in adult CNS neurons — [Ravenscroft et al. 2020](https://doi.org/10.1523/JNEUROSCI.0142-20.2020)
- In EM-constrained LHN models, somatic uEPSP amplitude is predicted by synapse *density* (count divided by postsynaptic surface area), because surface area scales inversely with membrane resistance (r² = 0.77). Axonal connections were severely underpredicted — [Liu et al. 2022, Curr Biol](https://doi.org/10.1016/j.cub.2021.11.056)
- Effective-resistance-matrix analysis of fly visual interneurons suggests some are "multi-output devices", "neither well approximated as 'point neurons' ... nor as collections of functionally independent compartments" — [Seung 2025, bioRxiv preprint](https://doi.org/10.1101/2025.02.02.636137)

#### Per-cell-type measurements (adult unless noted)

| Cell type | Measured values | Source |
|---|---|---|
| AL projection neuron | R<sub>in</sub> 598 ± 69 MΩ; single-ORN uEPSP 6.19 ± 0.45 mV (n = 23); uEPSC 29.0 ± 2.6 pA (n = 45); sustains >100 Hz for 500 ms without decline | [Gouwens & Wilson 2009](https://doi.org/10.1523/JNEUROSCI.0764-09.2009); [Kazama & Wilson 2008](https://doi.org/10.1016/j.neuron.2008.02.030) |
| Kenyon cell (ex-vivo whole brain) | RMP −60.9 ± 1.7 mV; R<sub>in</sub> 0.99–1.13 GΩ; mEPSC 3.8–4.9 pA, rise 1.2–1.5 ms, decay τ 4.5–6.7 ms | [Gu & O'Dowd 2006, J Neurosci](https://doi.org/10.1523/JNEUROSCI.4109-05.2006) |
| Kenyon cell (in vivo) | ~10 PN inputs per KC; rapidly decaying EPSPs; high threshold; somatic responses need several co-active claws (KCs have 5–7 claws), with near-linear summation; α′/β′ most excitable | [Turner et al. 2008](https://doi.org/10.1152/jn.01283.2007); [Gruntman & Turner 2013, Nat Neurosci](https://doi.org/10.1038/nn.3547); [Inada et al. 2017](https://doi.org/10.1016/j.neuron.2017.06.039) |
| T4 (medulla motion detector) | R<sub>in</sub> 5.28 ± 0.12 GΩ in dark (6.70 ± 0.16 GΩ with GluClα RNAi); GluClα knockdown depolarises rest by 11.94 mV (tonic glutamate shunt); motion response 18.10 ± 0.77 mV | [Groschner et al. 2022, Nature](https://doi.org/10.1038/s41586-022-04428-3) |
| HS cells (LPTC) | RMP ≈ −55 mV; R<sub>in</sub> 100–200 MΩ (n = 25) | [Schnell et al. 2010](https://doi.org/10.1152/jn.00950.2009) |
| Giant fiber (DNp01) | R<sub>in</sub> "typically" 50–100 MΩ (used as an inclusion criterion) | [Jang et al. 2023, J Exp Biol](https://doi.org/10.1242/jeb.244790) |
| Tibia flexor MNs | R<sub>in</sub> 150 MΩ (fast), 300 MΩ (intermediate), 700 MΩ (slow); one intermediate MN: −51 mV rest, 28 Hz spontaneous, 486 MΩ | [Azevedo et al. 2020](https://doi.org/10.7554/eLife.56754) |
| l-LNv clock neurons | Day: −41.5 mV, 3.1 Hz, burst firing; night: −45 mV, 1.7 Hz tonic; AP duration ~23 ms | [Sheeba et al. 2008](https://doi.org/10.1016/j.cub.2008.08.033) |
| Lamina LMCs | Rest −40 to −70 mV; light-evoked hyperpolarisation up to 45 mV | [Zheng et al. 2006](https://doi.org/10.1085/jgp.200509470) |
| Visual DNs (DNOVS2, DNHS1) | Small spikes on graded potentials; 8.2–8.8 and 3.9–5.9 Hz/mV | [Suver et al. 2016](https://doi.org/10.1523/JNEUROSCI.2277-16.2016) |
| Nonspiking patchy AL LNs | No detectable voltage-gated Na<sup>+</sup> current | [Schenk & Gaudry 2023](https://doi.org/10.1523/ENEURO.0109-22.2022) |

#### Firing rates, adaptation and bursting
- ORNs: spike generation behaves as a differentiating (adapting) linear filter, and knocking down Na<sup>+</sup> channels reshapes it — [Nagel & Wilson 2011](https://doi.org/10.1038/nn.2725). The brain receives ~20,000 ORN spikes/s even with no odour, from 1,200 ORNs per antenna — [Wilson 2013 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/)
- PN odour responses "accommodate rapidly" (responses were quantified in a 100 ms window starting 100 ms after odour onset) — [Bhandawat et al. 2007, Nat Neurosci](https://doi.org/10.1038/nn1976). The transience comes largely from ORN→PN short-term depression, not from PN intrinsic adaptation: PNs do not adapt to injected current over 500 ms — [Kazama & Wilson 2008](https://doi.org/10.1016/j.neuron.2008.02.030)
- LN diversity: some pan-glomerular LNs shut down completely during odours, sometimes after a brief onset burst. Others show especially transient onset bursts — [Chou et al. 2010](https://doi.org/10.1038/nn.2489)
- Bursting has been documented in l-LNv clock neurons during the day ([Sheeba et al. 2008](https://doi.org/10.1016/j.cub.2008.08.033)) and in R5 ring neurons, which switch from spiking to bursting under sleep pressure ([Liu et al. 2016](https://doi.org/10.1016/j.cell.2016.04.013))
- In the flight CPG, weakly electrically coupled MNs fire in a fixed, splayed sequence from unpatterned premotor drive. Asynchronous flight muscles oscillate at 100–1,000 Hz across insects — [Hürkey et al. 2023](https://doi.org/10.1038/s41586-023-06099-0)
- Mushroom-body scale: ~2,000 KCs converge onto 34 MBONs of 21 types, and MBON tuning curves are highly correlated with one another — [Hige et al. 2015, Nature](https://doi.org/10.1038/nature15396)

#### Parameter sets used by existing fly network models (for comparison)
- Whole-brain LIF (Shiu et al.), from the code defaults: V<sub>rest</sub> = V<sub>reset</sub> = −52 mV, V<sub>th</sub> = −45 mV, τ<sub>m</sub> = 20 ms, refractory 2.2 ms, synaptic delay 1.8 ms, synaptic τ 5 ms, w<sub>syn</sub> = 0.275 mV per synapse, Poisson drive 150 Hz. Parameters trace to [Kakaria & de Bivort 2017](https://doi.org/10.3389/fnbeh.2017.00008). Sources: [model.py](https://github.com/philshiu/Drosophila_brain_model/blob/main/model.py); [Shiu et al. 2024](https://doi.org/10.1038/s41586-024-07763-9)
- VNC rate model (Pugliese et al.), with parameters drawn per neuron and per replicate:
  - τ ~ N(20 ms, 2 ms), computed from R<sub>m</sub> = 10 kΩ·cm² × C<sub>m</sub> = 2 µF/cm²;
  - r<sub>max</sub> ~ N(200, 10) Hz, threshold ~ N(7.5, 0.6), gain ~ N(1, 0.1);
  - gain and threshold normalised by neuron size, because larger neurons have lower input resistance;
  - 18,416 parameters; dt = 0.01 ms.

  Source: [Pugliese et al. 2025, bioRxiv preprint](https://doi.org/10.1101/2025.09.12.675944)
- Optic-lobe DMN (Lappalainen et al.): one τ and one V<sub>rest</sub> per cell type, with τ initialised at 50 ms and trained, plus trainable unitary synapse strengths. That is 734 free parameters (65 τ, 65 V<sub>rest</sub>, 604 scale factors), integrated with dt 5–20 ms — [Lappalainen et al. 2024](https://doi.org/10.1038/s41586-024-07939-3)
- Generic insect-olfaction spiking model with spike-frequency adaptation: C<sub>m</sub> 289.5 pF, g<sub>L</sub> 28.95 nS, E<sub>L</sub> −70 mV, V<sub>th</sub> −57 mV, refractory 5 ms, τ<sub>E</sub> 2 ms, τ<sub>I</sub> 10 ms, adaptation τ 389 ms, ΔI<sub>A</sub> 0.132 nA. These are model choices, not Drosophila measurements — [Betkiewicz, Lindner & Nawrot 2020, eNeuro](https://doi.org/10.1523/ENEURO.0305-18.2020)

### Inferences
- Derived membrane time constants (τ = R<sub>m</sub>·C<sub>m</sub>):
  - PNs ≈ 17–31 ms (20.8×0.8, 8.3×2.6, 20.4×1.5);
  - DNp01 ≈ 1.6 ms (0.7 µF/cm² ÷ 4.35×10⁻⁴ S/cm²);
  - DNp03 ≈ 2.5 ms;
  - Pugliese's generic value 20 ms.

  The project's τ = 100 ms is 3–60× longer than any of these. At dt = 20 ms, per-step retention is e<sup>−0.2</sup> ≈ 0.82 for τ = 100 ms, versus e<sup>−1</sup> ≈ 0.37 for τ = 20 ms and ≈0.02 for τ = 5 ms. The current model therefore integrates over ~5 steps (100 ms) where real neurons integrate over <1 step. This slows propagation and smooths dynamics.
- Input resistance roughly tracks neuron size (GF < HS < MNs < PN < KC < T4). Per-type gain could be estimated from EM morphology (surface area or cable length) without per-type recordings. Liu et al. (synapse density predicts uEPSP) and Pugliese et al. (size-normalised gain/threshold) both did versions of this.
- Thresholds relative to input counts differ enormously. A PN reaches threshold with ~3 synchronous ORN inputs out of ~40 homotypic ORNs ([Kazama & Wilson 2009](https://doi.org/10.1038/nn.2376) give an average of ~40 ORNs per odorant receptor), while a KC needs several of its 5–7 claws. With inputs normalised to sum to 1, a single global threshold of 1 cannot capture both. Per-type thresholds, or per-type gain on the normalised input, are needed.
- With a 20 ms step, the model is effectively a rate model: refractoriness (2 ms), synaptic kinetics (1–6 ms) and bursts are unresolved. Either reduce dt to ≤0.1–0.5 ms for spiking types, or reinterpret the units as rates with per-type τ and a saturating output (Pugliese-style r<sub>max</sub> ~200 Hz).
- Somatic resting potentials in the literature are biased depolarised (seal artifact), and somatic spike amplitudes are small or filtered. Resting and threshold values from somatic recordings should not be copied literally into point models. Normalised thresholds or rates are safer.

### Gaps
- There are no direct τ<sub>m</sub> measurements for most types. KC, MBON, DAN, E-PG/P-EN, LC/LPLC and DN passive constants were not found in open full texts in this search.
- The Inada et al. 2017 per-subtype KC values (input resistance, thresholds) are behind a paywall; I verified only the abstract.
- Maximum firing rates by type were not compiled. Values found: PN >100 Hz sustained; Pugliese assumes r<sub>max</sub> ~200 Hz; the literature I reviewed has no systematic per-type maxima.
- No compiled database of Drosophila intrinsic properties was found (see Q1 Gaps).
- Most measurements are ex vivo or in head-fixed animals at room temperature. Temperature dependence and in-flight/walking state changes (e.g. the VS membrane-resistance drop in flight) are not systematically characterised.

## 3. Synapse biophysics (delays, time constants, receptor classes) and how well synapse count predicts synaptic strength

### Takeaway
Fast nicotinic and GABA-A (Rdl) synaptic currents in fly neurons rise in ≤1–1.5 ms and decay with τ ≈ 2–7 ms. GABA-B inhibition, much of it presynaptic, operates over ~100 ms to seconds. Glutamate acts mainly through the GluClα chloride channel: inhibitory and often shunting or divisive. There are proven excitatory exceptions via kainate-type receptors, and muscarinic ACh receptors can be inhibitory. Histamine (ort/HisCl1) is a chloride-channel, sign-inverting transmitter. Synapse counts predict connection strength well within a class when normalised by postsynaptic size (r² ≈ 0.77 for LHN dendritic inputs). They fail for some axonal inputs and for silent or weak anatomical connections, and absolute strength per synapse varies ≥3× between neuron types.

### Cited Findings

#### Nicotinic cholinergic transmission (the dominant fast excitation)
- In cultured embryonic neurons, cholinergic mEPSCs have a rise time of 0.6 ms and decay τ = 2 ms — [Lee & O'Dowd 1999, J Neurosci](https://doi.org/10.1523/JNEUROSCI.19-13-05311.1999)
- In adult KCs in situ, α-bungarotoxin-sensitive nicotinic mEPSCs had rise 1.21–1.53 ms, decay τ 4.45–6.73 ms and amplitude ~4 pA across KC populations — [Gu & O'Dowd 2006](https://doi.org/10.1523/JNEUROSCI.4109-05.2006)
- At ORN→PN synapses:
  - release probability ≈ 0.79 (multiple-probability fluctuation analysis) and "several dozen" release sites per unitary connection;
  - uEPSC 29.0 ± 2.6 pA, uEPSP ~6 mV;
  - strong short-term depression, with a presynaptic locus;
  - unitary current amplitude matched to PN dendritic size, and lowering input resistance increases unitary currents (homeostatic matching).

  Source: [Kazama & Wilson 2008](https://doi.org/10.1016/j.neuron.2008.02.030)
- Fitted conductance kinetics for ORN→PN input were rise 0.01 ms / decay 0.6 ms for a single site, and rise 0.2 ms / decay 1.1 ms when distributed over 25 branches — [Gouwens & Wilson 2009](https://doi.org/10.1523/JNEUROSCI.0764-09.2009). The 0.2/1.1 ms values were reused for DN models by [Moreno-Sanchez et al. 2024](https://doi.org/10.1101/2024.04.24.591016)
- ORN→PN depression model: each spike scales conductance by f = 0.78, with recovery τ = 893 ms. Two kinetic components plus presynaptic inhibition broaden the transmitted frequency band in vivo — [Nagel, Hong & Wilson 2015, Nat Neurosci](https://doi.org/10.1038/nn.3895)
- KC→MBON synapses are cholinergic: MBON activation needs KC VAChT and is blocked by ACh-receptor antagonists, and knocking down nAChR subunits in MBONs impairs odour responses. Peptidergic co-release enhances ACh-evoked MBON responses — [Barnstedt et al. 2016, Neuron](https://doi.org/10.1016/j.neuron.2016.02.015)
- Whole-brain LIF convention: synaptic τ 5 ms and delay 1.8 ms for every synapse — [Shiu et al. code](https://github.com/philshiu/Drosophila_brain_model/blob/main/model.py)

#### Muscarinic cholinergic transmission (slow; sign depends on receptor and cell)
- mAChR-A in KC dendrites *inhibits* KC odour responses and is required for learning-associated depression of MBON responses: "While acetylcholine usually excites fly neurons, activating muscarinic receptors inhibits Kenyon cells" — [Bielopolski et al. 2019, eLife](https://doi.org/10.7554/eLife.48264)
- In the AL, mAChR-A directly *excites* a subpopulation of GABAergic iLNs and stabilises the strongly depressing ORN→iLN synapse — [Rozenfeld, Lerner & Parnas 2019, Cell Rep](https://doi.org/10.1016/j.celrep.2019.10.125)
- mAChR-B mediates KC–KC axo-axonic connections that *suppress* odour-evoked Ca²⁺ and dopamine-evoked cAMP in neighbouring KCs, and is needed for stimulus-specific learning — [Manoim et al. 2022, Curr Biol](https://doi.org/10.1016/j.cub.2022.09.007)

#### GABA-A (Rdl) and GABA-B
- GABAergic mIPSCs in cultured neurons flow through picrotoxin-sensitive Cl⁻ channels containing Rdl. In wild type: decay 5.4 ± 0.3 ms, rise 0.88 ± 0.03 ms, amplitude 9.9 ± 0.3 pA, with decay kinetics maturing over days in vitro — [Lee, Su & O'Dowd 2003, J Neurosci](https://doi.org/10.1523/JNEUROSCI.23-11-04625.2003)
- In PNs, GABA acts through a picrotoxin-sensitive (GABA-A) and a CGP54626-sensitive (GABA-B) conductance, and picrotoxin blocked less than half of the PN GABA response. GABA-A shapes the early response. GABA-B mediates odour-evoked inhibitory epochs lasting "∼100 ms to several seconds" and affects spiking 1.5–2.5 s after odour onset — [Wilson & Laurent 2005, J Neurosci](https://doi.org/10.1523/JNEUROSCI.2070-05.2005)
- Interglomerular inhibition is largely *presynaptic* on ORN axon terminals, via both ionotropic and metabotropic GABA receptors, and scales with total AL input (gain control) — [Olsen & Wilson 2008, Nature](https://doi.org/10.1038/nature06864)
- The time course of LN-driven presynaptic inhibition fits an alpha function with τ ≈ 25 ms and "builds slowly" relative to LN spiking — [Nagel, Hong & Wilson 2015](https://doi.org/10.1038/nn.3895)
- LN→PN: "clear unitary synaptic connections are never observed", and LN spike trains are needed, which suggests volume transmission — [Wilson 2013 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/), citing [Yaksi & Wilson 2010](https://doi.org/10.1016/j.neuron.2010.08.041)
- GABA-LNs lack GABA-B conductances — [Liu & Wilson 2013, PNAS](https://doi.org/10.1073/pnas.1220560110) (citing earlier work)
- Possible *depolarising* GABA: Rdl and Lcch3 are expressed in nearly all optic-lobe neurons. L1 and L2 lack Rdl but express Grd, Lcch3 and CG8916, and in vitro Lcch3/Grd form GABA-gated *cation* channels. Musca LMCs depolarise to GABA. This is a prediction, not a Drosophila measurement — [Davis et al. 2020, eLife](https://doi.org/10.7554/eLife.50901)

#### Glutamate: GluClα (inhibitory) versus ionotropic excitatory receptors
- Glutamate applied in the AL hyperpolarises PNs, GABA-LNs and all other major AL cell types via GluClα, blocked by picrotoxin or GluClα RNAi. "We never observed a depolarizing response to glutamate." Stimulating Glu-LNs or GABA-LNs has similar effects on PNs — [Liu & Wilson 2013](https://doi.org/10.1073/pnas.1220560110)
- Contradiction to note: NMDA-receptor (NR1) knockdown in PNs affects olfactory habituation (cited in [Liu & Wilson 2013](https://doi.org/10.1073/pnas.1220560110)), yet no fast depolarising glutamate response was seen. The NMDARs may act in plasticity rather than fast transmission. NMDARs are also implicated in fly memory and in sleep-drive plasticity — [Xia & Chiang 2009, NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK5286/); [Liu et al. 2016](https://doi.org/10.1016/j.cell.2016.04.013)
- T4: glutamatergic Mi9 input via GluClα keeps T4 tonically shunted in darkness. Release from shunting plus coincident cholinergic excitation implements multiplication-like, *divisive* rather than subtractive inhibition — [Groschner et al. 2022](https://doi.org/10.1038/s41586-022-04428-3)
- On the T4 dendrite, GluClα, Dα7 (nAChR) and Rdl sit in a sequential spatial arrangement that matches EM synapse positions — [Fendl et al. 2020](https://doi.org/10.7554/eLife.62953)
- L1 (glutamatergic) drives ON cells through sign inversion via GluClα. Cells postsynaptic to L1 lose all responses in *GluClα* mutants, but not after cell-type-specific GluClα loss, so ON selectivity is distributed over several synapses — [Molina-Obando et al. 2019, eLife](https://doi.org/10.7554/eLife.49373)
- Glutamatergic LPi interneurons deliver direction-selective inhibition to LPTCs with the opposite preferred direction — [Mauss et al. 2015, Cell](https://doi.org/10.1016/j.cell.2015.06.035)
- **Excitatory glutamate:** Dm8 → Tm5c is excitatory via the kainate receptor Clumsy. R7 → Dm8 → Tm5c pools ~16 R7s for UV preference — [Karuppudurai et al. 2014, Neuron](https://doi.org/10.1016/j.neuron.2013.12.010). Four presumptive kainate receptors (Clumsy, DKaiR1C, DKaiR1D, CG11155) are required. Fly iGluRs also have unusual ligand pharmacology (e.g. DGluR1A is barely activated by AMPA) — [Li et al. 2016, Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC5145767/)
- ~80% of central-brain neurons express RNA for GluClα *and* at least one excitatory ionotropic glutamate receptor. "The sign of a glutamatergic connection may depend on the sub-localization and ratio of receptors at recipient sites" — [Eckstein et al. 2024, Cell](https://doi.org/10.1016/j.cell.2024.03.016)

#### Histamine (ort / HisCl1)
- Photoreceptor→LMC transmission is histaminergic via chloride channels, so LMCs hyperpolarise to light. In *ort* mutants, LMC light responses drop from >40 mV to >15 mV — [Zheng et al. 2006](https://doi.org/10.1085/jgp.200509470)
- *ort* is expressed in L1, Tm20 and Dm9, and *HisCl1* in R7/R8. Mi1, Mi4 and Mi15 express neither, so R8 must signal to them with another transmitter (ACh; R8 co-expresses cholinergic markers) — [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
- The optic-lobe DMN treats histaminergic, GABAergic and glutamatergic synapses as hyperpolarising, and handles R8 (ACh versus histamine) using target receptor expression — [Lappalainen et al. 2024](https://doi.org/10.1038/s41586-024-07939-3)

#### Delays and latencies
- ORN→PN is monosynaptic. Palp-PN EPSCs start only ~1.5 ms later than antennal-PN EPSCs, too short for polysynaptic routing, and the lateral (eLN-mediated) component starts ~1.5 ms after the direct one — [Kazama & Wilson 2008](https://doi.org/10.1016/j.neuron.2008.02.030)
- Giant-fibre pathway: wild-type brain-stimulus-to-muscle latency is 0.7–1.2 ms for GF→TTM and 1.3–1.7 ms for GF→DLM, which has an extra chemical synapse (PSI→DLMn). *shakB* mutants raise GF→TTM latency to ~1.5 ms, and the DLM branch becomes unresponsive — [Augustin, Allen & Partridge 2011, JoVE](https://doi.org/10.3791/2412). A conductance model matches latencies of 0.93 ms (TTM) and 1.44 ms (DLM) with ~0.35 ms neuromuscular delay — [Augustin, Zylbertal & Partridge 2019, eNeuro](https://doi.org/10.1523/ENEURO.0423-18.2019)
- Phototransduction adds an absolute delay of ~9 ms before photoreceptor axons depolarise — [Zheng et al. 2006](https://doi.org/10.1085/jgp.200509470)

#### Does synapse count predict strength? Direct tests
- LH neurons (paired recordings plus EM): synapse density (count ÷ LHN surface area) predicted mean uEPSP amplitude with r² = 0.77 (p = 10⁻⁴³) for dendritic connections, but severely underpredicted axonal connections. Residuals did not depend on synapse distance from the soma — [Liu et al. 2022](https://doi.org/10.1016/j.cub.2021.11.056)
- ORN→PN (EM of a glomerulus pair): synapse number per connection co-varies with PN dendrite size and "precisely compensates" for size-dependent dendritic filtering. Ipsilateral ORNs make more synapses than contralateral ones, and connections are imprecise. An isolated ORN spike depolarises a PN by ~5 mV — [Tobin, Wilson & Lee 2017, eLife](https://doi.org/10.7554/eLife.24838)
- Larval EM: per-edge synapse count predicts total synaptic contact area with R² = 0.905 — [Barnes, Bonnéry & Cardona 2022, PLoS ONE](https://doi.org/10.1371/journal.pone.0266064)
- Looming DNs: dendritic morphology normalises single-synapse EPSPs at the SIZ, and near-random synapse placement yields linear encoding of synapse number. Per-synapse SIZ EPSP differs ~3× between DNp01 (~0.05 mV) and DNp03 (~0.17 mV) — [Moreno-Sanchez et al. 2024, preprint](https://doi.org/10.1101/2024.04.24.591016)
- Synaptic-number gradients (e.g. antiparallel LC4→DNp02/DNp11) convert object location into escape direction, and the motif generalises across all 20 primary VPN types — [Dombrovski et al. 2023, Nature](https://doi.org/10.1038/s41586-022-05562-8)
- Counter-example: each compass neuron is inhibited only by specific visual cue positions, so "many potential connections from R neurons onto compass neurons are actually weak or silent", and the pattern reorganises within minutes — [Fisher et al. 2019, Nature](https://doi.org/10.1038/s41586-019-1772-4)
- Whole-network tests: the real connectome drove MN9 in 100% of simulations but only 1 of 100 shuffled connectomes did — [Shiu et al. 2024](https://doi.org/10.1038/s41586-024-07763-9). Region-level structural connectivity predicts resting functional connectivity — [Turner, Mann & Clandinin 2021, Curr Biol](https://doi.org/10.1016/j.cub.2021.03.004). The FC–SC correlation falls linearly as ROI count rises (finer parcellations) — [Okuno et al. 2025, bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2025.07.01.662601v1)

### Inferences
- At the project's 20 ms step, all fast synaptic kinetics (τ 1–7 ms) and delays (~1–2 ms per synapse) collapse into a single step. That is acceptable for a rate-level model. Slow components cannot be represented by an instantaneous weight and need an extra state variable per synapse class: GABA-B (100 ms–s), ORN→PN depression (recovery ~0.9 s), muscarinic and peptidergic effects.
- The project's rule "inputs normalised to sum to 1" approximates homeostatic matching: synapse number scales with dendrite size (Tobin) and unitary current with arbor size (Kazama). It discards real differences in absolute efficacy, though. Normalising by postsynaptic surface area (Liu) or by input resistance proxies (Pugliese) is better grounded than normalising by total input count.
- Some inhibition is divisive or presynaptic rather than subtractive: GluClα shunting in T4, and GABA-B plus GABA-A on ORN terminals. A signed additive weight can't reproduce gain control, so the model needs at least a multiplicative, input-specific inhibitory term for the AL and the medulla.
- Muscarinic receptors mean that "ACh = excitatory" also has exceptions (KC dendrites, KC–KC axo-axonic connections). These are slow and modulatory, better handled as slow inhibitory gain on KCs than as fast negative weights.

### Gaps
- No in vivo measurements of GABA-A IPSC kinetics at identified adult central synapses were found in this search. The kinetics above come from cultured embryonic neurons and from PN pharmacology.
- There are no per-synapse-class delay measurements beyond the olfactory and GF pathways.
- There is no direct Drosophila measurement of ort/HisCl1 synaptic kinetics in this search; histamine synapse kinetics would need targeted follow-up.
- Only a handful of connection types (PN→LHN, ORN→PN, VPN→DN, R→E-PG) have been directly tested for count-versus-strength. Axo-axonic, neuromodulatory and inhibitory connections are largely untested.

## 4. Neurotransmitter prediction from EM (accuracy, failure modes), receptor expression from transcriptomics, receptor-informed signs, and exceptions to "glutamate = inhibitory"

### Takeaway
EM-based transmitter classifiers score ~87% per synapse and 91–94% per neuron or cell type on held-out ground truth (Eckstein 2024). Later pipelines add histamine (optic lobe, MaleCNS) and tyramine (BANC). The dominant errors are GABA↔glutamate confusion, unreliable monoamines (serotonin, octopamine, dopamine), co-transmission and neuropeptides, and neurons with few presynapses. MaleCNS provides a recommended `consensusNt` field that overrides predictions with experimental ground truth and sets octopamine/serotonin to "unclear". Transcriptomic atlases exist for the optic lobe, whole head, VNC and, now, the central brain at ~10× coverage. Receptor-informed signs have been applied only locally, in optic-lobe models and single-circuit studies; I found no whole-CNS receptor-informed sign map. Proven or predicted exceptions to transmitter-only signs include excitatory kainate-type glutamate synapses (Dm8→Tm5c), inhibitory muscarinic ACh synapses, possibly depolarising GABA-A in L1/L2, and ACh co-release by histaminergic R8.

### Cited Findings

#### Eckstein et al. 2024 (the base method, "Synister")
- A 3D CNN classifies six transmitters (ACh, Glu, GABA, 5-HT, DA, OA). Accuracy: 87% per synapse on FAFB (78% on hemibrain), 94% per neuron on FAFB-CATMAID (91% on hemibrain; majority vote, neurons with >30 presynapses), and 91% of 624 FAFB-FlyWire cell types and 91% of 524 hemibrain types versus literature — [Eckstein et al. 2024, Cell](https://doi.org/10.1016/j.cell.2024.03.016)
- Ground truth: 356 cell types from 21 studies (3,025 FAFB neurons with 211,564 synapses; 5,902 hemibrain neurons with 840,535 synapses), later extended by 268 types — [Eckstein et al. 2024](https://doi.org/10.1016/j.cell.2024.03.016)
- Failure modes stated by the authors:
  - glutamate and GABA are the most confused pair;
  - serotonin is least reliable (33% FAFB-FlyWire, 38% hemibrain), and DA/5-HT are inconsistent between datasets;
  - co-transmitting types were excluded from training;
  - histamine, tyramine, glycine, nitric oxide and "∼53 different neuropeptides" are not predicted;
  - accuracy depends on the dataset (4 nm vs 8 nm lateral resolution);
  - low confidence tracks mismatches;
  - some KCs were mispredicted as dopaminergic, and AL LNs break both Dale's and Lacin's laws.

  Source: [Eckstein et al. 2024](https://doi.org/10.1016/j.cell.2024.03.016)
- Hemilineages: 88% express a single fast transmitter, and 19 of 183 show evidence of two, with discrete switches that correlate with morphotype — [Eckstein et al. 2024](https://doi.org/10.1016/j.cell.2024.03.016)

#### Successor pipelines (2024–2026)
- **Optic lobe (male, Janelia):**
  - Seven classes (ACh, Glu, GABA, histamine, DA, OA, 5-HT), trained on 59 cell types, predicting 7,014,581 presynapses (70/10/20 split).
  - Neuron-level calls need ≥50 presynapses and confidence ≥0.5; type-level calls need ≥100 presynapses.
  - `consensusNt` sets DA/OA/5-HT to unclear unless supported experimentally, because those classes were under-represented and their predicted abundance did not match independent measurements.
  - Cross-dataset agreement with FlyWire was 503/544 types (92.5%). Of 41 mismatches, 8 were histamine (absent from FlyWire's classes) and 26 were optic-lobe=Glu vs FlyWire=GABA, with none in the reverse direction.

  Source: [Nern et al. 2025, Nature](https://doi.org/10.1038/s41586-025-08746-0); code: [reiserlab repo](https://github.com/reiserlab/male-drosophila-visual-system-connectome-code)
- **MaleCNS v1.0 (Janelia):**
  - ResNet50 "following Eckstein et al.", 7 transmitter classes. Ground truth comes from a GitHub resource mapping cell types to 10 transmitters (ACh, DA, GABA, Glu, glycine, histamine, NO, OA, 5-HT, tyramine), filtered to evidence confidence ≥3, with co-transmitting types and conflicting evidence removed, split 80/20 by neuron.
  - Properties: `predictedNt` (≥50 presynapses and confidence ≥0.5, else "unclear"), `celltypePredictedNt` (≥100 presynapses) and `consensusNt`. `consensusNt` is recommended; it overrides with experimental ground truth and sets **all octopamine and serotonin results to "unclear"**.
  - Totals: 166,691 neurons, 25.6M edges among 166,391 neurons, 11,691 types.
  - Status: bioRxiv 2025; published in *Cell* in Sept 2026.

  Sources: [Berg et al. 2025, bioRxiv](https://doi.org/10.1101/2025.10.09.680999); [Cell 2026](https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6); [data portal](https://male-cns.janelia.org/)
- **BANC (female brain plus nerve cord):**
  - Eight classes including **histamine and tyramine**, with ground truth of 3,379 cell types (60,394 neurons) from FAFB, MANC and hemibrain.
  - Motor neurons were removed from ground truth "as they have few presynapses within the CNS".
  - ResNet-18 with focal loss; neuron-level calls by summed probability.
  - The lamina (~9,390 R1–6 and Lai neurons) is not in the volume.

  Sources: [Bates et al. 2026, Nature](https://doi.org/10.1038/s41586-026-10735-w); [synister_banc code](https://github.com/htem/synister_banc)
- FANC has no automated classifier, so hemilineage is used as a proxy. Four neurons in glutamatergic hemilineages in FANC (types INXXX464, INXXX466, INXXX468) are predicted cholinergic in MANC, a live sign conflict — [Pugliese et al. 2025, preprint](https://doi.org/10.1101/2025.09.12.675944)

#### Developmental and transcript-level caveats
- All neurons within a VNC hemilineage (34 hemilineages) use the same fast transmitter (ACh, GABA or Glu). However, *ChAT* is transcribed in many glutamatergic and GABAergic neurons without the transcripts leaving the nucleus or being translated, so transcript presence alone misassigns transmitters — [Lacin et al. 2019, eLife](https://doi.org/10.7554/eLife.43701)

#### Transcriptomic resources for receptor expression
- Optic lobe, TAPIN-seq: 100 driver lines covering 67 cell types, served at [opticlobe.com](http://www.opticlobe.com) — [Davis et al. 2020, eLife](https://doi.org/10.7554/eLife.50901). The authors caution that their model can err (e.g. an inferred Gad1 in Mi9 was not supported by FISH or antibody data).
- Optic lobe development atlas: 275,000 single cells across adult and five pupal stages, ~200 cell types — [Özel et al. 2021, Nature](https://doi.org/10.1038/s41586-020-2879-3)
- Visual-system time course: >150 neuronal populations, 88 followed through synaptogenesis — [Kurmangaliyev et al. 2020, Neuron](https://doi.org/10.1016/j.neuron.2020.10.006)
- Whole fly: Fly Cell Atlas, 580,000 nuclei, >250 annotated cell types — [Li et al. 2022, Science](https://doi.org/10.1126/science.abk2432)
- VNC: 26,000 cells, >100 transcriptionally distinct types, organised by hemilineage and birth order — [Allen et al. 2020, eLife](https://doi.org/10.7554/eLife.54074)
- Central brain: an integrated single-cell atlas with "10-fold coverage of every neuron", organised by lineage and birth order, described as a bridge to hemilineage and cell-type annotations — [Allen et al. 2026, Cell Genomics](https://doi.org/10.1016/j.xgen.2025.101103)

#### Receptor-informed sign work (all local, not whole-CNS)
- The optic-lobe DMN derived signs from "neurotransmitter and receptor expression profiling", using target receptor expression to special-case R8 (ACh vs histamine) — [Lappalainen et al. 2024](https://doi.org/10.1038/s41586-024-07939-3)
- Davis 2020 used receptor expression to predict signs and effects:
  - GluClα is "expressed in most but not all cell types" and absent from photoreceptors;
  - "The predicted absence of GluCl-alpha in Dm9 suggests that glutamatergic input from Dm8 to Dm9 may be excitatory";
  - L1/L2 may carry cation-permeable GABA-A (Grd/Lcch3);
  - Lai (the only vesicular-glutamate source in the lamina) targets cells with very diverse glutamate-receptor repertoires.

  Source: [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
- Subcellular receptor maps on T4 (GluClα, Rdl, Dα7) match EM synapse positions and support sign/type assignment per input — [Fendl et al. 2020](https://doi.org/10.7554/eLife.62953)
- Clock and neurosecretory circuits: single-cell transcriptomics plus receptor mapping were used to infer *paracrine peptidergic* links in addition to synapses — [Reinhard et al. 2024, Nat Commun](https://doi.org/10.1038/s41467-024-54694-0); [McKim et al. 2024, bioRxiv/eLife reviewed preprint](https://doi.org/10.1101/2024.08.28.609616)

#### Known or predicted exceptions to transmitter-only signs
- Glutamate excitatory:
  - Dm8→Tm5c via the kainate receptor Clumsy (proven) — [Karuppudurai et al. 2014](https://doi.org/10.1016/j.neuron.2013.12.010)
  - Dm8→Dm9 (predicted) — [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
  - Photoreceptors lack GluClα (prediction for Lai→R glutamate) — [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
  - Most central neurons co-express GluClα and excitatory iGluRs — [Eckstein et al. 2024](https://doi.org/10.1016/j.cell.2024.03.016)
- Glutamate inhibitory, as the rule assumes: AL Glu-LNs → PNs/LNs via GluClα ([Liu & Wilson 2013](https://doi.org/10.1073/pnas.1220560110)); Mi9→T4, divisive shunt ([Groschner et al. 2022](https://doi.org/10.1038/s41586-022-04428-3)); L1→Mi1, sign inversion ([Molina-Obando et al. 2019](https://doi.org/10.7554/eLife.49373)); LPi→LPTC ([Mauss et al. 2015](https://doi.org/10.1016/j.cell.2015.06.035))
- ACh inhibitory via muscarinic receptors: PN→KC dendrites (mAChR-A, [Bielopolski et al. 2019](https://doi.org/10.7554/eLife.48264)) and KC→KC axo-axonic (mAChR-B, [Manoim et al. 2022](https://doi.org/10.1016/j.cub.2022.09.007))
- GABA possibly excitatory in L1/L2 (predicted from subunit expression) — [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
- Histamine plus ACh co-release: R8's targets Mi1, Mi4 and Mi15 lack histamine receptors, so they are presumably excited via ACh — [Davis et al. 2020](https://doi.org/10.7554/eLife.50901)
- Electrical rather than chemical excitation: cholinergic eLNs excite PNs only via gap junctions, so the chemical sign (ACh→PN) would place an edge that doesn't exist chemically — [Yaksi & Wilson 2010](https://doi.org/10.1016/j.neuron.2010.08.041)

### Inferences
- For MaleCNS simulation, use `consensusNt`, not `predictedNt`. Decide explicitly what to do with "unclear" neurons (<50 presynapses or confidence <0.5) and with DA/OA/5-HT and histamine neurons. The project's current rule makes DA/5-HT/OA neurons fast-excitatory by default (only GABA/Glu/His are negative), which is biologically wrong for GPCR-acting monoamines (see Q6).
- The most frequent sign error is probably GABA↔Glu. That matters less for sign, since both are inhibitory under the project's rule, than for dynamics: GluClα shunts, and some glutamate synapses are excitatory. Glu-versus-ACh confusions, as in the MANC/FANC case above, flip signs and should be audited against hemilineage.
- A practical receptor-informed sign layer could be built by mapping transcriptomic clusters to connectome types. The optic lobe is the easiest (Davis 2020 plus Özel 2021 plus the Nern 2025 split-GAL4 lines), and the Allen 2026 central-brain atlas targets exactly this. Flip a Glu edge to excitatory when the postsynaptic type lacks GluClα and expresses kainate/AMPA subunits. That rule has at least one proven case (Dm8→Tm5c) and one prediction (Dm8→Dm9).

### Gaps
- No whole-CNS, receptor-informed sign assignment for Drosophila was found as of Sept 2026. Searches returned only local optic-lobe or circuit examples.
- I could not find quantitative accuracy figures for the MaleCNS classifier in the text I accessed (only the method and thresholds), or held-out accuracy numbers for BANC's histamine/tyramine classes.
- Receptor expression by connectome type for the central brain and VNC is not yet systematically mapped. Receptor subcellular localisation (Fendl-style) exists for very few types.
- How often GluClα-plus-iGluR co-expressing neurons actually receive excitatory glutamate is unknown.

## 5. Gap junctions: innexins, known electrical synapses, connectome annotation, prevalence, and modelling

### Takeaway
Drosophila has eight innexin genes. ShakB is the most widely expressed neuronal innexin, and Inx6/Inx7 (MB) and Inx5 (αβ KCs) also form functional electrical synapses. Electrical coupling is documented in the escape circuit, antennal lobe, lamina, lobula plate, mushroom body and flight CPG, and sometimes it is the *only* route of excitation (eLN→PN). No published fly connectome annotates electrical synapses. The whole-brain and optic-lobe models explicitly omit them, and there is no quantitative estimate of brain-wide prevalence.

### Cited Findings

#### Innexin family and expression
- Drosophila has "eight known ... innexins", and five of the eight (ogre, Inx2, Inx3, shakB, zpg) are transcribed in the adult antenna — [Prelic et al. 2024, Cell Tissue Res](https://doi.org/10.1007/s00441-024-03909-3)
- A light-microscopy immunohistochemical map of all innexins in the CNS found some localised to glia and others mainly neuronal, with *shakB* "the most widely expressed neuronal innexin" — [Ammer et al. 2022, Curr Biol](https://doi.org/10.1016/j.cub.2022.03.040)
- The alternative transcripts *shakB.neural* are expressed in the adult CNS, and *shakB²* eliminates all ShakB(neural) proteins — [Yaksi & Wilson 2010](https://doi.org/10.1016/j.neuron.2010.08.041)
- Ogre alone doesn't form homotypic channels, but co-expressing Ogre with Inx2 produces functional channels distinct from Inx2 homotypic channels. Both are required in glia for postembryonic CNS development — [Holcroft et al. 2013, J Cell Sci](https://doi.org/10.1242/jcs.117994)

#### Known electrical synapses (with physiology)
- **Giant fiber escape circuit:**
  - GF→TTMn and GF→PSI are mixed electrical (ShakB) and cholinergic synapses. They rectify: ShakB(N+16) is presynaptic in GF and ShakB(Lethal) postsynaptic, forming heterotypic, asymmetrically voltage-gated channels — [Phelan et al. 2008, Curr Biol](https://doi.org/10.1016/j.cub.2008.10.067)
  - Without gap junctions (*shakB*), GF→TTM latency rises to ~1.5 ms (from 0.7–1.2 ms) and the DLM branch fails — [Augustin et al. 2011, JoVE](https://doi.org/10.3791/2412)
  - Age-related loss of GF gap junctions slows escape; a conductance model uses g<sub>gap</sub> 135 µS (young) vs 34.5 µS (old) — [Augustin et al. 2019, eNeuro](https://doi.org/10.1523/ENEURO.0423-18.2019)
- **Antennal lobe, sister PNs:** homotypic PNs are reciprocally connected by mixed electrical/chemical synapses. The coupling coefficient is larger for depolarising steps, and Cd²⁺ removes this asymmetry (leaving the electrical part) — [Kazama & Wilson 2009, Nat Neurosci](https://doi.org/10.1038/nn.2376)
- **Antennal lobe, eLNs→PNs:**
  - These synapses pass both hyperpolarisation and depolarisation, survive blockade of chemical transmission, and are abolished by *shakB²*. "eLNs do not excite PNs through chemical synapses."
  - Each eLN appears connected to most or all PNs. PNs release ACh onto eLNs, and eLNs make mixed synapses onto iLNs.
  - *shakB²* raises input resistance in PNs that normally receive strong lateral excitation (VC1, VC2).

  Source: [Yaksi & Wilson 2010](https://doi.org/10.1016/j.neuron.2010.08.041)
- **Antennal lobe, Inx7:** Inx7 knockdown blocks synchronised Ca²⁺ transients in cultured PNs and impairs vinegar responses and behaviour in vivo — [Fuenzalida-Uribe et al. 2025, Front Neural Circuits](https://doi.org/10.3389/fncir.2025.1563401)
- **Mushroom body:**
  - APL and DPM form heterotypic gap junctions (Inx7 in APL, Inx6 in DPM) needed for anaesthesia-sensitive memory — [Wu et al. 2011, Curr Biol](https://doi.org/10.1016/j.cub.2011.02.041)
  - Inx5 in αβ KCs is required for retrieving anaesthesia-resistant memory — [Shyu et al. 2019, PLoS Genet](https://doi.org/10.1371/journal.pgen.1008153)
- **Lamina and photoreceptors:** gap junctions link R7/R8 to R6, and depolarising LMC responses suggest L2–R8 coupling — [Wardill et al. 2012](https://doi.org/10.1126/science.1215317)
- **Lobula plate:**
  - Neurobiotin coupling runs among ipsilateral HS cells and to contralateral-dendrite tangential cells — [Schnell et al. 2010](https://doi.org/10.1152/jn.00950.2009)
  - Lateral VS–VS connections widen receptive fields — [Joesch et al. 2008](https://doi.org/10.1016/j.cub.2008.02.022)
  - Removing *shakB* from VS/HS causes spontaneous cell-autonomous voltage and Ca²⁺ oscillations. Upstream, *shakB* loss impairs ON and OFF motion pathways differently but does not abolish direction selectivity — [Ammer et al. 2022](https://doi.org/10.1016/j.cub.2022.03.040)
- **Flight CPG:** motoneurons coupled by *weak* electrical synapses fire splayed out in time rather than synchronously. This depends on weak coupling plus specific intrinsic excitability, and it stabilises wingbeat power — [Hürkey et al. 2023, Nature](https://doi.org/10.1038/s41586-023-06099-0); commentary: [Gutierrez & Wang 2023, Curr Biol](https://doi.org/10.1016/j.cub.2023.06.058)

#### Connectome annotation and model status
- The whole-brain LIF model "does not account for gap junctions" — [Shiu et al. 2024](https://doi.org/10.1038/s41586-024-07763-9)
- The optic-lobe DMN "cannot account for the role played ... by electrical synapses, nonlinear chemical synapses and neuromodulation" — [Lappalainen et al. 2024](https://doi.org/10.1038/s41586-024-07939-3)
- "Existing fly connectome datasets lack important biophysical and molecular parameters, such as the expression of ion channels, receptors, neuromodulators, and gap junctions" — [Pugliese et al. 2025, preprint](https://doi.org/10.1101/2025.09.12.675944)
- Models that do include electrical synapses are circuit-scale: the GF system (unidirectional GF→PSI and GF→TTMn electrical synapses; [Augustin et al. 2019](https://doi.org/10.1523/ENEURO.0423-18.2019)) and the flight CPG ([Hürkey et al. 2023](https://doi.org/10.1038/s41586-023-06099-0))

### Inferences
- My full-text searches of the MaleCNS (Berg et al.) and BANC (Bates et al.) papers found no electrical-synapse annotation, so gap junctions must be added from the literature list above as a curated edge layer. A candidate first layer:
  - GF→TTMn and GF→PSI (rectifying);
  - sister-PN pairs within each glomerulus;
  - eLN↔PN (AL-wide);
  - APL–DPM;
  - HS–HS, VS–VS and HS/VS–contralateral tangential cells;
  - flight MNs (MN1–5);
  - R7/R8–R6 in the lamina (absent from BANC; check MaleCNS lamina coverage).
- In a voltage-based LIF, add I<sub>gap</sub> = g<sub>ij</sub>(V<sub>j</sub> − V<sub>i</sub>), rectified for GF. In a normalised-input model, coupling acts as a diffusive smoothing term. Use weak values where the literature says "weak" (flight CPG), because strong coupling synchronises and would give the wrong splay behaviour there.
- The eLN→PN case matters for sign assignment. If EM shows cholinergic eLN→PN chemical synapses, treating them as excitatory chemical edges approximates the electrical effect in sign but misses its bidirectionality and hyperpolarisation transfer.
- *shakB* expression is broad (Ammer 2022), so the documented list probably underestimates coupling. Prevalence could be approximated from ShakB transcript expression per type (FCA, the central-brain atlas), with the caveat from Q1 and Q4 that transcripts ≠ functional protein.

### Gaps
- There is no quantitative estimate of what fraction of neurons or cell types are electrically coupled in the adult fly.
- I did not extract coupling coefficients per pair. Kazama & Wilson 2009 and Yaksi & Wilson 2010 report them graphically; values need follow-up from figures.
- Rectification and innexin composition are known only for the GF synapses.
- No type-level or EM-registered electrical-synapse map exists as of Sept 2026 in what I found. Expansion microscopy with innexin tags is a plausible route, but I found no completed brain-wide map.

## 6. Neuromodulation (dopamine, serotonin, octopamine, neuropeptides), volume transmission, internal state, and models that include them

### Takeaway
Monoamines and neuropeptides in the fly act mostly through GPCRs on timescales of hundreds of ms to hours. Their effects are gain changes, kinetic changes, compartment-specific plasticity and receptor-level up/down-regulation, not fast signed synaptic drive. They are therefore poorly represented by treating DA/OA/5-HT synapses as fast excitatory edges, and neuropeptide signalling is invisible in EM. Well-quantified state effects include: flight doubling VS-cell visual gain via octopamine; octopamine speeding medulla inputs and shifting T4/T5 temporal tuning; walking raising HS gain; hunger raising Or42b ORN presynaptic gain via sNPF; and compartmentalised dopamine re-routing KC output. Whole-CNS models do not yet include neuromodulation. Existing models that do are circuit-scale (MB learning models, the larval feeding-state circuit, linear models of neurosecretory inputs).

### Cited Findings

#### Dopamine
- DAN inputs to the MB "modulate synaptic transmission with exquisite spatial specificity", so a single KC can send different signals to different MBONs. DANs work as an interconnected network encoding external context and internal state, and activating each γ-lobe MBON excites or inhibits DANs in every compartment — [Cohn, Morantte & Ruta 2015, Cell](https://doi.org/10.1016/j.cell.2015.11.019)
- DopR1 and DopR2 couple to different second messengers. DopR1 is required for depression after forward pairing, and DopR2 (via Gαq) for potentiation after backward pairing — [Handler et al. 2019, Cell](https://doi.org/10.1016/j.cell.2019.05.040)
- Male mating drive: dopaminergic activity in the anterior superior medial protocerebrum drops transiently and cumulatively with each copulation and acts on P1 neurons through DopR2. It sets how likely a female percept is to trigger courtship — [Zhang, Rogulja & Crickmore 2016, Neuron](https://doi.org/10.1016/j.neuron.2016.05.020)

#### Octopamine, locomotion and arousal
- VS-cell peak-to-peak visual responses double during flight, and passive membrane resistance falls — [Maimon et al. 2010](https://doi.org/10.1038/nn.2492)
- Octopamine neurons are necessary and sufficient for the flight boost in VS cells, bath octopamine mimics flight, and optic-lobe-projecting OA cells are more active in flight — [Suver, Mamiya & Dickinson 2012, Curr Biol](https://doi.org/10.1016/j.cub.2012.10.034)
- Behavioural state modulates the ON motion pathway, "especially prominent in the inhibitory neuron Mi4". Central octopaminergic neurons "provide input to Mi4 and increase its excitability", and are required for sustained behavioural responses to fast, not slow, motion. CDM (an OA agonist) reproduces active-state changes — [Strother et al. 2018, PNAS](https://doi.org/10.1073/pnas.1703090115)
- Octopamine-receptor activation shifts T4/T5 temporal tuning "toward higher frequencies", and this is "fully explained by the concomitant speeding of the input elements" — [Arenz et al. 2017, Curr Biol](https://doi.org/10.1016/j.cub.2017.01.051)
- Walking strengthens HS Ca²⁺ responses, in proportion to walking speed, and shifts their optimal temporal frequency upward — [Chiappe et al. 2010, Curr Biol](https://doi.org/10.1016/j.cub.2010.06.072)
- Context-dependent gating can also be synaptic: movement-encoding leg proprioceptor axons are suppressed during walking and grooming by GABAergic presynaptic inhibition from interneurons driven by descending pathways — [Dallmann et al. 2025, Nature](https://doi.org/10.1038/s41586-025-09554-2)

#### Neuropeptides, hunger and volume transmission
- Hunger: sNPF and its receptor sNPFR1 in Or42b ORNs are needed for starvation-induced food search. Starvation raises *sNPFR1* transcription, insulin signalling suppresses it, and the result is presynaptic facilitation (higher ORN→PN gain) — [Root et al. 2011, Cell](https://doi.org/10.1016/j.cell.2011.02.008)
- In parallel, sNPF sensitises an attraction-wired glomerulus while tachykinin (DTK) suppresses an aversion-wired glomerulus — [Ko et al. 2015, eLife](https://doi.org/10.7554/eLife.08298)
- Feeding state (sugar vs balanced diet) biases larval decisions through NPY-homolog neuropeptides acting on two reciprocally connected inhibitory neuron types (imaging, manipulation and computational modelling) — [de Tredern et al. 2025, Nat Commun](https://doi.org/10.1038/s41467-025-61805-y)
- KC peptidergic co-release enhances ACh-evoked MBON responses — [Barnstedt et al. 2016](https://doi.org/10.1016/j.neuron.2016.02.015)
- EM classifiers cannot predict "∼53 different neuropeptides" — [Eckstein et al. 2024](https://doi.org/10.1016/j.cell.2024.03.016)
- Clock network: ~240 neurons, not 150. Monosynaptic links from clock neurons to downstream centres and neurosecretory cells are sparse, so single-cell transcriptomics plus receptor mapping were used to infer paracrine peptidergic links (including newly identified DH44 and proctolin). These "significantly enrich" interconnectivity — [Reinhard et al. 2024, Nat Commun](https://doi.org/10.1038/s41467-024-54694-0)
- Neurosecretory-cell synaptic output is sparse, mostly from corazonin NSC. Linear dynamical modelling on the connectome ranks enteric neurons as the strongest influence on NSC activity — [McKim et al. 2024, bioRxiv / eLife reviewed preprint](https://doi.org/10.1101/2024.08.28.609616)
- In the whole-brain LIF model, a neuron type (Usnea) with strong activation and silencing phenotypes was not predicted. Knockdown of the prohormone convertase *amontillado* in Usnea phenocopied silencing, pointing to neuropeptide signalling. The model "failed to predict behavioural results ... when the neurons tested were predicted to be inhibitory ... or neuromodulatory", and "circuits with extensive neuromodulation or extrasynaptic signalling will be poorly modelled" — [Shiu et al. 2024](https://doi.org/10.1038/s41586-024-07763-9)
- Neuropeptides and peptide hormones are "the largest and most diverse class of neuroactive substances" in Drosophila, acting in feeding, sleep and clock, aggression, mating, learning and more — [Nässel & Zandawala 2019, Prog Neurobiol](https://doi.org/10.1016/j.pneurobio.2019.02.003)

#### Mating state, sleep, circadian state
- Female mating state: sex peptide acts on SPR in reproductive-tract sensory neurons (SPSNs), *lowering SPSN excitability* and so reducing drive to ascending SAG neurons, which control receptivity — [Feng et al. 2014, Neuron](https://doi.org/10.1016/j.neuron.2014.05.017)
- Sleep pressure is encoded by plasticity in R5 ring neurons: higher Ca²⁺, more NMDA receptor expression, structural synaptic markers, and a switch to burst firing — [Liu et al. 2016](https://doi.org/10.1016/j.cell.2016.04.013)
- l-LNv firing follows a day/night pattern: 3.1 Hz with bursting by day, 1.7 Hz tonic by night — [Sheeba et al. 2008](https://doi.org/10.1016/j.cub.2008.08.033)

#### Models that include neuromodulation
- MB models: DANs signalling reinforcement prediction errors through MBON→DAN feedback ([Bennett, Philippides & Nowotny 2021, Nat Commun](https://doi.org/10.1038/s41467-021-22592-4)); heterogeneous DAN activity inferred from task constraints, with RPE emerging as a population mode ([Jiang & Litwin-Kumar 2021, PLoS Comput Biol](https://doi.org/10.1371/journal.pcbi.1009205)); larval connectome of circuitry upstream of DANs with recurrent feedback, plus modelling ([Eschbach et al. 2020, Nat Neurosci](https://doi.org/10.1038/s41593-020-0607-9))
- Whole-brain effectome proposal: a linear dynamical model estimated from optogenetic perturbations with the connectome as a prior. Only ~0.01% of neuron pairs are connected, which gives a strong sparsity prior — [Pospisil et al. 2024, Nature](https://doi.org/10.1038/s41586-024-07982-0)

### Inferences
- The project currently treats DA/5-HT/OA neurons as excitatory. Better options:
  - route their outputs to *modulatory* state variables that scale gain, time constants or plasticity rates in target types (e.g. octopamine: ×~2 gain on VS/HS inputs and faster τ on Mi1/Tm3/Mi4 in "active" state);
  - or at least zero their fast weights and flag them.

  Using MaleCNS `consensusNt`, which sets OA/5-HT to "unclear", forces an explicit choice.
- Internal-state variables with quantitative targets for validation: flight/walking arousal (VS gain doubling; T4/T5 temporal-frequency shift; HS walking gain); hunger (Or42b ORN→PN gain up via sNPFR1; DTK down on aversive glomeruli); male mating drive (DA→P1 via DopR2; relevant to the male CNS); circadian (l-LNv rates); sleep pressure (R5 burst mode).
- Peptidergic paracrine edges can be generated from ligand/receptor co-expression across transcriptomic types, as Reinhard 2024 and McKim 2024 did. They would be slow and diffuse and not synapse-weighted. Accuracy is unvalidated beyond a few circuits.
- The Usnea case in Shiu 2024 is a concrete template for where a connectome-only model will fail. Neuropeptidergic "hub" types should be expected to show up as false negatives in silencing screens.

### Gaps
- There is no brain-wide map of monoamine or neuropeptide receptor expression per connectome type, and no measurements of diffusion range or volume-transmission extent for fly monoamines or peptides.
- The time constants of GPCR-mediated effects (onset and offset) are poorly quantified for most fly neuromodulator–target pairs.
- Serotonin's effects were not covered in depth in this search (e.g. the CSD neuron in the AL). The literature exists but I did not verify specific numbers.
- No whole-CNS fly model incorporating neuromodulation or internal state was found (Shiu 2024 explicitly omits both).

## 7. Plasticity: mushroom-body dopamine-gated rules and timescales, and other known plastic sites

### Takeaway
KC→MBON synapses have a well-characterised, compartment-specific, dopamine-gated rule. When KCs are active just before or with DAN activity (0 to +0.5 s), a single 1 s pairing depresses the KC→MBON synapse by ~80–90% for ≥40 min, via DopR1. When DAN activity precedes the odour (~1.2 s), the synapse is potentiated via DopR2, and the two effects can reverse each other trial by trial. Compartments differ in learning rate, decay (hours vs ≥4 days) and capacity. Other documented plastic sites include ring-neuron→compass-neuron (E-PG) mapping in the central complex (minutes), sleep-drive plasticity in R5 ring neurons, homeostatic plasticity in the MB and at ORN→PN synapses, and short-term depression at ORN→PN.

### Cited Findings

#### Mushroom body: induction rule, magnitude, timescale
- Hige et al. 2015 (Neuron) found:
  - A single 1 s odour (CS+) paired with PPL1-γ1pedc DAN activation (four 1 ms light pulses at 2 Hz starting 0.2 s after CS+ onset) caused odour-specific, long-lasting suppression of MBON-γ1pedc.
  - Odour-evoked spikes fell by 80 ± 5.7%, and EPSC charge transfer fell by 90 ± 3.7%.
  - The suppression "persisted throughout the duration of the recordings, which lasted at least 40 min".
  - Backward pairing had no effect.
  - The unpaired odour (CS−) was also slightly depressed (27 ± 7.1%).
  - KC excitability was unchanged, so the authors concluded it was LTD at KC→MBON synapses.
  - A behaviour-style 1-min pairing (120 pulses at 2 Hz) gave similar results.
  - "Dopamine action is confined to and distinct across different anatomical compartments."

  Source: [Hige et al. 2015, Neuron](https://doi.org/10.1016/j.neuron.2015.11.003)
- Timing rule (Handler et al. 2019):
  - At the γ4 MBON, forward pairing (inter-stimulus interval 0 or +0.5 s) depressed the response and backward pairing (−1.2 s) potentiated it.
  - "A single conditioning trial drove opposing forms of neural plasticity", and backward-induced potentiation "could be reversed by a single forward conditioning trial".
  - DopR1 acts as a coincidence detector but does not encode order; DopR2 (via Gαq) depends strictly on the order of KC and DAN activation.

  Source: [Handler et al. 2019](https://doi.org/10.1016/j.cell.2019.05.040)
- Compartment-specific rules (Aso & Rubin 2016):
  - PPL1-γ1pedc gives robust immediate memory after one training but no 4-day memory even after extensive spaced training, and has an effective memory capacity of one odour.
  - PPL1-α3 gives barely detectable immediate memory after one pairing but 1-day and 4-day memory after 10× spaced training.
  - The α1 compartment has capacity ≥2, and its MBON forms a recurrent loop onto its own DAN (PAM-α1).
  - One DAN type can write or weaken an aversive memory, or write an appetitive one, depending on when it fires relative to the odour.

  Source: [Aso & Rubin 2016, eLife](https://doi.org/10.7554/eLife.16135)
- Parallel memories with different decay rates (γ1pedc fast vs α1 slow) can shift the valence of the conditioned response over time — [Aso & Rubin 2016](https://doi.org/10.7554/eLife.16135)
- mAChR-A in KCs is needed for learning-induced depression of MBON responses — [Bielopolski et al. 2019](https://doi.org/10.7554/eLife.48264). mAChR-B-mediated lateral KC–KC suppression prevents non-specific learning — [Manoim et al. 2022](https://doi.org/10.1016/j.cub.2022.09.007)
- MBON tuning curves are highly correlated across MBONs, and plasticity drives inter-individual differences in MBON odour coding — [Hige et al. 2015, Nature](https://doi.org/10.1038/nature15396)
- Homeostatic plasticity in the MB: four days of artificially activating APL raises KC odour responses once the activation is removed, through more KC excitation and less APL activation, with KC-subtype differences. Blocking APL produces little compensation — [Apostolopoulou & Lin 2020, PNAS](https://doi.org/10.1073/pnas.1921294117)

#### Other plastic sites
- Central complex: correlated activity of compass neurons and visual ring neurons drives plasticity that maps 2D visual scenes onto a stable heading representation — [Kim et al. 2019, Nature](https://doi.org/10.1038/s41586-019-1767-1). Visually evoked inhibition from R neurons onto compass neurons "can reorganize over minutes" in an altered virtual environment — [Fisher et al. 2019, Nature](https://doi.org/10.1038/s41586-019-1772-4)
- Sleep homeostasis: R5 ring neurons show sleep-need-dependent plasticity (Ca²⁺, NMDAR expression, structural synaptic markers) that is "both necessary and sufficient for generating sleep drive" — [Liu et al. 2016](https://doi.org/10.1016/j.cell.2016.04.013)
- ORN→PN: homeostatic matching of unitary current to dendrite size, where lowering input resistance increases unitary currents ([Kazama & Wilson 2008](https://doi.org/10.1016/j.neuron.2008.02.030)); short-term depression with f = 0.78 and τ<sub>rec</sub> = 893 ms ([Nagel et al. 2015](https://doi.org/10.1038/nn.3895)); starvation-dependent presynaptic facilitation via sNPFR1 ([Root et al. 2011](https://doi.org/10.1016/j.cell.2011.02.008))

#### Models of MB plasticity
- Plasticity rules that minimise reinforcement prediction error, with DANs receiving MBON feedback, reproduce conditioning and blocking data — [Bennett et al. 2021](https://doi.org/10.1038/s41467-021-22592-4)
- DAN heterogeneity inferred from task constraints — [Jiang & Litwin-Kumar 2021](https://doi.org/10.1371/journal.pcbi.1009205). A larval recurrent architecture regulates learning — [Eschbach et al. 2020](https://doi.org/10.1038/s41593-020-0607-9)

### Inferences
- A minimal MB rule for the project, per compartment c:

  Δw<sub>KC→MBON</sub> = −η<sub>c</sub>·[KC activity ⊗ DA<sub>c</sub>]<sub>forward window (0 to ≥0.5 s)</sub> + η′<sub>c</sub>·[DA<sub>c</sub> preceding KC by ~1 s]

  with compartment-specific learning rates (γ1pedc fast, α3 slow) and decay rates (γ1pedc lasting <1 day; α3 ≥4 days after spaced training). A 20 ms step resolves these second-scale windows.
- The plasticity-sensitive sites that matter for "embodied" behaviour on seconds-to-minutes scales are MB compartments (valence learning) and ring-neuron→E-PG synapses (visual landmark to heading mapping). Both are well defined in the connectome, so they are good targets for a first plasticity layer.
- The MB rule is heterosynaptic and gated by a neuromodulator (DA), so it requires the modulatory channel from Q6. It cannot be implemented as a spike-timing rule on existing signed edges.

### Gaps
- The full timing kernel (outcome vs inter-stimulus interval) has been sampled at only a few intervals and in a few compartments. Quantitative learning and decay rates for all ~15 MB compartments are not tabulated in the sources I accessed.
- Plasticity outside the MB and CX (lateral horn, SEZ/gustatory circuits, VNC) is largely uncharacterised physiologically in adults.
- The interaction of short-term plasticity with the MB rule, and long-term structural changes, are not quantified for modelling.

## 8. Reduced neuron models used for flies (LIF, AdEx/adaptive, graded rate, conductance-based, multicompartment) and evidence on adequacy

### Takeaway
Three simplified approaches are validated in part. Uniform-parameter LIF across the central brain (Shiu 2024) predicts feedforward sensorimotor recruitment well: 91% of 164 tested predictions. Task-trained graded (threshold-linear) rate models of the optic lobe (Lappalainen 2024) predict ON/OFF polarity for all 32 tested types and T4/T5 direction selectivity. Randomised-parameter rate models of the VNC (Pugliese 2025, preprint) found a validated walking CPG, with results matched by LIF. Their failures cluster at inhibition-dominated, neuromodulatory and graded or compartmentalised neurons. Multicompartment work shows some neurons (CT1; some visual interneurons) are not point neurons, while large DNs encode synapse number linearly. Theory shows that connectivity alone underdetermines dynamics unless some neurons are recorded. I found no fly-specific AdEx parameter fits; adaptation has been modelled generically in insect olfaction.

### Cited Findings

#### LIF (point, spiking)
- The whole central brain as uniform LIF (FlyWire; >125,000 neurons, ~50M synapses):
  - "Across 164 predictions we were able to test empirically, 91% were consistent".
  - 10 of 11 cell types predicted to activate MN9 elicited proboscis extension when optogenetically activated.
  - ±30% W<sub>syn</sub> left 85–88% accuracy.
  - The real connectome activated MN9 in 100% of runs versus 1 of 100 shuffled runs.
  - Failures came at inhibitory or neuromodulatory neurons.
  - "Absolute firing rate predictions are unlikely to be accurate".

  Sources: [Shiu et al. 2024](https://doi.org/10.1038/s41586-024-07763-9); [code](https://github.com/philshiu/Drosophila_brain_model)
- In the PB–EB spiking model, "Ring attractor dynamics emerged under a wide variety of parameter configurations, even including non-spiking leaky-integrator implementations" — [Kakaria & de Bivort 2017](https://doi.org/10.3389/fnbeh.2017.00008)
- FlyWire v783 connectome simulations of escape versus feeding/grooming conflicts identify redundant feeding-suppression ensembles — [Xi & Chen 2025, bioRxiv preprint](https://doi.org/10.64898/2025.12.14.694122)

#### Graded / rate models
- The optic-lobe DMN has 64 types, 45,669 neurons, 1,513,231 synapses and 734 free parameters, and was trained on optic-flow estimation. It predicted ON/OFF polarity "for all 32 cell types for which contrast selectivity has been experimentally established" and T4/T5 direction selectivity, compared against 26 prior studies. Better task performance correlated with better DSI prediction (r = 0.60). Code: [flyvis](https://github.com/TuragaLab/flyvis) — [Lappalainen et al. 2024](https://doi.org/10.1038/s41586-024-07939-3)
- VNC rate model on all four published VNC connectomes (MANC, FANC, male CNS, BANC), from Pugliese et al.:
  - Pruning isolated a minimal 3-neuron rhythm generator (two excitatory, one inhibitory).
  - DNg100 drives leg-MN oscillations at ~7–15 Hz, matching stepping, with τ averaging 20 ms; the authors give a linearised frequency–τ relation.
  - The predicted DNb08-driven rhythmic leg movement was confirmed optogenetically.
  - Results held with 3× parameter variance, and LIF reproduced them.
  - The minimal circuit differed between datasets: FANC screens converged on a four-interneuron circuit, with a different inhibitory neuron, in 70.4% of replicates.

  Source: [Pugliese et al. 2025, bioRxiv preprint](https://doi.org/10.1101/2025.09.12.675944); [code](https://github.com/smpuglie/Pugliese_cpg_2025)
- A whole-brain FlyWire-constrained model fitted to spontaneous calcium activity reproduced untrained properties: lognormal weights, scale-free avalanches, and "short intrinsic time constants in visual neurons". A sparse ensemble of inhibitory hubs plus reciprocal excitatory partners was necessary and sufficient to sustain resting dynamics — [Li et al. 2026, bioRxiv preprint](https://www.biorxiv.org/content/10.64898/2026.08.21.745055v1)
- Linear models: region-level structure predicts resting functional connectivity ([Turner et al. 2021](https://doi.org/10.1016/j.cub.2021.03.004)); an effectome estimated with the connectome as a prior ([Pospisil et al. 2024](https://doi.org/10.1038/s41586-024-07982-0)); linear dynamical propagation to neurosecretory cells ([McKim et al. 2024](https://doi.org/10.1101/2024.08.28.609616))

#### Conductance-based and multicompartment models
- AL PN multicompartment (NEURON): distributed synapses and a proximal-axon SIZ — [Gouwens & Wilson 2009](https://doi.org/10.1523/JNEUROSCI.0764-09.2009); [ModelDB 118662](https://modeldb.science/118662)
- LHN models built on EM morphology show that arbor and cable architecture constrain computation, with dendritic versus axonal inputs behaving differently — [Liu et al. 2022](https://doi.org/10.1016/j.cub.2021.11.056)
- DN multicompartment models encode synapse number linearly — [Moreno-Sanchez et al. 2024, preprint](https://doi.org/10.1101/2024.04.24.591016)
- CT1: independent terminal compartments, "at the biophysical limit of neural computation" — [Meier & Borst 2019](https://doi.org/10.1016/j.cub.2019.03.070)
- Some fly visual interneurons are "multi-output devices", neither point neurons nor independent compartments, and are equivalent to a hierarchy of virtual neurons pooling over multiple length scales — [Seung 2025, preprint](https://doi.org/10.1101/2025.02.02.636137)
- T4 single-compartment conductance models:
  - Fitted solutions were either fast excitation (τ < 10 ms) with a slow membrane, or slower excitation with a negligible membrane τ — [Gruntman et al. 2018](https://doi.org/10.1038/s41593-017-0046-4)
  - GluClα shunting plus excitation reproduces multiplication — [Groschner et al. 2022](https://doi.org/10.1038/s41586-022-04428-3)
- A giant-fibre-system conductance model with electrical synapses reproduces escape latencies. Anatomy matters more than conductance densities — [Augustin et al. 2019](https://doi.org/10.1523/ENEURO.0423-18.2019)
- In a larval motoneuron model, the SIZ location was estimated from current filtering — [Günay et al. 2015](https://doi.org/10.1371/journal.pcbi.1004189)

#### Adaptation (AdEx-like) models
- In an insect olfactory spiking network, spike-frequency adaptation (τ<sub>A</sub> 389 ms) is "essential for sparse representations in time", while lateral inhibition sets population sparseness — [Betkiewicz et al. 2020](https://doi.org/10.1523/ENEURO.0305-18.2020)
- A larval olfactory neuromorphic model found the same division, with SFA plus feedback inhibition setting temporal sparseness — [Jürgensen et al. 2021, bioRxiv](https://doi.org/10.1101/2021.06.29.450278)

#### Identifiability theory and validation data
- "A connectome often does not substantially constrain the dynamics of recurrent networks", but "recordings from a small subset of neurons can remove this degeneracy". The theory can prioritise which neurons to record — [Beiran & Litwin-Kumar 2025, Nat Neurosci](https://doi.org/10.1038/s41593-025-02080-4)
- New validation data: whole-brain calcium imaging in behaving flies at 28 volumes/s (60 volumes/s for the central brain) using light-beads microscopy captures fast auditory responses missed by slower imaging — [Gauthey et al. 2026, Nat Commun](https://doi.org/10.1038/s41467-026-72437-1)

### Inferences
- The evidence supports a hybrid per-type model rather than one neuron model:
  - threshold-linear graded units (Lappalainen form, per-type τ and V<sub>rest</sub>) for the optic-lobe columnar and amacrine types, APL, patchy LNs, and nonspiking VNC and antennal interneurons;
  - rate units with saturating output (Pugliese form, r<sub>max</sub> ~200 Hz, size-normalised gain) or LIF/adaptive-LIF with dt ≤0.5 ms for spiking projection neurons;
  - add-ons: slow synaptic components (GABA-B, ORN→PN depression), a curated gap-junction layer, neuromodulatory state variables, and MB/CX plasticity.
- The project's τ = 100 ms matters for timing, not just amplitude. In the linearised VNC model, rhythm frequency scales with 1/τ, so going from 20 ms to 100 ms would push the 7–15 Hz stepping rhythm down to ~1.5–3 Hz (derived, assuming frequency ∝ 1/τ). Visual temporal tuning (fast medulla inputs; state-dependent speed-up) would be similarly distorted.
- Given Beiran & Litwin-Kumar, the per-layer validation strategy should favour datasets that constrain many neurons at once and that are registered to connectome types. Candidates:
  - optic-lobe ON/OFF and DSI tables (Lappalainen's 32 types);
  - Shiu's 164 feeding/grooming predictions;
  - Pugliese's DN→rhythm screen;
  - whole-brain calcium FC (Turner 2021; LBM imaging 2026);
  - specific quantitative anchors (VS gain ×2 in flight; ORN→PN f = 0.78, τ<sub>rec</sub> = 893 ms; KC sparseness; MB LTD ~80–90% after 1 s pairing).

### Gaps
- There is no head-to-head comparison of LIF vs AdEx vs rate vs multicompartment models on the same fly data at whole-brain scale, and no fly-specific AdEx parameter fits.
- Validation datasets with neuron-ID-level registration to MaleCNS types remain limited. Most whole-brain imaging is at region or supervoxel level.
- It is unclear how many cell types are multi-output (Seung 2025 analysed visual interneurons only, as a preprint), and so how often point-neuron assumptions break.
- Several key 2025–2026 modelling results are preprints (Pugliese; Li et al. 2026; Seung 2025; Moreno-Sanchez 2024) and should be rechecked for peer-reviewed versions.
