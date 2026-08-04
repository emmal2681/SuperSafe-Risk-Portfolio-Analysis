from io import StringIO
import os
import pandas as pd
import requests

# 1. Ensure output folder exists
os.makedirs("data/raw", exist_ok=True)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# --- 1. S&P 500 ---
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
res = requests.get(sp500_url, headers=headers)
sp500_tables = pd.read_html(StringIO(res.text))

sp500 = sp500_tables[0].iloc[:, :3].copy()
sp500.columns = ["Symbol", "Company", "Sector"]
sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=False)
sp500["Index"] = "S&P 500"
sp500.to_csv("data/raw/sp500_constituents.csv", index=False)
print(f"S&P 500: {len(sp500)} companies saved")

# --- 2. Nasdaq-100 ---
nasdaq_url = "https://en.wikipedia.org/wiki/List_of_NASDAQ-100_companies"
res = requests.get(nasdaq_url, headers=headers)
nasdaq_tables = pd.read_html(StringIO(res.text))

# .iloc[:, :3] grabs columns 0, 1, and 2 regardless of exact column title text
nasdaq = nasdaq_tables[0].iloc[:, :3].copy()
nasdaq.columns = ["Symbol", "Company", "Sector"]
nasdaq["Symbol"] = nasdaq["Symbol"].str.replace(".", "-", regex=False)
nasdaq["Index"] = "Nasdaq-100"
nasdaq.to_csv("data/raw/nasdaq100_constituents.csv", index=False)
print(f"Nasdaq-100: {len(nasdaq)} companies saved")

# --- 3. Dow Jones ---
dow_url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
res = requests.get(dow_url, headers=headers)
dow_tables = pd.read_html(StringIO(res.text))

dow = dow_tables[1][["Symbol", "Company", "Sector"]].copy()
dow["Symbol"] = dow["Symbol"].str.replace(".", "-", regex=False)
dow["Index"] = "Dow Jones"
dow.to_csv("data/raw/dow_constituents.csv", index=False)
print(f"Dow Jones: {len(dow)} companies saved")

print("\nSUCCESS: All constituent datasets fetched and saved to 'data/raw/'!")