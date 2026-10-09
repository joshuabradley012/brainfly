# Kenyon cell odor responses: the input stage, measured

From Turner, Bazhenov & Laurent 2008, "Olfactory representations by Drosophila mushroom body neurons", J Neurophysiol
99:734-746 ([PDF](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf)), read 2026-10-08.
In vivo whole-cell recordings from 71 Kenyon cells (KCs), each tested with about 10 of 25 odors.

## Odor stimulus
- "1:1,000 effective odor dilution" (1:100 in paraffin oil, 1:10 in the carrier stream), 500 ms pulses, six trials,
  22 s apart; "within the dynamic range of the OSNs (Hallem and Carlson 2006)" and similar to the T-maze protocol.

## Sparseness and spikes
- "A KC was described as responsive if its firing rate crossed a threshold >3.5 SD above baseline at any time in the
  2 s after odor onset."
- "a given odor evoked a spiking response in only 6 ± 5% of the cells. PN response probability, by contrast, was
  59 ± 14%" (n = 37 PNs). Locust, same definition: 11% of KCs, 64% of PNs.
- Tuning: 6 ± 12% of odors evoke a response in a KC; 53 ± 39% in a PN.
- "Average KC response profiles were single-peaked and closely followed the stimulus time course in all KC types."
- α′/β′ KCs "fired 4.9 ± 3.0 spikes during an odor response, significantly more than α/β KCs (2.2 ± 1.2)", and had the
  highest baseline rates and broadest tuning.
- 14 of 71 KCs never fired a spontaneous spike; "every KC had a synaptic response to at least one of the tested
  odors"; subthreshold responses could be depolarizing, hyperpolarizing or both.

## Synaptic input
- Spontaneous EPSPs at 32.6 ± 12.7 /s (n = 27). The smallest spontaneous and miniature (TTX) EPSPs have the same
  amplitude; the spontaneous distribution has a larger tail (multi-quantal or coincident).
- Unitary EPSP for their model: "either the mean (1.4 mV) or the median (1.2 mV) of the experimental distribution".
- Kinetics: EPSP 10-90% rise 2.1 ± 0.5 ms, decay 11.5 ± 5.3 ms (single exponential, 50 EPSPs, 7 cells); EPSC rise
  0.9 ± 0.4 ms, decay 2.8 ± 1.2 ms. "Although EPSP kinetics were fast, the membrane time constant, measured at the soma
  by hyperpolarizing current injection, was very long (>200 ms). These observations suggest that EPSP kinetics are
  determined mostly by synaptic (and possibly, voltage-gated) conductances in the dendrites."
- Resting potential to odor-evoked spike threshold: 21.5 ± 5.6 mV (n = 17); holding potential -57.8 mV.
- PN spontaneous rate 4.6 ± 4.2 /s (n = 37); 7.2 ± 4.2 output terminals per PN in the mushroom body (216 PNs).
- Convergence estimated at about 10 PNs per KC ("a likely range of 5:1 to 15:1").

## Their model
- 1,000 passive conductance-based KCs, each randomly connected to 23 PNs whose recorded benzaldehyde responses drove
  them, with EPSP kinetics fitted to the data and a -36.3 mV threshold. "with connectivity ratios around 10:1, and an
  EPSP amplitude of 1.4 mV, our model matched closely the experimental KC response probability of 6%"; 15:1 was
  needed at 1.2 mV. No synaptic depression is described.

## For brainfly
- In a current-based LIF the membrane time constant sets the EPSP's decay, so 11.5 ms (not the soma's >200 ms) is the
  KC time constant that matches synaptic integration (odor_probe4.py tried 150 ms; odor_probe5.py uses 11.5).
- With MaleCNS's PN-to-KC synapse counts, the mean connection gives 3.3 mV with a 20 ms membrane, against 1.4 mV.
- Gruntman & Turner 2013 (optogenetic PN activation): about 4 of a KC's 5-7 claws must be coactive to spike, summation
  linear to sublinear, the depolarization plateauing about 30 ms into >100 Hz PN firing.
