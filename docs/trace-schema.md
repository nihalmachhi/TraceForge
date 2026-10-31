# Trace schema

A trace contains a unique `trace_id`, name, start/end timestamps, status,
metadata, and spans. Each span records its ID, parent ID, kind, timing, status,
attributes, optional input/output, model and prompt identifiers, token counts,
and estimated cost. Root spans have no parent. Child spans reference a span in
the same trace. The SQLite schema is versioned in `storage/migrations/`.
