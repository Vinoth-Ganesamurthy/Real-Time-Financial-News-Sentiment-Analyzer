"""
NewsAPI Service

Fetches company-related news from NewsAPI,
filters weak results, removes duplicates,
and returns the most relevant articles.
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


COMPANY_ALIASES = {
    "reliance": [
        '"Reliance Industries"',
    ],
    "reliance industries": [
        '"Reliance Industries"',
    ],
    "infosys": [
        '"Infosys"',
    ],
    "tcs": [
        '"Tata Consultancy Services"',
    ],
    "hdfc bank": [
        '"HDFC Bank"',
    ],
    "icici bank": [
        '"ICICI Bank"',
    ],
    "tesla": [
        '"Tesla"',
    ],
    "nvidia": [
        '"NVIDIA"',
    ],
}


def _get_company_terms(company: str):
    """
    Return company terms used for matching.
    """

    key = company.strip().lower()

    terms = {
        "reliance": [
            "reliance industries",
            "reliance industries limited",
            "ril",
            "reliance jio",
            "reliance retail",
        ],
        "reliance industries": [
            "reliance industries",
            "reliance industries limited",
            "ril",
            "reliance jio",
            "reliance retail",
        ],
        "infosys": [
            "infosys",
            "infosys limited",
            "infy",
        ],
        "tcs": [
            "tata consultancy services",
            "tcs",
        ],
        "hdfc bank": [
            "hdfc bank",
            "hdfc bank limited",
        ],
        "icici bank": [
            "icici bank",
            "icici bank limited",
        ],
        "tesla": [
            "tesla",
        ],
        "nvidia": [
            "nvidia",
        ],
    }

    return terms.get(key, [key])


def _build_search_query(company: str):
    """
    Build a focused NewsAPI search query.
    """

    key = company.strip().lower()

    primary_names = {
        "reliance": '"Reliance Industries"',
        "reliance industries": '"Reliance Industries"',
        "infosys": '"Infosys"',
        "tcs": '"Tata Consultancy Services"',
        "hdfc bank": '"HDFC Bank"',
        "icici bank": '"ICICI Bank"',
        "tesla": '"Tesla"',
        "nvidia": '"NVIDIA"',
    }

    return primary_names.get(
        key,
        f'"{company.strip()}"'
    )


def _get_relevance_score(article, company: str):
    """
    Calculate article relevance.

    Company in headline = strong relevance.
    Company in description = additional relevance.
    """

    title = (
        article.get("title") or ""
    ).lower()

    description = (
        article.get("description") or ""
    ).lower()

    terms = _get_company_terms(company)

    score = 0

    for term in terms:

        term = term.lower()

        if term in title:
            score += 10

        if term in description:
            score += 2

    return score


def _is_low_quality_headline(article):
    """
    Reject generic market-list headlines.
    """

    title = (
        article.get("title") or ""
    ).strip().lower()

    blocked_phrases = [
        "stocks to watch:",
        "stocks to watch -",
        "stocks to watch |",
        "top stocks to watch",
        "stocks in focus:",
        "stocks in focus -",
        "stocks in focus |",
        "shares to watch:",
    ]

    return any(
        phrase in title
        for phrase in blocked_phrases
    )


def fetch_news(
    company: str,
    limit: int = 5
):
    """
    Fetch company-related news from NewsAPI.

    Articles are scored, filtered, deduplicated,
    and limited to the requested number.
    """

    if not NEWS_API_KEY:

        print("❌ NEWS_API_KEY is missing.")

        return []

    url = "https://newsapi.org/v2/everything"

    query = _build_search_query(company)

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": NEWS_API_KEY,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        print(
            f"NewsAPI HTTP Status: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "ok":

            print(
                f"❌ NewsAPI Error: "
                f"{data.get('code')} - "
                f"{data.get('message')}"
            )

            return []

        articles = data.get(
            "articles",
            []
        )

        print(
            f"NewsAPI Total Results: "
            f"{data.get('totalResults')}"
        )

        print(
            f"Articles received: "
            f"{len(articles)}"
        )

        # -----------------------------------------
        # Score and filter articles
        # -----------------------------------------

        scored_articles = []

        for article in articles:

            score = _get_relevance_score(
                article,
                company
            )

            if (
                score >= 10
                and not _is_low_quality_headline(article)
            ):

                scored_articles.append(
                    (
                        score,
                        article
                    )
                )

        print(
            f"Relevant articles after scoring: "
            f"{len(scored_articles)}"
        )

        # -----------------------------------------
        # Sort by relevance
        # -----------------------------------------

        scored_articles.sort(
            key=lambda item: item[0],
            reverse=True
        )

        # -----------------------------------------
        # Remove duplicate URLs
        # AND duplicate headlines
        # -----------------------------------------

        unique_articles = []

        seen_urls = set()
        seen_headlines = set()

        for score, article in scored_articles:

            article_url = (
                article.get("url") or ""
            ).strip()

            headline = (
                article.get("title") or ""
            ).strip().lower()

            if not article_url:
                continue

            if not headline:
                continue

            if article_url in seen_urls:
                continue

            if headline in seen_headlines:
                continue

            seen_urls.add(article_url)
            seen_headlines.add(headline)

            unique_articles.append(article)

        print(
            f"Unique relevant articles: "
            f"{len(unique_articles)}"
        )

        # -----------------------------------------
        # Selected articles
        # -----------------------------------------

        print("\nSelected articles:")

        for article in unique_articles[:limit]:

            print(
                "-",
                article.get("title")
            )

        # -----------------------------------------
        # Return results
        # -----------------------------------------

        return unique_articles[:limit]

    except requests.exceptions.RequestException as e:

        print(
            f"❌ NewsAPI request failed: {e}"
        )

        return []

    except Exception as e:

        print(
            f"❌ NewsAPI unexpected error: {e}"
        )

        return []