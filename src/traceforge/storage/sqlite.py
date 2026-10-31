"""SQLite-backed atomic trace repository."""

import json
import sqlite3
from pathlib import Path
from typing import Any

from traceforge.core.models import TraceRecord
from traceforge.storage.migrations.v001_initial import SQL, VERSION


class SQLiteTraceStore:
    """Persist traces and spans in a local, indexed SQLite database."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self._migrate()

    def _migrate(self) -> None:
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        applied = {int(row[0]) for row in self.db.execute("SELECT version FROM schema_migrations")}
        if VERSION not in applied:
            with self.db:
                self.db.executescript(SQL)
                self.db.execute("INSERT INTO schema_migrations(version) VALUES (?)", (VERSION,))

    def save(self, trace: TraceRecord) -> None:
        """Validate and save the trace as one transaction."""
        spans = trace["spans"]
        span_ids = {span["span_id"] for span in spans}
        if len(span_ids) != len(spans):
            raise ValueError("duplicate span ID")
        for span in spans:
            if span["trace_id"] != trace["trace_id"]:
                raise ValueError("span trace_id mismatch")
            if span["parent_span_id"] and span["parent_span_id"] not in span_ids:
                raise ValueError("orphan span")
        try:
            with self.db:
                self.db.execute(
                    "INSERT INTO traces VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        trace["trace_id"],
                        trace["name"],
                        trace["started_at"],
                        trace["ended_at"],
                        trace["status"],
                        json.dumps(trace["metadata"]),
                    ),
                )
                for span in spans:
                    self.db.execute(
                        "INSERT INTO spans VALUES ("
                        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            span["span_id"],
                            span["trace_id"],
                            span["parent_span_id"],
                            span["name"],
                            span["kind"],
                            span["started_at"],
                            span["duration_ms"],
                            span["status"],
                            json.dumps(span["attributes"]),
                            json.dumps(span["input"]) if span["input"] is not None else None,
                            json.dumps(span["output"]) if span["output"] is not None else None,
                            span["error"],
                            span["model"],
                            span["prompt_version"],
                            span["input_tokens"],
                            span["output_tokens"],
                            span["cost_usd"],
                        ),
                    )
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed" in str(error):
                raise ValueError("duplicate trace or span ID") from error
            raise

    def list(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """Return a bounded page of traces, newest first."""
        page_size = max(1, min(500, int(limit)))
        page_offset = max(0, int(offset))
        rows = self.db.execute(
            "SELECT * FROM traces ORDER BY started_at DESC, trace_id LIMIT ? OFFSET ?",
            (page_size, page_offset),
        )
        result = []
        for row in rows:
            trace = dict(row)
            trace["metadata"] = json.loads(trace["metadata"])
            result.append(trace)
        return result

    def get(self, trace_id: str) -> TraceRecord | None:
        """Return a complete trace with its spans, if present."""
        row = self.db.execute("SELECT * FROM traces WHERE trace_id=?", (trace_id,)).fetchone()
        if row is None:
            return None
        trace: dict[str, Any] = dict(row)
        trace["metadata"] = json.loads(trace["metadata"])
        spans = self.db.execute(
            "SELECT * FROM spans WHERE trace_id=? ORDER BY started_at, span_id", (trace_id,)
        )
        trace["spans"] = []
        for row in spans:
            span = dict(row)
            for field in ("attributes", "input_json", "output_json"):
                span[field] = json.loads(span[field]) if span[field] else None
            span["input"] = span.pop("input_json")
            span["output"] = span.pop("output_json")
            trace["spans"].append(span)
        return trace  # type: ignore[return-value]

    def clear_demo(self, demo_run: str) -> None:
        """Remove traces tagged with the specified synthetic demo run."""
        rows = self.db.execute("SELECT trace_id, metadata FROM traces").fetchall()
        trace_ids = [
            row["trace_id"]
            for row in rows
            if json.loads(row["metadata"]).get("demo_run") == demo_run
        ]
        with self.db:
            for trace_id in trace_ids:
                self.db.execute("DELETE FROM spans WHERE trace_id=?", (trace_id,))
                self.db.execute("DELETE FROM traces WHERE trace_id=?", (trace_id,))

    def close(self) -> None:
        """Close the SQLite connection."""
        self.db.close()

    def __enter__(self) -> "SQLiteTraceStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


TraceStore = SQLiteTraceStore
