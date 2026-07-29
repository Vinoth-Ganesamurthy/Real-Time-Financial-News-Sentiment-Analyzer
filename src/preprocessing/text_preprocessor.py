"""
Module for preprocessing financial news headlines.
"""

import re

import pandas as pd


def clean_headline(text: str) -> str:
    """
    Clean a single news headline.

    Args:
        text: Raw news headline.

    Returns:
        Cleaned news headline.
    """
    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text


def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply preprocessing to all headlines.

    Args:
        df: Financial news dataset.

    Returns:
        Preprocessed DataFrame.
    """
    processed_df = df.copy()

    processed_df["Headline"] = processed_df["Headline"].apply(clean_headline)

    return processed_df