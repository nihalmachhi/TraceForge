"""Best-effort key and token redaction before persistence."""
import re
KEY=re.compile(r"(?:api[_-]?key|token|secret|password|authorization|email|phone|ssn)",re.I)
TEXT=re.compile(r"(?i)(?:sk-[A-Za-z0-9_-]{12,}|Bearer\s+[A-Za-z0-9._~+/-]+=*)")
def redact(value,key=""):
    if KEY.search(key): return "[REDACTED]"
    if isinstance(value,dict): return {str(k):redact(v,str(k)) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [redact(v) for v in value]
    if isinstance(value,str): return TEXT.sub("[REDACTED]",value)
    return value
