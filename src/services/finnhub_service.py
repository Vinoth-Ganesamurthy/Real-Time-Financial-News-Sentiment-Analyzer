"""
Finnhub News Service
"""

import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


def fetch_news(symbol: str):

    today = datetime.date.today()
    from_date = today - datetime.timedelta(days=30)

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d"),
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(url, params=params)

    data = response.json()

    if isinstance(data, list):
     return data[:5]

    return []