# Courtship song: the circuit, its activity and the numbers a "pulses about 35 ms apart" test needs

Read 2026-10-11. Groundwork for rung 8's song criterion ("song pulses about 35 ms apart"): drive the song command
neurons in brainfly's MaleCNS model and ask whether wing motor neurons fire in pulse-like events spaced like flies'
inter-pulse interval (IPI). Wing power muscles and their splay state are in `dlm_splay_state.md`; descending/VNC
background is in `../Embodied fly connectome simulation/descending_vnc_motor.md`.

## Summary: what a model test should use

1. **IPI target (natural song, ~25 °C): 34–35 ms, accept about 30–40 ms.** Stern's Canton-S data (88 flies, 360,155 IPIs in his 15–65 ms window; my reanalysis [SD→D]): pooled mean 34.4 ms, SD 7.5 (CV 0.22), mode ≈31 ms, 5–95% 25.4–50.2 ms. Per-fly means are 34.6 ± 1.8 ms (31.6–39.4), and 59% of IPIs fall in 30–40 ms. Reviews give "15 to 80 ms but usually averages between 30 and 40 ms".
2. **IPI depends on temperature at about −1 ms/°C.** Canton-S courting: 30.9 ± 0.5, 27.9 ± 0.4 and 25.5 ± 0.4 ms at 27.5, 30 and 33 °C (von Philipsborn 2011). That is a Q10 of ≈1.4 for pulse rate and ≈33 ms extrapolated to 25 °C [D]. A model without temperature should use the ~25 °C value.
3. **Driving pIP10 gives near-natural IPIs that do not track drive.** TrpA1 at 29/31.5/33 °C gave 33.3/34.1/35.4 ms, while pulses/min rose 25 → 246 → 286 (von Philipsborn Table 1). P1 activation gives 28.4–33.7 ms. Activating thoracic neurons gives abnormal IPIs: dPR1 ≈46 ms at any drive; vPR6 36–68 ms, falling 5.4 ± 0.7 ms/°C with stronger activation; all fru neurons 51–56 ms (males) and 65–73 ms (females).
4. **Pulse shape.** 1–2 cycles (natural CPP 1.01–1.02) at ≈220 Hz: Pslow 200–250 Hz, Pfast 250–400 Hz. One cycle is ≈4.5 ms [D]. Sine song is ≈150 Hz (continuum 120–180). Trains are "2–50 pulses". In Stern's data the median train is 4 pulses (IQR 3–7) lasting 108 ms [SD→D]; his detector found only ~50% of manually logged IPIs, so these trains are too short.
5. **Drive pIP10.** One neuron per side: MaleCNS bodyIds 11116 (R) and 523998 (L); MANC 13038 and 13417. Fly activation sufficiency and necessity: activation starts wing extension with 0.08 ± 0.04 s latency, locked to the light. It drives pulse song in decapitated flies, and silencing cuts both pulse and sine song. An optional pulse-specific second command is pMP2 (10765 R, 10930 L). Its Ca rises during pulse song and falls during sine.
6. **VNC core.** Lillvis' eight core types, with MaleCNS counts: pIP10 (2), pMP2 (2), dPR1 (2), dMS9 (2), vMS12 (18), TN1A (22), dMS2 (20) and GABAergic vPR9 (9). The sine net is the subset pIP10 + TN1A + dMS2 + vPR9. Activity: dPR1 and pMP2 are active only in pulse song; TN1A-2, pIP10 and vPR9 are active in both modes.
7. **Read wing MNs.** During pulse song i1 and hg1–4 are reliably active, b1 and b2 are silent, and b3 is asymmetric (muscle Ca). Ewing's EMG: DLM, DVM2–3 and axillary potentials come "18 ms before each sound pulse"; DVM1, basalar and sternobasalar fire "3 ms after the onset". Power-muscle firing is tonic, with ISI ≈ 2 × IPI (≈14 Hz [D]). It is not phase-locked, and its rate tracks amplitude (r² 0.81), not IPI (r² 0.02).
8. **MaleCNS wiring to MNs [D].** Share of each MN's input from the core: hg1 13.8% (dMS2 3657, dPR1 593, TN1A 484 synapses), hg3 12.2%, MNwm35 (≈iii4) 9.4%, hg4 7.0%, ps1 5.4% (almost all vMS12), b3 2.1% (dPR1), i1 0.9%, DLMn 2.7–3.0% (TN1A). pIP10 makes only 12 synapses directly onto MNs.
9. **Where the rhythm comes from is unknown.** No recording resolves single pulses in any interneuron; Ca imaging ran at 7.1 volumes/s. The IPI is central, not set by feedback: Ewing found vestigial-winged flies still fire IFM potentials at song IPIs, and removing the antennae left the timing unchanged. It is thoracic: VNC activation and decapitated pIP10 drive both sing, and vPR6 activity sets the IPI under activation. No focal-cooling experiment exists.
10. **Controls (fly results to match).** Silencing dPR1, vMS12, dMS9 or pMP2 cuts pulse song; silencing TN1A cuts sine but leaves pulse song. Driving vPR6 should lengthen the IPI in a drive-dependent way, and driving dPR1 should give a long IPI that ignores drive. Co-driving pIP10 + vPR9 gives "almost entirely" sine. Removing the brain should not stop pIP10-driven pulses. A degree-preserving shuffle should abolish the IPI structure.
11. **Blockers.** The model has no wing mechanics: no carrier, and a "pulse" must be defined from MN spikes. There are no gap junctions (dMS2 may signal mostly electrically; pIP10 electrical synapses are proposed), no Ih/rebound (TN1) and no pIP10 adaptation. Whether song premotor neurons spike or are graded is unknown. In brainfly vMS11 is inhibitory (glutamatergic) and dMS9 is named `AN_GNG_SAD_23` (flywireType wins). TN1A-1/-2 do not map onto MaleCNS TN1a subtypes. vPR9's presynaptic inhibition of pIP10 terminals becomes somatic inhibition in point neurons.
12. **Prior models.** None reproduces the IPI. Roemschied et al. built a hand-built 4-node spiking model that fits bout statistics. flymsg (GitHub) is a MaleCNS LIF that reports only pathway rates (pIP10 → dPR1 ≈88 Hz) and says not to read exact firing from it.

Conventions:
- [P] stated in the peer-reviewed paper (quoted where wording matters).
- [PP] a preprint.
- [A] abstract only (full text not obtained).
- [2°] stated by a later paper about an earlier one, not checked in the original.
- [SD→D] my reanalysis of the authors' published data.
- [D] my calculation or my query of the local MaleCNS v1.0 tables (`~/fly-data/raw`, minconf 0.5; synapse counts summed over both sides unless stated).
- [M] a model value.
- Temperatures are as reported; "TrpA1 at X °C" means thermogenetic activation at that ambient temperature.

**Note (2026-10-11, after a review).** Summary 11's "dMS2 may signal mostly electrically" overstates §7: Lillvis et
al. list the dMS2 neurons "amongst the more prominent" ones whose electrical synapses connectomes miss. "Mostly" is
unsupported, and dMS2 also makes thousands of chemical synapses onto hg1, hg3, hg4 and MNwm35.

## 1. von Philipsborn et al. 2011, Neuron 69:509 ("Neuronal control of Drosophila courtship song") [P]

Read in full: Cell Press PDF via the Wayback Machine.

- **Approach.** A TrpA1 activation screen of 794 GAL4 lines crossed into `fruFLP UAS>stop>trpA1`, run on isolated, intact males warmed from 25 to 32–33 °C. Songs were recorded 3.5–4 min at fixed temperature (Peltier chamber). Silencing used `UAS>stop>TNT` in males paired with Canton-S virgins.
- **Analysis.** LifeSong settings: "IPI, 15–100 ms; minimum train length, 2 (for pulses/min) or 3 (for IPI)". IPI and CPP are "grand mean ± SEM, i.e., the mean of the mean per fly".
- **Background numbers (Introduction).**
  - Sine song: "fundamental frequency of 140–170 Hz".
  - Pulse song: "a train of 2–50 pulses, each containing one to three cycles … with a carrier frequency of 150–300 Hz. Pulses are separated by a pause that lasts an average of 35 ms".
- **Activating all fru neurons.** It gives "somewhat longer IPIs than normal": 55.7 ± 1.5 ms (fruGAL4 > TrpA1, 27.5 °C, n = 14 males).
  - Females: 72.8 ± 1.6 ms at 29 °C (n = 14). 11% ± 4% of their pulses had more than two cycles, against 2% ± 1% in males.
  - Females needed more drive (above 28.5 °C, against 26 °C for males).
  - With `nsyb-GAL4 fruFLP`: males 51.2 ± 1.9 ms at 29 °C (n = 10); females 64.7 ± 2.2 ms at 32 °C (n = 8), with 64% ± 6% of their pulses polycyclic.
  - With P2X2, robust singing was seen "only … with beheaded flies (Clyne and Miesenböck, 2008)"; with TrpA1, intact flies also sang.
- **Table 1 (TrpA1 activation; IPI and CPP are grand means ± SEM; n = flies, with IPIs or pulses in parentheses):**

| Class (GAL4) | T | Singers | Pulses/min | IPI (ms) | CPP |
|---|---|---|---|---|---|
| P1 (NP2361) | 30.0 °C | 63% of 35 | 4.2 ± 0.8 | 28.4 ± 0.7 (11; 311) | 1.01 ± 0.01 |
|  | 31.5 °C | 100% of 16 | 57.9 ± 11.4 | 29.4 ± 0.4 (16; 1850) | 1.00 ± 0.00 |
|  | 33.0 °C | 89% of 19 | 84.2 ± 10.7 | 33.7 ± 0.6 (16; 2567) | 1.00 ± 0.00 |
| pIP10 (VT40556) | 29.0 °C | 100% of 20 | 25.1 ± 4.9 | 33.3 ± 0.6 (14; 722) | 1.01 ± 0.01 |
|  | 31.5 °C | 100% of 16 | 245.8 ± 29.9 | 34.1 ± 0.7 (14; 6965) | 1.09 ± 0.02 |
|  | 33.0 °C | 100% of 15 | 285.7 ± 26.8 | 35.4 ± 0.7 (15; 6875) | 1.13 ± 0.06 |
| dPR1 (VT41688) | 31.5 °C | 43% of 35 | 21.3 ± 4.9 | 46.3 ± 0.9 (10; 522) | 1.01 ± 0.00 |
|  | 33.0 °C | 63% of 35 | 34.8 ± 7.0 | 45.7 ± 1.0 (16; 1308) | 1.01 ± 0.00 |
| vPR6 (VT19579) | 27.5 / 29 / 31.5 °C | 95/100/100% | 30.4 / 105.7 / 168.1 | 63.1 / 59.0 / 43.5 | 1.31 / 1.19 / 1.18 |
| vPR6 (VT5534) | 29 / 31.5 °C | 100/100% | 123.0 / 144.5 | 60.1 / 40.5 | 1.36 / 1.22 |
| vPR6 (VT57239) | 29 / 31.5 / 33 °C | 100% | 98.6 / 246.4 / 78.0 | 60.6 / 43.0 / 36.2 | 1.29 / 1.32 / 1.23 |
| vPR6 (VT46099) | 29 / 31.5 / 33 °C | 95/94/100% | 15.7 / 44.4 / 122.9 | 68.3 / 60.6 / 47.7 | 1.18 / 1.18 / 1.31 |
| vPR6 (VT17258) | 30 / 31.5 / 33 °C | 72/100/100% | 10.8 / 104.6 / 118.0 | 67.9 / 61.5 / 59.1 | 1.13 / 1.23 / 1.13 |
| wild-type courtship (Canton-S male + virgin) | 27.5 / 30.0 / 33.0 °C | – | – | 30.9 ± 0.5 (11; 645) / 27.9 ± 0.4 (11; 692) / 25.5 ± 0.4 (8; 606) | 1.02 / 1.01 / 1.01 |

- **IPI and temperature.** "IPIs decreased markedly with temperature for all five vPR6 GAL4 lines … at a rate of 5.4 ± 0.7 ms/°C. The mean IPI of natural song also decreases slightly with temperature (Shorey, 1962), but only at a rate of 1.0 ms/°C within this temperature range".
  - "IPIs did not decrease with temperature with any of the GAL4 lines that trigger songs by activating neurons other than vPR6 … particularly notable in the case of dPR1".
  - They read this as "a tight inverse coupling between vPR6 activity and the IPI".
  - [D] Regression on the wild-type row gives −0.98 ms/°C, 33.1 ms at 25 °C and a pulse-rate Q10 of 1.42.
  - [D] The pIP10 rows rise +0.50 ms/°C and the P1 rows +1.8 ms/°C. Activation-evoked IPIs therefore do not follow the natural temperature trend. They are 6–10 ms longer than natural song at the same temperature (30–33 °C).
- **Single-cell identification (stochastic TrpA1myc).**
  - P1: "Clusters of at least 10 individual P1 neurons were labeled in all of the singers (62/62)". The class has "15–20 individual … neurons per hemisphere".
  - pIP10: labeled "in all singers and in none of the nonsingers"; bilateral labeling gives more song (p = 0.009).
  - dPR1: labeled in all 57 singers and bilateral in 52/57 (only 7/54 of nonsingers).
  - vMS11: associated with ipsilateral wing extension (40 of 44 unilateral cases).
- **Silencing (TNT).**
  - P1 (NP2361), pIP10, dPR1 and vPR6 (VT19579, VT5534) lines: each cut song and copulation.
  - dPR1-silenced males "extend their wings but do not produce pulse song".
  - VT43702 (vMS11 + dMS2 + vMS12 + brain cells): fewer than half sang, IPIs were "significantly longer than normal", and 59% ± 4% of pulses had more than two cycles (<3% in controls).
- **Morphology and counts (light level).**
  - pIP10: one per side, soma in the posterior brain, nsyb-GFP only in the VNC, arborizing "within the wing neuropil of the anterior mesothoracic ganglia".
  - dPR1: one or two prothoracic somata; Dsx+; never seen in VT41688 females.
  - vPR6: 2–5 per hemisphere; Dsx+; "may represent a subclass of the dsx+ TN1 neurons".
  - vMS11: 2.9 ± 1.3 per hemisphere.
  - P1, pIP10 and dPR1 are male-specific. pIP10 and vMS11 do not express dsx.
- **Proposed circuit (from arbor overlap, not synapses).** P1 → pIP10 → dPR1 and vPR6, with dPR1 → vPR6 likely. "P1 and pIP10 … trigger but do not pattern the song". dPR1, vPR6 and vMS11 are "components of a central pattern generator that times and shapes the song's pulses".
  - [D] MaleCNS does not support the vPR6 links: pIP10 → vPR6 is 65 synapses (0.5% of vPR6 input) and dPR1 → vPR6 is 45 synapses (§12).
- **Wing choice.** Unilateral P1 or pIP10 activation gives no ipsi/contra wing bias.

## 2. Clyne & Miesenböck 2008, Cell 133:354 [A + 2°]

- Abstract: light-activated channels in fru neurons of "the thoracic-abdominal ganglia" initiate "the unilateral wing vibrations that normally generate the male courtship song". The circuit produces "wing movement and sound in both [sexes] but authentic songs only in males and in females expressing male fru product". "A song-like motor program is thus present in females but lies dormant".
- [2°] Robust song with P2X2 photoactivation needed beheaded flies (von Philipsborn 2011). The resulting pulse songs had longer than normal IPIs, as did those from TrpA1 activation.
- The full text was not obtained; the paper's headless IPI values are not in these notes.

## 3. Shirangi, Stern & Truman 2013 (Cell Rep 5:678) and Shirangi et al. 2016 (Dev Cell 37:533)

**2013** [A + full text via a PMC page summary, quotes as returned]:
- hg1 is "uniquely male-enlarged". "The hg1 motoneuron and the sexually dimorphic development of the hg1 muscle are required specifically for the sine component".
- The ps1 MN "is required specifically for a feature of pulse song". Kir2.1 in ps1 reduced "pulse carrier frequency and pulse amplitude".
- Kir2.1 in both hg1 MNs: "most males … displayed a complete absence of sine song". Pulse song was unchanged "including inter-pulse intervals, pulse carrier frequencies, pulse amplitudes, pulse shapes, and pulse train lengths".
- Recording: 10–15 min "at 25°C".

**2016** [P, full text via archived HTML]:
- TN1: "approximately 30 TN1 cells on each side". They derive from hemilineage 12A and are male-specific.
- TN1 silencing (TNT): "almost no sine song, but … plentiful pulse song", with "quantitative defects in the inter-pulse interval".
- Activating all TN1 gave song "composed almost exclusively of sine song".
- TN1A (11.8 ± 1.1 cells per intersection, n = 6): silencing cut sine but left "normal pulse song". Activating these TN1A alone "failed to induce much song" (Lillvis and Shiozaki later got sine from other TN1A lines; §§8–9).
- TN1A → hg1: Chrimson in TN1A gave "rapid and strong increases" of GCaMP6s in the hg1 MN in explants. This requires dsx in TN1A during development, which raises arbor density where the hg1 dendrites are.
- dsx mutants: no sine, and pulse IPI, carrier and amplitude defects.
- vPR6 is also from 12A and distinct from TN1A. Activating vPR6 did not induce sine; silencing it modestly reduced sine.
- TN1C silencing gave "a variety of song defects", and TN1C is not functionally linked to hg1.

## 4. O'Sullivan et al. 2018, Curr Biol 28:2705 (main text via Wayback PDF; supplement from CaltechAUTHORS) [P]

- **Song description.** "In pulse song, single wing beats with a frequency of around 220 Hz produce acoustic pulses. These are spaced at interpulse intervals (ipis) of 30–40 ms". Sine is "continuous wing oscillations of around 150 Hz, which can be several seconds long". "Wing vibration during courtship song is lower in amplitude compared to flight."
- **Muscle Ca (GCaMP6f through the cuticle; tethered males on a ball, pIP10 > ReaChR; n = 7 flies).**
  - On group: "the hg1–4 and i1 muscles were reliably active during pulse song".
  - Off group: "The b1 and b2 muscles were silent".
  - Variable group: "iii3, iii4, and i2". iii1 is intermediate.
  - b3 is asymmetric, more correlated with pulses on the folded-wing side.
  - The b1–3 muscles show "no or low activity during pulse song bouts" but are strongly active in flight; hg1–3 show the reverse.
  - "i1 and iii1 consistently decreased when flies switched from pulse to sine song". In the supplement this held in all 3 flies (n = 69 sine episodes, p < 0.0001).
  - Muscles were active on both sides regardless of which wing sang.
  - pIP10-triggered song was "close to natural, but pulse frequency is slightly decreased and percentage of polycyclic pulses slightly increased".
- **MN silencing (TNT; 20–40 flies per genotype; IPIs counted 15–80 ms in trains of >2 pulses).**
  - tpn MN: "complete loss of courtship song". tp1 and tp2: fewer males sang.
  - hg1 and hg2: less sine; with hg1 silenced the remaining sine had a higher carrier.
  - i2, ps1, tt and dlm: lower pulse carrier.
  - IPI: "spacing of pulses within trains (ipi) was altered in flies with silenced i2, hg1, or hg2 MNs. Whereas control flies sang with the majority of ipis between 30 and 40 ms, these genotypes produced fewer ipis in the 30- to 40-ms range and more ipis above 40 ms".
  - Polycyclic pulses increased with i2, hg1, hg2, ps1, tp1, tt and dlm silenced. Amplitude fell with hg1, tp1, tt and dlm.
  - b2 silencing changed nothing.
- **Their model.**
  - "i1 and i2 control pulse length, possibly contracting at the end of each pulse". "Pulse frequency is set by ps1 activity". Amplitude comes from "concerted action of tt and dlm"; "tp2 might also initiate pulses".
  - On Ewing's per-pulse b2 firing they "speculate Ewing may have misidentified i1 as the overlapping b2".
- **Flight is dominant.** pIP10 activation does not start song in flying flies (14/15 kept flying). Loss of ground contact starts flight despite pIP10 activation (10/11).
- **Octopamine.** Activating octopaminergic neurons stops song, including pIP10-evoked song, and raises flight amplitude.

## 5. Ewing 1977 and 1979 (EMG during song) and Coen et al. 2016 (IFM recording) [A, 2°, P]

- **Ewing 1979, Physiol Entomol 4:329 [A, via Crossref].**
  - "The dorsal longitudinal, second and third dorsal ventral and axillary muscles show potentials 18 ms before each sound pulse while the first dorsal ventral, basalar and sternobasalar muscles fire 3 ms after the onset of each pulse."
  - Timing "remains unaltered in animals with the antennae removed".
  - "Courting vestigial flies, in the absence of detectable wing base movements, produce indirect muscle potentials at the appropriate song inter-pulse intervals. Thus proprioceptive feedback is also unimportant in determining the intervals between pulses."
  - Basalar timing becomes abnormal in vestigial flies and phase-locks to an externally driven wing: "the timing of those muscles which fire at the beginning of the sound pulses is set by proprioceptive feedback".
- **[2°] As cited by Coen et al. 2016.** "the 13 IFMs (Ewing, 1977) fire tonically with an inter-spike-interval roughly double the IPI (Ewing, 1979)". "direct flight muscles spike in time with each song pulse".
- **[2°] As cited by Lillvis et al.** Power muscles are "sporadically but rhythmically active during both pulse and sine song". Each steering muscle "is innervated by a single motor neuron that fires one-for-one with muscle contraction".
- The original 1977 and 1979a (J Comp Physiol) full texts were not obtained.
- **Coen et al. 2016, Neuron 89:629 [P].**
  - "flies rapidly modulate individual pulses … separated by IPIs of ~35ms". Pulse amplitude changes within 30 ms of a light-level drop.
  - Extracellular IFM recordings in P1-activated (laser-heated TrpA1) males showed no "precise phase-locking between spiking of individual IFMs and song pulses". IFM rate correlated with pulse amplitude (r² = 0.81) but not IPI (r² = 0.02; n = 6 flies).
  - Thermogenetic activation (~33 °C): P1Act and pIP10Act males kept amplitude modulation with distance; dPR1Act reversed it; vPR6Act sang at constant amplitude.
  - Their reading: visual distance information enters "downstream of the pIP10 but upstream of the dPR1 neuron". They found "no correlation between IPI and pulse amplitude during courtship".
  - P1 is "a subset of ~20 neurons in the doublesex-expressing pC1 neural cluster".
- [D] An ISI of 2 × 34.4 ms is 68.8 ms, or ≈14.5 Hz per IFM unit during pulse song. That is about 2–3× the 4.5–8 Hz DLM rates in tethered flight (see `dlm_splay_state.md`) and half the ~29 Hz pulse rate.

## 6. Clemens et al. 2018, Curr Biol 28:2400 (Pslow/Pfast) [P]

- **Three song modes in NM91 males (47 males; ~20,000 normalized 25-ms waveforms).**
  - Sine: "a continuum of carrier frequencies between 120 and 180 Hz".
  - Pslow: "slow (200–250 Hz) and symmetrical".
  - Pfast: "biphasic (asymmetric) with faster oscillations (250–400 Hz)".
  - Pslow is sung with one wing at ≈60°, Pfast mostly at ≈20°.
  - Pulse detection rate: "78% for all pulses".
- **Pfast is louder** and chosen at larger male–female distance. Blind males sing more Pfast. 42 ± 11% of pulse trains are single-type, against 10 ± 7% shuffled.
- **Optogenetic activation (CsChrimson 0.46 mW/mm², 3-s period, duty cycle 0.1–0.9; solitary males).**
  - P1 (R71G01 or P1a) mainly drives sine.
  - pIP10: "Pfast, and not sine song, was the dominant mode produced during optogenetic activation". Sine dominated only after stimulus offset.
  - vPR6 "drives only pulses (and no sine)", with Pfast early and Pslow late.
  - Cell counts: "P1, a cluster of ~20 central brain neurons per hemibrain"; "vPR6, a set of ~5 thoracic interneurons per side".
- **Silencing.** pIP10 Kir2.1 or TNT increased the Pslow fraction. ps1 TNT reduced the switch to Pfast with distance and lowered amplitude, though "~10% of pulses are still of the Pfast type".
- **Raised at 25 °C.** No IPI numbers are given in this paper.

## 7. Lillvis et al. 2024, Curr Biol 34:808 ("Nested neural circuits generate distinct acoustic signals during Drosophila courtship") [P/PP]

The journal is Current Biology, not eLife. The journal text was blocked. I read the CC-BY bioRxiv v1 (1 Sep 2023, titled "The Neural Basis of Drosophila Courtship Song") via the Wayback Machine. Wording and numbers may differ in the published version.

- **Scale and methods.**
  - "over 40 distinct cell types … more than 1800 hours of songs from over 5000 male flies"; 58 split-GAL4 lines.
  - GtACR1 silencing in courting males; CsChrimson activation in isolated and in courting males; 0.3–42 µW/mm².
  - Isolated males: 10 s on / 10 s off. Courting males: 3 s on / 10 s off.
  - Raised at 25 °C. Audio at 5 kHz. SongExplorer precision/recall: pulse 89%/81%, sine 93%/98%.
  - Song features: "mode inter-pulse interval", mode pulse frequency, cycles per pulse, and others.
- **Song description.** "trains of discrete ~220 Hz pulses that recur every 35 milliseconds, and a continuous ~150 Hz hum called sine song".
- **Core eight and their roles.**
  - Sine: silencing TN1A or dMS2 cut sine but "did not significantly alter the amount of pulse song". Activating either gave sine (TN1A sine persisted the whole 10 s).
  - Pulse: silencing pMP2, dPR1, dMS9 or vMS12 cut pulse song. With dMS9 and dPR1 silenced, sine increased.
    - pMP2 activation: "normal pulse trains that lasted for only a few seconds after stimulus onset".
    - dPR1 activation: "Normal pulse trains were produced for up to 5 seconds of a 10 second activation window".
    - dMS9 activation: pulse and sine "for up to ~2 seconds", with polycyclic pulses.
  - Multimodal: pIP10 silencing "acutely and significantly reduced the amounts of both pulse and sine song".
    - pIP10 activation in isolated males "elicited normal pulse trains throughout the stimulus duration … often interspersed with short bouts of sine song".
    - In courting males, low intensities raised both modes. High intensities raised pulse "at the expense of sine song".
  - vPR9 (GABA): effects differ by driver. vPR9-SS1/-SS2 (1–2 cells) mainly cut pulse; -SS3/-SS4 cut sine; -SS5 cut both. Silencing with -SS5 cut both.
  - Not core: dMS5 and vPR6 gave pulse-like song when activated but had no silencing effect. "for vPR6, activation in courting males tended to reduce rather than increase pulse song".
- **IPI.** "silencing or activating any of the three cell types vPR9, dPR1, or vMS12 altered the inter-pulse interval". Among the non-core types, "AN08B114 is the only non-core neuron that altered the inter-pulse interval when silenced".
  - No IPI values are given in the text. Fig. 7C (dPR1 > GtACR1) plots IPIs on a 26–38 ms axis.
  - Female receptivity neurons are "tuned to the D. melanogaster inter-pulse interval of ~35ms (Wang et al., 2020)".
- **MANC counts.**
  - "11 TN1A neurons in each hemisphere".
  - dMS2: "a bilateral subtype represented by twelve neurons and a unilateral subtype consisting of six neurons".
  - vMS12: "14 bilateral and 6 unilateral vMS12 neurons".
  - vPR9: "7 vPR9 neurons".
  - "eight fru+ and/or dsx+ … cell types", with "A further 5-10 cell types" shaping features.
- **Structure.** "two largely feed-forward excitatory networks". Sine: pIP10 → TN1A → dMS2. Pulse: these plus pMP2, dPR1, dMS9 and vMS12.
  - Recurrent links: "TN1A makes strong recurrent connections with dPR1". vPR9 makes "strong recurrent connections with dPR1, TN1A, and pIP10". vPR9 provides "presynaptic inhibition to the pIP10 descending 'command' neurons".
  - "the eight core song cell types … receive almost half of their synaptic input from other members of this group".
  - MANC v1.0 threshold: 10 synapses per neuron pair.
- **Motor output (MANC).**
  - "Most direct core song circuit output to the power muscle (DLMs and DVMs) motor neurons is made by TN1A". "TN1A serves as the primary output of the core song circuit to the power muscles".
  - "i1, iii1, and b3 MNs are exclusively innervated by core neurons that were necessary to produce pulse but not sine song".
  - hg1–4, i2 and MNwm35 (likely iii4) get their strongest input from dMS2 and TN1A.
  - "no strong connections from the core song circuit to the b1 or b2 motor neurons".
  - "the ps1 motor neurons are innervated almost exclusively by vMS12". tp1 and tpn get weak input from TN1A and dMS2; tp2 gets none.
- **Switching.**
  - Uncharacterized inhibitory candidates (MANC v1.0 names): IN11B003, IN03B021 and IN06B044.
  - Descending inputs: DNxl080 and DNxl048 go to TN1A and dPR1. DNxl058 and DNfl038 go to dPR1. DNxn031, DNxn088, DNxn078 and pIP9 go to TN1A and vPR9.
  - "coactivation of pIP10 and vPR9 indeed results in a courtship song composed almost entirely of sine song".
- **Limitations they state.**
  - Connectomes miss electrical synapses, and "amongst the more prominent of these neurons in the male VNC are the dMS2 song neurons".
  - "Electrophysiology … will be considerably more challenging … due to the very wing vibrations it seeks to explain".
  - "a useful goal will be to construct computational models of the song circuit". None was built.

## 8. Shiozaki et al. 2024, Nat Neurosci 27:1954 ("Activity of nested neural circuits drives different courtship songs") [P]

- **Preparation.**
  - Two-photon imaging of the VNC in singing tethered males, glued by the legs with the ventral thorax opened. Song was induced by the "song driver" R22D03-LexA > CsChrimson, which includes P1.
  - Imaging at 7.1 volumes/s (10 planes) for song-driver runs, binned to 141 ms. When pIP10, dPR1 or TN1A-2 were the activated neurons, imaging ran at 1.4 volumes/s (30 planes).
  - Song classified every 1.6 ms (SongExplorer). A "pulse train" merges "pulse events with inter-pulse intervals of 50 ms or shorter".
  - Flies raised at 23 °C, recorded at 23 °C and 50% RH.
  - [D] Imaging cannot resolve single pulses (one bin spans ≈4 IPIs).
- **Decapitation.** "Removal of the head eliminated the production of song during optogenetic stimulation" with the song driver (n = 4 intact vs 6 decapitated). "optogenetic activation of pIP10 … in the same preparation elicited song in decapitated flies" (n = 5).
- **dPR1 (2 neurons).** "selectively active during pulse". Ca rose sine→pulse and fell pulse→sine (10 flies; 1,092 and 429 transitions). During sine, Ca decayed as it did after stimulus offset.
- **TN1A-2.** "active during both pulse and sine song with a preference for sine". Simultaneously recorded TN1A-2 cells were highly correlated.
- **TN1 (dsx-Gal4, ~22 per hemisphere).**
  - 56 of 89 responded; 38 of 56 preferred a mode, 25 of them sine.
  - Under pIP10 drive, 76 of 77 responsive TN1 rose during pulse song.
  - This contradicts the earlier anti-correlated responses; see Roemschied, §9.
- **Pan-neuronal and fru imaging.** Most active voxels were similar in both modes. Mode-selective voxels mostly preferred pulse (meso-thoracic triangle, dorsal VNC). Removing GCaMP from fru neurons abolished most of the selectivity.
- **Brain recordings of descending neurons (fly on a ball).** pIP10 was similar in both modes with a weak pulse preference. pMP2 was "strongly selective for song type", rising in pulse and falling in sine. "pIP10 neurons encode whether to sing or not, while the activity of pMP2 neurons contributes to specifying whether to sing pulse song". vPR9-SS1 and -SS3 were active in both modes.
- **Activation in courting males.** pIP10 raised both modes. pMP2 and dPR1 raised pulse and lowered sine. TN1A-2 raised sine only. pMP2, dPR1 and TN1A-2, but not pIP10, changed switch probabilities.
- **Connectome (MANC; all cholinergic).**
  - "only two neurons, one per hemisphere, for pIP10, pMP2 and dPR1"; "24 neurons whose morphology matched TN1A".
  - TN1A splits into TN1A-1 and TN1A-2. pIP10 and pMP2 both strongly target dPR1 and TN1A-1. TN1A-2 gets "substantial input from pIP10 but not from pMP2 or dPR1".
  - Hypothesis (not measured): "pIP10 input may set the membrane potential of dPR1 close to the spiking threshold".
- **Supplementary Data 1 (MANC bodyIds).**
  - pIP10: 13038, 13417. pMP2: 11977, 11987. dPR1: 10267, 10300.
  - TN1A-1 (10): 15521, 16465, 15148, 12883, 16207, 16113, 14581, 14810, 15387, 17640.
  - TN1A-2 (14): 13945, 14401, 13928, 16391, 16042, 13155, 13445, 14277, 14375, 14779, 16690, 15936, 13727, 13514.
  - The MaleCNS mapping of these ids is in §12.4.
- **Data and code.** Figshare 10.25378/janelia.25041485.v1; Zenodo 10.5281/zenodo.11493396.

## 9. Roemschied et al. 2023, Nature 622:794 ("Flexible circuit mechanisms for context-dependent song sequencing") [P]

- **Context.** "Male flies sing 'simple' trains of only one mode far from the female fly but complex song sequences … when near her" (threshold 4 mm). Simple pulse bouts are ">95%" of bouts far away and "around 55%" near.
- **Activation of pIP10 or TN1 (≈30 neurons, TN1A–E).**
  - pIP10 drives "stimulus-locked" pulse song, and strong stimuli drive "rebound" sine after pulses stop. TN1 drives sine with some pulse.
  - With a female present, complex song appears across many more stimuli.
  - "activation of either pIP10 or TN1 neurons in decapitated male flies still resulted in rebound sine or pulse song … the rebound circuit must be fully contained within the VNC". n = 10 headless males each.
- **Imaging (GCaMP6s; 123 TN1 in 3 flies; pIP10 drive).** "nearly half" of TN1 were positively correlated with the stimulus. "a smaller fraction showed activity perfectly anti-correlated", with alternating peaks persisting after stimulation. pIP10 axons and dPR1 tracked the stimulus.
- **Rebound.** Ih mutants "sang mostly simple pulse bouts". TN1-specific Ih or Rdl knockdown reduced complexity.
- **Upstream.**
  - P1a activation produced "persistent and variable song" and suppressed wing extension during the stimulus.
  - pC2 (pC2l, pC2m) drives pulse then rebound sine; silencing pC2 reduced song. "a direct connection from pC2 to pIP10 has been confirmed via expansion microscopy".
  - P1a + pIP10 co-activation gives long complex bouts.
- **pIP10 physiology.** In vivo patch clamp shows "clear signs of spike-frequency adaptation" and post-inhibitory rebound spikes after negative current. No song-time firing rate is given.
- **pIP10 silencing.** TNT and Kir2.1 both cut simple pulse bouts; only TNT raised sine-leading bouts. Their interpretation: "a potential role for electrical synapses".
- **Model [M].** Brian2 with four Izhikevich neurons ('pC2', 'inh', 'p', 's'). It has mutual inhibition between p and s, rebound in p and s, and inh disinhibited by pC2. The only input is male–female distance.
  - Fitted by genetic algorithm to bout statistics of 20 wild-type recordings.
  - It reproduces bout-type distributions and their distance dependence. Pulses and IPIs are not modelled.
  - It is not connectome-constrained; the male connectome was not yet public.
- Shiozaki et al. later dispute the mutual-inhibition core: TN1 are coactive during pulse song.

## 10. Other behavioural and activation papers

- **Inagaki et al. 2014, Nat Methods 11:325 [P].**
  - P1 > ReaChR: wing extension at variable latency (17.7 ± 27.5 s), bouts of 0.99 ± 0.48 s, persisting between trials.
  - pIP10: latency "0.08 ± 0.04 sec", extension through the light and co-terminating with it (r = 0.993).
  - Social isolation raises P1 but not pIP10 sensitivity.
- **Bath et al. 2014, Nat Methods (FlyMAD) [A].** Rapid thermogenetic control revealed "distinct timing relationships for two neuronal cell types previously linked to courtship song" (P1 and pIP10).
- **Coen et al. 2014, Nature 507:233 [A].** Song patterning choices depend on fast visual and self-motion cues ("not a fixed action pattern").
- **Calhoun et al. 2019, Nat Neurosci 22:2040 [P].** A GLM-HMM finds three internal states ("close", "chasing", "whatever"). pIP10 activation pushes males into "close". Song bins are 33 ms, "roughly the inter-event interval between pulse events".
- **McKellar et al. 2019, Curr Biol [A].** One DN pair orders courtship actions by activity thresholds (ramp-to-threshold).
- **Ding et al. 2019, Curr Biol 29:1089 [A].** Homologous pIP10 neurons in two species; relevant evolutionary changes lie "downstream of the intrinsic physiology of these descending neurons". "Artificial stimulation of these descending neurons drives multiple song types".

## 11. Song statistics papers

- **Kyriacou & Hall 1980, PNAS 77:6729 [A].** "pulses of tone produced at intervals of approximately 34 msec in D. melanogaster and 48 msec in D. simulans". They reported ~60-s IPI cycles. These were later disputed (Stern 2014; Stern et al. 2017) and defended (Kyriacou et al. 2017).
- **Ewing & Bennet-Clark 1968, Behaviour 31:288 [A].** "The frequency within the pulses and the interval between them varied between species but was constant and characteristic for each species." Bennet-Clark & Ewing 1969 (IPI playback) was not read.
- **Arthur et al. 2013, BMC Biol 11:11 [P].**
  - 75 males of five wild-type strains, "approximately 25°C".
  - Pulses mostly peak "at approximately 220 Hz"; "Approximately 17% of pulses had maximum energy at roughly double this frequency".
  - ">100,000 IPIs" "skewed to longer IPIs", best fit by a two-Gaussian mixture. Strains differ in IPI, carrier, train length and sine/pulse ratio.
  - "sine train carrier frequency increased over the course of most recordings, by about 10 to 20 Hz". Pulse carrier tends to decline within a bout.
- **Stern 2014, BMC Biol 12:38 [P + data].** IPIs "between 15 and 65 ms long". "The IPI varies over an order of approximately two on a short timescale, even within a single pulse train." Data: research.janelia.org/sternlab/IPIs.zip.
- **Kyriacou et al. 2017, PNAS 114:1970 [P via PMC page].**
  - IPI "ranges from 15 to 80 ms but usually averages between 30 and 40 ms". Canton-S mean IPI is ~35 ms; D. simulans is ~48 ms.
  - Stern's songs were "recorded between 23.6 and 27.9 °C". "Weighted mean recording temperatures for Canton-S were 25.5 °C"; per mutants were recorded at 23.5–24.6 °C. "The inverse correlation between temperature and IPI (Shorey 1962)" explains longer per0 and perS IPIs.
  - Stern's detector "identifies only ∼50% of the IPIs found by manual … monitoring".
  - Kyriacou & Hall used 2× the mean IPI as the upper limit.
- **Stern et al. 2017, PNAS [A].** They "cannot replicate" rhythms in hand-annotated data, and their segmentation "was not biased".
- **Stanley & Kyriacou 2021, J Neurogenet 35:333 [A].** IPI "usually falls in the mean range of 30-40 ms" and "is extremely temperature-sensitive". IPI correlates with latitude in Australian populations, but not with body size.
- **My reanalysis of Stern's IPI files [SD→D].**
  - Columns are pulse time and next IPI in 0.1-ms samples. All IPIs are already within 15–65 ms. Trains are chains of consecutive pulses; flies need ≥100 IPIs.

| Genotype (rec. temp.) | Flies / IPIs | Pooled mean ± SD (CV) | Mode | Per-fly mean (range) | % IPIs 30–40 / >40 ms | Pulses per train, median (IQR) | Train duration, median | Lag-1 IPI r |
|---|---|---|---|---|---|---|---|---|
| Canton-S (~25.5 °C) | 88 / 360,155 | 34.4 ± 7.5 (0.22) | 31.2 | 34.6 ± 1.8 (31.6–39.4) | 59 / 15 | 4 (3–7); 90th 11; max 51 | 108 ms (IQR 56–202) | 0.20 |
| perS (~23.8 °C) | 16 / 31,757 | 40.8 ± 6.6 (0.16) | 36.8 | 40.6 ± 1.1 | 56 / 44 | 4 (2–7) | 123 ms | 0.06 |
| perL (~24.6 °C) | 16 / 120,749 | 37.6 ± 6.0 (0.16) | 35.8 | 37.6 ± 1.0 | 71 / 25 | 5 (3–8) | 142 ms | 0.17 |
| per0 (~23.8 °C) | 14 / 27,319 | 41.1 ± 8.1 (0.20) | 37.2 | 41.6 ± 1.2 | 44 / 50 | 3 (2–5) | 87 ms | 0.20 |
| D. simulans NJ (~25.8 °C) | 103 / 129,707 | 43.4 ± 9.2 (0.21) | 41.2 | 44.0 ± 2.0 | 33 / 62 | 3 (2–4) | 74 ms | −0.04 |

  Caveats. The 65-ms cap truncates the upper tail; it truncates simulans much more, since its true mean is ≈48 ms. Missed pulses (Kyriacou: ~50%) split trains, so train lengths are lower bounds. Per-fly CV for Canton-S is 0.22 (IQR 0.19–0.24).
- **IPI changes with genes and lesions.**
  - Thoracic fruM RNAi (tsh-GAL4; Rubinstein, Rivlin & Hoy 2010): 42% of males sang no pulse song; the rest had fewer pulses per train, broader and polycyclic pulses, but IPI was normal ("did not show a disrupted IPI").
  - slo and cac (Peixoto & Hall 1998 [A]): slowpoke mutations "cause severe song abnormalities"; cac, para^ts1 and nap^ts1 have "subtler song defects".
  - slo-null "males sing little song with severely disrupted features" (Ding et al. 2016 [A]).
  - dsx mutants and TN1 silencing change the IPI (Shirangi 2016).
  - MN silencing (i2, hg1, hg2) shifts IPIs above 40 ms (O'Sullivan 2018).

## 12. MaleCNS v1.0: names and wiring of the song circuit (my queries of the local tables) [D]

Files: `body-annotations-male-cns-v1.0-minconf-0.5.feather`, `body-neurotransmitters-…`, `connectome-weights-…-minconf-0.5.feather`. I extracted all 396,360 edges touching 216 song and wing neurons. Scripts and outputs are in the scratchpad (`song_scripts/`, `song_conn/`). No model was run.

### 12.1 Names, counts, transmitters (MaleCNS `type`; MANC `mancType`; in brainfly `flywireType` replaces `type` when present)

| Literature name | MaleCNS type(s) (n, L/R) | Hemilineage | fru/dsx annotation | Consensus NT | Notes |
|---|---|---|---|---|---|
| P1 (pMP4, pMP-e) | `pC1_*` with synonyms "Yu 2010: pMP4" (male-specific; flymsg counts 86) | – | dsx/coexpress | ACh | "P1" is not a MaleCNS type |
| pC2l / pC2m | AVLP718m, PVLP210m, SIP109m, PVLP204m … / PVLP202m, VES203m, VES204m, AVLP702m, LAL30xm … | – | coexpress / dsx | – | from the synonyms column |
| pIP10 (P2b; pIP-a) | `pIP10` (2): 11116 R, 523998 L; MANC 13038, 13417 | – | fru_high, male-specific | ACh | |
| pMP2 | `pMP2` (2): 10765 R, 10930 L; MANC 11977, 11987 | – | fru_high, male-specific | ACh | |
| dPR1 | `dPR1` (2): 800323 R (MANC 10300), 800329 L (MANC 10267) | 08B | coexpress_high | ACh | `IN08B001` (2) also carries the synonym "Lillvis 2024: dPr1", but its wiring is leg-like |
| TN1A | `TN1a_a`…`TN1a_i` (22; 11 per side) | 12A | coexpress_high | ACh | TN1A-1/-2 are split across subtypes (§12.4) |
| TN1C | `TN1c_a`–`d` (13) | 12A | coexpress_high | ACh | |
| vPR6 | `vPR6` (8; 4 per side) | 12A | coexpress_high | ACh | LM 2–5 per side |
| vPR9 | `vPR9_a` (4), `_b` (2), `_c` (3) (midline) | 00A | fru_high | GABA | Lillvis: 7 in MANC |
| vMS11 | `vMS11` (14) | 08A | – | glutamate | LM 2.9 ± 1.3 per side, so the count disagrees |
| vMS12 | `vMS12_a`–`e` (18) | 12A | fru_high | ACh | Lillvis: 20 in MANC |
| dMS2 | `dMS2` (20) | 17A | fru_high | ACh | Lillvis: 18 in MANC |
| dMS9 | `dMS9` (2, ascending) | 19B | fru_high, dimorphic | ACh | flywireType `AN_GNG_SAD_23`; Stürner: AN19B007 |
| dMS5 | `dMS5` (2) | 19B | fru_high | ACh | |
| vMS16, vMS17 | `vMS16` (2), `IN27X001` (2) | 27X | fru | ?, GABA | |
| vPR13 | `AN08B031` (6), `AN08B043` (2), `AN08B059` (5), `AN08B069` (2) | 08B | fru_high | ACh | |
| vPR1 | `AN08B074` (6) | 08B | fru_high, potentially male-specific | ACh | |
| male-specific 08B ANs | AN08B020, 035, 047, 059, 061, 074, 084 (7 types) | 08B | – | ACh | matches Stürner's seven types |
| dMS1 (Ms1) | `IN10B013` (2) | 10B | coexpress, male-specific | ACh | |
| wing MNs | `b1 MN`, `b2 MN`, `b3 MN`, `i1 MN`, `i2 MN`, `iii1 MN`, `iii3 MN`, `MNwm35` (iii4?), `hg1`–`hg4 MN`, `ps1 MN`, `ps2 MN`, `tp1 MN`, `tp2 MN`, `tpn MN`, `TTMn`, `DLMn a, b`, `DLMn c-f`, `DVMn 1a-c`, `DVMn 2a, b`, `DVMn 3a, b`, `MNwm36` | – | – | glutamate or unclear | 2 per type except the power MNs |

Hemilineage 12A dsx/coexpress neurons number 44 (22 per side): TN1a 22, TN1c 13, vPR6 8 and IN12A030 1. This matches Shiozaki's "approximately 22 TN1 neurons in each hemisphere". Shirangi's light-level count was "approximately 30 TN1 cells on each side".

### 12.2 pIP10 and pMP2 (per type, both neurons summed)

- **pIP10.** 11,186 input and 14,924 output synapses per neuron. 48.8% of outputs go to bodies with no annotation; those are dropped from brainfly.
  - Top annotated outputs: AN08B061 2113 (7.1%), dPR1 1112 (3.7%), IN12A030 979, TN1a_g 940, vPR9_a 608, vPR9_c 607, TN1a_i 479, TN1a_d 401, vPR9_b 392.
  - By family: TN1A 3440, vPR9 1607, dPR1 1112. vPR6 gets only 65 (max 13 per neuron pair) and vMS11 50 (max 20 per pair). Of annotated outputs, 40.7% go to the core eight.
- **Inputs to pIP10.** 8.7% come from pC1_* (P1 included; pC1_14a 565, pC1_5b 215) and 8.8% from pC2-synonym types (AVLP718m 723, PVLP210m 275, VES204m 217, PVLP202m 208, VES203m 189).
  - Others: aIPg7 1280 (5.7%), ICL008m 916, AVLP717m/710m 754 each, DNp13 208.
  - VNC feedback onto pIP10 (axonal in reality): vPR9_c 519 and vPR9_a 334 (GABA), AN08B074 353.
  - 42% of pIP10 input comes from male-specific neurons.
- **pMP2.** 26,587 output synapses, 59.5% to unannotated bodies.
  - Top outputs: dPR1 1750 (6.6%), IN11A001 590, IN12A030 582, TN1a_g/i/h ≈420 each, vPR9_b 335, AN08B043 315.
  - Inputs: SIP107m, pC1_14a (962), AVLP712m and others; aSP22 gives 180.
- **Per-neuron counts onto each dPR1** (≈7,700 annotated input synapses each):
  - From the two pIP10: 497 (L) and 615 (R), i.e. 6.5–8%.
  - From the two pMP2: 870 and 880, ≈11%.
  - Between the dPR1 pair: 510 and 513 (≈6.6%).
  - The single largest dPR1 input type is IN03B024 (GABA): 1533 synapses (9.7%).

### 12.3 Core-eight recurrence and MN targets

- **Core share of each family's input / annotated output.** pIP10 4.9% / 40.7%; pMP2 1.4% / 37.3%; dPR1 35.6% / 27.4%; dMS9 13.2% / 49.2%; vMS12 40.0% / 46.7%; TN1A 38.5% / 41.3%; dMS2 34.4% / 10.4%; vPR9 48.1% / 45.2%. This is consistent with Lillvis' "almost half".
- **Family matrix (pre → post synapses).**
  - pIP10 → TN1A 3440, → vPR9 1607, → dPR1 1112.
  - pMP2 → dPR1 1750, → TN1A 1315, → vPR9 647.
  - dPR1 → dMS2 1646, → dPR1 1023, → dMS9 822, → TN1A 552.
  - dMS9 → vMS12 7415.
  - vMS12 → dMS2 6138, → vMS12 4825, → TN1A 1871.
  - TN1A → dMS2 7913, → vPR9 4342, → TN1A 3797, → dPR1 851.
  - vPR9 → TN1A 3791, → pIP10 877, → dPR1 749.
  - dMS2 → dMS2 1414 and almost nothing else in the core.
- **MN input from the core.**
  - hg1 13.8% (dMS2 3657, dPR1 593, TN1A 484); hg3 12.2% (TN1A 2157, dMS2 1099).
  - MNwm35 9.4% (dMS2 1495, vMS12 788); hg4 7.0%.
  - ps1 5.4% (vMS12 1808 of 1838).
  - DVMn 2a,b 4.7%, ps2 3.2%, DLMn a,b 3.0%, DLMn c-f 2.7% (all mostly TN1A).
  - b3 2.1% (dPR1 435); i1 0.9% (vMS12 142, dPR1 86).
  - b1 0.6%, b2 0.2%, iii1 0.2%, TTMn 0%.
- **Outside the core.** vPR6 → hg1 1123 (3.3% of hg1 input) and vMS11 → ps1 1074, → MNwm36 1128, → DVMn 3a,b 597.

### 12.4 TN1A-1 / TN1A-2 (Shiozaki's MANC ids → MaleCNS via `mancBodyid`)

- **TN1A-1** (9 of 10 mapped): TN1a_g ×2, TN1a_i ×2, TN1a_h ×1, TN1a_d (R) and TN1a_f (one L). Two are typed `IN12A030` (MANC 14810, 15387).
- **TN1A-2** (12 of 14 mapped): TN1a_a ×2, TN1a_b, TN1a_c ×2, TN1a_d (L), TN1a_e, TN1a_f ×3 and TN1a_g ×2.
- So the functional split cuts across MaleCNS subtypes d, f and g. A test needing TN1A-1 vs -2 must use bodyIds.
- In MaleCNS the subtypes getting both pIP10 and pMP2 input are TN1a_g (940/433), h (350/416) and i (479/421). IN12A030 gets 979/582 and is fru/dsx+, male-specific, with the synonym "Cachero 2010: vPr-k".

### 12.5 Other strong partners of the core (MaleCNS names)

- **IN03B024** (2, GABA): → dPR1 1533, → vMS12 1506, → TN1A 511, → pMP2 484; receives from vMS12 1729 and TN1A 497.
- **IN11A001** (2, GABA): receives from dPR1 1602 and pMP2 590; → vMS12 1312, → TN1A 472.
- **AN08B061** (7, ACh, potentially male-specific): receives from pIP10 2113, vPR9 984 and dPR1 771; → TN1A 892, → dPR1 691.
- The MaleCNS types named IN11B003 and IN03B021 have no contacts with the core. Lillvis' MANC v1.0 names do not carry over, and IN03B024 and IN11A001 may be their counterparts (unverified).

### 12.6 Implications for brainfly specifically

- Weights are signed counts divided by the target's total |input| from annotated neurons. Glutamate and GABA are negative, so vMS11 (glutamate) is inhibitory in the model.
- Outputs to unannotated fragments (about 30–68% of each song neuron's output) are dropped. About 95–98% of each one's input comes from annotated neurons.
- `cell_type` prefers flywireType, so dMS9 appears as `AN_GNG_SAD_23`; select by bodyId.

## 13. Connectome papers

- **Berg et al. (MaleCNS), bioRxiv 2025 [PP].**
  - "we identified song DNs (pIP10 and pMP2) and key wing pre-motor neurons in the ventral nerve cord (TN1A, vPR9, and dPR1)".
  - "a set of male-specific ascending neurons (AN08B074 and AN08B084)" feed "information from VNC song generation neurons to fru+ song detection circuits (aSP-a/pIP-e)" and to song DNs. The connections are bidirectional, so this "may function as an efference copy".
  - Song detection starts with JO-B neurons onto aPN1.
- **Stürner et al. 2025, Nature [P].**
  - Male dimorphic DNs connect strongly to "TN1a (silencing decreases sine song), vPR9 … and dPR1 (silencing increases sine song)".
  - "seven types of male-specific 08B AN … Five of these (including … vPR1) form an interconnected circuit with known song neurons such as the dimorphic DNs pMP2 and pIP10, intrinsic neuron dPR1 and sexually dimorphic AN19B007 (dMS9)". AN08B020 and AN08B059 are leg-related.
  - DNp13 (pMN1 in females) connects strongly to TN1a in MANC.
  - DNa12 (aSP22) connects to "the TN1c pulse song neuron".
  - Male-specific types missing from FANC (female): TN1c, IN12A037, IN12A041 and IN08A003.
- **Cheong et al. 2026, eLife (MANC premotor) [P].**
  - All 26 wing MNs were matched to muscles except one. "MNwm36 … remains unassigned", and the MNwm35 = iii4 match is putative.
  - Power MNs get "heavy shared input" from ~21 pairs of tectular INs.
  - Decapitated flies' VNC can "generate the appropriate signals for patterned motor activities including … courtship song".

## 14. Existing models of song generation

- **Roemschied et al. 2023 [M].** A hand-built 4-node Izhikevich network (§9). It reproduces bout-type statistics versus distance. It does not model pulses, IPI or the connectome.
- **flymsg** (gianlucamazza/flymsg, GitHub, 2026; not peer-reviewed) [M]. A Shiu-style LIF of all of MaleCNS v1.0 with w_syn 0.192 and 1.8 ms delay.
  - "pIP10 song pathway" case: both pIP10 get 100 Hz Poisson input for 300 ms; dPR1 fires ≈88 Hz (P1 drive ≈97 Hz).
  - Silencing tests: removing dMS9 raises dPR1 by 67%. Removing IN03B024 or vMS12_a+b+c raises it by 67–101%. Their supported loop is dPR1 → dMS9 → vMS12 → IN03B024 → dPR1.
  - "pIP10 → vPR6, vMS11: stay silent in the model although pIP10 synapses onto them". It advises: "Use the model to rank which circuits a stimulus recruits … not to predict exact firing".
  - It does not test rhythm or IPI.
- **Pugliese et al. 2025/26.** Walking only (a rate model); no wing or song.
- **Conclusion.** No connectome-constrained model has produced song pulses or an IPI. The earlier note "There is no fitted dynamical model of the song circuit" (`connectome_constrained_models.md`) still holds, apart from the bout-level Roemschied model and flymsg's rate checks.

## 15. Synthesis: is the IPI set in the VNC?

- **For: the thoracic VNC.**
  - Headless or VNC activation of fru neurons sings (Clyne & Miesenböck 2008; von Philipsborn 2011). Decapitated pIP10 activation sings (Shiozaki ED Fig. 1q,r; Roemschied Fig. 2e).
  - Gynandromorphs: "regions of the mesothoracic ganglia need to be male to ensure the correct song structure" (von Schilcher & Hall 1979 [2°]).
  - vPR6 activation sets the IPI in a graded way; dPR1 activation fixes it near 46 ms.
- **For: central, not feedback.**
  - Vestigial-winged flies keep IFM potentials at song IPIs. Antenna removal leaves the timing unchanged (Ewing 1979).
  - Thoracic fruM knockdown spares the IPI while damaging pulse shape.
  - IFM rate tracks amplitude, not IPI.
- **The brain's role.**
  - pIP10 and P1 activation give near-natural IPIs, "trigger but do not pattern".
  - Visual distance information modulates amplitude downstream of pIP10 without changing the IPI.
  - Mode selection is partly descending (pMP2 is pulse-specific).
- **Unknown.**
  - Which neuron or loop times pulses. No recording is fast enough, and there are no VNC song-interneuron electrophysiology papers.
  - Whether brain or thoracic temperature sets the 1 ms/°C natural slope. No focal-cooling study was found.
  - Whether the rhythm needs gap junctions (dMS2) or intrinsic rebound.

## 16. A minimal model test (proposal) and what would block it

- **Stimulus.**
  - Drive both pIP10 (bodyIds 11116, 523998) tonically. Sweep drive across a wide range, since fly firing during song is unknown; flymsg used 25–200 Hz Poisson.
  - Optionally co-drive pMP2 (10765, 10930).
  - Run 10 s episodes with ≥10 seeds, as fly trials are 3–10 s.
  - Variants: intact network, and "decapitated" (silence all `cb_*`, `ol_*` and visual superclasses, keeping pIP10's VNC axon).
- **Readout.**
  - Spike times of i1, b3, hg1–4, ps1 and MNwm35 MNs (pulse "on" group and core targets).
  - b1 and b2 MNs as a negative control (silent in fly song).
  - DLMn and DVMn rates.
  - Define a "pulse" a priori, e.g. a population spike volley across steering MNs. Define trains as events with gaps ≤65 ms, following Stern (Shiozaki used ≤50 ms).
- **Targets (fly, ~25 °C).**
  - Median IPI 30–40 ms (fly means 31.6–39.4 ms); pooled CV ≈0.2 (0.19–0.24 per fly); right-skewed distribution with mode ≈31 ms.
  - IPI nearly independent of pIP10 drive while event rate rises (fly: 33.3 → 35.4 ms as pulses/min rose 11×).
  - Trains: median ≥4 pulses, up to ~50.
  - IFM units ≈14 Hz and not locked to events [D from ISI ≈ 2 × IPI].
  - b1 and b2 silent.
- **Controls.**
  - (i) Degree- or weight-preserving shuffles of VNC wiring.
  - (ii) Silencing dPR1, vMS12, dMS9 or pMP2 should cut events; silencing TN1A should not cut pulse events.
  - (iii) vPR6-only drive should give long IPIs (36–68 ms) that shorten with drive; dPR1-only drive should give ≈46 ms at any drive.
  - (iv) pIP10 + vPR9 co-drive should suppress pulses ("almost entirely sine").
  - (v) Brain-silenced pIP10 drive should still give events.
  - (vi) A P1-only drive (pC1 P1 types) should be weaker, less locked and persistent (Inagaki: 17.7 s latency).
- **Blockers and caveats.**
  - (a) No wing mechanics or acoustics. The ≈220 Hz carrier and pulse shape come from asynchronous IFM resonance and steering-muscle damping. The test can only score MN event timing, and the MN → pulse mapping rests on EMG and Ca data (§§4–5).
  - (b) Electrical synapses are absent: dMS2 may be largely electrical, pIP10 electrical coupling is suggested, and the DLM splay coupling is already imposed separately.
  - (c) No rebound or adaptation currents: Ih and PIR matter for sine and complex song, and pIP10 adapts.
  - (d) Spiking vs graded song premotor neurons are unknown.
  - (e) Sign uncertainty for glutamatergic vMS11.
  - (f) vPR9 → pIP10 synapses (877) are presynaptic in flies but would inhibit the pIP10 soma in a point model.
  - (g) Type pitfalls: dMS9 = `AN_GNG_SAD_23`, TN1A-1/-2, and the IN08B001 "dPr1" synonym.
  - (h) brainfly's VNC recipe gives leg rhythms only in a narrow drive window. A song rhythm may need the same tuning, so pre-register the drive sweep and the "pulse" definition before running.

## Sources

- von Philipsborn AC et al. (2011) Neuronal control of Drosophila courtship song. Neuron 69:509–522. https://doi.org/10.1016/j.neuron.2011.01.011 (read via https://web.archive.org/web/20230517011826/https://www.cell.com/neuron/pdf/S0896-6273(11)00057-2.pdf)
- Lillvis JL et al. (2024) Nested neural circuits generate distinct acoustic signals during Drosophila courtship. Curr Biol 34:808–824.e6. https://doi.org/10.1016/j.cub.2024.01.015 ; preprint v1 https://doi.org/10.1101/2023.08.30.555537 (read via https://web.archive.org/web/20250125005324/https://www.biorxiv.org/content/10.1101/2023.08.30.555537v1.full.pdf)
- Shiozaki HM et al. (2024) Activity of nested neural circuits drives different courtship songs in Drosophila. Nat Neurosci 27:1954–1965. https://doi.org/10.1038/s41593-024-01738-9 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11452343/ ; Supplementary Data https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41593-024-01738-9/MediaObjects/41593_2024_1738_MOESM6_ESM.xlsx
- Roemschied FA et al. (2023) Flexible circuit mechanisms for context-dependent song sequencing. Nature 622:794–801. https://doi.org/10.1038/s41586-023-06632-1 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC10600009/
- Clemens J et al. (2018) Discovery of a new song mode in Drosophila reveals hidden structure in the sensory and neural drivers of behavior. Curr Biol 28:2400–2412.e6. https://doi.org/10.1016/j.cub.2018.06.011 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6830513/
- O'Sullivan A et al. (2018) Multifunctional wing motor control of song and flight. Curr Biol 28:2705–2717. https://doi.org/10.1016/j.cub.2018.06.038 (main text via https://web.archive.org/web/20221128161446/https://www.cell.com/current-biology/pdf/S0960-9822(18)30829-7.pdf ; supplement https://authors.library.caltech.edu/records/tbg1r-a1980)
- Shirangi TR, Stern DL, Truman JW (2013) Motor control of Drosophila courtship song. Cell Rep 5:678–686. https://doi.org/10.1016/j.celrep.2013.09.039 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC3926192/
- Shirangi TR et al. (2016) Doublesex regulates the connectivity of a neural circuit controlling Drosophila male courtship song. Dev Cell 37:533–544. https://doi.org/10.1016/j.devcel.2016.05.012 (via https://web.archive.org/web/20230508162256/https://www.cell.com/developmental-cell/fulltext/S1534-5807(16)30325-2)
- Clyne JD, Miesenböck G (2008) Sex-specific control and tuning of the pattern generator for courtship song in Drosophila. Cell 133:354–363. https://doi.org/10.1016/j.cell.2008.01.050 (abstract, PubMed 18423205)
- Ewing AW (1979) The role of feedback during singing and flight in Drosophila melanogaster. Physiol Entomol 4:329–337. https://doi.org/10.1111/j.1365-3032.1979.tb00624.x (abstract via Crossref) ; Ewing AW (1977) J Comp Physiol 119:249–265 https://doi.org/10.1007/BF00656637 and (1979) J Comp Physiol 130:87–93 https://doi.org/10.1007/BF02582977 (not read)
- Coen P et al. (2016) Sensorimotor transformations underlying variability in song intensity during Drosophila courtship. Neuron 89:629–644. https://doi.org/10.1016/j.neuron.2015.12.035 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC5047376/
- Coen P et al. (2014) Dynamic sensory cues shape song structure in Drosophila. Nature 507:233–237. https://doi.org/10.1038/nature13131 (abstract)
- Inagaki HK et al. (2014) Optogenetic control of Drosophila using a red-shifted channelrhodopsin reveals experience-dependent influences on courtship. Nat Methods 11:325–332. https://doi.org/10.1038/nmeth.2765 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4151318/
- Bath DE et al. (2014) FlyMAD. Nat Methods 11:756–762. https://doi.org/10.1038/nmeth.2973 (abstract)
- McKellar CE et al. (2019) Threshold-based ordering of sequential actions during Drosophila courtship. Curr Biol 29:426–434. https://doi.org/10.1016/j.cub.2018.12.019 (abstract)
- Ding Y et al. (2019) Neural evolution of context-dependent fly song. Curr Biol 29:1089–1099. https://doi.org/10.1016/j.cub.2019.02.019 (abstract)
- Ding Y et al. (2016) Natural courtship song variation caused by an intronic retroelement in an ion channel gene. Nature 536:329–332. https://doi.org/10.1038/nature19093 (abstract)
- Calhoun AJ, Pillow JW, Murthy M (2019) Unsupervised identification of the internal states that shape natural behavior. Nat Neurosci 22:2040–2049. https://doi.org/10.1038/s41593-019-0533-x ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7819718/
- Arthur BJ et al. (2013) Multi-channel acoustic recording and automated analysis of Drosophila courtship songs. BMC Biol 11:11. https://doi.org/10.1186/1741-7007-11-11 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC3599446/
- Stern DL (2014) Reported Drosophila courtship song rhythms are artifacts of data analysis. BMC Biol 12:38. https://doi.org/10.1186/1741-7007-12-38 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4071150/ ; data https://research.janelia.org/sternlab/IPIs.zip
- Kyriacou CP et al. (2017) Failure to reproduce period-dependent song cycles in Drosophila is due to poor automated pulse-detection and low-intensity courtship. PNAS 114:1970–1975. https://doi.org/10.1073/pnas.1615198114 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC5338454/
- Stern DL et al. (2017) Experimental and statistical reevaluation provides no evidence for Drosophila courtship song rhythms. PNAS 114:9978–9983. https://doi.org/10.1073/pnas.1707471114 (abstract)
- Kyriacou CP, Hall JC (1980) Circadian rhythm mutations in Drosophila melanogaster affect short-term fluctuations in the male's courtship song. PNAS 77:6729–6733. https://doi.org/10.1073/pnas.77.11.6729 (abstract)
- Stanley RA, Kyriacou CP (2021) A latitudinal cline in a courtship song character of Drosophila melanogaster. J Neurogenet 35:333–340. https://doi.org/10.1080/01677063.2021.1933968 (abstract)
- Ewing AW, Bennet-Clark HC (1968) The courtship songs of Drosophila. Behaviour 31:288–301. https://doi.org/10.1163/156853968x00298 (abstract) ; Bennet-Clark HC, Ewing AW (1969) Anim Behav 17:755–759 https://doi.org/10.1016/s0003-3472(69)80023-0 (not read)
- Rubinstein CD, Rivlin PK, Hoy RR (2010) Genetic feminization of the thoracic nervous system disrupts courtship song in male Drosophila melanogaster. J Neurogenet 24:234–245. https://doi.org/10.3109/01677063.2010.519805 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC3056398/
- Peixoto AA, Hall JC (1998) Analysis of temperature-sensitive mutants reveals new genes involved in the courtship song of Drosophila. Genetics 148:827–838. https://doi.org/10.1093/genetics/148.2.827 (abstract)
- Berg S et al. (2025) Sexual dimorphism in the complete connectome of the Drosophila male central nervous system. bioRxiv https://doi.org/10.1101/2025.10.09.680999 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12636603/
- Stürner T et al. (2025) Comparative connectomics of Drosophila descending and ascending neurons. Nature. https://doi.org/10.1038/s41586-025-08925-z ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12222017/
- Cheong HSJ et al. (2026) Organization of circuits linking descending input to motor output in the Drosophila Male Adult Nerve Cord connectome. eLife. https://doi.org/10.7554/eLife.96084 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/
- Pugliese SM et al. (2025/2026) Connectome simulations identify a central pattern generator circuit for fly walking. https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/
- flymsg (G. Mazza), MaleCNS v1.0 spiking model, GitHub: https://github.com/gianlucamazza/flymsg (README, docs/validation.md, docs/dimorphism.md)
- MaleCNS v1.0 tables used for §12 (local copies in `~/fly-data/raw`, from https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome)
