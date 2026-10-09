# Rung 4: short-term synaptic plasticity by synapse class for the MaleCNS LIF

Compiled 27 Sep 2026 by a research agent. Five literature sub-agents covered: the olfactory circuit; taste and hunger; vision and the giant fiber; mechanosensory synapses, the NMJ and release-probability rules; and models plus the central complex. I then re-found the quoted sentences and table values in the full texts myself (the ✓ marks, about 140), read kazemi's and Lulzx's repos, and did the arithmetic on brainfly's depression rule. I also queried the MaleCNS for the selectors and synapse counts. Drosophila melanogaster only, unless flagged **[other insect]** or **[mammalian]**.

**Conventions**
- **f** and **τ_rec** are the fraction of a presynaptic neuron's output strength left after each spike, and its recovery time constant.
  - They are `depression` and `recovery` in `brainfly/hybrid.py`: one resource per presynaptic neuron, shared by all its outputs.
  - Nagel, Hong & Wilson 2015 fit the same form (A → f·A per spike, recovering toward 1 with τ). So does Izhikevich & Edelman 2008 (x ← p·x).
- **PPR** = paired-pulse ratio (2nd ÷ 1st response).
- **r½ = 1/((1−f)·τ_rec)** is the Poisson rate at which the synapse sits at half strength. It is also the most drive the synapse can ever deliver, in full-strength spikes per second (§0.1).
- Labels:
  - **[PP]** = preprint. **WC** = whole-cell. **RT** = room temperature (20–23 °C).
  - **fig.** = read off a figure by a sub-agent (±10%). I did not re-check these.
  - **derived** = my arithmetic.
  - **✓** = I re-found the quoted sentence or table value in the full text myself.
- **Temperature.** Nearly every synaptic number here is at RT or at an unstated temperature. The one comparison, at the adult DLM NMJ, found recovery about 1.7× faster at 33 °C than at 20 °C (§5.1).
- **Gap in §4.** The taste sub-agent's report was cut off by a safety filter partway through its GRN firing-rate table. Its MN9/PER and hunger-modulation tables never arrived. I did not have them regenerated. §4.3 therefore carries only the summary-level claims that did arrive, marked as unchecked.

---

## 0. Recommendations

### 0.1 What a depression setting does (derived)

hybrid.py's rule (lines 272–274): a spike carries s = 1 − (1 − left)·e^(−Δt/τ), then sets left = f·s. I checked the following closed forms against a direct simulation of that update.
- **Poisson input at rate r:** mean strength per spike x̄ = 1/(1 + (1−f)·r·τ). This is exact.
- **Regular input:** x = (1 − q)/(1 − f·q), with q = e^(−1/(r·τ)).
- **Ceiling:** delivered drive r·x̄ rises toward **r½ = 1/((1−f)·τ)** full-strength spikes per second and never passes it.

| Setting | f | τ_rec (s) | r½ (Hz) | x̄ at 2 Hz | 5 Hz | 20 Hz | 50 Hz | 100 Hz |
|---|---|---|---|---|---|---|---|---|
| **Current rule** (ORN→PN values on every cholinergic neuron) | 0.78 | 0.893 | 5.1 | 0.72 | 0.50 | 0.20 | 0.09 | 0.05 |
| ORN→LN (Nagel & Wilson 2016) | 0.75 | 1.566 | 2.6 | 0.56 | 0.34 | 0.11 | 0.05 | 0.02 |
| ORN→PN unitary fit (Kazama & Wilson 2009) | 0.72 | 2.4 | 1.5 | 0.43 | 0.23 | 0.07 | 0.03 | 0.01 |
| ORN→PN slow nicotinic component alone (Nagel 2015) | 0.91 | 0.629 | 17.7 | 0.90 | 0.78 | 0.47 | 0.26 | 0.15 |
| PN→LHN1 (derived from Kim 2025) | 0.75 | 0.7 | 5.7 | 0.74 | 0.53 | 0.22 | 0.10 | 0.05 |
| **Recommended: uniglomerular PNs** | 0.85 | 0.8 | 8.3 | 0.81 | 0.62 | 0.29 | 0.14 | 0.08 |
| **Recommended: KCs** | 0.5 | 1.5 | 1.3 | 0.40 | 0.21 | 0.06 | 0.03 | 0.01 |
| **Recommended: unmeasured central cholinergic, first try** (= kazemi 10%/200 ms) | 0.9 | 0.2 | 50 | 0.96 | 0.91 | 0.71 | 0.50 | 0.33 |
| Stronger central variant, if loops persist | 0.9 | 0.5 | 20 | 0.91 | 0.80 | 0.50 | 0.29 | 0.17 |
| kazemi 5%/200 ms (stopped seizures at 0.7× gain only) | 0.95 | 0.2 | 100 | 0.98 | 0.95 | 0.83 | 0.67 | 0.50 |
| Izhikevich & Edelman 2008, E→E [mammalian] | 0.6 | 0.15 | 16.7 | 0.89 | 0.77 | 0.45 | 0.25 | 0.14 |
| Larval NMJ type Is (derived, §5.1) | 0.74 | 0.28 | 13.7 | 0.87 | 0.73 | 0.41 | 0.22 | 0.12 |

What this means:
1. **The current rule caps every cholinergic neuron at about 5 full-strength spikes/s.**
   - A relay that needs 100 Hz of LC4 or GRN input gets a twentieth of it.
   - Lowering the drive to realistic rates doesn't rescue it: at 30 Hz, x̄ = 0.15 and the cap still binds.
2. **It also depresses resting coupling** (x̄ = 0.72 at 2 Hz, 0.50 at 5 Hz). That is part of why it calms the loops.
3. **The measured high-release fly synapses really are this depressing.** ORN→PN, ORN→LN and DM1 PN→LHN1 all have r½ ≈ 2–6 Hz. But the evidence puts such depression on a minority of classes (§0.2).
4. **The first-try central default (f 0.9, τ 0.2 s; r½ 50 Hz) is the mildest setting known to stop all self-sustained activity in a Shiu-style MaleCNS LIF** (kazemi, §7.2).
   - It keeps resting coupling (0.96 at 2 Hz) and still cuts 100-Hz runaway to a third.
   - In the same test, recovery over 50 ms failed (6/9 trials still seized), and 100 ms worked at 0.7× gain but not at the published gain.
5. **Depression changes the gain, not only the dynamics.** Shiu's w_syn becomes the *rested* strength. To keep the Shiu-calibrated drive at a typical rate r_typ, multiply rested strength by 1 + (1−f)·r_typ·τ.
   - One calibration point (derived):
     - Shiu's kernel (τ_syn 5 ms, τ_m 20 ms) turns a g-jump into a peak PSP of 0.157 × g. So one synapse gives 0.043 mV, and a 23-synapse ORN→PN connection gives ~1 mV.
     - The real rested unitary ORN→PN EPSP is 6.19 ± 0.45 mV ✓ ([KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/); ~23 EM synapses per connection ✓, [Tobin 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/)), about 6× larger.
     - With ORN depression at 20 Hz (x̄ 0.2) it falls to ~1.2 mV.
   - So Shiu's uniform weight resembles a high-release synapse already depressed to a moderate rate. Adding depression on top of it double-counts it. This is one connection, and PN input resistance differs from the model's.

### 0.2 Recommended parameters by presynaptic class

| Presynaptic class (MaleCNS selector) | f | τ_rec | r½ | Confidence | Basis (details in §§1–7) |
|---|---|---|---|---|---|
| **ORNs** (`ORN_*`, 2,635) | **0.78** (0.72–0.90) | **0.9 s** (0.6–2.4) | 5 Hz | High (phasic component) | <ul><li>ORN→PN, fit to 10 Hz nerve trains: f 0.78, τ 893 ms, n = 19 ✓.</li><li>The synapse has two components: fast f 0.77 / 1006 ms, and a slow nicotinic one f 0.91 / 629 ms (≈20% of the conductance) ✓ ([Nagel 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/)).</li><li>ORN→LN: f 0.75, τ 1566 ms ✓ ([Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/)).</li><li>p = 0.79, N ≈ 51 ✓. "Strong depression at all frequencies above about 50 spikes/s" ✓, but only "about 40%" at 7 Hz in single fibres ✓ ([KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/)).</li></ul> |
| **Uniglomerular PNs** (`*_adPN`, `*_lPN`, `*_vPN`…, 307) | **0.85** (0.7–1.0) | **0.8 s** (0.7–1.8) | 8 Hz | Medium-low: one PN type, and STP depends on the target | <ul><li>DM1→LHN1 (PD2a1/b1) depresses: uEPSPs 1, 0.78, 0.50, 0.53 within ~70 Hz bursts; τ_rec ≈ 0.7 s (fig.); p ≈ 0.3. Derived f ≈ 0.7–0.78.</li><li>The same PN's synapses onto LHN2 (PV5a1) facilitate 2.7–4.3× (p ≈ 0.04) ✓qualitative ([Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/)).</li><li>Other PN→LHN pairs: "modest short-term facilitation" ✓ ([Liu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8825683/)).</li><li>PN→KC: no fly data; locust shows no PPF or PPD ✓ [other insect].</li><li>0.85 averages the depressing and facilitating targets.</li></ul> |
| **KCs** (`KC*`, 4,064) | **0.5** (0.2–0.65) | **1.5 s** (1–2) | 1.3 Hz | Low: one MBON, ex vivo optogenetics | <ul><li>γKC→MBON-γ1pedc PPR at 400 ms ≈ 0.4–0.7 (fig.).</li><li>PPR rises in low Ca²⁺ and falls in high Ca²⁺ ✓, so the depression is presynaptic ([Yamada 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11068490/)).</li><li>KCs fire sparsely, so this barely matters at rest.</li></ul> |
| **Unmeasured central-brain cholinergic neurons** (cb_intrinsic acetylcholine minus the rows above: LH/SLP, AL cholinergic LNs, SEZ interneurons, CX…). **This is the tuning knob.** | **0.9** (0.85–0.95) | **0.2 s** first; up to 0.5 s | 50 Hz (20–100) | Low: no direct data | <ul><li>The measured central cholinergic synapses split: PN→LHN1 and KC→MBON depress; PN→LHN2 and other PN→LHN pairs facilitate.</li><li>The first try is the mildest setting shown to stop all self-sustained states in a MaleCNS Shiu LIF, including at the published gain ✓ ([kazemi STABILITY.md](https://github.com/kazemi-mahdi/fly-escape-circuit/blob/main/STABILITY.md)).</li><li>Measured central recoveries are slower (0.7–1.8 s). If loops persist, lengthen τ before lowering f.</li></ul> |
| — within that: **CX ring-attractor types** (EPG, PEN, PEG, Δ7, PFN…) | 1.0, or τ ≤ 0.1–0.2 s | | | Very low (theory) | <ul><li>No STP has been measured at any CX synapse.</li><li>P-EN→E-PG responses to 30-Hz trains "did not desensitize" across runs ✓ ([Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/)).</li><li>In theory, depression increases bump drift and diffusion ✓ ([Seeholzer 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6493776/)). A depressing ring holds activity only with recovery ≤ 40 ms ✓ ([Chen 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11365315/)).</li><li>CX models get bursts from intrinsic currents, not depression (§3.5).</li></ul> |
| **GRNs** (`LB*`, `PhG*`, `claw_tpGRN`, `dorsal_tpGRN`, `LgLG*`, `WG*`, `SNch*`) | **1.0** (if any: f ≥ 0.9 with τ ≤ 0.2 s) | – | ∞ | Low: no synaptic data. Indirect evidence says the relay is transparent | <ul><li>No STP has been measured at any taste synapse.</li><li>G2N-1's response to three 2-s optogenetic GRN bursts 12 s apart: 2nd/1st 0.99, 3rd/1st 0.88 (sub-agent's calculation from the source data; protocol ✓) ([Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/)).</li><li>Bitter 2N dynamics "closely resemble responses in sensory neurons" ✓ ([Deere 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9873257/)).</li><li>The adaptation lives in GRN firing, so put it in the drive (§4.2).</li></ul> |
| **VPNs** (visual_projection), especially **LC4, LPLC2** | **1.0** (if any: f ≥ 0.95 with τ ≤ 0.3 s) | – | ∞ | Low-medium (indirect) | <ul><li>No paired-pulse data exist at any VPN→DN synapse.</li><li>GF depolarization builds throughout 0.1–0.8 s looms (fig., [Ache 2019](https://doi.org/10.1016/j.cub.2019.01.079)).</li><li>LC11's ACh output sums linearly; its fast adaptation sits upstream ✓ ([Tanaka & Clark 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8716191/)).</li><li>The LC4-dependent GF response survives a median 39–85 volleys at 2–10 Hz ✓ ([Engel & Wu 1996](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579151/)). Its habituation needs Shaker in LC4 ✓ ([Gaitanidis 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/)).</li><li>An optional slow LC4 term is in §2.2.</li></ul> |
| **Giant fiber (DNp01) and other DNs** (descending_neuron; PSI is "unclear" in MaleCNS, so it is already undepressed) | **1.0** | – | ∞ | High for the GF; unknown for other DNs | <ul><li>GF→TTMn follows 10 pulses 100% at 100 and 250 Hz. GF→PSI→DLMn: 84% at 100 Hz, 28% at 250 Hz ✓ ([Allen & Murphey 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1974813/), Table 1).</li><li>The GF synapse is mixed; its chemical part alone follows only 17.5% at 100 Hz ✓.</li><li>MaleCNS calls DNp01 cholinergic, so the current rule depresses the GF's own outputs: TTMn (90 synapses) and the electrically coupled GFC2–4 (derived from `counts()`). kazemi restored TTMn only by exempting the GFs ✓.</li></ul> |
| **JONs** (`JO-*`) and **proprioceptors with electrical/mixed outputs** (FeCO claw/club within `SNpp*`) | **1.0** | – | ∞ | Medium-high (mechanism measured) | <ul><li>JON→GF is electrical: Cd²⁺-insensitive, gone in shakB2, <300 µs delay ✓ ([Lehnert 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3811118/)).</li><li>Most JON input to B1 is electrical ✓ ([Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/)).</li><li>Claw→13Bα is "remarkably tonic (i.e., non-adapting)" ✓ ([Agrawal 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7752136/)).</li><li>In kazemi's model, depression cut the leg reflex at the proprioceptors' own synapses ✓.</li></ul> |
| **Other mechanosensory afferents, chemical only** (`BM*`, `SNta*`) | **1.0** default (0.9 / 0.5 s if needed) | – | ∞ | Low | <ul><li>One bristle spike gives a reliable EPSP ✓.</li><li>A spike train evokes "a single spike in most of the central neurons" ✓ ([Tuthill & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4879191/)). The mechanism is unknown.</li></ul> |
| **Thermo/hygrosensory receptor neurons** (`TRN_*`, `HRN_*`) | ORN-like by analogy, or 1.0 | | | Very low | Two cool-PN types fed by the same receptor cells adapt differently ✓ ([Liu, Mazor & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488797/)). No synaptic data. |
| **Inhibitory neurons** (GABA, glutamate, histamine) | **1.0** | – | ∞ | Medium for AL LNs | <ul><li>LN→LN is "slow and facilitating" ✓.</li><li>GABA-LN→PN acts through GABA-B ✓.</li><li>No depressing inhibitory synapse was found.</li></ul> |
| **Optic-lobe intrinsic, ascending, VNC intrinsic, motor neurons** | 1.0 default | | | Very low | <ul><li>R1–6→LMC transmission *sensitizes* over seconds ✓ ([Zheng 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2628724/)).</li><li>No data for the others.</li><li>Pugliese's VNC walking model has no STP (§7.1).</li></ul> |

### 0.3 The rule

Short-term plasticity in the fly follows the release probability of the **presynaptic class, and often of the target**:
- One DM1 PN axon depresses onto LHN1 and facilitates onto LHN2.
- Transmitter doesn't predict it: cholinergic synapses span strong depression to 4-fold facilitation.
- Synapse count and T-bar number don't either (§5.2).

So assign it by class:
- **Depress** where depression is measured: ORNs, uniglomerular PNs and KCs.
- Give **mild, fast depression** to the unmeasured central-brain cholinergic interneurons that carry the model's loops. This is the tuning knob, with a caution for the CX ring.
- **Leave undepressed:**
  - the feedforward sensory relays with evidence of faithful or electrical transmission: GRNs, JONs, proprioceptors, bristles;
  - the visual projection neurons;
  - the descending neurons, above all the giant fiber;
  - every inhibitory neuron.

Where a relay must carry depression, raise its rested strength by 1 + (1−f)·r_typ·τ. Put sensory adaptation into the sensory drive, not into the synapse. Facilitating classes (PN→PV5a1, other PN→LHN pairs, LN→LN) can only get f = 1 in this model unless a facilitation variable (Tsodyks–Markram U and τ_F) is added. Per-target STP would need one resource per (presynaptic neuron, target class).

In spec form, later entries override earlier ones:
```
"cholinergic":                      {"depression": 0.90, "recovery": 0.2}   # the knob; try 0.5 s next
ORN_* types:                        {"depression": 0.78, "recovery": 0.9}
uniglomerular PN types:             {"depression": 0.85, "recovery": 0.8}
KC* types:                          {"depression": 0.50, "recovery": 1.5}
GRN types, JO-*, SNpp*, BM*, SNta*: {"depression": 1.0}
visual_projection, descending_neuron (incl. DNp01): {"depression": 1.0}   # PSI is "unclear" in MaleCNS, so already undepressed
```
A cleaner selector for the sensory rows than type prefixes: the `class` column of the MaleCNS body annotations (`body-annotations-male-cns-v1.0-minconf-0.5.feather`).
- **Depress (ORN values):** `olfactory` (2,639).
- **f = 1:**
  - `gustatory`: 275 cb_sensory + 1,073 vnc_sensory + 80 sensory_ascending.
  - `mechanosensory`: 1,733 cb_sensory, JONs and bristles.
  - `mechanosensory_tactile`: 2,558.
  - `mechanosensory_proprioceptive`: 1,030 vnc_sensory + 423 sensory_ascending.
  - `chemosensory`: 57.
- **Unassigned:**
  - `hygrosensory` (66) and `thermosensory` (25): ORN-like or 1.0.
  - `unknown_sensory` (1,700): start at 1.0.

### 0.4 The three failures

- **LC4/LPLC2 → giant fiber.** Nothing measured supports fast depression here. Exempt LC4, LPLC2 and DNp01.
  - LC4 and LPLC2 supply 17% and 13% of DNp01's input synapses in MaleCNS (derived from `counts()`).
  - The GF's own outputs relay 1:1 up to 250 Hz.
  - The only documented decrement is slow habituation of the LC4-dependent response: tens of volleys at 2–10 Hz, recovery to ~1 within 5 s, plus a component slower than 120 s. It needs Shaker in LC4.
  - Visual escape habituates after "just ten or so trials of 0.2–0.5 Hz visual stimulation" ✓ ([Engel & Wu 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2730516/)). That is network-level, and GABAergic Ras-MAPK is implicated (§2.2).
- **Sugar → MN9.** Remove GRN depression. Drive the GRNs with an adapting rate instead of tonic 100 Hz Poisson (§4.2), and recalibrate w_syn, which Shiu fit to that 100-Hz drive ✓.
  - If the SEZ interneurons still block the route under the central default, exempt the neurons that get most of their input from GRNs. No data argue against that.
  - `taste_depression.json` (committed) already shows both stages matter. In rung 1's silent brain, depression only on the cholinergic sensory neurons, or on every cholinergic neuron except them, each silenced MN9 (0 Hz vs 39.8 Hz).
  - Lulzx/fly-brain hit the same wall: depression "killed the sugar-to-proboscis pathway" ✓ (§7.2).
- **Recurrent loops (LH/SLP, AL LNs, CX).** Keep the measured depression on ORNs, PNs and KCs, and tune the central default: τ 0.2 → 0.5 s, then f 0.9 → 0.85.
  - The AL's cholinergic LNs are a special case. eLN→PN excitation is "mainly or purely electrical" and weak (coupling ≈ 0.01), while eLN→iLN is cholinergic ✓ ([Yaksi & Wilson 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/)). So the connectome's cholinergic eLN→PN synapses probably overstate lateral excitation.
  - That, and the Krasavietz-LN sign question in [adaptation.md](adaptation.md), are structural fixes that STD only masks.

---

## 1. Sensory → second-order synapses

### 1.1 ORN → PN and ORN → LN

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| ORN→PN, unitary | uEPSC / uEPSP | 29.0 ± 2.6 pA (n = 45); uEPSP 6.19 ± 0.45 mV | In vivo WC, minimal nerve stimulation at 0.033 Hz; 1.5 mM Ca²⁺; temperature not stated | "minimal stimulation of the antennal nerve at 0.033 Hz evoked an average uEPSC measuring 29.0 ± 2.6 pA (n = 45)" ✓ | [Kazama & Wilson 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/) |
| same | Quantal parameters | N = 51.4 ± 7.8, q = 1.05 ± 0.11 pA, p = 0.79 ± 0.02 (DL5, DM4) | Multiple-probability fluctuation analysis | "Mean values are N = 51.4 ± 7.8, q = 1.05 ± 0.11 pA, and p = 0.79 ± 0.02" ✓ | same |
| same | Depression at low / high rates | ~40% at 7 Hz; strong above ~50 Hz. After 4 s at 7 Hz: 15 Hz → ~66% of first test EPSC by ~470 ms; 50 Hz → ~0–10% within ~120 ms (fig.) | same | "(7 Hz), synaptic responses depress by about 40%"; "strong depression at all frequencies above about 50 spikes/s" ✓ | same |
| PN spiking (control) | Intrinsic run-down | None: >100 Hz sustained for 500 ms (104.2%) | same | "final firing rates were 104.2% of the initial rate" ✓ | same |
| ORN→PN, multi-fibre | f, τ (one component) | **f = 0.78, τ = 893 ms** (n = 19 PNs, DM6/VM2) | In vivo WC, 10 Hz antennal-nerve trains | "f = 0.78 and τ = 893 ms" ✓; parameters "fit to the mean normalized amplitude of EPSCs … at 10 Hz" ✓ | [Nagel, Hong & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/) |
| same | Two components | Fast (IMI-resistant): f 0.77, τ 1006 ms. Slow (curare-resistant): f 0.91, τ 629 ms. Conductances 0.22 / 0.06 nS | Pharmacology | "For the IMI-resistant component … f = 0.77, and τ = 1006 ms … for the curare-resistant component … f = 0.91, τ = 629 ms" ✓ | same |
| same | Slow component refit to odor responses | r = 0.0073 per spike (f = 0.9927), τ 33.2 s | Model fit | "Fitted parameters for the slow component were r = 0.0073 spike-1, τA = 33247 ms" ✓ | same |
| same | Adequacy of one component | It predicts transient PN odor responses, but real PNs sustain them | — | "the assumptions of this simple depression model are incorrect" ✓ | same |
| LN → ORN terminals | Presynaptic inhibition onset | Alpha function, τ ≈ 25 ms | ChR2 in LNs | "an alpha function with a time constant of about 25 ms" ✓ | same |
| ORN→PN, unitary (DM4) | α, τ | **α = 0.72, τ = 2.4 s**, at the ORNs' spontaneous rate (~3.4 Hz) | In vivo | "The parameters α = 0.72 and τ = 2.4 s were obtained from a least-squares regression" ✓ | [Kazama & Wilson 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/) |
| ORN→LN | f, τ | **f = 0.75, τ = 1566 ms**; normalized ≈ 0.19 by pulse 20 (fig.) | In vivo WC, 10 Hz trains | "Values of f and τ are 0.75 and 1566 ms for LNs; 0.78 and 893 ms for PNs" ✓ | [Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/) |
| ORN→PN | PPR at 10 Hz; Unc13A dependence | Control ≈ 0.93 (0.45–1.25, fig.); unc13A knockdown → facilitation | In vivo, nerve stimulation | "RNAi-mediated KD of unc13A … produced synaptic facilitation in response to a 10 Hz train" ✓ | [Fulterer 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6436828/) |
| ORN→PN (**conflicting**) | PPR vs interval | WT ≈ 1.5 at 10 ms, 1.2 at 30 ms, ~1.0 at 100–1000 ms (fig.) | In vivo WC; suction-electrode nerve stimulation; 1.5 mM Ca²⁺ | "cacRNAi significantly increased paired-pulse facilitation at short inter-pulse intervals" ✓ (protocol) | [Rozenfeld 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10209050/) |
| ORN→PN | Slow adaptation | PN calcium falls on scales of 1–40 s (by glomerulus); release (Syp-pHTomato) falls in parallel | In vivo 2-photon; 20 °C | "timescales that vary in the range between 1 and 40 s" ✓ | [Martelli & Fiala 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/) |
| ORN→PN | GABA presynaptic inhibition | Early phase GABA-A, late phase (seconds) GABA-B | In vivo | "A GABAB receptor antagonist blocked the late phase of this inhibition, but had only a modest effect on the early phase" ✓ | [Olsen & Wilson 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/) |
| ORN→PN | GABA-B gain | Blocking GABA-B raises the PN input–output slope 105% | Ex vivo brain–antenna, imaging | "increased the slope of the input-output function by 105% with no effect on the offset" ✓ | [Root 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/) |
| ORN→PN | EM synapses per connection | ~23 | EM, DM6 | "unitary ORN→PN connections were composed of about 23 synapses" ✓ | [Tobin 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/) |
| ORN→PN | Ipsilateral vs contralateral | Ipsilateral sEPSCs 39% larger | Paired sister PNs | "ipsilateral sEPSCs were 39% larger than their contralateral counterparts" ✓ | [Gaudry 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3590906/) |

Notes:
- **The Nagel fit over-depresses unitary inputs at low rates.** It predicts a regular 7 Hz steady state of 0.44; Kazama & Wilson 2008 saw ~0.6 in single fibres (derived). The Kazama & Wilson 2009 unitary fit (0.72, 2.4 s) predicts even stronger depression, and I couldn't reconcile the two.
- **The two components make the synapse less depressing at high rates than one component suggests.** With the slow component (f 0.91) the ceiling is 17.7 Hz; the fast one alone gives about 4.

### 1.2 Thermo/hygrosensory afferents

| Synapse | Measure | Value | Prep | Quote | Source |
|---|---|---|---|---|---|
| Cool receptor cells → fast-cool-PNs vs slow-cool-PNs | PN adaptation | Fast-cool-PNs strongly adapting; slow-cool-PNs little adaptation. Synaptic vs intrinsic cause not resolved | In vivo WC | "One type showed strong adaptation to sustained temperature decreases"; "the second type … showed little adaptation" ✓ | [Liu, Mazor & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488797/) |

### 1.3 Mechanosensory afferents (Johnston's organ, bristles, femoral chordotonal organ)

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| JON → GF | Mechanism, latency | Electrical: Cd²⁺ no effect, TTX −95%, abolished in shakB2; <300 µs; bursts at 2× the tone frequency | In vivo WC voltage clamp | "Blocking chemical synapses (200 µM Cd2+) had no effect"; "delay of <300 µs from JON spiking" ✓ | [Lehnert 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3811118/) |
| JON → GF | Second volley | GF less sensitive to the 2nd sound-evoked volley; not chemical (tetanus toxin) | In vivo | "the GF was much less sensitive to SEP2s of any amplitude"; "ruled out by tetanus toxin" ✓ | [Pézier 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4145173/) |
| JON → GF | Innexin | ShakB only | In vivo, ~19 °C | "The only innexin for which RNAi knockdown greatly reduced the strength of the JON-GF connection was ShakB" ✓ | [Pézier 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4833477/) |
| JO-A → GF | EM chemical synapses | 690 in total (type-1 JO-A) | FAFB EM | "690 synapses from type-1 JO-A neurons to the GF neuron in total" | [Kim 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7676477/) |
| JON → B1 / A2 | Nicotinic share | B1 −20 ± 6% (n = 7); A2 −21% (n = 5) | In vivo WC; 1.5 mM Ca²⁺ | "20 ± 6% reduction"; "most of the mechanosensory input to B1 (and possibly A2) cells arrives via electrical synapses" ✓ | [Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/) |
| JON → aPN3 | Response adaptation (mechanism unknown) | τ 1.1 s (push) / 5.2 s (pull) | In vivo WC | "mean τ was 1.1 sec/5.2 sec" | [Chang 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5749228/) |
| Femur bristle → VNC interneurons | Reliability; trains | Reliable single-spike EPSP, latency ~3 ms, MLA-sensitive; a train → a single postsynaptic spike | Paired in vivo recordings | "a single bristle spike produced a reliable excitatory postsynaptic potential"; "a single spike in most of the central neurons" ✓ | [Tuthill & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4879191/) |
| FeCO claw → 13Bα | Adaptation; mechanism | Tonic; MLA/atropine only subtle (gap junctions suspected) | WC; 1.5 mM Ca²⁺; RT | "remarkably tonic (i.e., non-adapting)"; "only subtle effects on 13Bα encoding" ✓ | [Agrawal 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7752136/) |
| FeCO club → 10Ba; club → 9Ba; claw → 13Ba/13Bb | Chemical vs mixed | 10Ba and 13Ba mixed; 9Ba and 13Bb nicotinic | Ca²⁺ imaging + optogenetics; 2 mM Ca²⁺ | "MLA reduced but did not eliminate club-driven calcium signals in 10Ba neurons"; "chemical synapses exhibit adaptation (e.g., synaptic depression), whereas electrical synapses may be more advantageous for sustained synaptic transmission" ✓ | [Chen 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8665017/) |
| FeCO axons | Presynaptic inhibition (not STD) | Movement-encoding axons suppressed during walking/grooming | Behaving flies | "axons of movement-encoding leg proprioceptors are suppressed during walking and grooming" | [Dallmann 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC13070307/) |
| Larval chordotonal / md → A08n and others | STP | None measured | — | — | [Pan 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10089977/) |

### 1.4 Photoreceptor → lamina (graded, histaminergic; flyvis replaces this stage in the model)

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| R1–6 → LMC | Response type | Graded, phasic hyperpolarization | In vivo sharp electrode; 25 °C | "LMCs of WT Drosophila responded to photoreceptor depolarizations with a graded and phasic hyperpolarization" ✓ | [Zheng 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC2151524/) |
| R1–6 → LMC | Adaptation over seconds | LMC output **sensitizes**: τ 5.42 s (dim), 3.74 s (middle), 1.38 s (bright); photoreceptors desensitize | In vivo; 25 °C | "LMCs: dim, τ1 = 5.42 s; middle, τ1 = 3.74 s; bright, τ1 = 1.38 s"; "network adaptation in the time scale >100 ms invariably caused sensitization" ✓ | [Zheng 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2628724/) |
| [other insect] blowfly R → LMC | Light adaptation | Lower synaptic delay, higher contrast gain, lower overall gain | In situ | "decreased synaptic delay and increased contrast gain, but the overall synaptic gain … were reduced" | [Juusola 1995](https://pmc.ncbi.nlm.nih.gov/articles/PMC2216927/) |

No Drosophila paired-flash depression data at R→LMC were found.

---

## 2. Visual projection neurons and the giant fiber circuit

### 2.1 VPN → descending neurons

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| Loom → GF (via LC4 + LPLC2) | Time course | Builds through expansion: peak ~2–8 mV at ~0.1–0.75 s for r/v 10–80 ms; back to baseline ≲0.2 s after expansion stops (fig.) | In vivo WC; 20–22 °C | "Interstimulus intervals were set to 30 s to … avoid habituation" ✓ (protocol only) | [Jang 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10263144/) |
| Loom → GF | Decline mechanism | Repolarization then tonic hyperpolarization at maximum size; persists with LPLC2 silenced, so it is inhibition, not depression | In vivo WC | "the GF depolarizes gradually … but then repolarizes, ending with a tonic hyperpolarization" | [Ache 2019](https://doi.org/10.1016/j.cub.2019.01.079) |
| LC4 + LPLC2 → GF | Share of optic-lobe input | 99.4% (FAFB) | EM | "LPLC2 and LC4 contribute 99.4% of the GF's direct-input synapses from the optic lobe" | same |
| LC4 → GF | Integration | Linear integration of velocity (LC4) and size (LPLC2) inputs | In vivo WC (abstract only) | "Motor program selection and timing emerge from linear integration of these two features within the GF." | [von Reyn 2017](https://doi.org/10.1016/j.neuron.2017.05.036) |
| LC4 → GF (optogenetic) | Escape efficacy | ~25–30% of young flies escape | CsChrimson | "red-light flashes induce escape in ~25%-30% of all animals" ✓ | [Gaitanidis 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/) |
| VPN → GF (functional connectivity) | Protocol | Lobula stimulated every 90 s "to permit recovery" (no STP data) | In vivo WC | "at 90-s intervals to permit recovery between pulses" ✓ | [Dombrovski 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/) |
| LPLC2 → GF | Optogenetic protocol | Single 50 ms pulses every 30 s (no trains) | In vivo WC | "to deliver a 50 ms pulse every 30 seconds" | [Klapoetke 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC7457385/) |
| LC11 → glomerulus | Summation of successive stimuli | ACh output = linear sum for 10 squares at 1/6 s each; fast flicker adaptation sits upstream of LC11 | In vivo 2-photon, GACh3.0 | "no significant difference between cholinergic responses of LC11 … and the linear expectation"; "the fast adaptation to flicker happens upstream of LC11" ✓ | [Tanaka & Clark 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8716191/) |
| LC glomeruli (LC11, LC21, LC17, LC12, LC15) | Visual gain suppression | Attenuated within ~500 ms of saccade-like motion (upstream, not STD) | In vivo 2-photon | "When the saccade occurred within ∼500 ms of the probe response, the probe response was attenuated" | [Turner 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9651947/) |
| VPN → DNp07 / DNp10 | State gating (not STD) | DNp10 visual spiking absent without flight | In vivo WC; 22 °C | "Supra-threshold visual responses were completely eliminated without flight in DNp10" | [Ache 2019 NN](https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/) |
| [other insect] locust DCMD → FETi | Train | Facilitates: 2nd PSP +15 ± 5.2%, 6th +32% at 30 ms intervals | In vivo, 24–27 °C | "the second pulse in the train being 15 ± 5.2% larger than the first" | [Rogers 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC6672987/) |

### 2.2 Habituation of the GF afferent path (the long-latency response, LLR)

The LLR is evoked by electrical stimulation of the eye (retina → optic lobe → LC4 → GF → TTM/DLM). The decrement sits upstream of the GF.

| Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|
| Latency | LLR: TTM 3.37 ms, DLM 3.82 ms (short-latency: 0.94, 1.40 ms) | Tethered Canton-S, 20–25.5 °C | Table 1 | [Engel & Wu 1996](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579151/) |
| Twin-pulse refractory period | LL 86 ms (72–103; n = 37). Short-latency: DLM 5.2 ms, TTM 3.3 ms | same | Table 3 ✓ | same |
| Volleys to 5 consecutive failures (median) | 42 (2 Hz, n = 26); 85 (5 Hz, n = 90); 39 (10 Hz, n = 13) | same | Table 2 ✓ | same |
| Early reliability | Response probability ~0.9–1; first failure after ~15 / 30 / 10 volleys at 2 / 5 / 10 Hz (fig.) | same | — | same |
| Recovery | Full by 120 s; full at 30 s but rehabituates faster | same | "After 30 sec, response probabilities recovered fully, but subsequent habituation was more rapid" ✓ | same |
| Fast recovery | ~1 within 5 s | Review | "robust spontaneous recovery to a probability of about 1 within 5 s" ✓ | [Engel & Wu 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2730516/) |
| Slow component | Recovery takes >120 s after repeated bouts | Tethered | "a long-term component of response decrement … recovers with a time course exceeding 120 sec" ✓ | [Engel 2000](https://pmc.ncbi.nlm.nih.gov/articles/PMC311339/) |
| After 100 volleys | 35% (5 Hz), 0% (10 Hz) | In vivo | "after 100 stimuli response probability is down to 35% at 5 Hz stimulation and down to 0% at 10 Hz stimulation" ✓ | [Gaitanidis 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/) |
| Locus | Needs Shaker (Kv1) in LC4; LPLC2 knockdown minor; TNT in LC4 abolishes the LLR | In vivo | "habituation in the GF escape circuit requires the Shaker Kv1 potassium channel in the LC4 visual projection neurons" ✓ | same |
| Strain/age | Young WT flies often barely habituate over 100 volleys | Tethered, 21–23 °C | "a large fraction of flies showing little habituation throughout the stimulation train" ✓ | [Iyengar 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8805199/) |
| Visual vs electrical | Visual escape habituates in ~10 trials at 0.2–0.5 Hz and recovers more slowly | Tethered | "after just ten or so trials of 0.2–0.5 Hz visual stimulation" ✓ | [Engel & Wu 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2730516/) |
| Light-off jump habituation | Ras-MAPK in GABAergic, not cholinergic, neurons | Freely standing | "Ras-MAPK, in GABAergic but not in cholinergic neurons causes deficits in light-off jump habituation" ✓ | [Fenckova 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7053436/) |
| Overhead shadows | Arousal *grows* over 2–10 passes at 1 s ISI | Free walking | "a scalable increase in peak velocity was observed with an ISI=1 sec, but not for an ISI= 3 sec" ✓ | [Gibson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4452410/) |

**Optional slow LC4 term** (derived, rough; the data are volleys, not LC4 spikes): f_slow 0.98–0.99, τ_slow 3–10 s. Check it against repeated-loom protocols first: at ~100 Hz within a loom it would also cap drive.

### 2.3 GF outputs

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| GF → TTMn (mixed) | Latency; following (10 pulses) | 0.85 ± 0.03 ms; **100% at 100 Hz and at 250 Hz** (n = 6, shak-B2/+) | Intracellular TTM, brain stimulation | Table 1 ✓ | [Allen & Murphey 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1974813/) |
| GF → TTMn, chemical only (shakB2) | same | 1.62 ± 0.17 ms; 17.5 ± 5.5% at 100 Hz; 10.5% at 250 Hz | same | Table 1 ✓ | same |
| GF → PSI → DLMn | same | 1.43 ± 0.07 ms; **84 ± 10.7% at 100 Hz**; 27.6 ± 7.2% at 250 Hz | same | Table 1 ✓ | same |
| GF → TTM / DLM | Following | TTM 1:1 to 300 Hz; DLM to 100 Hz | Protocol review | "the GF-TTM path is able to follow 10 stimuli 1:1 up to 300 Hz and the GF-DLM pathway up to 100 Hz" ✓ | [Allen & Godenschwege 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2946074/) |
| GF → TTMn; GF → PSI → DLMn | Following | TTM 1:1 at ≤200 Hz; DLM follows 50 Hz, not 200 Hz | ~19 °C | "The GF-TTMn connection in controls can follow one-to-one at 200 Hz or less … GF-PSI-DLMn pathway is able to follow at 50Hz … but not at 200Hz" ✓ | [Pézier 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4833477/) |
| GF → DLM | 50% following frequency | ~180 Hz; DLM motor neuron → muscle reliable to 300 Hz | In vivo | "following frequency 50%) is ~180 Hz"; "highly reliable for stimulation frequencies of up to 300 Hz" ✓ | [Gaitanidis 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/) |
| PSI → DLMn (cholinergic, Dα7) | Following; EPSP | Follows GF stimulation up to 100 Hz; EPSP 4.71 ± 0.35 mV | Intracellular DLM; WC MN5 | "able to follow stimulation of the giant fiber at frequencies of up to 100 Hz" ✓ | [Fayyazuddin 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC1382016/) |
| Visual input → GF | Chemical drive | The cholinergic chemical inputs carry a "significant proportion" of the drive | Intracellular TTM | "the chemical synapses onto the giant fiber are cholinergic, and this component provides a significant proportion of the synaptic drive" ✓ | same |
| GF → PSI → DLM, long train | 20 Hz | ~1.0 for ~200 stimuli, ~0.8 by ~400 (fig.) | Tethered | — | [Engel & Wu 1996](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579151/) |
| GF → TTMn / PSI | Rectification | Heterotypic ShakB(N+16)/ShakB(L) junctions rectify (in oocytes) | Xenopus oocytes | "depolarizations were preferentially transmitted in one direction only" ✓ | [Phelan 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2663713/) |
| GF system | Model | Electrical GF→TTMn/PSI (g_gap 135 µS, young) reproduces latencies 0.93 / 1.44 ms | NEURON model | — | [Augustin 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6469880/) |

---

## 3. Central synapses

### 3.1 Antennal-lobe local neurons

| Synapse | Measure | Value | Prep | Quote | Source |
|---|---|---|---|---|---|
| LN → LN (GABA) | Dynamics | "Slow and facilitating": outward current grows over ~0.3–0.4 s while presynaptic firing falls (fig.). The authors allow slow GABA diffusion as an alternative cause | In vivo, ChR2 in ~50 LNs | "excitatory synapses onto LNs are fast and depressing, whereas inhibitory synapses are slow and facilitating" ✓ | [Nagel & Wilson 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4829653/) |
| LN → LN | Unc13 isoform | Unc13B-dominated | In vivo | "LN-LN synapses are rather slow and facilitating" ✓ | [Fulterer 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6436828/) |
| GABA-LN → PN | Receptor | GABA-B (abolished by CGP54626) | Paired WC | "these responses were abolished by CGP54626" ✓ | [Liu & Wilson 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3690841/) |
| Glu-LN → PN | Connectivity | 0 of 65 pairs | Paired WC | "We did not detect any connections from Glu-LNs onto PNs in 65 pairs" ✓ | same |
| GABA onto PNs vs LNs | Receptors | Picrotoxin blocks 46 ± 5% in PNs (the rest is GABA-B), 98 ± 3% in LNs | In vivo iontophoresis | "picrotoxin blocked less than one-half (46 ± 5%) of the GABA-gated hyperpolarization in PNs" | [Wilson & Laurent 2005](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/) |
| LN → ORN terminals | Heterogeneity | From complete suppression of sEPSCs to almost none, by glomerulus | In vivo | "sEPSCs were completely suppressed in the most sensitive PNs" | [Hong & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/) |
| eLN → PN | Mechanism; coupling | Electrical (shakB, Cd²⁺-resistant). Coupling ≈ 0.010 depolarizing / 0.003 hyperpolarizing (fig.) | In vivo dual WC | "eLN-to-iLN synapses are largely cholinergic, whereas eLN-to-PN synapses are mainly or purely electrical" ✓ | [Yaksi & Wilson 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/) |
| eLN ↔ PN (conflicting) | Mechanism | Cholinergic plus gap junctions | Abstract only | "reciprocal excitatory connections mediated by dendrodendritic cholinergic synapses and gap junctions" | [Huang 2010](https://doi.org/10.1016/j.neuron.2010.08.025) |
| Krasavietz LNs | Transmitter | 63% ChAT⁺ ([Shang 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866183/)) vs "mostly GABAergic" ([Seki 2010](https://doi.org/10.1152/jn.00249.2010)) | Immunostaining | — | — |
| Lateral excitation | Saturation | Little change when ORN input rises from 50 to 150 spikes/s | In vivo | "increasing the rate of incoming ORN spikes from 50 to 150 spikes/second had little effect" | [Olsen, Bhandawat & Wilson 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/) |

### 3.2 PN → lateral horn neurons

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| DM1 → LHN1 (PD2a1/b1, sustained type) | Train dynamics; p; N | Normalized uEPSPs 1, 0.78, 0.50, 0.53 (first burst); 0.60, 0.37, 0.32, 0.27 (last 5 bursts); τ_rec ≈ 0.7 s (fig.); p ≈ 0.30; N = 43.0 ± 8.4 (hemibrain) ✓ | Paired in vivo WC; 100-ms pulses at 5 Hz, 7.2 ± 1.1 spikes per pulse (~70 Hz) ✓; 1.5 mM Ca²⁺ | "the first four uEPSPs … in LHN1 exhibited depression, while the first four uEPSPs in LHN2 exhibited facilitation" ✓ | [Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/) |
| DM1 → LHN2 (PV5a1, transient type) | Facilitation plus slow depression | 1, 2.7, 4.1, 4.35 (first burst); τ_fac ≈ 0.05–0.09 s; τ_rec ≈ 1.8 s (fig.); p ≈ 0.04; N = 18.8 ± 4.4 ✓. EGTA and Unc13B RNAi reduce the facilitation ✓ | same | "synaptic depression operates at both synapses and requires more than the 100 msec pause between pulses to fully recover" ✓ | same |
| 135 PN → LHN pairs | Strength; STP | uEPSP 0.4–6.6 mV, scaling with synapse density; example trace shows modest facilitation | Two-photon optogenetic PN stimulation | "Mean uEPSP amplitudes spanned a ~10-fold range (0.4mV to 6.6mV)"; "modest short-term facilitation of this connection" ✓ | [Liu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8825683/) |
| DA1 PN → LHN | Unitary EPSP; latency | ~1 mV (0.5–1.6, fig.); 1.3 ± 0.2 ms | Paired in vivo | "the latency between the PN spike and EPSP onset is 1.3 ± 0.2 msec" | [Jeanne & Wilson 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5488793/) |
| PN → Mz671 LHN | High-rate transfer | Saturates (sigmoid) above ~40–60 spikes per 500 ms, at the synapse (fig.) | Paired/triplet in vivo | "the mechanism of saturation likely resides at the synapse, not the process of spike generation" | [Fişek & Wilson 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3992254/) |

The same PN axon depresses onto one target and facilitates onto another. Kim 2025 note that quantal N matches the hemibrain synapse count at both. So **synapse count sets strength, not the sign of STP**.

### 3.3 PN → Kenyon cells, APL

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| PN → KC | High-rate drive | KC voltage plateaus ~30 ms after onset although PNs keep firing >100 Hz. The cause (depression, inhibition, intrinsic) is not resolved | In vivo WC, ChR2 in Mz19 PNs | "even though PN spiking persisted at >100 spikes/sec, the membrane potential got no closer to spike threshold" ✓ | [Gruntman & Turner 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/) |
| ORN → PN → KC | Summation | EPSPs summate at 10–100 Hz | In vivo; 21–23 °C | "even EPSPs spaced 50 or even 100 ms apart could add up sufficiently to drive spiking" ✓ | [Groschner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/) |
| PN → KC | EPSP decay | Fast (abstract only) | In vivo | "excitatory synaptic potentials (from PNs) decay rapidly" | [Turner 2008](https://doi.org/10.1152/jn.01283.2007) |
| PN terminals in the calyx | Active-zone composition | Unc13B and Syd-1 enriched ("slow"); ORN terminals are BRP and Unc13A-rich | STED | "Unc13A enriched in ORN-derived AZs while Unc13B enriched in PN-derived AZs within the calyx" ✓ | [Fulterer 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6436828/) |
| [other insect] locust PN → KC | Paired-pulse | No PPF or PPD at ISIs of 0–150 ms | In vivo, spike-triggered averages | "No evidence is found for paired-pulse facilitation (or depression)" ✓ | [Jortner 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673743/) |
| APL ↔ KC | STP | None measured | — | — | [Amin 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7541083/) |

### 3.4 KC → MBON

| Synapse | Measure | Value | Prep / temp | Quote | Source |
|---|---|---|---|---|---|
| γKC → MBON-γ1pedc | PPR at 400 ms | ≈ 0.49 / 0.68 / 0.38 in three baseline groups (fig.). Low Ca²⁺ raises PPR; high Ca²⁺ lowers it ✓ | **Ex vivo**; CsChrimson in sparse γ KCs; 1.5 mM Ca²⁺ / 4 mM Mg²⁺ | "delivered two 1-ms light pulses 400 ms apart to measure PPRs" ✓ | [Yamada 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11068490/) |
| KC → MBON-γ1pedc>α/β | Release probability | High; Unc13A-dependent. Primary paper paywalled, so no numbers | — | "transmission and short-term synaptic plasticity at KC-to-mushroom body output neuron γ1pedc> α/β synapses operate with a high SV release probability" ✓ (review) | [Piao & Sigrist 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8762327/), citing [Woitkuhn 2020](https://doi.org/10.1080/01677063.2019.1710146) |
| KC → MBON-γ1pedc | In vivo odor EPSCs | >200 pA, sustained through 1-s odor | In vivo WC | "sustained throughout the duration of the odor pulse" ✓ | [Hige 2015 Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/) |
| α/β KC → MBON-α2sc | Unitary | 8 of 24 pairs with a significant response, 5 judged monosynaptic; ~0.1–0.2 mV steps (fig.) | Paired in vivo | "Out of 24 pairs recorded, we found only eight statistically significant postsynaptic responses. Five pairs were judged as monosynaptically connected" (corrected 2026-10-09; an earlier version of this row misquoted it as 7 of 24) | [Hige 2015 Nature](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860018/) |
| KC → MBON-α′3 | Repetition suppression (dopamine-dependent, minutes) | >50% by the 2nd odor; >80% after 3–7 | In vivo 2-photon | "Over 50% suppression is apparent by the second exposure to odor" ✓ | [Hattori 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806120/) |
| KC ACh release (γ lobe) | Across trials 1 min apart | No adaptation over 10 trials | In vivo GRAB-ACh; 23 °C | "Control animals exhibited no significant olfactory adaptation across the 10 trials in any compartment" ✓ | [Stahl 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8956283/) |
| KC → MBON (β′2, α′3) | Across trials | MBON responses fall while KC responses don't | In vivo imaging | "Responses decrease at the level of MBONs but not at the level of KCs over 10 trials" ✓ | [Pribbenow 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9733945/) |

Derived: with τ 1–2 s, a PPR of 0.4–0.7 at 400 ms implies f ≈ 0.1–0.63. Optogenetic artefacts (fewer KC spikes on the second pulse) could inflate the depression.

### 3.5 Central complex

No paired-pulse, train or recovery measurement exists for any identified CX synapse.

| Synapse | Measure | Value | Prep | Quote | Source |
|---|---|---|---|---|---|
| P-EN → E-PG | CsChrimson trains (30 Hz, 30 pulses) + imaging | Reliable excitation; stable across runs ~2 min apart | Explant, 2 mM Ca²⁺ | "Runs were themselves repeated every 2 min (approximately). When present, responses did not desensitize." ✓ | [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| CX pathways (ring → E-PG and others) | Response vs pulse number at 30 Hz | Saturates by ~20 pulses | Explant, GCaMP6m | "Note that both excitatory and inhibitory responses tend to saturate at 20 pulses." ✓ | [Franconville 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6150698/) |
| R5 → EPG | Paired WC | Unitary nicotinic EPSPs, ~1 ms onset, in 4/30 pairs (8/25 after sleep loss); no STP analysis | Explant | "The EPSP onset time (~1 ms) was comparable to that reported for monosynaptic connections" | [Ho 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9691613/) |
| R5 → EPG (sign conflict) | Optogenetics | EPG hyperpolarized (n = 3) | In vivo | "optogenetic stimulation of R5 induces hyperpolarization of EPG in vivo" | [Raccuglia 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12527942/) |
| Helicon → R2 (R5) | EPSP rate under 2 s of light | 9.44 → 15.33 Hz; depolarization 5.3 mV | WC, fly on ball | "Even single pulses of light could elicit reliable spiking of R2 neurons" | [Donlea 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5779612/) |
| dFB neurons (spike following) | Optical trains | ~1 spike per pulse at 5–20 Hz | WC | "close to 1 at driving frequencies between 5 and 20 Hz" | [Pimentel 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/) |
| dFBN ↔ dFBN [PP] | Glutamatergic inhibition | Monosynaptic IPSPs; sleep loss lowers release over hours (not short-term) | In vivo; RT | "the iGluSnFR signal saturated at lower levels in sleep-deprived than in rested flies" | [Hasenhuetl 2024 PP](https://doi.org/10.1101/2024.02.23.581780) |
| WL-L → R1 | Mixed | Contralateral GABA-A inhibition; ipsilateral dye coupling | In vivo WC | "WL-L neurons are dye-coupled to ipsilateral R1 neurons" | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| dFB neurons | Electrical coupling | Dye-coupled (innexin 6), mostly to pars intercerebralis cells | Dye fill | "the dFB neurons are coupled to other cells via gap junctions" | [Troup 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6117154/) |
| R5 synchrony | Mechanism | NMDA receptors, not gap junctions (abstract) | Voltage imaging | "this synchronization depends on NMDA receptor (NMDAR) coincidence detector function" | [Raccuglia 2019](https://doi.org/10.1016/j.cub.2019.08.070) |
| E-PG / P-EN / Δ7 coupling | — | Untested; EM cannot resolve gap junctions | — | "we cannot rule out the possibility of gap junctions between P-EN and E-PG neurons" | [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |

**Theory**
- "Facilitation decreases both diffusion and directed drifts, while short-term depression tends to increase both" ✓ ([Seeholzer 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6493776/)).
- A depressing rate ring keeps activity only "when the resource recovery rate is sufficiently rapid (α≤40 ms)" ✓ ([Chen 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11365315/)).
- Where CX models burst or oscillate, the mechanism is intrinsic, not synaptic depression: Izhikevich-type R5 neurons, dFBN rebound escape, and T-type Ca²⁺ spikes in PFNa ([Raccuglia 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12527942/); [Hasenhuetl 2024 PP](https://doi.org/10.1101/2024.02.23.581780); [Ishida 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12758628/)).

### 3.6 Descending → VNC and premotor → motor

- **No paired-pulse or train data were found for any DN other than the GF.** Checked: pIP10, DNa02, DNp09, MDN/moonwalker, and the Cande 2018 and Namiki 2018 surveys.
- **Larval premotor → aCC:** connectivity only (1-s optogenetic pulses in TTX) ([Giachello 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9435966/)).
- **Labellar mechanosensory neurons → proboscis MN:** monosynaptic, "approximately 2 ms" delay ✓ ([Zhou 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6531006/)).
- **The GF pathway (§2.3) is the only descending relay with following data, and it is reliable to 100–250 Hz.**

---

## 4. Taste pathway and hunger

### 4.1 Synaptic dynamics and relay behaviour

No short-term plasticity has been measured at any Drosophila taste synapse: GRN→2N, 2N→3N, premotor or MN9, adult or larva.

| Synapse / cell | Measure | Value | Prep | Quote | Source |
|---|---|---|---|---|---|
| Sugar GRN → G2N-1 (2N) | 3 × 2-s optogenetic bursts, onsets 12 s apart | Peak ΔF/F 2.43 / 2.39 / 2.10; 2nd/1st 0.99, 3rd/1st 0.88 (n = 7; sub-agent's calculation from source data) | In vivo 2-photon, Syt::GCaMP7b; Gr5a-LexA > ChrimsonR | "Two-second light pulses were delivered three times at 10 s intervals during imaging" ✓ | [Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/) |
| Sugar GRN → … → Roundup (premotor) | same | 1.49 / 0.90 / 0.69; 2nd/1st 0.64, 3rd/1st 0.47 (sub-agent's calculation). Run-down is downstream of the 2Ns, or is inhibition | same | same | same |
| 2Ns, 3N, premotor, natural stimulus | End ÷ peak ΔF/F, 1 M sucrose ~7 s | G2N-1 0.36, Zorro 0.48, Clavicle 0.46, FMIn 0.42, Phantom 0.25, Rattle 0.86, Bract 0.80, Roundup 0.15 (sub-agent's calculation) | In vivo GCaMP6s, food-deprived | "Taste solutions were in contact with the proboscis labellum from frame 20 to frame 25" ✓ | same |
| Bitter GRN → mlSEZt (2N) | Dynamics vs GRNs | Labellum: transient ON/OFF; leg: sustained ON — as in the GRNs | 2-photon GCaMP6f | "their taste selectivity, response dynamics, and experience-dependent modulation closely resemble responses in sensory neurons" ✓ | [Deere 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9873257/) |
| Pharyngeal sugar GRN → IN1 | Persistence | Fasted, 1 M sucrose: 7 min, decaying to 57 ± 5.7% of peak | In vivo 2-photon | "In fasted flies, 1 M sucrose-evoked activity of IN1 neurons lasted for 7 minutes" ✓ | [Yapici 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544016/) |
| GRNs → SEZ population | Trial-to-trial reliability | 88 ± 1% of responsive cells repeat | Pan-neuronal GCaMP6s; 22 °C rearing | "The repeatability was 88 ± 1% across all two tastant stimulation trials" ✓ | [Harris 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4474761/) |
| GRN transmitter | Identity | Cholinergic (sweet GRNs VGlut-negative); 2Ns express nAChRβ1 | Immunolabelling; RNA-seq | "VGlut is not expressed in water (Ppk28), sweet (Gr64f), or bitter (Gr66a) GRNs" ✓ | [Jaeger 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6181562/); [Mollá-Albaladejo 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12240583/) |
| Taste-circuit models | Gap junctions | Ignored | — | "Gap junctions cannot be identified in the electron microscopy dataset, so we ignore their possibility" ✓ | [Shiu 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/) |
| PER habituation | Mechanism | Stronger GABAergic inhibition, not excitatory depression | Behaviour and genetics | "PER habituation requires an adenylate cyclase-dependent enhancement of inhibitory output of GABAergic neurons" | [Paranjpe 2012](https://doi.org/10.1101/lm.026641.112) |

### 4.2 Real sugar-GRN firing (partial; the rest of this table was lost to the filter)

| Cell | Measure | Value | Prep | Quote | Source |
|---|---|---|---|---|---|
| Labellar L-type sugar GRN, 100 mM sucrose | Rate at 200–700 ms | 85.8 ± 8.5 spikes/s (n = 9) | Tip recording, RT | "(56.2±4.4 and 85.8±8.5 spikes per second, respectively, n=9)" ✓ | [Dahanukar 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC2096712/) |
| same | Shape | Initial burst that decays within ~100 ms, then slower sustained firing | same | "a high rate of initial firing, followed by a quick decay in firing rate over the course of 100 ms" ✓ | same |
| Sweet GRNs [PP] | Mechanism of adaptation | HisCl1-dependent spike-frequency adaptation | Tip recording + optogenetics | "HisCl1 tunes spike frequency adaptation in sweet taste neurons" | [Kim 2024 PP](https://doi.org/10.1101/2024.05.06.592591) |

From the taste sub-agent's summary (sources not delivered, **unchecked**):
- i-b sensilla at 5–50 mM sucrose fire 44–60 Hz in the first second, decaying with τ ≈ 2–3.5 s to 6–7 Hz by 20–30 s.
- Tarsal GRNs at 1 M arabinose fire ~130 Hz in the first 100 ms and ~50 Hz at 1–2 s.
- Spontaneous rate is <2–3 Hz.
- 100-ms light pulses at 1 Hz evoke a PER locked to each pulse. Under continuous light, GRN firing and PER decay together (half-time ~1.5 s).

**Drive recommendation** (sub-agent's, consistent with the rows above):
- Use r(t) = r_ss + (r_pk − r_ss)·e^(−t/τ), with r_pk ≈ 60–90 Hz (up to ~130 Hz in the first 100 ms at high sugar), τ ≈ 2–3 s, r_ss ≈ 6–10 Hz and baseline 1–3 Hz.
- Tonic 100 Hz is realistic only for the first ~0.1–0.5 s.
- Recalibrate w_syn, because Shiu chose it "such that activation of sugar GRNs at 100 Hz resulted in roughly 80% of maximal MN9 firing" ✓ ([Shiu 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/)).

### 4.3 Hunger and neuromodulation (summary-level only; unchecked)

The detailed table was lost. These claims come from the taste sub-agent's summary, and I did not check them.
- **Hunger mainly scales GRN output, not GRN firing.**
  - Sugar-GRN presynaptic Ca²⁺ rises ~1.3–3× with starvation, while spike rate is unchanged in Inagaki 2012. Two other tip-recording studies disagree.
  - The sugar route is dNPF → dopamine → DopEcR on sugar GRNs. The title of [Inagaki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3295637/) confirms "dopamine signaling reveals appetite control of sugar sensing" ✓.
- **sNPF lowers bitter sensitivity and does not act on sugar** (correcting the brief). [Inagaki 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365050/)'s abstract ✓ says only that "orthogonal neuromodulatory cascades … oppositely control peripheral taste sensitivity for each modality". The sNPF/dNPF assignment is unchecked.
- **Behavioural sugar sensitivity shifts ~4.6-fold** with hunger.
- **Hunger also acts at two 2Ns, G2N-1 and Clavicle**, but not further downstream or at MN9.
- Also relevant: [Marella 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310174/) (TH-VUM dopaminergic neuron), and [Yapici 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544016/) (IN1 persistence only in fasted flies ✓, §4.1).

For the model, hunger is a gain on GRN output of order 1.3–3×. It is a multiplier on the GRN presynaptic `scale` or on w_syn from GRNs, not a change in STP. Check the magnitudes in the papers before using them.

---

## 5. Release probability, active zones, and the NMJ (reference)

### 5.1 Neuromuscular junction

| Synapse | Measure | Value | Prep / [Ca²⁺] / temp | Quote | Source |
|---|---|---|---|---|---|
| Larval Is vs Ib (muscle 6) | p per active zone | Is 0.33 ± 0.10 (223 AZ); Ib 0.11 ± 0.02 (747 AZ) | TEVC; HL6, 2 mM Ca²⁺ | "Is: PAZ = QC / NAZ = 72.9/223 = 0.33±0.10; Ib: PAZ = 80.6/747 = 0.11±0.02" ✓ | [Lu 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5253075/) |
| same | Endogenous rate; 10 Hz train | Is fires 7.8 Hz, Ib 20.7 Hz. Mid-train depression at 10 Hz: Is 37.9%, Ib 8.0%. Ib at 22 Hz: 10.5% | same | "(Is: 7.8±0.7Hz; Ib: 20.7±0.8Hz …)"; "(Is: 37.9±1.5% mid-train … Ib: 8.0±2.2%" ✓ | same |
| Ib vs Is | 5 Hz train | Ib facilitates ~100% (192%); Is depresses ~20% (79%); Is p_r 2–3× Ib | Optical quantal imaging; 1.5 mM Ca²⁺ | "At 5 Hz the Ib input facilitated by nearly 100%, while the Is input depressed by ~20%" ✓ | [Newman 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5464967/) |
| Ib vs Is (isolated by BoNT-C) | PPR at 16.7 ms vs [Ca²⁺] | Ib 2.4 / 1.33 / 1.2 / 0.8 and Is 1.2 / 0.75 / 0.82 / 0.72 at 0.4 / 1.8 / 3 / 6 mM (fig.) | TEVC, 10 mM Mg²⁺ | "MN-Ib facilitates at lower Ca2+ levels, consistent with MN-Ib having a lower initial release probability" ✓ | [He 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10286941/) |
| same | Failures at 0.1 mM | Is 63%, Ib 95% | same | "failure rates were 63% at MN-Is NMJs, but 95% at MN-Ib" ✓ | same |
| Larval hemolymph | In vivo [Ca²⁺] | 2.2 mM | CEPIA1er | "determining a [Ca2+] of 2.2 mm" ✓ | same |
| Ib (muscle 4) | PPR at 50 ms; per-site behaviour | EPSC PPR 1.34 ± 0.15; high-p sites depress, low-p sites facilitate | 1.5 mM Ca²⁺ | "Paired-pulse stimulation depresses high-probability sites, facilitates low-probability sites, and recruits previously silent sites" ✓ | [Peled & Isacoff 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC7645962/) |
| Ib AZs | p_r distribution | Mean 0.073 ± 0.002 (n = 1933) | 1.3 mM Ca²⁺ | "an average Pr of 0.073 ± 0.002" ✓ | [Akbergenova 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6075867/) |
| Muscle 6 (Ib + Is) | Pool, p | ~300 readily releasable vesicles; p ~0.5 at 1 mM, ~0.05 at 0.4 mM; brp mutants p 0.08 vs 0.29 | TEVC, 22 °C | "∼300 readily releasable vesicles with an average release probability of ∼50% in 1 mM" ✓ | [Hallermann, Heckmann & Kittel 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2931299/) |
| Muscle 6 | Recovery after 60 Hz | Two components: τ 50 ms and 6.1 s | 1 mM Ca²⁺ | "a biphasic recovery with time constants of τ1 = 50 ms and τ2 = 6.1 s" ✓ | [Hallermann 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC6634796/) |
| Single Ib / Is synapses at 5 Hz | Direction | Ib: 41% facilitate / 40% depress; Is: 28% / 65% | Optical quantal imaging | "Is MNs … release glutamate with ~3-fold higher Pr and tend to depress" ✓ | [Aghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12439520/) |
| Adult DLM NMJ | Recovery from paired-pulse depression | 0.07 s (89%) + 2.07 s (11%) at 20 °C; 0.04 + 1.46 s at 33 °C; p_r ≈ 0.3 at 33 °C | TEVC; 1.8 mM Ca²⁺ | "τfast = 0.07 s (89%) and τslow = 2.07 s (11%) at 20 °C"; "the release probability is ≈0.3 under physiological conditions at 33 °C" ✓ | [Kawasaki & Ordway 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2732793/) |
| Adult DLM NMJ | Steady state vs rate | ≈0.80 (1 Hz), 0.60 (5 Hz), 0.46 (20 Hz), 0.37 (40 Hz) (fig.); PPR at 25 ms ≈ 0.6 | same, 20 °C | — | same |
| Ib vs Is (abstracts) | Trains | Is depresses; Ib facilitates | — | "axon 2 motor terminals show synaptic depression, whereas axon 1 EPSPs facilitate" | [Lnenicka & Keshishian 2000](https://doi.org/10.1002/(SICI)1097-4695(200005)43:2%3C186::AID-NEU8%3E3.0.CO;2-N); [Kurdyak 1994](https://doi.org/10.1002/cne.903500310) |

Derived fits: larval Is ≈ f 0.74, τ 0.28 s; DLM ≈ f 0.7, τ 0.2 s at 20–40 Hz. A single slow exponential fitted at 10 Hz over-depresses at ≥20 Hz, because real recovery has a fast (50–70 ms) component. **Depression is typical of high-p_r terminals, and facilitation of low-p_r terminals, at the NMJ.**

### 5.2 Rules linking release probability, active zones and STP

| Rule | Evidence | Source |
|---|---|---|
| High p_r → depression; low p_r → facilitation | Holds between NMJ inputs (Is vs Ib; tables above ✓), between single active zones ✓ ([Peled & Isacoff 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC7645962/)), and between central targets of one PN (p 0.30 depressing vs 0.04 facilitating ✓, [Kim 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/)) | — |
| BRP/Unc13A-rich terminals are fast and depressing; Syd-1/Unc13B-rich terminals are slow or facilitating | "High BRP/Unc13A levels promoted a high release probability at the first relay synapse of the olfactory system and, consequently, supported a fast but depressing release component" ✓. Unc13A sits ~70 nm from VGCCs, Unc13B >100 nm ✓ | [Fulterer 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6436828/) |
| PN outputs carry both isoforms | "Unc13B is somewhat more abundant than Unc13A at both calyx and lateral horn AZs" ✓; Unc13A promotes "fast phasic signal transfer" ✓ | [Pooryasin 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7997984/) |
| Molecular markers predict p_r *within* an input, not *between* inputs | Cac vs p_r r = 0.74 at single NMJs ✓ ([Gratz 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6435823/)). "VGCC levels are highly predictive of heterogeneous Pr among individual synapses of either low- or high-Pr inputs, but not between inputs" ✓ ([Medeiros 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11410372/)). Is has less BRP yet higher p_r | — |
| Synapse count predicts strength, not STP | Quantal N ≈ EM synapse count ([KW08](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/), [Tobin 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440167/), Kim 2025 ✓). uEPSP scales with synapse density ([Liu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8825683/)). Ib has ~3× Is's active zones yet facilitates | — |
| Transmitter doesn't predict STP | Cholinergic synapses: ORN→PN strongly depressing; DM1→LHN2 facilitating 4×; PSI→DLMn follows 100 Hz; LC11 linear | this file |
| [Ca²⁺] shifts the balance | Low Ca²⁺ → facilitation; at 1.8–2.2 mM Ib facilitates and Is depresses ([He 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10286941/) ✓) | — |
| [mammalian] The same p_r rule | Dobrunz & Stevens 1997 | [doi](https://doi.org/10.1016/s0896-6273(00)80338-4) |

**Consequence for the model:** the connectome can't assign STP from synapse counts, T-bar numbers or transmitter. Assign it by presynaptic class, and ideally per target class.

---

## 6. Electrical synapses (none reported to depress; absent from EM connectomes)

| Connection | Evidence | Size | Source |
|---|---|---|---|
| JON (JO-A/B) → GF | Cd²⁺-insensitive, abolished in shakB2, ShakB(N+16) required presynaptically ✓ | 12–13 coupled JO-A axons; unitary PSPs ~0.5–1 mV | [Lehnert 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3811118/); [Pézier 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4833477/); [Blagburn 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6946141/) |
| JON → B1 / A2 | "most of the mechanosensory input … arrives via electrical synapses" ✓ | Nicotinic share ~20% | [Azevedo & Wilson 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5771506/) |
| FeCO claw → 13Bα; claw → 13Ba; club → 10Bα / 10Ba | MLA-resistant, or only partly MLA-sensitive ✓ | — | [Agrawal 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7752136/); [Chen 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8665017/) |
| GF → TTMn (mixed), GF → PSI (electrical), PSI ↔ TTMn, GF ↔ GF via GCI, GF ↔ GFC1–4 | shakB2 abolishes the DLM path; the chemical part alone is labile ✓ | TTMn 1:1 to 250–300 Hz | [Allen & Murphey 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1974813/); [Kennedy & Broadie 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6325540/) |
| eLN → PN; eLN → iLN; sister PN ↔ PN | shakB-dependent; depolarization passes better than hyperpolarization ✓ | Coupling ≈ 0.01–0.03 | [Yaksi & Wilson 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/); [Kazama & Wilson 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/) |
| HS/VS ↔ HS/VS, HS–H2, HS/VS → DNHS1 / DNOVS1 / DNOVS2 and neck MNs | Dye coupling; HS–DN coupling survives Flp-shakB | — | [Suver 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5125229/); [Pokusaeva 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11470938/); [Ammer 2022](https://doi.org/10.1016/j.cub.2022.03.040) |
| DLM motor neurons 1–5 | Weak coupling ✓ | CC 0.023 ± 0.003 (MN1–2, MN3–4); 0.01 for other pairs | [Hürkey 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10232364/) |
| Larval motor neurons → CPG | Lost in shakB2 or ogre2 | — | [Matsunaga 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC6705691/) |
| dFB neurons; WL-L → R1 | Dye coupling (innexin 6 in dFB) | — | [Troup 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6117154/); [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| LC17 dendrites [PP] | shakB highly expressed, needed for tracking | — | [2025 PP](https://doi.org/10.1101/2025.10.14.682373) |
| LC4 / LPLC2 → GF | **No evidence** of coupling. The looming drive is chemical: TNT in LC4 abolishes the LLR ✓; restoring Dα7 in the GF rescues it ✓ | — | [Gaitanidis 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12707685/); [Fayyazuddin 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC1382016/) |

In the model, the MaleCNS carries these pathways, if at all, as cholinergic chemical synapses. Under the current rule they therefore depress.
- GF→TTMn: 90 chemical contacts (kazemi's count).
- JO→GF: 545 synapses from JO-B1_a in MaleCNS (derived); 690 from type-1 JO-A in FAFB ([Kim 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7676477/)).

Exempting these presynaptic types is the closest the per-neuron rule can get to a gap junction.

---

## 7. How other models handle short-term plasticity

### 7.1 Published fly models

**Almost all fly network models use static synapses.** No fly whole-brain model uses STP that differs by synapse class.

| Model | Scope | STP | How they got stability or relays | Source |
|---|---|---|---|---|
| Shiu 2024 (and 2023 [PP]); reused unchanged by Sapkal 2024, Walker 2025, Christie 2026 | FlyWire LIF | None: g += w, τ 5 ms | Zero baseline firing; 1-s trials; one free parameter w_syn, fit to sugar → MN9 at 100 Hz ✓ | [PMC11446845](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/); [code](https://github.com/philshiu/Drosophila_brain_model) |
| **Huang 2018 (Lo lab, Flysim)** | FlyCircuit, 20,089 neurons, conductance LIF | **Uniform STD on every synapse**, τ_D swept 0–1000 ms (their S1 table cites 893 ms from Nagel 2015) | Stronger inhibition alone never stopped the seizures. With STD and I/E factor 10, prevalence fell to ≤50% once τ_D > 125 ms; it failed on a randomized brain | "We implemented STD in every synapse of the fruit fly brain network and set the I/E factor equal to 10"; "the prevalence dropped to 50% or lower when τD was >125 ms" ✓ [PMC6335393](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335393/) |
| Pugliese 2025 [PP] | MANC front-leg VNC, 4,604 neurons, rate model | None; no adaptation | Rectified tanh, r_max ~200 Hz; gain and threshold scaled by size; synapses <5 dropped | [doi](https://doi.org/10.1101/2025.09.12.675944); [code](https://github.com/smpuglie/Pugliese_cpg_2025) |
| Lappalainen 2024 (flyvis) | Optic lobe, graded | None ("instantaneous graded synaptic release") | Task-trained | [PMC11525180](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/) |
| Pospisil 2024 (effectome); Bates 2026 (BANC influence) | Linear models | None | Largest eigenvalue rescaled to 1 or 0.99 | [PMC11446844](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446844/); [PMC13518251](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/) |
| Turner, Mann & Clandinin 2021 | Resting-state FC | No dynamical model (regression) | — | [PMC8519013](https://pmc.ncbi.nlm.nih.gov/articles/PMC8519013/) |
| Kakaria & de Bivort 2017 | PB–EB ring, 60 LIF | None (fixed PSC template) | Global inhibition, hand-tuned | [PMC5306390](https://pmc.ncbi.nlm.nih.gov/articles/PMC5306390/) |
| Turner-Evans 2017/2020; Pisokas 2020; Noorman 2024; Mussells Pires 2024; Westeinde 2024; Givon 2017; Stentiford 2024; Kim 2019; Fisher 2022 | CX | None (long-term Hebbian at most) | Global inhibition, fine-tuning | [PMC5440168](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/); [PMC7419142](https://pmc.ncbi.nlm.nih.gov/articles/PMC7419142/); [PMC11537979](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/) |
| Su 2017 | EB–PB conductance LIF | None | The bump needs slow, saturating NMDA synapses | [PMC5529380](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/) |
| Chang, Huang & Lo 2023 | Connectome CX LIF | None; STP planned "to increase the robustness of our models" | — | [PMC10353971](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353971/) |
| Vafidis 2022 | Head-direction learning | None; saturation stands in for depression | — | [PMC9286743](https://pmc.ncbi.nlm.nih.gov/articles/PMC9286743/) |
| Olsen, Bhandawat & Wilson 2010 | ORN → PN normalization | Static saturating function; the saturation "reflects the combined effects of short-term depression at ORN-PN synapses and the relative refractory period of PNs" ✓ | — | [PMC2866644](https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/) |
| Nagel 2015; Kazama & Wilson 2009; Liu 2021 | ORN → PN | Depletion depression (1–2 components); binomial release; Tsodyks–Markram facilitation + depression | — | [PMC4289142](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289142/); [PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/); [PMC8568954](https://pmc.ncbi.nlm.nih.gov/articles/PMC8568954/) |
| Kennedy 2019 [PP]; Rapp & Nawrot 2020; Betkiewicz 2020; Jürgensen 2021 [PP]; Nanami 2024 | MB / olfactory spiking models | None; spike-frequency adaptation instead (ORNs, KCs), slow GABA | — | [doi](https://doi.org/10.1101/783191); [PMC7668073](https://pmc.ncbi.nlm.nih.gov/articles/PMC7668073/); [PMC7294456](https://pmc.ncbi.nlm.nih.gov/articles/PMC7294456/); [PMC11238178](https://pmc.ncbi.nlm.nih.gov/articles/PMC11238178/) |
| Kim 2025 | PN → LHN | Tsodyks–Markram: depression only (LHN1); depression + facilitation (LHN2) | — | [PMC12235717](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235717/) |

### 7.2 Whole-CNS GitHub projects (not peer-reviewed; all hit the same trade-off)

**kazemi-mahdi/fly-escape-circuit** (MaleCNS v1.0, Shiu LIF). Depression was applied to every neuron, inhibitory ones included ✓ ([STABILITY.md](https://github.com/kazemi-mahdi/fly-escape-circuit/blob/main/STABILITY.md)).

| Setting | Seizures stopped (0.7× gain / published gain) | Motor output |
|---|---|---|
| 2% per spike, 200 ms | none / none | little change |
| 5%, 200 ms | 9/9 / none | TTMn 2.33 → 1.33 |
| 10%, 50 ms | 3 of 9 (6/9 still seized) / none | — |
| 10%, 100 ms | 9/9 / none | — |
| 10%, 200 ms | 9/9 / 4/4 | TTMn 0.67, leg 27 → 15 |
| 10%, 500 ms | 9/9 / 4/4 | — |
| **10%, 200 ms, giant fibres exempt** | 9/9 / 4/4 | **TTMn 2.67** |
| 20% or 40%, 200 ms | 9/9 / 4/4 | TTMn 0; wing 117.5 → 77.5 / 38 |

- The leg reflex lost output "either way": "the proprioceptors' own synapses tiring under 200 ms of 60 Hz drive" ✓.
- The authors report the GF exemption without adopting it, because it was "chosen because it restores the result we wanted" ✓. The literature (§2.3, §6) now supports it independently.

Other projects:
- **[Lulzx/fly-brain](https://github.com/Lulzx/fly-brain)** (embodied, ~165k LIF): "Spike-frequency adaptation and short-term depression: stabilised activity but killed the sugar-to-proboscis pathway" ✓. In their ablation fit, "the fit chose to leave both off" ✓.
- **[neurofly](https://github.com/neuroflyapp/neurofly):** STD "cut the stimulus responses to a few Hz", so they capped single-edge strength at 0.5 of threshold instead.
- **[brandoncho369/flybench](https://github.com/brandoncho369/flybench):** no STD. They used a global gain of 0.45 plus adaptation of 2 mV per spike (200 ms).
- **[lyutvs/flymon](https://github.com/lyutvs/flymon):** depression at ORN→PN only.

### 7.3 Class-specific templates from large mammalian models [mammalian]

| Model | Rule | Classes | Source |
|---|---|---|---|
| Izhikevich & Edelman 2008 (10⁶ neurons) | Exactly brainfly's form: "ẋ = (1 − x)/τx, x ← px when presynaptic neuron fires"; x is "different for each presynaptic cell" ✓ | **Depressing:** RS/FS → RS and FS, p 0.6, τx 150 ms (r½ 16.7 Hz); TC → RS p 0.7 / 150 ms; TC → FS p 0.5 / 200 ms. **Facilitating:** RS → LTS, p 1.5 / 100 ms. **No STP:** outputs of LTS cells ✓ | [PMC2265160](https://pmc.ncbi.nlm.nih.gov/articles/PMC2265160/) (SI Fig. 11) |
| Blue Brain (Markram 2015; Ecker 2020 CA1) | Tsodyks–Markram U, D, F | E1/I1 facilitating, E2/I2 depressing, I3 pseudo-linear. Example E2 (PC → PC): U 0.5 ± 0.02, D 671 ± 17 ms, F 17 ± 5 ms ✓ | [PMC7687201](https://pmc.ncbi.nlm.nih.gov/articles/PMC7687201/) |

For comparison, derived: the current fly rule has about the same per-spike depression as the mammalian depressing classes, but recovers 4–6× more slowly than Izhikevich's 150 ms.

---

## 8. Searched and not found

- **VPN → DN STP.** No paired-pulse, train or recovery data at LC4, LPLC2, LC6, LC10, LC11, LC16 or LPLC1 outputs. No GF recordings under optogenetic LC4/LPLC2 trains, or under repeated looms at short intervals (papers only state the 10–30 s intervals they chose).
- **Taste.** No STP at any taste synapse, and no evidence for or against electrical GRN synapses. The sub-agent's GRN firing, MN9/PER and hunger tables were lost to a safety filter (§4); they need a separate pass if wanted.
- **Mechanosensory chemical synapses** (JON, bristle, FeCO, campaniform, hair plate): no train data. No coupling coefficients for JON–GF or FeCO–13B.
- **Descending → VNC** (other than the GF), **larval premotor → MN**, **adult leg or abdominal NMJ:** no STP data.
- **PN → KC and APL ↔ KC:** no fly paired-pulse or train data. **LHN output synapses:** none.
- **Central complex:** no measurement at any identified synapse.
- **Temperature dependence of central STP:** none; only the NMJ (§5.1).
- **ORN → PN recovery curves at variable intervals:** none; every f/τ comes from fits to trains. The low-rate discrepancy between the unitary (Kazama & Wilson 2008/2009) and multi-fibre (Nagel 2015) values is unresolved.
- **A fly whole-brain model with class-specific STP:** none, peer-reviewed or on GitHub (~15 repos checked).
- **Could not read in full:** von Reyn 2014/2017, Tanouye & Wyman 1980, Allen 2006 (review), Blagburn 1999, Kittel 2006, Böhme 2016, Woitkuhn 2020, Turner 2008, Inada 2017, Huang 2010, Seki 2010, and the Kim 2017 (Science) supplement. Their values here come from abstracts or secondary sources.
