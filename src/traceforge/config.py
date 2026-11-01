"""Project paths, versioned defaults, and sample cost assumptions.

The paths work in three layouts: a source checkout, an editable install, and a
regular wheel install. Environment variables can override each location, which
keeps the CLI usable from CI and from read-only environments.
"""

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent


def _discover_project_root() -> Path | None:
    """Return the checkout that contains the dataset, if one is visible."""
    configured = os.environ.get("TRACEFORGE_ROOT")
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend([PACKAGE_DIR.parents[1], Path.cwd()])
    for candidate in candidates:
        if (candidate / "datasets" / "faq_v1.json").is_file():
            return candidate.resolve()
    return None


_PROJECT_ROOT = _discover_project_root()
ROOT = _PROJECT_ROOT or PACKAGE_DIR
DATA = Path(os.environ.get("TRACEFORGE_DATA", (_PROJECT_ROOT or Path.cwd()) / "data")).expanduser()
GENERATED = DATA / "generated"
DB = Path(os.environ.get("TRACEFORGE_DB", GENERATED / "traceforge.sqlite3")).expanduser()
REPORT = Path(
    os.environ.get("TRACEFORGE_REPORT", GENERATED / "evaluation_report.json")
).expanduser()

_REPO_DATASET = ROOT / "datasets" / "faq_v1.json"
_BUNDLED_DATASET = PACKAGE_DIR / "data" / "faq_v1.json"
DATASET = Path(
    os.environ.get(
        "TRACEFORGE_DATASET",
        _REPO_DATASET if _REPO_DATASET.is_file() else _BUNDLED_DATASET,
    )
).expanduser()
SITE = Path(os.environ.get("TRACEFORGE_SITE", ROOT / "site" / "dist")).expanduser()

DEMO_RUN = "traceforge_sample_v1"
MODEL = "traceforge-synthetic-model"
BASELINE_VERSION = "baseline"
CANDIDATE_VERSION = "candidate"
PROMPT_VERSIONS = (BASELINE_VERSION, CANDIDATE_VERSION)
RATE_CARD = {"input": 2.0, "output": 8.0}
GATE_THRESHOLDS = {"max_task_drop": 0.0, "max_groundedness_drop": 0.05}
