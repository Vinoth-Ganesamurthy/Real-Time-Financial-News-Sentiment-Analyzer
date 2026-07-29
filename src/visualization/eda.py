"""
Module for exploratory data analysis (EDA).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_sentiment_distribution(df: pd.DataFrame) -> None:
    """
    Plot and save the sentiment distribution.

    Args:
        df: Cleaned financial news dataset.
    """
    sentiment_counts = df["Sentiment"].value_counts()

    output_dir = Path("outputs/charts")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    sentiment_counts.plot(kind="bar")

    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Headlines")

    plt.tight_layout()

    output_file = output_dir / "sentiment_distribution.png"

    plt.savefig(output_file)

    plt.close()

    print("\n" + "=" * 40)
    print("CHART SAVED")
    print("=" * 40)
    print(f"Location: {output_file}")