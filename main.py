
from pathlib import Path
import json
import time
import uuid
from datetime import datetime, timezone, timedelta

from src.data_generator import generate_dataset, save_dataset
from src.ingestion import ingest_data
from src.profiling import profile_data, save_profile
from src.validation import validate_data, save_validation_results
from src.masking import get_secret_key, apply_privacy_transformations
from src.minimization import minimize_data
from src.security import validate_analytical_data
from src.publishing import publish_data
from src.audit import write_audit_log
from src.reconciliation import reconcile_counts


def _log_stage(
    stage,
    start_time,
    input_count,
    output_count,
    run_id,
    rejected_records=0
):
    duration = round(time.perf_counter() - start_time, 4)

    end_timestamp = datetime.now(timezone.utc)
    start_timestamp = (
        end_timestamp - timedelta(seconds=duration)
    ).isoformat()

    write_audit_log(
        stage=stage,
        status="success",
        input_records=input_count,
        output_records=output_count,
        rejected_records=rejected_records,
        duration_seconds=duration,
        run_id=run_id,
        start_time=start_timestamp,
        end_time=end_timestamp.isoformat()
    )

    return duration


def _run_pipeline(state, run_id):
    root = Path(__file__).resolve().parent

    # 1. Generate data
    state["stage"] = "data_generation"
    start = time.perf_counter()

    df, labels = generate_dataset(
        num_records=20,
        seed=42,
        include_edge_cases=True
    )
    save_dataset(df, labels)

    state["input_records"] = len(df)

    _log_stage(
        "data_generation", start, len(df), len(df), run_id
    )
    print("1. Data generation completed")

    # 2. Ingest data
    state["stage"] = "data_ingestion"
    start = time.perf_counter()

    input_file = root / "data" / "input" / "customers.csv"
    df = ingest_data(input_file)

    state["input_records"] = len(df)

    _log_stage(
        "data_ingestion", start, len(df), len(df), run_id
    )
    print("2. Data ingestion completed")

    # 3. Profile data
    state["stage"] = "data_profiling"
    start = time.perf_counter()

    report = profile_data(df)
    save_profile(
        report,
        root / "reports" / "profiling_report.json"
    )

    _log_stage(
        "data_profiling", start, len(df), len(df), run_id
    )
    print("3. Data profiling completed")

    # 4. Validate data
    state["stage"] = "data_validation"
    start = time.perf_counter()

    valid_df, rejected_df, validation_report = validate_data(
        df,
        source_file=input_file,
        run_id=run_id
    )

    quarantine_dir = root / "data" / "quarantine"

    save_validation_results(
        valid_df,
        rejected_df,
        validation_report,
        quarantine_dir
    )

    state["valid_records"] = len(valid_df)
    state["rejected_records"] = len(rejected_df)

    _log_stage(
        "data_validation",
        start,
        len(df),
        len(valid_df),
        run_id,
        rejected_records=len(rejected_df)
    )
    print("4. Data validation completed")

    # 5. Mask sensitive data
    state["stage"] = "data_masking"
    start = time.perf_counter()

    secret_key = get_secret_key()

    masked_df = apply_privacy_transformations(
        valid_df,
        secret_key
    )

    masked_file = root / "data" / "output" / "masked_customers.csv"
    masked_file.parent.mkdir(parents=True, exist_ok=True)
    masked_df.to_csv(masked_file, index=False)

    _log_stage(
        "data_masking",
        start,
        len(valid_df),
        len(masked_df),
        run_id
    )
    print("5. Data masking completed")

    # 6. Minimize data
    state["stage"] = "data_minimization"
    start = time.perf_counter()

    analytical_df = minimize_data(masked_df)

    analytical_file = (
        root / "data" / "output" / "analytical_customers.csv"
    )
    analytical_df.to_csv(analytical_file, index=False)

    _log_stage(
        "data_minimization",
        start,
        len(masked_df),
        len(analytical_df),
        run_id
    )
    print("6. Data minimization completed")

    # 7. Security validation
    state["stage"] = "security_validation"
    start = time.perf_counter()

    validate_analytical_data(analytical_df)

    _log_stage(
        "security_validation",
        start,
        len(analytical_df),
        len(analytical_df),
        run_id
    )
    print("7. Privacy security validation passed!")

    # 8. Database publishing
    state["stage"] = "database_publishing"
    start = time.perf_counter()

    database_file = root / "data" / "output" / "analytics.db"

    published_count = publish_data(
        analytical_df,
        database_file
    )

    state["published_records"] = published_count

    _log_stage(
        "database_publishing",
        start,
        len(analytical_df),
        published_count,
        run_id
    )
    print(
        f"8. Database publishing completed: "
        f"{published_count} records"
    )

    # 9. Reconciliation
    state["stage"] = "reconciliation"
    start = time.perf_counter()

    reconciliation_report = reconcile_counts(
        input_records=len(df),
        valid_records=len(valid_df),
        rejected_records=len(rejected_df),
        published_records=published_count
    )

    reconciliation_path = (
        root / "reports" / "reconciliation_report.json"
    )
    reconciliation_path.parent.mkdir(parents=True, exist_ok=True)

    with open(reconciliation_path, "w", encoding="utf-8") as file:
        json.dump(reconciliation_report, file, indent=4)

    _log_stage(
        "reconciliation",
        start,
        len(df),
        published_count,
        run_id
    )
    print("9. Reconciliation completed successfully!")

    # 10. Final summary
    print("\n========== PIPELINE SUMMARY ==========")
    print(f"Run ID: {run_id}")
    print(f"Input records: {len(df)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Rejected records: {len(rejected_df)}")
    print(f"Published records: {published_count}")
    print(
        "Reconciliation status:",
        reconciliation_report["reconciliation_status"]
    )

    print("\nPipeline completed successfully!")


def run_pipeline():
    run_id = str(uuid.uuid4())
    pipeline_start = datetime.now(timezone.utc)
    timer_start = time.perf_counter()

    state = {
        "run_id": run_id,
        "stage": "pipeline_initialization",
        "input_records": 0,
        "valid_records": 0,
        "rejected_records": 0,
        "published_records": 0
    }

    print(f"Starting pipeline. Run ID: {run_id}")

    try:
        _run_pipeline(state, run_id)

        duration = round(time.perf_counter() - timer_start, 4)
        pipeline_end = datetime.now(timezone.utc)

        write_audit_log(
            stage="pipeline_execution",
            status="success",
            input_records=state["input_records"],
            output_records=state["published_records"],
            rejected_records=state["rejected_records"],
            duration_seconds=duration,
            run_id=run_id,
            start_time=pipeline_start.isoformat(),
            end_time=pipeline_end.isoformat()
        )

    except Exception as error:
        duration = round(time.perf_counter() - timer_start, 4)
        pipeline_end = datetime.now(timezone.utc)

        print(f"\nPipeline failed during: {state['stage']}")
        print(f"Run ID: {run_id}")
        print(f"Error details: {error}")

        try:
            write_audit_log(
                stage=state["stage"],
                status="failed",
                input_records=state["input_records"],
                output_records=state["published_records"],
                rejected_records=state["rejected_records"],
                error_message=str(error),
                duration_seconds=duration,
                run_id=run_id,
                start_time=pipeline_start.isoformat(),
                end_time=pipeline_end.isoformat()
            )
        except Exception as audit_error:
            print(
                "Failure audit could not be saved:",
                audit_error
            )

        raise


if __name__ == "__main__":
    run_pipeline()
