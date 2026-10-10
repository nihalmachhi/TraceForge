"""Fixed dataset evaluator, version comparison, and CI threshold check."""
import json,re
from traceforge.config import DATASET,DEMO_RUN,REPORT
from traceforge.agent import SampleAgent
from traceforge.sdk import TraceForge

def words(s):
    stop={"the","a","an","is","are","to","of","and","in","for","you","your","can"}
    return {w for w in re.findall(r"[a-z0-9]+",s.lower()) if len(w)>2 and w not in stop}
def score(case,trace):
    spans=trace["spans"]; llm=next((s for s in spans if s["kind"]=="llm"),{}); retr=next((s for s in spans if s["kind"]=="retrieval"),{})
    tools=[s for s in spans if s["kind"]=="tool"]; answer=(llm.get("output") or {}).get("answer","")
    norm=lambda s:re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",s.lower())).strip()
    missing=[p for p in case["required_keywords"] if norm(p) not in norm(answer)]
    docs=" ".join((retr.get("output") or {}).get("documents",[])); at,dt=words(answer),words(docs); expected=set(case["retrieval_keywords"])
    return {"case_id":case["case_id"],"trace_id":trace["trace_id"],"prompt_version":trace["metadata"].get("prompt_version"),"task_success":not missing,"missing_keywords":missing,"groundedness":round(len(at&dt)/len(at),4) if at else 0.0,"retrieval_relevance":round(len(expected&dt)/len(expected),4) if expected else 1.0,"tool_success":bool(tools) and all(s["status"]=="ok" for s in tools),"answer":answer,"latency_ms":round(sum(s["duration_ms"] for s in spans),3),"estimated_cost_usd":round(sum(s["cost_usd"] for s in spans),8)}
def aggregate(rows):
    n=len(rows); mean=lambda k:round(sum(float(r[k]) for r in rows)/n,4) if n else 0.0
    return {"case_count":n,"task_success_rate":mean("task_success"),"groundedness":mean("groundedness"),"retrieval_relevance":mean("retrieval_relevance"),"tool_success_rate":mean("tool_success"),"mean_latency_ms":mean("latency_ms"),"mean_estimated_cost_usd":mean("estimated_cost_usd"),"cases":rows}
def run_demo(store):
    data=json.loads(DATASET.read_text(encoding="utf-8"))
    if not data.get("cases"):raise ValueError("empty dataset")
    store.clear_demo(DEMO_RUN); client=TraceForge(store)
    for version in ("baseline","candidate"):
        agent=SampleAgent(client,version)
        for case in data["cases"]:agent.run(case,DEMO_RUN)
    traces=store.list(500); versions={}
    for version in ("baseline","candidate"):
        rows=[]
        for case in data["cases"]:
            item=next((t for t in traces if t["metadata"].get("demo_run")==DEMO_RUN and t["metadata"].get("dataset_case_id")==case["case_id"] and t["metadata"].get("prompt_version")==version),None)
            if item:rows.append(score(case,store.get(item["trace_id"])))
        versions[version]=aggregate(rows)
    base={x["case_id"]:x for x in versions["baseline"]["cases"]}; cand={x["case_id"]:x for x in versions["candidate"]["cases"]}
    regressions=[k for k,v in base.items() if v["task_success"] and k in cand and not cand[k]["task_success"]]
    report={"dataset_id":data["dataset_id"],"demo_run":DEMO_RUN,"evaluator_version":"deterministic-v1","versions":versions,"regressed_cases":regressions}
    report["comparison"]={"task_success_delta":round(versions["candidate"]["task_success_rate"]-versions["baseline"]["task_success_rate"],4),"groundedness_delta":round(versions["candidate"]["groundedness"]-versions["baseline"]["groundedness"],4),"retrieval_relevance_delta":round(versions["candidate"]["retrieval_relevance"]-versions["baseline"]["retrieval_relevance"],4),"mean_latency_delta_ms":round(versions["candidate"]["mean_latency_ms"]-versions["baseline"]["mean_latency_ms"],3),"mean_estimated_cost_delta_usd":round(versions["candidate"]["mean_estimated_cost_usd"]-versions["baseline"]["mean_estimated_cost_usd"],8)}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
def gate(report,max_task_drop=0.0,max_groundedness_drop=0.05):
    d=report["comparison"]; failures=[]
    if d["task_success_delta"] < -max_task_drop:failures.append("task_success_regression")
    if d["groundedness_delta"] < -max_groundedness_drop:failures.append("groundedness_regression")
    return {"passed":not failures,"failures":failures,"thresholds":{"max_task_drop":max_task_drop,"max_groundedness_drop":max_groundedness_drop}}
