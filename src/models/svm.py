"""
Module for training a Linear Support Vector Machine.
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


def train_svm(X, df):
    """
    Train a Linear SVM model.
    """

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["Sentiment"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = LinearSVC(
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train, y_train)

    print("\n" + "=" * 40)
    print("LINEAR SVM TRAINED")
    print("=" * 40)

    return model, encoder, X_test, y_test