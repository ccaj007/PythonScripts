import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

df = pd.read_csv('D:\\repos\\PythonScripts\\portfolio_raw.csv')
print(df)

Portfolio_Total_Amount = sum( df['Quantity'] * df['Price'])
Portfolio_Total_Amount = round(Portfolio_Total_Amount, 2)
print(Portfolio_Total_Amount)

stock_tickers = df['Security'].values
sizes = df['Quantity'] * df['Price']

listofZeros = [0] * df.shape[0]
n = random.randint(0, df.shape[0]-1)
listOfZeros[n] = 0.1
explode = listofZeros

# Create a figure
plt.subplots(figsize = (10,10))
