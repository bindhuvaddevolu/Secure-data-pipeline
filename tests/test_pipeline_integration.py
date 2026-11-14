
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
import main


def test_complete_pipeline_execution():
    project_root = Path(__file__).resolve().parent.parent

    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr
    assert "Pipeline completed successfully!" in result.stdout
    assert "Reconciliation status: passed" in result.stdout

    database_path = project_root / "data" / "output" / "analytics.db"

    assert database_path.exists()

    with sqlite3.connect(database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM analytical_customers"
        ).fetchone()[0]

    assert count == 20


def test_pipeline_failure_and_retry(monkeypatch):
    project_root = Path(__file__).resolve().parent.parent
    database_path = (
        project_root / "data" / "output" / "analytics.db"
    )

    audit_records = []

    # Capture audit records without changing the actual log file
    monkeypatch.setattr(
        main,
        "write_audit_log",
        lambda **kwargs: audit_records.append(kwargs)
    )

    original_validation = main.validate_analytical_data
    attempts = {"count": 0}

    # Simulate a failure during the first execution
    def fail_once(df):
        attempts["count"] += 1

        if attempts["count"] == 1:
            raise RuntimeError("Simulated pipeline failure")

        return original_validation(df)

    monkeypatch.setattr(
        main,
        "validate_analytical_data",
        fail_once
    )

    # First execution should fail
    with pytest.raises(RuntimeError, match="Simulated pipeline failure"):
        main.run_pipeline()

    # Verify failure audit record
    failed_records = [
        record for record in audit_records
        if record["status"] == "failed"
    ]

    assert len(failed_records) == 1
    assert failed_records[0]["stage"] == "security_validation"
    assert failed_records[0]["error_message"] == (
        "Simulated pipeline failure"
    )

    failed_run_id = failed_records[0]["run_id"]

    # Retry the pipeline
    main.run_pipeline()

    # Verify successful retry audit record
    successful_records = [
        record for record in audit_records
        if record["stage"] == "pipeline_execution"
        and record["status"] == "success"
    ]

    assert len(successful_records) == 1

    retry_run_id = successful_records[0]["run_id"]

    # Each execution must have a different run ID
    assert failed_run_id != retry_run_id

    # Verify published records after retry
    with sqlite3.connect(database_path) as connection:
        total_count = connection.execute(
            "SELECT COUNT(*) FROM analytical_customers"
        ).fetchone()[0]

        unique_count = connection.execute(
            "SELECT COUNT(DISTINCT customer_token) "
            "FROM analytical_customers"
        ).fetchone()[0]

    assert total_count == 20
    assert unique_count == 20
