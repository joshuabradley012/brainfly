# Connectome-constrained computational models of the Drosophila nervous system: state of the art, fitting, validation, failures (as of September 2026)

Status labels used below: [PR] = peer-reviewed; [PP] = preprint (bioRxiv/arXiv), not peer reviewed; [UNREV] = company blog or hobby GitHub repo, no review.

## 1. Whole-brain and whole-CNS models: Shiu et al. 2024, Fly64/ornata, and 2025-2026 models (parameters and tricks)

### Takeaway
The reference whole-brain model is still Shiu et al. 2024 [PR]. It uses identical LIF units, raw synapse counts times one global weight (W_syn = 0.275 mV), a fixed transmitter-to-sign map and zero baseline activity. 91% of its 164 testable predictions held up, but those tests sit almost entirely inside short, spiking, brain-only chemosensory and mechanosensory chains (taste to MN9, Johnston's organ to grooming DNs). Every 2025-2026 whole-brain or whole-CNS effort I found builds on that recipe or swaps it for rate or graded units: Eon Systems' embodied fly [UNREV], hobby MaleCNS ports [UNREV], Pugliese's VNC model [PP], and FlyGM and BrainTrace, which are trained. None of them validates a full photoreceptor-to-motor-neuron pathway through the VNC in a spiking whole-CNS model.

### Cited Findings
**Shiu et al. 2024 (Nature 634:210-219, doi:10.1038/s41586-024-07763-9) [PR]**
- Model: LIF in Brian2 covering all 127,400 proofread neurons of FlyWire materialization v630. Synaptic weights come from FlyWire synapse counts. Parameters: V_rest = V_reset = -52 mV, V_th = -45 mV, R_m = 10 kOhm cm2, C_m = 2 uF/cm2 (tau_m = 20 ms), refractory 2.2 ms, synaptic decay tau = 5 ms, delay 1.8 ms. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- The single free parameter is W_syn = 0.275 mV per synapse, "chosen such that activation of sugar GRNs at 100 Hz resulted in roughly 80% of maximal MN9 firing." — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Sign rule: cholinergic, dopaminergic, octopaminergic and serotonergic neurons are excitatory; GABAergic and glutamatergic neurons are inhibitory. Predicted transmitters split as ~55% ACh, 24% Glu, 14% GABA and 7% DA/OA/5-HT. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Protocol: Poisson drive to chosen sensory neurons (sugar 10-200 Hz, water 20-260 Hz, JONs 20-220 Hz), 30 trials of 1,000 ms per experiment, and "activated" defined as >0 Hz. Sugar at 10 Hz activates 45 of 127,400 neurons; at 200 Hz, 455. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Headline accuracy: "Across 164 predictions we were able to test empirically, 91% were consistent", or 84% after excluding the optogenetic split-GAL4 screen, where most lines correctly did nothing. In that screen, 10 of 11 cell types predicted to evoke proboscis extension did so, and only 4 of the 95 predicted not to showed any rostrum extension. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Confirmed novel predictions: Ir94e GRNs inhibit proboscis extension; bitter input inhibits the sugar pathway at pre-motor neurons; JO-CE, but not JO-F, activates aBN1 even though JO-F synapses directly onto aBN1. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Robustness: W_syn at +/-30% keeps accuracy at 85-88%; E/I strength at +/-50% gives 88-89%. Treating glutamate as excitatory raises the false-positive rate from 1% to 16% and erases the inhibitory bitter and Ir94e results. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Known misses: Phantom (predicted inhibitory, but actually activates MN9) and Usnea (strong phenotype, possibly neuropeptidergic; Amontillado knockdown phenocopies it). The authors note that "because the basal firing rate of all neurons in the model is 0, activation of inhibitory neurons... cannot alter the firing of downstream neurons", so disinhibition is invisible to the model. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Stated limitations: no gap junctions (not visible in EM), no non-spiking neurons, no internal state or neuropeptides, zero basal firing, and descending neurons incomplete in FlyWire, which is why the feeding circuit was chosen: its motor neurons sit inside the brain volume. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Code: github.com/philshiu/Drosophila_brain_model (FlyWire v630). Activation is Poisson spiking at a fixed rate; silencing zeroes all synapses to and from the target. — [GitHub](https://github.com/philshiu/Drosophila_brain_model)
- A companion study, Sapkal et al. 2024 Nature [PR], used the model to find two halting mechanisms: "walk-OFF" (GABAergic neurons inhibiting walking DNs in the brain) and "brake" (cholinergic neurons in the VNC). — [Nature](https://www.nature.com/articles/s41586-024-07854-7); [State of Brain Emulation Report 2025](https://arxiv.org/pdf/2510.15745)

**Fly64 / ornata/fly [UNREV]**
- The README calls it an experiment linking a fly brain model to Super Mario 64, "100% vibe coded" and "not a validated living fly". It uses MaleCNS v1.0 wiring, with "some" cell ordering "estimated". — [ornata/fly](https://github.com/ornata/fly)
- Dynamics: each cell's value "fades toward zero", then fires and resets at threshold. The network runs at 50 steps/s (20 ms steps) with one-step propagation. Eyes are six hidden 128x128 images sampled 10 times/s (~270 deg, RGB rather than UV). A "steady background drive and repeatable noise" is added. — [ornata/fly](https://github.com/ornata/fly)
- Outputs are hand-written control rules: DNg100 means forward, DNa02/DNg13 right-minus-left means steering, and DNp01/DNp10 bursts mean jump. Tested only on one M2 MacBook (16 GB). The only documented check is a deterministic replay; there are no null models. — [ornata/fly](https://github.com/ornata/fly)
- The README I could read gives no numeric LIF parameters or normalisation rule. The "inputs normalised to sum to 1" detail comes from the project brief and was not verified in the README. — [ornata/fly](https://github.com/ornata/fly)

**Eon Systems embodied fly (March 2026) [UNREV]**
- Stack: the Shiu LIF on FlyWire (~140k neurons, ~50M synapses), fed by activations from the Lappalainen visual model, driving NeuroMechFly v2 (87 joints) in MuJoCo. Descending mappings: DNa01/DNa02 for steering, oDN1 for forward velocity, MN9 for feeding, antennal DNs for grooming. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- Admitted gaps: "Many of the mappings between brain and body were chosen by hand"; walking uses NeuroMechFly controllers trained by imitation. There is no VNC. Visual inputs are "somewhat decorative" and "do not currently substantially influence behavioral outputs". There is no validation against ring attractors or CPGs, and the 15 ms sync step "may be too slow for some behaviors". — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- Eon's benchmark repo runs the same model (138,639 neurons, 15.1M connections, dt 0.1 ms) on Brian2 CPU, Brian2CUDA, PyTorch, NEST GPU, GeNN 5.4.0 and Brian2GeNN 1.7.0. Brian2 CPU is the reference. Parity metrics are Jaccard overlap of active neurons, rate correlation and spike-count ratios. — [eonsystemspbc/fly-brain](https://github.com/eonsystemspbc/fly-brain)

**Hobby whole-CNS ports of the Shiu recipe onto MaleCNS v1.0 [UNREV]**
- flymsg: MaleCNS v1.0 (165,122 traced neurons, 25.6M connections, 124M synapses). It reports that male neurons carry a median 1.81x the synapses of FlyWire counterparts across 7,327 matched types, calls this a reconstruction difference rather than biology, and divides W_syn by that density factor. Histamine is treated as inhibitory; modulators have "no fast effect". Checks: reliability, specificity against random matched neurons, dose-response, latency order, and cessation after the stimulus. Silencing tests use 1,000 matched null draws. — [flymsg](https://github.com/gianlucamazza/flymsg)
- drosophila-brain-mlx (Apple MLX/Metal): FlyWire v630 (127,400 neurons, 14,687,178 edges) and MaleCNS v1.0 (166,700 neurons, 24,469,412 edges). On MaleCNS with Shiu parameters, labellum taste input at 100 Hz drives MN9_L to 52.97 Hz (MN9_R 0.20 Hz). The VNC's share of spikes climbs from 28.6% to 66.9% over the trial, and 69 abdominal neurons exceed 100 Hz, which hints at runaway VNC activity when raw counts are used unscaled. — [drosophila-brain-mlx](https://github.com/Kisame76/drosophila-brain-mlx)
- CAOS_FlyCNS: a hybrid of graded optic lobe (flyvis ensemble parameters mapped onto MaleCNS neuron-level wiring, 879/892 columns) and spiking LIF for the central brain and VNC (W_syn 0.275). Runs in Python and in-browser WebGPU. — [CAOS_FlyCNS](https://github.com/fsantibanezleal/CAOS_FlyCNS)
- Other listed projects: FastFly (CUDA real-time target on FlyWire v783), mps-malecns-model, webgpu-fly (FlyWire + MANC + flybody in the browser) and connectome-interpreter (effective connectivity, differentiable models). — [awesome-fly](https://github.com/cobanov/awesome-fly)

**Trained or linear whole-brain models, 2024-2026**
- Wang et al. 2026, Nature Communications 17:1745 [PR]: a FlyWire LIF (>125,000 neurons, 50M synapses, Shiu parameters) trained to match whole-brain resting-state calcium imaging (Mann 2017 / Turner 2021; 68 neuropils; 17-min recordings at 1.2 Hz; 80/20 split). Only synaptic weights were trained, with signs fixed, using the online pp-prop rule. Untrained, the model "failed to reproduce any experimentally observed spontaneous fluctuations": neurons within a neuropil moved together, so cross-neuropil correlation was high. After training, nearly every region's correlation rose and FC patterns matched in both train and test data. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913608/)
- FlyGM (Jin, Zhu, Zhang, Sui; arXiv 2602.17997 v3, June 2026) [PP]: FlyWire v783 as a fixed signed message-passing operator W = N_exc - N_inh (glutamate treated as EXCITATORY), plus trainable per-neuron descriptors. Trained by imitation learning plus PPO to control flybody in MuJoCo for walking, turning and flight. — [arXiv](https://arxiv.org/html/2602.17997)
- Pospisil et al. 2024 Nature [PR]: proposes estimating the "effectome", a linear dynamical model of causal interactions, from stochastic optogenetic perturbations with the connectome as prior. Its analysis suggests whole-brain dynamics are dominated by many small, largely independent circuits. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446844/)
- BANC (Bates et al., bioRxiv 2025.07.31.667571; reported published in Nature 2026) [PP/PR]: whole-CNS "influence" is the steady state of a linear model after a sustained step into source neurons. Weights are synapse count as a fraction of the postsynaptic cell's total input; the score is unsigned, then log-transformed plus a constant. It correlates with network distance at R2 = 0.94. Main finding: "effector cells receive their strongest influence from sensors in the same body part". — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.07.31.667571v2.full); [Drugowitsch lab](https://www.drugowitschlab.org/news/202606-banc_paper/)
- Pre-connectome whole-brain models (Huang 2019 LIF; Higuchi 2022 Hodgkin-Huxley) inferred connectivity from FlyCircuit morphology for ~14-15% of neurons and had limited predictive power. — [SoBE 2025](https://arxiv.org/pdf/2510.15745)

### Inferences
- The Fly64 recipe departs from the validated Shiu recipe on four axes: (i) per-neuron input normalisation instead of raw counts times W_syn, (ii) a 20 ms step instead of 0.1 ms, (iii) tonic drive plus noise instead of zero baseline, and (iv) MaleCNS transmitter calls, where octopamine and serotonin are "unclear" (Section 5). Shiu's 91% therefore does not carry over; each change needs its own validation.
- Normalising inputs to sum to 1 is the same weighting BANC uses, but BANC uses it for an unsigned linear steady-state metric, not a thresholded spiking model. In a spiking network with identical thresholds, it caps any one presynaptic partner's effect at its input fraction. Command pathways onto very high fan-in targets (motor neurons, DNs) then become weak.
- Tonic drive is the only way to capture the disinhibition and sign-inverting pathways Shiu cannot. It also makes E/I balance and runaway control central. The mlx MaleCNS runs (69 abdominal neurons >100 Hz) and the ~1.81x MaleCNS synapse density suggest the raw Shiu W_syn is too strong for MaleCNS without rescaling.
- A pragmatic middle path: a few calibrated gain parameters per superclass or neuropil (for example optic lobe, central brain, VNC), each fitted to one known pathway the way Shiu fitted W_syn to sugar to MN9. This is more defensible than one global gain.

### Gaps
- I found no peer-reviewed spiking whole-CNS model on MaleCNS or BANC. The MaleCNS paper itself runs no simulation; it cites Shiu and Lappalainen as encouragement ([MaleCNS PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)).
- Fly64's actual parameter values were not documented in the README text I could access.
- No independent lab has re-tested Shiu's 91% biological accuracy. Replications (Eon, Sandia, mlx) check numerical parity of simulation output, not biology.
- The 1.81x density factor comes from a hobby repo and is not verified in a paper.

## 2. Circuit models built from connectomes (visual, LC/social, central complex, mushroom body, antennal lobe, escape, courtship song, locomotion)

### Takeaway
The best-validated connectome circuit models share three traits. They use graded or rate units rather than identical spiking units. They share free parameters by cell type (flyvis: 734 parameters for 45,669 neurons; ring-attractor models: 3-4 scale factors). And they are fitted to a task or a small amount of data, then tested on held-out physiology. Where exact wiring is tested, it matters for specific computations (direction selectivity, ring attractors, CPG motifs) far more than for coarse properties.

### Cited Findings
**Visual system: Lappalainen et al. 2024 Nature 634:1132 (flyvis) [PR]**
- Size: 45,669 neurons, 1,513,231 synapses, 64 cell types (65 with CT1 split) on hexagonal lattices 31 columns across. Units are "passive leaky linear non-spiking" single-compartment neurons, threshold-linear at the synapse. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Fixed from data: EM synapse counts and signs (from transmitter and receptor profiling). Free: 734 parameters (65 resting potentials, 65 time constants, 604 type-to-type unitary synapse scale factors). Trained by BPTT on optic-flow estimation from Sintel. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Ensemble of 50 models; the 10 best by task error were analysed. Compared against 26 published studies: the best model gets contrast preference right for 30/32 cell types and predicts T4 ON- and T5 OFF-motion selectivity, with untuned inputs. Of 19 types with asymmetric connectivity, only 12 are predicted motion-selective. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Task performance tracks realism: lower task error predicts better T4/T5 DSI (r = 0.60, P = 2.6e-6). Known miss: Tm4's flash response. New predictions: ON-motion tuning in TmY3, TmY4, TmY5a, TmY13 and TmY18. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Code: PyTorch, with pretrained ensembles. — [TuragaLab/flyvis](https://github.com/TuragaLab/flyvis)
- NeuroMechFly v2 (Wang-Chen et al. 2024) put flyvis into an embodied fly-following task. flybody (Vaxenburg et al. 2025 Nature) has 67 segments and 102 DoF, with RL and imitation-trained ANN controllers. — [SoBE 2025](https://arxiv.org/pdf/2510.15745); [flybody Nature](https://www.nature.com/articles/s41586-025-09029-4)

**LC neurons and social behaviour: Cowley et al. 2024 Nature [PR]**
- Design: a CNN, then a 23-unit bottleneck with one unit per LC type, then a decision network. "Knockout training" zeroes a unit whenever the data come from flies with that LC type silenced. Trained on 459 courting pairs; outputs are 3 movement and 3 song variables from 10-frame (~300 ms) inputs. — [SoBE 2025](https://arxiv.org/pdf/2510.15745); [Nature](https://www.nature.com/articles/s41586-024-07451-8)
- Trained only on behaviour, the model matched calcium imaging of 5 LC types at "35% correlation" (as paraphrased by SoBE; the exact metric is unverified). It supports a combinatorial LC population code, consistent with shared LC inputs and outputs in FlyWire. — [SoBE 2025](https://arxiv.org/pdf/2510.15745)

**Central complex and head direction**
- Kakaria & de Bivort 2017 [PR]: a spiking model of the entire protocerebral bridge produces ring-attractor dynamics (pre-EM, light-microscopy connectivity). — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5306390/)
- Turner-Evans et al. 2020 Neuron [PR]: EM reconstruction plus RNA profiling found core ring-attractor motifs and unpredicted structural features. — [Janelia](https://www.janelia.org/publication/the-neuroanatomical-ultrastructure-and-function-of-a-biological-ring-attractor)
- Noorman et al. 2024 Nat Neurosci [PR]: the fly's small head-direction network maintains an accurate, near-continuous representation with "a handful of neurons". — [Nature Neuroscience](https://www.nature.com/articles/s41593-024-01766-5)
- Biswas, Stanoev, Romani, Fitzgerald (bioRxiv 2024.11.01.621596 v2) [PP]: threshold-linear EPG-Delta7 network, with synapse counts converted to weights by 4 cell-type scale factors (3 effective). All four connectomes (MaleCNS, hemibrain, FlyWire, BANC) admit three exact ring-attractor solutions. All reproduce EPG activity but predict different Delta7 activity (8, 6 or 4 active). Scale factors restore a ring attractor even when synapse counts vary by ~90%. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.11.01.621596v2.full)

**Mushroom body and antennal lobe**
- Amin et al. 2020 eLife [PR]: APL is non-spiking and its inhibition is spatially localized. Applied to the hemibrain, this predicts that individual KCs inhibit themselves via APL more strongly than they inhibit other KCs. — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7541083/)
- Hemibrain MB scale: ~2,600 neurons with arbors in the MB, ~1,500 directly downstream of MBONs, ~3,200 upstream of MB DANs. — [Li et al. 2020 eLife](https://elifesciences.org/articles/62576)
- Lazar & Zhou 2026 [PP]: argue that antennal-lobe connectome models treat the feedforward path in isolation, while it is "embedded in dense local feedback circuits", and that connectome data alone are insufficient. — [arXiv](https://arxiv.org/abs/2608.19290)
- Therianos 2026 [PP]: in the larval connectome core (2,825 neurons), exact wiring rather than degree statistics concentrates the leading driving modes in the mushroom body. — [arXiv](https://arxiv.org/abs/2606.17745)

**Escape (looming to giant fiber)**
- Dombrovski et al. 2023 Nature [PR]: LPLC2 turns looming into escape through dorsoventral synaptic gradients at its inputs and its outputs onto the giant fiber. Dpr13/DIP-epsilon sets the LPLC2-to-GF gradient. — [Nature](https://www.nature.com/articles/s41586-022-05562-8)
- The GF circuit uses shakB gap junctions "at all nodes of the circuit, from sensory neurons to interneurons to motor neurons", for near-zero-delay transmission. A conductance-based GF model reproduces escape latency. — [PLoS One 2016](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0152211); [eNeuro 2019](https://www.eneuro.org/content/6/2/ENEURO.0423-18.2019)
- DNs, including the GF system, receive axo-axonic synapses that modulate the GF system. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13126034/)

**Courtship song**
- Lillvis et al. 2024 Curr Biol [PR]: a sine circuit (pIP10, TN1A, dMS2, vPR9) nested inside a pulse circuit (plus pMP2, dPR1, dMS9, vMS12). The 8 types are highly interconnected with each other and with wing motor neurons in MANC. This rests on connectome plus optogenetics, not a fitted dynamical model. — [Current Biology](https://www.cell.com/current-biology/fulltext/S0960-9822(24)00015-0)

**Descending control and VNC locomotion**
- Braun et al. 2024 Nature [PR]: command-like DNs recruit networks of other DNs through direct excitatory brain connections. DNs with many descending partners "require network co-activation to drive complete behaviours" and drive only simple movements alone. — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11186778/)
- Pugliese et al. 2025/2026 (bioRxiv 2025.09.12.675944 v2, Apr 2026) [PP]: rate model, not LIF, because "many neurons in the insect VNC, including premotor neurons active during walking, are nonspiking". It runs on front-leg subnetworks: MANC 4,604, FANC 803, MaleCNS 4,310 and BANC 4,963 neurons. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Of 933 excitatory DNs screened, only 29 (3.4%) produced rhythmic motor output (score >0.5); DNg100 and DNb08 scored highest. Pruning converged in 636/1024 runs to a 3-neuron core (E1 IN17A001, E2 INXXX466, I1 IN16B036) that oscillates at ~14 Hz by eigendecomposition. The DNb08 prediction was confirmed optogenetically in flies (n = 10). — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); [The Transmitter](https://www.thetransmitter.org/systems-neuroscience/long-sought-walking-circuit-found-in-fruit-flies/)
- Failures: main tibia flexor MNs stayed silent or non-rhythmic, and no consistent left-right phase emerged. The authors suggest proprioceptive feedback is required. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Larva: Zarin et al. 2019 eLife [PR] reconstructed 60 MNs and 236 premotor neurons in one segment, built a recurrent network model that reproduced forward and backward crawling, and validated selected predictions optogenetically. — [eLife](https://elifesciences.org/articles/51781v1)

### Inferences
- The models with strong physiological validation (flyvis, Pugliese, Biswas, Zarin) all use non-spiking or rate units plus a handful of cell-type parameters. Identical spiking LIF units are validated mainly for spiking sensory-to-motor chains inside the brain (Shiu).
- For the optic lobe and VNC in particular, the literature favours graded or rate dynamics, which flyvis and CAOS_FlyCNS reuse.
- Loom-to-GF and LC10a-to-DNa02 are short, heavily weighted, feedforward VPN-to-DN pathways. Reproducing them is a weak test, because even simple graph-traversal or linear models predict such strong direct pathways.

### Gaps
- I found no connectome-constrained dynamical model of the full antennal lobe or mushroom body on FlyWire or MaleCNS with quantitative validation. Only the APL model and conceptual critiques turned up.
- There is no fitted dynamical model of the song circuit.
- Found but not reviewed: CX navigation models (PFL3 steering), arXiv 2604.13411 (CX orientation), 2607.18969 (FC2 goal normalization), 2609.01330 (optic-lobe orientation maps), 2512.06934 (visual function profiles), and a 2026 Neuroinformatics flyvis follow-up ([Springer](https://link.springer.com/article/10.1007/s12021-026-09811-3)).

## 3. Fitting methods: task-optimised vs data-fitted, surrogate gradients, differentiable simulators, parameter sharing, ensembles, identifiability

### Takeaway
A connectome alone does not pin down dynamics. Theory (Beiran & Litwin-Kumar 2025) and practice (flyvis clusters; three ring-attractor solutions) show degenerate parameter families. Adding a task objective or recordings from a small subset of neurons removes much of that degeneracy. The working toolkit is: share parameters by cell type, fit by gradient descent in differentiable simulators (PyTorch flyvis, JAX/Diffrax, Jaxley, BrainPy/BrainTrace), and report ensembles rather than single fits.

### Cited Findings
- Beiran & Litwin-Kumar 2025 Nat Neurosci [PR] used a teacher-student setup: same connectome, different single-neuron parameters. "A connectome is often insufficient to constrain the dynamics of networks that perform a specific task", but "recordings from a small subset of neurons can remove this degeneracy" and predict unrecorded neurons. — [Nature Neuroscience](https://www.nature.com/articles/s41593-025-02080-4); [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.02.22.581667v1)
- Task-optimised fitting (flyvis): 734 type-shared parameters trained on optic flow alone predict held-out physiology across 26 studies. A connectome with random parameters predicts contrast preference but not direction selectivity. Lumping the 37 excitatory types into one "E-type" performs as badly as random. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Degeneracy in flyvis: T4c falls into three UMAP clusters (two direction-selective, one not) with task errors of 5.297, 5.316 and 5.357. These track opposite Mi4/Mi9 contrast tuning, so "measuring the tuning of one neuron automatically translates to constraints on other neurons". — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Ensembles over unknown biophysics (Pugliese): each of 1,024 replicates draws gain ~N(1, 0.1)/size, threshold ~N(7.5, 0.6)*size, r_max ~N(200, 10) Hz and tau ~N(20, 2) ms. There is one global synaptic scale b = 0.03 on raw counts, a floor of 5 synapses per connection, and stimulus strength auto-tuned per replicate (doubled if <5 neurons are recruited, halved if >1,500). The logic: behaviour consistent across replicates reflects wiring rather than "precise knowledge of any of the 18,416 parameters". — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Cell-type scale factors (Biswas et al.): 3 effective parameters turn raw EPG-Delta7 counts into exact ring attractors across 4 connectomes. The solutions are underdetermined by EPG data but distinguishable by Delta7 recordings. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.11.01.621596v2.full)
- Whole-brain data-fitting with online spiking gradients: Wang et al. 2026 trained all FlyWire LIF weights (signs fixed) to 68-neuropil resting-state imaging with pp-prop in ~8.9 GB of GPU memory. D-RTRL and BPTT "exceed[ed] the 32 GB capacity of a single GPU". — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913608/)
- Surrogate-gradient learning for SNNs is the standard framework reviewed by Neftci, Mostafa & Zenke. — [arXiv 1901.09948](https://arxiv.org/abs/1901.09948)
- Jaxley (Deistler et al., Nat Methods, 13 Nov 2025) [PR]: a differentiable JAX simulator for biophysical, multicompartment models on CPU, GPU and TPU. It fits voltage or two-photon recordings "sometimes orders of magnitude more efficiently" and trained a morphologically detailed network with 100,000 parameters. — [Nature Methods](https://www.nature.com/articles/s41592-025-02895-w); [GitHub](https://github.com/jaxleyverse/jaxley)
- Pugliese used JAX plus Diffrax (Dopri5, rtol 2e-6, atol 5e-9) on 4 L40S GPUs. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Task-trained graph controllers (FlyGM) keep the connectome as a fixed operator and train per-neuron descriptors plus I/O maps with IL+PPO. — [arXiv](https://arxiv.org/html/2602.17997)
- A cautionary quote from The Transmitter: "The more faithful you are to the connectome, the harder it is to train a model to be faithful to the behavior" (B. Cowley). — [The Transmitter](https://www.thetransmitter.org/connectome/connectomics-2-0-simulating-the-brain/)

### Inferences
- For MaleCNS, the natural parameterisation is per-type (11,691 types) intrinsic parameters (threshold or gain, tau, baseline) plus coarse per-superclass-pair synaptic scale factors. Per-type-pair scales, as in flyvis, would run to hundreds of thousands of parameters and need far more data.
- Hand-tuning a global tonic drive, gain and noise is Shiu-style single-point calibration. The literature suggests replacing it with (a) ensembles over plausible ranges, as Pugliese does, and (b) gradient fits to a few recorded cell types, per Beiran & Litwin-Kumar, checked on held-out types.
- Recorded LIF parameters (e.g. Shiu's) can serve as priors, but identical units cannot represent the non-spiking lamina and VNC premotor neurons (Sections 4-5).

### Gaps
- I found no published MaleCNS-scale fit of per-type parameters to neural data.
- No study measures how many recorded cell types are needed to identify a whole-brain model; Beiran & Litwin-Kumar give theory and small networks.
- BrainPy/BrainTrace code availability and runtime per epoch were not verified.

## 4. Validation practice: imaging and ephys comparisons, optogenetic predictions, held-out types, null models, and how much exact wiring matters

### Takeaway
Validation practice spans four kinds of test:
- matching published tuning (flyvis, 26 studies);
- predicting optogenetic sufficiency and necessity (Shiu, 164 predictions; Pugliese, DNb08);
- fitting and holding out imaging data (BrainTrace 80/20);
- structural nulls.

Null-model results diverge. Weight shuffles and degree-preserving rewiring abolish specific routes (sugar to MN9). Degree-and-weight-matched ensembles reproduce gross gain and dimensionality within a few percent. So a model that "works" on gross activity can equally work on a scrambled connectome, which matches the project's observation.

### Cited Findings
- Shiu's null was a weight shuffle ("shuffled randomly while maintaining the global connectivity weight distribution"). Sugar at 100 Hz activated MN9 in 100% of real-connectome runs and in 1 of 100 shuffles. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Degree-preserving shuffle (each neuron keeps in/out counts and synapse signs and sizes, with random targets) on FlyWire v630: MN9 fired at 67.30 Hz on real wiring and fell silent in 5/5 shuffle seeds. The number of active neurons was similar (96 real vs 89-99 shuffled), so "it is the wiring, not the degrees or the signs, that carries the sugar signal to MN9". — [drosophila-brain-mlx](https://github.com/Kisame76/drosophila-brain-mlx) [UNREV]
- Degree-and-weight-matched rewiring (larval core, frozen leaky-tanh operator, no fitted parameters): gain and effective dimensionality fall "within a few percent of the ensemble". Exact wiring confines activity to about a fifth of the core, against two thirds for rewired networks, and concentrates the leading driving modes in the mushroom body. "Gross operator behavior is... largely a property of its degree and weight statistics, while the routing of input... [is] written into its exact wiring." — [Therianos arXiv](https://arxiv.org/abs/2606.17745) [PP]
- FlyGM (task-trained) mean angle error: FlyGM 4.96/5.57/6.36/8.29 deg (easy to hard) vs MLP 6.76/7.18/8.85/13.90. Degree-preserving rewiring reaches 13.55 at high yaw and Erdős-Rényi 125.36. Caveat: the non-connectome graphs used unweighted edges, while unweighted FlyGM scored 11.00 at high yaw. — [arXiv](https://arxiv.org/html/2602.17997) [PP]
- Motif-level null (Pugliese): 21,544 instances of the CPG motif in the MANC front-leg network vs 307 +/- 29 in weight-matrix shuffles. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Ablation-style nulls (flyvis): random parameters, cell-type-only connectivity, and signs without counts. Random-parameter models keep contrast preference but lose direction selectivity. — [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
- Functional connectivity: the connectome predicts resting-state FC between regions in Drosophila. Some regions follow direct connections closely; others, including the MB, depend more on indirect paths. — [Turner, Mann, Clandinin 2021](https://www.cell.com/current-biology/fulltext/S0960-9822(21)00343-2)
- Imaging fit: an untrained FlyWire LIF misses resting-state dynamics entirely, and training restores region-level and FC agreement on held-out data. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913608/)
- Pre-registered multi-criterion checks in hobby ports: reliability, specificity against matched random neurons, dose-response, latency order, and cessation after the stimulus. — [flymsg](https://github.com/gianlucamazza/flymsg) [UNREV]
- Cross-simulator parity (Eon, Sandia, mlx): Jaccard overlap of active sets, per-neuron rate correlation, spike-time matching. — [eonsystemspbc/fly-brain](https://github.com/eonsystemspbc/fly-brain); [Loihi 2 paper](https://arxiv.org/abs/2508.16792); [drosophila-brain-mlx](https://github.com/Kisame76/drosophila-brain-mlx)
- Expert caution: "Similar connectivity does not allow you to predict similarities in function" (Clandinin and Currier, quoted in The Transmitter). — [The Transmitter](https://www.thetransmitter.org/connectome/connectomics-2-0-simulating-the-brain/)

### Inferences
- A degree-preserving scramble "performing as well" is expected if the test metric is gross: total activity, whether any DN fires, or rates driven by uniform tonic drive. With inputs normalised to sum to 1, every neuron's total input weight is identical under any rewiring that keeps signs, so steady-state excitability barely changes.
- Discriminating tests must score routing and specificity: the correct side (ipsi vs contra), the correct target among matched decoys, dose-response, latency order, and sugar to MN9, which fails under a DP shuffle.
- A tiered benchmark from the literature:
  - Shiu's 164 predictions (Supplementary Table 9);
  - Sapkal halting, split into brain walk-OFF and VNC brake;
  - Braun DN co-recruitment;
  - Pugliese: DNg100 and DNb08 rhythmic output (and their failures);
  - flyvis's 26 physiology datasets (T4/T5 DS, ON/OFF polarity);
  - resting-state FC (Mann/Turner, 68 neuropils);
  - Cowley's LC-silencing behaviour;
  - Dombrovski LPLC2-to-GF lateral gradients;
  - null ladder: weight shuffle, then DP rewire, then degree-and-weight-matched, then cell-class-preserving.

### Gaps
- No published Drosophila whole-brain spiking model reports the full null ladder. The DP-shuffle MN9 result comes from an unreviewed repo; Therianos is a single-author larval preprint.
- No study directly measured how much gross vs specific behaviour a DP shuffle preserves in MaleCNS.

## 5. Known failure modes and criticisms of connectome-only models (signs, gap junctions, neuromodulation, count vs strength, non-spiking neurons, incompleteness)

### Takeaway
The recurring failure sources:
- wrong or unknown signs (glutamate, histamine, modulators, "unclear" calls);
- invisible electrical synapses and neuropeptides;
- non-spiking graded neurons forced into spiking units;
- zero-baseline models that cannot express disinhibition or sign inversion;
- incomplete reconstruction at the periphery (lamina photoreceptors, some sensory and motor neurons; only 40.1% of MaleCNS connections have both partners proofread);
- missing proprioceptive feedback and DN co-activation in motor control.

These map directly onto the project's lamina and VNC failures.

### Cited Findings
- The Bargmann & Marder critique (restated 2025): connectomes lack transmitter identity, electrical synapses and weights. "In the absence of knowing who's electrically coupled to who... [models] are going to be missing a lot of parallel pathways" (Marder). Otopalik adds missing plasticity. — [The Transmitter](https://www.thetransmitter.org/connectome/connectomics-2-0-simulating-the-brain/)
- Electrical synapses are absent from all published Drosophila connectomes because they are ~10-20 nm, below EM resolution. This wording came from a search-result summary tied to this paper and was not checked against its full text. — [Curr Biol 2022, electrical synapses in Drosophila](https://www.sciencedirect.com/science/article/pii/S0960982222004353)
- Transmitter prediction accuracy (FlyWire, 6 classes): 87% per synapse, 94% per neuron, 91% for known cell types. Per class for FAFB known types: ACh 91%, Glu 91%, GABA 96%, DA 90%, OA 85%. — [Eckstein et al. 2024 PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11106717/)
- MaleCNS transmitters come from a 7-class ResNet50 classifier trained on literature ground truth covering 10 transmitters (incl. histamine, glycine, NO, tyramine).
  - "all octopamine and serotonin results are set to unclear in consensusNt".
  - Neurons with <50 presynaptic sites, or confidence <0.5, get predictedNt "unclear".
  - Cell types with <100 pooled presynapses, or confidence <0.5, get celltypePredictedNt "unclear".
  - Source: [MaleCNS PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
- Glutamate's sign is assumption-dependent. Shiu (inhibitory) and FlyGM (excitatory) disagree, and flipping it in Shiu raises false positives from 1% to 16%. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/); [FlyGM](https://arxiv.org/html/2602.17997)
- The photoreceptor-to-LMC synapse is sign-inverting: histamine gates chloride channels, so L1-L3 hyperpolarise to light increments and depolarise to decrements. — [Curr Biol 2024](https://www.cell.com/current-biology/fulltext/S0960-9822(24)01631-2); [J Neurosci 2008](https://www.jneurosci.org/content/28/29/7250)
- MaleCNS reconstruction gaps: "some R1-6 photoreceptors neurons in the laminae" were lost to edge artefacts, and "some sensory and motor neurons" to segmentation issues. Pre- and postsynaptic completeness are 94% and 42%; connection completeness is 40.1%. — [MaleCNS PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)
- Non-spiking neurons: VNC walking premotor neurons are often nonspiking, hence Pugliese's rate model. flyvis models all optic-lobe neurons as non-spiking. APL is non-spiking. — [Pugliese PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); [flyvis PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/); [Amin 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7541083/)
- Point-neuron assumption: in antennal-lobe PNs, spikes start in the proximal axon, and input to a single dendritic branch "propagates poorly to the rest of the cell". — [Gouwens & Wilson 2009](https://www.jneurosci.org/content/29/19/6239)
- Neuropeptides: Shiu's Usnea miss is consistent with neuropeptide signalling. In C. elegans, measured signal propagation across 23,427 neuron pairs "differs from predictions based on anatomy", partly through extrasynaptic neuropeptide signalling on sub-second timescales. — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/); [Randi et al. 2023 Nature](https://www.nature.com/articles/s41586-023-06683-4)
- Count vs strength: in larval EM, summed synaptic contact area is accurately predicted by synapse count across transmitters. The caveats: some partners make few large contacts and others many small ones, and molecular or biophysical properties can break count-based weights. — [PLoS One 2022](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0266064)
- Motor-control gaps: DNs often need co-activated DN networks for complete behaviour. VNC CPG models lack proprioceptive feedback, leaving tibia flexor MNs silent and legs uncoordinated. Effectors are most influenced by local same-body-part sensors. — [Braun 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11186778/); [Pugliese PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); [BANC bioRxiv](https://www.biorxiv.org/content/10.1101/2025.07.31.667571v2.full)
- Metabolic ceiling: a rough ATP budget (~160 pmol O2/min, ~9e6 ATP per spike) caps mean firing across ~140k neurons at about 4 Hz, and likely lower. — [SoBE 2025](https://arxiv.org/pdf/2510.15745)

### Inferences
Mapping onto the project's three failures (inference, not tested):
- **Photoreceptor signal dies at the lamina.** Several causes compound. R1-6 to L1-L3 is a sign-inverting histaminergic synapse, so it carries information as hyperpolarisation of graded, non-spiking LMCs. A zero or low-baseline LIF lamina therefore cannot pass it on, just as Shiu's model cannot express disinhibition. On top of that, some R1-6 are missing from MaleCNS. Fixes used by others: swap the optic lobe for a graded flyvis-style model (CAOS_FlyCNS, Eon), or give LMCs a tonic baseline and rectified graded output so light decrements depolarise them (OFF) and sign flips again downstream (ON).
- **DN commands die before reaching MNs.** Likely causes:
  - 1/fan-in dilution from sum-to-1 normalisation on high-fan-in premotor neurons and MNs;
  - a missing requirement for co-activating DN networks (Braun);
  - VNC rhythm generation that relies on specific E/I motifs in non-spiking units (Pugliese needed rate units, auto-tuned stimuli and ensembles, and still only 3.4% of DNs worked);
  - glutamatergic premotor neurons treated as inhibitory;
  - missing gap junctions (GF to motor neurons);
  - partly reconstructed MNs;
  - no proprioceptive loop.

  A 20 ms step with per-step decay toward zero probably also loses signal at each of the several hops between DN and MN.
- **Degree-preserving scramble matches the real connectome.** See Section 4. Normalised inputs plus tonic drive make gross activity degree-determined. Specificity metrics (sugar to MN9-type tests, lateralised loom to DNp01) should separate real from scrambled wiring.

### Gaps
- I could not confirm which 7 classes the MaleCNS classifier outputs (whether histamine and glycine are direct classes) or how photoreceptors are labelled in consensusNt.
- There is no direct adult-fly evidence on how well synapse count predicts measured unitary strength across many connections.
- There is no quantitative estimate of how many VNC neurons are non-spiking.

## 6. Compute: full-connectome simulation on CPU, GPU and neuromorphic hardware; real-time feasibility

### Takeaway
A whole-brain or whole-CNS LIF at the fly's scale is cheap. Optimised GPU or Apple-Silicon code runs FlyWire faster than real time (0.29 s per biological second on an M4 Pro) and MaleCNS near real time (1.17 s per biological second). Loihi 2 beats real time only when activity is sparse. The bottleneck is gradient-based fitting (memory), not forward simulation. Embodied loops currently use coarse 15-20 ms sync steps, which the authors themselves flag as too slow for fast behaviours like escape.

### Cited Findings
- Shiu et al.: Brian2 takes "approximately 5 min per 1,000 ms trial per CPU thread" (sugar activation). — [Shiu et al. PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)
- Loihi 2 (Sandia; Wang, Theilman, Rothganger, Severa, Vineyard, Aimone; arXiv 2508.16792) [PP]
  - Model: the Shiu model on FlyWire (140K neurons; 50M synapses condensed to ~15M connections), v_th 7 mV above rest.
  - Hardware mapping: weights ranging -2405 to 1897 are quantised to 9-bit and capped at 255/-256. Max fan-in is 10,356 and fan-out 9,783. With shared-axon routing, the unmodified connectome fits on 12 chips (1,440 neurocores); an earlier scheme needed 20 chips.
  - Source: [arXiv](https://arxiv.org/abs/2508.16792)
- Loihi 2 wall time per 1 s simulated:

  | Platform | Sugar experiment | Background 0.5 Hz | Background 40 Hz |
  |---|---|---|---|
  | Brian2 | 4.42 s | 10.13 s | 13.99 s |
  | Loihi 2, 0.1 ms steps | 53.8 ms | 0.189 s | 5.79 s |
  | Loihi 2, 1 ms steps | 12.4 ms | 0.096 s | 4.80 s |

  - The speedup over Brian2 is "~3x-~350x", and Loihi beats real time only at low activity.
  - In the sugar run, a few hundred neurons fire at ~30 Hz while the network-wide average is ~0.1 Hz.
  - Source: [arXiv](https://arxiv.org/abs/2508.16792)
- Apple Silicon (M4 Pro, 24 GB), MLX port [UNREV]: FlyWire v630 at 0.29 s per biological second (fused kernel) vs 2.07 s for Brian2-cython; MaleCNS v1.0 at 1.17 s per biological second. The float32 run differs from a float64 Brian2 oracle by ≤1 spike in 2,973. — [drosophila-brain-mlx](https://github.com/Kisame76/drosophila-brain-mlx)
- Eon benchmark suite: six backends at dt = 0.1 ms on 138,639 neurons and 15.1M connections. The speed numbers sit in downloadable result files, not the README. — [eonsystemspbc/fly-brain](https://github.com/eonsystemspbc/fly-brain)
- Rate-model ensembles (Pugliese): 1,024 replicates of ~4-5k-neuron VNC subnetworks in ~18 min on 4 L40S GPUs (JAX/Diffrax). — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Training at whole-brain scale: pp-prop needs ~8.9 GB of GPU memory, while BPTT and D-RTRL exceed 32 GB. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913608/)
- FlyGM training ran on NVIDIA A100 80 GB GPUs, with longer per-step compute and more memory than an MLP. — [arXiv](https://arxiv.org/html/2602.17997)
- Embodiment timing: Eon syncs brain and body every 15 ms, which "may be too slow for some behaviors". Fly64 runs 50 steps/s with vision at 10 Hz. — [Eon](https://eon.systems/updates/embodied-brain-emulation); [ornata/fly](https://github.com/ornata/fly)

### Inferences
- At 166.7k neurons and 25.6M edges, a 0.1 ms event-driven or sparse LIF should run near real time on a single modern GPU or Apple-Silicon machine, judging by the MLX MaleCNS figure. There is no compute reason to keep a 20 ms step, which erases the 1.8 ms delays and 2.2 ms refractory periods central to the Shiu parameterisation.
- Hybrid graded optic lobe plus spiking central brain (CAOS_FlyCNS) and rate-model VNC ensembles add modest cost. Gradient fitting of per-type parameters is feasible with online or truncated methods on one 24-80 GB GPU.
- Speed depends strongly on activity on neuromorphic hardware (Loihi). Tonic drive that raises mean rates toward the ~4 Hz metabolic ceiling would cut neuromorphic speedups.

### Gaps
- I found no peer-reviewed benchmark of GPU runtimes for full-CNS (MaleCNS or BANC) models. The Eon numbers were not extractable from the README.
- Runtime claims for webgpu-fly and FastFly are unverified.
- The reported Brian2 timings conflict: ~5 min per 1 s trial per thread (Shiu), 4.42 s (Sandia) and 2.07 s (mlx). The differences likely reflect code-generation target, threading and hardware, but none of the sources state this.
