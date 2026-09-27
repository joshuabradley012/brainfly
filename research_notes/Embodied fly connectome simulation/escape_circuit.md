# The giant fiber escape circuit: latencies, electrical synapses and the jump (rung 6)

Notes compiled 2026-09-27 for brainfly: the MaleCNS v1.0 connectome as a leaky integrate-and-fire network (HybridBrain, 0.1 ms steps, Shiu et al.'s neuron: tau_m 20 ms, threshold 7 mV above rest, reset to rest, refractory 2.2 ms, current synapses with tau 5 ms, one fixed 1.8 ms synaptic delay). HybridBrain gained electrical synapses in commit b733054: `gap` is a sparse matrix in mV, rows postsynaptic. Each spike raises its partners' membranes at once, with no delay and no depression, so a spikelet above threshold fires the partner on the next step. Giving only one direction models rectification. These notes are about what to put in that matrix, what else the escape jump needs, and how to test it.

**Conventions**

- Tags: [PR] peer reviewed; [PP] preprint; [P] hobby project, not reviewed; [MODEL] a modelling paper's parameter or result, not a measurement.
- DERIVED: my own arithmetic or run. It is flagged each time.
- In the quote column, ✓ means I checked the quote against text I fetched myself or that one of my research agents fetched. Every text is saved in the session scratchpad.
- Evidence codes:
  - FT: full text.
  - ABS: abstract only.
  - SEC: a statement in a paper's full text that cites an older primary source I could not open.
  - DATA: the paper's source-data file.
  - IMG: a value read from a table rendered as an image, which can't be text-checked.
  - CODE: model code.
- "GF" is the giant fiber (DNp01). TTM is the jump muscle and TTMn its motor neuron. DLM is the dorsal longitudinal flight muscle and DLMn its motor neurons. PSI is the peripherally synapsing interneuron.
- Latencies in the fly literature are measured from a stimulus in the brain (electrodes through the eyes) to the muscle potential. Thoracic stimulation excites the motor neurons directly.

---

## Summary

- **Wild type.**
  - A stimulus in the brain fires the GF. The TTM responds 0.8–1.1 ms later and the DLM 1.3–1.6 ms later.
  - The field treats 0.7–1.2 ms (TTM) and 1.3–1.7 ms (DLM) as the healthy range. Rung 6's target comes from there.
  - Labs differ by 0.2–0.3 ms, mostly with temperature.
- **The latency budget.**
  - The GF axon takes 0.29 ms (2.07 m/s over about 0.6 mm; Kadas et al. 2019).
  - The GF→TTMn electrical synapse adds almost nothing.
  - TTMn spike to TTM potential takes about 0.5–0.8 ms. Thoracic stimulation gives 0.55–0.84 ms.
  - The one extra chemical synapse on the flight branch (PSI→DLMn) costs 0.3–0.5 ms.
- **Following.**
  - The TTM follows the GF 1:1 at 100 Hz and at 88–100% at 250 Hz.
  - The DLM follows 84% of spikes at 100 Hz and 28–57% at 250 Hz. It reaches 50% following at about 180 Hz.
  - Twin-pulse refractory periods are about 3.3 ms (TTM) and about 5 ms (DLM).
- **Without gap junctions (*shakB²*, Passover).**
  - Every study of the null allele found no DLM response at all.
  - The TTM responds only in some flies (22% of flies in one study, 4 of 7 in another). Its latency is 1.3–1.8 ms and it can't follow 100 Hz (10–26%).
  - That leftover response is cholinergic: tetanus toxin in the GF abolishes it.
- **The electrical synapse.**
  - It is a heterotypic junction: ShakB(N+16) on the GF side, ShakB(Lethal) in the TTMn and PSI.
  - In paired oocytes it passes depolarization from GF to target. The steady-state Gjmin/Gjmax is 0.21.
  - No one has recorded from a Drosophila TTMn or PSI with a microelectrode, so the size of the GF spike in TTMn is unmeasured.
  - The only quantitative model (Augustin et al. 2019) uses 135 nS. The paper prints "µS", but its code says nS. The coupling is one way.
  - Re-running that model gives a safety factor of about 3 for the TTMn and 2.3–2.7 for the PSI.
- **Recommendation.**
  - Add one-way spikelets: GF→TTMn about 20 mV and GF→PSI about 18 mV, each GF to its own-side TTMn and PSI.
  - Add 0.3 ms for the GF axon and about 0.5–0.6 ms for motor neuron to muscle, outside the model.
  - Make PSI→DLMn a fast (0.3 ms), strong, depressing synapse.
  - Keep TTMn, PSI and DLMn quiet at rest.
- **MaleCNS.**
  - Chemically, GF→TTMn has only 70 synapses on the right and 20 on the left. That is 1.9% and 0.8% of the TTMn's input.
  - GF→PSI has 2–9 synapses, and PSI→DLMn about 200 per side.
  - In the current brain one GF spike gives chemical PSPs of 3.9 mV (right TTMn) and 1.6 mV (left), against a 7 mV threshold. Both are subthreshold and arrive late.
- **The jump.**
  - The TTM extends the middle leg's coxa–trochanter joint, which depresses the femur. The femur–tibia joint extends too, driven by a tibia extensor that fires 1.46 ms after GF stimulation.
  - Escape leg extension takes 3.3 ms. Launch is 0.48 m/s at about 45°, with peak acceleration about 110 m/s² on each axis.
  - GF spike to takeoff is about 7 ms, a cross-preparation estimate.
- **FlyGym mapping.**
  - Drive `lm_coxa-lm_trochanterfemur-pitch` and `rm_coxa-rm_trochanterfemur-pitch` (increase = extension) with a torque actuator of about 60–140 µN·mm per leg, shaped by a twitch kernel. Release adhesion.
  - The demo position actuators (kp 45, ±65 µN·mm) are too weak and too slow for a 3 ms push.

---

## 1. Recommendations for brainfly

### 1.1 The gap-junction layer (first version)

| Junction | MaleCNS bodyIds (pre → post) | Direction | Spikelet | Why |
|---|---|---|---|---|
| GF → TTMn, left | 10010 → 804642 | GF to TTMn only | **20 mV** (try 14–30) | Rectifying heterotypic junction (Phelan 2008). TTM follows 1:1 to at least 200–250 Hz. The Augustin 2019 model gives a safety factor of about 3 (DERIVED run), and 3 × 7 mV ≈ 20 mV |
| GF → TTMn, right | 10001 → 800146 | GF to TTMn only | **20 mV** | Same |
| GF → PSI, left | 10010 → 802401 | GF to PSI only | **18 mV** (try 14–30) | Safety factor 2.3–2.7 in the same model (DERIVED) |
| GF → PSI, right | 10001 → 903327 | GF to PSI only | **18 mV** | Same |

These choices rest on the following.

- **Pairing.**
  - King & Wyman (1980) found that each GF contacts the same-side TTMn and one PSI. That PSI drives the opposite-side DLM.
  - MaleCNS agrees. GF_L's strongest PSI contact is PSI_L (9 synapses). PSI_L synapses onto DLMn c–f with right-side somata, and onto DLMn a,b (MN5) with a left soma. MN1–4 innervate muscle on their soma's side, and MN5 innervates muscle on the side opposite its soma (Hürkey 2023; Sun & Wyman 1997). So PSI_L drives the right DLM.
  - So GF_L → PSI_L and GF_R → PSI_R.
  - Dye from one GF does reach both PSIs (Phelan 2008), but the strength of the second route is unknown. Leave it out in v1.
- **One way, no depression.**
  - Depolarization passes from the ShakB(N+16) cell (GF) to the ShakB(L) cell (target).
  - The fly relay follows far above looming rates (the GF fires 25–75 Hz near contact in brainfly).
- **How big.**
  - The rule I suggest is a spikelet of about 3× (TTMn) and 2.5× (PSI) the distance from the target's median resting voltage to threshold.
  - For a neuron resting at 0 mV that gives 20 and 18 mV.
  - The current brain holds TTMn with a bias of −5.3 mV and PSI with −4.4 mV, against its network input and noise. So measure the resting voltage once, fix the sizes, and pre-register them.
  - If the relay fails on more than 1% of GF spikes at rest, raise the spikelet (cap it at 30 mV). Don't lower it to fit latencies.
- **Leave out of v1**, and try later as sensitivity runs:
  - GF_L ↔ GF_R (dye coupling is "weak"; strength unmeasured).
  - GF → the other side's PSI.
  - TTMn ↔ same-side PSI, and PSI ↔ PSI ("electrically coupled", strength unmeasured).
  - GF → GFC1–4. They are dye-coupled, but their physiology is unknown. GFC2_direct → TTMn chemical PSPs are 5.8–9.5 mV in the current brain. Watch for TTMn doublets if you add them.
  - Johnston's organ neurons → GF, and DLMn ↔ DLMn (coupling coefficient 0.01–0.023, which matters for flight, not the jump).
- **Continuous coupling is optional.**
  - No data constrain it.
  - If added, make it one way and rectified, with g·R_in ≤ 0.5.
  - The Augustin value (g·R_in ≈ 35, DERIVED) would pin the TTMn to the GF's subthreshold voltage. The TTMn would then fire without a GF spike, which flies don't show.
- **Spikelets can't make graded latencies.**
  - In old flies a 4-fold loss of junction conductance adds about 0.3 ms (Augustin 2017/2019). An all-or-none spikelet can't reproduce that; it either fires on the next step or fails.
  - If graded latency matters later (ageing, *frazzled*, Netrin), switch to pulse coupling. For about 0.4 ms after each GF spike, inject g·(V_spike − V_target) into the target, with V_spike about 100 mV above rest.
  - The target then reaches threshold after a charging time that grows as g falls. For a pulse of height A = 100 mV and width w = 0.4 ms, a 7 mV response needs g·R ≈ 3.7 and a 20 mV response needs g·R ≈ 11. (DERIVED from a research agent's formula: response = A·gR/(1+gR)·[1 − exp(−w(1+gR)/τm)].)

### 1.2 Five things the connectome can't supply here

1. **The jump and flight motor neurons must be quiet at rest.**
   - The calibration holds every type without a measured rate near 2 Hz (0.1 Hz for descending neurons), and the TTMn is one of them.
   - In the fly the TTM "fires only once at the start of flight" (Koenig & Ikeda 2005, citing Trimarchi & Schneiderman 1995b). One GF spike makes one TTMn spike and one takeoff.
   - With a body attached, a 2 Hz TTMn means two jumps a second. Set the targets for TTMn, STTMm, PSI and DLMn near 0 Hz.
2. **PSI → DLMn must be fast and strong.**
   - In the fly this one chemical synapse costs 0.3–0.5 ms and relays reliably at low rates. It follows 84% of spikes at 100 Hz and 28% at 250 Hz.
   - Its release sites sit on the DLMn axons "within a peripheral nerve" (King & Wyman 1980).
   - In MaleCNS, PSI→DLMn is 24–68 synapses per DLMn c–f and 17–26 onto DLMn a,b. That is 0.2–0.7% of each DLMn's 8,600–10,400 input synapses.
   - In the current brain a PSI spike gives a PSP of 0.3–1.6 mV, peaking about 9 ms after the 1.8 ms delay. The DLMns are biased at −12.5 to −13.4 mV, so a PSI spike can't fire a DLMn.
   - Model it as a delayed spikelet. Use a 3-step (0.3 ms) delay and a size set by the rule in 1.1. Add depression, fitted to 84% following at 100 Hz and then tested at 250 Hz (28%) or against FF50 ≈ 180 Hz.
   - HybridBrain now has one global chemical delay (the `pend` ring buffer) and an instant `gap`. The smallest change is to give `gap` entries an optional delay in steps and give its presynaptic types optional depression. A second short ring buffer for a named edge set would also work.
3. **The chemical GF→TTMn edge is weak and asymmetric.**
   - It is 70 synapses on the right and 20 on the left, a 3.5-fold asymmetry that probably reflects reconstruction.
   - It gives 3.9 and 1.6 mV PSPs peaking about 9 ms after the 1.8 ms delay.
   - It doesn't matter in the intact model, where the spikelet does the work.
   - In a *shakB*-like run it means no TTM response to single GF spikes. In flies, 22–57% of *shakB²* flies still respond, at about 1.6 ms.
   - Don't fit it in rung 6's first attempt; count failure as *shakB*-like (criteria below). If a closer match is wanted later, give this edge its own delay (0.5–0.8 ms) and a near-threshold weight with depression. Fit it to one *shakB²* statistic and test it on another.
4. **Signs near the TTMn are uncertain.**
   - About two thirds of the TTMn's input synapses are signed inhibitory in brainfly (right TTMn: +1,195 / −2,413). The largest is GABAergic IN13A022 (16%).
   - Cheong et al. (2026) argue that a glutamatergic trio upstream of the TTMn (IN07B023, IN21A026, IN21A027) is excitatory, because cholinergic DNp11 drives it and evokes jumping. Brainfly signs glutamate inhibitory.
   - This matters for GF-independent routes to the TTMn, not for the spikelet relay.
5. **Both GFs may see a loom.**
   - Jang et al. (2023, whole-cell) found that the GF "responds invariantly to looming stimuli across tested azimuthal locations". Input from the other eye comes "through an unidentified pathway".
   - brainfly's escape test asks the other side's GF to stay put. With own-side TTMn pairing, a loom on one side will then extend only one middle leg.
   - Decide before the body test whether a one-legged push counts. Report bilateral versus unilateral TTMn firing, and consider a sensitivity run with a weak GF–GF spikelet (1–3 mV).

### 1.3 Delays to add outside the model

| Stage | Use | Literature | Source |
|---|---|---|---|
| GF spike in the brain → thoracic terminal | **0.3 ms** | 0.29 ± 0.03 ms in 24 h adults (0.52 ms at 1 h); 2.07 m/s over about 0.6 mm | Kadas et al. 2019 [PR] |
| GF → TTMn junction and TTMn spike | **0.1 ms** (one step, as HybridBrain does now) | "does not add notable time"; in the model the TTMn peaks 0.19 ms after the GF (DERIVED re-run) | Kadas 2019; Augustin 2019 [MODEL] |
| TTMn spike → TTM muscle potential | **0.5 ms** (0.35–0.7) | Thoracic stimulation → TTM takes 0.55–0.84 ms, including the time from stimulus to spike. The model's pure NMJ delay is 0.35 ms | Thomas & Wyman 1984; Kadas 2019; Augustin 2019 |
| GF → PSI junction and PSI spike | **0.1 ms** | In the model the PSI peaks 0.25 ms after the GF (DERIVED) | Augustin 2019 |
| PSI → DLMn chemical synapse | **0.3 ms**, inside the model as a per-edge delay | 0.32 ms (Kadas 2019), ~0.4 ms (Allen & Godenschwege 2010), ~0.5 ms (Gaitanidis 2025). The model uses 0.15 ms delay plus 0.1/1 ms kinetics | as listed |
| DLMn spike → DLM potential | **0.6 ms** (0.5–0.8) | Thoracic stimulation → DLM takes 0.65–0.97 ms | Thomas & Wyman 1984; Kadas 2019 |
| TTM potential → force onset | **0.5–1.5 ms** (assumption) | Not measured in any source we could open | — |
| *Predicted* GF spike → TTM potential | 0.3 + 0.1 + 0.5 = **0.9 ms** | measured 0.8–1.1 ms; healthy range 0.7–1.2 | see 2.1 |
| *Predicted* GF spike → DLM potential | 0.3 + 0.1 + 0.3 + 0.1 + 0.6 = **1.4 ms** | measured 1.3–1.6 ms; healthy range 1.3–1.7 | see 2.1 |

The wild-type latency follows from these constants once the spikelet is suprathreshold. It is a consistency check, not a test of the wiring. Pre-register the constants before any run. Temperature moves every stage: labs working at room temperature report TTM at 1.0–1.1 ms and DLM at 1.5–1.6 ms. So compare interval structure first (DLM minus TTM 0.24–0.6 ms; GF axon about 0.3 ms), then absolute values.

### 1.4 A pre-registerable rung 6 test

**Question.** The model gets one-way spikelets from each giant fiber to its own TTMn and PSI, a fast PSI→DLMn synapse, and literature delays outside the model. Does the resting brain then relay GF spikes to the jump and flight muscles like a fly, in timing, reliability and following? And does removing the spikelets, like *shakB²*, slow or silence the relay as in flies?

**Fixed before running.**
- Spikelet sizes, by the rule in 1.1, from TTMn's and PSI's resting voltage measured once.
- Δ_GF 0.3 ms, Δ_TTM 0.5 ms and Δ_DLM 0.6 ms.
- The PSI→DLMn delay (0.3 ms) and size. Its depression is fitted only to 100 Hz following.
- Resting targets near 0 Hz for TTMn, PSI and DLMn.
- Fresh seeds.
- Predicted muscle latency is L_TTM = Δ_GF + (t_TTMn − t_GF) + Δ_TTM, and likewise for the DLM. If the spikelet itself carries a 3-step delay, drop Δ_GF from the formula.

**Conditions.**
1. Intact.
2. *shakB*-like: every spikelet removed and the chemical edges kept.
3. Null: the existing escape test's degree-preserving rewiring of the chemical matrix, with the same spikelets.
4. Optional, reported only: "aged", with spikelets at 1.9/3 of their size.

**Part A: GF stimulation, like electrodes in the brain.** Use 8 flies per condition and both sides.
- Force a single GF spike every 5 s, 50 times.
- Run 10 trains of 10 GF spikes at 100 Hz and at 250 Hz, 2 s apart.
- Run twin pulses 10, 8, 6, 4, 3 and 2 ms apart.

**Part B: looming, end to end.** Use the escape test's looming disk on each side, 10 per fly.

**Criteria, intact: all must pass.**
- W1 (latency): median L_TTM 0.7–1.2 ms; median L_DLM 1.3–1.7 ms; L_DLM − L_TTM 0.24–0.6 ms.
- W2 (reliability): TTMn fires within 0.5 ms of at least 95% of single GF spikes; DLMn after at least 90%.
- W3 (following): TTM at least 95% at 100 Hz and at least 80% at 250 Hz. DLM at least 70% at 100 Hz and at most 60% at 250 Hz. Fly values: TTM 100%/88–100%; DLM 84%/28–57%.
- W4 (quiet): in 100 s of rest per fly, TTMn fires no more than 1 spike without a GF spike in the preceding 5 ms, and likewise PSI.
- W5 (looming): in at least 95% of looms that fire the GF, the same-side TTMn fires within 0.5 ms of the first GF spike.

**Criteria, *shakB*-like: all must hold.**
- S1: TTMn responds to at most 50% of single GF spikes, or its median predicted latency is at least 0.4 ms longer than intact. Flies: 1.3–1.8 ms in responders, and many flies don't respond at all.
- S2: TTM follows at most 30% at 100 Hz (flies 10–26%).
- S3: DLM responds to at most 5% of GF spikes (flies: none).
- S4 (looming): in at least 80% of looms, TTMn's first spike comes at least 2 ms later than intact, or not at all.

**Null.** Rewired wiring abolishes the loom → GF → TTMn chain, as in the existing escape test. The spikelet layer alone can't make a jump without GF spikes.

**Reported, not scored.**
- Latency distributions.
- Bilateral versus unilateral TTMn firing per loom (see 1.2, point 5).
- TTMn doublets.
- The "aged" run. In a spikelet model it should keep the intact latency while it relays, which is a known limit (1.1).

**What would count against the approach.**
- W2 or W4 failing at every spikelet up to 30 mV. That would mean the TTMn's network input swamps the relay, a sign problem worth chasing (1.2, point 4).
- S3 failing, meaning the DLM still responds without gap junctions, would point to a chemical GF→PSI path the fly doesn't have.

### 1.5 From TTMn spikes to a jump in FlyGym

| Motor neuron | Muscle | FlyGym 2.1 degree of freedom | Extension is | Notes |
|---|---|---|---|---|
| TTMn_L (804642) | left TTM | `lm_coxa-lm_trochanterfemur-pitch` (CTr) | **an increase** (neutral −139°) | DERIVED forward kinematics: going from −139° to −80° swings the femur from 38° above horizontal to 20° below and lowers the foot 0.9 mm relative to the thorax |
| TTMn_R (800146) | right TTM | `rm_coxa-rm_trochanterfemur-pitch` | an increase | same |
| T2 tibia extensor motor neuron (TLMn) | TLM | `lm_trochanterfemur-lm_tibia-pitch` (FTi), and `rm_…` | **a decrease** (0° is a straight leg; neutral 103°) | Fires 1.46 ± 0.02 ms after GF stimulation, through a "novel" pathway rather than directly from the GF (Trimarchi & Schneiderman 1993). Its MaleCNS identity was not checked. Script it as a synergy in v1 |

1. Add a MOTOR actuator on each middle-leg CTr pitch, with a force range of ±250 µN·mm. FlyGym lets several actuator types share a joint (`add_actuators` docstring).
   - Units are mm, g and s, so force is in µN and torque in µN·mm. The body weighs 1.0 mg, a weight of 9.8 µN.
2. Build TTM activation from TTMn spikes: a(t) = Σ k(t − t_spike − d), capped at 1.
   - d = Δ_TTM (0.5 ms) + electromechanical delay (assume 0.5 ms), so d ≈ 1 ms.
   - k rises over about 1.3 ms (Kolomenskiy 2016's fit to Zumstein's force slope). It then decays with τ ≈ 8–10 ms, so the whole twitch lasts about 20 ms (Zumstein 2004, via Elliott 2007).
   - Only the first 3–5 ms matter for takeoff. The 8.2 ms time to peak comes from tethered, near-isometric flies.
3. Torque is τ(t) = τ_max · a(t) on the TTMn's own side. Start near τ_max ≈ 100 µN·mm (DERIVED).
   - Card & Dickinson's peak accelerations (about 155 m/s² resultant) give about 80 µN per leg.
   - Zumstein measured 101 ± 4.4 µN, and his model needs 137 µN per leg.
   - The moment arm about CTr is about the femur's 0.78 mm.
4. The tibia extensor: drive FTi toward extension 0.5 ms after CTr, for example with a torque of about half τ_max. Middle legs extend at the coxo-trochanteric, femoro-tibial and tibio-metatarsal joints (Trimarchi & Schneiderman 1995).
5. Adhesion and actuators.
   - Switch off middle-leg adhesion at force onset (`set_leg_adhesion_states`) and the other legs' adhesion at takeoff.
   - During the push, stop the joints' position actuators fighting the motor. Set their targets to the current angles, or scale kp down.
6. Calibrate τ_max once, on launch speed: 0.48 ± 0.01 m/s over the first 2 ms of flight in escapes (Card & Dickinson 2008). Then check, without retuning:
   - leg extension 3.33 ms (accept 2–5);
   - launch angle about 45°;
   - head-up pitch, seen in 39 of 43 flies;
   - peak acceleration about 110 m/s² per axis;
   - takeoff 5–10 ms after the GF spike.
7. Don't copy flybench's jump program [P]. It adds +1 rad to both CTr and FTi pitch. In FlyGym 2.1 a larger FTi pitch flexes the tibia (DERIVED forward kinematics: the femur–tibia angle equals the FTi pitch).
8. The demo actuators (kp 45 µN·mm/rad, ±65 µN·mm) are too weak and too slow (DERIVED).
   - With the body's roughly 1 mg on a roughly 1 mm lever, kp 45 gives ω ≈ √(45/10⁻³) ≈ 210 rad/s, a quarter period of about 7 ms. The fly pushes off in 3.3 ms.

Timeline a simulated escape should reproduce (time 0 = GF spike in the brain, 20–25 °C):

| t after GF spike | Event | Basis |
|---|---|---|
| 0.3 ms | Spike reaches the thoracic terminal; TTMn and PSI fire one model step later | Kadas 2019 |
| 0.9 ms | TTM muscle potential, one per GF spike | 0.88–0.94 ms measured |
| 1.1–1.4 ms | DLM potential ("tuck": wings held down) | 0.24–0.46 ms after the TTM |
| 1.5 ms | Tibia extensor (TLM) potential | Trimarchi & Schneiderman 1993 |
| about 1.5–2.5 ms | TTM force onset | assumption; unmeasured |
| about 3–4 ms | Middle-leg extension begins | DERIVED (takeoff minus 3.3 ms) |
| about 6–7 ms | Tarsi leave the ground | 3.3 ms extension; GF spike → takeoff about 7 ms (Fotowat 2009, cross-preparation) |
| 8.2 ms | Isometric twitch peak (tethered) | Zumstein 2004 |
| about 20 ms | Twitch over | Elliott 2007 citing Zumstein 2004 |

---

## 2. Evidence

### 2.1 Latencies, stage by stage (wild type)

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Healthy range | TTM 0.7–1.2 ms; DLM 1.3–1.7 ms | Electrodes through the eyes, 30–60 V, 0.03 ms pulses; varies with genotype, background, temperature, age | "Latencies between 0.7 and 1.2 ms for the GF-TTM pathway and between 1.3 and 1.7 ms for the GF-DLM pathway indicate a healthy preparation" ✓FT | Augustin, Allen & Partridge 2011, JoVE [PR] [PMC3182647](https://pmc.ncbi.nlm.nih.gov/articles/PMC3182647/) |
| Canonical values | TTM ~0.8 ms; DLM ~1.2 ms; pooled 0.8 ± 0.1 and 1.4 ± 0.3 ms | Protocol chapter, intracellular muscle recording | "average response latencies to a single stimulus are in the range 0.8 ms +/− 0.1 ms for the GF-TTM pathway and 1.4 ms +/− 0.3 ms for the GF-DLM pathway depending on genotype and genetic background" ✓FT | Allen & Godenschwege 2010, CSH Protoc [PR] [PMC2946074](https://pmc.ncbi.nlm.nih.gov/articles/PMC2946074/) |
| Brain stimulation, 23 °C | TTM 0.88 ± 0.09 ms; DLM 1.30 ± 0.09 ms (SD, n = 20 flies) | Canton-S, intracellular TTM and DLM | "was 0.88 ± 0.09 msec, and the mean DLM latency was 1.30 ± 0.09 msec. The mean latency varied somewhat with temperature" ✓FT (PDF text; OCR shows ± as "+") | Thomas & Wyman 1984, J Neurosci [PR] [PMC6564902](https://pmc.ncbi.nlm.nih.gov/articles/PMC6564902/) |
| Intracellular GF stimulation | TTM 0.9 ms; DLM 1.3 ms | GF impaled in the cervical connective and stimulated (0.05 ms pulses), 23 °C | "the GF drove the TTM and DLM with very constant latencies of 0.9 msec for the TTM and 1.3 msec for the DLM" ✓FT (OCR, split across columns) | Thomas & Wyman 1984 |
| Short-latency class, large sample | TTM 0.94 ± 0.014 ms (n = 217); DLM 1.40 ± 0.013 ms (n = 247), SEM | Tethered controls, 0.1 ms pulses via the eyes; shortest latency per fly | "Means ± SEM, in msec, of shortest latency of each class measured for each fly." (Table 1) ✓FT | Engel & Wu 1996, J Neurosci [PR] [PMC6579151](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579151/) |
| Young vs old | 5–7 d: TTM 0.93, DLM 1.44 ms; 45–50 d: 1.22, 1.85 ms | w^Dah, 40 V, 0.03 ms | "matches the values recorded experimentally in the TTM and DLM of young (5–7 d old) flies (0.93 and 1.44 ms, respectively; Augustin et al., 2017)" ✓FT | Augustin, Zylbertal & Partridge 2019, eNeuro [PR] [PMC6469880](https://pmc.ncbi.nlm.nih.gov/articles/PMC6469880/); data in Augustin et al. 2017 PLoS Biol [PMC5597081](https://pmc.ncbi.nlm.nih.gov/articles/PMC5597081/) (day 7: TTM 0.926 ± 0.139 SD, n = 17 ✓DATA) |
| Room-temperature lab | TTM ~1.0–1.1 ms; DLM ~1.5–1.6 ms | Blagburn lab controls | "Those latencies are longer than typically reported but consistent with the room temperature at which the experiments were carried out" ✓FT | Pézier et al. 2016, PLoS ONE [PR] [PMC4833477](https://pmc.ncbi.nlm.nih.gov/articles/PMC4833477/) |
| GF axon conduction | 0.29 ± 0.03 ms at 24 h after eclosion (n = 9); 0.52 ± 0.04 ms at 1 h (n = 7) | Computed as GF→TTM minus thoracic→TTM in the same flies; reared at 24 °C | "the GF axonal conduction duration decreased by 80% during the first day of postnatal period, from 0.52 ± 0.04 ms in 1hPE flies to 0.29 ± 0.03 ms in 24hPE flies" ✓FT | Kadas, Duch & Consoulas 2019, eNeuro [PR] [PMC6709211](https://pmc.ncbi.nlm.nih.gov/articles/PMC6709211/) |
| GF conduction velocity | 2.07 ± 0.21 m/s (24 h); 1.15 ± 0.09 m/s (1 h); axon about 0.6 mm long, about 7 µm wide | as above | "this equals to an increase in axonal conduction velocity from 1.15 ± 0.09 m/s at 1hPE to 2.07 ± 0.21 m/s in 24PE flies" ✓FT | Kadas 2019 |
| Same-preparation branch latencies | GF→TTM 1.13 ± 0.02 ms; GF→DLM 1.45 ± 0.03 ms (24 h, SEM, n = 9) | Extracellular tungsten electrodes, 0.15 ms pulses | "the latency of the GF-DLM5–6 (1.45 ± 0.03 ms) pathway is significantly … longer than that of the GF-TTM (1.13 ± 0.02 ms) pathway" ✓FT | Kadas 2019 |
| GF → TTMn synapse delay | negligible | Latency arithmetic | "Note that the GF to TTMn synapse is dominated by electrical transmission and, thus, does not add notable time to the latency." ✓FT | Kadas 2019 |
| Thoracic stimulation → muscle | TTM 0.63 ± 0.04; DLM 0.65 ± 0.05 ms (SD, n = 10) | Electrodes in the thoracic ganglion, Canton-S, 23 °C | Table I row "C-S 0.88 ± 0.09 1.30 ± 0.09 0.63 ± 0.04 0.65 ± 0.05" ✓FT (OCR) | Thomas & Wyman 1984 |
| Thoracic stimulation → muscle, other lab | TTM 0.84 ± 0.02 (n = 8); DLM (MN5) 0.97 ± 0.03 ms (n = 9), 24 h | as Kadas above | "the TTM branch (1hPE, 0.80 ± 0.04 ms and 24hPE, 0.84 ± 0.02 ms" ✓FT | Kadas 2019 |
| NMJ delay (estimate) | 0.35 ms, from a measured 0.65 ms "neuromuscular latency" minus 0.3 ms of modelled stimulus-to-spike time | Model plus Augustin 2017 data | "The estimated NMJ delay is therefore the remaining 0.35 ms, achieving a total of 0.65 ms." ✓FT | Augustin 2019 [MODEL] |
| PSI → DLMn chemical delay | about 0.3 ms | GF→DLM minus GF→TTM, same flies | "fast chemical synaptic transmission between PSI and MN5 takes only about one third of a millisecond" ✓FT | Kadas 2019 |
| TTM → DLM interval | ~0.4 ms | Protocol chapter | "the delay between the TTM and DLM response is always ~0.4 ms" ✓FT | Allen & Godenschwege 2010 |
| TTM → DLM interval | 0.24 ± 0.05 ms (SD, n = 13) | GF stimulated through the eyes; legs removed | "with the TTM spike occurring on average 0.24 ms before the DLM spike (SD = 0.05 ms" ✓FT | Fotowat et al. 2009, J Neurophysiol [PR] [PMC3817277](https://pmc.ncbi.nlm.nih.gov/articles/PMC3817277/) |
| Extra chemical synapse | ~0.5 ms | Review statement in a research paper | "The extra chemical synapse from the PSI to the DLM Mns … adds ~0.5 ms delay" ✓FT | Gaitanidis et al. 2025, PLoS Biol [PR] [PMC12707685](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/) |
| GF spike width | 0.40 ± 0.06 ms intracellular (connective near thorax) | Secondary citation | "recorded intracellularly from the connective near the thorax is reportedly 0.40 ± 0.06 ms" ✓SEC | Blagburn 2020, PLoS ONE [PR] [PMC6946141](https://pmc.ncbi.nlm.nih.gov/articles/PMC6946141/) |
| Tibia extensor (TLM) | 1.46 ± 0.02 ms after GF stimulation | TLM EMG | "activation of the TLM with a latency of 1.46 +/- 0.02 ms" ✓ABS | Trimarchi & Schneiderman 1993, J Exp Biol 177:149 [PR] |
| Intermediate and long latencies | IL: TTM 1.70, DLM 2.16 ms (in 28% of flies); LL: TTM 3.37, DLM 3.82 ms | Weaker brain stimulation, which reaches the GF through afferents | Table 1 "Controls 3.82 247 3.37 217 2.16 68 /247 1.70 64 /217 1.40 247 0.94 217" ✓FT | Engel & Wu 1996 |

### 2.2 Following frequency and refractoriness (wild type)

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| 1:1 at 100 Hz; TTM beyond 300 Hz | Both follow at 100 Hz; DLM fails above 100 Hz | 10 trains of 10 stimuli at 100/200/300 Hz | "At 100 Hz, both TTM and DLM follow the stimuli 1:1." … "The TTM responses, however, remain 1:1 with stimuli even beyond 300Hz" ✓FT | Augustin et al. 2011 |
| Following, table | TTM 100% at 100 and 250 Hz; DLM 84 ± 10.7% at 100 Hz, 27.6 ± 7.2% at 250 Hz (n = 6) | *shakB²*/+ females, 25 °C, intracellular TTM and contralateral DLM | Table 1 row "shak-B 2 /+ 6 0.85 ± 0.03 100 ± 0.0% 100 ± 0.0% 1.43 ± 0.07 84 ± 10.7% 27.6 ± 7.2%" ✓FT | Allen & Murphey 2007, Eur J Neurosci [PR] [PMC1974813](https://pmc.ncbi.nlm.nih.gov/articles/PMC1974813/) |
| Following at 200 Hz | GF–TTMn 1:1 at up to 200 Hz; DLM path follows 50 Hz, not 200 Hz | Controls, about 19 °C | "The GF-TTMn connection in controls can follow one-to-one at 200 Hz or less" ✓FT | Pézier et al. 2016 |
| Canton-S decrement | TTM almost none at 100 Hz; plateau about 70% at 200 Hz, about 60% at 300 Hz. At 250 Hz, TTM 88–100% and DLM 55–57% (Table 3) | 10 bouts of 10 pulses | "At 100 Hz, the wild-type specimens show almost no response decrement … the plateau at ∼70% for 200 Hz and near the 60% level at 300 Hz" ✓FT | Allen et al. 1999, J Neurosci [PR] [PMC6782895](https://pmc.ncbi.nlm.nih.gov/articles/PMC6782895/) |
| DLM FF50 | about 180 Hz (10 d: 200 ± 24 Hz, n = 10) | Extracellular DLM | "is ~180 Hz and similar in young responders and old NRs" ✓FT, ✓DATA | Gaitanidis et al. 2025 |
| Twin-pulse refractory period | TTM 3.3 ms (n = 48); DLM 5.2 ms (n = 41), geometric means | Tethered controls | Table 3; footnote "Short-latency DLM (not TTM) refractory periods may be underestimates" ✓FT | Engel & Wu 1996 |
| Refractory period, protocol statement | TTM ~3 ms; DLM ~5 ms | — | "For TTM this is ~3 ms and DLM is ~5 ms" ✓FT | Allen & Godenschwege 2010 |
| "Normal synapse" criterion used by several labs | latency ≤1 ms and 1:1 at 100 Hz | — | "A normal synapse is defined as response latency ≤1 msec and follow stimuli up to 100 Hz" ✓FT | Godenschwege et al. 2002, J Neurosci [PR] [PMC6757528](https://pmc.ncbi.nlm.nih.gov/articles/PMC6757528/) |
| TTM depresses more than DLM | at all rates from 10 to 100 Hz, over prolonged trains | Intracellular muscle recording | "the DLM demonstrated less synaptic depression than did the TTM when stimulated for prolonged periods of time at all of the stimulation frequencies tested (from 10 to 100 Hz)" ✓FT | Koenig & Ikeda 2005, J Neurophysiol [PR] [doi](https://doi.org/10.1152/jn.00323.2005) |

### 2.3 Without gap junctions: *shakB*, Passover, graded loss

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Passover | TTM 1.50 ± 0.18 ms (SD, n = 20); no DLM response; TTM follows only below 1 Hz; thoracic stimulation normal | Brain stimulation, 23 °C | "the TTM responses had abnormally long latencies (mean latency = 1.50 ± 0.18 msec, Table I), and no response could be evoked in the DLMs" ✓FT (OCR split across columns) | Thomas & Wyman 1984 |
| *shakB²*/Y | TTM 1.62 ± 0.17 ms (n = 7, 3 of 7 never responded); 17.5% at 100 Hz, 10.5% at 250 Hz; no DLM | 25 °C, brain stimulation 40–60 V | Table 1 "shak-B 2 /Y 7 a 1.62 ± 0.17 ** 17.5 ± 5.5% 10.5 ± 0.5% No responses" ✓FT | Allen & Murphey 2007 |
| *shakB²*, larger sample | 8 of 36 flies respond (22%); TTM 1.64 ± 0.07 ms; 2.63 of 10 at 100 Hz; 0 of 36 DLM | *shakB²*/Y; UAS-shakB(n+16) without driver | Table S2 row "shakB 36 8 (22%) 1.64 (± 0.07) 2.63 (± 0.92) 0" (*shakB²* in the original) ✓FT | Phelan et al. 2008, Curr Biol [PR] [PMC2663713](https://pmc.ncbi.nlm.nih.gov/articles/PMC2663713/) |
| Rescue by the GF isoform | A307>shakB(N+16): 14/14 respond, 1.45 ± 0.08 ms, 6.2/10 at 100 Hz, DLM in 2/14. ShakB(N) doesn't rescue | *shakB²* background | Table S2 rows ✓FT | Phelan et al. 2008 |
| *shakB²*/*shakB²* and deficiencies | TTM 1.8 ± 0.2 ms (80% of muscles); over deficiencies 1.6–2.5 ms; DLM none. Hypomorphs keep the DLM at 1.40–1.57 ms | Oregon-R background, brain stimulation | "the mean TTM latencies range between 1.6 and 2.5 msec, a substantial increase from the average value of 0.9 msec in shakB2/FM6 sibling controls" ✓FT (OCR, split across columns); table values IMG | Baird, Schalet & Wyman 1990, Genetics [PR] [PMC1204268](https://pmc.ncbi.nlm.nih.gov/articles/PMC1204268/) |
| Protocol summary | TTM ~1.5 ms, no following at 100–300 Hz, no DLM | — | "The average response latency for the TTM in these flies is consistently increased to an average of 1.5 ms" ✓FT (a round number) | Allen & Godenschwege 2010 |
| GF-specific knockdown | *shakB* RNAi in the GF raises both TTM and DLM latency and cuts following; "comparable to" *shakB²* | R79H05-GAL4 | "These results are comparable to those obtained with the shakB 2 null mutants" ✓FT | Pézier et al. 2016 |
| Behaviour | escape badly impaired, voluntary takeoff normal | *shakB²* flies | "While the escape response is severely impaired in these mutants, they displayed normal voluntary flight initiation." ✓ABS | Hammond & O'Shea 2007, J Comp Physiol A [PR] [doi](https://doi.org/10.1007/s00359-007-0265-3) |
| Graded loss: *frazzled* | TTM 1.18 ms (SD 0.30, n = 35 terminals), 68.6% at 100 Hz, vs control 0.93 ms, 98.3%. ShakB fills 5.14% vs 9.04% of the GF terminal | Loss-of-function mutants | "frazzled LOF mutant flies exhibit longer response latencies than their control siblings (1.18 ms; SD, 0.30; n = 35 terminals" ✓FT | Lopez et al. 2025, eNeuro [PR] [PMC12570126](https://pmc.ncbi.nlm.nih.gov/articles/PMC12570126/) |
| Graded loss: Netrin | TTM 1.26 ms (SD 0.53, n = 208), 52% at 100 Hz; latency leaves the normal range once ShakB fills less than about 6.5% of the terminal | NetAΔBΔ hemizygotes | "When Innexin levels fell below ∼6.5% of terminal volume occupied, muscle response latency was outside of normal ranges (≥0.95 ms)" ✓FT | Orr et al. 2014, J Neurosci [PR] [PMC6608228](https://pmc.ncbi.nlm.nih.gov/articles/PMC6608228/) |
| Ageing | slowing tracks thoracic ShakB loss; ShakB(N+16) overexpression prevents it | w^Dah, 45–50 d | "forced expression of SHAK-B(n+16) , the isoform crucial for functional hemichannel formation in the GFS [ 61 ], prevented the age-related functional decline" ✓FT | Augustin et al. 2017, PLoS Biol [PR] |

No GF-pathway data for *shakB^R-2* turned up (Europe PMC searches found nothing). The null used across GF studies is *shakB²*, plus Passover alleles and 19E deficiencies.

### 2.4 Chemical block: nAChR antagonists, Dα7, *Cha^ts*, tetanus toxin

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| The leftover *shakB²* response is chemical | Tetanus toxin in the GF plus *shakB²*: no TTM and no DLM response (n = 7) | *shakB²*/Y; c17>UAS-TNT | "Hemizygous shak-B 2 males that expressed TNT in their GFs gave no responses in TTM or DLM upon stimulation" ✓FT | Allen & Murphey 2007 |
| ACh synthesis block | *shakB²* hemizygotes with *Cha^ts2* at 28 °C: no TTM, no DLM. In *shakB²*/+ females: TTM normal, DLM none | 48 h at 28 °C | "gave no responses in DLM upon GF stimulation, as expected, but also gave no responses in TTM" ✓FT | Allen & Murphey 2007 |
| GF–PSI chemical component alone | insufficient | *shakB²* | "Unlike GF-TTMn, it appears that the chemical component of this synapse is unable to function on its own as no responses are seen in shak-B 2 mutants" ✓FT | Allen & Murphey 2007 |
| Could the leftover response be polysynaptic? | Left open | — | "Confirmation of GF-TTMn being monosynaptic only will require intracellular recordings from TTMn." ✓FT | Allen & Murphey 2007 |
| Mecamylamine | Blocks GF→DLM completely at about 39 ng/mg; GF→TTM unaffected; no latency change | Nanoinjection into the head, n = 15 per dose | "The maximum effect was reached with about 39 ng/mg of mecamylamine, when stimulation of the GF in the brain did not result in any response output at the DLM muscle" ✓FT | Mejia et al. 2010, Toxicon [PR] [PMC2967628](https://pmc.ncbi.nlm.nih.gov/articles/PMC2967628/) |
| α-conotoxins | GF–DLM following at 50 Hz falls to 1–34%, depending on the toxin; GF–TTM unchanged | 45 pmol/fly, n = 10 per toxin | "decreases the response of the giant fiber to dorsal longitudinal muscle (GF-DLM) connection to 20 ± 13.9% for MII…" ✓FT | Heghinian et al. 2015, FASEB J [PR] [PMC4422358](https://pmc.ncbi.nlm.nih.gov/articles/PMC4422358/) |
| Dα7 null | DLM gives no response to GF stimulation even at 1 Hz; TTM follows 100 Hz normally; long-latency (afferent) response lost | PΔEY6 and allelic series | "the TTMs were able to follow the giant fiber stimulation at 100 Hz without any problem in the most severe mutation" ✓FT | Fayyazuddin et al. 2006, PLoS Biol [PR] [PMC1382016](https://pmc.ncbi.nlm.nih.gov/articles/PMC1382016/) |
| Where Dα7 is | at PSI→DLMn and at GF inputs; probably not at GF outputs | — | "this subunit seems not to be present at the GF-PSI or GF-TTMn synapses, however, this is yet to be determined." ✓FT | Allen & Murphey 2007 |

The pattern is clean and useful for a model. Removing ShakB kills the flight branch and slows or kills the jump branch. Blocking nicotinic receptors kills the flight branch and the GF's afferent drive, but spares GF→TTM.

### 2.5 The electrical synapse: molecules, rectification, structure, sides

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Isoforms | ShakB(N+16) presynaptic in the GF; ShakB(Lethal) in TTMn and PSI; heterotypic | GAL4 rescue of *shakB²* plus in situ | "is required presynaptically in the Giant Fiber to couple this cell to its postsynaptic targets that express Shaking-B(Lethal)" ✓FT | Phelan et al. 2008 |
| Direction | depolarization passes N+16 → L (GF → target); hyperpolarization passes the other way | Paired Xenopus oocytes, dual voltage clamp | "depolarizations were preferentially transmitted in one direction only" … "whereas hyperpolarizing signals passed preferentially in the opposite direction" ✓FT | Phelan et al. 2008 |
| Rectification strength | steady-state Gjmin/Gjmax 0.21. At ±10 mV only about 1.6-fold (4.39 vs 2.78 µS, n = 49 pairs). Closing is mostly done by 5 ms, but opening reaches only 50–60% of maximum at 5 ms. A voltage-insensitive floor of about 15–20% | Oocytes; conductance in µS is an oocyte value, not a neuron value | "The Gjmin/Gjmax ratio was 0.21"; "The residual conductance presumably represents a small population (∼15%–∼20%) of voltage-insensitive channels." ✓FT; Table S3 ✓FT | Phelan et al. 2008 |
| Structure | 3.25 ± 0.12 nm close appositions with 41 nm vesicles on the GF side, lost in *shakB²*; chemical synapses remain | EM | "At mutant GF-TTMn and GF-PSI contacts, chemical synapses and small regions of close membrane apposition, more similar to vertebrate gap junctions, were not affected." ✓ABS | Blagburn et al. 1999, J Comp Neurol [PR] [doi](https://doi.org/10.1002/(SICI)1096-9861(19990222)404:4%3C449::AID-CNE3%3E3.0.CO;2-D) |
| ShakB share of the GF terminal | 9.04% (SD 1.33, n = 16 terminals) in controls | Immunostaining, 2–4 d adults | "In control siblings, gap junction antibody occupies 9.04% (SD, 1.33; n = 16 terminals" ✓FT | Lopez et al. 2025 |
| Which side | each GF: same-side TTMn, plus an interneuron that drives the opposite-side DLM | EM serial sections | "Each giant fibre contacts both a large motor axon and an interneuron." … "The interneuron synapses in turn with the motor neurons that innervate the contralateral dorsal longitudinal flight muscle." ✓ABS | King & Wyman 1980, J Neurocytol [PR] [doi](https://doi.org/10.1007/BF01205017) |
| Dye spread from one GF | same-side TTMn, both PSIs, weakly the other GF. Coupling frequency: brain GCIs 82%, TTMn 61%, PSI 46% (n = 28 fills); *shakB²* 0/15 | Lucifer yellow into one GF axon | "into the ipsilateral TTMn (B, arrowhead), both PSIs (B, arrows)" … "Weak coupling to the contralateral GF is also observed." ✓FT | Phelan et al. 2008 (Table S1 ✓FT) |
| GF–GF coupling | through giant commissural interneurons (GCIs) and midline axon branches; synchrony assumed, never measured | Secondary statements | "The two GFs are electrically coupled together" ✓SEC; "the two GF cells are interconnected at the dendritic level by a group of interneurons (giant commissural interneurons)" ✓SEC | Blagburn 2020; Kadas et al. 2012 [PMC6621333](https://pmc.ncbi.nlm.nih.gov/articles/PMC6621333/) |
| TTMn–PSI | coupled; strength unknown | — | "PSI and TTMn are also electrically coupled." ✓FT | Allen & Murphey 2007 |
| GFC1–4 | electrical synapses at the inframedial bridge; 2/7/5/4 cells per side; no physiology | Neurobiotin fills | "GFC1–4 share a central site of GFI connectivity, the inframedial bridge, where the neurons each form electrical synapses." ✓FT | Kennedy & Broadie 2018, eNeuro [PR] [PMC6325540](https://pmc.ncbi.nlm.nih.gov/articles/PMC6325540/) |
| GFC outputs | GF-coupled premotor neurons synapse only on the largest tibia and trochanter–femur flexor MNs | FANC connectome | "PreMNs that are electrically coupled to the giant fibre exclusively make chemical synapses onto the largest MNs innervating tibia and trochanter–femur flexor muscles" ✓FT | Azevedo et al. 2024, Nature [PR] [PMC11348827](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/) |
| Contralateral loom input | the GF responds equally to looms on either eye, through an unidentified pathway, probably not the VNC coupling | Whole-cell GF recording, ±45° | "responds invariantly to looming stimuli across tested azimuthal locations"; "suggest contralateral visual information is not arriving through this connection as it would be attenuated and delayed" ✓FT | Jang et al. 2023, J Exp Biol [PR] [PMC10263144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10263144/) |
| Another fly mixed synapse, for scale | haltere→B1 MN: EMG 1.72 ± 0.16 ms in wild type, over 2.1 ms in *shakB²* with 17% failures | Haltere nerve stimulation | "Strong stimuli (>50 V) evoke B1 EMGs at short and constant latencies of 1.72 ± 0.16 msec" ✓FT | Trimarchi & Murphey 1997, J Neurosci [PR] [PMC6573327](https://pmc.ncbi.nlm.nih.gov/articles/PMC6573327/) |

### 2.6 How big is one GF spike in the TTMn?

Nobody knows from a measurement. No intracellular TTMn or PSI recording exists in Drosophila (see the Allen & Murphey 2007 quote above; Europe PMC searches found none). Recordings from larger flies (Mulloney 1969; Bacon & Strausfeld 1986) could not be opened. The best available estimate is the Augustin model.

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Model junction conductance | 135 nS young, 34.5 nS old. The paper prints µS, but the code declares nanosiemens | NEURON model: 4 cells, GF 8 × 400 µm | Paper: "Gap junctions conductance (g gap, young fly) 135 μS (estimated)" ✓FT; code `gap2.mod`: "g = 0 (nanosiemens)", "i = (v - vgap)*g*(0.001)" ✓CODE | Augustin 2019 [MODEL]; [ModelDB 245415](http://modeldb.yale.edu/245415) |
| How the model rectifies | one-way coupling: current flows only into the target, no voltage gating. Chemical GF→TTMn and GF→PSI weights are 0 | code | "The GF is modeled as a single active section that forms unidirectional electrical synapses onto the active section (axon) of the PSI and the medial passive section (dendrite) of the TTMn." ✓FT; `'GF_TTMn_wt': 0.00` ✓CODE | Augustin 2019 |
| Model PSI→DLMn synapse | delay 0.15 ms, rise 0.1 ms, decay 1 ms, peak 80 nS (paper prints µS) | code and table | "Chemical synapse delay 0.15 ms (estimated)" ✓FT | Augustin 2019 |
| DERIVED re-run: latencies reproduced | TTM 0.929, DLM 1.440 ms (135 nS); 1.216 and 1.832 ms (34.5 nS) | research agent's NEURON 9.0.2 run of the unmodified code | "g_gap= 135.0: TTMn 0.929 ms DLMn 1.440 ms PSI 0.989 ms" ✓(run output) | this work |
| DERIVED: GF spike size in TTMn | With the TTMn's Na channels blocked, one GF spike (136 mV, 1.43 ms half-width in the model) depolarizes the TTMn by 109 mV (70 mV old); the PSI by 98 mV (60 old). The TTMn needs 35.5–39 mV to fire and the PSI 36–42 mV. Safety factor about 3 (TTMn), 1.9 (old), 2.3–2.7 (PSI) | as above | run output ✓ | this work |
| DERIVED: failure point | the relay fails at 6 nS or less (TTMn) and 10 nS or less (PSI), i.e. g·R_in ≈ 2 | as above | run output ✓ | this work |
| Caveat: model spike too wide | 1.43 ms half-width in the model vs a 0.40 ms spike duration measured in the connective, so the model probably overstates the target's passive depolarization | — | see 2.1 | — |
| GF input resistance | 50–100 MΩ | Whole-cell recording at the soma (a secondary value used as an inclusion criterion) | "the typical input resistance of the GF has been reported to be in the range of 50 to 100 MΩ" ✓SEC | Jang et al. 2023 |
| Another fly electrical input to the GF | Johnston's organ neurons → GF: delay under 300 µs; unitary PSPs 0.5–1 mV at the soma | Whole-cell voltage clamp of the GF | "there is a delay of <300 µs from JON spiking to the onset of currents in the GFN" ✓FT | Lehnert et al. 2013, Neuron [PR] [PMC3811118](https://pmc.ncbi.nlm.nih.gov/articles/PMC3811118/) |
| DLMn (MN5) properties, for the flight branch | R_in 102 ± 12 MΩ, C 43 ± 2 pF (n = 22), so τ ≈ 4.4 ms (DERIVED). The PSI→MN5 EPSP is 4.71 ± 0.35 mV at the soma (n = 10), an underestimate because the synapses sit far out on the axon | Whole-cell patch at the MN5 soma | "the capacitance of these cells was 43 ± 2 pF ( n = 22), and their average input resistance was 102 ± 12 MΩ ( n = 22)"; "was 4.71 ± 0.35 mV ( n = 10)" ✓FT | Fayyazuddin et al. 2006 (MN5 C = 127 ± 16 pF in Ryglewski & Duch 2009 conflicts) |
| DLMn–DLMn coupling | coupling coefficient 0.023 ± 0.003 (MN1–2, MN3–4) vs 0.01 ± 0.0027 (other pairs) | Paired patch in situ | "coupling is twice as strong for the MN1–MN2 and MN3–MN4 pairs (coupling coefficients (CC) = 0.023 ± 0.003)" ✓FT | Hürkey et al. 2023, Nature [PR] [PMC10232364](https://pmc.ncbi.nlm.nih.gov/articles/PMC10232364/) |

### 2.7 Modelling electrical synapses in point neurons, and existing escape models

| Approach or model | What it does | Parameters | Quote ✓ | Source |
|---|---|---|---|---|
| Continuous ohmic coupling | I = g(V_pre − V_post), summed; symmetric | Brian2 example w = 0.02 (fraction of leak) | "Igap_post = w * (v_pre - v_post) : 1 (summed)" ✓CODE | [Brian2 gapjunctions example](https://brian2.readthedocs.io/en/stable/examples/synapses.gapjunctions.html) |
| NEST | symmetric only, delay ignored | — | "Gap junctions are bidirectional connections." ✓FT | NEST documentation; Hahne et al. 2015, Front Neuroinform [PMC4563270](https://pmc.ncbi.nlm.nih.gov/articles/PMC4563270/) ("Secondly the step size of the approach needs to be small" ✓FT) |
| Rectifying junction | I_post = g·G(V_post − V_pre), with G a sigmoid of V_pre − V_post (Gmax 1, vα 8 mV, Gmin 0), fitted to Phelan 2008; instantaneous | g_el 0–9.5 nS | "is an approximation of the experimental rectification data in Phelan et al. (2008)"; "All synapses were modeled as instantaneous." ✓FT | Gutierrez & Marder 2013, J Neurosci [PMC3735893](https://pmc.ncbi.nlm.nih.gov/articles/PMC3735893/) |
| Spikelet kernel | the spike is modelled as an exponential current at spike time; dt 0.01 ms | — | "we model the spikelet as an exponential at the time of spike t j with the same time constant as the IPSC" ✓FT | Tchumatchenko & Clopath 2014, Nat Commun [PMC4243246](https://pmc.ncbi.nlm.nih.gov/articles/PMC4243246/) |
| Typical cortical coupling | g_coup 1 nS (coupling coefficient about 0.1) | — | "The electrical coupling conductance g coup was set to 1 nS" ✓FT | Mancilla et al. 2007, J Neurosci [PMC6673558](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673558/) |
| LIF theory | spike strength and after-hyperpolarization set whether spikelets excite or inhibit | — | abstracts only ✓ABS | Lewis & Rinzel 2003 J Comput Neurosci; Ostojic, Brunel & Hakim 2009 J Comput Neurosci |
| Fly flight MNs | linear non-rectifying junctions of 43.5 pS (heterogeneous case 27–87 pS; 3 nS for "strong coupling") in Brian2 | — | "identical single-neuron models were coupled by linear non-rectifying gap junction currents" ✓FT | Hürkey et al. 2023 |
| GF system, conductance model | one-way coupling 135/34.5 nS; latencies fit young and old flies | see 2.6 | ✓FT/CODE | Augustin 2019 [MODEL] |
| GF–TTMn compartment model | 3 GF compartments plus 1 TTMn; symmetric gap current plus chemical synapse; g_gap a sigmoid of ShakB volume between 34.5 and 135 | Code at github.com/Saint-Sam/Drosophila-Giant-Fiber-Compartment-Model | "Removal of the chemical synapse in the model did not significantly alter synaptic function, as in the wild-type animal." ✓FT | Lopez et al. 2025 [MODEL] |
| Behavioural model | a race between the GF and parallel pathways; no synapse model | — | "The process was well described by a simple model in which the GF circuit has a higher activation threshold than the parallel circuits" ✓ABS | von Reyn et al. 2014, Nat Neurosci [doi](https://doi.org/10.1038/nn.3741) |
| IONOFIELD/FLYCNS [P] | Brian2, MaleCNS, Shiu parameters. One-way ohmic coupling at 0.2 × leak plus a 9 mV spikelet, delivered after 0.8 ms. That misreads the whole brain→TTM latency as the junction delay | TTMn/GF ratio 1.0, lag 0.90 ms; chemical-only arm: 0 TTMn spikes | `G_GAP_RELAY = 0.2`; `("DNp01", "TTMn", True, 9.0, …)`; `gap_delay_ms: float = 0.8  # Tanouye & Wyman 1980` ✓CODE | [github.com/IONOFIELD/FLYCNS](https://github.com/IONOFIELD/FLYCNS) |
| Lulzx/fly-brain [P] | adds a conductance "pulse" of 20 (LIF kernel units) to every TTMn whenever either GF spikes; the jump is triggered by counting GF spikes | no latency reported | `params: { pulse: 20 },   // excitatory conductance deposited per GF spike` ✓CODE | [github.com/Lulzx/fly-brain](https://github.com/Lulzx/fly-brain) |
| kazemi-mahdi/fly-escape-circuit [P] | no gap junctions; TTMn fires through the 90 chemical synapses only after GF bursts, 26–186 ms after the first GF spike | — | from repo audit files ✓ | [github.com/kazemi-mahdi/fly-escape-circuit](https://github.com/kazemi-mahdi/fly-escape-circuit) |
| Pisokas | no escape-circuit paper found; only head-direction, path-integration and robotics papers | — | Europe PMC author search | — |

**Time step (DERIVED).** Spikelets have no stability problem at 0.1 ms. A one-way continuous term with forward Euler is stable for g·R_in < 2τ_m/dt − 1 = 399. Its error stays under about 2% per step up to g·R_in ≈ 35. Exponential integration that holds the partner's voltage over the step is always stable. Instant spikelets through a loop (TTMn↔PSI↔PSI) advance one hop per step.

### 2.8 The TTM and its twitch

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Anatomy | lateral tergum to the trochanter of the middle leg; 22–29 tubular fibres in a single-layer cylinder | Dissection, light and electron microscopy | "It is composed of 22–29 tubular muscle fibers that are arranged circularly, forming a monolayer cylinder." ✓FT | Koenig & Ikeda 2005 |
| Innervation | one giant axon (about 5 µm) plus two fine axons (about 1 µm). MaleCNS has TTMn plus STTMm ("satellite"); FANC counts 3 MNs to the tergotrochanter | EM and light microscopy; connectomes | "Three axons—one giant axon ∼5 μm in diameter and two fine axons ∼1 μm in diameter—were observed to innervate the TTM." ✓FT | Koenig & Ikeda 2005; Azevedo 2024; Cheong 2026 |
| Action | extends the middle legs; one excitatory MN | MANC review | "When stimulated by its single excitatory MN, the TTMn, the TTM rapidly extends the fly's mesothoracic (T2) legs, causing the fly to push off from the ground." ✓FT | Cheong et al. 2026, eLife [PR] [PMC13384506](https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/) |
| Joint | femur extension (coxa–trochanter) comes from the TTM; the femur–tibia joint extends in synergy through the TLM | EMG plus high-speed film | "Femur extension is generated by contraction of the tergotrochanteral muscle (TTM)" ✓ABS | Trimarchi & Schneiderman 1993 |
| One GF spike → one twitch | — | Review statement | "A single action potential in the giant fibre is quickly followed by an action potential in the motoneuron, and then a synaptic potential in the TDT. This causes a single twitch, extending the mesothoracic legs" ✓FT | Elliott et al. 2007, Fly [PR] [doi](https://doi.org/10.4161/fly.3979) |
| One spike patterns everything | — | Dye and physiology | "a single action potential in a CGF axon produces patterned activity in jump and flight muscles" ✓ABS | Koto et al. 1981, Brain Res [PR] |
| Peak twitch force | 101 ± 4.4 µN, probably per leg; 8.2 ms to peak | Tethered female Canton-S, strain gauge under the middle legs, GF-evoked | "The peak force produced by the main jumping muscle of female flies from a wild-type(Canton-S) strain is 101±4.4 μN"; "The force takes 8.2 ms to reach its peak." ✓ABS | Zumstein et al. 2004, J Exp Biol [PR] [doi](https://doi.org/10.1242/jeb.01181) |
| Required force, no catapult | model: takeoff at 5.0 ms, peak 274 µN (137 µN per leg); measured and model forces agree within 40% | Linear force–time model | "the time to take-off is 5.0 ms and the peak force should be 274 μN (137 μN leg–1)"; "the fly does not need to store large quantities of elastic energy in order to make its jump" ✓ABS | Zumstein et al. 2004 |
| No co-contraction | — | Free takeoffs | "flies do not need to cocontract the muscles of their jump legs to store energy before takeoff" ✓FT | Card & Dickinson 2008, Curr Biol [PR] [doi](https://doi.org/10.1016/j.cub.2008.07.094) |
| Force ramp | a 1.3 ms ramp matches Zumstein's dF/dt | Point-mass takeoff model | "The value τ ℓ = 1.3ms results in the gradient d F ℓ /d t consistent with the experimental data" ✓FT | Kolomenskiy et al. 2016, PLoS ONE [MODEL] [PMC4809487](https://pmc.ncbi.nlm.nih.gov/articles/PMC4809487/) |
| Middle legs do the work | two legs 287 ± 17 µm beam deflection vs one leg 184 ± 11 µm; free legs extend 1.3 mm | Ergometer, GF stimulated via the eyes | "much less than the 1.3 mm the leg extends during free take-off" ✓FT | Elliott et al. 2007 |
| Fires once per takeoff | whatever the trigger | Secondary (Trimarchi & Schneiderman 1995b) | "the TTM fires only once at the start of flight, regardless of triggering mode" ✓SEC | Koenig & Ikeda 2005 |

### 2.9 Takeoff kinematics and timing

| Quantity | Value | Preparation | Quote ✓ | Source |
|---|---|---|---|---|
| Leg extension | escape 3.33 ms (IQR 0.46, n = 27); voluntary 5.50 ms (IQR 2.00, n = 16) | Falling black disk, 6000 fps | Table 1 "Leg extension (ms) 5.50 (2.00) 3.33 (0.46)" ✓FT | Card & Dickinson 2008, J Exp Biol [PR] [doi](https://doi.org/10.1242/jeb.012682) |
| Launch speed | escape 0.48 ± 0.01 m/s; voluntary 0.28 ± 0.02 m/s | first 2 ms of flight | "Over the first 2 ms of flight, average COM speeds were 0.48±0.01 m s–1 and 0.28±0.02 m s–1 for escape and voluntary take-offs" ✓FT | Card & Dickinson 2008 JEB |
| Peak acceleration | escape 112 m/s² vertical, 107 m/s² horizontal | same | "Peak vertical acceleration was 57.0 m s–2 (IQR=35.8) for voluntary take-offs and 112 m s–2 (IQR=47.8) for escapes" ✓FT | Card & Dickinson 2008 JEB |
| Angle and pitch | about 45°; head-up in 39 of 43 | same | "a take-off angle of roughly 45° from the horizontal"; "39 out of 43 flies started take-off with a head-up pitching motion" ✓FT | Card & Dickinson 2008 JEB |
| Joints and legs | only the middle legs push; coxo-trochanteric, femoro-tibial and tibio-metatarsal joints extend | Unrestrained flies, high-speed film | "The mesothoracic legs extend at the coxo-trochanteric, femoro-tibial and tibio-metatarsal joints." ✓ABS | Trimarchi & Schneiderman 1995, J Zool 235:211 |
| Short vs long mode | short: less than 7 ms from wing raising to takeoff; long: wings raised at least 7 ms before | FlyPEZ | "the wings are raised at least 7 ms prior to the tarsi leaving the ground" ✓FT; "the 3-ms jump takeoff" ✓FT | Williamson et al. 2018, Cell Rep [PR] [doi](https://doi.org/10.1016/j.celrep.2018.10.048) |
| GF activation → takeoff | 100% of GF-activated flies take off, all short mode | CsChrimson, 50 ms at 3.5 mW/mm² | "This elicited takeoff in 100% of LC6, LC4, or GF-activated flies" ✓FT; "activation of the command-like GF drove nearly 100% takeoff (all short-mode takeoffs)" ✓FT | Williamson 2018; Dombrovski et al. 2023, Nature [PMC9849133](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/) |
| One GF spike is enough | a single GF sodium spike triggers a (short-mode) takeoff | Secondary, citing von Reyn 2014 | "single GF Na+ spikes cause takeoffs (von Reyn et al., 2014)" ✓SEC | von Reyn et al. 2017, Neuron [PR] [doi](https://doi.org/10.1016/j.neuron.2017.05.036) |
| Optogenetic GF latency | GF depolarizes about 0.5 ms after light onset | whole-cell, CsChrimson | "depolarized the GF with ∼0.5 ms latency at 100% power" ✓FT | von Reyn et al. 2017 |
| Photostimulation of GF vs its targets | escape in 63% vs 82% of trials | P2X2 and caged ATP | "elicited escape movements in 63% and 82% of trials, respectively" ✓FT | Lima & Miesenböck 2005, Cell [PR] [doi](https://doi.org/10.1016/j.cell.2005.02.004) |
| GF spike → takeoff | GF spike 18 ms (SD 1.5, n = 7) after light-off; takeoff 25 ms (SD 2) after light-off; so about 7 ms (DERIVED, cross-preparation) | tethered flies (spike) vs free flies (takeoff) | "a single spike on average 18 ms (SD = 1.5 ms) after the lights went off"; "TO occurred on average 25 ms (SD = 2 ms) after the light-off stimulus" ✓FT | Fotowat et al. 2009 |

### 2.10 Simulated jumps and FlyGym facts

| Item | Finding | Evidence |
|---|---|---|
| NeuroMechFly v1/v2, flybody | None simulates a jump or takeoff. flybody uses position actuators on leg joints and torque actuators on wings | full texts searched ✓FT (Lobato-Rios 2022; Wang-Chen 2024; Vaxenburg 2025 [PMC12310536](https://pmc.ncbi.nlm.nih.gov/articles/PMC12310536/)) |
| The only published takeoff leg-thrust model | spring leg, 1.3 ms ramp, about 5 ms push, point mass plus CFD | Kolomenskiy 2016 ✓FT |
| flybench [P] | +1.0 rad on both middle legs' CTr and FTi pitch over 5 ms, held 20 ms; thorax rises about 0.7 mm; feet leave the ground about 6–11 ms after the command. The FTi sign looks wrong (see 1.5) | "+1.0 rad on both middle legs' trochanter–femur and femur–tibia pitch over 5 ms, held 20 ms" ✓(repo RFC) |
| Lulzx/fly-brain [P] | scripted: 30 ms pre-posture, then a 20 ms push (middle femurs 70% and tibias 50% extension, claws released) | "Push \| 20 ms \| Middle femurs 70% and tibias 50% extension" ✓(repo docs) |
| FlyGym 2.1 units and body | mm, g, s; gravity −9810 mm/s²; body mass 1.0 mg | `mujoco_globals.yaml`, `rigging.yaml` ✓CODE; DERIVED sum of masses 0.99978 mg |
| Middle leg | coxa 0.181 mm, femur 0.784 mm, tibia 0.667 mm; neutral CTr −139°, FTi 103° | `rigging.yaml`, neutral pose ✓CODE |
| Demo actuators brainfly uses | position actuators kp 45, force range ±65 µN·mm; adhesion gain 40; joint stiffness 0.05, damping 0.06 | `flygym_demo.complex_terrain.make_locomotion_fly` ✓CODE; forward kinematics printout (DERIVED) |
| Joint signs (DERIVED forward kinematics) | CTr pitch up = femur down (−139° → −80°: femur elevation 38° → −20°; foot 0.9 mm lower). FTi pitch = femur–tibia angle (0° straight, so extension lowers it) | my run in the FlyGym 2.1 venv, kinematics only |
| Muscles in FlyGym | FlyMimic's 15 Hill-type muscles cover only the left front leg; no TTM | `compose/fly/musculoskeletal.py` docstring ✓CODE |

### 2.11 MaleCNS identities and connection counts (local tables)

From `body-annotations-male-cns-v1.0-minconf-0.5.feather`, `brainfly.shiu.counts()` (signed counts, rows postsynaptic) and `brainfly.hybrid.consensus_transmitters()`.

| Neuron | MaleCNS type (= MANC type) | bodyIds L / R | Per side | Soma; exit nerve | Consensus transmitter | Mean inputs |
|---|---|---|---|---|---|---|
| Giant fiber | DNp01, instances "DNp01(GF)_L/_R" | 10010 / 10001 | 1 | brain | acetylcholine | 18,366 |
| Jump MN | TTMn | 804642 / 800146 | 1 | T2; PDMNp | glutamate | 3,016 |
| Satellite TTM MN | STTMm | 830847, 924167 / 801391, 824223 | 2 | T2; PDMNp | unclear | 7,160 |
| PSI | PSI (superclass vnc_efferent) | 802401 / 903327 | 1 | T2; PDMNa | unclear (brainfly signs it excitatory, as the Cha^ts and Dα7 data require) | 5,418 |
| DLM MN5 | DLMn a, b | 801970 / 801295 | 1 | T2; PDMNa | unclear | 10,352 |
| DLM MN1–4 | DLMn c-f | 800718, 800890, 801895, 803013 / 801998, 802544, 803048, 1050014552 | 4 | T1; PDMNa | unclear | 8,607 |
| DVM MNs | DVMn 1a-c (3), DVMn 2a, b (2), DVMn 3a, b (2) | — | 7 in all | T2 (ADMN, MesoAN) and T1 (PDMNa) | glutamate or unclear | 2,700–4,400 |
| GF-coupled interneurons | GFC1 (3), GFC2 (10), GFC3 (13), GFC4 (8) | — | — | T2 (GFC4: T1) | acetylcholine | 280–2,900 |

There is no "DLMn a–e". The five DLM MNs per side are one "DLMn a, b" (MN5) and four "DLMn c-f" (MN1–4). MN5's soma is opposite its muscle, and MN1–4's somata are on the same side as their muscles (Hürkey 2023: "MN5 innervates DLM fibres 5 and 6 on the side contralateral to the MN5 soma" ✓FT). So score DLM output by muscle side, not soma side.

**Chemical synapses among escape neurons** (sum over cells, pre → post):

| Pre → post | Left pre | Right pre | Note |
|---|---|---|---|
| GF → TTMn (same side) | 20 | 70 | none to the other side's TTMn. That is 0.8% and 1.9% of the TTMn's input |
| GF → PSI | L→L 9, L→R 2 | R→L 3, R→R 2 | 0.2–0.3% of the PSI's input |
| GF → DLMn / DVMn | 0 / 4 (DVMn 1a-c L) | 0 / 0 | — |
| GF → GFC1 / GFC2 / GFC3 / GFC4 | both GFs together: 13 / 144 / 97 / 112 | | GFC4 gets 4.95% of its input from the GF |
| GFC2 → TTMn | L→L 206, L→R 9 | R→R 252, R→L 14 | the "GFC2_direct" cells 802551, 802599 (L) and 803025, 907675 (R) carry 73–123 each |
| GFC2 → DLMn a,b / c-f | both sides together: 322 / 463 | | — |
| PSI → DLMn c-f | PSI_L → c-f_R 206 | PSI_R → c-f_L 200 | 24–68 per MN |
| PSI → DLMn a,b | PSI_L → a,b_L 17 | PSI_R → a,b_R 26 | so each PSI drives one side's DLM (MN5's soma is on the other side) |
| PSI → DVMn 3a,b / 1a-c / 2a,b | 21 / 3 / 1 | 30 / 9 / 6 | — |
| PSI → GF (feedback) | L→L 52, L→R 6 | R→R 36, R→L 1 | — |
| TTMn → GFC2 | −28 (L→L) | −1 | glutamate is signed inhibitory |

**The GF's major outputs**, as a share of the target's input (at least 1% and at least 30 synapses; both GFs):

| Target | Share | Synapses |
|---|---|---|
| GFC4 | 4.95% | 112 |
| SAD109 (brain) | 2.77% | 37 |
| IN18B034 | 2.73% | 75 |
| GFC3 | 2.14% | 97 |
| TTMn | 1.49% | 90 |
| SAD096 (brain) | 1.32% | 33 |
| IN18B031 | 1.27% | 44 |
| IN00A062 | 1.06% | 46 |

By count, the top targets are GFC2 (144), GFC4 (112), DNp11 (107), IN06B008 (101), GFC3 (97), TTMn (90) and IN18B034 (75).

- Only 45% of the GF's 2,543 output synapses go to VNC-intrinsic, motor or efferent neurons. The rest go to brain, descending and ascending neurons, whose synapse locations I didn't check.
- The GF gets 8% of its 36,733 input synapses from VNC and ascending neurons. The largest are AN12B001 (−525), AN08B098 (+399), IN00A062 (−257), AN10B019 (+177), IN05B032 (−156) and PSI (+95).
- Cheong et al. 2026 match these types. The GF "contacts the TTMn both directly and indirectly" ✓FT, and "GFC2 groups 13127 and 13645, which we labeled 'GFC2_direct' had relatively strong synaptic outputs onto DLMns, DVMns, and the TTMn" ✓FT.

### 2.12 What the current brain does with these connections (DERIVED)

The current brain is taste_escape's: W_SYN 1.5556 mV per synapse, each neuron's inputs scaled by 1/size, and calibrated biases.

- **PSP size.** A current kick x₀ gives a voltage peak of 0.1575·x₀, 9.2 ms after arrival (τ_m 20 ms, τ_s 5 ms). Arrival is 1.8 ms after the spike.
- **Chemical PSP from one GF spike.**
  - TTMn_R: 3.9 mV (70 synapses, scale 0.227).
  - TTMn_L: 1.6 mV (20 synapses, scale 0.323).
  - PSI: 0.1–0.3 mV.
  - GFC2: 0.1–1.2 mV.
  - None reach threshold, and the TTMn sits under a −5.27 mV bias. Summed over a 50 Hz burst, the right TTMn's peaks would plateau about 7 mV above its resting level. That is still short of the roughly 12 mV its bias and threshold require, even before depression.
- **Other relevant PSPs.**
  - PSI → DLMn: 0.3–1.6 mV, against DLMn biases of −12.5 to −13.4 mV.
  - GFC2_direct → TTMn: 5.8–9.5 mV.
- **Calibrated biases:** GF −15.3, TTMn −5.27, PSI −4.39, GFC2 −4.76, DLMn a,b −13.4, DLMn c-f −12.5 mV. All come from the 2 Hz default target, or 0.1 Hz for the GF.

So without the spikelet layer, the model's GF cannot drive the jump muscle on a single spike, and its flight branch can't fire at all. That matches kazemi-mahdi's finding [P] that the TTMn fired only after GF bursts, tens of ms late.

---

## 3. Gaps and uncertainties

1. **No intracellular TTMn or PSI recording exists.** The 20 mV spikelet rests on a model safety factor. That model's GF spike lasts about 3.5× longer than the measured one, so it probably overstates the drive. Choose the spikelet by the pre-registered reliability rule, not by this number alone.
2. **Tanouye & Wyman 1980 (J Neurophysiol) was not accessible.** It is paywalled, and Europe PMC has no abstract. It is the primary source for the 0.8/1.2 ms latencies and the following limits (TTM >200 Hz, DLM about 100 Hz). Every use here is through later papers that measured the same things themselves (Thomas & Wyman 1984; Engel & Wu 1996; Allen & Murphey 2007; Kadas 2019).
3. **Temperature.** Most papers don't state recording temperature, and absolute latencies differ by 0.2–0.3 ms between labs. Subtractions such as GF conduction time must use latencies from the same preparation. Thoracic latencies are 0.55–0.65 ms in some labs and 0.80–0.97 ms in others.
4. **The residual *shakB²* response.** It is cholinergic, but it may not be monosynaptic (Allen & Murphey 2007 leave a polysynaptic path open). The fraction of responding flies varies: 22% (Phelan 2008), 4 of 7 (Allen & Murphey), 80% of muscles in *shakB²/shakB²* (Baird 1990). So "*shakB²* latency" is a mean over responders.
5. **The PSI→DLMn delay** is 0.3, 0.4 or 0.5 ms depending on the source. The DLM refractory period is 4.6–6.1 ms in direct measurements; the 7–15 ms in the JoVE protocol is a compiled secondary range.
6. **Rectification during a real spike is unknown.** In oocytes it is weak at small voltage differences (1.6×), stronger at steady state (about 5×) and slow to develop (milliseconds). The Augustin model's "rectification" is only one-way coupling.
7. **One GF or both.**
   - Dye coupling between the GFs is "weak", and GF synchrony is assumed but never measured.
   - The claim that "both GFs are normally connected to both TTMns" is second-hand (Godenschwege 2002, citing Phelan 1996).
   - No study shows that one GF spike fires the other side's TTMn.
   - The GF's input from the contralateral eye (Jang 2023) is unidentified in the connectome.
8. **Does looming fire the GF?** Fotowat et al. 2009 (tethered, legs removed) wrote that "these results show that the GF is not activated by looming". von Reyn 2014/2017 and Ache 2019 recorded GF spikes to looms and showed the GF is needed for short-mode takeoffs. The preparations and stimuli differ, which may explain the conflict. It doesn't change the relay test, but it bears on how often a loom should fire the GF at all.
9. **The TTM force time course in a free jump is unmeasured.** Zumstein's 8.2 ms time to peak comes from tethered, near-isometric flies. The latency from TTM potential to force onset was not found in any accessible source, so the 0.5–1.5 ms in 1.3 is an assumption. The GF spike → takeoff interval (about 7 ms) combines two preparations.
10. **Connectome caveats.**
    - GF→TTMn chemical counts are asymmetric (70 vs 20).
    - PSI→DLMn synapses lie on DLMn axons "within a peripheral nerve" (King & Wyman 1980), at or beyond the edge of the reconstructed neuropil, so their counts may be low.
    - Transmitters are "unclear" for PSI and DLMn.
    - Glutamate signs near the TTMn are contested (Cheong 2026).
11. **GFC1–4.** They are coupled by dye and ShakB(N+16) immunostaining, but their strength, direction and physiology are unknown. Kennedy & Broadie 2018 found that GFC2's contacts on the GF terminal bend "rarely" show ShakB, so they are mostly chemical.
12. **The tibia extensor MN.** Its MaleCNS type, and whether the connectome gives it a GF-driven route at 1.5 ms, were not checked. v1 scripts it.
13. **Not accessed (paywall or blocked):**
    - Tanouye & Wyman 1980; Tanouye, Ferrus & Fujita 1981 (GF spike amplitude).
    - Blagburn et al. 1999 full text (plaque and active-zone counts); King & Wyman 1980 full text; Sun & Wyman 1996/1997; Phelan 1996 and 1998 full texts; Jacobs 2000.
    - Gorczyca & Hall 1984; Engel & Wu 1992.
    - von Reyn 2014 full text; Trimarchi & Schneiderman 1993/1995 full texts; Hammond & O'Shea 2007 full texts; Zumstein 2004 full text; Elliott & Sparrow 2012; Peckham 1990.
    - Mulloney 1969 and Bacon & Strausfeld 1986 (the Calliphora GF/TTMn recordings).
    - Lewis & Rinzel 2003 and Ostojic 2009 full texts.
