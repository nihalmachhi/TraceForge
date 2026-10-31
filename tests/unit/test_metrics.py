from traceforge.core.models import SpanRecord, TraceRecord
from traceforge.evaluation.metrics import score


def test_latency_uses_root_span_only() -> None:
    root: SpanRecord = {
        "span_id": "t",
        "trace_id": "t",
        "parent_span_id": None,
        "name": "root",
        "kind": "trace",
        "started_at": "now",
        "duration_ms": 10.0,
        "status": "ok",
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
    child = {
        **root,
        "span_id": "c",
        "parent_span_id": "t",
        "kind": "llm",
        "duration_ms": 8.0,
        "output": {"answer": "mesh evidence"},
    }
    trace: TraceRecord = {
        "trace_id": "t",
        "name": "test",
        "started_at": "now",
        "ended_at": "now",
        "status": "ok",
        "metadata": {},
        "spans": [root, child],
    }
    case = {"case_id": "one", "required_keywords": [], "retrieval_keywords": []}
    assert score(case, trace)["latency_ms"] == 10.0
