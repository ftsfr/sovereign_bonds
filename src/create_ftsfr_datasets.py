"""
Create FTSFR standardized datasets for JP Morgan EMBI returns.

Outputs:
- ftsfr_embi_returns.parquet: Daily EMBI returns for aggregate and country indices
"""

import sys
from pathlib import Path

sys.path.insert(0, "./src")

import pandas as pd

import chartbook
import calc_embi_returns

BASE_DIR = chartbook.env.get_project_root()
DATA_DIR = BASE_DIR / "_data"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(">> Creating ftsfr_embi_returns...")

    # Calculate returns
    results = calc_embi_returns.calculate_embi_returns(data_dir=DATA_DIR)

    # Combine aggregate and country returns
    aggregate_df = results["returns"]
    country_df = results["country_returns"]

    # Merge on date index
    combined_df = aggregate_df.merge(
        country_df, left_index=True, right_index=True, how="outer"
    )

    # Convert from wide to long format
    df_stacked = combined_df.stack().reset_index()
    df_stacked.columns = ["ds", "unique_id", "y"]

    # Reorder columns to FTSFR standard: unique_id, ds, y
    df_stacked = df_stacked[["unique_id", "ds", "y"]]
    df_stacked["ds"] = pd.to_datetime(df_stacked["ds"])

    # Clean up
    df_stacked = df_stacked.dropna()
    df_stacked = df_stacked.sort_values(by=["unique_id", "ds"]).reset_index(drop=True)

    # Save
    output_path = DATA_DIR / "ftsfr_embi_returns.parquet"
    df_stacked.to_parquet(output_path, index=False)
    print(f"   Saved: {output_path.name}")
    print(f"   Records: {len(df_stacked):,}")
    print(f"   Series: {df_stacked['unique_id'].nunique()}")


if __name__ == "__main__":
    main()
