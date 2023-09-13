import pandas as pd
import yfinance as yf
import datetime
import requests

# nvda = yf.Ticker("NVDA")
# stockinfo = nvda.info
df = pd.DataFrame()

tickers = ['AMZN', 'NEE', 'CSCO', 'DMTK']
for ticker in tickers:
    data = yf.Ticker(ticker)
    price = data.info['currentPrice']

    new_row = {
        "ticker": ticker,
        "price": price
    }

    df = df.append(new_row, ignore_index=True)

print(df)
# for key,value in stockinfo.items():
#     print(key, ":", value)

# print(stockinfo['currentPrice'])
