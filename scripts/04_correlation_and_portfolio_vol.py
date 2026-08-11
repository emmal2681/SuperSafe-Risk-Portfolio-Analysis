"""
04_correlation_and_portfolio_vol.py
------------------------------------
Reads the daily returns table produced by 03_compute_returns.py and:
  1. Builds the pairwise correlation matrix across all 10 stocks.
  2. Computes the annualised volatility of an equal-weighted portfolio
     that holds the same fraction (1/N) of each stock.

Outputs saved to data/raw/:
  - correlation_matrix.csv
  - portfolio_volatility.csv
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load daily returns
# ---------------------------------------------------------------------------
# Each row is one trading day; each column is one stock's daily % return
# (expressed as a decimal, e.g. 0.01 = +1 %).
# index_col=0 promotes the "Date" column to the row index.
# parse_dates=True converts those index values to real Python date objects.
daily_returns = pd.read_csv(
    "data/raw/daily_returns.csv",
    index_col=0,
    parse_dates=True,
)

tickers = daily_returns.columns.tolist()
n_stocks = len(tickers)
n_days   = len(daily_returns)

print(f"Loaded {n_days:,} trading days x {n_stocks} stocks: {tickers}\n")

# ---------------------------------------------------------------------------
# 2. Correlation matrix
# ---------------------------------------------------------------------------
# The correlation between two assets tells us how their daily moves tend to
# track each other on a scale from -1 (perfectly opposite) to +1 (perfectly
# in sync).  A value near 0 means the two stocks move independently.
#
# pandas .corr() computes all N x N pairwise correlations in one call.
# The diagonal is always 1.0 (every stock is perfectly correlated with itself).
corr_matrix = daily_returns.corr()

# Save the full N x N matrix so it can be fed into downstream reports or
# visualisations without recomputing it.
corr_matrix.to_csv("data/raw/correlation_matrix.csv")
print("Correlation matrix (saved to data/raw/correlation_matrix.csv):")
print(corr_matrix.round(3).to_string())
print()

# ---------------------------------------------------------------------------
# 3. Equal-weighted portfolio volatility
# ---------------------------------------------------------------------------
# An "equal-weighted" portfolio puts the same dollar amount into each stock.
# With N stocks that means a weight of 1/N for every position.
weights = np.full(n_stocks, 1.0 / n_stocks)   # shape: (N,)

# The covariance matrix captures not just each stock's own variance
# (on the diagonal) but also how pairs of stocks move together (off-diagonal).
# Portfolio variance is a quadratic form:  w^T . Cov . w
# where Cov is the covariance matrix and w is the weight vector.
cov_matrix = daily_returns.cov()               # daily covariance, shape: (N, N)

# Daily portfolio variance: the scalar result of  w . Cov . w
portfolio_variance_daily = weights @ cov_matrix.values @ weights

# Annualise: multiply daily variance by 252 trading days per year,
# then take the square root to convert variance -> standard deviation (volatility).
portfolio_vol_annual = np.sqrt(portfolio_variance_daily * 252)

print(f"Equal-weighted portfolio annualised volatility: {portfolio_vol_annual:.4%}\n")

# ---------------------------------------------------------------------------
# 4. Save portfolio volatility summary
# ---------------------------------------------------------------------------
# Build a small one-row DataFrame so the result is self-documenting
# when opened in Excel or read back by the next script.
summary = pd.DataFrame(
    {
        "n_stocks":          [n_stocks],
        "weights":           [f"1/{n_stocks} each"],
        "portfolio_vol_ann": [round(portfolio_vol_annual, 6)],
    }
)
summary.to_csv("data/raw/portfolio_volatility.csv", index=False)
print("Portfolio volatility summary (saved to data/raw/portfolio_volatility.csv):")
print(summary.to_string(index=False))
print()

print("SUCCESS: correlation_matrix.csv and portfolio_volatility.csv written to data/raw/")
