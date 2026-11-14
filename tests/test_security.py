
import pandas as pd
import pytest

from src.security import validate_analytical_data


def valid_analytical_data():
    return pd.DataFrame({
        "customer_token": ["token1", "token2"],
        "age": [25, 30],
        "city": ["Hyderabad", "Vijayawada"],
        "annual_income": [500000, 600000],
        "registration_date": ["2026-01-01", "2026-02-01"]
    })


def test_valid_analytical_data():
    df = valid_analytical_data()
    assert validate_analytical_data(df) is True


def test_sensitive_columns_rejected():
    df = valid_analytical_data()
    df["email"] = ["a@test.com", "b@test.com"]

    with pytest.raises(ValueError, match="Privacy violation"):
        validate_analytical_data(df)


def test_extra_column_rejected():
    df = valid_analytical_data()
    df["extra_column"] = ["x", "y"]

    with pytest.raises(ValueError, match="schema"):
        validate_analytical_data(df)


def test_null_values_rejected():
    df = valid_analytical_data()
    df.loc[0, "city"] = None

    with pytest.raises(ValueError, match="Null values"):
        validate_analytical_data(df)
