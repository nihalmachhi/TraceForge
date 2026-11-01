import json

from traceforge import config


def test_dataset_resolves_in_source_checkout() -> None:
    assert config.DATASET.is_file()
    payload = json.loads(config.DATASET.read_text(encoding="utf-8"))
    assert payload["dataset_id"] == "traceforge-faq-v1"
    assert payload["cases"]


def test_bundled_dataset_matches_source_dataset() -> None:
    bundled = config.PACKAGE_DIR / "data" / "faq_v1.json"
    assert bundled.is_file()
    assert json.loads(bundled.read_text(encoding="utf-8")) == json.loads(
        config.DATASET.read_text(encoding="utf-8")
    )


def test_generated_paths_live_under_the_data_directory() -> None:
    assert config.DB.parent == config.GENERATED
    assert config.REPORT.parent == config.GENERATED
    assert config.SITE.name == "dist"
