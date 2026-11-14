
import os
import hmac
import hashlib
from pathlib import Path
import json

import pandas as pd


def get_secret_key():
    """
    Read tokenization secret from environment variable.
    Never hardcode production secrets in source code.
    """

    secret = os.environ.get("PIPELINE_TOKEN_SECRET")

    if not secret or len(secret) < 32:
        raise ValueError(
            "PIPELINE_TOKEN_SECRET must contain "
            "at least 32 characters."
        )

    return secret.encode("utf-8")


def tokenize_customer_id(customer_id, secret_key):
    """
    Generate a deterministic HMAC-SHA256 token.
    """

    if pd.isna(customer_id):
        raise ValueError("Customer ID cannot be null")

    token = hmac.new(
        secret_key,
        str(customer_id).encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return token


def mask_name(name):
    """
    Mask customer name.
    Example: Ravi Kumar -> R***
    """

    if pd.isna(name):
        return None

    name = str(name).strip()

    if not name:
        return None

    return name[0].upper() + "***"


def mask_email(email):
    """
    Mask email while preserving its domain.
    Example: ravi@gmail.com -> r***@gmail.com
    """

    if pd.isna(email):
        return None

    email = str(email).strip()

    if "@" not in email:
        return "***"

    local_part, domain = email.split("@", 1)

    if not local_part or not domain:
        return "***"

    return local_part[0] + "***@" + domain


def mask_phone(phone):
    """
    Show only the last four digits.
    """

    if pd.isna(phone):
        return None

    phone = str(phone).strip()

    if len(phone) < 4:
        return "*" * len(phone)

    return "*" * (len(phone) - 4) + phone[-4:]



import json
from pathlib import Path


def apply_privacy_transformations(df, secret_key, config_path=None):
    project_root = Path(__file__).resolve().parent.parent

    if config_path is None:
        config_path = project_root / "config" / "privacy_rules.json"

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    result = df.copy()

    # Tokenization
    token_config = config["tokenization"]

    if token_config["enabled"]:
        source = token_config["source_column"]
        output = token_config["output_column"]

        if source not in result.columns:
            raise ValueError(f"Missing column: {source}")

        result[output] = result[source].apply(
            lambda value: tokenize_customer_id(value, secret_key)
        )

    # Configurable masking
    masking_functions = {
        "mask_name": mask_name,
        "mask_email": mask_email,
        "mask_phone": mask_phone
    }

    for column, rules in config["masking"].items():
        if not rules["enabled"]:
            continue

        if column not in result.columns:
            raise ValueError(f"Missing column: {column}")

        method = rules["method"]

        if method not in masking_functions:
            raise ValueError(f"Unsupported masking method: {method}")

        output_column = rules["output_column"]
        masking_function = masking_functions[method]

        result[output_column] = result[column].apply(
            masking_function
        )

    # Remove original sensitive fields
    columns_to_drop = config["drop_original_columns"]

    result = result.drop(
        columns=columns_to_drop,
        errors="ignore"
    )

    return result

if __name__ == "__main__":

    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root
        / "data"
        / "quarantine"
        / "valid_records.csv"
    )

    output_file = (
        project_root
        / "data"
        / "output"
        / "masked_customers.csv"
    )

    # Load validated records
    df = pd.read_csv(input_file)

    # Get secret key
    secret_key = get_secret_key()

    # Apply privacy transformations
    masked_df = apply_privacy_transformations(
        df,
        secret_key
    )

    # Create output directory
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save transformed dataset
    masked_df.to_csv(
        output_file,
        index=False
    )

    print("Privacy transformation completed!")
    print(f"Input records: {len(df)}")
    print(f"Output records: {len(masked_df)}")
    print(f"Output file: {output_file}")

    print("\nMasked dataset preview:")
    print(masked_df.head().to_string(index=False))
