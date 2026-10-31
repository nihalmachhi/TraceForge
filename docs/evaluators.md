# Evaluators

The deterministic evaluator checks required answer phrases, evidence overlap,
retrieval keyword relevance, tool status, root-span latency, and estimated cost.
It repeats the same fixed examples for each prompt version. It does not use an
LLM judge; its numbers demonstrate regression-gate wiring only.
