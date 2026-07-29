"""
Module for analysing the most frequent words in financial headlines.
"""

from collections import Counter
from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords


def analyse_word_frequency(df: pd.DataFrame) -> None:
    """
    Display and plot the most common words in financial news headlines.
    """

    stop_words = set(stopwords.words("english"))

    all_words = []

    for headline in df["Headline"]:
        headline = headline.lower()

        headline = re.sub(r"[^a-zA-Z\s]", "", headline)

        words = headline.split()

        words = [word for word in words if word not in stop_words]

        all_words.extend(words)

    word_counts = Counter(all_words)

    print("\n" + "=" * 40)
    print("TOP 20 MOST FREQUENT WORDS")
    print("=" * 40)

    top_words = word_counts.most_common(20)

    for word, count in top_words:
        print(f"{word:<20} {count}")

    # -----------------------------
    # Create Bar Chart
    # -----------------------------

    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]

    output_dir = Path("outputs/charts")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))

    plt.bar(words, counts)

    plt.title("Top 20 Most Frequent Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    output_path = output_dir / "top_20_words.png"

    plt.savefig(output_path, dpi=300)

    plt.close()

    print("\n" + "=" * 40)
    print("TOP 20 WORDS CHART SAVED")
    print("=" * 40)
    print(f"Location: {output_path}")