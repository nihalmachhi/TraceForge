"""Provider contracts shared by optional integrations."""

from typing import Protocol, TypedDict


class Completion(TypedDict):
    """Normalized provider response fields used by traces."""

    text: str
    model: str
    input_tokens: int
    output_tokens: int


class Provider(Protocol):
    """Minimal synchronous text-generation interface."""

    def complete(self, prompt: str) -> Completion:
        """Generate one response and return normalized token metadata."""
        ...
