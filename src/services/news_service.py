"""
Main News Service

Coordinates:
1. Company Lookup
2. Finnhub News
3. NewsAPI Fallback
4. Sentiment Analysis
"""

from src.services.sentiment_service import analyze_articles
from src.services.company_service import get_stock_symbol
from src.services.finnhub_service import fetch_news as fetch_finnhub_news
from src.services.newsapi_service import fetch_news as fetch_newsapi_news


def fetch_news(company: str):
    """
    Fetch news using Finnhub first.
    If no news is found, fall back to NewsAPI.
    """

    symbol = get_stock_symbol(company)

    if symbol is None:
        print("Company not found.")
        return []

    print(f"\nDetected Symbol : {symbol}")
    print("Searching Finnhub...")

    articles = fetch_finnhub_news(symbol)

    if articles:
        print("✓ News found in Finnhub.")
        return articles

    print("No articles found in Finnhub.")
    print("Searching NewsAPI...")

    articles = fetch_newsapi_news(company)

    if articles:
        print("✓ News found in NewsAPI.")

    return articles

if __name__ == "__main__":

    company = input("Enter Company Name: ")

    # Get Stock Symbol
    symbol = get_stock_symbol(company)

    if symbol is None:
        print("\n❌ Company not found.")
        exit()

    # Fetch News
    articles = fetch_news(company)

    if not articles:
        print("\n❌ No news articles found for this company.")
        exit()

    # Analyze Sentiment
    results = analyze_articles(articles)

    # ================= HEADER =================

    print("\n" + "=" * 100)
    print("REAL-TIME FINANCIAL NEWS SENTIMENT ANALYZER".center(100))
    print("=" * 100)

    print(f"\nCompany         : {company.title()}")
    print(f"Stock Symbol    : {symbol}")
    print(f"News Source     : {'Finnhub / NewsAPI'}")
    print(f"Articles Found  : {len(results['articles'])}")

    # ================= ARTICLES =================

    for i, article in enumerate(results["articles"], start=1):

        sentiment = article["sentiment"].upper()

        if sentiment == "POSITIVE":
            icon = "🟢"
        elif sentiment == "NEGATIVE":
            icon = "🔴"
        else:
            icon = "🟡"

        print("\n" + "=" * 100)
        print(f"ARTICLE #{i}")
        print("=" * 100)

        print(f"📰 {'Title':<12}: {article['headline']}")
        print(f"🏢 {'Source':<12}: {article['source']}")
        print(f"📅 {'Published':<12}: {article['published']}")
        print(f"🤖 {'Sentiment':<12}: {icon} {sentiment}")

    # ================= SUMMARY =================

    if results["positive"] > results["negative"]:
        overall = "🟢 POSITIVE"

    elif results["negative"] > results["positive"]:
        overall = "🔴 NEGATIVE"

    else:
        overall = "🟡 NEUTRAL"

    print("\n" + "=" * 100)
    print("MARKET SENTIMENT SUMMARY".center(100))
    print("=" * 100)

    print(f"🟢 Positive Articles : {results['positive']}")
    print(f"🟡 Neutral Articles  : {results['neutral']}")
    print(f"🔴 Negative Articles : {results['negative']}")

    print(f"\nOverall Market Mood : {overall}")

    print("=" * 100)