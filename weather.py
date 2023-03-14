from INFO import API_KEYS
import requests
from bs4 import BeautifulSoup

api_key = API_KEYS.OPENWEATHERMAP_API
city="New York"

# Create the API URL by combining the base URL, the city name, and the API key
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

# Make a GET request to the API URL
response = requests.get(url)
data = response.json()
# Parse the response content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)
#
# Extract the temperature, humidity, and wind speed data from the parsed content
#temperature = soup.find('main', {'class': 'temp'}).get_text()
temperature_k = data['main']['temp']
temperature = round(((temperature_k - 273.15) * 9 / 5 + 32), 2)
humidity = data['main']['humidity']
wind_speed = data['wind']['speed']
#
# Print the weather data
print(f"The temperature in {city} is {temperature}. The humidity is {humidity}. The wind speed is {wind_speed}.")
