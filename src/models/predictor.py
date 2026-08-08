"""
Module for predicting the sentiment of a financial headline.
"""

from pathlib import Path
import joblib


# --------------------------------------------------
# Model Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"


# --------------------------------------------------
# Model Files
# --------------------------------------------------

MODEL_PATH = MODEL_DIR / "sentiment_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"


# --------------------------------------------------
# Validate Model Files
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Sentiment model not found: {MODEL_PATH}"
    )

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        f"TF-IDF vectorizer not found: {VECTORIZER_PATH}"
    )

if not ENCODER_PATH.exists():
    raise FileNotFoundError(
        f"Label encoder not found: {ENCODER_PATH}"
    )


# --------------------------------------------------
# Load Model Components
# --------------------------------------------------

print("Loading sentiment model...")

model = joblib.load(MODEL_PATH)

print("Loading TF-IDF vectorizer...")

vectorizer = joblib.load(VECTORIZER_PATH)

print("Loading label encoder...")

encoder = joblib.load(ENCODER_PATH)

print("✓ Sentiment model loaded successfully.")


# --------------------------------------------------
# Predict Sentiment
# --------------------------------------------------

def predict_sentiment(headline: str) -> str:
    """
    Predict sentiment for a financial headline.
    """

    if not headline:
        return "neutral"

    # Convert headline into TF-IDF features
    transformed = vectorizer.transform(
        [headline]
    )

    # Predict encoded sentiment
    prediction = model.predict(
        transformed
    )

    # Convert encoded value back to label
    sentiment = encoder.inverse_transform(
        prediction
    )

    return str(sentiment[0])
