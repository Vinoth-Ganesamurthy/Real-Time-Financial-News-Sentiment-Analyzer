"""
Historical Stock Performance Service

Fetches historical stock prices using yfinance
and calculates basic investment performance metrics.
"""

import yfinance as yf
import pandas as pd


def fetch_historical_data(symbol: str, days: int = 90):
    """
    Fetch historical daily stock prices.

    Args:
        symbol: Stock ticker symbol.
        days: Number of calendar days to retrieve.

    Returns:
        List of historical price records.
    """

    if not symbol:
        return []

    symbol = symbol.upper().strip()

    try:
        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period=f"{days}d",
            interval="1d",
            auto_adjust=False,
        )

        if history.empty:
            return []

        historical_data = []

        for index, row in history.iterrows():

            historical_data.append(
                {
                    "date": index.strftime("%Y-%m-%d"),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                }
            )

        return historical_data

    except Exception as e:
        print(f"Historical data error for {symbol}: {e}")
        return []


def calculate_performance(historical_data: list):
    """
    Calculate investment performance metrics from historical data.

    Returns:
        1-week return
        1-month return
        3-month return
        annualized volatility
        maximum drawdown
    """

    if not historical_data or len(historical_data) < 2:
        return {}

    prices = pd.Series(
        [item["close"] for item in historical_data]
    )

    # -------------------------
    # Current price
    # -------------------------

    current_price = prices.iloc[-1]

    # -------------------------
    # 1 Week Return
    # -------------------------

    week_index = max(0, len(prices) - 6)

    week_price = prices.iloc[week_index]

    week_return = (
        (current_price - week_price)
        / week_price
    ) * 100

    # -------------------------
    # 1 Month Return
    # -------------------------

    month_index = max(0, len(prices) - 22)

    month_price = prices.iloc[month_index]

    month_return = (
        (current_price - month_price)
        / month_price
    ) * 100

    # -------------------------
    # 3 Month Return
    # -------------------------

    three_month_price = prices.iloc[0]

    three_month_return = (
        (current_price - three_month_price)
        / three_month_price
    ) * 100

    # -------------------------
    # Volatility
    # -------------------------

    daily_returns = prices.pct_change().dropna()

    volatility = (
        daily_returns.std()
        * (252 ** 0.5)
        * 100
    )

    # -------------------------
    # Maximum Drawdown
    # -------------------------

    running_max = prices.cummax()

    drawdown = (
        (prices - running_max)
        / running_max
    ) * 100

    max_drawdown = drawdown.min()

    return {
        "current_price": round(float(current_price), 2),
        "one_week_return": round(float(week_return), 2),
        "one_month_return": round(float(month_return), 2),
        "three_month_return": round(float(three_month_return), 2),
        "annualized_volatility": round(float(volatility), 2),
        "maximum_drawdown": round(float(max_drawdown), 2),
    }