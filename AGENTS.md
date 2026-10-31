# TraceForge repository instructions

- Keep the core package dependency-free; provider integrations belong in optional extras.
- Use typed APIs, readable multi-line code, and lines no longer than 100 characters.
- Run `make lint`, `make types`, and `make test` before committing Python changes.
- Keep the local server bound to loopback; never add real credentials to fixtures.
- Synthetic evaluation results must be labeled as illustrative.
