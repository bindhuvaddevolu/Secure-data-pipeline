
import math
import pandas as pd


def reconcile_counts(
    input_records,
    valid_records,
    rejected_records,
    published_records,
    validated_data=None,
    published_data=None
):
    report = {
        "input_records": input_records,
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "published_records": published_records
    }

    # 1. Input count reconciliation
    if input_records != valid_records + rejected_records:
        raise ValueError("Input reconciliation failed!")

    # 2. Publishing count reconciliation
    if valid_records != published_records:
        raise ValueError("Publishing reconciliation failed!")

    # 3. Data-level reconciliation
    if validated_data is not None or published_data is not None:

        if validated_data is None or published_data is None:
            raise ValueError(
                "Both validated_data and published_data are required!"
            )

        required_columns = {"customer_token", "annual_income"}

        if not required_columns.issubset(validated_data.columns):
            raise ValueError("Validated data is missing required columns!")

        if not required_columns.issubset(published_data.columns):
            raise ValueError("Published data is missing required columns!")

        if len(validated_data) != valid_records:
            raise ValueError("Validated dataset count mismatch!")

        if len(published_data) != published_records:
            raise ValueError("Published dataset count mismatch!")

        # 4. Check null and duplicate tokens in both datasets
        for name, dataset in [
            ("Validated", validated_data),
            ("Published", published_data)
        ]:
            tokens = dataset["customer_token"]

            if tokens.isna().any():
                raise ValueError(
                    f"{name} customer tokens contain null values!"
                )

            if tokens.duplicated().any():
                raise ValueError(
                    f"Duplicate customer tokens found in {name.lower()} data!"
                )

        # 5. Compare dataset schemas
        if set(validated_data.columns) != set(published_data.columns):
            raise ValueError(
                "Validated and published dataset columns do not match!"
            )

        # 6. Compare customer tokens
        validated_tokens = set(validated_data["customer_token"])
        published_tokens = set(published_data["customer_token"])

        if validated_tokens != published_tokens:
            raise ValueError(
                "Validated and published customer tokens do not match!"
            )

        # 7. Compare annual income totals
        validated_income = pd.to_numeric(
            validated_data["annual_income"],
            errors="coerce"
        )

        published_income = pd.to_numeric(
            published_data["annual_income"],
            errors="coerce"
        )

        if (
            validated_income.isna().any()
            or published_income.isna().any()
        ):
            raise ValueError("Invalid annual income values found!")

        validated_total = float(validated_income.sum())
        published_total = float(published_income.sum())

        if not math.isclose(
            validated_total,
            published_total,
            rel_tol=1e-9,
            abs_tol=0.01
        ):
            raise ValueError("Annual income reconciliation failed!")

        # 8. Compare every record
        columns = sorted(validated_data.columns)

        validated_sorted = (
            validated_data[columns]
            .sort_values("customer_token")
            .reset_index(drop=True)
        )

        published_sorted = (
            published_data[columns]
            .sort_values("customer_token")
            .reset_index(drop=True)
        )

        try:
            pd.testing.assert_frame_equal(
                validated_sorted,
                published_sorted,
                check_dtype=False,
                check_exact=False,
                rtol=1e-9,
                atol=0.01
            )
        except AssertionError as error:
            raise ValueError(
                "Record-level reconciliation failed! "
                "Published data differs from validated data."
            ) from error

        report["published_tokens_unique"] = True
        report["validated_income_total"] = validated_total
        report["published_income_total"] = published_total
        report["income_reconciliation"] = "passed"
        report["record_level_reconciliation"] = "passed"
        report["records_verified"] = len(published_data)

    report["reconciliation_status"] = "passed"

    return report
