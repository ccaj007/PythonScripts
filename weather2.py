import requests
from ..keys import OPENWEATHER_API



r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=New York&appid={OPENWEATHER_API}")


print(f"City: {city}")
print(f"Temperature: {temperature}")
print(f"Weather Description: {weather_description}")