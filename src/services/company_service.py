"""
Dynamic Company Lookup Service.

Searches Finnhub for a company and selects
the most appropriate stock symbol.

Also supports common aliases for companies
across US, India, Singapore, and Australia.
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
# Known Company Aliases
# ======================================================

COMPANY_ALIASES = {
    # --------------------------
    # United States
    # --------------------------
    "tesla": "TSLA",
    "tesla inc": "TSLA",
    "nvidia": "NVDA",
    "nvidia corporation": "NVDA",
    "apple": "AAPL",
    "apple inc": "AAPL",
    "microsoft": "MSFT",
    "microsoft corporation": "MSFT",
    "amazon": "AMZN",
    "amazon.com": "AMZN",
    "meta": "META",
    "meta platforms": "META",
    "alphabet": "GOOGL",
    "google": "GOOGL",

    # --------------------------
    # India
    # --------------------------
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",
    "reliance industries limited": "RELIANCE.NS",

    "infosys": "INFY.NS",
    "infosys limited": "INFY.NS",

    "tcs": "TCS.NS",
    "tata consultancy services": "TCS.NS",

    "hdfc bank": "HDFCBANK.NS",
    "hdfc bank limited": "HDFCBANK.NS",

    "icici bank": "ICICIBANK.NS",
    "icici bank limited": "ICICIBANK.NS",

    "itc": "ITC.NS",
    "itc limited": "ITC.NS",

    # --------------------------
    # Singapore
    # --------------------------
    "dbs": "D05.SI",
    "dbs group": "D05.SI",
    "dbs group holdings": "D05.SI",
    "dbs bank": "D05.SI",

    "singapore technologies engineering": "S63.SI",
    "singapore technologies engineering ltd": "S63.SI",
    "st engineering": "S63.SI",

    # --------------------------
    # Australia
    # --------------------------
    "commonwealth bank": "CBA.AX",
    "commonwealth bank of australia": "CBA.AX",
    "cba": "CBA.AX",

    "bhp": "BHP.AX",
    "bhp group": "BHP.AX",

    "westpac": "WBC.AX",
    "westpac banking corporation": "WBC.AX",
}


# ======================================================
# Company Lookup
# ======================================================

def get_stock_symbol(company: str):
    """
    Return the best matching stock symbol.

    Lookup order:
        1. Known company aliases
        2. Finnhub search
        3. Preferred exchange-specific result
        4. Exact symbol match
        5. First available result
    """

    if not company or not company.strip():
        return None

    company_clean = company.strip()
    company_key = company_clean.lower()

    # ==================================================
    # 1. Known aliases
    # ==================================================

    if company_key in COMPANY_ALIASES:
        return COMPANY_ALIASES[company_key]

    # ==================================================
    # 2. Finnhub fallback
    # ==================================================

    if not FINNHUB_API_KEY:
        print("❌ FINNHUB_API_KEY not found.")
        return None

    url = "https://finnhub.io/api/v1/search"

    params = {
        "q": company_clean,
        "token": FINNHUB_API_KEY,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

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
        print(
            "❌ Invalid response received from Finnhub."
        )
        return None

    results = data.get("result", [])

    if not results:
        return None

    # ==================================================
    # 3. Prefer common supported exchanges
    # ==================================================

    preferred_suffixes = [
        ".NS",
        ".SI",
        ".AX",
    ]

    for suffix in preferred_suffixes:

        matching_results = [
            result
            for result in results
            if result.get(
                "symbol",
                ""
            ).upper().endswith(suffix)
        ]

        if matching_results:
            return matching_results[0].get(
                "symbol"
            )

    # ==================================================
    # 4. Exact symbol match
    # ==================================================

    company_upper = company_clean.upper()

    for result in results:

        symbol = result.get(
            "symbol",
            ""
        ).upper()

        if symbol == company_upper:
            return result.get("symbol")

    # ==================================================
    # 5. Fall back to first result
    # ==================================================

    return results[0].get("symbol")


# ======================================================
# Manual Test
# ======================================================

if __name__ == "__main__":

    company = input(
        "Enter Company Name: "
    )

    symbol = get_stock_symbol(company)

    print(
        f"\nStock Symbol : {symbol}"
    )