"""Initial normalized trace and span tables."""

VERSION = 1
SQL = """
CREATE TABLE IF NOT EXISTS traces (
    trace_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT NOT NULL,
    status TEXT NOT NULL,
    metadata TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS spans (
    span_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL REFERENCES traces(trace_id),
    parent_span_id TEXT,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    started_at TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    status TEXT NOT NULL,
    attributes TEXT NOT NULL,
    input_json TEXT,
    output_json TEXT,
    error TEXT,
    model TEXT,
    prompt_version TEXT,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cost_usd REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_trace_time ON traces(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_span_trace ON spans(trace_id, started_at);
"""
