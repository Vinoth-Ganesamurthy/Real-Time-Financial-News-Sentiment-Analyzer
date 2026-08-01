"""
NewsAPI Service
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(company: str):
    """
    Fetch news from NewsAPI.
    Used as a fallback when Finnhub has no articles.
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