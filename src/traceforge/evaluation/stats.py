"""Small dependency-free statistics helpers for paired evaluation results."""

import math
import random


def bootstrap_interval(
    values: list[float], confidence: float = 0.95, samples: int = 2000, seed: int = 0
) -> tuple[float, float]:
    """Return a deterministic percentile bootstrap interval around the mean."""
    if not values:
        raise ValueError("values cannot be empty")
    if not 0 < confidence < 1 or samples < 1:
        raise ValueError("confidence must be in (0, 1) and samples must be positive")
    generator = random.Random(seed)
    means = sorted(
        sum(generator.choice(values) for _ in values) / len(values) for _ in range(samples)
    )
    tail = (1 - confidence) / 2
    return means[math.floor(tail * samples)], means[
        min(samples - 1, math.ceil((1 - tail) * samples) - 1)
    ]


def paired_sign_test(before: list[float], after: list[float]) -> float:
    """Return a two-sided exact sign-test p-value for paired differences."""
    if len(before) != len(after):
        raise ValueError("paired samples must have equal lengths")
    differences = [right - left for left, right in zip(before, after, strict=True)]
    positive = sum(value > 0 for value in differences)
    negative = sum(value < 0 for value in differences)
    count = positive + negative
    if not count:
        return 1.0
    tail = sum(math.comb(count, index) for index in range(min(positive, negative) + 1))
    return float(min(1.0, 2 * tail / (2**count)))
