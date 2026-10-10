"""Atomic SQLite persistence for parent-linked traces and spans."""
import json,sqlite3
from pathlib import Path
from traceforge.privacy import redact
class TraceStore:
    def __init__(self,path:Path):
        path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path,check_same_thread=False); self.db.row_factory=sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS traces(trace_id TEXT PRIMARY KEY,name TEXT NOT NULL,started_at TEXT NOT NULL,ended_at TEXT NOT NULL,status TEXT NOT NULL,metadata TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS spans(span_id TEXT PRIMARY KEY,trace_id TEXT NOT NULL REFERENCES traces(trace_id),parent_span_id TEXT,name TEXT NOT NULL,kind TEXT NOT NULL,started_at TEXT NOT NULL,duration_ms REAL NOT NULL,status TEXT NOT NULL,attributes TEXT NOT NULL,input_json TEXT,output_json TEXT,error TEXT,model TEXT,prompt_version TEXT,input_tokens INTEGER NOT NULL,output_tokens INTEGER NOT NULL,cost_usd REAL NOT NULL);
        CREATE INDEX IF NOT EXISTS idx_trace_time ON traces(started_at DESC);
        CREATE INDEX IF NOT EXISTS idx_span_trace ON spans(trace_id,started_at);
        """); self.db.commit()
    def save(self,trace):
        spans=trace["spans"]; ids={s["span_id"] for s in spans}
        if len(ids)!=len(spans): raise ValueError("duplicate span ID")
        for s in spans:
            if s["trace_id"]!=trace["trace_id"]: raise ValueError("span trace_id mismatch")
            if s["parent_span_id"] and s["parent_span_id"] not in ids: raise ValueError("orphan span")
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO traces VALUES(?,?,?,?,?,?)",(trace["trace_id"],trace["name"],trace["started_at"],trace["ended_at"],trace["status"],json.dumps(redact(trace["metadata"]))))
            for s in spans:
                self.db.execute("INSERT OR IGNORE INTO spans VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(s["span_id"],s["trace_id"],s["parent_span_id"],s["name"],s["kind"],s["started_at"],s["duration_ms"],s["status"],json.dumps(redact(s["attributes"])),json.dumps(redact(s["input"])),json.dumps(redact(s["output"])),redact(s["error"]),s["model"],s["prompt_version"],s["input_tokens"],s["output_tokens"],s["cost_usd"]))
    def list(self,limit=100):
        rows=self.db.execute("SELECT * FROM traces ORDER BY started_at DESC LIMIT ?",(max(1,min(500,int(limit))),))
        out=[]
        for r in rows:
            x=dict(r); x["metadata"]=json.loads(x.pop("metadata")); out.append(x)
        return out
    def get(self,ident):
        row=self.db.execute("SELECT * FROM traces WHERE trace_id=?",(ident,)).fetchone()
        if row is None:return None
        x=dict(row); x["metadata"]=json.loads(x.pop("metadata")); x["spans"]=[]
        for r in self.db.execute("SELECT * FROM spans WHERE trace_id=? ORDER BY started_at,span_id",(ident,)):
            s=dict(r)
            for k in ("attributes","input_json","output_json"): s[k]=json.loads(s[k]) if s[k] else None
            s["input"]=s.pop("input_json"); s["output"]=s.pop("output_json"); x["spans"].append(s)
        return x
    def clear_demo(self,run):
        rows=self.db.execute("SELECT trace_id,metadata FROM traces").fetchall()
        ids=[r["trace_id"] for r in rows if json.loads(r["metadata"]).get("demo_run")==run]
        with self.db:
            for i in ids:
                self.db.execute("DELETE FROM spans WHERE trace_id=?",(i,)); self.db.execute("DELETE FROM traces WHERE trace_id=?",(i,))
    def close(self):self.db.close()
    def __enter__(self):return self
    def __exit__(self,*_):self.close()
