
import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Unique ID for each pipeline process execution
RUN_ID = str(uuid.uuid4())


def write_audit_log(
    stage,
    status,
    input_records,
    output_records,
    error_message=None,
    duration_seconds=None,
    run_id=None,
    start_time=None,
    end_time=None,
    rejected_records=0
):
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "logs" / "audit.jsonl"

    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Capture UTC timestamps
    current_time = datetime.now(timezone.utc)

    end_timestamp = end_time or current_time.isoformat()

    if start_time:
        start_timestamp = start_time
    elif duration_seconds is not None:
        start_timestamp = (
            current_time - timedelta(seconds=duration_seconds)
        ).isoformat()
    else:
        start_timestamp = current_time.isoformat()

    audit_record = {
        "run_id": run_id or RUN_ID,
        "timestamp": current_time.isoformat(),
        "start_time": start_timestamp,
        "end_time": end_timestamp,
        "stage": stage,
        "status": status,
        "input_records": int(input_records),
        "output_records": int(output_records),
        "rejected_records": int(rejected_records),
        "error_message": error_message,
        "duration_seconds": duration_seconds
    }

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(audit_record) + "\n")

    print(f"Audit log saved for: {stage}")


if __name__ == "__main__":
    write_audit_log(
        stage="data_validation",
        status="success",
        input_records=24,
        output_records=20,
        rejected_records=4,
        duration_seconds=1.25
    )
