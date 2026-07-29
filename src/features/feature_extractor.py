"""
Module for extracting text features.
"""

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_bow_features(df: pd.DataFrame):
    """
    Convert headlines into Bag of Words features.
    """

    vectorizer = CountVectorizer()

    X = vectorizer.fit_transform(df["Headline"])

    print("\n" + "=" * 40)
    print("BAG OF WORDS")
    print("=" * 40)

    print(f"Vocabulary Size : {len(vectorizer.vocabulary_)}")
    print(f"Feature Matrix  : {X.shape}")

    return X, vectorizer

def extract_tfidf_features(df: pd.DataFrame):
    """
    Convert headlines into TF-IDF features.
    """

    vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
)
    X = vectorizer.fit_transform(df["Headline"])

    print("\n" + "=" * 40)
    print("TF-IDF FEATURES")
    print("=" * 40)

    print(f"Vocabulary Size : {len(vectorizer.vocabulary_)}")
    print(f"Feature Matrix  : {X.shape}")

    return X, vectorizer
