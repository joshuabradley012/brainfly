# MBON11's Kenyon cell drive: where Hige et al.'s 250 pC comes from

Read 2026-10-10. This file extends:
- `mbon11_input.md`: MBON11 measurements, hemibrain counts, Yamada 2024 and Hige 2015 details.
- `kc_classes_and_apl.md` and `kenyon_cell_odor_responses.md`: per-class KC excitability; Turner 2008.
- `kc_integration.md`: KC time courses.
- `hige2015_specificity.md`: Hige's Fig. 3/4 charges, cell by cell.
- `oct_mch_input.md`: KC fractions for OCT and MCH.

Numbers already established there are cited, not re-derived.

**The puzzle.** Values are from `experiments/odor_probe44.json`.
- The model's KCs answer 3-octanol (OCT) at 3.1%: α/β 4.09% with 1.68 spikes per response, α′/β′ 3.45% (1.09), γ 1.67%
  (1.01). These use Turner's 0.5-s protocol and reliability criterion.
- Its KC-to-MBON11 synapses carry 0.030 pC per synapse per KC spike.
- MBON11's KC input to OCT is 27.1 pC per cell in 0–1.4 s: above-rest KC spikes × synapses × 0.030, averaged over the
  two MBON11s. That is ≈ 903 synapse-spikes per cell, and MBON11 gains ≈ 8.5 spikes.
- 4-methylcyclohexanol (MCH) gives 5.3 pC and 1.6 spikes.
- Hige et al. 2015 measured ≈ 250 pC and ≈ 118 spikes (`mbon11_input.md` §2).

Conventions:
- Quotes are verbatim; citation numbers inside them are dropped.
- (fig., approx.): read off a figure. The method is given; good to about ±10–20%.
- (derived): my arithmetic, shown.
- "Not reported": searched in the full text and legends, not found.
- "Synapse-spikes": KC spikes × that KC's synapses onto the MBON. Charge = synapse-spikes × q, with q the charge per
  synapse per spike.
- Connectome numbers are MaleCNS v1.0 (`~/fly-data/raw`, min. confidence 0.5) unless marked hemibrain.

## Summary

### The answer

**Mostly more KC activity, partly more charge per synapse, no other excitatory input.** The model is short by ≈ 9× in
synapse-spikes × q. The data allow neither lever to close that alone; both must rise, KC activity more.

1. **Other excitatory inputs: ruled out.**
   - KCs supply 85–87% of each MBON11's input synapses.
   - Cholinergic non-KC inputs total 57–63 synapses (0.20–0.32%), with no projection neurons (1 synapse).
   - The rest of the input is dopaminergic, GABAergic, glutamatergic and octopaminergic (§1). The hemibrain agrees.
   - No study found blocked KC output while recording an MBON's odor response (§4).
2. **Larger per-synapse charge alone: ruled out.**
   - With the model's KC activity (≈ 750–900 synapse-spikes per cell), 250 pC needs q ≈ 0.28–0.33 pC.
   - Yamada et al. 2024's flash data cap q for γ synapses at ≈ 0.095 pC. That cap assumes every labelled γ KC fired
     exactly once and only 3% were labelled.
   - The unitary KC→α2sc route, corrected for mecamylamine, gives ≈ 0.004–0.013 pC (§2).
3. **More KC activity alone: unlikely.**
   - At q = 0.030, 250 pC needs ≈ 8,300 synapse-spikes on MBON11_R.
   - γ-main KCs hold 59% of MBON11's KC synapses. To supply that many synapse-spikes, 12–15% of them would have to
     respond with 3–4 spikes each.
   - That is 3–6× above every γ measurement: Turner 2.3% of odor–cell pairs, Murthy 0 of 20 pairs, γ-only imaging
     sparser than pan-KC imaging (§3).
4. **In vivo vs ex vivo: no evidence of a systematic difference.**
   - Yamada (ex vivo) and Hige (in vivo) used the same saline, the same Cs⁺/QX-314 internal and the same holding
     potential.
   - Hige's charge is the same with a K⁺ internal (Fig. 4) as with Cs⁺/QX-314 (Fig. 3).
   - The real uncertainty is converting a flash into spikes, not the preparation (§2.6).

### The numbers (derived)

5. **Flies' KC activity onto MBON11 at Hige's stimulus** (2% saturated vapour, 1 s):
   - ≈ 3,200 synapse-spikes on MBON11_R in 0–1.4 s (range 1,300–7,500).
   - That is 3.5–4× the model's (range 1.5–10×).
   - Per-class basis (§3.7): γ-main ≈ 3.5% × 3.5 spikes, α/β (s, m, c) ≈ 6% × 2.5, α′/β′ ≈ 20% × 5; γ-d and α/β-p are
     inhibited, not excited.
6. **Effective charge.**
   - 250 pC ÷ 3,200 ≈ 0.08 pC per synapse per spike (range 0.03–0.19), ≈ 2.5× the model's 0.030.
   - That fits Yamada's γ data only if each flash drove ≈ 19 γ KCs once (≈ 2.5% of γ KCs), just below SPARC2-S's
     3–7%.
   - Yamada's three α/β example cells carry 2–3× the γ examples' charge from KCs with 3.3× fewer synapses on MBON11.
     So part of the extra charge may belong to α/β synapses (§2.4). That rests on example traces only.
7. **Re-measured Yamada charge.**
   - 26–43 pC per flash, not ≈ 19, once the slow tail is included. That is 0.47–2.0 pC per labelled γ KC and
     0.022–0.095 pC per synapse per flash (§2.1–2.2).
   - The model's 0.030 reproduces this if each labelled γ KC fires ≈ 1–2.5 spikes per flash.
   - Spikes per flash were never measured; ≈ 1–3 is derived from CsChrimson and KC kinetics (§2.3).
   - The EPSC still carries 15–26 pA 1.5 s after the flash, which points to more than one spike.
8. **MBON11's transfer in flies.**
   - From Hige's Fig. 4, with spikes and charge from the same 6 cells: spikes(0–1.4 s) ≈ 0.545 × Q(pC) − 15.5.
   - Threshold ≈ 28 pC; residuals ≤ 2.3 spikes over four group means (§4).
   - At the model's 27 pC the fit predicts ≈ 0 spikes, and the model gives 8.5. At high input the model is less
     responsive: 0.26–0.41 spikes per pC against 0.545.
9. **MBON input against the number of active KCs.** No experiment relates them with counted KCs. The only quantitative
   relation is Hafez et al. 2023's MBON-α3 model: linear, ≈ 0.017–0.020 mV per active synapse (§5).

### What to recalibrate

- KC activity at Hige's stimulus: per-class targets in item 5 and §3.7.
- q to ≈ 0.07–0.08 pC; or γ ≈ 0.03–0.05 and α/β ≈ 0.1–0.2 if Yamada's α/β examples hold.
- Check against three things:
  - Yamada's flash charge: 26–43 pC from a random 3–7% of γ KCs.
  - Hige's 250 pC, measured per cell on the right MBON11. MaleCNS's left MBON11 has 31% fewer KC synapses (§1.1).
  - The transfer function in item 8.
- MCH's input (5.3 pC, 50× short) needs the antennal-lobe fix in `oct_mch_input.md` first.

---

## 1. Connectome: MBON11's inputs (derived)

MaleCNS v1.0: both MBON11s are "Roughly traced"; transmitters are consensus predictions. Hemibrain v1.2:
traced-adjacency export, right MBON11 only; it has no transmitter column.

### 1.1 Totals

| | MaleCNS MBON11_R (11402) | MaleCNS MBON11_L (10704) | hemibrain MBON11_R |
|---|---|---|---|
| All input synapses | 28,316 | 19,812 | 26,228 |
| From KCs | 24,597 (86.9%), from 2,136 KCs | 16,863 (85.1%), from 2,048 KCs | 22,647 (86.3%), from 1,694 KCs |
| Synapses per connected KC | 11.5 | 8.2 | 13.4 |

- The left MBON11 has 31% fewer KC synapses than the right, for the same type and tracing status. The right one is close
  to the hemibrain's.
- 97–98% of each MBON11's KC synapses come from its own side's KCs. Opposite-side KCs supply 415 synapses on R and 455
  on L.

### 1.2 KC inputs by class (MaleCNS)

| KC type | MBON11_R: KCs, synapses (per KC), share | MBON11_L: KCs, synapses (per KC), share |
|---|---|---|
| KCg-m (γ main) | 667, 14,387 (21.6), 58.5% | 701, 9,826 (14.0), 58.3% |
| KCg-d | 107, 2,086 (19.5), 8.5% | 99, 1,187 (12.0), 7.0% |
| KCg-s1–4, KCg | 5, 195, 0.8% | 6, 139, 0.8% |
| KCab-s | 503, 4,100 (8.2), 16.7% | 421, 1,759 (4.2), 10.4% |
| KCab-m | 360, 1,795 (5.0), 7.3% | 342, 2,347 (6.9), 13.9% |
| KCab-c | 232, 1,333 (5.7), 5.4% | 297, 1,258 (4.2), 7.5% |
| KCab-p | 67, 365 (5.4), 1.5% | 61, 193 (3.2), 1.1% |
| KCa′b′ (ap1, ap2, m) | 195, 336 (1.7), 1.4% | 121, 154 (1.3), 0.9% |
| **γ total** | **779, 16,668 (21.4), 67.8%** | **806, 11,152 (13.8), 66.1%** |
| **α/β total** | **1,162, 7,593 (6.5), 30.9%** | **1,121, 5,557 (5.0), 33.0%** |

- Spread onto MBON11_R, 10th/50th/90th percentile synapses per KC:
  - KCg-m 14/21/30, KCg-d 13/19/27.
  - KCab-s 1/8/14, KCab-m 1/4/11, KCab-c 1/5/11.
- The hemibrain splits these as γ 62.8% and α/β 36.5% (`mbon11_input.md` §4.1).
- **Olfactory-capable synapses.**
  - γ-d KCs get 0.7% of their input from antennal-lobe PNs. That is 0.2 PN partners of ≥ 3 synapses on average, median
    0, against 6.6 for γ-main and 4.7–5.6 for α/β.
  - Their other inputs are APL, DPM and visual projection neurons (aMe12, MeVP41, LoVP42, MeVP36, aMe20, LoVP71,
    MeVP25), plus PLP095, CL258 and AVLP043.
  - α/β-p get 1.5% of their input from PNs.
  - So on MBON11_R the olfactory-capable KC synapses are γ-m + γ-s + α/β-s/m/c + α′β′ ≈ 22,146, 90% of the KC total.

### 1.3 Non-KC inputs

MBON11_R: 3,719 synapses (13.1%). MBON11_L: 2,949 (14.9%).

| Source (consensus transmitter) | R | L |
|---|---|---|
| PPL101 = PPL1-γ1pedc (dopamine) | 1,391 | 920 |
| Untyped fragments ("unclear"; 478 / 544 bodies, ≤ 7 / 9 synapses each) | 586 | 671 |
| APL (GABA) | 261 | 180 |
| MBON05 = γ4>γ1γ2 (glutamate) | 225 | 181 |
| DPM (predicted dopamine; serotonergic and GABAergic in the literature) | 217 | 131 |
| Other glutamatergic (MBON06 β1>α, MBON02 β2β′2a, MBON25, MBON30, …) | 329 | 313 |
| Other GABAergic (MBON20, contralateral MBON11, MB-C1, mALD3, LoVC20) | 203 | 174 |
| Other dopaminergic (PAMs, PPL102–106) | 248 | 213 |
| Octopaminergic (OA-VPM3, OA-VPM4) | 198 | 97 |
| **All cholinergic non-KC** | **57 (0.20%), 39 bodies; largest CRE072, 9** | **63 (0.32%), 27 bodies; largest MBON14, 23** |
| Projection neurons | 1 (M_lvPNm30) | 0 |

- **Hemibrain MBON11_R:** non-KC 3,581 (13.7%).
  - Named inputs: PPL101 1,950; DPM 409; MBON05 198; APL 168; OA-VPM3/4 181; PPL102 107; PAMs ≈ 170; contralateral
    MBON11 70; MBON06 66; MBON02 44.
  - The only other possibly excitatory named inputs are LHCENT1 and MBON29, 6 synapses each.
- **Bound.** Even if every untyped fragment were an excitatory non-KC neuron, it would add ≈ 2–3% to the KC synapse count.

### 1.4 Other MBONs in MaleCNS (relevant to the α2sc comparison in `mbon11_input.md`)

| MBON | KC synapses per cell, MaleCNS | hemibrain |
|---|---|---|
| MBON18 (α2sc), R / L | 6,940 / 6,985 (8.0–8.2 per KC) | 10,888 |
| MBON14 (α3), 4 cells | 4,929–6,719 | 11,022–11,723 |
| MBON07 (α1), 4 cells | 5,085–6,694 | 12,777–12,873 |
| MBON01 (γ5β′2a), R / L | 20,439 / 20,449 | 26,853 |
| MBON11, R / L | 24,597 / 16,863 | 22,647 |

- MaleCNS's α-lobe MBONs carry about half the hemibrain's KC synapses; MBON11_R carries slightly more.
- MBON11_R / α2sc is 3.5 in MaleCNS against 2.1 in the hemibrain. Transfers between α2sc and MBON11 through synapse
  counts inherit this difference.

## 2. Charge per synapse

### 2.1 Yamada, Davidson & Hige 2024: charge per flash, re-measured (fig., approx.)

Setup is in `mbon11_input.md` §3.1: ex vivo; 1-ms 625-nm flash at 4.25 mW/mm²; Cs-aspartate + 10 mM QX-314; −60 mV;
1.5 Ca / 4 Mg. New details:
- Genotype: "20XUAS-SPARC2-S-Syn21-CsChrimson::tdTomato-3.1 … MB623C" with "nSyb-IVS-phiC31 attp18/w". So females
  (derived, two X chromosomes).
- "we kept the final crosses for experiments in the dark at 18 °C".
- Recording temperature: Not reported.

**Method.**
- Fig. 1B–D's representative control traces (black) were measured by pixel. Time comes from the 400-ms pulse interval
  (63 px, so 6.35 ms/px). Current comes from each panel's 30-pA bar (B 59 px, C 24 px, D 62 px).
- The first EPSC was integrated from onset to the second flash.
- Its remaining tail was extrapolated with a single exponential fitted to the last ≈ 160 ms before the second flash.

| Panel | First-EPSC peak | Time to peak | Half-width | Current at 400 ms (of peak) | Charge to 400 ms | Tail τ; tail charge | Single-flash charge | pC per pA of peak |
|---|---|---|---|---|---|---|---|---|
| B | 88.7 pA | 102 ms | 235 ms | 30.5 pA (0.34) | 20.2 pC | 256 ms; 7.8 pC | 28.0 pC | 0.32 |
| C | 109 pA | 118 ms | 249 ms | 35.0 pA (0.32) | 26.6 pC | 267 ms; 9.3 pC | 35.9 pC | 0.33 |
| D | 82.5 pA | 102 ms | 260 ms | 32.2 pA (0.39) | 19.7 pC | 333 ms; 10.7 pC | 30.5 pC | 0.37 |

- At the end of the traces, ≈ 1.5 s after the first flash (1.1 s after the second), the current is still 15–26 pA.
- (derived) The group-mean first EPSCs were 80, 117 and 86 pA (`mbon11_input.md` §3.1). × 0.32–0.37 pC/pA gives
  **≈ 26–43 pC per flash**, ≈ 32 pC at the pooled ≈ 95 pA.
- The earlier ≈ 19 pC (peak × half-width) leaves out the tail and is ≈ 1.7× low.

### 2.2 How many γ KCs a flash drives

**Yamada's figure is borrowed.**
- Yamada's "~3–7% of γ KCs" cites Isaacman-Beck et al. 2020. That paper counted SPARC2-S labelling in five other cell
  types, with a different effector:
  - "SPARC2-D-mCD8::GFP labeled ~48–51% of cells, SPARC2-I-mCD8::GFP labeled ~17–22% of cells, and SPARC2-S-mCD8::GFP
    labeled ~3–7% of cells (Figure 3p–r)".
  - The cell types were T4/T5, Mi1, GH146 PNs, LC20 and HS (n = 10 per genotype).
  - Some cell types differed. The Fig. 3 legend gives Mi1 vs T4T5 p = 0.0002, Mi1 vs PN p = 0.0003 and Mi1 vs LC20
    p = 0.03, without saying for which variant.
- For KCs the paper is qualitative only, with first-generation SPARC-GCaMP6f: "We observed similar results in Kenyon
  cells, lobula columnar neurons, and several columnar neurons in the optic lobe (Extended Data Figure 3 and data not
  shown)".

**Nobody has counted it in KCs.**
- Yamada counted no labelled cells. "The time course data of EPSCs and PPRs are shown in normalized values because the
  initial EPSC size was highly variable presumably because of our stochastic labeling strategy of KCs".
- Individual first EPSCs ran 57–185 pA (`mbon11_input.md` §3.1).
- Davidson et al. 2023 (SPARC-S-jGCaMP7f in KCs) imaged about a dozen labelled γ axons per field (fig., approx.). That is
  a field of view, not a census.

**Not checked:**
- Which γ KCs MB623C labels. Shuai et al. 2025 doesn't describe the line in its text, and Yamada calls it "γ KC-specific".
- Whether CsChrimson levels under SPARC2-S let every labelled KC fire.

**(derived) Arithmetic.**
- γ KCs per side: 701 in the hemibrain; 764 (R) and 793 (L) in MaleCNS by soma side. 3–7% of 700–790 is 21–55 KCs.
- Per labelled KC per flash: 26–43 pC ÷ 21–55 KCs = **0.47–2.0 pC** (0.58–1.52 at 32 pC).
- Per synapse per flash (21.5 synapses per γ KC on MBON11): **0.022–0.095 pC** (central 0.027–0.071).
- The model's 0.030 pC gives 0.645 pC per γ KC spike. That matches Yamada if each labelled KC fires 0.7–3.2 spikes per
  flash (central 0.9–2.4).

### 2.3 How many spikes a 1-ms flash evokes: not reported anywhere

A Europe PMC full-text search for KC + cell-attached + CsChrimson/Chrimson returns nothing. The anchors:

**CsChrimson kinetics** (Klapoetke et al. 2014, cultured mouse neurons).
- "Chrimson's slow tau-off of 21.4 ± 1.1 ms (n = 11 cells)".
- The addendum: "CsChrimson has the same spectral and kinetic properties as Chrimson".

**γ KC firing** (Hige 2015 Neuron Fig. S7, in vivo, K-aspartate; values in `hige2015_specificity.md` §7).
- Threshold current ≈ 11.8 pA.
- 18.9 spikes for 15 pA × 1 s.
- So ≈ 19 Hz at ≈ 1.3× rheobase.

**αβc KCs under CsChrimson** (Wong, Talbot & Miesenböck 2023; in vivo whole-cell, males 1–2 days old, 21–23 °C;
NP6024-GAL4; 25-ms pulses).
- "At the optical powers used in later behavioral analyses (0.01–0.20 mW mm−2), CsChrimson::GluR1 produced only small,
  subthreshold membrane potential changes of 1–4 mV at the soma of αβc KCs (Fig. 1f), equivalent to at most three
  odor-evoked synaptic quanta".
- Threshold: "far short of the ~10-mV depolarization needed to breach spike threshold".
- Yamada's flash energy (4.25 mW/mm² × 1 ms = 4.25 µJ/mm²) is ≈ 0.4× their strongest pulse (0.4 mW/mm² × 25 ms)
  (derived).

**Vrontou et al. 2021, Fig. S6** (CsChrimson-positive αβc KC; 0.11–0.80 mW/mm²).
- A ≈ 200-ms pulse gives a plateau with ≈ 9–16 small ripples (fig., approx.; counted by eye and by a peak detector).
- That is ≈ 45–80 Hz, if the ripples are the attenuated somatic spikes, which Vrontou measured at 1.95 ± 0.09 mV.

**(derived) Estimate.**
- A ≈ 20–60-ms suprathreshold window × ≈ 20–80 Hz gives **≈ 1–3 spikes per labelled KC per flash**, up to ≈ 5.
- But Yamada's EPSC peaks ≈ 100 ms after the flash and lasts more than 1 s. A short volley set by τ_off ≈ 21 ms can't
  explain that.
- Fly nicotinic synaptic currents are fast. Hafez et al. 2023 take a 0.44-ms time to peak conductance from Su &
  O'Dowd 2003 (cultured KCs). Turner 2008's in vivo KC EPSCs decay in 2.8 ms.
- So either KCs fire longer than this (q per spike lower), or release is asynchronous, or the clamp filters the current
  (q per spike unchanged).
- Yamada's PPR of 0.4–0.7 at 400 ms says the synapses are still depressed 400 ms after the flash.

### 2.4 α/β KCs onto MBON11: Yamada Fig. 8 example traces (fig., approx.)

Setup: MB008C + SPARC2-S. Scale bars are 300 ms and 100 pA (B 34 px, D 43 px, F 52 px). Time comes from the 400-ms
interval (≈ 10 ms/px). Integrated as in §2.1.

| Cell (panel) | First-EPSC peak | Time to peak | Current at 400 ms (of peak) | Single-flash charge | pC per pA |
|---|---|---|---|---|---|
| B | ≈ 324 pA | ≈ 90 ms | ≈ 79 pA (0.25) | ≈ 87 pC | 0.27 |
| D | ≈ 198 pA | ≈ 113 ms | ≈ 62 pA (0.31) | ≈ 59 pC | 0.30 |
| F | ≈ 211 pA | ≈ 80 ms | ≈ 57 pA (0.27) | ≈ 58 pC | 0.27 |

- These are representative traces, and no α/β group mean is reported. In Fig. 1 the γ representative traces sat
  within ≈ 10% of their group means.
- (derived) The α/β examples carry 2–3× the γ examples' charge (58–87 vs 28–36 pC). Yet α/β KCs make 6.5–9.3 synapses
  per KC on MBON11 (MaleCNS R / hemibrain), against 21.4 for γ.
- Assume MB008C covers ≈ 840–925 α/β KCs per side, 3–7% are labelled, and each fires once. Then the α/β synapse carries
  ≈ 0.1–0.5 pC per flash, ≈ 4–6× the γ value.
- Other possible causes:
  - α/β KCs are more excitable than γ (Inada: ≈ 9 vs 4 Hz at −30 mV), so may fire more spikes per flash.
  - The labelled counts may differ between the two lines.
  - The α/β synapses (in the peduncle) may be better clamped.
- Counterpoint (derived, very rough), Vrontou's αβc drive in vivo:
  - +38 Hz in MBON11 ÷ 0.35–0.47 Hz/pA (Wang 2026) ≈ 81–109 pA.
  - Spread over 1,333–1,538 αβc synapses (MaleCNS R / hemibrain), with every αβc KC at 10–50 Hz, that is q ≈ 0.001–0.008
    pC.
  - This holds unless few αβc KCs fired or rates were under 10 Hz. Neither the labelled count nor the light-driven rates
    were reported.

### 2.5 The unitary route: KC→MBON-α2sc in mecamylamine

The unitary EPSP is ≈ 0.25 mV (0.14–0.45) in 100 µM mecamylamine, 5 of 24 pairs monosynaptic (Hige 2015 Nature;
`mbon11_input.md` §5).

**How much 100 µM blocks.** No fly IC50 or dose–response curve exists. Su & O'Dowd 2003 and Gu & O'Dowd 2006 used
α-bungarotoxin, not mecamylamine. Single points:

| [MEC] | Effect | Source |
|---|---|---|
| 10 µM | γKC→MBON11 first EPSC 86 → 41 pA (≈ 52% block), PPR unchanged | Yamada 2024 Fig. 1D, ex vivo VC |
| 100 µM | KC-evoked M4/6 Ca²⁺ ≈ 0.05–0.35 of control, varying over trials; "significantly reduced … and partially recovered after washout" | Barnstedt 2016 Fig. S5K–L, n = 2 brains (fig., approx.) |
| 250 µM | KC-evoked M4/6 Ca²⁺ ≈ 0–0.05 of control | Barnstedt Fig. S5M–N, n = 2 (fig., approx.) |
| 250 µM | α/β KC → MBON-α1 EPSP "effectively blocked" | Takemura 2017, Fig. 7—fig. suppl. 1 |
| 500 µM (+TTX) | αβc-driven MBON depolarization leveled | Vrontou 2021 |

- (derived) A one-site block anchored at Yamada's 10 µM leaves 1/(1 + 100/10) ≈ 9% at 100 µM.
- Barnstedt's Ca²⁺ signal is nonlinear in current, so it gives only a rough 0.1–0.3.
- **Correction ≈ 3–11×**, so ≈ 0.8–2.8 mV per connected KC drug-free.
- Mecamylamine is an open-channel blocker, so its potency depends on use; the anchors come from different MBONs and
  preparations.

**Converting to charge** (Hafez et al. 2023's MBON-α3 model).
- Hafez's synapse: alpha conductance, τ_s = 0.44 ms, E = 8.9 mV (both from Su & O'Dowd), g_max = 1.5627 × 10⁻¹¹ S per
  contact.
- "The maximal conductance for the synapses was set at 1.5627*10-5 μS, the value determined to achieve the target MBON
  depolarization from monosynaptic KC innervation (Hige et al., 2015b)".
- Their result: "Activating a single KC leads to a voltage excursion at the soma with a mean of 0.37 mV" (13.47
  contacts).
- (derived) Charge per contact = g_max × τ_s × e × (E − V_rest) = 1.5627e-11 S × 0.44 ms × 2.718 × 64.5 mV ≈ 1.2 fC,
  so 16 fC per KC.
- Drug-free (× 3–11): **≈ 0.004–0.013 pC per synapse**, 2–8× below the model's 0.030.
- This holds for an α3-sized cell (model whole-cell C ≈ 35–45 pF; derived from 16 fC → 0.37 mV).
- A cell with more effective capacitance per EPSP would give more charge.
- The 5-of-24 connectivity may itself partly reflect the block: 100 µM raised the detection threshold 3–11× (inference).

### 2.6 Ex vivo vs in vivo

**Same:**
- External saline: 103 NaCl, 3 KCl, 1.5 CaCl₂, 4 MgCl₂, 26 NaHCO₃ … in both.
- Cs-aspartate + 10 mM QX-314 internal.
- Somatic voltage clamp at −60 mV (Hige: −60 or −70 mV).

**Not stated:** recording temperature (Hige 2015 Neuron; Yamada 2024).

**Space clamp.** No quantitative correction exists for MBON11.
- Yamada chose MBON11 because "the relatively thick and short primary neurite of this neuron allows for superior
  membrane voltage control (i.e. space clamp)". Series resistance was compensated to leave ≈ 5 MΩ.
- Hige discarded "cells that showed unclamped spikes during odor response".

**Why Yamada went ex vivo:**
- "light stimulation we used for optogenetic activation of KCs evoked an EPSC-like inward current in MBON-γ1pedc as well
  as many of the randomly selected neurons in flies without CsChrimson transgene … they almost disappeared in blind
  norpA mutants and were completely absent when we removed the retina".
- Ex vivo "also improved the recording condition by minimizing the spontaneous circuit activity".

**Internal solution doesn't change Hige's charge** (`hige2015_specificity.md` §2–3).
- Fig. 3 (Cs/QX-314, n = 5): OCT 248 ± 40 pC, MCH 273 ± 48.
- Fig. 4 (K-aspartate, n = 6): 244 ± 28 and 230 ± 27.

**Conclusion:** no measured basis for a several-fold in vivo/ex vivo difference per synapse. The unmeasured
flash-to-spike conversion (§2.3) matters more.

### 2.7 q estimates side by side (pC per synapse per spike)

| Route | q | Assumptions |
|---|---|---|
| Yamada γ flash, 1 spike per labelled KC | 0.022–0.095 (central 0.027–0.071) | 3–7% of 700–790 γ KCs; 21.5 synapses per KC |
| Yamada γ flash, 1–3 spikes | 0.007–0.095 | plus the derived spikes per flash |
| Yamada α/β examples, 1 spike | ≈ 0.1–0.5 | three example cells; MB008C coverage unknown |
| α2sc unitary × 3–11 (MEC), Hafez conversion | ≈ 0.004–0.013 | α3-sized cell; different MBON |
| Vrontou αβc, very rough | ≤ ≈ 0.001–0.008 | if all αβc fired at 10–50 Hz |
| Model now | 0.030 | |
| Needed with the model's KC activity | 0.28–0.33 | MBON11_R, 755–903 synapse-spikes |
| Needed with flies' estimated KC activity | 0.03–0.19 (best ≈ 0.08) | §3.7 |

## 3. KC activity at Hige's stimulus

### 3.1 Hige 2015 Neuron's own KC imaging

Other details are in `oct_mch_input.md` §9 and `hige2015_specificity.md` §7.
- **Preparation.**
  - GCaMP6f under R13F02-LexA (pan-KC), 82 ± 9 somata per fly, imaged at 4.8 Hz.
  - Imaging was "performed as described previously (Campbell et al., 2013; Honegger et al., 2011)". The plane's
    position and class composition: Not reported.
- **Criterion.** Peak ΔF/F in 0.5–4.5 s above 2.33 SD on at least half the trials.
- **Counts.** 53 OCT-responsive and 49 MCH-responsive cells from 5 flies.
  - Fig. 2F legend: "Only cells that significantly responded to the odor in either pre- or post-pairing recordings were
    included".
  - (derived) 12.9% and 12.0% are therefore a union over two 4-trial sessions, and overstate a single session.
- **No-light controls.** "n = 32 from 2 flies" for OCT and MCH together. That is ≈ 9.8% per odor if n counts
  cell–odor pairs (derived; 82 cells per fly).
- **Inference only.** If the imaged posterior somata resemble Turner's patched ones (27 of 71 were α′/β′, against 17.5%
  of KCs in the hemibrain), α′/β′ cells are over-represented.

### 3.2 Single-cell data by class

| Source | Preparation and stimulus | γ | α/β | α′/β′ |
|---|---|---|---|---|
| Turner, Bazhenov & Laurent 2008 | in vivo WC; 1:100 in oil × 1:10 in air; 0.5 s; > 3.5 SD on ≥ half of 6 trials | 1 of 15 cells; ≈ 2.3% of odor–cell pairs (fig., approx.) | ≈ 4.1% of pairs; 2.2 ± 1.2 spikes | ≈ 10.7% of pairs; 4.9 ± 3.0 spikes |
| Murthy, Fiete & Laurent 2008 | in vivo WC; 1/100; 1 s; ≥ 1 spike on ≥ 3 trials (loose) | 0 of 20 pairs (3 cells) (fig., approx.) | GFP− α/β 39 of 93 (42%); αβc 44 of 224 (20%) (fig., approx.) | 20 of 23 (87%; 3 cells) (fig., approx.) |
| Vogt et al. 2016 | in vivo WC; saturated vapour 1:20 (5%); 1 L/min; 1 s; OCT, MCH, 2-heptanone, isoamyl acetate, cider vinegar | γ-d: 0 of 60 spiking, 1 excitation, 42 inhibition only, 17 none | 3 of 55 spiking (5.5%), 20 excitation, 21 inhibition only, 11 none | – |
| Bielopolski et al. 2019 | in vivo GCaMP6f; OCT, MCH at 10⁻¹; pixel sparseness | γ-only somata SP ≈ 0.96–0.97 (fig., approx.) | pan-KC (OK107) SP ≈ 0.89–0.93 (fig., approx.) | – |
| Inada et al. 2017 | lobe GCaMP5 (OK107); ethyl butyrate; 1 s; n = 17 flies | ΔF/F ≈ 0.40 (10⁻¹), 0.27 (10⁻³) | 0.57, 0.34 | 0.67, 0.48 |

Notes on the table:
- **Turner.** Per-class probabilities come from Fig. 2D's tuning histograms, counting the 0–10% bin as 0 and using bin
  midpoints. They reproduce the stated 6%.
  - Weighted by hemibrain class counts, the population value is ≈ 4.5% (derived).
  - Turner's γ: "Only 1 of the 15 γ KCs we tested with this odor set (and 1 of the 23 total γ KCs recorded at all odor
    concentrations) showed a spiking response".
- **Murthy.** Cells were classified by Fig. 3A marker colour; this reproduces the stated 18.6% and 49% within 2 points.
  - Same data, locust-style criterion: αβc 6.7% (stated).
  - (derived) Dividing by that 2.8× loose-to-strict ratio gives α/β ≈ 15% and α′/β′ ≈ 31%.
- **Vogt.** Counts are printed on the Fig. 2G pie charts. n = 11 α/β cells (MB008B) and 12 γ-d cells (MB607B), 3 flies.
  - Text: "Stimulating flies with 5 different odors did not lead to excitatory responses of the γd neurons; olfactory
    stimulation rather evoked slow inhibitory responses, implying the existence of feedforward inhibition through other
    odor-responsive KC populations (Figure 2E,G)."
- **Bielopolski.**
  - γ-only genotype: "mb247-GAL4 > GCaMP6f, R44E04-LexA > GAL80". Pan-KC (Fig. 4B) includes α′/β′; γ-only is Fig. 4H.
  - Delivery: "Odors at 10−1 dilution were delivered … Flow rates at the exit port of the odor tube were 0.5 or 0.8
    l/min".
  - (derived) Taking 1 − SP as the active fraction gives γ ≈ 3–4% vs pan-KC ≈ 7–11%. This assumes binary pixels.
- **Inada.** Values are from Fig. 8A, pixel-read on a 0–1 axis. The ≈ 0.7 (β, γ) and ≈ 1.4 (β′) in
  `kc_classes_and_apl.md` §3.2 are APL neurites (Fig. 6E), as filed there, not KCs.
- **(derived) Taken together,** γ responds at ≈ 0.4–0.8 of the α/β rate: Turner 0.56, Inada 0.7–0.8 in bulk Ca²⁺,
  Bielopolski ≈ 0.3–0.5 of pan-KC.
- **The model's ratio** is 1.67/4.09 = 0.41, the low end.

### 3.3 γ-d: odor-inhibited, visually driven

- **Physiology.** Vogt 2016: no odor excitation; 42 of 60 odor–cell pairs inhibited only. Light drove spikes in 5 of 24
  and excitation in 9 of 24 light–cell pairs (Fig. 2G).
- **Anatomy.** Li et al. 2020 (hemibrain): "visual projection neurons (VPNs) from the medulla (ME) and the lobula (LO)
  are the predominant inputs to the γd KCs".
- **Connectome.** MaleCNS agrees (§1.2).
- **α/β-p** are odor-inhibited at the lobe level (Perisse 2013; `kc_classes_and_apl.md`).

### 3.4 Spikes per response

- **Turner's means** (α/β 2.2, α′/β′ 4.9) are the only per-class counts.
- **Turner's one γ responder** fired ≈ 5–7 spikes per response (derived from Fig. 2E's class PSTH integral divided by
  2.3%). One cell, very uncertain.
- **Murthy Fig. 2C** (αβc, 1/100, 1 s; fig., approx.):
  - Onset clusters of 2–4 spikes within ≈ 0.1 s.
  - Some bursts of 6–10 or 8–12 spikes within 0.15–0.6 s.
  - Some off responses (`kc_integration.md` §5).
- **Honegger's "typically five to 10"** cites Turner, whose means are 2.2 and 4.9. In full: "This is likely because,
  although KCs fire a small number of spikes, typically five to 10, evoked spike rates are high and spontaneous firing
  is extremely rare (Turner et al., 2008)".

### 3.5 Concentration and pulse length

**Turner's stimulus vs Hige's** (derived).
- Turner's 1:1000 is 1% v/v in paraffin oil × 1:10 in air. For an ideal solution that is ≈ 0.2–0.3% of saturated
  vapour, more if the alcohols deviate positively in oil.
- So Hige's 2% is ≈ 1–10× stronger. No PID comparison exists.

**Honegger 2011** (OK107 > GCaMP3, 1:100, 1 s).
- "On any given odor trial, ∼20% of KCs may be active". The example is 121 KCs to one isoamyl acetate presentation.
- Fig. 6 per-trial fractions (banana, isoamyl acetate; fig., approx.):
  - ≈ 0.03–0.04 with an empty vial.
  - ≈ 0.06–0.12 at 1%, ≈ 0.08–0.13 at 2%, ≈ 0.13–0.18 at 10% of saturation.
  - The concentration effect appeared only when blocks ran from high to low.
- (derived) 1% → 2% adds ≈ 10–40% more responders. 10× adds ≈ 1.1–3×, typically 1.5–2×.
- "the very first odor presentation of the experiment typically evoked the broadest response, regardless of the
  concentration of odor".
- OCT ≈ 10%, MCH ≈ 7% at 1% (Fig. 7A; `oct_mch_input.md` §9).

**Murthy** (same cell and odor at two concentrations; fig., approx.).
- αβc: 9 of 39 pairs respond at 1/1000 vs 18 of 39 at 1/100.
- 8 of 16 vs 5 of 16 between 1/100 and 1/10.

**Pulse length:** no Drosophila KC data. Turner's and Murthy's responses are mostly onset-dominated, so 0.5 → 1 s
probably adds few spikes in onset cells and some off responses (inference).

### 3.6 Lateral axonal suppression among γ KCs

Manoim et al. 2022: "KCs have numerous axo-axonic connections mediated by the muscarinic type-B receptor (mAChR-B)". In
full: "we show that these axo-axonic connections suppress both odor-evoked calcium responses and dopamine-evoked cAMP
signals in neighboring KCs".
- Fig. 3 title: "mAChR-B knockdown increases odor responses only in γ KC axons".
- KC→KC synapses are about half of each KC's input in MaleCNS (51–58%, derived).
- This suppression lowers flies' γ output. It cannot explain extra input to MBON11.

### 3.7 Flies at Hige's stimulus vs the model, onto MBON11_R (derived)

| Class (MBON11_R synapses) | Fly estimate: responders × spikes (range) | Basis | Model (OCT) |
|---|---|---|---|
| γ-main + γ-s (14,582) | 3.5% × 3.5 (2–6% × 2–6) | Turner 2.3% at 1:1000 × 1.2–2 for concentration; γ ≈ 0.4–0.8 × α/β; one γ responder 5–7 spikes; α/β 2.2 | 1.67% × 1.01 |
| α/β s, m, c (7,228) | 6% × 2.5 (4–8% × 2–3) | Turner 4.1%; Vogt 5.5% at 5%; concentration factor | 4.09% × 1.68 |
| α′/β′ (336) | 20% × 5 (11–30% × 5) | Turner 10.7%; Murthy | 3.45% × 1.09 |
| γ-d (2,086), α/β-p (365) | 0 (inhibited) | Vogt; Perisse 2013 | – |
| **Synapse-spikes, 0–1.4 s** | **≈ 3,200 (1,300–7,500)** | | **≈ 755 (responders) to 903 (all above-rest spikes)** |
| Charge at q = 0.030 | ≈ 96 pC (40–225) | | 23–27 pC |
| q for 250 pC | ≈ 0.08 (0.033–0.19) | | 0.28–0.33 |

- **Imaging bound.** Pan-KC imaging near Hige's stimulus gives 10–13% responders (Hige, union of 8 trials) and 7–10%
  (Honegger, OCT/MCH at 1%). These cap the uniform-response case: 12.5% × 3 spikes is ≈ 8,300 synapse-spikes, 250 pC at
  0.030. But single-cell electrophysiology puts γ and α/β well below 12.5% (§3.2).
- **Left cell.** MBON11_L (fewer synapses) gets ≈ 2,180 synapse-spikes in the best case.

## 4. Hige 2015 Neuron's odor EPSC as a KC measurement

**Values** (`hige2015_specificity.md` §2–3).
- Fig. 3D (Cs/QX-314, n = 5): OCT 248 ± 40 pC (cells ≈ 152–395), MCH 273 ± 48 (≈ 206–464).
- Fig. 4H (K-aspartate, unclamped spike currents low-pass filtered at 100 Hz, n = 6): OCT 244 ± 28 (≈ 160–359), MCH
  230 ± 27 (≈ 158–336).
- Time course (`mbon11_input.md` §2.5): onset ≈ 0.18 s after the odor bar, peak ≈ 380–430 pA, ≈ 170 pA sustained from
  0.6 to 1.0 s, back to baseline ≈ 1.5 s.

**Spikes against charge, same cells** (Fig. 4E/H group means; derived).

| | OCT pre | OCT post | MCH pre | MCH post |
|---|---|---|---|---|
| Charge (pC) | 244 | 62 | 230 | 150 |
| Spikes | 116 | 17 | 110 | 68.5 |

- Linear fit: spikes ≈ 0.545 × Q − 15.5 (threshold ≈ 28 pC). Residuals −1.4, −1.2, +0.3, +2.3.
- The ratio before pairing is 0.48 spikes/pC. The model's MBON11 gave 0.26–0.41 (odor_probe35).

**Was any of it non-KC?**
- No KC block was done in Hige's paper. Europe PMC full-text searches found no paper that silenced KC output while
  recording an MBON's odor response. The search terms were MBON + odor response + shibire, Kir2.1, tetanus toxin or
  hydroxyurea + Kenyon.
- The evidence that KC→MBON transmission is nicotinic and monosynaptic comes from optogenetics:
  - Takemura 2017: TTX-resistant, MEC-sensitive.
  - Barnstedt 2016: nAChR RNAi in M4/6 reduces odor responses partly.
  - Vrontou 2021: TTX + MEC levels the response.
- **Dopamine.**
  - Takemura found a direct, non-nicotinic PAM-α1 → MBON-α1 depolarization: "(E) MBON responses to DAN photostimulation
    in the presence of TTX and MEC … were strongly diminished by the application of the dopamine receptor antagonist SCH
    23390 (100 μM; magenta)".
  - For MBON11, Wang et al. 2026: "we expressed CsChrimson in PPL101 and specifically stimulated the γ1-pedc
    compartments using one-photon or two-photon photostimulation while imaging MBON11, but detected minimal effects
    (Supplementary Fig. 5f)".
- **Connectome:** §1.3.

**(derived) What the time course asks of KCs.**
- At q = 0.08 the ≈ 400-pA peak needs ≈ 5,000 synapse-spikes/s and the ≈ 170-pA plateau ≈ 2,100/s.
- At q = 0.030 it needs 13,300 and 5,700/s.

## 5. MBON drive against the number of active KCs

**No experiment varies a counted number of active KCs.** The nearest:
- **Hafez et al. 2023 (model of MBON-α3, calibrated as in §2.5).** Table 3:
  - 38, 50 and 63 simultaneously active KCs give 12.14, 15.24 and 18.26 mV at the soma.
  - The response is nearly linear in active synapses: regression slopes 0.0203, 0.0185 and 0.0166 mV per synapse.
  - "The neuron is firmly in a small-signal operation mode".
- **Yamada 2024.** First EPSCs varied 57–185 pA across cells, which the authors attribute to stochastic labelling.
- **Population optogenetics without counts.**
  - Vrontou 2021: αβc → MBON11 +38 Hz.
  - Takemura 2017: all α/β → MBON-α1 +11 mV.
- **Woitkuhn et al. 2020** (paywalled; supplement only).
  - Genotype: pan-KC GMR13F02-Gal4 > 20XUAS-CsChrimson, MBON labelled by GMR12G04-lexA, the MBON-γ1pedc driver Hige
    used.
  - Its control EPSC would be a non-sparse KC→MBON11 calibration point. The abstract and later summaries give no
    amplitudes.
  - Piao & Sigrist 2022, summarizing it: KC-to-MBON γ1pedc>α/β synapses "operate with a high SV release probability".

---

## For the model

### A. The budget

- Charge onto MBON11 in 0–1.4 s = Σ over classes of (synapses onto MBON11 × responders × spikes per responder) × q.
- Hige's ≈ 250 pC per cell is the target. Compare the right MBON11, or expect ≈ 0.7× on the left (§1.1).
- Today the model has ≈ 755–903 synapse-spikes × 0.030 pC.

### B. Recalibration, in order of support

1. **KC activity at Hige's stimulus (2%, 1 s)**, per class (§3.7):
   - γ-main ≈ 3.5% (2–6%) with ≈ 3.5 spikes (2–6).
   - α/β s/m/c ≈ 6% (4–8%) with ≈ 2.5 (2–3).
   - α′/β′ ≈ 20% (11–30%) with ≈ 5.
   - γ-d and α/β-p inhibited only.
   - Keep Turner's 1:1000 / 0.5-s values as the low anchor: γ 2.3%, α/β 4.1%, α′/β′ 10.7%; 2.2 and 4.9 spikes.
   - Target ≈ 3,200 synapse-spikes on MBON11_R, ≈ 3.5–4× today.
2. **Effective q ≈ 0.07–0.08 pC per synapse per spike** (2.3–2.7×).
   - This is the upper end of Yamada's γ range. It holds if ≈ 19–21 γ KCs (≈ 2.5–3%) fire once per flash.
   - It is an average over the response. With Yamada's depression (PPR 0.4–0.7 at 400 ms; odor_probe34) the first-spike
     q would be higher.
3. **If step 2 fails the flash test (C1),** put the extra charge on α/β synapses (§2.4): γ ≈ 0.03–0.05, α/β ≈ 0.1–0.2.
   - With the best-estimate activity that gives ≈ 54–89 pC from γ and ≈ 110–220 pC from α/β (derived).
4. **Not supported:**
   - q alone (0.28–0.33).
   - KC activity alone at 0.030 (γ-main 12–15% × 3–4 spikes).
   - Non-KC excitation.
   - An in vivo/ex vivo factor.

### C. Tests

1. **Yamada's flash, in the model.**
   - Drive a random 3% and 7% of γ KCs with one brief pulse, MBON11 not spiking. Record KC spikes per flash and MBON11's
     synaptic current.
   - Fly values: 26–43 pC per flash; time to peak ≈ 100 ms; ≈ 0.3 of peak at 400 ms; PPR 0.4–0.7.
   - Repeat for α/β KCs: the examples gave 58–87 pC, about 2× γ.
   - With uniform q and equal labelled fractions and spikes, the model predicts α/β:γ ≈ 0.3–0.4 (derived from synapses
     per KC). Flies' examples give ≈ 2.
2. **Hige's EPSC.** 245–275 pC (cells 150–460); peak ≈ 400 pA at ≈ 0.2–0.3 s after onset; ≈ 170 pA sustained.
3. **Transfer.** Spikes ≈ 0.545 × Q − 15.5, in Hige's conditions: held near −60 mV, spontaneous rate subtracted.
4. **KC classes.** At the Turner protocol, γ/α/β/α′β′ ≈ 2.3/4.1/10.7%. The model's α′/β′ (3.45%, 1.09 spikes) is low on
   both counts, but matters little for MBON11 (1.4% of its KC synapses).

### D. Caveats

- **Per-class activity at Hige's exact stimulus.** No class-resolved single-cell data exist for OCT/MCH at 2% and 1 s.
  §3.7 interpolates from Turner (1:1000), Murthy (1/100), Vogt (5%) and imaging.
- **Spikes per γ response.** These rest on one Turner cell and analogy with α/β.
- **SPARC2-S in KCs.** The labelled fraction is unmeasured, and so are spikes per flash. Both set q.
- **MaleCNS's left MBON11.** It is under-connected relative to the right and the hemibrain.

---

## Sources

- Yamada, Davidson & Hige 2024, J Physiol 602:2019, [PMC11068490](https://pmc.ncbi.nlm.nih.gov/articles/PMC11068490/).
  Methods, Figs. 1 and 8 (pixel measurements here).
- Isaacman-Beck, Paik, Wienecke et al. 2020, Nat Neurosci 23:1168, "SPARC enables genetic manipulation of precise
  proportions of cells", [PMC7939234](https://pmc.ncbi.nlm.nih.gov/articles/PMC7939234/).
- Shuai et al. 2025, eLife 13:RP94168, "Driver lines for studying associative learning in Drosophila",
  [PMC11778931](https://pmc.ncbi.nlm.nih.gov/articles/PMC11778931/). Text checked for MB623C; not described.
- Hige, Aso, Modi, Rubin & Turner 2015, Neuron 88:985, [PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/).
  Experimental Procedures, Fig. 2 legend, Fig. S7.
- Hige, Aso, Rubin & Turner 2015, Nature 526:258, [PMC4860018](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860018/).
- Klapoetke et al. 2014, Nat Methods 11:338, [PMC3943671](https://pmc.ncbi.nlm.nih.gov/articles/PMC3943671/); addendum
  [PMC4920138](https://pmc.ncbi.nlm.nih.gov/articles/PMC4920138/).
- Wong, Talbot & Miesenböck 2023, Nat Commun 14:2770, "Transient photocurrents in a subthreshold evidence accumulator
  accelerate perceptual decisions", [PMC10182991](https://pmc.ncbi.nlm.nih.gov/articles/PMC10182991/).
- Vrontou, Groschner, Szydlowski et al. 2021, Curr Biol 31:4911,
  [PMC8612741](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/). Fig. 1H, Fig. S6, STAR Methods.
- Barnstedt et al. 2016, Neuron 89:1237, [PMC4819445](https://pmc.ncbi.nlm.nih.gov/articles/PMC4819445/).
  Supplement Fig. S5.
- Takemura et al. 2017, eLife 6:e26975, [PMC5550281](https://pmc.ncbi.nlm.nih.gov/articles/PMC5550281/).
  Fig. 7—figure supplement 1 and DAN figure legend.
- Hafez, Escribano, Ziegler, Hirtz, Niebur & Pielage 2023, eLife 12:e77578,
  [PMC10069864](https://pmc.ncbi.nlm.nih.gov/articles/PMC10069864/). Table 2, Table 3, Methods.
- Su & O'Dowd 2003, J Neurosci 23:9246, [PMC6740836](https://pmc.ncbi.nlm.nih.gov/articles/PMC6740836/).
- Gu & O'Dowd 2006, J Neurosci 26:265, [PMC6674319](https://pmc.ncbi.nlm.nih.gov/articles/PMC6674319/).
- Wang, Lv, Gao et al. 2026, Nat Commun, [PMC13624267](https://pmc.ncbi.nlm.nih.gov/articles/PMC13624267/).
- Woitkuhn et al. 2020, J Neurogenet 34:106, doi 10.1080/01677063.2019.1710146 (paywalled). Supplement:
  doi 10.6084/m9.figshare.11719554.
- Piao & Sigrist 2022, Front Synaptic Neurosci 13:798204, "(M)Unc13s in Active Zone Diversity: A Drosophila
  Perspective", [PMC8762327](https://pmc.ncbi.nlm.nih.gov/articles/PMC8762327/).
- Turner, Bazhenov & Laurent 2008, J Neurophysiol 99:734,
  [PDF](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf). Fig. 2D/E.
- Murthy, Fiete & Laurent 2008, Neuron 59:1009, [PMC2654402](https://pmc.ncbi.nlm.nih.gov/articles/PMC2654402/).
  Figs. 2C, 3A.
- Vogt, Aso, Hige et al. 2016, eLife 5:e14009, [PMC4884080](https://pmc.ncbi.nlm.nih.gov/articles/PMC4884080/).
  Fig. 2, Methods.
- Bielopolski et al. 2019, eLife 8:e48264, [PMC6641838](https://pmc.ncbi.nlm.nih.gov/articles/PMC6641838/). Fig. 4,
  Methods.
- Inada, Tsuchimoto & Kazama 2017, Neuron 95:357,
  [PDF](https://kazamalab.riken.jp/pdf/Neuron_Inada_2017.pdf). Fig. 8A.
- Honegger, Campbell & Turner 2011, J Neurosci 31:11772,
  [PMC3180869](https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/). Figs. 2, 6, 7.
- Groschner et al. 2018, Cell 173:894, [PMC5947940](https://pmc.ncbi.nlm.nih.gov/articles/PMC5947940/).
- Li et al. 2020, eLife 9:e62576, [PMC7909955](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909955/).
- Manoim, Davidson, Weiss, Hige & Parnas 2022, Curr Biol 32:4438,
  [PMC9613607](https://pmc.ncbi.nlm.nih.gov/articles/PMC9613607/).
- Davidson, Kaushik & Hige 2023, eNeuro, [PMC10616905](https://pmc.ncbi.nlm.nih.gov/articles/PMC10616905/).
- Perisse et al. 2013, Neuron 79:945, [PMC3765960](https://pmc.ncbi.nlm.nih.gov/articles/PMC3765960/).
- MaleCNS v1.0 annotations, transmitters and connectome weights (`~/fly-data/raw/*male-cns-v1.0*`).
- Hemibrain v1.2 traced adjacencies,
  `https://storage.googleapis.com/hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz`.
- Model values: `experiments/odor_probe44.json` (odors, mbon11_input, kc_timing); definitions in
  `experiments/odor_probe7.py` and `experiments/odor_probe33.py`.
