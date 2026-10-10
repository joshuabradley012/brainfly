"""HybridBrain: brainfly's own network model, in which each cell type can be the kind of unit the
biology calls for.

The research report (reports/, "Fly neurons span a hundredfold range of input resistance") found
that fly neurons differ by type. Membrane time constants run from about 2 ms to 30 ms, excitability
falls with size, and many neurons never spike: the optic lobe's columnar cells, the mushroom body's
APL, patchy antennal-lobe local neurons, some nerve-cord interneurons. Shiu et al.'s model gives
every neuron one set of parameters and every synapse one weight, and on MaleCNS it runs away
(experiments/shiu_*.py). HybridBrain keeps Shiu's machinery, the Brian2-exact 0.1 ms kernel of
brainfly.shiu, and lets each cell type differ:

    unit          "spiking", or "graded": integrates the same way but never spikes, releasing
                  transmitter continuously at clip(gain * (v - release_at), 0, max_release) Hz.
                  Each Hz acts on its targets like one spike per second, and no refractory
                  period caps it.
    tau_m         membrane time constant, s (Shiu: 0.020 for every neuron)
    threshold     mV above rest (Shiu: 7)
    reset         mV above rest (Shiu: 0)
    refractory    s (Shiu: 0.0022)
    bias          a constant drive, as the depolarisation it holds a quiet neuron at, mV (Shiu: 0,
                  so every neuron is silent until driven)
    scale         a multiplier on every synapse onto the type (Shiu: 1)
    gain, release_at, max_release    a graded unit's release: Hz per mV, mV above rest, Hz
                  (defaults 6 Hz/mV from the threshold up with no ceiling, which roughly follows
                  a Shiu neuron's firing rate between 60 and 130 Hz; nothing measured sets them)
    noise_rate, noise_kick  background: each neuron of the type gets independent Poisson kicks at
                  noise_rate Hz, each adding noise_kick mV (default none, so the network is
                  silent at rest, as in Shiu's model); a stand-in for the spontaneous activity the
                  model doesn't generate
    depression, recovery    short-term depression of the type's outgoing synapses: the fraction
                  of their strength each spike leaves, recovering toward full with time constant
                  recovery, s (default 1: none; olfactory receptor neurons onto projection neurons:
                  0.78 and 0.893, Nagel, Hong & Wilson 2015). brain.full_strength (one flag per
                  synapse, in brain.weights' order) exempts single synapses, for depression that
                  differs by target
    adaptation, adaptation_tau    spike-frequency adaptation: each spike adds a hyperpolarising
                  current that holds the neuron about `adaptation` mV lower and decays with time
                  constant adaptation_tau, s (default 0: none, as in Shiu's model; 0.2 s)
    tau_slow      the time constant of the type's slow current, s (default 0: the brain's tau_slow)

A spike adds w_syn x (signed synapse count) to a fast current in each target (tau 5 ms, as in
Shiu), or to a slow current (tau_slow, the target type's) along the edges given as slow, t_dly
later. A slow edge's spike adds the same increment as a fast one's, so it carries tau_slow / 5 ms
times the charge (20 times at tau_slow 0.1 s); scale slow counts down to match a fast synapse's
charge. Slow edges depress with their neuron's fast ones unless brain.slow_full (one flag per slow
edge, in brain.slow_weights' order) exempts them. Graded and
external release reach their targets in the same step, without the spikes' t_dly delay. As in
Brian2, input that reaches a refractory neuron is lost, and a spike resets the fast current but
not the slow one. Neurons can also take their output from outside: set_release gives each a
release in Hz, held until the next call, and they never spike. That is how an optic lobe simulated
elsewhere (brainfly.optic.FlyvisNative) drives the brain. With no types and no slow edges
HybridBrain is Shiu's model: tests/test_hybrid.py checks it against Brian2 spike for spike. Its
state persists between calls to advance(), so it can run inside a loop with a body, and advancing
in pieces gives the same spikes as advancing in one go.

    brain = HybridBrain(types={"APL": {"unit": "graded"}})
    rates = brain.run(1.0, drive=[(brain.cells(["LB3b", "LB3c"], side="L"), 100.0)]).rates
"""
from __future__ import annotations

from pathlib import Path

import numba
import numpy as np
from scipy import sparse

from .data import ensure_data
from .shiu import F_POI, T_DLY, T_MBR, T_RFC, TAU, V0, V_RST, V_TH, W_SYN, Result, counts, mcns_types

UNIT = {"spiking": False, "graded": True}
DEFAULTS = {"unit": "spiking", "tau_m": T_MBR, "threshold": V_TH - V0, "reset": V_RST - V0, "refractory": T_RFC,
            "bias": 0.0, "scale": 1.0, "gain": 6.0, "release_at": V_TH - V0, "max_release": np.inf,
            "depression": 1.0, "recovery": 1.0, "noise_rate": 0.0, "noise_kick": 0.0, "adaptation": 0.0,
            "adaptation_tau": 0.2, "tau_slow": 0.0}
MONOAMINES = ("dopamine", "octopamine", "serotonin")


def _approach(tau_in: float, tau_m: float, dt: float) -> float:
    """How much of a current decaying with tau_in reaches v (time constant tau_m) over one step, per
    unit of current at its start: the exact solution of dv/dt = (i - v)/tau_m, di/dt = -i/tau_in."""
    if abs(tau_in - tau_m) < 1e-12:
        return dt / tau_m * np.exp(-dt / tau_m)
    return tau_in / (tau_in - tau_m) * (np.exp(-dt / tau_in) - np.exp(-dt / tau_m))


@numba.njit(inline="always", cache=True)
def _uniform(rng, b):
    """The next number in [0, 1) from trial b's splitmix64 stream, whose state lives in rng[b], so it
    carries over from one call to the next."""
    z = rng[b] + np.uint64(0x9E3779B97F4A7C15)
    rng[b] = z
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return np.float64(z >> np.uint64(11)) * (1.0 / 9007199254740992.0)


@numba.njit(inline="always", cache=True)
def _poisson(rng, b, lam):
    """A Poisson(lam) count from trial b's stream, by inversion (in pieces of at most 500, whose
    sum is Poisson with the whole mean)."""
    k = 0
    while lam > 0.0:
        part = min(lam, 500.0)
        lam -= part
        u = _uniform(rng, b)
        p = np.exp(-part)
        total = p
        i = 0
        while u > total and p > 0.0:
            i += 1
            p *= part / i
            total += p
        k += i
    return k


@numba.njit(cache=True)
def _integrate_uniform(n, ub, xb, adb, tonic, A, B, C, TH, VA, AA, a_xx, external, tonic_on, adapt_on, fired):
    """One step of every neuron's membrane when all share one class's scalars; see _integrate_all."""
    m = 0
    for i in range(n):
        ui = A * ub[i] + B * xb[i] + C
        if tonic_on:
            ui += tonic[i]
        if adapt_on:
            ui -= VA * adb[i]
            adb[i] = AA * adb[i]
        xb[i] = a_xx * xb[i]
        ub[i] = ui
        if ui > TH and not external[i]:
            fired[m] = i
            m += 1
    return m


@numba.njit(cache=True)
def _integrate_all(n, cls, ub, xb, sb, adb, tonic, a_vv, a_vx, a_bias, a_va, a_aa, a_vs, a_xx, a_ss, theta, graded,
                   external, tonic_on, adapt_on, slow, slow_in, fired):
    """One step of every neuron's membrane (the non-uniform case), listing in fired the ones over
    threshold; returns how many. In its own function so the compiler optimises its loop alone. Only neurons
    with slow input (slow_in) carry a slow current; every other neuron's is always 0."""
    m = 0
    for i in range(n):
        c = cls[i]
        ui = a_vv[c] * ub[i] + a_vx[c] * xb[i] + a_bias[c]
        if tonic_on:
            ui += tonic[i]
        if adapt_on:
            ui -= a_va[c] * adb[i]
            adb[i] = a_aa[c] * adb[i]
        xb[i] = a_xx * xb[i]
        if slow and slow_in[i]:
            ui += a_vs[c] * sb[i]
            sb[i] = a_ss[c] * sb[i]
        ub[i] = ui
        if ui > theta[c] and not graded[c] and not external[i]:
            fired[m] = i
            m += 1
    return m


@numba.njit(cache=True)
def _integrate_listed(listed, cls, ub, xb, sb, adb, tonic, a_vv, a_vx, a_bias, a_va, a_aa, a_vs, a_xx, a_ss, theta,
                      graded, tonic_on, adapt_on, slow, slow_in, fired):
    """_integrate_all for only the neurons listed (none of them external)."""
    m = 0
    for q in range(len(listed)):
        i = listed[q]
        c = cls[i]
        ui = a_vv[c] * ub[i] + a_vx[c] * xb[i] + a_bias[c]
        if tonic_on:
            ui += tonic[i]
        if adapt_on:
            ui -= a_va[c] * adb[i]
            adb[i] = a_aa[c] * adb[i]
        xb[i] = a_xx * xb[i]
        if slow and slow_in[i]:
            ui += a_vs[c] * sb[i]
            sb[i] = a_ss[c] * sb[i]
        ub[i] = ui
        if ui > theta[c] and not graded[c]:
            fired[m] = i
            m += 1
    return m


@numba.njit(parallel=True, cache=True)
def _advance(t0, steps, delay, dt, ptr, idx, w, full, sptr, sidx, sw, sfull, stargets, slow_in, gptr, gidx, gw, fptr, fcomp, fw, ftargets, fpend,
             cls, a_vv, a_vx, a_vs, a_bias, tonic, a_va, a_aa, adapt, a_xx, a_ss, theta, reset, rfc, graded, depress, recover, uniform, graded_in,
             g_list, g_gain, g_at, g_max, g_targets,
             u, x, s, ad, until, pend, spend, touched, n_touched, R, RS, rel, rng, left, last,
             drive_idx, drive_p, w_poi, driven, external, internal, E, noise_lambda, noise_kick, members, member_start,
             silenced, counts, timeline, bin_start, bin_steps, rec_pos, rec_out):
    """Advance every trial `steps` steps from global step t0, in Brian2's order as brainfly.shiu does:
    integrate the neurons that aren't refractory, find the spiking ones over threshold, update graded
    release, deliver the input due now (spikes from `delay` steps ago, graded release, Poisson drive)
    to neurons that aren't refractory, then reset the neurons that fired and send their spikes.

    For speed, every neuron is integrated and input goes to every target, and the few refractory
    neurons, kept in a list, are then put back to the state they are frozen in (the reset voltage, no
    fast current, and the slow current they fired with). That is exactly equivalent, and saves reading
    a refractory counter for every neuron on every step. Input waiting in pend[b, slot] is delivered
    through the list of targets that received some, touched[b, slot, :n_touched[b, slot]], unless
    that list overflowed (n_touched > its capacity), when the whole row is scanned. uniform: every
    neuron is spiking and in class 0, and there is no slow current, so the parameters are scalars.
    external neurons never fire; their release is set from outside (HybridBrain.set_release), and
    E[i], the same for every trial, is what it adds to neuron i each second, like graded input R.
    internal lists the neurons that aren't external; in the non-uniform case only they are integrated,
    which gives the same spikes (external neurons never fire, and nothing reads their state).
    g_targets lists the only neurons R or E can reach: the targets of graded and external neurons.

    Per-neuron parameters come from a small table indexed by cls, and tonic[i], when given, adds
    each step's share of neuron i's own bias on top of its class's. ad[b, i], when given, is an
    adaptation current: it pulls v down like the slow current (a_va), decays by a_aa a step, keeps
    decaying through the refractory period and grows by adapt[cls] with each spike. A depressing neuron's spike carries
    the fraction left[b, i] of its full strength, recovered toward 1 (time constant recover, in
    steps) since its last spike, and leaves depress times that; synapses flagged in full[e] always carry full strength. A spike of neuron i also raises each of
    its electrical partners gidx[gptr[i]:gptr[i + 1]] by gw mV at once (no delay, no depression), so they
    can fire on the next step. Its fast synapses fptr[i]:fptr[i + 1] raise their targets ftargets[fcomp[e]] by
    fw[e] mV times the spike's strength (its depression) after fpend.shape[1] steps, through the ring buffer
    fpend[b, slot, target]; like other input, a jump that arrives during the target's refractory period is
    lost. counts[b, i] gains each spike, and
    timeline[b, (bin_start + k) // bin_steps] each step's spikes, if bin_steps > 0; a recorded neuron's spike
    (rec_pos[i] >= 0) also sets rec_out[b, k, rec_pos[i]]. Only the slow synapses' targets (stargets, flagged in
    slow_in) ever carry a slow current, so only they are updated for it. A graded neuron's release reaches its slow
    synapses' targets the same way, through RS[b, i], each Hz like one spike a second into the slow current."""
    trials, n = u.shape
    slow = len(sw) > 0
    ng = len(g_list)
    cap = touched.shape[2]
    tonic_on = len(tonic) > 0
    adapt_on = ad.shape[1] > 0
    fdelay, nf = fpend.shape[1], fpend.shape[2]
    recording = len(rec_pos) > 0
    for b in numba.prange(trials):
        fired = np.empty(n, np.int64)
        # this trial's state in arrays of its own while it runs, which the compiler optimises better
        ub, xb, sb, untilb, Rb = u[b].copy(), x[b].copy(), s[b].copy(), until[b].copy(), R[b].copy()
        RSb = RS[b].copy()
        adb = ad[b].copy()
        tl, nt = touched[b], n_touched[b]
        rlist = np.empty(n, np.int64)          # the refractory neurons, and the slow current each is frozen with
        rs = np.empty(n if slow else 0, np.float32)
        rn = 0
        for i in range(n):
            if untilb[i] > t0:
                rlist[rn] = i
                if slow:
                    rs[rn] = sb[i]
                rn += 1
        A, B, C, TH = a_vv[0], a_vx[0], a_bias[0], theta[0]
        skip_external = len(internal) < n
        VA, AA = a_va[0], a_aa[0]
        for k in range(steps):
            t = t0 + k
            kept = 0                           # drop the neurons whose refractory period ends now
            for q in range(rn):
                j = rlist[q]
                if untilb[j] > t:
                    rlist[kept] = j
                    if slow:
                        rs[kept] = rs[q]
                    kept += 1
            rn = kept
            m = 0
            if uniform:
                m = _integrate_uniform(n, ub, xb, adb, tonic, A, B, C, TH, VA, AA, a_xx, external, tonic_on, adapt_on, fired)
            elif skip_external:                # external neurons never fire and nothing reads their state: skipped
                m = _integrate_listed(internal, cls, ub, xb, sb, adb, tonic, a_vv, a_vx, a_bias, a_va, a_aa, a_vs,
                                      a_xx, a_ss, theta, graded, tonic_on, adapt_on, slow, slow_in, fired)
            else:
                m = _integrate_all(n, cls, ub, xb, sb, adb, tonic, a_vv, a_vx, a_bias, a_va, a_aa, a_vs,
                                   a_xx, a_ss, theta, graded, external, tonic_on, adapt_on, slow, slow_in, fired)
            for q in range(ng):
                i = g_list[q]
                r = 0.0 if silenced[i] else min(max(g_gain[q] * (ub[i] - g_at[q]), 0.0), g_max[q])
                change = r - rel[b, q]
                if change != 0.0:
                    rel[b, q] = r
                    for e in range(ptr[i], ptr[i + 1]):
                        Rb[idx[e]] += w[e] * change
                    if slow:                   # its slow synapses: release into the targets' slow current
                        for e in range(sptr[i], sptr[i + 1]):
                            RSb[sidx[e]] += sw[e] * change
            slot = t % delay
            row = pend[b, slot]
            srow = spend[b, slot]
            if nt[slot] > cap:
                for i in range(n):
                    if row[i] != 0.0:
                        xb[i] += row[i]
                        row[i] = 0.0
            else:
                for q in range(nt[slot]):
                    j = tl[slot, q]
                    if row[j] != 0.0:
                        xb[j] += row[j]
                        row[j] = 0.0
            nt[slot] = 0
            if graded_in:
                for q in range(len(g_targets)):
                    i = g_targets[q]
                    g = Rb[i] + E[i]
                    if g != 0.0:
                        xb[i] += g * dt
            if slow:                           # only the slow synapses' targets can have slow input due
                for q in range(len(stargets)):
                    i = stargets[q]
                    if srow[i] != 0.0:
                        sb[i] += srow[i]
                        srow[i] = 0.0
                    if RSb[i] != 0.0:
                        sb[i] += RSb[i] * dt
            frow = fpend[b, t % fdelay]
            for q in range(nf):                # fast synapses' jumps, due now
                if frow[q] != 0.0:
                    ub[ftargets[q]] += frow[q]
                    frow[q] = 0.0
            for q in range(len(drive_idx)):
                if _uniform(rng, b) < drive_p[q]:
                    ub[drive_idx[q]] += w_poi
            for c in range(len(noise_lambda)):  # background: a Poisson number of kicks per class, spread uniformly
                if noise_lambda[c] > 0.0:
                    size = member_start[c + 1] - member_start[c]
                    for _ in range(_poisson(rng, b, noise_lambda[c])):
                        j = members[member_start[c] + min(int(_uniform(rng, b) * size), size - 1)]
                        ub[j] += noise_kick[c]
            for q in range(rn):                # the refractory neurons back to their frozen state
                j = rlist[q]
                ub[j] = reset[cls[j]]
                xb[j] = 0.0
                if slow:
                    sb[j] = rs[q]
            spikes = 0
            for f in range(m):
                i = fired[f]
                if untilb[i] > t:              # refractory: integrated above only to be put back
                    continue
                spikes += 1
                ub[i] = reset[cls[i]]
                xb[i] = 0.0
                if adapt_on:
                    adb[i] += adapt[cls[i]]
                untilb[i] = t if driven[i] else t + rfc[cls[i]]
                if untilb[i] > t:
                    rlist[rn] = i
                    if slow:
                        rs[rn] = sb[i]
                    rn += 1
                counts[b, i] += 1
                if recording and rec_pos[i] >= 0:
                    rec_out[b, k, rec_pos[i]] = 1
                strength = np.float32(1.0)
                if depress[cls[i]] < 1.0:
                    strength = np.float32(1.0 - (1.0 - left[b, i]) * np.exp(-(t - last[b, i]) / recover[cls[i]]))
                    left[b, i] = strength * depress[cls[i]]
                    last[b, i] = t
                if not silenced[i]:
                    count = nt[slot]
                    for e in range(ptr[i], ptr[i + 1]):
                        j = idx[e]
                        if count <= cap and row[j] == 0.0:
                            if count < cap:
                                tl[slot, count] = j
                            count += 1
                        row[j] += w[e] if full[e] else w[e] * strength
                    nt[slot] = count
                    if slow:
                        for e in range(sptr[i], sptr[i + 1]):
                            srow[sidx[e]] += sw[e] if sfull[e] else sw[e] * strength
                    for e in range(gptr[i], gptr[i + 1]):       # electrical synapses: at once, undepressed
                        ub[gidx[e]] += gw[e]
                    for e in range(fptr[i], fptr[i + 1]):       # fast synapses: fdelay steps from now, depressing
                        frow[fcomp[e]] += fw[e] * strength
            if bin_steps > 0:
                timeline[b, (bin_start + k) // bin_steps] += spikes
        u[b, :] = ub
        x[b, :] = xb
        s[b, :] = sb
        ad[b, :] = adb
        until[b, :] = untilb
        R[b, :] = Rb
        RS[b, :] = RSb


@numba.njit(parallel=True, cache=True)
def _row_sums(indptr, indices, data, x, out):
    """out = M @ x for a CSR matrix, rows in parallel, each summed in order in double precision."""
    for r in numba.prange(len(indptr) - 1):
        total = 0.0
        for e in range(indptr[r], indptr[r + 1]):
            total += data[e] * x[indices[e]]
        out[r] = total


def consensus_transmitters(data: Path | str | None = None) -> np.ndarray:
    """Each neuron's consensus transmitter in MaleCNS ("" where it has none), as brainfly's sign rule
    reads it. Use this rather than predicted_nt: the machine prediction calls 4,058 of the 4,064
    Kenyon cells dopaminergic, while their consensus, like the literature, says acetylcholine."""
    import pyarrow.feather as feather

    from .build import TRANSMITTERS, download_all

    data = ensure_data(data)
    download_all(data / "raw")
    ids = np.load(data / "brain.npz")["ids"]
    nt = feather.read_table(data / "raw" / TRANSMITTERS, columns=["body", "consensus_nt"]).to_pandas()
    return nt.drop_duplicates("body").set_index("body").reindex(ids).consensus_nt.fillna("").astype(str).to_numpy()


def monoaminergic(data: Path | str | None = None) -> np.ndarray:
    """Which neurons MaleCNS's consensus calls dopaminergic, octopaminergic or serotonergic (541)."""
    return np.isin(consensus_transmitters(data), MONOAMINES)


def split(C: sparse.spmatrix, pre: np.ndarray | None = None, post: np.ndarray | None = None):
    """Split a matrix (rows = postsynaptic) into the entries whose presynaptic neuron is in `pre` and
    postsynaptic neuron in `post` (boolean masks; None means all), and the rest: (rest, chosen)."""
    coo = C.tocoo()
    chosen = np.ones(coo.nnz, bool)
    if pre is not None:
        chosen &= pre[coo.col]
    if post is not None:
        chosen &= post[coo.row]
    part = lambda keep: sparse.csr_matrix((coo.data[keep], (coo.row[keep], coo.col[keep])), shape=C.shape)
    return part(~chosen), part(chosen)


class HybridBrain:
    """MaleCNS with per-type units. data: the folder with brain.npz (as ShiuBrain). trials: independent
    copies, each with its own Poisson input, run in parallel. dt: step, s. w_syn: mV per synapse.
    types: {cell type or superclass: {parameter: value}} (see the module docstring), applied in order,
    so list broad classes first; "all" means every neuron. matrix: signed synapse counts, rows = postsynaptic (default
    shiu.counts). slow: signed counts of the edges that act through the slow current instead (not
    also in matrix), with tau_slow its time constant, s. gap: electrical synapses, in mV, rows
    postsynaptic: each spike of a presynaptic neuron raises the postsynaptic one's membrane by that
    much at once, with no synaptic delay and no depression (give one direction only for a rectifying
    junction). fast: synapses fast and strong enough to act as jumps of the membrane, in mV, rows
    postsynaptic (a fly's PSI onto its flight motor neurons, say): each spike raises the target by that much
    times the spike's strength under its neuron's depression, fast_delay s later, and the target can fire on
    the step after. w_poi: mV per Poisson event (default
    Shiu's, 250 x w_syn, which pushes any neuron over threshold). scale: a multiplier per neuron on
    every synapse onto it (e.g. 1 / size), on top of its type's. bias: mV per neuron added to its
    type's bias, for calibrating groups that types can't name (set_bias changes it). sets: {name:
    neuron indices}, named groups that types can use as keys like a cell type, for groups types
    don't name (every cholinergic neuron, say). labels: {"cell_type", "side", "superclass"} arrays
    for a network of your own, given as matrix, instead of MaleCNS."""

    def __init__(self, data: Path | str | None = None, trials: int = 1, dt: float = 1e-4, w_syn: float = W_SYN,
                 types: dict[str, dict] | None = None, matrix: sparse.spmatrix | None = None,
                 slow: sparse.spmatrix | None = None, tau_slow: float = 0.1, w_poi: float | None = None,
                 gap: sparse.spmatrix | None = None, fast: sparse.spmatrix | None = None, fast_delay: float = 3e-4,
                 scale: np.ndarray | None = None, bias: np.ndarray | None = None, seed: int = 0,
                 labels: dict[str, np.ndarray] | None = None, sets: dict[str, np.ndarray] | None = None):
        if labels is None:
            data = ensure_data(data)
            meta = np.load(data / "brain.npz")
            labels = {k: meta[k] for k in ("cell_type", "side", "superclass")} | {"mcns_type": mcns_types(data)}
        elif matrix is None:
            raise ValueError("a network given by labels needs its matrix")
        self.cell_type, self.side, self.superclass = (np.asarray(labels[k]) for k in ("cell_type", "side", "superclass"))
        self.mcns_type = np.asarray(labels.get("mcns_type", self.cell_type))
        self.n = len(self.cell_type)
        self.trials, self.dt = int(trials), float(dt)
        self._fixed_poi = None if w_poi is None else float(w_poi)
        self.types = dict(types or {})
        self.sets = {k: np.asarray(v, np.int64) for k, v in (sets or {}).items()}
        self._tables()
        self.set_bias(bias)
        if scale is not None:
            self.scale = (self.scale * np.asarray(scale, np.float32)).astype(np.float32)
        C = (counts(data) if matrix is None else matrix).tocsc()
        self.ptr, self.idx, self._counts = C.indptr, C.indices, C.data.astype(np.float32)
        self.full_strength = np.zeros(len(self._counts), np.bool_)    # synapses exempt from their neuron's depression
        G = sparse.csc_matrix((self.n, self.n), dtype=np.float32) if gap is None else sparse.csc_matrix(gap, dtype=np.float32)
        self.gptr, self.gidx, self.gap_mv = G.indptr, G.indices, G.data.astype(np.float32)
        F = sparse.csc_matrix((self.n, self.n), dtype=np.float32) if fast is None else sparse.csc_matrix(fast, dtype=np.float32)
        self.fptr, self.fast_mv = F.indptr, F.data.astype(np.float32)
        self.ftargets = np.unique(F.indices).astype(np.int64)            # the fast synapses' targets, compactly
        self.fcomp = np.searchsorted(self.ftargets, F.indices).astype(np.int64)
        self.fdelay = max(1, int(round(fast_delay / self.dt)))
        S = sparse.csc_matrix((self.n, self.n), dtype=np.float32) if slow is None else slow.tocsc()
        self.sptr, self.sidx, self._slow_counts = S.indptr, S.indices, S.data.astype(np.float32)
        self.slow_full = np.zeros(len(self._slow_counts), np.bool_)    # slow synapses exempt from their neuron's depression
        self.stargets = np.unique(S.indices).astype(np.int64)            # the slow synapses' targets
        self.slow_in = np.zeros(self.n, np.bool_)
        self.slow_in[self.stargets] = True
        self.w_syn = w_syn
        self.tau_slow = float(tau_slow)
        self.delay = int(round(T_DLY / self.dt))
        self.external = np.zeros(self.n, np.bool_)       # neurons whose release is set by set_release
        self._external_release = np.zeros(self.n, np.float32)
        self._external_matrix = None                     # rows: every neuron; columns: the external ones
        self.external_input = np.zeros(self.n, np.float32)
        self.reset(seed)

    @property
    def w_syn(self) -> float:
        """mV per synapse; setting it rescales every weight (and the Poisson events, unless w_poi was given)."""
        return self._w_syn

    @w_syn.setter
    def w_syn(self, value: float) -> None:
        if getattr(self, "graded_input", None) is not None and (self.graded_input.any() or self.external_input.any()):
            raise ValueError("set w_syn before any graded or external release, or after reset()")
        self._w_syn = float(value)
        self._external_matrix = None
        self.weights = (self._counts * np.float32(value) * self.scale[self.idx]).astype(np.float32)
        self.slow_weights = (self._slow_counts * np.float32(value) * self.scale[self.sidx]).astype(np.float32)
        self.w_poi = F_POI * self._w_syn if self._fixed_poi is None else self._fixed_poi

    def set_slow(self, slow: sparse.spmatrix | None) -> None:
        """Replace the slow edges (signed counts, rows postsynaptic; None for none), weighted like the others by
        w_syn and the target's scale. The slow currents start again from zero; graded neurons keep releasing, so their
        slow input is rebuilt from their present release along the new edges. Every new slow edge depresses with its
        neuron (brain.slow_full is reset)."""
        S = sparse.csc_matrix((self.n, self.n), dtype=np.float32) if slow is None else sparse.csc_matrix(slow, dtype=np.float32)
        self.sptr, self.sidx, self._slow_counts = S.indptr, S.indices, S.data.astype(np.float32)
        self.stargets = np.unique(S.indices).astype(np.int64)
        self.slow_in = np.zeros(self.n, np.bool_)
        self.slow_in[self.stargets] = True
        self.slow_weights = (self._slow_counts * np.float32(self._w_syn) * self.scale[self.sidx]).astype(np.float32)
        self.slow_full = np.zeros(len(self._slow_counts), np.bool_)
        self._tables_cache = None                        # whether the network is uniform depends on it
        self.s = np.zeros((self.trials, self.n), np.float32)
        self.pending_slow = np.zeros((self.trials, self.delay, self.n if len(self.slow_weights) else 0), np.float32)
        self.slow_graded_input = np.zeros((self.trials, self.n if len(self.slow_weights) else 0), np.float32)
        if len(self.slow_weights):
            for q, i in enumerate(self.graded):
                for e in range(self.sptr[i], self.sptr[i + 1]):
                    self.slow_graded_input[:, self.sidx[e]] += self.slow_weights[e] * self.release[:, q]

    def cells(self, types: list[str], side: str | None = None) -> np.ndarray:
        """Neurons whose cell type (FlyWire's or MaleCNS's own) or superclass is in `types`,
        optionally on one side."""
        named = np.isin(self.cell_type, types) | np.isin(self.mcns_type, types) | np.isin(self.superclass, types)
        return np.flatnonzero(named & (self.side == side) if side else named)

    def _tables(self) -> None:
        """Each neuron's parameters, stored once per distinct combination: self.params lists the
        combinations and self.cls gives each neuron's."""
        keys = [k for k in DEFAULTS if k != "scale"]
        numeric = lambda name, value: float(UNIT[value]) if name == "unit" else float(value)
        values = np.array([[numeric(k, DEFAULTS[k]) for k in keys]] * self.n)
        self.scale = np.ones(self.n, np.float32)
        for key, given in self.types.items():
            unknown = set(given) - set(DEFAULTS)
            if unknown:
                raise ValueError(f"unknown parameters for {key!r}: {sorted(unknown)}; known: {list(DEFAULTS)}")
            if "unit" in given and given["unit"] not in UNIT:
                raise ValueError(f"unit must be one of {list(UNIT)}, not {given['unit']!r}")
            rows = np.arange(self.n) if key == "all" else self.sets[key] if key in self.sets else self.cells([key])
            if not len(rows):
                raise ValueError(f"no neurons of type or superclass {key!r}")
            for name, value in given.items():
                if name == "scale":
                    self.scale[rows] = value
                else:
                    values[rows, keys.index(name)] = numeric(name, value)
        combos, cls = np.unique(values, axis=0, return_inverse=True)
        self.cls = cls.reshape(-1).astype(np.uint8 if len(combos) < 256 else np.int32)   # read every step: keep it small
        self.params = [{k: (("spiking", "graded")[int(v)] if k == "unit" else float(v)) for k, v in zip(keys, row)}
                       for row in combos]
        self.graded = np.flatnonzero(np.array([p["unit"] == "graded" for p in self.params])[self.cls])
        self._members = np.argsort(self.cls, kind="stable").astype(np.int64)   # neurons grouped by class
        self._member_start = np.concatenate([[0], np.cumsum(np.bincount(self.cls, minlength=len(self.params)))]).astype(np.int64)

    def _coefficients(self):
        dt, table = self.dt, self.params
        f32 = lambda key: np.array([key(p) for p in table], np.float32)
        return dict(
            a_vv=f32(lambda p: np.exp(-dt / p["tau_m"])),
            a_vx=f32(lambda p: _approach(TAU, p["tau_m"], dt)),
            a_vs=f32(lambda p: _approach(p["tau_slow"] or self.tau_slow, p["tau_m"], dt)),
            a_ss=f32(lambda p: np.exp(-dt / (p["tau_slow"] or self.tau_slow))),
            a_bias=f32(lambda p: (1 - np.exp(-dt / p["tau_m"])) * p["bias"]),
            a_va=f32(lambda p: _approach(p["adaptation_tau"], p["tau_m"], dt)),
            a_aa=f32(lambda p: np.exp(-dt / p["adaptation_tau"])), adapt=f32(lambda p: p["adaptation"]),
            theta=f32(lambda p: p["threshold"]), reset=f32(lambda p: p["reset"]),
            rfc=np.array([int(round(p["refractory"] / dt)) for p in table], np.int64),
            graded=np.array([UNIT[p["unit"]] for p in table], np.bool_),
            depress=f32(lambda p: p["depression"]), recover=np.array([p["recovery"] / dt for p in table]),
            noise_lambda=np.array([p["noise_rate"] * dt for p in table]) * np.bincount(self.cls, minlength=len(table)),
            noise_kick=f32(lambda p: p["noise_kick"]))

    def _uniform(self) -> bool:
        """Whether every neuron is spiking with the same parameters and there is no slow current."""
        return len(self.params) == 1 and self.params[0]["unit"] == "spiking" and not len(self.slow_weights)

    def set_bias(self, bias: np.ndarray | None) -> None:
        """Each neuron's bias on top of its type's, in mV (None for none), from the next step on;
        the state is kept, so this can move a running network, as calibration does."""
        self.bias = None if bias is None else np.asarray(bias, np.float64).copy()
        self._tonic = np.empty(0, np.float32)
        if self.bias is not None:
            if self.bias.shape != (self.n,):
                raise ValueError(f"bias needs one value per neuron ({self.n}), not shape {self.bias.shape}")
            tau = np.array([p["tau_m"] for p in self.params])[self.cls]
            self._tonic = ((1 - np.exp(-self.dt / tau)) * self.bias).astype(np.float32)   # each step's share

    def reset(self, seed: int = 0) -> None:
        """Every trial back to rest, with fresh Poisson streams from `seed`."""
        shape = (self.trials, self.n)
        self.u, self.x, self.s = np.zeros(shape, np.float32), np.zeros(shape, np.float32), np.zeros(shape, np.float32)
        self.until = np.zeros(shape, np.int64)
        adapting = any(p["adaptation"] != 0 for p in self.params)
        self.ad = np.zeros(shape if adapting else (self.trials, 0), np.float32)
        self.pending = np.zeros((self.trials, self.delay, self.n), np.float32)
        self.fpending = np.zeros((self.trials, self.fdelay, len(self.ftargets)), np.float32)
        slow_n = self.n if len(self.slow_weights) else 0
        self.pending_slow = np.zeros((self.trials, self.delay, slow_n), np.float32)
        cap = max(64, self.n // 8)             # targets remembered per slot before falling back to a full scan
        self.touched = np.zeros((self.trials, self.delay, cap), np.int32)
        self.n_touched = np.zeros((self.trials, self.delay), np.int64)
        self.graded_input = np.zeros(shape if len(self.graded) or self.external.any() else (self.trials, 0), np.float32)
        self.slow_graded_input = np.zeros(shape if len(self.slow_weights) else (self.trials, 0), np.float32)
        self._external_release[:] = 0.0
        self.external_input = np.zeros(self.n, np.float32)
        self.release = np.zeros((self.trials, len(self.graded)), np.float32)
        self.rng = np.random.SeedSequence(seed).generate_state(self.trials, dtype=np.uint64)
        self.driven = np.zeros(self.n, np.bool_)
        depressing = any(p["depression"] < 1 for p in self.params)
        self.left = np.ones(shape if depressing else (self.trials, 0), np.float32)
        self.last = np.full(shape if depressing else (self.trials, 0), -(1 << 40), np.int64)
        self.t = 0

    def advance(self, steps: int, drive=(), silence=(), record=None):
        """Run `steps` steps and return each trial's spike count per neuron, (trials, n). record: neuron
        indices whose spikes to return step by step as well: then (counts, spikes), spikes (trials, steps,
        len(record)) of 0 and 1. drive:
        (neuron indices, rate in Hz) pairs of Poisson input, each event pushing its neuron w_poi mV.
        A neuron given drive has no refractory period from then until reset(), as in Shiu's code,
        where that is a fixed property of the drive's targets. silence: neuron indices whose spikes
        and release go nowhere during these steps."""
        if record is None:
            return self._step(steps, drive, silence)
        spikes = np.zeros((self.trials, int(steps), len(record)), np.int8)
        return self._step(steps, drive, silence, record=np.asarray(record, np.int64), spikes=spikes), spikes

    def _step(self, steps, drive=(), silence=(), timeline=None, bin_start=0, bin_steps=0, record=None, spikes=None) -> np.ndarray:
        """advance(), also adding each step's spikes to timeline[:, (bin_start + k) // bin_steps]."""
        idx = [np.asarray(i, np.int64) for i, _ in drive]
        drive_idx = np.concatenate(idx) if idx else np.empty(0, np.int64)
        drive_p = np.concatenate([np.full(len(i), r * self.dt) for i, (_, r) in zip(idx, drive)]) if idx else np.empty(0)
        self.driven[drive_idx] = True
        silenced = np.zeros(self.n, np.bool_)
        silenced[np.asarray(silence, np.int64)] = True
        k = self._kernel_tables()
        counts = np.zeros((self.trials, self.n), np.int32)
        rec_pos = np.full(self.n if record is not None else 0, -1, np.int64)
        if record is not None:
            rec_pos[record] = np.arange(len(record))
        external_on = bool(self.external_input.any())      # else only graded neurons' targets can get release
        _advance(self.t, int(steps), self.delay, np.float32(self.dt), self.ptr, self.idx, self.weights, self.full_strength,
                 self.sptr, self.sidx, self.slow_weights, self.slow_full, self.stargets, self.slow_in, self.gptr, self.gidx, self.gap_mv,
                 self.fptr, self.fcomp, self.fast_mv, self.ftargets, self.fpending, self.cls, k["a_vv"], k["a_vx"], k["a_vs"], k["a_bias"], self._tonic, k["a_va"], k["a_aa"], k["adapt"],
                 k["a_xx"], k["a_ss"], k["theta"],
                 k["reset"], k["rfc"], k["graded"], k["depress"], k["recover"], k["uniform"],
                 bool(len(self.graded) or external_on), k["g_list"], k["g_gain"], k["g_at"], k["g_max"],
                 self._graded_targets() if external_on else self._graded_only_targets(), self.u, self.x, self.s, self.ad, self.until,
                 self.pending, self.pending_slow, self.touched, self.n_touched, self.graded_input, self.slow_graded_input, self.release,
                 self.rng, self.left, self.last,
                 drive_idx, drive_p, np.float32(self.w_poi), self.driven, self.external, self._internal_neurons(), self.external_input,
                 k["noise_lambda"], k["noise_kick"], self._members, self._member_start, silenced, counts,
                 np.zeros((self.trials, 0), np.int64) if timeline is None else timeline, int(bin_start), int(bin_steps),
                 rec_pos, np.zeros((self.trials, 0, 0), np.int8) if spikes is None else spikes)
        self.t += int(steps)
        return counts

    def _kernel_tables(self) -> dict:
        """The coefficient tables and graded-neuron arrays the kernel reads. They depend only on the types,
        dt and tau_slow, none of which changes after construction, so they are made once."""
        if getattr(self, "_tables_cache", None) is None:
            k = self._coefficients()
            g = [self.params[c] for c in self.cls[self.graded]]
            k.update(g_list=self.graded.astype(np.int64), g_gain=np.array([p["gain"] for p in g], np.float32),
                     g_at=np.array([p["release_at"] for p in g], np.float32), g_max=np.array([p["max_release"] for p in g], np.float32),
                     uniform=self._uniform(), a_xx=np.float32(np.exp(-self.dt / TAU)))
            self._tables_cache = k
        return self._tables_cache

    def _internal_neurons(self) -> np.ndarray:
        """The neurons that aren't external, for the kernel to integrate."""
        if getattr(self, "_internal", None) is None:
            self._internal = np.flatnonzero(~self.external).astype(np.int64)
        return self._internal

    def _graded_only_targets(self) -> np.ndarray:
        """The neurons graded release can reach (all the kernel visits while no external release arrives)."""
        if getattr(self, "_gr_targets", None) is None:
            parts = [self.idx[self.ptr[g]:self.ptr[g + 1]] for g in self.graded]
            self._gr_targets = np.unique(np.concatenate(parts)).astype(np.int64) if parts else np.empty(0, np.int64)
        return self._gr_targets

    def _graded_targets(self) -> np.ndarray:
        """The neurons graded or external release can reach, which are all the kernel visits for it."""
        if getattr(self, "_g_targets", None) is None:
            parts = [self.idx[self.ptr[g]:self.ptr[g + 1]] for g in self.graded]
            if self.external.any():
                parts.append(np.flatnonzero(np.diff(self._external_matrix[1].indptr)))
            self._g_targets = np.unique(np.concatenate(parts)).astype(np.int64) if parts else np.empty(0, np.int64)
        return self._g_targets

    def set_release(self, neurons, hz) -> None:
        """Make these neurons' output external. From now on they never spike (reset() keeps them external,
        releasing nothing until set again), and each
        passes on `hz` (one value per neuron, or one for all) as a change of its release from rest.
        Every Hz acts on its targets like one spike per second, and a negative change takes input
        away. It holds until the next call. This is for an optic lobe simulated elsewhere, like
        brainfly.optic.FlyvisNative. Input to an external neuron can't matter, so external release
        reaches only the other neurons, which also saves most of the work."""
        neurons = np.asarray(neurons, np.int64)
        hz = np.broadcast_to(np.asarray(hz, np.float32), neurons.shape)
        if not self.external[neurons].all():
            self.external[neurons] = True
            self._external_matrix = None
            self._g_targets = None
            self._internal = None
        if self.graded_input.shape[1] == 0:
            self.graded_input = np.zeros((self.trials, self.n), np.float32)
        if self._external_matrix is None:
            sources = np.flatnonzero(self.external)
            col = np.repeat(np.arange(self.n), np.diff(self.ptr))
            keep = self.external[col] & ~self.external[self.idx]
            M = sparse.csr_matrix((self.weights[keep], (self.idx[keep], np.searchsorted(sources, col[keep]))),
                                  shape=(self.n, len(sources)), dtype=np.float32)
            self._external_matrix = (sources, M)
        self._external_release[neurons] = hz
        sources, M = self._external_matrix
        _row_sums(M.indptr, M.indices, M.data, self._external_release[sources], self.external_input)

    def run(self, seconds: float, drive=(), silence=(), tail: float = 0.0, seed: int = 0, bin: float = 0.01) -> Result:
        """From rest, drive neurons for `seconds`, then run `tail` seconds without the drive; the same
        Result as ShiuBrain.run. silence here also cuts every synapse onto the silenced neurons, as
        ShiuBrain's does."""
        self.reset(seed)
        saved = self.weights
        if len(silence):
            cut = np.zeros(self.n, bool)
            cut[np.asarray(silence, np.int64)] = True
            self.weights = np.where(cut[self.idx], np.float32(0), self.weights).astype(np.float32)
        try:
            drive_steps, tail_steps = int(round(seconds / self.dt)), int(round(tail / self.dt))
            bin_steps = max(1, int(round(bin / self.dt)))
            timeline = np.zeros((self.trials, -(-(drive_steps + tail_steps) // bin_steps)), np.int64)
            during = self._step(drive_steps, drive, silence, timeline, 0, bin_steps)
            after = self._step(tail_steps, (), silence, timeline, drive_steps, bin_steps)
        finally:
            self.weights = saved
        rates = during / seconds
        return Result(rates=rates.mean(0), trial_rates=rates,
                      after_rates=after / tail if tail > 0 else np.zeros_like(rates),
                      timeline=timeline / (bin_steps * self.dt), bin=bin_steps * self.dt)
