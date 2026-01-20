"""
Fetches JP Morgan EMBI (Emerging Markets Bond Index) data from Bloomberg.

This module pulls JP Morgan EMBI index data for emerging market sovereign bonds,
including total return indices, spreads, and yields.
"""

import sys
from pathlib import Path

sys.path.insert(0, "./src")

import pandas as pd

import chartbook

BASE_DIR = chartbook.env.get_project_root()
DATA_DIR = BASE_DIR / "_data"
END_DATE = pd.Timestamp.today().strftime("%Y-%m-%d")


def pull_embi_data(start_date="1994-01-01", end_date=END_DATE):
    """
    Fetch historical JP Morgan EMBI data from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    dict
        Dictionary with DataFrames:
        - 'embi_total_return': Total return index levels
        - 'embi_spreads': Spread over US Treasuries
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # JP Morgan EMBI Total Return Index tickers
    total_return_tickers = [
        "JPEIGLBL Index",   # EMBI Global Total Return
        "JPEIDIV Index",    # EMBI Global Diversified Total Return
        "JPGCCOMP Index",   # GBI-EM Global Composite Total Return
        "JPMCEMBI Index",   # CEMBI (Corporate) Total Return
    ]

    # JP Morgan EMBI Spread tickers (over US Treasuries)
    spread_tickers = [
        "JPEMSOSD Index",   # EMBI Global Spread
        "JPEIDIVS Index",   # EMBI Global Diversified Spread
        "JPMCEMSP Index",   # CEMBI Spread
    ]

    # Individual country EMBI indices (selected major EM countries)
    country_tickers = [
        "JPEIBRAZ Index",   # Brazil
        "JPEIMEX Index",    # Mexico
        "JPEIRUSS Index",   # Russia
        "JPEITKEY Index",   # Turkey
        "JPEISAFR Index",   # South Africa
        "JPEIINDN Index",   # Indonesia
        "JPEICOLO Index",   # Colombia
        "JPEICHIN Index",   # China
    ]

    fields = ["PX_LAST"]

    # Helper to flatten multi-index columns from xbbg
    def process_bloomberg_df(df):
        if not df.empty and isinstance(df.columns, pd.MultiIndex):
            df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
            df.reset_index(inplace=True)
        return df

    print(">> Pulling JP Morgan EMBI data from Bloomberg...")

    # Pull total return indices
    print("   Pulling EMBI total return indices...")
    total_return_df = process_bloomberg_df(
        blp.bdh(
            tickers=total_return_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    # Pull spreads
    print("   Pulling EMBI spreads...")
    spreads_df = process_bloomberg_df(
        blp.bdh(
            tickers=spread_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    # Pull country indices
    print("   Pulling country EMBI indices...")
    country_df = process_bloomberg_df(
        blp.bdh(
            tickers=country_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    return {
        "embi_total_return": total_return_df,
        "embi_spreads": spreads_df,
        "embi_country": country_df,
    }


def load_embi_total_return(data_dir=DATA_DIR):
    """Load EMBI total return indices from parquet file."""
    path = data_dir / "embi_total_return.parquet"
    return pd.read_parquet(path)


def load_embi_spreads(data_dir=DATA_DIR):
    """Load EMBI spreads from parquet file."""
    path = data_dir / "embi_spreads.parquet"
    return pd.read_parquet(path)


def load_embi_country(data_dir=DATA_DIR):
    """Load country EMBI indices from parquet file."""
    path = data_dir / "embi_country.parquet"
    return pd.read_parquet(path)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull data from source
    data = pull_embi_data()

    # Save each dataset to parquet
    data["embi_total_return"].to_parquet(DATA_DIR / "embi_total_return.parquet")
    print(f">> Saved embi_total_return.parquet")

    data["embi_spreads"].to_parquet(DATA_DIR / "embi_spreads.parquet")
    print(f">> Saved embi_spreads.parquet")

    data["embi_country"].to_parquet(DATA_DIR / "embi_country.parquet")
    print(f">> Saved embi_country.parquet")


if __name__ == "__main__":
    main()
