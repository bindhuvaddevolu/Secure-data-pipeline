
import pandas as pd
import pytest

from src.reconciliation import reconcile_counts


def sample_data():
    return pd.DataFrame({
        "customer_token": ["TOKEN001", "TOKEN002"],
        "age": [25, 30],
        "city": ["Hyderabad", "Bangalore"],
        "annual_income": [500000.0, 700000.0],
        "registration_date": ["2025-01-01", "2025-02-01"]
    })


def test_reconciliation_success():
    report = reconcile_counts(10, 8, 2, 8)

    assert report["input_records"] == 10
    assert report["valid_records"] == 8
    assert report["rejected_records"] == 2
    assert report["published_records"] == 8
    assert report["reconciliation_status"] == "passed"


def test_input_reconciliation_failure():
    with pytest.raises(ValueError, match="Input reconciliation failed"):
        reconcile_counts(10, 7, 2, 7)


def test_publishing_reconciliation_failure():
    with pytest.raises(ValueError, match="Publishing reconciliation failed"):
        reconcile_counts(10, 8, 2, 7)


def test_data_level_reconciliation_success():
    df = sample_data()

    report = reconcile_counts(
        2, 2, 0, 2,
        validated_data=df,
        published_data=df.copy()
    )

    assert report["record_level_reconciliation"] == "passed"
    assert report["income_reconciliation"] == "passed"
    assert report["records_verified"] == 2
    assert report["reconciliation_status"] == "passed"


def test_duplicate_published_tokens_rejected():
    validated = sample_data()
    published = validated.copy()
    published.loc[1, "customer_token"] = "TOKEN001"

    with pytest.raises(ValueError, match="Duplicate customer tokens"):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )


def test_null_published_tokens_rejected():
    validated = sample_data()
    published = validated.copy()
    published.loc[0, "customer_token"] = None

    with pytest.raises(ValueError, match="null values"):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )


def test_income_reconciliation_failure():
    validated = sample_data()
    published = validated.copy()
    published.loc[0, "annual_income"] = 900000.0

    with pytest.raises(ValueError, match="Annual income reconciliation failed"):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )


def test_missing_analytical_dataset_rejected():
    validated = sample_data()

    with pytest.raises(
        ValueError,
        match="Both validated_data and published_data are required"
    ):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated
        )


def test_dataset_record_count_mismatch():
    validated = sample_data()
    published = validated.iloc[:1].copy()

    with pytest.raises(ValueError, match="Published dataset count mismatch"):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )


def test_record_level_reconciliation_detects_changed_city():
    validated = sample_data()
    published = validated.copy()
    published.loc[0, "city"] = "Chennai"

    with pytest.raises(
        ValueError,
        match="Record-level reconciliation failed"
    ):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )


def test_record_level_reconciliation_detects_swapped_income_values():
    validated = sample_data()
    published = validated.copy()
    published["annual_income"] = [700000.0, 500000.0]

    assert validated["annual_income"].sum() == published["annual_income"].sum()

    with pytest.raises(
        ValueError,
        match="Record-level reconciliation failed"
    ):
        reconcile_counts(
            2, 2, 0, 2,
            validated_data=validated,
            published_data=published
        )
