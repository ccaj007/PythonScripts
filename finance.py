import pandas as pd
import yfinance as yf
import datetime
import requests

df = pd.DataFrame()

# tickers = ['AMZN', 'NEE', 'CSCO', 'DMTK']
# for ticker in tickers:
#     data = yf.Ticker(ticker)
#     price = data.info['currentPrice']

#     new_row = {
#         "ticker": ticker,
#         "price": price
#     }

#     df = df.append(new_row, ignore_index=True)

# print(df)

portfolio = pd.read_csv('F:\Documents\Finance\Portfolio_raw.csv')
sum = 0
for index,row in portfolio.iterrows():
    data = yf.Ticker(row['Ticker'])
    price = data.info['regularMarketPreviousClose']
    value = price * row['Shares']
    sum += value

    new_row = {
        "CompanyName": data.info['shortName'],
        "Ticker": row['Ticker'],
        "Shares": row['Shares'],
        "Price": price,
        "Value": value
    }

    df = df.append(new_row, ignore_index=True)
    #print(data.info['shortName'],row['Ticker'],price, value)

new_row = {
    "CompanyName": "TOTAL",
    "Total": int(sum)
}
df = df.append(new_row, ignore_index=True)
df.to_csv("PortfolioValue.csv", index = False)
print(df)