import pandas as pd

close_prices = pd.read_csv("data/raw/close_prices.csv", index_col=0, parse_dates=True)

# Daily % returns: (today's price - yesterday's price) / yesterday's price
daily_returns = close_prices.pct_change().dropna()
daily_returns.to_csv("data/raw/daily_returns.csv")

# Individual stock volatility: standard deviation of daily returns,
# annualized by multiplying by sqrt(252) trading days per year
volatility = daily_returns.std() * (252 ** 0.5)
volatility = volatility.sort_values(ascending=False)

print("Annualized volatility by stock:")
print(volatility)

volatility.to_csv("data/raw/individual_volatility.csv", header=["Annualized Volatility"])