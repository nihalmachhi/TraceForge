import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from traceforge.api.app import factory
from traceforge.storage.sqlite import SQLiteTraceStore


def test_server_routes_static_files_and_empty_report(tmp_path, monkeypatch) -> None:
    site = tmp_path / "site"
    (site / "assets").mkdir(parents=True)
    (site / "index.html").write_text("<h1>TraceForge</h1>", encoding="utf-8")
    (site / "assets" / "app.js").write_text("const ok = true;", encoding="utf-8")
    monkeypatch.setattr("traceforge.api.app.DB", tmp_path / "traces.sqlite3")
    monkeypatch.setattr("traceforge.api.app.REPORT", tmp_path / "missing-report.json")
    monkeypatch.setattr("traceforge.api.app.SITE", site)
    store = SQLiteTraceStore(tmp_path / "traces.sqlite3")
    server = ThreadingHTTPServer(("127.0.0.1", 0), factory(store))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(f"{origin}/") as response:
            assert response.status == 200
            assert b"TraceForge" in response.read()
        with urlopen(f"{origin}/assets/app.js") as response:
            assert response.headers["Content-Type"].startswith("text/javascript")
        with urlopen(f"{origin}/api/health") as response:
            assert json.load(response)["status"] == "ok"
        with urlopen(f"{origin}/api/summary") as response:
            assert json.load(response)["report"] is None
        with urlopen(f"{origin}/api/traces?limit=2&offset=0") as response:
            assert json.load(response)["items"] == []
        try:
            urlopen(f"{origin}/api/traces?limit=nope")
        except HTTPError as error:
            assert error.code == 400
        else:
            raise AssertionError("invalid pagination should return HTTP 400")
        try:
            urlopen(f"{origin}/assets/%2e%2e%2f%2e%2e%2fsecret")
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("asset traversal should return HTTP 404")
        request = Request(f"{origin}/api/demo/rerun", data=b"", method="POST")
        with urlopen(request) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
        store.close()
