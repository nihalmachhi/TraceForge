"""Deterministic judge interface used by offline evaluation."""

from typing import Protocol, TypedDict


class Judgment(TypedDict):
    """Normalized rubric outcome."""

    score: float
    rationale: str


class Judge(Protocol):
    """Score an answer against evidence using a shared contract."""

    def judge(self, answer: str, evidence: str) -> Judgment:
        """Return an explainable score between zero and one."""
        ...


class OverlapJudge:
    """Simple deterministic evidence-overlap judge for CI and offline use."""

    def judge(self, answer: str, evidence: str) -> Judgment:
        """Score answer token overlap with its evidence."""
        answer_words = set(answer.lower().split())
        evidence_words = set(evidence.lower().split())
        score = len(answer_words & evidence_words) / len(answer_words) if answer_words else 0.0
        return {"score": round(score, 4), "rationale": "token overlap with supplied evidence"}
