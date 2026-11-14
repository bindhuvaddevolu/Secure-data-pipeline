
import pytest
from src.reconciliation import reconcile_counts


def test_reconciliation_success():
    report = reconcile_counts(24, 20, 4, 20)

    assert report["reconciliation_status"] == "passed"


def test_input_reconciliation_failure():
    with pytest.raises(ValueError):
        reconcile_counts(24, 20, 3, 20)


def test_publishing_reconciliation_failure():
    with pytest.raises(ValueError):
        reconcile_counts(24, 20, 4, 19)
