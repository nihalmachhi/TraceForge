"""Single source of evaluation gate thresholds."""

from typing import Any

from traceforge.config import GATE_THRESHOLDS


def gate(
    report: dict[str, Any],
    max_task_drop: float | None = None,
    max_groundedness_drop: float | None = None,
) -> dict[str, Any]:
    """Fail when the configured task or groundedness regression limit is exceeded."""
    task_limit = GATE_THRESHOLDS["max_task_drop"] if max_task_drop is None else max_task_drop
    grounding_limit = (
        GATE_THRESHOLDS["max_groundedness_drop"]
        if max_groundedness_drop is None
        else max_groundedness_drop
    )
    comparison = report["comparison"]
    failures = []
    if comparison["task_success_delta"] < -task_limit:
        failures.append("task_success_regression")
    if comparison["groundedness_delta"] < -grounding_limit:
        failures.append("groundedness_regression")
    return {
        "passed": not failures,
        "failures": failures,
        "thresholds": {
            "max_task_drop": task_limit,
            "max_groundedness_drop": grounding_limit,
        },
    }
