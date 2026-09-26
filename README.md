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

* **The model brainfly inherited fails in three places, each traced to a modelling choice**
  ([below](#where-it-started)). Light dies at the first synapse after the eye, commands from the
  brain never reach the motor neurons, and scrambled wiring signals as well as the real wiring.
* **Light now reaches the escape neuron through the eyes, weakly.** With the optic lobe graded and
  the photoreceptor input MaleCNS lost at the edge of its imaged volume filled in, a looming shadow
  raises the same side's LPLC2 looming detectors by 4.1–4.8 Hz and its giant fiber by 2.4–3.2 Hz,
  with the other side flat, in three seeds. That is the whole path, from photoreceptors to the
  neuron that fires the escape jump. It still fails its pre-registered test, because LC4 rises
  about 2.7 Hz against a 3 Hz bar ([details](#where-it-started)). The eye is also still simple. It
  is one-dimensional, so each photoreceptor knows only its azimuth, and the "shadow" is a dark,
  full-height stripe that widens as it sweeps in, not an expanding disk. In the last 0.3 s of the
  measurement the stripe starts to cover the other eye too, reaching half of it by the end, though
  the response stays on the correct side.
* **Rung 1 has failed twice.** Shiu et al.'s whole-brain recipe, the best-validated model of the fly
  brain, runs away on MaleCNS. Scaling each synapse by the size of its target shrinks the runaway
  22–37×, but doesn't end it, and then scrambled wiring drives the proboscis motor neuron too. No
  recipe tried so far gives Shiu's response without a runaway or a loss of specificity
  ([details](#rung-1-in-detail)).

## The ladder

Each rung adds the kind of model neuron and the data the biology calls for. A rung passes only if it
meets a benchmark from real flies, fixed in advance, and the effect goes away under scrambled wiring.
From the [report's plan](reports/Embodied%20fly%20connectome%20simulation.md#nine-rungs-to-an-embodied-fly-each-gated-by-real-fly-data-and-a-null-control):

| Rung | What it adds | Passes when | Status |
|---|---|---|---|
| 1. Validated baseline | Shiu et al.'s recipe on MaleCNS: raw synapse counts × one weight, silent at rest, 0.1 ms steps | sugar drives the proboscis motor neuron MN9, bitter and Ir94e inhibit it, the network stays stable, weight shuffles abolish it | **failed** twice |
| 2. Signs and modulators | MaleCNS's consensus transmitters; dopamine, octopamine and serotonin taken out of fast excitation | rung 1 still passes and false positives stay near Shiu's 1% | not started |
| 3. Eye and optic lobe | a graded optic lobe with per-type parameters; the missing photoreceptor input filled in | contrast polarity for at least 30 of 32 cell types; T4/T5 direction selectivity; looming responses of tens of Hz | in progress: light reaches the giant fiber through the eyes, weakly |
| 4. Central brain | per-type gains fitted to whole-brain resting-state imaging | held-out functional connectivity; a head-direction bump; a mean rate of 4 Hz or less | not started |
| 5. Nerve cord | Pugliese et al.'s recipe: raw counts, excitability scaled by size, graded premotor neurons, strong descending drive | DNg100 and DNb08 produce 7–15 Hz leg rhythms | not started |
| 6. Electrical synapses and proprioception | a curated layer of gap junctions; leg sensors driven by the body | giant fiber to jump muscle in 0.7–1.2 ms, slowing without the gap junctions as in *shakB* mutants | not started |
| 7. Body and muscles | a FlyGym body stepped with the brain: motor neurons drive torques, then a musculoskeletal foreleg | force per spike and twitch time match; the fly falls when its motor neurons are silenced | not started |
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
| Sugar taste neurons drive MN9, the motor neuron that extends the proboscis | 60 Hz. This is the calibration target, not an independent test. |
| Water taste neurons drive MN9 | **No**: 3.6 Hz. |
| Bitter and Ir94e taste neurons cut sugar's drive by at least 25% | By 54% and 71%, but inside a network that was running away, so unreliable. |
| The network stays stable | **No**: 7,443 undriven neurons pass 100 Hz, and the activity outlasts the drive. |
| Scrambled wiring abolishes sugar → MN9 | 0 of 20 weight shuffles and 0 of 20 degree-preserving rewirings activate MN9. |

The verdict is a **fail**. A follow-up that was not pre-registered,
[`experiments/shiu_runaway.py`](experiments/shiu_runaway.py), found the runaway in the central brain,
mostly among the mushroom body's Kenyon cells, igniting within about 100 ms. Removing the nerve cord,
the synapses onto sensory neurons, the monoamine synapses or the Kenyon-cell-to-Kenyon-cell synapses
shrinks it, and none of them stops it. At 0.20 mV per synapse and above, the network runs away. At
0.18 mV and below, it stays quiet, but sugar moves MN9 by 2.2 Hz at most. So no single global weight
carries Shiu's recipe over to MaleCNS, which counts more synapses per connection than FlyWire. (The
calibration grid also only searched down from Shiu's 0.275 mV, and hitting Shiu's own calibration
target would have needed a higher weight.)

The second attempt, [`experiments/shiu_scaled.py`](experiments/shiu_scaled.py), also pre-registered,
divides every synapse onto a neuron by that neuron's size, the scaling that the few recordings
comparing synapse counts with synaptic strength favour, or by the square root of its size. Total
synapse count stands in for size, since MaleCNS's tables carry no volumes, and both recipes calibrate
to 1.1 mV per synapse. Both fail. Dividing by size shrinks the runaway 22–37×, to 201 undriven
neurons above 100 Hz, but the activity still outlasts the drive, and now 15 of 20 weight shuffles
drive MN9 as well: the route is no longer specific to the wiring. The square root runs away harder,
with 14,662 neurons above 100 Hz. No recipe tried so far, one weight for every synapse or one scaled
by either measure of size, gives Shiu's MN9 response without a runaway or a loss of specificity.

Two limits apply throughout. The taste-neuron labels are provisional: LB3a as water and LB3b–c as
sugar come from an unreviewed MaleCNS port, and LB1a–d as bitter and LB1e as Ir94e-like from summaries
of the gustatory connectome papers. And Shiu's grooming test (JO-CE neurons drive aBN1, JO-F neurons
don't) can't run here, because MaleCNS has no aBN1 annotation.

## Where it started

brainfly began as a fork of [fly.ai](https://github.com/alextitonis/fly.ai), whose model is still
here as `brainfly.FlyBrain`. It runs each of MaleCNS's 166,700 neurons as the same leaky
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
| Looming is too weak even with a graded eye | LPLC2 +1.2–1.5 Hz, against tens of Hz in real flies | MaleCNS has 3,377 of about 10,650 expected photoreceptors, and 962 of its 1,769 lamina columns get no photoreceptor input. Normalisation dilutes the rest; one gain for every type; a 100 ms membrane. | Fill in the missing input. Done: LPLC2 +4.1–4.8 Hz and the giant fiber +2.4–3.2 Hz, still short of the bar. Next, per-type time constants and resting levels. |
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
| `experiments/motor_readout.py` | With Fly64's settings, does what the fly sees reach its motor neurons? | No. Every neuron rests exactly at threshold, so the network ticks at about 4 Hz whatever the fly sees. |
| `experiments/sweep.py` | Does looming reach the looming detectors through the eye? | No, in every setting tried: histamine from the photoreceptors silences the lamina. |
| `experiments/inject.py` | Past the eye, do the detectors drive the right outputs? | Yes, on the same side only: looming detectors raise the giant fiber by 17–25 Hz, and courtship-tracking LC10a raises the steering neuron DNa02 by 1.4–3.7 Hz. |
| `FlyBrain(sensory_input=False)` | Why do the smell neurons sit at the rate ceiling? | Olfactory receptor neurons get 0.43 of their 0.45 net input from each other. Removing synapses onto sensory neurons ends the runaway. |
| `experiments/flytalk.py` | Can two brains signal to each other through song and hearing? | Yes, but only through loudness, and at 2 ms steps scrambled wiring carries as much (0.87 vs 0.83 bits). |
| `experiments/eyepath.py` | Does a graded retina and lamina let looming through? | With the right signs along the whole pathway, but LPLC2 rises only 1.2–1.5 Hz: a fail against its 3 Hz bar. |
| `experiments/eyepath_filled.py` | With the missing photoreceptor input filled in, does looming reach the escape neuron through the eyes? | Yes, weakly, on a one-dimensional eye: the same side's LPLC2 rises 4.1–4.8 Hz and its giant fiber 2.4–3.2 Hz in three seeds. LC4's 2.7 Hz misses the 3 Hz bar, so the test fails. |
| `experiments/vnc/` | Do commands from the brain reach the motor neurons? | No: under 0.6 Hz in every motor group. Three calibrations failed, and no stimulus of 20 drives a walking command. |

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

Two models share the package:

* **`brainfly.FlyBrain`** is the inherited whole-CNS model: 20 ms steps (2 ms optional), faster than real
  time on a recent CPU or an NVIDIA GPU, with opt-in graded neurons, per-type parameters and an
  imputed retina. It is not validated, and its failures are listed above.
* **`brainfly.shiu.ShiuBrain`** is rung 1: Shiu et al.'s recipe on MaleCNS, in 0.1 ms steps, with many
  trials run in parallel, any neurons silenced, or any synapse matrix (a shuffled one, say) swapped in.

```sh
pip install "brainfly[build] @ git+https://github.com/joshuabradley012/brainfly"
```

`[build]` adds pandas and pyarrow, which read the raw MaleCNS tables that `ShiuBrain` runs on. Its
first run downloads them (~1.1 GB) and caches the synapse counts. `FlyBrain` alone needs neither: the
first `FlyBrain()` fetches a prebuilt copy of its brain files (~260 MB). Add `[gpu]` for CuPy on
an NVIDIA GPU (CUDA 12). Set `FLY_DATA=/some/path` to keep the data somewhere other than `~/fly-data`.

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

Rung 1, a taste of sugar, which runs in about 13 s on an Apple M4 Pro:

```python
from brainfly.shiu import ShiuBrain

brain = ShiuBrain(trials=8)                      # Shiu et al.'s recipe on MaleCNS
sugar = brain.cells(["LB3b", "LB3c"], side="L")  # sugar taste neurons (provisional labels)
mn9 = brain.cells(["MN9"], side="L")             # extends the proboscis

result = brain.run(1.0, drive=[(sugar, 100.0)])  # 1 s of sugar at 100 Hz, 0.1 ms steps
hot = result.rates > 100
hot[sugar] = False
print(f"MN9 {result.rates[mn9].mean():.0f} Hz, {hot.sum():,} other neurons above 100 Hz")
# MN9 53 Hz, 7,504 other neurons above 100 Hz
```

To connect your own task to `FlyBrain`, `brainfly.reservoir` records spike traces from any set of
neurons and fits cross-validated linear readouts on them, without training the brain itself.
[`examples/reservoir.py`](examples/reservoir.py) runs it end to end, and
[`examples/quickstart.ipynb`](examples/quickstart.ipynb) tours the brain in a notebook.

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
  `refractory=0.004` matched the 20 ms brain's resting descending-neuron rate.
* `sensory_input` (default `True`): `False` removes every synapse onto sensory neurons.
* `refractory` (default `0`): seconds a neuron is held at 0 after it spikes.
* `graded` (default none): cell types or superclasses simulated as graded neurons that release
  transmitter continuously, like the real retina and lamina.
* `cell_params`: a time constant, threshold, tonic drive or gain per cell type or superclass.
* `fill_retina` (default `False`): adds an imputed photoreceptor bundle to each of the 962 lamina
  columns MaleCNS lost at the edge of its volume, wired like the median intact column
  (`brainfly/retina.py`). It is imputed, not observed.

`brain.cells([...])` accepts superclass names such as `"descending_neuron"` as well as cell types.

</details>

## What's in the repository

| Path | What it is |
|---|---|
| [`reports/`](reports/) | the research report: what each layer of the fly needs, which models have been validated, why the inherited model fails, and the nine-rung plan |
| [`research_notes/`](research_notes/) | the sourced notes behind the report: senses, neuron biophysics, the nerve cord, muscles and body models, datasets, and this project's experiments |
| `brainfly/brain.py` | `FlyBrain`, the inherited model, on CPU (numba) or NVIDIA GPU (CuPy), one fly or a batch |
| `brainfly/shiu.py` | `ShiuBrain`, rung 1, and the raw signed synapse counts it runs on |
| `brainfly/retina.py` | the photoreceptor input MaleCNS lost at the edge of its volume, imputed from the intact columns |
| `brainfly/build.py`, `data.py` | building the brain files from MaleCNS v1.0, or fetching a prebuilt copy |
| `brainfly/eyes.py`, `reservoir.py` | a visual encoder for `FlyBrain`, and readouts trained on its spikes |
| `experiments/shiu_*.py` | rung 1: the two pre-registered attempts and the runaway follow-up, with results in `.json` next to them |
| `experiments/` (the rest) | the experiments on the inherited model, listed [above](#where-it-started) |
| `examples/` | a notebook tour, and a readout trained end to end |
| `assets/` | the logo and the looming figure, and the scripts that draw them from the data |

<details>
<summary><b>The data, and building it yourself</b></summary>

<br>

There are no trained weights. The "model" is the fly's wiring diagram. `brainfly download` fetches a
prebuilt copy of `FlyBrain`'s files (checked against their sha256); `brainfly build` builds them from
the public MaleCNS v1.0 release, downloading these files into `$FLY_DATA/raw/` and skipping any that are
already there:

| File | Size | What it is | Source |
|---|---|---|---|
| `connectome-weights-male-cns-v1.0-minconf-0.5.feather` | 1.05 GB | every neuron-to-neuron connection, with synapse counts | [MaleCNS bucket](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather) |
| `body-annotations-male-cns-v1.0-minconf-0.5.feather` | 14 MB | cell types, sides, classes, soma positions | [MaleCNS bucket](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather) |
| `body-neurotransmitters-male-cns-v1.0.feather` | 43 MB | predicted neurotransmitter for each neuron | [MaleCNS bucket](https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather) |
| `optic-columns.xlsx` | 0.1 MB | which eye column each photoreceptor belongs to | [flyconnectome/2025malecns](https://github.com/flyconnectome/2025malecns/blob/67767d2233657983993ff6c2be48e836a935863c/supplemental_data/optic-column-type-assignments-v1.0.xlsx) |

To download by hand instead (for example on a slow connection, or with `curl -C -` to resume):

```sh
mkdir -p ~/fly-data/raw && cd ~/fly-data/raw
B=https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome
curl -LO -C - $B/connectome-weights-male-cns-v1.0-minconf-0.5.feather
curl -LO -C - $B/body-annotations-male-cns-v1.0-minconf-0.5.feather
curl -LO -C - $B/body-neurotransmitters-male-cns-v1.0.feather
curl -L -o optic-columns.xlsx https://raw.githubusercontent.com/flyconnectome/2025malecns/67767d2233657983993ff6c2be48e836a935863c/supplemental_data/optic-column-type-assignments-v1.0.xlsx
```

Then `python -m brainfly build` builds the network in about a minute. It writes `weights.npz` (205 MB,
the signed and normalised connection matrix) and `brain.npz` (neuron types, sides, positions, readout
groups, eye layout) into `$FLY_DATA`. Expect exactly **166,700 neurons and 25,582,938 connections**.
The first `ShiuBrain()` adds `counts.npz`, the same connections as raw signed synapse counts.

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
* **The inherited model** comes from [fly.ai](https://github.com/alextitonis/fly.ai) (MIT), whose
  neuron model, weight normalisation and optic-column handling follow
  [Fly64](https://github.com/ornata/fly) by Jessica Paquette.
* **Sources:** what this README says about other people's work comes from the
  [research report](reports/Embodied%20fly%20connectome%20simulation.md), which cites it inline.
* **The logo** is the same data: the cell bodies of the MaleCNS neurons seen from the front, as a
  halftone, with the optic lobes in the red of the eyes they sit behind. The wordmark is set in
  [Newsreader](https://github.com/productiontype/Newsreader) by Production Type (SIL Open Font
  License).

## License

The code in this repository is released under the [MIT License](LICENSE).

The MaleCNS connectome data is **not** in the repository or the package. `brainfly build` downloads it
from its source, and `brainfly download` fetches files derived from it (the normalised weight matrix
and neuron annotations). Both stay under the data's own
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license from FlyEM (HHMI Janelia) and
collaborators.
