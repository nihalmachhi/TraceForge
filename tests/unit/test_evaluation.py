from traceforge.evaluation.gate import gate
from traceforge.evaluation.metrics import aggregate, normalize, words


def test_text_helpers_and_empty_aggregate() -> None:
    assert normalize("Hello,   WORLD!") == "hello world"
    assert words("a mesh with signals") == {"mesh", "with", "signals"}
    assert aggregate([])["case_count"] == 0


def test_gate_reports_both_regression_kinds() -> None:
    result = gate({"comparison": {"task_success_delta": -0.2, "groundedness_delta": -0.2}})
    assert result["passed"] is False
    assert len(result["failures"]) == 2


def test_gate_threshold_overrides_allow_expected_regression() -> None:
    result = gate(
        {"comparison": {"task_success_delta": -0.2, "groundedness_delta": -0.2}},
        max_task_drop=0.25,
        max_groundedness_drop=0.25,
    )
    assert result["passed"] is True


def test_aggregate_computes_means() -> None:
    row = {
        "case_id": "c1",
        "trace_id": "t1",
        "prompt_version": "v1",
        "task_success": True,
        "missing_keywords": [],
        "groundedness": 0.5,
        "retrieval_relevance": 1.0,
        "tool_success": True,
        "answer": "ok",
        "latency_ms": 10.0,
        "estimated_cost_usd": 0.01,
    }
    result = aggregate([row])
    assert result["task_success_rate"] == 1.0
    assert result["mean_latency_ms"] == 10.0
