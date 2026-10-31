import sqlite3

import pytest

from traceforge.core.tracer import TraceForge
from traceforge.storage.sqlite import SQLiteTraceStore


def test_nested_trace_persists_with_redaction_and_context(tmp_path) -> None:
    store = SQLiteTraceStore(tmp_path / "traces.sqlite3")
    client = TraceForge(store)
    with client.trace("request", {"prompt_version": "v1"}) as trace:
        with trace.span("agent", kind="agent"):
            with trace.span("model", kind="llm", input={"api_key": "secret"}) as span:
                span["output"] = {"answer": "safe"}
    saved = store.get(trace.ident)
    assert saved is not None
    llm_span = next(span for span in saved["spans"] if span["kind"] == "llm")
    assert llm_span["parent_span_id"] is not None
    assert llm_span["input"] == {"api_key": "[REDACTED]"}
    store.close()


def test_trace_records_exception_and_does_not_suppress(tmp_path) -> None:
    store = SQLiteTraceStore(tmp_path / "traces.sqlite3")
    client = TraceForge(store)
    with pytest.raises(RuntimeError, match="broken"):
        with client.trace("failed"):
            raise RuntimeError("broken")
    failed = store.list()[0]
    assert failed["status"] == "error"
    store.close()


def test_duplicate_trace_id_raises_clear_error(tmp_path) -> None:
    store = SQLiteTraceStore(tmp_path / "traces.sqlite3")
    client = TraceForge(store)
    with client.trace("first") as trace:
        pass
    with pytest.raises(ValueError, match="duplicate"):
        store.save(store.get(trace.ident))
    store.close()


def test_list_paginates_and_demo_clear_is_scoped(tmp_path) -> None:
    store = SQLiteTraceStore(tmp_path / "traces.sqlite3")
    client = TraceForge(store)
    for name in ("one", "two", "three"):
        with client.trace(name, {"demo_run": "sample" if name != "two" else "keep"}):
            pass
    assert len(store.list(limit=1, offset=1)) == 1
    store.clear_demo("sample")
    assert len(store.list()) == 1
    store.close()


def test_migration_and_wal_are_enabled(tmp_path) -> None:
    path = tmp_path / "traces.sqlite3"
    store = SQLiteTraceStore(path)
    assert store.db.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    assert store.db.execute("SELECT version FROM schema_migrations").fetchall()
    store.close()
    with pytest.raises(sqlite3.ProgrammingError):
        store.db.execute("SELECT 1")
