
import pandas as pd
import pytest

from src.ingestion import ingest_data


EXPECTED_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "phone",
    "age",
    "city",
    "annual_income",
    "registration_date",
    "source_row_number"
]


def create_valid_dataset():
    return pd.DataFrame({
        "customer_id": ["CUST001"],
        "full_name": ["Test User"],
        "email": ["test@example.com"],
        "phone": ["9876543210"],
        "age": [25],
        "city": ["Hyderabad"],
        "annual_income": [500000],
        "registration_date": ["2026-01-01"],
        "source_row_number": [1]
    })


def test_successful_ingestion(tmp_path):
    file_path = tmp_path / "customers.csv"
    create_valid_dataset().to_csv(file_path, index=False)

    result = ingest_data(file_path)

    assert len(result) == 1
    assert list(result.columns) == EXPECTED_COLUMNS


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        ingest_data("missing_customers.csv")


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises((ValueError, pd.errors.EmptyDataError)):
        ingest_data(file_path)


def test_missing_columns(tmp_path):
    file_path = tmp_path / "missing_columns.csv"

    df = create_valid_dataset().drop(columns=["email"])
    df.to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        ingest_data(file_path)


def test_unexpected_columns(tmp_path):
    file_path = tmp_path / "extra_columns.csv"

    df = create_valid_dataset()
    df["extra_column"] = ["unexpected"]
    df.to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        ingest_data(file_path)
