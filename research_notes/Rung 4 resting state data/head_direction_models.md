# Rung 4: a head-direction bump in the MaleCNS LIF. Connectome-constrained compass models, mechanisms and physiology

Compiled 27 Sep 2026 by a research agent: five literature sub-agents (classic models, connectome-era models, model code, mechanisms, physiology), plus my own analysis of the local MaleCNS tables and toy simulations in the rung-1 LIF. *Drosophila melanogaster* unless flagged **[other insect]**.

**Conventions**
- **[PP]** = preprint. **[non-PR]** = GitHub project, not peer reviewed (anecdote only). **fig.** = read off a figure (±10%). **derived** = arithmetic on published numbers. **mine** = my analysis of the MaleCNS v1.0 flat connectome in `~/fly-data` ([FlyEM release](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome); [Berg et al. 2025 [PP]](https://doi.org/10.1101/2025.10.09.680999)). **toy** = my simulation (§2).
- Names: EPG = E-PG; PEN_a = P-EN1; PEN_b = P-EN2; PEG = P-EG; Delta7 = Δ7; ER1–6 = ring neurons R1–R6; ExR = extrinsic ring neurons. Liu 2016's "R2" is ER5.
- **Strength** = the repo's bump measure (population-vector length per PB side over 8 glomeruli in 1-s windows; ≈0.7 for a real ~100° bump). **EB PVL** = the same over the 16 EB wedges.
- **Rung-1 weights**: 1.5556 mV × signed count / size(target). Mean drive per Hz = weight × 5 ms.
- **EB wedge of an EPG** (mine, from EPG→EPG contacts): glomerulus R_k → wedge 2k mod 16, L_k → (19 − 2k) mod 16, in 22.5° steps. EPG R2 thus sits between L8 and L7.

---

## 0. Recommendations

### 0.1 Why there is no bump

1. **No published model gets a bump from synapse counts × one weight.**
   - "All tested models failed if we simply set the synaptic weights proportional to these numbers" ([Chang, Huang & Lo 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353971/), spiking).
   - "the central complex connectivity alone does not guarantee stable attractor dynamics" ([Beiran & Litwin-Kumar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12648571/)). Their network is the same 152 hemibrain cells as ring_alone.
   - "global parameter tying fails to recover attractor behavior" ([Duan, Dong & Fiete 2025 [PP]](https://doi.org/10.1101/2025.05.26.655406)).
   - Exact attractors need a separate scale factor per cell-type pair ([Biswas et al. 2024 [PP]](https://doi.org/10.1101/2024.11.01.621596)).
   - Shiu-style whole-brain runs on MaleCNS show no bump at unit gains: the ring is "0.0 % active" ([flybench [non-PR]](https://raw.githubusercontent.com/brandoncho369/flybench/master/docs/FINDINGS.md)), and no bump in [flyverse-core [non-PR]](https://github.com/tel-0s/flyverse-core/blob/959f2e927b1c2806bc526fd5fc51cb3f5cc3e4b1/docs/audits/cx_wedge.md#L14-L18).
2. **EPG input is ~74% inhibitory and dominated by flat ring-neuron input** (mine, model matrix, 4,222 synapses per EPG):
   - ER 63.8%, ExR 11.4%, PEN_a 7.4%, EPG 5.9%, PEN_b 5.0%, Delta7 2.2%.
   - Recurrence (EPG + PEN_a + PEN_b) is 18.3% (17.6% of raw counts). The brief's ~13% matches EPG + PEN_a alone (12.9% raw).
   - Hemibrain and FlyWire agree: ER 58.6–58.7%, recurrence 18–20%, Delta7 2.5–3.9% (derived by sub-agents from the [hemibrain v1.2 export](https://storage.googleapis.com/hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz) and [FlyWire v783](https://zenodo.org/records/10676866)).
3. **Ring-neuron inhibition carries no bump structure, but it is the only activity-dependent global inhibition EPGs get.**
   - ER→EPG counts are flat across the 16 wedges (CV 0.12–0.22). Every neuron of the large ER types contacts all 16 wedges (mine, §1.4).
   - EPGs drive the inhibitors: EPG supplies 52% of ExR6 input, 38% of ER6, 17% of ER4m and 18% of ExR4 (mine).
   - ring_alone removed exactly this loop. In the toy, the 152-cell ring runs away (EPG 170–270 Hz) at every inhibitory gain up to ×4, even with slow synapses and depression. Adding the 308 ER/ExR cells stops the runaway (§2).
4. **With 5 ms synapses the ring holds no seeded bump at any gains I tried** (toy). The only strong fast-synapse bump ran at ~130 Hz and pinned 120° from the seed. Every working spiking model used one of two things:
   - Slow excitation: NMDA τ 100 ms, which works down to ~50 ms and fails at 10 ms ([Su et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/)); 100 ms excitatory / 50 ms inhibitory ([Stentiford et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11349202/)).
   - Suprathreshold relays: one PEN→EPG connection ≈ the 7 mV threshold gap ([Pisokas code, derived](https://github.com/johnpi/eLife_Pisokas_Heinze_Webb_2019/blob/dfb95dfeaad0da2df0f7f687846d4df44079a483/Exp_Recurrent_PB_EB/collect_stats_long_run.m#L394-L413)).
5. **A self-sustained bump in this LIF sits at ≥100 Hz unless something caps the drive.** This is the ignition result in adaptation.md §0.1. In the toy, slow synapses alone gave bumps at 90–350 Hz; adding short-term depression brought them to 20–40 Hz.
6. **Wiring facts that change what the model's loops do** (mine unless cited):
   - **The PEN loop is mostly unshifted.** ≥84% of EPG→PEN_a synapses come from EPGs in other PB glomeruli than the PEN's own, so they are EB "hyper-local" contacts ([Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). The two-step EPG→PEN→EPG kernel peaks at 0° with only a slight left/right skew. The ±45–67° shift lives in PEN→EPG and in the minority PB EPG→PEN synapses (hemibrain EB:PB ≈ 3:1, derived by sub-agent).
   - **Delta7 inhibition is a clean cosine but mostly misses EPGs.** EPG→Delta7→target is a cosine (R² 0.98) peaking 180° away. It lands mostly on PEN_b (17.4% of its model input) and PEG (19.7%), not EPG (2.2%). Delta7→Delta7 is 53% of Delta7 input.
   - **GLNO is dropped.** It is the angular-velocity input: 23.2% of PEN_a and 15.5% of PEN_b raw input. Its consensus transmitter is "unclear", so fast_network drops it. FlyWire predicts GABA in 3/4 cells (derived by sub-agent), and GL-N1 neurons inhibit PENs ([Franconville 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6150698/)).
   - **LPsP may have the wrong sign.** The MaleCNS consensus calls it acetylcholine, but it is dopaminergic ([Eckstein 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11106717/); [Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/)). In the model it supplies 2.0% of EPG, 8.3% of PEN_a, 14.5% of PEG and 12% of EPGt input.

### 0.2 Recipe: the ring sub-network first, then embed

This recipe was validated only in the 460-neuron ring + ER + ExR sub-network (rung-1 weights, Poisson background 200 Hz × 1 mV, bias 0; §2). It has not been tested inside the whole brain.

| Step | Setting | Evidence |
|---|---|---|
| **1. Include ring neurons** | All 282 ER and 26 ExR cells with their MaleCNS wiring | The only activity-dependent global inhibition EPGs get. Toy ring-only runs away. Without ring neurons "no activity bump could be formed" ([Su 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/)). Ablating them gives more drift ([Duan 2025 [PP]](https://doi.org/10.1101/2025.05.26.655406)). Ring-neuron models are more robust, with bumps of 0.73π vs 1.23π for Delta7-only ([Chang 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353971/)) |
| **2. Slow ring excitation** | Edges from EPG, EPGt, PEN_a, PEN_b and PEG onto the six ring types go through a τ = 100 ms current, with weight × 0.05 to conserve charge (HybridBrain `slow`, `tau_slow`). Everything else stays at 5 ms | Toy: required; fast-only never persists, with or without depression. [Su 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/) works at ≥50 ms. [Stentiford 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11349202/) uses 100/50 ms. [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) τ = 80/65 ms; [Vafidis 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9286743/) τs = 65 ms. EPGs express Nmdar2 (≈69 vs 48 whole brain; [GSE155329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155329), derived), but no slow receptor has been tested for the bump |
| **3. Cap the rate** | Short-term depression on outgoing synapses of EPG, EPGt, PEN_a, PEN_b and PEG: `depression` 0.9, `recovery` 0.3 s. Steady efficacy ≈ 1/(1 + 0.03·r) (derived) | Toy: top wedge falls from 90–350 to 20–40 Hz. With 0.95, or recovery 0.1 s: 50–95 Hz. With ≤0.8, or recovery 1 s: no persistence. **No STP has been measured at any central-complex synapse** (mechanisms sub-agent), so this is a modelling device. Alternatives: saturating NMDA (Su: without saturation the working window shrank to 0.08–0.09× weight), or adaptation |
| **4. Gains** | gE ≈ 3 (2–4) on every excitatory edge inside the sub-network, including EPG/PEG→ER/ExR. gI ≈ 1.5 (1.5–2) on every inhibitory edge (ER, ExR4/5/6, Delta7) | Toy: gE 3/gI 1.5 held seeded bumps for 10 s at 6 of 8 positions; gE 4/gI 2 at 5 of 8. gI 1 runs hot or pins; gI ≥3 at gE 2 fades. Every working model sets per-class gains: EPG→PEN ≈16× PEN→EPG ([Pisokas code](https://github.com/johnpi/eLife_Pisokas_Heinze_Webb_2019/blob/dfb95dfeaad0da2df0f7f687846d4df44079a483/Exp_Recurrent_PB_EB/collect_stats_long_run.m#L394-L413)); a Delta7 synapse ≈6–7× an excitatory one after training ([Beiran, code sub-agent from Zenodo](https://zenodo.org/records/16618353)); Delta7→EPG ×15 with gE 2 ([flyverse [non-PR]](https://github.com/tel-0s/flyverse-core/blob/959f2e927b1c2806bc526fd5fc51cb3f5cc3e4b1/docs/audits/cx_wedge.md#L19-L27)) |
| **5. Drive** | Bias 0 on ring cells plus the usual background; no tonic cue | Toy: a bump nucleates from noise (4/4 runs of 10 s) and holds seeded positions. Every rate model has a uniform +1 drive ([Kim 2019 SI](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-019-1767-1/MediaObjects/41586_2019_1767_MOESM1_ESM.pdf); [Noorman 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/)). Kakaria and Pisokas use 5 Hz Poisson onto EPGs. [Lulzx/fly-brain [non-PR]](https://github.com/Lulzx/fly-brain/blob/08cf8666bd3cb405c803f95821ebe06d22b3e5ab/docs/textbook/07-heading-lab.md#L21-L23): no attractor without a 3–7 mV EPG bias |
| **6. Seed and score** | +10 mV bias on the EPGs of 3 adjacent EB wedges for 0.3 s, then ≥10 s free | Pass criteria: strength ≥0.3 and near 0.7; FWHM 80–120°; bump held ≥10 s; D ≲ 0.04 rad²/s; rates as in §0.3 |

**Shortfalls of this recipe in the toy**

- **Too narrow.** FWHM is 45° (2 of 16 wedges; strength ≈0.99) vs 80–120° measured.
  - Doubling EPG→PEN and PEN→EPG broadens it to 90–135° (strength 0.78–0.91 at gI 1.25–2), but rates climb to 200–300 Hz.
  - Delta7 ×2–3, EPG→EPG ×0.5 and ER→EPG ×0.5 do not broaden it.
- **PEN_a nearly silent** at 0.2–0.6 Hz, vs 3.9 ± 2.6 Hz measured. ER cells fire 1.7–2 Hz vs 4.5–5.2 Hz (ER1, ER3a).
- **Pinned to wedges.** The bump settles on wedges with more EPGs (MaleCNS wedges hold 2–4 each). 2/8 seeds were lost at gE 3/gI 1.5. Flies show no preferred positions ([Noorman 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/)).
- **Drift is wrong in both directions.** Held bumps drift 0.04–0.16°/s, far below flies (D ≈ 0.003–0.04 rad²/s, derived by the physiology sub-agent). Spontaneous bumps drift 6–7°/s.

**Next steps, ranked**
1. **Fit class gains on the sub-network with a gradient-free search** (CMA-ES; each 4-trial run of ~5 s took ~1–3 s on this Mac).
   - Search ~8–12 gains: EPG→EPG, EPG→PEN, PEN→EPG, EPG→PEG, PEG→PEN_b, EPG→Delta7, Delta7→{PEN_b, PEG, EPG}, Delta7→Delta7, EPG/PEG→ER/ExR, ER/ExR→ring, ER→ER.
   - Objective: strength 0.6–0.8, FWHM 80–120°, in-bump ≤ ~20 Hz, 10-s persistence, PEN_a 3–4 Hz, ER ~5 Hz.
   - This is [Duan 2025 [PP]](https://doi.org/10.1101/2025.05.26.655406)'s recipe (57 type-level parameters) done in spiking form.
2. **Test two Delta7 variants:**
   - Delta7→Delta7 ≈ 0. [Biswas 2024 [PP]](https://doi.org/10.1101/2024.11.01.621596) needed γ_II ∈ [−7.15×10⁻⁴, 0]; [Kutschireiter 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9992764/) omitted it.
   - Delta7→PEN_b excitatory, as [Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) hypothesise.
3. **Embed in the whole brain:**
   - Carry the ring settings over as type-specific parameters, then recalibrate biases with the bump present.
   - Watch ER→ER inhibition. ER4d gets 81% of its model input from other ER4d, and all-to-all ring-neuron inhibition is winner-take-all ([Pospisil 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446844/)), which could make EPG inhibition patchy.
   - Keep left and right PEN background balanced, since imbalance drives drift.
4. **Sign fixes to test:** GLNO as inhibitory (or keep it out at rest), and LPsP removed as dopaminergic.
5. **Do not add EPG gap junctions.** EPG innexin transcripts are ≈0 (shakB 0.3–5.4 vs ≈75 whole brain; [GSE155329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155329), derived), and EM cannot see gap junctions.

### 0.3 Resting targets (darkness, no locomotion)

| Quantity | Target | Source |
|---|---|---|
| EPG population mean | 0.5–2 Hz. Explant: ≈0.9 Hz rested, ≈2.0 Hz after 12 h sleep deprivation (fig.) | [Ho et al. 2022](https://doi.org/10.1016/j.cub.2022.09.048) |
| EPG in bump / out of bump | In vivo, non-walking example cell (fig.; spikes small, low confidence): ≈0 spikes/s most of the time, ≈1–3 spikes/s peaks at its preferred cue; 45–55 spikes/s after ExR2 dopamine activation. Vm ≈ −44 inside vs −54 mV outside the preferred heading (LJP-corrected). My suggested target: in-bump ≤ ~20 Hz, out-of-bump ≤1 Hz | [Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/); [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/) |
| Bump FWHM | EB: 90.9 ± 11.2° dark vs 82.3 ± 11.5° with a stripe. ≈100° in EB; ≈2 glomeruli in PB. PB ≈118° with no cue vs ≈98° with a bright cue (fig.) | [Seelig & Jayaraman 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/); [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/); [Basnak 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12321575/) |
| Persistence | ΔPVA 0.017 ± 0.76 rad across standing bouts of 6.7 ± 5.1 s (n = 499); sometimes >30 s. 5,278 bouts: drift "strongly peaked at zero", mostly within ±0.2 rad (fig.) | [SJ2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/); [Noorman 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/) |
| Diffusion | D ≈ 0.003–0.04 rad²/s (derived; no published D) | physiology sub-agent from the two sources above |
| PEN_a | 3.9 ± 2.6 Hz standing (loose patch). 2.7 ± 2.0 Hz across 12 cells at rest (derived). Peaks 31–80 Hz | [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PEN_b, PEG | No resting rates. PEN_b must be active: Kir2.1 in PEN_b "almost entirely abolished" the dark bump. PEG ≈35–40 Hz when depolarized (one cell, fig.) | [Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/); [Mussells Pires 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10881393/) |
| Delta7 | Tonic, broad cosine-like profile peaking 3.6 ± 0.25 glomeruli (≈180°) from EPG. No spike data | [Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| Ring neurons | ER1 4.5 ± 1.7 and ER3a 5.2 ± 2.7 spikes/s (dark). ER5 ≈1.3 Hz (morning), ≈3.7 Hz (early night), ≈7 Hz (sleep-deprived) (fig.). Visual ER2 ≈0 without a stimulus | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/); [Liu 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4892967/); [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/) |
| ExR | ExR1 bistable: <1 Hz DOWN, 16.9 ± 3.6 Hz UP. ExR2 ≈0–1 spikes/s at rest (fig.) | [Donlea 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5779612/); [Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/) |

---

## 1. MaleCNS ring wiring as the rung-1 model sees it (mine)

Source: `rest_calibration.network()`. This matrix has fast transmitters only (no monoaminergic or unknown-transmitter presynaptic cells) and no input onto sensory neurons. Scale = 1/size; w_syn = 1.5556 mV.

### 1.1 Cells and effective synapse weight

| Type | n | Transmitter | size | mV per synapse |
|---|---|---|---|---|
| EPG | 46 | ACh | 8.31 | 0.189 |
| EPGt | 4 | ACh | 1.71 | 0.920 |
| PEN_a | 20 | ACh | 5.06 | 0.320 |
| PEN_b | 22 | ACh | 4.31 | 0.373 |
| PEG | 18 | ACh | 2.59 | 0.606 |
| Delta7 | 42 | Glu | 4.18 | 0.376 |
| ER (282: ER1 28, ER2 41, ER3a 30, ER3d 54, ER3m 18, ER3p 18, ER3w 31, ER4d 26, ER4m 11, ER5 21, ER6 4) | 282 | GABA | 2.0–8.7 | 0.18 (ER4m) – 0.79 (ER1_c) |
| ExR1–8 | 26 | ExR1/7/8 ACh; ExR4/5/6 Glu; ExR2 DA; ExR3 5-HT | 3.5–24.6 | 0.063 (ExR1) – 0.44 (ExR8); ExR6 0.066 |

EPGs are large (size 8.3), so every synapse onto them is weak: 0.19 mV, against 0.61 mV onto PEG and 0.92 mV onto EPGt.

### 1.2 Input composition (% of input synapses; model matrix unless marked raw)

| Target (syn/cell) | Top inputs |
|---|---|
| **EPG** (4,222) | ER4m 10.9, ER2_c 7.5, PEN_a 7.4, ER4d 6.4, EPG 5.9, ER3w_b 5.4, PEN_b 5.0, ER3p_a 4.6, ER2_a 4.2, ExR1 3.2 (+), ExR6 3.2, ExR5 3.1, ER1_b 2.9, Delta7 2.2, ER1_a 2.2, LPsP 2.0. **ER total 63.8, ExR 11.4, excitatory 26.3, inhibitory 73.7** |
| **PEN_a** raw (2,116) | **GLNO 23.2 (dropped)**, EPG 14.4, PEN_a 12.9, ExR6 12.0, PEN_b 7.2, LPsP 6.1, ER1_b 5.1, ExR4 4.9, Delta7 2.8 |
| **PEN_b** raw (1,920) | **GLNO 15.5 (dropped)**, EPG 14.7, PEN_b 14.7, Delta7 14.3, ExR4 11.9, PEN_a 7.5, PEG 5.3, ER6 5.3 |
| **PEG** (1,107) | EPG 30.9, Delta7 19.7, ER6 18.1, LPsP 14.5, ExR4 3.5 |
| **Delta7** (1,184) | **Delta7 53.4**, EPG 40.0 |
| **EPGt** (711) | Delta7 37.5, P6-8P9 14.6, LPsP 12.0, EPG 7.1 |
| **ExR6** (9,730) | EPG 52.3, PEN_a 6.4, PEG 4.0 |
| **ER6** (2,989) | EPG 38.3, PEG 37.1, LAL206 16.5 |
| **ER4m / ER4d / ER2_c** | Own type 54.7 / 80.8 / 47.0; EPG 16.8 / 5.3 / 8.1; TuBu 5.7 / 2.7 / 3.8 |

### 1.3 Outputs and where the synapses sit

- **Outputs (% of output synapses):**
  - EPG → Delta7 17.3, EPG 10.0, ExR6 8.9, EL 8.0, PEN_b 5.4, PEG 5.4, PEN_a 5.3, ER6 4.0, ER4m 3.9.
  - PEN_a → EPG 34.9. PEN_b → EPG 26.7.
  - PEG → ExR4 34.9, ER6 24.2, PEN_b 12.2, EPG 5.4.
  - Delta7 → Delta7 28.0, PFNa 7.6, PEN_b 6.4, PFL3 5.9 … EPG 4.5, PEG 4.1.
- **Synapse sites per cell by ROI** (`roi_elements.feather`):
  - EPG: post EB 4,032 / PB 192 / gall 168; pre EB 295 / PB 223 / gall 105.
  - PEN_a: post EB 962 / NO 894 / PB 288. PEN_b: post EB 842 / NO 690 / PB 405.
  - Delta7: PB only (post 1,212, pre 580). PEG: post PB 599 / EB 351 / gall 172.
- **EPG→PEN is mostly in the EB.**
  - PEN_a has only 288 PB postsynaptic sites against 305 EPG→PEN_a synapses per cell.
  - By glomerulus, ≥84% of EPG→PEN_a synapses come from EPGs outside the PEN's own glomerulus.
  - This matches hemibrain EB:PB ≈ 3,844:1,281 for EPG→PEN_a and 3,645:1,512 for PEN_b (mechanisms sub-agent, derived), and [pwang724 [non-PR]](https://github.com/pwang724/fly-circuit-exploration/blob/80b94e6608cf927ca2c9f2bbce0577c5a998684c/docs/compass-recurrence.md): only 14–15% of EPG→PEN_a weight is same-glomerulus.

### 1.4 Angular structure (16 EB wedges; offset = post − pre)

| Pathway | Profile | Reading |
|---|---|---|
| EPG→EPG, synapses per pair | 0°: 32.8; ±22.5°: 22.4/21.6; ±45°: 3.1/3.0; beyond: <1 | Local excitation confined to ±22.5° |
| PEN_a→EPG | Peaks at ±45° and ±67.5° (34–36); ±22.5°: 21; 0°: 13 | Shifted output |
| PEN_b→EPG | Peaks at ±45/67.5° (26–31); 0°: 1.9 | Shifted output, tighter |
| EPG→PEN→EPG (two-step), per PB side | Peak at 0°. PEN_a L: 0.93 at +22.5° vs 0.86 at −22.5°; R mirror. PEN_b similar | Mostly local, slight skew |
| EPG→Delta7→X (X = EPG, PEN_a, PEN_b, PEG) | Normalized: 0.10 0.09 0.12 0.23 0.45 0.70 0.86 0.98 **1.00** 0.99 0.88 0.69 0.44 0.23 0.11 0.09; cosine R² 0.98 | Cosine anti-bump, max 180° away |
| ER→EPG, synapses per EPG by wedge | CV 0.12–0.22; first-harmonic tuning 0.03–0.09 (ER4m, ER2_c, ER4d, ER3w_b, ER3p_a, ER2_a, ER1_b, ExR6/5/1). Each neuron covers 16/16 wedges. Exception: ER5, coverage 0.51, tuning 0.20 | Flat, all-to-all |
| EPG→ER/ExR, by EPG wedge | Tuning ≤0.08 (ER4m, ER2_c, ER4d, ER6, ExR6, ExR4, ExR5, ER2_a, ER1_b) | Inhibitors read the total EPG activity |

### 1.5 Mean-field drive (mV per Hz of the whole presynaptic population, rung-1 weights, 5 ms)

| Onto | EPG | PEN_a | PEN_b | PEG | Delta7 | ER (all) | ExR4/5/6 | ExR1 | own type |
|---|---|---|---|---|---|---|---|---|---|
| EPG | +0.233 | +0.293 | +0.197 | +0.020 | −0.088 | **−2.517** | −0.284 | +0.127 | |
| PEN_a | +0.469 | +0.423 | +0.237 | +0.014 | −0.091 | −0.303 | −0.564 | 0 | |
| PEN_b | +0.508 | +0.264 | +0.515 | +0.184 | −0.498 | −0.289 | −0.435 | 0 | |
| PEG | +1.027 | +0.023 | +0.052 | +0.094 | −0.658 | −0.697 | −0.135 | +0.005 | |
| Delta7 | +0.885 | 0 | 0 | 0 | −1.183 | 0 | 0 | 0 | |
| ExR6 | +1.671 | +0.205 | +0.042 | +0.127 | | −0.059 | | | −0.010 |
| ER6 | +1.282 | +0.004 | +0.030 | +1.240 | | −0.042 | | | −0.039 |
| ExR4 | +0.653 | +0.120 | +0.086 | +1.201 | | −0.254 | | | −0.217 |
| ER4m | +0.365 | +0.057 | +0.155 | +0.006 | | −1.433 | | | −1.188 |

Reading the table (derived):
- Every ER cell at the measured ≈5 Hz would put −12.6 mV of DC inhibition on each EPG. That is ~2× the 7 mV threshold gap, so it must be cancelled by bias.
- Local excitation at gain 1 gives ~0.7 mV per Hz of partner activity.
- Noise-free LIF drive (7 mV gap, τm 20 ms, 2.2 ms refractory) for 10 / 30 / 50 Hz is 7.05 / 8.87 / 11.9 mV (derived).

---

## 2. Toy simulations (mine)

**Setup**
- Networks: the 152 ring cells, or ring + all ER + ExR (460 cells), cut from the rung-1 matrix with whole-brain `scale`. Everything is in HybridBrain, 0.1 ms steps, 4 trials.
- Inputs: Poisson 200 Hz × 1 mV (or 100 Hz × 0.5 mV), bias 0.
- Gains: gE on every excitatory edge, gI on every inhibitory edge.
- Seed: +10 mV on the EPGs of 3 adjacent EB wedges for 0.3 s. Then 4 s, or 10 s, free.
- Scores: EB PVL per 0.5 s, angular error from the seed, net drift, rates, and the aligned 16-wedge profile.
- Scripts were in the session scratchpad; the core is below.

```python
# ring + ER + ExR, slow ring excitation, STD on ring excitatory outputs (rung-1 weights); run from experiments/
import re, numpy as np
from scipy import sparse
import rest_calibration as attempt1
from brainfly.hybrid import HybridBrain
from shiu_rewiring import W_SYN                                        # 1.5556 mV
M, scale, labels, types, _ = attempt1.network()
RING = ["EPG", "EPGt", "PEN_a(PEN1)", "PEN_b(PEN2)", "PEG", "Delta7"]; EXC = RING[:5]
ER = sorted({t for t in types if re.match(r"^ER\d", t)}); EXR = sorted({t for t in types if t.startswith("ExR")})
sel = np.flatnonzero(np.isin(types, RING + ER + EXR))                  # 460 neurons
C = M.tocsr()[sel][:, sel].tocoo(); pre, post = types[sel][C.col], types[sel][C.row]
gE, gI, TAU = 3.0, 1.5, 0.1
w = np.where(C.data > 0, gE * C.data, gI * C.data)
slow = np.isin(pre, EXC) & np.isin(post, RING) & (w > 0)               # ring-internal excitation
S = sparse.csr_matrix((w[slow] * 0.005 / TAU, (C.row[slow], C.col[slow])), shape=(len(sel),) * 2)
F = sparse.csr_matrix((np.where(slow, 0.0, w), (C.row, C.col)), shape=(len(sel),) * 2)
brain = HybridBrain(trials=4, w_syn=W_SYN, matrix=F, slow=S, tau_slow=TAU, scale=scale[sel],
                    labels={k: v[sel] for k, v in labels.items()},
                    types={"all": {"noise_rate": 200.0, "noise_kick": 1.0}}
                          | {t: {"depression": 0.9, "recovery": 0.3} for t in EXC})
# seed: brain.set_bias(+10 mV on EPGs of 3 adjacent wedges) for 0.3 s, then set_bias(0) and run free
```

**Results**

| Condition | Outcome |
|---|---|
| Ring only, fast, gE 0.05–8 (ring_alone, for reference) | Runaway (170–320 Hz) or weak broad pattern (strength ≤0.29) |
| Ring only, slow + STD, gE 2–4, gI 1–4 | **Runaway at every setting**: EPG 170–270 Hz, strength ≈0.08 |
| Ring + ER + ExR, fast, gE 1.5–4, gI 0.5–3 | **No persistent bump.** gI 0.5–1 with gE ≥2.5: runaway (180–250 Hz). gE 2/gI 1: a bump pinned 120° from the seed at 130 Hz. gI ≥1.5: low-rate activity (0.1–7 Hz) whose position wanders (error ~90° = chance) |
| + STD 0.9/0.3, fast only, gE 2–6, gI 1.5–3 | No bump (EB PVL 0.25–0.57, random positions) |
| + slow (τ 0.1 s), no STD | Seeded bumps hold (e.g. gE 1.5/gI 2, 3 mV bias, low noise: error 12–15° over 4 s) but top wedge 90–350 Hz; or everything goes silent |
| **+ slow + STD 0.9/0.3, gE 3, gI 1.5** | **Strength 0.99–1.0; EB PVL 0.98.** 6/8 seed positions held within 6–17° for 10 s (drift 0.04–0.16°/s); 2/8 lost. EPG mean 2.4–5.1 Hz, top wedge 21–42 Hz, max cell 36–66 Hz; FWHM 45°. PEN_a 0.3–0.6, PEN_b 6–16, Delta7 4–7, PEG 4–10, ER 1.7–2.0, ExR 5–8 Hz |
| Same, gE 4, gI 2 | 5/8 held within ≤18°; 2/8 settled on a neighbouring wedge (20–46°); 1/8 lost. Similar rates |
| Same, no seed (10 s) | Bump forms from noise in 4/4 runs (strength 0.96–1.0); drift 6–7°/s at gE 3/gI 1.5 |
| STD variants at gE 3/gI 1.5 | 0.95/0.3 s: held (settled ~30° from the seed), top 85 Hz, max 200 Hz. 0.9/0.1 s: held (~45° from the seed), top 95 Hz, max 309 Hz. 0.8/0.3, 0.7/0.5 or 0.9/1.0 s: no persistence |
| Half the charge slow | Partial persistence (error 36–90°) |
| Width: EPG→PEN ×2 and PEN→EPG ×2 | At gI 1.25–2: FWHM 90–135°, strength 0.78–0.91, but EPG mean 76–106 Hz, top wedge 203–271 Hz (at gI 1: FWHM 157–180°) |
| Width: Delta7 ×2–3, EPG→EPG ×0.5, ER→EPG ×0.5, PEN loop ×1.5–2 with gI 3–4 | Width stays 45°. Rates of 10–40 Hz are possible with gI 3–4 |

---

## 3. Models: per-model evidence

### 3a. Connectome-constrained models (hemibrain / FlyWire)

| Model | Neuron model, time constants | Cells | Weights from connectome | What had to be set or tuned | Drive, seed | Bump, persistence | Lesson |
|---|---|---|---|---|---|---|---|
| [Beiran & Litwin-Kumar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12648571/) ([code](https://github.com/emebeiran/connconstr/blob/f5f397b88f8dd5c2a5c13558ce6039194a284586/nn_fig5_drosophilaCx_teacher.py#L562-L565)) | Rate, softplus β 5, τ = 1 | 46 EPG, 4 EPGt, 20 PEN_a, 22 PEN_b, 18 PEG, 42 Delta7 (the same 152) | Raw hemibrain counts; Delta7 × −2; scaled so the leading eigenvalue is 0.8 (text) or 0.9 (code) = 0.0016 per synapse (derived) | Per-neuron gains and biases trained. Trained means (code sub-agent from [Zenodo](https://zenodo.org/records/16618353), derived): Delta7 output gain 0.82 → 3.64; EPGt 3.44, PEG 1.72, PEN_b 1.30, EPG 1.16, PEN_a 0.88. Biases: PEG +1.15, PEN_b +0.82, EPGt +1.44, EPG +0.12 | 0.3 τ cue pulse | Bump held 2.5 τ. Type-shuffled gains "did not behave as ring attractors" | Counts alone are not enough; per-type excitability and strong Delta7 are needed |
| [Duan, Dong & Fiete 2025 [PP]](https://doi.org/10.1101/2025.05.26.655406) | Rate, sigmoid; global τ, leak | 439: EPG, Delta7, PEG, PEN, GLNO, 29 ER/ExR subtypes | W = w0(1 + Z_AB)·sign·count; left/right-symmetrized hemibrain | 57 parameters: a gain per pre/post type pair plus a bias per type. Global tying, or E/I-only gains, fail | One EPG set to 1; velocity via GLNO | Width ≈π/2; near-zero drift at ≤1% noise. Delta7 ablation abolishes the bump; ring-neuron ablation adds drift; PEN_b matters more than PEN_a | Fit type-pair gains; keep ring neurons and Delta7 |
| [Biswas, Stanoev, Romani & Fitzgerald 2024 [PP]](https://doi.org/10.1101/2024.11.01.621596) | Threshold-linear, analytic | EPG + Delta7, 8 units | Symmetrized counts × 4 type-pair scales γ | γ_II ≈ 0 (range [−7.15×10⁻⁴, 0]); three realizations (8/6/4 Delta7 active). ~15% of random count matrices can be rescaled into attractors | Self-sustained profiles | Matched imaged EPG bumps in darkness (4 flies) | Per-pair scales; Delta7→Delta7 ≈ 0; ER6 is an alternative uniform inhibitor |
| [Chang, Huang & Lo 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353971/) | Conductance LIF, τm 15 ms; ACh 20 ms, GABA_A 5 ms, NMDA 100 ms | 3 identical cells per glomerular type; PEN_a only; EPG↔EPG instead of PEG loops | "failed if we simply set the synaptic weights proportional to these numbers" | Per-class base conductance, 176,400 sets per model: EPG↔PEN 5–25 nS, inhibitory 1–20 nS. Hybrid: EPG→R 7, EPG→Δ7 7, EPG→PEN 12.2, PEN→EPG 13.6 nS | Cue via PENs at 50 Hz | FWHM 0.73π (ring) vs 1.23π (Delta7) vs ≈0.5π in flies. 9-s dark SD 2.7–22.9°. 2% weight noise → success 0.34–0.37 (hybrid tolerates 4.25%) | Ring-neuron global inhibition narrows bumps; heterogeneity is fatal without extra stabilizers |
| [Stentiford et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11349202/) ([code](https://github.com/stenti/stentiford_cx_ra/blob/eff923fbf5e8b5ad4b89257310753496536fbc99/cx_ra_rn.py#L27-L42)) | Current LIF, τm 20 ms, threshold 25 mV above rest; **exc 100 ms, inh 50 ms** | 16 EPG, 16 PEN, 8 Delta7, 1 global R, visual ER2/ER4 | Hand-set, "supported by" hemibrain | nA: EPG→PEN 0.13, PEN→EPG 0.14, EPG→EPG 0.02, EPG→Δ7 0.05, Δ7→EPG −2.6, R→EPG −1.3, EPG→R 0.01 (critical; only 0.01–0.015 work). Derived peak PSPs: +8.7/+9.4 mV excitatory vs −141 mV from Delta7 | PEN drive 0.13 nA | Bump 4–5 of 16 cells (90–112.5°) | Slow synapses plus strong inhibition in a current-based LIF |
| [Kutschireiter et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9992764/) | Rate, network filter | Populations patterned on hemibrain EPG/Delta7/PEN1 | Counts as within-population patterns | Cross-population gains tuned analytically; nonlinear global inhibition added; Delta7→Delta7 omitted | Inhibitory observations | Matches a circular Kalman filter | Patterns usable; gains and nonlinearity added |
| [Basnak et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12321575/) | Rate, N = 32, τ 50 ms | EPG + ER | ER→EPG all-to-all (anatomy); plastic | α −8.93, D 5.19, β 0.11 | Visual via ER | Stronger cue → narrower bump (more ER inhibition) | Uniform ER activity acts as global inhibition |
| [Noorman et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/) ([code](https://github.com/HermundstadLab/DiscreteRingAttractor/blob/1d9e83af0d71e8ab828563b991655341eea68fc7/plotModelingFigs.m#L2902-L2934)) | Threshold-linear, τ 0.1 s | N = 4–20 abstract units | Not fitted to the connectome | Bump needs J_E > 2 and J_I negative enough. Optimal J_E* for N = 6: 12, 4, 2.4; tolerance ∝ J_E*·N | c_ff = 1 | Unstable / homogeneous / bump regimes; drift to N discrete positions off-optimum | ring_alone's two failures are the unstable and homogeneous regimes |
| [Vafidis et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9286743/) | Two-compartment rate; **τs 65 ms**; sigmoid, max 150 Hz | 60 HD + 60 HR | Learned (hemibrain only checks synapse segregation) | Constant inhibition −1 (HD) / −1.5 (HR); saturation essential | Visual disinhibition | Holds ≥3 min; D 24.5 deg²/s (82.3 ± 15.7 with weight noise); FWHM ~60° | Slow synapses and constant global inhibition |
| [Hulse et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/) | Analysis only | Hemibrain CX | Relative weight = synapses / target's input in ROI | — | — | Linear pass of a fictive bump through Delta7 gives a sinusoid shifted 180° | ER→EPG has no wedge modularity except ER4m (p = 0) and ER1_a (0.028) |
| [Lyu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC11104186/), [Lu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10759448/), [Mussells Pires 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10881393/) | Feedforward readouts | PFN/hΔB/PFL3 | Counts × one scale | — | Heading given as input | No bump generation. PFL3 PB input: Delta7 77%, EPG 14% | Counts suffice feedforward, not for the ring |
| [Pospisil 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446844/) | Linear eigencircuits | FlyWire | Signed counts, <5 synapses dropped | EB circuit scaled to max eigenvalue 1; τ set by hand to 0.5 ms | — | Eigenvector 45 = all-to-all R4d mutual inhibition (winner-take-all) | ER→ER inhibition makes ring-neuron activity competitive |
| [Shiu 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/) ([code](https://github.com/philshiu/Drosophila_brain_model/blob/91bdd1e7dcf193f3e7ca5a8933497fcef63b7960/model.py#L15-L41)) | Current LIF (Kakaria constants), 5 ms | Whole FlyWire | Counts × 0.275 mV | — | Silent baseline | No CX test. One synapse = 0.043 mV peak PSP, so 162 coincident synapses reach threshold (derived) | Built for feedforward propagation |

### 3b. Whole-brain and other connectome LIF attempts [non-PR]

| Project | Setting | Result |
|---|---|---|
| [flybench](https://raw.githubusercontent.com/brandoncho369/flybench/master/docs/FINDINGS.md) | Shiu-style LIF, task "epg_ring_attractor" | FlyWire: all wedges at 260–380 Hz via the EPG↔ExR6 loop (one ExR6 has a blank transmitter label, defaulting to excitatory). MaleCNS: "0.0 % active", silenced by glutamatergic ExR6 plus GABAergic ER4m. Adaptation of 2 mV/200 ms makes it worse |
| [flyverse-core](https://github.com/tel-0s/flyverse-core/blob/959f2e927b1c2806bc526fd5fc51cb3f5cc3e4b1/docs/audits/cx_wedge.md#L19-L29) | MaleCNS, Shiu LIF, fan-in normalization | No bump at unit gains. Flat ER/ExR two-step inhibition onto EPG is −2,760 to −3,210 per wedge, more than on-wedge PEN excitation (+2,465) and 7× the Delta7 peak (−433). Bump with gE 2 (EPG↔PEN/PEG) and Delta7→EPG ×15 (Delta7→PEN ×1): 201 Hz, vector strength 0.76. Or ER/ExR ×0.3 with gE 1 / gD 4–15. Confinement needs gD/gE² ≈ 9–28 for a 90° bump |
| [Lulzx/fly-brain](https://github.com/Lulzx/fly-brain/blob/08cf8666bd3cb405c803f95821ebe06d22b3e5ab/docs/textbook/07-heading-lab.md#L21-L23) | Whole-CNS LIF, 48-point grid | "None is classified as an attractor without tonic bias"; 12/48 attractors with a 3–7 mV EPG bias and EPG recurrence ×3–6 |
| [chorus](https://github.com/aaygan29/chorus/blob/bfaede205c6f50147deddc0463342d18294c2137/code/cx_real_dynamics.py#L29-L75) / [galvani](https://github.com/marvosyntactical/galvani/blob/811ec30f78ab1fae142c2a199b447ff67c910e7f/README.md#L84-L95) | FlyWire / hemibrain rate models | Need sqrt fan-in normalization with global gain 13 and per-type gains, or log1p + symmetrized weights with gain 0.012 |

### 3c. Pre-connectome models (light-microscopy wiring, hand-set class weights)

| Model | Neuron model | Cells | Class weights | Inhibition | Drive | Bump | Lesson |
|---|---|---|---|---|---|---|---|
| [Turner-Evans 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) ([code](https://github.com/hrouault/ang_veloc_integr/blob/d20978df4580dd215a7390957ccbcbd1ff5b6a60/veloc_integr.py#L141-L205)) | Rate [x]+; τ EPG 80, PEN 65–67 ms | 54 EPG, 2×9 PEN | EPG→PEN α/3 (α 10); PEN→EPG von Mises κ 12, shifted 35° plus half-weight unshifted | EPG→every PEN −β/N (β 25): summed inhibition 2.5× excitation, "a pre-requisite to obtain a stationary bump" | +1 bias on PENs | D = 1.82×10⁻³ rad²/s (≈6 deg²/s, derived) | Net-inhibitory feedforward plus tonic PEN bias |
| [Kakaria & de Bivort 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5306390/) | LIF, Shiu's constants (−52/−45 mV, 20 ms, 5 ms PSC) | 18 EPG, 16 PEN, 16 PEG, 10 Pintr | All +20 PSC; Pintr→PEN/PEG −15; Pintr→Pintr −20. One unit ≈1.16 mV in code, so +20 ≈ 23 mV (3.3× threshold) (derived) | Pintr onto PEN/PEG, not EPG | 5 Hz Poisson onto EPGs | 2–3 glomeruli; drift ~1 glomerulus/s; only ~1.5% of 24,000 random configurations work; ±50% on one class is usually fine | Suprathreshold relays |
| [Pisokas, Heinze & Webb 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7419142/) ([code](https://github.com/johnpi/eLife_Pisokas_Heinze_Webb_2019/blob/dfb95dfeaad0da2df0f7f687846d4df44079a483/Exp_Recurrent_PB_EB/collect_stats_long_run.m#L394-L413)) | Kakaria LIF | 18 EPG, 16 PEN, 18 PEG, 8 Delta7 | Optimized: EPG→PEN/PEG +99.97 (~115 mV), EPG→Δ7 +47.9, PEN/PEG→EPG +6.07 (~7.0 mV), Δ7→PEN/PEG −35.7, Δ7→Δ7 −19.3 | Delta7 near-uniform (≈275 imp/s, ~10% modulation) onto PEN/PEG | 5 Hz Poisson onto EPGs | EPG FWHM 88.3°; 161 imp/s per unit (40–90 per real cell) | Feedforward ≫ return; tonic Delta7. [other insect: locust] needs local Delta7 |
| [Su et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5529380/) | Conductance LIF, τm 15 ms; **NMDA 100 ms, saturating** | 18 EIP, 16 PEI, 16 PEN types × 10 cells; 3 ring types | EIP→PEI 5, EIP→PEN 6, PEI→EIP 4, PEN→EIP 6 | EPG-driven ring neurons: R→EIP 5, EIP→R 1, R→R 1.6 | Cue only | FWHM 58.4°; NMDA works 50–100 ms, fails at 10 ms; NMDA weight window 100–120% | Slow saturating excitation plus ring feedback inhibition |
| [Han et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8425968/) | Su model re-tuned | as Su | EIP→PEI/PEN 4; PEI→EIP 8; PEN→EIP 10 | Ring-EIP→EIP 3.0 | — | Suppressing ring inhibition widens the bump (1.86 → 2.04 rad) and adds drift; PEN disinhibition gives "unstable and widespread" activity | Inhibition works only inside a window |
| [Kim et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC8115876/) ([SI](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-019-1767-1/MediaObjects/41586_2019_1767_MOESM1_ESM.pdf)) | Rate, τ 50 ms | 32 EPG-like | α −7.76, D 5.19 | Uniform β 1.96 per unit (×32 ≈ 63 ≈ 6× local excitation, derived); plastic ER input w ≤ 0.33 | +1 to all | FWHM ≈67.5° (sub-agent simulation) | Strong uniform inhibition suppresses the uniform mode (eigenvalue −60) |
| [Kim et al. 2017](https://doi.org/10.1126/science.aal4835) | Rate (paywalled) | — | [Code](https://github.com/hrouault/RingAttractor/blob/2b7b3dc08e0ca191d05796424087497264ceec26/ring_attractor/src/para_sweep.cpp#L132-L142): α 3, β 20, D 0.1; cosine J0 −0.2, J1 0.15 | Global | +1 | "local excitation and global inhibition" | Fitted parameters not retrieved |
| [Cope et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5328262/) | Rate, τ 1 ms | 16 wedge units | Self 0.6, ±1 0.35, ±2 0.225 | −0.1 × all 16 (1.6 vs 1.75 excitation) | Landmarks | 82.7° | Excitation spans ±2 wedges |
| [Green 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC6320684/), [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/), [Givon 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5447672/), [Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) | No bump simulation | | | Green: "requires additional inhibitory circuitry"; TE2020 only compared the 2017 matrix with extrapolated FAFB counts | | | No gains to copy |
| [Stone 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC6196076/) [other insect: bee]; [Goulard 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8491911/) [other insect] | Rate | TB1 (Delta7-like) | Cosine inhibition (cos Δθ − 1)/2 | | Heading imposed | Not an attractor | Delta7 as a cosine shaper |

### 3d. Cross-model regularities

| Quantity | Working range | Sources |
|---|---|---|
| Summed uniform inhibition vs summed local excitation | 0.9× (Cope), 2.5× (TE2017), ≈6× (Kim 2019) | §3c |
| Per-spike inhibitory vs excitatory PSP | Pisokas Delta7 ≈6× the PEN→EPG PSP; Stentiford ≈15×; Beiran ≈6–7× per synapse; flyverse gD/gE² 9–28 [non-PR] | §3a–c |
| Feedforward vs return excitation | Pisokas EPG→PEN ≈16× PEN→EPG; Han PEN→EIP 10 vs EIP→PEN 4 (reverse) | §3c |
| Excitatory synaptic τ | 50–100 ms (Su, Chang, Stentiford), 65 ms (Vafidis), rate τ 50–80 ms | §3a, §3c |
| Tonic drive | Present in every working model: +1 (rate models), 5 Hz Poisson onto EPGs, 3–7 mV bias [non-PR] | §3a–c |
| Bump criteria used | FWHM ≈90°; half-width 3π/16–π/4 (Kim 2017 code); 2–8 of 16 cells (Stentiford); vector strength >0.4 and peak >50 Hz (flyverse) | §3a–c |

---

## 4. Mechanisms: what each element does

| Element | Evidence | Implication for the model |
|---|---|---|
| **Delta7** | Glutamatergic (VGlut, FISH); EPGs express GluClα (≈266 vs 200 whole brain, derived) ([Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/); [GSE155329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155329)). EPG→Delta7 input is "well fit by a cosine"; output goes to glomeruli ~180° away ([Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/)). Blocking Delta7 output (shi^ts): the bump is dimmer and erratic, with the same width and no second bump. "The Δ7 neurons cannot be the only source of inhibition" ([Turner-Evans 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). Delta7 activation inhibits EPGs, mildly activates PENs, and is picrotoxin-sensitive ([Franconville 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6150698/)). A cosine kernel has no second harmonic, so it favours a single bump (derived; [Pisokas 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7419142/); [Aceituno 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11139481/)) | Shapes PEN_b/PEG drive; weak onto EPG. Delta7→Delta7 (53% of Delta7 input) may need ≈0 (Biswas) |
| **Ring neurons (ER)** | GABAergic (Gad1; FlyWire GABA in 24/24 ER4d and 21/21 ER5). All-to-all onto EPGs: ER4d contacts 1,148 of 1,150 possible pairs (hemibrain, derived). Tonic in darkness (ER1 4.5, ER3a 5.2 Hz) ([Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/)). Functionally selective: "many potential connections from R neurons onto compass neurons are actually weak or silent"; R2/R4d activation hyperpolarizes EPGs by a median −13 mV ([Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/)). Silencing ER1 or the visual TuBu pathway leaves the dark bump ([Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/); [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). Within-type all-to-all inhibition; ER4m at the top of a suppression hierarchy ([Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/)) | Global inhibition that tethers the bump rather than generating it. Include with EPG feedback (ExR6, ER6, ER4m) |
| **ER→EPG plasticity** | Associative LTD/LTP over minutes; 5-min pairing remaps ([Kim 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC8115876/); [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/)). Dopamine (ExR2) effects last >10 min ([Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/)) | Not needed at rest; explains why counts carry no visual map |
| **EPG–EPG** | On the diagonal in the EB; hemibrain ≈167 synapses per EPG (≈5% of input); EPG output is necessary (shi^ts abolishes localization) ([TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/); mechanisms sub-agent, derived). MaleCNS: 250 per EPG, confined to ±22.5° (mine) | Too weak alone at count weights; part of local excitation |
| **PEN loops** | PEN_a→EPG is the largest excitatory input (hemibrain 293 synapses per EPG, 8.0%); PEN_b→EPG 183 (5.0%). PEN_a shi^ts: weaker, drifting bump ([TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/)). PEN_b Kir: dark bump "almost entirely abolished", restored by a stripe ([TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). PEN synapses are electrotonically closer to the EPG root than ring synapses ([Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/)) | Carry the dark bump. Point-neuron counts probably under-weight them relative to ER |
| **PEG loop** | EPG→PEG→PEN_b→EPG; PEG→EPG sparse ([Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/); [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). PEG excites a gall ring neuron that inhibits EPGs ([Franconville 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6150698/)); MaleCNS PEG→ExR4 34.9%, →ER6 24.2% (mine) | Both excitatory (via PEN_b) and inhibitory (via ER6/ExR4) routes |
| **Gap junctions** | EM cannot see them ([Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/)). EPG innexins ≈0; PEN2, Delta7, R4d and PEG express modest shakB ([GSE155329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155329), derived). ER5 synchrony is NMDA-dependent, not electrical ([Raccuglia 2019](https://doi.org/10.1016/j.cub.2019.08.070)) | Don't add; PEN2/ER coupling only as a sensitivity test |
| **Slow receptors** | EPG transcripts vs whole brain (derived): Nmdar2 ≈69 vs 48; mAChR-B (inhibitory) ≈85 vs 15; GABA-B R1–3 ≈18/14/23; Ca-α1T 107–237 vs 85; Ih 81–207 ([GSE155329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155329)). "Persistent activity ... could also be sustained by voltage-gated channels and prevented from running away by inhibitory autoreceptors" (hypothesis, [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). NMDA in R4m (LTM; [Wu 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC3055246/)). In an FB ring, slow excitation plus fast inhibition gives persistence ([Lanz 2025 [PP]](https://doi.org/10.1101/2025.10.07.681003)) | No test of any slow receptor in the bump. The slow current in §0.2 is a stand-in |
| **Short-term plasticity** | None measured at any CX synapse (mechanisms sub-agent). Chang 2023 suggests STP "may play a key role" against heterogeneity | Modelling assumption only |
| **Transmitter signs to check** | EL octopaminergic (FlyWire says GABA; MaleCNS drops it). ExR1 ACh; ExR5/ExR6 vGlut ([Wolff 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12005719/)). LPsP dopaminergic ([Eckstein 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11106717/)). GLNO: FlyWire GABA in 3/4 cells. Delta7→PEN_b possibly excitatory ([TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/)). R5 activation hyperpolarizes EPGs; ExR1 depolarizes them ([Raccuglia 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12527942/)) | MaleCNS consensus is right for EL, ExR1, ExR5 and ExR6; check LPsP (ACh in MaleCNS) and GLNO (dropped) |

---

## 5. Physiology: measurements

### 5a. EPG

| Quantity | Value | Preparation | Source |
|---|---|---|---|
| Spontaneous rate | ≈0.9 Hz rested (n = 5), ≈2.0 Hz after 12 h sleep deprivation (n = 4) (fig.); resting Vm and threshold unchanged | Explant, perforated patch | [Ho 2022](https://doi.org/10.1016/j.cub.2022.09.048) |
| Spontaneous EPSPs | ≈11.5 Hz at ≈1.75 mV (control) vs ≈20.5 Hz at ≈2.1 mV (sleep-deprived) (fig.) | same | [Ho 2022](https://doi.org/10.1016/j.cub.2022.09.048) |
| In vivo rate, one cell | ≈0 most of the time; ≈1–3 spikes/s peaks at its preferred cue; 45–55 spikes/s after ExR2 activation (fig.). "spikes are unambiguously identifiable [here], but that was not true in all recordings" | Whole-cell, not walking | [Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/) |
| Vm tuning | ≈−54 mV outside vs ≈−44 mV inside the preferred heading; spike-removed tuning spans 4–8 mV | Walking VR, LJP-corrected | [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/) |
| Visual inhibition | Flash hyperpolarization peak ≈−7.7 mV; R2/R4d activation median −13 mV (−3 to −28), decaying over 2–3 s | same | [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/) |
| EPGt | No physiology; far fewer EB inputs and sparse ring-neuron input | Connectome | [Hulse 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/) |

### 5b. Bump shape

| Quantity | Value | Source |
|---|---|---|
| FWHM, EB | 82.3 ± 11.5° (single stripe), 78.7 ± 15.6° (two stripes), 90.9 ± 11.2° (darkness; GCaMP6f, walking) | [SJ2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/) |
| FWHM, EB and PB | "both bumps were ~100° wide"; EPG ≈97–112° across turning speeds (fig.); PB ≈2 glomeruli ("90 degrees") | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| FWHM vs cue | ≈118° no cue, ≈113° dim, ≈98° bright (fig.) | [Basnak 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12321575/) |
| Amplitude | ×1.48 from 0–30 to 150–180°/s turning (EPG), ×2.1 (PEN_a) (fig.). No effect of forward speed in Lu 2022 (conflicts with TE2017) | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/); [Lu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10759448/) |
| PVA strength | ≈0.12–0.45 per fly (fig.); lower after Delta7 block | [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| Number | One bump in every condition, including darkness and two-stripe scenes | [SJ2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/); [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| Spike vs calcium width | Single PEN spike tuning ≈60° vs ≈110° by imaging | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |

### 5c. Persistence and drift in darkness

| Quantity | Value | Source |
|---|---|---|
| Standing bouts | ΔPVA 0.017 ± 0.76 rad over 6.7 ± 5.1 s (n = 499 bouts, 11 flies); "sometimes persisted for more than 30 seconds" | [SJ2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/) |
| Drift distribution | 5,278 bouts: "strongly peaked at zero", mostly within ±0.2 rad (fig.); no preferred 8 or 16 positions | [Noorman 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11537979/) |
| Diffusion | D ≈ 0.043 rad²/s (upper bound) or 0.003–0.01 rad²/s (core) (derived) | physiology sub-agent |
| Legs suspended | "the E-PG bump was typically moving spontaneously" | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| Integration gain in darkness | 0.47 ± 1.2 (naive) vs 0.86 ± 0.64 with a stripe | [SJ2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/) |
| Model drift for comparison | D = 1.82×10⁻³ rad²/s (TE2017 rate model); 24.5 deg²/s ([Vafidis](https://pmc.ncbi.nlm.nih.gov/articles/PMC9286743/)); ~1 glomerulus/s ([Kakaria](https://pmc.ncbi.nlm.nih.gov/articles/PMC5306390/)) | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| Sleep / anaesthesia | Not imaged. The bump persists at night with more error | [Flores-Valle 2022](https://doi.org/10.1016/j.jneumeth.2021.109432) |

### 5d. PEN_a, PEN_b, PEG

| Quantity | Value | Source |
|---|---|---|
| PEN_a rate | 3.9 ± 2.6 Hz standing (loose patch); 0.2–7.5 Hz per cell, mean 2.7 ± 2.0 (derived); maxima 31–80 Hz | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PEN_a turning modulation | 5.6 ± 3.7 Hz between fast preferred and non-preferred turns (≈1.4 Hz per 100°/s mean, derived) | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PEN_a membrane | Rin 1.9 ± 0.8 GΩ; Vm ≈−46 mV and threshold ≈−34 mV (not LJP-corrected; derived) | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PEN_a tuning | 56 ± 20° (spikes) | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| PEN_b | No spike data; antiphase to EPG in the PB; trailing edge in the EB; needed for the dark bump | [Green 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC6320684/); [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| PEG | ≈35–40 spikes/s at ≈−45 to −49 mV (one cell, fig.); no heading tuning | [Mussells Pires 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10881393/) |

### 5e. Delta7

| Quantity | Value | Source |
|---|---|---|
| Offset from EPG | 3.6 ± 0.25 glomeruli (4 = 180°) | [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| Profile | Broad, ≈4 of 8 glomeruli per half; ΔF/F up to ≈1.25 (fig.) | [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| Downstream IPSPs | PFL2/3 IPSP rate changes ≈−1.7 / +2.2 Hz with heading; ≈80% of PFL heading input comes from Delta7 | [Westeinde 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10881397/) |
| Spike rate | Not measured | — |

### 5f. Ring and ExR neurons

| Type | Value | Source |
|---|---|---|
| ER1 | 4.5 ± 1.7 spikes/s (n = 9), darkness | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| ER3a | 5.2 ± 2.7 spikes/s (n = 12) | [Okubo 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7507644/) |
| ER2 (visual) | ≈0 without a stimulus; ≈7–8 spikes/s for a bar in its receptive field (one cell, fig.); receptive fields ≈30–60° | [Fisher 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7753972/); [SJ2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3830704/) |
| ER4d | More active in darkness than with a stripe (population; no rate) | [TE2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) |
| ER5 ("R2") | ≈1.3 Hz ZT0–2, ≈3.7 Hz ZT13–15, ≈7.0 Hz after sleep deprivation (fig.); 0.5–1.5 Hz slow waves with sleep need | [Liu 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4892967/); [Raccuglia 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12527942/) |
| ExR1 (helicon) | <1 Hz DOWN; 16.9 ± 3.6 Hz UP | [Donlea 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5779612/) |
| ExR2 (PPM3) | ≈0–1 spikes/s at rest; scales with rotational speed | [Fisher 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9729112/) |

### 5g. Timescales

| Quantity | Value | Source |
|---|---|---|
| Calcium lag | Phase delayed 300 ms (GCaMP6m) or 200 ms (GCaMP6f) relative to the ball | [Green 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC6320684/) |
| PEN_a spike lag after turns | ≈0.12 s (0.07–0.21); Vm 125 ± 21 ms | [TE2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| Bump relocation by PEN stimulation | Moves within <1 s; returns to tracking in a few seconds | [Green 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7688015/) |
| Optogenetic bump | An imposed bump "was then maintained by the circuit with naturalistic dynamics" (abstract only) | [Kim 2017](https://doi.org/10.1126/science.aal4835) |

---

## 6. Gaps and caveats

- **Toy vs whole brain.**
  - The recipe is from a 460-cell sub-network with no other inputs, no TuBu drive to ring neurons and no GLNO.
  - Its bump is too narrow (45°), PEN_a is silent, and it pins to wedges.
  - Whole-brain behaviour (tonic ER rates near 5 Hz, ER winner-take-all, left/right noise) is untested.
- **Missing numbers.**
  - Kim et al. 2017 *Science* fitted parameters are paywalled.
  - Duan 2025's fitted Z_AB and Biswas 2024's γ values are not in the retrieved texts.
  - Beiran's trained gains were extracted from Zenodo by a sub-agent, not by me.
- **Missing measurements.**
  - No population EPG spike rates in or out of the bump.
  - No spike rates for PEN_b or Delta7.
  - No passive properties for EPG or ring neurons.
  - No short-term plasticity at any CX synapse, and no slow-receptor test.
  - The bump has not been imaged in scored sleep or under anaesthesia.
- **Non-peer-reviewed sources.** The flybench, flyverse-core, Lulzx, chorus, galvani and pwang724 numbers are anecdotes. Their MaleCNS findings (ER/ExR swamping, EB EPG→PEN) agree with my own counts.
