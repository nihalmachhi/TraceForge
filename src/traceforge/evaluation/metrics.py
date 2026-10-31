"""Deterministic evaluation metrics over trace evidence."""

import re
from typing import Any, cast

from traceforge.core.models import EvaluationResult, TraceRecord

STOP_WORDS = {"the", "a", "an", "is", "are", "to", "of", "and", "in", "for", "you", "your", "can"}


def words(value: str) -> set[str]:
    """Return normalized content words for deterministic overlap scoring."""
    return {
        word
        for word in re.findall(r"[a-z0-9]+", value.lower())
        if len(word) > 2 and word not in STOP_WORDS
    }


def normalize(value: str) -> str:
    """Normalize a phrase for stable substring comparison."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", value.lower())).strip()


def score(case: dict[str, Any], trace: TraceRecord) -> EvaluationResult:
    """Score one trace against one fixed fixture case."""
    spans = trace["spans"]
    root = next((span for span in spans if span["kind"] == "trace"), spans[0])
    llm = next((span for span in spans if span["kind"] == "llm"), None)
    retrieval = next((span for span in spans if span["kind"] == "retrieval"), None)
    tools = [span for span in spans if span["kind"] == "tool"]
    output = llm.get("output") or {} if llm else {}
    output = cast(dict[str, Any], output)
    answer = str(output.get("answer", ""))
    missing = [
        phrase for phrase in case["required_keywords"] if normalize(phrase) not in normalize(answer)
    ]
    retrieval_output = (retrieval.get("output") or {}) if retrieval else {}
    retrieval_output = cast(dict[str, Any], retrieval_output)
    documents = " ".join(retrieval_output.get("documents", []))
    answer_words = words(answer)
    document_words = words(documents)
    expected = set(case["retrieval_keywords"])
    cost = sum(float(span["cost_usd"]) for span in spans)
    prompt_version = trace["metadata"].get("prompt_version")
    return {
        "case_id": case["case_id"],
        "trace_id": trace["trace_id"],
        "prompt_version": prompt_version if isinstance(prompt_version, str) else None,
        "task_success": not missing,
        "missing_keywords": missing,
        "groundedness": round(len(answer_words & document_words) / len(answer_words), 4)
        if answer_words
        else 0.0,
        "retrieval_relevance": round(len(expected & document_words) / len(expected), 4)
        if expected
        else 1.0,
        "tool_success": bool(tools) and all(span["status"] == "ok" for span in tools),
        "answer": answer,
        "latency_ms": round(float(root["duration_ms"]), 3),
        "estimated_cost_usd": round(cost, 8),
    }


def aggregate(rows: list[EvaluationResult]) -> dict[str, Any]:
    """Compute reproducible means and retain each case result."""
    count = len(rows)

    def mean(key: str) -> float:
        values = [float(cast(Any, row)[key]) for row in rows]
        return round(sum(values) / count, 4) if count else 0.0

    return {
        "case_count": count,
        "task_success_rate": round(sum(row["task_success"] for row in rows) / count, 4)
        if count
        else 0.0,
        "groundedness": mean("groundedness"),
        "retrieval_relevance": mean("retrieval_relevance"),
        "tool_success_rate": round(sum(row["tool_success"] for row in rows) / count, 4)
        if count
        else 0.0,
        "mean_latency_ms": mean("latency_ms"),
        "mean_estimated_cost_usd": mean("estimated_cost_usd"),
        "cases": rows,
    }
