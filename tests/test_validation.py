"""Tests for historical price-data validation."""

import pandas as pd
import pytest

from alpha_lab.data.validation import (
    validate_no_missing_values,
    validate_not_empty,
    validate_required_columns,
    validate_sorted_dates,
)


def test_validate_not_empty_rejects_empty_dataframe() -> None:
    empty_df = pd.DataFrame()

    with pytest.raises(ValueError, match="Price data is empty"):
        validate_not_empty(empty_df)


def test_validate_not_empty_accepts_complete_dataframe() -> None:
    data = {
        "Date": ["2026-07-01", "2026-07-02", "2026-07-03"],
        "Close": [150.25, 152.10, 151.80],
    }

    df = pd.DataFrame(data)
    validate_not_empty(df)


def test_validate_required_columns_rejects_missing_columns() -> None:
    data = {
        "Date": ["2026-07-01", "2026-07-02", "2026-07-03"],
        "Close": [150.25, 152.10, 151.80],
    }

    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="missing required columns"):
        validate_required_columns(df, ["Date", "Close", "Volume"])


def test_validate_required_columns_accepts_complete_dataframe() -> None:
    data = {
        "Date": ["2026-07-01", "2026-07-02"],
        "Close": [150.25, 152.10],
        "Volume": [1_000_000, 1_100_000],
    }

    df = pd.DataFrame(data)
    validate_required_columns(df, ["Date", "Close", "Volume"])


def test_validate_sorted_dates_rejects_unsorted_dates() -> None:
    data = {
        "Date": ["2026-07-01", "2026-07-03", "2026-07-02"],
        "Close": [150.25, 152.10, 151.80],
    }

    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="not in ascending chronological order"):
        validate_sorted_dates(df)


def test_validate_sorted_dates_accepts_sorted_dates() -> None:
    data = {
        "Date": ["2026-07-01", "2026-07-02", "2026-07-03"],
        "Close": [150.25, 152.10, 151.80],
    }

    df = pd.DataFrame(data)
    validate_sorted_dates(df)


def test_validate_no_missing_values_rejects_missing_values() -> None:
    df = pd.DataFrame(
        {
            "Date": ["2026-07-01", "2026-07-02"],
            "Close": [150.25, None],
            "Volume": [1_000_000, 1_100_000],
        }
    )

    with pytest.raises(ValueError, match="contains missing values"):
        validate_no_missing_values(df)


def test_validate_no_missing_values_accepts_complete_dataframe() -> None:
    df = pd.DataFrame(
        {
            "Date": ["2026-07-01", "2026-07-02"],
            "Close": [150.25, 152.10],
            "Volume": [1_000_000, 1_100_000],
        }
    )
    validate_no_missing_values(df)
