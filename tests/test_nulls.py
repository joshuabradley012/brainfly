"""brainfly.nulls: each null model scrambles what it should and keeps what it should."""
from __future__ import annotations

import numpy as np
import pytest
from scipy import sparse

from brainfly import nulls


@pytest.fixture
def matrix():
    M = sparse.random(500, 500, density=0.03, random_state=4, format="csr")
    M.data = np.round((M.data - 0.35) * 30)          # signed integer counts, with ties
    M.eliminate_zeros()
    return M


def rows_of(M):
    return [M.data[M.indptr[r]:M.indptr[r + 1]] for r in range(M.shape[0])]


def test_global_shuffle_keeps_the_pattern_and_the_counts(matrix):
    S = nulls.global_shuffle(matrix, np.random.default_rng(1))
    assert np.array_equal(S.indptr, matrix.indptr) and np.array_equal(S.indices, matrix.indices)
    assert np.array_equal(np.sort(S.data), np.sort(matrix.data)) and not np.array_equal(S.data, matrix.data)


def test_within_neuron_keeps_partners_and_each_sign_s_counts(matrix):
    S = nulls.within_neuron(matrix, np.random.default_rng(2))
    assert np.array_equal(S.indptr, matrix.indptr) and np.array_equal(S.indices, matrix.indices)
    changed = 0
    for a, b in zip(rows_of(matrix), rows_of(S)):
        assert np.array_equal(a > 0, b > 0)
        assert np.array_equal(np.sort(a[a > 0]), np.sort(b[b > 0])) and np.array_equal(np.sort(a[a < 0]), np.sort(b[b < 0]))
        changed += not np.array_equal(a, b)
    assert changed > 400


def degrees(M):
    return np.diff(M.tocsr().indptr), np.diff(M.tocsc().indptr)


def sent(M):
    """What each source sends: its counts, sorted, column by column."""
    A = M.tocsc()
    return [np.sort(A.data[A.indptr[c]:A.indptr[c + 1]]) for c in range(A.shape[1])]


def test_degree_preserving_keeps_degrees_and_what_each_source_sends(matrix):
    S = nulls.degree_preserving(matrix, np.random.default_rng(3))
    for a, b in zip(degrees(matrix), degrees(S)):
        assert np.array_equal(a, b)
    assert all(np.array_equal(a, b) for a, b in zip(sent(matrix), sent(S)))
    assert (matrix != S).nnz > 0


def test_class_preserving_also_keeps_each_connection_s_target_class(matrix):
    klass = np.random.default_rng(0).integers(0, 6, matrix.shape[0])
    S = nulls.class_preserving(matrix, klass, np.random.default_rng(4))
    for a, b in zip(degrees(matrix), degrees(S)):
        assert np.array_equal(a, b)
    assert all(np.array_equal(a, b) for a, b in zip(sent(matrix), sent(S)))
    A, B = matrix.tocsc(), S.tocsc()
    for c in range(A.shape[1]):                      # each source sends as much into each class as before
        a, b = A.indices[A.indptr[c]:A.indptr[c + 1]], B.indices[B.indptr[c]:B.indptr[c + 1]]
        assert np.array_equal(np.bincount(klass[a], minlength=6), np.bincount(klass[b], minlength=6))
    assert (matrix != S).nnz > 0.7 * matrix.nnz


def test_the_same_generator_gives_the_same_null(matrix):
    klass = np.arange(matrix.shape[0]) % 4
    for make in (nulls.global_shuffle, nulls.within_neuron, nulls.degree_preserving,
                 lambda M, g: nulls.class_preserving(M, klass, g)):
        a, b = make(matrix, np.random.default_rng(9)), make(matrix, np.random.default_rng(9))
        assert (a != b).nnz == 0
