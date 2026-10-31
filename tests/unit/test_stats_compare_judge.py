import pytest

from traceforge.evaluation.compare import compare
from traceforge.evaluation.judges import OverlapJudge
from traceforge.evaluation.stats import bootstrap_interval, paired_sign_test


def test_overlap_judge_returns_explainable_score() -> None:
    judge = OverlapJudge()
    result = judge.judge("mesh evidence", "mesh evidence found")
    assert result["score"] == 1.0
    assert "overlap" in result["rationale"]
    assert judge.judge("", "evidence")["score"] == 0.0


def test_bootstrap_interval_is_reproducible_and_validates_inputs() -> None:
    values = [1.0, 2.0, 3.0]
    first = bootstrap_interval(values, samples=100, seed=4)
    assert first == bootstrap_interval(values, samples=100, seed=4)
    assert first[0] <= 2.0 <= first[1]
    with pytest.raises(ValueError):
        bootstrap_interval([])
    with pytest.raises(ValueError):
        bootstrap_interval([1.0], confidence=1.0)


def test_paired_sign_test_handles_ties_and_mismatched_samples() -> None:
    assert paired_sign_test([1.0, 2.0], [1.0, 2.0]) == 1.0
    assert paired_sign_test([0.0, 0.0], [1.0, 1.0]) == 0.5
    with pytest.raises(ValueError):
        paired_sign_test([1.0], [])


def test_compare_reports_candidate_minus_baseline() -> None:
    baseline = {
        "task_success_rate": 0.9,
        "groundedness": 0.8,
        "retrieval_relevance": 0.7,
        "mean_latency_ms": 10,
        "mean_estimated_cost_usd": 0.01,
    }
    candidate = {
        "task_success_rate": 1.0,
        "groundedness": 0.7,
        "retrieval_relevance": 0.9,
        "mean_latency_ms": 8,
        "mean_estimated_cost_usd": 0.02,
    }
    result = compare(baseline, candidate)
    assert result["task_success_delta"] == 0.1
    assert result["groundedness_delta"] == -0.1
