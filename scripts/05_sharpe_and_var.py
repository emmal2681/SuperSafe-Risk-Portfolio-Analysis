"""
05_sharpe_and_var.py
---------------------
Uses the same daily returns and equal weights from scripts 03 & 04 to compute:
  1. Portfolio Sharpe Ratio   -- reward per unit of risk taken
  2. 95% Historical VaR       -- worst-case daily loss on 19 out of 20 days

Assumptions
  - Equal weights: 1/N per stock (same as script 04)
  - Risk-free rate: 4.5% annualised (e.g. current T-bill yield)
  - VaR confidence: 95% historical (no distributional assumptions)

Output saved to data/raw/portfolio_summary.csv
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load daily returns
# ---------------------------------------------------------------------------
# Rows = trading days, columns = individual stock daily % returns (decimals).
daily_returns = pd.read_csv(
    "data/raw/daily_returns.csv",
    index_col=0,
    parse_dates=True,
)

tickers  = daily_returns.columns.tolist()
n_stocks = len(tickers)
n_days   = len(daily_returns)

print(f"Loaded {n_days:,} trading days x {n_stocks} stocks.\n")

# ---------------------------------------------------------------------------
# 2. Build equal-weighted daily portfolio return series
# ---------------------------------------------------------------------------
# Each day's portfolio return is the simple average of all stock returns,
# because every stock carries the same weight (1/10 = 10%).
# np.full creates an array [0.1, 0.1, ..., 0.1] with N_STOCKS entries.
weights = np.full(n_stocks, 1.0 / n_stocks)

# Matrix multiply: (1906 days x 10 stocks) @ (10 weights,) -> (1906 days,)
# This collapses ten columns into a single daily portfolio return number.
portfolio_daily_returns = daily_returns.values @ weights
portfolio_daily_returns = pd.Series(portfolio_daily_returns, index=daily_returns.index)

# Quick sanity check -- shows first few portfolio daily returns
print("Sample portfolio daily returns (first 5 days):")
print(portfolio_daily_returns.head().map("{:.4%}".format).to_string())
print()

# ---------------------------------------------------------------------------
# 3. Sharpe Ratio
# ---------------------------------------------------------------------------
# The Sharpe ratio answers: "How much *extra* return did I earn per unit of
# risk I took on?"  A higher Sharpe means better risk-adjusted performance.
#
# Formula:
#   Sharpe = (Annualised Portfolio Return - Risk-Free Rate)
#            ---------------------------------------------------
#                     Annualised Portfolio Volatility
#
# Step 3a -- Annualise the mean daily return.
# The average daily return is compounded across ~252 trading days per year.
# We use the simple approximation: annual mean = daily mean * 252.
mean_daily_return    = portfolio_daily_returns.mean()
annual_portfolio_ret = mean_daily_return * 252

# Step 3b -- Annualise the daily standard deviation (volatility).
# Daily std dev scaled up by sqrt(252) because variance scales linearly
# with time, so std dev scales by the square root.
daily_std            = portfolio_daily_returns.std()
annual_portfolio_vol = daily_std * np.sqrt(252)

# Step 3c -- Subtract the risk-free rate then divide by volatility.
# The risk-free rate is what you'd earn with zero risk (e.g. T-bills).
# Subtracting it isolates the *excess* return the portfolio generated.
RISK_FREE_RATE = 0.045   # 4.5% annualised
excess_return  = annual_portfolio_ret - RISK_FREE_RATE
sharpe_ratio   = excess_return / annual_portfolio_vol

print("=" * 55)
print("SHARPE RATIO")
print("=" * 55)
print(f"  Annualised portfolio return : {annual_portfolio_ret:>8.4%}")
print(f"  Risk-free rate (assumed)    : {RISK_FREE_RATE:>8.4%}")
print(f"  Excess return               : {excess_return:>8.4%}")
print(f"  Annualised volatility       : {annual_portfolio_vol:>8.4%}")
print(f"  Sharpe ratio                : {sharpe_ratio:>8.4f}")
print()
print("  Plain-English interpretation:")
if sharpe_ratio >= 1.0:
    quality = "excellent (above 1.0 is generally considered strong)"
elif sharpe_ratio >= 0.5:
    quality = "acceptable (0.5-1.0 is considered reasonable)"
else:
    quality = "weak (below 0.5 suggests poor risk-adjusted performance)"
print(f"  For every 1% of annual risk taken, the portfolio earned")
print(f"  {sharpe_ratio:.2f}x the risk-free rate in excess return -- {quality}.")
print()

# ---------------------------------------------------------------------------
# 4. 95% Historical Value at Risk (VaR)
# ---------------------------------------------------------------------------
# VaR answers: "What is the most I should expect to lose on a bad day?"
# At 95% confidence, we are saying: on 95 out of 100 trading days the loss
# will be SMALLER than this number.  The other 5 days (tail risk) may be worse.
#
# "Historical" VaR uses real observed returns, not a bell-curve assumption.
# This is more honest when returns have fat tails (large crashes happen more
# often than a normal distribution predicts).
#
# Method: sort all daily returns from worst to best, then take the 5th
# percentile -- the return that is worse than 95% of all other days.
CONFIDENCE_LEVEL = 0.95
var_percentile   = 1.0 - CONFIDENCE_LEVEL   # = 0.05, i.e. the 5th percentile

# np.percentile(x, 5) finds the value below which 5% of observations fall.
var_daily = np.percentile(portfolio_daily_returns, var_percentile * 100)

# VaR is conventionally expressed as a positive loss figure.
# var_daily will be a negative number (a loss), so we flip the sign.
var_daily_loss = -var_daily

print("=" * 55)
print("95% HISTORICAL VALUE AT RISK (VaR)")
print("=" * 55)
print(f"  Daily VaR (95% confidence)  : {var_daily_loss:>8.4%}")
print()
print("  Plain-English interpretation:")
print(f"  On any given trading day, there is a 95% chance the")
print(f"  equal-weighted portfolio will NOT lose more than {var_daily_loss:.2%}.")
print(f"  Equivalently, on roughly 1 in 20 trading days the loss")
print(f"  could exceed {var_daily_loss:.2%} -- those are the tail-risk days")
print(f"  that need stress-testing or hedging consideration.")
print()

# How many days in history actually breached that threshold?
breach_days = (portfolio_daily_returns < var_daily).sum()
print(f"  Historical check: {breach_days} of {n_days:,} days ({breach_days/n_days:.1%})")
print(f"  exceeded the VaR threshold (expected ~5%, or ~{int(n_days*0.05)} days).")
print()

# ---------------------------------------------------------------------------
# 5. Save summary to CSV
# ---------------------------------------------------------------------------
# One-row DataFrame so every field is clearly labelled for downstream use.
summary = pd.DataFrame([{
    "n_stocks":                n_stocks,
    "weights":                 f"1/{n_stocks} each",
    "risk_free_rate":          RISK_FREE_RATE,
    "annual_portfolio_return": round(annual_portfolio_ret, 6),
    "annual_portfolio_vol":    round(annual_portfolio_vol, 6),
    "sharpe_ratio":            round(sharpe_ratio, 6),
    "var_95_daily_loss":       round(var_daily_loss, 6),
    "var_confidence":          CONFIDENCE_LEVEL,
    "var_method":              "historical",
}])

summary.to_csv("data/raw/portfolio_summary.csv", index=False)
print("=" * 55)
print("Saved to data/raw/portfolio_summary.csv")
print("=" * 55)
print(summary.T.to_string(header=False))
print()
print("SUCCESS: portfolio_summary.csv written to data/raw/")
