
from pathlib import Path
import pandas as pd


# Define the expected source columns
EXPECTED_COLUMNS = [
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


def ingest_data(file_path):
    """
    Read customer data from a CSV file.

    Returns:
        pandas DataFrame containing source data.
    """

    file_path = Path(file_path)

    # Check whether the file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    # Check whether the path points to a file
    if not file_path.is_file():
        raise ValueError(
            f"Source path is not a file: {file_path}"
        )

    # Read CSV file
    try:
        df = pd.read_csv(file_path)

    except pd.errors.EmptyDataError:
        raise ValueError("Source CSV file is empty")

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Malformed CSV file: {error}"
        )

    # Check for empty dataset
    if df.empty:
        raise ValueError(
            "CSV contains headers but no records"
        )

    # Check expected columns
    actual_columns = list(df.columns)

    missing_columns = [
        col for col in EXPECTED_COLUMNS
        if col not in actual_columns
    ]

    unexpected_columns = [
        col for col in actual_columns
        if col not in EXPECTED_COLUMNS
    ]

    if missing_columns or unexpected_columns:
        raise ValueError(
            f"Schema mismatch. "
            f"Missing columns: {missing_columns}. "
            f"Unexpected columns: {unexpected_columns}."
        )

    print("Data ingestion completed successfully!")
    print(f"Total records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    return df


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parent.parent

    source_file = (
        project_root / "data" / "input" / "customers.csv"
    )

    customers_df = ingest_data(source_file)

    print("\nFirst five records:")
    print(customers_df.head())
