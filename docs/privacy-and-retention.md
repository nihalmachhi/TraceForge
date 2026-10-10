# Privacy and retention

Avoid capturing secrets or personal data. Prefer IDs and summaries over full prompts and outputs. Define retention rules before instrumenting real traffic.

TraceForge masks values for keys matching API key, token, secret, password, authorization, email, phone, or SSN, plus common sk-prefixed and bearer-token strings. This is best-effort filtering, not a security boundary; it may miss encoded or unrecognized sensitive values. Add and validate application-specific filters.

The dashboard has no authentication. SQLite is local and unencrypted. Keep the server on loopback and use synthetic data. Real deployment requires access controls, encryption, retention deletion, audit controls, and privacy review.
