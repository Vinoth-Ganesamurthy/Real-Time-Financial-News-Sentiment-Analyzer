"""
Module for predicting the sentiment of a financial headline.
"""

from pathlib import Path
import joblib

MODEL_DIR = Path("models")

model = joblib.load(
    MODEL_DIR / "sentiment_model.pkl"
)

vectorizer = joblib.load(
    MODEL_DIR / "tfidf_vectorizer.pkl"
)

encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)

def predict_sentiment(headline: str) -> str:
    """
    Predict sentiment for a financial headline.
    """

    transformed = vectorizer.transform([headline])

    prediction = model.predict(transformed)

    sentiment = encoder.inverse_transform(prediction)

    return sentiment[0]

