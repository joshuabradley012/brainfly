# Who is building connectome-driven flies, and how much of the behaviour is the connectome? (survey, 2026-09-26)

Scope: extends `research_notes/Embodied fly connectome simulation/embodied_integration_and_datasets.md` and `connectome_constrained_models.md`. Items already covered there (Eon's March posts, Mineault's first pass, FlyGM, the digital sphinx, Pugliese v1/v2, Wang et al. 2026 Nat Commun, Fly64, flymsg, drosophila-brain-mlx, CAOS_FlyCNS in outline, Lulzx in outline) are only updated here, not repeated.

Markers:
- **[P]** read from the primary source (paper/preprint abstract or full text, the repo README or docs, or the author's own post).
- **[S]** secondary only (press, list entry, search-engine summary).
- **[U]** could not verify; treat as a lead.
- Hobby repos are self-reported. "[P]" for a repo means that I read the README; I did not run the code.

Background dates: MaleCNS v1.0 data went public in June 2026. The Cell paper (Berg, Beckett et al., *Cell* 189, doi:10.1016/j.cell.2026.08.015) and the Google Research blog came out on **3 Sep 2026**, and that date started the viral wave [P: townie/awesome-fruit-fly; CAOS_FlyCNS README; S: 404 Media].

---

## 0. The short version

1. **The Sept 2026 wave is huge (100+ repos) and mostly decoration.** In almost every game demo, one of three things supplies the behaviour:
   - a hand-written neuron-to-button map, or
   - a trained readout (logistic, DQN, PPO, CEM, DAgger), or
   - a pre-built gait generator.

   The projects that ran a scrambled-wiring control with a *trained* readout found that the shuffled brain does as well: YYK2007/flybrain 3/3, FLM's direct-input control, and neilt93's topology-learning test.
2. **A second, smaller wave is doing brainfly-style science in public**: pre-registration, scrambled nulls, published failures. The biggest overlaps are:
   - **flybench** (Brandon Cho): 36 pre-registered reflex tasks, shuffled controls on every row, a flyvis eye and a FlyGym body.
   - **therealfly**: MaleCNS → flybody through real motor neurons with no controller. Stage 1 was pre-registered and FAILED.
   - **fly-afterlife**: MaleCNS LIF plus flyvis on true eye geometry, and a body driven through 373 leg MNs. It stands but doesn't step.
   - **CAOS_FlyCNS**: flyvis transferred onto MaleCNS wiring, with CT1 split per column and stand-in photoreceptors.
   - **AbijahKaj / closed-loop-fly**: flyvis transfer gives zero DSI on MaleCNS wiring, so the parameters were refitted.
   - **kazemi-mahdi/fly-escape-circuit** and **IONOFIELD/FLYCNS**: loom → GF → TTMn with nulls, one of them with a GF–TTMn electrical synapse.
3. **The academic side has no connectome-driven body through real motor neurons.** Nor does any published paper run loom → LC4/LPLC2 → GF → TTMn end to end from pixels. The closest are:
   - Pugliese et al. (VNC rhythm, no body)
   - FlyGM and FLYNN (RL-trained on connectome topology)
   - the digital sphinx (the negative control for the whole field)
   - Wang/Li (whole-brain LIF fitted to resting-state imaging)

   New 2026 academic items that bear on brainfly: Karaneen, Schomburg & Chklovskii on flyvis reproducibility, He on identifiability, Xi & Chen on escape suppressing feeding, and FlyMimic muscles (ICLR 2026).

---

## 1. Viral and hobby demos

### 1a. Eon Systems, update since the notes
- **New post: "More flies are getting 'uploaded' and living their best lives." (Sep 11 2026)** [P]
  - It is a perspective piece on "flyslop" (NeuroCraft Fly, DOOMFLY, Fly64, a Bad Apple video) and restates Eon's March architecture.
  - The brain is Shiu's LIF on the FlyWire central brain.
  - Motor output is "selected descending neuron activity to drive body-level controllers (but specifically not individual motor neurons)".
  - It concedes that "A connectome is an extraordinary measurement, but it is not a frozen executable brain." Interface choices are arbitrary engineering.
  - Its stated validation standard is reproducing activity and behaviour "especially for interventions it was not tuned on".
  - It reports no new embodied results, no VNC, no null control, and no code release.
  - Link: https://eon.systems/updates/more-flies-are-getting-uploaded. The update index, https://eon.systems/updates, lists only four posts.
- **Verdict (unchanged):** connectome for a few sensory→DN routes. Locomotion comes from NeuroMechFly's controllers, and vision is "decorative" by Eon's own account.

### 1b. The games (hand-written or trained readouts)

| Project | Connectome / neuron model | Neurons → actions | Trained part | Null control reported | Verdict |
|---|---|---|---|---|---|
| **Fly64 / Super Mario 64** ([ornata/fly](https://github.com/ornata/fly)) [P] | MaleCNS; uniform "fade toward zero" threshold units, 20 ms steps, tonic drive + noise; "100% vibe coded" | Hand-written: DNg100 → forward, DNa02/DNg13 L−R → steer, DNp01/DNp10 → jump | none | none (deterministic replay only) | Mineault: "random button mashing". Connectome ≈ a noise source. |
| **Beat Saber** (@_lyraaaa_, X, 8/9 Sep 2026) [S/U] | MaleCNS; Three.js; reportedly reads 130 motor neurons | Per press and later statements, the motor system was *trained to reproduce a recorded sequence*; RL for visual reactions "still being developed" | yes (imitation/RL) | none known | Memorised choreography. No repo found; X post not fetched. |
| **DOOMFLY** ([nftechie/doomfly](https://github.com/nftechie/doomfly)) [P] | MaleCNS v1.0 full graph, "approximate neural dynamics"; frames → 3,335 R1–R6 + 811 R8 proxies | Fixed: DNp20 R−L → turn, DNpe017 → move/fire ("engineered controller assignments, not established natural motor functions") | experimental dopamine rule on 4,184 KC→MBON11 synapses | Author reports its own v6 "failed its visual, conditioning and survival validation gates" | Hand map. The authors honestly report that learning didn't work. |
| **FlyDoom** ([eganeganegan/flydoom](https://github.com/eganeganegan/flydoom)) [P] | MaleCNS edge set as a sparse leaky RNN, weights init log1p(count) | DN units → PPO policy/value heads; fly-inspired feature encoder ("engineering features, not a retinal physiology model") | yes (PPO, optionally internal weights) | Framework includes Erdős–Rényi, degree-preserving rewire, MLP/GRU/LSTM; **no numbers reported** | Good design, no result yet. |
| **fly-flappy** ([ns2250225/fly-flappy](https://github.com/ns2250225/fly-flappy)) [P] | MaleCNS v1.0 at 50 Hz; game state hand-encoded into LC4/LPLC2/LC10a/velocity channels | DNp01 rule, or a trained logistic readout | yes (logistic) | none | The readout and the input encoding do the work. |
| **Flybrain gate course** ([YYK2007/flybrain](https://github.com/YYK2007/flybrain)) [P] | Full MaleCNS *rate* model (tanh), 7 game variables → R1–R6 | Logistic decoder on 64 population averages, trained by DAgger | yes | **Presynaptic-ID shuffle also completes 3/3 courses**; silenced 0; untrained 0 | Clean demonstration that the wiring is not the skill. |
| **Fly Dino** ([cobanov/flyjump](https://github.com/cobanov/flyjump)) [P] | 80-cell MaleCNS subgraph, signed leaky tanh | 243-parameter readout trained by CEM | yes | silenced 0/100; untrained 0/100; no rewire. The author states "not superiority of biological topology" | Readout learning. |
| **Flyhard** ([MarkUnthank/flyhard](https://github.com/MarkUnthank/flyhard)) [P/S] | MaleCNS (165,122 neurons); NeuroMechFly foreleg on a steering wheel, CARLA | Trained "connection strengths and neuronal dynamics" (behaviour cloning through the connectome, per Mineault) | yes | only a mechanical control (foot grip removed); no wiring null | Mineault: "no functioning visual system … memorizing trajectories". |
| **fly-garden, fly-fpv, Fly Space Program, fly-craftax, FLYT3, fly-mario, Fly-NAF, Swat, Fly Brain Minecraft, NeuroCraft Fly, DesktopFly, Help the Fly Escape** | listed in [townie/awesome-fruit-fly](https://github.com/townie/awesome-fruit-fly) and [cobanov/awesome-fly](https://github.com/cobanov/awesome-fly) [P for lists; a few READMEs read] | Mixed: DQN (fly-garden), BC+PPO (fly-fpv), learned 10-command readout (Fly Space Program: "covering the eyes → 0/80"), PPO DN readout (fly-craftax), hand-chosen readouts + scripted body programs (NeuroCraft), hand mapping with "looming drive hand-built" (Minecraft) | mostly yes | NeuroCraft reports a shuffled-weight comparison. Fly Space Program ablates the eyes. Most have none. | Game behaviour is supplied by readouts and scripts. |
| **FLM, Fly Language Model** ([nftechie/flm](https://github.com/nftechie/flm)) [P]; methods note ["Flies Are All You Need"](https://artificialscientific.com/papers/flies-are-all-you-need) [S] | MaleCNS as a frozen tanh reservoir | A 278k-parameter adapter nudges a 1.2B LLM (LFM2.5) | yes; the LLM does the language | A parameter-matched direct-input control is trained alongside. Per townie's list, the direct-input control slightly *beats* the fly graph. | Pure reservoir. The LLM does everything. Related: "Drosophila Connectome Topology Provides No Measurable Language-Model Advantage" (Research Square, Sep 2026) [S, title/metadata only]. xtensionlabs/anima-0 ("Claude … + MaleCNS as sampler, with a shuffled-wiring control") appeared in search but the repo now 404s [U]. |
| **Xenova fruit-fly-simulation** ([HF space](https://huggingface.co/spaces/Xenova/fruit-fly-simulation)) [P] | MaleCNS, Shiu-style LIF, WebGPU | Walk = stimulate LC9; turn = same-side LC9 + DNa02; fly = LC4. "Movement gains, activation thresholds, and foot trajectories are chosen for the demo". Crafted tripod + IK; "no contact, muscle, or aerodynamic simulation" | none | none | The body is animation. Many projects fork this back end. |

Other lists: [watthem/awesome-fruit-fly-connectome](https://github.com/watthem/awesome-fruit-fly-connectome) exists but was not read in full.

**Pattern.** Mineault's recommendations in [Deconstructing viral fly sims](https://www.neuroai.science/p/are-flies-playing-beat-saber) (14 Sep 2026) [P] are:
- a flyvis-style eye;
- decoding from the VNC;
- Hill muscles;
- learning only in intrinsic neurons (e.g. the mushroom body);
- an "ultrastructure-to-dynamics compiler" (Kording et al., [arXiv 2603.25713](https://arxiv.org/abs/2603.25713) [P abstract]).

Together those amount to brainfly's ladder.

### 1c. Embodied hobby flies (a body, not a game)

| Project | Brain | Body path | Controller/decoder | Nulls | Verdict |
|---|---|---|---|---|---|
| **Lulzx/fly-brain** ([repo](https://github.com/Lulzx/fly-brain); [what-the-wiring-gives](https://github.com/Lulzx/fly-brain/blob/main/docs/guide/what-the-wiring-gives.md)) [P] | MaleCNS 165,122-neuron LIF (WASM/WebGPU) + flyvis runtime | flybody (MuJoCo) | "a stepping generator fitted to real walking kinematics sits between the descending neurons and the legs". Hand-added reafference gain, escape gating, GF→TTMn electrical synapse, and slow steering adaptation (the fly "circled right" from connectome asymmetry) | none reported in the pages read | The best-documented honest boundary. Only 2/10 looms trigger escape. Octopamine made hungry flies walk *less*. Restoring the 2–3× optic-lobe gain during walking "did not bring back the giant-fibre loom response". |
| **erojasoficial-byte/fly-brain** ([repo](https://github.com/erojasoficial-byte/fly-brain)) [P]; Zenodo preprint "Emergent Individuality…" (Rojas Aliaga 2026) [S] | FlyWire v783 LIF (τ 10 ms, 0.2 ms), Hebbian plasticity on all synapses, glutamate *excitatory* | NeuroMechFly v2 | "DN→drive rates mode selection (walk/escape/groom/feed/flight)" → joint torques | two identical flies diverge (not a null) | The README claims the VNC and motor neurons are simulated, but **FlyWire v783 is brain-only, so this claim is wrong**. Behaviour-mode selector. |
| **NeuroFly** ([seven-monarchs/NeuroFly](https://github.com/seven-monarchs/NeuroFly)) [P] | Shiu LIF on FlyWire v783 | flygym `HybridTurningController` (CPG) | DN L−R asymmetry × 0.15 added to an odour steering signal ("steering is mainly guided by odour, with subtle brain modulation") | none | The connectome is a small perturbation on a hand-built odour-taxis controller. |
| **neilt93/Fly-Brain-AI ("plastic-fly")** ([repo](https://github.com/neilt93/Fly-Brain-AI); [ABSTRACT](https://github.com/neilt93/Fly-Brain-AI/blob/main/plastic-fly/ABSTRACT.md); PAPER_DRAFT.md) [P] | Shiu LIF on FlyWire v783, Brian2, 20 ms windows | FlyGym v1.2.1, PreprogrammedSteps tripod CPG; later a Pugliese-style **BANC VNC rate model (8k neurons) → 390 MNs → 42 joints** | Hand-designed decoder: 204–389 DNs → forward/turn/frequency/stance; "VNC-lite" leaky integrators | **Yes**: out-degree-preserving postsynaptic shuffle. Looming escape index 1.11 vs 0.053 shuffled; odour valence vanishes; ablation 10/10 vs 3/10 trivially. ES topology-learning test: connectome = random sparse = degree-preserving (**no topology advantage**) | Strongest hobby null work on FlyWire. Behaviour is routed by the connectome but produced by the CPG. BANC-VNC "4/6 legs anti-phase" is README-level [U]. The README wrongly calls DNg02 the giant fiber (the GF is DNp01). |
| **Fly.exe** ([Ibtisam-Mohammad/Fly.exe](https://github.com/Ibtisam-Mohammad/Fly.exe)) [P] | MaleCNS "Traced" (165,122 / 25.56M edges), 15 ms coupling | 12 NeuroMechFly bodies | Two DN population rates → a locomotion state machine; analytic vision (position + radius, no pixels); onset on a timer | identical-seed stimulus-absent control (12/12 vs 0/12 flies reach objects) | Careful ADRs, but the control is stimulus-off, not scrambled wiring; one seed. |
| **webgpu-fly** ([abgnydn/webgpu-fly](https://github.com/abgnydn/webgpu-fly)) [P] | FlyWire LIF + separate **MANC LIF** (23,188 neurons) | flybody | The 369 MNs are "averaged into six leg-group means" → walk magnitude + turn bias → "hand-written tripod CPG". An optional Vaxenburg RL policy bypasses the brain | Kenyon sparsity used as calibration (the authors call it circular) | The MANC is simulated, but the gait is hand-written. |
| **closed-loop-fly** ([ZeroXClem/closed-loop-fly](https://github.com/ZeroXClem/closed-loop-fly)) [P] | AbijahKaj optic-lobe rate model (65.8k units, refitted) → Xenova MaleCNS LIF | wing amplitude of a flight body | Steering on DNa02 because the "published DNg02 code does not lateralise in this un-refit LIF" | Phase-6 ablations. A follow-up retracts part of its own "vision matters" result as a readout artefact ("the intact loop drifts ~200° in 20 s") | Honest. Looming works end to end; steering doesn't. |
| **jamesbiederbeck/flybody-connectome** ([repo](https://github.com/jamesbiederbeck/flybody-connectome)) [P] | MaleCNS full graph | flybody wings on a wingbeat pattern generator | DNp20 R−L + DNpe017 → wingbeat frequency/steer | frozen-vision control (reproduces the live run exactly) | Measured: retinal input reaches DNp20/DNpe017 but **0 of 708 VNC motor neurons** fire; the wing pool is reachable only via haltere current. |
| **DesktopFly** ([DenisSergeevitch/desktop-fly](https://github.com/DenisSergeevitch/desktop-fly), ~1k stars) [P] | 668-neuron FlyWire LIF (LC4/LPLC2/GF/DNs) + 1,045-neuron MaleCNS locomotor extract (220 leg MNs) | a 3D desktop fly | "Simulated motor activity drives articulated joints"; brain–cord link "through a modeled interface" | 18 locomotor checks, no wiring null | A curated subcircuit toy. |
| **Haltere Pilot** ([Ameerkhanjk/haltere-pilot](https://github.com/Ameerkhanjk/haltere-pilot)) [P] | 9,235-neuron MaleCNS subgraph (≤3 hops from inputs to wing MNs) | quadrotor; **gyro → 204 haltere afferents; output read from real wing MNs** (b1, b3, i1…) | trained ("tuned gains", 93% of a teacher) | degree-preserving rewired controller; silencing 204 haltere cells crashes it vs 204 random cells | The right anatomy at both ends, but trained in between. The monosynaptic haltere→b1/b3/i1 arc is a nice structural finding. |
| **fly-cord-robots** ([SakshayMahna/fly-cord-robots](https://github.com/SakshayMahna/fly-cord-robots); [closed-loop RESULTS](https://github.com/SakshayMahna/fly-cord-robots/blob/main/docs/closed_loop/RESULTS.md)) [P] | Pugliese's VNC code, unmodified | MuJoCo hexapod/quadruped, open loop from MN data | none trained | Pre-registered closed-loop pilot: across 4 proprioceptive encoders, feedback is "either negligible or destroys the rhythm", 0/7 gain levels usable | A clean negative result on adding proprioception to Pugliese. |
| **skulitom/haltere** ([repo](https://github.com/skulitom/haltere)) [P] | 30k-neuron MaleCNS subset trained to fly an FPV drone (Liftoff) | game drone | trained + disclosed "race-cue pilot" supplies the velocity goal and yaw | brain 0/2 vs PD 1/2 finishes | Trained controller. |

### 1d. Hobby projects doing brainfly-style science (pre-registration, nulls, failures)

These are the real peers. Each has its own section in §3.

- **flybench** ([brandoncho369/flybench](https://github.com/brandoncho369/flybench); Zenodo 10.5281/zenodo.22886374; live at fly-bench.com) [P]
  - 36 pre-registered tasks on FlyWire v783 and MaleCNS. Rewired, random and sign-flip controls run on every task.
  - A flyvis front end, a FlyGym body, and a hidden hold-out set.
  - Findings:
    - The working gain is **0.45 of Shiu's** on the current synapse predictions.
    - On MaleCNS, **no gain gives both taste and vision**. Part of the reason: 13% of the male sugar neurons are called glutamatergic, which the model treats as inhibitory.
    - Spike-frequency adaptation fixes return-to-rest and wiring robustness.
    - A terminal-aware LIF (axo-axonic synapses kept off the soma) makes the mushroom body sparse.
    - flyvis → connectome loom **never reaches LPLC2/LC4/GF** (0/3), and a flash fires the GF (RFC 32).
    - On MaleCNS, a loom reaches TTMn **without the GF** through nine DN types (RFCs 34–35).
    - A closed-loop escape task through NeuroMechFly's eyes (RFC 36) is not yet passed by anyone.
- **therealfly** ([fruitflydev/therealfly](https://github.com/fruitflydev/therealfly)) [P]
  - MaleCNS LIF (Shiu) → flybody, with "no target posture, no gait table, no trained policy". Built from the motor-neuron map (708 MNs, 381 leg MNs, 86% muscle-named from MANC types) and 1,453 proprioceptors.
  - Stage 1 was pre-registered, driving DNa01+DNa02 at 150 Hz. It **FAILED**:
    - It produced a 45.5 Hz runaway, with the legs in phase.
    - The degree-preserving scramble reproduced the "11.4 Hz" peak (a harmonic).
    - 35–44% of the VNC was active.
  - Stages 2–3 were not run on that evidence. A smoke test fell over at 0.22 s.
  - The companion brain comes from `fruitflydev/flycoinrh` (a crypto-token-adjacent account, although this repo says it is "offline science only").
- **fly-afterlife** ([nsfm/fly-afterlife](https://github.com/nsfm/fly-afterlife)) [P]: MaleCNS LIF (Shiu constants) plus flyvis on a raytraced compound eye seamed onto the brain's own T4/T5. Two tracks:
  - **Brain track (readout):** walking on DNg100, halting on DNg105, optomotor from the HS L−R difference, and a hand-modelled feeding latch.
  - **Body track:** NeuroMechFly through **373 leg MNs** with sourced springs and fed-back leg senses.
    - "He stands… his legs lift, and the file at its weights does not make stance and swing."
    - Middle-leg twitches are reproduced by random spike trains.
    - A gain solver over nine labelled gains is under way.
  - A 31-row compromise ledger is kept.
- **kazemi-mahdi/fly-escape-circuit** ([repo](https://github.com/kazemi-mahdi/fly-escape-circuit)) [P]: loom → GF → TTMn on the whole MaleCNS, untrained.
- **IONOFIELD/FLYCNS** ([repo](https://github.com/IONOFIELD/FLYCNS)) [P]: 16/16 scored criteria, with a GF–TTMn electrical synapse and a feeding failure diagnosed as disinhibition (§3).
- **annel0/flybrain** ([repo](https://github.com/annel0/flybrain)) [P]:
  - A Triton GPU LIF at 2.4× real time for the full CNS on an RTX 3060.
  - It **replicates Shiu's published rates on FlyWire** (MN9 67.8 vs 68.0 Hz; median ratio 1.01, r = 0.97).
  - Degree-preserving rewiring spreads activity 8× wider and leaves APL silent.
  - It uses per-cell membrane τ (Kenyon cells >200 ms).
- **flyconnectome-nulls** ([gyujeongion/flyconnectome-nulls](https://github.com/gyujeongion/flyconnectome-nulls); Zenodo 10.5281/zenodo.22871090) [P]
  - Evolved agents on a compressed FlyWire.
  - Standard shuffles *beat* the connectome by inventing olfactory→motor shortcuts. Boundary-preserving nulls erase the gap.
  - One pre-registered prediction failed and is reported as failed.
  - Directly relevant to how brainfly builds nulls (see §4).
- **syn-ack-ai/fruit-fly-lab** ([repo](https://github.com/syn-ack-ai/fruit-fly-lab)) [P]
  - Shiu LIF on FlyWire with cited calibrations: ORN resting input, depression, a GF correction.
  - A 32-test "fly exam" with shuffled controls: published model 16/32, calibrated 32/32, shuffled 9/32.
  - The calibrations are tuned to the exam, so the hold-out claim (21/21) is self-reported.
- **NeuroTerrarium** ([5p00kyy/neuroterrarium](https://github.com/5p00kyy/neuroterrarium)) [P]: a 51-body MaleCNS GF input microcircuit. "Biological and all five rewired controls produce the same response." A negative result.
- **chris017/fly-connectome-escape-circuit** [P]: LC4/LPLC2 → GF on MaleCNS and hemibrain. Silencing 5% of either LC population collapses escape by 80–90%, which is a model artefact of threshold tuning (my inference).
- **kiatechn/sight-to-action** [P]: structural only. R1–R6 → DNg13 ranks 312/480 among DNs against weight-shuffled nulls, i.e. "a path exists" is weak evidence.

---

## 2. Academic work

| Work | What drives behaviour | Validation against real flies | Status |
|---|---|---|---|
| **Shiu et al. 2024** ([Nature](https://www.nature.com/articles/s41586-024-07763-9); [code](https://github.com/philshiu/Drosophila_brain_model)) | uniform LIF, one global weight, brain only; no body | 164 predictions, 91% consistent; optogenetic screen 10/11 | PR (in notes) |
| Follow-up: **Sapkal et al. 2024** Nature | used the Shiu model to find walk-OFF and brake halting | behaviour experiments | PR (in notes) |
| Follow-up: **Xi & Chen, "Whole-brain connectomics of Drosophila reveals a robust, distributed architecture for the suppression of feeding during escape"**, bioRxiv 10.64898/2025.12.14.694122 (16 Dec 2025) | FlyWire simulations: loom → escape "holistic state"; a redundant inhibitory ensemble suppresses feeding with additive logic | none found in the abstract | PP [P abstract via Europe PMC; full text blocked by HTTP 429] |
| Replications | annel0 (rates, r = 0.97), Eon benchmark repo, Sandia Loihi 2 | numerical parity, not biology | hobby / PP |
| **flyvis**, Lappalainen et al. 2024 ([Nature](https://www.nature.com/articles/s41586-024-07939-3); [code](https://github.com/TuragaLab/flyvis)) | graded units, 734 type-shared parameters, trained on optic flow | 26 studies; contrast polarity 30/32; T4/T5 DS | PR (in notes) |
| flyvis follow-up: **Karaneen, Schomburg & Chklovskii, "Reproducibility and model-selection stability in connectome-constrained circuit modeling"**, bioRxiv 10.64898/2026.04.18.717873 | retrains ensembles | "model clusters selected by lowest validation task error do not reliably correspond to experimentally observed neural tuning" | PP [P abstract] |
| flyvis follow-ups: **Dhiman & Panwar**, Neuroinformatics 2026 ([doi](https://link.springer.com/article/10.1007/s12021-026-09811-3)): scale stability of direction coding in flyvis checkpoints. **Dhiman**, "Dynamical Interrogation of Serpentine Medulla Circuits", bioRxiv 10.64898/2026.01.08.698345. **Zhou & Hasler**, "Representational geometry as a fidelity metric for connectome-constrained networks", bioRxiv 10.64898/2026.06.10.731214 | analyses of flyvis | model–data geometry comparisons | PR/PP [titles + partial abstracts, Europe PMC] |
| **Liew et al., "Connectome-Based Modelling Reveals Orientation Maps in the Drosophila Optic Lobe"**, NeurIPS 2025, [arXiv 2609.01330](https://arxiv.org/abs/2609.01330) | spiking model on the whole FlyWire connectome, oriented stimuli | emergent orientation maps; experimental match not checked by me | PR (conference) [S abstract] |
| **He, "How much of a nervous-system model does behaviour identify?"**, Research Square 10.21203/rs.3.rs-10856254/v1 (Sep 2026) | Fisher-style analysis. Behaviour pins down 8–47 of 3,076 parameter directions in a worm model, and **14 of 330** in a Drosophila optic-lobe model | theory | PP [P abstract]. Directly supports brainfly's "behaviour alone is weak evidence". |
| **NeuroMechFly v2 / FlyGym 2.x** ([Nature Methods 2024](https://www.nature.com/articles/s41592-024-02497-y); [flygym](https://github.com/NeLy-EPFL/flygym)) | preprogrammed CPG and hybrid controllers; flyvis in fly-following | kinematic replay | PR (in notes) |
| **FlyMimic**: Özdil et al., "Musculoskeletal simulation of limb movement biomechanics in Drosophila melanogaster", [arXiv 2509.06426](https://arxiv.org/abs/2509.06426), ICLR 2026 ([anthology](https://mlanthology.org/iclr/2026/ozdil2026iclr-musculoskeletal/)); [FlyGym muscle tutorial](https://neuromechfly.org/tutorials/6_muscle_imitation/) | 15 Hill-type muscles of the left front leg; parameters fitted by NSGA-II to 3D pose; imitation-learned muscle policies | kinematic replay of walking/grooming; predicted muscle synergies | PR (conference) [S search summary + tutorial page]. The rung-7 musculoskeletal foreleg that brainfly plans already exists here. |
| **Özdil et al. 2026**, antennal grooming, Nat Commun | connectome-derived grooming network + kinematic replay | amputation/immobilisation experiments | PR (in notes) |
| **flybody**, Vaxenburg et al. 2025 ([Nature](https://www.nature.com/articles/s41586-025-09029-4)) | deep-RL MLP controllers | imitation of real walking/flight kinematics | PR (in notes) |
| **FlyGM** ([arXiv 2602.17997](https://arxiv.org/abs/2602.17997)) | FlyWire as a fixed message-passing operator + trainable per-neuron descriptors; IL+PPO on flybody | task error only; beats rewired/ER graphs | PP (in notes) |
| **FLYNN**, Wang & Chen, [arXiv 2607.00025](https://arxiv.org/abs/2607.00025) (Jun/Jul 2026) | FlyWire as a sparse RNN trained with DAgger for vision-based robot navigation | OOD and sensory-loss robustness vs baselines; no fly data | PP [P abstract] |
| **FlyCNS**, Zhang, Lin & Lu, [arXiv 2609.28816](https://arxiv.org/html/2609.28816) (23 Sep 2026) | BANC ascending/descending spectrum as a routing prior for a *quadruped robot* (RL) | none; robotics | PP [P]. Not a fly model despite the name. |
| **The digital sphinx** (Brunton lab w/ Tuthill), bioRxiv 10.64898/2026.03.20.713233; [eLife RP](https://elifesciences.org/reviewed-preprints/111516) | worm connectome + RL-trained decoder → realistic fly walking | the field's negative control | PP (in notes) |
| **Pugliese et al.**, "Connectome simulations identify a CPG circuit for fly walking" ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.12.675944v1); [PMC v2](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); code [smpuglie/Pugliese_2026](https://github.com/smpuglie/Pugliese_2026), updated 15 Sep 2026) | rate model of the VNC (MANC/FANC/MaleCNS/BANC front-leg subnetworks); **no body** | DNb08 confirmed optogenetically; failures: tibia flexors silent, no L–R phase | PP (in notes); PubMed 42094485 suggests it is now indexed/published [S] |
| **Sapkal et al., "Central versus peripheral neural control of a coordinated walking pattern"**, bioRxiv 10.64898/2026.04.29.721658 (3 May 2026; Bidaye lab) | experiments, not a simulation | each leg has its own CPG with an intrinsic period, unmasked when proprioception is reduced | PP [P abstract]. Our notes misattribute this to Pugliese; first author is Sapkal. |
| **Dallmann … Ache, "A dedicated brain circuit controls forward walking"**, bioRxiv 10.64898/2026.01.04.697356 | connectome + physiology of a layered brain circuit recruiting forward-walking DNs | activation experiments | PP [P abstract]. A benchmark candidate for DN interfaces. |
| **Wang et al. 2026 Nat Commun** (BrainTrace) and **Li, Ping, Zhang & Wang (Chaoming), "Connectome-constrained modeling identifies neurons and synapses that sustain spontaneous activity in Drosophila"**, bioRxiv 10.64898/2026.08.21.745055 (25 Aug 2026) | FlyWire whole-brain model fitted to spontaneous calcium imaging | held-out FC; reproduces untrained features (lognormal weights, scale-free avalanches, short visual τ); a sparse inhibitory hub ensemble is necessary and sufficient for resting dynamics | PP [P abstract; full text blocked by HTTP 429]. The obvious template for brainfly's rung 4. |
| **BANC** (Bates et al., Nature 2026) | linear "influence" over brain + cord | structural | PR (in notes) |
| **Lazar et al., NeuroGraphBench**, bioRxiv 10.64898/2026.08.22.746456 | tooling for interacting with connectomes at scale | none | PP [title] |
| MANC descending-to-motor organisation, PubMed [42474298](https://pubmed.ncbi.nlm.nih.gov/42474298/) / [PMC13384506](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/) | structural: "direct DN-MN connections are infrequent" | none | PR [S] |
| **MIMIC-MJX** ([arXiv 2511.20532](https://arxiv.org/pdf/2511.20532)) | neuromechanical imitation framework | none | PP [S title only] |

**Academic bottom line.** Every academic embodied fly gets its motor behaviour from a trained policy, a pre-built CPG, or kinematic replay. The connectome-only results (Shiu, Pugliese, Wang/Li) are disembodied. No paper found drives a body from connectome motor neurons without training.

---

## 3. Direct overlaps with brainfly's next steps

### 3a. Driving a body through the real nerve cord and motor neurons
- **Academic:** nobody has done it. Pugliese stops at MN rates. FlyMimic has muscles but uses imitation-learned control. Eon explicitly does "not individual motor neurons".
- **Hobby attempts, all failing at stepping:**

| Project | Approach | Outcome |
|---|---|---|
| therealfly | MaleCNS LIF, DNa01+DNa02 drive | runaway 45 Hz in-phase oscillation; the scramble does the same |
| fly-afterlife | 373 leg MNs + springs + feedback | stands; no stance/swing |
| fly-cord-robots | Pugliese + proprioception | feedback is negligible or destructive |
| neilt93 | BANC-VNC rate model | partial anti-phase [U]. The MANC LIF gave no flex/ext alternation in 41 configurations: "uniform LIF dynamics cannot exploit the MANC's CPG wiring" |
| jamesbiederbeck | vision → MNs | 0/708 MNs fire from vision |

- **What this means for rung 5–7:** the rate-model route (Pugliese) is the only one with any rhythm, and it lacks L–R phase and flexor activity. Adding proprioception naively fails (fly-cord-robots). The unclaimed piece is **Pugliese's graded premotor recipe + size-scaled excitability + a pre-registered DNg100/DNb08 test inside a whole-CNS (brain-attached) model, then MNs → FlyGym torques with a scrambled cord null**. therealfly's protocol and metrics (M1–M4, 381 leg MNs by muscle) are reusable and worth citing.

### 3b. Loom → LC4/LPLC2 → giant fiber → TTMn, end to end
- **flybench** [P]:
  - RFC 32: flyvis loom → connectome optic cells never reaches LPLC2/LC4/GF, while a flash fires the GF at 37 Hz.
  - RFC 33: the embodied fly jumps at the flash.
  - RFCs 34–35: on MaleCNS, the loom reaches TTMn without the GF, via nine DN types.
  - The terminal-aware LIF stops flash-jumping.
  - Task 19 is a pre-registered GF→TTMn latency test (≤1.5 ms), written to fail without gap junctions.
- **kazemi-mahdi** [P]:
  - GF response ≈ the direct LC4/LPLC2 → GF projection (19.3 of 21.3 spikes).
  - A **cell-type-preserving shuffle changes nothing** (21.4 vs 21.3).
  - Spike count and timing are set by the assumed LC rate.
  - The real mismatch: the model GF *integrates* while the fly thresholds at ~39° angular size.
  - TTMn needs a GF burst, because there is no electrical synapse.
  - Ignition at ≥0.22 mV. It is mostly sustained by 120 antennal-lobe LNs labelled cholinergic.
- **IONOFIELD/FLYCNS** [P]:
  - LC amplitudes are "measured from Turner et al. 2022".
  - Scored: 1–2 GF spikes per loom, 10–60 ms latency, **1:1 TTMn relay at 0.8 ms, lost without the electrical synapse**, rewired null silent.
  - Feeding fails on MaleCNS because MN9's input is disinhibitory. A uniform tonic baseline destroys specificity and abolishes escape.
- **AbijahKaj** [P]: fitted LC4/LPLC2 give selectivity ~1.0 for approach vs recede, translate and gratings. But the LC receptive fields start 17° off midline, and looming detection depends on the background stripe.
- **Lulzx** [P]: 2/10 looms trigger escape. Self-motion looms caused wall-jumping, so escape gating was added by hand.
- **Academic anchors** (prior-knowledge, well-established):
  - von Reyn 2014; Ache 2019; Dombrovski 2023 (Nature);
  - eNeuro 2019 GF latency model ([link](https://www.eneuro.org/content/6/2/ENEURO.0423-18.2019));
  - Frazzled/DCC gap-junction latency (eNeuro 2025, [link](https://www.eneuro.org/content/12/10/ENEURO.0202-25.2025)) [S].
  - Xi & Chen 2025 (loom state suppresses feeding) is the only 2025–26 academic whole-brain loom simulation found.
- **Where brainfly differs.** brainfly's `FlyvisNative` gets LPLC2 to 28–46 Hz and GF spikes on the loomed side only, ~80 ms before contact. That is the **positive** counterpart to flybench's RFC 32 negative. The difference is methodological: flyvis on its own lattice tiled onto the male eye, versus flyvis outputs injected into connectome cells. That contrast is worth publishing with flybench.
  - Nobody has explained the LC4 weakness via **T2 polarity** (ON-only in flyvis's best model vs ON/OFF in Keleş 2020). This appears unclaimed.

### 3c. flyvis run on FlyWire/MaleCNS wiring

| Project | Approach | Result |
|---|---|---|
| **CAOS_FlyCNS** ([docs/models/04_optic_lobe.md](https://github.com/fsantibanezleal/CAOS_FlyCNS/blob/main/docs/models/04_optic_lobe.md)) [P] | flyvis parameters transferred onto MaleCNS neuron-level wiring, both eyes (879 L / 892 R columns) | T4 prefers known directions within 45° on both eyes (median error 8–11°) but DSI is weak (0.03–0.10 vs 0.17–0.59 on the lattice). **T5 mostly fails** (15/39 cases; DSI ~0.005). A per-column CT1 split restores T5 in some networks. It also found an initial ~+65° eye-rotation error, fixed via the eye model. |
| **AbijahKaj/fruit-fly-brain-research** ([repo](https://github.com/AbijahKaj/fruit-fly-brain-research); [HF](https://huggingface.co/AbijahKaj/fruit-fly-brain)) [P] | flyvis transfer, then refit per-type τ/bias and per-pair strengths (RTX 5090) | Transfer: "synapse counts agree within ~30% but give zero direction selectivity on the real per-cell wiring". Refit: DSI 0.66, tuning r = 0.96, all 16 T4/T5 × eye groups correct. |
| **fly-afterlife** [P] | flyvis seamed onto the spiking brain's T4/T5 on raytraced true eye geometry | drives optomotor steering (3/3 seeds) |
| **flybench RFC 32** [P] | flyvis output drives the connectome's own T4/T5/T2/T3/Tm/TmY cells | loom fails downstream |
| **Eon, NeuroMechFly v2, Lulzx** | flyvis as a front end | not validated on MaleCNS wiring |
| **Academic** | none found running flyvis on FlyWire or MaleCNS wiring | Karaneen/Chklovskii is relevant to *which* ensemble member to trust |

- **brainfly's two variants map onto this split.** `FlyvisOpticLobe` (a port onto MaleCNS wiring, wrong operating point) reproduces CAOS's and AbijahKaj's transfer problem. `FlyvisNative` (flyvis's own net tiled on MaleCNS columns, orientation from dendrite anatomy, all 16 T4/T5 correct) is closest to AbijahKaj's outcome, reached **without refitting**. I found nobody else doing native tiling plus a downstream LPLC2 → GF readout.

### 3d. Missing CT1 / Mi12 / R7–R8 (and R1–R6)
- **CAOS_FlyCNS** [P]:
  - "flyvis's Am, Mi3, Mi11, Mi12 and Tm28 have no counterpart by name" in MaleCNS.
  - CT1 is one giant cell per side; they split it into 3,536 per-column compartments following flyvis's model, not measured compartmentalisation.
  - **945 of 1,771 columns have no reconstructed R1–R6 terminal, 585 no R7, 450 no R8.** Stand-in photoreceptors with median synapse counts are added, so light reaches 10,768 photoreceptors, 5,895 of them real.
  - brainfly's numbers are 3,377 photoreceptors and 962/1,769 columns without R input. They agree closely.
- **brainfly's own port** (`brainfly/optic.py`) leaves out CT1 and Mi3/Mi11/Mi12/Tm28, and notes that the inhibition from CT1, Mi12 and R7/R8 goes missing.
- **fsantibanezleal/CAOS_RES_Conectoma PR #6/#7** [S, search snippet]: "R7/R8 spectral subtypes each fall below full coverage, so no input type tiled the lattice".
- **MaleCNS paper** ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/)) acknowledges "some R1-6 photoreceptors" were lost at the lamina edges (in notes). The companion visual-pathways paper ([Cell](https://www.cell.com/cell/fulltext/S0092-8674(26)00941-4); [bioRxiv 10.64898/2025.12.22.696097](https://www.biorxiv.org/content/10.64898/2025.12.22.696097v1.full)) was not read for Mi12/Mi11 synonymy.
- **[U] Gap:** whether Mi12, Mi11 or Mi3 exist under new names in Nern et al. 2025 / MaleCNS is unresolved. It is worth a direct question to FlyEM or the Reiser lab.

---

## 4. Where brainfly stands

**Genuinely novel or unclaimed (as of 2026-09-26, from what I found):**
1. **flyvis tiled natively onto the male eye's measured columns**, with the lattice orientation taken from dendrite anatomy alone, giving all 16 T4/T5 directions in both eyes with no refit, and then loom → LPLC2 (tens of Hz) → a lateralised GF firing before contact.
   - Others transfer flyvis onto MaleCNS wiring (CAOS: T5 fails), refit it (AbijahKaj), or inject its outputs (flybench: the loom fails).
   - The positive result, plus the explicit contrast with flybench RFC 32, is new.
2. **The LC4 / T2-polarity diagnosis**, and the plan to test the 10 of 50 flyvis ensemble members with ON/OFF T2. It is unclaimed, and Karaneen/Chklovskii's reproducibility paper makes the "choose by tuning, not task error" point for you.
3. **Rung 1 on MaleCNS with size-scaled synapses** (divide by target size or √size), with pre-registered specificity nulls. The runaway and the loss of specificity are *corroborated* by others, not unique:
   - flybench: no gain works for taste plus vision; 13% of sugar GRNs are glutamatergic.
   - IONOFIELD: MN9 is disinhibitory.
   - kazemi: ignition at 0.8–0.9× gain, driven by antennal-lobe LNs labelled cholinergic.
   - therealfly: 35–44% of the VNC active.
   - brainfly's own finding: the runaway sits in Kenyon cells.

   The size-scaling test itself appears unclaimed (flymsg only divides by a 1.81 density factor). The disagreement over *where* the runaway sits (Kenyon cells vs antennal-lobe LNs) is worth resolving jointly.
4. **A single laddered project where every layer has its own benchmark and null.** Pieces exist elsewhere (flybench tasks, therealfly stages, fly-afterlife ledger), but no one else builds bottom-up with a gate per layer. The novelty is the structure, not any single test.

**Where brainfly would duplicate others:**
- **Rung 1 diagnostics:** flybench, IONOFIELD and kazemi already published gain sweeps and why MaleCNS feeding fails. Cite them; don't redo them.
- **Rung 6 (GF→TTMn gap junction, 0.7–1.2 ms):** IONOFIELD implements and scores it (0.8 ms, lost without the synapse). flybench task 19 pre-registers it. Lulzx hand-adds it. brainfly can add the *shakB* slowing comparison, which I didn't see elsewhere.
- **Rungs 5–7 (the body through MNs):** therealfly, fly-afterlife, fly-cord-robots and neilt93 are all on it and failing. Reuse therealfly's MN→muscle map and metrics, and fly-cord-robots' proprioception negative result. Don't repeat DNa01+DNa02 as a walking command; therealfly shows it's a steering pair.
- **Scrambled nulls:** now common. Lessons from others:
  - Use the flyconnectome-nulls **boundary-preserving** null (a naive shuffle creates sensory→motor shortcuts).
  - Use kazemi's **cell-type-preserving** shuffle (it shows which results need only type-level wiring).
  - Apply flybench's saturation and floor rules.
  - Adopt these rather than inventing new ones.
- **The rung-7 musculoskeletal foreleg:** FlyMimic (ICLR 2026, in FlyGym) already provides it.
- **Rung 4:** Wang/Li (BrainPy group) already fit a FlyWire LIF to resting-state imaging, with held-out FC. Use their method or data.

**Who to share results with:**
- **Hobby/open (highest immediate value):**
  - **Brandon Cho / flybench**: submit brainfly as an open-division model, and send the FlyvisNative loom result as a direct counterpoint to RFC 32 (loom → LPLC2 → GF works when flyvis runs on its own lattice).
  - **fsantibanezleal / CAOS_FlyCNS**: shared photoreceptor stand-ins, CT1 split, T5 failure versus native tiling.
  - **AbijahKaj** (refit versus native).
  - **kazemi-mahdi and IONOFIELD** (GF physiology, runaway causes).
  - **fruitflydev/therealfly, nsfm/fly-afterlife, SakshayMahna/fly-cord-robots** (VNC to body).
  - **Lulzx** (the wiring-gives boundary).
  - For visibility: the list maintainers **townie/awesome-fruit-fly** and **cobanov/awesome-fly**, and **Patrick Mineault** (neuroai.science), whose recommended program is essentially brainfly's ladder.
- **Academic:**
  - **Turaga lab (Janelia)**: flyvis native tiling on MaleCNS, the T2 polarity choice.
  - **Chklovskii and co-authors**: ensemble selection.
  - **Brunton/Tuthill labs (UW)**: Pugliese VNC recipe and digital-sphinx-style nulls.
  - **Ramdya lab (EPFL)**: FlyGym body, FlyMimic muscles.
  - **Philip Shiu (Eon / Shiu model)**: the MaleCNS runaway.
  - **FlyEM / MaleCNS team and the Reiser lab**: missing photoreceptors, the Mi12/Mi11/Mi3 naming, eyemap.
  - **Card lab (Janelia)**: GF escape benchmarks such as the ~39° threshold and single-spike GF [prior knowledge; the lab association is not verified this session].
  - **Chaoming Wang group**: resting-state fitting for rung 4.

---

## Discrepancies and cautions found
- **erojasoficial-byte/fly-brain** says its FlyWire v783 model includes the VNC and motor neurons. FlyWire FAFB is brain-only.
- **neilt93** calls DNg02 the giant fiber. The GF is DNp01.
- **Our notes** attribute "Central versus peripheral neural control…" to Pugliese; the first author is Sapkal (Bidaye lab).
- **MaleCNS neuron counts vary** by filtering: 166,700 annotated; 165,122 "Traced"; 162,517 (fly-afterlife); 176,422 (Minecraft README, likely including non-neuron bodies) [U].
- **Beat Saber:** no repo found. Details come from press and townie's list [S/U].
- **bioRxiv full texts** for 2025.12.14.694122 and 2026.08.21.745055 returned HTTP 429. Only Europe PMC abstracts were read.

## URLs visited this session
- Eon: https://eon.systems/updates ; https://eon.systems/updates/more-flies-are-getting-uploaded
- Mineault: https://www.neuroai.science/p/are-flies-playing-beat-saber
- Press: https://www.404media.co/a-digital-fly-brain-has-taken-over-the-internet/
- Other pages: https://www.doriantodd.com/projects/fly-brain-bridge/ (Fly Brain Bridge: MaleCNS LIF → Sesame robot via a 485-parameter ES-trained CPG decoder; "blind fly" and "swapped eyes" controls [P]); https://huggingface.co/spaces/Xenova/fruit-fly-simulation/blob/main/README.md
- Lists: https://github.com/cobanov/awesome-fly ; https://github.com/townie/awesome-fruit-fly
- Repos (READMEs via GitHub API):
  - Games: nftechie/doomfly, eganeganegan/flydoom, MarkUnthank/flyhard, ns2250225/fly-flappy, evnsnclr/neurocraft-fly-public, ornata/fly, nftechie/flm, blendi-remade/fly-brain-minecraft, cobanov/flyjump, dzhng/fly-escape, hrook1/Swat, YYK2007/flybrain
  - Desktop and browser flies: DenisSergeevitch/desktop-fly, snedea/flybrain, Lulzx/fly-brain (+ docs/guide/what-the-wiring-gives.md)
  - Embodied flies and robots: erojasoficial-byte/fly-brain, abgnydn/webgpu-fly, seven-monarchs/NeuroFly, neilt93/Fly-Brain-AI (+ ABSTRACT.md, PAPER_DRAFT.md), Ibtisam-Mohammad/Fly.exe, jamesbiederbeck/flybody-connectome, Ameerkhanjk/haltere-pilot, skulitom/haltere
  - Optic lobe and vision: ZeroXClem/closed-loop-fly, AbijahKaj/fruit-fly-brain-research, fsantibanezleal/CAOS_FlyCNS (+ docs/models/04_optic_lobe.md)
  - Benchmarks, nulls and VNC: brandoncho369/flybench, fruitflydev/therealfly, nsfm/fly-afterlife, SakshayMahna/fly-cord-robots (+ docs/closed_loop/RESULTS.md), gyujeongion/flyconnectome-nulls, annel0/flybrain, smpuglie/Pugliese_2026 (metadata)
  - Escape circuits: kazemi-mahdi/fly-escape-circuit, IONOFIELD/FLYCNS, chris017/fly-connectome-escape-circuit, Ranuja01/fly-simulator, fruitflyworld/sim, 5p00kyy/neuroterrarium, syn-ack-ai/fruit-fly-lab
  - Structural: kiatechn/sight-to-action
- Papers/abstracts:
  - https://arxiv.org/abs/2607.00025 ; https://arxiv.org/html/2609.28816 ; https://arxiv.org/abs/2603.25713
  - Europe PMC REST search and abstract records for 10.64898/2026.08.21.745055, 10.64898/2025.12.14.694122, 10.64898/2026.01.04.697356, 10.21203/rs.3.rs-10856254/v1, 10.64898/2026.04.18.717873, 10.64898/2026.04.29.721658, 10.64898/2026.06.10.731214, 10.1007/s12021-026-09811-3, 10.64898/2026.08.22.746456
- Search-result-only (not opened): arXiv 2509.06426 and the ICLR anthology page (FlyMimic); arXiv 2609.01330 (Liew); PubMed 42474298; eNeuro GF papers; x.com posts; PC Gamer/Dexerto/IBTimes; xtensionlabs/anima-0 (404).
