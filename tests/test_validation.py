
import pandas as pd
import pytest

from src.validation import validate_data


def test_validation_edge_cases():
    df = pd.DataFrame({
        "customer_id": ["CUST001", "CUST001", "CUST002", "CUST003", "CUST004"],
        "full_name": ["Rahul", "Kiran", "Priya", "Arun", "Sita"],
        "email": [
            "rahul@gmail.com",
            "kiran@gmail.com",
            None,
            "arun@gmail.com",
            "invalid-email"
        ],
        "phone": [
            "9876543210", "9876543211", "9876543212",
            "9876543213", "9876543214"
        ],
        "age": [25, 30, 28, 150, 35],
        "city": ["Hyderabad", "Mumbai", "Delhi", "Chennai", "Pune"],
        "annual_income": [500000, 600000, 700000, 800000, 900000],
        "registration_date": [
            "2026-01-01", "2026-01-02", "2026-01-03",
            "2026-01-04", "2026-01-05"
        ],
        "source_row_number": [1, 2, 3, 4, 5]
    })

    valid_df, rejected_df, report = validate_data(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 4
    assert len(valid_df) + len(rejected_df) == len(df)


def test_empty_dataframe():
    columns = [
        "customer_id", "full_name", "email", "phone", "age",
        "city", "annual_income", "registration_date",
        "source_row_number"
    ]

    df = pd.DataFrame(columns=columns)
    valid_df, rejected_df, report = validate_data(df)

    assert len(valid_df) == 0
    assert len(rejected_df) == 0


def test_missing_schema_column():
    df = pd.DataFrame({
        "customer_id": ["CUST001"],
        "full_name": ["Rahul"]
    })

    with pytest.raises(ValueError):
        validate_data(df)
