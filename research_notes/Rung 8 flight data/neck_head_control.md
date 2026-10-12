# Neck motor neurons and head control: anatomy, wiring, physiology and behaviour for a first visual-to-neck probe

Read 2026-10-11. Groundwork for rung 8's head-pose arm: a first whole-network probe in which wide-field visual motion
reaches the neck motor neurons (MNs) through lobula plate tangential cells (LPTCs) and descending neurons (DNs), and
the fly data to pre-register it against.
- Wing power MNs are in `dlm_splay_state.md`.
- DN and nerve-cord background is in `../Embodied fly connectome simulation/descending_vnc_motor.md`.
- Neck mechanics in body models are in `../Embodied fly connectome simulation/muscles_biomechanics_body_models.md` §4.

## Summary: what a model test should use

1. **The neck MN set.** MaleCNS v1.0 has 49 neck MNs, about 25 per side [D]. 44 carry subclass `nm`: 24 in the nerve cord (T1 somata) and 20 in the brain (labial-neuromere somata). The other 5, GNG647 (3 cells) and GNG314 (2), are typed as retinal MNs (`rm`, exit nerve "ON"), but BANC matches them to VCvN1–3. BANC v888 also has 49 (yaw 14, roll 12, pitch 8, roll-pitch 2, unassigned 13) [D]. Gorko et al. 2024 give "about 25" pairs; the blowfly has 21 per side (§6). `experiments/vnc/relay.py`'s "neck" pool (all 107 `cb_motor` neurons) is a different set. (§2.1, §2.3)
2. **Who moves what (Gorko et al. 2024; BANC).** Pitch down (ventral longitudinal muscles): CvN4–7, model labels CB0899, CB0838, CB0916 and CB0831. Yaw (oblique and transverse horizontal muscles): VCvN1–3 (GNG647 = CB0918, GNG314 = CB0004), CvN1/2 (GNG653 = CB0706) and, in the nerve cord, CvNA1/A2 (ADNM1/ADNM2 MN). Roll: CvN3 (GNG648 = CB0913) and DProN1–4 (MNnm11, MNnm13, MNnm07/12, MNnm03); DProN5 (MNnm08) rolls and pitches. GNG283 and GNG276 (both CB0705) are unmatched brain MNs with yaw-like inputs. CvN6, CvN7, CvN9 and CvNA1/A2 have their somata on the side opposite their nerve [D]. (§1.2, §1.4, §2.2)
3. **Direct LPTC input reaches only the brain MNs [D].** Synapses per neuron: CvN7 ≈100 from soma-side VS; CvN6 105–109 from soma-side VS, 33–44 from the opposite HSS and 11–26 from soma-side H2; CvN5 64–69 from the opposite side's VS; CvN4 20–22. These VS cells are the frontal ones (estimated RF azimuth ≈47–76°, ≈VS1–3). The VS and HSS counts match Gorko's FAFB counts (CvN6: VS1–3 127, HSS 41; CvN7: VS1–3 123, HSS 1) within ≈20%. The yaw MNs take soma-side HS and opposite-side H2: per side, GNG283 gets HS 101–115, H2 65–77 and HST 52–85 (3.4% of its input, the largest LPTC share of any neck MN), and GNG647 HS 59–88 and H2 26–28. The shares are small: VS → CvN6/7 is 1.2–1.4% of each MN's input. Across neck MNs, 37% of input comes from DNs, 26% from ascending neurons and about 30% from interneurons; 46% is inhibitory-signed. (§3.1–3.2)
4. **The nerve-cord neck MNs hear LPTCs only through DNs [D].** DNp15 (DNHS1) takes 13.3% of its input from LPTCs (soma-side HSN 126–138 and HSE 78–122, opposite-side H2 201–253) and makes 947 neck synapses (MNnm11 349, ADNM1 232, MNnm14 124, ADNM2 116, FNM2 99). DNp20 (DNOVS1) takes soma-side VS 442–494 (9–10%) and VST2 290 but makes only 208 chemical neck synapses; it is graded, has a 4.5 µm axon and is dye-coupled to frontal neck MNs, so its route is probably electrical. DNp22 (DNOVS2): 5.7% LPTC input, 167 neck synapses. Two-hop weights HS → DNp15 → CvNA1/A2 and MNnm11 are 0.0009–0.0015, about a tenth of the direct VS → CvN6/7 weight (0.012–0.013). The four DNs with the most neck output (DNge033, DNge002, DNa06, DNg93; ≈4,300–5,000 synapses each) take ≤0.5% of their input from LPTCs. (§3.3–3.4)
5. **CvN7, the only Drosophila neck MN recorded (Gorko et al. 2024; female, head-fixed, not flying, 22 °C) [P, SD].** Rin 150–200 MΩ; rest −45 to −55 mV; spikes on current injection. It depolarizes and spikes to downward, not upward, local motion on the eye contralateral to its axon, fronto-dorsally and laterally (in the authors' RF map, largest from 60° toward the soma side to 30° past the midline at elevation 0–60°, peaking at 2.8 mV 60° lateral and 30° up [D]). To a star field rotating about 12 horizontal axes 30° apart (one cell, 5 trials) the response is graded and on average subthreshold: +1.42 mV at the best axis, −1.76 mV at the worst, ≈3.2 mV peak to peak. The best body-rotation axis is at azimuth 60–90° (62°, elevation 9°, predicted from the RF map): nose-up pitch mixed with roll. Optogenetic drive makes it fire up to ≈200 Hz [fig./D]. (§1.3)
6. **HS and VS cells [P, fig.].** Graded potentials with small spikes ("spikelets"). Rest −44.7 mV (VS) and −50.0 mV (HS) in Suver et al. 2016, ≈−55 mV in Joesch et al. 2008 and Schnell et al. 2010 (LJP-corrected). Rm 140–151 MΩ (Kim et al. 2017); HS τm 4.3–4.9 ms (Cuntz et al. 2013). At 1 Hz with 40–50° gratings: preferred direction +8–12 mV, null/preferred ratio −0.35 to −0.55. Temporal-frequency optimum ≈1 Hz at rest. Star-field yaw at rest: HS 5.6, VS4–6 2.5, VS1–3 0.8 mV; VS1–3 respond most to pitch. Preferred horizontal rotation axes in flight: VS1–3 +121 to +164°, VS4–6 −120 to −165°, HS −24 to +5° (Suver et al.'s convention). HSN's visual latency is 24 ms to a 1,000°/s sweep. (§4.1)
7. **The LPTC-recipient DNs (Suver et al. 2016; females, 20 °C; star field at 22.5°/s about 13 horizontal axes 15° apart, 2 s) [P, fig.].** DNOVS1 (DNp20): graded; preferred axis −139.9°; ≈6–7 mV between null and preferred axes in flight, ≈2–3 mV at rest; rest −46.7 mV. DNOVS2 (DNp22): small spikes; +144.3°; ≈8 → 48 Hz in flight (≈0–5 → 22 Hz at rest); 8.2 Hz/mV; rest −40.9 mV. DNHS1 (DNp15): small spikes; −7.5°, and stronger to pure yaw than to any horizontal-axis rotation; ≈10 → 38 Hz in flight (≈3 → 12 Hz at rest); 5.9 Hz/mV; rest −43.1 mV. In calcium imaging, DNp15 prefers binocular yaw over binocular front-to-back motion more than HS does (discrimination index ≈−0.65 against ≈−0.1; Erginkaya et al. 2025) [fig.]. (§4.2)
8. **Head yaw benchmarks, rigid tether, flight [P, fig.].** Single sines of a 30° grating at 250°/s peak (Cellini & Mongeau 2022): head gain 0.37–0.51 from 0.7 to 10.6 Hz, phase +40° to −95°. Sum of sines at 1–9.6 Hz (Cellini & Mongeau 2020): gain 0.47–0.71, phase +20° to −50°; the head follows within 10 ms, the wings lag by more than 40 ms. Constant rotation, 30° period at 112.5°/s (3.75 Hz): head yaw peaks at 10–15° at every contrast from 0.09 to 0.98, and the response starts 73–120 ms after onset, against 92–220 ms for the wings (Duistermars et al. 2012). Head tuning peaks at 120°/s for a 1 Hz triangle wave (Rauscher & Fox 2024). Yaw is limited to about ±15°, and reset saccades fire at ±9°. With the body free to yaw (magnetic tether), the head is high-pass: gain 0.05 at 0.7 Hz to 0.36 at 10.6 Hz. (§5.1, §5.3)
9. **Manipulation benchmarks [P, fig.].** Kir2.1 in HS/VS halves the head optomotor response (peak ≈3.5–4° → 1.8–1.9°) and barely changes the wings' (Kim et al. 2017). Unilateral HS activation (+4.4 mV) turns the head toward the stimulated side, by 1.35° in sighted and 3.05° in blind non-flying flies (Haikala et al. 2013). Immobilizing or removing the halteres cuts head optomotor amplitude from 5.7° to 2.8° or 2.0° (Rauscher & Fox 2024). Unilateral DNp03 activation turns the head ≈2.5–4° away from the activated side (Croke et al. 2026). In flight, head pitch is largest for downward pitch motion (Suver et al. 2016, n = 56). (§5.2)
10. **One MN's effect on the head, for a later rung with a head [P, M].** Activating CvN7 pitches the head down about an axis at azimuth 69°, elevation 18°, toward a set pose (≈12° pitched down) from any start. Single MNs move the head at 20–115°/s at peak, starting within ≈10 ms of light onset and peaking at 20–55 ms. A pose-plus-velocity feedback model predicts held-out trials better than a feedforward one (NRMSE 0.4 against 0.6). Silencing the lateral neck chordotonal neurons raises CvN7's pitch speed from 34 to 60°/s and moves the set pose to 19° (in the model, pitch-velocity feedback −53%). A fitted transfer function from visual slip to head yaw (magnetic tether; Cellini et al. 2022): G_head = e^(−0.02s)·0.037s/(0.063s + 1). (§1.4–1.5, §5.1)
11. **Expected directions, and one to hold back [D].** Pitch: every pitch MN reads frontal VS cells on the eye opposite its nerve (CvN6/7 take soma-side VS and their axons cross; CvN5 takes the other side's VS and doesn't cross) and pitches the head down. Downward motion in that field comes from nose-up pitch and from body roll lifting that side, so this compensates. Yaw: the right VCvN gets right HS and left H2, which both signal clockwise world rotation seen from above (the fly turned left); compensating means turning the head right, toward its nerve, as blowfly VCNM tuning and ADN stimulation suggest. Read literally, Gorko's plotted roll and yaw signs give the opposite, so pre-register the direction of yaw and roll head turns only after checking his raw axes. (§1.6, §3.6)
12. **State gating is the main caveat.** Flies' neck-motor visual responses are small at rest and large when active. In blowflies, head yaw optomotor amplitude is 30–40× larger in flight than at rest, and VCNM depolarizes ≈20 mV, centrally, while the halteres beat (Haag et al. 2010); "type II" neck MNs don't spike to vision unless the halteres oscillate (Huston & Krapp 2009). In Drosophila, DN responses are ≈2–3× larger in flight (Suver et al. 2016), and VS and HS responses grow most at 2–8 Hz (Suver et al. 2012; Schnell et al. 2014). Mureli et al. 2017 saw visually guided head movements only in flight, though Haikala et al. 2013 measured ≈3° in non-flying flies. Brainfly has no flight state or octopaminergic gain, so the fair targets now are quiescent data (CvN7's recording; Suver's quiescent DN ranges) and ratios, not flight amplitudes. (§4, §5.1, §6)
13. **What the chemical connectome cannot show.** Gap junctions sit at most visual entry points to the neck: HSN/HSE with VCNM-like and HSS with CNM-like MNs, HS with DNp15 (kept in shakB FlpStop flies), DNOVS1 with VS4–6 and frontal neck MNs, DNOVS2 with VS2–3 (Pokusaeva et al. 2024; Suver et al. 2016), and in blowflies CNMN6/7 with VS2/3, contralateral HSS and each other (Wertz et al. 2012). No coupling strength has been measured in Drosophila, so any junction imposed with `HybridBrain.set_coupling` is a free parameter to state before the run. Also missing: ocellar drive (MaleCNS has no ocellar ganglion; OCG01b/f carry ≈6% of CvN6's input), graded transmission (flies' HS, VS and DNOVS1 don't spike; brainfly's do) and flight or octopamine gain. (§3.7, §8)
14. **Mechanosensory inputs the connectome does show [D].** Haltere afferents (SApp types, ≈300 cells in the haltere nerve) make ≈12,900 synapses directly onto neck MNs (≈4% of their input; ≈11% of CvN6's), and inhibitory GNG546/327/529 add a disynaptic negative route. The prosternal hair plate (SNpp19) drives mainly DProN4, the levator (673 synapses, 5% of its input). Neck chordotonal afferents reach neck MNs only through ascending neurons. In blowflies, haltere deflection excites neck MNs after 2.5–3 ms (Sandeman & Markl 1980), far faster than vision (≥22 ms for head pitch). (§3.5, §6)
15. **Stimuli and read-outs for a first probe.** Wide-field rotation about 12 horizontal axes 30° apart (Gorko) or 13 axes 15° apart at 22.5°/s (Suver); local up/down patches in CvN7's RF; temporal frequency near 1 Hz, the LPTC optimum at rest; the existing optomotor drum (30° period, 40°/s, 1.33 Hz) for yaw. Read out the brain neck MNs' rates, VS and HS by RF rank, and DNp15/20/22. Pre-register signs, axes and selectivity ratios rather than mV or Hz, with degree-preserving rewiring and VS → CvN deletion as nulls. (§7)

Conventions:
- [P] stated in the cited paper (quoted where the wording matters).
- [A] stated in an abstract only; the full text wasn't read.
- [PP] stated in a preprint version; the published paper may differ.
- [fig.] read off a published figure by eye, about ±5%.
- [SD] taken from the authors' data files or code (Gorko et al.'s Bitbucket repository).
- [D] derived by me: queries of brainfly's MaleCNS tables (`~/fly-data`, minconf 0.5) or BANC's metadata (scripts in the scratchpad, not the repo), or arithmetic.
- [M] a value inside a published model.
- [2°] known only through later citation or a review.
- Combined tags, with "/" or ",", mean both: [P/fig.] is stated and read off a figure; [fig./D] is counted from a figure; "SI" is the paper's Supplementary Information.
- Other species are named where they appear. §6 is about blowflies (mostly Calliphora) and other non-Drosophila flies throughout.
- MaleCNS synapse counts are signed by the presynaptic neuron's consensus transmitter (GABA, glutamate and histamine negative), as in the model.
- "Soma side" is the side of an MN's cell body and "nerve side" the side where its axon leaves; they differ for CvN6, CvN7, CvN9 and CvNA1/A2.
- Rotation axes follow each source's convention. Suver et al.'s azimuths are their own; Gorko's frame is in §1.6.

---

## 1. Gorko et al. 2024, Nature 628:596 ("Motor neurons generate pose-targeted movements via proprioceptive sculpting") [P, SD]

The only study of identified Drosophila neck MNs: anatomy, one MN's visual physiology, and single-MN activation for 16
MN types. Full text from the Tuthill lab copy; Supplementary Information and Peer Review File from Springer; figure
code and the CvN7 tuning and receptive-field data from the authors' Bitbucket repository.

### 1.1 Preparation

- Behaviour: male flies, 5 days old, retinal-fed, cold-tethered, then 30 min recovery, **tethered flight**. The flies carry
  norpA (blind) "and did not show any behavioural reaction to the red light stimulus". Two cameras at 125 frames/s, 3D
  head tracking (APT, 5 head points; mean error 0.9° roll, 1.2° pitch, 3.2° yaw on hard frames). Stimulus: 300 ms flashes
  of 625 nm at 0.37 mW/mm², every 1.5 s, 120 flashes per fly. CsChrimson was expressed stochastically in single MNs and
  each fly was dissected afterwards to identify the stimulated neuron [P].
- Unilateral stimulation for every MN except CvN7: "in the case of a yaw-inducing motor neuron, the left and right
  neurons of the bilateral pair will drive the head to move in opposite directions". CvN7 was stimulated uni- or
  bilaterally because "both motor neurons in the bilateral pair drive the same pitch movements" [P].
- Electrophysiology (CvN7 only): female SS00754 > GFP flies, head-fixed, **not flying**, saline at 22 °C, whole-cell
  current clamp, no holding current. "Input resistances ranged between 150-200 MΩ and the resting membrane potential
  ranged between -45 to -55 mV, spikes could be elicited by current injection" [P, SI].
- Visual stimuli: three orthogonal 360 Hz projector screens (green LEDs) forming a cube corner, perspective-corrected and
  rotated for each fly's measured head angle. Receptive fields were mapped with a 5° black dot scanned at 50°/s in four
  directions; wide-field tuning used a "star field" rotated about different axes [P, SI].

### 1.2 Anatomy: nerves, MN groups, muscles

- "Many behaviours incorporate head movements, which in the fly are controlled by about 25 motor neurons driving small
  muscles in the neck". Their driver library "expressed in at least 16 of the about 25 pairs of motor neurons that drive
  fly head movements" [P].
- Four outputs (Extended Data Fig. 7g) [P]:
  - **CvN** (cervical nerve; Strausfeld's CN), "which branches from the cervical connective half way down its length".
    CvN1–8 have somata in the brain and descend the connective.
  - **VCvN** (ventral cervical nerve; Strausfeld's VCN), which "branches from the subesophageal zone where it meets the
    cervical connective". Its three MNs could not be told apart and were treated as one class.
  - **DProN** (dorsal prothoracic nerve; "called frontal nerve/FN in Strausfeld"). DProN1–5 have VNC somata.
  - **CvN A1–A2**, which "ascend from the ventral nerve cord to reach the Cervical nerve". They are "likely homologous to
    ADN1-2 in the blowfly", whose own thin anterior dorsal nerve "is missing" in D. melanogaster.
  - So the blowfly's ADN (anterior dorsal nerve, prothoracic) is not the ADMN (anterior dorsal mesothoracic nerve). In
    MaleCNS the ADMN carries only wing MNs (§2).
- "Most neck muscles do not directly enter the neck and are contained in the fly's thorax". They act through long
  tendons or by moving the cervical sclerite. Three small oblique horizontal (OH) muscles have tendons that fuse at ≈45°
  with the large transverse horizontal (TH) tendon (Extended Data Fig. 8, "The tendons of yaw muscles are coupled").
  "Most muscles are innervated by a single motor neuron" [P].
- Named muscles (Extended Data Fig. 7): SC-CO DV1–2 (dorsoventral, cervical sclerite to condyle), VL1–2 (ventral
  longitudinal), DE (depressor), SC-RO (sclerite rotator), SC-RE (sclerite retractor), LEV (levator), TH1–2, OH (a group
  of 3), AD (adductor) and ABD (abductor). That is about 15 muscles per side (my count of the legend).
- **MN → muscle map (Fig. 4h)** [fig., exact cells read from the table]:

  | MN | Muscle | | MN | Muscle |
  |---|---|---|---|---|
  | VCvN (3 cells) | OH | | CvN A1 | TH1 |
  | CvN1 | TH1 | | CvN A2 | TH2 |
  | CvN2 | OH | | DProN1 | SC-CO DV1 |
  | CvN3 | SC-RO | | DProN2 | SC-CO DV2 |
  | CvN4 | VL2 | | DProN3 | DE |
  | CvN5, CvN6, CvN7, CvN8 | VL1 | | DProN4 | LEV |
  | | | | DProN5 | AD |

- Proprioceptors (Fig. 3, Extended Data Fig. 5) [P]:
  - The **neck chordotonal organ** is "strung parallel to the neck muscles by connective tissue". Two afferent types: lateral
    (LNC) and medial (MNC). Both "project to the ventral nerve cord through the prothoracic nerve", via the dorsal medial
    tract.
  - The **prosternal organ** (hair plate) is the other proprioceptor manipulated.
- CvN6 and CvN7 were reconstructed in FAFB (CATMAID skeletons 1167858 and 1337777). Synapses from LPTCs (Fig. 1b inset)
  [P]:

  | | VS1 | VS2 | VS3 | H2 | HSS |
  |---|---|---|---|---|---|
  | CvN6 | 50 | 70 | 7 | 17 | 41 |
  | CvN7 | 25 | 81 | 17 | 0 | 1 |

  "HSS is ipsilateral to the motor neuron axons, VS1–3 and H2 are contralateral."

### 1.3 CvN7 physiology (the only Drosophila neck MN recorded)

- Local motion: CvN7 depolarizes and spikes to downward motion and does not to upward motion (Fig. 1c, 5 mV scale bar).
  The RF lies on the eye contralateral to the axon, fronto-dorsal and lateral [P/fig.].
- Authors' RF-map data [SD, `mapData_rfMapping_started_172847.mat`]:
  - The local response is largest for downward motion at azimuth −60 to +30° (file's convention), elevation 0–60°.
  - The peak is −0.028 V × 100 = 2.8 mV at azimuth −60°, elevation +30° (×100 converts the ×10-gain volts to mV, as the
    authors' script does).
  - The recorded cell's soma was on the fly's left and its axon on the right (`plotEgRfMap.m`), so its RF is on the left
    eye. The file's azimuth must then be positive to the right, as in Krapp's convention, which puts the peak 60° to the
    left, on the soma-side eye [D].
- **Wide-field rotation tuning** [SD, `20130806RotAxisTcurveData.mat`]: one cell, 5 trials, 12 rotation axes in the
  horizontal plane, mean Δ membrane potential in mV.
  - Visual axis azimuth −90, −60, −30, 0, 30, 60, 90, 120, 150, 180, 210, 240°: +1.00, +0.15, −0.12, −0.66, −1.33, −1.76,
    −1.76, −0.45, +0.93, +0.75, +0.73, +1.42 mV.
  - Peak to peak ≈ 3.2 mV. The response is graded, sub-spike-threshold on average.
  - The authors' script plots the **body-rotation axis** (visual axis + 180°) in Krapp's convention (0° frontal, +90°
    right). The axis predicted from the RF map is azimuth 62°, elevation 9° (`bestAxis = [62,9]`), which matches the
    measured peak (body axis 60–90°).
  - In words: CvN7 is driven by the visual consequence of a nose-up pitch, mixed with roll, of the body [SD/D].
- Optogenetic calibration (Extended Data Fig. 3; female, non-flying): 300 ms light at 0.04 / 0.09 / 0.37 / 1.43 mW/mm².
  - My dot counts of the rasters [fig./D]: ≈15–20 Hz, ≈55–60 Hz and ≈180–215 Hz for the first three. At 1.43 mW/mm² the
    cell sits depolarized with small fast spikes. 0.37 mW/mm² is the behavioural intensity.
  - "When using identical stimuli to activate CvN7 neurons in our behavioural experiments we observed convergent head
    movements, regardless of stimulus intensity". Higher intensity only raised the speed of approach [P].
  - So **CvN7 can fire at ~200 Hz**.

### 1.4 What single MNs do to the head

- CvN7: "activation pitches the head downward as predicted from its visual responses (Fig. 1g, mean axis of head rotation:
  69° azimuth, 18° elevation with a spherical variance of 0.09)". The visual and motor axes are roughly parallel, so the
  MN turns "the visual consequences of the fly rotating in space into the appropriate counter-rotation of the head" [P].
- **Pose dependence ("action fields")** [P]:
  - The same MN moves the head toward an MN-specific pose. From a pitched-up start CvN7 pitches the head down strongly;
    from a pitched-down start it moves it weakly upward (Fig. 1h–j).
  - CvN7's convergence point is "10–15° pitched down, whereas the head can pitch downward unimpeded as far as 35°" (later
    given as 12° pitch).
  - Convergence holds in the first 80 ms and after removing trials with head saccades (yaw > 200°/s).
- Trial counts: CvN7 action field 2,442 trials from 32 flies; DProN2 3,912 trials from 21 flies; the 16 per-type
  supplementary figures use 61 trials (CvN8, 1 fly) to 3,243 trials (54 flies) [P].
  - The legends disagree with each other: Fig. 2a gives CvN7 3,912 trials from 32 flies (Fig. 1k's DProN2 count), and
    Supplementary Fig. 13 gives DProN2 1,403 trials from 23 flies. Check the data files before using a count.
- **Peak speed about each MN's mean axis (Fig. 4j)** [fig.]:
  - CvN5 ≈113°/s at ≈30 ms; CvN4 ≈100°/s, decaying slowly; CvN8 ≈78; DProN2 ≈70; DProN3 ≈65; CvN7 ≈60.
  - CvN6 and CvN A1 ≈45; CvN3 ≈40; DProN5 ≈35; CvN2 and CvN A2 ≈30; VCvN and CvN1 ≈25; DProN1 ≈20°/s.
  - The rise starts within ≈10 ms of light onset and peaks at 20–55 ms.
- **Per-axis peak mean angular velocity** (Supplementary Figs 1–16, panels g–i; unilateral, plotted as right-nerve
  neurons; °/s; positive pitch = head down) [fig., ±5°/s]. Roll and yaw signs are as plotted; see §1.6.

  | MN (muscle) | roll | pitch | yaw | | MN (muscle) | roll | pitch | yaw |
  |---|---|---|---|---|---|---|---|---|
  | CvN1 (TH1) | −5 | −18 | +20 | | CvN A1 (TH1) | +5 | −30 | +30 |
  | CvN2 (OH) | +10 | −25 | +23 | | CvN A2 (TH2) | +5 | −30 | +20 |
  | CvN3 (SC-RO) | −43 | +22 | +5 | | VCvN (OH) | +12 | −15 | +22 |
  | CvN4 (VL2) | +38 | +95 | +12 | | DProN1 (SC-CO DV1) | −18 | −7 | +8 |
  | CvN5 (VL1) | +60 | +115 | +25 | | DProN2 (SC-CO DV2) | −75 | −48 | −10 |
  | CvN6 (VL1) | +12 | +70 | +10 | | DProN3 (DE) | −88 | +32 | +12 |
  | CvN7 (VL1) | +28 | +68 | +18 | | DProN4 (LEV) | +58 | −20 | 0 |
  | CvN8 (VL1, 1 fly) | +25 | +78 | ≈0 | | DProN5 (AD) | −22 | +40 | −15 |

  - Groups: yaw = CvN1, CvN2, CvN A1, CvN A2, VCvN (TH, OH). Pitch-down = CvN4–8 (VL1–2). Roll = CvN3 and DProN1–4.
    Roll plus pitch = DProN5.
  - BANC's axis classes (§2) agree: yaw for CvN1/2, CvNA1/2 and VCvN1–3; pitch for CvN4–7; roll for CvN3 and DProN1–4;
    roll-pitch for DProN5.
- Resting head pose in tethered flight without stimulation (control flies): roll, pitch, yaw means 0, 8, −1°, with SD 8,
  12 and 4° (N = 36) [P]. Gorko's frame tilts X 40° below the body axis (flight posture).

### 1.5 Proprioception and the feedback model

- Kir2.1 in LNCs during CvN7 stimulation [P]:
  - Peak pitch velocity (at the 135 ms mean peak time) rose from 34 ± 43°/s (median ± IQR, controls) to 60 ± 66°/s (P =
    5 × 10⁻⁴, n = 43).
  - The head "overshoots the normal convergence point (12° pitch …) and converges instead towards a more pitched pose
    (19° pitch)".
  - Resting posture was unchanged (P = 0.3, 0.9, 0.2 for roll, pitch, yaw), "probably because the velocity damping
    performed by the LNCs falls outside the velocity range of normal head movements at rest".
  - Kir2.1 in MNCs (43 flies, 5,160 trials) or in the prosternal organ (SS47486; 12 flies, 1,632 trials) also changed
    CvN7's action field, "but the effect could not be captured by changing a single parameter in our model".
- **Model [M].** A linear time-invariant model:
  - The light step is band-pass filtered and pushes the head along the MN's pull axis. Head acceleration also gets
    position and velocity feedback (`ẍ = r·mx + p11·x + p14·ẋ`, etc., plus a yaw→pitch coupling term).
  - It was fit with MATLAB `greyest` on half the trials, with a per-fly gain.
  - On held-out trials, NRMSE was 0.4 for the feedback model and 0.6 for feedforward (CvN7). 71% against 45% of trials
    stayed within 5°.
  - Across all MN types the mean NMSE was 0.5 for feedback and 0.8 for feedforward.
  - The LNC data were fit best by cutting the pitch-velocity feedback parameter by 53%.
  - Fitted parameter values are not given in the paper or SI. They sit in the authors' .mat outputs (Fig. 3 file 33 MB;
    Fig. 4 file 1.6 GB; not downloaded).
- Discussion points the modeller should keep [P]:
  - Some blowfly neck MNs get visual input that "alone does not lead to action potentials but instead changes the action
    potential threshold for mechanosensory inputs" (Huston & Krapp 2009).
  - "Studies in other species have shown electrical synapses between synergistic motor neurons".
  - "Passive properties of the fly neck are likely to also contribute".

### 1.6 Sign conventions, and a mirror inconsistency (my reading)

- Gorko's frame (Extended Data Fig. 2c): X is the roll axis (pointing forward, 40° below the body axis), Y the pitch axis
  ("positive azimuth as moving from the fly's front to its left, i.e. from the X axis to the Y axis"), and Z the yaw axis,
  right-hand rule. Fig. 1h: "Positive angular velocity indicates downward head movement".
- Data are "flipped so as to appear as if they came from the equivalent neuron on the right side" (axon side). Taken
  literally, +yaw is nose-left and +roll is left side up.
- Read that way, four facts clash:
  1. The right-nerve yaw MNs (all +yaw) would turn the head away from their own nerve. Electrical stimulation of the
     blowfly ADN (CvN A1–2's homolog) turns it toward the stimulated side (Gilbert et al. 1995 [A], via Kauer 2016 [2°];
     §6).
  2. DProN4 (levator, +58) would lower its own side and DProN3 (depressor, −88) raise it. The blowfly levator lifts and
     the depressor pulls down its own side (Kauer 2016, from Strausfeld et al. 1987; §6).
  3. CvN7's roll component would add to, not oppose, the body roll that excites it.
  4. With MaleCNS wiring and BANC nerve sides, HS→VCvN would be anti-compensatory (§3.6).
- Flipping left and right in the plotted roll and yaw resolves all four. Pitch is unaffected by a left–right mirror.
- **I therefore treat roll and yaw signs in Gorko's per-MN kinematics as mirror-ambiguous.** The working reading is: yaw
  MNs turn the head toward their nerve side; +roll lifts the nerve side; VL MNs pitch the head down. That reading is
  consistent with the blowfly and with the connectome.
- Check it against the authors' raw axes (`meanAxisAllFlies` in the 1.6 GB Fig. 4 file) before using it in a
  pre-registered direction criterion.

---

## 2. Identity in the connectomes

### 2.1 Counts

- **Calliphora**: 21 MNs per side, 11 with brain somata (CN 8, VCN 3) and 10 prothoracic (ADN 2, FN 8) [2°]. Nerves,
  muscles and exceptions are in §6. Namiki et al. 2018 cite "~19 pairs of neck motor neurons (Strausfeld and Seyan,
  1985b)".
- **MANC** (Cheong et al. 2024/2026, eLife RP96084) [P]:
  - "we identified 12 pairs of likely neck MNs (compared to 10 pairs in Calliphora) by their predominant presynaptic input
    in the NTct and exit through the cervical nerve (CvN) or dorsal prothoracic nerve (DProN)". Only three "can be
    tentatively identified".
  - "fly neck MNs are split between those residing in the VNC and the brain, and so the neck MNs are not complete in the
    MANC dataset". "we also identified four neck MNs running through the neck connective".
  - MN types are named MNnm## (nm = neck muscle).
  - My inference: the three tentative identifications are the Calliphora-named types ADNM1, ADNM2 and FNM2 (MaleCNS
    `mancType`).
- **FANC**: 24 neck MNs (both sides; Azevedo et al. 2024, as summarized in
  `../Embodied fly connectome simulation/descending_vnc_motor.md`) [2°].
- **BANC v888** (Bates et al. 2026, Nature; metadata `banc_888_meta_20260521.parquet` from the project's GitHub) [D]:
  - 49 `neck_motor_neuron` cells, sub-classed yaw 14, roll 12, pitch 8, roll-pitch 2 and unassigned 13.
  - Types follow and extend Gorko: CvN1–CvN11 (CvN8 not found), CvNA1/A2, VCvN1–3 and DProN1–9. The paper lists "the
    neck motor neurons CvN1–CvN11, CvNA1/A2, VCvN1–VCvN3 and DProN1–DProN9", "perhaps for gaze control" [P].
  - BANC also has 44 neck chordotonal neurons (SNpp17, SNpp18, SNpp22, SNpp40, SNpp59; prothoracic chordotonal nerve)
    and 31 prosternal hair plate neurons (SNpp19; prosternal nerve).
  - FAFB/FlyWire types now carry the same names (BANC `fafb_cell_type`: CvN1,CvN2; CvN3–7; CvN9–11; VCvN1,VCvN2; VCvN3).
- **MaleCNS v1.0** (brainfly's tables) [D]:
  - 44 neurons with subclass `nm`: 24 `vnc_motor` (12 pairs, T1 somata) and 20 `cb_motor` (10 pairs, labial-neuromere
    somata).
  - Plus GNG647 (3 cells) and GNG314 (2), typed `cb_motor` subclass `rm` with exit nerve "ON". BANC matches them to
    VCvN1/2 and VCvN3 (ventral cervical nerve, OH muscles), so they are neck MNs mislabelled as retinal.
  - **49 neck MNs in all, ≈25 per side.**
  - The ADMN carries only wing MNs (28) and the ProAN and VProN only front-leg MNs. Every neck MN leaves through CvN, DProN
    or (for GNG647/GNG314) "ON".

### 2.2 Crosswalk (MaleCNS → model label → Gorko/BANC name, muscle, axis, sides) [D]

The model's `cell_type` is the FlyWire type where one exists, so brain neck MNs are named CB####. `HybridBrain.cells()`
also matches MaleCNS types. Nerve sides are from BANC through `malecns_match`/`manc_match`.

| MaleCNS type (n) | brainfly `cell_type` | Gorko/BANC name | Muscle | Axis | Soma | Nerve vs soma |
|---|---|---|---|---|---|---|
| GNG653 (2) | CB0706 | CvN1/CvN2 | TH1 or OH | yaw | brain | ipsi |
| GNG648 (2) | CB0913 | CvN3 | SC-RO | roll | brain | ipsi |
| CvN4 (2) | CB0899 | CvN4 | VL2 | pitch (down) | brain | ipsi |
| CvN5 (2) | CB0838 | CvN5 | VL1 | pitch (down) | brain | ipsi |
| CvN6 (2) | CB0916 | CvN6 | VL1 | pitch (down) | brain | **contra** |
| CvN7 (2) | CB0831 | CvN7 | VL1 | pitch (down) | brain | **contra** |
| GNG641 (2) | CB4212 | CvN9 | ? | ? | brain | contra |
| GNG650 (2) | CB0835 | CvN10 (BANC auto-match) | ? | ? | brain | ? |
| GNG276 (2), GNG283 (2) | CB0705 | unmatched: candidates are the other CvN1/2, CvN8, CvN11 | ? | yaw-like inputs (§3.2) | brain | ? |
| GNG647 (3; typed rm/ON) | CB0918 | VCvN1/VCvN2 | OH | yaw | brain | ipsi |
| GNG314 (2; typed rm/ON) | CB0004 | VCvN3 | OH | yaw | brain | ipsi |
| ADNM1 MN (2) | ADNM1 MN | CvNA1 | TH1 | yaw | T1 | **contra** |
| ADNM2 MN (2) | ADNM2 MN | CvNA2 | TH2 | yaw | T1 | **contra** |
| MNnm11 (2) | MNnm11 | DProN1 (by MANC id; BANC's own MaleCNS match says DProN3a/b) | SC-CO DV1 | roll | T1 | ipsi |
| MNnm13 (2) | MNnm13 | DProN2 | SC-CO DV2 | roll | T1 | ipsi |
| MNnm07,MNnm12 (4) | MNnm07,MNnm12 | DProN3a/3b (by MANC id) | DE | roll | T1 | ipsi |
| MNnm03 (2) | MNnm03 | DProN4 (Gorko SI Table 2) | LEV | roll | T1 | ipsi |
| MNnm08 (2) | MNnm08 | DProN5 (Gorko SI Table 2) | AD | roll-pitch | T1 | ipsi |
| FNM2 (2) | FNM2 | DProN6 | ? | ? | T1 | ipsi |
| MNnm14 (2) | MNnm14 | DProN7 | ? | ? | T1 | ipsi |
| MNnm09 (2) | MNnm09 | DProN8 | ? | ? | T1 | ipsi |
| MNnm10 (2) | MNnm10 | DProN9 | ? | ? | T1 | ipsi |

- Gorko SI Table 2 maps CvNA1 = MANC 20860/10407, CvNA2 = 14549/17653, DProN4 = 156960/45594 and DProN5 = 11059/11954.
  These are exactly MaleCNS ADNM1, ADNM2, MNnm03 and MNnm08 by `mancBodyid`.
- FlyWire ids are given for CvN4, CvN5 (2), CvN6 and CvN7, and FAFB skeletons for CvN6 and CvN7.
- The VNC CvNA1/A2 somata are contralateral to their nerve, as in the blowfly ADN ("arise from contralateral cell bodies";
  §6). CvN6 and CvN7 axons cross; CvN4, CvN5, VCvN and CvN1–3 do not [D, MaleCNS soma side against BANC nerve side].
- Caveats [D]:
  - MaleCNS gives MNnm07,MNnm12 L 853504 and FNM2 L 928688 the same `mancBodyid` (24975).
  - BANC's `side` column is inconsistent for some brain MNs (two "left" CvN7). I used the nerve column.
  - Croke et al. 2026 name a neck MN "CB0935", which is absent from MaleCNS and BANC v888.

### 2.3 Consequences for brainfly code [D]

- `experiments/vnc/relay.py` defines its "neck" pool as every `cb_motor` neuron. That is 107 cells: 20 neck (nm), 67
  proboscis, 13 antennal and 7 "retinal" (of which 5 are the VCvN neck MNs). The 24 VNC neck MNs fall in its "T1" pool
  with the front-leg MNs.
- A neck read-out should use the 49 bodyIds of §2.2. MaleCNS `subclass == "nm"` plus GNG647 and GNG314 gives exactly
  these.

---

## 3. Wiring of the neck MNs in MaleCNS v1.0 [D]

My queries of brainfly's `counts.npz`: MaleCNS v1.0, minconf 0.5, signed by presynaptic consensus transmitter
(GABA/Glu/His negative, as in the model). Synapse counts are summed over a type's neurons unless stated. Scripts are in
the scratchpad (`neck_work/q5–q13*.py`).

### 3.1 Input composition

- Input synapses per neck MN: median 6,559 (328–13,233). Brain MNs: median 8,002 (4,148–13,233). VNC MNs: median 5,418
  (328–8,219). The one 328-synapse MNnm07/12 is probably fragmented.
- Shares of each MN's input, median (range):
  - DNs 37% (12–62%); ANs 26% (13–51%).
  - VNC interneurons 29% (12–50%; VNC MNs). Central-brain interneurons 30% (17–43%; brain MNs).
  - Visual projection/centrifugal 0% (0–11%): CvN6 10–11%, CvN7 6%, CvN5 4%.
  - Sensory 5% (0–13%). Inhibitory-signed 46% (31–59%).
- Of 312,133 neck-MN input synapses, 116,893 (37%) come directly from DNs. This matches Cheong et al.: "Most neck MNs …
  receive >20% (up to ~60%) of their synaptic input directly from DNs".
- Neck MNs make few central outputs (median 35 synapses per cell, 1–235), mostly onto other brain neck MNs (e.g. GNG648
  → CvN7 30, CvN7 → CvN6 19) and GNG interneurons. Their transmitter is "unclear" (so excitatory in the model).

### 3.2 Direct LPTC input

- The **pitch MNs get frontal VS cells**. The table gives synapses per neuron, presynaptic side relative to MN soma.

  | MN | VS | HSS | H2 | Other |
  |---|---|---|---|---|
  | CvN7 L / R | 96 + 4 / 95 + 4 (soma side + other) | 1 / 1 | 0 / 1 | — |
  | CvN6 L / R | 105 / 109 (soma side) | 33 / 44 (opposite side) | 11 / 26 (soma side) | V1 6 |
  | CvN5 L / R | 64 / 69 (**opposite** side) | 4 / 3 | ≤1 | — |
  | CvN4 L / R | 20 / 22 (both sides) | 10 / 16 | 2 | — |

  - Against Gorko's FAFB counts (CvN6: VS1–3 127, HSS 41, H2 17; CvN7: VS1–3 123, HSS 1, H2 0), MaleCNS's VS and HSS
    counts agree within ≈20%. CvN6's H2 input agrees less well (11 and 26 against 17).
  - With BANC nerve sides (CvN6/7 cross, CvN5 does not), **every pitch MN takes its VS input from the eye contralateral to
    its nerve**, as Gorko states.
  - VS→CvN6/7 is 1.2–1.4% of each MN's input; VS→CvN5 is 0.5%.
- **Which VS cells?** MaleCNS lumps VS1–8 into one type "VS" (9 per side). I estimated each LPTC's RF centre as the
  synapse-weighted mean viewing direction of its T4/T5 inputs, propagated from column-assigned Mi/Tm neurons through
  brainfly's `eye2d.column_directions()` (Zhao et al. eye map). VS cells come out at azimuth 47–118° and elevation 18–52°.
  Ranking each side's VS cells by azimuth (synapses below are summed over both sides' cells of a rank):
  - Rank 1 (azimuth ≈47–49°, with T4b/T5b input like Drosophila VS1): CvN6 133, CvN5 67, CvN7 52, CvN4 42.
  - Rank 2 (≈49°): CvN7 90, CvN6 69, CvN5 48. Rank 3 (≈61–74°): CvN7 43, CvN5 17, CvN6 13. Rank 4 (≈76–81°): CvN7 14.
  - Rank ≥ 5 (lateral, ≥ 81°): no pitch-MN synapses.
  - **So CvN4–7 sample the frontal VS cells (≈VS1–3), as Gorko found.**
  - DNp20 (DNOVS1) takes ranks 3–9 (79–184 synapses per rank), and DNb06 and DNp17 take the lateral ranks 5–9 (DNp17
    mostly 7–9). DNp22 (DNOVS2) and DNge043 take ranks 1–4.
  - Suver et al. 2016 found DNOVS1 dye-coupled to VS4–6 and DNOVS2 to VS2–3 (§4). My RF estimate puts HSN at elevation
    +29°, HSE +10–15° and HSS −24 to −31°, a sanity check.
- **The yaw and roll MNs get the horizontal system**. Synapses per side (L / R; GNG647's right side is two cells,
  summed), soma-side HS and opposite-side H2:

  | MN | HS (soma side) | H2 (opposite side) | HST |
  |---|---|---|---|
  | GNG283 | HSE 54/69, HSN 35/39, HSS 12/7 | 77/65 | 85/52 |
  | GNG647 (VCvN1/2) | HSN 37/54, HSE 15/30, HSS 7/4 | 28/26 | 0/4 |
  | GNG276 | HSE 10/8, HSN 4/8, HSS 7/5 | 50/46 | 8/9 |
  | GNG314 (VCvN3) | HSN 10/14, HSS 6/7, HSE 0/5 | 3/0 | — |
  | GNG653 (CvN1/2) | HSN 9/11, HSE 5/7 | 13/0 | — |
  | GNG648 (CvN3) | HSS 16/22, HSE 0/3 | 12/8 | — |

  - GNG283's direct LPTC input is the largest of any neck MN: 3.4% of its input.
  - No VNC neck MN gets LPTC input (the LPTCs end in the brain).
- Pokusaeva et al. 2024 found the same partners electrically: "HSN and HSE form electrical connections with VCNM-like
  neurons …, and HSS cells form electrical synapses with CNM-like neurons" (§4).

### 3.3 Descending neurons

- **Largest DN inputs** to all neck MNs, synapses summed over all 49 MNs (consensus transmitter) [D]:

  | DN (cells) | Synapses | Main targets |
  |---|---|---|
  | DNge033 (2, GABA) | −5,026 | brain yaw MNs, ADNM1, MNnm11 |
  | DNge002 (2, ACh) | +4,867 | ADNM1/2, DProN MNs, brain yaw MNs |
  | DNa06 (2, ACh) | +4,381 | GNG283 785, GNG276 576, GNG653 558, GNG647 508, GNG648, ADNM1, MNnm11, GNG314 |
  | DNg93 (2, GABA) | −4,255 | pitch and yaw MNs |
  | DNge143 (2, GABA) | −4,112 | yaw MNs |
  | DNg76 (2, ACh) | +3,712 | CvN7 636, GNG276, GNG648, GNG283 |
  | DNge125 (2, ACh) | +3,708 | DProN MNs |
  | DNg12_a (8, ACh) | +3,639 | CvN4–7 |
  | DNge026 (2, Glu) | −3,474 | mixed |
  | DNg49 (2, GABA) | −3,337 | DProN MNs |
  | DNg81 (2) | −3,031 | yaw MNs |
  | DNg78 (2) | +2,466 | MNnm03, GNG276, GNG314 |
  | DNpe013 (2) | +2,330 | CvN4/6/7 |

  - None of these 13 types takes more than 0.5% of its own input from LPTCs: DNa06 0.5%, DNpe013 0.4%, DNge026 0.3%,
    the rest ≤ 0.1%.
- **The LPTC-recipient DNs** (Calliphora-homologous names from MaleCNS synonyms):
  - **DNp15 = DNHS1** ("Suver 2016: DNHS1"):
    - Inputs: 13.3% of its input from LPTCs. DNp15 R gets HSN R 138, HSE R 122, HSS R 23 and HST R 26, plus **H2 L 253**
      (6.3% of its input); mirror for DNp15 L.
    - Neck output 947 synapses: MNnm11 349, ADNM1 232, MNnm14 124, ADNM2 116, FNM2 99.
    - Each DNp15 reaches ADNM1/2 with soma on the other side (whose nerve is on the DN's own side) and MNnm11/14 with soma
      on its own side.
  - **DNp20 = DNOVS1** ("Dorkenwald 2024: DNOVS1"): VS (soma side) 442–494, i.e. 9–10% of its input, and VST2 290 (6%).
    Neck output only 208 chemical synapses, to MNnm10, MNnm09, MNnm08, MNnm13 and FNM2, 7–46 each. Cheong et al.: "DNp20
    has few vesicles and may be electrically coupled", with a 4.5 µm axon (Suver 2016).
  - **DNp22 = DNOVS2**: VSm 116–150 (3–4%) and VS 51–73 (1–2%). Neck output 167, to MNnm11, MNnm14 and FNM2.
  - Other LPTC-heavy DNs, LPTC share of their input and neck output:
    - DNb03: HST 628, H2 617, Nod5 461 (32%); neck 448, to ADNM1/2 and GNG283.
    - DNg41: HST/H2 (22%); neck −59.
    - DNg46 (Glu): VSm 925 (32.5%); neck −569 onto CvN5/6.
    - DNp17 (12 cells): VST2/VS/HST (18%); neck 522, to MNnm10/13.
    - DNb06: lateral VS (3%); neck 194. DNge006: H2 137 (3.6%); neck 845.
- **DNa06** is BANC's head-orienting hub ("excitatory DN with connections onto eye motor neurons as well as neck motor
  neurons that control all three axes"). In MaleCNS only 0.5% of its input is from LPTCs; 72% is central-brain (PS322,
  PS307, GNG285, PS124, PS019, DNa11). It is a candidate for targeted, non-optomotor head turns.
- BANC's head-orienting cluster: DNa06, DNb02, DNb06, DNg10, DNp15, DNp17, DNp22 and DNpe013 [P].

### 3.4 Two-hop routes

Fraction-weighted measure: W2 = Σ_X (share of X's input from source) × (share of MN input from X). Direct share is W1.

- HS → CvNA1/A2 and MNnm11: W1 = 0. W2 = 0.0009–0.0015, almost all via DNp15.
- H2 → CvNA1/A2: W2 ≈ 0.002, via DNp15 and DNb03. HS → GNG283: W1 = 0.015 (direct dominates).
- VS → CvN6/7: W1 = 0.012–0.013. The VS → OCG01f → CvN route is negative (OCG01f is glutamatergic), W2 ≈ −0.005.
- VSm/VST1/VST2/HST → PS237 (ACh; 27% of PS237's input is from these LPTCs) → CvN4/6/7: W2 = +0.0035 to +0.0064, about
  half the size of the direct VS path.
- VS → DNp20/DNp17 → MNnm10: W2 = 0.0015.
- Ocellar: OCG01b (ACh, +475) and OCG01f (Glu, −582) are among CvN6's largest inputs (≈6% together); CvN7 −449/+.
  MaleCNS lacks the ocellar ganglion ("both the lamina and the ocellar ganglion are missing"), so these neurons keep only
  their brain inputs. OCG01f's brain input is 54% OCG01b and 18% VS.

### 3.5 Mechanosensory inputs

- **Haltere campaniform afferents synapse directly on brain neck MNs.** These are sensory-ascending types entering through
  the dorsal metathoracic (haltere) nerve, DMetaN: SApp ("haltere", 148 cells), SApp08, SApp09/SApp22, SApp06/SApp15 and
  SApp01 (campaniform). All are cholinergic.
  - Per target: CvN6 1,804 (≈11% of its input), GNG647 (VCvN) 1,729, CvN5 1,575, ADNM1 1,025, GNG648 1,015, GNG653 1,001,
    CvN7 844, MNnm11 667, GNG283 611, GNG650 581.
  - Total ≈12,900 synapses onto neck MNs (≈4% of all their input).
  - Inhibitory GNG interneurons that get haltere input (GNG546, GNG327, GNG529: 8–16% of their input from haltere
    afferents) add a disynaptic negative route (−1,100 to −1,600 synapses each onto neck MNs).
  - This matches the blowfly, where "haltere interneurons, and primary afferents from the prosternal organs and halteres"
    converge on neck MNs (Strausfeld & Seyan 1985 [A]).
- Wing-base campaniform afferents (ADMN: SApp10, SApp19, SApp21, SApp04, SNpp08/11/28/37/38) add 2,069 synapses, mainly
  onto MNnm13 (DProN2), GNG647 and GNG648.
- **Prosternal hair plate** (SNpp19, prosternal nerve, 35 cells; cholinergic):
  - 888 direct synapses, mostly onto **MNnm03 = DProN4 (levator) 673 (5% of its input)**, FNM2 114 and MNnm14 74.
  - One hop via AN11B008 and AN11B012 (ascending) and IN02A007 and IN02A029 (Glu): broadly inhibitory onto DProN MNs.
- **Neck chordotonal organ** (SNpp17/18/22, prothoracic chordotonal nerve, 32 cells): **no direct synapses** onto neck
  MNs. One hop via ascending AN18B004, AN18B032, AN19B001 and AN04A001, which project onto brain neck MNs (e.g. GNG650).
  Gorko's LNC/MNC effects therefore run through interneurons.
- Johnston's organ wind/gravity afferents (JO-DP, JO-DA) make 113 synapses onto neck MNs, 100 of them onto CvN5 and
  CvN6. In the blowfly, wind on the antennae depolarizes VCNM (§6).

### 3.6 Side logic and compensatory direction

- Pitch:
  - CvN6 and CvN7 axons cross, so a right-nerve CvN7 sits on the left of the brain and takes left VS1–3.
  - Downward motion in the left fronto-lateral field comes from nose-up pitch and from body roll lifting the left side.
  - Right-nerve CvN7 pitches the head down (and, on the mirrored reading of §1.6, lowers the left side), so it
    compensates on both components.
- Yaw:
  - VCvN R (GNG647/GNG314; right soma, right nerve) gets HS R (front-to-back on the right eye) and H2 L (back-to-front on
    the left eye). Both mean the world is turning clockwise seen from above, i.e. the fly turned left.
  - Compensation means turning the head right, toward VCvN R's nerve. That fits the mirrored reading of §1.6, the blowfly
    ADN result and Calliphora VCNM (ipsilateral front-to-back depolarizes; unilateral OH contraction gives "sidewise
    deflection of the head").
  - DNp15 R (HS R + H2 L) → ADNM1/2 with left somata and right nerves is the same logic one synapse later.
- **Unresolved.** Gorko's plotted yaw signs read literally predict the opposite. A pre-registered yaw-direction criterion
  needs the raw axis file first.

### 3.7 What the chemical connectome cannot show here

- **Gap junctions** at almost every visual entry point:
  - Drosophila: HS ↔ VCNM-like and HSS ↔ CNM-like MNs, HS ↔ DNp15 (HSN strongly; preserved in shakB FlpStop flies), and
    HSE ↔ contralateral H2 (Pokusaeva et al. 2024).
  - DNOVS1 ↔ "a cluster of frontal neck motor neurons", DNOVS1 ↔ VS4–6 and DNOVS2 ↔ VS2–3 (Suver et al. 2016).
  - Calliphora: CNMN6/7 ↔ ipsilateral VS2/3 and contralateral HSS, CNMN7 ↔ CNMN6 and contralateral CNMN7 (Wertz et
    al. 2012); HSN/HSE ↔ VCNM (Haag et al. 2010); VS4–9 ↔ DNOVS1 and VS5/6 ↔ DNOVS2 (§6).
- Ocellar drive (the ocellar ganglion is missing), and flight-state and octopaminergic gating (§4, §6).
- Graded transmission: HS, VS and DNOVS1 are non-spiking or spikelet neurons.

---

## 4. Drosophila physiology of the visual pathway to the neck

Tags as above. Recording temperatures are 20–22 °C where stated; LJP = liquid junction potential.

### 4.1 HS and VS cells

- **Resting potentials** (whole-cell, LJP-corrected):
  - Suver et al. 2016, quiescent flies: VS1 −43.0, VS2 −43.2, VS3 −47.9, VS4 −48.9, VS5 −44.9, VS6 −48.0, HSN −46.3,
    HSE −53.4, HSS −47.3 mV [fig.]. Means given in the text: VS −44.7, HS −50.0 mV [P].
  - Joesch et al. 2008 (VS) and Schnell et al. 2010 (HS): "about −55 mV (corrected)" [P].
- **Membrane resistance:**
  - Rm in tethered-flight preparations: HS 150 ± 51 MΩ (n = 13), VS1–3 140 ± 83 (n = 21), VS4–6 151 ± 31 MΩ (n = 13)
    (Kim et al. 2017); HSN 147 ± 35 MΩ (n = 10) and VS1–2 122 ± 49 MΩ (n = 21) (Kim et al. 2015) [P].
  - Older dissected preps gave much lower values: VS Rin 30–40 MΩ (Joesch 2008), HS 10–20 MΩ (Schnell 2010) [P].
  - HS soma Rin 176 ± 46 → 205 ± 45 MΩ and τm 4.3 ± 1.4 → 4.9 ± 1.3 ms, from 30 s to 10 min after break-in (N = 14;
    Cuntz et al. 2013) [P].
- **Graded responses with small spikes:**
  - VS: preferred direction (PD, downward) is a graded depolarization; null direction (ND) a hyperpolarization
    "superimposed by small action potentials of irregular amplitude" (TTX-sensitive).
  - Example VS1 at λ 50°, 1 Hz: PD ≈ +10–12 mV, ND ≈ −6 mV [fig.] (Joesch 2008).
  - HSN at λ 42.5°, 1 Hz: PD ≈ +8–10 mV, ND ≈ −4–5 mV [fig.]. ND/PD ratio is −0.35 to −0.42 for HS and ≈−0.55 for VS
    [fig.] (Schnell 2010; Joesch 2008).
  - "HSN cells are non-spiking neurons" with "spikelets" (Kim et al. 2015) [P].
- **Tuning:**
  - Temporal-frequency optimum ≈1 Hz at rest for VS and HS (λ 22–45°). VS contrast half-maximum ≈24% (Joesch 2008;
    Schnell 2010) [P].
  - Walking raises HSN calcium responses at 4 Hz 2.7–16× (mean 6.5 ± 4.4, n = 8) and shifts the optimum toward 2–3 Hz;
    the gain is largest at ≈6 Hz (Chiappe et al. 2010) [P/fig.].
  - Flight "doubled" VS peak-to-peak responses (Maimon et al. 2010 [A]; measured at 1 Hz [2°]) and depolarizes baselines
    by ≈1.5–4.6 mV in example cells [fig., SI].
  - Suver et al. 2012 found the flight boost in VS greatest at 2–8 Hz, "a 20-30% increase in response as measured at the
    cell body", with the optimum staying at 1 Hz. Flight raised the baseline 3.4 ± 1.5 mV, and octopamine (100 µM)
    mimicked the boost in quiescent flies [P]. At 1 Hz this disagrees with Maimon et al.; the measures differ (first-cycle
    peak of the PD response against PD–ND peak-to-peak).
  - HS in flight (Schnell et al. 2014): rest −42.2 → −40.1 mV at flight onset [P]. Steady-state PD − ND responses,
    quiescent against flight: ≈12.0 against ≈10.1 mV at 1 Hz, ≈5.0 against ≈8.9 at 4 Hz, ≈2.1 against ≈5.6 at 7 Hz, so
    the optimum moves from 0.5–1 Hz to ≈2 Hz [fig.]. HS's impulse response in flight decays with τ = 65 ms [P].
- **Star-field yaw responses** (non-flying, 2 s mean): HS 5.6 ± 0.7 mV, VS4–6 2.5 ± 0.4, VS1–3 0.8 ± 0.4 mV. VS1–3
  "responded strongly to pitch, but also to roll, with weak responses to yaw" (Kim et al. 2017) [P].
- **Preferred rotation axes** (Suver 2016, flight, azimuth of the horizontal rotation axis) [fig.]: VS1 +120.8°, VS2
  +126.0°, VS3 +164.3°, VS4 −165.1°, VS5 −147.9°, VS6 −120.4°, HSN −24.2°, HSE −14.4°, HSS +5.1°.
- **Latency and timing:**
  - HSN visual latency 24 ms for PD and 30 ms for ND, to a 1,000°/s sweep (Kim et al. 2015) [P].
  - Optogenetic T4/T5 activation gives an LPTC excitatory peak 5.4 ± 0.4 ms after the flash (Mauss et al. 2014) [P].
- **Efference copy** during flight saccades: "saccade-related potentials" in HSN of −3.5 mV (contraversive) and +1.8 mV
  (ipsiversive), starting ≥21 ms before the wing saccade. They are strongest in HS, intermediate in VS4–6 and weak in
  VS1–3 (Kim et al. 2015, 2017) [P].
  - When walking, HS carry a congruent, not cancelling, angular-velocity signal (≈1 mV per 100°/s) and 2–6 mV
    stride-locked oscillations (Fujiwara et al. 2017 [A], 2022 [P/fig.]).
- **Electrical coupling:**
  - VS cells couple to neighbouring VS cells (neurobiotin, n = 15; Joesch 2008).
  - HS couple to HS, CH-like cells, DNp15, VCNM-like and CNM-like neck MNs, bIPS and contralateral H2 (Pokusaeva et al.
    2024).
  - In shakB FlpStop flies LPTC–LPTC coupling is lost but HS→DN/MN coupling is preserved, and HSE cells "lost
    sensitivity to the motion in the contralateral field almost entirely" [P].

### 4.2 Descending neurons with LPTC input

- **Suver et al. 2016** (J Neurosci 36:11768): whole-cell recordings in tethered flying and quiescent females at 20 °C;
  star field rotated at 22.5°/s about 13 horizontal axes 15° apart, 2 s of motion [P/fig.].

  | DN (MaleCNS) | Spiking | Dye-coupled to | VNC targets | Preferred axis (flight) | Baseline rise in flight | Tuning range (flight) |
  |---|---|---|---|---|---|---|
  | DNOVS1 (DNp20) | no ("graded"), axon 4.5 µm | VS4, VS5, VS6; likely "a cluster of frontal neck motor neurons" | dorsal prothoracic (neck) only | −139.9° (r² 0.94) | +4.7 ± 1.6 mV | ≈−46 to −39.5 mV (quiescent ≈2–3 mV) |
  | DNOVS2 (DNp22) | small spikes; 8.2 Hz/mV | VS2, VS3 | neck, wing, haltere | +144.3° (≈ roll axis of saccades) | +24.5 ± 13.9 Hz | ≈8 → 48 Hz (quiescent ≈0–5 → 22) |
  | DNHS1 (DNp15) | small spikes; 5.9 Hz/mV (3.9 quiescent) | HSN, HSE | neck and haltere (skips T2) | −7.5°; "responded more strongly to motion corresponding to pure yaw" | +13.6 ± 5.0 Hz | ≈10 → 38 Hz (quiescent ≈3 → 12) |

  - Resting potentials (LJP-corrected): DNOVS1 −46.7, DNOVS2 −40.9, DNHS1 −43.1 mV. Recorded cells: n = 8, 11 and 4 (2
    of the 4 flew) [P].
  - "a few millivolt increase was accompanied by an increase in spike rate of a few tens of Hz" [P].
  - Head yaw tuning in flight resembled DNHS1's, and head pitch was largest for downward pitch motion (Kinefly, n = 56)
    [P].
- **DNp15** (Erginkaya et al. 2025; two-photon calcium in non-behaving flies):
  - Velocity tuning is like HS. It responds most to binocular yaw and less to binocular front-to-back translation than
    HS does.
  - Discrimination index DI = (bFtoB − yaw)/(|bFtoB| + |yaw|): **DNp15 ≈ −0.65 (−0.9 to −0.35, 7 ROIs) against HS ≈ −0.1
    (−0.65 to +0.8, ≈17 ROIs)**, P < 0.001 (Fig. 1h) [fig.].
  - Responses to right front-to-back alone: HS ≈13, DNp15 ≈5 z [fig.]. DNp15 responds to left back-to-front through the
    contralateral H2.
  - Disrupting GABA-A in DNp15 raised its rotation sensitivity (P < 0.006). Unilateral DNp15 Kir2.1 or ricin made walking
    flies drift during forward runs; bilateral silencing had no effect [P].
  - MANC outputs of right DNp15: ≈33% leg neuropil, ≈30% neck MNs, ≈21% UTct [fig.]. In MaleCNS 22.8% of DNp15's 4,150
    output synapses go to neck MNs [D].
- **DNp03** (Croke et al. 2026; Buchsbaum & Schnell 2025):
  - A loom-driven collision-avoidance DN that spikes only in flight (max ≈120 Hz flying against ≈0–15 Hz quiescent)
    [fig.].
  - Unilateral activation "caused a head turn away from the activated side", ≈2.5–4° (right DNp03 ≈3.5–4°, left
    ≈2.5–3°) peaking 100–200 ms after light onset (n = 21 and 18 trials) [P/fig.].
  - It reaches neck MNs only indirectly, through DNa04, DNa05 and DNa15 to DProN4/5, "CB0935" and CvN5 [P].
  - Silencing it reduced loom-evoked head yaw only for the fastest looms (r/v 10 ms) [P].
- Other DN screens:
  - Cande et al. 2018 found head grooming but no head-orienting phenotypes (DNg07/08, DNg12).
  - Aymanns et al. 2022 found no head-orientation-encoding DNs among those imaged [P].
  - Flight gating of visually driven DNs is strong: DNp07 92 → 27 Hz without flight, and octopamine restores it (Ache et
    al. 2019) [P].

### 4.3 Neck MN recordings in Drosophila

- Only CvN7 (Gorko 2024; §1.3). There is no published EMG or calcium imaging of Drosophila neck muscles or MNs during
  visual stimulation, beyond Suver's behavioural head tracking. Searched 2026-10.

---

## 5. Drosophila head behaviour: benchmarks

All rigid-tether (body-fixed) flight unless stated. Values are [P] unless marked.

### 5.1 Yaw optomotor gain and phase against frequency

- **Cellini & Mongeau 2022** (eLife 11:e80880; Fig. 4–figure supplement 3, read by eye twice; the two readings agreed
  within 0.02 in gain and 5° in phase).
  - Conditions: 30° grating, single sinusoids with peak velocity 250°/s, 3.75°/pixel LED arena, females 3–5 d, 100 fps
    video. Body-fixed n = 9, body-free (magnetic tether) n = 10. Values [fig.]:

  | Frequency (Hz) | 0.7 | 1 | 1.5 | 2.1 | 3.5 | 5.3 | 10.6 |
  |---|---|---|---|---|---|---|---|
  | Head gain, body-fixed | 0.37 | 0.44 | 0.44 | 0.50 | 0.50 | 0.51 | 0.46 |
  | Head phase, body-fixed (°) | +40 | +30 | +15 | +2 | −12 | −30 | −95 |
  | Head gain, body-free | 0.05 | 0.07 | 0.11 | 0.15 | 0.24 | 0.28 | 0.36 |
  | Head phase, body-free (°) | +78 | +75 | +70 | +58 | +25 | 0 | −60 |
  | Body gain, body-free | 0.73 | 0.62 | 0.56 | 0.48 | 0.37 | 0.29 | 0.20 |
  | Body phase, body-free (°) | −15 | −22 | −32 | −43 | −68 | −92 | −160 |

  - Body-free heads are "inversely tuned to the body and resembled a high-pass filter". Body-fixed heads often hit
    "approximately ±15°".
  - The haltere → head path (inferred) has phase −70 to −200° (mean −119°) [P].
  - Anaesthetized (passive) heads "rarely moved more than 0.5°" [P].
- **Cellini & Mongeau 2020** (PNAS 117:23085):
  - Rigid tether, sum-of-sines 1–9.6 Hz. Head gain ≈0.47, 0.47, 0.55, 0.68, 0.71 and phase ≈+20, −5, −20, −40, −50° at
    1, 3.1, 5.3, 7.4, 9.6 Hz [fig.].
  - "Head movements followed the visual stimulus in as little as 10 ms … whereas wing steering responses lagged by more
    than 40 ms." "can reduce retinal slip speed via head movements in yaw by up to 60%." Neck yaw limit "~±15°" [P].
- **Cellini, Salem & Mongeau 2022** (PNAS 119:e2121660119), magnetic tether:
  - Head takes over gaze above a crossover at "~2.5 Hz". Head phase lead cuts effective gaze latency by 20 ms [P].
  - Fitted open-loop transfer functions from visual slip to head and body yaw [M]: G_head = e^(−0.02 s)·0.037 s/(0.063 s
    + 1) and G_body = e^(−0.02 s)·2.23/(0.155 s + 1). The head term is a 63 ms first-order plant under a derivative
    (acceleration-sensitive) controller.
- **Duistermars, Care & Frye 2012** (Front Behav Neurosci 6:6), rigid tether, N = 42 (34 in the 3.75 Hz contrast series):
  - "head turning increases with TF and saturates above 1 Hz". At TF 3.75 Hz (30° period, 112.5°/s) mean head yaw peaks
    "between 10° and 15°" at every contrast from 0.09 to 0.98.
  - Head response delays 73–120 ms against 92–220 ms for wings (time to exceed 1 SD of baseline). Head and wing
    magnitudes correlate, R² = 0.815 [P].
- **Rauscher & Fox 2024** (Proc R Soc B 291:20240311): the head tuning curve peaks at 120°/s pattern velocity (wings at
  180°/s) for a 1 Hz triangle wave of random stripes [P]. Head 1-Hz FFT magnitude ≈5.6–5.7° at 90°/s in untreated flies
  (n = 34) [fig.]. The FFT normalization may make these half-amplitudes; check before converting to gain.
- **Non-flying flies:**
  - Head responses are small: ≈3° at λ 24°, 1.2 Hz (Haikala et al. 2013) [P].
  - Mureli et al. 2017 report the opposite: "visually guided head movements occur only during flight" [A]. None of 6
    non-flying flies on a coverslip followed a 1 Hz triangle wave (from a web summary of the full text; unverified).
  - Blowflies make gaze-stabilizing head movements "only when walking or flying, not when standing still" (Hengstenberg
    1991 [2°]).
- **Range and gain from an early Drosophila study** (Hengstenberg, c. 1995 poster) [P]: head range yaw ±25°, pitch ±35°,
  roll ±120°; in flight the head is pitched down 23.0 ± 7.5° relative to rest. To a 24°-wavelength pattern moving back
  and forth at 24°/s, head movements cut the apparent pattern motion by ≈65% in flying and ≈80% in resting flies.
  *optomotor-blind^H31* and *ruby^5* mutants, which lack HS and VS cells, move their heads normally but don't turn them
  to wide-field motion.

### 5.2 Manipulations

| Manipulation | Effect on head | Source |
|---|---|---|
| HS/VS Kir2.1 (two drivers) | depolarizing visual responses ≈25% of WT, hyperpolarizing ones abolished; head optomotor "dampened by ~50%" (peak ≈3.5–4° → ≈1.8–1.9° [fig.]; initial slope 17–22 → 6–8°/s); wing response barely changed | Kim et al. 2017 [P/fig.] |
| Unilateral HS activation (ChR2-C128S, +4.4 ± 1.5 mV in HS) | head yaw toward the stimulated side: 1.35 ± 0.25° sighted (N = 44), 3.05 ± 0.4° blind norpA (N = 15) [fig.]; also flight turns toward that side | Haikala et al. 2013 |
| Haltere immobilization, ablation or asynchronous drive | head optomotor amplitude ≈halved: 5.7 → 2.8° (immobilized), 2.0° (ablated) [fig.]; tuning shape kept | Rauscher & Fox 2024; Mureli et al. 2017 [2°] |
| One haltere slowed by magnet | head yaw ≈5° toward the treated haltere (11 of 13 flies); no linear summation with vision for the head (wings sum linearly) | Rauscher & Fox 2021 |
| LNC Kir2.1 | faster CvN7-driven pitch (34 → 60°/s), convergence 12 → 19°; rest unchanged (§1.5) | Gorko 2024 |
| DNp03 unilateral activation | head yaw ≈2.5–4° away from the activated side (§4.2) | Croke et al. 2026 [P/fig.] |

### 5.3 Saccades and head–body coordination

- **Flight, rigid tether:**
  - Reset head saccades are triggered when the head reaches ±9°, ending ≈7.5° on the other side. They last ≈50 ms, and
    the wings lead the head by ≈5–10 ms (Cellini, Salem & Mongeau 2021, preprint wording) [PP].
  - Passive neck relaxation τ ≈25 ms accounts for ≈65% of saccade peak velocity [PP].
  - Head saccades followed wing saccades by ≈20 ms (Kim et al. 2015) [P].
- **Body-fixed against body-free** (Cellini & Mongeau 2022 Fig. 7D) [fig.]:
  - Head saccade amplitude ≈11° against ≈8°; duration ≈45–47 ms in both.
  - Peak velocity ≈360 against ≈300°/s; return time constant 0.91 against 0.13 s.
- **Magnetic tether, spontaneous body saccades** (Kim et al. 2017) [P/fig.]:
  - The head yaws with the body (≈4–5°; "anti-stabilizing") and rolls opposite to the expected body roll (≈8–10°),
    within 30 ms.
  - Body saccades average 33° and 77 ms during bar fixation and 64° and 101 ms when spontaneous (spontaneous medians 56°,
    83 ms, 929°/s) (Mongeau & Frye 2017) [P]. Head movement during bar tracking is only 1.1 ± 1.9° [P].
- **Walking:**
  - Head moves with the body in saccades, peak-velocity disparity ≈2 ms (Geurten et al. 2014).
  - Head counter-rotates at the body-saccade peak and follows the body by 66 ms in forward runs (Cruz et al. 2021).
  - The head's range is "<20°" and its contribution to gaze shifts "minor". Walking optomotor gain ≈0.56 (Cruz 2021)
    [P].

---

## 6. Calliphora and other flies (other species throughout)

- **Anatomy** (Strausfeld, Seyan & Milde 1987, and later summaries):
  - Strausfeld & Seyan 1985 [A]: "8 motor neurons arising in the brain (cervical nerve neurons, CN1–8) and at least 13
    motor neurons arising in the prothoracic ganglion (anterior dorsal and frontal nerve neurons, ADN1,2 and FN1-11)".
  - The standard later count is four nerves (FN, CN, ADN, VCN) with "a total of 21 pairs of NMNs" for 21 pairs of
    muscles, "in most cases each muscle receives input from only one NMN" (Huston & Krapp 2008) [P]. Per side: CN 8,
    VCN 3, ADN 2, FN 8 [2°]. The exceptions: one CN MN supplies both OH1 and OH2, and TH2 gets two MNs, ADNM2 and CNMN3
    [2°].
  - Muscles by nerve (Strausfeld et al. 1987, via Kauer 2016) [2°]:
    - CN: oblique horizontal (CNMN2), transverse horizontal (CNMN3), abductor (CNMN4), ventral longitudinal, which lower
      the head (CNMN6, CNMN7), and the sclerite retractor and rotator (CNMN1, CNMN5, CNMN8).
    - VCN: OH3–5 (VCNM1–3). ADN: TH1 (ADNM1, large axon) and TH2 (ADNM2, small).
    - FN: at least 13 somata, 8 of them large-axon MNs. FNM1 drives the sclerite levator, FNM2 the sclerite adductor,
      FNM3–4 the two segments of the sclerite depressor, FNM5–8 the sclerite-condyle muscles. One levator or depressor
      alone rolls the head; both levators pitch it up and both depressors pitch it down.
  - CN and VCN somata are in the brain, with direct LPTC input. ADN and FN somata are in the prothoracic ganglion, with
    LPTC input via DNs. The 10 prothoracic pairs (ADN 2 + FN 8) are the "10 pairs in Calliphora" that Cheong et al.
    compare with MANC's 12 (§2.1).
  - ADN MNs "arise from contralateral cell bodies" [2°]. VCN's three MNs supply OH3–5, and "unilateral contraction …
    leads to a sidewise deflection of the head (yaw response)" (Haag et al. 2010) [P].
  - About 50 pairs of DNs have terminals that visit neck MNs (Gronenberg et al. 1995 [A]).
  - Head range: yaw ±20°, pitch ±20°, roll ±90° (Haag et al. 2010) [P]. Head mass ≈8 mg (van Hateren & Schilstra 1999)
    [P].
- **Nerve stimulation** (Gilbert et al. 1995 [A], via Kauer 2016 [2°]): electrical stimulation of the ADN yaws the head
  toward the stimulated side, and of the FN rolls it down toward the stimulated side. The two ADN MNs of the right side
  are excited by clockwise yaw motion and inhibited by the opposite [A].
- **VCNM** (Haag, Wertz & Borst 2010):
  - Graded, with ipsilateral front-to-back PD. Bidirectionally electrically coupled to HSN and HSE: "HSN and HSE cells form
    the sole direct visual input". Rest ≈−60 mV; no spikes to vision alone.
  - Wind on the antennae (Johnston's organ) depolarizes it with transient spikes; wind plus motion makes it spike,
    supralinearly.
  - Haltere-beating episodes depolarize it by 20.2 ± 2.4 mV (HS by 2.3 ± 0.7 mV), centrally (persisting with halteres
    waxed), with spiking. The depolarization starts a few ms before the halteres move.
  - "During flight, the amplitude [of head yaw optomotor responses] is, on average, 30- to 40-fold larger than during rest"
    [P] (8 flying, 7 non-flying flies). A fixed fly's head moved only during haltere-beating episodes.
- **CNMN6/7** (Wertz, Haag & Borst 2012 [A/2°]):
  - Tuned to downward (pitch) rotation; coupled to ipsilateral VS2/VS3 and contralateral HSS. CNMN7 is coupled to
    CNMN6 and to the contralateral CNMN7. Dye coupling suggests only CNMN7 takes LPTC input directly, and CNMN6 takes it
    through CNMN7.
  - Head pitch responses needed both eyes. This is the blowfly counterpart of Drosophila CvN6/7. Cobalt coupling of
    VS2/3 to CNM6/7 was first shown by Milde & Strausfeld 1986 [2°].
- **DNOVS1/2** (Haag et al. 2007; Wertz et al. 2008, 2009):
  - DNOVS1 is graded and electrically coupled to VS4–9 (cross-correlation half-width 3.2 ms). Motion latency 42.4 ± 1.7
    ms against 12.9 ± 1.8 ms for ocellar input.
  - DNOVS2 spikes (up to ≈90 Hz from a 5–15 Hz rest), is coupled to VS5/6 and prefers roll.
  - Both are dye-coupled to frontal-nerve neck MNs [P]. Cobalt fills couple VS4–9 through DNOVS1 to at least FNM1–4 and
    FNM7 (Strausfeld et al. 1987 [2°]). Kauer (2016) found one DNOVS1–FN MN coupling (probably FNMN3), "the only synaptic
    connection found between a descending neuron and a neck motor neuron of the frontal nerve" in her study [P].
- **Which links are electrical:** VS→CNMN6/7, HS→VCNM and VS→DNOVS1/2→FN MNs are dye- or cobalt-coupled (above). The ADN
  MNs showed no cobalt coupling on backfill, and current injected into HSN or HSE changed the small ADN MN's rate only
  weakly, so HS reaches them through chemical DN synapses (Kauer 2016) [P]. Haltere afferents cobalt-couple to giant
  heterolateral thoracic interneurons, and long fills stain ADN and frontal-nerve MNs: a fast electrical haltere → neck
  route (Hengstenberg, Hausen & Hengstenberg 1988, poster) [P].
- **Neck MN physiology and gating:**
  - Huston & Krapp 2008: 47 wide-field neck MNs. Receptive fields match rotations and are more binocular than LPTCs
    (binocularity 0.6 against 0.32) [P].
  - Huston & Krapp 2009: "type II" neck MNs do not spike to vision alone (subthreshold median 0.5 mV). With haltere
    oscillation they fire spikes phase-locked within ≈2–4 ms, whose probability vision modulates [P].
  - Kauer et al. 2015 and Kauer 2016 (frontal-nerve MNs): levator and adductor MNs are tuned to one roll direction,
    depressor MNs to the other, and the tuning "optimally matches the pulling planes of the muscles they innervate";
    maximum responses 28–139 Hz across cells [P]. The two ADN MNs give at most 45 ± 5 Hz (small) and 78 ± 6 Hz (large;
    mean ± SEM) to yaw; the large one needs both eyes [P].
  - Every ADN and FN MN class Kauer recorded responded to strong panoramic motion alone (Huston & Krapp had used small
    gratings). She concluded that what gates spiking is "not the sensory modality of the input but its pure strength at
    the level of dendritic summation" [P].
  - Head-pitch optomotor gain switches between two internal states, up to 30-fold apart. The high-gain state comes with
    head jitter and haltere beating, but halteres aren't needed for it (Rosner et al. 2009 [A], via Haag et al. 2010).
    The gain change lies downstream of the LPTCs (Rosner et al. 2010 [A]; Rosner & Warzecha 2011 [M]).
  - Compensatory head roll is switched off at rest (Hengstenberg et al. 1986 [A]); a fly that stops flying in mid-air
    suppresses it (Hengstenberg 1993) [P].
  - Flight also changes the visual input itself. In Lucilia, H1's spontaneous rate rises from 8.4 to 75.5 Hz, and its
    temporal-frequency tuning, peaking near 2 Hz at rest, stays flat to ≈7 Hz in flight (Jung et al. 2011) [P].
- **Haltere and other latencies:**
  - Forward haltere deflection excites neck MNs after 2.5–3 ms, and their spikes follow haltere vibration one to one up
    to 200 Hz (Sandeman & Markl 1980) [A].
  - Type II FN MN spikes lock to haltere phase within 2.1 ± 1.1 ms at 105 Hz (Huston & Krapp 2009) [P].
  - Step roll of the body (90° at 2,000°/s, tethered flight): with a structured surround the head responds after ≈10 ms
    at up to 1,200°/s; on haltere signals alone (featureless surround) after ≈12 ms at ≈700°/s, fading within 5 s; on
    vision alone (pattern rolled) after ≈30 ms at ≈450°/s (Hengstenberg 1991, 1993, 1997) [P]. Haltere roll signals
    register only above ≈50°/s.
  - Visually driven head pitch has a latency of at least 22 ms (Rosner & Warzecha 2011, citing Rosner et al. 2009) [P].
- **Head kinematics:**
  - Compensatory head roll latency "down to Δt ≈ 5 ms" with gain below 1 (Hengstenberg et al. 1986 [A]).
  - Free-flight saccades: the head lags the thorax ≈10 ms, then moves faster, at 684 ± 92°/s relative to the thorax, and
    finishes first (van Hateren & Schilstra 1999) [P].
  - On a trackball, fast head yaw turns (>100°/s) "rarely last longer than 50 ms" (Longden et al. 2022) [P].
- **Prosternal organs** (Preuss & Hengstenberg 1992 [A]): ≈110 hairs per field. They sense pitch and roll, barely yaw.
  Unilateral manipulation biases head roll.
- **Transfer to Drosophila:**
  - Likely to transfer: the brain/VNC split of MNs, VS→pitch MNs, HS→yaw MNs (VCN), DNOVS1/2 → frontal-nerve MNs, and
    haltere-afferent convergence. All have Drosophila connectome or physiology counterparts (§2–§4).
  - Unlikely to be visible in a chemical connectome: the electrical VS–DNOVS, HS–VCNM and CNMN–CNMN links, and the flight
    and haltere gating.

---

## 7. What a first probe could test, and what to pre-register

### 7.1 Why start with the brain-resident pitch and yaw MNs

- About half of the neck MNs (25 of 49) have their somata and dendrites in the brain (labial neuromere of the GNG).
- Of those, CvN4–7, VCvN (GNG647/GNG314), GNG283/GNG276, CvN1/2 (GNG653) and CvN3 (GNG648) take **direct** LPTC
  synapses (§3.2). The pitch MNs' inputs reproduce Gorko's FAFB counts.
- A probe on them needs only the eye → flyvis → LPTC → brain MN chain that rung 3 and the optomotor experiment already
  exercise. It does not depend on the nerve-cord relay, which `experiments/vnc/relay.py` found transmits nothing.
- The VNC MNs (CvNA1/A2, DProN1–9) are reached through DNp15, DNp20, DNp22, DNp17, DNa06 and others. They are a second
  stage, gated by rung 5.

### 7.2 Probe A: frontal vertical motion → VS1–3 → CvN4–7 (pitch)

- **Stimulus**, through `FlyvisNative` and `eye2d`:
  - Wide-field rotation of a random-dot or grating pattern about 12 horizontal axes, 30° apart, as in Gorko Fig. 1e.
  - Plus local up/down motion patches at the predicted RF: the eye contralateral to each CvN7's nerve (its soma side),
    azimuth 30–90°, elevation 0–60°.
  - Speed near the LPTC optimum at rest (TF ≈ 1 Hz; §4).
- **Read-out:** CvN4–7 rates per neuron (model labels CB0899, CB0838, CB0916, CB0831), VS by RF rank, DNp20 and DNp22.
- **Pass/fail benchmarks from flies:**
  1. Direction: CvN7 fires more to downward than to upward local motion in its RF (Gorko Fig. 1c), with t ≥ 4 over model
     flies. Use rate differences, because flies' CvN7 is near threshold at rest.
  2. Axis: CvN7's best body-rotation axis lies within ±45° of the measured 60–90° azimuth toward its nerve side, elevation
     ≈ 9° (Gorko Fig. 1e and the authors' data; §1.3).
     - Measured modulation: +1.42 mV at the best axis, −1.76 mV at the opposite axes, i.e. a full cosine-like curve over
       the 12 axes. Score the shape with a fitted cosine and its phase, not the amplitude.
  3. Field: CvN4–7 respond to frontal (≈VS1–3 field) but not lateral vertical motion. DNp20 (DNOVS1) prefers lateral
     vertical motion and DNp22 (DNOVS2) frontal (Suver 2016 axes; my RF ranks, §3.2).
     - Suver's measured preferred axes: DNOVS1 −139.9°, DNOVS2 +144.3° (their convention; §4). These are a second-order
       check.
- **Nulls:**
  - Brainfly's degree-preserving rewiring should abolish the axis tuning.
  - Deleting only the VS → CvN4–7 synapses should cut CvN7's modulation by roughly the direct share. My W1 against W2
    predicts direct ≈ 2× the PS237 route, with the OCG01f route opposing.
  - An identity swap (give VS cells HS cells' output rows) should rotate the preferred axis toward yaw.

### 7.3 Probe B: horizontal rotation → HS/H2 → VCvN, GNG283/GNG276, CvN1/2 and DNp15 (yaw)

- **Stimulus:** `experiments/optomotor.py`'s drum (30° period, 40°/s, 1.33 Hz), clockwise against counterclockwise. Add
  binocular front-to-back ("translation") and monocular front-to-back and back-to-front conditions, as in Erginkaya et al.
  2025 Fig. 1g.
- **Read-out:** GNG647 and GNG314 (VCvN; CB0918, CB0004), GNG283, GNG276 (CB0705), GNG653 (CB0706), DNp15 (L/R) and HS.
- **Benchmarks:**
  1. Sign: the right VCvN (HS R + H2 L) fires more for clockwise than counterclockwise drums, and the left the reverse.
     Blowfly VCNM depolarizes to ipsilateral front-to-back motion (Haag et al. 2010, other species). Drosophila HS–VCNM
     coupling is shown by dye coupling only (Pokusaeva 2024).
  2. Rotation over translation: DNp15 responds more to yaw than to binocular front-to-back translation, while HS responds
     to both (Erginkaya et al. 2025, Fig. 1g,h; calcium, non-behaving flies). This is a network-level test, because the
     difference needs the contralateral H2 and the GABAergic middle layer.
  3. DNp15's preferred axis lies between ipsilateral roll-down and yaw (Suver 2016: azimuth −7.5°, and DNHS1 "responded
     more strongly to motion corresponding to pure yaw").
- **Do not pre-register the direction of the head turn yet** (§1.6, §3.6).
- **Nulls:** degree-preserving rewiring; a side swap (mirror H2's targets); removing H2 → DNp15 synapses, which should
  remove the rotation-over-translation advantage.

### 7.4 Probe C (multisensory gating; optional)

- Flies' benchmarks:
  - Blowfly: "type II" neck MNs spike to vision only while the halteres oscillate (Huston & Krapp 2009), VCNM
    depolarizes ≈20 mV during haltere beating, and head yaw optomotor amplitude is 30–40× larger in flight (Haag et al.
    2010); details in §6.
  - In Drosophila, haltere manipulations roughly halve head optomotor amplitude (Rauscher & Fox 2024; Mureli et al. 2017;
    §5.2).
- In the model:
  - Drive the haltere campaniform afferents (SApp, SApp08, SApp09/22, SApp06/15, SApp01; ≈300 cells) at a wingbeat-like
    rate.
  - Ask whether the visual modulation of brain neck MNs (Probe A/B) grows.
  - The connectome predicts mixed signs: direct excitation of CvN5/6/7, VCvN and ADNM1, plus GNG546/327/529 inhibition.

### 7.5 Later, with a head

- Gorko's feedback model (§1.5) or the Mongeau lab's fitted head transfer function G_head (§5.1).
- Fly benchmarks are head yaw gain against frequency (§5.1). The rigid-tether gain is 0.37–0.51 across 0.7–10.6 Hz
  (single sines at 250°/s).
- Wire MN populations to pull axes with the per-MN table of §1.4, after resolving its roll/yaw mirror.

---

## 8. What this means for brainfly (my reading)

1. **The neck is the cleanest place in rung 8 to test a visuomotor transformation without the nerve cord.**
   - Half the neck MNs are brain neurons with direct LPTC input.
   - The connectome reproduces the one Drosophila wiring measurement (Gorko's CvN6/CvN7 counts) and the DNOVS1/DNOVS2
     VS pattern (Suver).
   - A pass on Probe A or B would show that the model routes optic flow to the right effectors with the right axis.
2. **What the fly data can and can't anchor.**
   - Only one Drosophila neck MN (CvN7) has visual recordings: one cell's tuning curve, plus RF maps.
   - DNHS1, DNOVS1 and DNOVS2 have axes, resting potentials and Hz/mV slopes. DNp15 has calcium tuning for rotation
     against translation. HS and VS cells are well characterized.
   - Pre-register **signs, axes and selectivity ratios**, not mV or Hz. Brainfly's HS and VS cells spike, while flies'
     are graded.
3. **The largest structural gap is electrical.**
   - Every first-order visual link to the neck that has been tested has a gap-junction component (§3.7). In Drosophila:
     HS–VCNM-like, HSS–CNM-like, HS–DNp15, DNOVS1–"frontal neck motor neurons", VS–DNOVS1/2. In the blowfly: VS–DNOVS1/2,
     HS–VCNM, VS–CNMN6/7, CNMN6–CNMN7. One stage further on, the blowfly's ADN MNs showed no dye coupling and get HS
     signals through chemical DN synapses (§6).
   - The chemical connectome gives the same partners, and for DNp20 almost nothing (208 synapses).
   - `HybridBrain.set_coupling` can impose these as a sensitivity arm. Coupling strengths are unmeasured in Drosophila,
     so any value is a free parameter and must be stated before the run.
4. **State gating is missing.**
   - Flies' neck-motor visual responses are small at rest and large in flight: in the blowfly, VCNM, type II neck MNs and
     the 30–40× head optomotor gain; in Drosophila, the ≈2–3× DN amplification in flight (§4.2, §6).
   - Brainfly has no flight state or octopaminergic gain. A quiescent-fly benchmark (Gorko's CvN7, non-flying, 22 °C) is
     the fair target for now.
5. **The ocellar input to CvN6/CvN7 is truncated.** OCG01b/f carry ≈6% of CvN6's input but have no ocellar drive in
   MaleCNS. Leave them undriven and say so.
6. **Bookkeeping fixes before any neck run:**
   - Use the 49-neuron neck set of §2.2, not `cb_motor`.
   - Tag GNG647 and GNG314 as neck MNs.
   - Record soma side and nerve side separately (CvN6, CvN7, CvN9, CvNA1 and CvNA2 cross).
7. **For a later rung with a head:**
   - Gorko's result that one MN drives the head toward a pose means a torque-per-MN body model will be wrong away from
     the centre.
   - A pose-plus-velocity feedback plant (his model; LNC loss = −53% pitch-velocity feedback) is the published
     alternative. Its parameters must be refit or extracted from the authors' files.

---

**Note (2026-10-12, review 14).** Corrections to this note:
- Suver et al. 2016's DN rates were misread from Fig. 3G (summary item 7, §4.2's table). Read against the axis ticks
  (Fig. 3F agrees):
  - DNHS1 (DNp15): flight about 10 to 36.5 Hz, null to preferred axis; at rest about 0.5-1 to 14 Hz (Fig. 3E prints a
    quiescent example at 0.52 Hz).
  - DNOVS2 (DNp22): flight about 27 to 53 Hz, rest about 3 to 28 Hz.
  - DNOVS1 (DNp20): flight -41.5 to -38.9 mV (about 2.6 mV), rest -46.7 to -43.2 mV (about 3.5 mV). The earlier "6-7 mV
    in flight, 2-3 at rest" paired the rest null with the flight peak.
  So flight-to-rest modulation depth is about 0.75 times for DNOVS1, 1-1.4 times for DNOVS2 and 2 times for DNHS1. What
  flight raises is the baseline: "DNOVS1: 4.7 ± 1.6 mV; DNOVS2: 24.5 ± 13.9 Hz; and DNHS1: 13.6 ± 5.0 Hz".
- Item 12's and §8's "DN responses are ≈2-3× larger in flight (Suver et al. 2016)" is unsupported, as above.
- §3.2's table: GNG653 R gets 2 synapses from H2 L, not 0.
- §3.3: DNp22's VS input is 54 (L) and 77 (R) synapses. 51 and 73 count only connections of 5 or more.
- Item 11 and §3.2's "every pitch MN takes its VS input from the eye contralateral to its nerve" doesn't hold for CvN4.
  CvN4 R takes 18 of its 22 VS synapses from its own side, its nerve side; CvN4 L takes 13 of 20 from the other side.
- "VS → CvN6/7 is 1.2-1.4%" is the pair. CvN7 alone is 1.16-1.23%.
- Item 8 and §5.1: Duistermars et al.'s "73-120 ms against 92-220 ms for the wings" is for high-contrast temporal
  frequencies above 0.19 Hz. At 3.75 Hz across contrast they give head 80-93 ms and wings 172-316 ms.
- Smaller:
  - Item 7's Erginkaya discrimination-index range tops out at about -0.2 in their Fig. 1h.
  - Item 9's haltere immobilization was unilateral.
  - Item 10's 34 to 60 deg/s is at the 135 ms mean peak time.
  - Item 13 drops Suver et al.'s "likely" ("what are likely a cluster of frontal neck motor neurons").
  - Kim et al. 2017's error bars are SEM.

## Sources

Neck MNs and connectomes:
- Gorko B et al. (2024) Nature 628:596–603, "Motor neurons generate pose-targeted movements via proprioceptive sculpting".
  - https://doi.org/10.1038/s41586-024-07222-5
  - Full text: https://faculty.washington.edu/tuthill/docs/gorko%202024.pdf
  - Supplementary Information (Supplementary Tables 1–2 and Figs 1–17, Supplementary Methods): https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07222-5/MediaObjects/41586_2024_7222_MOESM1_ESM.pdf
  - Peer Review File: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07222-5/MediaObjects/41586_2024_7222_MOESM3_ESM.pdf
  - Code and data (CvN7 tuning `figure_1/1e/20130806RotAxisTcurveData.mat`, RF map `figure_1/1d/…172847.mat`, `plotDynamics.m`, `rotQ2levelHead.m`): https://bitbucket.org/stephenhuston/code_data_gorko_et_al
  - Commentary: Petrovic-Erfurth & Jordanova (2024) Signal Transduct Target Ther 9:220, https://pmc.ncbi.nlm.nih.gov/articles/PMC11362485/
- Bates AS et al. (2026) Nature, "Distributed control circuits across a brain-and-cord connectome" (BANC).
  - https://doi.org/10.1038/s41586-026-10735-w
  - Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13518251/
  - Metadata: https://github.com/htem/BANC-project (`data/meta/banc_888_meta_20260521.parquet`)
- Cheong HSJ et al. (2026) eLife 13:RP96084, MANC premotor circuits.
  - https://elifesciences.org/articles/96084
  - Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13384506/
- Azevedo A et al. (2024) Nature (FANC), via `descending_vnc_motor.md`: https://pmc.ncbi.nlm.nih.gov/articles/PMC11348827/
- Namiki S et al. (2018) eLife 7:e34272: https://pmc.ncbi.nlm.nih.gov/articles/PMC6019073/
- Berg S et al. (2025/2026) MaleCNS connectome. bioRxiv https://doi.org/10.1101/2025.10.09.680999; Cell 189:5504 (2026). Tables used through brainfly's `~/fly-data` (minconf 0.5).
- Zhao A et al. (2025) Nature, "Eye structure shapes neuron function in Drosophila motion vision".
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC12488493/
  - Eye map used by brainfly `eye2d`: https://github.com/reiserlab/eyemap_T4
- Erginkaya M et al. (2025) Nat Neurosci 28:1241–1255, "A competitive disinhibitory network for robust optic flow processing in Drosophila".
  - https://doi.org/10.1038/s41593-025-01948-9
  - Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC12148931/
  - Fig. 1: https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41593-025-01948-9/MediaObjects/41593_2025_1948_Fig1_HTML.png
- Pokusaeva VO, Satapathy R, Symonova O, Jösch M (2024) Nat Commun 15:8830.
  - https://doi.org/10.1038/s41467-024-53173-w
  - Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC11470938/
- Croke et al. (2026) Curr Biol, "Drosophila DNp03 descending neurons serve as a hub within a flight saccade network".
  - https://doi.org/10.1016/j.cub.2025.11.035
  - Full text (author manuscript): https://pmc.ncbi.nlm.nih.gov/articles/PMC12977095/

Drosophila physiology:
- Suver MP, Huda A, Iwasaki N, Safarik S, Dickinson MH (2016) J Neurosci 36:11768: https://pmc.ncbi.nlm.nih.gov/articles/PMC5125229/
- Joesch M, Plett J, Borst A, Reiff DF (2008) Curr Biol 18:368: https://doi.org/10.1016/j.cub.2008.02.022 (read as the manuscript in Joesch's PhD thesis, LMU 2010, pp 72–89: https://edoc.ub.uni-muenchen.de/12049/1/Joesch-Krotki_Maximilian.pdf)
- Schnell B, Joesch M, Forstner F, Raghu SV, Otsuna H, Ito K, Borst A, Reiff DF (2010) J Neurophysiol 103:1646: https://doi.org/10.1152/jn.00950.2009 (read in the same thesis, pp 117–140)
- Kim AJ, Fitzgerald JK, Maimon G (2015) Nat Neurosci 18:1247: https://pmc.ncbi.nlm.nih.gov/articles/PMC6327952/
- Kim AJ, Fenk LM, Lyu C, Maimon G (2017) Cell 168:280: https://pmc.ncbi.nlm.nih.gov/articles/PMC6320683/
- Chiappe ME, Seelig JD, Reiser MB, Jayaraman V (2010) Curr Biol 20:1470: https://pmc.ncbi.nlm.nih.gov/articles/PMC4435946/
- Maimon G, Straw AD, Dickinson MH (2010) Nat Neurosci 13:393 (abstract; supplement read): https://authors.library.caltech.edu/records/swbcc-mt576
- Suver MP, Mamiya A, Dickinson MH (2012) Curr Biol 22:2294, read as chapter 2 of Suver's PhD thesis (Caltech 2013): https://thesis.caltech.edu/7923/1/suver_marie_2013_thesis.pdf
- Schnell B, Weir PT, Roth E, Fairhall AL, Dickinson MH (2014) PNAS 111:5700: https://authors.library.caltech.edu/records/52pkv-z5n16
- Cuntz H, Forstner F, Schnell B, Ammer G, Raghu SV, Borst A (2013) PLoS ONE 8:e71540: https://pmc.ncbi.nlm.nih.gov/articles/PMC3747245/
- Mauss AS, Meier M, Serbe E, Borst A (2014) J Neurosci 34:2254: https://pmc.ncbi.nlm.nih.gov/articles/PMC6608528/
- Fujiwara T, Cruz TL, Bohnslav JP, Chiappe ME (2017) Nat Neurosci 20:72 (abstract only).
- Fujiwara T, Brotas M, Chiappe ME (2022) Neuron 110:2124: https://pmc.ncbi.nlm.nih.gov/articles/PMC9275417/
- Buchsbaum & Schnell (2025) Curr Biol, "Activity of a descending neuron associated with visually elicited flight saccades in Drosophila": https://doi.org/10.1016/j.cub.2024.12.001 (preprint read: https://doi.org/10.1101/2024.08.22.608914)
- Ache JM, Namiki S, Lee A, Branson K, Card GM (2019) Nat Neurosci 22:1132: https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/
- Cande J et al. (2018) eLife (DN activation screen): https://pmc.ncbi.nlm.nih.gov/articles/PMC6031430/
- Aymanns F, Chen C-L, Ramdya P (2022) eLife (DN population imaging): https://pmc.ncbi.nlm.nih.gov/articles/PMC9605690/

Drosophila behaviour:
- Cellini B, Mongeau J-M (2020) PNAS 117:23085: https://pmc.ncbi.nlm.nih.gov/articles/PMC7502703/
- Cellini B, Mongeau J-M (2022) eLife 11:e80880: https://elifesciences.org/articles/80880 (PMC9651946)
- Cellini B, Salem W, Mongeau J-M (2022) PNAS 119:e2121660119: https://pmc.ncbi.nlm.nih.gov/articles/PMC9172134/
- Cellini B, Salem W, Mongeau J-M (2021) Curr Biol 31:4009: https://doi.org/10.1016/j.cub.2021.06.080 (not accessible; preprint v1 read: https://www.biorxiv.org/content/10.1101/2020.12.16.422884v1.full-text)
- Duistermars BJ, Care RA, Frye MA (2012) Front Behav Neurosci 6:6: https://pmc.ncbi.nlm.nih.gov/articles/PMC3284692/
- Rauscher MJ, Fox JL (2021) Proc R Soc B 288:20202374: https://pmc.ncbi.nlm.nih.gov/articles/PMC7893272/
- Rauscher MJ, Fox JL (2024) Proc R Soc B 291:20240311: https://pmc.ncbi.nlm.nih.gov/articles/PMC11338569/
- Mureli S, Thanigaivelan I, Schaffer ML, Fox JL (2017) J Exp Biol 220:2218 (abstract and short quotes; not in PMC): https://journals.biologists.com/jeb/article/doi/10.1242/jeb.146282/262447/
- Haikala V, Joesch M, Borst A, Mauss AS (2013) J Neurosci 33:13927: https://pmc.ncbi.nlm.nih.gov/articles/PMC6618655/
- Mongeau J-M, Frye MA (2017) Curr Biol 27:2901: https://pmc.ncbi.nlm.nih.gov/articles/PMC5634948/
- Geurten BRH, Jähde P, Corthals K, Göpfert MC (2014) Front Behav Neurosci 8:365: https://pmc.ncbi.nlm.nih.gov/articles/PMC4205811/
- Cruz TL, Pérez SM, Chiappe ME (2021) Curr Biol 31:4596: https://pmc.ncbi.nlm.nih.gov/articles/PMC8556163/
- Hengstenberg R (c. 1995) poster on Drosophila head movements, Proc 4th Int Congr Neuroethology p 255 (MPG.PuRe item_1794527).

Blowfly and other flies:
- Strausfeld NJ, Seyan HS (1985) Cell Tissue Res 240:601: https://doi.org/10.1007/BF00216350
- Strausfeld NJ, Seyan HS, Milde JJ (1987) J Comp Physiol A 160:205: https://doi.org/10.1007/BF00609727
- Milde JJ, Strausfeld NJ (1986) Naturwissenschaften 73:151 (via Kauer 2016): https://doi.org/10.1007/BF00367404
- Gronenberg W, Milde JJ, Strausfeld NJ (1995) J Comp Neurol 361:267: https://doi.org/10.1002/cne.903610206
- Gilbert C, Gronenberg W, Strausfeld NJ (1995) J Comp Neurol 361:285: https://doi.org/10.1002/cne.903610207
- Haag J, Wertz A, Borst A (2007) J Neurosci 27:1992 (DNOVS1): https://pmc.ncbi.nlm.nih.gov/articles/PMC6673546/
- Wertz A, Borst A, Haag J (2008) J Neurosci 28:3131 (DNOVS2): https://pmc.ncbi.nlm.nih.gov/articles/PMC6670693/
- Wertz A, Gaub B, Plett J, Haag J, Borst A (2009) J Neurosci 29:14993: https://pmc.ncbi.nlm.nih.gov/articles/PMC6665999/
- Haag J, Wertz A, Borst A (2010) PNAS 107:20104 (VCNM): https://pmc.ncbi.nlm.nih.gov/articles/PMC2993391/
- Wertz A, Haag J, Borst A (2012) J Comp Physiol A 198:655 (CNMN6/7; abstract and Kauer 2016): https://doi.org/10.1007/s00359-012-0737-y
- Huston SJ, Krapp HG (2008) PLoS Biol 6:e173: https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0060173 (PMC2475543)
- Huston SJ, Krapp HG (2009) J Neurosci 29:13097: https://pmc.ncbi.nlm.nih.gov/articles/PMC6665201/
- Kauer I, Borst A, Haag J (2015) J Comp Physiol A 201:411, "Complementary motion tuning in frontal nerve motor neurons of the blowfly" (read through Kauer 2016): https://doi.org/10.1007/s00359-015-0980-0
- Kauer I (2016) PhD thesis, LMU, "Characterization of prothoracic neck motor neurons in the blowfly Calliphora vicina": https://edoc.ub.uni-muenchen.de/20234/7/Kauer_Isabella.pdf
- Hengstenberg R, Sandeman DC, Hengstenberg B (1986) Proc R Soc Lond B 227:455 (abstract): https://doi.org/10.1098/rspb.1986.0034
- Hengstenberg R (1991) Zool Jb Physiol 95:297: https://pure.mpg.de/rest/items/item_1794710/component/file_3220332/content
- Hengstenberg R (1993) "Multisensory control in insect oculomotor systems", in Miles FA, Wallman J (eds) Visual Motion and its Role in the Stabilization of Gaze, pp 285–298: https://pure.mpg.de/rest/items/item_1794633/component/file_3219428/content
- Hengstenberg R (1997) "The organization of gaze control in the blowfly Calliphora erythrocephala", in Taddei-Ferretti C (ed) Biocybernetics of Vision: https://pure.mpg.de/rest/items/item_1794077/component/file_3214078/content
- Hengstenberg R, Hausen K, Hengstenberg B (1988) poster, Göttingen Neurobiology Conference, "Cobalt pathways from haltere mechanoreceptors to inter- and motoneurons controlling head posture and flight steering in the blowfly Calliphora" (MPG.PuRe).
- Sandeman DC, Markl H (1980) J Exp Biol 85:43 (abstract): https://journals.biologists.com/jeb/article/85/1/43/22810
- Preuss T, Hengstenberg R (1992) J Comp Physiol A 171:483 (abstract): https://doi.org/10.1007/BF00194581
- van Hateren JH, Schilstra C (1999) J Exp Biol 202:1491: https://pure.rug.nl/ws/files/38798845/1999JExpBiolvHateren.pdf
- Longden KD, Schützenberger A, Hardcastle BJ, Krapp HG (2022) Sci Rep 12:11540: https://www.nature.com/articles/s41598-022-15740-3 (PMC9262929)
- Rosner R, Egelhaaf M, Grewe J, Warzecha A-K (2009) J Exp Biol 212:1170 (abstract): https://pubmed.ncbi.nlm.nih.gov/19329750/
- Rosner R, Egelhaaf M, Warzecha A-K (2010) J Exp Biol 213:331 (abstract): https://pubmed.ncbi.nlm.nih.gov/20038668/
- Rosner R, Warzecha A-K (2011) PLoS ONE 6:e26886: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0026886
- Jung SN, Borst A, Haag J (2011) J Neurosci 31:9231 (Lucilia): https://pmc.ncbi.nlm.nih.gov/articles/PMC6623490/

Internal:
- `brainfly/shiu.py` (`mcns_types`), `brainfly/eye2d.py` (`column_directions`), `brainfly/hybrid.py` (`HybridBrain.cells`, `HybridBrain.set_coupling`) and `brainfly/optic.py` (`FlyvisNative`).
- `experiments/vnc/relay.py` (its "neck" pool) and `experiments/optomotor.py`.
- `README.md` (rung 8 row; optomotor results).
- `../Embodied fly connectome simulation/descending_vnc_motor.md` and `muscles_biomechanics_body_models.md`.
- Connectome queries `q1`–`q13` and their outputs, in the session scratchpad (`neck_work/`), not the repo.
