"""Utilities for validating historical market data."""

import pandas as pd


def validate_not_empty(df: pd.DataFrame) -> None:
    """Raise an error if the DataFrame contains no rows."""
    if df.empty:
        raise ValueError("Price data is empty.")


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Raise an error if any required columns are missing."""
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Price data is missing required columns: {missing_columns}")


def validate_sorted_dates(df: pd.DataFrame) -> None:
    """Raise an error if any dates are not in ascending chronological order."""
    for i in range(1, len(df)):
        previous = df["Date"].iloc[i - 1]
        current = df["Date"].iloc[i]

        if previous > current:
            raise ValueError(
                "Dates are not in ascending chronological order: "
                f"{current} appears after {previous}."
            )

def validate_no_missing_values(df: pd.DataFrame) -> None:
    """Raise an error if there are any 'NaN' values."""
    columns_with_missing_values = df.columns[df.isna().any()].tolist()

    if columns_with_missing_values:
        raise ValueError(
            "Price data contains missing values in columns: "
            f"{columns_with_missing_values}"
        )