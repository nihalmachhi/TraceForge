"""Compare aggregate metrics for two prompt versions."""

from typing import Any


def compare(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, float]:
    """Return candidate-minus-baseline deltas for quality, latency, and cost."""
    fields = {
        "task_success_rate": "task_success_delta",
        "groundedness": "groundedness_delta",
        "retrieval_relevance": "retrieval_relevance_delta",
        "mean_latency_ms": "mean_latency_delta_ms",
        "mean_estimated_cost_usd": "mean_estimated_cost_delta_usd",
    }
    return {
        output: round(float(candidate[key]) - float(baseline[key]), 8)
        for key, output in fields.items()
    }
