# %%
"""
# JP Morgan EMBI Returns Summary

Emerging Market Bond Index returns and spreads from JP Morgan.
"""

# %%
import sys
sys.path.insert(0, "./src")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import chartbook

BASE_DIR = chartbook.env.get_project_root()
DATA_DIR = BASE_DIR / "_data"

# %%
"""
## Methodology

Daily returns are calculated from JP Morgan EMBI total return indices:

$$
r_t = \\frac{P_t - P_{t-1}}{P_{t-1}} \\times 100
$$

Where $P_t$ is the total return index level on day $t$.

### Data Sources

- JP Morgan EMBI Global and Diversified indices
- JP Morgan GBI-EM (local currency) indices
- JP Morgan CEMBI (corporate) indices
- Individual country EMBI indices
"""

# %%
"""
## Data Overview
"""

# %%
df = pd.read_parquet(DATA_DIR / "ftsfr_embi_returns.parquet")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nDate range: {df['ds'].min()} to {df['ds'].max()}")
print(f"Number of series: {df['unique_id'].nunique()}")

# %%
print("\nSeries:")
for series in sorted(df['unique_id'].unique()):
    print(f"  {series}")

# %%
"""
### Summary Statistics
"""

# %%
embi_wide = df.pivot(index='ds', columns='unique_id', values='y')
embi_stats = embi_wide.describe().T
embi_stats['skewness'] = embi_wide.skew()
embi_stats['kurtosis'] = embi_wide.kurtosis()
print(embi_stats[['mean', 'std', 'min', 'max', 'skewness', 'kurtosis']].round(4).to_string())

# %%
"""
### Aggregate Index Returns
"""

# %%
fig, ax = plt.subplots(figsize=(14, 8))

aggregate_cols = ['EMBI_Global', 'EMBI_Global_Diversified', 'GBI_EM_Composite', 'CEMBI_Corporate']
for col in aggregate_cols:
    if col in embi_wide.columns:
        ax.plot(embi_wide.index, embi_wide[col], label=col, alpha=0.7, linewidth=0.8)

ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Date')
ax.set_ylabel('Daily Return (%)')
ax.set_title('JP Morgan EMBI Aggregate Index Returns')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(DATA_DIR.parent / "_output" / "embi_aggregate_returns.png", dpi=150, bbox_inches='tight')
plt.show()

# %%
"""
### Country Index Returns
"""

# %%
fig, ax = plt.subplots(figsize=(14, 8))

country_cols = [col for col in embi_wide.columns if col.startswith('EMBI_') and col not in aggregate_cols]
for col in country_cols:
    if col in embi_wide.columns:
        ax.plot(embi_wide.index, embi_wide[col], label=col.replace('EMBI_', ''), alpha=0.7, linewidth=0.8)

ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Date')
ax.set_ylabel('Daily Return (%)')
ax.set_title('JP Morgan EMBI Country Index Returns')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(DATA_DIR.parent / "_output" / "embi_country_returns.png", dpi=150, bbox_inches='tight')
plt.show()

# %%
"""
### Cumulative Returns
"""

# %%
# Calculate cumulative returns
cumulative = (1 + embi_wide / 100).cumprod()

fig, ax = plt.subplots(figsize=(14, 8))

for col in aggregate_cols:
    if col in cumulative.columns:
        ax.plot(cumulative.index, cumulative[col], label=col, alpha=0.8)

ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Return')
ax.set_title('JP Morgan EMBI Cumulative Returns (Growth of $1)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_yscale('log')

plt.tight_layout()
plt.savefig(DATA_DIR.parent / "_output" / "embi_cumulative_returns.png", dpi=150, bbox_inches='tight')
plt.show()

# %%
"""
### Correlation Matrix
"""

# %%
fig, ax = plt.subplots(figsize=(12, 10))
corr = embi_wide.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax,
            annot_kws={'size': 8})
ax.set_title('EMBI Returns Correlations')
plt.tight_layout()
plt.savefig(DATA_DIR.parent / "_output" / "embi_correlation.png", dpi=150, bbox_inches='tight')
plt.show()

# %%
"""
## Data Definitions

### EMBI Returns (ftsfr_embi_returns)

| Variable | Description |
|----------|-------------|
| unique_id | Index identifier (e.g., EMBI_Global, EMBI_Brazil) |
| ds | Date |
| y | Daily return (percentage) |

### Aggregate Indices

| Code | Description |
|------|-------------|
| EMBI_Global | JP Morgan EMBI Global Total Return |
| EMBI_Global_Diversified | JP Morgan EMBI Global Diversified Total Return |
| GBI_EM_Composite | JP Morgan GBI-EM Global Composite (Local Currency) |
| CEMBI_Corporate | JP Morgan CEMBI (EM Corporate Bonds) |

### Country Indices

| Code | Country |
|------|---------|
| EMBI_Brazil | Brazil |
| EMBI_Mexico | Mexico |
| EMBI_Russia | Russia |
| EMBI_Turkey | Turkey |
| EMBI_South_Africa | South Africa |
| EMBI_Indonesia | Indonesia |
| EMBI_Colombia | Colombia |
| EMBI_China | China |
"""
