"""Open-set nearest-class-mean rejection (stdlib only)."""

import math
from collections import defaultdict


def _dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def class_means(train):
    buckets = defaultdict(list)
    for row in train:
        buckets[row["label"]].append(row["vec"])
    means = {}
    for label, vecs in buckets.items():
        dim = len(vecs[0])
        means[label] = [sum(v[i] for v in vecs) / len(vecs) for i in range(dim)]
    return means


def predict_ncm(vec, means, threshold):
    nearest = None
    best = None
    for label, mean in means.items():
        dist = _dist(vec, mean)
        if best is None or dist < best:
            best = dist
            nearest = label
    if best is None:
        return {"label": "unknown", "distance": None, "rejected": True}
    rejected = best > threshold
    return {"label": "unknown" if rejected else nearest, "nearest": nearest, "distance": best, "rejected": rejected}


def predict_forced_nn(vec, train):
    nearest = None
    best = None
    for row in train:
        dist = _dist(vec, row["vec"])
        if best is None or dist < best:
            best = dist
            nearest = row["label"]
    return {"label": nearest, "distance": best, "rejected": False}
