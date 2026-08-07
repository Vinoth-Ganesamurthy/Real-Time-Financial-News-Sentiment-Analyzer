"""
Service for analyzing the sentiment of news articles.
"""

from datetime import datetime
import re

from src.models.predictor import predict_sentiment


def normalize_headline(headline: str) -> str:
    """
    Normalize a headline so that minor formatting differences
    do not cause duplicate articles to be treated as separate.
    """

    if not headline:
        return ""

    headline = headline.lower().strip()

    # Remove punctuation
    headline = re.sub(r"[^\w\s]", "", headline)

    # Remove extra spaces
    headline = re.sub(r"\s+", " ", headline)

    return headline


def analyze_articles(articles):
    """
    Analyze sentiment for news articles from either
    Finnhub or NewsAPI.

    Duplicate articles are removed before sentiment analysis.
    """

    results = []

    positive = 0
    neutral = 0
    negative = 0

    # Track already-seen articles
    seen_urls = set()
    seen_headlines = set()

    for article in articles:

        # -------------------------------------------------
        # Finnhub Response
        # -------------------------------------------------

        if "headline" in article:

            headline = article.get("headline", "")
            source = article.get("source", "")

            timestamp = article.get("datetime", 0)

            if timestamp:
                published = datetime.fromtimestamp(timestamp).strftime(
                    "%Y-%m-%d %H:%M"
                )
            else:
                published = ""

            url = article.get("url", "")
            summary = article.get("summary", "")

        # -------------------------------------------------
        # NewsAPI Response
        # -------------------------------------------------

        else:

            headline = article.get("title", "")
            source = article.get("source", {}).get("name", "")
            published = article.get("publishedAt", "")
            url = article.get("url", "")
            summary = article.get("description", "")

        # -------------------------------------------------
        # Duplicate Detection
        # -------------------------------------------------

        normalized_headline = normalize_headline(headline)

        # First priority: exact URL
        if url and url in seen_urls:
            continue

        # Second priority: normalized headline
        if normalized_headline and normalized_headline in seen_headlines:
            continue

        # Remember this article
        if url:
            seen_urls.add(url)

        if normalized_headline:
            seen_headlines.add(normalized_headline)

        # -------------------------------------------------
        # Sentiment Prediction
        # -------------------------------------------------

        sentiment = predict_sentiment(headline)

        sentiment_lower = sentiment.lower()

        if sentiment_lower == "positive":
            positive += 1

        elif sentiment_lower == "negative":
            negative += 1

        else:
            neutral += 1

        # -------------------------------------------------
        # Store Clean Article
        # -------------------------------------------------

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

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return {
        "articles": results,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }