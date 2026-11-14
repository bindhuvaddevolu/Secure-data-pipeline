
import json
import re
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "source_row_number",
    "customer_id",
    "full_name",
    "email",
    "phone",
    "age",
    "city",
    "annual_income",
    "registration_date"
]

REQUIRED_FIELDS = [
    "customer_id",
    "full_name",
    "email",
    "phone",
    "age",
    "city",
    "annual_income",
    "registration_date"
]

EMAIL_PATTERN = (
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_PATTERN = r"^\d{10}$"


def validate_data(df, source_file=None, run_id=None):
    """
    Validate customer records using vectorized Pandas operations.

    Returns:
        valid_df: Records that pass all validation rules.
        rejected_df: Records that fail validation with reasons.
        report: Validation summary.
    """

    # Verify schema
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    working_df = df.copy()
        # Add source traceability metadata
    if source_file is not None:
        working_df["source_file"] = str(source_file)

    if run_id is not None:
        working_df["run_id"] = run_id

    # Store rejection reasons by row position
    rejection_reasons = [
        [] for _ in range(len(working_df))
    ]

    def add_reason(mask, reason):
        """Add a rejection reason to matching row positions."""
        positions = (
            mask.fillna(False)
            .to_numpy()
            .nonzero()[0]
        )

        for position in positions:
            rejection_reasons[position].append(reason)

    # 1. Required field validation
    for field in REQUIRED_FIELDS:
        missing_mask = (
            working_df[field].isna()
            | working_df[field]
                .astype("string")
                .str.strip()
                .eq("")
        )

        add_reason(
            missing_mask,
            f"missing_required_field:{field}"
        )

    # 2. Duplicate customer ID validation
    duplicate_mask = (
        working_df["customer_id"].notna()
        & working_df["customer_id"].duplicated(keep="first")
    )

    add_reason(
        duplicate_mask,
        "duplicate_customer_id"
    )

    # 3. Email validation
    email_values = (
        working_df["email"]
        .astype("string")
        .str.strip()
    )

    email_mask = (
        email_values.notna()
        & email_values.ne("")
    )

    valid_email_mask = email_values.str.fullmatch(
        EMAIL_PATTERN,
        na=False
    )

    add_reason(
        email_mask & ~valid_email_mask,
        "malformed_email"
    )

    # 4. Age validation
    age_values = pd.to_numeric(
        working_df["age"],
        errors="coerce"
    )

    invalid_age_mask = (
        age_values.notna()
        & (
            (age_values < 18)
            | (age_values > 100)
            | (age_values % 1 != 0)
        )
    )

    add_reason(
        invalid_age_mask,
        "invalid_age"
    )

    invalid_age_format_mask = (
        working_df["age"].notna()
        & age_values.isna()
    )

    add_reason(
        invalid_age_format_mask,
        "invalid_age_format"
    )

    # 5. Phone validation
    phone_values = (
        working_df["phone"]
        .astype("string")
        .str.strip()
    )

    phone_mask = (
        phone_values.notna()
        & phone_values.ne("")
    )

    valid_phone_mask = phone_values.str.fullmatch(
        PHONE_PATTERN,
        na=False
    )

    add_reason(
        phone_mask & ~valid_phone_mask,
        "invalid_phone"
    )

    # 6. Annual income validation
    income_values = pd.to_numeric(
        working_df["annual_income"],
        errors="coerce"
    )

    add_reason(
        income_values.notna() & (income_values <= 0),
        "invalid_annual_income"
    )

    invalid_income_format_mask = (
        working_df["annual_income"].notna()
        & income_values.isna()
    )

    add_reason(
        invalid_income_format_mask,
        "invalid_income_format"
    )

    # 7. Registration date validation
    dates = pd.to_datetime(
        working_df["registration_date"],
        errors="coerce"
    )

    invalid_date_mask = (
        working_df["registration_date"].notna()
        & dates.isna()
    )

    add_reason(
        invalid_date_mask,
        "invalid_registration_date"
    )

    # Separate valid and rejected records
    working_df["rejection_reasons"] = [
        ";".join(reasons)
        for reasons in rejection_reasons
    ]

    valid_mask = working_df["rejection_reasons"].eq("")

    valid_df = working_df.loc[valid_mask].drop(
        columns=["rejection_reasons"]
    ).copy()

    rejected_df = working_df.loc[~valid_mask].copy()

    # Generate validation report
    report = {
        "total_input_records": len(working_df),
        "valid_records": len(valid_df),
        "rejected_records": len(rejected_df),
        "validation_status": "completed"
    }

    return valid_df, rejected_df, report


def save_validation_results(
    valid_df,
    rejected_df,
    report,
    output_dir
):
    """Save valid records, rejected records and report."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    valid_df.to_csv(
        output_dir / "valid_records.csv",
        index=False
    )

    rejected_df.to_csv(
        output_dir / "rejected_records.csv",
        index=False
    )

    with open(
        output_dir / "validation_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    print("\nValidation results saved successfully!")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root / "data" / "input" / "customers.csv"
    )

    output_dir = (
        project_root / "data" / "quarantine"
    )

    df = pd.read_csv(input_file)

    valid_df, rejected_df, report = validate_data(df)

    save_validation_results(
        valid_df,
        rejected_df,
        report,
        output_dir
    )

    print("\n========== VALIDATION REPORT ==========")
    print(json.dumps(report, indent=4))

    print("\nRejected record details:")

    if not rejected_df.empty:
        print(
            rejected_df[
                [
                    "source_row_number",
                    "customer_id",
                    "rejection_reasons"
                ]
            ].to_string(index=False)
        )

    print("\nData validation completed successfully!")
