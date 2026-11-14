
import pandas as pd
import pytest

from src.minimization import minimize_data


def test_minimize_data():
    df = pd.DataFrame({
        "customer_token": ["abc123"],
        "age": [25],
        "city": ["Hyderabad"],
        "annual_income": [500000],
        "registration_date": ["2026-01-01"],
        "masked_email": ["a***@gmail.com"]
    })

    result = minimize_data(df)

    assert len(result.columns) == 5
    assert len(result) == 1
    assert "masked_email" not in result.columns


def test_missing_column():
    df = pd.DataFrame({
        "customer_token": ["abc123"],
        "age": [25]
    })

    with pytest.raises(ValueError):
        minimize_data(df)
