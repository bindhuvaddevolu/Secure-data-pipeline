
from pathlib import Path
import json

from src.data_generator import generate_dataset, save_dataset
from src.ingestion import ingest_data
from src.profiling import profile_data, save_profile
from src.validation import validate_data, save_validation_results
from src.masking import (
    get_secret_key,
    apply_privacy_transformations
)
from src.minimization import minimize_data
from src.publishing import publish_data
from src.audit import write_audit_log
from src.reconciliation import reconcile_counts


def _run_pipeline():
    root = Path(__file__).resolve().parent

    # 1. Generate data
    df, labels = generate_dataset(
        num_records=20,
        seed=42,
        include_edge_cases=True
    )
    save_dataset(df, labels)
    print("1. Data generation completed")

    # 2. Ingest data
    input_file = root / "data" / "input" / "customers.csv"
    df = ingest_data(input_file)
    print("2. Data ingestion completed")

    # 3. Profile data
    report = profile_data(df)
    save_profile(
        report,
        root / "reports" / "profiling_report.json"
    )
    print("3. Data profiling completed")

    # 4. Validate data
    valid_df, rejected_df, validation_report = validate_data(df)

    quarantine_dir = root / "data" / "quarantine"
    save_validation_results(
        valid_df,
        rejected_df,
        validation_report,
        quarantine_dir
    )
    print("4. Data validation completed")

    write_audit_log(
        "validation",
        "success",
        len(df),
        len(valid_df)
    )

    # 5. Mask sensitive data
    secret_key = get_secret_key()
    masked_df = apply_privacy_transformations(
        valid_df,
        secret_key
    )

    masked_file = root / "data" / "output" / "masked_customers.csv"
    masked_file.parent.mkdir(parents=True, exist_ok=True)
    masked_df.to_csv(masked_file, index=False)
    print("5. Data masking completed")

    # 6. Minimize data
    analytical_df = minimize_data(masked_df)

    analytical_file = (
        root / "data" / "output" / "analytical_customers.csv"
    )
    analytical_df.to_csv(analytical_file, index=False)
    print("6. Data minimization completed")

    write_audit_log(
        "data_minimization",
        "success",
        len(masked_df),
        len(analytical_df)
    )

    # 7. Publish to SQLite
    database_file = root / "data" / "output" / "analytics.db"

    published_count = publish_data(
        analytical_df,
        database_file
    )
    print(f"7. Database publishing completed: {published_count} records")

    write_audit_log(
        "publishing",
        "success",
        len(analytical_df),
        published_count
    )

    # 8. Reconciliation
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

    print("8. Reconciliation completed successfully!")

    write_audit_log(
        "reconciliation",
        "success",
        len(df),
        published_count
    )

    # 9. Final pipeline summary
    print("\n========== PIPELINE SUMMARY ==========")
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
    try:
        _run_pipeline()

    except Exception as error:
        print(f"Pipeline failed: {error}")

        try:
            write_audit_log(
                stage="pipeline",
                status="failed",
                input_records=0,
                output_records=0
            )
        except Exception as audit_error:
            print(f"Failure audit could not be saved: {audit_error}")

        raise


if __name__ == "__main__":
    run_pipeline()
