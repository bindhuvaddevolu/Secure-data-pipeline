
import os
import random
import pandas as pd

from faker import Faker


def generate_dataset(
    num_records=20,
    seed=42,
    include_edge_cases=True
):
    """
    Generate synthetic customer data.

    Parameters:
        num_records: Number of normal customer records.
        seed: Random seed for reproducibility.
        include_edge_cases: Whether to add invalid records
                            and duplicate records.

    Returns:
        customers_df: Generated customer dataset.
        labels_df: Separate expected issue labels.
    """

    if num_records < 1:
        raise ValueError("num_records must be at least 1")

    # Initialize random generators
    fake = Faker("en_IN")
    fake.seed_instance(seed)

    rng = random.Random(seed)

    customers = []
    expected_labels = []

    # Generate normal customer records
    for i in range(1, num_records + 1):

        customer = {
            "customer_id": f"CUST{i:06d}",
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.numerify("9#########"),
            "age": rng.randint(18, 80),
            "city": fake.city(),
            "annual_income": rng.randint(200000, 2000000),
            "registration_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            ).isoformat()
        }

        customers.append(customer)

    # Add deliberately generated edge cases
    if include_edge_cases:

        # Edge case 1: Duplicate customer ID
        duplicate = customers[0].copy()
        customers.append(duplicate)
        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "duplicate_customer_id"
        })

        # Edge case 2: Missing required email
        missing_email = customers[1].copy()
        missing_email["customer_id"] = f"CUST{num_records + 1:06d}"
        missing_email["email"] = None
        customers.append(missing_email)
        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "missing_email"
        })

        # Edge case 3: Invalid age
        invalid_age = customers[2].copy()
        invalid_age["customer_id"] = f"CUST{num_records + 2:06d}"
        invalid_age["age"] = 150
        customers.append(invalid_age)
        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "invalid_age"
        })

        # Edge case 4: Malformed email
        invalid_email = customers[3].copy()
        invalid_email["customer_id"] = f"CUST{num_records + 3:06d}"
        invalid_email["email"] = "invalid-email"
        customers.append(invalid_email)
        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "malformed_email"
        })

    customers_df = pd.DataFrame(customers)

    # Assign source row numbers for traceability
    customers_df.insert(
        0,
        "source_row_number",
        range(1, len(customers_df) + 1)
    )

    labels_df = pd.DataFrame(
        expected_labels,
        columns=["row_number", "expected_issue"]
    )

    return customers_df, labels_df



def save_dataset(customers_df, labels_df):
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent

    input_folder = project_root / "data" / "input"
    input_folder.mkdir(parents=True, exist_ok=True)

    customers_df.to_csv(
        input_folder / "customers.csv",
        index=False
    )

    labels_df.to_csv(
        input_folder / "expected_labels.csv",
        index=False
    )

    print("Dataset saved successfully!")


if __name__ == "__main__":

    save_dataset(
        num_records=20,
        seed=42
    )
