# APL→Kenyon cell inhibition: time course, receptors, reversal potential and location

Read 2026-10-11. This file adds to `kc_classes_and_apl.md` §3.2, §3.3 and §5. Sizes, wiring counts and the first timing
notes are there and are not repeated. Rdl receptor kinetics in culture are in
`../Embodied fly connectome simulation/neuron_synapse_biophysics.md` §3.

Conventions:
- (vec.): extracted from the vector paths of the published PDF figure (Inada 2017), so exact for the plotted trace. Still
  one example cell, as published.
- (fig.): read off a raster figure, by eye or by pixel colour. Good to about ±10–20%.
- derived: my own arithmetic or a simple simulation (scratch scripts, not in the repo).
- [other insect], [larval]: not adult Drosophila.
- Times run from light or valve onset unless stated. Negative mV is hyperpolarization from baseline.

## Summary

1. **No one has recorded APL→KC IPSCs, unitary IPSPs or a KC GABA reversal potential.** Every time course is a somatic
   current-clamp response to optogenetic drive.
   - Direct APL drive (Inada 2017 Fig. 5B; about 1 s of light; ex vivo; one KC; vec.): onset ≈ 70 ms; 10–90% rise
     0.14–0.56 s; half at 0.27 s; plateau ≈ −10 mV.
   - After the light: half-recovery in 0.32 s, then a tail (−2.2 mV at +1 s, −1.3 mV at +2 s). Two exponentials fit
     the decay: 0.26 s (−7.6 mV) and 2.2 s (−3.2 mV).
2. **GABA-A comes first, GABA-B later.**
   - In that cell the picrotoxin-sensitive part starts at ≈ 50–75 ms, is half-up at ≈ 0.22 s, and falls by half
     ≈ 0.25–0.3 s after light-off (derived from vec. traces).
   - The CGP54626-sensitive part starts at ≈ 0.3–0.35 s, is half-up at ≈ 0.75 s, is still growing at 1 s, and decays
     with τ ≈ 0.4 s (derived).
   - Means (n = 10, vec.): picrotoxin leaves 0.61 ± 0.09 of the response; picrotoxin + CGP leaves 0.26 ± 0.07.
   - In vivo, KC-driven inhibition is almost all picrotoxin-sensitive after 8–500 ms of drive, and ≈ 70% after 2 s
     (Vrontou 2021 Fig. 7B, fig.).
3. **"Several hundred ms" is Inada's phrase, about PN drive. It is not from Vrontou.**
   - With 1 s of Mz19-PN drive (ex vivo), inhibition of unconnected KCs starts ≈ 0.5 s after light onset. It bottoms
     out at ≈ −6 mV 0.2–0.7 s after light-off. In a connected KC the trough (−10.4 mV) comes 0.65 s after light-off
     (vec.).
   - In Vrontou's KC→APL→KC test (200 ms light, in vivo) the IPSP starts ≈ 80–100 ms after light onset. It peaks at
     −7.7 mV at ≈ 0.31 s, ≈ 0.1 s after the driving KCs peak. It decays with τ ≈ 0.39 s and leaves ≈ 1.7 mV for more
     than 2 s (fig.). It survives TTX.
4. **No experiment separates APL's integration from slow receptors.** The kinetics point to APL's own dynamics for the
   main part (derived inference).
   - Under direct APL drive even the GABA-A part takes ≈ 0.2 s to rise and ≈ 0.3 s to fall.
   - Rdl currents decay in ≈ 5 ms in culture, and the recorded KCs' membranes take ≈ 0.1 s.
   - GABA-B adds a later, slower part that grows with the length of the drive.
   - APL calcium follows KC calcium closely: the half-rise times differ by −0.09 to +0.17 s, lobe by lobe (Inada Figs
     6D and 7B, vec.; different indicators).
5. **Every KC recording set E_Cl with its pipette.**
   - Pipettes held ≈ 1 mM Cl⁻ (Inada, Vrontou, Groschner, Chen) or ≈ 0.2 mM (Turner). So E_Cl was ≈ −121 to −122 mV,
     or ≈ −162 mV for Turner (derived).
   - The only adult fly central neuron I found with a transporter-set E_GABA is the l-LNv clock neuron: −65.5 mV (95%
     CI −68.3 to −62.7, n = 7), ≈ 10 mV below its −55.4 mV rest (Eick 2022 preprint).
   - KCC in mushroom body neurons keeps GABA inhibitory (Hekmat-Scafe 2010). KC rest in vivo is ≈ −46 mV at break-in,
     "likely to be more hyperpolarized" (Groschner 2018).
   - GABA-B is presumably a K⁺ conductance: E_K ≈ −85 to −99 mV in 3–5 mM K⁺ saline (derived).
6. **APL inhibits dendrites and axons, and by synapse count mostly axons.**
   - Hemibrain: ≈ 49 APL→KC synapses per KC; ≈ 27% in the calyx, 11% in the peduncle, 62% in the lobes (derived from
     Amin 2020 Fig. 8—figure supplement 3D).
   - Rdl is in the calyx and lobes. GABA-B receptor label is in the calyces but not the lobes (Enell 2007).
   - GABA or APL activation in the calyx silences KC Ca²⁺ signals along the whole axon. In a lobe it cuts axonal Ca²⁺
     locally (Amin 2020).
   - Shunting is assumed (Amin), not measured. The larval APL releases only in the calyx.
7. **For brainfly** (derived):
   - Replace the 5 ms decay with ≈ 0.3 s (0.25–0.4 s). Add a ≈ 50 ms rise or delay, and optionally a 20–30% tail of
     1.5–3 s.
   - Use an effective reversal ≈ 10–20 mV below rest for odor-length drive.
   - Fit strength to the conductance in Inada's recording conditions (ceiling ≈ 0.2–0.7 × KC leak), not to 11 mV at a
     physiological reversal. A quiet KC at APL's ceiling would then sit only ≈ 2–7 mV below rest (2–10 mV over the full
     range), if the pipette's chloride reached the synapses in those recordings.

---

## 1. Time course of APL-evoked inhibition in Kenyon cells

### 1.1 Direct APL drive: Inada, Tsuchimoto & Kazama 2017, Neuron 95:357

Source: [PDF](https://kazamalab.riken.jp/pdf/Neuron_Inada_2017.pdf), doi 10.1016/j.neuron.2017.06.039.

Protocol:
- Ex vivo explant at 25 °C. CsChrimson in APL, amber LED (M590L3). "LED light was pulsated at 80 Hz".
- Fig. 5B light lasts ≈ 1.0 s: the bar is 28.5 pt against a 14.27 pt bar for 500 ms (vec.). Its intensity is not
  given. Fig. 5D's saturation curve uses 0–6 µW.
- KC whole-cell recording. KCs "were held at around [−]60 mV by injecting a hyperpolarizing current". "Voltages were
  uncorrected for the liquid junction potential."
- Pipette: "140 KOH, 140 aspartic acid, 10 HEPES, 1 EGTA, 4 MgATP, 0.5 Na3GTP, 1 KCl".
- Drugs: picrotoxin and CGP54626 "dissolved in the external saline at 5 [µM] and 10 [µM]" (the µ is lost in the PDF
  text).
- Legend: "KC responses to optogenetic activation of APL neurons with or without the presence of GABA receptor
  antagonists. Each trace is an average of three trials." Also: "KCs receive inhibition from APL neurons through both
  GABAA and GABAB receptors (n = 10 KCs)."

Fig. 5B, one KC (vec.). Onset is the first time the smoothed trace stays 3 SD below baseline; for a small response this
can come after the 10% point. Percentages are of each trace's own peak. "Off" is light-off.

| Trace | Onset | 10% | 50% | 90% | Peak | off +0.25 s | +0.5 s | +1 s | +2 s | Decay |
|---|---|---|---|---|---|---|---|---|---|---|
| Saline | 67 ms | 138 ms | 269 ms | 558 ms | −9.9 mV at 1.02 s | −6.2 | −3.7 | −2.2 | −1.3 | half 0.32 s after peak; 2-exp 0.26 s (−7.6 mV) + 2.2 s (−3.2 mV) |
| Picrotoxin (GABA-B + remainder) | 260 ms | 251 ms | 462 ms | 926 ms | −5.3 mV at off | −3.5 | −2.3 | −0.6 | −0.5 | τ ≈ 0.5 s |
| Picrotoxin + CGP (remainder) | ≈ 200 ms | 208 ms | 418 ms | 882 ms | −3.0 mV at 0.94 s | −2.0 | −1.4 | −1.4 | −0.2 | τ ≈ 0.9 s |
| Saline − picrotoxin (GABA-A, derived) | 50–76 ms | — | 216 ms | 435 ms | −6.1 mV at 0.69 s; −4.5 at off | −2.7 | −1.3 | ≈ −1.6 | ≈ −0.8 | half ≈ 0.25–0.3 s after off |
| Picrotoxin − (picrotoxin + CGP) (GABA-B, derived) | 300–350 ms | 304 ms | 751 ms | 978 ms | −2.5 mV at off | −1.5 | −0.9 | ≈ 0 | — | τ ≈ 0.4 s |

Fig. 5C means (n = 10, vec.):
- Saline 1. Picrotoxin 0.61 ± 0.09. Picrotoxin + CGP 0.26 ± 0.07. The error bars are as drawn; the legend does not say
  whether they are SEM or SD.
- So GABA-A carries ≈ 39%, GABA-B ≈ 35%, and the drug-resistant remainder ≈ 26% (derived; `kc_classes_and_apl.md` had
  40/35/25 by eye).

Notes:
- The GABA-A part sags from −6.1 to −4.5 mV during the light. Rdl desensitization or APL adaptation could explain this;
  neither was tested.
- The KC membrane filters all of these traces. In the same paper, KCs repolarize after 500 ms current steps with
  τ ≈ 0.1 s: in the αβ and γ examples of Fig. 4B the voltage falls by half 55–65 ms after the step (vec., derived).
- The IPSP's 0.26–0.35 s decay is about three times slower than that. So the inhibitory conductance outlasts the light
  by ≈ 0.2–0.3 s (derived; §2).

### 1.2 Kenyon cell→APL→Kenyon cell drive: Vrontou et al. 2021, Curr Biol 31:4911

Source: [PMC8612741](https://pmc.ncbi.nlm.nih.gov/articles/PMC8612741/). Supplement (Fig. S6) via
[Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8612741/supplementaryFiles).

Protocol:
- In vivo, 21–23 °C. CsChrimson in a random half of the αβc KCs (whole neuroblast clones) and GFP in the rest. The
  recordings are from GFP-positive αβc KCs.
- 630 nm LED, "11–80 mW cm-2".
- Pipette: "140 mM potassium aspartate, 1 mM KCl". No holding current is mentioned.
- Drugs: TTX at 1 µM. Picrotoxin at "10 μM as standard; up to 250 μM in some cases".
- Fig. 7C legend: "Example voltage responses of a CD8::GFP-positive αβc KC during a 500-ms depolarizing current step
  (left) and a 200-ms light pulse (right), before and after the addition of TTX".

Fig. 7C right, one KC (fig., pixel-digitized; 10 mV = 64.5 px, 1 s = 43 px):

| Condition | Onset | 10% | 50% | Peak | Back to 50% | Decay τ (1-exp + offset) | Residual |
|---|---|---|---|---|---|---|---|
| No toxin | ≈ 80–100 ms | ≈ 100 ms | ≈ 170 ms | −7.7 mV at ≈ 0.31 s | 0.45 s after peak | 0.39 s | ≈ −1.7 mV at 1.5–2.8 s after light-off |
| TTX | ≈ 100 ms | ≈ 125 ms | ≈ 195 ms | −9.3 mV at ≈ 0.36 s | 0.56 s after peak | 0.52 s | ≈ −2 mV |

- A depolarizing blip of under 1 mV comes 30–60 ms after light onset in both traces.
- The pre-light baseline is only ≈ 0.14 s long, so the residual is uncertain.
- The same cell's current step (Fig. 7C left, TTX trace) rises to 63% in ≈ 106 ms and falls to 37% ≈ 90 ms after the
  step (fig.). So τ_m ≈ 0.1 s, about a quarter of the IPSP's decay τ.
- These values refine `kc_classes_and_apl.md` §3.3, which read "peak ≈ −10 mV within ≈ 0.2 s". The peak is at
  ≈ 0.31 s, and −7.7 mV in this cell.

The driving KCs (Fig. S6, a different cell, ≈ 200 ms light; fig.):
- +11.5 mV within 43 ms. Peak ≈ +13 mV at ≈ 0.1 s.
- Half-decay ≈ 85 ms after light-off. ≈ +0.9 mV (≈ 8% of the light-off value) at +0.5 s.
- An undershoot of ≈ −1 mV at 0.8–1.1 s after light-off.
- At +0.5 s the undriven KC's IPSP is still ≈ 56% of its peak (derived; different cells). So the inhibition outlasts its
  drive by a factor of about three.
- During 2 s of light the driven KC sags from ≈ +13 to ≈ +8 mV.

Fig. 7B, peak hyperpolarization (fig.; n = 7–8, n = 5 for the TTX pair):

| Light | 8 ms | 50 ms | 500 ms | 2000 ms |
|---|---|---|---|---|
| No toxin | −2.1 mV | −5.8 mV | −7.3 mV | −7.7 mV |
| Picrotoxin | ≈ 0 | ≈ 0 | −0.6 mV | −2.3 mV |
| Picrotoxin-sensitive share (derived) | ≈ 100% | ≈ 100% | ≈ 92% | ≈ 70% |

- TTX: −8.1 → −7.3 mV. "TTX had no effect (p = 0.6250; Wilcoxon test)."
- Quote: "the light-induced hyperpolarizations of CsChrimson-negative αβc KCs persisted unabated when action potentials
  were blocked with TTX".
- The KC-driven inhibition is therefore mostly GABA-A, unlike Inada's direct APL drive (39% GABA-A). The protocols
  differ: drive strength and length, in vivo against ex vivo, and 10 µM against 5 µM picrotoxin.

### 1.3 Projection neuron drive: Inada 2017 Fig. 3 (vec.)

Protocol:
- ReaChR in "13 PNs using Mz19-Gal4" (DA1, VA1d and DC3 PNs).
- 470 nm LED pulsed at 80 Hz for 1 s. "blue light was sufficient to make the PNs expressing ReaChR fire at 200 Hz".
- Each trace is a mean of 3 trials; ex vivo.

| KC | Excitation | Crosses baseline | Inhibition trough | Half-recovery | Back at baseline |
|---|---|---|---|---|---|
| 3B, connected, 11 µW | +9.3 mV at 0.28 s; +5.9 at 0.5 s; +0.9 at 0.9 s | 0.98 s | −10.4 mV at 1.65 s | ≈ 2.45 s | ≈ 3.2 s |
| 3B, connected, 1.9 µW | +4.3 mV at 0.48 s | 1.12 s | −4.1 mV at 1.55 s | ≈ 2.2 s | ≈ 2.5 s |
| 3D, unconnected, 6.5 µW | none | — | −6.0 to −6.3 mV at 1.2–1.7 s | ≈ 2.35 s | ≈ 2.8 s |

- In 3D the inhibition starts ≈ 0.5 s after light onset: −1.8 mV at 0.7 s, −4.7 mV at 1.0 s.
- Results: "When these PNs were optogenetically stimulated with higher intensity of light, excitatory KC responses were
  followed by more salient, slow inhibition".
- Discussion: "Inhibition followed excitation by several hundred ms and were often strong enough to override the
  initial depolarization (Figures 3B and S3B)."

### 1.4 One Kenyon cell's own spikes: Inada 2017 Fig. 4B (vec.)

- Protocol: a 500 ms current step of 5–40 pA. The offset response is measured 500 ms after the step.
- The example α′β′ KC bottoms out at ≈ −21 mV, ≈ 0.8 s after the step ends. It is half recovered ≈ 2.3 s after the step
  ends (−10.6 mV) and still ≈ −3 mV at 4.2 s.
- The αβ and γ examples reach only ≈ −1 to −1.7 mV.
- This is much slower than direct APL drive, and part of it may be intrinsic.
  - Picrotoxin + CGP cut the α′β′ slope by about 60% (Fig. 4D), and Arch in APL by about 75% (Fig. 4E) (fig.).
  - The authors: "The offset response does not reflect intrinsically generated slow afterhyperpolarization as it was
    significantly reduced by GABA receptor antagonists".

### 1.5 Receptor kinetics, and what is not reported

- Cultured pupal KCs: "Fast IPSCs are mediated by picrotoxin-sensitive chloride conducting GABA receptors. The miniature
  IPSCs also have a rapid rate of rise and decay" (Su & O'Dowd 2003, J Neurosci 23:9246,
  [PMC6740836](https://pmc.ncbi.nlm.nih.gov/articles/PMC6740836/)). Only the abstract was read; the numbers are in the
  scanned full text.
- Cultured embryonic neurons: Rdl mIPSCs decay with τ = 5.4 ± 0.3 ms and rise in 0.88 ms (Lee, Su & O'Dowd 2003; see
  `neuron_synapse_biophysics.md` §3).
- Not found anywhere:
  - APL→KC IPSCs in voltage clamp, and unitary APL→KC IPSPs.
  - Spontaneous IPSPs in KCs. Turner 2008: background PSPs were "abundant and mostly depolarizing", and "we find no
    evidence for a periodic voltage reset by IPSPs". With Turner's ≈ −162 mV E_Cl, discrete IPSPs would have been large
    (derived).
  - GABA-B kinetics in KCs, apart from Inada's drug subtraction.
  - Any larval APL→KC electrophysiology.

## 2. Where the "several hundred ms" comes from

Source and protocol:
- The phrase is in Inada et al.'s Discussion, about Figures 3B and S3B. That is PN drive: 1 s of 80 Hz light on 13
  Mz19 PNs firing at about 200 Hz, in an ex vivo explant at 25 °C.
- `kc_integration.md` quotes it correctly. `kc_classes_and_apl.md` summary item 6 attaches it to Vrontou's lateral
  inhibition, which it does not describe.
- In that protocol the delay includes:
  - PN→KC excitation;
  - the recruitment of more and more KCs;
  - KC→APL and APL→KC transmission;
  - the KC's membrane.
- A connected KC's own excitation also masks the inhibition until the light ends (§1.3).
- Vrontou 2021 measured a different loop, KC→APL→KC, with 8–2000 ms of light in vivo.
  - Its IPSP lags the driving KCs by ≈ 50–80 ms at onset and ≈ 0.1 s at peak (§1.2; fig.).
  - Vrontou's text gives no lag value.

APL's own integration, or slow receptors? Neither paper tests this directly. The evidence, with my reasoning (derived):
1. **Direct APL drive** skips KC recruitment. Even so, the GABA-A part takes ≈ 50–75 ms to start and ≈ 0.22 s to reach
   half. It falls by half ≈ 0.25–0.3 s after the light (§1.1).
2. **Rdl is fast.** Its mIPSCs decay in ≈ 5 ms in culture. A ≈ 0.3 s GABA-A IPSP therefore needs GABA release that
   rises and falls slowly. That points to APL's own voltage or Ca²⁺ dynamics, or slow GABA clearance (spillover).
   - Opsin kinetics are not reported in these papers. I assume CsChrimson closes within tens of ms.
3. **The KC membrane contributes, but too little.**
   - Its τ_m is ≈ 0.1 s in both preparations (Inada Fig. 4B steps; Vrontou Fig. 7C left). The IPSP decays with
     0.26–0.39 s.
   - A linear simulation (KC τ_m 0.1 s, first-order conductance) matches Inada's landmarks with a conductance
     τ ≈ 0.3 s, and Vrontou's with ≈ 0.3–0.4 s.
   - A 5 ms conductance gives a half-rise of 0.07–0.09 s and a half-decay of 0.07–0.10 s, three to four times too fast.
4. **GABA-B is slower and later.**
   - The CGP-sensitive part starts at ≈ 0.3 s and is half-up at ≈ 0.75 s (§1.1).
   - In vivo its share grows with the drive. Picrotoxin removes almost all inhibition after ≤ 0.5 s of KC drive, but
     leaves ≈ 30% after 2 s (§1.2).
   - So for odor-length KC drive, slow receptors are a small part of the delay. For strong, long drive they add a slow
     tail.
5. **APL itself lags little.**
   - APL calcium's half-rise falls within −0.09 to +0.17 s of the KCs' (§4).
   - Most of the lag between KC activity and KC inhibition therefore comes after APL's calcium signal: release, GABA
     clearance and the KC membrane.
6. **APL is non-spiking and leaky** (Chen et al. 2026, Curr Biol 36:1633,
   [PMC13075853](https://pmc.ncbi.nlm.nih.gov/articles/PMC13075853/)).
   - "APL neurons are non-spiking and exhibit graded responses to somatic current injection". R_in is "∼120 MΩ".
   - After strong depolarization APL shows an SK-mediated AHP. In sleep-deprived flies "The decay time constant of the
     enhanced AHP is 491.1 ± 72.17 ms". It is smaller after normal sleep.
   - APL's membrane time constant was measured, but the value is only in Fig. S2, which I could not retrieve.
7. **Transmission is graded.**
   - TTX leaves Vrontou's KC→APL→KC inhibition unchanged, so KC spikes are not needed.
   - Inada's single-KC feedback does need spikes: it "was abolished by the addition of tetrodotoxin".

Conclusion (derived): the measured lag and duration come mostly from APL's own integration and graded release, plus KC
membrane filtering. GABA-B adds a delayed component when the drive is long or strong. This is an inference from
kinetics, not a direct measurement.

## 3. Reversal potentials and Kenyon cell resting potential

### 3.1 Pipette-set values: every published KC recording

| Study | Preparation | Pipette Cl⁻ | Saline Cl⁻ | E_Cl (derived) | Membrane potential |
|---|---|---|---|---|---|
| Inada 2017 | ex vivo, 25 °C | 1 mM (140 K-aspartate, 1 KCl) | 117 mM | −122 mV | held "around [−]60 mV", not LJP-corrected |
| Vrontou 2021 | in vivo, 21–23 °C | 1 mM (140 K-aspartate, 1 KCl) | 117 mM | −121 mV | no holding current stated |
| Groschner 2018 | in vivo | 1 mM (140 K-aspartate, 1 KCl) | 117 mM | −121 mV | rest at break-in, LJP-corrected |
| Turner 2008 | in vivo | ≈ 0.2 mM (125 K-aspartate, 0.1 CaCl₂) | 117 mM | ≈ −162 mV | held at −58 mV |
| Chen 2026 | ex vivo | 1 mM (140 K-gluconate, 1 KCl) | 117 mM | −121 mV | ramps from −60 ± 5 mV |

- E_K (derived): −98 to −99 mV with 3 mM K⁺ saline and a 141 mM K⁺ pipette; −85 mV with 5 mM K⁺ saline.
- Junction potential: if K-aspartate's is 10–15 mV, Inada's −60 mV is ≈ −70 to −75 mV true (derived). Eick computed
  13 mV for a similar K-gluconate solution.
- A constraint (derived):
  - Inada saw a picrotoxin-sensitive hyperpolarization of ≈ 4 mV in KCs held near −70 to −75 mV (true).
  - So during those recordings E_GABA-A at the APL synapses was below ≈ −75 mV.
  - Either the pipette's chloride reached the synapses, or KCs keep [Cl⁻]i at about 5 mM or less.

### 3.2 Physiological chloride in fly central neurons

**l-LNv clock neurons: Eick et al. 2022.** Curr Biol 32:1420, doi 10.1016/j.cub.2022.01.056. Read as the bioRxiv
preprint, [10.1101/2021.09.14.460201](https://www.biorxiv.org/content/10.1101/2021.09.14.460201v1).
- Table S2, E_GABA (mean, 95% CI, n):
  - control −65.5 mV (−68.3, −62.7; n = 7);
  - kcc knockout −49.4 mV (n = 8);
  - KCC overexpression −78.2 mV (n = 9);
  - NKCC knockout −73.2 mV (n = 5);
  - qsm knockout −48.3 mV (n = 4).
- Method: ex vivo whole brain at 20–22 °C. GABA was puffed "in the ipsilateral medulla", onto distal neurites.
  - "GABA reversal potentials (EGABA) were calculated from the IV-curves".
  - "The liquid junction potential was calculated as 13 mV and subtracted from all the membrane voltages."
- Their pipette held 17 mM NaCl, so ≈ 17–21 mM Cl⁻ and E_Cl ≈ −43 to −48 mV (derived).
  - E_GABA still moved with transporter genotype. So the transporters, not the pipette, set chloride at the distal GABA
    sites.
  - The wild-type value implies [Cl⁻]i ≈ 8.6 mM there (derived, assuming a pure Cl⁻ conductance).
- Rest: "average wild type resting membrane potential (-55.4 mV)". So E_GABA sat ≈ 10 mV below rest.

**sLNv clock neurons: Schellinger et al. 2022.** Curr Biol 32:1429,
[PMC8972083](https://pmc.ncbi.nlm.nih.gov/articles/PMC8972083/).
- ClopHensor imaging shows [Cl⁻]i changing over the day and lower in Ncc69 mutants.
- Absolute values are only in Fig. S1, which I did not retrieve.

**Mushroom body neurons extrude chloride, but no KC E_Cl has been measured.**
- Hekmat-Scafe et al. 2010, Genetics 184:171, [PMC2815914](https://pmc.ncbi.nlm.nih.gov/articles/PMC2815914/):
  "kcc(DHS1) seizure sensitivity in MB neurons acts via a weakening of chemical synaptic inhibition by GABAergic
  transmission and suggest that this is due to disruption of intracellular Cl(-) gradients in MB neurons."
- Hekmat-Scafe et al. 2006, J Neurosci, [PMC6675325](https://pmc.ncbi.nlm.nih.gov/articles/PMC6675325/): "Drosophila kcc
  protein is widely expressed in brain neuropil, and its level rises with developmental age."

**With intact chloride, GABA and APL still inhibit KCs in imaging.**
- Local GABA puffs and APL activation reduce KC Ca²⁺ (Amin 2020).
- Rdl knockdown raises KC odor responses (Liu, Krause & Davis 2007, Neuron 56:1090,
  [PMC2709803](https://pmc.ncbi.nlm.nih.gov/articles/PMC2709803/)).
- This bounds E_GABA-A below KC spike threshold (≈ −38 mV in αβc), but not below rest.

**GABA-B effector: not identified in KCs.**
- In insulin-producing cells: "Knockdown of irk3, possibly part of a G protein-activated inwardly rectifying K(+)
  channel that may link to GBRs, phenocopies GBR knockdown" (Enell et al. 2010, PLoS One 5:e15780,
  [PMC3012717](https://pmc.ncbi.nlm.nih.gov/articles/PMC3012717/)).
- I assume E_GABA-B ≈ E_K.

**Not accessed:** Wilson & Laurent 2005's supplement on PN GABA reversal under two internal solutions (the server
returned 403).

### 3.3 Kenyon cell resting potential (details in `kc_classes_and_apl.md` §1)

- In vivo αβc: ≈ −46 mV at break-in, LJP-corrected. Groschner 2018 says it is "likely to be more hyperpolarized" because
  of seal leak.
- Turner held KCs at −58 mV. Chen required rest below −50 mV ex vivo. Vrontou accepted cells with rest "below –30 mV".
- Derived: with R_in ≈ 10 GΩ, a 40–50 GΩ seal would make a −58 mV cell read ≈ −47 mV. So a true rest of ≈ −55 to
  −60 mV is plausible.

### 3.4 Bounds (derived)

Reversals relative to rest:
- **GABA-A.** Suppose KCs resemble l-LNvs, with [Cl⁻]i ≈ 5–10 mM and so E_Cl ≈ −63 to −81 mV. Then E_GABA-A sits
  ≈ 5–25 mV below a −55 to −60 mV rest. Near rest it is mostly shunting; it hyperpolarizes more as the KC depolarizes.
- **GABA-B:** ≈ 25–45 mV below rest.
- **Lumped conductance.** At 70–100% GABA-A (odor-length drive; §1.2), the effective reversal is ≈ 10–20 mV below
  rest. With 30% GABA-B (2 s drive) it is ≈ 15–25 mV below.

What the 10–12 mV ceiling implies:
- Inada measured it with driving forces of ≈ 50 mV (GABA-A) and ≈ 25 mV (GABA-B), assuming a true holding potential of
  −73 mV.
- That needs a ceiling conductance of ≈ 0.2–0.7 × the KC's resting conductance: g/g_L = 11 / (D − 11), with driving
  forces D = 26–62 mV (GABA-B to GABA-A, with or without the junction-potential correction).
- With physiological driving forces of 10–25 mV, the same conductance hyperpolarizes a quiet KC by only ≈ 2–10 mV:
  ΔV = g·D / (g_L + g). For the likeliest ceiling of 0.3–0.4 × leak it is ≈ 2–7 mV.

Vrontou's mean of −7.5 mV:
- If the pipette set the chloride, the driving force was ≈ 65 mV, assuming a baseline near −55 mV. Then −7.5 mV
  corresponds to g/g_L ≈ 0.13.
- With a physiological driving force of 10–25 mV, that conductance would give only ≈ 1–3 mV.

The main unknown:
- These numbers assume the pipette's chloride reached the APL synapses.
- If it did not, as at the l-LNvs' distal sites, the published mV values are already physiological and the
  conductances are larger.

## 4. APL's own odor response time course

- **No voltage recording of APL during odors exists in flies.** Chen 2026's recordings are ex vivo current injections.

**Inada 2017 Fig. 6D against Fig. 7B (vec.).**
- Both use the same lab, the same 1 s ethyl butyrate at 10⁻¹, and in vivo two-photon imaging. Times run from the onset
  of the odor bar.
- APL: GCaMP6s, mean of 4 trials. KCs: GCaMP5 in all KCs, mean of 10 trials.

| Signal | 20% | 50% | 90% | Peak |
|---|---|---|---|---|
| APL, β′ lobe | 0.63 s | 0.76 s | 1.11 s | 1.07 ΔF/F at 1.28 s |
| APL, β lobe | 0.72 s | 0.76 s | 1.07 s | 0.77 at 1.15 s |
| APL, γ lobe | 0.72 s | 0.85 s | 1.11 s | 0.79 at 1.37 s |
| KC α′β′ | 0.52 s | 0.71 s | 1.07 s | 0.34 at 1.17 s |
| KC αβ | 0.66 s | 0.85 s | 1.07 s | 0.16 at 1.26 s |
| KC γ | 0.49 s | 0.68 s | 1.07 s | 0.10 at 1.21 s |

- Lobe by lobe, APL's half-rise differs from the matching KCs' by +0.05 s (β′ against α′β′), −0.09 s (β against αβ)
  and +0.17 s (γ against γ). The peaks differ by 0.11–0.16 s, in both directions. Both peak near the odor's end.
- GCaMP6s rises more slowly than GCaMP5, so the true lag is probably shorter (indicator caveat).
- After the odor, APL falls to about half within ≈ 0.25 s of its peak. It holds ≈ 0.4–0.6 ΔF/F until ≈ 2 s and is near
  baseline by ≈ 2.7–3.2 s.
- The α′β′ KC signal drops below baseline from ≈ 2.5 s, to ≈ −0.1 ΔF/F (about 30% of its peak), and stays there until at
  least 5 s. This is an observation only; nobody tested whether it is post-odor inhibition.
- Inada's Fig. 7D onset times (α′β′ ≈ 210, αβ ≈ 340, γ ≈ 370 ms) run from an "onset of the odor" arrow, not from the
  valve command (`kc_classes_and_apl.md` §2.2).

**Prisco et al. 2021 Fig. 2C and 2F.** eLife 10:e74172, [PMC8741211](https://pmc.ncbi.nlm.nih.gov/articles/PMC8741211/).
GCaMP6m in the calyx; 5 s odors at 1:100; one fly; fig.
- 4-methylcyclohexanol: rises ≈ 0.3 s after valve onset and peaks at ≈ 22% ΔF/F at ≈ 0.9 s. It falls to ≈ 5% by ≈ 4 s
  while the odor is still on, then dips to ≈ −5% about 5 s after offset.
- 3-octanol: peaks at ≈ 62% at ≈ 1.1 s. It is ≈ 45% at 2.4 s and ≈ 30% at 3.7 s, and back to baseline ≈ 2 s after
  offset.
- So calyx APL activity is phasic-tonic: it peaks within ≈ 1 s, then declines during a sustained odor.

**Other papers give no usable timing.**
- Lin et al. 2014, Nat Neurosci 17:559, [PMC4000970](https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/): APL's odor
  response needs KC output. "odor-evoked GCaMP3 responses were blocked at the restrictive temperature."
- Bergmann et al. 2026, J Physiol 604:3005, [PMC13039246](https://pmc.ncbi.nlm.nih.gov/articles/PMC13039246/):
  amplitudes only ("APL = k*KC"). KCs carry jRGECO1a and APL carries GCaMP6f, so their timing cannot be compared.
- Liu & Davis 2009, Nat Neurosci 12:53, [PMC2680707](https://pmc.ncbi.nlm.nih.gov/articles/PMC2680707/): G-CaMP1.6 and
  synapto-pHluorin responses during 3 s odors and shocks in the horizontal lobes. The indicator is too slow for timing.
- [larval] Masuda-Nakagawa et al. 2014, Front Neural Circuits 8:35,
  [PMC3988396](https://pmc.ncbi.nlm.nih.gov/articles/PMC3988396/), GCaMP3: "we could not distinguish any temporal
  difference in activity between larval APL dendrites in the MB lobes, and its pre-synaptic terminals in the calyx".
  The larval APL's odor responses also need KC output.

## 5. Where APL inhibits Kenyon cells, and whether it shunts

### 5.1 Anatomy

Source: Amin et al. 2020, eLife 9:e56954, [PMC7541083](https://pmc.ncbi.nlm.nih.gov/articles/PMC7541083/).
- Hemibrain v1.1: "All 1927 traced Kenyon cells in this volume form reciprocal synapses with APL (49.6 ± 17.9 APL-KC and
  52.6 ± 13.4 KC-APL synapses per KC; mean ± s.d.) in both their dendrites and axons".
- "APL-KC synapses are polyadic (a single presynaptic density on APL contacts multiple KCs)."

APL→KC synapses per KC by compartment (Amin Fig. 8—figure supplement 3D; pixel-digitized, derived):

| Class (n KCs) | Calyx | Peduncle | Lobes | Total | Calyx share |
|---|---|---|---|---|---|
| γ-m (590) | 23.3 | 7.6 | 35.6 | 66.5 | 35% |
| γ-t (8) | 22.0 | 8.1 | 31.0 | 61.1 | 36% |
| γ-d (99) | 13.9 | 5.4 | 28.1 | 47.5 | 29% |
| αβ-p (60) | 2.4 | 14.9 | 30.5 | 47.8 | 5% |
| αβ-s (223) | 8.7 | 6.7 | 29.7 | 45.0 | 19% |
| αβ-m (354) | 9.1 | 4.4 | 19.7 | 33.2 | 27% |
| αβ-c (252) | 9.3 | 2.2 | 10.2 | 21.7 | 43% |
| α′β′-ap1 (91) | 4.0 | ≈ 0.5 | ≈ 49 | 53.8 | 8% |
| α′β′-ap2 (127) | 10.5 | 2.3 | 47.3 | 60.0 | 17% |
| α′β′-m (119) | 9.9 | 4.7 | 45.3 | 59.9 | 17% |

- Weighted by class size: ≈ 49 per KC, ≈ 27% in the calyx, 11% in the peduncle, 62% in the lobes (derived).
- The αβc calyx count (≈ 9) matches Vrontou's "inhibited by APL via 10.0 reciprocal synapses".

In the calyx (Prisco 2021):
- Most APL→KC synapses are on claws: "While most are localized on dendritic claws, some connections along dendritic
  branches could be seen as well."
- "The fraction of APL to KCαβ synapses localized on KC claws was lower than in other KC types."
- APL also synapses onto PN boutons: "84% ± 2%" of each PN's APL synapses are on boutons. So presynaptic inhibition of
  PNs is possible.

[larval]:
- The larval APL "is highly polarized, with overwhelmingly dendritic processes in the MB lobes and pre-synaptic
  processes in the calyx" (Masuda-Nakagawa 2014).
- Amin 2020: "The larval APL has pre-synapses only in the calyx, while adult APL has pre-synapses everywhere".

### 5.2 Receptors

- Rdl: APL's innervation "matched precisely the expression pattern of the GABAA receptor RDL in the mushroom bodies"
  (Liu & Davis 2009). That covers the calyx, peduncle and lobes. Amin: "the GABAA receptor Rdl is expressed in both"
  dendrites and axons (citing Liu et al. 2007).
- GABA-B (Enell et al. 2007, J Comp Neurol 505:18, [PubMed 17729251](https://pubmed.ncbi.nlm.nih.gov/17729251/)): "Most
  abundant labeling was seen in the mushroom body calyces ... However, the mushroom body lobes displayed RDL-IR but not
  GABA(B)R-IR material".
  - The calyx label could be on PN boutons or on KC dendrites.
  - Amin: KCs express GABABR1 and GABABR2, "although their subcellular localization is unknown".

### 5.3 Function

- **Calyx:** local APL activation or GABA in the calyx silences KCs along their whole axons. Amin's interpretation:
  "inhibition from APL shunts away the resulting depolarization and stops the Kenyon cells from spiking ... These
  results show that sufficiently strong local inhibition in Kenyon cell dendrites can silence Kenyon cells throughout
  their axons."
- **Lobes:** local APL activation in a lobe reduces KC Ca²⁺ there. The effect is stronger near the start of the axon
  than at the lobe tip. Amin:
  - "GABA should act on Kenyon cells by suppressing depolarization through shunting inhibition in both dendrites and
    axons".
  - "More likely, local inhibition might particularly suppress Ca2+ influx rather than depolarization, perhaps by acting
    through GABAB receptors".
- Lin 2014, Supplementary Fig. 3 title: "APL inhibits Kenyon cells in all lobes".
- **Locality:** "Some KCs were almost not hyperpolarized at all, suggesting that the inhibition is effective locally"
  (Inada).
- **Normalization:** APL normalizes claw responses. "APL acts as an input strength normalizer on MGs in the MB calyx"
  (Prisco). With APL blocked, claw responses follow PN bouton strength.
- **Shunting is not measured.** No study reports a KC input-resistance change, or a reversal potential, during APL
  activation. If E_GABA-A sits ≈ 5–25 mV below rest (§3.4), APL inhibition is partly shunting at rest and more
  hyperpolarizing during excitation (derived).

## For brainfly

What the model does now (read from the docstrings of `mb_calibration3.py` and `odor_apl_conductance_check.py`):
- APL is a graded unit, with τ_m 20 ms by default.
- Its synapses onto KCs are a conductance in the KCs' slow current. That current is set to the fast current's 5 ms
  decay.
- The conductance reverses 15, 20 or 30 mV below rest. It is scaled so that APL's ceiling holds a quiet KC 11 mV down.
- Model inhibition peaks 80–110 ms after odor onset.

### 1. Time course (derived from §1–§2)

- **Decay:** ≈ 0.3 s (range 0.25–0.4 s) for the APL→KC conductance, if APL's unit stays fast.
  - 5 ms is 50–80 times too short.
  - With the model's 20 ms KC and APL membranes, a 5 ms conductance gives an IPSP half-rise of ≈ 0.04 s, and a
    half-decay of ≈ 0.04 s after the drive ends (derived). Flies show ≈ 0.17–0.27 s and ≈ 0.32–0.45 s, four to eleven
    times slower.
- **Rise:** a ≈ 50 ms first-order rise, or a 50 ms delay. A simulation with KC τ_m 20 ms, a 50 ms rise and a
  0.3–0.35 s decay gives the values below. APL's own 20 ms membrane would add about 20 ms to each.

  | Drive | Landmark | Model | Fly |
  |---|---|---|---|
  | 1 s step (Inada 5B) | 10% | 0.09 s | 0.14 s |
  | | 50% | 0.27–0.31 s | 0.27 s |
  | | half-decay after offset | 0.28–0.35 s | 0.32 s |
  | 200 ms drive (Vrontou 7C) | 50% | 0.16 s | 0.17 s |
  | | peak | 0.30 s | 0.31 s |
  | | half-decay after peak | 0.27–0.33 s | 0.45 s |

- **Tail:** optionally a second component carrying 20–30%, with τ ≈ 1.5–3 s. This matches Inada's 2.2 s component and
  Vrontou's ≈ 1.7 mV residual. It stands for GABA-B and the drug-resistant remainder.
- **Two components, if the model allows:**
  - GABA-A-like: 70–100% of the conductance for drives of 0.5 s or less; decay 0.25–0.3 s; reversal 5–25 mV below rest.
  - GABA-B-like: 0–35%, growing with drive length; onset delay ≈ 0.3 s; rise ≈ 0.4 s; decay ≈ 0.4 s; reversal at E_K,
    ≈ 25–45 mV below rest.
- **Implementation:** `hybrid.py` says a slow edge "carries tau_slow / 5 ms times the charge". So scale the APL→KC
  weights by 5 ms / τ to keep the same steady conductance at APL's ceiling.
- **Expected consequences:**
  - Inhibition peaks ≈ 0.2–0.3 s after KC excitation starts, instead of ≈ 50–80 ms.
  - It trims late spikes more than first spikes.
  - It outlasts the odor by ≈ 0.5–1 s.

### 2. Reversal

- For odor-length drive (GABA-A-dominated), a lumped conductance at ≈ 10–20 mV below rest is best supported.
- The current −15 and −20 mV settings are inside that range.
- −30 mV needs a large GABA-B share, or a KC [Cl⁻]i at about 5 mM or less.

### 3. Strength

The 10–12 mV ceiling holds only under the pipette's chloride. There are two ways to use it.
- **Simulate Inada's recording.**
  - Set E_GABA-A = −122 mV and E_GABA-B = −99 mV.
  - Hold the KC near −70 to −75 mV (or −60 mV, if no LJP correction) with a constant current.
  - Scale APL's ceiling to give 10–12 mV there. Then run odors with physiological reversals.
  - The equivalent target is a ceiling conductance of ≈ 0.2–0.7 × KC leak, most likely ≈ 0.3–0.4.
- **The current calibration** (11 mV at −15, −20 and −30 mV) implies 2.75, 1.2 and 0.58 × leak.
  - That is 1–10 times too much conductance if the pipette set the synaptic chloride.
  - It is right only if the synapses kept physiological chloride during the recordings.
- **Expected result:** a quiet KC at rest sits ≈ 2–7 mV down at APL's ceiling (2–10 mV over the full range).

### 4. Location

- In the connectome 62% of APL→KC synapses are axonal (lobes) and 27% are in the calyx. In a point neuron they all act
  on spike initiation.
- If the model gets a KC output (release) stage, the axonal synapses would better act on output, for example as a
  GABA-B-like cut in release. The dendritic ones would act on the membrane potential.

### 5. Tests

Each test is a model run with the same protocol as the fly experiment.
1. **Inada Fig. 5B.** Drive model APL to its ceiling for 1 s and record a quiet KC under the §3 recording conditions.
   - Targets: onset ≈ 70 ms; half-rise ≈ 0.27 s; plateau ≈ −10 mV; half-recovery ≈ 0.32 s after offset; ≈ −2 mV left
     at +1 s.
   - With GABA-A removed: ≈ 0.6 of the response, starting at ≈ 0.25 s.
2. **Vrontou Fig. 7.** Drive half of the αβc KCs for 8, 50, 500 and 2000 ms, and record an undriven αβc KC under pipette
   conditions.
   - Peaks: −2.1, −5.8, −7.3 and −7.7 mV, nearly all GABA-A for drives of 0.5 s or less.
   - 200 ms drive: onset 80–100 ms; peak at ≈ 0.31 s; decay τ ≈ 0.4 s.
   - It must work without KC spikes (graded KC→APL transmission).
3. **Inada Fig. 3D.** Give the Mz19 PNs (DA1, VA1d, DC3) 1 s of ≈ 200 Hz drive.
   - Unconnected KCs: no excitation; inhibition from ≈ 0.5 s; a trough of ≈ −6 mV at 1.2–1.7 s; back by ≈ 2.8 s. About
     half of them get almost none, because the inhibition is local.
   - Connected KC: +9 mV at 0.28 s; crosses baseline at ≈ 1 s; trough of −10 mV at 1.65 s.
4. **Imaging level.** Model APL release should be half-up within ≈ 0.1–0.2 s of KC population activity. During a 5 s
   odor it should fall to 20–50% of its peak (Prisco).
5. **Fly experiments that would settle the reversal.**
   - Gramicidin perforated-patch KC recordings with APL drive, at several holding potentials.
   - Or ClopHensor/SuperClomeleon chloride imaging in KCs, calibrated as in Schellinger 2022.
