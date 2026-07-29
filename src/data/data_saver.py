"""
Module for saving processed datasets.
"""

from pathlib import Path

import pandas as pd


def save_dataset(df: pd.DataFrame, output_path: str) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df: Dataset to save.
        output_path: Destination CSV file.
    """
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    print("\n" + "=" * 40)
    print("DATASET SAVED")
    print("=" * 40)
    print(f"Location: {path}")