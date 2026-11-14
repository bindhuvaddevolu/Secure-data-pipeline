
import json
from pathlib import Path


def profile_data(df):
    """
    Analyze dataset structure and data quality.

    Returns:
        Dictionary containing profiling results.
    """

    # Basic dataset information
    total_rows = len(df)
    total_columns = len(df.columns)

    # Missing values for each column
    missing_values = df.isnull().sum()

    # Duplicate customer IDs
    duplicate_ids = df["customer_id"].duplicated().sum()

    # Unique values for each column
    unique_values = df.nunique(dropna=True)

    # Column-level profiling
    column_profiles = {}

    for column in df.columns:

        column_profiles[column] = {
            "data_type": str(df[column].dtype),
            "missing_count": int(missing_values[column]),
            "unique_count": int(unique_values[column]),
            "missing_percentage": round(
                (missing_values[column] / total_rows) * 100,
                2
            ) if total_rows else 0
        }

    # Numeric column statistics
    numeric_columns = df.select_dtypes(
        include="number"
    )

    numeric_statistics = {}

    for column in numeric_columns.columns:

        numeric_statistics[column] = {
            "minimum": float(df[column].min()),
            "maximum": float(df[column].max()),
            "average": round(float(df[column].mean()), 2)
        }

    # Final profiling report
    report = {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "duplicate_customer_ids": int(duplicate_ids),
        "total_missing_values": int(missing_values.sum()),
        "column_profiles": column_profiles,
        "numeric_statistics": numeric_statistics
    }

    return report


def save_profile(report, output_path):
    """
    Save profiling results as a JSON report.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(f"Profiling report saved: {output_path}")


if __name__ == "__main__":

    import pandas as pd

    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root / "data" / "input" / "customers.csv"
    )

    output_file = (
        project_root / "reports" / "profiling_report.json"
    )

    # Read source dataset
    df = pd.read_csv(input_file)

    # Generate profiling report
    report = profile_data(df)

    # Display results
    print("\n========== DATA PROFILING REPORT ==========")

    print(f"Total rows: {report['total_rows']}")
    print(f"Total columns: {report['total_columns']}")

    print(
        "Duplicate customer IDs:",
        report["duplicate_customer_ids"]
    )

    print(
        "Total missing values:",
        report["total_missing_values"]
    )

    print("\nColumn Information:")

    for column, details in report["column_profiles"].items():

        print(f"\nColumn: {column}")
        print(f"Data type: {details['data_type']}")
        print(f"Missing values: {details['missing_count']}")
        print(f"Unique values: {details['unique_count']}")

    print("\nNumeric Statistics:")

    for column, stats in report["numeric_statistics"].items():

        print(f"\nColumn: {column}")
        print(f"Minimum: {stats['minimum']}")
        print(f"Maximum: {stats['maximum']}")
        print(f"Average: {stats['average']}")

    # Save report
    save_profile(report, output_file)

    print("\nData profiling completed successfully!")
