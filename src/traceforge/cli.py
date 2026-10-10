"""Commands for sample traces, quality gates, and the local dashboard."""
import argparse,json
from traceforge.config import DB,REPORT
from traceforge.evaluation import gate,run_demo
from traceforge.store import TraceStore
from traceforge.web import serve
def main():
    p=argparse.ArgumentParser(prog="traceforge"); sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("demo"); g=sub.add_parser("gate"); g.add_argument("--max-task-drop",type=float,default=0.0); g.add_argument("--max-groundedness-drop",type=float,default=0.05)
    w=sub.add_parser("serve"); w.add_argument("--host",default="127.0.0.1"); w.add_argument("--port",type=int,default=8000)
    a=p.parse_args()
    if a.cmd=="serve":serve(a.host,a.port); return 0
    if a.cmd=="demo":
        with TraceStore(DB) as store:r=run_demo(store)
        print(json.dumps(r,indent=2)); return 0
    if not REPORT.exists():print("Run demo first."); return 2
    r=gate(json.loads(REPORT.read_text(encoding="utf-8")),a.max_task_drop,a.max_groundedness_drop)
    print(json.dumps(r,indent=2)); return 0 if r["passed"] else 1
if __name__=="__main__":raise SystemExit(main())
