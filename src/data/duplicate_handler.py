"""
Module for inspecting and removing duplicate records.
"""

import pandas as pd


def inspect_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Display duplicate rows in the dataset.

    Args:
        df: Financial news dataset.

    Returns:
        DataFrame containing duplicate rows.
    """
    duplicates = df[df.duplicated()]

    print("\n" + "=" * 40)
    print("DUPLICATE RECORDS")
    print("=" * 40)

    print(f"Number of duplicate rows: {len(duplicates)}")

    if duplicates.empty:
        print("No duplicate rows found.")
    else:
        print("\nDuplicate Records:\n")
        print(duplicates)

    return duplicates


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the dataset.

    Args:
        df: Financial news dataset.

    Returns:
        Dataset with duplicate rows removed.
    """
    rows_before = len(df)

    cleaned_df = df.drop_duplicates().copy()

    rows_after = len(cleaned_df)

    duplicates_removed = rows_before - rows_after

    print("\n" + "=" * 40)
    print("DUPLICATE REMOVAL REPORT")
    print("=" * 40)
    print(f"Rows Before        : {rows_before}")
    print(f"Duplicates Removed : {duplicates_removed}")
    print(f"Rows After         : {rows_after}")

    return cleaned_df