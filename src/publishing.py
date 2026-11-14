
from pathlib import Path
import sqlite3
import pandas as pd


def publish_data(df, database_path):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    target_table = "analytical_customers"
    staging_table = "analytical_customers_staging"

    # Validate required column
    if "customer_token" not in df.columns:
        raise ValueError("customer_token column is missing!")

    # Reject empty data
    if df.empty:
        raise ValueError("Cannot publish an empty dataset!")

    # Reject null tokens
    if df["customer_token"].isnull().any():
        raise ValueError("Null customer tokens found!")

    # Reject duplicate tokens
    if df["customer_token"].duplicated().any():
        raise ValueError("Duplicate customer tokens found!")

    connection = sqlite3.connect(database_path)

    try:
        # Step 1: Load data into staging table
        df.to_sql(
            staging_table,
            connection,
            if_exists="replace",
            index=False
        )

        # Step 2: Verify staging records
        staging_count = connection.execute(
            f"SELECT COUNT(*) FROM {staging_table}"
        ).fetchone()[0]

        if staging_count != len(df):
            raise RuntimeError("Staging verification failed!")

        # Step 3: Atomically replace target table
        connection.execute("BEGIN IMMEDIATE")

        connection.execute(
            f"DROP TABLE IF EXISTS {target_table}"
        )

        connection.execute(
            f"ALTER TABLE {staging_table} RENAME TO {target_table}"
        )

        connection.commit()

        # Step 4: Verify final published records
        published_count = connection.execute(
            f"SELECT COUNT(*) FROM {target_table}"
        ).fetchone()[0]

        if published_count != len(df):
            raise RuntimeError("Publishing verification failed!")

        return published_count

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
