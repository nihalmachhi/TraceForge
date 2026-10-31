"""Project paths and sample cost assumptions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
GENERATED = DATA / "generated"
DB = GENERATED / "traceforge.sqlite3"
REPORT = GENERATED / "evaluation_report.json"
DATASET = DATA / "evaluation_cases.json"
SITE = ROOT / "site" / "dist"
DEMO_RUN = "traceforge_sample_v1"
MODEL = "traceforge-synthetic-model"
RATE_CARD = {"input": 2.0, "output": 8.0}
