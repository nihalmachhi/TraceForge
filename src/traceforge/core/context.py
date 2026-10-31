"""Context-local active span tracking."""

from contextvars import ContextVar

from traceforge.core.models import SpanRecord

ACTIVE_SPAN: ContextVar[SpanRecord | None] = ContextVar("traceforge_active_span", default=None)
