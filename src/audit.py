
import json
from datetime import datetime, timezone
from pathlib import Path


def write_audit_log(stage, status, input_records, output_records):
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "logs" / "audit.jsonl"

    log_file.parent.mkdir(parents=True, exist_ok=True)

    audit_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "status": status,
        "input_records": input_records,
        "output_records": output_records
    }

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(audit_record, default=int) + "\n")

    print(f"Audit log saved for: {stage}")


if __name__ == "__main__":
    write_audit_log(
        stage="data_minimization",
        status="success",
        input_records=20,
        output_records=20
    )
