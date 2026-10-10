# TraceForge: how it works

A trace is the journey of one agent request. Spans are its timed steps, connected by parent IDs.

1. The agent starts a root trace for a synthetic FAQ case.
2. It records retrieval, a catalog tool, and answer generation as child spans.
3. Spans capture timing, status, payloads, prompt version, token use, and estimated cost.
4. Redaction runs before SQLite persistence.
5. A fixed dataset is evaluated against baseline and candidate prompts.
6. Deterministic checks score answer phrases, evidence overlap, retrieval, and tool status.
7. A report lists changes and case regressions; the CLI gate returns a failure code.
8. The dashboard shows the comparison and trace waterfall.

## Run

    py -3 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    .\scripts\run.ps1 demo
    .\scripts\run.ps1 serve

Open http://127.0.0.1:8000. Select a trace and find the sample api_key stored as [REDACTED]. Run the gate to see the intentionally regressed candidate fail.

## Limits

Keyword and evidence-overlap checks are heuristics. Local latency is not remote-model latency. Costs are estimates. Redaction is not comprehensive. No production integration or load benchmark is included.
