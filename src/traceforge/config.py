"""Project paths, versioned defaults, and sample cost assumptions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DATASETS = ROOT / "datasets"
GENERATED = DATA / "generated"
DB = GENERATED / "traceforge.sqlite3"
REPORT = GENERATED / "evaluation_report.json"
DATASET = DATASETS / "faq_v1.json"
SITE = ROOT / "site" / "dist"
DEMO_RUN = "traceforge_sample_v1"
MODEL = "traceforge-synthetic-model"
BASELINE_VERSION = "baseline"
CANDIDATE_VERSION = "candidate"
PROMPT_VERSIONS = (BASELINE_VERSION, CANDIDATE_VERSION)
RATE_CARD = {"input": 2.0, "output": 8.0}
GATE_THRESHOLDS = {"max_task_drop": 0.0, "max_groundedness_drop": 0.05}
