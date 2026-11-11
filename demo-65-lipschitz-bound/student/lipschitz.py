"""Spectral-norm Lipschitz bounds for two-by-two linear maps (stdlib only)."""

import math


def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def matmul(A, B):
    rows, mid, cols = len(A), len(B), len(B[0])
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            out[i][j] = sum(A[i][k] * B[k][j] for k in range(mid))
    return out


def frobenius(M):
    return math.sqrt(sum(v * v for row in M for v in row))


def spectral_norm_2x2(M):
    """Largest singular value of a 2x2 real matrix, via eigenvalues of M^T M."""
    MtM = matmul(transpose(M), M)
    a, b = MtM[0][0], MtM[0][1]
    c, d = MtM[1][0], MtM[1][1]
    tr = a + d
    det = a * d - b * c
    disc = max(tr * tr - 4 * det, 0.0)
    lambda_max = (tr + math.sqrt(disc)) / 2.0
    return math.sqrt(max(lambda_max, 0.0))


def bounds(W1, W2):
    s1 = spectral_norm_2x2(W1)
    s2 = spectral_norm_2x2(W2)
    f1 = frobenius(W1)
    f2 = frobenius(W2)
    return {
        "spectral_W1": s1, "spectral_W2": s2, "spectral_product": s1 * s2,
        "frobenius_W1": f1, "frobenius_W2": f2, "frobenius_product": f1 * f2,
    }
