# Why flies' antennal lobe makes MCH about equal to OCT: what was checked, with numbers

Research-agent report (10 October 2026), saved as received. Scratch scripts are in the session scratchpad
(`helper_mech/`), outside the repo. "Derived" numbers come from published values, the model's existing output
(`experiments/odor_probe54.json`) and the MaleCNS v1.0 files the model is built from. "Static eq." means the Olsen 2010 /
Luo 2010 equation with Rmax 165, exponent 1.5, m 0.05, inputs = DoOR × 200 and σ 12 or 25; it reproduces
weak_input_gain.md §8's values (0.64/0.59, and 0.75/0.69 with Barth fills).

## Bottom line

1. **The biggest effect that can be put in numbers is that the model and flies are summed over different glomeruli,
   not a missing mechanism.**
   - Flies' 0.85 (Barth, GH146) and 0.98 (Badel, NP225) are sums over glomeruli that leave out OCT's strongest targets:
     neither driver labels VC3 or VM5d PNs; NP225 also misses VM5v and DC1; GH146 also misses VM5v.
   - These are the model's top OCT glomeruli: VM5d 152, VM5v 123, DC1 64 and DA4m 56 Hz in probe54.
   - The model's own probe54 output, summed over the same glomeruli (derived; no new run):

     | probe54 condition | all 63 glomeruli | Badel's 37 (NP225) | Barth's 18 (GH146) |
     |---|---|---|---|
     | equalization | 0.56 | **0.86** (flies 0.98) | **0.82** (flies 0.85) |
     | equalization_filled | 0.66 | **0.93** (flies 0.98) | **0.76** (flies 0.85) |

   - The static eq. shows the same pattern: 0.64/0.59 over all glomeruli becomes 0.87/0.82 on the NP225 set.
   - A second difference: the model's `upn_first` (0.515) sums over neurons, while imaging is per glomerulus. Weighting
     Badel's numbers by PN count lowers 0.98 to 0.93–0.95.
   - Flies' ratio over the whole lobe has never been measured. Adding plausible OCT responses in the four missing
     glomeruli turns Badel's 0.98 into about 0.70–0.88 (derived).
2. **Real equalization remains on the same glomeruli, but smaller.** On the 11 glomeruli Barth imaged at both ORN and PN
   level, MCH/OCT is 0.15–0.35 at the ORN terminals and 0.56–0.66 at the PNs (derived).
3. **Glomerulus-specific inhibition does not favour MCH.** Hong & Wilson 2015 found VA3, MCH's main ORN input, among
   the most inhibitable glomeruli (0.89 by LN activation, 0.87 by GABA). Weighted by ORN drive, MCH's input lands in
   glomeruli of sensitivity 0.57–0.62 against 0.38–0.42 for OCT's. Root 2008 says the opposite for GABA-B (VA3's
   terminals 27% suppression). In the static eq. the measured differences move MCH/OCT by −0.06 to +0.01.
4. **LN anatomy and the connectome show no OCT/MCH difference.** Chou 2010 innervation probability, weighted by drive:
   0.85 vs 0.85. MaleCNS GABA-LN→ORN synapses per ORN→PN synapse: 0.27 vs 0.30 (OCT vs MCH). In MaleCNS, LN→ORN wiring
   density does not predict Hong & Wilson's sensitivity (r −0.27 and −0.13).
5. **One antennal-lobe lever not measured for these odours could be large: odour-specific LN recruitment.** At equal
   total ORN input Hong & Wilson found LN recruitment depends on the odour (ANCOVA p = 0.002): at 1 mV·s of ORN field
   potential pentyl acetate gives about 67% LN ΔF/F and E2-hexenal about 43%. If OCT's broader input recruited 1.25–1.5×
   the inhibition its total input implies, the static eq. gives 0.64 → 0.75–0.86. Synapse counts alone give no such bonus
   (MaleCNS ORN→LN drive, MCH/OCT 0.44, about the input ratio 0.43), so it would have to come from LN nonlinearity.
6. **Mixture interactions, ORN kinetics, convergence, spontaneous rates and PN properties do not favour MCH.** No
   mixture synergy in the fly antennal lobe; a model run on steady-state rates overweights OCT by at most about
   1.15–1.25× (derived); convergence and PN uEPSPs slightly favour OCT.
7. **No GCaMP3 or GCaMP6f calibration against PN spike rate exists, and no study recorded PN spikes to both odours.**
   The only PN calibration (G-CaMP1.3) has a threshold of about 30 spikes/s, which makes weak MCH responses look weaker.
   Saturation could turn a true 0.6 into 0.8–0.9, but only under firing rates nobody has measured.
8. **Where the remaining gap is.**
   - Breadth. On the matched glomeruli, flies' PNs respond to both odours in DL3, DA3, DA4l, VA5, VM2, and to MCH in DM6
     and DM3; the unfilled model's PNs are at about 0 Hz there. Cyclohexanol (MCH without its methyl group) drives Or43a
     (DA4l) at 0.51 and Or85f (DL4) at 0.23 in DoOR, and MCH was never tested on those receptors.
   - Kenyon cells. At the KC level the gap is real (model 0.25, flies 0.73–0.92), and KCs receive input from all PNs,
     VM5d and VM5v included. In flies, APL equalizes KC claw responses: peak MCH/OCT about 0.89 with APL working and
     about 0.65 with APL silenced (Prisco 2021); peak × count goes from about 0.50 to 0.84 (derived).

## 1. Glomerulus-specific inhibition

**Hong & Wilson 2015, Neuron 85:573** ([PMC5495107](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495107/); Supplemental
Table 1, [mmc2.xlsx](https://ars.els-cdn.com/content/image/1-s2.0-S0896627314011490-mmc2.xlsx), parsed).
- Method: ChR2 in NP3056 LNs ("labels between 50 – 60 LNs"), shakB² males; sensitivity is the slope of PN sEPSC
  suppression against light intensity, 46 PNs; GABA sensitivity by DPNI-GABA uncaging, 52 PNs from females; both
  normalized so the most sensitive cell is 1.
- "sEPSCs were completely suppressed in the most sensitive PNs, whereas sEPSCs were almost completely unaffected in other
  PNs". "Sensitivity ranges from nearly totally insensitive (e.g. glomerulus DL4) to almost completely inhibited (e.g.
  glomerulus VA3)". "PNs corresponding to glomerulus DC4 were among the least sensitive to both GABA and LN activity,
  whereas PNs corresponding to VA3 were among the most sensitive".
- By LN activation (mean, n): DM5 0.98 (1), DL2v 0.97 (1), VA3 0.90 (3), VA7 0.71 (1) … VM2 0.29 (1), DL4 0.18 (2), DC4
  0.04 (1). By GABA: DA1 0.97 (2), VA3 0.87 (3), DL2d 0.75 (1) … VM5d 0.21 (3), VM5v 0.19 (2), VA1d 0.15 (2), DC4 0.05 (1).
  Absolute size: the mean of 3 PNs at 22 mW/mm² leaves about 32% of sEPSC activity (Fig. 4D, fig., approx.).
- Predictors: GABA sensitivity R² 0.65 (p 0.002); not LN calcium (R² 0.28), LN release-site density (0.02), tuning
  breadth (0.17), or odour-profile distance (0.04, 0.03). "the lifetime strength of lateral inhibition in each glomerulus
  is mainly an autonomous feature of that glomerulus, not a property of the LN network."
- VC3 excluded by the authors ("the odor response profiles of VC3 PNs differed dramatically in recordings from different
  brains"; its values 0.43 (7) by LN activation, 0.26 (3) by GABA).
- Recruitment: "focal activation of even a single glomerulus recruits GABAergic interneurons in all glomeruli"; "LN
  activity scales with the logarithm of total ORN spike rate". Geosmin gives extra LN activity inside DA2.

**Root et al. 2008, Neuron 59:311** ([PMC2539065](https://pmc.ncbi.nlm.nih.gov/articles/PMC2539065/)). Explant,
olfactory-nerve stimulation, GCaMP. "ORNs innervating the VC3 and DM2 glomeruli have relatively weak intensity. In
contrast, the VC1, VA4 and VM7 glomeruli … exhibit very high intensity." CGP54626 raised the PN slope 153% for cVA (DA1),
67% for ethyl hexanoate (DM2), 43% for 2-phenylethanol (VA3), 0 for CO₂ (V). Fig. 5G, % suppression of ORN-terminal
calcium by 20 µM SKF97541 (fig., approx.): V 16, VA3 27, VM4 55, VC3 59, DM2 67, DA4 69, VA4 75, VA1d 81, DA1 84, VC1 89,
DC2 89, VA6 91, VA1lm 92, VM7 97. Root and Hong disagree about VA3 (possibly GABA-A included in Hong's, GABA-B only in
Root's; not tested).

**Olsen 2010 / Olsen & Wilson 2008.** m 10.63 (VM7) vs 4.19 (DL5): "glomeruli differ in their sensitivity to lateral
inhibition". DM1's σ 44.8 in saline attributed to "odor-evoked intra-glomerular GABA release and/or tonic
inter-glomerular GABA release". Removing lateral input disinhibited 18 of 20 odours in VM7 and 13 of 20 in VC1. No OCT or
MCH.

**LN anatomy.** Chou et al. 2010 (Table S2, 1,532 LNs × 54 glomeruli): "The LN innervation probability of a glomerulus is
positively correlated with the mean odor-evoked firing rate of the ORNs presynaptic to that glomerulus (r=0.63, p<0.005,
n=23 glomeruli)"; per glomerulus (derived; median 0.85, range 0.57–0.92): OCT glomeruli DC2 0.89, VM5d 0.89, VC3 0.88,
VA4 0.88, DC1 0.87, DM2 0.85, VM2 0.84, VM5v 0.83, D 0.82, DM3 0.82, DM6 0.81; MCH glomeruli VM7 0.88, DC3 0.88, VC2
0.88, VA3 0.87, DL4 0.80, DA2 0.80, VA5 0.77, DA4l 0.76, DA3 0.74, DL3 0.57. Schlegel et al. 2021 (hemibrain):
"pheromone-sensitive ORNs (targeting DA1, DL3 and VA1v) are amongst those with the least ALLN input onto their
terminals"; uPNs get 15–70% of their input from ALLNs; the hemibrain truncates D, DA2, DA3, DA4l, VM5d, VM5v and VM7d.
Mohamed et al. 2019: "DL1 is mediating the inhibition of glomeruli DM1 and DM4 via HB4-93-type LNs, while glomeruli DM3
and, to some extent, DM2 are inhibited by DL5 via NP3056-type LNs". Liu & Wilson 2013: glutamatergic LNs (a third of all
LNs) inhibit through GluClα; "glutamate release is concentrated between glomeruli, whereas GABA release is concentrated
within glomeruli".

**MaleCNS v1.0 (derived; 115 GABAergic ALLNs, 286 uPNs).** GABA-LN→ORN synapses per ORN→uPN synapse: median 0.26, range
0.03 (DL3) to 0.60; not correlated with Hong & Wilson's sensitivity (r −0.27 by LN activation, n 15; −0.13 by GABA, n 16).
Share of uPN input from GABA LNs: median 0.116, range 0.072–0.158; correlates with LN-activation sensitivity (r +0.67)
but weakly with GABA sensitivity (r +0.30).

**Per glomerulus** (ORN is DoOR; PN is Badel ΔF/F; S is Hong & Wilson (mean, n); Root is GABA-B R2 intensity / %
suppression; Chou is innervation probability; MCNS pre is GABA-LN→ORN per ORN→uPN synapse; MCNS post is the GABA-LN share
of uPN input):

| glomerulus | ORN OCT/MCH | PN OCT/MCH | S, LN | S, GABA | Root | Chou | MCNS pre | MCNS post |
|---|---|---|---|---|---|---|---|---|
| DC2 | 0.58/0.08 | 74/20 | – | 0.62 (2) | 1.67/89 | 0.89 | 0.31 | 0.148 |
| VM5d | 0.68/0.08 | not imaged | – | 0.21 (3) | – | 0.89 | 0.19 | 0.110 |
| VM5v | 0.59/0.09 | not imaged | 0.37 (1) | 0.19 (2) | – | 0.83 | 0.25 | 0.118 |
| DM3 | 0.47/0 | 219/87 | – | – | – | 0.82 | 0.26 | 0.118 |
| VC3 | 0.43/– | not imaged | 0.43 (7)* | 0.26 (3)* | 0.59/59 | 0.88 | 0.24 | 0.147 |
| DC1 | 0.37/<0 | not imaged | – | 0.54 (1) | – | 0.87 | 0.40 | 0.097 |
| DM2 | 0.34/0.25 | 97/42 | – | – | 0.50/67 | 0.85 | 0.26 | 0.101 |
| DM6 | 0.32/– | 278/88 | 0.45 (6) | 0.62 (2) | – | 0.81 | 0.20 | 0.102 |
| D | 0.74/0.64 | 146/172 | 0.40 (5) | – | – | 0.82 | 0.38 | 0.123 |
| DA2 | 0.24/0.27 | 140/236 | 0.44 (5) | – | – | 0.80 | 0.24 | 0.081 |
| VA3 | 0.12/0.88 | 18/108 | 0.89 (3) | 0.87 (3) | 0.58/27 | 0.87 | 0.32 | 0.157 |
| VM7v | 0.20/– | 106/121 | – | 0.34 (3, "VM7") | 1.35/97 | 0.88 | 0.20 | 0.128 |
| DL4 | 0.12/– | 26/97 | 0.18 (2) | – | – | 0.80 | 0.26 | 0.076 |
| DA4l | –/– | 15/96 | – | – | 0.82/69 ("DA4") | 0.76 | 0.24 | 0.078 |
| DL3 | –/– | 166/91 | – | – | – | 0.57 | 0.03 | 0.080 |
| DA3 / VA5 | –/– | 113/116, 19/110 | – | – | – | 0.74 / 0.77 | 0.37 / 0.14 | 0.144 / 0.108 |

\* Excluded by Hong & Wilson.

**Does it favour MCH? (derived)** Hong & Wilson sensitivity weighted by drive (GABA value where no LN-activation value):
DoOR weights OCT 0.39–0.42, MCH 0.57–0.59 (74% and 88% of drive covered); Barth ORN weights 0.38–0.40 vs 0.58–0.62; Badel
PN weights 0.49–0.51 vs 0.45–0.48 (about 60% covered). Root, weighted by DoOR drive: intensity 1.08 vs 0.70; suppression
76% vs 43% (40% and 48% covered). Static eq.:

| per-glomerulus m | σ 12 | σ 25 | Barth fills, σ 12 | Barth fills, σ 25 |
|---|---|---|---|---|
| uniform | 0.639 | 0.586 | 0.748 | 0.686 |
| m scaled by Hong's S, linear | 0.647 | 0.577 | 0.746 | 0.668 |
| m scaled by S/(1−S) | 0.60–0.61 | 0.52–0.53 | 0.734 | 0.623 |
| m scaled by Root intensity | 0.622 | 0.578 | 0.749 | 0.687 |

Hong & Wilson's S relative to the mean over glomeruli (0.469), if per-glomerulus k is wanted anyway: DA1 2.07, DL2v 2.07,
VA3 1.88, DM5 1.73, DC2 1.32, DC1 1.16, DM6 1.13, DA2 0.94, D 0.86, VM2 0.79, VC3 0.73, VM7 0.73, VC2 0.62, VM5v 0.60,
DC3 0.59, VM5d 0.45, DL4 0.38, DC4 0.10 (S is a slope against light intensity, not a divisive constant).

**Odour-dependent recruitment.** Hong & Wilson: "not all odors were equally efficient at recruiting LN activity, even
when they evoked equal levels of total ORN activity … This difference may reflect the fact that the pentyl acetate
stimulus elicits ORN spiking that is distributed across more ORN types" (ANCOVA p = 0.002). Fig. 3D fit lines (fig.,
approx.): at 1 mV·s LN ΔF/F about 67 (pentyl acetate), 50 (2-butanone), 43 (E2-hexenal); 50% at about 0.3, 1.0 and 1.4
mV·s; the lines converge near 10 mV·s. OCT spreads its input over more ORN types than MCH (12 vs 4 glomeruli above 0.2 in
DoOR; 7 vs 1 above 40% in Barth's ORN imaging). Static eq. if OCT's effective inhibition were ×1.25, ×1.5, ×2: σ 12 0.746,
0.859, 1.107; σ 25 0.676, 0.773, 0.985. Not measured for OCT against MCH.

## 2. Mixtures

- Silbering & Galizia 2007: "no mixture synergism takes place in the fly AL for the mixture of 1-hexanol and
  2-heptanone"; "only two cases of mixture suppression were found in OSNs (both in glomerulus DL5), every glomerulus
  showed suppression for at least two mixtures in the PNs"; their model is "a glomerulus specific network, which includes
  excitatory and inhibitory connections and a PTX sensitive inhibitory global network that acts on all glomeruli with
  proportional strength to the global AL input".
- Silbering et al. 2008: "profile broadening" in "12 of 24 odor/glomerulus combinations, although in most cases only at
  the highest concentration"; in DL5, PN activity with no OSN response "must have been driven by lateral connections
  across glomeruli". No OCT or MCH.
- Asahina et al. 2009 (larva): interactions suppressive only.
- Verdict: apart from lateral excitation (lateral_excitation.md), nothing boosts weak glomeruli or MCH selectively.

## 3. ORN kinetics and adaptation

- Firing-rate time courses for OCT or MCH on any relevant ORN class: Not reported (Martelli 2013, Nagel & Wilson 2011,
  Cao 2016, Montague 2011, Martelli & Fiala 2019, de Bruyne 1999 checked).
- OCT (0.27 mmHg) and MCH (0.29 mmHg) should arrive with similar slow kinetics (Martelli: "all odors with long rising time
  (>100 ms) had low vapor pressure (<1 mmHg)"; inference).
- Steady-state bias (derived): OCT drives ab3B to 245–254 spikes/s and ab6A to 176; MCH stays at 27 or less; with
  adaptation about 0.5 at 500 ms, 500-ms rates overweight OCT relative to MCH by at most about 1.15–1.25×.
- Barth's heat maps re-read: PN MCH/OCT 0.84–0.87 in every window; ORNs 0.52 at the peak, 0.38 with an 8% floor, 0.40
  over the odour, 0.26 integrated; OCT's ORN calcium persists after the odour (VM5 0.64, VM2 0.50, VC3 0.39, DM2 0.33 of
  peak 4–7 s after offset), MCH's does not (VA3 0.02); PNs show no such tail.
- Martelli & Fiala 2019: "glomerular calcium responses do not decrease upon adaptation" (adaptation index ORNs −0.06 ±
  0.1, PNs 0.57 ± 0.1): Barth's ORN ratios are calcium ratios, not firing ratios.
- de Bruyne 1999: "The only other response from pb1B that was significantly different from that of the paraffin oil
  control is the response to 4-methylcyclohexanol"; "The pb3 sensillum contains two neurons that are both excited by
  3-octanol and isoamyl acetate" (pb3 answered only 3 of the first 16 odours, so MCH probably does not excite Or59c/VM7v,
  which bears on VM7v's MCH PN response, Badel 121).

## 4. Imaging nonlinearity

- Only PN calibration: G-CaMP1.3 (Jayaraman & Laurent 2007): "G-CaMP failed to report even sustained (>1 second) activity
  if it was below 30 sp/second or to capture fast modulations of instantaneous firing rate (up to 80 sp/second)"; mean
  ΔF/F against mean rate r = 0.61.
- Badel's supplement has no simultaneous patch and imaging; DA2 reaches 456% for geosmin in the same preparation, so
  hard clipping of OCT's largest values (DM6 278, DM3 219) is unlikely.
- Purified indicator (Chen 2013 SI): GCaMP3 Fmax/Fmin 13.5, Kd 345 nM, Hill 2.54; GCaMP6f 51.8, 375 nM, Hill 2.27.
- Larval NMJ: half-maximum at 54 Hz (GCaMP1.6) and 63 Hz (GCaMP2), Hill about 2.3 (Hendel 2008); GCaMP3 ΔF/F about 0.55,
  1.05, 2.25, 3.35 at 10, 20, 40, 80 Hz (Akerboom 2012, fig., approx.).
- PN dendrites in DC1: GCaMP3 levels off near 3 (3.18 ± 0.90 at 1% octanol); GCaMP6f with 3-octanol 5.3, 6.2, 7.6 at
  10⁻⁵, 10⁻⁴, 10⁻³ (fig., approx.).
- Barth's colour bars may clip: PN bar tops at 260% (OCT's DA2 and DM1 read 256; if really 300–350% the PN ratio would be
  0.76–0.81); ORN bar tops at 97% (OCT's VC3 95, VM5 92; if really 120–150% the ORN ratio would be 0.34–0.38) (derived).
- Compression (derived): with a Hill curve n 2.3 and K 40–100 Hz, a true 0.60 reads as 0.85–0.98 only if OCT's glomeruli
  fire at 100–200 Hz, MCH falls short in rate per glomerulus rather than in number, and K is about 60 Hz or less;
  otherwise 0.37–0.66.
- PN spikes to both odours: Not reported (Turner 2008's PN panel had 3-octanol but no MCH).

## 5. Glomerulus sampling

- NP225 ("labels 37 glomeruli") misses DA4m, DC1, DC4, DL2d, DL2v, DP1l, V, VC3, VC4, VC5, VL1, VM5d, VM5v and VP1–4
  (OCT glomeruli missing: DC1, VC3, VM5d, VM5v; MCH glomeruli missing: none).
- GH146 negative (Grabe Table S1): DA3, DA4m, DC4, DL2d, DL2v, DP1l, VC3, VC4, VC5, VL1, VM5d, VP1+VM6, VP4; VM5v counted
  with ChA-GAL4, implying GH146 misses it too. Barth's 18 PN glomeruli lack OCT's VC3, VM5d/v, DM3, DC2, VA4, VM3, D, DC3.
- Badel on other sets (derived): Barth's set 0.82 (1109/1349); Prisco's 9-glomerulus plane 0.67; the 19 glomeruli Barth
  did not image 1.20.
- Prisco 2021's own antennal-lobe PN imaging (GH146 > GCaMP6m, one plane): MCH about 30 vs OCT about 76 %max, 0.40 (n 10,
  p 0.002; fig., approx.); its bouton counts (0.98) come from NP225 and share its blind spot.
- PN data for VM5d, VM5v or VC3 with either odour: Not reported (Endo 2020 on request only).
- On matched glomeruli the remaining mismatch is breadth (Badel: DL3 166/91, DA3 113/116, DA4l 15/96, VA5 19/110 OCT/MCH;
  VM2 171 to OCT; DM6 88 and DM3 87 to MCH); the unfilled model gives −3 to −2 Hz in all of these.

## 6. Downstream normalization (Prisco 2021, fig., approx.)

- APL calcium: MCH about 43 vs OCT about 88 %max (0.49); "Δ(Oct-Mch) = 45% ± 27%".
- PN boutons: about the same number active (0.98), lower peaks for MCH (0.69).
- KC claws (MB247-homer::GCaMP3): APL working: peaks about 63 vs 71 (0.89, p 0.949), claws responding 17.5 vs 18.5; APL
  silenced with TeTx: peaks about 115 vs 177 (0.65, p 0.0003), claws 21 vs 27.5 (p 0.047).
- Lin 2014: "APL>GADRNAi manipulations do not affect the sparseness of, or correlation between, Kenyon cell
  representations of MCH and OCT"; values for the pair itself Not reported. Inada 2017: neither odour tested.
- The model (probe54): KCs 0.25; MBON11 25 vs 8.2 spikes (flies 118 vs 110).

## 7. Other things that could boost weak glomeruli

- Convergence slightly favours OCT: ORNs per side, drive-weighted, MCH/OCT: FlyWire ♀ 0.75–0.89, Grabe 0.91–0.97, model
  0.76–0.89; MaleCNS both sides, DoOR-weighted: 44 vs 38.5 ORNs per glomerulus and 1831 vs 1623 ORN→uPN synapses per uPN
  (OCT vs MCH). Grabe's Gal4-based counts look unreliable here (DM2 8 vs FlyWire 27; VM5d 8 vs 33.5; VC3 47.5 vs 15.5).
- PNs per glomerulus: weighting Badel by uPN count gives 0.93–0.95 (0.929 with MaleCNS counts).
- Spontaneous ORN rate, drive-weighted: OCT 10.0 vs MCH 6.7 Hz (DoOR weights), 13.0 vs 12.7 (Barth weights); a high
  spontaneous rate does not lower gain in flies (DL5 at 14–20 Hz has σ 11.8, DM4 at 3.4–11 Hz 16.3).
- Synapses: Kazama & Wilson 2008: unitary current "matched to the size of its dendritic arbor … to produce uniform
  depolarization across PN types" (DL5 7.0, DM4 6.9, DM6 5.5, VM2 5.4 mV; no MCH glomerulus measured); the model gives
  DM6 7.0 and VM2 9.0 mV, slightly favouring OCT.
- Receptors never tested with MCH: cyclohexanol drives Or43a (DA4l) at 0.51 (spontaneous 0.10), Or85f (DL4) 0.23, Or2a
  (DA4m) 0.19, Or23a (DA3) 0.13 (DoOR); Störtkuhl & Kettler 2001: Or43a's ligands "cyclohexanol, cyclohexanone,
  benzaldehyde, and benzyl alcohol". DC3 (Or83c) data conflict: Grabe Table S3 MCH −1 and OCT 9 spikes/s; DoOR's
  Ronderos 2014 entry MCH 17 and OCT 10.

## Suggested checks on the model

1. Score PN-level equalization over Badel's 37 and Barth's 18 glomeruli (probe54 already gives 0.86 and 0.82; filled 0.93
   and 0.76).
2. Compare breadth on the NP225 set (flies: 13 vs 18 significant; 14 vs 19 above 50% ΔF/F).
3. Plot the model's GABAergic LN rates for OCT and MCH against summed ORN rate; if OCT recruits no more inhibition per
   unit of input than MCH, that is the one antennal-lobe lever left.
4. Test the KC/APL stage against Prisco's claw numbers.
