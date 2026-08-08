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


# ======================================================
# Company Search Names
# ======================================================

PRIMARY_NAMES = {
    # USA
    "tesla": '"Tesla"',
    "nvidia": '"NVIDIA"',

    # India
    "reliance": '"Reliance Industries"',
    "reliance industries": '"Reliance Industries"',
    "infosys": '"Infosys"',
    "tcs": '"Tata Consultancy Services"',
    "hdfc bank": '"HDFC Bank"',
    "icici bank": '"ICICI Bank"',

    # Singapore
    "dbs": '"DBS Group"',
    "dbs group": '"DBS Group"',
    "dbs bank": '"DBS Bank"',

    "st engineering": '"ST Engineering"',
    "singapore technologies engineering": '"ST Engineering"',
    "singapore technologies engineering ltd": '"ST Engineering"',

    # Australia
    "commonwealth bank": '"Commonwealth Bank"',
    "commonwealth bank of australia": '"Commonwealth Bank"',
}


# ======================================================
# Company Matching Terms
# ======================================================

COMPANY_TERMS = {
    "tesla": [
        "tesla",
        "tsla",
    ],

    "nvidia": [
        "nvidia",
        "nvda",
    ],

    "reliance": [
        "reliance industries",
        "ril",
        "reliance retail",
        "reliance jio",
    ],

    "reliance industries": [
        "reliance industries",
        "ril",
        "reliance retail",
        "reliance jio",
    ],

    "infosys": [
        "infosys",
        "infy",
    ],

    "tcs": [
        "tata consultancy services",
        "tcs",
    ],

    "hdfc bank": [
        "hdfc bank",
    ],

    "icici bank": [
        "icici bank",
    ],

    "dbs": [
        "dbs group",
        "dbs bank",
    ],

    "dbs group": [
        "dbs group",
        "dbs bank",
    ],

    "dbs bank": [
        "dbs bank",
        "dbs group",
    ],

    "st engineering": [
        "st engineering",
        "singapore technologies engineering",
    ],

    "singapore technologies engineering": [
        "st engineering",
        "singapore technologies engineering",
    ],

    "singapore technologies engineering ltd": [
        "st engineering",
        "singapore technologies engineering",
    ],

    "commonwealth bank": [
        "commonwealth bank",
        "commonwealth bank of australia",
        "cba",
    ],

    "commonwealth bank of australia": [
        "commonwealth bank",
        "commonwealth bank of australia",
        "cba",
    ],
}


# Companies where an exact NewsAPI search can be trusted
# if the returned snippet does not repeat the company name.
TRUSTED_EXACT_QUERY_COMPANIES = {
    "st engineering",
    "singapore technologies engineering",
    "singapore technologies engineering ltd",
}


def _build_search_query(company: str):
    """
    Build a focused NewsAPI search query.
    """

    key = company.strip().lower()

    return PRIMARY_NAMES.get(
        key,
        f'"{company.strip()}"'
    )


def _get_company_terms(company: str):
    """
    Return company terms used for article matching.
    """

    key = company.strip().lower()

    return COMPANY_TERMS.get(
        key,
        [key]
    )


def _get_relevance_score(article, company: str):
    """
    Calculate article relevance.

    Headline      = strongest
    Description   = medium
    Content       = weaker fallback
    """

    title = (
        article.get("title") or ""
    ).lower()

    description = (
        article.get("description") or ""
    ).lower()

    content = (
        article.get("content") or ""
    ).lower()

    terms = _get_company_terms(company)

    score = 0

    for term in terms:

        term = term.lower()

        if term in title:
            score += 10

        if term in description:
            score += 5

        if term in content:
            score += 2

    return score


def _is_low_quality_headline(article):
    """
    Reject broad list-style market headlines.
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


def _remove_duplicates(articles):
    """
    Remove duplicate article URLs and headlines.
    """

    unique_articles = []

    seen_urls = set()
    seen_headlines = set()

    for article in articles:

        url = (
            article.get("url") or ""
        ).strip()

        headline = (
            article.get("title") or ""
        ).strip().lower()

        if not url or not headline:
            continue

        if url in seen_urls:
            continue

        if headline in seen_headlines:
            continue

        seen_urls.add(url)
        seen_headlines.add(headline)

        unique_articles.append(article)

    return unique_articles


def fetch_news(
    company: str,
    limit: int = 5
):
    """
    Fetch relevant company news from NewsAPI.
    """

    if not NEWS_API_KEY:

        print("❌ NEWS_API_KEY is missing.")

        return []

    company_key = company.strip().lower()

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

        # ==================================================
        # Relevance Scoring
        # ==================================================

        scored_articles = []

        for article in articles:

            if _is_low_quality_headline(article):
                continue

            score = _get_relevance_score(
                article,
                company
            )

            if score > 0:

                scored_articles.append(
                    (
                        score,
                        article
                    )
                )

        scored_articles.sort(
            key=lambda item: item[0],
            reverse=True
        )

        relevant_articles = [
            article
            for score, article
            in scored_articles
        ]

        print(
            f"Relevant articles after scoring: "
            f"{len(relevant_articles)}"
        )

        # ==================================================
        # Trusted Exact Query Fallback
        # ==================================================

        if (
            not relevant_articles
            and company_key
            in TRUSTED_EXACT_QUERY_COMPANIES
        ):

            print(
                "Using exact-query fallback "
                "for trusted company."
            )

            relevant_articles = [
                article
                for article in articles
                if not _is_low_quality_headline(article)
            ]

        # ==================================================
        # Duplicate Removal
        # ==================================================

        unique_articles = _remove_duplicates(
            relevant_articles
        )

        print(
            f"Unique relevant articles: "
            f"{len(unique_articles)}"
        )

        print("\nSelected articles:")

        for article in unique_articles[:limit]:

            print(
                "-",
                article.get("title")
            )

        return unique_articles[:limit]

    except requests.exceptions.RequestException as error:

        print(
            f"❌ NewsAPI request failed: "
            f"{error}"
        )

        return []

    except Exception as error:

        print(
            f"❌ NewsAPI unexpected error: "
            f"{error}"
        )

        return []