# Trace schema

A trace is one end-to-end operation. A span is a timed child operation.

| Field | Meaning |
| --- | --- |
| trace_id | ID for the full operation. |
| span_id | Unique span ID and deduplication key for replayed batches. |
| parent_span_id | Parent span; null for root. |
| kind | trace, agent, retrieval, tool, llm, or custom. |
| started_at, duration_ms | UTC start and measured duration. |
| status, error | ok/error state; exception text is redacted. |
| input, output, attributes | JSON payloads, redacted before persistence. |
| model, prompt_version | Optional model and prompt metadata. |
| input_tokens, output_tokens, cost_usd | Usage and estimate fields. |

Missing parents reject a batch. SQLite saves a whole trace atomically. Replaying the same serialized batch with stable IDs is idempotent; a new operation gets new IDs.
