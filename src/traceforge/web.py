"""Loopback-only trace dashboard API and built React site."""
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from traceforge.config import DB, REPORT, SITE
from traceforge.evaluation import gate, run_demo
from traceforge.store import TraceStore


def factory():
    store = TraceStore(DB)
    report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else None

    class Handler(BaseHTTPRequestHandler):
        def send_json(self, value, status=200):
            body = json.dumps(value).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_site_file(self, relative_path):
            root = SITE.resolve()
            target = (root / relative_path).resolve()
            if not target.is_relative_to(root):
                self.send_json({"error": "not found"}, 404)
                return
            if not target.is_file():
                status = 503 if relative_path == "index.html" else 404
                message = (
                    "Build the React site with npm run build in site/."
                    if status == 503
                    else "not found"
                )
                self.send_json({"error": message}, status)
                return
            body = target.read_bytes()
            content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            if content_type.startswith("text/") or content_type in {
                "application/javascript",
                "application/json",
            }:
                content_type += "; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            nonlocal report
            path = urlparse(self.path).path
            if path == "/":
                self.send_site_file("index.html")
            elif path.startswith("/assets/"):
                self.send_site_file(unquote(path.lstrip("/")))
            elif path == "/api/health":
                self.send_json({"status": "ok", "data_mode": "synthetic"})
            elif path == "/api/summary":
                if report is None:
                    self.send_json({"report": None, "gate": None, "hint": "Run demo first."})
                else:
                    self.send_json({"report": report, "gate": gate(report)})
            elif path == "/api/traces":
                self.send_json(store.list())
            elif path.startswith("/api/traces/"):
                trace = store.get(path.rsplit("/", 1)[-1])
                self.send_json(trace or {"error": "not found"}, 200 if trace else 404)
            else:
                self.send_json({"error": "not found"}, 404)

        def do_POST(self):
            nonlocal report
            if urlparse(self.path).path != "/api/demo/rerun":
                self.send_json({"error": "not found"}, 404)
                return
            report = run_demo(store)
            self.send_json({"report": report, "gate": gate(report)})

        def log_message(self, fmt, *args):
            print(fmt % args)

    return Handler


def serve(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), factory())
    print(f"TraceForge: http://{host}:{port} (synthetic demo)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping TraceForge.")
    finally:
        server.server_close()
