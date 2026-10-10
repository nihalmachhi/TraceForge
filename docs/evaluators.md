# Evaluators

The fixed synthetic FAQ dataset has four cases covering refund timing, shipping, password reset, and credential-safety refusal.

- Task success checks required answer phrases.
- Groundedness measures answer-term overlap with retrieved evidence.
- Retrieval relevance checks expected evidence terms in retrieved text.
- Tool success requires a successful tool span.
- Latency sums local span durations.
- Cost uses synthetic tokens and the configurable sample rate card.

Evaluator version and per-case trace IDs are saved. These heuristics are deterministic but easy to fool. They do not measure broad reasoning or prove support. Use human labels and review false passes/failures before using model judges.
