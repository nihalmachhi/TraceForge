"""Minimal OTLP/HTTP JSON trace exporter."""

import json
from urllib.request import Request, urlopen

from traceforge.core.models import TraceRecord


class OTLPHTTPExporter:
    """Export spans to an OTLP JSON collector endpoint."""

    def __init__(self, endpoint: str, timeout: float = 10) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.timeout = timeout

    def export(self, trace: TraceRecord) -> None:
        """POST one trace using the OTLP JSON trace shape."""
        spans = [
            {
                "traceId": span["trace_id"],
                "spanId": span["span_id"],
                "parentSpanId": span["parent_span_id"] or "",
                "name": span["name"],
                "kind": 1,
                "startTimeUnixNano": str(
                    int(
                        __import__("datetime")
                        .datetime.fromisoformat(span["started_at"].replace("Z", "+00:00"))
                        .timestamp()
                        * 1_000_000_000
                    )
                ),
                "attributes": [
                    {"key": key, "value": {"stringValue": str(value)}}
                    for key, value in span["attributes"].items()
                ],
                "status": {"code": 2 if span["status"] == "error" else 1},
            }
            for span in trace["spans"]
        ]
        body = json.dumps({"resourceSpans": [{"scopeSpans": [{"spans": spans}]}]}).encode()
        request = Request(
            f"{self.endpoint}/v1/traces",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=self.timeout):
            return
