"""Agent interfaces and deterministic demo agents."""

from typing import Protocol


class Agent(Protocol):
    """Agent interface used by evaluation runners."""

    def run(self, case: dict[str, object], demo_run: str) -> str:
        """Run one case and return the generated answer."""
        ...
