# Sovereign Bonds - JP Morgan EMBI

Emerging market sovereign bond returns from JP Morgan EMBI indices.

## Overview

This pipeline calculates daily returns from JP Morgan EMBI total return indices:

```
Return = (Price_t / Price_{t-1} - 1) * 100
```

Results are in percentage.

## Indices

### Aggregate Indices

- **EMBI_Global**: JP Morgan EMBI Global Total Return
- **EMBI_Global_Diversified**: JP Morgan EMBI Global Diversified Total Return
- **GBI_EM_Composite**: JP Morgan GBI-EM Global Composite (Local Currency)
- **CEMBI_Corporate**: JP Morgan CEMBI (EM Corporate Bonds)

### Country Indices

- EMBI_Brazil
- EMBI_Mexico
- EMBI_Russia
- EMBI_Turkey
- EMBI_South_Africa
- EMBI_Indonesia
- EMBI_Colombia
- EMBI_China

## Data Sources

- **Bloomberg**: JP Morgan EMBI index data

## Outputs

- `ftsfr_embi_returns.parquet`: Daily returns for all EMBI indices

## Requirements

- Bloomberg Terminal running
- Python 3.10+
- xbbg package

## Setup

1. Ensure Bloomberg Terminal is running
2. Install dependencies: `pip install -r requirements.txt`
3. Run pipeline: `doit`

## Academic References

### Primary Paper

- **Borri and Verdelhan (2011)** - "Sovereign Risk Premia"
  - Studies how risk aversion affects sovereign bond prices and defaults

### Key Findings

- Sovereign bond excess returns range from 4% to 15%
- Higher correlation with US equity/corporate returns leads to higher returns
- Market prices of risk are positive and significant
- Emerging market debt exposes countries to US business cycle risk
