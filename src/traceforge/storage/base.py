"""Repository contracts shared by storage implementations."""

from typing import Protocol

from traceforge.core.models import TraceRecord


class TraceRepository(Protocol):
    """Persistence interface used by the tracer and API."""

    def save(self, trace: TraceRecord) -> None:
        """Persist one complete trace atomically."""
        ...

    def list(self, limit: int = 100, offset: int = 0) -> list[dict[str, object]]:
        """Return a page of traces ordered newest first."""
        ...

    def get(self, trace_id: str) -> TraceRecord | None:
        """Return one complete trace, if present."""
        ...

    def clear_demo(self, demo_run: str) -> None:
        """Remove a named synthetic run and its traces."""
        ...

    def close(self) -> None:
        """Release storage resources."""
        ...
