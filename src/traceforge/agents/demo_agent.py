"""Deterministic retrieval and answer-generation demo agent."""

import time
from typing import Any

from traceforge.config import MODEL
from traceforge.core.tracer import TraceForge


class DemoAgent:
    """Record a synthetic RAG workflow without contacting a model provider."""

    def __init__(self, client: TraceForge, version: str) -> None:
        self.client = client
        self.version = version

    def run(self, case: dict[str, Any], demo_run: str) -> str:
        """Record retrieval, tool, and answer spans for one fixture case."""
        answers = case.get("prompt_overrides", {})
        answer = str(answers.get(self.version, case["evidence"]))
        metadata: dict[str, object] = {
            "dataset_case_id": case["case_id"],
            "prompt_version": self.version,
            "demo_run": demo_run,
        }
        with self.client.trace("sample RAG agent", metadata) as trace:
            with trace.span("agent workflow", kind="agent", input={"question": case["question"]}):
                with trace.span(
                    "retrieve FAQ", kind="retrieval", input={"query": case["question"]}
                ) as span:
                    time.sleep(0.002)
                    span["output"] = {
                        "documents": [case["evidence"]],
                        "document_ids": [case["case_id"]],
                    }
                    span["attributes"] = {"retriever_version": "keyword-demo-v1", "top_k": 1}
                with trace.span(
                    "FAQ lookup", kind="tool", input={"case_id": case["case_id"]}
                ) as span:
                    span["output"] = {"found": True, "status": "ok"}
                    span["attributes"] = {"tool_name": "faq_catalog_lookup"}
                with trace.span(
                    "generate answer",
                    kind="llm",
                    input={"question": case["question"], "api_key": "tf_demo_fake_secret"},
                    model=MODEL,
                    prompt=self.version,
                    in_tokens=max(1, len(case["question"].split()) * 2),
                    out_tokens=max(1, len(answer.split()) * 2),
                ) as span:
                    time.sleep(0.004)
                    span["output"] = {"answer": answer}
        return answer


SampleAgent = DemoAgent
