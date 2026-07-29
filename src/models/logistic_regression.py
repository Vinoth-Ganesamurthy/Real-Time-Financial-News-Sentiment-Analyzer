"""
Module for training a Logistic Regression model.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def train_logistic_regression(X, df):
    """
    Train a Logistic Regression model.
    """

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["Sentiment"])

    print("\n" + "=" * 40)
    print("LABEL ENCODING")
    print("=" * 40)
    print("Classes:", list(encoder.classes_))

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("\n" + "=" * 40)
    print("TRAIN TEST SPLIT")
    print("=" * 40)
    print(f"Training Samples : {X_train.shape[0]}")
    print(f"Testing Samples  : {X_test.shape[0]}")

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train, y_train)

    print("\n" + "=" * 40)
    print("LOGISTIC REGRESSION TRAINED")
    print("=" * 40)

    return model, encoder, X_test, y_test