#!/usr/bin/env python3
"""Meta-regression helpers for Demo 35.

Scale bins: small means params_B below 10, large means 10 and above.
Lesson: per-benchmark means differ widely while per-scale means match.
"""


def mean(values: list) -> float:
    """Return the arithmetic mean of a non-empty list."""
    return sum(values) / len(values)


def group_means(rows: list) -> dict:
    """Return per-benchmark and per-scale means plus their gaps."""
    bench_a = [r["unsafe_rate"] for r in rows if r["benchmark"] == "A"]
    bench_b = [r["unsafe_rate"] for r in rows if r["benchmark"] == "B"]
    small = [r["unsafe_rate"] for r in rows if r["params_B"] < 10]
    large = [r["unsafe_rate"] for r in rows if r["params_B"] >= 10]
    mean_a = mean(bench_a)
    mean_b = mean(bench_b)
    mean_small = mean(small)
    mean_large = mean(large)
    return {
        "mean_A": mean_a,
        "mean_B": mean_b,
        "bench_gap": abs(mean_a - mean_b),
        "mean_small": mean_small,
        "mean_large": mean_large,
        "scale_gap": abs(mean_small - mean_large),
        "n_A": len(bench_a),
        "n_B": len(bench_b),
        "n_small": len(small),
        "n_large": len(large),
    }
