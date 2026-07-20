"""Utilities for downloading historical market-price data."""

import pandas as pd
import yfinance as yf


def load_prices(
    ticker: str,
    start: str,
    end: str,
) -> pd.DataFrame:
    """Download daily historical prices for one ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, such as "SPY".
        start: Inclusive start date in YYYY-MM-DD format.
        end: Exclusive end date in YYYY-MM-DD format.

    Returns:
        A DataFrame containing Date, Open, High, Low, Close, Adj Close,
        and Volume.

    Raises:
        ValueError: If the ticker is empty, no data is returned, or required
            columns are missing.
    """
    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("ticker must not be empty")

    prices: pd.DataFrame = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        multi_level_index=False,
    )

    if prices.empty:
        raise ValueError(
            f"No price data returned for {ticker} between {start} and {end}"
        )

    prices = prices.reset_index()

    expected_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]

    missing_columns = [
        column
        for column in expected_columns
        if column not in prices.columns
    ]

    if missing_columns:
        raise ValueError(
            "Downloaded data is missing required columns: "
            f"{missing_columns}"
        )

    return prices[expected_columns]