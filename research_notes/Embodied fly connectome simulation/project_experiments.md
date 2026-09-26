# This project's own experiments (brainfly, unpublished)

These are results from the brainfly codebase itself, not from the literature. They show where the
project's model stands today, so the report's roadmap can start from it. None are peer-reviewed.

## The model today

- Full MaleCNS v1.0 CNS: 166,700 neurons, 25,582,938 connections (neuron pairs), including 89,403
  optic lobe intrinsic, 13,161 VNC intrinsic, 708 VNC motor and 1,314 descending neurons.
- Identical leaky integrate-and-fire units following Fly64 (ornata/fly): tau 100 ms, threshold 1, reset 0,
  20 ms steps (2 ms optional), tonic 0.14 per step, global synaptic gain 3.0, Poisson noise kicks.
- Weights = synapse count, negative if the presynaptic transmitter is GABA, glutamate or histamine, with
  each neuron's inputs normalised so their absolute values sum to 1.
- As of 2026-09-25 the package also supports (off by default, bit-for-bit identical to the original when unused):
  - `cell_params`: tau, threshold, tonic and gain per cell type or superclass.
  - `graded`: chosen cell types simulated as graded (non-spiking) neurons. They integrate the same way
    but never spike, and pass on the change in transmitter release from rest:
    out = clip(k * (v - v_rest), -b, 1 - b), in units of one spike per step.

## Results so far

1. **Eye path, original model (experiments/eyepath.py reference run; the original sweep.py has since been retired).** A dark object looming on one side
   changes photoreceptor firing (-7 Hz) but nothing past the lamina (L1 +0.1 Hz, L2 0; LC4, LPLC2, DNp01
   all 0.0 Hz). Photoreceptors inhibit L1-L3 via histamine; a spiking neuron silent at rest can't be
   inhibited further.

2. **Eye path with a graded retina and lamina (experiments/eyepath.py, 2026-09-25).**
   - Pre-registered test FAILED: no setting raised the population mean of LC4/LPLC2 by the required
     3 Hz.
   - What did happen: with photoreceptors and lamina graded (graded_gain 0.15, resting release 0.3),
     the looming signal crosses the lamina with the correct sign and splits correctly. L1 went +3.1 Hz-eq
     and L2 +1.5. The OFF channel rose (Tm1 +0.5, Tm2 +1.0, T5 +0.9 Hz) and the ON channel fell
     (Mi1, T4), which is correct for a dark object. LPLC2 rose +1.2 to +1.5 Hz (t 21-25, 6 flies) and
     LC4 +0.4 to +0.8 Hz (t 29-40), on the stimulated side only (near-far difference t 19-39). The giant
     fiber DNp01 rose only +0.3 Hz.
   - Making the whole optic lobe graded (89k neurons) gave similar sizes. Higher graded gain pinned about
     half of the graded neurons at their release limits.
   - Post hoc: the response is retinotopically concentrated. The top 10% of left LPLC2 rose +4.7 Hz
     (max +5.6); the top 10% of T5 rose +6.2 Hz (max +11). Real LPLC2/LC4 looming responses are tens of Hz.
   - The pre-registered REST criterion "mean rate of all spiking neurons <= 5 Hz" was flawed for the
     whole-optic-lobe set. It changes the denominator: the non-optic neurons already average 8.35 Hz in the
     original model and stayed at 8.35 Hz. The flaw did not change the verdict.

3. **Data limitation found (2026-09-25).** In MaleCNS v1.0 only 3,377 R1-6 photoreceptors are present,
   about 32% of the ~10,650 expected for ~888 columns per eye. 66% of left L1/L2/L3 neurons receive no
   photoreceptor input at all, and only 14% have 5 or more of their 6 expected R1-6 partners. R1-6 make up
   only 16% (L1), 11% (L2) and 7% (L3) of lamina neurons' normalised input. So roughly a third of the eye
   feeds the model. Candidate fix: synthesise the missing R1-6 -> lamina inputs from the regular
   neural-superposition wiring.

4. **Skipping the eye (experiments/inject.py).** Driving LC4+LPLC2 directly on one side raises the same-side giant
   fiber DNp01 by +17 to +25 Hz. Driving LC10a raises the same-side steering neuron DNa02 by +1.4 to
   +3.7 Hz. The other side and other readouts are unchanged.

5. **Nerve cord relay (since reproduced by experiments/vnc/relay.py; the original probe.py, vnc.py, vnc2.py and vnc3.py have been retired).** Driving command neurons (DNg100,
   DNa02, DNp01, MDN) at ~25 Hz moves no motor neuron group (< 0.6 Hz). Raising VNC tonic drive and gain,
   or amplifying only the DN -> premotor and premotor -> MN synapses, failed all pre-registered criteria
   (REST, COMMAND, DISTINCT, LATERAL) in every setting.

6. **Two brains signalling (a two-fly song test, since removed).** A song carried 0.3-0.83 bits about the singer's situation. At
   2 ms steps a degree-preserving scrambled wiring carried as many bits (0.87), so the "real wiring
   matters" test failed at 2 ms.

7. **Resting activity.** In the original model with a blank bright field, central brain intrinsic neurons
   average about 12 Hz and central-brain sensory neurons about 24 Hz: olfactory receptor neurons excite
   each other into a runaway loop unless `sensory_input=False`.
