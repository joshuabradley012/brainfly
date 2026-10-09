"""Null models: the connectome with its wiring or its weights scrambled, to test whether a result
depends on them. The research report's ladder climbs from weight shuffles to degree-preserving
rewiring to rewiring that keeps cell classes. Each function takes a signed synapse-count matrix with
rows = postsynaptic neurons and a numpy Generator, and returns a new matrix. The two grouped ones
make a single pass instead of sorting, so a null of the whole connectome (25.6 million connections)
takes well under a second.

    global_shuffle       every connection keeps its place and takes a random connection's count (and sign:
                         signs move between neurons, so it breaks Dale's law)
    within_neuron        each neuron's input counts permuted among its inputs of the same sign; it
                         keeps its partners and its total excitation and inhibition
    degree_preserving    every connection keeps its source and count and takes a random connection's
                         target; each neuron keeps its in- and out-degree, but not its input strength: a
                         neuron whose inputs are strong gets random connections' counts instead (on the
                         raw connectome MN9 L keeps 743-823 of its 3,092 excitatory synapses in three
                         draws), so a result this null abolishes may only have lost its input
    class_preserving     the same, with targets drawn only from connections whose target is in the
                         same class (superclass, say), which keeps more of a neuron's input strength
                         (MN9 L: 2,187-3,618 of 3,092 in three draws)

The experiments of rung 1 (shiu_*.py) keep their own implementations, which draw differently, so that
they reproduce their recorded null networks.
"""
from __future__ import annotations

import numba
import numpy as np
from scipy import sparse


def global_shuffle(C: sparse.spmatrix, rng: np.random.Generator) -> sparse.csr_matrix:
    M = C.tocsr()
    return sparse.csr_matrix((rng.permutation(M.data), M.indices, M.indptr), shape=M.shape)


def degree_preserving(C: sparse.spmatrix, rng: np.random.Generator) -> sparse.csr_matrix:
    M = C.tocsc()                                # columns = sources, indices = targets
    return sparse.csc_matrix((M.data, rng.permutation(M.indices), M.indptr), shape=M.shape).tocsr()


def within_neuron(C: sparse.spmatrix, rng: np.random.Generator) -> sparse.csr_matrix:
    M = C.tocsr()
    data = _within_rows(M.indptr, M.data, int(rng.integers(2**62)))
    return sparse.csr_matrix((data, M.indices.copy(), M.indptr.copy()), shape=M.shape)


def class_preserving(C: sparse.spmatrix, klass: np.ndarray, rng: np.random.Generator) -> sparse.csr_matrix:
    """klass: an integer class per neuron (np.unique(..., return_inverse=True)[1], say)."""
    M = C.tocsc()
    klass = np.asarray(klass, np.int64)
    targets = _within_classes(M.indices.astype(np.int64), klass, int(klass.max()) + 1, int(rng.integers(2**62)))
    return sparse.csc_matrix((M.data, targets, M.indptr), shape=M.shape).tocsr()


@numba.njit(cache=True)
def _within_rows(indptr, data, seed):
    """Each row's positive entries shuffled among themselves, and its negative ones (Fisher-Yates)."""
    np.random.seed(seed)
    out = data.copy()
    longest = 0
    for r in range(len(indptr) - 1):
        longest = max(longest, indptr[r + 1] - indptr[r])
    place = np.empty(longest, np.int64)
    for r in range(len(indptr) - 1):
        for positive in (True, False):
            k = 0
            for e in range(indptr[r], indptr[r + 1]):
                if (out[e] > 0) == positive:
                    place[k] = e
                    k += 1
            for a in range(k - 1, 0, -1):
                j = np.random.randint(0, a + 1)
                out[place[a]], out[place[j]] = out[place[j]], out[place[a]]
    return out


@numba.njit(cache=True)
def _within_classes(targets, klass, n_classes, seed):
    """The targets shuffled among the connections whose targets share a class (Fisher-Yates)."""
    np.random.seed(seed)
    size = np.zeros(n_classes + 1, np.int64)
    for t in targets:
        size[klass[t] + 1] += 1
    start = np.cumsum(size)                          # connections of class c: start[c]:start[c + 1]
    place = np.empty(len(targets), np.int64)
    fill = start[:-1].copy()
    for e in range(len(targets)):
        c = klass[targets[e]]
        place[fill[c]] = e
        fill[c] += 1
    out = targets.copy()
    for c in range(n_classes):
        lo, hi = start[c], start[c + 1]
        for a in range(hi - 1, lo, -1):
            j = lo + np.random.randint(0, a - lo + 1)
            out[place[a]], out[place[j]] = out[place[j]], out[place[a]]
    return out
