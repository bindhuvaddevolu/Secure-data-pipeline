
from pathlib import Path
import sqlite3
import pandas as pd


def publish_data(df, database_path):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    if df["customer_token"].duplicated().any():
        raise ValueError("Duplicate customer tokens found!")

    with sqlite3.connect(database_path) as connection:
        df.to_sql(
            "analytical_customers",
            connection,
            if_exists="replace",
            index=False
        )

        count = connection.execute(
            "SELECT COUNT(*) FROM analytical_customers"
        ).fetchone()[0]

        if count != len(df):
            raise RuntimeError(
                "Publishing verification failed!"
            )

    return count
