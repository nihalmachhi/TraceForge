from traceforge.config import DATASET
from traceforge.evaluation.runner import run_demo
from traceforge.storage.sqlite import SQLiteTraceStore


def test_demo_generates_report_with_regressed_candidate(tmp_path, monkeypatch) -> None:
    database = tmp_path / "demo.sqlite3"
    monkeypatch.setattr("traceforge.evaluation.runner.REPORT", tmp_path / "report.json")
    monkeypatch.setattr("traceforge.evaluation.runner.DATASET", DATASET)
    with SQLiteTraceStore(database) as store:
        report = run_demo(store)
    assert report["regressed_cases"]
    assert (tmp_path / "report.json").exists()
