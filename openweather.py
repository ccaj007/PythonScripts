from INFO import API_KEYS
import requests

openweather_api = API_KEYS.OPENWEATHERMAP_API

url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={openweather_api}"

r = requests.get(url)

print(r)
