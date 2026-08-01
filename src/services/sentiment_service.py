"""
Service for analyzing the sentiment of news articles.
"""

from datetime import datetime
from src.models.predictor import predict_sentiment


def analyze_articles(articles):
    """
    Analyze sentiment for news articles from either
    Finnhub or NewsAPI.
    """

    results = []

    positive = 0
    neutral = 0
    negative = 0

    for article in articles:

        # ----------------------------
        # Finnhub Response
        # ----------------------------
        if "headline" in article:

            headline = article.get("headline", "")
            source = article.get("source", "")
            published = datetime.fromtimestamp(
                article.get("datetime", 0)
            ).strftime("%Y-%m-%d %H:%M")
            url = article.get("url", "")
            summary = article.get("summary", "")

        # ----------------------------
        # NewsAPI Response
        # ----------------------------
        else:

            headline = article.get("title", "")
            source = article.get("source", {}).get("name", "")
            published = article.get("publishedAt", "")
            url = article.get("url", "")
            summary = article.get("description", "")

        # Predict sentiment
        sentiment = predict_sentiment(headline)

        if sentiment.lower() == "positive":
            positive += 1
        elif sentiment.lower() == "negative":
            negative += 1
        else:
            neutral += 1

        results.append(
            {
                "headline": headline,
                "source": source,
                "published": published,
                "url": url,
                "summary": summary,
                "sentiment": sentiment,
            }
        )

    return {
        "articles": results,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }