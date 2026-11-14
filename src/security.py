
EXPECTED_ANALYTICAL_COLUMNS = [
    "customer_token",
    "age",
    "city",
    "annual_income",
    "registration_date"
]

SENSITIVE_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "phone"
]


def validate_analytical_data(df):
    """Check that analytical data contains no original PII columns."""

    sensitive_found = [
        column for column in SENSITIVE_COLUMNS
        if column in df.columns
    ]

    if sensitive_found:
        raise ValueError(
            f"Privacy violation! Sensitive columns found: {sensitive_found}"
        )

    if list(df.columns) != EXPECTED_ANALYTICAL_COLUMNS:
        raise ValueError(
            "Analytical dataset schema does not match expected columns!"
        )

    if df.isnull().any().any():
        raise ValueError("Null values found in analytical dataset!")

    return True
