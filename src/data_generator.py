
import random
from pathlib import Path

import pandas as pd
from faker import Faker


def generate_dataset(
    num_records=20,
    seed=42,
    include_edge_cases=True
):
    """
    Generate reproducible synthetic customer data.
    Faker values are generated in batches and reused
    to improve large dataset generation performance.
    """

    if num_records < 1:
        raise ValueError("num_records must be at least 1")

    fake = Faker("en_IN")
    fake.seed_instance(seed)
    rng = random.Random(seed)

    # Generate reusable Faker value pools
    pool_size = min(num_records, 1000)

    name_pool = [fake.name() for _ in range(pool_size)]
    email_pool = [fake.email() for _ in range(pool_size)]
    phone_pool = [
        fake.numerify("9#########")
        for _ in range(pool_size)
    ]
    city_pool = [fake.city() for _ in range(pool_size)]
    date_pool = [
        fake.date_between(
            start_date="-3y",
            end_date="today"
        ).isoformat()
        for _ in range(pool_size)
    ]

    # Generate records
    customers = []

    for i in range(1, num_records + 1):
        customer = {
            "customer_id": f"CUST{i:06d}",
            "full_name": rng.choice(name_pool),
            "email": rng.choice(email_pool),
            "phone": rng.choice(phone_pool),
            "age": rng.randint(18, 80),
            "city": rng.choice(city_pool),
            "annual_income": rng.randint(200000, 2000000),
            "registration_date": rng.choice(date_pool)
        }

        customers.append(customer)

    expected_labels = []

    if include_edge_cases:

        # Edge case 1: Duplicate customer ID
        duplicate = customers[0].copy()
        customers.append(duplicate)

        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "duplicate_customer_id"
        })

        # Edge case 2: Missing email
        missing_email = customers[1 % num_records].copy()
        missing_email["customer_id"] = (
            f"CUST{num_records + 1:06d}"
        )
        missing_email["email"] = None
        customers.append(missing_email)

        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "missing_email"
        })

        # Edge case 3: Invalid age
        invalid_age = customers[2 % num_records].copy()
        invalid_age["customer_id"] = (
            f"CUST{num_records + 2:06d}"
        )
        invalid_age["age"] = 150
        customers.append(invalid_age)

        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "invalid_age"
        })

        # Edge case 4: Malformed email
        invalid_email = customers[3 % num_records].copy()
        invalid_email["customer_id"] = (
            f"CUST{num_records + 3:06d}"
        )
        invalid_email["email"] = "invalid-email"
        customers.append(invalid_email)

        expected_labels.append({
            "row_number": len(customers),
            "expected_issue": "malformed_email"
        })

    customers_df = pd.DataFrame(customers)

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
    customers_df, labels_df = generate_dataset(
        num_records=20,
        seed=42
    )
    save_dataset(customers_df, labels_df)
