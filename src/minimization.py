
from pathlib import Path
import pandas as pd


ANALYTICAL_COLUMNS = [
    "customer_token",
    "age",
    "city",
    "annual_income",
    "registration_date"
]


def minimize_data(df):
    missing_columns = [
        col for col in ANALYTICAL_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    return df[ANALYTICAL_COLUMNS].copy()


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "output" / "masked_customers.csv"
    output_file = project_root / "data" / "output" / "analytical_customers.csv"

    df = pd.read_csv(input_file)
    analytical_df = minimize_data(df)

    analytical_df.to_csv(output_file, index=False)

    print("Data minimization completed!")
    print(f"Input columns: {len(df.columns)}")
    print(f"Output columns: {len(analytical_df.columns)}")
    print(f"Output records: {len(analytical_df)}")
    print(analytical_df.head().to_string(index=False))
