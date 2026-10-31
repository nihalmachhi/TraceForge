"""Create the illustrated TraceForge operating guide PDF."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "TraceForge_How_It_Works.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], fontSize=27, leading=33, textColor=colors.HexColor("#12304a"), alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="Sub", parent=styles["Normal"], fontSize=12, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#476276")))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=13))
def P(text, style="BodyText"): return Paragraph(text, styles[style])
def box(text, width=1.4*inch):
    t=Table([[P(text,"Small")]], colWidths=[width], rowHeights=[.65*inch])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#e7f1f7")),("BOX",(0,0),(-1,-1),1,colors.HexColor("#36708a")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(0,0),(-1,-1),"CENTER"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7)]))
    return t
def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica",8); canvas.setFillColor(colors.HexColor("#607080"))
    canvas.drawString(.65*inch,.4*inch,"TraceForge ? local synthetic observability demo")
    canvas.drawRightString(7.85*inch,.4*inch,str(doc.page)); canvas.restoreState()
story=[Spacer(1,1.2*inch),P("TraceForge","Cover"),P("How the AI agent observability project works","Sub"),Spacer(1,.3*inch),P("A practical illustrated guide to running the demo, reading traces, comparing prompt versions, and understanding the regression gate.","Sub"),Spacer(1,.5*inch),P("Everything runs locally. The sample agent is deterministic and makes no external model calls.","Sub"),PageBreak()]
story += [P("1. What you built","Heading1"),P("TraceForge is a small observability and evaluation system for an AI-agent workflow. It records a tree of trace spans, redacts sensitive-looking values before storage, evaluates two prompt versions against the same fixed cases, and exposes the results through a local web dashboard and a CI-style gate."),Spacer(1,12),P("System map","Heading2")]
diagram=Table([[box("User / CLI calls the agent workflow",2.15*inch),box("Workflow records nested spans",2.15*inch),box("Redactor persists spans to SQLite",2.15*inch)],[box("Dashboard reads the local API",2.15*inch),box("Evaluation compares prompt versions",2.15*inch),box("Gate checks quality thresholds",2.15*inch)]],colWidths=[2.15*inch]*3)
diagram.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [diagram,Spacer(1,12),P("The evaluator is deterministic: identical inputs produce identical demo outputs. This makes the project easy to run and inspect without API keys. It demonstrates the observability pattern; it does not claim production model quality.","Small"),P("2. Run it","Heading1"),P("From PowerShell, open the TraceForge folder, create and activate a virtual environment, then run the demo and dashboard:")]
story += [Preformatted("py -3 -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1\n.\\scripts\\run.ps1 demo\n.\\scripts\\run.ps1 serve",styles["Code"]),P("Open http://127.0.0.1:8000. The demo writes its SQLite database and JSON report under data/generated/. Rerunning the demo replaces only its tagged sample records."),P("3. Follow one request","Heading1"),P("A trace is the complete request. It contains spans arranged as parent and child operations. The root workflow span groups retrieval, tool, and model-like work. Each span has a name, timestamps, status, attributes, and optional input/output summaries. The SDK uses context-local state to connect child operations to their parent."),P("Sensitive-looking keys such as password, token, and API key are redacted before persistence. This is a best-effort safeguard, not a guarantee that arbitrary personal data will be detected."),PageBreak()]
story += [P("4. Evaluation and comparison","Heading1"),P("The bundled JSON cases exercise task success, evidence grounding, and credential safety. The demo evaluates a baseline and a deliberately regressed candidate over the same cases. The report also records illustrative latency and cost values."),P("The CI gate compares candidate metrics with configured limits. A failed gate is expected for the intentionally regressed sample and returns a nonzero exit code. That gives you a concrete example of blocking a regression before release."),P("5. Dashboard and endpoints","Heading1"),P("The standard-library HTTP server binds to loopback by default. The page reads a summary and recent traces from the local API. The demo rerun button creates a fresh report. Endpoints include /api/health, /api/summary, /api/traces, /api/traces/{trace_id}, and POST /api/demo/rerun."),P("Keep the server on localhost: it has no authentication. Do not expose it to an untrusted network."),P("6. Folder map","Heading1")]
rows=[[P("<b>Path</b>","Small"),P("<b>Purpose</b>","Small")]]
for a,b in [("src/traceforge/","Agent, SDK, storage, privacy, evaluation, HTTP API, CLI"),("data/","Fixed synthetic evaluation cases; runtime output is ignored"),("site/","React dashboard and browser simulator"),("scripts/","PowerShell runner and PDF guide builder"),("docs/","Architecture, schema, evaluator, CI, privacy, walkthrough"),("output/pdf/","Generated illustrated guide")]:
    rows.append([P(a,"Small"),P(b,"Small")])
tbl=Table(rows,colWidths=[1.65*inch,5.0*inch]);tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#dceaf1")),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#b7c7d1")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story += [tbl,Spacer(1,12),P("7. What to explore next","Heading1"),P("Inspect docs/architecture.md and docs/trace-schema.md, then run the CLI gate and compare the JSON report. Replace the deterministic agent adapter with a real model provider only after adding provider-specific timeout, retry, cost, and secret-handling policies. Keep real credentials out of the synthetic dataset."),P("Limitations","Heading2"),P("This starter is local and single-process, uses SQLite, has no authentication, and has no production load or security validation. The redactor is heuristic. Cost numbers are examples, and the evaluator is not a model judge.")]
OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=.65*inch,leftMargin=.65*inch,topMargin=.65*inch,bottomMargin=.7*inch,title="TraceForge: How It Works",author="TraceForge Project").build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
