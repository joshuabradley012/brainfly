# Descending neuron firing rates during walking, and what they imply for DNg100 and DNb08 drive

Notes compiled 2026-10-11 for brainfly's rung 5. They ask what spike rates flies' descending neurons (DNs) reach during
walking, so that a fourth rung 5 attempt can drive DNg100 and DNb08 at flies' rates rather than chosen ones.
"Derived" marks my own arithmetic. "Fig., approx." marks values read off a figure. Quotes are verbatim.

One correction to the brief: rung 5's drive is not a Poisson rate. In `experiments/vnc_rhythm.py` and `rung5_vnc3.py`
it is a constant input I (Pugliese et al.'s arbitrary units) added inside each DN's transfer function. The DN's own
rate is an output. In `rung5_vnc3.json` the drives 50/100/200/400/800 gave DNg100 rates of 0/0/4.4/16.5/0 Hz (left)
and 0/0/4.3/16.2/0 Hz (right). The 0 Hz at 800 came with runaway (about 2,100 of 4,309 neurons active). The left VES082
DNb08 gave 7.6/23.3/53.0/107/155 Hz.

## Summary

- **No one has recorded DNg100 (BDN2) or DNb08 spikes.** DNg100's only activity data are GCaMP6f imaging of its nerve
  cord axons in 3 walking flies. Activity tracks forward velocity: pooled r ≈ 0.47-0.53, against ≈ −0.1 for turning
  (derived from source data; Sapkal et al. 2024). There is no spike calibration. DNb08 has no activity data of any kind.
- **Walking DNs recorded whole-cell fire tens of spikes/s while walking.** DNa02: ≈20-30 spikes/s mean (Rayshubskiy et
  al. 2025) or ≈52 Hz (Yang et al. 2024). DNg13: ≈63 Hz walking, ≈39 Hz not walking. MDN: 8.5 Hz baseline, 12-16 Hz
  during touch-evoked backward walking, 0-75 Hz in a spontaneous-walking example. Brief peaks reach 75-150 spikes/s.
  DNa02's dynamic range is about 150 spikes/s.
- **Resting rates range from about zero to tens of Hz.** DNp07 and DNp10 fire 0.017 and 0.003 Hz when not flying, and
  the giant fiber did not even spike to looming. DA-DNs fire 3.1 Hz, MDN 8.5 Hz, DNp17 17 Hz. DNa02 at rest reads ≈3-9
  spikes/s (Rayshubskiy) or ≈19 Hz (Yang, fig., approx.).
- **Optogenetics, which defined both neurons' roles, can drive DNs far above these rates.** CsChrimson drove DNp07 and
  DNp10 to ≈100-500 spikes/s at 0.03-0.23 mW/mm², and DNp10 past 100 Hz from about 0.005 mW/mm² (Ache et al. 2019). It
  drove DNa02 to about 100 spikes/s in one 0.2 s pulse (derived from an example trace; Yang et al. 2024). DNg100 was
  driven at 0.01-0.33 mW/mm². Its rate under that light was never measured.
- **DNg100 alone makes decapitated flies step at about 3.5-12 Hz.** About 7.6-8.3 Hz on a ball, 11-12 Hz in air and about
  8 Hz on amputated stumps (Sapkal et al. 2026, fig., approx.). In another lab, 3.5 → 5.5 Hz on a ball as light rose
  from 0.03 to 0.33 mW/mm² (Pugliese et al., fig., approx.). Co-driving DNg97 (oDN1) raised ball stepping to ≈12 Hz and
  front-leg air-stepping to ≈21 Hz, near intact BPN-driven walking (≈12.5 Hz).
- **No study relates a DN's spike rate to step frequency.** The quantitative relations are for steering and speed.
  Rotational velocity is linear in the right-left DNa02 rate difference: ±100 spikes/s gives about ±600 °/s, so roughly
  6 °/s per spike/s (derived, fig., approx.). MDN's rate predicts backward walking speed.
- **The models chose drives without DN data.** Pugliese et al. state that "The inputs to the DNs in the network are in
  arbitrary units" and that the rate is "an abstract quantification of activity". Their DNg100 inputs (250 in MANC, 400
  in the male CNS) imply DNg100 at about 16 Hz (derived). Brainfly measured 16.2-16.5 Hz at 400. Their sweep from 180 to
  340 implies 9-24 Hz and gave motor rhythms of 7.7 → 12.7 Hz (derived from their repository data). Their MANC DNb08 input
  of 65 implies about 27-33 Hz (derived).
- **For brainfly, flies' data put walking DNs at about 20-60 Hz.** That is above the 16 Hz at which rung 5 tested DNg100.
  It corresponds to brainfly inputs of about 460-1,160. The low end lies between the accepted 400 and the runaway 800,
  which no attempt sampled. For DNb08 the general DN range is 20-100 Hz (inputs of about 90-390 for the left VES082).
  Brainfly's DNb08 passed at about 53 Hz. Confidence is low for DNg100 and very low for DNb08.

## 1. DNg100 / BDN2

### Names
- Bidaye et al. 2020 (Neuron) described P9 (DNp09) and BPN, not BDN2. The PMC text never mentions "BDN".
  [doi:10.1016/j.neuron.2020.07.032](https://doi.org/10.1016/j.neuron.2020.07.032),
  [PMC9435592](https://pmc.ncbi.nlm.nih.gov/articles/PMC9435592/)
- Sapkal et al. 2024 (Nature) named BDN2 and oDN1. They found them in a whole-brain model as DNs recruited by BPN and P9.
  [doi:10.1038/s41586-024-07854-7](https://doi.org/10.1038/s41586-024-07854-7),
  [PMC11446846](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446846/)
- Pugliese et al.: "([50], where DNg100 is referred to as BDN2)".
- Sapkal et al. 2026 (bioRxiv): "DNg100 (also referred to as BDN2) and DNg97 (also referred to as oDN1)".
  [doi:10.64898/2026.04.29.721658](https://doi.org/10.64898/2026.04.29.721658)

### Activity during walking: calcium imaging only
Source: Sapkal et al. 2024, Fig. 3l, Supplementary Video 4 and Methods.
- Method: two-photon GCaMP6f imaging of BDN2 axons in the nerve cord at 6 Hz volume rate. Flies walked on an air ball.
  The genotype was "BDN2-Gal4>Act88F:Rpr; UAS-GCaMP6f; UAS-tdTomato", which ablates the indirect flight muscles. n = 3
  flies.
- "Indeed, on in vivo imaging, we found that BDN2 activity is strongly correlated to forward (but not angular) velocity
  of the fly (Fig. 3l and Supplementary Video 4)."
- Sapkal et al. 2026 restate it: "By recording DNg100 activity in spontaneously walking flies, we previously showed that
  DNg100 activity correlates with and precedes forward velocity changes".
- Derived from Source Data Fig. 3l (z-scored traces pooled over the 3 flies):
  - zero-lag r with forward velocity: 0.47 (left cell) and 0.53 (right cell);
  - with angular velocity: −0.10 and −0.11;
  - the cross-correlation peaks at r = 0.54-0.60, slightly off zero lag (the sample rate isn't given, so I can't convert
    the lag to seconds).
- Not reported: dF/F magnitudes in the text, any spike rate, or any calibration of GCaMP6f to spikes in this neuron.

### Silencing
- "However, on optogenetic silencing, only BDN2-silenced flies showed a reduction in forward velocity (Fig. 3k)."
- Derived from Source Data Fig. 3k (GtACR1, freely walking): BDN2-silenced flies had a median of 13.2 mm/s (IQR
  12.0-13.7, n = 13). Controls had 19.2 mm/s (IQR 15.8-21.3, n = 20).

### Optogenetic activation: protocols and outcomes

| Study | Preparation | Light | Outcome |
|---|---|---|---|
| Sapkal 2024, Fig. 3j | intact, powdered (grooming) flies in an arena | 630 nm, 0.04 mW/mm², pulsed at 100 Hz, 10 s on | median 2.62 mm/s (IQR 1.11-3.29, n = 17), against 0.25 for controls (derived from source data) |
| Sapkal 2024, Ext. Data Fig. 6e | decapitated, tethered on a ball, 7-10 days old | 3 s light | text: "robust forward walking"; Methods: robust walking needed 10-12-day-old flies, "probably due to lower and more variable expression levels in younger flies" |
| Sapkal 2024, Fig. 4e-j | decapitated, 10-12 days old | one of five intensities (0.01, 0.015, 0.025, 0.041, 0.058 mW/mm²) chosen per fly | intensity picked where "that individual fly showed some degree of intention for forward walking" |
| Pugliese 2025/2026, Fig. 2h-j | decapitated, 10-12 days old, on a 9.08 mm, 0.13 g ball | 638 nm laser, pulsed at 1,200 Hz, 30% duty cycle, aimed at the front-left body-coxa joint; 0.03, 0.09, 0.33 mW/mm²; 5 s | left front leg stepped at ≈3.5, 5.2 and 5.5 Hz (fig., approx.); forward velocity ≈1.6, 3.2 and 3.9 mm/s at onset, ≈1, 2 and 2 mm/s by the end (fig., approx.); n = 7 flies, 8 trials per intensity |
| Sapkal 2026, Figs. 1 and 4 | decapitated, 14-16 days old (12-14 for amputation) | 630 nm fibre, pulsed at 66 Hz, ≈0.040 mW/mm², 3 s | ball: ≈7.6-8.3 Hz, ≈5.4 mm/s median; air: ≈11-12 Hz; amputated stumps: ≈8 Hz (all fig., approx.) |

- Pugliese et al.: "Increasing laser intensity led to an increase in both forward velocity and stepping frequency (Fig.
  2i–j)". And: "DNg100 activation produced forward walking on the ball, but at a lower speed than is typical of
  wild-type flies". The step frequencies and velocities above come from their repository notebook "Anipose data
  figures.ipynb", which draws Fig. 2i-j. Per-fly slopes of frequency against log10 intensity were 3.22, 4.75, 2.45, 1.44,
  −1.54, 1.90 and 0.99 Hz per decade. Their mean is 1.9 Hz per decade (derived; t-test p = 0.044 as printed).
- Sapkal et al. 2026: "However, DNg100 stimulated flies rarely walked faster than 8mm/s (Fig. 1b)." And: "Co-activating
  DNg100 with DNg97 led to a major increase in walking velocities (Fig. 4b), stepping frequencies (Fig. 4d) and
  tripod-coordination (Fig. 4c), all of which now almost reached BPN levels." Fig. 4 legend: "All flies except BPN are
  decapitated."
  - Fig. 4b, d (ball, fig., approx.): DNg100 alone stepped at ≈7.8-8.3 Hz and walked at ≈5.4 mm/s. DNg100 + DNg97
    stepped at ≈11.7 Hz and walked at ≈14.4 mm/s. Intact flies with BPN driven stepped at ≈12.4 Hz and walked at
    ≈17.6 mm/s.
  - Fig. 4g (air): DNg100 alone stepped at ≈11-12 Hz on all legs. With DNg97: "front legs stepped at much higher
    frequencies (∼22 Hz which is almost twice as fast as DNg100) compared to middle and hind legs which were stepping
    only slightly faster than DNg100 levels" (fig.: front ≈20.6 Hz, middle and hind ≈13.5 Hz).
  - "Silencing FeCO caused the stepping frequency to reduce even during non-amputated air-stepping bringing it down to
    amputated levels".

## 2. DNb08

Source: Pugliese et al. 2025/2026, bioRxiv,
[doi:10.1101/2025.09.12.675944](https://doi.org/10.1101/2025.09.12.675944),
[PMC13142387](https://pmc.ncbi.nlm.nih.gov/articles/PMC13142387/), code at
[github.com/smpuglie/Pugliese_2026](https://github.com/smpuglie/Pugliese_2026).
- Four neurons, two per side. "all four of its neurons (two per side) produced among the highest rhythmicity scores in
  the screen". "Although a study had created a genetic driver line for DNb08 neurons [54], their function had not been
  previously investigated." Reference 54 is the Zung et al. 2025 split-GAL4 catalogue. The line is SS70620
  (R94D12-p65.AD; VT031392-GAL4.DBD).
- Behavior: decapitated, 2-5-day-old flies with CsChrimson. "they reliably produced rhythmic leg movements". "they
  resembled the searching movements that insects exhibit when their legs are not in contact with the ground". "Indeed,
  movements were evoked more reliably when the spherical treadmill was removed." Fig. 5e: front and middle legs, n = 10
  flies, stimulus on against off, p = 0.036 (front) and 0.004 (middle).
- The light was 0.329 mW/mm². The repository notebook scores only that intensity ("skip the weaker strength"). The
  frequency of DNb08-driven leg oscillations is not given in the text.
- Possible natural roles (Discussion): "DNb08 may be involved in leg searching, aggression, or grooming. For instance,
  DNb08 was recently identified as a descending output of the aggression-associated neuron AVLP491 in the male brain
  [66]." Reference 66 is Cao & Anderson 2025 (bioRxiv; [PMC12633336](https://pmc.ncbi.nlm.nih.gov/articles/PMC12633336/)).
  I did not find DNb08 named in their main text. It names DNg100 and DNge050 among the targets shared by AVLP491 and
  AVLP710m (Fig. S6F).
- Sapkal et al. 2026, Fig. 4a, draws DNb08 among 27 DNs downstream of BPN, the forward-walking neuron. Arrow widths
  there scale "from 50 to 1,163 synapses", so each drawn DN presumably gets at least 50.
- Model: "Activating a single DNb08 neuron in the full network simulation consistently produced rhythmic leg motor neuron
  activity across three of the four connectome datasets (MANC, FANC, and mCNS)". The MANC input was 65
  (`configs/experiment/DNb08_Stim.yaml`).
- **Not reported anywhere:** DNb08 spike rates, calcium activity, the frequency of its evoked leg rhythm, or the behavior
  that recruits it naturally.

## 3. DNs with measured spike rates

All are in vivo whole-cell recordings in tethered flies unless noted.

| DN | Rest / not walking | Walking or behavior | Scaling | Source |
|---|---|---|---|---|
| DNa02 (steering) | ≈5-6 spikes/s after stopping (Fig. 6B, n = 7); ≈3-9 immobile (Fig. 6D, n = 4) | ≈20 spikes/s while walking at ≈400 °/s total speed; ≈38 at walking onset; ≈27-29 baseline while active; ≈80 peak with an attractive fictive odor; single cells to ≈150 in sharp turns (Fig. 3D) (all fig., approx.) | rotation ∝ right-left rate difference, ±100 spikes/s ↔ ±600 °/s (Fig. 3C); ≈2.5-5 °/s per spike/s per cell (Fig. 2F) | Rayshubskiy et al. 2025, eLife |
| DNa02 | ≈19 Hz (per fly ≈8-38) | ≈52 Hz (per fly ≈35-77), n = 4 (Fig. S7A, fig., approx.) | stride-locked modulation ≈15 spikes/s, "approximately 10% of the cell's dynamic range"; not correlated with forward velocity | Yang et al. 2024, Cell |
| DNa01 (steering) | — | binned mean rates up to ≈70 spikes/s (Fig. 2G, fig., approx.) | ≈0.5-2 °/s per spike/s, slower and lower-gain than DNa02 | Rayshubskiy et al. 2025 |
| DNg13 (steering) | ≈39 Hz | ≈63 Hz, n = 9 (Fig. S7A, fig., approx.) | over 130 spikes/s from current injection turns the fly; weakly correlated with forward velocity (r = 0.11-0.20) | Yang et al. 2024 |
| MDN (backward walking) | 8.5 Hz with legs on the ball | touch-evoked backward walking: 7.2 → 12.4 Hz (left antenna) and 7.8 → 15.8 Hz (right), N = 9; spontaneous example 0-75 Hz | rate rises from slow forward walking to stopping to backward walking and predicts backward speed; 13.8 → 0.3 Hz in flight | Dahlhoff, Liessem et al. 2025, bioRxiv (Curr Biol 2026) |
| DopaMeander (dopaminergic DN) | tonic; 7.8 Hz before flight | 0-40 Hz; higher in forward walking and ipsiversive turns | lateralized correlation with turning | same |
| DNp17 | 17 Hz | "not modulated during walking bouts" | none | same |
| DA-DNs (dopaminergic) | 3.1 ± 1.9 Hz, n = 10 | bursts during leg movements, instantaneous rate ≈15-20 Hz (Fig. 2B, fig., approx.) | correlated with total leg speed (CC 0.24 ± 0.11); changing their rate didn't change movement | Tschida & Bhandawat 2015, Physiol Rep |
| DNp07, DNp10 (landing) | 0.017 ± 0.06 and 0.003 ± 0.017 Hz when not flying, including air-walking | "spike rates exceeding 50 Hz during visual stimulation in flight" | spike rate sets leg extension amplitude | Ache et al. 2019, Nat Neurosci |
| DNp01 (giant fiber) | silent | head-fixed: depolarized to looming but did not spike | — | Dombrovski et al. 2023, Nature |

Key quotes and details:
- Rayshubskiy et al. 2025: "This relationship was essentially linear through its entire dynamic range". "DNa02
  hyperpolarized whenever the fly stopped walking". "The firing rate increase precedes the onset of movement by
  ~250 ms." In the author response: "DNa02 has a relatively high basal firing rate". Recordings: n = 13 single DNa02, 10
  single DNa01, and 4 bilateral DNa02 pairs. Rates are spikes in 10 ms bins, smoothed with a 30 ms filter.
  [doi:10.7554/eLife.102230](https://doi.org/10.7554/eLife.102230),
  [PMC12279373](https://pmc.ncbi.nlm.nih.gov/articles/PMC12279373/)
- Yang et al. 2024: "The firing rate of both DNs was higher when the fly was walking (Figure S7A)". "Although this
  stride-locked firing rate modulation was only about 15 spikes/sec (approximately 10% of the cell's dynamic range), it
  was highly consistent across DNa02 recordings." "depolarizing current injection into DNg13 could reliably elevate the
  spike rate to >100 spikes/s". Rate changes "preceded changes in rotational velocity and stride length by about
  150 ms".
  [doi:10.1016/j.cell.2024.08.033](https://doi.org/10.1016/j.cell.2024.08.033),
  [PMC12778575](https://pmc.ncbi.nlm.nih.gov/articles/PMC12778575/)
  - The two DNa02 papers disagree at rest. Yang's Methods call the not-walking rate "typically very low", and the Fig.
    S5 legend says "DNa02 does not spike if the fly is still". Yet Fig. S7A's not-walking mean reads ≈19 Hz.
    Rayshubskiy's immobile mean is ≈3-9 spikes/s. S7A's "not walking" epochs need not be still.
- Dahlhoff, Liessem et al. 2025: "MDNs exhibited a baseline spike rate of 8.5 Hz with a median spike amplitude of 6.5 mV
  when flies were tethered, and the legs were in contact with the treadmill." "In the example recording shown in Figure
  5B, MDN spike frequencies ranged from 0 to 75 Hz." "Essentially, MDN exhibited an increasing firing rate from slow
  forward walking to stopping to backward walking, during which it was predictive of backward walking speed." Before
  this study "MDN has not been characterized extensively in behaving animals". Fig. 5F's tuning curves use normalized
  rates.
  [doi:10.1101/2025.07.22.666129](https://doi.org/10.1101/2025.07.22.666129); published as Liessem, Dahlhoff et al.,
  Curr Biol 2026, [doi:10.1016/j.cub.2026.06.045](https://doi.org/10.1016/j.cub.2026.06.045)
- Tschida & Bhandawat 2015: "During time periods without leg movements, DA-DNs exhibited regular tonic firing (Fig.2B;
  mean spontaneous spike rate was 3.1 ± 1.9 Hz, N = 10 neurons)." The flies were in a holder with the head rotated, not
  walking on a ball. [PMC4393157](https://pmc.ncbi.nlm.nih.gov/articles/PMC4393157/)
- Ache et al. 2019: "spiking was almost completely absent in both DN types" when not flying. Optogenetic calibration,
  Supplementary Fig. 7 (625 nm, 50 ms pulses through the cuticle): "DN spike rate depended linearly on LED intensity".
  At 100% LED (≈0.23 mW/mm² at the fly), DNp07 reached ≈340-380 Hz and DNp10 ≈480-530 Hz. At ≈0.005-0.03 mW/mm²
  DNp10 reached ≈100-300 Hz (fig., approx.). In the main text: "leg extension amplitudes continued to increase with
  artificial activation of a single cell type beyond spike rates typically observed during visual stimulation
  (estimated spike rates >150 Hz)". [PMC7444277](https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/)
- Yang et al. 2024, Fig. S5A: CsChrimson-expressing DNa02 under a 0.2 s pulse at 0.02 mW/mm² (matched to 0.09 mW/mm²
  through cuticle). I count about 20 spikes in the pulse, so ≈100 spikes/s (derived from one example trace).
- Dombrovski et al. 2023: "DNp02, DNp11, the GF and DNp04 all depolarized in response to looming, and all except the GF
  produced action potentials". [PMC9849133](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/)

DNs named in the brief that have no electrophysiology:
- **DNp09 (P9):** none. In GCaMP6s imaging "P9 was not active during spontaneous walking" (Bidaye et al. 2020, Fig.
  S6L-N). Zacarias et al. 2018 silenced it (freezing) and did not record it.
- **DNg97 (oDN1):** none. Activation drives forward walking in decapitated flies (Sapkal 2024). Air-stepping ≈11 Hz, but
  ball walking only ≈2 mm/s peak (Sapkal 2026, Fig. 1b, e).
- **DNa06:** none found. It appears only as a model-recruited DN downstream of P9 and BPN (Sapkal 2024, Fig. 3).

Population imaging gives no spike rates:
- Aymanns et al. 2022 (eLife; GCaMP6s in the neck connective): "The largest fraction (~60%) of DNs encode walking." "a
  more distributed set of DNs weakly encode walking speed".
  [PMC9605690](https://pmc.ncbi.nlm.nih.gov/articles/PMC9605690/)
- Braun et al. 2024 (Nature): gnathal-ganglion DN populations were recruited both by DNp09 stimulation and in
  spontaneous walking, mostly alike. They warn of "the potentially high firing rate and relatively static temporal
  activity pattern driven by optogenetic stimulation". They used 640 nm light at 21 µW for DNp09 and MDN.
  [PMC11186778](https://pmc.ncbi.nlm.nih.gov/articles/PMC11186778/)
- Aimon et al. 2023 (eLife; whole-brain light-field imaging): a brain-wide rise in activity during walking, partly from
  ascending input. No DN-resolved rates. [PMC10168698](https://pmc.ncbi.nlm.nih.gov/articles/PMC10168698/)

## 4. DN rate and step frequency

- **No measurement in Drosophila relates a DN's spike rate to step frequency.**
- Nearest proxies:
  - DNg100 light intensity sets step frequency: 3.5 → 5.5 Hz for a tenfold-plus rise in light, about 1.9 Hz per decade
    (Pugliese; derived). The DN rate at each intensity is unknown.
  - Co-driving DNg97 with DNg100 raises ball stepping from ≈8 to ≈12 Hz by shortening stance from ≈85-90 to ≈55 ms
    (Sapkal 2026, Fig. 4d-e, fig., approx.).
  - BPN (central brain, upstream of DNg100): "increasing the light stimulation frequencies (from 10–150 Hz) of
    CsChrimson-mediated BPN activation increased the walking duration and translational velocity" (Bidaye 2020, Fig.
    7A). BPN-silenced flies "walked slowly as a result of an increased step period, due to an increased stance
    duration".
  - The step cycle modulates DNa02's spiking (≈15 spikes/s, phase-locked), the reverse direction (Yang 2024).
  - DNa02's rate predicts stride length during turns, not frequency (Yang 2024, Fig. 5C).
  - MDN's rate predicts backward speed (Dahlhoff, Liessem et al. 2025).
- In other insects, Aymanns et al. note: "For some DNs, links between firing rate and behavioral features like walking
  speed have also been established (Böhm and Schildberger, 1992)" (cricket). I did not read that paper.
- In the Pugliese model, derived from `figures/DNg100_Stim-hyak-run_id=28914803/frequencies.csv` in their repository
  (MANC, left DNg100, 512 replicates per input):

| input | median motor neuron frequency (IQR) | DNg100's own rate (derived) |
|---|---|---|
| 180 | 7.7 Hz (6.2-8.6), only 64 of 512 replicates with a frequency | ≈9 Hz |
| 220 | 9.8 Hz (8.8-10.5) | ≈13 Hz |
| 260 | 11.0 Hz (10.3-11.8) | ≈17 Hz |
| 300 | 12.0 Hz (11.2-12.8) | ≈21 Hz |
| 340 | 12.7 Hz (12.0-13.5) | ≈24 Hz |

  The DN rate is r = 200·tanh((I − 7.5s)/(200s)), with s = 10.7, DNg100's volume over the median in MANC (derived). This
  ignores the DN's recurrent input. Their linearized three-neuron circuit oscillates at "∼14 Hz", and "The MANC core CPG
  circuit does not show the same modulation of motor neuron frequency with DNg100 input strength as the full network
  does".

## 5. What the connectome nerve cord models assumed

- **Pugliese et al. 2025/2026** (rate model; the recipe brainfly reran):
  - "We report the output of this model as a rate in units of Hz, but as the model itself does not spike, this rate is
    interpreted as an abstract quantification of activity. The inputs to the DNs in the network are in arbitrary
    units."
  - "Because the input strength Istim was arbitrary in magnitude in our model, we automatically tuned Istim over a range
    of values depending on if the simulation was underactive or oversaturated." The screen starts at 128
    (`configs/experiment/DN_Screen.yaml`). It doubles or halves Istim to keep between 5 and 1,500 neurons active.
  - Inputs: DNg100 250 in MANC and 150 in FANC (repository configs), 400 in the male CNS (as rung 5 used). DNb08 65 in
    MANC.
  - rmax ~ N(200, 10) Hz and τ ~ N(20, 2) ms were set from "reasonable ranges ... given experimental literature [47,
    44]". Those references are Gouwens & Wilson 2009 (central brain neurons) and Agrawal et al. 2020 (leg
    proprioception), not DN recordings.
  - Implied DN rates (derived; open loop, from volumes): DNg100 ≈15-16 Hz at 250 in MANC (s = 10.7-11.2); DNb08 ≈27-33 Hz
    at 65 (s = 1.6-1.9). In brainfly's male CNS rerun (s = 16.6-16.7), DNg100 measured 16.2-16.5 Hz at 400. So their
    MANC and male CNS inputs, chosen separately, both put DNg100 at about 16 Hz (derived). I didn't check FANC, whose
    sizes are surface areas.
- **Sapkal et al. 2024** (Shiu et al.'s whole-brain LIF model on FlyWire) produced model DN rates, including BDN2's, from
  Poisson input to upstream neurons. "The walk neurons P9 and BPN were stimulated bilaterally at 150 and 50 Hz,
  respectively." "It is important to realize that the intrinsic firing rate of neurons in this model is zero and that
  the Poisson inputs constitute the only external input." Their wiring diagrams show DNs above 10.3 Hz (P9) or 20 Hz
  (BPN). The text gives no BDN2 rates. The source data point to an external repository
  ([doi:10.17617/3.OIX8RZ](https://doi.org/10.17617/3.OIX8RZ)), which I did not open.
- **No model sets DN rates from recordings.** I found no other connectome nerve cord model that does.

## For brainfly

**How the drive maps to a DN rate in brainfly's model (derived).** Take the mean parameters (gain 1/s, threshold 7.5·s,
rmax 200 Hz) and ignore recurrent input. Then a DN fires r = 200·tanh((I/s − 7.5)/200), which is about I/s − 7.5 Hz
below roughly 60 Hz. Here s is its volume over the median, from `wTable_20260210_vncRoisOnly.csv`. This matches
`rung5_vnc3.json` within about 1-2 Hz below runaway:
- DNg100_L at 400 predicts 16.4 Hz, measured 16.5. At 200 it predicts 4.5, measured 4.4.
- VES082_L DNb08 at 200 predicts 51.0 Hz, measured 53.0.
- VES082_L at 400 predicts 101.5 Hz, measured 107.1. The excess is presumably recurrent excitation.

The mapping fails once the network runs away: DNg100 at 800 predicts 40 Hz but measured 0.

| target DN rate | DNg100 input (s = 16.6-16.7) | DNb08 VES082_L input (s = 3.35) | other DNb08s (s = 3.74-3.82) |
|---|---|---|---|
| 10 Hz | ≈290 | ≈59 | ≈66 |
| 20 Hz | ≈460 | ≈92 | ≈104 |
| 30 Hz | ≈630 | ≈126 | ≈143 |
| 40 Hz | ≈800 | ≈161 | ≈182 |
| 60 Hz | ≈1,160 | ≈233 | ≈262 |
| 100 Hz | ≈1,950 | ≈393 | ≈444 |

**What the evidence supports.**
- **DNg100: about 20-40 Hz during steady walking, plausibly 10-60 Hz; about 0-10 Hz at rest.** That is input ≈460-800
  (range 290-1,160).
  - Basis: the walking means of the DNs actually recorded (DNa02 ≈20-52 Hz, DNg13 ≈63 Hz, MDN up to 75 Hz while
    backing).
  - DNg100's calcium signal grades with forward speed, so its rate should rise with speed.
  - Confidence: low. DNg100 itself has never been recorded. The proxies steer or walk backward. DNg100 is large (s ≈ 17)
    and might fire differently.
  - Rung 5's 16 Hz is at the low edge of this range. Inputs between the accepted 400 and the runaway 800 were never
    sampled, and that gap is where flies' rates probably sit.
- **DNb08: about 20-100 Hz while it drives leg movement.** That is input ≈90-390 for the left VES082.
  - Basis: only the general range of DNs during vigorous movement. There are no DNb08 data.
  - Confidence: very low.
  - Brainfly's passing drive (200, ≈53 Hz for the left VES082) sits inside this range. So does 400, where the two left
    neurons fired ≈100-107 Hz and were rhythmic in 7-8 of 16 runs.
- **The behaviors that define both neurons came from optogenetic drive of unknown rate.** CsChrimson at comparable
  intensities drives other DNs to ≈100-500 spikes/s (Ache 2019) and DNa02 to ≈100 (Yang 2024). So headless flies'
  3.5-12 Hz stepping under DNg100 light may reflect DN rates well above natural ones. This is an inference, not a
  measurement.
- **The frequency band is supported, with a caveat.** DNg100 alone in decapitated flies steps at ≈7.6-8.3 Hz on a ball
  (3.5-5.5 Hz in Pugliese's flies), ≈11-12 Hz in air and ≈8 Hz on amputated stumps. Silencing the femoral chordotonal
  organ brings air-stepping down to the amputated level. Brainfly's front-leg network has no proprioceptive feedback, so
  the amputated (≈8 Hz) and air-stepping (≈11-12 Hz) values are its closest benchmarks. Its 11.6-13.7 Hz at a 16 Hz DN
  rate is at or above them. Higher DN rates would push it further up if the Pugliese sweep's trend holds.

**What would test it.**
- **Record DNg100 whole-cell in walking flies.** Yang et al. recorded DNg13, another gnathal-ganglion DN, in walking
  flies, and the DNg100 split (VT058557-AD; R85F12-DBD) exists. Report rate at rest, at walking onset, and against
  forward speed.
- **Calibrate DNg100's rate under CsChrimson** at the intensities used (0.01-0.33 mW/mm²), as Ache et al. did for
  DNp07/DNp10. That would turn the headless frequency-intensity curves (Pugliese Fig. 2j; Sapkal 2026 Fig. 1e) into
  step frequency against DN rate, which brainfly can be scored on directly.
- **Record DNb08 (SS70620),** for example during unloaded leg searching or male aggression, and measure the frequency of
  its evoked leg rhythm. Neither is published.
- **In brainfly now, without new data:**
  - Pre-register a sweep of DN rates spanning flies' range: DNg100 at 10, 20, 30 and 40 Hz (inputs ≈290, 460, 630
    and 800) and DNb08 at 20-100 Hz. Ask whether the rhythm survives without runaway, and whether its frequency rises
    with rate as headless flies' stepping rises with light.
  - Co-driving DNg97 with DNg100 should speed the rhythm, as in Sapkal et al. 2026 (≈8 → 12 Hz on a ball). That is a
    falsifiable prediction for the same network. DNg97 needs inputs of about 200-540 for 10-40 Hz (s = 10.9-11.5).
  - Brainfly's rung 4 notes report that raw DNa02 recordings with ball velocity are on Harvard Dataverse
    (10.7910/DVN/0NCLP1). They could give the full distribution of one walking DN's rate.

**Not read.** Dallmann et al. 2026 (bioRxiv,
[doi:10.64898/2026.01.04.697356](https://doi.org/10.64898/2026.01.04.697356); Roadrunner neurons upstream of a
forward-walking DN population, with patch-clamp of the brain neurons) could not be read in full: bioRxiv rate-limited
fetches. The part read names no recorded DNs. The cricket rate-speed paper (Böhm & Schildberger 1992) was not accessible.
