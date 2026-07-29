"""
Module for loading the financial news dataset.
"""

from pathlib import Path

import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the financial news dataset from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the dataset.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(
    path,
    header=None,
    names=["Sentiment", "Headline"],
    encoding="latin-1",
)

    return df