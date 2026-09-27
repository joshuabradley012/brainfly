<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" width="340" alt="brainfly: the fly's central nervous system seen from the front, drawn as dots from its real neuron positions, with the optic lobes in red">
  </picture>
</p>

<p align="center"><i>Closing the loop from connectome to fly.</i></p>

brainfly is an open attempt to turn a complete fruit fly connectome into a fly that senses, decides
and moves, and to say at every layer which parts are validated, which are fitted and which are
still guesses.

It works from **MaleCNS v1.0**, the first map of a whole fly central nervous system, brain and nerve
cord in one animal: **166,700 neurons and 25.6 million connections**, traced synapse by synapse in
electron microscopy. Because the nerve cord is in the map, a simulated body can be driven through the
fly's real motor neurons rather than through a few hand-picked command neurons. Nobody has done that
yet. The best-known attempt, Eon Systems' March 2026 "embodied fly", maps brain to body
[by hand, by its own account](https://eon.systems/updates/embodied-brain-emulation), and it has no
nerve cord.

## A wiring diagram is not a working fly

A connectome records who connects to whom. It doesn't record which neurons spike and which signal in
graded steps, what sign each synapse has, where the electrical synapses are, what the neuromodulators
do, or how the muscles respond. Theory says the wiring alone
[often can't pin down a network's dynamics](https://www.nature.com/articles/s41593-025-02080-4), and
in 2026 a worm's connectome with a trained decoder
[walked a simulated fly body realistically](https://www.biorxiv.org/content/10.64898/2026.03.20.713233v1).
A simulation that looks like a fly proves little.

So brainfly adds biology one layer at a time and holds each layer to two tests, written down before
it runs: it has to match data from real flies, and it has to **stop working when the wiring is
scrambled**. The plan, the evidence behind it, and a diagnosis of what has gone wrong so far are in
the [research report](reports/Embodied%20fly%20connectome%20simulation.md).

## Where it stands (September 2026)

* **The brain now steers a body, and the body turns with a rotating drum: the project's first
  pre-registered passes.** Seen through `FlyvisNative`, a drum turning counterclockwise sweeps
  front-to-back across the left eye. The left HS cells fire 29 Hz, against 10 Hz when it turns the
  other way, the right ones the reverse, and the steering neuron DNa02 follows on the same side (3.3
  against 0.8 Hz), confirmed on a fresh seed. Rewiring the connectome at random, with every neuron
  keeping as much input as before, abolishes both signals in three rewirings out of three, while the
  neurons stay active. Then the loop is closed: NeuroMechFly (FlyGym) walks inside the drum while
  DNa02 sets the drive to each side of its body (`brainfly/body.py`), and all 8 flies turn with the
  drum, at about 0.4 times its speed. The link from DNa02 to the legs is an assumption: the nerve cord
  isn't simulated, and a walking controller stands in for it.
* **The model brainfly inherited fails in three places, each traced to a modelling choice**
  ([below](#where-it-started)). Light dies at the first synapse after the eye, commands from the
  brain never reach the motor neurons, and scrambled wiring signals as well as the real wiring.
* **flyvis, run on its own terms, carries looming to the escape neuron.** brainfly now tiles flyvis's
  fitted network onto the male eye's 1,771 columns (`FlyvisNative`, `brainfly/optic.py`). On flyvis's
  own lattice the tiler rebuilds flyvis exactly. On the male eye, all 16 T4/T5 motion detector types,
  in both eyes, prefer their biologically correct direction, with the lattice orientation taken from
  dendrite anatomy alone. A looming disk (`brainfly/eye2d.py`) then drives the same side's LPLC2 at
  peaks of 28–46 Hz, and the giant fiber, the neuron that fires the escape jump, spikes in every
  fly on the loomed side, first about 80 ms before contact, and never on the other side
  ([details](#where-it-started)). LC4, the other looming detector, still barely responds. Its
  largest input is T2, and in flyvis's best-performing model T2 responds only to light increments,
  while a real T2 is excited by increments and decrements alike (Keleş et al. 2020). T2 is
  ON-and-OFF in 10 of flyvis's 50 trained models, the natural next test. An earlier port of
  flyvis's parameters onto MaleCNS's own wiring ran at the wrong operating point and is kept for
  comparison (`FlyvisOpticLobe`); an earlier giant fiber result came from a one-dimensional eye whose
  "azimuth" tracked elevation.
* **Rung 1 passes, on the sixth attempt.** Shiu et al.'s whole-brain recipe, the best-validated model
  of the fly brain, runs away on MaleCNS as it stands. A test against Brian2, an idea borrowed from
  doomfly, found brainfly's implementation of it three steps out of line, and the first three
  attempts were rerun on the corrected kernel. The pass runs on `HybridBrain`, brainfly's own
  engine, with Shiu's neuron model and four changes, each from the report or the literature: each
  synapse divided by its target's size, fast transmission only from neurons with a known fast
  transmitter, no Kenyon-to-Kenyon excitation, and no synapses onto sensory neurons. The network stays
  stable, sugar drives the proboscis motor neuron in proportion to its rate, bitter and Ir94e
  suppress it, and scrambling the wiring abolishes the route. Shuffling the synapses' strengths does
  not, so the route rests on which neurons connect ([details](#rung-1-in-detail)).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/optomotor-dark.svg">
  <img src="assets/optomotor-light.svg" width="100%" alt="Left, bar charts: under a drum turning counterclockwise the left HS cells fire about 29 spikes a second and the right about 10, and the reverse for a clockwise drum; the steering neuron DNa02 follows, about 3.3 against 0.8 spikes a second, on the side the drum sweeps front-to-back. Right, the heading of 8 walking flies over 3 s with the brain steering the body: under a counterclockwise drum every fly turns left, under a clockwise drum every fly turns right, each slower than the drum itself, and with the drum still the headings stay near zero.">
</picture>

The optomotor pathway, open loop (left; `experiments/optomotor.py`) and closed loop (right;
`experiments/closed_loop.py`). `python assets/optomotor.py` redraws it from the saved results.

## The ladder

Each rung adds the kind of model neuron and the data the biology calls for. A rung passes only if it
meets a benchmark from real flies, fixed in advance, and the effect goes away under scrambled wiring.
From the [report's plan](reports/Embodied%20fly%20connectome%20simulation.md#nine-rungs-to-an-embodied-fly-each-gated-by-real-fly-data-and-a-null-control):

| Rung | What it adds | Passes when | Status |
|---|---|---|---|
| 1. Validated baseline | Shiu et al.'s recipe on MaleCNS: raw synapse counts × one weight, silent at rest, 0.1 ms steps | sugar drives the proboscis motor neuron MN9, bitter and Ir94e inhibit it, the network stays stable, weight shuffles abolish it | **passed** on the sixth attempt (pre-registered, fresh seeds, null gated on scrambled wiring): stable, MN9 follows the sugar rate, bitter and Ir94e suppress it, and rewiring abolishes the route. It survives weight shuffles, so the route rests on which neurons connect |
| 2. Signs and modulators | MaleCNS's consensus transmitters; dopamine, octopamine and serotonin taken out of fast excitation | rung 1 still passes and false positives stay near Shiu's 1% | in progress: rung 1's pass uses consensus transmitters with the monoamines out of fast excitation; false positives not yet measured |
| 3. Eye and optic lobe | a graded optic lobe with per-type parameters; the missing photoreceptor input filled in | contrast polarity for at least 30 of 32 cell types; T4/T5 direction selectivity; looming responses of tens of Hz | in progress: flyvis on its own terms gets all 16 T4/T5 directions right, drives LPLC2 and the giant fiber, and carries a rotating drum to the steering neuron DNa02 with the right sign; LC4 still barely responds |
| 4. Central brain | per-type gains fitted to whole-brain resting-state imaging | held-out functional connectivity; a head-direction bump; a mean rate of 4 Hz or less | not started |
| 5. Nerve cord | Pugliese et al.'s recipe: raw counts, excitability scaled by size, graded premotor neurons, strong descending drive | DNg100 and DNb08 produce 7–15 Hz leg rhythms | not started |
| 6. Electrical synapses and proprioception | a curated layer of gap junctions; leg sensors driven by the body | giant fiber to jump muscle in 0.7–1.2 ms, slowing without the gap junctions as in *shakB* mutants | not started |
| 7. Body and muscles | a FlyGym body stepped with the brain: motor neurons drive torques, then a musculoskeletal foreleg | force per spike and twitch time match; the fly falls when its motor neurons are silenced | started: NeuroMechFly walks under a walking controller that the brain steers through DNa02; no motor neurons or muscles yet |
| 8. Flight, neck and song | wing power and steering, head pose, courtship song | saccades within about 10 wingbeats; song pulses about 35 ms apart | not started |
| 9. State and learning | arousal, hunger, the mushroom body's dopamine learning rule | 80–90% depression after 1 s of odour paired with dopamine | not started |

## Rung 1 in detail

[Shiu et al. (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446845/) simulated the FlyWire brain
as leaky integrate-and-fire neurons sharing one set of parameters, with a single free parameter: how
much one synapse moves its target. 91% of its 164 testable predictions held, nearly all of them in taste and grooming circuits.
[`brainfly/shiu.py`](brainfly/shiu.py) runs the same recipe on MaleCNS, and
[`experiments/shiu_baseline.py`](experiments/shiu_baseline.py) tests it against criteria fixed
before its first run:

| Test | Result |
|---|---|
| Sugar taste neurons drive MN9, the motor neuron that extends the proboscis | 65 Hz. This is the calibration target, not an independent test. |
| Water taste neurons drive MN9 | **No**: 1.5 Hz. |
| Bitter and Ir94e taste neurons cut sugar's drive by at least 25% | By 90% and 87%, but inside a network that was running away, so unreliable. |
| The network stays stable | **No**: 4,226 undriven neurons pass 100 Hz, and the activity outlasts the drive. |
| Scrambled wiring abolishes sugar → MN9 | 0 of 20 weight shuffles and 0 of 20 degree-preserving rewirings activate MN9. |

The verdict is a **fail**. These numbers come from a rerun.
[`tests/test_shiu_brian2.py`](tests/test_shiu_brian2.py) runs brainfly's kernel side by side with
Brian2, the simulator Shiu's results come from (an idea taken from
[doomfly](https://github.com/nftechie/doomfly)). The first version of the kernel failed it three ways.
It kept input that reached a neuron during its refractory period, which Brian2 drops. It delivered
input before applying the threshold instead of after, which shortened the synaptic delay by a step.
And it held neurons refractory one step too long. On a small random network it ran 27% hot. The
corrected kernel matches Brian2 spike for spike, and all four rung-1 experiments were rerun on it (the
first runs are in git history). The runaway shrank, from 7,443 hot neurons to 4,226, but every verdict
stood. A follow-up that was not pre-registered,
[`experiments/shiu_runaway.py`](experiments/shiu_runaway.py), found the runaway in the central brain,
mostly among the mushroom body's Kenyon cells, igniting within about 100 ms. Removing the nerve cord,
the synapses onto sensory neurons, the monoamine synapses (by a rule that, as the third attempt
revealed, also silenced most Kenyon-cell output) or the Kenyon-cell-to-Kenyon-cell synapses shrinks
it, to between 1,134 and 3,811 neurons above 100 Hz, and none of them stops it. At 0.20 mV per
synapse and above, the activity outlasts the drive. At 0.20 mV itself no neuron passes 100 Hz, but
13,511 are active, and the network fires 2.5 times harder after the drive than during it. At 0.18 mV
and below, it stays quiet, but sugar moves MN9 by 1.8 Hz at most. So no single global weight
carries Shiu's recipe over to MaleCNS, which counts more synapses per connection than FlyWire. (The
calibration grid also only searched down from Shiu's 0.275 mV, and hitting Shiu's own calibration
target would have needed a higher weight.)

The second attempt, [`experiments/shiu_scaled.py`](experiments/shiu_scaled.py), also pre-registered,
divides every synapse onto a neuron by that neuron's size, the scaling that the few recordings
comparing synapse counts with synaptic strength favour, or by the square root of its size. Total
synapse count stands in for size, since MaleCNS's tables carry no volumes, and both recipes calibrate
to 1.1 mV per synapse, the top of the grid. Both fail. Dividing by size comes closest of any attempt.
Only 20 undriven neurons pass 100 Hz, the most STABLE allows. MN9 follows the sugar rate: silent at 10
and 25 Hz, 68 Hz at 100 Hz. And bitter and Ir94e silence it. But activity outlasts the drive, at 23%
of its level, and 11 of 20 weight shuffles drive MN9 as well, although no degree-preserving rewiring
does. So the route depends on which neurons connect, but not enough on how strongly. The square root
runs away, with 10,278 neurons above 100 Hz. No recipe tried so far gives Shiu's MN9 response without
lasting activity or a loss of specificity.

The third attempt, [`experiments/shiu_mb.py`](experiments/shiu_mb.py), pre-registered, follows the
wiring. An average Kenyon cell gets about 284 synapses from other Kenyon cells and 55 from dopamine
neurons, both counted as fast excitation, against 125 from olfactory projection neurons and 48
inhibitory ones from APL. Neither is fast excitation in the fly: acetylcholine acts on Kenyon cells
partly through inhibitory muscarinic receptors, and dopamine, octopamine and serotonin are slow
modulators. Taking both out of the fast network (4.2 million monoamine and 1.2 million
Kenyon-to-Kenyon synapses) fails too, and it removed more than intended. Its rule for monoamine
neurons, a consensus *or predicted* transmitter of dopamine, octopamine or serotonin, also caught
4,058 of the 4,064 Kenyon cells. MaleCNS's machine prediction calls them dopaminergic, while their
consensus transmitter, like the literature, is acetylcholine. So most of the synapses removed as
monoamine synapses were Kenyon-cell outputs, and the mushroom body's output was all but silenced.
Calibration lands on 0.55 mV, where every taste test passes on paper: sugar drives MN9 at 167 Hz,
water at 80 Hz, and bitter and Ir94e cut sugar's drive by 99% and 89%. But there MN9 fires 128 Hz
when sugar arrives at only 10 Hz. The runaway drives MN9, not
the sugar, and all 20 weight shuffles and all 20 rewirings drive it as well. The network runs away
(4,764 undriven neurons above 100 Hz), and APL fires at 290 Hz with Kenyon cells averaging 68 Hz. The
first run, on the old kernel, reported every taste test passing at 0.385 mV. There too MN9 fired as
fast at 10 Hz sugar (99 Hz) as at 100 Hz (77 Hz), so that pass was no sugar response either. Taste
tests alone can't tell a response from a runaway, which is why the criteria include STABLE and
NULL.

The fourth attempt, [`experiments/shiu_signs.py`](experiments/shiu_signs.py), pre-registered,
builds on the density recipe. A diagnostic that wasn't pre-registered had traced that recipe's lasting
activity to pars intercerebralis neurosecretory cells and prow and SMP interneurons. Most of them
have no transmitter MaleCNS could call, which the sign rule counts as fast excitation by default. So
this attempt keeps in the fast network only synapses from neurons with a known fast transmitter. It
removes synapses from the 541 neurons whose consensus transmitter is a monoamine and from the 2,352
with no consensus transmitter (sensory neurons exempted), as well as Kenyon-to-Kenyon synapses. It
runs on `HybridBrain` with Shiu's neuron model, and it adds a criterion: MN9 must follow the sugar
rate. It fails.

What it gets right: MN9 follows the sugar rate (0 Hz at 10 Hz sugar, 62 Hz at 100 Hz), only 8
undriven neurons pass 100 Hz, and bitter and Ir94e cut sugar's drive by 99.8% and 84%. What fails:
activity still outlasts the drive, at 14% of its level. It sits in the Ir94e taste neurons, which
input onto their axon terminals keeps firing, and in nerve-cord circuits. And 18 of 20 weight
shuffles drive MN9, while no degree-preserving rewiring does. A check afterwards showed why that
weight shuffle can't be passed. Shuffling the counts runs these networks away, with 50,000–83,000
neurons above 100 Hz. Even shuffling the final synaptic strengths leaves 9,000–27,000 there. A
network that runs away drives MN9 whatever its routing.

The fifth attempt, [`experiments/shiu_sensory.py`](experiments/shiu_sensory.py), pre-registered,
adds what the report's rung-1 recipe specifies and the first four left out: no synapses onto
sensory neurons. It is the first network on MaleCNS to pass STABLE. Activity stops with the drive,
apart from the proboscis motor program winding down over about 250 ms, and only 2 undriven neurons
pass 100 Hz. MN9 follows the sugar rate (0 Hz at 10 Hz sugar, 43 Hz at 100 Hz), and bitter and Ir94e
cut sugar's drive by 99.9% and 84%.

It still fails, on its null. The global weight shuffle runs these networks away (61,000–79,000
neurons above 100 Hz), so this attempt instead shuffled strengths among each neuron's inputs of one
sign. That keeps every neuron's partners and its total excitation and inhibition. Sugar still drives
MN9 in 15 of 20 such networks, which stay quiet. Degree-preserving rewiring, which scrambles who
connects to whom, abolishes the route in all 20 and leaves the network quiet too. So in this model,
the route from sugar to MN9 depends on which neurons connect, not on which of a neuron's partners
carries which strength.

So the sixth attempt, [`experiments/shiu_rewiring.py`](experiments/shiu_rewiring.py),
pre-registered, gates on the report's rule that a rung passes only if its effect degrades under
scrambled wiring, and reports the weight shuffles without gating on them. It tests the fifth
attempt's network unchanged, calibrated weight included, on seeds no earlier run used. The null has
two parts: degree-preserving rewiring, and rewiring that keeps each synapse's target superclass (so
each neuron keeps its number of synapses into each of the 27 superclasses). **It passes.** Activity
stops with the drive, and only 2 undriven neurons pass 100 Hz. MN9 is silent at 10 Hz sugar and
fires 41 Hz at 100 Hz. Bitter and Ir94e cut sugar's drive by 100% and 81%. And both kinds of
rewiring abolish the route in 20 of 20 networks, which stay quiet. As reported but not gated,
shuffling the strengths among each neuron's inputs leaves the route in 16 of 20, and global
shuffles run 18 of 20 networks away.

What the pass means: on MaleCNS, Shiu's neuron model gives a stable network in which sugar drives the
proboscis motor neuron in proportion to its rate, and bitter and Ir94e suppress it, through a route
set by which neurons connect. Getting there took four changes, each from the report or the
literature:
- each synapse divided by its target's size
- fast transmission only from neurons with a known fast transmitter, with the monoamines moved out
- no Kenyon-to-Kenyon excitation
- no synapses onto sensory neurons
It also took a choice of null, made after the fifth attempt. What it doesn't show: that the route
depends on the synapses' relative strengths, as Shiu found on FlyWire; the water response, which
never appears; and Shiu's grooming test, which MaleCNS can't run.

Two limits apply throughout. The taste-neuron labels are provisional: LB3a as water and LB3b–c as
sugar come from an unreviewed MaleCNS port, and LB1a–d as bitter and LB1e as Ir94e-like from summaries
of the gustatory connectome papers. And Shiu's grooming test (JO-CE neurons drive aBN1, JO-F neurons
don't) can't run here, because MaleCNS has no aBN1 annotation.

## Where it started

brainfly began from a simple whole-CNS model, still here as `brainfly.FlyBrain`. It runs each of MaleCNS's 166,700 neurons as the same leaky
integrate-and-fire unit, following [Fly64](https://github.com/ornata/fly): a 100 ms membrane stepped
every 20 ms, a constant drive plus noise, and each neuron's inputs scaled to add up to 1. It is fast,
about 6 ms per 20 ms step on an Apple M4 Pro CPU, and it gets short routes right. Drive the looming
detectors on one side, and that side's giant fiber, the neuron that fires the escape jump, fires:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/loom-dark.svg">
  <img src="assets/loom-light.svg" width="100%" alt="A map of the fly's brain seen from the front, with the driven looming detectors on the fly's left in red and the neurons that responded marked, beside a spike raster: while the looming detectors are driven, the left giant fiber fires at 25 Hz in all 8 flies and the right giant fiber stays silent.">
</picture>

In 8 simulated flies, driving the 165 LC4 and LPLC2 looming detectors on the fly's left for one
second takes the left giant fiber from 0.2 to 25 spikes a second in every fly. The right one stays
silent, and 162 of the 187 other neurons that speed up by 5 Hz or more are on the left
(`python assets/loom.py` redraws it). That is real but weak evidence. It's a short, heavily weighted
feedforward route that simple graph traversal also predicts, and it hasn't been run against scrambled
wiring yet.

Past shortcuts like this one, the inherited model fails. The report traces each failure to a choice
that no validated fly model makes:

| Symptom | Measured | Likely causes | What the evidence points to |
|---|---|---|---|
| Light stops at the first synapse after the eye | L1 +0.1 Hz; LC4 and LPLC2 unmoved | Photoreceptors inhibit the lamina, and a spiking neuron that is silent at rest can't be inhibited further. | A graded retina and lamina. Done: right signs, too weak. |
| Looming is too weak even with a graded eye | LPLC2 +1.2–1.5 Hz, against tens of Hz in real flies | MaleCNS has 3,377 of about 10,650 expected photoreceptors, and 962 of its 1,769 lamina columns get no photoreceptor input. Normalisation dilutes the rest; one gain for every type; a 100 ms membrane. | Fill in the missing input, model the eye in 2-D, and give the optic lobe flyvis's fitted per-type time constants, resting levels and synapse strengths. All done: with a realistic looming disk, LPLC2 +3.4–5.1 Hz, LC4 +0.7 Hz and the giant fiber +1.4–1.7 Hz. A fast loom doesn't help LC4: on MaleCNS wiring, flyvis's OFF pathway rests below threshold. flyvis on its own terms (`FlyvisNative`) drives LPLC2 at tens of Hz and the giant fiber in every fly; LC4 waits on T2's polarity. |
| Commands never reach the motor neurons | Under 0.6 Hz in every motor group | Sum-to-one normalisation dilutes a command roughly 100–1,000× per synapse; no size-scaled excitability; a slow membrane; weak drive; no electrical synapses. | Raw counts × one scale; excitability scaled by size; graded premotor neurons; test DNg100 and DNb08. |
| Scrambled wiring signals as well as the real wiring | 0.87 vs 0.83 bits at 2 ms steps | Under normalisation a rewiring leaves every neuron's total input unchanged, and the test only measured loudness. | Tests of routing, against a ladder of null models. |
| Resting activity runs hot | About 12 Hz in the central brain, against a metabolic ceiling of about 4 Hz | Constant drive; no presynaptic gain control. | A zero or fitted baseline. |

In the report's words, "the failures are a map of which refinements the evidence requires rather than
a sign that the approach is broken."

<details>
<summary><b>Every experiment on the inherited model</b></summary>

<br>

| Script | Question | Answer |
|---|---|---|
| `experiments/motor_readout.py` | Does what the fly sees reach its command neurons, with Fly64's settings or brainfly's? | No, with either. Under Fly64's settings every neuron rests at threshold, and the command neurons fire at 3–4 Hz (forward 0.8 Hz) whatever the scene, darkness included; no scene moves any of them by 3 Hz. Under brainfly's defaults they are nearly silent, and just as blind. |
| `experiments/inject.py` | Past the eye, do the detectors drive the right outputs? | Yes, on the same side only: driving the left looming detectors raises the left giant fiber by 17 Hz (at 0.3 V a step) to 46 Hz (at 0.8 V), and courtship-tracking LC10a raises the left steering neuron DNa02 by 1.9–4.2 Hz; the right side's stay within 0.2 Hz. |
| `FlyBrain(sensory_input=False)` | Why do the smell neurons sit at the rate ceiling? | Olfactory receptor neurons get 0.43 of their 0.45 net input from each other. Removing synapses onto sensory neurons ends the runaway. |
| a two-fly song test (since removed) | Can two brains signal to each other through song and hearing? | Yes, but only through loudness, and at 2 ms steps scrambled wiring carries as much (0.87 vs 0.83 bits). |
| `experiments/eyepath.py` | Does a graded retina and lamina let looming through? | With the right signs along the whole pathway, but LPLC2 rises only 1.2–1.5 Hz: a fail against its 3 Hz bar. Its all-spiking reference run shows the original model's failure: a loom drops the photoreceptors by 7 Hz, but L1 moves 0.1 Hz and LC4, LPLC2 and the giant fiber not at all. |
| `experiments/eyepath_filled.py` | With the missing photoreceptor input filled in, does looming reach the escape neuron through the eyes? | Only with an unrealistic stimulus: on the 1-D eye, a band darkening up to 90% of one eye raised the same side's giant fiber by 2.4–3.2 Hz. LC4's 2.7 Hz missed its 3 Hz bar, so the test failed anyway. |
| `experiments/eyepath_2d.py` | With a 2-D eye from a micro-CT map and a proper looming disk, does looming reach the escape neuron? | No. At settings that keep the resting network healthy, LPLC2 on the correct side rises about 1 Hz and LC4 0.5 Hz, and the giant fiber doesn't reliably respond. With the fill, blind parts of the eye respond like intact ones, but every response stays under 0.7 Hz. |
| `experiments/eyepath_flyvis.py` | With flyvis's fitted optic lobe on MaleCNS wiring? | All four T4 subtypes prefer the correct direction (DSI 0.21–0.49; T5 only two of four). At the strongest coupling tried, looming raises LPLC2 by 3.4–5.1 Hz, but LC4 only 0.7 Hz and the giant fiber 1.4–1.7 Hz. A fail. |
| `experiments/eyepath_fast.py` | Is LC4 only held back by the slow loom? A loom ten times faster, at 2 ms steps. | No. The fast loom raises LC4 no more than the slow one (+0.0–0.8 Hz at every coupling), while LPLC2 rises 1.1–8.4 Hz on average and peaks at 15–29 Hz. At the strongest coupling the loomed side's giant fiber fires two spikes in every fly and the other side's none, within 0.2 s after the projected contact, when a real fly would already be escaping. The test fails. (Its secondary ESCAPE test is also recorded as failed, only because the pre-registered t-test scores a response identical in every fly as t = 0.) The slow loom at 2 ms repeats the 20 ms result, and T4 direction selectivity is unchanged. |
| `experiments/flyvis_port.py` | How faithful is the port of flyvis to MaleCNS wiring? | Faithful in the input layers (photoreceptors, lamina, Tm9), not deeper. On grey, T4a/b rest at +2.1 instead of 0, T2 at +7.7 instead of +3.5, and OFF cells so far below zero that an OFF step barely changes their output. The port lacks the resting inhibition of CT1 (left out), Mi12 (not in MaleCNS) and R7/R8 (absent from the filled columns), and recurrent loops amplify the shift. flyvis's own T2 responds to ON steps only. |
| `experiments/flyvis_native.py` | Is `FlyvisNative` flyvis, and is it oriented right on the male eye? | Yes. Tiled onto flyvis's own lattice it rebuilds flyvis's 45,669 cells and 1,513,231 synapses (weights within 1e-7) and reproduces a flash within 3e-6. The orientation, from T4/T5 dendrite anatomy alone, picks one lattice symmetry on both sides, and under it all 16 T4/T5 types, in both eyes, prefer their biological direction (DSI 0.73–0.94). |
| `experiments/eyepath_native.py` | With flyvis on its own terms, does looming reach LC4, LPLC2 and the giant fiber? | LPLC2 and the giant fiber, yes; LC4, no, so the test fails. At gain 3 the fast loom raises LPLC2 8.3–9.2 Hz on average (peaks 28 Hz) and the loomed side's giant fiber fires in every fly, the other side's never, first about 80 ms before contact; at gain 10, 21–23 Hz and 8–10 Hz. LC4 rises at most 0.4 Hz. |
| `experiments/optomotor.py` | Does a rotating drum reach the HS cells and the steering neuron DNa02 with the biological signs? | Yes, confirmed on a fresh seed at the lowest gain: under a counterclockwise drum the left HS cells fire 29 Hz and the right 10 Hz, and the reverse under a clockwise drum (difference 37.6 Hz, t = 632); DNa02's left-minus-right rate is 5.3 Hz higher (t = 21). DNa01, the secondary test, carries no signal. 65 of 455 descending neuron types carry the direction. No scrambled-wiring control yet. |
| `experiments/optomotor_null.py` | Does the optomotor signal need the connectome's wiring? | Yes. On three random rewirings (every neuron keeping its total input, 0.6% of the original pairs still connected), the HS signal falls from 37.6 Hz to -0.1 to +0.2 Hz and DNa02's from 5.3 Hz to 0.6-1.2 Hz (t up to 5 in one rewiring, still under its 2 Hz bar); 8-13 descending neuron types keep a direction signal, against 65. HS cells stay active but stop responding to the grating. The rewired brains rest quieter (0.8 Hz against 8.7). |
| `experiments/closed_loop.py` | With the brain steering NeuroMechFly through DNa02, does the fly turn with a rotating drum? | Yes: all 8 flies turn with it, +19.6 deg/s on average under a counterclockwise drum and -14.1 under a clockwise one (difference 33.7 deg/s, t = 8.7), against +4.7 with the drum still; about 0.4 times the drum's 40 deg/s. With the link cut, both directions give identical paths. |
| `experiments/optomotor_hybrid.py` | Does the brain that passed rung 1 (`HybridBrain`, nothing changed for vision) carry the drum's signal from flyvis to DNa02? | No, pre-registered, at every gain tried (1-100). The signal gets through: HS swings by 74-210 Hz between the two directions, and at gains 3 and 10 DNa02 steers the right way. But the network runs away: 600-20,000 neurons pass 100 Hz. A check afterwards (not pre-registered) found the brain still firing at 75% of its drum-time level a second after the drum stopped, once flyvis itself had settled. The persistent activity is in the central complex (PFN cells), the anterior visual pathway (TuBu cells) and the nerve cord. Stable under a taste, rung 1's network is not stable under full-field vision. |
| `experiments/optomotor_hybrid2.py` | Is there a lower gain where vision reaches DNa02 in that brain without igniting it? | No, pre-registered, with stability now measured after flyvis settles and the hot count leaving out the visual system. At gain 0.03 nothing gets through. At 0.1 HS carries the direction (11.6 Hz) but DNa02 stays silent, and at 0.3 the central circuits ignite again. A brain silent at rest, like Shiu's, has no window where a visual signal is strong enough to reach DNa02 yet too weak to set its recurrent circuits running. FlyBrain, whose neurons idle near threshold, has one. |
| `experiments/rest_probe.py` | Exploratory, not pre-registered: can uniform background give that brain a resting state? | No. With the same Poisson background for every neuron, the network is either silent or, just above a threshold, holds a stable state in which half the brain is silent and a few thousand neurons run over 100 Hz (mean 7-9 Hz, never the report's 4 Hz or less with few hot neurons). The hot neurons are the mushroom body (Kenyon cells averaging 42 Hz, where real ones fire under 1 Hz; MBONs 91 Hz; APL pinned at 179 Hz) and the central complex's PFN cells. The mushroom body's measured properties calm it: a graded APL, with Kenyon cells resting at -61 mV, brings Kenyon cells to 12 Hz (3 over 100 Hz) and MBONs to 40 Hz. But 2,100 other neurons stay over 100 Hz, in visual projection neurons driven by the optic lobe's own activity, the central complex and antennal-lobe local neurons. A resting state needs per-type properties throughout, which is rung 4's fitting. |
| `experiments/vnc/relay.py` | Do commands from the brain reach the motor neurons? | No. Walking, steering, escape and backward commands, each driven at 26 Hz, move no pool of motor neurons (neck, front, middle or hind segment, either side) by more than 0.17 Hz. Earlier calibrations with the inherited code, since retired, found the same: raising the nerve cord's gain and drive, or amplifying just the relay, let commands through only by driving the motor neurons at rest, and 2–5 ms steps didn't help. |

Every eye experiment before `eyepath_2d.py` used the one-dimensional eye in `brainfly/eyes.py`, whose
"azimuth" turned out to follow elevation (r = 0.93), so its looms were bands sweeping across most of
one eye. The sides were right; the geometry wasn't.

</details>

## How the work is done

Four habits from the report keep every rung honest:

* **Biological timescales.** Spiking neurons step at 0.1 ms, as in Shiu's model, so that 1.8 ms
  synaptic delays and 2.2 ms refractory periods mean something.
* **Score routing, not gross activity.** Criteria test the correct side, the correct target against
  matched decoys, dose-response, latency order and silence after the stimulus.
* **Climb a ladder of null models.** Weight shuffles first, then degree-preserving rewiring, then
  ensembles matched for degree and weight, then rewiring that keeps cell classes. Anything with a
  trained decoder must also fail with a non-fly connectome and with noise as input.
* **Check robustness to wiring variation.** Key results are repeated with only the conserved
  connections (more than 10 synapses, or more than 1% of a neuron's input) and with the matching
  FlyWire or BANC wiring.

Parameters should be shared within a cell type and fitted as ensembles, not hand-tuned to a single point.
Pass criteria go into an experiment before its first run, post hoc analyses say so, and failed results
stay in the record.

## Use it

Three models share the package:

* **`brainfly.FlyBrain`** is the inherited whole-CNS model: 20 ms steps (2 ms optional), faster than real
  time on a recent CPU or an NVIDIA GPU, with opt-in graded neurons, per-type parameters, an
  imputed retina, a 2-D eye (`brainfly.eye2d`), flyvis's fitted optic lobe (`brainfly.optic`) and a
  walking body (`brainfly.body`). It is not validated, and its failures are listed above.
* **`brainfly.shiu.ShiuBrain`** is rung 1: Shiu et al.'s recipe on MaleCNS, in 0.1 ms steps, with many
  trials run in parallel, any neurons silenced, or any synapse matrix (a shuffled one, say) swapped in.
  It matches Brian2 spike for spike.
* **`brainfly.hybrid.HybridBrain`** is brainfly's own model, under construction: Shiu's kernel with
  each cell type free to differ, as the report's biophysics calls for. A type can be graded instead of
  spiking, with no rate ceiling, and can have its own membrane time constant, threshold, reset,
  refractory period, resting drive and synaptic scale. Chosen edges can act through a slow current.
  Its state carries over between calls, so it can be stepped in a loop with a body. With nothing
  changed, it is Shiu's model exactly. On rung 1's network it simulates one fly faster than real
  time on one core of an Apple M4 Pro (0.84 s per simulated second), and 8 flies in 0.88 s.
  `set_release` lets an optic lobe simulated elsewhere drive it: `FlyvisNative` sets the release
  of its 69,917 neurons every 2 ms, in about 1 ms.

```sh
pip install "brainfly[build] @ git+https://github.com/joshuabradley012/brainfly"
```

`[build]` adds pandas, pyarrow and openpyxl, which read the raw MaleCNS tables that `ShiuBrain`,
`brainfly.eye2d` and `brainfly.optic` run on, and rdata, which reads the eye map behind
`brainfly.eye2d`. The first of them to run downloads the tables (~1.1 GB) and caches the synapse
counts. `[flyvis]` adds flyvis and PyTorch for `brainfly.optic`, which fetches flyvis's pretrained
models (3.4 MB) on first use. `[body]` adds FlyGym and MuJoCo for `brainfly.body` (Python 3.12+). `FlyBrain` alone needs none of these: the first `FlyBrain()` fetches a
prebuilt copy of its brain files (~260 MB). Add `[gpu]` for CuPy on an NVIDIA GPU (CUDA 12). Set
`FLY_DATA=/some/path` to keep the data somewhere other than `~/fly-data`.

The inherited model, looming on the left:

```python
from brainfly import FlyBrain

brain = FlyBrain()                              # first run downloads it (~260 MB)
loom = brain.cells(["LC4", "LPLC2"], side="L")  # looming detectors, fly's left
left = set(brain.cells(["DNp01"], side="L"))    # the giant fibers: escape commands
right = set(brain.cells(["DNp01"], side="R"))

for _ in range(100):                            # settle for 2 s (20 ms steps)
    brain.step()

spikes = {"left": 0, "right": 0}
for _ in range(50):                             # 1 s of looming on the left
    fired = set(brain.step(inject=[(loom, 0.4)]))
    spikes["left"] += bool(fired & left)
    spikes["right"] += bool(fired & right)
print(spikes)                                   # {'left': 25, 'right': 0}
```

Rung 1, a taste of sugar, which runs in about 4 s on an Apple M4 Pro once numba has compiled it:

```python
from brainfly.shiu import ShiuBrain

brain = ShiuBrain(trials=8)                      # Shiu et al.'s recipe on MaleCNS
sugar = brain.cells(["LB3b", "LB3c"], side="L")  # sugar taste neurons (provisional labels)
mn9 = brain.cells(["MN9"], side="L")             # extends the proboscis

result = brain.run(1.0, drive=[(sugar, 100.0)])  # 1 s of sugar at 100 Hz, 0.1 ms steps
hot = result.rates > 100
hot[sugar] = False
print(f"MN9 {result.rates[mn9].mean():.0f} Hz, {hot.sum():,} other neurons above 100 Hz")
# MN9 75 Hz, 4,312 other neurons above 100 Hz
```

<details>
<summary><b><code>FlyBrain</code> options</b></summary>

<br>

* `device` (`"cpu"`, `"cuda"` or `"auto"`, or set `FLY_DEVICE`): numba on the CPU, CuPy on an NVIDIA
  GPU. The whole connectome fits in about 210 MB of GPU memory, and a step takes 1.4 ms on an RTX 4060
  laptop GPU. Both devices run the same model; only the random noise differs.
* `batch` (default `1`): independent flies with the same wiring, each with its own voltages and
  noise. Inputs can be the same for every fly or differ per fly.
* `dt` (default `0.020`): the step length. `tonic` is rescaled so a silent neuron settles at the same
  voltage. At `dt=0.002` the network runs far hotter unless you also set a refractory period;
  `refractory=0.004` matched the 20 ms brain's resting descending-neuron rate. Graded release is set
  per 20 ms, so a coupling carries over to other steps; eye input, as in the inherited model, is added
  once per step.
* `sensory_input` (default `True`): `False` removes every synapse onto sensory neurons.
* `refractory` (default `0`): how long, in seconds, a neuron stays at 0 after a spike.
* `graded` (default none): cell types or superclasses simulated as graded neurons that release
  transmitter continuously, like the real retina and lamina.
* `cell_params`: a time constant, threshold, tonic drive or gain per cell type or superclass.
* `fill_retina` (default `False`): adds an imputed photoreceptor bundle to each of the 962 lamina
  columns MaleCNS lost at the edge of its volume, wired like the median intact column
  (`brainfly/retina.py`). It is imputed, not observed.

`brain.set_graded(neurons, release)` sets graded neurons' release from outside the model, which is
how `FlyvisOpticLobe` drives the rest of the brain.

`brain.cells([...])` takes cell types, or whole superclasses such as `"descending_neuron"`.

</details>

## What's in the repository

| Path | What it is |
|---|---|
| [`reports/`](reports/) | the research report: what each layer of the fly needs, which models have been validated, why the inherited model fails, and the nine-rung plan |
| [`research_notes/`](research_notes/) | the sourced notes behind the report: senses, neuron biophysics, the nerve cord, muscles and body models, datasets, and this project's experiments |
| `brainfly/brain.py` | `FlyBrain`, the inherited model, on CPU (numba) or NVIDIA GPU (CuPy), one fly or a batch |
| `brainfly/shiu.py` | `ShiuBrain`, rung 1, and the raw signed synapse counts it runs on |
| `brainfly/hybrid.py` | `HybridBrain`, brainfly's own per-type model, built on Shiu's kernel |
| `brainfly/nulls.py` | null models: weight shuffles (global, or within each neuron's inputs) and rewiring (degree-preserving, or keeping each connection's target class), each under a second on the whole connectome |
| `brainfly/retina.py` | the photoreceptor input MaleCNS lost at the edge of its volume, imputed from the intact columns |
| `brainfly/build.py`, `data.py` | building the brain files from MaleCNS v1.0, or fetching a prebuilt copy |
| `brainfly/eye2d.py` | a 2-D compound eye: each photoreceptor looks in its measured direction, from a micro-CT eye map; looming disks and moving edges |
| `brainfly/optic.py` | `FlyvisNative`: flyvis's own network tiled onto the male eye, feeding `FlyBrain`; `FlyvisOpticLobe`, the earlier port onto MaleCNS wiring |
| `brainfly/body.py` | NeuroMechFly (FlyGym 2.1) walking in a virtual-reality arena, and `Loop`, which steps eyes, optic lobe, brain and body together (`pip install "brainfly[body]"`) |
| `brainfly/eyes.py` | the original 1-D eye, kept so the early eye experiments still run |
| `experiments/shiu_*.py` | rung 1: the pre-registered attempts and the runaway follow-up, with results in `.json` next to them |
| `experiments/` (the rest) | the experiments on the inherited model, listed [above](#where-it-started) |
| `assets/` | the logo and the looming figure, and the scripts that draw them from the data |
| `tests/` | `python -m pytest`: both 0.1 ms kernels against Brian2, `FlyBrain`'s spikes against hashes recorded from the code behind every result, and the build against the release (`pip install "brainfly[test]"`) |

<details>
<summary><b>The data, and building it yourself</b></summary>

<br>

Nothing here is trained: the network is the fly's wiring diagram. `brainfly download` fetches the two
network files this project builds and publishes (each checked against its sha256). `brainfly build`
makes them yourself from the public MaleCNS v1.0 release, fetching the four source files below into
`$FLY_DATA/raw/` first, unless they're already there. Each source file is checked against its sha256
too, and the build reproduces the published files byte for byte:

| File | Size | Contents | From |
|---|---|---|---|
| `connectome-weights-male-cns-v1.0-minconf-0.5.feather` | 1.05 GB | synapse counts for every connected pair of neurons | [the MaleCNS release](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather) |
| `body-annotations-male-cns-v1.0-minconf-0.5.feather` | 14 MB | each neuron's type, side, superclass and cell body position | [the MaleCNS release](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather) |
| `body-neurotransmitters-male-cns-v1.0.feather` | 43 MB | each neuron's predicted transmitter | [the MaleCNS release](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather) |
| `optic-columns.xlsx` | 0.1 MB | the medulla column of each L1, R7 and R8 neuron | [flyconnectome/2025malecns](https://github.com/flyconnectome/2025malecns/blob/67767d2233657983993ff6c2be48e836a935863c/supplemental_data/optic-column-type-assignments-v1.0.xlsx) |

On a slow or flaky connection, fetch them yourself (curl's `-C -` resumes a partial download):

```sh
cd "${FLY_DATA:-$HOME/fly-data}" && mkdir -p raw && cd raw
SRC=https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome
for f in connectome-weights body-annotations; do curl -LO -C - "$SRC/$f-male-cns-v1.0-minconf-0.5.feather"; done
curl -LO -C - "$SRC/body-neurotransmitters-male-cns-v1.0.feather"
curl -L -o optic-columns.xlsx "https://raw.githubusercontent.com/flyconnectome/2025malecns/67767d2233657983993ff6c2be48e836a935863c/supplemental_data/optic-column-type-assignments-v1.0.xlsx"
```

`brainfly build` then takes under a minute. It writes `weights.npz` (205 MB: synapse counts, signed by
transmitter, each neuron's input scaled to at most one unit) and `brain.npz` (cell types, sides, cell
body positions, superclasses, four descending-neuron read-out groups, and the photoreceptors with their
1-D azimuths) into `$FLY_DATA`: **166,700 neurons and 25,582,938 connections**. The first `ShiuBrain()`
adds `counts.npz`, the same connections as raw signed synapse counts.

To look around the same data without downloading anything, use [neuPrint](https://neuprint.janelia.org)
(dataset `male-cns:v1.0`), where you can look up any neuron's inputs and outputs, or the
[MaleCNS site](https://male-cns.janelia.org).

</details>

## Credits

* **Connectome:** MaleCNS v1.0 by FlyEM (HHMI Janelia), the University of Cambridge, the MRC
  Laboratory of Molecular Biology and Google Research, used under
  [CC BY 4.0](https://male-cns.janelia.org/download/). If you use it, cite
  Berg, S. et al. (2026), *Sexual dimorphism in the complete connectome of the Drosophila male central
  nervous system*, *Cell*, and follow the [MaleCNS attribution terms](https://male-cns.janelia.org/download/).
* **Rung 1** reimplements the model of Shiu, P. K. et al. (2024), *A Drosophila computational brain
  model reveals sensorimotor processing*, *Nature* 634
  ([code](https://github.com/philshiu/Drosophila_brain_model)).
* **The 2-D eye** uses the micro-CT eye map of Zhao et al., *Eye structure shapes neuron function in
  Drosophila motion vision* ([reiserlab/eyemap_T4](https://github.com/reiserlab/eyemap_T4), GPL-3.0),
  which `brainfly.eye2d` downloads on first use. It is not redistributed here.
* **The body** is NeuroMechFly v2: Wang-Chen, S. et al. (2024), *NeuroMechFly v2: simulating embodied
  sensorimotor control in adult Drosophila*, *Nature Methods* 21, as packaged in FlyGym 2.1
  ([code](https://github.com/NeLy-EPFL/flygym), Apache-2.0), with its hybrid turning controller.
* **The optic lobe's parameters** come from flyvis: Lappalainen, J. K. et al. (2024),
  *Connectome-constrained networks predict neural activity across the fly visual system*, *Nature*
  634 ([code](https://github.com/TuragaLab/flyvis), MIT). `brainfly.optic` downloads the pretrained
  models on first use.
* **The inherited model's** neuron model, weight normalisation and optic-column handling follow
  [Fly64](https://github.com/ornata/fly) by Jessica Paquette.
* **Sources:** what this README says about other people's work comes from the
  [research report](reports/Embodied%20fly%20connectome%20simulation.md), which cites it inline.
* **The logo** is the same data: the cell bodies of the MaleCNS neurons seen from the front, as a
  halftone, with the optic lobes in the red of the eyes they sit behind. The wordmark is set in
  [Newsreader](https://github.com/productiontype/Newsreader) by Production Type (SIL Open Font
  License).

## License

brainfly is MIT-licensed ([LICENSE](LICENSE)).

The MaleCNS connectome data is **not** in the repository or the package. `brainfly build` downloads it
from its source, and `brainfly download` fetches files derived from it (the normalised weight matrix
and neuron annotations). Both stay under the data's own
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license from FlyEM (HHMI Janelia) and
collaborators.
