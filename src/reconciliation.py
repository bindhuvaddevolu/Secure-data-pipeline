
def reconcile_counts(
    input_records,
    valid_records,
    rejected_records,
    published_records
):
    report = {
        "input_records": input_records,
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "published_records": published_records
    }

    if input_records != valid_records + rejected_records:
        raise ValueError("Input reconciliation failed!")

    if valid_records != published_records:
        raise ValueError("Publishing reconciliation failed!")

    report["reconciliation_status"] = "passed"
    return report
