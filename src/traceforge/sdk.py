"""Context-manager SDK with context-local nested parent spans."""
from contextvars import ContextVar
from datetime import datetime,timezone
import time,uuid
from traceforge.config import RATE_CARD
from traceforge.privacy import redact
ACTIVE=ContextVar("traceforge_active_span",default=None)
def utcnow():return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")
class Span:
    def __init__(self,trace,name,kind,input,attributes,model,prompt,in_tokens,out_tokens):
        parent=ACTIVE.get()
        if parent and parent["trace_id"]!=trace.ident:parent=None
        self.trace=trace; self.data={"span_id":uuid.uuid4().hex,"trace_id":trace.ident,"parent_span_id":parent["span_id"] if parent else None,"name":name,"kind":kind,"started_at":utcnow(),"duration_ms":0.0,"status":"running","attributes":redact(attributes),"input":redact(input),"output":None,"error":None,"model":model,"prompt_version":prompt,"input_tokens":in_tokens,"output_tokens":out_tokens,"cost_usd":round((in_tokens*RATE_CARD["input"]+out_tokens*RATE_CARD["output"])/1e6,8)}
        self.start=time.perf_counter()
    def __enter__(self):self.token=ACTIVE.set(self.data); return self.data
    def __exit__(self,kind,error,tb):
        self.data["duration_ms"]=round((time.perf_counter()-self.start)*1000,3); self.data["status"]="error" if error else "ok"
        if error:self.data["error"]=redact(str(error))
        self.trace.spans.append(self.data); ACTIVE.reset(self.token); return False
class Trace:
    def __init__(self,store,name,metadata):
        self.store,self.name,self.metadata=store,name,redact(metadata); self.ident=uuid.uuid4().hex; self.started_at=utcnow(); self.start=time.perf_counter(); self.spans=[]
        self.root={"span_id":self.ident,"trace_id":self.ident,"parent_span_id":None,"name":name,"kind":"trace","started_at":self.started_at,"duration_ms":0.0,"status":"running","attributes":{},"input":None,"output":None,"error":None,"model":None,"prompt_version":None,"input_tokens":0,"output_tokens":0,"cost_usd":0.0}
    def __enter__(self):self.token=ACTIVE.set(self.root); return self
    def span(self,name,kind="custom",input=None,attributes=None,model=None,prompt=None,in_tokens=0,out_tokens=0):return Span(self,name,kind,input,attributes or {},model,prompt,in_tokens,out_tokens)
    def __exit__(self,kind,error,tb):
        self.root["duration_ms"]=round((time.perf_counter()-self.start)*1000,3); self.root["status"]="error" if error else "ok"
        if error:self.root["error"]=redact(str(error))
        ACTIVE.reset(self.token); self.spans.insert(0,self.root)
        self.store.save({"trace_id":self.ident,"name":self.name,"started_at":self.started_at,"ended_at":utcnow(),"status":self.root["status"],"metadata":self.metadata,"spans":self.spans})
        return False
class TraceForge:
    def __init__(self,store):self.store=store
    def trace(self,name,metadata=None):return Trace(self.store,name,metadata or {})
