# Security policy

## Supported versions

TraceForge is a pre-1.0 teaching project. Security fixes land on `main` and in the latest tagged
release.

## Reporting a vulnerability

Please do not open a public issue for a security problem. Use GitHub's private vulnerability
reporting on the repository's **Security** tab, or email the maintainer listed on the GitHub
profile. Include:

- the affected version or commit,
- a minimal reproduction,
- the impact you believe it has,
- any suggested fix.

You should receive an acknowledgement within a few days. Please allow time for a fix before public
disclosure.

## Scope and threat model

TraceForge is designed to run on a developer machine.

- The HTTP server binds to `127.0.0.1` and has **no authentication**. Do not expose it to a network.
- Redaction is best effort. It is not a compliance control and cannot detect every form of personal
  data.
- The demo agent is synthetic and makes no external model calls.
- Provider adapters are optional extras and are disabled unless explicitly configured.
- Never put real credentials in fixtures, tests, examples, or reports.

If you deploy or extend TraceForge, add authentication, TLS, request limits, and a reviewed
redaction policy before handling real user data.
