"""
Service for fetching financial news from NewsAPI.
"""

import os
import requests

from dotenv import load_dotenv
from src.models.predictor import predict_sentiment

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(company: str):
    """
    Fetch the latest financial news for a company.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data.get("articles", [])


if __name__ == "__main__":

    articles = fetch_news("Apple")

    print(f"\nFound {len(articles)} articles.\n")

    for article in articles:

        headline = article["title"]

        sentiment = predict_sentiment(headline)

        print("=" * 80)
        print(f"Title      : {headline}")
        print(f"Source     : {article['source']['name']}")
        print(f"Published  : {article['publishedAt']}")
        print(f"Sentiment  : {sentiment}")