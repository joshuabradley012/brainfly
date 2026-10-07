# Rung 9: dopamine-gated plasticity at Kenyon cell to MBON synapses

Rung 9's first criterion (the report's plan): "80–90% depression after 1 s of odour paired with dopamine". It comes from
Hige, Aso, Modi, Rubin & Turner 2015, "Heterosynaptic plasticity underlies aversive olfactory learning in Drosophila",
Neuron 88:985 ([PMC4674068](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/)). Read 2026-10-07 through the PMC page
(quotes as the page gives them).

## Protocol
- "1-s odor pulses"; the dopaminergic neuron PPL1-γ1pedc driven optogenetically (CsChrimson, split-GAL4 MB320C).
- "Four light pulses (1 ms in duration) were delivered at 2 Hz, starting 0.2 s after CS+ onset."
- A longer protocol: "1-min odor delivery and 120 photostimulation pulses."

## Effect on MBON-γ1pedc (in brainfly's MaleCNS types, MBON11, MBON-γ1pedc>α/β)
- Spikes to the paired odor: "pre-pairing: 118 ± 8.3 spikes, post: 24 ± 7.4, mean ± SEM; n = 7", about 80% depression.
- Synaptic currents: "average reduction in charge transfer was 90 ± 3.7 %".
- Duration: depression persisted "at least 40 min".

## Specificity
- The unpaired odor: "pre: 110 ± 11 spikes, post: 83 ± 14", and "the effect of pairing was significantly different
  between odors". About 25% for the unpaired odor against 80% for the paired one.
- Timing: backward pairing (the dopamine neuron 0.5 s before the odor) gave "no change in odor responses".
- Compartment: activating PPL1-γ2α'1 left MBON-γ1pedc's odor responses "unaltered".
- The α2 compartment needed more: "the 1-s odor-light pairing protocol ... failed to induce any change" there; the
  1-min protocol did.
- Controls: flies without the driver showed no change with the same odor-light pairing.

## Where the change is
- Kenyon cells' responses decreased slightly for both odors, indistinguishably; whole-cell, pairing "did not change
  the spike threshold or the sustained spike rate". So the depression is at the KC to MBON synapses, specific to the
  paired odor's KCs.

## What a model can predict rather than fit
- The paired odor's depression in MBON-γ1pedc (80–90%) is what a plasticity rule's rate would be fitted to.
- The unpaired odor's smaller change depends on how the two odors' KC populations overlap, which follows from the
  real PN to KC wiring: a prediction, given odors as PN (glomerulus) drives.
- The compartment specificity and the timing rule follow from how the rule is written (which DAN gates which
  compartment's synapses; an eligibility window), so they check the implementation, not the connectome.
