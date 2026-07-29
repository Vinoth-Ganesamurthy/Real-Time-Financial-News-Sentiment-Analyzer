"""
Module for training a Multinomial Naive Bayes model.
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB


def train_naive_bayes(X, df):
    """
    Train a Multinomial Naive Bayes model.
    """

    # Encode labels
    encoder = LabelEncoder()
    y = encoder.fit_transform(df["Sentiment"])

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Train model
    model = MultinomialNB()

    model.fit(X_train, y_train)

    print("\n" + "=" * 40)
    print("NAIVE BAYES TRAINED")
    print("=" * 40)

    return model, encoder, X_test, y_test