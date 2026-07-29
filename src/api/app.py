"""
FastAPI application for Financial News Sentiment Analysis.
"""

from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    PredictionRequest,
    PredictionResponse,
)
from src.models.predictor import predict_sentiment

app = FastAPI(
    title="Financial News Sentiment API",
    description="Predict the sentiment of financial news headlines using a trained Machine Learning model.",
    version="1.0.0",
)


@app.get("/")
def home():
    """Health check endpoint."""
    return {
        "status": "success",
        "message": "Financial News Sentiment API is running!"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):
    """Predict sentiment from a financial news headline."""

    try:
        prediction = predict_sentiment(request.headline)

        return PredictionResponse(
            prediction=prediction
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )