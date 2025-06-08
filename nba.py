import pandas as pd
pd.set_option('display.max_columns', None) # so we can see all columns in a wide dataframe
import time
import numpy as np
import requests
import json
import pprint

url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Regular%20Season&StatCategory=PTS'

r = requests.get(url).json()
table_headers = r['resultSet']['headers']

df = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
print(df)


