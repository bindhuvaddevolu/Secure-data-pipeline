
import json

from datetime import datetime

from src import audit


def setup_audit_path(tmp_path, monkeypatch):
    fake_src = tmp_path / "src"
    fake_src.mkdir()

    fake_file = fake_src / "audit.py"
    fake_file.touch()

    monkeypatch.setattr(audit, "__file__", str(fake_file))


def read_audit_records(tmp_path):
    log_file = tmp_path / "logs" / "audit.jsonl"

    with open(log_file, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file]


def test_audit_log_creation(tmp_path, monkeypatch):
    setup_audit_path(tmp_path, monkeypatch)

    audit.write_audit_log(
    stage="validation",
    status="success",
    input_records=24,
    output_records=20,
    rejected_records=4
)

    records = read_audit_records(tmp_path)
    record = records[0]

    assert record["stage"] == "validation"
    assert record["status"] == "success"
    assert record["input_records"] == 24
    assert record["output_records"] == 20
    assert record["rejected_records"] == 4
    assert record["run_id"]
    assert record["timestamp"]


def test_audit_failure_details(tmp_path, monkeypatch):
    setup_audit_path(tmp_path, monkeypatch)

    audit.write_audit_log(
        stage="pipeline",
        status="failed",
        input_records=24,
        output_records=0,
        error_message="Database connection failed"
    )

    record = read_audit_records(tmp_path)[0]

    assert record["status"] == "failed"
    assert record["error_message"] == "Database connection failed"
    assert record["run_id"]


def test_audit_run_id_consistency(tmp_path, monkeypatch):
    setup_audit_path(tmp_path, monkeypatch)

    audit.write_audit_log(
        "validation", "success", 24, 20
    )
    audit.write_audit_log(
        "publishing", "success", 20, 20
    )

    records = read_audit_records(tmp_path)

    assert len(records) == 2
    assert records[0]["run_id"] == records[1]["run_id"]


def test_audit_timestamps_and_duration(tmp_path, monkeypatch):
    setup_audit_path(tmp_path, monkeypatch)

    start_time = "2026-11-14T10:00:00+00:00"
    end_time = "2026-11-14T10:00:05+00:00"

    audit.write_audit_log(
        stage="validation",
        status="success",
        input_records=24,
        output_records=20,
        duration_seconds=5.0,
        start_time=start_time,
        end_time=end_time
    )

    record = read_audit_records(tmp_path)[0]

    assert record["start_time"] == start_time
    assert record["end_time"] == end_time
    assert record["duration_seconds"] == 5.0

    # Verify timestamp format
    datetime.fromisoformat(record["timestamp"])
