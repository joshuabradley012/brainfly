# brainfly: a real fruit fly brain, running on your computer

This is a simulation of the **complete central nervous system of an adult male fruit fly**
(*Drosophila melanogaster*): **166,700 neurons and 25.6 million connections** from the
[MaleCNS v1.0 connectome](https://male-cns.janelia.org), wired exactly as electron microscopy
found them in a real fly.

There is **no training and no learned policy inside the brain**. You connect a task to it at a few
neuron types known from the literature, one side for input (what the fly senses) and one for
output (the commands its brain sends to the body). Everything in between is the connectome.

The goal is a general-purpose "fly reservoir": plug any task into the same frozen brain, read
out what it does, and find out what a real nervous system's wiring is good for.

## How it works

```
task input
  └─> encoder: drives the fly's own sensory / feature-detector neurons
        └─> 166,700-neuron connectome, leaky integrate-and-fire, 50 steps/s (500 with `dt=0.002`)
              └─> descending neurons (the brain's 1,314 output cables to the body)
                    └─> decoder or trained linear readout
                          └─> task output
```

* **Network** (`brainfly/build.py`, `brainfly/brain.py`): every neuron with a MaleCNS superclass
  annotation, and every connection between them. The weight is the synapse count, made negative
  when the presynaptic neuron's predicted transmitter is GABA, glutamate or histamine, then scaled
  so each neuron's inputs add up to 1. Each neuron is a simple leaky integrate-and-fire unit
  (`v ← e^(-dt/τ)·v + gain·W·spikes + tonic + noise`; it spikes and resets at 1). This recipe
  follows [Fly64](https://github.com/ornata/fly). The simulation is multi-threaded with numba.
* **Visual encoder** (`brainfly/eyes.py`): two routes into the brain.
  * *Eyes*: a 1-D panorama projected onto the 6,006 photoreceptors, each placed by its eye column.
  * *Feature detectors*: drive the fly's own visual projection neurons directly, on the side
    where things are:

    | Neuron type | Responds to (in a real fly) |
    |---|---|
    | LPLC2 | looming: something getting bigger as it approaches |
    | LC4 | fast looming, escape |
    | LPLC1 | small approaching objects |
    | LC10a | a moving target the male chases |

* **Outputs**: the brain's descending neurons, including identified command neurons such as
  DNa02 (steering), DNp01 (the giant fiber, escape take-off), DNg100 (forward walking) and
  MDN (backward walking). A task either decodes these by hand or trains a linear readout on all
  of them (reservoir computing).

## What we found

These are small experiments, run on a desktop. They are not peer-reviewed science.

1. **With Fly64's settings, vision does nothing.** Fly64 uses tonic 0.18 and decay e^(-0.2).
   That puts every neuron's resting voltage at 0.18 / (1 − 0.82) ≈ 1.0, exactly the firing
   threshold. The whole network ticks along by itself at about 4 Hz, and the motor neurons fire
   at the same rate whatever the fly is shown (`experiments/motor_readout.py`).
2. **The signal from the photoreceptors dies at the first relay.** Photoreceptors release
   histamine, which is inhibitory, onto lamina neurons. Real lamina neurons use smooth, graded
   signals rather than spikes, which this simple model can't reproduce. In every setting we
   tried, looming stimuli never reached the looming detectors (`experiments/sweep.py`).
3. **Past the eye, the wiring does the right thing on the correct side** (`experiments/inject.py`,
   tonic 0.14 and gain 3.0, 6 noise seeds):

   | Stimulate (left side only) | Result |
   |---|---|
   | LC4 + LPLC2 looming detectors | left giant fiber DNp01 **+17 to +25 spikes/s**; right side unchanged |
   | LC10a courtship-tracking neurons | left DNa02 steering neuron **+1.4 to +3.7 spikes/s**; right side unchanged |

   None of the other readout neurons changed. These are the known looming → escape and
   courtship pursuit → steering pathways, and they come out of the wiring alone.
4. **Smell neurons ran away until sensory neurons stopped receiving synapses.** In the original
   model, olfactory receptor neurons get 0.43 of their 0.45 net input from each other
   (ORN-to-ORN connections). At gain 3.0 that loop pins them near maximum rate, so the
   food-odour projection neurons (DM1/DM2) sat at 50 Hz, the model's ceiling, with or without an
   odour. `FlyBrain(sensory_input=False)` removes every synapse onto sensory neurons, as
   whole-brain spiking models of the fly do. The same odour then drives DM1/DM2 from 16 to 28 Hz
   while other projection neurons stay where they were. The default is unchanged, so every earlier
   result still holds.
5. **Two brains can signal to each other** (`experiments/flytalk.py`).
   Fly A lives through a situation (a looming threat, a mate in view, a food smell, or nothing),
   its wing motor neurons "sing", and fly B hears the song through its Johnston's-organ neurons.
   Three runs, with the tests fixed before running and 50-shuffle permutation nulls:

   | | Run 1: original, 20 ms | Run 2: smell fixed, 20 ms | Run 3: smell fixed, 2 ms |
   |---|---|---|---|
   | song → what happened to the singer | 0.30 bits | 0.63 bits | 0.83 bits |
   | same test, degree-preserving scrambled wiring | 0.01 bits | 0.01 bits | **0.87 bits** |
   | listener reacts to a threat song (vs silence) | 23% vs 17% | 21% vs 14% | **77.5% vs 17.5%** (p < 0.001) |

   Threat is the clear word in every run, and "mate" becomes partly readable at 2 ms. In every
   run the listener's descending neurons carry the singer's situation and stay at chance in
   silence, but the listener only uses loudness: a time-shuffled song works as well. The "real
   wiring matters" test **fails at 2 ms**, where the scrambled brain's song carries as many bits,
   although it groups the situations differently. Food reaches the brain but never the wings,
   and hearing a song never makes a fly sing back.
6. **A graded retina and lamina let the eyes through, weakly** (`experiments/eyepath.py`). Finding 2 has a
   specific cause: photoreceptors inhibit the lamina, and a spiking neuron that is silent at rest
   can't be inhibited any further. `FlyBrain(graded=[...])` simulates chosen cell types as graded
   neurons that release transmitter continuously, so a drop below rest reaches their targets too.
   With the photoreceptors and lamina graded, a dark object approaching on one side moves the whole
   pathway on that side with the real signs: L1 and L2 up, the OFF channel (Tm1, Tm2, T5) up and
   the ON channel (Mi1, T4) down, then LPLC2 and LC4 up (t ≈ 20 to 40 over 6 flies), while the
   other side stays flat. It still **fails its pre-set test**: the looming detectors rise by about
   1.5 Hz on average (the top tenth of LPLC2 by about 5 Hz) against a 3 Hz bar, and the giant
   fiber barely moves. Part of the cause is in the data: two-thirds of the lamina neurons get no
   photoreceptor input in MaleCNS v1.0, which has 32% of the eye's expected R1-6 photoreceptors.

## Use it on your own task

`brainfly/reservoir.py` connects any task to the brain:

```
input -> encoder -> fly brain (frozen) -> trace -> trained readout -> output
```

The brain never trains, on any task: `FlyBrain`'s weights are the connectome, fixed at load
time. Only two things ever get fit:

* **An encoder**, which you write: pick the neuron types your input should drive with
  `brain.cells([...types], side=...)` and pass `(indices, amount)` pairs to
  `brain.step(inject=...)`. `brainfly/eyes.py` is a worked example for visual input;
  the neuron types available are whatever the MaleCNS connectome names (look one up on
  [neuPrint](https://neuprint.janelia.org)).
* **A readout**, which `brainfly.Readout.fit` trains for you: a linear (`kind="ridge"`) or
  logistic (`kind="logistic"`) fit on the top principal components of neural activity, with the
  PCA rank and L2 strength picked by cross-validation.

`brainfly.Trace` collects a decaying spike trace of any neuron population (a cell type, a
`brain.groups[...]` set, or your own index array) step by step; `brainfly.run` steps the
brain over a sequence of encoded inputs and returns the trace stacked over time, so the whole
loop is one call from a notebook:

```python
from brainfly import FlyBrain
from brainfly.reservoir import Trace, Readout, run

brain = FlyBrain(device="auto")
trace = Trace(brain, types=["descending_neuron"])   # or group=..., or idx=your_own_array

def encode(t):
    return [(brain.cells(["LC10a"], side="L"), my_inputs[t])]   # your task's encoder

activity = run(brain, len(my_inputs), encode=encode, trace=trace)
readout = Readout.fit(activity, my_labels, kind="ridge")        # or "logistic" for 0/1 labels
prediction = readout.predict(activity[-1])
readout.save("readout.npz")                                      # Readout.load(...) later
```

`examples/reservoir.py` runs this end to end on a synthetic task (classify and measure the
strength of a left/right stimulus) with no recordings needed:
`python examples/reservoir.py`. Its held-out numbers are printed as they come out, not curated
— on the fixed seed it ships with, the classifier does better than chance and the strength
regression is close to just predicting the average; that is the honest state of a two-line
encoder on an invented task, not a claim about what the connectome can do in general (see
"What's next" for the open question of how much the real wiring helps versus
a random network of the same size).

Batching and the GPU option work the same way they do in `brainfly/brain.py`: `FlyBrain(batch=8)` or
`FlyBrain(device="cuda")` (or `FLY_DEVICE=cuda`); `Trace(..., aggregate="mean")` (the default)
gives one feature vector averaged across the batch, `aggregate="batch"` keeps one per fly.

### Brain options

`FlyBrain` takes these options. The defaults are the model every earlier result used.

* `dt` (default `0.020`): the step length. `tonic` is rescaled so a silent neuron settles at the
  same voltage. At `dt=0.002` the network runs far hotter unless you also set a refractory
  period; `refractory=0.004` matched the 20 ms brain's resting descending-neuron rate with no
  neurons above 100 Hz.
* `sensory_input` (default `True`): `False` removes every synapse onto sensory neurons, which
  fixes the olfactory runaway loop (finding 4).
* `refractory` (default `0`): seconds a neuron is held at 0 after it spikes.
* `graded` (default none): cell types or superclasses simulated as graded (non-spiking) neurons
  that release transmitter continuously, like the real retina and lamina (finding 6).

`brain.cells([...])` accepts superclass names such as `"descending_neuron"` as well as cell types.

### Limitations

* Point neurons with one global set of parameters. There are no dendrites (graded neurons
  only where `graded=` asks for them), no neuromodulators and no plasticity.
* Transmitter sign is a rough rule (GABA, glutamate and histamine inhibitory; everything else
  excitatory). Real effects depend on the receptor.
* The visual front end is a shortcut, like [Eon's embodied fly](https://eon.systems/updates/embodied-brain-emulation).
  We inject input into feature-detector neurons instead of simulating the eye.
* None of this is validated against recordings from real flies. It's a demo, not an emulation.

## Run it

A multi-core CPU helps: one brain step takes about 12–15 ms on 24 threads, and real time needs
under 20 ms.

**Just the brain, as a library** (Python 3.10+):

```sh
pip install "brainfly @ git+https://github.com/joshuabradley012/brainfly"   # add [gpu] for an NVIDIA GPU
brainfly download               # optional: the first FlyBrain() does this itself (~260 MB, once)
brainfly info                   # where the data lives, and whether CUDA works
```

**This repository** (the package plus experiments and examples): install it in editable mode so
the scripts in `experiments/` and `examples/` can import it.

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -e ".[build]"         # pandas/pyarrow for build + experiments; ".[build,gpu]" for CUDA

python -m brainfly download       # prebuilt brain (~260 MB) into ~/fly-data
# or: python -m brainfly build    # download MaleCNS v1.0 (~1.1 GB) and build the network yourself
```

Set `FLY_DATA=/some/path` to store the data somewhere else.

**Quickstart notebook:** [`examples/quickstart.ipynb`](examples/quickstart.ipynb) loads the
brain, stimulates the left looming detectors and shows the left giant fiber fire, maps where
the activity goes, and tests the chase pathway. It needs `pip install matplotlib jupyter`.

```python
from brainfly import FlyBrain
brain = FlyBrain(device="auto")                      # GPU if available, else CPU
brain.stimulate(brain.cells(["LC4", "LPLC2"], side="L"), 0.8)
fired = brain.step()                                 # advance 20 ms; indices of neurons that spiked
```

**GPU:** on an NVIDIA card, `pip install -e ".[gpu]"` and set `FLY_DEVICE=cuda` (or
pass `device="cuda"`). The whole connectome fits in about 210 MB of
GPU memory. On an RTX 4060 laptop GPU a step takes **1.4 ms, against 8.9 ms on a 24-thread CPU**.
Both devices run the same model and give the same results. Only the random noise differs, so
individual spikes differ between them.

**Many flies at once:** `FlyBrain(batch=8)` runs 8 independent copies of the brain with the
same wiring, each with its own voltages and noise. On a GPU they share one sparse multiply, at
about 1.2 ms per fly per step. Inputs can be the same for every fly or differ per fly, so several
encoders can run side by side.

**Experiments:** `python experiments/motor_readout.py`, `python experiments/sweep.py`,
`python experiments/inject.py`, `python experiments/eyepath.py`, `python experiments/flytalk.py --help`.

### Getting the data (the "model")

There are no trained weights. The "model" is the fly's wiring diagram. `brainfly download` fetches
a prebuilt copy (checked against its sha256); `brainfly build` (needs `pip install "brainfly[build]"`) builds the same files from the public MaleCNS v1.0 release. It downloads these files into
`$FLY_DATA/raw/` and skips any that are already there. An interrupted download starts over on
the next run:

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

Then `python -m brainfly build` builds the network in about a minute. It writes
`weights.npz` (205 MB, the signed and normalized connection matrix) and `brain.npz` (neuron
types, sides, positions, readout groups, eye layout) into `$FLY_DATA`. Expect exactly
**166,700 neurons and 25,582,938 connections**. If you get different numbers, the data changed.

**Other ways to explore the same data**, without downloading anything:

* [neuPrint](https://neuprint.janelia.org) (dataset `male-cns:v1.0`): look up any neuron's inputs and
  outputs in the browser, for example `DNp01`, the giant fiber. Its top inputs are LC4 and LPLC2.
  For code, use `pip install neuprint-python` with an API token from your neuPrint account page.
* The [MaleCNS site](https://male-cns.janelia.org): cell type and dimorphism explorers, 3D viewers,
  and the full download list (synapse positions, skeletons, EM images; far larger and not needed
  here).

## Files

| File | What it does |
|---|---|
| `brainfly/` | the package (`pyproject.toml`); `brainfly download/build/info` is its command line |
| `brainfly/data.py` | where the brain files live (`$FLY_DATA`), and downloading the prebuilt copy |
| `brainfly/build.py` | downloads MaleCNS v1.0 and builds the weight matrix, readout groups, eye layout and neuron positions |
| `brainfly/brain.py` | integrate-and-fire simulation (with optional graded neurons): CPU (numba) or NVIDIA GPU (CuPy), one fly or a batch |
| `brainfly/eyes.py` | photoreceptor rendering plus the looming/chase feature-detector input, with tunable encoder parameters (`ENCODER`) |
| `brainfly/reservoir.py` | generic reservoir readout: spike trace of any neuron population, PCA + linear/logistic readout, cross-validated |
| `examples/reservoir.py` | the module above, end to end, on a synthetic task |
| `examples/quickstart.ipynb` | notebook tour: load the brain, trigger the giant fiber, follow the activity |
| `experiments/motor_readout.py`, `sweep.py`, `inject.py` | findings 1–3 |
| `experiments/eyepath.py` | graded retina and lamina: does looming reach the looming detectors through the eyes (pre-set criteria, results in `eyepath.json`) |
| `experiments/flytalk.py` | the talking-flies experiment: two brains coupled through wing song and hearing, a scrambled-wiring control, permutation tests (`pilot`, `run`, `report`, `followup`); results go to `experiments/<out>/` |
| `experiments/vnc/` | can the ventral nerve cord relay descending commands to motor neurons: `probe.py` (which motor groups answer which stimulus), `dnscreen.py` (all descending neurons), `vnc.py`, `vnc2.py`, `vnc3.py` (calibration; all failed their pre-set criteria) |
| `research_notes/` | working notes |

## What's next

* Encoders (mapping images, sound, odour-like patterns, sensor readings onto neuron groups) are
  still written per task; `brainfly/reservoir.py` handles the readout side.
* A benchmark: does the real wiring beat randomly rewired copies of itself on the same tasks?
  The talking-flies control is the first data point, and it points both ways: scrambled wiring
  carries nothing at 20 ms and as much as the real brain at 2 ms.
* Getting the eyes through: graded photoreceptors and lamina (finding 6) move the looming pathway
  with the right signs but not yet enough to pass.
* Descending commands don't reach the motor neurons through the VNC (`experiments/vnc/`, three
  calibration attempts, all failed their pre-set criteria).
* Learning inside the brain through the mushroom body's dopamine rule, the way real flies learn.

## Credits

* **Connectome:** MaleCNS v1.0 by FlyEM (HHMI Janelia), the University of Cambridge, the MRC
  Laboratory of Molecular Biology and Google Research. Data used under
  [CC BY 4.0](https://male-cns.janelia.org/download/).
* **[Fly64](https://github.com/ornata/fly)** by Jessica Paquette, who got the MaleCNS brain
  to play Super Mario 64. The neuron model, weight normalization and optic-column handling here
  are adapted from it.
* **[Eon Systems](https://eon.systems/updates/embodied-brain-emulation)**, for the idea of
  feeding a visual front end into an embodied connectome.
* Originally forked from [alextitonis/fly.ai](https://github.com/alextitonis/fly.ai) (MIT).

## References

1. Berg, S. et al. (2026). Sexual dimorphism in the complete connectome of the *Drosophila* male central nervous system. *Cell*. Data: [male-cns.janelia.org](https://male-cns.janelia.org)
2. Google Research (2026). [A connectomics milestone: mapping the complete male fruit fly brain](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/)
3. flyconnectome/2025malecns: [optic column type assignments v1.0](https://github.com/flyconnectome/2025malecns)
4. Plaza, S. M. et al. (2022). neuPrint: an open access tool for EM connectomics. *Frontiers in Neuroinformatics* 16.
5. Dorkenwald, S. et al. (2024). Neuronal wiring diagram of an adult brain. *Nature* 634.
6. Shiu, P. K. et al. (2024). A *Drosophila* computational brain model reveals sensorimotor processing. *Nature* 634.
7. Wang-Chen, S. et al. (2024). NeuroMechFly v2: simulating embodied sensorimotor control in adult *Drosophila*. *Nature Methods* 21, 2353–2362.
8. von Reyn, C. R. et al. (2014). A spike-timing mechanism for action selection. *Nature Neuroscience* 17, 962–970.
9. Ache, J. M. et al. (2019). Neural basis for looming size and velocity encoding in the *Drosophila* giant fiber escape pathway. *Current Biology* 29, 1073–1081.
10. Ribeiro, I. M. A. et al. (2018). Visual projection neurons mediating directed courtship in *Drosophila*. *Cell* 174, 607–621.
11. Rayshubskiy, A. et al. (2020). Neural control of steering in walking *Drosophila*. *bioRxiv*.
12. Bidaye, S. S. et al. (2014). Neuronal control of *Drosophila* walking direction. *Science* 344, 97–101.
13. von Philipsborn, A. C. et al. (2011). Neuronal control of *Drosophila* courtship song. *Neuron* 69, 509–522.
14. Paquette, J. (2026). [Fly64: a fly brain model plays Super Mario 64](https://github.com/ornata/fly).
15. Eon Systems (2026). [How the Eon team produced a virtual embodied fly](https://eon.systems/updates/embodied-brain-emulation).

If you use the connectome data, cite reference 1 and follow the
[MaleCNS attribution terms](https://male-cns.janelia.org/download/).

## License

The code in this repository is released under the [MIT License](LICENSE).

The MaleCNS connectome data is **not** in the repository or the pip package. `brainfly build`
downloads it from its source; `brainfly download` fetches files derived from it (the normalized
weight matrix and neuron annotations). Both stay under the data's own [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license from
FlyEM (HHMI Janelia) and collaborators.
