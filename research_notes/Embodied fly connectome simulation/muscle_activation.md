# Muscle activation: relaxing fast yet summing strongly

Question: which activation model, with parameters from measurements where possible, lets FlyMimic's tibia flexor
relax like a fly's (half the force gone 12-16 ms after the peak) and still sum to flies' 28-30 uN plateau? A first-order
activation can't (experiments/leg_deactivation_check.py). The fly numbers are in `leg_twitch_data.md` and are not
repeated here.

Tags: "(fig., approx.)" means read off a figure; "(derived)" means my arithmetic, on closed-form expressions only (no
simulation); "Not reported" means searched for and absent. Checked 2026-10-10.

## Summary (most decision-relevant first)

1. **Use two states per motor unit, outside MuJoCo.** This is the Ding/Wilson form (§4.3):
   - a calcium-like active state c that each spike raises by 1 and that decays with τc;
   - a steep, switch-like link x = c^m/(c^m + k^m);
   - force with dF/dt = A·x − F/(τ1 + τ2·x).

   With a near-switch link (m ≥ 4), the starting set below comes within about 10% of all four fly targets at once
   (derived; idealised, no leg mechanics, §4.5). The set is τc 8 ms, k 0.3, τ1 10 ms, τ1 + τ2 28 ms, and a ceiling
   A(τ1 + τ2) of 29 uN for the fast unit. It gives:
   - one spike: 0.29 of the ceiling (8.4 uN; flies 9 uN), peaking 9.6 ms after force onset and relaxing with τ 10 ms;
   - two spikes 12 ms apart: 1.66× (1.50× at 15 ms; flies 1.4-1.6);
   - 80 Hz: 2.9×; 100 Hz and up: 3.4×, a fused tetanus at the ceiling (flies 3.1-3.3).

   Measured: the ceiling, the twitch size and time course, part of the delay, and the steepness of the link (in the
   jump muscle). Fitted: τc, k, τ1, τ2. The parameter table is in "What this means for brainfly".
2. **The mechanism is measured in fast insect and vertebrate muscle.** Each spike gives a brief, nearly saturating
   active state. Force develops more slowly than that state lasts, and relaxes as soon as it ends.
   - Locust flight muscle: the degree of activation "reached 80° [sic] of the tetanic value during a single twitch",
     reached "approximately the tetanic value" in the second twitch of a pair, and decayed with τ "about 14 ms"
     ([MJ91]).
   - Mouse fast fibres: after one action potential troponin's regulatory sites are "rapidly and nearly completely
     occupied with Ca2+" (0.95 in fast fibres; [BH12]). So a twitch is limited by how fast force develops, not by
     calcium (my reading).
   - Barnacle: the calcium transient "resembles the first derivative of the rising phase of the isometric tension"
     ([AR70]).
   - In a tetanus the free-calcium peaks don't grow: they "reached approximately the same amplitude that resulted from a
     single shock" ([HZB96]). So summation comes from prolonging the active state, not from more calcium per spike.
3. **If brainfly keeps MuJoCo's activation, it should swap the time constants.** Drive ctrl with the calcium switch
   (a ~10 ms pulse per spike that merges at high rates) instead of 0.1 ms pulses. Then set activation slower than
   deactivation:
   - effective τ_act ≈ 28 ms and τ_deact ≈ 10 ms;
   - nominal values about 43-53 ms and 5-7 ms at a twitch's activation (derived from MuJoCo's formula);
   - the reverse of OpenSim's 10/40 ms.

   MuJoCo's own form (Millard 2013) makes the smallest twitches relax slowest, at 2 × τ_deact as activation → 0 ([mjm];
   derived). That largely explains why the stated 40 ms gives a 58 ms half-decay. Muscle does the opposite: its
   relaxation slows with force or rate ([BS98], [BL00], [Ah06]).
4. **The 80 Hz rate in rung 7's plateau test is not in the paper.** The bursts were evoked by Chrimson flashes and
   plotted as peak force against spike number. Burst rates: Not reported; the only interval visible is ≈12 ms, in a
   two-spike example.
   - Linear summation of a fly-shaped twitch gives 2.0-2.1× at 80 Hz and 3.0-3.1× at 120 Hz (derived, §4.2). So the
     10 ms deactivation run (2.04× at 80 Hz) sums like a fly's twitch would at that rate.
   - In the proposed model the plateau is the unit's ceiling at any rate above ≈85-95 Hz, so the rate matters less.
   - Brainfly should still read the real rates from Azevedo's Dryad data before calling the 80 Hz test a failure.
5. **The plateau belongs to one motor unit and should be a per-unit ceiling.** Spikes came from the fast MN alone, which
   is "the only motor neuron that innervates the large tibia flexor muscle fibers in the middle of the femur" ([e]).
   - So 28-30 uN is one unit's maximum, ≈0.3 of the ~100 uN muscle (derived).
   - The authors attribute the saturation to fatigue, which they did not test. Equally possible:
     - a fused tetanus: stick-insect muscle reaches 80% of its 80 Hz plateau only after ≈14 spikes, without fatigue
       ([Gu07]; derived);
     - synaptic depression: at the jump-muscle junction "depression occurred almost immediately" (abstract, [IK]);
     - mechanics: 28-30 uN rotates the tibia 17-18° against the probe (derived).
6. **Two spikes sum at or slightly below linear.** Linear superposition of a fly-shaped twitch gives 1.67-1.69× at
   12 ms and 1.53-1.57× at 15 ms (derived); flies give 1.4-1.6×. A facilitation term (Ding's R0 > 1) is not needed.
7. **Per-spike calcium in fly muscle is Not reported.**
   - Azevedo et al. imaged muscle with GCaMP6f, whose kinetics "are slow relative to fly tibia movements" ([e]).
   - GCaMP6f decays with t½ = 288 ms at 20 °C ([He16]).
   - The authors' records list an unpublished experiment, "Muscle imaging Following MN Stimulation", at 100 Hz with
     the fast-MN line ([c4]).
   - Priors from other muscles: locust flight muscle active-state decay τ ≈14 ms at 25 °C ([MJ91]); mouse fast-fibre
     free-calcium half-width 2.0 ms at 28 °C ([HZB96]).
   - Drosophila leg and jump muscles are SR-rich (≈35-45% vs ≈10% ER volume in flight muscle; [Ka22], fig., approx.).
     The adult thorax's tubular muscles carry a parvalbumin-like sarcoplasmic calcium-binding protein ([Ke97]); leg
     muscles are tubular, so probably they do too (inference).
8. **The link is steep in fly leg-type muscle.**
   - Drosophila jump-muscle skinned fibres have a Hill coefficient of 10.2-12.4 at pCa50 5.6 ([El10], [Lo22]). Flight
     muscle is 1-3; intact frog fibres are 3.2-3.9.
   - A steep link makes force fall faster than calcium: 90%→10% in 4.39τ/n, against 2.2τ for a linear link (derived).
   - It would make doublets strongly supralinear unless one spike already saturates it, which is the regime in point 2.
9. **Among insects, the fly flexor's combination sits at the strong end but within range.**
   - Fast-relaxing insect muscles sum only moderately:
     - blowfly b1: the mean tension at 150 Hz is 2.1× the twitch, unfused ([TD94]; derived);
     - cockroach extensors 178/179: half-relaxation 12-13 ms after the peak ([Ah06]; derived).
   - Strongly summing ones relax slowly: stick-insect twitch/tetanus is 0.05 ([Gu07]), larval Drosophila 0.026-0.033
     ([Or22]).
   - Relaxation slows after bursts: in cockroach 178/179 half-relaxation goes from 12-13 to 15-19 ms after three
     pulses at 100 Hz ([Ah06]; derived). Ding's τ2 term reproduces this; Millard's form does the reverse.
10. **Flies' times are measured from the somatic spike.**
    - Conduction to the EMG takes ≈0.6-1.0 ms ([f4] Fig 4G, fig., approx.).
    - Neuromuscular plus excitation-contraction latency is Not reported for the fly leg. In the blowfly b1 the delay
      from stimulus to force onset is "2.1±0.3 ms" ([TD94]).
    - So add ≈2.5 ms. With it, the 10 ms deactivation run would read 7.5 ms half-rise and 16.1 ms peak (derived; flies
      7.7-9.7 and 17-23).

## 1. Calcium transients in insect muscle

### 1.1 Drosophila
- **Adult leg (Azevedo 2020).** Widefield GCaMP6f imaging of the femur "at 50–60 Hz" identified motor units, but not
  per-spike kinetics ([e]):
  - "The kinetics of GCaMP6f are slow relative to fly tibia movements, so we examined only periods when the derivative
    of the fluorescence signal was positive".
  - "The time constant of the calcium indicator was slower than the fly's movements, such that fluorescence built up over
    subsequent contractions. Thus, pixel intensity (ΔF/F) was not directly related to contraction of the muscle."
  - Size of the signal: superficial flexor fibres "could increase more than six-fold during flexion events".
  - The authors also speculate that the low-force distal flexor (muscle 41) differs from the high-force muscle 40,
    "including larger calcium concentrations during contractions" (response to review).
  - Per-spike rise, decay and summation: Not reported.
- **Unpublished lead.** The authors' analysis records list "Record - Muscle imaging Following MN Stimulation", with "60
  trials without the bar at 100 Hz calcium imaging", for two 81A07 (fast MN) flies and one 35C09 (slow) fly ([c4]).
- **Other adult leg imaging.** Wang-Chen et al. 2026 imaged the long-tendon muscles at 33 Hz with jGCaMP8m. They note
  its "half-decay time (134 ms, or ~4.4 frames at 33 Hz...)" ([WC26]). Per-spike resolution is not possible at that rate.
- **Larval body wall.**
  - Desai & Lnenicka 2011 injected rhod-2 and Oregon Green BAPTA-1 and found "discrete postsynaptic Ca(2+) transients
    along the NMJ during single action potentials (APs)" that "remained localized to the postsynaptic membrane" in trains
    (abstract only; [DL11]).
  - No global per-spike transient with a fast indicator was found (Not reported).
  - SERCA sets relaxation:
    - "Disruption of SERCA function affected both the force and kinetics of contraction, with significant increases in
      both rise- and decay-tau values" ([Or22]);
    - SERCA mutants show "prolonged neural activity-driven muscle contraction" ([Sa05]).
  - Coupling: "Ca2+ influx via Dmca1D might initiate CICR that leads to Ca2+ transients during EC coupling" ([Hs20]).
- **Indirect flight muscle** (asynchronous, low SR; cameleon): "Ca2+ levels increase in proportion to muscle firing
  rate". Power rose and fell with time constants of "0.442 and 1.79 s" ([GD06]). This is a slow, integrating muscle and
  the wrong model for the leg.
- **Steering muscles** (GCaMP6f; Lindsay et al. 2017): kinetics not characterised in the accessible parts (abstract and
  supplement only; [Li17]).
- **Ultrastructure.** "All three leg regions had higher SR content than the flight muscles". ER volume fractions:
  flight ≈10%, jump muscle (TDT) ≈37%, leg fibre types ≈35-45% ([Ka22], Fig 1v, fig., approx.). These are confocal
  KDEL-RFP estimates of coxa muscles.
- **Buffer.** A sarcoplasmic calcium-binding protein (Dcabp-A.1/Scp1) "is present in the tubular but not the fibrillar
  muscles of the adult thorax. This expression pattern is consistent with this being a true SCP" ([Ke97], abstract).
  SCP "has been proposed to fulfill a similar function in muscle relaxation as vertebrate parvalbumin" ([Wh11]). Its
  concentration and kinetics in fly leg muscle: Not reported. Parvalbumin itself: Not reported in insects.

### 1.2 Other insects and arthropods
- **Honeybee leg (tibia) fibres** fire all-or-none action potentials, blocked by Cd2+ and La3+ but not TTX ([Co07]).
  - "A single AP leads to rapid and transient cytoplasmic Ca(2+) increase ... which afterwards returns toward baseline
    following an exponential time course. Trains of APs elicit a staircase increase of Ca(2+), as a result of multiple
    Ca(2+) transient summation." (abstract, [Co09])
  - Time constants: Not reported in the abstract.
  - Release units are slower than frog's: spark FDHM 25.5 vs 5.7 ms, rise 10.5 vs 3.5 ms (Fluo-8, 22-23 °C; [Co21]).
- **Locust flight muscle, degree of activation (DA),** read from force-velocity at 25 °C ([MJ91], abstract):
  - "DA rose to a maximum in 2–3 ms after the end of the latent period."
  - "DA reached 80° [sic] of the tetanic value during a single twitch; during the second twitch of a pair, the peak DA
    reached approximately the tetanic value."
  - "After a brief plateau, DA declined approximately exponentially. The time constant of DA decay was about 14 ms."
  - This is the closest insect measurement of the active state rung 7 needs.
- **SR content tracks twitch speed.**
  - Katydid fast units: "rise time equal 7.3 msec, half duration equals 14.3 msec, 25 C", with 20-24% SR; slow fibres
    have "only 10%" ([St75]).
  - Cicada tymbal muscle: "the sarcoplasmic reticulum is extraordinarily well developed" and "A twitch duration of under
    6ms was observed at 30°C" ([JY85]).
- **Barnacle (crustacean), aequorin** ([AR70]):
  - decay "time constant of 50-80 msec at 11-12 degrees C";
  - "The shape of the calcium transient resembles the first derivative of the rising phase of the isometric tension
    response, thus suggesting that calcium controls the rate of tension development";
  - "There is no detectable increase of the light emission above resting values, during the falling phase of isometric
    tension".

### 1.3 Fast vertebrate muscle, for calibration (true free calcium, furaptra)
- Mouse EDL: the twitch peak is "17.8 +/- 0.4 microM" and "the half-width of delta [Ca2+] was 4.6 +/- 0.3 ms" at 16 °C,
  and "2.0 +/- 0.1 ms" at 28 °C. "During a brief high-frequency tetanus, individual peaks of delta [Ca2+] were also well
  resolved and reached approximately the same amplitude that resulted from a single shock" ([HZB96]).
- Release per action potential falls in a train: at 67 Hz "Ca(2+) release decreases progressively from 0.25 to 0.15
  times that elicited by the first AP". The decay slows through "a reduction in available Ca(2+) binding sites on
  troponin and parvalbumin" ([BH07]).
- Parvalbumin speeds twitch relaxation and saturates in tetani:
  - knockout fibres decay more slowly, and "the force generated during a single twitch was approximately 40% greater"
    ([PV99]);
  - "Relaxation slowing as tetanus duration increases, reflects the progressive saturation of parvalbumin by Ca2+"
    ([PV00]).
  - This is a vertebrate route to fast twitch relaxation with intact tetanic summation. Fly leg muscle has an SCP, not
    parvalbumin (§1.1).

### 1.4 Indicator limits (read imaged decays as upper bounds)
- GCaMP6f: "t1/2 at 20 °C of 288 ms of GCaMP6f was reduced to 63 ms at 37 °C" ([He16]). Spikes are resolvable only
  "if they were separated by an interval on the order of the rise time of the sensor or more (... 50-75 ms, GCaMP6f)"
  ([Ch13]).
- jGCaMP8: "half-rise times of 2 ms" in vitro, but in Drosophila L2 neurons the half-decay was "192 ± 26 ms
  (jGCaMP8f), 137 ± 21 ms (jGCaMP8m)" ([Zh23]).
- So any GCaMP muscle trace at room temperature says nothing about calcium decays faster than ≈0.1-0.3 s. Low-affinity
  synthetic dyes (furaptra) are the standard for millisecond transients.

### 1.5 Arithmetic: linear calcium summation alone can't give flies' summation (derived)
An instantly rising exponential, summed linearly, with two spikes 12 ms apart and 80 Hz trains:

| τ_Ca | Two spikes | 80 Hz peak, × one spike |
|---|---|---|
| 10 ms | 1.30 | 1.40 |
| 15 ms | 1.45 | 1.77 |
| 20 ms | 1.55 | 2.15 |
| 30 ms | 1.67 | 2.93 |

- The two-spike ratio of 1.4-1.6 would need τ ≈13-23 ms, which gives only 1.6-2.4× at 80 Hz (flies 3.1-3.3×).
- So the extra summation has to arise downstream of free calcium, from a saturating link and force developing more
  slowly than the active state lasts.

## 2. Force-calcium relation, and where tetanic summation comes from

### 2.1 pCa-force curves in insects (skinned fibres)

| Muscle | Hill coefficient | pCa50 | Conditions | Source |
|---|---|---|---|---|
| Drosophila jump muscle (TDT) | "10.2 ± 2.1" | "5.62 ± 0.01" | 15 °C | [El10] |
| Drosophila jump muscle | "12.4 ± 1.4" (n = 13) | "5.6 ± 0.1" | 15 °C, SL 3.6 um | [Lo22] Table 1 |
| Drosophila flight muscle | 1.2-2.6 | 6.0-6.3 | 15 °C | [WZS11], [Lo22] |
| Lethocerus flight muscle | 1.0-2.2 | 5.6-5.65 | various | [Ag04], [Li04], [Lo22] |
| Crab fast fibres (crustacean) | 5.27 ± 0.76 | 6.03 | | [Pa00] |
| Frog, intact fibres | 3.2-3.9 | Ca50 1.5-1.7 uM | | [KW98] |

- Eldred 2010: "TDT expressing Tr-WT displayed a very steep tension-pCa curve" ([El10]). Swapping in the embryonic
  myosin alone lowered the coefficient to "6.3 ± 0.9" ([El10] Table 2). So part of the steepness depends on the myosin
  isoform (my reading).
- Loya 2022: "Hill coefficient values were greatest in Drosophila jump muscle, suggesting a high degree of cooperativity
  and fast calcium activation" ([Lo22]).
- Leg muscle and larval body-wall muscle: Not reported (searched). Ca50 for the jump muscle ≈2.5 uM (derived from pCa
  5.6).
- These are steady-state values in skinned fibres at 15 °C. The effective dynamic steepness in an intact twitch is
  Not reported.

### 2.2 Troponin isoforms
- Five Drosophila troponin C genes. TpnC41C is "expressed exclusively in the tubular muscles of the adult head and
  thorax, and is the predominant TpnC expressed in that tissue" ([Ch15]); "TpnC41C was a specific TpnC isoform of TDT
  muscles" ([Ch17]).
- Larval isoforms: "DmTpnC47D and DmTpnC73F, show a high embryonic/larval expression" ([He04], abstract).
- Leg muscles specifically: Not reported. Inference: they are tubular, so TpnC41C is likely.
- Calcium sites: "TnC1 (TnC-F2 in Lethocerus IFM) has two calcium binding sites, while an unusual isoform, TnC4 (TnC-F1
  in Lethocerus IFM), has only one binding site" ([El14]). TnC1 is TpnC41C.
  - "Lethocerus has another TnC isoform in leg muscle which also has two Ca(2+)-binding sites. Ca(2+) binds more
    strongly to domain IV than to domain II in two-site isoforms." ([Qi03], abstract)
  - So there is one N-terminal regulatory site, as in cardiac TnC, and the steepness doesn't come from extra sites
    (my reading).
- Calcium affinity of TpnC41C: Not reported.

### 2.3 Why tetanus exceeds twitch
- **Vertebrate fast fibres: the twitch is time-limited, not calcium-limited.**
  - One action potential occupies troponin's regulatory sites almost completely: "peak fCaTrop is similar in slow-twitch
    and fast-twitch fibers: 0.79 and 0.95, respectively".
  - "the troponin regulatory sites are rapidly and nearly completely occupied with Ca2+ in both fiber types while the
    rate of tension development is much slower in slow-twitch than in fast-twitch fibers" ([BH12]).
  - Tetanic calcium peaks match a twitch's ([HZB96]).
  - So force falls short of tetanus in a twitch because occupancy is brief compared with cross-bridge force development
    and series stretch (my reading).
- **Cross-bridges stay incomplete in a twitch:** "S-twitch/S-tetanus = 0.82" at 6 °C, and "During relaxation, force fell
  more rapidly than stiffness" ([SW84]).
- **Force integrates calcium** (barnacle; [AR70]): calcium transient area against peak force is "linear", and calcium is
  back at rest while force is still falling.
- **Insects: a near-saturating active state per spike.** In locust flight muscle a twitch reaches ≈80% of tetanic DA
  and a doublet ≈100% ([MJ91]). Locust leg muscle also shows "force potentiation (i.e., the supra-linear increase of
  peak force with increasing stimulation frequency)" ([H19]).
- **A steep link speeds relaxation (derived).** For calcium decaying with τ through x^n/(1 + x^n), force falls from 90%
  to 10% in (2·ln 9/n)·τ = 4.39τ/n, against 2.2τ for a linear link.
  - With n = 10 and τ = 40 ms that is ≈18 ms, against 88 ms.
  - But if the twitch put calcium in the steep part of the curve, a second spike would push force to near maximum.
    Example: twitch at 0.3 of maximum, 74% residual calcium at 12 ms → a doublet ratio ≈3.3, against flies' 1.4-1.6.
  - So a steep link fits only if one spike already saturates it. Force is then limited by its own kinetics, as in
    point 2 of the summary.

### 2.4 Insect excitation-contraction coupling
- Many insect fibres are graded: responses "graded in amplitude depending upon the strength of the stimuli and do not
  exceed about 30 mv. in height" (grasshopper; [Ce59]).
- Honeybee leg fibres are the opposite case: "in contrast to many other insect species, action potentials... are not
  graded but actual all-or-none responses" ([Co07]).
- Drosophila larval contractions grade with external calcium: "The amplitude of contractions induced from a single
  stimulus increased in a proportional manner with increases in external Ca2+" ([Or22]).
- Adult Drosophila leg-muscle fibre electrophysiology (junction potentials, calcium spikes, the tibia flexor junction):
  Not reported. A 2026 manuscript: "In the future, electrophysiological recordings from adult NMJs… will be essential";
  it also shows that leg muscles differ in glutamate-receptor subunits ([Su26]).
- **Lead for the plateau:** at the jump-muscle junction, "The TTM was observed to respond up to 100 Hz, but depression
  occurred almost immediately" (SICB abstract, year not shown; [IK]).

### 2.5 Series compliance, and why the probe twitch is not isometric
- Drosophila tendon or apodeme stiffness: Not reported.
- Stick insect extensor: series element "FSE=k3⋅LSE²", stiffness "8 to 14.2 N/mm2" without the outlier ([Bl12]). That is
  ≈7% of fibre length at maximum force (derived, across ranges).
- Shortening deactivation in the jump muscle: "a 30% tension decrease due to SD could be important for muscle function"
  ([Lo22]).
- In Azevedo's set-up the probe and the leg's passive stiffness sit in series. 9 uN moves the probe 40 um (5.5°), and
  28-30 uN moves it 125-134 um (17-18°) (derived, k = 0.2234 uN/um, arm 417 um).

## 3. Twitch and tetanus kinetics

### 3.1 Drosophila
- **Larval body wall** (whole larva, nerve stimulation, 22 °C, HL3 with 1.5 mM Ca2+; [Or22]):
  - "A single action potential was sufficient to induce a contraction that was between 2.6 and 3.3% of the 150 Hz
    contraction force".
  - "Force generation saturated at/above 100 Hz stimulation and 200 ms stimulus duration."
  - Decay τ "approximate 200 ms" after trains. Native bursts at "27.2 and 22.4 Hz".
  - Fatigue: "only a 29.2 ± 9.6% reduction in force" after 1 h.
  - Single-twitch time to peak: Not reported.
- **Larva (Paterson et al. 2010):** "force increases with stimulus rate monotonically and saturates between 20 Hz and
  30 Hz" ([Pt10]).
- **Adult:** besides Azevedo 2020 and Zumstein 2004 (both in leg_twitch_data.md), no twitch or tetanus recordings of
  leg, jump or steering muscle were found (Not reported). Skinned-fibre work (Peckham 1990, Swank 2012) has no intact
  twitches.
- **Jump-muscle myofibrils (17 °C)** ([Fe26]):
  - "an activation rate of 8.2 ± 4.0 s-1";
  - "an initial slow, linear phase lasting 75.6 ± 21.1 ms, followed by a fast exponential decay with a rate constant of
    19.7 ± 9.6 s−1";
  - "the myosin kinetics are a key determinant of how fast" activation proceeds.
  - Fully activated myofibrils are far slower than the leg's twitch (half-max ≈8.5 ms), so they bound but don't set the
    in vivo force-development time (my reading).

### 3.2 Other insects
- **Blowfly b1 steering muscle** (one large axon, Calliphora, ≈23 °C; [TD94], full text):
  - "delay between stimulation of the motor axon and the onset of force generation was 2.1±0.3 ms"
  - "Rise time, measured from onset to peak force, was 7.0±1.5 ms. The time from onset to 50 % relaxation was 18.9±7.1
    ms"
  - "Stimulation at 150 Hz did not result in complete tetanus. The mean tension in the b1 during stimulation at 150 Hz
    was 29±10 mN", against a 13.9 mN twitch: 2.1× (derived). (The Methods define the relaxation interval from the peak
    instead, which would make it 18.9 ms after the peak.)
- **Cockroach leg extensors 178/179** (one fast MN, 25 °C; [Ah06], Table 1):
  - twitch peak at 30.4 and 26.5 ms, 50% relaxation at 42.7 and 39.5 ms from stimulation, i.e. 12-13 ms after the peak;
  - after three pulses at 100 Hz (the natural burst), the peak is at 46.8 ms and half-relaxation 15-19 ms after it
    (derived).
- **Stick insect extensor tibiae** (FETi, SETi and CI1 together, 20-22 °C; [Gu07]):
  - peak at "26.41±6.30 ms" and 50% relaxation at "60.69±15.65 ms" after force onset;
  - twitch 5.74 mN against 114 mN at 200 Hz, a ratio of 0.050 (derived);
  - "At 80 Hz and higher stimulation frequencies, tetanus was complete in all preparations".
  - In one animal, 50% and 80% of the 80 Hz plateau took 85 and 173 ms, ≈7 and ≈14 spikes (derived).
  - Relaxation slows with use: "Increasing either frequency or duration of the stimulation extends maximal force
    production and prolongs the relaxation time" (Guschlbauer's thesis abstract, [GuT]).
- **Locust extensor tibiae** ([H19]):
  - FETi twitch peak "on average 61 ms (SD: 6 ms)", SETi 67 ms; "At stimulus frequencies above 20 Hz, single twitches
    fused into a smooth tetanic contraction";
  - "Maximum potentiation was achieved when a spike occurred approximately 15 ms before peak twitch force generated by
    the preceding spike".
  - FETi natural bursts: "12 to 17 spikes at up to 70 s-1".
- **Locust tergosternal flight muscle, 30 °C:** "The average twitch rise time (30 degrees C) was 15 ms, the twitch
  duration (to 50% relaxation) was 26 ms" ([JS91]). A fly-like twitch.

### 3.3 Comparison

| Preparation | Temp | Time to peak | Half-relaxation | Twitch/tetanus | Fusion | Source |
|---|---|---|---|---|---|---|
| Fly tibia flexor, fast unit | room | 17-23 ms (from soma) | 12-16 ms after peak | ≈0.30-0.32 if plateau = tetanus (derived) | rate unknown | [e] |
| Blowfly b1 (one MN) | ≈23 °C | 9.1 ms (derived) | 21.0 ms from stimulus | 150 Hz mean 2.1× twitch | not at 150 Hz | [TD94] |
| Cockroach 178/179 (one MN) | 25 °C | 26.5-30.4 ms | 12-13 ms after peak | Not reported | Not reported | [Ah06] |
| Locust tergosternal | 30 °C | 15 ms (rise) | 26 ms from onset | Not reported | — | [JS91] |
| Stick insect ext. tibiae (whole nerve) | 20-22 °C | ≈35 ms from stimulus | ≈34 ms after peak | 0.050 | complete ≥80 Hz | [Gu07] |
| Locust ext. tibiae FETi | Not reported | 61 ms | up to 1 s (SETi) | Not reported | >20 Hz | [H19] |
| Drosophila larva (whole body wall) | 22 °C | Not reported | τ ≈200 ms after trains | 0.026-0.033 | saturates ≥100 Hz | [Or22] |

### 3.4 Saturation or fatigue within 10-20 spikes?
- Frequency saturation is normal in insect leg muscle: stick insect at 80, 100 and 200 Hz gives 0.93, 0.97 and 1.00 of
  the 200 Hz force ([Gu07]; derived). Reaching 80% of the 80 Hz plateau takes ≈14 spikes.
- A plateau by ~10 spikes needs no fatigue.
- Within-burst fatigue of a fast insect unit over 10-20 spikes: Not reported. Larval body-wall muscle is very
  fatigue-resistant ([Or22]).

## 4. Models that relax fast and still sum strongly

### 4.1 Why a first-order activation fails here
- MuJoCo's muscle activation: "∂act/∂t = (ctrl − act)/τ(ctrl, act)", with τ = "τ_act · (0.5 + 1.5·act)" when ctrl >
  act and "τ_deact / (0.5 + 1.5·act)" otherwise. This follows "Millard et al. (2013)", "with defaults (0.01, 0.04)"
  ([mjm]).
- The deactivation constant is longest at low activation (derived): 2 × τ_deact as act → 0, 1.54× at 0.1, 1.05× at 0.3,
  0.5× at 1.
- A brainfly spike (a 0.1 ms pulse at τ_act = 10 ms) raises act by about 0.02 (derived: 0.1/(10 × 0.5)). So a twitch
  relaxes with ≈1.9 × τ_deact:
  - about 75 ms for the stated 40 ms;
  - a half-life of ≈52 ms before the leg's lag, against 58 ms measured (derived).
- Muscle goes the other way (§4.3), so one τ_deact must trade relaxation against summation.
- Harischandra et al. 2019 compared five models on one locust data set ([H19]):
  - "Linear first-order models can approximate isometric force time courses well at high spike rates, but they cannot
    account for appropriate force time courses at low spike rates. A linear third-order model performs better, but only
    non-linear models can account for frequency-dependent change of decay time and force potentiation at intermediate
    stimulus frequencies."
  - "Linear models show no frequency-dependence of decay time".

### 4.2 Linear summation of a fly-shaped twitch (derived)
The twitch is a 4 ms delay then a gamma shape of order 2 with τ 7 ms. Its half-rise is 9.3 ms, peak 18.0 ms and
half-decay 15.1 ms after the peak (flies 7.7-9.7, 17-23 and 12-16). The second figure in each cell is a 3 ms delay with
order 3 and τ 5.5 ms (10.7, 19.5 and 13.9 ms).

| Input | Peak, × one twitch |
|---|---|
| Two spikes 8 / 10 / 12 / 15 / 20 ms apart | 1.85 / 1.78 / 1.69 / 1.57 / 1.38 (1.84 / 1.76 / 1.67 / 1.53 / 1.33) |
| 17 spikes at 80 Hz | 2.14 (2.01); 90% of it by spike 3 |
| 100 Hz | 2.64 (2.48); by spike 4 |
| 120 Hz | 3.14 (2.96); by spike 4-5 |
| 150 Hz | 3.90 (3.69); by spike 5-6 |
| 200 Hz | 5.19 (4.91); by spike 7 |

- Flies' 3.1-3.3× is linear summation at ≈120 Hz or faster. But linear summation saturates within 3-5 spikes, against
  flies' "~10 spikes".
- The 10 ms deactivation run's 16.9 over 8.3 uN (2.04×) at 80 Hz is what a fly-shaped twitch gives at 80 Hz.

### 4.3 Published models with fast twitch relaxation and strong summation
All of them put summation in a calcium-like state and a saturating nonlinearity, and set force relaxation separately.
In several, relaxation slows as force rises.

- **Ding-Wexler-Binder-Macleod** (human quadriceps, rat; [W97], [D00]; definitions and values from [FL05]):
  - Equations: a calcium-troponin state CN driven by each pulse and decaying with τc; force dF/dt = A·CN/(Km + CN) −
    F/(τ1 + τ2·CN/(Km + CN)); a pulse factor Ri = 1 + (R0 − 1)·exp(−(ti − ti−1)/τc).
  - "The first two equations represent the calcium dynamics and the third equation represents force dynamics" ([W97]).
  - [FL05] Table 1 defines:
    - τ1: "Force decay time constant when CN is absent, i.e. 'in absence of strongly bound cross-bridges'";
    - τ2: "Force decay time constant when CN is present; 'extra friction due to bound cross-bridges'";
    - km: "'Sensitivity of strongly bound cross-bridges to CN'";
    - R0: "Magnitude of force enhancement due to closely-spaced pulses".
  - Human values: A 3-5 N/ms, τ1 42-51 ms, τ2 up to 124 ms, τc 20 ms ("preset"), km 0.1-0.3, R0 1.14-2 ("preset").
  - After a twitch CN falls, so force relaxes with τ1. In a tetanus it integrates with τ1 + τ2 and settles at
    A·x(τ1 + τ2·x) (derived from the equation).
- **Bobet & Stein 1998** (cat soleus and plantaris; [BS98]):
  - "The model consists of two linear, first-order systems separated by a static nonlinearity. The rate constant of the
    second first-order system varies with force level."
  - "The model shows that a force-dependent rate constant is essential for model validity".
  - Written out: x = q^n/(q^n + k^n), with "a variable time constant parameter (5), which generally decreases (becomes
    slower) with increasing force" ([FL05]).
  - Cat values ([FL05], Table 2): n 3.2-4.0, k 0.78-1.0, q decay rate 9.4-40 s⁻¹.
- **Wilson non-linear model** (locust hind-leg extensor; a simplified Ding model; [H19] Eqs 7-10):
  - Equations: "dCN/dt + CN/τc = u(t)", "x = CN^m/(CN^m + k^m)", "dF/dt + F/(τ1 + τ2·x) = A·x", with u a train of unit
    impulses, so CN steps by 1 per spike.
  - "The variable x(t) is an intermediate stage in the model and represents a non-linear saturation. The parameters m and
    k define the shape of this non-linearity. A measure of [Ca2+]i is represented by the variable CN."
  - Refits to FETi data, three locusts ([H19] Table 2): τc 72 / 93 / 83 ms; τ1 13 / 67 / 69 ms; τ2 80 / 40 / 19 ms;
    k 0.77 / 1.05 / 1.08; m 3.05 / 2.16 / 3.37.
  - Wilson 2013's published FETi means: τc 70 ms, τ1 83 ms, τ2 100 ms, k 0.57, m 1.8.
  - SETi refits gave τ2 of −27, −210 and +103 ms, so its sign is not general. The gains A depend on normalisation.
  - "For stimulation of the fast motoneuron (FETi), the non-linear Wilson model achieves better fits, particularly with
    regard to frequency-dependent force potentiation." "No experimental data are available for frequency dependence of
    FETi decay." ([H19])
  - As a fly prior this is poor. Locust FETi twitches are 3× slower. Scaled by 0.33 (derived) they give τc ≈24-31 ms,
    and with k ≈0.8 and m ≈3 two spikes 12 ms apart give 2.7× the active-state integral of one spike (derived, §4.4),
    far above flies' doublet.
- **Hatze-Zakotnik** (locust): Hatze's two second-order stages, with the twitch modulated by spike frequency. It
  "performs best for the slow motoneuron", but "Frequency-dependent modulation of a single twitch works less well for the
  fast motoneuron" ([H19]).
- **Hatze 1977** (as written in [RG]): "γ̇ = m·(σ − γ)" for normalised calcium, then q = (q0 + (ργ)^ν)/(1 + (ργ)^ν),
  with ν "2 or 3" and m "range: 3.67…11.25 1/s".
- **Virtual Muscle** (Cheng, Brown & Loeb 2000; cat; CellML encoding [CBL]): two cascaded first-order filters, with a
  fall time constant (T_f3 + T_f4·Af)/L, so relaxation slows as activation Af rises. Brown & Loeb 2000: "the isometric
  fall time relationship showed a single minimum at short lengths + low stimulus frequencies" ([BL00]).
- **Zahalak & Ma 1990:** a cross-bridge distribution-moment model whose excitation-contraction coupling "requires the
  introduction of only one more state variable--the free calcium concentration" ([ZM90]).
- **Baylor & Hollingworth** (mouse; mechanistic): release, binding to ATP, troponin, parvalbumin and the SR pump, and
  pump transport ([BH07]). Release per action potential has "a peak of 200-225 microM/ms and a FDHM of approximately 1.6
  ms (16 degrees C)". A reference if brainfly ever wants mechanism instead of the Ding form.
- **Other insect models:**
  - Stick-insect extensor time constants "are always extremely slow (200-700 ms)" ([Ho07]); the Blümel first-order filter
    ([H19]).
  - Wilson 2011: "When the interpulse frequency (IPF) was low and the number of pulses in the train small, a second-order
    model provided a good fit", but at "higher IPFs with a large number of pulses the assumptions that the response was
    linear could not be confirmed" ([Wi11]).

### 4.4 Closed-form handles on the Wilson/Ding model (derived)
- Active-state integral for one spike (CN = e^(−t/τc) after a unit step): ∫x dt = (τc/m)·ln(1 + k^(−m)). Peak x =
  1/(1 + k^m).
- The single-spike x(t) depends only on k^m and τc/m. τc and m separately set how much residual calcium the next spike
  adds to, so the twitch alone cannot pin them; the doublet and the train can.
- Fusion with a switch-like link: the trough CN = e^(−T/τc)/(1 − e^(−T/τc)) stays above k while T ≤ τc·ln(1 + 1/k).
  For τc 8 ms and k 0.3 that is 11.7 ms, ≈85 Hz.
- Tetanus: x → 1, F → A(τ1 + τ2). Twitch/tetanus ≤ ∫x dt/(τ1 + τ2).
- With a switch-like link, one spike holds x = 1 for t_on = τc·ln(1/k). The twitch is then
  1 − e^(−t_on/(τ1 + τ2)) of the ceiling and peaks at t_on. For a twitch at 0.3 of the ceiling, τ1 + τ2 ≈ 2.8·t_on.
- A gentle link fits flies' doublet but sums too little, or peaks too late. Example: m = 1, k = 0.25 (one spike gives
  x 0.8, as in [MJ91]), τc 14 ms.
  - Two spikes 12 ms apart give 1.57× the integral of one.
  - Mean x at 80 / 120 / 150 Hz is only 0.81 / 0.87 / 0.89.
  - Making the twitch 0.3 of maximum then needs τ1 + τ2 ≈70 ms, which delays the twitch peak to roughly 25 ms after
    onset (rough estimate).

### 4.5 Idealised outcomes of the proposed set (derived)
Switch-like link; force relaxes toward 1 with τ_on = τ1 + τ2 while x = 1 and toward 0 with τ_off = τ1 while x = 0;
exact piecewise exponentials; no leg mechanics, no delay.

| τc, k, τ_on, τ_off (ms) | Twitch (× ceiling) | Peak / half-rise from onset | Two spikes 12 / 15 ms | 60 / 80 / 100 / 120 Hz (× twitch; spikes to 90%) |
|---|---|---|---|---|
| 8, 0.3, 28, 10 | 0.29 | 9.6 / 4.4 ms | 1.66 / 1.50 | 1.75 / 2.90 (6) / 3.44 (7) / 3.44 (8) |
| 8, 0.3, 25, 10 | 0.32 | 9.6 / 4.4 | 1.64 / 1.47 | 1.70 / 2.69 / 3.13 / 3.13 |
| 8, 0.3, 35, 10 | 0.24 | 9.6 / 4.5 | 1.71 / 1.53 | 1.84 / 3.35 / 4.16 / 4.15 |
| 6, 0.2, 28, 10 | 0.29 | 9.7 / 4.4 | 1.61 / 1.45 | 1.61 / 2.43 / 3.43 / 3.43 |
| 10, 0.4, 28, 10 | 0.28 | 9.2 / 4.2 | 1.73 / 1.55 | 1.94 / 3.58 / 3.58 / 3.58 |

- Relaxation after the active state: τ_off, a half-life of 6.9 ms before the leg's mechanics.
- In brainfly the leg adds lag and smoothing. In the 10 ms run, an activation that jumped within 0.3 ms and then decayed
  gave a force peak at 13.6 ms. Add ≈2.5 ms of delay too, and the 9.6 ms peak would land near flies' 17-23 ms. This is
  an expectation, not a result.

## 5. Motor-unit recruitment in the fly tibia flexor

### 5.1 The plateau comes from one motor neuron
- Spikes were evoked in a single identified MN per line ([e]): "To evoke spikes in the fast and intermediate neurons, we
  optogenetically stimulated motor neuron dendrites in the VNC using expression of Chrimson ... Brief (10–20 ms) flashes
  of increasing intensity produced increasing numbers of spikes, corresponding spikes in the EMG, and movement of the
  tibia".
  - The Fig 4A legend gives a "50 ms flash from a 625 nm LED,~2 mW/mm2" ([f4]).
  - "Current injection in the fast and intermediate neurons failed to reliably trigger action potentials" ([e]).
- The fast MN alone drives its fibres: it "is the only motor neuron that innervates the large tibia flexor muscle fibers
  in the middle of the femur" ([e]). "(Each muscle fiber is innervated by just one motor neuron.)" (response to review,
  [e]).
- So the 28-30 uN plateau is one motor unit's, with no recruitment inside the measurement: ≈0.28-0.30 of the muscle's
  ~100 uN (derived).
- The authors' reading: "the force-per-spike curves saturated at ~10 spikes (Figure 4D). These observations suggest that
  the fast and intermediate muscle fibers fatigue during repeated stimulation." Supporting context they give:
  - "fast muscle fibers are anaerobic and lack energy stores, leading to more rapid fatigue (Kernell, 2006)";
  - flies did not maintain "sufficient resting force on the probe (>5 s) to require sustained firing of fast or
    intermediate neurons" ([e]).
- Fatigue was not tested. Not reported: force for a fixed spike count at different rates, sag within a burst, and
  recovery.
- Other readings: a fused tetanus (§3.4), junctional depression (§2.4) or mechanics (§2.5).

### 5.2 Burst rates are not reported
- Fig 4D plots peak force against spike number on log-log axes. Rates within the 3-17-spike bursts are Not reported in
  the text, the legends or the analysis scripts ([c2], [c3]).
- The only visible interval is ≈12 ms, in a two-spike example (leg_twitch_data.md).
- Inference: a 10-20 ms (or 50 ms) flash that evokes ~10-17 spikes means rates well above 80 Hz, unless firing outlasted
  the flash. Spike number and rate probably rose together with flash intensity, so Fig 4D cannot separate them.
- The per-cell data are on Dryad: 60 files, 48.76 GB, with per-cell zips of 164 MB-5.5 GB. The fast and intermediate
  force cells together exceed 4 GB ([D]; leg_twitch_data.md).

### 5.3 Higher forces need recruitment
- "Flexor 1 activity increased only during the fastest, most powerful movements"; "The highest probe forces and velocities
  were achieved only when both Flexors 1 and 2 were active together" ([e]).
- "We are certain that the calcium activity cluster we call Flexor 1 represents the activity of the fast neuron. Flexor 2,
  on the other hand, likely represents the coordinated activity of at least two intermediate neurons." (response to
  review, [e])
- So the 85-100 uN maximum needs intermediate and slow units too. Their force per spike and time course differ by orders
  of magnitude. The slow unit's force was "gradual and did not reach its peak within 500 ms". Each unit needs its own
  activation parameters, which MuJoCo's single activation per actuator can't provide.

## What this means for brainfly (my reading)

### A. Fix three things in the test before fitting
1. **Time base.** Flies' times run from the somatic spike. Add a delay d ≈ 2.5 ms between a brainfly spike and the
   muscle, or compare from force onset.
2. **Rate.** Don't treat 80 Hz as the fly's rate. Read the fast cells' spike times from the Dryad data (or ask the
   authors) and test the plateau at the measured rates. Until then, test it at 80 Hz and at ≥120 Hz, and require a
   ceiling of 28-30 uN that holds at high rates.
3. **Ceiling in force units.** Calibrate the fast unit's ceiling against probe force in brainfly's own leg. That leg's
   activation-to-force map is very concave: 9 uN at act ≈0.02 and 100 uN at act = 1, mostly from the scaled extensor's
   passive tension (leg_twitch.py). That compresses the twitch/tetanus force ratio and can hide a correct activation
   model, so fix or account for it alongside.

### B. The model (per motor unit u; exact updates at brainfly's 0.1 ms step)
```
on each somatic spike at t:      schedule c_u += R_i at t + d          (R_i = 1 unless the doublet demands Ding's R0)
every step:                      c_u *= exp(-dt / tau_c)
                                 x_u  = c_u^m / (c_u^m + k^m)
                                 tauF = tau1 + tau2 * x_u
                                 F_u  = A*x_u*tauF + (F_u - A*x_u*tauF) * exp(-dt / tauF)
muscle ctrl:                     ctrl = clip( sum_u  g_u * F_u / F_u,max , 0, 1 )      F_u,max = A*(tau1 + tau2)
```
- **Variant A (recommended).** Compute the above in numpy and make MuJoCo's own activation near-instant. Either use
  FlyGym's shipped dynprm (0.1/0.4 ms), or a general actuator with dyntype "none" and muscle gain and bias (check it
  compiles in brainfly's MuJoCo version). MuJoCo: the force formula "uses the activation state when present, and the
  control otherwise" ([mjx]).
  - g_u is the ctrl level that, held, gives unit u's ceiling at the probe (§A.3).
  - One state pair per motor neuron gives slow, intermediate and fast units their own kinetics in one tendon.
- **Variant B (fewest changes).** Keep MuJoCo's activation as the force stage.
  - Set ctrl = g·x, with x from the calcium switch, instead of 1 for 0.1 ms.
  - Set effective τ_act ≈ τ1 + τ2 ≈ 28 ms and τ_deact ≈ τ1 ≈ 10 ms. Through MuJoCo's factors this is nominal
    τ_act ≈ 28/(0.5 + 1.5a) and τ_deact ≈ 10·(0.5 + 1.5a); at a twitch's a ≈ 0.02-0.1, that is ≈43-53 ms and ≈5-7 ms
    (derived).
  - Caveat: Millard's factor makes relaxation faster after strong activation, the reverse of muscle. The fly data can't
    test that yet: tetanic relaxation is Not reported.

### C. Parameters, starting values and sources

| Parameter | Start | Range | Source | Status |
|---|---|---|---|---|
| d, spike → muscle | 2.5 ms | 2-4 | soma→EMG ≈0.6-1.0 ms ([f4] Fig 4G, fig., approx.); stimulus→force onset 2.1 ms in blowfly b1 ([TD94]) | partly measured |
| τc, active-state decay | 8 ms | 6-10 | fitted to the twitch peak and fusion; bounded by mouse free calcium (half-width 2.0 ms at 28 °C, [HZB96]) and locust flight-muscle DA (τ 14 ms at 25 °C, [MJ91]) | fitted |
| m, link steepness | 8 | ≥4 | jump-muscle skinned fibres, Hill coefficient 10.2-12.4 ([El10], [Lo22]) | measured (another fly leg-type muscle) |
| k, half-activation in spike units | 0.3 | 0.2-0.4 | one spike must saturate the link: DA 0.8 of tetanic in one twitch ([MJ91]); troponin 0.95 occupied ([BH12]) | fitted, constrained |
| R0, doublet factor | 1 | 0.5-1.5 | flies' doublet is at or below linear (§4.2); vertebrate release to later spikes is 0.1-0.3 of the first ([BH03], [BH07]) | fit only if the doublet demands it |
| τ1, relaxation at low activation | 10 ms | 8-12 | fly twitch decay τ ≈13 ms at the probe (leg_twitch_data.md), less the leg's own filtering | measured, then fitted |
| τ1 + τ2, force development at full activation | 28 ms | 25-35 | twitch/ceiling = 9/29 with t_on ≈10 ms (§4.4); slower than the active state, as in [AR70] and [BH12]; myofibrils are slower still (122 ms at 17 °C, [Fe26]) | fitted |
| Ceiling A(τ1 + τ2), fast unit | 29 uN at the probe | 28-30 | [e] Fig 4D plateau | measured |
| Unit share of the muscle | ≈0.3 | 0.28-0.30 | 28-30 of ~100 uN ([e]) | derived |

### D. Fitting order and checks
1. Delay d from the twitch half-rise (7.7-9.7 ms).
2. t_on = τc·ln(1/k) from the twitch peak (17-23 ms, less d and the leg's lag).
3. τ1 + τ2 from twitch/ceiling: 1 − e^(−t_on/(τ1 + τ2)) = 9/29.
4. τ1 from the relaxation (half gone 12-16 ms after the peak).
5. τc against k (fusion frequency ≈ 1/(τc·ln(1 + 1/k))) from the doublet at its real interval and the plateau at the
   real rates.
6. Hold out the force-against-spike-count curve (Fig 4D) at the measured rates as the prediction.
- If the doublet comes out high, try R0 < 1 (release depression) before softening the link. A gentle link loses the
  plateau or delays the peak (§4.4).

### E. Data that would pin the free parameters
- **Spike times in Azevedo's multi-spike trials** (Dryad): fixes the rate question and the fusion frequency.
- **The authors' unpublished fast-MN-stimulation muscle imaging** ([c4]): GCaMP6f at 100 Hz can't give τc. It would show
  how the active state sums across a burst.
- **A fast-indicator measurement of a fly leg muscle's calcium per spike,** or the DA method of [MJ91], applied to the
  tibia flexor.
- **Relaxation after a tetanus in any fly muscle:** this decides τ2's role, and whether Millard's form in Variant B is
  acceptable.
- **Junctional depression at the fast MN's terminal** (Azevedo's EMG could show it): this decides whether the plateau is
  muscle or synapse.

## Access limits
- Full text read:
  - Azevedo 2020 (PMC), with its analysis scripts on GitHub. The Dryad data were not downloaded (the force cells exceed
    4 GB).
  - Harischandra 2019; Frey Law & Shields 2005; Baylor & Hollingworth 2003 and 2012; Hollingworth 1996; Fenwick 2026;
    Eldred 2010; Loya 2022; Ormerod 2022; Tu & Dickinson 1994 (PDF); Helassa 2016.
  - Visible in full: Guschlbauer 2007, Paterson 2010, Ahn 2006.
- Abstract only:
  - models: Wexler 1997, Ding 2000, Bobet & Stein 1998, Brown & Loeb 2000, Zahalak & Ma 1990, Baylor & Hollingworth
    2007, Wilson 2010-2013, Hooper 2007;
  - insect muscle: Malamud & Josephson 1991, Josephson & Stevenson 1991, Desai & Lnenicka 2011, Collet 2009, Collet &
    Belzunces 2007, Lindsay 2017, Herranz 2004, Qiu 2003, Kelly 1997, Stokes 1975;
  - other: Ashley & Ridgway 1970, the parvalbumin papers;
  - the Ikeda & Koenig SICB abstract, whose year is not shown.
- Secondary sources stand in for originals:
  - the Ding and Bobet-Stein equations and values come from Frey Law & Shields 2005;
  - the Hatze equations come from Rockenfeller et al. (arXiv);
  - the Virtual Muscle equations come from its CellML encoding.
- Blocked: Springer pages, JEB silverchair PDFs (403), Cell (Lindsay 2017).
- Not downloaded: the Guschlbauer and Blümel dissertations.
- Figure reads (fig., approx.): Azevedo Fig 4G conduction delays (the axis reads "µs", presumably ms) and Katti 2022
  Fig 1v.

## Sources
[e]: https://elifesciences.org/articles/56754 (read via https://pmc.ncbi.nlm.nih.gov/articles/PMC7347388/)
[f4]: https://elifesciences.org/articles/56754#fig4
[c2]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Script_forcePerSpike.m
[c3]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Dataset3_SlowInterFast_ForcePerSpike.m
[c4]: https://github.com/tony-azevedo/FlyAnalysis/blob/main/Records/Azevedo_2020_Records/Dataset4_MNStim_LegCaImaging.m
[D]: https://doi.org/10.5061/dryad.76hdr7stb
[mjm]: https://mujoco.readthedocs.io/en/stable/modeling.html
[mjx]: https://mujoco.readthedocs.io/en/stable/XMLreference.html
[H19]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6812852/
[W97]: https://doi.org/10.1109/10.568909
[D00]: https://doi.org/10.1152/jappl.2000.88.3.917
[FL05]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1175855/
[BS98]: https://doi.org/10.1109/10.704869
[BL00]: https://doi.org/10.1023/a:1005687416896
[CBL]: https://models.physiomeproject.org/exposure/ef739f4fa746419338ff20f1e23287c1
[RG]: https://arxiv.org/abs/1411.6470
[ZM90]: https://doi.org/10.1115/1.2891126
[BH03]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2343150/
[BH07]: https://doi.org/10.1085/jgp.200709827
[BH12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3315149/
[HZB96]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2229350/
[PV99]: https://doi.org/10.1152/ajpcell.1999.276.2.C395
[PV00]: https://doi.org/10.1111/j.1469-7793.2000.00355.x
[MJ91]: https://doi.org/10.1242/jeb.159.1.65
[JS91]: https://doi.org/10.1113/jphysiol.1991.sp018800
[AR70]: https://doi.org/10.1113/jphysiol.1970.sp009158
[SW84]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1434863
[Fe26]: https://pmc.ncbi.nlm.nih.gov/articles/PMC13316580/
[El10]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2849092
[Lo22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8977141/
[WZS11]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3207158
[Ag04]: https://pmc.ncbi.nlm.nih.gov/articles/PMC381005
[Li04]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1304450
[KW98]: https://doi.org/10.1085/jgp.111.4.505
[Pa00]: https://doi.org/10.1023/A:1005656528208
[He04]: https://europepmc.org/article/MED/15161098
[Ch15]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4671713/
[Ch17]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5349783
[El14]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4232998
[Qi03]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1223341
[Ce59]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2194985
[Su26]: https://faculty.washington.edu/tuthill/docs/GluR%20manuscript%2003172026%20JT.pdf
[IK]: https://sicb.org/?p=31981
[Bl12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3501687/
[Or22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9044916/
[Pt10]: https://doi.org/10.1242/jeb.043026
[TD94]: https://authors.library.caltech.edu/records/pvfs1-c9372
[Ah06]: https://doi.org/10.1242/jeb.02392
[Gu07]: https://doi.org/10.1242/jeb.02729
[GuT]: https://kups.ub.uni-koeln.de/3001/
[Ho07]: https://doi.org/10.1152/jn.01283.2006
[Wi11]: https://doi.org/10.1007/s00422-011-0423-0
[DL11]: https://doi.org/10.1152/jn.00045.2011
[Sa05]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1449089/
[Hs20]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7573238/
[GD06]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1449689/
[Li17]: https://doi.org/10.1016/j.cub.2016.12.018
[WC26]: https://doi.org/10.64898/2026.03.11.711180
[Ka22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9636386/
[Ke97]: https://doi.org/10.1016/s0965-1748(97)00062-3
[Wh11]: https://doi.org/10.1016/j.cbpb.2011.04.003
[Co07]: https://doi.org/10.1242/jeb.02667
[Co09]: https://doi.org/10.1007/s00424-009-0642-6
[Co21]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8373864/
[St75]: https://doi.org/10.1002/jez.1401940205
[JY85]: https://journals.biologists.com/jeb/article/118/1/185/5180/A-Synchronous-Insect-Muscle-with-an-Operating
[He16]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5138832/
[Ch13]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3777791/
[Zh23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10060165/
