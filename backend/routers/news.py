from fastapi import APIRouter, HTTPException

from backend.schemas.news_response import (
    NewsResponse,
    Article,
    SentimentSummary,
)

from src.services.news_service import fetch_news
from src.services.sentiment_service import analyze_articles

router = APIRouter(
    prefix="/news",
    tags=["Financial News"],
)


@router.get("/{company}", response_model=NewsResponse)
def get_news(company: str):

    articles = fetch_news(company)

    if not articles:
        raise HTTPException(
            status_code=404,
            detail="No news found for this company."
        )

    results = analyze_articles(articles)

    response_articles = [
        Article(**article)
        for article in results["articles"]
    ]

    return NewsResponse(
        company=company,
        total_articles=len(response_articles),
        summary=SentimentSummary(
            positive=results["positive"],
            neutral=results["neutral"],
            negative=results["negative"],
        ),
        articles=response_articles,
    )