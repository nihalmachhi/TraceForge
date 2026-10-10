# Architecture

    Sample agent -> TraceForge SDK -> redaction and parent validation -> SQLite
                    |                                         |
                    +-> fixed dataset -> evaluators -> comparison -> CI gate/UI

The SDK owns active trace and span context. Storage owns redaction, parent checks, and atomic writes. Evaluators read the same fixed dataset and stored spans. The CLI and dashboard share the evaluation pipeline.

## Lifecycle

1. Start a trace with dataset case and prompt version.
2. Wrap retrieval, tools, and model calls in spans.
3. Record time, duration, status, payloads, usage, and estimated cost.
4. Redact, validate parent IDs, and persist the trace batch.
5. Evaluate baseline and candidate on identical cases.
6. Inspect aggregate deltas and per-case changes.

SQLite and the standard-library server keep this project local. Queues, auth, PostgreSQL, and OpenTelemetry export are future extensions.
