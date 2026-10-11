# PN responses without ORN input in DA1, DL3, DA2, DA3 and other glomeruli: electrophysiology vs Badel's imaging

Compiled 2026-10-10 from full texts, supplements, supplementary tables and figure pixels. Purpose: decide whether
Badel et al. 2016's strong projection-neuron (PN) calcium responses to 3-octanol (OCT), 4-methylcyclohexanol (MCH) and
other general odors in glomeruli whose receptor neurons (ORNs) do not respond (DA1, DL3, DA2, DA3; secondarily VA5,
VM7v, DC3, DM3, DL5, VA6, VM3) are PN firing that brainfly is missing (lateral excitation), an imaging artifact, or ORN
input below detection.

Related notes (not repeated here): [lateral_excitation.md](lateral_excitation.md) (eLN physiology and coupling, Olsen
2007, Yaksi & Wilson 2010, Huang 2010, Kazama 2011, Das 2017, Shimizu & Stopfer 2017, MaleCNS eLN candidates),
[oct_mch_concentration.md](oct_mch_concentration.md) §2.1 (Badel vs Barth) and §5.7 (imaging nonlinearity),
[oct_mch_input.md](oct_mch_input.md) §8 (Badel's and Barth's PN data), [mch_oct_equalization.md](mch_oct_equalization.md)
§4-5 (calibration search, NP225 and GH146 coverage).

## Summary

1. **Whole-cell recordings find no firing in DA1, DL3 or DA2 PNs to general odors, including the odors that give
   107-362% ΔF/F in Badel's imaging.** DA1 (Schlief & Wilson 2007; 18 odors at 1:100): every non-cVA odor ≤ ≈4.4
   spikes/s vs ≈32 to cVA (fig., approx.); ethyl butyrate (Badel 144%) gives nothing. DA1, DL3, DA2 (Seki 2017 /
   Stensmyr 2012; 16 odors at 10⁻²): DA1 −1.7 to 0 spikes/s (n = 3), DL3 −1 to 6 (n = 1), DA2 −1.5 to 1.5 (n = 2;
   geosmin 91.5), where Badel has DA1 ethyl butyrate 144, 2,3-butanedione 116, 1-octen-3-ol 107%; DL3 180 and 138%;
   DA2 362, 256, 166, benzaldehyde 185, acetophenone 175%. OCT and MCH were never tested on these PNs (Not reported).
2. **Lateral excitation reaches DA1 PNs but stays subthreshold.** Deafferented lateral-lineage PNs including DA1
   depolarize 5.7-6.2 mV, abolished in shakB² (Shimizu & Stopfer 2017); with ORNs intact they do not fire (item 1).
   LNs skip or sparsely innervate "a cluster of anterolateral glomeruli (DL3, DA1, VA1d, and VA1lm)" (Wilson & Laurent
   2005), as Huang 2010 and the MaleCNS contact counts also suggest.
3. **Lateral-type firing without ORN excitation is documented elsewhere:** VA6 (PSTH peaks ≈74-87 spikes/s to pentyl
   acetate and 2-octanone, which inhibit VA6 ORNs; Schlief 2007), VA1d (35-43 spikes/s to C6-C8 alcohols; Seki), DL5
   (25-30 spikes/s to two odors with ORN ≤ 3; Seki), DM3 (134-217 spikes/s at onset to esters with ORN ≤ 7; Bhandawat
   2007), and VM2/DL1 with silent receptors (5-32 spikes/s; Olsen 2007). VA5, VM3 and VM7v PNs follow their own ORNs.
   DA3 and DC3 have no PN recordings.
4. **Badel's table disagrees with whole-cell PN rates beyond DA1/DL3/DA2** (derived; 14 odors × 24 glomeruli vs Seki):
   r = 0.47; 24 of 74 pairs with ≥ 80% ΔF/F have PN firing ≤ 10 spikes/s (DA2, VM7v, DA1, DL3, DC2, VA7m, VM3).
   Agreement is good for VA5, VA3, VL2a, DL4, VM2, DM4, VA7l, VM7d (r = 0.82-0.96), absent for DA1 (−0.52) and DL3.
5. **Several Badel glomeruli copy a neighbour** (derived; my reading): DA3 tracks D (r = 0.84), DM3 is a scaled copy of
   DM6 (r = 0.97), VM7v reports VM7d's ligands and misses its own best odor, VM3 reports VM2's, and VA6 tracks DA2 and
   answers geosmin (78%). Badel's inferred "PN-PN connectivity" is mostly adjacent pairs, whereas measured lateral
   excitation is "not correlated with the distance" (Olsen 2007).
6. **DA1/DL3's imaging responses are not the signature of eLN excitation** (derived): they are odor-selective (ethyl
   butyrate, OCT, 2,3-butanedione, MCH, 1-octen-3-ol ≥ 78%; benzaldehyde, ethyl acetate, 1-butanol ≈ 0), track each
   other (r = 0.87) more than total lobe activity (0.51), and are absent from VA1d and VA1v. Measured lateral excitation
   is nearly odor-independent and saturates at low input.
7. **NP225 and Badel's ROIs.** NP225 labels "67-73 projection neurons in 35 of 43 antennal glomeruli" (Tanaka 2004 via
   FlyBase); no LN expression reported. ROIs are fixed template masks (50% of mean glomerulus volume) placed by affine
   registration on four guide-posts (DL3, DA2, VM2, DM5); median overlap 70.8%, single glomeruli ≈13-98%. DL3 and DA3
   are among the smallest glomeruli (≈615-629 µm³). Badel et al. allow "some degree of contamination" and do not
   discuss the DA1/DL3 responses.
8. **Other PN imaging does not reproduce the breadth** (§2; helper, spot-checked): DA1 is flat to general odors in
   seven datasets (GH146 with GCaMP3, GCaMP6s, G-CaMP1.6, Cameleon or synapto-pHluorin), and general odors inhibit it
   (Grabe 2020, Cl⁻ imaging); DA2 is geosmin-only in both two-photon datasets that tested other odors (one exception:
   Barth's OCT 256%); DL3 shows only single-odor signals; DA3 is unmeasured elsewhere. Endo 2020 (same lab, NP225 >
   GCaMP5G) reports no glomerulus-named values.
9. **Calibration** (§4; helper, spot-checked): no GCaMP3/GCaMP6f calibration in PNs exists; dendritic calcium is
   largely nicotinic (Root 2007), and lateral excitation is electrical. Scaling NMJ data, Badel's 100-236% needs ≈18-27
   spikes/s sustained (range 12-38), while 5-10 spikes/s gives ≈8-30% (derived; tenfold uncertainty). With ≈0 spikes/s
   measured in DA1/DL3/DA2, the calibration cannot turn Badel's values there into PN firing.
10. **For brainfly (my reading): no missing mechanism should make DA1, DL3 or DA2 PNs fire to OCT or MCH.** The spiking
    data match the connectome's weak eLN contact there. Badel's values in DA1, DL3, DA2 (and DA3, DM3, VM7v, VM3, VA6)
    should not be PN-rate targets or ORN drive. Lateral firing is real in VA6, VA1d, DL5, DM3, VM2 and DL1, and makes
    better tests for an eLN model (§5).

## Conventions and access

**Conventions** (as in the other notes)
- Text in quotation marks is verbatim.
- "(fig., approx.)" = read off a published figure with a pixel grid calibrated on its axis ticks or colour bar; expect
  ±3-5% of full scale.
- "(derived)" = my arithmetic on published numbers (for Badel's Table S2 and Seki's Tables S2-S3, my own re-extraction
  of the spreadsheets).
- "Not reported" = searched the text, legends and supplement and did not find it.
- "(helper)" = compiled by one of two helper agents from the cited full texts; I spot-checked the quotes I rely on.
- Odor concentrations are the dilution in the vial; all the studies below then dilute about 7-10-fold in air.
- Seki's and Schlief's numbers are spikes/s (baseline- or solvent-subtracted); Badel's and Barth's are mean ΔF/F (%).

**Access limits.** Tanaka et al. 2004 (Curr Biol) and 2012 (J Comp Neurol) full texts returned 403, so NP225's
expression pattern is taken from FlyBase's curation of them and from Thum et al. 2007. Datta et al. 2008 and Kurtovic
et al. 2007 (Nature) are paywalled. Schlief & Wilson's Supplementary Table 1 (n per odor, odor order of the tuning
curves) was not accessed; their tuning-curve and PSTH values were read from the 800-px PMC figures. Frechter et al.
2019's PN data (R package) were not examined. Badel's Figs. S3 and S5 were read from the vector supplement rendered at
400-600 dpi; Olsen 2007 Figs. 8-9 from 800-px PMC images. Helpers could not access Someya et al. 2025 (Cell), the Root
2007 supplement or Stensmyr's Fig. S3 odor list beyond its legend, and read several calibration figures (Root 2007,
Akerboom 2012, Hendel 2008) from low-resolution images.

## 1. Electrophysiology of PNs in these glomeruli

### 1.1 Schlief & Wilson 2007, Nat Neurosci 10:623 ([PMC2838507](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838507/)): DA1 narrow, VA6 broad

**Setup.** In vivo whole-cell recordings from PN somata, females 3-8 days old. "In Mz19-Gal4,UAS-CD8GFP flies, all six
GFP-positive PNs with somata lateral to the antennal lobe are known to innervate glomerulus DA1"; VA6 PNs from
Mz612-Gal4 ("all GFP-positive PNs innervate glomerulus VA6"); every cell filled with biocytin. "Odors were diluted 1:100
v/v in paraffin oil" (3-methylthio-1-propanol and propionic acid 1:100 in water, 4-methylphenol 1:100 w/v in water,
cVA undiluted), and "all odors (including cis-vaccenyl acetate) were diluted 10-fold in air"; 500-ms pulses, six trials.
Tuning curves: "overall spike rate ... during the 500-ms period beginning 100ms after odor valve opening", minus the
baseline rate. Panel (Fig. 4d): cVA, butyric acid, 4-methylphenol, geranyl acetate, cyclohexanone,
3-methylthio-1-propanol, γ-valerolactone, propionic acid, pentyl acetate, 1-butanol, methyl salicylate,
trans-2-hexenal, pyrrolidine, benzaldehyde, isoamyl acetate, ethyl butyrate, octanal, 2-octanone, cis-3-hexen-1-ol,
plus paraffin oil, water and an empty vial. No OCT or MCH. n per odor is in Supplementary Table 1 (not accessed).

**DA1.**
- "We found that, like their presynaptic ORNs, PNs in glomerulus DA1 are highly selective for cis-vaccenyl acetate
  (Fig. 4b-d). Other odors in our test set elicited either no response, or a comparatively small response. The
  lifetime sparseness (S) of the average DA1 PN tuning curve was 0.90".
- Fig. 4c tuning curve (fig., approx.; 0/20/40 ticks at 2.84 px per spike/s): cVA 32 spikes/s (DA1 ORNs 5.4); the
  other points 4.4, 4.4, 3.7, 2.7, 1.8, 1.6, 1.5, 1.1 spikes/s and the rest on the zero line. PSTHs (Fig. 4d): the
  largest non-cVA transients are isoamyl acetate (≈8 spikes/s peak), pentyl acetate and trans-2-hexenal (≈5).
- Ethyl butyrate, the odor giving DA1 its largest Badel response (144%), evokes no visible DA1 PN response (PSTH
  ≈0-3 spikes/s, fig., approx.). Badel and Schlief agree that 1-butanol, benzaldehyde, isopentyl acetate, pentyl
  acetate, methyl salicylate, propionic acid and 3-methylthio-1-propanol give DA1 nothing (Badel −8 to 6%).
- "We observed that DA1 PNs are insensitive to propionic acid even at a high concentration (10% saturated vapor, data
  not shown)."
- Caveat (stated): "this enhancer trap line does not label all DA1 PNs, and we cannot exclude the possibility that
  unlabeled cells respond differently to our stimuli." NP225 and Mz19 both label DA1's lateral-lineage PNs (FlyBase:
  "adult antennal lobe projection neuron DA1 lPN" for NP225, Tanaka 2012), so the two studies sample the same class.

**VA6.**
- "In contrast to the DA1 PNs, PNs in glomerulus VA6 show broad odor tuning (Fig. 5b-d). These PNs are excited by
  geranyl acetate, but also by several other acetates. Several odors dissimilar to geranyl acetate (pyrrolidine and
  2-octanone) also evoke a robust response. The lifetime sparseness of the VA6 PN tuning curve is 0.58" (ORNs 0.94).
- Fig. 5c 500-ms means (fig., approx.; odor order not labelled): ≈95 and ≈80 (geranyl acetate and the next-best odor),
  then 41, 32, 31, 25, 22, 21, 21, 19.5, 19, 16, 14, 13, 9, 8, 7, 5, 1, −4 spikes/s. VA6 ORNs: 65.5 (geranyl acetate),
  then 24.5, 17, 8.5 and ≤ 5.4, many negative.
- Fig. 5d PSTH peaks, PN (ORN) (fig., approx.; control panels peak at 14-18 from noise): geranyl acetate ≈116 (≈74);
  pyrrolidine ≈116 (≈20); pentyl acetate ≈87 (inhibited); 2-octanone ≈74 (inhibited); isoamyl acetate ≈61;
  3-methylthio-1-propanol ≈47 (≈26); cis-3-hexen-1-ol ≈46; cyclohexanone ≈46 (inhibited, ≈−19); ethyl butyrate ≈42
  (inhibited, ≈−15); propionic acid ≈35; cVA ≈32; γ-valerolactone ≈32; 1-butanol ≈31.
- "it is difficult to see how feedforward mechanisms alone could excite a VA6 PN in response to an odor that inhibits
  its presynaptic ORNs (e.g., pentyl acetate or 2-octanone, Fig. 5d)."
- Statistics: "only 1 of the 19 test odors elicit DA1 PN responses that are significantly different from DA1 ORN
  responses, and none of these are significant after a Bonferroni correction ... For glomerulus VA6, by contrast, 9 of
  the 19 test odors elicit responses that are significantly different at p<0.05, and 3 of these odors are still
  significant after the stringent Bonferroni correction".
- Mechanism (authors' discussion): "One possibility is that most PNs receive indirect input from several ORN types via
  excitatory local interneurons ... If inter-glomerular excitatory connections contribute to broad tuning in VA6 PNs,
  then DA1 PNs may receive less inter-glomerular excitatory input than VA6 PNs. Consistent with this idea, we have
  previously found that some local networks in the antennal lobe selectively exclude glomerulus DA1" (ref. 47 = Wilson &
  Laurent 2005, §1.4).
- Badel's VA6: OCT 25%, MCH 69%, ethyl butyrate 104%, benzaldehyde 71%, geosmin 78%. VA6 is therefore the one target
  glomerulus where spiking without ORN excitation is documented, but OCT and MCH were not tested.

On imaging the authors add: "some functional imaging experiments in the Drosophila antennal lobe paint a somewhat
different picture, suggesting that the selectivity of most PNs closely matches that of their presynaptic ORNs. These
results may reflect the low sensitivity and limited dynamic range of the fluorescent probes used in these experiments".

### 1.2 Seki et al. 2017, BMC Biol 15:56 ([PMC5493115](https://pmc.ncbi.nlm.nih.gov/articles/PMC5493115/)) and Stensmyr et al. 2012, Cell 151:1345: DA1, DL3, DA2, VA5, VM3, VM7v, DL5

**Setup.** In vivo whole-cell recordings, "one neuron per brain", females 1-3 days; Canton-S (n = 42 flies),
GH146-GAL4 > mCD8GFP (25), NP5221 (3), NP7217 (1); 67 uniglomerular PNs in 31 glomeruli. "Odorants were diluted (10–2
v/v) except for geosmin (mostly 10–3, only three PNs were tested with 10–2 and they did not respond to 10–2 geosmin) in
H2O (for acetic acid, propionic acid) or mineral oil (for all other odors)"; 10 µl on filter paper; "additionally
diluted approximately 10 times" in air; 1-s pulses. Response: "spike numbers during the 1-s odor stimulus (0.05 s after
the onset of stimuli to 1.05 s) ... made by subtraction with the control stimulus (either mineral oil or H2O)", first
stimulus round only. ORNs by single-sensillum recording (n = 3 per class).

Stensmyr et al. 2012 (same lab; Seki is a co-author; PDF and supplement from the MPG repository): "We obtained
recordings and fills from 66 PNs (from 66 individual flies), which covered 31 different glomeruli" with the same 17
compounds, so the DA2 recordings are probably the same data as Seki's (not independent).

**Statements.**
- Seki: "a few PN classes did not show any clear responses (responses were ≤10 spikes/s) to any odors in our odor set
  (e.g., PNs innervating glomeruli DA1 and DL3)."
- Seki: "for the four glomeruli DA1, VA1lm, DL3, and VA1d, a low correlation was found (r = 0.19 ± 0.07, n = 4 ...).
  These glomeruli are innervated by OSNs present in trichoid sensilla, and the specific ligands for the OSNs and PNs
  targeting these were not included in our odor set".
- Stensmyr: "Geosmin elicited significant responses only from two PNs, both of which innervated the DA2 glomerulus ...
  DA2 PNs appear to be as selective as the input OSNs because these PNs responded exclusively to geosmin and not to any
  of the other screened compounds (Figures 4F and S3)." Fig. S3 legend: "Spike traces from a DA2 PN following odor
  stimulation. Only geosmin elicits any response."

**Values for the 14 odors shared with Badel** (Seki Tables S2 and S3, re-extracted; Badel Table S2):

| odor (10⁻²) | DA1 PN / ORN / Badel | DL3 PN / ORN / Badel | DA2 PN / ORN / Badel |
|---|---|---|---|
| ethyl butyrate | −1 / 2.7 / **144** | 0 / −3.3 / **180** | −1.5 / −4.7 / **362** |
| 2,3-butanedione | −1 / −2 / **116** | 0 / 0 / **138** | −1.5 / 1 / **256** |
| 1-octen-3-ol | −0.7 / 0.7 / **107** | 6 / 3 / 27 | −1 / −13 / **166** |
| benzaldehyde | −0.7 / 1.7 / −8 | −1 / 1.7 / 2 | −1 / −13.7 / **185** |
| acetophenone | 0 / −1.3 / 8 | 0 / 1.7 / 14 | −1 / −16.3 / **175** |
| ethyl acetate | −0.3 / −1.7 / 4 | 0 / 0 / 3 | −1 / −2 / 15 |
| isopentyl acetate | −0.3 / 2.3 / 4 | 0 / 4 / 7 | −1.5 / −6.7 / 12 |
| 2-methylphenol | −0.7 / −4.7 / −1 | 2 / −3.3 / −1 | −1 / −12.3 / 20 |
| methyl salicylate | 0 / −5.3 / 2 | 0 / 0 / 3 | −1.5 / −2.3 / 13 |
| linalool | −0.7 / −3 / 22 | 0 / 0 / 19 | −1.5 / −2.7 / 30 |
| 1-octanol | −1 / −3.7 / 20 | −1 / 0 / 25 | 0 / −5 / 11 |
| hexanoic acid | 0 / −1.7 / 17 | −1 / 6.7 / 11 | −0.5 / −2 / 29 |
| propionic acid | 0 / −0.7 / −4 | 3 / 1 / −0 | 0.5 / 0.3 / 5 |
| geosmin (Seki 10⁻³) | −1 / −0.7 / 5 | 1 / 0 / 3 | 91.5 / 132.3 / 456 |
| n PNs | 3 | 1 | 2 |

PN and ORN in spikes/s (solvent-subtracted); Badel in % ΔF/F. Bold: ≥ 80% ΔF/F with no PN firing.

- DA2's ORNs are inhibited by benzaldehyde, acetophenone and 1-octen-3-ol (−13 to −16 spikes/s; ab4A in the same
  sensillum answers benzaldehyde with 183), and DA2 PNs stay at rest; Badel's DA2 shows 166-185% for the same three.
- DL3 rests on n = 1 PN; DA1 is replicated across two labs (§1.1).

**Secondary glomeruli in the same dataset** (PN / ORN spikes/s; Badel % in brackets; selected odors):
- VA5 (n = 3): PNs follow ORNs (2-methylphenol 98.7 / 152.7 [125], benzaldehyde 79.7 / 71.3 [117], acetophenone
  65.7 / 35 [73]); without ORN excitation ≤ 8 spikes/s (isopentyl acetate 8 / −6.7, ethyl butyrate 3.3 / −1).
  Badel agrees here (r = 0.96, derived, §3.4).
- VM3 (n = 1): PNs follow ORNs (isopentyl acetate 110 / 107 [173], ethyl butyrate 70 / 65 [171], 2,3-butanedione
  96 / 35 [21]); benzaldehyde −1 / 0 [94] and 2-methylphenol −1 / 0 [80] are silent in the PN but large in Badel.
- VM7v (n = 1): PNs follow ORNs (ethyl butyrate 82 / 100 [299], 1-octen-3-ol 85 / 51 [24]); 2,3-butanedione 2 / 1.3
  [195], ethyl acetate 8 / 5.3 [212], propionic acid 0 / 11.7 [165], geosmin −1 / 1.7 [150].
- DL5 (n = 2): the only secondary glomerulus with clear PN firing beyond its ORNs: 1-octen-3-ol 30 / 1.3 [40], ethyl
  acetate 25 / 2.7 [21], 2,3-butanedione 27.5 / 10 [37], hexanoic acid 58.5 / 24 [21].
- DA3, DC3, DM3 and VA6 were not in Seki's set (Not reported).
- Contrast, the other two trichoid "pheromone" glomeruli: VA1d PNs (n = 4) fire to 1-hexanol 42.8, 1-octen-3-ol 35.5,
  1-octanol 35, linalool 23.3 and 2-methylphenol 19.5 spikes/s while their Or88a ORNs sit at −6.3 to 2.7; VA1lm (= VA1v,
  n = 1) PN 1-hexanol 28 (ORN −20.7), 1-octanol 26, linalool 22. So lateral-type firing of 20-43 spikes/s to a few
  alcohols does occur in two pheromone glomeruli, but not in DA1 or DL3. Badel's VA1d and VA1v show none of it (VA1d
  1-octen-3-ol 11%, VA1v −33%).

### 1.3 Lateral excitation measured in these glomeruli with ORN input removed

- **DA1.** Shimizu & Stopfer 2017 ([PMC5413558](https://pmc.ncbi.nlm.nih.gov/articles/PMC5413558/); antennae removed,
  palp odors 0.3%): "In antenna-less wild-type flies, odors evoked lateral excitation in ePNs in these four glomeruli
  ... While in DA1 and VA5 glomeruli of antenna-less shakB2 mutant flies, these odor-evoked lateral excitatory inputs
  were abolished and inhibition dominated". Pooled lateral-lineage values: "for ethyl acetate, peak depolarization was
  5.71 ± 1.89 mV in control flies and 0.76 ± 0.67 mV in shakB2 mutants. For ethyl butyrate, peak depolarization was
  6.23 ± 2.60 mV ... including ePNs in DA1 and VA5". DA1-only values: Not reported (traces only, Fig. 5B).
- **Trichoid glomeruli as a class.** Olsen et al. 2007 ([PMC2048819](https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/)),
  only VA7l ORNs functional, 4-methylphenol: "Glomeruli postsynaptic to different morphological types of sensilla
  receive similar levels of lateral input"; Fig. 9B (fig., approx.; 48 px per mV·s): basiconic 1.9 (n = 14
  glomeruli), coeloconic 1.7 (n = 3), trichoid 1.8 ± 0.3 mV·s (n = 6). Which six trichoid glomeruli: Not reported.
- **DM3, DC3, VM3, DL5** (Olsen 2007 Fig. 8C, ≥ 3 PNs each, same protocol; fig., approx., 37 px per mV·s): DL5 2.7,
  DM3 1.9, DC3 1.7, VM3 1.7 mV·s, against VC4 3.0 and DM6 1.3; VA1v 1.55 and VA1d 1.45 (trichoid pheromone glomeruli);
  mean of all PNs 1.9. "Responses in some PNs were large enough to elicit a few spikes, but responses in other PNs
  responses were much weaker."
- **Distance.** "there is no obvious relationship between inter-glomerular distance and the strength of lateral
  excitatory connections"; "the strength of these lateral excitatory connections is not correlated with the distance
  between the target glomerulus and the location of the ORN inputs" (Olsen 2007).
- **DA1 synergy.** Das et al. 2017: cVA + vinegar exceed the sum in DA1 PNs (eLN- and shakB-dependent), but "vinegar
  alone" gives DA1 PNs ≈0-2% ΔF/F (GCaMP3; lateral_excitation.md §6.1). Badel's DA1 also gives apple cider vinegar 3%
  and vinegar mimic −9%.
- **Sparse LN innervation of the pheromone cluster.** Wilson & Laurent 2005
  ([PMC6725763](https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/); GH298, c739 and wild-type LN fills): "some LNs did
  not send any branch into one to three glomeruli. These 'bypassed' glomeruli often included a cluster of anterolateral
  glomeruli (DL3, DA1, VA1d, and VA1lm) and less frequently other glomeruli (e.g., DC3)"; "We also measured
  innervation density in the four atypical anterolateral glomeruli (DL3, DA1, VA1d, and VA1lm) and found a lower
  innervation density for these glomeruli". Huang 2010: "Krasavietz eLNs usually send their arbors to all glomeruli
  except DA1, DL3" (lateral_excitation.md §3).

So lateral excitation in DA1 is real but, in intact flies, subthreshold for general odors: DA1 PNs at rest fire 8.6 ±
6.3 spikes/s (Jeanne & Wilson 2015, males; pn_ln_dynamics.md) and show no odor-evoked change for 18 general odors.

### 1.4 ORN-level evidence for the pheromone glomeruli

- DA1 ORNs (at1, Or67d): "DA1 ORNs are excited exclusively by cis-vaccenyl acetate, and do not respond to any other odor
  stimuli in our test set" (Schlief & Wilson 2007, 19 odors; lifetime sparseness 1.00). Seki: DA1 ORNs −5.3 to 2.7
  spikes/s for 16 general odors.
- Trichoid ORNs generally (van der Goes van Naters & Carlson 2007,
  [PMC1876700](https://pmc.ncbi.nlm.nih.gov/articles/PMC1876700/)): "Initially we tested 86 compounds ..., most of which
  are found in fruits or are fermentation products. These compounds were tested on 60 trichoid sensilla ... The compounds
  were tested in mixtures, and no mixture elicited a response greater than 20 impulses s−1 (not shown), which represents
  less than 10% of the maximal response of these ORNs". In the empty neuron, Or65a (DL3) and Or67d (DA1) responded to
  male extract, male genital material and cVA; Or47b and Or88a "were previously tested in the empty neuron system with a
  panel of 110 odors ... and no excitatory responses were recorded".
- DL3 ORNs (at4, Or65a/b/c): Seki −3.3 to 6.7 spikes/s for 16 general odors.
- DA2 ORNs (ab4B, Or56a): "The ab4B Neurons Respond Exclusively to Geosmin" (Stensmyr 2012 section title); inhibited by
  several general odors (table above).
- So DA1, DL3 and DA2 have no ORN excitation by a general odor above ≈20 spikes/s in any single-sensillum dataset
  found, and their PNs do not fire either. (DA3's Or23a has sparse data: weak DoOR responses, e.g. cyclohexanol 0.13;
  mch_oct_equalization.md §7.) "ORN input below detection" cannot produce PN
  firing that the PN recordings do not see.

### 1.5 Papers checked without usable data for this question

- Datta et al. 2008 (Nature 452:473; DA1 and VA1lm PNs): paywalled; the abstract reports anatomy and cVA only. Not
  accessed.
- Kurtovic et al. 2007 (Nature; at1/Or67d single-sensillum): paywalled; not accessed. Grosjean et al. 2011 concerns
  IR84a/VL2a, not a target glomerulus.
- Kohl et al. 2013 ([PMC3898676](https://pmc.ncbi.nlm.nih.gov/articles/PMC3898676/)): records LHNs, not DA1 PNs; cites
  "the narrow tuning of Or67d ORNs and DA1 PNs (Ha and Smith, 2006; Schlief and Wilson, 2007)".
- Frechter et al. 2019 ([PMC6550879](https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/)): "84 identified PNs" recorded
  with a 36-odor set (250-ms pulses; "12% of odors elicited a significant PN response"), but the glomerular identities
  are not given in the text; the data are in the authors' R package (not examined; no R available here). A possible
  source of DA1 (Mz19) PN responses to a larger panel.
- Jeanne & Wilson 2015 and Jeanne et al. 2018: DA1 PNs and other PNs driven optogenetically; no general-odor PN data
  for target glomeruli (Not reported).
- Bhandawat et al. 2007 ([PMC2838615](https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/); DM3 among seven glomeruli,
  18 odors at 1:100, no OCT or MCH). Fig. 3a, "mean spike rate during the 100-ms epoch when firing rates are peaking ...
  minus baseline" (fig., approx.; 0-200 ticks, bars assigned to odor slots by position), DM3 ORN / PN: ethyl acetate
  7 / 217, ethyl butyrate ≈0 / 134, benzaldehyde ≈0 / 50, 1-butanol ≈0 / 50, cis-3-hexen-1-ol ≈0 / 50, cyclohexanone
  ≈0 / 39, trans-2-hexenal ≈0 / 39; with ORN drive, pentyl acetate 183 / 246, 3-methylthio-1-propanol 186 / 240,
  2-octanone 47 / 258. So DM3 PNs, unlike DA1 PNs, fire strongly at onset to esters that barely drive their ORNs
  (peak-epoch values; 500-ms means are lower). The authors: PN-vs-ORN functions have "a y-intercept >0 ... Lateral
  excitatory connections are strong enough to trigger these responses"; lateral_excitation.md §5.6 adds the caveat that
  1-5 Hz of ORN input alone can drive 10-30 Hz through the steep transform.
- Olsen et al. 2010: in intact flies, an odor that barely drives DL5 ORNs gave DL5 PNs −1.1 Hz (lateral_excitation.md
  §5.5).
- Kazama & Wilson 2009: sister-PN correlations (DM6 and others); no target-glomerulus odor panels.
- Turner et al. 2008 and Wilson et al. 2004 recorded PNs with 3-octanol but did not identify the glomeruli.

### 1.6 Electrophysiology by glomerulus

| glomerulus (receptor) | Badel OCT / MCH (%) | PN firing to general odors without ORN excitation (intact flies) | lateral input when deafferented |
|---|---|---|---|
| DA1 (Or67d) | 118 / 78 | none: ≤ 4.4 spikes/s, 18 odors (Schlief); −1.7 to 0, 16 odors, n = 3 (Seki) | 5.7-6.2 mV peak, lateral lineage incl. DA1, shakB-dependent (Shimizu & Stopfer) |
| DL3 (Or65a/b/c) | 166 / 91 | none: −1 to 6 spikes/s, 16 odors, n = 1 (Seki) | Not reported |
| DA2 (Or56a) | 140 / 236 | none: geosmin only, n = 2 (Stensmyr/Seki) | Not reported |
| DA3 (Or23a) | 113 / 116 | Not reported (no PN recordings found; GH146-negative) | Not reported |
| VA6 (Or82a) | 25 / 69 | yes: 500-ms means up to 32-41, PSTH peaks 30-116 spikes/s, incl. odors that inhibit the ORNs (Schlief) | Not reported |
| DL5 (Or7a) | 38 / 77 | partly: 25-30 spikes/s to two odors with ORN ≤ 3 (Seki, n = 2); −1.1 Hz (Olsen 2010) | ≈2.7 mV·s (Olsen 2007) |
| VA5 (Or49b) | 19 / 110 | ≤ 8 spikes/s (Seki, n = 3) | lateral lineage, as DA1 (Shimizu & Stopfer) |
| VM3 (Or9a) | 122 / 72 | ≤ 4 spikes/s (Seki, n = 1) | ≈1.7 mV·s (Olsen 2007) |
| VM7v (Or59c) | 106 / 121 | ≤ 8 spikes/s (Seki, n = 1) | Not reported |
| DM3 (Or47a/Or33b) | 219 / 87 | yes at onset: ethyl acetate 217, ethyl butyrate 134 spikes/s (100-ms peak) with ORN ≤ 7 (Bhandawat 2007); OCT/MCH not tested | ≈1.9 mV·s (Olsen 2007) |
| DC3 (Or83c) | 86 / 101 | Not reported | ≈1.7 mV·s (Olsen 2007) |

## 2. Other PN imaging datasets

Compiled by a helper agent (helper) from the cited full texts, supplements and figure pixels; I re-checked the Knaden
Table S2 rows, the Endo 2020 genotype and method, and the Grabe 2020, Mohamed 2019, Das 2017 and Ng 2002 quotes.

### 2.1 Tally for the four main glomeruli (PN-level imaging, general odors)

| glomerulus | broad, large responses | small or odor-restricted | none | not covered or not named |
|---|---|---|---|---|
| DA1 | Badel 2016 only | Das 2017 (2-3% to limonene, 1-hexanol, acetic acid vs 15-22% to cVA); Knaden 2012 (hexanoic acid 0.14 only) | Barth 2014; Knaden 2012; Grabe 2020 (Cl⁻ imaging shows inhibition); Mohamed 2019; Ng 2002; Das 2017 (vinegar); Dweck 2015 | Endo 2020 (not named); Wang 2003 (not imaged); Strube-Bloss 2017 (illegible) |
| DL3 | Badel 2016 only | Yu 2004 (OCT, spH); Knaden 2012 (acetophenone 0.31, mirrored in DL3's ORN signal); Ng 2002 (banana); Grabe 2020 (benzaldehyde, weak) | Barth 2014; Mohamed 2019; Dweck 2015 | Wang 2003; Endo 2020 |
| DA2 | Badel 2016; Barth 2014 for OCT only (256%) | Knaden 2012 (0.1-0.3 to several odors, mirrored in DA2's ORN signal, which SSR says is silent or inhibited); Wang 2003 (cineole at ≈23% saturated vapour only) | Mohamed 2019 (geosmin only); Stensmyr 2012 (imaging of geosmin only; whole-cell flat); Wang 2003 (15 of 16 odors); Dweck 2015 | Grabe 2020; Ng 2002; Endo 2020 |
| DA3 | Badel 2016 | Pech 2015 (MCH ≈29, OCT ≈18%, one plane) | Barth 2014 (but GH146 does not label DA3, §3.1) | Knaden, Mohamed, Grabe, Wang, Ng, Dweck (not covered); Endo 2020 (not named) |

### 2.2 Datasets

**Barth et al. 2014, J Neurosci 34:1819** ([PMC6827587](https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/); project
readings in oct_mch_input.md §8). GH146-Gal4 > GCaMP3, two-photon at 5 Hz, three focal planes, 18 glomeruli, ≈2-s
odors, one presentation per odor (helper). DA1 MCH 5 / OCT 4, DL3 5 / 4, DA3 11 / 16, DL5 17 / 20% against 109-255% in
responding glomeruli (fig., approx.); DA2 OCT 256, MCH 44% although Barth's own ORN imaging shows no DA2 response. The
same data reach ≈180-280% in strongly driven glomeruli (Fig. 4D, DM1 3-octanol ≈280%; helper, fig., approx.).

**Knaden, Strutz, Ahsan, Sachse & Hansson 2012, Cell Rep 1:392** (doi:10.1016/j.celrep.2012.03.002; Table S2 .xls).
- GH146-GAL4 > G-CaMP1.6 (PNs) and Orco-GAL4 (ORNs) in the same study; widefield CCD, one top plane, 20 glomeruli
  ("the top layer of the antennal lobe"); ROI "a coordinate (10×10 µm) ... placed in the center of an identified
  glomerulus".
- Odors (the 12 later used by Endo 2020 and Badel): acetophenone, benzaldehyde, linalool, 2-methylphenol, 1-octen-3-ol,
  1-octanol, formic acid, 3-methylthio-1-propanol, pentanoic acid, 2,3-butanedione, γ-butyrolactone, hexanoic acid;
  "diluted (10^-1 or 10^-3) in mineral oil ... additionally diluted by 1:10" (Table S2 labels 10⁻² and 10⁻⁴).
- Table S2 PN values at 10⁻² ("Median Odor-specific Glomerular Activation", normalized; I re-checked these rows):
  - DA1: −0.105 to 0.076 for 11 odors, hexanoic acid 0.142 (2,3-butanedione −0.047, 1-octen-3-ol −0.055); DA1 ORNs
    ≤ 0.021.
  - DL3: acetophenone 0.314, benzaldehyde 0.109, others −0.06 to 0.05 (2,3-butanedione −0.0006); DL3's ORN signal is
    similar (acetophenone 0.33, benzaldehyde 0.39), and neighbouring DL1's ORNs answer these with 0.63 and 0.46.
  - DA2: 1-octen-3-ol 0.280, 2,3-butanedione 0.264, acetophenone 0.187, 2-methylphenol 0.126, benzaldehyde 0.119; DA2's
    ORN signal shows the same odors (1-octen-3-ol 0.36, 1-octanol 0.31), although Or56a neurons answer only geosmin.
  - For scale: PN maximum 0.78 (DL1, acetophenone) (helper, derived).
- Authors: "the effect of light scattering that arises when using wide field imaging occurs at both the OSN and the PN
  level and is thus compensated by comparing both data sets." Responses mirrored at the ORN level in glomeruli whose
  ORNs are silent (DA2, DL3) are most simply scatter from neighbours (helper's and my reading).

**Mohamed et al. 2019, Nat Commun 10:1201** ([PMC6416470](https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/)).
- GH146-GAL4 > GCaMP6s, two-photon, "34 identified glomeruli from 5-6 focal planes" (planes ≈25-30 µm apart, 4 Hz;
  helper); "The glomeruli could be reliably
  identified from the baseline fluorescence of GCaMP6s, GCaMP6f, or GCaMP3.0." Includes DA1, DA2, DL3, VA5, VA6, VM3,
  VM7v, DC3, DL5, DM3; not DA3.
- Odors: ethyl acetate 10⁻²-10⁻⁴, benzaldehyde 10⁻¹ and 10⁻², methyl salicylate 10⁻³, balsamic vinegar 10⁻², geosmin
  10⁻³.
- Supplementary Figs. 2-3 (helper, fig., approx., ΔF/F0): DA1 ≤ 0.51 (solvent 0.08-0.31; largest net 0.28); DA2 geosmin
  3.82, other odors ≤ 0.71 (largest net 0.34); DL3 ≤ 0.24; against DM1 6.6 (ethyl acetate 10⁻²) and DL1 6.6-7.1
  (benzaldehyde 10⁻¹). Secondary: VA5 ≤ 0.21; VA6 ≤ 0.37 with dips to −0.29; VM3 ≤ 0.41; VM7v 1.5-2.0 (ethyl acetate
  10⁻²); DC3 1.9-2.6 (benzaldehyde 10⁻¹); DL5 5.5-6.3; DM3 5.5-5.7.

**Grabe et al. 2020, eNeuro 7:ENEURO.0213-19.2019** ([PMC6957311](https://pmc.ncbi.nlm.nih.gov/articles/PMC6957311/)).
- GH146-GAL4 > Cameleon (Ca²⁺) and Clomeleon (Cl⁻), widefield; ROI "a 7 × 7-pixel coordinate (i.e., 9 × 9 μm), which
  was positioned into an anatomically identified glomerulus"; 11 odors, "6 μl of 1:10 diluted odor" on filter paper;
  "Responses were normalized to highest Cl- or Ca2+ influx in each animal over all odors."
- Fig. 6 (helper, colour bins): DA1 Ca²⁺ 0.8-1 for cVA, < 0.2 for the 10 general odors; DA1 Cl⁻ 0.4-0.8 for benzaldehyde,
  1-hexanol, cyclohexanone, isoamyl acetate and pentyl acetate, i.e. general odors inhibit DA1 PNs. DL3 Ca²⁺ 0.2-0.4 for
  benzaldehyde and cVA, < 0.2 otherwise. No DA2 or DA3.
- "some glomeruli were inhibited without being excited."

**Wang, Wong, Flores, Vosshall & Axel 2003, Cell 112:271** (doi:10.1016/S0092-8674(03)00004-7). GH146 > G-CaMP,
two-photon, explant, "23 different glomeruli to 16 pure odorants at multiple concentrations"; threshold = "minimum
concentration required to elicit a 20% change in ΔF/F". DA2: only cineole, at ≈23% saturated vapour; nothing else up
to 40% (3-octanol, 1-octen-3-ol, isoamyl acetate, benzaldehyde among them). 3-octanol drove only VM2, DM2, DM1, DM6 and
DC2. VA5: benzaldehyde at ≈38% only. DA1, DL3, DA3 not imaged (helper, fig., approx.). Authors: "The spatial resolution
(0.5 × 0.5 × 2 μm) allows discrimination among neighboring glomeruli with confidence."

**Ng et al. 2002, Neuron 36:463** (doi:10.1016/S0896-6273(02)00975-3). GH146 > synapto-pHluorin, two-photon; apple,
cherry and banana fragrances at 10⁻²-10⁻³. ORNs: "glomeruli were observed that responded to none (DA1, DL1, VA3,
VC1)". PNs: the PN codes "each differed from their ORN counterparts ... by a single missing 'letter,' corresponding to
activity in glomeruli DL3, VA5, and VA1, respectively." Fig. 4B (helper): DA1 none; DL3 banana only, ≈2-3% ΔF/F
(fig., approx.). The helper notes that an ORN-level DL3 response to fruit fragrances conflicts with Or65a's narrow
tuning, so either the assignment or spillover is in question.

**Das et al. 2017, PNAS 114:E9962** ([PMC5699073](https://pmc.ncbi.nlm.nih.gov/articles/PMC5699073/)). GH146 > GCaMP3:
"cVA evoked a strong and clear response in the DA1 glomerulus in a dose-dependent manner, whereas vinegar did not elicit
any activity in this glomerulus." Fig. 1K (helper, fig., approx., 10⁻¹): DA1 limonene 2.0%, 1-hexanol 3.0%, acetic
acid 2.2% vs cVA 14.8-21.7%.

**Dweck et al. 2015, PNAS 112:E2829** ([PMC4450379](https://pmc.ncbi.nlm.nih.gov/articles/PMC4450379/)). GH146 >
GCaMP6s, two-photon; methyl laurate, myristate, palmitate at 10⁻¹: "this information enters and leaves the AL through
these two channels only" (VA1v, VA1d). DA1, DA2, DL3, DC3, DL5, VA5, VA6 ≈0 in Fig. 2C (helper, fig., approx.).

**Stensmyr et al. 2012** (imaging part). Orco > GCaMP3: geosmin activated DA2 only ("In a number of recordings, we also
noted activity from VM2; however, these signals were not consistently reproducible"). GH146 > GCaMP3: "Stimulation with
geosmin again exclusively activated the DA2 glomerulus"; general odors were not imaged. Compare Badel's geosmin:
DC2 157, VM7v 150, VM7d 127, VM1 99, VA6 78% besides DA2 456%.

**Yu et al. 2004 and Pech et al. 2015** (oct_mch_input.md §8). Synapto-pHluorin in PNs: "Four of the eight glomeruli were
activated reproducibly by OCT": DM6, DM2, DM3 and DL3. Pech 2015 (one focal plane): DA3 MCH ≈29, OCT ≈18%.

**Endo, Tsuchimoto & Kazama 2020, Neuron 108:367** (doi:10.1016/j.neuron.2020.07.029; article PDF from the publisher
supplement, re-checked). Same lab and olfactometer as Badel. Genotype "NP225-Gal4,UAS-GCaMP5G(attP40)/UAS-GCaMP5G(attP40)"
(GCaMP5G, not GCaMP6f); "volumetric Ca2+ imaging of PNs in 37 out of 51 AL glomeruli"; "PN responses in individual
glomeruli were extracted by registering AL images in all the trials to a template AL and averaging fluorescence in each
template glomerulus (Badel et al., 2016)"; 15 odors (the Knaden 12 plus MCH, OCT and ethyl butyrate). Values by
glomerulus name: Not reported (glomeruli indexed by number); the data are "available from the corresponding author on
request". On tuning only: "This is consistent with PNs being more broadly tuned than KCs (Turner et al., 2008)". No
discussion of DA1/DL3 breadth (Not reported). Someya et al. 2025 (Cell; same lab; odor list includes 3-octanol, ethyl
butyrate, geosmin, cVA): main text not accessible.

**Lateral PN responses in secondary glomeruli, imaging.** Shang et al. 2007 (GH146 > spH, two-photon, 0.1% saturated
vapour): "PN responses could be stimulated in either glomerulus with odors that failed to activate its monosynaptic ORN
afferent"; DM3 PN phenylacetaldehyde ≈2.2% vs 2-heptanone ≈4.3% ΔF/F (helper, fig., approx.). Silbering et al. 2008
(G-CaMP1.3, eight glomeruli): DL5 lateral responses, "Similar broadening effects were found in 12 of 24 odor/glomerulus
combinations, although in most cases only at the highest concentration" (lateral_excitation.md §6.5).

**Checked, no PN imaging of the target glomeruli with general odors** (helper): Silbering et al. 2011 (IR ORNs only:
"We expressed ... GCaMP1.6 ... in defined subpopulations of IR OSNs"); Strutz et al. 2014 (PNs imaged in the lateral horn
only); Root 2007 (no target glomeruli named); Hige et al. 2015 Neuron and Nature (no PN imaging); Kohl 2013; Liang 2013
(Mz699 iPNs); Ronderos 2014 (DC3 anatomy); Hong & Wilson 2015 (ORN and LN imaging); Lin 2014; Prisco 2021 (calyx);
Inada 2017; Semmelhack & Wang 2009 (vinegar glomeruli named, targets not); Churgin et al. 2025 (five glomeruli, none of
the four); Taisz 2023 and Lebreton 2014 (cVA only); Strube-Bloss 2017 (DA1 in the set, heat map illegible). Abstract
only: Datta 2008, Ruta 2010, Kurtovic 2007, Dweck 2013.

**Anatomy-level statement.** Grabe et al. 2016: "glomeruli innervated by narrowly tuned OSNs seem to possess a larger
number of projection neurons and are involved in less lateral processing than glomeruli targeted by broadly tuned OSNs"
(re-checked in the article PDF).

### 2.3 Reading of §2

- Badel's broad DA1 and DL3 responses are not reproduced by any other PN imaging dataset (seven for DA1, at
  concentrations similar to or above Badel's: Knaden 10⁻² effective, Mohamed benzaldehyde 10⁻¹, Grabe 10⁻¹), with
  GCaMP6s, GCaMP3, G-CaMP1.6, Cameleon and synapto-pHluorin, widefield and two-photon. They agree with the whole-cell
  data (§1).
- DA2 is geosmin-specific in both two-photon datasets that tested other odors (Mohamed; Wang). Knaden's small DA2
  signals appear equally in DA2's ORN signal and are best read as widefield scatter. The one replication of a DA2
  general-odor response is Barth's OCT 256%, unexplained (Barth's ORNs show no DA2 response; whole-cell OCT not tested;
  Wang 2003 saw no DA2 response to 3-octanol up to 40% saturated vapour, but with G-CaMP1.3 and a 20% criterion).
- DL3 has a few odor-specific signals (OCT in Yu 2004, acetophenone in Knaden, banana in Ng), not Badel's broad profile.
- DA3 is essentially unmeasured outside Badel; Pech's one plane gives ≈18-29%.
- The same lab's Endo 2020 uses the same driver, registration and olfactometer with a different GCaMP, and does not
  report or discuss glomerulus-level values, so it neither replicates nor refutes Badel independently.

## 3. Imaging confounds: NP225, Badel's ROIs, and what Badel's own table shows

### 3.1 NP225-Gal4

- FlyBase (P{GawB}NP0225, [FBti0058535](https://flybase.org/reports/FBti0058535.html)), curated from Tanaka et al. 2004
  and 2012: "Expression is observed in 67-73 projection neurons in 35 of 43 antennal glomeruli. (Tanaka et al., 2004)";
  "ScerGAL4NP0225 drives expression in around 68 uniglomerular antennal lobe projection neurons. The cell bodies of
  around 31 of these neurons are positioned in the anterior-dorsal part of the antennal lobe. Around 29 cell bodies are
  found in the lateral part and around 9 are positioned ventrally ... (Tanaka et al., 2012)". The per-type list includes
  "DA1 lPN", "DL3 lPN", "DA2 lPN", "DA3 adPN", "DC3 adPN", "DM3 adPN", "VA6 adPN", "VM3 adPN", "VM7v adPN", "VA1d adPN",
  "VA1v adPN" and others; outside the antennal lobe a "mushroom body pedunculus-vertical lobe arborizing neuron 1"
  (Flybrain Neuron Database) and SEZ/VNC neurons (Israel et al. 2022).
- Thum et al. 2007 ([PMC6672858](https://pmc.ncbi.nlm.nih.gov/articles/PMC6672858/)): "This strain predominantly labels 75
  PNs projecting to 35 glomeruli with few neurons in other parts of the brain potentially overlapping with the cells in
  GH146 (Tanaka et al., 2004)".
- Badel: NP225 "labels 37 glomeruli with high specificity (Figure 2A)".
- Antennal-lobe LNs, multiglomerular PNs or other non-uniglomerular cells in NP225: Not reported (FlyBase, Thum 2007,
  Badel, Tanaka 2009 [PMC2753235](https://pmc.ncbi.nlm.nih.gov/articles/PMC2753235/)). Tanaka 2004/2012 full texts were
  not accessible (Cell Press and Wiley returned 403), so a small LN population cannot be excluded from the primary
  source.
- Coverage: NP225 includes DA3, which GH146 lacks (Grabe 2016 Table S1: DA3 "GH146 negative"; GH146 labels 8 DA1, 5
  DL3 and 6.5 DA2 PNs in females). Barth's GH146 "DA3" values are therefore not a test of DA3 PNs.

### 3.2 Badel's imaging and ROI method (main text and Supplemental Experimental Procedures)

- Two-photon, Zeiss LSM 710, "W Plan-Apochromat, 20x, numerical aperture 1.0", 930 nm, "33 optical slices separated by
  3 μm in 595 ms (18 ms/slice)", "volume scanning at a rate of ~1.7 Hz", "pixel size in a slice was 1.384 x 1.384 μm,
  which was sufficient to resolve individual glomeruli measuring on average ~10 μm in diameter". Genotype
  "NP225-Gal4,UAS-IVS-GCaMP6f(attP40)/UAS-IVS-GCaMP6f(attP40)", females 2-4 days. 4-s odor, response = mean ΔF/F over
  "frames 10-17" (≈0.6-5.4 s after valve opening at 0.595 s per volume, derived; the odor reaches the fly ≈0.5 s
  after the valve opens).
- Motion: each volume "re-aligned to the high-resolution 3D image with sub-pixel precision ... by shifting the target
  image" (rigid translation only).
- ROIs: "To extract fluorescence changes in individual glomeruli in an efficient and objective manner, we constructed a
  template AL against which all images were registered." Glomeruli were delineated in immunostained brains, registered
  "by optimizing an affine transformation to maximize the cross-correlation between four guidepost glomeruli (DL3, DA2,
  VM2, and DM5)", superimposed and "thresholded to obtain the template AL, in such a way that each glomerulus in the
  template covers 50% of the mean volume of the corresponding glomerulus. This moderate threshold volume was chosen to
  increase the probability that template glomeruli fall within the boundaries of actual glomeruli." In each experiment
  only the four guide-posts were delineated; the transform was then "applied to all images". Brains were discarded if
  "the correlation with the template was lower than 0.6 in the 4 guidepost glomeruli".
- Accuracy: "the median overlap computed across glomeruli was 70.8% with respect to the template volume". Fig. S3B
  (fig., approx.; 30 of 37 dots resolvable, glomeruli not labelled): 13, 27, 33, 35, 38, 42, 45, 51, 52, 57% ... up to
  96 and 98%; 8 of the 30 below 50%.
- DL3 and DA2 are guide-posts, chosen "because they are strongly labeled by NP225-Gal4", so they are the best-registered
  glomeruli; their responses cannot be blamed on misplaced masks of their own, only on what falls inside them.
- Glomerulus sizes (Grabe et al. 2016 Table S1, females, in vivo, µm³ ± SD): DA1 4738 ± 732, DA2 1630 ± 677, DL3 615 ±
  177, DA3 629 ± 99, D 1170 ± 473, DL4 622 ± 177, DM3 1336 ± 305, DM6 1439 ± 236, VA6 2520 ± 218, VM7v 1296 ± 632,
  VM7d 1578 ± 638, VM3 1898 ± 170; whole lobe 111,593. Equivalent-sphere diameters: DL3 and DA3 ≈10.5 µm, DA1 ≈21 µm
  (derived), so DL3 and DA3 span about three or four of Badel's 3-µm slices.
- Neighbours (FlyBase anatomy ontology definitions, after Laissue 1999 and Couto 2005): DA1 "lies ventrolateral to
  glomerulus DL3 and lateral to glomerulus DL4"; DL3 "lies at the dorsal tip of the antennal lobe dorsomedial to
  glomerulus DA1"; DA3 "lies dorsal to glomerulus D and ventrolateral to glomerulus DL3"; DL4 "is a small glomerulus
  surrounded by glomeruli D, DL3 and DA1"; DA2 "lies dorsal to glomerulus VA6 and medial to glomerulus DA4"; VA1d is
  "dorsal to VA1v and ventral to DA1"; VM7d is "dorsal to VM7v"; VM3 is "ventromedial to glomerulus VA2", VM2
  "dorsomedial to glomerulus VA2"; DM3 "lies dorsal to glomerulus DM2", and Badel's Fig. S3D calls DM2, DM5 and DM6
  "neighboring glomeruli".

### 3.3 What Badel et al. say about contamination and lateral input

- Contamination: "These data suggest that our registration procedure reliably extracts individual glomerular responses
  without substantial contamination from neighboring glomeruli. We cannot, however, rule out some degree of
  contamination due to animal-to-animal variability in AL morphology ... Nevertheless, because morphological variation
  must occur randomly, it can be safely assumed that no systematic contamination is present in our data." The test was
  one example (hexanoic acid: DM2 responds, neighbours DM5 and DM6 do not) and a simulation that mixed "10% or 20% of
  the response of one of its 3 nearest neighbors" into each glomerulus and found decoding weights unchanged. A fixed
  template applied to every fly can produce systematic contamination for a given pair of glomeruli, which this argument
  does not cover (my reading).
- Comparison with ORNs (Fig. S3C, Hallem & Carlson 2006, 26 odors): "The Pearson correlation between the entire data
  sets was 0.52." Per glomerulus (fig., approx.): VA5 0.87, VM2 0.80, DL4 0.79, VM3 0.76, DM2 0.69, DM4 0.65, DM5 0.55,
  DL5 0.54, DL1 0.51, VA1v 0.49, DA4l 0.45, VA1d 0.43, DM6 0.42, **DA3 0.23, DM3 0.17, DL3 0.05, VA6 −0.10**.
- Lateral input: blocking DM1 ORN output with TNT (GH146-QF > QUAS-GCaMP3, ethyl acetate) "the reduction in PN response
  was only 40% ... this residual activity is likely to be the result of lateral interactions between glomeruli, which
  provide excitatory drive to PNs whose cognate ORNs are silenced (Olsen et al., 2007; Root et al., 2007; Shang et al.,
  2007)", whereas "PN activity in glomerulus DM5 was completely abolished". In whole-cell recordings DM1 is the glomerulus
  with the least lateral excitation (0.1-1.1 mV, unchanged in shakB²; Yaksi & Wilson 2010, lateral_excitation.md), and
  Root 2007 found ≈0-4% ΔF/F in Or42b-mutant DM1 PNs. Badel tested TNT efficacy only in DM5.
- They then inferred a "PN-PN connectivity matrix using the correlation structure of Ca2+ signals during the baseline
  period" (Fig. S5) and used it to predict the TNT results.
- DA1, DL3, pheromones, Or67d, Or65a: Not discussed (searched main text and supplement).
- Endo et al. 2020: see §2.

### 3.4 Derived checks on Badel's Table S2 (84 stimuli, 37 glomeruli)

All numbers here are mine, from the published spreadsheet (mmc2.xls); "pure" = the 36 single odors.

**(a) DA1 and DL3 respond to a few odors, not to everything that drives the lobe.**

| odor (10⁻²) | DA1 | DL3 | DA2 | DA3 | D | sum of 37 glomeruli |
|---|---|---|---|---|---|---|
| ethyl butyrate | 144 | 180 | 362 | −0 | 10 | 3647 |
| benzaldehyde | −8 | 2 | 185 | 11 | 65 | 2635 |
| 3-octanol | 118 | 166 | 140 | 113 | 146 | 2346 |
| 4-methylcyclohexanol | 78 | 91 | 236 | 116 | 172 | 2305 |
| 1-butanol | 6 | 17 | 25 | 19 | 12 | 1929 |
| acetophenone | 8 | 14 | 175 | 135 | 125 | 1917 |
| 1-octen-3-ol | 107 | 27 | 166 | 107 | 136 | 1861 |
| 2,3-butanedione | 116 | 138 | 256 | 9 | 32 | 1766 |
| ethyl acetate | 4 | 3 | 15 | −12 | −43 | 1729 |
| isopentyl acetate | 4 | 7 | 12 | 25 | 86 | 1725 |
| geosmin | 5 | 3 | 456 | 1 | −6 | 1364 |
| pentanoic acid | 66 | 24 | 23 | −5 | −16 | 1336 |
| 1-octanol | 20 | 25 | 11 | 102 | 149 | 1204 |
| 3-methylthio-1-propanol | 3 | 76 | 19 | 4 | 4 | 923 |
| linalool | 22 | 19 | 30 | 41 | 172 | 849 |

- Correlation with the summed response of the other 36 glomeruli (pure odors): DA1 0.51, DL3 0.51, DA2 0.49, DA3 0.33;
  for comparison VA2 0.83, VM3 0.71, VA6 0.70.
- DA1 vs DL3: r = 0.87 (pure), 0.79 (all 84). No other glomerulus matches them above 0.55 (DC3, DA2, VM4, VA2).
- The other pheromone glomeruli are quiet: VA1d's largest pure-odor response is 50% (MCH), VA1v's 26% (Badel lists
  VA1v's OCT as −33%).
- Geosmin, which excites only DA2 ORNs, gives DA1 5% and DL3 3%. If DA1/DL3 responses were broad eLN excitation, one
  ORN type firing ≈130 spikes/s should drive it: Olsen 2007 found lateral depolarization half-maximal at ≈7-10 spikes/s
  of one ORN type and saturated above 50 (lateral_excitation.md §8.3).

**(b) Profiles that copy a neighbour.** Best-matching glomerulus over the 36 pure odors (r):

| glomerulus | best match (r) | neighbour? | r with total activity | whole-cell check |
|---|---|---|---|---|
| DA3 | D (0.84), DL4 (0.71) | yes, DA3 "dorsal to D"; DL4 adjacent | 0.33 | none |
| DM3 | DM6 (0.97) | both border DM2 | 0.55 | DM3 PNs fire 217 spikes/s (peak) to ethyl acetate (Bhandawat); Badel's DM3 15%, DM6 2% |
| VM7v | VM7d (0.87) | yes | 0.46 | VM7v PN silent to VM7d's ligands (§1.2) |
| VM3 | VM2 (0.89), VA2 (0.81) | VA2 adjacent; VM2 next to VA2 | 0.71 | VM3 PN silent to VM2's ligands (§1.2) |
| VA6 | DA2 (0.72) | yes, DA2 "dorsal to VA6" | 0.70 | VA6 PNs broad (§1.1) |
| DA1 | DL3 (0.87) | yes | 0.51 | DA1 PN silent (§1.1-1.2) |
| DL3 | DA1 (0.87) | yes | 0.51 | DL3 PN silent (§1.2) |
| VA5 | DL1, VC1 (0.83) | no (DL1) | 0.40 | VA5 agrees with whole-cell (r = 0.96) |

- DM3 looks like a scaled copy of DM6: 1-butanol 193 vs 237, acetophenone 153 vs 215, mango mimic 156 vs 255,
  acetaldehyde 156 vs 255, phenylethylamine 150 vs 245%. Phenylethylamine (an amine) driving the ab5B ORN class is not
  expected, and DM3's correlation with Or47a's Hallem-Carlson profile is 0.17 (Fig. S3C).
- Badel's VM7v and VM7d are nearly the same signal: 2,3-butanedione 195 vs 178, ethyl acetate 212 vs 178, propionic acid
  165 vs 160, geosmin 150 vs 127, acetophenone 103 vs 82%. In Seki's recordings these are VM7d ligands (VM7d ORN 65, 61,
  82 spikes/s) that leave the VM7v PN at rest, while VM7v's best odor, 1-octen-3-ol (VM7v PN 85, ORN 51 spikes/s), gives
  only 24% in Badel's VM7v. So Badel's "VM7v" mostly reports VM7d. (FlyBase notes that VM7v "was not found in all
  samples when it was originally categorised".) Likewise VM3 ≈ 0.35-0.8 × VM2 for VM2's ligands (2-methylphenol 80 vs
  231, ethyl butyrate 171 vs 349, ethyl acetate 79 vs 150%).
- VA6 answers geosmin with 78% (VM7d 127%, VM7v 150%, DC2 157% too); in Seki's recordings geosmin moves only DA2 PNs
  (VM7d −1, VM7v −1, DC2 3.3 spikes/s; DC2 ORN 1). Badel used geosmin at 10⁻² and Seki mostly at 10⁻³ ("three PNs were
  tested with 10–2 and they did not respond").

**(c) Badel's inferred PN-PN "connectivity" is a map of neighbours.** Fig. S5A, digitized on its colour bar (0-0.35;
fig., approx.): the largest entries are VA1d←VA1v 0.35, VA1v←VA1d 0.29, DA3←D 0.24, VM7d←VM7v 0.24, VA7m←VC2 0.23,
DA4l←DC3 0.19, VA1v↔VA5 0.17, VC2←VA7m 0.17, VA7m←VA7l 0.17, VM7v←VM7d 0.16, DL3←DA1 0.15, VM3←VM2 0.15, DM3←DM6 0.14,
DM5←DM2 0.14; mean row sum 0.62 (row = target). Most of these are anatomical neighbours (§3.2). Correlated baseline
fluctuations in adjacent masks are what optical or registration crosstalk produces; electrophysiological lateral
excitation is not distance-dependent (§1.3), and heterotypic PN pairs have spike-count correlations of only 0.004-0.015
(Kazama & Wilson 2009; lateral_excitation.md §5.2). Neighbour-restricted circuits (patchy LNs, multiglomerular PNs)
could also correlate neighbours, so this is suggestive rather than decisive (my reading).

**(d) Badel vs whole-cell PN recordings, all shared glomeruli.** 14 odors in both studies (ethyl butyrate,
2,3-butanedione, 1-octen-3-ol, benzaldehyde, acetophenone, ethyl acetate, isopentyl acetate, 2-methylphenol, methyl
salicylate, linalool, 1-octanol, hexanoic acid, propionic acid, geosmin) × 24 glomeruli in both (Seki's VA1lm = VA1v):
- Pearson r = 0.47, Spearman 0.38 over 336 pairs.
- 74 pairs reach ≥ 80% ΔF/F; 24 of them have PN firing ≤ 10 spikes/s: DA2 ×5, VM7v ×5, DA1 ×3, DL3 ×2, DC2 ×2 (ethyl
  acetate 104%, geosmin 157%), VA7m ×2 (benzaldehyde 288%, ethyl acetate 120%), VM3 ×2, DL1 ×1 (2-methylphenol 105% at
  −12 spikes/s), VM7d ×1 (geosmin 127%), VL2a ×1 (benzaldehyde 87%).
- The reverse also occurs: 13 of 59 pairs with ≥ 50 spikes/s have < 30% ΔF/F (e.g. VA4 isopentyl acetate 114 spikes/s
  vs 19%; DL1 methyl salicylate 140 vs 21%; VA2 and VM3 2,3-butanedione 95-96 vs 12-21%; DC2 linalool and 1-octanol
  92-96 vs 1-9%).
- Per-glomerulus r: VA5 0.96, VA3 0.96, VL2a 0.94, DL4 0.92, VM2 0.86, DM4 0.84, VA7l 0.84, VM7d 0.82, DM6 0.69, VC2
  0.68, D 0.66, DA2 0.64 (carried by geosmin; −0.40 without it), VM3 0.59, DL5 0.51, VA7m 0.44, VA1d 0.44, DL1 0.43,
  VA4 0.35, VM7v 0.28, VA2 0.07, DC2 −0.06, DL3 −0.11, VA1lm −0.33, DA1 −0.52 (−0.61 without geosmin).
- Caveats: Seki has 1-4 PNs per glomerulus, one trial each, a 1-s window, filter-paper delivery and a different lab;
  Badel averages 4-9 flies × 4 trials over ≈4.7 s. Small DL3/VM3/VM7v samples. Neither study measured both modalities
  in the same flies. The whole-cell studies used 0.5-1-s pulses and Badel 4-s pulses, so a PN response that builds up
  only after more than ≈1-2 s of odor would be missed by the recordings (Schlief's PSTHs run to 2 s after a 0.5-s
  pulse and show none in DA1); Not tested.

## 4. Calibration: GCaMP ΔF/F vs PN firing

Compiled by a helper agent (and three sub-helpers) from the cited sources (helper); I re-checked the Jayaraman &
Laurent, Root 2007, Wang 2003, Yaksi & Wilson, Moreaux & Laurent and Xiao et al. quotes in the downloaded texts.

### 4.1 PN calibrations exist only for G-CaMP1.3

No calibration of GCaMP3, GCaMP5G or GCaMP6 against PN spiking exists (Not reported), and none for Kenyon cells or LNs
(Gruntman & Turner 2013: "we were unable to establish the relationship between these somatic signals and KC spiking
activity").

- **Jayaraman & Laurent 2007** (Front Neural Circuits 1:3, [PMC2526281](https://pmc.ncbi.nlm.nih.gov/articles/PMC2526281/)).
  "GH146-Gal4, UAS-GCaMP flies ... with four copies of G-CaMP"; in vivo, two-photon line scans across PN somata with
  simultaneous loose-patch recording (n = 8 PNs, 7 flies), 1-s odors.
  - "G-CaMP failed to report even sustained (>1 second) activity if it was below 30 sp∕second or to capture fast
    modulations of instantaneous firing rate (up to 80 sp∕second)". "This correlation (mean response rate vs. mean
    fluorescence change) was 0.61".
  - Fig. 3H (helper, fig., approx.): significant trials 6-54% ΔF/F at 24-72 spikes/s; fitted ≈0.47% ΔF/F per spike/s,
    intercept ≈−3%; trials ≤ ≈23-29 spikes/s non-significant (−2 to +3.5%).
  - DL1 glomerulus (NP3529): 45-60% peaks at 38-67 spikes/s held 1-2 s; 7-17 spikes/s sustained for ≈10 s left ΔF/F at or
    below baseline (helper, fig., approx.).
- **Root et al. 2007** (same lab, same glomerulus, same odor, separate experiments; explant): VM2 dendrites ≈122% ΔF/F to
  isoamyl acetate at ≈8% saturated vapour; VM2 loose patch ≈29 spikes/s in the first second at ≈8.8% (fig., approx.),
  i.e. ≈4% per spike/s (helper, derived), ≈9× the somatic slope above. Quotes (re-checked): "Insect nicotinic
  acetylcholine receptors are highly permeable to calcium (23, 24); therefore monitoring intracellular calcium provides a
  measure of synaptic excitation"; imaging-guided recordings: calcium activity "was always accompanied by brisk firing of
  action potentials with spike frequencies (spikes in the first second of odor response) ranging from 16 to 48 Hz ...
  Conversely, the absence of calcium activity was always associated with a few or no action potentials"; one PN "reaches
  a peak value of 100% in the dendrites and 24% in the cell body"; "Thus, our measure of calcium activity in PN dendrites
  reflects the PN spike output."
- **Wang et al. 2003** (G-CaMP, four copies, explant, antennal-nerve stimulation at 100 Hz): "a 10% increase in
  fluorescent intensity (at 2 mM extracellular Ca2+) when only a single stimulus was delivered to each sensory axon ...
  maximum change in fluorescent intensity of 50%"; "a 2-fold increase in extracellular Ca2+ results in close to an
  8-fold increase in ΔF/F"; Hill coefficient 3 against stimulus number.

### 4.2 What sets dendritic calcium in PNs

- ORN-driven dendritic calcium is largely nicotinic (Root 2007 above; Root et al. 2008: "Insect dendritic calcium
  increases are mostly due to influx through nicotinic acetylcholine receptors").
- Lateral excitation is electrical: "This mutation eliminates odor-evoked lateral excitation in PNs and diminishes some
  PN odor responses. This implies that lateral excitation is mediated by electrical synapses from eLNs onto PNs" (Yaksi &
  Wilson 2010). It brings no nicotinic calcium entry; only voltage-gated channels (PNs have them, Iniguez et al. 2013)
  and the spikes it causes.
- In locust PNs (OGB-1, simultaneous recording; Moreaux & Laurent 2007): "ΔF/F (t) variations in PNs are influenced by at
  least three different factors: firing (Figures 3 and 5), subthreshold depolarization (Figures 4 and 5), and calcium
  clearance (Figure 4A)"; linear decoding "S = 1.2 (sp/second)/%", i.e. ≈0.83% per spike/s up to 40 spikes/s (derived).
- ORNs with modern indicators (simultaneous SSR and imaging; Xiao et al. 2025, 2026): linear within a cell type, but
  "calcium responses scaled linearly with spike frequency across ORNs but with widely varying slopes—from 0.09 in ac4C to
  1.11 in at1"; "Despite comparable spike rates, calcium signals can differ by more than tenfold." So cell-type gain can
  differ tenfold at equal spiking.

### 4.3 Ceilings and indicator ratios

- PN dendrite maxima: GCaMP3 ≈144% (DM2, Tian 2009), 318 ± 90% (DC1, Akerboom 2012, maximum 472%), ≈280% (DM1, Barth
  2014); GCaMP6f ≈760% peak (DC1, 3-octanol 10⁻³, Chen 2013, fig., approx.); Badel's table (mean over the odor period)
  maximum 456%, with 366 of 3108 values above 100% (helper, derived). Badel's OCT/MCH values are not near a ceiling.
- Larval NMJ boutons, 2-s trains (Chen 2013 Supp. Table 4 = Dana 2016 data; Akerboom 2012, fig., approx.), ΔF/F at 1 / 5
  / 10 / 20 / 40 / 80 Hz: GCaMP6f 3.4 / 10.5 / 38 / 230 / 779 / 1062%; GCaMP3 ≈1 / 3 / 10 / 59 / 236 / 341%. Half-maximum
  ≈31 Hz for both; GCaMP6f/GCaMP3 ≈3.5-3.9 at 5-20 Hz (helper, derived).
- Purified protein (Chen 2013 Supp. Table 2): GCaMP3 Fmax/Fmin 13.5, Kd 345 nM, Hill 2.54; GCaMP6f 51.8, 375 nM, 2.27.
- Inside Badel, GCaMP3 (GH146-QF, Fig. 5B) and GCaMP6f (NP225, Table S2) disagree in the wrong direction for ethyl
  acetate: DM5 ≈222 vs 202%, DM1 ≈159 vs 30% (helper, fig., approx.); driver, window and genotype differ.

### 4.4 Derived estimates for PN dendrites (helper)

Method (helper's, derived): assume steady-state calcium rises linearly with rate, so a PN firing at r gives the ΔF/F
an NMJ bouton gives at g·r; estimate g from G-CaMP1.3 measured in both preparations (Jayaraman & Laurent somata g ≈
0.5-0.9; in vivo DL1 glomerulus g ≈ 1; Root's explant VM2 dendrites with cognate ORN input g > 2.8); then read GCaMP6f
and GCaMP3 off the NMJ curves, scaled ×1.2-1.5 for 4 s instead of 2 s.

| sustained PN rate (4 s) | 5 spikes/s | 10 | 20 | 30 | 100 |
|---|---|---|---|---|---|
| GCaMP6f, spike-driven (g = 0.5) | ≈8-10% | ≈13-16% | ≈47-58% | ≈130-170% | at ceiling |
| GCaMP6f, spike-driven, central (g = 0.7) | ≈10-12% | ≈24-30% | ≈110-140% | ≈300-380% | at ceiling |
| GCaMP6f, g = 1 | ≈13-16% | ≈47-58% | ≈280-350% | ≈470% | at ceiling |
| GCaMP6f, cognate nicotinic input (g = 3) | ≈130-170% | ≈470% | at ceiling | — | — |
| GCaMP3 (2 s), g = 0.5 | ≈2% | ≈3% | ≈10% | ≈28% | ≈270% |
| GCaMP3 (2 s), g = 0.7 | ≈2% | ≈5% | ≈24% | ≈65% | ≈320% |
| GCaMP3 (2 s), g = 1 | ≈3% | ≈10% | ≈59% | ≈133% | ≈340% |

Inversions (helper, derived): Badel's 100-236% (4-s window means) needs ≈25-38 spikes/s sustained at g = 0.5, ≈18-27
at g = 0.7 and ≈12-19 at g = 1; only with cognate (nicotinic) input (g = 3) does ≈4-6 spikes/s suffice. Barth's 4-16%
(GCaMP3, ≈2 s) corresponds to ≈12-24 spikes/s at g = 0.5, ≈8-17 at g = 0.7 and ≈6-12 at g = 1, very uncertain because
values of a few percent are near the noise level (plausible span 2-50). Uncertainty is about tenfold overall (g,
expression, peak vs mean, cell-type gain), and external Ca²⁺ matters: Badel's saline had 1.5 mM, the G-CaMP1.3
anchors 2 mM, and Wang 2003 saw ≈8× more ΔF/F at 2 than at 1 mM.

### 4.5 Reading of §4

- 100-236% GCaMP6f from purely lateral firing would need the top of the measured lateral range (≈18-38 spikes/s for
  spike-driven gains g = 0.5-0.7). At 5-10 spikes/s the expected signal is ≈8-30% (≈13-58% at g = 1), three to ten
  times too small, and lateral input, being electrical, should not add the nicotinic calcium that makes ORN-driven
  dendritic signals large.
- For DA1, DL3 and DA2 the measured lateral firing to general odors is ≈0 (§1), so no reading of the calibration turns
  Badel's 100-362% there into PN firing. Either the signal is not from those PNs' own activity (contamination, §3.4), or
  NP225 dendritic calcium there reports something the soma does not; the second has no direct support.
- Barth's 4-5% in DA1 and DL3 (GCaMP3) is consistent with ≈0-12 spikes/s; it cannot distinguish 0 from a few
  spikes/s.

## 5. What this means for brainfly (my reading)

These are inferences from the measurements above, not measurements.

**Which reading is right, glomerulus by glomerulus.**

| glomerulus | lateral excitation making PNs fire? | imaging artifact? | ORN input below detection? | reading |
|---|---|---|---|---|
| DA1 | no: silent to 18 + 16 general odors in two labs; lateral input subthreshold (5.7-6.2 mV only when deafferented) | likely: profile shared with neighbour DL3, uncorrelated with ephys (r = −0.52); flat in seven other imaging datasets | no: ORNs silent, and PNs silent too | not PN firing; drop as a target |
| DL3 | no (n = 1 PN, 16 odors) | likely (as DA1); other imaging shows only single-odor signals | no | not PN firing; drop |
| DA2 | no: geosmin only (n = 2) | likely for the general odors (166-362% where PNs rest and ORNs are inhibited); OCT also high in Barth's GH146 > GCaMP3 imaging (256%, oct_mch_input.md §8, fig., approx.), so not unique to NP225 | no for the 16 tested odors; OCT/MCH untested in ephys | not PN firing for general odors; OCT/MCH unresolved but very unlikely to be strong |
| DA3 | no data | possible: tracks neighbour D (r = 0.84) | possible (Or23a untested with MCH) | unresolved; do not use as a firing target |
| VA6 | yes: up to ≈30-40 spikes/s (500-ms means) to many odors, including odors that inhibit its ORNs | partly possible (tracks neighbour DA2; geosmin 78%) | no | real lateral-type firing; a genuine test for an eLN model |
| DL5 | partly: 25-30 spikes/s to 1-octen-3-ol and ethyl acetate with ORN ≤ 3 | — | — | some lateral firing |
| VM7v, VM3 | no: PNs follow their ORNs | likely for the non-spiking responses (copies of VM7d and VM2) | — | use only where the ORN supports it |
| DM3 (MCH) | possible: DM3 PNs fire at onset to esters with weak ORN input (Bhandawat); MCH untested | likely: DM3 is a 0.6-0.8× copy of DM6 (r = 0.97), and Badel's DM3 gives ethyl acetate 15% where DM3 PNs fire 217 spikes/s | ab5B −2 spikes/s to MCH | Badel's DM3 values not usable; MCH firing unresolved |
| VA5 | no: follows ORNs; imaging agrees with ephys (r = 0.96) | unlikely | possible for MCH (ab6B coded 0; MCH resembles VA5's cresol ligands) | treat as ORN-driven if anything |
| DC3 | no intact data | possible (tracks DA4l, 0.77) | weak ORN data (Or83c OCT 9, MCH −1 spikes/s) | unresolved |

- **The decision-relevant answer: for DA1, DL3 and DA2, none of the three proposed mechanisms makes the PNs fire,
  because the PNs do not fire.** The connectome's sparse cholinergic-LN contact with these glomeruli, Huang's eLN
  avoidance of DA1/DL3 and Wilson & Laurent's LN bypassing of the anterolateral cluster all predict weak lateral input,
  and the spiking data agree. A connectome-based lateral excitation that leaves DA1/DL3/DA2/DA3 PNs near rest for OCT and
  MCH matches the flies; the model is not missing a mechanism there.
- **Imaging elsewhere and the calibration point the same way.** Seven other PN imaging datasets see DA1 flat to
  general odors and DA2 geosmin-specific (§2), and 100-236% ΔF/F would need ≈18-27 spikes/s sustained (§4), which the
  recordings rule out in DA1, DL3 and DA2. The remaining alternative, that NP225 dendritic calcium there reports input
  that does not reach the soma, has no direct support; lateral input to these PNs is electrical, without the nicotinic
  calcium entry that makes dendritic signals large. Either way the model's PN firing, not Badel's ΔF/F, is the quantity
  to match.
- **This revises earlier project readings.** oct_mch_concentration.md §2.1 reads Badel's DA1 and DL3 responses as
  "most likely lateral input to PNs", and §2.3 calls "Lateral excitation of 5-32 spikes/s" "the likely source" of the
  MCH breadth without receptor support. For DA1, DL3 and DA2 the measured firing to general odors is ≈0, not 5-32; the
  5-32 comes from VM2 and DL1 PNs with silent receptors (Olsen 2007), glomeruli with ordinary LN innervation.
  weak_input_gain.md §8 proposes MCH ORN input in "VM7v, DA3, DL4, DA4l, DL3, DA1, VM3"; for DA1 and DL3 that would
  make PNs fire where real ones do not. The PN-inferred fills described in oct_mch_concentration.md §2.1 (OCT DL3 0.47,
  DA1 0.33; MCH DL3 0.25, DA1 0.22) have the same problem, if any version of the model still uses them.
- **Effect on the fly targets** (derived, Badel Table S2): leaving out DA1, DL3, DA2 and DA3 changes summed
  MCH/OCT from 0.98 to 0.99 (OCT 2346 → 1808, MCH 2305 → 1784) and glomeruli > 50% from 14 : 19 to 10 : 15. Also leaving
  out DM3, VM7v and VM3 gives 1.11 (1361 vs 1504; 7 : 12). The equalization target barely moves; the breadth target
  (glomeruli answering both odors) loses most of its "unsupported" members.
- **Where lateral excitation should make PNs fire (held-out tests for the eLN work in lateral_excitation.md §9):**
  - T20, VA6 tuning (Schlief 2007, 1:100, 500 ms): PSTH peaks ≈116 pyrrolidine, ≈87 pentyl acetate and ≈74 2-octanone
    (both inhibit VA6 ORNs), ≈61 isoamyl acetate, ≈42 ethyl butyrate; lifetime sparseness 0.58 vs 0.94 in ORNs.
  - T21, DA1 silence (Schlief 2007; Seki 2017): DA1 PNs ≤ ≈4 spikes/s to 18 general odors (1:100) and −1.7 to 0 to 16
    (10⁻²), with cVA ≈32; DL3 ≤ 6 and DA2 ≤ 1.5 spikes/s (Seki). An eLN model that fires these PNs fails.
  - T22, DL5 (Seki): 1-octen-3-ol 30 and ethyl acetate 25 spikes/s with ORN ≤ 3.
  - T23, VA1d and VA1v (Seki): 1-hexanol, 1-octanol, 1-octen-3-ol and linalool 22-43 spikes/s with silent ORNs, but no
    response to ethyl butyrate, benzaldehyde or ethyl acetate (−0.75 to −0.5 spikes/s in VA1d).
  - T24, DM3 onset (Bhandawat 2007, 1:100, 100-ms peak epoch): ethyl acetate ≈217 and ethyl butyrate ≈134 spikes/s
    with DM3 ORNs at ≤ 7 (fig., approx.); a joint test of the steep ORN→PN transform and lateral input, not of lateral
    input alone.
  - These sit alongside T7 (VM2/DL1 receptor mutants, 5-32 spikes/s) and T15 (Olsen 2010, near-zero net responses in
    VM7 and DL5 to weak odors).
- **Use of Badel's table generally.** About a third of Badel's ≥ 80% responses on odor-glomerulus pairs shared with
  whole-cell data have no PN firing, and several glomeruli copy a neighbour (§3.4). Glomerulus-by-glomerulus matching
  to Badel is unreliable for DA1, DL3, DA2, DA3, DM3, VM7v, VM3, VA6, DC2 and VA7m; it is good for VA5, VA3, VL2a, DL4,
  VM2, DM4, VA7l and VM7d (r ≥ 0.82 with whole-cell rates). Population-level quantities (summed ratio, number of
  glomeruli) are affected less, because the unsupported responses fall on both odors.
- **Open.** No one has recorded identified PNs of any target glomerulus to OCT or MCH. A whole-cell recording of DA1,
  DL3 and DA2 PNs at Badel's or Hige's concentration of OCT and MCH would settle the remainder; so would re-registering
  Badel's or Endo's volumes with per-fly glomerulus segmentation.

## Sources

Primary sources read for this note (§1, §3, §5):
- Badel L, Ohta K, Tsuchimoto Y, Kazama H (2016). Decoding of context-dependent olfactory behavior in Drosophila.
  Neuron 91:155-167. doi:10.1016/j.neuron.2016.05.022. PDF: https://kazamalab.riken.jp/pdf/Neuron_Badel_2016.pdf;
  supplement: https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc1.pdf; Table S2:
  https://ars.els-cdn.com/content/image/1-s2.0-S089662731630201X-mmc2.xls (re-extracted).
- Schlief ML, Wilson RI (2007). Olfactory processing and behavior downstream from highly selective receptor neurons.
  Nat Neurosci 10:623-630. https://pmc.ncbi.nlm.nih.gov/articles/PMC2838507/ (Supplementary Table 1 with n per odor not
  accessed).
- Seki Y, Dweck HKM, Rybak J, Wicher D, Sachse S, Hansson BS (2017). Olfactory coding from the periphery to higher brain
  centers in the Drosophila brain. BMC Biol 15:56. https://pmc.ncbi.nlm.nih.gov/articles/PMC5493115/; Tables S2 and S3:
  https://static-content.springer.com/esm/art%3A10.1186%2Fs12915-017-0389-z/MediaObjects/12915_2017_389_MOESM3_ESM.xlsx
  and ..._MOESM4_ESM.xlsx (re-extracted).
- Stensmyr MC, Dweck HKM, Farhan A, et al. (2012). A conserved dedicated olfactory circuit for detecting harmful microbes
  in Drosophila. Cell 151:1345-1357. doi:10.1016/j.cell.2012.09.046. PDF and supplement from the MPG repository:
  https://pure.mpg.de/rest/items/item_1577953_10/component/file_1577957/content and
  .../file_3157174/content.
- Olsen SR, Bhandawat V, Wilson RI (2007). Excitatory interactions between olfactory processing channels in the
  Drosophila antennal lobe. Neuron 54:89-103. https://pmc.ncbi.nlm.nih.gov/articles/PMC2048819/ (Figs. 8 and 9
  digitized).
- Shimizu K, Stopfer M (2017). A population of projection neurons that inhibits the lateral horn but excites the antennal
  lobe through chemical synapses in Drosophila. Front Neural Circuits 11:30.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5413558/
- Wilson RI, Laurent G (2005). Role of GABAergic inhibition in shaping odor-evoked spatiotemporal patterns in the
  Drosophila antennal lobe. J Neurosci 25:9069-9079. https://pmc.ncbi.nlm.nih.gov/articles/PMC6725763/
- van der Goes van Naters W, Carlson JR (2007). Receptors and neurons for fly odors in Drosophila. Curr Biol 17:606-612.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1876700/
- Thum AS, Jenett A, Ito K, Heisenberg M, Tanimoto H (2007). Multiple memory traces for olfactory reward learning in
  Drosophila. J Neurosci 27:11132-11138. https://pmc.ncbi.nlm.nih.gov/articles/PMC6672858/
- FlyBase report for P{GawB}NP0225 (curating Tanaka et al. 2004 Curr Biol 14:449 and Tanaka, Endo & Ito 2012 J Comp
  Neurol 520:4067, neither accessible directly): https://flybase.org/reports/FBti0058535.html
- FlyBase anatomy ontology glomerulus definitions (via EBI OLS): DA1 FBbt:00003932, DL3 FBbt:00003964, DA2
  FBbt:00003933, DA3 FBbt:00003934, DL4 FBbt:00003965, D FBbt:00003960, DM6 FBbt:00003941, DM3 FBbt:00003972, VA6
  FBbt:00003938, VM7d FBbt:00110028, VM7v FBbt:00007092, VM3 FBbt:00003948, VM2 FBbt:00003947, VA1d FBbt:00007101.
  https://www.ebi.ac.uk/ols4/ontologies/fbbt
- Grabe V, Baschwitz A, Dweck HKM, Lavista-Llanos S, Hansson BS, Sachse S (2016). Elucidating the neuronal architecture
  of olfactory glomeruli in the Drosophila antennal lobe. Cell Rep 16:3401-3413. doi:10.1016/j.celrep.2016.08.063;
  Table S1 in https://ars.els-cdn.com/content/image/1-s2.0-S2211124716311445-mmc1.pdf; Table S3 (SSR of 11 receptors)
  in ..._mmc2.xlsx.
- Kohl J, Ostrovsky AD, Frechter S, Jefferis GSXE (2013). A bidirectional circuit switch reroutes pheromone signals in
  male and female brains. Cell 155:1610-1623. https://pmc.ncbi.nlm.nih.gov/articles/PMC3898676/
- Frechter S, Bates AS, Tootoonian S, et al. (2019). Functional and anatomical specificity in a higher olfactory centre.
  eLife 8:e44590. https://pmc.ncbi.nlm.nih.gov/articles/PMC6550879/
- Liang L, Li Y, Potter CJ, et al. (2013). GABAergic projection neurons route selective olfactory inputs to specific
  higher-order neurons. Neuron 79:917-931. https://pmc.ncbi.nlm.nih.gov/articles/PMC3838762/ (DA1 iPN/ePN responses to
  optogenetic Or67d activation only).
- Tanaka NK, Ito K, Stopfer M (2009). Odor-evoked neural oscillations in Drosophila are mediated by widely branching
  interneurons. J Neurosci 29:8595-8603. https://pmc.ncbi.nlm.nih.gov/articles/PMC2753235/ (NP225 used as PN marker).
- Not accessed (paywall): Datta SR et al. (2008) Nature 452:473; Kurtovic A, Widmer A, Dickson BJ (2007) Nature 446:542;
  Grosjean Y et al. (2011) Nature 478:236 (IR84a, not a target glomerulus); Tanaka et al. 2004 and 2012 full texts.
- Cited through existing notes: Yaksi & Wilson 2010, Huang et al. 2010, Kazama & Wilson 2009, Kazama, Yaksi & Wilson
  2011, Das et al. 2017, Root et al. 2007, Bhandawat et al. 2007, Olsen et al. 2010, Olsen & Wilson 2008
  (lateral_excitation.md §11); Jeanne & Wilson 2015 (pn_ln_dynamics.md); Barth et al. 2014, Yu et al. 2004, Pech et al.
  2015 (oct_mch_input.md §8); Hallem & Carlson 2006 (as plotted in Badel Fig. S3C).

Sources for §2 (helper-compiled; spot-checked where stated):
- Knaden M, Strutz A, Ahsan J, Sachse S, Hansson BS (2012). Spatial representation of odorant valence in an insect
  brain. Cell Rep 1:392-399. doi:10.1016/j.celrep.2012.03.002 (Table S2 read).
- Mohamed AAM et al. (2019). Odor mixtures of opposing valence unveil inter-glomerular crosstalk in the Drosophila
  antennal lobe. Nat Commun 10:1201. https://pmc.ncbi.nlm.nih.gov/articles/PMC6416470/
- Grabe V, Schubert M, Strube-Bloss M, et al. (2020). Odor-induced multi-level inhibitory maps in Drosophila. eNeuro
  7:ENEURO.0213-19.2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6957311/
- Wang JW, Wong AM, Flores J, Vosshall LB, Axel R (2003). Two-photon calcium imaging reveals an odor-evoked map of
  activity in the fly brain. Cell 112:271-282. doi:10.1016/S0092-8674(03)00004-7
- Ng M, Roorda RD, Lima SQ, et al. (2002). Transmission of olfactory information between three populations of neurons
  in the antennal lobe of the fly. Neuron 36:463-474. doi:10.1016/S0896-6273(02)00975-3
- Das S et al. (2017) PNAS 114:E9962 (https://pmc.ncbi.nlm.nih.gov/articles/PMC5699073/); Dweck HKM et al. (2015) PNAS
  112:E2829 (https://pmc.ncbi.nlm.nih.gov/articles/PMC4450379/); Barth J et al. (2014) J Neurosci 34:1819
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC6827587/); Shang Y et al. (2007) Cell 128:601
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC2866183/); Silbering AF et al. (2008) J Neurosci 28:13075
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC6671615/); Silbering AF et al. (2011) J Neurosci 31:13357
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC6623294/); Strutz A et al. (2014) eLife 3:e04147
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC4270039/); Strube-Bloss MF et al. (2017) Sci Rep 7:7854
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC5552818/); Semmelhack JL, Wang JW (2009) Nature 459:218
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC2702439/); Churgin MA et al. (2025) eLife
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC11896609/); Hige T et al. (2015) Neuron
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/) and Nature (https://pmc.ncbi.nlm.nih.gov/articles/PMC4860018/).
- Endo K, Tsuchimoto Y, Kazama H (2020). Synthesis of conserved odor object representations in a random,
  divergent-convergent network. Neuron 108:367-381. doi:10.1016/j.neuron.2020.07.029 (article PDF from the publisher's
  supplementary files, re-checked). Someya et al. (2025) Cell, doi:10.1016/j.cell.2025.08.032 (not accessible).

Sources for §4 (helper-compiled; quotes spot-checked where stated):
- Jayaraman V, Laurent G (2007). Evaluating a genetically encoded optical sensor of neural activity using
  electrophysiology in intact adult fruit flies. Front Neural Circuits 1:3. https://pmc.ncbi.nlm.nih.gov/articles/PMC2526281/
- Root CM et al. (2007) PNAS 104:11826 (https://pmc.ncbi.nlm.nih.gov/articles/PMC1913902/); Root CM et al. (2008)
  Neuron 59:311 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/).
- Yaksi E, Wilson RI (2010) Neuron 67:1034 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2954501/); Iniguez J et al.
  (2013) (https://pmc.ncbi.nlm.nih.gov/articles/PMC4042424/); Gouwens NW, Wilson RI (2009) J Neurosci 29:6239
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/); Moreaux L, Laurent G (2007) Front Neural Circuits 1:2 (locust)
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC2526277/).
- Chen TW et al. (2013) Nature 499:295 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3777791/; SI tables 2 and 4); Dana H
  et al. (2016) eLife (https://pmc.ncbi.nlm.nih.gov/articles/PMC4846379/); Dana H et al. (2019) Nat Methods 16:649
  (doi:10.1038/s41592-019-0435-6); Akerboom J et al. (2012) J Neurosci 32:13819
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC3482105/); Tian L et al. (2009) Nat Methods 6:875
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC2858873/); Hendel T et al. (2008) J Neurosci 28:7399
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC6670390/); Reiff DF et al. (2005) J Neurosci 25:4766
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC1464576/).
- Xiao et al. (2025) J Neurogenet (https://pmc.ncbi.nlm.nih.gov/articles/PMC13088990/); Xiao et al. (2026) J Neurosci
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC13107351/); Martelli C, Fiala A (2019) eLife
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/).
- Gruntman E, Turner GC (2013) Nat Neurosci 16:1821 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/); Honegger KS,
  Campbell RAA, Turner GC (2011) J Neurosci 31:11772 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3180869/).

