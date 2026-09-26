# Embodied connectome simulation of the fruit fly: prior efforts, lessons from other animals, and layer-by-layer validation data

*Status as of 2026-09-25. "Preprint" means not peer reviewed. "PR" means a peer-reviewed paper. A few items tagged "(prior-knowledge citation, not re-fetched)" are standard references whose DOIs were not re-opened this session.*

## Q1. Embodied fly efforts: Eon Systems, NeuroMechFly/flygym integrations, and other whole-fly or digital-twin projects (to Sept 2026)

### Takeaway
No one has yet shown a connectome-driven fly body whose behaviour or internal dynamics are quantitatively validated against real flies.

- **Eon Systems (March 2026).** Eon joined three existing published pieces:
  - the Shiu et al. FlyWire LIF brain
  - the NeuroMechFly v2 body
  - the flyvis optic-lobe model

  A few hand-picked descending neurons (DNs) drive NeuroMechFly's pre-built locomotion controllers. Eon itself calls vision "somewhat decorative".
- **Academic work** has produced three key pieces:
  - the body platforms (NeuroMechFly/FlyGym 2.x; flybody)
  - a connectome-constrained optic lobe (flyvis)
  - VNC connectome simulations that produce walking rhythms (Pugliese et al. 2025, preprint)
- **Two 2026 results show that behavioural realism alone is weak evidence.** An RL-trained whole-connectome controller (FlyGM) walks and flies, learning faster than rewired or random graphs. But a *worm* connectome driving a fly body ("digital sphinx") also produces realistic fly walking.

### Cited Findings

#### Eon Systems: what was built, and what it claims
- **Three posts in four days.** "The First Multi-Behavior Brain Upload" (7 Mar 2026), "We've Uploaded a Fruit Fly" (8 Mar 2026), and the technical write-up "How the Eon Team Produced a Virtual Embodied Fly" (10 Mar 2026). — [Eon, 7 Mar](https://eon.systems/updates/first-multi-behavior-brain-upload); [Eon, 8 Mar](https://eon.systems/updates/weve-uploaded-a-fruit-fly); [Eon, 10 Mar](https://eon.systems/updates/embodied-brain-emulation)
- **Team.** The technical post names Scott Harris, Aarav Sinha, Viktor Toth, Alexis Pomares and Philip Shiu, with Alex Wissner-Gross as co-founder and founding advisor. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
  - CEO is Michael Andregg. — [Untapped Ventures](https://untappedventures.substack.com/p/untapped-ventures-invests-in-eon)
  - The 8 Mar post describes "a small team in San Francisco" with advisors David Eagleman and Robin Hanson. — [Eon](https://eon.systems/updates/weve-uploaded-a-fruit-fly)
  - Philip Shiu is "Head of Engineering, Eon Systems". — [The Transmitter](https://www.thetransmitter.org/systems-neuroscience/digital-sphinx-raises-questions-about-connectome-models/)
- **Brain.** "A leaky integrate-and-fire (LIF) model built from the adult Drosophila central-brain connectome, with approximately 140,000 neurons and roughly 50 million synaptic connections" (Shiu et al.). Synapse sign comes from inferred neurotransmitter identity. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Body.** NeuroMechFly, with "87 independent joints embodied in a precise 3D mesh … from an X-ray microtomography scan", running in MuJoCo. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Vision (relevant to this project's retina shortcut).** Eon integrated the Lappalainen et al. model, "a connectome-constrained recurrent network for 64 visual cell types, spanning tens of thousands of neurons". It "pipes in" predicted visual-neuron activity directly into the LIF brain rather than simulating the retina. Eon says these inputs are "somewhat 'decorative' in that they do not currently substantially influence our behavioral outputs". — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Demonstrated behaviours:**
  - antennal grooming ("virtual dust" activating Johnston's organ mechanosensory neurons)
  - sugar-triggered feeding (gustatory receptor neurons)
  - taste-guided foraging
  - walking and turning through a few DNs: oDN1 for forward velocity, DNa01/DNa02 for steering

  Looming escape was validated only in the disembodied model and was not implemented in the body. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Eon's own caveats (10 Mar post):**
  - "Our current descending-neuron interface is quite sparse" (a handful of DNs out of ~1,000).
  - Brain-to-body mappings were "chosen by hand rather than derived from the connectome".
  - "We have not yet validated the model's internal dynamics against known biological signatures, such as the head-direction ring attractor or central pattern generators."
  - "Internal state, plasticity, learning, hormonal changes are largely missing."
  - Results "should not yet be interpreted as a proof that structure alone is sufficient".
  - No quantitative comparison of walking speed, turning or foraging against real flies is reported.

  — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Eon's framing.** "We don't think it is the first fly upload. That, in our view, was the unembodied brain model of Shiu et al. … We do think it is the first embodied fly upload, the first to close a sensorimotor loop in a simulated body." — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Inconsistent accuracy figures across Eon's own posts.** Neither figure measures embodied behaviour.
  - 7 Mar post: "motor behavior at 95% accuracy" (attributed to the 2024 computational model). — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload)
  - 8 Mar post: "91% behavior accuracy" from four ingredients (graph, synapse-count weights, E/I class, LIF). — [Eon](https://eon.systems/updates/weve-uploaded-a-fruit-fly)
  - The primary paper: "Across 164 predictions … 91% were consistent" with experiments. These were disembodied activation predictions (e.g. which neurons respond to sugar or water gustatory neurons, which drive motor neuron firing). — [Shiu et al., Nature 2024, doi:10.1038/s41586-024-07763-9](https://www.nature.com/articles/s41586-024-07763-9); [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11446845/)
  - Press repeated "95 percent accuracy" as if it measured the embodied fly. — [Futurism](https://futurism.com/science-energy/research-fly-brain-matrix)
- **Inconsistent descriptions of hand-tuning.**
  - 7 Mar post: behaviours are "driven by the emulated brain's own circuit dynamics". — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload)
  - A secondary site repeats "no hand-tuning, no additional learning algorithms". — [nexi.fund](https://nexi.fund/whole-brain-emulation-eon-2026/)
  - Both are contradicted by Eon's own 10 Mar statement that mappings were chosen by hand. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- **Inconsistent neuron counts.** These probably reflect FlyWire v630 versus v783 snapshots.
  - "more than 125,000 neurons and 50 million synaptic connections" (7 Mar). — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload)
  - "~140,000" (10 Mar). — [Eon](https://eon.systems/updates/embodied-brain-emulation)
  - 139,255 (secondary). — [nexi.fund](https://nexi.fund/whole-brain-emulation-eon-2026/)
  - The Shiu model used 127,400 proofread neurons and 50M+ synapses. — [search summary of Shiu et al.](https://pubmed.ncbi.nlm.nih.gov/39358519/)
- **Why motor neurons are missing.** Eon: "Motor neurons couldn't be traced since the body wasn't scanned". FlyWire FAFB is brain-only. No plasticity rules are included. — [Eon](https://eon.systems/updates/weve-uploaded-a-fruit-fly)
- **What is public.** No embodied-fly code is released. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
  - Eon's GitHub `eonsystemspbc/fly-brain` contains only the disembodied whole-brain LIF: FlyWire v783, with v630 archived for the paper figures.
  - Backends: Brian2, Brian2CUDA, PyTorch, NEST GPU, GeNN/PyGeNN, Brian2GeNN.
  - Licence: GPL-2.0-or-later, with the Shiu et al. code under MIT. About 917 stars.
  - Its README says "~138k neurons, ~5M synapses". The 5M conflicts with the ~50M synapses quoted elsewhere; it is possibly a count of connections or a typo. — [GitHub](https://github.com/eonsystemspbc/fly-brain)
  - The original Shiu et al. research code is at [philshiu/Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model). — [awesome-fly list](https://github.com/cobanov/awesome-fly)
- **Roadmap.** The next target is "a complete digital emulation of a mouse brain", roughly 70 million neurons. — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload)
  - Secondary sources add "within two years" and describe expansion-microscopy connectomics plus tens of thousands of hours of calcium and voltage imaging. — [nexi.fund](https://nexi.fund/whole-brain-emulation-eon-2026/)
  - Investor: Untapped Ventures; amount not disclosed. — [Untapped Ventures](https://untappedventures.substack.com/p/untapped-ventures-invests-in-eon)
  - Home page slogan: "Upload the Human Mind". — [Eon](https://eon.systems/)

#### Independent assessments of Eon and the 2026 wave of viral fly simulations
- **Ariel Zeleznikow-Johnston, "No, we haven't uploaded a fly yet" (19 Mar 2026).**
  - The brain only "activates a few descending neurons – oDN1 for forward velocity, DNa01/DNa02 for steering – and hands that signal off to a locomotion controller".
  - Leg coordination comes from NeuroMechFly's pre-built controllers.
  - The ~15,000-neuron ventral nerve cord is not simulated.
  - His standard for an upload: it should "do everything the original fly could do … responding to novel situations as the original would have".

  — [LessWrong](https://www.lesswrong.com/posts/ybwcxBRrsKavJB9Wz/no-we-haven-t-uploaded-a-fly-yet)
- **Neuroscientist response.** Neuroscientists accused Eon of misrepresentation after the "We've uploaded a fruit fly" framing. This comes from a search-engine summary of the coverage; no named critic was confirmed. — [Ojha substack (commentary)](https://saanyaojha.substack.com/p/sci-fi-fruit-flies-in-the-hypegiest); [Futurism](https://futurism.com/science-energy/research-fly-brain-matrix)
  - Philip Shiu later told The Transmitter: "This is not a full blown copy of a fly … maybe we ought to call this a digital twin or an embodied model." — [The Transmitter, 2 Apr 2026](https://www.thetransmitter.org/systems-neuroscience/digital-sphinx-raises-questions-about-connectome-models/)
- **Patrick Mineault, "Deconstructing viral fly sims" (14 Sep 2026).** He reviewed Eon, a Beat Saber demo, Fly64 (Super Mario 64) and Doom demos.
  - "Most of the demos for which I've been able to find the source for are not 'real': they don't demonstrate a full loop from sensation to motor output."
  - He calls the Super Mario 64 demo "random button mashing in a video game environment". This matters here because this project adapted Fly64's neuron model.
  - Flexible decoders trained on top of the connectome make the connectome "beside the point".
  - His recommendations:
    - flyvis-style visual front ends
    - decoding motor output from the VNC rather than from central neurons
    - confining learning to the mushroom body or intrinsic neurons
    - testing learned maze navigation

  — [neuroai.science](https://www.neuroai.science/p/are-flies-playing-beat-saber)

#### Body platforms and connectome integrations
- **NeuroMechFly v1** (Lobato-Rios et al., Nature Methods 19:620–627, 2022; PR). An open-source biomechanical model from micro-CT. Kinematic replay of tethered walking predicts unmeasured torques and contact forces. — [Nature Methods](https://www.nature.com/articles/s41592-022-01466-7)
- **NeuroMechFly v2** (Wang-Chen et al., Nature Methods 21:2353–2362, 2024; PR).
  - Adds vision (compound eyes), olfaction, leg adhesion, rugged terrain and hierarchical brain–VNC control.
  - Includes a fly-following task that interfaces the Lappalainen connectome-constrained visual network with NeuroMechFly. It uses T1–T5, all Tm and all TmY activities as inputs for object detection.
  - This is an embodied connectome sub-model predating Eon.

  — [Nature Methods](https://www.nature.com/articles/s41592-024-02497-y); [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.09.18.556649.full.pdf); [EPFL postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- **FlyGym 2.x** (March 2026) is a complete, non-backward-compatible rewrite.
  - About 10× faster on CPU (~2× real time) and about 300× faster on GPU via Warp/MJWarp (~60× real time).
  - Apache-2.0. The 1.x API moved to `flygym-gymnasium`.

  — [GitHub](https://github.com/NeLy-EPFL/flygym)
- **flyvis** (Lappalainen et al., Nature, 11 Sep 2024; PR). A connectome-constrained "deep mechanistic network" of 64 optic-lobe cell types, trained on a motion-detection task. Predictions agreed with measurements across 26 studies, and sparse connectivity improved predictivity. PyTorch code is public. — [Janelia](https://www.janelia.org/publication/connectome-constrained-networks-predict-neural-activity-across-the-fly-visual-system); [Nature](https://www.nature.com/articles/s41586-024-07939-3); [GitHub](https://github.com/TuragaLab/flyvis)
- **flybody** (Vaxenburg et al., "Whole-body physics simulation of fruit fly locomotion", Nature 643:1312–1320, 2025; PR). Google DeepMind + HHMI Janelia.
  - MuJoCo body with walking-imitation, flight and vision-guided flight tasks, and a 59-dimensional walking action space.
  - Controllers are trained by deep RL, not taken from the connectome. Apache-2.0.

  — [GitHub](https://github.com/TuragaLab/flybody); [Nature](https://www.nature.com/articles/s41586-025-09029-4)
  - Eon contrasts its work with DeepMind's approach, which used "reinforcement learning, not connectome-derived neural dynamics". — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload)

#### Other connectome-to-behaviour embodied efforts
- **FlyGM** (Jin, Zhu, Zhang, Sui; Georgia Tech/Tsinghua; arXiv 2602.17997, Feb 2026, revised Jun 2026; preprint). "Whole-Brain Connectomic Graph Model Enables Whole-Body Locomotion Control in Fruit Fly".
  - FlyWire v783 as a graph whose synaptic weight matrix is a fixed recurrent operator. Each neuron gets trainable "intrinsic descriptors".
  - Drives flybody with 59 walking actuators and 12 flight signals. Tasks: gait initiation, straight walking, turning and flight.
  - Training: imitation of expert MLP policies, then PPO.
  - Baselines: degree-preserving rewired graphs, Erdős–Rényi graphs and MLPs.
  - High-yaw turning angle error was 8.29 for FlyGM, versus 13.55 for rewired and 125.36 for random graphs.
  - Evaluation is task performance, not fidelity to fly neural data. Code at lnsgroup.cc/research/FlyGM.

  — [arXiv abs](https://arxiv.org/abs/2602.17997); [arXiv html](https://arxiv.org/html/2602.17997v1)
- **"The digital sphinx: Can a worm brain control a fly body?"** (Brunton lab with Tuthill, UW; bioRxiv Mar 2026; eLife reviewed preprint).
  - A *C. elegans* connectome gets fly-body sensory input. A deep-RL-trained network maps worm motor neurons to fly leg actuators.
  - The result is "highly realistic fly walking", including joint-angle trajectories and leg coordination, "yet it is biologically meaningless".
  - The authors' conclusion: "behavioral fidelity is achievable without biological fidelity, making such models easy to overinterpret".

  — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.03.20.713233v1); [eLife RP](https://elifesciences.org/reviewed-preprints/111516); [GitHub](https://github.com/Brunton-Lab/DigitalSphinx2026)
  - Quotes in The Transmitter:
    - Turaga (Janelia): connectome models lack "biophysical properties of neurons or the pools of neurotransmitters that modulate neural communication".
    - Cowley (CSHL): "Even a small network of 300 neurons contains enough information for deep learning to extract patterns."
    - Brunton: "biological systems don't always work optimally."

    — [The Transmitter](https://www.thetransmitter.org/systems-neuroscience/digital-sphinx-raises-questions-about-connectome-models/)
- **VNC connectome simulations** (Pugliese, Chou, Abe, Turcu, Lancaster, Tuthill, Brunton; bioRxiv Sep 2025; preprint).
  - A computational activation screen of DNs in VNC connectome simulations finds DNs that drive rhythmic leg motor activity, including walking command neuron DNg100.
  - Pruning isolates a minimal three-neuron rhythm generator (one inhibitory, two excitatory interneurons).
  - It predicts that DNb08 drives rhythmic leg movement, which was confirmed optogenetically in behaving flies. Code is public.

  — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.12.675944v1); [GitHub](https://github.com/smpuglie/Pugliese_cpg_2025)
  - Related preprint, not by Pugliese et al.: Sapkal et al. (Bidaye lab), "Central versus peripheral neural control of a coordinated walking pattern in Drosophila" (bioRxiv Apr 2026), experiments rather than a simulation. — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.04.29.721658v1.full)
- **Antennal grooming coordination** (Özdil et al., Ramdya lab, Nature Communications, 23 Apr 2026; PR; cited by Eon as "Özdil et al.").
  - Kinematic replay in NeuroMechFly infers contacts and forces.
  - Amputation and immobilisation show that body-part coordination does not need cross-body proprioceptive feedback.
  - The brain connectome shows centralized interneurons and shared premotor neurons.

  — [Nat Commun](https://www.nature.com/articles/s41467-026-72152-x); [bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.12.17.628844v1)
- **Descending networks** (Braun, Hurtak, Wang-Chen, Ramdya, Nature 630:686–694, 2024; PR). Command-like DNs co-activate larger DN populations through direct excitatory DN–DN connections in the brain. So single-DN "command" interfaces (as in Eon) are a simplification. — [Nature](https://www.nature.com/articles/s41586-024-07523-9)
- **Knockout training of visual projection neurons** (Cowley et al., Nature 2024; PR).
  - A deep network whose units map one-to-one to 57 lobula columnar (LC/LPLC) types, about 3.5% of brain neurons.
  - Trained on behaviour after silencing each type in male flies during courtship.
  - Found that "combinations of visual projection neurons, including those involved in non-social behaviours, drive male interactions with the female", i.e. a population code.

  — [Nature](https://www.nature.com/articles/s41586-024-07451-8)
- **Earlier whole-fly-brain emulation platform.** Neurokernel (Lazar lab; open-source fly brain emulation platform). — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4709234/)
- **Review.** Wang-Chen & Ramdya, "The embodied brain: Bridging the brain, body, and behavior with biorealistic neuromechanical models" (arXiv 2601.08056, Jan 2026, revised Jul 2026). Advocates "coupling experimental studies with active probing of their neuromechanical surrogates". — [arXiv](https://arxiv.org/abs/2601.08056)

#### Hobbyist and open-source wave (2026)
- **The `awesome-fly` list** catalogues 20+ "games" driven by MaleCNS or FlyWire graphs (Doom, Mario 64/Fly64, Flappy Bird, CARLA driving, chess and others) and several embodied implementations:
  - webgpu-fly (FlyWire + MANC + flybody in WebGPU)
  - NeuroFly (FlyWire activity + NeuroMechFly)
  - "Embodied fly-brain" (FlyWire spiking + NeuroMechFly/MuJoCo)
  - CHIMERA (larval connectome + MuJoCo)

  — [GitHub](https://github.com/cobanov/awesome-fly)
- **Lulzx/fly-brain.** "Embodied whole-CNS Drosophila connectome simulation in the browser: 165k-neuron LIF brain (WASM) + MuJoCo flybody + flyvis vision". Architecturally very close to this project's plan. — [GitHub](https://github.com/Lulzx/fly-brain)
- **nfly.** MaleCNS v1.0 as a recurrent network playing Gymnasium games. — [GitHub](https://github.com/zhengxuyu/nfly)

### Inferences
- **The project's README says its visual front end is "like Eon's embodied fly". That is only partly true.**
  - Both skip retina-to-lamina spiking.
  - Eon used a *connectome-constrained optic-lobe model* (flyvis, 64 types) as the front end. This project drives four hand-picked visual projection neuron (VPN) types (LPLC2, LC4, LPLC1, LC10a) with hand-designed feature detectors.
  - Eon reports that its vision did not substantially affect behaviour, so it is not a validated precedent for vision-driven behaviour.
  - Cowley et al.'s population-code result warns against assigning one behaviour per LC type (e.g. "LC10a = chase") without testing.
- **MaleCNS contains the VNC, so this project can go beyond Eon.** Eon lacked motor neurons ("body wasn't scanned").
  - With the whole CNS, legs could be driven by simulated leg motor neurons rather than hand-mapped DN-to-controller shortcuts.
  - Pugliese et al. show that VNC connectome simulations can produce DN-triggered rhythms.
  - Mineault explicitly recommends decoding motor output from the VNC.
- **Any trained decoder, adapter or RL policy between the connectome and the body needs controls.** The digital sphinx and FlyGM results show why. Controls should include:
  - degree-preserving rewired graphs
  - random graphs
  - a non-fly connectome
  - noise-only drive (Mineault's "button mashing" critique of Fly64, whose neuron model this project adapted)
- **"First embodied" is debatable.** NeuroMechFly v2 already closed a loop through a connectome-constrained sub-network (flyvis) in 2024. Eon's novelty is using a *whole-brain* LIF, but locomotion is still produced by non-connectome controllers.

### Gaps
- **How flyvis outputs reach Eon's brain.** Which FlyWire neurons receive the flyvis outputs, and how graded outputs become LIF input currents, is not described in the fetched text.
- **Eon specifics:** the exact oDN1/DNa01/DNa02-to-controller mapping, simulation timestep and coupling rate, funding amount, and whether any peer-reviewed paper is planned.
- **Muscle-level body model.** "Musculoskeletal simulation of limb movement biomechanics in Drosophila melanogaster" (arXiv 2509.06426) surfaced but was not reviewed. It is likely relevant for body-layer refinement ([arXiv](https://arxiv.org/pdf/2509.06426)).
- **Other companies.** No other startup or company (Google, DeepMind beyond flybody) with a public connectome-driven embodied fly was found.
- **Sources not reviewed:** the Hacker News discussion of Eon ([HN](https://news.ycombinator.com/item?id=47393324)).

## Q2. Analogous projects in other animals (OpenWorm, BAAIWorm/MetaWorm, larval Drosophila, larval zebrafish) and their lessons

### Takeaway
Lesson from the worm: having a connectome did not produce an emulation. Progress stalled for a decade, largely because synaptic strengths (and, by inference, signs and neuromodulation) could not be read from anatomy. Randi et al. 2023 showed that anatomy predicts signal propagation poorly and that extrasynaptic signalling contributes.

Progress in the worm resumed only when detailed biophysics was combined with functional data (BAAIWorm 2024). Zebrafish has the best activity benchmark (ZAPBench), with a matched connectome still in progress. Larval Drosophila has a complete brain connectome, and body models are only now being coupled to it.

### Cited Findings

#### C. elegans
- **OpenWorm** launched in 2011 as an open-science project to build a biophysical simulation of *C. elegans*. — [Sarma et al., Phil Trans B 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6158220/)
  - Summaries note that anatomical data "can't tell … the relative importance of connections … only that a connection exists". — [search summary of OpenWorm sources](https://royalsocietypublishing.org/rstb/article/373/1758/20170382/42153/OpenWorm-overview-and-recent-advances-in)
  - Community critique: "Whole Brain Emulation: No Progress on C. elegans After 10 Years" (commentary). — [LessWrong](https://www.lesswrong.com/posts/mHqQxwKuzZS69CXX5/whole-brain-emulation-no-progress-on-c-elegans-after-10)
- **BAAIWorm / MetaWorm** (BAAI; Nature Computational Science 4(12), 2024; PR; bioRxiv Feb 2024).
  - Brain model: multi-compartment neurons with realistic morphology, the connectome, and population dynamics fit to data.
  - Body: a soft body of 3,341 tetrahedra with 96 muscles, in a 3D fluid environment with food.
  - It replicated locomotion, and synthetic perturbations of synapses changed embodied behaviour. Open source.

  — [Nat Comput Sci](https://www.nature.com/articles/s43588-024-00738-w); [GitHub](https://github.com/Jessie940611/BAAIWorm); [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.02.22.581686v2); [N&V](https://www.nature.com/articles/s43588-024-00740-2)
- **Neural signal propagation atlas** (Randi, Sharma, Divali, Leifer, Nature, Nov 2023; PR).
  - Optogenetic activation plus whole-brain imaging across 23,433 neuron pairs.
  - "Signal propagation differs from model predictions that are based on anatomy". Mutants show that extrasynaptic signalling not visible in the connectome contributes.

  — [Nature](https://www.nature.com/articles/s41586-023-06683-4)
- **Theory** (Beiran & Litwin-Kumar, Nature Neuroscience 28:2561–2574, 2025; PR). "Connectome datasets alone are generally not sufficient to predict neural activity". Pairing connectivity with recordings from a subset of neurons can predict unrecorded neurons. Code public. — [Nat Neurosci](https://www.nature.com/articles/s41593-025-02080-4); [GitHub](https://github.com/emebeiran/connconstr)

#### Larval Drosophila
- **Connectome** (Winding et al., Science, 10 Mar 2023; PR). Complete larval brain: 3,016 neurons and 548,000 synapses. Highly recurrent, with abundant feedback from DNs. — [Science](https://www.science.org/doi/full/10.1126/science.add9330); [data on GitHub](https://github.com/brain-networks/larval-drosophila-connectome)
- **"A behavioral architecture for realistic simulations of Drosophila larva locomotion and foraging"** (eLife reviewed preprint 104262). Modular, hierarchical larva simulations for closed-loop runs and direct comparison of simulated with empirical data. Includes intermittent crawling phase-coupled to lateral bending. — [eLife RP](https://elifesciences.org/reviewed-preprints/104262)
- **Connectome-coupled larva bodies (hobbyist/open source):**
  - cyber-larva: Winding connectome → sparse neural simulation → segmental VNC controller → 11-segment MuJoCo body. — [GitHub](https://github.com/ChenYvhang/cyber-larva)
  - CHIMERA: larval connectome linked to a MuJoCo body. — [awesome-fly](https://github.com/cobanov/awesome-fly)
  - An earlier physically measured neuromechanical crawling model. — [bioRxiv 2020](https://www.biorxiv.org/content/10.1101/2020.07.17.208611v1.full)
- **Frozen rate operator from the complete larval connectome** (arXiv 2606.17745, Jun 2026; preprint). "Degree and weight govern the gross response, exact wiring governs input routing and mushroom-body modes." This is directly relevant to what exact wiring buys. — [arXiv](https://arxiv.org/pdf/2606.17745)

#### Larval zebrafish
- **ZAPBench** (Google Research + HHMI Janelia; ICLR 2025).
  - About 71,721 neurons recorded by light-sheet for 2 h under 9 visual stimulus conditions.
  - Task: forecast activity up to 30 s ahead, scored by MAE against naive baselines.
  - Data and code are public. The same fish's EM connectome is being reconstructed at Janelia.

  — [Google blog, 24 Apr 2025](https://research.google/blog/improving-brain-models-with-zapbench/); [arXiv](https://arxiv.org/pdf/2503.02618); [GitHub](https://github.com/google-research/zapbench)
- **simZFish** (EPFL/Duke; Science Robotics 2025; PR). A neuromechanical larval zebrafish with body–water hydrodynamics, visual environment and experimentally derived network architecture, reproducing the optomotor response. Validated with a physical robot. Open source. — [Science Robotics](https://www.science.org/doi/10.1126/scirobotics.adv4408); [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.19.629427v1.full)
- **System identification on a synthetic zebrafish** (arXiv 2602.04492; preprint). Uses an in-silico zebrafish with known ground truth. — [arXiv](https://arxiv.org/html/2602.04492v1)

### Inferences
- **Why progress is faster in the fly than in the worm:**
  - several complete, proofread adult connectomes with neurotransmitter predictions (Q4)
  - thousands of cell-type-specific genetic lines (Q5)
  - whole-brain imaging (Q3)
  - two mature body simulators (Q1)
- **The worm's warnings carry over directly to a point-neuron LIF with one global parameter set, no neuromodulators and a rough sign rule (this project's stated limitations):**
  - extrasynaptic and neuromodulatory signalling (Randi)
  - non-identifiability of biophysical parameters from wiring alone (Beiran & Litwin-Kumar)
- **ZAPBench is the template for a fly neural-activity benchmark.** It uses held-out forecasting on public whole-brain recordings, with a connectome from the same animal. No fly equivalent was found (Q6).

### Gaps
- No quantitative BAAIWorm-versus-real-worm neural activity comparison numbers were extracted.
- Whether the ZAPBench fish's connectome has been released by Sept 2026 could not be confirmed.
- No published peer-reviewed larval Drosophila model coupling the full Winding connectome to a physical body was found; only hobbyist repos and behavioural models.

## Q3. Neural activity datasets for validation: whole-brain imaging, DN populations, cell-type activity and electrophysiology

### Takeaway
There are now about ten public adult-fly brain-wide activity datasets, most in NWB on DANDI, figshare or Princeton DataSpace. They are good for statistical and structural comparisons such as behaviour-locked activity maps, functional connectivity and global state effects.

Almost none are indexed to connectome neuron IDs. So cell-by-cell validation of a LIF model is still limited to targeted circuits:
- the visual system (via flyvis's compiled studies)
- the head-direction system
- DN populations
- olfaction

### Cited Findings

#### Whole-brain and large-volume imaging
- **Mann, Gallen & Clandinin 2017**, "Whole-Brain Calcium Imaging Reveals an Intrinsic Functional Network in Drosophila" (Current Biology 27:2389–2396; PR).
  - Resting-state activity is aligned to atlas regions.
  - Functional connectivity tracks direct and indirect anatomical pathways, with some regions exceeding predictions from direct connections.
  - The brief's "Mann, Gordon, Scott" author list is wrong.

  — [PubMed](https://pubmed.ncbi.nlm.nih.gov/28756955/)
- **Mann, Deny, Ganguli & Clandinin 2021**, "Coupling of activity, metabolism and behaviour across the Drosophila brain" (Nature; PR). — [Nature](https://www.nature.com/articles/s41586-021-03497-0)
- **Turner, Mann & Clandinin 2021** (Current Biology; PR).
  - The hemibrain connectome predicts region-to-region resting-state functional correlations.
  - Correspondence varies by region. The mushroom body depends more on indirect connections.
  - This is a ready-made structure-versus-function test.

  — [Current Biology](https://www.cell.com/current-biology/fulltext/S0960-9822(21)00343-2)
- **Aimon et al. 2019** (PLoS Biology 17:e2006732; PR).
  - Light-field near-whole-brain calcium and voltage imaging at up to 200 Hz in behaving flies.
  - Global activity rises during walking but not grooming, especially in dopamine neurons.

  — [PLoS Biol](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.2006732)
- **Pacheco, Thiberge, Pnevmatikakis & Murthy 2021** (Nature Neuroscience 24:93–104; PR).
  - Volumetric imaging with across-brain registration.
  - Auditory activity appears in 33 of 36 brain regions, mostly tuned to courtship-song features, with comparisons across individuals and sexes.
  - Dataset on Princeton DataSpace, doi:10.34770/gv6w-5351.

  — [Nat Neurosci](https://www.nature.com/articles/s41593-020-00743-y); [dataset](https://datacommons.princeton.edu/discovery/catalog/doi-10-34770-gv6w-5351)
- **Schaffer et al. 2023**, "The spatial and temporal structure of neural activity across the fly brain" (Nature Communications 14:5572; PR).
  - SCAPE imaging of about 1,419 single-cell ROIs per fly, across 18 female flies, at 8–12 volumes/s.
  - Covers the dorsal third of the central brain during running, grooming, flailing and quiescence.
  - Most neurons correlate or anticorrelate with running and flailing. The high-dimensional residual forms small spatial clusters, possibly cell types.
  - Data in NWB on figshare (doi:10.6084/m9.figshare.23749074). Code: VIP, flygenvectors, daart.

  — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10495430/); [Nat Commun](https://www.nature.com/articles/s41467-023-41261-2)
- **Brezovec et al. 2024**, "Mapping the neural dynamics of locomotion across the Drosophila brain" (Current Biology, online 18 Jan 2024; PR).
  - Volumetric two-photon whole-brain maps of forward- and angular-velocity-related signals, and their temporal order.
  - Data on DANDI as dandiset 000727, "Mapping the Neural Dynamics of Locomotion across the Drosophila Brain".

  — [PubMed](https://pubmed.ncbi.nlm.nih.gov/38242122/); [DANDI ID via Sci Data 2025](https://www.nature.com/articles/s41597-025-06285-x)
- **Gauthey et al. 2026**, "High-speed whole-brain imaging in Drosophila" (Nature Communications 17:5810, 28 Apr 2026; PR). Light beads microscopy records the whole brain at 28 volumes/s, or the central brain at 60 volumes/s, in behaving flies. It reveals fast auditory responses missed by conventional two-photon imaging. — [Nat Commun](https://www.nature.com/articles/s41467-026-72437-1); [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.06.18.660371v2)

#### Descending neurons and motor-related populations
- **Aymanns, Chen & Ramdya 2022** (eLife 11:e81527; PR). Recordings of about 100 DNs per tethered fly during odour-evoked and spontaneous walking and grooming. Most encode walking; fewer are active in head grooming and rest. Analysis code and data pointers on GitHub. — [eLife](https://elifesciences.org/articles/81527); [GitHub](https://github.com/NeLy-EPFL/DN_population_analysis)
- **Braun et al. 2024.** DN population recruitment by command-like DNs, explained by DN–DN connectome wiring (see Q1). — [Nature](https://www.nature.com/articles/s41586-024-07523-9)

#### Circuit-specific activity (for the internal-dynamics checks Eon says it has not done)
- **Head-direction ring attractor:**
  - Seelig & Jayaraman 2015, E-PG bump dynamics. — [doi:10.1038/nature14446](https://doi.org/10.1038/nature14446) (prior-knowledge citation, not re-fetched)
  - Kim et al. 2017, "Ring attractor dynamics in the Drosophila central brain". — [doi:10.1126/science.aal4835](https://doi.org/10.1126/science.aal4835) (prior-knowledge citation, not re-fetched)
- **Visual system.** flyvis predictions agreed with measurements from 26 studies; these form a curated target set for the optic-lobe layer. — [Janelia](https://www.janelia.org/publication/connectome-constrained-networks-predict-neural-activity-across-the-fly-visual-system)
- **Olfaction:**
  - Odorant-receptor response matrix (Hallem & Carlson 2006). — [doi:10.1016/j.cell.2006.01.050](https://doi.org/10.1016/j.cell.2006.01.050) (prior-knowledge citation, not re-fetched)
  - The DoOR 2.0 consensus odorant-response database. — [doi:10.1038/srep21841](https://doi.org/10.1038/srep21841) (prior-knowledge citation, not re-fetched)

#### Repositories
- **DANDI** holds over 400 NWB datasets (>350 TB, >20 species), including Drosophila dandiset 000727. — [Scientific Data 2025](https://www.nature.com/articles/s41597-025-06285-x)
- **State of Brain Emulation data repository** (24 curated datasets, 2,086 data points; CC BY 4.0). — [Zenodo via report site](https://brainemulation.mxschons.com/)

### Inferences
- **Most usable now for a LIF whole-CNS model:**
  - behaviour-conditioned whole-brain statistics: fraction of neurons modulated by walking versus grooming (Aimon, Schaffer, Brezovec)
  - region-level functional connectivity (Mann 2017; Turner 2021)
  - modality spread (Pacheco)
  - DN population tuning (Aymanns)

  These can be compared at region or population level by mapping simulated neurons to atlas regions. That avoids the missing neuron-ID correspondence.
- **All major whole-brain datasets come from females.** This project's MaleCNS model should be validated in regions shown to be isomorphic (Q4), or its sex-specific predictions treated as untested.
- **Temporal resolution limits spike-level checks.** Calcium imaging at 8–60 volumes/s can test slow population structure but not spike-timing-level LIF details (the 12–15 ms brain step mentioned in the project README).

### Gaps
- **No cell-type-resolved, connectome-ID-indexed, whole-brain activity atlas for adult flies was found.**
  - The "Functional Drosophila Atlas" (an in vivo reference for aligning imaging to connectomes) surfaced in search, but its primary paper and download could not be confirmed.
  - A model-derived "visual function profile" preprint (arXiv 2512.06934) was not reviewed.
- **Data availability not verified** for Mann 2017, Aimon 2019, Gauthey 2026 and Aymanns 2022. Aymanns data is possibly on Harvard Dataverse (unconfirmed).
- **No systematic search of public fly electrophysiology archives** (e.g. CRCNS, DANDI fly ephys) was completed. The olfactory and head-direction citations above are from prior knowledge.
- **No whole-VNC activity dataset** was reviewed, e.g. VNC imaging in behaving flies.

## Q4. Connectome datasets, access tools, and differences between sexes and individuals

### Takeaway
As of Sept 2026 there are three whole-CNS-scale adult datasets:
- **MaleCNS v1.0** (male; 166,700 neurons; CC-BY 4.0)
- **BANC** (female brain and nerve cord; Nature 2026)
- **FlyWire FAFB v783** (female brain only; CC BY-NC 4.0)

These sit alongside the hemibrain, MANC, FANC and the male optic lobe.

Cross-dataset work shows that:
- cell types and strong connections are stereotyped
- connection weights vary within and between animals
- sexual dimorphism is concentrated in higher brain centres

### Cited Findings
- **MaleCNS v1.0** (Berg et al., "Sexual dimorphism in the complete Drosophila male central nervous system connectome", Cell 2026; bioRxiv Oct 2025; PR).
  - 166,700 neurons across brain and nerve cord, fully proofread and annotated, including fruitless/doublesex expression.
  - 11,710 neuron types.
  - Male–female comparison: 8,069 isomorphic, 138 dimorphic, 289 male-specific and 71 female-specific types.
  - Dimorphism is concentrated in higher brain centres, while the sensory and motor periphery is largely isomorphic. Male-specific connections form "hotspots" and "circuit switches".

  — [Cell](https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6); [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.10.09.680999v1); [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12636603/)
  - **Access:** v1.0 was released 8 Jun 2026 (v0.9 on 3 Oct 2025), via neuPrint (`male-cns:v1.0`), Clio and downloads, under CC-BY 4.0. It includes a Dimorphism Explorer. Collaborators: FlyEM/Janelia, Cambridge, MRC LMB, Google Research. — [male-cns.janelia.org](https://male-cns.janelia.org/); [neuPrint](https://neuprint.janelia.org/?dataset=male-cns%3Av1.0&qt=findneurons)
  - **Companion paper:** "The organization of visual pathways in the Drosophila brain" (Cell 2026). — [Cell](https://www.cell.com/cell/fulltext/S0092-8674(26)00941-4)
  - **Count discrepancies:** other sources give 166,691 neurons / 11,691 types ([nfly README](https://github.com/zhengxuyu/nfly)) and "13,000+ annotations" ([flyconnecto.me](https://flyconnecto.me/2026/09/04/the-adult-drosophila-connectome-ecosystem/)).
- **FlyWire FAFB v783** (Dorkenwald et al., Nature 2024; PR).
  - 139,255 proofread neurons and 54.5 million synapses. Brain only: central brain plus optic lobes.

  — [Nature](https://www.nature.com/articles/s41586-024-07558-y); [Science News](https://www.sciencenews.org/article/fruit-fly-brain-connections-traced)
  - **Snapshot:** v783 corresponds to October 2023. — [FlyWire ToS](https://flywire.ai/tos)
  - **Licence:** data are CC BY-NC 4.0 (non-commercial). Cite Dorkenwald et al., flywire.ai and the Zheng et al. 2018 EM data (also CC BY-NC 4.0). — [FlyWire ToS](https://flywire.ai/tos); [guidelines](https://flywire.ai/guidelines)
  - **Access:** Codex holds FAFB v783, BANC (v888, 20 May 2026; v626, Jul 2025), MANC v1.2.1, MAOL v1.1 and MCNS v1.0/v0.9. The hemibrain is not in Codex. — [Codex FAQ](https://codex.flywire.ai/faq)
  - Codex tracks the live database, so reproducible builds should use static snapshots. — [connectome-kg docs](https://pypi.org/project/connectome-kg/0.5.0/)
- **Annotation and stereotypy** (Schlegel et al., Nature 2024; PR).
  - Hierarchical annotation of FlyWire and a consensus cell-type atlas across FlyWire and the hemibrain.
  - Cell-type counts and strong connections are largely stable, but "connection weights were surprisingly variable within and across animals".
  - Connections stronger than 10 synapses, or providing >1% of a target's input, are highly conserved.
  - Kenyon cells are almost twice as numerous in FlyWire as in the hemibrain. There is evidence for homeostatic preservation of the excitation/inhibition ratio.

  — [Nature](https://www.nature.com/articles/s41586-024-07686-5); [search summary](https://pmc.ncbi.nlm.nih.gov/articles/PMC10327018/)
- **Hemibrain v1.2.1.** About 25,000 neurons, female, about one-third of the central brain, 8 nm isotropic, via neuPrint. — [flyconnecto.me](https://flyconnecto.me/2026/09/04/the-adult-drosophila-connectome-ecosystem/); [Scheffer et al. 2020, doi:10.7554/eLife.57443](https://doi.org/10.7554/eLife.57443) (prior-knowledge citation, not re-fetched)
- **Male optic lobe (MAOL)** (Nern et al., "Connectome-driven neural inventory of a complete visual system", Nature 641:1225–1237, 2025; PR). About 53,000 neurons in 732 types (about half newly named), with matched split-GAL4 lines. The Cell Type Explorer and analysis code are public. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/38659887/); [Nature](https://www.nature.com/articles/s41586-025-08746-0); [code](https://github.com/reiserlab/male-drosophila-visual-system-connectome-code)
- **MANC** (male VNC; Takemura et al. eLife 2024). Over 23,000 neurons, more than 10M presynapses and 74M postsynapses. All DNs and motor neurons proofread and matched to light microscopy. — [search summary / eLife RP](https://elifesciences.org/reviewed-preprints/97769v1/reviews)
  - Premotor organisation analysed in Cheong et al. — [eLife](https://elifesciences.org/articles/96084)
  - Systematic annotation in Marin et al. — [eLife RP](https://elifesciences.org/reviewed-preprints/97766)
  - **Discrepancy:** flyconnecto.me lists MANC as 15,800 neurons on neuPrint v1.2.3 (Codex lists v1.2.1). — [flyconnecto.me](https://flyconnecto.me/2026/09/04/the-adult-drosophila-connectome-ecosystem/)
- **FANC** (female VNC; Azevedo et al., Nature 631:360–368, 2024; PR). About 14,600 neuronal cell bodies and about 45M synapses. Maps the muscle targets of leg and wing motor neurons. — [Nature](https://www.nature.com/articles/s41586-024-07389-x)
- **BANC** (female brain and nerve cord with intact neck; Bates, Phelps, Kim, Yang et al., "Distributed control circuits across a brain-and-cord connectome", Nature 2026; PR, open access).
  - The first connectome to unite brain and VNC in one animal.
  - Annotated for type, neurotransmitter, hemilineage, function and cross-dataset identity. Public via flywire.ai/Codex.

  — [GitHub](https://github.com/htem/BANC-project); [Nature](https://www.nature.com/articles/s41586-026-10735-w); [FlyWire blog](https://blog.flywire.ai/2025/11/03/the-banc-brain-and-nerve-cord/)
  - **Size discrepancy:** ~188,000 neurons and 199M predicted synapses per the BANC repo, versus 142,000 neurons per flyconnecto.me. — [flyconnecto.me](https://flyconnecto.me/2026/09/04/the-adult-drosophila-connectome-ecosystem/)
- **DN/AN comparative connectomics** (Stürner et al., Nature 643:158–172, 2025; PR). Integrates FAFB, FANC and MANC to fully describe female descending and ascending neurons and compare them with the male nerve cord. Describes sexually dimorphic DN/AN populations and matches 51% of DN types to driver lines. — [Nature](https://www.nature.com/articles/s41586-025-08925-z)
- **Tools:**
  - access clients: neuPrint (and neuprint-python), CAVEclient, Codex
  - R and Python toolkits: natverse (malecns, coconatfly, bancr), navis and fafbseg
  - analysis helpers: cocoa (cross-dataset typing), connectome_interpreter and connectome_data_prep (prepared matrices for MaleCNS, BANC, FlyWire, hemibrain)
  - flyconnectome/drosophila_neurotransmitters (cross-dataset neurotransmitter ground truth)

  — [awesome-fly](https://github.com/cobanov/awesome-fly)

### Inferences
- **Licensing favours MaleCNS.** MaleCNS (CC-BY 4.0) permits commercial reuse. FlyWire-derived assets are CC BY-NC 4.0, including Eon's repo and the Shiu model built on FlyWire. This matters if any part of the project is commercial.
- **Test robustness to variability.** Schlegel's conservation thresholds suggest two checks:
  - re-run key experiments using only conserved edges (>10 synapses or >1% input)
  - swap in type-matched connectivity from FlyWire or BANC

  A result that depends on weak, variable edges is unlikely to be biological.
- **Sex-specific predictions need female controls.** Most validation data come from females (Q3), and dimorphism is concentrated in higher centres. Behaviours routed through male-specific "hotspots" (e.g. the project's pC1/courtship features) should be treated as male-specific predictions and checked against female-connectome controls (BANC/FlyWire).

### Gaps
- **Unconfirmed MaleCNS counts.** The brief's "25.6M connections" for MaleCNS could not be confirmed, nor could the MaleCNS total synapse count.
- **Unattributed synapse figure.** A Science news item on "124 million contact points" surfaced but could not be tied to a specific dataset.
- **Licences not verified** for BANC, MANC and FANC.
- **Unreviewed sex-difference paper.** A connectome-alignment paper on VNC sex differences surfaced but was not reviewed ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13307954/)).

## Q5. Behaviour, kinematics and perturbation datasets

### Takeaway
Validation data for the behaviour layer are rich and mostly public:
- Janelia's thermogenetic activation atlas (2,204 lines) and DN optogenetic screens (Cande 2018; Dryad videos)
- unsupervised behaviour maps (Berman 2014)
- courtship state models (Calhoun 2019)
- about 3,000 split-GAL4 lines, plus 738 DN lines covering 171 DN types
- 3D kinematics for walking (DeepFly3D, DeAngelis/Dryad), wings (Melis/CaltechDATA) and grooming (Özdil 2026)
- multi-fly pose benchmarks (MABe22)

Perturbation outcomes from connectome-model papers (Shiu, Pugliese, Cowley, Braun) give ready-made pass/fail tests.

### Cited Findings

#### Behaviour atlases and maps
- **Robie et al. 2017**, "Mapping the Neural Substrates of Behavior" (Cell; PR).
  - Thermogenetic activation of 2,204 Janelia GAL4 lines.
  - JAABA classifiers scored 14 behaviours (e.g. wing flicking, crab walking, attempted copulation) over about 400,000 flies and more than 225 days of video.
  - Browsable via BABAM (Browsable Atlas of Behavior-Anatomy Maps).

  — [Cell](https://www.cell.com/cell/fulltext/S0092-8674(17)30716-X); [HHMI](https://www.hhmi.org/news/artificial-intelligence-helps-build-brain-atlas-fly-behavior)
- **Berman, Choi, Bialek & Shaevitz 2014** (J. R. Soc. Interface 11:20140672; PR). Unsupervised postural-dynamics map. Flies are stereotyped about 50% of the time, with over 100 stereotyped behavioural states. MotionMapper code is public. — [J R Soc Interface](https://royalsocietypublishing.org/doi/10.1098/rsif.2014.0672); [GitHub](https://github.com/gordonberman/MotionMapper)
- **Calhoun, Pillow & Murthy 2019** (Nature Neuroscience 22:2040–2049; PR). Three latent internal states govern male song patterning based on female feedback. A pair of putative song "command" neurons is sufficient to drive state switching. — [Nat Neurosci](https://www.nature.com/articles/s41593-019-0533-x)
- **MABe22** (ICML 2023). Includes 4.4M frames of multi-fly pose tracking from the Janelia Branson/Rubin labs, with downstream tasks such as strain, optogenetic stimulation and behaviour. Data on CaltechDATA. — [arXiv](https://arxiv.org/abs/2207.10553); [data](https://data.caltech.edu/records/rdsa8-rde65)

#### Perturbation screens and genetic access
- **Cande et al. 2018**, "Optogenetic dissection of descending behavioral control in Drosophila" (eLife; PR). Activates DN lines in freely behaving flies and maps effects onto a 2D behaviour space. Videos (1 s before and after activation) are on Dryad, doi:10.5061/dryad.fr89c0c. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6031430/); [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.fr89c0c)
- **Namiki et al. 2018** (DN anatomical organisation; eLife). — [doi:10.7554/eLife.34272](https://doi.org/10.7554/eLife.34272) (prior-knowledge citation, not re-fetched)
- **Zung, Namiki, Meissner & Card 2025** (bioRxiv Feb 2025; eLife reviewed preprint). 500 new DN split-GAL4 lines, bringing the total to 738 lines targeting 171 DN types, each quality-scored A–C. — [eLife RP](https://elifesciences.org/reviewed-preprints/107450); [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.02.22.639679v1)
- **Meissner et al. 2025** (eLife, 24 Jan 2025; PR).
  - 3,060 adult split-GAL4 lines (from more than 77,000 combinations tested) plus 1,373 larval lines.
  - Searchable for light-to-EM matching in NeuronBridge.
  - FlyLight has contributed 540,000 3D images, and stocks have been distributed 300,000 times.

  — [eLife](https://elifesciences.org/articles/98405)
- **Perturbation outcomes from connectome-model papers (ready-made tests):**
  - Shiu et al. 2024: sugar- and water-gustatory-neuron activation, feeding motor neurons, and antennal grooming circuits; 164 tested predictions, 91% consistent. — [Nature](https://www.nature.com/articles/s41586-024-07763-9)
  - Pugliese et al. 2025: DNg100 and DNb08 drive leg rhythms, the latter confirmed optogenetically. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.12.675944v1)
  - Cowley et al. 2024: behavioural effects of silencing each of more than a dozen LC/LPLC types during courtship. — [Nature](https://www.nature.com/articles/s41586-024-07451-8)
  - Braun et al. 2024: activating command-like DNs recruits DN networks. — [Nature](https://www.nature.com/articles/s41586-024-07523-9)

#### 3D pose and kinematics
- **DeepFly3D** (Günel et al., eLife 2019; PR). Multi-camera 3D pose for tethered flies. Nearly one million images with 3D joint positions, plus network weights and training data, are public. — [eLife](https://elifesciences.org/articles/48571); [GitHub](https://github.com/NeLy-EPFL/DeepFly3D)
- **DeAngelis, Zavatone-Veth & Clark 2019**, "The manifold structure of limb coordination in walking Drosophila" (eLife 8:e46409; PR). Gait is a continuum of coordination patterns with no discrete preferred gaits. Data on Dryad (doi:10.5061/dryad.3p9h20r). A 2020 correction fixed a coherence-equation sign. — [eLife](https://elifesciences.org/articles/46409); [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.3p9h20r)
- **Related Dryad dataset:** "Spatiotemporally precise optogenetic activation of sensory neurons in freely walking Drosophila". — [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.nzs7h44nk)
- **Melis, Siwanowicz & Dickinson 2024**, "Machine learning reveals the control mechanics of an insect wing hinge" (Nature; PR). Steering-muscle calcium imaging with simultaneous high-speed 3D wing tracking; a CNN predicts wing motion from muscle activity. Data on CaltechDATA; code on GitHub. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.06.29.547116v3); [data](https://data.caltech.edu/records/aypcy-ck464); [code](https://github.com/FlyRanch/mscode-melis-siwanowicz-dickinson)
- **Grooming kinematics** (Özdil et al. 2026). Head, antenna and foreleg synchrony, replayed in NeuroMechFly. — [Nat Commun](https://www.nature.com/articles/s41467-026-72152-x)
- **Kinematic replay** in NeuroMechFly v1 and imitation targets in flybody provide body-level ground truth pipelines. — [NMF v1](https://www.nature.com/articles/s41592-022-01466-7); [flybody](https://github.com/TuragaLab/flybody)

### Inferences
- **Cheapest high-value behavioural test for this project.** Reproduce the *direction* of published activation phenotypes by stimulating the same cell types in the model and reading out behaviour:
  - Cande 2018 DN activations
  - Robie 2017 line activations, mapped to cell types via FlyLight/NeuronBridge
  - Shiu's 164 predictions (needs FlyWire-to-MaleCNS type matching)
- **Kinematic validation.** DeAngelis (walking coordination continuum), DeepFly3D (joint angles) and Melis (wing kinematics) give quantitative targets once motor output is decoded from simulated motor neurons rather than pre-built controllers.

### Gaps
- **Unconfirmed download details:** a direct download URL and licence for the BABAM/Robie 2017 data, and the data availability for Calhoun 2019.
- **No large free-flight kinematics dataset** (e.g. looming-evoked evasive saccades) was verified this session.
- **Unreviewed dataset:** the flybody paper's imitation-learning kinematic datasets were not individually identified.

## Q6. Benchmarks, roadmaps and expert views on the feasibility and timeline of whole-fly emulation

### Takeaway
No agreed benchmark for fly brain emulation exists. The closest analogues are:
- ZAPBench (zebrafish activity forecasting)
- the Carboncopies synthetic-ground-truth challenge
- ad hoc test sets inside papers: Shiu's 164 predictions, flyvis's 26-study comparison, and Turner 2021's structure–function correlation

Optimistic roadmaps put sub-million-neuron emulations (fly, zebrafish) 3–10 years out, at costs up to about $100M:
- the State of Brain Emulation Report 2025, co-authored by Eon's head of engineering
- Schons (Asimov Press, Jan 2026)

Working fly neuroscientists stress the missing pieces:
- biophysics and neuromodulation
- the non-identifiability of parameters from wiring alone
- the ease of faking behavioural fidelity

### Cited Findings

#### Roadmaps and reports
- **State of Brain Emulation Report 2025** (Zanichelli, Schons, Freeman, Shiu, Arkhipov; arXiv 2510.15745, Oct 2025, v3 Nov 2025; CC BY 4.0; preprint). Reassesses the field since Sandberg & Bostrom's 2008 roadmap, across recording, connectomics, and emulation plus embodiment. — [arXiv](https://arxiv.org/abs/2510.15745)
  - Scope: a 175-page technical report with 41 expert contributors. It estimates that fewer than 500 people worldwide work directly on brain emulation. It includes a Budget Guesstimator and 24 curated datasets (2,086 data points). — [report site](https://mxschons.com/projects/state-of-brain-emulation-report-2025/); [research overview](https://brainemulation.mxschons.com/)
  - Fly emulation is described as within reach, potentially within the decade at costs in the low $100Ms (paraphrase from the report site, not a verbatim quote). Data acquisition, not hardware or algorithms, is the main constraint, with recording duration, temporal resolution and head fixation as limits. Data repository: Zenodo doi:10.5281/zenodo.18377594. — [brainemulation.mxschons.com](https://brainemulation.mxschons.com/)
  - **Conflict of interest:** co-author Philip Shiu is Eon's Head of Engineering. — [The Transmitter](https://www.thetransmitter.org/systems-neuroscience/digital-sphinx-raises-questions-about-connectome-models/)
- **Max Schons, "Building Brains on a Computer"** (Asimov Press, 26 Jan 2026).
  - Sub-million-neuron emulations, including fly and zebrafish, are possible in "the next three to eight years", given breakthroughs and funding.
  - A fly connectome costs "low hundreds of thousands of dollars" with automated proofreading, and a mouse connectome "low hundreds of millions".
  - Neural recording is "the most severe constraint", and emulations need neuromodulators and hormones.
  - He consulted more than 50 researchers. Human emulation is projected for the "late 2040s", with 10–50× error margins.

  — [Asimov Press](https://press.asimov.com/articles/brains)
- **Eon's roadmap.** The mouse (~70M neurons) is next, then human-scale emulation. A two-year mouse timeline appears only in secondary sources. — [Eon](https://eon.systems/updates/first-multi-behavior-brain-upload); [nexi.fund](https://nexi.fund/whole-brain-emulation-eon-2026/)
- **Wang-Chen & Ramdya 2026 review.** Neuromechanical surrogates should be iteratively probed alongside experiments. — [arXiv](https://arxiv.org/abs/2601.08056)

#### Benchmarks and validation frameworks
- **ZAPBench:** whole-brain activity forecasting (30 s horizon, MAE) on about 71,721 zebrafish neurons, with a same-animal connectome in progress. — [Google](https://research.google/blog/improving-brain-models-with-zapbench/); [arXiv](https://arxiv.org/pdf/2503.02618)
- **Carboncopies Brain Emulation Challenge.** Synthetic brains with known structure and function let reconstruction and emulation methods be scored on structural similarity, behavioural success and dynamic similarity. Inspired by ImageNet and Kaggle. — [Carboncopies](https://carboncopies.org/Research/BrainGenix/Challenge/Overview/); [GitHub](https://github.com/carboncopies/BrainEmulationChallenge)
- **In-silico zebrafish** as a ground-truth system-identification testbed. — [arXiv](https://arxiv.org/html/2602.04492v1)
- **Effectome** (Pospisil, Aragon, Pillow et al., Nature 634:201–209, 2024; PR). The connectome gives possible paths but not in vivo effect strengths. They propose estimating a linear whole-brain causal model from stochastic optogenetic perturbations, with the connectome as a prior. Analysis suggests high-dimensional dynamics from many small independent circuits. — [Nature](https://www.nature.com/articles/s41586-024-07982-0)
- **Existing fly "test sets" usable as benchmarks:**
  - Shiu's 164 predictions (91% agreement). — [Nature](https://www.nature.com/articles/s41586-024-07763-9)
  - flyvis's agreement with 26 studies. — [Janelia](https://www.janelia.org/publication/connectome-constrained-networks-predict-neural-activity-across-the-fly-visual-system)
  - Turner 2021 structure-versus-functional-connectivity. — [Current Biology](https://www.cell.com/current-biology/fulltext/S0960-9822(21)00343-2)
  - FlyGM's rewired and random-graph controls. — [arXiv](https://arxiv.org/html/2602.17997v1)
- **Mineault's three success criteria:** "the virtual fly displays complex, naturalistic, sensory-driven behaviors; when the generated electrophysiological activity looks increasingly fly-like; and when a simulated fly displays behaviors unique to that fly." — [neuroai.science](https://www.neuroai.science/p/are-flies-playing-beat-saber)

#### Expert scepticism
- Turaga, Cowley and Brunton (quotes in Q1) argue that behavioural realism can come from optimisation rather than biology. The key control question: "if I just created a randomly connected connectome, could it also do the same behaviors?" — [The Transmitter](https://www.thetransmitter.org/systems-neuroscience/digital-sphinx-raises-questions-about-connectome-models/)
- The connectome alone is generally insufficient to predict activity (Beiran & Litwin-Kumar 2025). — [Nat Neurosci](https://www.nature.com/articles/s41593-025-02080-4)
- Anatomy mispredicts signal propagation in the worm (Randi 2023). — [Nature](https://www.nature.com/articles/s41586-023-06683-4)

### Inferences
- **Timelines disagree by source.** Estimates from emulation advocates (3–10 years for a fly) come from people close to Eon and the report. Working connectome modellers (Turaga, Brunton, Tuthill, Litwin-Kumar) emphasise unsolved identifiability and biophysics. No source gives an evidence-based timeline for a *validated* fly emulation, and the gap between "embodied demo" (done, 2026) and "validated emulation" is not estimated anywhere.
- **Suggested layer-by-layer validation ladder for this project** (a synthesis of the datasets above; each row lists a dataset and a comparison):

| Layer | Validation data | Comparison |
|---|---|---|
| Wiring robustness | MaleCNS versus FlyWire/BANC type-matched connectivity; Schlegel conserved-edge thresholds (Q4) | Output stability when weak or variable edges are removed or connectomes swapped |
| Synapse sign | FlyWire/MaleCNS neurotransmitter predictions; drosophila_neurotransmitters ground truth (Q4) | Sensitivity of results to sign-rule errors (e.g. glutamate treated as inhibitory) |
| Visual front end | flyvis 26-study targets; Nern 2025 types; Cowley 2024 LC silencing phenotypes (Q1, Q3, Q5) | Replace hand-built feature detectors with flyvis outputs; test LC-type behavioural effects |
| Taste and mechanosensory to motor | Shiu 164 predictions (Q5) | Pass rate after FlyWire-to-MaleCNS type mapping |
| Central dynamics | Head-direction bump (Seelig 2015; Kim 2017); whole-brain behaviour-locked maps (Aimon, Schaffer, Brezovec, Gauthey); functional connectivity (Mann 2017; Turner 2021); auditory spread (Pacheco) (Q3) | Region- and population-level statistics; ring-attractor signatures |
| Descending neurons | Aymanns 2022 (~100 DNs); Braun 2024 recruitment; Cande 2018 activation phenotypes; Zung 2025 lines (Q3, Q5) | DN tuning versus walking and grooming; DN–DN co-activation |
| VNC and central pattern generators | Pugliese 2025 (DNg100, DNb08, 3-neuron CPG); MANC/FANC premotor maps (Q1, Q4) | Rhythms emerge in simulated leg motor neurons without a hand-coded CPG |
| Body and kinematics | DeAngelis 2019; DeepFly3D; Melis 2024 wings; Özdil 2026 grooming; NMF kinematic replay (Q5) | Joint-angle and inter-leg phase distributions |
| Behaviour | Berman 2014 maps; Robie 2017/BABAM; MABe22; Calhoun 2019 states (Q5) | Behaviour-space occupancy and transition statistics |
| Controls (every layer) | Rewired, random and non-fly connectomes; noise-only drive (FlyGM; digital sphinx; Mineault) | The effect must disappear or degrade under the controls |

### Gaps
- **No fly equivalent of ZAPBench** was found: no community held-out whole-brain forecasting benchmark with fly data plus connectome.
- **Mammalian benchmarks not checked:** Neural Latents Benchmark, Sensorium and Brain-Score are possible templates but were not verified this session.
- **Report internals not extracted:** fly-specific numbers from the State of Brain Emulation Report PDF, such as the percentage of fly neurons recordable simultaneously, and its exact fly cost model.
- **Affiliations unconfirmed:** whether other report authors (e.g. Schons) are affiliated with Eon.
- **No independent peer review** of Eon's work exists yet. All critiques found are blog, press or preprint commentary.
