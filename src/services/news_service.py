"""
Main News Service

Coordinates:

1. Company Lookup
2. Finnhub News for supported US stocks
3. NewsAPI for Indian NSE stocks
4. NewsAPI Fallback
5. Sentiment Analysis
"""

from src.services.sentiment_service import analyze_articles
from src.services.company_service import get_stock_symbol
from src.services.finnhub_service import fetch_news as fetch_finnhub_news
from src.services.newsapi_service import fetch_news as fetch_newsapi_news


def fetch_news(company: str, limit: int = 5):
    """
    Fetch news using the appropriate news source.

    Indian NSE stocks (.NS):
        -> NewsAPI directly

    Other stocks:
        -> Finnhub first
        -> NewsAPI fallback if Finnhub fails
    """

    symbol = get_stock_symbol(company)

    if symbol is None:
        print("Company not found.")
        return []

    print(f"\nDetected Symbol : {symbol}")

    # --------------------------------------------------
    # Indian NSE Stocks
    # --------------------------------------------------

    if symbol.upper().endswith(".NS"):

        print("Indian NSE stock detected.")
        print("Skipping Finnhub.")
        print("Searching NewsAPI...")

        articles = fetch_newsapi_news(
            company,
            limit
        )

        if articles:
            print("✓ News found in NewsAPI.")

        return articles

    # --------------------------------------------------
    # Finnhub for supported stocks
    # --------------------------------------------------

    print("Searching Finnhub...")

    articles = fetch_finnhub_news(
        symbol,
        limit
    )

    if articles:

        print("✓ News found in Finnhub.")

        return articles

    # --------------------------------------------------
    # NewsAPI Fallback
    # --------------------------------------------------

    print("No articles found in Finnhub.")
    print("Searching NewsAPI...")

    articles = fetch_newsapi_news(
        company,
        limit
    )

    if articles:

        print("✓ News found in NewsAPI.")

    return articles


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    company = input("Enter Company Name: ")

    limit = 5

    # --------------------------------------------------
    # Get Stock Symbol
    # --------------------------------------------------

    symbol = get_stock_symbol(company)

    if symbol is None:

        print("\n❌ Company not found.")

        exit()


    # --------------------------------------------------
    # Fetch News
    # --------------------------------------------------

    articles = fetch_news(
        company,
        limit
    )
    print("DEBUG: News fetching completed.")
    print("DEBUG: Starting sentiment analysis...")
    if not articles:

        print(
            "\n❌ No news articles found "
            "for this company."
        )

        exit()


    # --------------------------------------------------
    # Analyze Sentiment
    # --------------------------------------------------
    print("DEBUG: Calling analyze_articles...")
    results = analyze_articles(articles)
    print("DEBUG: Sentiment analysis completed.")

    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    print(
        "\n" + "=" * 100
    )

    print(
        "REAL-TIME FINANCIAL NEWS SENTIMENT ANALYZER"
        .center(100)
    )

    print(
        "=" * 100
    )

    print(
        f"\nCompany         : "
        f"{company.title()}"
    )

    print(
        f"Stock Symbol    : "
        f"{symbol}"
    )

    print(
        f"News Source     : "
        f"Finnhub / NewsAPI"
    )

    print(
        f"Articles Found  : "
        f"{len(results['articles'])}"
    )


    # --------------------------------------------------
    # Individual Articles
    # --------------------------------------------------

    for i, article in enumerate(
        results["articles"],
        start=1
    ):

        sentiment = (
            article["sentiment"]
            .upper()
        )


        if sentiment == "POSITIVE":

            icon = "🟢"

        elif sentiment == "NEGATIVE":

            icon = "🔴"

        else:

            icon = "🟡"


        print(
            "\n" + "=" * 100
        )

        print(
            f"ARTICLE #{i}"
        )

        print(
            "=" * 100
        )

        print(
            f"📰 {'Title':<12}: "
            f"{article['headline']}"
        )

        print(
            f"🏢 {'Source':<12}: "
            f"{article['source']}"
        )

        print(
            f"📅 {'Published':<12}: "
            f"{article['published']}"
        )

        print(
            f"🤖 {'Sentiment':<12}: "
            f"{icon} {sentiment}"
        )


    # --------------------------------------------------
    # Overall Sentiment
    # --------------------------------------------------

    if (
        results["positive"]
        > results["negative"]
    ):

        overall = "🟢 POSITIVE"

    elif (
        results["negative"]
        > results["positive"]
    ):

        overall = "🔴 NEGATIVE"

    else:

        overall = "🟡 NEUTRAL"


    # --------------------------------------------------
    # Market Sentiment Summary
    # --------------------------------------------------

    print(
        "\n" + "=" * 100
    )

    print(
        "MARKET SENTIMENT SUMMARY"
        .center(100)
    )

    print(
        "=" * 100
    )

    print(
        f"🟢 Positive Articles : "
        f"{results['positive']}"
    )

    print(
        f"🟡 Neutral Articles  : "
        f"{results['neutral']}"
    )

    print(
        f"🔴 Negative Articles : "
        f"{results['negative']}"
    )

    print(
        f"\nOverall Market Mood : "
        f"{overall}"
    )

    print(
        "=" * 100
    )
