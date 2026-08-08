"""
Dynamic Company Lookup Service.

Searches Finnhub for a company and selects
the most appropriate stock symbol.
"""

import os

import requests
from dotenv import load_dotenv


# ======================================================
# Configuration
# ======================================================

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


# ======================================================
# Company Lookup
# ======================================================

def get_stock_symbol(company: str):
    """
    Search Finnhub and return the best matching stock symbol.

    Preference:
        1. Indian NSE (.NS) symbol
        2. Exact symbol/company match
        3. First available result
    """

    if not company or not company.strip():
        return None

    if not FINNHUB_API_KEY:
        print("❌ FINNHUB_API_KEY not found.")
        return None

    url = "https://finnhub.io/api/v1/search"

    params = {
        "q": company.strip(),
        "token": FINNHUB_API_KEY,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        # Handle HTTP errors
        if response.status_code != 200:
            print(
                f"❌ Company lookup failed: "
                f"HTTP {response.status_code}"
            )
            return None

        data = response.json()

    except requests.RequestException as error:
        print(
            f"❌ Company lookup request failed: "
            f"{error}"
        )
        return None

    except ValueError:
        print("❌ Invalid response received from Finnhub.")
        return None

    results = data.get("result", [])

    if not results:
        return None

    # ==================================================
    # 1. Prefer Indian NSE (.NS)
    # ==================================================

    nse_results = [
        result
        for result in results
        if result.get("symbol", "").upper().endswith(".NS")
    ]

    if nse_results:
        return nse_results[0]["symbol"]

    # ==================================================
    # 2. Look for exact symbol match
    # ==================================================

    company_upper = company.strip().upper()

    for result in results:

        symbol = result.get("symbol", "").upper()

        if symbol == company_upper:
            return result["symbol"]

    # ==================================================
    # 3. Fall back to first result
    # ==================================================

    return results[0].get("symbol")


# ======================================================
# Manual Test
# ======================================================

if __name__ == "__main__":

    company = input("Enter Company Name: ")

    symbol = get_stock_symbol(company)

    print(f"\nStock Symbol : {symbol}")