
import pytest

from src.data_generator import generate_dataset


def test_generate_dataset_default_records():
    customers_df, labels_df = generate_dataset()

    assert len(customers_df) == 24
    assert len(labels_df) == 4


def test_generate_dataset_without_edge_cases():
    customers_df, labels_df = generate_dataset(
        num_records=100,
        seed=42,
        include_edge_cases=False
    )

    assert len(customers_df) == 100
    assert len(labels_df) == 0
    assert customers_df["customer_id"].is_unique


def test_generate_dataset_reproducibility():
    first_df, _ = generate_dataset(num_records=10, seed=42)
    second_df, _ = generate_dataset(num_records=10, seed=42)

    assert first_df.equals(second_df)


def test_generate_dataset_invalid_record_count():
    with pytest.raises(ValueError):
        generate_dataset(num_records=0)


def test_generate_dataset_small_record_count():
    customers_df, labels_df = generate_dataset(num_records=2)

    assert len(customers_df) == 6
    assert len(labels_df) == 4
