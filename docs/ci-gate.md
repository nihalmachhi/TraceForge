# CI regression gate

    .\scripts\run.ps1 demo
    .\scripts\run.ps1 gate

Exit 0 means thresholds passed. Exit 1 means task success or groundedness regressed. Exit 2 means no report exists. Defaults allow no task-success drop and 0.05 groundedness drop; values are fractions.

    .\scripts\run.ps1 gate --max-task-drop 0.25

The bundled candidate intentionally breaks two cases, so the default gate should fail. Archive data/generated/evaluation_report.json as a CI artifact.
