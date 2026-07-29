"""
Module for saving trained machine learning models.
"""

from pathlib import Path
import joblib


def save_model(model, vectorizer, encoder) -> None:
    """
    Save the trained model, vectorizer and label encoder.
    """

    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    joblib.dump(model, model_dir / "sentiment_model.pkl")
    joblib.dump(vectorizer, model_dir / "tfidf_vectorizer.pkl")
    joblib.dump(encoder, model_dir / "label_encoder.pkl")

    print("\n" + "=" * 40)
    print("MODEL SAVED")
    print("=" * 40)
    print(f"Location: {model_dir.resolve()}")