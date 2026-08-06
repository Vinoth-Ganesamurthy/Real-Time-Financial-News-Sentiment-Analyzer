"""
NewsAPI Service
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(company: str, limit: int = 5):
    """
    Fetch news from NewsAPI.
    Used as a fallback when Finnhub has no articles.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    return data.get("articles", [])