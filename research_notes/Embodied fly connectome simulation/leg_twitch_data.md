# Front-leg tibia flexor: measured force and twitch data

The main source is Azevedo, Dickinson, Gurung, Venkatasubramanian, Mann & Tuthill 2020, eLife 9:e56754 ([e]). The author is Gurung, not Gorko.

Tags: **computed** means my own calculation. **read** means digitized from the published figure TIFF against its axes (about ±5%). Checked 2026-09-28.

## 1. Force per spike (peak force at the probe)
- Summary: "Slow motor neurons produce <0.1 µN per spike, while fast motor neurons produce ~10 µN per spike, approximately equal to the fly's weight." ([e])
- Fast MN: "a single fast motor neuron spike produced ~10 μN of force, resulting in a 50 μm movement of the force probe". n = 7 cells (Fig 4F). ([s2-3])
- Fast MN range (**read**, Fig 4D at 1 spike): 5.4–15.4 µN; mean 9.0 µN over 6 separable cells (**computed**). ([f4])
- Intermediate MN: "An intermediate neuron spike produced ~1 μN that moved the tibia 5 μm". n = 6 cells (Fig 4F). ([s2-3])
- The figures give lower intermediate values (**read**): 0.3–0.5 µN in Fig 4D, and 2.7–4.0 µm in Fig 4E. The latter is 0.6–0.9 µN (**computed** as ×k). ([f4])
- Slow MN: the Fig 4D fit is labelled "m = 0.013 µN/spike" (n = 9). Spikes are counted as "the average number of spikes during positive current injection steps minus the baseline firing rate". ([f4])
- These are peak forces at the probe near the tibia tip (§4): "Peak average force vs. number of spikes". Figs 4D–F include "drag and inertia". ([f4], [s4-3])
- Not isometric: 50 µm at a 417 µm lever arm is ≈6.9° of joint rotation (**computed**).
- Joint torque (**computed**, F × 417 µm): ≈4.2 nN·m per fast spike; ≈42 nN·m at 100 µN.

## 2. Single-spike twitch time course
- Paper: "the effect of a spike in the fast and intermediate motor neurons reached half maximal force in ~8.5 ms (Figure 4H)". ([s2-3])
- Fig 4H per cell (**read**): fast 7.7–9.7 ms, mean 8.4 (n = 7). Intermediate 6.3–8.9 ms, mean 7.6 (n = 6). Legend: "p=0.2". ([f4])
- Authors' method ([code][c1]): the time from the somatic spike until a line fitted to the rising phase reaches 50% of the mean per-trial peak. One fast cell is hard-coded to "0.0077" s.
- Time to peak and decay are not reported in the paper.
- Single fast-spike trial (**computed**; Fig 1—figure supplement 2C, drag and inertia included; times from the EMG spike) ([f1s2]):
  - Peak 11.2 µN at ≈17 ms; half-max at ≈7 ms.
  - Half-decay ≈12 ms after the peak; full width at half max ≈21 ms; baseline by ≈52 ms.
- Overlaid 1-spike trials in Fig 4A/B (**computed**, median across traces) ([f4]):
  - Fast: half-max 11.5 ms, peak 23 ms, half-decay 16 ms after the peak, decay τ ≈13 ms (exponential fit from 90% to 20% of peak).
  - Intermediate: half-max 11.8 ms, peak 20 ms, half-decay 18 ms after the peak, τ ≈17 ms.
  - These half-max values run ~3 ms later than every Fig 4H value, so trust the shape more than the timing. Video was "170 Hz" (5.9 ms frames). ([s4-3])
- Slow MN: force was "gradual and did not reach its peak within 500 ms"; hyperpolarization "required ~100 ms". ([s2-3])

## 3. Force vs spike number and rate
- Summation: "the force produced by two spikes was ~1.6X the force produced by a single spike (Figure 4E) and the force-per-spike curves saturated at ~10 spikes". The authors attribute the saturation to fatigue. ([s2-3])
- Two-spike ratio (**computed**, Fig 4E dots): 1.4–1.6. The example inter-spike interval is ≈12 ms (**read**, Fig 4A). ([f4])
- Plateau (**read**, Fig 4D): fast ≈28–30 µN at 9–17 spikes; intermediate ≈3–4 µN at about 30 spikes. ([f4])
- No sustained-rate or tetanus data exist for fast or intermediate MNs. Spikes came from "Brief (10–20 ms) flashes", and burst rates were not reported. ([s2-3])
- Slow MN tonic firing: "a resting spike rate of approximately 30 Hz" that "maintains constant force on the probe". ([s2-2], [s2-3])
- Slow MN tonic force: MLA "reduced the resting force on the probe by ~1.5 μN". Hyperpolarizing one slow MN cut force by ≈0.3–1.5 µN (**read**, Fig 4F). ([s2-3], [f4])
- Slow MN gain (**computed**): the code counts spikes as Δrate × 0.5 s ("firing rate *stim dur", [c2]). So 0.013 µN/spike ≈ 0.0065 µN per Hz above rest. This is the peak within a 0.5 s step, not steady state.
- Example slow cell in MLA (**read**, Fig 4C): ≈45, 55 and 72 Hz gave ≈0.8, 1.25 and 1.9 µN at step end, still rising. ([f4])

## 4. Measurement setup
- Flies: "female flies, 1–4 days post eclosion", "at room temperature". Leg: right T1, "the fly's right front femur and tibia". ([s4-2])
- Mounting: "The front legs were glued to the horizontal top of the holder, the coxa aligned with the thorax, and the femur positioned at a right angle to the coxa and body axis." ([s4-2])
- The femur is fixed; the tibia swings "in an arc at an angle of ~50–65° to the top surface of the holder". ([s4-2])
- Probe position: "The probe tip was positioned near the end of the tibia, giving a lever arm of 417 ± 7 (s.d.) μm across flies (n = 8)." ([s4-4])
- Joint angle: the tibia was set "approximately at 90° to the femur". "A 60 μm movement of the probe resulted in an 8° change". ([s4-4], [f6])
- The angle during force trials is not stated. Inference: the force code keeps only probe "Position == 0" ([c3]), probably the 90° home position.
- Probe: a paint-brush fiber, "k = 0.2234 µN/µm", "m = 0.1702 mg", "protruded approximately 1.5 cm". It has "a relaxation time constant of 2.5 ms and oscillation period of 5.8 ms". ([s4-3])
- Drag typo: the Methods say "c = 0.1377 kg/s", the figure "c = 0.14E-3 kg/s". Only the figure value gives τ = 2m/c = 2.47 ms and a 5.86 ms damped period (**computed**). ([f1s2])
- Maximum: "close to 100 μN of force at the tip of the tibia and changes in force of ~1.3 mN/s". The 400 µm maximum deflection is ≈89 µN (**computed**). ([s2-1])
- Saturation: "F ~ 85 µN". Only lateral motion was tracked, so forces "may be slightly underestimated". ([f1], [s4-3])
- Tibia length: not given. Wang et al. 2025 list the prothoracic tibia as "452.4" µm under "Ellipsoid radii", so radius versus length is unclear ([w]). Read as a length, the probe sat at ≈0.92 of the tibia (**computed**).

## 5. MN identity and counts
- Lines: "three lines that each label a single tibia flexor motor neuron". R81A07-Gal4 is fast, R22A08-Gal4 intermediate, R35C09-Gal4 slow. ([s2-2])
- Input resistance: "The input resistance was 150 MΩ for fast motor neurons, 300 MΩ for intermediate motor neurons, and 700 MΩ for slow motor neurons". Measured from "−5 pA" steps; n = 15, 11, 14. ([s2-2], [f3])
- Axon diameter (**read**, Fig 3A): fast ≈2.0–2.8 µm, intermediate 0.9–1.8 µm, slow 0.5–1.1 µm. ([f3])
- Pool: "approximately 15 motor neurons". The fast MN "is the only motor neuron that innervates the large tibia flexor muscle fibers in the middle of the femur". "2–5 neurons" innervate the proximal fibres; the slow MN "is one of 8–9" at the distal tip. ([s3-2])
- FANC left T1 (Azevedo 2024, Fig 4c): "Ti flexor (5)", "Acc. Ti flexor (10)", "Ti extensor (2)", of "all 69 left T1 MNs". ([F])
- FANC fibre counts (**read**, Fig 4a): tibia flexor 26, accessory tibia flexor 29, tibia extensor 36. ([F])
- Mapping (Lesser 2024, Fig 4c,i): fast and intermediate are tibia flexor MNs 5 and 4, the two largest. Slow is accessory tibia flexor MN 2. Labels: "10 µN per MN spike" and "0.013 µN per MN spike". ([L])
- MN size marks fast versus slow: "Tibia flex A MNs are ordered by surface area". "The largest leg MN in the fly, the fast tibia flexor, has nearly 1 cm of total dendritic length". ([L], [F])
- Other markers:
  - Synapse count scales with MN area, at "around 0.45 synapses μm−2".
  - GFC4 escape input reaches only "the largest MNs that innervate trochanter–femur and tibia flexor muscles".
  - The biggest MNs get the most input yet are "rarely recruited". ([L], [F])

## 6. Other Drosophila leg muscles (brief)
- Tibia extensor: 2 MNs. "The SETi receives 7,090 input synapses, and the FETi receives 14,904" ([F]). No force data found.
- Gorko et al. 2024 is about neck MNs ("the motor neurons that control head movement"), not FeTi. ([G])
- Jump muscle (T2 trochanter/femur): "101+/-4.4 microN"; "The force takes 8.2 ms to reach its peak". Force was unaffected over "75-120 degrees" of femur–tibia angle. ([Z])
- Passive joints: torque is "well approximated by a linear spring" and "seventy times smaller than necessary to support the weight". Active force decays with "a time constant of ∼100 ms". The paper's stiffness units are inconsistent. ([w])
- Coxa and trochanter: no twitch or force data found. FANC gives only MN counts, e.g. "Tr flexor (8)". ([F])

## 7. Data availability and a surprise
- Dryad: 60 files, 48.76 GB in total, with per-cell zips of 164 MB–5.5 GB. The fast and intermediate force cells alone exceed 4 GB, so **nothing was downloaded**. Downloads also need a token or a bot check. ([D])
- eLife has no source data. Cell IDs come from the authors' code: 7 fast, 7 intermediate (6 used for single spikes) and 9 slow. ([c3])
- Fig 4E's axes say µN, but its legend says "Peak probe displacement" and the values match µm. ([f4])

[e]: https://elifesciences.org/articles/56754
[s2-1]: https://elifesciences.org/articles/56754#s2-1
[s2-2]: https://elifesciences.org/articles/56754#s2-2
[s2-3]: https://elifesciences.org/articles/56754#s2-3
[s3-2]: https://elifesciences.org/articles/56754#s3-2
[s4-2]: https://elifesciences.org/articles/56754#s4-2
[s4-3]: https://elifesciences.org/articles/56754#s4-3
[s4-4]: https://elifesciences.org/articles/56754#s4-4
[f1]: https://elifesciences.org/articles/56754#fig1
[f1s2]: https://elifesciences.org/articles/56754#fig1s2
[f3]: https://elifesciences.org/articles/56754#fig3
[f4]: https://elifesciences.org/articles/56754#fig4
[f6]: https://elifesciences.org/articles/56754#fig6
[c1]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Script_alignSingleSpikes.m
[c2]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Script_forcePerSpike.m
[c3]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Dataset3_SlowInterFast_ForcePerSpike.m
[D]: https://doi.org/10.5061/dryad.76hdr7stb
[F]: https://www.nature.com/articles/s41586-024-07389-x
[L]: https://www.nature.com/articles/s41586-024-07600-z
[G]: https://doi.org/10.1038/s41586-024-07222-5
[Z]: https://doi.org/10.1242/jeb.01181
[w]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12324252/
