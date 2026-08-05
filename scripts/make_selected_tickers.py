import pandas as pd

selected = pd.DataFrame([
    {"Symbol": "AAPL",  "Company": "Apple",               "Sector": "Technology",              "Index": "Nasdaq-100"},
    {"Symbol": "MSFT",  "Company": "Microsoft",            "Sector": "Technology",              "Index": "Nasdaq-100"},
    {"Symbol": "AMZN",  "Company": "Amazon",               "Sector": "Consumer Discretionary",  "Index": "Nasdaq-100"},
    {"Symbol": "GOOGL", "Company": "Alphabet (Google)",    "Sector": "Communication Services",  "Index": "Nasdaq-100"},
    {"Symbol": "JNJ",   "Company": "Johnson & Johnson",    "Sector": "Health Care",              "Index": "Dow Jones"},
    {"Symbol": "XOM",   "Company": "Exxon Mobil",          "Sector": "Energy",                  "Index": "Dow Jones"},
    {"Symbol": "JPM",   "Company": "JPMorgan Chase",       "Sector": "Financials",               "Index": "Dow Jones"},
    {"Symbol": "KO",    "Company": "Coca-Cola",            "Sector": "Consumer Staples",         "Index": "Dow Jones"},
    {"Symbol": "PG",    "Company": "Procter & Gamble",     "Sector": "Consumer Staples",         "Index": "Dow Jones"},
    {"Symbol": "CAT",   "Company": "Caterpillar",          "Sector": "Industrials",              "Index": "Dow Jones"},
])
selected.to_csv("data/selected_tickers.csv", index=False)
print(selected)