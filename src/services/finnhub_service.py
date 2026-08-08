"""
Finnhub News Service

Fetches company news from Finnhub,
filters irrelevant headlines,
removes duplicates,
and returns the most relevant articles.
"""

import os
import requests
import datetime

from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


# --------------------------------------------------
# Company Terms
# --------------------------------------------------

def _get_company_terms(symbol: str):
    """
    Return company-related terms for headline matching.
    """

    symbol = symbol.strip().upper()

    company_terms = {
        "TSLA": [
            "tesla",
            "tsla",
        ],
        "NVDA": [
            "nvidia",
            "nvda",
        ],
        "RELIANCE.NS": [
            "reliance",
            "ril",
        ],
        "INFY.NS": [
            "infosys",
            "infy",
        ],
    }

    return company_terms.get(
        symbol,
        [symbol.split(".")[0].lower()]
    )


# --------------------------------------------------
# Headline Relevance
# --------------------------------------------------

def _headline_matches_company(
    article,
    symbol: str
):
    """
    Check whether the company is mentioned
    in the headline.
    """

    headline = (
        article.get("headline") or ""
    ).lower()

    terms = _get_company_terms(symbol)

    for term in terms:

        if term.lower() in headline:
            return True

    return False


# --------------------------------------------------
# Low Quality Headline Filter
# --------------------------------------------------

def _is_low_quality_headline(article):
    """
    Reject generic market-list headlines.
    """

    headline = (
        article.get("headline") or ""
    ).strip().lower()

    blocked_phrases = [
        "stocks to watch:",
        "stocks to watch -",
        "stocks to watch |",
        "stocks in focus:",
        "stocks in focus -",
        "stocks in focus |",
        "market today:",
        "stock market today",
    ]

    return any(
        phrase in headline
        for phrase in blocked_phrases
    )


# --------------------------------------------------
# Fetch News
# --------------------------------------------------

def fetch_news(
    symbol: str,
    limit: int = 5
):
    """
    Fetch and filter latest company news from Finnhub.
    """

    # --------------------------------------------------
    # Validate API Key
    # --------------------------------------------------

    if not FINNHUB_API_KEY:

        print(
            "❌ FINNHUB_API_KEY is missing."
        )

        return []


    # --------------------------------------------------
    # Date Range
    # --------------------------------------------------

    today = datetime.date.today()

    from_date = (
        today - datetime.timedelta(days=30)
    )


    # --------------------------------------------------
    # Finnhub API
    # --------------------------------------------------

    url = (
        "https://finnhub.io/api/v1/company-news"
    )

    params = {
        "symbol": symbol,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d"),
        "token": FINNHUB_API_KEY,
    }


    # --------------------------------------------------
    # Request
    # --------------------------------------------------

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )


        # --------------------------------------------------
        # HTTP Status
        # --------------------------------------------------

        print(
            f"Finnhub HTTP Status: "
            f"{response.status_code}"
        )


        # --------------------------------------------------
        # Handle API Errors
        # --------------------------------------------------

        if response.status_code != 200:

            print(
                f"❌ Finnhub request failed: "
                f"HTTP {response.status_code}"
            )

            # Print server response for debugging
            try:

                print(
                    "Finnhub response:"
                )

                print(
                    response.text[:500]
                )

            except Exception:

                pass

            return []


        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            data = response.json()

        except ValueError:

            print(
                "❌ Finnhub returned invalid JSON."
            )

            print(
                response.text[:500]
            )

            return []


        # --------------------------------------------------
        # Validate Response
        # --------------------------------------------------

        if not isinstance(data, list):

            print(
                "❌ Unexpected Finnhub response format."
            )

            print(
                data
            )

            return []


        print(
            f"Finnhub Articles Received: "
            f"{len(data)}"
        )


        # --------------------------------------------------
        # Filter Relevant Headlines
        # --------------------------------------------------

        relevant_articles = []


        for article in data:

            # Company relevance
            if not _headline_matches_company(
                article,
                symbol
            ):
                continue


            # Low-quality headline filter
            if _is_low_quality_headline(
                article
            ):
                continue


            relevant_articles.append(
                article
            )


        print(
            f"Finnhub Relevant Articles: "
            f"{len(relevant_articles)}"
        )


        # --------------------------------------------------
        # Remove Duplicates
        # --------------------------------------------------

        unique_articles = []

        seen_urls = set()
        seen_headlines = set()


        for article in relevant_articles:

            article_url = (
                article.get("url") or ""
            ).strip()

            headline = (
                article.get("headline") or ""
            ).strip().lower()


            # Ignore articles without URL
            if not article_url:
                continue


            # Ignore articles without headline
            if not headline:
                continue


            # Duplicate URL
            if article_url in seen_urls:
                continue


            # Duplicate headline
            if headline in seen_headlines:
                continue


            seen_urls.add(article_url)
            seen_headlines.add(headline)


            unique_articles.append(
                article
            )


        print(
            f"Finnhub Unique Articles: "
            f"{len(unique_articles)}"
        )


        # --------------------------------------------------
        # Selected Articles
        # --------------------------------------------------

        print(
            "\nFinnhub Selected Articles:"
        )


        for article in unique_articles[:limit]:

            print(
                "-",
                article.get("headline")
            )


        return unique_articles[:limit]


    # --------------------------------------------------
    # Request Error
    # --------------------------------------------------

    except requests.exceptions.RequestException as e:

        print(
            f"❌ Finnhub request failed: {e}"
        )

        return []


    # --------------------------------------------------
    # Unexpected Error
    # --------------------------------------------------

    except Exception as e:

        print(
            f"❌ Finnhub unexpected error: {e}"
        )

        return []
