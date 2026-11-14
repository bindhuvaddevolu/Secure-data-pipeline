
import json
from pathlib import Path


def profile_data(df):
    """
    Analyze dataset structure and data quality.
    Returns detailed profiling and quality metrics.
    """

    total_rows = len(df)
    total_columns = len(df.columns)

    missing_values = df.isnull().sum()
    duplicate_ids = (
        int(df["customer_id"].duplicated().sum())
        if "customer_id" in df.columns else 0
    )

    unique_values = df.nunique(dropna=True)

    column_profiles = {}

    for column in df.columns:
        missing_count = int(missing_values[column])

        completeness = (
            ((total_rows - missing_count) / total_rows) * 100
            if total_rows else 0
        )

        column_profiles[column] = {
            "data_type": str(df[column].dtype),
            "missing_count": missing_count,
            "unique_count": int(unique_values[column]),
            "missing_percentage": round(
                (missing_count / total_rows) * 100, 2
            ) if total_rows else 0,
            "completeness_percentage": round(completeness, 2)
        }

    numeric_columns = df.select_dtypes(include="number")
    numeric_statistics = {}

    for column in numeric_columns.columns:
        if numeric_columns[column].notna().any():
            numeric_statistics[column] = {
                "minimum": float(numeric_columns[column].min()),
                "maximum": float(numeric_columns[column].max()),
                "average": round(
                    float(numeric_columns[column].mean()), 2
                )
            }

    total_missing = int(missing_values.sum())

    total_cells = total_rows * total_columns

    completeness_percentage = (
        ((total_cells - total_missing) / total_cells) * 100
        if total_cells else 100
    )

    duplicate_percentage = (
        (duplicate_ids / total_rows) * 100
        if total_rows else 0
    )

    # Quality score: completeness and uniqueness
    quality_score = max(
        0,
        round(
            (completeness_percentage + (100 - duplicate_percentage)) / 2,
            2
        )
    )

    report = {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "duplicate_customer_ids": duplicate_ids,
        "duplicate_percentage": round(duplicate_percentage, 2),
        "total_missing_values": total_missing,
        "completeness_percentage": round(
            completeness_percentage, 2
        ),
        "data_quality_score": quality_score,
        "column_profiles": column_profiles,
        "numeric_statistics": numeric_statistics
    }

    return report


def save_profile(report, output_path):
    """Save profiling results as a JSON report."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Profiling report saved: {output_path}")


if __name__ == "__main__":
    import pandas as pd

    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "input" / "customers.csv"
    output_file = project_root / "reports" / "profiling_report.json"

    df = pd.read_csv(input_file)
    report = profile_data(df)

    print("\n========== DATA QUALITY REPORT ==========")
    print(f"Total rows: {report['total_rows']}")
    print(f"Total columns: {report['total_columns']}")
    print(f"Duplicate IDs: {report['duplicate_customer_ids']}")
    print(f"Duplicate percentage: {report['duplicate_percentage']}%")
    print(f"Missing values: {report['total_missing_values']}")
    print(f"Completeness: {report['completeness_percentage']}%")
    print(f"Data quality score: {report['data_quality_score']}%")

    print("\nColumn Completeness:")
    for column, details in report["column_profiles"].items():
        print(
            f"{column}: {details['completeness_percentage']}%"
        )

    print("\nNumeric Statistics:")
    for column, stats in report["numeric_statistics"].items():
        print(f"{column}: {stats}")

    save_profile(report, output_file)
    print("\nData profiling completed successfully!")
