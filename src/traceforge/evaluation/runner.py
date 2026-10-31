"""Evaluation runs over a shared synthetic dataset."""

import json
from typing import Any

from traceforge.agents.demo_agent import DemoAgent
from traceforge.config import (
    BASELINE_VERSION,
    CANDIDATE_VERSION,
    DATASET,
    DEMO_RUN,
    PROMPT_VERSIONS,
    REPORT,
)
from traceforge.core.tracer import TraceForge
from traceforge.evaluation.metrics import aggregate, score
from traceforge.storage.base import TraceRepository


def _all_traces(repository: TraceRepository) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    offset = 0
    while page := repository.list(limit=500, offset=offset):
        items.extend(page)
        offset += len(page)
    return items


def run_demo(repository: TraceRepository) -> dict[str, Any]:
    """Evaluate baseline and intentionally regressed fixture-driven prompts."""
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = dataset.get("cases", [])
    if not cases:
        raise ValueError("evaluation dataset must contain at least one case")
    repository.clear_demo(DEMO_RUN)
    client = TraceForge(repository)
    for version in PROMPT_VERSIONS:
        agent = DemoAgent(client, version)
        for case in cases:
            agent.run(case, DEMO_RUN)
    traces = _all_traces(repository)
    versions: dict[str, Any] = {}
    for version in PROMPT_VERSIONS:
        rows = []
        for case in cases:
            item = next(
                (
                    trace
                    for trace in traces
                    if trace["metadata"].get("demo_run") == DEMO_RUN
                    and trace["metadata"].get("dataset_case_id") == case["case_id"]
                    and trace["metadata"].get("prompt_version") == version
                ),
                None,
            )
            if item is not None:
                complete_trace = repository.get(str(item["trace_id"]))
                if complete_trace is not None:
                    rows.append(score(case, complete_trace))
        versions[version] = aggregate(rows)
    baseline = {row["case_id"]: row for row in versions[BASELINE_VERSION]["cases"]}
    candidate = {row["case_id"]: row for row in versions[CANDIDATE_VERSION]["cases"]}
    regressions = [
        case_id
        for case_id, result in baseline.items()
        if result["task_success"]
        and case_id in candidate
        and not candidate[case_id]["task_success"]
    ]
    baseline_metrics = versions[BASELINE_VERSION]
    candidate_metrics = versions[CANDIDATE_VERSION]
    report = {
        "dataset_id": dataset["dataset_id"],
        "demo_run": DEMO_RUN,
        "evaluator_version": "deterministic-v1",
        "versions": versions,
        "regressed_cases": regressions,
        "comparison": {
            "task_success_delta": round(
                candidate_metrics["task_success_rate"] - baseline_metrics["task_success_rate"], 4
            ),
            "groundedness_delta": round(
                candidate_metrics["groundedness"] - baseline_metrics["groundedness"], 4
            ),
            "retrieval_relevance_delta": round(
                candidate_metrics["retrieval_relevance"] - baseline_metrics["retrieval_relevance"],
                4,
            ),
            "mean_latency_delta_ms": round(
                candidate_metrics["mean_latency_ms"] - baseline_metrics["mean_latency_ms"], 3
            ),
            "mean_estimated_cost_delta_usd": round(
                candidate_metrics["mean_estimated_cost_usd"]
                - baseline_metrics["mean_estimated_cost_usd"],
                8,
            ),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
