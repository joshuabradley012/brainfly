# Rung 4: taste at rest. Why sugar no longer reaches MN9, and what makes proboscis extension work in a fly with ongoing activity

Compiled 27 Sep 2026 by a research agent. Four literature sub-agents covered resting activity and timing, restraint and disinhibition, hunger gating, and models. I re-found about 90 of the quoted sentences in the full texts myself (the ✓ marks). I also analysed the MaleCNS tables and the calibrated resting model, ran six short probes in that model, and built a one-neuron toy. *Drosophila melanogaster* only.

**Conventions**
- **✓** = I re-found the quoted sentence or value in the full text. Unmarked quotes were checked in full text by a sub-agent only.
- Labels:
  - **[PP]** = preprint. **[non-PR]** = GitHub project or blog, not peer reviewed (anecdote only).
  - **fig.** = read off a figure or computed from source data by a sub-agent (±10%).
  - **abs** = abstract only. **derived** = my arithmetic on published numbers.
  - **mine** = my analysis of the model or of the MaleCNS v1.0 tables in `~/fly-data`. **probe** = a short run of the resting model (§1.4).
- Abbreviations:
  - **2N** = second-order gustatory neuron; **3N** = third-order. **GRN** = gustatory receptor neuron.
  - **PER** = proboscis extension response. **FD** = food-deprived.
  - MaleCNS type names are in `code`.
- Model terms:
  - The **silent brain** is rung 1's: no background, no bias, no depression.
  - The **resting brain** is `escape_at_rest.py`'s model with its calibrated biases (`experiments/escape_at_rest/intact.npz`). It has background kicks (1 mV at 200 Hz), one bias per type, and depression (0.9 per spike, 0.5 s recovery) on central cholinergic neurons. Sensory, visual projection and descending neurons are undepressed.
- The existing taste notes are [short_term_plasticity.md](short_term_plasticity.md) §4 and [adaptation.md](adaptation.md). This file does not repeat them.

---

## 0. Recommendations

### 0.1 Diagnosis

1. **Sugar's signal survives the first synapse and dies at the next two** (mine, §1.1).
   - In the resting brain, the excitatory 2Ns Shiu et al. named rise as much as in the silent brain: G2N-1 (`GNG232`), Zorro (`GNG215`), Clavicle (`ANXXX462a`) and FMIn (`GNG197`) by 25–90 Hz, and Rattle (`GNG132`) by 41 Hz.
   - The next layers barely move:
     - the third-order Sternum (`GNG585`) and Bract (`DNge173/174`);
     - the premotor Roundup (`GNG108`), Roundtree (`GNG120`) and Rounddown (`DNge080`);
     - `DNge062`, MN9's largest input.

     These rise 0–4 Hz, against 11–45 Hz in the silent brain. MN9 rises 2 Hz, against 40.
   - The "3-fold loss per synapse" median in `taste_trace.json` hides this, because each layer also holds many weakly connected neurons.
2. **Short-term depression on the taste interneurons is the main cause** (probe).
   - Under 100 Hz sugar the cholinergic 2Ns fire at 25–90 Hz. At 0.9 per spike with 0.5 s recovery, that leaves 0.44–0.18 of their strength. No neuron can deliver more than 20 full-strength spikes/s (r½; short_term_plasticity.md §0.1).
   - Exempting the 326 neurons of the sugar route from depression raises MN9's rise from +2 to +15 Hz.
3. **The 0.1 Hz target for descending neurons is the second cause** (probe).
   - 42 of the route's neurons are descending neurons of 26 types, among them Rounddown, both Bract types and `DNge062`.
   - Held at 0.1 Hz, they sit 12–16 mV below threshold (biases −10 to −12 mV). In the silent brain every neuron sits 7 mV below.
   - Recalibrating those 26 types to 2 Hz takes MN9 from +15 to +27 Hz when the route is undepressed. With MN9 recalibrated as well, it is +25 Hz. With depression kept, the same change does nothing (+2 Hz).
4. **Both settings hit a recurrent excitatory premotor cluster** (mine, §1.3).
   - Roundup, `DNge059`, Rounddown, `GNG169` and Sternum are all cholinergic and excite each other with hundreds of synapses. Examples: Sternum→Roundup 835, Rounddown→`DNge059` 1,037, `GNG169`→Roundup 649, Roundup↔`DNge059` 343/333.
   - In Shiu's silent model, MN9 is a steep function of the sugar rate: ~0 Hz up to 30 Hz sugar, 19 Hz at 50 Hz, 66 Hz at 100 Hz (sub-agent, from Shiu 2024's supplementary tables).
   - Two cluster members (Rounddown, `DNge059`) are descending neurons held 14–15 mV below threshold. The other members are depressed. My inference is that the cluster can no longer ignite. One [non-PR] fork reached the same view: the loop "must ignite".
5. **MN9's own resting state halves its gain but does not block it** (probe, toy).
   - Driving Roundup, Roundtree and Rounddown directly at 20 or 50 Hz raises MN9 L by 17 or 39 Hz in the resting brain. In the silent brain the same drive gives 51 or 100 Hz.
   - The cause: ten SEZ premotor types each make 260–520 synapses onto MN9, and nine of them fire at the 2 Hz default (`DNge062` at 0.1 Hz). They give MN9 L input fluctuations with an SD of about 6 mV. To hold MN9 at 2 Hz, the calibration puts it 11 mV below threshold (bias −6.7 mV).
6. **Why the fixes already tried failed** (derived).
   - More sugar-GRN output also drives the inhibitory 2Ns harder. Phantom, Usnea, Billiards/Specter and Quasimodo are GABAergic, so they are undepressed, while the excitatory 2Ns' output is capped. More sugar therefore adds relatively more inhibition, consistent with MN9 falling to −2.6 Hz at 10×.
   - Hunger also changes GRN output mostly at middle concentrations, not at saturation. Starvation enhanced sugar-GRN calcium "at 100 mM sucrose, and a non-significant trend to enhancement at 400 mM" ✓ ([Inagaki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3295637/)). A 100 Hz drive is already the saturated end.
   - Stronger synapses everywhere are undone by recalibration, and are still capped by depression.
7. **The literature does not support the model's resting targets for this circuit.**
   - The 0.1 Hz rule for descending neurons rests on DNa02, DNg13, DNp07, DNp10 and the giant fiber (rung4_data.md §3). None of them is an SEZ premotor neuron.
   - The two SEZ descending populations with measured rates fire tonically:
     - DSOG1 (`DNg70` + `DNg98`) at "∼17Hz, with a standard deviation of 6Hz" ✓, the same in fed and deprived flies ✓ ([Pool 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4092013/));
     - the octopaminergic VUMd DNs at "4.12±3.12 Hz (n = 11)" ✓ ([Babski 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064449/)).
   - No resting spike rate, membrane potential or absolute calcium baseline has been published for any 2N, 3N, premotor taste neuron or MN9 (sub-agent search).
   - MN9 is active only when the rostrum moves: "a perfect correlation between rostrum movement and motor neuron activity" ✓ ([Gordon & Scott 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2650400/)). Spontaneous PER is rare in awake flies ✓. The proboscis extends rhythmically at rest only in deep sleep, in bursts at 0.34 Hz ✓ ([van Alphen 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7817094/)).
8. **Tonic inhibition sets a feeding threshold. Hunger raises excitatory gain instead of releasing it.**
   - Two identified inhibitory populations fire tonically and ignore hunger and taste: DSOG1 at ~17 Hz ✓ and PERin at ~14 Hz ✓ ([Mann 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750742/)). Silencing either makes flies extend to almost anything ✓.
   - Hunger acts upstream:
     - on sugar-GRN terminals, whose spiking does not change ✓;
     - on two 2Ns, G2N-1 and Clavicle ✓ ([Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/));
     - on Fdg, which answers sugar "only in starved flies" ✓ ([Flood 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3727048/));
     - through TH-VUM dopamine (1 → 25 Hz ✓) and ISNs (0.8 → 3.4 Hz, fig.).
   - Activating any node from the 3Ns to MN9 gives the same PER fed or starved ✓. The behavioural sucrose threshold falls 4.6-fold after 2 days without food ✓ ([Inagaki 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365050/)).
9. **The model cannot express most of hunger directly.**
   - TH-VUM, the OA-VUM and OA-VPM neurons, the serotonergic Sugar/Bitter SEL neurons, IPCs, Hugin-RG and the NPF neurons have no outputs in the fast-transmitter matrix.
   - Synapses onto GRN terminals are removed, so presynaptic GABA-B inhibition and dopamine or octopamine at GRNs cannot act.
   - A hunger state therefore has to be a parameter change on identified neurons.

### 0.2 Ranked model changes

Ranked by evidence, then by effect in the probes. Recalibrate after each change and re-check REST, ignition and looming.

| Rank | Change | Parameters | Evidence | Effect; what to check |
|---|---|---|---|---|
| 1 | **No fast depression on the SEZ taste route** | `depression` 1.0 for central cholinergic neurons on the route. Selectors, in order of preference:<ul><li>(a) the neurons that sugar, bitter, water and Ir94e each raise by more than 5 Hz in the silent brain (326 for sugar);</li><li>(b) a type rule: cholinergic `GNG*` and `PRW*` types (825 neurons, 305 types, about 1% of the depressed class), plus the gustatory ascending neurons (Clavicle `ANXXX462a`).</li></ul>Descending neurons are already exempt | <ul><li>No short-term plasticity has been measured at any taste synapse (short_term_plasticity.md §4.1).</li><li>G2N-1 answers repeated GRN activation almost undiminished (2nd/1st 0.99).</li><li>Rattle and Bract hold 80–86% of their peak through ~7 s of sucrose (sub-agent calculation, same notes).</li><li>Central depression was added to calm LH/SLP, AL and CX loops (short_term_plasticity.md §0.4), not SEZ ones.</li></ul> | Probe: MN9 +2 → +15 Hz. Check the Fano criterion and ignition after recalibration |
| 2 | **SEZ descending neurons off the blanket 0.1 Hz** | <ul><li>`DNg70`, `DNg98` (DSOG1): **17 Hz**.</li><li>The 26 descending types on the taste route: the 2 Hz default.</li><li>Then consider all gnathal descending types (`DNg*`, `DNge*`; 856 neurons, 294 types).</li><li>Keep 0.1 Hz for the measured walking, flight and escape DNs.</li></ul> | <ul><li>DSOG1 fires ~17 ± 6 Hz in every feeding state ✓.</li><li>VUMd DNs fire 4.1 ± 3.1 Hz ✓.</li><li>DNg13 is "typically very low" when not walking (rung4_data.md), so gnathal DNs differ.</li><li>Fewer DNs are active at rest than during walking: "the largest fraction of recorded DNs encode walking while fewer are active during head grooming and resting" ✓ ([Aymanns 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9605690/)).</li></ul> | Probe, with rank 1: +15 → +27 Hz; alone: nothing. DSOG1 at 17 Hz would put ~3 mV of tonic inhibition on `GNG117` (an excitatory MN9 input) and up to 30 mV on some VNC targets (mine). Watch those |
| 3 | **A hunger state as gain on identified nodes, not as released inhibition** | Fed vs starved differ at sugar-GRN output, Clavicle, G2N-1, Fdg (and SELK `DNg68`), ISN, and bitter-GRN output after 24 h. DSOG1, PERin and everything from the 3Ns to MN9 stay the same (§0.4) | See §0.4 and §3.3 | Test at realistic GRN rates, where hunger shifts sensitivity. Target: the sugar rate MN9 needs falls about 3–5× (24–48 h) |
| 4 | **A quiet proboscis motor module** (uncertain) | MN9 (and the proboscis protractor MNs) at 0.1–0.5 Hz, together with quieter MN9 inputs where their drive is sensory: `GNG015` and `GNG095` (fed by labellar mechanosensory `BM_Taste`). Never MN9 alone | <ul><li>For: MN9 activity tracks rostrum movement ✓; silencing MN9 leaves the resting posture unchanged ✓ ([McKellar 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7316511/)); few SEZ neurons show spontaneous calcium events ✓ ([Harris 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4474761/)).</li><li>Against quieting the inhibitors: Tastekin 2026 proposes feeding is tonically inhibited at several layers, released by disinhibition through Quasimodo (`GNG042`) onto `GNG015` (§3.2). No inhibitor's rate has been measured.</li></ul> | Toy: quieting MN9's SEZ inputs doubles its response; lowering MN9's target alone cuts it 3–7×. Test both hypotheses |
| 5 | **Realistic GRN drive and a fly-like sensitivity** | <ul><li>Drive: short bursts (100 ms, ~20–40 Hz per GRN) and an adapting drive, r(t) = r_ss + (r_pk − r_ss)·e^(−t/τ) with r_pk 60–90 Hz, τ 2–3 s, r_ss 6–10 Hz (short_term_plasticity.md §4.2).</li><li>Recalibrate `w_syn`, or better the route's gains, so that fed flies extend to strong drive and starved flies to 3–5× weaker drive.</li></ul> | <ul><li>A 100-ms light pulse (about 4 spikes per GRN) evokes a PER in fed flies, and PER tracks GRN firing (r = 0.96) ✓ ([Inagaki 2014 Nat Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4151318/)).</li><li>Fed flies extend to strong sugar-GRN activation 56% of the time (fig.).</li></ul> | Lower 2N rates also shrink depression's bite if rank 1 is only partial |
| — | **Not recommended** | Sugar-GRN output ×; global `w_syn` ×; "hunger" by silencing DSOG1 or PERin; removing inhibition wholesale | Tried (`taste_hunger.py`, `taste_wsyn.py`). DSOG1 and PERin are tonic in every state ✓. Silencing them gives indiscriminate feeding, including of bitter ✓ | — |

Spec sketch (later entries override earlier ones, as in `escape_at_rest.py`):
```
"cholinergic":                        {"depression": 0.9, "recovery": 0.5}
cholinergic GNG*/PRW* types, Clavicle: {"depression": 1.0}     # rank 1 (or the silent-brain taste routes)
descending_neuron:                     {"depression": 1.0}     # already
targets: DNg70, DNg98 -> 17 Hz; taste-route DN types (or DNg*/DNge*) -> 2 Hz   # rank 2
```

### 0.3 Resting targets for the PER circuit

| Neurons (MaleCNS type) | Current target | Recommended | Basis |
|---|---|---|---|
| DSOG1 (`DNg70`, `DNg98`) | 0.1 Hz | **17 Hz** | Cell-attached; fed, food-deprived and water-deprived alike ✓ ([Pool 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4092013/)). The mapping is likely, not proven (§2) |
| PERin (a T1 ascending pair; type not identified in MaleCNS) | 2 Hz, if typed | **14 Hz** once identified | Cell-attached; fed and 24 h deprived alike ✓ ([Mann 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750742/)) |
| OA-VUMd DNs (`DNge138`, `DNge149`, `DNge152`, `DNge150`, `DNg66`) | 0.1 Hz | **4 Hz** | Whole-cell ✓ ([Babski 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064449/)). No outputs in the fast-transmitter model, so this affects only the rate statistics |
| ISN (`ISN`) | 2 Hz | fed **0.8 Hz**, starved 3.4 Hz | Fig. 2E of [Jourjine 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983267/) (fig.) |
| TH-VUM (dopaminergic; no MaleCNS name found; no model output) | — | fed 1 Hz, 12 h ~10 Hz, 24 h 25 Hz | ✓ ([Marella 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310174/)) |
| IPC (`IPC`; no model output) | 2 Hz | fed 0–1.4 Hz, 24 h ~0 Hz | [Bisen 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11778929/) |
| MN9 | 2 Hz | 0.1–0.5 Hz, only with rank 4 | Gordon & Scott 2009 and McKellar 2020 (quotes in §3.1) |
| Descending neurons of the taste route: Rounddown `DNge080`, Bract `DNge173/174`, `DNge062`, `DNge059`, Fudog `DNg67`, `DNge051` and others | 0.1 Hz | 2 Hz default | No measurement; 0.1 Hz came from non-SEZ DNs |
| 2Ns: G2N-1, Zorro, Clavicle, FMIn, Phantom, Usnea | 2 Hz | keep | Unmeasured. Calcium data fit a low baseline, perhaps ≤2 Hz (sub-agent's reading). They transmit well at 2 Hz (§1.1) |
| 3Ns and premotor interneurons: Roundup, Roundtree, Sternum, Rattle, Fdg, `GNG117`, `GNG234`, `GNG169` | 2 Hz | keep, or lower with rank 4 | Unmeasured |
| MN9's GABAergic inputs: `GNG130`, `GNG095`, `GNG015`, `GNG180`, `GNG184`, `DNge051` | 2 Hz (`DNge051` 0.1) | unresolved (rank 4) | Unmeasured. `GNG015` and `GNG095` are mechanosensory-driven (mine) |
| Retractor MNs (MN1 and others) | 2 Hz | probably tonic | "silencing mn1 showed the opposite phenotype, impairing the retraction of the proboscis at rest" ✓ (McKellar 2020) |

### 0.4 A hunger state

Sources are in §3.3–3.4.

| Node (MaleCNS) | Fed | 24–48 h without food | Evidence | In the LIF |
|---|---|---|---|---|
| Sugar-GRN output (`LB3b`, `LB3c` and others) | ×1 | Terminal calcium at 100 mM rises from ~8% to ~30% ΔF/F (×3.5); at 400 mM, 34% → 50% (not significant). Spiking unchanged ✓ | [Inagaki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3295637/) (fig.). Kain 2015 saw no change in 2-week-old flies (conflict) | A gain that is larger for weak input (×1.5 near saturation, up to ×3 mid-range), or a leftward shift of the drive–output curve |
| TH-VUM dopamine; OA-VPM4 octopamine | 1 Hz; octopamine potentiates sugar GRNs only in fed flies ✓ | 25 Hz ✓ | Marella 2012; [Youn 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6021039/) | Folded into the GRN gain; neither neuron has model outputs |
| Clavicle (`ANXXX462a`) | PER to its activation 0/6/13/22% | 9/35/53/66% (48 h) | Shiu 2022 source data (fig.) | Output gain or bias. Its threshold shifts >8×, the largest central effect |
| G2N-1 (`GNG232`) | 0/30/73/98% | 0/56/86/97% | same | Small gain (~×1.5) |
| Fdg (`GNG588`); SELK (`DNg68`) | No sugar response ✓; no sweet response | Responds ✓; responds | Flood 2013; [Savaş 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13096221/). Shiu 2022 saw no taste response in Fdg (conflict) | Fed: lower bias so that sugar does not recruit them; starved: calibrated |
| ISN (`ISN`) | 0.8 Hz | 3.4 Hz (fig.) | Jourjine 2016 ✓ (direction) | Set the target per state. Its effect goes through dILP3 (peptide), so the fast model can't carry it |
| Bitter-GRN output | ×1 | Response to weak bitter halves (0.6 → 0.3 ΔF/F, 2 days) | [Inagaki 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365050/) (fig.); LeDue 2016 (OA-VL firing −50%) | Bitter output ×0.5 at 48 h |
| DSOG1, PERin | 17, 14 Hz | same ✓ | Pool 2014; Mann 2013 | Unchanged |
| 3Ns, premotor neurons, MN9 | — | unchanged ✓ | Shiu 2022 | Unchanged |

Behavioural targets for the hunger state:
- The labellar S50 falls from ~700 mM fed to 270 (6 h), 200 (24 h) and 150 mM (48 h); "sugar sensitivity alone changes 4.6 fold" ✓ (Inagaki 2014).
- Optogenetic sugar-GRN drive gives PER in 1/13/16/56% of fed flies and 30/64/69/96% of 48-h-starved flies across the same four light levels (fig.).

### 0.5 A test to pre-register next

1. **Model.** Ranks 1 and 2, full recalibration (fresh starts, as in `rest_calibration2.py`).
2. **Tests.**
   - `taste_at_rest.py`'s tests: SUGAR, RESPONSE, BITTER, IR94E, STABLE, NULL.
   - `escape_at_rest.py`'s REST and ESCAPE.
   - Direct activation of Roundup/Roundtree/Rounddown and of MN9 must still drive MN9 (fed flies extend ~96% to MN9 activation).
3. **Second step.** Add the §0.4 hunger state. The sugar rate that gives half of MN9's maximal rise should fall 3–5× from "fed" to "starved", with bitter still vetoing in both.
4. **Report, don't gate.** Rank 4's two variants (quiet vs tonic MN9 inhibitors) as a sensitivity analysis.

---

## 1. What breaks in the model (mine)

Rises are for the 17 left sugar GRNs (`LB3b`, `LB3c`) driven at 100 Hz for 1 s, against the 0.5 s before, 8 flies, as in `taste_trace.py`. Scripts ran from the session scratchpad; nothing in the repository changed.

### 1.1 Where the signal dies

| Stage | Neuron (MaleCNS type) | Transmitter, superclass | Silent brain rise, L / R (Hz) | Resting brain rise, L / R (Hz) |
|---|---|---|---|---|
| 2N | G2N-1 (`GNG232`) | ACh | 23.8 / 0.1 | 39.1 / 1.2 |
| 2N | Zorro (`GNG215`) | ACh | 74.5 / 0 | 76.6 / 4.5 |
| 2N | Clavicle (`ANXXX462a`) | ACh, ascending | 96.9 / 0 | 90.1 / −1.5 |
| 2N | FMIn (`GNG197`) | ACh | 21.5 / 0 | 24.6 / −0.4 |
| 2N | Phantom (`GNG229`) | GABA | 104 / 36.6 | 87.8 / 40.2 |
| 2N | Usnea (`GNG175`) | GABA | 95.9 / 40.4 | 80.0 / 39.8 |
| 2N | Billiards/Specter (`GNG038`) | GABA | 101 / 100 | 86.9 / 84.0 |
| 2N | Quasimodo (`GNG042`) | GABA | 81.8 / 46.0 | 63.2 / 30.0 |
| 2N–3N | Rattle (`GNG132`) | ACh | 42.6 / 0 | 40.8 / −0.9 |
| 3N | Fudog (`DNg67`) | ACh, DN | 36.9 / 29.2 | 33.1 / 27.5 |
| 3N | Sternum (`GNG585`) | ACh | 30.6 / 0 | 4.4 / −0.9 |
| 3N | Fdg (`GNG588`) | ACh | 12.1 / 0 | 4.0 / 0.6 |
| 3N | Bract 1 / 2 (`DNge174` / `DNge173`) | ACh, DN | 11.2 / 0 (each) | 0.1 / 0 |
| Premotor | Roundup (`GNG108`) | ACh | 45.2 / 24.9 | 3.6 / 1.5 |
| Premotor | Roundtree (`GNG120`) | ACh | 24.1 / 23.4 | 1.6 / 1.6 |
| Premotor | Rounddown (`DNge080`) | ACh, DN | 23.0 / 35.6 | −0.2 / 0.1 |
| Premotor (unnamed) | `DNge062` | ACh, DN | 20.4 / 16.9 | −0.2 / −0.2 |
| Premotor, inhibitory | `GNG130` | GABA | 23.8 / 13.4 | 3.0 / 1.2 |
| Premotor, inhibitory | `GNG095`, `GNG015` | GABA | 0 / 0 | −2.0 to −3.5 |
| Motor | MN9 | ACh, motor | 39.8 / 41.0 | 1.9 / −0.2 |

Names come from the MaleCNS `synonyms` column. Shiu et al. class Roundup, Roundtree and Rounddown as premotor: "Roundtree and Rounddown were named because they, like Roundup (named in Sterne et al., 2021), are premotor neurons" ✓. They class Bract as third-order ✓ ([Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/)).

### 1.2 How far each stage sits from threshold at rest

The mean membrane potential combines the calibrated bias, the background (4 mV mean, SD 1.4 mV), and each neuron's partners firing at their targets (independent Poisson, depression at the resting rate). The shot-noise SD is computed from the same terms (derived). In the silent brain every neuron sits 7 mV below threshold with no noise.

| Stage | Examples | Bias (mV) | Below threshold (mV) | Input SD (mV) |
|---|---|---|---|---|
| Excitatory 2Ns | G2N-1, Zorro, Clavicle, FMIn | −1.6 to +0.5 | 4.8–6.0 | 2.5–3.1 |
| Cholinergic premotor interneurons | Roundup, Roundtree, Fdg | −4.6 to −7.7 | 8.0–9.6 | 3.0–4.7 |
| Descending neurons feeding MN9 (target 0.1 Hz) | Rounddown, Bract, `DNge062` | −10.1 to −12.3 | 12.4–16.1 | 2.2–3.7 |
| All 42 DNs on the sugar route (26 types) | | median −11.3 | median 14.7 | median 2.8 |
| The other 284 neurons on the route | | median −4.1 | median 7.4 | median 3.4 |
| MN9 L / R | | −6.7 | 11.2 / 10.8 | 6.0 / 3.7 |

### 1.3 MN9's inputs and the premotor cluster

**MN9's inputs**
- MN9 L has 5,877 fast-transmitter input synapses in the model; MN9 R only 523, which looks like incomplete reconstruction. The size scaling makes their weights similar.
- MN9 L's largest inputs (synapses, % of input):
  - excitatory: `DNge062` 520 (8.8%), Roundtree 418 (7.1%), `GNG117` 401 (6.8%), Roundup 355 (6.0%), `GNG234` 334 (5.7%), Rounddown 197;
  - inhibitory: `GNG015` 443 (7.5%), `GNG095` 377 (6.4%), `GNG130` 373 (6.3%), `GNG180` 276, `GNG184` 261, `DNge051` 212.
- Roundup, Roundtree and Rounddown supply 16.5% of MN9 L's input, close to the "approximately 13%" Shiu et al. found in FAFB ✓. Bract makes no synapses onto MN9.
- **At rest, 98% of MN9 L's input variance (34 of 34.3 mV²) comes from 157 SEZ interneurons at the 2 Hz default**, mostly nine of the ten types above (all but `DNge062`). One spike of `GNG130`, `GNG095` or Roundtree moves MN9 L by about 11 mV (0.157 × weight; short_term_plasticity.md §0.1).
- **MN9's two strongest steady inhibitors are driven by labellar mechanosensory neurons.** `GNG015` gets 1,376 synapses from `BM_Taste`, its largest input; `GNG095` gets 215. `BM_Taste` is sensory, so it is silent at rest in the model. These inhibitors fire at 2 Hz only because the calibration puts them there.
- **Pool et al.'s DSOG1 (`DNg70`, `DNg98`) make no synapses onto MN9 or its GABAergic inputs.** `DNg98` sends 546 synapses to `GNG117`, an excitatory MN9 input; `DNg70` sends 276 to Scapula (`GNG087`) and 52 to Fdg. Most of their output is in the VNC.

**The recurrent premotor cluster.** Signed synapse counts, both sides pooled; rows are presynaptic.

| From \ to | Roundup | `DNge059` | Rounddown | `GNG169` | Sternum | Roundtree | `DNge062` |
|---|---|---|---|---|---|---|---|
| Roundup `GNG108` | 35 | 343 | 13 | 242 | 50 | 264 | 48 |
| `DNge059` (DN) | 333 | 9 | 47 | 4 | 2 | 1 | 117 |
| Rounddown `DNge080` (DN) | 11 | 1,037 | 128 | 8 | 0 | 15 | 200 |
| `GNG169` | 649 | 518 | 243 | 0 | 2 | 53 | 79 |
| Sternum `GNG585` | 835 | 9 | 7 | 2 | 13 | 350 | 0 |
| Roundtree `GNG120` | 16 | 71 | 231 | 7 | 1 | 19 | 8 |

All members are cholinergic. The DN members sit 14–15 mV below threshold at rest (biases −10.6 and −10.9 mV); the others are depressed.

**Hunger-related neurons in the matrix**
- `ISN` (4 cells, cholinergic) has 10,055 output synapses, none onto MN9's premotor pool.
- `AstA1` (GABA) has 44,425 outputs, none onto the pool.
- These have no outputs in the fast-transmitter model: TH-VUM, `OA-VUMa*`, `OA-VPM4`, the Sugar/Bitter SEL neurons (`GNG540`, `GNG550`, `GNG056`, `DNg28`), `IPC`, `Hugin-RG`, `DH44`, `NPFL1-I` and `DNp29` (NPF).

### 1.4 Probes

Two seeds × 8 trials (16 flies) per row, in the resting model with its calibrated biases except where stated. Left sugar at 100 Hz for 1 s, unless stated. These are exploratory, not pre-registered: there was no full recalibration, and no check of bitter, REST or looming.

| Condition | Roundup L / R | Rounddown L / R | `DNge062` L / R | Bract 2 L | MN9 L / R |
|---|---|---|---|---|---|
| Resting brain (`taste_trace.py`, 8 flies) | 3.6 / 1.5 | −0.2 / 0.1 | −0.2 / −0.2 | 0.1 | 1.9 / −0.2 |
| The 70 first-order neurons undepressed | 26.1 / 10.2 | 0.8 / 5.9 | 1.1 / 0.0 | 3.7 | 1.4 / 2.6 |
| All 326 route neurons undepressed | 32.4 / 18.8 | 5.0 / 10.4 | 5.5 / 1.1 | 1.0 | **15.6 / 14.6** |
| The route's 26 DN types recalibrated to 2 Hz (6 rounds), depression kept | 4.9 / 1.4 | 0.9 / 2.4 | 3.1 / 0.2 | 2.4 | 1.8 / 2.7 |
| Both | 38.9 / 23.1 | 19.9 / 26.2 | 21.4 / 12.8 | 11.3 | **26.9 / 27.4** |
| Both, with MN9 also recalibrated to 2 Hz (8 rounds) | 39.6 / 23.2 | 19.9 / 27.1 | 21.2 / 13.4 | 10.4 | **25.4 / 24.2** |
| Silent brain (rung 1) | 45.2 / 24.9 | 23.0 / 35.6 | 20.4 / 16.9 | 11.2 | 39.8 / 41.0 |
| **Direct drive** of Roundup, Roundtree and Rounddown (both sides) at 20 / 50 Hz, resting brain | — | — | — | — | 17.2 / 7.2 at 20 Hz; 39.3 / 23.5 at 50 Hz |
| Same, silent brain | — | — | — | — | 51.2 / 29.8 at 20 Hz; 100 / 68.1 at 50 Hz |

- The route is the 326 neurons that sugar raises by more than 5 Hz in the silent brain, reached by excitatory steps from the sugar GRNs: 70 at one step, 160 at two, 79 at three and 17 at four.
- In the "both" condition:
  - the DN types' biases rose from a median −11.3 to −5.5 mV;
  - MN9 L's resting rate rose to 6.5 Hz (4.5 Hz after its own recalibration);
  - the brain's mean rate stayed at 1.0 Hz.
- 45% of the sugar GRNs' direct drive goes to GABAergic or glutamatergic first-order neurons (derived from the weights).

### 1.5 One-neuron toy: MN9 with its real inputs

MN9 L is modelled as one LIF neuron (τm 20 ms, τs 5 ms, threshold 7 mV, reset −5 mV, refractory 2.2 ms). Its 252 model inputs are independent Poisson trains, plus the background. The bias is found by bisection for MN9's resting rate. "Resting-brain rises" and "silent-brain rises" add the measured rises of MN9's 15 largest inputs (§1.1) to their resting rates.

| MN9 resting rate | Partners' resting rates | Bias (mV) | MN9 with resting-brain rises (Hz) | MN9 with silent-brain rises (Hz) |
|---|---|---|---|---|
| 2 Hz | Model targets (SEZ 2 Hz, DNs 0.1 Hz) | −7.9 | 4.7 | 16.4 |
| 2 Hz | SEZ interneurons at 0.2 Hz | −1.7 | 9.6 | 27.8 |
| 2 Hz | All silent (background only) | −0.7 | 10.9 | 31.3 |
| 0.2 Hz | Model targets | −16.2 | 0.7 | 8.1 |
| 0.2 Hz | SEZ interneurons at 0.2 Hz | −9.4 | 2.0 | 15.9 |
| 0.2 Hz | All silent | −3.0 | 7.3 | 26.9 |

Two readings:
- MN9's own resting input halves its response to a given premotor signal.
- Lowering MN9's target without quieting its inputs makes things worse, because the calibration must then push MN9 further below threshold.

---

## 2. MaleCNS names for published taste and feeding neurons (mine)

From the MaleCNS `synonyms` and `flywireType` columns, with the resting model's settings.

| Published name | MaleCNS type (FlyWire) | Role | Transmitter (MaleCNS) | Model target / bias |
|---|---|---|---|---|
| G2N-1 | `GNG232` (CB0616) | 2N, sugar | ACh | 2 Hz / 0.2 mV |
| Zorro | `GNG215` (CB0192) | 2N, sugar | ACh | 2 / 0.5 |
| Clavicle | `ANXXX462a` (AN_GNG_30) | 2N, sugar; ascending | ACh | 2 / 0.2 |
| FMIn | `GNG197` (CB0366) | 2N, sugar | ACh | 2 / −1.6 |
| Phantom | `GNG229` (CB0062) | 2N, sugar and water | GABA | 2 / −0.8 |
| Usnea | `GNG175` (CB0008) | 2N, water in Shiu 2022's imaging; likely peptidergic (Shiu 2024) | GABA | 2 / −0.9 |
| Billiards / Specter | `GNG038` (CB0248) | 2N (Shiu 2024) | GABA | 2 / −0.9 |
| Quasimodo | `GNG042` (CB0118) | 2N; disinhibits MN9 via `GNG015` (Tastekin 2026) | GABA | 2 / −3.6 |
| Rattle | `GNG132` (CB0499) | 2N/3N, sugar | ACh | 2 / −2.3 |
| Sternum | `GNG585` (CB0051) | 3N | ACh | 2 / −2.8 |
| Fdg | `GNG588` (CB0038) | 3N; putative command neuron | ACh | 2 / −7.7 |
| Bract 1 / 2 | `DNge174` / `DNge173` | 3N, descending | ACh | 0.1 / −11.4, −12.3 |
| Fudog | `DNg67` | sugar and water (Shiu 2024) | ACh | 0.1 / −2.9 |
| Roundup | `GNG108` (CB0553) | premotor | ACh | 2 / −5.0 |
| Roundtree | `GNG120` (CB0493) | premotor | ACh | 2 / −4.6 |
| Rounddown | `DNge080` | premotor, descending | ACh | 0.1 / −10.9 |
| Scapula | `GNG087` (CB0219) | bitter 2N onto Roundup and Rounddown | Glu | 2 / −6.1 |
| MN9, rostrum protractor | `MN9` (CB0701) | motor | ACh | 2 / −6.7 |
| — | `DNge062`, `GNG117` (CB0216), `GNG234` (CB0893) | unnamed excitatory MN9 inputs | ACh | 0.1 / −10.1; 2 / −3.8; 2 / −2.9 |
| "buddy" (Sterne 2021, via Shiu's split lines) | `GNG180`, `GNG184` (CB0806) | MN9 inhibitors | GABA | 2 / −1.7, −1.8 |
| — | `GNG130` (CB0465, fru), `GNG095` (CB0903), `GNG015` (CB0862, fru), `DNge051` | MN9 inhibitors | GABA | 2 / −5.3, −8.1, −3.8; 0.1 / −11.2 |
| DSOG1 (Pool 2014) | `DNg70`, `DNg98` | tonic restraint | GABA (FlyWire lists leucokinin for `DNg70`; §3.2) | 0.1 / −5.6, −4.9 |
| ISN (Jourjine 2016) | `ISN` | AKH-sensing | ACh (acts through dILP3) | 2 / −0.6 |
| SELK | `DNg68` | 2N with sweet and bitter input; sweet responses only when starved | leucokinin + ACh | — |
| Sugar SEL PN / LN; Bitter-SEL (Yao & Scott 2022) | `GNG540`, `GNG550` / `GNG056`; `DNg28` | serotonergic | 5-HT (no model output) | 2 |
| OA-VUMa1–8; OA-VUMd1–4 (Babski 2024) | `OA-VUMa*`; `DNge138`, `DNge149`/`152`, `DNge150`, `DNg66` | octopaminergic | OA / unclear (no model output) | 2; 0.1 |
| OA-VPM4 (Youn 2018) | `OA-VPM4` | potentiates sugar GRNs | OA (no model output) | 2 |
| TPN3 (Kim 2017) | `ANXXX470` | taste projection neuron | ACh | 2 / −1.8 |
| mute (Sterne 2021) | `DNge172` | SEZ DN onto abdominal MNs | ACh | 0.1 / −3.8 |
| Not found in MaleCNS | TH-VUM, PERin, IN1, sGPNs (Kain & Dahanukar 2015), OA-VL1/2, SIFamide neurons | | | |

---

## 3. Evidence

### 3.1 Resting activity near the PER circuit

| Neuron (MaleCNS) | Quantity | Value | Preparation | Quote | Source |
|---|---|---|---|---|---|
| DSOG1 (`DNg70` + `DNg98`) | Spontaneous rate | ~17 Hz (SD 6) | Cell-attached, in vivo | "DSOG1 neurons showed an average baseline firing rate of ∼17Hz, with a standard deviation of 6Hz" ✓ | [Pool 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4092013/) |
| same | vs state and taste | No change with water or food deprivation; no response to 1 M sucrose, 1 mM denatonium or water, fed or deprived | same | "The baseline activity of DSOG1 neurons was not significantly different in flies that were water-deprived, food-deprived or non-deprived" ✓ | same |
| PERin (E564; one pair; somata in the T1 neuromere, axons to the SEZ) | Spontaneous rate | ~14 Hz, fed (n = 6) and 24 h deprived (n = 5); unchanged by 350 mM sucrose or 10 mM quinine; driven by leg movement | Cell-attached | "In both conditions, PER in neurons exhibited constant basal activity of ~14 Hz" ✓ | [Mann 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750742/) |
| OA-VUMd DNs (`DNge138` and others) | Spontaneous rate | 4.1 ± 3.1 Hz; every cell active, regular (ISI CV 0.43) | Whole-cell | "DNs in this cluster fired at 4.12±3.12 Hz (n = 11)" ✓ | [Babski 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064449/) |
| TH-VUM | Tonic rate vs hunger | 1 Hz just fed; 25 Hz after 24 h (cells 8–49 Hz, fig.); three other ventral SEZ DA neurons unchanged | Loose patch | "The lowest average tonic firing rate (1 Hz) was found in flies that had recently been fed, whereas the highest rate (25 Hz)…" ✓ | [Marella 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310174/) |
| ISN (`ISN`) | Tonic rate vs hunger | ~0.8 Hz fed vs ~3.4 Hz after 24 h (fig.); needs AKHR | Cell-attached | "ISN activity decreased in the fed state and increased in the starved state" ✓ | [Jourjine 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983267/) |
| IPC | Spontaneous rate | 0–1.4 Hz fed; median ~0 after 24 h; Vm −51 → −59 mV | Patch | "The baseline firing rate varied between individual IPCs and ranged from 0 to 1.4 Hz" | [Bisen 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11778929/) |
| Sugar GRNs (Gr5a) | Spontaneous rate | ≈0 Hz (sparse spikes) | Tip recording, fed | — | [Inagaki 2014 Nat Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4151318/) Fig. 1d (fig.) |
| MN9 | Activity vs behaviour | Calcium present exactly when the rostrum moves | G-CaMP + video | "we observed a perfect correlation between rostrum movement and motor neuron activity" ✓ | [Gordon & Scott 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2650400/) |
| MN9 | Needed at rest? | TNT silencing leaves the resting posture unchanged | Behaviour | "Silencing mn9 with tetanus toxin (Sweeney et al., 1995) did not impair proboscis position or joint angles at rest" ✓ | [McKellar 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7316511/) |
| Spontaneous PER, awake | Frequency | Rare in tethered flies | Video | "Proboscis extension was filmed during rare instances when it occurred spontaneously." ✓ | same |
| Proboscis extensions in deep sleep | Frequency | Bursts at 0.34 Hz; haustellum flip 636 ± 46 ms (71 ± 6 ms in PER) | Tethered, sleeping | "During these bursts, a PE occurs about every 3 s (Fig. 1C), with an average frequency of 0.34 Hz" ✓ | [van Alphen 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7817094/) |
| SEZ, pan-neuronal | Spontaneous calcium events | 1–2 rhythmically active cells in ~5% of preparations (18–24 h FD) | nSyb>GCaMP6s, nuclear ROIs | "in approximately 5% of preparations, there is spontaneous rhythmic activity of a few cells (1–2)" ✓ | [Harris 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4474761/) |
| same | Sugar-recruited cells | 23 ± 1 sucrose-only, 6 ± 1 water-only, 8 ± 1 both, per SEZ; 12 ± 1 of them MNs | same | "On average, 23 ± 1 cells/SEZ were sucrose-selective, 6 ± 1 were water-selective, and 8 ± 1 cells were activated by both" ✓ | same |
| DNs in general | Activity at rest | Fewer active at rest than during walking (calcium) | Population imaging | "the largest fraction of recorded DNs encode walking while fewer are active during head grooming and resting" ✓ | [Aymanns 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9605690/) |
| 2Ns, 3Ns, premotor taste neurons, MN9 | Resting rate | **None published.** Every measurement is ΔF/F against the trial's own baseline. None of Shiu 2022's neurons dips below baseline to bitter or water (fig.) | — | — | Sub-agent search of Shiu 2022, Snell 2022, Sterne 2021, Engert 2022, Kim 2017, Harris 2015, Yapici 2016 |

### 3.2 Inhibitory restraint and disinhibition

| System (MaleCNS) | Finding | Preparation | Quote | Source |
|---|---|---|---|---|
| DSOG1 identity | Four GABAergic "descending suboesophageal neurons" (98-Gal4 ∩ 276B-FLP). Soma in the ventral SEZ; arbors in the SEZ and VNC | Mosaic silencing screen | "Here, we identify four GABAergic interneurons in the Drosophila brain that establish a central feeding threshold" ✓ | [Pool 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4092013/) |
| DSOG1 → MaleCNS | MaleCNS synonyms give `DNg70` and `DNg98` (2 cells each; GABA-predicted; hemilineage MX3). FlyWire support is partial: of four "DSOG1" IDs among ISN targets (8.18% of ISN output ✓), one maps to DNg98, one to DNg70, one to DNg27 (glutamate) and one to no type. FlyWire lists leucokinin for DNg70; the final eLife version moves the leucokinin SELK neurons to DNg68. **Likely, not proven** | EM annotation | — | Sub-agent; [González-Segarra 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10513480/) ✓; [Mollá-Albaladejo 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12240583/) |
| DSOG1 silencing, PER | Fed, tarsal (fig.): 100 mM sucrose 78% vs 15–20% in controls; 1 M 92% vs 46–51%; water 44% vs 5–8%; denatonium 43% vs 2–3%. In 24-h-deprived flies both groups reach 95–98% at ≥100 mM | Kir2.1, n = 60 | "flies lacking DSOG1 activity showed increased proboscis extension to nutrients and bitter compounds in fed and deprived states" ✓ | same |
| DSOG1 silencing, intake | ~150 s of drinking of any fluid, including 1 mM denatonium, 6 M NaCl or ethanol, fed or deprived. Controls: 0 s fed, ~17 s deprived | Temporal consumption assay | "a new layer of inhibitory control in feeding circuits that is required to suppress a latent state of unrestricted and non-selective consumption" ✓ | same |
| DSOG1 activation | Sucrose intake −1/3 (17 → 11 s); water −1/2 | dTRPA1 | — | same (fig.) |
| DSOG1 → motor neurons | Denatonium drives E49 (MN9) and MN11 only when DSOG1 is silenced. No light-level contact with either | GCaMP | "Stimulation with denatonium produced strong GCaMP responses in E49 and MN11 in DSOG1-inactivated flies but not in controls" ✓ | same |
| DSOG1 and hunger | Constant inhibition, which the authors suggest other systems override | Discussion | "This implies that DSOG1 inhibition is overcome or bypassed in deprived states." ✓ | same |
| PERin | Silencing gives constant extension; activity sets the PER threshold; activated by leg mechanosensation and movement | Kir2.1; cell-attached; GCaMP | "Nearly 100% of flies with chronically silenced E564 neurons exhibited constitutive proboscis extension" ✓; "E564 neurons modulate the threshold of PER, with high activity suppressing and low activity promoting proboscis extension" ✓ | [Mann 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750742/) |
| TRdm GABAergic local neurons | Activated by sugar and bitter, sated or starved; silencing shifts labellar PER ~3× to lower sucrose, fed and starved | GCaMP; TNT | "TRdm neurons express the inhibitory transmitter GABA, and silencing these neurons increases appetitive feeding behavior" ✓ | [Zhao 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10728805/) |
| GABA-B on sweet GRNs | GABABR2 RNAi in Gr64f GRNs raises PER; 24 of 36 taste-responsive GAD1 neurons are excited by both sweet and bitter (evoked, not tonic) | 22–24 h starved | — | [Chu 2014](https://doi.org/10.1016/j.cub.2014.07.020) |
| Bitter → premotor | Scapula (`GNG087`, glutamate; >150 bitter-GRN synapses) targets Roundup and Rounddown; bitter co-activation cuts Roundup's sugar response, not G2N-1's | EM; GCaMP, FD | "Scapula synapses directly onto two feeding initiation premotor neurons, Roundup and Rounddown" ✓ | [Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/) |
| Quasimodo disinhibition | 16/31 top three-hop LB3→proboscis-MN motifs are disinhibitory (2.9% expected); Quasimodo (`GNG042`) is in 12/16. Quasimodo → `GNG015` (329 synapses) → MN9 (473) | MaleCNS connectome; Shiu LIF with `GNG015` driven at 100 Hz | "tonically inhibiting feeding at multiple circuit layers, an inhibition that attractive input overrides through sustained disinhibition and feedforward excitation" ✓ (author PDF) | [Tastekin 2026, Cell](https://doi.org/10.1016/j.cell.2026.08.016) ([PP 2025](https://doi.org/10.1101/2025.08.25.671814)) |
| GABAergic SEZ neurons whose activation evokes PER | Phantom 0.6 and Tentacular (`GNG129`) 0.5 of flies extend the rostrum; "buddy" (`GNG180`/`GNG184`) 0. The zero-baseline model mispredicts these | SEZ split-GAL4 screen | "Our model failed to predict behavioural results in the SEZ split-GAL4 screen (Fig. 2) when the neurons tested were predicted to be inhibitory (that is, Tentacular or Phantom)" ✓ | [Shiu 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/) |
| PER habituation | Needs GABA release from GAD1 neurons; acute block of GAD1 output left naive PER unchanged (data not shown) | 24 h starved males | — | [Paranjpe 2012](https://doi.org/10.1101/lm.026641.112) |
| Satiety brakes | AstA activation blocks the starvation shift in PER without affecting unstarved flies (Hergarden 2012, [PMC3309792](https://pmc.ncbi.nlm.nih.gov/articles/PMC3309792/)). MIP silencing makes sated flies extend like starved ones ([Min 2016](https://www.cell.com/current-biology/fulltext/S0960-9822(16)00079-8)). Hugin silencing speeds feeding onset in fed flies ([Melcher & Pankratz 2005](https://pmc.ncbi.nlm.nih.gov/articles/PMC1193519/)); hugin activity is higher when sated, acting through AstA ([Qin 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13143273/)). Serotonergic R50H05 activation makes sated flies extend like starved ones ([Albin 2015](https://doi.org/10.1016/j.cub.2015.08.005)) | Various | — | Sub-agents; peptide effects are outside the fast model |
| Bitter interneuron (Bohra) | One cholinergic pair; activation cuts PER to sucrose to <4% of trials | TrpA1; shibire | — | [Bohra 2018](https://doi.org/10.1016/j.cub.2018.01.084) (abs; [PP](https://www.biorxiv.org/content/10.1101/170464v1.full)) |
| "Wanderer" | Nothing found under that name | — | — | Sub-agent |

**Answer to "does the fed state hold PER back by tonic inhibition that hunger releases?"**
- Fed flies do carry tonic inhibition. DSOG1 and PERin fire at 14–17 Hz, and removing either releases PER. Silencing TRdm, MIP or GABA-B signalling also raises PER.
- But this inhibition does not change with hunger (DSOG1 ✓, PERin ✓). Nodes from the 3Ns to MN9 drive the same PER fed or starved ✓. Hunger raises excitatory gain upstream: GRN terminals, G2N-1, Clavicle, Fdg, TH-VUM and ISN.
- Most identified inhibition that varies is phasic: bitter through Scapula, taste-evoked GABA (TRdm, Chu 2014) and mechanosensory input (PERin). Hunger also weakens bitter input after 24 h.

### 3.3 Hunger gating: where and how much

| Stage (MaleCNS) | Quantity: fed → starved | Preparation | Quote | Source |
|---|---|---|---|---|
| Sugar GRN spikes | No change | Tip recording, wet-starved | "extracellular recordings from GRN somata in the labella indicated no change in the frequency of sucrose-evoked spiking in wet-starved vs. control fed flies" ✓ | [Inagaki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3295637/) |
| Sugar GRN spikes (conflicts) | +~20% (16 h starved); an increase at low sucrose in one strain only | Tip recording | — | [Meunier 2007](https://doi.org/10.1242/jeb.02755) (sub-agent summary); [Nishimura 2012](https://doi.org/10.3109/01677063.2012.694931) (abs) |
| Gr5a terminal calcium | 100 mM: ~8 → 30% ΔF/F; 400 mM: 34 → 50% (n.s.) | 1 day wet-starved, in vivo | "…at 100 mM sucrose, and a non-significant trend to enhancement at 400 mM sucrose" ✓ | Inagaki 2012 (fig. 6C/D) |
| Gr5a terminal calcium, bath dopamine | Baseline ×1.2; 400 mM response ×1.3–1.4; blocked by DopEcR RNAi | Explant, 1 mM DA | "a ~1.2 fold increase in basal Ca 2+ influx, and a ~1.3–1.4 fold influx in Ca 2+ influx caused by 400mM sucrose" ✓ | Inagaki 2012 |
| Gr5a / Gr64f calcium (conflicts) | No change (starved = 110/83/98% of fed at 10/50/100 mM; flies ≥2 weeks old); a trend (p = 0.063) in another lab; increases in two 2026 papers | 24 h / 1–2 days | "we did not observe any significant differences" | [Kain 2015](https://doi.org/10.1016/j.neuron.2015.01.005); [Devineni 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579511/); [Qin 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13143273/); [Arntsen 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13595129/) |
| Sweet GPNs (sGPN, AMMC projection) | ΔF/F at 10/25/50/100 mM: 35/38/68/128% → 52/80/118/108% | 24 h wet-starved | "significant increase in the sensitivity of these neurons to 25 and 50 mM sucrose" | Kain 2015 (fig. 7A) |
| Clavicle (`ANXXX462a`) | PER to its activation at 1.8/8.9/17.8/153 µW/mm²: fed 0/6/13/22% vs FD 9/35/53/66% | CsChrimson, 48 h wet-starved | "activation of two second-order neurons, G2N-1, and Clavicle, increased proboscis extension in food-deprived flies, whereas activation of all other neural classes did not" ✓ | [Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/) + source data (fig.) |
| G2N-1 (`GNG232`) | fed 0/30/73/98% vs FD 0/56/86/97% | same | same | same |
| FMIn (`GNG197`) | fed 0/3/22/78% vs FD 0/12/34/91% (trend, p ≈ 0.06) | same | — | same (fig.) |
| Sugar GRNs, optogenetic | fed 1/13/16/56% vs FD 30/64/69/96% | same | "CsChrimson-mediated activation of sugar GRNs caused higher proboscis extension rates in food-deprived flies than in fed flies" ✓ | same |
| Rattle, Roundup, Bract, Fdg, MN9 | No difference (e.g. MN9 fed 12/96/98/96% vs FD 16/96/96/92%) | same | "activation of MN9 elicited the same proboscis extension rate in food-deprived and fed flies" ✓ | same |
| Fdg (`GNG588`) | Calcium to 400 mM labellar sucrose only when starved | GCaMP3, in vivo | "neither labellar opening nor Ca2+ elevation in the Fdg-neuron was observed in satiated flies" ✓ | [Flood 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3727048/) |
| Fdg (conflict) | No response to proboscis taste in FD flies; responds to optogenetic GRN activation | GCaMP7b | "Fdg, did not respond to proboscis taste stimulation, but did respond to optogenetic activation of sugar-sensing GRNs" ✓ | Shiu 2022 |
| SELK (`DNg68`) | Sweet responses only when starved; bitter in both states; baseline unchanged | GCaMP, 21–24 h | "sweet substances elicit responses only when the animal is starved" | [Savaş 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13096221/) |
| IN1 (12 cholinergic local neurons; ingestion) | Peak ΔF/F₀ to 1 M ingestion ~1.1 → 2.1 (fig.); persistent only when fasted (7 min, to 57% of peak) | GCaMP | "Sucrose responses of IN1 interneurons in fed flies were significantly smaller and lacked persistent activity" ✓ | [Yapici 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544016/) |
| 2N population (trans-Tango) | Slightly more ROIs respond to several sugars | 22–26 h | "while we observed a general increase in the proportion of ROIs responding to multiple sweet tastants, this increase was small" ✓ | [Snell 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9474709/) |
| Bitter GRN calcium | Response to 0.07 mM lobeline halves (0.6 → 0.3 ΔF/F); no change at 0.31–1.25 mM | 2 days | — | [Inagaki 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365050/) (fig. 5G) |
| OA-VL (bitter potentiation) | Tonic firing −50% at 24 h (Babski 2024 saw no drop: conflict) | Cell-attached | "we did not observe a decrease in the firing rate of the VL neurons in starved flies" ✓ (Babski) | [LeDue 2016](https://doi.org/10.1016/j.cub.2016.08.028); [Babski 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064449/) |

**Modulators**

| Modulator | Releasing neurons (MaleCNS) | Site | Direction and size | Source |
|---|---|---|---|---|
| Dopamine | TH-VUM (no model output) | Sugar GRNs. DopEcR is needed only early (6 h); TH-VUM-driven PER needs D2R | TH-VUM 1 → ~10 (12 h) → 25 Hz (24 h). "dopamine acts as a gain control system to alter the probability of proboscis extension" ✓ | Marella 2012; Inagaki 2012 |
| dNPF | NPF neurons (`NPFL1-I`; NPF1 = `DNp29`) | Upstream of dopamine, indirectly (NPFR knockdown in DA neurons has no effect) | Activation makes fed flies as sugar-sensitive as starved ones; no effect on bitter | Inagaki 2014 |
| sNPF | ~11–12 lateral neurosecretory cells | sNPFR on GABAergic neurons → bitter GRNs | Needed for the bitter decrease; no effect on sugar | Inagaki 2014 |
| AKH | Corpora cardiaca (outside the connectome) | ISN (AKHR, direct) | ISN 0.8 → 3.4 Hz (fig.) | Jourjine 2016 |
| Insulin | `IPC`; ISN releases dILP3 | InR on sweet GRNs suppresses them | InR knockdown raises PER in fed flies only; IPC firing → ~0 in hunger | Arntsen 2026; Bisen 2025; González-Segarra 2023 |
| Octopamine | `OA-VPM4` | OAMB on sugar GRNs | ~×1.4 at 100 mM in fed flies only: "application of octopamine potentiates sensory responses to sucrose in satiated flies" ✓ | [Youn 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6021039/) |
| SIFamide | 4 PI neurons | Broad, including the SEZ | Activation in sated flies raises PER to 0.5–1 M from ~0.33 to 0.64 (fig.); no further rise when starved | [Martelli 2017](https://doi.org/10.1016/j.celrep.2017.06.043) |
| Hugin → AstA (fed brake) | `Hugin-RG`, `AstA1` (subclass match unchecked) | AstA-R1 on Gr5a GRNs | Hugin activity higher when sated; no effect sizes | Qin 2026; Hergarden 2012 |
| Leucokinin | SELK (`DNg68`) | 2N with sweet and bitter input | Lk release suppresses feeding; ACh promotes it | Mollá-Albaladejo 2025; Savaş 2026 |
| 5-HT | Sugar SEL (`GNG540`, `GNG550`, `GNG056`) and others | IPCs and others | Sugar-SEL activation cuts intake; R50H05 activation evokes hunger-like feeding | [Yao & Scott 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8930643/); Albin 2015 (abs) |

Expression in G2Ns barely changes after 24 h without food: "no variation in expression levels for any neurotransmitter receptors" (Mollá-Albaladejo 2025).

### 3.4 Behavioural PER thresholds, fed vs starved

| Study (assay) | Fed | Starved | Threshold shift | Quote |
|---|---|---|---|---|
| [Inagaki 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4365050/) (labellar) | 800 mM ≈60% | 400 mM ≈92% (1 day), ≈95% (2 days) | S50 ≈700 → 270 (6 h) → 200 (24 h) → 150 mM (48 h) (fig.) | "A comparison of fed vs. 2 days starved flies revealed that sugar sensitivity alone changes 4.6 fold" ✓ |
| [Inagaki 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3295637/) (labellar) | 200 mM ≈10%, 400 mM ≈68% | 2 days: 50 mM ≈50%, 200 mM ≈93% | Mean acceptance threshold ≈330 → 120 (1 day) → 42 mM (2 days), ~2.8× and ~8× (fig.) | "significant changes observed as early as 6 hours of wet starvation" ✓ |
| [Marella 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310174/) (tarsal, transgenic controls) | 10/100/316/1000 mM: 0/~5/~20/~22% | 24 h: ~51/69/74/82% | — | (fig.) |
| [Pool 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4092013/) controls (tarsal) | 100 mM 15–20%; 1 M 46–51% | 24 h: ≥100 mM ~95% | — | (fig.) |
| [Devineni 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6579511/) | 300 mM: 79% | — | — | "79% of fed flies exhibited PER to 300 mM sucrose alone" |
| [Martelli 2017](https://doi.org/10.1016/j.celrep.2017.06.043) controls | 1 M: 10–16% (18 °C), 32–36% (29 °C) | 12–28% / 64–84% | Strongly temperature-dependent | (fig.) |
| [Yapici 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544016/) (drinking) | Most do not drink 1 M sucrose | 24 h: drink avidly | — | "Most of the fed flies (0 hr fasted) did not consume 1 M sucrose." ✓ |

Fed flies do extend to strong sugar, in about 20–80% of trials depending on genotype, temperature and body part. A fed-like resting brain should therefore still drive MN9 at strong drive.

### 3.5 Latency, drive, and command-like stages

| Quantity | Value | Preparation | Quote | Source |
|---|---|---|---|---|
| Sucrose on the legs → rostrum lift | Mean ≈225 ms (single trials ≈40–400 ms); haustellum +75 ms, labellar extension +210 ms, spread +365 ms; fed = starved | Video, 25–50 fps (fig.) | "we did not observe significant deviations of the temporal sequence in fed flies compared to starved flies" ✓ | [Schwarz 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5315463/) |
| Sequence generation | Each movement is started centrally, not by the previous one | Activation experiments | "the execution of one movement does not automatically trigger the initiation of the subsequent movement" ✓ | same |
| Food contact → labellar spread | As short as 10 ms; bristle mechanosensory → MN monosynaptic (~2 ms) | 200 fps; patch | "could be as short as 10 ms" ✓ | [Zhou 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6531006/) |
| Light → first GRN spike | ≈5 ms (first pulse), 10–20 ms later | Gr5a>ReaChR tip recording (fig.) | — | [Inagaki 2014 Nat Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4151318/) |
| GRN drive that triggers PER | One 100-ms pulse: ~20 Hz per GRN in a 200 ms bin (~4 spikes), up to ~50 Hz in single cells, PER on each pulse. Continuous light: GRNs peak ~22 Hz and adapt; PER ~50% at ~10 Hz, ~0 at 4–5 Hz (fig.) | Fed flies | "pulsatile illumination (1 Hz, 100 msec pulse duration) evoked a train of PERs time-locked to each light pulse" ✓; the decay of spiking and PER correlate, "r = 0.96" ✓ | same |
| GRN → MN9 spike latency | **Not found**; MN9 data are calcium at 0.3–1 Hz | — | — | Sub-agent |
| MN9 grading | Calcium roughly doubles from 100 mM to 1 M sucrose | E49>G-CaMP | "stimulation with 1M sucrose elicited almost twice the activity of 100mM sucrose" ✓ | [Gordon & Scott 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2650400/) |
| Feedforward reading | Graded MN9 calcium read as a simple feedforward path | — | "information about stimulus intensity is maintained at the level of the motor neuron and suggests that perhaps a relatively simple feed-forward circuit" ✓ | same |
| Circuit depth | Three intermediate layers | EM + imaging | "This circuit connects gustatory sensory neurons to proboscis motor neurons through three intermediate layers." ✓ | [Shiu 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9292995/) |
| Redundancy | Silencing single 2Ns reduces PER; silencing single 3Ns or premotor neurons does not | GtACR1, 50 mM sucrose | "Inhibiting activity of single second-order neurons reduced the behavioral response, whereas inhibiting activity of third-order or premotor neurons did not." ✓ | same |
| Fdg as command neuron | Activation of even one Fdg gives the whole feeding sequence in sated flies; bilateral ablation abolishes PER to sucrose (conflicts with Shiu 2022's acute silencing) | TrpA1; laser ablation | "reminiscent of the 'command neurons' first described by Wiersma and Ikeda in the crayfish" ✓; "The induced feeding thus represents a “fixed action pattern”" ✓ | [Flood 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3727048/) |
| Threshold at the motor end | MN9 activation PER is step-like: 12–16% → ~96% between the two lowest light levels, while sugar-GRN activation is graded (fig.) | CsChrimson | — | Shiu 2022 source data |
| Integration upstream of the motor layer | Brief sugar raises PER to water for 10–40 s; needs GRN activity afterwards; Fdg or MN9 activation does not do it | Behaviour | "PER to water increased most substantially (30%–40% higher than baseline) when tested within 10–40 s of sugar exposure" ✓; "neither Fdg nor MN9 activation enhanced PER to water 20 s later" ✓ | [Deere & Devineni 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9529979/) |
| Persistence | IN1 activity lasts minutes after ingestion, only when fasted | GCaMP | "In fasted flies, 1 M sucrose-evoked activity of IN1 neurons lasted for 7 minutes" ✓ | [Yapici 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544016/) |

**Reading.** PER behaves as a thresholded, all-or-none motor event fed by graded drive.
- MN9's optogenetic dose-response is a step. Its calcium coincides with movement on single trials. A single command-like neuron (Fdg) can trigger the whole program.
- Upstream drive is graded and hunger-shifted, with parallel paths.
- In the MaleCNS, the premotor layer contains a recurrent excitatory cluster (§1.3) that could supply the threshold. No physiology tests this.
- Integration over seconds to minutes (sugar priming, IN1) sits upstream of Fdg and MN9.

### 3.6 Models

**Peer-reviewed and preprints**

| Model | Setting | Taste result | What they needed | Source |
|---|---|---|---|---|
| Shiu 2024 (FlyWire LIF) | Silent: "The baseline firing of each neuron in our model is 0 Hz." ✓ | MN9 vs sugar rate: ~0 up to 30 Hz, 4.8 at 40, 19 at 50, 36 at 60, 58 at 80, 66 at 100, 93 at 200 Hz (sub-agent, from SI). Relays at 100 Hz: Zorro 102, Rattle 75, G2N-1 69, Clavicle 54, Roundup 46 Hz | w_syn fitted to sugar → MN9. The authors flag: "circuits in which there is extensive basal inhibition, not captured by the model because of the zero basal firing rate, may be poorly simulated" ✓, and "the model does not account for gap junctions, non-spiking neurons, internal state or long-range neuropeptides" ✓. Also: "inhibitory connections to an inactive neuron have no effect" ✓ | [PMC11446845](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/) |
| Walker, Peña-Garcia & Devineni 2025 (Sci Rep) | Shiu model, silent; GRNs at 25–200 Hz | 10–60% of 2Ns activated at low rates, 70–80% at high; 0–11% of 3Ns, rising to 3–33% | Nothing. They note: "some 3Ns receive taste input that is too weak to elicit neuronal firing on its own" ✓ | [PMC11821855](https://pmc.ncbi.nlm.nih.gov/articles/PMC11821855/) |
| Christie … Shao 2026 (Curr Biol) | Shiu model, silent, w_syn 0.37–0.39 mV | Sugar → Fox → ascending FDA neurons → PAM DANs | A higher weight: "The free parameter model synaptic weight (Wsyn) was adjusted to achieve differing levels of propagation" ✓ | [PMC12869359](https://pmc.ncbi.nlm.nih.gov/articles/PMC12869359/) |
| Tastekin … Ribeiro 2026 (Cell), on MaleCNS | Shiu code, silent, w_syn 0.275 mV | LB3 at 200 Hz drives MN9; lower with `GNG015` driven | Drove the brake by hand: "We therefore drove the inhibitory premotor neuron GNG015 at 100 Hz to establish tonic MN9 inhibition" ✓ (author PDF) | [doi](https://doi.org/10.1016/j.cell.2026.08.016) |
| Sapkal 2024 (Nature) | Shiu model | Sugar recruits GABAergic FG | Co-drove walking neurons to see inhibition | [doi](https://doi.org/10.1038/s41586-024-07854-7) |
| Savaş 2026 (Nat Commun) | Shiu model | SELK activation raises DNs and MNs | Nothing; the model sees only SELK's ACh, not its leucokinin | [PMC13096221](https://pmc.ncbi.nlm.nih.gov/articles/PMC13096221/) |
| An 2026 [PP] | Shiu model plus white membrane noise σ 3.0–3.5 mV (25% of cells active) | Sugar 100 Hz: MN9 29–49 Hz vs 65–68 Hz silent; bitter still vetoes | Noise alone; no bias, no depression | [doi](https://doi.org/10.64898/2026.09.19.752860); [code](https://github.com/aikian/flylite/blob/cba2afaa7b722936c7682d68e2dd1c5b05e24aa5/run_flylite.py#L41) (code/results only) |
| Li, Ping, Zhang & Wang 2026 [PP] | Shiu-form LIF fitted to spontaneous calcium with low-rank weight corrections | No taste test | "inhibitory hub neurons and their reciprocal synapses with excitatory partners are necessary and sufficient to sustain whole-brain resting-state dynamics" (abs) | [doi](https://doi.org/10.64898/2026.08.21.745055) |

No peer-reviewed model runs sugar → MN9 in a spontaneously active whole brain, and none implements a hunger state that rescues it (sub-agent, 99 citing works checked).

**GitHub projects [non-PR]**

| Project | Setting | Sugar → MN9 | What mattered |
|---|---|---|---|
| [Lulzx/fly-brain](https://github.com/Lulzx/fly-brain/blob/08cf8666bd3cb405c803f95821ebe06d22b3e5ab/docs/20-roadmap.md#L254-L283) | MaleCNS conductance LIF, inhibition ×0.58 | STD (U 0.2): 35 → 4 Hz even in a silent brain; SFA 2 mV → ~9 Hz; full-strength inhibition → 2.5 Hz | "stabilised activity but killed the sugar-to-proboscis pathway" (quoted in short_term_plasticity.md). An unshipped fix: antennal-lobe LNs ×8 plus outputs ×3 on `GNG232` and `DNge080` gave MN9 0.5 Hz idle and 125–159 Hz evoked |
| [neurofly](https://github.com/neuroflyapp/neurofly/blob/03f149d18852f83c9c23983d2b0eabe0574ffcb3/windows/src/sim.js#L69-L76) | 7.3k cells; random kicks everywhere; tonic bias in the core, zero bias on taste relays and MNs | GRNs at 29–78 Hz → MN9 53–273 Hz; rest 0 | Isolating the pathway from the noisy core; STD "cut the stimulus responses to a few Hz" |
| [flyverse-core](https://github.com/tel-0s/flyverse-core/blob/959f2e927b1c2806bc526fd5fc51cb3f5cc3e4b1/docs/audits/monoamine_slow_term.md#L425-L446) | MaleCNS Shiu LIF + SFA | 123.5 Hz by Shiu's rules; 4–11 Hz calibrated; each added tone cuts it | MN9 sits on a near-balanced E/I residual dominated by `DNge051` |
| [ask-the-fly](https://github.com/Felix471/ask-the-fly/blob/5f28a726ecde8d305ea33358c99bb4334ccf5618/docs/tonic_inhibition.md#L21-L28) | Shiu model, single brakes driven tonically | CB0806 (`GNG180`/`GNG184`) at 50 Hz abolishes MN9 at 100 Hz sugar | One tonic brake is enough |
| [cwklurks fork](https://github.com/cwklurks/Drosophila_brain_model/blob/87bdc4b860f38d4cfc926f98248a2760a088a6c9/STORY.md#L24-L28) | Shiu v783, silent | 10/25/50/100/200 Hz → 0/0/13.6/65/89.6 Hz | A recurrent excitatory premotor loop (CB0553 Roundup, `DNge059`, `DNge080`, CB0824 `GNG169`, CB0051 Sternum) "must ignite" |
| [FLYCNS](https://github.com/IONOFIELD/FLYCNS/blob/ccfdff2df4234c5b3bc0b2ebfcf9436d9f3217f9/results/feeding/mechanism.json) | MaleCNS, uniform depolarisation plus OU noise | MN9 fires, but so does a wind control | "taste -> MN9 in MaleCNS is disinhibitory; a silent network cannot express that" |
| [flybench](https://github.com/brandoncho369/flybench/blob/3052ce5fa9ab8cc0a9e101e8cd8f5bb520a80ff5/results/adaptive-lif-b-2-mv-tau-200-ms.json#L201-L221) | Shiu LIF, global gain 0.45, adaptive LIF; silent | 43.6 Hz with 0.7% of the brain active | "at the rate a real sugar GRN fires the reference model sits on the threshold of its own reflex" |
| kazemi, TheMrRaGe, hypnagogia, kick-the-fly | MaleCNS with global depression, noise or homeostats | Depression ends seizures, but motor output → 0; a 200 Hz afferent keeps 11% under STD | Global settings only |

**Theory**

| Claim | Source |
|---|---|
| With background noise, "firing rate modulations are transmitted linearly through many layers" | [van Rossum 2002](https://doi.org/10.1523/JNEUROSCI.22-05-01956.2002) |
| Rate signals propagate through several layers of network-generated background "if appropriate adjustments are made in synaptic strengths" | [Vogels & Abbott 2005](https://doi.org/10.1523/JNEUROSCI.3508-05.2005) |
| When excitation is cancelled by locally evoked inhibition, shifting the balance gates transmission on | [Vogels & Abbott 2009](https://doi.org/10.1038/nn.2276) |
| Balanced background input reduces gain divisively | [Chance 2002](https://doi.org/10.1016/S0896-6273(02)00820-6) |
| Depressing synapses transmit rate changes, not sustained rates | [Abbott 1997](https://doi.org/10.1126/science.275.5297.221) |

---

## 4. Gaps and caveats

- **No resting rate for any taste interneuron or MN9.** The only SEZ rates are DSOG1, PERin, OA-VUMd, TH-VUM, ISN and IPC. Every 2N, 3N and premotor measurement is ΔF/F against its own baseline. Nuclear GCaMP6s misses low-rate firing, so "few spontaneous calcium events" (Harris 2015) caps rates only loosely.
- **The inhibitors' resting state is unresolved.** No rate exists for `GNG015`, `GNG095`, `GNG130`, `GNG180`, `GNG184` or `DNge051`. The literature points both ways: mechanosensory-driven and phasic (their wiring; Zhou 2019), or tonic and released by disinhibition (Tastekin 2026's hypothesis; Shiu 2024's Phantom and Tentacular results).
- **Identity.** DSOG1 = `DNg70` + `DNg98` is likely but not proven, and FlyWire lists leucokinin for DNg70. PERin, TH-VUM, IN1, the sGPNs and OA-VL have no MaleCNS type. E49 = MN9 rests on Shiu 2022's citation of Gordon & Scott 2009.
- **Conflicts.**
  - Starvation's effect on GRN calcium and spiking differs between labs: ×3.5 at 100 mM (Inagaki 2012) vs no change (Kain 2015, older flies).
  - Fdg's hunger dependence and necessity differ between Flood 2013 (ablation, natural sugar) and Shiu 2022 (acute silencing, split lines).
  - OA-VL's starvation drop was seen by LeDue 2016 but not by Babski 2024.
- **Hunger effects on 2Ns rest on behaviour.** Shiu 2022 imaged every 2N in food-deprived flies only. The central-node conclusion comes from PER to optogenetic activation, fed vs 48 h starved.
- **Latency.** No GRN → MN9 spike latency exists. The ~225 ms from leg sucrose to rostrum lift is behavioural and figure-read.
- **My probes are not tests.**
  - Each ran 16 flies without full recalibration and without checking bitter, REST, ignition or looming.
  - The toy treats inputs as independent Poisson trains.
  - MN9 R's 523 input synapses look incompletely reconstructed.
  - Recalibrating the route after removing its depression may change the numbers.
- **Outside the model.** These brakes and accelerators cannot act in a fast-transmitter LIF without new mechanisms:
  - presynaptic inhibition of GRNs (GABA-B; mechanosensory inhibition of sweet GRNs);
  - dopamine and octopamine at GRNs;
  - peptides: AstA, MIP, hugin, DSK, leucokinin, dILP3, SIFamide, NPF;
  - serotonin.
- **Not found:** a whole-brain model with spontaneous activity that passes sugar → MN9 (peer-reviewed); EMG or spike recordings of proboscis MNs at rest; "Wanderer" neurons.
- **Partly read:**
  - Figure values were not digitised for Hergarden 2012, Min 2016, Chu 2014 and Zhao 2022.
  - Albin 2015 and Bohra 2018 were read as abstracts (Bohra's preprint in full).
  - Manzo 2012 could not be opened by the sub-agent.
  - An 2026 and Li 2026 [PP] were read through code, results files and abstracts only.
  - Kain 2015 was read by a sub-agent from an archived copy.
