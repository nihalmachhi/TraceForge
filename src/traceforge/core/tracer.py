"""Context-manager SDK with context-local nested parent spans."""

import time
import uuid
from contextvars import Token
from datetime import UTC, datetime
from types import TracebackType
from typing import Literal, cast

from traceforge.core.context import ACTIVE_SPAN
from traceforge.core.models import SpanRecord, TraceRecord
from traceforge.core.pricing import estimate_cost
from traceforge.privacy.redactor import redact
from traceforge.storage.base import TraceRepository


def utcnow() -> str:
    """Return the current UTC time in sortable ISO-8601 form."""
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class Span:
    """One timed child operation in a trace."""

    def __init__(
        self,
        trace: "Trace",
        name: str,
        kind: str,
        input_data: object | None,
        attributes: dict[str, object] | None,
        model: str | None,
        prompt_version: str | None,
        input_tokens: int,
        output_tokens: int,
    ) -> None:
        parent = ACTIVE_SPAN.get()
        if parent is not None and parent["trace_id"] != trace.ident:
            parent = None
        self.trace = trace
        self.record: SpanRecord = {
            "span_id": uuid.uuid4().hex,
            "trace_id": trace.ident,
            "parent_span_id": parent["span_id"] if parent else None,
            "name": name,
            "kind": kind,
            "started_at": utcnow(),
            "duration_ms": 0.0,
            "status": "running",
            "attributes": attributes or {},
            "input": input_data,
            "output": None,
            "error": None,
            "model": model,
            "prompt_version": prompt_version,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": estimate_cost(input_tokens, output_tokens),
        }
        self.started = time.perf_counter()
        self.token: Token[SpanRecord | None] | None = None

    def __enter__(self) -> SpanRecord:
        """Activate this span and return its mutable record."""
        self.token = ACTIVE_SPAN.set(self.record)
        return self.record

    def __exit__(
        self,
        error_type: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        """Finalize, redact once, and attach this span to its trace."""
        self.record["duration_ms"] = round((time.perf_counter() - self.started) * 1000, 3)
        self.record["status"] = "error" if error is not None else "ok"
        if error is not None:
            self.record["error"] = str(error)
        if self.token is not None:
            ACTIVE_SPAN.reset(self.token)
        self.trace.spans.append(self.record)
        return False


class Trace:
    """A trace context that stores a root span and all nested operations."""

    def __init__(self, repository: TraceRepository, name: str, metadata: dict[str, object]) -> None:
        self.repository = repository
        self.name = name
        self.metadata = metadata
        self.ident = uuid.uuid4().hex
        self.started_at = utcnow()
        self.started = time.perf_counter()
        self.spans: list[SpanRecord] = []
        self.root: SpanRecord = {
            "span_id": self.ident,
            "trace_id": self.ident,
            "parent_span_id": None,
            "name": name,
            "kind": "trace",
            "started_at": self.started_at,
            "duration_ms": 0.0,
            "status": "running",
            "attributes": {},
            "input": None,
            "output": None,
            "error": None,
            "model": None,
            "prompt_version": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0.0,
        }
        self.token: Token[SpanRecord | None] | None = None

    def __enter__(self) -> "Trace":
        """Set the root as the active span for this context."""
        self.token = ACTIVE_SPAN.set(self.root)
        return self

    def span(
        self,
        name: str,
        kind: str = "custom",
        input: object | None = None,
        attributes: dict[str, object] | None = None,
        model: str | None = None,
        prompt: str | None = None,
        in_tokens: int = 0,
        out_tokens: int = 0,
    ) -> Span:
        """Create a child span using the existing demo SDK argument names."""
        return Span(self, name, kind, input, attributes, model, prompt, in_tokens, out_tokens)

    def __exit__(
        self,
        error_type: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        """Finalize and persist this trace without suppressing user errors."""
        self.root["duration_ms"] = round((time.perf_counter() - self.started) * 1000, 3)
        self.root["status"] = "error" if error is not None else "ok"
        if error is not None:
            self.root["error"] = str(error)
        if self.token is not None:
            ACTIVE_SPAN.reset(self.token)
        record: TraceRecord = {
            "trace_id": self.ident,
            "name": self.name,
            "started_at": self.started_at,
            "ended_at": utcnow(),
            "status": self.root["status"],
            "metadata": self.metadata,
            "spans": [self.root, *self.spans],
        }
        self.repository.save(cast(TraceRecord, redact(record)))
        return False


class TraceForge:
    """Public synchronous tracing client."""

    def __init__(self, repository: TraceRepository) -> None:
        self.repository = repository

    def trace(self, name: str, metadata: dict[str, object] | None = None) -> Trace:
        """Create a trace context with optional metadata."""
        return Trace(self.repository, name, metadata or {})
