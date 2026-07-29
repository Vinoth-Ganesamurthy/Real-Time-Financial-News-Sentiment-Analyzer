"""
Module for analysing headline lengths.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def analyse_headline_lengths(df: pd.DataFrame) -> None:
    """
    Analyse the length of financial news headlines.
    """

    headline_lengths = df["Headline"].str.split().str.len()

    print("\n" + "=" * 40)
    print("HEADLINE LENGTH ANALYSIS")
    print("=" * 40)

    print(f"Average headline length : {headline_lengths.mean():.2f} words")
    print(f"Shortest headline       : {headline_lengths.min()} words")
    print(f"Longest headline        : {headline_lengths.max()} words")

    output_dir = Path("outputs/charts")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.hist(
        headline_lengths,
        bins=20,
        edgecolor="black",
    )

    plt.title("Headline Length Distribution")
    plt.xlabel("Number of Words")
    plt.ylabel("Number of Headlines")

    plt.tight_layout()

    output_path = output_dir / "headline_length_distribution.png"

    plt.savefig(output_path, dpi=300)
    plt.close()

    print("\n" + "=" * 40)
    print("HEADLINE LENGTH CHART SAVED")
    print("=" * 40)
    print(f"Location: {output_path}")