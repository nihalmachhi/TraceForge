# Privacy and data handling

TraceForge applies heuristic redaction to sensitive keys and common secret or
personal-data patterns before persisting SDK traces. This is best effort and
cannot guarantee identification of all sensitive data. Keep real credentials
out of fixtures and avoid storing personal information. The unauthenticated
dashboard binds to loopback by default; do not expose it to an untrusted
network.
