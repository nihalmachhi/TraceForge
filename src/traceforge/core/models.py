"""Types shared by the tracer, storage, and API layers."""

from typing import NotRequired, TypedDict


class SpanRecord(TypedDict):
    span_id: str
    trace_id: str
    parent_span_id: str | None
    name: str
    kind: str
    started_at: str
    duration_ms: float
    status: str
    attributes: dict[str, object]
    input: object | None
    output: object | None
    error: str | None
    model: str | None
    prompt_version: str | None
    input_tokens: int
    output_tokens: int
    cost_usd: float


class TraceRecord(TypedDict):
    trace_id: str
    name: str
    started_at: str
    ended_at: str
    status: str
    metadata: dict[str, object]
    spans: list[SpanRecord]


class EvaluationResult(TypedDict):
    case_id: str
    trace_id: str
    prompt_version: str | None
    task_success: bool
    missing_keywords: list[str]
    groundedness: float
    retrieval_relevance: float
    tool_success: bool
    answer: str
    latency_ms: float
    estimated_cost_usd: float
    extras: NotRequired[dict[str, object]]
