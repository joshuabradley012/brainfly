# Drosophila muscles, biomechanics and physics-based body models: what it takes to turn motor neuron spikes into forces, joint torques and movement

Scope: the body side of an embodied, connectome-driven fly (Janelia MaleCNS v1.0 spiking model -> VNC motor neurons -> muscles -> joints -> physics). Status is as of September 2026. Every item is tagged peer-reviewed (PR), preprint (PP), conference paper (CONF), software/docs (SW) or company blog (BLOG). Numbers are quoted as reported. Anything marked "Inference" is my own reasoning, not a sourced claim.

## 1. Existing fly body models (NeuroMechFly v1, NeuroMechFly v2/FlyGym 1.x and 2.x, flybody) and 2025-2026 successors, including how connectome models were plugged in

### Takeaway
Two open MuJoCo fly bodies dominate. NeuroMechFly/FlyGym (EPFL, Ramdya lab) is a walking-first model with vision, olfaction, adhesion, CPG/rule-based/hybrid controllers, a 2-D "descending" command interface, and a flyvis connectome visual front end. FlyGym 2.x (April 2026) is a full rewrite that adds GPU batching (MuJoCo Warp), bundles the flybody model, and ships the first muscle-actuated fly leg (FlyMimic, Özdil et al.: 15 Hill-type muscles on the left front leg, experimental). flybody (DeepMind/Janelia, Nature 2025) is a 102-DoF whole-body model with a phenomenological wing-aerodynamics model and RL-trained walking and flight controllers. Every published whole-fly model still drives joints with position or torque actuators. Muscles exist only for one leg. Connectome-to-body coupling so far goes through a handful of descending neurons or learned decoders, not motor neurons.

### Cited Findings

#### NeuroMechFly v1 (Lobato-Rios et al., Nature Methods 2022; PR)
- Four modules: physics environment, a biomechanical exoskeleton, muscle models and neural-network controllers. Minimum leg DoFs were defined from 3-D walking and grooming kinematics. The model estimated torques and contact forces by kinematic replay, and optimized neural and muscle parameters for speed and stability. — [Nature Methods, doi:10.1038/s41592-022-01466-7](https://doi.org/10.1038/s41592-022-01466-7)
- Physics engine PyBullet. Body from X-ray micro-CT, split into 65 body segments. 7 DoFs per leg: ThC 3 (elevation/depression, protraction/retraction, rotation), CTr pitch + roll (the roll DoF "most markedly reduced" replay error), FTi pitch, TiTa pitch. Simulation time step 1 ms. — [bioRxiv v1 full text](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full)
- Muscles: an adapted Ekeberg spring-damper model, where joint torque is a linear function of flexor (M_F) and extensor (M_E) MN activity, with gain α, stiffness gain β, tonic stiffness γ, damping d and rest-angle offset Δφ. Only 3 DoFs per leg were controlled during optimization (ThC protraction/retraction, CTr and FTi flexion/extension). That gives 36 coupled oscillators (intrinsic frequency 3 Hz, amplitude 1). NSGA-II used 20 individuals × 50 generations, about 2.5 h per run on an i9-9900K. — [bioRxiv v1](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full)
- Replay data: DeepFly3D, 7 synchronized cameras at 100 fps, tethered walking and grooming. Estimated ground reaction forces fell within the range of the ~100 µN tibia-tip maximum. — [bioRxiv v1](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full)
- Contradiction (units): bioRxiv v1 states body length and mass "2.8 mm and 1 µg" with a head of 0.125 µg, a thorax of 0.31 µg, etc. A real fly weighs about 1 mg, so this is very likely a µg/mg typo. — [bioRxiv v1](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full); compare the flybody mass of 0.983 mg in [Vaxenburg et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Unresolved: I could not verify the total DoF count for v1 in the primary text. One secondary summary says "122 DoF". Eon Systems describes NeuroMechFly as having "87 independent joints". — [Eon blog](https://eon.systems/updates/embodied-brain-emulation)

#### NeuroMechFly v2 / FlyGym 1.x (Wang-Chen et al., Nature Methods, 12 Nov 2024; PR)
- Moved from PyBullet to MuJoCo (via dm_control). Fully Gymnasium-compliant; the problem is framed as a POMDP. Observations include vision, olfaction, ground contacts, joint angles/velocities/torques and the states of multiple flies. Actions are per-DoF control signals (e.g. target angles) plus a per-leg adhesion on/off. — [Nature Methods](https://www.nature.com/articles/s41592-024-02497-y); [EPFL postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Morphology updates: re-placed ThC and neck joints; antenna split into pedicel/funiculus/arista with new DoFs (four muscles actively control the scape–pedicel joint, the funiculus and arista move passively); neck yaw and roll DoFs added. Untethered 3-view corridor kinematics replaced v1's tethered-ball steps. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Adhesion is an extra normal force applied when the pretarsus touches a surface, switched off in swing, because Drosophila liftoff mechanisms are unknown. Without adhesion the fly slipped at about 30° incline. With it, the fly could sometimes walk on >90° slopes. Benchmarks used joint position gain kp = 45 and adhesion force "40 mN". — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Controllers:
  - CPG: one oscillator per leg, idealized tripod, adapted from salamander CPGs.
  - Rule-based: first three Walknet rules.
  - Hybrid: CPG plus "overstretch" and "stumbling" rules. Overstretch fires when a leg tip is >0.05 mm below the third most-extended leg. Stumbling fires on >1 "mN" contact force opposing heading during swing.
  - On gapped and blocks terrain the pure CPG struggles and the hybrid stays fast. The terrains are 1 mm blocks with 0.3 mm × 2 mm gaps, and 1.3 × 1.3 mm blocks offset 0.35 mm, benchmarked with 20 runs × 1.5 s.
  - Source: [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- "Descending" interface: a 2-D signal [DN_left, DN_right] modulates each side's oscillator intrinsic frequency and maximum amplitude. This mirrors real turning: outer-leg amplitude rises for turns <20°, inner-leg amplitude also falls for 20–50°, and inner legs step backward for >50°. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Senses:
  - Compound eye on a hexagonal ommatidia lattice with side length 16 (721 ommatidia per eye by hex-number arithmetic; real eyes have about 700–750). Yellow- and pale-type ommatidia at a 7:3 ratio.
  - Odor sensors on antennae and maxillary palps; odor gains γ_attractive = −500, γ_aversive = 80.
  - Source: [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Ascending-feedback demos: an MLP maps leg joint angles and contacts to neck roll and pitch for head stabilization; path integration from idiothetic cues predicts heading change with r² = 0.97. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Connectome plug-in (flyvis, Lappalainen et al. 2024):
  - The ommatidia lattices of FlyGym and FlyVision map one-to-one. Vision is sampled and flyvis is run at 500 Hz, with each eye simulated independently and a single best model used rather than the ensemble.
  - The readout is the activity of "34 T-shaped transmedullary neurons" (the figure says "34 putative output columnar neuron types (of 65 total)"). An object is detected where activity deviates from baseline by χ > 7. That detection drives the DN turning signal (range [0.4, 1.2]) for fly-following.
  - Source: [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Stated limitations: flight, abdomen (egg-laying) and proboscis (feeding) are "not yet implemented". The authors expect "careful measurements and analyses of the Drosophila musculoskeletal system (i.e., tendons and muscles)" to improve the interface between neural controllers and body. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Contradiction (units): the paper says meshes were scaled 1000× "to obtain observation measurements in mm and mN". But the FlyGym 2 rigging masses sum to 0.0009998 and gravity is 9810 mm/s², which is g–mm–s units, so forces are in µN (fly weight ≈ 9.8 units). Read as µN, the "40 mN" adhesion is about 4 body weights. Check the units before mapping any physiological muscle force into FlyGym. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf); [mujoco_globals.yaml](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/neuromechfly/mujoco_globals.yaml); [rigging.yaml](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/neuromechfly/rigging.yaml)
- Speed: the v2 paper plays videos back at 0.05–0.1× real time. That is a playback rate, not a benchmark. I found no real-time-factor number in the v2 paper. — [postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)

#### FlyGym 2.x (SW; complete rewrite)
- 2.0.0 released 2026-04-02 and 2.0.1 on 2026-04-16. Not backward compatible. The 1.x line moved to `flygym-gymnasium` (gymnasium.neuromechfly.org). — [changelog](https://neuromechfly.org/changelog/)
  - Date inconsistency: the GitHub README says "introduced in March 2026" and the docs home page says April 2026. — [README](https://github.com/NeLy-EPFL/flygym); [docs](https://neuromechfly.org/)
- Stated performance: "~10x speed-up for CPU-based simulations (~2x real-time throughput)" and "~300x speed-up for GPU-based simulation via Warp/MJWarp (~60x real-time throughput)". The benchmark conditions are not specified on the page. — [README](https://github.com/NeLy-EPFL/flygym)
- The GPU tutorial runs 100–1000 parallel worlds that must share one model, at a 1e-4 s timestep on an RTX 3080 Ti. GPU vision was "deferred" as of 2.0.2. — [GPU tutorial](https://neuromechfly.org/tutorials/3_gpu_accelerated_simulation/); [changelog](https://neuromechfly.org/changelog/)
- 2.0.2 changes:
  - Adhesion control range normalized to [0, 1].
  - Complex terrains added.
  - CPG, rule-based, hybrid and hybrid-turning controllers added as demos.
  - Fixed a bug where contact `solimp` silently lost its width parameter.
  - Source: [changelog](https://neuromechfly.org/changelog/)
- 2.1.0 changes:
  - Replaced dm_control PyMJCF with MuJoCo's native MjSpec.
  - Integrated FlyMimic (the Özdil et al. musculoskeletal leg) and the FlyBody model, both "experimental".
  - MuJoCo and MuJoCo Warp bumped to 3.9; Python 3.12–3.14.
  - Source: [changelog](https://neuromechfly.org/changelog/)
- Defaults in the FlyGym 2 code and config (units are g–mm–s, so µN and µN·mm):
  - Timestep 1e-4 s, Euler integrator, Newton solver, 100 iterations. — [mujoco_globals.yaml](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/neuromechfly/mujoco_globals.yaml)
  - `add_joints` default passive stiffness 10.0, damping 0.5, armature 1e-6. Actuator types motor/position/velocity/intvelocity, with default forcerange (−30, 30). — [base_fly.py](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/compose/fly/base_fly.py)
  - Contact defaults: sliding friction 1.0, torsional 0.02, rolling 1e-4, solref time constant 2e-4 (MuJoCo default 0.02), solimp dmin/dmax 0.98/0.99, width 1e-5, power 3.0, margin 1e-3. — [physics API](https://neuromechfly.org/api_reference/flygym/compose/physics/)

#### FlyMimic: first muscle-actuated fly leg (Özdil, Ning, Phelps, Wang-Chen, Elisha, Blanke, Ijspeert, Ramdya; arXiv:2509.06426, Sept 2025; ICLR 2026, CONF)
- Described as the "first 3D, data-driven musculoskeletal model of Drosophila legs", implemented in OpenSim and MuJoCo. It uses Hill-type muscles built from high-resolution X-ray data of several fixed specimens (Kuan et al. 2020 plus custom scans) and has 15 muscle-tendon units (MTUs) per foreleg: 7 in the thorax, 6 in the coxa and 2 in the femur. These span ThC, CTr (3 DoF) and FTi. The model captures "12 of the 19 muscle groups"; tibia muscles (incomplete data) and trochanter muscles (unclear function) are excluded. — [arXiv html](https://arxiv.org/html/2509.06426v1); [ICLR listing](https://mlanthology.org/iclr/2026/ozdil2026iclr-musculoskeletal/)
- Model: Millard 2013 Hill-type (contractile, passive parallel elastic and series elastic elements) with rigid tendons. — [arXiv](https://arxiv.org/html/2509.06426v1)
  - F_max = PCSA × 28 mN/mm², chosen between Drosophila jump muscle (37 mN/mm²) and flight muscle (9 mN/mm²).
  - Optimal fibre length and tendon slack length come from CT, scaled 0.8–1.2×.
  - Pennation is set to 0.
  - v_max is estimated from X-ray video of contraction, scaled 0.4–2.4×.
  - Activation and deactivation time constants are fixed at OpenSim defaults.
- Fitting: NSGA-II with 200 individuals × 40 generations, fit across antennal grooming and walking to avoid overfitting. Free parameters: F_max scale 0.3–3×, v_max scale, length ratios, and insertion points within a 5–10 µm cube. About 8 h per 3-DoF joint and about 20 h for the full foreleg. — [arXiv](https://arxiv.org/html/2509.06426v1)
- Converted to MuJoCo with MyoConverter; physics 10 kHz, control 500 Hz. Tested passive stiffness, damping and armature: "combination of stiffness and damping yields the fastest learning and highest performance". — [arXiv](https://arxiv.org/html/2509.06426v1)
- PPO imitation of tethered ball-walking and grooming (5 cameras, DeepLabCut + Anipose, 100 Hz interpolated to 500 Hz) took about 96 h for the 7-DoF / 15-MTU leg. In the synergy analysis, three NMF primitives explain >90% of the variance. — [arXiv](https://arxiv.org/html/2509.06426v1)
- As shipped in FlyGym 2.1 (`best_combined_arm_damping_stiff_cvt3.xml`):
  - 73 bodies; 15 MuJoCo `muscle` actuators acting through spatial tendons; left-front leg only. RF is locked, LM/LH are passive, and the thorax is tethered.
  - Action is 15 activations in [0, 1]. The bundled mocap clip is 225 frames at 500 Hz. The docs note there are no per-leg contact sensors.
  - Source: [tutorial](https://neuromechfly.org/tutorials/6_muscle_imitation/)
- Parameters read from the shipped XML (F0 in model units, i.e. µN given g–mm–s):
  - F0 ranges from 10.6 (sternal anterior rotator) to 303.9 (tibia extensor); tibia flexor 68.1.
  - `vmax` = 10 L0/s, `fvmax` 1.4, `lmin`/`lmax` 0/2.
  - Joint stiffness 0.4, damping 0.02, armature 0.0005.
  - Activation and deactivation time constants (`dynprm`) = 0.0001 s / 0.0004 s. That is 0.1–0.4 ms, 100× faster than MuJoCo's defaults of 10/40 ms. This conflicts with the paper's "default OpenSim" statement and is far faster than measured twitch kinetics (see §2).
  - Source: [XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml)
- Muscle names in the XML map directly onto connectome MN target annotations: tergopleural promotor a/b, pleural promotor, pleural remotor & abductor, sternal anterior rotator, sternal posterior rotator, sternal adductor, trochanter flexor a/b, accessory trochanter flexor, trochanter extensor, sterno-tergo-trochanter extensor a/b, tibia flexor, tibia extensor. — [XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml)

#### flybody (Vaxenburg, Siwanowicz, Merel, Robie, … Tassa, Turaga; Nature 643:1312–1320, 2025; PR)
- Body: a female D. melanogaster reconstructed from confocal images of disassembled, bleached, Congo-Red-stained body parts, with 67 body components.
  - 66 joint locations give 102 DoFs, modelled as 1–3 hinge joints per biological joint.
  - Legs have coxa, femur, tibia, 4 tarsal segments and claws (6 × 8 segments). Proboscis has 4 segments, abdomen 7 segments, plus antennae, wings and halteres.
  - Masses: total 0.983 mg; head 0.15; thorax 0.34; abdomen 0.38; each leg 0.0162; each wing 0.008 mg. Length 0.297 cm, span 0.604 cm.
  - Source: [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Actuators: position actuators on all non-wing joints and torque actuators on the wings; tarsi and abdomen are each driven by one MuJoCo tendon. Adhesion actuators sit on the tarsal tips and the labrum and are now a general MuJoCo feature. The Methods report maximum adhesion per leg as about one body weight (0.96 dyn). The authors "caution against interpreting the control signals sent to these actuators as biologically meaningful". — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Fluid model: a stateless, quasi-steady approximation on ellipsoids (added mass, viscous drag, viscous resistance, Magnus lift, Kutta lift). Coefficients were tuned for stable hover, and flight stays stable under 20% coefficient variation. Kutta lift and viscous drag dominate. The model captures only time-averaged turbulence and has no wing flexibility. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Control:
  - Walking controls 59 DoFs versus 12 for flight.
  - Flight uses a wing-beat pattern generator (WPG): a baseline pattern from hovering D. melanogaster at 218 Hz, with frequency modulated within ±10%. Real flies vary wingbeat frequency by up to 40 Hz; the model only by 0–10 Hz.
  - Timesteps: flight 0.05 ms physics / 0.2 ms control; walking 2 ms control.
  - RL is DMPO (distributional MPO) on Ray: walking ~10⁹ simulation steps and ~10⁸ updates; flight ~10⁸ steps and ~10⁷ updates.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Speed on one CPU core: 421.5 ms of wall time per 10 ms of flight and 68.65 ms per 10 ms of walking. MuJoCo alone accounts for 55.5 ms (flight) and 23.2 ms (walking). — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Validation:
  - Flight CoM error median 0.25 mm, orientation error <5°.
  - Walking CoM error median "0.4 cm" (larger than a body length, so check the figure), orientation error 4°.
  - At least 3 legs in stance: 3.1 legs at 4 cm/s and 3.9 at 1 cm/s.
  - Vision: 32 × 32-pixel eye cameras with a 150° field of view and 4.6° inter-ommatidial angle, used for bumps and trench flight tasks.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Limitations: simplified neck, wing hinge and ThC; no muscles; degenerate left-right asymmetry in adhesion when climbing; adhesion not in the reward because "we lacked direct leg adhesion measurements". The anatomical dataset shows muscle origins, insertions and hair-plate locations "which can be incorporated into future model iterations". — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Code and data: [TuragaLab/flybody](https://github.com/TuragaLab/flybody) (Apache-2.0; walking-imitation action space 59-dim); [Janelia figshare datasets](https://janelia.figshare.com/articles/dataset/MuJoCo_fruit_fly_body_model_datasets_supporting_Whole-body_simulation_of_realistic_fruit_fly_locomotion_with_deep_reinforcement_learning_/25309105)

#### Other 2025–2026 successors and connectome-body couplings
- Eon Systems, 10 Mar 2026 (BLOG, not peer-reviewed):
  - Brain: the FlyWire LIF model of Shiu et al. (~140k neurons, ~50M synapses), with flyvis feeding vision. Coupled to NeuroMechFly in MuJoCo.
  - Outputs go through "a small number of descending outputs": DNa01/DNa02 for steering, oDN1 for forward velocity, antennal DNs for grooming and MN9 for proboscis. These drive controllers "trained by imitation learning".
  - Brain and body sync every 15 ms. Acknowledged limitation: "many of the mappings between brain and body were chosen by hand".
  - Source: [Eon](https://eon.systems/updates/embodied-brain-emulation)
- FlyGM (Jin, Zhu, Zhang, Sui; arXiv:2602.17997, Feb 2026; PP): the FlyWire FAFB v783 graph is used as a policy network on flybody. It is partitioned into afferent, intrinsic and efferent neurons, with efferent states decoded into actions. Trained by imitation of an MLP expert, then PPO. It achieves gait initiation, walking, turning and flight. Turning error was 8.29 ± 0.21 versus 13.55 for degree-preserving rewired graphs and 125.36 for random graphs. It is slower and uses more memory than MLPs. — [arXiv](https://arxiv.org/html/2602.17997v1)
- Pugliese et al. (bioRxiv Sept 2025; PP): rate models of four VNC connectomes (MANC, FANC, BANC and the male CNS, "mCNS"). The MANC front-leg network has 4,604 neurons: 1,318 DNs, 144 leg MNs and 3,142 premotor neurons. DNg100 and DNb08 drive rhythmic leg MN activity, and a 3-neuron core (1 inhibitory, 2 excitatory) is necessary and sufficient. A mean τ ≈ 20 ms reproduces the ~7–15 Hz stepping frequency. Rhythms survive weight noise at connectome-error scale, and stronger DNg100 drive gives faster stepping (confirmed with optogenetics). — [PMC13142387](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/); [code](https://github.com/smpuglie/Pugliese_cpg_2025)
- Karashchuk et al. (eLife 2025; PR): a layered 3-D kinematic/dynamical model of walking. A per-leg optimal controller runs at 600 Hz and a learned trajectory generator at 300 Hz, trained on Anipose treadmill kinematics. It uses a 10 ms sensory delay and a 30 ms motor delay taken from electrophysiology. Mean joint-angle error is <6° over 500 bouts. — [eLife](https://doi.org/10.7554/eLife.99005); [code](https://github.com/lambdaloop/layered-walking/)
- MIMIC-MJX (Zhang, … Pereira; arXiv:2511.20532, v. Aug 2026; PP): GPU (MJX) imitation-learning framework supporting "rat, fly, mouse arm, worm, and stick insect", with repos stac-mjx and track-mjx. — [project page](https://mimic-mjx.talmolab.org); [arXiv](https://arxiv.org/abs/2511.20532)
- Özdil et al. grooming (bioRxiv Dec 2024; PP): replays antennal grooming in NeuroMechFly and builds an antennal-grooming network from the brain connectome. A simulated activation screen finds recurrent excitation plus broadcast inhibition motifs that coordinate the head, antennae and forelegs. — [Europe PMC abstract](https://doi.org/10.1101/2024.12.17.628844)
- Review (Wang-Chen & Ramdya, arXiv:2601.08056 v4, 20 Jul 2026; PP):
  - Fly body models are "rigid bodies" lacking "detailed sensory organs and muscle models".
  - Parameters that represent biology (joint stiffness, muscle properties, connections) "should not be tuned simply to improve the simulation".
  - Cites Hill-type numerical instability (Yeo et al. 2023) and MuJoCo Warp as enabling tech.
  - Source: [arXiv](https://arxiv.org/abs/2601.08056)

### Inferences
- Inference: the likely stack for the MaleCNS project is FlyGym 2.x plus the NeuroMechFly body for walking and vision. The FlyMimic MSK leg is the entry point for a real MN→muscle→joint pathway. The flybody model, now loadable inside FlyGym 2.1, covers flight, abdomen and proboscis. All muscle and flybody-in-FlyGym features are labelled experimental.
- Inference (derived from flybody numbers): real-time factor on one core is about 0.15× for walking (10/68.65) and about 0.024× for flight (10/421.5). MuJoCo alone is about 0.43× for walking and 0.18× for flight at 102 DoF. FlyGym 2's "~2× real-time" CPU and "~60× real-time" GPU figures are aggregate throughput claims. The GPU number comes from batching many identical worlds, so it will not speed up one closed-loop fly coupled to one spiking CNS. For a single fly, the spiking network, not physics, is probably the bottleneck.
- Inference: both bodies default to 0.05–0.1 ms physics steps (1e-4 s in FlyGym 2; 0.05 ms for flybody flight). That matches typical spiking-network dt, so lockstep coupling at ≤0.1–0.2 ms is feasible. Eon's 15 ms brain–body sync is coarse compared with muscle twitch dynamics (~8.5 ms to half-max force; §2).
- Inference: since every whole-fly model uses position actuators, "motor neuron spikes → joint position targets" is the current de facto shortcut. Replacing it requires a force/torque actuation mode plus a muscle layer, and neither flybody nor NeuroMechFly v2 validated one against physiology.

### Gaps
- No peer-reviewed whole-body muscle-actuated fly model exists as of September 2026. FlyMimic covers only the left front leg's proximal joints, and it is a conference paper plus experimental software.
- I could not verify NeuroMechFly v1's total DoF count from the primary text, or the benchmark conditions behind FlyGym 2's "2×/60× real-time" claims.
- I found no report of a connectome-driven body whose motor neurons (as opposed to DNs or learned decoders) drive actuators.
- I found no published flybody GPU (MJX/Warp) port with benchmark numbers, beyond FlyGym 2.1 integrating the flybody model.

## 2. Leg muscles: anatomy, motor-neuron innervation maps, recruitment, twitch kinetics, muscle mechanics, passive joint properties, exoskeleton and tarsal adhesion

### Takeaway
Leg MN→muscle mapping is now connectome-grade for the front leg. FANC gives 69 left-T1 MNs mapped to 18 muscles, and MANC assigns muscle targets to T1 MNs directly and to T2/T3 MNs by serial homology. The tibia flexor pool is the only one with good physiology: a size-principle gradient where the slow MN gives <0.1 µN per spike and the fast MN about 10 µN (about body weight), with half-max force about 8.5 ms after a fast spike. Almost everything else a Hill model needs is unmeasured for Drosophila leg muscles and has to be estimated from anatomy (X-ray PCSA, attachment points) or borrowed from the jump muscle. That includes force–length and force–velocity curves, tendon compliance, activation dynamics for most muscles, and moment arms. Passive joint torques were measured at multiple joints in 2025: they are linear springs, larger than gravitational torque on the leg, and about 70× too weak to support the body. Drosophila tarsal adhesion forces are unmeasured.

### Cited Findings

#### Muscle anatomy and counts
- Classic count: "The leg of the fruit fly … contains 14 muscles which are innervated by just 53 motor neurons" (citing Baek & Mann 2009, Brierley et al. 2012, Maniates-Selvin et al. 2020, Soler et al. 2004). — [Azevedo et al. 2020, eLife](https://elifesciences.org/articles/56754)
- Soler et al. 2004 described all adult leg muscles and tendons, including internal string-like tendons within segments; the muscles are multi-fibre. — [Development](https://doi.org/10.1242/dev.01527)
- FANC (connectome of a female adult nerve cord) mapped "all 69 left T1 MNs to 18 target muscles" using EM plus genetic driver lines plus X-ray holographic nanotomography (XNH) of the front leg. The right T1 has 70; the extra cell looks like a second tarsus levator MN. — [Azevedo et al. 2024, Nature 631:360](https://www.nature.com/articles/s41586-024-07389-x) (PMC11348827)
- FANC details:
  - The trochanter flexor has 8 MNs: 5 to the anterior fibres via ProAN and 3 to the posterior fibres via VProN.
  - The femur reductor, in the trochanter, has 6 MNs. So the trochanter and femur are not simply "functionally fused".
  - Tibia extensor: 2 MNs (FETi and SETi analogues).
  - Polyneuronal innervation occurs in the long tendon muscle (LTM), the proximal trochanter-flexor fibres and the femur reductor.
  - LTM fibres originate in the femur (ltm2) and tibia (ltm1) and insert on the long tendon (retractor unguis) that runs to the claw.
  - The XNH volume gives fibre counts, origins and cuticle attachments for each muscle.
  - Source: [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- XNH imaging of a whole adult leg at sub-100-nm resolution allowed tracing of individual motor axons from muscle to CNS. — [Kuan et al. 2020, Nat Neurosci](https://doi.org/10.1038/s41593-020-0704-9)
- MANC (connectome of the male adult nerve cord):
  - 733 MNs in 168 types.
  - 392 leg MNs: 142 T1, 119 T2, 131 T3, i.e. about 71, 60 and 65 per leg.
  - All 142 T1 MNs were identified by NBLAST matching to FANC. 198 of the 252 T2/T3 MNs were "putatively" identified via serial homology.
  - Reconstruction issues affect about 49% of leg MNs.
  - Source: [Cheong, Eichler, Stürner et al., eLife](https://elifesciences.org/articles/96084) (PMC13384506)
- Lineages: over two-thirds of leg MNs come from Lin A (Lin 15, 28 MNs) and Lin B (Lin 24, 7 MNs). Lin B MNs target the coxa (4), trochanter (2) and femur (1). — [Enriquez et al. 2015, Neuron](https://doi.org/10.1016/j.neuron.2015.04.011)
- Most leg MNs are born postembryonically from 5 neuroblasts per hemineuromere. Two lineages make only MNs, and there is a myotopic map between dendrites and muscles. — [Brierley et al. 2012, J Comp Neurol](https://doi.org/10.1002/cne.23003)
- About 50 MNs innervate 14 muscles per leg; they come from at least 11 lineages, and birth time plus lineage predict targeting. — [Baek & Mann 2009, J Neurosci](https://www.jneurosci.org/content/29/21/6904) (via [Venkatasubramanian et al. 2019](https://elifesciences.org/articles/42692))
- Contradiction (counts): 14 muscles / ~50–53 MNs (light microscopy era) versus 18 target muscles / 69–70 MNs (FANC T1) versus about 60–71 MNs per leg (MANC). Pugliese uses 144 T1 leg MNs in MANC against Cheong's 142. The differences reflect muscle splitting (e.g. anterior/posterior trochanter flexor, femur reductor, LTM1/2), EM completeness, sex and dataset. — sources above

#### Leg muscles by joint (naming used in FANC/MANC and the FlyMimic XML)
- Thorax→coxa (ThC; extrinsic muscles in the thorax): tergopleural promotor, pleural promotor, pleural remotor & abductor, sternal anterior rotator, sternal posterior rotator, sternal adductor. — [FlyMimic XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml); MN group example "Sternal rotator anterior MN" in [Cheong et al.](https://elifesciences.org/articles/96084)
- Coxa→trochanter (CTr):
  - Trochanter flexor (a/b), accessory trochanter flexor, trochanter extensor, sterno-(tergo-)trochanter extensor. — [FlyMimic XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml)
  - In T2 only, the large tergotrochanter "jump" muscle (TTM), with 3 candidate MNs. — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- Trochanter→femur: femur reductor (6 MNs). — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- Femur→tibia (FTi): tibia extensor (2 MNs), tibia flexor (about 15 MNs) plus accessory tibia flexor, and ltm2. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754); [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- Tibia→tarsus and claw: tibial muscles including the tarsus levator, plus ltm1 on the long tendon to the claw. Tibia muscles are not in FlyMimic. — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x); [Özdil et al.](https://arxiv.org/html/2509.06426v1)

#### Recruitment (size principle) and premotor wiring
- Tibia flexor MNs form a graded pool (fast, intermediate, slow). Input resistance is 150 MΩ fast, 300 MΩ intermediate and 700 MΩ slow. Recruitment normally goes slow→fast, but violations occur, and each class receives different proprioceptive feedback. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754)
- "The slow tibia flexor motor neuron … is one of 8–9 motor neurons that innervates tibia flexor muscle fibers located at the distal tip of the femur." Slow MNs fire tonically to hold resting tension: blocking with MLA cut resting force by about 1.5 µN (~15% of body weight). A 1° tibia change significantly changes slow-MN firing. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754)
- Premotor connectome: 69 leg MNs receive 212,190 synapses from 1,546 premotor neurons; 29 wing and thorax MNs receive 144,668 synapses from 1,784 premotor neurons. MN surface area varies more than 40-fold, and leg MNs carry about 0.45 synapses/µm².
  - In leg modules, premotor synaptic weights are "proportional to the size of their target MNs", which is a circuit basis for recruitment order. Wing premotor networks lack this proportionality.
  - Source: [Lesser et al. 2024, Nature](https://www.nature.com/articles/s41586-024-07600-z) (PMC11356479)
- The escape-related GFC4 interneurons synapse only onto the largest trochanter–femur and tibia flexor MNs. This explains recruitment-order violations in which fast MNs fire first. — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)

#### Force per spike and twitch kinetics (only direct Drosophila leg data)
- "Slow motor neurons produce <0.1 µN per spike, while fast motor neurons produce ~10 µN per spike, approximately equal to the fly's weight." Force regimes span three orders of magnitude across MN classes. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754)
  - Correction: one search aggregator wrote "mN". The primary text says µN.
- Maximum tibia-tip force is about 100 µN (the probe saturated near 85 µN), with force changes of about 1.3 mN/s. Fly weight is about 10 µN, so the FTi joint can lift about 10× body weight. Probe spring constant 0.22 µN/µm. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754)
- Kinetics: a single fast or intermediate spike reaches half-max force in about 8.5 ms. Slow-MN rate changes act gradually and do not peak within 500 ms. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754); data on [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.76hdr7stb)
- Delays used in fly locomotion modelling: 10 ms sensory and 30 ms motor, "based on values measured experimentally with electrophysiology" (Tuthill & Wilson 2016; Azevedo et al. 2020). — [Karashchuk et al. 2025](https://doi.org/10.7554/eLife.99005)
- When all MNs are silenced in a standing fly, the fall is consistent with active force decaying with τ ≈ 100 ms. — [Wang et al. 2025 bioRxiv](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/)

#### Muscle mechanics data (force–length, force–velocity, specific tension)
- The Drosophila jump muscle (TDT, a mesothoracic leg muscle) is the only leg-type muscle with force–velocity data. At 15 °C: V_slack 6.1 ± 0.3 muscle lengths/s, isometric tension 37 ± 3 mN/mm², maximum power at 26% of isometric tension, "equivalent to a very fast vertebrate muscle". — [Eldred et al. 2010, Biophys J](https://www.sciencedirect.com/science/article/pii/S0006349509061414)
- Jump-muscle myofibrils (2026):
  - Net active tension 19.8 ± 10.5 mN/mm²; activation rate 8.2 ± 4.0 s⁻¹.
  - Relaxation is biphasic: a slow linear phase of 75.6 ± 21.1 ms, then exponential decay at 19.7 ± 9.6 s⁻¹.
  - Source: [Fenwick et al. 2026, Biophys Rep](https://pmc.ncbi.nlm.nih.gov/articles/PMC13316580/)
- FlyMimic assumes 28 mN/mm² for leg muscles, between jump (37) and flight (9) muscle. Its v_max comes from X-ray video. Its force–length/velocity curves are MuJoCo/OpenSim generic shapes, not Drosophila measurements. — [Özdil et al.](https://arxiv.org/html/2509.06426v1); [XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml)
- Hill-type models are known to be numerically unstable in some regimes. — [Yeo et al. 2023, cited in Wang-Chen & Ramdya 2026](https://arxiv.org/abs/2601.08056)

#### Passive joint properties
- Wang et al. (bioRxiv 2025; PP) silenced all glutamatergic MNs with VGlut-Gal4 > GtACR1, rotated the body to vary gravitational torque, and inferred passive torque at four DoFs per leg.
  - Passive torque is "well approximated by a linear spring". It is much larger than the gravitational torque on the leg, but "seventy times smaller than necessary to support the weight of the animal". A fly falls when its MNs are silenced. Stiffness varies across flies and legs, and metathoracic legs are stiffer.
  - Source: [PMC12324252](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/)
- Median stiffness values (Table 1), by leg and axis (Lev-Dep, Ret-Pro, Ext-Flex, Pro-sup):
  - Prothoracic: 1.5e-8, 1.9e-9, 1.7e-8, 1.5e-8.
  - Mesothoracic: 8.6e-9, 1.1e-8, 2.5e-8, 1e-8.
  - Metathoracic: 2.7e-8, 5.6e-8, 1.7e-8, 4.7e-8.
  - Contradiction (units): the table header says "mN/°" but the Discussion says the range is "8X10−9 Nm/° … 6X10−8 Nm/°". Read literally as N·m/°, those values would easily support the body weight, which contradicts the paper's own 70× conclusion. Recompute from the figures before use.
  - Source: [PMC12324252](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/)
- In insects generally, passive joint forces are tuned to limb use and can drive movements without motor activity. — [Ache & Matheson 2013, Curr Biol](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3739007/)
- Model defaults are unconstrained and differ by orders of magnitude: FlyGym 2 `add_joints` stiffness 10, damping 0.5, armature 1e-6, versus FlyMimic stiffness 0.4, damping 0.02, armature 5e-4 (both in model units). — [base_fly.py](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/compose/fly/base_fly.py); [FlyMimic XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml)

#### Hill-type and other muscle models used for flies
- Ekeberg antagonistic spring-damper torque model: NeuroMechFly v1. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full)
- Millard 2013 Hill model (OpenSim) converted to MuJoCo muscle actuators: FlyMimic. — [Özdil et al.](https://arxiv.org/html/2509.06426v1)
- Reduced-order validation model: an angular and radial spring-loaded inverted pendulum (ARSLIP). Flies use a tripod gait across all walking speeds, and effective leg springs stiffen with speed through tripod geometry rather than individual-leg stiffness. — [Chun et al. 2021, eLife](https://doi.org/10.7554/eLife.65878)

#### Exoskeleton and tarsal adhesion
- Insect adhesive pads can generate normal forces over 100× body weight. Drosophila liftoff mechanisms are unknown, so NeuroMechFly toggles adhesion by gait phase. — [NMF v2 postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- flybody lacked "direct leg adhesion measurements" and caps adhesion at about one body weight per leg. — [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Drosophila pulvilli morphology (length, setae number, spatula width) is affected in climbing mutants. In wild-type footprints the claws do not touch smooth ground. — [JEB 2015, Su(z)2 adhesive pad paper](https://journals.biologists.com/jeb/article/218/8/1159/14480/Adhesive-pad-differentiation-in-Drosophila)
- High-speed video of flies (a larger fly species, not Drosophila; species not re-verified) shows four pulvillus detachment modes (pulling, shifting, twisting, lifting); only lifting uses the claws. — [Niederegger & Gorb 2003, J Insect Physiol](https://pubmed.ncbi.nlm.nih.gov/12804721/)
- In large insects, passive femur–tibia forces arise from both cuticle elasticity and muscle. — [Wang et al. 2025, introduction](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/)

### Inferences
- Inference: the connectome side is ready for a muscle layer. MaleCNS includes the VNC, and MANC's T1/T2/T3 MN→muscle annotations (from FANC matching and serial sets) can be carried over. The body side can currently accept only the 15 FlyMimic MTUs, and only for one leg. A practical first mapping: group MaleCNS T1 MN types by annotated target muscle, then assign groups to the FlyMimic tendons. For example, all tibia flexor MNs (fast, intermediate, slow) sum into `LFTibia_flex`, and the anterior and posterior trochanter flexor MNs go to `trochanter_flexor_a/b`. Leave unmodelled targets (femur reductor, tibial and tarsal muscles, LTM) as passive or position-controlled DoFs.
- Inference: a minimal spike→force model per MN could be a twitch kernel with rise to half-max around 8.5 ms (fast and intermediate), scaled by class-specific gain (~10 µN fast, <0.1 µN slow, measured at the tibia tip) and passed through a summation/saturation nonlinearity. That can be converted to a normalized Hill activation by calibrating against Azevedo 2020's force-vs-firing-rate curves and the ~100 µN maximum tip force. The shipped FlyMimic activation dynamics (0.1/0.4 ms) are too fast to reproduce those kinetics and should be refit.
- Inference: the tibia extensor F0 (303.9) exceeding the flexor F0 (68.1) in FlyMimic is surprising. The flexor pool has about 15 MNs and generates the large escape forces. This may be an optimization artefact of fitting to kinematics alone, and it could be checked against Azevedo 2020 forces.
- Inference: Lesser et al.'s finding that premotor weights scale with MN size means a size-principle recruitment order should emerge automatically in a connectome-driven spiking model, provided MN input resistance or size is represented. Uniform MN parameters would lose it.

### Gaps
- No Drosophila leg-muscle force–length curves; no force–velocity curves except the TDT; no tendon or apodeme stiffness; no moment arms other than those implied by XNH-based muscle paths; no activation or deactivation time constants except tibia-flexor twitch data and TDT myofibrils; no per-MN force or twitch for any muscle except the tibia flexor.
- No Drosophila tarsal adhesion or friction force measurements; no cuticle or exoskeleton material properties specific to Drosophila legs.
- No passive damping measurements. Passive stiffness units are ambiguous in the only Drosophila dataset (a preprint).
- I did not retrieve stick-insect Hill parameter sets (e.g. Guschlbauer et al. 2007; Blümel et al. 2012) in this pass. They are the usual proxies.

## 3. Flight: asynchronous indirect flight muscles, direct steering muscles and their motor neurons, wing-hinge mechanics, aerodynamic models and haltere feedback

### Takeaway
Flight power comes from stretch-activated, asynchronous indirect flight muscles (IFMs): per side, the dorsal longitudinal muscle (DLM) has 6 fibres driven by 5 MNs, and three dorsoventral muscles (DVM1–3) have 7 fibres driven by 7 MNs. They beat at 200–250 Hz, while the MNs fire far below wingbeat frequency and only set [Ca²⁺] and thus power. Steering uses 12 direct muscles on 4 hinge sclerites, each sclerite having large phasic and small tonic muscles, one MN per muscle for most, plus tension and indirect control muscles (tp, ps, TTM). FANC counts 29 wing and thorax MNs per side and MANC 26 wing MNs. The key data-driven hinge model maps steering-muscle GCaMP to wing kinematics (Melis et al. 2024: 72,219 wingbeats). flybody's quasi-steady ellipsoid aerodynamics plus RL gives body-level flight but without muscles. Halteres carry hundreds of campaniform sensilla, make fast electrical synapses onto the b1 MN, and have their own 7 MN pairs.

### Cited Findings

#### Indirect (power) flight muscles
- 13 large fibres per side power flight indirectly by causing "the thorax to resonate at high frequencies". They form 4 muscles per side:
  - DLM with 6 fibres (DLM1–6), innervated by 5 MNs.
  - DVM1 with 3 fibres and 3 MNs, DVM2 with 2 fibres and 2 MNs, DVM3 with 2 fibres and 2 MNs.
  - DLM MNs are the only MNs with presynaptic sites in the VNC. Gap junctions offset their spike timing during flight.
  - Source: [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- DLM and DVM form "an antagonistic oscillatory system that produces wing beat frequencies of 200–250 Hz through reciprocal stretch activation". — [Teoh et al. 2025 bioRxiv (tp1)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12637562/)
- Power control: A-IFM MNs "fire at a rate much slower than contraction frequency". Power "rises and falls in concert with the firing frequency of all A-IFM fibers and cannot be explained by differential recruitment", and [Ca²⁺] rises in proportion to firing rate. — [Gordon & Dickinson 2006, PNAS](https://www.pnas.org/doi/full/10.1073/pnas.0510109103)
  - A review reports calcium–power linearity with R² ≈ 0.95 (DLM) to 0.97 (DVM) over about 20–120 W/kg flight-muscle mass, and flight-muscle efficiency of about 5–20%. — [Lehmann & Bartussek 2017, J Comp Physiol A](https://pmc.ncbi.nlm.nih.gov/articles/PMC5263198/)
- A modelling paradox: D. melanogaster flight apparently violates a derived condition for self-oscillation. The motor is "probably not resonant with respect to exoskeletal elasticity", and muscle elasticity dominates. — [Pons 2023, J R Soc Interface](https://doi.org/10.1098/rsif.2023.0421)
- The tergotrochanter (TTM, T2 jump muscle) "is also thought to initiate the first cycle of mechanical oscillation in the power muscles". — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
- Tension muscles (tp, ps) control thoracic stiffness and resonance and so indirectly modulate wingbeat amplitude. — [Cheong et al.](https://elifesciences.org/articles/96084)

#### Direct steering muscles and motor neurons
- The wing is controlled "using only a dozen pairs of muscles". Each of the 4 skeletal elements at the wing base has "large phasically active muscles capable of executing large changes and smaller tonically active muscles" for fine adjustment (GCaMP imaging of the full ensemble). — [Lindsay, Sustar & Dickinson 2017, Curr Biol](https://doi.org/10.1016/j.cub.2016.12.018)
  - Tonic: b1, b3, i2, iii3. Phasic: b2, i1, iii1, iii4, hg1–hg3 (via search summary of Lindsay 2017 and related work).
- Muscle and MN naming: power muscles DLM and DVM1–3; steering muscles basalar b1–b3, first axillary i1–i2, third axillary iii1, iii3, iii4, fourth axillary hg1–hg4; indirect control muscles tp, ps1, ps2, TTM. — [Cheong et al.](https://elifesciences.org/articles/96084)
  - Wing and thorax MNs: 29 per side in FANC. — [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x)
  - Wing MNs: 26 in MANC. — [Cheong et al.](https://elifesciences.org/articles/96084)
  - The difference probably reflects inclusion of TTM and other thorax MNs.
- Wing hinge model:
  - Dataset: 12 steering muscles imaged in 82 flies, giving 72,219 wingbeats from 485 sequences. Wings filmed at 15,000 fps; muscle calcium at about 100 fps, strobed at dorsal stroke reversal.
  - Kinematics: stroke (φ), deviation (θ), pitch (η) and deformation (ξ), each fit with Legendre polynomials (80 coefficients per wingbeat).
  - Models: a CNN predicts wing motion from a 13 × 9 matrix of muscle activity over 9 wingbeats. An encoder–decoder with a 5-D latent space (4 sclerites plus frequency) captures sclerite roles.
  - Validation: Robofly force measurements in mineral oil with a 6-DoF sensor. An MPC over muscle activity in a physics simulation reproduces saccades (90° yaw within 10 wingbeats).
  - Naming contradiction: the preprint uses iv1–iv4 for the fourth axillary muscles, which other papers call hg1–hg4. Phasic examples are b2, i1, iii1, iv1; tonic are b1, b3, i2, iii3, iv4.
  - Source: [Melis, Siwanowicz & Dickinson 2024, Nature 628:795](https://www.nature.com/articles/s41586-024-07293-4); [bioRxiv v3](https://www.biorxiv.org/content/10.1101/2023.06.29.547116v3.full)
- The basalar motor units b1 and b2 modulate the I and P terms, respectively, of a PI controller for pitch (Whitehead et al. 2022). tp1, an indirect tergopleural muscle, supplies the proportional gain for wing pitch-angle control during large pitch perturbations. A torsional-spring hinge model captures this, with tp1 shifting the wing rest angle. — [Teoh et al. 2025 bioRxiv](https://pmc.ncbi.nlm.nih.gov/articles/PMC12637562/)
- Hinge "gearbox" (radial stop – pleural wing process): ablating the PWP in freely flying Musca did not change amplitude modulation during yaw turns. This favours active neuromuscular control over passive gearbox engagement. — [Ghosh, Kumar & Sane 2026, JEB](https://doi.org/10.1242/jeb.250768)

#### Aerodynamic models and flight dynamics
- Insect lift comes from delayed stall (translation), rotational circulation and wake capture (stroke reversal). — [Dickinson, Lehmann & Sane 1999, Science](https://doi.org/10.1126/science.284.5422.1954)
- The standard quasi-steady blade-element approach builds on Sane & Dickinson 2002 (JEB, "The aerodynamic effects of wing rotation and a revised quasi-steady model of flapping flight"), which adds rotational terms. I found this only via search summaries and did not retrieve the paper or its coefficient equations. A later CFD-informed quasi-steady model that refines this approach: [CFD-informed quasi-steady model (PMC4918218)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4918218/)
- Flies turn with "surprisingly subtle modifications in wing motion", and "inertia, not friction, dominates the flight dynamics" during rapid turns (free-flight kinematics replayed on a robot). — [Fry, Sayaman & Dickinson 2003, Science](https://doi.org/10.1126/science.1081944)
- Evasive banked turns under looming reorient the flight path "within a few wingbeats". — [Muijres et al. 2014, Science](https://doi.org/10.1126/science.1248955)
- flybody's aerodynamics: a stateless quasi-steady ellipsoid model with coefficients tuned for hover, 218 Hz WPG, and 0.05 ms physics step. See §1. — [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Recent quasi-steady refinements exist; I found only titles: "Data-Driven Discovery and Formulation Refines the Quasi-Steady Model of Flapping-Wing Aerodynamics" (2025) and "Quasi-steady aerodynamics predicts the dynamics of flapping locomotion" (JFM 2025). — [arXiv 2508.18703](https://arxiv.org/pdf/2508.18703); [arXiv 2508.19899](https://arxiv.org/html/2508.19899v1)

#### Haltere feedback
- Haltere campaniform sensilla make "fast electrical synapses" with the b1 MN, which regulates stroke amplitude. The haltere acts as both a gyroscope and a clock for steering-muscle firing phase. — [Dickerson et al. 2019, Curr Biol](https://pmc.ncbi.nlm.nih.gov/articles/PMC7307274/) (via search summary)
- Robust haltere-mediated equilibrium reflexes: angular rotations elicit compensatory changes in stroke amplitude and frequency. — [Dickinson 1999, Phil Trans R Soc B](https://pmc.ncbi.nlm.nih.gov/articles/PMC1692594/)
- Haltere dorsal-field afferents are continuously active, modulated in closed loop, and recruited during saccades. The haltere's own steering muscles regulate haltere stroke amplitude to modulate campaniform input. — [Verbe et al. 2024, Curr Biol](https://doi.org/10.1016/j.cub.2024.06.066)
- Halteres contain "hundreds of strain-sensing campaniform sensilla". Wing and head reflex magnitudes fall linearly as more sensilla are silenced. — [Sharma et al. 2026, JEB](https://doi.org/10.1242/jeb.250431)
- Haltere MNs in MANC: 7 pairs, innervating hDVM (power) and the steering muscles hb1, hb2, hi1, hi2 and hiii1–3; three matches are putative. — [Cheong et al.](https://elifesciences.org/articles/96084)

### Inferences
- Inference: a biologically grounded flight actuator path would have three parts:
  - IFM MN spike rate → slow [Ca²⁺] state → wingbeat power or amplitude envelope, with no per-spike twitches.
  - Steering MN activity → sclerite or hinge state → wing kinematic deviations. This could use the Melis CNN or encoder–decoder as a learned hinge model feeding flybody's wing joints.
  - Haltere afferents → phase-locked b1 feedback.
- That would replace flybody's WPG plus policy torques. None of this is packaged in current open simulators.
- Inference: since IFMs are asynchronous, spiking-MN-to-force fidelity matters much less for power muscles than for steering muscles. Steering muscle spikes are phase-locked to the wingbeat, so they need sub-millisecond timing relative to the ~4.6 ms wingbeat period (1/218 Hz).

### Gaps
- No open, validated muscle-level model of the Drosophila wing hinge integrated in MuJoCo. I could not confirm whether Melis et al.'s simulation used flybody.
- I did not verify MN firing rates for IFMs or steering muscles, or Robofly quasi-steady coefficient equations, from primary text in this pass. A ~5 Hz IFM MN rate appears only in a search snippet.
- The wing MN counts (29 vs 26) and some haltere MN identities remain provisional.

## 4. Head/neck, proboscis, antennae, abdomen and courtship-song wing movements

### Takeaway
These systems are anatomically and genetically mapped but barely represented in body models:
- Neck: about 25 MN pairs, split between brain and VNC. Single-MN activation drives the head toward MN-specific poses through proprioceptive feedback.
- Proboscis: 16 muscles, with genetic access to the MNs of every muscle.
- Antenna: 4 scape–pedicel muscles.
- Abdomen: about 150 MANC MNs, mostly unidentified.
- Courtship song: uses mostly the flight motor. hg1 is needed for sine song and ps1 for a pulse feature, and the song circuit is two nested pathways.

flybody has proboscis and abdomen DoFs and labrum adhesion. NeuroMechFly v2 has neck and antenna DoFs but no feeding, abdomen or flight control. Neither has muscles for these systems.

### Cited Findings
- Neck: head movement is controlled by "about 25 pairs of neck motor neurons innervating predominantly thoracic neck muscles" in roll, pitch and yaw. — [commentary on Gorko et al. 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11362485/)
  - "Activity in a single motor neuron rotates the head in different directions, depending on the starting posture". The head converges toward an MN-specific pose. A feedback model explains this as MN drive interacting with proprioceptive feedback, and suppressing one proprioceptor class changes the convergence as predicted. — [Gorko et al. 2024, Nature](https://www.nature.com/articles/s41586-024-07222-5)
- In MANC, "12 pairs of likely neck MNs" were found, only three tentatively identified. "Neck MNs are split between those residing in the VNC and the brain", and 4 neck MNs run through the neck connective. — [Cheong et al.](https://elifesciences.org/articles/96084)
- NeuroMechFly v2 neck: the joint was re-placed and yaw and roll DoFs added. Head stabilization is learned from leg proprioception. — [NMF v2 postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Proboscis: 16 muscles, with split-GAL4 lines targeting the primary MNs of "every proboscis muscle". MN dendrites are in the subesophageal zone. The authors predict 8 muscles position the proboscis (reaching) and 8 pump. Segments are rostrum, haustellum and labella. — [McKellar et al. 2020, eLife](https://doi.org/10.7554/eLife.54978)
- Body models: flybody's proboscis has 4 segments and labrum adhesion actuators "to enable modelling of feeding and courtship behaviours". — [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
  - NeuroMechFly v2 does not implement feeding. — [NMF v2](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
  - Eon drove proboscis extension through MN9. — [Eon](https://eon.systems/updates/embodied-brain-emulation)
- Antennae: four muscles actively control the scape–pedicel joint; the funiculus and arista move passively. — [NMF v2 postprint](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf)
- Antennal grooming coordinates head, antennae and forelegs, without requiring proprioceptive feedback from the other parts. — [Özdil et al. 2024 bioRxiv](https://doi.org/10.1101/2024.12.17.628844)
- Abdomen:
  - MANC has about 150 abdominal MNs in serial groups (10 exit via the abdominal trunk nerve) that "remain unidentified". — [Cheong et al.](https://elifesciences.org/articles/96084)
  - flybody's 7 abdominal segments are coupled through one tendon actuator. — [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)
- Courtship song (flight motor reused):
  - Song and flight use distinct configurations of neuromuscular activity. Most, but not all, flight muscles and their MNs contribute to song and shape its acoustics. The flight command overrides song. — [O'Sullivan et al. 2018, Curr Biol](https://doi.org/10.1016/j.cub.2018.06.038)
  - The hg1 MN and the sexually dimorphic hg1 muscle are required for sine song; the ps1 MN is required for a pulse-song feature. — [Cell Reports 2013, "Motor Control of Drosophila Courtship Song"](https://www.sciencedirect.com/science/article/pii/S2211124713005627)
  - Male-specific TN1A interneurons drive hg1, a connection built by doublesex. — [Shirangi et al. 2016, Dev Cell](https://doi.org/10.1016/j.devcel.2016.05.012)
  - Mapped with the MANC connectome, the song circuit is "two nested feedforward pathways". The larger one produces pulse song and a subset produces sine song. — [Lillvis et al. 2024, Curr Biol](https://doi.org/10.1016/j.cub.2024.01.015)
- Song parameters:
  - Sine song is a tone burst of about 160 Hz; pulses are about 3 ms, single-cycle, at an inter-pulse interval of about 34 ms. — [Kyriacou & Hall 1982 (abstract via search)](https://www.sciencedirect.com/science/article/abs/pii/S0003347282801528)
  - Mean IPI is about 35 ms. — [Stern 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4071150/)
- New 3-D kinematics (preprint): "courting males coordinate both wings during song and modulate body pitch to track the female's vertical position". — [Ispizua, Abe et al. 2026 bioRxiv](https://www.biorxiv.org/content/10.64898/2026.05.03.722293v1)

### Inferences
- Inference: for a male CNS model, courtship song is a natural early target beyond walking, because the MN targets (hg1, ps1, other wing MNs) and premotor circuits (TN1A, nested pulse/sine pathways) are already annotated in MANC. But it needs flybody's wing DoFs plus a song-specific wing-motion model: unilateral or bilateral extension and vibration at about 160 Hz. The flight WPG does not produce this, and it has no muscle-level implementation.
- Inference: the neck is well suited to MN-level control even in position-actuated bodies. Gorko et al. show single-MN drive acts as a pose target within a proprioceptive loop, so a "MN population → head pose setpoint + proprioceptive feedback" layer is closer to biology than direct torque control.

### Gaps
- No neck-muscle count, force or kinetics data for Drosophila was retrieved. Brain-resident neck MNs are outside the VNC datasets, although MaleCNS should contain them.
- No abdominal muscle map or MN targets. No song-producing wing kinematics or muscle model exists in any public simulator.

## 5. Kinematics and physiology datasets for validation

### Takeaway
Validation data are plentiful for walking kinematics (tethered and free, 2-D and 3-D, some with Dryad releases) and growing for free 3-D whole-body behaviour and muscle calcium (2026 preprints). Flight has large free-flight and tethered wing-plus-muscle datasets. Direct force data are limited to tibia-tip forces and per-MN force regimes, passive joint torques, and robot-measured aerodynamic forces.

### Cited Findings
- DeepFly3D (Günel et al. 2019, eLife): tethered flies on a ball, 7 cameras. 38 3-D landmarks: 5 per leg (ThC, CTr, FTi, TiTa joints and pretarsus), 6 on the abdomen, 1 on each antenna. Trained on 37,000 frames (85% self-supervised). — [eLife](https://elifesciences.org/articles/48571); [code](https://github.com/NeLy-EPFL/DeepFly3D)
  - NeuroMechFly v1 replay used 100 fps. — [NMF v1](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full)
- Anipose (Karashchuk et al. 2021, Cell Reports): 3-D calibration (ChArUco), filters and triangulation. Fly middle legs rotate the coxa and femur; front and hind legs mainly flex the femur–tibia joint. — [Cell Reports](https://doi.org/10.1016/j.celrep.2021.109730); data on [Dryad](https://doi.org/10.5061/dryad.nzs7h44s4)
- DeAngelis, Zavatone-Veth & Clark 2019 (eLife): freely walking flies filmed from below at 150 fps. Forward speeds span −1.3 to 30.4 mm/s (2.5–97.5 percentiles), with peaks at 0 and ~17.5 mm/s. The 3-, 4- and 5-feet-down configurations peak at 24, 13 and 7 mm/s. — [eLife](https://doi.org/10.7554/eLife.46409); data on [Dryad](https://doi.org/10.5061/dryad.3p9h20r)
- Mendes et al. 2013 (eLife, FlyWalker): 71 wild-type videos with mean speeds of 7.2–44.7 mm/s, most often 28 mm/s, and ~20 mm/s underrepresented. Blocking leg proprioception degrades step precision but not tripod coordination. — [eLife](https://doi.org/10.7554/eLife.00231)
- Chun, Biswas & Bhandawat 2021 (eLife): tripod gait at all speeds, plus the ARSLIP mechanical model. — [eLife](https://doi.org/10.7554/eLife.65878); data on [Dryad](https://doi.org/10.5061/dryad.m63xsj41g)
- Pratt et al. 2024 (Curr Biol): miniature linear and split-belt treadmills with 3-D kinematics. Linear-treadmill stepping resembles free walking, while tethered stepping is "subtly different". Middle legs adapt step distance on a split belt. — [Curr Biol](https://doi.org/10.1016/j.cub.2024.08.006)
- Stepping frequency in real walking flies is about 7–15 Hz (as cited for model validation). — [Pugliese et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/)
- Karashchuk et al. 2025: Anipose ball-walking joint angles used to train and validate a layered walking model. — [eLife](https://doi.org/10.7554/eLife.99005)
- Spotlight/PoseForge (Wang-Chen, Stimpfling, Azcorra, Ramdya; bioRxiv Mar 2026; PP): closed-loop tracking of untethered flies at 5–10 µm/pixel, 300–400 Hz behaviour and 30–60 Hz muscle calcium through intact cuticle (e.g. long tendon muscle responses to vibration). PoseForge uses NeuroMechFly-synthesized training data for single-view 3-D keypoints and segmentation, and behaviours are replayed in NeuroMechFly to infer limb forces. — [Europe PMC PPR1219815](https://doi.org/10.64898/2026.03.11.711180); [hardware](https://github.com/NeLy-EPFL/spotlight-hardware); [control code](https://github.com/NeLy-EPFL/spotlight-control)
- Whole-body 3-D kinematics (Ispizua, Abe et al.; UW/Janelia/Stowers; bioRxiv 4 May 2026; PP): 7 high-speed cameras at 800 fps and 50 landmarks, with biomechanical inverse-kinematics refinement. Covers walking and running ("grounded running across their full speed range, without transitioning between discrete gaits") and courtship. Open pipeline and dataset. — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.05.03.722293v1)
- flybody training data: about 16,000 walking snippets (about 80 min; female D. melanogaster at 150 fps, 13 APT keypoints, 0–4 cm/s). Flight: 272 free-flight trajectories (about 53 s; D. hydei at 7,500 fps, including saccades and evasions). — [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/); [figshare](https://janelia.figshare.com/articles/dataset/MuJoCo_fruit_fly_body_model_datasets_supporting_Whole-body_simulation_of_realistic_fruit_fly_locomotion_with_deep_reinforcement_learning_/25309105)
  - Consistency check: the training subsets (216 flight trajectories, about 43 s; about 13,000 walking snippets, about 64 min) are subsets of those totals.
- Flight wing kinematics plus muscle activity: Melis et al. 2024 (72,219 wingbeats, 12 muscles, 82 flies). — [Nature](https://www.nature.com/articles/s41586-024-07293-4)
  - Free-flight maneuvers: [Fry et al. 2003](https://doi.org/10.1126/science.1081944); [Muijres et al. 2014](https://doi.org/10.1126/science.1248955)
- Force and physiology validation targets:
  - Per-spike tibia forces, maximum tip force and MN recruitment. — [Azevedo et al. 2020](https://elifesciences.org/articles/56754)
  - Passive torque–angle springs and the ~100 ms force decay. — [Wang et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/)
  - Muscle calcium during walking and song. — [O'Sullivan et al. 2018](https://doi.org/10.1016/j.cub.2018.06.038); [Spotlight](https://doi.org/10.64898/2026.03.11.711180)

### Inferences
- Inference: a staged validation ladder for the MN→muscle→joint pathway:
  - (i) Single-muscle: reproduce per-spike tibia-tip force classes and ~8.5 ms kinetics from Azevedo 2020.
  - (ii) Passive: reproduce Wang 2025 rest angles and spring behaviour with MNs silenced, and the ~100 ms fall.
  - (iii) Leg kinematics: joint-angle trajectories against Anipose, Karashchuk, FlyMimic and Spotlight data.
  - (iv) Gait statistics: speed distributions, stance counts and phase relations against DeAngelis 2019, Mendes 2013, Pratt 2024 and Ispizua 2026.
  - (v) Closed-loop behaviour: turning and DN-evoked walking, e.g. DNg100 drive → stepping frequency, as in Pugliese 2025.
- Inference: tethered-ball kinematics (DeepFly3D, Anipose) differ subtly from free walking (Pratt 2024). NeuroMechFly v2 replaced tethered steps for this reason. Free-walking 3-D data (Ispizua 2026, Spotlight) are the better validation targets for an untethered body.

### Gaps
- There is no public dataset pairing MN spikes with muscle force and joint kinematics in behaving flies. The closest are Azevedo 2020 (single MNs, tethered, force probe) and the Spotlight calcium recordings.
- I did not retrieve formal gait-parameter tables (stance and swing duration versus speed) or the dataset sizes and licences of the 2026 preprints.

## 6. The minimal parameter set from motor neuron spikes to muscle force to joint torque, and which parameters are measured versus fitted

### Takeaway
A working chain needs five things:
1. An MN→muscle (MTU) map.
2. Per-MN spike→activation dynamics: twitch kinetics, electromechanical delay, summation.
3. Per-MTU force generation: F_max, force–length and force–velocity curves, passive elasticity, tendon.
4. Geometry: attachment points giving moment arms.
5. Joint and body mechanics: passive stiffness, damping and rest angle, segment inertia, contact and adhesion.

For the Drosophila leg, only the MN→muscle map (T1 fully, T2/T3 putatively), segment masses, joint DoFs and ranges, MTU paths (via X-ray), tibia-flexor per-spike forces and kinetics, and passive joint springs (preprint) are measured. Everything else is fitted or borrowed: F_max scaling, v_max, activation constants, force–length/velocity shapes, tendon compliance, damping, adhesion and friction.

### Cited Findings

| Stage / parameter | Status for Drosophila leg | Value(s) and source |
|---|---|---|
| MN identity → target muscle | Measured (T1: all 69–71 MNs; T2/T3: ~79% putative via serial homology) | [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x); [Cheong et al.](https://elifesciences.org/articles/96084) |
| Number of MNs per muscle (motor pool size) | Measured for T1 (e.g. tibia flexor ~15, trochanter flexor 8, femur reductor 6, tibia extensor 2) | [Azevedo et al. 2020](https://elifesciences.org/articles/56754); [Azevedo et al. 2024](https://www.nature.com/articles/s41586-024-07389-x) |
| MN size / input resistance (recruitment order) | Measured for tibia flexor (150/300/700 MΩ); MN morphology and synapse counts from EM for all T1 MNs | [Azevedo et al. 2020](https://elifesciences.org/articles/56754); [Lesser et al. 2024](https://www.nature.com/articles/s41586-024-07600-z) |
| Force per spike (motor-unit gain) | Measured only for tibia flexor classes: slow <0.1 µN, fast ~10 µN at tibia tip | [Azevedo et al. 2020](https://elifesciences.org/articles/56754) |
| Twitch time course | Measured only for tibia flexor: ~8.5 ms to half-max (fast/intermediate); slow MN effects build over >500 ms | [Azevedo et al. 2020](https://elifesciences.org/articles/56754) |
| Electromechanical / motor delay | Used value 30 ms (motor), 10 ms (sensory), from electrophysiology | [Karashchuk et al. 2025](https://doi.org/10.7554/eLife.99005) |
| Activation / deactivation time constants | Not measured in vivo for leg muscles. TDT myofibril activation 8.2 s⁻¹, relaxation slow phase 75.6 ms then 19.7 s⁻¹. Whole-body active-force decay τ ≈ 100 ms after MN silencing. FlyMimic XML uses 0.1/0.4 ms (fitted or converted; conflicts with the paper's "OpenSim default") | [Fenwick et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13316580/); [Wang et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/); [XML](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml) |
| Max isometric force F_max | Estimated: PCSA (X-ray) × assumed 28 mN/mm², then fitted ×0.3–3. Reference tensions: TDT 37 ± 3 mN/mm²; flight ~9 mN/mm²; TDT myofibrils 19.8 mN/mm² | [Özdil et al.](https://arxiv.org/html/2509.06426v1); [Eldred et al. 2010](https://www.sciencedirect.com/science/article/pii/S0006349509061414) |
| Optimal fibre length, tendon slack length | Anatomical (CT) then fitted ×0.8–1.2 | [Özdil et al.](https://arxiv.org/html/2509.06426v1) |
| Max shortening velocity | Estimated from X-ray video, fitted ×0.4–2.4. Only direct measurement is TDT V_slack 6.1 ML/s (15 °C). FlyMimic XML vmax = 10 L0/s | [Özdil et al.](https://arxiv.org/html/2509.06426v1); [Eldred et al. 2010](https://www.sciencedirect.com/science/article/pii/S0006349509061414) |
| Force–length, force–velocity curve shapes | Not measured (generic Millard/MuJoCo curves); TDT gives maximum power at 26% of isometric tension | [Özdil et al.](https://arxiv.org/html/2509.06426v1); [Eldred et al. 2010](https://www.sciencedirect.com/science/article/pii/S0006349509061414) |
| Pennation | Set to 0 (assumption) | [Özdil et al.](https://arxiv.org/html/2509.06426v1) |
| Tendon compliance | Assumed rigid | [Özdil et al.](https://arxiv.org/html/2509.06426v1) |
| Muscle paths / moment arms | Attachment points from X-ray (Kuan 2020 XNH plus others); insertion points fitted within 5–10 µm | [Özdil et al.](https://arxiv.org/html/2509.06426v1); [Kuan et al. 2020](https://doi.org/10.1038/s41593-020-0704-9) |
| Passive joint stiffness and rest angle | Measured (preprint) at 4 DoFs per leg: linear springs, ~7-fold range across joints (units ambiguous); model defaults vary 25× (FlyGym 2: 10; FlyMimic: 0.4) | [Wang et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/); [base_fly.py](https://github.com/NeLy-EPFL/flygym/blob/main/src/flygym/compose/fly/base_fly.py) |
| Passive damping, armature | Not measured; fitted or assumed (FlyGym 2: 0.5 / 1e-6; FlyMimic: 0.02 / 5e-4) | same |
| Segment masses / inertia | Measured masses (flybody: total 0.983 mg; leg 0.0162 mg); inertia computed assuming uniform density | [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/) |
| Joint DoFs and ranges | From 3-D kinematics (7 DoFs per leg incl. CTr roll) and inverse-kinematics fits to videography including grooming postures | [NMF v1](https://www.biorxiv.org/content/10.1101/2021.04.17.440214v1.full); [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/) |
| Ground friction, contact softness | Assumed (FlyGym 2: μ = 1.0, solref 2e-4 s, etc.) | [physics API](https://neuromechfly.org/api_reference/flygym/compose/physics/) |
| Tarsal adhesion | Not measured in Drosophila; modelled as switchable normal force ("40 mN" in NMF v2, units suspect; ~1 body weight per leg in flybody) | [NMF v2](https://www.epfl.ch/labs/ramdya-lab/wp-content/uploads/2024/08/NMF2_postprint.pdf); [flybody](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/) |

- The review cautions that "the distinction between parameters that serve purely to improve simulation realism and those that represent biological quantities" must be made explicitly. Joint stiffness and muscle properties "should not be tuned simply to improve the simulation". — [Wang-Chen & Ramdya 2026](https://arxiv.org/abs/2601.08056)
- Muscle redundancy (more muscles than DoFs) makes inverse inference of muscle activity ill-posed without criteria such as OpenSim static optimization, or dynamics-based imitation. — [Wang-Chen & Ramdya 2026](https://arxiv.org/abs/2601.08056)

### Inferences
- Inference: a minimal forward model that can be implemented now in FlyGym 2.1 for the left front leg:
  - For each MaleCNS T1 MN i, set target muscle m(i) from the MANC/FANC annotation. Set gain g_i by MN class, using the size proxy from EM surface area or synapse count, anchored to the tibia flexor's 0.1–10 µN tip-force range. Use a twitch kernel k_i(t) with τ_rise so that half-max is reached in about 8.5 ms, and an additional ~30 ms end-to-end motor delay if spikes are taken at the soma. (Karashchuk's 30 ms may include conduction and electromechanical delays; the 8.5 ms is measured from spike to half-max, so avoid double counting.)
  - Activation a_m(t) = sat(Σ_{i→m} g_i · (k_i * spikes_i)(t)).
  - F = F0_m · f_L(l) · f_V(v) · a_m + F_passive(l), using MuJoCo muscle actuators on FlyMimic tendons with refit `dynprm`.
  - Joint torque then follows from MuJoCo tendon geometry. Add passive joint springs fitted to Wang 2025 rest angles and stiffness once units are resolved.
- Inference: the parameters worth fitting first, with the targets that constrain them:
  - Per-muscle F0 scale: tibia-tip forces, and whole-leg support of body weight (passive is 70× too weak, so active tone is needed).
  - Activation and deactivation time constants: 8.5 ms twitch rise, ~100 ms decay.
  - Class gains within each pool: recruitment curves.
  - Damping: kinematic smoothness.
- Leave the anatomical geometry as measured.
- Inference: for legs other than the left front, and for the neck and wings, the fallback is a muscle-group-to-torque layer until MSK models exist. That means Ekeberg-style antagonistic torques per DoF (as in NeuroMechFly v1) driven by summed MN-group activity, which is still a biologically meaningful step up from position targets.

### Gaps
- Most entries in the table are fitted or assumed. Direct Drosophila measurements needed: force–length and force–velocity curves for leg muscles, per-MN twitch and force for muscles other than the tibia flexor, tendon stiffness, in-vivo activation time constants, joint damping, and adhesion and friction forces.
- MN→MTU aggregation is itself a modelling choice. FANC has 18 T1 target muscles, but FlyMimic has 15 MTUs covering 12 of 19 muscle groups, and no tibial, tarsal or LTM muscles.
