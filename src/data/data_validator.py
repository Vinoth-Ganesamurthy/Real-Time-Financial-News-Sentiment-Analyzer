"""
Module for validating the financial news dataset.
"""

import pandas as pd


def validate_dataset(df: pd.DataFrame) -> None:
    """
    Print a validation report for the dataset.

    Args:
        df: Financial news dataset.
    """
    print("\n" + "=" * 40)
    print("DATASET VALIDATION REPORT")
    print("=" * 40)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names")
    print("-" * 20)
    for column in df.columns:
        print(column)

    print("\nMissing Values")
    print("-" * 20)
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print("-" * 20)
    print(df.duplicated().sum())

    print("\nData Types")
    print("-" * 20)
    print(df.dtypes)

    print("\nSentiment Distribution")
    print("-" * 20)
    print(df["Sentiment"].value_counts())