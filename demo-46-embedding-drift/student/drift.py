"""Cosine shift between two embedding vectors (stdlib only).

An embedding swap moves every artefact at once. The shift reported here is
1 - cosine(baseline, replacement). A frozen headline from the simulated
study is included so the toy can be compared with that number; the toy
does not rerun the study.
"""

import math


def cosine(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("vectors must be the same non-empty length")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        raise ValueError("zero vector")
    return dot / (na * nb)


def shift(a, b):
    return 1.0 - cosine(a, b)
