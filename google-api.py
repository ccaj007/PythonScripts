import requests
import pandas as pd
import time
from keys import GOOGLE_API_KEY, GOOGLE_CHANNEL_ID

API_KEY = GOOGLE_API_KEY
CHANNEL_ID = GOOGLE_CHANNEL_ID

url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelID="+CHANNEL_ID
response = requests.get(url).json()
print(response)
