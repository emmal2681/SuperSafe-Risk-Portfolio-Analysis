import pandas as pd
import yfinance as yf
import os
import time

os.makedirs("data/raw", exist_ok=True)

tickers_df = pd.read_csv("data/selected_tickers.csv")
tickers = tickers_df["Symbol"].tolist()

print(f"Downloading data for: {tickers}")

all_closes = {}
for ticker in tickers:
    print(f"  Downloading {ticker}...")
    data = yf.download(ticker, start="2019-01-01", auto_adjust=True)
    if data.empty:
        print(f"  WARNING: {ticker} came back empty, skipping")
        continue

    close_col = data["Close"]
    # .squeeze() flattens a single-column DataFrame down to a plain Series
    close_col = close_col.squeeze()
    all_closes[ticker] = close_col
    time.sleep(1)

close_prices = pd.DataFrame(all_closes)
close_prices = close_prices.ffill()
close_prices = close_prices.dropna(how="all")

close_prices.to_csv("data/raw/close_prices.csv")
print(f"\nSaved {close_prices.shape[0]} days x {close_prices.shape[1]} stocks")
print(f"Stocks included: {list(close_prices.columns)}")
print(close_prices.tail())