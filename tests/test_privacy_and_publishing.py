
import pandas as pd
import pytest

from src.masking import apply_privacy_transformations
from src.publishing import publish_data


def test_configurable_masking(tmp_path):
    df = pd.DataFrame({
        "customer_id": ["CUST000001"],
        "full_name": ["Rahul Kumar"],
        "email": ["rahul@gmail.com"],
        "phone": ["9876543210"],
        "age": [25]
    })

    config_file = tmp_path / "privacy_rules.json"

    config_file.write_text("""
    {
        "tokenization": {
            "enabled": true,
            "source_column": "customer_id",
            "output_column": "customer_token"
        },
        "masking": {
            "full_name": {
                "enabled": true,
                "output_column": "masked_name",
                "method": "mask_name"
            },
            "email": {
                "enabled": true,
                "output_column": "masked_email",
                "method": "mask_email"
            },
            "phone": {
                "enabled": true,
                "output_column": "masked_phone",
                "method": "mask_phone"
            }
        },
        "drop_original_columns": [
            "customer_id",
            "full_name",
            "email",
            "phone"
        ]
    }
    """, encoding="utf-8")

    result = apply_privacy_transformations(
        df,
        b"test-secret-key-for-unit-tests-123456",
        config_file
    )

    assert "customer_token" in result.columns
    assert "masked_email" in result.columns
    assert "email" not in result.columns
    assert len(result) == 1


def test_repeated_publishing(tmp_path):
    df = pd.DataFrame({
        "customer_token": ["token1", "token2"],
        "age": [25, 30],
        "city": ["Hyderabad", "Vijayawada"],
        "annual_income": [500000, 600000],
        "registration_date": ["2026-01-01", "2026-01-02"]
    })

    database = tmp_path / "test.db"

    first = publish_data(df, database)
    second = publish_data(df, database)

    assert first == 2
    assert second == 2


def test_duplicate_tokens_rejected(tmp_path):
    df = pd.DataFrame({
        "customer_token": ["token1", "token1"],
        "age": [25, 30],
        "city": ["Hyderabad", "Vijayawada"],
        "annual_income": [500000, 600000],
        "registration_date": ["2026-01-01", "2026-01-02"]
    })

    with pytest.raises(ValueError):
        publish_data(df, tmp_path / "test.db")
