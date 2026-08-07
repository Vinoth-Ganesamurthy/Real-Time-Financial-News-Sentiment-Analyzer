"""
Stock Quote Service

Fetches the latest stock quote from Finnhub.
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


def fetch_stock_quote(symbol: str):
    """
    Fetch the latest stock quote for a stock symbol.
    """

    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "symbol": symbol,
        "current_price": data.get("c"),
        "change": data.get("d"),
        "change_percent": data.get("dp"),
        "day_high": data.get("h"),
        "day_low": data.get("l"),
        "previous_close": data.get("pc"),
    }