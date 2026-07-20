"""Tests for the historical price loader."""

import pandas as pd
import pytest
from pytest import MonkeyPatch

from alpha_lab.data.loader import load_prices


def test_load_prices_rejects_empty_ticker() -> None:
    """An empty ticker should fail before attempting a download."""
    with pytest.raises(ValueError, match="ticker must not be empty"):
        load_prices(
            ticker="   ",
            start="2020-01-01",
            end="2021-01-01",
        )


def test_load_prices_normalizes_and_returns_expected_columns(
    monkeypatch: MonkeyPatch,
) -> None:
    """The loader should normalize the ticker and return a stable schema."""
    downloaded_prices = pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [102.0, 103.0],
            "Low": [99.0, 100.0],
            "Close": [101.0, 102.0],
            "Adj Close": [100.5, 101.5],
            "Volume": [1_000_000, 1_100_000],
        },
        index=pd.DatetimeIndex(
            ["2020-01-02", "2020-01-03"],
            name="Date",
        ),
    )

    captured_arguments: dict[str, object] = {}

    def fake_download(**kwargs: object) -> pd.DataFrame:
        captured_arguments.update(kwargs)
        return downloaded_prices

    monkeypatch.setattr(
        "alpha_lab.data.loader.yf.download",
        fake_download,
    )

    result = load_prices(
        ticker=" spy ",
        start="2020-01-01",
        end="2021-01-01",
    )

    assert captured_arguments["tickers"] == "SPY"
    assert captured_arguments["start"] == "2020-01-01"
    assert captured_arguments["end"] == "2021-01-01"
    assert captured_arguments["auto_adjust"] is False
    assert captured_arguments["progress"] is False
    assert captured_arguments["multi_level_index"] is False

    assert list(result.columns) == [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]
    assert len(result) == 2


def test_load_prices_rejects_empty_download(
    monkeypatch: MonkeyPatch,
) -> None:
    """The loader should fail clearly when the provider returns no rows."""

    def fake_download(**_: object) -> pd.DataFrame:
        return pd.DataFrame()

    monkeypatch.setattr(
        "alpha_lab.data.loader.yf.download",
        fake_download,
    )

    with pytest.raises(ValueError, match="No price data returned"):
        load_prices(
            ticker="INVALID",
            start="2020-01-01",
            end="2021-01-01",
        )