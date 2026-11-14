
import re
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


def validate_data(df):
    """
    Validate customer records using business rules.

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

    # Work on a copy to preserve source data
    working_df = df.copy()

    # Store rejection reasons for each row
    rejection_reasons = [[] for _ in range(len(working_df))]

    # Required field checks
    required_fields = [
        "customer_id",
        "full_name",
        "email",
        "phone",
        "age",
        "city",
        "annual_income",
        "registration_date"
    ]

    for field in required_fields:

        missing_mask = (
            working_df[field].isna()
            | working_df[field].astype("string").str.strip().eq("")
        ).fillna(True)

        for index in range(len(working_df)):
            if missing_mask.iloc[index]:
                rejection_reasons[index].append(
                    f"missing_required_field:{field}"
                )

    # Duplicate customer ID check
    duplicate_mask = (
        working_df["customer_id"].notna()
        & working_df["customer_id"].duplicated(keep="first")
    )

    for index in range(len(working_df)):
        if duplicate_mask.iloc[index]:
            rejection_reasons[index].append(
                "duplicate_customer_id"
            )

    # Email format validation
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    for index, email in enumerate(working_df["email"]):

        if pd.notna(email) and str(email).strip():

            if not re.fullmatch(email_pattern, str(email).strip()):
                rejection_reasons[index].append(
                    "malformed_email"
                )

    # Age validation
    age_values = pd.to_numeric(
        working_df["age"],
        errors="coerce"
    )

    for index, age in enumerate(age_values):

        if pd.notna(age):

            if age < 18 or age > 100 or not float(age).is_integer():
                rejection_reasons[index].append(
                    "invalid_age"
                )

        elif pd.notna(working_df.iloc[index]["age"]):
            rejection_reasons[index].append(
                "invalid_age_format"
            )

    # Phone validation
    for index, phone in enumerate(working_df["phone"]):

        if pd.notna(phone) and str(phone).strip():

            if not re.fullmatch(r"\d{10}", str(phone).strip()):
                rejection_reasons[index].append(
                    "invalid_phone"
                )

    # Income validation
    income_values = pd.to_numeric(
        working_df["annual_income"],
        errors="coerce"
    )

    for index, income in enumerate(income_values):

        if pd.notna(income) and income <= 0:
            rejection_reasons[index].append(
                "invalid_annual_income"
            )

        elif pd.isna(income) and pd.notna(
            working_df.iloc[index]["annual_income"]
        ):
            rejection_reasons[index].append(
                "invalid_income_format"
            )

    # Registration date validation
    dates = pd.to_datetime(
        working_df["registration_date"],
        errors="coerce"
    )

    for index, date in enumerate(dates):

        if pd.isna(date) and pd.notna(
            working_df.iloc[index]["registration_date"]
        ):
            rejection_reasons[index].append(
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
    """
    Save validated records, rejected records
    and validation report.
    """

    from pathlib import Path
    import json

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

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

        json.dump(
            report,
            file,
            indent=4
        )

    print("\nValidation results saved successfully!")


if __name__ == "__main__":

    from pathlib import Path
    import json

    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root / "data" / "input" / "customers.csv"
    )

    output_dir = (
        project_root / "data" / "quarantine"
    )

    # Read source dataset
    df = pd.read_csv(input_file)

    # Perform validation
    valid_df, rejected_df, report = validate_data(df)

    # Save results
    save_validation_results(
        valid_df,
        rejected_df,
        report,
        output_dir
    )

    # Display summary
    print("\n========== VALIDATION REPORT ==========")

    print(json.dumps(report, indent=4))

    print("\nRejected record details:")

    if not rejected_df.empty:
        print(
            rejected_df[
                ["source_row_number", "customer_id", "rejection_reasons"]
            ].to_string(index=False)
        )

    print("\nData validation completed successfully!")
