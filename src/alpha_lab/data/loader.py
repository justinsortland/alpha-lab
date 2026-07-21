"""Utilities for downloading historical market-price data."""

import pandas as pd
import yfinance as yf

from alpha_lab.data.validation import (
    validate_no_missing_values,
    validate_not_empty,
    validate_required_columns,
    validate_sorted_dates,
)

REQUIRED_PRICE_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]


def load_prices(
    ticker: str,
    start: str,
    end: str,
) -> pd.DataFrame:
    """Download and validate daily historical prices for one ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, such as "SPY".
        start: Inclusive start date in YYYY-MM-DD format.
        end: Exclusive end date in YYYY-MM-DD format.

    Returns:
        A validated DataFrame containing Date, Open, High, Low, Close,
        Adj Close, and Volume.

    Raises:
        ValueError: If the ticker is empty or the downloaded data fails
            validation.
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

    validate_not_empty(prices)

    prices = prices.reset_index()

    validate_required_columns(prices, REQUIRED_PRICE_COLUMNS)
    validate_no_missing_values(prices)
    validate_sorted_dates(prices)

    return prices[REQUIRED_PRICE_COLUMNS]
