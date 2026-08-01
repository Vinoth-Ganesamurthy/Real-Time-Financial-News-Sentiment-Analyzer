"""
Dynamic Company Lookup Service.

This service will search for companies
and return their stock symbols.
"""

"""
Dynamic Company Lookup Service using Finnhub.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


def get_stock_symbol(company: str):
    """
    Search Finnhub and return the best matching stock symbol.
    """

    url = "https://finnhub.io/api/v1/search"

    params = {
        "q": company,
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(url, params=params)

    data = response.json()

    results = data.get("result", [])

    if not results:
        return None

    return results[0]["symbol"]

if __name__ == "__main__":

    company = input("Enter Company Name: ")

    symbol = get_stock_symbol(company)

    print(f"\nStock Symbol : {symbol}")