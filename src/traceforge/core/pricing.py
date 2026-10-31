"""Illustrative sample pricing calculations."""

from traceforge.config import RATE_CARD


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Return estimated USD from the project's explicitly illustrative rate card."""
    return round(
        (input_tokens * RATE_CARD["input"] + output_tokens * RATE_CARD["output"]) / 1_000_000,
        8,
    )
