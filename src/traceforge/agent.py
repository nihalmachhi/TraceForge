"""Deterministic RAG-like example; no provider API call."""
import time
from traceforge.config import MODEL
class SampleAgent:
    def __init__(self,client,version):self.client,self.version=client,version
    def run(self,case,run):
        answer=case["evidence"]
        if self.version=="candidate" and case["case_id"]=="refund_window":answer="Please contact support for more information."
        if self.version=="candidate" and case["case_id"]=="password_reset":answer="Open your profile to make account changes."
        with self.client.trace("sample RAG agent",{"dataset_case_id":case["case_id"],"prompt_version":self.version,"demo_run":run}) as trace:
            with trace.span("agent workflow",kind="agent",input={"question":case["question"]}):
                with trace.span("retrieve FAQ",kind="retrieval",input={"query":case["question"]}) as s:
                    time.sleep(.002); s["output"]={"documents":[case["evidence"]],"document_ids":[case["case_id"]]}; s["attributes"]={"retriever_version":"keyword-demo-v1","top_k":1}
                with trace.span("FAQ lookup",kind="tool",input={"case_id":case["case_id"]}) as s:
                    s["output"]={"found":True,"status":"ok"}; s["attributes"]={"tool_name":"faq_catalog_lookup"}
                with trace.span("generate answer",kind="llm",input={"question":case["question"],"api_key":"tf_demo_fake_secret"},model=MODEL,prompt=self.version,in_tokens=max(1,len(case["question"].split())*2),out_tokens=max(1,len(answer.split())*2)) as s:
                    time.sleep(.004); s["output"]={"answer":answer}
        return answer
