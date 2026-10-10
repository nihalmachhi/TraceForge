"""Loopback-only trace dashboard API."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from urllib.parse import urlparse
from traceforge.config import DB,FRONTEND,REPORT
from traceforge.evaluation import gate,run_demo
from traceforge.store import TraceStore
def factory():
    store=TraceStore(DB); report=json.loads(REPORT.read_text(encoding="utf-8"))
    class Handler(BaseHTTPRequestHandler):
        def send_json(self,value,status=200):
            b=json.dumps(value).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Cache-Control","no-store"); self.send_header("X-Content-Type-Options","nosniff"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            p=urlparse(self.path).path
            if p=="/":
                b=(FRONTEND/"index.html").read_bytes(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
            elif p=="/api/health":self.send_json({"status":"ok","data_mode":"synthetic"})
            elif p=="/api/summary":self.send_json({"report":report,"gate":gate(report)})
            elif p=="/api/traces":self.send_json(store.list())
            elif p.startswith("/api/traces/"):
                x=store.get(p.rsplit("/",1)[-1]); self.send_json(x or {"error":"not found"},200 if x else 404)
            else:self.send_json({"error":"not found"},404)
        def do_POST(self):
            nonlocal report
            if urlparse(self.path).path!="/api/demo/rerun":self.send_json({"error":"not found"},404); return
            report=run_demo(store); self.send_json({"report":report,"gate":gate(report)})
        def log_message(self,fmt,*args):print(args[0]%args[1:])
    return Handler
def serve(host="127.0.0.1",port=8000):
    server=ThreadingHTTPServer((host,port),factory()); print("TraceForge: http://%s:%s (synthetic demo)"%(host,port))
    try:server.serve_forever()
    except KeyboardInterrupt:print("\nStopping TraceForge.")
    finally:server.server_close()
