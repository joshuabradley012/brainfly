# Drosophila descending neurons, VNC circuits and motor neurons: how brain commands become motor patterns

Scope note for the report writer: these notes are compiled for a project that simulates the Janelia male CNS v1.0 connectome (about 166,700 neurons) as identical LIF units. Synapse-count weights are signed by predicted transmitter and each neuron's inputs are normalised to sum to 1. In that model, driving DNg100, DNa02, DNp01 (giant fiber) or MDN at about 25 Hz moves no motor neuron group. Status tags: [PR] = peer reviewed; [PP] = preprint (not peer reviewed); [news] = press/news. Research date: September 2026. Most numbers were checked against full text via Europe PMC/PMC. A few came from abstracts or search snippets, and those are flagged.

---

## 1. VNC connectomes (MANC, FANC, BANC, male CNS v1.0): coverage, completeness of motor and sensory neurons, and how they differ

### Takeaway
Four EM datasets now contain the fly VNC:
- MANC: male, VNC only, densely proofread.
- FANC: female, VNC only, partially proofread.
- BANC: female, brain plus VNC, about 160k neurons, published in Nature in June 2026.
- Male CNS: male, brain plus VNC, 166,691 neurons, published in Cell in 2026.

They broadly agree on neuron classes: about 1,300 DNs, about 1,800 ANs, and about 700+ MNs in a full VNC. Motor neuron counts per appendage differ by a few cells between datasets. No EM dataset resolves gap junctions, and all of them lack biophysical parameters. Sensory and motor neurons are the least complete classes because peripheral-nerve segmentation is poor.

### Cited Findings
**MANC (male adult nerve cord; VNC only; neck connective cut)**
- [PR] MANC holds more than 23,000 neurons connected by more than 10 million presynapses and 74 million postsynapses, with 44 m of arbour. It was the largest published connectome at release. — [Takemura et al., eLife 2024, RP97769](https://elifesciences.org/reviewed-preprints/97769) (figures via eLife page/search summary)
- [PR] MANC annotation counts about 23,500 neurons:
  - 13,066 intrinsic neurons (INs)
  - 1,328 descending neurons (DNs)
  - 1,862 ascending neurons (ANs)
  - 733 motor neurons (MNs): 362 exit left nerves, 361 exit right nerves, and 10 exit the abdominal trunk nerve
  - 5,927 sensory neurons ending in the VNC
  - 535 sensory ascending neurons (SAs)

  Over 5,000 sensory neurons were assigned a modality. Over 35% of intrinsic, ascending and non-motor efferent neurons were matched across segments as serial sets. — [Marin et al., eLife 2024, RP97766](https://elifesciences.org/reviewed-preprints/97766); [bioRxiv 10.1101/2023.06.05.543407](https://doi.org/10.1101/2023.06.05.543407)
- [PR] Marin et al. confirm that larval-born neurons of a hemilineage generally share one transmitter. Earlier-born neurons often express a different one, so hemilineage-based transmitter assignment is imperfect. — [Marin et al. (bioRxiv abstract)](https://doi.org/10.1101/2023.06.05.543407)
- [PR] Cheong et al. (final eLife version, 20 Jul 2026) report the following MN coverage in MANC:

  | MN set | Count |
  |---|---|
  | All MNs | 733, in 319 groups plus 14 singletons, 168 types |
  | T1 leg MNs identified | 142 of 142 |
  | T2 and T3 leg MNs identified by serial homology | 198 of 252 |
  | Wing MNs identified | all but 1 of 26 |
  | Haltere MNs | 7 pairs (3 putative) |
  | Likely neck MNs | 12 pairs (only 3 tentatively matched) |
  | Abdominal MNs | reconstructed but unidentified |

  — [Cheong et al., eLife 2026;13:RP96084 (PMC13384506)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] In MANC, 85% of DNs were assigned to known descending tracts, and two new tracts were found (MTD-III and CVL). — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)

**FANC (female adult nerve cord; VNC only)**
- [PR] FANC was imaged with GridTape serial-section TEM. The first paper reconstructed "all 507 motor neurons that control the limbs". It found a class of leg sensory neurons synapsing directly onto the largest-calibre MNs on both sides of the body, a fast limb-control pathway. — [Phelps et al., Cell 2021](https://doi.org/10.1016/j.cell.2020.12.013)
- [PR] The female VNC contains about 45 million synapses and 14,600 neuronal cell bodies. About 30% of non-sensory neurons were marked proofread by the community at publication. MN counts:
  - Front-leg T1: 69 left and 70 right, mapped to 18 target muscles
  - Wing: 29 per side
  - Haltere: 32
  - Neck: 24
  - Middle-leg tergotrochanter: 3

  Synapse partner precision and recall exceed 80% for partners with more than 3 synapses. — [Azevedo et al., Nature 2024 (PMC11348827)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/); [DOI](https://doi.org/10.1038/s41586-024-07389-x)
- [PR] As of the Stürner et al. writing, the FANC community had proofread "just over 5,000 neurons", including 1,804 ANs. — [Stürner et al., Nature 2025 (PMC12222017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222017/)

**BANC (brain and nerve cord together; female)**
- [PR] BANC contains about 160,000 neurons, about 1,300 DNs and about 1,800 ANs. It is published in Nature (8 Jun 2026) after a bioRxiv preprint (Jul 2025). Proofreading took 155 proofreaders about 3.5 years. The paper identified MNs and effectors of legs, wings, halteres, antennae, eyes, neck, crop, pharynx, proboscis, salivary glands and uterus, plus 49 neck efferent neurons that leave via the cervical nerves. — [Bates et al., Nature 2026 (PMC13518251)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/); [DOI](https://doi.org/10.1038/s41586-026-10735-w); [bioRxiv](https://doi.org/10.1101/2025.07.31.667571); [repo](https://github.com/htem/BANC-project)
- [PR] Sex differences in the VNC, estimated by comparing BANC with MANC:

  | Category | Total | Intrinsic | Ascending | Sensory | Effector |
  |---|---|---|---|---|---|
  | Dimorphic | 2,316 | 1,439 | 359 | 430 | 83 |
  | Female-specific | 600 | 430 | 38 | 56 | 29 |

  — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)
- [PR] BANC notes that "many afferent neurons (that is, sensory neurons) and efferent neurons ... have been incompletely annotated in existing connectome datasets". BANC did expert manual annotation of these classes. — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)

**Male CNS v1.0 (the project's dataset)**
- [PR] The male CNS has 166,691 neurons, including sensory axons, and 11,691 types in the bioRxiv version. It has 46 million presynapses connected to 312 million PSDs. Synapse precision and recall average 0.82/0.81. Neuropil completion is 94% presynaptic and 42% postsynaptic, and 40.1% of connections have both partners proofread. 97.5% of neurons have a type match to FAFB/FlyWire, hemibrain and/or MANC. Parallel `mancType`/`flywireType` annotations are provided. The volume is 160 teravoxels at 8 nm isotropic. — [Berg et al., bioRxiv 2025 / PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/); [bioRxiv DOI](https://doi.org/10.1101/2025.10.09.680999)
- [PR] Peer-reviewed version: Cell 189(18):5504–5526 (2026). It reports "166,700 neurons" and "11,710 neuron types", so the type count differs slightly from the bioRxiv's 11,691, probably through revision. — [Cell 2026](https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6); [PubMed](https://pubmed.ncbi.nlm.nih.gov/42691995)
- [PR] Known limitations of the male CNS:
  - Segmentation problems left some sensory and motor neurons unreconstructed.
  - Gap junctions are not visible.
  - The sensory and motor periphery is "largely isomorphic" between sexes.
  - Sex-specific and dimorphic neurons are concentrated in higher brain centres.

  — [Berg et al. PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/); [Cell abstract via PubMed](https://pubmed.ncbi.nlm.nih.gov/42691995)
- [PR] The male CNS segmentation used the same pipeline as the MANC volume, but MANC is a different male specimen. — [Berg et al. PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
- [PR] Information in the male CNS travels mainly feedforward from sensory nerves to VNC motor neurons. Ascending neurons output a similar number of synapses onto VNC intrinsic neurons as descending neurons do. — [Berg et al. PMC12636603](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
- [PR] Using the "complete EM connectome of the adult male Drosophila", Ceballos et al. charted every axo-axonic input onto 1,314 DNs. — [Ceballos et al., iScience 2026](https://doi.org/10.1016/j.isci.2026.115624)

**Cross-dataset comparison**
- [PR] Across FAFB-FlyWire, FANC and MANC there are:
  - 1,315–1,347 DNs
  - 1,733–1,865 ANs
  - 535–611 SAs

  MANC's 1,328 DNs are "almost twice the previous estimate of 700 DNs". 51% of DN cell types were matched to light-level driver lines. — [Stürner et al., Nature 2025 (PMC12222017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222017/)
- [PR] On the brain side, FlyWire efferent output runs through 1,303 DNs, 80 endocrine neurons and 106 motor neurons. 75% of central-brain output synapses target the VNC via DNs. — [Schlegel et al., Nature 2024](https://doi.org/10.1038/s41586-024-07686-5)
- [PR] Gap junctions "are not yet resolvable in the FANC dataset", and "the spatial resolution of existing electron microscopy datasets is insufficient to resolve gap junctions". — [Lesser et al. 2024 (PMC11356479)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11356479/); [Azevedo et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/)

### Inferences
- FANC's 14,600 cell bodies and MANC's intrinsic plus ascending plus motor total (about 15,660 VNC somata) are the same order of magnitude. Remaining differences probably reflect sex, proofreading and counting conventions: DN and sensory somata sit outside the VNC.
- MN counts per appendage do not match exactly and should not be treated as ground truth:
  - Wing: 26 per side in MANC vs 29 per side in FANC.
  - Haltere: 7 pairs in MANC vs 32 in FANC.
  - Neck: 12 pairs in MANC vs 24 in FANC, which is consistent if FANC's 24 counts both sides.
- For a male CNS model, `mancType` labels give a direct bridge to the MANC-based premotor and CPG literature. Pugliese et al. exploit this bridge (see section 4).
- None of the four datasets is enough on its own to parameterise dynamics. Gap junctions, receptor types (especially glutamate sign), neuromodulators and intrinsic properties are missing from all of them.

### Gaps
- I could not extract exact DN, AN, MN and sensory neuron counts for the male CNS v1.0 from the paper text; they appear to be in figures and tables. The 1,314 DN count comes from Ceballos et al. 2026, which used "the complete EM connectome of the adult male". Pugliese et al. also report n=1,314 DNs, but for BANC. Whether both counts are really 1,314 is unverified.
- BANC's synapse-level completeness statistics were not verified from text. One summary gave "18% of synapses have identified cells on both sides", but I could not confirm the context, so it is not used here.
- Reconciliation of the wing and haltere MN counts between MANC and FANC was not found.

---

## 2. Descending neurons: counts, atlases, activation screens, command-like neurons, population coding, and ascending neurons

### Takeaway
There are about 1,300 DNs in EM, versus light-level estimates of about 700 (Namiki 2018) and about 1,100 (Hsu and Bhandawat 2016). Split-GAL4 atlases and optogenetic screens show that many single DN types can drive stereotyped behaviours, but these are rarely "commands" in the strict sense.

Several "command-like" DNs work by recruiting other DNs through brain collaterals:
- DNp09/P9 turning needs the brain.
- DNb02 turning is lost after decapitation.

Others act stand-alone through VNC outputs: MDN, BDN2/DNg100 and oDN1 still drive walking in decapitated flies.

DN firing rates reach more than 100 spikes/s. Steering DNs modulate stride parameters phase-specifically rather than switching programmes. Ascending neurons (about 1,800) mostly report walking state back to the brain.

### Cited Findings
**Counts, atlases and screens**
- [PR] Namiki et al. estimated about 350 DNs per side (about 700 total) by PA-GFP labelling: maximum 356 cells, mean 321 ± 23, N=4. They built more than 100 split-GAL4 lines, identified 190 bilateral pairs (at least 98 cell types), and described the VNC as layered: dorsal flight neuropils and ventral leg neuropils. — [Namiki et al., eLife 2018 (PMC6019073)](https://doi.org/10.7554/eLife.34272)
- [PR] Hsu and Bhandawat estimated about 1,100 DNs in 6 clusters by dextran backfill. DNs span ACh, GABA, Glu, 5-HT, DA and OA, and "acetylcholine and GABA are employed equally". — [Hsu & Bhandawat, Sci Rep 2016](https://doi.org/10.1038/srep20259)
- [PR] Contradiction: EM transmitter predictions for MANC DNs are 68.4% cholinergic, 16.2% GABAergic, 7.5% glutamatergic, and 7.9% other or below threshold (0.7 cutoff). FISH validation of 53 DN types was correct for:
  - ACh: 23/28 (+4 uncertain)
  - GABA: 3/9 (+1 uncertain)
  - Glu: 9/10 (+1 uncertain)

  The authors conclude ACh and Glu predictions are good but "GABA predictions are still unverified". — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/); contradicts [Hsu & Bhandawat 2016](https://doi.org/10.1038/srep20259)
- [PR] Cande et al. screened 130 DN split-GAL4 lines optogenetically with unsupervised behaviour mapping (about 700 million images). 91 of 130 lines (69%) significantly changed behaviour-space density. Most DNs drove stereotyped behaviours, several DNs drove similar behaviours, and effects depended on prior behavioural state. — [Cande et al., eLife 2018 (PMC6031430)](https://doi.org/10.7554/eLife.34275)
- [PR] In a screen of about one third of all DNs, P9 (DNp09) was the only DN that initiated walking. P9 drives forward walking with ipsilateral turning and is needed for courtship pursuit. BPN, a central-brain neuron, drives fast straight walking. — [Bidaye et al., Neuron 2020](https://doi.org/10.1016/j.neuron.2020.07.032); [bioRxiv v1 full text](https://www.biorxiv.org/content/10.1101/798439v1.full)

**Command-like neurons**
- **BDN2 = DNg100 (forward walking)** [PR]
  - Optogenetic activation of BDN2 and oDN1 initiates walking, and BDN2 has "a much stronger phenotype".
  - "Even decapitated oDN1 and BDN2 activated flies initiated robust forward walking", so their VNC outputs are sufficient, unlike P9.
  - Only BDN2 silencing had a strong loss-of-function effect (text truncated in extraction).
  - Halting uses GABAergic walk-OFF neurons (FG, BB) that inhibit walking DNs in the brain, and cholinergic VNC "brake" (BRK) neurons.
  - The study used a FlyWire LIF model in silico.

  — [Sapkal et al., Nature 2024 (PMC11446846)](https://doi.org/10.1038/s41586-024-07854-7). DNg100 is the current name for BDN2: "DNg100 is referred to as BDN2" — [Pugliese et al. PP](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- [PP] Increasing DNg100>CsChrimson laser intensity (0.03, 0.09, 0.33 mW/mm²) in decapitated flies raised forward velocity and stepping frequency. — [Pugliese et al. 2025/2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- **MDN (moonwalker, backward walking)** [PR]
  - MDN is required for backing away from an impassable barrier and sufficient to trigger backward walking.
  - The ascending MAN neuron promotes persistent backward walking. — [Bidaye et al., Science 2014](https://doi.org/10.1126/science.1249964)
  - LC16 looming neurons act through MDN, and asymmetric MDN activity produces turning while backing. — [Sen et al., Curr Biol 2017](https://doi.org/10.1016/j.cub.2017.02.008)
  - MDN acts through distributed VNC targets ("several dozen"): LBL40 (T3-specific) gives the hindleg stance power stroke by tibia flexion, and LUL130 lifts legs to start swing. Decapitated flies walk backward when MDN VNC axons are activated. — [Feng et al., Nat Commun 2020](https://doi.org/10.1038/s41467-020-19936-x)
  - Larval MDNs, which persist into adults, both activate a backward-active premotor neuron and disynaptically inhibit a forward premotor neuron. — [Carreira-Rosario et al., eLife 2018](https://doi.org/10.7554/eLife.38554)
  - In vivo recordings show MDN integrates antennal touch. MDN is gated out during flight. — [Liessem et al., Curr Biol 2026](https://doi.org/10.1016/j.cub.2026.06.045)
- **Giant fiber (DNp01, escape take-off)** [PR]
  - Looming stimuli evoke two take-off modes: long-mode, which gives stable flight, and short-mode, which is faster but unstable.
  - Intracellular GF recording showed that the timing of the GF spike relative to parallel escape circuits selects the mode. The GF has a higher activation threshold but can override ongoing behaviour. — [von Reyn et al., Nat Neurosci 2014](https://doi.org/10.1038/nn.3741)
  - The rapid take-off is on average about 8 ms faster than the controlled one. — [HHMI news on von Reyn 2014](https://www.hhmi.org/news/quick-getaway-how-flies-escape-looming-predators) [news]
  - The GF linearly integrates looming angular size and angular velocity. — [von Reyn et al., Neuron 2017](https://doi.org/10.1016/j.neuron.2017.05.036)
  - GF silencing lowers survival against damselfly predators. — [Chai et al., Proc R Soc B 2025](https://doi.org/10.1098/rspb.2024.1724)
  - Direct GF stimulation gives a DLM short-latency response of about 1.4 ms. Retinal stimulation gives a long-latency response of about 5 ms. — [Gaitanidis et al., PLoS Biol 2025](https://doi.org/10.1371/journal.pbio.3003553)
- **Steering DNs (DNa01, DNa02, DNg13)** [PR]
  - DNa01 predicts sustained low-gain steering and DNa02 transient high-gain steering.
  - Turning velocity is linearly related to the right–left difference in DNa02 activity.
  - Inputs from the head-direction system and sensory pathways are arranged as a "see-saw": excitation of one copy comes with inhibition of the other. — [Rayshubskiy et al., eLife 2025](https://doi.org/10.7554/eLife.102230)
  - DNa01, DNa02, DNb05, DNb06 and DNg13 all correlate with rotational velocity.
  - DNg13 depolarisation lengthens contralateral (outside) strides. DNa02 hyperpolarisation lengthens ipsilateral strides, so DNa02 attenuates inside strides.
  - DN rate changes lead rotational velocity and stride changes by about 150 ms.
  - DNa02's stride-locked modulation is only about 15 spikes/s, "approximately 10% of the cell's dynamic range".
  - DNg13 can be driven above 100 spikes/s; trials analysed required more than 130 spikes/s.
  - One DN can have opposite effects at different phases of the step cycle. — [Yang et al., Cell 2024 (PMC12778575)](https://doi.org/10.1016/j.cell.2024.08.033)
- **Flight DNs** [PR]
  - DNg02 is a population of at least 15 near-identical cell pairs projecting to the dorsal flight neuropil. Activating different numbers of DNg02 cells sets wingbeat amplitude over a wide range: a population code. — [Namiki et al., Curr Biol 2022](https://doi.org/10.1016/j.cub.2022.01.008)
  - Four DNs appear sufficient for flight saccades: DNae014 (excitatory) plus DNb01 (inhibitory) per side. VES041 inhibits all four and suppresses saccades. — [Ros et al., Curr Biol 2024](https://doi.org/10.1016/j.cub.2023.12.047)
  - A DN correlates with spontaneous and visually evoked saccades. — [Schnell et al., Curr Biol 2017](https://doi.org/10.1016/j.cub.2017.03.004)
  - DNp03 is a collision-avoidance hub that connects directly and indirectly to wing and neck MNs. Natural saccades depend on a network of interconnected DNs that partly compensates when DNp03 is lost. — [Croke et al., Curr Biol 2026](https://doi.org/10.1016/j.cub.2025.11.035)
- **Landing DNs** [PR] For DNp07 and DNp10, silencing impairs landing, activation drives it, and spike rate sets leg-extension amplitude. Their visual responses are strongly reduced when the fly is not flying, and octopamine mimics the flight effect in one of them. — [Ache et al., Nat Neurosci 2019](https://doi.org/10.1038/s41593-019-0413-4)
- **Grooming DNs** [PR]
  - Antennal grooming uses a layered command circuit: JO chordotonal neurons feed brain interneurons aBN1 and aBN2 and parallel antennal DNs (aDN1, aDN2). Neurons in each layer are sufficient, but grooming duration differs by layer. — [Hampel et al., eLife 2015](https://doi.org/10.7554/eLife.08758)
  - Different DNs start head sweeps, leg rubs, or both. Unilateral activation of one DN coordinates both legs for rubbing, while another DN decouples the legs. — [Guo et al., Curr Biol 2022](https://doi.org/10.1016/j.cub.2021.12.055)
  - The grooming sequence arises from a suppression hierarchy among parallel motor programmes. — [Seeds et al., eLife 2014](https://doi.org/10.7554/eLife.02951)
- **Courtship song DNs** [PR]
  - P1 and pIP10 in the brain mediate the decision to sing. Thoracic dPR1, vPR6 and vMS11 time and shape pulses. — [von Philipsborn et al., Neuron 2011](https://doi.org/10.1016/j.neuron.2011.01.011)
  - Two descending pathways give nested input: one VNC population is active in both pulse and sine song, and an expanded population is active in pulse song. — [Shiozaki et al., Nat Neurosci 2024](https://doi.org/10.1038/s41593-024-01738-9)
  - The male CNS paper names the song DNs pIP10 and pMP2, and the wing premotor neurons TN1A, vPR9 and dPR1. — [Berg et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
  - Song circuits are dimorphic: DNa12/aSP22 for courtship, AN neurons of hemilineage 08B for song. — [Stürner et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222017/)
- **DNb08** [PP] Simulations predicted, and optogenetics (SS70620>CsChrimson) confirmed, that DNb08 (4 neurons) drives rhythmic front- and middle-leg movements in decapitated flies (n=10), resembling "searching or flailing". — [Pugliese et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)

**Population coding vs command**
- [PR] Command-like DNs recruit networks of other DNs through direct excitatory brain connections. 85% of DNs have axon collaterals, mostly in the GNG. Decapitation separates two kinds:
  - "Broadcaster" DNs need downstream DNs: DNp09 behaviour degrades without the head, though abdominal contraction remains. DNb02 connects to 20 other DNs and drives turning when intact, but only front-leg flexion when headless.
  - "Standalone" DNs work without the head: MDN still drives backward walking.

  DN networks sit in behaviour-specific clusters that inhibit one another. — [Braun et al., Nature 2024 (PMC11186778)](https://doi.org/10.1038/s41586-024-07523-9)
- [PR] BDN2 and oDN1 have DN connectivity patterns similar to DNp09. — [Braun et al. 2024](https://doi.org/10.1038/s41586-024-07523-9)
- [PR] Decapitated P9-activated flies lose the forward-turning phenotype, but MDN's VNC circuit is sufficient. — [Sapkal et al. 2024](https://doi.org/10.1038/s41586-024-07854-7)
- [PR] Imaging nearly 100 DNs per fly showed the largest fraction encode walking and many encode turning. Few encode speed, and some encode odours rather than behaviour. The same paper cites about 1,100 DNs, following the pre-EM estimate. — [Aymanns et al., eLife 2022](https://doi.org/10.7554/eLife.81527)
- [PR] DNs in MANC are grouped by output neuropil:
  - DNut (upper tectulum: neck, wing, haltere)
  - DNwt, DNnt, DNht
  - DNfl, DNml, DNhl (front, middle, hind leg)
  - DNit, DNlt (intermediate and lower tectulum)
  - DNad (abdominal)
  - DNxn, DNxl (broad, multi-neuropil)

  Upper-tectulum classes are about 75–100% population types (more than 2 cells per group), while leg DNs are more often pairs (about 50–100%). The DN:MN ratio is about 404:392 for leg neuropils and 381:106 for the upper tectulum. — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] The BANC authors define 17 behaviour-centric AN/DN clusters:
  - flight power
  - flight steering (2)
  - walking
  - walking steering
  - head orienting
  - threat response
  - feeding
  - reproduction
  - grooming
  - postural control
  - visceral control
  - probing
  - 4 sensory-centric clusters

  Single ANs and DNs often reach several body parts. — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)

**Ascending neurons**
- [PR] Imaging of 247 AN ROIs from 70 sparse driver lines shows ANs "most predominantly encode walking". Self-motion signals go to the AVLP and discrete actions to the GNG. — [Chen et al., Nat Neurosci 2023](https://doi.org/10.1038/s41593-023-01281-z)
- [PR] Chains of DNs and ANs span the neck and may support motor sequences. — [Stürner et al. 2025](https://doi.org/10.1038/s41586-025-08925-z)
- [PR] Eight cholinergic ANs (AN08B098) make axo-axonic synapses onto the giant fibers in the VNC and increase DNp01 excitability. — [Ceballos et al., iScience 2026](https://doi.org/10.1016/j.isci.2026.115624)

**Recent 2026 preprints on walking control**
- [PP] Central-brain neurons can start walking and grade its speed by recruiting a specific DN population. This drive is suppressed during flight. — [Dallmann, ..., Ache, bioRxiv 2026](https://doi.org/10.64898/2026.01.04.697356)
- [PR] DopaMeander dopaminergic neurons drive forward walking with more turning. — [Liessem et al., Curr Biol 2026](https://doi.org/10.1016/j.cub.2026.06.045)

### Inferences
- Taken together, the DN literature suggests driving one DN type at a modest rate is not how real flies generate behaviour. Evidence:
  - DNs have large dynamic ranges: about 150 spikes/s is implied for DNa02, and DNg13 exceeds 100 spikes/s.
  - Walking is normally accompanied by co-activation of DN networks.
  - Several behaviours need that recruitment in the brain.

  About 25 Hz on a single type is at the low end of physiological DN drive.
- MDN and BDN2/DNg100 are the best test cases for a VNC-only pathway, because decapitated flies still walk (backward or forward) when their VNC axons are driven. DNp09 is a poor test because it needs the brain. For the GF, the relevant pathway partly depends on gap junctions (section 5), which the connectome cannot show.
- Because MANC and FlyWire DN transmitter predictions disagree with FISH for GABA, some "inhibitory" DN edges in a model may actually be excitatory, or the reverse.

### Gaps
- No verified behaviour for DNg11 was found. Braun et al. 2024 list DNg11 only among nine DNs placed on the broadcaster-to-standalone continuum.
- No verified whole-cell firing-rate ranges were found for DNg100, MDN or DNa02 during natural walking (Rayshubskiy 2025 gives filters, not absolute rates in the extracted text).
- The original paper in which "BDN2" was first named was not pinned down. The earliest confirmed functional description is Sapkal et al. 2024 (Nature).

---

## 3. VNC motor circuits: CPG evidence, interleg coordination, premotor organisation, MN pools and recruitment, wing, haltere and neck MNs, take-off, grooming, song and flight

### Takeaway
The evidence now favours per-leg central rhythm generators in the fly VNC:
- Leg stumps oscillate on their own.
- Decapitated flies step when BDN2/DNg100, MDN or DNb08 is driven.
- Grooming rhythms speed up with temperature and persist with reduced sensory feedback.
- A 2026 preprint finds a per-leg CPG with an intrinsic period that appears when proprioception is reduced.

Proprioceptive and load feedback shapes the step, and interleg coordination seems to use central coupling that feedback modulates. No fictive-walking preparation of the isolated adult VNC is reported in the sources found.

Premotor networks:
- They are modular.
- About 10% of MN input comes directly from DNs.
- Most DN-to-MN paths are indirect and multi-layer.
- Leg premotor synapses scale with MN size (a size principle), while wing steering premotor input does not.

Flight power is generated by stretch-activated muscles plus a gap-junction-coupled MN "CPG".

### Cited Findings
**CPGs and interleg coordination**
- [PR] When legs are amputated, stumps "were still rhythmically active during walking" at a "high and relatively constant oscillation frequency at all walking speeds". Stump coupling to intact legs is loose at low speed and 1:1 at high speed. — [Berendes et al., J Exp Biol 2016](https://doi.org/10.1242/jeb.146720)
- [PP] "Each leg is governed by its own CPG module with an inherent cycle period that is unmasked when proprioceptive feedback is reduced". Contact-driven load inputs and descending brain inputs shape the within-leg step. "Central coupling pathways underlie inter-leg coordination", and feedback and DNs modulate that coupling. Co-stimulating specific DNs speeds the rhythm. — [Sapkal et al., bioRxiv May 2026](https://doi.org/10.64898/2026.04.29.721658)
- [PR] Silencing leg sensory neurons (5-40Leg>TNT, and chordotonal inactivation) reduced step precision, but "interleg coordination and the ability to execute a tripod gait were unaffected". — [Mendes et al., eLife 2013](https://doi.org/10.7554/eLife.00231)
- [PR] Silencing mechanosensory neurons changed step kinematics "across all speeds" on a linear treadmill. On a split belt, flies keep heading by adapting middle-leg step distance. — [Pratt et al., Curr Biol 2024](https://doi.org/10.1016/j.cub.2024.08.006)
- Gait vs speed, where sources disagree:
  - [PR] Flies control speed almost entirely through step frequency. They are tripod at high speed, with tetrapod and wave-like patterns at low speed. — [Wosnitza et al., J Exp Biol 2013](https://doi.org/10.1242/jeb.078139)
  - [PR] A single continuum of coordination patterns, with no preferred gaits. — [DeAngelis et al., eLife 2019](https://doi.org/10.7554/eLife.46409)
  - [PR] "Drosophila uses a tripod gait across all walking speeds". — [Chun et al., eLife 2021](https://doi.org/10.7554/eLife.65878)
- [PR] Walking strides repeat at about 10 Hz. — [Yang et al. 2024](https://doi.org/10.1016/j.cell.2024.08.033)
- [PP] Real stepping is about 7–15 Hz. — [Pugliese et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- [PR] 33 postembryonic hemilineages contribute more than 90% of neurons per thoracic hemisegment. Decapitated flies are mostly quiescent. Thermogenetic activation in decapitated flies gives three levels of response:
  - Local-interneuron hemilineages: tonic or phasic leg movements without interlimb coordination.
  - Projection hemilineages: intersegmentally coordinated walking that is "erratic and not organized in the tripod gait".
  - Higher hemilineages: complex acts such as take-off.

  — [Harris et al., eLife 2015](https://doi.org/10.7554/eLife.04493)
- [PR] The isolated larval CNS produces fictive forward and backward waves about 10 times slower than crawling. The waves persist after removal of the brain and SEZ. — [Pulver et al., J Neurophysiol 2015](https://doi.org/10.1152/jn.00731.2015)
- [PR] Reviews: [Bidaye, Bockemühl & Büschges, J Neurophysiol 2018](https://doi.org/10.1152/jn.00658.2017); [Mantziaris, Bockemühl & Büschges, Dev Neurobiol 2020](https://doi.org/10.1002/dneu.22738); [Goulding, Bollu & Büschges, Annu Rev Neurosci 2025](https://doi.org/10.1146/annurev-neuro-112723-042229)

**Premotor organisation (connectomics)**
- [PR] In MANC, most DN-to-MN paths are indirect, "involving multiple layers of neurons between DN and MN":
  - MN groups get on average 7% of their input directly from DNs.
  - About 80% of MN groups get some direct DN input.
  - Neck MNs, some abdominal MNs, and several wing and haltere MNs get more than 20% (up to about 60%) directly from DNs.
  - In the Bayesian layer analysis, neck and abdominal MNs are closest to DNs, and leg MNs are about twice as far from DNht as neck, wing and haltere MNs.

  — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] Infomap splits premotor interneurons into 37 communities, 18 of which have at least 50 cells:
  - one per leg neuropil per side
  - five covering the upper tectulum
  - three in the abdominal neuromeres
  - three intermediate

  Upper-tectulum DNs feed communities 8–10, which output to wing MNs. The hemilineages that DNs and MNs connect to match expected function. — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] FANC T1 leg and wing premotor networks (Lesser et al.):

  | Measure | Leg (T1) | Wing |
  |---|---|---|
  | MNs | 69 | 29 |
  | Premotor neurons | 1,546 | 1,784 |
  | Synapses from premotor neurons | 212,190 | 144,668 |
  | DN share of MN input | 9.1 ± 4.2% | 11.2 ± 6.5% |

  - Local premotor neurons make up 43% of leg premotor neurons but supply 63.4 ± 9% of each MN's synaptic input.
  - Leg MNs get more input from putatively glutamatergic premotor neurons.
  - Leg modules show proportional connectivity: "each preMN provides the same output weight onto all MNs within both the extensor and flexor modules". Leg MN synapse density is about 0.45 synapses/µm² (r=0.94). This is a wiring basis for size-ordered recruitment.
  - Wing steering modules lack this proportionality.
  - Antagonist modules get less shared input: module weight 0.012 vs 0.020.
  - Four wing steering MNs get more than 10% sensory input: iii3 18.5%, b1 17.3%, b3 13.5%, i2 11%.

  — [Lesser et al., Nature 2024 (PMC11356479)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11356479/)
- [PR] Hemilineages 13A and 13B contain about 120 GABAergic inhibitory neurons (FANC right T1: 62 13A plus 64 13B). They form pathways that inhibit MN groups, disinhibit antagonists and produce flexion–extension alternation. More 13B-to-flexor-inhibiting-13A connections suggest a "flexor burst generator". Pulsed optogenetic activation "triggers the circuit's intrinsic rhythm rather than pacing it". — [Syed, Ravbar & Simpson, eLife 2026 (PMC12844901)](https://doi.org/10.7554/eLife.106446). The bioRxiv title was "Inhibitory circuits generate rhythms...", and the final title is "...control leg movements...".

**Leg MN pools and recruitment**
- [PR] Azevedo et al. 2020 on leg MNs:
  - The fly leg has 14 muscles innervated by 53 MNs (light-microscopy counts).
  - Tibia flexor MNs form a gradient. Input resistance is about 150 MΩ (fast), 300 MΩ (intermediate) and 700 MΩ (slow).
  - Fast and intermediate MNs are silent at rest, while slow MNs fire spontaneously (about 12–30 Hz).
  - One fast-MN spike produces enough force to support body weight.
  - Recruitment in behaving flies is usually slow to fast, but MN types get different proprioceptive feedback, so size is not the only factor.

  — [Azevedo et al., eLife 2020 (PMC7347388)](https://doi.org/10.7554/eLife.56754)
- [PR] Flies use 14 intrinsic leg muscles and 3–5 body-wall muscles. — [Syed et al. 2026](https://doi.org/10.7554/eLife.106446). EM counts of 69–71 T1 MNs per side (FANC, MANC) exceed the light-microscopy 53, probably because body-wall and coxal muscles are included.

**Wing, haltere and neck MNs; flight control**
- [PR] About a dozen pairs of steering muscles control the wing base. Each of four sclerites has large phasic muscles for big changes and small tonic muscles for fine continuous adjustment. — [Lindsay, Sustar & Dickinson, Curr Biol 2017](https://doi.org/10.1016/j.cub.2016.12.018)
- [PR] Power muscles are stretch-activated and keep oscillating as long as MN activity supplies calcium. — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] DLM MNs MN1–5 fire at about 3–12 Hz during tethered flight, with a linear f–I curve over 3–30 Hz. MN firing rate correlates with wingbeat frequency (r²=0.63 within animals). Weak ShakB electrical synapses combined with specific excitability desynchronise MN spikes into fixed "splay-state" sequences. shakB knockdown abolishes coupling and increases synchrony, so the flight "CPG" is MNs plus gap junctions turning unpatterned premotor drive into ordered firing. — [Hürkey et al., Nature 2023](https://doi.org/10.1038/s41586-023-06099-0)
- [PR] Haltere muscles, driven by descending visual input, set the spike timing of wing steering MNs, acting as "an adjustable clock". — [Dickerson et al., Curr Biol 2019](https://doi.org/10.1016/j.cub.2019.08.065)
- [PR] Song and flight share most wing MNs. The flight command overrides song, and octopamine is a candidate for stabilising flight but not song. — [O'Sullivan et al., Curr Biol 2018](https://doi.org/10.1016/j.cub.2018.06.038)
- [PR] Neck: activating one neck MN moves the head towards a fixed pose whatever the start posture, which a model explains through ongoing proprioceptive feedback. Suppressing one proprioceptor class changes this convergence. — [Gorko et al., Nature 2024](https://doi.org/10.1038/s41586-024-07222-5)

**Take-off**
- [PR] The GF contacts TTMn directly and indirectly, and reaches the DLMns through GFC2 subsets and the PSI. — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] GFC interneurons, electrically coupled to the GF, synapse onto leg flexor and wing MNs. GFC4 targets the largest trochanter–femur and tibia flexor MNs, bypassing the normal size-ordered recruitment during the ballistic escape. — [Azevedo et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/)

**Grooming**
- [PR] Grooming uses nested rhythms: sweeps and rubs at 5–7 Hz (about 200 ms per movement), and bout alternation at 0.3–0.6 Hz. Both speed up with temperature, a hallmark of a CPG. With reduced sensory feedback (front-leg amputation) periodicity persists, but the slow alternation becomes slower. — [Ravbar, Zhang & Simpson, eLife 2021](https://doi.org/10.7554/eLife.71508)
- [PR] Dusted flies rub and sweep at about 7–8 Hz. — [Syed et al. 2026](https://doi.org/10.7554/eLife.106446)
- [PR] Antennal-grooming leg sweeps run at about 8 Hz. Moving one body part does not need proprioceptive feedback from the others. — [Özdil et al., Nat Commun 2026](https://doi.org/10.1038/s41467-026-72152-x)

**Courtship song**
- [PR] The VNC song circuit is two nested feedforward pathways with extensive reciprocal and feedback connections. The larger network makes pulse song and a subset makes sine song. — [Lillvis et al., Curr Biol 2024](https://doi.org/10.1016/j.cub.2024.01.015)

### Inferences
- Pattern generation is probably local to each leg neuropil. Several lines of evidence agree:
  - Behavioural decoupling (Berendes, Sapkal 2026)
  - Decapitated DN activation (Sapkal 2024, Feng 2020, Pugliese)
  - Inhibitory 13A/13B motifs (Syed)
  - The connectome CPG search (section 4)

  So a model that drives DNs but gets no leg-MN activity is failing at DN-to-premotor transmission or at local recurrent excitation. It is not simply missing a brain-level programme.
- Only about 10% of MN input comes from DNs. The rest is local premotor (about 63%) and sensory. In a model with inputs normalised to sum to 1, DN and premotor drive onto an MN is diluted by sensory and inhibitory inputs that are silent or dominant in the model.
- The size principle in leg modules (equal fractional weights across a module, synapse density about 0.45/µm²) means real recruitment order comes from MN excitability (150–700 MΩ), not wiring. Identical LIF units with input normalisation cannot show size-ordered recruitment.
- Interleg coordination is contested:
  - Mendes 2013: coordination survives sensory silencing.
  - Sapkal 2026 (PP): it needs central coupling pathways.
  - Pugliese (PP): connectome-only simulations do not couple legs.
  - Harris 2015: hemilineage-driven stepping is not tripod.

  So coordination probably needs central coupling that is too weak or mis-signed in current models, and/or feedback.

### Gaps
- I found no report of a fictive walking rhythm from an isolated adult Drosophila VNC, as in pilocarpine preparations in stick insects. Its absence is not confirmed, only not found.
- No direct recordings from putative walking-CPG interneurons (E1, E2, I1; see section 4) were found. The Pugliese authors say such recordings are still needed.
- No direct evidence was found for non-spiking premotor interneurons in adult Drosophila. Harris et al. 2015 cite spiking and non-spiking interneurons in grasshoppers only.

---

## 4. Computational models of the VNC from connectomes (2023–2026): what they needed

### Takeaway
The key model is Pugliese et al. (Tuthill and Brunton labs; bioRxiv Sep 2025, v2 Apr 2026, not yet peer reviewed). It simulated MANC, FANC, BANC and the male CNS as a rate network and found:
- DNg100 is the top driver of leg rhythms.
- DNb08 also drives rhythm, confirmed experimentally.
- A 3-neuron CPG (E1, E2, I1) repeats in every leg.
- There is no interleg coordination.

What made it work:
- Raw synapse counts × a single global scale (b=0.03). There is no per-neuron input normalisation.
- Per-neuron threshold multiplied by, and gain divided by, relative neuron size. The authors call this "crucial": without it there were no robust oscillations.
- Connections under 5 synapses dropped in MANC and the male CNS.
- Glutamate treated as inhibitory.
- Random parameter heterogeneity.
- Strong DN drive: Istim 250–400 against a threshold of about 7.5 × size.

No intrinsic bursting was needed. An LIF version with Shiu et al. brain-model parameters (0.275 mV per synapse, raw counts) also gave rhythm. Connectome graph analyses (Cheong, BANC) use input-fraction normalisation, but only as static distance or influence metrics.

### Cited Findings
**Pugliese et al. 2025/2026 [PP]** — [bioRxiv 10.1101/2025.09.12.675944](https://www.biorxiv.org/content/10.1101/2025.09.12.675944v1.full); [PMC13142387 (preprint, v. 30 Apr 2026, "not yet peer reviewed")](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); [code: github.com/smpuglie/Pugliese_cpg_2025 (JAX, Hydra configs, e.g. `experiment=DNg100_Stim`; data on Zenodo)](https://github.com/smpuglie/Pugliese_cpg_2025)

*Model equation and parameters*
- The rate model is τᵢ drᵢ/dt = max(rᵢᵐᵃˣ·tanh((aᵢ/rᵢᵐᵃˣ)(Iᵢ(t) + b·Σⱼ wᵢⱼ rⱼ(t) − θᵢ)), 0) − rᵢ(t).
- |wᵢⱼ| is the synapse count from j to i. The sign is + for predicted cholinergic neurons and − for GABAergic or glutamatergic neurons.
- b = 0.03 was chosen by hyperparameter search on monosynaptic chains, so that downstream activity follows input and decays after it ends.
- Per-neuron parameters are redrawn in each replicate:
  - gain a* ~ N(1, 0.1), divided by relative size
  - threshold θ* ~ N(7.5, 0.6), multiplied by relative size
  - rmax ~ N(200, 10) Hz
  - τ ~ N(20 ms, 2 ms)
- Size is neuron volume (MANC, male CNS) or mesh surface area (FANC, BANC), divided by the dataset median.
- The rationale is that larger neurons have lower input resistance, and "postsynaptic potential amplitudes scale linearly with the number of synapses per unit area in Drosophila neurons". Quote: "without adjusting a and θ for size, the network does not produce robust oscillations".

*On normalisation, weight floor and propagation*
- The authors write: "Other connectome analyses have normalized the strength of synaptic connections by the total number of synaptic inputs received by the postsynaptic cell, which is in practice similar to size normalization, since large neurons tend to receive many synapses". They did not use input normalisation.
- There is a floor of 5 synapses per connection in MANC and the male CNS, but none in FANC and BANC. Weight perturbations were not allowed to flip sign.

*Networks simulated*
- MANC front-leg network: 4,604 neurons (1,318 DNs, 144 leg MNs, 3,142 premotor neurons).
- Male CNS subnetwork: 4,310 neurons. Brain-side synapses were excluded.
- BANC: all 1,314 DNs included.
- Full MANC: 23,532 "Traced" neurons, including all six leg neuropils, DN axons, sensory axons, and wing, haltere and abdominal regions.

*Stimulation*
- DNs got step input in arbitrary units.
- Istim for DNg100 was 250 (MANC), 150 (FANC) and 400 (male CNS and BANC).
- Stimulus was auto-tuned (up to 10 iterations) so that between 5 and 1,500 neurons were recruited.

*DN activation screen*
- 933 excitatory DNs were screened with 16 replicates each.
- 184 (19.7%) gave no interpretable activity.
- Of the remaining 749, 455 (60.7%) scored zero.
- Only 37 (4.0% of all) had a mean rhythmicity score above 0.5. DNg100 was the top driver.
- A single DNb08 neuron gave rhythm in MANC, FANC and the male CNS, but not BANC.
- The CPG neurons also get input from DNg97 (oDN1), DNg74 (web), DNg12 and DNg62 (aDN1).

*The core CPG*
- Pruning found E1 = IN17A001, E2 = INXXX466 (cholinergic) and I1 = IN16B036 (inhibitory).
  - They are all-to-all connected, strongest E1→E2, E2→I1, I1→E1 and I1→E2.
  - Only E1 gets direct DNg100 input.
  - FANC gives a variant with I2 = IN19A007 and E3 = IN19B012, found in 70.4% of 1,024 pruning screens.
- Linearising the 3-neuron circuit gives an oscillation near 14 Hz.
- Frequency is inversely proportional to mean τ.
- Stronger DNg100 drive raises frequency in the full network but not in the minimal circuit.
- Silencing E1 or E2 abolishes rhythm in all four datasets. The inhibitory cell is needed but its identity varies.
- Rhythm survives up to about 10% weight noise, about the estimated uncertainty in synapse counts.
- The motif repeats in all six legs in all four datasets.

*Outputs and failures*
- Within a leg, coxa promotor and remotor show a realistic phase offset.
- There is no consistent left–right phase and no coupling among the six legs, even in the full MANC. Hind-leg rhythm is weaker.
- "Other key muscles likely active during walking were either silent or non-rhythmic".
- The authors attribute these failures to missing "proprioceptive feedback, mechanical coupling, neuromodulation, or combinatorial activity of multiple DNs". They add that the datasets lack "ion channels, receptors, neuromodulators, and gap junctions".
- MDN, the GF and DNa02 are not discussed in the extracted text.

*Spiking check*
- An LIF variant "without tuning" used Vrest = Vreset = −52 mV, Vthresh = −45 mV, refractory 2.2 ms, τm 20 ms, τsyn 5 ms, wsyn 0.275 mV, delay 1.8 ms, dt 0.01 ms and "network input = 0.15 nA". It gave similar rhythmic spiking.

**Shiu et al., Nature 2024 [PR] (FlyWire brain LIF; no VNC)** — [DOI](https://doi.org/10.1038/s41586-024-07763-9); [PMC11446845](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- The model is LIF with α-synapses on FlyWire (more than 125k neurons, 50M synapses). Parameters:
  - Vrest −52 mV, Vreset −52 mV, Vthreshold −45 mV
  - Rm 10 kΩ·cm², Cm 2 µF/cm², so τm = 20 ms
  - refractory 2.2 ms, τsyn 5 ms, delay 1.8 ms
  - Wsyn = 0.275 mV, "the single free parameter"
- The weight is (synapse count) × (±1 by transmitter) × Wsyn. There is no input normalisation.
- Wsyn was set so that sugar GRNs at 100 Hz gave about 80% of maximal MN9 firing. Results were robust to ±30% Wsyn when input rates were compensated.
- Inputs were Poisson at 10–200 Hz (sugar) and 20–260 Hz (water).
- Glutamate is treated as inhibitory by default. Assuming glutamate is excitatory removes the model's prediction that bitter and Ir94e taste is inhibitory.
- FlyWire transmitter mix: 55% ACh, 24% Glu, 14% GABA and 7% monoamine.
- The model predicted MN9 (proboscis) activation and the antennal-grooming circuit (aBN/aDN) response to JO activation.

**Other connectome or embodied models**
- [PR] Sapkal et al. used the Shiu FlyWire LIF model in silico to test how halting neurons override walking pathways. — [Sapkal et al., Nature 2024](https://doi.org/10.1038/s41586-024-07854-7)
- [PR] The inhibitory 13A/13B circuit model uses "rate based" units, not spiking. A 40-unit RNN "black box" supplies excitatory sensory input. The model reproduces rhythmic leg movements. — [Syed et al., eLife 2026](https://doi.org/10.7554/eLife.106446)
- [PR] A simulated activation screen of a brain antennal-grooming network found recurrent excitation plus "broadcast inhibition" ("asteroid" neurons), then validated it experimentally. — [Özdil et al., Nat Commun 2026](https://doi.org/10.1038/s41467-026-72152-x)
- [PR] Graph metrics with input normalisation, not dynamics:
  - Cheong et al. compute "indirect connectivity strength" by normalising "all synapse weights to input fractions (sum of inputs for each neuron equals 1)" and multiplying the matrix by path length. Values are re-normalised per path length by the non-zero mean. — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
  - BANC "adjusted influence" is the steady state of a linear system where each weight is "the number of synapses ... as a fraction of the total synaptic input of the postsynaptic cell". It is log-transformed plus a constant, unsigned, and "inversely proportional to the network distance". The modal score is 20 for direct and 5 for indirect connections. — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/); [scores: Harvard Dataverse 10.7910/DVN/7WTH1N](https://doi.org/10.7910/DVN/7WTH1N); [code: Zenodo 10.5281/zenodo.15999929](https://doi.org/10.5281/zenodo.15999929)
- [PR] Body models with controllers that are not connectome-derived:
  - NeuroMechFly (MuJoCo/PyBullet lineage): [Lobato-Rios et al., Nat Methods 2022](https://doi.org/10.1038/s41592-022-01466-7); [NeuroMechFly v2, Nat Methods 2024](https://doi.org/10.1038/s41592-024-02497-y). v2 has biologically inspired controllers, RL, and a connectome-constrained visual network.
  - flybody: RL-trained controllers produce walking and flight. — [Vaxenburg et al., Nature 2025](https://doi.org/10.1038/s41586-025-09029-4)
  - A 3D kinematic model with a layered controller shows that robustness breaks down when sensorimotor delays exceed the physiological range. — [Karashchuk et al., eLife 2025](https://doi.org/10.7554/eLife.99005)
- [PP] A whole-brain "Fly-connectomic Graph Model" is trained by deep RL to control a biomechanical fly. The search summary reports LIF units with a surrogate gradient. It is not a purely connectome-derived dynamics model. — [Jin et al., arXiv 2602.17997 (v3 Jun 2026)](https://arxiv.org/abs/2602.17997)
- [PR] Theory: "a connectome often does not substantially constrain the dynamics of recurrent networks". Recordings from a small subset of neurons can remove this degeneracy. — [Beiran & Litwin-Kumar, Nat Neurosci 2025](https://doi.org/10.1038/s41593-025-02080-4)
- [PR] A LAL model with contralateral inhibition explains locomotor statistics (search vs dispersal). — [Gattuso et al., PNAS 2025](https://doi.org/10.1073/pnas.2407626122)
- Community reimplementations of the Shiu model on other simulators exist (Brian2, Brian2CUDA, PyTorch, NEST GPU, neuromorphic hardware). — [eonsystemspbc/fly-brain (repo title only; not reviewed)](https://github.com/eonsystemspbc/fly-brain)

### Inferences
Direct implications for the project; these are my synthesis, not tested claims.

- **Input normalisation vs size scaling.**
  - In Pugliese, the input a median-sized neuron needs to reach threshold is θ/b = 7.5/0.03 ≈ 250 synapse·Hz. So 10 synapses from a DN firing at 25 Hz already reaches threshold, and DNs are driven near saturation: my estimate is about 170 Hz for a median-sized DN at Istim=250, using the published equation with a=1, rmax=200.
  - With inputs normalised to sum to 1, the same edge contributes (10/total inputs) × 25 Hz. For a neuron with about 1,000 input synapses that is 0.25 "Hz-equivalents", so the effective gain is roughly 100–1,000× lower per hop unless a matching global scale is applied.
  - Multiplying fractional weights over 2–4 hops (Cheong's metric, BANC's log influence) decays geometrically. That matches the "chain dies out" symptom.
  - The published working recipe is raw counts × a global scale, with threshold and gain scaled by neuron volume.
- **DN rates.** Both working models drive sources hard: Shiu Poisson up to 200–260 Hz, Pugliese near rmax. About 25 Hz is below both and below measured DN dynamic ranges (section 2).
- **Pruning weak edges.** Dropping connections under 5 synapses removes many weak, often inhibitory, edges that otherwise add up under normalisation.
- **Read-out.** Even in Pugliese, many muscles stay silent or non-rhythmic, and only a subset of MNs oscillate. A criterion of "any MN group moves" should target flexor, extensor and promotor/remotor pools of the legs, and check DNg100 and DNb08 first. DNa02 (a modulator of stride length, not a rhythm initiator) and MDN (whose rhythm depends on the leg CPG) are weaker tests.
- **Glutamate sign.** Both working models treat glutamate as inhibitory. The CPG's inhibitory element (IN16B036) and much leg premotor input are glutamatergic (Lesser: leg MNs get more glutamatergic premotor input). A model that treats glutamate as excitatory, or mixes signs differently, will behave differently.
- **Degeneracy.** Beiran and Litwin-Kumar imply that uniform identical units are one arbitrary point in parameter space. Heterogeneous, size-scaled parameters (as in Pugliese) or fitting to a few recordings are principled alternatives to raising global VNC gain.

### Gaps
- Pugliese's rhythmicity scores for MDN, DNa02 and the GF are in a supplementary table I could not read. Whether MDN produces backward-appropriate phasing in their model is unknown.
- Whether the Pugliese LIF variant used raw counts × 0.275 mV (implied by "same connectome weights") and how "0.15 nA" maps onto Shiu's voltage-unit LIF was not stated in the extracted text.
- No published LIF or rate simulation of the complete male CNS (brain plus VNC together) that drives MNs from DNs was found. Pugliese's male CNS runs removed brain-side synapses.
- No published model was found that combines input-fraction normalisation with spiking dynamics and still gets DN-to-MN transmission. That combination seems untested in the literature.

---

## 5. Intrinsic properties and transmitters of VNC neurons, gap junctions, neuromodulation, and sensory feedback in rhythm generation

### Takeaway
VNC neurons are not identical:
- MN input resistance spans about 150–700 MΩ.
- Slow MNs fire tonically at about 12–30 Hz at rest.
- Flight MNs have specific excitability that, with weak ShakB gap junctions, produces ordered splay firing.

Other properties that shape VNC output:
- Transmitter identity is fixed per hemilineage (ACh, GABA or Glu), and glutamate can be excitatory or inhibitory depending on the receptor.
- Gap junctions are widespread and required in the GF escape and flight circuits, but invisible to EM.
- Amines applied to the VNC induce locomotion and grooming, and flight state gates DN pathways.
- Proprioceptive feedback is tonic for position signals, presynaptically suppressed for movement signals during walking, and dominates the local input to effectors.

It shapes and stabilises rhythm, but it is not strictly required to generate within-leg rhythm.

### Cited Findings
**Transmitters**
- [PR] The adult VNC is mostly 34 hemilineages. All neurons in a hemilineage use the same fast transmitter (ACh, GABA or Glu), and no neuron uses more than one. ChAT transcripts in GABAergic and glutamatergic neurons are not translated. "Glutamate can serve as an inhibitory or excitatory neurotransmitter in the fly CNS depending on the neuronal type". — [Lacin et al., eLife 2019](https://doi.org/10.7554/eLife.43701)
- [PR] Earlier-born neurons within a hemilineage often express a different transmitter. — [Marin et al. 2024](https://doi.org/10.1101/2023.06.05.543407)
- [PR] EM transmitter prediction accuracy is 87% per synapse, 94% per neuron and 91% per known type in the brain. — [Eckstein et al., Cell 2024](https://doi.org/10.1016/j.cell.2024.03.016)
- [PR] In the VNC (MANC DNs), GABA predictions fail FISH validation often (3/9 correct). — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] Some DNs may co-release transmitters (e.g., glutamate plus tyramine; unverified). — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] BANC notes "we do not actually know the signs of all connections ... particularly concerning glutamatergic, dopaminergic, serotonergic, octopaminergic and tyraminergic synapses". — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)

**Intrinsic properties**
- [PR] Tibia flexor MNs span a gradient of anatomy, input resistance (about 150, 300 and 700 MΩ), resting potential and spontaneous rate. Slow MNs fire about 12–30 Hz at rest, while fast and intermediate MNs are silent. — [Azevedo et al. 2020](https://doi.org/10.7554/eLife.56754)
- [PR] Whether electrical synapses synchronise or desynchronise a small network depends "on the neuron-intrinsic dynamics and ion channel composition". — [Hürkey et al. 2023](https://doi.org/10.1038/s41586-023-06099-0)
- [PR] Removing shakB from VS/HS visual neurons causes spontaneous cell-autonomous voltage and calcium oscillations, so electrical synapses can be needed for a neuron's stability. — [Ammer et al., Curr Biol 2022](https://doi.org/10.1016/j.cub.2022.03.040)
- [PP] Pugliese et al. found no intrinsic bursting was needed for the leg rhythm, but "electrophysiological recordings will be required to test whether these cells exhibit nonlinear membrane properties". — [Pugliese et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)

**Gap junctions in the VNC**
- [PR] ShakB is the innexin in the escape circuit, including DLM MN1–5. Knocking it down abolishes MN coupling and synchronises firing, which disrupts the stable flight pattern. — [Hürkey et al. 2023](https://doi.org/10.1038/s41586-023-06099-0)
- [PR] Frazzled/DCC loss removes the presynaptic ShakB(N+16) gap junctions of the GF. GF-to-MN transmission then has longer latencies and lower response frequencies. — [Lopez et al., eNeuro 2025](https://doi.org/10.1523/ENEURO.0202-25.2025)
- [PR] GFC interneurons are electrically coupled to the GF. — [Azevedo et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/)
- [PR] Cheong et al. flag putative electrical synapses in MANC:
  - putative electrical interneurons, ranked by low presynaptic-site density per volume
  - wing contralateral haltere interneurons (w-cHINs) that may have electrical synapses onto wing MNs, inferred from contact area
  - DNp20 (DNOVS1), which is gap-junction coupled

  — [Cheong et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/)
- [PR] shakB is the most widely expressed neuronal innexin. — [Ammer et al. 2022](https://doi.org/10.1016/j.cub.2022.03.040)
- [PR] In the isolated larval VNC, MNs send signals back to the CPG through gap junctions (shakB in MNs, ogre in interneurons). Inhibiting MNs in A4–A6 sharply lowers fictive wave frequency, and exciting posterior MNs raises it. — [Matsunaga et al., J Neurosci 2017](https://doi.org/10.1523/JNEUROSCI.1453-16.2017)

**Neuromodulation and state**
- [PR] Applying serotonin, dopamine or octopamine to the nerve cord of decapitated flies stimulates locomotion and grooming. D2-like and D1-like dopamine antagonists cause akinesia. — [Yellman et al., PNAS 1997](https://doi.org/10.1073/pnas.94.8.4131)
- [PR] Serotonin modulates walking speed through distinct receptors. — [Howard et al., Curr Biol 2019](https://doi.org/10.1016/j.cub.2019.10.042)
- [PR] Octopamine mimics the flight-state gating of a landing DN. — [Ache et al. 2019](https://doi.org/10.1038/s41593-019-0413-4)
- [PR] MDN and DopaMeander are gated out during flight. — [Liessem et al. 2026](https://doi.org/10.1016/j.cub.2026.06.045)
- [PR] Octopaminergic DNs sit in the BANC feeding, reproduction and other clusters (e.g., DNge138, DNg104, DNg34, DNge149). — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)

**Sensory feedback and presynaptic control**
- [PR] "Most groups of effector neurons receive their strongest influence from sensors in the same body part" (W = 2,535.5, P = 3.49 × 10⁻¹⁰). Behaviour control is "distributed, parallel and embodied". — [Bates et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/)
- [PR] During behaviour, leg proprioceptor axons are treated differently:
  - Position-encoding proprioceptor axons are active across behaviours.
  - Movement-encoding proprioceptor axons are suppressed during walking and grooming, through GABAergic presynaptic inhibition from interneurons driven by excitatory and inhibitory DN pathways.

  — [Dallmann et al., Nature 2025](https://doi.org/10.1038/s41586-025-09554-2)
- [PR] Leg joint position and movement signals converge in second-order neurons, with inhibition gating the flow. — [Chen et al., Curr Biol 2021](https://doi.org/10.1016/j.cub.2021.09.035)
- [PR] A leg sensory class synapses directly onto the largest-calibre MNs on both sides. — [Phelps et al. 2021](https://doi.org/10.1016/j.cell.2020.12.013)
- [PR] Axo-axonic synapses onto DN axons within the VNC can gate DN output; AN08B098 increases GF excitability. — [Ceballos et al. 2026](https://doi.org/10.1016/j.isci.2026.115624)
- [PR] Sensory feedback "may be needed to stabilize rhythms but not necessarily to generate them in the first place". — [Ravbar et al. 2021](https://doi.org/10.7554/eLife.71508)
- [PP] Load and contact inputs shape within-leg step microstructure, and proprioception modulates interleg coupling. — [Sapkal et al. 2026](https://doi.org/10.64898/2026.04.29.721658)
- [PR] Neck MNs act through a continuing proprioceptive–motor loop. — [Gorko et al. 2024](https://doi.org/10.1038/s41586-024-07222-5)
- [PR] Haltere feedback sets wing MN spike timing. — [Dickerson et al. 2019](https://doi.org/10.1016/j.cub.2019.08.065)

### Inferences
Candidate missing ingredients for the project's male CNS LIF model, ranked by how strong the evidence is that they matter for DN-to-MN transmission:
1. **Excitability heterogeneity scaled by size.** This is shown to be necessary in the only successful VNC rhythm model (Pugliese). It is justified by measured MN input resistances of 150–700 MΩ and by synapse density scaling with area.
2. **Absolute rather than fractional synaptic drive**, plus stronger DN rates. Both successful models use raw counts × a global weight and drive sources at 100+ Hz.
3. **Tonic sensory and proprioceptive drive.** Position proprioceptors are tonically active, local sensors dominate effector input, and slow MNs fire at rest. A model with silent afferents lacks the baseline depolarisation the real VNC sits on. This is more specific than a uniform "VNC tonic drive".
4. **Gap junctions.** They are essential for the GF-to-TTMn/PSI/GFC pathway and for flight MN patterning, and invisible in EM. A GF test in a chemical-only model is expected to underperform whatever the gain.
5. **Neuromodulatory state** (octopamine, serotonin, dopamine), which enables locomotion and gates DN pathways by behavioural state.
6. **Compartmentalisation.** Presynaptic and axo-axonic inhibition acts on DN and afferent axons. A point-neuron model treats these inputs as somatic, so it can wrongly veto DN output.

Intrinsic bursting or plateau properties are not required for within-leg rhythm in current models (Pugliese). They remain untested experimentally in Drosophila premotor neurons.

### Gaps
- No quantitative estimate of VNC-wide transmitter proportions (ACh, GABA, Glu) for intrinsic neurons was extracted. The DN proportions are from Cheong, and the brain proportions from Shiu.
- No data were found on which VNC glutamatergic connections are excitatory (NMDA- or kainate-type) versus inhibitory (GluCl).
- No measurements were found of gap-junction coupling strengths in leg premotor circuits.
- No direct Drosophila evidence was found for plateau potentials or persistent inward currents in leg MNs or premotor interneurons.
