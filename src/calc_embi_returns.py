"""
Calculate returns from JP Morgan EMBI indices.

This module computes daily returns from EMBI total return index levels
for emerging market sovereign bond analysis.

Data Sources:
    - Bloomberg JP Morgan EMBI indices
"""

import sys
from pathlib import Path

sys.path.insert(0, "./src")

import pandas as pd
import numpy as np

import chartbook
import pull_bbg_embi

BASE_DIR = chartbook.env.get_project_root()
DATA_DIR = BASE_DIR / "_data"

# Mapping from Bloomberg tickers to friendly names
TOTAL_RETURN_MAPPING = {
    "JPEIGLBL": "EMBI_Global",
    "JPEIDIV": "EMBI_Global_Diversified",
    "JPGCCOMP": "GBI_EM_Composite",
    "JPMCEMBI": "CEMBI_Corporate",
}

SPREAD_MAPPING = {
    "JPEMSOSD": "EMBI_Global_Spread",
    "JPEIDIVS": "EMBI_Global_Div_Spread",
    "JPMCEMSP": "CEMBI_Spread",
}

COUNTRY_MAPPING = {
    "JPEIBRAZ": "EMBI_Brazil",
    "JPEIMEX": "EMBI_Mexico",
    "JPEIRUSS": "EMBI_Russia",
    "JPEITKEY": "EMBI_Turkey",
    "JPEISAFR": "EMBI_South_Africa",
    "JPEIINDN": "EMBI_Indonesia",
    "JPEICOLO": "EMBI_Colombia",
    "JPEICHIN": "EMBI_China",
}


def prepare_data(df, mapping):
    """
    Prepare Bloomberg data by cleaning column names.

    Parameters
    ----------
    df : pd.DataFrame
        Raw data from Bloomberg
    mapping : dict
        Mapping from ticker codes to friendly names

    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned column names
    """
    # Set Date as index
    df = df.set_index("index") if "index" in df.columns else df

    # Clean up column names
    new_cols = {}
    for col in df.columns:
        if "_PX_LAST" in col:
            ticker = col.split()[0]
            if ticker in mapping:
                new_cols[col] = mapping[ticker]
    df = df.rename(columns=new_cols)

    return df


def compute_returns(index_df):
    """
    Compute daily returns from total return index levels.

    Parameters
    ----------
    index_df : pd.DataFrame
        DataFrame with total return index levels

    Returns
    -------
    pd.DataFrame
        DataFrame with daily returns (percentage)
    """
    # Calculate daily returns as percentage change
    returns_df = index_df.pct_change() * 100

    # Remove first row (NaN from pct_change)
    returns_df = returns_df.iloc[1:]

    return returns_df


def calculate_embi_returns(end_date=None, data_dir=DATA_DIR):
    """
    Calculate EMBI returns from index data.

    Parameters
    ----------
    end_date : str, optional
        End date for the data
    data_dir : Path
        Directory containing the data files

    Returns
    -------
    dict
        Dictionary with DataFrames:
        - 'returns': Daily returns for aggregate indices
        - 'country_returns': Daily returns for country indices
        - 'spreads': Spread levels
    """
    data_dir = Path(data_dir)

    print(">> Calculating EMBI returns...")

    # Load data
    total_return_df = pull_bbg_embi.load_embi_total_return(data_dir=data_dir)
    spreads_df = pull_bbg_embi.load_embi_spreads(data_dir=data_dir)
    country_df = pull_bbg_embi.load_embi_country(data_dir=data_dir)

    # Prepare data
    total_return_df = prepare_data(total_return_df, TOTAL_RETURN_MAPPING)
    spreads_df = prepare_data(spreads_df, SPREAD_MAPPING)
    country_df = prepare_data(country_df, COUNTRY_MAPPING)

    # Filter by end date if specified
    if end_date:
        date = pd.Timestamp(end_date).date()
        total_return_df = total_return_df.loc[:date]
        spreads_df = spreads_df.loc[:date]
        country_df = country_df.loc[:date]

    # Compute returns
    returns_df = compute_returns(total_return_df)
    country_returns_df = compute_returns(country_df)

    print(f">> Aggregate records: {len(returns_df):,}")
    print(f">> Country records: {len(country_returns_df):,}")

    return {
        "returns": returns_df,
        "country_returns": country_returns_df,
        "spreads": spreads_df,
    }


def load_embi_returns(data_dir=DATA_DIR):
    """Load calculated EMBI returns from parquet file."""
    path = data_dir / "embi_returns.parquet"
    return pd.read_parquet(path)


def load_embi_country_returns(data_dir=DATA_DIR):
    """Load calculated country EMBI returns from parquet file."""
    path = data_dir / "embi_country_returns.parquet"
    return pd.read_parquet(path)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    results = calculate_embi_returns(data_dir=DATA_DIR)

    results["returns"].to_parquet(DATA_DIR / "embi_returns.parquet")
    print(">> Saved embi_returns.parquet")

    results["country_returns"].to_parquet(DATA_DIR / "embi_country_returns.parquet")
    print(">> Saved embi_country_returns.parquet")

    results["spreads"].to_parquet(DATA_DIR / "embi_spreads_clean.parquet")
    print(">> Saved embi_spreads_clean.parquet")


if __name__ == "__main__":
    main()
