"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    headline: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Financial news headline",
        example="Apple reports record quarterly profits.",
    )


class PredictionResponse(BaseModel):
    prediction: str