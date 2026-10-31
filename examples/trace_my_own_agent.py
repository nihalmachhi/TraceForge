"""Trace a local function with the TraceForge SDK."""

from traceforge.core.tracer import TraceForge
from traceforge.storage.sqlite import SQLiteTraceStore


def answer(question: str) -> str:
    """Example application function."""
    return f"You asked: {question}"


with SQLiteTraceStore(__import__("pathlib").Path("example.sqlite3")) as store:
    tracer = TraceForge(store)
    with tracer.trace("answer question") as trace:
        with trace.span("answer", kind="llm", input={"question": "What is tracing?"}) as span:
            span["output"] = {"answer": answer("What is tracing?")}
